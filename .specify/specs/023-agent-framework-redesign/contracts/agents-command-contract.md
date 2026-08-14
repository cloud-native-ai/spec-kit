# Contract: `/speckit.agents` Single Entry

**Spec**: [requirements.md](../requirements.md) | **Plan**: [plan.md](../plan.md)

Normative behavior for the single agent command entry point. Keywords per RFC 2119.

## A1. Single Entry Point

`/speckit.agents` MUST be the only agent-specific command. No additional agent command MUST be introduced (FR-001). All create / organize / execute operations MUST be reachable through it.

## A2. Intent Recognition & Routing

The command MUST first recognize user intent from natural-language input, then route:

| Recognized intent | Routes to | Skill |
|-------------------|-----------|-------|
| Create / refine an agent | authoring | `create-agent` (new) / `improve-agent` (existing) |
| Organize agents (parallel / serial / team-loop) | orchestration | `organize-agents` |
| Execute a team / run a loop | orchestration | `organize-agents` |

The command MUST delegate to skills (Delegation Model) and MUST NOT render templates inline.

## A3. Ambiguous / Unsupported Intent

When intent is ambiguous or unsupported, the command MUST report the recognized capabilities and request the missing intent. It MUST NOT guess silently or fail without a message (FR-019).

## A4. Lifecycle

- Temporary agents MUST be recorded in context only (not written to the agent directory).
- Persistent agents MUST be written under `.specify/agents/` and MUST be made available to **all officially supported tools** on initialization (FR-010/011/012), e.g. `.qoder/agents` → `.specify/agents`.

## A5. Collaboration Scenarios

The command MUST support three scenarios via `organize-agents`: **parallel**, **serial**, **team closed-loop**. The team closed-loop MUST comprise Worker agents, Meta agents, and a Team Supervisor (FR-008/009).

## A6. Provider Whitelist

The command MUST reject unsupported providers and preserve the approved-provider whitelist (Constitution V).
