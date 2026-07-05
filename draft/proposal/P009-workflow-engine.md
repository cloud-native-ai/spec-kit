# P009 — Workflow Engine & Deterministic Orchestration

- **Status:** Draft
- **Pillars:** Workflow · Infra
- **Source projects:** claude-code-ts, intellegix-code-agent-toolkit
- **Value:** H · **Effort:** H · **Phase:** 3
- **Related:** [[P004]], [[P005]], [[P001]]

## Problem / Gap

spec-kit's SDD flow (constitution → specify → clarify → plan → tasks → analyze → implement →
review) is, in effect, a workflow — but today it is a chain of slash-commands a human drives one
at a time. There is no durable execution state, no way to run steps in parallel, no resume after
interruption, and no first-class way for users to author their *own* multi-step, multi-agent
processes over spec-kit's commands.

The `draft/skills/spec-kit-extensions/` skill already defines a **declarative YAML workflow
format** (see `references/workflow-format.md`): 11 step types, typed inputs, gates,
`if`/`switch`/`while`/`do-while`, `fan-out`/`fan-in`, and `specify workflow run|resume|status`
with per-run state under `.specify/workflows/runs/<run_id>/`. That format specifies *what* a
workflow looks like. What is missing is the **engine underneath it** — the deterministic,
replayable orchestrator that actually executes steps, journals results, bounds concurrency,
enforces budgets, and resumes correctly. This proposal defines that engine and a complementary
programmatic authoring surface for graphs the linear YAML DSL cannot express cleanly.

## Proposal

Introduce a **ports-driven workflow engine** that runs both authoring surfaces:

1. **The existing YAML DSL** (`spec-kit-extensions` `workflow.yml`) for linear/gated pipelines —
   this proposal supplies its runtime, not a competing format.
2. **A programmatic script surface** exposing injected primitives — `agent()`, `parallel()`,
   `pipeline()`, `phase()`, `workflow()` (sub-workflows), `budget`, `log` — for richer
   fan-out/dependency graphs.

The engine isolates all non-determinism behind **ports** (agent runner, journal store, progress
emitter, task registrar) so the core is host-agnostic and testable. It **journals every
`agent()` result**, so resume replays completed steps for free; enforces **bounded concurrency**
via a semaphore and **token/USD budgets**; **auto-retries once**; and degrades a single failed
agent to a null result rather than killing the whole run. spec-kit's canonical SDD chain ships as
the first named workflow (`speckit-sdd`), and users drop their own under `.specify/workflows/`.

## Design sketch

### File layout (lands in `draft/` first)

```
draft/
  scripts/workflow/
    engine.py          # WorkflowRunner: journal replay, semaphore, budget, retry
    ports.py           # AgentRunner / JournalStore / ProgressEmitter / TaskRegistrar (ABCs)
    primitives.py      # agent / parallel / pipeline / phase / workflow / budget / log
    dsl_runner.py      # executes the extensions YAML format via the same engine
  workflows/
    speckit-sdd.py     # canonical SDD chain as a programmatic workflow (bundled)
```

Run state reuses the format the extensions skill already defined:
`.specify/workflows/runs/<run_id>/{state.json, inputs.json, journal.jsonl, log.jsonl}`.

### Ports (dependency injection — the core has zero host deps)

```python
class AgentRunner(Protocol):
    def run(self, prompt: str, *, schema=None, agent_type=None,
            isolation=None, allowed_tools=None) -> AgentResult: ...

class JournalStore(Protocol):
    def get(self, step_key: str) -> AgentResult | None: ...   # replay on resume
    def put(self, step_key: str, result: AgentResult) -> None: ...

class ProgressEmitter(Protocol):
    def emit(self, event: dict) -> None: ...

class TaskRegistrar(Protocol):                # bridges to the task graph ([[P004]])
    def register(self, tasks: list[dict]) -> None: ...
```

### Programmatic workflow script

```python
def workflow(ctx, inputs):
    with ctx.phase("design"):
        spec = ctx.agent(f"/speckit.specify {inputs['spec']}", schema=SpecSchema)
        ctx.gate("Review the spec before planning")          # human checkpoint
        plan = ctx.agent("/speckit.plan", schema=PlanSchema)

    with ctx.phase("build"):
        tasks = ctx.agent("/speckit.tasks", schema=TaskListSchema)
        # bounded-concurrency fan-out; one failure degrades to None, run continues
        results = ctx.parallel(
            [lambda t=t: ctx.agent(f"/speckit.implement {t.id}") for t in tasks.ready],
            max_concurrency=inputs.get("max_concurrency", 3),
        )
    return ctx.agent("/speckit.review", schema=ReviewSchema)
```

### Engine contract (ported design, reimplemented in Python)

- **Journal replay on resume.** Before running an `agent()` step, look it up by a stable step key
  in the `JournalStore`; on a hit, return the recorded result without re-invoking the agent.
- **Semaphore-guarded budget.** Each `agent()` acquires a concurrency slot and checks the run
  budget (tokens/USD) before dispatch; over-budget short-circuits with a typed terminal result.
- **Auto-retry-once.** A failed agent is retried a single time before it is classified.
- **Dead-agent classification, not run death.** A failed agent yields `null` with a reason
  (`no-structured-output` / `runagent-threw` / `worktree-failed`); the workflow decides how to
  proceed rather than crashing.
- **Sub-workflows** resolve named workflows from `.specify/workflows/<name>` with a depth guard.
- **Detached runs** return a `run_id` immediately; progress streams through `ProgressEmitter`.

### Relationship to the extensions YAML DSL

`dsl_runner.py` interprets the existing `spec-kit-extensions` `workflow.yml` (its 11 step types,
gates, loops, `fan-out`/`fan-in`) by lowering each step onto engine primitives — `command`/`prompt`
→ `agent()`, `fan-out` → `parallel()`, `gate` → a pause with the existing `on_reject` semantics,
`while`/`do-while` → a bounded loop. The two surfaces share one engine, one run directory, one
resume model, so `specify workflow run|resume|status` (already specified in
`references/workflow-format.md`) works uniformly. **Note the known limitation** documented there:
resume tracking is at the top-level step index; exact nested-step resume is a planned enhancement
the engine's journal keying is designed to eventually support.

### Bundled SDD workflow

`speckit-sdd.py` expresses the canonical chain as an engine workflow — steps call the *existing*
`/speckit.*` commands unchanged, with the plan-review and implementation gates as `ctx.gate(...)`
checkpoints. It is opt-in orchestration *over* the pipeline, not a rewrite of it.

## Source evidence

- Ports-driven engine, primitives, journal replay, semaphore, budget, auto-retry, dead-agent
  classification — `/cws_work/claude-code-ts/packages/workflow-engine/src/engine/hooks.ts`
  (primitives + replay 73–90, budget 92–105, failure→null 173–270),
  `/cws_work/claude-code-ts/packages/workflow-engine/src/engine/runWorkflow.ts` (resume/replay,
  sub-workflow depth), `/cws_work/claude-code-ts/packages/workflow-engine/src/ports.ts`.
- Tool/workflow surface, input schema (`maxConcurrency`, `resumeFromRunId`), script-model prompt —
  `/cws_work/claude-code-ts/packages/workflow-engine/src/tool/WorkflowTool.ts`,
  `/cws_work/claude-code-ts/packages/workflow-engine/src/tool/schema.ts`.
- End-to-end minimal wiring (which ports to implement, retry/backoff, structured output) —
  `/cws_work/claude-code-ts/packages/workflow-engine/examples/smoke.ts`,
  `/cws_work/claude-code-ts/packages/workflow-engine/README.md`.
- Managed multi-step flows with per-step status + approval gates + resumable runs.json —
  `/cws_work/claude-code-ts/src/utils/autonomyFlows.ts`,
  `/cws_work/claude-code-ts/src/utils/autonomyRuns.ts`.
- Territory-split parallel orchestration + appropriateness gate (fall back to single-agent for
  small/coupled work) — `/cws_work/intellegix-code-agent-toolkit/commands/orchestrator-multi.md`
  (appropriateness matrix 43–53, territory rules 188–201, merge/rollback 674–753),
  `/cws_work/intellegix-code-agent-toolkit/automated-loop/multi_agent.py`
  (`WorkSplitter.split_for_agents` greedy bin-packing 149–183).
- Existing YAML workflow format this engine executes —
  `/cws_work/spec-kit/draft/skills/spec-kit-extensions/references/workflow-format.md`,
  `/cws_work/spec-kit/draft/skills/spec-kit-extensions/assets/workflow-template.yml`.

## Adoption plan

1. **Port the *design*, not the TypeScript.** Land `engine.py` + `ports.py` + `primitives.py` in
   `draft/scripts/workflow/`, reusing the run-directory and resume model the extensions skill
   already defines so the two efforts converge rather than fork.
2. **Wire `dsl_runner.py`** to execute the existing `workflow.yml` format on the new engine;
   validate against `assets/workflow-template.yml`.
3. **Ship `speckit-sdd.py`** as the first bundled workflow, calling the current `/speckit.*`
   commands verbatim with human gates preserved.
4. **Add parallel execution behind an appropriateness gate** (intellegix): only fan out over
   genuinely independent tasks (file "territories" from [[P004]]'s task graph); fall back to
   sequential for small/coupled work. Pair each parallel lane with a worktree ([[P004]]).
5. **Keep the pipeline sacrosanct.** The engine *invokes* `/speckit.*` steps; it never changes
   them. A user who never runs `specify workflow run` sees the exact current behavior. **Nothing
   here disturbs the main `/speckit.*` flow** until deliberately promoted.

## Risks & mitigations

- **Over-engineering.** A full engine is a large bet. *Mitigation:* land the linear-DSL runtime
  first (it already has a spec), add programmatic primitives + parallelism only once the linear
  case is proven; Phase 3 by design.
- **Determinism vs LLM nondeterminism.** Journaling replays *results*, but agents are
  nondeterministic within a step. *Mitigation:* journal at the `agent()` boundary and treat each
  step as an idempotent unit keyed by its inputs; document that replay reproduces the recorded
  output, not the reasoning.
- **Resume correctness.** Nested-step resume is a known gap in the YAML format. *Mitigation:*
  design journal keys to be nesting-aware from the start so exact nested resume can be enabled
  without a data migration.
- **Parallel write collisions.** *Mitigation:* gate concurrency on task-territory non-overlap and
  run each lane in an isolated worktree ([[P004]]); serialize write-heavy steps.
- **Don't port the Bun runtime.** *Mitigation:* mine the prompts and control-flow contracts from
  `hooks.ts`/`smoke.ts`; reimplement cleanly in Python.

## Value / Effort rationale

**Value H:** turns spec-kit's implicit, human-driven pipeline into a durable, resumable,
parallelizable process and gives users a real authoring surface for their own flows — the
capstone of the Workflow pillar, composing [[P004]]'s task graph and [[P005]]'s loop driver.
**Effort H:** even porting only the design, a correct ports-driven engine with journaling,
concurrency, budgets, resume, and a DSL interpreter is substantial, and it must integrate with the
already-drafted YAML format without diverging. Phase 3: it sits atop the Phase-1 hook layer
([[P001]]) and Phase-2 process depth ([[P004]], [[P005]]), and represents the largest single bet
in the set.
