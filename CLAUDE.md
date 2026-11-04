# ZOE Games — instructions for Claude

Static game hub served at https://zoe.games by **GitHub Pages** (custom domain, HTTPS enforced).
The old DigitalOcean server does not serve this site. Do not change DNS, Pages settings, or `CNAME`.

## Environments

| Branch    | URL                          | Role |
| --------- | ---------------------------- | ---- |
| `staging` | https://zoe.games/staging/   | All work lands here first. Test banner, noindex. |
| `main`    | https://zoe.games/           | Production. Only updated by merging `staging`. |

Each successful push to either branch triggers *Validate games*, then *Publish production and staging*,
which rebuilds **both** branches into one Pages deployment. A failing check on either branch blocks
publishing for both, and the last good deploy stays live.

## Deploy rules

1. Never push directly to `main`. Commit to `staging` (or a feature branch with a PR into `staging`).
2. Before pushing, run `python3 scripts/check.py` and fix anything it reports.
3. After pushing to `staging`, check the Actions runs: *Validate games* and then *Publish production and staging*.
   Tell the user to test at https://zoe.games/staging/.
4. Promote only when the user says so: open a PR `staging` → `main`. Merge it only with the user's explicit OK.
   Do not delete `staging` after merging.
5. If a publish run fails, read its job logs and fix the cause on `staging`. Never disable or skip checks.

## Site rules (enforced by `scripts/check.py`)

- All internal links and asset paths must be **relative**, never starting with `/`, so pages work at both `/` and `/staging/`.
- Every linked directory needs an `index.html`. Links must stay inside the repo.
- Inline and `assets/` JavaScript must pass `node --check`.
- `CNAME` must contain exactly `zoe.games`.
- No build tools, npm packages, analytics, or external fonts. Plain HTML, CSS, and JS.
- Only `index.html`, `assets/`, `games/`, and `labs/` are published (see `scripts/build.py`). Anything else is not served.

## Adding or updating a game

Games are **snapshots** copied into this repo. Changes in a game's own repo never go live by themselves.

1. On `staging`, copy the game's browser build into `games/<slug>/` with `index.html` at its root and assets beneath it.
   Record the source repo and commit in the README's "Games and experiments" list.
2. Add a return link to the hub: `../../`.
3. Add or update its card in `index.html`. Playable games get `data-status="playable"` and a relative play link.
   Unfinished games get `data-status="development"` and no play link.
4. Staging and production share one origin. Any game using localStorage or IndexedDB must prefix its keys
   by environment, e.g. `location.pathname.startsWith('/staging/') ? 'staging:' : 'prod:'`, so testing can't overwrite real saves.
5. Run the checks, push to `staging`, and hand off to the user for testing.

Known game repos: `zombieorpheus/little-elsewhere`, `zombieorpheus/glyph-and-gold`, `zombieorpheus/grab-gold-go`
(server: `grab-gold-go-server`, which needs real hosting since Pages can't run server code), `zombieorpheus/ascii-rpg-world`.
