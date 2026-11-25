---
name: Decision Governance Construction
slug: 107-decision-governance
description: Serial construction crew for Feature 107 — the AI Agent decision-governance contract (text/options, archive/audit, superagent→subagent transmission and implementation, M/B enforcement, migration), spec-side writeback only.
binding:
  owner: sdd-run
  owner_id: r20261125T134500Z-107a
  origin: 107-decision-governance
lifecycle_state: active
goal: >-
  Deliver spec 107 as one decision-governance contract: unambiguous decision text (full names; full resource location on
  possible same-name conflicts), closed option sets, archive/audit in existing carriers, intact superagent→subagent
  transmission with implementation receipts, and distinct emphases for human-interactive (readability) and AI-autonomous
  (rigor) decisions. The bound Anchor `.specify/anchoring/107-decision-governance/anchor.md` is authoritative.
anchor_slug: 107-decision-governance
territory:
  write:
    - .specify/specs/107-decision-governance/notes/**
    - .specify/specs/107-decision-governance/writeback/**
    - .specify/specs/107-decision-governance/test-evidence/**
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
    - .specify/specs/107-decision-governance/requirements.md
    - .specify/specs/107-decision-governance/tasks.md
    - .specify/specs/107-decision-governance/verification.md
    - .specify/specs/107-decision-governance/handoff.md
    - .specify/specs/107-decision-governance/plan.md
    - .specify/specs/107-decision-governance/data-model.md
    - .specify/specs/107-decision-governance/contracts/**
    - .specify/specs/107-decision-governance/quickstart.md
    - .specify/specs/107-decision-governance/research.md
    - .specify/specs/107-decision-governance/feature-ref.md
    - .specify/specs/107-decision-governance/checkpoints/**
    - .specify/anchoring/**
    - .specify/teams/**
    - .specify/state/**
    - .specify/features.md
    - .specify/features/107-decision-governance.md
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
      read: [".specify/state/decision-governance.md", ".specify/specs/107-decision-governance/test-evidence/**", ".specify/teams/107-decision-governance/runs/**"]
      write: [".specify/specs/107-decision-governance/test-evidence/reporter-107-decision-governance.live.log"]
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
handoff_ref: .specify/specs/107-decision-governance/handoff.md
---

## Goal

Deliver spec 107 through a serial construction chain: implementation in task order, independent verification of each bounded package, deterministic integration, and spec-side writeback. The bound Anchor at `.specify/anchoring/107-decision-governance/anchor.md` is authoritative; this section is readability only.

## Static Structure

| Seat | SDD stage | Role | Type | Lifetime |
|------|-----------|------|------|----------|
| `sdd-implement-coordinator` | implement | coordinator | Worker | temporary |
| `sdd-implement-executor` | implement | executor | Worker | temporary |
| `sdd-stage-verifier` | implement | verifier | Worker | temporary |
| `sdd-stage-integrator` | implement | integrator | Worker | temporary |
| `reporter` | all stages | reporter | Meta | temporary |

Every seat resolves to an existing template under `.specify/agents/templates/`.

## Dynamic Structure

Pattern: **serial** (quality-first). `implement → verify → integrate`; the reporter observes without gating. One writeback record per completed task at `.specify/specs/107-decision-governance/writeback/<T-NNN>.yaml`. The design face is read-only to the crew.

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports and Post-Run Critique.
- Improve: route through `improve-team`; preserve authority, maturity gates, budget, kill-switch and verifier independence.
- Verify: validate now and wait for a comparable later run.
