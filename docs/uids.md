# Workload user and group ids

Every workload that needs a fixed uid/gid gets its number from this table, so two groups of apps
never share a number by accident and no app runs as a human login on the nodes.

## Rules

- **Never use 1000.** On the nodes uid 1000 is the administrator's login account, so a process that
  escaped its container as 1000 could read that account's files. Pick a number below.
- **One number per trust group**, not per app: apps that belong together (same namespace, same data)
  share one. A compromised app then only owns its group's files.
- **Containers only need the number.** A name on the node (`users.users.<name>` in the `nix-config`
  repo) is needed only when something on the host acts as that account. The media owner below has
  one, because a host service writes into the same files. Define it in
  `nix-config/hosts/sheol/media-user.nix`.
- **Leave images with their own fixed uid alone** (PostgreSQL 26, Grafana 472, Loki 10001,
  1Password Connect 999, Nextcloud 33, Mosquitto 1883, and the 65532/65534 exporters): they are
  already separate from any login, and changing them risks the app for no gain.
- **Set the same number everywhere it applies:** `PUID`/`PGID` or `runAsUser`/`runAsGroup`, and
  `fsGroup` where the pod uses it.

## Assigned ids

uid and gid are the same number in every row.

| Id | Group | Used by |
| ---- | ----- | ------- |
| 1500 | media files | Owner of `/mnt/moriyya/media/data` and of the config directories of the Sonarr/Radarr family, Bazarr, Deluge, Kapowarr, Lidarr and Readarr. Host account `media`. |
| 1501 | media config-only apps | Kavita, Seerr, Prowlarr, Tautulli, Recyclarr, FlareSolverr |
| 1502 | Plex | Plex only (the most exposed app, so it is kept apart from the media-file owner) |
| 1510 | monitoring | Prometheus |
| 1511 | utilities | Atuin, Reflector |
| 1512 | wiki | Wiki.js |

Next free id: 1513. Add a row here in the same change that uses the number.

## Changing an app's id

Which order is safe depends on how the app starts:

1. **App starts as root and drops to `PUID`** (linuxserver images, Plex): change the owner of shared
   data first (a root app keeps working while you do), then change the numbers. These images fix
   their own `/config` ownership on start.
2. **App runs as a fixed non-root id from the start** (`runAsUser`): do not change file owners
   first, the old id would lose access. Change `runAsUser`, `runAsGroup` and `fsGroup` together
   and let `fsGroup` fix the volume. Check the pod actually starts.
3. Take a snapshot of the dataset before changing shared data (`zfs snapshot -r moriyya@...`) so a
   mistake can be rolled back.
4. After the rollout, check the process owner (`/proc/*/status`, not `id`, because s6-based images
   report their root entrypoint), that the app writes its config, and one real operation (an
   import, a scan, a login).
