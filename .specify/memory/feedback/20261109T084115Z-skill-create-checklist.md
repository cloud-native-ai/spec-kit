---
id: "20261109T084115Z-skill-create-checklist"
unit_id: "skill:create-checklist"
unit_type: "skill"
run_id: "093-checklist-skill-a1"
scope: "local"
probe: "skill-create-checklist-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-09T08:41:15Z"
summary: "needs-improvement"
---

## Review
needs-improvement

## Optimization Points
- the skill binds its evidence to doc-consistency-check.py's reader/duplicate faces as separate repo-wide checks; neither face judges checklist items, and with the duplicate face blind under .specify/ the skill must carry its own item-level machine check (count, ids, anchors, duplicate bodies)
