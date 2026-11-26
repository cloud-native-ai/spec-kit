---
id: "20261126T125545Z-skill-implement-feature"
unit_id: "skill:implement-feature"
unit_type: "skill"
run_id: "r20261126T071500Z-108a"
scope: "local"
probe: "skill-implement-feature-wrapup"
kind: "internal"
slice: "skills"
feature: "108-team-view-degradation"
feature_id: "108"
partial: false
created: "2026-11-26T12:55:45Z"
summary: "Implement stage of 108-team-view-degradation: four verified packages (T001–T029, 29/29 covered by one passing effective verdict per row; P1's a1 fail was superseded by a2 after the spine E2 row's miss"
---

## Review
Implement stage of 108-team-view-degradation: four verified packages (T001–T029, 29/29 covered by one passing effective verdict per row; P1's a1 fail was superseded by a2 after the spine E2 row's missing trigger field was repaired) integrated in order P1→P4; the task table was closed by the integrator (29 rows [X], text untouched, validate-tasks PASS 0 errors / 0 warnings) and the closing commit carried the closed table, the integration record and six driver-audit stage-evidence JSONL files without touching the eleven part commits. Measured axes (run determination r20261126T071500Z-108a): token not_evaluated (no session source), elapsed regressed (11,234,000 ms vs the same unit's latest settled run at 6,268,542 ms; whole-stage span, caller-declared on both sides), artifact_correctness ok (4 declared green checks all covered by red-first evidence; zero added failed names over the recorded targeted set), satisfaction pending the next user turn; trigger bit false.

Friction observed: (a) the worktree had no .specify/state/wp/ at all; the five package verdicts lived only in the main repo's .specify/state/wp/ (the 107 run hit the same split and asked for an explicit state root; the dispatch still cites the worktree-relative path); (b) two part-era evidence notes carried narrative count slips (targeted-set wrote "72 new" nodes where its own enumeration and a collect-only reading give 43; notes/us2-green split 17 as "7+10" where the file holds 6+11) that no program check had validated, costing a reconciliation detour at integration; (c) the handoff's one-record-per-task writeback duty was met for T001–T018 but unmet for T019–T029, discovered only at integration.

## Optimization Points
- 1. token-efficiency — the integrator read all five package verdict JSONs in full (~57 KB; checks[].evidence bodies dominate) to answer coverage and the a1→a2 supersession question; a program-side digest projection (package, task ids, result, verdict, verified_at) would answer 29/29 and reach the full bodies only on a contradiction (recurrence of the 107 entry's point 1).
- 2. Package-verdict and stage-state location: for worktree runs the runtime store (.specify/state/wp/, the spine, runner evidence) lives in the main repo while the dispatch cites a worktree-relative path; naming the state root explicitly, or projecting the verdicts into the worktree store, would remove a filesystem-wide search (recurrence of the 107 entry's point 2, still unfixed).
- 3. Narrative counts in evidence notes have no machine check: targeted-set.txt's "72 new" vs the measured 43, and notes/us2-green.txt's "7+10" vs the file's 6+11 — a one-line program derivation (collect-only node count, task-id coverage) at the authoring step would pin the numbers the notes assert.
- 4. Handoff § Writeback completeness is unverified at package close: 18 of 29 records existed at integration time; a per-task-id presence check in the package close (or in stage U4) would surface the gap at the seat that owns the write.
