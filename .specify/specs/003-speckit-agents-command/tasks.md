# Tasks: Speckit Agents Command

**Input**: Design documents from `/storage/project/cloud-native-ai/spec-kit/.specify/specs/003-speckit-agents-command/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/agents-command.openapi.yaml, quickstart.md

**Tests**: No additional TDD/automated testing requirements were received this time; the following focuses on independently verifiable implementation and manual validation tasks.

**Organization**: Tasks are grouped by user story to enable independent implementation and validation.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Align the command skeleton, prompt entry point, and documentation anchors for `/speckit.agents`.

- [X] T001 Align command template metadata and execution entry point in templates/commands/agents.md
- [X] T002 [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T003 [P] [CN] `/speckit.agents` [CN] in docs/usage.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: [CN]

- [X] T004 [CN] agent [CN]kebab-case + `.github/agents/*.agent.md`[CN] in .github/prompts/speckit.agents.prompt.md
- [X] T005 [P] [CN] approved providers [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T006 [P] [CN] least-privilege [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T007 [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T008 [CN] YAML/frontmatter [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T009 [CN]create/update/infer/validate[CN] in .specify/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml

**Checkpoint**: Foundation ready - US1/US2/US3 can start.

---

## Phase 3: User Story 1 - Create Custom AI Agent (Priority: P1) 🎯 MVP

**Goal**: [CN] `.agent.md`[CN]

**Independent Test**: [CN] intent [CN] `.github/agents/` [CN] frontmatter [CN] agent [CN] intent[CN]

### Implementation for User Story 1

- [X] T010 [US1] [CN]“[CN]”[CN] in .github/prompts/speckit.agents.prompt.md
- [X] T011 [US1] [CN]“[CN]”[CN] in .github/prompts/speckit.agents.prompt.md
- [X] T012 [US1] [CN]“[CN] intent”[CN] in .github/prompts/speckit.agents.prompt.md
- [X] T013 [P] [US1] [CN] frontmatter [CN] prompts in templates/commands/agents.md
- [X] T014 [US1] [CN] Create/Infer [CN] in .specify/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml
- [X] T015 [US1] [CN] US1 [CN]/[CN] in .specify/specs/003-speckit-agents-command/quickstart.md
- [X] T016 [US1] [CN] US1 [CN] in .specify/specs/003-speckit-agents-command/quickstart.md

**Checkpoint**: US1 [CN] MVP[CN]

---

## Phase 4: User Story 2 - Update Existing AI Agent (Priority: P2)

**Goal**: [CN] agent [CN]

**Independent Test**: [CN] agent [CN]

### Implementation for User Story 2

- [X] T017 [P] [US2] [CN] agent [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T018 [US2] [CN]“[CN]”[CN] in .github/prompts/speckit.agents.prompt.md
- [X] T019 [US2] [CN]“[CN]”[CN] in .github/prompts/speckit.agents.prompt.md
- [X] T020 [US2] [CN] Update/Overwrite [CN] in .specify/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml
- [X] T021 [US2] [CN]Saved→Updated [CN] in .specify/specs/003-speckit-agents-command/data-model.md
- [X] T022 [US2] [CN] US2 [CN] in .specify/specs/003-speckit-agents-command/quickstart.md

**Checkpoint**: US2 [CN] US3 [CN]

---

## Phase 5: User Story 3 - Validate Agent Quality and Consistency (Priority: P3)

**Goal**: [CN] YAML[CN]provider[CN]tools [CN]

**Independent Test**: [CN] YAML[CN] provider[CN]tools/workflow [CN]

### Implementation for User Story 3

- [X] T023 [P] [US3] [CN] YAML/frontmatter [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T024 [P] [US3] [CN] provider [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T025 [US3] [CN] tools [CN] workflow [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T026 [US3] [CN] tools [CN] in .github/prompts/speckit.agents.prompt.md
- [X] T027 [US3] [CN] Validate [CN] in .specify/specs/003-speckit-agents-command/contracts/agents-command.openapi.yaml
- [X] T028 [US3] [CN] US3 [CN]invalid YAML/provider/tools[CN] in .specify/specs/003-speckit-agents-command/quickstart.md
- [X] T029 [US3] [CN] US3 [CN] in .specify/specs/003-speckit-agents-command/quickstart.md

**Checkpoint**: [CN]

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: [CN]feature [CN]

- [X] T030 [P] [CN] in .specify/specs/003-speckit-agents-command/requirements.md
- [X] T031 [P] [CN] in .specify/memory/features/019.md
- [X] T032 [CN] feature [CN] in .specify/memory/features.md
- [X] T033 [CN]requirements/plan/data-model/contracts/tasks[CN] in .specify/specs/003-speckit-agents-command/

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: [CN]
- **Phase 2 (Foundational)**: [CN] Phase 1[CN]
- **Phase 3/4/5 (US1/US2/US3)**: [CN] Phase 2 [CN] US1[CN]
- **Phase 6 (Polish)**: [CN]

### User Story Dependencies

- **US1 (P1)**: [CN] Foundational[CN] MVP[CN]
- **US2 (P2)**: [CN] Foundational[CN] US1 [CN]“[CN]/[CN]”[CN]
- **US3 (P3)**: [CN] Foundational[CN]“[CN]”[CN]

### Within Each User Story

- [CN] quickstart [CN]

## Parallel Opportunities

- **Setup**: T003 [CN] T001/T002 [CN]
- **Foundational**: T005 [CN] T006 [CN] T007/T008/T009[CN]
- **US1**: T013 [CN] T010/T011/T012 [CN]
- **US2**: T017 [CN] T018/T019/T020[CN]
- **US3**: T023 [CN] T024 [CN] T025/T026/T027[CN]
- **Polish**: T030 [CN] T031 [CN]

## Parallel Example: User Story 1

```bash
Task: "T010 [US1] [CN] in .github/prompts/speckit.agents.prompt.md"
Task: "T013 [P] [US1] [CN] in templates/commands/agents.md"
```

## Implementation Strategy

### MVP First (User Story 1 Only)

1. [CN] Phase 1 [CN] Phase 2[CN]
2. [CN] Phase 3[CN]US1[CN]
3. [CN] quickstart [CN] US1 [CN]

### Incremental Delivery

1. [CN] US1[CN] MVP[CN]
2. [CN] US2[CN]
3. [CN] US3[CN]
4. [CN] Phase 6 [CN]

### Team Parallel Strategy

1. [CN] Phase 1/2 [CN]
2. [CN]A [CN] US1[CN]B [CN] US2[CN]C [CN] US3[CN]
3. [CN] Phase 6 [CN] feature [CN]

## Notes

- [CN] `- [ ] Txxx [P] [USx] [CN] + File path` [CN]
- `[P]` [CN]
- [CN]
