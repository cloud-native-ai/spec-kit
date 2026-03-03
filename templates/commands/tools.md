---
description: Explicitly describe and invoke a tool via reusable local records across MCP/System/Shell/Project sources.
handoffs:
  - label: Create Plan
    agent: speckit.plan
    prompt: Generate an implementation plan for /speckit.tools
    send: false
scripts:
  sh: scripts/bash/refresh-tools.sh --mcp --system --shell --project
---

> Note: `$ARGUMENTS` is **optional**. If empty, continue with discovery + interactive disambiguation. If provided, treat it as hint(s) for target tool, source type, alias preference, or execution priority.

## User Input

```text
$ARGUMENTS
```

You **MUST** treat `$ARGUMENTS` as command parameters, not as a replacement of this workflow.

## Outline

Goal: Resolve one target tool, ensure a complete ToolRecord exists at `.specify/memory/tools/<tool-name>.md`, show execution preview, and execute only after explicit confirmation.

### Tool Type Standardization

Tool naming and categorization MUST use the following four canonical types:

1. `mcp-call`: invoke MCP services.
2. `project-script`: scripts inside the current project, typically custom project-specific capabilities.
3. `system-binary`: binary tools in the current runtime environment (on Linux, typically tools like `find`, `grep`, etc.).
4. `shell-function`: functions defined in the current shell session (e.g., bash functions loaded at session startup via `~/.bashrc`).

In `refresh-tools.sh`, discovery MUST use JSON mode only when calling each Python discovery script. Then combine discovered JSON data with `templates/tool-*.md` template files (current repository pattern: `templates/tool-*-template.md`) to generate Markdown tool description documents.

Execution steps:

1. **Identify target tool basic info**
   - Parse `$ARGUMENTS` to extract tool name or intent.
   - If missing, present interactive selection from available tools.

2. **Discover tools via JSON**
   - Run `scripts/bash/refresh-tools.sh --mcp --system --shell --project` to get JSON output.
   - Parse JSON and map tool to its source type (`mcp-call`, `project-script`, `system-binary`, `shell-function`).

3. **Resolve naming and conflicts**
   - Check exact name, alias match, and fuzzy candidates.
   - If same name exists across source types, require explicit user disambiguation before continuing.

4. **Reuse or create tool record**
   - Primary location: `.specify/memory/tools/<tool-name>.md`.
   - If existing record is complete, reuse directly.
   - If missing or incomplete, create/update from `templates/tool-*-template.md` with generalized ToolRecord fields:
     - Tool Name / Tool Type / Source Identifier / Description / Status / Last Updated
     - Parameters / Returns / Aliases

5. **Validate record before invocation**
   - Required fields: `name`, `tool_type`, `source_identifier`, `description`.
   - `tool_type` must be one of `mcp-call|project-script|system-binary|shell-function`.
   - If status is `Verified`, Parameters and Returns cannot both be empty.
   - If invalid, guide user to fill missing fields and re-validate.

6. **Collect and sanitize parameters**
   - Collect required parameters one by one.
   - Apply minimal sanitization/escaping rules based on source type.
   - Produce one compact preview summary: source, tool, arguments, expected return shape.

7. **Explicit confirmation gate**
   - Ask: `Proceed with execution? (yes/no)`.
   - `yes` → execute tool.
   - otherwise → mark session as cancelled and do not execute.

8. **Report session result and persist artifacts**
   - Write/update tool record.
   - Record invocation session status (`success|failed|cancelled`) with summary.
   - If user asks to rename/alias, update record aliases and ensure uniqueness.

## Output Requirements

- Tool records are stored in `.specify/memory/tools/` as `.md` files.
- Execution must not happen before user confirmation.
- Conflict scenarios must be resolved before invocation.
- Existing complete records should be reused to avoid repeated discovery.
- Alias/rename changes must remain discoverable by future `/speckit.tools` calls.