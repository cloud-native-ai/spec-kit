---
name: Team View Degradation Construction
slug: 108-team-view-degradation
description: Serial construction crew for Feature 027 slice 108 — honest /speckit.team view presentation under real degraded team definitions; spec-side writeback only.
binding:
  owner: sdd-run
  owner_id: r20261126T071500Z-108a
  origin: 108-team-view-degradation
lifecycle_state: active
goal: >-
  Deliver spec 108: harden the single team-view engine for real-world workspaces — parseable-timestamp report
  recognition (incl. 4-hex suffixes), latest-by-parsed-time, named residue, explicit missing artifacts and
  binding/goal degradation guidance, roster-matrix anomalies, closed degradation reasons and exit codes, with
  healthy output preserved byte-for-byte. The bound Anchor `.specify/anchoring/108-team-view-degradation/anchor.md`
  is authoritative.
anchor_slug: 108-team-view-degradation
territory:
  write:
    - .specify/specs/108-team-view-degradation/notes/**
    - .specify/specs/108-team-view-degradation/writeback/**
    - .specify/specs/108-team-view-degradation/test-evidence/**
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
    - seed/**
    - shared/**
    - skills/**
    - scripts/**
    - src/specify_cli/**
    - templates/**
    - agents/**
    - tests/**
    - docs/reference/**
    - docs/concepts/**
    - docs/tutorials/**
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
    - .specify/specs/108-team-view-degradation/requirements.md
    - .specify/specs/108-team-view-degradation/tasks.md
    - .specify/specs/108-team-view-degradation/verification.md
    - .specify/specs/108-team-view-degradation/handoff.md
    - .specify/specs/108-team-view-degradation/plan.md
    - .specify/specs/108-team-view-degradation/data-model.md
    - .specify/specs/108-team-view-degradation/contracts/**
    - .specify/specs/108-team-view-degradation/quickstart.md
    - .specify/specs/108-team-view-degradation/research.md
    - .specify/specs/108-team-view-degradation/feature-ref.md
    - .specify/specs/108-team-view-degradation/checkpoints/**
    - .specify/anchoring/**
    - .specify/teams/**
    - .specify/state/**
    - .specify/features.md
    - .specify/features/027-team-management.md
    - docs/reference/history/**
    - docs/decisions/**
    - docs/archive/**
  non_path:
    - { type: runtime, target: "host agent concurrency and rendered agent surfaces (specify render-agents output)" }
pattern: serial
created: 2026-11-26
updated: 2026-11-26
seats:
  sdd-implement-coordinator: { sdd-invocation: forbidden }
  sdd-implement-executor: { sdd-invocation: forbidden }
  sdd-stage-verifier: { sdd-invocation: forbidden }
  sdd-stage-integrator: { sdd-invocation: forbidden }
  reporter: { sdd-invocation: forbidden }
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
      read: [".specify/state/team-view-degradation.md", ".specify/specs/108-team-view-degradation/test-evidence/**", ".specify/teams/108-team-view-degradation/runs/**"]
      write: [".specify/specs/108-team-view-degradation/test-evidence/reporter-108-team-view-degradation.live.log"]
    reporting-cadence: default
config:
  isolation: shared-tree
  agent_concurrency: { requested: 1, effective: 1, reason: serial quality-first construction; one active stage at a time }
  verifier_reserve: 1
  decomposition_slot_cap: 6
  checkpoint_policy: { propose: true, max_config_changes: 1, ratification: standing }
  coordinator_slot: roster-only
  summary: { enabled: false, reason: run-scoped }
handoff_ref: .specify/specs/108-team-view-degradation/handoff.md
---

## Goal
Deliver spec 108 through a serial construction chain. The bound Anchor is authoritative; this section is readability only.

## Static Structure
| Seat | SDD stage | Role | Type | Lifetime |
|------|-----------|------|------|----------|
| `sdd-implement-coordinator` | implement | coordinator | Worker | temporary |
| `sdd-implement-executor` | implement | executor | Worker | temporary |
| `sdd-stage-verifier` | implement | verifier | Worker | temporary |
| `sdd-stage-integrator` | implement | integrator | Worker | temporary |
| `reporter` | all stages | reporter | Meta | temporary |

## Dynamic Structure
Pattern: serial. `implement → verify → integrate`; one writeback record per completed task at `.specify/specs/108-team-view-degradation/writeback/<T-NNN>.yaml`. The design face is read-only to the crew.

## Self-Improvement Contract
Subject: this team definition. Observe: run reports. Improve: through `improve-team`. Preserve authority, budget, verifier independence.
