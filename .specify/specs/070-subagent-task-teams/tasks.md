# Tasks: Task Decomposition & Team Coordination for Subagent-Driven SDD — 070

**Requirement ID**: 070
**Requirement Key**: `070-subagent-task-teams`
**Branch**: `070-subagent-task-teams`
**Related Feature**: Feature 070 — 驱动子代理的任务拆解与配合机制（Task Decomposition & Team Coordination for Subagent-Driven SDD）, status Planned
**Input**: Design documents from `.specify/specs/070-subagent-task-teams/`
**Prerequisites**: plan.md (required), requirements.md (required; 30 FR / 8 SC), research.md (R1–R20), data-model.md (E1–E13), contracts/ (7 files, 110 domain-prefixed clauses), quickstart.md (Scenarios A–G), feature-ref.md.

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating: pure functions and utilities MUST have unit tests and critical flows MUST have automated regression coverage; this feature ships two executable stdlib scripts plus prompt-owner documents, so the template-only exception does not apply. Red-first evidence is mandatory for new behavior; the non-regression and mutation rows are regression nets and use the create-tasks migration/regression exception with explicit `[blockedBy:]`.)

**Tests**: Every new-behavior test row is red-first and records its failing command, real output, and exit code in `notes/red-first-evidence.md`. The non-regression row (T033) and the mutation-drill row (T036) guard or exercise behavior that already exists or is fully implemented, so they land with explicit `[blockedBy:]` rather than a red-first claim. The two full-suite slots are the implement baseline (T002) and closure (T039); no other row runs a full suite. Verifier-selected tests use the existing `targeted-set-v1` procedure.

**Organization**: Tasks are grouped by the five user stories in requirements.md. US1, US2, and US3 are all P1 and together form the MVP: decomposition without safe dispatch and independent verification is not an independently valuable increment. US4 (team preset/adapter) and US5 (observability/metrics) are P2 and can follow the MVP. Setup and Foundational phases contain no story label; Polish contains none.

## Definition of Done (DoD)

- DoD-1: Every task row is `[X]`, or `[~]` with its reason recorded in `.specify/specs/070-subagent-task-teams/verification.md` under `deferred_tasks=`.
- DoD-2: `skills/external/sdd-loop-driver/scripts/wp-gate.py` and `wp-report.py` exist, are stdlib-only, and pass their unit and contract suites.
- DoD-3: `skills/external/sdd-loop-driver/references/decomposition-model.md`, `templates/stage-team-preset.md`, the new `SKILL.md` H2, and the `docs/reference/skills/sdd-loop-driver.md` section land as additive changes; no predecessor rule is redefined.
- DoD-4: Every FR-001…FR-030 maps to at least one task row in § Requirement Coverage Map, and every SC-001…SC-008 has a status, command, output, and evidence pointer in `verification.md`; SC-001 and SC-002 close only on met evidence or a recorded user waiver naming the criterion (FR-023).
- DoD-5: All 110 domain-prefixed contract clauses are covered by at least one contract-test task in § Clause Coverage Model (WG-18 is pinned at both the CLI-envelope and the fallback/preflight layers), and T039 proves every clause id appears in one of the four contract test files.
- DoD-6: Red-first evidence exists for every new-behavior test row; the mutation drills prove each guard turns at least one test red; a green check that would not go red is not cited.
- DoD-7: The closure full-suite slot reports zero NEW name-level failures against `baseline-failed.txt`, and the mirror check reports zero NEW drift against the T001 clean 28-file baseline.
- DoD-8: No plan-owned artifact is rewritten by implement without a front-loaded `PLAN-EDIT:` declaration; no push, force merge, or confirmation-gate bypass occurs.

**DoD Status**: pending

## Completion Gate

- GATE-1: Task file structure is valid — check: `python3 scripts/python/validate-tasks.py .specify/specs/070-subagent-task-teams/tasks.md` exits 0.
- GATE-2: Cross-artifact consistency holds — check: `python3 /home/agent/sdd-070/tools/pre-analyze-check.py --spec-dir .specify/specs/070-subagent-task-teams --stage tasks --repo .` reports `decision=pass` with `errors=0` and `waived=0`; no waiver is used or needed (the former per-package eight-task-bound count-claim waivers are obsolete after the wording repair recorded in § Validator Status (post-repair)).
- GATE-3: The decomposition size gate passes — check: `python3 skills/external/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/070-subagent-task-teams/requirements.md --tasks .specify/specs/070-subagent-task-teams/tasks.md` reports `proceed` with `task_count=39`, at or below the 40-row ceiling.
- GATE-4: All new test suites are green — check: `python3 -m pytest -q tests/unit/test_wp_gate.py tests/unit/test_wp_report.py tests/contract/test_sdd_loop_driver_wp_model.py tests/contract/test_sdd_loop_driver_wp_gate.py tests/contract/test_sdd_loop_driver_wp_coordination.py tests/contract/test_sdd_loop_driver_wp_preset.py tests/contract/test_non_regression_070.py tests/contract/test_wp_mutation_drills.py tests/integration/test_wp_coordination_dry_runs.py`.
- GATE-5: The closure full suite has zero NEW name-level failures — check: `bash scripts/bash/run-tests.sh --names-out .specify/specs/070-subagent-task-teams/final-failed.txt` followed by `comm -13 .specify/specs/070-subagent-task-teams/baseline-failed.txt .specify/specs/070-subagent-task-teams/final-failed.txt` returns empty.
- GATE-6: The mirror pair is clean — check: `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` reports `ok` and every source/mirror pair named in plan.md § Mirror Obligations is byte-identical.
- GATE-7: Clause coverage is complete — check: every id in `notes/contract-clause-inventory.txt` appears in one of `tests/contract/test_sdd_loop_driver_wp_model.py`, `test_sdd_loop_driver_wp_gate.py`, `test_sdd_loop_driver_wp_coordination.py`, or `test_sdd_loop_driver_wp_preset.py` (T039 command).
- GATE-8: The SC matrix is complete — check: `grep -cE '^- \*\*SC-00[1-8]\*\*' .specify/specs/070-subagent-task-teams/verification.md` returns 8, and SC-001/SC-002 each carry met evidence or a recorded user waiver naming the criterion; `not_evaluated` without a waiver blocks closure.
- GATE-9: No unfinished rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/070-subagent-task-teams/tasks.md` returns 0.

## Environment Prerequisites

- Python and pytest: **available** — probe: `python3 --version` → `Python 3.11.11`; `python3 -m pytest --version` → `pytest 8.4.2` @ 2026-10-25; affected: every test and validator row.
- External environment (container runtime, image registry, live cluster, network, special hardware): **none** — all work is local files, local git, and local pytest; affected: none.
- Mirror pair `skills/external/sdd-loop-driver/` → `.specify/skills/sdd-loop-driver/`: **clean baseline** — probe: `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` → `ok skills/external/ == .specify/skills/ (28 files)`, rc 0 @ 2026-10-25; affected: T037, T039.
- Clause-form probe: `python3 .specify/scripts/python/clause_extract.py .specify/specs/070-subagent-task-teams/contracts/*.md` reports `form=md-none` and 0 clauses for every contract file because the extractor recognizes only the closed `C-\d+` form; Feature 070's contracts use domain-prefixed ids. The limitation and its coverage mitigation are owned by § Clause Coverage Model; affected: T003, T009, T039.

## Test Budget (E2 / E3 / closure)

- **E2 baseline slot (implement start, exactly once)**: T002 runs the canonical full suite before any implementation edit and records the name list at `baseline-failed.txt`; the comparison form is owned by `/speckit.implement` step 6's `**Test runs**` bullet and is not restated here.
- **E3 stage-status rows (targeted evidence)**: T008, T013, T019, T023, T026, and T030 append `targeted-set-v1` stage-status rows to `test-evidence/implement-stage-status.jsonl`. The tasks stage itself is docs-only and records one `status=not-run-docs-only` row in `test-evidence/tasks.jsonl`.
- **Closure slot (after review)**: T039 runs the full suite once more, writes `final-failed.txt`, and compares name-level failures against the E2 baseline. No other row runs a full suite, and verifiers may run only a package's declared targeted tests.
- **Frozen plan baseline ≠ E2**: `test-evidence/targeted-baseline-plan.txt` (65 passed, 2026-10-24) is a plan-stage targeted baseline for the existing driver suite; it is not the implement E2 baseline.

## Mirror Obligations

The authoritative source/mirror list is plan.md § Mirror Obligations, the sole owner; feature-ref.md §7 is a pointer to it. This file only lands its task. The five changed driver files are `SKILL.md`, `references/decomposition-model.md`, `templates/stage-team-preset.md`, `scripts/wp-gate.py`, and `scripts/wp-report.py`. T037 runs the existing generator in write mode and then checks for zero NEW drift against the T001 clean 28-file baseline; `.specify/skills/sdd-loop-driver/` is generated and MUST NOT be hand-edited. `docs/` and `tests/` have no mirror.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel with the other `[P]` rows in the same phase (different write targets, no unfinished dependency).
- **[Story]**: `[US1]`…`[US5]`; required on every row inside a User Story phase and forbidden in Setup, Foundational, and Polish.
- **[blockedBy: T001,T002]**: Explicit dependency edge; the row MUST NOT start until every listed task is `[X]`. Omitted when only phase order applies.
- **[green: <contract>#<clause>]**: Intentionally not used in this file. The repository extractor recognizes only the closed `C-\d+` clause form, while Feature 070's contracts use domain-prefixed ids and are classified `md-none`; adding a parallel `C-` numbering would be a substantive plan-owned contract change. Coverage is instead fixed by § Clause Coverage Model and mechanically checked by T039. This is a disclosed tooling limitation, not a silent omission.

## Clause Coverage Model (contract test task per clause)

Every clause in `contracts/` is covered by at least one contract-test task. The contract file owns the clause text; this table only maps it to the test task that pins it and the row that turns it green. WG-18 is pinned at both the CLI-envelope layer (T005) and the preflight/fallback layer (T016), with T035 as its green point. The 110 clause ids are frozen in `notes/contract-clause-inventory.txt` by T003.

| Contract file | Clauses | Count | Contract test task(s) | Green-point row |
|---|---|---|---|---|
| `contracts/work-package-model.md` | WP-01…WP-18 | 18 | T009 | T012 |
| `contracts/wp-gate.md` | WG-01…WG-05 | 5 | T005 | T007 |
| `contracts/wp-gate.md` | WG-06…WG-13 | 8 | T010 | T011 |
| `contracts/wp-gate.md` | WG-14…WG-17 | 4 | T016 | T017 |
| `contracts/wp-gate.md` | WG-18 | 1 | T005, T016 | T035 |
| `contracts/scheduler-and-dispatch.md` | SD-01…SD-16 | 16 | T014 | T018 |
| `contracts/verification-and-integration.md` | VI-01…VI-14 | 14 | T020 | T022 |
| `contracts/stage-team-adapter.md` | ST-01…ST-12 | 12 | T024 | T025 |
| `contracts/observability-and-retry.md` | OR-01, OR-02 | 2 | T009 | T012 |
| `contracts/observability-and-retry.md` | OR-03…OR-13 | 11 | T009 | T028 |
| `contracts/observability-and-retry.md` | OR-14…OR-16 | 3 | T009 | T029 |
| `contracts/fallback-and-nonregression.md` | FN-01…FN-16 | 16 | T034 | T035 |

**Partition check**: 18 + 5 + 8 + 4 + 1 + 16 + 14 + 12 + 2 + 11 + 3 + 16 = 110; each id appears in exactly one green-point row, and the green-point row order is monotonic within each contract file.

## Measured Premises (re-measured at tasks generation, 2026-10-25)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| Python / pytest | `python3 --version`; `python3 -m pytest --version` | `Python 3.11.11`; `pytest 8.4.2` |
| FR / SC definition rows | `grep -cE '^\- \*\*FR-[0-9]+\*\*' .specify/specs/070-subagent-task-teams/requirements.md`; the same with `SC-` | 30 / 8 |
| Clause inventory | `grep -hE '^- \*\*(WP\|WG\|SD\|VI\|ST\|OR\|FN)-[0-9]{2}\b' .specify/specs/070-subagent-task-teams/contracts/*.md \| wc -l` | 110 (18 + 18 + 16 + 14 + 12 + 16 + 16) |
| Clause-form classification | `python3 .specify/scripts/python/clause_extract.py .specify/specs/070-subagent-task-teams/contracts/*.md` | `form=md-none`, 0 clauses per file (see § Clause Coverage Model) |
| Mirror baseline | `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | `ok skills/external/ == .specify/skills/ (28 files)`, rc 0 |
| Targeted driver baseline | `python3 -m pytest -q tests/unit/test_decomposition_check.py tests/unit/test_pre_analyze_check.py tests/unit/test_overlap_check.py tests/contract/test_sdd_loop_driver_gates.py tests/contract/test_sdd_loop_driver_skill.py` | `65 passed in 18.03s`, rc 0 |
| Existing driver contract test surface | `ls tests/contract/test_sdd_loop_driver_*.py` | `test_sdd_loop_driver_cli_profiles.py`, `test_sdd_loop_driver_efficiency.py`, `test_sdd_loop_driver_gates.py`, `test_sdd_loop_driver_skill.py` |
| Pinned H2 sections | count of entries in `PINNED_H2_SECTIONS` inside `tests/contract/test_sdd_loop_driver_skill.py` | 13 before T031; 14 after the 070 section lands |
| Plan task budget | plan.md § Task Budget | 35 planned steps against the 40-step ceiling; this file defines 39 task rows, below the ceiling |
| Git snapshot | `git rev-parse HEAD`; `git status --short` | HEAD `dd7a71fedd582e2ce867fef94c22e0233b137632`; clean working tree |

## Validator Status (post-repair)

The tasks-stage `pre-analyze-check.py` run is waiver-free. The three earlier `count-claim` findings on `requirements.md` and `data-model.md` were per-package dispatch caps misread as total-task claims; they were reworded at `tasks-repair` (commit `9b964d5c`), and the current raw run returns `decision=pass`, `errors=0`, `waived=0` without any `--waive` flag. The remaining advisories are `missing-path` for planned new scripts, tests, reference, preset, and evidence files; they disappear as implement creates those paths.

## Requirement Coverage Map

Every FR-001…FR-030 and SC-001…SC-008 is mapped below. A row may cover several requirements; no requirement is left without a task.

| Requirement | Tasks |
|-------------|-------|
| FR-001 | T009, T012 |
| FR-002 | T012 |
| FR-003 | T011, T012, T022 |
| FR-004 | T012 |
| FR-005 | T012, T035 |
| FR-006 | T025 |
| FR-007 | T025 |
| FR-008 | T025 |
| FR-009 | T017, T035 |
| FR-010 | T018, T032 |
| FR-011 | T018 |
| FR-012 | T018, T022 |
| FR-013 | T016, T017, T018 |
| FR-014 | T022 |
| FR-015 | T018, T032 |
| FR-016 | T020, T022 |
| FR-017 | T022 |
| FR-018 | T022 |
| FR-019 | T033, T035 |
| FR-020 | T012, T028, T029 |
| FR-021 | T028, T029 |
| FR-022 | T028, T029 |
| FR-023 | T028, T029, T038 |
| FR-024 | T032, T035 |
| FR-025 | T033, T035 |
| FR-026 | T035 |
| FR-027 | T037, T039 |
| FR-028 | T005, T009, T014, T020, T024, T027, T034 |
| FR-029 | T015, T021, T033, T036 |
| FR-030 | T008, T013, T019, T023, T026, T030, T038, T039 |
| SC-001 | T028, T029, T038 |
| SC-002 | T028, T038 |
| SC-003 | T033, T039 |
| SC-004 | T017, T021, T022, T039 |
| SC-005 | T012, T035, T039 |
| SC-006 | T028, T038 |
| SC-007 | T027, T030, T038 |
| SC-008 | T015, T021, T036, T039 |

## Test Deliverable Map

Every plan-named test file or fixture has a creating task, an implementation dependency, and a final regression edge. Test → implement → regression is therefore explicit, not implied by phase order.

| Test file or fixture | Creating task | Implementation dependency | Final regression |
|----------------------|---------------|---------------------------|------------------|
| `tests/fixtures/wp_fixtures.py` | T004 | consumed by T009, T015, T027 | T039 |
| `tests/fixtures/wp_driver_sim.py` | T004 (stubs), T018/T022/T035 (algorithm) | T018, T022, T035 | T039 |
| `tests/unit/test_wp_gate.py` | T006 | T007, T011, T017 | T039 |
| `tests/unit/test_wp_report.py` | T027 | T028 | T039 |
| `tests/contract/test_sdd_loop_driver_wp_model.py` | T009 | T011, T012, T028, T029 | T039 |
| `tests/contract/test_sdd_loop_driver_wp_gate.py` | T005 | T007, T011, T017, T035 | T039 |
| `tests/contract/test_sdd_loop_driver_wp_coordination.py` | T014 | T018, T022, T035 | T039 |
| `tests/contract/test_sdd_loop_driver_wp_preset.py` | T024 | T025 | T039 |
| `tests/contract/test_non_regression_070.py` | T033 | T032, T035 (pins current text) | T039 |
| `tests/contract/test_wp_mutation_drills.py` | T036 | T011, T017, T022, T028, T035 | T039 |
| `tests/contract/test_sdd_loop_driver_skill.py` | T031 (pin update) | T032 | T039 |
| `tests/integration/test_wp_coordination_dry_runs.py` | T015 | T018, T022, T035 | T039 |

**Task Distribution**: Setup 4 · Foundational 4 · US1 5 · US2 6 · US3 4 · US4 3 · US5 4 · Polish 9 · total 39 task rows.

## Feature Registry Review

The task breakdown introduces no new Feature, merge, or split: the 39 task rows stay inside Feature 070 and below the 40-row ceiling. `.specify/memory/features.md` row 070 remains **Planned**, and `.specify/memory/features/070.md` is unchanged at the tasks stage; the move to Implemented belongs to `/speckit.implement`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Freeze the pre-change baselines and create the shared test fixtures so every later "relative to baseline" or "red-first" claim has a dated control.

- [x] T001 Create `.specify/specs/070-subagent-task-teams/notes/` and capture the pre-change measurements in `notes/pre-change-measurements.md`: Python and pytest versions, `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` (28-file clean baseline, rc 0), the targeted driver baseline command and result, `git rev-parse HEAD`, `git status --short`, and the clause-form probe result. Test anchor: this dated note is consumed by T037 and T039; evidence: `notes/pre-change-measurements.md`.
- [x] T002 [P] Capture the implement-start full-suite baseline exactly once with `bash scripts/bash/run-tests.sh --names-out .specify/specs/070-subagent-task-teams/baseline-failed.txt`, record the `slot=baseline` row in the line state spine's test-budget ledger, and keep the name list at `baseline-failed.txt`; do not edit T001's note. Test anchor: the baseline name list and the spine row; evidence: `baseline-failed.txt`.
- [x] T003 [P] Freeze the domain-prefixed contract-clause inventory to `notes/contract-clause-inventory.txt` with `grep -hE '^- \*\*(WP|WG|SD|VI|ST|OR|FN)-[0-9]{2}\b' .specify/specs/070-subagent-task-teams/contracts/*.md | sort`, assert 110 rows and per-file counts 18/18/16/14/12/16/16, and state the disclosed clause-form limitation in the file header. Test anchor: the inventory is consumed by T039; evidence: `notes/contract-clause-inventory.txt`.
- [x] T004 [P] Create `tests/fixtures/wp_fixtures.py` with builders for WP plans, `wp-plan`/`wp-ledger` spine fences, 064-style ownership manifests, ledger event sequences, and attempt-scoped evidence paths, and `tests/fixtures/wp_driver_sim.py` with deterministic fixture data plus explicit `NotImplementedError` stubs for the scheduler, verifier, and integrator steps; both are test-only and never write the repository. Test anchor: `python3 -m py_compile tests/fixtures/wp_fixtures.py tests/fixtures/wp_driver_sim.py`; evidence: `tests/fixtures/wp_fixtures.py` and `tests/fixtures/wp_driver_sim.py`.

**Checkpoint**: The E2 baseline, mirror baseline, clause inventory, and fixture harness are in place; every later comparison has a dated control.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the gate script's shared core — CLI, spine reader, schema validators, canonical hash, JSON envelope, and exit codes — before any user-story behavior is built on it.

- [x] T005 [P] Write the red-first contract tests to `tests/contract/test_sdd_loop_driver_wp_gate.py` for WG-01…WG-05: script path and stdlib-only guard, CLI grammar and defaults (including `--stage-attempt`), `--plan-json` precedence over `--spine`, the preflight manifest requirement, the WG-04 JSON envelope, exit 0/1/2, stable finding order, and the never-writes-the-spine guarantee; record the failing command, real output, and rc in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`.
- [x] T006 Write the red-first unit tests to `tests/unit/test_wp_gate.py` for the foundational gate core: spine fence reading (`wp-plan`, amendments, `wp-ledger`), required-field `schema-missing`, schema-before-graph ordering, canonical JSON SHA-256 `plan_hash` with excluded keys and timestamps, and exit-2 input handling; record the failing run in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`.
- [x] T007 Implement `skills/external/sdd-loop-driver/scripts/wp-gate.py` foundational layer: argparse CLI per WG-02, input precedence per WG-03, spine/plan reader, shared required-field and schema validators, canonical plan hash per WG-12, WG-04 JSON output, WG-05 exit codes, and deterministic finding order; stdlib only, Python 3.8+, never writes the spine or plan. Test anchor: `tests/contract/test_sdd_loop_driver_wp_gate.py` and `tests/unit/test_wp_gate.py`; evidence: the green run recorded in `notes/red-first-evidence.md`. [blockedBy: T005,T006]
- [x] T008 Verify the Foundational gate: run `python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_gate.py tests/unit/test_wp_gate.py`, record command/output/rc and the red-to-green transition in `notes/red-first-evidence.md`, and append a targeted-set-v1 stage-status row to `test-evidence/implement-stage-status.jsonl` with the selection basis naming the gate-core files. Test anchor: both gate test files; evidence: `notes/red-first-evidence.md` and `test-evidence/implement-stage-status.jsonl`. [blockedBy: T007]

**Checkpoint**: The gate CLI, spine reader, schema validators, canonical hash, JSON envelope, and exit-code taxonomy are green; US1 can now build plan-check behavior on them.

---

## Phase 3: User Story 1 - Decompose a stage into bounded, gated work packages (Priority: P1) 🎯 MVP

**Goal**: Derive a bounded, replayable WP plan from the stage's own artifacts, validate it with the deterministic gate, and represent the single-package decision when decomposition is not beneficial or is disabled.

**Independent Test**: Run the decomposition on a fixture stage whose artifacts imply several packages and inspect the plan plus gate verdict; inject a cycle, an unowned required output, and an overlapping write pair and confirm each is rejected; disable decomposition and confirm one package with the same acceptance evidence.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [x] T009 [P] [US1] Write the red-first contract tests to `tests/contract/test_sdd_loop_driver_wp_model.py` for WP-01…WP-18 and OR-01…OR-16: WP required fields, kind/territory invariants, stable ids and sentinels, deterministic layers, plan fence, canonical hash, amendments and split retries, ledger fence and event set, attempt-scoped evidence paths, the 067 extension, single-package representation, no second ledger, replayability, timestamp units, spine write authority, attempt identity, stage-close fields, and ledger field sets; record the failing run in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T004]
- [x] T010 [US1] Extend `tests/unit/test_wp_gate.py` with red-first `--check plan` cases: duplicate/dangling/cycle, orphan and duplicate output, boundedness (eight-task and 40-clause caps), kind mismatch, pattern compatibility, plan-hash mismatch, and benefit determination returning `single-package` with a `not-beneficial` advisory; record the failing run in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T006]

### Implementation for User Story 1

- [x] T011 [US1] Implement `wp-gate.py --check plan` for WG-06…WG-13, including `dispatch_layers` and `integration_order` in the JSON envelope, and run the US1 gate tests to green; record command, output, and rc in `notes/red-first-evidence.md`. Test anchor: `tests/contract/test_sdd_loop_driver_wp_gate.py` and `tests/unit/test_wp_gate.py`; evidence: the green run in `notes/red-first-evidence.md`. [blockedBy: T009,T010]
- [x] T012 [US1] Write `skills/external/sdd-loop-driver/references/decomposition-model.md` part 1: WP record schema, plan/amendment/ledger fences, id and layer assignment, canonical hash, attempt-scoped evidence paths, the 067 implement projection, the four decomposition rules with pointers to the required-output inventory owner (`data-model.md` E13) and the mirror owner (`plan.md` § Mirror Obligations), single-package representation, and gate invocation/repair/fallback pointers; cite the contracts and do not restate their tables or the two owned inventories. Test anchor: `tests/contract/test_sdd_loop_driver_wp_model.py`; evidence: `skills/external/sdd-loop-driver/references/decomposition-model.md`. [blockedBy: T011]
- [x] T013 [US1] Verify US1: run `python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_model.py tests/unit/test_wp_gate.py`, record the red-to-green evidence in `notes/red-first-evidence.md`, and append a targeted stage-status row to `test-evidence/implement-stage-status.jsonl`; confirm quickstart Scenarios A and B have a passing assertion or a recorded reason. Test anchor: both US1 test files; evidence: `notes/red-first-evidence.md` and `test-evidence/implement-stage-status.jsonl`. [blockedBy: T011,T012]

**Checkpoint**: US1 is independently testable: a fixture stage yields a gated WP plan, each injected defect is rejected, and the single-package decision is recorded.

---

## Phase 4: User Story 2 - Coordinate package dispatch with safe parallelism and deterministic writes (Priority: P1) 🎯 MVP

**Goal**: Dispatch packages through the existing mechanisms, overlap independent read-only packages within the slot cap, serialize every write package, isolate failures, and enforce the one-retry delta rule.

**Independent Test**: Dispatch a fixture DAG with two independent read-only packages and one dependent write package; confirm the read-only intervals overlap, the write starts only after its dependency is verified, and no writes overlap; force a failure and confirm the dependent stays blocked while unrelated work completes.

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [x] T014 [P] [US2] Write the red-first contract tests to `tests/contract/test_sdd_loop_driver_wp_coordination.py` for SD-01…SD-16: sole coordinator, readiness only on a verified verdict, write-alone rule, read-only slot cap, deterministic order and no starvation, local native and detached-runner topology, result collection, verifier dispatch, failure isolation, unlock rule, no nested driver, resource isolation, reuse without a new mechanism, and stage-attempt reset/re-entry; record the failing run in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T004]
- [x] T015 [US2] Write the red-first integration dry runs to `tests/integration/test_wp_coordination_dry_runs.py`: overlapping read-only intervals, write serialization, ownership/path rejection, dependency unlock only on `pass`, and failure isolation; use `tests/fixtures/wp_driver_sim.py` and `tests/fixtures/wp_fixtures.py` and assert intervals rather than wall-clock. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T004,T014]
- [x] T016 [US2] Extend `tests/unit/test_wp_gate.py` with red-first `--check preflight` and `--check retry` cases: manifest coverage and forbidden paths, unordered write/read and write/write overlaps, slot-cap bounds, isolation-missing, attempt-1 admission, `retry-unchanged`, `retry-exhausted`, scope/budget/topology delta validation (including a non-strictly-greater budget), split-child attempt inheritance, and split-depth-one rejection; record the failing run in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T010]

### Implementation for User Story 2

- [x] T017 [US2] Implement `wp-gate.py --check preflight` and `--check retry` for WG-14…WG-17: manifest normalization and coverage, territory overlaps, slot cap and resource isolation, ledger-derived dispatch counts, retry delta validation (strictly greater budget; split-child attempt inheritance; split depth one), and exit-2 as `decomposition-unavailable`; run the preflight/retry tests to green. Test anchor: `tests/unit/test_wp_gate.py` and `tests/contract/test_sdd_loop_driver_wp_gate.py`; evidence: `notes/red-first-evidence.md`. [blockedBy: T016]
- [x] T018 [US2] Write the scheduler, dispatch, and retry sections of `decomposition-model.md` (readiness, write priority, slot cap, collection, failure isolation, local native vs detached runner, anti-nesting check, retry counter/delta/escalation, stage-attempt reset), implement the scheduling algorithm in `tests/fixtures/wp_driver_sim.py`, and turn the T014/T015 scheduling cases green. Test anchor: `tests/contract/test_sdd_loop_driver_wp_coordination.py` and `tests/integration/test_wp_coordination_dry_runs.py`; evidence: `notes/red-first-evidence.md`. [blockedBy: T014,T015,T017]
- [x] T019 [US2] Verify US2: run the coordination contract tests, the scheduling dry runs, and the preflight/retry unit tests; record the red-to-green evidence, append a targeted stage-status row, and confirm quickstart Scenario C has a passing interval assertion. Test anchor: the US2 test files; evidence: `notes/red-first-evidence.md` and `test-evidence/implement-stage-status.jsonl`. [blockedBy: T017,T018]

**Checkpoint**: US2 is independently testable: read-only intervals overlap within the slot cap, every write interval is alone, a failure does not unlock dependents or cancel unrelated work, and a second attempt needs a material delta.

---

## Phase 5: User Story 3 - Verify each package independently, then integrate before the stage gate (Priority: P1) 🎯 MVP

**Goal**: Give every package exactly one independent verdict, aggregate outputs, stop on missing or contradictory results, integrate in the declared order with one closing commit, and only then run the unchanged stage U4.

**Independent Test**: Run a fixture where one package claims success without its output and another produces a conflicting artifact; confirm aggregation detects both, integration stops, and the stage gate fails. Then run a clean fixture and confirm the stage sentinel and U4 pass only after integration.

### Tests for User Story 3 (MANDATORY) ⚠️

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [x] T020 [P] [US3] Extend `tests/contract/test_sdd_loop_driver_wp_coordination.py` with red-first VI-01…VI-14 pins: one independent verifier, verifier read-only scope and targeted tests, verdict schema, missing verdict equals fail, verdict event, aggregation (including the `integrator_outputs` assignment), deterministic integration order, conflict stops integration, one closing commit, preserved implement part commits, integrator seat, owned outputs, and sentinel, package sentinels never promoted, unchanged stage U4, and driver-owned closure/merge; record the failing run in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T014]
- [x] T021 [US3] Extend `tests/integration/test_wp_coordination_dry_runs.py` with red-first verification/integration scenarios: missing output, contradictory output, deterministic integration order, package sentinel not promoted, stage U4 after integration, and the `driver-u4` capability fallback; record the failing run in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T015]

### Implementation for User Story 3

- [x] T022 [US3] Write the verification and integration sections of `decomposition-model.md` (verifier seat, verdict schema, aggregation, integration order, conflict stop, integrator `integrator_outputs` ownership, closing commit, unchanged U4), extend `tests/fixtures/wp_driver_sim.py` with independent verdicts and integration order, and turn the T020/T021 US3 cases green. Test anchor: the US3 test files; evidence: `notes/red-first-evidence.md`. [blockedBy: T020,T021]
- [x] T023 [US3] Verify US3: run the VI contract cases and the verification/integration dry runs, record the red-to-green evidence, append a targeted stage-status row, and confirm quickstart Scenarios D and F have passing assertions or recorded reasons. Test anchor: the US3 test files; evidence: `notes/red-first-evidence.md` and `test-evidence/implement-stage-status.jsonl`. [blockedBy: T022]

**Checkpoint**: US3 is independently testable: a missing or contradictory output stops integration, a clean set is integrated in graph order, and the stage U4 remains the final authority.

---

## Phase 6: User Story 4 - Reuse the team substrate through a stage-team preset and pattern selection (Priority: P2)

**Goal**: Map packages to existing Role × Stage × Type seats, select the graph-derived pattern, and bind the preset plus graph into a run-scoped plan without creating a persisted team.

**Independent Test**: Instantiate the preset for a fixture stage and confirm the seats, pattern, and slot cap derive from the graph; confirm no `.specify/teams/<slug>/` directory is created; confirm `parallel` is selected only for independent read-only graphs and `serial` for any graph containing a write package.

### Tests for User Story 4 (MANDATORY) ⚠️

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [x] T024 [P] [US4] Write the red-first contract tests to `tests/contract/test_sdd_loop_driver_wp_preset.py` for ST-01…ST-12: preset path and status, frontmatter fields, six mandatory body sections, four seats, seat-to-execution mapping, graph-derived pattern selection, `continuous` excluded, run-scoped adapter, no persisted team, `create-team`/`run-team` unchanged, provenance, and graph-over-preset precedence; record the failing run in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T004]

### Implementation for User Story 4

- [x] T025 [US4] Create `skills/external/sdd-loop-driver/templates/stage-team-preset.md` with the schema-compatible frontmatter, the six mandatory sections, the four seats (`stage-planner`, `stage-worker`, `stage-verifier`, `stage-integrator`), pattern-selection config, provenance, and the no-team-directory instantiation rule; add the adapter, seat-mapping, and pattern-selection sections to `decomposition-model.md`; run the preset tests to green. Test anchor: `tests/contract/test_sdd_loop_driver_wp_preset.py`; evidence: `notes/red-first-evidence.md`. [blockedBy: T024]
- [x] T026 [US4] Verify US4: run the preset contract tests and the no-team-directory dry-run case, assert no `.specify/teams/` directory is created, record the red-to-green evidence, and append a targeted stage-status row. Test anchor: `tests/contract/test_sdd_loop_driver_wp_preset.py` and `tests/integration/test_wp_coordination_dry_runs.py`; evidence: `notes/red-first-evidence.md` and `test-evidence/implement-stage-status.jsonl`. [blockedBy: T025]

**Checkpoint**: US4 is independently testable: the preset carries the four seats and pattern rules, the adapter records a run-scoped projection, and no team directory or create-team/run-team change appears.

---

## Phase 7: User Story 5 - Make the improvement measurable without a second ledger (Priority: P2)

**Goal**: Derive wall-clock, critical path, parallelism efficiency, stage-execution rate, retry counts, and manual interventions from the existing line state spine, and report `not_evaluated` for every missing source.

**Independent Test**: Run a fixture stage with two concurrent read-only packages and read the spine plus report; recompute the critical path and parallelism efficiency from the recorded timestamps; delete a timestamp and confirm the metric becomes `not_evaluated` rather than zero.

### Tests for User Story 5 (MANDATORY) ⚠️

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [ ] T027 [P] [US5] Write the red-first unit tests to `tests/unit/test_wp_report.py` for: stage wall-clock, duration-weighted critical path, parallelism efficiency with the product in the denominator, stage executions per canonical stage, package and stage retry counts, manual interventions, maximum concurrency and the overlap flag, token cost, `not_evaluated` for every missing source, Markdown/JSON parity, and no raw transcripts; record the failing run in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T004]

### Implementation for User Story 5

- [ ] T028 [US5] Implement `skills/external/sdd-loop-driver/scripts/wp-report.py`: CLI per OR-11 (`--spine`, `--stage`, `--stage-attempt`, `--out-dir`, `--stage-u4-at`, `--manual-interventions`, `--sessions`), derive OR-04…OR-13 metrics from the ledger (including the per-session intervention rate), write `<line>-<stage>-a<N>-coordination.md` and `.json`, print the metrics JSON, and never write the spine; run the report tests to green. Test anchor: `tests/unit/test_wp_report.py`; evidence: `notes/red-first-evidence.md`. [blockedBy: T027]
- [ ] T029 [US5] Write the observability, metrics, stage-close, and retry-accounting sections of `decomposition-model.md`: ledger and stage-close fields, metric definitions (the stage-attempt numerator, the per-session intervention rate with its session input, and the `not_evaluated` rule), the benchmark method (at least three comparable samples on the same host class and topology; conservative plan 70 min / review 37 min anchor; OR-04 interval), the closure consequence of an all-`not_evaluated` benchmark, retry accounting per OR-14…OR-16, report pointers, and no raw transcripts. Test anchor: `tests/unit/test_wp_report.py` and `tests/contract/test_sdd_loop_driver_wp_model.py`; evidence: `skills/external/sdd-loop-driver/references/decomposition-model.md`. [blockedBy: T028]
- [ ] T030 [US5] Verify US5: run the report unit tests and quickstart Scenario E against fixtures, assert that a deleted timestamp yields `not_evaluated` rather than zero, record the red-to-green evidence, and append a targeted stage-status row. Test anchor: `tests/unit/test_wp_report.py`; evidence: `notes/red-first-evidence.md` and `test-evidence/implement-stage-status.jsonl`. [blockedBy: T028,T029]

**Checkpoint**: US5 is independently testable: the report is derived from the spine, its metrics are recomputable, and missing sources are the literal `not_evaluated`.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Land the driver entry surface and docs, harden opt-out/fallback, prove non-regression and mutation resistance, sync mirrors, run the quickstart and benchmark, and close with the final regression.

- [ ] T031 [P] Update `tests/contract/test_sdd_loop_driver_skill.py` `PINNED_H2_SECTIONS` intentionally for the new 070 decomposition section, record the pin change in the test comment and the red run in `notes/red-first-evidence.md`, and keep every predecessor H2 pin unchanged. Test anchor: this test file; evidence: `notes/red-first-evidence.md`.
- [ ] T032 Write the new decomposition H2 in `skills/external/sdd-loop-driver/SKILL.md` (entry, when to decompose, gate/scheduler/verifier/integrator pointers, opt-out, boundaries) and the new section in `docs/reference/skills/sdd-loop-driver.md` (user-facing entry with pointers only); run T031 to green. Test anchor: `tests/contract/test_sdd_loop_driver_skill.py`; evidence: `skills/external/sdd-loop-driver/SKILL.md` and `docs/reference/skills/sdd-loop-driver.md`. [blockedBy: T031]
- [ ] T033 Create `tests/contract/test_non_regression_070.py` pinning 058 sentinel/U4 text, 063 fast lane/two-slot test budget/plan minor-fix/detach literals, 064 registry/ownership/worktree/integration interfaces, 067 part brief and dispatch-log fields, and 068 channel boundary; add the owner-agreement check — `plan.md` § Mirror Obligations is the only complete mirror source/mirror/verify table, `data-model.md` E13 is the only complete required-output inventory, `feature-ref.md` §7 and `research.md` R18 are pointers that name the owners, and `decomposition-model.md` references both owners without restating either table; assert additive-only changes and record the green run in `test-evidence/non-regression-070.txt`; this is a regression net (migration/regression exception) and makes no red-first claim. Test anchor: this test file; evidence: `test-evidence/non-regression-070.txt`. [blockedBy: T032]
- [ ] T034 Extend `tests/contract/test_sdd_loop_driver_wp_coordination.py` and `tests/integration/test_wp_coordination_dry_runs.py` with red-first FN-01…FN-16 cases: declaration fields, precedence, built-in defaults, auto and benefit, single-package path, fallback causes, no silent partial run, every-stage decision, preserved 058/063/064/067/068 behavior, test matrix, red-first evidence, and delivery surface; add the dry-run single-package, fallback, no-nested-driver, and no-team-directory cases; record the failing run in `notes/red-first-evidence.md`. Test anchor: both test files; evidence: `notes/red-first-evidence.md`. [blockedBy: T020,T021]
- [ ] T035 Write the opt-out and fallback sections of `decomposition-model.md` (U0 declaration, precedence, defaults, auto/benefit, single-package, the decision-to-gate-verdict mapping owned by FN-08, fallback causes, no silent partial run, every-stage decision with the plan fence as the canonical record, preserved behaviors, delivery surface), implement the fallback procedure in `tests/fixtures/wp_driver_sim.py`, and turn the T034 cases green. Test anchor: the FN contract and dry-run cases; evidence: `notes/red-first-evidence.md`. [blockedBy: T034]
- [ ] T036 Create `tests/contract/test_wp_mutation_drills.py` with mutated copies that remove the cycle check, allow write concurrency, treat a missing verdict as pass, and replace `not_evaluated` with zero; assert each drill makes at least one contract, unit, or integration test fail, and record each red drill result in `notes/red-first-evidence.md`. Test anchor: this test file; evidence: `notes/red-first-evidence.md`. [blockedBy: T011,T017,T022,T028,T035]
- [ ] T037 [P] Mirror sync: run `python3 scripts/python/sync-mirrors.py --write --only skills/external/sdd-loop-driver`, then `--check` against the T001 clean 28-file baseline, and `cmp` each source/mirror pair for `SKILL.md`, `references/decomposition-model.md`, `templates/stage-team-preset.md`, `scripts/wp-gate.py`, and `scripts/wp-report.py`; record zero NEW drift and never hand-edit `.specify/`. Test anchor: mirror `--check` and the five `cmp` results; evidence: `notes/pre-change-measurements.md` plus the sync output. [blockedBy: T032,T035]
- [ ] T038 Run quickstart Scenarios A–G against fixtures through the `.specify/skills/sdd-loop-driver/` mirror paths, write the real commands, outputs, rc, and teardown to `notes/quickstart-run.md`, and record the benchmark result in `notes/benchmark-070.md` with at least three comparable samples or the literal `not_evaluated` plus the manual-intervention and driver-session inputs; when the result is `not_evaluated`, record that closure is blocked unless the user explicitly waives SC-001/SC-002 in a written decision, and never mark either SC met on `not_evaluated`; make no absolute wall-clock claim. Test anchor: the seven scenarios; evidence: `notes/quickstart-run.md` and `notes/benchmark-070.md`. [blockedBy: T036,T037]
- [ ] T039 Final regression/closure: run all new unit, contract, and integration tests, `python3 scripts/python/validate-tasks.py .specify/specs/070-subagent-task-teams/tasks.md`, the 110-ID clause-inventory check (`for id in $(cat notes/contract-clause-inventory.txt); do grep -q "$id" tests/contract/test_sdd_loop_driver_wp_model.py tests/contract/test_sdd_loop_driver_wp_gate.py tests/contract/test_sdd_loop_driver_wp_coordination.py tests/contract/test_sdd_loop_driver_wp_preset.py || exit 1; done`), the full-suite closure slot `bash scripts/bash/run-tests.sh --names-out .specify/specs/070-subagent-task-teams/final-failed.txt`, the name-level `comm -13 baseline-failed.txt final-failed.txt` comparison (zero NEW failures), and the mirror `--check`; write the SC-001…SC-008 evidence matrix and handoff to `verification.md`, where SC-001/SC-002 each record met evidence or `not_evaluated` plus the recorded user waiver, and the closure gate fails (no handoff) when neither exists; do not push. Test anchor: all test suites plus the two baseline name lists; evidence: `verification.md`, `final-failed.txt`, and `notes/quickstart-run.md`. [blockedBy: T033,T036,T037,T038]

**Checkpoint**: Documentation, opt-out/fallback, non-regression, mutation resistance, mirrors, quickstart, benchmark, and closure evidence are all in place; only the driver's U4/review remains.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; T001–T004 can run together. T002 MUST run before any implementation edit.
- **Foundational (Phase 2)**: Depends on Setup; it blocks all user stories because every gate check uses the shared CLI, spine reader, schema validators, and canonical hash.
- **US1 (Phase 3)**: Depends on Foundational. It supplies the plan check and the model/ledger representation used by every later story.
- **US2 (Phase 4)**: Depends on US1's plan check (T011) and on the fixtures; it adds preflight/retry and the scheduler.
- **US3 (Phase 5)**: Depends on US2's scheduler and result collection; it adds independent verdicts and integration.
- **US4 (Phase 6)**: Depends on Setup's fixtures; it is independent of US3's integration behavior and may start once the preset test file is authored.
- **US5 (Phase 7)**: Depends on the ledger/model representation from US1 and the dispatch events from US2; it is independent of US3 and US4.
- **Polish (Phase 8)**: Depends on all user stories; T039 additionally depends on the non-regression and mutation nets.

### User Story Dependencies

- **US1 (P1)**: No story dependency; independent test = fixture plan + gate verdict + injected defects + single-package decision.
- **US2 (P1)**: Depends on US1's plan check; independent test = overlapping read-only intervals, write serialization, failure isolation, retry delta.
- **US3 (P1)**: Depends on US2's dispatch/collection; independent test = missing/contradictory output stops integration, clean set passes U4.
- **US4 (P2)**: Independent of US2/US3; independent test = preset seats, graph-derived pattern, no team directory.
- **US5 (P2)**: Depends on the US1 ledger and US2 dispatch events; independent test = recomputable metrics and `not_evaluated`.

### Within Each User Story

- Test rows come before implementation rows; each test row records a real failing run before the subject exists.
- The verification row runs the story's targeted tests, records red-to-green evidence, and appends a targeted stage-status row.
- Shared sinks: the red-first rows append to `notes/red-first-evidence.md`; they are sequenced within a phase rather than all marked `[P]`.

## Parallel Opportunities

- Setup: T001, T002, T003, and T004 write different targets and can run together.
- Foundational: T005 starts the gate contract test; T006 writes the gate unit test and follows in the same phase because both append to the red-first evidence sink.
- US1: T009 writes the model contract test while T010 waits for T006; after T011/T012, T013 verifies.
- US2: T014 writes the coordination contract test; T015 and T016 follow in phase order because they share the evidence sink and build on T014/T010.
- US3: T020 writes the VI contract cases; T021 writes the integration scenarios; both depend on earlier test files and share the evidence sink.
- US4: T024 writes the preset contract test; T025 follows; T026 verifies.
- US5: T027 writes the report unit test; T028 implements; T029 documents; T030 verifies.
- Polish: T031 is the only `[P]` row in this group (it edits the pin file); T032 follows T031; T033 follows T032 and runs the owner-agreement check; T034/T035/T036 are sequenced; T037 can run alongside T036 once T032/T035 are done; T038 follows T036/T037; T039 is last.

## Parallel Example: Setup

```bash
# These four rows write different targets and can be dispatched together.
Task: "T001 capture pre-change measurements in notes/pre-change-measurements.md"
Task: "T002 capture the E2 full-suite baseline at baseline-failed.txt"
Task: "T003 freeze the 110-id clause inventory at notes/contract-clause-inventory.txt"
Task: "T004 create tests/fixtures/wp_fixtures.py and tests/fixtures/wp_driver_sim.py"
```

## Parallel Example: User Story 2 tests

```bash
# T014 is the only [P] row in this test group because all three rows share the
# append-only red-first evidence sink; T015 and T016 follow in phase order.
Task: "T014 write the SD-01…SD-16 contract tests"
Task: "T015 write the scheduling dry runs"
Task: "T016 extend the gate unit tests with preflight and retry cases"
```

## Implementation Strategy

### MVP First

The MVP is US1 + US2 + US3 together: decomposition, safe dispatch, and independent verification/integration are each necessary for an independently valuable increment. Complete Setup and Foundational, then US1, US2, and US3, and stop at each checkpoint to validate the story independently. US4 and US5 follow as P2 refinements; Polish closes the surface.

### Incremental Delivery

1. Setup + Foundational → the gate core and dated baselines are ready.
2. US1 → a gated WP plan and the single-package decision are testable.
3. US2 → read-only overlap, write serialization, failure isolation, and retry deltas are testable.
4. US3 → independent verdicts, deterministic integration, and unchanged U4 are testable.
5. US4 → the preset and graph-derived pattern are testable without a persisted team.
6. US5 → the report and `not_evaluated` discipline are testable.
7. Polish → docs, fallback, non-regression, mutation, mirrors, quickstart, benchmark, and closure.

### Parallel Team Strategy

With multiple workers: one worker owns the gate script and its unit tests; one owns the model/ledger reference and its contract tests; one owns the simulator and the integration dry runs; one owns the report script and its unit tests. The driver remains the sole coordinator; no worker dispatches another worker or edits the plan.

## Notes

- `[P]` tasks write different targets and have no unfinished dependency; the shared red-first evidence sink is why several test rows are sequenced rather than all marked `[P]`.
- Package sentinels never satisfy a stage sentinel; only the integrator's `<STAGE>-DONE` (or the standard stage executor in a non-decomposed stage) does.
- The single-package path is the stage execution itself; for `implement`, the 067 part discipline remains in force.
- The mirror is generated by `sync-mirrors.py`; `.specify/skills/sdd-loop-driver/` is never hand-edited.
- Runtime records (`feedback/`, `session/`, `knowledge/`, `exec-quant/`, `history/`, `trigger/`) are not deliverables of this feature.
- No push, force merge, or confirmation-gate bypass; closure and merge remain driver-owned.
