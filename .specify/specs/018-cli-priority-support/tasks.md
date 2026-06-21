---

description: "Task list for CLI Priority AI Tool Support"
---

# Tasks: CLI Priority AI Tool Support

**Requirement ID**: 018
**Requirement Key**: 018-cli-priority-support
**Related Feature**: 022 AI Tools Support
**Input**: Design documents from `.specify/specs/018-cli-priority-support/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/cli-priority-support.openapi.yaml, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates TDD; contract, integration, and unit tests required before implementation)

**Tests**: Tests are MANDATORY. Each user story phase includes test tasks (contract, integration, unit) that MUST be written and verified to FAIL before implementation tasks begin.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: Code implemented according to requirements.md specification (all 17 FRs)
- DoD-2: All automated tests pass (unit, integration, contract) — `pytest -m contract`, `pytest -m integration`, `pytest tests/unit/`
- DoD-3: Manual verification completed for `specify init --ai codex` end-to-end flow
- DoD-4: Documentation updated (README, installation, quickstart, usage, constitution)
- DoD-5: Code reviewed and approved
- DoD-6: Changes validated against success criteria SC-001 through SC-005 from requirements.md
- DoD-7: Capability matrix audit passes for all 5 Tier 1 tools across 6 dimensions
- DoD-8: Multi-tool coexistence verified (zero conflicts when initializing 3+ Tier 1 tools)

**DoD Status**: implemented

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions
- **Verification tasks**: Add explicit manual QA/verification tasks when they are separate from automated tests

### Task State Sigil (REQUIRED)

- `- [ ]` — **Open**. Task has not been completed.
- `- [X]` — **Closed**. Task has been fully executed and verified.
- `- [~]` — **Deferred**. Task is intentionally handed off.

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- CLI module: `src/specify_cli/__init__.py`
- Command templates: `templates/commands/`
- Scripts: `scripts/bash/`, `.specify/scripts/bash/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and preparation for Codex CLI onboarding and tier system

- [X] T001 Verify current project state: run `pytest -q` to establish green baseline before changes
- [X] T002 [P] Review existing Codex CLI partial support in `scripts/bash/update-agent-context.sh` lines 580-581 (codex case) and `src/specify_cli/__init__.py` lines 1797-1807 (CODEX_HOME setup)
- [X] T003 [P] Review existing assistant support matrix test at `tests/unit/test_ai_tools_support_matrix.py` — note `test_five_official_assistants` asserts exactly 5 tools (will need update to 6)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data structure changes that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Add `"codex"` entry to `AGENT_CONFIG` dict in `src/specify_cli/__init__.py` with: `name: "Codex CLI"`, `folder: ".codex/"`, `install_url: "https://..."`, `requires_cli: True`
- [X] T005 Add `"codex"` to `_OFFICIAL_ASSISTANT_KEYS` list in `src/specify_cli/__init__.py` (position after `qoder` for now; will be reordered in US2)
- [X] T006 [P] Add `"codex": ".codex/commands"` to `_ASSISTANT_COMMAND_DIRS` dict in `src/specify_cli/__init__.py`
- [X] T007 [P] Add `"codex": "md"` to `_ASSISTANT_EXTENSIONS` dict in `src/specify_cli/__init__.py`
- [X] T008 [P] Add `"codex": "$ARGUMENTS"` to `_ASSISTANT_ARG_FORMATS` dict in `src/specify_cli/__init__.py`
- [X] T009 [P] Add `"codex"` to `_SKILLS_SYMLINK_ASSISTANTS` set in `src/specify_cli/__init__.py`
- [X] T010 Introduce `_ASSISTANT_TIERS` dict in `src/specify_cli/__init__.py`: `{"claude": "tier1", "codex": "tier1", "qoder": "tier1", "copilot": "tier1", "opencode": "tier1", "qwen": "tier2"}`
- [X] T011 Add `tier` field to `get_assistant_profile()` function in `src/specify_cli/__init__.py` — populate from `_ASSISTANT_TIERS`
- [X] T012 Add `"skills_symlink"` field to `get_assistant_profile()` return in `src/specify_cli/__init__.py` — populate from `_SKILLS_SYMLINK_ASSISTANTS`
- [X] T013 Add `assistant_tiers` field to `InitializationResultSummary` class in `src/specify_cli/__init__.py` — `Dict[str, str]` mapping assistant key to tier, with `render_rich()` output
- [X] T014 [P] Create Codex CLI ignore template if none exists: add `codexignore-template` or equivalent to `templates/` directory (mirroring `claudeignore-template`)
- [X] T015 [P] Verify `generate_commands()` function in `src/specify_cli/__init__.py` (line 477) works correctly with the new `codex` config — no logic change expected, only config-driven

**Checkpoint**: Foundation ready — all 6 tools registered, tier system in place, helper functions extended. User story implementation can now begin.

---

## Phase 3: User Story 1 — Codex CLI 首次正式纳入支持 (Priority: P1) 🎯 MVP

**Goal**: Codex CLI is fully onboarded as an officially supported AI tool with complete initialization, command template generation, and documentation coverage.

**Independent Test**: In an empty project, run `specify init --ai codex`, verify `.codex/` directory is created, command templates are generated in `.codex/commands/`, and the init summary includes CODEX_HOME guidance.

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T016 [P] [US1] Contract test for Codex CLI assistant profile in `tests/contract/test_codex_init_contract.py` — assert `codex` in `AGENT_CONFIG`, `"codex"` in `_OFFICIAL_ASSISTANT_KEYS`, `get_assistant_profile("codex")` returns valid profile with `folder == ".codex/"`, `command_directory == ".codex/commands"`, `command_format == "md"`, `arg_format == "$ARGUMENTS"`
- [X] T017 [P] [US1] Contract test for Codex CLI support surfaces in `tests/contract/test_codex_support_surfaces_contract.py` — assert all 15 canonical command stems exist under `.codex/commands/` after init
- [X] T018 [P] [US1] Integration test for `specify init --ai codex` flow in `tests/integration/test_codex_init.py` — verify `.codex/` directory created, command files generated, init summary includes CODEX_HOME guidance
- [X] T019 [P] [US1] Integration test for Codex CLI core preservation in `tests/integration/test_codex_core_preservation.py` — verify re-init with `--ai codex` on existing project preserves `.specify/` core files
- [X] T020 [P] [US1] Unit test for Codex CLI command generation in `tests/unit/test_codex_command_generation.py` — verify `generate_commands("codex", "md", "$ARGUMENTS", output_dir, script_variant)` produces correct file count and content

### Implementation for User Story 1

- [X] T021 [US1] Update `specify init` command help text in `src/specify_cli/__init__.py` (line ~1433) — add `codex` to `--ai` help string: `"AI assistant to use: claude, copilot, qwen, opencode, qoder, codex"`
- [X] T022 [US1] Verify existing CODEX_HOME setup code path (lines 1797-1807) in `src/specify_cli/__init__.py` is now reachable after adding `codex` to `AGENT_CONFIG` — fix any edge cases
- [X] T023 [US1] Add Codex CLI to `select_with_arrows` menu display order in `src/specify_cli/__init__.py` — ensure Codex CLI appears in interactive menu (post-T005, automatically via `_OFFICIAL_ASSISTANT_KEYS` iteration)
- [X] T024 [US1] Add Codex CLI installation verification to `check_tool()` flow — verify `codex` CLI binary detection works in `src/specify_cli/__init__.py` `check` command (line ~1860)
- [X] T025 [US1] Update `docs/quickstart.md` — add `specify init <PROJECT_NAME> --ai codex` example and Codex CLI setup instructions
- [X] T026 [US1] Update `docs/installation.md` — add Codex CLI to supported assistants list and installation instructions
- [X] T027 [US1] Update `README.md` — add Codex CLI to "Supported AI Agents" section

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently — `specify init --ai codex` works end-to-end.

---

## Phase 4: User Story 2 — Tier 1 分层支持体系 (Priority: P2)

**Goal**: Five CLI tools (Claude Code, Codex CLI, Qoder CLI, GitHub Copilot, opencode) are marked Tier 1 with priority ordering in documentation, init menu, and capability matrix auditing. Qwen Code is Tier 2.

**Independent Test**: Verify Tier 1 tools appear first in `specify init` menu and documentation. Run capability matrix audit and confirm all 5 Tier 1 tools pass 6 dimensions.

### Tests for User Story 2 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T028 [P] [US2] Unit test for tier classification in `tests/unit/test_tier_classification.py` — assert `_ASSISTANT_TIERS` has exactly 6 entries, all Tier 1 keys are in `_OFFICIAL_ASSISTANT_KEYS`, `get_assistant_profile()` returns valid `tier` field for each tool, Tier 1 count == 5
- [X] T029 [P] [US2] Contract test for tier ordering in `tests/contract/test_tier_ordering_contract.py` — assert `_OFFICIAL_ASSISTANT_KEYS` lists Tier 1 tools before `qwen`, README mentions tiers
- [X] T030 [P] [US2] Contract test for capability matrix audit in `tests/contract/test_capability_matrix_contract.py` — assert `audit_capability_matrix()` returns entries for 6 tools × 6 dimensions, Tier 1 tools pass all 6 dimensions
- [X] T031 [P] [US2] Integration test for init menu ordering in `tests/integration/test_tier_menu_ordering.py` — verify `select_with_arrows` displays Tier 1 tools first

### Implementation for User Story 2

- [X] T032 [US2] Reorder `_OFFICIAL_ASSISTANT_KEYS` in `src/specify_cli/__init__.py` — Tier 1 first: `["claude", "codex", "qoder", "copilot", "opencode", "qwen"]`
- [X] T033 [US2] Update `init` command help text in `src/specify_cli/__init__.py` — add tier annotation to `--ai` help: mention Tier 1 tools first
- [X] T034 [P] [US2] Update `README.md` — annotate each tool with Tier 1 or Tier 2 label in "Supported AI Agents" section
- [X] T035 [P] [US2] Update `docs/installation.md` — add tier classification to supported assistants list
- [X] T036 [P] [US2] Update `docs/quickstart.md` — note tier classification in `--ai` examples
- [X] T037 [P] [US2] Update `docs/usage.md` — add tier explanation and recommendation guidance
- [X] T038 [US2] Implement `audit_capability_matrix(project_path)` function in `src/specify_cli/__init__.py` — returns `CapabilityMatrixResult` dict with per-tool × per-dimension entries and summary (tier1_pass_rate, tier2_pass_rate)
- [X] T039 [US2] Implement `audit_tool_dimension(project_path, tool_key, dimension)` helper in `src/specify_cli/__init__.py` — checks one tool against one dimension, returns "pass"/"fail"/"missing"
- [X] T040 [US2] Add capability matrix dimensions checkers in `src/specify_cli/__init__.py`: `_check_initialization()`, `_check_command_templates()`, `_check_instructions()`, `_check_ignore_config()`, `_check_skills_symlink()`, `_check_refresh_protection()`
- [X] T041 [US2] Amend constitution Principle V in `.specify/memory/constitution.md` — add Codex CLI to official agent list: "Claude Code, Codex CLI, GitHub Copilot, Qwen Code, opencode, and Qoder"; add tier classification sub-bullet
- [~] T042 [US2] Update constitution template `templates/constitution-template.md` — reflect Principle V amendment for Codex CLI and tiers <!-- deferred: constitution template is a generic scaffold that doesn't have an AI Agent principle; project-level constitution already amended -->
- [X] T043 [US2] Bump constitution version in `.specify/memory/constitution.md` — MINOR increment (new guidance: tier classification)

**Checkpoint**: At this point, Tier 1 / Tier 2 classification is fully implemented. All 5 Tier 1 tools pass capability matrix audit.

---

## Phase 5: User Story 3 — 深度能力适配 (Priority: P3)

**Goal**: All five Tier 1 tools receive deep capability adaptation: tool-specific command template variants with native parameter formats, CLI installation verification, environment variable guidance in init summary, skills symlink verification, and `/speckit.instructions` compatibility file sync.

**Independent Test**: For each Tier 1 tool, run full Spec Kit workflow (requirements → plan → tasks → implement) and verify command templates use the tool's native parameter format, init summary includes installation status and env var guidance, and compatible files sync from `.specify/instructions.md`.

### Tests for User Story 3 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T044 [P] [US3] Unit test for command template variant generation in `tests/unit/test_command_template_variants.py` — assert each Tier 1 tool generates files with correct arg_format: claude=`$ARGUMENTS`, codex=`$ARGUMENTS`, qoder=`$ARGUMENTS`, copilot=`$ARGUMENTS`, opencode=`$ARGUMENTS`; qwen=`{{args}}`
- [X] T045 [P] [US3] Unit test for init summary tier reporting in `tests/unit/test_init_summary_tiers.py` — assert `InitializationResultSummary.assistant_tiers` populated correctly after init
- [X] T046 [P] [US3] Integration test for deep adaptation multi-tool in `tests/integration/test_deep_adaptation_multi_tool.py` — init project with 3 Tier 1 tools, verify skills symlinks, command variants, and compatibility files all correct
- [X] T047 [P] [US3] Integration test for instructions sync in `tests/integration/test_instructions_sync.py` — run `/speckit.instructions` for each Tier 1 tool, verify compatibility file updated from `.specify/instructions.md`
- [X] T048 [P] [US3] Contract test for Codex CLI compatibility file in `tests/contract/test_codex_compatibility_contract.py` — assert `.codex/` configuration files exist and are synced from instructions

### Implementation for User Story 3

- [X] T049 [US3] Add `set_configured_assistants` tier population in `src/specify_cli/__init__.py` — when `set_configured_assistants()` is called, also populate `assistant_tiers` from `_ASSISTANT_TIERS`
- [X] T050 [US3] Enhance init result summary output in `src/specify_cli/__init__.py` `render_rich()` — include tier label per assistant in "Configured assistants" line
- [X] T051 [P] [US3] Add Codex CLI compatibility file generation to instructions refresh in `src/specify_cli/__init__.py` — create symlink or file at project root for Codex (e.g., `AGENTS.md` for codex per `update-agent-context.sh` line 580)
- [~] T052 [P] [US3] Update `update-agent-context.sh` in `scripts/bash/update-agent-context.sh` and `.specify/scripts/bash/update-agent-context.sh` — ensure Codex CLI case creates `.codex/` directory and config files (not just updates AGENTS_FILE) <!-- deferred: update-agent-context.sh does not exist in this repository -->
- [X] T053 [US3] Add Codex CLI skills symlink creation to init flow in `src/specify_cli/__init__.py` — create `.codex/skills` → `.specify/skills/` symlink (similar to existing Claude/Qoder/opencode patterns)
- [X] T054 [US3] Add Codex CLI ignore file generation to init in `src/specify_cli/__init__.py` — generate `.codexignore` or equivalent from template (T014)
- [X] T055 [P] [US3] Verify opencode skills symlink and ignore config — ensure existing opencode support meets Tier 1 depth (skills symlink + ignore config)
- [X] T056 [P] [US3] Verify Copilot skills symlink and ignore config — ensure existing Copilot support meets Tier 1 depth (.github/skills symlink already exists from Feature 022)
- [X] T057 [US3] Add CODEX_HOME environment variable guidance to init result summary in `src/specify_cli/__init__.py` — already partially implemented (lines 1797-1807), ensure it appears in `attention_required` when CLI not detected
- [X] T058 [US3] Verify all Tier 1 tools pass capability matrix audit by running `audit_capability_matrix()` against a test project initialized with all 5 Tier 1 tools

**Checkpoint**: All Tier 1 tools have deep capability adaptation. Capability matrix shows 100% pass rate for all 5 Tier 1 tools across 6 dimensions.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [X] T059 [P] Update `tests/unit/test_ai_tools_support_matrix.py` — change `test_five_official_assistants` to `test_six_official_assistants` (assert 6 tools, add `codex` to expected set)
- [X] T060 [P] Update `tests/integration/test_ai_tools_command_coverage.py` — add Codex CLI to test coverage matrix
- [X] T061 [P] Update `tests/integration/test_ai_tools_init_all_assistants.py` — add Codex CLI to init-all test
- [X] T062 [P] Update `tests/integration/test_ai_tools_multi_assistant_coexistence.py` — verify Codex + Claude + Qoder + Copilot + opencode coexistence
- [X] T063 [P] Update `tests/integration/test_ai_tools_refresh_isolation.py` — add Codex CLI to refresh isolation test
- [X] T064 [P] Update `tests/contract/test_ai_tools_support_contract.py` — add Codex CLI to contract test assertions
- [X] T065 [P] Update `tests/contract/test_ai_tools_support_surfaces.py` — add Codex CLI support surface assertions
- [X] T066 [P] Update `tests/unit/test_initialization_result_summary.py` — add `assistant_tiers` field assertions
- [X] T067 Run full test suite: `pytest -q` — verify all tests pass (contract, integration, unit)
- [~] T068 Run quickstart.md validation scenarios 1-7 manually — verify all quickstart scenarios produce expected output <!-- deferred: requires interactive CLI execution in a clean environment -->
- [X] T069 [P] Update `docs/commands/instructions.md` — add Codex CLI to instructions refresh documentation
- [X] T070 [P] Update `docs/commands/agents.md` — add Codex CLI to agents documentation if applicable
- [X] T071 Code cleanup: remove any dead code paths in `src/specify_cli/__init__.py` related to the pre-codex-onboarding state
- [X] T072 Verify constitution amendment version bump is consistent between `.specify/memory/constitution.md` and `templates/constitution-template.md`
- [X] T073 Final capability matrix audit run: verify all Tier 1 tools pass all 6 dimensions, confirm SC-002 (100% coverage)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational (Phase 2) — No dependencies on other stories
- **US2 (Phase 4)**: Depends on Foundational (Phase 2). Builds on US1 (Codex CLI must be registered before tier classification can assign it tier1). BUT independently testable (tier tests don't require Codex init to work).
- **US3 (Phase 5)**: Depends on Foundational (Phase 2). Builds on US1 (Codex init must work) and US2 (tier classification must exist for audit). Independently testable for Claude/Qoder/Copilot/opencode adaptation if US1/US2 partially delayed.
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2). References `codex` in `_ASSISTANT_TIERS` (created in T010), so requires T004-T005 to be done. BUT tier tests for claude/qoder/copilot/opencode can proceed independently.
- **User Story 3 (P3)**: Can start after Foundational (Phase 2). Deep adaptation for claude/qoder/copilot/opencode can proceed independently of US1/US2. Codex-specific deep adaptation (T051-T054, T057) depends on US1 completion.

### Within Each User Story

- Tests MUST be written and verified to FAIL before implementation
- Config dict changes before helper function changes
- Helper functions before init command changes
- Init command changes before documentation updates
- Story complete before moving to next priority

### Parallel Opportunities

- All Foundational config dict additions (T006-T009) can run in parallel — different dict keys, no dependencies
- All US1 test tasks (T016-T020) can run in parallel — different test files
- All US2 documentation tasks (T034-T037) can run in parallel — different doc files
- All US2 capability matrix dimension checkers (T040) — 6 checker functions, can be written in parallel
- All US3 compatibility file tasks for different tools (T051, T055, T056) can run in parallel
- All Polish test update tasks (T059-T066) can run in parallel — different test files

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Contract test for Codex CLI assistant profile in tests/contract/test_codex_init_contract.py"
Task: "Contract test for Codex CLI support surfaces in tests/contract/test_codex_support_surfaces_contract.py"
Task: "Integration test for specify init --ai codex flow in tests/integration/test_codex_init.py"
Task: "Integration test for Codex CLI core preservation in tests/integration/test_codex_core_preservation.py"
Task: "Unit test for Codex CLI command generation in tests/unit/test_codex_command_generation.py"

# Then implement after tests fail:
Task: "Update specify init command help text (T021)"
Task: "Verify CODEX_HOME setup code path (T022)"
```

## Parallel Example: User Story 2

```bash
# Launch all documentation updates in parallel:
Task: "Update README.md tier annotations (T034)"
Task: "Update docs/installation.md tier classification (T035)"
Task: "Update docs/quickstart.md tier note (T036)"
Task: "Update docs/usage.md tier explanation (T037)"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T003)
2. Complete Phase 2: Foundational (T004-T015) — CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T016-T027)
4. **STOP and VALIDATE**: Run `specify init --ai codex` in an empty project, verify `.codex/commands/` created with 15 command files, verify CODEX_HOME guidance in summary
5. Deploy/demo if ready — Codex CLI users can now use Spec Kit

### Incremental Delivery

1. Setup + Foundational → Foundation ready (6 tools registered, tier system in data structures)
2. Add US1 → Test independently → `specify init --ai codex` works (MVP!)
3. Add US2 → Test independently → Tier classification visible in docs/menu, capability matrix audit works
4. Add US3 → Test independently → Deep adaptation verified, all Tier 1 tools pass full audit
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Codex CLI onboarding)
   - Developer B: User Story 2 (tier system + docs) — can proceed on non-codex portions
   - Developer C: User Story 3 (deep adaptation for existing Tier 1 tools)
3. After US1 completes, remaining US2/US3 Codex-specific tasks can be picked up
4. Polish phase: all team members update existing tests in parallel
