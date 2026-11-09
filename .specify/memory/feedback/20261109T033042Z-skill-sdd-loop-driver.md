---
id: "20261109T033042Z-skill-sdd-loop-driver"
unit_id: "skill:sdd-loop-driver"
unit_type: "skill"
run_id: "r20261109T023000Z-auto-closeout-analyze2b"
scope: "local"
probe: "skill-sdd-loop-driver-cli-profile"
kind: "internal"
slice: "skills"
feature: "091-auto-git-closeout"
feature_id: "091"
partial: false
created: "2026-11-09T03:30:42Z"
summary: "Analyze round 2 over the repaired 091-auto-git-closeout spec set at 35248f14. All 20 round-1 findings verified"
---

## Review
Analyze round 2 over the repaired 091-auto-git-closeout spec set at 35248f14. All 20 round-1 findings verified
resolved, most mechanically: the coverage claim was reproduced twice (shipped accountant plus an ad-hoc parser that
re-implements the citation-group rule) and agreed at FR claimed 28 / uncovered 0 with 32 clauses claimed exactly once
in the green partition; the four formerly-orphaned FRs were additionally checked at subject level, not just citation
level, because that was the failure mode C-01 named. Five required gates re-read green with 0 errors. Ten new
residuals are dispositioned (0 CRITICAL, 0 HIGH, 5 MEDIUM, 5 LOW), none blocking implement; the two MEDIUM ones that
touch deliverable text are handed to implement as named preconditions. Weakest points: tasks.md's premise table is
stale in five cells and contradicts its own FR-lane note, the settle-on-misclassification produced an errant
determination record that the engine will not let me correct, and the checklist file's 15 fail marks remain as
round-1 state because this stage is read-only by instruction.

## Optimization Points
- account-clause-coverage.py: the `baseline-missing` state has no action for a caller who has legitimately not frozen a baseline yet — every pre-implement stage reports 599 errors and a `fail` on the delta lane while the FR lane is green. A verdict tier between "missing" and "green" (e.g. `unfrozen`, with only the FR lane judged) would let an analyze stage report honestly instead of disclaiming the gate.
- tasks.md "Premises measured at generation time" is a hand-maintained measurement table with no drift guard; a repair round can invalidate it silently and it is the section implement reads first. A re-derivation helper, or a stamp that records WHICH commit the numbers were measured at, would make staleness visible.
- run-determination.py `--action settle` accepts any `--user-turn-class` for a run with no user turn at all; a subagent slice has no user turn and declaring `continuation_negative` produces a `rejected` verdict that is factually about nothing. The engine should admit a `no_user_turn` class for subagent runs, or refuse to settle one.
- run-determination.py write-once settlement means a misdeclared class cannot be corrected, and the errant record stays in the run history forever. A `--action correct` (append a superseding record naming the prior one) would let honesty win over immutability.
- exec-quant score `--provenance` is recorded as `user-given` even when a subagent self-assesses; the label overstates the source and a later aggregate cannot distinguish self-scores from user scores.
- validate-tasks.py `green-cross-phase` has no disclosed-exception channel, so a spec whose page order cannot ascend with row order must carry a permanent non-zero warning count; a DoD cannot then assert "zero warnings", only "exactly N with reasons". A structured exception list would make the count assertable at zero.
- pre-analyze-check.py reads a code span in a format legend as a real `[blockedBy:]` token; documentation of the tag syntax is indistinguishable from a use of it.
