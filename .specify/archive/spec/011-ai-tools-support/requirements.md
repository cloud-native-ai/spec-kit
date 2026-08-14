# Requirements Specification: AI Tools Support

**Requirement Branch**: `011-ai-tools-support`  
**Created**: 2026-05-18  
**Status**: Implemented  
**Input**: User description: "完善所有的AI工具的支持，当前的流程主要是以支持vscode中的github copilot工具为主的，当使用其他AI工具的时候，对应的init命令中缺少必要的框架代码。同时需要支持多个工具共存，在执行init命令的时候如果.specify目录已经存在并且其中的核心文件已经初始化过了，新工具就不应该使用template去覆盖更新过的文件，而是直接使用现有的文件。"

## Related Feature *(mandatory)*

**Feature ID**: 022  
**Feature Name**: AI Tools Support

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 初始化任一受支持 AI 工具 (Priority: P1)

作为使用 Spec Kit 的项目维护者，我希望在新项目初始化时选择任一官方支持的 AI 工具后，都能获得该工具运行 Spec Kit 工作流所需的完整项目脚手架和说明，以便不再只依赖 GitHub Copilot 的默认体验。

**Why this priority**: 这是功能的核心价值；如果某个受支持工具初始化后缺少必要资产，用户将无法可靠进入 spec → plan → tasks → implement 流程。

**Independent Test**: 可以在空项目中分别选择每个官方支持的 AI 工具完成初始化，并确认每个工具都有可发现、可使用、与核心工作流一致的入口和说明。

**Acceptance Scenarios**:

1. **Given** 一个没有 Spec Kit 配置的新项目，**When** 用户选择任一官方支持的 AI 工具执行初始化，**Then** 项目中包含该工具完成核心 Spec Kit 工作流所需的说明、命令入口和配置资产。
2. **Given** 同一个新项目分别选择不同官方支持的 AI 工具初始化，**When** 用户查看每个工具生成的资产，**Then** 每个工具都提供等价的核心工作流覆盖，不出现只适配 GitHub Copilot 的缺口。
3. **Given** 用户选择了一个官方支持但非默认的 AI 工具，**When** 初始化完成，**Then** 用户无需手工复制 GitHub Copilot 专用文件即可开始使用该工具执行 Spec Kit 流程。

---

### User Story 2 - 在已有 Spec Kit 项目中追加工具支持 (Priority: P2)

作为已经使用 Spec Kit 的团队成员，我希望在 `.specify` 核心内容已存在的项目中追加新的 AI 工具支持时，现有核心文件被复用而不是被模板重置，以便保留团队已经更新过的规则、规格记忆和工作流约定。

**Why this priority**: 该场景直接保护现有项目资产，避免引入新工具时覆盖用户已经维护过的核心内容。

**Independent Test**: 可以在一个已有 `.specify` 目录且核心文件已被用户修改的项目中追加第二个 AI 工具，并确认核心内容保持不变，同时新工具可用。

**Acceptance Scenarios**:

1. **Given** 项目已存在 `.specify` 目录且核心文件已初始化并被用户更新，**When** 用户为该项目追加另一个官方支持的 AI 工具，**Then** 初始化流程复用现有核心文件，不用模板覆盖这些文件。
2. **Given** 项目已存在一个 AI 工具的可用配置，**When** 用户追加第二个 AI 工具，**Then** 原工具配置仍可用，新工具配置也可用，二者共享同一套核心 Spec Kit 内容。
3. **Given** 项目核心文件与模板默认内容不同，**When** 追加工具支持完成，**Then** 用户的核心内容差异被保留，并且新增工具引用保留后的核心内容。

---

### User Story 3 - 多工具共存和一致性验证 (Priority: P3)

作为项目负责人，我希望项目可以同时声明和维护多个 AI 工具，并能清楚验证各工具支持范围一致，以便团队成员按个人偏好使用不同工具而不会产生流程分叉。

**Why this priority**: 多工具共存提升团队采用弹性，但在单工具初始化可靠后才产生完整价值。

**Independent Test**: 可以在同一项目中启用多个官方支持的 AI 工具，并通过用户可见清单或检查结果确认每个工具覆盖相同核心命令、说明和入口。

**Acceptance Scenarios**:

1. **Given** 一个项目已经启用多个官方支持的 AI 工具，**When** 用户查看项目的工具支持状态，**Then** 每个工具的可用状态、覆盖范围和缺失项都能被清楚识别。
2. **Given** 多个工具共存于同一项目，**When** 用户刷新或重新初始化其中一个工具，**Then** 其他工具的配置和核心 `.specify` 内容不被破坏。
3. **Given** 官方支持工具清单发生变化，**When** 项目执行支持范围检查，**Then** 用户能发现哪些工具需要补齐、更新或保留现有配置。

---

### Edge Cases

- `.specify` 目录存在但核心文件不完整时，流程应只补齐缺失的核心内容，并清楚告知哪些文件被创建或仍需用户确认。
- 新增工具所需的工具专属资产已存在且被用户修改时，流程应优先保留用户版本，并提示可选择刷新或人工合并。
- 一个项目连续追加多个工具时，后续追加不得移除或降级先前工具的入口、说明和配置。
- 工具支持清单中存在已弃用或未安装工具时，用户应能区分“项目已配置”和“本机可运行”两类状态。
- 核心文件与模板存在差异时，差异应被视为用户维护内容，而不是待覆盖的旧模板内容。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide complete initialization support for every officially supported AI tool, not only the default or historically primary tool.
- **FR-002**: System MUST ensure each officially supported AI tool receives the user-facing assets needed to discover and run the core Spec Kit workflow.
- **FR-003**: System MUST allow multiple officially supported AI tools to coexist in the same project without requiring separate `.specify` roots.
- **FR-004**: System MUST detect when `.specify` core files already exist and have been initialized, then reuse those files instead of replacing them with template defaults.
- **FR-005**: System MUST preserve user-modified core `.specify` content when adding or refreshing support for another AI tool.
- **FR-006**: System MUST create only missing required core files when an existing `.specify` directory is incomplete, while clearly communicating what was added.
- **FR-007**: System MUST keep tool-specific files separate from canonical core files so that adding one tool does not overwrite another tool’s configuration.
- **FR-008**: System MUST provide a clear user-visible summary after initialization or refresh showing which AI tools are configured, which assets were created, reused, skipped, or require attention.
- **FR-009**: System MUST treat the official AI tool support list as the source for determining which tools require initialization coverage and consistency checks.
- **FR-010**: System MUST identify and report gaps when any officially supported AI tool lacks the expected workflow coverage or coexistence behavior.
- **FR-011**: System MUST support repeated initialization or refresh runs without duplicating core content, degrading existing tool support, or changing user-maintained files unexpectedly.
- **FR-012**: System MUST document the intended behavior for new-project initialization, existing-project tool addition, multi-tool coexistence, and core-file reuse in user-facing guidance.

### Key Entities

- **AI Tool Support Profile**: A supported AI tool’s expected project-facing assets, workflow coverage, display name, status, and coexistence rules.
- **Core Spec Kit Workspace**: The canonical `.specify` content shared by all tools in a project, including instructions, memory, templates, scripts, skills, and other workflow assets.
- **Tool-Specific Asset Set**: Files or guidance dedicated to one AI tool that reference the core workspace without becoming a separate source of truth.
- **Initialization Result Summary**: The user-visible record of created, reused, skipped, preserved, or attention-required items after an initialization or refresh run.

## Assumptions

- “所有的 AI 工具”指项目官方声明支持的 AI 工具集合，而不是任意第三方工具自动适配。
- `.specify` 中已经初始化且被修改的核心文件应被视为用户维护内容，默认不得用模板覆盖。
- 新增工具可以创建或更新该工具专属资产，但不得把工具专属资产变成核心工作流的新事实来源。
- 多工具共存的目标是共享同一套 Spec Kit 核心工作流，而不是为每个工具维护彼此分叉的流程定义。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of officially supported AI tools can initialize a new project with complete core workflow coverage in one user action.
- **SC-002**: In an existing project with user-modified `.specify` core files, adding another supported AI tool preserves 100% of those core file contents unless the user explicitly chooses otherwise.
- **SC-003**: A project can configure at least three officially supported AI tools concurrently, and users can identify each tool’s configured status and workflow coverage from the initialization summary.
- **SC-004**: Re-running initialization or refresh for any supported tool produces no duplicate core content and no unintended changes to other configured tools in 100% of tested coexistence scenarios.
- **SC-005**: At least 90% of first-time users in validation can correctly identify whether initialization created, reused, skipped, or preserved core files after reading the result summary.
- **SC-006**: Support requests or issue reports about non-default AI tools missing initialization scaffolding decrease by at least 50% after release compared with the previous comparable period.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Initialization acceptance checks across the official tool support list, recorded once per release candidate.
- **SC-002 Source**: Existing-project preservation checks using representative modified core files, recorded for every release candidate and regression run.
- **SC-003 Source**: Multi-tool coexistence validation reports showing configured tool count, coverage status, and any missing assets.
- **SC-004 Source**: Repeat-run regression checks comparing before-and-after project content and configured tool states.
- **SC-005 Source**: User validation survey or moderated onboarding test asking participants to interpret the result summary.
- **SC-006 Source**: Public issue tracker, support channel, or maintainer triage labels comparing reports before and after release.

## Clarifications

### Session 2026-05-18

- Q: 该规格应绑定到哪个长期 Feature？ → A: 022 / AI Tools Support
