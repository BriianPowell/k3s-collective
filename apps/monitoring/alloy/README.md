# Alloy Pod Log Aggregation

## App Logs

### Atuin

| Service  | Logs | Grafana Dashboard | Notes |
| -------- | ---- | ----------------- | ----- |
| App      | ✅   | ✅                |       |
| Postgres | ✅   | ✅                |       |

### Error-Pages

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Home Assistant

| Service  | Logs | Grafana Dashboard | Notes |
| -------- | ---- | ----------------- | ----- |
| App      | ✅   | ✅                |       |
| Postgres | ✅   | ✅                |       |

### Keycloak

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Postgres          | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Nextcloud

| Service  | Logs | Grafana Dashboard | Notes                                       |
| -------- | ---- | ----------------- | ------------------------------------------- |
| App      | ✅   | ✅                |                                             |
| Exporter | ❌   | ❌                | Not supporting dashboards for exporter logs |
| Cron     | ✅   | ✅                |                                             |
| Redis    | ✅   | ✅                |                                             |
| Postgres | ✅   | ✅                |                                             |

### Maybe

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ❌   | ❌                |       |

### Ntfy

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Pihole

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Wiki.JS

| Service  | Logs | Grafana Dashboard | Notes |
| -------- | ---- | ----------------- | ----- |
| App      | ✅   | ✅                |       |
| Postgres | ✅   | ✅                |       |

## Flux System

### Helm Controller

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Kustomize Controller

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Notification Controller

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Sealed Secrets Controller

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Source Controller

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

## Game Logs

### Minecraft

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| Server  | ✅   | ✅                |       |

### V-Rising

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| Server  | ✅   | ✅                |       |

### Valheim

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| Server  | ✅   | ✅                |       |

## Infrastructure Logs

### Kube-System

#### Core DNS

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

#### Local Path Provisioner

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Cert Manager

| Service     | Logs | Grafana Dashboard | Notes |
| ----------- | ---- | ----------------- | ----- |
| Controller  | ✅   | ✅                |       |
| CA-Injector | ✅   | ✅                |       |
| Webhook     | ✅   | ✅                |       |

### CloudNative PG

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| Manager | ✅   | ✅                |       |

### Crowdsec

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| LAPI    | ✅   | ✅                |       |
| Agent   | ✅   | ✅                |       |

### Nvidia Device Plugin

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Reflector

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Reloader

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Traefik

| Service      | Logs | Grafana Dashboard | Notes |
| ------------ | ---- | ----------------- | ----- |
| App          | ✅   | ✅                |       |
| Forward Auth | ✅   | ✅                |       |

## Monitoring Applications

### Alert Manager

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Alloy

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Grafana

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### kube-state-metrics

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Loki

| Service       | Logs | Grafana Dashboard | Notes |
| ------------- | ---- | ----------------- | ----- |
| App           | ✅   | ✅                |       |
| Canary        | ✅   | ✅                |       |
| Chunks Cache  | ✅   | ✅                |       |
| Gateway       | ✅   | ✅                |       |
| Results Cache | ✅   | ✅                |       |

### Node Exporter

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Prometheus

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

### Prometheus Operator

| Service | Logs | Grafana Dashboard | Notes |
| ------- | ---- | ----------------- | ----- |
| App     | ✅   | ✅                |       |

## Media Applications

| Service            | Logs | Grafana Dashboard | Notes                                                                         |
| ------------------ | ---- | ----------------- | ----------------------------------------------------------------------------- |
| Bazaar             | ✅   | ✅                |                                                                               |
| Bazaar Exporter    | ❌   | ❌                | Not supporting dashboards for exporter logs                                   |
| Deluge             | ✅   | ✅                |                                                                               |
| Deluge Exporter    | ❌   | ❌                | Not supporting dashboards for exporter logs                                   |
| Flaresolverr       | ✅   | ✅                |                                                                               |
| Kapowarr           | ❌   | ❌                | Currently in the testing phase, will revisit if I decide to keep this service |
| Kavita             | ❌   | ❌                | Currently in the testing phase, will revisit if I decide to keep this service |
| Lidarr             | ✅   | ✅                |                                                                               |
| Lidarr Exporter    | ❌   | ❌                | Not supporting dashboards for exporter logs                                   |
| Mylar3             | ❌   | ❌                | Currently in the testing phase, will revisit if I decide to keep this service |
| Overseerr          | ✅   | ✅                |                                                                               |
| Overseerr Exporter | ❌   | ❌                | Not supporting dashboards for exporter logs                                   |
| Plex               | ✅   | ✅                |                                                                               |
| Plex Exporter      | ❌   | ❌                | Not supporting dashboards for exporter logs                                   |
| Prowlarr           | ✅   | ✅                |                                                                               |
| Prowlarr Exporter  | ❌   | ❌                | Not supporting dashboards for exporter logs                                   |
| Radarr             | ✅   | ✅                |                                                                               |
| Radarr Exporter    | ❌   | ❌                | Not supporting dashboards for exporter logs                                   |
| Readarr            | ❌   | ❌                | Currently in the testing phase, will revisit if I decide to keep this service |
| Readarr Exporter   | ❌   | ❌                | Currently in the testing phase, will revisit if I decide to keep this service |
| Recyclarr          | ✅   | ✅                |                                                                               |
| Sonarr             | ✅   | ✅                |                                                                               |
| Sonarr Exporterr   | ❌   | ❌                | Not supporting dashboards for exporter logs                                   |
| Tautulli           | ✅   | ✅                |                                                                               |
| Tautulli Exporter  | ❌   | ❌                | Not supporting dashboards for exporter logs                                   |
