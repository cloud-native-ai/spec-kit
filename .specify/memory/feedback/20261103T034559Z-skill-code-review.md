---
id: "20261103T034559Z-skill-code-review"
unit_id: "skill:code-review"
unit_type: "skill"
run_id: "r20261102T225758Z-081a"
scope: "local"
probe: "skill-code-review-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-03T03:45:59Z"
summary: "Code segment over f9f6d4f3..d0186dc5, 90de4d7f excluded as concurrent non-081 work. 7 findings: FR-006's three named counts unimplemented; contract C-03/C-05 stale; final_path bucket set cannot repres"
---

## Review
Code segment over f9f6d4f3..d0186dc5, 90de4d7f excluded as concurrent non-081 work. 7 findings: FR-006's three named counts unimplemented; contract C-03/C-05 stale; final_path bucket set cannot represent partial; a Markdown bold marker lost in templates/commands/tasks.md and propagated to four copies.

## Optimization Points
- A closed output-field contract should be asserted by a test that reads the requirement's literal field names, so an implementation drift from final_pass/final_blocked/final_deferred to a different shape is caught mechanically.
