# Cluster ops runbook

Quick commands for day-two operations. Apply Git changes with Flux unless noted.

## Flux reconcile

Reconcile a kustomization and its Git source:

```bash
flux reconcile kustomization <name> -n flux-system --with-source
```

Common targets:

| Kustomization | Path |
|---------------|------|
| `infra-policies` | `./infrastructure/policies` |
| `infra-controllers` | `./infrastructure/controllers` |
| `infra-configs` | `./infrastructure/configs` |
| `games` | `./apps/games` |

Check status:

```bash
flux get kustomizations -A
flux get helmreleases -A
```

## CrowdSec unban

Traefik bouncer decisions live in the LAPI. List and remove by IP:

```bash
# List active bans
kubectl -n crowdsec exec deploy/crowdsec-lapi -- cscli decisions list

# Remove one IP
kubectl -n crowdsec exec deploy/crowdsec-lapi -- cscli decisions delete --ip <IP>

# Remove all decisions for an IP (alias)
kubectl -n crowdsec exec deploy/crowdsec-lapi -- cscli decisions delete --ip <IP> --all
```

If the deployment name differs, find the LAPI pod:

```bash
kubectl -n crowdsec get pods -l app.kubernetes.io/name=crowdsec-lapi
kubectl -n crowdsec exec <lapi-pod> -- cscli decisions list
```

After unban, retry the client; no Traefik restart is required.

## Resume idle games

Games are idle at two levels: Flux `games` kustomization is suspended, and each `HelmRelease` is suspended with `replicaCount` / `replicas: 0`.

### Start one game (example: Minecraft)

1. In git, for that game’s `helm-release.yaml`:
   - Set `spec.suspend: false` (or remove it).
   - Set `replicaCount` / `controller.replicas` to `1`.
2. Commit and push, or patch live for a test:

```bash
flux resume kustomization games -n flux-system
flux reconcile kustomization games -n flux-system --with-source
```

### Park games again

1. Set `replicaCount` / `replicas` back to `0` and `spec.suspend: true` on each game `HelmRelease`.
2. Suspend the kustomization:

```bash
flux suspend kustomization games -n flux-system
```

| Game | Namespace | Replicas field |
|------|-----------|----------------|
| Minecraft | `minecraft` | `values.replicaCount` |
| Valheim | `valheim` | `values.controller.replicas` |
| V-Rising | `v-rising` | `values.controller.replicas` |

## Periodic ops (not in git)

On the k3s node(s):

```bash
k3s-remove-unused-rs   # if installed; prune old ReplicaSets
crictl rmi --prune     # unused images
```

Review orphan PVCs before deleting (`kubectl get pvc -A`).
