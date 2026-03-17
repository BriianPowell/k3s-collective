# Secrets Management

1. Register Helm Repo

```sh
flux create source helm sealed-secrets \
  --interval=1h \
  --url=https://bitnami-labs.github.io/sealed-secrets
```

1. Create HelmRelease to install Sealed-Secrets Controller

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

1. Retrieve the public key:

```sh
kubeseal --fetch-cert \
  --controller-name=sealed-secrets-controller \
  --controller-namespace=flux-system \
  > pub-sealed-secrets.pem
```

1. Create a secret

```sh
kubectl -n default create secret generic basic-auth \
  --from-literal=user=admin \
  --from-literal=password=change-me \
  --dry-run=client \
  -o yaml > basic-auth.yaml
```

1. Seal the Secret

```sh
kubeseal --format=yaml --cert=pub-sealed-secrets.pem \
  < basic-auth.yaml > basic-auth-sealed.yaml
```

1. Apply the Sealed Secret

```sh
kubectl apply -f basic-auth-sealed.yaml
```
