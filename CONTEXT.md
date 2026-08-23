# CONTEXT.md -- read this before touching anything in this repository

This file exists so that a future version of me (Diogo), or any AI assistant
helping me, can pick this project back up without re-deriving everything from
scratch or reintroducing bugs that were already found and fixed. If you are
an AI reading this to make a change: read this whole file first, make the
change through `scripts/build_svgs.py` (not by hand-editing the SVGs), and
run the test suite before telling me it's done.

## 1. What this repository is

This is `diogoslsceno/diogoslsceno` -- a GitHub "profile README" repository.
Its `README.md` embeds two SVG cards (`light_mode.svg` and `dark_mode.svg`,
chosen automatically by the visitor's OS/browser theme) that render a
neofetch-style summary: an ASCII art portrait on the left, and system-info
style fields (OS, Uptime, languages, hobbies, contact) plus live GitHub
statistics on the right.

It was forked from `Vikbg/Vikbg` (Apache-2.0). The `NOTICE` file carries the
required attribution to that original project -- keep it if you ever
redistribute this repo or a derivative of it.

## 2. File map

```
today.py                   Core engine: SVG parsing/editing, GitHub GraphQL
                            + REST queries, age calculation, dot-leader
                            alignment. This is what actually runs in CI.
generate_readme.py         Thin entrypoint the Action calls. Wraps today.py
                            with the private-stats-in-memory-only privacy
                            guarantee described in its own docstring.
scripts/build_svgs.py       Regenerates dark_mode.svg / light_mode.svg from
                            plain Python data. THIS is how you edit the
                            static text on the card. See section 4.
light_mode.svg              Committed, ready-to-render output of
dark_mode.svg               scripts/build_svgs.py. Don't hand-edit these.
tests/                      32+ automated tests. Must pass before every
                            commit (the Action also runs them first and will
                            refuse to update the README if they fail).
.github/workflows/build.yaml  Daily cron (04:00 UTC) + push + manual trigger.
                            Runs tests, regenerates the dynamic fields
                            (Uptime, GitHub Stats), commits if anything
                            changed. See section 6 for the permissions model.
cache/                      requirements.txt, plus a per-user hashed cache
                            file the Action maintains at runtime (tracks
                            which public repos have already been counted, so
                            the LOC/commit stats don't need to be
                            recalculated from scratch every day). Don't hand
                            edit the hash file; it's regenerated automatically.
README.md                   Just the <picture>/<img> wrapper that embeds the
                            two SVGs from raw.githubusercontent.com.
NOTICE, LICENSE             Apache-2.0 + required attribution. Keep both.
```

## 3. Static data vs. live data -- read this before "fixing" a stale number

Fields on the card fall into two completely different categories:

**Static** (OS, Host, Kernel, IDE, Languages.*, Hobbies.*, Email.Work, the
ASCII art, the `diogo@diogoslsceno` header line): plain text baked into the
SVG. Nothing recalculates these automatically. **This is the category the
Ubuntu point-release update in section 5 belongs to.**

**Dynamic** (Uptime, and everything in the GitHub Stats block -- Repos,
Contributed, Stars, Commits, Followers, GitHub LOC): recalculated by
`today.py` on every Action run (daily cron, every push to `main`, or a
manual `workflow_dispatch`) and committed back automatically. Uptime comes
from `BIRTHDAY = datetime.datetime(2004, 11, 6)` in `today.py` -- never edit
the Uptime text by hand, it will just be overwritten (correctly) on the next
run. Never invent numbers for the GitHub Stats block either, for the same
reason.

If you're not sure which category a field is in, check
`today.SIMPLE_ROW_SPECS` and `scripts/build_svgs.py`'s `VALUES` dict: if a
field's value id is a key in `VALUES`, it's static; `age_data` and the
`*_data`/`loc_add`/`loc_del` ids in the GitHub Stats block are dynamic.

## 4. How to update static information

1. Edit the relevant entry in the `VALUES` dict (or `HEADER_USER`, or
   `ASCII_ART`) at the top of `scripts/build_svgs.py`. That file has a
   comment above each constant explaining exactly what it controls and why
   it's shaped the way it is -- read those comments, they document real bugs
   that happened here before (see section 7).
2. Run, from the repository root:
   ```
   python3 scripts/build_svgs.py
   ```
   This overwrites both `dark_mode.svg` and `light_mode.svg`.
3. Run the test suite:
   ```
   python -m unittest discover -s tests -v
   ```
   `tests/test_build_script.py` will fail if the committed SVGs and the
   script's output disagree on anything static -- that's the point, don't
   silence it, figure out why they disagree.
4. Commit `scripts/build_svgs.py` together with the regenerated
   `dark_mode.svg` and `light_mode.svg`.

Do not hand-edit the `<tspan>` text inside the SVGs directly. Every time
that's happened in this project's history it introduced a rendering bug
(see section 7) that wasn't caught until someone looked at the rendered
card.

## 5. Pending update: Ubuntu 26.04.1 LTS

The `os_value` field currently reads `Linux (Ubuntu 26.04 LTS)`. Ubuntu
26.04's first point release, **26.04.1 LTS**, is scheduled for **27 August
2026**. (It was originally announced for 4 August 2026, then officially
pushed back to 6 August, then delayed again to 27 August -- Canonical had
not published a public reason for the second delay as of early September
2026. If you're reading this well after that date, quickly check whether it
actually shipped on schedule before making the change -- point releases have
slipped before.)

**When 26.04.1 has actually shipped**, update it like this:

1. In `scripts/build_svgs.py`, change:
   ```python
   "os_value": "Linux (Ubuntu 26.04 LTS)",
   ```
   to:
   ```python
   "os_value": "Linux (Ubuntu 26.04.1 LTS)",
   ```
2. Regenerate and test as described in section 4.

Don't jump ahead of the actual release date -- verify (e.g. a quick web
search for "Ubuntu 26.04.1 LTS release notes") that it has shipped before
changing the text, since this specific point release has already slipped
twice.

## 6. GitHub Actions permissions -- why this matters

The workflow declares `permissions: contents: write` at the top level so the
`Commit generated profile outputs` step can push back to `main` using the
Action's own token -- no extra repo setting needs to be touched for that
part.

The `ACCESS_TOKEN` environment variable follows a **fallback pattern**:

```yaml
ACCESS_TOKEN: ${{ secrets.ACCESS_TOKEN || github.token }}
```

Without a repository secret named `ACCESS_TOKEN` configured, it falls back
to the Action's own `github.token`. That token is scoped to this repository
only, so `today.py`/`generate_readme.py` will still publish public
repo/star totals but **will show reduced GitHub Stats** (no visibility into
private repositories' commits/LOC, since `github.token` can't read them).

**Do not reintroduce a hard failure here.** An earlier version of this
workflow had a step that ran `exit 1` if `ACCESS_TOKEN` wasn't set, on the
theory that it should force full configuration before running. In practice
this meant *every single Action run failed* until the secret was added,
which is a strictly worse outcome than "runs immediately with slightly
smaller numbers." `tests/test_stats_integrity.py::test_workflow_falls_back_to_default_token_and_stages_only_generated_outputs`
asserts the fallback is present and that there's no `exit 1` in the
workflow -- don't weaken that test to reintroduce the old behavior.

To unlock full private-repo stats, add a repository secret `ACCESS_TOKEN`
(Settings -> Secrets and variables -> Actions) containing a classic Personal
Access Token with `repo` and `read:user` scopes. `USER_NAME` is optional --
it defaults to `github.repository_owner` (`diogoslsceno`).

## 7. Bugs that already happened here (don't repeat them)

Recorded so nobody -- human or AI -- "fixes" `scripts/build_svgs.py` in a
way that reintroduces one of these:

- **Dot-leader padding not reaching the target width.** Every "key: ......
  value" row is padded to a *visible* total width of 60 characters (prefix +
  dots + value). `scripts/build_svgs.py` computes this with
  `today.build_dot_leader`, the exact function `today.py` itself uses at
  runtime -- don't hardcode a dot count.
- **Header separator line stopping short.** The `diogo@diogoslsceno -----`
  line at the top must also total 60 visible characters. When the header
  username was changed from `diogo@sales` to `diogo@diogoslsceno`, the dash
  count wasn't recalculated and the line visibly stopped ~12 characters
  short of the `- Contact` / `- GitHub Stats` lines below it.
  `scripts/build_svgs.py`'s `separator_line()` computes the dash count from
  `SEPARATOR_TARGET_WIDTH`, so this can't happen again as long as the header
  is edited through `HEADER_USER`.
- **ASCII art overlapping the info column.** The art and the info column
  share the card: art occupies roughly `x=[15, 390)`, info starts at
  `x=390`. An early version left the art flush against the left edge, which
  both looked off-center and, before the art was narrowed, actually
  overlapped the text column at its widest rows. The current `ART_X = 48`
  was derived by rendering the card and measuring the actual ink bounding
  box (see the comment above `ART_X` in `scripts/build_svgs.py`) -- if you
  change `ASCII_ART`'s dimensions, re-measure, don't eyeball it.
- **Ids drifting between the SVG and `today.py`.** `today.py` looks up
  fields by exact `id` (e.g. `languages_programming_value`). Early drafts of
  this project used different field names (`Languages.Application` /
  `.Systems` / `.Spoken`, an extra `Portfolio.Link`/`Instagram`/`Discord`
  contact block) than what actually ended up in `today.SIMPLE_ROW_SPECS`.
  `scripts/build_svgs.py` now imports `today.SIMPLE_ROW_SPECS` directly
  instead of maintaining a second copy of the id list, so this class of bug
  is now structurally impossible -- keep it that way.
- **A workflow that fails without ACCESS_TOKEN.** Covered in section 6.

## 8. Testing

```
pip install -r cache/requirements.txt --break-system-packages   # if needed
python -m unittest discover -s tests -v
```

All tests must pass before pushing. `tests/test_build_script.py` in
particular will catch any hand-edit of the SVGs that wasn't made through
`scripts/build_svgs.py`.
