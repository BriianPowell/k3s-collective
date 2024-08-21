# Service Monitors

| App           | Service Monitor | Supported                        |
| ------------- | --------------- | -------------------------------- |
| Atuin         | ❓              |                                  |
| Error Pages   | ❌              | Not supported                    |
| HomeAssistant | ✅              | Created through API spec         |
| Keycloak      | ✅              | Created through API spec         |
| NextCloud     | ✅              | Created through API spec         |
| Ntfy          | ✅              | Supported through ServiceMonitor |
| Pihole        | ✅              | Created through API spec         |
| Wiki.JS       | ❌              | Not Supported                    |

| Game      | Service Monitor | Supported                 |
| --------- | --------------- | ------------------------- |
| Minecraft | ❌              | Created but not supported |
| Valheim   | ❌              | Created but not supported |
| V-Rising  | ❌              | Created but not supported |

| Flux                      | Service Monitor | Supported                                                                                  |
| ------------------------- | --------------- | ------------------------------------------------------------------------------------------ |
| Helm Controller           | ✅              | Supported through PodMonitor API spec                                                      |
| Kustomize Controller      | ✅              | Supported through PodMonitor API spec                                                      |
| Notification Controller   | ✅              | Supported through PodMonitor API spec                                                      |
| Sealed Secrets Controller | ❌              | Connection refused error when setting up PodMonitor or ServiceMonitor, I think it's bugged |
| Source Controller         | ✅              | Supported through PodMonitor API spec                                                      |

| Infra                | Service Monitor | Supported                               |
| -------------------- | --------------- | --------------------------------------- |
| Cert Manager         | ✅              | Supported by helm chart                 |
| CloudNativePG        | ✅              | Supported through PodMonitor API spec   |
| CrowdSec             | ✅              | Created though API spec                 |
| Kube APIServer       | ✅              | Supported by helm chart                 |
| Kube CoreDNS         | ✅              | Supported by helm chart                 |
| Kube Controller      | ✅              | Supported by helm chart                 |
| Kube ETCD            | ✅              | Supported by helm chart                 |
| Kube Proxy           | ✅              | Supported by helm chart                 |
| Kube Scheduler       | ✅              | Supported by helm chart                 |
| Kubelet              | ✅              | Supported by helm chart                 |
| Nvidia Device Plugin | ❓              | Unsure if supported                     |
| Reflector            | ❌              | Not supported                           |
| Reloader             | ✅              | PodMonitor supported through helm chart |
| Traefik              | ✅              | Created through API Spec                |

| Monitoring            | Service Monitor | Supported                 |
| --------------------- | --------------- | ------------------------- |
| Alert Manager         | ✅              | Supported from helm chart |
| Alloy                 | ✅              | Supported from helm Chart |
| Grafana               | ✅              | Supported from helm Chart |
| Kube State Metrics    | ✅              | Supported from helm chart |
| Loki                  | ❓              | Unsure if supported       |
| Node Exporter         | ✅              | Supported from helm chart |
| Prometheus + Operator | ✅              | Supported from helm chart |

| PG Clusters            | Pod Monitor | Supported                  |
| ---------------------- | ----------- | -------------------------- |
| HomeAssistant Postgres | ✅          | Supported through CPNG API |
| Keycloak Postgres      | ✅          | Supported through CNPG API |
| Nextcloud Postgres     | ✅          | Supported through CNPG API |
| Wiki.Js Postgres       | ✅          | Supported through CNPG API |

| Media        | Monitor | Supported |
| ------------ | ------- | --------- |
| Bazaarr      | ❓      |           |
| Deluge       | ❓      |           |
| Flaresolverr | ❓      |           |
| Lidarr       | ❓      |           |
| Overseerr    | ❓      |           |
| Plex         | ❓      |           |
| Prowlarr     | ❓      |           |
| Radarr       | ❓      |           |
| Recyclarr    | ❓      |           |
| Sonarr       | ❓      |           |
| Tautulli     | ❓      |           |
