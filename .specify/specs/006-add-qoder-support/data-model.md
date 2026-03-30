# Data Model: Add Qoder Support

## Overview

本 feature 不引入数据库，但需要明确文件型配置与发布一致性对象，作为后续 tasks、实现与测试的共享语言。

## Entities

### 1. `SupportedAssistant`

表示一个可被 `specify init` 选择并被公开文档承认的助手定义。

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `key` | string | yes | 机器标识，如 `copilot`、`qwen`、`opencode`、`qoder` |
| `display_name` | string | yes | 用户可见名称，如 `Qoder CLI` |
| `assistant_type` | enum | yes | `ide` 或 `cli` |
| `folder` | string | yes | 助手根目录，如 `.qoder/` |
| `command_dir` | string | yes | 命令文件输出目录，如 `.qoder/commands/` |
| `command_extension` | string | yes | 命令文件扩展名，如 `md` |
| `argument_format` | string | yes | 模板参数占位格式，如 `$ARGUMENTS` |
| `install_url` | string/null | yes | CLI 安装指引链接；IDE 型助手可为空 |
| `requires_cli` | boolean | yes | 是否必须检查本地 CLI |
| `approved` | boolean | yes | 是否在治理白名单与公开支持列表中正式获批 |

**Validation Rules**:
- `key` 必须唯一。
- `approved=true` 的助手必须同时出现在宪法、README/安装文档、CLI 帮助与模板白名单中。
- `assistant_type=cli` 时，`install_url` 与 `requires_cli` 必须可用。

### 2. `AssistantAssetSet`

表示某个助手在用户项目中可用的最小资产集合。

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `assistant_key` | string | yes | 关联 `SupportedAssistant.key` |
| `project_rules_path` | string | no | 助手说明/上下文文件路径，如 `.qoder/project_rules.md` |
| `command_paths` | array<string> | yes | 生成的命令文件列表 |
| `generated_on_init` | boolean | yes | 是否在初始化时生成 |
| `generated_on_refresh` | boolean | yes | 是否在刷新时更新 |
| `scope` | enum | yes | `new-project` 或 `existing-directory` 或 `both` |

**Validation Rules**:
- `assistant_key=qoder` 时，`command_paths` 必须位于 `.qoder/commands/`。
- `generated_on_refresh=true` 时，不得要求先删除其他助手目录。

### 3. `AssistantValidationRule`

表示某个助手在初始化或检查时的依赖校验规则。

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `assistant_key` | string | yes | 关联助手 |
| `cli_command` | string | no | 需检查的二进制，如 `qoder` |
| `skip_flag` | string | yes | 允许跳过校验的 flag，当前统一为 `--ignore-agent-tools` |
| `failure_message_template` | string | yes | 缺少依赖时显示的错误文案模板 |
| `install_url` | string | no | 错误提示中使用的安装链接 |

**State Transitions**:
- `unchecked` → `available`
- `unchecked` → `missing`
- `missing` → `ignored`

### 4. `SupportSurface`

表示任何会公开宣称助手支持状态的用户可见面。

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `surface_id` | string | yes | 唯一标识，如 `readme-supported-agents` |
| `surface_type` | enum | yes | `cli-help`、`documentation`、`template`、`script-output`、`release-output` |
| `location` | string | yes | 文件路径或生成目标 |
| `must_include_assistants` | array<string> | yes | 该表面必须列出的助手 key |
| `must_include_install_guidance` | boolean | yes | 是否必须提供安装/获取信息 |
| `release_blocking` | boolean | yes | 不一致是否构成发布阻塞 |

**Validation Rules**:
- 对 Qoder 相关表面，`release_blocking` 必须为 `true`。
- 若表面列出支持助手，则命名与链接必须与 `SupportedAssistant` 一致。

### 5. `DistributionVariant`

表示一个发布或分发模板变体。

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `variant_id` | string | yes | 如 `spec-kit-template-qoder-sh` |
| `assistant_key` | string | yes | 关联助手 |
| `script_variant` | enum | yes | `sh`（当前仓库主路径） |
| `artifact_type` | enum | yes | `wheel-resource`、`template-archive`、`generated-project` |
| `expected_assets` | array<string> | yes | 该变体应包含的关键文件/目录 |
| `audit_status` | enum | yes | `pending`、`generated`、`verified`、`failed` |

**State Transitions**:
- `pending` → `generated`
- `generated` → `verified`
- `generated` → `failed`

## Relationships

- `SupportedAssistant 1..1 -> 0..1 AssistantValidationRule`
- `SupportedAssistant 1..1 -> 1..* AssistantAssetSet`
- `SupportedAssistant 1..* -> 1..* SupportSurface`
- `SupportedAssistant 1..* -> 0..* DistributionVariant`

## Derived Rules for Qoder

1. `SupportedAssistant(key=qoder).approved` 必须为 `true` 才算 feature 完成。
2. `AssistantValidationRule(assistant_key=qoder).skip_flag` 必须是 `--ignore-agent-tools`。
3. `AssistantAssetSet(assistant_key=qoder)` 必须覆盖 `new-project` 与 `existing-directory`。
4. 所有列出支持助手的 `SupportSurface` 必须同步包含 `qoder`，否则视为发布阻塞缺陷。
5. 至少一个 `DistributionVariant` 必须能证明 Qoder 相关模板资产进入标准分发流程。