# Requirements Specification: Agent Framework Redesign

**Requirement Branch**: `023-agent-framework-redesign`  
**Created**: 2026-07-10  
**Status**: Draft  
**Input**: User description: "基于 docs/agents/design.md 的设计方案重构当前项目的 agent 整体实现，需要从代码和文档两个角度进行整体的重构。"

## Related Feature *(mandatory)*

**Feature ID**: 019  
**Feature Name**: Agents Command

## Context & Motivation

The current Agent framework mixes several concepts whose boundaries are unclear, making it hard to reason about, extend, or teach. Per `docs/agents/design.md`, the confusion manifests as:

- **Role is not cleanly abstracted** — an Agent's responsibility and perspective are implied but never explicitly modeled.
- **Stage and Role are conflated** — the three execution phases (executor / evaluator / optimizer) are entangled with Role definitions.
- **Team (static structure) is missing** — the static organization of multiple Agents plus a Supervisor is not expressed.
- **Loop (dynamic structure) is missing** — the runtime iteration cycle across stages is not formally defined.
- **Templates are scattered** — assorted `agent-*` templates live in the templates directory, disconnected from the `create-agent` skill.
- **Terminology is inconsistent** — "SubRole" vs "Stage", "improver" vs "optimizer" coexist across templates, skills, orchestration files, and tests.

This specification defines WHAT the redesigned Agent framework must deliver — a single conceptual model, a single command entry point, consolidated templates, unified terminology, and coherent documentation — refactored across **both code and documentation**. It does not prescribe implementation details (the HOW is deferred to `/speckit.plan`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Single Command Entry for All Agent Operations (Priority: P1)

A framework user performs every Agent-related action — creating, organizing/orchestrating, and executing agents — through the single `/speckit.agents` command. They never need to discover or learn any other agent-specific command.

**Why this priority**: A single, intent-driven entry point is the anchor of the redesign. Without it, the conceptual model and scenarios have no coherent surface for users to interact with.

**Independent Test**: Invoke `/speckit.agents` with representative intents (create an agent, organize agents in parallel/serial/team-loop, run a team) and confirm each is handled end-to-end without any other agent command existing or being required.

**Acceptance Scenarios**:

1. **Given** a user wants to create, orchestrate, or execute agents, **When** they invoke `/speckit.agents` with a natural-language intent, **Then** the command recognizes the intent and routes it to the appropriate capability (create / organize / execute) without requiring another command.
2. **Given** the redesign is complete, **When** the command surface is inventoried, **Then** no new agent-specific command exists beyond `/speckit.agents`, and any prior agent-related command paths are consolidated into it.
3. **Given** an ambiguous or unsupported intent, **When** the user invokes `/speckit.agents`, **Then** the command reports the recognized options and asks for the missing intent rather than failing silently.

---

### User Story 2 - Unified Conceptual Model and Terminology (Priority: P1)

A developer reading or authoring an Agent finds a single, unambiguous conceptual model: each Agent is described by three orthogonal attribute dimensions (Role, Stage, Type) plus two organizational structures (Team, Loop). Terminology is consistent everywhere — no "SubRole", no "improver".

**Why this priority**: The core problem being solved is conceptual confusion. A consistent model and vocabulary is what every other change depends on.

**Independent Test**: Review any agent definition, template, skill doc, or orchestration file and confirm it expresses Role/Stage/Type/Team/Loop consistently, and that a repository-wide search finds zero remaining references to the deprecated terms "SubRole"/"Subrole" and "improver" (outside historical changelogs).

**Acceptance Scenarios**:

1. **Given** an Agent definition, **When** it is inspected, **Then** it declares a **Role** (responsibility + perspective), a **Stage** (one of executor / evaluator / optimizer), and a **Type** (Worker or Meta).
2. **Given** an Agent moves through an iteration, **When** its Stage changes, **Then** its Type follows the coupling rule: **executor → Worker**, **evaluator → Meta**, **optimizer → Meta**.
3. **Given** a Team is described, **When** rendered as a two-dimensional matrix, **Then** rows are Roles, columns are the three Stages, and each cell states the Type (Worker/Meta) for that Role at that Stage, including a single merged **Team Supervisor** (Meta at all stages).
4. **Given** the redesign is complete, **When** the repository is searched, **Then** "SubRole" is fully replaced by "Stage" and "improver" is fully replaced by "optimizer" across templates, skills, orchestration files, and tests.

---

### User Story 3 - Three Multi-Agent Collaboration Scenarios (Priority: P2)

A user orchestrates multiple agents in one of three supported topologies — parallel, serial, or team-loop — all reachable via `/speckit.agents`.

**Why this priority**: These scenarios are the practical payoff of the model; they enable real multi-agent work but depend on the model (US2) and entry point (US1) being in place first.

**Independent Test**: Trigger each of the three scenarios via `/speckit.agents` and confirm the framework selects and runs the corresponding orchestration pattern.

**Acceptance Scenarios**:

1. **Given** independent tasks with no shared state, **When** the user requests parallel work, **Then** the framework organizes agents to run concurrently to improve throughput.
2. **Given** phased work where each stage feeds the next, **When** the user requests serial work, **Then** the framework organizes agents into an ordered chain where each agent owns one phase.
3. **Given** a quality-critical deliverable, **When** the user requests a team, **Then** the framework organizes a closed-loop, self-iterating team composed of Worker agents, Meta agents, and a Supervisor.

---

### User Story 4 - Temporary vs Persistent Agent Lifecycle (Priority: P2)

A user creates agents that are either temporary (recorded only in the working context) or persistent (saved to the project's agent directory and wired into supported tools' configuration).

**Why this priority**: Lifecycle handling determines whether agents survive a session and integrate with tooling; it is essential for real projects but sits on top of the core model.

**Independent Test**: Create one temporary and one persistent agent; confirm the temporary one exists only in context, and the persistent one is written to `.specify/agents` and made available to supported tools via the initialization step.

**Acceptance Scenarios**:

1. **Given** a temporary agent, **When** it is created, **Then** it is recorded in the working context only and is not written to the project agent directory.
2. **Given** a persistent agent, **When** it is created, **Then** it is stored under `.specify/agents`.
3. **Given** a persistent agent and the supported tools, **When** the project initialization step runs, **Then** each supported tool's agent configuration is produced (e.g., `.qoder/agents` linked to `.specify/agents` for Qoder).

---

### User Story 5 - Consolidated Templates and Coherent Documentation (Priority: P3)

A contributor finds all agent templates co-located with the `create-agent` skill, and finds the `docs/agents` documentation consistent with the new model and vocabulary.

**Why this priority**: Consolidation and doc coherence prevent regression back into scattered, inconsistent state, but they follow the substantive model and command changes.

**Independent Test**: Confirm the assorted `agent-*` templates now live under the `create-agent` skill's templates directory, that `create-agent`/orchestration docs and tests reference the new paths and names, and that `docs/agents` uses the unified terminology.

**Acceptance Scenarios**:

1. **Given** the assorted `agent-*` templates, **When** the redesign is complete, **Then** they reside under the `create-agent` skill's `templates` directory rather than scattered in the top-level templates directory.
2. **Given** the stage templates, **When** the redesign is complete, **Then** `agent-subrole-*.md` files are renamed to `agent-stage-*.md`, and the optimizer stage template and its internal `name`/`description` no longer say "improver".
3. **Given** the `create-agent` skill doc, orchestration templates, and tests, **When** the redesign is complete, **Then** they all reference the new template locations and stage names with no broken references.
4. **Given** the `docs/agents` documentation, **When** reviewed, **Then** it describes the Role/Stage/Type/Team/Loop model and the three collaboration scenarios consistently with `docs/agents/design.md`.

---

### Edge Cases

- **Ambiguous intent to `/speckit.agents`**: The command must surface recognized capabilities and prompt for the missing intent instead of guessing or erroring out.
- **Persistence without an active tool mapping**: A persistent agent is still stored under `.specify/agents` even if a tool has no link yet; the link is (re)created on the next initialization.
- **Residual deprecated terms in generated/historical files**: Changelogs and archived specs may still contain "SubRole"/"improver"; the zero-reference requirement applies to live templates, skills, orchestration files, docs, and tests — not immutable history.
- **Templates referenced by old paths**: Any dangling reference to a pre-migration template path must fail loudly (be detectable), not silently resolve to nothing.
- **Team Supervisor merge**: References to the former separate "Meta-Coordinator" and "Team Supervisor" roles must resolve to the single merged Team Supervisor without leaving orphaned role definitions.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST expose `/speckit.agents` as the single command entry point for all agent operations (creation, organization/orchestration, execution) and MUST NOT introduce any additional agent-specific command.
- **FR-002**: `/speckit.agents` MUST first recognize user intent from natural-language input, then route to the appropriate capability based on that analysis.
- **FR-003**: The system MUST describe every Agent using three orthogonal attribute dimensions: **Role** (responsibility and perspective), **Stage** (one of [[STR-001]] / [[STR-002]] / [[STR-003]]), and **Type** (one of [[STR-004]] / [[STR-005]]).
- **FR-004**: The system MUST enforce the Type-follows-Stage coupling: an Agent is a **Worker** in the executor Stage, and a **Meta** in the evaluator and optimizer Stages.
- **FR-005**: The system MUST represent a **Team** (static structure) as a two-dimensional matrix where each row is a Role, each column is a Stage, and each cell states the Type for that Role at that Stage.
- **FR-006**: The system MUST define a **Loop** (dynamic structure) as the runtime iteration across stages that a multi-Agent group executes.
- **FR-007**: The Team model MUST include a single merged **Team Supervisor** (a Meta Role, Meta at all Stages) that unifies the responsibilities of the former "Meta-Coordinator" and "Team Supervisor".
- **FR-008**: The system MUST support three multi-Agent collaboration scenarios reachable via `/speckit.agents`: **parallel**, **serial**, and **team closed-loop**.
- **FR-009**: The team closed-loop scenario MUST comprise three Agent categories: Worker agents (real tasks), Meta agents (optimize skills/other agents), and a Supervisor agent (evaluation/scoring and convergence control).
- **FR-010**: The system MUST support two Agent lifecycles: **temporary** (recorded in context only) and **persistent** (stored in the project agent directory).
- **FR-011**: Persistent agents MUST be stored under [[STR-006]].
- **FR-012**: The project initialization step MUST produce agent configuration for **all officially supported tools** (e.g., Qoder, Claude Code) from the persistent agents — e.g., a `.qoder/agents` link to [[STR-006]] for the Qoder tool — consistent with the multi-tool support of Feature 022.
- **FR-013**: The system MUST relocate the assorted `agent-*` templates into the `create-agent` skill's templates directory ([[STR-007]]).
- **FR-014**: The system MUST rename stage templates from `agent-subrole-*.md` to [[STR-008]], including renaming the optimizer stage template so it no longer uses "improver".
- **FR-015**: The system MUST replace the deprecated term "SubRole"/"Subrole" with "Stage" and "improver" with "optimizer" across all live templates, skills, orchestration files, and tests.
- **FR-016**: The system MUST update the `create-agent` skill documentation, all orchestration templates, and tests to reference the new template locations and stage names, with no broken references.
- **FR-017**: The `docs/agents` documentation MUST be refactored to describe the Role/Stage/Type/Team/Loop model and the three collaboration scenarios consistently with `docs/agents/design.md`.
- **FR-018**: The redesign MUST cover both **code** (commands, skills, templates, tests) and **documentation** so that the two remain mutually consistent.
- **FR-019**: When `/speckit.agents` receives ambiguous or unsupported intent, the system MUST report the recognized capabilities and request the missing intent rather than failing silently.
- **FR-020**: The system MUST migrate existing persisted agent definitions under [[STR-006]] to the new conceptual model and unified terminology (Role/Stage/Type; Stage not SubRole; optimizer not improver), so that no live persisted agent retains deprecated concepts or terms.
- **FR-021**: The redesign MUST include a multi-agent research activity that mines agent-related best practices from the sibling `/cws_work/*` projects (excluding `spec-kit` itself), assigning one agent per project, and MUST produce a consolidated research-findings artifact whose conclusions are integrated into the redesigned model and templates.

### Key Entities *(include if requirement involves data)*

- **Agent**: A unit of work described by Role + Stage + Type; may be temporary or persistent.
- **Role**: The responsibility and problem-solving perspective an Agent embodies (e.g., Requirements Analyst, System Designer, Team Supervisor).
- **Stage**: The execution phase of a Role — executor, evaluator, or optimizer.
- **Type**: The classification of an Agent as Worker (does real project tasks) or Meta (optimizes/manages other agents); derived from Stage.
- **Team**: The static organizational structure — a Role × Stage matrix of Agents including a Team Supervisor.
- **Loop**: The dynamic runtime structure — the iteration cycle across stages a multi-Agent group performs.
- **Agent Template**: A reusable definition (role template, stage template, orchestration template) co-located with the `create-agent` skill.
- **Research Findings**: The consolidated artifact capturing agent-related best practices mined from each in-scope `/cws_work/*` sibling project, feeding the redesigned model and templates.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of agent operations (create, organize, execute) are reachable through `/speckit.agents`, and the count of other agent-specific commands is exactly 0.
- **SC-002**: A repository-wide search for the deprecated terms "SubRole"/"Subrole" and "improver" returns 0 matches across live templates, skills, orchestration files, docs, and tests.
- **SC-003**: 100% of the previously scattered `agent-*` templates reside under the `create-agent` skill's templates directory, and 0 templates remain in the former top-level location.
- **SC-004**: 0 broken references to old template paths or old stage names remain (verified by the existing test suite passing and by reference validation).
- **SC-005**: Every Agent definition and every stage/role/orchestration template expresses Role, Stage, and Type consistently — 100% conformance on inspection.
- **SC-006**: All three collaboration scenarios (parallel, serial, team-loop) can be initiated via `/speckit.agents` and select the correct orchestration pattern in 100% of trials.
- **SC-007**: `docs/agents` documentation contains 0 statements that contradict `docs/agents/design.md`'s conceptual model or terminology.
- **SC-008**: A consolidated research-findings artifact exists covering every in-scope `/cws_work/*` sibling project (one agent per project), and at least one concrete redesign decision cites it.
- **SC-009**: 0 live persisted agents under `.specify/agents` retain deprecated concepts or terms after migration.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Command inventory of the commands directory plus manual walkthrough of the three operation intents through `/speckit.agents`.
- **SC-002 Source**: Automated repository grep (excluding changelogs/archived history) for the deprecated terms; count must be 0.
- **SC-003 Source**: Directory listing comparison of the `create-agent` skill templates directory versus the former top-level templates directory.
- **SC-004 Source**: Execution of the existing test suite plus a reference-integrity check for template paths and stage names.
- **SC-005 Source**: Manual/scripted inspection of agent definitions and templates for the presence of Role/Stage/Type fields.
- **SC-006 Source**: Manual walkthrough invoking each scenario via `/speckit.agents` and confirming the selected orchestration mode.
- **SC-007 Source**: Documentation review of `docs/agents` against `docs/agents/design.md`.
- **SC-008 Source**: Presence/inventory check of the research-findings artifact against the list of in-scope `/cws_work/*` sibling projects, plus traceability from redesign decisions to cited findings.
- **SC-009 Source**: Automated grep of `.specify/agents/*.agent.md` for deprecated terms and inspection for Role/Stage/Type conformance; count of non-conforming files must be 0.

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

<!--
  Canonical vocabulary and path literals for the redesign. Downstream artefacts
  (FRs, plan, tasks, tests, templates) MUST cite by `[[STR-NNN]]` rather than
  re-typing, so a rename only edits this section.
-->

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "executor" | FR-003, stage templates, orchestration docs |
| `STR-002` | "evaluator" | FR-003, stage templates, orchestration docs |
| `STR-003` | "optimizer" | FR-003, FR-014, FR-015, stage templates |
| `STR-004` | "Worker" | FR-003, FR-004, Team matrix |
| `STR-005` | "Meta" | FR-003, FR-004, FR-007, FR-009, Team matrix |
| `STR-006` | ".specify/agents" | FR-011, FR-012 |
| `STR-007` | "skills/create-agent/templates" | FR-013, FR-016 |
| `STR-008` | "agent-stage-*.md" | FR-014, FR-016 |

**Citation convention**: When an FR, plan, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-07-10

- Q: Which Feature does this requirement bind to? → A: **019 Agents Command** (natural continuation; prior EEI spec `022-eei-agent-triad` bound to it).
- Q: Is the cross-project research over `/cws_work/*` (design.md §3.6) in scope? → A: **In-scope deliverable** — the plan must schedule multi-agent research tasks and produce a consolidated research-findings artifact (see FR-021, SC-008).
- Q: How are existing persisted agents and current templates handled? → A: **Full migration/alignment** — existing persisted agents, templates, skills, orchestration files, and tests are all migrated to the new model and terminology (see FR-020, SC-009).
- Q: What is the coverage scope for persistent-agent tool-side config (FR-012)? → A: **All officially supported tools** (e.g., Qoder, Claude Code), consistent with Feature 022 (see FR-012).
