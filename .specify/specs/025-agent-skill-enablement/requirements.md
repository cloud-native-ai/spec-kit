# Requirements Specification: Agent Skill Enablement

**Requirement Branch**: `025-agent-skill-enablement`  
**Created**: 2026-07-13  
**Status**: Draft  
**Input**: User description: "需要对当前框架中内置的这些 Agent 进行技能的赋能。核心前提是：框架中的技能与 Agent 定义同步安装，因此内置的所有 Agent 均可调用框架提供的技能。在这种情况下，每个 Agent 都应尽可能使用技能执行对应操作。"

## Related Feature *(mandatory)*

**Feature ID**: 026  
**Feature Name**: Agent Skill Enablement

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agents prefer role-relevant skills for their work (Priority: P1)

As a Spec Kit user who invokes a built-in agent (e.g. Requirements Analyst, System Designer, Test Engineer), I expect the agent to accomplish a task by using the framework skill purpose-built for that kind of work — rather than improvising the same operation manually — so that the work is consistent, higher quality, and benefits from the skill's maintained logic.

**Why this priority**: This is the core value the requester asked for. Without it, agents duplicate ad-hoc logic that skills already encapsulate, producing inconsistent results and wasting the framework's shipped capabilities. It is the minimum viable outcome of this feature.

**Independent Test**: Take one built-in agent whose role has an obviously matching skill (e.g. a diagramming task for the System Designer, an end-to-end web test for the Test Engineer). Give it a task covered by that skill and confirm the agent routes the operation through the skill instead of performing it by hand. Delivers value on its own for that agent.

**Acceptance Scenarios**:

1. **Given** a built-in agent whose role has a matching framework skill, **When** it is asked to perform an operation that skill covers, **Then** the agent uses that skill to perform the operation.
2. **Given** a built-in agent's definition, **When** a user reviews it, **Then** the definition states which framework skills the agent uses and for which kinds of operations.
3. **Given** a task with no matching framework skill, **When** the agent performs it, **Then** the agent completes it directly without failing or fabricating a skill reference.

---

### User Story 2 - Declared skills are guaranteed to be invocable (Priority: P2)

As a maintainer, I want every skill an agent declares or references to be one that is actually installed alongside the agents, so that agents never point at a missing capability and skill invocation never fails due to an unresolved reference.

**Why this priority**: The requester's core premise is that skills and agent definitions install together, which makes every referenced skill invocable. Enforcing that no agent references a non-installed skill protects the premise from drifting and prevents broken agent runs.

**Independent Test**: Cross-check every skill named in every built-in agent against the installed skill set; the referenced set must be a subset of the installed set with zero dangling references. Testable without running any agent.

**Acceptance Scenarios**:

1. **Given** the set of installed framework skills, **When** every built-in agent's skill references are collected, **Then** every referenced skill exists in the installed set.
2. **Given** a skill referenced by an agent, **When** the agent invokes it, **Then** the reference resolves to the canonical installed skill and executes.

---

### User Story 3 - Consistent, discoverable skill-usage guidance across all built-in agents (Priority: P3)

As a user comparing or maintaining agents, I want each built-in agent to express its skill usage in the same, discoverable way, so that I can quickly understand any agent's skill behavior and tooling can enumerate agent→skill relationships uniformly.

**Why this priority**: Consistency and discoverability multiply the value of the first two stories and reduce maintenance cost, but the feature still delivers value without perfect uniformity, so this is P3.

**Independent Test**: Inspect all built-in agents and confirm skill usage is declared in the same location/format and that each includes guidance on when to reach for a skill and what to do when none applies.

**Acceptance Scenarios**:

1. **Given** any two built-in agents, **When** their skill declarations are compared, **Then** they use the same declaration format and location.
2. **Given** a built-in agent, **When** a user reads its guidance, **Then** the agent explains when to prefer a skill and how it behaves when a relevant skill is unavailable.

### Edge Cases

- What happens when a role has **no** matching framework skill? The agent must operate normally without a skill (no forced or fabricated skill use).
- What happens when a relevant skill **fails or is unavailable at runtime**? The agent must degrade gracefully to completing the operation directly and surface the failure, not silently stall.
- What happens when **multiple skills** could apply to one operation? The agent must have a deterministic basis for selecting one (e.g. role-relevance / most specific).
- What happens when the **installed skill set changes** (a skill is added or removed)? Agent references must remain a subset of installed skills, with no dangling references introduced.
- What happens to an agent's **supervision / EEI loop and handoff behavior**? Skill enablement must not alter or break existing supervision, tool access, or handoff wiring.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The set of "built-in agents" in scope MUST be explicitly enumerated as the framework's shipped role agents (Requirements Analyst, System Designer, Module Designer, Test Engineer, QA Engineer, Knowledge Manager, UX Analyst).
- **FR-002**: Every built-in agent MUST declare, in its definition, the framework skills relevant to its role.
- **FR-003**: Every built-in agent MUST include guidance instructing it to prefer an applicable framework skill over performing the same operation manually or ad-hoc.
- **FR-004**: The skill(s) each agent declares MUST be selected from the installed skill set based on that agent's role definition — the mapping MUST be meaningful and role-appropriate, not arbitrary (e.g. Requirements Analyst → `draw-plantuml` for UML use-case diagrams; Module Designer → `analysis-project` for project-structure analysis).
- **FR-005**: Every skill referenced by any built-in agent MUST be a member of the framework's installed skill set (no references to non-installed skills; zero dangling references).
- **FR-006**: Skill references MUST use the canonical skill identifier/location so that references resolve to the installed skill.
- **FR-007**: The framework's guarantee that skills and agent definitions install together (making every declared skill invocable by every built-in agent) MUST be preserved and stated as the operating premise.
- **FR-008**: Each built-in agent MUST define fallback behavior for when no relevant skill applies, or when a relevant skill is unavailable/fails — degrading gracefully to direct execution and surfacing failures.
- **FR-009**: Skill-usage declarations MUST use a consistent format and location across all built-in agents so agent→skill relationships can be enumerated uniformly.
- **FR-010**: When an operation could match more than one skill, the agent MUST have a deterministic basis for choosing which skill to use.
- **FR-011**: Skill enablement MUST NOT regress existing agent behavior — existing tool access, supervision/EEI loops, role scope, and handoffs MUST continue to function unchanged.
- **FR-012**: Agents MUST delegate covered operations to the skill rather than duplicating the skill's internal logic inside the agent definition.

### Key Entities *(include if requirement involves data)*

- **Built-in Agent**: A framework-shipped role agent definition; the unit being empowered. Attributes: role identity, responsibilities, declared tools, declared skills, guidance.
- **Framework Skill**: An installed capability that agents can invoke to perform a class of operations. Attributes: canonical identifier/location, purpose, applicable operation types.
- **Agent–Skill Mapping**: The role-appropriate association between a built-in agent and the skills relevant to its responsibilities.
- **Skill-Usage Guidance**: The per-agent instruction describing when to prefer a skill, how one is selected, and fallback behavior when none applies or a skill fails.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of built-in agents (all 7 enumerated role agents) declare at least one role-relevant framework skill.
- **SC-002**: 0 dangling skill references — 100% of skills referenced across all built-in agents exist in the installed skill set.
- **SC-003**: For every operation type that a built-in agent's role shares with an installed skill, the agent's guidance directs it to prefer that skill (100% coverage of identified skill-eligible operations).
- **SC-004**: 0 regressions in existing agent capabilities (tools, supervision/EEI, role scope, handoffs) after the change, verified against pre-change behavior.
- **SC-005**: A user reviewing any single built-in agent can identify which skills it uses and when in under 1 minute, because the declaration format and guidance are consistent across agents.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Static inspection of each built-in agent definition; count agents with ≥1 role-relevant declared skill divided by total built-in agents.
- **SC-002 Source**: Automated cross-check of every skill reference in built-in agents against the installed skill inventory; count of unresolved references (target 0).
- **SC-003 Source**: Review matrix mapping each role's skill-eligible operation types to the agent's guidance directives; percentage of covered operations that direct to a skill.
- **SC-004 Source**: Before/after behavioral comparison and existing test suite results (contract/integration), plus manual verification of supervision/handoff wiring; count of regressions.
- **SC-005 Source**: Reviewer time-on-task sampling across agents; consistency confirmed by comparing declaration format/location across all built-in agents.

## Assumptions

- **Scope of "built-in agents"**: interpreted as the seven framework-shipped role agents under `.specify/agents/` (Requirements Analyst, System Designer, Module Designer, Test Engineer, QA Engineer, Knowledge Manager, UX Analyst). Transient EEI stage sub-agents inherit their parent role's skill context and are not separately enumerated.
- **Skill availability**: taken as guaranteed because skills and agent definitions install together (the requester's stated premise); therefore every built-in agent can technically invoke any installed skill, while each agent's *declared/recommended* set is the curated, role-relevant subset.
- **Role-definition-driven selection**: although all agents can invoke all installed skills, each agent declares the role-relevant subset chosen from its role definition (e.g. Requirements Analyst → `draw-plantuml`; Module Designer → `analysis-project`), keeping guidance meaningful and discoverable; the broader invocation capability is retained as fallback.
- **No new skills required**: this feature wires existing installed skills into agents; it does not mandate authoring new skills.
- **Consistency baseline**: the declaration format follows the framework's existing agent-definition conventions (the supported agent frontmatter/skill field and body-guidance sections) rather than a newly invented format.

## Clarifications

### Session 2026-07-13

- Q: Which feature should this spec bind to? → A: New Feature 026 "Agent Skill Enablement" (its own capability with a clean lifecycle).
- Q: Which agents are the "built-in agents" to be empowered? → A: Only the 7 persistent role agents in `.specify/agents/`; EEI stage sub-agents inherit their parent role's skills.
- Q: How many skills should each agent declare, given all installed skills remain invocable? → A: A role-definition-driven curated subset — each agent selects the skills relevant to its role (e.g. Requirements Analyst → `draw-plantuml` for UML use-case diagrams; Module Designer → `analysis-project` for structure analysis), with all installed skills still invocable as fallback.
