---
description: "Task list for Agent Team Management (Feature 027)"
---

# Tasks: Agent Team Management

**Requirement ID**: 026
**Requirement Key**: 026-agent-team-management
**Related Feature**: 027 Team Management (from `.specify/memory/features.md`)
**Input**: Design documents from `.specify/specs/026-agent-team-management/`
**Prerequisites**: plan.md ✅, requirements.md ✅, data-model.md ✅, contracts/ ✅ (4 contracts), quickstart.md ✅

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates writing/updating tests BEFORE implementing new behavior; plan §M7 requires the migration guard tests to be authored before implementation)

**Tests**: Test tasks below are MANDATORY and MUST be written first and observed FAILING before their corresponding implementation tasks.

**Organization**: Tasks are grouped by user story (US1/US2/US3 from requirements.md) to enable independent implementation and testing. Because this is a rename+relocation migration, US3 (separation) validates work partly produced in US1; explicit cross-story dependencies are noted in the Dependencies section.

## Definition of Done (DoD)

- DoD-1: `/speckit.team` exposes exactly three modes (create / modify / run) and routes each to the correct skill (FR-001, FR-002).
- DoD-2: `create-team` (renamed from `organize-agents`) and `improve-team` skills exist, resolve, and preserve the three collaboration patterns (FR-004, FR-005, FR-008).
- DoD-3: Zero `organize-agents` references remain in active (non-archived) paths (SC-004).
- DoD-4: The multi-agent Conceptual Model is defined exactly once — in the team domain — and is no longer embedded in `create-agent` (SC-003, SC-006).
- DoD-5: All M7 guard tests pass (`pytest -m contract`): rename, command routing, single Conceptual Model, single-agent purity, zero dangling reference, skill presence.
- DoD-6: `.specify/instructions.md` and per-tool command copies regenerated; docs/registries reflect `/speckit.team` + team skills (FR-015).
- DoD-7: quickstart.md create → modify → run walkthrough validated; changes traced to requirements FR-001…FR-017.

**DoD Status**: met

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: US1 / US2 / US3 (Setup, Foundational, Polish carry no story label)
- Include exact file paths in descriptions

### Task State Sigil (REQUIRED)

- `- [ ]` — **Open**. Not completed.
- `- [X]` — **Closed**. Fully executed and verified.
- `- [~]` — **Deferred**. Intentionally handed off; record reason in `verification.md`.

## Path Conventions

Code-generator / framework layout: `templates/` (command sources), `skills/<slug>/` (skills, mirrored to `.specify/skills/`), `docs/`, `tests/{contract,integration,scenarios}/`, `.specify/` runtime. Team runtime store: `.specify/teams/<slug>.team.md`.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Establish the new runtime store and skill scaffolding.

- [X] T001 Create the runtime team store marker `.specify/teams/.gitkeep` so `.specify/teams/` (canonical persisted-team store per data-model.md) is tracked
- [X] T002 [P] Scaffold the new skill directory `skills/improve-team/` (empty dir to receive SKILL.md in Phase 4)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Rename `organize-agents` → `create-team`. This is the gate for every user story (US1 creates/runs via it, US2 improves referencing it, US3 validates its new name).

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [X] T003 [P] Write the rename guard test in tests/contract/test_create_team_rename.py — asserts `skills/create-team/SKILL.md` resolves as a skill and `skills/organize-agents/` no longer resolves (MUST FAIL first)
- [X] T004 Rename directory `skills/organize-agents/` → `skills/create-team/` via `git mv` (preserve history) and create the `references/` and `templates/` subdirectories under `skills/create-team/`
- [X] T005 Update `skills/create-team/SKILL.md` frontmatter and body: `name: create-team`, `skill_id: "<SKILL:.specify/skills/create-team/SKILL.md>"`, description covering team creation + execution (parallel / serial / team-loop); remove every `organize-agents` string from the skill body (per create-team-skill-contract § Identity)

**Checkpoint**: `create-team` resolves under its new name; T003 rename guard green.

---

## Phase 3: User Story 1 - Create & run a team via /speckit.team (Priority: P1) 🎯 MVP

**Goal**: A single command `/speckit.team` lets a user organize agents into a team (static + dynamic structure), persist it as `.specify/teams/<slug>.team.md`, and run it behind a preview→confirm→execute gate.

**Independent Test**: Invoke `/speckit.team 组织一个团队…` → intent classified `create` → `create-team` proposes a roster + pattern → on confirm a `.team.md` is persisted with Static + Dynamic structure; then `/speckit.team 运行 <slug>` renders both structures and executes only after confirmation.

### Tests for User Story 1 (MANDATORY) ⚠️

> Write FIRST, ensure they FAIL before implementation.

- [X] T006 [P] [US1] Command routing guard test in tests/contract/test_team_command_routing.py — asserts `templates/commands/team.md` exposes create/modify/run modes and that `templates/commands/agents.md` does NOT route team operations (SC-002; command-contract § MUST/MUST NOT)
- [X] T007 [P] [US1] Integration test in tests/integration/test_team_create_flow.py — quickstart §1: create intent → serial roster proposed → persisted `.team.md` contains YAML frontmatter (slug/pattern/members/config), a `## Static Structure` matrix, and a `## Dynamic Structure` (DAG + handoff) per data-model schema

### Implementation for User Story 1

- [X] T008 [US1] Create `templates/commands/team.md` — source for `/speckit.team` with 3 modes (create→create-team, modify→improve-team, run→create-team execution), intent routing, ambiguous-intent capability report (FR-002), team-not-found handling (FR-010), and the run-mode preview→confirm→execute gate (team-command-contract §§ Modes/Routing/Run-mode)
- [X] T009 [P] [US1] Create `skills/create-team/references/conceptual-model.md` — the extracted Conceptual Model (Role × Stage × Type + Team/Loop) as the single source of truth for the team domain (FR-012)
- [X] T010 [US1] Relocate the 8 multi-agent templates from `skills/create-agent/templates/` → `skills/create-team/templates/` via `git mv`: `agent-role-team-supervisor-template.md`, `agent-stage-executor-template.md`, `agent-stage-evaluator-template.md`, `agent-stage-optimizer-template.md`, `agent-triad-orchestration-template.md`, `agent-parallel-orchestration-template.md`, `agent-serial-orchestration-template.md`, `agent-workflow-schema.md` (data-model § Template Classification)
- [X] T011 [US1] Update `skills/create-team/SKILL.md` behavior sections: define (decision-tree pattern selection; build roster + pattern config per data-model `.team.md` schema; propose members from a goal per FR-007; team-loop requires exactly one Team Supervisor) and execute (preview→confirm→orchestrate; territory validation / DAG no-cycle / max-iteration cap / file-path-only handoff); repoint references to `references/conceptual-model.md` and `templates/` at the new paths (depends on T009, T010)
- [X] T012 [US1] Update `templates/commands/agents.md` — remove the organize/execute rows and all `organize-agents` routing; scope `/speckit.agents` to single-agent create/refine only; direct team intents to `/speckit.team` (FR-003; migration-contract M6)
- [X] T013 [P] [US1] Create `docs/commands/team.md` — user doc for `/speckit.team` (3 modes + preview/confirm gate)

### Manual Verification for User Story 1

- [X] T014 [US1] Manual QA: run quickstart.md §1 (create) and §3 (run preview→confirm→execute) end-to-end; confirm no single-agent path is touched

**Checkpoint**: `/speckit.team` create + run functional and independently testable (MVP).

---

## Phase 4: User Story 2 - Improve an existing team (Priority: P2)

**Goal**: `improve-team` makes targeted, evidence-based, structure-preserving edits to a persisted team and reports a clear "team not found" when the target is missing.

**Independent Test**: `/speckit.team 给 <slug> 增加一个 QA 工程师` → `improve-team` loads the `.team.md`, adds the member, leaves the rest unchanged, bumps `updated`; `/speckit.team 优化 nonexistent-team` → "team not found" + offer to create.

### Tests for User Story 2 (MANDATORY) ⚠️

- [X] T015 [P] [US2] Skill-presence guard test in tests/contract/test_improve_team_presence.py — asserts `skills/improve-team/SKILL.md` resolves and `improve-team` is in the non-declarable set (MUST FAIL first)
- [X] T016 [P] [US2] Integration test in tests/integration/test_team_improve_flow.py — quickstart §2: add a `qa-engineer` member with all unaffected fields byte-identical (SC-005) and `updated` bumped; plus the negative "team not found" case returning an offer to create (FR-010)

### Implementation for User Story 2

- [X] T017 [US2] Create `skills/improve-team/SKILL.md` per improve-team-skill-contract — frontmatter (`name: improve-team`, `skill_id: "<SKILL:.specify/skills/improve-team/SKILL.md>"`, trigger-phrase description) and behavior: resolve target → gather evidence → attribute root cause → apply targeted structure-preserving edits → re-persist + bump `updated` → change report; "team not found" offers to create (FR-008, FR-009, FR-010)
- [X] T018 [US2] Update the non-declarable skill list in `skills/create-skills/SKILL.md` (line ~149) — replace `organize-agents` with `create-team` and `improve-team`
- [X] T019 [US2] Update the `NON_DECLARABLE` set in `tests/contract/test_agent_skill_enablement.py` — replace `organize-agents` with `create-team`, `improve-team`

**Checkpoint**: create → improve lifecycle for teams complete (FR-014).

---

## Phase 5: User Story 3 - Clean separation between single-agent and team management (Priority: P2)

**Goal**: Single-agent skills manage only single agents; the team domain owns all multi-agent concepts; the Conceptual Model lives in exactly one place; no dangling `organize-agents` references remain.

**Independent Test**: Inspect `create-agent`/`improve-agent` → no team/orchestration content, no `triad`/`team-supervisor` modes; the Conceptual Model appears authoritatively once (team domain); repo search for `organize-agents` in active paths → zero hits.

### Tests for User Story 3 (MANDATORY) ⚠️

- [X] T020 [P] [US3] Single-Conceptual-Model guard test in tests/contract/test_single_conceptual_model.py — asserts the Conceptual Model is defined exactly once (in `skills/create-team/references/conceptual-model.md`) and is NOT embedded in `skills/create-agent/SKILL.md` (SC-006) (MUST FAIL first)
- [X] T021 [P] [US3] Single-agent-purity guard test in tests/contract/test_single_agent_purity.py — asserts `skills/create-agent/SKILL.md` and `skills/improve-agent/SKILL.md` contain no team/orchestration content and no `triad`/`team-supervisor` modes (SC-003) (MUST FAIL first)
- [X] T022 [P] [US3] Zero-dangling-reference guard test in tests/contract/test_no_organize_agents_refs.py — repo-wide search asserts `organize-agents` appears in NO active path, excluding historical `.specify/specs/*` archives (SC-004) (MUST FAIL first)

### Implementation for User Story 3

- [X] T023 [US3] Edit `skills/create-agent/SKILL.md` — remove the `## Conceptual Model (Role × Stage × Type + Team/Loop)` section, replace with a one-line pointer to `skills/create-team/references/conceptual-model.md`, and drop `triad` + `team-supervisor` from the capability matrix (retain `role`, `supervisor`, `custom`, `project-custom`) (FR-011, FR-013, FR-016; depends on T009)
- [X] T024 [US3] Edit `skills/improve-agent/SKILL.md` — remove the Triad Refinement section and stage/orchestration refinement targets (those move to `improve-team`) (FR-013)
- [X] T025 [P] [US3] Update `templates/commands/skills.md` — repoint any `organize-agents` reference to the team skills (migration-contract M6)
- [X] T026 [P] [US3] Update `tests/scenarios/agents-command/single-entry-routing-scenario.md` — remove team routing from the `/speckit.agents` scenario
- [X] T027 [US3] Repoint Conceptual Model + orchestration ownership to the team domain and `/speckit.team` across `docs/agents/design.md`, `docs/agents/command-and-skills.md`, `docs/agents/multi-agent-orchestration.md`, `docs/agents/README.md`
- [X] T028 [P] [US3] Update routing tables in `docs/commands/agents.md` and `docs/commands/skills.md`; add `/speckit.team` entry

**Checkpoint**: Single-agent ↔ team separation fully realized and guarded.

---

## Phase 6: Polish & Cross-Cutting Concerns

- [X] T029 Regenerate `.specify/instructions.md` (and compatibility symlinks) via `/speckit.instructions` — refresh the skills registry, resource registry, and skill inventory (add `create-team`/`improve-team`, drop `organize-agents`) (FR-015)
- [X] T030 Regenerate per-tool command copies so `speckit.agents.*` drops team routing and `speckit.team.*` is added across `.qoder/commands/`, `.claude/commands/`, `.github/prompts/`, `.opencode/command/`, `.qwen/commands/` (migration-contract M6)
- [X] T031 [P] Run `pytest -m contract` — confirm all M7 guard tests green (rename, routing, single Conceptual Model, single-agent purity, zero dangling reference, improve-team presence)
- [X] T032 [P] Execute quickstart.md end-to-end (create → modify → run + separation checks) and record results in `.specify/specs/026-agent-team-management/verification.md`
- [X] T033 Advance Feature 027 status per the state machine in `.specify/memory/features.md` and `.specify/memory/features/027.md` once implementation is verified

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: no dependencies.
- **Foundational (Phase 2)**: after Setup; T003 (test) before T004→T005. **Blocks all user stories.**
- **US1 (Phase 3)**: after Foundational. Tests T006–T007 before T008–T013.
- **US2 (Phase 4)**: after Foundational. Tests T015–T016 before T017–T019. Authorable independently; a real team to improve comes from US1 (soft dependency for the live walkthrough only).
- **US3 (Phase 5)**: after Foundational. Tests T020–T022 before T023–T028. **Depends on US1 T009 (conceptual-model.md must exist before removal from create-agent) and T010 (templates must be moved out of create-agent) for its guards to pass.**
- **Polish (Phase 6)**: after all desired stories; T029/T030 before T031/T032.

### Within Each User Story

- Tests written and FAILING before implementation.
- create-team references (T009) + moved templates (T010) before create-team behavior (T011).
- Command source (T008) + skills before instruction/command regeneration (T029/T030).

### Parallel Opportunities

- Setup: T002 [P].
- US1 tests T006, T007 [P]; impl T009 and T013 [P] (distinct files) while T008/T010/T011/T012 are sequential-ish (T011 depends on T009/T010).
- US2 tests T015, T016 [P].
- US3 tests T020, T021, T022 [P]; impl T025, T026, T028 [P].
- Polish: T031, T032 [P].

---

## Parallel Example: User Story 3

```bash
# Launch all US3 guard tests together (all MUST fail initially):
Task: "Single-Conceptual-Model guard test in tests/contract/test_single_conceptual_model.py"
Task: "Single-agent-purity guard test in tests/contract/test_single_agent_purity.py"
Task: "Zero-dangling-reference guard test in tests/contract/test_no_organize_agents_refs.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Phase 1 Setup → Phase 2 Foundational (rename) → Phase 3 US1.
2. **STOP and VALIDATE**: create a team and run it (preview→confirm→execute) via `/speckit.team`.
3. Ships the core value: a dedicated home for multi-agent work.

### Incremental Delivery

1. Setup + Foundational → create-team resolves.
2. US1 → create + run a team (MVP).
3. US2 → improve lifecycle closes (create → improve).
4. US3 → separation guaranteed and guarded.
5. Polish → regenerate instructions/commands, run guard suite, validate quickstart, advance Feature 027.

---

## Notes

- [P] tasks = different files, no dependencies.
- This is a migration/refactor feature: US2 depends on US1 (a team must exist), and US3 (separation) validates work partly produced in US1 — mirrored in the Dependencies section, consistent with requirements.md (US3 is the structural foundation for US1/US2).
- Prefer `git mv` for all renames/relocations to preserve history.
- Historical `.specify/specs/*` archives are excluded from the zero-dangling-reference rule.
- Commit after each task or logical group; verify guard tests fail before implementing.
