# Requirements Specification: Add Qoder Support

**Requirement Branch**: `006-add-qoder-support`  
**Created**: 2026-03-29  
**Status**: Draft  
**Input**: User description: "在spec-kit项目中添加对qoder的支持，可以使用./tmp目录中来自上游的patch作为核心实现。"

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

### User Story 1 - 在初始化时选择 Qoder (Priority: P1)

作为准备使用 Spec Kit 的开发者，我希望在初始化新项目或现有项目时可以直接选择 Qoder 作为 AI 助手，这样我无需手工补齐命令文件、说明文档或额外配置，就能马上开始使用 Qoder 工作流。

**Why this priority**: 这是用户感知最直接的主流程。如果初始化阶段不能正确支持 Qoder，后续文档、校验和发布能力都无法形成完整价值闭环。

**Independent Test**: 通过一次选择 Qoder 的项目初始化流程即可独立验证；若生成结果中已包含完整的 Qoder 使用资产与说明，并且用户无需手工复制文件，则该故事成立。

**Acceptance Scenarios**:

1. **Given** 用户准备初始化一个新的 Spec Kit 项目，**When** 用户选择 Qoder 作为目标 AI 助手，**Then** 系统应在生成结果中包含 Qoder 所需的项目内命令资产与使用说明。
2. **Given** 用户在现有目录中初始化项目并选择 Qoder，**When** 初始化完成，**Then** 系统应保留原有项目内容并补齐 Qoder 所需资产，而不要求用户额外手工创建这些内容。

---

### User Story 2 - 校验与更新现有 Qoder 项目 (Priority: P2)

作为已经在使用或维护 Spec Kit 项目的开发者，我希望系统能够识别、校验并刷新与 Qoder 相关的项目资产，这样我可以在升级模板或补齐缺失内容时保持项目一致性，而不影响其他 AI 助手的配置。

**Why this priority**: 初始化之后，真实项目更常见的需求是升级、刷新和校验。如果 Qoder 只能“首次创建”，却不能“持续维护”，支持就不完整。

**Independent Test**: 在一个已包含或部分包含 Qoder 资产的项目中执行一次校验或刷新流程，验证系统是否能识别缺失、给出指引并更新 Qoder 相关内容且不改坏其他助手资产。

**Acceptance Scenarios**:

1. **Given** 一个项目已经包含 Qoder 相关资产，**When** 维护者执行刷新或更新流程，**Then** 系统应更新 Qoder 相关内容并保持其他助手资产不变。
2. **Given** 用户选择 Qoder 且启用了助手工具校验，**When** 本地缺少对应 CLI，**Then** 系统应明确指出缺失依赖并给出下一步操作指引。

---

### User Story 3 - 文档与发布产物保持一致 (Priority: P3)

作为项目维护者，我希望面向用户的文档、帮助信息和分发产物都一致地展示 Qoder 支持状态，这样用户看到的能力说明、下载到的模板内容和实际行为不会相互矛盾。

**Why this priority**: 一致的说明和分发结果可以减少误导与支持成本。即使核心流程已可用，如果文档、校验和分发产物不一致，用户仍会遭遇失败或困惑。

**Independent Test**: 对一次候选发布执行文档与分发检查，验证帮助输出、能力列表和模板分发结果是否都包含一致的 Qoder 支持信息。

**Acceptance Scenarios**:

1. **Given** 用户查看支持的 AI 助手列表，**When** 用户查阅项目文档或命令帮助，**Then** 其看到的 Qoder 名称、可用性和获取指引应保持一致。
2. **Given** 维护者生成面向用户的模板分发产物，**When** 用户下载对应产物，**Then** 该产物应包含与 Qoder 支持声明一致的内容。

---

### Edge Cases

- 当用户选择 Qoder，但当前流程缺少必要的 Qoder 资产时，系统应在同一次操作中明确失败原因，而不是生成一个看似成功但实际不可用的项目。
- 当用户启用助手工具校验且本地未安装 Qoder CLI 时，系统应给出清晰的安装或绕过校验指引。
- 当项目同时包含多个 AI 助手资产时，刷新 Qoder 相关内容不应覆盖或破坏其他助手的已有文件。
- 当文档、帮助输出和分发产物中存在命名或链接不一致时，系统应将其视为发布前必须解决的一致性问题。
- 当用户在现有目录初始化并已存在部分 Qoder 文件时，系统应更新缺失或过期内容，而不是要求用户先手工清理目录。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to select Qoder wherever Spec Kit asks the user to choose a supported AI assistant during project initialization.
- **FR-002**: System MUST generate the complete set of Qoder-specific project assets required for a user to start the Qoder workflow immediately after initialization.
- **FR-003**: System MUST include Qoder in user-facing supported-assistant listings, option descriptions, and setup guidance wherever those lists are presented.
- **FR-004**: System MUST validate the availability of the Qoder CLI in workflows where assistant tool checks are enabled, and MUST provide actionable guidance when the dependency is missing.
- **FR-005**: System MUST allow users to skip Qoder tool validation through the same ignore-check behavior already available for other CLI-based assistants.
- **FR-006**: System MUST support refreshing or regenerating Qoder-related assets in existing projects without overwriting unrelated assistant assets.
- **FR-007**: System MUST include Qoder in all distributable template and release outputs that are expected to contain supported CLI-based assistants.
- **FR-008**: System MUST keep Qoder naming, availability messaging, and acquisition guidance consistent across initialization flows, maintenance flows, help text, and user documentation.
- **FR-009**: System MUST preserve existing behavior for already supported assistants when Qoder support is added.
- **FR-010**: System MUST surface a clear failure message when a user selects Qoder in a workflow that cannot provide the necessary Qoder-specific assets.
- **FR-011**: System MUST support both standard new-project initialization and existing-directory initialization when Qoder is selected.
- **FR-012**: System MUST treat inconsistent Qoder support across product surfaces as a release-blocking defect for this feature.
- **FR-013**: System MUST update the project's official supported-assistant governance records so Qoder is recognized as an approved assistant before this feature is considered complete.

### Key Entities *(include if requirement involves data)*

- **Supported AI Assistant**: A user-selectable assistant option that includes a name, setup guidance, validation expectations, and associated project assets.
- **Qoder Asset Set**: The collection of user-visible project artifacts that make the Qoder workflow usable immediately after initialization or refresh.
- **Assistant Validation Result**: The outcome shown to a user when Spec Kit checks whether the chosen assistant is available and ready to use.
- **Distribution Variant**: A releasable template package that should reflect the same assistant support claims as the product documentation and help output.

### Assumptions

- Qoder is intended to be supported as a first-class CLI-based assistant in the same user journeys where other CLI-based assistants are available.
- This requirement focuses on user-visible support across initialization, validation, maintenance, documentation, distribution, and governance alignment; it does not require redefining the behavior of unrelated features.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of initialization runs that select Qoder produce a workspace containing the full Qoder asset set without requiring manual file copying.
- **SC-002**: 100% of Qoder dependency check failures identify Qoder as the missing prerequisite and provide a next-step instruction in the same interaction.
- **SC-003**: 100% of maintained user-facing supported-assistant lists and help surfaces present the same Qoder name and support status within a release candidate.
- **SC-004**: Maintainers can generate release-ready template outputs that include Qoder support for every supported script variant in one standard packaging run without manual post-processing.
- **SC-005**: In validation samples of existing projects that already contain Qoder assets, at least 95% of refresh operations update Qoder-specific content without modifying unrelated assistant assets.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Release-candidate smoke tests over new-project and existing-directory initialization samples; collected from generated workspace audits on each candidate build.
- **SC-002 Source**: Negative-path validation tests with Qoder intentionally unavailable; collected from automated test logs on each change set touching assistant validation.
- **SC-003 Source**: Pre-release content audit comparing help output, README-style capability tables, and generated template metadata; collected once per release candidate.
- **SC-004 Source**: Packaging verification results over all supported script variants; collected from standard release preparation runs and archive manifest review.
- **SC-005 Source**: Regression suite on sample repositories containing mixed assistant assets; collected on each change that affects refresh or update behavior.

## Clarifications

### Session 2026-03-29

- Q: 本次 Qoder 支持是否应当同时把项目治理/批准助手范围更新为包含 Qoder？ → A: 是，本次需求包含治理对齐；Qoder 作为正式批准的受支持助手交付。

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
