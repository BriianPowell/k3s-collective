# Hostname Migration Plan: Functional URLs

## Goal

Replace app-branded subdomains (e.g. `radarr.powell.place`) with subdomains that
describe what the service actually does (e.g. `movies.powell.place`). This
covers **all** apps, including infra/admin tools, per decision on 2026-09-23.

DNS and TLS are already domain-agnostic (wildcard `*.powell.place` cert in
`infrastructure/configs/certificate.yaml`, and presumably a wildcard rewrite in
AdGuard — **needs verification**, see Phase 0), so most renames are just an
`IngressRoute` host swap. The risk is entirely in the handful of apps that
have the old hostname hardcoded somewhere *other* than their own
`ingress.yaml`, or that are integrated with Keycloak SSO / external clients.

## Final naming table

| Category | App | Current host | New host | In-repo ingress file |
| --- | --- | --- | --- | --- |
| Media | Radarr | `radarr` | `movies` | `apps/media/radarr/ingress.yaml` |
| Media | Sonarr (TV) | `sonarr-tv` | `tv` | `apps/media/sonarr-tv/ingress.yaml` |
| Media | Sonarr (Anime) | `sonarr-anime` | `tv-anime` | `apps/media/sonarr-anime/ingress.yaml` |
| Media | Lidarr | `lidarr` | `music` | `apps/media/lidarr/ingress.yaml` |
| Media | Readarr | `readarr` | `library` | `apps/media/readarr/ingress.yaml` |
| Media | Kapowarr | `kapowarr` | `comics` | `apps/media/kapowarr/ingress.yaml` |
| Media | Bazarr | `bazarr` | `subtitles` | `apps/media/bazarr/ingress.yaml` |
| Media | Bazarr (Anime) | `bazarr-anime` | `subtitles-anime` | `apps/media/bazarr-anime/ingress.yaml` |
| Media | Prowlarr | `prowlarr` | `indexers` | `apps/media/prowlarr/ingress.yaml` |
| Media | Plex | `plex` | `watch` | `apps/media/plex/ingress.yaml` |
| Media | Kavita | `kavita` | `books` | `apps/media/kavita/ingress.yaml` |
| Media | Tautulli | `tautulli` | `watch-stats` | `apps/media/tautulli/ingress.yaml` |
| Media | Deluge | `deluge` | `downloads` | `apps/media/deluge/ingress.yaml` |
| Media | FlareSolverr | `flaresolverr` | *(no rename — internal only, see note)* | `apps/media/flaresolverr/ingress.yaml` |
| Media | Seerr | `requests` | *(already renamed, no change)* | `apps/media/seerr/ingress.yaml` |
| Infra | Grafana | `grafana` | `dashboards` | `apps/monitoring/grafana/ingress.yaml` |
| Infra | Prometheus | `prometheus` | `metrics` | `apps/monitoring/prometheus/ingress.yaml` |
| Infra | Alertmanager | `alertmanager` | `alerts` | `apps/monitoring/alert-manager/ingress.yaml` |
| Infra | Traefik dashboard | `traefik` | `proxy` | `apps/base/traefik/ingress.yaml` |
| Infra | AdGuard Home | `guard` | `dns` | `apps/base/adguard/ingress.yaml` |
| Infra | Keycloak | `keycloak` | `identity` | `apps/base/keycloak/ingress.yaml` |
| Infra | Alloy | `alloy` | `telemetry` | `apps/monitoring/alloy/ingress.yaml` |
| Infra | Atuin | `atuin` | `history` | `apps/utilities/atuin/ingress.yaml` |
| Infra | ntfy | `ntfy` | `notify` | `apps/utilities/ntfy/ingress.yaml` |
| Infra | Nextcloud | `nextcloud` | `cloud` | `apps/base/nextcloud/ingress.yaml` |
| Infra | Home Assistant | `hass` | `home` | `apps/base/homeassistant/ingress.yaml` |
| Infra | Wiki.js | `wiki` | *(already functional, no change)* | `apps/base/wiki-js/ingress.yaml` |
| Infra | forward-auth | `auth` | *(already functional, no change)* | `apps/base/forward-auth/ingress.yaml` |

**Note on FlareSolverr:** it's a CAPTCHA-solving proxy consumed internally by
Prowlarr, not something a human visits. Recommend dropping its public ingress
entirely rather than renaming it — flag for a separate decision, not part of
this migration.

## Cross-file / cross-repo dependencies discovered

These are places where the *old* hostname is hardcoded outside the app's own
`ingress.yaml`. Every one of these needs to be updated **in the same change**
as its ingress, or the app will break even though DNS/TLS still resolve.

| Old hostname | File | What breaks if missed |
| --- | --- | --- |
| `prometheus.powell.place` | `infrastructure/controllers/kube-prometheus-stack/helm-release.yaml:166` (`externalUrl`) | Alert links / UI links point to dead host |
| `alertmanager.powell.place` | `apps/monitoring/alert-manager/deployment.yaml:11` (`externalUrl`) | Same as above, for Alertmanager |
| `ntfy.powell.place` | `apps/utilities/ntfy/deployment.yaml:71` | ntfy's `NTFY_BASE_URL` — push links/QR codes break |
| `grafana.powell.place` | `apps/monitoring/grafana/helm-release.yaml:220` (`root_url`) | OAuth callback + asset URLs break |
| `keycloak.powell.place` | `apps/monitoring/grafana/helm-release.yaml:225` (commented `signout_redirect_url`) | Cosmetic (already commented out), but update if uncommented later |
| `nextcloud.powell.place` | `apps/base/nextcloud/deployment.yaml:123` (`OVERWRITEHOST`) | Nextcloud generates broken absolute URLs (shares, previews, CalDAV/CardDAV) |
| `auth.powell.place` | `apps/base/forward-auth/config.yaml:13` (`AUTH_HOST`) | forward-auth's own OAuth callback breaks — **this would lock everyone out of every SSO-protected app** |
| `keycloak.powell.place` | `apps/base/forward-auth/config.yaml:16` (`PROVIDERS_OIDC_ISSUER_URL`) | Same — forward-auth can't reach the OIDC issuer, SSO login breaks cluster-wide |
| `atuin.powell.place` | `nix-config/home/atuin/README.md:7`, `nix-config/home/modules/atuin.nix:45` (`sync_address`) | Shell history sync breaks on **every machine** until each is rebuilt with the new config |

**Not found in git (config lives outside this repo / in a running service's own DB — must be changed by hand):**

- **Keycloak realm client redirect URIs.** Any client (Grafana, forward-auth,
  anything else using `auth.generic_oauth`) has a "Valid Redirect URIs" list
  configured live in the Keycloak admin console for realm `inferno`. Renaming
  `grafana` → `dashboards`, `auth` → *(unchanged)*, or `keycloak` → `identity`
  requires updating these by hand in the Keycloak UI, in the same
  maintenance window as the code change. There is no realm-import file in
  git to grep, so this has to be checked live, per client.
- **Grafana OAuth env vars** (`auth_url`, `token_url`, `user_info_url`,
  `logout_url` in `apps/monitoring/grafana/helm-release.yaml`) are populated
  from a secret (likely 1Password-synced) that isn't in git. If Keycloak's
  hostname changes, that secret's values need updating too.
- **Nextcloud `NEXTCLOUD_TRUSTED_DOMAINS`** comes from a secret
  (`nextcloud` secret, key `trusted_domains`), not a plain env value. Adding
  the new hostname there (and removing the old one once cut over) has to
  happen out-of-band, or Nextcloud will show "Access through untrusted
  domain" for the new URL.
- **AdGuard Home DNS rewrites.** Need to confirm whether local DNS resolution
  for `*.powell.place` is one wildcard rewrite (nothing to do) or individual
  per-host rewrites (each renamed host needs a new rewrite entry, since
  that config lives in AdGuard's own database, not git).
- **Client-side configuration on every device:** Nextcloud desktop/mobile
  sync clients, Plex mobile/TV apps (server discovery may still work via
  Plex.tv relay, but manual "custom server" entries won't), any bookmarks,
  home screen shortcuts, and HomeKit/HomeAssistant companion apps.

## Risk tiers / suggested rollout order

**Tier 1 — Low risk, no external references found.** Safe to batch together:
Radarr, Sonarr (TV + Anime), Lidarr, Readarr, Kapowarr, Bazarr (+ anime),
Prowlarr, Kavita, Deluge, Home Assistant, Wiki.js *(no-op)*.

**Tier 2 — Low-medium risk, one extra file to update, no live/manual config:**
Plex → `watch` (check Tautulli's `PLEX_URL`-style env if any point at
`plex.powell.place` directly — verify before cutover), Tautulli → `watch-stats`,
ntfy → `notify` (update `deployment.yaml`).

**Tier 3 — Medium risk, has a live out-of-band dependency:**
Nextcloud → `cloud` (update `OVERWRITEHOST` **and** the `trusted_domains`
secret in the same window; warn household members their sync clients will
need re-pointing).

**Tier 4 — High risk, SSO-linked, requires coordinated multi-system change.**
Do these last, one at a time, with a rollback plan (see below):

- Grafana → `dashboards` (update `root_url` + Keycloak client redirect URI)
- Traefik dashboard → `proxy`, Alertmanager → `alerts`, Prometheus → `metrics`,
  Alloy → `telemetry` (all behind forward-auth; confirm forward-auth's
  `DOMAINS`/`COOKIE_DOMAIN` being apex-wide means these don't need any
  forward-auth config change — only their own `externalUrl`/ingress)
- AdGuard → `dns` (verify this isn't also how you access router-adjacent
  admin during an incident — keep the old host as a fallback longer here)
- Atuin → `history` (update ingress **and** `nix-config`, then rebuild/switch
  every machine before removing the old host)
- Keycloak → `identity` **and** forward-auth → keep `auth` as-is, but update
  `PROVIDERS_OIDC_ISSUER_URL` to the new Keycloak host. Do this last: if it's
  wrong, you lose SSO login to every protected app simultaneously, including
  Keycloak's own admin console if that's also gated.

## Rollback safety net

For Tier 3/4 apps, keep the **old** `IngressRoute` (old hostname) alive
alongside the new one for a cool-down period (recommend 1–2 weeks) instead of
a hard cutover — i.e. add the new `Host()` match rather than replacing it,
then remove the old one in a follow-up commit once nothing is hitting it
(check Traefik access logs / Prometheus `traefik_service_requests_total` by
host for the old hostname before removing).

## Open questions before implementation

1. Confirm AdGuard's DNS rewrite is a single wildcard vs. per-host entries.
2. ~~Confirm whether Tautulli has Plex's URL hardcoded~~ — checked
   `apps/media/tautulli/*.yaml`, no `plex.powell.place` reference found (it
   talks to Plex over the internal service address). No extra change needed.
3. Decide on FlareSolverr: drop public ingress vs. rename.
4. Confirm timing for the Atuin rename, since it requires a `nixos-rebuild`/
   `darwin-rebuild` on every machine to avoid a sync outage.
