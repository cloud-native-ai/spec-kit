---
id: "20260730T130054Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-20260730-article-bestpractices"
scope: "local"
partial: false
created: "2026-07-30T13:00:54Z"
summary: "Applied externally sourced, quantified skill best-practice knowledge (150-run constraint-injection experiment + LLM Wiki L0-L3 model) to improve-skills: added constraint non-compliance failure mode, e"
---

## Review
Applied externally sourced, quantified skill best-practice knowledge (150-run constraint-injection experiment + LLM Wiki L0-L3 model) to improve-skills: added constraint non-compliance failure mode, evidence-based placement fix ladder (new references/constraint-placement.md), checklist group, and L0-L3 compliance rationale in slimming principles. Zero contract-test regression proven via clean-worktree failure-set diff.

## Optimization Points
- The evidence engine returned a fresh findings run with 0 findings for skill:improve-skills; when the improvement is driven purely by user-supplied external knowledge (articles), the workflow's evidence-step wording could acknowledge "external-knowledge-driven run with empty findings" explicitly so future runs don't over-search for execution evidence that doesn't exist.
- SearchReplace tool reported "save failed, reason: unknown" on edits that had actually persisted; verifying with grep before retrying avoided duplicate insertions — worth remembering as a tooling caution for future improvement loops.
