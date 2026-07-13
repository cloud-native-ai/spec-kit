---
description: "Task list for Agent Skill Enablement"
---

# Tasks: Agent Skill Enablement

**Requirement ID**: 025
**Requirement Key**: 025-agent-skill-enablement
**Related Feature**: 026 Agent Skill Enablement (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/025-agent-skill-enablement/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/agent-skill-enablement-contract.md, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is MUST/Contract-Driven; contract C-5 requires `tests/contract/test_agent_skill_enablement.py` to fail before edits and pass after)

**Tests**: Test tasks below are MANDATORY and must be authored and observed FAILING before the corresponding implementation.

**Organization**: Tasks are grouped by user story (US1 P1, US2 P2, US3 P3) to enable independent implementation and testing.

## Definition of Done (DoD)

- DoD-1: All 7 built-in role agents declare a `skills:` frontmatter list of ≥1 role-relevant installed skill (SC-001).
- DoD-2: All 7 agents contain one `## Skill Enablement` section composing the single-source shared protocol + per-role skill table (SC-003, SC-005).
- DoD-3: Union of declared skills is a subset of installed declarable skills with 0 dangling references and 0 non-declarable slugs (SC-002).
- DoD-4: `pytest -m contract tests/contract/test_agent_skill_enablement.py` is green; `test_shipped_agent_presets.py` remains green (no regression, SC-004).
- DoD-5: The 7 `create-agent` role templates mirror the same additions (C-3 parity; FR-011 regeneration safety).
- DoD-6: Docs (`docs/agents/command-and-skills.md`, `docs/agents/design.md`) document the skill-enablement convention; quickstart Scenarios 1–5 pass.

**DoD Status**: green

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Include exact file paths in descriptions

### Task State Sigil (REQUIRED)

- `- [ ]` — **Open**. Not yet completed.
- `- [X]` — **Closed**. Fully executed and verified.
- `- [~]` — **Deferred**. Intentionally handed off; record reason in `verification.md`.

## Path Conventions

- Shipped agents: `agents/<slug>.agent.md` (mirrored to `.specify/agents/` on install)
- Generator templates: `skills/create-agent/templates/agent-role-<role>-template.md`
- Shared snippet: `skills/create-agent/templates/agent-skill-enablement.md`
- Installed skills reference set: `skills/<slug>/SKILL.md` (mirrored to `.specify/skills/<slug>/SKILL.md`)
- Contract test: `tests/contract/test_agent_skill_enablement.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the reference facts the change depends on.

- [X] T001 Confirm the installed declarable skill inventory under `skills/` and reconcile it against the Agent–Skill Mapping in `.specify/specs/025-agent-skill-enablement/data-model.md`; confirm the non-declarable set (`sdd-workflow`, `create-agent`, `improve-agent`, `create-skills`, `improve-skills`, `organize-agents`) is excluded from every mapped row.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Create the single source of truth for the skill-preference protocol that both agents and generator templates compose.

**⚠️ CRITICAL**: Blocks all user stories — every agent and template edit composes this snippet.

- [X] T002 Create the shared single-source protocol snippet `skills/create-agent/templates/agent-skill-enablement.md` (composed like `agent-supervision-delegation.md`) containing the 5-point protocol from contract C-2 / data-model.md §Skill-Usage Guidance: (1) skills install with agents so every declared skill is invocable; (2) prefer an applicable framework skill over manual/ad-hoc work; (3) when multiple apply, choose the most role-specific; (4) when none applies or a skill is unavailable/fails, complete directly and surface the failure; (5) invoke the skill rather than reimplementing its logic inline.

**Checkpoint**: Shared protocol snippet exists — agent and template edits can begin.

---

## Phase 3: User Story 1 - Agents prefer role-relevant skills (Priority: P1) 🎯 MVP

**Goal**: Each of the 7 built-in role agents declares its role-relevant skills and includes guidance to prefer those skills over improvising the same operation.

**Independent Test**: Give an agent a task covered by its declared skill (e.g. System Designer → architecture diagram) and confirm it routes through the skill; confirm each agent definition states which skills it uses and when.

### Tests for User Story 1 (MANDATORY) ⚠️

> Write FIRST, ensure they FAIL before implementation.

- [X] T003 [US1] Author `tests/contract/test_agent_skill_enablement.py` (pytest marker `contract`) implementing contract C-5 assertions T-1 (frontmatter contains `skills:`), T-2 (parsed `skills` list is non-empty), and T-5 (agent body contains a `## Skill Enablement` heading) for all 7 preset agents under `agents/`; run `pytest -m contract tests/contract/test_agent_skill_enablement.py` and confirm it FAILS.

### Implementation for User Story 1

- [X] T004 [P] [US1] Edit `agents/requirements-analyst.agent.md`: add `skills: [draw-plantuml, memory-recall, memory-record, think-skills]` frontmatter (preserving all existing keys) and a `## Skill Enablement` section composing `agent-skill-enablement.md` + a `| Skill | When to use |` table (UML use-case diagrams; recall prior requirements/decisions; record clarifications; simulate requirement logic).
- [X] T005 [P] [US1] Edit `agents/system-designer.agent.md`: add `skills: [draw-plantuml, analysis-project, memory-recall, memory-record, think-skills]` + `## Skill Enablement` section with per-role table (architecture/component/sequence diagrams; analyze existing architecture; recall design decisions; record rationale; simulate designs).
- [X] T006 [P] [US1] Edit `agents/module-designer.agent.md`: add `skills: [analysis-project, git-workflow, git-submodule-edit, memory-record, think-skills]` + `## Skill Enablement` section (analyze project structure; branch sync; submodule edits; record module decisions; simulate change logic).
- [X] T007 [P] [US1] Edit `agents/test-engineer.agent.md`: add `skills: [browser-utils, extension-e2e-test, database-utils, think-skills]` + `## Skill Enablement` section (web E2E; browser-extension E2E; DB-backed verification; simulate test scenarios).
- [X] T008 [P] [US1] Edit `agents/qa-engineer.agent.md`: add `skills: [analysis-project, browser-utils, database-utils, memory-recall]` + `## Skill Enablement` section (architecture/constitution compliance analysis; end-to-end web checks; data validation; recall requirements/acceptance criteria).
- [X] T009 [P] [US1] Edit `agents/knowledge-manager.agent.md`: add `skills: [document-utils, memory-record, memory-recall, draw-plantuml, draw-d3js, draw-echarts]` + `## Skill Enablement` section (produce/edit office docs; record & recall knowledge; diagrams and data visualizations).
- [X] T010 [P] [US1] Edit `agents/ux-analyst.agent.md`: add `skills: [browser-utils, document-utils, draw-echarts, draw-d3js, extension-e2e-test]` + `## Skill Enablement` section (UI/UX inspection & screenshots; UX reports; UX data visualization; extension UI testing).
- [X] T011 [US1] Run `pytest -m contract tests/contract/test_agent_skill_enablement.py` and confirm T-1, T-2, T-5 now PASS for all 7 agents.

### Manual Verification for User Story 1

- [X] T011A [US1] Manual QA: follow quickstart.md Scenario 1 (each agent declares role-relevant skills, consistent format) and Scenario 2 (agent prefers the declared skill for a covered operation).

**Checkpoint**: All 7 agents declare role-relevant skills and prefer them — MVP functional.

---

## Phase 4: User Story 2 - Declared skills are guaranteed to be invocable (Priority: P2)

**Goal**: Every skill referenced by any built-in agent resolves to an installed skill; no dangling references and no non-declarable slugs.

**Independent Test**: Cross-check the union of every skill named across all 7 agents against the installed skill set; the referenced set MUST be a subset with zero dangling references.

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T012 [US2] Extend `tests/contract/test_agent_skill_enablement.py` with contract C-5 assertions T-3 (every declared slug resolves to an existing `skills/<slug>/SKILL.md`, i.e. installed under `.specify/skills/<slug>/`) and T-4 (no declared slug is a member of the non-declarable set: `sdd-workflow`, `create-agent`, `improve-agent`, `create-skills`, `improve-skills`, `organize-agents`), asserted over the union across all 7 agents.

### Implementation for User Story 2

- [X] T013 [US2] Run `pytest -m contract tests/contract/test_agent_skill_enablement.py` and confirm 0 dangling references and 0 non-declarable declarations (SC-002); record the union of declared skills verified as a subset of installed declarable skills.

**Checkpoint**: Skill references are provably invocable with zero drift.

---

## Phase 5: User Story 3 - Consistent, discoverable skill-usage guidance (Priority: P3)

**Goal**: All built-in agents express skill usage in the same format/location, and the `create-agent` generator templates mirror the same additions so regenerated agents inherit the behavior.

**Independent Test**: Compare any two agents' skill declarations (identical format/location, shared protocol text, only the table differs); confirm regenerating an agent from its template yields the same structure.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T014 [US3] Add a template-parity assertion (contract C-3) to `tests/contract/test_agent_skill_enablement.py`: each `skills/create-agent/templates/agent-role-<role>-template.md` MUST declare a `skills:` frontmatter list and contain a `## Skill Enablement` heading. Run and confirm it FAILS before the template edits.

### Implementation for User Story 3

- [X] T015 [P] [US3] Edit `skills/create-agent/templates/agent-role-requirements-analyst-template.md`: mirror the `skills:` frontmatter and `## Skill Enablement` section from `agents/requirements-analyst.agent.md`.
- [X] T016 [P] [US3] Edit `skills/create-agent/templates/agent-role-system-designer-template.md`: mirror the additions from `agents/system-designer.agent.md`.
- [X] T017 [P] [US3] Edit `skills/create-agent/templates/agent-role-module-designer-template.md`: mirror the additions from `agents/module-designer.agent.md`.
- [X] T018 [P] [US3] Edit `skills/create-agent/templates/agent-role-test-engineer-template.md`: mirror the additions from `agents/test-engineer.agent.md`.
- [X] T019 [P] [US3] Edit `skills/create-agent/templates/agent-role-qa-engineer-template.md`: mirror the additions from `agents/qa-engineer.agent.md`.
- [X] T020 [P] [US3] Edit `skills/create-agent/templates/agent-role-knowledge-manager-template.md`: mirror the additions from `agents/knowledge-manager.agent.md`.
- [X] T021 [P] [US3] Edit `skills/create-agent/templates/agent-role-ux-analyst-template.md`: mirror the additions from `agents/ux-analyst.agent.md`.
- [X] T022 [US3] Run `pytest -m contract tests/contract/test_agent_skill_enablement.py` and confirm the template-parity assertion (T014) now PASSES.
- [X] T023 [P] [US3] Update `docs/agents/command-and-skills.md` to document the `skills:` frontmatter field and the `## Skill Enablement` section convention (single-source protocol + per-role table).
- [X] T024 [P] [US3] Update `docs/agents/design.md` to reference the skill-enablement convention and its single-source snippet.
- [X] T025 [US3] Verify uniformity (quickstart Scenario 1 uniformity check, SC-005): confirm all 7 agents share identical protocol text and section location, differing only in the skill table.

**Checkpoint**: Skill guidance is uniform, discoverable, and regeneration-safe.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T026 [P] Run the full contract suite: `pytest -m contract tests/contract/test_shipped_agent_presets.py tests/contract/test_agent_skill_enablement.py -q` — confirm no regression to existing frontmatter fields (SC-004) and the new test is green.
- [X] T027 Run full quickstart.md validation (Scenarios 1–5), including Scenario 3 graceful-fallback and Scenario 5 no-regression checks.
- [X] T028 Update `.specify/memory/features/026.md` implementation notes with the final Agent–Skill mapping and test coverage summary (status remains `Planned` until `/speckit.implement` completes).

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2)**: Depends on Setup; the shared snippet (T002) BLOCKS all agent/template edits.
- **User Stories (Phase 3–5)**: All depend on Foundational (T002).
  - US1 (P1) is the MVP and should complete first.
  - US2 (P2) depends on US1 agent edits existing (so the subset check has content to validate).
  - US3 (P3) template edits depend on the corresponding US1 agent edits (each template mirrors its shipped agent).
- **Polish (Phase 6)**: Depends on all desired user stories being complete.

### User Story Dependencies

- **US1 (P1)**: Independent — delivers the core value on its own.
- **US2 (P2)**: Validation layer over US1's declarations; independently testable via the subset cross-check.
- **US3 (P3)**: Consistency + regeneration parity; mirrors US1 into templates and documents the convention.

### Within Each Story

- Tests authored and observed FAILING before implementation (Principle IV).
- Foundational snippet before any agent/template composition.
- Agent edits (US1) before template mirrors (US3).

### Parallel Opportunities

- US1 agent edits T004–T010 are all different files → run in parallel.
- US3 template edits T015–T021 are all different files → run in parallel.
- US3 doc updates T023, T024 are different files → run in parallel.
- Polish T026 is independent of doc tasks.

---

## Parallel Example: User Story 1

```bash
# After T002 (shared snippet) and T003 (failing test), edit all 7 agents in parallel:
Task: "Edit agents/requirements-analyst.agent.md — skills frontmatter + Skill Enablement section"
Task: "Edit agents/system-designer.agent.md — skills frontmatter + Skill Enablement section"
Task: "Edit agents/module-designer.agent.md — skills frontmatter + Skill Enablement section"
Task: "Edit agents/test-engineer.agent.md — skills frontmatter + Skill Enablement section"
Task: "Edit agents/qa-engineer.agent.md — skills frontmatter + Skill Enablement section"
Task: "Edit agents/knowledge-manager.agent.md — skills frontmatter + Skill Enablement section"
Task: "Edit agents/ux-analyst.agent.md — skills frontmatter + Skill Enablement section"
```

## Parallel Example: User Story 3

```bash
# Mirror the same additions into all 7 role templates in parallel:
Task: "Edit skills/create-agent/templates/agent-role-requirements-analyst-template.md"
Task: "Edit skills/create-agent/templates/agent-role-system-designer-template.md"
Task: "Edit skills/create-agent/templates/agent-role-module-designer-template.md"
Task: "Edit skills/create-agent/templates/agent-role-test-engineer-template.md"
Task: "Edit skills/create-agent/templates/agent-role-qa-engineer-template.md"
Task: "Edit skills/create-agent/templates/agent-role-knowledge-manager-template.md"
Task: "Edit skills/create-agent/templates/agent-role-ux-analyst-template.md"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001).
2. Complete Phase 2: Foundational (T002 shared snippet — CRITICAL).
3. Complete Phase 3: US1 (author failing contract test, edit 7 agents, confirm green).
4. **STOP and VALIDATE**: Run T011 + T011A — agents now prefer role-relevant skills.
5. Ship MVP.

### Incremental Delivery

1. Setup + Foundational → protocol snippet ready.
2. US1 → 7 agents skill-enabled → validate (MVP!).
3. US2 → prove zero dangling references → validate.
4. US3 → template parity + docs → validate uniformity.
5. Polish → full suite + quickstart + feature notes.

---

## Notes

- [P] tasks = different files, no dependencies.
- This is a documentation/template change — no `src/specify_cli/` runtime code changes (contract Non-Goals).
- Preserve all existing agent frontmatter keys byte-for-byte when adding `skills:` (FR-011, C-1).
- Non-declarable skills MUST NOT appear in any agent list (C-4).
- Prefer `[~]` (deferred, with recorded reason) over leaving a task `[ ]`.
