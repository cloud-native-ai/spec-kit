# Requirements Specification: Speckit Agents Command

**Requirement Branch**: `003-speckit-agents-command`  
**Created**: 2026-02-27  
**Status**: Draft  
**Input**: User description: "创建一个新的/speckit.agents命令"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Custom AI Agent (Priority: P1)

As a developer or project maintainer, I want to create a custom AI agent with a specific role and workflow that can be invoked directly or as a subagent, so that I can extend the project's capabilities with workspace-specific automation.

**Why this priority**: This is the core functionality that enables users to define reusable, specialized AI agents tailored to their project's unique needs, providing extensibility beyond built-in commands.

**Independent Test**: Can be fully tested by providing an agent description and verifying that a properly formatted .agent.md file is created in `.github/agents/` with correct YAML frontmatter and role definition.

**Acceptance Scenarios**:

1. **Given** a user provides a clear agent intent with role description, **When** they run `/speckit.agents` with the description, **Then** a new `.agent.md` file is created in `.github/agents/` with appropriate filename and content.
2. **Given** a user runs `/speckit.agents` without arguments, **When** the system analyzes the current conversation and repository context, **Then** it creates a relevant agent based on inferred needs.
3. **Given** a user runs `/speckit.agents` without arguments and intent inference confidence is low, **When** the system evaluates available context, **Then** it does not create an agent and requests one short intent sentence from the user.
4. **Given** `.github/agents/` does not exist, **When** a user runs `/speckit.agents`, **Then** the system creates the directory automatically and continues agent generation.

---

### User Story 2 - Update Existing AI Agent (Priority: P2)

As a developer, I want to refine or update an existing custom AI agent by providing modified constraints or enhanced capabilities, so that I can iteratively improve my agents as project requirements evolve.

**Why this priority**: Projects evolve over time, and agents need to be maintainable and updatable to remain relevant and effective throughout the project lifecycle.

**Independent Test**: Can be fully tested by targeting an existing agent file and verifying that it is updated with new specifications while preserving its core identity.

**Acceptance Scenarios**:

1. **Given** an existing agent file exists in `.github/agents/`, **When** a user provides updated specifications for the same agent role, **Then** the existing file is updated with the new constraints and workflow details.
2. **Given** conflicting updates are provided, **When** the system processes the request, **Then** it resolves conflicts by prioritizing explicit user input over inferred context.
3. **Given** a target agent filename already exists, **When** a user runs `/speckit.agents` for that same name, **Then** the existing file is overwritten with the latest specification.

---

### User Story 3 - Validate Agent Quality and Consistency (Priority: P3)

As a project maintainer, I want the system to validate that created agents meet quality standards including valid YAML frontmatter, consistent tool permissions, and non-contradictory constraints, so that all agents in the project are reliable and well-formed.

**Why this priority**: Quality validation ensures that all custom agents maintain a consistent standard, preventing errors and ensuring predictable behavior across the project.

**Independent Test**: Can be fully tested by creating agents with various potential issues and verifying that the system catches and reports validation problems.

**Acceptance Scenarios**:

1. **Given** an agent specification contains invalid YAML frontmatter, **When** the agent is created, **Then** the system validates and reports the YAML error before saving.
2. **Given** an agent requests tools that don't match its workflow needs, **When** the system analyzes the specification, **Then** it flags the mismatch and suggests appropriate tool permissions.
3. **Given** a user does not specify `tools` permissions, **When** the system generates agent configuration, **Then** it assigns only the minimal tool set required by the declared workflow.

---

### Edge Cases

- Existing agent name with different functionality: system overwrites the existing `.agent.md` file with the latest specification.
- Low-confidence intent inference with empty input: system halts creation and asks for a one-sentence intent clarification.
- Missing `.github/agents/` directory: system creates the directory automatically before writing agent files.
- Contradictory constraints: system prioritizes latest explicit user input; if conflict still remains unresolved, it stops and asks the user to correct constraints.
- Unspecified tools permissions: system defaults to least-privilege tools scoped to the agent workflow.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST create or update AI agent files with `.agent.md` extension in the `.github/agents/` directory
- **FR-002**: System MUST generate kebab-case filenames based on agent display names or roles
- **FR-003**: Users MUST be able to invoke agents directly as commands or use them as subagents in complex workflows
- **FR-004**: System MUST include valid YAML frontmatter with meaningful description, tool permissions, and invocation metadata
- **FR-005**: System MUST validate agent files for YAML correctness, constraint consistency, and tool-workflow alignment before saving
- **FR-006**: System MUST infer agent intent from conversation context when no explicit arguments are provided
- **FR-007**: System MUST provide example prompts that demonstrate how to trigger the created agent
- **FR-008**: System MUST ensure agent roles follow single responsibility principle and are narrowly focused
- **FR-009**: System MUST restrict generated agent guidance to project-approved AI providers (GitHub Copilot, Qwen Code, opencode) and reject unsupported provider references
- **FR-010**: System MUST overwrite existing `.github/agents/<agent-name>.agent.md` when a new request targets the same agent name
- **FR-011**: System MUST stop generation and request a one-sentence user intent when context-based intent inference confidence is below the command threshold
- **FR-012**: System MUST resolve contradictory constraints by prioritizing latest explicit user input, and MUST stop with correction guidance when contradictions remain
- **FR-013**: System MUST create `.github/agents/` automatically when missing and continue generation in the same command execution
- **FR-014**: System MUST apply least-privilege default tool permissions when users do not explicitly provide a tools list

### Key Entities

- **AI Agent**: A reusable configuration file (.agent.md) that defines a specialized AI role with specific capabilities, constraints, and workflows
- **Agent Frontmatter**: YAML metadata at the beginning of agent files that includes description, tool permissions, and invocation settings
- **Agent Workflow**: The defined sequence of actions, decision points, and output formats that govern the agent's behavior

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a functional custom AI agent in under 2 minutes with a single command invocation
- **SC-002**: 100% of created agents pass validation for YAML correctness and constraint consistency
- **SC-003**: All generated agents include clear example prompts that accurately demonstrate their intended usage
- **SC-004**: Agent files are consistently structured with proper frontmatter and role definitions that enable reliable invocation
- **SC-005**: System successfully infers relevant agent specifications from context when no explicit arguments are provided in at least 80% of cases

## Clarifications

### Session 2026-02-27

- Q: 当目标 `.github/agents/<name>.agent.md` 已存在且新需求指向同名代理时，系统应采用哪种默认行为？ → A: Always overwrite existing file.
- Q: 当用户不传参数且系统基于上下文推断 agent 意图时，若推断置信度不足，默认应如何处理？ → A: Stop and ask for one-sentence intent.
- Q: 当用户输入中出现互相冲突的约束时，系统默认应如何决策？ → A: Prioritize latest explicit input; if still conflicting, stop and request correction.
- Q: 当 `.github/agents/` 目录不存在时，`/speckit.agents` 默认应如何处理？ → A: Automatically create directory and continue.
- Q: 当用户未明确指定 `tools` 权限时，`/speckit.agents` 默认应采用哪种权限策略？ → A: Use least-privilege default tools required by workflow.

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
