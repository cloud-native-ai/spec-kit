---
name: SDD Temporary Team 092
slug: 092-non-disposable
description: Run-scoped SDD team for Feature 092 — Non-Disposable; serial stage chain over tasks / implement / review with per-stage coordinator + executor seats, one independent verifier reserve, a reporter seat, and the checkpoint-03 concurrency decision (requested 24 / effective 24, implement ceiling 8).
scope: spec
spec_dir: .specify/specs/092-non-disposable
lifecycle_state: active
goal: >-
  Deliver Feature 092 Non-Disposable through the remaining SDD stages: a review surface of exactly the ten
  .specify/ historical roots is decided by a read-only deterministic engine, every expired / useless / deferred
  entry must land in one of the four closed dispositions (archive / supersede / correct / explicit exempt with an
  expiry), /speckit.history becomes the four-segment review -> design -> user confirmation -> execute shape with a
  zero-write review and design segment, and the A–H corpus of notes/input-review-080-090.md is reproduced by the
  mechanism and driven to zero for 档 I — measured by the named gates and the landed test-evidence/, never by the
  presence of the definitions.
goal_slug: 092-non-disposable
territory:
  write:
    # the spec's own artifacts: tasks / plan / evidence / checkpoints / team runs
    - .specify/specs/092-non-disposable/**
    # the line state spine (driver-owned)
    - .specify/state/092-non-disposable.md
    # P1 — owner page, declaration fact, framework-map registration row
    - shared/definitions/non-disposable-definitions.md
    - shared/declarations/facts/non-disposable-review-surface.yaml
    - shared/definitions/framework-map.md
    # P1 — canonical registries (single-owner files, edited by the driver only)
    - .specify/memory/glossary.md
    - .specify/memory/features.md
    - .specify/memory/features/092.md
    - .specify/memory/register.md
    # P2 — the deterministic engine (framework source; the .specify/scripts mirror is generated)
    - scripts/python/non-disposable-check.py
    # P3 — the history seam
    - skills/internal/manage-history/SKILL.md
    - templates/commands/history.md
    # P4 — the three pointer faces (AGENTS.md is a symlink to .specify/instructions.md and flows)
    - templates/instructions-template.md
    - .specify/instructions.md
    # P5 — the contract guard and the one allowance entry
    - tests/contract/test_non_disposable_contract.py
    - tests/contract/test_expression_compatibility.py
  read:
    - "**"
  forbidden:
    # 092 owns no global team or goal definition; the spec-local goal is engine-rendered only
    - .specify/teams/**
    - .specify/goal/**
    # other features' bodies are NOT rewritten wholesale here; two narrow write faces are carved out below
    # (FR-056 / D-8): P6's 档 I record-completion repairs, and P7's one handoff marker per receiving body.
    # Everything not named in the carve-out stays forbidden, including 档 II bodies' own prose.
    - .specify/specs/081-*/**
    - .specify/specs/082-*/**
    - .specify/specs/083-*/**
    - .specify/specs/084-*/**
    - .specify/specs/085-sdd-temporary-goal-team/**
    - .specify/specs/086-efficient-test-execution/**
    - .specify/specs/087-arch-diagram-docs/**
    - .specify/specs/088-speckit-visualization/**
    - .specify/specs/089-script-interface-contract/**
    - .specify/specs/090-re-anchoring/**
    - .specify/specs/067-*/**
    - .specify/specs/069*/**   # the dated bodies F1/F3 name
    - .specify/specs/077-*/**
    - .specify/specs/079-*/**
    - .specify/specs/080-*/**
  # Handoff boundary (C-805): the two write faces carved out of `forbidden` above. P6 (档 I repair) may
  # complete a RECORD in a foreign body — add a missing machine-block field, a `**Path**:` marker, a tier
  # column — never redesign the body and never rewrite a 档 II body's prose. P7 (档 II detection) may land
  # exactly ONE marker line per receiving body, in the form C-805 fixes, at the defect's location. Which
  # surface lands the marker (P7 cross-line write or the receiving body's own line) is a recorded decision,
  # not a correction.
  write_carve_outs:
    - pkg: P6
      paths: [.specify/specs/080-*/, .specify/specs/084-*/, .specify/specs/085-*/, .specify/specs/086-*/, .specify/specs/087-*/, .specify/specs/088-*/, .specify/specs/089-*/, .specify/specs/090-*/, .specify/memory/features.md]
      scope: record completion only (missing field, marker, pointer) — no redesign, no prose rewrite
    - pkg: P7
      paths: [.specify/specs/081-*/, .specify/specs/082-*/, .specify/specs/083-*/, .specify/specs/084-*/, .specify/specs/085-*/, .specify/specs/086-*/, .specify/specs/087-*/, .specify/specs/088-*/, .specify/specs/089-*/, .specify/specs/090-*/, .specify/memory/features.md]
      scope: one handoff marker line per receiving body (C-805) — nothing else
  non_path:
    - { type: runtime, target: "host agent concurrency and the rendered agent registration surface (specify render-agents output)" }
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
    seats: [sdd-task-coordinator, sdd-task-executor, sdd-stage-verifier, sdd-stage-integrator, reporter]
    max_parallel: 4
  implement:
    seats: [sdd-implement-coordinator, sdd-implement-executor, sdd-stage-verifier, sdd-stage-integrator, reporter]
    max_parallel: 8
  review:
    seats: [sdd-review-coordinator, sdd-review-executor, sdd-stage-verifier, sdd-stage-integrator, reporter]
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
  - agent: sdd-stage-integrator
    role: stage-integrator
    lifecycle: temporary
  - agent: reporter
    role: reporter
    lifecycle: temporary
    reporting-territory:
      read: [".specify/state/092-non-disposable.md", ".specify/specs/092-non-disposable/test-evidence/**", ".specify/specs/092-non-disposable/checkpoints/**", ".specify/specs/092-non-disposable/team/092-non-disposable/runs/**"]
      write: [".specify/specs/092-non-disposable/test-evidence/reporter-092-non-disposable.live.log"]
    reporting-cadence: default
config:
  isolation: shared-tree
  agent_concurrency:
    requested: 24
    effective: 24
    reason: >-
      local native subagents, shared-tree isolation; the user explicitly requires a team of large-concurrency
      subagents. Requested and effective both read the state spine's agent_concurrency_requested /
      agent_concurrency_effective (FR-050), and every stage's max_parallel is the existing declaration's
      per-stage minimum, not a second ceiling constant.
  stage_max_parallel:
    tasks: 4
    implement: 8
    review: 4
  verifier_reserve: 1
  decomposition_slot_cap: 8
  checkpoint_policy:
    propose: true
    max_config_changes: 1
    ratification: standing
  coordinator_slot: roster-only
  stage_order: [tasks, implement, review]
  package_plan: P1 -> P2 -> P3 -> P4 -> P5 -> P6 with P7 concurrent -> P8
  summary:
    enabled: false
    reason: run-scoped
---

## Goal

Deliver the remaining stages of Feature 092 (Non-Disposable) through a spec-local temporary team. The goal
definition is `.specify/specs/092-non-disposable/goal/092-non-disposable/goal.md`; this section is readability
rendering only, and that definition is authoritative. The goal carries **no `## Targets` section**, so this
roster declares **no `focus_target`** — there is no open Target to bind.

Success is judged by the goal's three criteria: the mechanism reproduces the A–H detections on the corpus tree
(SC-001 / SC-005…SC-010), every expired-or-deferred entry lands in one of the four closed dispositions with a
decidable expiry (SC-003), and the repair lane runs only after user confirmation and leaves per-entry
four-segment evidence (SC-004 / SC-010 / SC-020) — each measured by the named gates and the landed
`test-evidence/`, never by the presence of the definitions.

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
| `sdd-stage-integrator` | tasks / implement / review | integrator | Worker | temporary |
| `reporter` | all stages (lifecycle-wide seat) | reporter | Meta | temporary |

Every seat resolves to a definition already shipped with the framework under `.specify/agents/templates/`
(mirror `agents/`): `sdd-task-{coordinator,executor}`, `sdd-implement-{coordinator,executor}`,
`sdd-review-{coordinator,executor}`, `sdd-stage-verifier`, `sdd-stage-integrator`, `reporter`. This roster is
created with **zero new agent definitions** — no seat needed instantiation from a stage frame, so no
`team-scope` seat instance is produced by this creation, and the framework sources under `skills/`, `agents/`
and `shared/` receive **zero writes** from this creation step.

**Type by operating object** (never by stage): the six stage seats, the verifier and the integrator operate on
business artifacts (spec files, framework sources, tests, gate verdicts) → `Worker`. The reporter operates on
the run's observable state and writes only its own stream artifact → `Meta`.

**Coordinator status**: the coordination duty is carried by the **orchestrating SDD driver session**, which
already selects the stage, the slice and the next step (`.specify/shared/workflow/execution-topology.md` puts
team seats on the execution side, with the driver owning the loop). The coordinator seats stay in the roster
because the tasks / implement / review stages declare their own coordinator + executor pair, and they are
invoked when a stage's package count exceeds what the driver partitions in one turn.

## Dynamic Structure

Pattern: **serial** (质量优先) with in-stage parallelism — a DAG over the three remaining canonical SDD stages;
no cycles; each stage hands off by **file path only** and a per-handoff verification guards every step.

```
tasks  ──(U4)──►  implement  ──(U4)──►  review
  │                  │                   │
  └────────── verifier (independent, one reserve per stage) ──────────┘
```

- **Outer chain**: serial across `tasks` → `implement` → `review`; no stage starts before its predecessor
  closes at U4. Checklists / analyze are already-completed canonical stages and are not re-declared here.
- **In-stage parallelism (checkpoint 03 decision)**: `stage_seats.<stage>.max_parallel` is the ceiling for
  concurrent seats inside one stage — `tasks: 4`, `implement: 8`, `review: 4` — and none exceeds the run's
  effective concurrency (24, verifier reserve 1). `decomposition_slot_cap: 8` matches the implement ceiling.
  All write packages share one tree (`isolation: shared-tree`), so concurrent executors MUST hold **disjoint
  write paths**.
- **Package plan (plan.md § Implement Package Proposal)**: `P1` owner + declaration + registration →
  `P2` the deterministic engine → `P3` the history seam → `P4` the three pointer faces → `P5` the contract
  guard → `P6` the 档 I repair lane, with **`P7` (档 II shift list) concurrent with `P6`** → `P8` stage
  verification. P6||P7 is the only real in-stage parallelism the plan authorizes; everything else is a chain,
  so the implement ceiling of 8 is a bound, not a target.
- **Verifier reserve**: exactly **one** verifier is reserved per stage and is never the executor of the object
  it verifies (every invocation is a fresh subagent).
- **Integrator seat**: consolidates the stage's produced artifacts into the checkpoint and the run report; it
  never dispatches agents and never writes the state spine.
- **Reporter seat**: emits one attributed status line per the cadence owned by
  `.specify/shared/guidelines/progress-reporting.md` (the literal `default`), writing only
  `test-evidence/reporter-092-non-disposable.live.log`; it mutates nothing else.
- **Design-approval gate (spec-specific, non-negotiable)**: `/speckit.history`'s review and design segments
  MUST write nothing to disk; the execute segment runs only after explicit user confirmation (US-3/SC-004).
  The driver carries this gate, not the seats.
- **Run reports**: per stage, at `<team-root>/<slug>/runs/<UTC-timestamp>-report.md`, with the mandatory
  `## Verification` section and the `## Nested SDD Runs` section appended last.

Ownership of the run report: the SDD driver session is the sole writer of tracked artifacts for this
spec-local team, so run reports are written by the driver under `runs/` when a stage closes.

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports under `runs/` and the per-stage checkpoints under
  `.specify/specs/092-non-disposable/checkpoints/`.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team` (the
  checkpoint's single configuration proposal is the entry, cap one change per stage).
- Boundary: preserve team authority, the verifier's independence, the stage sequence, the design-approval gate
  and the sentinel literals; this team never writes `.specify/teams/**` or `.specify/goal/**`.
- Verify: validate now (`skills/internal/create-team/scripts/validate-roster.py`) and wait for a comparable
  later run before claiming improvement.
