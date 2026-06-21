# Data Model: CLI Priority AI Tool Support

**Spec**: [requirements.md](requirements.md)
**Created**: 2026-06-21

## Entities

### AssistantProfile

Represents the configuration and metadata for a single AI tool within Spec Kit.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | `string` | Yes | Canonical identifier (e.g., `"codex"`, `"claude"`) — matches `AGENT_CONFIG` key |
| `name` | `string` | Yes | Display name (e.g., `"Codex CLI"`, `"Claude Code"`) |
| `folder` | `string` | Yes | Project-level config directory (e.g., `".codex/"`) |
| `install_url` | `string\|null` | Yes | Installation URL; `null` for IDE-based tools (Copilot) |
| `requires_cli` | `boolean` | Yes | Whether CLI installation check is needed |
| `officially_supported` | `boolean` | Yes | Whether the tool is in `_OFFICIAL_ASSISTANT_KEYS` |
| `command_directory` | `string` | Yes | Where generated command templates are written (e.g., `".codex/commands"`) |
| `command_format` | `string` | Yes | File extension for command files (e.g., `"md"`, `"prompt.md"`) |
| `arg_format` | `string` | Yes | Argument placeholder format (e.g., `"$ARGUMENTS"`, `"{{args}}"`) |
| `tier` | `"tier1"\|"tier2"` | Yes | Support priority tier |
| `skills_symlink` | `boolean` | Yes | Whether a skills symlink is needed for this tool |

**Relationships**: Each `AssistantProfile` maps 1:1 to a key in `AGENT_CONFIG`. The `tier` field is resolved from `_ASSISTANT_TIERS`.

### SupportTier

Enumerates the two-tier support classification.

| Value | Description | Tools |
|-------|-------------|-------|
| `tier1` | First-priority support with deepest Spec Kit integration | Claude Code, Codex CLI, Qoder CLI, GitHub Copilot, opencode |
| `tier2` | Standard support with basic command coverage | Qwen Code |

### CapabilityDimension

Enumerates the 6 audit dimensions of the capability matrix.

| Dimension | Description |
|-----------|-------------|
| `initialization` | Tool directory and config assets created by `specify init` |
| `command_templates` | All canonical command templates generated for the tool |
| `instructions` | Tool-specific compatibility file exists (e.g., `CLAUDE.md`, `QODER.md`) |
| `ignore_config` | Tool-specific ignore rules file exists (e.g., `.claudeignore`) |
| `skills_symlink` | Skills directory symlink or discovery config points to `.specify/skills/` |
| `refresh_protection` | Refreshing this tool does not overwrite `.specify` core or other tools |

### CapabilityMatrixEntry

A single cell in the tool × dimension capability matrix.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `tool_key` | `string` | Yes | Reference to `AssistantProfile.key` |
| `dimension` | `CapabilityDimension` | Yes | The audit dimension |
| `status` | `"pass"\|"fail"\|"missing"` | Yes | Whether the dimension is satisfied for this tool |
| `evidence` | `string` | No | File path or description proving the status |

### InitializationResultSummary (existing, extended)

Extended with a `tier` field per configured assistant.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `created` | `string[]` | Yes | List of created asset paths |
| `reused` | `string[]` | Yes | List of reused (pre-existing) asset paths |
| `skipped` | `string[]` | Yes | List of skipped assets |
| `preserved` | `string[]` | Yes | List of preserved (not overwritten) core assets |
| `conflicts` | `string[]` | Yes | List of conflicting paths |
| `attention_required` | `string[]` | Yes | List of attention messages (e.g., CLI not detected) |
| `configured_assistants` | `string[]` | Yes | List of configured assistant keys |
| `assistant_tiers` | `Record<string, string>` | No | NEW: Map of assistant key → tier for display in summary |

## State Transitions

### Tool Support Lifecycle

```
NOT_REGISTERED → REGISTERED → OFFICIALLY_SUPPORTED → TIER_CLASSIFIED
                                                        ↓
                                            INITIALIZED ↔ REFRESHED
```

- `NOT_REGISTERED`: Tool not in `AGENT_CONFIG` (e.g., new tool not yet added)
- `REGISTERED`: Tool in `AGENT_CONFIG` but not `_OFFICIAL_ASSISTANT_KEYS`
- `OFFICIALLY_SUPPORTED`: Tool in both `AGENT_CONFIG` and `_OFFICIAL_ASSISTANT_KEYS`
- `TIER_CLASSIFIED`: Tool has a `tier` assignment in `_ASSISTANT_TIERS`
- `INITIALIZED`: Project has been initialized with this tool (folder + commands exist)
- `REFRESHED`: Tool assets have been refreshed without overwriting core content

## Validation Rules

1. Every key in `_ASSISTANT_TIERS` MUST exist in `AGENT_CONFIG`.
2. Every key in `_OFFICIAL_ASSISTANT_KEYS` MUST have a corresponding entry in `_ASSISTANT_TIERS`.
3. Tier 1 tools MUST pass all 6 capability dimensions during audit.
4. Tier 2 tools MUST pass `initialization` and `command_templates` dimensions; other dimensions are optional.
5. `tier` field returned by `get_assistant_profile()` MUST NOT be null for any officially supported tool.
