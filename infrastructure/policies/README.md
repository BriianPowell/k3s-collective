# Cluster network policies

Ingress-focused policies aligned with the [K3s CIS hardening guide](https://docs.k3s.io/security/hardening-guide#networkpolicies).

## Coverage

| Policy | Namespaces |
| -------- | ------------ |
| `standard-ingress` | `media`, `monitoring`, `crowdsec`, `cert-manager`, `reflector`, `reloader` — Traefik pods, Prometheus pods and the namespace itself (cert-manager, reflector, reloader: no Traefik) |
| `standard-egress` | `cert-manager`, `reflector`, `reloader` — LAN + cluster CIDRs + kube-system + monitoring + DNS + WAN :80/:443 |
| `allow-all-egress` | `media` (only Deluge is left: VPN) — arbitrary ports (torrent/VPN); every other media app has its own egress policy in `manifests/media-egress.yaml` and is excluded here (`manifests/permissive-egress.yaml`) |
| `monitoring-base-egress` + per-component | `monitoring` — DNS + same namespace for all; Prometheus pod CIDR and node metric ports, API-server access for Prometheus/Alloy/kube-state-metrics/operator, Alertmanager SMTP :587, Grafana WAN :80/:443 (`manifests/monitoring-egress.yaml`) |
| `crowdsec-base-egress`, `crowdsec-internet-egress` | `crowdsec` — DNS + same namespace; LAPI and agent reach the internet on :80/:443 for hub and CAPI (`manifests/crowdsec-egress.yaml`) |
| `adguard-base-egress`, `adguard-home-egress` | `adguard` — DNS + same namespace; AdGuard reaches public IPs on TCP 443/853 and 53 (DoH/DoT upstreams, bootstrap, filter lists). Add a port here if you add an upstream on another one (`manifests/adguard-egress.yaml`) |
| `bazarr-egress`, `kapowarr-egress` | `media` Bazarr (both) and Kapowarr — DNS + WAN :80/:443, private ranges blocked; Bazarr also reaches Sonarr/Radarr (`manifests/media-egress.yaml`) |
| `plex-egress` | `media` Plex pod only — DNS + WAN :80/:443, private ranges blocked (`manifests/plex-egress.yaml`) |
| `flaresolverr-egress` | `media` FlareSolverr pod only — DNS + WAN :80/:443, private ranges blocked (`manifests/flaresolverr-egress.yaml`) |
| `radarr-ingress`, `sonarr-tv-ingress`, `sonarr-anime-ingress`, `prowlarr-ingress` | `media` core *arr pods — ingress only from Traefik, monitoring and named callers on the app port; excluded from `standard-ingress` (`manifests/media-ingress.yaml`) |
| `deluge-ingress` | `media` Deluge — :8112 from Traefik, Radarr, Sonarr (both), Prowlarr, Lidarr, Readarr and its exporter; daemon :58846 from tqm only; excluded from `standard-ingress` (`manifests/media-ingress.yaml`) |
| `bazarr-ingress`, `kapowarr-ingress` | `media` Bazarr (both) and Kapowarr — ingress only from Traefik (and Bazarr's own exporters); excluded from `standard-ingress` (`manifests/media-ingress.yaml`) |
| `flaresolverr-ingress` | `media` FlareSolverr — ingress only from Prowlarr (:8191) and monitoring (:8192); no Traefik route; excluded from `standard-ingress` (`manifests/media-ingress.yaml`) |
| `media-container-limits` | `media` — per-container/pod/PVC min/max and defaults |
| `standard-ingress` + CNPG | `homeassistant`, `nextcloud`, `keycloak`, `wiki`, `atuin` — as above plus the CloudNativePG operator pod |
| `standard-egress` + CNPG | `homeassistant`, `nextcloud`, `keycloak`, `wiki` — adds `cnpg-system` to egress |
| `renovate-ingress`, `renovate-egress` | `renovate` — no ingress at all; egress to DNS and public HTTPS :443 only, private ranges blocked (`manifests/renovate-network.yaml`) |
| `atuin-base-egress`, `atuin-pgcluster-egress` | `atuin` — DNS + same namespace; Postgres pod also reaches the API server only; nothing to LAN or internet (`manifests/atuin-egress.yaml`) |
| `adguard-home-ingress`, `adguard-exporter-ingress` | `adguard` — UI from Traefik :80, exporter from AdGuard, DNS ports (53, 853, 784, 8853, 5443) from RFC1918 sources only; exporter :9618 from `monitoring` (`manifests/adguard-ingress.yaml`) |
| `minecraft-ingress`, `valheim-ingress`, `v-rising-ingress` | game namespaces — Traefik pods only, on each game's ports (`manifests/games-ingress.yaml`; games suspended, untested live) |
| `allow-all-egress` | `minecraft`, `valheim`, `v-rising` |
| `kube-system` bundle | `kube-system` (intra-ns, DNS :53, CoreDNS metrics :9153, ntfy :80, Traefik, metrics-server) |

**No policies:** `flux-system`, `cnpg-system`, `onepassword` — operators and webhooks need broader reach.

## Pod Security Admission

Enforced per namespace by a label in `infrastructure/namespaces/<ns>.yaml`. Before changing a level,
dry-run it: `kubectl label --dry-run=server --overwrite ns <ns> pod-security.kubernetes.io/enforce=<level>`
lists the pods that would break.

| Level | Namespaces |
| ----- | ---------- |
| `restricted` | `atuin`, `renovate`, `cert-manager`, `cnpg-system`, `onepassword`, `wiki`, `flux-system`, `adguard`, `reflector`, `reloader` |
| `baseline` | `nextcloud` (Apache and cron start as root), `keycloak`, `minecraft`, `valheim`, `v-rising` (suspended) |
| `privileged` | `media` (Deluge: NET_ADMIN, hostPath, sysctls), `monitoring` (node-exporter host namespaces, smartctl), `kube-system` (k3s system pods), `homeassistant` (`hostNetwork` for HomeKit), `crowdsec` (agent mounts the node's container logs) |

A `privileged` namespace needs a stated reason. Splitting the one or two pods that need it into their
own namespace would let the rest tighten, at the cost of renaming their Service DNS names.

## Apply

Flux kustomization `infra-policies` (after `infra-namespaces`).

```bash
flux reconcile kustomization infra-policies -n flux-system --with-source
```

## Host hardening (sheol)

See `nix-config/hosts/sheol/kubernetes.nix`: `secrets-encryption`, `protect-kernel-defaults`, API audit logs, PKI `chmod` (activation + `k3s-pki-permissions` oneshot after `k3s`). Apply on sheol: `sudo nixos-rebuild switch`, then `systemctl start k3s-pki-permissions` (or reboot).

## Housekeeping (excluding backups)

| # | Item | Status |
| --- | ------ | -------- |
| 1 | Revision caps (`revisionHistoryLimit` / `maxHistory: 3`) | done |
| 2 | CrowdSec bouncer `updateMaxFailure: -1` | done |
| 3 | Idle games: `games` Kustomization + HelmRelease `suspend` | done |
| 4 | CronJob: prune succeeded Jobs cluster-wide | done |
| 5 | `LimitRange` in `media` (and optionally `monitoring`) | done |
| 6 | PDBs for Traefik, Prometheus, Grafana, CrowdSec LAPI | done |
| 7 | CIS: `automountServiceAccountToken: false` on default SAs | done |
| 8 | sheol PKI `chmod 600` on k3s server TLS material | done |
| 9 | Prometheus alerts (cert expiry, Flux Not Ready, disk, PVC) | done |
| 10 | Loki retention vs disk budget | done |
| 11 | Egress network policies per namespace | done |
| 12 | Ops runbook (CrowdSec unban, Flux reconcile, game resume) | done — [OPS.md](./OPS.md) |

Periodic ops (no git): `k3s-remove-unused-rs`, `crictl rmi --prune`, orphan PVC review.

**Alerts** (`apps/monitoring/prometheus/rules.yaml` → `monitor-custom-rules`): cert-manager expiry (21d/7d), Flux Not Ready (excludes `suspend: true`), PVC over 85% full; node disk already in `High Node Disk Usage`; default `KubePersistentVolumeFillingUp` at ~97%.

**Loki** (`apps/monitoring/loki/helm-release.yaml`): 3d retention (`72h`), compactor enabled, PVC `10Gi`, memcached caches + canary disabled, lighter single-binary resources (debug-only).

**Alloy / log dashboards:** allowlist in `apps/monitoring/alloy/config.yaml`; Grafana log panels use `{namespace,pod}` LogQL ([grafana-dashboards](https://github.com/BriianPowell/grafana-dashboards)). Game and monitoring log folders removed from Grafana Helm provisioning.

## Later (optional)

- Global PSA via `/var/lib/rancher/k3s/server/psa.yaml` with `kube-system` exempt (the per-namespace labels above already cover it; this would only set a default for new namespaces).
- Tighten `allow-all-egress` namespaces (e.g. media torrent ports only) once traffic patterns are known.
- CIS 5.1.5: extend default SA hardening to `kube-system` / `flux-system` / operators after testing (see second document in each `infrastructure/namespaces/*.yaml` except operator/core namespaces).
