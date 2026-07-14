# Command & Skills

This document describes the **operational surface** of the Agent framework: the single-agent
`/speckit.agents` command, how it recognizes intent and routes to skills, the single-agent
authoring/refinement skills, and the temporary/persistent agent lifecycle. Multi-agent teams
are owned by a separate command (`/speckit.team`) and the team skills (`create-team`,
`improve-team`). For the underlying concept model see [design.md](./design.md).

## The single-agent entry point: `/speckit.agents`

`/speckit.agents` is the **only** single-agent command. It creates or refines **one** agent;
team operations (organize / run several agents) are directed to `/speckit.team`. Its contract:

- It **recognizes intent**, then **routes to the owning skill**.
- It **delegates** — it never renders templates inline.
- Persistent agents are always written to the canonical location `.specify/agents/<name>.agent.md`;
  tool-specific directories are symlinks and are **never** written to directly.

> Source: `templates/commands/agents.md` (installed as the `/speckit.agents` command).

### Intent → capability routing

| Recognized intent | Capability | Delegates to skill |
|-------------------|------------|--------------------|
| Create a new agent | authoring | `create-agent` |
| Refine / improve an existing agent | authoring | `improve-agent` |
| Organize / run a team of agents | out of scope | redirect to `/speckit.team` |

**Routing flow:**

1. **Recognize intent** from `$ARGUMENTS` and conversation/repo context — is this
   single-agent *authoring* (create/refine), or a *team* request?
2. **Authoring** → check whether `.specify/agents/<name>.agent.md` exists: absent →
   `create-agent`; present → `improve-agent`. Build the `AgentAuthoringRequest`, handle
   backup/preservation, write to `.specify/agents/`, verify per-file symlinks.
3. **Team request** → do **not** handle it here; direct the user to `/speckit.team` and stop.
4. **Ambiguous / unsupported** → do **not** guess silently. Report the recognized single-agent
   capabilities (create / refine) and request the missing intent (FR-019).

### Team topologies (owned by `/speckit.team`)

Organizing and running multiple agents (parallel / serial / team closed-loop) is owned by the
team domain — the `create-team` skill via `/speckit.team`. Operational detail lives in
[multi-agent-orchestration.md](./multi-agent-orchestration.md).

## The single-agent skills

`/speckit.agents` owns no logic of its own beyond routing; the work is done by two skills.

### `create-agent` — authoring engine

The single authoring engine. Given a `kind`, it produces the corresponding artifact from
templates under `skills/create-agent/templates/`:

| `kind` | Produces | Key source templates |
|--------|----------|----------------------|
| `role` | One role-based agent (six mandatory sections) | `agent-role-*-template.md` |
| `supervisor` | A role agent that runs its own EEI loop | role template + `agent-supervision-delegation.md` (inlined) |
| `custom` | A single narrow, general-purpose custom `.agent.md` (not project-bound) | free-form per intent |
| `project-custom` | A project-bound custom agent (marks its project + carries a scope guard) | `agent-project-custom-template.md` |

Key rules:
- **Supervision is active by default** (`supervisor: true`); the delegation snippet is
  **composed at generation time**, never copied into role templates — edit it only in
  `agent-supervision-delegation.md` (single source of truth).
- It operates on **templates**, not on generated agents in `.specify/agents/`.
- It accepts an `AgentAuthoringRequest` (`kind`, `role_slug`, `task`, `scoring_dimensions[]`,
  `threshold`, `max_iterations`, environment/workspace paths, `project_context`) and returns
  an `AuthoringResult` (`artifact_paths`, `kind`, `status`).

### `improve-agent` — refinement engine

Improves **any existing agent artifact** from real-usage evidence (user feedback, failure
cases, behavioral drift). It first classifies the target, then routes:

| Target kind | Match | Route |
|-------------|-------|-------|
| role | `agent-role-*-template.md` | six-section root-cause workflow |
| supervision snippet | `agent-supervision-delegation.md` | steps 3–5; **warns** the edit affects every supervisor |
| custom | `.specify/agents/*.agent.md` | six-section workflow against the generated file |

Changes must be **evidence-based** and **minimal**, preserving established structure. To adjust
a multi-agent **team** (stages, orchestration, thresholds), use `improve-team` via `/speckit.team`.

> **Team orchestration**: organizing and running multiple agents is owned by the team domain —
> the `create-team` skill via `/speckit.team`. It selects a pattern (Parallel Dispatch / Serial
> Chain / Team Loop) via a decision tree and enforces territory validation, DAG (no-cycle)
> validation, a mandatory max-iteration cap, file-path-only handoff, and context isolation.
> See [multi-agent-orchestration.md](./multi-agent-orchestration.md) for full protocols.

## Agent lifecycle: temporary vs persistent

Every agent `create-agent` can produce has one of two lifecycles; choose it before generating files.

| Lifecycle | Where it lives | When to use | Tool config |
|-----------|----------------|-------------|-------------|
| **temporary** | Context-only — never written to disk | A worker/stage agent spawned for a single Loop or orchestration run; discarded when the run ends | None; exists only in the orchestrator's context (FR-011) |
| **persistent** | `.specify/agents/<slug>.agent.md` (canonical store) | A reusable role or supervisor kept across sessions | Per-file symlinked into every supported tool's agent dir on init (FR-010/012) |

**Persistent generation rules:**
- Write to `.specify/agents/<slug>.agent.md` (single source of truth).
- On initialization the CLI (re)creates a **per-file** symlink for each `.specify/agents/*.agent.md`
  inside each supported tool's agent dir — e.g. `.qoder/agents/<slug>.agent.md → ../../.specify/agents/<slug>.agent.md`,
  plus `.github/agents`, `.qwen/agents`, `.opencode/agents` (and `.hermes/agents`, `.iflow/agents`
  where supported). Each tool `agents/` is a real directory of links; never write tool-specific
  copies of framework agents.
- Agents are discovered by globbing `.specify/agents/*.agent.md` (frontmatter `name`/`description`); there is no separate registry file.

## Tool integration & provider whitelist

- **Approved providers**: Claude Code, GitHub Copilot, Qwen Code, opencode, Qoder — anything
  else is rejected at validation time.
- Each skill runs an **Agent-Specific Configuration** step: it identifies the executing agent
  from detection signals, optionally loads a `references/<agent-slug>-guide.md`, and captures
  execution feedback to `.specify/memory/feedback/` when a genuine agent-specific obstacle
  occurs.
- **Frontmatter baseline** for generated agents:

  ```yaml
  ---
  name: "<required: unique identifier>"
  description: "<required: trigger words + when to use>"
  tools: [Read, Grep, Glob]
  model: auto
  maxTurns: 12
  ---
  ```

  Supported fields: `name` (required), `description` (required), `tools`, `disallowedTools`,
  `model` (`auto`/`lite`/`efficient`/`performance`/`ultimate`), `maxTurns`, `timeoutMins`, `skills`,
  `mcpServers`, `permissionMode`, `background`, `isolation`, `color`, plus the framework fields
  `user-invocable`, `disable-model-invocation`, `supervisor`, `role-scope`. Validation rejects
  invalid YAML, unsupported providers, and unresolved contradictions.

## Skill Enablement convention

Because framework skills and agent definitions install together, every installed skill is
invocable by every agent. The seven built-in role agents make this explicit and consistent so
they prefer a purpose-built framework skill over improvising the same operation. Each role agent
(and its `agent-role-*-template.md` generator) declares two things:

1. **`skills:` frontmatter** — a YAML list of the canonical slugs of the installed skills
   relevant to that role (e.g. `skills: [draw-plantuml, memory-recall, memory-record, think-skills]`).
   Slugs MUST resolve to an installed `.specify/skills/<slug>/SKILL.md`. Meta/framework-authoring skills (`create-agent`, `improve-agent`,
   `create-skills`, `improve-skills`, `create-team`, `improve-team`) are **non-declarable** and never appear
   in a role agent's list.
2. **A `## Skill Enablement` body section** — the shared preference protocol (single source of
   truth at `skills/create-agent/templates/agent-skill-enablement.md`, composed rather than
   reworded per agent) plus a `| Skill | When to use |` table whose skill set equals the
   `skills:` list. The protocol directs the agent to prefer an applicable skill, choose the most
   role-specific one when several apply, and degrade gracefully to direct execution (surfacing
   the failure) when no skill applies or a skill is unavailable.

The contract test `tests/contract/test_agent_skill_enablement.py` enforces this convention
(≥1 declared skill per agent, all references installed, no non-declarable slugs, section present,
and template parity).

## Handoffs

After creating or updating agents, run `/speckit.instructions` to refresh discovery metadata.
Optionally run `/speckit.skills` first if an agent depends on a new skill, or `/speckit.tools`
for tool records.

## Traceability

Normative source: `.specify/specs/023-agent-framework-redesign/contracts/agents-command-contract.md`
and the skill contracts. See also `skills/create-agent/SKILL.md`,
`skills/improve-agent/SKILL.md`, and the team skills `skills/create-team/SKILL.md`,
`skills/improve-team/SKILL.md`.
