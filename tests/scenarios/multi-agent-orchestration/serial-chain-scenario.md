# Test Scenario: Serial Chain — 4-Stage Development Pipeline

## Scenario Description

A feature request flows through a 4-stage serial pipeline: Requirements → Design → Implementation → Testing. Each stage depends on the output of the previous stage, communicated via file handshake.

**Model alignment**: this is a **serial Loop** across four Worker roles (requirements-analyst, system-designer, module-designer, test-engineer). Each agent runs at the `executor` stage (Type: Worker); no Meta role is required for a pure serial chain (a Team Supervisor may optionally gate quality between stages).

## Setup

### Workflow Definition

```yaml
workflow:
  id: feature-pipeline
  stages:
    - id: requirements
      agent: requirements-analyst
      blockedBy: []
      output: .specify/handoff/requirements-output.md
    - id: design
      agent: system-designer
      blockedBy: [requirements]
      output: .specify/handoff/design-output.md
    - id: implement
      agent: module-designer
      blockedBy: [design]
      output: .specify/handoff/implement-output.md
    - id: test
      agent: test-engineer
      blockedBy: [implement]
      output: .specify/handoff/test-output.md
```

### Input

- User story: "As a user, I want to reset my password via email so I can regain access to my account"

## Expected Behavior

### Stage 1: Requirements Analysis
1. `requirements-analyst` receives the user story.
2. Produces structured requirements: acceptance criteria, edge cases, constraints.
3. Writes output to `.specify/handoff/requirements-output.md`.
4. Status transitions: `pending` → `in_progress` → `completed`.

### Stage 2: System Design
1. `system-designer` reads `requirements-output.md` (file handshake).
2. Produces architecture: component diagram, API endpoints, data flow.
3. Writes output to `.specify/handoff/design-output.md`.
4. Only starts after Stage 1 status = `completed`.

### Stage 3: Implementation
1. `module-designer` reads `design-output.md`.
2. Implements the password reset feature in code.
3. Writes summary to `.specify/handoff/implement-output.md`.
4. Only starts after Stage 2 status = `completed`.

### Stage 4: Testing
1. `test-engineer` reads `implement-output.md` and `design-output.md`.
2. Writes and runs tests against the implementation.
3. Writes results to `.specify/handoff/test-output.md`.
4. Only starts after Stage 3 status = `completed`.

## Verification Points

### V1: Dependency Correctness
- [ ] Stage N never starts before Stage N-1 is `completed`
- [ ] DAG validation rejects circular dependencies at startup
- [ ] Adding `blockedBy: [test]` to requirements is correctly rejected

### V2: Context Transfer Completeness
- [ ] Each handoff file contains a metadata header (stage_id, timestamp, status, confidence)
- [ ] Downstream agent can produce correct output solely from the handoff file
- [ ] No critical information is lost between stages

### V3: Interrupt and Resume
- [ ] If Stage 2 crashes, Stage 1 output is preserved in handoff file
- [ ] Restarting the workflow resumes from Stage 2 (not Stage 1)
- [ ] Stage 2 produces identical output on retry with same input

### V4: Progress Tracking
- [ ] Each stage status is visible: `pending` / `in_progress` / `completed` / `failed`
- [ ] Elapsed time per stage is recorded
- [ ] Total pipeline progress is reported as percentage (0/4, 1/4, 2/4, 3/4, 4/4)

### V5: Failure Propagation
- [ ] If Stage 3 fails, Stage 4 remains in `blocked` state (not `pending`)
- [ ] Error details from failed stage are captured in its handoff file
- [ ] Pipeline correctly reports "failed at stage: implement"

## Success Criteria

- All 4 stages execute in correct topological order
- Context is fully transferred via file handshake without prompt-based passing
- Pipeline is resumable from any intermediate failure point
- Final test report correctly validates the implemented feature
