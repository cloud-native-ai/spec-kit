---
id: "20260814T080457Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-create-pages-generalization-2026-08-14"
scope: "local"
feature: "create-pages"
partial: false
created: "2026-08-14T08:04:57Z"
summary: "Generalized create-pages skill per user direction: added --platform parameter with ci-templates/ registry (aoneci implemented as moved-out template, github structural stub), marked --image environment"
---

## Review
Generalized create-pages skill per user direction: added --platform parameter with ci-templates/ registry (aoneci implemented as moved-out template, github structural stub), marked --image environment-specific. Baseline byte-identical regression proof for aoneci default; stub/unknown-platform/image-override branches runtime-verified; shape gate pass; mirrors synced byte-equal. Main friction: root-owned canonical dir forced staging-swap workaround.

## Optimization Points
- ## Optimization Points
- Preflight writability check missing: the canonical skill dir (skills/create-pages/) was root-owned, so direct Edit failed and required a staging-copy + rename-swap workaround. improve-skills Step 1 should include a one-line writability preflight (`test -w <SKILL.md>`) and a documented staging-swap recovery path, deferring the root-cause `sudo chown` fix to the user.
- Leftover-backup pollution pattern: a root-owned backup kept inside skills/ is re-mirrored by every sync-mirrors.py run and re-discovered as a duplicate skill; the only agent-side mitigation is exclusion entries + user sudo cleanup. Worth recording as a recurring-environment lesson (AGENTS.md already documents the root-owned-mirror variant, but not the backup-inside-source variant).
