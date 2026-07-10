# Tool Definitions Reference

Detailed behavioral rules format, tool type semantics, and edge case handling for `/speckit.tools`.

## Tool Type Standardization

| Type | Scope | Description | Source Identifier |
|------|-------|-------------|-------------------|
| `project-script` | Project-level | Scripts bundled with the current project (e.g., `scripts/bash/*.sh`). Available only within the project workspace. | Path relative to project root |
| `system-binary` | System-level | Executables installed system-wide via package manager or `PATH`. Available to all users/sessions. | Absolute binary path |
| `shell-function` | Shell-session | Functions loaded via `source` from dotfiles or activation scripts. Available only in current shell session. | Function name |
| `webhook` | Network-level | Remote operations triggered by HTTP request to a web endpoint. Available wherever HTTP connectivity and credentials exist. | URL endpoint |

## Behavioral Rules Format

Each behavioral rule MUST be a markdown bullet prefixed with an RFC 2119 keyword:

- `MUST` — absolute requirement the agent must follow in every invocation
- `MUST NOT` — absolute prohibition the agent must never violate
- `SHOULD` — recommended practice unless a justified exception applies
- `SHOULD NOT` — discouraged practice unless a justified exception applies

Format: `- {KEYWORD} {constraint text}`

These rules are **authoritative**: when a tool has a definition record, the AI agent MUST use the persisted behavioral rules as the source of truth, instead of relying on training knowledge about the tool.

## Edge Cases

- **Name conflict across types**: When same name exists under different types, require explicit user disambiguation. Present all matching records.
- **Non-existent source**: When tool references a source path that doesn't exist, warn user but allow record creation with `Draft` status.
- **Incomplete record invocation**: Block invocation of `Draft` tools. Guide user to complete the definition.
- **Contradictory behavioral rules**: Persist rules as-is with advisory note. User is authoritative source.

## Invocation Preview Format

Before executing any tool, display:

```
## Invocation Preview

**Tool**: <name> (<tool_type>)
**Command**: <resolved command>
**Parameters**: <resolved parameter values>

### Behavioral Rules
- MUST <rule 1>
- MUST NOT <rule 2>
...

**Expected Output**: <output shape>
```

Prompt: `Proceed with execution? (yes/no)`
- Only execute if explicit `yes`
- Do NOT modify parameters beyond what was previewed
- Record invocation session: tool_name, tool_id, resolved_command, result_status

## Output Requirements

- Tool records stored in `.specify/memory/tools/` as `.md` files
- Command output must include `tool_id` and canonical path
- Execution never happens before user confirmation via preview gate
- Existing complete records should be reused (avoid repeated discovery)
- AI agent MUST use persisted records as authoritative source
