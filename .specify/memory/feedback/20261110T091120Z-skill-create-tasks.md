---
id: "20261110T091120Z-skill-create-tasks"
unit_id: "skill:create-tasks"
unit_type: "skill"
run_id: "r20261110T081104Z-b096"
scope: "local"
probe: "skill-create-tasks-wrapup"
kind: "internal"
slice: "skills"
feature: "096-sdd-observer-agent"
feature_id: "096"
partial: false
created: "2026-11-10T09:11:20Z"
summary: "Produced a 47-row, dependency-ordered tasks.md from the 096 design artifacts: format owner fact and fixture builder as Foundational; US1 engine core; US2 objectivity checker; US3 driver lifecycle; US4"
---

## Review
Produced a 47-row, dependency-ordered tasks.md from the 096 design artifacts: format owner fact and fixture builder as Foundational; US1 engine core; US2 objectivity checker; US3 driver lifecycle; US4/US5 boundary and cardinality; Polish mirrors/evidence. Both structural gates are green (validate-tasks 0 error/0 warning; pre-analyze tasks-stage decision pass, 0 errors, 77 expected missing-path advisories). The main frictions were the clause-order/phase-order constraint in green attribution and the repeated re-derivation of the fixed evidence landing points.

## Optimization Points
- token-efficiency: this run read the full requirements.md and plan.md bodies (~75 KB) into context to derive the 47-row partition; a digest-first projection (FR/SC inventories, clause headings, the plan's Work Packages table) would have cut context spend without losing a fact — the plan already carries the package partition, so the full body re-read was avoidable.
- The green-clause attribution rule (ascending clause ordinals against row order) forced a hand-computed subset and three fully covered clauses to stay unclaimed; create-tasks could state the safe partition rule (claim in ascending clause blocks, skip the cross-phase remainder) next to the [green:] tag definition so every run does not re-derive it.
- The tasks template could pre-name the five runtime-evidence landing points (notes/red-first-evidence.md, notes/quickstart-run.md, notes/pre-change-measurements.md, coverage-baseline.txt) directly in the Setup phase skeleton, so Setup rows are copied instead of re-derived from the skill's landing-point list.
