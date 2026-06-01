# Cluster network policies

Ingress-focused policies aligned with the [K3s CIS hardening guide](https://docs.k3s.io/security/hardening-guide#networkpolicies).

## Coverage

| Policy | Namespaces |
|--------|------------|
| `standard-ingress` | `media`, `monitoring`, `crowdsec`, `cert-manager`, `reflector`, `reloader` |
| `standard-egress` | `cert-manager`, `reflector`, `reloader` — LAN + cluster CIDRs + kube-system + monitoring + DNS + WAN :80/:443 |
| `allow-all-egress` | `media`, `monitoring`, `crowdsec` — arbitrary ports (torrent/VPN, scrapes, CrowdSec hub) |
| `media-container-limits` | `media` — per-container/pod/PVC min/max and defaults |
| `standard-ingress` + CNPG | `homeassistant`, `nextcloud`, `keycloak`, `wiki`, `atuin` |
| `standard-egress` + CNPG | same app namespaces — adds `cnpg-system` to egress |
| `allow-all-ingress` | `adguard`, `minecraft`, `valheim`, `v-rising` (LB / game / DNS ports) |
| `allow-all-egress` | same open namespaces |
| `kube-system` bundle | `kube-system` (intra-ns, DNS :53, CoreDNS metrics :9153, ntfy :80, Traefik, metrics-server) |

**No policies:** `flux-system`, `cnpg-system`, `onepassword` — operators and webhooks need broader reach.

## Apply

Flux kustomization `infra-policies` (after `infra-namespaces`).

```bash
flux reconcile kustomization infra-policies -n flux-system --with-source
```

## Host hardening (sheol)

See `nix-config/hosts/sheol/kubernetes.nix`: `secrets-encryption`, `protect-kernel-defaults`, API audit logs, PKI `chmod` (activation + `k3s-pki-permissions` oneshot after `k3s`). Apply on sheol: `sudo nixos-rebuild switch`, then `systemctl start k3s-pki-permissions` (or reboot).

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

- Global PSA via `/var/lib/rancher/k3s/server/psa.yaml` with `kube-system` exempt (conflicts with per-namespace baseline labels until privileged workloads are removed).
- Tighten `allow-all-egress` namespaces (e.g. media torrent ports only) once traffic patterns are known.
- CIS 5.1.5: extend default SA hardening to `kube-system` / `flux-system` / operators after testing (see second document in each `infrastructure/namespaces/*.yaml` except operator/core namespaces).
