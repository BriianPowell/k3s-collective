# Secrets Management

## 1Password Operator

Bootstrap (once, not in git):

```sh
kubectl -n onepassword create secret generic op-credentials \
  --from-file=1password-credentials.json=/path/to/1password-credentials.json

kubectl -n onepassword create secret generic onepassword-token \
  --from-literal=token='YOUR_CONNECT_TOKEN'
```

App secrets use `OnePasswordItem` CRs (see `apps/base/*/onepassword-item.yaml`). The operator creates a `Secret` with the same name as the CR. **Field labels in 1Password must match the Kubernetes secret keys** your apps reference (`secretKeyRef.key`).

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

### Cloudflare API token (cert-manager DNS-01)

Used by `ClusterIssuer/lets-encrypt` (`apiTokenSecretRef` → `Secret/cloudflare-api-token`, key `api-token`).

1. In vault **Collective**, create item **Cloudflare** (or match `itemPath` below) with one field:

   | Label | Type | Value |
   |-------|------|--------|
   | `api-token` | password | Cloudflare API token (DNS Edit for your zones) |

   Create the token: [Cloudflare API Tokens](https://dash.cloudflare.com/profile/api-tokens) → **Edit zone DNS** for zones you issue certs on.

2. Set `spec.itemPath` in `cloudflare-api-token-onepassword-item.yaml` if your vault/item name differs.

3. Copy the current token from the old secret before cutover (if still running):

   ```sh
   kubectl -n cert-manager get secret cloudflare-api-token -o jsonpath='{.data.api-token}' | base64 -d; echo
   ```

4. Commit, push, reconcile. Confirm:

   ```sh
   kubectl -n cert-manager get onepassworditem,secret cloudflare-api-token
   kubectl describe clusterissuer lets-encrypt
   ```

5. Remove legacy sealed secret if still present: `kubectl -n cert-manager delete sealedsecret cloudflare-api-token`

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
