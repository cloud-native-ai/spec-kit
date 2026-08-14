# Data Model: Agent Framework Redesign

**Spec**: [requirements.md](./requirements.md) | **Plan**: [plan.md](./plan.md)

This is a documentation/tooling refactor; "entities" are conceptual constructs and file artifacts, not database records.

## Core Entities

### Agent

An agent is fully described by three orthogonal attribute dimensions plus its lifecycle.

| Field | Type | Description | Source |
|-------|------|-------------|--------|
| `name` | string (kebab-case) | Unique agent identifier / filename stem | existing |
| `role` | Role | Responsibility + perspective | FR-003 |
| `stage` | Stage | Current execution phase | FR-003 |
| `type` | Type | Worker or Meta (derived from `stage`) | FR-003/004 |
| `lifecycle` | enum(`temporary`, `persistent`) | Context-only vs stored under `.specify/agents` | FR-010/011 |
| `provider` | enum | Approved provider only | Constitution V |

**Validation rules**:
- `type` MUST equal the value derived from `stage` (see Type-follows-Stage).
- `persistent` agents MUST be written under `.specify/agents/` (`[[STR-006]]`).
- `provider` MUST be in the approved whitelist; unsupported providers rejected.

### Role

The responsibility and problem-solving perspective an agent embodies.

**Worker roles (6, current)**: Requirements Analyst, System Designer, Module Designer, Test Engineer, QA Engineer, Knowledge Manager.
**Meta role (1)**: Team Supervisor (merged from Meta-Coordinator + Team Supervisor).
**Deferred (D1)**: UX Analyst (in design matrix; no template this iteration).

### Stage

The execution phase of a role. Enum, canonical names:

| Stage | English (`[[STR]]`) | Deprecated alias (removed) |
|-------|---------------------|----------------------------|
| Executor | `executor` `[[STR-001]]` | — |
| Evaluator | `evaluator` `[[STR-002]]` | — |
| Optimizer | `optimizer` `[[STR-003]]` | `improver` |

The dimension itself is **Stage**; the deprecated dimension name **SubRole** is removed.

### Type

Classification derived from Stage.

| Type | Value | Meaning |
|------|-------|---------|
| Worker | `[[STR-004]]` | Performs real project tasks |
| Meta | `[[STR-005]]` | Optimizes/manages other agents |

### Type-follows-Stage Coupling (FR-004)

| Stage | Type |
|-------|------|
| executor | Worker |
| evaluator | Meta |
| optimizer | Meta |

Exception: a **Meta role** (Team Supervisor) is Meta at **all** stages — it never performs real project tasks.

### Team (static structure, FR-005/007)

A Role × Stage matrix; each cell is a Type.

| Role \ Stage | executor | evaluator | optimizer |
|--------------|----------|-----------|-----------|
| Requirements Analyst | Worker | Meta | Meta |
| System Designer | Worker | Meta | Meta |
| Module Designer | Worker | Meta | Meta |
| Test Engineer | Worker | Meta | Meta |
| QA Engineer | Worker | Meta | Meta |
| Knowledge Manager | Worker | Meta | Meta |
| **Team Supervisor** (Meta role) | Meta | Meta | Meta |

### Loop (dynamic structure, FR-006)

The runtime iteration a multi-agent group performs across stages. Realized by `organize-agents` Team Loop: initialize → coordinate → execute → evaluate → decide → optimize, bounded by threshold / max-iterations / regression-limit.

### AgentTemplate

A reusable Markdown template co-located with the `create-agent` skill.

| Category | Naming scheme | Examples |
|----------|---------------|----------|
| Role | `agent-role-<role>-template.md` | `agent-role-requirements-analyst-template.md`, `agent-role-team-supervisor-template.md` |
| Stage | `agent-stage-<stage>-template.md` | `agent-stage-executor-template.md`, `agent-stage-evaluator-template.md`, `agent-stage-optimizer-template.md` |
| Orchestration | `agent-<pattern>-orchestration-template.md` / `agent-triad-orchestration-template.md` | parallel, serial, triad |
| Support | descriptive | `agent-supervision-delegation.md`, `agent-workflow-schema.md` |

### ResearchFindings (FR-021)

Consolidated artifact at `.specify/specs/023-agent-framework-redesign/research.md` capturing best practices mined from each in-scope `/cws_work/*` sibling project (one agent per project), feeding redesign decisions.

## Template Migration Map (old → new)

Applied within `skills/create-agent/templates/` (canonical) and mirrored to `.specify/skills/create-agent/templates/`.

| Old file | New file | Change |
|----------|----------|--------|
| `agent-subrole-executor-template.md` | `agent-stage-executor-template.md` | rename |
| `agent-subrole-evaluator-template.md` | `agent-stage-evaluator-template.md` | rename |
| `agent-subrole-improver-template.md` | `agent-stage-optimizer-template.md` | rename + internal `improver`→`optimizer`, `name`/`description` |
| `agent-role-meta-coordinator-template.md` + `agent-team-supervisor-template.md` | `agent-role-team-supervisor-template.md` | **merge** into one Meta role |
| `agent-supervision-delegation.md` | (same name) | terminology update |
| `agent-triad-orchestration-template.md` | (same name) | `improver`→`optimizer`, add Stage/Type framing |
| `.specify/templates/agent-*` (legacy duplicates) | (removed) | delete stale copies (D3) |

**Migration targets outside templates**: `create-agent/SKILL.md`, `improve-agent/SKILL.md`, `organize-agents/SKILL.md`, `templates/commands/agents.md`, `docs/agents/*`, `docs/commands/agents.md`, `tests/scenarios/multi-agent-orchestration/*`, `.specify/agents/*.agent.md` + `AGENTS.md`, and installed `.specify/skills/**` mirrors.

## State Transitions

Agent lifecycle: `intent → (temporary | persistent)`. Persistent agents: `authored → written to .specify/agents → linked into supported tools on init`. No other stateful transitions.
