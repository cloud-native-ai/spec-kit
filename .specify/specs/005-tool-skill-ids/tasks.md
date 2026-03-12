# Tasks: Deterministic Tool and Skill IDs

**Input**: Design documents from `.specify/specs/005-tool-skill-ids/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/deterministic-resource-ids.openapi.yaml, quickstart.md

**Tests**: Tests are required for this feature because the constitution mandates contract-driven, regression-safe changes for critical interactive flows.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions
- **Verification tasks**: Add explicit manual QA/verification tasks when they are separate from automated tests

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare shared task scaffolding for deterministic ID work across tools and skills

- [X] T001 Create deterministic ID helper module scaffold in scripts/python/manage_resource_ids.py
- [X] T002 [P] Create deterministic ID contract test files in tests/contract/test_resource_id_generation.py and tests/contract/test_resource_id_resolution.py
- [X] T003 [P] Create deterministic ID integration test files in tests/integration/test_skills_resource_ids.py and tests/integration/test_resource_id_resolution.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Implement workspace-relative canonical path normalization and validation in scripts/python/manage_resource_ids.py
- [X] T005 [P] Implement ToolRecord resource ID persistence helpers in scripts/python/manage_tool_records.py
- [X] T006 [P] Implement SkillArtifact resource ID persistence helpers in scripts/python/manage_skill_resources.py
- [X] T007 Create shared ID-first resolution service in scripts/python/resolve_resource_ids.py
- [X] T008 [P] Add reusable Resource ID sections to templates/tool-mcp-call-template.md, templates/tool-project-script-template.md, templates/tool-shell-function-template.md, templates/tool-system-binary-template.md, and templates/skills-template.md
- [X] T009 Configure deterministic ID test fixtures and workspace path helpers in tests/conftest.py

**Checkpoint**: Canonical ID infrastructure is ready; user story implementation can now begin

---

## Phase 3: User Story 1 - 生成可精确引用的唯一标识 (Priority: P1) 🎯 MVP

**Goal**: Make `/speckit.tools` and `/speckit.skills` return and persist a deterministic canonical ID whenever they create, discover, or refresh a target artifact.

**Independent Test**: Run one tool flow and one skill flow; each must return one canonical ID and persist the same value into the resulting artifact.

### Tests for User Story 1

- [X] T010 [P] [US1] Add contract coverage for ID generation responses in tests/contract/test_resource_id_generation.py
- [X] T011 [P] [US1] Extend persisted tool ID creation coverage in tests/integration/test_tools_record_creation.py
- [X] T012 [P] [US1] Add persisted skill ID creation and refresh coverage in tests/integration/test_skills_resource_ids.py

### Manual Verification for User Story 1

- [ ] T013 [US1] Validate quickstart scenarios 1 and 2 in .specify/specs/005-tool-skill-ids/quickstart.md

### Implementation for User Story 1

- [X] T014 [US1] Update scripts/bash/create-new-tools.sh to return the canonical tool record path needed for `tool_id` derivation
- [X] T015 [US1] Update templates/commands/tools.md to generate, display, and persist `tool_id` using .specify/memory/tools/<tool-name>.md
- [X] T016 [US1] Update scripts/bash/create-new-skill.sh to return the canonical skill root or SKILL.md path needed for `skill_id` derivation
- [X] T017 [US1] Update templates/commands/skills.md to generate, display, and persist `skill_id` for .github/skills/<skill-name>/SKILL.md
- [X] T018 [P] [US1] Persist generated IDs in templates/tool-mcp-call-template.md, templates/tool-project-script-template.md, templates/tool-shell-function-template.md, templates/tool-system-binary-template.md, and templates/skills-template.md

**Checkpoint**: `/speckit.tools` and `/speckit.skills` both emit deterministic IDs and save them to persisted artifacts

---

## Phase 4: User Story 2 - 用唯一标识进行后续定位 (Priority: P2)

**Goal**: Allow later commands, documents, and conversations to resolve the same tool or skill directly from the previously returned identifier.

**Independent Test**: Reuse a previously generated `tool_id` or `skill_id` and resolve the same artifact without re-running fuzzy discovery.

### Tests for User Story 2

- [X] T019 [P] [US2] Add resolve and backfill contract coverage in tests/contract/test_resource_id_resolution.py
- [X] T020 [P] [US2] Add ID-first resolution and historical backfill integration coverage in tests/integration/test_resource_id_resolution.py

### Manual Verification for User Story 2

- [ ] T021 [US2] Validate quickstart scenarios 3 and 4 in .specify/specs/005-tool-skill-ids/quickstart.md

### Implementation for User Story 2

- [X] T022 [US2] Implement resource ID resolution rules in scripts/python/resolve_resource_ids.py
- [X] T023 [US2] Update templates/commands/tools.md to accept `tool_id` references before fuzzy discovery and disambiguation
- [X] T024 [US2] Update templates/commands/skills.md to accept `skill_id` references before fuzzy discovery and disambiguation
- [X] T025 [US2] Add backfill-on-refresh behavior for historical tool records in scripts/python/manage_tool_records.py and scripts/bash/create-new-tools.sh
- [X] T026 [US2] Add backfill-on-refresh behavior for historical skill artifacts in scripts/python/manage_skill_resources.py and scripts/bash/create-new-skill.sh

**Checkpoint**: Previously generated IDs resolve deterministically, and historical artifacts can be upgraded incrementally

---

## Phase 5: User Story 3 - 在模糊匹配与精确定位之间平滑切换 (Priority: P3)

**Goal**: Preserve current natural-language discovery while making ID-based resolution the preferred path and stopping on conflicts.

**Independent Test**: Valid IDs resolve directly; invalid or conflicting inputs either fall back safely or stop with an explicit user-facing error.

### Tests for User Story 3

- [X] T027 [P] [US3] Add stale ID, conflict, and type-mismatch contract coverage in tests/contract/test_resource_id_resolution.py
- [X] T028 [P] [US3] Add stale ID, fallback, and hint-conflict integration coverage in tests/integration/test_resource_id_resolution.py
- [X] T029 [P] [US3] Add unit validation for Resource ID lifecycle states in tests/unit/test_resource_id_helpers.py and tests/unit/test_tool_record.py

### Manual Verification for User Story 3

- [ ] T030 [US3] Validate quickstart scenarios 5 and 6 plus regression expectations in .specify/specs/005-tool-skill-ids/quickstart.md

### Implementation for User Story 3

- [X] T031 [US3] Implement ID-versus-text conflict detection in scripts/python/resolve_resource_ids.py
- [X] T032 [US3] Implement stale, out-of-workspace, and invalid-type error reporting in scripts/python/manage_resource_ids.py and scripts/python/resolve_resource_ids.py
- [X] T033 [US3] Update templates/commands/tools.md to fall back to fuzzy discovery only when `tool_id` is missing or invalid
- [X] T034 [US3] Update templates/commands/skills.md to fall back to fuzzy discovery only when `skill_id` is missing or invalid

**Checkpoint**: Exact resolution, safe fallback, and conflict blocking all work without breaking existing fuzzy flows

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Sync documentation, prompt assets, feature memory, and end-to-end validation across all user stories

- [X] T035 [P] Sync generated prompt assets in .github/prompts/speckit.tools.prompt.md and .github/prompts/speckit.skills.prompt.md with the updated command templates
- [X] T036 [P] Update user-facing documentation in docs/usage.md and docs/speckit/spec-driven.md for deterministic tool and skill IDs
- [X] T037 Update feature memory references in .specify/memory/features/013.md and .specify/memory/features.md after task completion
- [X] T038 Run regression suite in tests/contract/test_resource_id_generation.py, tests/contract/test_resource_id_resolution.py, tests/integration/test_tools_record_creation.py, tests/integration/test_skills_resource_ids.py, tests/integration/test_resource_id_resolution.py, tests/unit/test_resource_id_helpers.py, and tests/unit/test_tool_record.py
- [ ] T039 Perform end-to-end quickstart and manual QA sweep using .specify/specs/005-tool-skill-ids/quickstart.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; starts immediately
- **Foundational (Phase 2)**: Depends on Setup; blocks all user story work
- **User Stories (Phases 3-5)**: Depend on Foundational completion
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Starts immediately after Foundational; defines the MVP
- **User Story 2 (P2)**: Depends on User Story 1 persistence outputs because it reuses generated IDs
- **User Story 3 (P3)**: Depends on User Story 2 resolution flow so fallback and conflict behavior can be layered on top of real ID parsing

### Within Each User Story

- Contract and integration tests first
- Manual verification after automated coverage exists
- Script/path output changes before command template changes that consume them
- Persistence before resolution
- Resolution before fallback/conflict handling

### Parallel Opportunities

- T002 and T003 can run in parallel
- T005, T006, T008, and T009 can run in parallel after T004 starts the shared path model
- US1 tests (T010-T012) can run in parallel
- US1 persistence updates (T014, T016, T018) can run in parallel before command-layer integration in T015 and T017
- US2 test work (T019-T020) can run in parallel
- US3 test work (T027-T029) can run in parallel
- Documentation sync tasks T035 and T036 can run in parallel during polish

---

## Parallel Example: User Story 1

```text
Task: T010 [US1] Add contract coverage for ID generation responses in tests/contract/test_resource_id_generation.py
Task: T011 [US1] Extend persisted tool ID creation coverage in tests/integration/test_tools_record_creation.py
Task: T012 [US1] Add persisted skill ID creation and refresh coverage in tests/integration/test_skills_resource_ids.py

Task: T014 [US1] Update scripts/bash/create-new-tools.sh to return the canonical tool record path needed for `tool_id` derivation
Task: T016 [US1] Update scripts/bash/create-new-skill.sh to return the canonical skill root or SKILL.md path needed for `skill_id` derivation
Task: T018 [US1] Persist generated IDs in the tool and skill markdown templates
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. Validate quickstart scenarios 1 and 2
5. Stop and confirm that deterministic IDs are emitted and persisted for both tool and skill flows

### Incremental Delivery

1. Deliver US1 to make ID generation visible and persistent
2. Deliver US2 to unlock deterministic follow-up resolution and historical backfill
3. Deliver US3 to preserve fuzzy discovery compatibility while enforcing safe conflict handling
4. Finish with prompt/doc sync and end-to-end regression validation

### Parallel Team Strategy

1. One developer handles shared path normalization and resolution helpers
2. One developer handles `/speckit.tools` command and tool persistence updates
3. One developer handles `/speckit.skills` command and skill persistence updates
4. After US1 lands, validation and fallback/conflict work can proceed in parallel with documentation sync

---

## Notes

- All tasks follow the required checklist format
- New helper modules under `scripts/python/` are acceptable because this feature adds shared deterministic ID logic not currently isolated in one module
- No new Feature was identified during task decomposition; Feature 013 remains the correct parent feature
- Suggested MVP scope: Phase 1 + Phase 2 + Phase 3 (User Story 1 only)