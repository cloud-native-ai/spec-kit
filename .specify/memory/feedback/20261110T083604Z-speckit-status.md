---
id: "20261110T083604Z-speckit-status"
unit_id: "/speckit.status"
unit_type: "command"
run_id: "20261110T083603Z-speckit-status"
scope: "local"
probe: "speckit-status-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-11-10T08:36:04Z"
summary: "digest rendered verbatim, exit 0; worktree-based lines absent from the projection"
---

## Review
digest rendered verbatim, exit 0; worktree-based lines absent from the projection

## Optimization Points
- projection gap: registry lines whose project_dir is a worktree do not appear when the digest runs from the main tree
