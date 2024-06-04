# k3s-collective

Collection of all of my kubernetes resources created for my k3s cluster, hosted on a 2 nodes in my home office.

| Name    | CPU      | GPU        |
| ------- | -------- | ---------- |
| Sheol   | i7-6700k | RTX-3080   |
| Abaddon | i5-6600T | Integrated |

## FluxCD Installation

**Will need to create a GitHub Personal Access Token**

```sh
flux bootstrap github \
  --owner=BriianPowell \
  --repository=k3s-collective \
  --branch=master \
  --path=clusters/k3s \
  --personal \
  --private
```

## Infrastructure

### Base

- [x] [Traefik](https://artifacthub.io/packages/helm/traefik/traefik)
- [x] [Traefik Forward Auth](https://github.com/thomseddon/traefik-forward-auth)
- [x] [Cert Manager](https://github.com/cert-manager/cert-manager)
- [x] [Metrics Server](https://github.com/kubernetes-sigs/metrics-server)
- [x] [Reflector](https://github.com/emberstack/kubernetes-reflector)
- [x] [Reloader](https://github.com/stakater/Reloader)
- [x] [Keycloak](https://github.com/keycloak/keycloak)
- [x] [HomeAssistant](https://www.home-assistant.io/)
- [x] [Nextcloud](https://github.com/nextcloud/server) + [Nextcloud Exporter](https://github.com/xperimental/nextcloud-exporter)
- [x] [Wiki.js](https://js.wiki/)
- [x] [Pi-hole](https://pi-hole.net/)

### Monitoring & Logging

- [x] [Prometheus](https://prometheus.io/)
- [x] [Grafana](https://github.com/grafana/grafana)
- [x] [alertmanager](https://github.com/prometheus/alertmanager)
- [x] [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
- [x] [node_exporter](https://github.com/prometheus/node_exporter)
- [x] [Loki](https://grafana.com/docs/loki/latest/)

### Security

- [x] [CrowdSec](https://github.com/crowdsecurity/crowdsec)

### Games

- [x] [Valheim](https://artifacthub.io/packages/helm/geek-cookbook/valheim)
- [x] [Minecraft](https://artifacthub.io/packages/helm/minecraft-server-charts/minecraft)
- [x] [V-Rising](https://truecharts.org/charts/stable/v-rising/)

### Media

- [x] [nvidia-device-plugin](https://github.com/NVIDIA/k8s-device-plugin)
- [ ] Jellyfin OR Plex (Haven't Decided Yet!)
- [ ] Sonarr
- [ ] Lidarr
- [ ] Radarr
- [ ] Readarr
- [ ] Deluge OR Transmission

### TBD

- [ ] [Scrutiny](https://github.com/AnalogJ/scrutiny) - **find alternative** as this is not compatible with k8s
- [ ] [Gotify](https://github.com/gotify/server) - **find alternative** as is not possible with iOS
- [ ] [Uptime Kuma](https://github.com/louislam/uptime-kuma) - On the fence, kinda like the idea tho

## Secrets Management

1. Register Helm Repo

```sh
flux create source helm sealed-secrets \
  --interval=1h \
  --url=https://bitnami-labs.github.io/sealed-secrets
```

2. Create HelmRelease to install Sealed-Secrets Controller

```sh
flux create helmrelease sealed-secrets \
  --interval=1h \
  --release-name=sealed-secrets-controller \
  --target-namespace=flux-system \
  --source=HelmRepository/sealed-secrets \
  --chart=sealed-secrets \
  --chart-version=">=2.8.0 <3.0.0" \
  --crds=CreateReplace
```

3. Retrieve the public key:

```sh
kubeseal --fetch-cert \
  --controller-name=sealed-secrets-controller \
  --controller-namespace=flux-system \
  > pub-sealed-secrets.pem
```

4. Create a secret

```sh
kubectl -n default create secret generic basic-auth \
  --from-literal=user=admin \
  --from-literal=password=change-me \
  --dry-run=client \
  -o yaml > basic-auth.yaml
```

5. Seal the Secret

```sh
kubeseal --format=yaml --cert=pub-sealed-secrets.pem \
  < basic-auth.yaml > basic-auth-sealed.yaml
```

6. Apply the Sealed Secret

```sh
kubectl apply -f basic-auth-sealed.yaml
```

## References

All references I've used to create this project are listed as comments within each of their respective projects. In many cases I had to utilize several sources to create a working deployment file for my needs. If anyone has any questons or would like to reach out about the way I've done things, I'd be more than happy to talk about this project :grin:
