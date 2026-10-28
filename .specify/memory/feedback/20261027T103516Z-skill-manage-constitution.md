---
id: "20261027T103516Z-skill-manage-constitution"
unit_id: "skill:manage-constitution"
unit_type: "skill"
run_id: "r20261027T1828Z-directory-governance"
scope: "local"
probe: "skill-manage-constitution-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-10-27T10:35:16Z"
summary: "v1.14.0 MINOR amendment landed (Principle XVII Directory Governance) across live constitution, template, generator skill, ambient pointer and a new owner doc; focused contract tests green; remaining s"
---

## Review
v1.14.0 MINOR amendment landed (Principle XVII Directory Governance) across live constitution, template, generator skill, ambient pointer and a new owner doc; focused contract tests green; remaining suite failures are pre-existing stale pins.

## Optimization Points
- Pre-existing stale pins: test_fast_fail a7 (24/25 vs actual 26/27 sections), g9 + neutrality cap + proactive trigger (frozen gate total 23 vs live 27), registry header/rows, and mirror drift (improve-skills loop-playbook; sdd-project-setup setup-recipes + missing logical-framework.py). Refreshing these is a separate baseline task.
- Slice-scoped frozen baselines (test_expression_compatibility) go red on any later legitimate amendment; the new ALLOWED_POST_BASELINE_PATHS entry handles .specify/instructions.md, but the pattern could be generalized.
- The repo-root .spec-kit/ runtime state was untracked and unignored; it is now registered as the loop driver's runtime root (directory-governance §5) and .gitignore covers it.
- Template carries XV Single-Run Evidence while the live constitution does not; pre-existing asymmetry, not caused by this amendment.
