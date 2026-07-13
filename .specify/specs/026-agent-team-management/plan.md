# Implementation Plan: Agent Team Management

**Branch**: `026-agent-team-management` | **Date**: 2026-07-13 | **Spec**: [requirements.md](./requirements.md)
**Input**: Specification from `.specify/specs/026-agent-team-management/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Introduce a first-class **team** domain that owns everything multi-agent, mirroring how the single-agent domain works today. A new command `/speckit.team` becomes the sole entry point for team work with **three modes** — **create**, **modify**, and **run** — routing to two skills: `create-team` (the renamed `organize-agents`, which also owns execution) and `improve-team` (new). The multi-agent **Conceptual Model** and the inherently multi-agent authoring constructs (EEI **triad**, **team-supervisor**, and all orchestration templates) move out of `create-agent` into the team domain, leaving `create-agent`/`improve-agent` scoped to single agents. Teams persist as `.specify/teams/<slug>.team.md` so they can be re-opened, improved, and run across sessions. The **run** mode first renders the team's static structure (Role×Stage×Type roster) and dynamic structure (pattern, parallelism, execution flow diagram), then executes **only after explicit user confirmation**.

## Technical Context

**Language/Version**: Python `>=3.8` (CLI, scripts, tests) + Markdown (commands, skills, docs, templates)
**Primary Dependencies**: `typer`, `rich`, `httpx` (CLI runtime — unchanged); no new runtime deps
**Storage**: Files only. New canonical store `.specify/teams/<slug>.team.md` (Markdown + YAML frontmatter). No per-tool symlinks for teams (teams are a framework concept, not a tool-native artifact).
**Testing**: `pytest` with `contract` / `integration` markers (existing suites under `tests/`)
**Target Platform**: Local developer CLI across supported agents (Tier 1/2 per Constitution V)
**Project Type**: Code generator / framework (templates + scripts + `src/specify_cli/`)
**Performance Goals**: N/A (interactive authoring/orchestration; no throughput target)
**Constraints**: Backward-incompatible rename is acceptable (internal framework, no external consumers); no dangling `organize-agents` references may remain in active (non-archived) paths
**Scale/Scope**: ~1 new command source + per-tool generated command files; 1 skill rename + 1 new skill; template relocation (7 files) + 1 extracted reference; doc + registry + test updates

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every change traces to FR-001…FR-017 in `requirements.md`; artifacts drive the rename/move |
| II | Feature-Centric Development | ✅ Pass | New Feature **027 Team Management** registered; status advanced Draft→Planned; detail file created |
| III | Intent-Driven Development | ✅ Pass | Plan states WHAT/WHY per FR set; command routing expresses user intent (create/modify/run) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Contracts in `contracts/`; guard tests planned (no `organize-agents` refs; single Conceptual Model; NON_DECLARABLE updated) authored before impl in `/speckit.tasks` |
| V | AI Agent Integration Standards | ✅ Pass | No provider list change; new command generated for all supported tools via existing `_ASSISTANT_COMMAND_DIRS` mechanism |
| VI | Continuous Quality & Observability | ✅ Pass | Hard rename with breaking-change note; team persistence justified by improve/run (not speculative); docs updated; YAGNI honored (2 skills, reuse orchestration engine) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following requirements→clarify→plan→tasks→implement; feature re-validated this phase |

**Gates Status**: ✅ All gates pass. No Fail/Partial rows → Complexity Tracking = N/A.

**Re-check after Phase 1**: 2026-07-13 — Re-evaluated against `data-model.md` and `contracts/`. All rows remain ✅ Pass; the design introduces no new principle violations (teams are file-based, no new providers, no new runtime deps).

## Project Structure

### Documentation (this spec)

```text
.specify/specs/026-agent-team-management/
├── plan.md              # This file
├── data-model.md        # Phase 1 — Team/TeamMember/TeamConfiguration + template classification
├── quickstart.md        # Phase 1 — end-to-end create/modify/run walkthrough
├── contracts/           # Phase 1 — command + 2 skill contracts + migration contract
│   ├── team-command-contract.md
│   ├── create-team-skill-contract.md
│   ├── improve-team-skill-contract.md
│   └── team-migration-contract.md
├── feature-ref.md       # Phase 1 — feature linkage record (027)
├── checklists/requirements.md   # from /speckit.requirements + /speckit.clarify
└── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
```

No standalone `research.md` — Phase 0 findings are internal (project docs + code) and inlined below (§ Phase 0).

### Source Code (repository root)

```text
templates/commands/team.md                       # NEW — source for /speckit.team (3 modes: create/modify/run)
skills/create-team/                               # RENAMED from skills/organize-agents/ (owns create + run/execute)
skills/create-team/references/conceptual-model.md # NEW — extracted Conceptual Model (single source of truth)
skills/create-team/templates/                     # NEW — receives moved multi-agent templates (see data-model)
skills/improve-team/SKILL.md                      # NEW — refine/optimize an existing team
skills/create-agent/                              # EDIT — remove Conceptual Model; drop triad/team-supervisor/orchestration
skills/improve-agent/SKILL.md                     # EDIT — drop Triad/orchestration refinement (moves to improve-team)
skills/create-skills/SKILL.md                     # EDIT — update non-declarable skill list
docs/commands/team.md                             # NEW — /speckit.team user doc
docs/agents/  (+ docs/teams or reuse)             # EDIT — repoint Conceptual Model + orchestration ownership to team domain
tests/contract/                                   # EDIT/NEW — guard tests (rename, single Conceptual Model, NON_DECLARABLE)
.specify/teams/                                   # NEW canonical runtime store for persisted teams (created on first use)
.specify/memory/features.md + features/027.md     # EDIT/NEW — feature registration (done this phase)
```

**Structure Decision**: This spec extends the existing **code-generator/framework** layout. It adds one command source under `templates/commands/`, renames one skill directory and adds one new skill under `skills/`, relocates a defined set of `agent-*` templates from `skills/create-agent/templates/` into a new `skills/create-team/templates/`, and introduces one new top-level runtime directory `.specify/teams/` (canonical team store, no symlinks). All per-tool command/skill copies are regenerated by the existing install/instructions mechanism — no new bespoke wiring.

## Phase 0: Research Review & Context (inlined)

**Decisions resolved from project docs + code (no external research needed):**

1. **Command wiring** — Commands are discovered from `templates/commands/*.md` and rendered per tool via `_ASSISTANT_COMMAND_DIRS` in `src/specify_cli/__init__.py` (command stems scanned from `speckit.*` files; no hardcoded command allow-list). *Decision*: add `templates/commands/team.md`; per-tool files (`.qoder/commands/`, `.claude/commands/`, `.github/prompts/`, `.opencode/command/`, `.qwen/…`, etc.) are regenerated by init/instructions.
2. **Skill packaging** — Skills live at `skills/<slug>/SKILL.md` (frontmatter `name`/`description`/`skill_id`), mirrored to `.specify/skills/` on install; `.github/skills` is a symlink. *Decision*: rename dir `organize-agents`→`create-team` (update `name`, `description`, `skill_id`); add `skills/improve-team/SKILL.md`.
3. **Conceptual Model source** — Embedded in `skills/create-agent/SKILL.md` (§ Conceptual Model) and documented in `docs/agents/design.md`. *Decision*: extract the skill-level definition to `skills/create-team/references/conceptual-model.md` (single source of truth for the team domain); `create-agent` links to it instead of embedding; `docs/agents/design.md` remains the doc-level authority and repoints ownership to the team domain.
4. **Template classification** — Inventory of `skills/create-agent/templates/` classified into *stay (single-agent)* vs *move (team)* — see `data-model.md` § Template Classification. Triad stages + triad orchestration + team-supervisor + parallel/serial orchestration + workflow schema **move**; the 7 role templates, `agent-supervision-delegation.md`, `agent-skill-enablement.md`, and `agent-project-custom-template.md` **stay**.
5. **Execution ownership** — `organize-agents` already performs runtime orchestration (dispatch/monitor/loop). *Decision*: `create-team` inherits execution; `/speckit.team run` invokes it behind a mandatory static+dynamic **preview + confirm** gate (per user planning input and FR-017).
6. **Team persistence** — improve/run require an "existing team". *Decision*: persist as `.specify/teams/<slug>.team.md`; no per-tool symlink (framework-internal). Ephemeral one-shot orchestration remains possible (create-then-run without persist), but a persisted team is the target for `modify`/`run`.
7. **Impacted guards** — `tests/contract/test_agent_skill_enablement.py` `NON_DECLARABLE` set and `skills/create-skills/SKILL.md` non-declarable list reference `organize-agents`; `.specify/instructions.md` carries skill inventory. *Decision*: update the NON_DECLARABLE set and non-declarable lists to `create-team`/`improve-team`; regenerate instructions.

**Phase 0 output**: Technical Context above is fully resolved; no `NEEDS CLARIFICATION` remain.

## Phase 1: Design & Contracts

Generated in this run:

- **data-model.md** — `Team`, `TeamMember`, `TeamConfiguration` entities; the `.team.md` file schema; the static (Role×Stage×Type) and dynamic (pattern/parallelism/flow) structures; and the full template-relocation classification table.
- **contracts/team-command-contract.md** — `/speckit.team` 3-mode contract (create/modify/run), intent routing, and the run-mode preview→confirm→execute gate.
- **contracts/create-team-skill-contract.md** — create-team inputs/outputs (define + persist + execute), inherited orchestration patterns.
- **contracts/improve-team-skill-contract.md** — improve-team evidence-based, targeted, structure-preserving edits; "team not found" behavior.
- **contracts/team-migration-contract.md** — the rename, Conceptual Model extraction, template moves, reference/registry/test updates, and the zero-dangling-reference guarantee.
- **quickstart.md** — create → modify → run walkthrough including the confirmation gate.

**Post-design Constitution re-check**: ✅ All gates still pass (see table above).

## Complexity Tracking

N/A — no Constitution Check violations.
