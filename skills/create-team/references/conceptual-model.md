# Conceptual Model: Role × Stage × Type + Team/Loop

**Owner**: the team domain (`create-team` / `/speckit.team`). This file is the **single source of truth** for the multi-agent conceptual model (FR-011, FR-012, SC-006). Single-agent skills (`create-agent`, `improve-agent`) MUST link here rather than re-defining any part of this model.

## The three orthogonal dimensions

Every agent participating in a team is described by three orthogonal dimensions:

- **Role** — the responsibility/perspective (e.g. `system-designer`, `test-engineer`, `team-supervisor`); maps to exactly one `agent-role-<role>-template.md`.
- **Stage** — one of `executor`, `evaluator`, `optimizer` (canonical names; the deprecated dimension name "SubRole" and stage name "improver" are removed).
- **Type** — `Worker` or `Meta`, **derived from Stage** (Type-follows-Stage): `executor → Worker`, `evaluator → Meta`, `optimizer → Meta`.

## Static vs Dynamic structure

- **Team (static structure)** — a **Role × Stage × Type** matrix describing the roster: which agents participate, in what role, at what stage, and of what type. This is what a persisted team's `## Static Structure` section renders.
- **Loop (dynamic structure)** — the runtime collaboration pattern: how the roster executes (parallel / serial / iteration / continuous), its parallelism/DAG/iteration/operating settings, and the execution flow (dispatch → handoff → loop edges). This is what a persisted team's `## Dynamic Structure` section renders.

## The Team Supervisor (single Meta role)

- **Team Supervisor** is the single **Meta role** — Meta at all stages, and it never performs real project tasks.
- It is the merge of the former **Meta-Coordinator** (task decomposition + worker dispatch) and the **Team Supervisor** (quality gating + iteration control). There is **no separate Meta-Coordinator** role.
- An `iteration` or `continuous` team MUST include **exactly one** Team Supervisor; a `parallel`/`serial` team MAY use one as the Lead / quality gate.

## Collaboration patterns (the dynamic structure)

The team domain has **four** collaboration patterns. Each encodes a different **priority**; the goal decides which one fits. The first three are **bounded** (they run once and stop); `continuous` is **unbounded** (it operates indefinitely on a cadence).

| Pattern | Priority | Static shape | Dynamic behavior | Lifecycle |
|---------|----------|--------------|------------------|-----------|
| **parallel** | 效率优先 (throughput) | independent Workers with disjoint territories | dispatched together (one response, many delegations); conflict-free write scopes | bounded — ends when all territories complete and results aggregate |
| **serial** | 质量优先 (quality) | an ordered chain of stages/roles | each stage's output feeds the next via file-path-only handoff; DAG, no cycles; a **simple verification between each step and its predecessor** guards every handoff | bounded — slower, but ends only when the final stage passes its gate |
| **iteration** | 目标收敛 (converge) | Workers + exactly one Team Supervisor | Supervisor decomposes → Workers execute → Supervisor scores → iterate until threshold or cap | bounded — converges to the goal, then delivers and stops |
| **continuous** | 长期运营 (operate) | Workers + exactly one Team Supervisor + operating discipline | runs on a **cadence**; each cycle reads constraints + budget, acts, **independently verifies**, scores, critiques, and updates a cross-run state spine | unbounded — runs indefinitely at a maturity level (L1→L2→L3), bounded per cycle by budget / circuit-breaker / kill-switch |

- **`continuous`** is the long-lived operating form — its discipline lives in [`operating-loops.md`](operating-loops.md).
- `iteration` maps to a **one-time** optimization goal; `continuous` maps to a **continuous** one (see [`optimization-goals.md`](optimization-goals.md)).

## Lifecycle: temporary vs persistent members

- **temporary** — a worker/stage agent instantiated for a single run from a stage/worker template; discarded when the run ends. Lives only in the orchestrator's context.
- **persistent** — a reusable agent stored at `.specify/agents/<slug>.agent.md` and symlinked into each supported tool.

## Template home

The multi-agent authoring templates (team-supervisor, the three EEI stages, and the parallel/serial/triad orchestration templates + workflow schema) live in `skills/create-team/templates/` (installed mirror: `.specify/skills/create-team/templates/`). The single-agent role/supervisor/custom templates remain in `skills/create-agent/templates/`. The `continuous` operating discipline is documented in [`operating-loops.md`](operating-loops.md).
