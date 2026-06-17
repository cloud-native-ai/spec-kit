# Quick Start Guide

This guide walks you through the complete Spec Kit workflow in three phases: **Setup**, **Customize**, and **Develop**.

## Phase 1: Setup

### Install and Initialize

Initialize your project with the `specify` CLI:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init <PROJECT_NAME>
```

Or initialize in the current directory:

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init .
```

Specify your AI assistant explicitly (optional):

```bash
specify init <PROJECT_NAME> --ai copilot   # GitHub Copilot
specify init <PROJECT_NAME> --ai claude    # Claude Code
specify init <PROJECT_NAME> --ai qwen     # Qwen Code
specify init <PROJECT_NAME> --ai opencode  # opencode
specify init <PROJECT_NAME> --ai qoder    # Qoder
```

### What `specify init` Creates

After initialization, your project has a `.specify/` directory with the following structure:

```text
.specify/
├── instructions.md          # AI agent instructions (symlinked to CLAUDE.md, etc.)
├── memory/                  # Project memory (constitution, features, knowledge)
│   ├── constitution.md      # Core principles and governance rules
│   └── features.md          # Feature index
├── templates/               # Spec/plan/task templates
├── scripts/                 # Automation scripts (bash)
├── skills/                  # Installed skills (analysis, draw, create-skills, etc.)
├── agents/                  # Agent workspace (bundled + generated agents)
│   ├── code-reviewer.agent.md  # Pre-installed agent
│   └── references/          # Shared reference materials for agents
└── specs/                   # Feature specifications (created per feature)
```

Symlinks are created for your AI tool:
- `.github/agents/` → `.specify/agents/` (Copilot, Claude Code)
- `.qoder/agents/` → `.specify/agents/` (Qoder)
- `.qwen/agents/` → `.specify/agents/` (Qwen Code)
- `.opencode/agents/` → `.specify/agents/` (opencode)

The same symlink model applies to skills directories.

### Generate Role-Based Agents

After initialization, run `/speckit.agents` (no arguments) to generate six development workflow agents tailored to your project:

```text
/speckit.agents
```

This generates:

| Agent | File | Role |
|-------|------|------|
| Requirements Analyst | `requirements-analyst.agent.md` | Clarifies and structures requirements from stakeholder input |
| System Designer | `system-designer.agent.md` | Designs system-level architecture and implementation approaches |
| Module Designer | `module-designer.agent.md` | Designs detailed implementations within specific modules |
| Test Engineer | `test-engineer.agent.md` | Designs and executes acceptance tests |
| QA Engineer | `qa-engineer.agent.md` | Validates system quality against design and requirements |
| Knowledge Manager | `knowledge-manager.agent.md` | Maintains documentation and project knowledge |

Each agent is populated with your project's actual context (tech stack, directory structure, constitution, features).

---

## Phase 2: Customize (Optional)

You can use the built-in agents and skills as-is, or create custom ones for your project's specific needs.

### Create Custom Agents

Use the `create-agent` skill to define new role-based agent templates:

```text
/create-agent A security auditor who reviews code changes for OWASP vulnerabilities
```

Use the `improve-agent` skill to refine agents based on usage feedback:

```text
/improve-agent The requirements-analyst agent should ask more targeted questions about data privacy
```

### Create Custom Skills

Use the `create-skills` skill to define new reusable workflows:

```text
/create-skills api-testing - Validates API endpoints against OpenAPI specifications
```

Use the `improve-skills` skill to iterate on existing skills:

```text
/improve-skills The draw-plantuml skill should support C4 model diagrams
```

### Pre-installed Skills

Spec Kit ships with these skills ready to use:

- `analysis-project` — Deep architecture analysis reports
- `draw-plantuml` — System architecture diagrams via PlantUML
- `draw-echarts` — Data visualizations via Apache ECharts
- `draw-d3js` — Interactive D3.js visualizations
- `create-skills` / `improve-skills` — Skill lifecycle management
- `create-agent` / `improve-agent` — Agent template lifecycle management
- `think-skills` — Dry-run simulation of skills

---

## Phase 3: Develop

Use the standard Spec Kit development workflow. Agents and skills assist naturally at each stage — they are auxiliary aids, not required dependencies.

### The SDD Workflow

```text
/speckit.feature → /speckit.requirements → /speckit.clarify → /speckit.plan → /speckit.tasks → /speckit.implement → /speckit.review
```

### Step 1: Define Requirements

```text
/speckit.requirements Build a task management app with Kanban boards, drag-and-drop, and user assignment
```

The `@requirements-analyst` agent can help translate business language into structured requirements when you need interactive clarification.

### Step 2: Clarify Ambiguities

```text
/speckit.clarify
```

Resolves `[NEEDS CLARIFICATION]` markers and binds the spec to a Feature.

### Step 3: Create Technical Plan

```text
/speckit.plan Use React with TypeScript, PostgreSQL, and REST APIs
```

The `@system-designer` agent can help evaluate architectural trade-offs from a holistic project perspective.

### Step 4: Break Down into Tasks

```text
/speckit.tasks
```

### Step 5: Implement

```text
/speckit.implement
```

The `@module-designer` and `@test-engineer` agents can assist with module-level design and test-first development during implementation.

### Step 6: Review

```text
/speckit.review
```

The `@qa-engineer` agent can help validate that the implementation satisfies both the architectural design and the original requirements.

### Auxiliary Commands

These commands support the core workflow at any stage:

| Command | When to Use |
|---------|-------------|
| `/speckit.research` | Need external data to inform requirements or planning |
| `/speckit.clarify` | Specifications have unresolved ambiguities |
| `/speckit.checklist` | Need quality gates before implementation |
| `/speckit.analyze` | Check cross-artifact consistency at any stage |
| `/speckit.constitution` | Update project governance principles |
| `/speckit.instructions` | Refresh AI agent instructions after changes |

---

## Example: Building Taskify

Here's a complete walkthrough using the three-phase model.

### Phase 1: Setup

```bash
uvx --from git+https://github.com/github/spec-kit.git specify init taskify --ai copilot
```

Then generate role-based agents:

```text
/speckit.agents
```

### Phase 2: Skip (use defaults)

The built-in agents and skills are sufficient for this project.

### Phase 3: Develop

**Define requirements:**

```text
/speckit.requirements Develop Taskify, a team productivity platform with Kanban boards. Users can create projects, add team members, assign tasks, comment, and drag-and-drop tasks between status columns. Start with 5 predefined users (1 PM, 4 engineers), 3 sample projects, standard Kanban columns (To Do, In Progress, In Review, Done). No login required for initial testing.
```

**Refine and clarify:**

```text
For each project, create 5-15 tasks randomly distributed across columns, with at least one task per column.
```

**Generate technical plan:**

```text
/speckit.plan Use .NET Aspire with Postgres, Blazor Server frontend with drag-and-drop, REST APIs for projects, tasks, and notifications.
```

**Break down and implement:**

```text
/speckit.tasks
/speckit.implement
```

**Review:**

```text
/speckit.review
```

## Key Principles

- **Be explicit** about what you're building and why
- **Don't focus on tech stack** during the specification phase
- **Iterate and refine** requirements before implementation
- **Validate** the plan before coding begins
- **Use agents as consultants** — invoke them for their role perspective, not as required gatekeepers
- **Use skills for repeatability** — codify workflows you run more than once

## Next Steps

- [Usage Guide](usage.md) — Full command reference and workflow details
- [Spec-Driven Development](spec-driven.md) — Methodology deep-dive
- [Installation Guide](installation.md) — Detailed setup options
