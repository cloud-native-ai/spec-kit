---
id: "20260716T102401Z-skill-draw-plantuml"
unit_id: "skill:draw-plantuml"
unit_type: "skill"
run_id: "arc7-stability-round2-deploy-govern"
scope: "local"
feature: "draw-plantuml-optimizer"
partial: false
created: "2026-07-16T10:24:01Z"
summary: "Generated a band-by-plane E2B deployment & governance diagram from the context digest, strictly applying diagram-principles §1-§4 and large-diagram-playbook §4d/§4e/§2/§5. Full UML deployment semantic"
---

## Review
Generated a band-by-plane E2B deployment & governance diagram from the context digest, strictly applying diagram-principles §1-§4 and large-diagram-playbook §4d/§4e/§2/§5. Full UML deployment semantics (node/artifact/database/cloud/component/interface + «stereotype» + «×N»), two governance planes (③ declarative into etcd vs ④ imperative out-of-band gRPC bypassing API Server), per-tenant control plane «×N» + single shared Node Agent hub, four-tier font ladder, semantic color families, self-sufficient legend. Reached clean two-band horizontal stack after 4 renders; main friction was Graphviz cross-cluster band placement and a color-persistence bug on re-render into the same basename.

## Optimization Points
- When input path and output prefix resolve to the same `.puml` (as this task's render command mandates), `render-plantuml.sh` overwrites the source with its style-injected copy and `strip_style` deletes `skinparam monochrome false`. On a *second* render the color-detection (`grep '<color:|<font color|skinparam monochrome false'`) no longer fires, so `skinparam monochrome true` is injected and a colored diagram silently reverts to grayscale — losing semantic color families. Robust fix applied: embed a `<color:#...>` token in a comment line (survives `strip_style`) so detection always fires. The skill/guide should document this color-persistence gotcha for iterative renders into the same basename.
- Band-by-plane (§4d/§4e) with nested frames hits the §4c cross-cluster wall: a tall narrow top band sits *beside* a wide bottom band. The decisive lever was converting in-band flow edges to explicit `-right->` (flatten each band to a single rank) + direct `B1 -[hidden]down-> B2` frame stacking + corner pins. A worked band-by-plane code sample in the playbook would shorten the iterate loop (took 4 renders).
