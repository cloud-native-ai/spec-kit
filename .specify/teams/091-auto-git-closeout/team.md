---
name: SDD Temporary Team 091
slug: 091-auto-git-closeout
description: Run-scoped SDD team for Feature 091 — Automatic git close-out; serial stage chain over tasks / implement / review with per-stage coordinator + executor seats, one independent verifier reserve per stage, and roster-only creation (execution belongs to the SDD driver).
scope: spec
spec_dir: .specify/specs/091-auto-git-closeout
lifecycle_state: archived
goal: >-
  Every retained write ends with one git close-out (commit -> merge -> push) whose sequence is derived
  from the model declared in .specify/workflow/git.md, with no per-run manual trigger; the four workflow
  models reproduce their sequences in fixture repositories, ask/absent policy presents and waits, push
  rejection or merge conflict stops at the first failure without force-push or a second retry, and the
  artifact commands and unattended runs use the same close-out step (no second mechanism).
goal_slug: 091-auto-git-closeout
territory:
  write:
    - .specify/specs/091-auto-git-closeout/**
    - .specify/state/091-auto-git-closeout.md
    - .specify/workflow/git.md
    - .specify/memory/features.md
    - .specify/memory/features/091.md
    - shared/workflow/artifact-commit-step.md
    - .specify/shared/workflow/artifact-commit-step.md
    - shared/definitions/framework-map.md
    - .specify/shared/definitions/framework-map.md
    - skills/external/git-utils/**
    - .specify/skills/git-utils/**
    - scripts/python/**
    - .specify/scripts/python/**
    - tests/contract/**
    - templates/instructions-template.md
    - .specify/templates/instructions-template.md
    - .specify/instructions.md
  read:
    - "**"
  forbidden:
    - .specify/goal/**
    - .specify/teams/**
    - .specify/specs/085-sdd-temporary-goal-team/**
    - .specify/specs/086-efficient-test-execution/**
    - .specify/specs/087-arch-diagram-docs/**
    - .specify/specs/088-speckit-visualization/**
    - .specify/specs/089-script-interface-contract/**
    - .specify/specs/090-re-anchoring/**
  non_path:
    - { type: runtime, target: "host agent concurrency and rendered agent surfaces (specify render-agents output)" }
pattern: serial
created: 2026-11-09
updated: 2026-11-09
seats:
  sdd-task-coordinator:
    sdd-invocation: forbidden
  sdd-task-executor:
    sdd-invocation: forbidden
  sdd-implement-coordinator:
    sdd-invocation: forbidden
  sdd-implement-executor:
    sdd-invocation: forbidden
  sdd-review-coordinator:
    sdd-invocation: forbidden
  sdd-review-executor:
    sdd-invocation: forbidden
  sdd-stage-verifier:
    sdd-invocation: forbidden
  sdd-stage-integrator:
    sdd-invocation: forbidden
  reporter:
    sdd-invocation: forbidden
stage_seats:
  tasks:
    seats: [sdd-task-coordinator, sdd-task-executor, sdd-stage-verifier]
    max_parallel: 2
  implement:
    seats: [sdd-implement-coordinator, sdd-implement-executor, sdd-stage-verifier]
    max_parallel: 6
  review:
    seats: [sdd-review-coordinator, sdd-review-executor, sdd-stage-verifier]
    max_parallel: 2
members:
  - agent: sdd-task-coordinator
    role: task-coordinator
    lifecycle: temporary
  - agent: sdd-task-executor
    role: task-executor
    lifecycle: temporary
  - agent: sdd-implement-coordinator
    role: implement-coordinator
    lifecycle: temporary
  - agent: sdd-implement-executor
    role: implement-executor
    lifecycle: temporary
  - agent: sdd-review-coordinator
    role: review-coordinator
    lifecycle: temporary
  - agent: sdd-review-executor
    role: review-executor
    lifecycle: temporary
  - agent: sdd-stage-verifier
    role: stage-verifier
    lifecycle: temporary
  - agent: reporter
    role: reporter
    lifecycle: temporary
    reporting-territory:
      read: [".specify/state/091-auto-git-closeout.md", ".specify/specs/091-auto-git-closeout/test-evidence/**", ".specify/specs/091-auto-git-closeout/team/091-auto-git-closeout/runs/**"]
      write: [".specify/specs/091-auto-git-closeout/test-evidence/reporter-091-auto-git-closeout.live.log"]
    reporting-cadence: default
config:
  isolation: worktree
  agent_concurrency:
    requested: 24
    effective: 24
    reason: local native subagents, shared-tree isolation; ready packages recomputed per stage
  verifier_reserve: 1
  decomposition_slot_cap: 6
  checkpoint_policy:
    propose: true
    max_config_changes: 1
    ratification: standing
  coordinator_slot: roster-only
  summary:
    enabled: false
    reason: run-scoped
binding:
  owner: human
  owner_id: human
  origin: 091-auto-git-closeout
---

## Goal

Every retained write ends with one git close-out (commit -> merge -> push) derived from the model declared in
`.specify/workflow/git.md`; the goal definition at `.specify/specs/091-auto-git-closeout/goal/091-auto-git-closeout/goal.md`
is authoritative and this section is readability rendering only.

Success is judged by the goal's four criteria: the four workflow models reproduce their sequences in fixture
repositories; ask/absent policy presents and waits; push rejection or merge conflict stops at the first failure
without force-push or a second retry; artifact commands and unattended runs use the same close-out step.

## Static Structure

| Seat | SDD stage | Role | Type | Lifetime |
|------|-----------|------|------|----------|
| `sdd-task-coordinator` | tasks | coordinator | Worker | temporary |
| `sdd-task-executor` | tasks | executor | Worker | temporary |
| `sdd-implement-coordinator` | implement | coordinator | Worker | temporary |
| `sdd-implement-executor` | implement | executor | Worker | temporary |
| `sdd-review-coordinator` | review | coordinator | Worker | temporary |
| `sdd-review-executor` | review | executor | Worker | temporary |
| `sdd-stage-verifier` | tasks / implement / review | verifier | Worker | temporary |
| `reporter` | all stages (lifecycle-wide seat) | reporter | Meta | temporary |

Every seat resolves to a definition already shipped with the framework under `.specify/agents/templates/`; this
roster creates no new agent definitions.
