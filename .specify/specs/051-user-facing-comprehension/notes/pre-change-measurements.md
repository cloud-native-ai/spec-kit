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
BASE_SHA=925badb60860fdbbb8a5fade24cecb01627fbc6f
```

Re-derive: `git rev-parse gitlab/master` — the commit this feature's branch sits on.

**Range closed 2026-09-20** — the feature reached `Implemented` and was merged to `master`, so
the comparison now has an upper bound as well:

```
FEATURE_END_SHA=f8a287bef7b49007320123bd5b9306a540a1e705
```

Re-derive: `git rev-parse f8a287be` — this feature's last commit (its wrap-up glossary entry).

**Why the end bound was added.** `BASE_SHA` alone defines a half-open range: `git diff BASE_SHA`
compares the base against the **live working tree**, so it stays true only for as long as nothing
else in the repository ever touches the compared paths. Once this feature closed, that reading
turned two of its own guards into assertions about all future work rather than about itself —
`gate-neutrality` C-5 ("this feature adds no executable scripts outside `tests/contract/`") and
C-6 ("`src/specify_cli/`, `scripts/`, `templates/plan-template.md` are zero-change surfaces") both
went red the first time a later change legitimately edited `scripts/`, while the feature they were
written to judge had not changed at all. Both clauses are **historical** claims about one commit
span; the range now says so. Measured over the closed span `BASE_SHA..FEATURE_END_SHA` both hold
(0 files on the zero-change surfaces, 0 executables outside `tests/contract/`), and C-5's
anti-vacuity sentinel still finds this feature's own six test files inside the span — so bounding
the range preserves exactly what was being asserted and drops only the part that was never meant
to outlive the run.

**This does NOT re-freeze `BASE_SHA`.** Re-freezing the start would have made both clauses
unfalsifiable about the feature they document (a base equal to the present reports no changes by
construction). The start stays as frozen below, including through any future rebase of the branch.

**Re-frozen 2026-09-18 after the rebase onto `gitlab/master`** (supersedes the original
freeze `710c7179fc1896d85b5d7d0c8ad52719af18f558`, recorded at US1 kickoff). The rebase
replayed all 32 feature commits onto the new base, so every pre-rebase commit SHA — including
the original `BASE_SHA` — became **orphaned**: `git merge-base --is-ancestor 710c7179 HEAD`
now returns false. A comparison base that is not an ancestor of `HEAD` does not delimit
"what this feature changed"; `git diff 710c7179 HEAD` instead reports the union of this
feature's work **and the 4 upstream commits** picked up by the rebase. Two gates failed for
exactly that reason and named upstream's files as this feature's edits:

| Gate | Reported against the orphaned base | Against the re-frozen base |
|---|---|---|
| `scripts/` zero-change surface | `1` file (`scripts/python/derive-utils.py`, from upstream's `feat(derive)`) | **0** |
| new executables outside `tests/contract/` | `.specify/scripts/python/derive-utils.py`, `.specify/skills/browser-utils/scripts/chrome_open_trust.sh` (both upstream) | **0** |

So the re-freeze is not a relaxation — it removes upstream's changes from this feature's
measurement and makes the assertion strictly about the 33 commits on top of `gitlab/master`.
**Rule for any future rebase of this branch: `BASE_SHA` MUST be re-frozen to the new base in
the same operation**, because every comparative gate in this feature (GATE-1, GATE-2, GATE-4,
GATE-9, T011, T033, T055, T056, and contract clauses `gate-neutrality` C-5/C-6) reads this
literal. This file MUST carry exactly **one** `BASE_SHA=` line — the gates extract it with
`sed -n 's/^BASE_SHA=//p'` and the contract test with a `re.M` search, so a second line
would either break the shell substitution or be silently ignored.

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

**Post-rebase re-measurement (2026-09-18)**: `baseline-failed.txt` is **unchanged** — after
rebasing onto `gitlab/master` and fast-forwarding `master`, the suite reports
**26 failed, 2008 passed**, and `comm -13` against the frozen file is **empty in both
directions** (0 new, 0 gone). Two things moved underneath it without changing the set:

- **passed 1972 → 2008 (+36)**: upstream's four commits added tests
  (`test_derivation_definitions.py`, `test_derive_engine_contract.py`, `tests/derive_fixtures.py`,
  `test_derive_us3.py`, `test_derive_validate.py` and others). All 36 pass, so the failure
  set is untouched and this feature's 34 cases are still green.
- **the cause of 3 of the 26 changed while the count did not**: those three assert a
  whole-tree `sync-mirrors.py --check`. They previously failed on the `skills/draw-diagram/`
  drift, which this session committed and mirrored away; they now fail on the
  `skills/improve-skills/scripts/redline-check.py` drift that upstream itself shipped. See
  section ③. This is exactly why GATE-1 and GATE-2③ compare **name sets**, not counts — a
  count-only check would have reported "still 26, nothing changed" across a real change of
  cause.

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
DIFF  .specify/skills/improve-skills/scripts/redline-check.py
MIRROR_DRIFT_PREEXISTING_END
```

Re-derive:
```bash
python3 scripts/python/sync-mirrors.py --check 2>&1 | grep -E '^(MISS|DIFF)' | sort
```

**Re-frozen 2026-09-18 after the rebase onto `gitlab/master`.** The originally frozen set was
the two `skills/draw-diagram/` lines (one modified source file, one untracked file — another
unit's in-flight work). Both are gone from this set for two separate reasons:

1. That work was **committed at the user's direction** as its own clearly-attributed commit
   (`docs(draw-diagram): add the shared render-backend preflight and self-deploy fallback`),
   and its `.specify/` projection was then synced in a follow-up commit. Source and mirror
   now agree, so neither line is drift any more.
2. The single remaining line **arrived with the rebase** and is upstream's own: commit
   `925badb6 feat(improve-skills): add attribute-triggered red-line framework` committed
   `skills/improve-skills/scripts/redline-check.py` and its mirror with **different content**.
   Verified rather than assumed — extracting both blobs from upstream's own tree and
   comparing them:

   ```bash
   git show gitlab/master:skills/improve-skills/scripts/redline-check.py          > /tmp/up-src.py
   git show gitlab/master:.specify/skills/improve-skills/scripts/redline-check.py > /tmp/up-mir.py
   cmp /tmp/up-src.py /tmp/up-mir.py   # → differ: byte 6510, line 122
   ```

   The source carries the newer multi-line tuple formatting (14 lines where the mirror has
   7), i.e. the mirror is a **stale projection** of an earlier revision — upstream edited the
   source and did not re-sync. Repair is one command, `sync-mirrors.py --write --only
   skills/improve-skills`, but it is **deliberately not run here**: it is another unit's
   script, and folding its repair into this feature's branch would attribute their fix to
   this work. Reported as an upstream deviation instead.

Whole-tree `--check` is therefore still **EXIT=2**, while the scope this feature touches is
**EXIT=0**:

```bash
python3 scripts/python/sync-mirrors.py --check --only shared --only templates --only skills/summarize-project
# → ok templates/ · ok skills/ · ok shared/ · EXIT=0
```

Consequence for gates: GATE-2 / DoD-8 / T010 / T029 / T051 use the criterion "touched pairs
report `ok`, and the whole-tree `MISS`/`DIFF` set has **no new lines** versus this frozen
set" — never a whole-tree EXIT=0. `regen-command-copies.py --check` **is** clean today
(EXIT=0) and keeps an absolute criterion. Mirror writes MUST stay `--only`-scoped: a bare
`sync-mirrors.py --write` would absorb unrelated in-flight work into this feature's commits
and turn five gates green for the wrong reason (T050; `049`'s tasks forbid that action in the
same words).

**Three existing contract tests fail solely because of this one line** —
`test_trigger_engine.py::test_c2_sync_mirrors_check_clean`,
`test_scripts_distribution_parity.py::…::test_repo_has_no_orphan_or_drifted_scripts`, and
`test_browser_site_exclusions.py::…::test_mirror_check_ignores_site_probe` all assert a
whole-tree `--check`. They are part of the frozen failure set and MUST NOT be reported as
this feature's regressions. Note the *cause* moved while the *count* did not: before the
rebase these three failed on the draw-diagram lines, now they fail on the improve-skills
line. A count-only comparison would have hidden that, which is why GATE-2③ compares the
line **set** and not the number.

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

---

## ⑤ Unit + integration baseline (added at US3, 2026-09-18)

T001 froze only `tests/contract/`, because that is what GATE-1 and DoD-10 compare. US3 edited
`templates/constitution-template.md` and `.specify/memory/constitution.md`, which the
`tests/unit` and `tests/integration` suites also read, so their state had to be attributed
rather than assumed. Measured by running the same selection in a throwaway worktree at the
comparison base and diffing the failure-name sets:

```bash
git worktree add /tmp/base-wt gitlab/master
cd /tmp/base-wt && python3 -m pytest tests/unit tests/integration -q   # → 20 failed, 930 passed
cd - && python3 -m pytest tests/unit tests/integration -q              # → 20 failed, 930 passed
# comm -13 base now  → empty     (0 new)
# comm -23 base now  → empty     (0 healed)
```

**Result: 20 failures, identical name sets on both sides — all pre-existing, none caused by
this branch.** The two that look closest to this work are
`tests/integration/test_team_create_flow.py::…::test_skill_describes_team_file_schema` and
`tests/integration/test_zero_sdd_workflow_references.py::test_no_sdd_workflow_reference_in_source`;
both fail at the base commit too.

Recorded because "the contract suite is clean" is not the same claim as "the suite is clean":
a count-only comparison across two suites with different baselines would have hidden 20
failures, and a name-set comparison against the *wrong* base would have attributed them here.
The worktree was removed after use (`git worktree remove --force` + `prune`).
