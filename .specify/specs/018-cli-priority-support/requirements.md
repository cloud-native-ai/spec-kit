# Requirements Specification: CLI Priority AI Tool Support

**Requirement Branch**: `018-cli-priority-support`  
**Created**: 2026-06-21  
**Status**: Draft  
**Input**: User description: "需要将claude code, codex cli 和 Qoder cli这三款cli 工具作为第一优先级支持的ai 工具, 通过本框架speckit能发挥这几个工具的最大能力."

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: 022  
**Feature Name**: AI Tools Support

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

### User Story 1 - Codex CLI 首次正式纳入支持 (Priority: P1)

作为 Spec Kit 用户，我希望 Codex CLI 被正式纳入官方支持的 AI 工具列表，使其在初始化、配置、命令发现和文档层面与 Claude Code、Qoder CLI 等享有同等待遇，以便我能直接使用 Codex CLI 运行 Spec Kit 的完整 spec → plan → tasks → implement 工作流。

**Why this priority**: 目前 Codex CLI 虽在 `update-agent-context.sh` 脚本中有部分适配逻辑，但未被纳入 `AGENT_CONFIG`、`_OFFICIAL_ASSISTANT_KEYS`、宪法官方支持列表以及初始化流程。用户选择 Codex CLI 时无法获得完整的 Spec Kit 工作流覆盖。这是本需求的 MVP 核心——如果 Codex CLI 没有被正式纳入，则"三款 CLI 工具第一优先级"的目标就无法达成。

**Independent Test**: 可以在一个空项目中执行 `specify init --ai codex`，验证 `.codex/` 目录被创建、Codex CLI 命令模板被生成、用户可直接运行 Speckit 工作流命令。

**Acceptance Scenarios**:

1. **Given** 一个没有 Spec Kit 配置的新项目，**When** 用户执行初始化并选择 Codex CLI，**Then** 项目中包含 `.codex/` 目录及其下完整的 Speckit 命令模板、说明文件和配置资产。
2. **Given** Codex CLI 被正式纳入支持列表，**When** 用户查看 `specify init` 的 AI 工具选择菜单，**Then** Codex CLI 出现在可选列表中并标注为官方支持。
3. **Given** 项目已使用 Codex CLI 初始化，**When** 用户运行 `/speckit.*` 系列命令，**Then** 命令模板能被 Codex CLI 正确发现和执行，不出现路径或格式错误。
4. **Given** 已有 `.specify` 目录且核心文件已初始化，**When** 用户追加 Codex CLI 支持，**Then** 核心文件被复用而非覆盖，仅创建 Codex 专属资产。

---

### User Story 2 - CLI 工具成为第一优先级支持 (Priority: P2)

作为项目维护者，我希望 Claude Code、Codex CLI、Qoder CLI、GitHub Copilot 和 opencode 这五款 CLI 工具被标记为第一优先级（Tier 1）支持，Qwen Code 标记为 Tier 2（标准支持），在文档、初始化推荐顺序、能力矩阵和一致性审计中优先于其他支持工具，以便用户在选择 AI 工具时获得明确引导，并能在此五款工具上获得最深度的 Spec Kit 集成体验。

**Why this priority**: 在 Codex CLI 正式纳入支持后，需要建立分层支持体系。当前所有 AI 工具被视为同一优先级，但 Claude Code、Codex CLI、Qoder CLI、GitHub Copilot 和 opencode 作为功能更完整的 CLI 工具应获得更深度的适配（例如更丰富的命令模板内容、原生 CLI 安装验证、环境变量引导等），在文档和用户引导中被推荐为首选。Qwen Code 作为 Tier 2 工具仍保持基础命令覆盖，但不强制要求通过能力矩阵全部审计维度。

**Independent Test**: 可以在文档和 CLI `--help` 输出中验证五款 Tier 1 工具被优先推荐，并通过能力矩阵检查它们拥有最深度的 Spec Kit 集成覆盖。

**Acceptance Scenarios**:

1. **Given** 项目文档和 README 中列出支持的 AI 工具，**When** 用户查看工具列表，**Then** Claude Code、Codex CLI、Qoder CLI、GitHub Copilot 和 opencode 被标注为 Tier 1 优先级，Qwen Code 标注为 Tier 2，排在 Tier 1 之后。
2. **Given** 用户执行 `specify init` 且未指定 `--ai` 参数，**When** 交互式选择菜单展示可用工具，**Then** 五款 Tier 1 CLI 工具被排在推荐位置，Qwen Code 排列在后。
3. **Given** Tier 1 工具具备完整的能力矩阵覆盖，**When** 系统执行一致性审计，**Then** 五款 Tier 1 工具通过全部审计项（命令模板、说明文件、忽略配置、skills 链接、刷新行为保护），任何缺失项被明确报告。
4. **Given** 一款 Tier 1 工具被刷新或重新初始化，**When** 刷新行为执行，**Then** `.specify` 核心内容和其他工具配置不被影响。

---

### User Story 3 - 深度能力适配以发挥 CLI 工具最大能力 (Priority: P3)

作为使用 CLI 工具进行开发的工程师，我希望 Spec Kit 为 Claude Code、Codex CLI、Qoder CLI、GitHub Copilot 和 opencode 提供深度能力适配——包括工具特定的命令模板变体、CLI 安装与环境验证、`.specify` 工作流脚本路径优化、skills 发现机制适配等，以便这五款 Tier 1 CLI 工具能在 Spec Kit 框架内发挥最大能力，而非仅获得基础命令覆盖。

**Why this priority**: 在基础支持和分级完成后，深度适配是实现"发挥最大能力"目标的关键。不同 CLI 工具在命令格式、参数传递、目录约定、配置发现机制上存在差异，需要针对性优化才能让用户体验到最优的工作流集成。五款 Tier 1 工具均需获得此深度适配。

**Independent Test**: 可以分别在五款 Tier 1 工具中运行完整的 Spec Kit 工作流（requirements → plan → tasks → implement），验证每个环节的命令模板、参数格式、路径解析和结果输出都能正确工作。

**Acceptance Scenarios**:

1. **Given** 五款 Tier 1 CLI 工具各自有不同的命令文件格式和参数约定，**When** 初始化生成命令模板，**Then** 每款工具的命令模板使用该工具原生的参数格式（如 Claude Code 用 `$ARGUMENTS`、Codex CLI 按其命令格式约定、Qoder CLI 按其约定、GitHub Copilot 按其约定、opencode 按其约定），且命令内容保持工作流语义一致。
2. **Given** CLI 工具可能依赖环境变量或特定安装路径，**When** 用户完成初始化，**Then** 初始化结果摘要包含 CLI 安装验证状态和所需的环境变量设置指引（如 Codex CLI 的 `CODEX_HOME`）。
3. **Given** Spec Kit 的 skills 系统需要在 CLI 工具中被发现，**When** Tier 1 工具初始化完成，**Then** skills 目录的符号链接或发现配置正确指向 `.specify/skills/`。
4. **Given** 用户在 Tier 1 CLI 工具中运行 `/speckit.instructions`，**When** 指令文件被刷新，**Then** 该工具的兼容性文件（如 `CLAUDE.md`、`.codex/` 配置、`QODER.md`）被同步更新且基于 `.specify/instructions.md` 作为单一事实来源。

---

### Edge Cases

- 用户同时安装多款 Tier 1 CLI 工具，希望在同一项目中全部初始化——流程应确保各工具配置不互相覆盖，核心 `.specify` 内容共享。
- Codex CLI 尚未正式安装但用户选择了该工具——初始化应完成项目资产创建，但在结果摘要中标注 "CLI 未检测到" 以提醒用户安装。
- 一款 Tier 1 工具的命令模板格式与现有模板引擎不兼容——需要为该工具提供独立的命令模板变体，而非强制使用统一格式。
- 用户从 Tier 2 工具（Qwen Code）迁移到 Tier 1 工具——流程应保留已有核心内容，追加 Tier 1 工具配置，不删除原有工具配置。
- Codex CLI 版本更新导致目录结构变化——Spec Kit 初始化应记录工具适配版本，便于后续升级时平稳迁移。
- 宪法中官方支持列表当前不包含 Codex CLI——需要同步更新宪法条款以纳入正式支持。

## Requirements *(mandatory)*

<!--
  ACTION REQUIRED: The content in this section represents placeholders.
  Fill them out with the right functional requirements.
-->

### Functional Requirements

#### Codex CLI 正式纳入支持

- **FR-001**: System MUST 将 Codex CLI 纳入官方支持的 AI 工具列表，使其在助手配置矩阵（`AGENT_CONFIG`）、官方助手标识集合（`_OFFICIAL_ASSISTANT_KEYS`）、宪法支持条款和初始化流程中与 Claude Code、Qoder CLI 享有同等待遇。
- **FR-002**: System MUST 在执行 `specify init` 时提供 Codex CLI 作为可选 AI 工具，且用户选择 Codex CLI 后生成 `.codex/` 目录及其中完整的 Speckit 命令模板、说明文件和配置资产。
- **FR-003**: System MUST 为 Codex CLI 生成符合其原生命令格式约定的命令模板变体，使 `/speckit.*` 系列命令能被 Codex CLI 正确发现和执行，不出现路径或格式错误。
- **FR-004**: System MUST 在初始化结果摘要中报告 Codex CLI 专属资产的创建状态，并在检测到 Codex CLI 未安装时标注提醒信息。
- **FR-005**: System MUST 在已有 `.specify` 核心 content 的项目中追加 Codex CLI 支持时复用而非覆盖核心文件，仅创建 Codex 专属资产。

#### 分层支持体系（Tier 1 优先级）

- **FR-006**: System MUST 建立分层支持体系，将 Claude Code、Codex CLI、Qoder CLI、GitHub Copilot 和 opencode 标记为 Tier 1（第一优先级），Qwen Code 标记为 Tier 2（标准支持）。
- **FR-007**: System MUST 在 README、安装文档、快速入门和用法指南中优先推荐五款 Tier 1 CLI 工具，Qwen Code 排列在后。
- **FR-008**: System MUST 在 `specify init` 交互式选择菜单中将五款 Tier 1 CLI 工具排列在推荐位置，Qwen Code 排列在后。
- **FR-009**: System MUST 维护一份能力矩阵，记录每款支持工具在各支持维度（初始化、命令模板、说明文件、忽略配置、skills 链接、刷新行为保护）上的覆盖状态，Tier 1 工具须通过全部审计项。
- **FR-010**: System MUST 在执行一致性审计时对 Tier 1 工具执行全量审计项检查，任何缺失项被明确报告。

#### 深度能力适配

- **FR-011**: System MUST 为五款 Tier 1 CLI 工具分别生成工具特定的命令模板变体，使用各工具原生的参数格式（如 Claude Code 用 `$ARGUMENTS`、Codex CLI 按其命令格式约定、Qoder CLI 按其约定、GitHub Copilot 按其约定、opencode 按其约定），且命令内容保持 Spec Kit 工作流语义一致。
- **FR-012**: System MUST 在初始化结果摘要中包含 Tier 1 CLI 工具的安装验证状态和所需环境变量设置指引（如 Codex CLI 的 `CODEX_HOME`）。
- **FR-013**: System MUST 确保 Tier 1 工具初始化完成后 skills 目录的符号链接或发现配置正确指向 `.specify/skills/`。
- **FR-014**: System MUST 在 Tier 1 CLI 工具中运行 `/speckit.instructions` 时，基于 `.specify/instructions.md` 作为单一事实来源同步更新该工具的兼容性文件（如 `CLAUDE.md`、`.codex/` 配置、`QODER.md`）。
- **FR-015**: System MUST 确保多款 Tier 1 CLI 工具在同一项目中共存时配置不互相覆盖，核心 `.specify` 内容共享。

#### 宪法与治理同步

- **FR-016**: System MUST 同步更新宪法 Principle V，将 Codex CLI 新增至官方支持 AI 代理列表，并在 Principle V 主体中增加分层支持说明（Tier 1：Claude Code、Codex CLI、Qoder CLI、GitHub Copilot、opencode；Tier 2：Qwen Code；及划分原则），使宪法与规格中的分层体系保持一致。
- **FR-017**: System MUST 在刷新或重新初始化 Tier 1 工具时保护 `.specify` 核心 content 和其他工具配置不受影响。

### Key Entities

- **Support Tier**: 分层支持等级（Tier 1 / Tier 2），标识 AI 工具在 Spec Kit 中的集成深度和优先级。Tier 1 包含 5 款工具（Claude Code、Codex CLI、Qoder CLI、GitHub Copilot、opencode），享有最深度的适配覆盖；Tier 2 包含 Qwen Code，保持基础命令覆盖。
- **Assistant Profile**: 每款 AI 工具的初始化配置档案，包含工具标识、目录约定、命令模板格式、兼容性文件路径、环境变量要求等属性。
- **Capability Matrix**: 工具能力覆盖矩阵，以工具 × 支持维度（初始化、命令模板、说明文件、忽略配置、skills 链接、刷新行为保护）的形式记录每款工具的覆盖状态。
- **Command Template Variant**: 针对特定 CLI 工具的命令模板变体，使用该工具原生的参数格式和目录约定，同时保持 Spec Kit 工作流语义一致。

## Success Criteria *(mandatory)*

<!--
  ACTION REQUIRED: Define measurable success criteria.
  These must be technology-agnostic and measurable.
-->

### Measurable Outcomes

- **SC-001**: 用户在选择 Codex CLI 初始化后，可在 5 分钟内完成全部 Spec Kit 环境搭建并运行第一条 `/speckit.*` 命令。
- **SC-002**: 五款 Tier 1 CLI 工具在能力矩阵的全部 6 个支持维度上均达到 100% 覆盖率，通过一致性审计无缺失项。
- **SC-003**: 90% 的首次使用用户能在不查阅外部文档的情况下，仅凭 `specify init` 交互引导和结果摘要完成 Tier 1 工具的初始化配置。
- **SC-004**: 在同一项目中同时初始化 2 款以上 Tier 1 CLI 工具时，核心 `.specify` 内容和各工具专属配置之间零冲突、零覆盖。
- **SC-005**: `specify init` 交互菜单和项目文档中，Tier 1 工具排在推荐位置的可验证比例达 100%。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 在空项目中执行 `specify init --ai codex` 计时，并验证 `.codex/` 目录和命令模板已生成。手动执行一条 `/speckit.requirements` 命令确认工作流可用。在集成测试中自动化覆盖。
- **SC-002 Source**: 运行支持面审计脚本（`support-surface audit`），对五款 Tier 1 工具逐一检查 6 个维度的覆盖状态，输出通过/缺失报告。在合约测试中固化断言。
- **SC-003 Source**: 通过用户测试或可用性调研收集首次使用完成率数据，以无外部文档依赖为标准。初期通过集成测试验证交互引导和结果摘要的完整性作为代理指标。
- **SC-004 Source**: 在测试环境中对同一项目依次初始化 Claude Code + Codex CLI + Qoder CLI，运行核心资产完整性校验和工具间隔离校验，验证零冲突。在集成测试中自动化覆盖。
- **SC-005 Source**: 对 README、安装文档、快速入门和 `specify init --help` 输出进行静态检查，验证 Tier 1 工具排列顺序。在合约测试中固化断言。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

<!--
  ACTION REQUIRED:
  Use this section as the SINGLE SOURCE OF TRUTH for string literals that must match
  exactly across multiple artefacts (FRs, contracts, snippet bodies, test assertions,
  task descriptions). Downstream artefacts MUST cite by `<string-id>` rather than
  re-typing the text, so a rotation only edits this section.

  Examples of strings that belong here:
    - Error messages asserted by tests
    - Sentinel substrings in stderr / logs
    - Env var names, exit codes treated as contract
    - URL paths or filenames that contracts pin to a specific string

  Omit this section entirely if no such cross-artefact strings exist.
-->

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-TIER1` | `"tier1"` | FR-006, FR-007, FR-008, FR-009, FR-010, contracts, tasks |
| `STR-TIER2` | `"tier2"` | FR-006, contracts, tasks |
| `STR-CODEX_KEY` | `"codex"` | FR-001, FR-002, AGENT_CONFIG, contracts |
| `STR-CLAUDE_KEY` | `"claude"` | FR-006, FR-011, AGENT_CONFIG, contracts |
| `STR-QODER_KEY` | `"qoder"` | FR-006, FR-011, AGENT_CONFIG, contracts |
| `STR-COPILOT_KEY` | `"copilot"` | FR-006, FR-011, AGENT_CONFIG, contracts |
| `STR-OPENCODE_KEY` | `"opencode"` | FR-006, FR-011, AGENT_CONFIG, contracts |
| `STR-QWEN_KEY` | `"qwen"` | FR-006, contracts |
| `STR-CODEX_HOME` | `"CODEX_HOME"` | FR-012, init summary, contracts |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-06-21

- Q: 这个需求规格（`018-cli-priority-support`）是否应绑定到 Feature 025 "Tiered AI Tool Support"？ → A: 绑定到 Feature 022 — AI Tools Support。用户选择将本需求作为现有 Feature 022 的延伸，而非新建 Feature 025。Feature 022 的范围（确保所有官方支持工具获得完整初始化覆盖并能共存）可涵盖分层支持和 Codex CLI 纳入的演进。
- Q: Codex CLI 的项目级配置目录和命令模板路径应采用哪种约定？ → A: `.codex/` + `.codex/commands/`，与 Claude Code (`.claude/commands/`) 和 Qoder (`.qoder/commands/`) 的模式一致。
- Q: 是否应在宪法 Principle V 的官方支持列表中新增 Codex CLI，并同时引入 Tier 1 / Tier 2 分层概念的描述？ → A: 是。在宪法 Principle V 主体中同时新增 Codex CLI 到官方支持列表，并增加分层支持说明（Tier 1 / Tier 2 定义和划分原则），使宪法与规格中的分层体系保持一致。
- Q: 将工具标记为 Tier 2 的影响范围应如何界定？ → A: 用户调整了分层划分：将 Copilot 和 opencode 升级为 Tier 1，Qwen Code 作为唯一的 Tier 2 工具。Tier 1 扩展为 5 款工具（Claude Code、Codex CLI、Qoder CLI、GitHub Copilot、opencode）。分层影响范围为描述性引导（文档排序和菜单推荐位置），不限制任何现有功能可用性。深度适配（FR-011~FR-015）扩展覆盖全部 5 款 Tier 1 工具。

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

## Assumptions

- **Codex CLI 目录约定**: Codex CLI 使用 `.codex/` 作为项目级配置目录，命令模板存放在 `.codex/commands/` 下，与 Claude Code (`.claude/commands/`) 和 Qoder (`.qoder/commands/`) 的模式一致。（已通过 `/speckit.clarify` 确认）
- **Codex CLI 命令格式**: 假设 Codex CLI 接受 Markdown 格式的命令提示文件，参数传递方式与其原生约定一致。Spec Kit 将基于现有 `update-agent-context.sh` 中的 Codex 适配逻辑进行扩展。
- **Tier 1 / Tier 2 划分依据**: Tier 1 = 完整 CLI 工具能力（支持终端原生运行、命令模板发现、独立安装验证）；Tier 2 = 功能覆盖有限的工具。Tier 1 包含 5 款工具（Claude Code、Codex CLI、Qoder CLI、GitHub Copilot、opencode），Tier 2 包含 Qwen Code。此划分基于当前已知工具能力评估。（已通过 `/speckit.clarify` 确认）
- **能力矩阵 6 维度**: 初始化、命令模板、说明文件、忽略配置、skills 链接、刷新行为保护。如需增加维度（如 "环境变量引导" 或 "工具版本检测"），在 `/speckit.clarify` 或 `/speckit.plan` 阶段扩展。
- **非破坏性升级**: 现有已初始化的项目在升级到包含本特性的版本后，通过 `specify init` 的幂等行为自动补全缺失的 Codex CLI 资产，不影响已有配置。
- **opencode 纳入 Tier 1**: opencode 作为 CLI 工具且已具备 Spec Kit 集成基础，升级为 Tier 1，享有深度适配覆盖。（已通过 `/speckit.clarify` 确认）
