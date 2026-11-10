# 098 test-evidence index

Owner of the mapping: `tasks.md` T059. Every success criterion SC-001…SC-011 links to the
evidence path(s) that carry its reading; the feature's coverage baseline and the closure
records are included. Paths are relative to `.specify/specs/098-suite-speed-optimizations/`.
Statuses: `pass` = the reading exists and supports the criterion; `supporting` = the
criterion's declared path; `pending-closure` = executed by the driver's closure stage (T061).

| SC | Path | Evidence |
|----|------|----------|
| SC-001 | final | `test-evidence/full-collection-diff.txt` — removed 0 / added 46 (the five new contract files); baseline id set in `notes/pre-change-measurements.md` (`implement-start-full-ids` block, 8543 ids from base `b3da3a26d`); disposed list `test-evidence/full-collection-disposed.txt` |
| SC-002 | final | `test-evidence/parallel-consistency-contract.txt` (commands, exits, durations, both empty `comm` directions, non-parallel-safe drill); name lists `test-evidence/parallel-contract-parallel-names.txt`, `test-evidence/parallel-contract-serial-names.txt`; mutation drills `test-evidence/parallel-mutations.txt`; final-tree quickstart re-check `notes/quickstart-run.md` §S-4 with lists `test-evidence/quickstart-s4-parallel-names.txt`, `test-evidence/quickstart-s4-serial-names.txt`; **review-repair r1**: `test-evidence/review-repair-r1-sc002-comm.txt` — both `comm` directions empty (137/137 names), lists `test-evidence/review-repair-s4-parallel-names.txt` / `-serial-names.txt`, logs `test-evidence/run-logs/review-repair-s4-{parallel,serial}.log.gz`, root-cause record `test-evidence/review-repair-r1-trigger-fix.txt` |
| SC-003 | final | `test-evidence/closure.txt` — pending-closure (T061: slot-2 full-tier `--names-out` vs `baseline-failed.txt`, plus the same-tree `--full --serial` bidirectional name comparison); current status `partial` with the ladder in `verification.md` (subset analogue = SC-002's record) |
| SC-004 | final | `test-evidence/tier-measurements.txt` — default-tier parallel vs same-selection serial walls (73.42 s vs 692.15 s, ratio 10.6 % ≤ 50 %), selection-equality collection readings; complete outputs `test-evidence/run-logs/default-parallel.log.gz`, `test-evidence/run-logs/default-serial.log.gz`; scope-disclosure readings |
| SC-005 | final | `test-evidence/tier-measurements.txt` (slot-1 full wall 70.99 s, full/default raw walls and the ≤ 110 % premise); complete slot-1 output `test-evidence/run-logs/slot1-full.log.gz`; `test-evidence/closure.txt` — pending-closure (slot 2 + wall ratio); **review-repair r1**: `test-evidence/review-repair-r1-sc005-walls.txt` — rebuilt pre-change baseline 76.52 s vs final tree 70.73 s = 92.4 % ≤ 110 % (throwaway worktree at `af73f65f1`); names `test-evidence/review-repair-prechange-failed.txt` / `review-repair-final-failed.txt`, logs `test-evidence/run-logs/review-repair-{prechange,final}-full.log.gz`; current status `partial` (two-slot completeness = T061) |
| SC-006 | final | `test-evidence/tier-contract-green.txt`; `test-evidence/slow-members.md`; `test-evidence/slow-members-measurement.txt`; mutation drills `test-evidence/tier-mutations.txt` |
| SC-007 | final | `test-evidence/cache-counts.txt`; `test-evidence/cache-green.txt`; mutation drills `test-evidence/cache-mutations.txt` |
| SC-008 | final | `test-evidence/event-wait-green.txt`; mutation drills `test-evidence/event-wait-mutations.txt` |
| SC-009 | final | `test-evidence/inprocess-equivalence.txt`; `test-evidence/inprocess-conversion.md`; mutation drills `test-evidence/inprocess-mutations.txt`; guards `test-evidence/inprocess-guard-wp7.txt`, `test-evidence/inprocess-guard-wp8.txt` |
| SC-010 | supporting | `test-evidence/forbidden-shortcuts.txt` — dual-channel diff scan (text over added lines + base-vs-HEAD AST): zero new skip/xfail/retry/conditional forms, zero parametrize removals, no worker-resolution drift |
| SC-011 | supporting | `test-evidence/interface-evidence.txt` (`--help` lists `--full`, `--version` one line, undeclared option exits non-zero); `test-evidence/tier-contract-green.txt` (086 runner contract 40 cases + tier cases) |

## WP-9 task records

| Task | Record |
|------|--------|
| T003 | `notes/pre-change-measurements.md` (slot 1 of 2, full-suite wall + `--names-out`, implement-start id set, S-0.4/S-0.5 readings, P-3/P-4 censuses); names `baseline-failed.txt` (287 entries, sha256 `1887c9cf…99da44`) |
| T022 | `test-evidence/full-collection-diff.txt`; disposed `test-evidence/full-collection-disposed.txt` |
| T055 / T056 | `test-evidence/tier-measurements.txt` (scope disclosure; same-selection wall pair and ratio) |
| T057 | `test-evidence/forbidden-shortcuts.txt` |
| T058 | `test-evidence/interface-evidence.txt` |
| T059 | this index |
| T060 | `notes/quickstart-run.md` (S-1…S-13, with teardown) |

## Feature-level records

- Coverage baseline: `coverage-baseline.txt` (frozen 68-clause universe over the six contract
  files, produced by `account-clause-coverage.py --freeze`).
- Quickstart execution: `notes/quickstart-run.md` (S-1…S-13 with teardown).
- Slot 1 baseline names: `baseline-failed.txt` (287 pre-existing names; sha256 recorded in
  `notes/pre-change-measurements.md`); slot 2 closure comparison: `test-evidence/closure.txt`
  (pending-closure, T061).
- Mutation legs: `tier-mutations.txt`, `parallel-mutations.txt`, `cache-mutations.txt`,
  `event-wait-mutations.txt`, `inprocess-mutations.txt`.
- Contract-green records: `tier-contract-green.txt`, `parallel-consistency-contract.txt`,
  `cache-green.txt`, `event-wait-green.txt`, `inprocess-equivalence.txt`.

## Review-repair r1 records (2026-11-11)

| Record | What it carries |
|--------|-----------------|
| `verification.md` (spec dir) | the implement close-out carrier: SC-001…SC-011 status rows, smoke triple, `deferred_tasks=T061`, RS-004 joint acceptance, the copied closure verdict |
| `test-evidence/review-repair-r1-closure-verdict.txt` + `review-repair-r1-closure-payload.json` | both checker invocations and the full `block` record (pass 7 / partial 2 / total 9) |
| `test-evidence/verification-smoke-098.txt` | the feature smoke transcript (exit 0, `86 passed in 34.74s`) |
| `test-evidence/review-repair-r1-sc002-comm.txt` | SC-002 final-tree re-run, both `comm` directions empty |
| `test-evidence/review-repair-r1-sc005-walls.txt` | SC-005 rebuilt pre-change baseline → final tree pair (92.4 % ≤ 110 %) |
| `test-evidence/review-repair-r1-trigger-fix.txt` | the `test_trigger_engine.py` fixture-isolation root cause and repair (SC-002's P0) |
| `test-evidence/review-repair-r1-f6-receipt.txt` | the receipt skip-selector ordering fix with positive/negative drills |
| `notes/pre-change-measurements.md` § 7 | the rebuilt-baseline record (command, tree, walls, name disclosure, budget statement) |
| `notes/quickstart-run.md` § S-4 repair r1 | the final-tree bidirectional re-reading appended to S-4 |
