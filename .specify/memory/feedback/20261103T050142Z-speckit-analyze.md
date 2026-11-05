---
id: "20261103T050142Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261103T043000Z-081b"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
disposition: "processed"
partial: false
created: "2026-11-03T05:01:42Z"
summary: "081b analyze over the US2 artifact set: 18 checklist FAILs dispositioned (7 P1 confirmed HIGH, CHK020 downgraded to MEDIUM by its validator), 5 new findings raised (signed-contract contract-path oblig"
introspection_ref: "introspection-20261105T080109Z#F-05"
disposition_reason: "introspection:introspection-20261105T080109Z#F-05"
---

## Review
081b analyze over the US2 artifact set: 18 checklist FAILs dispositioned (7 P1 confirmed HIGH, CHK020 downgraded to MEDIUM by its validator), 5 new findings raised (signed-contract contract-path obligation has no column/carrier; duty 2 judged by whole-file substring; 7 of 12 rows cite no FR; expression-gates G-req-clarity operator row stale; coverage lane delta not reproducible), 9 external read-only validators dispatched (8 confirm / 1 downgrade / 0 reject), coverage accountant surfaced a carried-over fr-uncovered 25/25 with no owning slice

## Optimization Points
- analyze template: the fixed coverage step (account-clause-coverage) has no slot in the report skeleton the previous run used, so its verdict silently vanished twice; add it as a mandatory section. Checklist CHK numbering restarted at 001 for the new slice while the analyze finding IDs are feature-scoped — the rerun delta had to re-derive prior-ID collisions by hand; recommend slice-scoped finding-ID namespacing or a documented continuation rule.
