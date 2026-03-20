# Requirements Specification: Speckit Tools Command

**Requirement Branch**: `004-speckit-tools-command`  
**Created**: 2026-03-02  
**Status**: Draft  
**Input**: User description: "将旧的 MCP-only 命令体系统一到 /speckit.tools，这个命令的主要作用是将 AI Agent 对 tool 的调用进行显式说明。默认情况下 agent 调用哪些工具都是封装在 agent 内部的，而 templates/commands/tools.md 的作用就是将工具显式输出到 .specify/memory/tools/<tool name>.md 文档中，供 AI Agent 用户查看、封装和重命名等。将 /speckit.tools 进行泛化，使之不仅仅只支持 MCP tool。"

## User Scenarios & Testing *(mandatory)*

<!--
  IMPORTANT: User stories should be PRIORITIZED as user journeys ordered by importance.
  Each user story/journey must be INDEPENDENTLY TESTABLE - meaning if you implement just ONE of them,
  you should still have a viable MVP (Minimum Viable Product) that delivers value.
  
  Assign priorities (P1, P2, P3, etc.) to each story, where P1 is the most critical.
  Think of each story as a standalone slice of functionality that can be:
  - Developed independently
  - Tested independently
  - Deployed independently
  - Demonstrated to users independently
-->

### User Story 1 - 显式说明并调用工具 (Priority: P1)

作为使用 Spec Kit 的用户，我希望通过 `/speckit.tools` 显式指定一个工具并查看其可执行信息，从而在 AI Agent 调用前清楚知道工具来源、参数与预期结果。

**Why this priority**: 这是命令的核心价值，直接决定用户能否把“隐式工具调用”转为“可见、可理解、可复用”的流程。

**Independent Test**: 用户执行 `/speckit.tools <tool-name>` 后，可在一次流程中看到工具信息摘要并完成一次受控调用或取消。

**Acceptance Scenarios**:

1. **Given** 用户在工作区执行 `/speckit.tools` 并提供目标工具名，**When** 系统识别到可匹配工具，**Then** 系统展示该工具的来源、描述、参数与返回信息摘要。
2. **Given** 工具记录不存在，**When** 系统完成工具信息发现与补全，**Then** 系统生成对应工具记录并继续执行后续确认流程。

---

### User Story 2 - 复用与封装工具记录 (Priority: P2)

作为使用 Spec Kit 的用户，我希望当工具记录已存在时直接复用该记录，并可基于记录进行封装与重命名，减少重复输入。

**Why this priority**: 复用能力决定命令的持续效率，封装与重命名能力决定记录是否能成为团队可维护资产。

**Independent Test**: 在已有工具记录的情况下，用户无需重新发现即可完成调用，并可更新记录名称或别名后再次复用。

**Acceptance Scenarios**:

1. **Given** `.specify/memory/tools/<tool name>.md` 已存在且字段完整，**When** 用户再次调用 `/speckit.tools`，**Then** 系统直接复用记录完成确认与调用流程。
2. **Given** 用户希望以更易读名称管理工具记录，**When** 用户提交封装或重命名意图，**Then** 系统按规则更新记录并保证后续可检索与可调用。

---

### User Story 3 - 泛化到多类工具生态 (Priority: P3)

作为使用 Spec Kit 的用户，我希望 `/speckit.tools` 不只支持 MCP 工具，还支持系统命令、Shell 函数与项目脚本等工具类型，以统一查看与调用入口。

**Why this priority**: 泛化能力将命令从单一场景升级为统一工具入口，提升在复杂工作流中的适配范围。

**Independent Test**: 用户分别选择 MCP、System、Shell、Project 四类工具中的任一工具，均可走通同一套记录与确认流程。

**Acceptance Scenarios**:

1. **Given** 用户指定的是非 MCP 工具，**When** 系统完成类型识别，**Then** 系统仍可生成标准化工具记录并支持后续确认调用。
2. **Given** 工具名在不同类型中重名，**When** 用户调用 `/speckit.tools <name>`，**Then** 系统要求用户选择唯一目标后再继续。

---

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- 当目标工具在所有可发现来源中均不存在时，系统应给出候选列表或明确提示“未找到”，并允许用户取消。
- 当同名工具来自多个来源（如 MCP 与 Project 脚本）时，系统应强制用户确认来源，避免误调用。
- 当现有工具记录缺失必填字段时，系统应进入补全过程而不是直接调用。
- 当用户提供的重命名与已有记录冲突时，系统应提示冲突并要求用户确认替代名称。

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: 系统 MUST 使用 `/speckit.tools` 作为唯一命令入口，并在命令说明中明确该命令用于显式说明工具调用。
- **FR-002**: 系统 MUST 允许用户通过 `/speckit.tools` 指定目标工具，并支持在信息不足时引导用户从可发现工具列表中选择。
- **FR-003**: 系统 MUST 支持至少四类工具来源：MCP tools、System binaries、Shell functions、Project scripts。
- **FR-004**: 系统 MUST 为任意受支持工具类型生成或更新标准化工具记录文件，存储于 `.specify/memory/tools/<tool name>.md`。
- **FR-005**: 系统 MUST 在工具记录已存在且完整时优先复用记录，避免重复发现流程。
- **FR-006**: 系统 MUST 在工具记录缺失或不完整时，通过分步交互补全来源、用途说明、参数与返回信息。
- **FR-007**: 系统 MUST 在执行前向用户展示工具基本信息与本次参数摘要，并要求明确确认后才执行。
- **FR-008**: 系统 MUST 支持用户对工具记录进行封装与重命名，并确保更新后记录仍可被 `/speckit.tools` 检索与复用。
- **FR-009**: 系统 MUST 在工具重名、来源冲突或记录命名冲突时阻止直接执行，并提供可操作的消歧引导。
- **FR-010**: 系统 MUST 在调用结束后返回可核验结果，失败时返回可定位问题的错误说明。

### Key Entities *(include if requirement involves data)*

- **工具记录（Tool Record）**: 描述单个工具的统一文档实体，包含工具名、工具类型、来源、用途描述、参数定义、返回信息、别名/封装信息。
- **工具来源（Tool Source）**: 工具所属来源分类（MCP/System/Shell/Project）及其定位信息，用于发现与消歧。
- **工具调用会话（Tool Invocation Session）**: 一次 `/speckit.tools` 交互过程，包含用户输入、参数收集、确认结论与执行结果。

### Assumptions

- 默认保留历史 MCP-only 文档能力的核心语义，但对外命令统一以 `/speckit.tools` 为准。
- 工具记录路径仍统一保存在 `.specify/memory/tools/` 下，文件命名遵循项目现有约定。
- 当工具可被自动发现时，用户无需手动输入底层技术细节。
- 若用户未确认执行，则本次会话仅更新记录，不触发工具调用。

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 95% 的 `/speckit.tools` 调用在一次流程内完成“发现/复用 + 参数确认 + 执行或取消决策”。
- **SC-002**: 在已有工具记录场景下，用户从输入命令到得到执行结果或取消确认的中位时长不超过 20 秒。
- **SC-003**: 在首次使用新工具场景下，用户完成记录创建并获得可执行确认摘要的成功率达到 90% 以上。
- **SC-004**: 100% 新生成的工具记录包含工具类型、来源、参数与返回信息四类核心字段。
- **SC-005**: 对于重名或冲突场景，100% 调用在消歧完成前不发生实际执行。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
