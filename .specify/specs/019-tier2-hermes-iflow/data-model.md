# Data Model: Tier 2 Agent Support for Hermes-Agent and iFlow

**Spec**: [requirements.md](requirements.md) | **Plan**: [plan.md](plan.md)

## Overview

This spec extends the existing assistant data model with 2 new Tier 2 tool entries. No new entities are introduced — all changes are additive rows in existing configuration dictionaries.

## Entity: Assistant Profile

The assistant profile is the central data structure for each supported AI tool. It is assembled by `get_assistant_profile(key)` from multiple source dictionaries.

### Existing Fields (unchanged)

| Field | Type | Source | Description |
|-------|------|--------|-------------|
| `key` | `str` | Parameter | Unique tool identifier |
| `name` | `str` | `AGENT_CONFIG[key]["name"]` | Human-readable display name |
| `folder` | `str` | `AGENT_CONFIG[key]["folder"]` | Project-level config directory path |
| `install_url` | `str | None` | `AGENT_CONFIG[key]["install_url"]` | CLI install URL |
| `requires_cli` | `bool` | `AGENT_CONFIG[key]["requires_cli"]` | Whether CLI binary must be present |
| `command_directory` | `str` | `_ASSISTANT_COMMAND_DIRS[key]` | Command template output directory |
| `command_format` | `str` | `_ASSISTANT_EXTENSIONS[key]` | File extension for command files |
| `arg_format` | `str` | `_ASSISTANT_ARG_FORMATS[key]` | Argument placeholder in templates |
| `officially_supported` | `bool` | Computed | Whether key is in `_OFFICIAL_ASSISTANT_KEYS` |
| `tier` | `str` | `_ASSISTANT_TIERS[key]` | Support tier: `"tier1"` or `"tier2"` |
| `skills_symlink` | `bool` | Computed | Whether key is in `_SKILLS_SYMLINK_ASSISTANTS` |

### New Rows (2 additions)

#### Hermes-Agent Profile

| Field | Value |
|-------|-------|
| `key` | `"hermes"` |
| `name` | `"Hermes Agent"` |
| `folder` | `".hermes/"` |
| `install_url` | TBD |
| `requires_cli` | `True` |
| `command_directory` | `".hermes/commands"` |
| `command_format` | `"md"` |
| `arg_format` | `"$ARGUMENTS"` |
| `officially_supported` | `True` |
| `tier` | `"tier2"` |
| `skills_symlink` | `True` |

#### iFlow Profile

| Field | Value |
|-------|-------|
| `key` | `"iflow"` |
| `name` | `"iFlow"` |
| `folder` | `".iflow/"` |
| `install_url` | TBD |
| `requires_cli` | `True` |
| `command_directory` | `".iflow/commands"` |
| `command_format` | `"md"` |
| `arg_format` | `"$ARGUMENTS"` |
| `officially_supported` | `True` |
| `tier` | `"tier2"` |
| `skills_symlink` | `True` |

## Entity: Capability Matrix Entry

Each tool × dimension pair produces one audit entry. Adding 2 tools × 6 dimensions = 12 new entries in the matrix.

| Field | Type | Description |
|-------|------|-------------|
| `tool_key` | `str` | `"hermes"` or `"iflow"` |
| `dimension` | `str` | One of: `initialization`, `command_templates`, `instructions`, `ignore_config`, `skills_symlink`, `refresh_protection` |
| `status` | `str` | `"pass"`, `"fail"`, or `"missing"` |

### Expected Audit Behavior for New Tier 2 Tools

| Dimension | Hermes | iFlow | Notes |
|-----------|--------|-------|-------|
| `initialization` | pass (after init) | pass (after init) | `.hermes/` / `.iflow/` directory exists |
| `command_templates` | pass (after init) | pass (after init) | Commands generated in `.hermes/commands/` / `.iflow/commands/` |
| `instructions` | pass (after init) | pass (after init) | `HERMES.md` / `IFLOW.md` symlink exists |
| `ignore_config` | missing | missing | No ignore file for Tier 2 tools (matches Qwen pattern) |
| `skills_symlink` | pass (after init) | pass (after init) | `.hermes/skills` / `.iflow/skills` → `.specify/skills/` |
| `refresh_protection` | pass | pass | Core `.specify/` assets preserved |

## Entity: Extended Tier System

The tier classification expands from 6 tools to 8:

| Tier | Tools (before) | Tools (after) |
|------|----------------|---------------|
| Tier 1 | claude, codex, qoder, copilot, opencode (5) | claude, codex, qoder, copilot, opencode (5) — unchanged |
| Tier 2 | qwen (1) | qwen, hermes, iflow (3) |

## Relationships

```
_OFFICIAL_ASSISTANT_KEYS (ordered list)
  └── AGENT_CONFIG (1:1 — config per key)
  └── _ASSISTANT_TIERS (1:1 — tier per key)
  └── _ASSISTANT_COMMAND_DIRS (1:1 — command dir per key)
  └── _ASSISTANT_EXTENSIONS (1:1 — file ext per key)
  └── _ASSISTANT_ARG_FORMATS (1:1 — arg format per key)
  └── _SKILLS_SYMLINK_ASSISTANTS (subset — tools needing skills symlink)
  └── _INSTRUCTIONS_FILE_MAP (1:1 — instructions file per key)
  └── _IGNORE_FILE_MAP (partial — only claude, codex have entries)
```

No new relationships introduced. Hermes and iFlow follow the same 1:1 mapping pattern.
