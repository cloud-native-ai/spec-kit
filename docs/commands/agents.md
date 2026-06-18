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
