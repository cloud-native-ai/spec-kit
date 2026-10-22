# Efficiency Diagnosis — 065a implement stage (2026-10-22)

Dated record; input to spec 067-loop-efficiency-hardening. Not a runtime guarantee.

## Observed checkpoint

- 065a implement: 30 tasks / 60 clauses.
- Sub-dispatches: 6 recorded; 2 failed before the budget change (40-turn limit; output-token limit); T003–T014 completed by 3 bounded parts after the budget was raised to 120.
- Tasks: 14/30 done, 16 open.
- Tests: unit 58 + contract 25 = 83; 57 passed / 26 failed. The 26 reds were concentrated: T015 actions 18, T016 probe 5, T018 reference 3.
- Commits: `0989d804`, `33500623`, `55bc4ec4`, `0ac387eb`, `35aa0192`.
- token/elapsed: run-determination recorded `not_evaluated`; only dispatch count, task completion, and red-test count are available as proxies.

## Root causes

1. **Part sizing by task ID, not by verifiable outcome.** T003–T008 and T009–T014 were six tasks each but coupled test authoring and engine implementation; the apparent task count understated the work.
2. **Test-first surface too large and mostly one-test-per-scenario.** 83 tests preceded the engine; the T015 action matrix and T016 probe matrix are natural tables but were written as individual tests.
3. **Context reacquisition per sub-dispatch.** The state spine had high-level checkpoints but no part brief (task IDs, files, test node IDs/commands, expected red→green, no-go files).
4. **Output discipline.** The first failure was the 40-turn budget; the second was a monolithic response hitting the output-token limit.
5. **Micro-gaps dispatched separately.** The `state_dir` R-02 fallback was a real U4 catch but required its own micro-dispatch.
6. **No dispatch-level measurement.** Token/time are not instrumented; budget adequacy and part sizing could not be measured.

## What already worked

- `run-turn-budget` 40 → 120, codified in `agents/sdd-executor.agent.md` and rendered for qoder/opencode (`696d5f4b`).
- Skill source now says: large stages split into ≤8-task parts; incremental tool writes; state spine records `part_scope`.
- C1a/C2/C2.5 completed within the new budget; C2's engine core made 54 tests pass.

## Recommended next split (for the 065a cycle and future runs)

1. T015 actions (18 reds) — table-driven C-46 matrix.
2. T016–T017 probe/self-test (5 reds) — probe matrix + self-test cases.
3. T018 reference (3 reds) — owner reference and parity assertions.
4. T019–T025 docs/mirror/compat.
5. T026–T030 mutation/regression/verification/gates.

## Efficiency rules to carry forward

- Part brief before every dispatch; dispatch log after every part.
- Table-driven tests for matrix contracts; targeted test selection; full suite only at the 063 two slots.
- Small residuals fold into the next part unless gate-blocking.
- Pre-authorize non-destructive implement/test segments; keep destructive gates.
- Record unavailable metrics as `not_evaluated`, never as zero or a guess.
