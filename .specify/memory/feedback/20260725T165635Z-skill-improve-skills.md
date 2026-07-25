---
id: "20260725T165635Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-skills-summarize-project-rename-20260726"
scope: "local"
feature: "013"
partial: false
created: "2026-07-25T16:56:35Z"
summary: "Renamed visualize-project back to summarize-project per user direction: the report pairs textual summary with visual charts, so 'summarize' is the more accurate name (also the original spec-030 name)."
---

## Review
Renamed visualize-project back to summarize-project per user direction: the report pairs textual summary with visual charts, so 'summarize' is the more accurate name (also the original spec-030 name). Pure rename + framing edit with zero positioning change: git mv of both skill trees and the contract test, frontmatter/description reframed as text+charts, playbook renamed to reporting-playbook.md, report defaults moved to summary.md/project-summary.md, detect-script output updated, visualize-project added to _OBSOLETE_SKILLS (committed on local master), registry row + skills list + feature history + dogfood-doc header updated. Discovered the user had evolved the skill between turns (five-layer references structure) — adapted the rename to preserve it. Validation: 49 contract tests green; full-suite failure set byte-identical to pre-change baseline via stash diff (52F/13E pre-existing); detect script runtime-checked.

## Optimization Points
- A rename loop must re-read every file at its NEW path before editing: Write/Edit tools gate on having Read the exact path, and content may also have evolved between turns (this run hit both — the user had enhanced the skill with a five-layer references structure after the previous loop). "git mv first, then re-read, then edit" is the safe order.
- When the predecessor name was committed to the local master (even unpushed/untagged), add it to `_OBSOLETE_SKILLS` — workspaces initialized from that commit would otherwise keep the stale skill directory forever. Rename chains should be documented in the manifest comment (manage-project→visualize-project→summarize-project).
