# Tasks: Claude Code Support

**Requirement ID**: 009
**Requirement Key**: 009-claude-code-support
**Related Feature**: 021 Claude Code Support
**Input**: Design documents from `.specify/specs/009-claude-code-support/`
**Prerequisites**: plan.md, requirements.md, research.md, data-model.md, contracts/claude-code-support.openapi.yaml, quickstart.md

**Tests**: Automated tests are mandatory for this feature because the constitution requires test-first and contract-driven implementation, and the plan explicitly calls for contract, integration, and unit tests before implementation.

**Organization**: Tasks are grouped by user story so each story can be independently implemented, independently tested, and accepted as an incremental slice.

## Definition of Done (DoD)

- [ ] Each task satisfies the referenced requirement, design artifact, and user-story acceptance criteria.
- [ ] Contract, integration, and unit tests are written before implementation and fail for the missing behavior first.
- [ ] All automated tests pass for affected contract, integration, and unit suites.
- [ ] Claude Code support is consistent across governance, CLI help, docs, templates, generated assets, and packaged resources.
- [ ] `.claudeignore` protects local/generated/private content without excluding required Spec Kit workflow artifacts.
- [ ] Existing Copilot, Qwen Code, opencode, and Qoder integrations remain unchanged unless their canonical shared source changes.
- [ ] Quickstart validation scenarios are completed or documented with any environment-dependent skips.
- [ ] Feature 021 memory and feature index remain synchronized with implementation outcomes.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel because it touches different files and has no dependency on incomplete tasks.
- **[Story]**: `US1`, `US2`, or `US3`; required only for user-story phase tasks.
- Every task includes at least one exact file path.

## Path Conventions

- Python CLI source: `src/specify_cli/__init__.py`
- Bash instruction refresh: `scripts/bash/generate-instructions.sh` and `.specify/scripts/bash/generate-instructions.sh`
- Canonical command templates: `templates/commands/*.md`
- Generated assistant assets under test: `.claude/commands/`, `CLAUDE.md`, `.claudeignore`, and `.specify/instructions.md`
- Tests: `tests/contract/`, `tests/integration/`, and `tests/unit/`
- Documentation and governance: `.specify/memory/constitution.md`, `README.md`, `docs/installation.md`, `docs/usage.md`, `docs/quickstart.md`, and `.specify/memory/features/021.md`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Prepare test helpers, fixtures, and command inventory utilities needed by all user stories.

- [x] T001 Create Claude Code temporary workspace fixtures in tests/conftest.py
- [x] T002 [P] Add reusable Claude Code init and refresh invocation helpers in tests/script_api.py
- [x] T003 [P] Create canonical command inventory helper for Claude Code coverage checks in tests/unit/test_claude_command_generation.py
- [x] T004 [P] Create `.claudeignore` expected-pattern fixture data in tests/unit/test_claude_ignore_policy.py
- [x] T005 [P] Create support-surface fixture definitions for Claude Code audits in tests/unit/test_claude_support_surfaces.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Establish governance approval, assistant metadata invariants, and shared validation contracts before user-story implementation begins.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete because Claude Code is currently not in the constitution-approved assistant list.

### Foundational Tests

- [x] T006 [P] Add contract coverage for `/assistants` including `claude` approval requirements in tests/contract/test_claude_support_contract.py
- [x] T007 [P] Add unit coverage for assistant support matrix invariants including unique `claude` key, display name, folder, install URL, and CLI requirement in tests/unit/test_claude_support_matrix.py
- [x] T008 [P] Add unit coverage for governance/support-surface release blockers in tests/unit/test_claude_support_surfaces.py

### Foundational Implementation

- [x] T009 Update approved assistant governance to include Claude Code in .specify/memory/constitution.md
- [x] T010 Update assistant support matrix metadata for Claude Code in src/specify_cli/__init__.py
- [x] T011 [P] Update public supported-agent list for Claude Code in README.md
- [x] T012 [P] Update installation prerequisites and `--ai claude` examples in docs/installation.md
- [x] T013 [P] Update quickstart assistant setup guidance for Claude Code in docs/quickstart.md
- [x] T014 [P] Update usage guide with Claude Code maintenance and refresh workflow in docs/usage.md
- [x] T015 Record foundational governance and task-splitting notes in .specify/memory/features/021.md

**Checkpoint**: Governance, support matrix, and documentation baseline are ready; user-story implementation can proceed.

---

## Phase 3: User Story 1 - Start a Claude Code Ready Project (Priority: P1) 🎯 MVP

**Goal**: A user can initialize a new Spec Kit project with Claude Code and receive Claude Code guidance, custom commands, `.claudeignore`, and usable Spec Kit workflow assets.

**Independent Test**: Run the Claude Code initialization path in a temporary project and verify `.claude/commands/`, `CLAUDE.md`, `.claudeignore`, and `.specify/` workflow assets exist with complete command coverage.

### Tests for User Story 1 (MANDATORY)

> **NOTE: Write these tests FIRST and ensure they fail before implementation.**

- [x] T016 [P] [US1] Add contract coverage for Claude Code project initialization request and generated asset result in tests/contract/test_claude_init_contract.py
- [x] T017 [P] [US1] Add integration coverage for new-project initialization with `--ai claude` in tests/integration/test_claude_init.py
- [x] T018 [P] [US1] Add integration coverage for current-directory initialization with `--ai claude --ignore-agent-tools` in tests/integration/test_claude_init.py
- [x] T019 [P] [US1] Add unit coverage for Claude Code command generation inventory and `$ARGUMENTS` handoff in tests/unit/test_claude_command_generation.py
- [x] T020 [P] [US1] Add unit coverage for `.claudeignore` defaults preserving required `.specify/` workflow paths in tests/unit/test_claude_ignore_policy.py

### Manual Verification for User Story 1

- [ ] T021 [US1] Manual QA: validate quickstart scenarios 1, 5, 6, and 8 in .specify/specs/009-claude-code-support/quickstart.md

### Implementation for User Story 1

- [x] T022 [US1] Extend `--ai` help text, validation choices, and interactive assistant selection for `claude` in src/specify_cli/__init__.py
- [x] T023 [US1] Generate Claude Code custom commands into `.claude/commands/` from `templates/commands/*.md` in src/specify_cli/__init__.py
- [x] T024 [US1] Ensure generated Claude Code command files preserve canonical descriptions and `$ARGUMENTS` semantics in src/specify_cli/__init__.py
- [x] T025 [US1] Add Claude Code guidance/compatibility file generation for `CLAUDE.md` from canonical `.specify/instructions.md` in src/specify_cli/__init__.py
- [x] T026 [US1] Add `.claudeignore` generation during project initialization in src/specify_cli/__init__.py
- [x] T027 [US1] Add default `.claudeignore` template content that excludes dependency, cache, build, temporary, local environment, and secret-like paths in templates/claudeignore-template
- [x] T028 [US1] Ensure `.claudeignore` template keeps `.specify/instructions.md`, `.specify/specs/`, `.specify/memory/`, and `.claude/commands/` accessible in templates/claudeignore-template
- [x] T029 [US1] Add Claude Code skills compatibility link creation for `.claude/skills` to `.specify/skills` in src/specify_cli/__init__.py
- [x] T030 [US1] Include Claude Code assets in packaged template resources via pyproject.toml
- [x] T031 [US1] Update setup success output to show Claude Code next steps and custom command location in src/specify_cli/__init__.py

**Checkpoint**: User Story 1 is independently functional as the MVP.

---

## Phase 4: User Story 2 - Adopt Claude Code in an Existing Project (Priority: P2)

**Goal**: A maintainer can add or refresh Claude Code support in an existing Spec Kit workspace without disrupting other assistant integrations or user customizations.

**Independent Test**: Run the refresh flow in a workspace that already has Copilot, Qwen Code, opencode, Qoder, and customized Claude Code files; verify Claude Code assets update safely and unrelated assistant roots remain untouched.

### Tests for User Story 2 (MANDATORY)

> **NOTE: Write these tests FIRST and ensure they fail before implementation.**

- [x] T032 [P] [US2] Add contract coverage for Claude Code refresh success and conflict responses in tests/contract/test_claude_refresh_contract.py
- [x] T033 [P] [US2] Add integration coverage for non-destructive Claude Code refresh with existing assistant roots in tests/integration/test_claude_refresh.py
- [x] T034 [P] [US2] Add integration coverage for customized Claude Code file preservation and conflict reporting in tests/integration/test_claude_refresh.py
- [x] T035 [P] [US2] Add integration coverage for missing Claude Code tool guidance and `--ignore-agent-tools` behavior in tests/integration/test_claude_validation.py
- [x] T036 [P] [US2] Add unit coverage for Claude Code refresh helper behavior in tests/unit/test_claude_refresh_helpers.py

### Manual Verification for User Story 2

- [ ] T037 [US2] Manual QA: validate quickstart scenarios 2, 3, and 4 in .specify/specs/009-claude-code-support/quickstart.md

### Implementation for User Story 2

- [x] T038 [US2] Implement Claude Code missing-tool detection and install/setup guidance in src/specify_cli/__init__.py
- [x] T039 [US2] Implement Claude Code `--ignore-agent-tools` bypass parity with existing CLI assistants in src/specify_cli/__init__.py
- [x] T040 [US2] Extend instruction refresh to create or update Claude Code compatibility links in scripts/bash/generate-instructions.sh
- [x] T041 [US2] Mirror Claude Code instruction refresh behavior in .specify/scripts/bash/generate-instructions.sh
- [x] T042 [US2] Implement `.claudeignore` refresh preservation and conflict guidance in src/specify_cli/__init__.py
- [x] T043 [US2] Ensure refresh leaves `.github/`, `.qwen/`, `.opencode/`, and `.qoder/` assistant roots untouched unless their canonical shared source changes in src/specify_cli/__init__.py
- [x] T044 [US2] Update generated instruction template guidance for Claude Code compatibility in templates/instructions-template.md

**Checkpoint**: User Story 2 is independently functional and safe for existing workspaces.

---

## Phase 5: User Story 3 - Validate Claude Code Support Consistency (Priority: P3)

**Goal**: Contributors can audit and validate Claude Code support across governance, docs, CLI help, templates, generated assets, and release outputs with no contradictory support claims.

**Independent Test**: Run support-surface and distribution audits and verify Claude Code appears consistently wherever supported assistants are enumerated.

### Tests for User Story 3 (MANDATORY)

> **NOTE: Write these tests FIRST and ensure they fail before implementation.**

- [x] T045 [P] [US3] Add contract coverage for `/audits/claude-code-support` and `/assistants/claude/commands/coverage` in tests/contract/test_claude_support_surfaces_contract.py
- [x] T046 [P] [US3] Add integration coverage for generated project distribution consistency in tests/integration/test_claude_distribution.py
- [x] T047 [P] [US3] Add unit coverage for CLI help, README, docs, templates, and governance support-surface audits in tests/unit/test_claude_support_surfaces.py
- [x] T048 [P] [US3] Add unit coverage for packaged resource inclusion of Claude Code assets in tests/unit/test_claude_distribution.py

### Manual Verification for User Story 3

- [ ] T049 [US3] Manual QA: validate quickstart scenario 7 in .specify/specs/009-claude-code-support/quickstart.md

### Implementation for User Story 3

- [x] T050 [US3] Update `specify init --help`, invalid assistant error text, and `check` output support claims for Claude Code in src/specify_cli/__init__.py
- [x] T051 [US3] Update supported-agent references and Claude Code overview in README.md
- [x] T052 [P] [US3] Update Claude Code installation and validation examples in docs/installation.md
- [x] T053 [P] [US3] Update Claude Code workflow and maintenance instructions in docs/usage.md
- [x] T054 [P] [US3] Update quickstart assistant selection examples for Claude Code in docs/quickstart.md
- [x] T055 [P] [US3] Update AI agent integration guidance for Claude Code in templates/plan-template.md
- [x] T056 [P] [US3] Update agent/provider whitelist guidance for Claude Code in templates/commands/agents.md
- [x] T057 [P] [US3] Update instruction compatibility guidance for Claude Code in templates/instructions-template.md
- [x] T058 [US3] Add release audit coverage for Claude Code docs, templates, generated assets, and package resources in tests/integration/test_claude_distribution.py

**Checkpoint**: User Story 3 validates release-ready consistency for Claude Code support.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, cleanup, and feature-memory synchronization after all selected user stories are complete.

- [x] T059 [P] Run focused contract tests for Claude Code support in tests/contract/test_claude_init_contract.py, tests/contract/test_claude_refresh_contract.py, and tests/contract/test_claude_support_surfaces_contract.py
- [x] T060 [P] Run focused integration tests for Claude Code support in tests/integration/test_claude_init.py, tests/integration/test_claude_refresh.py, tests/integration/test_claude_validation.py, and tests/integration/test_claude_distribution.py
- [x] T061 [P] Run focused unit tests for Claude Code support in tests/unit/test_claude_support_matrix.py, tests/unit/test_claude_command_generation.py, tests/unit/test_claude_ignore_policy.py, tests/unit/test_claude_refresh_helpers.py, tests/unit/test_claude_support_surfaces.py, and tests/unit/test_claude_distribution.py
- [ ] T062 Run full regression test suite with pytest from repository root
- [ ] T063 Validate quickstart scenarios and record any environment-dependent notes in .specify/specs/009-claude-code-support/quickstart.md
- [x] T064 [P] Refresh generated instructions and compatibility links using scripts/bash/generate-instructions.sh
- [x] T065 Update Feature 021 implementation notes and related files in .specify/memory/features/021.md
- [x] T066 Update Feature 021 timestamp and status consistency in .specify/memory/features.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies; can start immediately.
- **Phase 2 (Foundational)**: Depends on Phase 1 and blocks all user stories because governance approval and support matrix invariants are shared prerequisites.
- **Phase 3 (US1)**: Depends on Phase 2; delivers MVP new-project Claude Code support.
- **Phase 4 (US2)**: Depends on Phase 2; can run in parallel with US1 after shared helpers exist, but final refresh behavior should be validated against US1-generated assets.
- **Phase 5 (US3)**: Depends on Phase 2; can run in parallel with US1/US2 for docs/tests, but final release audit depends on generated assets from US1 and refresh behavior from US2.
- **Phase 6 (Polish)**: Depends on completed selected user stories.

### User Story Dependencies

- **US1 (P1)**: Starts after Foundational; no dependency on US2 or US3.
- **US2 (P2)**: Starts after Foundational; integrates with US1-generated asset conventions but remains independently testable through refresh fixtures.
- **US3 (P3)**: Starts after Foundational; final audit requires US1 and US2 outputs for full pass.

### Within Each User Story

- Tests must be written and fail before implementation.
- Contract tests before integration tests where endpoint/operation behavior is involved.
- Support matrix and governance updates before CLI selection behavior is treated as complete.
- Command generation before command coverage audit can pass.
- `.claudeignore` generation before ignore policy audit can pass.
- Docs and templates before support-surface release audit can pass.

### Parallel Opportunities

- Setup tasks T002 through T005 can run in parallel after T001.
- Foundational tests T006 through T008 can run in parallel.
- Foundational documentation tasks T011 through T014 can run in parallel after governance wording is agreed in T009.
- US1 test tasks T016 through T020 can run in parallel.
- US2 test tasks T032 through T036 can run in parallel.
- US3 test tasks T045 through T048 can run in parallel.
- US3 documentation/template updates T052 through T057 can run in parallel.
- Polish test runs T059 through T061 can run in parallel.

---

## Parallel Example: User Story 1

```bash
Task: "Add contract coverage for Claude Code project initialization request and generated asset result in tests/contract/test_claude_init_contract.py"
Task: "Add integration coverage for new-project initialization with --ai claude in tests/integration/test_claude_init.py"
Task: "Add unit coverage for Claude Code command generation inventory and $ARGUMENTS handoff in tests/unit/test_claude_command_generation.py"
Task: "Add unit coverage for .claudeignore defaults preserving required .specify/ workflow paths in tests/unit/test_claude_ignore_policy.py"
```

---

## Parallel Example: User Story 2

```bash
Task: "Add contract coverage for Claude Code refresh success and conflict responses in tests/contract/test_claude_refresh_contract.py"
Task: "Add integration coverage for non-destructive Claude Code refresh with existing assistant roots in tests/integration/test_claude_refresh.py"
Task: "Add integration coverage for missing Claude Code tool guidance and --ignore-agent-tools behavior in tests/integration/test_claude_validation.py"
Task: "Add unit coverage for Claude Code refresh helper behavior in tests/unit/test_claude_refresh_helpers.py"
```

---

## Parallel Example: User Story 3

```bash
Task: "Add contract coverage for /audits/claude-code-support and /assistants/claude/commands/coverage in tests/contract/test_claude_support_surfaces_contract.py"
Task: "Add integration coverage for generated project distribution consistency in tests/integration/test_claude_distribution.py"
Task: "Update Claude Code installation and validation examples in docs/installation.md"
Task: "Update agent/provider whitelist guidance for Claude Code in templates/commands/agents.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1 setup helpers.
2. Complete Phase 2 governance and support matrix prerequisites.
3. Complete Phase 3 tests and implementation for Claude Code new-project setup.
4. Stop and validate quickstart scenarios 1, 5, 6, and 8.
5. Demo `specify init <project> --ai claude` producing Claude Code-ready assets.

### Incremental Delivery

1. Deliver US1 for new-project Claude Code readiness.
2. Deliver US2 for existing-workspace refresh, user customization preservation, and missing-tool guidance.
3. Deliver US3 for support-surface consistency and release/package audit.
4. Complete Phase 6 regression, quickstart, instruction refresh, and feature-memory updates.

### Parallel Team Strategy

1. One contributor prepares setup/foundational helpers and governance.
2. One contributor implements US1 command/ignore asset generation after foundational tests exist.
3. One contributor implements US2 refresh and preservation behavior after foundational tests exist.
4. One contributor implements US3 documentation/template/audit coverage after foundational tests exist.
5. Rejoin for Phase 6 regression and feature-memory synchronization.

## Notes

- Input arguments were empty; tasks were generated entirely from requirements, plan, data model, contract, research, and quickstart artifacts.
- Tests are intentionally included in every user-story phase because the plan and constitution require test-first validation.
- Claude Code governance approval is the highest-priority blocker and must remain visible until constitution and support claims are updated.
