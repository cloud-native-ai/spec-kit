---
id: "20260815T061846Z-speckit-instructions"
unit_id: "/speckit.instructions"
unit_type: "command"
run_id: "instructions-20260815-141412"
scope: "local"
probe: "speckit-instructions-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-08-15T06:18:46Z"
summary: "Full reconcile run (no args): setup script non-destructive (backup written, base kept, section reconcile reported all template sections present); agent pass converged 3 silently-drifted numeric facts "
---

## Review
Full reconcile run (no args): setup script non-destructive (backup written, base kept, section reconcile reported all template sections present); agent pass converged 3 silently-drifted numeric facts (principles 10->13, features 35->44, skills 27->31) missed by prior refreshes; symlinks and managed markers intact; diff vs backup exactly 3 lines.

## Optimization Points
- Recurring convergence class: hard-coded counts in Documentation Map / Key Directories (features, skills, principles) drift every time the source grows and survive multiple refreshes. Suggest generate-instructions.sh add a programmatic count-check pass that emits explicit drift lines (instructions-claim vs source-count) so the LLM only repairs flagged rows, or drop volatile counts from map rows in favor of pointers to the source.
