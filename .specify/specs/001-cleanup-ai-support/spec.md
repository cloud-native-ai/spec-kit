# Feature Specification: Cleanup Legacy AI Tools Support

**Feature Branch**: \`001-cleanup-ai-support\`
**Created**: 2026-01-30
**Status**: Draft
**Input**: User description: "我打算彻底抛弃上游跟踪进入独立演进状态，因此需要对代码中上游遗留的功能进行清理。在代码中只保留对"GitHub Copilot"、"Qwen Code"、"opencode"这三个工具的支持，其他的AI 工具都可以删除。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Remove Unsupported AI Tools (Priority: P1)

As a maintainer, I want the codebase to explicitly support only GitHub Copilot, Qwen Code, and opencode, removing all other upstream legacy AI tools, so that the project is cleaner and fully decoupled from upstream dependencies I don't need.

**Why this priority**: Core requirement for independent evolution.

**Independent Test**: Can be tested by searching the codebase for removed provider names and verifying they are absent or defined as unsupported.

**Acceptance Scenarios**:

1. **Given** the codebase, **When** I inspect the list of supported AI providers, **Then** I only see GitHub Copilot, Qwen Code, and opencode.
2. **Given** the codebase, **When** I search for code implementing other providers (e.g., standard OpenAI, Anthropic, Bedrock), **Then** I find no functional implementation code.

---

### User Story 2 - Verify Supported Tools Configuration (Priority: P1)

As a developer, I want to ensure that the configuration system properly recognizes and loads the three supported tools, so that the cleanup doesn't break existing valid workflows.

**Why this priority**: Ensures the cleanup doesn't cause regression for intended usage.

**Independent Test**: Configure the system with each of the 3 supported tools and verify they are accepted.

**Acceptance Scenarios**:

1. **Given** a configuration file specifying "GitHub Copilot", **When** the application loads, **Then** the provider is successfully initialized.
2. **Given** a configuration file specifying "Qwen Code", **When** the application loads, **Then** the provider is successfully initialized.
3. **Given** a configuration file specifying "opencode", **When** the application loads, **Then** the provider is successfully initialized.

### Edge Cases

- What happens if a user provides a configuration for a removed tool?
  - The system should fail gracefully with a clear error message stating the tool is no longer supported.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST remove all code modules, classes, and functions dedicated to AI providers other than GitHub Copilot, Qwen Code, and opencode.
- **FR-002**: The system MUST retain full functional support for **GitHub Copilot**.
- **FR-003**: The system MUST retain full functional support for **Qwen Code**.
- **FR-004**: The system MUST retain full functional support for **opencode**.
- **FR-005**: The configuration loader MUST validate that the selected provider is one of the three supported options.
- **FR-006**: Any command-line arguments or flags specific to removed providers MUST be removed.
- **FR-007**: Documentation and help messages MUST be updated to list only the three supported providers.

### Key Entities *(include if feature involves data)*

- **AI Provider Registry**: Internal registry or mapping that connects provider names to their implementation classes.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Zero references to removed AI providers (e.g., "DeepSeek", "OpenAI" as direct providers) remain in the active code path.
- **SC-002**: Application starts successfully with each of the 3 supported providers.
- **SC-003**: Specifying an unsupported provider results in a clear "unsupported" error, not a crash or silent failure.

## Clarifications
<!-- This section will be populated by /speckit.clarify command -->
