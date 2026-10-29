---
id: "20261029T050729Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261029T045000Z-b074"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "074b-nested-governance"
feature_id: "074"
partial: false
created: "2026-10-29T05:07:29Z"
summary: "analyze on slice 074b: read-only pass over requirements/plan/contracts/data-model/tasks/checklists; 14 findings (2 HIGH, 7 MEDIUM, 5 LOW) with 13 checklist items adjudicated (11 real, 2 covered-by); n"
---

## Review
analyze on slice 074b: read-only pass over requirements/plan/contracts/data-model/tasks/checklists; 14 findings (2 HIGH, 7 MEDIUM, 5 LOW) with 13 checklist items adjudicated (11 real, 2 covered-by); no artifact modified, no commit; gate evidence collected (pre-analyze decision=fail errors=1; coverage claimed 30 / FR 8-8 / beyond-baseline 0 / status ok; 266-case containment carrier re-run all green).

## Optimization Points
- Analyze ran the seven detection passes plus the checklist-accountability pass; the fixed coverage accountant (claimed 30 / FR 8/8 / 0 beyond baseline) made the clause-coverage part of the verdict mechanical rather than a reading exercise.
- The containment-baseline carrier (7 named sets / 17 files / 266 case ids, per-set '# files:' lines) was sufficient to decide the suite-membership question without re-collecting: a carrier that states its own membership file list is what made that adjudication cheap.
- Prerequisite friction: check-prerequisites.sh resolved REQUIREMENTS_DIR to the parent feature directory (074) even though the branch is 074b-nested-governance, so the unit's declared input contract cannot reach a slice's artifacts; the slice paths had to be supplied out of band.
- Validation-wave friction: the skill's subagent-unavailable fallback is phrased as 'dispatch fails twice in a row (upstream error)', but an executor dispatch can expose no dispatch capability at all; the direct-re-read marker had to be applied without a failed attempt to point at.
- Pre-analyze-check scans checklists/ as well as spec artifacts, so a cross-slice id written unqualified in a checklist turns a stage gate red at HEAD; the checklist writer has to qualify such ids (the sibling stage did this for some ids but not all).
