---
id: "20260725T154402Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-visualize-project-refactor-20260725"
scope: "local"
feature: "013"
partial: false
created: "2026-07-25T15:44:02Z"
summary: "Refactored manage-project into visualize-project per user direction: repositioned from a PM input tool (overlapping spec-kit's own requirements/features/tasks framework) into a read-only presentation/"
---

## Review
Refactored manage-project into visualize-project per user direction: repositioned from a PM input tool (overlapping spec-kit's own requirements/features/tasks framework) into a read-only presentation/output tool producing a derived visual status report. Added SpecKit auto-detection (codified as scripts/detect-project-sources.py per the deterministic-logic-to-code principle), multi-source inputs (code/README/docs/external documents/git), dropped the agile management loop and integration seams, rewrote playbook with derived-report refresh semantics, mirrored to .specify/skills byte-identically, added manage-project to _OBSOLETE_SKILLS, rewrote contract tests (35 new, all green), and verified zero regressions via stash-based before/after failure-set diff (52F/13E pre-existing baseline identical).

## Optimization Points
- When an improvement is a full skill **rename/removal** (not just an edit), the loop should carry an explicit downstream-wiring checklist: `_OBSOLETE_SKILLS` cleanup manifest entry, contract-test file rename, `.specify/instructions.md` registry row + skills-count list, feature-history entry, and stale-pointer fixes in dogfooded artifacts. These are easy to miss because grep only finds textual references; the obsolete-manifest and test-rename steps have no textual trail.
- The stash-based before/after failure-set diff (capture `FAILED|ERROR` lines, stash, rerun, diff) proved to be a reliable way to distinguish pre-existing baseline failures from regressions; worth referencing in the validation step as a concrete technique alongside "run the affected contract tests".
