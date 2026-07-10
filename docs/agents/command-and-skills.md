# Command & Skills

This document describes the **operational surface** of the Agent framework: the single
`/speckit.agents` command, how it recognizes intent and routes to skills, the three skills
that do the real work, and the temporary/persistent agent lifecycle. For the underlying
concept model see [design.md](./design.md).

## The single entry point: `/speckit.agents`

`/speckit.agents` is the **only** agent-specific command. There is no separate create,
organize, or execute command. Its contract:

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
| Organize agents — parallel | orchestration | `organize-agents` |
| Organize agents — serial chain | orchestration | `organize-agents` |
| Execute a team / run a team closed-loop | orchestration | `organize-agents` |

**Routing flow:**

1. **Recognize intent** from `$ARGUMENTS` and conversation/repo context — is this
   *authoring* (create/refine) or *orchestration* (organize/execute)?
2. **Authoring** → check whether `.specify/agents/<name>.agent.md` exists: absent →
   `create-agent`; present → `improve-agent`. Build the `AgentAuthoringRequest`, handle
   backup/preservation, write to `.specify/agents/`, verify symlinks, update the registry.
3. **Orchestration** → identify the topology (parallel / serial / team-loop) and delegate
   to `organize-agents`, which selects the matching orchestration template.
4. **Ambiguous / unsupported** → do **not** guess silently. Report the recognized
   capabilities (create / refine / organize / execute) and request the missing intent (FR-019).

### Collaboration topologies (delegated to `organize-agents`)

- **parallel** — many agents dispatched together (single response, many delegations).
- **serial** — an ordered chain where each stage's output feeds the next.
- **team closed-loop** — Worker agents + a single **Team Supervisor** iterate to a quality
  threshold. The loop has **two layers** (Team Supervisor + Workers); the
  formerly separate Meta-Coordinator is merged into the Team Supervisor — no separate role.

Operational detail for all three lives in [multi-agent-orchestration.md](./multi-agent-orchestration.md).

## The three skills

`/speckit.agents` owns no logic of its own beyond routing; the work is done by three skills.

### `create-agent` — authoring engine

The single authoring engine. Given a `kind`, it produces the corresponding artifact from
templates under `skills/create-agent/templates/`:

| `kind` | Produces | Key source templates |
|--------|----------|----------------------|
| `role` | One role-based agent (six mandatory sections) | `agent-role-*-template.md` |
| `supervisor` | A role agent that runs its own EEI loop | role template + `agent-supervision-delegation.md` (inlined) |
| `triad` | 3 stage agents (executor/evaluator/optimizer) + orchestration prompt | `agent-stage-*` + `agent-triad-orchestration-template.md` |
| `custom` | A single narrow custom `.agent.md` | free-form per intent |
| `team-supervisor` | The merged Team Supervisor (Meta role) | `agent-role-team-supervisor-template.md` |

Key rules:
- **Supervision is active by default** (`supervisor: true`); the delegation snippet is
  **composed at generation time**, never copied into role templates — edit it only in
  `agent-supervision-delegation.md` (single source of truth).
- It operates on **templates**, not on generated agents in `.specify/agents/`.
- It accepts an `AgentAuthoringRequest` (`kind`, `role_slug`, `task`, `scoring_dimensions[]`,
  `threshold`, `max_iterations`, environment/workspace paths, `project_context`) and returns
  an `AuthoringResult` (`artifact_paths`, `kind`, `status`, `registry_entry`).

### `improve-agent` — refinement engine

Improves **any existing agent artifact** from real-usage evidence (user feedback, failure
cases, behavioral drift). It first classifies the target, then routes:

| Target kind | Match | Route |
|-------------|-------|-------|
| role | `agent-role-*-template.md` | six-section root-cause workflow |
| stage | `agent-stage-{executor,evaluator,optimizer}-template.md` | Triad Refinement (per-stage fixes) |
| orchestration | `agent-triad-orchestration-template.md` | Triad Refinement (loop/threshold/handoff) |
| supervision snippet | `agent-supervision-delegation.md` | steps 3–5; **warns** the edit affects every supervisor |
| custom | `.specify/agents/*.agent.md` | six-section workflow against the generated file |

Changes must be **evidence-based** and **minimal**, preserving established structure.

### `organize-agents` — orchestration engine

The single orchestration skill for all multi-agent coordination. It selects a pattern via a
decision tree:

1. Independent sub-tasks, no shared mutable state → **Parallel Dispatch**
2. Strict sequence (output of A feeds B) → **Serial Chain**
3. Deliverable needs iterative quality improvement by a team → **Team Loop**

Shared hard constraints across patterns: territory validation before parallel dispatch,
DAG (no-cycle) validation before serial chain, a mandatory max-iteration cap for team loops,
**file-path-only handoff** (never paste content between agents), context isolation (each
invocation is a fresh subagent), and idempotent execution. See
[multi-agent-orchestration.md](./multi-agent-orchestration.md) for full protocols.

## Agent lifecycle: temporary vs persistent

Every agent `create-agent` can produce has one of two lifecycles; choose it before generating files.

| Lifecycle | Where it lives | When to use | Tool config |
|-----------|----------------|-------------|-------------|
| **temporary** | Context-only — never written to disk | A worker/stage agent spawned for a single Loop or orchestration run; discarded when the run ends | None; exists only in the orchestrator's context (FR-011) |
| **persistent** | `.specify/agents/<slug>.agent.md` (canonical store) | A reusable role, supervisor, or triad kept across sessions | Linked into every supported tool's agent dir on init (FR-010/012) |

**Persistent generation rules:**
- Write to `.specify/agents/<slug>.agent.md` (single source of truth).
- On initialization the CLI (re)creates a directory symlink from each supported tool's agent
  dir to `.specify/agents/` — e.g. `.qoder/agents → .specify/agents`, plus `.github/agents`,
  `.qwen/agents`, `.opencode/agents` (and `.hermes/agents`, `.iflow/agents` where supported).
  Never write tool-specific copies; symlinks keep every tool in sync.
- Record the agent in `.specify/agents/AGENTS.md` so it is discoverable.

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
  description: "<required: trigger words + when to use>"
  tools: ["read", "search"]
  ---
  ```

  Supported fields: `name`, `tools`, `model`, `argument-hint`, `agents`, `user-invocable`,
  `disable-model-invocation`, `handoffs`. Validation rejects invalid YAML, unsupported
  providers, and unresolved contradictions.

## Handoffs

After creating or updating agents, run `/speckit.instructions` to refresh discovery metadata.
Optionally run `/speckit.skills` first if an agent depends on a new skill, or `/speckit.tools`
for tool records.

## Traceability

Normative source: `.specify/specs/023-agent-framework-redesign/contracts/agents-command-contract.md`
and the two skill contracts. See also `skills/create-agent/SKILL.md`,
`skills/improve-agent/SKILL.md`, and `skills/organize-agents/SKILL.md`.
