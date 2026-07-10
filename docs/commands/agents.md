# /speckit.agents

The single entry point for **all** agent operations — create, refine, organize, and execute agents. No other agent-specific command exists; `/speckit.agents` recognizes your intent and routes it to the owning skill.

## When to Use

- After `specify init` to generate project-aware role-based agents
- When you need a custom agent for a specialized workflow
- When you want to organize agents into a parallel, serial, or team-loop topology
- When you want to execute a team or run a team closed-loop
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
| Organize agents — parallel | orchestration | `organize-agents` |
| Organize agents — serial chain | orchestration | `organize-agents` |
| Execute a team / run a team closed-loop | orchestration | `organize-agents` |

The command **delegates to skills** and never renders templates inline. On ambiguous or unsupported intent it reports the recognized capabilities (create / refine / organize / execute) and requests the missing intent — it never guesses silently.

## Collaboration Topologies

- **parallel** — many agents dispatched together (single response, many delegations)
- **serial** — an ordered chain where each stage's output feeds the next
- **team closed-loop** — Worker agents + Meta agents + a single **Team Supervisor** iterate until a quality threshold is met

The Team closed-loop has **two layers**: Team Supervisor (Meta role) + Workers. The former Meta-Coordinator has been **merged into the Team Supervisor**.

## Lifecycle: Temporary vs Persistent

| Lifecycle | Behavior |
|-----------|----------|
| Temporary | Lives only in conversation context; not written to the agent directory |
| Persistent | Written under `.specify/agents/` and made available to all officially supported tools on initialization |

## Role-Based Generation

With no explicit intent, `/speckit.agents` generates the six role-based workflow agents, populated with the current project's context:

| Agent | File | Role |
|-------|------|------|
| Requirements Analyst | `requirements-analyst.agent.md` | Clarifies and structures requirements from stakeholder input |
| System Designer | `system-designer.agent.md` | Designs system-level architecture and implementation approaches |
| Module Designer | `module-designer.agent.md` | Designs detailed implementations within specific modules |
| Test Engineer | `test-engineer.agent.md` | Designs and executes acceptance tests |
| QA Engineer | `qa-engineer.agent.md` | Validates system quality against design and requirements |
| Knowledge Manager | `knowledge-manager.agent.md` | Maintains documentation and project knowledge |

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Agent files | `.specify/agents/<name>.agent.md` |
| Workspace files | `.specify/agents/AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md` |

## Symlink Model

Tool-specific directories are **directory-level symlinks** to `.specify/agents/` (never write to them directly):

- `.github/agents/` → `.specify/agents/` (Copilot, Claude Code)
- `.qoder/agents/` → `.specify/agents/` (Qoder)
- `.qwen/agents/` → `.specify/agents/` (Qwen Code)
- `.opencode/agents/` → `.specify/agents/` (opencode)

## Companion Skills

- `create-agent` — author new role-based or custom agents (canonical templates in `skills/create-agent/templates/`)
- `improve-agent` — iteratively improve an existing agent from execution feedback
- `organize-agents` — arrange and execute agents in parallel / serial / team-loop topologies

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
/speckit.agents                    # Mode A: Generate all six role-based agents
/speckit.agents [agent intent]     # Mode B: Create a custom agent
```

## Mode A: Role-Based Generation (no arguments)

Generates six software development workflow agents from role templates, populated with the current project's actual context.

| Agent | File | Role |
|-------|------|------|
| Requirements Analyst | `requirements-analyst.agent.md` | Clarifies and structures requirements from stakeholder input |
| System Designer | `system-designer.agent.md` | Designs system-level architecture and implementation approaches |
| Module Designer | `module-designer.agent.md` | Designs detailed implementations within specific modules |
| Test Engineer | `test-engineer.agent.md` | Designs and executes acceptance tests |
| QA Engineer | `qa-engineer.agent.md` | Validates system quality against design and requirements |
| Knowledge Manager | `knowledge-manager.agent.md` | Maintains documentation and project knowledge |

### Mode A Execution Flow

1. **Gather project context** — Reads README, build config, directory tree, source modules, constitution, feature index, specs, test configuration, and docs.

2. **Resolve placeholders** — For each role template, fills `{{PROJECT_NAME}}`, `{{TECH_STACK}}`, `{{PROJECT_STRUCTURE}}`, `{{CONSTITUTION_PRINCIPLES}}`, etc.

3. **Backup detection** — If an agent file already exists and has been customized, creates a `.bak` copy before overwriting.

4. **Agent preservation** — Only creates/updates the six role-based agent files. Leaves all other existing agents untouched.

5. **Write agents** — All six agents written to `.specify/agents/` (canonical location).

6. **Workspace scaffolding** — Creates `AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md` if first run.

7. **Report** — Lists generated agents, notes any backups, suggests running `/speckit.instructions`.

## Mode B: Custom Agent Creation (with arguments)

Creates or updates a single custom agent based on user-provided intent.

### Mode B Execution Flow

1. **Extract from conversation** — Reviews conversation history for specialized roles, tool preferences, and domain scope.

2. **Determine agent intent** — Uses `$ARGUMENTS` as explicit intent. Asks clarification questions if confidence is low.

3. **Define agent shape** — Produces: file name, display name, trigger description, least-privilege tool set, invocation mode, and reference files.

4. **Iterate** — Drafts the agent file, identifies weak parts, asks targeted follow-ups.

5. **Create `.agent.md`** — Writes to `.specify/agents/<agent-name>.agent.md` with YAML frontmatter and body sections for role, constraints, workflow, and output format.

6. **Quality checks** — Validates YAML syntax, provider support (Claude Code, Copilot, Qwen Code, opencode, Qoder only), and tool-workflow alignment.

7. **Register agent** — Generates a deterministic `agent_id` and updates the Resource Registry in `.specify/instructions.md`.

8. **Report** — Outputs the file path, agent ID, example trigger prompts, and suggested next customizations.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Agent files | `.specify/agents/<name>.agent.md` |
| Workspace files | `.specify/agents/AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md` |

## Symlink Model

Tool-specific directories are **directory-level symlinks** to `.specify/agents/`:
- `.github/agents/` → `.specify/agents/` (Copilot, Claude Code)
- `.qoder/agents/` → `.specify/agents/` (Qoder)
- `.qwen/agents/` → `.specify/agents/` (Qwen Code)
- `.opencode/agents/` → `.specify/agents/` (opencode)

## Companion Skills

- `create-agent` — Create new role-based agent templates in `templates/`
- `improve-agent` — Iteratively improve agent templates from execution feedback

## Prerequisites

- `specify init` (project initialized)

## Next Steps

- Run [`/speckit.instructions`](instructions.md) to refresh discovery metadata
