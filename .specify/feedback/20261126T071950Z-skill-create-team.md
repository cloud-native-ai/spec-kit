---
id: "20261126T071950Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "r20261126T071500Z-fb"
scope: "local"
probe: "skill-create-team-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-26T07:19:50Z"
summary: "Team-view output degrades on real team workspaces, and the fix belongs where teams are created: the line-107 queued-next-line record (spine decision-governance.md:204) names team-view-degradation — un"
---

## Review
Team-view output degrades on real team workspaces, and the fix belongs where teams are created: the line-107 queued-next-line record (spine decision-governance.md:204) names team-view-degradation — unrecognized 4-hex report names, missing items.jsonl/STATE.md/run-log.jsonl, and binding/goal normalization — and is the subject of the separate line 108. A read-only survey of .specify/teams in this repository shows the same shape: many team directories hold only team.md, and run reports follow several timestamp grammars (for example 20260730T082021Z-report.md and 2026-08-07T15-00-00Z-report.md). The create-team run-workspace contract and report-naming rule do not pin what a team writes, so readers must guess and degrade.

## Optimization Points
- 1. Pin one run-report filename grammar in the create-team run-workspace contract, validate it at write time, and give readers one documented legacy-tolerance list instead of guesswork.
- 2. Declare per collaboration pattern which workspace files every run writes (items.jsonl/STATE.md/run-log.jsonl) and write explicit empty placeholders so readers can distinguish missing from empty.
- 3. Add fixture teams with a legacy 4-hex report name and with missing workspace files to the create-team and view-team tests, so degradation is measured before line 108 lands.
