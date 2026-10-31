# ZOE Games

A lightweight, responsive game shelf for https://zoe.games.

## Environments

| Purpose | Branch | URL |
| --- | --- | --- |
| Production | `main` | https://zoe.games/ |
| Staging | `staging` | https://zoe.games/staging/ |

`main` is the production branch. Keep its name so existing Pages links and configuration remain recognizable. Work on `staging` or feature branches targeting `staging`. Test the staging URL, then open a pull request from `staging` into `main`. Merge only the changes you want released. Do not delete the staging branch after merging.

Staging is publicly accessible for testing, has a test banner, and requests no indexing. It is not password protected. Both paths share an origin. Current imported games do not store saves; future games that add localStorage or IndexedDB must namespace staging saves separately from production.

## GitHub Pages setup

The publish workflow sets Pages Source to **GitHub Actions** to prevent the legacy branch publisher from overwriting staging. If permissions prevent this automatic setup, set it in Settings → Pages → Build and deployment. Keep the custom domain `zoe.games`. The `github-pages` environment must permit deployments from `main`.

`Validate games` runs checks for pushes and pull requests. After a successful push check, `Publish production and staging` runs on the default branch. It packages `main` at the root and the separate `staging` branch under `/staging/`, then deploys the combined artifact. This default-branch deployment avoids granting the staging branch direct production-environment deployment rights. Fork PRs do not deploy. No third-party hosting account or secret is needed.

The latest snapshots of both branches are revalidated before deployment. A failing snapshot stops publication; the last deployed version remains live. Deployment jobs are serialized. You can rerun publication using its Run workflow button on `main`.

## Games and experiments

- `games/little-elsewhere/`: playable living-world prototype, imported from `ZombieOrpheus/Little-Elsewhere` at blob `ac72c4d242af1ea608686b110d581e8387e68a13`.
- `labs/ascii-library/`: living text art experiments from that same repository.
- Goblin Gold: source not yet located. The shelf intentionally has no play link until a real build is added.
- Other projects are marked in development, with no misleading play buttons.

Game builds are snapshots in this repository, so later changes in a separate game repository cannot silently change production. To update a game, copy its approved browser build into the corresponding staging folder and test before promotion.

## Add a game

1. Work on `staging`. Put its browser build under `games/<slug>/index.html` with any assets beneath that folder.
2. Use relative asset and navigation paths so the same game works at both environment URLs. Add a return link to `../../`.
3. Add its card to `index.html` with `data-status="playable"` and a relative play URL. Until the build exists, use `data-status="development"` without a play link.
4. Run `python3 scripts/check.py`, push, and test `/staging/` with keyboard and touch.
5. Open a staging → main pull request and merge after testing.

## Local checks

Requires Python 3 and Node.js. No npm packages, build framework, analytics, or external fonts are needed.

```sh
python3 scripts/check.py
python3 scripts/build.py --production /path/to/main-checkout --staging /path/to/staging-checkout --output /tmp/zoe-games-preview
```

Choose an output path outside both source checkouts that does not already exist. Only explicitly listed public files are packaged; repository metadata and scripts are excluded.
