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

`kubectl`, `flux` and `jq` are on the Mac's PATH. `helm`, `kustomize`, `kubeconform` and `yq`
are not installed, and the nix-config devShell no longer provides them (it has only `git` and
`transcrypt`). Use an ad-hoc shell, e.g.
`nix shell nixpkgs#kustomize nixpkgs#kubeconform nixpkgs#yq-go -c kustomize build apps/media/plex`
(`nixpkgs#kubernetes-helm` for `helm`). Re-check with `command -v` if a tool seems missing.

## Conventions

- Add apps as Flux `HelmRelease`s next to a `HelmRepository`, with
  `app.kubernetes.io/*` labels, matching neighbouring apps.
- Secrets come from 1Password through the 1Password Connect operator
  (`OnePasswordItem`). Field labels must match the secret keys the manifests
  reference. Never put secret values in git; see `infrastructure/secrets/README.md`.
- Monitoring is Prometheus, Grafana, Loki and Alloy. New services should expose
  metrics and a `ServiceMonitor` where the app supports it.
- Reference links go in comments at the top of each manifest, as existing files do.

## Security

This repo is public. Never commit secrets, tokens, or notes about which services are weak.

- **Workloads:** run as non-root, set `allowPrivilegeEscalation: false`, `seccompProfile:
  RuntimeDefault` and drop all capabilities where the app allows. Set
  `automountServiceAccountToken: false` unless the app talks to the Kubernetes API. Do not infer
  "runs as root" from the pod spec alone; many images drop privileges themselves. Check with
  `kubectl exec <pod> -- id`, but for s6-based images (linuxserver) `id` reports the root
  entrypoint even when the app runs as `PUID`; read process owners from `/proc/*/status` too.
- **Exposure:** assume every hostname Traefik routes is reachable from the internet. A new
  `IngressRoute` needs SSO (`traefik-forward-auth`) in front, or an app login you have verified.
  Do not add a public route for something only other pods use; they call the Service name.
- **Behind Traefik, clients look local** (the pod IP). Any "no auth for local addresses" setting
  in an app is effectively "no auth". Loopback is often trusted too, so test auth from a
  non-loopback address.
- **Network policies:** put per-app egress restrictions in `infrastructure/policies`, not in the
  app directory. App kustomizations use `commonLabels`, which rewrites a policy's `podSelector`
  and can make it silently select nothing; select on `app.kubernetes.io/name` only. Policies are
  additive, so a pod covered by an allow-all policy must be excluded from it
  (`matchExpressions NotIn`) for a restriction to take effect.
- **Images:** pin by tag; pin by digest only where Flux image automation (a
  `# {"$imagepolicy": ...}` marker) is not managing the line, because automation rewrites it and
  drops the digest. The cluster's Flux (v2.3.0) has no digest reflection; that needs a Flux
  upgrade and moving image APIs from `v1beta2` to `v1` (see `.memories/` if present).
- **Verify before handing back:** render with `kustomize build`, run `kubeconform`, run
  `kubectl apply --dry-run=server`, and confirm any policy selector matches the live pod's
  labels (a dry-run cannot detect a no-op policy). After rollout, test the behaviour, not just
  that the pod is Running.
- **Workflow:** the maintainer commits and pushes. Agents edit and verify, and do not commit or
  push.

## Local notes

`.memories/` is gitignored (this repo is public) and may not exist on a fresh clone. If it is
present, read `.memories/security-hardening.md` before changing exposure, auth, network policies
or pod security: it has the incident history, what is verified, and a per-service tracker.
Treat it as a hint, not truth; re-verify against the cluster, and update it when you finish a
service.
