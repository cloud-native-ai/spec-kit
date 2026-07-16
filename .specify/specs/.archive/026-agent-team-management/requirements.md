# Requirements Specification: Agent Team Management

**Requirement Branch**: `026-agent-team-management`  
**Created**: 2026-07-13  
**Status**: Draft  
**Input**: User description: "新建一个 team 概念用来专门管理多 agent 的配置。将 Conceptual Model 从 skills/create-agent/SKILL.md 中剥离；skills/create-agent 和 skills/improve-agent 技能只负责单个 agent 的管理；多个 agent 形成一个 team，使用专门的 team 命令和技能进行管理。将 skills/organize-agents 技能重命名为 skills/create-team，再创建一个新的 skills/improve-team 技能，完成最终的闭环。speckit 框架中支持 '/speckit.team' 作为 team 相关操作的唯一入口；skills/create-team 用来创建一个 team（基于用户需求组织的多 agents 结构）；skills/improve-team 用来针对一个已经存在的 team 进行调整和优化。"

## Related Feature *(mandatory)*

**Feature ID**: 027  
**Feature Name**: Team Management

## User Scenarios & Testing *(mandatory)*

<!--
  User stories are prioritized user journeys. Each is independently testable and
  delivers a standalone slice of value.
-->

### User Story 1 - Create a team through a single command (Priority: P1)

As a Spec Kit user, I want to organize several agents into a collaborative **team** through one dedicated command, so that I have a single, obvious place to structure multi-agent work — mirroring how single-agent work already has its own home.

**Why this priority**: This is the core value of the feature. Without the ability to create a team through the dedicated entry point, the "team" concept does not exist for users. It is the minimum viable slice: a user states what they want the group of agents to accomplish, and the framework produces a team structure organized from that need.

**Independent Test**: Invoke the team entry point with an intent to build a multi-agent structure (e.g., "组织一个团队完成 X") and confirm a team is created that organizes the chosen agents into a coherent collaboration structure, without touching any single-agent authoring path.

**Acceptance Scenarios**:

1. **Given** a project with existing agents, **When** the user invokes the team entry point asking to organize multiple agents to reach a goal, **Then** the framework creates a team that groups the selected agents into a collaboration structure derived from the stated need.
2. **Given** the user expresses only a goal (no explicit agent list), **When** they invoke team creation, **Then** the framework proposes a suitable set of member agents and a collaboration structure for confirmation.
3. **Given** an ambiguous request that maps to neither "create" nor "improve", **When** the user invokes the team entry point, **Then** the framework reports the recognized team capabilities and requests the missing intent rather than guessing silently.

---

### User Story 2 - Improve an existing team (Priority: P2)

As a Spec Kit user, I want to adjust and optimize a team I already created, so that I can evolve its membership and collaboration structure as my needs change — without recreating it from scratch.

**Why this priority**: Completes the create → improve lifecycle ("闭环") for teams. It depends on US1 (a team must exist first) but delivers independent, repeatable value every time a team needs tuning.

**Independent Test**: Take an existing team, invoke the team entry point with an improvement intent (e.g., "调整这个团队，增加一个评审角色"), and confirm the targeted change is applied while the team's unaffected parts remain intact.

**Acceptance Scenarios**:

1. **Given** an existing team, **When** the user requests a specific adjustment (add/remove a member, change the collaboration pattern, tune quality thresholds), **Then** the framework applies the targeted change and preserves the parts that were working.
2. **Given** an improvement request that references a team that does not exist, **When** the user invokes team improvement, **Then** the framework reports that no such team was found and offers to create one instead.
3. **Given** an improvement request based on observed problems (evidence), **When** the user provides that evidence, **Then** the applied changes are traceable to the stated evidence rather than generic rewriting.

---

### User Story 3 - Clean separation between single-agent and team management (Priority: P2)

As a framework maintainer, I want single-agent skills to manage only single agents and the team domain to own all multi-agent concepts, so that each skill has an unambiguous responsibility and users are never confused about where to go.

**Why this priority**: This separation is the structural foundation that makes US1 and US2 coherent. It can be validated independently by inspecting skill responsibilities and cross-references, and it prevents duplicated or contradictory guidance across the agent and team domains.

**Independent Test**: Inspect the single-agent authoring/refinement skills and confirm they contain no team/multi-agent orchestration content, that the shared conceptual vocabulary lives in exactly one place (the team domain), and that the former orchestration skill is reachable only under its new team name.

**Acceptance Scenarios**:

1. **Given** the single-agent authoring skill, **When** it is reviewed, **Then** it no longer embeds the multi-agent Conceptual Model, and that model is defined once in the team domain.
2. **Given** the former `organize-agents` skill, **When** the framework is searched, **Then** it is reachable only as `create-team`, and no dangling references to the old name remain (outside historical specs).
3. **Given** a user tries to perform a team operation through the single-agent command, **When** they do so, **Then** they are directed to the dedicated team entry point (team operations are not served by the single-agent command).

---

### Edge Cases

- **Ambiguous intent**: The team entry point receives a request that is neither clearly "create" nor "improve" → it reports recognized team capabilities and asks for the missing intent instead of guessing.
- **Improve a non-existent team**: `improve-team` is asked to change a team that cannot be found → clear "not found" report with an offer to create it.
- **Missing member agents**: `create-team` references member agents that do not yet exist → the framework prompts the user to author the missing single agents (via the single-agent path) before finalizing the team.
- **Stale membership**: A team references agents that were later renamed or deleted → improve/inspect surfaces the broken references rather than failing silently.
- **Legacy invocation**: A user relies on the old `organize-agents` name or the old single-agent-command routing for team work → the framework guides them to the new `create-team` / `/speckit.team` path.
- **Conceptual Model drift**: A single-agent skill re-introduces multi-agent concepts → this must be detectable as a violation of the single-source-of-truth rule.

## Requirements *(mandatory)*

### Functional Requirements

**Team entry point**

- **FR-001**: The framework MUST provide `[[STR-001]]` as the single entry point for all team-related operations.
- **FR-002**: The team entry point MUST recognize user intent and route it to the owning team skill (create vs. improve). On ambiguous or unsupported intent it MUST report the recognized team capabilities and request the missing intent — it MUST NOT guess silently.
- **FR-003**: Team operations MUST NOT be reachable through the single-agent command (`/speckit.agents`); that command MUST be scoped to single-agent operations only, and MUST direct team requests to the team entry point.

**create-team skill**

- **FR-004**: A `[[STR-002]]` skill MUST exist that creates a **team** — a multi-agent structure organized from the user's stated needs.
- **FR-005**: `create-team` MUST be the renamed successor of `[[STR-004]]`, preserving its existing collaboration capabilities (parallel dispatch, serial chain, and self-iterating team loop).
- **FR-006**: The rename MUST update every reference to the former skill — skill identifier, registry entries, discovery metadata, symlinks, documentation, and cross-skill references — so that no dangling `[[STR-004]]` reference remains anywhere in the active framework (historical spec archives excluded).
- **FR-007**: `create-team` MUST allow a team to be created either from an explicit list of member agents or from a goal statement, proposing member agents and a collaboration structure when the user provides only a goal.

**improve-team skill**

- **FR-008**: An `[[STR-003]]` skill MUST exist that adjusts and optimizes an **existing** team.
- **FR-009**: `improve-team` MUST make targeted, evidence-based changes (membership, collaboration pattern, quality thresholds/iteration settings) while preserving the parts of the team that are working correctly.
- **FR-010**: `improve-team` MUST report a clear "team not found" result when asked to improve a team that does not exist, and offer to create one.

**Separation of concerns & Conceptual Model**

- **FR-011**: The multi-agent Conceptual Model (Role × Stage × Type + Team/Loop) MUST be removed from the single-agent authoring skill (`create-agent`).
- **FR-012**: The Conceptual Model MUST be owned by the team domain as the single source of truth; other skills MAY reference it but MUST NOT redefine or duplicate it.
- **FR-013**: `create-agent` and `improve-agent` MUST be scoped to single-agent management only and MUST NOT contain multi-agent orchestration or team-lifecycle content.
- **FR-014**: The set of team skills (`create-team`, `improve-team`) MUST form a complete create → improve lifecycle for teams, consistent with the existing single-agent create → improve lifecycle.

**Discovery & consistency**

- **FR-015**: All discovery and registry surfaces (skills registry, instructions, documentation, command index) MUST reflect the new team command and skills and the removal of the old orchestration skill name.
- **FR-016**: The inherently multi-agent authoring constructs currently in `create-agent` — the EEI **triad** (three stage agents forming a loop) and the **team-supervisor** — MUST move into the team domain (`create-team`), so that the framework has exactly one home for each multi-agent concept. After the move, `create-agent` retains only single-agent authoring modes (`role`, `supervisor`, `custom`, `project-custom`).

**Scope boundary of the team domain**

- **FR-017**: The team domain MUST own the full team lifecycle — creating, improving, **and executing/running** a team at runtime (the parallel dispatch, serial chain, and self-iterating team-loop orchestration that `organize-agents` performs today). Team execution MUST be reachable through `[[STR-001]]` and MUST NOT be served by the single-agent command.

### Key Entities *(include if requirement involves data)*

- **Team**: A named, reusable multi-agent structure organized from a user goal. Attributes: member agents (roster), a collaboration pattern (parallel / serial / team-loop), and pattern-specific configuration (e.g., quality dimensions, threshold, iteration cap for a team-loop). This is the primary new concept.
- **Team Configuration**: The persisted representation of a Team that `improve-team` targets and modifies. It is what makes a team "existing" and improvable across sessions.
- **Agent**: A single unit that can be a member of a team. Authored and refined only through the single-agent skills (`create-agent` / `improve-agent`).
- **Conceptual Model**: The shared vocabulary (Role × Stage × Type + Team/Loop) describing how agents and teams relate. Owned by the team domain as a single source of truth.
- **Team Entry Point**: The single command surface (`/speckit.team`) through which all team operations are requested and routed.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can create a team by issuing a single command, without needing to know which underlying skill executes (100% of team-create journeys start at the team entry point).
- **SC-002**: 100% of team operations (create, improve) are reachable through the team entry point, and 0% require the single-agent command.
- **SC-003**: The single-agent skills contain **zero** multi-agent/team orchestration content, verified by inspection of `create-agent` and `improve-agent`.
- **SC-004**: **Zero** dangling references to the former `organize-agents` name remain in the active framework (documentation, registries, skill bodies, symlinks), excluding historical spec archives.
- **SC-005**: A user can adjust an existing team and, in 100% of cases, the parts of the team not targeted by the request remain unchanged.
- **SC-006**: The Conceptual Model is defined in exactly **one** location (single source of truth), and the single-agent authoring skill no longer embeds it.
- **SC-007**: A first-time user correctly identifies where to go for team work versus single-agent work on the first attempt, because each domain has one unambiguous command.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Manual/scripted walkthrough of the team-create journey; confirm the entry point is the sole starting surface.
- **SC-002 Source**: Command/skill routing inspection plus documentation review; enumerate every team operation and confirm its entry surface.
- **SC-003 Source**: Content inspection (search) of the single-agent skill files for orchestration/team keywords; expected count = 0.
- **SC-004 Source**: Repository-wide search for the old skill name across active (non-archived) paths; expected count = 0.
- **SC-005 Source**: Before/after diff of a team configuration across an improve operation; only the intended sections change.
- **SC-006 Source**: Repository-wide search for the Conceptual Model definition; expected authoritative-definition count = 1.
- **SC-007 Source**: Lightweight usability check / documentation review confirming one command per domain.

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "/speckit.team" | FR-001, FR-002, FR-017 |
| `STR-002` | "create-team" | FR-004, FR-005, FR-006, FR-014, FR-016 |
| `STR-003` | "improve-team" | FR-008, FR-009, FR-010, FR-014 |
| `STR-004` | "organize-agents" | FR-005, FR-006, SC-004 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-07-13

- Q: Which feature should this requirement bind to? → A: Create a new feature — Feature ID 027, "Team Management" — distinct from the single-agent "Agents Command" (019).
- Q: Where should the EEI triad and team-supervisor authoring modes live after the split? → A: Move both into the team domain (`create-team`); `create-agent` keeps only single-agent modes (`role`, `supervisor`, `custom`, `project-custom`).
- Q: Should `/speckit.team` also run/execute teams at runtime, or only author them? → A: The team domain owns the full lifecycle — create, improve, and execute; runtime orchestration stays with the team domain, reachable via `/speckit.team`.

## Assumptions

- **Team persistence**: A team is persisted as a durable, reusable team-configuration artifact (mirroring how a single agent persists under `.specify/agents/`), so that `improve-team` has a concrete "existing team" to operate on across sessions. The exact storage location/format is an implementation detail for `/speckit.plan`.
- **Hard rename (no alias)**: Because Spec Kit is an internal framework, `organize-agents` is renamed to `create-team` outright, with all references updated; no backward-compatible alias for the old skill name is maintained in the active framework.
- **Single-agent command scope**: `/speckit.agents` remains the single entry point for single-agent operations (`create-agent`, `improve-agent`) and stops routing any team/organize/execute intent to the team domain.
- **Member agents already exist or are authored separately**: Team creation composes existing agents; authoring a brand-new member agent is done through the single-agent path, not inside `create-team`.
- **Terminology continuity**: The collaboration patterns keep their current meaning (parallel dispatch, serial chain, team loop); this feature relocates and re-scopes them rather than redefining them.
