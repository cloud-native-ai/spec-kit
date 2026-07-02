# EEI Triad Orchestration Protocol

## Overview

This contract defines the interaction protocol between the orchestrator (main agent) and the three sub-agents (Executor, Evaluator, Improver) in an EEI triad loop.

## Protocol Flow

```
Orchestrator
  │
  ├─1─► Executor (fresh context, reads environment files)
  │       └─► produces: output artifacts (files, images)
  │
  ├─2─► Evaluator (fresh context, reads ONLY output artifacts)
  │       └─► produces: structured score + suggestions
  │
  ├─3─► [if score < threshold] Improver (fresh context, reads ONLY evaluator feedback)
  │       └─► produces: file edits (environment) + prompt adjustments (executor)
  │
  └─4─► [loop back to step 1 with updated environment]
```

## Contract: Executor Sub-Agent

### Input (provided by orchestrator)

| Field | Required | Description |
|-------|----------|-------------|
| task_description | MUST | What to produce (e.g., "draw a K8s architecture diagram") |
| environment_paths | MUST | List of file paths to read for reference (skills, howtos, templates) |
| output_directory | MUST | Where to write output artifacts |
| iteration_context | SHOULD | Brief note on what changed since last iteration (empty on first run) |

### Output (returned to orchestrator)

| Field | Required | Description |
|-------|----------|-------------|
| artifact_paths | MUST | List of file paths produced |
| status | MUST | "success" or "error" with description |

### Constraints

- MUST read all `environment_paths` at the start of each invocation
- MUST NOT receive evaluator feedback directly
- MUST NOT retain state from previous iterations

## Contract: Evaluator Sub-Agent

### Input (provided by orchestrator)

| Field | Required | Description |
|-------|----------|-------------|
| artifact_paths | MUST | Paths to executor's output artifacts |
| scoring_dimensions | MUST | Array of `{name, weight, description}` |
| evaluation_guidelines | SHOULD | Additional criteria or style preferences |

### Output (returned to orchestrator)

The evaluator MUST produce output in this exact format:

```
DIMENSION_1_SCORE: [0-100]
DIMENSION_1_NOTES: [brief assessment]
DIMENSION_2_SCORE: [0-100]
DIMENSION_2_NOTES: [brief assessment]
WEIGHTED_TOTAL: [calculated weighted sum]
SUGGESTIONS: [numbered list of specific improvements]
```

### Constraints

- MUST NOT receive the executor's prompt, reasoning, or conversation history
- MUST NOT receive the improver's previous changes
- MUST evaluate based solely on the artifacts provided
- MUST provide specific, actionable suggestions (not vague directives)

## Contract: Improver Sub-Agent

### Input (provided by orchestrator)

| Field | Required | Description |
|-------|----------|-------------|
| evaluator_feedback | MUST | The evaluator's full structured output (scores + suggestions) |
| environment_paths | MUST | File paths available for modification |
| workspace_paths | MUST | Subset of environment_paths that the improver is allowed to edit |
| iteration_history | SHOULD | Summary of previous iterations (scores, changes) for convergence awareness |

### Output (returned to orchestrator)

| Field | Required | Description |
|-------|----------|-------------|
| environment_changes | MUST | List of `{file_path, description}` for files modified |
| executor_adjustments | SHOULD | Suggested prompt/context changes for next executor invocation |
| rationale | MUST | Brief explanation of why these changes should improve the score |

### Constraints

- MUST only modify files within `workspace_paths`
- MUST NOT modify the executor's core identity or role
- MUST NOT communicate directly with the executor or evaluator
- MUST document every change with rationale

## Orchestrator Responsibilities

The orchestrator (main agent managing the loop) MUST:

1. **Initialize**: Parse triad configuration, set up scoring dimensions and limits
2. **Invoke Executor**: Pass task description + environment paths; collect artifacts
3. **Invoke Evaluator**: Pass ONLY artifacts + scoring config; collect structured scores
4. **Check Threshold**: Compare weighted_total against threshold
5. **Track History**: Record iteration data (scores, changes, deltas)
6. **Invoke Improver** (if needed): Pass ONLY evaluator feedback + workspace paths; apply changes
7. **Check Limits**: Enforce max_iterations and max_consecutive_regressions
8. **Report**: Present final results with iteration history summary

## Stopping Conditions

The loop MUST stop when ANY of these conditions is met:

| Condition | Action |
|-----------|--------|
| `weighted_total > threshold` | Report success with converged output |
| `iteration_count >= max_iterations` | Report best-scoring output with warning |
| `consecutive_regressions >= max_consecutive_regressions` | Revert to best state, report with warning |
| Executor or evaluator returns error | Report error, preserve last good output |
