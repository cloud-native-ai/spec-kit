---
name: 088 Reporting Dogfood
slug: 088-reporting-dogfood
description: Spec-local dogfood team proving the reporting obligation end to end — a real >90 s verification run with a reporter seat emitting attributed status lines on cadence.
scope: spec
spec_dir: .specify/specs/088-speckit-visualization
lifecycle_state: archived
goal: >-
  Prove the reporting obligation end to end: a real >90 s verification task runs while a
  reporter seat emits attributed status lines on the 30-second long-run cadence, and the
  run record names the carrier.
territory:
  write:
    - test-evidence/dogfood-worker-*
    - test-evidence/dogfood-reporter-*
  read:
    - "**"
pattern: parallel
created: 2026-11-06
updated: 2026-11-06
seats:
  reporter:
    sdd-invocation: forbidden
members:
  - agent: framework-engineer
    role: worker
    lifecycle: persistent
    territory: ["test-evidence/dogfood-worker-*"]
  - agent: reporter
    role: reporter
    lifecycle: temporary
    reporting-territory:
      read: [".specify/specs/088-speckit-visualization/verification.md", "test-evidence/dogfood-worker-*"]
      write: ["test-evidence/dogfood-reporter-*"]
    reporting-cadence: 30s
config:
  agent_concurrency:
    requested: 2
    effective: 2
    reason: two-member dogfood run
binding:
  owner: human
  owner_id: human
  origin: 088-speckit-visualization
---

## Goal

Prove the reporting obligation end to end: a real >90 s verification task runs while a
reporter seat emits attributed status lines on the 30-second long-run cadence, and the
run record names the carrier.

## Static Structure

| Agent | Role | Stage | Type | Territory | Lifecycle |
|-------|------|-------|------|-----------|-----------|
| framework-engineer | worker | executor | Worker | `test-evidence/dogfood-worker-*` | persistent |
| reporter | reporter | all-stage seat | Meta | write `test-evidence/dogfood-reporter-*` (read-only elsewhere) | temporary |

## Dynamic Structure

Pattern: **parallel** — two lanes dispatched concurrently with disjoint write territories.

- Lane 1 (worker): `framework-engineer` runs the real >90 s verification task, writing only under `test-evidence/dogfood-worker-*`.
- Lane 2 (reporter): `reporter` emits one attributed status line per 30-second cadence interval into its single stream artifact under `test-evidence/dogfood-reporter-*`, observing the run's state surfaces (read list above); it never mutates the worker's territory or any canonical artifact.

Execution flow: dispatch both lanes → worker completes the verification task → reporter's stream artifact and the run record are checked together — the run record names the carrier, and the status lines carry attribution, position, delta, remainder and blocker state.

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports and Post-Run Critique.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team`.
- Boundary: preserve team authority, maturity gates, budget, kill-switch, and verifier independence.
- Verify: validate now and wait for a comparable later run before claiming improvement.
