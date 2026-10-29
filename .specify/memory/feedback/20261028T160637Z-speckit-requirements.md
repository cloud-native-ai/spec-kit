---
id: "20261028T160637Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "r20261028T132000Z-074d"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "074a-authorized-routing"
feature_id: "074"
partial: true
created: "2026-10-28T16:06:37Z"
summary: "**Partial run** — slice 074a requirements: the artifact-authoring dispatch ended at its 40-turn limit with requirements.md (475 lines, 20 FR + 6 SC, 10 shared strings) and checklists/requirements.md o"
---

## Review
**Partial run** — slice 074a requirements: the artifact-authoring dispatch ended at its 40-turn limit with requirements.md (475 lines, 20 FR + 6 SC, 10 shared strings) and checklists/requirements.md on disk; this close-out dispatch re-ran both gates (validate-requirements.py status ok, 0 error / 0 warning; decomposition-check --mode plan proceed, 20 <= 30), checked the checklist's 19 items against the slice artifact programmatically (3 user stories, 11 Given scenarios, 13 edge cases, 9 key entities, 11 assumptions A1-A7/A9-A12, parent mapping 20 FR + 6 SC + 10 STR rows, 0 open markers), and committed the stage artifacts. Close-out changed no requirement text, id, or parent mapping. Accounting for this (unit, run): the determination and exec-quant records predate this dispatch and both engines return duplicate, so both stand as recorded with qualification=partial; the feedback entry is written here because it was the missing third piece.

## Optimization Points
- Add a slice-to-parent mapping proposition to validate-requirements.py: the checker passes a slice whose `## Parent Mapping` table silently drops a row, so the requirement that every local FR/SC/STR maps to exactly one parent id is currently a hand assertion (the 074a checklist had to state 20 + 6 + 10 rows by hand and compare them against the parent spec by grep). A `--parent <parent-requirements.md>` flag that set-compares the mapping tables against the parent's definition rows would turn that into a machine verdict and catch a dropped projection row at the gate rather than at plan.
- Align run-determination.py's --red-source closed value set with the owner doc: .specify/shared/workflow/feedback-step.md § "Unresolved-red input — engine exit codes only" declares `surfaced_anomaly_unanswered` dropped and MUST NOT be declared, yet the CLI still offers it as a value and a prior /speckit.requirements run for 074a persisted it (session record 20261028T160359Z-run-determination-speckit-requirements-...md). Either remove the value from the CLI domain or re-document it as live; today the doc and the code disagree about what may be declared.
- token-efficiency — this close-out dispatch read the whole persisted run-determination record body (roughly 200 lines of JSON) merely to check its qualification field, when the engine's own `--action history` returns a projection. Reading the projection first and opening the body only when a field must be amended would avoid a raw machine-data dump (summary-first), with no loss of evidence.
