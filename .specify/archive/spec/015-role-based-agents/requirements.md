# Feature Specification: Role-Based Agent Templates

**Feature Branch**: `015-role-based-agents`  
**Created**: 2026-06-17  
**Status**: Draft  
**Input**: User description: "进一步完善agents相关命令和机制,创建预置的agent来扮演软件开发工作流程中的各个角色"

## Related Feature

**Feature ID**: 019  
**Feature Name**: Agents Command

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate role-based agents for a project (Priority: P1)

A project maintainer runs `/speckit.agents` and the system generates six predefined role-based agent files, each tailored to the current project's context (tech stack, directory structure, conventions). The generated agents cover the core software development workflow roles: Requirements Analyst, System Designer, Module Designer, Test Engineer, Quality Assurance Engineer, and Knowledge Manager.

**Why this priority**: This is the core value proposition — replacing generic capability-based agent templates with role-based agents that mirror a real software development team structure. Without this, the feature has no value.

**Independent Test**: Can be fully tested by running `/speckit.agents` in a project and verifying that six `.agent.md` files are generated under `.specify/agents/` with role-appropriate content including project-specific context.

**Acceptance Scenarios**:

1. **Given** a project with `/speckit.agents` configured, **When** the user runs `/speckit.agents`, **Then** six role-based agent files are generated under `.specify/agents/`, each named with a role-descriptive kebab-case slug (e.g., `requirements-analyst.agent.md`, `system-designer.agent.md`, `module-designer.agent.md`, `test-engineer.agent.md`, `qa-engineer.agent.md`, `knowledge-manager.agent.md`)
2. **Given** a project with existing source code and documentation, **When** agents are generated, **Then** each agent's instructions reference the project's actual tech stack, directory structure, and conventions — not generic placeholders
3. **Given** the six agents are generated, **When** a user invokes any agent (e.g., `@requirements-analyst`), **Then** the agent responds in-character with the role's perspective and responsibilities

---

### User Story 2 - Remove legacy capability-based agent templates (Priority: P1)

The existing `templates/agent-*-template.md` files (agent-common, agent-knowledge, agent-plan, agent-research) are removed and replaced by the new role-based agent templates. The `/speckit.agents` command uses role templates as the source for agent generation instead of the old capability-based templates.

**Why this priority**: Tied to P1 because role-based and capability-based templates cannot coexist as the design philosophy — the old templates must be removed for the new approach to take effect cleanly.

**Independent Test**: Can be tested by verifying that old `templates/agent-*-template.md` files no longer exist and that `/speckit.agents` exclusively uses role-based templates for generation.

**Acceptance Scenarios**:

1. **Given** the current codebase contains `templates/agent-common-template.md`, `agent-knowledge-template.md`, `agent-plan-template.md`, and `agent-research-template.md`, **When** the migration is complete, **Then** these four files are removed from `templates/`
2. **Given** the old templates are removed, **When** `/speckit.agents` is executed, **Then** it uses the new role-based templates to generate agents

---

### User Story 3 - Agents collaborate through workflow handoffs (Priority: P2)

Each role-based agent clearly defines its upstream inputs and downstream outputs, enabling structured handoffs between roles. For example, the Requirements Analyst produces clarified requirements that feed into the System Designer, who produces designs that feed into the Module Designer and Test Engineer.

**Why this priority**: Handoff definitions are what make the role-based agents more than persona prompts — they create a structured development workflow. However, individual agents are still useful without explicit handoffs.

**Independent Test**: Can be tested by examining each agent's instructions for explicit upstream/downstream references and verifying that agent outputs match the expected inputs of downstream agents.

**Acceptance Scenarios**:

1. **Given** the Requirements Analyst agent produces a requirements document, **When** the System Designer agent is invoked, **Then** it can accept the Requirements Analyst's output as its input context
2. **Given** the Module Designer produces implementation changes, **When** the Test Engineer agent is invoked, **Then** it references the Module Designer's changes as the scope for test design
3. **Given** the Quality Assurance Engineer completes a review, **When** the review finds gaps, **Then** it references back to the System Designer's design and the Requirements Analyst's requirements as the authoritative baselines

---

### User Story 4 - Dynamic context injection during agent generation (Priority: P2)

When `/speckit.agents` generates role-based agents, it reads the project's current state (codebase structure, existing specs, feature index, constitution) and injects relevant context into each agent's template. Each role receives the context most relevant to its responsibilities.

**Why this priority**: Dynamic context injection is what makes generated agents project-aware rather than generic. Critical for agent usefulness but depends on the core role templates existing first.

**Independent Test**: Can be tested by comparing generated agents across two projects with different tech stacks and verifying that agent instructions differ in project-specific details while maintaining consistent role structure.

**Acceptance Scenarios**:

1. **Given** a Python project with a `src/` layout, **When** agents are generated, **Then** the Module Designer agent references the actual module structure under `src/`
2. **Given** a project with an existing constitution at `.specify/memory/constitution.md`, **When** agents are generated, **Then** the Quality Assurance Engineer agent references the constitution's principles as quality baselines
3. **Given** a project with feature index at `.specify/memory/features.md`, **When** agents are generated, **Then** the System Designer agent references the feature index for architectural context

---

### Edge Cases

- What happens when a project has no existing specs or constitution? Agents should still generate with sensible defaults and note that project-specific context was not available.
- How does the system handle a project with an unconventional directory structure? Agents describe what they found, not assume a standard layout.
- What happens when only a subset of roles is needed? The system generates all six by default; users can delete the ones they don't need.
- What happens when agents are regenerated after project evolution? New context is reflected; existing agent customizations should prompt a warning before overwriting.
- What happens when user-created agents (e.g., `code-reviewer.agent.md`) already exist? They are preserved — only role-based agents are created or updated.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide six role-based agent templates, one for each role: Requirements Analyst, System Designer, Module Designer, Test Engineer, Quality Assurance Engineer, and Knowledge Manager
- **FR-002**: Each role-based agent template MUST define the role's identity, responsibilities, upstream inputs, downstream outputs, workflow steps, and expected output format
- **FR-003**: The `/speckit.agents` command MUST generate all six role-based agents when invoked, dynamically incorporating the current project's context (tech stack, directory structure, existing specs, constitution)
- **FR-004**: Generated agent files MUST follow the `.agent.md` format with YAML frontmatter (name, description, tools, user-invocable, etc.) and be placed in `.specify/agents/`
- **FR-005**: The existing capability-based templates (`templates/agent-common-template.md`, `agent-knowledge-template.md`, `agent-plan-template.md`, `agent-research-template.md`) MUST be removed and replaced by the new role-based templates
- **FR-006**: Each agent MUST clearly define its position in the development workflow — who provides its inputs and who consumes its outputs
- **FR-007**: Agent templates MUST use placeholder variables that are resolved at generation time based on project analysis
- **FR-008**: The system MUST preserve any existing user-created agents when generating role-based agents — only role-based agent files are created or updated
- **FR-008a**: When regenerating role-based agents, the system MUST detect whether an existing role-based agent file has been modified by the user; if so, it MUST create a `.bak` copy of the customized file before overwriting with the newly generated version, and warn the user about the backup
- **FR-009**: Each agent's instructions MUST be written in the agent's role perspective (first-person professional identity), not as a generic assistant
- **FR-009a**: All role-based agents MUST receive full read-write tool access; role boundaries are enforced through the agent's behavioral instructions, not through tool permission restrictions
- **FR-010**: The system MUST maintain symlink compatibility between `.specify/agents/` and tool-specific agent directories as established by the existing agent framework

### Role Definitions

- **Requirements Analyst** (`requirements-analyst.agent.md`): Interface between software users and the development team. Clarifies and analyzes requirements, translating external/business language into internal project terminology and structured specifications.
  - *Upstream*: User/stakeholder input
  - *Downstream*: System Designer

- **System Designer** (`system-designer.agent.md`): Maintains the holistic view of project architecture. Designs overall implementation approaches based on requirements, considering system-wide impacts, integration points, and architectural constraints.
  - *Upstream*: Requirements Analyst
  - *Downstream*: Module Designer, Quality Assurance Engineer

- **Module Designer** (`module-designer.agent.md`): Deep expertise in specific subsystems/modules. Designs detailed implementation within module boundaries, respecting upstream/downstream interface contracts and programming conventions. Does not need full system visibility.
  - *Upstream*: System Designer
  - *Downstream*: Test Engineer

- **Test Engineer** (`test-engineer.agent.md`): Designs, writes, and executes test cases from an acceptance perspective. Validates that module implementations meet their specifications. Feeds test results back to Module Designer for iteration.
  - *Upstream*: Module Designer
  - *Downstream*: Module Designer (feedback loop), Quality Assurance Engineer

- **Quality Assurance Engineer** (`qa-engineer.agent.md`): Full-system quality oversight. Validates that the integrated system matches the System Designer's architecture and satisfies the Requirements Analyst's requirements. Focuses on systemic quality, not code-level details.
  - *Upstream*: System Designer, Test Engineer
  - *Downstream*: Requirements Analyst (gap feedback)

- **Knowledge Manager** (`knowledge-manager.agent.md`): Manages project knowledge assets — documentation, knowledge base maintenance, onboarding materials, and decision records. Ensures project knowledge is current, discoverable, and consistent.
  - *Upstream*: All roles
  - *Downstream*: All roles

### Key Entities

- **Role Template**: A parameterized `.md` template in `templates/` that defines a development workflow role (identity, responsibilities, workflow, inputs/outputs) with project-context placeholders
- **Generated Agent**: A concrete `.agent.md` file in `.specify/agents/` produced by resolving a Role Template against the current project's context
- **Workflow Handoff**: A defined input→output relationship between two roles, specifying what artifact type flows between them

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All six role-based agents are generated by a single `/speckit.agents` invocation in under 2 minutes
- **SC-002**: Generated agents produce role-appropriate responses when invoked — a Requirements Analyst focuses on requirements clarification, a System Designer focuses on architecture, etc.
- **SC-003**: 100% of generated agents contain project-specific context (not generic placeholders) when the project has existing code and documentation
- **SC-004**: Existing user-created agents are never modified or deleted during role-based agent generation
- **SC-005**: The workflow handoff chain (Requirements Analyst → System Designer → Module Designer → Test Engineer → Quality Assurance Engineer) can be traced through the agents' documented inputs and outputs
- **SC-006**: Teams using the role-based agents can execute a complete requirements→design→implement→test→review cycle with each agent contributing its defined perspective

### Measurement Sources & Collection Methods

- **SC-001 Source**: Manual timing of `/speckit.agents` execution; measured per invocation
- **SC-002 Source**: Manual invocation of each agent with a sample task; evaluated by checking that responses stay within the role's defined scope
- **SC-003 Source**: Automated diff of generated agents across two projects with different stacks; verify project-specific sections differ
- **SC-004 Source**: File system comparison before and after agent generation; verify non-role agent files are untouched
- **SC-005 Source**: Manual inspection of each agent's upstream/downstream documentation; verify chain completeness
- **SC-006 Source**: End-to-end walkthrough using all six agents on a sample feature; verify each role contributes meaningfully

## Assumptions

- The project uses the existing `.specify/` workspace structure with agents stored in `.specify/agents/`
- The `/speckit.agents` command already exists and handles agent generation — this spec extends its behavior with role-based templates
- The existing agent file format (`.agent.md` with YAML frontmatter) is sufficient for role-based agents
- All six roles are relevant to most software projects; users can remove unused agents after generation
- The existing symlink model (`.specify/agents/` → `.github/agents/` etc.) continues to work for role-based agents
- Agent templates are stored in `templates/` alongside other Spec Kit templates

## Clarifications

### Session 2026-06-17

- Q: Should this spec be bound to Feature 019 (Agents Command) or create a new Feature? → A: Bind to Feature 019 — role-based templates are a further evolution of the existing agent system.
- Q: What should happen when a user has customized a role-based agent and re-runs `/speckit.agents`? → A: Warn and backup — detect modifications, create a `.bak` copy of the customized file, then overwrite with the newly generated version.
- Q: Should the spec define tool permission scoping per role (read-only vs read-write)? → A: All read-write — every role gets full tool access; the agent's behavioral instructions guide scope, not tool restrictions.
