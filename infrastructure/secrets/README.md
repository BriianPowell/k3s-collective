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
