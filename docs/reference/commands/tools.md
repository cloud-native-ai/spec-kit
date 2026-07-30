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

## Modes → Intent Routing

`/speckit.tools` is the **single entry point** for every tool operation. It recognizes intent and routes to the owning skill; it does not render templates inline.

| Mode | Recognized intent | Routes to |
|------|-------------------|-----------|
| **define** | "定义工具", "创建工具", "define/create/add/register a tool" | `create-tools` skill |
| **modify** | "修改工具", "优化工具", "modify/improve/fix a tool", "add alias", "verify tool" | `improve-tools` skill |
| **view** | "查看工具", "view/show a tool" | read-only display |
| **list** | "列出工具", "list tools" | read-only display |
| **invoke** | "调用工具", "执行工具", "invoke/run a tool" | invocation gate |

**Definition-first**: a record exists so its behavioral rules **override the agent's built-in training knowledge**. Mandatory fields therefore come from the user; discovery only bootstraps a `Draft` for the user to complete. A record auto-filled from model knowledge would defeat its own purpose.

Empty arguments list all records plus contextual suggestions; ambiguous intent reports the capability list rather than guessing.

## Tool Types

| Type | Scope | Example |
|------|-------|---------|
| `project-script` | Project-level | `scripts/bash/deploy.sh` |
| `system-binary` | System-level | `/usr/bin/jq`, `/usr/local/bin/docker` |
| `shell-function` | Shell-session-level | Functions from `${HOME}/.bashrc` |
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

## Companion Skills

| Skill | Owns | Canonical path |
|-------|------|----------------|
| `create-tools` | Authoring a new record: intake, template selection, validation, persistence, registry row | `.specify/skills/create-tools/SKILL.md` |
| `improve-tools` | Field-level refinement of an existing record: source/contract correction, rule hardening, alias/rename, `Draft` → `Verified` promotion | `.specify/skills/improve-tools/SKILL.md` |

The four type templates live inside the owning skill at `.specify/skills/create-tools/templates/` (`tool-project-script-template.md`, `tool-system-binary-template.md`, `tool-shell-function-template.md`, `tool-webhook-template.md`). Shared type semantics, the rules format, and the invocation preview contract are defined once in `.specify/shared/definitions/tool-definitions.md`.

**Dogfooding**: Spec Kit manages its own core scripts through this command — see the `### Tools` registry in `.specify/instructions.md` and the records under `.specify/memory/tools/`.

## Prerequisites

- (Optional) Repo available for project-script discovery

## Next Steps

- Depends on the tool defined — use it in subsequent workflow steps
