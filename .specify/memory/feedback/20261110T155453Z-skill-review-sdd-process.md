---
id: "20261110T155453Z-skill-review-sdd-process"
unit_id: "skill:review-sdd-process"
unit_type: "skill"
run_id: "r20261110T081104Z-b097"
scope: "local"
probe: "skill-review-sdd-process-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-10T15:54:53Z"
summary: "Process segment: 16-event timeline reconstructed from git; findings F1-F6 (P1: stale state spine, owner-conflict repair loop, ignored analyze M/L backlog; P2: uncommitted stage checkpoints, incomplete"
---

## Review
Process segment: 16-event timeline reconstructed from git; findings F1-F6 (P1: stale state spine, owner-conflict repair loop, ignored analyze M/L backlog; P2: uncommitted stage checkpoints, incomplete constitution carrier sweep, unchecked evidence pointers). One P0 (A1) validated by an independent read-only subagent.

## Optimization Points
- The state spine lives outside the worktree, so a worktree-local review silently misses it; the report only found the staleness by citing the absolute path.
- The same-author gate and the P0 validation wave both require fresh-context subagents; no guidance covers reusing one read-only pass when the artifacts came from earlier sessions.
