# /speckit.tools

Define, modify, view, or invoke reusable tools with persistent records and explicit behavioral rules.

## When to Use

- To define a new tool record with behavioral rules that the AI agent must follow
- To modify or view an existing tool definition
- To invoke a defined tool with preview and confirmation
- To list all registered tools in the project

## Syntax

```text
/speckit.tools [argument]
```

| Input | Intent |
|-------|--------|
| Tool purpose or name | Define a new tool or view an existing one |
| `tool_id` | Resolve by ID |
| Verb phrase ("run...", "execute...") | Invoke a defined tool |
| No arguments | List all registered tools |

**Important**: Natural-language arguments describe the **tool capability to define**, not immediate execution. `/speckit.tools download DingTalk docs` means "create/locate a tool for downloading DingTalk docs", not "download now".

## Tool Types

| Type | Scope | Example |
|------|-------|---------|
| `project-script` | Project-level | `scripts/bash/deploy.sh` |
| `system-binary` | System-level | `/usr/bin/jq`, `/usr/local/bin/docker` |
| `shell-function` | Shell-session-level | Functions from `~/.bashrc` |
| `webhook` | Network-level | `https://ci.example.com/api/trigger-build` |

## Execution Flow

### Define (create new tool)

1. **Collect mandatory fields** from the user:
   - **Tool Name**: Identifier for the tool
   - **Tool Type**: One of the four canonical types
   - **Source Identifier**: Script path, binary path, function name, or URL
   - **Description**: What this tool does in the project context

2. **Collect optional behavioral rules** — RFC 2119 format:
   - `MUST` — absolute requirement for every invocation
   - `MUST NOT` — absolute prohibition
   - `SHOULD` / `SHOULD NOT` — recommended/discouraged practices

3. **Persist record** at `.specify/memory/tools/<tool-name>.md` with a deterministic `tool_id`.

4. **Register** in the Resource Registry of `.specify/instructions.md`.

### Modify (update existing tool)

- Field-level updates only — unchanged fields are preserved
- Behavioral rules support add, remove, and replace operations
- Re-validates mandatory fields after modification

### View / List

- **Single tool**: Displays complete definition including behavioral rules
- **List mode**: Summary table of all registered tools

### Invoke (execute a defined tool)

1. **Preview** — Displays resolved command, parameters, and applicable behavioral rules
2. **Confirm** — Explicit `Proceed with execution? (yes/no)` prompt
3. **Execute** — Runs exactly as previewed (no parameter modifications)
4. **Record** — Logs the invocation session

## Behavioral Rules

Rules are **authoritative** — when a tool has a definition record, the AI agent uses the persisted behavioral rules instead of its training knowledge.

```markdown
- MUST redirect stderr to a log file when running in CI
- MUST NOT pass credentials via command-line arguments
- SHOULD use --dry-run flag for first invocation on production data
```

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Tool definition | `.specify/memory/tools/<tool-name>.md` |
| Registry update | `.specify/instructions.md` → Tools section |

## Tool Statuses

| Status | Meaning |
|--------|---------|
| Draft | Missing mandatory fields or parameters |
| Verified | All mandatory fields present, ready for invocation |

## Edge Cases

- **Name conflict**: Same tool name under different types requires user disambiguation
- **Non-existent source**: Warning issued but record created as `Draft`
- **Incomplete record invocation**: Blocked with guidance to complete the definition
- **Contradictory rules**: Persisted as-is with advisory note (user is authoritative)

## Prerequisites

- (Optional) Repo available for project-script discovery

## Next Steps

- Depends on the tool defined — use it in subsequent workflow steps
