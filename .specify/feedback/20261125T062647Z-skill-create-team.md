---
id: "20261125T062647Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "r20261125T022857Z-06dd-eff2"
scope: "local"
probe: "skill-create-team-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-25T06:26:47Z"
summary: "093 effective-concurrency reading never settles in practice: every per-dispatch triple is requested=1, effective=not_evaluated, effective_reason=single-unit, while the run declared requested 24 / effe"
---

## Review
093 effective-concurrency reading never settles in practice: every per-dispatch triple is requested=1, effective=not_evaluated, effective_reason=single-unit, while the run declared requested 24 / effective 5 at U0. The real serialization cause is the bound team's max_parallel=1 (serial pattern), which the closed reason vocabulary cannot express, so 'single-unit' masks an avoidable serialization opportunity.

## Optimization Points
- 1. Give the serial-reason vocabulary a closed representation for a team-pattern/max_parallel constraint (or make the team pattern an input to the reading) instead of reusing single-unit. 2. Compute effective by interval overlap at dispatch settle and make an unsettled effective a visible warning in status and /speckit.measure. Routing verdict: sdd (nature=feature, traceability=required, blast=cross-cutting, reversibility=reversible, complexity=complex; reason sdd-capability-or-contract-change).
