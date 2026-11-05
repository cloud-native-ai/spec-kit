---
id: "20261105T040452Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "r20261105T032102Z-c139-analyze"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-11-05T04:04:52Z"
summary: "analyze read-only: 7 CRITICAL/HIGH candidates validated (1 confirm of the already-MEDIUM-capped H-01, 4 downgrade, 2 reject); 7 CHK Gap items all raised or dispositioned; gates must be read after appl"
---

## Review
analyze read-only: 7 CRITICAL/HIGH candidates validated (1 confirm of the already-MEDIUM-capped H-01, 4 downgrade, 2 reject); 7 CHK Gap items all raised or dispositioned; gates must be read after apply-as-instructed

## Optimization Points
- T006 red-first premise is false as written (T051 would close on a fabricated pairing); C-26/T029 unsatisfiable against the installed entry point without an unstated reinstall; CHK009 (summary bound) missing from a VERIFIABLE FR; requirements silence on Documentation Map row (CHK001) required by T028 to be recorded in test-evidence; cross-artifact counts disagree (34 vs 33 vs 32 clauses, 8 vs 9 SC, 3 vs 4 STR, 4 vs 7 mutation legs); plan EP-002 marked verified without the failing measurement its own stage recorded
