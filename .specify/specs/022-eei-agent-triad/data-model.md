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

## Relationships

```
Triad 1--3 SubAgentConfig    (executor, evaluator, improver)
Triad 1--1 ScoringConfig
Triad 1--1 LoopLimits
ScoringConfig 1--* Dimension
IterationHistory 1--* Iteration
Iteration 1--* DimensionScore
Iteration 0--* Change
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
