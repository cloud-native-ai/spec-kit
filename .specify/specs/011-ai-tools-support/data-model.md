# Data Model: AI Tools Support

## Overview

This feature does not introduce persistent application data or a database. It defines file-based configuration concepts, generated assistant assets, preservation decisions, and validation summaries used by CLI initialization, refresh flows, tests, and release audits.

## Entities

### 1. `AssistantSupportProfile`

Represents one officially supported AI tool that can be selected during initialization or audited for support parity.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `key` | string | yes | Stable machine key such as `copilot`, `claude`, `qwen`, `opencode`, or `qoder`. |
| `display_name` | string | yes | User-facing assistant name. |
| `assistant_type` | enum | yes | `ide` or `cli`. |
| `root_folder` | string | yes | Assistant-specific project root, such as `.github/` or `.claude/`. |
| `command_directory` | string | yes | Directory where generated Spec Kit commands are discoverable for this assistant. |
| `command_format` | string | yes | Output file format and argument placeholder semantics. |
| `install_url` | string/null | yes | Setup guidance URL when validation fails. |
| `requires_cli` | boolean | yes | Whether local tool validation is expected by default. |
| `officially_supported` | boolean | yes | Whether the assistant is part of the project’s official support set. |

**Validation Rules**:

- `key` is unique and stable across releases.
- `officially_supported=true` requires matching support claims in CLI help, README/docs, templates, and tests.
- `requires_cli=true` requires both a normal validation path and an explicit skip-validation path.

### 2. `CoreWorkspaceAsset`

Represents canonical Spec Kit files shared by all assistants.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `path` | string | yes | Workspace-relative canonical asset path under `.specify/` or root compatibility link. |
| `asset_category` | enum | yes | `memory`, `script`, `template`, `instruction`, `skill`, `tool`, or `spec`. |
| `source_template` | string/null | no | Template/package source when the asset is newly copied. |
| `initialized` | boolean | yes | Whether the asset already exists in the workspace. |
| `user_modified` | boolean/unknown | yes | Whether content differs from the default template or cannot be safely assumed pristine. |
| `preservation_policy` | enum | yes | `preserve`, `create-if-missing`, `link`, or `explicit-overwrite-only`. |

**Validation Rules**:

- Existing initialized assets are preserved by default.
- Missing required assets may be created from templates and reported.
- User-modified assets are never overwritten by adding another assistant.

### 3. `ToolSpecificAssetSet`

Represents files owned by one assistant integration.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `assistant_key` | string | yes | References `AssistantSupportProfile.key`. |
| `asset_paths` | array<string> | yes | Assistant-specific files/directories generated or inspected. |
| `canonical_sources` | array<string> | yes | Shared templates or instructions that generate these assets. |
| `coexistence_scope` | array<string> | yes | Other assistant roots that must not be changed by this asset set. |
| `refresh_policy` | enum | yes | `generate`, `refresh-derived`, `preserve-custom`, `warn-conflict`, or `skip`. |
| `coverage_status` | enum | yes | `complete`, `partial`, `missing`, or `excluded-with-reason`. |

**Validation Rules**:

- One assistant’s refresh does not delete or rewrite another assistant root.
- Generated command coverage matches canonical command templates unless an exclusion is documented.
- Assets derived from canonical instructions must reference or link to the canonical source where supported.

### 4. `InitializationOperation`

Represents a single initialization or refresh run.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `operation_id` | string | yes | Stable identifier for logs/tests within a run. |
| `project_mode` | enum | yes | `new-project` or `existing-workspace`. |
| `assistant_keys` | array<string> | yes | Assistants requested for setup or refresh. |
| `core_workspace_exists` | boolean | yes | Whether `.specify` existed before the run. |
| `ignore_agent_tools` | boolean | yes | Whether local assistant tool validation is skipped. |
| `force_overwrite` | boolean | yes | Whether user explicitly allowed overwrite/merge behavior. |
| `status` | enum | yes | `completed`, `completed-with-warnings`, `blocked`, or `failed`. |

**Validation Rules**:

- `existing-workspace` with `core_workspace_exists=true` defaults to preservation.
- `force_overwrite=false` blocks silent template replacement of core files.
- Re-running the same operation is idempotent for core assets.

### 5. `InitializationResultSummary`

Represents the user-visible outcome after initialization or refresh.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `created` | array<string> | yes | Assets newly created. |
| `reused` | array<string> | yes | Existing assets reused unchanged. |
| `skipped` | array<string> | yes | Assets intentionally not touched. |
| `preserved` | array<string> | yes | User-maintained assets protected from overwrite. |
| `conflicts` | array<string> | yes | Assets needing user resolution. |
| `attention_required` | array<string> | yes | Warnings such as missing local assistant tools. |
| `configured_assistants` | array<string> | yes | Assistant keys now configured in the workspace. |

**Validation Rules**:

- Every touched or intentionally skipped asset appears in exactly one appropriate category.
- Summaries distinguish project configuration from local tool availability.
- Conflict entries include enough information for the user to decide next action.

### 6. `SupportSurfaceAudit`

Represents a consistency check across release and user-facing support claims.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `surface_id` | string | yes | Stable audit identifier. |
| `surface_type` | enum | yes | `cli-help`, `documentation`, `template`, `script`, `package`, `test`, `generated-asset`, or `governance`. |
| `location` | string | yes | File path or output being audited. |
| `expected_assistants` | array<string> | yes | Official assistant keys expected on the surface. |
| `observed_assistants` | array<string> | yes | Assistant keys found on the surface. |
| `consistent` | boolean | yes | Whether observed support matches expected support. |
| `release_blocking` | boolean | yes | Whether failure blocks release readiness. |

**Validation Rules**:

- Official assistant support claims match the assistant matrix on release-blocking surfaces.
- Generated command coverage is checked for every official assistant.
- Audit failures identify the mismatched surface and missing or extra assistant key.

## Relationships

- `AssistantSupportProfile 1..* -> ToolSpecificAssetSet`
- `AssistantSupportProfile 1..* -> SupportSurfaceAudit`
- `CoreWorkspaceAsset 1..* -> ToolSpecificAssetSet` via `canonical_sources`
- `InitializationOperation 1..1 -> InitializationResultSummary`
- `InitializationOperation 1..* -> AssistantSupportProfile`
- `InitializationResultSummary 1..* -> CoreWorkspaceAsset`
- `InitializationResultSummary 1..* -> ToolSpecificAssetSet`

## State Transitions

### Core workspace asset

- `missing` → `created`
- `existing` → `reused`
- `existing-customized` → `preserved`
- `conflicting` → `attention-required`
- `explicitly-approved` → `merged-or-overwritten`

### Assistant asset coverage

- `not-configured` → `generated`
- `generated` → `refreshed-derived`
- `customized` → `preserved`
- `customized` → `conflict-reported`
- `obsolete` → `reported-for-user-action`

### Initialization operation

- `requested` → `validating`
- `validating` → `copying-missing-core`
- `copying-missing-core` → `generating-tool-assets`
- `generating-tool-assets` → `summarizing`
- `summarizing` → `completed`
- Any state → `blocked` when safe preservation cannot be guaranteed

### Support audit

- `pending` → `pass`
- `pending` → `fail`
- `fail` → `fixed`
- `fail` → `deferred-with-risk`

## Derived Rules

1. The official assistant list for this feature is: `copilot`, `claude`, `qwen`, `opencode`, and `qoder`.
2. `.specify` core assets are shared across assistants and must not be duplicated per assistant.
3. Tool-specific assets can be refreshed only within their assistant root unless explicitly updating canonical shared sources.
4. A repeat initialization with the same assistant must produce no duplicate core content.
5. Adding a new assistant to an existing project must preserve already configured assistant roots.
6. Any support-surface mismatch for CLI help, documentation, package resources, or canonical command coverage is release-blocking.
