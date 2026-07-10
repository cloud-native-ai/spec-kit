---
name: create-agent
description: General-purpose authoring skill for Spec Kit agents — creates role, supervisor (role + embedded EEI triad), triad sub-role, or custom agents. Use this when the user mentions ["create an agent", "new agent", "add agent role", "agent template", "supervisor agent", "EEI triad", "创建agent", "新建agent", "添加角色"]
skill_id: "<SKILL:.specify/skills/create-agent/SKILL.md>"
---

# create-agent

## Goal

Author **any agent artifact** for the Spec Kit agent system — a role template, a role-scoped **supervisor** (role + embedded EEI triad), an EEI **triad** (three stage agents + orchestration prompt), or a **custom** `.agent.md`. This skill is the single authoring engine invoked by `/speckit.agents`; the command gathers project context and delegates here rather than rendering templates inline.

## Conceptual Model (Role × Stage × Type + Team/Loop)

Every agent is described by three orthogonal dimensions and organized into a Team/Loop:

- **Role** — the responsibility/perspective; maps to exactly one `agent-role-<role>-template.md`.
- **Stage** — one of `executor`, `evaluator`, `optimizer` (canonical names; the deprecated dimension name "SubRole" and stage name "improver" are removed).
- **Type** — `Worker` or `Meta`, **derived from Stage** (Type-follows-Stage): executor→Worker, evaluator→Meta, optimizer→Meta.
- **Team** (static) — a Role×Stage matrix; **Loop** (dynamic) — the runtime iteration across stages.
- **Team Supervisor** — the single **Meta role** (Meta at all stages, never performs real project tasks). It is the merge of the former Meta-Coordinator (coordination) and Team Supervisor (quality gate); there is no separate Meta-Coordinator.

Canonical template home: `skills/create-agent/templates/` (installed mirror: `.specify/skills/create-agent/templates/`).

## Capability Matrix

Select the capability from the request `kind` (or infer from user intent):

| kind | Produces | Source templates | Primary section |
|------|----------|------------------|-----------------|
| `role` | One role-based agent (six mandatory sections) | `skills/create-agent/templates/agent-role-*-template.md` | Workflow steps 1–5 below |
| `supervisor` | A role agent that runs its own EEI loop | role template + `skills/create-agent/templates/agent-supervision-delegation.md` inlined | § Supervisor Capability |
| `triad` | 3 stage agents (executor/evaluator/optimizer) + orchestration prompt | `skills/create-agent/templates/agent-stage-*` + `agent-triad-orchestration-template.md` | § Triad Mode (EEI Pattern) |
| `custom` | A single narrow custom `.agent.md` | free-form per intent | `/speckit.agents` Mode B flow |
| `team-supervisor` | The merged Team Supervisor (Meta role): task decomposition + quality gating + iteration control | `skills/create-agent/templates/agent-role-team-supervisor-template.md` | § Team Supervisor Mode |

All capabilities share the same validate + report tail (Workflow steps 4–5) and the Agent-Specific Configuration handling below.

## AgentAuthoringRequest Intake

When invoked by `/speckit.agents`, accept the `AgentAuthoringRequest` defined in `.specify/specs/022-eei-agent-triad/contracts/agent-authoring-contract.md` and consume every field: `kind`, `role_slug`, `task`, `scoring_dimensions[]`, `threshold`, `max_iterations`, `environment_paths[]`, `workspace_paths[]`, `project_context`. Missing optional fields fall back to role/triad defaults (threshold from role, `max_iterations`=20). Return an `AuthoringResult` (`artifact_paths`, `kind`, `status`, `registry_entry`).

## Workflow

### 1. Determine the role definition

**Case A — User provided explicit role description**

Parse the role name, responsibilities, and workflow constraints from the user input:

- **Role name**: A concise display name (e.g., "Security Auditor", "DevOps Engineer")
- **Role slug**: Derive kebab-case slug from role name (e.g., `security-auditor`, `devops-engineer`)
- **Responsibilities**: Core duties of this role in a software development workflow
- **Upstream/Downstream**: Who provides inputs and who consumes outputs

**Case B — User provided no input (empty arguments)**

Analyze the conversation history and project context to infer a useful role:

1. Review conversation for recurring task patterns or specialized workflows
2. Identify the role's position in the development workflow
3. Ask one targeted clarification question if the role is ambiguous

### 2. Validate against existing templates

- Check `skills/create-agent/templates/agent-role-*-template.md` for existing roles
- If a similar role exists, suggest updating it via `improve-agent` instead
- Ensure the new role does not overlap significantly with the seven preset roles

### 3. Create the template file

Write `skills/create-agent/templates/agent-role-<slug>-template.md` following the established structure:

```markdown
---
name: {{AGENT_NAME}}
description: {{AGENT_DESCRIPTION}}
user-invocable: true
disable-model-invocation: false
---
You are a **<Role Name>** for the {{PROJECT_NAME}} project.

## Identity & Responsibilities
[First-person professional identity and core duties]

## Project Context
[Project-specific placeholders from approved list]

## Workflow
[Step-by-step workflow for this role]

## Upstream (Inputs)
[Who provides inputs and what format]

## Downstream (Outputs)
[Who consumes outputs and what format]

## Output Format
[Expected output structure]
```

### 4. Validate the template

- Verify YAML frontmatter has required fields (name, description, user-invocable)
- Verify `tools` field is omitted (inherits platform defaults)
- Verify all six mandatory sections are present
- Verify only approved `{{PLACEHOLDER}}` variables are used
- Verify upstream/downstream references are consistent with existing role chain

### 5. Report

- Report the created template file path
- Suggest running `/speckit.agents` to generate the new agent from the template
- Propose how this role fits into the existing workflow chain

## Constraints

- Templates MUST follow the established role-based structure (six mandatory sections)
- Templates MUST use only approved `{{PLACEHOLDER}}` variables
- The `tools` field MUST be omitted from YAML frontmatter
- Role instructions MUST be written in first-person professional identity
- This skill operates on templates in `skills/create-agent/templates/`, NOT on generated agents in `.specify/agents/`

## Agent Lifecycle (temporary vs persistent)

Every agent this skill can produce has one of two lifecycles. Choose the lifecycle before generating files.

| Lifecycle | Where it lives | When to use | Tool config |
|-----------|----------------|-------------|-------------|
| **temporary** | Context-only — never written to disk | A worker/stage agent spawned for a single Loop or orchestration run; discarded when the run ends | None; it exists only in the orchestrator's context (FR-011) |
| **persistent** | `.specify/agents/<slug>.agent.md` (the canonical store) | A reusable role, supervisor, or triad the project keeps across sessions | Linked into every officially supported tool's agent config directory on initialization (FR-010/012) |

**Persistent generation rules**:

- Write the generated agent to `.specify/agents/<slug>.agent.md` (canonical, single source of truth).
- On initialization the CLI (re)creates a directory symlink from each officially supported tool's agent config dir to `.specify/agents/` — e.g. `.qoder/agents → ../.specify/agents`, plus `.github/agents`, `.qwen/agents`, `.opencode/agents`, `.hermes/agents`, `.iflow/agents` — consistent with Feature 022 multi-tool support (FR-012, A4). Never write tool-specific copies; the symlinks keep every tool in sync.
- Record the agent in `.specify/agents/AGENTS.md` so it is discoverable.

**Temporary generation rules**:

- Do NOT write the agent under `.specify/agents/` and do NOT create tool config links. The orchestrator (Team Supervisor) instantiates it from a stage/role template into its own context for the duration of the Loop only (FR-011).

## Triad Mode (EEI Pattern)

Use this mode when the user wants to create an agent that iteratively improves its output through an **Executor-Evaluator-Optimizer** loop (the "EEI triad").

### When to Use

Trigger on phrases: "create triad", "EEI agent", "iterative quality", "executor evaluator optimizer", or any request for a self-refining agent that scores and re-drafts its own output.

### How It Works

Instead of producing a single role template, Triad Mode creates **three stage agents** plus an **orchestration prompt** that wires them into a loop:

1. **Executor** (stage `executor`, Worker) -- performs the core task and produces a draft artifact.
2. **Evaluator** (stage `evaluator`, Meta) -- scores the draft against weighted dimensions, emits a structured rubric, and decides pass/fail against a threshold.
3. **Optimizer** (stage `optimizer`, Meta) -- reads the rubric, rewrites the artifact to address low-scoring dimensions, and feeds the revision back to the Evaluator.

The orchestration prompt drives the loop: Executor -> Evaluator -> (if below threshold) Optimizer -> Evaluator -> ... until the threshold is met or a max-iteration cap is reached.

### Required Inputs

| Input | Description |
|-------|-------------|
| **Task description** | What the Executor should produce (e.g., "generate an API spec") |
| **Scoring dimensions + weights** | Named quality axes and their relative weights (e.g., correctness 0.4, completeness 0.3, clarity 0.3) |
| **Threshold** | Minimum weighted score (0-1) for the Evaluator to accept the artifact |
| **Environment paths** | Project root, templates dir, output dir |
| **Workspace paths** | Where intermediate artifacts and rubrics are written |

### Template Files

All four templates live in `skills/create-agent/templates/`:

- `agent-stage-executor-template.md`
- `agent-stage-evaluator-template.md`
- `agent-stage-optimizer-template.md`
- `agent-triad-orchestration-template.md`

The skill populates placeholders and writes the generated files to `.specify/agents/`.

### Triad Workflow (within this skill)

1. Collect required inputs (prompt or infer from conversation).
2. Validate that all four stage templates exist in `skills/create-agent/templates/`.
3. Generate three stage agent files and one orchestration prompt.
4. Report the created file paths and suggest a test invocation.

## Supervisor Capability

Use this capability (`kind: supervisor`) to author a **role-scoped supervisor** — a role agent that, for quality-gated deliverables, orchestrates its own EEI loop. Per the amendment decisions: supervision is **active by default** (OQ-1) and the delegation section is **composed at generation, not copied into role templates** (OQ-2).

### How it works

1. Load the role template `skills/create-agent/templates/agent-role-<role_slug>-template.md` (it carries `supervisor: true` and `role-scope: <role_slug>` in frontmatter).
2. **Inline the single-source snippet** `skills/create-agent/templates/agent-supervision-delegation.md` into the generated agent body, resolving its placeholders:
   - `{{ROLE_SCOPE}}` → `role_slug`
   - `{{ROLE_NAME}}` → role display name
   - `{{ROLE_DIMENSIONS}}` → the request's `scoring_dimensions` (or role-appropriate defaults if omitted)
3. Preserve `supervisor: true` in the generated frontmatter (honor `supervisor: false` only if the request explicitly opts out).
4. Write the generated agent to `.specify/agents/<role_slug>.agent.md` and run the shared validate + report tail.

### Rule

Never copy the delegation section text into `skills/create-agent/templates/agent-role-*-template.md`; edit it only in `skills/create-agent/templates/agent-supervision-delegation.md` so all supervisors stay in sync (single source of truth).

## Agent-Specific Configuration

### Step 1: Identify Executing Agent

Before executing this skill's workflow, identify which AI agent you are:

| Agent | Detection Signals |
|-------|-------------------|
| **Claude Code** | System prompt contains "Claude Code"; tools include `Agent`, `Edit`, `Bash`, `Read`; `.claude/` directory exists |
| **GitHub Copilot** | Running in VS Code Copilot Chat context; `.github/copilot-instructions.md` loaded; tools include `workspace edit`, `@terminal` |
| **Qoder CLI** | `.qoder/` directory exists; `AGENTS.md` instructions loaded |
| **opencode** | `.opencode/` directory exists |
| **Qwen Code** | `QWEN.md` instructions loaded; `.qwen/` directory exists |
| **Codex CLI** | `.codex/` directory exists |
| **Hermes Agent** | `.hermes/` directory exists |
| **iFlow** | `.iflow/` directory exists |

If you cannot identify your agent, skip Step 2 and proceed with the standard workflow.

### Step 2: Load Agent-Specific Guidance

If you identified your agent in Step 1, check if a guide exists at:

```
${SKILL_HOME}/references/<agent-slug>-guide.md
```

Where `<agent-slug>` is: `claude-code`, `copilot`, `qoder`, `opencode`, `qwen`, `codex`, `hermes`, or `iflow`.

If the guide exists, read it and apply the agent-specific tool mappings, best practices, and pitfall avoidances during execution. If no guide exists for your agent, proceed with the standard workflow.

### Step 3: Capture Execution Feedback

If you encounter an agent-specific obstacle during execution (e.g., a tool call is unavailable, output format doesn't match expectations, a workaround was needed), generate a feedback document at:

```
.specify/memory/feedback/create-agent-<agent-slug>-<YYYY-MM-DDTHH-MM-SS>.md
```

The feedback document MUST contain:

```markdown
# Agent Execution Feedback

**Source**: create-agent
**Agent**: <agent-slug>
**Timestamp**: <ISO-8601>
**Outcome**: <success-with-workaround | partial-failure | full-failure>

## Obstacle
[Description of the agent-specific issue encountered]

## Workaround Applied
[What was done to work around the issue, if anything]

## Suggested Improvement
[Specific change to the skill or reference document that would prevent this issue]
```

Only generate feedback when a genuine agent-specific obstacle was encountered.

## Team Supervisor Mode

Use this mode (`kind: team-supervisor`) to author the merged **Team Supervisor** — the single **Meta role** that unifies task decomposition + worker dispatch (formerly the Meta-Coordinator) with quality gating, iteration control, and convergence detection. There is no separate coordinator mode; both responsibilities live in this one Meta role.

### When to Use

Trigger on phrases: "create team supervisor", "team coordinator", "orchestration agent", "quality gate agent", "iteration supervisor", "team quality control", or any request for an agent that decomposes goals, dispatches workers, evaluates team output, and drives iterative improvement.

### How It Works

1. Collect the **team goal** and the **quality dimensions and weights** (what to build and how to score it).
2. Identify the **worker agent list** (which agents will execute sub-tasks) and the **dispatch strategy**: `parallel` (all at once), `serial` (sequenced), or `mixed` (DAG with some parallel stages).
3. Define the **threshold** (minimum acceptable weighted score).
4. Set **max_iterations** (iteration cap to prevent infinite loops) and **regression_limit** (max consecutive score drops before aborting).
5. Load `skills/create-agent/templates/agent-role-team-supervisor-template.md` and populate placeholders.
6. Write the generated supervisor to `.specify/agents/<team-slug>-supervisor.agent.md`.
7. Run the shared validate + report tail (Workflow steps 4–5).

### Required Inputs

| Input | Description |
|-------|-------------|
| **Team goal** | High-level objective the supervisor will decompose (e.g., "implement feature X") |
| **Worker agent list** | Agents available for dispatch (e.g., module-designer, test-engineer) |
| **Dispatch strategy** | One of `parallel`, `serial`, or `mixed` |
| **Quality dimensions + weights** | Named axes and weights (e.g., correctness 0.4, completeness 0.3, clarity 0.3) |
| **Threshold** | Minimum weighted score (0–1) for acceptance |
| **max_iterations** | Maximum loop iterations before forced stop (default: 5) |
| **regression_limit** | Max consecutive score decreases before abort (default: 2) |
| **Territory definitions** | (Optional) File/directory ownership per worker to prevent conflicts |
