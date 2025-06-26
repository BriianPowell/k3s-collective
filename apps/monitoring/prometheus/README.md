# Service Monitors

| App           | Service Monitor | Supported                |
| ------------- | --------------- | ------------------------ |
| Adguard | ✅ | Supported through [Adguard Exporter](https://github.com/henrywhitaker3/adguard-exporter) |
| Atuin         | ❌              | Not currently supported  |
| Error Pages   | ❌              | Not currently supported  |
| HomeAssistant | ✅              | Created through API spec |
| Keycloak      | ✅              | Created through API spec |
| NextCloud     | ✅              | Created through API spec |
| Ntfy          | ✅              | Created through API spec |
| Pihole        | 🗑️           | Migrated to Adguard Home |
| Wiki.JS       | ❌              | Not currently supported  |

| Game      | Service Monitor | Supported               |
| --------- | --------------- | ----------------------- |
| Minecraft | ❌              | Not currently supported |
| Valheim   | ❌              | Not currently supported |
| V-Rising  | ❌              | Not currently supported |

| Flux                      | Service Monitor | Supported                                                                                  |
| ------------------------- | --------------- | ------------------------------------------------------------------------------------------ |
| Helm Controller           | ✅              | Supported through PodMonitor API spec                                                      |
| Kustomize Controller      | ✅              | Supported through PodMonitor API spec                                                      |
| Notification Controller   | ✅              | Supported through PodMonitor API spec                                                      |
| Sealed Secrets Controller | ❌              | Connection refused error when setting up PodMonitor or ServiceMonitor, I think it's bugged |
| Source Controller         | ✅              | Supported through PodMonitor API spec                                                      |

| Infra                | Service Monitor | Supported                               |
| -------------------- | --------------- | --------------------------------------- |
| Cert Manager         | ✅              | Supported by Helm Chart                 |
| CloudNativePG        | ✅              | Supported through PodMonitor API spec   |
| CrowdSec             | ✅              | Created though API spec                 |
| Kube APIServer       | ✅              | Supported by Helm Chart                 |
| Kube CoreDNS         | ✅              | Supported by Helm Chart                 |
| Kube Controller      | ✅              | Supported by Helm Chart                 |
| Kube ETCD            | ✅              | Supported by Helm Chart                 |
| Kube Proxy           | ✅              | Supported by Helm Chart                 |
| Kube Scheduler       | ✅              | Supported by Helm Chart                 |
| Kubelet              | ✅              | Supported by Helm Chart                 |
| Nvidia Device Plugin | ❌              | Not currently supported                 |
| Reflector            | ❌              | Not currently supported                 |
| Reloader             | ✅              | PodMonitor supported through Helm Chart |
| Traefik              | ✅              | Created through API Spec                |

| Monitoring            | Service Monitor | Supported                                                                                                                            |
| --------------------- | --------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Alert Manager         | ✅              | Supported from Helm Chart                                                                                                            |
| Alloy                 | ✅              | Supported from Helm Chart                                                                                                            |
| Grafana               | ✅              | Supported from Helm Chart                                                                                                            |
| Kube State Metrics    | ✅              | Supported from Helm Chart                                                                                                            |
| Loki                  | ❓              | Supported through [meta-monitoring-chart](https://github.com/grafana/meta-monitoring-chart), but need to spend the time to implement |
| Node Exporter         | ✅              | Supported from Helm Chart                                                                                                            |
| Prometheus + Operator | ✅              | Supported from Helm Chart                                                                                                            |

| PG Clusters            | Pod Monitor | Supported                  |
| ---------------------- | ----------- | -------------------------- |
| HomeAssistant Postgres | ✅          | Supported through CPNG API |
| Keycloak Postgres      | ✅          | Supported through CNPG API |
| Nextcloud Postgres     | ✅          | Supported through CNPG API |
| Wiki.Js Postgres       | ✅          | Supported through CNPG API |

| Media        | Service Monitor | Supported                                                                                            |
| ------------ | --------------- | ---------------------------------------------------------------------------------------------------- |
| Bazaarr      | ✅              | Supported through [exportarr](https://github.com/onedr0p/exportarr)                                  |
| Deluge       | ✅              | Supported through [deluge_exporter](https://github.com/tobbez/deluge_exporter)                       |
| Flaresolverr | ✅              | Supported through API Spec                                                                           |
| Kapowarr     | ❌              | Not currently supported                                                                              |
| Kavita       | ❌              | Not currently supported                                                                              |
| Lidarr       | ✅              | Supported through [exportarr](https://github.com/onedr0p/exportarr)                                  |
| Mylar3       | ❌              | Not going to maintain this service, old and kinda clunky                                             |
| Overseerr    | ✅              | Supported through [overseerr-exporter](https://github.com/WillFantom/overseerr-exporter)             |
| Plex         | ✅              | Supported through [plex-media-server-exporter](https://github.com/axsuul/plex-media-server-exporter) |
| Prowlarr     | ✅              | Supported through [exportarr](https://github.com/onedr0p/exportarr)                                  |
| Radarr       | ✅              | Supported through [exportarr](https://github.com/onedr0p/exportarr)                                  |
| Readarr      | ✅              | Supported through [exportarr](https://github.com/onedr0p/exportarr)                                  |
| Recyclarr    | ❌              | Not currently supported, but also not really needed                                                  |
| Sonarr       | ✅              | Supported through [exportarr](https://github.com/onedr0p/exportarr)                                  |
| Tautulli     | ✅              | Supported through [tautulli-exporter](https://github.com/nwalke/tautulli-exporter)                   |
