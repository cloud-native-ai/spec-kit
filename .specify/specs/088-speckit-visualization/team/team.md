---
name: SDD Temporary Team 088
slug: 088-speckit-visualization
description: Run-scoped SDD team for Feature 088 — framework visualization, stage-specific agents, explicit concurrency, reporter obligations, and stage checkpoints.
scope: spec
spec_dir: .specify/specs/088-speckit-visualization
lifecycle_state: active
goal: >-
  Deliver Feature 088 through the full SDD chain: make the current state of concurrent and
  asynchronous Speckit flows continuously visible to the user, with a single reporting-obligation
  owner, reporter-seat duties for teams, supervision reporting for master-slave flows, a bounded
  current-state digest entry, and truthful traceable progress at a declared cadence.
goal_slug: 088-speckit-visualization
territory:
  write:
    - .specify/specs/088-speckit-visualization/**
    - shared/**
    - agents/**
    - skills/**
    - scripts/**
    - templates/**
    - tests/**
    - .claude/commands/**
    - .github/prompts/**
    - .opencode/command/**
    - .qoder/commands/**
  read:
    - "**"
  forbidden:
    - .specify/goal/**
    - .specify/teams/**
  non_path:
    - { type: runtime, target: "host agent concurrency and rendered agent surfaces" }
pattern: serial
created: 2026-11-06
updated: 2026-11-06
seats:
  sdd-requirement-analyzer:
    sdd-invocation: forbidden
  sdd-clarify-analyzer:
    sdd-invocation: forbidden
  sdd-plan-coordinator:
    sdd-invocation: forbidden
  sdd-plan-executor:
    sdd-invocation: forbidden
  sdd-task-coordinator:
    sdd-invocation: forbidden
  sdd-task-executor:
    sdd-invocation: forbidden
  sdd-checklist-worker:
    sdd-invocation: forbidden
  sdd-analysis-worker:
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
stage_seats:
  requirements:
    seats: [sdd-requirement-analyzer, sdd-stage-verifier]
    max_parallel: 1
  clarify:
    seats: [sdd-clarify-analyzer, sdd-stage-verifier]
    max_parallel: 1
  plan:
    seats: [sdd-plan-coordinator, sdd-plan-executor, sdd-stage-verifier, sdd-stage-integrator]
    max_parallel: 2
  tasks:
    seats: [sdd-task-coordinator, sdd-task-executor, sdd-stage-verifier, sdd-stage-integrator]
    max_parallel: 2
  checklist:
    seats: [sdd-checklist-worker, sdd-stage-verifier]
    max_parallel: 1
  analyze:
    seats: [sdd-analysis-worker, sdd-stage-verifier]
    max_parallel: 2
  implement:
    seats: [sdd-implement-coordinator, sdd-implement-executor, sdd-stage-verifier, sdd-stage-integrator]
    max_parallel: 2
  review:
    seats: [sdd-review-coordinator, sdd-review-executor, sdd-stage-verifier]
    max_parallel: 2
members:
  - agent: sdd-requirement-analyzer
    role: requirements-analyzer
    lifecycle: temporary
  - agent: sdd-clarify-analyzer
    role: clarify-analyzer
    lifecycle: temporary
  - agent: sdd-plan-coordinator
    role: plan-coordinator
    lifecycle: temporary
  - agent: sdd-plan-executor
    role: plan-executor
    lifecycle: temporary
  - agent: sdd-task-coordinator
    role: task-coordinator
    lifecycle: temporary
  - agent: sdd-task-executor
    role: task-executor
    lifecycle: temporary
  - agent: sdd-checklist-worker
    role: checklist-worker
    lifecycle: temporary
  - agent: sdd-analysis-worker
    role: analysis-worker
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
  - agent: sdd-stage-integrator
    role: stage-integrator
    lifecycle: temporary
config:
  isolation: shared-tree
  agent_concurrency: { requested: 24, effective: 2, reason: "decomposition slot cap 2; write-alone serializes writes; verifier reserve 1" }
  checkpoint_policy: { propose: true, max_config_changes: 1, ratification: standing }
  summary: { enabled: false, reason: run-scoped }
---

## Goal

Deliver Feature 088 through the full SDD chain: every concurrent or asynchronous Speckit flow reports its
current state to the user at a declared cadence, team runs carry a reporter seat obligation, supervising
master-slave flows report sub-flow state, and reporting stays truthful and traceable. Success is measured by
the delivered framework surfaces and their contract tests, not by the presence of the definitions alone.

## Static Structure

| Seat | SDD stage | Type | Lifetime |
|------|-----------|------|----------|
| `sdd-requirement-analyzer` | requirements | Worker | temporary |
| `sdd-clarify-analyzer` | clarify | Worker | temporary |
| `sdd-plan-coordinator` | plan | Worker | temporary |
| `sdd-plan-executor` | plan | Worker | temporary |
| `sdd-task-coordinator` | tasks | Worker | temporary |
| `sdd-task-executor` | tasks | Worker | temporary |
| `sdd-checklist-worker` | checklist | Worker | temporary |
| `sdd-analysis-worker` | analyze | Worker | temporary |
| `sdd-implement-coordinator` | implement | Worker | temporary |
| `sdd-implement-executor` | implement | Worker | temporary |
| `sdd-review-coordinator` | review | Worker | temporary |
| `sdd-review-executor` | review | Worker | temporary |
| `sdd-stage-verifier` | any | Evaluator | temporary |
| `sdd-stage-integrator` | any | Worker | temporary |

## Dynamic Structure

- **Outer chain**: serial across the eight canonical SDD stages; each stage closes before the next starts.
- **Inner stage**: the stage's `stage_seats` bounds the ready work packages; read-only packages may overlap up to `max_parallel` (2), while write packages are dispatched alone in the shared tree.
- **Checkpoints**: after every stage U4, the four-part checkpoint records artifact verification, goal degree, at most one configuration proposal, and the next stage's concurrency/roster decision.

## Self-Improvement Contract

- **Subject**: `team:088-speckit-visualization` (this temporary team).
- **Runs-lane evidence**: `team/runs/*-report.md` plus the checkpoint files and the wp ledger.
- **Improver route**: `improve-team` for roster/pattern/config edits; `/speckit.goal modify --scope spec` for goal content; no automatic mutation.
- **Attempt cap**: one configuration change per checkpoint; a regression triggers rollback at the next checkpoint.
