---
id: "20261106T075035Z-skill-review-sdd-process"
unit_id: "skill:review-sdd-process"
unit_type: "skill"
run_id: "r20261106t120000z-086rev"
scope: "local"
probe: "skill-review-sdd-process-wrapup"
kind: "internal"
slice: "skills"
feature: "086-efficient-test-execution"
feature_id: "086"
partial: false
created: "2026-11-06T07:50:35Z"
summary: "Process segment of the composed review of 086. Reconstructed the 14-row timeline from git log plus test-evidence; judged four disclosed limitations and found three of four do not stand as disclosed: t"
---

## Review
Process segment of the composed review of 086. Reconstructed the 14-row timeline from git log plus test-evidence; judged four disclosed limitations and found three of four do not stand as disclosed: the SC-003 substitution (F1 P1, F3 P2), the mutation-leg carrier-map backfill (F2 P1) and the predicted-Blocked status write (F6 P1). The fourth (.specify/memory/trigger/index.json as runtime residue) stands and was correctly not treated as a finding. Also raised F4, F5, F7, F8, F9. No P0.

## Optimization Points
- 1) A 'final' criterion was accepted on a substituted surface (shipped templates instead of rendered downstream output) without the report naming the substitution as a narrowing; the process rules have no verb for 'this criterion was read on a weaker surface than its text names', so the narrowing has to be inferred by the reviewer rather than declared by the executor.|2) DoD-2's mutation-leg carrier map was marked met before the named carrier files existed, and the backfill of M-2..M-4 and M-10..M-15 readings was not recorded as a red-first event; the task-carrier mechanism checks that a carrier is NAMED, never that the named file exists at the time of the claim.|3) The feature-details status field was written as Blocked as a prediction before closure-acceptance-check.py had returned, then corrected after the accept verdict; there is no rule forbidding a pre-written status, so a wrong prediction and a wrong conclusion are indistinguishable in the record.|4) The two-slot full-run budget is enforced by executor discipline and an audit script that reads the ledger, not by a machine that can refuse the third run; a ledger row can be written for a run that never happened and nothing detects it.|5) The temporary-SDD-run mechanism has a stage for every authoring artifact but no stage for the process defect that recurs across waves (sandbox worktree inside the repo root), so the same class of defect is re-discovered rather than inherited as a guard.
