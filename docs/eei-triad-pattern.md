# EEI Triad Pattern: Executor-Evaluator-Improver

A quality optimization pattern for AI agent workflows. Instead of running a task once and accepting the result, the triad iteratively improves output until a measurable quality threshold is met.

## Pattern Overview

The EEI triad decomposes a quality-sensitive task into three independent sub-agents coordinated by an orchestrator:

```
Orchestrator
 |
 |  1. Invoke         2. Score output      3. Improve env
 |  ┌──────────┐     ┌───────────┐       ┌──────────┐
 +->| Executor |---->| Evaluator |------>| Improver |--+
    | (do work)|     | (judge)   |       | (refine) |  |
    └──────────┘     └───────────┘       └──────────┘  |
         ^                                              |
         └──────── loop until score > threshold ────────┘
```

**Use when**: the task has measurable quality dimensions, output quality matters more than latency, and iterative refinement is feasible (the executor can re-run with an updated environment).

## Architecture

### Three Sub-Agents

| Role | Receives | Produces | Writes to disk |
|------|----------|----------|----------------|
| **Executor** | Task prompt + environment files (skills, templates, instructions) | Output artifacts (files, images, code) | Output directory only |
| **Evaluator** | Output artifacts + scoring dimensions with weights | Per-dimension scores, weighted total, specific suggestions | Nothing |
| **Improver** | Evaluator feedback (scores + suggestions) | Edits to environment files + executor context adjustments | Skill/reference files only |

### Isolation Rules

- Each sub-agent is spawned as an **independent subagent** with its own context. No shared conversation state.
- The evaluator never sees the executor's prompt or reasoning -- only the output artifacts.
- The improver never sees the executor's internal state -- only the evaluator's structured feedback.
- The executor re-reads all environment files from disk at each iteration (no caching from prior runs).

## The Loop

The orchestrator manages a simple state machine:

1. **Invoke Executor** with the task prompt and current environment files.
2. **Invoke Evaluator** with the executor's output artifacts and scoring criteria.
3. **Check threshold**: if `weighted_total >= threshold`, stop and return output.
4. **Check iteration limit**: if `round >= max_iterations` (default 20), stop and return the best-scoring output.
5. **Invoke Improver** with the evaluator's feedback. The improver edits environment files on disk.
6. **Go to step 1**.

The orchestrator tracks the best-scoring output across all rounds. If the threshold is never met, it returns the best result found.

## Key Principles

**Context Isolation** -- Each sub-agent gets a clean context per invocation. This prevents the evaluator from being biased by the executor's reasoning and ensures the executor genuinely re-reads improved environment files rather than relying on stale cached context.

**Dual-Target Improvement** -- The improver modifies two things: (a) the executor's *environment* (skill reference files, best practices, style configs) and (b) the executor's *prompt context* (adding constraints, examples, or corrections). Environment changes persist on disk; prompt changes are passed through the orchestrator.

**Convergent Optimization** -- Improvement is directional. The improver maps each evaluator suggestion to a concrete file edit or prompt adjustment. Regressions are tracked; after 3 consecutive score drops, the system reverts to the best-known state and tries a different strategy.

**Best-Output Tracking** -- The orchestrator preserves the highest-scoring output across all iterations, so a late regression never loses earlier progress.

## Usage Examples

### Diagram Drawing

```
Executor:  Draw a K8s architecture diagram in PlantUML, render to PNG
Evaluator: Score on correctness (60%) + aesthetics (40%), threshold 90
Improver:  Edit PlantUML skill howto/best-practices files based on feedback

Round 1:  Score 49 -- "missing Ingress, arrow congestion"
Round 5:  Score 72 -- "layout improved, color coding inconsistent"
Round 17: Score 91 -- threshold met, done
```

### Code Review

```
Executor:  Write code implementing a feature
Evaluator: Score on correctness (50%) + security (30%) + style (20%), threshold 85
Improver:  Update coding guidelines and security checklist

Round 1: Score 58 -- "SQL injection vulnerability in query builder"
Round 2: Score 74 -- "style violations in error handling"
Round 3: Score 92 -- threshold met, done
```

### Document Writing

```
Executor:  Write API reference documentation
Evaluator: Score on completeness (40%) + clarity (30%) + accuracy (30%), threshold 85
Improver:  Update writing guidelines and add missing topic context

Round 1: Score 61 -- "missing authentication section, jargon-heavy"
Round 3: Score 87 -- threshold met, done
```

## Lessons Learned

From the K8s diagram optimization session (49 to 91 over 17 rounds):

- **Environment improvement > prompt tweaking**: Editing the skill reference files (best practices, layout howto) produced larger and more durable score gains than adjusting the executor's prompt alone.
- **Scoring variability is real**: LLM-based evaluators have natural variability of roughly plus or minus 3 points. Set thresholds with this margin in mind.
- **Diminishing returns above 85**: The jump from 49 to 72 took 5 rounds; from 72 to 91 took 12. Plan iteration budgets accordingly.
- **Specific feedback drives convergence**: Vague evaluator suggestions ("improve layout") led to minimal gains. Specific suggestions ("reduce arrow crossings by grouping related services") drove measurable improvement.
- **File diffs are essential**: Logging exactly what the improver changed each round made it possible to identify which edits helped and which caused regressions.

## When NOT to Use

- **Simple one-shot tasks**: If the task does not benefit from iteration (e.g., "list files in a directory"), the overhead of three sub-agents is wasteful.
- **Tasks without measurable quality criteria**: If you cannot define scoring dimensions and weights, the evaluator has nothing to score and the loop cannot converge.
- **Latency-sensitive workflows**: Each round spawns three sub-agents. If you need a response in seconds, use a single agent.
- **Deterministic tasks**: If the output is either correct or incorrect with no gradient (e.g., "what is 2+2?"), there is nothing for the improver to refine.

## Template Reference

The full specification and examples live in the spec directory:

- **Requirements**: `.specify/specs/022-eei-agent-triad/requirements.md`
- **Quickstart**: `.specify/specs/022-eei-agent-triad/quickstart.md`
- **Tasks**: `.specify/specs/022-eei-agent-triad/tasks.md`
- **Plan**: `.specify/specs/022-eei-agent-triad/plan.md`
