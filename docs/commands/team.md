# /speckit.team

The single entry point for **all team operations** — create, modify, and run agent teams. `/speckit.team` is the multi-agent analogue of `/speckit.agents`: it recognizes your intent and routes it to the owning team skill. Single-agent authoring lives in `/speckit.agents`; team operations live here.

## When to Use

- When you want to organize several agents into a collaborative **team** (parallel / serial / team-loop)
- When you want to **run** an existing team behind a preview → confirm gate
- When you want to **adjust or optimize** an existing team (add/remove members, tune thresholds, repartition territories)

## Conceptual Model

A **team** has two structures (defined once in `skills/create-team/references/conceptual-model.md`):

- **Static structure** — a **Role × Stage × Type** roster (who participates, in what role, at what stage, Worker or Meta).
- **Dynamic structure** — the collaboration **pattern** (parallel / serial / team-loop) with its parallelism / DAG / iteration settings and an execution flow.

Persistent teams are stored at `.specify/teams/<slug>.team.md` (Markdown + YAML frontmatter, no per-tool symlink).

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

1. **Load** the team from `.specify/teams/<slug>.team.md`.
2. **Render Static Structure** — the Role × Stage × Type roster matrix.
3. **Render Dynamic Structure** — the pattern, its parallelism/DAG/loop settings, and an execution flow diagram.
4. **Confirmation gate** — you review both structures and explicitly confirm. Only then does orchestration run (territory validation for parallel, DAG no-cycle for serial, max-iteration cap for team-loop, file-path-only handoff). Declining stops without executing.

## Collaboration Patterns

- **parallel** — independent Workers dispatched together with disjoint write territories
- **serial** — an ordered DAG chain where each stage's output feeds the next via file-path-only handoff
- **team-loop** — Workers + exactly one **Team Supervisor** (Meta role) iterate to a quality threshold

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Persisted teams | `.specify/teams/<slug>.team.md` |

## Companion Skills

- `create-team` — define a team (static + dynamic structure), persist it, and execute it (parallel / serial / team-loop)
- `improve-team` — apply targeted, evidence-based, structure-preserving edits to an existing team

## Prerequisites

- `specify init` (project initialized); `.specify/agents/` populated with the agents that become team members

## Next Steps

- Run [`/speckit.instructions`](instructions.md) to refresh discovery metadata
