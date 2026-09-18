---
id: "20260918T065831Z-speckit-analyze"
unit_id: "/speckit.analyze"
unit_type: "command"
run_id: "051-user-facing-comprehension-analyze-rerun-20260918b"
scope: "local"
probe: "speckit-analyze-wrapup"
kind: "internal"
slice: "commands"
feature: "051-user-facing-comprehension"
partial: false
created: "2026-09-18T06:58:31Z"
summary: "Rerun after the first remediation batch. Same-author condition held, so detection was delegated to three fresh-context detectors on disjoint artifact-pair scopes and validation to 13 fresh-context val"
---

## Review
Rerun after the first remediation batch. Same-author condition held, so detection was delegated to three fresh-context detectors on disjoint artifact-pair scopes and validation to 13 fresh-context validators disjoint from the detectors — the first run of the newly codified §4 gate. It paid for itself immediately: 5 of the open findings were introduced or exposed by the previous remediation batch, including a one-character regex escape defect (B-01) typed into the very command that a prior fix had rewritten, and a CRITICAL Principle XIV breach (C-01) created by propagating a clause count as a corrected number rather than a reference. Self-review of my own remediation would not have surfaced either. Validation downgraded 9 of 13 CRITICAL/HIGH findings (69%), all on propagation facts the detectors had not checked, which is itself the actionable signal. Prior-run delta was produced by content matching after recovering the earlier table from the session transcript.

## Optimization Points
- **Tighten rule 3 in the detector briefs, or pre-compute the propagation surface.** 9 of 13 CRITICAL/HIGH findings were downgraded, and every downgrade turned on a propagation fact the detector had not checked — "the defect sits in unimplemented planning prose", "a redundant backstop already guards it", "the copy is a permitted dated record". The briefs did state the rule, but two of three detectors applied it as a formality rather than a gate. Concrete fix: require each detector to emit a `propagation_surface` column with a *named consumer artifact* (a task ID, a clause, a test file) or the literal string `none`, and have the orchestrator refuse any CRITICAL/HIGH row whose column reads `none` before dispatching validation. That converts the cap from advice into an intake filter and would have suppressed most of the 9 before they cost a validator dispatch.
- **Give detectors the legitimate-duplicate test explicitly.** Two downgrades (C-01's four dated `60` copies, C-04's dated `features/040.md` record) rested on the detector treating a permitted dated record as a live copy. `one-source-of-truth.md`'s three legitimate-duplicate conditions are the decisive test for a large share of count-drift and stale-copy findings in this repo, yet neither brief named them. Adding "before reporting a stale copy, apply the three legitimate-duplicate conditions and quote which one fails" would have narrowed both findings at detection time.
- **Make the rerun delta recoverable at authoring time, not by grepping the transcript.** §6 requires an ID-level delta against the prior report, but the prior run's IDs used category initials (G-1, I-05, T-2) while this run's used scope letters (A-01, B-05, C-04) per the owner doc's disjoint-scope split — so ID matching was impossible and I had to recover the prior table by regex over a 5.9 MB transcript. Two options: pin the ID scheme in the command (category initials always, with the scope recorded in a separate column), or have the report written to a stable path the next run can read. The first is cheaper and keeps the command read-only.
