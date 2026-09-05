# Tasks: /speckit.docs 三段式调协编排(目标结构驱动)

**Requirement ID**: 048
**Requirement Key**: `048-docs-reconcile`
**Related Feature**: Feature 037 Docs Command
**Input**: Design documents from `.specify/specs/048-docs-reconcile/`
**Prerequisites**: `plan.md`, `requirements.md`, `data-model.md`, `contracts/`, `quickstart.md`, `feature-ref.md`

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates automated regression/contract coverage; Principle VII's template-only gate requires structural contract tests for templates, prompts, skills, mirrors, and docs rather than runtime unit/integration tests.

**Organization**: Tasks use the doc-feature taxonomy (author-section → mirror-parity → render/surface-verify → refresh-verify), grouped by user story. User Stories 1 and 2 are both P1 and together form the MVP: US1 establishes the target declaration; US2 consumes it to compute and dispatch typed actions.

## Definition of Done (DoD)

- DoD-1: Every task row is closed `[X]` or explicitly deferred `[~]` with its reason recorded in `verification.md`
- DoD-2: New structural contract tests and all existing docs-command/skill regression tests pass with zero new failures versus the recorded baseline
- DoD-3: All four mirror obligations in `plan.md` are fulfilled: command copies regenerate cleanly; the new template and both skill mirrors are byte-identical; no new mirror drift appears beyond the recorded `git-fleet` baseline
- DoD-4: Confirmation-gate scan remains `total: 23`, `governance_kept: 10`, `destructive: 13`, and `violations: 0`; no new gate or probe is introduced
- DoD-5: Quickstart scenarios 1–6 are exercised at the command surface in an isolated worktree or disposable fixture, with observed outcomes recorded honestly
- DoD-6: `verification.md` lists SC-001 through SC-007 with Pass/Partial/Fail status, evidence paths, and any deferred tasks
- DoD-7: Feature 037 memory/index notes and `docs/reference/commands/docs.md` reflect the implemented behavior while Feature status remains Implemented

**DoD Status**: pending

## Completion Gate

- GATE-1: Targeted contract suite passes — check: `pytest tests/contract/test_docs_command_template.py tests/contract/test_docs_skill_pair.py tests/contract/test_docs_utils_cli.py tests/contract/test_confirmation_gates_sweep.py tests/contract/test_feedback_command_classification.py tests/contract/test_docs_target_structure_declaration.py tests/contract/test_docs_action_routing.py tests/contract/test_docs_reconcile_orchestration.py -q`
- GATE-2: Full suite has zero new failing node IDs versus baseline — check: `bash -o pipefail -c 'set +e; .specify/scripts/bash/run-tests.sh -q --names-out /tmp/spec048-current-failed.txt > /tmp/spec048-pytest.txt 2>&1; code=$?; set -e; test "$code" -ne 2 -a "$code" -ne 3 -a "$code" -ne 4; comm -13 .specify/specs/048-docs-reconcile/baseline-failed.txt /tmp/spec048-current-failed.txt > /tmp/spec048-new-failures.txt; test ! -s /tmp/spec048-new-failures.txt'`
- GATE-3: Generated command copies are current — check: `python3 scripts/python/regen-command-copies.py --check` returns 0
- GATE-4: Touched mirrors are byte-identical — check: `diff -q templates/docs-target-structure-template.md .specify/templates/docs-target-structure-template.md && diff -q skills/create-docs/SKILL.md .specify/skills/create-docs/SKILL.md && diff -q skills/improve-docs/SKILL.md .specify/skills/improve-docs/SKILL.md`
- GATE-5: Mirror scanner introduces no new `MISS`/`DIFF` rows beyond baseline — check: `bash -o pipefail -c 'set -e; code=0; python3 scripts/python/sync-mirrors.py --check > /tmp/spec048-mirrors.txt 2>&1 || code=$?; test "$code" -eq 0 -o "$code" -eq 2; comm -13 <(grep -E "^(MISS|DIFF)" .specify/specs/048-docs-reconcile/baseline-mirrors.txt | sort -u) <(grep -E "^(MISS|DIFF)" /tmp/spec048-mirrors.txt | sort -u) > /tmp/spec048-new-mirror-drift.txt; test ! -s /tmp/spec048-new-mirror-drift.txt'`
- GATE-6: Confirmation gates remain unchanged — check: `python3 scripts/python/scan-confirmation-gates.py --json | python3 -c 'import json,sys; d=json.load(sys.stdin); assert d["total"] == 23 and d["by_class"] == {"governance_kept": 10, "destructive": 13} and not d["violations"]'`
- GATE-7: Documentation-space validation has no new findings — check: `python3 scripts/python/docs-utils.py --action validate --root .`
- GATE-8: No open/claimed tasks remain and every success criterion is recorded — check: `bash -o pipefail -c 'set -e; test -f .specify/specs/048-docs-reconcile/verification.md; ! grep -qE "^- \[[ >]\]" .specify/specs/048-docs-reconcile/tasks.md; comm -3 <(grep -oE "SC-[0-9]{3}" .specify/specs/048-docs-reconcile/requirements.md | sort -u) <(grep -oE "SC-[0-9]{3}" .specify/specs/048-docs-reconcile/verification.md | sort -u) > /tmp/spec048-sc-delta.txt; test ! -s /tmp/spec048-sc-delta.txt'`

## Format: `[ID] [P?] [Story] Description`

- **[P]**: May run in parallel after its blockers close because it writes a different file and has no shared mutable state
- **[Story]**: Maps the task to US1, US2, or US3 from `requirements.md`
- **[blockedBy: Txxx,Tyyy]**: Machine-readable task dependency
- Every task row is one physical line and names exact repository paths

## Phase 1: Setup (Baseline Evidence)

**Purpose**: Freeze mutable test and governance baselines before implementation so existing failures/drift are never misreported as regressions.

- [X] T001 Run `.specify/scripts/bash/run-tests.sh -q --names-out .specify/specs/048-docs-reconcile/baseline-failed.txt`, verify collection succeeds (pytest exit 2/3/4 is a probe failure, not a baseline), preserve the sorted raw failing node IDs exactly as written by the canonical runner, and record pass/fail/skip totals separately in `.specify/specs/048-docs-reconcile/verification.md`
- [X] T002 [P] Capture `scan-confirmation-gates.py --json`, `regen-command-copies.py --check`, and full `sync-mirrors.py --check` outputs in `.specify/specs/048-docs-reconcile/baseline-gates.json` and `.specify/specs/048-docs-reconcile/baseline-mirrors.txt`, preserving every observed `MISS`/`DIFF`/`note` row verbatim instead of pinning a planning-time note count

**Checkpoint**: Test, gate, command-copy, and mirror baselines are frozen before any source artifact changes.

---

## Phase 2: Foundational (Shared Contracts and RED Harness)

**Purpose**: Update the existing Feature 037 contract and establish shared RED assertions before any user-story implementation.

**⚠️ CRITICAL**: No user-story implementation starts until the shared contract and RED harness are ready.

- [X] T003 Revise C-1, C-4a, C-5, C-7, C-8, and C-18 with a dated 2026-09-01 revision note in `.specify/specs/033-docs-command/contracts/docs-command-template.md`, preserving C-3 and historical withdrawn clauses while correcting the retired command mirror and 18-complex/4-simple facts
- [X] T004 [blockedBy: T003] Extend `tests/contract/test_docs_command_template.py` with structural assertions for the target declaration path/template, two-skill single-source ownership, fifth cross-run artifact, unchanged six-heading order, retained required literals, absent `R0 需求解析`, absent retired `.specify/templates/commands/docs.md`, and 18/4 classification without hard-coding incidental file counts
- [X] T005 [blockedBy: T004] Run `pytest tests/contract/test_docs_command_template.py -q`, confirm the new assertions fail for the intended missing behavior rather than fixture/path errors, and record the RED evidence in `.specify/specs/048-docs-reconcile/verification.md`

**Checkpoint**: The shared contract is current and the common structural harness fails only because the new orchestration is not implemented.

---

## Phase 3: User Story 1 — 目标结构设定与持久化 (Priority: P1) 🎯 MVP Part 1

**Goal**: Establish a project-specific, confirmed, persistent target structure declaration that later runs reuse without redesign.

**Independent Test**: In a repository without `.specify/docs/target-structure.md`, produce a project-specific declaration from the template, verify it references rather than copies the create-docs baseline, persist it only after the existing R4 plan confirmation, and verify a second unchanged run reuses it with zero convergence.

### Structural Contract Tests for User Story 1

- [X] T006 [US1] [blockedBy: T005] Author and run RED tests in `tests/contract/test_docs_target_structure_declaration.py` covering root-level path, paired `DOCS_TARGET_STRUCTURE_START/END` markers, seven required fields (including fixed discovery routes), byte-preserving outside-block semantics, invalid-marker stop behavior, owner-derived detection of copied baseline facts, no `docs-utils.py` action expansion, underdetermined design producing 1–3 questions with zero declaration writes before answers, substantive project drift producing a confirmation-gated redesign proposal with zero pre-confirmation writes, and real-path existence checks for every asserted surface

### Authoring and Mirror Parity for User Story 1

- [X] T007 [P] [US1] [blockedBy: T006] Create `templates/docs-target-structure-template.md` with the managed-block markers and placeholders for 项目形态、目标读者、静态基线引用、项目专属扩展、内容盘点摘要、最后确认, keeping all create-docs-owned enumerations out of the file
- [X] T008 [P] [US1] [blockedBy: T006] Rewrite the first orchestration stage inside `templates/commands/docs.md` so it resolves `.specify/docs/target-structure.md`; derives project shape, audience, inventory, and extensions from repository evidence; asks one consolidated batch of at most 3 necessary questions and writes nothing when evidence is insufficient; designs only when absent or explicitly reset; detects evidence-backed substantive drift and adds a redesign proposal to the existing R4 plan without changing the declaration before confirmation; merges declaration approval into that same R4 confirmation; reuses unchanged declarations without churn; and stops on malformed markers without adding a heading, mode, or gate
- [X] T009 [P] [US1] [blockedBy: T006] Update the R0 baseline/interface wording in `skills/create-docs/SKILL.md` so the command may supply the confirmed target declaration as a higher-precedence project input while create-docs remains the owner of the static baseline and standalone skill behavior remains unchanged
- [X] T010 [US1] [blockedBy: T007] Run `python3 scripts/python/sync-mirrors.py --write --only templates/docs-target-structure-template.md` to create `.specify/templates/docs-target-structure-template.md` without touching the unrelated `git-fleet` mirror drift
- [X] T011 [US1] [blockedBy: T009] Run `python3 scripts/python/sync-mirrors.py --write --only skills/create-docs/` to update `.specify/skills/create-docs/SKILL.md` without broad mirror repair
- [X] T012 [US1] [blockedBy: T008,T010,T011] Verify `diff -q` parity for the target template and create-docs skill, run `pytest tests/contract/test_docs_target_structure_declaration.py tests/contract/test_docs_command_template.py -q`, and confirm the owner-derived T-5 check finds zero copied baseline facts in the template

### Surface Verification for User Story 1

- [X] T013 [US1] [blockedBy: T012] Enter a disposable isolated git worktree, invoke `/speckit.docs` through the active AI agent CLI command/skill surface (Qoder: `Skill` with `speckit.docs`; never execute the slash command in Bash), and exercise quickstart scenarios 1–2 plus their FR-003 underdetermined-input and FR-015 substantive-drift variants: verify one R4 confirmation, persistent outside-block-safe declaration writes, 1–3 questions with zero pre-answer writes, zero convergence on an unchanged rerun, and redesign proposal with zero pre-confirmation writes; append the command transcript, residual reports, and `git diff --name-status` evidence for SC-001/SC-005/SC-006 to `.specify/specs/048-docs-reconcile/verification.md`, then remove the disposable worktree

**Checkpoint**: A project can establish and safely reuse a persistent target structure declaration; this story is independently testable but the full P1 MVP additionally requires US2 routing.

---

## Phase 4: User Story 2 — 差异分解与双技能分发 (Priority: P1) 🎯 MVP Part 2

**Goal**: Convert substantive current-vs-target differences into typed actions and dispatch structure work to create-docs and evidence-backed content work to improve-docs.

**Independent Test**: In an isolated worktree containing one misplaced document and one correctly placed document with a verified stale claim, a full run produces two typed actions, routes each to the correct skill, preserves the existing confirmation tiers, reports both skill outcomes, and leaves all unfaulted documents unchanged.

### Structural Contract Tests for User Story 2

- [X] T014 [P] [US2] [blockedBy: T012] Author and run RED tests in `tests/contract/test_docs_action_routing.py` covering action fields, tolerance-band suppression, evidence-required content actions, exact create-docs/improve-docs routing, one-document sequential content dispatch, no cap or silent truncation, pre-dispatch count announcement, abort/pending semantics, per-skill residual reporting, and zero new confirmation gates
- [X] T015 [P] [US2] [blockedBy: T012] Extend and run RED assertions in `tests/contract/test_docs_skill_pair.py` proving improve-docs still cannot create/move/rename/archive documents, excludes `.specify/docs/target-structure.md` as a non-document cross-run contract rather than misclassifying all `.specify/docs/**` as disposable run artifacts, and preserves create-docs structural ownership

### Authoring and Mirror Parity for User Story 2

- [X] T016 [P] [US2] [blockedBy: T014] Rewrite the second and third orchestration stages inside `templates/commands/docs.md` to emit actions with type/target/owner/confirmation tier/evidence/source fields, suppress tolerated differences, mechanically route structure actions to create-docs and content actions to improve-docs, dispatch content sequentially, and group residual results by owning skill
- [X] T017 [P] [US2] [blockedBy: T015] Correct the machine-managed-store constraint in `skills/improve-docs/SKILL.md` so `.specify/docs/target-structure.md` is explicitly a cross-run non-document contract that improve-docs never edits while `.specify/docs/plans/` and `.specify/docs/audit/` remain run artifacts
- [X] T018 [US2] [blockedBy: T017] Run `python3 scripts/python/sync-mirrors.py --write --only skills/improve-docs/` to update `.specify/skills/improve-docs/SKILL.md` without broad mirror repair
- [X] T019 [US2] [blockedBy: T016] Run `python3 scripts/python/regen-command-copies.py` to regenerate `.claude/commands/speckit.docs.md`, `.github/prompts/speckit.docs.prompt.md`, `.qoder/commands/speckit.docs.md`, and `.opencode/command/speckit.docs.md` from the canonical command template
- [X] T020 [US2] [blockedBy: T018,T019] Verify `diff -q skills/improve-docs/SKILL.md .specify/skills/improve-docs/SKILL.md`, verify all four generated command copies carry the dual-skill routing edit and AUTO-GENERATED marker, and confirm `.specify/templates/commands/docs.md` remains absent
- [X] T021 [US2] [blockedBy: T020] Run `pytest tests/contract/test_docs_action_routing.py tests/contract/test_docs_skill_pair.py tests/contract/test_docs_command_template.py tests/contract/test_confirmation_gates_sweep.py -q` and verify the gate scanner remains total 23 with zero violations

### Surface Verification for User Story 2

- [X] T022 [US2] [blockedBy: T021] Enter a disposable isolated git worktree, seed one structural drift and one evidence-backed content drift, invoke `/speckit.docs` through the active AI agent CLI command/skill surface (Qoder: `Skill` with `speckit.docs`; never Bash), and exercise quickstart scenario 3; verify 100% action-to-skill routing, unchanged confirmation tiers, per-skill residual sections, and zero diffs on unfaulted documents; append the command transcript, residual report, and before/after `git diff --name-status` as SC-002/SC-004 evidence in `.specify/specs/048-docs-reconcile/verification.md`, then remove the disposable worktree

**Checkpoint**: US1 + US2 form the complete P1 MVP: a stable target exists and every substantive difference has one correct execution owner.

---

## Phase 5: User Story 3 — 用户附加输入的额外动作分解 (Priority: P2)

**Goal**: Make user-supplied instructions additive to baseline reconciliation, including writing commissions, directional priorities, confirmed target updates, and unbounded-but-announced content fan-out.

**Independent Test**: On an already converged isolated worktree, `/speckit.docs "创建一个描述登录流程的文档"` reports baseline zero convergence and creates/indexes the new compliant document in the same run; structure-changing input is written back only after the existing plan confirmation; large content fan-out announces its count and preserves completed work while carrying unstarted items as pending after an abort.

### Structural Contract Tests for User Story 3

- [X] T023 [US3] [blockedBy: T021] Author and run RED tests in `tests/contract/test_docs_reconcile_orchestration.py` covering additive-not-replacing input, the “what to write / where it lives” split, five-input content plans, canonical-owner search and near-duplicate prevention, unique canonical home, human index maintenance, `/speckit.instructions` Documentation Map refresh without alias edits, directional-input priority without target mutation, confirmed target writeback, create-pages/improve-skills handoffs, no-cap fan-out announcement, abort/pending semantics, unchanged six-heading order, required literal survival, and reference-document coverage

### Authoring, Documentation, and Generated Copies for User Story 3

- [X] T024 [P] [US3] [blockedBy: T023] Complete user-input orchestration in `templates/commands/docs.md`: always run baseline reconciliation; answer “what to write” with a content plan combining target reader/task context/user input/repository evidence/boundary; answer “where it lives” by searching a canonical owner first and otherwise selecting exactly one home; maintain human indexes and dispatch `/speckit.instructions` for Documentation Map refresh after canonical path changes; merge structural target updates into the existing R4 plan; announce full content count and preserve completed/pending results on abort without adding a gate or mode
- [X] T025 [P] [US3] [blockedBy: T023] Update `docs/reference/commands/docs.md` to lead with “what to write / where it lives”, explain five-input content planning, canonical-owner deduplication, unique placement, human index and Agent Documentation Map discovery, three-stage routing, additive examples, fifth artifact, no-cap/abort semantics, and links to both skills while referencing rather than copying the create-docs baseline
- [X] T026 [US3] [blockedBy: T024] Re-run `python3 scripts/python/regen-command-copies.py` so all four tool-specific command copies include the final additive-input and fan-out semantics
- [X] T027 [US3] [blockedBy: T025,T026] Run `python3 scripts/python/regen-command-copies.py --check`, verify all four generated copies contain the final edit and required AUTO-GENERATED header, verify the canonical template still has exactly six ordered top-level sections and all D-2 literals but no `R0 需求解析`, and confirm the updated reference document exposes every public behavior from D-8/D-9
- [X] T028 [US3] [blockedBy: T027] Run `pytest tests/contract/test_docs_reconcile_orchestration.py tests/contract/test_docs_command_template.py tests/contract/test_docs_action_routing.py tests/contract/test_confirmation_gates_sweep.py tests/contract/test_feedback_command_classification.py -q` and re-run the gate scanner to prove total 23/violations 0

### Surface Verification for User Story 3

- [X] T029 [US3] [blockedBy: T028] Enter a disposable isolated git worktree and invoke `/speckit.docs` through the active Qoder `Skill` surface for quickstart scenarios 4–6; for the login document capture the five-input content plan, canonical-owner search, unique home, human index diff, and `/speckit.instructions` Documentation Map refresh; verify same-run zero-reconcile plus creation, confirmed managed-block writeback, full fan-out count announcement, pre-start/mid-run abort, pending carryover, zero alias hand-edits, and fixed human/Agent lookup routes; append evidence for SC-003/SC-007 and edge cases to `.specify/specs/048-docs-reconcile/verification.md`, then remove the worktree

**Checkpoint**: All three stories are independently demonstrated and the command supports additive user intent without weakening baseline reconciliation.

---

## Phase 6: Polish & Cross-Cutting Verification

**Purpose**: Close mirror, governance, documentation, full-regression, Feature-memory, and success-criteria obligations across all stories.

- [ ] T030 [blockedBy: T013,T022,T029] Run the complete targeted contract suite from GATE-1 and append totals plus any failures to `.specify/specs/048-docs-reconcile/verification.md`
- [ ] T031 [blockedBy: T030] Run `regen-command-copies.py --check`, targeted `diff -q` checks for `templates/docs-target-structure-template.md`, `skills/create-docs/SKILL.md`, and `skills/improve-docs/SKILL.md`, compare full `sync-mirrors.py --check` MISS/DIFF rows with `.specify/specs/048-docs-reconcile/baseline-mirrors.txt`, and append the mirror verdict to `.specify/specs/048-docs-reconcile/verification.md`
- [ ] T032 [blockedBy: T031] Run `scan-confirmation-gates.py --json` and `docs-utils.py --action validate --root .`, verify the exact gate baseline and zero new documentation findings, and append both results to `.specify/specs/048-docs-reconcile/verification.md`
- [ ] T033 [blockedBy: T032] Run the full pytest suite, compare failing node IDs with `.specify/specs/048-docs-reconcile/baseline-failed.txt`, investigate every new failure instead of bypassing hooks/tests, and record the final regression delta in `.specify/specs/048-docs-reconcile/verification.md`
- [ ] T034 [blockedBy: T033] Update `.specify/memory/features/037.md` and the Feature 037 row in `.specify/memory/features.md` with implementation evidence, task/test/SC totals, dogfood results, mirror-baseline attribution, and Feature status remaining Implemented; keep `Total Features` at 48
- [ ] T035 [blockedBy: T034] Finalize `.specify/specs/048-docs-reconcile/verification.md` with SC-001…SC-007 status/evidence, deferred_tasks, touched-file inventory, confirmation-gate/mirror/full-suite results, and an explicit statement of any skipped or unavailable command-surface check; then re-run GATE-1 through GATE-8 and set DoD Status to green only if all pass

**Checkpoint**: Implementation is evidence-complete, Feature memory is current, and no task or success criterion is silently left unresolved.

---

## Requirements & Success-Criteria Coverage

| Requirement / Outcome | Primary Tasks | Verification Evidence |
|-----------------------|---------------|-----------------------|
| FR-001/FR-002/FR-002a/FR-003/FR-004/FR-015 — declaration design, reference-only baseline, persistence, bounded clarification, confirmation, reuse, and evidence-backed redesign proposal | T006–T013 | Target-declaration contract tests + quickstart scenarios 1–2 and their FR-003/FR-015 variants |
| FR-005/FR-006/FR-007 — typed action fields, mechanical create-docs/improve-docs routing, evidence-only content actions | T014–T022 | Action-routing and skill-pair tests + quickstart scenario 3 |
| FR-008 — sequential no-cap content dispatch, pre-dispatch count, abort/pending behavior | T014,T016,T023,T024,T028,T029 | Routing/orchestration tests + quickstart scenario 6 |
| FR-009/FR-010 — additive input and confirmed target writeback | T023–T029 | Orchestration tests + quickstart scenarios 4–5 |
| FR-011/FR-012 — existing tiered gates and thin orchestration | T004,T008,T016,T021,T024,T027,T028,T032 | Existing contract regression + exact gate total/violation check |
| FR-013 — per-skill residual report and no-op audit | T014,T016,T022,T023,T024,T029 | Scenarios 2–3 and routing report assertions |
| FR-014 — create-pages/improve-skills handoffs | T023,T024,T025,T028 | Orchestration/reference-document assertions |
| FR-016/FR-017/FR-018 — evidence/context-driven writing, one canonical home with duplicate prevention, and fixed human/Agent discovery | T023–T029,T035 | Orchestration tests + isolated writing commission + index/Documentation Map evidence |
| SC-001/SC-005/SC-006 | T006–T013,T030–T035 | Persistent/repeat-run evidence, zero baseline copies, thin-template structural checks |
| SC-002/SC-004 | T014–T022,T030–T035 | Dual-drift routing and unfaulted-document zero-diff evidence |
| SC-003/SC-007 | T023–T029,T030–T035 | Same-run reconcile + five-input writing plan + canonical placement/dedup + fixed lookup evidence |

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: T001 and T002 may run in parallel; both baselines must exist before Foundational changes
- **Foundational (Phase 2)**: Depends on Setup; T003 → T004 → T005 and blocks all user stories
- **US1 (Phase 3)**: Depends on T005; T007/T008/T009 may run in parallel after T006; mirror writes serialize; T013 closes the story
- **US2 (Phase 4)**: Depends on US1 target-declaration contract (T012); T014/T015 and then T016/T017 form two parallel file lanes; T022 closes the P1 MVP
- **US3 (Phase 5)**: Depends on the dual-routing harness (T021); T024/T025 may run in parallel after T023; T029 closes the story
- **Polish (Phase 6)**: Depends on all three story surface checks; shared `verification.md` writes are serialized T030 → T031 → T032 → T033 → T034 → T035

### User Story Dependencies

```text
Setup → Foundational → US1 (P1) → US2 (P1) → US3 (P2) → Polish
                             └──── MVP = US1 + US2 ────┘
```

- **US1**: Establishes the target declaration; no story dependency beyond Foundational
- **US2**: Depends on US1 because current-vs-target diffing has no stable target without the declaration
- **US3**: Depends on US2 because user-derived extra requirements are represented and dispatched as the same typed-action model

### Within Each User Story

1. Author structural contract tests and confirm RED
2. Edit canonical template/skill/reference sources only
3. Run targeted mirror/command-copy write paths
4. Verify exact mirror rows and regenerated copies
5. Run contract suite GREEN
6. Exercise the command surface in an isolated worktree and record observed evidence

### Parallel Opportunities

- T001 ∥ T002
- US1 after T006: T007 ∥ T008 ∥ T009
- US2 after T012: T014 ∥ T015; then T016 ∥ T017
- US3 after T023: T024 ∥ T025
- Polish deliberately has no parallel writes because every task appends to the single `verification.md` evidence ledger

## Parallel Example: User Story 1

```text
After T006 is RED:
  Worker A → T007 (`templates/docs-target-structure-template.md`)
  Worker B → T008 (`templates/commands/docs.md`, target-declaration stage only)
  Worker C → T009 (`skills/create-docs/SKILL.md`)

Join before mirror writes:
  T010 → T011 → T012 → T013
```

## Parallel Example: User Story 2

```text
After T012:
  Worker A → T014 (`tests/contract/test_docs_action_routing.py`)
  Worker B → T015 (`tests/contract/test_docs_skill_pair.py`)

After both RED lanes are ready:
  Worker A → T016 (`templates/commands/docs.md`)
  Worker B → T017 (`skills/improve-docs/SKILL.md`)

Join:
  T018 + T019 → T020 → T021 → T022
```

## Parallel Example: User Story 3

```text
After T023 is RED:
  Worker A → T024 (`templates/commands/docs.md`)
  Worker B → T025 (`docs/reference/commands/docs.md`)

Join:
  T026 → T027 → T028 → T029
```

## Implementation Strategy

### MVP First

The MVP is **US1 + US2**, not US1 alone: a declaration that is never consumed by typed diff/routing is only half a mechanism, while both P1 stories remain independently testable at their own checkpoints.

1. Freeze baselines (T001–T002)
2. Establish shared contract RED harness (T003–T005)
3. Deliver and verify US1 (T006–T013)
4. Deliver and verify US2 (T014–T022)
5. **STOP AND VALIDATE MVP**: rerun US1/US2 contract suites and quickstart scenarios 1–3 before beginning US3
6. Add US3 additive-input behavior (T023–T029)
7. Complete cross-cutting gates and Feature evidence (T030–T035)

### Incremental Delivery

1. **US1 increment**: persistent target declaration with no churn on a repeat run
2. **US2 increment (MVP complete)**: target diff → typed actions → correct two-skill dispatch
3. **US3 increment**: additive user requests, confirmed target writeback, and announced unbounded fan-out
4. **Polish**: mirror/gate/full-suite/Feature-memory/SC closure

### Multi-Agent Strategy

- Keep one writer per canonical file: `templates/commands/docs.md` is intentionally serialized across US1→US2→US3
- Parallelize only the different-file lanes explicitly marked `[P]`
- Never run broad `sync-mirrors.py --write`; use the targeted `--only` commands in T010/T011/T018 so unrelated `git-fleet` drift is not pulled into this feature
- Generated command copies are never hand-edited; regenerate only through `scripts/python/regen-command-copies.py`

## Notes

- `[P]` marks different-file work that is safe after its blockers close; same-file edits are intentionally serialized
- Structural tests use floor/derived semantics: no incidental hard-coded file counts; every path in a test surface list must exist or be derived from the tree
- No task adds a `docs-utils.py` action, confirmation gate, gate probe, top-level command section, runtime dependency, or new Feature
- The known `sync-mirrors.py --check` exit 2 is baseline evidence, not permission to ignore new drift; only the six `git-fleet` MISS rows and 14 migration-backup notes are pre-existing
- Surface verification uses isolated worktrees/fixtures so scenarios that create/move documentation never mutate the user's primary worktree without the existing R4 confirmation
- Prefer `[~]` with an explicit `verification.md` reason over leaving unavailable environment-dependent work `[ ]`; no external environment prerequisite is currently known
