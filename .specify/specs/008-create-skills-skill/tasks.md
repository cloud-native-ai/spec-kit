# Tasks: Create Skills Skill

**Requirement ID**: 008
**Requirement Key**: 008-create-skills-skill
**Related Feature**: 013 Skills Command
**Input**: Design documents from `.specify/specs/008-create-skills-skill/`
**Prerequisites**: plan.md, requirements.md, research.md, data-model.md, contracts/create-skills-workflow.openapi.yaml, quickstart.md

**User Input Analysis**: `$ARGUMENTS` is empty. Input type is empty/background-neutral, so no extra task outline or additional task entries are merged.
**Input Handling Strategy**: Generate a complete executable task list from available design artifacts, preserving the default user-story organization and validation workflow.

**Tests**: Automated test tasks are included because the Constitution requires test-first implementation and the plan calls for targeted prompt/Skill asset assertions plus existing pytest regression checks.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- [ ] Code and prompt assets implemented according to requirements.md
- [ ] All automated tests pass for prompt assets, Skill layout, and resource IDs
- [ ] Manual quickstart validation completed for creation and improvement routing
- [ ] Feature memory references remain aligned with Feature 013
- [ ] Changes validated against success criteria SC-001 through SC-005

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files or depends only on completed setup/foundation
- **[Story]**: User story label for story phases only
- Every task includes exact repository-relative file paths

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the implementation workspace and identify the source guidance to extract.

- [x] T001 Verify current feature artifacts in .specify/specs/008-create-skills-skill/plan.md and .specify/specs/008-create-skills-skill/requirements.md
- [x] T002 [P] Create the source Skill directory at skills/create-skills/ for the new reusable Skill
- [x] T003 [P] Create the current-workspace mirror directory at .specify/skills/create-skills/ for discoverability during local validation
- [x] T004 [P] Create prompt asset test scaffold in tests/contract/test_create_skills_prompt_assets.py
- [x] T005 Review the inline creation workflow currently in templates/commands/skills.md and identify creation-only sections to move into skills/create-skills/SKILL.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Add failing guardrails before changing prompt assets and define extraction boundaries shared by all stories.

**⚠️ CRITICAL**: No user story implementation should begin until these checks exist and fail against the current state.

- [x] T006 [P] Add failing frontmatter and required-section tests for skills/create-skills/SKILL.md in tests/contract/test_create_skills_prompt_assets.py
- [x] T007 [P] Add failing routing tests for missing-target `create-skills` and existing-target `improve-skills` language in templates/commands/skills.md using tests/contract/test_create_skills_prompt_assets.py
- [x] T008 [P] Add failing duplication-boundary tests that reject full creation methodology remaining in templates/commands/skills.md using tests/contract/test_create_skills_prompt_assets.py
- [x] T009 [P] Add failing packaging assertion that pyproject.toml still force-includes the root skills/ directory in tests/contract/test_create_skills_prompt_assets.py
- [x] T010 Document the extracted creation responsibility checklist in .specify/specs/008-create-skills-skill/checklists/create-skills-extraction.md

**Checkpoint**: Failing tests and extraction checklist are ready; user story implementation can proceed.

---

## Phase 3: User Story 1 - Create new skills through a dedicated capability (Priority: P1) 🎯 MVP

**Goal**: Provide a reusable `create-skills` Skill at `skills/create-skills/SKILL.md` that owns new Skill creation guidance.

**Independent Test**: A maintainer can open `skills/create-skills/SKILL.md` and follow it end-to-end to create a new Skill without relying on creation-specific instructions from `templates/commands/skills.md`.

### Tests for User Story 1

- [x] T011 [P] [US1] Run failing Skill existence/frontmatter checks in tests/contract/test_create_skills_prompt_assets.py for skills/create-skills/SKILL.md
- [x] T012 [P] [US1] Add and run failing checks for explicit-input and conversation-history creation guidance in tests/contract/test_create_skills_prompt_assets.py

### Implementation for User Story 1

- [x] T013 [US1] Create skills/create-skills/SKILL.md with YAML frontmatter containing `name: create-skills`, a trigger-rich `description`, and `skill_id: "<SKILL:.specify/skills/create-skills/SKILL.md>"`
- [x] T014 [US1] Move explicit user input parsing, valid Skill name rules, and description extraction guidance from templates/commands/skills.md into skills/create-skills/SKILL.md
- [x] T015 [US1] Move empty-argument conversation distillation guidance from templates/commands/skills.md into skills/create-skills/SKILL.md
- [x] T016 [US1] Add minimal clarification rules and one-question-at-a-time behavior to skills/create-skills/SKILL.md
- [x] T017 [US1] Add completion reporting requirements with created path, `skill_id`, example prompts, and follow-up actions to skills/create-skills/SKILL.md
- [x] T018 [US1] Mirror the completed Skill content from skills/create-skills/SKILL.md to .specify/skills/create-skills/SKILL.md for current-workspace discovery

**Checkpoint**: User Story 1 delivers the MVP dedicated creation capability.

---

## Phase 4: User Story 2 - Keep command prompts focused on orchestration (Priority: P2)

**Goal**: Refactor `templates/commands/skills.md` into a concise router that parses intent, checks target existence, and delegates to the correct Skill.

**Independent Test**: A reviewer can identify missing-target and existing-target routing in `templates/commands/skills.md` in under 2 minutes, with no duplicated creation playbook inline.

### Tests for User Story 2

- [x] T019 [P] [US2] Run failing routing-language checks in tests/contract/test_create_skills_prompt_assets.py for templates/commands/skills.md
- [x] T020 [P] [US2] Run failing no-duplication checks in tests/contract/test_create_skills_prompt_assets.py for templates/commands/skills.md

### Implementation for User Story 2

- [x] T021 [US2] Replace detailed creation sections in templates/commands/skills.md with orchestration steps for parsing `$ARGUMENTS`, inferring target Skill, and validating target name
- [x] T022 [US2] Add explicit missing-target delegation instructions to templates/commands/skills.md that route creation to `create-skills`
- [x] T023 [US2] Add explicit existing-target delegation instructions to templates/commands/skills.md that route refinement to `improve-skills`
- [x] T024 [US2] Preserve handoff instructions in templates/commands/skills.md for running `/speckit.instructions` after Skill registry or discoverability changes
- [x] T025 [US2] Remove command-owned Skill authoring methodology from templates/commands/skills.md while keeping validation expectations and ambiguity handling

**Checkpoint**: User Story 2 keeps `/speckit.skills` as the predictable entrypoint without owning creation details.

---

## Phase 5: User Story 3 - Preserve existing skill quality expectations (Priority: P3)

**Goal**: Ensure the extracted Skill retains quality rules for metadata, progressive disclosure, resource organization, registry updates, validation, and completion reporting.

**Independent Test**: A reviewer can compare the extraction checklist against `skills/create-skills/SKILL.md` and confirm at least 90% of previous creation responsibilities remain represented.

### Tests for User Story 3

- [x] T026 [P] [US3] Add and run failing checks for progressive disclosure, resource directories, and relative resource paths in tests/contract/test_create_skills_prompt_assets.py
- [x] T027 [P] [US3] Add and run failing checks for registry update instructions and deterministic `skill_id` guidance in tests/contract/test_create_skills_prompt_assets.py
- [x] T028 [P] [US3] Add and run failing checks for quality anti-patterns in tests/contract/test_create_skills_prompt_assets.py

### Implementation for User Story 3

- [x] T029 [US3] Add Skill structure, `SKILL.md` frontmatter, body, and relative resource path guidance to skills/create-skills/SKILL.md
- [x] T030 [US3] Add progressive disclosure and size-control guidance to skills/create-skills/SKILL.md, including when to use skills/create-skills/references/
- [x] T031 [US3] Create skills/create-skills/references/skill-creation-quality-checklist.md with metadata, structure, registry, resource, and validation checks
- [x] T032 [US3] Link skills/create-skills/references/skill-creation-quality-checklist.md from skills/create-skills/SKILL.md using a relative path
- [x] T033 [US3] Add registry update instructions for .specify/instructions.md and `.specify/memory/features.md` discoverability constraints to skills/create-skills/SKILL.md
- [x] T034 [US3] Add quality anti-pattern guidance for vague descriptions, invalid names, oversized `SKILL.md`, missing executable steps, and inconsistent resource paths to skills/create-skills/SKILL.md
- [x] T035 [US3] Mirror skills/create-skills/references/skill-creation-quality-checklist.md to .specify/skills/create-skills/references/skill-creation-quality-checklist.md for current-workspace discovery
- [x] T036 [US3] Update .specify/instructions.md Skills registry with one deduplicated row for `create-skills` pointing to .specify/skills/create-skills/SKILL.md

**Checkpoint**: User Story 3 preserves existing creation quality expectations after extraction.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Validate regression coverage, feature tracking, and documentation consistency across all stories.

- [x] T037 [P] Update .specify/specs/008-create-skills-skill/checklists/create-skills-extraction.md with completed responsibility coverage results
- [x] T038 [P] Update .specify/memory/features/013.md with task-breakdown notes and the latest tasks.md related file entry
- [x] T039 [P] Verify .specify/memory/features.md keeps Feature 013 status `Implemented`, spec path .specify/specs/008-create-skills-skill/requirements.md, and last updated date 2026-05-10
- [x] T040 Run pytest tests/contract/test_create_skills_prompt_assets.py
- [ ] T041 Run pytest tests/contract/test_create_new_skill_contract.py tests/contracts/test_skill_install_layout_contract.py tests/integration/test_skill_install_layout_integration.py tests/integration/test_skills_resource_ids.py
- [x] T042 Execute quickstart validation scenarios from .specify/specs/008-create-skills-skill/quickstart.md against templates/commands/skills.md and skills/create-skills/SKILL.md
- [x] T043 [P] Confirm pyproject.toml still force-includes skills/ so skills/create-skills/SKILL.md is packaged
- [x] T044 Review git diff for templates/commands/skills.md, skills/create-skills/SKILL.md, .specify/skills/create-skills/SKILL.md, and tests/contract/test_create_skills_prompt_assets.py to ensure no unrelated changes

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; starts immediately.
- **Foundational (Phase 2)**: Depends on Setup; blocks all user story implementation.
- **User Story 1 (Phase 3)**: Depends on Foundational; delivers MVP dedicated creation Skill.
- **User Story 2 (Phase 4)**: Depends on Foundational; can run after or alongside US1 but final validation expects US1 content to exist.
- **User Story 3 (Phase 5)**: Depends on US1 because it enriches the extracted Skill; can run alongside late US2 tasks after the Skill file exists.
- **Polish (Phase 6)**: Depends on desired user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies on other stories after Foundational; MVP scope.
- **User Story 2 (P2)**: Depends only on Foundational, but references `create-skills` produced by US1 for full end-to-end validation.
- **User Story 3 (P3)**: Depends on US1 because it validates and extends the new Skill's quality rules.

### Within Each User Story

- Tests must be written and fail before implementation tasks.
- For US1, create frontmatter before moving detailed workflow content.
- For US2, routing text should be added before removing duplicated creation details.
- For US3, resource checklist should be created before linking and mirroring.

### Parallel Opportunities

- T002, T003, and T004 can run in parallel after T001.
- T006 through T009 can run in parallel because they add independent assertions to one new test module after T004 exists.
- US1 tests T011 and T012 can run in parallel.
- US2 tests T019 and T020 can run in parallel.
- US3 tests T026 through T028 can run in parallel.
- Polish documentation checks T037 through T039 can run in parallel.

---

## Parallel Example: User Story 1

```text
Task: "Run failing Skill existence/frontmatter checks in tests/contract/test_create_skills_prompt_assets.py for skills/create-skills/SKILL.md"
Task: "Add and run failing checks for explicit-input and conversation-history creation guidance in tests/contract/test_create_skills_prompt_assets.py"
```

## Parallel Example: User Story 2

```text
Task: "Run failing routing-language checks in tests/contract/test_create_skills_prompt_assets.py for templates/commands/skills.md"
Task: "Run failing no-duplication checks in tests/contract/test_create_skills_prompt_assets.py for templates/commands/skills.md"
```

## Parallel Example: User Story 3

```text
Task: "Add and run failing checks for progressive disclosure, resource directories, and relative resource paths in tests/contract/test_create_skills_prompt_assets.py"
Task: "Add and run failing checks for registry update instructions and deterministic `skill_id` guidance in tests/contract/test_create_skills_prompt_assets.py"
Task: "Add and run failing checks for quality anti-patterns in tests/contract/test_create_skills_prompt_assets.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational tests and extraction checklist.
3. Complete Phase 3: User Story 1.
4. Stop and validate `skills/create-skills/SKILL.md` independently against quickstart Scenario 3.
5. Demo the new Skill as the reusable creation capability.

### Incremental Delivery

1. Deliver Setup + Foundational tests.
2. Deliver US1 to make `create-skills` available.
3. Deliver US2 to reduce `templates/commands/skills.md` to orchestration.
4. Deliver US3 to preserve quality expectations and registry guidance.
5. Complete Polish validation and regression tests.

### Validation Commands

```text
pytest tests/contract/test_create_skills_prompt_assets.py
pytest tests/contract/test_create_new_skill_contract.py tests/contracts/test_skill_install_layout_contract.py tests/integration/test_skill_install_layout_integration.py tests/integration/test_skills_resource_ids.py
```
