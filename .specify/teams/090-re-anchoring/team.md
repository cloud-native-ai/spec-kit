---
name: SDD Temporary Team 090
slug: 090-re-anchoring
description: Run-scoped SDD team for Feature 090 — Re-Anchoring; serial stage chain over tasks / implement / review with per-stage coordinator + executor seats, one independent verifier reserve per stage, and a roster-only creation (execution belongs to the SDD driver).
scope: spec
spec_dir: .specify/specs/090-re-anchoring
lifecycle_state: active
goal: >-
  Deliver the remaining stages of Feature 090 through a spec-local temporary team: the rules are
  re-loaded and evaluated at every core step in T0/T1/T2 tiers (rule-first five questions, three-value
  verdict), the five rule faces exist and cross-reference by pointer, and the count pins and their
  guards move together — measured by the guard tests the spec names, not by the presence of definitions.
goal_slug: 090-re-anchoring
territory:
  write:
    - .specify/specs/090-re-anchoring/**
    - .specify/state/090-re-anchoring.md
    - shared/definitions/re-anchoring-definitions.md
    - shared/definitions/agent-definitions.md
    - templates/constitution-template.md
    - templates/instructions-template.md
    - skills/internal/manage-constitution/SKILL.md
    - skills/external/sdd-loop-driver/SKILL.md
    - skills/external/sdd-loop-driver/references/checkpoint-protocol.md
    - .specify/shared/definitions/re-anchoring-definitions.md
    - .specify/shared/definitions/agent-definitions.md
    - .specify/templates/constitution-template.md
    - .specify/templates/instructions-template.md
    - .specify/skills/internal/manage-constitution/SKILL.md
    - .specify/skills/sdd-loop-driver/SKILL.md
    - .specify/skills/sdd-loop-driver/references/checkpoint-protocol.md
    - .specify/memory/constitution.md
    - .specify/instructions.md
    - tests/contract/test_reanchoring_contract.py
    - tests/contract/test_sdd_loop_driver_reanchor.py
    - tests/contract/test_constitution_double_landing.py
    - tests/contract/test_fast_fail_discipline.py
    - scripts/bash/generate-instructions.sh
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
    max_parallel: 2
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
      read: [".specify/state/090-re-anchoring.md", ".specify/specs/090-re-anchoring/test-evidence/**", ".specify/specs/090-re-anchoring/team/090-re-anchoring/runs/**"]
      write: [".specify/specs/090-re-anchoring/test-evidence/reporter-090-re-anchoring.live.log"]
    reporting-cadence: default
config:
  isolation: shared-tree
  agent_concurrency:
    requested: 24
    effective: 24
    reason: local native subagents, shared-tree isolation; ready packages recomputed per stage
  verifier_reserve: 1
  decomposition_slot_cap: 2
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
  origin: 090-re-anchoring
---

## Goal

Deliver the remaining stages of Feature 090 through a spec-local temporary team. The spec-local goal definition is
`.specify/archive/goal-team/trees/090-re-anchoring/goal/090-re-anchoring/goal.md`; this section is readability rendering only, and the
definition is authoritative.

Success is judged by the goal's four criteria: the five rule faces exist and cross-reference (SC-001), the five
questions are rule-first in the checkpoint protocol and pinned by a test (SC-002), the count pins and their guards
move together (SC-003), and the T0/T1/T2 tiers agree between the owner document and the checkpoint protocol
(SC-004) — each measured by the guard tests this spec names, never by the presence of the definitions.

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

Every seat resolves to a definition already shipped with the framework under `.specify/agents/templates/` (mirror
`agents/`); this roster is created with **zero new agent definitions** — no seat needed instantiation from a stage
frame, so no `team-scope` seat instance is produced by this creation.

**Type by operating object** (never by stage): the six stage seats and the verifier operate on business artifacts
(spec files, framework sources, tests) → `Worker`. The reporter operates on the run's observable state and writes
only its own stream artifact → `Meta`.

**Coordinator status**: the coordinator coordination duty is carried by the **orchestrating SDD driver session**,
which already selects the stage, the slice and the next step (`.specify/shared/workflow/execution-topology.md` puts
team seats on the execution side, with the driver owning the loop). The coordinator seats remain in the roster
because 085 model §3.6 requires the tasks / implement / review stages to declare their own coordinator + executor
pair; they are invoked only if a stage's package count exceeds what the driver will partition in one turn.

## Dynamic Structure

Pattern: **serial** (质量优先) — a DAG over the three remaining canonical SDD stages; no cycles; each stage's
output feeds the next by **file-path-only handoff**, and a per-handoff verification guards every step.

```
tasks  ──(U4)──►  implement  ──(U4)──►  review
  │                  │                   │
  └────────── verifier (independent, one reserve per stage) ──────────┘
```

- **Stage loop (per stage)**: coordinator/driver partitions the stage input into bounded work packages → executors
  run the packages, writing only inside the territory above → `sdd-stage-verifier` independently verifies by
  re-running the named programmatic gates → the stage closes with its checkpoint (artifact verification, goal degree,
  at most one configuration proposal, next-stage concurrency/roster).
- **In-stage parallelism**: `stage_seats.<stage>.max_parallel` is the ceiling for concurrent seats inside one stage;
  it is bounded by `decomposition_slot_cap: 2` and never exceeds the run's effective concurrency (24). All write
  packages share one tree (`isolation: shared-tree`), so concurrent executors MUST hold disjoint write paths.
- **Verifier reserve**: exactly **one** verifier is reserved per stage and is never the executor of the object it
  verifies (context isolation: every invocation is a fresh subagent).
- **Reporter seat**: emits one attributed status line per the cadence owned by
  `.specify/shared/guidelines/progress-reporting.md` (the literal `default`), writing only
  `test-evidence/reporter-090-re-anchoring.live.log`; it observes the state spine and stage evidence and mutates
  nothing else.
- **Loop discipline**: the outer chain is the SDD driver's; this team contributes its structure and its concurrency
  settings, and the driver's own stage loop (hard requirements, checkpoints, direction audit) stays in force.
- **Run reports**: per stage, at `<team-root>/<slug>/runs/<UTC-timestamp>-report.md` with the mandatory
  `## Verification` section and the `## Nested SDD Runs` section.

Ownership of the run report: the SDD driver session is the sole writer of tracked artifacts (it is the orchestrating
session for this spec-local team), so run reports are written by the driver under `runs/` when a stage closes.

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports under `runs/` and the per-stage checkpoints under `.specify/specs/090-re-anchoring/checkpoints/`.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team` (the checkpoint's single configuration proposal is the entry, cap one change per stage).
- Boundary: preserve team authority, the verifier's independence, the stage sequence, and the sentinel literals; this team never writes `.specify/teams/**` or `.specify/goal/**`.
- Verify: validate now (`skills/internal/create-team/scripts/validate-roster.py`) and wait for a comparable later run before claiming improvement.
