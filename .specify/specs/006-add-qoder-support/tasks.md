# Tasks: Add Qoder Support

**Requirement ID**: 006
**Requirement Key**: 006-add-qoder-support
**Related Feature**: 020 Qoder Support
**Input**: Design documents from `.specify/specs/006-add-qoder-support/`
**Prerequisites**: plan.md, requirements.md, research.md, data-model.md, contracts/qoder-support.openapi.yaml, quickstart.md

**Tests**: To meet the independent acceptance criteria in requirements as well as contract/quick validation scenarios, automated test tasks are generated as mandatory items in each user story.

**Organization**: Tasks are grouped by user story, ensuring each story can be independently implemented, independently tested, and independently accepted.

## Definition of Done (DoD)

- [ ] Changes satisfy the corresponding functional requirements and boundary conditions in requirements.md
- [ ] [CN]
- [ ] quickstart.md [CN]
- [ ] [CN]
- [ ] [CN] Copilot/Qwen/opencode [CN]
- [ ] [CN] SC-001 ~ SC-005 [CN]

## Format: `[ID] [P?] [Story] Description`

- **[P]**: [CN]
- **[Story]**: [CN] `US1`[CN]`US2`[CN]`US3`[CN]
- [CN]File path

## Path Conventions

- [CN] Python CLI[CN]`src/`[CN]`tests/`[CN]`templates/`[CN]`scripts/`[CN]`docs/` [CN]
- [CN] `.specify/specs/006-add-qoder-support/`
- Feature [CN] `.specify/memory/`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: [CN]

- [X] T001 Create Qoder CLI bootstrap fixtures and temporary workspace helpers in tests/conftest.py
- [X] T002 [P] Add reusable CLI invocation helpers for init and refresh scenarios in tests/script_api.py
- [X] T003 [P] Create support-surface fixture definitions for Qoder audits in tests/unit/test_qoder_support_surfaces.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: [CN]

**⚠️ CRITICAL**: [CN]

- [X] T004 Update approved assistant governance whitelist to include Qoder in .specify/memory/constitution.md
- [X] T005 [P] Align planning gate language with approved Qoder support in templates/plan-template.md
- [X] T006 [P] Align agent/provider whitelist guidance with Qoder in templates/commands/agents.md
- [X] T007 [P] Add shared assistant matrix invariants for Qoder support in tests/unit/test_qoder_support_matrix.py
- [X] T008 Record task-splitting notes and shared asset impact in .specify/memory/features/020.md

**Checkpoint**: [CN]

---

## Phase 3: User Story 1 - [CN] Qoder (Priority: P1) 🎯 MVP

**Goal**: [CN] Qoder[CN]

**Independent Test**: [CN] `specify init <dir> --ai qoder` [CN] `specify init . --ai qoder`[CN] `.qoder/commands/` [CN]

### Tests for User Story 1

- [X] T009 [P] [US1] Add contract coverage for supported-assistant listing and init request rules in tests/contract/test_qoder_init_contract.py
- [X] T010 [P] [US1] Add integration coverage for new-project and existing-directory Qoder bootstrap in tests/integration/test_qoder_init.py
- [X] T011 [P] [US1] Add unit coverage for Qoder bootstrap helper paths in tests/unit/test_qoder_bootstrap.py

### Manual Verification for User Story 1

- [ ] T012 [US1] Manual QA: validate Quickstart scenarios 1-2 in .specify/specs/006-add-qoder-support/quickstart.md

### Implementation for User Story 1

- [X] T013 [US1] Extend assistant metadata, `--ai` help text, CLI detection, and `check()` output for Qoder in src/specify_cli/__init__.py
- [X] T014 [US1] Generate `.qoder/commands/` assets during new-project and current-directory bootstrap in src/specify_cli/__init__.py

**Checkpoint**: User Story 1 [CN]Qoder [CN] MVP

---

## Phase 4: User Story 2 - [CN] Qoder [CN] (Priority: P2)

**Goal**: [CN] Qoder CLI [CN]

**Independent Test**: [CN] `qoder` CLI [CN] `--ignore-agent-tools` [CN]

### Tests for User Story 2

- [X] T015 [P] [US2] Add contract coverage for Qoder validation and refresh behaviors in tests/contract/test_qoder_refresh_contract.py
- [X] T016 [P] [US2] Add integration coverage for missing-CLI guidance and non-destructive refresh in tests/integration/test_qoder_refresh.py
- [X] T017 [P] [US2] Add unit coverage for ignore-check and refresh helper behavior in tests/unit/test_qoder_refresh_helpers.py

### Manual Verification for User Story 2

- [ ] T018 [US2] Manual QA: validate Quickstart scenarios 3-5 in .specify/specs/006-add-qoder-support/quickstart.md

### Implementation for User Story 2

- [X] T019 [US2] Implement Qoder missing-CLI guidance and `--ignore-agent-tools` parity in src/specify_cli/__init__.py
- [X] T020 [US2] Extend Qoder compatibility link generation for refresh flows in scripts/bash/generate-instructions.sh
- [X] T021 [P] [US2] Align instruction generation template with approved Qoder support in templates/instructions-template.md
- [X] T022 [P] [US2] Document Qoder maintenance and refresh workflows in docs/usage.md

**Checkpoint**: User Story 2 [CN]Qoder [CN]

---

## Phase 5: User Story 3 - [CN] (Priority: P3)

**Goal**: [CN] README[CN] Qoder

**Independent Test**: [CN]README[CN] Qoder [CN]

### Tests for User Story 3

- [X] T023 [P] [US3] Add contract coverage for support-surface and distribution audits in tests/contract/test_qoder_support_surfaces_contract.py
- [X] T024 [P] [US3] Add integration coverage for documentation and packaged resource consistency in tests/integration/test_qoder_distribution.py
- [X] T025 [P] [US3] Add unit coverage for support-surface audit rules in tests/unit/test_qoder_support_surfaces.py

### Manual Verification for User Story 3

- [ ] T026 [US3] Manual QA: validate Quickstart scenario 6 in .specify/specs/006-add-qoder-support/quickstart.md

### Implementation for User Story 3

- [X] T027 [US3] Update public support matrix and Qoder overview in README.md
- [X] T028 [P] [US3] Update installation examples and prerequisite guidance for Qoder in docs/installation.md
- [X] T029 [P] [US3] Regenerate supported-agent instruction content for Qoder in .ai/instructions.md
- [X] T030 [P] [US3] Align approved-provider guidance with Qoder in .github/prompts/speckit.agents.prompt.md
- [X] T031 [US3] Ensure packaged template resources continue shipping Qoder-facing assets via pyproject.toml

**Checkpoint**: [CN] Qoder [CN]

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: [CN]

- [X] T032 [P] Regenerate compatibility links and Qoder project rules in scripts/bash/generate-instructions.sh
- [ ] T033 Run end-to-end Qoder quickstart validation and capture final audit notes in .specify/specs/006-add-qoder-support/quickstart.md
- [X] T034 [P] Refresh feature index timestamp while keeping Feature 020 status implemented in .specify/memory/features.md

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: [CN]
- **Phase 2 (Foundational)**: [CN] Phase 1 [CN]
- **Phase 3 (US1)**: [CN] Phase 2[CN] MVP
- **Phase 4 (US2)**: [CN] Phase 2[CN] US1 [CN]
- **Phase 5 (US3)**: [CN] Phase 2[CN] US1/US2 [CN]
- **Phase 6 (Polish)**: [CN]

### User Story Dependencies

- **US1 (P1)**: [CN] Foundational [CN]
- **US2 (P2)**: [CN] US1 [CN] Qoder [CN]
- **US3 (P3)**: [CN] US1/US2 [CN] Qoder [CN]

### Within Each User Story

- [CN]/[CN]/[CN]
- [CN] quickstart [CN]
- [CN]

### Parallel Opportunities

- Phase 1 [CN] `[P]` [CN]
- Phase 2 [CN]
- [CN]
- US3 [CN] README[CN]prompt/[CN]

---

## Parallel Example: User Story 1

```bash
# [CN] US1 [CN]
Task: "Add contract coverage for supported-assistant listing and init request rules in tests/contract/test_qoder_init_contract.py"
Task: "Add integration coverage for new-project and existing-directory Qoder bootstrap in tests/integration/test_qoder_init.py"
Task: "Add unit coverage for Qoder bootstrap helper paths in tests/unit/test_qoder_bootstrap.py"
```

---

## Parallel Example: User Story 3

```bash
# [CN] US3 [CN]
Task: "Update installation examples and prerequisite guidance for Qoder in docs/installation.md"
Task: "Regenerate supported-agent instruction content for Qoder in .ai/instructions.md"
Task: "Align approved-provider guidance with Qoder in .github/prompts/speckit.agents.prompt.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. [CN] Phase 1 [CN] Phase 2
2. [CN] Phase 3[CN]US1[CN]
3. [CN] US1 [CN] quickstart [CN]
4. [CN]“[CN] Qoder”[CN] MVP

### Incremental Delivery

1. [CN] US1[CN]
2. [CN] US2[CN]
3. [CN] US3[CN]
4. [CN]

### Parallel Team Strategy

1. [CN]/[CN]Phase 2[CN]
2. [CN] CLI [CN]US1/US2[CN]
3. [CN]US3[CN]
4. [CN] Phase 6 [CN]

---

## Notes

- [CN] `[P]` [CN]
- [CN]
- [CN] Feature 020 [CN]
- [CN] Phase [CN]