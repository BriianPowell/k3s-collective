# Cluster network policies

Ingress-focused policies aligned with the [K3s CIS hardening guide](https://docs.k3s.io/security/hardening-guide#networkpolicies).

## Coverage

| Policy | Namespaces |
|--------|------------|
| `standard-ingress` | `media`, `monitoring`, `crowdsec`, `cert-manager`, `reflector`, `reloader` |
| `media-container-limits` | `media` — per-container/pod/PVC min/max and defaults |

**PDBs** (voluntary disruption): Traefik DS `minAvailable: 1` (Helm); Prometheus + Grafana `minAvailable: 1` (Helm); CrowdSec LAPI `pdb-crowdsec-lapi.yaml`. Single-replica workloads block `kubectl drain` until scaled or PDB removed.
| `standard-ingress` + CNPG | `homeassistant`, `nextcloud`, `keycloak`, `wiki`, `atuin` |
| `allow-all-ingress` | `adguard`, `minecraft`, `valheim`, `v-rising` (LB / game / DNS ports) |
| `kube-system` bundle | `kube-system` (intra-ns, DNS :53, CoreDNS metrics :9153, ntfy :80, Traefik, metrics-server) |

**No policies:** `flux-system`, `cnpg-system`, `onepassword` — operators and webhooks need broader reach.

## Apply

Flux kustomization `infra-policies` (after `infra-namespaces`).

```bash
flux reconcile kustomization infra-policies -n flux-system --with-source
```

## Host hardening (sheol)

See `nix-config/hosts/sheol/kubernetes.nix`: `secrets-encryption`, `protect-kernel-defaults`, API audit logs. Requires a planned `k3s` restart on the server node.

## Housekeeping (excluding backups)

| # | Item | Status |
|---|------|--------|
| 1 | Revision caps (`revisionHistoryLimit` / `maxHistory: 3`) | done |
| 2 | CrowdSec bouncer `updateMaxFailure: -1` | done |
| 3 | Idle games: `games` Kustomization + HelmRelease `suspend` | done |
| 4 | CronJob: prune succeeded Jobs cluster-wide | done |
| 5 | `LimitRange` in `media` (and optionally `monitoring`) | done |
| 6 | PDBs for Traefik, Prometheus, Grafana, CrowdSec LAPI | done |
| 7 | CIS: `automountServiceAccountToken: false` on default SAs | done |
| 8 | sheol PKI `chmod 600` on k3s server TLS material | pending |
| 9 | Prometheus alerts (cert expiry, Flux Not Ready, disk, PVC) | pending |
| 10 | Loki retention vs disk budget | pending |
| 11 | Egress network policies per namespace | pending |
| 12 | Ops runbook (CrowdSec unban, Flux reconcile, game resume) | pending |

Periodic ops (no git): `k3s-remove-unused-rs`, `crictl rmi --prune`, orphan PVC review.

## Later (optional)

- Global PSA via `/var/lib/rancher/k3s/server/psa.yaml` with `kube-system` exempt (conflicts with per-namespace baseline labels until privileged workloads are removed).
- Egress policies per namespace (also tracked in housekeeping #11).
- CIS 5.1.5: extend default SA hardening to `kube-system` / `flux-system` / operators after testing (see second document in each `infrastructure/namespaces/*.yaml` except operator/core namespaces).
- PKI file permissions on sheol: `chmod 600` on `/var/lib/rancher/k3s/server/tls/*.crt` (housekeeping #8).
