# Agent Authoring Contract

> Added by Plan Amendment (2026-07-02). Defines how the `/speckit.agents` command delegates agent authoring to the general-purpose `create-agent` / `improve-agent` skills, and the request shape for advanced (supervisor + triad) agents. Companion to `triad-protocol.md` (which governs the runtime EEI loop between orchestrator and sub-agents).

## Overview

`create-agent` and `improve-agent` are the single authoring engine for all agent artifacts. `/speckit.agents` gathers project context and delegates; it MUST NOT re-implement template rendering.

```
/speckit.agents  ──(AgentAuthoringRequest)──►  create-agent | improve-agent
      │                                                │
      │  gathers project context                       │  renders templates,
      │  handles backup/preservation,                  │  writes artifacts,
      │  symlinks, registry updates                    │  validates, reports
      └──────────────◄──(AuthoringResult)──────────────┘
```

## Contract: `/speckit.agents` → `create-agent`

### Input: AgentAuthoringRequest

| Field | Required | Applies to `kind` | Description |
|-------|----------|-------------------|-------------|
| kind | MUST | all | `role` \| `supervisor` \| `triad` \| `custom` |
| role_slug | MUST for `role`,`supervisor` | role, supervisor | Kebab-case role identity |
| task | MUST for `supervisor`,`triad` | supervisor, triad | What the executor produces |
| scoring_dimensions | MUST for `supervisor`,`triad` | supervisor, triad | Array of `{name, weight, description}` |
| threshold | SHOULD | supervisor, triad | Acceptance score (default from role) |
| max_iterations | SHOULD | supervisor, triad | Loop cap (default 20) |
| environment_paths | MUST for `supervisor`,`triad` | supervisor, triad | Executor reference paths |
| workspace_paths | MUST for `supervisor`,`triad` | supervisor, triad | Improver-editable paths |
| project_context | MUST | all | Resolved `{{PLACEHOLDER}}` map gathered by the command |

### Output: AuthoringResult

| Field | Required | Description |
|-------|----------|-------------|
| artifact_paths | MUST | Files written (`.agent.md`, sub-role agents, orchestration prompt) |
| kind | MUST | Echo of the authored kind |
| status | MUST | `success` or `error` with description |
| registry_entry | SHOULD | Structured row for `.specify/instructions.md` § Resource Registry → Agents |

### Constraints

- `create-agent` MUST validate frontmatter and required sections before write (unchanged from current skill).
- For `kind: supervisor`, `create-agent` MUST compose the role template with the shared **Supervision & EEI Delegation** section and bind `{{ROLE_SCOPE}}` to `role_slug`.
- `create-agent` MUST write to canonical `.specify/agents/` (and `templates/` for reusable role templates), never to symlinked tool dirs.
- `/speckit.agents` MUST retain backup/preservation (FR-008/FR-008a), symlink discoverability checks, and registry updates — these are NOT delegated.

## Contract: `/speckit.agents` → `improve-agent`

### Input

| Field | Required | Description |
|-------|----------|-------------|
| target | MUST | Path or identifier resolving to exactly one authored artifact: role template, `agent-subrole-*`, `agent-triad-orchestration-*`, or `.specify/agents/*.agent.md` |
| improvement_direction | MUST | What to change, with evidence |
| iteration_history | SHOULD | For triad-layer refinement (score trajectory + change logs) |

### Output

| Field | Required | Description |
|-------|----------|-------------|
| changes | MUST | List of `{target, description, rationale}` |
| status | MUST | `success` or `error` |

### Constraints

- `improve-agent` MUST classify the target kind first, then route to the matching refinement rules (role vs. sub-role vs. orchestration vs. custom).
- Changes MUST be evidence-based and minimal (unchanged principle).

## Normative Rules

- **R1**: `/speckit.agents` MUST NOT contain inline template-rendering logic once delegation lands; both modes route through `create-agent`.
- **R2**: A `supervisor` artifact MUST embed a dormant delegation section even when `supervisor: false`, so it can be activated without re-authoring (resolves OQ-1 default-off recommendation).
- **R3**: Every edited `templates/` or `skills/` file MUST be mirrored to its `.specify/` runtime counterpart in the same change (review finding F4).
- **R4**: The advanced-agent request MUST reuse the four existing EEI templates (`agent-subrole-*`, `agent-triad-orchestration-*`); no new sub-role template files are introduced.
