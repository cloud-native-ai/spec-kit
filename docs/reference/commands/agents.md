# /speckit.agents

The single entry point for **single-agent** operations — create and refine one agent. `/speckit.agents` recognizes your intent and routes it to the owning skill. Organizing or running multiple agents as a team lives behind [`/speckit.team`](team.md).

## When to Use

- After `specify init` to generate project-aware role-based agents
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
/speckit.agents                    # infer intent from context (e.g. generate role-based agents)
/speckit.agents [intent]           # natural-language intent → routed to the matching skill
```

## Intent Routing

| Recognized intent | Capability | Skill |
|-------------------|------------|-------|
| Create a new agent | authoring | `create-agent` |
| Refine / improve an existing agent | authoring | `improve-agent` |
| Organize / run a team of agents | out of scope | redirect to [`/speckit.team`](team.md) |

The command **delegates to skills** and never renders templates inline. On ambiguous or unsupported intent it reports the recognized single-agent capabilities (create / refine) and requests the missing intent — it never guesses silently. Team requests are directed to [`/speckit.team`](team.md).

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

- **Project marking** — the agent is generated from `skills/create-agent/templates/agent-project-custom-template.md` and MUST record its bound project in the `project:` frontmatter field.
- **Project Scope Guard** — the agent keeps a `## Project Scope Guard` section that, at invocation, resolves the current project (from `.specify/instructions.md`, the constitution, or `README.md`) and compares it to the bound project. On a mismatch it warns the user prominently and requests explicit confirmation before proceeding, rather than running silently in a project it was not built for.

Everything else (purpose, workflow, output format) is free-form and adapts to the project.

## Team Operations

Organizing and running multiple agents (parallel / serial / iteration / continuous) is owned by [`/speckit.team`](team.md) and the `create-team` / `improve-team` skills — not by `/speckit.agents`.

## Lifecycle: Temporary vs Persistent

| Lifecycle | Behavior |
|-----------|----------|
| Temporary | Lives only in conversation context; not written to the agent directory |
| Persistent | Written under `.specify/agents/templates/` (role Templates) or `.specify/agents/instances/` (Instances) and made available to all officially supported tools on initialization |

## Role-Based Generation

With no explicit intent, `/speckit.agents` generates the seven role-based workflow agents, populated with the current project's context:

| Agent | File | Role |
|-------|------|------|
| Requirements Analyst | `requirements-analyst.agent.md` | Clarifies and structures requirements from stakeholder input |
| UX Analyst | `ux-analyst.agent.md` | Analyzes and optimizes all user interfaces — front-end/GUI, CLI, commands, and skills |
| System Designer | `system-designer.agent.md` | Designs system-level architecture and implementation approaches |
| Module Designer | `module-designer.agent.md` | Designs detailed implementations within specific modules |
| Test Engineer | `test-engineer.agent.md` | Designs and executes acceptance tests |
| QA Engineer | `qa-engineer.agent.md` | Validates system quality against design and requirements |
| Knowledge Manager | `knowledge-manager.agent.md` | Maintains documentation and project knowledge |

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

- `create-agent` — author new role-based, custom, or project-custom agents (canonical templates in `skills/create-agent/templates/`)
- `improve-agent` — iteratively improve an existing agent from execution feedback
- Team orchestration (parallel / serial / iteration / continuous) is owned by [`/speckit.team`](team.md) via the `create-team` / `improve-team` skills

## Prerequisites

- `specify init` (project initialized)

## Next Steps

- Run [`/speckit.instructions`](instructions.md) to refresh discovery metadata
# /speckit.agents

The single entry point for **single-agent** operations — create and refine one agent. `/speckit.agents` recognizes your intent and routes it to the owning skill. Organizing or running multiple agents as a team lives behind [`/speckit.team`](team.md).

## When to Use

- After `specify init` to generate project-aware role-based agents
- When you need a custom agent for a specialized workflow
- (To organize or run multiple agents as a team, use [`/speckit.team`](team.md) instead)
- When project context has changed and agents need to be refreshed

## Conceptual Model

Agents are expressed with the **Role × Stage × Type** model:

- **Role** — the domain responsibility (e.g. Requirements Analyst, Team Supervisor)
- **Stage** — the lifecycle stage the agent operates in (executor / evaluator / optimizer)
- **Type** — follows the Stage (executor→Worker, evaluator→Meta, optimizer→Meta)

Agents are organized statically as a **Team** (a Role×Stage matrix) and dynamically as a **Loop** (iterative refinement to a quality threshold).

## Syntax

```text
/speckit.agents                    # infer intent from context (e.g. generate role-based agents)
/speckit.agents [intent]           # natural-language intent → routed to the matching skill
```

## Intent Routing

| Recognized intent | Capability | Skill |
|-------------------|------------|-------|
| Create a new agent | authoring | `create-agent` |
| Refine / improve an existing agent | authoring | `improve-agent` |
| Organize / run a team of agents | out of scope | redirect to [`/speckit.team`](team.md) |

The command **delegates to skills** and never renders templates inline. On ambiguous or unsupported intent it reports the recognized single-agent capabilities (create / refine) and requests the missing intent — it never guesses silently. Team requests are directed to [`/speckit.team`](team.md).

## Team Operations

Organizing and running multiple agents (parallel / serial / iteration / continuous) is owned by [`/speckit.team`](team.md) and the `create-team` / `improve-team` skills — not by `/speckit.agents`.

## Lifecycle: Temporary vs Persistent

| Lifecycle | Behavior |
|-----------|----------|
| Temporary | Lives only in conversation context; not written to the agent directory |
| Persistent | Written under `.specify/agents/templates/` (role Templates) or `.specify/agents/instances/` (Instances) and made available to all officially supported tools on initialization |

## Role-Based Generation

With no explicit intent, `/speckit.agents` generates the seven role-based workflow agents, populated with the current project's context:

| Agent | File | Role |
|-------|------|------|
| Requirements Analyst | `requirements-analyst.agent.md` | Clarifies and structures requirements from stakeholder input |
| UX Analyst | `ux-analyst.agent.md` | Analyzes and optimizes all user interfaces — front-end/GUI, CLI, commands, and skills |
| System Designer | `system-designer.agent.md` | Designs system-level architecture and implementation approaches |
| Module Designer | `module-designer.agent.md` | Designs detailed implementations within specific modules |
| Test Engineer | `test-engineer.agent.md` | Designs and executes acceptance tests |
| QA Engineer | `qa-engineer.agent.md` | Validates system quality against design and requirements |
| Knowledge Manager | `knowledge-manager.agent.md` | Maintains documentation and project knowledge |

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

- `create-agent` — author new role-based or custom agents (canonical templates in `skills/create-agent/templates/`)
- `improve-agent` — iteratively improve an existing agent from execution feedback
- Team orchestration (parallel / serial / iteration / continuous) is owned by [`/speckit.team`](team.md) via the `create-team` / `improve-team` skills

## Prerequisites

- `specify init` (project initialized)

## Next Steps

- Run [`/speckit.instructions`](instructions.md) to refresh discovery metadata
# /speckit.agents

Generate role-based development workflow agents or create custom agents using `.agent.md` files.

## When to Use

- After `specify init` to generate project-aware role-based agents
- When you need a custom agent for a specialized workflow
- When project context has changed and agents need to be refreshed

## Syntax

```text
/speckit.agents                    # Mode A: Generate all seven role-based agents
/speckit.agents [agent intent]     # Mode B: Create a custom agent
```

## Mode A: Role-Based Generation (no arguments)

Generates seven software development workflow agents from role templates, populated with the current project's actual context.

| Agent | File | Role |
|-------|------|------|
| Requirements Analyst | `requirements-analyst.agent.md` | Clarifies and structures requirements from stakeholder input |
| UX Analyst | `ux-analyst.agent.md` | Analyzes and optimizes all user interfaces — front-end/GUI, CLI, commands, and skills |
| System Designer | `system-designer.agent.md` | Designs system-level architecture and implementation approaches |
| Module Designer | `module-designer.agent.md` | Designs detailed implementations within specific modules |
| Test Engineer | `test-engineer.agent.md` | Designs and executes acceptance tests |
| QA Engineer | `qa-engineer.agent.md` | Validates system quality against design and requirements |
| Knowledge Manager | `knowledge-manager.agent.md` | Maintains documentation and project knowledge |

### Mode A Execution Flow

1. **Gather project context** — Reads README, build config, directory tree, source modules, constitution, feature index, specs, test configuration, and docs.

2. **Resolve placeholders** — For each role template, fills `{{PROJECT_NAME}}`, `{{TECH_STACK}}`, `{{PROJECT_STRUCTURE}}`, `{{CONSTITUTION_PRINCIPLES}}`, etc.

3. **Backup detection** — If an agent file already exists and has been customized, creates a `.bak` copy before overwriting.

4. **Agent preservation** — Only creates/updates the seven role-based agent files. Leaves all other existing agents untouched.

5. **Write agents** — All seven agents written to `.specify/agents/templates/` (canonical Template store).

6. **Discovery** — Agents are discovered by globbing `.specify/agents/{templates,instances}/*.agent.md`; no separate registry/workspace files are created.

7. **Report** — Lists generated agents, notes any backups, suggests running `/speckit.instructions`.

## Mode B: Custom Agent Creation (with arguments)

Creates or updates a single custom agent based on user-provided intent.

### Mode B Execution Flow

1. **Extract from conversation** — Reviews conversation history for specialized roles, tool preferences, and domain scope.

2. **Determine agent intent** — Uses `$ARGUMENTS` as explicit intent. Asks clarification questions if confidence is low.

3. **Define agent shape** — Produces: file name, display name, trigger description, least-privilege tool set, invocation mode, and reference files.

4. **Iterate** — Drafts the agent file, identifies weak parts, asks targeted follow-ups.

5. **Create `.agent.md`** — Writes to `.specify/agents/instances/<agent-name>.agent.md` with YAML frontmatter and body sections for role, constraints, workflow, and output format.

6. **Quality checks** — Validates YAML syntax, provider support (Claude Code, Copilot, opencode, Qoder, Codex CLI, Hermes Agent only), and tool-workflow alignment.

7. **Register agent** — Generates a deterministic `agent_id` and updates the Resource Registry in `.specify/instructions.md`.

8. **Report** — Outputs the file path, agent ID, example trigger prompts, and suggested next customizations.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Agent files | `.specify/agents/templates/<name>.agent.md` (Templates) · `.specify/agents/instances/<name>.agent.md` (Instances) |

## Symlink Model

Each tool's `agents/` directory holds **rendered real files** translated at `specify init` from the neutral metadata in `.specify/agents/{templates,instances}/`:
- `.qoder/agents/<slug>.agent.md` — Qoder format
- `.claude/agents/<slug>.md` — Claude Code format
- `.github/agents/<slug>.agent.md` — GitHub Copilot format
- `.opencode/agents/<slug>.md` — opencode format (filename carries the agent name)

## Companion Skills

- `create-agent` — Create new role-based agent templates in `templates/`
- `improve-agent` — Iteratively improve agent templates from execution feedback

## Prerequisites

- `specify init` (project initialized)

## Next Steps

- Run [`/speckit.instructions`](instructions.md) to refresh discovery metadata
