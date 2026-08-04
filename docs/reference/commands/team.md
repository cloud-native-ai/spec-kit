# /speckit.team

The single entry point for **all team operations** — create, modify, and run agent teams. `/speckit.team` is the multi-agent analogue of `/speckit.agents`: it recognizes your intent and routes it to the owning team skill. Single-agent authoring lives in `/speckit.agents`; team operations live here.

## When to Use

- When you want to organize several agents into a collaborative **team** (parallel / serial / iteration / continuous)
- When you want to **run** an existing team behind a preview → confirm gate
- When you want to **adjust or optimize** an existing team (add/remove members, tune thresholds, repartition territories)

## Conceptual Model

A **team** has two structures (defined once in `skills/create-team/references/conceptual-model.md`):

- **Static structure** — a **Role × Stage × Type** roster (who participates, in what role, at what stage, Worker or Meta).
- **Dynamic structure** — the collaboration **pattern** (parallel / serial / iteration / continuous) with its parallelism / DAG / iteration / operating settings and an execution flow. Each pattern encodes a priority: **parallel** = 效率优先 (throughput), **serial** = 质量优先 (quality, verified handoffs), **iteration** = 目标收敛 (converge then stop), **continuous** = 长期运营 (operate on a cadence).

An `iteration`/`continuous` team MUST include **exactly one** Team Supervisor (Meta role); a `parallel`/`serial` team MAY use one as the Lead / quality gate.

Persistent teams own a directory `.specify/teams/<slug>/` — the definition lives at `.specify/teams/<slug>/team.md` (Markdown + YAML frontmatter, no per-tool symlink) and per-run reports accumulate under `.specify/teams/<slug>/runs/`. A **continuous** team additionally owns tracked operating-spine files — `constraints.md`, `STATE.md`, `run-log.jsonl` (see [`docs/teams/continuous-operations.md`](../teams/continuous-operations.md)).

## Syntax

```text
/speckit.team                      # infer intent from context
/speckit.team [intent]             # natural-language intent → routed to the matching mode/skill
```

## Modes → Intent Routing

`/speckit.team` exposes **exactly three modes**:

| Mode | Recognized intent | Skill |
|------|-------------------|-------|
| **create** | "组织一个团队", "创建团队", "build a team" | `create-team` |
| **modify** | "调整团队", "优化 team", "improve/adjust team" | `improve-team` |
| **run** | "运行团队", "执行团队", "run/execute team" | `create-team` (execution path) |

The command **delegates to skills** and never renders templates inline. On ambiguous or unsupported intent it reports the three recognized capabilities (create / modify / run) and requests the missing intent — it never guesses silently. A `modify`/`run` targeting a team that does not exist reports **"team not found"** and offers to `create` it.

## Run Mode: preview → confirm → execute

The **run** mode never executes before you confirm:

1. **Load** the team from `.specify/teams/<slug>/team.md`.
2. **Render Static Structure** — the Role × Stage × Type roster matrix.
3. **Render Dynamic Structure** — the pattern, its parallelism/DAG/loop settings, and an execution flow diagram.
4. **Confirmation gate** — you review the goal and both structures and explicitly confirm. Only then does orchestration run (territory validation for parallel, DAG no-cycle + per-handoff verification for serial, max-iteration cap for iteration, and — for **continuous** — read `constraints.md` + budget + kill-switch and run exactly **one cycle** at the declared maturity level with an independent verifier at L2+; file-path-only handoff throughout). Declining stops without executing.
5. **Report** — after execution, a dated report is written to `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md` (goal, timing, result summary, process detail). Run intermediates stay in the git-ignored `.specify/teams/.work/<slug>/`; deliverables go only to their declared target paths.

## Collaboration Patterns

Four patterns; the goal decides which fits. The first three are **bounded** (run once and stop); `continuous` is **unbounded** (operates on a cadence). Pick with the decision tree in [`docs/teams/orchestration.md`](../teams/orchestration.md).

- **parallel** (效率优先) — independent Workers dispatched together with disjoint write territories
- **serial** (质量优先) — an ordered DAG chain where each stage's output feeds the next via file-path-only handoff, with a simple verification between each step and its predecessor
- **iteration** (目标收敛) — Workers + exactly one **Team Supervisor** (Meta role) iterate to a quality threshold, then deliver and stop
- **continuous** (长期运营) — runs on a cadence; each cycle reads constraints + budget, acts, independently verifies, scores, critiques, and updates a cross-run state spine (maturity L1→L2→L3; see [`docs/teams/continuous-operations.md`](../teams/continuous-operations.md))

## Output Artifacts

| Artifact | Location | Git |
|----------|----------|-----|
| Team definition | `.specify/teams/<slug>/team.md` | tracked |
| Item ledger (all patterns) | `.specify/teams/<slug>/items.jsonl` | tracked, append-only |
| Continuous operating spine (continuous only) | `.specify/teams/<slug>/{constraints.md,STATE.md,run-log.jsonl}` | tracked |
| Run reports (per execution) | `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md` | tracked |
| **Goal summary** (per goal, not per team) | `.specify/project/goal/<goal-slug>/` (`summary.md` + `assets/` + `data/`) | tracked |
| Deliverables (standard output) | declared target path (real project path) | tracked |
| Run intermediates | `.specify/teams/.work/<slug>/` | git-ignored |

## Goal Summary

A team's execution flow periodically produces a **goal-level summary** — the team treated
as a project — by driving the `summarize-project` skill. Output is **dual-indexed**:

| Index | Path | Answers |
|-------|------|---------|
| **team** | `.specify/teams/<team-slug>/` | how is this team running |
| **goal** | `.specify/project/goal/<goal-slug>/` | how far has this goal progressed |

The goal directory holds the single complete summary and aggregates **every** team that
declares the same `goal_slug`, so a goal outlives any individual team's rebuild or rename.
The team directory keeps run information only.

### Trigger boundaries

| Pattern | Boundary |
|---------|----------|
| `continuous` | end of every Nth cycle (phase 9 SUMMARIZE, after REPORT) |
| `iteration` | after each generation's DECIDE phase |
| `serial` | after each stage handoff verification passes |
| `parallel` | after cross-verification and result aggregation |
| all | terminal summary on goal met / converged / halt / manual stop |

Gates are evaluated in a fixed order — **budget → cadence → material** — and every run
records the outcome in its report:

```text
Summary: produced | skipped(cadence) | skipped(budget) | declined(no-material)
```

That line is mandatory: it is what makes "not observed" distinguishable from "observed,
no progress". The run-mode confirmation gate discloses the summary decision, the resolved
goal identity, and the target directory before you confirm, so the cost is known up front.

### Configuration

```yaml
goal_slug: my-goal        # frontmatter — the GOAL's identity; distinct from `slug`
config:
  summary:
    enabled: true         # omit the whole block and the summary is still enabled
    every: 5              # per N boundaries; continuous defaults to 5, bounded patterns 1
    interactive: false
```

`goal_slug` is optional: a team that omits it falls back to its own slug as an *inferred*
goal identity, so pre-existing teams need no migration. Editing the goal prose never moves
the delivery directory, because identity is declared rather than derived. Concurrent
refreshes of one goal serialize into a single atomic write.

Details: `skills/create-team/references/summary-mapping.md`.

## Companion Skills

- `create-team` — define a team (static + dynamic structure), persist it, and execute it (parallel / serial / iteration / continuous)
- `improve-team` — apply targeted, evidence-based, structure-preserving edits to an existing team

## Prerequisites

- `specify init` (project initialized); `.specify/agents/{templates,instances}/` populated with the agents that become team members

## Next Steps

- Run [`/speckit.instructions`](instructions.md) to refresh discovery metadata
