# Infrastructure configs

## Cloudflare API token (cert-manager DNS-01)

`onepassword-item.yaml` syncs 1Password → `Secret/cloudflare-api-token` in `cert-manager`. Used by `ClusterIssuer/lets-encrypt` (`apiTokenSecretRef`, key `api-token`).

1. In vault **Collective**, item **Cloudflare** with field `api-token` (password). [Create token](https://dash.cloudflare.com/profile/api-tokens) → **Edit zone DNS** for your zones.

2. Adjust `spec.itemPath` in `cloudflare-api-token-onepassword-item.yaml` if needed.

3. Verify after Flux reconciles `infra-configs`:

   ```sh
   kubectl -n cert-manager get onepassworditem,secret cloudflare-api-token
   kubectl describe clusterissuer lets-encrypt
   kubectl -n cert-manager get certificate wildcard-powell-place
   ```

Deployed with `infra-configs` (after `infra-controllers`, so the 1Password operator is already running).
