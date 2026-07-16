---
id: "20260716T074022Z-skill-draw-plantuml"
unit_id: "skill:draw-plantuml"
unit_type: "skill"
run_id: "gen21-textdecor-d2"
scope: "local"
feature: "arc4-context-split"
partial: false
created: "2026-07-16T07:40:22Z"
summary: "文字修饰 pass on 图2 Deployment&Governance: stripped verbose subtitles to concise titles (always-safe win), then attempted external explanatory notes. Layout-safety guard proved decisive — of 3 candidate n"
---

## Review
文字修饰 pass on 图2 Deployment&Governance: stripped verbose subtitles to concise titles (always-safe win), then attempted external explanatory notes. Layout-safety guard proved decisive — of 3 candidate notes, 2 flew to far margins (crd deep in DECL frame; sys nested node) and were omitted; only the top-level worker node note settled adjacent. Final: 2 notes (worker + preserved etcd callout), viewBox 19625x9275 vs seed 17400x9500, all constraints preserved.

## Optimization Points
- On nested PlantUML deployment diagrams (frame→node→component), notes attached to deep members (agent/wasm) or even frame-level members (crd, and the nested node sys) frequently fly to a far margin and inflate the canvas (17400→23837 wide with 3 notes). Only notes on the outermost sibling node (worker) settled adjacent to their element. Practical rule: attach explanatory notes ONLY to top-level nodes; for deep members fold their detail into the parent node's note, and keep cross-refs (▶见图N) inline as concise titles rather than as notes.
- A per-element decision log (kept as inline comments: which note added vs omitted and why) makes the layout-safety "omit rather than harm" pass auditable and reversible across regenerations.
