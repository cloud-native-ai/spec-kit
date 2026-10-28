---
id: "20261024T151452Z-speckit-review"
unit_id: "/speckit.review"
unit_type: "command"
run_id: "069a-review-20261024T1515Z"
scope: "local"
probe: "speckit-review-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-10-24T15:14:52Z"
summary: "069a slice review: the two shipped gate entry points fail when executed as written (W1/W3 verifier exits 2; client-shape class lookup exits 2 owner-unavailable); SC-002 pass and checklist 40/40 overst"
---

## Review
069a slice review: the two shipped gate entry points fail when executed as written (W1/W3 verifier exits 2; client-shape class lookup exits 2 owner-unavailable); SC-002 pass and checklist 40/40 overstate the evidence; slice strengthened 8+ FRs while claiming the parent was carried verbatim.

## Optimization Points
- REC-069a-01..14: (1) never mark a runtime-denominator SC pass on static text; (2) out-of-slice checklist items stay [ ] and the closure count is derived; (3) wired commands must carry scope + --strict and be executed by a contract test, not grepped; (4) two-hats root/payload resolution for engines living under .specify/; (5) lookup must degrade on an invalid class instead of returning it; (6) slice projection needs a 'slice-strengthened' value and a parent sync; (7) freeze measurement instruments before the run; (8) Feature status must not be advanced by one slice; (9) author-adjudicated checklists need one independent pass; (10) shipped gate faces must have a passing state in the distribution target.
