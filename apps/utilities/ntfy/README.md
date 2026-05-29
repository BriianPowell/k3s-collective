# ntfy (cluster notifications)

## *arr apps (Sonarr, Radarr, Prowlarr, Lidarr, Bazarr, …)

Use the **native Ntfy** connection in each app (not Generic Webhook).

| Field | Value |
|--------|--------|
| **Server URL** | `http://ntfy.kube-system.svc` (no trailing slash; topic is a separate field) |
| **Topic** | Per app, lowercase: `sonarr`, `radarr`, `prowlarr`, … |
| **Access Token** | From the ntfy UI (`https://ntfy.powell.place`) — token needs **write** on that topic |

Prefer the in-cluster URL so pods in `media` do not traverse Traefik or CrowdSec.

### Network policy

`kube-system` `intra-namespace` policy only allowed traffic from `kube-system`. Pods in `media` could not reach ntfy until **`allow-ntfy-http`** (ingress TCP 80 to ntfy pods).

Apply or reconcile:

```bash
flux reconcile kustomization infra-policies -n flux-system --with-source
kubectl -n kube-system get networkpolicy allow-ntfy-http
```

### Verify from media (optional)

```bash
kubectl -n media exec deploy/sonarr -- curl -sS -o /dev/null -w "%{http_code}\n" \
  -H "Authorization: Bearer <token-from-ui>" \
  -d "test" "http://ntfy.kube-system.svc/<topic>"
```

Expect **200**.
