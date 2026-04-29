# Tasks: Skill Install Layout

**Requirement ID**: 007
**Requirement Key**: 007-skill-install-layout
**Related Feature**: 013 Skills Command
**Input**: Design documents from `.specify/specs/007-skill-install-layout/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/skill-install-layout.openapi.yaml, quickstart.md

**User Input Analysis**: `$ARGUMENTS` [CN]

**Tests**: [CN] contract/integration/unit [CN]

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Definition of Done (DoD)

- [ ] [CN] requirements.md [CN] FR-001 ~ FR-016
- [ ] [CN]contract/integration/unit[CN]
- [ ] quickstart [CN]
- [ ] [CN]/[CN]
- [ ] Feature [CN]

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no blocking dependencies)
- **[Story]**: User story label (`[US1]`, `[US2]`, `[US3]`) for story phases only
- [CN]File path

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: [CN]

- [X] T001 [CN] `tests/contracts/test_skill_install_layout_contract.py`[CN]`tests/integration/test_skill_install_layout_integration.py`[CN]`tests/unit/test_skills_utils_layout.py`
- [X] T002 [P] [CN] `tests/fixtures/skill-layout/`
- [X] T003 [P] [CN] `.specify/specs/007-skill-install-layout/quickstart.md` [CN]

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: [CN]

**⚠️ CRITICAL**: [CN]

- [X] T004 [CN] `scripts/bash/create-new-skill.sh` [CN] `.specify/skills`
- [X] T005 [P] [CN] `.specify/scripts/bash/create-new-skill.sh` [CN] `.specify/skills` [CN]
- [X] T006 [CN] `scripts/python/skills-utils.py` [CN] `.specify/skills/*/SKILL.md` [CN] canonical [CN]
- [X] T007 [P] [CN] `.specify/scripts/python/skills-utils.py` [CN] `.specify/skills` [CN]
- [X] T008 [CN] `scripts/python/skills-utils.py` [CN]created/skipped/failed/conflict, success/partial-success/failed[CN]
- [X] T009 [P] [CN] `.specify/scripts/python/skills-utils.py` [CN]
- [X] T010 [CN] `tests/unit/test_skills_utils_layout.py` [CN] `.specify` [CN]

**Checkpoint**: [CN]

---

## Phase 3: User Story 1 - [CN] (Priority: P1) 🎯 MVP

**Goal**: [CN] skill [CN] `.specify/skills/<skill-name>/`[CN]

**Independent Test**: [CN] skill [CN] `.specify/skills/<skill-name>/` [CN]

### Tests for User Story 1

- [X] T011 [P] [US1] [CN] `tests/contracts/test_skill_install_layout_contract.py` [CN] `/skills/{skillName}/install` [CN]
- [X] T012 [P] [US1] [CN] `tests/integration/test_skill_install_layout_integration.py` [CN]

### Implementation for User Story 1

- [X] T013 [US1] [CN] `scripts/bash/create-new-skill.sh` [CN] `.specify/skills/<skill-name>/`
- [X] T014 [US1] [CN] `.specify/scripts/bash/create-new-skill.sh` [CN] `.specify/skills/<skill-name>/`
- [X] T015 [US1] [CN] `templates/commands/skills.md` [CN] `.specify/skills` [CN]
- [X] T016 [US1] [CN] `templates/skills-template.md` [CN] `.github/skills` [CN]
- [X] T017 [US1] [CN] `scripts/bash/create-new-skill.sh` [CN]created/reused/failed[CN]
- [X] T018 [US1] [CN] `.specify/scripts/bash/create-new-skill.sh` [CN]created/reused/failed[CN]

### Manual Verification for User Story 1

- [ ] T019 [US1] [CN] `.specify/specs/007-skill-install-layout/quickstart.md` [CN] Scenario 1 [CN] Scenario 7 [CN]

**Checkpoint**: US1 [CN]

---

## Phase 4: User Story 2 - [CN] (Priority: P2)

**Goal**: [CN]+[CN]

**Independent Test**: [CN] skill [CN]`.github/skills/<skill-name>` [CN] partial-success[CN]

### Tests for User Story 2

- [X] T020 [P] [US2] [CN] `tests/contracts/test_skill_install_layout_contract.py` [CN] `/skills/{skillName}/entrypoints` [CN] mode/status [CN]
- [X] T021 [P] [US2] [CN] `tests/integration/test_skill_install_layout_integration.py` [CN] GitHub [CN]/[CN]
- [X] T022 [P] [US2] [CN] `tests/integration/test_skill_install_layout_integration.py` [CN] placeholder [CN]

### Implementation for User Story 2

- [X] T023 [US2] [CN] `scripts/bash/create-new-skill.sh` [CN]symlink [CN]placeholder [CN]
- [X] T024 [US2] [CN] `.specify/scripts/bash/create-new-skill.sh` [CN]
- [X] T025 [US2] [CN] `scripts/python/skills-utils.py` [CN]
- [X] T026 [US2] [CN] `.specify/scripts/python/skills-utils.py` [CN]
- [X] T027 [US2] [CN] `scripts/bash/create-new-skill.sh` [CN] placeholder [CN] `README.md`[CN] skill [CN]
- [X] T028 [US2] [CN] `.specify/scripts/bash/create-new-skill.sh` [CN] placeholder [CN]

### Manual Verification for User Story 2

- [ ] T029 [US2] [CN] `.specify/specs/007-skill-install-layout/quickstart.md` [CN] Scenario 2 [CN] Scenario 3 [CN]

**Checkpoint**: US2 [CN]

---

## Phase 5: User Story 3 - [CN] (Priority: P3)

**Goal**: [CN] `.github/skills/<skill-name>` [CN]

**Independent Test**: [CN] manual-required[CN]

### Tests for User Story 3

- [ ] T030 [P] [US3] [CN] `tests/contracts/test_skill_install_layout_contract.py` [CN] `/skills/{skillName}/migrate-legacy` [CN]/422 [CN]
- [X] T031 [P] [US3] [CN] `tests/integration/test_skill_install_layout_integration.py` [CN]+[CN]+[CN]
- [X] T032 [P] [US3] [CN] `tests/integration/test_skill_install_layout_integration.py` [CN] manual-required [CN]
- [X] T033 [P] [US3] [CN] `tests/integration/test_skill_install_layout_integration.py` [CN]/[CN]

### Implementation for User Story 3

- [X] T034 [US3] [CN] `scripts/bash/create-new-skill.sh` [CN] `.github/skills` [CN]
- [X] T035 [US3] [CN] `.specify/scripts/bash/create-new-skill.sh` [CN]
- [X] T036 [US3] [CN] `scripts/bash/create-new-skill.sh` [CN]
- [X] T037 [US3] [CN] `.specify/scripts/bash/create-new-skill.sh` [CN]
- [X] T038 [US3] [CN] `scripts/bash/create-new-skill.sh` [CN]
- [X] T039 [US3] [CN] `.specify/scripts/bash/create-new-skill.sh` [CN]

### Manual Verification for User Story 3

- [ ] T040 [US3] [CN] `.specify/specs/007-skill-install-layout/quickstart.md` [CN] Scenario 4[CN]Scenario 5[CN]Scenario 6 [CN]

**Checkpoint**: US3 [CN]

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: [CN]

- [X] T041 [P] [CN] `README.md` [CN] `docs/skills/vscode.md`[CN] `.specify/skills` [CN]`.github/skills` [CN]
- [X] T042 [P] [CN] `docs/usage.md` [CN] `/speckit.skills` [CN]
- [X] T043 [CN] `.specify/memory/features/013.md`[CN] tasks [CN]
- [X] T044 [CN] `.specify/memory/features.md` [CN] Feature 013 [CN] Last Updated [CN] Implemented
- [X] T045 [CN] `tests/contracts/test_skill_install_layout_contract.py`[CN]`tests/integration/test_skill_install_layout_integration.py`[CN]`tests/unit/test_skills_utils_layout.py`
- [ ] T046 [CN] `.specify/specs/007-skill-install-layout/quickstart.md` [CN]

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: [CN]
- **Phase 2 (Foundational)**: [CN] Phase 1[CN]
- **Phase 3 (US1)**: [CN] Phase 2 [CN]
- **Phase 4 (US2)**: [CN] Phase 2 [CN] US1 [CN]
- **Phase 5 (US3)**: [CN] Phase 3 [CN] Phase 4 [CN]/[CN]
- **Phase 6 (Polish)**: [CN]

### User Story Dependencies

- **US1 (P1)**: MVP[CN]
- **US2 (P2)**: [CN]
- **US3 (P3)**: [CN]

### Within Each User Story

- [CN]
- [CN]
- [CN] quickstart [CN]

### Parallel Opportunities

- Setup [CN] T002/T003 [CN]
- Foundational [CN] T005/T007/T009 [CN] T004/T006/T008 [CN]
- US1 [CN] T011/T012 [CN]T017/T018 [CN]
- US2 [CN] T020/T021/T022 [CN]T023/T024 [CN] T025/T026 [CN]
- US3 [CN] T030/T031/T032/T033 [CN]T034/T035[CN]T036/T037[CN]T038/T039 [CN]
- Polish [CN] T041/T042 [CN]

---

## Parallel Example: User Story 2

```text
Task: T020 [US2] Contract assertions for /skills/{skillName}/entrypoints in tests/contracts/test_skill_install_layout_contract.py
Task: T021 [US2] Multi-tool entrypoint integration scenarios in tests/integration/test_skill_install_layout_integration.py
Task: T022 [US2] Placeholder fallback integration scenario in tests/integration/test_skill_install_layout_integration.py

Task: T023 [US2] Implement entrypoint creation flow in scripts/bash/create-new-skill.sh
Task: T024 [US2] Mirror entrypoint creation flow in .specify/scripts/bash/create-new-skill.sh
Task: T025 [US2] Implement tool support profile planner in scripts/python/skills-utils.py
Task: T026 [US2] Mirror tool support profile planner in .specify/scripts/python/skills-utils.py
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. [CN] Phase 1 + Phase 2
2. [CN] Phase 3[CN]US1[CN]
3. [CN] quickstart Scenario 1 [CN] 7
4. [CN]“[CN] + [CN]”[CN]

### Incremental Delivery

1. MVP[CN]US1
2. [CN]US2[CN] + [CN]
3. [CN]US3[CN] + [CN] + [CN]
4. [CN] Polish [CN]

### Parallel Team Strategy

1. [CN] A[CN]`scripts/bash/create-new-skill.sh` [CN]
2. [CN] B[CN]`.specify/scripts/bash/create-new-skill.sh` [CN]
3. [CN] C[CN]`scripts/python/skills-utils.py` [CN]/[CN]
4. [CN] feature [CN] Phase 6 [CN]

---

## Notes

- [CN] `- [ ] T### [P?] [US?] [CN] + File path` [CN]
- [CN] Feature[CN] Feature[CN]Feature 013 [CN]
- [CN] MVP [CN]Phase 1 + Phase 2 + Phase 3
