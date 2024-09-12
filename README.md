# k3s-collective

Collection of all of my kubernetes resources created for my k3s cluster, hosted on a 2 nodes in my home office.

| Name    | CPU      | Memory                 | **GPU**    |
| ------- | -------- | ---------------------- | ---------- |
| Sheol   | i7-6700k | 32 GiB DDR4 @ 3000 MHz | RTX-3080   |
| Abaddon | i5-6600T | 16 GiB DDR4 @ 2400 MHz | Integrated |

## Infrastructure

### Base

- [x] [Atuin](https://github.com/atuinsh/atuin)
- [x] [Traefik](https://artifacthub.io/packages/helm/traefik/traefik) + [Traefik Forward Auth](https://github.com/thomseddon/traefik-forward-auth)
- [x] [Cert Manager](https://github.com/cert-manager/cert-manager)
- [x] [Metrics Server](https://github.com/kubernetes-sigs/metrics-server)
- [x] [Reflector](https://github.com/emberstack/kubernetes-reflector)
- [x] [Reloader](https://github.com/stakater/Reloader)
- [x] [Keycloak](https://github.com/keycloak/keycloak)
- [x] [HomeAssistant](https://github.com/home-assistant)
- [x] [Nextcloud](https://github.com/nextcloud/server) + [Nextcloud Exporter](https://github.com/xperimental/nextcloud-exporter)
- [x] [Ntfy](https://github.com/binwiederhier/ntfy)
- [x] [Wiki.js](https://github.com/requarks/wiki)
- [x] [Pi-hole](https://github.com/MoJo2600/pihole-kubernetes)
- [x] [Cloudnative-PG](https://github.com/cloudnative-pg/cloudnative-pg)
- [x] [Error Pages](https://github.com/tarampampam/error-pages)

### Monitoring & Logging

- [x] [Prometheus](https://github.com/prometheus/prometheus)
- [x] [Grafana](https://github.com/grafana/grafana)
- [x] [Alert Manager](https://github.com/prometheus/alertmanager)
- [x] [Kube State Metrics](https://github.com/kubernetes/kube-state-metrics)
- [x] [Node Exporter](https://github.com/prometheus/node_exporter)
- [x] [Smartctl Exporter](https://github.com/prometheus-community/smartctl_exporter)
- [x] [Loki](https://github.com/grafana/loki)
- [x] [Alloy](https://github.com/grafana/alloy)

#### More detailed loggin configurations are outlined here:

- [Prometheus Service Monitors](./apps/monitoring/prometheus/README.md)
- [Alloy Log Aggregations](./apps/monitoring/alloy/README.md)

### Security

- [x] [CrowdSec](https://github.com/crowdsecurity/crowdsec)

### Games

- [x] [Valheim](https://artifacthub.io/packages/helm/geek-cookbook/valheim)
- [x] [Minecraft](https://artifacthub.io/packages/helm/minecraft-server-charts/minecraft)
- [x] [V-Rising](https://truecharts.org/charts/stable/v-rising/)

### Media

_In Installation Order_

- [x] [nvidia-device-plugin](https://github.com/NVIDIA/k8s-device-plugin)
- [x] [Plex](https://github.com/plexinc/pms-docker/blob/master/charts/plex-media-server/README.md) + [plex-media-server-exporter](https://github.com/axsuul/plex-media-server-exporter)
- [x] [Deluge](https://github.com/binhex/arch-delugevpn) + [deluge_exporter](https://github.com/ngosang/deluge-exporter)
- [x] [Radarr](https://github.com/Radarr/Radarr) + [Exportarr](https://github.com/onedr0p/exportarr)
- [x] [Sonarr](https://github.com/Sonarr/Sonarr) + [Exportarr](https://github.com/onedr0p/exportarr)
- [x] [Lidarr](https://github.com/Lidarr/Lidarr)+ [Exportarr](https://github.com/onedr0p/exportarr)
- [x] [Bazarr](https://github.com/morpheus65535/bazarr) + [Exportarr](https://github.com/onedr0p/exportarr)
- [x] [Prowlarr](https://github.com/Prowlarr/Prowlarr) + [Exportarr](https://github.com/onedr0p/exportarr)
- [x] [Recyclarr](https://github.com/recyclarr/recyclarr)
- [x] [Overseerr](https://github.com/sct/overseerr) + [overseer-exporter](https://github.com/WillFantom/overseerr-exporter)
- [x] [Tautulli](https://github.com/Tautulli/Tautulli) + [tautulli-exporter](https://github.com/nwalke/tautulli-exporter)

### TBD

- [ ] [Readarr](https://github.com/Readarr/Readarr)
- [ ] [Kavita](https://github.com/Kareadita/Kavita)
- [ ] [Jellyfin](https://github.com/jellyfin/jellyfin)

### [Secrets Management](./infrastructure/secrets/README.md)

## FluxCD Installation

**Will need to create a GitHub Personal Access Token**

```sh
flux bootstrap github \
  --components-extra=image-reflector-controller,image-automation-controller \
  --owner=BriianPowell \
  --repository=k3s-collective \
  --branch=main \
  --path=clusters/k3s \
  --read-write-key \
  --personal=true \
  --private=false \
  --reconcile # use if repository already exists
```

## References

All references I've used to create this project are listed as comments within each of their respective projects. In many cases I had to utilize several sources to create a working deployment file for my needs. If anyone has any questons or would like to reach out about the way I've done things, I'd be more than happy to talk about this project :grin:
