# Data Model: EEI Agent Triad

## Entities

### Triad

A configured set of three sub-agent definitions bound to a single Role-Based Agent.

| Field | Type | Description |
|-------|------|-------------|
| role | string | The parent role this triad belongs to (e.g., "system-designer") |
| executor | SubAgentConfig | Configuration for the Executor sub-agent |
| evaluator | SubAgentConfig | Configuration for the Evaluator sub-agent |
| improver | SubAgentConfig | Configuration for the Improver sub-agent |
| scoring | ScoringConfig | Scoring dimensions and threshold |
| limits | LoopLimits | Iteration limits and convergence rules |

### SubAgentConfig

Configuration for a single sub-agent within the triad.

| Field | Type | Description |
|-------|------|-------------|
| template | string | Path to the sub-role template (e.g., `agent-subrole-executor-template.md`) |
| environment_paths | string[] | File paths the agent reads (skills, instructions, templates) |
| workspace_paths | string[] | File paths the agent is allowed to modify (improver only) |
| prompt_context | string | Additional context injected into the agent's prompt each iteration |

### ScoringConfig

Defines what "quality" means for a specific task.

| Field | Type | Description |
|-------|------|-------------|
| dimensions | Dimension[] | Named scoring criteria with weights |
| threshold | number | Score above which the loop stops (e.g., 90) |
| output_format | string | Expected output format from evaluator (structured text) |

### Dimension

A single scoring criterion.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Criterion name (e.g., "correctness", "aesthetics") |
| weight | number | Weight as decimal (e.g., 0.6 for 60%) |
| description | string | What this dimension evaluates |

### LoopLimits

Controls for the iteration loop.

| Field | Type | Description |
|-------|------|-------------|
| max_iterations | number | Hard limit on iterations (default: 20) |
| max_consecutive_regressions | number | Stop after N regressions in a row (default: 3) |
| warn_at_percentage | number | Warn user at this % of max_iterations (default: 50) |

### Iteration

One complete cycle of Executor → Evaluator (→ optional Improver).

| Field | Type | Description |
|-------|------|-------------|
| round | number | Iteration number (1-based) |
| executor_output | string[] | Paths to files produced by the executor |
| scores | DimensionScore[] | Per-dimension scores from evaluator |
| weighted_total | number | Weighted total score |
| suggestions | string[] | Improvement suggestions from evaluator |
| changes_made | Change[] | Changes made by improver (empty if score met threshold) |
| delta | number | Score change from previous iteration |

### DimensionScore

Score for a single dimension in one iteration.

| Field | Type | Description |
|-------|------|-------------|
| dimension | string | Dimension name |
| score | number | Score 0-100 |

### Change

A modification made by the improver.

| Field | Type | Description |
|-------|------|-------------|
| type | enum | "environment" or "executor" |
| target | string | File path (environment) or "prompt" (executor) |
| description | string | What was changed and why |

### IterationHistory

Ordered log of all iterations.

| Field | Type | Description |
|-------|------|-------------|
| triad_id | string | Identifier for the triad run |
| goal | string | The user's quality goal description |
| iterations | Iteration[] | All completed iterations |
| best_iteration | number | Round number with highest weighted_total |
| converged | boolean | Whether the threshold was met |
| total_duration | string | Total time across all iterations |

### RoleSupervisor *(added by Plan Amendment 2026-07-02)*

A role-based agent that can act as an orchestrator, dynamically spawning a role-scoped EEI triad for quality-gated deliverables. Produced by `create-agent` (Supervisor capability) and generated via `/speckit.agents`.

| Field | Type | Description |
|-------|------|-------------|
| role_slug | string | The role this supervisor embodies (e.g., `system-designer`) |
| supervisor | boolean | Whether the delegation loop is active (`supervisor: true` in frontmatter) or dormant |
| role_scope | string | The domain binding passed to the triad (`{{ROLE_SCOPE}}`) — constrains the executor's task and the evaluator's default dimensions to the role |
| default_dimensions | Dimension[] | Role-appropriate default scoring dimensions the supervisor uses unless overridden per task |
| triad | Triad \| null | The embedded triad configuration; null when `supervisor` is false |

### AgentAuthoringRequest *(added by Plan Amendment 2026-07-02)*

The input `/speckit.agents` passes to `create-agent`/`improve-agent` when delegating authoring (contract in `contracts/agent-authoring-contract.md`).

| Field | Type | Description |
|-------|------|-------------|
| kind | enum | `role` \| `supervisor` \| `triad` \| `custom` |
| role_slug | string | Target role (for `role`/`supervisor`) |
| task | string | Task description (for `supervisor`/`triad`) |
| scoring_dimensions | Dimension[] | Weighted quality axes (for `supervisor`/`triad`) |
| threshold | number | Acceptance threshold |
| max_iterations | number | Loop cap (default 20) |
| environment_paths | string[] | Reference paths the executor reads |
| workspace_paths | string[] | Paths the improver may edit |
| project_context | object | Gathered `{{PLACEHOLDER}}` values from the command |

## Relationships

```
Triad 1--3 SubAgentConfig    (executor, evaluator, improver)
Triad 1--1 ScoringConfig
Triad 1--1 LoopLimits
ScoringConfig 1--* Dimension
IterationHistory 1--* Iteration
Iteration 1--* DimensionScore
Iteration 0--* Change
RoleSupervisor 0..1--1 Triad  (optional embedded triad; amendment)
RoleSupervisor 1--* Dimension (default_dimensions; amendment)
AgentAuthoringRequest 1--1 RoleSupervisor|Triad  (request produces one artifact; amendment)
```

## State Transitions

```
[Idle] → (start goal) → [Running]
[Running] → (executor complete) → [Evaluating]
[Evaluating] → (score ≥ threshold) → [Converged]
[Evaluating] → (score < threshold, iterations < max) → [Improving]
[Evaluating] → (iterations = max) → [MaxReached]
[Improving] → (improvements applied) → [Running]
[Converged] → [Done]
[MaxReached] → [Done]
```
