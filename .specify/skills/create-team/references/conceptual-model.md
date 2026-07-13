# Conceptual Model: Role × Stage × Type + Team/Loop

**Owner**: the team domain (`create-team` / `/speckit.team`). This file is the **single source of truth** for the multi-agent conceptual model (FR-011, FR-012, SC-006). Single-agent skills (`create-agent`, `improve-agent`) MUST link here rather than re-defining any part of this model.

## The three orthogonal dimensions

Every agent participating in a team is described by three orthogonal dimensions:

- **Role** — the responsibility/perspective (e.g. `system-designer`, `test-engineer`, `team-supervisor`); maps to exactly one `agent-role-<role>-template.md`.
- **Stage** — one of `executor`, `evaluator`, `optimizer` (canonical names; the deprecated dimension name "SubRole" and stage name "improver" are removed).
- **Type** — `Worker` or `Meta`, **derived from Stage** (Type-follows-Stage): `executor → Worker`, `evaluator → Meta`, `optimizer → Meta`.

## Static vs Dynamic structure

- **Team (static structure)** — a **Role × Stage × Type** matrix describing the roster: which agents participate, in what role, at what stage, and of what type. This is what a persisted team's `## Static Structure` section renders.
- **Loop (dynamic structure)** — the runtime collaboration pattern: how the roster executes (parallel / serial / team-loop), its parallelism/DAG/iteration settings, and the execution flow (dispatch → handoff → loop edges). This is what a persisted team's `## Dynamic Structure` section renders.

## The Team Supervisor (single Meta role)

- **Team Supervisor** is the single **Meta role** — Meta at all stages, and it never performs real project tasks.
- It is the merge of the former **Meta-Coordinator** (task decomposition + worker dispatch) and the **Team Supervisor** (quality gating + iteration control). There is **no separate Meta-Coordinator** role.
- A `team-loop` team MUST include **exactly one** Team Supervisor.

## Collaboration patterns (the dynamic structure)

| Pattern | Static shape | Dynamic behavior |
|---------|--------------|------------------|
| **parallel** | independent Workers with disjoint territories | dispatched together (one response, many delegations); conflict-free write scopes |
| **serial** | an ordered chain of stages/roles | each stage's output feeds the next via file-path-only handoff; DAG, no cycles |
| **team-loop** | Workers + exactly one Team Supervisor | Supervisor decomposes → Workers execute → Supervisor scores → iterate until threshold or cap |

## Lifecycle: temporary vs persistent members

- **temporary** — a worker/stage agent instantiated for a single run from a stage/worker template; discarded when the run ends. Lives only in the orchestrator's context.
- **persistent** — a reusable agent stored at `.specify/agents/<slug>.agent.md` and symlinked into each supported tool.

## Template home

The multi-agent authoring templates (team-supervisor, the three EEI stages, and the parallel/serial/triad orchestration templates + workflow schema) live in `skills/create-team/templates/` (installed mirror: `.specify/skills/create-team/templates/`). The single-agent role/supervisor/custom templates remain in `skills/create-agent/templates/`.
