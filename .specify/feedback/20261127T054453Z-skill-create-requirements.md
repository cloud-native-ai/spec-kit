---
id: "20261127T054453Z-skill-create-requirements"
unit_id: "skill:create-requirements"
unit_type: "skill"
run_id: "r20261127T053750Z-109a"
scope: "local"
probe: "skill-create-requirements-wrapup"
kind: "internal"
slice: "skills"
feature: "109-prompt-adherence"
partial: false
created: "2026-11-27T05:44:53Z"
summary: "Requirements stage ported ai-harness 092 into spec 109-prompt-adherence: owner document, engine, five declaration facts, six-row catalog, six blind spots and guard roster ported; every read surface, r"
---

## Review
Requirements stage ported ai-harness 092 into spec 109-prompt-adherence: owner document, engine, five declaration facts, six-row catalog, six blind spots and guard roster ported; every read surface, record kind token, CLI form and mirror pair adapted to and verified against this tree. Five open points adjudicated in Assumptions (Feature 109 binding, store-layout read-surface divergence FR-030, no new store, excluded tasks-template hunk, required dated baseline). Validator green on first pass; pre-analyze pass with 3 deliverable-path advisories; decomposition proceed; workspace guard clean. Token self-check: no machine-managed store dumped into context; deterministic branch-number derivation was not handed to a program because the scaffold script is incompatible with the worktree topology; one avoidable spend disclosed (a multi-file cat bundle truncated to a temp file and re-read).

## Optimization Points
- create-requirements scaffold incompatibility: when the worktree is already on the target feature branch, create-new-requirements.sh counts that branch in number derivation and then fails on git checkout -b (or would create 110); add an explicit in-place mode (--no-branch / --branch-number) so unattended SDD stages scaffold without the manual template-copy workaround recorded as 108 A-16 / 109 A-13.
- token-efficiency: avoid a single cat over a contracts bundle; the 37.9 KB output was truncated to a temp file and re-read whole. Read each contract file directly or grep the needed sections.
