# Data Model: Speckit Tools Command

**Branch**: 004-speckit-tools-command | **Date**: 2026-03-02

## Entities

### ToolRecord
- **Description**: 存放在 `.specify/memory/tools/<tool-name>.md` 的统一工具记录文档。
- **Fields**:
  - name: string（必填，工具名称）
  - tool_type: string（必填，`mcp` | `system` | `shell` | `project`）
  - source_identifier: string（必填，来源唯一标识，如 server/tool/path）
  - description: string（必填，用途说明）
  - arguments: array<ToolArgument>（可空）
  - returns: array<ToolReturnField>（可空）
  - aliases: array<ToolAlias>（可空）
  - status: string（Draft | Verified | Deprecated）
  - last_updated: date（YYYY-MM-DD）

### ToolSourceDescriptor
- **Description**: 一条可发现工具来源的标准化描述。
- **Fields**:
  - source_type: string（`mcp` | `system` | `shell` | `project`）
  - source_name: string（来源名称，如 mcp server 名）
  - canonical_name: string（工具原始名称）
  - display_name: string（可展示名称）
  - metadata: object（来源附加信息）

### ToolArgument
- **Description**: 工具参数定义。
- **Fields**:
  - name: string
  - type: string
  - required: boolean
  - description: string
  - default: string | null

### ToolReturnField
- **Description**: 工具返回结构中的字段定义。
- **Fields**:
  - name: string
  - type: string
  - description: string

### ToolAlias
- **Description**: 用户对工具记录的封装或重命名映射。
- **Fields**:
  - alias: string
  - canonical_name: string
  - note: string | null

### ToolInvocationSession
- **Description**: 一次 `/speckit.tools` 命令会话。
- **Fields**:
  - requested_name: string
  - resolved_name: string
  - resolved_type: string
  - used_existing_record: boolean
  - disambiguation_required: boolean
  - user_confirmed_execution: boolean
  - result_status: string（success | cancelled | failed）
  - result_summary: string
  - executed_at: datetime

## Validation Rules

- ToolRecord 必须包含 `name`、`tool_type`、`source_identifier`、`description`。
- `tool_type` 必须属于受支持四类之一。
- 当 `status=Verified` 时，`arguments` 与 `returns` 字段不得全部缺失。
- ToolAlias 的 `alias` 在同一工具记录命名空间内必须唯一。
- ToolInvocationSession 在 `user_confirmed_execution=false` 时，`result_status` 只能为 `cancelled`。
