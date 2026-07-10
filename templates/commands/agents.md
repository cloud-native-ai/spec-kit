---
description: Single entry point for all agent operations — create, organize, and execute agents via intent routing.
handoffs:
  - label: Update Instructions
    agent: speckit.instructions
    prompt: Refresh project instructions so newly created agents are discoverable.
    send: false
---

> Compatibility: Follow VS Code Copilot custom agent format for `.agent.md` files.

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](skills/sdd-workflow/references/user-input-protocol.md). If empty, infer intent from conversation/repo context. If intent is ambiguous or unsupported, report capabilities and request the missing intent (do NOT guess silently).

## Outline

`/speckit.agents` is the **single entry point** for every agent operation. There is no other agent-specific command. It recognizes intent, then routes to the owning skill. It delegates to skills and does **NOT** render templates inline.

Agents are expressed with the **Role × Stage × Type** model, organized statically as a **Team** (Role×Stage matrix) and dynamically as a **Loop**. Persistent agents are written to the canonical location `.specify/agents/<name>.agent.md`; tool-specific directories are symlinks — never write to them directly.

### Intent → Capability Routing

| Recognized intent | Capability | Delegates to skill |
|-------------------|------------|--------------------|
| Create a new agent | authoring | `create-agent` |
| Refine / improve an existing agent | authoring | `improve-agent` |
| Organize agents — parallel | orchestration | `organize-agents` |
| Organize agents — serial chain | orchestration | `organize-agents` |
| Execute a team / run a team closed-loop | orchestration | `organize-agents` |

**Routing flow**:

1. **Recognize intent** from `$ARGUMENTS` and conversation/repo context: is this *authoring* (create/refine) or *orchestration* (organize/execute)?
2. **Authoring** → check `.specify/agents/<name>.agent.md` existence: absent → `create-agent`; present → `improve-agent`. Build the `AgentAuthoringRequest`, handle backup/preservation, write to `.specify/agents/`, verify symlinks, update registry.
3. **Orchestration** → identify topology (parallel / serial / team-loop) and delegate to `organize-agents`, which selects the matching orchestration template.
4. **Ambiguous / unsupported** → see below.

### Ambiguous or Unsupported Intent (FR-019)

When intent cannot be resolved, the command MUST report the recognized capabilities and request the missing intent. It MUST NOT guess silently or fail without a message. Report this capability listing:

- **create** — author a new agent (role-based or custom) → `create-agent`
- **refine** — improve an existing agent → `improve-agent`
- **organize** — arrange agents into a parallel, serial, or team-loop topology → `organize-agents`
- **execute** — run a team or team closed-loop → `organize-agents`

### Collaboration Topologies (via `organize-agents`)

- **parallel** — many agents dispatched together (single response, many delegations)
- **serial** — an ordered chain where each stage's output feeds the next
- **team closed-loop** — Worker agents + Meta agents + a single **Team Supervisor** iterate to a quality threshold

The Team closed-loop has **two layers**: Team Supervisor (Meta role) + Workers. The former Meta-Coordinator is **merged into the Team Supervisor** — do not reference a separate Meta-Coordinator role.

### Lifecycle: Temporary vs Persistent

- **Temporary** agents live only in conversation context and are NOT written to the agent directory.
- **Persistent** agents are written under `.specify/agents/` and made available to **all officially supported tools** on initialization (e.g. `.qoder/agents` → `.specify/agents`).

### Authoring Rules

- Focus on **what** the agent does and **when to call** it
- Concise, explicit instructions over narrative
- Single responsibility per agent
- Least-privilege tool set
- Approved providers: Claude Code, GitHub Copilot, Qwen Code, opencode, Qoder — reject anything else

### Frontmatter Baseline

```yaml
---
description: "<required: trigger words + when to use>"
tools: ["read", "search"]
---
```

Supported fields: `name`, `tools`, `model`, `argument-hint`, `agents`, `user-invocable`, `disable-model-invocation`, `handoffs`.

### Valid File Locations

- Canonical: `.specify/agents/*.agent.md`
- Canonical (workspace) scope: shared workspace files `AGENTS.md`, `MEMORY.md`, `SOUL.md`, `USER.md`, and shared assets under `.specify/agents/references/`
- Symlinks (read-only): `.github/agents/`, `.qoder/agents/`, `.qwen/agents/`, `.opencode/agents/`

### Validation

- YAML frontmatter must be valid
- Reject unsupported provider references (Provider Whitelist)
- Tool list must match workflow needs
- Unresolved contradictions block save

For agent-specific operational guidance and the Role/Stage/Type + Team/Loop model, see `skills/create-agent/SKILL.md` and `skills/sdd-workflow/references/agent-configuration.md`.

## Handoffs

**Before**: Optional `/speckit.skills` if an agent depends on a new skill. Optional `/speckit.tools` for tool records.

**After**: Run `/speckit.instructions` to sync discoverability.
