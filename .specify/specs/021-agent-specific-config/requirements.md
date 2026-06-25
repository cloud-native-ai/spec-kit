# Feature Specification: Agent-Specific Configuration for Commands and Skills

**Feature Branch**: `021-agent-specific-config`  
**Created**: 2026-06-25  
**Status**: Draft  
**Input**: User description: "为所有的命令和skill都添加一个"Agent特定配置和说明", 目前speckit框架中的commands和skills对所有的AI Agent工具都一视同仁,都是使用"通用配置".但是在实际执行的过程中不同的Agent工具的差别会比较大. 需要在 "templates/commands/agents.md", "templates/commands/skills.md", "templates/commands/tools.md", "skills/browser-utils", "skills/create-agent", "skills/improve-agent", "skills/improve-skills" 等和特定工具高度相关的命令和技能中添加对应的"特定工具优化"章节, 这些章节需要执行以下步骤:1)识别当前工具是什么: claude code,copilot,qoderwork等等;2)根据工具引入特定工具需要注意的事项和工具特定的方法(使用references子文档);3)回顾执行流程中当前工具执行中遇到的阻碍,生成新的feedback文档供持续优化."

## Related Feature *(mandatory)*

**Feature ID**: 022  
**Feature Name**: AI Tools Support

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Agent-Aware Command Execution (Priority: P1)

A Spec Kit user runs `/speckit.agents` from Claude Code. The command template detects that the executing agent is Claude Code and loads Claude Code-specific guidance from a references subdocument. The guidance includes tool-specific best practices (e.g., Claude Code's `Agent` tool for subagent delegation, `Edit` vs `Write` tool preferences, hook-based automation). The user gets optimized output that leverages Claude Code's unique capabilities instead of generic, lowest-common-denominator instructions.

**Why this priority**: This is the core value proposition — making commands produce better results by adapting to the specific AI agent executing them. Without this, all agents receive identical instructions that may reference capabilities they don't have or miss capabilities they do.

**Independent Test**: Can be fully tested by running `/speckit.agents` from Claude Code and verifying that the output includes Claude Code-specific guidance sections, while the same command run from Copilot includes Copilot-specific guidance instead.

**Acceptance Scenarios**:

1. **Given** a command template with an Agent-Specific Configuration section, **When** the command is executed from Claude Code, **Then** the template identifies the executing agent as "Claude Code" and loads the corresponding references subdocument.
2. **Given** a command template with an Agent-Specific Configuration section, **When** the command is executed from GitHub Copilot, **Then** the template identifies the executing agent as "GitHub Copilot" and loads the Copilot-specific references subdocument.
3. **Given** a command template with an Agent-Specific Configuration section, **When** the executing agent cannot be identified, **Then** the template falls back to generic/universal guidance without errors.

---

### User Story 2 - Tool-Specific References for Skills (Priority: P1)

A Spec Kit user runs the `browser-utils` skill from Qoder. The skill detects Qoder as the executing agent and loads Qoder-specific references that describe how to handle browser automation within Qoder's execution model (e.g., tool call syntax differences, output format preferences, available shell capabilities). The user avoids common pitfalls that arise from the skill assuming Claude Code or Copilot-specific capabilities.

**Why this priority**: Skills like `browser-utils`, `create-agent`, `improve-agent`, and `improve-skills` are highly tool-dependent. Their workflows reference specific tool capabilities (shell execution, file editing, subagent delegation) that differ significantly across agents. Without agent-specific references, these skills frequently fail or produce suboptimal results on non-primary agents.

**Independent Test**: Can be fully tested by examining the `browser-utils` SKILL.md for an Agent-Specific Configuration section that references tool-specific subdocuments, and verifying the referenced files exist with meaningful content for at least two different agents.

**Acceptance Scenarios**:

1. **Given** the `browser-utils` skill with agent-specific references, **When** executed from Claude Code, **Then** the skill references Claude Code-specific patterns (e.g., using `Bash` tool for Playwright execution, `Read` tool for screenshot review).
2. **Given** the `create-agent` skill with agent-specific references, **When** executed from GitHub Copilot, **Then** the skill references Copilot-specific patterns (e.g., `.agent.md` frontmatter fields specific to Copilot's agent system).
3. **Given** a skill with agent-specific references, **When** the executing agent has no dedicated references subdocument, **Then** the skill uses the generic guidance and notes the absence for future reference creation.

---

### User Story 3 - Execution Feedback Generation (Priority: P2)

After a command or skill execution encounters agent-specific obstacles (e.g., a tool call fails because the agent doesn't support that tool type, or output format doesn't match the agent's expectations), the framework generates a structured feedback document capturing the obstacle, the agent context, and suggested improvements. This feedback document is stored in a predictable location and can be consumed by `/speckit.improve-skills` or `/speckit.improve-agent` for continuous optimization.

**Why this priority**: This completes the feedback loop. Without structured feedback capture, agent-specific issues are lost between sessions, and the same problems recur. However, the primary value (P1) comes from the detection and references — feedback generation builds on that foundation.

**Independent Test**: Can be fully tested by intentionally triggering an agent-specific obstacle during skill execution and verifying that a feedback document is created with the expected structure (agent identity, obstacle description, suggested fix, timestamp).

**Acceptance Scenarios**:

1. **Given** a command execution that encounters an agent-specific obstacle, **When** the execution completes (successfully or with workarounds), **Then** a feedback document is generated at a predictable path capturing the obstacle and agent context.
2. **Given** existing feedback documents from prior executions, **When** a user runs `/speckit.improve-skills` targeting a skill, **Then** the improvement workflow can discover and incorporate the agent-specific feedback as evidence.

---

### Edge Cases

- What happens when a new AI agent tool is added to Spec Kit that has no references subdocuments yet? The system falls back to generic guidance and logs a note suggesting reference creation.
- What happens when an agent identification is ambiguous (e.g., a Copilot extension running in a terminal context)? The system uses the most specific match available and documents the ambiguity.
- What happens when references subdocuments for different agents contradict each other? Each agent's references are independent; contradictions are acceptable because they reflect genuinely different tool behaviors.
- How does the system handle agent-specific sections in templates that are not tool-dependent (e.g., `/speckit.requirements`, `/speckit.plan`)? Non-tool-dependent commands do not require agent-specific sections; the feature targets only commands and skills where tool differences materially affect execution.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each targeted command template (`templates/commands/agents.md`, `templates/commands/skills.md`, `templates/commands/tools.md`) MUST include an "Agent-Specific Configuration" section that defines the three-step agent adaptation workflow: identify → load references → capture feedback.
- **FR-002**: Each targeted skill (`skills/browser-utils`, `skills/create-agent`, `skills/improve-agent`, `skills/improve-skills`) MUST include an "Agent-Specific Configuration" section in its SKILL.md following the same three-step workflow.
- **FR-003**: The agent identification step MUST support all officially supported AI tools: Claude Code, GitHub Copilot, Qwen Code, opencode, Qoder, and any Tier 2 agents (Hermes-Agent, iFlow).
- **FR-004**: Agent identification MUST use environmental signals available to the executing agent (e.g., tool-specific environment variables, file system markers, command invocation context) rather than requiring explicit user input.
- **FR-005**: Each targeted skill (`skills/browser-utils`, `skills/create-agent`, `skills/improve-agent`, `skills/improve-skills`) MUST maintain a `references/` subdirectory containing per-agent reference documents named `<agent-slug>-guide.md` (e.g., `claude-code-guide.md`, `copilot-guide.md`). Command templates (`templates/commands/*.md`) MUST embed agent-specific guidance inline within the Agent-Specific Configuration section rather than using separate reference files.
- **FR-006**: Reference documents MUST contain agent-specific guidance including: tool capabilities and limitations relevant to the command/skill, preferred tool call patterns, known pitfalls, and workarounds.
- **FR-007**: When the executing agent cannot be identified or has no corresponding reference document, the command or skill MUST fall back to generic execution without errors.
- **FR-008**: The feedback generation step MUST produce a structured markdown document capturing: agent identity, execution timestamp, obstacle encountered, workaround applied (if any), and suggested improvement for the command/skill template.
- **FR-009**: Feedback documents MUST be stored at `.specify/memory/feedback/<skill-or-command>-<agent-slug>-<timestamp>.md`, centralizing all agent-specific execution feedback for cross-cutting analysis and discovery by `/speckit.improve-skills` and `/speckit.improve-agent`.
- **FR-010**: The Agent-Specific Configuration section MUST be additive — it augments existing command/skill behavior without modifying the core workflow or breaking execution for agents without specific references.
- **FR-011**: Reference documents MUST use the `${SKILL_HOME}/references/` path convention for skills. Command templates do not use separate reference files; agent-specific guidance is embedded inline.

### Key Entities

- **Agent Profile**: Represents a supported AI agent tool with its identity slug, detection signals, and capability characteristics. Used for agent identification.
- **Agent Reference Document**: A per-agent markdown file containing tool-specific guidance. For skills, lives in the `${SKILL_HOME}/references/` subdirectory. For command templates, guidance is embedded inline within the template file itself.
- **Execution Feedback Document**: A structured capture of agent-specific execution obstacles. Contains agent identity, timestamp, obstacle description, and improvement suggestions. Stored centrally at `.specify/memory/feedback/`.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 7 targeted files (3 command templates + 4 skills) contain an Agent-Specific Configuration section following the three-step workflow within one release cycle.
- **SC-002**: At least 2 agent reference documents exist per targeted command/skill (covering the 2 most-used agents: Claude Code and GitHub Copilot) at launch.
- **SC-003**: Commands and skills executed from a supported agent with a reference document produce agent-tailored output in 100% of executions.
- **SC-004**: Commands and skills executed from an unrecognized agent complete successfully without errors in 100% of executions (graceful fallback).
- **SC-005**: Feedback documents generated during execution contain all required fields (agent identity, timestamp, obstacle, suggestion) in 100% of cases where an agent-specific obstacle is encountered.
- **SC-006**: The `improve-skills` workflow successfully discovers and incorporates agent-specific feedback documents as improvement evidence.

### Measurement Sources & Collection Methods

- **SC-001 Source**: File inspection — verify presence of "Agent-Specific Configuration" section heading in all 7 target files.
- **SC-002 Source**: File system check — count `*-guide.md` files in each target's `references/` subdirectory.
- **SC-003 Source**: Manual execution testing — run each targeted command/skill from Claude Code and Copilot, verify agent-specific content appears in output.
- **SC-004 Source**: Manual execution testing — run each targeted command/skill from an unrecognized agent context, verify clean completion.
- **SC-005 Source**: File inspection of generated feedback documents after intentional obstacle scenarios.
- **SC-006 Source**: Run `improve-skills` targeting a skill with existing feedback documents, verify feedback is cited in the improvement analysis.

## Assumptions

- Agent identification can be performed reliably using environmental signals (environment variables, file system markers) without requiring user input. This is a reasonable assumption given that each supported tool sets distinctive environment variables or runs from distinctive paths.
- The `references/` subdirectory pattern already established for skills (`${SKILL_HOME}/references/`) is used for skill-level agent references. Command templates use inline guidance to avoid restructuring single-file templates into directories.
- Feedback documents are a supplement to, not a replacement for, the existing `improve-skills` evidence-gathering workflow.
- Not all commands and skills need agent-specific sections — only those where tool differences materially affect execution quality. The initial scope is limited to 7 high-impact targets.

## Clarifications

### Session 2026-06-25

- Q: Which Feature should this spec bind to? → A: Feature 022 (AI Tools Support) — extends multi-tool support from initialization/coexistence to runtime template adaptation.
- Q: How should agent-specific reference documents be organized for command templates? → A: `references/` subdirectories for skills only; command templates embed agent-specific guidance inline to avoid restructuring single-file templates.
- Q: Where should agent-specific execution feedback documents be stored? → A: Centralized at `.specify/memory/feedback/<skill-or-command>-<agent-slug>-<timestamp>.md` for cross-cutting analysis.
