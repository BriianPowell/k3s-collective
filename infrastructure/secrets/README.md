# Secrets Management

## 1Password Operator

Bootstrap (once, not in git):

```sh
kubectl -n onepassword create secret generic op-credentials \
  --from-file=1password-credentials.json=/path/to/1password-credentials.json

kubectl -n onepassword create secret generic onepassword-token \
  --from-literal=token='YOUR_CONNECT_TOKEN'
```

App secrets use `OnePasswordItem` CRs (see `apps/base/*/onepassword-item.yaml`, `apps/media/*/onepassword-item.yaml`, `apps/games/*/onepassword-item.yaml`, and this directory for cluster-wide secrets). The operator creates a `Secret` with the same name as the CR. **Field labels in 1Password must match the Kubernetes secret keys** your apps reference (`secretKeyRef.key`).

### Keycloak

`apps/base/keycloak/onepassword-item.yaml` → `Secret/keycloak` in `keycloak` (deployed with the `base` Flux kustomization).

| Label | Used by |
|-------|---------|
| `DOMAIN` | `KC_HOSTNAME` (e.g. `keycloak.powell.place`) |
| `KC_ADMN` | Legacy / optional bootstrap admin username (typo preserved for key parity; `KEYCLOAK_ADMIN` is commented out in deployment) |
| `KC_PASS` | Legacy / optional bootstrap admin password (`KEYCLOAK_ADMIN_PASSWORD` commented out) |

Postgres credentials come from CNPG `Secret/keycloak-pgcluster-app`, not this secret.

1. In vault **Collective**, create item **Keycloak** with those three fields (labels must match exactly, including `KC_ADMN`).

2. Copy before cutover:

   ```sh
   kubectl -n keycloak get secret keycloak -o json | jq -r '.data | keys[]'
   kubectl -n keycloak get secret keycloak -o jsonpath='{.data.DOMAIN}' | base64 -d; echo
   ```

   Or decode from local `infrastructure/secrets/keycloak-secret.yaml` (gitignored).

3. Verify:

   ```sh
   kubectl -n keycloak get onepassworditem,secret keycloak
   kubectl -n keycloak get pods -l app.kubernetes.io/name=keycloak
   ```

4. Remove legacy: `kubectl -n keycloak delete sealedsecret keycloak`

### Nextcloud

`apps/base/nextcloud/onepassword-item.yaml` → `Secret/nextcloud` in `nextcloud` (deployed with the `base` Flux kustomization).

| Label | Used by |
|-------|---------|
| `ADMIN_USER` | `NEXTCLOUD_ADMIN_USER` |
| `ADMIN_PASS` | `NEXTCLOUD_ADMIN_PASSWORD` |
| `DOMAIN` | `NEXTCLOUD_TRUSTED_DOMAINS` |
| `SMTP_NAME` | `SMTP_NAME` |
| `SMTP_PASSWORD` | `SMTP_PASSWORD` |
| `MAIL_FROM_ADDRESS` | `MAIL_FROM_ADDRESS` |
| `TOKEN` | nextcloud-exporter `NEXTCLOUD_AUTH_TOKEN` |
| `PG_DB`, `PG_USER`, `PG_PASS` | Legacy (Postgres is CNPG `nextcloud-pgcluster-app`; optional to keep for reference) |

1. In vault **Collective**, create item **Nextcloud** with those fields (labels must match exactly).

2. Copy before cutover:

   ```sh
   kubectl -n nextcloud get secret nextcloud -o json | jq -r '.data | keys[]'
   kubectl -n nextcloud get secret nextcloud -o jsonpath='{.data.DOMAIN}' | base64 -d; echo
   ```

   Or decode from local `infrastructure/secrets/nextcloud-secret.yaml` (gitignored).

3. Verify:

   ```sh
   kubectl -n nextcloud get onepassworditem,secret nextcloud
   kubectl -n nextcloud get pods -l app.kubernetes.io/name=nextcloud
   kubectl -n nextcloud get pods -l app.kubernetes.io/name=nextcloud-exporter
   ```

4. Remove legacy: `kubectl -n nextcloud delete sealedsecret nextcloud`

### Traefik Forward Auth (OIDC)

`apps/base/forward-auth/onepassword-item.yaml` → `Secret/traefik-forward-auth` in `kube-system` (deployed with the `kube-system` app kustomization, not `infra-secrets`).

| Label | Used as |
|-------|---------|
| `client-id` | `PROVIDERS_OIDC_CLIENT_ID` |
| `client-secret` | `PROVIDERS_OIDC_CLIENT_SECRET` |
| `secret` | `SECRET` (cookie signing) |

1. In vault **Collective**, item **Forward Auth** with those three fields (labels must match exactly, including hyphens).
2. Copy values before cutover: `kubectl -n kube-system get secret traefik-forward-auth -o jsonpath='{.data}' | jq 'keys'`
3. Verify: `kubectl -n kube-system get onepassworditem,secret traefik-forward-auth` and `kubectl -n kube-system get pods -l app.kubernetes.io/name=traefik-forward-auth`
4. Remove legacy: `kubectl -n kube-system delete sealedsecret traefik-forward-auth`

### Home Assistant

Vault **Collective**, item **Home Assistant**:

| Label | Type | Used by |
|-------|------|---------|
| `secrets.yaml` | text (multiline) | `apps/base/homeassistant/onepassword-item.yaml` → `Secret/homeassistant`; copied to `/config/secrets.yaml` on pod start |
| `token` | concealed | `apps/monitoring/prometheus/onepassword-item.yaml` → `Secret/prometheus` in `monitoring`; Home Assistant Prometheus `/api/prometheus` scrapes |

**HA config secrets**

1. Paste entire `secrets.yaml` (plain YAML only — no markdown code fences).
2. Copy before cutover: `kubectl -n homeassistant get secret homeassistant -o jsonpath='{.data.secrets\.yaml}' | base64 -d`
3. Verify: `kubectl -n homeassistant get onepassworditem,secret homeassistant` and `kubectl -n homeassistant get pods`
4. Remove legacy: `kubectl -n homeassistant delete sealedsecret homeassistant`

**Prometheus scrape token**

1. In Home Assistant: Profile → Security → Long-Lived Access Tokens → create token (or reuse existing).
2. Add field `token` on the **Home Assistant** 1Password item with that value.
3. Copy before cutover: `kubectl -n monitoring get secret prometheus -o jsonpath='{.data.HASSTOKEN}' | base64 -d`
4. Verify:

   ```sh
   kubectl -n monitoring get onepassworditem prometheus
   kubectl -n monitoring get secret prometheus -o jsonpath='{.data.token}' | base64 -d | wc -c
   ```

5. Remove legacy: `kubectl -n monitoring delete sealedsecret prometheus`

### AdGuard (exporter API credentials)

1. In 1Password, create a **Login** or **Secure Note** in a vault Connect can access.
2. Add fields with these **exact labels** (not `username` / `password` unless you change the exporter):

   | Label | Type | Value |
   |-------|------|--------|
   | `USERNAMES` | text | AdGuard API user (e.g. `admin`) |
   | `PASSWORDS` | concealed | Plain AdGuard API password |

3. Grant the Connect server access to that vault.
4. Set `spec.itemPath` in `apps/base/adguard/onepassword-item.yaml`:

   ```yaml
   itemPath: vaults/<VaultName>/items/<ItemTitle>
   ```

   Use vault/item **title** or UUID from `op item get --format json`.

5. Copy values from the old sealed secret before cutover (if still running):

   ```sh
   kubectl -n adguard get secret adguard -o jsonpath='{.data.USERNAMES}' | base64 -d; echo
   kubectl -n adguard get secret adguard -o jsonpath='{.data.PASSWORDS}' | base64 -d; echo
   ```

6. Commit, push, reconcile. Confirm:

   ```sh
   kubectl -n adguard get onepassworditem,secret adguard
   kubectl -n adguard logs deploy/adguard-exporter --tail=20
   ```

The exporter reads `Secret/adguard` keys `USERNAMES` and `PASSWORDS`. AdGuard Home UI auth in `helm-release.yaml` is separate (bcrypt in values).

### Alertmanager (config in git, SMTP password in 1Password)

- **Git:** `apps/monitoring/alert-manager/alertmanager.yaml` — routes, receivers, SMTP host/user (no password). Kustomize `secretGenerator` creates `Secret/alertmanager`.
- **1Password:** item **Alertmanager SMTP**, field `smtp_auth_password` → `Secret/alertmanager-smtp`, mounted at `/etc/alertmanager/secrets/smtp_auth_password`.

1. In vault **Collective**, create **Alertmanager SMTP** with one field:

   | Label | Type | Value |
   |-------|------|--------|
   | `smtp_auth_password` | password | iCloud app-specific SMTP password (plain text, one line) |

2. Edit routes/receivers in `alertmanager.yaml` in git as needed.

3. After deploy, verify:

   ```sh
   kubectl -n monitoring get secret alertmanager alertmanager-smtp
   kubectl -n monitoring get onepassworditem alertmanager-smtp
   kubectl -n monitoring get pods -l app.kubernetes.io/name=alertmanager
   ```

4. Remove legacy sealed secret if still present: `kubectl -n monitoring delete sealedsecret alertmanager`

### CrowdSec (Console enroll key)

Used by `HelmRelease/crowdsec` LAPI (`ENROLL_KEY` → `Secret/crowdsec`).

1. In vault **Collective**, create item **CrowdSec** with one field:

   | Label | Type | Value |
   |-------|------|--------|
   | `ENROLL_KEY` | password | CrowdSec Console enrollment key |

   Create the key: [CrowdSec Console](https://app.crowdsec.net/) → enroll / instance key for your k3s deployment.

2. Set `spec.itemPath` in `crowdsec-onepassword-item.yaml` if your vault/item name differs.

3. Copy the current key before cutover (if still running):

   ```sh
   kubectl -n crowdsec get secret crowdsec -o jsonpath='{.data.ENROLL_KEY}' | base64 -d; echo
   ```

4. Commit, push, reconcile. Confirm:

   ```sh
   kubectl -n crowdsec get onepassworditem,secret crowdsec
   kubectl -n crowdsec get pods
   ```

5. Remove legacy sealed secret if still present: `kubectl -n crowdsec delete sealedsecret crowdsec`

### Arr Stack (exportarr + Recyclarr)

One 1Password item for all *arr exporter API keys and Recyclarr instance credentials.

`apps/media/arr-stack/onepassword-item.yaml` → `Secret/arr-stack` in `media` (deployed with the `media` Flux kustomization).

1. In vault **Collective**, create item **Arr Stack** with these fields (labels must match exactly):

   | Label | Type | Used by |
   |-------|------|---------|
   | `bazarr_api_key` | password | Bazarr exportarr |
   | `bazarr_anime_api_key` | password | Bazarr Anime exportarr |
   | `lidarr_api_key` | password | Lidarr exportarr |
   | `prowlarr_api_key` | password | Prowlarr exportarr |
   | `radarr_api_key` | password | Radarr exportarr |
   | `readarr_api_key` | password | Readarr exportarr |
   | `sonarr_tv_api_key` | password | Sonarr TV exportarr |
   | `sonarr_anime_api_key` | password | Sonarr Anime exportarr |
   | `plex_token` | password | Plex exporter |
   | `seerr_api_key` | password | Seerr exporter |
   | `tautulli_api_key` | password | Tautulli exporter |
   | `secrets.yml` | text (multiline) | Recyclarr → copied to `/config/secrets.yml` on pod start |

   `secrets.yml` example (plain YAML, no code fences):

   ```yaml
   radarr_url: http://radarr.media.svc:7878
   radarr_api_key: <api-key>
   sonarr_tv_url: http://sonarr-tv.media.svc:8989
   sonarr_tv_api_key: <api-key>
   sonarr_anime_url: http://sonarr-anime.media.svc:8989
   sonarr_anime_api_key: <api-key>
   ```

2. Copy before cutover from legacy secrets (if still running):

   ```sh
   kubectl -n media get secret exportarr -o json | jq -r '.data | keys[]'
   kubectl -n media get secret recyclarr -o jsonpath='{.data.secrets\.yml}' | base64 -d
   ```

   Or use gitignored `exportarr-secret.yaml` / `recyclarr-secret.yaml` under `infrastructure/secrets/`.

3. Verify:

   ```sh
   kubectl -n media get onepassworditem,secret arr-stack
   kubectl -n media get secret arr-stack -o json | jq -r '.data | keys[]'
   kubectl -n media rollout restart deploy/recyclarr
   for d in $(kubectl -n media get deploy -o name | grep exportarr); do kubectl -n media rollout restart "$d"; done
   ```

4. Remove legacy:

   ```sh
   kubectl -n media delete onepassworditem exportarr recyclarr --ignore-not-found
   kubectl -n media delete secret exportarr recyclarr --ignore-not-found
   kubectl -n media delete sealedsecret exportarr recyclarr --ignore-not-found
   ```

### Deluge (VPN + Web UI exporter password)

Used by `Deployment/deluge` (`VPN_USER`, `VPN_PASS`) and `Deployment/deluge-exporter` (`APP_PASS` as Deluge Web UI password).

1. In vault **Collective**, create item **Deluge** with three fields:

   | Label | Type | Value |
   |-------|------|--------|
   | `VPN_USER` | text | PIA WireGuard username |
   | `VPN_PASS` | password | PIA WireGuard password |
   | `APP_PASS` | password | Deluge Web UI password (for deluge-exporter metrics) |

2. Set `spec.itemPath` in `deluge-onepassword-item.yaml` if your vault/item name differs.

3. Copy values before cutover (if still running):

   ```sh
   kubectl -n media get secret deluge -o jsonpath='{.data.VPN_USER}' | base64 -d; echo
   kubectl -n media get secret deluge -o jsonpath='{.data.VPN_PASS}' | base64 -d; echo
   kubectl -n media get secret deluge -o jsonpath='{.data.APP_PASS}' | base64 -d; echo
   ```

4. Commit, push, reconcile. Confirm:

   ```sh
   kubectl -n media get onepassworditem,secret deluge
   kubectl -n media get pods -l app.kubernetes.io/name=deluge
   kubectl -n media get pods -l app.kubernetes.io/name=deluge-exporter
   ```

5. Remove legacy sealed secret if still present: `kubectl -n media delete sealedsecret deluge`

### Valheim (server password)

`apps/games/valheim/onepassword-item.yaml` → `Secret/valheim` in `valheim` (deployed with the `games` Flux kustomization). Used by `HelmRelease/valheim-server` as `SERVER_PASS` (`key: password`, min 5 characters).

1. In vault **Collective**, create item **Valheim** with one field:

   | Label | Type | Value |
   |-------|------|--------|
   | `password` | password | Valheim server password |

2. Copy before cutover:

   ```sh
   kubectl -n valheim get secret valheim -o jsonpath='{.data.password}' | base64 -d; echo
   ```

3. Verify:

   ```sh
   kubectl -n valheim get onepassworditem,secret valheim
   ```

4. Remove legacy: `kubectl -n valheim delete sealedsecret valheim`

### V Rising (server password)

`apps/games/v-rising/onepassword-item.yaml` → `Secret/v-rising` in `v-rising`. Used by `HelmRelease/v-rising-server` as `VR_PASSWORD` (`key: password`; leave empty in 1Password for no password).

1. In vault **Collective**, create item **V-Rising** with one field:

   | Label | Type | Value |
   |-------|------|--------|
   | `password` | password | V Rising server password (optional) |

2. Copy before cutover:

   ```sh
   kubectl -n v-rising get secret v-rising -o jsonpath='{.data.password}' | base64 -d; echo
   ```

3. Verify:

   ```sh
   kubectl -n v-rising get onepassworditem,secret v-rising
   ```

4. Remove legacy: `kubectl -n v-rising delete sealedsecret v-rising`

---

## Sealed Secrets (legacy)

1. Register Helm Repo

```sh
flux create source helm sealed-secrets \
  --interval=1h \
  --url=https://bitnami-labs.github.io/sealed-secrets
```

1. Create HelmRelease to install Sealed-Secrets Controller

```sh
flux create helmrelease sealed-secrets \
  --interval=1h \
  --release-name=sealed-secrets-controller \
  --target-namespace=flux-system \
  --source=HelmRepository/sealed-secrets \
  --chart=sealed-secrets \
  --chart-version=">=2.8.0 <3.0.0" \
  --crds=CreateReplace
```

1. Retrieve the public key:

```sh
kubeseal --fetch-cert \
  --controller-name=sealed-secrets-controller \
  --controller-namespace=flux-system \
  > pub-sealed-secrets.pem
```

1. Create a secret

```sh
kubectl -n default create secret generic basic-auth \
  --from-literal=user=admin \
  --from-literal=password=change-me \
  --dry-run=client \
  -o yaml > basic-auth.yaml
```

1. Seal the Secret

```sh
kubeseal --format=yaml --cert=pub-sealed-secrets.pem \
  < basic-auth.yaml > basic-auth-sealed.yaml
```

1. Apply the Sealed Secret

```sh
kubectl apply -f basic-auth-sealed.yaml
```
