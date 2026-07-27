---
id: "20260727T032629Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-summarize-project-selfcontained-20260727"
scope: "local"
feature: "summarize-project"
partial: false
created: "2026-07-27T03:26:29Z"
summary: "Improved summarize-project per user emphasis on self-contained output. Root cause found in skill text itself: rendering was optional and images were referenced by relative path (SKILL.md Step 6, playb"
---

## Review
Improved summarize-project per user emphasis on self-contained output. Root cause found in skill text itself: rendering was optional and images were referenced by relative path (SKILL.md Step 6, playbook §1/§6), so the report depended on sibling files and a reader-side renderer. Fix: new 自包含交付 core principle, Step 6 rewritten to mandatory render + inline SVG embedding with path/URL image bans, Step 7 self-containment check, playbook skeleton markers and both checklists updated. Mirror synced byte-identical; 43/43 skill contract tests pass; full-suite stash diff shows zero regression.

## Optimization Points
- When a skill's output is a deliverable for external readers, "optional rendering + relative-path images" silently produces a report that breaks when moved or shared; self-containment must be a stated core principle with a pre-landing checklist gate (no path/URL image refs, every source block has an inline rendered figure), not an afterthought.
