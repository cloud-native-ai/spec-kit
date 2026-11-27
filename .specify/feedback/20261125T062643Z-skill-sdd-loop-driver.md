---
id: "20261125T062643Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "r20261125T022857Z-06dd-eff1"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-11-25T06:26:43Z"
summary: "061 per-dispatch quantification is not wired into the driver's stage-runner dispatch path: the store holds 439 schema-v2 exec-quant records and zero 'agent:' records. The stage-level key (unit, run_id"
introspection_ref: "introspection-20261127T162331Z#F-06"
disposition_reason: "introspection:introspection-20261127T162331Z#F-06"
---

## Review
061 per-dispatch quantification is not wired into the driver's stage-runner dispatch path: the store holds 439 schema-v2 exec-quant records and zero 'agent:' records. The stage-level key (unit, run_id) also collapses multiple package dispatches into duplicate no-ops, so the largest cost in an unattended run (subagent packages) has no measured token/time row.

## Optimization Points
- 1. Have stage-runner (or its caller) invoke exec-quant collect-dispatch after each dispatch with unit_id agent:<seat> and run_id equal to the dispatch label, non-blocking and bounded. 2. Expose those per-dispatch rows to /speckit.measure so stage cost can be read without ad-hoc raw-stream parsing. Routing verdict: sdd (nature=feature, traceability=required, blast=cross-cutting, reversibility=reversible, complexity=complex; reason sdd-capability-or-contract-change).
