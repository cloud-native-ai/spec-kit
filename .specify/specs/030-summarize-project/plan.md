# Implementation Plan: Visual Project Reporting — summarize-project Skill & analysis-project UML Enhancement

**Branch**: `030-summarize-project` | **Date**: 2026-07-18 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `030-summarize-project` → Feature 013 Skills Command
**Input**: Specification from `.specify/specs/030-summarize-project/requirements.md`

## Summary

Deliver visualization-driven project information collection and presentation as two workstreams sharing one rendering dependency (the `draw-plantuml` skill):

- **WS-A (new)**: Create `skills/summarize-project/` — a skill that collects project work items from workspace materials, decomposes them once into a hierarchical breakdown, renders that breakdown as a WBS chart and a Gantt chart (milestones, schedule, progress status) by delegating to `draw-plantuml`, and assembles one self-contained HTML report for external readers.
- **WS-B (enhancement)**: Extend `skills/analysis-project/` with UML diagramming actions so its report's primary views (structure, key flows, deployment topology) are expressed as standard UML diagrams rendered via `draw-plantuml`, while lightweight Mermaid sketches remain for secondary content and all existing analysis behavior is preserved.

No new runtime code: both workstreams are prompt-artifact skill packages, validated by structural contract tests. No standalone research.md — findings inlined below (all decisions resolve from internal sources: `skills/draw-plantuml/`, `skills/analysis-project/`, `.specify/memory/features/013.md`, constitution).

## Technical Context

**Language/Version**: N/A runtime — skills are prompt/document artifacts (`SKILL.md` + `references/`); contract tests are Python 3.8+ / pytest per the repo test suite.  
**Primary Dependencies**: `skills/draw-plantuml/` (delegation target: WBS `@startwbs` via `references/howto/13-wbs-diagram.md`, Gantt `@startgantt` via `references/howto/14-gantt-diagram.md`, UML diagram guides, `scripts/render-plantuml.sh`, output conventions in SKILL.md §输出要求); `templates/skills-template.md` and `skills/create-skills/` (authoring conventions); `${SKILL_HOME}` / `${SKILL_WORKDIR}` path idioms (spec 012); `.specify/instructions.md` skills registry.  
**Storage**: N/A — file-based skill packages under `skills/` (canonical) and `.specify/skills/` (mirror).  
**Testing**: pytest structural contract tests under `tests/contract/` (precedent: `test_create_skills_prompt_assets.py`, `test_portable_skill_creation.py`, `test_skill_home_workdir_template.py`).  
**Target Platform**: AI agent prompt surfaces (Qoder, Claude Code, Codex CLI, GitHub Copilot, Qwen Code, opencode, Hermes, iFlow) consuming installed skill packages.  
**Project Type**: Code generator / framework — prompt-artifact skill packages in the Spec Kit skills registry.  
**Performance Goals**: Agent-executed summary report delivered in a single session ≤10 minutes with ≤1 clarification round (SC-001); no runtime performance targets for document artifacts.  
**Constraints**: Framework-not-runtime (Constitution IX) — no rendering re-implementation, delegation to `draw-plantuml` only; canonical/mirror byte-equivalence between `skills/` and `.specify/skills/`; documentation naming per Constitution X; no regression to `analysis-project` existing workflow (FR-018).  
**Scale/Scope**: 1 new skill package (`summarize-project`), 1 enhanced skill package (`analysis-project`: SKILL.md edits + 1 new reference guide), 2 new contract test files, 1 registry update, mirror synchronization.

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | Plan is driven by `requirements.md` (US1–US4, FR-001…FR-019, SC-001…SC-007); every design decision traces to an FR (see Phase 0 Design Decisions) |
| II | Feature-Centric Development | ✅ Pass | Spec bound to Feature 013 via `/speckit.clarify`; feature index and `features/013.md` updated at binding time and again at this planning phase |
| III | Intent-Driven Development | ✅ Pass | Requirements state WHAT/WHY (visual reporting for external readers); this plan states HOW (skill packages + delegation) without inventing unspecified scope |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Structural contract tests planned (`tests/contract/test_summarize_project_prompt_assets.py`, `test_analysis_project_uml_assets.py`) to be authored before skill content per Red-Green order; prompt-asset assertions follow 008/012/013 precedent |
| V | AI Agent Integration Standards | ✅ Pass | Skill packages follow the established format discoverable by all approved agents; no new agent/provider is introduced |
| VI | Continuous Quality & Observability | ✅ Pass | Changes tracked via Feature 013 detail log and git history; YAGNI respected (no render code, no new scripts — delegation only) |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Full SDD flow executed (requirements → clarify → plan); reuse-first gate honored (bound to existing Feature 013, no new Feature); no status regression (013 stays Implemented) |
| VIII | Code as the Single Source of Truth | ✅ Pass | Design grounded in the actual sources read during planning: `skills/draw-plantuml/SKILL.md`, `references/howto/13-wbs-diagram.md`, `references/howto/14-gantt-diagram.md`, `skills/analysis-project/SKILL.md` |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | Prompt artifacts only; rendering delegated to the existing `draw-plantuml` skill; no orchestration runtime, no duplicated PlantUML logic |
| X | Documentation Naming & Location Conventions | ✅ Pass | New docs use lowercase kebab-case under semantic paths (`references/uml-visualization-guide.md`, spec-dir artifacts); tool-mandated names (`SKILL.md`) preserved verbatim |

**Gates Status**: ✅ All gates pass — no violations requiring justification.

**Re-check after Phase 1**: 2026-07-18 — Post-design check confirms no additional violations. `data-model.md`, `contracts/visual-reporting-skills.openapi.yaml`, `quickstart.md`, and `feature-ref.md` are structural/prompt-asset specifications consistent with Constitution IX; the contract file is declarative (no deliberation markers) and every schema/rule maps to an FR.

## Project Structure

### Documentation (this spec)

```text
.specify/specs/030-summarize-project/
├── plan.md              # This file (/speckit.plan command output)
├── requirements.md      # Dual-workstream specification (US1–US4, FR-001…FR-019)
├── data-model.md        # Phase 1: entities + skill package structural model
├── quickstart.md        # Phase 1: implementation & verification walkthrough
├── contracts/           # Phase 1 output
│   └── visual-reporting-skills.openapi.yaml  # Structural contract for both skill packages
├── feature-ref.md       # Phase 1: Feature 013 binding reference
├── checklists/
│   └── requirements.md  # Specification quality checklist
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

No standalone research.md — Phase 0 findings inlined below.

### Source Code (repository root)

```text
skills/summarize-project/           # NEW: visual project summary skill (WBS + Gantt → HTML report)
skills/analysis-project/            # MODIFIED: SKILL.md gains UML diagramming actions; +references/uml-visualization-guide.md
.specify/skills/summarize-project/  # NEW MIRROR: byte-equivalent copy of the canonical skill
.specify/skills/analysis-project/   # MODIFIED MIRROR: synchronized with canonical edits
.specify/instructions.md            # MODIFIED: skills registry gains the summarize-project entry
tests/contract/                     # MODIFIED: +test_summarize_project_prompt_assets.py, +test_analysis_project_uml_assets.py
```

**Structure Decision**: Extends the existing skill-package layout (canonical `skills/<name>/` + byte-equivalent `.specify/skills/<name>/` mirror + registry row + contract tests), exactly the shape used by iterations 008/012/013/017 under Feature 013. WS-A adds one new package; WS-B edits one existing package in place. No new top-level directories are created.

## Complexity Tracking

N/A — all Constitution Check rows pass; no violations to justify.

## Phase 0: Research Review

### Key Findings from Internal Analysis

1. **draw-plantuml already provides everything both workstreams need**: WBS (`@startwbs`, guide `references/howto/13-wbs-diagram.md`), Gantt (`@startgantt` with milestones/dependencies/progress coloring, guide `references/howto/14-gantt-diagram.md`), the full UML diagram set with per-type guides (`references/howto/02`–`12`), a render script (`scripts/render-plantuml.sh` producing PNG+SVG), and explicit output conventions (single HTML, relative paths, `.puml` sources kept). Therefore both workstreams MUST reference this skill rather than duplicate any of it (FR-005/006/011/016; Constitution IX).

2. **analysis-project's current visualization is Mermaid-only and text-heavy**: its SKILL.md mandates Mermaid sketches (Phase 5 report-structure design, Output Requirements) and fixes the deliverable at `$WORK_DIR/docs/overview.md`. The enhancement injection points are: frontmatter description (mention UML), Phase 5 (plan UML figures for primary views), Phase 8 (assemble rendered figures into the report), Output Requirements (UML figures as the standard for primary views; Mermaid retained for secondary sketches), plus a new `references/uml-visualization-guide.md` carrying the view→diagram-type mapping (FR-017).

3. **Skill authoring conventions are fully established**: package layout and frontmatter from `templates/skills-template.md` and the `create-skills` skill; `${SKILL_HOME}` / `${SKILL_WORKDIR}` idioms from spec 012; registry row in `.specify/instructions.md` from spec 008; canonical→mirror byte-equivalence from specs 013/017; structural contract tests from `tests/contract/test_create_skills_prompt_assets.py` and `test_portable_skill_creation.py`.

4. **Two-chart consistency is the core domain rule of WS-A**: the single work breakdown is the shared basis for both charts; every scheduled WBS leaf work item appears as a Gantt entry with identical naming (FR-004/FR-009, SC-003). The skill's workflow must therefore produce the breakdown FIRST as data, then derive both charts from it.

### Design Decisions

1. **summarize-project package shape** (WS-A): `SKILL.md` (workflow: ① collect & source-trace work items → ② single hierarchical decomposition → ③ WBS chart via draw-plantuml → ④ Gantt chart with milestones/progress via draw-plantuml → ⑤ assemble self-contained HTML report with narrative) + `references/reporting-playbook.md` (decomposition depth rules, schedule-estimation defaults & visible-assumption marking, chart-set splitting for large projects, two-chart consistency checklist). No `scripts/` directory — rendering is delegated (FR-005/006/011).

2. **analysis-project enhancement shape** (WS-B): in-place SKILL.md edits at the four injection points above + one new reference guide `references/uml-visualization-guide.md` (view→UML-type mapping: component/package for static structure, deployment for runtime topology, sequence for key flows — activity as the acceptable alternative for business/process flows — class/ER for data structures; delegation pointer to draw-plantuml's howto guides; degradation rule when rendering is unavailable). No changes to phases 1–4, 6–7 logic, deliverable location, or subagent discipline (FR-018).

3. **Output locations** (resolved at re-clarification 2026-07-18): summary report defaults to `docs/project-summary/` under the target workspace (user-overridable); analysis UML figures and `.puml` sources live under `docs/figures/` of the analyzed workspace, referenced by relative paths. UML/Mermaid division is a strict primary/secondary split — primary views MUST be UML figures, Mermaid restricted to secondary sketches (FR-018).

4. **Contract strategy**: one structural contract `contracts/visual-reporting-skills.openapi.yaml` covering both packages' assets, delegation references, output conventions, and fallback behaviors — the assertions the two new pytest files will verify structurally (frontmatter, registry row, mirror equivalence, delegation references to `draw-plantuml`, required sections).

5. **No status regression**: Feature 013 remains `Implemented` per Constitution VII workflow gates; this iteration appends a new requirements slice under it.

Design decisions 3–5 above incorporate the 2026-07-18 re-clarification answers (output locations, UML/Mermaid boundary, activity alternative).

## Phase 1 Design Artifacts

Generated as separate files:
- `data-model.md` — Domain entities (Work Item, Milestone, Summary Report, UML Figure, Analysis Report) + skill package structural model
- `contracts/visual-reporting-skills.openapi.yaml` — Structural contract for both skill packages
- `quickstart.md` — Step-by-step implementation & verification walkthrough
- `feature-ref.md` — Feature 013 binding reference
