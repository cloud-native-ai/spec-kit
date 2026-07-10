# Test Scenario: Single-Entry Intent Routing — `/speckit.agents`

Layer-2 structural scenario for the single agent command entry point.
Contract: [agents-command-contract.md](../../../.specify/specs/023-agent-framework-redesign/contracts/agents-command-contract.md) A1–A6; FR-019, FR-001, FR-002.

## Scenario Description

A user invokes the single `/speckit.agents` command with different natural-language
intents. The command recognizes each intent and routes it to the correct skill —
without any other agent-specific command existing, and without rendering templates inline.

## Setup

### Single Entry Point (A1)

```yaml
command: /speckit.agents
is_only_agent_command: true          # no create-agent / organize-agents command exists
delegates_to_skills: true            # never renders templates inline
```

### Intent → Capability Routing Table (A2)

```yaml
routes:
  - intent: "create a new agent"
    capability: authoring
    skill: create-agent
  - intent: "refine / improve an existing agent"
    capability: authoring
    skill: improve-agent
  - intent: "organize agents in parallel"
    capability: orchestration
    skill: organize-agents
  - intent: "run these agents as a serial chain"
    capability: orchestration
    skill: organize-agents
  - intent: "execute a team / run a team loop"
    capability: orchestration
    skill: organize-agents
```

### Inputs

- I1: "Create a security-review agent" → authoring / create-agent
- I2: "Improve the qa-engineer agent" → authoring / improve-agent
- I3: "Organize a parallel dispatch of three reviewers" → orchestration / organize-agents
- I4: "Run planning → design → implementation as a serial chain" → orchestration / organize-agents
- I5: "Execute the review team as a closed loop" → orchestration / organize-agents
- I6 (ambiguous): "do the agent thing" → capability report + intent request

## Expected Behavior

### E1: Create Intent (I1)
1. Command recognizes authoring intent (new agent).
2. Routes to `create-agent`; no inline template rendering.

### E2: Refine Intent (I2)
1. Command detects an existing agent target.
2. Routes to `improve-agent`.

### E3: Organize — Parallel (I3)
1. Command recognizes orchestration intent (parallel topology).
2. Routes to `organize-agents`.

### E4: Organize — Serial (I4)
1. Recognizes orchestration intent (serial chain).
2. Routes to `organize-agents`.

### E5: Execute — Team Loop (I5)
1. Recognizes orchestration/execution intent (team closed-loop: Workers + Meta + Team Supervisor).
2. Routes to `organize-agents`. The formerly separate Meta-Coordinator role is no longer referenced (merged into Team Supervisor).

### E6: Ambiguous Intent (I6)
1. Command does NOT guess silently and does NOT fail without a message.
2. Reports recognized capabilities (create / organize / execute) and requests the missing intent.

## Verification Points

### V1: Single Entry (A1, SC-001, FR-001)
- [ ] `/speckit.agents` is the only agent-specific command
- [ ] No standalone create-agent / organize-agents / execute command exists
- [ ] All create / organize / execute operations are reachable through it

### V2: Intent Routing (A2, FR-002)
- [ ] Create intent routes to `create-agent`
- [ ] Refine intent routes to `improve-agent`
- [ ] Organize (parallel / serial / team-loop) routes to `organize-agents`
- [ ] Execute (team / loop) routes to `organize-agents`

### V3: Delegation (A2)
- [ ] Command delegates to skills and does NOT render templates inline

### V4: Ambiguous / Unsupported Intent (A3, FR-019)
- [ ] On ambiguous intent, capabilities are reported and the missing intent is requested
- [ ] The command never guesses silently or fails without a message

### V5: Merged Team Supervisor (A5, FR-007)
- [ ] Team closed-loop comprises Workers + Meta + a single Team Supervisor
- [ ] The deprecated Meta-Coordinator role is not referenced anywhere in the routing description (merged into Team Supervisor)

### V6: Provider Whitelist (A6)
- [ ] Unsupported providers are rejected; approved-provider whitelist preserved

## Success Criteria

- Every agent operation is reachable through `/speckit.agents` alone (SC-001).
- Each intent routes to the correct skill with no inline template rendering.
- Ambiguous input yields a capability report, never a silent guess (FR-019).
- The routing model references the merged Team Supervisor, never the formerly separate Meta-Coordinator role.
