---
id: "20260725T161016Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-visualize-project-layering-20260726"
scope: "local"
feature: "013"
partial: false
created: "2026-07-25T16:10:16Z"
summary: "Layered decomposition of visualize-project per user direction: split the monolithic visualization-playbook.md into five per-layer reference docs (project-overview / requirements-features / work-breakd"
---

## Review
Layered decomposition of visualize-project per user direction: split the monolithic visualization-playbook.md into five per-layer reference docs (project-overview / requirements-features / work-breakdown / milestones / task-progress), each answering one external-reader question (goals, capabilities, tasks, milestones-achieved, per-task status + overall schedule) with uniform structure (呈现要素→取材优先级→规则→落笔检查). Playbook slimmed to cross-layer conventions plus a question→layer index; SKILL.md gained the question/layer mapping table and per-step layer-doc pointers. Mirror synced byte-identically; contract tests extended 33→42 (9 new layered-reference tests, 1 retargeted), all green; full contract suite matches the documented 52F/13E pre-existing baseline with zero regressions.

## Optimization Points
- When a user asks for a "one reference doc per concern" decomposition, deriving the layer set from the report's existing section skeleton (5 sections → 5 layer docs) kept the mapping contract-stable and avoided inventing a parallel taxonomy; reuse this section-driven decomposition heuristic for future doc-splitting requests.
- Contract tests that pin content to a specific reference file (e.g. 推断/退化 asserted inside visualization-playbook.md) break on any content relocation; prefer asserting per-layer semantics against the owning layer doc, and only skeleton/index/cross-layer rules against the playbook, so future restructures stay cheap.
