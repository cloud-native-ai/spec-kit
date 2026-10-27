# Tasks: Review 命令与代码评审技能的组合与治理 (Review × Code-Review Composition) — 071

**Requirement ID**: 071
**Requirement Key**: `071-review-code-integration`
**Branch**: `master` (no branch was created or switched by this line; see requirements Assumption A1)
**Related Feature**: Feature 071 — Review 命令与代码评审技能的组合与治理, status `Planned` (the tasks stage adds no new status value — the canonical state machine's vocabulary is `Draft | Planned | Implemented | Ready for Review | Completed`)
**Input**: Design documents from `.specify/specs/071-review-code-integration/`
**Prerequisites**: `plan.md` (required), `requirements.md` (required; 28 FR / 7 SC, 5 user stories), `research.md` (R1–R14 + DR1), `data-model.md` (E1–E13, V1–V28), `contracts/` (6 files, 73 clauses), `quickstart.md` (scenarios A–H), `feature-ref.md`

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating ("Critical flows MUST have automated regression coverage; Integration/contract tests MUST cover …"), and the feature carries one executable artifact (`skills/internal/code-review/scripts/git-delta-review.sh`) whose new subcommands are pure deterministic behaviour. The Principle VII "Template-only features" gate applies to the template/prompt/document surfaces only: those are judged by **structural contract tests** (content, path, and mirror-parity assertions), never by unit or integration tests. Both layers are emitted, one test file per contract document.

**Tests**: Every new-behaviour row is red-first and records its failing command, real output, and exit code in `notes/red-first-evidence.md`. The six new contract groups are authored once, against the unchanged tree, after the shared temporary-repository fixture exists (T003). Regression nets — the neighbouring-suite re-runs (T027, T035, T036) and the pin update (T030) — exercise behaviour that already exists or that fully lands before they run, so they carry explicit `[blockedBy:]` instead of a red-first claim (the create-tasks migration/regression exception).

**Organization**: Rows are grouped by the five user stories of `requirements.md`. US1 and US2 are both P1 and together form the MVP: a composed command whose review object cannot be resolved is not an independently valuable increment, so both close before any P2 story starts. Setup, Foundational, and Polish rows carry no story label. The `[green:]` tags partition the 73 contract clauses so every clause is claimed by exactly one row and the clause order ascends with the row order (§ Clause Partition).

## Definition of Done (DoD)

- DoD-1: Every row is `[X]`, or `[~]` with its reason recorded in `.specify/specs/071-review-code-integration/verification.md` under `deferred_tasks=`.
- DoD-2: All 73 contract clauses are claimed exactly once by a `[green:]` row, and `account-clause-coverage.py` reports the full claimed count with zero names beyond the frozen baseline.
- DoD-3: The six new contract groups exist, were red-first, and are green; the five neighbouring suites show no NEW failures by name against the implement-start baseline, and the mirror pairs show no NEW drift against the T001 measurements.
- DoD-4: The one intentional pin change (`test_review_p1_review_loop.py::test_c15_…`) lands in the same commit as the convergence edit that removes the wording it quotes, keeps its subject, and increases the assertion count.
- DoD-5: `verification.md` records a `SC-NNN_status=` row for every Success Criterion in `requirements.md`, drawn from the status vocabulary owned by `.specify/templates/verification-log-template.md`.
- DoD-6: No plan-owned artifact is rewritten without a front-loaded `PLAN-EDIT: <path> — <reason>；分类=minor|substantive` declaration, and no substantive plan edit is made by the implementation run.
- DoD-7: No push, no force merge, no hand-edited runtime projection, and no new command, skill, agent, dependency, external service, resident process, or second feedback store.

**DoD Status**: pending — every row is open; `verification.md` does not exist yet.

## Completion Gate

- GATE-1: Task-file structure is valid — check: `python3 scripts/python/validate-tasks.py .specify/specs/071-review-code-integration/tasks.md` exits 0.
- GATE-2: Cross-artifact consistency holds — check: `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/071-review-code-integration --stage tasks --repo .` reports `decision=pass` with `errors=0`. At generation time it reported 42 `missing-path` advisories, and every one names a deliverable this file creates: the six new contract test files and `tests/fixtures/review_git_repo.py`. The advisories disappear as the implementation creates those paths; a `missing-path` advisory for any OTHER path is a defect, not an expected state.
- GATE-3: The decomposition size gate passes — check: `python3 .qoder/skills/sdd-loop-driver/scripts/decomposition-check.py --mode tasks --requirements .specify/specs/071-review-code-integration/requirements.md --tasks .specify/specs/071-review-code-integration/tasks.md` reports `decision=proceed` with a row count at or below the ceiling of 40.
- GATE-4: The six new contract groups are green — check: `python3 -m pytest -q tests/contract/test_review_code_composition.py tests/contract/test_code_review_skill_contract.py tests/contract/test_coverage_receipt.py tests/contract/test_status_gate_owner.py tests/contract/test_review_feedback_boundary.py tests/contract/test_review_docs_isomorphism.py`.
- GATE-5: No NEW test failure by name — check: `comm -13 .specify/specs/071-review-code-integration/baseline-failed.txt <current failing-name list>` returns empty; the capture flag and comparison form are owned by `/speckit.implement` step 6's `**Test runs**` bullet.
- GATE-6: Clause coverage is complete — check: `python3 scripts/python/account-clause-coverage.py .specify/specs/071-review-code-integration` reports the claimed-clause count equal to the contract set and `uncovered beyond baseline: 0`, exit 0.
- GATE-7: Mirrors are clean — check: `python3 scripts/python/sync-mirrors.py --check --only templates`, `--only skills/internal`, `--only shared`, and `python3 scripts/python/regen-command-copies.py --check` each report `ok` / `OK` with no NEW drift against the T001 baselines.
- GATE-8: No unfinished rows remain — check: `grep -cE '^- \[[ >]\]' .specify/specs/071-review-code-integration/tasks.md` returns 0.

## Environment Prerequisites

This is the single landing point for every environment verdict in this file; any row that needs one references this section instead of restating it.

- Python / pytest: **available** — probe: `python3 --version` → `Python 3.11.11`; `python3 -m pytest --version` → `pytest 8.4.2` @ 2026-10-27; affected: every test and validator row.
- Shell / git: **available** — probe: `bash --version` → `GNU bash, version 4.4.20(1)-release`; `git --version` → `git version 2.43.5` @ 2026-10-27; affected: T003, T011, T012, T015, T017, T018, T034.
- Renderer `delta`: **available on this host** — probe: `command -v delta` → `/home/agent/.cargo/bin/delta` @ 2026-10-27. The absent-renderer path is *not* probed by removing it from `PATH`; it is exercised deterministically by pointing the script's own `DELTA_BIN` at a non-existent binary, so the text-mode behaviour stays testable on a host that has the renderer. Affected: T014, T015, T018.
- Container runtime / image registry / live cluster / network / special hardware: **none required** — the whole feature is local files, local git, and local pytest; affected: none.
- Mirror baselines: **clean** — probe: `sync-mirrors.py --check --only templates` → `ok (22 files)`; `--only skills/internal` → `ok (136 files)`; `--only shared` → `ok (55 files)`; `regen-command-copies.py --check` → `OK: all per-tool command copies match the source templates.` @ 2026-10-27; the acceptance criterion is therefore "no NEW drift", never an absolute green. Affected: T032, T033.

## Format: `[ID] [P?] [Story] Description` (see § Environment Prerequisites for environment verdicts)

- **[P]**: can run in parallel with the other `[P]` rows in the same phase — different write targets, no unfinished dependency.
- **[Story]**: `[US1]`…`[US5]`; required on every row inside a User Story phase and forbidden in Setup, Foundational, and Polish.
- **[blockedBy: T001,T002]**: this row MUST NOT start until every listed task is `[X]`.
- **[green: <contract>#<clause>]**: this row is the one that turns that contract clause green. The tag's surface definition is owned by `.specify/templates/tasks-template.md` § Format and its machine checks by `scripts/python/validate-tasks.py`; this file only declares claims. A row may carry several; the partition below keeps each clause on exactly one row.
- Every row names its concrete file path; every test row names the file it writes and the evidence sink it appends to.

## Clause Partition

73 clauses, six contract files, each clause claimed by exactly one row. The clause order ascends with the row order inside each contract, so no earlier row is left claiming a contract green at its own phase.

| Contract file | Clauses | Claimed by | Clause band |
|---|---|---|---|
| `contracts/command-orchestration.md` | C-1…C-16 | T006 | C-1…C-8 |
| `contracts/command-orchestration.md` | — | T007 | C-9, C-10 |
| `contracts/command-orchestration.md` | — | T008 | C-11…C-16 |
| `contracts/code-review-skill.md` | C-17…C-30 | T013 | C-17…C-21 |
| `contracts/code-review-skill.md` | — | T016 | C-22…C-25 |
| `contracts/code-review-skill.md` | — | T017 | C-26, C-27 |
| `contracts/code-review-skill.md` | — | T018 | C-28 |
| `contracts/code-review-skill.md` | — | T031 | C-29 |
| `contracts/code-review-skill.md` | — | T035 | C-30 |
| `contracts/coverage-receipt.md` | C-31…C-44 | T015 | C-31…C-42 |
| `contracts/coverage-receipt.md` | — | T018 | C-43, C-44 |
| `contracts/status-gate-ownership.md` | C-45…C-54 | T020 | C-45, C-46 |
| `contracts/status-gate-ownership.md` | — | T021 | C-47, C-48 |
| `contracts/status-gate-ownership.md` | — | T022 | C-49…C-53 |
| `contracts/status-gate-ownership.md` | — | T023 | C-54 |
| `contracts/feedback-and-boundaries.md` | C-55…C-64 | T025 | C-55, C-56 |
| `contracts/feedback-and-boundaries.md` | — | T026 | C-57…C-59 |
| `contracts/feedback-and-boundaries.md` | — | T027 | C-60…C-63 |
| `contracts/feedback-and-boundaries.md` | — | T030 | C-64 |
| `contracts/tests-and-docs-sync.md` | C-65…C-73 | T029 | C-65, C-66 |
| `contracts/tests-and-docs-sync.md` | — | T030 | C-67 |
| `contracts/tests-and-docs-sync.md` | — | T031 | C-68 |
| `contracts/tests-and-docs-sync.md` | — | T032 | C-69 |
| `contracts/tests-and-docs-sync.md` | — | T033 | C-70 |
| `contracts/tests-and-docs-sync.md` | — | T034 | C-71 |
| `contracts/tests-and-docs-sync.md` | — | T035 | C-72 |
| `contracts/tests-and-docs-sync.md` | — | T036 | C-73 |

**Partition check**: 16 + 14 + 14 + 10 + 10 + 9 = 73; no clause appears on two rows and no row claims a clause from a later band. The engine of record is `python3 scripts/python/account-clause-coverage.py .specify/specs/071-review-code-integration` (its claimed-clause count must equal the contract set), not this table.

## Measured Premises (re-measured at tasks generation, 2026-10-27, HEAD `59f3bda6`)

| Premise | Re-derivation command | Real output |
|---------|-----------------------|-------------|
| FR definition rows | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/071-review-code-integration/requirements.md` | `28` |
| SC definition rows | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/071-review-code-integration/requirements.md` | `7` |
| User stories | `grep -cE '^### User Story' .specify/specs/071-review-code-integration/requirements.md` | `5` |
| Shared strings | `grep -cE '^\| `STR-[0-9]{3}`' .specify/specs/071-review-code-integration/requirements.md` | `4` |
| Contract clauses | `python3 scripts/python/clause_extract.py .specify/specs/071-review-code-integration/contracts/*.md` | 14 + 16 + 14 + 10 + 10 + 9 = `73`, every file `form=md-bold-closed`, `no_citation=[]` |
| Clause count — the trap form | `grep -oh 'C-[0-9]\{1,2\}' .specify/specs/071-review-code-integration/contracts/*.md \| wc -l` | `209` — this counts *mentions* (cross-references inside other clauses and traceability tables), not clause definitions; the unit of this measurement is a clause *definition*, and the correct answer is `73`. Recording both so a reader can tell the measurement was taken deliberately. |
| New test files absent as expected | `ls tests/contract/ \| grep -E 'review_code_composition\|code_review_skill_contract\|coverage_receipt\|status_gate_owner\|review_feedback_boundary\|review_docs_isomorphism'` | no output (all six absent; T004, T005, T010, T014, T019, T024 create them) |
| Existing skill script shape | `wc -l skills/internal/code-review/scripts/git-delta-review.sh skills/internal/code-review/SKILL.md` | `512` and `110` — the subcommands extend the existing entity (C-30) |
| Existing pin subject | `grep -n 'test_c15' tests/contract/test_review_p1_review_loop.py` | `177: def test_c15_review_owns_the_ready_for_review_transition():` (the row T030 updates), `186: def test_c15_checklist_row_is_annotated_and_keeps_one_transition_per_command():` (the annotation T021 must preserve), `200: def test_c15_top_command_list_includes_review():` (untouched) |
| Two disagreeing transition rows | `grep -rn 'Implemented → Ready for Review' templates shared` | `templates/feature-details-template.md` (owner, § Canonical Status State Machine), `shared/workflow/feature-integration.md:37` (checklist) and `:38` (review) — C-45…C-48 converge the two summary rows |
| Mirror baselines | `sync-mirrors.py --check` on three scopes + `regen-command-copies.py --check` | `ok (22 files)`, `ok (136 files)`, `ok (55 files)`, `OK: all per-tool command copies match` |
| Frozen coverage baseline | `python3 scripts/python/account-clause-coverage.py .specify/specs/071-review-code-integration --freeze > .specify/specs/071-review-code-integration/coverage-baseline.txt` | `rc=0`; 495 frozen names over 191 corpus files (`parsed 97 + named 94`), `base-sha: 59f3bda68e9c` — frozen at the tasks stage, i.e. at the first full-tree accounting for this feature, not at the first green one |
| Git snapshot | `git rev-parse HEAD`; `git status --short` | `59f3bda68e9cc42a215714bdd8d39c7b1982e908`; clean tree before this stage's commits |
| Plan task budget | `plan.md` § Task Budget | 30 planned steps against the 40-row ceiling; this file defines 36 rows (the split exists because the clause partition needs contiguous ascending bands, not because scope grew) |

## Test Budget (E2 / E3 / closure)

- **E2 baseline slot (implement start, exactly once)**: T002 captures the failing-test name list at `.specify/specs/071-review-code-integration/baseline-failed.txt`, using the capture flag and comparison form owned by `/speckit.implement` step 6's `**Test runs**` bullet. No other row re-captures it.
- **E3 stage-status rows (targeted evidence)**: T009, T013, T018, T023, and T028 append `targeted-set-v1` stage-status rows to `.specify/specs/071-review-code-integration/test-evidence/implement-stage-status.jsonl`. The tasks stage itself is documentation-only and already recorded its own `status=not-run-docs-only` row in `.specify/specs/071-review-code-integration/test-evidence/tasks.jsonl`.
- **Closure slot (after review)**: T036 runs the six new suites plus the five neighbouring suites once, compares failing names against the E2 baseline, and writes the SC matrix into `verification.md`. No other row runs a full suite.
- **Frozen plan baseline is not the E2 baseline**: `.specify/specs/071-review-code-integration/test-evidence/regression-baseline.txt` (18 passed for `test_expression_gates_doc.py`; 60 passed over the five neighbouring files, 2026-10-27) is a plan-stage pre-change measurement. The implementation criterion against it is **no NEW failure and no NEW drift**, not a green run, and T036 names the counts rather than assuming them.
- **No new full-suite cost claim**: this feature adds no suite-level run to a review execution (plan § Performance Goals); a review run's added work is one `git diff --numstat` plus one pass over the changed-file list.

## Mirror Obligations

The authoritative per-pair source/mirror/verify table is `plan.md` § Mirror Obligations — its sole owner; `feature-ref.md` § 6 only points there. This file lands the work as T032 (one write task for all rows, because they share the two generators) plus T033 (one verify task that enumerates every pair and is the only place the "no NEW drift" verdict is stated). `docs/` and `tests/` have no mirror. The probe registry is not edited, so no compiled closing face is regenerated.

## Requirement Coverage Map

Every FR and SC from `requirements.md` maps to at least one row; no requirement is left without a row.

| Requirement | Tasks | Requirement | Tasks |
|-------------|-------|-------------|-------|
| FR-001 | T004, T006 | FR-015 | T015, T016 |
| FR-002 | T004, T006 | FR-016 | T025, T028 |
| FR-003 | T006, T009 | FR-017 | T024, T025, T026 |
| FR-004 | T010, T011, T013 | FR-018 | T025, T026, T028 |
| FR-005 | T006, T015, T018 | FR-019 | T007, T008, T018 |
| FR-006 | T011, T013 | FR-020 | T008, T027, T035 |
| FR-007 | T006, T022 | FR-021 | T011, T012, T013, T015, T017 |
| FR-008 | T019, T020, T021, T022, T023, T030 | FR-022 | T011, T012, T013 |
| FR-009 | T022, T023 | FR-023 | T017, T023 |
| FR-010 | T007, T008, T012 | FR-024 | T016, T018 |
| FR-011 | T007, T018 | FR-025 | T031 |
| FR-012 | T008 | FR-026 | T003, T015, T035 |
| FR-013 | T014, T016, T018 | FR-027 | T027, T030, T034 |
| FR-014 | T014, T015, T018 | FR-028 | T004, T005, T010, T014, T019, T024, T029, T031, T033, T034 |

| Success Criterion | Tasks |
|-------------------|-------|
| SC-001 | T007, T008, T009 |
| SC-002 | T014, T015, T018 |
| SC-003 | T014, T016, T018 |
| SC-004 | T019, T020, T022, T023 |
| SC-005 | T005, T006, T027 |
| SC-006 | T029, T033, T036 |
| SC-007 | T024, T025, T026 |

## Test Deliverable Map

| Test file or fixture | Created by | Implementation it pins | Regression edge |
|---|---|---|---|
| `tests/fixtures/review_git_repo.py` | T003 | consumed by T010, T014 | T036 |
| `tests/contract/test_review_code_composition.py` | T004 | T006, T007, T008 | T036 |
| `tests/contract/test_review_docs_isomorphism.py` | T005 | T031 (docs page), T006, T008 | T036 |
| `tests/contract/test_code_review_skill_contract.py` | T010 | T011, T012, T016, T017 | T036 |
| `tests/contract/test_coverage_receipt.py` | T014 | T015 | T036 |
| `tests/contract/test_status_gate_owner.py` | T019 | T020, T021, T022, T030 | T036 |
| `tests/contract/test_review_feedback_boundary.py` | T024 | T025, T026, T027 | T036 |
| `tests/contract/test_review_p1_review_loop.py` | T030 (one pin updated) | T021 | T036 |

**Distribution**: Setup 2 · Foundational 1 · US1 6 · US2 4 · US3 5 · US4 5 · US5 5 · Polish 8 — 36 rows in total.

## Feature Registry Review

The breakdown exposes no new, merged, split, or invalidated Feature: all 36 rows stay inside Feature 071, and the row count is below the ceiling of 40. `.specify/memory/features.md` row 071 stays **Planned** (the status vocabulary has no tasks-side value), with the tasks-stage record appended to its `Last Updated` cell; `.specify/memory/features/071.md` gains the tasks-stage entry in § Latest Review and its § Status Tracking line names `tasks.md` as complete. The move to `Implemented` belongs to `/speckit.implement`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create the evidence sinks and freeze the dated controls every later "red-first" or "no NEW failure" claim is measured against.

- [ ] T001 [P] Create `.specify/specs/071-review-code-integration/notes/red-first-evidence.md` with a header naming the six new contract test files, and capture the pre-change measurements in `.specify/specs/071-review-code-integration/notes/pre-change-measurements.md`: `python3 --version`, `python3 -m pytest --version`, `bash --version`, `git --version`, the three `sync-mirrors.py --check` file counts, `regen-command-copies.py --check`, the five neighbouring-suite counts re-measured at implement start, `git rev-parse HEAD`, and `git status --short`. Test anchor: this dated note is the control for T033 and T036; evidence: `.specify/specs/071-review-code-integration/notes/pre-change-measurements.md`.
- [ ] T002 [P] Capture the implement-start failing-test baseline name list exactly once at `.specify/specs/071-review-code-integration/baseline-failed.txt`, using the capture command, the capture flag, and the name-level comparison form owned by `/speckit.implement` step 6's `**Test runs**` bullet (referenced, never restated here), and mark the row as the baseline slot in the line's test-budget ledger. Test anchor: the baseline name list; evidence: `.specify/specs/071-review-code-integration/baseline-failed.txt`.

**Checkpoint**: Two dated controls exist — the pre-change measurements and the failing-name baseline — so every later red/green and no-NEW-failure claim has a reproducible reference instead of an assertion.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build the one shared harness the deterministic script tests need before any story can write them.

- [ ] T003 Create `tests/fixtures/review_git_repo.py`: a helper that builds a throwaway git repository (an initial commit, a second commit that adds `.specify/specs/<key>/requirements.md` plus a code file, and an optional dirty working-tree hook), invokes `skills/internal/code-review/scripts/git-delta-review.sh` with an explicit working directory and `DELTA_BIN`, and parses the delimited receipt block into a name→value mapping plus ordered per-file rows; stdlib + `subprocess` only, test-only, and it never writes the framework repository. Test anchor: `python3 -m py_compile tests/fixtures/review_git_repo.py` plus the helper's own round-trip self-check; evidence: the fixture file.

**Checkpoint**: A deterministic temporary-repository harness exists, so the base, header, receipt, and verdict assertions are proven against real git behaviour rather than against prose.

---

## Phase 3: User Story 1 - 一次 review 同时得到过程结论与代码结论 (Priority: P1) — MVP

**Goal**: `/speckit.review` runs two segments in a fixed order, writes two artifacts that never overwrite each other, triages the code segment to one of three applicability values, and surfaces both conclusions in one place.

**Independent Test**: On a feature with a committed delta, one invocation produces `review.md` first and `code-review.md` second, `review.md` § 2.1 carries the code-segment verdict and pointers, and the closing summary lists both segments' conclusions; on a code-less feature the same command records `not-applicable` with a basis instead of silently dropping the segment.

### Tests for User Story 1 (MANDATORY)

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [ ] T004 [P] [US1] Write the red-first contract test `tests/contract/test_review_code_composition.py` pinning the command template's composed surface: exactly two segments in a fixed order with no third mode, the process segment unconditional (no class, argument, or missing-delta exemption), delegation to both skills by named runtime path with no inlined methodology or severity definition, the three applicability values each with its mandatory basis or reason, the failure-propagation rule, the review object with its uncommitted-scope exclusion, the two-artifact rule with rotation, the report subsection's allowed content, the closing-summary duty, the code finding's locating form, and the untouched non-segment surfaces; record the failing command, real output, and exit code in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. Test anchor: this test file; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`.
- [ ] T005 [US1] Write the red-first docs↔template isomorphism test `tests/contract/test_review_docs_isomorphism.py`, comparing the *declared surface* of `docs/reference/commands/review.md` against `templates/commands/review.md` — named segments, artifacts, applicability values, and the two unmapped severity vocabularies — so a cosmetic reword does not red it and a deleted segment does; the page still describes a process-only review, so the run is red by construction; record it in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. Test anchor: this test file; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`.

### Implementation for User Story 1

- [ ] T006 [US1] Write the composition and applicability-triage section of `templates/commands/review.md`: the fixed order (process segment first and unconditional, code segment second), delegation to both skills by runtime path with no methodology inlined, the no-merged-severity rule, the three triage values with their mandatory basis or reason and no silent fourth state, the failure-propagation rule (a process-segment abort records `not-evaluated` and does not suppress the code segment, and the run is never presented as a completed review), and the review object (this feature slice's committed delta, working-tree changes excluded and disclosed). [green: contracts/command-orchestration.md#C-1] [green: contracts/command-orchestration.md#C-2] [green: contracts/command-orchestration.md#C-3] [green: contracts/command-orchestration.md#C-4] [green: contracts/command-orchestration.md#C-5] [green: contracts/command-orchestration.md#C-6] [green: contracts/command-orchestration.md#C-7] [green: contracts/command-orchestration.md#C-8] [blockedBy: T004]
- [ ] T007 [US1] Add the `### 2.1` code-segment subsection and its placeholder-glossary rows to `templates/review-template.md`: base and head commit ids with the base source, the renderer mode, the receipt counts (changed / judged / skipped / gap), the segment verdict, the gate verdict, the not-applicable or not-evaluated reason when one applies, the record path, and this run's archive path — verdict and pointers only, never the opinion bodies or a per-item count list; keep every existing top-level section number stable. [green: contracts/command-orchestration.md#C-9] [green: contracts/command-orchestration.md#C-10] [blockedBy: T004]
- [ ] T008 [US1] Write the output, placement, and closing rules of `templates/commands/review.md`: two artifacts that never overwrite each other and never share one severity summary table, the rotation that archives the previous record and the recorded archive path, the record's exclusion from any downstream available-documents list together with its link from the bound feature's review-record row, the closing summary carrying both segment conclusions, the code finding's severity-plus-location form (never a `REC-…` identifier), and the statement that the frontmatter `scripts:` block, the compiled `## Wrap-up` face, and `## Handoffs` are unchanged. [green: contracts/command-orchestration.md#C-11] [green: contracts/command-orchestration.md#C-12] [green: contracts/command-orchestration.md#C-13] [green: contracts/command-orchestration.md#C-14] [green: contracts/command-orchestration.md#C-15] [green: contracts/command-orchestration.md#C-16] [blockedBy: T006]
- [ ] T009 [US1] Verify US1: run `python3 -m pytest -q tests/contract/test_review_code_composition.py`, record the red-to-green transition (command, output, exit code) in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`, confirm quickstart Scenario B's four observable results and Scenario C's `not-applicable` path each have a passing assertion or a recorded reason, and append a `targeted-set-v1` stage-status row to `.specify/specs/071-review-code-integration/test-evidence/implement-stage-status.jsonl`; the isomorphism test stays red by design until T031 lands the page. Test anchor: `tests/contract/test_review_code_composition.py`; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. [blockedBy: T004,T005,T007,T008]

**Checkpoint**: US1 is independently testable: one invocation yields both artifacts, the triage is one of three recorded values, the report subsection carries verdict and pointers only, and neither severity vocabulary is merged.

---

## Phase 4: User Story 2 - 代码评审的对象与基准可判定、可复算 (Priority: P1) — MVP

**Goal**: The reviewed object and its diff base are reproducible from the repository, the base is never a branch-name default, and uncommitted work is disclosed rather than absorbed.

**Independent Test**: Resolve the base twice on an unchanged repository and get the same `base=` plus the same `base_source=`; point an explicit base at a different commit and see it win; dirty the tree and see the record disclose an unreviewed scope without any conclusion over it; construct an unresolvable base and get `not-evaluated` with a reproducible command instead of a guess.

### Tests for User Story 2 (MANDATORY)

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [ ] T010 [P] [US2] Write the red-first contract test `tests/contract/test_code_review_skill_contract.py` against the unchanged tree: the base-resolution order and its `base_source` tier names, the first-add instrument for the feature-slice tier, the refusal of a branch-name default, the single record-header form, the non-interactive reachability of record creation and rotation, the renderer-absence clause in its rewritten form, the receipt as sole evidence, the explicit-input verdict, and the sibling boundary — the US3 bands (renderer, receipt evidence, verdict, boundary) are authored here in the same pass because they belong to the same pinned file, and their green points are the US3 implementation rows; record the failing run in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. Test anchor: this test file; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. [blockedBy: T003]

### Implementation for User Story 2

- [ ] T011 [US2] Add the `base` subcommand to `skills/internal/code-review/scripts/git-delta-review.sh`: the three ordered tiers — an explicit caller value, else the parent of the first commit that added `<spec>/requirements.md` derived with `git log --diff-filter=A -- <spec>/requirements.md` (never `git log -1` over the directory), else the merge base with the repository's default trunk — printing `base=`, `head=`, and `base_source=`, exiting `2` when no tier resolves, and never falling back to a branch literal or to the script's built-in default. [blockedBy: T010]
- [ ] T012 [US2] Add the `start` subcommand to `skills/internal/code-review/scripts/git-delta-review.sh`: create the record with the one header form (branch, base and head in full and short form, the base source tier, the renderer marker, the reviewer, the run date), rotate an existing record to `<spec>/code-review-<YYYYMMDD-HHMMSS>.md` before writing, and exit `2` rather than overwrite an existing archive. [blockedBy: T010]
- [ ] T013 [US2] Verify US2 and turn its band green: run the base-tier, header, and record-creation cases in `tests/contract/test_code_review_skill_contract.py` against the temporary repository, record the red-to-green transition in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`, confirm quickstart Scenario A yields `base_source=feature-first-commit` with the measured base, prove that two runs on the same repository state resolve the same base, and append a `targeted-set-v1` stage-status row to `.specify/specs/071-review-code-integration/test-evidence/implement-stage-status.jsonl`. [green: contracts/code-review-skill.md#C-17] [green: contracts/code-review-skill.md#C-18] [green: contracts/code-review-skill.md#C-19] [green: contracts/code-review-skill.md#C-20] [green: contracts/code-review-skill.md#C-21] Test anchor: `tests/contract/test_code_review_skill_contract.py`; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. [blockedBy: T011,T012]

**Checkpoint**: US2 is independently testable: the base and its tier are printable and repeatable, an explicit base wins, no branch literal participates, and an unresolvable base yields `not-evaluated` with the command that failed.

---

## Phase 5: User Story 3 - 缺渲染器时不冒充已评审 (Priority: P2)

**Goal**: A missing renderer no longer stops the code segment; the coverage receipt — not the presence of tool output — becomes the only evidence that the whole diff was read, and a gap exits non-zero.

**Independent Test**: Drive the script with `DELTA_BIN` pointed at a non-existent binary and get a completed segment with the text-mode marker and a full receipt; delete one per-file entry and get exit `1` with a non-zero `gap_files`; mark files as reasoned skips and get exit `0` with `skipped_files > 0` and a verdict that is not `pass`.

### Tests for User Story 3 (MANDATORY)

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [ ] T014 [P] [US3] Write the red-first contract test `tests/contract/test_coverage_receipt.py` pinning the receipt carrier and grammar (delimited block, closed name set, sorted zero-padded per-file rows, the counting identity), the exit-code semantics `0`/`1`/`2`, the gap-versus-skip distinction, the mechanical verdict derivation, the renderer-literal equality between the header marker and the block, and the gap drill (delete one per-file entry and re-run); drive the real script inside the temporary repository from T003, including the text-mode case via `DELTA_BIN`, and record the failing run in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. Test anchor: this test file; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. [blockedBy: T003]

### Implementation for User Story 3

- [ ] T015 [US3] Add the `receipt` subcommand to `skills/internal/code-review/scripts/git-delta-review.sh`: compute the changed-file set over the resolved range, compare it with the judged set, write the one delimited `name=value` block with the closed field set and sorted zero-padded per-file rows, measure `lines_added`/`lines_deleted` from `git diff --numstat`, accept a repeatable reasoned skip selector, exit `0` only when the two sets are equal and every changed file carries a verdict, exit `1` on any gap, exit `2` with no block written when the range, the record, or the repository is unusable, and derive the segment verdict from the three signals together without letting a skip count as coverage. [green: contracts/coverage-receipt.md#C-31] [green: contracts/coverage-receipt.md#C-32] [green: contracts/coverage-receipt.md#C-33] [green: contracts/coverage-receipt.md#C-34] [green: contracts/coverage-receipt.md#C-35] [green: contracts/coverage-receipt.md#C-36] [green: contracts/coverage-receipt.md#C-37] [green: contracts/coverage-receipt.md#C-38] [green: contracts/coverage-receipt.md#C-39] [green: contracts/coverage-receipt.md#C-40] [green: contracts/coverage-receipt.md#C-41] [green: contracts/coverage-receipt.md#C-42] [blockedBy: T014]
- [ ] T016 [US3] Rewrite the renderer-absence clause in `skills/internal/code-review/SKILL.md` — the `Strict Requirements` block and the Phase 0 environment-confirmation step — and align `skills/internal/code-review/references/delta-setup.md` with it: keep one statement naming the replaced clause, its substitute evidence form (the coverage receipt), and the reason for the replacement; carry the text-mode marker literal; keep the anti-pretense rule verbatim (no claim of a rendered, visual, or side-by-side review while the text mode ran); keep the never-install-the-renderer invariant and its install pointer; and declare the receipt the sole evidence form for "the whole diff was read". No surface may retain a "stop when the renderer is missing" assertion. [green: contracts/code-review-skill.md#C-22] [green: contracts/code-review-skill.md#C-23] [green: contracts/code-review-skill.md#C-24] [green: contracts/code-review-skill.md#C-25] [blockedBy: T015]
- [ ] T017 [US3] Add `--file` to the `report` subcommand of `skills/internal/code-review/scripts/git-delta-review.sh`: the record path becomes explicit, an omitted path stays a legacy selection that labels itself as implicit and is never used by the composed path, and the exit codes become `0` allow / `1` deny with the unresolved `blocking` count / `2` input error, so exactly one verdict source exists and the command reuses it instead of recomputing a criterion. [green: contracts/code-review-skill.md#C-26] [green: contracts/code-review-skill.md#C-27] [blockedBy: T012,T015]
- [ ] T018 [US3] Verify US3: run `python3 -m pytest -q tests/contract/test_coverage_receipt.py`, record the red-to-green transition in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`, confirm quickstart Scenarios D, E, and F (text mode, gap drill, focused pass) behave as stated, confirm the interactive per-file walk and its six-level validation are intact (end-to-end against the temporary repository, not by reading the script), confirm a non-zero gap or skip count is surfaced outside the block in the report subsection and the closing summary and that a dirty tree is disclosed with no conclusion over it, and append a `targeted-set-v1` stage-status row to `.specify/specs/071-review-code-integration/test-evidence/implement-stage-status.jsonl`. [green: contracts/code-review-skill.md#C-28] [green: contracts/coverage-receipt.md#C-43] [green: contracts/coverage-receipt.md#C-44] Test anchor: `tests/contract/test_coverage_receipt.py`; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. [blockedBy: T016,T017]

**Checkpoint**: US3 is independently testable: the text-mode run completes and says so, a gap is a non-zero exit, a skip is legal but never a pass, and the verdict comes from three counted signals rather than from a hand assignment.

---

## Phase 6: User Story 4 - 两套严重度各有其位，门禁关系单一可判定 (Priority: P2)

**Goal**: The `Implemented → Ready for Review` criterion lives in one declared owner, an unresolved `blocking` blocks the transition, `important`-only allows it with per-item answers, and no mapping between the two vocabularies exists anywhere.

**Independent Test**: Build a record with an unresolved `blocking` item and confirm the gate refuses with a reason naming the count; clear it and confirm the gate allows; build an `important`-only record and confirm the transition is allowed while the items must each be answered; confirm the integration protocol's rows carry a reference and not a second criteria wording.

### Tests for User Story 4 (MANDATORY)

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [ ] T019 [P] [US4] Write the red-first contract test `tests/contract/test_status_gate_owner.py` pinning the owner row's three conjunctive conditions and the direct six-level read, the `important`-only allowance, the four never-blocking levels, the explicit-user-ruling-only waiver recorded in two places, the three disclosure places for `not-applicable` and `not-evaluated`, the refusal reason naming the failed condition with the status left at `Implemented`, the single checkpoint after both segments, and the convergence of both initiating rows to a reference; record the failing run in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. Test anchor: this test file; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`.

### Implementation for User Story 4

- [ ] T020 [US4] Edit the `Implemented → Ready for Review` row of `templates/feature-details-template.md` § Canonical Status State Machine so it carries its three conjunctive conditions — every deferred task resolved or explicitly waived, review evidence produced, and no unresolved `blocking` item in the code segment — and states that the third is judged by reading the six-level vocabulary directly rather than by relabelling it. [green: contracts/status-gate-ownership.md#C-45] [green: contracts/status-gate-ownership.md#C-46] [blockedBy: T019]
- [ ] T021 [US4] Converge `shared/workflow/feature-integration.md` § Status State Machine: the `/speckit.review` row and the `/speckit.checklist` row each name the transition, name the owner section, and state that the criteria are not restated there — the duplicated wording is removed rather than reworded to agree — while the checklist row's "applies only when the checklist runs after implement" annotation stays, because an existing pin reads it. [green: contracts/status-gate-ownership.md#C-47] [green: contracts/status-gate-ownership.md#C-48] [blockedBy: T020]
- [ ] T022 [US4] Add the remaining owner clauses to `templates/feature-details-template.md` and the matching pointer in `templates/commands/review.md`: `important` items allow the transition but must each be answered while `suggestion`, `nitpick`, `question`, and `praise` never block; a waiver comes only from an explicit user ruling and is written into the report and the feature detail; `not-applicable` and `not-evaluated` are disclosed in the report subsection, the closing summary, and the feature detail's review-record row; a refusal names the failed condition and leaves the status at `Implemented`; and no numeric conversion, mapping matrix, or unified score exists or ever may. [green: contracts/status-gate-ownership.md#C-49] [green: contracts/status-gate-ownership.md#C-50] [green: contracts/status-gate-ownership.md#C-51] [green: contracts/status-gate-ownership.md#C-52] [green: contracts/status-gate-ownership.md#C-53] [blockedBy: T021]
- [ ] T023 [US4] Verify US4: run `python3 -m pytest -q tests/contract/test_status_gate_owner.py`, record the red-to-green transition in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`, confirm quickstart Scenario G's two runs (an unresolved `blocking` exits `1` with the count; resolved exits `0`) against the temporary repository, and confirm the transition is judged once after both artifacts exist. [green: contracts/status-gate-ownership.md#C-54] Test anchor: `tests/contract/test_status_gate_owner.py`; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. [blockedBy: T020,T021,T022]

**Checkpoint**: US4 is independently testable: the owner row is the only place the criteria exist, both initiating rows reference it, `blocking` denies and `important` allows, and no artifact stores a mapped severity value.

---

## Phase 7: User Story 5 - review 与 feedback 的通道不再互相污染 (Priority: P2)

**Goal**: Only framework friction reaches the feedback store, each nested unit closes itself, the predecessor invariants stay intact, and the expression-class review face keeps its own judgment object.

**Independent Test**: Run a composed review that produces both a code defect and an environment friction and check that only the latter is a legal feedback entry; confirm the closing step set is unchanged and that the expression-face assertion still passes unchanged.

### Tests for User Story 5 (MANDATORY)

> **NOTE: Write these tests first and confirm they fail before implementation.**

- [ ] T024 [P] [US5] Write the red-first contract test `tests/contract/test_review_feedback_boundary.py` pinning both constructed samples (a framework-friction item is legal; a code defect copied out of the record violates the written classification duty), the nested-unit rule under the `(unit_id, run_id)` key with neither unit suppressed, the unchanged closing step set, the predecessor invariants, the expression-face protection, and the receipt-counts-reviewed-files distinction; record the failing run in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. Test anchor: this test file; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`.

### Implementation for User Story 5

- [ ] T025 [US5] Write the classification duty and the nested-unit rule into `templates/commands/review.md`, outside the compiled `## Wrap-up` face: framework friction is the only legal feedback payload while a code defect stays in the record, both units close themselves, and the command neither suppresses the skill's closing record nor writes its run determination on its behalf; the closing step set stays exactly as published. [green: contracts/feedback-and-boundaries.md#C-55] [green: contracts/feedback-and-boundaries.md#C-56] [blockedBy: T024]
- [ ] T026 [US5] Write the same classification duty into `skills/internal/code-review/SKILL.md` as the second surface and state the skill's own closing obligation under the shared run id, so posting a code defect as feedback is a detectable violation of a written rule rather than a matter of taste. [green: contracts/feedback-and-boundaries.md#C-57] [green: contracts/feedback-and-boundaries.md#C-58] [green: contracts/feedback-and-boundaries.md#C-59] [blockedBy: T016,T024]
- [ ] T027 [US5] Record the predecessor invariants as unchanged and protect the expression face: state in `skills/internal/code-review/SKILL.md` that the receipt counts reviewed files and is never evidence for the reader-baseline judgement, and that the code segment is an additional segment recorded as `not-applicable` for a feature with no delta; confirm no new intake store, aggregation directory, id family, or upload path is introduced; re-run `python3 -m pytest -q tests/contract/test_expression_gates_doc.py` and record its result against the plan-stage pre-change count of 18 passed in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. [green: contracts/feedback-and-boundaries.md#C-60] [green: contracts/feedback-and-boundaries.md#C-61] [green: contracts/feedback-and-boundaries.md#C-62] [green: contracts/feedback-and-boundaries.md#C-63] [blockedBy: T025,T026]
- [ ] T028 [US5] Verify US5: run `python3 -m pytest -q tests/contract/test_review_feedback_boundary.py`, record the red-to-green transition in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`, confirm quickstart Scenario H's two samples are judged as stated, enumerate the closing step set from the compiled face and confirm it equals the pre-change set, and append a `targeted-set-v1` stage-status row to `.specify/specs/071-review-code-integration/test-evidence/implement-stage-status.jsonl`. Test anchor: `tests/contract/test_review_feedback_boundary.py`; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. [blockedBy: T025,T026,T027]

**Checkpoint**: US5 is independently testable: a code defect is not a legal payload, both units record themselves, the closing face is untouched, and the expression assertion is unchanged and still green.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Prove the six contract groups are real, land the one intentional pin change, sync documentation and mirrors, run the quickstart, sweep the scope, and close with the final comparison.

- [ ] T029 Confirm the six new-behaviour contract groups exist and were red-first: enumerate them from each contract file's `Pinned by` line, verify each has a recorded failing command, real output, and exit code in `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`, and record any group whose red run is missing or could not go red as a fast-fail finding in the same note instead of citing it as coverage. [green: contracts/tests-and-docs-sync.md#C-65] [green: contracts/tests-and-docs-sync.md#C-66] Test anchor: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`; evidence: the same note plus the six test files. [blockedBy: T004,T005,T010,T014,T019,T024]
- [ ] T030 Update the one intentional pin `tests/contract/test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition`: it keeps its subject (the `/speckit.review` row exists and the command owns the transition), stops requiring the duplicated criteria wording that T021 removed, and gains an assertion that the row cites `templates/feature-details-template.md` § Canonical Status State Machine plus a negative assertion that the duplicated wording is gone — net assertions rise and nothing is dropped without a replacement naming the same obligation. [green: contracts/tests-and-docs-sync.md#C-67] [green: contracts/feedback-and-boundaries.md#C-64] Test anchor: this test file; evidence: `.specify/specs/071-review-code-integration/notes/red-first-evidence.md`. [blockedBy: T021]
- [ ] T031 Rewrite `docs/reference/commands/review.md` to the composed surface (two segments and their order, two artifacts, two severity vocabularies that are never mapped, the three applicability values, and a pointer to the transition owner) and rewrite both skills' boundary wording — the `description` and `## Boundaries` of `skills/internal/review-sdd-process/SKILL.md` and the matching paragraph of `skills/internal/code-review/SKILL.md` — as "distinct judgment objects, composed by the command in a fixed order", so no "the two are unrelated, keep them separate" statement survives anywhere. [green: contracts/tests-and-docs-sync.md#C-68] [green: contracts/code-review-skill.md#C-29] [blockedBy: T022,T030]
- [ ] T032 Mirror write: run `python3 scripts/python/sync-mirrors.py --write` for the edited template, skill, and shared files, then `python3 scripts/python/regen-command-copies.py` for the per-tool command copies; the source is the only edit surface, and no `.specify/` copy or per-tool copy is hand-edited. [green: contracts/tests-and-docs-sync.md#C-69] [blockedBy: T008,T016,T017,T022,T026,T031]
- [ ] T033 Mirror verify: run `python3 scripts/python/sync-mirrors.py --check --only templates`, `--only skills/internal`, `--only shared`, and `python3 scripts/python/regen-command-copies.py --check`, and compare each result against the T001 measurements (22 / 136 / 55 files, per-tool copies matching) so the verdict is "no NEW drift", never an absolute pass. [green: contracts/tests-and-docs-sync.md#C-70] Test anchor: the four check commands' output; evidence: `.specify/specs/071-review-code-integration/notes/pre-change-measurements.md`. [blockedBy: T032]
- [ ] T034 Run the docs↔template isomorphism test green, then execute quickstart Scenarios A through H through the `.specify/skills/internal/code-review/` mirror path and write the real commands, outputs, exit codes, and teardown steps to `.specify/specs/071-review-code-integration/notes/quickstart-run.md`; a scenario that cannot run records its blocking premise instead of being reported as passed. [green: contracts/tests-and-docs-sync.md#C-71] Test anchor: `tests/contract/test_review_docs_isomorphism.py` plus the seven scenario runs; evidence: `.specify/specs/071-review-code-integration/notes/quickstart-run.md`. [blockedBy: T031,T033]
- [ ] T035 Scope sweep: re-run `tests/contract/test_migration_distribution.py`, `tests/contract/test_expression_compatibility.py`, `tests/contract/test_flat_internal_skill_migration.py`, and `tests/contract/test_run_skills_wiring.py` and compare by name, confirming the command and skill rosters are unchanged; confirm no new engine, daemon, external service, network call, or package dependency; and confirm every new capability is a subcommand of `skills/internal/code-review/scripts/git-delta-review.sh` rather than a second script or engine. [green: contracts/tests-and-docs-sync.md#C-72] [green: contracts/code-review-skill.md#C-30] Test anchor: the four suites' results; evidence: `.specify/specs/071-review-code-integration/notes/pre-change-measurements.md`. [blockedBy: T017,T034]
- [ ] T036 Final closure: run the six new suites plus the five neighbouring suites, compare failing test names against the T002 baseline (zero NEW), run `python3 scripts/python/validate-tasks.py .specify/specs/071-review-code-integration/tasks.md`, run `python3 scripts/python/account-clause-coverage.py .specify/specs/071-review-code-integration` and require the claimed-clause count to equal the contract set with zero names beyond the frozen baseline, and run `python3 .qoder/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/071-review-code-integration --stage tasks --repo .`; then write the SC-001…SC-007 evidence matrix into `.specify/specs/071-review-code-integration/verification.md`, one status row per criterion, `not_evaluated` where a source is missing and never a fabricated pass. [green: contracts/tests-and-docs-sync.md#C-73] Test anchor: all new and neighbouring suites plus the two accounting commands; evidence: `.specify/specs/071-review-code-integration/verification.md` and `.specify/specs/071-review-code-integration/baseline-failed.txt`. [blockedBy: T029,T030,T031,T033,T035]

**Checkpoint**: Documentation, the pin change, mirrors, quickstart execution, scope limits, and closure evidence are in place; only the stage's own review remains.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies; T001 and T002 write different targets and run together. T002 MUST run before any implementation edit.
- **Foundational (Phase 2)**: depends on Setup; T003 blocks every script-level test because the base, header, receipt, and verdict assertions all drive real git.
- **US1 (Phase 3)**: depends on Foundational only for the fixture-free text assertions; it supplies the command template and the report subsection that US3, US4, and US5 all extend.
- **US2 (Phase 4)**: depends on Foundational (T003); its base and record-creation subcommands are a prerequisite for US3's receipt and verdict.
- **US3 (Phase 5)**: depends on US2's `base` and `start` (the receipt needs a range and a record to write into) and on US1's report subsection (the counts must be surfaced outside the block).
- **US4 (Phase 6)**: depends on US1's command template; its verification reads the code segment's severity vocabulary, so the receipt must exist (US3) before the gate can be exercised end to end.
- **US5 (Phase 7)**: depends on US3's skill body (the second classification surface is written into the same file) and on US1's command template.
- **Polish (Phase 8)**: depends on all stories; T032 follows every source edit, T034 follows the docs rewrite, and T036 follows the pin change, the mirror check, and the scope sweep.

### Story Dependencies

- **US1 (P1)**: no story dependency; independent test = both artifacts plus the three triage values.
- **US2 (P1)**: independent of US1's text rules; independent test = repeatable base, explicit base wins, `not-evaluated` on failure.
- **US3 (P2)**: depends on US2's subcommands; independent test = text mode completes, gap exits non-zero, skip never passes.
- **US4 (P2)**: depends on US1's template surface and on US3's severity vocabulary being present; independent test = deny on `blocking`, allow on `important`-only.
- **US5 (P2)**: depends on US1 and US3; independent test = the two feedback samples are judged differently and the closing face is unchanged.

### Within Each User Story

- Test rows come before implementation rows, and each records a real failing run before its subject exists.
- The verification row runs the story's cases, records the red-to-green transition, and appends its targeted stage-status row.
- Shared sinks (`notes/red-first-evidence.md`, `test-evidence/implement-stage-status.jsonl`) are written by several rows, which is why those rows are sequenced rather than all marked `[P]`.

## Parallel Opportunities

- Setup: T001 and T002 write different targets and run together.
- US1: T004 is the only `[P]` row, because T005 and every later row append to the same red-first evidence sink.
- US2: T010 is the only `[P]` row; T011 and T012 follow it and both edit the same script, so they are sequenced.
- US3: T014 is the only `[P]` row; T015 → T016 → T017 are sequenced by file and by the script-before-prose rule.
- US4: T019 is the only `[P]` row; T020 → T021 → T022 edit the owner row and its convergence in dependency order.
- US5: T024 is the only `[P]` row; T025 → T026 → T027 depend on each other's surfaces.
- Polish: every row edits or checks a target an earlier Polish row produced, so none is marked `[P]`.

## Parallel Example: Setup

```bash
# Two rows, two targets, no shared sink.
Task: "T001 record the pre-change measurements in notes/pre-change-measurements.md"
Task: "T002 capture the implement-start failing-test baseline name list"
```

## Implementation Strategy

### MVP First

The MVP is US1 + US2 together: a command that composes two segments but cannot say which commits it reviewed is not an independently valuable increment, and both are P1. Complete Setup and Foundational, then US1 and US2, and stop at each checkpoint to validate independently. US3, US4, and US5 follow as P2 refinements; Polish closes the surface.

### Incremental Delivery

1. Setup + Foundational → dated controls and the temporary-repository harness exist.
2. US1 → the composed command and the report subsection are testable.
3. US2 → the review object and its base are reproducible and overridable.
4. US3 → text mode, the receipt, and the gap exit are testable.
5. US4 → the single-owner gate denies on `blocking` and allows `important`-only.
6. US5 → the feedback classification duty and the expression boundary are testable.
7. Polish → pin, docs, mirrors, quickstart, scope sweep, closure.

### Parallel Team Strategy

With multiple workers: one owns the script subcommands and their contract tests; one owns the command template and the report template; one owns the two governance documents and their pin; one owns the docs page, the boundary wording, mirrors, and the quickstart. The owner row is edited by one worker only, and no worker rewrites a plan-owned artifact.

## Notes

- `[P]` rows write different targets and have no unfinished dependency; the shared red-first sink is why most test rows are sequenced instead of marked `[P]`.
- The code segment never assigns its verdict by hand: `pass` requires `gap_files = 0`, `skipped_files = 0`, and no unresolved `blocking` item together.
- A reasoned skip is legal and exits `0`, but it is not coverage credit and it forbids a `pass` verdict.
- The merge gate has one verdict source (`report --summary --file`); the command reuses it and never recomputes a criterion.
- Framework sources are the only edit surface; `.specify/` and the per-tool command copies are produced by the existing generators.
- No push, force merge, confirmation-gate bypass, new `/speckit.*` command, new skill, new dependency, second feedback store, or plan-owned rewrite.
