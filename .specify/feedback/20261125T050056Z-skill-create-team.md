---
id: "20261125T050056Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "r20261125T022857Z-06dd"
scope: "local"
probe: "skill-create-team-wrapup"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-11-25T05:00:56Z"
summary: "Team definition persisted and validated: reporter seat present, run-checks ok, handoff binding active; territory expanded before implement to grant notes and the two migration sources while keeping de"
introspection_ref: "introspection-20261127T162331Z#F-04"
disposition_reason: "introspection:introspection-20261127T162331Z#F-04"
---

## Review
Team definition persisted and validated: reporter seat present, run-checks ok, handoff binding active; territory expanded before implement to grant notes and the two migration sources while keeping design-face files forbidden.

## Optimization Points
- Implement dispatch prep must diff every task's write paths against the crew territory before the first executor dispatch; a missing evidence sink silently blocks TDD evidence. After a territory expansion, re-run territory-check on both a granted and a forbidden path, not only run-checks.
