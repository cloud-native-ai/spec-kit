# Data Model: Agent Team Management

**Feature**: 027 Team Management | **Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

This document defines the entities of the team domain, the persisted team-directory schema (`<slug>/team.md` + `<slug>/runs/`), the run-workspace/output discipline, and the classification that governs which `agent-*` templates move from the single-agent domain into the team domain.

## Entities

### Team

A named, reusable multi-agent structure organized from a user goal. It is the primary new concept and the unit that `/speckit.team` creates, modifies, and runs.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `slug` | kebab-case string | yes | Unique identifier; also names the team directory `.specify/teams/<slug>/` (definition at `<slug>/team.md`). |
| `name` | string | yes | Human-readable display name. |
| `description` | string | yes | One-line purpose (goal statement). |
| `pattern` | enum `parallel` \| `serial` \| `team-loop` | yes | The collaboration/dynamic structure. |
| `members` | list<TeamMember> | yes (≥1) | The roster (static structure). |
| `config` | TeamConfiguration | yes | Pattern-specific runtime settings. |
| `created` / `updated` | ISO date | yes | Lifecycle timestamps. |

**Validation rules** (from FR-004, FR-007, FR-009):
- `slug` MUST be unique within `.specify/teams/`.
- `members` MUST reference agents that resolve to `.specify/agents/<slug>.agent.md` **or** to a temporary stage/worker template; unresolved members are surfaced as broken references (Edge Case: stale membership).
- `pattern` MUST be one of the three canonical values; `config` MUST match the pattern (see TeamConfiguration).
- A `team-loop` team MUST include exactly one **Team Supervisor** (Meta role) member.

### TeamMember

One agent's participation in the team (one row of the static Role×Stage×Type matrix).

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `agent` | string | yes | Agent slug (persistent) or stage template id (temporary). |
| `role` | string | yes | Role/perspective (e.g. `system-designer`, `team-supervisor`). |
| `type` | enum `Worker` \| `Meta` | derived | Type-follows-Stage; `Worker` at executor stage, `Meta` at evaluator/optimizer; Team Supervisor is always `Meta`. |
| `lifecycle` | enum `persistent` \| `temporary` | yes | Persistent = a `.specify/agents/*` agent; temporary = instantiated per run from a stage/worker template. |
| `territory` | list<path> | parallel only | Exclusive write scope (parallel dispatch). |
| `blockedBy` | list<member-id> | serial only | Upstream dependencies (serial DAG). |

### TeamConfiguration

Pattern-specific runtime settings; exactly one shape applies per `pattern`.

| Pattern | Fields |
|---------|--------|
| `parallel` | `parallelism` (int, recommended 2–4), `territories` (per-member write/read scopes), `forbidden_write` (shared files only the lead writes) |
| `serial` | `stages` (ordered), `blockedBy` edges (DAG, no cycles), `handoff` = file-path-only, `progress_file` (a run intermediate → `.specify/teams/.work/<slug>/`) |
| `team-loop` | `quality_dimensions[]` (name+weight, Σ=1.0), `threshold` (default 0.8), `max_iterations` (default 5, max 10), `regression_limit` (default 2) |

### Report

A per-run record written **after every run** to `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md` (tracked; reports accumulate across runs).

| Field | Required | Description |
|-------|----------|-------------|
| goal | yes | The team's goal / success criteria for this run. |
| timing | yes | Started / finished / duration. |
| result summary | yes | Concise summary of the final result against the goal. |
| execution detail | yes | Full process record (decomposition / stage or iteration log / scores / decisions / handoffs / problems) — enough to later optimize the team, its skills, and commands. |
| deliverables | yes | Final deliverable paths (real target paths, not the team directory). |

### Run Workspace & Output Discipline

Every run separates four output classes:

| Class | Location | Git |
|-------|----------|-----|
| Team definition | `.specify/teams/<slug>/team.md` | tracked |
| Run reports | `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md` | tracked, accumulate |
| Deliverables (standard output) | declared target path (real project path) | tracked |
| Run intermediates (progress, manifests, iteration scratch, working memory, intermediate handoffs) | `.specify/teams/.work/<slug>/` | git-ignored |

The team directory `.specify/teams/<slug>/` holds **only** `team.md` + `runs/`. Only final deliverables count as standard output; intermediate serial-stage handoffs are run intermediates.

### Team `team.md` file schema (canonical persistence)

Stored at `.specify/teams/<slug>/team.md` (the team owns the directory `.specify/teams/<slug>/`; run reports accumulate under `<slug>/runs/`). No per-tool symlink (framework-internal artifact).

```markdown
---
name: <display name>
slug: <kebab-slug>
description: <goal / purpose>
pattern: parallel | serial | team-loop
created: YYYY-MM-DD
updated: YYYY-MM-DD
members:
  - agent: <slug-or-template-id>
    role: <role>
    lifecycle: persistent | temporary
    # territory: [...]        # parallel
    # blockedBy: [...]        # serial
config:
  # pattern-specific block (see TeamConfiguration)
---

## Static Structure
<Role × Stage × Type matrix table for this team's roster>

## Dynamic Structure
<pattern description, parallelism/DAG/loop settings, and the execution flow diagram>
```

## State / Lifecycle

```
(none) --create--> Defined(persisted <slug>/team.md)
Defined --modify--> Defined(updated)
Defined --run--> Preview(static+dynamic) --confirm--> Executing --> Completed/Halted --> Report(<slug>/runs/<ts>-report.md)
```

- **create** (create-team): produce a `Team` and persist `<slug>/team.md` (or run one-shot without persisting).
- **modify** (improve-team): load an existing `<slug>/team.md`, apply targeted evidence-based edits, re-persist; unaffected fields unchanged (SC-005).
- **run** (create-team execution): load `<slug>/team.md`, render **Static Structure** + **Dynamic Structure** (incl. flow diagram), require explicit user confirmation, orchestrate (parallel/serial/team-loop) with intermediates in `.specify/teams/.work/<slug>/`, then write a dated report to `<slug>/runs/`.

## Template Classification (single-agent vs team)

This governs the physical relocation performed by the migration contract. Source: `skills/create-agent/templates/`.

| Template file | Destination | Rationale |
|---------------|-------------|-----------|
| `agent-role-requirements-analyst-template.md` | **stay** `create-agent` | single Worker role |
| `agent-role-ux-analyst-template.md` | **stay** | single Worker role |
| `agent-role-system-designer-template.md` | **stay** | single Worker role |
| `agent-role-module-designer-template.md` | **stay** | single Worker role |
| `agent-role-test-engineer-template.md` | **stay** | single Worker role |
| `agent-role-qa-engineer-template.md` | **stay** | single Worker role |
| `agent-role-knowledge-manager-template.md` | **stay** | single Worker role |
| `agent-supervision-delegation.md` | **stay** | single self-improving role (`supervisor` kind) |
| `agent-skill-enablement.md` | **stay** | role-agent skill-enablement snippet |
| `agent-project-custom-template.md` | **stay** | single project-bound agent |
| `agent-role-team-supervisor-template.md` | **move → `create-team/templates/`** | team-supervisor is a team construct (FR-016) |
| `agent-stage-executor-template.md` | **move → `create-team/templates/`** | triad stage (multi-agent loop, FR-016) |
| `agent-stage-evaluator-template.md` | **move** | triad stage (FR-016) |
| `agent-stage-optimizer-template.md` | **move** | triad stage (FR-016) |
| `agent-triad-orchestration-template.md` | **move** | triad orchestration (FR-016) |
| `agent-parallel-orchestration-template.md` | **move** | orchestration (team domain) |
| `agent-serial-orchestration-template.md` | **move** | orchestration (team domain) |
| `agent-workflow-schema.md` | **move** | AgentWorkflow JSON schema for serial/parallel |
| `references/conceptual-model.md` (NEW) | **create in `create-team`** | extracted Conceptual Model — single source of truth (FR-011/FR-012) |

**Post-move guarantee** (SC-003/SC-004/SC-006): after relocation, `create-agent` retains only `role`, `supervisor`, `custom`, `project-custom` modes; the Conceptual Model is defined exactly once (in the team domain); zero `organize-agents` references remain in active paths.
