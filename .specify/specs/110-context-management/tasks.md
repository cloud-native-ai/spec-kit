# Tasks: Context Management — 上下文的声明、组合与只读审计

**Requirement ID**: 110
**Requirement Key**: `110-context-management`
**Related Feature**: 110 Context Management（上下文管理）— the fixed binding per requirements A-2. By the line constraint this run writes no registry row and no detail file; the absent `.specify/features.md` row MUST NOT be read as "the feature does not exist" — registration is a recovery point for the line close-out's Feature Integration Protocol.
**Input**: Design documents from `.specify/specs/110-context-management/`
**Prerequisites**: plan.md (Technical Context / Mirror Obligations / Execution Premises EP-001…EP-010 / Inherited Blockers), requirements.md (29 FR / 11 SC / [[STR-001]]…[[STR-006]] / A-1…A-17 / US1…US5), research.md (R-1…R-10 / RU-1…RU-3), data-model.md (E-1…E-11 / I-1…I-14), contracts/ ×5 (C-001…C-007 / C-010…C-016 / C-020…C-029 / C-030…C-037 / C-040…C-046), quickstart.md (6 scenarios), feature-ref.md.

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" — a test-mandating principle: pure functions/utilities MUST have unit tests, critical flows MUST have automated regression coverage, and integration/contract tests MUST cover cross-service communication. The feature ships an executable stdlib engine plus framework docs and declarations, so the runtime form is four contract guard files + one integration guard file; the doc/declaration surfaces are pinned by structural contract tests, the engine by runtime tests. Every guard file is authored red-first in Phase 2, before any implementation row.)

**Tests**: All test execution goes through `scripts/bash/run-tests.sh` (single entry; direct interpreter-level test commands are never the entry). Red-first evidence consolidates at `.specify/specs/110-context-management/notes/red-first-evidence.md`; the failing-test-name baseline belongs to the implement **Test runs** bullet — this file references that owner and never restates its path or flag. The interpreter constraint is fixed in § Environment Prerequisites.

**Organization**: Tasks are grouped by user story in requirement priority order — US1 (一条不变基线，组合一次, P1), US2 (可变层逐任务选择, P1), US3 (客户项目经 init 获得它：离线且诚实, P1), US4 (主动触发与具名组合角色, P2), US5 (一次只读审计读数, P3). Because one mechanism serves all stories (one owner document, one engine), the guard files are authored once in Foundational and each story phase owns the implementation rows that turn its clause subset green; each story phase therefore carries its goal, its independent test, the pointer to the guard legs that certify it, and a verification row holding its `[green:]` claims.

## Definition of Done (DoD)

- DoD-1: All task rows read `[X]`; any `[~]` row carries its reason inline and in `.specify/specs/110-context-management/test-evidence/verification-input.md` (`deferred_tasks=`); no row is silently dropped.
- DoD-2: Deliverable set complete — the owner document with the machine-parsed layout table, the four declaration facts plus their four append-only registration keys, the stdlib read-only engine with both actions, the five guard files plus the fixture family, the ambient instructions section in the template and the regenerated live file, the three framework-map rows, and byte-identical mirrors; zero new third-party dependencies. The containment claim follows `.specify/shared/guidelines/closed-set-claims.md`: baseline referent = the implement-entry commit captured by T004; comparison units per artifact class (dependency requirement sets; changed-path set vs the declared file fan-out; per-action tree manifests); allowed-delta set = the declared fan-out derived from the change itself; complement assertion = empty outside the fan-out and inside the runtime scratch roots; no undefined aggregate words.
- DoD-3: Coverage accounting — every FR (FR 29/29) and every SC (SC 11/11) appears in § Requirement Coverage Map; all 39 contract clauses are claimed exactly once in § Clause Coverage & Green Partition; `validate-tasks.py` exits 0 with every WARN adjudicated in `test-evidence/tasks-validator.txt`.
- DoD-4: Red-first and guard credibility — all five guard files were authored and observed red before any implementation row; every `check` rule's guard test went red under its own mutation drill, with per-rule command, output and exit captured; no guard is skipped, muted or excluded.
- DoD-5: Closed-set honesty — every member of `context-categories`, `context-layers` and `context-forms` is exercised (mutating or removing it produces an observable difference), and every unknown or missing declaration member is refused with exit 2, never defaulted.
- DoD-6: Ambient section fits — the generator's `BUDGET:` line reads `within` under the unchanged constant, no existing section is trimmed, and the section is summary-plus-pointer with no layout table, no class roster and no cap literal.
- DoD-7: Audit determinism and honesty — byte-identical reruns on an unchanged tree, no timestamps or host values in any output, a metadata-only `source-reading` digest, and the three concept-pointer rows present here with honest absence readings on the concept-missing fixture (never `present`, never agreement).
- DoD-8: Protected surfaces unchanged against the implement entry — the super↔sub protocol's declared item set, the memory-recall output on the populated stores, and the rendered-agent fixture output all equal their pre-change captures; the full suite reports zero NEW failures.
- DoD-9: Containment of the surface — no new `/speckit.*` command, skill wrapper, gate, red line, store, cache or network path; the runtime-store roster is unchanged; the only durable additions are the declared set of DoD-2.

**DoD Status**: pending

## Completion Gate

- GATE-1: Task file structure legal — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/110-context-management/tasks.md` exit 0 (zero ERROR; every WARN adjudicated in `test-evidence/tasks-validator.txt`).
- GATE-2: Cross-artifact gate — check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/110-context-management --stage tasks --repo .` prints `decision=pass` with errors=0 (deliverable-path advisories adjudicated).
- GATE-3: FR / SC / clause coverage — check: § Requirement Coverage Map reads FR 29/29 and SC 11/11; § Clause Coverage & Green Partition claims all 39 clauses exactly once; `validate-tasks.py` reports zero ERROR for `green-dangling`, `green-clause-collision`, `green-cross-phase` and `green-path-divergence`.
- GATE-4: Final-path success criteria and smoke record — check: in the implement-produced `verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and an existing non-empty `smoke_evidence_path=` are all present (condition-set owner: `shared/workflow/acceptance-hardening.md` § Gates).
- GATE-5: Mirrors and generated copies — check: `python3 scripts/python/sync-mirrors.py --check` shows no NEW drift against `test-evidence/mirror-baseline-plan.txt`, and the owner document, the four facts and the engine are byte-identical between source and mirror.
- GATE-6: Ambient section — check: `bash scripts/bash/generate-instructions.sh` reports a `BUDGET:` line reading `within`, and the heading `## Context Management(上下文管理)` appears verbatim in `templates/instructions-template.md`, `.specify/templates/instructions-template.md` and `.specify/instructions.md` with pointer shape intact.
- GATE-7: Audit reading — check: `python3 .specify/scripts/python/context-audit.py --action check` exits 0 with zero findings on this repository, the four named seeded fixtures each produce exactly their expected finding at exit 1, and a second run over each unchanged tree is byte-identical.
- GATE-8: No open or claimed rows — check: `grep -cE '^- \[[ >]\]' .specify/specs/110-context-management/tasks.md` returns 0.
- GATE-9: Full suite and protected surfaces — check: the full run through `scripts/bash/run-tests.sh` reports zero NEW failure names against the implement-entry baseline (owner: the implement **Test runs** bullet), and the three protected-surface captures equal `notes/pre-change-measurements.md`.
- GATE-10: Mutation drill evidence — check: `test-evidence/mutation-drill.txt` carries one red guard verdict per `check` rule (nine rules), and `git diff` over the engine is empty after the drill.

## Environment Prerequisites

- CPython `>=3.8`: **available** — probe: `/usr/local/bin/python3 --version` → `Python 3.11.11` @ 2026-11-27; affected: the engine and every test row.
- pytest: **available under `/usr/local/bin/python3` only** — probe: `/usr/local/bin/python3 -m pytest --version` → `pytest 8.4.2`; the PATH `python3` (profiles venv) answers `No module named pytest`. All test rows MUST run through `scripts/bash/run-tests.sh` with `SPECKIT_PYTHON=/usr/local/bin/python3` (the runner resolves `SPECKIT_PYTHON` first, then a repo `.venv`, then PATH); affected: every test row.
- bash / git: **available** — probe: `bash --version` → `GNU bash, version 4.4.20(1)-release`; `git --version` → `git version 2.43.5` @ 2026-11-27; affected: the instructions generator, the mirror flow, the baselines and the changed-set audit.
- Network / container runtime / registry / live cluster: **none required and none permitted** — the init fixture blocks sockets in process (precedent `tests/integration/test_feedback_exec_quant_channel.py`), and the audit itself must open no socket; no build, pull or daemon; affected: none.

**A13 boundary** (owner: `shared/workflow/acceptance-hardening.md` § Gates — this note is a pointer, not a second rule): this section records task-generation probe verdicts only, each with its probe command and an ISO date. A planning-time load-bearing premise belongs to `plan.md` § Execution Premises; an inherited dependency record belongs to `plan.md` § Inherited Blockers.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: parallelizable only where the write targets are disjoint (the Setup captures and the five guard authoring rows). T004 deliberately carries no [P] because it re-measures the mirror and toolchain readings after T003's freeze so the two records agree. All implementation rows share the one engine file, the one owner document or the one verification sink and are serial by row order.
- **[Story]**: `[US1]`…`[US5]` on every row inside a user-story phase; Setup, Foundational and Polish rows carry no story label.
- **[blockedBy: T001,T002]**: explicit dependency tag; the row MUST NOT start until every listed task is `[X]`. Omitted when only phase order applies.
- **[green: <contract>#<clause>]**: green-point claim, carried only by the verification row that leaves the clause green; the contract path resolves beside this file; the 39-clause partition is in § Clause Coverage & Green Partition; test-authoring rows carry none.
- One line per task (mechanical-validation contract): the whole row — checkbox, id, labels, description and file paths — stays on a single line.

### Task State Sigil (REQUIRED)

- `- [ ]` — Open; `- [>]` — Claimed (multi-agent runs only); `- [X]` — Closed; `- [~]` — Deferred, with the reason recorded inline and in `test-evidence/verification-input.md` `deferred_tasks=`.

## Path Conventions

- **Framework source edit surface**: `shared/definitions/context-management-definitions.md`, `shared/definitions/framework-map.md`, `shared/declarations/facts/context-{categories,layers,forms,classes}.yaml`, `shared/declarations/contract.yaml`, `scripts/python/context-audit.py`, `templates/instructions-template.md`, `tests/contract/test_context_management_*.py`, `tests/integration/test_context_management_init.py`, `tests/fixtures/context-management/`, `tests/fixtures/context_management_support.py`.
- **Generated surface (MUST NOT be hand-edited)**: `.specify/shared/`, `.specify/scripts/`, `.specify/templates/` (projected by `sync-mirrors.py`); `.specify/instructions.md` (regenerated by `scripts/bash/generate-instructions.sh`); the tool instruction files are symlinks into `.specify/instructions.md`.
- **Read-only surface**: this spec's plan-owned artifacts (`plan.md`, `requirements.md`, `data-model.md`, `research.md`, `quickstart.md`, `feature-ref.md`, `contracts/`, `checklists/`, `checkpoints/`), other specs, `.specify/features.md`, `.specify/features/`, `.specify/register.md`, `.specify/glossary.md` and the state spine. The task stage writes none of them.
- **Evidence landing points (this feature)**: `.specify/specs/110-context-management/notes/{pre-change-measurements.md,red-first-evidence.md,quickstart-run.md}`, `.specify/specs/110-context-management/coverage-baseline.txt`, `.specify/specs/110-context-management/test-evidence/{implement-entry-readings.txt,red-owner.txt,red-declarations.txt,red-engine.txt,red-readonly.txt,red-init.txt,us1-green.txt,us2-green.txt,us3-green.txt,us4-green.txt,us5-green.txt,audit-fixtures.txt,determinism.txt,concept-presence.txt,mutation-drill.txt,full-suite.txt,guard-convergence.txt,changed-set.txt,cap-scan.txt,mirror-final.txt,tasks-validator.txt,verification-input.md}`.

## Measured Premises (re-measured at generation time 2026-11-27, HEAD `ae9922ca8`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| FR / SC counts | `grep -cE '^- \*\*FR-[0-9]+\*\*:' .specify/specs/110-context-management/requirements.md`; same for `SC-` | **29 / 11** |
| Contract clause counts | `grep -cE '^## C-[0-9]+' .specify/specs/110-context-management/contracts/*.md` | owner-and-layout **7** / declarations **7** / matrix-and-triggers **10** / engine-and-distribution **8** / guards-and-boundaries **7** → **39**. **Trap form**: `grep -ohE '\bC-[0-9]+\b' …/contracts/*.md \| wc -l` → **54** (in-body cross-references mixed in); the unit is the `## C-NNN` definition heading |
| Live instructions budget | `wc -c < .specify/instructions.md`; `grep -c '^## ' .specify/templates/instructions-template.md .specify/instructions.md`; `grep -n 'INSTRUCTIONS_BUDGET_BYTES' scripts/bash/generate-instructions.sh` | **40,170 B**; template **39** sections, live **40**; constant at line **119**, value **40,960** — headroom **789 B** (40,960 − 1 − 40,170) |
| Mirror baseline | `python3 scripts/python/sync-mirrors.py --check` | rc **0** — six pairs byte-identical (templates 23, skills/external 439, skills/internal 139, agents 20, scripts 133, shared 117) and six per-file projections `ok` |
| New artifacts absent | per-path `test -e` for owner doc, four facts, engine, five guard files, fixture directory | **12/12 ABSENT** (red-first prerequisite) |
| Toolchain | `/usr/local/bin/python3 --version`; `/usr/local/bin/python3 -m pytest --version`; `python3 -m pytest --version`; `git --version`; `bash --version` | **3.11.11**; **pytest 8.4.2**; PATH `python3` → **No module named pytest**; **git 2.43.5**; **bash 4.4.20** |
| Protocol item set (protected surface) | read `shared/definitions/superagent-definitions.md` § Downlink | seven role fields (`parent_identity`, `child_label`, `role_declaration`, `dispatch_duty`, `depth_position`, `authority_ref`, `return_channel`) + four injections (fast-fail clause, concurrency obligation, reporting duty, re-anchoring anchor digest) — the baseline the protocol-boundary guard compares against |
| Reader / interface carriers | `grep -n 'def load_fact' scripts/python/declaration_reader.py`; `ls scripts/python/script_interface_cli.py scripts/bash/run-tests.sh` | `load_fact` at line **400**; both helper entries present |
| Memory recall surface | `python3 scripts/python/memory-utils.py --help` | action `recall` with `--scope`, `--query`, `--format {text,json}` — the protected-surface capture command |
| Section-count pins | `grep -nE ' 39| 40|section_count' tests/contract/test_instructions_section_propagation.py` | no literal count pin found (presence/verbatim legs only); re-measured at implement per RU-3 |
| Worktree base and status | `git rev-parse HEAD`; `git status --short` | `ae9922ca8`; one pre-existing other-run session record modified — attributed and never committed or reverted by this stage |

## Requirement Coverage Map

| FR | Rows | FR | Rows | FR | Rows |
|----|------|----|------|----|------|
| FR-001 | T009, T016, T020 | FR-011 | T012, T016, T018, T036 | FR-021 | T011, T018, T022, T024 |
| FR-002 | T009, T010, T014, T016, T020 | FR-012 | T009, T017, T020, T028, T031 | FR-022 | T011, T018, T022, T024, T032, T036 |
| FR-003 | T009, T010, T014, T016, T020 | FR-013 | T009, T011, T021, T024 | FR-023 | T013, T019, T023, T025, T026, T027, T038 |
| FR-004 | T009, T014, T017, T024 | FR-014 | T009, T028, T031 | FR-024 | T012, T013, T018, T027, T036 |
| FR-005 | T009, T016, T028, T036 | FR-015 | T009, T028, T031 | FR-025 | T009, T013, T029, T030, T031 |
| FR-006 | T011, T017, T018 | FR-016 | T009, T011, T028, T031 | FR-026 | T011, T036 |
| FR-007 | T011, T017, T018, T020 | FR-017 | T009, T028, T031, T036 | FR-027 | T010, T034, T035, T036 |
| FR-008 | T011, T021, T024 | FR-018 | T010, T014, T015, T022 | FR-028 | T009, T011, T024, T028, T031, T033, T036 |
| FR-009 | T010, T011, T014, T016, T022, T024 | FR-019 | T010, T017, T021, T022, T024, T038 | FR-029 | T009, T016, T036 |
| FR-010 | T011, T021, T024 | FR-020 | T011, T016, T018, T020, T024, T033 |  |  |

| SC | Rows |
|----|------|
| SC-001 | T032 |
| SC-002 | T012, T027 |
| SC-003 | T032 |
| SC-004 | T032 |
| SC-005 | T027 |
| SC-006 | T038 |
| SC-007 | T024, T036 |
| SC-008 | T035 |
| SC-009 | T030, T031 |
| SC-010 | T033 |
| SC-011 | T036 |

## Clause Coverage & Green Partition

All 39 machine-decidable clauses are claimed exactly once. Testing-authoring rows (T009–T013) carry no `[green:]` tags; each story's verification row owns its clause subset, so within one contract the clause ordinals never run backwards against row order and no clause collides.

| Contract | Clause | Pinning test | Green point |
|----------|--------|--------------|-------------|
| `contracts/owner-and-layout.contract.md` | C-001 | `test_context_management_owner.py::test_owner_document_is_the_single_model_home` | T020 |
| `contracts/owner-and-layout.contract.md` | C-002 | `test_context_management_owner.py::test_bilingual_definition_sites_carry_the_fixed_literals` | T020 |
| `contracts/owner-and-layout.contract.md` | C-003 | `test_context_management_owner.py::test_terminology_boundary_table_names_four_neighbours_by_pointer` | T020 |
| `contracts/owner-and-layout.contract.md` | C-004 | `test_context_management_owner.py::test_layout_table_is_the_single_row_data_home` | T024 |
| `contracts/owner-and-layout.contract.md` | C-005 | `test_context_management_owner.py::test_form_legality_matrix_matches_the_owner_document` | T024 |
| `contracts/owner-and-layout.contract.md` | C-006 | `test_context_management_owner.py::test_landing_contract_declares_three_cells_and_three_forbidden_pairs` | T024 |
| `contracts/owner-and-layout.contract.md` | C-007 | `test_context_management_owner.py::test_concept_pointer_slot_structures_have_carriers_and_presence_surfaces` | T031 |
| `contracts/declarations-and-domains.contract.md` | C-010 | `test_context_management_declarations.py::test_four_facts_carry_required_keys_and_registration` | T024 |
| `contracts/declarations-and-domains.contract.md` | C-011 | `test_context_management_declarations.py::test_domains_are_closed_sets_with_one_owner` | T024 |
| `contracts/declarations-and-domains.contract.md` | C-012 | `test_context_management_declarations.py::test_engine_reads_facts_through_the_shared_reader` | T024 |
| `contracts/declarations-and-domains.contract.md` | C-013 | `test_context_management_declarations.py::test_no_numeric_bound_and_cap_reference_form` | T024 |
| `contracts/declarations-and-domains.contract.md` | C-014 | `test_context_management_declarations.py::test_presence_vocabulary_is_defined_once` | T024 |
| `contracts/declarations-and-domains.contract.md` | C-015 | `test_context_management_declarations.py::test_roster_agreement_is_machine_checked` | T024 |
| `contracts/declarations-and-domains.contract.md` | C-016 | `test_context_management_declarations.py::test_unknown_or_missing_declaration_member_is_refused` | T024 |
| `contracts/matrix-and-triggers.contract.md` | C-020 | `test_context_management_owner.py::test_baseline_composes_once_per_session_or_line` | T020 |
| `contracts/matrix-and-triggers.contract.md` | C-021 | `test_context_management_owner.py::test_task_composition_selects_under_caps_without_widening` | T024 |
| `contracts/matrix-and-triggers.contract.md` | C-022 | `test_context_management_owner.py::test_trigger_set_is_closed_at_seven` | T031 |
| `contracts/matrix-and-triggers.contract.md` | C-023 | `test_context_management_owner.py::test_composer_roles_resolve_through_the_existing_relative_model` | T031 |
| `contracts/matrix-and-triggers.contract.md` | C-024 | `test_context_management_owner.py::test_source_drift_is_an_observed_record_change_not_a_poll` | T031 |
| `contracts/matrix-and-triggers.contract.md` | C-025 | `test_context_management_owner.py::test_dispatch_mapping_keeps_the_existing_payload` | T031 |
| `contracts/matrix-and-triggers.contract.md` | C-026 | `test_context_management_owner.py::test_concept_pointer_slot_maps_onto_existing_channels_per_structure` | T031 |
| `contracts/matrix-and-triggers.contract.md` | C-027 | `test_context_management_engine.py::test_decidable_duplication_shapes_are_reported` | T031 |
| `contracts/matrix-and-triggers.contract.md` | C-028 | `test_context_management_owner.py::test_reentry_recites_refreshes_delta_and_records_statement` | T031 |
| `contracts/matrix-and-triggers.contract.md` | C-029 | `test_context_management_readonly.py::test_no_composition_is_persisted` | T036 |
| `contracts/engine-and-distribution.contract.md` | C-030 | `test_context_management_engine.py::test_single_documented_entry_two_actions_no_wrapper` | T020 |
| `contracts/engine-and-distribution.contract.md` | C-031 | `test_context_management_engine.py::test_script_interface_contract_is_satisfied` | T020 |
| `contracts/engine-and-distribution.contract.md` | C-032 | `test_context_management_engine.py::test_check_reports_the_closed_rule_set_deterministically` | T024 |
| `contracts/engine-and-distribution.contract.md` | C-033 | `test_context_management_engine.py::test_manifest_prints_roster_rows_with_presence_and_cap` | T024 |
| `contracts/engine-and-distribution.contract.md` | C-034 | `test_context_management_engine.py::test_audit_does_not_select_rank_or_read_content` | T024 |
| `contracts/engine-and-distribution.contract.md` | C-035 | `test_context_management_readonly.py::test_containment_claims_are_decidable` | T027 |
| `contracts/engine-and-distribution.contract.md` | C-036 | `test_context_management_init.py::test_fresh_init_distributes_and_audits_offline` | T027 |
| `contracts/engine-and-distribution.contract.md` | C-037 | `test_context_management_owner.py::test_ambient_section_stays_summary_plus_pointer` | T031 |
| `contracts/guards-and-boundaries.contract.md` | C-040 | `test_context_management_engine.py::test_seeded_rule_fixtures_are_exact` | T034 |
| `contracts/guards-and-boundaries.contract.md` | C-041 | `test_context_management_readonly.py::test_containment_claims_are_decidable` | T035 |
| `contracts/guards-and-boundaries.contract.md` | C-042 | `test_context_management_owner.py::test_concept_pointer_and_protocol_boundary_guard` | T036 |
| `contracts/guards-and-boundaries.contract.md` | C-043 | `test_context_management_owner.py::test_layer_landing_guard` | T036 |
| `contracts/guards-and-boundaries.contract.md` | C-044 | `test_context_management_owner.py::test_existing_owners_are_not_redefined` | T036 |
| `contracts/guards-and-boundaries.contract.md` | C-045 | `test_context_management_readonly.py::test_no_new_command_skill_gate_store_or_network` | T036 |
| `contracts/guards-and-boundaries.contract.md` | C-046 | `test_context_management_declarations.py::test_every_declared_member_is_exercised` | T036 |

## Feature Integration Review

- **Review performed at generation (2026-11-27)**: `.specify/features.md` carries no row for Feature 110 — expected under the line constraint (A-2; plan § Feature Integration). The task breakdown exposes no new feature and invalidates none; the index row, the detail file and the status advance remain a recovery point for the line close-out's Feature Integration Protocol.
- **Glossary**: no edit — `.specify/glossary.md` is a single-owner canonical registry and this line is forbidden to edit registries. The six bilingual terms live in the owner document definition sites ([[STR-001]]…[[STR-006]]); a glossary proposal, if the close-out judges one warranted, goes through `shared/workflow/glossary.md`'s protocol then.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the evidence landing points and freeze every pre-change reading before any edit.

- [ ] T001 Create the evidence landing directory `.specify/specs/110-context-management/notes/` with a `.gitkeep` so red-first, quickstart and pre-change records have their fixed landing points.
- [ ] T002 [P] [blockedBy:T001] Freeze the contract/FR coverage baseline: run `python3 scripts/python/account-clause-coverage.py .specify/specs/110-context-management --freeze > .specify/specs/110-context-management/coverage-baseline.txt`, assert the frozen file is non-empty and its header records the exclusion of `110-context-management` itself, and note the frozen clause and FR name counts in the file header (FR-027).
- [ ] T003 [P] [blockedBy:T001] Capture the pre-change side of every diff premise in `.specify/specs/110-context-management/notes/pre-change-measurements.md` with command, real output and date per row: live `.specify/instructions.md` size and section counts against the template, the generator budget constant, run `python3 scripts/python/sync-mirrors.py --check` and record its verdict, the super↔sub protocol's declared item set (seven role fields plus four injections) read from `shared/definitions/superagent-definitions.md`, the `memory-utils.py --action recall` output on the populated stores, the rendered-agent fixture output, the measured FR/SC/clause counts with their trap forms, and the absence checks for the twelve new artifacts (FR-027, SC-008).
- [ ] T004 [blockedBy:T001] Record the implement-entry readings in `.specify/specs/110-context-management/test-evidence/implement-entry-readings.txt`: the `implement_start_commit=` line from `git rev-parse HEAD` (the SC-008 baseline referent), the `pyproject.toml` dependency sets, the CPython and pytest readings, the `scripts/bash/run-tests.sh` presence and its resolution order, run `python3 scripts/python/sync-mirrors.py --check` and record its rc, and the per-path `test -e` results for the twelve new artifacts; this is the environment reading plus the containment baseline, never a second failing-test baseline (owner of that baseline: the implement **Test runs** bullet).
- [ ] T005 [P] [blockedBy:T001] Create the red-first evidence skeleton `.specify/specs/110-context-management/notes/red-first-evidence.md` with one slot per guard file and per `check` rule (nine rules), each slot recording command, real output and exit status; reference the implement **Test runs** owner for the failing-name baseline instead of restating its path or flag (FR-027, C-040).

**Checkpoint**: evidence landing points exist; all pre-change values are frozen; no executable surface changed yet.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Author the fixture family and all five guard files red-first — every implementation row in every story depends on these being in place and observed failing.

**⚠️ CRITICAL**: No user story implementation can begin until this phase is complete.

- [ ] T006 Author the fixture support module `tests/fixtures/context_management_support.py`: copy a fixture case tree into a pytest `tmp_path` workspace, run the engine as a subprocess with `--workspace-root` (interpreter from `sys.executable`), parse the JSON face, compute a SHA-256 tree manifest that excludes `__pycache__` by name, and expose the minimal owner-document and fact text helpers; standard library plus pytest only, no network (A-17, C-040).
- [ ] T007 [blockedBy:T006] Author the behavioral fixture trees under `tests/fixtures/context-management/`: `all-present/` (every roster source resolvable, readable and non-empty, including the three concept-pointer rows), `absence-mixed/` (one missing source, one empty store, one unreachable source built as a dangling symlink so the mechanism never depends on privileges), and `concept-missing/` (one concept-pointer layout row deleted plus one declared source unreadable); each case carries its own `shared/definitions/context-management-definitions.md` and `shared/declarations/facts/context-{categories,layers,forms,classes}.yaml` at its workspace root in the framework-source shape (A-17, SC-003, SC-010).
- [ ] T008 [blockedBy:T007] Author the rule and input fixture trees under `tests/fixtures/context-management/`: `violation-unknown-layer/`, `violation-unknown-form/`, `violation-roster-mismatch/`, `violation-roster-order/`, `violation-layer-form/` (one task row `read-in-full` plus one system row `bounded-index`, expecting exactly the two layer-form findings), `violation-duplicate-class/`, `violation-empty-layer/`, `violation-cap-missing/`, `violation-category-column/`, `declaration-unknown-member/` and `declaration-missing/`; each case carries its own minimal declaration layer and deviates in exactly the one token its rule judges, with declaration-layer violations kept as exit-2 inputs, never findings (C-040, C-032, C-016).
- [ ] T009 [P] [blockedBy:T008] Author `tests/contract/test_context_management_owner.py` red-first before any owner-document edit: the bilingual definition-site literals [[STR-001]]…[[STR-006]], the heading and ownership set, the four-neighbour boundary table by pointer, the fixed six-column layout table with no category column, the roster and landing-cell declarations (three legal cells, three forbidden combinations, allowed forms by reference), the once-defined presence vocabulary plus the `Unobserved` pointer, the concept-pointer slot (triple, four governed structures, per-structure carrier and named presence surface), the protocol legs (baseline once, session versus line; task composition under caps; closed trigger set; composer roles through the existing model; reentry semantics; source-drift definition; dispatch mapping that adds no field, injection, cap, identifier or self-check), the protocol-boundary leg that parses the owner's seven role fields plus four injections and asserts the set equals the pre-change baseline from `notes/pre-change-measurements.md`, and the ambient-section legs (template and live presence, pointer shape with no layout table, roster or cap literal, template-side mutation leg); run `scripts/bash/run-tests.sh` and capture the failing output in `.specify/specs/110-context-management/test-evidence/red-owner.txt` (FR-001, FR-002, FR-003, FR-004, FR-005, FR-012, FR-013, FR-014, FR-015, FR-016, FR-017, FR-025, FR-028, FR-029).
- [ ] T010 [P] [blockedBy:T008] Author `tests/contract/test_context_management_declarations.py` red-first: the four facts' required keys and kinds, the four append-only registration keys in `shared/declarations/contract.yaml`, membership and order of the closed sets, the classes roster rendered against the owner-document row order, the single-reader read-point (no second YAML parser and no hard-coded member in the engine), the no-numeric-bound scan, the cap-reference form check, the unknown or missing declaration member refusal (exit 2, no partial verdict) and member-exercise legs that mutate each declared member and require an observable difference; run `scripts/bash/run-tests.sh` and capture the failing output in `test-evidence/red-declarations.txt` (FR-002, FR-003, FR-009, FR-018, FR-019, FR-027).
- [ ] T011 [P] [blockedBy:T008] Author `tests/contract/test_context_management_engine.py` red-first: the CLI surface (`-h` and `--help` identical bodies, the `--version` identity line, an undeclared option exits 2 before any action including after a bare `--`, `manifest` without or with an out-of-domain `--layer` exits 2, `--layer` with `check` exits 2, an unresolvable workspace root exits 2); `check` clean on this repository (exit 0, zero findings) and every seeded-violation fixture producing exactly its expected finding and exit 1, with the four SC-001 fixtures exact (unknown-layer, unknown-form, roster-mismatch, layer-form) and the merged layer-form fixture yielding exactly two findings; the declaration-error fixtures exit 2 with no partial verdict; `manifest` exact tokens and reasons on the all-present and absence-mixed fixtures, the roster row set on concept-missing (missing-layout row reading `not-evaluated`), ordered JSON keys and same-content text/JSON faces for both actions, the `source-reading` digest stability and its change when a declared source's metadata changes, byte-identical reruns, and the honesty legs (no selection, ranking, content read or host values and timestamps); run `scripts/bash/run-tests.sh` and capture the failing output in `test-evidence/red-engine.txt` (FR-006, FR-007, FR-008, FR-009, FR-010, FR-013, FR-016, FR-020, FR-021, FR-022, FR-028).
- [ ] T012 [P] [blockedBy:T008] Author `tests/contract/test_context_management_readonly.py` red-first: a SHA-256 tree manifest taken immediately before and after each audit action over the fixture trees and the repository tree (identical bytes, zero new files, `__pycache__` excluded by name), a socket-blocked in-process run that monkeypatches the socket entry points and asserts no connection attempt, and the zero-write and no-cache legs; run `scripts/bash/run-tests.sh` and capture the failing output in `test-evidence/red-readonly.txt` (FR-011, FR-024, SC-002, C-041).
- [ ] T013 [P] [blockedBy:T008] Author `tests/integration/test_context_management_init.py` red-first with two separately named legs: `test_fresh_init_distributes_and_audits_offline` initializes a fresh project through the repository's own in-process init path (`specify_cli` with its resource root pointed at the repository root, sockets blocked, precedent `tests/integration/test_ai_tools_instruction_preservation.py`), asserts the owner document, the four facts and the engine land under `.specify/`, and runs `check` (exit 0) and `manifest --layer project` (explicit absence lines, exit 0) with zero sockets opened and nothing transmitted; `test_fresh_init_instructions_carry_the_ambient_section` asserts the generated instructions of that fresh tree carry `## Context Management(上下文管理)` in summary-plus-pointer shape, and this leg stays red until the ambient section lands; run `scripts/bash/run-tests.sh` and capture the failing output in `test-evidence/red-init.txt` (FR-023, FR-024, FR-025, SC-005, SC-009).

**Checkpoint**: fixtures and all five guard files exist and were observed red; no implementation row has run.

---

## Phase 3: User Story 1 - 一条不变基线，组合一次 (Priority: P1) 🎯 MVP

**Goal**: The model and its value domains land together with the owner document and the audit engine's manifest, so a session composes the invariant baseline once — system facts discovered, project facts carried as canonical pointers with zero copied bytes — and reuses it.

**Independent Test**: On the all-present fixture the manifest's system and project layer rows list form and source in roster order with every row `present`, the governance baseline appears as `read-in-full` canonical pointers with no copied content, a second run is byte-identical, and the owner-model legs (definition sites, categories, layers, forms, landing cells, presence vocabulary, boundary table, baseline-once protocol) are green.

### Tests for User Story 1 (MANDATORY)

> All guard files were authored red-first in Phase 2. This story's legs are the model and baseline legs of `tests/contract/test_context_management_owner.py`, the fact-shape and registration legs of `tests/contract/test_context_management_declarations.py`, and the manifest system/project legs of `tests/contract/test_context_management_engine.py`. No new test file is authored in this phase.

### Implementation for User Story 1

- [ ] T014 [US1] [blockedBy:T010] Author the four declaration facts under `shared/declarations/facts/`: `context-categories.yaml` (`closed-set`: `invariant`, `variable`), `context-layers.yaml` (`closed-set`: `system`, `project`, `task` in composition order), `context-forms.yaml` (`closed-set`: `pointer`, `read-in-full`, `bounded-index`, `runtime-discovery`, `inline-digest`), and `context-classes.yaml` (`mapping`: each layer to its ordered class ids — the eighteen-class roster); each carries `fact`, `kind`, `statement`, `consumers` (the engine and the declarations guard) and an empty `former_carriers`, and defines no numeric bound (FR-002, FR-003, FR-004, FR-009, FR-018, C-010, C-013).
- [ ] T015 [US1] [blockedBy:T014] Append the four registration keys to `shared/declarations/contract.yaml` as one append-only flat block after the 093/105 precedent — `context-categories:`, `context-layers:`, `context-forms:` and `context-classes:`, each pointing at its `shared/declarations/facts/<slug>.yaml` — before any consumer reads them, leaving every existing key untouched (FR-018, C-010).
- [ ] T016 [US1] [blockedBy:T014] Author the owner document model half in `shared/definitions/context-management-definitions.md`: the umbrella term and bilingual definition sites [[STR-001]]…[[STR-006]], the membership test stated once, the two categories derived from the layer (never a layout column), the three layers by owner location, the five materialization forms with the legality matrix, the layer landing contract (three legal cells each with definition, carriers, allowed forms by reference and content-versus-pointer rule; the three forbidden combinations named outside every row), the presence vocabulary defined once (positive `present` plus the four absence tokens) with the `Unobserved` reading reaching `shared/declarations/facts/evidence-seven-states.yaml#/statement` by pointer, the four-neighbour boundary table by pointer, and the red lines (no persistence, no replacement of existing owners, no new command, gate or watcher) (FR-001, FR-002, FR-003, FR-005, FR-009, FR-011, FR-020, FR-029, C-001, C-002, C-003, C-006, C-014).
- [ ] T017 [US1] [blockedBy:T016] Author the owner document projection half in `shared/definitions/context-management-definitions.md`: the single machine-parsed layout table with the fixed six columns `class id | layer | form | source | owner | cap reference` and all eighteen seed rows in layer order (system 4, project 7, task 7; cap references as `<path> § <section>` pointing at `shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) where the form is capped, never a numeric value), plus the baseline composition protocol (composed once at session or line entry by the root session; system-layer discovery and constraint pointers; project-layer `read-in-full` governance pointers with zero copied bytes and pointer or bounded-index rows; session versus line definitions; no invariant content restated) (FR-004, FR-006, FR-007, FR-012, FR-019, C-004, C-020).
- [ ] T018 [US1] [blockedBy:T015,T017] Implement the engine foundation and `--action manifest` in `scripts/python/context-audit.py`: the script-interface surface (`-h` and `--help` identical bodies, the runtime-derived `--version` through `scripts/python/script_interface_cli.py` with `unknown` an allowed form, undeclared options rejected with exit 2 before any action including after a bare `--`), the two-root resolution (workspace root from `--workspace-root` or the nearest `.specify/` ancestor; layer root the audited tree's own declaration layer — `<workspace-root>/shared/` when the framework-source layer is present, else `<workspace-root>/.specify/shared/` — with no fallback), declaration reads through `declaration_reader.load_fact` only, the layout-table parser with header validation, the presence reading that consumes only resolvable, readable and empty metadata plus the three stdlib no-side-effect probes (`platform`, `path-tools`, `fs-access`) and prints `present` or one of the four absence tokens with a reason in declared source order, and `--action manifest --layer <system|project|task>` in text and `--json` (ordered keys `action`, `layer`, `rows` with `class`, `layer`, `form`, `sources`, `token`, `reason`, `cap`; `counts`; `source_reading`; the roster row set with missing-layout rows reading `not-evaluated`; one `source-reading: <digest>` tail line over `(class id, workspace-relative resolved path, presence token, file size or directory entry count, mtime_ns)` tuples); exit 0 or 2 only, no writes, no sockets, no host values or timestamps, no content reads (FR-006, FR-007, FR-011, FR-020, FR-021, FR-022, FR-024, C-012, C-030, C-031, C-033).
- [ ] T019 [US1] [blockedBy:T018] Run the mirror flow for the new sources: `python3 scripts/python/sync-mirrors.py --write` to project `shared/` and `scripts/` into `.specify/shared/` and `.specify/scripts/`, then `--check` with no NEW drift against the 2026-11-27 baseline recorded in `test-evidence/mirror-baseline-plan.txt`; confirm the installed copy `.specify/scripts/python/context-audit.py` answers `--version` and that the installed owner document and four facts are byte-identical to their sources (FR-023, C-036).
- [ ] T020 [US1] [blockedBy:T018,T019] Verify the US1 baseline slice through the single entry: run the owner guard's model and baseline legs (definition sites, categories, layers, forms, landing cells, presence vocabulary, boundary table, baseline-once protocol), the declarations guard's fact-shape and registration legs, and the engine guard's manifest legs on the all-present fixture (system and project layers, governance pointers canonical, zero copied content) plus the byte-identical rerun; capture command, output and exit status in `test-evidence/us1-green.txt` and open the red-first slots in `notes/red-first-evidence.md` [green: contracts/owner-and-layout.contract.md#C-001] [green: contracts/owner-and-layout.contract.md#C-002] [green: contracts/owner-and-layout.contract.md#C-003] [green: contracts/matrix-and-triggers.contract.md#C-020] [green: contracts/engine-and-distribution.contract.md#C-030] [green: contracts/engine-and-distribution.contract.md#C-031]

**Checkpoint**: US1 独立可测 — the model, the value domains and the baseline manifest reading are green; the invariant baseline composes once and carries zero copied governance text.

---

## Phase 4: User Story 2 - 可变层逐任务选择 (Priority: P1)

**Goal**: The variable layer's protocol and its machine check land: task rows compose per task within owner-declared caps, invariant sources are cited by pointer only, the two `inline-digest` rows keep standing witnesses, and the audit's `check` action enforces the roster, the matrix, the caps and the landing contract.

**Independent Test**: On this repository `check` exits 0 with zero findings; the nine seeded-violation fixtures each produce exactly their expected finding and exit code; the declarations guard is fully green (closed sets, registration, member exercise, unknown-member refusal); and the task-layer manifest rows print in roster order with cap references and the two standing witnesses, while two task compositions share identical invariant rows and differ only in task relevance (the selection itself belongs to the composing agents, never to the engine).

### Tests for User Story 2 (MANDATORY)

> This story's legs are the layout, roster and landing legs plus the task-composition protocol legs of `tests/contract/test_context_management_owner.py`, the full `tests/contract/test_context_management_declarations.py`, and the full `tests/contract/test_context_management_engine.py`; all were authored red-first in Phase 2.

### Implementation for User Story 2

- [ ] T021 [US2] [blockedBy:T020] Extend the owner document in `shared/definitions/context-management-definitions.md` with the variable-layer protocol: task composition at `task-entry`, `task-switch` and `pre-dispatch` (selection by task scope and keywords, invariant sources cited by pointer only, caps by reference and never widened, discard at task end), the task-row meanings including the two `inline-digest` standing witnesses (`task-statement` → `shared/workflow/user-input-protocol.md`; `task-delta` → `.specify/register.md` plus `.specify/state/`), and the two decidable duplication shapes (a task row `read-in-full` over an invariant-declared source; a task row `inline-digest` over a source an invariant row materializes `read-in-full`) with the remaining cases left to review (FR-008, FR-010, FR-013, FR-019, C-021, C-027).
- [ ] T022 [US2] [blockedBy:T021] Implement `--action check` in `scripts/python/context-audit.py`: the closed nine-rule set (`roster-mismatch`, `roster-order`, `unknown-layer`, `unknown-form`, `layer-form-illegal`, `duplicate-class`, `empty-layer` naming the side and layer, `cap-missing`, `category-column` judged by the header alone), findings naming file, row and rule, the layout-token-is-a-finding versus declaration-member-is-exit-2 boundary, and exit 0 clean, 1 findings, 2 usage, unreadable input or unknown or missing declaration member; deterministic output, no ranking and no content reads (FR-009, FR-018, FR-019, FR-021, FR-022, C-013, C-015, C-016, C-032, C-034).
- [ ] T023 [US2] [blockedBy:T022] Re-run `python3 scripts/python/sync-mirrors.py --write` then `--check` after the owner-document and engine edits; confirm no NEW drift against `test-evidence/mirror-baseline-plan.txt` and byte-identical mirrors for the owner document, the four facts and the engine (FR-023, C-036).
- [ ] T024 [US2] [blockedBy:T022,T023] Verify the US2 layer slice through the single entry: run the owner guard's layout, roster, landing and task-composition legs, the full declarations guard, and the full engine guard (clean repository check, the nine seeded-violation fixtures, the declaration-error fixtures, manifest task-layer rows with caps and the two inline-digest witnesses, absence tokens, JSON shape, determinism, honesty); capture command, output and exit status in `test-evidence/us2-green.txt`, and confirm the two-task manifest comparison described in the Independent Test [green: contracts/owner-and-layout.contract.md#C-004] [green: contracts/owner-and-layout.contract.md#C-005] [green: contracts/owner-and-layout.contract.md#C-006] [green: contracts/declarations-and-domains.contract.md#C-010] [green: contracts/declarations-and-domains.contract.md#C-011] [green: contracts/declarations-and-domains.contract.md#C-012] [green: contracts/declarations-and-domains.contract.md#C-013] [green: contracts/declarations-and-domains.contract.md#C-014] [green: contracts/declarations-and-domains.contract.md#C-015] [green: contracts/declarations-and-domains.contract.md#C-016] [green: contracts/matrix-and-triggers.contract.md#C-021] [green: contracts/engine-and-distribution.contract.md#C-032] [green: contracts/engine-and-distribution.contract.md#C-033] [green: contracts/engine-and-distribution.contract.md#C-034] (FR-004, FR-008, FR-009, FR-010, FR-013, FR-019, FR-020, FR-021, FR-022, FR-028).

**Checkpoint**: US2 独立可测 — the task layer's declared rows, caps and standing witnesses are machine-checked, and every closed value domain is exercised or refused.

---

## Phase 5: User Story 3 - 客户项目经 init 获得它：离线且诚实 (Priority: P1)

**Goal**: A downstream project receives the owner document, the four facts and the engine through the existing publish → install → init flow with no extra step; the framework map names the three entries; a fresh project under blocked sockets runs both actions, reads genuine absences honestly and transmits nothing.

**Independent Test**: A fresh project initialized through the repository's own init path, with sockets blocked in process, carries the owner document, the four facts and the engine under `.specify/`; `check` exits 0 and `manifest --layer project` prints explicit absence lines at exit 0; zero sockets open and nothing is transmitted; the readonly guard's per-action hash manifests are identical with zero new files.

### Tests for User Story 3 (MANDATORY)

> This story's legs are `tests/integration/test_context_management_init.py::test_fresh_init_distributes_and_audits_offline` and the full `tests/contract/test_context_management_readonly.py`; both were authored red-first in Phase 2.

### Implementation for User Story 3

- [ ] T025 [US3] [blockedBy:T024] Edit `shared/definitions/framework-map.md` to add exactly three resolvable rows: the owner document `shared/definitions/context-management-definitions.md`; the four context value-domain facts as one directory entry `shared/declarations/facts/` naming the four `context-*.yaml` files; and the audit entry `scripts/python/context-audit.py` with its documented invocation (`--action check` and `--action manifest --layer <system|project|task>`); no other map row changes (FR-023, C-036).
- [ ] T026 [US3] [blockedBy:T025] Regenerate and verify the distribution mirrors: `python3 scripts/python/sync-mirrors.py --write` then `--check` with no NEW drift against the baseline; confirm the `specify init` flow copies the `shared/`, `scripts/` and `templates/` trees without any init-code change, and that `.specify/shared/definitions/framework-map.md` carries the three new rows (FR-023, C-036).
- [ ] T027 [US3] [blockedBy:T026] Verify the US3 distribution slice through the single entry: run `test_fresh_init_distributes_and_audits_offline` (fresh project through the repository's own init path, sockets blocked; owner document, facts and engine present; `check` exit 0; `manifest --layer project` absence lines; zero sockets and no transmission) and the full readonly guard (hash-manifest containment for both actions, zero new files, socket guard); capture command, output and exit status in `test-evidence/us3-green.txt` [green: contracts/engine-and-distribution.contract.md#C-035] [green: contracts/engine-and-distribution.contract.md#C-036] (FR-023, FR-024).

**Checkpoint**: US3 独立可测 — distribution rides the existing flow, the fresh tree audits honestly offline, and every reading is contained.

---

## Phase 6: User Story 4 - 主动触发与具名组合角色 (Priority: P2)

**Goal**: Composition stops being accidental: the closed trigger set, the composer roles, source drift, reentry and the dispatch mapping land in the owner document, and one ambient instructions section carries the three rules into every session within the generator's existing budget.

**Independent Test**: The owner guard's trigger, role, reentry, source-drift, dispatch-mapping and concept-pointer legs are green; a declared source's metadata change moves the `source-reading` digest while a task-only change leaves the baseline rows untouched; the ambient section appears verbatim in the template, the regenerated live file and therefore the symlinked tool files, and the generator's `BUDGET:` line reads `within`.

### Tests for User Story 4 (MANDATORY)

> This story's legs are the protocol, slot, dispatch-mapping and ambient legs of `tests/contract/test_context_management_owner.py`, the source-reading drift legs of `tests/contract/test_context_management_engine.py`, and `tests/integration/test_context_management_init.py::test_fresh_init_instructions_carry_the_ambient_section`; all were authored red-first in Phase 2.

### Implementation for User Story 4

- [ ] T028 [US4] [blockedBy:T027] Extend the owner document in `shared/definitions/context-management-definitions.md` with the composition protocol remainder: the closed seven-trigger set (`session-entry`, `task-entry`, `task-switch`, `pre-dispatch`, `stage-boundary`, `source-drift`, `reentry`) each naming composer, scope and evidence; the composer roles resolved through `shared/definitions/superagent-definitions.md` (root session, superagent, dispatched executor with no re-gathering); `source-drift` as an observed record change triggering exactly one baseline refresh with no watcher or poll; `reentry` as baseline re-citation by pointer (recomposition only when a baseline-refresh trigger also fired) plus `task-delta` refresh and the recorded re-anchoring statement; the dispatch mapping onto the existing seven role fields (including `authority_ref`), four injections and uplink return with nothing added; and the concept-pointer slot (glossary, definitions and explanations triple; four governed structures; per-structure carrier and named presence surface; absence reading `Unobserved`, never `present`) (FR-005, FR-012, FR-014, FR-015, FR-016, FR-017, FR-028, C-007, C-022, C-023, C-024, C-025, C-026, C-028).
- [ ] T029 [US4] [blockedBy:T028] Append the ambient section `## Context Management(上下文管理)` to `templates/instructions-template.md` in summary-plus-pointer shape: baseline-once and task-per-selection, pointer-not-content, absence-names-the-gap; pointing at `shared/definitions/context-management-definitions.md` and the audit entry; carrying no layout table, no class roster and no cap literal, and fitting the generator's existing budget headroom (measured 789 B; the constant is neither raised nor are existing sections trimmed) (FR-025, C-037).
- [ ] T030 [US4] [blockedBy:T029] Regenerate the live instructions with `bash scripts/bash/generate-instructions.sh` and verify its `BUDGET:` line reads `within` under the unchanged constant; run `python3 scripts/python/sync-mirrors.py --write` then `--check` with no NEW drift; confirm the section appears verbatim in `templates/instructions-template.md`, `.specify/templates/instructions-template.md` and `.specify/instructions.md` (and therefore in the symlinked tool files) with pointer shape intact; if the section does not fit, surface the anomaly instead of raising the budget or trimming sections (FR-025, C-037).
- [ ] T031 [US4] [blockedBy:T030] Verify the US4 trigger slice through the single entry: run the full owner guard (trigger set, composer roles, reentry, source-drift legs including the source-reading digest change, dispatch mapping, concept-pointer slot and structure legs, protocol-boundary leg, ambient template and live and pointer-shape legs), the engine guard's source-reading drift legs, and `test_fresh_init_instructions_carry_the_ambient_section`; capture command, output and exit status in `test-evidence/us4-green.txt` [green: contracts/owner-and-layout.contract.md#C-007] [green: contracts/matrix-and-triggers.contract.md#C-022] [green: contracts/matrix-and-triggers.contract.md#C-023] [green: contracts/matrix-and-triggers.contract.md#C-024] [green: contracts/matrix-and-triggers.contract.md#C-025] [green: contracts/matrix-and-triggers.contract.md#C-026] [green: contracts/matrix-and-triggers.contract.md#C-027] [green: contracts/matrix-and-triggers.contract.md#C-028] [green: contracts/engine-and-distribution.contract.md#C-037] (FR-012, FR-014, FR-015, FR-016, FR-017, FR-025, FR-028).

**Checkpoint**: US4 独立可测 — composition has named triggers and composers, reentry re-cites without recomposing, and every session receives the ambient three-rule summary inside budget.

---

## Phase 7: User Story 5 - 一次只读审计读数 (Priority: P3)

**Goal**: The audit reading becomes credible and closing: the seeded violations are exact, reruns are byte-identical, the concept-pointer rows are honest under deletion and unreadability, the mutation drill proves each guard would catch its rule's removal, and the full-suite and containment claims close the feature.

**Independent Test**: On this repository `check` exits 0 with zero findings and two runs are byte-identical; each of the nine rule fixtures produces exactly its expected finding at exit 1; the concept-missing fixture prints the deleted row `not-evaluated` with the missing-layout-row reason, the unreadable row `unreachable`, and `Unobserved` for the derived consistency reading; the mutation drill shows a red guard verdict per rule; the full suite shows zero NEW failures and the protected surfaces equal their pre-change captures.

### Tests for User Story 5 (MANDATORY)

> This story's evidence comes from the full `tests/contract/test_context_management_engine.py` and `tests/contract/test_context_management_readonly.py`, both authored red-first in Phase 2, plus the mutation drill executed here.

### Implementation for User Story 5

- [ ] T032 [US5] [blockedBy:T031] Run the audit reading battery: `context-audit.py --action check` on this repository (exit 0, zero findings) and on the four SC-001 fixtures plus the remaining rule fixtures (exact findings and exit codes, the merged layer-form fixture yielding exactly two), the declaration-error fixtures (exit 2, no partial verdict), byte-identical reruns per unchanged tree, and the JSON key-order and content-equality legs; capture commands, outputs and exit codes in `test-evidence/audit-fixtures.txt` and `test-evidence/determinism.txt` (FR-022).
- [ ] T033 [US5] [blockedBy:T032] Run the concept-pointer presence battery: on this repository `manifest --layer project` lists `project-vocabulary`, `concept-definitions` and `concept-explanations` each reading `present` with resolvable sources; on the concept-missing fixture the manifest still prints the deleted row (the row set is the roster) reading `not-evaluated` with the missing-layout-row reason, the unreadable-source row reads `unreachable`, the affected structure's consistency reading is `Unobserved`, and no output reports agreement or `present`; the fixture's `check` roster-mismatch reading (exit 1) may co-occur without changing the manifest exit; capture in `test-evidence/concept-presence.txt` (FR-020, FR-028).
- [ ] T034 [US5] [blockedBy:T033] Execute the mutation drill: for each of the nine `check` rules, disable only that rule in a scratch copy of the engine, run that rule's guard test and require it to go red, then restore; capture the per-rule command, real output and exit status in `test-evidence/mutation-drill.txt`, and prove the working engine is byte-identical to its pre-drill state (`git diff` empty) — the observable is the guard test's verdict, not the engine's finding output [green: contracts/guards-and-boundaries.contract.md#C-040] (FR-027).
- [ ] T035 [US5] [blockedBy:T034] Run the full suite through `scripts/bash/run-tests.sh`, capture the complete failure-name list and compare it with the implement-entry baseline (path and flag owned by the implement **Test runs** bullet, referenced not restated); assert zero NEW failures, mirrors byte-identical, and the three protected surfaces equal to `notes/pre-change-measurements.md` (the super↔sub protocol's declared item set, the `memory-utils.py --action recall` output on the populated stores, the rendered-agent fixture output); capture in `test-evidence/full-suite.txt` [green: contracts/guards-and-boundaries.contract.md#C-041] (FR-027).
- [ ] T036 [US5] [blockedBy:T035] Close the guard convergence and the final changed-set audit: re-run all five guard files green; demonstrate from the same runs the concept-pointer and protocol-boundary guard, the layer-landing guard and the member-exercise legs; compare the changed-path set against the declared fan-out (owner document, four facts, four registration keys, engine, five guard files and fixtures, ambient template section plus its generated copies, three framework-map rows, mirrors, and this spec's records) with an empty complement; assert no new `/speckit.*` command, skill wrapper, gate, red line, store, cache or network path and an unchanged runtime-store roster; capture in `test-evidence/guard-convergence.txt` and `test-evidence/changed-set.txt` [green: contracts/matrix-and-triggers.contract.md#C-029] [green: contracts/guards-and-boundaries.contract.md#C-042] [green: contracts/guards-and-boundaries.contract.md#C-043] [green: contracts/guards-and-boundaries.contract.md#C-044] [green: contracts/guards-and-boundaries.contract.md#C-045] [green: contracts/guards-and-boundaries.contract.md#C-046] (FR-005, FR-011, FR-017, FR-022, FR-024, FR-026, FR-027, FR-028, FR-029).

**Checkpoint**: US5 独立可测 — the audit's rules, determinism, concept presence and guard credibility are all evidenced by captured readings and a per-rule mutation drill.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Execute the documented scenarios end to end, close the cap and mirror scans, and assemble the verification input.

- [ ] T037 [blockedBy:T036] Execute every quickstart scenario in `.specify/specs/110-context-management/quickstart.md` exactly as written (scenarios 1–6, with the existing-carrier reads re-taken) and record command, real output, exit status and teardown per scenario in `.specify/specs/110-context-management/notes/quickstart-run.md`; the init scenario runs through the repository's own init path (the installed 0.0.22 build predates this feature).
- [ ] T038 [blockedBy:T037] Run the cap and mirror closure scans: every `bounded-index` row's cap reference resolves to `shared/guidelines/token-efficiency.md` § 摘要优先(Summary-First) (path plus section), the four facts carry no numeric bound field, no new numeric cap literal sits beside a cap unit in this feature's artifacts, and `python3 scripts/python/sync-mirrors.py --check` shows no NEW drift; capture in `test-evidence/cap-scan.txt` and `test-evidence/mirror-final.txt` (FR-019, FR-023).
- [ ] T039 [blockedBy:T038] Assemble `test-evidence/verification-input.md`: one status row per success criterion (SC-001…SC-011) with value, command and evidence pointer; the `final`-path criteria read `pass` and the single smoke record carries `smoke_command=`, `smoke_exit_code=0` and an existing non-empty `smoke_evidence_path=`; consolidate `notes/red-first-evidence.md`; record any deferred task as `[~]` with its inline reason (expected none) — `verification.md` is derived spec-side from this input under the implement command (condition-set owner: `shared/workflow/acceptance-hardening.md` § Gates).

**Checkpoint**: every documented scenario has a real run record; the cap and mirror scans are empty; the verification input is ready to be derived into `verification.md`.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies.
- **Foundational (Phase 2)**: depends on Setup's evidence landing points; blocks every story's implementation rows.
- **US1 (Phase 3)**: depends on Foundational (guard files red) — the MVP increment.
- **US2 (Phase 4)**: depends on US1's verification (same owner document, same engine, same mirror flow).
- **US3 (Phase 5)**: depends on US2 (framework map edit + final distribution of the settled sources).
- **US4 (Phase 6)**: depends on US3 (the ambient template edit rides the already-verified mirror flow).
- **US5 (Phase 7)**: depends on US4 (all sources final before the mutating drill, full suite and changed-set audit).
- **Polish (Phase 8)**: depends on US5.

### User Story Dependencies

- **US1 (P1)**: the smallest independently testable increment — model, value domains, engine manifest; MVP.
- **US2 (P1)**: immediately follows; adds the variable-layer protocol and the `check` action.
- **US3 (P1)**: distribution and offline honesty; needs the engine's actions final.
- **US4 (P2)**: triggers, roles, reentry and the ambient section; depends on the settled model and mirror flow.
- **US5 (P3)**: audit credibility and the closing claims; depends on every source edit being final.

### Within Each User Story

- Guard files precede implementation (authored red in Phase 2).
- The owner document and the engine are shared write targets and are edited sequentially by row order.
- Each story's verification row holds that story's `[green:]` claims; test-authoring rows hold none.
- US5's mutating drill runs only after all source edits are final, and its restore step is proven byte-identical.

### Parallel Opportunities

- The Setup captures T002, T003 and T005 write disjoint evidence files and may run together; T004 follows T003 so both records carry the same mirror and toolchain readings.
- The five guard authoring rows T009–T013 write disjoint files and may run together.
- Everything else is serial: one engine file, one owner document, one verification sink per story.

---

## Parallel Example: Foundational guard authoring

```bash
# Launch the five guard-file authoring rows together (disjoint write targets and red sinks):
Task: "Author tests/contract/test_context_management_owner.py (red sink test-evidence/red-owner.txt)"
Task: "Author tests/contract/test_context_management_declarations.py (red sink test-evidence/red-declarations.txt)"
Task: "Author tests/contract/test_context_management_engine.py (red sink test-evidence/red-engine.txt)"
Task: "Author tests/contract/test_context_management_readonly.py (red sink test-evidence/red-readonly.txt)"
Task: "Author tests/integration/test_context_management_init.py (red sink test-evidence/red-init.txt)"
```

---

## Implementation Strategy

### MVP First

**MVP scope**: US1 alone — the smallest same-priority set whose checkpoint is independently testable: the model, the four closed value domains, the owner document with the machine-parsed layout table, and the engine's manifest reading. US2 and US3 are the immediate P1 increments; US4 completes the composition protocol; US5 certifies the whole.

1. Complete Setup and Foundational (fixtures + five red guard files).
2. Complete US1 → verify the baseline manifest and model legs.
3. **STOP and VALIDATE**: run the US1 independent test exactly as written.
4. Deliver US2, then US3, then US4, then US5, then Polish.

### Incremental Delivery

1. Setup → every pre-change reading frozen.
2. Foundational → every guard file observed red.
3. US1 → the model and the baseline manifest (MVP).
4. US2 → the variable layer and the check action.
5. US3 → distribution and offline honesty.
6. US4 → triggers, roles and the ambient section.
7. US5 → audit credibility and the closing claims.
8. Polish → quickstart run record, cap and mirror scans, verification input.

### Parallel Team Strategy

Single execution body (this line is `single-unit`). If later split: only the Setup captures and the guard-authoring rows are partitionable; the owner document, the engine, the mirrors and each story's verification sink are never written by two executors at once.

---

## Notes

- **PLAN-EDIT**: none. No plan-owned path is edited; the contracts, quickstart, data-model, research and feature-ref are read-only references. A substantive change to a plan-owned path during implementation is an anomaly to surface, not a silent edit.
- **Red-first partition**: all five guard files are authored before any implementation row (C-040's "authored before the implementation"); the story phases carry implementation plus the clause-green verification rows.
- **Green partition**: all 39 clauses are claimed exactly once, monotonically per contract by row order; the test-authoring rows carry no tags, so no clause collides and no test path is claimed green at two points.
- **Measurement traps**: the clause unit is the `## C-NNN` definition heading (in-body references inflate the naive count to 54); the instructions headroom is 40960 − 1 − 40170 = 789 B and the generator's `BUDGET:` line is the only judge; deliverable-path advisories from the stage gate are expected until implementation creates the paths.
- **Single engine, single owner document**: every engine edit lands in `scripts/python/context-audit.py`; every model edit lands in `shared/definitions/context-management-definitions.md`; mirrors are generated and never hand-edited.
- **No store, no migration**: the mechanism is read-only; the runtime-store roster is unchanged; the only durable additions are the declared set in DoD-2.
- **Test budget**: targeted sets run first through `scripts/bash/run-tests.sh`; the full suite runs once at T035 against the implement-entry baseline. `SPECKIT_PYTHON=/usr/local/bin/python3` is fixed in § Environment Prerequisites.
- **Anomaly discipline**: a section that cannot fit the instructions budget, or any premise measured differently at implement entry, is surfaced as an anomaly — never repaired by raising a budget, trimming sections or muting a guard.