---
id: "20260807T035328Z-skill-create-skills"
unit_id: "skill:create-skills"
unit_type: "skill"
run_id: "20260807-create-draw-mermaid"
scope: "local"
feature: "draw-mermaid-skill"
partial: false
created: "2026-08-07T03:53:28Z"
summary: "Created skills/draw-mermaid mirroring draw-plantuml: full PlantUML-to-Mermaid type mapping, 8-step workflow, render pipeline verified live against mermaid.ink; registry, mirrors, and agent wiring upda"
---

## Review
Created skills/draw-mermaid mirroring draw-plantuml: full PlantUML-to-Mermaid type mapping, 8-step workflow, render pipeline verified live against mermaid.ink; registry, mirrors, and agent wiring updated; contract suite shows 0 new failures.

## Optimization Points
- draw-mermaid skill created mirroring draw-plantuml: 49 files (SKILL.md, 3 scripts, index, 6 guide, 21 howto, 17 document) with full PlantUML→Mermaid type mapping; render-mermaid.sh (mermaid.ink pako protocol + local mmdc) verified end-to-end (percent-encoding and ?type=png were the two fixes needed).
- Optimization point: create-skills could codify the "cp -r nested-destination" hazard (mirror copies ending up nested when the destination already exists) and the `\cp` unaliased-copy lesson as a checklist item; also recommend creating the mirror copy via sync-mirrors.py instead of raw cp.
