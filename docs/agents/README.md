# Spec Kit Agent Framework

This directory documents the Spec Kit **Agent framework** as it is actually implemented
(spec `023-agent-framework-redesign`, Feature 019 *Agents Command*). It supersedes the
earlier conceptual proposal: every statement here reflects the code, skills, templates,
and persisted agents that ship in the repository.

## What the framework is

An **Agent** is a unit of work fully described by three orthogonal attribute dimensions,
organized by two structures, driven by one command, and produced by three skills:

- **Model** — every agent is `Role × Stage × Type`, arranged statically as a **Team**
  (a Role×Stage matrix) and dynamically as a **Loop** (iteration across stages).
- **Command** — `/speckit.agents` is the *single* entry point for single-agent work. It
  recognizes intent and delegates; it never renders templates inline. Multi-agent teams
  (organizing / running several agents) live behind `/speckit.team`.
- **Skills** — `create-agent` (author a single agent), `improve-agent` (refine a single
  agent). Team orchestration (parallel / serial / team-loop) is owned by the team domain:
  `create-team` and `improve-team` via `/speckit.team`.
- **Artifacts** — reusable templates under `skills/create-agent/templates/` and persisted
  agents under `.specify/agents/`, linked into every supported tool by per-file symlink.

```
         /speckit.agents  (single-agent entry)        /speckit.team  (team entry)
                 │                                            │
        ┌────────┴────────┐                          ┌────────┴────────┐
        ▼                 ▼                          ▼                 ▼
   create-agent      improve-agent               create-team      improve-team
   (author)          (refine)                    (define|run:              (refine team:
        │                 │                        parallel|serial|          stages/thresholds)
        ▼                 ▼                        team-loop)
   skills/create-agent/templates/*        .specify/agents/*.agent.md  ──(per-file symlink)──▶ .qoder/agents/, .github/agents/, …
   (Role × Stage × Type source)           (persisted Team members)
```

## Document map

| Document | What it covers |
|----------|----------------|
| [design.md](./design.md) | **Authoritative conceptual model & design** — Role/Stage/Type, Type-follows-Stage, the Team matrix, the Loop, and the merged Team Supervisor. Start here. |
| [command-and-skills.md](./command-and-skills.md) | The `/speckit.agents` single entry point, intent→capability routing, the three skills, the temporary/persistent lifecycle, and tool integration. |
| [templates-and-agents.md](./templates-and-agents.md) | The canonical template catalog and naming scheme, the seven preset role agents + Team Supervisor, the `.specify/agents/` layout, and the `AGENTS.md` registry. |
| [eei-triad-pattern.md](./eei-triad-pattern.md) | The Executor-Evaluator-Optimizer (EEI) quality loop and role-scoped supervisors. |
| [multi-agent-orchestration.md](./multi-agent-orchestration.md) | Operational guide for the three collaboration topologies: parallel dispatch, serial chain, team loop — owned by the team domain (`/speckit.team`, `create-team`). |

## Core vocabulary (quick reference)

| Term | Meaning | Canonical values |
|------|---------|------------------|
| **Role** | Responsibility + problem-solving perspective | 7 Worker roles + 1 Meta role (Team Supervisor) |
| **Stage** | Execution phase of a role | `executor`, `evaluator`, `optimizer` |
| **Type** | Classification derived from Stage | `Worker` (real tasks) · `Meta` (manages/optimizes agents) |
| **Team** | Static structure | Role×Stage matrix, cells hold the Type |
| **Loop** | Dynamic structure | runtime iteration across stages |
| **Lifecycle** | Where an agent lives | `temporary` (context-only) · `persistent` (`.specify/agents/`) |

> **Terminology note**: `Stage` replaced the deprecated "SubRole" dimension name;
> `optimizer` replaced the former "improver" stage name; and a single merged
> **Team Supervisor** replaced the formerly separate "Meta-Coordinator" role.
> These are the only accepted terms in live artifacts.

## Traceability

The normative source of these docs is the redesign spec:
`.specify/specs/023-agent-framework-redesign/` — see `requirements.md`, `data-model.md`,
and `contracts/{conceptual-model,agents-command,template-migration}-contract.md`.
