---
id: "20261027T070344Z-skill-analyze-artifacts"
unit_id: "skill:analyze-artifacts"
unit_type: "skill"
run_id: "r20261027T061144z-a3ec"
scope: "local"
probe: "skill-analyze-artifacts-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-10-27T07:03:44Z"
summary: "analyze-artifacts on Feature 071: the seven passes plus the checklist-accountability pass produced 32 findings (0 CRITICAL / 6 HIGH / 22 MEDIUM / 4 LOW) and consumed all 27 unchecked checklist FAILs w"
---

## Review
analyze-artifacts on Feature 071: the seven passes plus the checklist-accountability pass produced 32 findings (0 CRITICAL / 6 HIGH / 22 MEDIUM / 4 LOW) and consumed all 27 unchecked checklist FAILs with zero undispositioned. Two of the 32 are the self-authored seam defects this pass exists to catch (a Shared Strings consumer column pointing at contract files renamed during plan authoring; a closed report-content list missing a field the same design added). Two HIGH rows were surface-derived rather than chosen: their propagation surface caps dictated MEDIUM, which is what kept the tier honest.

## Optimization Points
- The skill's severity cap is stated as 'propagation_surface none => capped at MEDIUM (the command's own mid tier)', but this command's own table also puts 'ambiguous security/performance attribute; untestable acceptance criterion' at HIGH — and an unverifiable acceptance criterion whose finding nothing downstream inherits is exactly a none-surface row. The two rules give different answers for the same row and the skill does not say which wins; I resolved it by letting the cap win and recording the row at MEDIUM with its decision-class label, which hides a real gate cost (SC-004 remains unimplementable but does not enter the gate count). Suggested owner: shared/workflow/objective-analysis-gate.md rule 3, stating explicitly that a requirement-level acceptance criterion is itself a downstream surface; The checklist-accountability pass requires each unchecked item to be 'raised as a finding or carry an explicit disposition marker', and the marker form is fixed to two shapes (raised-as-finding / covered-by). There is no shape for 're-read and judged not a finding for the stated reason', which is what this run needed for CHK026: the honest verdict was neither 'raised' nor 'covered by an artifact'. I emitted covered-by with the reasoning in prose, but the machine-checkable form now asserts something slightly different from what happened. A third shape (judged-not-a-finding <reason-ref>) would make the identity 'unchecked = raised + covered + judged + undispositioned' honest instead of forcing a near-fit; The same-author detection gate and its validation wave both need subagent dispatch, and three consecutive stages of this line ran without it. The fallback marker is per-row, so a reader counting markers can see the degradation, but nothing measures whether a wave of 'confirm' verdicts from the detecting agent differs from an independent one — and the skill's own rule 6 metric (downgrade rate) becomes unreportable rather than unfavourable. Degradation that cannot be scored is degradation that will keep being chosen.
