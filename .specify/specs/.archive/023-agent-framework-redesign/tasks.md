---
description: "Task list for Agent Framework Redesign"
---

# Tasks: Agent Framework Redesign

**Requirement ID**: 023
**Requirement Key**: 023-agent-framework-redesign
**Related Feature**: 019 Agents Command
**Input**: Design documents from `.specify/specs/023-agent-framework-redesign/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/, quickstart.md

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is MUST/NON-NEGOTIABLE; Layer-1 pytest unit/contract/integration + Layer-2 structural Markdown scenario validation `tests/scenarios/` + a deprecated-term / reference-integrity guard are required)

**Organization**: Tasks are grouped by user story (US1–US5) to enable independent implementation and testing.

## Definition of Done (DoD)

- DoD-1: Code/docs implemented according to requirements.md, plan.md, data-model.md, and contracts/
- DoD-2: Spec-023 automated tests pass — deprecated-term + reference-integrity + persistent-agent guards green (10/10) and Layer-2 scenarios consistent, with 0 new regressions vs baseline HEAD. (106 pre-existing failures belong to other Features — 016 Tools, 020/021/022 support/tier, and a stale top-level `templates/` path in `test_context_injection.py` — documented as out-of-scope in verification.md.)
- DoD-3: Layer-2 structural validation passes — the three `tests/scenarios/multi-agent-orchestration/*` scenarios and the quickstart.md walkthrough
- DoD-4: 0 live references to "SubRole"/"Subrole", "improver", and "Meta-Coordinator" (as a separate role) outside immutable history (SC-002, SC-009)
- DoD-5: Source templates and installed `.specify/` mirrors are consistent (M7)
- DoD-6: `docs/agents/*` and `docs/commands/agents.md` are coherent with `docs/agents/design.md` and the Role/Stage/Type + Team/Loop model (SC-007)
- DoD-7: FR-021 research deliverable exists and ≥1 redesign decision cites it (SC-008)
- DoD-8: All success criteria SC-001…SC-009 validated via quickstart.md and recorded in verification.md

**DoD Status**: green   <!-- spec-023 scope: all DoD-N satisfied; 0 new regressions; 106 pre-existing unrelated failures documented in verification.md -->

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies on incomplete tasks)
- **[Story]**: Which user story this task belongs to (US1–US5)
- Include exact file paths in descriptions

### Task State Sigil (REQUIRED)

- `- [ ]` — Open. Not yet completed.
- `- [X]` — Closed. Fully executed and verified.
- `- [~]` — Deferred. Intentional handoff; record reason in verification.md.

## Path Conventions

Single project (code-generator / authoring-time tooling). Canonical template home: `skills/create-agent/templates/`; installed mirror: `.specify/skills/create-agent/templates/`. Tests under `tests/` (unit, contract, integration, scenarios).

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish baselines and confirm canonical locations before any migration.

- [X] T001 Capture a pre-migration baseline in `.specify/specs/023-agent-framework-redesign/verification.md`: record current counts from the quickstart.md grep commands (live `subrole|improver` files, `agent-subrole-|meta-coordinator` reference files) so post-migration deltas are measurable.
- [X] T002 Confirm canonical vs installed locations for the refactor: verify `skills/create-agent/templates/` is the source of truth and note that the installed mirror `.specify/skills/create-agent/templates/` is currently absent (must be created in T032); record the finding inline in verification.md.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Test guards and the research deliverable that gate the model/terminology work.

**⚠️ CRITICAL**: No user story work may begin until this phase is complete. The guards MUST be authored to FAIL against the current (pre-migration) tree, establishing the TDD red state.

- [X] T003 [P] Author deprecated-term guard test in `tests/unit/test_agent_deprecated_terms.py`: assert 0 live matches for `SubRole`/`Subrole`, `improver`, and `Meta-Coordinator` (as a role) across `skills/`, `templates/`, `docs/`, `tests/`, `.specify/agents/`, `.specify/skills/`, excluding immutable history (`.specify/specs/`, `CHANGELOG`, `draft/`, `.specify/memory/features/019.md`). Must FAIL now.
- [X] T004 [P] Author reference-integrity guard test in `tests/unit/test_agent_reference_integrity.py`: assert no live reference resolves to a pre-migration path/name (`agent-subrole-*`, `agent-role-meta-coordinator-template.md`, `agent-team-supervisor-template.md`) and that every referenced `agent-*-template.md` path exists under `skills/create-agent/templates/`. Must FAIL now.
- [X] T005 Produce FR-021 cross-project research deliverable `.specify/specs/023-agent-framework-redesign/research.md`: dispatch one agent per in-scope `/cws_work/*` sibling (exclude `spec-kit`) via the `organize-agents` parallel pattern, mining agent-framework best practices; consolidate findings and ensure ≥1 concrete redesign decision in this spec cites it (SC-008).

**Checkpoint**: Guards are red; research findings are available to inform model/template decisions.

---

## Phase 3: User Story 1 - Single Command Entry for All Agent Operations (Priority: P1) 🎯 MVP

**Goal**: Every agent action (create / organize / execute) is reachable through the single `/speckit.agents` command with intent recognition and graceful ambiguous-intent handling.

**Independent Test**: Invoke `/speckit.agents` with create / organize (parallel, serial, team-loop) / execute intents and an ambiguous input; confirm correct routing and that no other agent-specific command exists (SC-001, SC-006 entry path).

### Tests for User Story 1 (MANDATORY) ⚠️

- [X] T006 [US1] Add command-routing scenario test in `tests/scenarios/agents-command/single-entry-routing-scenario.md` asserting `/speckit.agents` routes create→create-agent, organize/execute→organize-agents, and reports capabilities on ambiguous intent (contracts/agents-command-contract.md A1–A6, FR-019). Must FAIL before T007.

### Implementation for User Story 1

- [X] T007 [US1] Refactor `templates/commands/agents.md` into the single-entry intent→capability router (create / organize / execute), delegate to skills without inline template rendering, add ambiguous/unsupported-intent capability listing (FR-001, FR-002, FR-019), and reflect the merged Team Supervisor (no Meta-Coordinator).
- [X] T008 [US1] Update `docs/commands/agents.md` to describe the single entry point, intent routing table, and Role/Stage/Type + Team/Loop model alignment.
- [X] T009 [US1] Verify command inventory: confirm `.qoder/commands/`, `.github/prompts/`, `.opencode/command/`, `.qwen/commands/` contain only `speckit.agents` as the agent-specific command (SC-001); record result in verification.md.

**Checkpoint**: `/speckit.agents` is the sole agent command and routes all intents — MVP functional.

---

## Phase 4: User Story 2 - Unified Conceptual Model and Terminology (Priority: P1)

**Goal**: Every agent artifact expresses Role/Stage/Type + Team/Loop with unified terminology; "SubRole" and "improver" are eliminated and the Team Supervisor is a single merged Meta role.

**Independent Test**: Inspect any template/skill and confirm Role/Stage/Type expression; repo-wide search finds 0 live "SubRole"/"improver"/"Meta-Coordinator" (as a role) outside history (SC-002, SC-005).

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T010 [P] [US2] Add model-conformance scenario test in `tests/scenarios/conceptual-model/role-stage-type-conformance-scenario.md` asserting each `skills/create-agent/templates/agent-role-*-template.md` declares Role, applicable Stage(s), and Type, and enforces Type-follows-Stage (contracts/conceptual-model-contract.md C1–C6). Must FAIL before implementation.

### Implementation for User Story 2

- [X] T011 [P] [US2] Rename `skills/create-agent/templates/agent-subrole-executor-template.md` → `agent-stage-executor-template.md` and update its internal Stage/Type framing (M2).
- [X] T012 [P] [US2] Rename `skills/create-agent/templates/agent-subrole-evaluator-template.md` → `agent-stage-evaluator-template.md` and update its internal Stage/Type framing (M2).
- [X] T013 [P] [US2] Rename `skills/create-agent/templates/agent-subrole-improver-template.md` → `agent-stage-optimizer-template.md`; replace all "improver" occurrences (including internal `name`/`description`) with "optimizer" (FR-014, M2).
- [X] T014 [US2] Merge `skills/create-agent/templates/agent-role-meta-coordinator-template.md` + `agent-team-supervisor-template.md` into a single `agent-role-team-supervisor-template.md` (Meta role, Meta at all stages); delete the two source files (FR-007, M3, D2).
- [X] T015 [P] [US2] Update `skills/create-agent/templates/agent-triad-orchestration-template.md`: "improver"→"optimizer", add Stage/Type framing (M4, data-model migration map).
- [X] T016 [P] [US2] Update `skills/create-agent/templates/agent-supervision-delegation.md`: terminology substitution ("SubRole"→"Stage", "improver"→"optimizer") and Team Supervisor merge references (M4).
- [X] T017 [P] [US2] Add Role/Stage/Type + Team/Loop model headers to the 6 worker role templates in `skills/create-agent/templates/agent-role-{requirements-analyst,system-designer,module-designer,test-engineer,qa-engineer,knowledge-manager}-template.md` (SC-005, C1/C6).
- [X] T018 [US2] Refactor `skills/create-agent/SKILL.md`: add the canonical Role/Stage/Type + Team/Loop model section, new stage/role names, canonical template location, and Team Supervisor merge; remove "SubRole"/"improver"/"Meta-Coordinator" (FR-003, FR-015, FR-016).
- [X] T019 [P] [US2] Update `skills/improve-agent/SKILL.md`: replace "improver"→"optimizer" and "SubRole"→"Stage" (FR-015).
- [X] T020 [US2] Update `skills/organize-agents/SKILL.md`: collapse the Team Loop from 3 layers to 2 (Team Supervisor + Workers), merge Meta-Coordinator into Team Supervisor, and apply terminology substitution (FR-007, M3, D2).

**Checkpoint**: Model and terminology unified across templates and skills; guards from T003/T004 now pass for these files.

---

## Phase 5: User Story 3 - Three Multi-Agent Collaboration Scenarios (Priority: P2)

**Goal**: parallel, serial, and team-loop topologies are reachable via `/speckit.agents` and expressed with the unified model.

**Independent Test**: Trigger each scenario via `/speckit.agents` and confirm the correct orchestration pattern is selected (SC-006).

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T021 [P] [US3] Update Layer-2 scenario `tests/scenarios/multi-agent-orchestration/team-loop-scenario.md`: apply terminology substitution and the 2-layer (Team Supervisor + Workers) structure; remove Meta-Coordinator (FR-008/009, M3, M4). Must reflect target state before T024.
- [X] T022 [P] [US3] Update Layer-2 scenario `tests/scenarios/multi-agent-orchestration/parallel-dispatch-scenario.md`: Meta-Coordinator→Team Supervisor, terminology and model alignment.
- [X] T023 [P] [US3] Update Layer-2 scenario `tests/scenarios/multi-agent-orchestration/serial-chain-scenario.md`: terminology and Role/Stage/Type alignment.

### Implementation for User Story 3

- [X] T024 [P] [US3] Align orchestration templates `skills/create-agent/templates/agent-parallel-orchestration-template.md` and `agent-serial-orchestration-template.md` to the Role/Stage/Type + Team/Loop model and unified terminology (FR-008, C2).
- [X] T025 [US3] Validate all three scenarios route correctly via `/speckit.agents` per quickstart.md §5 (parallel / serial / team-loop → `organize-agents`) and record the walkthrough result in verification.md (SC-006).

**Checkpoint**: All three collaboration topologies are model-consistent and selectable through the single entry point.

---

## Phase 6: User Story 4 - Temporary vs Persistent Agent Lifecycle (Priority: P2)

**Goal**: Temporary agents live only in context; persistent agents are stored under `.specify/agents` and wired into all supported tools; existing persisted agents are migrated to the new model.

**Independent Test**: Create one temporary and one persistent agent; confirm the temporary one is context-only and the persistent one is written to `.specify/agents` and linked into supported tools (e.g., `.qoder/agents` → `.specify/agents`) (FR-010/011/012, SC-009).

### Tests for User Story 4 (MANDATORY) ⚠️

- [X] T026 [P] [US4] Add integration test in `tests/integration/test_persistent_agent_lifecycle.py` asserting a persistent agent is written under `.specify/agents/` and that initialization produces each supported tool's agent config link (e.g., `.qoder/agents` → `.specify/agents`) while a temporary agent is not persisted (FR-010/011/012). Must FAIL before implementation as needed.

### Implementation for User Story 4

- [X] T027 [P] [US4] Migrate the 6 persisted agents `.specify/agents/{requirements-analyst,system-designer,module-designer,test-engineer,qa-engineer,knowledge-manager}.agent.md` to Role/Stage/Type expression and unified terminology (Stage not SubRole; optimizer not improver) so 0 retain deprecated concepts/terms (FR-020, SC-009).
- [X] T028 [US4] Migrate `.specify/agents/AGENTS.md`: replace Meta-Coordinator references with the merged Team Supervisor and apply terminology substitution (FR-020, M6).
- [X] T029 [US4] Document the temporary vs persistent lifecycle and all-officially-supported-tools config generation in `skills/create-agent/SKILL.md` (FR-010/011/012), consistent with Feature 022 multi-tool support.
- [X] T030 [US4] Verify `.qoder/agents → ../.specify/agents` link (and any other supported-tool agent config) is (re)created on initialization and survives migration; record in verification.md (FR-012, A4).

**Checkpoint**: Lifecycle handling verified; no live persisted agent retains deprecated concepts.

---

## Phase 7: User Story 5 - Consolidated Templates and Coherent Documentation (Priority: P3)

**Goal**: All agent templates are canonical under the `create-agent` skill, installed mirrors are re-synced, legacy duplicates are removed, and `docs/agents` is coherent with `design.md`.

**Independent Test**: Confirm 0 `agent-*` templates remain in `.specify/templates/` and top-level `templates/`; installed mirror matches source; `docs/agents/*` uses unified terminology with no statements contradicting `design.md` (SC-003, SC-004, SC-007).

### Implementation for User Story 5

- [X] T031 [US5] Remove stale `.specify/templates/agent-*` duplicates (`agent-role-*`, `agent-subrole-*`, `agent-supervision-delegation.md`, `agent-triad-orchestration-template.md`, and the `agent-{common,file,knowledge,plan,research}-template.md` set) after confirming no live references remain, so `ls .specify/templates/ | grep -i '^agent-'` returns none (FR-013, M1, D3).
- [X] T032 [US5] Create/re-sync installed mirrors from source: `.specify/skills/create-agent/**` (including the missing `templates/` subdir), `.specify/skills/improve-agent/**`, and `.specify/skills/organize-agents/**`, so installed copies match the refactored source (M7, Constitution VI).
- [X] T033 [P] [US5] Refactor `docs/agents/eei-triad-pattern.md` to the Role/Stage/Type + Team/Loop model and unified terminology (FR-017, SC-007).
- [X] T034 [P] [US5] Refactor `docs/agents/multi-agent-orchestration.md`: Meta-Coordinator→merged Team Supervisor, terminology, and the three collaboration scenarios (FR-017, SC-007).
- [X] T035 [US5] Reconcile `docs/agents/design.md` so any remaining "SubRole"/"improver"/"Meta-Coordinator" mentions appear only as explicit historical/migration context, not as live model vocabulary; ensure it remains the authoritative, self-consistent model source (SC-007).
- [X] T036 [US5] Fix any remaining broken references to old template paths or old stage names across `skills/`, `docs/`, `tests/`, and command templates so all references resolve (FR-016, SC-004).

**Checkpoint**: Templates consolidated, mirrors synced, docs coherent.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Turn all guards green, validate success criteria, and complete feature governance.

- [X] T037 [P] Run the deprecated-term and reference-integrity guards (`tests/unit/test_agent_deprecated_terms.py`, `tests/unit/test_agent_reference_integrity.py`) and confirm they now pass (Layer-1; SC-002, SC-004, SC-009).
- [X] T038 Run the full `pytest -q` suite and the Layer-2 structural scenario validation (`tests/scenarios/**`); resolve any regressions (Constitution IV/VI).
- [X] T039 [P] Execute the quickstart.md walkthrough end-to-end (§1–§7) and record SC-001…SC-009 outcomes in verification.md.
- [X] T040 [P] Feature integration review: confirm no new/invalidated Features result from this breakdown; update `.specify/memory/features.md` `Last Updated` and confirm the Feature 019 spec-023 evolution note in `.specify/memory/features/019.md` (status stays `Implemented`, per Decision D4).
- [X] T041 Final terminology sweep: run the quickstart.md §1/§3 greps and confirm 0 live matches; append the final measured deltas (vs T001 baseline) to verification.md and flip **DoD Status** to `green` when all DoD-N are satisfied.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately.
- **Foundational (Phase 2)**: Depends on Setup; guards (T003/T004) must be red and research (T005) available before user-story work. BLOCKS all user stories.
- **User Stories (Phase 3–7)**: All depend on Foundational completion.
  - US1 (P1) and US2 (P1) are the core; US2 underpins US3/US4/US5 conceptually.
  - US3 (P2) depends on US2 terminology/merge (T014, T020) landing.
  - US4 (P2) depends on US2 for the model expression migrated into persisted agents; shares `create-agent/SKILL.md` with US2 (T018→T029 ordering).
  - US5 (P3) depends on US2 renames/merge (T011–T020) and US3/US4 edits being complete before mirror re-sync (T032) and reference fixes (T036).
- **Polish (Phase 8)**: Depends on all desired user stories.

### Within Each User Story

- Tests are written/updated to reflect target state BEFORE the corresponding implementation.
- Renames/merge before terminology sweeps that depend on the new filenames.
- Docs and mirror sync after source templates are finalized.

### Parallel Opportunities

- T003 and T004 (distinct test files) run in parallel.
- US2 template edits on distinct files run in parallel: T011, T012, T013, T015, T016, T017, T019 (T014, T018, T020 are hubs — sequential).
- US3 scenario updates T021, T022, T023, and template alignment T024 run in parallel (distinct files).
- US4 T026 and T027 run in parallel (distinct files).
- US5 doc refactors T033 and T034 run in parallel.
- Polish T037, T039, T040 run in parallel.

---

## Parallel Example: User Story 2

```bash
# Stage renames + isolated template edits together (distinct files):
Task: "Rename agent-subrole-executor-template.md → agent-stage-executor-template.md"
Task: "Rename agent-subrole-evaluator-template.md → agent-stage-evaluator-template.md"
Task: "Rename agent-subrole-improver-template.md → agent-stage-optimizer-template.md (+ internal terms)"
Task: "Update agent-triad-orchestration-template.md (improver→optimizer, Stage/Type)"
Task: "Update agent-supervision-delegation.md (terminology + merge)"
Task: "Add model headers to the 6 agent-role-*-template.md worker roles"
Task: "Update improve-agent/SKILL.md (improver→optimizer, subrole→stage)"

# Then run hubs sequentially: merge supervisor (T014) → create-agent SKILL (T018) → organize-agents SKILL (T020)
```

---

## Implementation Strategy

### MVP First (User Story 1)

1. Complete Phase 1: Setup.
2. Complete Phase 2: Foundational (guards red + research).
3. Complete Phase 3: User Story 1 (single entry + routing).
4. **STOP and VALIDATE**: `/speckit.agents` routes all intents; only agent command exists (SC-001).

### Incremental Delivery

1. Setup + Foundational → guards and research ready.
2. US1 → single entry (MVP).
3. US2 → unified model/terminology (unblocks the rest).
4. US3 → collaboration scenarios.
5. US4 → lifecycle + persisted-agent migration.
6. US5 → template consolidation + doc coherence + mirror sync.
7. Polish → guards green, quickstart validated, feature governance.

### Parallel Team Strategy

After Foundational: one developer drives US1 while another drives US2 (the conceptual backbone). Once US2 renames/merge land, US3, US4, and US5 doc/scenario work can proceed in parallel by different owners, converging at Phase 8.

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks.
- [Story] label maps each task to its user story for traceability (Setup/Foundational/Polish carry no story label).
- Tests Mode ON: guards (T003/T004) and story tests are authored to fail first, then made green by implementation.
- Immutable history (`.specify/specs/*`, `CHANGELOG`, `draft/`, `features/019.md` narrative) is excluded from the zero-reference requirement (Decision D5).
- Deferral discipline: prefer `[~]` with a recorded reason over leaving a task `[ ]`.
