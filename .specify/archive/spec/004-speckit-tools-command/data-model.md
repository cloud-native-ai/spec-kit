# Data Model: Speckit Tools Command

**Branch**: 004-speckit-tools-command | **Date**: 2026-03-02

## Entities

### ToolRecord
- **Description**: Unified tool record document stored at `.specify/memory/tools/<tool-name>.md`.
- **Fields**:
  - name: string (required, tool name)
  - tool_type: string (required, `mcp` | `system` | `shell` | `project`)
  - source_identifier: string[CN] server/tool/path[CN]
  - description: string[CN]
  - arguments: array<ToolArgument>[CN]
  - returns: array<ToolReturnField>[CN]
  - aliases: array<ToolAlias>[CN]
  - status: string[CN]Draft | Verified | Deprecated[CN]
  - last_updated: date[CN]YYYY-MM-DD[CN]

### ToolSourceDescriptor
- **Description**: [CN]
- **Fields**:
  - source_type: string[CN]`mcp` | `system` | `shell` | `project`[CN]
  - source_name: string[CN] mcp server [CN]
  - canonical_name: string[CN]
  - display_name: string[CN]
  - metadata: object[CN]

### ToolArgument
- **Description**: [CN]
- **Fields**:
  - name: string
  - type: string
  - required: boolean
  - description: string
  - default: string | null

### ToolReturnField
- **Description**: [CN]
- **Fields**:
  - name: string
  - type: string
  - description: string

### ToolAlias
- **Description**: [CN]
- **Fields**:
  - alias: string
  - canonical_name: string
  - note: string | null

### ToolInvocationSession
- **Description**: [CN] `/speckit.tools` [CN]
- **Fields**:
  - requested_name: string
  - resolved_name: string
  - resolved_type: string
  - used_existing_record: boolean
  - disambiguation_required: boolean
  - user_confirmed_execution: boolean
  - result_status: string[CN]success | cancelled | failed[CN]
  - result_summary: string
  - executed_at: datetime

## Validation Rules

- ToolRecord [CN] `name`[CN]`tool_type`[CN]`source_identifier`[CN]`description`[CN]
- `tool_type` [CN]
- [CN] `status=Verified` [CN]`arguments` [CN] `returns` [CN]
- ToolAlias [CN] `alias` [CN]
- ToolInvocationSession [CN] `user_confirmed_execution=false` [CN]`result_status` [CN] `cancelled`[CN]
