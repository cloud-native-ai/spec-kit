# Implement report — wp01-foundation (094-goal-team-parallel)

Package: `wp01-foundation`, rows T001–T015
Tree: `/storage/project/cloud-native-ai/spec-kit` (branch `master`, main tree — no worktree)
Base commit at dispatch: `124759e3`
Date: 2026-11-09
Write domain used: `scripts/python/goal-utils.py` (binding + scope + writability sections),
`tests/contract/test_binding_model.py`, `notes/`, `test-evidence/`. Nothing outside it was edited.

## Per-row closure

| Row | Status | Evidence |
|-----|--------|----------|
| T001 | closed | `test-evidence/wp01-T001-red-first-skeleton.txt`; artifact `notes/red-first-evidence.md` |
| T002 | closed | `test-evidence/wp01-T002-baseline.txt`, `implementation-baseline-names.txt`, `implementation-baseline-ids.txt`, `implementation-baseline-full.out`, `implementation-baseline-exit.txt`, `implementation-baseline-restore.txt` |
| T003 | closed | `test-evidence/T003-fixture-probe.txt` |
| T004 | closed | `notes/pre-change-measurements.md`; `test-evidence/wp01-T004-measurements.txt` |
| T005 | closed | `test-evidence/wp01-T005-binding-missing.txt`, `wp01-T005-green.txt`, `wp01-T005-red.txt`; engine section "binding record" |
| T006 | closed | `test-evidence/wp01-T006-owner-domain.txt` |
| T007 | closed | `test-evidence/wp01-T007-owner-id-shape.txt` |
| T008 | closed | `test-evidence/wp01-T008-origin-resolution.txt` |
| T009 | closed | `test-evidence/wp01-T009-bind-byte-rule.txt` |
| T010 | closed | `test-evidence/wp01-T010-hand-edited-binding.txt` |
| T011 | closed | `test-evidence/wp01-T011-terminal-rebind.txt` |
| T012 | closed | `test-evidence/wp01-T012-binding-read.txt` |
| T013 | closed | `test-evidence/wp01-T013-scope-values.txt`; retired-literal scan recorded in that file |
| T014 | closed | `test-evidence/wp01-T014-both-roots-auto.txt` |
| T015 | closed | `test-evidence/wp01-T015-cross-layer.txt`; engine `main()` cross-layer refusal |
| C-14 (writability) | closed | `test-evidence/wp01-T005b-writability.txt` (extra guard appended to the module for the writability clause T005's green set carries) |

## Test readings

- Red-first (T005 `[green:]` obligation), command `python3 -m pytest tests/contract/test_binding_model.py -q`:
  **12 failed, exit 1** — `test-evidence/wp01-T005-red.txt`, recorded in `notes/red-first-evidence.md`.
- Green, same command after implementation: **12 passed, exit 0** — `test-evidence/wp01-T005-green.txt`.
- Focused per-row guards: all exit 0 (see the table).
- Affected pre-existing goal/team suite (disclosure, not a gate): **21 failed / 267 passed** —
  `test-evidence/wp01-collateral.txt`. Of the 21: 17 are the 085 disposal-table scope/temp
  modules (expected rewrites, § Residual risks 2), 2 are in the 46-id plan baseline, 1 is the
  stale mirror projection, 1 is the pre-existing `test_goal_migration_path` staleness.
- `tests/contract/test_run_checks.py::test_c1_the_action_exists_and_the_roster_grew_by_exactly_one`
  now fails: it pins the action roster at exactly 11 (`sub.add_parser` count 11), and this
  package necessarily adds `bind` and `binding` (13). The module is not in the 085 disposal
  table and no package owns it — § Residual risks 3.
- `tests/contract/test_script_interface_contract.py` C-20/C-33/C-35 failed while
  `tests/contract/test_binding_model.py` was **untracked** (`candidate-not-collected`); the
  post-commit reading is recorded below.

## T002 baseline reading

`test-evidence/wp01-T002-baseline.txt`. The clean reading was captured against the HEAD
engine with this package's test module absent, so the comparison is against implement entry
rather than against a half-edited tree; the working tree was restored in the same command
(`implementation-baseline-restore.txt`, engine object = HEAD object `27adac3f`).

**Measured: 113 failing ids at implement entry, against the plan-recorded 46.**
`exit 1`, `113 failed, 8187 passed, 2 skipped in 679.29s`. Against a C-order-sorted copy of
`plan-baseline-names.txt` (the plan file itself fails `LC_ALL=C sort -c`), the diff is **69
new-not-in-plan** and **2 in-plan-not-now**. The 113 is the implement-entry state of the
HEAD engine; none of it is caused by wp01. The 69 cluster in the goal/summary/target
integration suites (68) plus tree-scanning contract tests — the upstream `.specify/goal/` →
`.specify/anchoring/` rename drift and the pre-existing `.specify/.tmp/sdd-loop`
worktrees/run scratch that execution lesson 2 says must be removed before a closure run.
The comparison surface is therefore stale for GATE-1; this is disclosed as an anomaly
(§ Residual risks 1), not repaired here (re-baselining is a driver/plan ruling).

## Commits

- `a8965b03` — `feat(094-wp01): binding model + scope engine + contract tests (T001–T015)`
  (parent `5278d4d1`; the branch advanced by one spine-note commit after this package was
  dispatched at `124759e3` — no conflicting paths). No push.
- `HEAD~` post-commit reading: `test-evidence/wp01-postcommit.txt` — binding model 12 passed;
  script-interface C-20 resolved once the module became tracked, C-33/C-35 remain red only on
  the pending mirror projection; the run-checks roster pin remains red as disclosed.

## Residual risks and disclosed boundaries

1. **The plan baseline (46 ids) is not the implement-entry reading (113 ids).** T002's clean
   run against the HEAD engine measured 113 failures with 69 names absent from
   `plan-baseline-names.txt` and 2 plan names no longer failing; the plan file also fails
   `LC_ALL=C sort -c`. GATE-1 as written will attribute ~69 pre-existing failures to this
   stage. The fix is a driver/plan ruling (clean `.specify/.tmp/sdd-loop` per execution
   lesson 2, re-freeze the baseline, or adjudicate per name) — this package discloses the
   reading and does not re-baseline.
2. **085 disposal modules are now red and no package in the partition owns their rewrite.**
   T013's value-set change (by design) turns `tests/contract/test_scope_resolution.py`,
   `tests/unit/test_goal_scope_engine.py`, `tests/contract/test_temp_goal_contract.py` and
   `tests/contract/test_temp_team_schema.py` red. The 085 disposal table marks these `rewrite`,
   but no row in the Package Map declares them in a write domain. Closure (GATE-1) needs an
   owner for these rewrites before the closure suite.
3. **The action-roster pin in `tests/contract/test_run_checks.py` moved from 11 to 13 and is
   unowned.** Its C-22 clause asserts exactly 11 `sub.add_parser` calls; `bind` and `binding`
   make 13. The module is not in the 085 disposal table and no package owns it; the pinned
   literal needs an explicit ruling (`13`) rather than a silent edit.
4. **Mirror projection is pending the driver's integration step.** `sync-mirrors.py --check`
   reports exactly one drift: `.specify/scripts/python/goal-utils.py` (the projection of this
   package's edit). The reading is `test-evidence/wp01-mirror-check.txt`; the fix is the
   driver's `sync-mirrors.py --write`, not a hand edit.
5. **C-19 (`reopen`) has a contract clause and a green-set attribution but no implementation
   row.** T005's clause tag covers C-1…C-30, yet no task row asks for a `reopen` action and the
   engine's existing transition table still refuses terminal → active. This package did not
   invent the action; it is surfaced as a tasks-file gap for the driver.
6. **Pre-existing failures unrelated to this package.**
   `tests/integration/test_goal_migration_path.py::test_migration_preserves_the_resolved_objective`
   reads `.specify/goal/<slug>/summary/...` while the generator writes `.specify/anchoring/...`
   at HEAD (verified by reading `skills/internal/create-team/scripts/build-summary-input.py`
   at HEAD; the test predates the 092 rename). The two `test_goal_migration.py` failures are in
   the plan baseline (leftover `.specify/.tmp/sdd-loop` worktrees, execution lesson 2).
7. **Binding-preservation repair (C-20) touched five render call sites.** To keep the binding
   block byte-identical across `status` / `objective` / `criteria` / `targets` writes, `_render`
   gained a `binding_lines` argument and `parse_goal` now carries `binding_block`. This is the
   clause C-20 requires of the T005 module; it changes no rendered byte for definitions without
   a binding.
8. **Hand-edit detection boundary.** `binding-hand-edited` is decidable for any block that
   differs from the engine's canonical rendering (order, indentation, quoting, extra keys,
   duplicates). A hand edit that reproduces the canonical text byte-for-byte is
   indistinguishable from an engine write; this limit is stated in the code and in this report
   rather than claimed away.
9. **T015's row carries a stray evidence pointer** to `test-evidence/validate-tasks.txt` (a
   tasks-stage artifact). This package recorded T015's own reading instead; the stray pointer
   names no artifact this stage produces.
