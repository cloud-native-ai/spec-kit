<!--
  Feature: Add Instructions and Skills Commands
  Branch: 1000-add-instr-skills-cmds
  Spec: .specify/specs/1000-add-instr-skills-cmds/spec.md
  Plan: .specify/specs/1000-add-instr-skills-cmds/plan.md
-->

# Tasks: Add Instructions and Skills Commands

**Feature Branch**: `1000-add-instr-skills-cmds`
**Status**: Planned

## Implementation Strategy

- **Phase 1: Setup**: Verify task environment.
- **Phase 2: Foundation**: Not applicable (No shared code changes).
- **Phase 3: User Story 1 (Instructions Command)**: Implement `.ai/instructions.md` generator.
- **Phase 4: User Story 2 (Skills Command)**: Implement `.github/skills/` generator.
- **Phase 5: Polish**: Verification and manual tests.

## Dependencies

- **US1 & US2** are independent.
- **Polish** depends on US1 & US2.

## Parallel Execution Examples
- **US1** and **US2** can be implemented in parallel as they touch different template files.

---

## Phase 1: Setup

- [x] T001 Verify `templates/commands/` directory exists for `specify-cli`.

## Phase 2: Foundational

*No foundational tasks required.*

## Phase 3: User Story 1 - Generate Project Instructions

**Goal**: Enable `/speckit.instructions` command.
**Independent Test**: Run `specify init . --ai copilot` then trigger `/speckit.instructions` in chat.

- [x] T002 [US1] Create template file `templates/commands/instructions.md` with implementation details from plan.

## Phase 4: User Story 2 - Generate Skill Scaffold

**Goal**: Enable `/speckit.skills` command.
**Independent Test**: Trigger `/speckit.skills` in chat.

- [x] T003 [P] [US2] Create template file `templates/commands/skills.md` with implementation details from plan.

## Phase 5: Polish & Cross-Cutting

- [x] T004 Manual verification: Create a temporary test directory, init specify, and verify both commands generate expected files.
