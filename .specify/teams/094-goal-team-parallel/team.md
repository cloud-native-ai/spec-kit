---
name: SDD Temporary Team 094
slug: 094-goal-team-parallel
description: Run-scoped SDD team for Feature 094 — goal/team × spec parallelism; default-concurrent stages (plan packages, implement packages up to 6, review 4 segments), worktree write isolation, deterministic integration.
scope: spec
spec_dir: .specify/specs/094-goal-team-parallel
lifecycle_state: active
goal: >-
  goal/team 与 spec(SDD) 成为平行执行线：goal/team 可在 /speckit.* 命令运行中创建并归档到 .specify/goal|teams；
  spec 与 goal+team 各自可设计/执行，复杂工作由 spec 设计、goal+team 执行；用 owner/lifecycle/write-scope
  绑定模型替代「临时/全局」。
goal_slug: 094-goal-team-parallel
territory:
  write:
    - .specify/specs/094-goal-team-parallel/**
    - .specify/state/094-goal-team-parallel.md
    - .specify/anchoring/**
    - .specify/teams/**
    - scripts/python/goal-utils.py
    - .specify/scripts/python/goal-utils.py
    - skills/internal/create-team/**
    - .specify/skills/internal/create-team/**
    - skills/internal/run-team/**
    - .specify/skills/internal/run-team/**
    - skills/external/sdd-loop-driver/**
    - .specify/skills/sdd-loop-driver/**
    - templates/commands/**
    - .specify/templates/commands/**
    - shared/definitions/framework-map.md
    - .specify/shared/definitions/framework-map.md
    - shared/guidelines/directory-governance.md
    - .specify/shared/guidelines/directory-governance.md
    - shared/definitions/goal-definitions.md
    - .specify/shared/definitions/goal-definitions.md
    - tests/contract/**
    - .specify/memory/features.md
    - .specify/memory/features/094.md
  read:
    - "**"
  forbidden:
    - .specify/specs/085-sdd-temporary-goal-team/**
    - .specify/specs/086-efficient-test-execution/**
    - .specify/specs/087-arch-diagram-docs/**
    - .specify/specs/088-speckit-visualization/**
    - .specify/specs/089-script-interface-contract/**
    - .specify/specs/090-re-anchoring/**
    - .specify/specs/091-auto-git-closeout/**
  non_path:
    - { type: runtime, target: "host agent concurrency and rendered agent surfaces (specify render-agents output)" }
pattern: parallel
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
    max_parallel: 4
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
      read: [".specify/state/094-goal-team-parallel.md", ".specify/specs/094-goal-team-parallel/test-evidence/**", ".specify/specs/094-goal-team-parallel/team/094-goal-team-parallel/runs/**"]
      write: [".specify/specs/094-goal-team-parallel/test-evidence/reporter-094-goal-team-parallel.live.log"]
    reporting-cadence: default
config:
  isolation: worktree
  agent_concurrency:
    requested: 24
    effective: 24
    reason: local native subagents, worktree write isolation; ready packages recomputed per stage; implement ~10 tasks/package up to 6 concurrent
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
  origin: 094-goal-team-parallel
---

## Goal

goal/team 与 spec(SDD) 平行；.specify/goal|teams 统一归档；复杂工作由 spec 设计、goal+team 执行。目标定义在
`.specify/archive/goal-team/trees/094-goal-team-parallel/goal/094-goal-team-parallel/goal.md`，本节只作可读呈现。

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
| `reporter` | all stages | reporter | Meta | temporary |
