---
id: "20260730T064240Z-skill-create-team"
unit_id: "skill:create-team"
unit_type: "skill"
run_id: "meta-write-authority-clarification-20260730"
scope: "local"
partial: false
created: "2026-07-30T06:42:40Z"
summary: "Clarified the Meta<->role relationship as a one-way implication, closing the confusion that made the retired coupling feel compulsory. Stated in conceptual-model.md (new 'Meta and write authority' sub"
---

## Review
Clarified the Meta<->role relationship as a one-way implication, closing the confusion that made the retired coupling feel compulsory. Stated in conceptual-model.md (new 'Meta and write authority' subsection), the create-team roster step, and design.md: modifying team config / agent definitions / skill definitions requires Meta (necessary), but holding an evaluator/optimizer/continuous-improvement role does not by itself imply Meta (not sufficient) — no biconditional. Decide Type by what the member writes to, not its role name. Validation: failure set identical to baseline (74), zero new; create-team mirror byte-identical.

## Optimization Points
- The Type criterion clarification was incomplete without stating the direction of implication. Readers correctly observe that in practice the continuous-improvement agent in a complex team is almost always Meta, and without an explicit "necessary but not sufficient" statement they re-derive the very biconditional we just removed. Documenting a corrected rule should also name the true relationship (one-way implication via write authority) so the intuition behind the old error has somewhere legitimate to land.
- The real invariant is a write-authority gate, not a role-to-type mapping: only Meta may modify team config / agent definitions / skill definitions. Anchoring Type to "what the member writes to" is more robust than anchoring it to operating-object abstraction alone, because it gives roster-building a concrete, checkable question ("does this member write agent/skill/team definitions?") instead of an abstract classification.
