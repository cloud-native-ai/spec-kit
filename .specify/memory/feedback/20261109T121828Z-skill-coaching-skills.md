---
id: "20261109T121828Z-skill-coaching-skills"
unit_id: "skill:coaching-skills"
unit_type: "skill"
run_id: "20261109T121113Z-speckit-history"
scope: "local"
probe: "skill-coaching-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-09T12:18:28Z"
summary: "pass"
---

## Review
pass

## Optimization Points
- coaching /speckit.history (no-arg): seam-stop before Step B caused by concurrent external writers incl. the coach's own sibling-run commits; inherited none-of applied; zero tracked writes; run=partial (coach-caused), lesson: history seam windows are exclusive per workspace
