---
id: "20261105T085423Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261105T074027Z-084a"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "084-harness-triple-structure"
feature_id: "084"
disposition: "processed"
partial: false
created: "2026-11-05T08:54:23Z"
summary: "Round-1 analyze of feature 084: 17 findings (1 CRITICAL / 2 HIGH / 10 MEDIUM / 4 LOW), all adjudicated; CRITICAL/HIGH confirmed by an external read-only validator wave (3 confirm, 1 downgrade, 0 rejec"
introspection_ref: "introspection-20261106T084116Z#F-01"
disposition_reason: "introspection:introspection-20261106T084116Z#F-01"
---

## Review
Round-1 analyze of feature 084: 17 findings (1 CRITICAL / 2 HIGH / 10 MEDIUM / 4 LOW), all adjudicated; CRITICAL/HIGH confirmed by an external read-only validator wave (3 confirm, 1 downgrade, 0 reject).

## Optimization Points
- Analyze stage friction: (1) the fixed clause/FR coverage step cannot run for this feature because the five contracts use DS/HC/SR/MB/DM prefixes while the syntax owner requires the C-NNN form, and coverage-baseline.txt was never frozen at the tasks stage -> status baseline-missing; (2) the reused duplicate face has no per-fact selector, so FR-007(b)/SC-002's 'zero hits for that fact' reading depends on the invocation shape; (3) research.md R7/R10 records '39 test files for the five gate scripts' with the script names elided and no five-name union reproduces 39 (measured 38 / 35 / 39-for-six); (4) the analyze skill's checklist pass H wants an unchecked [Gap] residue of zero, which required a per-item disposition table -- useful, but the 10-item manual mapping is expensive for a 38-item checklist.
