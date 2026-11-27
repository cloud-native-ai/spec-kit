---
id: "20261126T071950Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "r20261126T071500Z-fb-3"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-11-26T07:19:50Z"
summary: "The checkpoint protocol's workspace-signature obligation was not met at review time: the 107 review took only a post-run snapshot, whose self-check is trivially clean, and its evidence file records ve"
introspection_ref: "introspection-20261127T162331Z#F-08"
disposition_reason: "introspection:introspection-20261127T162331Z#F-08"
---

## Review
The checkpoint protocol's workspace-signature obligation was not met at review time: the 107 review took only a post-run snapshot, whose self-check is trivially clean, and its evidence file records verbatim "DISCLOSED OMISSION: no pre-run signature was captured at stage start, so the before/after comparison the checkpoint protocol requires is not available for this stage" (test-evidence/review-evidence.txt:70-76; the requirement is owned by sdd-loop-driver/references/checkpoint-protocol.md:159). Without the before signature the review cannot prove its probes and agents stayed inside the measured repository, and the mitigation had to rest on prose; the adjacent 106 F4 finding (an all-null after-snapshot accepted as a snapshot) shows the same guard surface already failing on the writer side.

## Optimization Points
- 1. Make the pre-stage snapshot a named precondition of stage dispatch/checkpoint: take it in stage-runner before the first model call, or refuse to start the stage without it.
- 2. Make workspace-guard --check reject a self-referential comparison (a single snapshot checked against itself) as an input error instead of returning a trivially clean result.
- 3. Record both snapshot paths in the stage record so an omission is visible mechanically at checkpoint time, not only when a reviewer reads the evidence file.
