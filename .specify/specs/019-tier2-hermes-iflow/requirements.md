# Requirements Specification: Tier 2 Agent Support for Hermes-Agent and iFlow

**Requirement Branch**: `019-tier2-hermes-iflow`  
**Created**: 2026-06-22  
**Status**: Draft  
**Input**: User description: "在项目中再添加两个tier 2的Agent的支持 hermes-agent和iflow,"

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: 022  
**Feature Name**: AI Tools Support

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Hermes-Agent 纳入 Tier 2 支持 (Priority: P1)

作为 Spec Kit 用户，我希望 Hermes-Agent 被纳入官方支持的 AI 工具列表并标记为 Tier 2（标准支持），使其在初始化、命令模板生成和说明文件层面获得基础覆盖，以便我可以在 Hermes-Agent 环境中使用 Spec Kit 的 `/speckit.*` 工作流命令。

**Why this priority**: Hermes-Agent 是用户明确要求新增的两款工具之一。将其纳入 Tier 2 支持是本需求的核心交付目标。只要完成 Hermes-Agent 的 Tier 2 接入，用户就能获得该工具的基础 Spec Kit 工作流覆盖，这是 MVP 的一半。

**Independent Test**: 在一个空项目中执行 `specify init --ai hermes`，验证 Hermes-Agent 对应的配置目录被创建、基础命令模板被生成、初始化结果摘要正确显示 Hermes-Agent 为 Tier 2 工具。

**Acceptance Scenarios**:

1. **Given** 一个没有 Spec Kit 配置的新项目，**When** 用户执行初始化并选择 Hermes-Agent，**Then** 项目中创建 Hermes-Agent 对应的配置目录及基础 Speckit 命令模板和说明文件。
2. **Given** Hermes-Agent 已被纳入支持列表，**When** 用户查看 `specify init` 的 AI 工具选择菜单，**Then** Hermes-Agent 出现在可选列表中并标注为 Tier 2。
3. **Given** 项目已使用 Hermes-Agent 初始化，**When** 用户运行 `/speckit.*` 系列命令，**Then** 命令模板能被 Hermes-Agent 正确发现和执行。
4. **Given** 已有 `.specify` 目录且核心文件已初始化，**When** 用户追加 Hermes-Agent 支持，**Then** 核心文件被复用而非覆盖，仅创建 Hermes-Agent 专属资产。

---

### User Story 2 - iFlow 纳入 Tier 2 支持 (Priority: P1)

作为 Spec Kit 用户，我希望 iFlow 被纳入官方支持的 AI 工具列表并标记为 Tier 2（标准支持），使其在初始化、命令模板生成和说明文件层面获得基础覆盖，以便我可以在 iFlow 环境中使用 Spec Kit 的 `/speckit.*` 工作流命令。

**Why this priority**: iFlow 是用户明确要求新增的两款工具之一，与 Hermes-Agent 同等重要。两者共同构成本需求的完整交付目标。

**Independent Test**: 在一个空项目中执行 `specify init --ai iflow`，验证 iFlow 对应的配置目录被创建、基础命令模板被生成、初始化结果摘要正确显示 iFlow 为 Tier 2 工具。

**Acceptance Scenarios**:

1. **Given** 一个没有 Spec Kit 配置的新项目，**When** 用户执行初始化并选择 iFlow，**Then** 项目中创建 iFlow 对应的配置目录及基础 Speckit 命令模板和说明文件。
2. **Given** iFlow 已被纳入支持列表，**When** 用户查看 `specify init` 的 AI 工具选择菜单，**Then** iFlow 出现在可选列表中并标注为 Tier 2。
3. **Given** 项目已使用 iFlow 初始化，**When** 用户运行 `/speckit.*` 系列命令，**Then** 命令模板能被 iFlow 正确发现和执行。
4. **Given** 已有 `.specify` 目录且核心文件已初始化，**When** 用户追加 iFlow 支持，**Then** 核心文件被复用而非覆盖，仅创建 iFlow 专属资产。

---

### User Story 3 - 8 工具共存与一致性审计 (Priority: P2)

作为项目维护者，我希望在新增 Hermes-Agent 和 iFlow 后，全部 8 款已支持的 AI 工具（6 款现有 + 2 款新增）能够在同一项目中共存，并且能力矩阵审计和分层体系正确反映 Tier 2 工具的扩展。

**Why this priority**: 在两款新工具各自的基础接入完成后，需要确保多工具共存不出现冲突，且审计和文档系统正确反映 8 工具分层格局。

**Independent Test**: 在同一项目中同时初始化 Claude Code（Tier 1）+ Hermes-Agent（Tier 2）+ iFlow（Tier 2），运行能力矩阵审计，验证所有工具通过各自 Tier 对应的审计维度。

**Acceptance Scenarios**:

1. **Given** 项目中已初始化多款 Tier 1 工具，**When** 用户追加 Hermes-Agent 和 iFlow 的 Tier 2 支持，**Then** 现有工具配置和 `.specify` 核心内容不受影响。
2. **Given** 全部 8 款工具均已纳入支持列表，**When** 系统执行能力矩阵审计，**Then** Tier 1 工具通过全部 6 个审计维度，Tier 2 工具（Qwen Code、Hermes-Agent、iFlow）按 Tier 2 标准审计并报告覆盖状态。
3. **Given** 文档和 CLI 帮助信息列出支持的 AI 工具，**When** 用户查看工具列表，**Then** Tier 1 工具排在前列，3 款 Tier 2 工具（Qwen Code、Hermes-Agent、iFlow）排在 Tier 1 之后。

---

### Edge Cases

- 用户选择 Hermes-Agent 或 iFlow 初始化但本地未安装该 CLI 工具——初始化应完成项目资产创建，在结果摘要中标注 "CLI 未检测到" 提醒。
- 用户同时初始化所有 8 款工具——各工具配置目录应独立，核心 `.specify` 内容共享，不出现覆盖或冲突。
- Hermes-Agent 或 iFlow 的命令模板格式约定与现有工具不同——需按该工具原生约定生成命令模板变体。
- 用户从 Tier 2 工具（如 Hermes-Agent）升级到 Tier 1——当前需求不涉及升级路径，但追加 Tier 1 工具时不应影响已有 Tier 2 配置。
- 宪法 Principle V 当前列出 6 款支持工具——需要同步更新以纳入 Hermes-Agent 和 iFlow。

## Requirements *(mandatory)*

### Functional Requirements

#### Hermes-Agent Tier 2 接入

- **FR-001**: System MUST 将 Hermes-Agent 纳入官方支持的 AI 工具列表，添加至助手配置矩阵（`AGENT_CONFIG`）和官方助手标识集合（`_OFFICIAL_ASSISTANT_KEYS`），标记为 Tier 2。
- **FR-002**: System MUST 在执行 `specify init` 时提供 Hermes-Agent 作为可选 AI 工具，且用户选择后生成 Hermes-Agent 对应的配置目录及基础 Speckit 命令模板和说明文件。
- **FR-003**: System MUST 为 Hermes-Agent 生成符合其原生命令格式约定的命令模板变体，使 `/speckit.*` 系列命令能被 Hermes-Agent 正确发现和执行。
- **FR-004**: System MUST 在初始化结果摘要中报告 Hermes-Agent 资产的创建状态，并显示 Tier 2 标签。

#### iFlow Tier 2 接入

- **FR-005**: System MUST 将 iFlow 纳入官方支持的 AI 工具列表，添加至助手配置矩阵（`AGENT_CONFIG`）和官方助手标识集合（`_OFFICIAL_ASSISTANT_KEYS`），标记为 Tier 2。
- **FR-006**: System MUST 在执行 `specify init` 时提供 iFlow 作为可选 AI 工具，且用户选择后生成 iFlow 对应的配置目录及基础 Speckit 命令模板和说明文件。
- **FR-007**: System MUST 为 iFlow 生成符合其原生命令格式约定的命令模板变体，使 `/speckit.*` 系列命令能被 iFlow 正确发现和执行。
- **FR-008**: System MUST 在初始化结果摘要中报告 iFlow 资产的创建状态，并显示 Tier 2 标签。

#### 分层体系与审计更新

- **FR-009**: System MUST 将 Hermes-Agent 和 iFlow 加入分层支持体系中的 Tier 2 分类，与现有 Qwen Code 同级，使 Tier 2 工具总数从 1 款扩展为 3 款。
- **FR-010**: System MUST 在能力矩阵审计中覆盖 Hermes-Agent 和 iFlow，按 Tier 2 标准检查基础支持维度（初始化、命令模板、说明文件），不强制要求通过全部 6 个审计维度。
- **FR-011**: System MUST 在 `specify init` 交互式选择菜单中将 Hermes-Agent 和 iFlow 排列在 Tier 1 工具之后，与 Qwen Code 同区域展示。
- **FR-012**: System MUST 确保追加 Hermes-Agent 或 iFlow 支持时复用已有 `.specify` 核心文件，仅创建工具专属资产，不覆盖核心内容或其他工具配置。

#### 治理与文档同步

- **FR-013**: System MUST 同步更新宪法 Principle V，将 Hermes-Agent 和 iFlow 新增至官方支持 AI 代理列表中的 Tier 2 部分。
- **FR-014**: System MUST 更新 README、安装文档和快速入门指南，列出 Hermes-Agent 和 iFlow 为 Tier 2 支持工具。
- **FR-015**: System MUST 在 CLI `--help` 输出中将 Hermes-Agent 和 iFlow 列为可选的 AI 工具选项，标注 Tier 2。

#### 工具配置约定

- **FR-016**: System MUST 为 Hermes-Agent 定义项目级配置目录 `.hermes/`、命令模板目录 `.hermes/commands/`、命令文件扩展名 `md`、参数格式占位符 `$ARGUMENTS`。
- **FR-017**: System MUST 为 iFlow 定义项目级配置目录 `.iflow/`、命令模板目录 `.iflow/commands/`、命令文件扩展名 `md`、参数格式占位符 `$ARGUMENTS`。

### Key Entities

- **Hermes-Agent Profile**: Hermes-Agent 的助手配置档案，包含工具标识键（`hermes`）、配置目录、命令模板路径、文件扩展名、参数格式、Tier 2 分类标签。
- **iFlow Profile**: iFlow 的助手配置档案，包含工具标识键（`iflow`）、配置目录、命令模板路径、文件扩展名、参数格式、Tier 2 分类标签。
- **Extended Tier System**: 扩展后的分层支持体系——Tier 1 保持 5 款工具（Claude Code、Codex CLI、Qoder CLI、GitHub Copilot、opencode），Tier 2 从 1 款（Qwen Code）扩展为 3 款（Qwen Code、Hermes-Agent、iFlow）。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 用户选择 Hermes-Agent 或 iFlow 初始化后，可在 5 分钟内完成 Spec Kit 环境搭建并运行第一条 `/speckit.*` 命令。
- **SC-002**: 3 款 Tier 2 工具（Qwen Code、Hermes-Agent、iFlow）在能力矩阵的 Tier 2 基础审计维度上均达到 100% 覆盖。
- **SC-003**: 在同一项目中同时初始化 Tier 1 工具和 2 款新增 Tier 2 工具时，核心 `.specify` 内容和各工具专属配置之间零冲突、零覆盖。
- **SC-004**: CLI 工具选择菜单和项目文档中，Hermes-Agent 和 iFlow 被正确标注为 Tier 2 并排列在 Tier 1 工具之后。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 在空项目中分别执行 `specify init --ai hermes` 和 `specify init --ai iflow` 计时，验证配置目录和命令模板已生成，手动执行一条 `/speckit.requirements` 命令确认工作流可用。在集成测试中自动化覆盖。
- **SC-002 Source**: 运行能力矩阵审计，对 3 款 Tier 2 工具检查基础审计维度覆盖状态。在合约测试中固化断言。
- **SC-003 Source**: 在测试环境中对同一项目依次初始化 Claude Code + Hermes-Agent + iFlow，运行核心资产完整性校验和工具间隔离校验。在集成测试中自动化覆盖。
- **SC-004 Source**: 对 README、CLI `--help` 输出和 `specify init` 菜单进行静态检查，验证 Tier 2 标注和排列顺序。在合约测试中固化断言。

## Shared Strings *(optional)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-HERMES_KEY` | `"hermes"` | FR-001, FR-002, FR-003, FR-016, AGENT_CONFIG, contracts |
| `STR-IFLOW_KEY` | `"iflow"` | FR-005, FR-006, FR-007, FR-017, AGENT_CONFIG, contracts |
| `STR-TIER2` | `"tier2"` | FR-009, FR-010, FR-011, contracts |
| `STR-HERMES_DIR` | `".hermes/"` | FR-002, FR-016, contracts |
| `STR-HERMES_CMD_DIR` | `".hermes/commands/"` | FR-003, FR-016, contracts |
| `STR-IFLOW_DIR` | `".iflow/"` | FR-006, FR-017, contracts |
| `STR-IFLOW_CMD_DIR` | `".iflow/commands/"` | FR-007, FR-017, contracts |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-06-22

- Q: 本需求（019-tier2-hermes-iflow）应绑定到哪个 Feature？ → A: 绑定到 Feature 022 — AI Tools Support。作为现有 Feature 的延伸，与 Spec 018 的绑定模式一致。
- Q: Hermes-Agent 的项目级配置目录名、命令模板路径、命令文件扩展名和参数格式应采用什么约定？ → A: `.hermes/` + `.hermes/commands/` + `md` 扩展名 + `$ARGUMENTS` 参数格式，与 Claude Code / Qoder / Codex 模式一致。
- Q: iFlow 的项目级配置目录名、命令模板路径、命令文件扩展名和参数格式应采用什么约定？ → A: `.iflow/` + `.iflow/commands/` + `md` 扩展名 + `$ARGUMENTS` 参数格式，与 Hermes-Agent 及多数现有工具一致。

## Assumptions

- **Hermes-Agent 标识键**: 使用 `hermes` 作为 `AGENT_CONFIG` 和 `_OFFICIAL_ASSISTANT_KEYS` 中的标识键。
- **iFlow 标识键**: 使用 `iflow` 作为 `AGENT_CONFIG` 和 `_OFFICIAL_ASSISTANT_KEYS` 中的标识键。
- **Tier 2 标准与 Qwen Code 一致**: 新增的两款 Tier 2 工具遵循与 Qwen Code 相同的 Tier 2 支持标准——提供基础命令覆盖（初始化、命令模板、说明文件），不强制通过全部 6 个审计维度。
- **Skills 符号链接**: 新增 Tier 2 工具加入 `_SKILLS_SYMLINK_ASSISTANTS` 集合，确保 skills 目录链接正确指向 `.specify/skills/`。
- **Hermes-Agent 目录约定**: 使用 `.hermes/` 作为配置目录、`.hermes/commands/` 作为命令模板目录、`md` 扩展名、`$ARGUMENTS` 参数格式。（已通过 `/speckit.clarify` 确认）
- **iFlow 目录约定**: 使用 `.iflow/` 作为配置目录、`.iflow/commands/` 作为命令模板目录、`md` 扩展名、`$ARGUMENTS` 参数格式。（已通过 `/speckit.clarify` 确认）
- **非破坏性升级**: 已有项目升级到包含本特性的版本后，通过 `specify init` 的幂等行为自动补全新增工具资产，不影响已有配置。
- **Tier 1 工具不受影响**: 本需求仅新增 Tier 2 工具，不改变现有 5 款 Tier 1 工具和 1 款 Tier 2 工具（Qwen Code）的配置或行为。
