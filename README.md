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
