# Contributing

## Sign off every commit

```bash
git commit -s
```

Every commit needs a `Signed-off-by:` trailer (the
[DCO](https://developercertificate.org/)). `-s` generates it from your git
identity; don't write the line by hand.

## ⚠ Check the base repo on every PR

This repository is a **fork**, so GitHub defaults the base of a new pull request
to **`lshw/prc`** — upstream — not to us. Always confirm the base is
`osuosl/prc` and the branch is `main`:

```bash
gh pr create --repo osuosl/prc --base main
```

No repository setting changes this default; it has to be checked each time.

## Syncing with upstream: merge, never rebase

Upstream's default branch is still `master`; ours is `main`.

```bash
git fetch upstream
git checkout main
git merge upstream/master      # NOT rebase
```

Our translation commit rewrites `README.md`, `control/control.ino`, `link.txt`
and the BOM part-number column. Rebasing replays that on top of upstream and
re-conflicts every line, every time; merging conflicts once. Upstream has not
moved since 2020-02-01, so this should be rare.

## Working on the EDA files

These are gEDA formats. A GUI round-trip rewrites the **entire file**, renumbers
primitives and reorders sections, so a one-component change can produce a
thousand-line diff that nobody can review.

- Use `pcb-rnd` for `.pcb` and `lepton-schematic` for `.sch`. Both are in Debian.
- **Keep the diff reviewable.** If a GUI save produces churn far beyond your
  change, say so in the PR description.
- **`control2.*` is the current layout.** Anything exported — BOM, XY, Gerbers —
  must come from rev 3, not from `control.*` or `control1.*`.
- **Never regenerate the Gerber zips** unless you are actually respinning the
  board. They are the record of what was fabricated.
- Run `python3 tools/check_bom.py` before pushing.

## The pin assignments are a contract

`_24V_OUT`=D3, `NET_RESET`=D4, W5500 SPI on D10–D13, `DS`=A3, `PC_RESET`=A4,
`PC_POWER`=A5. Changing any of them here means changing
[osuosl/proc](https://github.com/osuosl/proc) in the same breath, and reflashing
every deployed board. See [AGENTS.md](AGENTS.md) §6.2 for the full map.

## Known-issue baseline

`tools/check_bom.py` fails on any BOM-versus-layout mismatch except those listed
in `tools/known_bom_issues.txt`. That file currently holds the unresolved R5
discrepancy, so CI blocks on *new* drift without being permanently red.

**When an entry is resolved, delete it** — that is what turns the check back on
for that part. Don't add entries to silence a finding you haven't investigated.

## What CI enforces

| Check | Blocking | Notes |
|---|---|---|
| BOM / layout consistency | yes | except the baselined entries above |
| Relative links in markdown resolve | yes | catches doc rot |

Neither needs EDA tooling, so CI stays fast and can't break when `pcb-rnd`
changes.
