---
id: "20261116T101155Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "analyze-r3-w1-20261116"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
disposition: "processed"
partial: false
created: "2026-11-16T10:11:55Z"
summary: "Analyze round 3 (incremental re-check), domain W1 requirements: 14 findings reported (1 HIGH / 9 MEDIUM / 4 LOW); no artifact modified."
introspection_ref: "introspection-20261116T141525Z#F-05"
disposition_reason: "introspection:introspection-20261116T141525Z#F-05"
---

## Review
Analyze round 3 (incremental re-check), domain W1 requirements: 14 findings reported (1 HIGH / 9 MEDIUM / 4 LOW); no artifact modified.

## Optimization Points
- scanner repo-root referent undefined (CHK038 open); reason has no registry field carrier; status.md 'Single source' anchor absent; COMPLIANT_INVOCATIONS unowned; SC-002 red-leg injection lacks isolation; scan-root set duplicated 4x; digest invariant duplicated 8x; FR-021 exec-record evidence uncovered; FR-009 event count uncovered; FR-017 points to superseded A-7; checklist dispositions are prose-only; criterion literal-match vs caller-only contradiction; delta owner mismatch; RS-002 pin contradiction.
