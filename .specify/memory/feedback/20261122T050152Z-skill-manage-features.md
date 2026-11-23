---
id: "20261122T050152Z-skill-manage-features"
unit_id: "skill:manage-features"
unit_type: "skill"
run_id: "feature-reconcile-20261122-audit"
scope: "local"
probe: "skill-manage-features-wrapup"
kind: "internal"
slice: "skills"
feature_id: "006"
partial: false
created: "2026-11-22T05:01:52Z"
summary: "Reconciled 100 registry rows: 64 existing rows changed, 35 tolerated, and Feature 103 added. Registry/state checks passed 33 and direct debt-governance guards passed 32; the combined run had 3 histori"
---

## Review
Reconciled 100 registry rows: 64 existing rows changed, 35 tolerated, and Feature 103 added. Registry/state checks passed 33 and direct debt-governance guards passed 32; the combined run had 3 historical baseline failures, while 078's 12 directed failures were recorded as Blocked. Axes without baselines remain not_evaluated and no full-suite claim was made.

## Optimization Points
- token-efficiency: full-registry runs should always split the first table cell and consume metadata projections; the early broad ID extraction produced a 30 KB result, and one audit worker repeated the same overly broad match before correcting it. A shared deterministic extractor would avoid that duplicated spend.
- Preserve separate evidence lanes for pre-existing baseline failures and feature-specific failures. The 078 audit correction was justified only after reading the canonical runner's raw 12-failure record and the source/mirror divergence, not from the registry's prior status prose.
