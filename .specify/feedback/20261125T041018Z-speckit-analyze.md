---
id: "20261125T041018Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261125T022857Z-06dd"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "105-runtime-store-layout"
feature_id: "024"
disposition: "processed"
partial: false
created: "2026-11-25T04:10:18Z"
summary: "Read-only analyze of 105-runtime-store-layout completed over the full artifact set (requirements/plan/tasks/4 contracts/data-model/research/quickstart/feature-ref/40-item checklist/checkpoints/handoff"
introspection_ref: "introspection-20261127T162331Z#F-11"
disposition_reason: "introspection:introspection-20261127T162331Z#F-11"
---

## Review
Read-only analyze of 105-runtime-store-layout completed over the full artifact set (requirements/plan/tasks/4 contracts/data-model/research/quickstart/feature-ref/40-item checklist/checkpoints/handoff) with deterministic gates: validate-tasks 0 error/0 warning, validate-requirements 0/0, validate-decision-tensions 7 mechanical HIGH labels (exit 1), clause coverage claimed 8 / clause-uncovered 0 beyond the frozen baseline. Verdict: 0 CRITICAL / 6 HIGH. The tasks-stage addendum (BC01-BC18) broke the plan's Decision Tensions section anchor and left five expected_sacrifice fields unmapped to a declared SC measurement source; SC-007's literal rc-0 clause contradicts its measured no-new-drift criterion; SC-006/FR-004/A-8's allowlist enumeration disagrees with contract L-5's four-file allowlist; and the container-pass end state is undefined for paths claimed by a store item but left in place (non-content collisions, legacy non-store file). The analyze gate cannot proceed until these upstream repairs land. Full-artifact reads were required by the deep analysis brief; no deterministic work was done in-prose and no machine-managed store was dumped wholesale.

## Optimization Points
- Run validate-decision-tensions.py as part of the analyze fixed deterministic step and fail the analyze gate on its non-zero exit; this run's dtr-anchor / dtr-record-incomplete / expected-sacrifice-unmapped labels (7 mechanical HIGH) were invisible to the clause-coverage accountant.
- Mechanically diff every closed-set containment success criterion against its guard's declared allowlist or criterion (SC-006 vs L-5; SC-007 vs T-003) in the analyze report, so a requirements-to-guard mismatch cannot pass as prose.
