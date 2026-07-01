# Tasks: Speckit Todo Command

**Requirement ID**: 020 (from branch name)
**Requirement Key**: 020-speckit-todo-command
**Related Feature**: 025 Todo Command
**Input**: Design documents from `.specify/specs/020-speckit-todo-command/`
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/search-todo-cli.md, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates tests-first and contract/integration coverage)

**Input Analysis**: `$ARGUMENTS` is empty; used default workflow to generate a complete executable task list from available artifacts.

## Definition of Done (DoD)

- DoD-1: `/speckit.todo` supports collection mode and insertion mode per FR-001..FR-013.
- DoD-2: Contract rules in `contracts/search-todo-cli.md` are covered by automated tests and passing.
- DoD-3: Tests were written before implementation tasks within each user story phase.
- DoD-4: User Story 1, User Story 2, and User Story 3 can each be verified independently using their independent test criteria.
- DoD-5: Feature tracking updated in `.specify/memory/features.md` and `.specify/memory/features/025.md` with task-breakdown notes.
- DoD-6: Documentation and quickstart references reflect final command behavior.

**DoD Status**: green

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare fixtures, prompt file, and script entry points used by all stories.

- [X] T001 Create fixture folders and seed placeholders in `tests/fixtures/todo-workspaces/valid/`, `tests/fixtures/todo-workspaces/malformed/`, `tests/fixtures/todo-workspaces/empty/`, `tests/fixtures/todo-workspaces/negative/`, and `tests/fixtures/todo-workspaces/oversized/`
- [X] T002 [P] Add valid extraction fixtures with multiple marked blocks in `tests/fixtures/todo-workspaces/valid/docs/auth.md` and `tests/fixtures/todo-workspaces/valid/src/workflow.md`
- [X] T003 [P] Add malformed fence fixtures in `tests/fixtures/todo-workspaces/malformed/broken.md`
- [X] T004 [P] Add negative fixtures for ordinary TODO text and ignored-like content in `tests/fixtures/todo-workspaces/negative/plain_todos.md`
- [X] T005 [P] Add oversized fixture containing >10 valid TODO blocks in `tests/fixtures/todo-workspaces/oversized/backlog.md`
- [X] T006 Create scanner contract test module skeleton in `tests/contract/test_search_todo_contract.py`
- [X] T007 [P] Create prompt integration test module skeleton in `tests/integration/test_speckit_todo_prompt.py`
- [X] T008 Create `/speckit.todo` prompt template skeleton in `.github/prompts/speckit.todo.prompt.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Build shared scanner and insertion primitives that block all stories.

- [X] T009 Extend shared helpers for root/path and JSON escaping in `.specify/scripts/bash/common-todo.sh`
- [X] T010 Implement reusable default exclude patterns and custom exclude merge logic in `.specify/scripts/bash/common-todo.sh`
- [X] T011 Implement UTF-8 and size guard helpers (`encoding_error`, `too_large`) in `.specify/scripts/bash/common-todo.sh`
- [X] T012 Create `search-todo.sh` CLI scaffold with option parsing and exit-code baseline in `.specify/scripts/bash/search-todo.sh`
- [X] T013 Implement marker fence parser state machine API in `.specify/scripts/bash/search-todo.sh`
- [X] T014 Implement output serializer stubs for key:value and `--json` modes in `.specify/scripts/bash/search-todo.sh`

**Checkpoint**: Shared scanner infrastructure is ready; story phases can proceed.

---

## Phase 3: User Story 1 - Collect TODO markers (Priority: P1) 🎯 MVP

**Goal**: Collect every valid marked TODO block with source and paragraph-boundary context while excluding non-eligible content.

**Independent Test**: Run scanner against mixed fixtures and verify each valid block appears once with correct file/context; ordinary TODOs and excluded content are ignored.

### Tests for User Story 1 (MANDATORY)

- [X] T015 [P] [US1] Add contract test for D-1 and D-8 marker matching behavior in `tests/contract/test_search_todo_contract.py`
- [X] T016 [P] [US1] Add contract test for D-2 closing-fence matching behavior in `tests/contract/test_search_todo_contract.py`
- [X] T017 [P] [US1] Add contract test for D-5 exclusion behavior (ignored/dependency/binary-like) in `tests/contract/test_search_todo_contract.py`
- [X] T018 [P] [US1] Add contract tests for C-1/C-2/C-3 context extraction in `tests/contract/test_search_todo_contract.py`
- [X] T019 [P] [US1] Add contract test for JSON schema and deterministic ordering in `tests/contract/test_search_todo_contract.py`
- [X] T020 [P] [US1] Add contract tests for SC-001 and SC-002 fixtures in `tests/contract/test_search_todo_contract.py`

### Implementation for User Story 1

- [X] T021 [US1] Implement file traversal with default/custom excludes in `.specify/scripts/bash/search-todo.sh`
- [X] T022 [US1] Implement SPECKIT TODO fenced-block extraction and ordering in `.specify/scripts/bash/search-todo.sh`
- [X] T023 [US1] Implement context heading/prologue/epilogue extraction with `--context-depth` and `--context-only-headings` in `.specify/scripts/bash/search-todo.sh`
- [X] T024 [US1] Implement final key:value output lines and block/malformed summaries in `.specify/scripts/bash/search-todo.sh`
- [X] T025 [US1] Implement final JSON output object and escaping compliance in `.specify/scripts/bash/search-todo.sh`
- [X] T026 [US1] Run focused contract tests for US1 scanner behavior in `tests/contract/test_search_todo_contract.py`

**Checkpoint**: Collection mode is independently functional and contract-compliant.

---

## Phase 4: User Story 2 - Insert TODO at specified location (Priority: P1)

**Goal**: Support insertion mode that parses user description, validates target file/location, and inserts a conforming `SPECKIT TODO` block only at the requested location.

**Independent Test**: Provide insertion description and verify marker block insertion at target; verify missing file path fails without creating files.

### Tests for User Story 2 (MANDATORY)

- [X] T027 [P] [US2] Add integration test for insertion-argument parsing (target file, location, content) in `tests/integration/test_speckit_todo_prompt.py`
- [X] T028 [P] [US2] Add integration test for conforming block insertion format in `tests/integration/test_speckit_todo_prompt.py`
- [X] T029 [P] [US2] Add integration test for non-existent target file hard-fail behavior in `tests/integration/test_speckit_todo_prompt.py`
- [X] T029A [P] [US2] Add integration test for non-writable target file rejection in `tests/integration/test_speckit_todo_prompt.py`
- [X] T030 [P] [US2] Add integration test for preserving surrounding content (insert-only delta) in `tests/integration/test_speckit_todo_prompt.py`

### Implementation for User Story 2

- [X] T031 [US2] Implement insertion-mode workflow in `.github/prompts/speckit.todo.prompt.md` (`--insert` path, description parsing, validation steps)
- [X] T032 [US2] Implement insertion formatting rules and marker synthesis in `.github/prompts/speckit.todo.prompt.md`
- [X] T033 [US2] Implement location-based insertion procedure, no-create-on-missing-file guard, and writable-file check in `.github/prompts/speckit.todo.prompt.md`
- [X] T034 [US2] Implement insertion error/report messages and exit behavior contract in `.github/prompts/speckit.todo.prompt.md`
- [X] T035 [US2] Run focused integration tests for US2 insertion behavior in `tests/integration/test_speckit_todo_prompt.py`

**Checkpoint**: Insertion mode is independently functional with safe file handling.

---

## Phase 5: User Story 3 - Handle scan and insertion safely (Priority: P2)

**Goal**: Provide robust malformed reporting, no-op behavior, and safe bounded execution/batching for risky or high-volume scenarios.

**Independent Test**: Run against empty/malformed/oversized and invalid insertion targets; verify clear diagnostics and bounded behavior.

### Tests for User Story 3 (MANDATORY)

- [X] T036 [P] [US3] Add contract test for D-3 unclosed fence malformed reporting in `tests/contract/test_search_todo_contract.py`
- [X] T037 [P] [US3] Add contract test for D-4 nested fence handling in `tests/contract/test_search_todo_contract.py`
- [X] T038 [P] [US3] Add contract test for D-6/D-7 encoding and file-size exclusion diagnostics in `tests/contract/test_search_todo_contract.py`
- [X] T039 [P] [US3] Add contract test for FR-012 no-op response when zero valid blocks in `tests/contract/test_search_todo_contract.py`
- [X] T040 [P] [US3] Add integration test for FR-013 batching behavior (>10 blocks, max 5 per batch) in `tests/integration/test_speckit_todo_prompt.py`
- [X] T041 [P] [US3] Add integration test for malformed exclusion from execution planning in `tests/integration/test_speckit_todo_prompt.py`
- [X] T042 [P] [US3] Add integration test for destructive/out-of-scope TODO safety veto in `tests/integration/test_speckit_todo_prompt.py`

### Implementation for User Story 3

- [X] T043 [US3] Implement malformed detection and malformed array records in `.specify/scripts/bash/search-todo.sh`
- [X] T044 [US3] Implement warning/info stderr messages and exit-code behavior in `.specify/scripts/bash/search-todo.sh`
- [X] T045 [US3] Implement no-action result path for empty scans in `.github/prompts/speckit.todo.prompt.md`
- [X] T046 [US3] Implement batching orchestration and confirmation gates in `.github/prompts/speckit.todo.prompt.md` (FR-013: when total_blocks > 10, split into batches of ≤5 groups each, present sequentially)
- [X] T047 [US3] Implement malformed exclusion and risky-action veto policy in `.github/prompts/speckit.todo.prompt.md`
- [X] T048 [US3] Run focused contract/integration tests for US3 safety behavior in `tests/contract/test_search_todo_contract.py` and `tests/integration/test_speckit_todo_prompt.py`

**Checkpoint**: Safety and edge-case handling is independently functional.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, docs, and feature bookkeeping.

- [X] T049 Update command documentation to include `/speckit.todo` behavior in `docs/usage.md`
- [X] T050 [P] Add command-focused documentation page in `docs/commands/todo.md`
- [X] T051 [P] Add/refresh quickstart verification notes for todo workflow in `docs/quickstart.md`
- [X] T052 Update feature detail notes after task breakdown in `.specify/memory/features/025.md`
- [X] T053 Update feature index status/date for feature 025 in `.specify/memory/features.md`
- [X] T054 Run targeted test commands for todo contract/integration suites and record results in `.specify/specs/020-speckit-todo-command/verification.md`
- [X] T055 Re-run consistency review and record deferred items (if any) in `.specify/specs/020-speckit-todo-command/verification.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- Phase 1 → Phase 2 → User Stories (Phase 3-5) → Phase 6.
- Phase 2 is blocking for all stories.
- Story execution order by priority: US1 (P1) and US2 (P1) first, then US3 (P2).

### User Story Dependencies

- US1 depends only on foundational scanner primitives from Phase 2.
- US2 depends on prompt skeleton from Phase 1 and shared validation helpers from Phase 2.
- US3 depends on outputs from US1/US2 to enforce safety and batching policies.

### Within Each Story

- Tests first, then implementation, then focused verification.

## Parallel Opportunities

- Phase 1: T002-T005 and T007 are parallelizable.
- US1: T015-T020 can run in parallel; T021-T025 remain mostly sequential.
- US2: T027-T030 can run in parallel; T031-T034 are sequential.
- US3: T036-T042 can run in parallel; T043-T047 are sequential.
- Phase 6: T050, T051 can run in parallel with non-conflicting files.

## Parallel Example: User Story 1

```bash
# Parallel tests
T015 + T016 + T017 + T018 + T019 + T020

# Then sequential implementation
T021 -> T022 -> T023 -> T024 -> T025 -> T026
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 and Phase 2.
2. Deliver US1 (Phase 3) as MVP for discovery value.
3. Deliver US2 insertion support.
4. Deliver US3 safety and batching.
5. Finish cross-cutting docs and feature tracking updates.

### Incremental Delivery

- Increment 1: Collection mode + scanner contract compliance (US1).
- Increment 2: Insertion mode in prompt workflow (US2).
- Increment 3: Safety hardening, malformed handling, batching (US3).
- Increment 4: Documentation and feature governance updates.
