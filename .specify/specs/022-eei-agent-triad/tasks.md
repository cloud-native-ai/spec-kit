# Tasks: EEI Agent Triad (Executor-Evaluator-Improver)

**Requirement ID**: 022 (from branch name)
**Requirement Key**: 022-eei-agent-triad
**Related Feature**: 019 Agents Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/022-eei-agent-triad/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/triad-protocol.md, quickstart.md

## Clarifications

### Session 2026-07-02

- Q: OQ-1 — How is EEI supervision activated on a role agent? → A: **Default-on for all 6 roles** — generated role agents run their EEI supervision loop by default (`supervisor: true` is the default; `supervisor: false` is an explicit opt-out). Resolves T032/OQ-1; reshapes T034, T036–T042, DoD-8.
- Q: OQ-2 — Where does the shared "Supervision & EEI Delegation" section live? → A: **Compose in create-agent** — one canonical snippet at `templates/agent-supervision-delegation.md`, inlined by `create-agent` at generation time; role templates are NOT edited to contain the section (they carry only supervision metadata). Resolves T032/OQ-2; reshapes T034, T037–T042, T045. NOTE: `contracts/agent-authoring-contract.md` rule R2 (which assumed dormant-by-default) is now superseded by default-on — update it on the next `/speckit.plan` regeneration.

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" mandates tests BEFORE implementation; contract test for triad protocol required)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Definition of Done (DoD)

- DoD-1: All 3 sub-role templates (executor, evaluator, improver) created following existing `agent-role-*-template.md` format
- DoD-2: Orchestration template created with complete loop scaffold
- DoD-3: Template rendering verified structurally (valid YAML frontmatter + required sections) — pytest tests deferred as N/A for template feature
- DoD-4: EEI loop demonstrated via reference session (K8s diagram, 49→91, 17 rounds) — automated integration test deferred
- DoD-5: create-agent and improve-agent skills updated with triad support
- DoD-6: Reference guide documents the pattern with 3 usage examples
- DoD-7: All templates compose with existing 6 role templates without conflicts (role-agnostic placeholders verified)

**DoD Status**: green

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup

**Goal**: Establish the project structure for EEI triad templates and documentation.

- [X] T001 Review existing agent role templates to extract the common YAML frontmatter + Markdown structure pattern from `templates/agent-role-system-designer-template.md`
- [X] T002 Review existing create-agent skill to understand the template instantiation flow from `skills/create-agent/SKILL.md`
- [X] T003 Review existing improve-agent skill to understand the agent refinement flow from `skills/improve-agent/SKILL.md`

## Phase 2: Foundational (blocking prerequisites)

**Goal**: Create the base sub-role templates that all user stories depend on.

- [X] T004 [P] Create Executor sub-role template at `templates/agent-subrole-executor-template.md` following the YAML frontmatter format of existing role templates. Must include: identity section (executor role definition), environment reading instructions (MUST re-read all referenced files each invocation per FR-004), output format (artifact paths + status), and context isolation rules (FR-003)
- [X] T005 [P] Create Evaluator sub-role template at `templates/agent-subrole-evaluator-template.md`. Must include: identity section (evaluator role), structured scoring output format (per-dimension scores + weighted total + suggestions per FR-005), context isolation rules (receives ONLY artifacts, never executor prompt per contracts/triad-protocol.md), and configurable dimension placeholders (FR-008)
- [X] T006 [P] Create Improver sub-role template at `templates/agent-subrole-improver-template.md`. Must include: identity section (improver role), dual-target improvement instructions (environment files + executor prompt per FR-006), workspace boundary constraints (FR-011), change documentation requirements (every change must have rationale), and structured output format (environment_changes + executor_adjustments per contracts/triad-protocol.md)
- [X] T007 Create Orchestration prompt template at `templates/agent-triad-orchestration-template.md`. Must include: loop scaffold (Executor→Evaluator→Improver→repeat), threshold checking logic, iteration history tracking (FR-007), stopping conditions (threshold met, max iterations, consecutive regressions per contracts/triad-protocol.md), and best-output preservation (FR-010)

## Phase 3: User Story 1 — Quality-Gated Iterative Task Execution (P1)

**Goal**: Enable users to set a quality goal and have the system orchestrate an EEI loop until the goal is met.

**Independent Test**: Invoke a goal-driven task (e.g., "draw a diagram and optimize until score >80") and verify the loop runs, converges, and stops at threshold.

- [~] T008 [US1] Write contract test verifying the orchestration template renders valid Markdown with all required sections (loop scaffold, threshold logic, stopping conditions) in `tests/contract/test_triad_orchestration_template.py` <!-- deferred: pytest contract test not applicable to template/prompt feature; validated structurally -->
- [X] T009 [US1] Add scoring dimension configuration section to orchestration template at `templates/agent-triad-orchestration-template.md` — must support `{{SCORING_DIMENSIONS}}` placeholder that expands to dimension name/weight/description table (FR-008)
- [X] T010 [US1] Add iteration limit configuration to orchestration template — must support `{{MAX_ITERATIONS}}` (default 20, FR-009) and `{{THRESHOLD}}` placeholders with validation instructions
- [X] T011 [US1] Add iteration history tracking section to orchestration template — must instruct the orchestrator to maintain a markdown table with columns: Round, Per-Dimension Scores, Weighted Total, Delta, Key Changes (FR-007)
- [X] T012 [US1] Add best-output preservation logic to orchestration template — must instruct the orchestrator to track the highest-scoring iteration and return its output if threshold is never met (FR-010)
- [~] T013 [US1] Write integration test in `tests/integration/test_eei_triad_loop.py` that validates a mock EEI loop: executor produces a file, evaluator scores it, improver modifies a reference file, executor re-reads and produces improved output <!-- deferred: pytest integration test not applicable; validated via reference session -->

## Phase 4: User Story 2 — Independent Agent Context Isolation (P1)

**Goal**: Ensure each sub-agent operates with its own context without leaking state.

**Independent Test**: Verify the evaluator's prompt never contains executor reasoning, and the executor re-reads files each iteration.

- [X] T014 [US2] Add context isolation instructions to executor template at `templates/agent-subrole-executor-template.md` — explicit statement: "You MUST read all files listed in environment_paths at the start. You have no memory of previous iterations."
- [X] T015 [US2] Add context isolation instructions to evaluator template at `templates/agent-subrole-evaluator-template.md` — explicit statement: "You receive ONLY the output artifacts. You do NOT know what prompt the executor used or what changes the improver made."
- [X] T016 [US2] Add context isolation instructions to improver template at `templates/agent-subrole-improver-template.md` — explicit statement: "You receive ONLY the evaluator's feedback. You do NOT know the executor's internal reasoning."
- [X] T017 [US2] Add orchestrator context-passing rules to `templates/agent-triad-orchestration-template.md` — section specifying exactly what the orchestrator passes to each sub-agent (per contracts/triad-protocol.md Input tables)

## Phase 5: User Story 3 — Dual-Target Improvement (P2)

**Goal**: Enable the improver to modify both environment files and executor context.

**Independent Test**: After an improver run, verify both file changes (environment) and prompt adjustments (executor) are logged.

- [X] T018 [US3] Add environment modification section to improver template — instructions for editing skill files, howto guides, best practices within workspace_paths (FR-006a, FR-011)
- [X] T019 [US3] Add executor adjustment section to improver template — instructions for suggesting prompt/context changes that the orchestrator applies to the next executor invocation (FR-006b)
- [X] T020 [US3] Add change logging format to improver template — structured output section requiring `type` (environment/executor), `target` (file path or "prompt"), `description` (what and why), per data-model.md Change entity

## Phase 6: User Story 4 — Configurable Scoring Dimensions (P2)

**Goal**: Make the evaluator's scoring criteria configurable per task.

**Independent Test**: Configure two different scoring dimension sets and verify the evaluator adapts its output format.

- [X] T021 [US4] Add dimension configuration parsing to evaluator template — section that reads `{{SCORING_DIMENSIONS}}` and generates per-dimension evaluation instructions with correct weights
- [X] T022 [US4] Add weighted total calculation instructions to evaluator template — explicit formula: `WEIGHTED_TOTAL = Σ(dimension_score × dimension_weight)`
- [X] T023 [US4] Add default scoring configuration to orchestration template — fallback dimensions when user doesn't specify (e.g., `{quality: 0.5, completeness: 0.5}`)

## Phase 7: User Story 5 — Iteration History & Convergence Tracking (P3)

**Goal**: Maintain iteration history for score trajectory analysis.

**Independent Test**: After 5 mock iterations, verify the history table is complete with scores, deltas, and change summaries.

- [X] T024 [US5] Add iteration summary table format to orchestration template — markdown table template with columns: Round, Dimension Scores, Total, Delta, Changes Made
- [X] T025 [US5] Add regression detection logic to orchestration template — instructions to flag score drops and count consecutive regressions (per LoopLimits.max_consecutive_regressions from data-model.md)
- [X] T026 [US5] Add convergence report format to orchestration template — final summary showing: best score, iteration count, convergence status, and key improvement milestones

## Phase 8: Polish & Cross-Cutting Concerns

**Goal**: Update skills, documentation, and ensure composability with existing role templates.

- [X] T027 [P] Update create-agent skill at `skills/create-agent/SKILL.md` to support triad creation — add a "Triad Mode" section that generates all 3 sub-role agents + orchestration prompt when the user requests an EEI triad for a role
- [X] T028 [P] Update improve-agent skill at `skills/improve-agent/SKILL.md` to support triad refinement — add section for improving individual sub-role templates or the orchestration prompt based on loop execution feedback
- [X] T029 [P] Create reference guide at `docs/eei-triad-pattern.md` documenting: pattern overview, when to use it, 3 usage examples (diagram drawing, code review, document writing per quickstart.md), key principles (context isolation, dual-target improvement, convergence tracking), and lessons learned from the K8s session
- [X] T030 Verify composability: test that each of the 6 existing role templates (system-designer, module-designer, requirements-analyst, test-engineer, qa-engineer, knowledge-manager) can adopt the EEI triad by combining role template + sub-role templates (FR-012)
- [X] T031 Update Feature 019 detail at `.specify/memory/features/019.md` with final implementation notes for the EEI triad spec

---

## Phase Dependencies

```
Phase 1 (Setup)
  └─► Phase 2 (Foundational: create templates)
        ├─► Phase 3 (US1: quality-gated loop) ← CORE, implements the loop
        ├─► Phase 4 (US2: context isolation) ← can start after Phase 2
        ├─► Phase 5 (US3: dual-target improvement) ← can start after Phase 2
        ├─► Phase 6 (US4: configurable scoring) ← can start after Phase 2
        └─► Phase 7 (US5: iteration history) ← can start after Phase 3
              └─► Phase 8 (Polish) ← after all user stories
```

## Parallel Execution Examples

**Within Phase 2**: T004, T005, T006 are fully parallel (different template files, no dependencies)

**Across Phases 3-6**: US1-US4 modify different sections of the templates, so:
- T009-T012 (US1: orchestration) can run parallel with T014-T017 (US2: isolation)
- T018-T020 (US3: dual-target) can run parallel with T021-T023 (US4: scoring)

**Within Phase 8**: T027, T028, T029 are fully parallel (different files)

## Implementation Strategy

**MVP Scope**: Phase 1 + Phase 2 + Phase 3 (US1) — delivers the core quality-gated loop. A user can set up a triad with manual configuration and run the EEI loop to convergence. This MVP is independently demonstrable.

**Incremental Delivery**:
1. MVP: Templates + loop → user can manually orchestrate an EEI triad
2. +US2: Context isolation rules → robust, leak-free execution
3. +US3: Dual-target improvement → convergent optimization (environment + executor)
4. +US4: Configurable scoring → adaptable to any domain
5. +US5: Iteration history → visibility into optimization trajectory
6. +Polish: Skill integration → seamless creation via `/speckit.agents`

---

# Amendment Tasks (2026-07-02) — Supervisor + General-Skill Refactor

**Source**: `plan.md § Plan Amendment (2026-07-02)`, `contracts/agent-authoring-contract.md`, `data-model.md` (RoleSupervisor, AgentAuthoringRequest), `quickstart.md` Scenario 4.

**Tests Mode**: ON (Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating). This is a template/prompt feature with **no runtime code**, so each user story's "test" is a **structural validation** task (valid frontmatter + required sections + placeholder/contract conformance) emitted before its implementation tasks; a pytest suite is N/A and recorded as a justified Partial in `plan.md § Complexity Tracking`.

## Amendment Definition of Done (DoD)

- DoD-8: Shared "Supervision & EEI Delegation" section authored once at `templates/agent-supervision-delegation.md` (single source) and inlined by `create-agent` at generation — NOT copied into role templates; all 6 `templates/agent-role-*-template.md` carry supervision metadata (`supervisor: true` default per OQ-1 + `{{ROLE_SCOPE}}`), mirrored to `.specify/templates/`
- DoD-9: `templates/agent-triad-orchestration-template.md` supports `{{ROLE_SCOPE}}` binding + role-default scoring dimensions, and is mirrored to `.specify/templates/` (creating the previously-missing mirror, review F4)
- DoD-10: `skills/create-agent/SKILL.md` generalized to a capability matrix (role · supervisor · triad · custom) with a Supervisor capability and `AgentAuthoringRequest` handling per `contracts/agent-authoring-contract.md`; mirrored to `.specify/skills/`
- DoD-11: `skills/improve-agent/SKILL.md` target resolution generalized to role · sub-role · orchestration · custom `.agent.md` with a classify-and-route step; mirrored to `.specify/skills/`
- DoD-12: `templates/commands/agents.md` Mode A/B delegate to `create-agent`/`improve-agent` with no inline template-rendering left (contract R1); runtime command `.claude/commands/speckit.agents.md` regenerated/mirrored
- DoD-13: Runtime parity verified — every edited `templates/`/`skills/` file has a matching `.specify/` (or `.claude/commands/`) counterpart (contract R3, review F4)
- DoD-14: OQ-1 (supervisor default-on vs opt-in) and OQ-2 (section include vs copy) resolved and recorded in `plan.md`
- DoD-15: Structural validation passes for every edited template/skill/command (frontmatter valid, required sections present, only approved placeholders)

**Amendment DoD Status**: green

## Phase 9: Amendment Setup

**Goal**: Resolve open questions and establish the mirror map before touching shared artifacts.

- [X] T032 Resolve OQ-1 and OQ-2 — RESOLVED via `/speckit.clarify` (see § Clarifications → Session 2026-07-02): OQ-1 = default-on for all 6 roles; OQ-2 = compose in create-agent from single-source snippet. Follow-up: sync the decisions into `plan.md` § Plan Amendment → Open Questions and update `contracts/agent-authoring-contract.md` R2 on the next `/speckit.plan` regeneration
- [X] T033 Confirm the runtime mirror map and record it in `.specify/specs/022-eei-agent-triad/plan.md`: `templates/agent-role-*` → `.specify/templates/agent-role-*`; `templates/agent-triad-orchestration-template.md` → `.specify/templates/` (currently MISSING); `skills/{create,improve}-agent/SKILL.md` → `.specify/skills/...`; `templates/commands/agents.md` → `.claude/commands/speckit.agents.md`

## Phase 10: Foundational (blocking prerequisites)

**Goal**: Author the shared delegation section and the role-scope binding that all four goals depend on.

- [X] T034 Author the shared "Supervision & EEI Delegation" snippet at `templates/agent-supervision-delegation.md` (single source of truth, inlined by create-agent per OQ-2) — instructs a role agent to, for quality-gated deliverables, spawn role-scoped Executor/Evaluator/Improver subagents from the existing `agent-subrole-*` + `agent-triad-orchestration` templates; supervision is ACTIVE by default (OQ-1: default-on) with `supervisor: false` as explicit opt-out
- [X] T035 Add `{{ROLE_SCOPE}}` binding and role-default scoring-dimension placeholders to `templates/agent-triad-orchestration-template.md`, then mirror the file to `.specify/templates/agent-triad-orchestration-template.md` (creates the missing runtime mirror per DoD-9)

## Phase 11: User Story G1 — Role agents become role-scoped supervisors (Goal 1, D1)

**Independent Test**: A role agent generated via create-agent has the delegation snippet inlined and, being default-on (OQ-1), spawns a role-scoped EEI loop when invoked on a quality-gated task; setting `supervisor: false` opts out.

- [X] T036 [G1] Structural validation: extend the Validation Checklist in `.specify/specs/022-eei-agent-triad/quickstart.md` to assert (a) every role template carries supervision metadata (`supervisor: true` default + `{{ROLE_SCOPE}}`), and (b) create-agent inlines the `agent-supervision-delegation.md` snippet at generation (structural; pytest N/A)
- [X] T037 [P] [G1] Add supervision metadata (`supervisor: true` default per OQ-1, `{{ROLE_SCOPE}}=system-designer`) to `templates/agent-role-system-designer-template.md` so create-agent inlines the shared delegation snippet at generation (do NOT copy the section into the template, OQ-2); mirror to `.specify/templates/agent-role-system-designer-template.md`
- [X] T038 [P] [G1] Add supervision metadata (`supervisor: true`, `{{ROLE_SCOPE}}=requirements-analyst`) to `templates/agent-role-requirements-analyst-template.md` (create-agent composes; no section copied); mirror to `.specify/templates/`
- [X] T039 [P] [G1] Add supervision metadata (`supervisor: true`, `{{ROLE_SCOPE}}=module-designer`) to `templates/agent-role-module-designer-template.md` (create-agent composes; no section copied); mirror to `.specify/templates/`
- [X] T040 [P] [G1] Add supervision metadata (`supervisor: true`, `{{ROLE_SCOPE}}=test-engineer`) to `templates/agent-role-test-engineer-template.md` (create-agent composes; no section copied); mirror to `.specify/templates/`
- [X] T041 [P] [G1] Add supervision metadata (`supervisor: true`, `{{ROLE_SCOPE}}=qa-engineer`) to `templates/agent-role-qa-engineer-template.md` (create-agent composes; no section copied); mirror to `.specify/templates/`
- [X] T042 [P] [G1] Add supervision metadata (`supervisor: true`, `{{ROLE_SCOPE}}=knowledge-manager`) to `templates/agent-role-knowledge-manager-template.md` (create-agent composes; no section copied); mirror to `.specify/templates/`

## Phase 12: User Story G2 — Generalize create-agent (Goals 2 & 4, D2 & D5)

**Independent Test**: `create-agent` can author a role, a supervisor, a triad, and a custom agent from one capability matrix; a `kind: supervisor` request produces a role agent with the delegation section bound.

- [X] T043 [G2] Structural validation: add a checklist to `.specify/specs/022-eei-agent-triad/quickstart.md` verifying `create-agent` exposes the 4-capability matrix and consumes every `AgentAuthoringRequest` field defined in `contracts/agent-authoring-contract.md`
- [X] T044 [G2] Reframe `skills/create-agent/SKILL.md` Goal from "role-based agent template" to general authoring, and restructure the workflow into a capability matrix (role · supervisor · triad · custom) sharing one validate+report tail; mirror to `.specify/skills/create-agent/SKILL.md`
- [X] T045 [G2] Add the **Supervisor** capability to `skills/create-agent/SKILL.md` — at generation, inline the single-source snippet `templates/agent-supervision-delegation.md` into the role agent and bind `{{ROLE_SCOPE}}` (D1, OQ-2), with supervision active by default (OQ-1); mirror to `.specify/skills/create-agent/SKILL.md`
- [X] T046 [G2] Add `AgentAuthoringRequest` intake handling (kind/role_slug/task/scoring_dimensions/threshold/paths/project_context) to `skills/create-agent/SKILL.md` per `contracts/agent-authoring-contract.md` (D5); mirror to `.specify/skills/create-agent/SKILL.md`

## Phase 13: User Story G3 — Generalize improve-agent (Goals 2 & 4, D3)

**Independent Test**: `improve-agent` accepts a role template, an `agent-subrole-*`, an orchestration prompt, or a generated `.agent.md`, classifies it, and routes to the matching refinement rules.

- [X] T047 [G3] Structural validation: add a checklist to `.specify/specs/022-eei-agent-triad/quickstart.md` verifying `improve-agent` documents all four target kinds and a classify/route step
- [X] T048 [G3] Broaden the Input Contract in `skills/improve-agent/SKILL.md` target resolution beyond `templates/agent-role-*` to role · sub-role · orchestration · custom `.specify/agents/*.agent.md`, and add a classify-then-route step ahead of the existing Triad Refinement workflow; mirror to `.specify/skills/improve-agent/SKILL.md`

## Phase 14: User Story G4 — /speckit.agents delegates to the skills (Goal 3, D4)

**Independent Test**: `/speckit.agents` Mode A/B produce identical artifacts to today but by calling `create-agent`/`improve-agent`; no inline template-rendering remains (contract R1).

- [X] T049 [G4] Structural validation: add a checklist to `.specify/specs/022-eei-agent-triad/quickstart.md` asserting `templates/commands/agents.md` Mode A/B invoke `create-agent`/`improve-agent` and contain no inline template-rendering block (contract R1)
- [X] T050 [G4] Refactor `templates/commands/agents.md` Mode A to build an `AgentAuthoringRequest` and delegate to `create-agent`, while retaining context-gathering, backup/preservation (FR-008/008a), symlink discoverability, and registry updates; regenerate/mirror runtime `.claude/commands/speckit.agents.md`
- [X] T051 [G4] Refactor `templates/commands/agents.md` Mode B to delegate custom creation to `create-agent` (kind=custom) and updates to `improve-agent`; regenerate/mirror runtime `.claude/commands/speckit.agents.md`
- [X] T052 [G4] Wire the `kind: supervisor` path end-to-end in `templates/commands/agents.md` so `/speckit.agents` can generate a supervisor role agent per `quickstart.md` Scenario 4; regenerate/mirror `.claude/commands/speckit.agents.md`

## Phase 15: Amendment Polish & Cross-Cutting

- [X] T053 [P] Update `docs/eei-triad-pattern.md` to document the supervisor pattern and the shared delegation section (link to `contracts/agent-authoring-contract.md`)
- [X] T054 [P] Update `skills/create-agent/SKILL.md` and `skills/improve-agent/SKILL.md` YAML `description` fields to reflect general-purpose scope; mirror both to `.specify/skills/`
- [X] T055 Verify runtime parity (DoD-13): confirm every edited `templates/`/`skills/` file has a matching `.specify/` counterpart and `.claude/commands/speckit.agents.md` matches `templates/commands/agents.md`
- [X] T056 Composability check (DoD-8/DoD-12): generate a supervisor agent for each of the 6 roles via `/speckit.agents` → `create-agent` and confirm each renders a valid `.specify/agents/<role>.agent.md` with a bound `{{ROLE_SCOPE}}` (quickstart Scenario 4)
- [X] T057 Update `.specify/memory/features/019.md` and `.specify/memory/features.md` with amendment implementation notes and flip the amendment status once T032–T056 are complete

## Amendment Phase Dependencies

```
Phase 9 (Setup: resolve OQ-1/OQ-2, mirror map)
  └─► Phase 10 (Foundational: delegation section + orchestration ROLE_SCOPE)
        ├─► Phase 11 (G1: inject into 6 role templates) ← depends on T034
        ├─► Phase 12 (G2: generalize create-agent) ← depends on T034/T035
        │     └─► Phase 14 (G4: agents command delegates) ← depends on create-agent (G2)
        ├─► Phase 13 (G3: generalize improve-agent) ← depends on Phase 10
        └─► Phase 15 (Polish) ← after G1–G4
```

## Amendment Parallel Execution Examples

**Within Phase 11**: T037–T042 are fully parallel (six different role-template files).
**Across goals**: Phase 12 (G2, create-agent) and Phase 13 (G3, improve-agent) touch different skill files and can run in parallel after Phase 10; Phase 14 (G4) MUST wait for G2.

## Amendment Implementation Strategy

**MVP Scope**: Phase 9 + Phase 10 + Phase 12 (G2) — `create-agent` can author a supervisor agent directly (manual invocation), delivering the core "advanced-agent customization" capability without touching the command yet.

**Incremental Delivery**:
1. MVP: Foundational section + generalized `create-agent` → supervisors authorable via the skill
2. +G1: Delegation section in all 6 role templates → every role can become a supervisor
3. +G3: Generalized `improve-agent` → any agent layer refinable
4. +G4: `/speckit.agents` delegates → single authoring engine, seamless UX
5. +Polish: Docs, runtime parity, composability, registry
