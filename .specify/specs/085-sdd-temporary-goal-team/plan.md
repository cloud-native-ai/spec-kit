# Implementation Plan: SDD 临时 Goal / 临时 Team 与多 Agent 并发

**Branch**: `085-sdd-temporary-goal-team` | **Date**: 2026-11-06 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `085-sdd-temporary-goal-team` → Feature 085 SDD 临时 Goal / 临时 Team 与多 Agent 并发
**Input**: Specification from `.specify/specs/085-sdd-temporary-goal-team/requirements.md` (50 FR / 10 SC / 5 runtime rows; requirements stage validated 2026-11-06)

## Summary

Feature 085 adds a **temporary hierarchy inside the SDD run** and makes stage-level concurrency the primary efficiency mechanism:

```text
Global (unchanged):   Global Goal → Global Team → Agent → SDD run
Temporary (new):      SDD run → Temporary Goal → Temporary Team → stage agents
```

The temporary Goal is authored after `requirements` U4 and stored at `.specify/specs/<NNN-slug>/goal/goal.md`; the temporary Team is created after `clarify` + `plan` U4 and stored at `.specify/specs/<NNN-slug>/team/team.md`. Both are adjustable at any time and retained in place at completion. `/speckit.goal` and `/speckit.team` gain a deterministic `--scope global|spec|auto` + `--spec-dir` surface, resolved by one `goal-utils.py resolve-scope` owner.

Every SDD startup declares `agent_concurrency_requested` (default 24). The driver resolves `agent_concurrency_effective` per stage from the declared value, host capacity, stage `max_parallel`, ready packages, verifier reserve, and resource capacity; every downgrade is named. Stage work uses stage-specific roles (`sdd-requirement-analyzer`, `sdd-plan-coordinator`, `sdd-plan-executor`, and the `<stage>-<role>` grammar) rather than one generic executor. Writing agents each get a child line, a dedicated git worktree/branch, and an entry in the existing 064 integration queue; integration order comes from the work-package plan, never dispatch timing.

Each stage boundary runs a four-part checkpoint: artifact verification, temporary-goal progress by degree, at most one team-configuration proposal with ratification, and the next stage's concurrency/roster decision. The proposal reuses `wp-report.py` + team run report + ledger evidence and the existing `improve-team` / `coordinate` proposal shape. The generic `agents/sdd-executor.agent.md` is removed; all retained framework agents carry `run-turn-budget: 500`, and every rendered copy carries the corresponding budget.

The design is deliberately additive: 074's global hierarchy, 070's `shared-tree` write mode, and 064's root-line behavior remain the compatibility baseline. No new command, scheduler, daemon, registry, ledger, or state spine is introduced.

## Technical Context

**Language/Version**: Python 3.8+ for `goal-utils.py`, `line-registry.py`, `wp-gate.py`, and new contract tests; Markdown for concepts, skills, commands, contracts, and agent definitions. Host tested with Python 3.11.11.
**Primary Dependencies**: none new. Reuses `goal-utils.py`, `line-registry.py`, `wp-gate.py`, `wp-report.py`, `sync-mirrors.py`, `regen-command-copies.py`, `specify render-agents`, `scripts/bash/run-tests.sh`, and the existing pytest suites.
**Storage**: spec-local `goal/`, `team/`, `checkpoints/`; child worktrees under `.specify/.tmp/sdd-loop/worktrees/<child_line_id>`; line registry entries in the existing environment registry; no new database or daemon.
**Testing**: pytest (`tests/contract`, `tests/unit`, `tests/integration`); Tests Mode = ON. Red-first evidence for each new behavior; full suite at implement start and closure; targeted sets for intermediate stages.
**Target Platform**: macOS/Linux driver hosts; local native and remote external topologies; hosts may support fewer than 24 concurrent agents and must record the effective value.
**Project Type**: SDD framework (skills, commands, shared definitions, scripts, agent definitions, tests).
**Performance Goals**: shorten the SDD wall-clock by using more concurrent stage agents; no absolute wall-clock promise. The measurable target is that at least one stage in the dogfood run dispatches more than one agent concurrently and that every dispatch records requested/effective concurrency.
**Constraints**: no new `/speckit.*` command; no new scheduler/daemon/registry/ledger/state spine; no global Goal/Team writes from an SDD run; no automatic merge/push; no silent downgrade; no rewrite of dated historical records.
**Scale/Scope**: 50 FR / 10 SC; 8 stage role families; 1 scope resolver; 1 checkpoint protocol; 1 child-line extension; 1 write-isolation mode; ~10-15 agent definition files removed/created/updated.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development as Foundation | ✅ Pass | Every design decision maps to an FR; requirements validated with 0 error / 0 warning; this plan cites the requirement rows. |
| II | Feature-Centric Development | ✅ Pass | Feature 085 is registered in `features.md` and `.specify/memory/features/085.md`; the plan advances Draft → Planned at tasks. |
| III | Intent-Driven Development | ✅ Pass | User decisions (temporary hierarchy, 24 default, per-agent worktrees, stage agents, maxTurns 500) are recorded in requirements § Clarifications; alternatives are recorded in research.md. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Tests Mode ON; each slice has a red-first behavior group; contracts own the new clauses. |
| V | AI Agent Integration Standards | ✅ Pass | Agent changes use the existing neutral key set and renderer; no host-specific field is hand-written; every rendered copy is produced by `specify render-agents`. |
| VI | Continuous Quality & Observability | ✅ Pass | Requested/effective concurrency, downgrade reasons, checkpoint decisions, and integration results are recorded; no fabricated metrics. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify (recorded) → plan respected; status stays Draft until tasks; no implementation before tasks. |
| VIII | Code as the Single Source of Truth | ✅ Pass | The plan reads the live `goal-utils.py`, `line-registry.py`, `wp-gate.py`, `create-mode.md`, and the 064/070 owners; it does not design from memory. |
| IX | Framework Scope Discipline | ✅ Pass | One new engine action, one child-line extension, one checkpoint reference, one role grammar; no new command/scheduler/daemon/store. |
| X | Documentation Naming & Location Conventions | ✅ Pass | New files use path-semantic lowercase names; `SKILL.md` and reserved names unchanged. |
| XI | Dogfooding | ✅ Pass | The feature runs through its own SDD chain; framework-source edits are mirrored by `sync-mirrors.py`; no client-runtime hand edits. |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | Reuses `goal-utils.py`, `line-registry.py`, `wp-gate.py`, `wp-report.py`, `improve-team`, `coordinate`, and the renderer; no second engine for the same predicate. |
| XIII | Better-Harness Orientation | ✅ Pass | The change targets Task Understanding (stage-specific roles), Controlled Execution (concurrency + checkpoints), and Reliable Delivery (worktrees + integration queue). |
| XIV | One Source Of Truth | ✅ Pass | Scope rule owned by `goal-utils.py resolve-scope`; temp Goal/Team concepts owned by goal-definitions/conceptual-model; 070/064 clauses cited by path. |
| XV | User-Facing Comprehension | ✅ Pass | The plan and quickstart define temporary vs global at first use, give commands with premises, and point to evidence paths. |
| XVI | Fast Fail | ✅ Pass | Disk exhaustion, scope ambiguity, wrong scope, host downgrade, integration conflict, and missing artifacts are surfaced with named reasons; no silent repair. |
| XVII | Directory Governance | ✅ Pass | New directories are spec-local `goal/`, `team/`, `checkpoints/`; child worktrees use the sanctioned `.specify/.tmp/` root; no ad-hoc top-level directory. |
| XVIII | Grounded Naming | ✅ Pass | `Temporary Goal` / `Temporary Team` come from the user's own vocabulary; role names follow the user's examples and the existing `<stage>-<role>` convention. |
| XIX | Self-Explanatory Structure | ✅ Pass | The user-visible surface is the SDD run: goal, team, concurrency, checkpoints, and status; internal schema is projected only as needed. |

**Gates Status**: ✅ All gates pass. No ❌ or ⚠ row; Complexity Tracking is N/A.

## Decision Tensions

### T-001 — Temporary hierarchy vs global hierarchy

- **decision**: Add a spec-local Temporary Goal/Team hierarchy inside the SDD run; keep the global Goal→Team→SDD hierarchy unchanged.
- **antithesis**: Let the SDD driver create a Global Goal/Team at U0, making the SDD run the top-level author.
- **binding_constraints**: `pole_a`: global hierarchy remains authoritative (074 FR-001, `sdd-routing-definitions.md` § Hierarchy); `pole_b`: the user wants goal/team attached to the SDD flow, created after requirements/plan.
- **discriminating_evidence**: The user explicitly said the temporary artifacts are attached to the spec and only become known after requirements/plan; 074 forbids a run creating global Goal/Team.
- **expected_sacrifice**: Two hierarchies and a scope resolver instead of one hierarchy.
- **revision_trigger**: A future user decision to promote temporary artifacts to global, or a requirement that global Goal/Team must be created by the SDD run.
- **tension_id**: T-001

### T-002 — Per-agent worktrees vs shared-tree disjoint writes

- **decision**: Writing agents run in independent worktrees and integrate through the existing line registry/integration queue.
- **antithesis**: Keep 070's shared-tree write serialization and use concurrency only for read-only work.
- **binding_constraints**: `pole_a`: safe concurrent writes; `pole_b`: minimal change and no new isolation machinery.
- **discriminating_evidence**: The user chose per-agent worktrees + integration queue; existing 064 already provides the queue and worktree primitives.
- **expected_sacrifice**: Higher disk usage and integration overhead; more line-registry fields.
- **revision_trigger**: A host or repo where worktree cost outweighs concurrency gain, or 064's queue cannot support child lines.
- **tension_id**: T-002

### T-003 — Fixed stage roster vs dynamic role grammar

- **decision**: Define a role grammar (coordinator/worker/verifier/integrator) and let each stage decide its count and type from the benefit test and effective concurrency.
- **antithesis**: Ship a fixed roster with a fixed number of agents per stage.
- **binding_constraints**: `pole_a`: the user's core goal is efficiency through concurrency; `pole_b`: agents need stable definitions and testable roles.
- **discriminating_evidence**: The user said agent count/type are implementation details and should vary by stage; requirements starts with 1 while tasks/implement may use many.
- **expected_sacrifice**: Less predictable per-stage behavior; the checkpoint must record and validate the decision.
- **revision_trigger**: Dogfood shows that a fixed roster is safer or that dynamic roles cause coordination overhead.
- **tension_id**: T-003

## Project Structure

### Documentation (this spec)

```text
.specify/specs/085-sdd-temporary-goal-team/
├── plan.md
├── requirements.md
├── research.md
├── data-model.md
├── contracts/
│   ├── scope-resolution.md
│   ├── temporary-goal-team.md
│   ├── concurrency-and-worktrees.md
│   ├── checkpoint-and-agents.md
│   └── stage-agents.md
├── quickstart.md
├── feature-ref.md
├── checklists/
├── test-evidence/
├── tasks.md              # /speckit.tasks output, not created here
└── verification.md       # /speckit.implement output, not created here
```

### Source Code (repository root)

```text
scripts/python/goal-utils.py                  # EDIT: Scope + resolve-scope + spec-local paths
scripts/python/sdd-route.py                   # EDIT: authorize accepts scope/spec-dir
skills/internal/create-team/                  # EDIT: spec scope, stage_seats, run/improve paths
skills/internal/manage-goal/                  # EDIT: temporary goal workflow and scope
skills/internal/run-team/                     # EDIT: scoped team load/report
skills/internal/improve-team/                 # EDIT: scoped team and checkpoint proposals
skills/external/sdd-loop-driver/              # EDIT: U0 fields, checkpoint protocol, worktree mode, new rules
skills/external/sdd-loop-driver/scripts/      # EDIT: line-registry child lines, wp-gate rules
shared/definitions/goal-definitions.md        # EDIT: Temporary Goal concept
shared/definitions/sdd-routing-definitions.md # EDIT: spec-local carve-out
shared/definitions/subagent-definitions.md    # EDIT: child-line/agent nesting boundary
agents/*.agent.md                             # DELETE generic; ADD stage-specific role templates
.specify/agents/{templates,instances}/        # MIRROR: regenerated definitions; remove generic
skills/internal/create-agent/templates/       # EDIT: unified 500 budgets; stage role bases
skills/internal/create-team/templates/agents/ # EDIT: supervisor budget 500
templates/commands/goal.md, team.md           # EDIT: --scope/--spec-dir
tests/contract/, tests/unit/, tests/integration/  # ADD/EDIT guards
docs/reference/                              # EDIT: command/skill/agent docs
```

**Structure Decision**: This spec extends the existing SDD framework layout. It creates no new top-level directory; the new runtime directories are spec-local (`goal/`, `team/`, `checkpoints/`) and the child worktrees use the sanctioned `.specify/.tmp/` root. Framework sources are edited in `scripts/`, `skills/`, `shared/`, `agents/`, and `templates/`; `.specify/` copies are regenerated by the mirror/generator machinery.

### Mirror Obligations

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/goal-utils.py`, `scripts/python/sdd-route.py` | `.specify/scripts/python/...` via `sync-mirrors.py` | `sync-mirrors.py --check` — no new drift vs pre-change baseline |
| `skills/internal/{create-team,manage-goal,run-team,improve-team}/**` | `.specify/skills/internal/...` via `sync-mirrors.py` | same |
| `skills/external/sdd-loop-driver/**` | `.specify/skills/sdd-loop-driver/...` via `sync-mirrors.py` | same |
| `shared/definitions/{goal-definitions,sdd-routing-definitions,subagent-definitions}.md` | `.specify/shared/definitions/...` via `sync-mirrors.py` | same |
| `templates/commands/{goal,team}.md` | per-tool copies via `regen-command-copies.py` | `regen-command-copies.py --check` |
| `agents/*.agent.md`, `.specify/agents/{templates,instances}/**` | `.qoder/.claude/.github/.opencode/agents/**` + `.render-manifest.json` via `specify render-agents` | manifest sha match; removed generic absent everywhere |
| `skills/internal/create-agent/templates/**`, `skills/internal/create-team/templates/agents/**` | `.specify/skills/...` via `sync-mirrors.py` | same |

## Execution Premises

| ID | Premise | Evidence | Status | Decision |
|----|---------|----------|--------|----------|
| EP-001 | Python 3.8+ and pytest are available; deterministic checks and contract tests run locally without network or a daemon. | `python3 --version`; `python3 -m pytest --version`; `scripts/bash/run-tests.sh`; `pyproject.toml` | verified | — |
| EP-002 | At least one supported host can load rendered agent definitions and run stage agents with the declared budget. | `docs/reference/cli/supported-agent-tools.md`; render manifest; dogfood run | unverified | — |
| EP-003 | The repository has enough disk space for child worktrees and their integration copies; the preflight can measure it. | `df -h /storage` (729G free after user cleanup); `git check-ignore -q .specify/.tmp` | verified | — |
| EP-004 | Features 070 and 064 are the compatibility baseline; their legacy modes remain available and testable. | `.specify/memory/features/070.md` (Implemented); `.specify/memory/features/064.md`; existing contract suites | verified | — |

## Inherited Blockers

Dependency set: none.

| # | Source row | Disposition | Carrier | Carrier slice | Evidence / note |
|---|-----------|-------------|---------|---------------|-----------------|

## Complexity Tracking

N/A — the Constitution Check has no ❌ Fail and no ⚠ Partial row.

## Phase 0: Research Review

The research findings are recorded in [research.md](research.md). The key rulings are: (R1) temporary hierarchy carve-out rather than global inversion; (R2) spec-local scope resolution owned by `goal-utils.py`; (R3) child lines reuse 064 rather than a second queue; (R4) `write_isolation=worktree` is additive to 070; (R5) dynamic role grammar instead of a fixed roster; (R6) all retained agents use 500; (R7) generic `sdd-executor` is removed; (R8) checkpoint proposals reuse `improve-team`/`coordinate` shapes.

## Implementation Slicing

| Slice | Scope | Exit evidence |
|-------|-------|---------------|
| S0 | Preflight: disk, git, baseline | baseline test run + node-id set in `test-evidence/` |
| S1 | Scope resolver and command surfaces | `test_scope_resolution.py`, `test_goal_scope_engine.py`; old global behavior unchanged |
| S2 | Temporary Goal concept and lifecycle | `test_temp_goal_contract.py`; goal created only after requirements U4 |
| S3 | Temporary Team schema and `stage_seats` | `test_temp_team_schema.py`, `test_stage_seat_map.py` |
| S4 | 064 child lines, worktrees, integration queue | `test_line_registry_child_lines.py`, `test_temp_team_worktree_queue.py` |
| S5 | 070 write isolation + requirements/tasks rules | `test_sdd_loop_driver_wp_gate.py`, `test_sdd_loop_driver_wp_coordination.py` updates |
| S6 | Stage agents, remove generic executor, unify 500 | `test_unified_turn_budget.py`, render manifest checks |
| S7 | Checkpoint protocol and config optimization | `test_checkpoint_protocol.py`, rollback drill |
| S8 | Dogfood, docs, closure | `verification.md`, dogfood evidence, `review.md` |

If the tasks stage returns `split-required`, split into `085a` (S1–S3 + S7) and `085b` (S4–S6 + S8), following the 074a/074b precedent.

## Phase 1: Design Artifacts Summary

Counts below are backfilled after the artifacts land on disk.

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Research | [`research.md`](research.md) | R1–R8 |
| Data model | [`data-model.md`](data-model.md) | 8 entities, validation rules |
| Contracts | [`contracts/`](contracts/) | 5 files: scope-resolution, temporary-goal-team, concurrency-and-worktrees, checkpoint-and-agents, stage-agents |
| Quickstart | [`quickstart.md`](quickstart.md) | S1–S6 |
| Feature ref | [`feature-ref.md`](feature-ref.md) | binding, delivery surface, FR/SC map |
