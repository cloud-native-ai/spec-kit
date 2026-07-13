# Data Model: Agent Skill Enablement

**Feature**: 026 — Agent Skill Enablement
**Spec**: [requirements.md](./requirements.md)
**Date**: 2026-07-13

This feature has no database. "Entities" here are the conceptual objects manipulated by the
change: agent definitions, skills, and the mapping between them. They are expressed as
Markdown/YAML files, not tables.

## Entities

### Built-in Agent

The unit being empowered. A framework-shipped role agent under `agents/<slug>.agent.md`
(mirrored to `.specify/agents/`).

| Field | Type | Source / Rule |
|-------|------|---------------|
| `slug` | string | File stem; one of the 7 preset roles (FR-001) |
| `name` | string | Existing frontmatter `name` (unchanged) |
| `tools` | list<string> | Existing frontmatter `tools` (unchanged, FR-011) |
| `skills` | list<string> | **NEW** frontmatter list of canonical skill slugs relevant to the role (FR-002, FR-004, FR-006) |
| `skill_guidance` | Markdown section | **NEW** `## Skill Enablement` body section: shared protocol + per-role skill table with when-to-use + fallback (FR-003, FR-008, FR-009) |

**Validation rules**:
- `skills` MUST contain ≥1 slug (SC-001).
- Every slug in `skills` MUST exist under `.specify/skills/<slug>/SKILL.md` (FR-005, SC-002).
- Slugs MUST NOT include reference-only or meta skills (see Framework Skill below).
- All other frontmatter fields MUST be byte-for-byte preserved (FR-011).

**Scope**: exactly the 7 presets — `requirements-analyst`, `system-designer`,
`module-designer`, `test-engineer`, `qa-engineer`, `knowledge-manager`, `ux-analyst`.
Transient EEI stage sub-agents inherit the parent role's skills and are NOT edited.

### Framework Skill

An installed capability under `.specify/skills/<slug>/`. Reference set for validation.

| Field | Type | Rule |
|-------|------|------|
| `slug` | string | Directory name; canonical identifier used by agents (FR-006) |
| `declarable` | bool | `true` unless reference-only or meta (see below) |

**Non-declarable skills** (excluded from any agent `skills:` list, FR-004):
- Reference-only: `sdd-workflow` (documented as "NOT invoked directly").
- Meta / framework-authoring: `create-agent`, `improve-agent`, `create-skills`,
  `improve-skills`, `organize-agents` (owned by `/speckit.agents` and `/speckit.skills`).

### Agent–Skill Mapping

The role-appropriate association between a Built-in Agent and its declared skills.
Derived from each role's definition (FR-004). This is the authoritative mapping to implement.

| Agent | Declared skills | Rationale (representative operations) |
|-------|-----------------|----------------------------------------|
| requirements-analyst | `draw-plantuml`, `memory-recall`, `memory-record`, `think-skills` | Draw UML use-case diagrams; recall prior requirements/decisions; record clarifications; mentally simulate requirement logic |
| system-designer | `draw-plantuml`, `analysis-project`, `memory-recall`, `memory-record`, `think-skills` | Architecture/component/sequence diagrams; analyze existing architecture; recall design decisions; record rationale; simulate designs |
| module-designer | `analysis-project`, `git-workflow`, `git-submodule-edit`, `memory-record`, `think-skills` | Analyze project structure before implementing; branch sync; submodule edits; record module decisions; simulate change logic |
| test-engineer | `browser-utils`, `extension-e2e-test`, `database-utils`, `think-skills` | Web E2E tests; browser-extension E2E; DB-backed verification; simulate test scenarios |
| qa-engineer | `analysis-project`, `browser-utils`, `database-utils`, `memory-recall` | Architecture/constitution compliance analysis; end-to-end web checks; data validation; recall requirements/acceptance criteria |
| knowledge-manager | `document-utils`, `memory-record`, `memory-recall`, `draw-plantuml`, `draw-d3js`, `draw-echarts` | Produce/edit office docs; record & recall knowledge; diagrams and data visualizations for documentation |
| ux-analyst | `browser-utils`, `document-utils`, `draw-echarts`, `draw-d3js`, `extension-e2e-test` | UI/UX inspection & screenshots; UX reports; UX data visualization; extension UI testing |

**Invariants**:
- Union of all declared skills ⊆ declarable installed skills (SC-002).
- Each row has ≥1 skill (SC-001).
- No non-declarable skill appears in any row.

### Skill-Usage Guidance

The per-agent `## Skill Enablement` section. Structure (identical across agents except the table):

1. **Shared protocol** (single source, from `agent-skill-enablement.md`): "Prefer an
   applicable framework skill over performing the operation manually; select the most
   role-specific skill; if multiple apply, choose the most specific; if none applies or a
   skill fails, complete the operation directly and surface the failure." (FR-003, FR-008, FR-010, FR-012)
2. **Per-role skill table**: `| Skill | When to use |` rows from the Agent–Skill Mapping.

## State / Lifecycle

Not applicable — agent definitions are static files. The only transition is the feature
status `Draft → Planned` (this plan) → `Implemented` (future `/speckit.implement`).

## Requirements Traceability

| Requirement | Entity / rule |
|-------------|---------------|
| FR-001 | Built-in Agent scope = 7 presets |
| FR-002 | Built-in Agent `skills` field |
| FR-003 | Skill-Usage Guidance shared protocol |
| FR-004 | Agent–Skill Mapping (role-derived) + non-declarable exclusions |
| FR-005 | Validation: `skills` ⊆ installed set |
| FR-006 | `skills` uses canonical slugs |
| FR-007 | Premise stated in guidance (skills install with agents) |
| FR-008 | Guidance fallback rule |
| FR-009 | Uniform frontmatter field + section format across agents |
| FR-010 | Guidance multi-match selection rule |
| FR-011 | All other frontmatter preserved; templates updated in lockstep |
| FR-012 | Guidance delegates to skill (no logic duplication) |
