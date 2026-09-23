---
id: "20260915T065348Z-skill-create-skills"
unit_id: "skill:create-skills"
unit_type: "skill"
run_id: "20260915T070500Z-create-draw-diagram"
scope: "local"
probe: "skill-create-skills-wrapup"
kind: "internal"
slice: "skills"
feature: "draw-diagram-front-door"
partial: false
created: "2026-09-15T06:53:48Z"
summary: "Created skills/draw-diagram front door (semantic LDM + exclusivity registry + delegation) over five draw-* specialists; mirror and host load-dir wired; conformance suite attributed failures to pre-exi"
introspection_ref: "introspection-20260923T120035Z#F-21"
---

## Review
Created skills/draw-diagram front door (semantic LDM + exclusivity registry + delegation) over five draw-* specialists; mirror and host load-dir wired; conformance suite attributed failures to pre-existing draw-excalidraw debt, new skill clean; RED-GREEN pressure pair 2 demonstrated registry-first routing value.

## Optimization Points
- For front-door/routing skills, pressure scenarios must be discriminative against the exclusivity registry: scenario 1 (editable-whiteboard) passed RED even WITHOUT the skill because the lower-layer excalidraw description already carries a strong editability cue; add a scenario-selection rule to create-skills pressure-testing guidance — pick requests whose lower-layer description cues point in the WRONG direction (e.g. pixel-replication vs "架构图" keyword pulling to plantuml/mermaid).
- When a parallel session actively edits the same skill family, conformance-suite failures must be attributed per-skill before treating them as regressions of the new skill; the attribution command (pytest --tb=line on the conformance files, read the asserted skill list) should be cited in the completion report.
