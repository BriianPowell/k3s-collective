# Secrets Management

Cluster secrets are synced from **1Password** via the [1Password Connect Kubernetes operator](https://developer.1password.com/docs/k8s/operator). Each `OnePasswordItem` creates a `Secret` with the same name in the CR’s namespace. **Field labels in 1Password must match the Kubernetes secret keys** your manifests reference (`secretKeyRef.key`, Helm `existingSecret`, etc.).

## Operator bootstrap (once, not in git)

```sh
kubectl -n onepassword create secret generic op-credentials \
  --from-file=1password-credentials.json=/path/to/1password-credentials.json

kubectl -n onepassword create secret generic onepassword-token \
  --from-literal=token='YOUR_CONNECT_TOKEN'
```

The operator is deployed by Flux (`infrastructure/controllers/onepassword.yaml`). It polls 1Password every 10 minutes (`pollingInterval: 600`) and can restart workloads when secrets change (`autoRestart: true`).

## Where secrets live in git

| Secret | Manifest | Namespace | Flux kustomization |
|--------|----------|-----------|-------------------|
| Cloudflare API token | `infrastructure/configs/onepassword-item.yaml` | `cert-manager` | `infra-configs` |
| CrowdSec enroll key | `infrastructure/controllers/crowdsec-onepassword-item.yaml` | `crowdsec` | `infra-controllers` |
| AdGuard exporter | `apps/base/adguard/onepassword-item.yaml` | `adguard` | `base` |
| Forward Auth (OIDC) | `apps/base/forward-auth/onepassword-item.yaml` | `kube-system` | `kube-system` |
| Home Assistant | `apps/base/homeassistant/onepassword-item.yaml` | `homeassistant` | `base` |
| Keycloak | `apps/base/keycloak/onepassword-item.yaml` | `keycloak` | `base` |
| Nextcloud + SMTP | `apps/base/nextcloud/onepassword-item.yaml` | `nextcloud` | `base` |
| Alertmanager SMTP | `apps/monitoring/alert-manager/onepassword-item.yaml` | `monitoring` | `monitoring` |
| Grafana | `apps/monitoring/grafana/onepassword-item.yaml` | `monitoring` | `monitoring` |
| Prometheus (HA token) | `apps/monitoring/prometheus/onepassword-item.yaml` | `monitoring` | `monitoring` |
| Arr stack (exportarr + Recyclarr) | `apps/media/arr-stack/onepassword-item.yaml` | `media` | `media` |
| Deluge | `apps/media/deluge/onepassword-item.yaml` | `media` | `media` |
| Valheim | `apps/games/valheim/onepassword-item.yaml` | `valheim` | `games` |
| V Rising | `apps/games/v-rising/onepassword-item.yaml` | `v-rising` | `games` |

Cloudflare DNS-01 setup is documented in [infrastructure/configs/README.md](../configs/README.md).

Adjust `spec.itemPath` in each manifest if your vault or item title differs from `vaults/Collective/items/<Title>`.

## Verify any secret

```sh
kubectl -n <namespace> get onepassworditem,secret <name>
kubectl -n <namespace> get secret <name> -o json | jq -r '.data | keys[]'
```

## Per-application fields

### Cloudflare (cert-manager)

Item **Cloudflare**, field `api-token` → `Secret/cloudflare-api-token` (key `api-token`). See [configs README](../configs/README.md).

### CrowdSec

| Label | Used by |
|-------|---------|
| `ENROLL_KEY` | CrowdSec Console enrollment (`HelmRelease/crowdsec` LAPI) |

[CrowdSec Console](https://app.crowdsec.net/) → create instance / enroll key.

### AdGuard (exporter API)

| Label | Used by |
|-------|---------|
| `USERNAMES` | AdGuard exporter |
| `PASSWORDS` | AdGuard exporter |

AdGuard Home UI auth in `helm-release.yaml` is separate (bcrypt in values).

### Traefik Forward Auth (OIDC)

| Label | Used as |
|-------|---------|
| `client-id` | `PROVIDERS_OIDC_CLIENT_ID` |
| `client-secret` | `PROVIDERS_OIDC_CLIENT_SECRET` |
| `secret` | `SECRET` (cookie signing) |

### Home Assistant

| Label | Used by |
|-------|---------|
| `secrets.yaml` | Multiline file mounted to `/config/secrets.yaml` |
| `token` | Also synced to `Secret/prometheus` in `monitoring` for Prometheus scrape |
| `mqtt-username` | Mosquitto broker init container |
| `mqtt-password` | Mosquitto broker init container |

**Prometheus token:** Home Assistant → Profile → Security → Long-Lived Access Tokens. Same 1Password item, field `token`.

**MQTT:** Add matching `MQTT_USERNAME` and `MQTT_PASSWORD` entries to the `secrets.yaml` field content (same values as `mqtt-username` / `mqtt-password`). LAN devices connect to `abaddon:1883` with those credentials.

### Keycloak

| Label | Notes |
|-------|-------|
| `DOMAIN` | `KC_HOSTNAME` (e.g. `keycloak.powell.place`) |
| `KC_ADMN` | Optional legacy bootstrap username |
| `KC_PASS` | Optional legacy bootstrap password |

Postgres: CNPG `Secret/keycloak-pgcluster-app`, not this secret.

### Nextcloud

**Item Nextcloud** → `Secret/nextcloud`:

| Label | Used by |
|-------|---------|
| `username` | `NEXTCLOUD_ADMIN_USER` |
| `password` | `NEXTCLOUD_ADMIN_PASSWORD` |
| `trusted_domains` | `NEXTCLOUD_TRUSTED_DOMAINS` |
| `mail_from_address` | `MAIL_FROM_ADDRESS` |
| `token` | nextcloud-exporter `NEXTCLOUD_AUTH_TOKEN` |

**Item SMTP Secondary** → `Secret/nextcloud-smtp`:

| Label | Used by |
|-------|---------|
| `username` | `SMTP_NAME` |
| `password` | `SMTP_PASSWORD` |

Postgres: CNPG `Secret/nextcloud-pgcluster-app`.

Exporter token: `occ config:app:set serverinfo token` in Nextcloud, or use app-password env vars per [exportarr docs](https://github.com/xperimental/nextcloud-exporter).

### Alertmanager

Config (routes, receivers, SMTP host/user) lives in git: `apps/monitoring/alert-manager/alertmanager.yaml`.

| Label | Mounted at |
|-------|------------|
| `password` | iCloud app-specific SMTP password → mounted as `/etc/alertmanager/secrets/smtp_auth_password` |

Item **SMTP** (Login) in vault **Collective** → `Secret/alertmanager-smtp`. Use a **password** field (standard Login field); the deployment renames it to the path Alertmanager expects.

### Grafana

| Label | Used by |
|-------|---------|
| `USER` | Admin username |
| `PASS` | Admin password |
| `CLIENT_ID` | Keycloak OAuth |
| `CLIENT_SECRET` | Keycloak OAuth |
| `AUTH_URL` | Keycloak authorization endpoint |
| `TOKEN_URL` | Keycloak token endpoint |
| `API_URL` | Keycloak userinfo endpoint |
| `LOGOUT_URL` | Keycloak logout redirect |

Keycloak realm **inferno** well-known: `https://keycloak.powell.place/realms/inferno/.well-known/openid-configuration`.

### Arr stack (exportarr + Recyclarr)

Item **Arr Stack** → `Secret/arr-stack` in `media`:

| Label | Used by |
|-------|---------|
| `bazarr_api_key` | Bazarr exportarr |
| `bazarr_anime_api_key` | Bazarr Anime exportarr |
| `lidarr_api_key` | Lidarr exportarr |
| `prowlarr_api_key` | Prowlarr exportarr |
| `radarr_api_key` | Radarr exportarr |
| `readarr_api_key` | Readarr exportarr |
| `sonarr_tv_api_key` | Sonarr TV exportarr |
| `sonarr_anime_api_key` | Sonarr Anime exportarr |
| `plex_token` | Plex exporter |
| `seerr_api_key` | Seerr exporter |
| `tautulli_api_key` | Tautulli exporter |
| `secrets.yml` | Recyclarr (multiline YAML → `/config/secrets.yml`) |

Example `secrets.yml` (plain YAML in 1Password, no markdown fences):

```yaml
radarr_url: http://radarr.media.svc:7878
radarr_api_key: <api-key>
sonarr_tv_url: http://sonarr-tv.media.svc:8989
sonarr_tv_api_key: <api-key>
```

After changing keys:

```sh
kubectl -n media rollout restart deploy/recyclarr
for d in $(kubectl -n media get deploy -o name | grep exportarr); do kubectl -n media rollout restart "$d"; done
```

### Deluge

| Label | Used by |
|-------|---------|
| `VPN_USER` | Deluge deployment (PIA WireGuard) |
| `VPN_PASS` | Deluge deployment |
| `APP_PASS` | deluge-exporter (Web UI password) |

### Valheim / V Rising

| Label | Used by |
|-------|---------|
| `password` | Server password (`SERVER_PASS` / `VR_PASSWORD`; min 5 chars for Valheim) |

## Local migration files (gitignored)

Plaintext `*-secret.yaml` under this directory (if present) are for one-off migration only and must not be committed. Use them to copy values into 1Password, then delete locally.

## Uninstalling the old Sealed Secrets controller

If the cluster still runs the Bitnami controller from the previous setup, remove it after all apps use 1Password:

```sh
flux delete helmrelease sealed-secrets -n flux-system --silent
flux delete source helm sealed-secrets -n flux-system --silent
kubectl delete sealedsecrets --all-namespaces --all
```
