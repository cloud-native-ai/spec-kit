# Tasks: Portable Skill Creation

**Requirement ID**: 013 (from branch name)
**Requirement Key**: 013-portable-skill-creation
**Related Feature**: 013 Skills Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/013-portable-skill-creation/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/

**Tests**: Contract tests are included per Constitution Principle IV (Test-First & Contract-Driven Implementation). Tests are written first and expected to fail before implementation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- [x] All tool-manifest references removed from skill creation pipeline
- [x] Contract tests pass (`pytest -m contract tests/contract/test_portable_skill_creation.py -v`)
- [x] Existing contract tests still pass (`pytest -m contract tests/contract/test_create_skills_prompt_assets.py -v`)
- [x] Mirror files are byte-identical to their canonical sources
- [x] `scripts/bash/create-new-skill.sh` no longer generates `tools/` directories
- [x] Existing skills with `tools/` directories retain their content unchanged
- [x] Changes validated against SC-001 through SC-005 from requirements.md

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Purpose**: Create test skeleton and establish the TDD baseline

- [x] T001 Create contract test file `tests/contract/test_portable_skill_creation.py` with test skeleton — define `ROOT`, file path constants, and helper functions for reading file content; all test functions should be empty stubs that `assert False` (ensures they fail before implementation)

**Checkpoint**: Test file exists, all stub tests fail when run

---

## Phase 2: Foundational (Contract Tests — Must Fail)

**Purpose**: Write all contract test assertions that will validate the implementation. These MUST fail before implementation begins.

**⚠️ CRITICAL**: All tests in this phase must FAIL initially. They define the target state.

- [x] T002 [P] Write test `test_create_skills_no_refresh_tools_ref` in `tests/contract/test_portable_skill_creation.py` — assert `skills/create-skills/SKILL.md` does not contain "refresh-tools.sh" (FR-001)
- [x] T003 [P] Write test `test_create_skills_no_tool_manifest_refs` in `tests/contract/test_portable_skill_creation.py` — assert `skills/create-skills/SKILL.md` does not contain "tools/system.json", "tools/shell.json", "tools/project.json" (FR-002)
- [x] T004 [P] Write test `test_create_skills_no_obtain_tools_step` in `tests/contract/test_portable_skill_creation.py` — assert `skills/create-skills/SKILL.md` does not contain "Obtain available tools information" heading (FR-002, SC-005)
- [x] T005 [P] Write test `test_skills_template_no_tools_subsection` in `tests/contract/test_portable_skill_creation.py` — assert `templates/skills-template.md` does not contain "### Tools" heading or "refresh-tools.sh" (FR-003)
- [x] T006 [P] Write test `test_skills_template_retains_resources` in `tests/contract/test_portable_skill_creation.py` — assert `templates/skills-template.md` still contains sections for scripts, references, and assets (FR-004)
- [x] T007 [P] Write test `test_orchestration_no_refresh_tools` in `tests/contract/test_portable_skill_creation.py` — assert `templates/commands/skills.md` does not contain "refresh-tools.sh" (FR-005)
- [x] T008 [P] Write test `test_script_no_refresh_tools_for_target` in `tests/contract/test_portable_skill_creation.py` — assert `scripts/bash/create-new-skill.sh` does not contain "refresh_tools_for_target" (FR-007)
- [x] T009 [P] Write test `test_create_skills_mirror_parity` in `tests/contract/test_portable_skill_creation.py` — assert `skills/create-skills/SKILL.md` is byte-identical to `.specify/skills/create-skills/SKILL.md` (FR-009)
- [x] T010 [P] Write test `test_checklist_no_tool_manifest_refs` in `tests/contract/test_portable_skill_creation.py` — assert `skills/create-skills/references/skill-creation-quality-checklist.md` does not contain "tool manifests" or "tools/system.json" (FR-011)
- [x] T011 Verify all T002–T010 tests FAIL by running `pytest -m contract tests/contract/test_portable_skill_creation.py -v` — confirm every test is red

**Checkpoint**: All 9 contract tests exist and fail. TDD baseline established.

---

## Phase 3: User Story 1 — Environment-Portable Skill Creation (Priority: P1) 🎯 MVP

**Goal**: Remove tool-discovery step and tool-manifest references from `create-skills/SKILL.md` so created skills are portable across environments.

**Independent Test**: After completion, `skills/create-skills/SKILL.md` contains zero references to `refresh-tools.sh`, `tools/system.json`, `tools/shell.json`, `tools/project.json`, or "Obtain available tools information". Contract tests T002–T004 pass.

### Implementation for User Story 1

- [x] T012 [US1] Remove Step 3 ("### 3. Obtain available tools information") entirely from `skills/create-skills/SKILL.md` — delete the heading and all content under it (lines 52–65 approximately: the heading, the `scripts/bash/refresh-tools.sh` code block, the tool manifest category list, and the "Filter available tools" instruction)
- [x] T013 [US1] Renumber remaining steps in `skills/create-skills/SKILL.md` — Step 4 → Step 3 ("Structure the Skill"), Step 5 → Step 4 ("Incrementally clarify details"), Step 6 → Step 5 ("Register the Skill"), Step 7 → Step 6 ("Validate the Skill"), Step 8 → Step 7 ("Report completion")
- [x] T014 [US1] Remove `tools/` from the Resource Directory Layout in `skills/create-skills/SKILL.md` — in the directory tree under "#### Resource Directory Layout" (around line 96), delete the `├── tools/              # Tool descriptions (optional)` line
- [x] T015 [US1] Remove tool-manifest references from the validation step in `skills/create-skills/SKILL.md` — in the "Progressive Disclosure" constraints section, remove any reference to `tools/` in the discovery/load steps
- [x] T016 [US1] Run contract tests T002–T004: `pytest tests/contract/test_portable_skill_creation.py::test_create_skills_no_refresh_tools_ref tests/contract/test_portable_skill_creation.py::test_create_skills_no_tool_manifest_refs tests/contract/test_portable_skill_creation.py::test_create_skills_no_obtain_tools_step -v` — all three must pass

**Checkpoint**: US1 contract tests pass. `create-skills/SKILL.md` has no tool-discovery logic.

---

## Phase 4: User Story 2 — Portable Skill Template (Priority: P1)

**Goal**: Remove tool boilerplate from `templates/skills-template.md` so scaffolded skills contain no environment-specific references.

**Independent Test**: `templates/skills-template.md` has no "### Tools" subsection, no tool-manifest refresh commands, but retains scripts/references/assets sections. Contract tests T005–T006 pass.

### Implementation for User Story 2

- [x] T017 [US2] Remove the "### Tools" subsection from `templates/skills-template.md` — delete the "### Tools (`${SKILL_HOME}/tools/`)" heading and all content under it (the tool manifest bullet and refresh commands)
- [x] T018 [US2] Rename the parent section heading from "## Available Tools & Resources" to "## Resources" in `templates/skills-template.md`
- [x] T019 [US2] Run contract tests T005–T006: `pytest tests/contract/test_portable_skill_creation.py::test_skills_template_no_tools_subsection tests/contract/test_portable_skill_creation.py::test_skills_template_retains_resources -v` — both must pass

**Checkpoint**: US2 contract tests pass. Template is tool-free but retains resource sections.

---

## Phase 5: User Story 3 — Simplified Orchestration Template (Priority: P2)

**Goal**: Remove tool-manifest requirements from the `/speckit.skills` orchestration template validation and modernization checklist.

**Independent Test**: `templates/commands/skills.md` does not contain "refresh-tools.sh" and has no mandatory tool-manifest modernization step. Contract test T007 passes.

### Implementation for User Story 3

- [x] T020 [US3] Remove `tools/` from the directory layout example in `templates/commands/skills.md` — in the "Canonical path & directory layout" section (Step 1 of the modernization checklist, around line 68), delete the `├── tools/           # auto-generated tool manifests` line
- [x] T021 [US3] Remove Step 6 ("Tool manifests") from the Spec-Compliance Modernization Checklist in `templates/commands/skills.md` — delete the entire "6. **Tool manifests**" item (around lines 102–103) including the `create-new-skill.sh --refresh-only` instruction
- [x] T022 [US3] Renumber Step 7 ("Hygiene") → Step 6 in the modernization checklist in `templates/commands/skills.md`
- [x] T023 [US3] Remove tool-manifest references from Step 4 validation in `templates/commands/skills.md` — in the "Validate and report" section (around line 122), remove "refresh tool manifests" from the follow-up actions example
- [x] T024 [US3] Run contract test T007: `pytest tests/contract/test_portable_skill_creation.py::test_orchestration_no_refresh_tools -v` — must pass

**Checkpoint**: US3 contract test passes. Orchestration template no longer mandates tool manifests.

---

## Phase 6: User Story 4 — Script Behavior Update (Priority: P3)

**Goal**: Remove `refresh_tools_for_target()` function and all its call sites from `scripts/bash/create-new-skill.sh`.

**Independent Test**: Script file does not contain "refresh_tools_for_target". Contract test T008 passes.

### Implementation for User Story 4

- [x] T025 [US4] Remove the `refresh_tools_for_target()` function definition from `scripts/bash/create-new-skill.sh` — delete lines 105–115 (the function body that creates `tools/` dir and runs `refresh-tools.sh` three times)
- [x] T026 [US4] Remove `refresh_tools_for_target "$target"` call in `--refresh-only` single-skill mode in `scripts/bash/create-new-skill.sh` — line 332
- [x] T027 [US4] Remove `refresh_tools_for_target "$skill_dir"` call in `--refresh-only` all-skills loop in `scripts/bash/create-new-skill.sh` — line 342
- [x] T028 [US4] Remove `refresh_tools_for_target "$TARGET_DIR"` call in existing-skill path in `scripts/bash/create-new-skill.sh` — line 379
- [x] T029 [US4] Remove `refresh_tools_for_target "$TARGET_DIR"` call in new-skill creation path in `scripts/bash/create-new-skill.sh` — line 415
- [x] T030 [US4] Update the JSON message on line 353 from "Skill tools refreshed" to "Skill metadata refreshed" in `scripts/bash/create-new-skill.sh`
- [x] T031 [US4] Run contract test T008: `pytest tests/contract/test_portable_skill_creation.py::test_script_no_refresh_tools_for_target -v` — must pass

**Checkpoint**: US4 contract test passes. Script no longer generates tool manifests.

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Quality checklist update, improve-skills update, mirror sync, existing test fix, and full validation.

- [x] T032 [P] Update `skills/create-skills/references/skill-creation-quality-checklist.md` — in the "Resource Organization" section, remove the mention of `tools/` and "generated tool manifests from project scripts" from the checklist item about acceptable resource directories (FR-011)
- [x] T033 [P] Update `skills/improve-skills/SKILL.md` Step 6 (validation) — remove the bullet about refreshing tool manifests with `create-new-skill.sh --refresh-only` or `refresh-tools.sh` (around line 70), and remove the paragraph about distinguishing generated manifests from instruction changes (around lines 71-72)
- [x] T034 Sync mirror: copy `skills/create-skills/SKILL.md` to `.specify/skills/create-skills/SKILL.md` (byte-identical copy)
- [x] T035 Sync mirror: copy `skills/create-skills/references/skill-creation-quality-checklist.md` to `.specify/skills/create-skills/references/skill-creation-quality-checklist.md` (byte-identical copy)
- [x] T036 Sync mirror: copy `skills/improve-skills/SKILL.md` to `.specify/skills/improve-skills/SKILL.md` (byte-identical copy)
- [x] T037 Update `tests/contract/test_create_skills_prompt_assets.py` — in `test_create_skills_uses_relative_resource_paths` (line 206), remove `"./tools/"` from the `rel_patterns` list so the test no longer expects a tools path reference
- [x] T038 Run mirror parity test T009: `pytest tests/contract/test_portable_skill_creation.py::test_create_skills_mirror_parity -v` — must pass
- [x] T039 Run checklist test T010: `pytest tests/contract/test_portable_skill_creation.py::test_checklist_no_tool_manifest_refs -v` — must pass
- [x] T040 Run full contract test suite: `pytest -m contract tests/contract/ -v` — all tests must pass (new and existing)
- [x] T041 Run full test suite: `pytest` — verify no regressions across all test categories

**Checkpoint**: All contract tests green. All existing tests still pass. Mirrors in sync.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — can start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 — BLOCKS all user stories
- **Phase 3 (US1)**: Depends on Phase 2. Can start immediately after foundational tests are written.
- **Phase 4 (US2)**: Depends on Phase 2. Independent of Phase 3 — can run in parallel.
- **Phase 5 (US3)**: Depends on Phase 2. Independent of Phases 3–4 — can run in parallel.
- **Phase 6 (US4)**: Depends on Phase 2. Independent of Phases 3–5 — can run in parallel.
- **Phase 7 (Polish)**: Depends on Phases 3–6 completion (mirrors need final content, full test suite needs all changes)

### User Story Dependencies

- **US1 (P1)**: Independent — edits `skills/create-skills/SKILL.md` only
- **US2 (P1)**: Independent — edits `templates/skills-template.md` only
- **US3 (P2)**: Independent — edits `templates/commands/skills.md` only
- **US4 (P3)**: Independent — edits `scripts/bash/create-new-skill.sh` only

All four user stories touch different files and have zero cross-dependencies. They can be implemented in any order or in parallel after Phase 2.

### Within Each User Story

- Implementation edits → then run the story's contract tests to confirm pass

### Parallel Opportunities

- T002–T010 (all foundational tests) can run in parallel — different test functions, same file
- US1, US2, US3, US4 can all run in parallel — different target files
- T032–T033 (quality checklist + improve-skills) can run in parallel — different files
- T034–T036 (mirror syncs) must run after their corresponding source files are edited

---

## Parallel Example: All User Stories

```bash
# After Phase 2 (foundational tests written), all stories can start in parallel:
# Stream 1: US1 — edit skills/create-skills/SKILL.md (T012–T016)
# Stream 2: US2 — edit templates/skills-template.md (T017–T019)
# Stream 3: US3 — edit templates/commands/skills.md (T020–T024)
# Stream 4: US4 — edit scripts/bash/create-new-skill.sh (T025–T031)
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1. Complete Phase 1: Setup (T001)
2. Complete Phase 2: Foundational tests (T002–T011)
3. Complete Phase 3: US1 — remove tool-discovery from create-skills workflow (T012–T016)
4. Complete Phase 4: US2 — remove tool boilerplate from template (T017–T019)
5. **STOP and VALIDATE**: New skills created via `create-skills` and scaffolded from template are tool-free

### Full Delivery

6. Complete Phase 5: US3 — orchestration template (T020–T024)
7. Complete Phase 6: US4 — script behavior (T025–T031)
8. Complete Phase 7: Polish — mirrors, checklist, full test suite (T032–T041)

### Sequential Single-Developer Path

T001 → T002–T011 → T012–T016 → T017–T019 → T020–T024 → T025–T031 → T032–T041

---

## Notes

- All user stories edit different files — zero merge conflicts possible
- [P] tasks = different files, no dependencies on incomplete tasks
- Mirror syncs (T034–T036) must wait until source files have their final content
- The `refresh-tools.sh` script itself is NOT modified — only its invocation from skill creation flows is removed
- Existing `tools/` directories in skills are unaffected (FR-010) — verified structurally because `create_skill_structure()` in `common.sh` never created `tools/`
