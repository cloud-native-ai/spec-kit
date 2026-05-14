# Data Model: Claude Code Support

## Overview

This feature does not introduce persistent application data. It defines file-based configuration, generated assistant assets, validation rules, and support-surface audit concepts used by planning, tasks, implementation, and tests.

## Entities

### 1. `SupportedAssistant`

Represents an assistant that users can select during project initialization and that the project recognizes as officially supported.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | yes | Stable machine identifier, e.g., `claude` |
| `display_name` | string | yes | User-facing name, e.g., `Claude Code` |
| `assistant_type` | enum | yes | `ide` or `cli` |
| `folder` | string | yes | Primary assistant-specific folder, e.g., `.claude/` |
| `install_url` | string/null | yes | User-facing install/setup guidance URL when validation fails |
| `requires_cli` | boolean | yes | Whether local CLI validation is expected by default |
| `approved` | boolean | yes | Whether governance treats the assistant as officially supported |

**Validation Rules**:

- `key` must be unique across all supported assistants.
- `approved=true` requires matching constitution, README, docs, CLI help, and generated template support claims.
- `requires_cli=true` requires a validation path and an `--ignore-agent-tools` bypass path.

### 2. `ClaudeCodeAssetSet`

Represents the Claude Code-specific files and directories generated for a project.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assistant_key` | string | yes | Must reference `SupportedAssistant.key` |
| `guidance_path` | string | yes | Claude Code guidance or compatibility file path |
| `command_directory` | string | yes | Directory containing generated Claude Code custom commands |
| `ignore_path` | string | yes | Claude Code ignore configuration path, expected as `.claudeignore` |
| `skills_link_path` | string/null | no | Optional compatibility link to canonical Spec Kit skills |
| `generated_on_init` | boolean | yes | Whether assets are created during new-project initialization |
| `generated_on_refresh` | boolean | yes | Whether assets are refreshed in existing workspaces |
| `canonical_source` | string | yes | Source-of-truth path for generated/linked content |

**Validation Rules**:

- `ignore_path` must exist for Claude Code-ready projects.
- Generated command files must map to the canonical command template inventory.
- Assets derived from canonical instructions must not become independent workflow sources.

### 3. `ClaudeCodeCommandSurface`

Represents a Claude Code custom command that exposes one canonical Spec Kit workflow command.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `command_name` | string | yes | User-invocable command name |
| `canonical_template` | string | yes | Source template under `templates/commands/` |
| `output_path` | string | yes | Generated Claude Code command file path |
| `argument_format` | string | yes | Handoff placeholder, expected to preserve `$ARGUMENTS` semantics |
| `description` | string | yes | Short user-facing purpose |
| `included` | boolean | yes | Whether this command is generated for Claude Code |
| `exclusion_reason` | string/null | no | Required if `included=false` |

**Validation Rules**:

- Every canonical Spec Kit workflow command must have `included=true` or a documented `exclusion_reason`.
- Command descriptions must match the intent of their canonical templates.
- Generated command paths must not overwrite unrelated assistant commands.

### 4. `ClaudeCodeIgnorePolicy`

Represents path categories excluded from Claude Code context.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `policy_path` | string | yes | Expected `.claudeignore` file path |
| `excluded_categories` | array<string> | yes | Category names such as dependencies, caches, build outputs, secrets, local environments |
| `preserved_paths` | array<string> | yes | Required workflow paths that must remain available |
| `privacy_rationale` | string | yes | Why the defaults protect users |
| `validation_status` | enum | yes | `pending`, `verified`, or `failed` |

**Validation Rules**:

- Must exclude common dependency, cache, build, temporary, local environment, and secret-like files.
- Must not exclude required `.specify/` workflow artifacts, canonical instructions, or generated Claude Code commands.
- Must be auditable without requiring access to private user files.

### 5. `AssistantRefreshRule`

Represents how generated assets are updated in existing workspaces.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assistant_key` | string | yes | Assistant being refreshed |
| `target_assets` | array<string> | yes | Assets eligible for refresh |
| `preserve_user_content` | boolean | yes | Whether user-authored content must be preserved |
| `conflict_behavior` | enum | yes | `preserve`, `merge`, `warn`, or `block` |
| `unrelated_roots_untouched` | array<string> | yes | Other assistant roots that must not be modified |

**Validation Rules**:

- Refresh must not delete or rewrite unrelated assistant integrations.
- User customizations must be preserved or a clear conflict must be reported.
- Canonical instruction changes must propagate to Claude Code compatibility surfaces.

### 6. `SupportSurfaceAudit`

Represents a consistency check across user-facing and release-facing support claims.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `surface_id` | string | yes | Stable audit identifier |
| `surface_type` | enum | yes | `cli-help`, `documentation`, `template`, `script-output`, `test`, `release-output`, or `governance` |
| `location` | string | yes | File or output being audited |
| `must_include_assistants` | array<string> | yes | Assistant keys expected on the surface |
| `consistent` | boolean | yes | Whether the surface matches the support matrix |
| `release_blocking` | boolean | yes | Whether failure blocks release readiness |

**Validation Rules**:

- Claude Code must appear on all surfaces where supported assistants are enumerated.
- Governance surfaces are release-blocking.
- Audit failures must identify the mismatched location and expected wording or support state.

## Relationships

- `SupportedAssistant 1..1 -> 1..1 ClaudeCodeAssetSet`
- `SupportedAssistant 1..1 -> 1..* ClaudeCodeCommandSurface`
- `ClaudeCodeAssetSet 1..1 -> 1..1 ClaudeCodeIgnorePolicy`
- `SupportedAssistant 1..1 -> 1..* AssistantRefreshRule`
- `SupportedAssistant 1..* -> 1..* SupportSurfaceAudit`

## State Transitions

### Assistant validation

- `unchecked` → `available`
- `unchecked` → `missing`
- `missing` → `ignored`
- `missing` → `blocked`

### Asset refresh

- `not-present` → `generated`
- `generated` → `refreshed`
- `customized` → `preserved`
- `customized` → `conflict-reported`

### Support surface audit

- `pending` → `pass`
- `pending` → `fail`
- `fail` → `fixed`

## Derived Rules for Claude Code

1. `SupportedAssistant(key=claude).approved` can only be `true` after governance is updated.
2. `ClaudeCodeAssetSet(ignore_path=.claudeignore)` is required for Claude Code-ready projects.
3. `ClaudeCodeCommandSurface` coverage must match the canonical `templates/commands/*.md` inventory.
4. `ClaudeCodeIgnorePolicy.preserved_paths` must include required Spec Kit workflow artifacts.
5. `SupportSurfaceAudit` failures for governance, CLI help, docs, or packaged templates are release-blocking.
