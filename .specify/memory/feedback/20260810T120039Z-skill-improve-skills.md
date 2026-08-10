---
id: "20260810T120039Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "git-workflow-instructions-block-20260810"
scope: "local"
partial: false
created: "2026-08-10T12:00:39Z"
summary: "Moved git-workflow's branch data out of a generated document and into a GIT_WORKFLOW managed block in the project's instructions file, per user request. Corrected two premise errors first (the store w"
---

## Review
Moved git-workflow's branch data out of a generated document and into a GIT_WORKFLOW managed block in the project's instructions file, per user request. Corrected two premise errors first (the store was .specify/memory/git-workflow.md, not docs/git-workflow.md; neither existed since the skill was never bootstrapped here). Scoped the move to branch STATE, keeping the 216-line asset's procedure out of ambient context because every section of it already existed in the skill's own references — then deleted that duplicate asset. Registered the block in both the instructions template and the refresh command's preserve-list so a later refresh cannot overwrite it, rewired all skill scope/read/write paths, repurposed instructions-lookup.md with marker-only write rules and a symlink warning, and kept both legacy paths as migration sources with no auto-delete. 8 new contract assertions green; full suite 37 failures vs 44 at HEAD baseline, zero attributable to this change.

## Optimization Points
- Verify the user's premise about file locations before acting: the request named `docs/git-workflow.md`, but the skill actually wrote `.specify/memory/git-workflow.md` (docs/ was a legacy path it only migrated away from) and neither file existed in this repo — the skill had never been bootstrapped here. Stating the correction up front avoided "moving" a file that did not exist.
- Measure a pipeline's exit code, not the exit code of the pipe. `sync-mirrors --check ... | grep | tail; echo $?` reported 0 while the engine was actually returning 2 (drift), which nearly concealed an unsynced mirror. Read the engine's own status, or capture it before piping.
- sync-mirrors --write aborts on the first PermissionError and still prints its planned DIFF lines, so several mirror files silently stayed stale: five `.specify/skills/git-workflow/*` files were root-owned from a prior container run. The recurring-lessons entry about root-owned dirs should be extended to mirror FILES, and the engine would be better off collecting per-file errors and exiting non-zero with a summary rather than dying on the first one. It also never prunes files deleted from the canonical source (the removed 216-line asset survived in the mirror until deleted by hand) — a byte-level mirror-parity assertion in the contract test is what caught both.
- Registering a new managed range needs two edits, not one: the marker block in `templates/instructions-template.md` AND the enumerated preserve-list in `templates/commands/instructions.md`. Registering only the first would let a later /speckit.instructions refresh converge (overwrite) the branch data. One of the two edits was silently lost to a failed-then-not-retried Edit call and only the contract test caught it.
- token-efficiency: the 216-line asset was pure duplication of the skill's own references (execute-commands / troubleshooting / gitexcludes-subroutine / SKILL.md Security); moving branch state into instructions.md (~10 lines of ambient context) while deleting the duplicate removed a third copy instead of adding one.
