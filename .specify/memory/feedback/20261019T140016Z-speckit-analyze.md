---
id: "20261019T140016Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "T135958Z-analyze"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
disposition: "ignored"
partial: false
created: "2026-10-19T14:00:16Z"
summary: "063 analyze completed read-only: CRITICAL=0/HIGH=0, 5 MEDIUM + 3 LOW findings (top: tasks.md [P] count 25 vs actual 24 with T002 listed parallel but marked non-parallel; SC-001 comparison-object ambig"
disposition_reason: "introspection-20261021T133447Z: excluded (no actionable framework finding)"
---

## Review
063 analyze completed read-only: CRITICAL=0/HIGH=0, 5 MEDIUM + 3 LOW findings (top: tasks.md [P] count 25 vs actual 24 with T002 listed parallel but marked non-parallel; SC-001 comparison-object ambiguity resolved one layer down by C-2; FR-017 run-evidence carrier undefined; FR-022 glob roots narrower than C-29; waiver storage location unpinned), coverage 30/30 FR + 34/34 clauses, linkage 100%, no project files modified, no commits.

## Optimization Points
- Measured-premises hand-maintained literals drift ([P] 25 vs 24) — mechanical derivation candidates at implement. F4 reproduced live at this run's wrap-up: run-determination required explicit --run-id/--complexity, confirming the compiled-face placeholder gap C-20..C-23 targets. No significant optimization beyond recording the drift pattern.
