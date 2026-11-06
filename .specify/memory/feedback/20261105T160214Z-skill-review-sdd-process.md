---
id: "20261105T160214Z-skill-review-sdd-process"
unit_id: "skill:review-sdd-process"
unit_type: "skill"
run_id: "r20261105T074027Z-084a"
scope: "local"
probe: "skill-review-sdd-process-wrapup"
kind: "internal"
slice: "skills"
feature: "084-harness-triple-structure"
feature_id: "084"
partial: false
created: "2026-11-05T16:02:14Z"
summary: "Process segment of feature 084's review: the SDD chain, its gates and its two halts (task/plan turn budgets, analyze U5) were sound; the failures are in how a machine fact was recorded and then believ"
---

## Review
Process segment of feature 084's review: the SDD chain, its gates and its two halts (task/plan turn budgets, analyze U5) were sound; the failures are in how a machine fact was recorded and then believed.

## Optimization Points
- 1) A closed set frozen in an older contract test (081's finding-name subset assertion) forbids the driver gate from adopting the new delegation by default, so the improvement ships behind an off-by-default flag nobody passes. 2) Same-author detection could not be delegated (no subagent dispatch in this topology) so every P0 rests on a direct re-read; the fallback is invisible unless the skill is read — it should be a report field. 3) Two closed task rows name evidence carriers that do not exist on disk (T031 -> notes/quickstart-run.md, GATE-2 -> test-evidence/head-failed.txt), so a row state cannot be distinguished from an assertion. 4) The code-review skill's help text says the non-interactive path has four steps while the skill says five (capture was added); pre-existing, same defect class the feature removes.
