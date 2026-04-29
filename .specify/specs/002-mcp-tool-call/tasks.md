---

description: "Task list for MCP Tool Call Command"
---

# Tasks: MCP Tool Call Command

> Archived Note: This task list corresponds to the historical MCP-only phase. The current unified entry point is `/speckit.tools`.

**Input**: Design documents from `.specify/specs/002-mcp-tool-call/`
**Prerequisites**: plan.md, requirements.md, data-model.md, contracts/, quickstart.md

**Tests**: Test tasks are included per constitution requirements (write tests first, confirm failure, then implement).

## Format: `[ID] [P?] [Story] Description`

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project structure and basic template preparation

- [x] T001 [CN] `src/specify_cli/commands/__init__.py`
- [x] T002 [P] [CN] `templates/` [CN] `templates/commands/` [CN]
- [x] T003 [P] [CN]/[CN] `src/specify_cli/__init__.py` [CN]

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: [CN]

- [x] T004 [CN] `templates/commands/tools.md` [CN] MCP [CN]/[CN]
- [x] T005 [P] [CN] `templates/commands/tools.md` [CN] schema [CN] `contracts/mcptool-record.schema.json`[CN]
- [x] T006 [P] [CN] `templates/commands/tools.md` [CN] schema[CN]
- [x] T007 [CN] `templates/commands/tools.md` [CN] MCP [CN] refresh-tools.sh [CN] MCP [CN]
- [x] T008 [P] [CN] `templates/commands/tools.md` [CN]server/description/params/returns[CN]
- [x] T009 [CN] `templates/commands/tools.md` [CN]

**Checkpoint**: [CN]

---

## Phase 3: User Story 1 - [CN] MCP [CN] (Priority: P1) 🎯 MVP

**Goal**: [CN]

**Independent Test**: [CN] quickstart [CN] 1 [CN]

### Tests for User Story 1 (MANDATORY)

- [x] T010 [P] [US1] [CN] `templates/commands/tools.md` [CN] MCP [CN] schema [CN]
- [x] T011 [P] [US1] [CN] `templates/commands/tools.md` [CN] schema [CN]
- [x] T012 [P] [US1] [CN] `templates/commands/tools.md` [CN] + [CN] + [CN]

### Manual Verification for User Story 1

- [ ] T013 [US1] [CN] `quickstart.md` [CN] 1 [CN] `.specify/specs/002-mcp-tool-call/quickstart.md`

### Implementation for User Story 1

- [x] T014 [US1] [CN]/[CN] MCP [CN] `.specify/memory/tools/<mcp tool name>.md`
- [x] T015 [US1] [CN] MCP [CN] `/speckit.tools` [CN]
- [x] T016 [US1] [CN] `/speckit.tools` [CN]
- [x] T017 [US1] [CN] `/speckit.tools` [CN]

**Checkpoint**: US1 [CN]

---

## Phase 4: User Story 2 - [CN] (Priority: P2)

**Goal**: [CN]

**Independent Test**: [CN] quickstart [CN] 2 [CN]

### Tests for User Story 2 (MANDATORY)

- [x] T018 [P] [US2] [CN] `templates/commands/tools.md` [CN]
- [x] T019 [P] [US2] [CN] `templates/commands/tools.md` [CN]

### Manual Verification for User Story 2

- [ ] T020 [US2] [CN] `quickstart.md` [CN] 2 [CN] 3 [CN] `.specify/specs/002-mcp-tool-call/quickstart.md`

### Implementation for User Story 2

- [x] T021 [US2] [CN] `templates/commands/tools.md` [CN]
- [x] T022 [US2] [CN] `templates/commands/tools.md` [CN]

**Checkpoint**: US2 [CN]

---

## Phase 5: Polish & Cross-Cutting Concerns

**Purpose**: [CN]

- [x] T023 [P] [CN] `templates/commands/tools.md` [CN]
- [x] T024 [P] [CN] MCP [CN] `templates/mcptool-template.md`[CN]
- [ ] T025 [P] [CN] feature [CN] ` .specify/specs/002-mcp-tool-call/feature-ref.md`
- [ ] T026 [CN] quickstart [CN] `.specify/specs/002-mcp-tool-call/quickstart.md`

---

## Dependencies & Execution Order

- Setup (Phase 1) → Foundational (Phase 2) → US1 → US2 → Polish
- US1 [CN] US2 [CN] Foundational [CN]

## Parallel Opportunities

- Phase 1 [CN] T002/T003 [CN]
- Phase 2 [CN] T005/T006/T008 [CN]
- US1 [CN] T010/T011 [CN]
- US2 [CN] T018/T019 [CN]

## Implementation Strategy

- MVP[CN] Phase 1 + Phase 2 + US1
- [CN] US1 [CN] US2[CN] Polish
