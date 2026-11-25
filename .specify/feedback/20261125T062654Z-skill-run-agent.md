---
id: "20261125T062654Z-skill-run-agent"
unit_id: "skill:run-agent"
unit_type: "skill"
run_id: "r20261125T022857Z-06dd-eff4"
scope: "local"
probe: "skill-run-agent-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-25T06:26:54Z"
summary: "Two dispatcher paths coexist: unattended SDD dispatches through the driver's stage-runner fork carrier, while 061 per-dispatch quantification, 070 package coordination and 088 reporter/measure wiring "
---

## Review
Two dispatcher paths coexist: unattended SDD dispatches through the driver's stage-runner fork carrier, while 061 per-dispatch quantification, 070 package coordination and 088 reporter/measure wiring live on the run-agent / team-run path. Evidence: zero agent: exec-quant records, reporter seat never dispatched, /speckit.measure used once. Efficiency features are merged but inert in the main path.

## Optimization Points
- 1. Choose one dispatch path or port the reporter/measure/per-dispatch-quant wiring into the driver path (or move the driver onto run-agent), and state the boundary in subagent-definitions. 2. Add a contract test proving the chosen path emits the 061 agent record and a run report line, so the wiring cannot silently regress. Routing verdict: sdd (nature=feature, traceability=required, blast=cross-cutting, reversibility=hard, complexity=high-stakes; reason sdd-capability-or-contract-change).
