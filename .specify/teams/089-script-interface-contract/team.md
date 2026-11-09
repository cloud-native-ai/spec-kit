---
name: SDD Temporary Team 089
slug: 089-script-interface-contract
description: Run-scoped SDD team for Feature 089 — script interface contract, governance landings, checker engine, and backfill.
scope: spec
spec_dir: .specify/specs/089-script-interface-contract
lifecycle_state: active
goal: >-
  Deliver Feature 089 through the full SDD chain: every directly executable *.sh/*.py supports
  -h/--help and --version with zero side effects, unknown options fail non-zero, the rule lands in
  the framework constitution/instructions templates and this repo's constitution, and a deterministic
  checker reports zero violations.
goal_slug: script-interface-contract
territory:
  write:
    - .specify/specs/089-script-interface-contract/**
    - scripts/**
    - templates/**
    - skills/**
    - shared/**
    - tests/**
    - .specify/scripts/**
    - .specify/shared/**
    - .specify/skills/**
    - .specify/templates/**
  read:
    - "**"
  forbidden:
    - .specify/goal/**
    - .specify/teams/**
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
    max_parallel: 2
  plan:
    seats: [sdd-plan-coordinator, sdd-plan-executor, sdd-stage-verifier, sdd-stage-integrator]
    max_parallel: 4
  tasks:
    seats: [sdd-task-coordinator, sdd-task-executor, sdd-stage-verifier, sdd-stage-integrator]
    max_parallel: 4
  checklist:
    seats: [sdd-checklist-worker, sdd-stage-verifier]
    max_parallel: 2
  analyze:
    seats: [sdd-analysis-worker, sdd-stage-verifier]
    max_parallel: 4
  implement:
    seats: [sdd-implement-coordinator, sdd-implement-executor, sdd-stage-verifier, sdd-stage-integrator]
    max_parallel: 6
  review:
    seats: [sdd-review-coordinator, sdd-review-executor, sdd-stage-verifier]
    max_parallel: 4
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
  agent_concurrency: { requested: 24, effective: 6, reason: package-count }
  checkpoint_policy: { propose: true, max_config_changes: 1, ratification: standing }
  summary: { enabled: false, reason: run-scoped }
binding:
  owner: human
  owner_id: human
  origin: 089-script-interface-contract
---

## Goal

Deliver Feature 089 through the full SDD chain. The spec-local goal definition is
`goal/script-interface-contract/goal.md`; this section is readability rendering only.

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
| `sdd-stage-verifier` | all | Worker | temporary |
| `sdd-stage-integrator` | plan/tasks/implement | Worker | temporary |

## Dynamic Structure

Serial stage chain: requirements → clarify → plan → tasks → checklist → analyze → implement → review.
Each stage hands off file paths only; the next stage starts after the driver's U4 verification.
Concurrency is per-stage (`stage_seats`); the default requested value is 24 and the effective value is
recomputed at each stage entry from the ready package count.

## Self-Improvement Contract

- verifier: `sdd-stage-verifier` (never the executor of the object verified)
- threshold: stage U4 pass (sentinel + artifacts + discipline + wrap-up accounting)
- max_iterations: 3 per stage
- state spine: `.specify/state/089-script-interface-contract.md`
