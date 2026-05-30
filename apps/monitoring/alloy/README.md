# Alloy → Loki

Alloy tails pod logs and pushes to Loki (`http://loki.monitoring:3100`). Query logs in **Grafana Explore** or the **log dashboards** in [grafana-dashboards](https://github.com/BriianPowell/grafana-dashboards) (LogQL uses `namespace` / `pod`, not Alloy `job` names).

Config: `config.yaml` (ConfigMap `alloy`).

## What we collect

### Namespaces (`loki.source.kubernetes.apps`)

| Namespace | Workloads |
|-----------|-----------|
| `adguard` | AdGuard Home |
| `atuin` | App + Postgres (CNPG) |
| `cert-manager` | controller, webhook, cainjector |
| `cnpg-system` | CloudNative-PG operator |
| `crowdsec` | agent + LAPI |
| `flux-system` | helm / kustomize / notification / source controllers |
| `homeassistant` | app + Postgres |
| `keycloak` | app + Postgres |
| `media` | *arr, Deluge, Plex, Seerr, etc. (not exporter sidecars) |
| `nextcloud` | app, cron, redis, Postgres |
| `wiki` | app + Postgres |

**Relabel drops (all namespaces):** `Succeeded` / `Failed` pods; containers matching `*exporter*`, `*metrics*`, `*memcached*`.

### `kube-system` (`loki.source.kubernetes.kube_system`)

| Target | Selector |
|--------|----------|
| Traefik | `app.kubernetes.io/name=traefik` |
| ntfy | `app.kubernetes.io/name=ntfy` |
| CoreDNS | `k8s-app=kube-dns` |

## Not collected (debug-only trim)

- `monitoring` (Alloy, Loki, Prometheus, Grafana, … — avoids noise and loops)
- `minecraft`, `valheim`, `v-rising` (idle / games suspended)
- `reflector`, `reloader`, `kube-system` bulk (local-path-provisioner, metrics-server, …)
- NVIDIA device plugin

Re-enable by adding the namespace to `discovery.kubernetes.apps.names` in `config.yaml`, or add a dedicated `discovery.kubernetes` block like Traefik.

## Grafana dashboards

Log dashboards live in **grafana-dashboards** (`dashboards/logs/…`). Panels use LogQL such as:

```logql
{namespace="media", pod=~"deluge.*"}
```

After changing Alloy namespaces, update the matching dashboard JSON (or Explore with the same selectors). Dashboards for workloads we do not ship to Loki are **not** provisioned in Grafana Helm (`game-logs`, `monitoring-logs`, etc.).

## Helm

`helm-release.yaml`: ConfigMap `alloy` / key `config.content`, `nodeSelector: abaddon`.

## Adding a workload

1. Ensure the pod’s namespace is in the `names` list in `config.yaml`, **or** add a `kube-system` selector block.
2. In Grafana, use `{namespace="…", pod=~"…"}` (copy an existing dashboard panel).
3. Optional: add a dashboard JSON under `grafana-dashboards/dashboards/logs/` and wire it in `apps/monitoring/grafana/helm-release.yaml`.
