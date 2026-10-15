#!/usr/bin/env python3
"""Remove torrents from Deluge once they have been seeded long enough.

Talks to the Deluge web UI JSON-RPC API (the same one the exporter uses), so it
only needs the web URL and password. Rules are per tracker host, see config.toml.

A torrent is removed only when *every* rule matching its trackers allows it:

  1. seeded < min_seed_hours            -> keep (hit-and-run protection, hard floor)
  2. min_ratio set and ratio >= it      -> remove
  3. max_seed_hours set and seeded >= it -> remove
  4. otherwise                          -> keep

Private torrents on a tracker with no rule are always kept, so a tracker you
join later is safe until you add a rule for it.
"""

import json
import logging
import os
import sys
import tomllib
from http.cookiejar import CookieJar
from urllib.parse import urlparse
from urllib.request import HTTPCookieProcessor, Request, build_opener

log = logging.getLogger("deluge-cleanup")

STATUS_KEYS = [
    "name",
    "state",
    "progress",
    "ratio",
    "seeding_time",
    "private",
    "label",
    "trackers",
    "tracker_host",
    "total_size",
]

# Only touch torrents that are done downloading. Paused covers torrents Deluge
# stopped itself after hitting a ratio limit; never touch Error/Checking/Moving.
REMOVABLE_STATES = {"Seeding", "Paused", "Queued"}


class DelugeError(RuntimeError):
    pass


class Deluge:
    def __init__(self, url: str, password: str):
        self.url = url.rstrip("/") + "/json"
        self.password = password
        self.opener = build_opener(HTTPCookieProcessor(CookieJar()))
        self._id = 0

    def call(self, method: str, *params):
        self._id += 1
        body = json.dumps({"method": method, "params": list(params), "id": self._id})
        req = Request(
            self.url,
            data=body.encode(),
            headers={"Content-Type": "application/json"},
        )
        with self.opener.open(req, timeout=30) as resp:
            payload = json.load(resp)
        if payload.get("error"):
            raise DelugeError(f"{method}: {payload['error']}")
        return payload["result"]

    def connect(self):
        if not self.call("auth.login", self.password):
            raise DelugeError("auth.login rejected the password")
        if not self.call("web.connected"):
            hosts = self.call("web.get_hosts")
            if not hosts:
                raise DelugeError("web UI has no daemon configured")
            self.call("web.connect", hosts[0][0])

    def torrents(self) -> dict:
        return self.call("core.get_torrents_status", {}, STATUS_KEYS)

    def remove(self, torrent_id: str, remove_data: bool) -> bool:
        return bool(self.call("core.remove_torrent", torrent_id, remove_data))


def tracker_hosts(torrent: dict) -> set[str]:
    hosts = set()
    for tracker in torrent.get("trackers") or []:
        host = urlparse(tracker.get("url", "")).hostname
        if host:
            hosts.add(host.lower())
    if torrent.get("tracker_host"):
        hosts.add(torrent["tracker_host"].lower())
    return hosts


def host_matches(host: str, pattern: str) -> bool:
    pattern = pattern.lower()
    return host == pattern or host.endswith("." + pattern)


def matching_rules(config: dict, torrent: dict) -> list[tuple[str, dict]]:
    hosts = tracker_hosts(torrent)
    rules = [
        (name, rule)
        for name, rule in config.get("tracker", {}).items()
        if any(host_matches(h, p) for h in hosts for p in rule.get("hosts", []))
    ]
    if not rules and not torrent.get("private") and "public" in config:
        rules = [("public", config["public"])]
    return rules


def check_rule(rule: dict, torrent: dict) -> tuple[bool, str]:
    seeded_hours = torrent["seeding_time"] / 3600
    ratio = torrent["ratio"]
    if seeded_hours < rule.get("min_seed_hours", 0):
        return False, f"seeded {seeded_hours:.1f}h < min {rule['min_seed_hours']}h"
    if "min_ratio" in rule and ratio >= rule["min_ratio"]:
        return True, f"ratio {ratio:.2f} >= {rule['min_ratio']}"
    if "max_seed_hours" in rule and seeded_hours >= rule["max_seed_hours"]:
        return True, f"seeded {seeded_hours:.1f}h >= max {rule['max_seed_hours']}h"
    return False, f"ratio {ratio:.2f}, seeded {seeded_hours:.1f}h, no limit reached"


def decide(config: dict, torrent: dict) -> tuple[bool, str]:
    """Return (remove, reason) for one torrent."""
    if torrent["state"] not in REMOVABLE_STATES:
        return False, f"state {torrent['state']}"
    if torrent["progress"] < 100:
        return False, "not fully downloaded"
    if torrent.get("label") in config.get("protected_labels", []):
        return False, f"protected label {torrent['label']!r}"

    rules = matching_rules(config, torrent)
    if not rules:
        kind = "private" if torrent.get("private") else "public"
        return False, f"{kind} torrent with no rule ({', '.join(sorted(tracker_hosts(torrent))) or 'no tracker'})"

    reasons = []
    for name, rule in rules:
        ok, why = check_rule(rule, torrent)
        reasons.append(f"{name}: {why}")
        if not ok:
            return False, "; ".join(reasons)
    return True, "; ".join(reasons)


def main() -> int:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    with open(os.environ.get("CONFIG_PATH", "/config/config.toml"), "rb") as f:
        config = tomllib.load(f)

    # DRY_RUN env wins so a one-off `kubectl create job --from` can flip it.
    dry_run = os.environ.get("DRY_RUN", str(config.get("dry_run", True))).lower() in ("1", "true", "yes")
    remove_data = config.get("remove_data", True)
    max_removals = config.get("max_removals_per_run", 10)

    client = Deluge(
        os.environ.get("DELUGE_URL", "http://deluge.media.svc:8112"),
        os.environ["DELUGE_PASSWORD"],
    )
    client.connect()
    torrents = client.torrents()
    log.info("%d torrents in Deluge, dry_run=%s, remove_data=%s", len(torrents), dry_run, remove_data)

    candidates = []
    for torrent_id, torrent in torrents.items():
        remove, reason = decide(config, torrent)
        log.debug("%s %s: %s", "REMOVE" if remove else "keep", torrent["name"], reason)
        if remove:
            candidates.append((torrent_id, torrent, reason))

    # Oldest-seeded first, so the cap trims the most overdue torrents.
    candidates.sort(key=lambda c: c[1]["seeding_time"], reverse=True)
    if len(candidates) > max_removals:
        log.warning(
            "%d torrents eligible, capped at max_removals_per_run=%d; the rest wait for the next run",
            len(candidates),
            max_removals,
        )
        candidates = candidates[:max_removals]

    failures = 0
    freed = 0
    for torrent_id, torrent, reason in candidates:
        action = "would remove" if dry_run else "removing"
        log.info("%s %s (%.1f GiB): %s", action, torrent["name"], torrent["total_size"] / 2**30, reason)
        if dry_run:
            continue
        try:
            if client.remove(torrent_id, remove_data):
                freed += torrent["total_size"]
            else:
                failures += 1
                log.error("Deluge refused to remove %s", torrent["name"])
        except DelugeError as e:
            failures += 1
            log.error("failed to remove %s: %s", torrent["name"], e)

    log.info(
        "done: %d %s, %.1f GiB %s, %d failures",
        len(candidates),
        "eligible" if dry_run else "processed",
        freed / 2**30 if not dry_run else sum(c[1]["total_size"] for c in candidates) / 2**30,
        "reclaimable" if dry_run else "freed",
        failures,
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
