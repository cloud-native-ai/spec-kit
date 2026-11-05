---
id: "20261105T133034Z-skill-sanitize-materials"
unit_id: "skill:sanitize-materials"
unit_type: "skill"
run_id: "r20261105T133000Z-sanitize"
scope: "local"
probe: "skill-sanitize-materials-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-11-05T13:30:34Z"
summary: "Executed the sanitize materials cleanup on the spec-kit workspace: 2,495 dead-reference findings plus 1 stale residue. Archived .specify/tools under the user's explicit cleanup request. A first blanke"
---

## Review
Executed the sanitize materials cleanup on the spec-kit workspace: 2,495 dead-reference findings plus 1 stale residue. Archived .specify/tools under the user's explicit cleanup request. A first blanket-replacement pass corrupted text (e.g. .opencode/agents/x.md -> .opencode/) and was reverted; the redo used bounded exact-token, existence-verified replacements: 1,453 substitutions across 296 files, 1,023 findings resolved, 1,521 dismissed state-only as historical/prose/example/placeholder/scanner artifacts, 49 equivalent findings surfaced by re-scan and dismissed the same way. Ledger 2,544 resolved / 0 pending. Targeted sanitize/registry and contract subsets passed (153 + 140) before the user asked to skip further tests.

## Optimization Points
- token-efficiency: the first repair pass applied blanket replacements and had to be discarded (607 files reverted); anchoring every candidate to an existence-checked mapping avoids the wasted edit + re-collect cycle.
- sanitize engine: REPO_PATH_RE/SKILL_REF_RE are not boundary-anchored, so agents/<file> inside .opencode/agents/<file>, skills/<name> inside docs/reference/skills/<name>.md, and placeholder-prefixed tokens are reported as dead; 1,521 findings required dismissal and will be re-detected on the next full scan unless the engine anchors or exempts them.
- sanitize engine: apply() marks dismiss items resolved, not dismissed, so adjudicated false positives reopen on the next full collect; the findings contract's dismissed state (C-12) is unreachable from apply.
- Placeholder truncation: a token like .specify/specs/078-coaching-<dir> is matched only up to '<' and the bare prefix is reported dead even though the placeholder form is intentional.
