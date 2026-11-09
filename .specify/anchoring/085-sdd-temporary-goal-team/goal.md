---
status: active
created: 2026-11-06
updated: 2026-11-06
binding:
  owner: human
  owner_id: human
  origin: 085-sdd-temporary-goal-team
---

# Goal: 085-sdd-temporary-goal-team

## Objective

The SDD framework runs a feature as a temporary, spec-attached Goal/Team with stage-specific agents and explicit concurrency, so a multi-agent SDD run can be observed, adjusted, and archived without touching the global Goal/Team layer.

## Success Criteria

1. A feature run's temporary goal exists only after requirements and its criteria are traceable to evidence rather than duplicated from the requirement success criteria.
2. Stage checkpoints record concurrency, roster, and at most one configuration change, and the dogfood run demonstrates a measurable concurrency gain.
3. Every writing agent has an isolated worktree and the integration queue produces a deterministic, conflict-safe result.

## History

- 2026-11-06 — created.
