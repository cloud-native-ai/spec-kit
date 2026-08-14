# Tasks: AI Tools Support

**Input**: Design documents from `.specify/specs/011-ai-tools-support/`  
**Prerequisites**: `plan.md`, `requirements.md`, `research.md`, `data-model.md`, `contracts/ai-tools-support.openapi.yaml`, `quickstart.md`  
**Input Type Analysis**: `$ARGUMENTS` is empty; generated a complete executable task list from available design artifacts.  
**Tests**: Included because the plan requires test-first and contract-driven implementation, and the quickstart defines validation scenarios.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because the task touches different files or has no dependency on incomplete tasks.
- **[Story]**: Maps to the corresponding user story from `requirements.md`.
- Every task includes an exact file path.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish baseline fixtures and audit locations used by all stories.

- [X] T001 Inspect current assistant support behavior in `src/specify_cli/__init__.py` and record implementation notes in `.specify/specs/011-ai-tools-support/feature-ref.md`
- [X] T002 [P] Create reusable multi-assistant fixture builder in `tests/fixtures/ai_tools_support.py`
- [X] T003 [P] Add contract fixture loader for `ai-tools-support.openapi.yaml` in `tests/contract/test_ai_tools_support_contract.py`
- [X] T004 [P] Add temporary workspace comparison helpers in `tests/integration/test_ai_tools_core_preservation.py`
- [X] T005 [P] Add command inventory helper for canonical templates in `tests/integration/test_ai_tools_command_coverage.py`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core metadata, summary, preservation, and script-path infrastructure that all stories depend on.

**⚠️ CRITICAL**: No user story implementation can begin until this phase is complete.

- [X] T006 Add `AssistantSupportProfile` helper model or equivalent typed structure in `src/specify_cli/__init__.py`
- [X] T007 Add `InitializationResultSummary` helper model or equivalent typed structure in `src/specify_cli/__init__.py`
- [X] T008 Add `CoreWorkspaceAsset` preservation helper functions in `src/specify_cli/__init__.py`
- [X] T009 Add assistant command coverage helper functions in `src/specify_cli/__init__.py`
- [X] T010 Add summary rendering for created/reused/skipped/preserved/conflict/attention-required categories in `src/specify_cli/__init__.py`
- [X] T011 Align runtime workflow path variables with `.specify/specs/<requirements-key>/requirements.md` in `.specify/scripts/bash/common.sh`
- [X] T012 Mirror workflow path helper alignment in packaged scripts under `scripts/bash/common.sh`
- [X] T013 [P] Add unit tests for assistant profile uniqueness and official assistant list in `tests/unit/test_ai_tools_support_matrix.py`
- [X] T014 [P] Add unit tests for result summary categorization in `tests/unit/test_initialization_result_summary.py`
- [X] T015 [P] Add unit tests for core asset preservation decisions in `tests/unit/test_core_workspace_asset_preservation.py`
- [X] T016 [P] Add contract tests for OpenAPI path and schema completeness in `tests/contract/test_ai_tools_support_contract.py`
- [X] T017 [P] Add shell path regression tests for `.specify/specs` and `requirements.md` resolution in `tests/contract/test_specify_script_paths.py`

**Checkpoint**: Foundation ready - assistant metadata, preservation decisions, summaries, and script paths are testable.

---

## Phase 3: User Story 1 - 初始化任一受支持 AI 工具 (Priority: P1) 🎯 MVP

**Goal**: Every officially supported AI tool can initialize a new project with full Spec Kit workflow coverage.

**Independent Test**: Initialize a fresh workspace for each official assistant and verify `.specify` core assets plus assistant-specific command/guidance assets exist and are summarized.

### Tests for User Story 1

**NOTE: Write these tests FIRST, ensure they FAIL before implementation.**

- [X] T018 [P] [US1] Add integration test for new-project initialization across `copilot`, `claude`, `qwen`, `opencode`, and `qoder` in `tests/integration/test_ai_tools_init_all_assistants.py`
- [X] T019 [P] [US1] Add command coverage test comparing generated assistant commands with `templates/commands/*.md` in `tests/integration/test_ai_tools_command_coverage.py`
- [X] T020 [P] [US1] Add package resource test for all assistant command and template assets in `tests/integration/test_ai_tools_distribution.py`
- [X] T021 [P] [US1] Add unit test for CLI help assistant list consistency in `tests/unit/test_ai_tools_cli_help.py`
- [X] T022 [P] [US1] Add quickstart scenario test for new-project initialization in `tests/integration/test_ai_tools_quickstart.py`

### Implementation for User Story 1

- [X] T023 [US1] Refactor `AGENT_CONFIG` into complete official assistant profiles in `src/specify_cli/__init__.py`
- [X] T024 [US1] Add assistant-to-command-surface mapping for Copilot, Claude Code, Qwen Code, opencode, and Qoder in `src/specify_cli/__init__.py`
- [X] T025 [US1] Update `generate_commands()` handling to report generated command assets per assistant in `src/specify_cli/__init__.py`
- [X] T026 [US1] Update `copy_local_templates()` to generate complete command assets for every official assistant in `src/specify_cli/__init__.py`
- [X] T027 [US1] Add missing skill compatibility link handling for Qwen Code and opencode in `src/specify_cli/__init__.py`
- [X] T028 [US1] Update assistant selection and `--ai` help text to derive supported assistants from the support profile in `src/specify_cli/__init__.py`
- [X] T029 [US1] Ensure packaged templates include canonical assistant command sources in `pyproject.toml`
- [X] T030 [US1] Run the User Story 1 validation scenario described in `.specify/specs/011-ai-tools-support/quickstart.md`

**Checkpoint**: User Story 1 is independently functional as the MVP.

---

## Phase 4: User Story 2 - 在已有 Spec Kit 项目中追加工具支持 (Priority: P2)

**Goal**: Adding a new assistant to an existing Spec Kit workspace reuses initialized `.specify` core files instead of overwriting user-maintained content.

**Independent Test**: Start from an existing workspace with modified core files, add a second assistant, and verify core content is unchanged while new assistant assets are available.

### Tests for User Story 2

**NOTE: Write these tests FIRST, ensure they FAIL before implementation.**

- [X] T031 [P] [US2] Add integration test preserving modified `.specify/memory/features.md` during assistant addition in `tests/integration/test_ai_tools_core_preservation.py`
- [X] T032 [P] [US2] Add integration test preserving modified `.specify/instructions.md` during assistant refresh in `tests/integration/test_ai_tools_instruction_preservation.py`
- [X] T033 [P] [US2] Add integration test for partial `.specify` repair with missing core files in `tests/integration/test_ai_tools_partial_core_repair.py`
- [X] T034 [P] [US2] Add integration test for customized assistant-specific command conflict reporting in `tests/integration/test_ai_tools_custom_asset_conflicts.py`
- [X] T035 [P] [US2] Add repeat-run idempotence test for adding the same assistant twice in `tests/integration/test_ai_tools_repeat_run_idempotence.py`

### Implementation for User Story 2

- [X] T036 [US2] Replace unconditional core template copying with create-if-missing preservation logic in `src/specify_cli/__init__.py`
- [X] T037 [US2] Add initialized core file detection for `.specify/memory`, `.specify/templates`, `.specify/scripts`, `.specify/skills`, and `.specify/instructions.md` in `src/specify_cli/__init__.py`
- [X] T038 [US2] Add partial core repair logic that copies only missing required core assets in `src/specify_cli/__init__.py`
- [X] T039 [US2] Add customized assistant-specific asset preservation and conflict reporting in `src/specify_cli/__init__.py`
- [X] T040 [US2] Add existing-workspace result summary output for reused and preserved assets in `src/specify_cli/__init__.py`
- [X] T041 [US2] Update `--force` behavior documentation to distinguish explicit overwrite from default preservation in `src/specify_cli/__init__.py`
- [X] T042 [US2] Run the User Story 2 validation scenario described in `.specify/specs/011-ai-tools-support/quickstart.md`

**Checkpoint**: User Story 2 is independently functional and preserves existing Spec Kit core files.

---

## Phase 5: User Story 3 - 多工具共存和一致性验证 (Priority: P3)

**Goal**: Multiple AI tools can coexist in one project and users can validate configured status, command coverage, and support-surface consistency.

**Independent Test**: Configure at least three assistants in one workspace, refresh one assistant, and verify other assistant roots plus canonical core assets remain intact while audits show coverage status.

### Tests for User Story 3

**NOTE: Write these tests FIRST, ensure they FAIL before implementation.**

- [X] T043 [P] [US3] Add integration test for three-assistant coexistence in `tests/integration/test_ai_tools_multi_assistant_coexistence.py`
- [X] T044 [P] [US3] Add integration test ensuring refreshing one assistant leaves other assistant roots untouched in `tests/integration/test_ai_tools_refresh_isolation.py`
- [X] T045 [P] [US3] Add support-surface audit test for README, docs, templates, CLI help, and package resources in `tests/contract/test_ai_tools_support_surfaces.py`
- [X] T046 [P] [US3] Add local tool availability vs project configuration test in `tests/integration/test_ai_tools_validation_summary.py`
- [X] T047 [P] [US3] Add quickstart audit scenario test in `tests/integration/test_ai_tools_quickstart.py`

### Implementation for User Story 3

- [X] T048 [US3] Add multi-assistant configured-status detection and display in `src/specify_cli/__init__.py`
- [X] T049 [US3] Add refresh isolation guards so one assistant refresh cannot remove other assistant roots in `src/specify_cli/__init__.py`
- [X] T050 [US3] Add support-surface audit helper for official assistant consistency in `src/specify_cli/__init__.py`
- [X] T051 [US3] Add generated command coverage audit output for each official assistant in `src/specify_cli/__init__.py`
- [X] T052 [US3] Update supported assistant references in `README.md`
- [X] T053 [US3] Update initialization and maintenance guidance in `docs/installation.md`, `docs/quickstart.md`, and `docs/usage.md`
- [X] T054 [US3] Update assistant support references in `.specify/templates/instructions-template.md` and `templates/instructions-template.md`
- [X] T055 [US3] Run the User Story 3 validation scenario described in `.specify/specs/011-ai-tools-support/quickstart.md`

**Checkpoint**: All user stories are independently functional and multi-tool coexistence is auditable.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final consistency, quality, and feature tracking work across all user stories.

- [X] T056 [P] Update release and support-surface notes in `.specify/specs/011-ai-tools-support/feature-ref.md`
- [X] T057 [P] Update Feature 022 implementation notes and related files in `.specify/memory/features/022.md`
- [X] T058 [P] Ensure Feature 022 status and latest date remain synchronized in `.specify/memory/features.md`
- [X] T059 Run focused pytest suites for AI tools support in `tests/contract/test_ai_tools_support_contract.py`, `tests/unit/test_ai_tools_support_matrix.py`, and `tests/integration/test_ai_tools_init_all_assistants.py`
- [X] T060 Run preservation and coexistence pytest suites in `tests/integration/test_ai_tools_core_preservation.py`, `tests/integration/test_ai_tools_multi_assistant_coexistence.py`, and `tests/integration/test_ai_tools_refresh_isolation.py`
- [X] T061 Run script-path regression tests in `tests/contract/test_specify_script_paths.py`
- [X] T062 Run full repository test suite using `pyproject.toml` project configuration
- [X] T063 Review `.specify/specs/011-ai-tools-support/requirements.md`, `.specify/specs/011-ai-tools-support/plan.md`, and `.specify/specs/011-ai-tools-support/tasks.md` for cross-artifact consistency
- [X] T064 Confirm no generated assistant asset duplicates canonical `.specify` workflow content in `.specify/specs/011-ai-tools-support/quickstart.md`
- [X] T065 [P] Update task template constitution references so test-first/TDD guidance points to Constitution Principle IV and verify mirrored task templates remain consistent in `templates/tasks-template.md` and `.specify/templates/tasks-template.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies; can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion; blocks all user stories.
- **User Story 1 (Phase 3)**: Depends on Foundational completion; MVP scope.
- **User Story 2 (Phase 4)**: Depends on Foundational completion; can proceed after or alongside US1, but validates best after baseline assistant generation exists.
- **User Story 3 (Phase 5)**: Depends on Foundational completion; benefits from US1 and US2 but remains independently testable with fixture workspaces.
- **Polish (Phase 6)**: Depends on selected user stories being complete.

### User Story Dependencies

- **US1 (P1)**: No dependency on other user stories after Foundational; delivers MVP initialization parity.
- **US2 (P2)**: No hard dependency on US1 implementation, but shares preservation helpers and validates existing-workspace safety.
- **US3 (P3)**: Uses support profile, preservation, and command coverage helpers; should run after enough assistant asset generation exists for meaningful audits.

### Within Each User Story

- Tests must be written first and must fail before implementation.
- Contract and integration tests precede implementation tasks.
- Metadata/profile work precedes asset generation work.
- Preservation logic precedes summary and conflict reporting.
- Audit helpers precede documentation and support-surface updates.

---

## Parallel Opportunities

- T002, T003, T004, and T005 can run in parallel after T001 starts.
- T013, T014, T015, T016, and T017 can run in parallel after T006 through T012 interfaces are sketched.
- T018 through T022 can run in parallel for US1 test creation.
- T031 through T035 can run in parallel for US2 test creation.
- T043 through T047 can run in parallel for US3 test creation.
- Documentation updates T052 through T054 can run in parallel after audit expectations are defined.
- Polish tasks T056 through T058 and T065 can run in parallel before final test execution.

## Parallel Example: User Story 1

```bash
# Launch US1 test creation in parallel:
Task: "T018 [US1] Add integration test for new-project initialization across all assistants in tests/integration/test_ai_tools_init_all_assistants.py"
Task: "T019 [US1] Add command coverage test in tests/integration/test_ai_tools_command_coverage.py"
Task: "T020 [US1] Add package resource test in tests/integration/test_ai_tools_distribution.py"
Task: "T021 [US1] Add unit test for CLI help assistant list consistency in tests/unit/test_ai_tools_cli_help.py"
```

## Parallel Example: User Story 2

```bash
# Launch US2 preservation tests in parallel:
Task: "T031 [US2] Add core preservation test in tests/integration/test_ai_tools_core_preservation.py"
Task: "T032 [US2] Add instruction preservation test in tests/integration/test_ai_tools_instruction_preservation.py"
Task: "T033 [US2] Add partial core repair test in tests/integration/test_ai_tools_partial_core_repair.py"
Task: "T034 [US2] Add custom asset conflict test in tests/integration/test_ai_tools_custom_asset_conflicts.py"
```

## Parallel Example: User Story 3

```bash
# Launch US3 coexistence and audit tests in parallel:
Task: "T043 [US3] Add three-assistant coexistence test in tests/integration/test_ai_tools_multi_assistant_coexistence.py"
Task: "T044 [US3] Add refresh isolation test in tests/integration/test_ai_tools_refresh_isolation.py"
Task: "T045 [US3] Add support-surface audit test in tests/contract/test_ai_tools_support_surfaces.py"
Task: "T046 [US3] Add validation summary test in tests/integration/test_ai_tools_validation_summary.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational.
3. Complete Phase 3: User Story 1.
4. Stop and validate that every official assistant can initialize a new project with command coverage.
5. Demo MVP using the quickstart Scenario 1.

### Incremental Delivery

1. Deliver Setup + Foundational infrastructure.
2. Deliver US1 to establish new-project support parity.
3. Deliver US2 to protect existing projects when adding tools.
4. Deliver US3 to validate multi-tool coexistence and release-wide support claims.
5. Complete Polish to synchronize feature memory, docs, and full validation.

### Parallel Team Strategy

1. One developer prepares assistant profile and summary interfaces.
2. One developer writes contract/unit tests for support matrix and coverage.
3. One developer writes integration tests for preservation and coexistence fixtures.
4. After Foundational completion, split US1, US2, and US3 implementation by story while coordinating shared changes in `src/specify_cli/__init__.py`.

## Notes

- `[P]` tasks touch different files or are safe to parallelize after prerequisite interfaces are known.
- Every story is independently testable with fixture workspaces.
- Commit after each phase or independently validated story.
- Avoid overwriting `.specify` core files during implementation experiments.
- If generated artifacts need design updates, re-run `/speckit.plan` before regenerating tasks.
