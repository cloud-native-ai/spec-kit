# Tasks: Tier 2 Agent Support for Hermes-Agent and iFlow

**Requirement ID**: 019 (from branch name)
**Requirement Key**: 019-tier2-hermes-iflow
**Related Feature**: 022 AI Tools Support (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/019-tier2-hermes-iflow/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), data-model.md, contracts/

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates tests BEFORE implementation)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: Both `hermes` and `iflow` entries added to all 8 config dicts in `src/specify_cli/__init__.py`
- DoD-2: Init flow generates command templates, skills symlinks, and agents symlinks for both tools
- DoD-3: All contract, integration, and unit tests pass (`pytest`)
- DoD-4: Constitution Principle V updated with Hermes Agent and iFlow in Tier 2
- DoD-5: README, quickstart, and installation docs list both new Tier 2 tools
- DoD-6: CLI `--help` output lists hermes and iflow as Tier 2 options
- DoD-7: Multi-tool coexistence verified (8 tools, zero conflicts)

**DoD Status**: pending

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Verify baseline state before making changes

- [ ] T001 Run existing test suite to confirm green baseline: `pytest` from repo root
- [ ] T002 Record current assistant count (6) and Tier 2 count (1) for regression reference

---

## Phase 2: Foundational (Config Dict Additions)

**Purpose**: Add `hermes` and `iflow` entries to all config dictionaries. These changes are the shared prerequisite for both user stories.

**⚠️ CRITICAL**: No user story init-flow work can begin until config dicts are complete.

### Tests for Foundational Phase (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T003 [P] Contract test: assert `"hermes" in AGENT_CONFIG` and AGENT_CONFIG["hermes"] has required fields (name="Hermes Agent", folder=".hermes/", requires_cli=True) in `tests/contract/test_hermes_init_contract.py` (C-001)
- [ ] T004 [P] Contract test: assert `"iflow" in AGENT_CONFIG` and AGENT_CONFIG["iflow"] has required fields (name="iFlow", folder=".iflow/", requires_cli=True) in `tests/contract/test_iflow_init_contract.py` (C-001)
- [ ] T005 [P] Contract test: assert `_ASSISTANT_TIERS["hermes"] == "tier2"` and `_ASSISTANT_TIERS["iflow"] == "tier2"` in `tests/contract/test_hermes_init_contract.py` and `tests/contract/test_iflow_init_contract.py` (C-003)
- [ ] T006 [P] Contract test: assert `len(_OFFICIAL_ASSISTANT_KEYS) == 8` and both `"hermes"` and `"iflow"` are present in `tests/contract/test_tier_ordering_contract.py` (C-011, update existing)
- [ ] T007 [P] Contract test: assert all Tier 1 keys appear before all Tier 2 keys in `_OFFICIAL_ASSISTANT_KEYS` in `tests/contract/test_tier_ordering_contract.py` (C-004, update existing)
- [ ] T008 [P] Contract test: assert `get_assistant_profile("hermes")` and `get_assistant_profile("iflow")` return complete profiles with correct tier, officially_supported, skills_symlink fields in `tests/contract/test_hermes_init_contract.py` and `tests/contract/test_iflow_init_contract.py` (C-010)

### Implementation for Foundational Phase

- [ ] T009 Add `"hermes"` entry to `AGENT_CONFIG` dict in `src/specify_cli/__init__.py` with name="Hermes Agent", folder=".hermes/", install_url=None, requires_cli=True
- [ ] T010 Add `"iflow"` entry to `AGENT_CONFIG` dict in `src/specify_cli/__init__.py` with name="iFlow", folder=".iflow/", install_url=None, requires_cli=True
- [ ] T011 Append `"hermes"` and `"iflow"` to `_OFFICIAL_ASSISTANT_KEYS` list after `"qwen"` (Tier 2 section) in `src/specify_cli/__init__.py`
- [ ] T012 Add `"hermes": ".hermes/commands"` and `"iflow": ".iflow/commands"` to `_ASSISTANT_COMMAND_DIRS` in `src/specify_cli/__init__.py`
- [ ] T013 Add `"hermes": "md"` and `"iflow": "md"` to `_ASSISTANT_EXTENSIONS` in `src/specify_cli/__init__.py`
- [ ] T014 Add `"hermes": "$ARGUMENTS"` and `"iflow": "$ARGUMENTS"` to `_ASSISTANT_ARG_FORMATS` in `src/specify_cli/__init__.py`
- [ ] T015 Add `"hermes"` and `"iflow"` to `_SKILLS_SYMLINK_ASSISTANTS` set in `src/specify_cli/__init__.py`
- [ ] T016 Add `"hermes": "tier2"` and `"iflow": "tier2"` to `_ASSISTANT_TIERS` in `src/specify_cli/__init__.py`
- [ ] T017 Add `"hermes": "HERMES.md"` and `"iflow": "IFLOW.md"` to `_INSTRUCTIONS_FILE_MAP` in `src/specify_cli/__init__.py`
- [ ] T018 Run foundational contract tests (T003–T008) and verify they pass

**Checkpoint**: Config dicts complete — both tools are registered. Init flow and user story work can proceed.

---

## Phase 3: User Story 1 — Hermes-Agent 纳入 Tier 2 支持 (Priority: P1) 🎯 MVP

**Goal**: Users can run `specify init --ai hermes` and get a fully functional Spec Kit workspace with `.hermes/` config directory, command templates, and symlinks.

**Independent Test**: Run `specify init . --ai hermes` in an empty project, verify `.hermes/commands/` exists with `.md` command files, `.hermes/skills` symlink points to `.specify/skills/`, and init summary shows "Tier 2".

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T019 [P] [US1] Integration test: `specify init . --ai hermes` creates `.hermes/` directory and `.hermes/commands/` with at least one `.md` file in `tests/integration/test_hermes_init.py` (C-012)
- [ ] T020 [P] [US1] Integration test: `specify init . --ai hermes` creates `.hermes/skills` symlink pointing to `.specify/skills/` in `tests/integration/test_hermes_init.py` (C-013)
- [ ] T021 [P] [US1] Integration test: `specify init . --ai hermes` on a project with existing `.specify/` core files does not overwrite them in `tests/integration/test_hermes_init.py` (C-014)
- [ ] T022 [P] [US1] Contract test: `InitializationResultSummary.set_configured_assistants(["hermes"])` sets `assistant_tiers["hermes"] == "tier2"` and `render_rich()` contains "(Tier 2)" in `tests/contract/test_hermes_init_contract.py` (C-016)

### Implementation for User Story 1

- [ ] T023 [US1] Add `elif ai_assistant == "hermes"` branch in `copy_local_templates()` for command generation: `generate_commands("hermes", "md", "$ARGUMENTS", project_path / ".hermes" / "commands", script_type)` in `src/specify_cli/__init__.py`
- [ ] T024 [US1] Add skills symlink block for hermes: `if ai_assistant == "hermes": ensure_specify_symlink(project_path, ".hermes", "skills")` in `src/specify_cli/__init__.py`
- [ ] T025 [US1] Add agents symlink block for hermes: `if ai_assistant == "hermes": ensure_specify_symlink(project_path, ".hermes", "agents")` in `src/specify_cli/__init__.py`
- [ ] T026 [US1] Run US1 tests (T019–T022) and verify they pass

**Checkpoint**: `specify init --ai hermes` produces a complete Hermes-Agent workspace. US1 is independently functional.

---

## Phase 4: User Story 2 — iFlow 纳入 Tier 2 支持 (Priority: P1)

**Goal**: Users can run `specify init --ai iflow` and get a fully functional Spec Kit workspace with `.iflow/` config directory, command templates, and symlinks.

**Independent Test**: Run `specify init . --ai iflow` in an empty project, verify `.iflow/commands/` exists with `.md` command files, `.iflow/skills` symlink points to `.specify/skills/`, and init summary shows "Tier 2".

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T027 [P] [US2] Integration test: `specify init . --ai iflow` creates `.iflow/` directory and `.iflow/commands/` with at least one `.md` file in `tests/integration/test_iflow_init.py` (C-012)
- [ ] T028 [P] [US2] Integration test: `specify init . --ai iflow` creates `.iflow/skills` symlink pointing to `.specify/skills/` in `tests/integration/test_iflow_init.py` (C-013)
- [ ] T029 [P] [US2] Integration test: `specify init . --ai iflow` on a project with existing `.specify/` core files does not overwrite them in `tests/integration/test_iflow_init.py` (C-014)
- [ ] T030 [P] [US2] Contract test: `InitializationResultSummary.set_configured_assistants(["iflow"])` sets `assistant_tiers["iflow"] == "tier2"` and `render_rich()` contains "(Tier 2)" in `tests/contract/test_iflow_init_contract.py` (C-016)

### Implementation for User Story 2

- [ ] T031 [US2] Add `elif ai_assistant == "iflow"` branch in `copy_local_templates()` for command generation: `generate_commands("iflow", "md", "$ARGUMENTS", project_path / ".iflow" / "commands", script_type)` in `src/specify_cli/__init__.py`
- [ ] T032 [US2] Add skills symlink block for iflow: `if ai_assistant == "iflow": ensure_specify_symlink(project_path, ".iflow", "skills")` in `src/specify_cli/__init__.py`
- [ ] T033 [US2] Add agents symlink block for iflow: `if ai_assistant == "iflow": ensure_specify_symlink(project_path, ".iflow", "agents")` in `src/specify_cli/__init__.py`
- [ ] T034 [US2] Run US2 tests (T027–T030) and verify they pass

**Checkpoint**: `specify init --ai iflow` produces a complete iFlow workspace. US2 is independently functional.

---

## Phase 5: User Story 3 — 8 工具共存与一致性审计 (Priority: P2)

**Goal**: All 8 supported AI tools coexist in a single project without conflicts, and the capability matrix audit correctly covers all tools with tier-appropriate checks.

**Independent Test**: In the same project, init Claude Code + Hermes-Agent + iFlow sequentially, verify core `.specify/` files unchanged, run capability matrix audit, verify hermes and iflow appear with correct tier2 status.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T035 [P] [US3] Contract test: `audit_capability_matrix()` returns entries for both `"hermes"` and `"iflow"` across all 6 dimensions (12 new entries) in `tests/contract/test_capability_matrix_contract.py` (C-015, update existing)
- [ ] T036 [P] [US3] Integration test: sequential init of claude + hermes + iflow in same project preserves `.specify/` core and all tool configs coexist in `tests/integration/test_ai_tools_multi_assistant_coexistence.py` (C-014, update existing)
- [ ] T037 [P] [US3] Contract test: update `test_ai_tools_support_contract.py` to assert total official assistant count is 8 (C-011, update existing)

### Implementation for User Story 3

- [ ] T038 [US3] Update CLI `--ai` option help string in `init()` command to include hermes and iflow as Tier 2 options in `src/specify_cli/__init__.py` (C-017)
- [ ] T039 [US3] Update `--ignore-agent-tools` help string to mention Hermes Agent and iFlow in `src/specify_cli/__init__.py`
- [ ] T040 [US3] Update `specify init` examples docstring to include `--ai hermes` and `--ai iflow` examples in `src/specify_cli/__init__.py`
- [ ] T041 [US3] Run US3 tests (T035–T037) and verify they pass

**Checkpoint**: All 8 tools coexist, audit covers new tools. US3 is verified.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Documentation, constitution, and final validation across all stories

- [ ] T042 [P] Update Constitution Principle V in `.specify/memory/constitution.md`: add Hermes Agent and iFlow to official agent list, update Tier 2 line to include 3 tools, bump version to 1.2.0
- [ ] T043 [P] Update README.md: add Hermes Agent and iFlow entries under "Tier 2 (Standard Support)" section
- [ ] T044 [P] Update `docs/quickstart.md`: add hermes and iflow to tool list references where Tier 2 tools are mentioned
- [ ] T045 [P] Update `docs/installation.md`: add hermes and iflow to tool list references where supported tools are listed
- [ ] T046 Update `test_ai_tools_init_all_assistants.py` in `tests/integration/` to include hermes and iflow in the all-assistant init loop
- [ ] T047 Run full test suite: `pytest` from repo root — all tests must pass
- [ ] T048 Run quickstart.md validation: manually verify scenarios from `.specify/specs/019-tier2-hermes-iflow/quickstart.md`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup — BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational (Phase 2) — no dependency on US2
- **User Story 2 (Phase 4)**: Depends on Foundational (Phase 2) — no dependency on US1
- **User Story 3 (Phase 5)**: Depends on US1 and US2 completion (needs both tools in init flow)
- **Polish (Phase 6)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational — independent of US2
- **User Story 2 (P1)**: Can start after Foundational — independent of US1
- **User Story 3 (P2)**: Requires both US1 and US2 — tests multi-tool coexistence

### Within Each User Story

- Tests MUST be written and FAIL before implementation (TDD)
- Init-flow command generation before symlink blocks
- All story tasks before checkpoint verification

### Parallel Opportunities

- T003–T008 (foundational tests) can all run in parallel — different test files
- T009–T017 (config dict entries) touch the same file but different dict sections — sequential recommended
- US1 (Phase 3) and US2 (Phase 4) can run in parallel after Foundational — different `elif` branches and symlink blocks in the same file, but non-overlapping sections
- T042–T045 (documentation updates) can all run in parallel — different files
- T019–T022 (US1 tests) can run in parallel — same test file but independent test functions
- T027–T030 (US2 tests) can run in parallel — same test file but independent test functions

---

## Parallel Example: Foundational Tests

```bash
# Launch all foundational contract tests in parallel:
Task T003: "Contract test for hermes in AGENT_CONFIG in tests/contract/test_hermes_init_contract.py"
Task T004: "Contract test for iflow in AGENT_CONFIG in tests/contract/test_iflow_init_contract.py"
Task T005: "Contract test for tier classification in test_hermes_init_contract.py and test_iflow_init_contract.py"
Task T006: "Contract test for 8-tool count in tests/contract/test_tier_ordering_contract.py"
Task T007: "Contract test for tier ordering in tests/contract/test_tier_ordering_contract.py"
Task T008: "Contract test for get_assistant_profile in test_hermes_init_contract.py and test_iflow_init_contract.py"
```

## Parallel Example: US1 and US2 Simultaneously

```bash
# After Foundational phase, both user stories can proceed:
# Developer A: US1 (Hermes-Agent)
Task T019-T022: US1 tests
Task T023-T025: US1 init-flow implementation

# Developer B: US2 (iFlow)  
Task T027-T030: US2 tests
Task T031-T033: US2 init-flow implementation
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (verify green baseline)
2. Complete Phase 2: Foundational (all config dicts for BOTH tools)
3. Complete Phase 3: User Story 1 (Hermes-Agent init flow)
4. **STOP and VALIDATE**: `specify init . --ai hermes` works end-to-end
5. Continue with US2 and US3

### Incremental Delivery

1. Setup + Foundational → Config dicts registered for both tools
2. Add US1 (Hermes-Agent) → Test independently → Hermes-Agent usable
3. Add US2 (iFlow) → Test independently → iFlow usable
4. Add US3 (coexistence) → Verify 8-tool coexistence
5. Polish → Documentation, constitution, final validation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- All source code changes are in `src/specify_cli/__init__.py` — single file, but changes touch distinct sections
- Config dict additions (Phase 2) add entries for BOTH tools together since they're in the same dicts
- Init-flow branches (US1/US2) are separate `elif` blocks — no overlap
- Deferral discipline: prefer `[~]` over leaving a task `[ ]` "for now"
