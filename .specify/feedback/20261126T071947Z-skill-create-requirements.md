---
id: "20261126T071947Z-skill-create-requirements"
unit_id: "skill:create-requirements"
unit_type: "skill"
run_id: "r20261126T071500Z-fb"
scope: "local"
probe: "skill-create-requirements-wrapup"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-11-26T07:19:47Z"
summary: "Containment claims were authored undecidable and analyze paid for it five times: FR-025/SC-008's allowed-delta and ruling-authorization reading survived four repair rounds and a full mid-analyze plan "
introspection_ref: "introspection-20261127T162331Z#F-11"
disposition_reason: "introspection:introspection-20261127T162331Z#F-11"
---

## Review
Containment claims were authored undecidable and analyze paid for it five times: FR-025/SC-008's allowed-delta and ruling-authorization reading survived four repair rounds and a full mid-analyze plan re-review, only closing at R4-01/R5 (line 107, review F4; spine "Update — analyze rounds 3–4" and "ANALYZE GATE — PASS"). The closed-set-claims discipline exists in shared/guidelines/closed-set-claims.md, but nothing at requirements-authoring time forces its five elements, so undecidability surfaces in analyze rounds 3–4 instead of where the sentence is written; every spec that asserts "unchanged" pays the same toll.

## Optimization Points
- 1. Add a decidability pre-check to requirements authoring/validation requiring the five containment elements — baseline reference, comparison unit, allowed-delta set, complement assertion, ruling location — for every claim that a surface stays unchanged.
- 2. Route the same check through clarify so a claim missing an element is resolved before plan and tasks, instead of at analyze round 3–4.
- 3. Add a reverse sample (a deliberately undecidable containment claim) to the validator's red tests so the pre-check is shown to fail when its subject breaks.
