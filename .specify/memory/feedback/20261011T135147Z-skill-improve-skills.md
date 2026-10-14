---
id: "20261011T135147Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-merge-skills-provenance-20261011T1320"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
disposition: "processed"
partial: false
created: "2026-10-11T13:51:47Z"
summary: "Ran a full improvement loop on merge-skills against a user requirement (retain a functional record and verifiable capability checklist of pre-merge skills inside the merged target). Research preceded "
introspection_ref: "introspection-20261013T155006Z#F-01"
disposition_reason: "introspection:introspection-20261013T155006Z#F-01"
---

## Review
Ran a full improvement loop on merge-skills against a user requirement (retain a functional record and verifiable capability checklist of pre-merge skills inside the merged target). Research preceded edits: read the whole target implementation, then grounded the defect in the one real completed merge in this repo (git-workflow/git-fleet/git-server-init/git-submodule-edit -> git-workspace), whose allow file and scratch survived only in a git-ignored team workspace while the target itself carried a name-level assertion. Delivered the requirement as a committed capability-inheritance record plus frozen coverage baselines and a re-verification gate; validated on real merge data (807 frozen tokens across 4 sources, re-verified clean) and via 31 behavioral cases. Pressure testing surfaced three soundness defects in my own new code (non-idempotent extraction, tokens beginning with '#' silently dropped on re-read, provenance artifacts inside their own corpus) plus one pre-existing probe false-negative (independent enum words swallowed as substrings of longer constants) — all repaired, the last one disclosed as an in-passing correction. Both gates exit 0; contract-suite failure set identical to a clean HEAD worktree, so zero regression; mirrors synced. Outcome is pending: no next-run comparison exists yet, so nothing here is claimed as fixed.

## Optimization Points
- Step 3 evidence lane returned no target-specific signal. `evidence-utils.py --action collect --target skill:merge-skills --lanes all` produced 17 entries, of which 15 were project-level (language profile, dependency governance, asset lint, per-team run-report counts) and one was `Unobserved`. Nothing described the target skill's own behavior or outputs. Every load-bearing observation this loop came from inspecting the artifacts the target skill had *produced* elsewhere in the repo — a merged target carrying only a name-level "formerly four skills, content preserved" note, and its 18-entry allow file surviving solely in a git-ignored team workspace. Step 3 should name "the target skill's own produced artifacts in the repo" as a first-class evidence source to consult when the engine returns only project-level signal, instead of leaving the agent to improvise that search.
- Step 8's shape gate reports pass/fail but not headroom consumed. merge-skills' `SKILL.md` went from 3491 to 4545 controllable tokens against a 5000 budget — 91% consumed, gate still exit 0. Nothing in the loop forced the slimming pass; I ran it by choice, and a loop that skipped it would have reported a clean pass while leaving ~450 tokens for every future edit. Hard Constraint 3 requires the before/after delta only when the gate trips, which is exactly the case where it is too late. Step 8 should require the delta and remaining-headroom disclosure whenever a loop *grows* the body at all, not only past the threshold.
- Pressure-test matrices authored in `/tmp` are invisible to the run-determination anti-vacuity guard. This loop executed 31 behavioral cases across two scripts (19 provenance-checker verdicts, 12 probe regression cases) plus four real-data round-trip checks, and caught three genuine soundness defects that way. But `--green-check` entries were all reported `green evidence absent`, so `artifact_correctness` settled as `not_evaluated / green_unproven` — because the guard searches a declared red-first file for each check's literal name, and the matrices were ephemeral. The verdict is defensible (no durable artifact pins those checks) yet it reads the same as "the loop validated nothing". Step 8 should either commit the matrix where the guard can see it, or require the loop report to state plainly that its checks are unrepeatable by a later session, so an unrepeatable validation is not mistaken for an absent one.
