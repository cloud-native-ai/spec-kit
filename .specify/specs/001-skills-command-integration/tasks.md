---

description: "Task list template for feature implementation"
---

# Tasks: Skills Command Integration

**Input**: Design documents from `.specify/specs/001-skills-command-integration/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are MANDATORY per Constitution Principle IV (Test-First & Contract-Driven Implementation).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume single project - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create refresh-skills.sh script in scripts/bash/ directory
- [x] T002 Update existing create-new-skill.sh script to handle new parameter format
- [x] T003 Create skills command template in templates/commands/skills.md

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core utilities and validation functions needed by all user stories

- [x] T004 [P] Implement skill name validation function in scripts/bash/common.sh
- [x] T005 [P] Implement skill directory structure creation function in scripts/bash/common.sh
- [x] T006 [P] Implement skill specification parsing function in scripts/bash/common.sh
- [x] T007 [P] Implement error handling and feedback functions in scripts/bash/common.sh

## Phase 3: User Story 1 - Refresh Existing Skills (Priority: P1)

**Goal**: Enable developers to refresh all installed skills by running `/speckit.skills` without parameters

**Independent Test**: Can be fully tested by running `/speckit.skills` command with no arguments and verifying that all skills in `.github/skills/` directory are updated to match the latest specifications from the speckit documentation.

- [x] T008 [P] [US1] Implement skills directory detection and creation in refresh-skills.sh
- [x] T009 [P] [US1] Implement existing skills scanning logic in refresh-skills.sh
- [x] T010 [P] [US1] Implement skill refresh from current specifications in refresh-skills.sh
- [x] T011 [P] [US1] Implement missing skills creation from specifications in refresh-skills.sh
- [x] T012 [P] [US1] Implement feedback and status reporting in refresh-skills.sh
- [x] T013 [US1] Integrate refresh-skills.sh with main speckit command system

## Phase 4: User Story 2 - Create New Skill (Priority: P2)

**Goal**: Enable developers to create new skills by running `/speckit.skills "<name> - <description>"` with properly formatted parameter

**Independent Test**: Can be fully tested by running `/speckit.skills "test-skill - A test skill for validation"` and verifying that a new skill directory is created at `.github/skills/test-skill/` with proper structure and content.

- [x] T014 [P] [US2] Implement parameter parsing for "<name> - <description>" format in create-new-skill.sh
- [x] T015 [P] [US2] Implement skill name validation against naming conventions in create-new-skill.sh
- [x] T016 [P] [US2] Implement skill directory structure creation in create-new-skill.sh
- [x] T017 [P] [US2] Implement SKILL.md template population with YAML frontmatter in create-new-skill.sh
- [x] T018 [P] [US2] Implement resource directories creation (scripts, references, assets) in create-new-skill.sh
- [x] T019 [US2] Implement success confirmation and error handling in create-new-skill.sh

## Phase 5: User Story 3 - Validate Skill Structure (Priority: P3)

**Goal**: Ensure system validates that created skills follow proper structure and naming conventions

**Independent Test**: Can be tested by attempting to create skills with various naming patterns and verifying that only valid names are accepted and properly structured directories are created.

- [x] T020 [P] [US3] Enhance skill name validation to reject invalid characters (spaces, special characters) in common.sh
- [x] T021 [P] [US3] Implement skill name uniqueness checking in create-new-skill.sh
- [x] T022 [P] [US3] Implement clear error messages for invalid input formats in create-new-skill.sh
- [x] T023 [P] [US3] Implement skill directory structure validation in refresh-skills.sh
- [x] T024 [US3] Implement graceful handling of edge cases (missing directories, existing names, invalid characters)

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final integration, documentation, and quality assurance

- [x] T025 Update agent context files with new skill command capabilities
- [x] T026 Update feature documentation with implementation details
- [x] T027 Create integration tests for both command modes (refresh and create)
- [x] T028 Verify performance meets requirements (<10s for refresh, <5s for create)
- [x] T029 Update README.md and documentation to include new /speckit.skills command
- [x] T030 Final validation against all acceptance criteria from specification

## Dependencies

**User Story Completion Order**:
1. **US1 (Refresh Existing Skills)**: Must be completed first as it provides the foundational capability
2. **US2 (Create New Skill)**: Can be implemented independently but benefits from US1 validation functions
3. **US3 (Validate Skill Structure)**: Enhances both US1 and US2 with additional validation

**Parallel Execution Opportunities**:
- **Within US1**: All T008-T012 can run in parallel as they work on different aspects of the refresh functionality
- **Within US2**: All T014-T019 can run in parallel as they handle different parts of skill creation
- **Within US3**: All T020-T024 can run in parallel as they enhance validation across different scenarios
- **Cross-story**: Foundational tasks (T004-T007) can run in parallel with setup tasks (T001-T003)

## Implementation Strategy

**MVP Scope**: Implement only User Story 1 (Refresh Existing Skills) as the minimum viable product. This provides immediate value by ensuring developers have up-to-date skills.

**Incremental Delivery**:
1. **Phase 1**: Deliver MVP with refresh capability (US1)
2. **Phase 2**: Add new skill creation capability (US2) 
3. **Phase 3**: Enhance with comprehensive validation (US3)
4. **Phase 4**: Complete with polish and documentation

Each phase delivers independently testable and valuable functionality that can be used immediately by developers.