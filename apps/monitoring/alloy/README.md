# Alloy Pod Log Aggregation

## App Logs

### Error-Pages

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

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

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Kustomize Controller

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Notification Controller

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Sealed Secrets Controller

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Source Controller

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

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

### Core DNS

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Grafana Dashboard | ❌   |       |

### Cert Manager

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| Controller        | ✅   |       |
| CA-Injector       | ✅   |       |
| Webhook           | ✅   |       |
| Grafana Dashboard | ✅   |       |

### CloudnativePG

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| Manager           | ❌   |       |
| Grafana Dashboard | ❌   |       |

### Crowdsec

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| LAPI              | ✅   |       |
| Agent             | ✅   |       |
| Grafana Dashboard | ✅   |       |

### Local Path Provisioner

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Grafana Dashboard | ❌   |       |

### Nvidia Device Plugin

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ✅   |       |
| Grafana Dashboard | ✅   |       |

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

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Grafana Dashboard | ❌   |       |

### Alloy

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Grafana Dashboard | ❌   |       |

### Grafana

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Grafana Dashboard | ❌   |       |

### kube-state-metrics

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Grafana Dashboard | ❌   |       |

### Node Exporter

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Grafana Dashboard | ❌   |       |

### Loki

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Canary            | ❌   |       |
| Chunks Cache      | ❌   |       |
| Gateway           | ❌   |       |
| Results Cache     | ❌   |       |
| Grafana Dashboard | ❌   |       |

### Prometheus

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Grafana Dashboard | ❌   |       |

### Prometheus Operator

| Service           | Logs | Notes |
| ----------------- | ---- | ----- |
| App               | ❌   |       |
| Grafana Dashboard | ❌   |       |
