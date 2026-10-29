---
id: "20261029T043138Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "r20261029T045000Z-b074"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "074b-nested-governance"
feature_id: "074"
partial: false
created: "2026-10-29T04:31:38Z"
summary: "requirements stage for slice 074b: gates green on first second-pass; one in-passing correction disclosed (cross-slice id form), no scope or quality regression observed"
---

## Review
requirements stage for slice 074b: gates green on first second-pass; one in-passing correction disclosed (cross-slice id form), no scope or quality regression observed

## Optimization Points
- 1) validate-requirements.py refuses to see [[STR-nnn]] citations that wrap onto a continuation line: the Consumed-by reverse check reads only the definition row's first physical line, so a correctly-cited requirement fails unless the citations are reflowed onto that line; the constraint is undocumented in the validator docstring and cost one fix round. 2) pre-analyze-check.py does not strip inline code spans, so a backticked cross-slice id (FR-020 referring to another slice) is reported as dangling even though validate-requirements.py resolves it correctly; two deterministic gates disagree on the same token class. 3) The slice branch name 074b-nested-governance does not match the ^[0-9]+-<slug> convention, so check-prerequisites.sh cannot resolve the slice spec dir; every downstream slice stage must hard-target the directory.
