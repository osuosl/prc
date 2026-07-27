# Contributing

## Commit messages

We use [Conventional Commits](https://www.conventionalcommits.org/), because
[release-please](https://github.com/googleapis/release-please) derives the
version bump and the changelog from them.

```
fix: correct the R5 value in both BOM exports

Longer explanation of why, and what you measured.

Refs: #1
Signed-off-by: Your Name <you@example.org>
```

| Type | Use for | Bumps |
|---|---|---|
| `feat` | a design change — new part, new net, a re-export | minor |
| `fix` | correcting something wrong in the design or its exports | patch |
| `docs`, `build`, `ci`, `refactor`, `chore` | everything else | none |

Most work here is `docs` or `fix`. Reserve `feat` for changes to the design
itself, and use `!` or a `BREAKING CHANGE:` footer when a change would make an
already-fabricated board incorrect — a changed pinout, a moved connector, a part
that is no longer compatible with firmware in the field.

**⚠ We do not squash-merge.** Every commit you write lands on `main` intact and
is parsed by release-please, so each one appears in the changelog on its own. CI
checks every commit in a PR for a conventional subject and a `Signed-off-by`
trailer.

## Sign off every commit

```bash
git commit -s
```

Every commit needs a `Signed-off-by:` trailer (the
[DCO](https://developercertificate.org/)). `-s` generates it from your git
identity; don't write the line by hand.

## Releases

Merging to `main` makes release-please open (or update) a release PR that bumps
`version.txt` and `CHANGELOG.md`. Merging that PR tags `vX.Y.Z` and publishes a
GitHub Release.

**A release here is a snapshot of the design and its documentation, not a
fabricated board revision.** Board revisions are `control.*`, `control1.*`,
`control2.*` and the unpublished V1.1. Don't conflate the two: `v1.2.0` says
nothing about which PCB is in the rack.

Never hand-edit [CHANGELOG.md](CHANGELOG.md) or `version.txt`; release-please
owns both. Release PRs are created with `GITHUB_TOKEN`, so CI does not run on
them and they show as blocked by branch protection — see
[Branch protection](#branch-protection).

## Branch protection

`main` is protected:

| Rule | Setting |
|---|---|
| Changes must go through a PR | yes, **0 approvals required** |
| Required status checks | all of them (see below) |
| Force pushes / deletions | blocked |
| Conversation resolution | required |
| Linear history | **not** required — merge commits are the workflow |
| Admin enforcement | **off** — see the release caveat below |

Approvals are not required so a solo maintainer can still land a fix. Review
anyway when there is someone to review.

### ⚠ The release PR will look blocked

release-please's PR is created with `GITHUB_TOKEN`, and by GitHub's design a
token-created PR **does not trigger workflows**. So the release PR gets no CI
runs, its required checks never report, and it shows as blocked.

Admin enforcement is deliberately off so a repo admin can merge it anyway. That
is a workaround, not a fix.

The workflow already reads `secrets.RELEASE_PLEASE_TOKEN` and falls back to
`GITHUB_TOKEN` when it is unset, so setting the secret is all that is needed.

**Creating the token** (needs org owner/admin):

1. <https://github.com/settings/personal-access-tokens/new> — a *fine-grained*
   PAT.
2. Resource owner: **osuosl**. Repository access: **only** `osuosl/proc` and
   `osuosl/prc`.
3. Repository permissions — exactly two:
   - **Contents: Read and write** (branches, commits, tags, releases)
   - **Pull requests: Read and write** (open and update the release PR)
4. Expiry: pick a date and put a calendar reminder on it. An expired token
   fails silently — release PRs simply stop appearing.
5. If the org requires approval for fine-grained PATs, approve it at
   *Organization settings → Personal access tokens → Pending requests*.

**Storing it** — set it once at the org so both repos share it:

```bash
gh secret set RELEASE_PLEASE_TOKEN --org osuosl --repos proc,prc
# paste the token at the prompt; it is read from stdin and never hits your shell history
```

Per-repo instead, if you prefer:

```bash
gh secret set RELEASE_PLEASE_TOKEN --repo osuosl/proc
gh secret set RELEASE_PLEASE_TOKEN --repo osuosl/prc
```

**After it works** — confirm a release PR shows CI runs, then close the loop by
turning admin enforcement back on, which is the whole point of the exercise:

```bash
gh api -X PATCH repos/osuosl/proc/branches/main/protection/enforce_admins
gh api -X PATCH repos/osuosl/prc/branches/main/protection/enforce_admins
```

**A note on authorship.** A user PAT makes release PRs appear authored by that
user, and they will not be able to approve their own PR if approvals are ever
required. A GitHub App installation token or a dedicated machine account avoids
both, at the cost of more setup. For two low-traffic repos a PAT is proportionate.

## Merging

**Merge commit or rebase — never squash.** Squashing collapses a branch into one
commit, which would reduce a PR's worth of distinct fixes to a single changelog
line and lose the individual sign-offs. Squash merging is disabled on the
repository for that reason.

Keep the branch tidy before it merges, since nothing will tidy it afterwards:
fold up "fix typo" commits with `git rebase -i`, and make sure each surviving
commit is one logical change.

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

## Dependency updates

Dependabot opens a **single grouped PR** for GitHub Actions, weekly on Monday —
one PR for all actions rather than one per action.

Its commits are prefixed **`chore(deps):`**, so they never trigger a release
(only `feat`, `fix` and breaking changes bump a version) and stay out of the
changelog, while still satisfying the conventional-commit check.

Bot authors are exempt from the sign-off requirement, because Dependabot has no
DCO option. They are not exempt from the format check.

Nothing else here has a manifest Dependabot understands: `tools/check_bom.py` is
pure standard library, by design, so CI has no dependencies to drift.

## What CI enforces

| Check | Blocking | Notes |
|---|---|---|
| BOM / layout consistency | yes | except the baselined entries above |
| Relative links in markdown resolve | yes | cross-repo links must be absolute URLs |
| Conventional subject + sign-off, every commit | yes | commits land on `main` intact and drive the changelog |

None of these need EDA tooling, so CI stays fast and can't break when `pcb-rnd`
changes.
