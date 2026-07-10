# Implementation Plan: Agent Framework Redesign

**Branch**: `023-agent-framework-redesign` | **Date**: 2026-07-10 | **Spec**: [requirements.md](./requirements.md)
**Input**: Specification from `.specify/specs/023-agent-framework-redesign/requirements.md`

## Summary

Refactor the Agent framework across **code and documentation** so a single conceptual model governs everything: each Agent is described by **Role × Stage × Type**, organized statically as a **Team** (Role × Stage matrix) and dynamically as a **Loop**. All agent operations stay behind the single `/speckit.agents` entry point (no new commands), which recognizes intent and delegates to the `create-agent` and `organize-agents` skills. The redesign unifies terminology (**SubRole → Stage**, **improver → optimizer**), merges **Meta-Coordinator + Team Supervisor → a single Team Supervisor (Meta role)**, consolidates templates under the `create-agent` skill (removing stale duplicates), migrates existing persisted agents, and regenerates `docs/agents`. It also folds in a cross-project research deliverable mining `/cws_work/*` sibling projects.

## Technical Context

**Language/Version**: Python 3.11+ (CLI in `src/specify_cli`), Markdown (templates/skills/docs/commands), Bash (`.specify/scripts/bash`)  
**Primary Dependencies**: Typer (CLI), pytest (tests); no runtime services or network  
**Storage**: Filesystem only — Markdown templates, `.agent.md` files under `.specify/agents/`, tool symlinks (`.qoder/agents` → `.specify/agents`)  
**Testing**: pytest (`tests/contract`, `tests/integration`, `tests/unit`) + structural Markdown scenario validation (`tests/scenarios/`) + a new deprecated-term / reference-integrity guard  
**Target Platform**: Local developer CLI, cross-platform (Linux/macOS)  
**Project Type**: single — code generator / framework (authoring-time tooling)  
**Performance Goals**: N/A (authoring-time; no runtime hot path)  
**Constraints**: 0 live references to "SubRole"/"improver"; 0 broken template references; single canonical template location; approved-provider whitelist preserved  
**Scale/Scope**: ~16 source templates, 3 agent skills, 1 command, 3 `docs/agents` files, 6 persisted role agents + workspace files, orchestration scenario tests, installed mirrors under `.specify/`

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every change traces to FR-001…FR-021; plan derived from `requirements.md` |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 019 (Agents Command); `feature-ref.md` + features/019.md evolution note updated |
| III | Intent-Driven Development | ✅ Pass | Conceptual model + contracts express what/why; `/speckit.agents` is intent-driven |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Contracts authored in Phase 1; tasks update pytest + scenario tests and add a deprecated-term guard before edits |
| V | AI Agent Integration Standards | ✅ Pass | Approved-provider whitelist preserved; FR-012 covers all officially supported tools |
| VI | Continuous Quality & Observability | ✅ Pass | Docs regenerated, YAGNI (no new command), migration notes recorded, CI/pytest must pass |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following the workflow; Feature Index re-evaluated at this phase |

**Gates Status**: ✅ All gates pass — no violations.

**Re-check after Phase 1**: 2026-07-10 — Re-evaluated against `data-model.md`, `contracts/`, `quickstart.md`; all rows remain ✅ Pass. No new complexity introduced (rename/merge/terminology only; no new command, no new runtime dependency).

## Project Structure

### Documentation (this spec)

```text
.specify/specs/023-agent-framework-redesign/
├── plan.md              # This file
├── research.md          # FR-021 deliverable — consolidated cross-project findings (produced in implement phase)
├── data-model.md        # Phase 1 — conceptual model entities + migration map
├── quickstart.md        # Phase 1 — validation walkthrough
├── contracts/           # Phase 1 — behavioral contracts (see below)
│   ├── conceptual-model-contract.md
│   ├── agents-command-contract.md
│   └── template-migration-contract.md
├── feature-ref.md       # Phase 1 — Feature 019 linkage
├── checklists/          # requirements.md quality checklist (from /speckit.requirements)
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md      # Implementation output (/speckit.implement)
```

Phase 0 planning findings are inlined below (< 50 lines, fully resolved from repo). The standalone `research.md` slot is reserved for the **FR-021 cross-project research deliverable**, not for planning research.

### Source Code (repository root)

```text
templates/commands/agents.md               # Single-entry /speckit.agents source: intent→capability; Team Supervisor merge
skills/create-agent/SKILL.md               # Authoring skill: add Role/Stage/Type model; new stage/role names
skills/create-agent/templates/             # Canonical template home: rename stages, merge supervisor, add model headers
skills/create-agent/references/            # Supporting references (terminology-aligned)
skills/improve-agent/SKILL.md              # Terminology alignment (improver→optimizer, subrole→stage)
skills/organize-agents/SKILL.md            # Team Loop: merge Supervisor+Meta-Coordinator→Team Supervisor; terminology
docs/agents/                               # design.md (done), eei-triad-pattern.md, multi-agent-orchestration.md → model+terms
docs/commands/agents.md                    # Command doc aligned to single-entry + model
tests/scenarios/multi-agent-orchestration/ # team-loop/serial/parallel scenarios: terminology + supervisor merge
tests/                                      # add deprecated-term / reference-integrity guard; update affected tests
.specify/agents/                           # Migrate persisted role agents + AGENTS.md (FR-020)
.specify/templates/                        # Remove stale agent-* duplicates (canonicalize to create-agent skill)
.specify/skills/                           # Re-sync installed mirror of create-agent/improve-agent/organize-agents
.specify/memory/features.md                # Feature 019 index update (Last Updated + note)
.specify/memory/features/019.md            # Feature 019 evolution note for spec 023
```

**Structure Decision**: This spec extends the existing **code-generator / framework** shape. It does NOT add top-level directories or a new command. The canonical template location is confirmed as `skills/create-agent/templates/` (source) with its installed mirror `.specify/skills/create-agent/templates/`; the legacy `.specify/templates/agent-*` duplicates are removed to eliminate the "scattered templates" problem. All work is rename/merge/terminology/model-doc plus persisted-agent migration and installed-mirror re-sync.

## Phase 0: Research Review & Context (inlined)

**Findings from repo + memory (no unknowns remain):**

1. **Templates already consolidated** under `skills/create-agent/templates/` (16 files). Root `templates/` has no `agent-*`. FR-013 is therefore mostly satisfied; remaining work = remove stale `.specify/templates/agent-*` duplicates and fix references (FR-016).
2. **Deprecated-term footprint (live, excluding specs/CHANGELOG/draft)**: `subrole` and `improver` appear in create-agent/improve-agent SKILLs, stage templates, supervision/triad templates, `docs/agents/*`, `tests/scenarios/.../team-loop-scenario.md`, persisted `.specify/agents/*.agent.md`, and installed `.specify/` mirrors. `draft/` is out of scope (archived proposals).
3. **Supervisor merge is a real change**: `organize-agents` Team Loop currently has 3 layers (Supervisor + Meta-Coordinator + Workers) with templates `agent-role-meta-coordinator-template.md` + `agent-team-supervisor-template.md`. Design mandates a single **Team Supervisor** (Meta) absorbing coordination + supervision.
4. **Role set discrepancy**: design matrix lists 7 workers incl. **UX Analyst**, but only 6 worker role templates exist (no UX Analyst). See Decision D1.
5. **Model not documented as first-class**: neither skill states Role/Stage/Type or Team/Loop explicitly; a canonical concept section is needed (docs + create-agent SKILL).
6. **FR-021 research** is a product deliverable (mine `/cws_work/*` for best practices, one agent per project) — scheduled for the implement phase via `organize-agents` parallel dispatch, output to this spec's `research.md`. It is not a planning blocker.

### Decisions & Assumptions

- **D1 — UX Analyst**: The design matrix lists UX Analyst, but requirements FRs do not mandate role-set expansion. **Decision**: keep the existing 6 worker roles for this refactor and treat UX Analyst as an illustrative/aspirational matrix entry; adding an `agent-role-ux-analyst-template.md` is **deferred** (documented, not silently dropped). Rationale: avoids scope creep; the matrix's Type/Stage rules apply identically to any future role.
  > **Superseded (2026-07-10, commit `d87dfca9`)** — This deferral **no longer holds**. A follow-up change promoted UX Analyst to a built-in **seventh Worker role**, adding `skills/create-agent/templates/agent-role-ux-analyst-template.md` and the persisted agent `.specify/agents/ux-analyst.agent.md`. Its scope covers **all user interfaces** — front-end/GUI pages, CLI design, and `/command` + skill interaction surfaces. The original decision text above is retained unchanged as immutable history; this annotation records the reversal. See `docs/agents/design.md`.
- **D2 — Supervisor merge**: Merge `agent-role-meta-coordinator-template.md` + `agent-team-supervisor-template.md` → `agent-role-team-supervisor-template.md` (Meta role, Meta at all stages). Update `organize-agents` Team Loop to 2 layers (Team Supervisor + Workers). All references to "Meta-Coordinator" resolve to Team Supervisor.
- **D3 — Canonical template location**: `skills/create-agent/templates/` is the single source of truth; `.specify/skills/create-agent/templates/` is its installed mirror. Legacy `.specify/templates/agent-*` files are removed. All references (command, skills, tests, docs) point to the canonical location.
- **D4 — Feature status**: Feature 019 is already `Implemented`; this refactor is an evolution under it. **Do NOT regress status**. Keep `Implemented`, update `Last Updated`, and append a spec-023 evolution note (per feature-integration guidance, `/speckit.plan` never lands `Implemented`, and here it must not downgrade either).
- **D5 — History exclusion**: `draft/`, `CHANGELOG`, prior `.specify/specs/*`, and historical narrative in `features/019.md` "Latest Evolution" are immutable history — excluded from the zero-reference requirement (SC-002). A new evolution note is additive.

## Phase 1: Design & Contracts

**Artifacts generated in this phase:**

- `data-model.md` — Entities (Agent, Role, Stage, Type, Team, Loop, AgentTemplate, ResearchFindings), the Role × Stage × Type matrix, Type-follows-Stage rule, template naming scheme, and the old→new migration map.
- `contracts/conceptual-model-contract.md` — Normative definitions of Role/Stage/Type/Team/Loop and the Type-follows-Stage coupling.
- `contracts/agents-command-contract.md` — `/speckit.agents` single-entry intent→capability routing contract (create / organize / execute; ambiguous-intent behavior).
- `contracts/template-migration-contract.md` — Normative rename/merge map, terminology substitution rules, canonical-location + reference-integrity rules, persisted-agent migration rules.
- `quickstart.md` — Executable validation walkthrough mapping to SC-001…SC-009.
- `feature-ref.md` — Feature 019 linkage record.

**Feature Integration**: Update `.specify/memory/features/019.md` (evolution note: spec 023 planned) and `.specify/memory/features.md` (Last Updated → 2026-07-10). Status stays `Implemented` per Decision D4.

## Complexity Tracking

N/A — Constitution Check has no Fail/Partial rows.
