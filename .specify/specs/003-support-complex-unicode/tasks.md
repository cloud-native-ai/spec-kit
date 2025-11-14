# Tasks: Support for Complex Prompts and Unicode (Pure Bash)

**Input**: Design documents from `/.specify/specs/003-support-complex-unicode/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story. **All implementation must be in pure Bash with no external dependencies.**

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create `scripts/bash/lib/` directory for reusable Bash functions
- [x] T002 Initialize Bats testing framework for Bash unit and integration tests

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create a Bash library function `scripts/bash/lib/safe_quote.sh` that wraps `printf '%q'` for safe argument escaping
- [x] T004 [P] Enhance the `ensure_utf8_locale` function in `scripts/bash/common.sh` to be more robust and consistently used
- [x] T005 [P] Create a Bash library function `scripts/bash/lib/validate_input.sh` to check input length and basic structure

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Execute commands with complex special characters (Priority: P1) 🎯 MVP

**Goal**: Safely handle and execute user prompts containing Bash special characters without misinterpretation, using pure Bash.

**Independent Test**: A user can submit a prompt containing a mix of special characters (e.g., `echo "Price is $100 & it's 50% off!" | grep '50%'`) and the system will generate and execute a command that correctly outputs the expected result.

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T006 [P] [US1] Contract test for special character handling in `tests/contract/test_special_chars.bats`
- [x] T007 [P] [US1] Integration test for command execution with special characters in `tests/integration/test_special_chars.bats`

### Implementation for User Story 1

- [x] T008 [US1] Modify the `create-new-feature.sh` script to source and use the `safe_quote.sh` library function for processing the `--json` argument
- [x] T009 [US1] Update the command execution logic in `create-new-feature.sh` to use the safely quoted input
- [x] T010 [US1] Add error handling in the script for scenarios where quoting might fail

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Execute commands with Unicode characters (Priority: P1)

**Goal**: Correctly handle and execute user prompts containing Unicode characters without data corruption, using pure Bash.

**Independent Test**: A user can submit a prompt containing various Unicode characters (e.g., `echo "Hello 世界! 👋"`) and the system will generate and execute a command that correctly outputs the exact same Unicode string.

### Tests for User Story 2

- [x] T011 [P] [US2] Contract test for Unicode character handling in `tests/contract/test_unicode.bats`
- [x] T012 [P] [US2] Integration test for command execution with Unicode in `tests/integration/test_unicode.bats`

### Implementation for User Story 2

- [x] T013 [US2] Ensure the `create-new-feature.sh` script calls `ensure_utf8_locale` from `common.sh` at the start of execution
- [x] T014 [US2] Update all file I/O operations in `create-new-feature.sh` to be compatible with the UTF-8 locale
- [x] T015 [US2] Verify that the `safe_quote.sh` function correctly handles Unicode characters when passed through `printf '%q'`

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Combine complex and Unicode inputs (Priority: P2)

**Goal**: Handle user prompts that combine both complex special characters and Unicode characters correctly, using pure Bash.

**Independent Test**: A user can submit a prompt like `echo "The price in 中国 is $100 & it's 50% off! 🎉"` and the system will generate a command that outputs the string exactly as provided.

### Tests for User Story 3

- [x] T016 [P] [US3] Contract test for combined special character and Unicode handling in `tests/contract/test_combined.bats`
- [x] T017 [P] [US3] Integration test for command execution with combined inputs in `tests/integration/test_combined.bats`

### Implementation for User Story 3

- [x] T018 [US3] Refactor the main input processing pipeline in `create-new-feature.sh` to seamlessly integrate the `validate_input.sh`, `ensure_utf8_locale`, and `safe_quote.sh` functions
- [x] T019 [US3] Add comprehensive logging to the command execution process to aid in debugging combined input scenarios

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Edge Cases & Polish

**Purpose**: Handle edge cases and cross-cutting concerns

- [x] T020 Implement strict input length validation (max 10,000 characters) in the `validate_input.sh` function and integrate it into `create-new-feature.sh`
- [x] T021 Add error handling for invalid or malformed UTF-8 sequences by leveraging the `C.UTF-8` locale's behavior
- [x] T022 [P] Update `quickstart.md` with final test commands and expected outputs, using pure Bash examples
- [ ] T023 [P] Run the quickstart validation to ensure all success criteria (SC-001 to SC-005) are met
- [ ] T024 Update the project's AI agent context files (e.g., `.github/copilot-instructions.md`) to reflect the new pure-Bash implementation details

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (US1 → US2 → US3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- All tests for a user story marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for special character handling in tests/contract/test_special_chars.bats"
Task: "Integration test for command execution with special characters in tests/integration/test_special_chars.bats"

# Implementation can proceed after tests are written and failing.
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently using the `quickstart.md` guide
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **MUST NOT introduce any dependency on external tools like Python**