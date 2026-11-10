# Requirements Specification: Skill Install Layout

**Requirement Branch**: `007-skill-install-layout`  
**Created**: 2026-04-21  
**Status**: Draft  
**Input**: User description: "重构skills的安装逻辑，当前会把skills中的skill安装到目标项目的.github/skills目录，这个是对.github定制的路径，需要将skills目录安装到.specify/skills这个通用目录，然后根据情况创建软链接到.github/skills和其他支持的工具。"

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: 013  
**Feature Name**: Skills Command

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

### User Story 1 - 统一项目级技能主目录 (Priority: P1)

作为维护目标项目的用户，我希望所有项目级 skills 都先安装到 `.specify/skills/` 这个通用目录，以便同一套技能资产不再绑定某个特定 AI 工具目录，后续也更容易迁移、管理和复用。

**Why this priority**: 这是本次需求的核心价值。只有先把技能主副本放到通用目录，后续给不同工具提供兼容入口才不会导致重复安装和路径绑定。

**Independent Test**: 在一个全新的目标项目中安装任意一个 skill，验证 skill 主目录被创建在 `.specify/skills/<skill-name>/`，且用户无需手工移动文件即可开始后续配置。

**Acceptance Scenarios**:

1. **Given** 目标项目尚未安装任何 project-level skill，**When** 用户执行一次 skill 安装流程，**Then** 系统在 `.specify/skills/` 下创建该 skill 的主目录并将完整内容安装到该位置。
2. **Given** 目标项目已经存在支持工具但尚未创建工具专属技能目录，**When** skill 安装完成，**Then** 系统仍以 `.specify/skills/` 作为唯一主副本，而不是直接把主内容写入工具专属目录。

---

### User Story 2 - 为已支持工具暴露兼容入口 (Priority: P2)

作为在不同 AI 工具之间切换的用户，我希望系统在需要时自动为技能创建兼容入口，例如链接到 `.github/skills/` 或其他已支持工具的技能目录，这样现有工具仍能发现技能，而技能本体只维护一份。

**Why this priority**: 统一主目录之后，兼容入口决定现有工具能否无缝继续工作，是避免破坏已有使用方式的关键。

**Independent Test**: 在包含 GitHub 工具目录或其他受支持工具目录的目标项目中安装 skill，验证每个应暴露的入口都指向 `.specify/skills/` 下的同一技能主副本。

**Acceptance Scenarios**:

1. **Given** 目标项目启用了 GitHub 风格的 skills 入口，**When** 用户安装一个 skill，**Then** 系统创建指向 `.specify/skills/<skill-name>/` 的 `.github/skills/<skill-name>` 兼容入口，而不是复制出第二份技能内容。
2. **Given** 目标项目还启用了其他已支持工具的 skill 入口，**When** 用户安装同一个 skill，**Then** 系统按该工具的支持规则创建对应兼容入口，并保证这些入口都映射到同一主副本。

---

### User Story 3 - 平滑迁移既有安装方式 (Priority: P3)

作为已经在旧布局下使用 skills 的用户，我希望系统在升级到新安装逻辑后仍能识别并迁移既有 skill，避免出现重复目录、失效引用或需要手工重装的情况。

**Why this priority**: 这是降低变更风险的重要保障。即使新布局更合理，如果现有项目迁移成本过高，用户也难以采纳。

**Independent Test**: 准备一个只在 `.github/skills/` 下存在旧 skill 的项目，执行新安装或刷新流程，验证系统能识别旧状态并将有效结果收敛到 `.specify/skills/` 主目录与兼容入口布局。

**Acceptance Scenarios**:

1. **Given** 目标项目已有旧版 `.github/skills/<skill-name>/` 目录，**When** 用户对同名 skill 执行安装或刷新，**Then** 系统将该 skill 收敛到 `.specify/skills/` 主目录，并保留可继续使用的兼容入口布局。
2. **Given** 目标项目中已存在与目标链接位置冲突的真实目录或文件，**When** 系统尝试创建兼容入口，**Then** 系统明确提示冲突原因，并避免静默覆盖已有内容。

---

### Edge Cases

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right edge cases.
-->

- 当 `.specify/skills/<skill-name>/` 已存在且内容与待安装 skill 不一致时，系统应阻止静默覆盖，并提示用户处理冲突。
- 当目标工具目录位置已经存在普通目录、普通文件或损坏链接时，系统应根据迁移策略执行处理；对于旧版 `.github/skills/<skill-name>` 的可迁移真实目录，应在迁移后删除该旧目录。
- 当当前环境不支持创建软链接，或用户没有足够权限创建链接时，系统应创建占位目录与指引文件，并明确标记该兼容入口处于需手工处理状态。
- 当目标项目只支持部分工具入口时，系统应仅创建适用入口，并对未启用或不受支持的工具保持跳过而非报错。
- 当用户重复安装同一个 skill 时，系统应保持幂等，避免生成多个彼此偏离的副本。
- 当迁移前自动备份失败时，系统应跳过旧目录删除，仅保留新主副本与旧目录并明确提示后续人工处理。

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

- **FR-001**: 系统 MUST 将项目级 skill 的主安装位置统一设为 `.specify/skills/<skill-name>/`。
- **FR-002**: 系统 MUST 将 `.specify/skills/` 视为 skill 内容的唯一主副本来源，而不是在多个工具目录中维护独立副本。
- **FR-003**: 系统 MUST 在目标项目启用了 GitHub 风格技能入口时，为每个已安装 skill 提供指向主副本的 `.github/skills/<skill-name>` 兼容入口。
- **FR-004**: 系统 MUST 在目标项目启用了其他受支持工具的技能入口时，按照各自入口约定为同一主副本创建对应兼容入口。
- **FR-005**: 系统 MUST 根据目标项目实际启用且属于 Spec Kit 当前正式支持范围的工具集合决定创建哪些兼容入口，而不是无差别创建所有可能目录。
- **FR-006**: 系统 MUST 在重复安装、刷新或升级同一 skill 时保持幂等，确保最终只存在一个可识别的主副本。
- **FR-007**: 系统 MUST 在发现旧版 `.github/skills/` 布局时支持迁移到 `.specify/skills/` 主目录，并将旧目录内容以“移动（mv）语义”收敛到主目录；在删除前置条件满足时删除旧版真实目录，否则按失败降级策略保留旧目录并提示人工处理。
- **FR-008**: 系统 MUST 在兼容入口位置已存在冲突目录、文件或无效链接时停止自动覆盖，并返回明确的冲突说明。
- **FR-009**: 系统 MUST 在无法创建兼容入口时保留已安装的主副本状态，并向用户说明哪些入口创建成功、哪些失败以及原因。
- **FR-010**: 系统 MUST 确保任何兼容入口都能追溯到 `.specify/skills/` 下的对应 skill 主副本，避免出现指向过期副本的分叉状态。
- **FR-011**: 系统 MUST 让后续的 skill 发现、刷新和引用流程优先基于 `.specify/skills/` 主目录进行判断。
- **FR-012**: 系统 MUST 在项目文档、模板和用户可见说明中将 `.specify/skills/` 描述为通用技能目录，并将 `.github/skills/` 等路径描述为兼容入口而非主安装位置。
- **FR-013**: 当兼容入口无法使用软链接创建时，系统 MUST 创建不复制 skill 内容的占位目录与指引文件，并在结果中明确提示该入口需要人工完成后续处理。
- **FR-014**: 本次需求 MUST 仅覆盖 Spec Kit 当前正式支持且具备明确技能目录约定的工具，不包含草稿、实验或未正式支持工具的自动入口创建。
- **FR-015**: 当迁移流程需要删除旧版真实目录时，系统 MUST 先执行一次自动备份，再执行删除动作，并在迁移结果中报告备份位置与删除结果。
- **FR-016**: 当自动备份失败时，系统 MUST 跳过旧目录删除，保留主副本与旧目录并将迁移标记为“需人工处理”，同时在输出中给出明确后续指引。

### Key Entities *(include if requirement involves data)*

- **Skill 主副本**: 安装在 `.specify/skills/<skill-name>/` 下的项目级 skill 正本，是所有兼容入口的唯一来源。
- **兼容入口**: 暴露给某个已支持工具使用的技能访问点，例如 `.github/skills/<skill-name>`；其职责是将工具访问路由到 skill 主副本。
- **工具支持画像**: 目标项目当前启用或支持的工具集合，用于决定需要创建哪些兼容入口。
- **迁移状态**: 记录某个 skill 是全新安装、从旧布局迁移，还是重复刷新，用于判断是否需要冲突处理或收敛旧目录。

### Assumptions

- 项目级 skill 仍然允许被多个 AI 工具共享，只是从工具专属目录改为以通用目录为主。
- 兼容入口以“链接到主副本”为首选行为，避免复制文件造成内容漂移。
- 本次需求聚焦项目级 skill 安装与迁移，不涉及个人级 skill 目录的重新设计。
- 若目标工具尚未被 Spec Kit 明确支持，则本次需求不要求为其自动创建新入口。

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 100% 新安装或刷新后的项目级 skills 都将主副本落在 `.specify/skills/` 下，而不是直接落在工具专属目录中。
- **SC-002**: 对于目标项目中已启用的每一种受支持工具入口，95% 以上的 skill 安装在一次执行后即可生成可用的兼容入口或明确的跳过结果。
- **SC-003**: 在旧版 `.github/skills/` 布局迁移场景中，90% 以上的验证样例无需手工复制 skill 内容即可完成收敛。
- **SC-004**: 对同一 skill 重复执行安装或刷新时，100% 的验证样例不会产生两个内容不一致的项目级副本。
- **SC-005**: 与变更前基线相比，用户因 skill 路径分叉或工具专属目录绑定导致的安装后修复步骤减少至少 80%。

### Measurement Sources & Collection Methods

<!--
  ACTION REQUIRED: For each measurable outcome above, specify:
  - Where the metric data will be collected from (logs, monitoring, user surveys, etc.)
  - How the data will be collected and aggregated
  - What the baseline measurement is (if applicable)
  - How often the metric will be measured
-->

- **SC-001 Source**: 通过项目级 skill 安装与刷新验证样例统计主副本所在目录，按每次需求验收与回归测试汇总。
- **SC-002 Source**: 通过受支持工具矩阵的安装验证结果统计兼容入口创建成功、跳过与失败原因，按每次发布前汇总。
- **SC-003 Source**: 通过旧布局迁移样例的验收记录统计是否需要人工复制内容，按每次回归测试汇总。
- **SC-004 Source**: 通过重复安装与刷新样例检查同名 skill 是否出现多个偏离副本，按每次回归测试汇总。
- **SC-005 Source**: 通过安装问题记录、验收备注或用户反馈对比变更前后的手工修复步骤数量，按迭代复盘汇总。

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-04-21

- Q: 当目标环境不支持创建软链接时，兼容入口应采用哪种策略？ → A: Option C（自动创建占位目录+指引文件，不复制内容）
- Q: 本次需求中“其他支持的工具”覆盖范围应如何界定？ → A: Option A（仅覆盖 Spec Kit 当前已正式支持且有明确技能目录约定的工具）
- Q: 检测到旧版 `.github/skills/<name>` 为“真实目录（非链接）”且内容可用时，迁移策略应是什么？ → A: Option A（将旧目录内容迁移到 `.specify/skills/<name>`，按 mv 语义覆盖同名项，再删除旧目录）
- Q: 执行“删除旧目录”前，是否要求系统自动生成一次迁移备份？ → A: Option B（备份一次后再执行迁移删除）
- Q: 如果“自动备份”本身失败，迁移流程应如何处理？ → A: Option C（跳过删除，仅保留主副本并提示存在旧目录）
