# Multi-Agent Orchestration Guide

## Overview

Spec Kit supports three orchestration patterns for coordinating multiple AI agents on complex tasks:

| Mode | Pattern | Best For |
|------|---------|----------|
| **Parallel Dispatch** | Territory isolation → Concurrent execution → Aggregation | Independent tasks with no shared state |
| **Serial Chain** | DAG definition → Topological execution → Progress tracking | Sequential phases with explicit dependencies |
| **Team Loop** | Team Supervisor (Meta) + Workers → Iterative quality loop | Quality-critical deliverables needing refinement |

Each mode addresses a different collaboration topology. They can also be composed — e.g., a Serial Chain where individual stages internally use Parallel Dispatch.

---

## Decision Tree

Use the following questions to select the right orchestration mode:

```
1. Are the tasks independent (no shared files, no ordering)?
   → YES: Use Parallel Dispatch
   → NO: Continue to Q2

2. Do tasks form a strict sequence (output of A feeds input of B)?
   → YES: Use Serial Chain
   → NO: Continue to Q3

3. Does the deliverable need iterative quality improvement?
   → YES: Use Team Loop
   → NO: Consider Serial Chain with parallel stages
```

**Quick heuristics:**
- 2–6 independent modules → Parallel Dispatch
- Pipeline with clear handoff artifacts → Serial Chain
- "Good enough" isn't acceptable, need convergence → Team Loop

---

## Parallel Dispatch Guide

**Entry**: `/speckit.agents` (intent: "并行", "parallel", "同时执行", "独立任务")
**Key Skill**: `organize-agents` (parallel mode)

### Territory Division Best Practices

Territory isolation is the foundation of conflict-free parallel execution:

1. **File-level ownership**: Each worker owns specific directories/files. No overlap allowed.
2. **Interface contracts**: Define shared interfaces upfront; workers implement behind the boundary.
3. **Shared dependencies**: Lock shared config files before dispatch; workers read but don't write.

Example territory map:
```yaml
workers:
  - agent: module-designer-auth
    territory: ["src/auth/", "tests/auth/"]
  - agent: module-designer-payments
    territory: ["src/payments/", "tests/payments/"]
shared_readonly: ["src/types/", "src/config/"]
```

### Parallel Count Recommendations

| Agent Count | Recommendation |
|-------------|----------------|
| 2–3 | Ideal for most projects. Low coordination overhead. |
| 4–6 | Good for large features with clear module boundaries. |
| 7+ | Avoid. Coordination overhead exceeds parallelism benefit. |

### Conflict Prevention Checklist

- [ ] Each worker has exclusive write access to its territory
- [ ] Shared types/interfaces are frozen before dispatch
- [ ] No two workers modify the same package.json dependencies section
- [ ] Integration test ownership is assigned to aggregation phase, not workers
- [ ] Workers output to designated handoff files for aggregation

### Example: 2 Modules in Parallel

**Goal**: Implement `auth` and `payments` modules simultaneously.

1. **Team Supervisor** (Lead) decomposes the feature into two independent modules.
2. **Territory assignment**: `auth` worker owns `src/auth/**`, `payments` worker owns `src/payments/**`.
3. **Dispatch**: Both workers start concurrently with their respective specs.
4. **Execution**: Each worker implements, writes tests, validates independently.
5. **Aggregation**: The Team Supervisor collects results, runs integration tests, produces unified report.

---

## Serial Chain Guide

**Entry**: `/speckit.agents` (intent: "阶段", "串行", "pipeline", "chain", "依次")
**Key Skill**: `organize-agents` (serial mode)

### Workflow DAG Design Principles

1. **Minimal stages**: Each stage should represent a meaningful transformation, not a trivial step.
2. **Clear input/output contracts**: Define what each stage produces and what the next stage expects.
3. **Idempotent stages**: A stage re-run with the same input should produce the same output.
4. **Checkpoint artifacts**: Each stage writes a durable artifact that enables resume-from-failure.

### blockedBy Dependency Management

Dependencies use a `blockedBy` field referencing upstream stage IDs:

```yaml
stages:
  - id: requirements
    agent: requirements-analyst
    blockedBy: []
  - id: design
    agent: system-designer
    blockedBy: [requirements]
  - id: implement
    agent: module-designer
    blockedBy: [design]
  - id: test
    agent: test-engineer
    blockedBy: [implement]
```

Rules:
- A stage only starts when ALL `blockedBy` dependencies are in `completed` status.
- Circular dependencies are rejected at DAG validation time.
- Stages with no `blockedBy` can start immediately (useful for parallel roots).

### File Handshake Protocol

The file handshake is how stages communicate context without token-heavy prompt chaining:

1. **Producer** writes output to a designated handoff file: `.specify/handoff/<stage-id>-output.md`
2. **Consumer** reads the handoff file at stage start, gaining full context.
3. **Metadata header** in each handoff file includes: stage ID, timestamp, status, confidence score.

Benefits:
- Drastically reduces token consumption (no need to pass full context in prompts).
- Enables resume: a crashed stage can re-read the previous handoff and continue.
- Provides audit trail: all intermediate artifacts are preserved.

### Example: 4-Stage Pipeline

**Goal**: Requirements → Design → Implementation → Testing

```
Stage 1: Requirements Analyst
  Input: User story / feature request
  Output: .specify/handoff/requirements-output.md (structured spec)

Stage 2: System Designer
  Input: requirements-output.md
  Output: .specify/handoff/design-output.md (architecture + interfaces)

Stage 3: Module Designer
  Input: design-output.md
  Output: .specify/handoff/implement-output.md (code changes + summary)

Stage 4: Test Engineer
  Input: implement-output.md + design-output.md
  Output: .specify/handoff/test-output.md (test results + coverage)
```

---

## Team Loop Guide

**Entry**: `/speckit.agents` (intent: "团队", "闭环", "自迭代", "持续优化")
**Key Skill**: `organize-agents` (team-loop mode)

> **Model alignment (Role × Stage × Type)**: a Team Loop is a **Loop** over a **Team** (the Role×Stage matrix). It has exactly **two layers** — a single **Team Supervisor** (Meta role) and its **Workers** — with the `executor`/`evaluator`/`optimizer` stages running under the Supervisor's control. The former separate Meta-Coordinator layer is merged into the Team Supervisor.

### Team Role Configuration

A Team Loop has **two layers**. Coordination and quality gating are unified in a single **Team Supervisor** (Meta role); the formerly separate Meta-Coordinator layer is merged into it.

| Layer | Responsibility | Example Agents |
|-------|---------------|----------------|
| **Team Supervisor** (Meta) | Task decomposition, worker dispatch, result collection, quality gating, convergence detection, iteration control | team-supervisor |
| **Workers** | Execute specific sub-tasks within their expertise (each runs the `executor` stage) | module-designer, test-engineer |

The Team Supervisor sits at the top: it decomposes and dispatches work to Workers, then evaluates the team output each iteration. Workers produce artifacts that flow back to the Team Supervisor for scoring.

### Quality Dimension Definition

Quality dimensions define what "good" looks like:

```yaml
quality_dimensions:
  - name: correctness
    weight: 0.4
    description: "Does the output correctly implement the specification?"
  - name: completeness
    weight: 0.3
    description: "Are all required elements present?"
  - name: clarity
    weight: 0.2
    description: "Is the output clear and well-structured?"
  - name: consistency
    weight: 0.1
    description: "Is the output internally consistent and aligned with project conventions?"
```

Weights must sum to 1.0. The Supervisor scores each dimension per iteration.

### Convergence Condition Design

The loop terminates when ANY of these conditions is met:

1. **Threshold reached**: Weighted score ≥ `threshold` (e.g., 0.85)
2. **Max iterations**: Loop count reaches `max_iterations` (e.g., 5)
3. **Regression detected**: Score decreases for `regression_limit` consecutive iterations (e.g., 2)

Design tips:
- Set threshold realistically — 0.80–0.90 for most tasks.
- Keep max_iterations low (3–5) to control costs.
- Regression limit of 2 prevents wasted iterations on diverging output.

### Example: Spec Writing Team Loop

**Goal**: Produce a high-quality API specification through iterative refinement.

```
Iteration 1:
  Writer (Worker) → drafts API spec
  Reviewer (Worker) → scores: correctness=0.6, completeness=0.5, clarity=0.7
  Supervisor → weighted score = 0.59 < threshold(0.85) → continue

Iteration 2:
  Optimizer (Worker) → addresses feedback, rewrites spec
  Reviewer (Worker) → scores: correctness=0.8, completeness=0.75, clarity=0.85
  Supervisor → weighted score = 0.79 < threshold(0.85) → continue

Iteration 3:
  Optimizer (Worker) → final refinements
  Reviewer (Worker) → scores: correctness=0.9, completeness=0.9, clarity=0.9
  Supervisor → weighted score = 0.90 ≥ threshold(0.85) → ACCEPT
```

---

## Model Selection Guidance

Different tasks within an orchestration have different cognitive requirements:

| Task Type | Characteristics | Recommended Model Tier |
|-----------|----------------|----------------------|
| **Deterministic** | Template filling, file copying, status tracking | Lightweight / fast model |
| **Judgment** | Code review, scoring, standard implementation | Standard model |
| **Deep Analysis** | Architecture design, complex debugging, novel problem-solving | High-capability model |

### Mapping to Orchestration Roles

- **Team Supervisor** (dispatch/aggregation + quality scoring, convergence): Standard to High — structural coordination plus judgment
- **Workers** (implementation, testing — `executor` stage): Standard — requires coding ability
- **Evaluator** (`evaluator` stage, rubric scoring): Standard — structured evaluation
- **Optimizer** (`optimizer` stage, rewriting based on feedback): Standard — targeted modifications

### Cost Optimization Rule

> Use the cheapest model that reliably produces correct output for each role.

For a team of 5 agents running 3 iterations, using lightweight models where possible can reduce total token cost by 40–60% compared to using high-capability models everywhere.

---

## Cost Control Best Practices

### 1. File Handshake Over Prompt Chaining

Instead of passing full context between agents in prompts:
- Write artifacts to `.specify/handoff/` files
- Downstream agents read only what they need
- **Savings**: 50–80% token reduction per stage transition

### 2. Appropriate Parallelism

- More workers ≠ faster results if coordination overhead dominates
- Sweet spot: 2–4 parallel workers for most tasks
- Each additional worker adds aggregation complexity

### 3. Confidence Score Filtering

- Workers report confidence scores with their output
- Supervisor can skip full re-evaluation for high-confidence results (>0.9)
- Low-confidence results (<0.6) get priority review
- **Savings**: 20–30% fewer evaluation cycles

### 4. Early Termination

- If first iteration scores >0.9, accept immediately (no need for more iterations)
- If two consecutive iterations show regression, abort and report
- Set aggressive `max_iterations` (3–5, not 10+)

### 5. Incremental Improvement

- Optimizer should only rewrite low-scoring sections, not the entire artifact
- Provide delta feedback (what changed, what's still wrong) not full rubrics each time
- **Savings**: 30–50% token reduction in improvement cycles

---

## Troubleshooting

### Common Issues

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| File conflicts in parallel dispatch | Overlapping territory definitions | Audit territory map; ensure exclusive ownership |
| Stage stuck in "blocked" state | Upstream stage failed silently | Check handoff file exists; re-run upstream stage |
| Team loop never converges | Threshold too high or dimensions conflicting | Lower threshold or adjust dimension weights |
| Score oscillates without improving | Optimizer and Evaluator disagree on quality | Align scoring rubric with improvement instructions |
| Excessive token usage | Full context passed in prompts | Switch to file handshake protocol |
| Worker produces empty output | Missing input context | Verify handoff file is populated before dispatch |

### Debugging Steps

1. **Check handoff files**: Verify `.specify/handoff/` contains expected artifacts from each stage.
2. **Review iteration history**: Team Loop logs scores per iteration — look for patterns.
3. **Validate territory map**: For parallel dispatch, ensure no file is claimed by multiple workers.
4. **Test single-agent first**: Run one worker in isolation to verify it works before orchestrating.
5. **Reduce scope**: If a complex orchestration fails, simplify (fewer stages, fewer workers) and rebuild.

### Recovery Strategies

- **Parallel Dispatch failure**: Re-dispatch only the failed worker; successful workers' output is preserved.
- **Serial Chain failure**: Resume from the last successful stage (checkpoint artifacts enable this).
- **Team Loop divergence**: Reset to the highest-scoring iteration's artifact and retry with adjusted dimensions.
