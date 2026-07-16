# Test Scenario: Iteration — API Specification Writing Team

## Scenario Description

An API specification is iteratively refined by a team of three workers (Writer, Reviewer, Optimizer) under the supervision of a Team Supervisor, until quality threshold is met or max iterations are exhausted. The team has **two layers**: the Team Supervisor (Meta role — coordination + quality gate) and the Workers.

## Setup

### Team Configuration

```yaml
team:
  supervisor:
    agent: team-supervisor          # Meta role: coordination + quality gate (merged)
    dispatch_strategy: serial
    threshold: 0.85
    max_iterations: 5
    regression_limit: 2
  workers:
    - id: writer
      agent: module-designer
      role: "Draft the API specification"
    - id: reviewer
      agent: qa-engineer
      role: "Score the specification against quality dimensions"
    - id: optimizer
      agent: module-designer
      role: "Rewrite low-scoring sections based on review feedback"
```

### Quality Dimensions

```yaml
quality_dimensions:
  - name: correctness
    weight: 0.4
    description: "API endpoints match requirements; request/response schemas are valid"
  - name: completeness
    weight: 0.3
    description: "All required endpoints, error codes, and edge cases are documented"
  - name: clarity
    weight: 0.2
    description: "Descriptions are unambiguous; examples are provided"
  - name: consistency
    weight: 0.1
    description: "Naming conventions, response formats, and patterns are uniform"
```

### Input

- Feature requirements: "Design REST API for user management (CRUD + search + bulk operations)"

## Expected Behavior

### Iteration 1: Initial Draft
1. **Writer** produces first draft of the API spec.
2. **Reviewer** scores: correctness=0.6, completeness=0.5, clarity=0.7, consistency=0.8.
3. **Supervisor** calculates weighted score: 0.6×0.4 + 0.5×0.3 + 0.7×0.2 + 0.8×0.1 = 0.61.
4. Score 0.61 < threshold 0.85 → **continue**.

### Iteration 2: First Improvement
1. **Optimizer** reads review feedback, rewrites low-scoring sections (completeness, correctness).
2. **Reviewer** re-scores: correctness=0.8, completeness=0.75, clarity=0.8, consistency=0.85.
3. **Supervisor** calculates: 0.8×0.4 + 0.75×0.3 + 0.8×0.2 + 0.85×0.1 = 0.79.
4. Score 0.79 < threshold 0.85 → **continue**. Score increased (no regression).

### Iteration 3: Final Refinement
1. **Optimizer** addresses remaining gaps (completeness edge cases, correctness validation).
2. **Reviewer** re-scores: correctness=0.9, completeness=0.9, clarity=0.85, consistency=0.9.
3. **Supervisor** calculates: 0.9×0.4 + 0.9×0.3 + 0.85×0.2 + 0.9×0.1 = 0.89.
4. Score 0.89 ≥ threshold 0.85 → **ACCEPT**.

## Verification Points

### V1: Convergence Detection
- [ ] Loop terminates when weighted score ≥ threshold
- [ ] Loop terminates at max_iterations if threshold never reached
- [ ] Loop aborts early if regression_limit consecutive score drops detected
- [ ] Correct termination reason is reported ("threshold_met" / "max_iterations" / "regression_abort")

### V2: Iteration History
- [ ] Each iteration records: iteration number, per-dimension scores, weighted score, decision
- [ ] History is written to `.specify/handoff/iteration-history.md`
- [ ] Score progression is monotonically increasing (in successful scenarios)
- [ ] Regression counter resets when score improves

### V3: Role Execution Correctness
- [ ] Writer only executes in iteration 1 (initial draft)
- [ ] Reviewer executes every iteration (scoring)
- [ ] Optimizer executes in iterations 2+ (never iteration 1)
- [ ] Supervisor makes accept/reject decision after each review

### V4: Final Report Accuracy
- [ ] Final report includes: accepted artifact path, final scores, iteration count
- [ ] Report lists improvement delta (final score - initial score)
- [ ] Report includes total token/cost estimate for the full loop
- [ ] Accepted artifact matches the last Optimizer output (not an earlier version)

### V5: Edge Cases

#### Regression Scenario
- [ ] If iteration 2 score drops below iteration 1: regression_counter = 1
- [ ] If iteration 3 score drops again: regression_counter = 2 → abort
- [ ] Abort report identifies the highest-scoring iteration's artifact as "best attempt"

#### Single-Iteration Pass
- [ ] If writer's initial draft scores ≥ threshold: loop exits after iteration 1
- [ ] No optimizer is invoked; report correctly states "passed on first attempt"

## Success Criteria

- Iteration converges within max_iterations
- Quality scores improve monotonically across iterations (in happy path)
- Final artifact meets or exceeds all quality dimension expectations
- Iteration history provides full audit trail for review
- Cost remains proportional to iteration count (no redundant work)
