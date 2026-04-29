# Data Model: MCP Tool Call

**Branch**: 002-mcp-tool-call | **Date**: 2026-02-10

## Entities

### McpToolRecord
- **Description**: Local MCP tool record for reusing tool definitions and invocation information.
- **Fields**:
  - name: string (required, tool name)
  - server: string (required, owning MCP Server)
  - description: string ([CN])
  - parameters: array<McpToolParameter> ([CN])
  - returns: array<McpToolReturn> ([CN])
  - status: string (Draft | Verified | Deprecated)
  - last_updated: date (YYYY-MM-DD)
  - usage_notes: array<string>
  - examples: array<McpToolExample>

### McpToolParameter
- **Description**: [CN]
- **Fields**:
  - name: string
  - type: string
  - required: boolean
  - description: string
  - default: string | null

### McpToolReturn
- **Description**: [CN]
- **Fields**:
  - name: string
  - type: string
  - description: string

### McpToolExample
- **Description**: [CN]
- **Fields**:
  - input: object
  - output: object

### McpCallSession
- **Description**: [CN] `/speckit.tools`[CN]MCP [CN]
- **Fields**:
  - tool_name: string
  - used_record: boolean
  - discovery_source: string | null
  - executed_at: datetime
  - result_summary: string

## Validation Rules

- McpToolRecord [CN] name[CN]server[CN]description[CN]
- [CN]
- [CN] Draft[CN]Verified [CN] Deprecated[CN]
- last_updated [CN] ISO [CN]YYYY-MM-DD[CN]
