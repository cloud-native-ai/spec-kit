# 098 test-evidence index

Owner of the mapping: `tasks.md` T059. Every success criterion SC-001…SC-011 links to the
evidence path(s) that carry its reading; the feature's coverage baseline and the closure
records are included. Paths are relative to `.specify/specs/098-suite-speed-optimizations/`.
Statuses: `pass` = the reading exists and supports the criterion; `supporting` = the
criterion's declared path; `pending-closure` = a criterion whose reading is a later closure-stage
leg (none remains after T061 executed, 2026-11-11).

| SC | Path | Evidence |
|----|------|----------|
| SC-001 | final | `test-evidence/full-collection-diff.txt` — removed 0 / added 46 (the five new contract files); baseline id set in `notes/pre-change-measurements.md` (`implement-start-full-ids` block, 8543 ids from base `b3da3a26d`); disposed list `test-evidence/full-collection-disposed.txt` |
| SC-002 | final | `test-evidence/parallel-consistency-contract.txt` (commands, exits, durations, both empty `comm` directions, non-parallel-safe drill); name lists `test-evidence/parallel-contract-parallel-names.txt`, `test-evidence/parallel-contract-serial-names.txt`; mutation drills `test-evidence/parallel-mutations.txt`; final-tree quickstart re-check `notes/quickstart-run.md` §S-4 with lists `test-evidence/quickstart-s4-parallel-names.txt`, `test-evidence/quickstart-s4-serial-names.txt`; **review-repair r1**: `test-evidence/review-repair-r1-sc002-comm.txt` — both `comm` directions empty (137/137 names), lists `test-evidence/review-repair-s4-parallel-names.txt` / `-serial-names.txt`, logs `test-evidence/run-logs/review-repair-s4-{parallel,serial}.log.gz`, root-cause record `test-evidence/review-repair-r1-trigger-fix.txt` |
| SC-003 | final | `test-evidence/closure.txt` — **executed (T061, 2026-11-11)**: full-tier same-tree comparison, parallel 223 names / serial 223 names, `comm -13` = 0 and `comm -23` = 0 (lists byte-identical); names `final-failed.txt` / `test-evidence/closure-serial-failed.txt`; root-cause record `test-evidence/closure-isolation-fix.txt` (the attempt-1 five-name parallel-only isolation defect); status `pass` |
| SC-004 | final | `test-evidence/tier-measurements.txt` — default-tier parallel vs same-selection serial walls (73.42 s vs 692.15 s, ratio 10.6 % ≤ 50 %), selection-equality collection readings; complete outputs `test-evidence/run-logs/default-parallel.log.gz`, `test-evidence/run-logs/default-serial.log.gz`; scope-disclosure readings |
| SC-005 | final | `test-evidence/closure.txt` — **executed (T061, slot 2 of 2, 2026-11-11)**: repaired-tree closure wall 70.62 s vs rebuilt pre-change baseline 76.52 s = 92.3 % ≤ 110 %; both slots full-tier `--names-out`; `comm -13 baseline-failed.txt → final-failed.txt` = 0 new names (64 removals). The baseline referent is the **rebuilt pre-change** wall (76.52 s) — the earlier slot-1 wall 70.99 s is superseded (`notes/pre-change-measurements.md` § 7). Names/lists: `final-failed.txt`, `test-evidence/closure-serial-failed.txt`; first-attempt lists `test-evidence/closure-prerepair-{parallel,serial}-failed.txt`; logs `test-evidence/run-logs/closure-{parallel,serial}-full.log.gz` + `closure-prerepair-{parallel,serial}.log.gz`; status `pass` |
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
  `notes/pre-change-measurements.md`); slot 2 closure reading: `test-evidence/closure.txt`
  (executed 2026-11-11 — parallel 223 / serial 223 names, both `comm` directions empty).
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

## Review-repair r2 records (2026-11-11, closure stage)

| Record | What it carries |
|--------|-----------------|
| `test-evidence/closure.txt` | T061: slot-2 full parallel run (223 names, 70.62 s), same-tree `--full --serial` run (223 names, 708.13 s), both `comm` directions empty, wall ratio 92.3 %, the slot-1 name comparison, and the attempt-1 diagnostic |
| `final-failed.txt` | slot-2 parallel `--names-out` list, 223 entries (sha256 `1f85ac90…`) |
| `test-evidence/closure-serial-failed.txt` | same-tree serial validation list, 223 entries (byte-identical to the parallel list) |
| `test-evidence/closure-prerepair-{parallel,serial}-failed.txt` | attempt-1 diagnostic lists (254 / 249 names; `comm -23` = 5) |
| `test-evidence/closure-isolation-fix.txt` | root cause (engine C-7 self-location resolves to the parent repo from this nested worktree), the two helper edits, and the targeted green runs |
| `test-evidence/review-repair-r2-closure-verdict.txt` + `review-repair-r2-closure-payload.json` | the `accept` verdict (final path 9/9; tasks 61 closed / 0 deferred; smoke valid) |
| `test-evidence/review-repair-dispositions-r2-2026-11-11.md` | the round's dispositions |
