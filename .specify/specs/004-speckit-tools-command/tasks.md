# Tasks: Speckit Tools Command

**Input**: Design documents from `.specify/specs/004-speckit-tools-command/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/tools-command.openapi.yaml, quickstart.md

**Tests**: Tests are MANDATORY per Constitution Principle V (Test-Driven Development (TDD) for Interactivity).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions
- **Verification tasks**: Add explicit manual QA/verification tasks when they are separate from automated tests

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure for tools command evolution

- [x] T001 Create directory structure for new tools command assets in `.specify/memory/tools/`
- [x] T002 Initialize unified tool record schema based on data-model.md entity definitions
- [x] T003 [P] Configure tool discovery integration with existing refresh-tools.sh script

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Standardize tools.md template with unified four-source support (MCP/System/Shell/Project)
- [x] T005 [P] Update refresh-tools.sh script to support unified JSON output format for all tool sources
- [x] T006 [P] Implement tool record validation logic based on ToolRecord schema from data-model.md
- [x] T007 Create base ToolInvocationSession handler for tracking command sessions
- [x] T008 Configure tool name conflict detection and disambiguation framework
- [x] T009 Setup tool aliasing and renaming capability with ToolAlias entity support

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - 显式说明并调用工具 (Priority: P1) 🎯 MVP

**Goal**: Enable users to explicitly specify a tool and view its executable information before AI Agent invocation

**Independent Test**: User executes `/speckit.tools <tool-name>` and sees tool information summary with option to confirm or cancel execution

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T010 [P] [US1] Contract test for tool discovery endpoint in tests/contract/test_tools_discover.py
- [x] T011 [P] [US1] Integration test for tool record creation flow in tests/integration/test_tools_record_creation.py

### Manual Verification for User Story 1 (if required)

- [ ] T011A [US1] Manual QA: validate MCP tool first-time invocation using quickstart.md scenario 1

### Implementation for User Story 1

- [x] T012 [P] [US1] Implement tool discovery across four sources (MCP/System/Shell/Project) using refresh-tools.sh
- [x] T013 [P] [US1] Create ToolRecord generation logic with standardized markdown template in templates/mcptool-template.md
- [x] T014 [US1] Implement interactive parameter collection workflow for missing tool record fields
- [x] T015 [US1] Implement execution preview and confirmation step before actual tool invocation
- [ ] T016 [US1] Add error handling for tool not found scenarios with candidate suggestions
- [x] T017 [US1] Integrate tool invocation result reporting with success/failure/cancelled status

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - 复用与封装工具记录 (Priority: P2)

**Goal**: Enable reuse of existing tool records and support encapsulation/renaming capabilities

**Independent Test**: With existing tool record, user can reuse without rediscovery and apply renaming/aliasing

### Tests for User Story 2 (MANDATORY) ⚠️

- [x] T018 [P] [US2] Contract test for tool record retrieval endpoint in tests/contract/test_tools_get_record.py
- [x] T019 [P] [US2] Integration test for tool aliasing workflow in tests/integration/test_tools_aliasing.py

### Manual Verification for User Story 2 (if required)

- [ ] T019A [US2] Manual QA: validate existing record reuse and renaming using quickstart.md scenarios 3 and 5

### Implementation for User Story 2

- [x] T020 [P] [US2] Implement tool record existence check and reuse logic in tools command flow
- [x] T021 [US2] Create tool aliasing system with ToolAlias entity management
- [x] T022 [US2] Implement tool record renaming capability with conflict detection
- [x] T023 [US2] Add alias resolution logic for tool name lookups in .specify/memory/tools/

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - 泛化到多类工具生态 (Priority: P3)

**Goal**: Support unified tool visibility and invocation across MCP, System, Shell, and Project tool types

**Independent Test**: User can select tools from any of the four supported sources and complete the same record/confirmation flow

### Tests for User Story 3 (MANDATORY) ⚠️

- [x] T024 [P] [US3] Contract test for cross-source tool discovery in tests/contract/test_tools_cross_source.py
- [x] T025 [P] [US3] Integration test for source-specific tool handling in tests/integration/test_tools_source_handling.py

### Manual Verification for User Story 3 (if required)

- [ ] T025A [US3] Manual QA: validate non-MCP tool invocation using quickstart.md scenario 2

### Implementation for User Story 3

- [x] T026 [P] [US3] Implement source-type specific tool record population logic for System tools
- [x] T027 [P] [US3] Implement source-type specific tool record population logic for Shell functions
- [x] T028 [P] [US3] Implement source-type specific tool record population logic for Project scripts
- [ ] T029 [US3] Create unified tool parameter handling across different source types
- [ ] T030 [US3] Implement source-specific execution logic while maintaining unified interface

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Conflict Resolution & Edge Cases

**Purpose**: Handle complex scenarios like name conflicts, missing records, and edge cases

- [x] T031 [P] Implement same-name collision resolution across different source types
- [x] T032 [P] Add validation for incomplete tool records requiring补全 process
- [x] T033 Handle tool record naming conflicts during renaming operations
- [x] T034 Implement graceful fallback for unavailable/disconnected MCP servers

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T035 [P] Update documentation in docs/speckit/spec-driven.md for /speckit.tools command
- [x] T036 Update templates/commands/agents.md to reference new /speckit.tools command
- [ ] T037 Performance optimization for tool discovery across large tool sets
- [x] T038 [P] Additional unit tests for ToolRecord validation in tests/unit/test_tool_record.py
- [ ] T039 Security hardening for tool parameter sanitization
- [ ] T040 Run all quickstart.md validation scenarios end-to-end
- [ ] T041 Manual QA sweep for all critical paths and edge cases
- [x] T042 Update feature index entry for Feature 016 with completion status

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Conflict Resolution (Phase 6)**: Can run in parallel with User Story 3
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent but benefits from US1 completion
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independent but shares foundational components

### Within Each User Story

- Tests (MANDATORY) MUST be written and FAIL before implementation
- Discovery logic before record handling
- Record handling before execution
- Core implementation before edge case handling
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel
- Source-specific implementations within US3 marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for tool discovery endpoint in tests/contract/test_tools_discover.py"
Task: "Integration test for tool record creation flow in tests/integration/test_tools_record_creation.py"

# Launch core implementation tasks for User Story 1 together:
Task: "Implement tool discovery across four sources (MCP/System/Shell/Project) using refresh-tools.sh"
Task: "Create ToolRecord generation logic with standardized markdown template in templates/mcptool-template.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently with MCP tool scenario
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (MCP-focused)
   - Developer B: User Story 2 (Record reuse/aliasing)
   - Developer C: User Story 3 (Non-MCP sources)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Feature 016 in .specify/memory/features.md must be updated to "Completed" status upon full implementation
- All tool records must be stored in .specify/memory/tools/ with .md extension following ToolRecord schema