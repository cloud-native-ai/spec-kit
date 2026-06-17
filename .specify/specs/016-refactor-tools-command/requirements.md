# Requirements Specification: Refactor Tools Command — Definition-First Model

**Requirement Branch**: `016-refactor-tools-command`  
**Created**: 2026-06-17  
**Status**: Draft  
**Input**: User description: "重构/speckit.tools命令,这个命令的核心应该是"定义"工具而不是"发现"工具. 这个命令的核心作用应该是创建和修改有明确的定义和行为逻辑的工具,避免因为大语言模型内置的知识和上下文的干扰到的工具使用错误."

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: 016  
**Feature Name**: Tools Command

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
-->

### User Story 1 - Define a New Tool with Explicit Behavior (Priority: P1)

As a Spec Kit user, I want to define a new tool via `/speckit.tools` by describing its name, purpose, parameters, expected outputs, and behavioral rules, so the AI agent invokes it exactly as I intended — without guessing from its built-in knowledge.

**Why this priority**: The entire refactoring is motivated by the need to replace discovery-driven (and thus LLM-knowledge-dependent) tool resolution with author-controlled, explicit definitions. If tool definition does not work correctly, the rest of the command has no foundation.

**Independent Test**: Can be fully tested by running `/speckit.tools` with a tool description, verifying a complete tool definition record is persisted at `.specify/memory/tools/<tool-name>.md`, and confirming every mandatory field is populated from user-provided input rather than inferred by the LLM.

**Acceptance Scenarios**:

1. **Given** no prior tool record exists for the named tool, **When** the user invokes `/speckit.tools` with a tool name and describes its purpose, parameters, and expected output, **Then** a new tool definition record is created at `.specify/memory/tools/<tool-name>.md` containing all user-supplied fields and no LLM-inferred defaults for mandatory fields.
2. **Given** the user provides a tool name that matches a common system utility (e.g., "curl", "grep"), **When** the tool definition is created, **Then** the record captures only the user's stated purpose and parameter constraints — not a generic description derived from the LLM's general knowledge of that utility.
3. **Given** a tool definition record has been created, **When** the AI agent encounters a request to use this tool, **Then** the agent references the persisted definition record and follows the behavioral rules specified there, rather than relying on its own training data about the tool.

---

### User Story 2 - Modify an Existing Tool Definition (Priority: P2)

As a Spec Kit user, I want to update an existing tool's definition — including its parameters, behavioral rules, or usage constraints — so the definition stays accurate as the tool evolves without requiring deletion and recreation.

**Why this priority**: Tools change over time (new parameters, deprecated options, different output formats). If definitions cannot be modified in place, users will either work with stale definitions or resort to delete-and-recreate workflows, increasing the risk of drift and inconsistency.

**Independent Test**: Can be fully tested by modifying a field in an existing tool definition record and verifying the updated record reflects the change while preserving unmodified fields.

**Acceptance Scenarios**:

1. **Given** a tool definition record already exists, **When** the user invokes `/speckit.tools` referencing that tool and specifies updated parameters or behavioral rules, **Then** the existing record is updated in place with only the changed fields modified.
2. **Given** a tool definition record exists with behavioral rules, **When** the user adds a new constraint (e.g., "never pass flag --force"), **Then** the constraint is appended to the behavioral rules section and preserved in subsequent reads.

---

### User Story 3 - Preview Tool Invocation Before Execution (Priority: P3)

As a Spec Kit user, I want to see a complete invocation preview — showing the resolved command, parameters, and behavioral constraints — before the tool is actually executed, so I can catch mismatches between intent and execution before they cause errors.

**Why this priority**: Preview is the safety mechanism that makes the definition-first model trustworthy. Without it, users cannot verify that the AI agent is honoring the definition rather than improvising.

**Independent Test**: Can be fully tested by requesting a tool invocation, verifying the preview is displayed with all resolved values, and confirming execution does not proceed until explicit user consent.

**Acceptance Scenarios**:

1. **Given** a verified tool definition exists and the user requests tool invocation, **When** the preview is displayed, **Then** it shows the exact command, all resolved parameter values, applicable behavioral constraints, and expected output shape.
2. **Given** the preview is displayed, **When** the user declines execution, **Then** no invocation occurs and the session is marked as cancelled.
3. **Given** the preview is displayed, **When** the user confirms execution, **Then** the tool is invoked exactly as previewed with no additional parameters or modifications introduced by the AI agent.

---

### User Story 4 - View Tool Definition Details (Priority: P4)

As a Spec Kit user, I want to view the complete definition of any registered tool so I can understand its purpose, constraints, and behavioral rules before deciding to invoke or modify it.

**Why this priority**: Read access to definitions is prerequisite for users to trust and maintain the tool registry, but it delivers no value without create (P1) and update (P2) flows being functional first.

**Independent Test**: Can be fully tested by invoking `/speckit.tools` with a tool name in view mode and verifying all definition fields are displayed.

**Acceptance Scenarios**:

1. **Given** a tool definition record exists, **When** the user invokes `/speckit.tools` with the tool name and no modification intent, **Then** the complete definition is displayed including name, type, source, description, parameters, returns, behavioral rules, and aliases.
2. **Given** multiple tool definitions exist, **When** the user invokes `/speckit.tools` without specifying a tool name, **Then** a list of all registered tools is shown with name, type, and one-line description.

---

### Edge Cases

- What happens when the user defines a tool with the same name as an existing tool of a different type (e.g., a project-script "deploy" vs. a shell-function "deploy")?
- How does the system handle a tool definition that references a source (script path, binary) that does not currently exist on the system?
- What happens when a tool definition's behavioral rules contradict the tool's actual capabilities (e.g., "never return error codes" for a script that may fail)?
- How does the system behave when the user attempts to invoke a tool whose definition record is incomplete (missing mandatory fields)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The `/speckit.tools` command MUST treat tool definition (create and modify) as the primary action, not tool discovery or invocation.
- **FR-002**: When creating a new tool definition, the system MUST require the user to provide at minimum: tool name, tool type, source identifier, and description — these fields MUST NOT be auto-populated from the LLM's built-in knowledge.
- **FR-003**: Each tool definition record MUST include a "Behavioral Rules" section where users can specify constraints, guardrails, and usage patterns that the AI agent must follow when invoking the tool. Each rule MUST be a markdown bullet prefixed with an RFC 2119 keyword (`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`) followed by free-form constraint text.
- **FR-004**: Tool definition records MUST be persisted as structured markdown files at `.specify/memory/tools/<tool-name>.md` with a deterministic `tool_id` derived from the canonical file path.
- **FR-005**: When modifying an existing tool definition, the system MUST perform field-level updates — changed fields are updated, unchanged fields are preserved, and no fields are re-inferred from LLM knowledge.
- **FR-006**: The system MUST validate that all mandatory fields (name, type, source identifier, description) are present and non-empty before marking a tool definition as "Verified".
- **FR-007**: Tool type MUST be one of three canonical values: `project-script`, `system-binary`, or `shell-function`.
- **FR-008**: Before any tool invocation, the system MUST display a complete preview showing the resolved command, parameters, behavioral constraints, and expected output shape, and MUST NOT proceed until the user provides explicit confirmation.
- **FR-009**: The system MUST register each created or updated tool in the Resource Registry (Tools subsection) of `.specify/instructions.md`, keeping entries sorted and deduplicated.
- **FR-010**: When the AI agent encounters a tool that has a definition record, it MUST use the persisted definition — including behavioral rules and parameter specifications — as the authoritative source, not its own training knowledge about the tool.
- **FR-011**: The system MUST support tool aliases so a single tool can be referenced by multiple names, with all aliases resolving to the same canonical definition record.
- **FR-012**: When a tool name conflicts across different tool types, the system MUST require explicit user disambiguation before proceeding with any action.
- **FR-013**: When a user references a tool that has no existing definition record, the system MUST offer to run discovery to scan the system and propose a draft definition — the user MUST review and explicitly confirm every mandatory field before the record is persisted.
- **FR-014**: Discovery-proposed draft definitions MUST be clearly labeled as "Draft — pending user confirmation" and MUST NOT be treated as verified records until the user has reviewed and accepted all mandatory fields.

### Key Entities

- **Tool Definition Record**: The core artifact — a structured file containing a tool's name, type, source identifier, description, parameters, return shape, behavioral rules, aliases, and status. Stored at `.specify/memory/tools/<tool-name>.md`.
- **Behavioral Rules**: A set of user-authored constraints within a tool definition, each expressed as an RFC 2119-prefixed markdown bullet (`MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`), that prescribe or prohibit specific invocation patterns, parameter combinations, or output handling behaviors. These override LLM assumptions.
- **Tool Invocation Session**: A transient session representing one attempt to use a tool, including parameter resolution, preview display, user confirmation, execution, and result reporting.

### Assumptions

- Tool discovery (scanning the system for available binaries, shell functions, or project scripts) remains available as a secondary convenience but is no longer the primary entry point of the command.
- Users are the authoritative source for what a tool does and how it should be used; the LLM's built-in knowledge about tools is treated as fallible and subordinate to the user's definition.
- Existing tool records created under the discovery-first model remain compatible and can be augmented with behavioral rules without migration.
- The refactored command continues to operate as an AI chat instruction (not a terminal command), consistent with the rest of the `/speckit.*` command family.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of tool invocations initiated through `/speckit.tools` use the persisted tool definition record as the authoritative source — zero invocations rely solely on LLM-inferred tool knowledge.
- **SC-002**: Users can create a complete tool definition (all mandatory fields plus at least one behavioral rule) in under 3 minutes via the `/speckit.tools` command.
- **SC-003**: 100% of tool invocations display a preview and require explicit user confirmation before execution.
- **SC-004**: Tool definition modifications preserve all unmodified fields with zero data loss across 100% of update operations.
- **SC-005**: Reduction in tool invocation errors caused by LLM knowledge interference by at least 80% compared to the discovery-first model, as measured by user-reported mismatches between intended and actual tool behavior.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Review of `/speckit.tools` command template logic — verify that all invocation paths reference the tool record before execution. Measurable by code inspection and contract tests.
- **SC-002 Source**: User testing sessions — time from `/speckit.tools` invocation to persisted record creation for 5 representative tool types.
- **SC-003 Source**: Contract tests verifying that the confirmation gate is present in all execution paths within the command template.
- **SC-004 Source**: Integration tests that modify individual fields and assert remaining fields match their pre-modification values.
- **SC-005 Source**: Comparison of user-reported tool invocation error rates before and after the refactoring, collected over a 30-day period post-release.

## Shared Strings *(optional)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "Proceed with execution? (yes/no)" | FR-008, preview confirmation gate |
| `STR-002` | "project-script" | FR-007, tool type validation |
| `STR-003` | "system-binary" | FR-007, tool type validation |
| `STR-004` | "shell-function" | FR-007, tool type validation |
| `STR-005` | "Verified" | FR-006, tool status after validation |

## Clarifications

### Session 2026-06-17

- Q: Should this spec be bound to Feature 016 (Tools Command) or create a new Feature? → A: Bind to Feature 016 — this is a refactoring of the existing tools command, not a new capability.
- Q: When no definition record exists, should discovery assist definition creation or require strict manual input? → A: Discovery assists definition — scan the system and propose a draft for the user to review and confirm before persisting. User retains control at the confirmation gate.
- Q: What structure should behavioral rules use in tool definition records? → A: RFC 2119 keyword bullets — each rule is a markdown bullet prefixed with MUST/MUST NOT/SHOULD/SHOULD NOT, followed by free-form constraint text.
