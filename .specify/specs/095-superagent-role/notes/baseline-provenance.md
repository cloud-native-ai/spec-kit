# Baseline provenance — implement-start full-suite baseline (reconstructed)

**Why this file exists**: the Setup package (T001) was marked closed but left no `--names-out` artifact on disk (measured: no `baseline-*` file existed under the spec directory or `notes/` at P5 start; the same absence is disclosed in `test-evidence/zero-mechanism-readings.txt` §5). Per `.specify/templates/commands/implement.md` § Baseline pre-flight, a missing baseline is a **first capture with provenance recorded**, never zero drift.

**What was reconstructed** (2026-11-10, P6):

1. Throwaway worktree at the P1 parent commit — the tree as it stood immediately before the first implement commit:
   `git worktree add --detach .specify/.tmp/095-base-wt c671e168a`
2. The 29 pre-existing dirty **tracked** files were copied into the worktree (the current `git status` dirty set — every 095 edit is committed, so this residual dirt is exactly the pre-existing drift that was present at implement start).
3. The canonical runner was executed in that worktree:
   `bash scripts/bash/run-tests.sh --names-out baseline-names.txt` → exit 1, **303 failed**, 8335 passed, 2 skipped.

**Classification** (implement.md vocabulary): `inherited` — the 303 failures belong to the pre-feature tree (frozen/known reds of earlier features plus environment drift), not to this feature. Baseline-only names (72) are not adjudicated individually; the Completion Gate reads only NEW names (`comm -13`).

**Known limit of the reproduction**: untracked `.specify/.tmp/` scratch existed in the working tree at implement start but was not reproduced in the worktree. Two closure-run failures therefore appear as NEW only because their cause lives in that untracked scratch (root-owned probe files; other lines' temp worktrees). Both are adjudicated row by row in `test-evidence/closure-suite-comparison.txt`.

**Landing**: the reconstructed names list is `notes/baseline-failed-names.txt` (303 entries, pure names — no header, so `comm` stays valid). This path matches the baseline pre-flight glob (`<spec-dir>/notes/baseline-*`), so a future implement run re-captures it instead of deriving it again.

## Per-module guard health and in-range attribution (review F2, measured 2026-11-10)

Name-set subtraction alone is not an attribution: a guard broken by a commit inside the review range is red at the
reconstruction tree too (the tree sits after those commits), so it would be absorbed as "inherited". The rule
applied here: **a failure is classified `inherited` only when it is also red at the range base**; a red that first
appears inside the range is attributed to the in-range commit that caused it.

| Tree | Command | Reading |
|------|---------|---------|
| Range base `b3da3a26d` (throwaway worktree `.specify/.tmp/095-base-b3da`) | `bash scripts/bash/run-tests.sh tests/unit/test_status_digest_unit.py tests/contract/test_efficiency_element.py -q` | exit 1 — **18 failed / 23 passed** |
| Reconstruction tree `c671e168a` (the two module files are unchanged in `c671e168a..HEAD`, so this equals the pre-repair HEAD reading) | same command | exit 1 — **18 failed / 23 passed** |
| Repaired tree (review-repair r1) | same command | exit 0 — **41 passed** (`test-evidence/review-repair-suite.txt`) |

Name-level comparison of the two red sets:

- **17 names red at BOTH trees** — red before the review range, attributable to the master-side digest redesign
  (`9ac56bf10`, `fb5125eae` — ancestors of the range base), not to Feature 095. Legitimately `inherited`; they were
  nevertheless blocking at HEAD and are repaired in this round.
- **1 name red only at HEAD** — `tests/unit/test_status_digest_unit.py::test_projected_state_is_a_member_of_the_engine_state_set`,
  introduced inside the range by the executor-primary revision `c2f199955` (closed lines leave the capped view).
  **Refused as `inherited`**; repaired by aligning the guard to the declared reader revision (the state remains in
  `all_entries`).
- **1 name red only at the range base** — `tests/contract/test_efficiency_element.py::test_c70_neither_delivered_script_names_a_schema_version_field_slot_or_quality_subkey`,
  fixed inside the range.

**Known limit of the reproduction, corrected**: the earlier "all 303 are inherited" classification was too broad.
The 18 red guards were red at the reconstructed baseline because the baseline post-dates the master-side redesign;
17 of them also pre-date the review range, and one was introduced in-range. The repaired tree re-measures both
modules green, so the closure comparison's "zero NEW attributable to this feature" is now supported by measured
green modules, not only by name-set subtraction.
