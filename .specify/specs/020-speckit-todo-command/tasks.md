# Tasks: Speckit Todo Command

**Requirement ID**: 020 (from branch 020-speckit-todo-command)
**Requirement Key**: 020-speckit-todo-command
**Related Feature**: 025 Todo Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/020-speckit-todo-command/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/search-todo-cli.md, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is NON-NEGOTIABLE; Layer-1 unit + Layer-2 validation required)

**Tests**: When Tests Mode is ON, the examples below include test tasks and they are MANDATORY. When OFF, remove the test rows entirely (do NOT leave empty placeholders).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: Code implemented according to specification
- DoD-2: All automated tests pass (unit, integration, contract)
- DoD-3: Manual verification completed where applicable
- DoD-4: Documentation updated (inline comments, README, etc.)
- DoD-5: Code reviewed and approved
- DoD-6: Changes validated against success criteria from requirements.md
- DoD-7: Test-first workflow followed: tests written before implementation for each story

**DoD Status**: pending

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions
- **Verification tasks**: Add explicit manual QA/verification tasks when they are separate from automated tests

### Task State Sigil (REQUIRED)

Each task row starts with one of three checkbox states. They are first-class — `/speckit.implement` parses them and `/speckit.review` enumerates them across features.

- `- [ ]` — **Open**. Task has not been completed. A run is NOT complete while any `[ ]` remains.
- `- [X]` — **Closed**. Task has been fully executed and verified.
- `- [~]` — **Deferred**. Task is intentionally handed off to the user (or to a later phase). Reasons must be recorded in `verification.log` under `deferred_tasks=` and ideally a one-line `<!-- deferred: <reason> -->` inline comment on the task row itself. Typical deferral causes: Layer-2 docker smoke build requiring a real docker daemon, external system access not available in CI, multi-day backfill.

A `/speckit.implement` run is considered complete when **zero `[ ]` rows remain**. `[~]` rows are allowed at completion and surface in the run summary's "Deferred Tasks" block.

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Scripts**: `.specify/scripts/bash/` for shell scripts
- **Prompts**: `.github/prompts/` for agent prompt templates
- **Fixtures**: `tests/fixtures/todo-workspaces/` for test fixtures
- **Contracts**: `.specify/specs/020-speckit-todo-command/contracts/` for CLI contracts

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create project structure and test scaffolding for the todo command feature.

- [ ] T001 Create fixture directory structure in tests/fixtures/todo-workspaces/ with subdirectories: valid/, malformed/, empty/, negative/, oversized/, mixed/
- [ ] T002 [P] Create valid workspace fixture in tests/fixtures/todo-workspaces/valid/ with 3 test files containing SPECKIT TODO blocks (docs/auth.md, src/api.py, tests/integration.rs)
- [ ] T003 [P] Create malformed workspace fixture in tests/fixtures/todo-workspaces/malformed/ with unclosed fence, nested fence, and unparseable examples
- [ ] T004 [P] Create empty workspace fixture in tests/fixtures/todo-workspaces/empty/ with no TODO blocks
- [ ] T005 [P] Create negative workspace fixture in tests/fixtures/todo-workspaces/negative/ with ordinary TODO comments (not SPECKIT TODO markers) and binary files
- [ ] T006 [P] Create oversized workspace fixture in tests/fixtures/todo-workspaces/oversized/ with 15+ SPECKIT TODO blocks to test batching threshold (FR-011)
- [ ] T007 Create test conftest.py in tests/contract/ with helper functions for loading fixtures and validating JSON schema
- [ ] T008 [P] Create shared bash helper functions in .specify/scripts/bash/common-todo.sh for JSON escaping, repo root discovery, and path normalization

**Checkpoint**: All fixtures ready; test infrastructure in place.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [ ] T009 Implement repo root discovery function in .specify/scripts/bash/common-todo.sh (reuses logic from create-new-plan.sh)
- [ ] T010 Implement JSON string escaping function in .specify/scripts/bash/common-todo.sh (handles newlines, quotes, backslashes per RFC 8259)
- [ ] T011 Implement default exclude list in .specify/scripts/bash/common-todo.sh (.git/, .venv/, node_modules/, __pycache__/, .specify/specs/*/contracts/, .specify/specs/*/checklists/)
- [ ] T012 Implement gitignore-style pattern matching function in .specify/scripts/bash/common-todo.sh for --exclude support
- [ ] T013 Implement UTF-8 encoding detection function in .specify/scripts/bash/common-todo.sh (checks first 8192 bytes for non-UTF-8 sequences)
- [ ] T014 Implement file size check function in .specify/scripts/bash/common-todo.sh (rejects files > 16 MB)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Discover actionable TODO blocks (Priority: P1) 🎯 MVP

**Goal**: Implement core scanner that discovers SPECKIT TODO blocks in workspace text files and emits structured JSON/key:value output.

**Independent Test**: Add marked TODO blocks to multiple text files, run `./search-todo.sh`, and verify that each block appears exactly once with its originating file and surrounding context.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T015 [P] [US1] Contract test for D-1 discovery rule (opening fence contains SPECKIT TODO) in tests/contract/test_search_todo_script.py::test_discovery_rule_d1
- [ ] T016 [P] [US1] Contract test for D-2 discovery rule (closing fence matching) in tests/contract/test_search_todo_script.py::test_discovery_rule_d2
- [ ] T017 [P] [US1] Contract test for D-5 exclusion (binary/dependency/ignored files) in tests/contract/test_search_todo_script.py::test_discovery_rule_d5
- [ ] T018 [P] [US1] Contract test for D-8 case-exact matching in tests/contract/test_search_todo_script.py::test_discovery_rule_d8
- [ ] T019 [P] [US1] Contract test for C-1 context heading extraction in tests/contract/test_search_todo_script.py::test_context_rule_c1
- [ ] T020 [P] [US1] Contract test for C-2 prologue context (paragraph-boundary upward) in tests/contract/test_search_todo_script.py::test_context_rule_c2
- [ ] T021 [P] [US1] Contract test for C-3 epilogue context (paragraph-boundary downward) in tests/contract/test_search_todo_script.py::test_context_rule_c3
- [ ] T022 [P] [US1] Contract test for JSON output schema (§4.2) in tests/contract/test_search_todo_script.py::test_json_output_schema
- [ ] T023 [P] [US1] Contract test for key:value output format (§4.1) in tests/contract/test_search_todo_script.py::test_keyvalue_output_format
- [ ] T024 [P] [US1] Contract test for deterministic block ordering (source_file ASC, opening_line ASC) in tests/contract/test_search_todo_script.py::test_deterministic_ordering
- [ ] T025 [P] [US1] Contract test for SC-001 success criterion (25 blocks across 10 files, 100% match, zero duplicates) in tests/contract/test_search_todo_script.py::test_sc001_full_discovery
- [ ] T026 [P] [US1] Contract test for SC-002 success criterion (negative cases: ordinary TODO comments excluded) in tests/contract/test_search_todo_script.py::test_sc002_negative_exclusion

### Manuals Verification for User Story 1 (if required)

- [ ] T026A [US1] Manual QA: run search-todo.sh against valid fixture, verify output matches expected JSON schema and block count

### Implementation for User Story 1

- [ ] T027 [US1] Create search-todo.sh script skeleton in .specify/scripts/bash/search-todo.sh with --help output (exit 0)
- [ ] T028 [US1] Implement argument parsing in search-todo.sh (--json, --root, --exclude, --no-default-excludes, --context-depth, --context-only-headings)
- [ ] T029 [US1] Implement workspace file traversal in search-todo.sh using find with default excludes from common-todo.sh
- [ ] T030 [US1] Implement awk-based fence state machine in search-todo.sh to detect SPECKIT TODO opening/closing fences (D-1, D-2)
- [ ] T031 [US1] Implement case-exact substring matching for SPECKIT TODO marker (D-8) in search-todo.sh
- [ ] T032 [US1] Implement context heading extraction (C-1) in search-todo.sh via awk
- [ ] T033 [US1] Implement prologue context extraction (C-2) in search-todo.sh (paragraph-boundary upward, capped by --context-depth)
- [ ] T034 [US1] Implement epilogue context extraction (C-3) in search-todo.sh (paragraph-boundary downward, capped by --context-depth)
- [ ] T035 [US1] Implement JSON output formatting in search-todo.sh using common-todo.sh escaping (all fields present, RFC 8259 escaping)
- [ ] T036 [US1] Implement key:value output formatting in search-todo.sh (BRANCH, REPO_ROOT, TOTAL_FILES, TOTAL_BLOCKS, MALFORMED, EXCLUDED_FILES, SCANNED_AT, BLOCK[i], MALFORMED[i])
- [ ] T037 [US1] Implement deterministic block ordering (source_file ASC, opening_line ASC) in search-todo.sh
- [ ] T038 [US1] Add stderr diagnostics: "search-todo: info: scanned <N> files in <S> seconds" per contract §7
- [ ] T039 [US1] Run contract tests for US1, ensure all pass (T015-T026)

**Checkpoint**: Core scanner working; can discover SPECKIT TODO blocks with full context.

---

## Phase 4: User Story 2 - Generate execution-ready todo plan (Priority: P2)

**Goal**: Implement agent prompt template that consumes scanner JSON, groups related blocks, and generates a reviewable execution plan.

**Independent Test**: Create a TODO block describing a specific change, run `/speckit.todo` in agent chat, and verify the produced plan contains ordered tasks, affected context, validation expectations, and execution boundaries.

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T040 [P] [US2] Integration test for prompt template structure (required sections: User Input, Outline, Handoffs) in tests/integration/test_todo_prompt.py::test_prompt_structure
- [ ] T041 [P] [US2] Integration test for FR-008 (combine TODO content and source context into prompt) in tests/integration/test_todo_prompt.py::test_fr008_prompt_generation
- [ ] T042 [P] [US2] Integration test for FR-009 (plan includes grouped work items, source refs, intended outcomes, safety notes, validation expectations) in tests/integration/test_todo_prompt.py::test_fr009_plan_elements
- [ ] T043 [P] [US2] Integration test for FR-010 (present plan before execution, require confirmation) in tests/integration/test_todo_prompt.py::test_fr010_review_gate
- [ ] T044 [P] [US2] Integration test for grouping logic (same_file, same_heading, same_topic affinity) in tests/integration/test_todo_prompt.py::test_grouping_affinity

### Manual Verification for User Story 2 (if required)

- [ ] T044A [US2] Manual QA: create a TODO block in quickstart.md style, run `/speckit.todo` in agent chat, verify plan groups blocks by topic and includes all FR-009 elements

### Implementation for User Story 2

- [ ] T045 [US2] Create speckit.todo.prompt.md in .github/prompts/speckit.todo.prompt.md with User Input, Outline, and Handoffs sections
- [ ] T046 [US2] Define outline workflow in speckit.todo.prompt.md: (1) run search-todo.sh --json, (2) parse JSON, (3) group blocks by affinity, (4) generate plan, (5) present for review, (6) execute after confirmation
- [ ] T047 [US2] Implement grouping logic in prompt template: same_file affinity (blocks in same source_file), same_heading affinity (blocks under same Markdown heading), same_topic affinity (heuristic: similar content keywords)
- [ ] T048 [US2] Implement plan generation in prompt template: for each group, output (source references, intended outcomes, safety notes, validation expectations)
- [ ] T049 [US2] Implement review gate in prompt template: before any workspace modifications, agent MUST present plan and wait for explicit user confirmation (FR-010)
- [ ] T050 [US2] Implement execution logic in prompt template: after confirmation, agent executes each group's tasks in order
- [ ] T051 [US2] Run integration tests for US2, ensure all pass (T040-T044)

**Checkpoint**: Prompt template complete; agent can generate and execute plans from TODO blocks.

---

## Phase 5: User Story 3 - Handle scan outcomes safely (Priority: P3)

**Goal**: Implement malformed block detection, batching logic (FR-011), and safety vetoes for destructive/out-of-scope TODOs.

**Independent Test**: Run the command against empty, malformed, and oversized TODO examples and verify that the command gives clear status messages and bounded next steps.

### Tests for User Story 3 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T052 [P] [US3] Contract test for D-3 malformed detection (unclosed fence) in tests/contract/test_search_todo_script.py::test_malformed_d3_unclosed_fence
- [ ] T053 [P] [US3] Contract test for D-4 malformed detection (nested fence) in tests/contract/test_search_todo_script.py::test_malformed_d4_nested_fence
- [ ] T054 [P] [US3] Contract test for D-6 malformed detection (encoding error) in tests/contract/test_search_todo_script.py::test_malformed_d6_encoding_error
- [ ] T055 [P] [US3] Contract test for D-7 malformed detection (too_large > 16 MB) in tests/contract/test_search_todo_script.py::test_malformed_d7_too_large
- [ ] T056 [P] [US3] Contract test for FR-012 (no-op result when no valid TODO blocks found) in tests/contract/test_search_todo_script.py::test_fr012_noop
- [ ] T057 [P] [US3] Integration test for FR-011 (batching: >10 blocks → max 5 per batch) in tests/integration/test_todo_batching.py::test_fr011_batching_threshold
- [ ] T058 [P] [US3] Integration test for FR-007 (malformed blocks excluded from automatic execution planning) in tests/integration/test_todo_batching.py::test_fr007_malformed_exclusion
- [ ] T059 [P] [US3] Contract test for SC-004 success criterion (malformed fixtures: 100% reported location, 100% excluded from plan) in tests/contract/test_search_todo_script.py::test_sc004_malformed_reporting

### Manual Verification for User Story 3 (if required)

- [ ] T059A [US3] Manual QA: run search-todo.sh against malformed fixture, verify stderr warnings match contract §7 error messages
- [ ] T059B [US3] Manual QA: run search-todo.sh against oversized fixture (15 blocks), verify prompt batches into 3 batches of 5 blocks each (FR-011)

### Implementation for User Story 3

- [ ] T060 [US3] Implement D-3 malformed detection (unclosed fence: opening fence with no matching closing fence before EOF) in search-todo.sh
- [ ] T061 [US3] Implement D-4 malformed detection (nested fence: SPECKIT TODO inside another fenced block) in search-todo.sh
- [ ] T062 [US3] Implement D-6 malformed detection (encoding_error: non-UTF-8 in first 8192 bytes) in search-todo.sh using common-todo.sh helper
- [ ] T063 [US3] Implement D-7 malformed detection (too_large: file > 16 MB) in search-todo.sh using common-todo.sh helper
- [ ] T064 [US3] Add stderr warnings for malformed blocks per contract §7: "search-todo: warning: excluded file (encoding_error): <path>", "search-todo: warning: excluded file (too_large): <path>"
- [ ] T065 [US3] Implement FR-012 no-op result in prompt template: when search-todo.sh reports TOTAL_BLOCKS: 0, agent MUST output clear "no actionable blocks found" message and perform no planning work
- [ ] T066 [US3] Implement FR-011 batching logic in prompt template: when JSON counters.total_blocks_found > 10, agent MUST split groups into batches (max 5 groups per batch) and present each batch sequentially for review and execution
- [ ] T067 [US3] Implement FR-007 safety gate in prompt template: malformed blocks (JSON malformed array) MUST be reported with source_file and opening_line but excluded from any ExecutionBatch
- [ ] T068 [US3] Implement safety veto in prompt template: agent MUST reject TODO blocks that request destructive operations (rm -rf /, format C:, etc.), secret exposure (export API keys, commit .env, etc.), or out-of-scope work (tasks unrelated to the project)
- [ ] T069 [US3] Run contract tests for US3, ensure all pass (T052-T059)

**Checkpoint**: All safety mechanisms in place; command handles edge cases correctly.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, integration tests, and final validation.

- [ ] T070 Update README.md to add /speckit.todo to the command list (in installation.md verification checklist)
- [ ] T071 [P] Create example usage documentation in docs/commands/todo.md with quickstart-style walkthrough
- [ ] T072 [P] Add /speckit.todo to .specify/memory/features.md Feature Index (already tracked as Feature 025)
- [ ] T073 Run full test suite (contract + integration) and ensure all tests pass
- [ ] T074 Manual QA: run /speckit.todo end-to-end against a real workspace, verify plan generation and execution
- [ ] T075 Verify success criteria: SC-001 (25 blocks, 100% match), SC-002 (negative exclusion), SC-003 (<10 sec trace-back), SC-004 (malformed reporting), SC-005 (90% correct next-action identification)
- [ ] T076 Update .specify/memory/features/025.md with implementation complete status and key changes
- [ ] T077 [P] Add inline code comments to search-todo.sh explaining awk state machine and JSON escaping
- [ ] T078 Verify contract compliance: all 7 constitution principles pass (re-check from plan.md)

---

## Dependency Graph

```
Phase 1: T001-T008 (fixtures, common helpers)
    ↓
Phase 2: T009-T014 (foundational bash helpers) [BLOCKING for all user stories]
    ↓
Phase 3: T015-T039 (US1 - discovery) [MVP, can be tested independently]
    ↓
Phase 4: T040-T051 (US2 - plan generation) [depends on US1 JSON output]
    ↓
Phase 5: T052-T069 (US3 - safety) [depends on US1 malformed detection]
    ↓
Phase 6: T070-T078 (polish) [runs after all stories complete]
```

## Parallel Execution Examples per Story

### Phase 1 (Setup) - Parallel Opportunities
- T002-T006 (fixture creation) are **independent** — can run in parallel
- T008 (common-todo.sh) depends on T001 but is independent of fixtures

### Phase 3 (US1 - Discovery) - Parallel Opportunities
- T015-T026 (contract tests) are **independent** — can run in parallel (different test functions)
- T032-T034 (context extraction) are **independent** — can run in parallel (different awk sections)
- T035-T036 (output formatting) are **independent** — can run in parallel (JSON vs key:value)

### Phase 4 (US2 - Plan Generation) - Parallel Opportunities
- T040-T044 (integration tests) are **independent** — can run in parallel (different test functions)
- T046-T048 (prompt template sections) are **sequential** — outline → grouping → plan generation

### Phase 5 (US3 - Safety) - Parallel Opportunities
- T052-T059 (contract/integration tests) are **independent** — can run in parallel (different test functions)
- T060-T063 (malformed detection) are **sequential** — D-3 → D-4 → D-6 → D-7
- T065-T068 (prompt template safety) are **sequential** — FR-012 → FR-011 → FR-007 → safety veto

### Phase 6 (Polish) - Parallel Opportunities
- T071-T072 (documentation) are **independent** — can run in parallel
- T077 (inline comments) is independent of T070-T075

## Implementation Strategy

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (T001-T039) delivers the core discovery capability. User Story 1 can be tested independently and provides immediate value.

**Incremental Delivery**:
1. **Phase 1-3 (US1)**: Core scanner with contract tests — deliverable MVP
2. **Phase 4 (US2)**: Agent prompt template — enables plan generation
3. **Phase 5 (US3)**: Safety mechanisms — production-ready
4. **Phase 6 (Polish)**: Documentation and validation — complete feature

**Test-First Workflow**: For each story phase, tests are written BEFORE implementation. The `/speckit.implement` agent MUST run tests after each task and ensure they pass before moving to the next task.
