# Implementation Plan: EEI Agent Triad

**Branch**: `022-eei-agent-triad` | **Date**: 2026-07-02 | **Spec**: [requirements.md](requirements.md)
**Input**: Specification from `.specify/specs/022-eei-agent-triad/requirements.md`

## Summary

Add the Executor-Evaluator-Improver (EEI) triad pattern to the existing Role-Based Agent architecture. The triad adds a second dimension to agent design: within any role, work can be decomposed into three independent sub-agents (Executor, Evaluator, Improver) that operate in a quality-gated iterative loop. Implementation consists of: (1) three new sub-role agent templates, (2) a triad orchestration prompt template, (3) updates to create-agent and improve-agent skills to support triad creation, and (4) a reference guide documenting the pattern.

> **⚠️ Plan Amendment (2026-07-02) — see [§ Plan Amendment](#plan-amendment-2026-07-02--supervisor--general-skill-refactor) at the end of this document.** The original plan above (Phases 0–1) shipped the four EEI templates and the initial skill sections. The amendment supersedes the *integration* strategy: role agents become role-scoped **supervisors** that dynamically spawn their own EEI triad, `create-agent`/`improve-agent` become **general-purpose authoring skills**, and `/speckit.agents` is refactored to **delegate** to those skills instead of inlining generation logic. New/changed design artifacts for the amendment are called out in that section.

## Technical Context

**Language/Version**: N/A — this is a template/prompt engineering feature, not runtime code  
**Primary Dependencies**: Existing agent template system (`templates/agent-role-*-template.md`), create-agent skill, improve-agent skill  
**Storage**: Filesystem — `.specify/agents/` directory for generated agents, `templates/` for templates  
**Testing**: Contract tests verifying template rendering; integration test applying the triad to a sample task  
**Target Platform**: All supported AI agents (Claude Code, Copilot, Qwen, opencode, Qoder)  
**Project Type**: Template/prompt system (extends existing `templates/` + `skills/` directories)  
**Performance Goals**: N/A — template rendering is near-instantaneous  
**Constraints**: Templates must follow existing YAML frontmatter + Markdown body format; must compose with all 6 existing role templates  
**Scale/Scope**: 3 new sub-role templates, 1 orchestration template, 2 skill updates, 1 reference guide

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Spec `022-eei-agent-triad/requirements.md` drives all template design; 12 FRs trace to 5 user stories |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 019 (Agents Command); feature index updated |
| III | Intent-Driven Development | ✅ Pass | Pattern derived from real session experience (K8s diagram 49→91); intent documented in Context & Motivation |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Contract defined for triad orchestration protocol; test scenarios in US1-US5 acceptance criteria |
| V | AI Agent Integration Standards | ✅ Pass | Templates target all Tier 1 agents; sub-role templates follow existing `agent-role-*-template.md` format |
| VI | Continuous Quality & Observability | ✅ Pass | FR-007 requires iteration history tracking; FR-005 requires structured scoring output |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Full SDD workflow followed: requirements → clarify → plan → tasks → implement |

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/022-eei-agent-triad/
├── requirements.md          # Feature specification
├── plan.md                  # This file
├── data-model.md            # Triad entity model
├── contracts/               # Orchestration protocol contracts
│   └── triad-protocol.md    # EEI loop protocol specification
├── quickstart.md            # How to create and use an EEI triad
├── checklists/
│   └── requirements.md      # Spec quality checklist
└── tasks.md                 # Task breakdown (via /speckit.tasks)
```

No standalone research.md — findings inlined below (pattern fully understood from session experience).

### Source Code (repository root)

```text
templates/                                    # New sub-role templates
├── agent-subrole-executor-template.md        # Executor sub-role template
├── agent-subrole-evaluator-template.md       # Evaluator sub-role template
├── agent-subrole-improver-template.md        # Improver sub-role template
└── agent-triad-orchestration-template.md     # Orchestration prompt template

skills/create-agent/                          # Updated skill
└── SKILL.md                                  # Add triad creation support

skills/improve-agent/                         # Updated skill
└── SKILL.md                                  # Add triad improvement support

docs/                                         # Reference documentation
└── eei-triad-pattern.md                      # Pattern guide with examples
```

**Structure Decision**: Extends the existing agent template system by adding 3 sub-role templates (`agent-subrole-*`) alongside the 6 existing role templates (`agent-role-*`). The `subrole` prefix distinguishes them from role-level templates. One orchestration template provides the loop scaffold. No new top-level directories.

## Complexity Tracking

N/A — no constitution violations.

## Phase 0: Research Review

### Findings from Session Experience

The K8s diagram optimization session (17 rounds, score 49→91) provided complete empirical evidence:

**What worked:**
- Independent subagent invocation (no shared context) → clean evaluation
- Evaluator receiving ONLY output artifacts (PNG) → unbiased scoring
- Improver modifying skill reference files → environment improvement persists across iterations
- Structured scoring output (per-dimension + weighted total + suggestions) → actionable feedback
- Grouping arrows by semantic category in prompts → better executor output quality

**What didn't work:**
- Re-scoring the same output hoping for a higher score → waste of tokens
- Adding notes/elements to "help" the evaluator → often hurt aesthetics score
- Switching layout direction mid-loop without clear evidence → caused regressions

**Key design decisions:**
- The orchestrator (main agent) manages the loop, NOT the sub-agents themselves
- Each sub-agent is a fresh invocation with no memory of prior rounds
- The improver's changes to files persist on disk, so the executor naturally picks them up
- Scoring variability of ±3 points is inherent to LLM-based evaluation; the loop handles this by tracking the best score

## Phase 1: Design & Contracts

### Data Model

See [data-model.md](data-model.md) for full entity definitions.

### Contracts

See [contracts/triad-protocol.md](contracts/triad-protocol.md) for the orchestration protocol.

### Quickstart

See [quickstart.md](quickstart.md) for usage guide.

---

## Plan Amendment (2026-07-02) — Supervisor + General-Skill Refactor

**Trigger**: User directive — *"需要将这个 agent 的重构也更新到 skills/create-agent 和 skills/improve-agent 技能中"*, clarified to four goals:

1. Each role-based agent is a **role-scoped supervisor** that dynamically creates multiple subagents according to the EEI triad design.
2. `create-agent` and `improve-agent` (and other agent-related skills) are **general-purpose** skills, not role-only.
3. The `/speckit.agents` command **invokes** the general `create-agent` / `improve-agent` skills to produce both role-based and EEI-triad agents.
4. `create-agent` / `improve-agent` gain the **customization capability** to author these advanced (supervisor + triad) agents.

**Scope decision**: Amend Feature 022 in place (no new branch). The destructive `create-new-plan.sh` was intentionally **not** run so the original `plan.md` history is preserved; this section is additive.

### A. Problem Statement (why the original integration is insufficient)

The 022 implementation created the four EEI templates and bolted a "Triad Mode" onto `create-agent` and a "Triad Refinement" onto `improve-agent`, but left three structural gaps:

| Gap | Evidence (current state @ commit 0bf2a9a) | Consequence |
|-----|-------------------------------------------|-------------|
| **G1 — Role and triad are disjoint dimensions** | `templates/agent-role-*-template.md` have no supervision/delegation section; `templates/agent-triad-orchestration-template.md` is standalone and role-agnostic | A generated role agent (e.g. `system-designer.agent.md`) cannot spin up its own quality loop; the two "dimensions" never meet in a single artifact |
| **G2 — `/speckit.agents` inlines authoring; skills are a parallel path** | `templates/commands/agents.md` Mode A (lines 47–93) renders role templates directly; Mode B (lines 97–206) writes `.agent.md` inline — neither calls `create-agent` | Two authoring engines drift apart (the review already flagged runtime/skill drift); triad creation lives only in the skill and is unreachable from the command |
| **G3 — Skills are framed as "role-based only"** | `skills/create-agent/SKILL.md:11` Goal: *"Create a new role-based agent template"*; `skills/improve-agent/SKILL.md:17` resolves target to *"exactly one `templates/agent-role-*-template.md` file"* | The skills cannot uniformly author/refine supervisors, sub-roles, orchestration prompts, or custom agents; "customization capability" (goal 4) has no home |

### B. Technical Context (delta)

| Field | Value |
|-------|-------|
| **Project Type** | Unchanged — template/prompt engineering; **no runtime code** (aligns with the "no DFX over-design" constraint: supervision is achieved via prompt instructions, not an orchestration runtime) |
| **Primary targets** | `templates/commands/agents.md`; `skills/create-agent/SKILL.md`; `skills/improve-agent/SKILL.md`; the six `templates/agent-role-*-template.md`; `templates/agent-triad-orchestration-template.md` |
| **New template concept** | A shared **"Supervision & EEI Delegation"** section injected into role templates (single source, referenced — not copy-pasted per role) |
| **Authoring engine** | `create-agent` / `improve-agent` become the single authoring engine; `/speckit.agents` becomes a thin orchestrator that gathers project context and delegates |
| **Runtime mirror** | Any edited `templates/` or `skills/` file MUST be mirrored to `.specify/templates/` / `.specify/skills/` (addresses review finding F4) |
| **NEEDS CLARIFICATION** | Whether Mode A should embed the triad in **every** role by default, or only when the role is flagged `supervisor: true` (see Open Question OQ-1 below) |

### C. Constitution Check (re-derived from `.specify/memory/constitution.md` v1.2.0)

| # | Principle | Compliance | Evidence / Note |
|---|-----------|------------|-----------------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Amendment traces to the four clarified goals; each design decision D1–D5 below maps to a goal |
| II | Feature-Centric Development | ✅ Pass | Remains under Feature 019; registry note added; no new feature split required |
| III | Intent-Driven Development | ✅ Pass | Amendment expresses the "what/why" (unify role+triad, single authoring engine) before the "how" |
| IV | Test-First & Contract-Driven Implementation | ⚠️ Partial | Template/prompt feature with no runtime code — automated tests remain N/A (see Complexity Tracking); validation is structural + reference-session based. Contract for skill invocation is defined in `contracts/agent-authoring-contract.md` |
| V | AI Agent Integration Standards | ✅ Pass | No provider-list change; the existing per-agent detection tables in both skills are preserved and generalized |
| VI | Continuous Quality & Observability | ✅ Pass | Delegation removes the duplicate authoring path (G2), reducing drift; changes reflected in specs/plan/docs |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | This amendment is the Planning phase; handoff to `/speckit.tasks` follows |

**Gate result**: Pass with one justified Partial (Principle IV) recorded under Complexity Tracking.

### D. Design Decisions

- **D1 — Role agents become role-scoped supervisors** *(goal 1)*. Add a shared **"Supervision & EEI Delegation"** section to each `templates/agent-role-*-template.md`. It instructs the role agent that, for any quality-gated deliverable, it MAY act as an orchestrator: spawn Executor/Evaluator/Improver **subagents whose task, environment paths, and scoring dimensions are bound to the role's domain** (e.g. the System Designer's executor drafts architecture, its evaluator scores on the role's own criteria). The subagents are instantiated from the existing `agent-subrole-*` + `agent-triad-orchestration` templates — no new sub-role templates are introduced. Default scoring dimensions are role-appropriate defaults the supervisor can override per task.

- **D2 — Generalize `create-agent`** *(goals 2 & 4)*. Reframe its Goal from "role-based agent template" to *"author any agent artifact — role, supervisor (role+embedded triad), triad sub-role, orchestration prompt, or custom `.agent.md`"*. Replace the single linear workflow with an explicit **capability/mode matrix** (Role · Supervisor · Triad · Custom) that shares one validation+report tail. The existing "Triad Mode" becomes one row of that matrix; a new **Supervisor** capability composes a role template with the delegation section from D1.

- **D3 — Generalize `improve-agent`** *(goals 2 & 4)*. Broaden the Input Contract target resolution from *only* `templates/agent-role-*` to any authored artifact: role template, `agent-subrole-*`, `agent-triad-orchestration-*`, or a generated `.specify/agents/*.agent.md`. Keep the existing "Triad Refinement" workflow as the triad-layer specialization; add a resolver step that classifies the target and routes to the matching refinement rules.

- **D4 — `/speckit.agents` delegates to the skills** *(goal 3)*. Refactor `templates/commands/agents.md` so Mode A and Mode B **call `create-agent`** as the authoring engine (and `improve-agent` for updates), passing gathered project context. The command retains responsibility for context-gathering, backup/preservation (FR-008/008a), symlink discoverability, and registry updates; it stops re-implementing template rendering. This makes the skills the single source of truth (closes G2).

- **D5 — Advanced-agent customization contract** *(goal 4)*. Define the input shape a caller passes to `create-agent` to request an advanced agent: `{ kind: role|supervisor|triad|custom, role_slug, task, scoring_dimensions[], threshold, max_iterations, environment_paths[], workspace_paths[] }`. Specified in `contracts/agent-authoring-contract.md`.

### E. Project Structure (files this amendment will change — planned, not yet executed)

```text
templates/
├── agent-role-*-template.md            # + shared "Supervision & EEI Delegation" section (D1) ×6
├── agent-triad-orchestration-template.md  # generalize {{ROLE_SCOPE}} binding for role supervisors (D1)
└── commands/agents.md                  # Mode A/B refactored to delegate to create-agent/improve-agent (D4)

skills/create-agent/SKILL.md            # generalize Goal + capability matrix + Supervisor capability (D2, D5)
skills/improve-agent/SKILL.md           # generalize target resolution + classify/route (D3)

.specify/templates/ , .specify/skills/  # mirror all of the above (runtime parity, review F4)

.specify/specs/022-eei-agent-triad/
├── plan.md                             # THIS amendment
├── data-model.md                       # + RoleSupervisor entity + Role↔Triad relationship
├── contracts/agent-authoring-contract.md  # NEW — skill invocation + advanced-agent request contract
└── quickstart.md                       # + Scenario: supervisor role via /speckit.agents → create-agent
```

**Structure decision**: No new template *files* for sub-roles — supervision is a *section* reused across the six role templates, and the triad reuses the existing four templates. The only new spec artifact is one contract document.

### F. Phase 0 (Amendment) — Findings

- The two authoring paths (command-inline vs skill) are the root cause of drift; consolidating on the skills is lower-risk than the reverse because skills already contain the triad logic.
- Supervision must be expressed as **prompt instructions**, not a scheduler, to stay within the framework's document/prompt scope (no runtime infrastructure).
- Role-scoping the triad requires one new binding (`{{ROLE_SCOPE}}` / role-default dimensions) in the orchestration template; everything else is reuse.

### G. Phase 1 (Amendment) — Artifacts

- `data-model.md`: add **RoleSupervisor** entity and the `Role 0..1 — 1 Triad` (optional embedded triad) relationship.
- `contracts/agent-authoring-contract.md` (**new**): the `/speckit.agents → create-agent/improve-agent` invocation contract and the advanced-agent request schema (D5).
- `quickstart.md`: add a scenario walking through `/speckit.agents` generating a **supervisor** role agent that runs its own EEI loop.

### H. Complexity Tracking

| Item | Why (Partial/deviation) | Justification |
|------|--------------------------|---------------|
| Principle IV — automated tests N/A | No runtime code; artifacts are Markdown templates/prompts | Validation is structural (valid frontmatter + required sections present) plus the documented K8s reference session; a pytest suite would assert nothing meaningful. Recorded here per the constitution's "any Partial needs a Complexity Tracking entry" rule. |

### I. Open Questions (carry into `/speckit.tasks` or `/speckit.clarify`)

- **OQ-1**: Does Mode A embed the EEI triad in **all six** roles by default, or only in roles marked `supervisor: true` in frontmatter? (Default-off is safer and cheaper; default-on maximizes the "every role is a supervisor" intent.) Recommend `supervisor: true` opt-in with the delegation section always present but dormant.
- **OQ-2**: Should the shared "Supervision & EEI Delegation" section be a literal include (single file transcluded) or a maintained copy per role template? (Include reduces drift but the current template system has no transclusion mechanism.)

**Resolution (via `/speckit.clarify`, 2026-07-02)**: OQ-1 → **default-on for all 6 roles** (`supervisor: true` default, `supervisor: false` opt-out). OQ-2 → **compose in create-agent** — one canonical snippet `templates/agent-supervision-delegation.md` inlined at generation; role templates carry only supervision metadata. (Contract R2's dormant-by-default assumption is superseded and should be updated on the next full plan regeneration.)

### J. Runtime Mirror Map (T033)

Every edited source file mirrors to a runtime counterpart in the same change (contract R3, review F4):

| Source | Runtime counterpart |
|--------|---------------------|
| `templates/agent-role-*-template.md` | `.specify/templates/agent-role-*-template.md` |
| `templates/agent-triad-orchestration-template.md` | `.specify/templates/agent-triad-orchestration-template.md` (was MISSING — created) |
| `templates/agent-subrole-*-template.md` | `.specify/templates/agent-subrole-*-template.md` (was MISSING — created) |
| `templates/agent-supervision-delegation.md` (new) | `.specify/templates/agent-supervision-delegation.md` |
| `skills/create-agent/SKILL.md` | `.specify/skills/create-agent/SKILL.md` |
| `skills/improve-agent/SKILL.md` | `.specify/skills/improve-agent/SKILL.md` |
| `templates/commands/agents.md` | `.claude/commands/speckit.agents.md` (installed runtime command) |
