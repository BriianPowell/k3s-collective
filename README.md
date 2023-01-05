# k3s-collective

Collection of helm charts and deployment definitions for my k3s cluster

## Install Flux into your Cluster

```sh
flux bootstrap github \
  --owner=BriianPowell \
  --repository=k3s-collective \
  --branch=master \
  --path=clusters/k3s \
  --personal \
  --private
```
