---
name: Runtime Store Layout Construction
slug: 105-runtime-store-layout
description: Serial construction crew for Feature 024 slice 105 — migrates runtime stores out of .specify/memory/ with a tested /speckit.migrate transition, independent verification, and spec-side writeback only.
binding:
  owner: sdd-run
  owner_id: r20261125T022857Z-06dd
  origin: 105-runtime-store-layout
lifecycle_state: active
goal: >-
  Deliver spec 105 as a safe, complete runtime-store layout migration: retire the .specify/memory/ catch-all,
  move every runtime store to its named top-level home, preserve temporary memory and super-agent to sub-agent
  context injection, and make every backward-incompatible change migrate or refuse deterministically through
  /speckit.migrate. The bound Anchor `.specify/anchoring/105-runtime-store-layout/anchor.md` is authoritative.
anchor_slug: 105-runtime-store-layout
territory:
  write:
    - .specify/specs/105-runtime-store-layout/notes/**
    - .specify/specs/105-runtime-store-layout/writeback/**
    - .specify/specs/105-runtime-store-layout/test-evidence/**
    - .specify/session/**
    - .specify/knowledge/**
    - .specify/feedback/**
    - .specify/evidence/**
    - .specify/exec-quant/**
    - .specify/trigger/**
    - .specify/retention/**
    - .specify/renumber/**
    - .specify/sanitize/**
    - .specify/housekeeping/**
    - .specify/coaching/**
    - .specify/todo/**
    - .specify/tools/**
    - .specify/migrate/**
    - .specify/memory/**
    - seed/**
    - memory/**
    - shared/**
    - skills/**
    - scripts/**
    - src/specify_cli/**
    - templates/**
    - agents/**
    - tests/**
    - docs/concepts/**
    - docs/reference/**
    - docs/tutorials/**
    - docs/tasks/**
    - docs/contribute/**
    - .specify/shared/**
    - .specify/scripts/**
    - .specify/templates/**
    - .specify/agents/templates/**
    - .specify/skills/**
    - .github/prompts/**
    - .claude/commands/**
    - .qoder/commands/**
    - .opencode/command/**
    - .specify/instructions.md
    - .specify/glossary.md
    - .specify/.gitignore
    - pyproject.toml
  read:
    - "**"
  forbidden:
    - .specify/specs/105-runtime-store-layout/requirements.md
    - .specify/specs/105-runtime-store-layout/tasks.md
    - .specify/specs/105-runtime-store-layout/verification.md
    - .specify/specs/105-runtime-store-layout/handoff.md
    - .specify/specs/105-runtime-store-layout/plan.md
    - .specify/specs/105-runtime-store-layout/data-model.md
    - .specify/specs/105-runtime-store-layout/contracts/**
    - .specify/specs/105-runtime-store-layout/quickstart.md
    - .specify/specs/105-runtime-store-layout/research.md
    - .specify/specs/105-runtime-store-layout/feature-ref.md
    - .specify/specs/105-runtime-store-layout/checkpoints/**
    - .specify/anchoring/**
    - .specify/teams/**
    - .specify/state/**
    - .specify/features.md
    - .specify/features/024-specification-workspace-versioning.md
    - docs/reference/history/**
    - docs/decisions/**
    - docs/archive/**
  non_path:
    - { type: runtime, target: "host agent concurrency and rendered agent surfaces (specify render-agents output)" }
pattern: serial
created: 2026-11-25
updated: 2026-11-25
seats:
  sdd-implement-coordinator:
    sdd-invocation: forbidden
  sdd-implement-executor:
    sdd-invocation: forbidden
  sdd-stage-verifier:
    sdd-invocation: forbidden
  sdd-stage-integrator:
    sdd-invocation: forbidden
  reporter:
    sdd-invocation: forbidden
stage_seats:
  implement:
    seats: [sdd-implement-coordinator, sdd-implement-executor, sdd-stage-verifier, sdd-stage-integrator]
    max_parallel: 1
members:
  - agent: sdd-implement-coordinator
    role: implement-coordinator
    class: serial-only
    lifecycle: temporary
  - agent: sdd-implement-executor
    role: implement-executor
    class: serial-only
    lifecycle: temporary
  - agent: sdd-stage-verifier
    role: stage-verifier
    class: serial-only
    lifecycle: temporary
  - agent: sdd-stage-integrator
    role: stage-integrator
    class: serial-only
    lifecycle: temporary
  - agent: reporter
    role: reporter
    class: serial-only
    lifecycle: temporary
    reporting-territory:
      read: [".specify/state/105-runtime-store-layout.md", ".specify/specs/105-runtime-store-layout/test-evidence/**", ".specify/teams/105-runtime-store-layout/runs/**"]
      write: [".specify/specs/105-runtime-store-layout/test-evidence/reporter-105-runtime-store-layout.live.log"]
    reporting-cadence: default
config:
  isolation: shared-tree
  agent_concurrency:
    requested: 1
    effective: 1
    reason: serial quality-first construction; one active stage at a time
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
handoff_ref: .specify/specs/105-runtime-store-layout/handoff.md
---

## Goal

Deliver spec 105 through a serial construction chain: implementation in task order, independent verification of
each bounded package, deterministic integration, and spec-side writeback. The bound Anchor at
`.specify/anchoring/105-runtime-store-layout/anchor.md` is authoritative; this section is readability only.

## Static Structure

| Seat | SDD stage | Role | Type | Lifetime |
|------|-----------|------|------|----------|
| `sdd-implement-coordinator` | implement | coordinator | Worker | temporary |
| `sdd-implement-executor` | implement | executor | Worker | temporary |
| `sdd-stage-verifier` | implement | verifier | Worker | temporary |
| `sdd-stage-integrator` | implement | integrator | Worker | temporary |
| `reporter` | all stages (lifecycle-wide seat) | reporter | Meta | temporary |

Every seat resolves to an existing template under `.specify/agents/templates/`; this roster creates no new agent definitions.

## Dynamic Structure

Pattern: **serial** (quality-first). Construction stages, each gated by its predecessor:

1. `implement` — coordinator partitions the 43 task rows into bounded packages; executor performs them in task order inside the declared territory. No task-table writes.
2. `verify` — `sdd-stage-verifier` checks every package's artifacts, tests and writeback records with fresh context; a package verdict never replaces the stage U4.
3. `integrate` — `sdd-stage-integrator` deterministically applies the verified packages and makes the single construction commit.
4. `report` — the reporter seat records cadence reports; the run report is written after every run.

DAG: `implement → verify → integrate`; the reporter observes lifecycles without gating. Handoffs are path-only; the crew writes
one `.specify/specs/105-runtime-store-layout/writeback/<T-NNN>.yaml` per completed task. The design face
(`requirements.md`, `plan.md`, `tasks.md`, `verification.md`, `handoff.md`, contracts and checkpoints) is read-only to the crew.

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports and Post-Run Critique.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team`.
- Boundary: preserve team authority, maturity gates, budget, kill-switch, and verifier independence.
- Verify: validate now and wait for a comparable later run before claiming improvement.