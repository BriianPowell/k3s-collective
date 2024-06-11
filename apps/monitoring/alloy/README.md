# Alloy Pod Log Aggregation

## App Logs

### Error-Pages

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ❌   |       |

### Home Assistant

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Postgres          | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Keycloak

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Postgres          | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Nextcloud

| Service           | Logs | Notes                                                      |
| ----------------- | ---- | ---------------------------------------------------------- |
| App               | ✅   |                                                            |
| Exporter          | ❌   | Can't figure out how to get the exporter logs from the pod |
| cron              | ✅   |                                                            |
| redis             | ✅   |                                                            |
| postgres          | ✅   |                                                            |
| Grafana Dashboard | ✅   |                                                            |

### Pihole

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Wiki.JS

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Postgres          | ✅   |       |
| Grafana Dashboard | ✅   |       |

## Flux System

### Helm Controller

### Kustomize Controller

### Notification Controller

### Sealed Secrets Controller

### Source Controller

## Game Logs

### Minecraft

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| Server            | ✅   |       |
| Grafana Dashboard | ✅   |       |

### V-Rising

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| Server            | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Valheim

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| Server            | ✅   |       |
| Grafana Dashboard | ✅   |       |

## Infrastructure Logs

### Cert-Manager

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| Controller        | ✅   |       |
| CA-Injector       | ✅   |       |
| Webhook           | ✅   |       |
| Grafana Dashboard | ✅   |       |

## Cloudnative-PG

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| Manager           | ❌   |       |
| Grafana Dashboard | ✅   |       |

### Crowdsec

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| LAPI              | ✅   |       |
| Agent             | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Nvidia-Device-Plugin

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ❌   |       |

### Reflector

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Reloader

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Traefik

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Forward Auth      | ✅   |       |
| Grafana Dashboard | ✅   |       |

## Monitoring Applications

### Alert Manager

### Loki

### Alloy

### Grafana

### Prometheus

### kube-state-metrics

### Node Exporter

### Prometheus Operator
