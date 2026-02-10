# Data Model: MCP Tool Call

**Branch**: 002-mcp-tool-call | **Date**: 2026-02-10

## Entities

### McpToolRecord
- **Description**: 本地 MCP 工具记录，用于复用工具定义与调用信息。
- **Fields**:
  - name: string (必填，工具名称)
  - server: string (必填，所属 MCP Server)
  - description: string (必填，工具用途说明)
  - parameters: array<McpToolParameter> (可为空)
  - returns: array<McpToolReturn> (可为空)
  - status: string (Draft | Verified | Deprecated)
  - last_updated: date (YYYY-MM-DD)
  - usage_notes: array<string>
  - examples: array<McpToolExample>

### McpToolParameter
- **Description**: 工具参数定义。
- **Fields**:
  - name: string
  - type: string
  - required: boolean
  - description: string
  - default: string | null

### McpToolReturn
- **Description**: 工具返回值字段定义。
- **Fields**:
  - name: string
  - type: string
  - description: string

### McpToolExample
- **Description**: 调用示例与期望输出。
- **Fields**:
  - input: object
  - output: object

### McpCallSession
- **Description**: 一次 `/speckit.mcpcall` 调用会话。
- **Fields**:
  - tool_name: string
  - used_record: boolean
  - discovery_source: string | null
  - executed_at: datetime
  - result_summary: string

## Validation Rules

- McpToolRecord 必须包含 name、server、description。
- 参数与返回值字段名称不可为空。
- 状态必须为 Draft、Verified 或 Deprecated。
- last_updated 必须是 ISO 日期格式（YYYY-MM-DD）。
