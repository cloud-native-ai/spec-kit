---
id: "20261105T094516Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261105T074027Z-084a-r2"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "084-harness-triple-structure"
feature_id: "084"
partial: false
created: "2026-11-05T09:45:16Z"
summary: "Analyze round 2 re-adjudicated all 17 round-1 findings and found two HIGH defects the first round did not: a regression introduced by the remediation commit itself (a features-file line trips an exist"
---

## Review
Analyze round 2 re-adjudicated all 17 round-1 findings and found two HIGH defects the first round did not: a regression introduced by the remediation commit itself (a features-file line trips an existing contract guard) and a scope-criterion conflict between FR-006 (i) and eight 'none'-engine-side roster rows. Both were confirmed by independent validators; the gate is not green and the loop budget is spent.

## Optimization Points
- Mechanical-first detection paid off: one pytest invocation, one grep over .specify/memory/, one git log -S and one table parse produced both new HIGH findings, while the 17-row residue list still needed full reading. Two process lessons: (a) when a finding has two causes, the repair list must name both sites - round 1 named the contracts and the missing [green:] claim, the repair fixed only the contracts and left the tasks banner asserting the stale premise; (b) the analyze dispatch brief attributed '0 of 19 FRs' to the optional tag, but that lane derives from contract citation groups, so the brief's stated cause was incomplete and had to be re-derived from the accountant's implementation. Suggest the driver run tests/contract/test_expression_compatibility.py in the targeted set of any stage that writes to .specify/memory/, since registry edits can break the flow-class guard and no gate in the spec chain looks at it.
