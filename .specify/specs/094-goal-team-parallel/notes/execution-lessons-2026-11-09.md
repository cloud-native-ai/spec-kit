# Execution Lessons (2026-11-09) — from the 091 close-out run into 092

## 091 measured lessons
1. **Single-agent implement is the bottleneck**: 62 tasks in one 500-turn agent took 116 min and hit the turn limit. The fix (landed in 091): ~10 tasks/package (<=16), up to 6 concurrent implement executors, worktree writes + the existing integration queue; validated by the 091 3-package fix loop with zero integration conflicts.
2. **Worktrees contaminate tree-scanning tests**: the three fix worktrees under `.specify/.tmp` were seen by the goal-migration/isomorphism/script-interface tests as duplicate repo copies. The closure suite MUST run after the fix worktrees are removed (HR11 cleanup).
3. **Parallel runner readings are not the closure comparison surface**: `run-tests.sh` parallel mode writes bare ids, while the frozen baseline is the serial `FAILED`-prefixed list. Use the serial failed-id set for GATE-1.
4. **Test expectations drift with legitimate changes**: a tracked `test-evidence/*.txt` run log was counted as a live face; modified command files were treated as added commands. Dated-record and added-vs-modified distinctions belong in the tests.
5. **Verification writer/checker format**: `closure-acceptance-check.py` reads `SC-NNN_status=`; a Markdown table alone reads as `unknown`. Emit the machine-readable block.
6. **Gate/engine argument shapes**: `pre-analyze-check` `clean_cell` (paired code span + prose) and `overlap-check` vacuous clear; `run-determination` `--collected`/`--names-*`/`--green-check` shapes. These cost avoidable rework; encode them in the plan's evidence rules.
7. **Renumber/accept leaves stale records**: 088's verification notes and `cl-01` still quoted the pre-renumber 087 block; the record was corrected. Any renumber or second acceptance must update the verification/notes/evidence pointers.
8. **The spec-local goal/team is the 092 subject**: the 092 run itself follows the current 085 protocol (spec-local goal created) until this feature lands the `.specify/goal|teams` migration.

## 094 run lessons so far
- Clarify's `id-contiguous` rejects letter-suffixed ids; a mid-file add forced a full-tail renumber. Safe add/remove with programmatic remapping is missing.
- `ref-resolvable` strips inline code, so `[[STR-NNN]]` inside backticks is silently uncited (a silent trap in the owner).
- Clarify gates reuse `--stage requirements`; evidence filenames need the stage suffix to stay distinguishable.

## Directive for this run
- Use large-concurrency subagents wherever dependencies allow: plan executors partitioned in parallel (up to 6), implement ~10 tasks/package up to 6 concurrent with worktree writes, review segments parallel. The goal/team "construction crew" is the consumer of the complex handoff; the spec "designer" retains design authority.

## Addendum (2026-11-09): parallel-line isolation is mandatory
- Dispatching the 092 tasks and the 093 requirements in one working tree put the 092 commits on the 093 branch (the two lines mixed). The correction moved 092 back to `master` via cherry-pick and rebuilt a clean `093-concurrency-by-default` branch.
- Parallel lines MUST each run in their own worktree (worktree-per-write-line, 064/084); the driver's multi-line dispatch uses the line registry + worktrees, never one shared tree.
- 093's dispatch-capability/default-concurrency requirements and this lesson are the same rule: concurrency without write isolation is not safe concurrency.
