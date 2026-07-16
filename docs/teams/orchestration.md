# Team Orchestration Guide

Operational guide for coordinating multiple agents through the team domain. Every mode is
entered through the single `/speckit.team` command and executed by the `create-team` skill.

> **Scope**: this is the **doc-level operational guide**. The normative single source of truth
> is the skill references — [`conceptual-model.md`](../../skills/create-team/references/conceptual-model.md)
> (the Role × Stage × Type model and the four patterns) and, for the long-lived operating form,
> [`continuous-operations.md`](./continuous-operations.md) (which points to
> [`operating-loops.md`](../../skills/create-team/references/operating-loops.md)). When this guide
> and a reference disagree, the reference wins.

## Overview

The team domain supports **four** collaboration patterns. Each encodes a different **priority** —
the team's [goal](./overview.md) decides which one fits. The first three are **bounded** (run once
and stop); `continuous` is **unbounded** (operates indefinitely on a cadence).

| Pattern | Priority | Best for | Lifecycle |
|---------|----------|----------|-----------|
| **parallel** | 效率优先 (throughput) | Independent tasks with no shared state — split work across disjoint territories | bounded |
| **serial** | 质量优先 (quality) | Sequential phases with explicit dependencies where each handoff must be checked | bounded |
| **iteration** | 目标收敛 (converge) | Quality-critical deliverables that must be refined until they meet a threshold | bounded |
| **continuous** | 长期运营 (operate) | Standing work that arrives forever (CI failures, new PRs/issues) or a quality that must be kept up long-term | unbounded |

Patterns can be **composed** — e.g. a serial chain whose individual stages internally use parallel
dispatch, or a continuous team whose per-cycle work is an iteration loop.

> `continuous` carries a full operating discipline (maturity, budget, independent verification,
> a cross-run state spine); it lives in [continuous-operations.md](./continuous-operations.md).

---

## Decision Tree

```
1. Does this work arrive continuously / must a quality be kept up long-term?
   ("持续", "不断", "长期维持", "每天/每次", CI/PR/issue streams)
   → YES: Use continuous  (see continuous-operations.md)
   → NO: Continue to Q2

2. Are the tasks independent (no shared files, no ordering)?
   → YES: Use parallel        (priority: throughput)
   → NO: Continue to Q3

3. Do tasks form a strict sequence (output of A feeds input of B), and does each
   handoff need to be verified before the next stage starts?
   → YES: Use serial          (priority: quality)
   → NO: Continue to Q4

4. Does one deliverable need iterative quality improvement until it converges?
   → YES: Use iteration       (priority: convergence)
   → NO: Reconsider — a serial chain with parallel stages usually fits
```

**Quick heuristics:**
- 2–6 independent modules → **parallel**
- Pipeline with clear handoff artifacts, each checked → **serial**
- "Good enough" isn't acceptable, need convergence to a threshold → **iteration**
- Work never ends / a quality must be maintained → **continuous**

---

## Parallel Dispatch (priority: 效率优先 / throughput)

**Entry**: `/speckit.team` (intent: "并行", "parallel", "同时执行", "独立任务")
**Skill**: `create-team` (parallel mode)

Parallel dispatch chases **maximum throughput** by running many independent Workers at once.
It is conflict-free only when territories are disjoint.

### Territory Division Best Practices

1. **File-level ownership**: Each worker owns specific directories/files. No overlap allowed.
2. **Interface contracts**: Define shared interfaces upfront; workers implement behind the boundary.
3. **Shared dependencies**: Lock shared config files before dispatch; workers read but don't write.

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
- [ ] No two workers modify the same `package.json` dependencies section
- [ ] Integration test ownership is assigned to the aggregation phase, not workers
- [ ] Workers output to designated handoff files for aggregation

### Example: 2 Modules in Parallel

**Goal**: Implement `auth` and `payments` modules simultaneously.

1. The **Lead** (optionally a Team Supervisor) decomposes the feature into two independent modules.
2. **Territory assignment**: `auth` worker owns `src/auth/**`, `payments` worker owns `src/payments/**`.
3. **Dispatch**: Both workers start concurrently with their respective specs.
4. **Execution**: Each worker implements, writes tests, validates independently.
5. **Aggregation**: The Lead collects results, runs integration tests, produces a unified report.

---

## Serial Chain (priority: 质量优先 / quality)

**Entry**: `/speckit.team` (intent: "阶段", "串行", "pipeline", "chain", "依次")
**Skill**: `create-team` (serial mode)

Serial chain trades speed for **quality**: stages run strictly in dependency order, and a
**simple verification between each step and its predecessor** guards every handoff. It is slower
than parallel, but nothing advances on an unverified artifact.

### Workflow DAG Design Principles

1. **Minimal stages**: Each stage should represent a meaningful transformation, not a trivial step.
2. **Clear input/output contracts**: Define what each stage produces and what the next expects.
3. **Idempotent stages**: A stage re-run with the same input should produce the same output.
4. **Checkpoint artifacts**: Each stage writes a durable artifact that enables resume-from-failure.

### `blockedBy` Dependency Management

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

### Step Verification (the quality guard)

Because serial chain is **quality-first**, each stage runs a **simple verification against its
predecessor's handoff before it begins its own work**:

- Confirm the upstream handoff file exists and is non-empty.
- Confirm its metadata header (stage ID, status `completed`, confidence score) is present and sane.
- Confirm the required inputs for this stage are actually contained in the handoff.
- On failure, do **not** proceed — report and (optionally) re-run the upstream stage.

This is deliberately lightweight (a gate, not a full evaluator). For heavyweight, scored
convergence use the **iteration** pattern instead.

### File Handshake Protocol

The file handshake lets stages communicate context without token-heavy prompt chaining:

1. **Producer** writes output to a designated handoff file: `.specify/handoff/<stage-id>-output.md`
2. **Consumer** reads the handoff file at stage start (and runs the step verification above).
3. **Metadata header** in each handoff file includes: stage ID, timestamp, status, confidence score.

Benefits: drastically reduced token consumption, resume-from-failure, and a full audit trail.

### Example: 4-Stage Pipeline

```
Stage 1: Requirements Analyst
  Input: User story / feature request
  Output: .specify/handoff/requirements-output.md (structured spec)

Stage 2: System Designer
  Verify: requirements-output.md exists, status=completed
  Input: requirements-output.md
  Output: .specify/handoff/design-output.md (architecture + interfaces)

Stage 3: Module Designer
  Verify: design-output.md exists, interfaces present
  Input: design-output.md
  Output: .specify/handoff/implement-output.md (code changes + summary)

Stage 4: Test Engineer
  Verify: implement-output.md exists, summary present
  Input: implement-output.md + design-output.md
  Output: .specify/handoff/test-output.md (test results + coverage)
```

---

## Iteration (priority: 目标收敛 / converge)

**Entry**: `/speckit.team` (intent: "团队", "闭环", "自迭代", "收敛", "持续优化 [一次性]")
**Skill**: `create-team` (iteration mode)

> **Model alignment (Role × Stage × Type)**: an iteration team is a **Loop** over a **Team** (the
> Role×Stage matrix). It has exactly **two layers** — a single **Team Supervisor** (Meta role) and
> its **Workers** — with the `executor`/`evaluator`/`optimizer` stages running under the Supervisor's
> control. The per-role quality loop it builds on is documented in
> [quality-loop.md](../agents/quality-loop.md).

Iteration exists to **converge one deliverable to a measurable quality threshold**. It maps to a
**one-time** optimization goal (raise X from A to B, then deliver and stop). For a quality that must
be maintained forever, use **continuous** instead.

### Team Role Configuration

An iteration team has **two layers**. Coordination and quality gating are unified in a single
**Team Supervisor** (Meta role); the formerly separate Meta-Coordinator layer is merged into it.

| Layer | Responsibility | Example Agents |
|-------|---------------|----------------|
| **Team Supervisor** (Meta) | Task decomposition, worker dispatch, result collection, quality gating, convergence detection, iteration control | team-supervisor |
| **Workers** | Execute specific sub-tasks within their expertise (each runs the `executor` stage) | module-designer, test-engineer |

The Team Supervisor sits at the top: it decomposes and dispatches work to Workers, then evaluates
the team output each iteration. Workers produce artifacts that flow back for scoring.

### Quality Dimension Definition

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

The loop terminates when ANY of these is met:

1. **Threshold reached**: Weighted score ≥ `threshold` (e.g. 0.85)
2. **Max iterations**: Loop count reaches `max_iterations` (e.g. 5)
3. **Regression detected**: Score decreases for `regression_limit` consecutive iterations (e.g. 2)

Design tips: set threshold realistically (0.80–0.90); keep `max_iterations` low (3–5) to control
cost; a regression limit of 2 prevents wasted iterations on diverging output.

### Example: Spec-Writing Iteration Team

```
Iteration 1:
  Writer (Worker)   → drafts API spec
  Reviewer (Worker) → scores: correctness=0.6, completeness=0.5, clarity=0.7
  Supervisor        → weighted score = 0.59 < threshold(0.85) → continue

Iteration 2:
  Optimizer (Worker) → addresses feedback, rewrites spec
  Reviewer (Worker)  → scores: correctness=0.8, completeness=0.75, clarity=0.85
  Supervisor         → weighted score = 0.79 < threshold(0.85) → continue

Iteration 3:
  Optimizer (Worker) → final refinements
  Reviewer (Worker)  → scores: correctness=0.9, completeness=0.9, clarity=0.9
  Supervisor         → weighted score = 0.90 ≥ threshold(0.85) → ACCEPT
```

---

## Continuous (priority: 长期运营 / operate)

**Entry**: `/speckit.team` (intent: "持续运营", "长期维持", "每天处理", "keep running / improving")
**Skill**: `create-team` (continuous mode)

Continuous is the **long-lived operating form**: it runs on a **cadence**, and each run is one
**bounded cycle** that reads its constraints and budget, discovers and triages work, (at higher
maturity) makes a minimal change under an **independent verifier**, scores against the goal,
appends a critique, and updates a **cross-run state spine**.

Because it can run unattended and repeatedly, continuous carries a full operating discipline —
maturity levels (**start at L1**, graduate L1→L2→L3), a constraints file, a budget /
circuit-breaker / kill-switch, a state spine, and Maker/Checker verification.

> This guide intentionally does not duplicate that discipline. See
> **[continuous-operations.md](./continuous-operations.md)** for the full operating model, and the
> normative source [`operating-loops.md`](../../skills/create-team/references/operating-loops.md).

---

## Model Selection Guidance

Different tasks within an orchestration have different cognitive requirements:

| Task Type | Characteristics | Recommended Model Tier |
|-----------|----------------|------------------------|
| **Deterministic** | Template filling, file copying, status tracking | Lightweight / fast model |
| **Judgment** | Code review, scoring, standard implementation | Standard model |
| **Deep Analysis** | Architecture design, complex debugging, novel problem-solving | High-capability model |

### Mapping to Team Roles

- **Team Supervisor** (dispatch/aggregation + quality scoring, convergence): Standard→High — structural coordination plus judgment
- **Workers** (implementation, testing — `executor` stage): Standard — requires coding ability
- **Evaluator / Independent Verifier** (`evaluator` stage, rubric scoring): Standard — structured evaluation
- **Optimizer** (`optimizer` stage, rewriting based on feedback): Standard — targeted modifications

### Cost Optimization Rule

> Use the cheapest model that reliably produces correct output for each role.

For a team of 5 agents running 3 iterations, using lightweight models where possible can reduce
total token cost by 40–60% compared to using high-capability models everywhere.

---

## Cost Control Best Practices

1. **File handshake over prompt chaining** — write artifacts to `.specify/handoff/`; downstream agents read only what they need (50–80% token reduction per transition).
2. **Appropriate parallelism** — more workers ≠ faster if coordination dominates; sweet spot is 2–4 parallel workers.
3. **Confidence-score filtering** — skip full re-evaluation for high-confidence results (>0.9); prioritize low-confidence (<0.6) ones (20–30% fewer eval cycles).
4. **Early termination** — accept a first-iteration score >0.9 immediately; abort after two consecutive regressions; keep `max_iterations` aggressive (3–5).
5. **Incremental improvement** — the optimizer rewrites only low-scoring sections and receives delta feedback, not full rubrics each time (30–50% reduction).
6. **Continuous budget guard** — for continuous teams, the per-day/per-cycle budget and circuit-breaker are mandatory, not optional (see [continuous-operations.md](./continuous-operations.md)).

---

## Troubleshooting

| Problem | Likely Cause | Solution |
|---------|-------------|----------|
| File conflicts in parallel dispatch | Overlapping territory definitions | Audit territory map; ensure exclusive ownership |
| Serial stage stuck in "blocked" state | Upstream stage failed silently | Check handoff file exists; re-run upstream stage |
| Serial handoff verification keeps failing | Upstream produced a malformed / empty artifact | Fix the producer stage; do not relax the gate |
| Iteration never converges | Threshold too high or dimensions conflicting | Lower threshold or adjust dimension weights |
| Score oscillates without improving | Optimizer and Evaluator disagree on quality | Align scoring rubric with improvement instructions |
| Excessive token usage | Full context passed in prompts | Switch to file handshake protocol |
| Worker produces empty output | Missing input context | Verify handoff file is populated before dispatch |
| Continuous team burns tokens / makes bad edits | Started above L1, no budget, non-independent verifier | Reset to L1, add budget/circuit-breaker, enforce independent verifier (see continuous-operations.md) |

### Recovery Strategies

- **Parallel failure**: re-dispatch only the failed worker; successful workers' output is preserved.
- **Serial failure**: resume from the last successful stage (checkpoint artifacts enable this).
- **Iteration divergence**: reset to the highest-scoring iteration's artifact and retry with adjusted dimensions.
- **Continuous incident**: trip the kill-switch, drop to report-only (L1), read the state spine + run-log to diagnose, then let `improve-team` re-tune before resuming.

---

## Multi-Agent Template Catalog

The multi-agent authoring templates live at **`skills/create-team/templates/`** (installed mirror:
`.specify/skills/create-team/templates/`). The single-agent role/custom templates stay in
`skills/create-agent/templates/` (see [`docs/agents/templates-and-agents.md`](../agents/templates-and-agents.md)).

| Template | Purpose |
|----------|---------|
| `agent-role-team-supervisor-template.md` | The single **Meta** role (Meta at all stages) — the Lead / quality gate; mandatory for iteration & continuous |
| `agent-stage-executor-template.md` | EEI `executor` stage (Type Worker) — does the work |
| `agent-stage-evaluator-template.md` | EEI `evaluator` stage (Type Meta) — scores / independently verifies |
| `agent-stage-optimizer-template.md` | EEI `optimizer` stage (Type Meta) — refines from feedback |
| `agent-parallel-orchestration-template.md` | parallel dispatch topology |
| `agent-serial-orchestration-template.md` | serial chain topology |
| `agent-triad-orchestration-template.md` | the EEI iteration loop (backs the `iteration` pattern; `continuous` reuses it per cycle) |
| `agent-workflow-schema.md` | the `AgentWorkflow` JSON schema used by serial orchestration |

> The former `agent-subrole-*` naming and the `improver` stage name are **removed**
> (now `agent-stage-*` / `optimizer`). `continuous` adds no new template — its discipline is
> documented in [continuous-operations.md](./continuous-operations.md) and applied by the
> Team Supervisor at run time.

---

## Related Documents & Traceability

- Team concept, 4-pattern semantics, directory layout, authoritative-source index: [overview.md](./overview.md)
- The long-lived operating discipline (maturity, constraints, budget, verifier, state spine): [continuous-operations.md](./continuous-operations.md)
- Normative concept model (Role × Stage × Type, Team/Loop, merged Team Supervisor): [`conceptual-model.md`](../../skills/create-team/references/conceptual-model.md)
- Command entry point (create / modify / run): [`templates/commands/team.md`](../../templates/commands/team.md)
- The per-role quality loop iteration builds on: [quality-loop.md](../agents/quality-loop.md)

Normative source: `.specify/specs/.archive/026-agent-team-management/` and the orchestration templates
`skills/create-team/templates/agent-{parallel,serial,triad}-orchestration-template.md`.
