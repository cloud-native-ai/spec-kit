# Pre-Change Measurements — Feature 051 (User-Facing Comprehension)

**Frozen by**: T001 · **Date**: 2026-09-18 · **Branch**: `051-user-facing-comprehension`

This file is the **single baseline source** for every comparative gate in this feature
(GATE-1, GATE-2, GATE-4, GATE-9, T010, T011, T029, T033, T051, T055, T056, T057).
Each value below carries the command that re-derives it. Values are measured, never
predicted: where `tasks.md` T001 listed a snapshot that disagreed with this run, the
measured value won and the disagreement is recorded inline.

---

## ① Comparison base

```
BASE_SHA=710c7179fc1896d85b5d7d0c8ad52719af18f558
```

Re-derive: `git rev-parse HEAD` (run at freeze time, before any US1 edit).

Every zero-change-surface assertion MUST compare against this literal SHA — `git diff
--name-only --no-renames --diff-filter=ACMR "$BASE" -- <paths>`. MUST NOT use `HEAD`
or `HEAD~<n>`: `HEAD` is blind to this feature's own committed work (the commit
discipline requires committing per task) and is **unconditionally vacuous in CI**, where
a clean checkout makes the worktree identical to `HEAD`. See `contracts/gate-neutrality.md`
C-6(a). The single legitimate `HEAD`-relative use is T002, which runs at kickoff when
`HEAD` *is* this SHA (C-6(c)).

MUST NOT use `--stat`: its line endings are `| N ++++` and long paths are elided to
`.../name`, so any path-shaped filter matches nothing (C-5, and the defect this froze).

## ② Test-failure baseline (re-frozen per C-7)

`baseline-failed.txt` was **overwritten** this run: **24 → 26** entries.

Re-derive:
```bash
python3 -m pytest tests/contract/ -q 2>&1 | grep '^FAILED' | sed -E 's/^FAILED //; s/ - .*$//' | sort
```

Suite totals at freeze time: **26 failed, 1972 passed**.

**Disagreement with the T001 snapshot, recorded per its own instruction**: the row cited
"24 failed / 1924 passed". Both numbers were stale — 24 was frozen on 2026-09-17 during
planning, and the passed count has since grown by 48 tests. The delta from 24 to 26 is
fully attributed:

- **+3 new failures**, all caused by uncommitted in-flight work in `skills/draw-diagram/`
  that postdates the planning baseline and is unrelated to this feature
  (`test_browser_site_exclusions.py::…::test_mirror_check_ignores_site_probe`,
  `test_scripts_distribution_parity.py::…::test_repo_has_no_orphan_or_drifted_scripts`,
  `test_trigger_engine.py::test_c2_sync_mirrors_check_clean` — all three assert a
  whole-tree `sync-mirrors.py --check`, which that drift turns to EXIT=2).
- **−1 self-healed**: `test_specify_script_paths.py::…::test_review_prerequisite_flags_are_supported`
  now passes because `tasks.md` exists (its `:90` asserts `tasks.md` appears in
  `check-prerequisites.sh` output). C-7 predicted this.

24 + 3 − 1 = 26. ✔

**Self-check that the freeze is usable** (GATE-1's exact pipeline against the freshly
frozen file):
```bash
comm -13 baseline-failed.txt <(re-run | normalise | sort)   # → empty
```
Result at freeze time: **empty**. GATE-1 and DoD-10 are therefore satisfiable from this
point, which they were not against the stale 24-entry file.

The `s/ - .*$//` normalisation is not optional: under `running_on_ci()` (true when `CI` or
`BUILD_NUMBER` is set) pytest appends ` - <crash message>` to each FAILED line, and the
baseline stores bare node IDs — omitting the `sed` makes every baseline entry mismatch and
`comm -13` report the whole baseline as "new failures".

## ③ Pre-existing mirror drift

```
MIRROR_DRIFT_PREEXISTING_BEGIN
DIFF  .specify/skills/draw-diagram/SKILL.md
MISS  .specify/skills/draw-diagram/references/self-deploy-render-service.md
MIRROR_DRIFT_PREEXISTING_END
```

Re-derive:
```bash
python3 scripts/python/sync-mirrors.py --check 2>&1 | grep -E '^(MISS|DIFF)' | sort
```

Attribution (verified, not assumed): `git status --porcelain skills/draw-diagram/` shows
one modified source file and one untracked file; both are uncommitted in-flight work, their
mtimes (2026-09-18 10:48/10:49) postdate this feature's 2026-09-17 planning baseline, and
`grep -c user-facing-comprehension` on both returns **0**. Whole-tree `--check` is therefore
**EXIT=2**, while the scope this feature touches is **EXIT=0**:

```bash
python3 scripts/python/sync-mirrors.py --check --only shared --only templates --only skills/summarize-project
# → ok templates/ (22 files) · ok skills/ (24 files) · ok shared/ (41 files) · EXIT=0
```

Consequence for gates: GATE-2 / DoD-8 / T010 / T029 / T051 use the criterion "touched pairs
report `ok`, and the whole-tree `MISS`/`DIFF` set has **no new lines** versus this frozen
set" — never a whole-tree EXIT=0. `regen-command-copies.py --check` **is** clean today
(EXIT=0) and keeps an absolute criterion. Mirror writes MUST stay `--only`-scoped: a bare
`sync-mirrors.py --write` would absorb the draw-diagram work into this feature's commits and
turn five gates green for the wrong reason (T050; `049`'s tasks forbid that action in the
same words).

This drift is expected to disappear when its author commits or syncs. When it does, T001's
re-freeze yields an empty set and the criterion's shape is unchanged.

## ④ Structural measurements

| Quantity | Measured | Re-derive |
|---|---|---|
| Confirmation-gate `total` | **23** (`destructive` 13 / `governance_kept` 10 / `violations` 0) | `python3 scripts/python/scan-confirmation-gates.py` |
| `shared/guidelines/*.md` | **11** | `ls -1 shared/guidelines/*.md \| wc -l` |
| `## ` sections in `templates/instructions-template.md` | **17** | `grep -c '^## ' templates/instructions-template.md` |
| `## ` sections in `.specify/instructions.md` | **18** | `grep -c '^## ' .specify/instructions.md` |
| Principles in `templates/constitution-template.md` | **11** (I…XI) | `grep -cE '^### [IVXLC0-9]+\.' templates/constitution-template.md` |
| Principles in `.specify/memory/constitution.md` | **14** (I…XIV) | same, on that file |
| `**MUST include** a principle for` entries | **5** | `grep -c '\*\*MUST include\*\* a principle for' templates/commands/constitution.md` |
| `len(BLOCKING_PATTERNS)` | **17** | importlib-load the scanner, then `len(m.BLOCKING_PATTERNS)` |

All eight agree with the T001 snapshot; none had drifted.

### Pointer targets before the change — 0 of 8

`grep -c 'shared/guidelines/user-facing-comprehension.md' <file>` returned **0** for all
eight rule-source files, confirming the discipline has no name and no pointer anywhere yet:

```
0  shared/guidelines/confirmation-gates.md
0  shared/workflow/feedback-step.md
0  shared/patterns/interview-pattern.md
0  templates/commands/clarify.md
0  shared/guidelines/requirements-guidelines.md
0  shared/guidelines/proactive-trigger.md
0  skills/summarize-project/references/reporting-playbook.md
0  shared/workflow/glossary.md
```

Re-derive: GATE-8's loop. After US2/US5 land, every line MUST read `1` — exactly one, per
`surface-pointers` C-1.

### Contract-clause inventory

Clause counts are **derived, never transcribed** (Principle XIV; see `plan.md` § Phase 1).
At freeze time: `grep -cE '^\*\*C-[0-9]+\*\*' contracts/*.md` → discipline-doc **18**,
surface-pointers **14**, constitution-export **13**, ambient-section **11**, gate-neutrality **7**.

---

## T002 — zero-change surfaces clean at kickoff

Appended by T002 (`[blockedBy: T001]`), run immediately after the freeze and before any
US1 edit. This is the comparison start point for T055's Phase 7 re-check.

```bash
BASE=$(sed -n 's/^BASE_SHA=//p' .specify/specs/051-user-facing-comprehension/notes/pre-change-measurements.md)
git diff --name-only --no-renames --diff-filter=ACMR "$BASE" -- src/specify_cli/ scripts/ templates/plan-template.md | wc -l
```

| Check | Command scope | Result |
|---|---|---|
| Three zero-change surfaces (T002 / C-6) | `src/specify_cli/`, `scripts/`, `templates/plan-template.md` | **0** — clean ✔ |
| GATE-4's full path set | the three above plus `.specify/scripts/` | **0** ✔ |
| GATE-9 repo-wide new-executable probe | whole tree, `.py`/`.sh`, excluding `tests/contract/` | **0** ✔ |

**Mechanism validated, not assumed.** The `sed -n 's/^BASE_SHA=//p'` extraction that
GATE-4, GATE-9, T011, T033, T055 and T056 all depend on was exercised end-to-end: it
returned `710c7179fc1896d85b5d7d0c8ad52719af18f558`, equal to `git rev-parse HEAD`, and
`git cat-file -t` resolves it as a `commit`. A gate whose baseline variable silently
expands to empty would compare against nothing and pass vacuously, so this is checked here
rather than discovered at T055.

At kickoff `HEAD` equals `BASE_SHA` and this feature has no commits yet, so the
`HEAD`-relative form would give the same answer here — this is the one place it is
legitimate (C-6(c)). The `"$BASE"` form is used anyway so this row cannot be copied as a
template into T011 / T033 / T055 / GATE-4, which run mid-implementation where `HEAD` is
wrong.
