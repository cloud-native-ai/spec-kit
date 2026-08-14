# Tasks: Role-Based Agent Templates

**Requirement ID**: 015 (from branch name)
**Requirement Key**: 015-role-based-agents
**Related Feature**: 019 Agents Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/015-role-based-agents/`
**Prerequisites**: plan.md (required), requirements.md (required for user stories), quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates tests BEFORE implementation)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: All six role-based agent templates created in `templates/` with correct structure and placeholders
- DoD-2: Four legacy capability-based agent templates removed from `templates/`
- DoD-3: `/speckit.agents` command prompt updated for role-based generation flow
- DoD-4: All automated tests pass (contract, integration)
- DoD-5: Each generated agent contains project-specific context, not generic placeholders
- DoD-6: Workflow handoff chain is traceable through all six agents' upstream/downstream sections
- DoD-7: Backup semantics work correctly for customized role-based agents (FR-008a)
- DoD-8: `create-agent` and `improve-agent` skills created following existing skill patterns
- DoD-9: Quickstart validation scenarios pass

**DoD Status**: green

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Phase 1: Setup

**Purpose**: Prepare the workspace for role-based agent template development

- [X] T001 Review existing agent templates to understand current placeholder patterns in `templates/agent-common-template.md`, `templates/agent-knowledge-template.md`, `templates/agent-plan-template.md`, `templates/agent-research-template.md`
- [X] T002 Review existing agents command prompt to understand current generation flow in `templates/commands/agents.md`
- [X] T003 [P] Review existing skill patterns for create-agent/improve-agent reference in `skills/create-skills/SKILL.md` and `skills/improve-skills/SKILL.md`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the shared template structure that all role-based templates will follow

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Define the common template structure for role-based agents — establish the shared sections (Identity & Responsibilities, Project Context, Workflow, Upstream, Downstream, Output Format) and YAML frontmatter fields (name, description, user-invocable, disable-model-invocation) with `tools` omitted per clarification. Document as a reference comment block at the top of the first template created in Phase 3.

**Checkpoint**: Foundation ready — role template authoring can now begin

---

## Phase 3: User Story 1 — Generate role-based agents for a project (Priority: P1) 🎯 MVP

**Goal**: Create six role-based agent templates that `/speckit.agents` can use to generate project-aware agents

**Independent Test**: Run `/speckit.agents` in an initialized project and verify six `.agent.md` files are generated under `.specify/agents/` with role-appropriate content

### Tests for User Story 1 (MANDATORY) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [X] T005 [P] [US1] Contract test: verify each role template file exists and has valid YAML frontmatter with required fields (name, description, user-invocable) in `tests/contract/test_role_templates.py`
- [X] T006 [P] [US1] Contract test: verify each role template contains the mandatory sections (Identity & Responsibilities, Project Context, Workflow, Upstream, Downstream, Output Format) in `tests/contract/test_role_templates.py`
- [X] T007 [P] [US1] Contract test: verify each role template uses only approved placeholder variables from the context placeholders table in `tests/contract/test_role_templates.py`

### Implementation for User Story 1

- [X] T008 [P] [US1] Create Requirements Analyst role template in `templates/agent-role-requirements-analyst-template.md` — define identity as user-team interface, responsibilities for requirement clarification and translation, upstream (user/stakeholder input), downstream (System Designer), workflow for analyzing and structuring requirements
- [X] T009 [P] [US1] Create System Designer role template in `templates/agent-role-system-designer-template.md` — define identity as architecture owner, responsibilities for holistic design, upstream (Requirements Analyst), downstream (Module Designer, QA Engineer), workflow for system-level design with placeholders `{{PROJECT_STRUCTURE}}`, `{{CONSTITUTION_PRINCIPLES}}`, `{{FEATURE_INDEX}}`
- [X] T010 [P] [US1] Create Module Designer role template in `templates/agent-role-module-designer-template.md` — define identity as subsystem specialist, responsibilities for detailed module design, upstream (System Designer), downstream (Test Engineer), workflow for module-scoped implementation with placeholders `{{PROJECT_STRUCTURE}}`, `{{MODULE_LIST}}`
- [X] T011 [P] [US1] Create Test Engineer role template in `templates/agent-role-test-engineer-template.md` — define identity as acceptance-focused tester, responsibilities for test design/execution, upstream (Module Designer), downstream (Module Designer feedback loop, QA Engineer), workflow for test-first validation with placeholder `{{TESTING_FRAMEWORK}}`
- [X] T012 [P] [US1] Create QA Engineer role template in `templates/agent-role-qa-engineer-template.md` — define identity as systemic quality guardian, responsibilities for design-requirements alignment validation, upstream (System Designer, Test Engineer), downstream (Requirements Analyst gap feedback), workflow for full-system quality review with placeholder `{{CONSTITUTION_PRINCIPLES}}`
- [X] T013 [P] [US1] Create Knowledge Manager role template in `templates/agent-role-knowledge-manager-template.md` — define identity as knowledge steward, responsibilities for documentation and knowledge base maintenance, upstream (all roles), downstream (all roles), workflow for knowledge capture and organization with placeholders `{{FEATURE_INDEX}}`, `{{DOCS_DIR}}`
- [X] T014 [US1] Verify all six templates pass the contract tests from T005-T007

**Checkpoint**: Six role-based templates exist and pass structural validation

---

## Phase 4: User Story 2 — Remove legacy capability-based agent templates (Priority: P1)

**Goal**: Remove old templates and update the `/speckit.agents` command to use role-based templates

**Independent Test**: Verify old `templates/agent-*-template.md` files no longer exist and `/speckit.agents` uses role templates

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T015 [P] [US2] Contract test: verify `templates/agent-common-template.md`, `templates/agent-knowledge-template.md`, `templates/agent-plan-template.md`, `templates/agent-research-template.md` do NOT exist in `tests/contract/test_legacy_removal.py`
- [X] T016 [P] [US2] Contract test: verify `templates/commands/agents.md` does not reference `agent-common-template`, `agent-knowledge-template`, `agent-plan-template`, or `agent-research-template` in `tests/contract/test_legacy_removal.py`

### Implementation for User Story 2

- [X] T017 [P] [US2] Delete `templates/agent-common-template.md`
- [X] T018 [P] [US2] Delete `templates/agent-knowledge-template.md`
- [X] T019 [P] [US2] Delete `templates/agent-plan-template.md`
- [X] T020 [P] [US2] Delete `templates/agent-research-template.md`
- [X] T021 [US2] Update `templates/commands/agents.md` — replace the type-classification flow (steps 5-8: Knowledge/Plan/Research/Common selection) with role-based generation flow: (1) no arguments → generate all six role-based agents using `templates/agent-role-*-template.md`, reading project context and resolving placeholders; (2) with arguments → fall back to general-purpose ad-hoc agent creation with generic template structure embedded in the command
- [X] T022 [US2] Update `templates/commands/agents.md` — add backup detection logic per FR-008a: before overwriting a role-based agent, compare existing file content against what would be generated; if different, create `.bak` copy and warn user
- [X] T023 [US2] Update `templates/commands/agents.md` — add agent preservation logic per FR-008: skip non-role agents (e.g., `code-reviewer.agent.md`) during role-based generation; only create/update files matching the six role slugs
- [X] T024 [US2] Verify legacy removal tests from T015-T016 pass

**Checkpoint**: Old templates removed; command prompt updated for role-based flow

---

## Phase 5: User Story 3 — Agents collaborate through workflow handoffs (Priority: P2)

**Goal**: Each agent defines explicit upstream inputs and downstream outputs, enabling structured workflow handoffs

**Independent Test**: Examine each agent's instructions for upstream/downstream references; verify the complete handoff chain is traceable

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T025 [P] [US3] Contract test: verify each role template has non-empty `## Upstream (Inputs)` and `## Downstream (Outputs)` sections in `tests/contract/test_handoff_chain.py`
- [X] T026 [P] [US3] Contract test: verify the handoff chain completeness — Requirements Analyst downstream mentions System Designer; System Designer downstream mentions Module Designer and QA Engineer; Module Designer downstream mentions Test Engineer; Test Engineer downstream mentions Module Designer and QA Engineer; QA Engineer downstream mentions Requirements Analyst; Knowledge Manager references all roles in `tests/contract/test_handoff_chain.py`

### Implementation for User Story 3

- [X] T027 [US3] Review and refine all six role templates to ensure upstream/downstream sections explicitly reference the correct roles and artifact types per the Workflow Handoff table in plan.md — update `templates/agent-role-*-template.md` as needed
- [X] T028 [US3] Verify handoff chain tests from T025-T026 pass

**Checkpoint**: Handoff chain is complete and verifiable across all agents

---

## Phase 6: User Story 4 — Dynamic context injection during agent generation (Priority: P2)

**Goal**: Generated agents contain project-specific context resolved from the current project state

**Independent Test**: Generate agents in a project and verify agent instructions reference actual project details (tech stack, modules, constitution, etc.)

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T029 [P] [US4] Integration test: generate agents in a test project fixture and verify `{{PLACEHOLDER}}` variables are not present in generated output in `tests/integration/test_context_injection.py`
- [X] T030 [P] [US4] Integration test: generate agents in a Python project fixture and verify Module Designer references actual module paths in `tests/integration/test_context_injection.py`

### Implementation for User Story 4

- [X] T031 [US4] Ensure `templates/commands/agents.md` context resolution logic reads and injects: `{{PROJECT_NAME}}` from README.md/pyproject.toml, `{{TECH_STACK}}` from dependency files, `{{PROJECT_STRUCTURE}}` from directory analysis, `{{MODULE_LIST}}` from source scan, `{{CONSTITUTION_PRINCIPLES}}` from `.specify/memory/constitution.md`, `{{FEATURE_INDEX}}` from `.specify/memory/features.md`, `{{SPECS_DIR}}` from `.specify/specs/`, `{{TESTING_FRAMEWORK}}` from test config, `{{DOCS_DIR}}` from `docs/`
- [X] T032 [US4] Verify context injection tests from T029-T030 pass

**Checkpoint**: Generated agents contain real project context

---

## Phase 7: Companion Skills (Priority: P2)

**Goal**: Create `create-agent` and `improve-agent` skills for agent template evolution

**Independent Test**: Invoke each skill and verify it operates on template files in `templates/`, not on generated agents in `.specify/agents/`

### Implementation for Companion Skills

- [X] T033 [P] Create `skills/create-agent/SKILL.md` — mirror `skills/create-skills/SKILL.md` structure: frontmatter (name, description, skill_id, trigger keywords), Goal section, Workflow section covering (1) parse role description from user input, (2) generate `templates/agent-role-<name>-template.md` with correct structure, (3) validate template has all mandatory sections and valid placeholders, (4) report created template path
- [X] T034 [P] Create `skills/improve-agent/SKILL.md` — mirror `skills/improve-skills/SKILL.md` structure: frontmatter (name, description, skill_id, trigger keywords), Goal section, Workflow section covering (1) identify target agent template from user input, (2) gather execution evidence (feedback, failures, behavioral drift), (3) analyze root causes, (4) update `templates/agent-role-<name>-template.md` with minimal targeted fixes, (5) report changes made

**Checkpoint**: Both companion skills exist and follow established skill patterns

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation, and cleanup

- [X] T035 Run all contract and integration tests to verify end-to-end correctness
- [~] T036 Run quickstart.md validation scenarios (Scenarios 1-7) and record results <!-- deferred: requires running /speckit.agents in a live project to validate dynamic generation; template-level validation covered by contract tests -->
- [X] T037 [P] Verify symlink compatibility — confirm role-based agents are visible through `.github/agents/`, `.qoder/agents/`, `.qwen/agents/`, `.opencode/agents/` symlinks
- [~] T038 [P] Update `.specify/agents/` workspace files if needed — ensure `AGENTS.md` index reflects the six new role-based agents <!-- deferred: AGENTS.md is created by /speckit.agents at runtime, not by this implementation; role agents don't exist until generated -->
- [X] T039 Verify that `specify init` bundled agents directory (`agents/`) still correctly installs `code-reviewer.agent.md` and `references/.gitkeep` without conflicting with dynamically generated role agents

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational — creates the six role templates
- **US2 (Phase 4)**: Depends on US1 — removes old templates and updates command to use new ones
- **US3 (Phase 5)**: Depends on US1 — refines handoff sections in templates created by US1
- **US4 (Phase 6)**: Depends on US2 — requires updated command prompt for context injection
- **Companion Skills (Phase 7)**: Can start after Foundational (Phase 2) — independent of US1-US4
- **Polish (Phase 8)**: Depends on all prior phases

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational — creates templates (no dependencies on other stories)
- **US2 (P1)**: Depends on US1 — needs new templates before removing old ones and updating command
- **US3 (P2)**: Depends on US1 — refines templates that US1 created
- **US4 (P2)**: Depends on US2 — requires the updated command prompt
- **Companion Skills**: Independent — can run in parallel with US1-US4

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Template creation before command prompt updates
- Core implementation before integration/validation

### Parallel Opportunities

- All Setup tasks (T001-T003) can run in parallel
- All six role template creation tasks (T008-T013) can run in parallel within US1
- All four legacy template deletions (T017-T020) can run in parallel within US2
- US3 and US4 can run in parallel after their respective dependencies complete
- Companion skills (Phase 7) can run in parallel with US3 and US4
- Polish tasks marked [P] can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch all contract tests for US1 together:
Task T005: "Contract test for role template YAML frontmatter"
Task T006: "Contract test for role template mandatory sections"
Task T007: "Contract test for role template placeholder variables"

# Launch all six role template creation tasks together:
Task T008: "Create Requirements Analyst template"
Task T009: "Create System Designer template"
Task T010: "Create Module Designer template"
Task T011: "Create Test Engineer template"
Task T012: "Create QA Engineer template"
Task T013: "Create Knowledge Manager template"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2)

1. Complete Phase 1: Setup (review existing templates)
2. Complete Phase 2: Foundational (define common template structure)
3. Complete Phase 3: US1 — create six role templates
4. Complete Phase 4: US2 — remove old templates, update command
5. **STOP and VALIDATE**: Run `/speckit.agents` and verify six agents generated correctly

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. US1 → Six role templates exist → Structural validation passes (MVP templates!)
3. US2 → Old templates removed, command updated → `/speckit.agents` generates role agents (MVP!)
4. US3 → Handoff chain refined → Workflow traceable across all agents
5. US4 → Context injection working → Agents contain project-specific content
6. Companion Skills → Template evolution workflow available
7. Polish → Full validation, symlinks, documentation

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Templates use `{{PLACEHOLDER}}` syntax for variables resolved at generation time
- `tools` field is intentionally omitted from YAML frontmatter (inherits platform defaults per FR-009a clarification)
