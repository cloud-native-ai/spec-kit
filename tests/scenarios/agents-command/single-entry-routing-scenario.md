# Test Scenario: Single-Entry Intent Routing — `/speckit.agents`

Layer-2 structural scenario for the single **single-agent** command entry point.
Contract: [agents-command-contract.md](../../../.specify/specs/023-agent-framework-redesign/contracts/agents-command-contract.md) A1–A6; FR-019, FR-001, FR-002. Team routing was removed in Feature 027 (Team Management) — all multi-agent/team operations now live behind `/speckit.team`.

## Scenario Description

A user invokes the single `/speckit.agents` command with different natural-language
intents. The command recognizes each **single-agent** intent and routes it to the
correct skill — without rendering templates inline. Team operations (organizing or
running several agents) are NOT served here; they are directed to `/speckit.team`.

## Setup

### Single Entry Point (A1)

```yaml
command: /speckit.agents
scope: single-agent only              # create / refine one agent
delegates_to_skills: true             # never renders templates inline
team_ops: out_of_scope                # organize / run a team → /speckit.team
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
  - intent: "organize / run a team of agents"
    capability: out_of_scope
    redirect: /speckit.team
```

### Inputs

- I1: "Create a security-review agent" → authoring / create-agent
- I2: "Improve the qa-engineer agent" → authoring / improve-agent
- I3 (team): "Organize a parallel dispatch of three reviewers" → redirected to `/speckit.team`
- I4 (ambiguous): "do the agent thing" → capability report + intent request

## Expected Behavior

### E1: Create Intent (I1)
1. Command recognizes authoring intent (new agent).
2. Routes to `create-agent`; no inline template rendering.

### E2: Refine Intent (I2)
1. Command detects an existing agent target.
2. Routes to `improve-agent`.

### E3: Team Intent (I3)
1. Command recognizes a multi-agent/team request.
2. Does NOT handle it; directs the user to `/speckit.team` and stops.

### E4: Ambiguous Intent (I4)
1. Command does NOT guess silently and does NOT fail without a message.
2. Reports recognized single-agent capabilities (create / refine) and requests the missing intent.

## Verification Points

### V1: Single Entry (A1, SC-001, FR-001)
- [ ] `/speckit.agents` is the single entry point for single-agent operations
- [ ] All create / refine operations are reachable through it
- [ ] Team operations are directed to `/speckit.team`, not served here

### V2: Intent Routing (A2, FR-002)
- [ ] Create intent routes to `create-agent`
- [ ] Refine intent routes to `improve-agent`
- [ ] Team/organize/run intents are redirected to `/speckit.team`

### V3: Delegation (A2)
- [ ] Command delegates to skills and does NOT render templates inline

### V4: Ambiguous / Unsupported Intent (A3, FR-019)
- [ ] On ambiguous intent, single-agent capabilities are reported and the missing intent is requested
- [ ] The command never guesses silently or fails without a message

### V5: Provider Whitelist (A6)
- [ ] Unsupported providers are rejected; approved-provider whitelist preserved

## Success Criteria

- Every **single-agent** operation is reachable through `/speckit.agents` alone (SC-001).
- Each intent routes to the correct skill with no inline template rendering.
- Team operations are cleanly redirected to `/speckit.team` (Feature 027 separation).
- Ambiguous input yields a capability report, never a silent guess (FR-019).
