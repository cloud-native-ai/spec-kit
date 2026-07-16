---
id: "20260716T073831Z-skill-draw-plantuml"
unit_id: "skill:draw-plantuml"
unit_type: "skill"
run_id: "gen21-textdecor-d1"
scope: "local"
feature: "arc4-context-split"
partial: false
created: "2026-07-16T07:38:31Z"
summary: "Applied a focused text-decoration pass to 图1 Overview: stripped the 3 layer boxes (access/k8s/exec) to concise bold titles + tiny cross-ref, moved verbose multi-clause descriptions into 3 family-tinte"
---

## Review
Applied a focused text-decoration pass to 图1 Overview: stripped the 3 layer boxes (access/k8s/exec) to concise bold titles + tiny cross-ref, moved verbose multi-clause descriptions into 3 family-tinted external notes, kept iaas/actors undecorated (selectivity), preserved the ★callout/legend/footer/channels/colors. All 4 notes verified layout-safe against the render (no fling/crossing); viewBox 11762x10562 vs seed 10100x10962, render succeeded.

## Optimization Points
- When applying the text-decoration step, prefer placing external notes on the element side that faces existing whitespace (inspect the seed render first): here `left of k8s`/`left of exec`/`right of access` filled the seed's empty left and bottom-left gaps, so decorating actually *improved* balance instead of harming it. A quick whitespace map before choosing note anchors avoids margin-fling reflows.
- Tinting each detail note with a lighter shade of its element's family color (blue/green/amber) preserves the semantic color channel while keeping the note visually subordinate to the box — reserve the saturated alert tint (#FFCDD2) for the single ★ callout.
