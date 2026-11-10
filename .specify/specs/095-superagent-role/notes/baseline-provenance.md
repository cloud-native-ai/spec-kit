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
