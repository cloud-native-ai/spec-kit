# Feature Reference — Feature 086

## 1. Binding

| Field | Value |
|-------|-------|
| Feature ID | 086 |
| Feature name | Efficient Test Execution (Concurrent by Default) |
| Requirement branch | `086-efficient-test-execution` |
| Requirements | [`requirements.md`](requirements.md) |
| Feature detail | `.specify/features/086-efficient-test-execution.md` |
| Feature index row | `.specify/features.md` (Draft → Planned, this stage) |
| Flow class | execution |
| FR / SC | 33 / 12 |

## 2. Delivery Surface

Every row below is a path this plan changes or creates, mapped to the requirement rows it serves.

| # | Surface | Change | FR |
|---|---------|--------|-----|
| 1 | `scripts/bash/run-tests.sh` | Parallel default, mode line, `--serial`, `--workers`/`SPECKIT_TEST_WORKERS`, no-duplicate-`-n`, nested auto-serial, xdist-missing fallback, two-pass serial exceptions, combined list + exit code | FR-001…FR-009 |
| 2 | `.specify/scripts/bash/run-tests.sh` | Byte-identical mirror, written by `sync-mirrors.py` | FR-009 |
| 3 | `shared/guidelines/test-execution-efficiency.md` (new) | The rule's only definition point (six sections) | FR-018 |
| 4 | `.specify/shared/guidelines/test-execution-efficiency.md` | Mirror | FR-018 |
| 5 | `templates/constitution-template.md` | `### XIX. Efficient Test Execution (Concurrent by Default)` | FR-019 |
| 6 | `.specify/constitution.md` | `### XX.` + version 1.17.0 + Sync Impact Report | FR-019 |
| 7 | `templates/instructions-template.md` | `## Test Execution Efficiency (测试执行效率)` after `## Single-Run Evidence Discipline` | FR-020 |
| 8 | `.specify/instructions.md` | Same section, produced by the generator | FR-020 |
| 9 | `skills/internal/manage-constitution/SKILL.md` + mirror | MUST-include entry 12 | FR-021 |
| 10 | `pyproject.toml` | Dev extra (`pytest`, `pytest-xdist` with `python_version >= "3.9"`), `serial` marker registration | FR-015, FR-016, FR-011 |
| 11 | `skills/external/sdd-loop-driver/scripts/audit-test-budget.py` + mirror | `VALUE_FLAGS` + 4 tokens | FR-024…FR-026 |
| 12 | `tests/contract/test_sdd_loop_driver_skill.py` | `serial` marker on `test_c22_watch_target_hook_selftest` | FR-012 |
| 13 | `tests/contract/test_run_tests_runner_contract.py` (new) | Runner contract cases + mutation legs | FR-001…FR-011 |
| 14 | `tests/unit/test_audit_test_budget.py` | Parallel full-run classification rows | FR-024…FR-026 |
| 15 | `tests/contract/test_test_execution_efficiency.py` (new) | Both-sides principle guard with a red leg per surface | FR-019…FR-023 |
| 16 | `tests/contract/test_constitution_double_landing.py`, `test_fast_fail_discipline.py`, `test_instructions_section_propagation.py`, `test_instructions_size_budget.py` | Count/budget pins raised in the same change | FR-022 |
| 17 | `tests/contract/test_temp_goal_contract.py`, `test_temp_team_schema.py`, `test_checkpoint_protocol.py`, `tests/integration/test_temp_team_worktree_queue.py`, `tests/integration/test_checkpoint_rollback.py` | Re-run as the 085 preservation evidence (no edit planned; any needed change is disclosed) | FR-027, FR-029 |
| 18 | `docs/contribute/dev-setup.md`, `CONTRIBUTING.md` | How to run the suite under the new default | FR-032 |
| 19 | `CHANGELOG.md` | Entry | FR-031 |
| 20 | `.specify/features.md`, `.specify/features/086-efficient-test-execution.md` | Registry + detail; `Planned` this stage | FR-031 |
| 21 | `test-evidence/` | Phase 0 baseline, plan gates, dogfood record, closure name diff | FR-014, FR-028, FR-033 |

No new command, skill entry template, runtime service, schedule or store is created (FR-017).

## 3. Rulings Disclosed in This Plan

1. The watcher test's identifier is `test_c22_watch_target_hook_selftest`, not the brief's `test_c24` label
   (`research.md` R-9).
2. The gate-scan criterion is "no increase over the pre-change value (27)", not equality with the stale
   frozen baseline (23); two guard tests assert the equality and are already red on the serial baseline
   (`research.md` R-8, `plan.md` EP-008).
3. The inherited-blocker carrier names an existing 085 test file rather than a new preservation test, so the
   carrier resolves without creating a test purely to satisfy the table.
4. The 085 carrier downgrade (host-native stage agents) is recorded as an observation, not repaired
   (`plan.md` § 085 Carrier Observation, contract C-051).
5. Execution premises are all `verified`; the eight facts that could have been assumed were measured
   (`plan.md` § Disclosed Deviations 2).
6. Same-author scoring was performed as a direct bounded read (subagent dispatch unavailable in this
   carrier) and is marked as such wherever it is asserted (`research.md` R-10).
7. `## Document Structure` is deliberately absent: this is an execution-class line and the plan template's
   class condition forbids adding that mandatory section to it.
