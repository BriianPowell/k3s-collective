# k3s-collective

FluxCD GitOps repo for a two-node k3s cluster in a home office. Flux reconciles
`clusters/k3s`; do not `kubectl apply` manifests by hand except to debug.

## Nodes

| Name    | CPU      | Memory                 | GPU        |
| ------- | -------- | ---------------------- | ---------- |
| Sheol   | i7-6700k | 32 GiB DDR4 @ 3000 MHz | RTX-3080   |
| Abaddon | i5-6600T | 16 GiB DDR4 @ 2400 MHz | Integrated |

The nodes run NixOS; their configuration is in the separate `nix-config` repo
(`hosts/sheol`, `hosts/abaddon`). GPU workloads (e.g. Plex) use the
`nvidia-device-plugin` from `infrastructure/controllers/nvidia.yaml`.

## Layout

- `clusters/k3s/`: Flux entrypoint and Kustomizations (`base`, `infrastructure`,
  `media`, `monitoring`, `games`, `utilities`).
- `infrastructure/`: controllers, configs, namespaces, policies, secrets.
- `apps/<group>/<app>/`: one folder per app, usually a `HelmRelease` plus its
  `HelmRepository`.

## Tools

`helm`, `kustomize`, `kubeconform`, `yq` and `jq` are not installed on the Mac;
they, plus `kubectl` and `flux`, come from the devShell in the nix-config repo.
Run them with `nix develop ~/Code/Self/nix-config -c <cmd>`, e.g.
`nix develop ~/Code/Self/nix-config -c kustomize build apps/media/plex`.

## Conventions

- Add apps as Flux `HelmRelease`s next to a `HelmRepository`, with
  `app.kubernetes.io/*` labels, matching neighbouring apps.
- Secrets come from 1Password through the 1Password Connect operator
  (`OnePasswordItem`). Field labels must match the secret keys the manifests
  reference. Never put secret values in git; see `infrastructure/secrets/README.md`.
- Monitoring is Prometheus, Grafana, Loki and Alloy. New services should expose
  metrics and a `ServiceMonitor` where the app supports it.
- Reference links go in comments at the top of each manifest, as existing files do.
