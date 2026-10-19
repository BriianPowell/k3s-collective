#!/usr/bin/env bash
# Pre-commit check for manifests: render each touched kustomization with `kustomize build` and
# validate the output with `kubeconform`. Files outside any kustomization are validated directly.
#
# CRDs without a published schema (Traefik, Flux, 1Password) are skipped, not failed
# (-ignore-missing-schemas), so this catches YAML/Kubernetes-schema mistakes and broken
# kustomizations, not CRD field typos. `kubectl apply --dry-run=server` covers those.
#
# kustomize and kubeconform are not installed globally; if they are not on PATH this re-runs
# itself inside an ad-hoc nix shell (see AGENTS.md).
#
# https://github.com/yannh/kubeconform
# https://kubectl.docs.kubernetes.io/references/kustomize/
set -euo pipefail

cd "$(git rev-parse --show-toplevel)"

if ! command -v kustomize >/dev/null 2>&1 || ! command -v kubeconform >/dev/null 2>&1; then
  if ! command -v nix >/dev/null 2>&1; then
    echo "pre-commit-render: kustomize/kubeconform not found and nix is not available" >&2
    exit 1
  fi
  exec nix shell nixpkgs#kustomize nixpkgs#kubeconform -c "$0" "$@"
fi

declare -A dirs=()
declare -A files=()

for f in "$@"; do
  [ -f "$f" ] || continue
  d=$(dirname "$f")
  while [ "$d" != "." ] && [ ! -f "$d/kustomization.yaml" ]; do
    d=$(dirname "$d")
  done
  if [ "$d" != "." ]; then
    dirs["$d"]=1
  else
    files["$f"]=1
  fi
done

status=0
kc=(kubeconform -strict -ignore-missing-schemas -summary)

for d in "${!dirs[@]}"; do
  echo "== kustomize build $d"
  if ! out=$(kustomize build "$d" 2>&1); then
    echo "$out" >&2
    status=1
    continue
  fi
  printf '%s\n' "$out" | "${kc[@]}" - || status=1
done

for f in "${!files[@]}"; do
  echo "== kubeconform $f"
  "${kc[@]}" "$f" || status=1
done

exit "$status"
