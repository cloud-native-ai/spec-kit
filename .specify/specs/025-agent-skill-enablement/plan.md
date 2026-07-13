# Implementation Plan: Agent Skill Enablement

**Branch**: `025-agent-skill-enablement` | **Date**: 2026-07-13 | **Spec**: [requirements.md](./requirements.md)
**Input**: Specification from `.specify/specs/025-agent-skill-enablement/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Wire framework skills into the seven built-in role agents so each one prefers a role-relevant installed skill over improvising the same operation. Since skills and agent definitions install together, every agent can already invoke any installed skill; this feature makes that intent explicit and consistent by (1) adding a `skills:` frontmatter list to each shipped agent, (2) adding a uniform "Skill Enablement" body section (single-source protocol + per-role skill table with when-to-use and fallback), (3) mirroring the same additions into the matching `create-agent` role templates so regenerated agents inherit the behavior, and (4) adding a contract test that proves every declared skill exists in the installed skill set. This is a documentation/template change to Markdown agent definitions — no CLI runtime code changes.

## Technical Context

**Language/Version**: Markdown agent definitions + YAML frontmatter (no Python runtime change); repo tooling is Python >=3.8  
**Primary Dependencies**: Existing agent framework (`.specify/agents/`, `skills/create-agent/templates/`), installed skills under `.specify/skills/`; pytest for validation  
**Storage**: Files only — `agents/*.agent.md`, `skills/create-agent/templates/agent-role-*-template.md`, shared reference snippet  
**Testing**: pytest (`contract` marker) — reuse the pattern in `tests/contract/test_shipped_agent_presets.py`  
**Target Platform**: Spec Kit workspace consumed by supported AI agents (Tier 1/2)  
**Project Type**: Code generator / framework (templates + scripts + `src/specify_cli`)  
**Performance Goals**: N/A (static definition change)  
**Constraints**: Zero regression to existing frontmatter fields, supervision/EEI loops, role scope, and per-file symlink model; skill references MUST be a subset of installed skills (zero dangling references)  
**Scale/Scope**: 7 built-in role agents; 7 matching role templates; 1 shared reference snippet; 1 new contract test; ~19 installed skills as the reference set

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Every design element traces to FR-001…FR-012 / SC-001…SC-005 in `requirements.md`; see `contracts/agent-skill-enablement-contract.md` traceability. |
| II | Feature-Centric Development | ✅ Pass | Bound to Feature 026; `features.md` + `features/026.md` updated; status advances Draft → Planned. |
| III | Intent-Driven Development | ✅ Pass | Spec defines WHAT/WHY (role-relevant skill preference); plan maps to concrete Markdown/template design. |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | `contracts/agent-skill-enablement-contract.md` defines normative rules; a failing contract test (skill-refs ⊆ installed set, each agent ≥1 skill) is authored before edits. |
| V | AI Agent Integration Standards | ✅ Pass | No new providers; only existing agent defs/templates edited; provider whitelist and per-file symlink model unchanged. |
| VI | Continuous Quality & Observability | ✅ Pass | Minimal, YAGNI-aligned change; single-source shared snippet avoids drift; docs updated; CI tests pass. |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Following spec → plan → tasks → implement; Feature Index re-evaluated this phase. |

**Gates Status**: ✅ All gates pass — no violations, Complexity Tracking = N/A.

**Re-check after Phase 1**: 2026-07-13 — Re-evaluated against generated `data-model.md`, `contracts/`, and `quickstart.md`; all seven principles remain ✅ Pass. No new complexity introduced.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/025-agent-skill-enablement/
├── plan.md              # This file (/speckit.plan command output)
├── requirements.md      # Input specification (clarified)
├── data-model.md        # Phase 1 output — entities + Agent↔Skill mapping table
├── quickstart.md        # Phase 1 output — how to verify skill enablement end to end
├── contracts/           # Phase 1 output — agent-skill-enablement contract
│   └── agent-skill-enablement-contract.md
├── checklists/
│   └── requirements.md  # From /speckit.requirements
├── tasks.md             # Phase 2 output (/speckit.tasks — NOT created here)
└── verification.md      # Implementation output (/speckit.implement)
```

No standalone `research.md` — Phase 0 findings are brief and internal; inlined below under "Phase 0: Research Review".

### Source Code (repository root)

```text
agents/                                      # 7 shipped role agents — add `skills:` frontmatter + "## Skill Enablement" section to each
skills/create-agent/templates/               # 7 agent-role-*-template.md — mirror the same additions so regenerated agents inherit skill enablement
skills/create-agent/templates/               # add agent-skill-enablement.md — single-source skill-preference protocol snippet (composed like agent-supervision-delegation.md)
tests/contract/                              # add test_agent_skill_enablement.py — assert each preset declares ≥1 skill and all refs ⊆ installed skills
docs/agents/                                 # update command-and-skills.md / design.md to document the skill-enablement convention
```

**Structure Decision**: Extends the existing agent framework (a code generator / framework). The canonical source of built-in agents is `agents/*.agent.md` (mirrored to `.specify/agents/` on install); their generators are `skills/create-agent/templates/agent-role-*-template.md`. This spec edits both in lockstep, introduces one shared reference snippet (`agent-skill-enablement.md`) as the single source for the skill-preference protocol, and adds one contract test. No new top-level directory; no `src/specify_cli` change.

## Phase 0: Research Review

Findings (inlined; internal investigation only):

- **`skills:` frontmatter is supported but unused.** `docs/agents/command-and-skills.md` lists `skills` among supported agent frontmatter fields; `grep` confirms no agent or template currently sets it. Decision: use the existing `skills:` field (YAML list of canonical skill slugs) — no new schema invented (satisfies FR-006, FR-009, "consistency baseline" assumption).
- **Two edit surfaces exist and must stay in lockstep.** Built-in agents live in `agents/` (shipped, mirrored to `.specify/agents/`); their generators live in `skills/create-agent/templates/agent-role-*-template.md`. Decision: edit both so a regenerated agent is not a regression (FR-011).
- **Single-source guidance pattern already exists.** `agent-supervision-delegation.md` is composed into supervisors at generation time rather than copy-pasted. Decision: add `agent-skill-enablement.md` as the single-source protocol text; each agent's per-role skill table is the only per-agent-varying part (FR-009).
- **Existing contract test is non-blocking for this change.** `tests/contract/test_shipped_agent_presets.py` only asserts presence of `name/description/model/tools/maxTurns`; adding `skills:` does not break it. Decision: add a dedicated `test_agent_skill_enablement.py` that fails first (Principle IV).
- **Reference-only skills are excluded from declarations.** `sdd-workflow` is documented as "NOT invoked directly." Meta skills (`create-agent`, `improve-agent`, `create-skills`, `improve-skills`, `organize-agents`) belong to `/speckit.agents` and `/speckit.skills` workflows, not role-agent operations. Decision: exclude both classes from role `skills:` lists to keep the mapping meaningful (FR-004).

No unresolved `NEEDS CLARIFICATION` remain; Technical Context is fully populated.

## Complexity Tracking

N/A — Constitution Check has no violations.
