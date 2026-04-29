# Data Model: Add Qoder Support

## Overview

This feature does not introduce a database, but requires clear file-based configuration and release consistency objects as a shared language for subsequent tasks, implementation, and testing.

## Entities

### 1. `SupportedAssistant`

Represents an assistant definition that can be selected by `specify init` and recognized by public documentation.

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `key` | string | yes | Machine identifier, e.g., `copilot`, `qwen`, `opencode`, `qoder` |
| `display_name` | string | yes | [CN] `Qoder CLI` |
| `assistant_type` | enum | yes | `ide` [CN] `cli` |
| `folder` | string | yes | [CN] `.qoder/` |
| `command_dir` | string | yes | [CN] `.qoder/commands/` |
| `command_extension` | string | yes | [CN] `md` |
| `argument_format` | string | yes | [CN] `$ARGUMENTS` |
| `install_url` | string/null | yes | CLI [CN]IDE [CN] |
| `requires_cli` | boolean | yes | [CN] CLI |
| `approved` | boolean | yes | [CN] |

**Validation Rules**:
- `key` [CN]
- `approved=true` [CN]README/[CN]CLI [CN]
- `assistant_type=cli` [CN]`install_url` [CN] `requires_cli` [CN]

### 2. `AssistantAssetSet`

[CN]

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `assistant_key` | string | yes | [CN] `SupportedAssistant.key` |
| `project_rules_path` | string | no | [CN]/[CN]File path[CN] `.qoder/project_rules.md` |
| `command_paths` | array<string> | yes | [CN] |
| `generated_on_init` | boolean | yes | [CN] |
| `generated_on_refresh` | boolean | yes | [CN] |
| `scope` | enum | yes | `new-project` [CN] `existing-directory` [CN] `both` |

**Validation Rules**:
- `assistant_key=qoder` [CN]`command_paths` [CN] `.qoder/commands/`[CN]
- `generated_on_refresh=true` [CN]

### 3. `AssistantValidationRule`

[CN]

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `assistant_key` | string | yes | [CN] |
| `cli_command` | string | no | [CN] `qoder` |
| `skip_flag` | string | yes | [CN] flag[CN] `--ignore-agent-tools` |
| `failure_message_template` | string | yes | [CN] |
| `install_url` | string | no | [CN] |

**State Transitions**:
- `unchecked` → `available`
- `unchecked` → `missing`
- `missing` → `ignored`

### 4. `SupportSurface`

[CN]

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `surface_id` | string | yes | [CN] `readme-supported-agents` |
| `surface_type` | enum | yes | `cli-help`[CN]`documentation`[CN]`template`[CN]`script-output`[CN]`release-output` |
| `location` | string | yes | File path[CN] |
| `must_include_assistants` | array<string> | yes | [CN] key |
| `must_include_install_guidance` | boolean | yes | [CN]/[CN] |
| `release_blocking` | boolean | yes | [CN] |

**Validation Rules**:
- [CN] Qoder [CN]`release_blocking` [CN] `true`[CN]
- [CN] `SupportedAssistant` [CN]

### 5. `DistributionVariant`

[CN]

| Field | Type | Required | Description |
|------|------|----------|-------------|
| `variant_id` | string | yes | [CN] `spec-kit-template-qoder-sh` |
| `assistant_key` | string | yes | [CN] |
| `script_variant` | enum | yes | `sh`[CN] |
| `artifact_type` | enum | yes | `wheel-resource`[CN]`template-archive`[CN]`generated-project` |
| `expected_assets` | array<string> | yes | [CN]/[CN] |
| `audit_status` | enum | yes | `pending`[CN]`generated`[CN]`verified`[CN]`failed` |

**State Transitions**:
- `pending` → `generated`
- `generated` → `verified`
- `generated` → `failed`

## Relationships

- `SupportedAssistant 1..1 -> 0..1 AssistantValidationRule`
- `SupportedAssistant 1..1 -> 1..* AssistantAssetSet`
- `SupportedAssistant 1..* -> 1..* SupportSurface`
- `SupportedAssistant 1..* -> 0..* DistributionVariant`

## Derived Rules for Qoder

1. `SupportedAssistant(key=qoder).approved` [CN] `true` [CN] feature [CN]
2. `AssistantValidationRule(assistant_key=qoder).skip_flag` [CN] `--ignore-agent-tools`[CN]
3. `AssistantAssetSet(assistant_key=qoder)` [CN] `new-project` [CN] `existing-directory`[CN]
4. [CN] `SupportSurface` [CN] `qoder`[CN]
5. [CN] `DistributionVariant` [CN] Qoder [CN]