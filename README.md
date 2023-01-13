# k3s-collective

Collection of helm charts and deployment definitions for my k3s cluster

## Install Flux into your Cluster

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

## To Use Secrets

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
  --chart-version=">=1.15.0-0" \
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

## Infrastructure

- [x] [Traefik](https://artifacthub.io/packages/helm/traefik/traefik)
- [x] [Kubed](https://appscode.com/products/kubed/v0.12.0/welcome/)
- [x] [System Upgrade Controller](https://github.com/rancher/system-upgrade-controller)
- [x] [Keycloak](https://github.com/keycloak/keycloak)
- [x] [Traefik Forward Auth](https://github.com/thomseddon/traefik-forward-auth)
- [x] [Grafana](https://github.com/grafana/grafana)
- [x] [Prometheus](https://prometheus.io/)
- [x] [alertmanager](https://github.com/prometheus/alertmanager)
- [x] [kube-state-metrics](https://github.com/kubernetes/kube-state-metrics)
- [x] [node_exporter](https://github.com/prometheus/node_exporter)
- [x] [HomeAssistant](https://www.home-assistant.io/)
- [ ] [Nextcloud](https://github.com/nextcloud/server)
- [ ] [Scrutiny](https://github.com/AnalogJ/scrutiny) - **find alternative** as this is not compatible with k8s
- [ ] [Gotify](https://github.com/gotify/server) - **find alternative** as is not possible with iOS
- [ ] CrowdSec - maybe worth looking into
- [ ] Graylog 

## Helpful References

- <https://stackoverflow.com/questions/60528376/traefik-redirect-from-one-host-to-another>
- <https://community.traefik.io/t/cant-route-to-other-ip-port-on-subnet/11152/2>
- <https://kubernetes.io/docs/reference/kubectl/cheatsheet/>
- <https://github.com/cert-manager/cert-manager>
- <https://devopscube.com/setup-prometheus-monitoring-on-kubernetes/>
- <https://github.com/fluxcd/flux2-kustomize-helm-example>

## Helpful Debugging

Useful to verify k8s DNS entries

```bash
kubectl create -f https://k8s.io/examples/admin/dns/busybox.yaml
kubectl exec -ti busybox -- nslookup kubernetes.default homeassistant.homeassistant.svc:8123
```
