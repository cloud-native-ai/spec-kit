# Requirements Specification: MCP Tool Call Command

**Requirement Branch**: `002-mcp-tool-call`  
**Created**: 2026-02-10  
**Status**: Draft  
**Input**: User description: "新建一个/speckit.mcpcall命令，这个命令用来指定调用某一个mcp工具，一个mcp工具主要的信息包括：所属的mcp server、mcp tool描述、参数和返回值等。/speckit.mcpcall命令调用后需要通过自动发现和交互的方式补全这些信息，然后在.specify/memory/tools/<mcp tool name>.md路径记录这些信息，每次调用的时候需要判断是否已经存在这样一个文件，如果有则直接使用文件中的内容进行执行，否则就一步一步生成这个文件。"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 选择并调用 MCP 工具 (Priority: P1)

作为使用 Spec Kit 的用户，我希望通过 `/speckit.mcpcall` 指定并调用某一个 MCP 工具，以便快速完成一次工具调用而无需手动整理工具定义信息。

**Why this priority**: 这是核心能力，直接决定命令是否可用。

**Independent Test**: 用户能够在一次调用中完成工具选择、信息补全与执行，并获得可验证的调用结果。

**Acceptance Scenarios**:

1. **Given** 用户在工作区内执行 `/speckit.mcpcall` 并指定目标 MCP 工具，**When** 系统完成工具信息收集，**Then** 工具被成功调用并返回结果。
2. **Given** 用户指定的 MCP 工具尚无本地记录，**When** 系统通过自动发现与交互补全信息，**Then** 生成并保存对应的工具记录文件。

---

### User Story 2 - 复用已有工具记录 (Priority: P2)

作为使用 Spec Kit 的用户，我希望当已有工具记录文件存在时能够直接复用，避免重复的发现与交互流程。

**Why this priority**: 复用能力显著提升效率并保证工具调用一致性。

**Independent Test**: 在已有记录文件的情况下，命令可以直接执行并完成调用，不需要再次补全信息。

**Acceptance Scenarios**:

1. **Given** `.specify/memory/tools/<mcp tool name>.md` 已存在且内容完整，**When** 用户再次调用 `/speckit.mcpcall`，**Then** 系统直接使用文件信息完成工具调用。

---

### Edge Cases

- 当自动发现未找到指定的 MCP 工具时，系统应清晰提示并提供可执行的下一步（例如重新选择或取消）。
- 当工具参数定义不完整或存在冲突时，系统应阻止执行并提示需要补全或修正的信息。
- 当工具记录文件存在但缺失关键字段时，系统应引导用户补全缺失内容后再执行。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系统 MUST 允许用户在调用 `/speckit.mcpcall` 时明确指定目标 MCP 工具。
- **FR-002**: 系统 MUST 通过自动发现获取可用的 MCP Server 与其工具清单，以支持用户选择目标工具。
- **FR-003**: 系统 MUST 通过交互流程收集并确认 MCP 工具的关键信息（所属 MCP Server、工具描述、参数与返回值）。
- **FR-004**: 系统 MUST 在 `.specify/memory/tools/<mcp tool name>.md` 生成并保存 MCP 工具记录文件。
- **FR-005**: 系统 MUST 在工具记录文件存在且内容完整时直接复用其信息完成调用。
- **FR-006**: 系统 MUST 在工具记录文件不存在或不完整时引导用户补全信息后再执行调用。
- **FR-007**: 系统 MUST 在执行前向用户展示将要调用的 MCP 工具信息，以便用户确认。
- **FR-008**: 系统 MUST 在调用完成后提供可核验的结果输出或错误说明。

### Key Entities *(include if requirement involves data)*

- **MCP 工具记录**: 保存工具所属 Server、工具描述、参数、返回值与必要的使用说明。
- **MCP Server**: 工具所属的服务端标识与可用工具集合。
- **工具调用会话**: 一次 `/speckit.mcpcall` 调用过程中的上下文、交互记录与执行结果。

### Assumptions

- 当工具记录文件存在且信息完整时，默认不触发重新发现流程。
- 交互流程在用户确认关键字段后方可执行调用。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 95% 的 `/speckit.mcpcall` 调用可在一次流程中完成工具发现/复用并成功执行。
- **SC-002**: 用户在首次调用新工具时，完成信息补全并执行的平均时间不超过 2 分钟。
- **SC-003**: 已存在工具记录时，用户在 15 秒内即可完成调用并获得结果。
- **SC-004**: 100% 的工具记录文件包含 MCP Server、工具描述、参数与返回值信息。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
