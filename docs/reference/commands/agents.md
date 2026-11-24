# /speckit.agents

The single entry point for **single-agent** operations — create, refine and run one agent.
`/speckit.agents` recognizes your intent and routes it to the owning skill. Organizing or
running multiple agents as a team lives behind [`/speckit.team`](team.md).

## When to Use

- After `specify init` to generate project-aware role-based agents
- When you need to run an existing agent on a bounded task — `/speckit.agents run <agent-name> [task]`
- When you need a custom agent for a specialized workflow (generic `custom`) or a **project-specific** agent tailored to one project (`project-custom`)
- (To organize or run multiple agents as a team, use [`/speckit.team`](team.md) instead)
- When project context has changed and agents need to be refreshed

## Conceptual Model

Agents are expressed with the **Role × Stage × Type** model:

- **Role** — the domain responsibility (e.g. Requirements Analyst, Team Supervisor)
- **Stage** — the lifecycle stage the agent operates in (executor / evaluator / optimizer)
- **Type** — follows the Stage (executor→Worker, evaluator→Meta, optimizer→Meta)

Agents are organized statically as a **Team** (a Role×Stage matrix) and dynamically as a **Loop** (iterative refinement to a quality threshold).

Not every agent fits the preset Role×Stage grid. When a project's needs fall outside it, author a **custom** agent (narrow, general-purpose) or a **project-custom** agent (bound to a single project). See [Authoring Modes](#authoring-modes).

## Syntax

```text
/speckit.agents [create|refine|run] [agent-name] [task]  # command-level argument grammar
/speckit.agents run <agent-name> [task]                  # explicit run: dispatch one agent as a subagent
/speckit.agents                                          # no arguments: list existing agents, give grounded suggestions, show the three-mode summary
/speckit.agents <natural-language intent>                # natural-language intent → routed to the matching skill
```

An explicit leading verb (`run` / `create` / `refine`) wins over context inference. An explicit `run` with no agent name reports `missing agent name`, the three capabilities (create / refine / run) and the usage line, and dispatches nothing.

## Intent Routing

| Recognized intent | Capability | Skill |
|-------------------|------------|-------|
| Run an existing agent on a task | execution | `run-agent` |
| Create a new agent | authoring | `create-agent` |
| Refine / improve an existing agent | authoring | `improve-agent` |
| Organize / run a team of agents | out of scope | redirect to [`/speckit.team`](team.md) |

The command **delegates to skills** and never renders templates inline. On ambiguous or unsupported intent it reports the three single-agent capabilities (create / refine / run) and requests the missing intent — it never guesses silently. Team requests are directed to [`/speckit.team`](team.md).

## Run Mode

Running is owned by the `run-agent` skill: it resolves the definition across the layers
(`.specify/agents/instances/<name>.agent.md`, falling back to
`.specify/agents/templates/<name>.agent.md`; instance wins on collision), applies
`.specify/agents/execution/configs/<name>.yaml` when present, presents the agent and the role
relation of the dispatch (this session is the edge's superagent/root), dispatches **one**
independent Agent Execution and relays a return that satisfies the five-element uplink.
`run <agent-name>` without a task reports `missing task` and asks for it; an unknown name
reports `agent not found` with a bounded suggestion list and a create suggestion — neither
path dispatches an agent.

## Authoring Modes

When creating an agent, `create-agent` supports several **modes** (`kind`). If the request does not clearly map to one, `/speckit.agents` **confirms which mode you want before generating** — it never guesses the mode silently:

| Mode (`kind`) | Produces |
|---------------|----------|
| `role` | One of the seven preset role-based agents (or a new role) |
| `supervisor` | A role agent that runs its own EEI loop |
| `custom` | A single narrow, **general-purpose** custom agent (not bound to a project) |
| `project-custom` | A **project-bound** custom agent for one specific project |

### Project-Custom Agents

Different projects often need very different agents, so `project-custom` creation follows a **flexible flow** (not a fixed sequence). Two things are always mandatory:

- **Project marking** — the agent is generated from `skills/internal/create-agent/templates/agent-project-custom-template.md` and MUST record its bound project in the `project:` frontmatter field.
- **Project Scope Guard** — the agent keeps a `## Project Scope Guard` section that, at invocation, resolves the current project (from `.specify/instructions.md`, the constitution, or `README.md`) and compares it to the bound project. On a mismatch it warns the user prominently and requests explicit confirmation before proceeding, rather than running silently in a project it was not built for.

Everything else (purpose, workflow, output format) is free-form and adapts to the project.

## Team Operations

Organizing and running multiple agents (parallel / serial / iteration / continuous) is owned by [`/speckit.team`](team.md) and the `create-team` / `improve-team` skills — not by `/speckit.agents`.

## Lifecycle: Temporary vs Persistent

| Lifecycle | Behavior |
|-----------|----------|
| Temporary | Lives only in conversation context; not written to the agent directory |
| Persistent | Written under `.specify/agents/templates/` (role Templates) or `.specify/agents/instances/` (Instances) and made available to all officially supported tools on initialization |

## Default Behavior (No Arguments)

With empty arguments the command executes the list + suggestion sequence owned by the `run-agent` skill (informational and non-destructive):

1. **List every existing agent** — scan `.specify/agents/{templates,instances}/*.agent.md` and present a summary table with each agent's **layer**, `name`, `description`, `tools`, and `model`; state `No agents found` explicitly when none exist.
2. **Give grounded suggestions** — grounded in observable context, never fabricated: a description that matches the current task → suggest `run <name>`; an outdated or underperforming definition → suggest `refine <name>`; nothing fits → suggest `create` with a proposed role derived from context.
3. **Show the three-mode capability summary** — briefly list the three modes (create / refine / run).

It creates, refines, or runs no agent without an explicit user instruction.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Agent files | `.specify/agents/templates/<name>.agent.md` (Templates) · `.specify/agents/instances/<name>.agent.md` (Instances) |

## Symlink Model

Each tool's `agents/` directory holds **rendered real files** translated at `specify init` from the neutral metadata in `.specify/agents/{templates,instances}/` (never write framework agents into them directly — outputs are rebuilt from the neutral source):

- `.qoder/agents/<slug>.agent.md` — Qoder format
- `.claude/agents/<slug>.md` — Claude Code format
- `.github/agents/<slug>.agent.md` — GitHub Copilot format
- `.opencode/agents/<slug>.md` — opencode format (filename carries the agent name)

## Companion Skills

- `run-agent` — run an existing agent: resolve → present → dispatch one independent execution → (external) collect → report; also owns the no-argument listing behaviour
- `create-agent` — author new role-based, custom, or project-custom agents (canonical templates in `skills/internal/create-agent/templates/`)
- `improve-agent` — iteratively improve an existing agent from execution feedback
- Team orchestration (parallel / serial / iteration / continuous) is owned by [`/speckit.team`](team.md) via the `create-team` / `improve-team` skills

## Prerequisites

- `specify init` (project initialized)

## Next Steps

- Run [`/speckit.instructions`](instructions.md) to refresh discovery metadata
