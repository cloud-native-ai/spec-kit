---
id: "20261027T062017Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "r20261027T061144Z-a3ec"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-10-27T06:20:17Z"
summary: "requirements stage for Feature 071 (review x code-review composition): artifacts landed and committed at 8d18265b"
---

## Review
requirements stage for Feature 071 (review x code-review composition): artifacts landed and committed at 8d18265b

## Optimization Points
- validate-requirements.py --ref-resolvable reads code-span-stripped lines, so a Shared Strings citation written the natural way inside backticks is invisible: the first pass exited 1 with 10 ref-resolvable errors for citations that were present. The Shared Strings section teaches the [[STR-NNN]] form in a code span, which is exactly the shape the checker discards; the citation form and the checker disagree
