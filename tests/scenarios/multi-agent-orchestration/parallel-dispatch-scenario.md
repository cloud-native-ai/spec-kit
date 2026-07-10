# Test Scenario: Parallel Dispatch — Dual Module Development

## Scenario Description

Two independent modules (`auth` and `payments`) are developed in parallel by separate worker agents, orchestrated by the **Team Supervisor** (Meta role). Each worker runs at the `executor` stage (Type: Worker); the Team Supervisor is Meta at all stages.

## Setup

### Team Configuration

```yaml
supervisor: team-supervisor          # Meta role (coordination merged in)
workers:
  - id: worker-auth
    agent: module-designer
    territory: ["src/auth/", "tests/auth/"]
  - id: worker-payments
    agent: module-designer
    territory: ["src/payments/", "tests/payments/"]
shared_readonly: ["src/types/shared.ts", "src/config/app.ts"]
dispatch_strategy: parallel
```

### Input

- Feature spec: "Implement JWT authentication module and Stripe payments module"
- Shared interface: `src/types/shared.ts` (read-only, pre-defined)

## Expected Behavior

### Phase 1: Territory Division
1. Team Supervisor reads the feature spec and identifies two independent modules.
2. Team Supervisor assigns exclusive territories to each worker.
3. Team Supervisor verifies no territory overlap exists.

### Phase 2: Parallel Dispatch
1. Team Supervisor dispatches both workers simultaneously.
2. Each worker receives: its territory definition, the feature spec subset, and shared type references.
3. Workers begin execution independently.

### Phase 3: Independent Execution
1. `worker-auth` implements JWT auth in `src/auth/`, writes tests in `tests/auth/`.
2. `worker-payments` implements Stripe integration in `src/payments/`, writes tests in `tests/payments/`.
3. Neither worker touches the other's territory or shared files.

### Phase 4: Aggregation
1. Team Supervisor collects completion signals from both workers.
2. Team Supervisor reads each worker's output summary from handoff files.
3. Team Supervisor produces a unified progress report.

## Verification Points

### V1: No File Conflicts
- [ ] No file is modified by more than one worker
- [ ] Shared readonly files remain unmodified
- [ ] Git diff shows changes only within assigned territories

### V2: Result Completeness
- [ ] `worker-auth` produced: implementation files + test files + handoff summary
- [ ] `worker-payments` produced: implementation files + test files + handoff summary
- [ ] Both modules compile independently

### V3: Progress Report Accuracy
- [ ] Team Supervisor report lists both workers and their status
- [ ] Timing data shows parallel (overlapping) execution, not sequential
- [ ] Final report includes file counts and test pass rates per worker

### V4: Error Handling
- [ ] If one worker fails, the other continues to completion
- [ ] Team Supervisor correctly reports partial success
- [ ] Failed worker's territory is flagged for retry

## Success Criteria

- Both modules implemented without file conflicts
- Aggregated report produced within expected timeframe
- No territory violations detected
