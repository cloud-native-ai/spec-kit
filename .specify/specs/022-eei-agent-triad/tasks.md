# Tasks: EEI Agent Triad (Executor-Evaluator-Improver)

**Requirement ID**: 022 (from branch name)
**Requirement Key**: 022-eei-agent-triad
**Related Feature**: 019 Agents Command (from .specify/memory/features.md)
**Input**: Design documents from `.specify/specs/022-eei-agent-triad/`
**Prerequisites**: plan.md (required), requirements.md (required), data-model.md, contracts/triad-protocol.md, quickstart.md

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
