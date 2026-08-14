# Data Model: Deterministic Tool and Skill IDs

## Overview

This data model defines the canonical identification layer added to reusable tool and skill artifacts so that later commands, documents, and conversations can resolve them deterministically.

## Entities

### 1. ResourceId

**Purpose**: Canonical identifier used to uniquely locate one reusable artifact inside the workspace.

**Fields**:
- `id`: Workspace-relative canonical path string
- `resource_type`: `tool` or `skill`
- `canonical_path`: Normalized workspace-relative path used for persistence and display
- `display_label`: Human-readable summary shown alongside the identifier
- `status`: `active`, `stale`, `invalid`, or `conflict`
- `generated_at`: ISO timestamp for when the identifier was generated or refreshed

**Validation Rules**:
- `id` MUST equal the canonical workspace-relative path
- `resource_type` MUST match the resolved artifact type
- `canonical_path` MUST stay within the workspace root
- Two active artifacts MUST NOT share the same `id`

**State Transitions**:
- `active` → `stale` when the referenced artifact is moved, renamed, or deleted
- `stale` → `active` when the artifact is re-saved and a valid canonical path is restored
- `active` → `conflict` when multiple candidates are mapped to the same identifier representation
- Any state → `invalid` when the path is out-of-scope or type validation fails

### 2. ToolArtifact

**Purpose**: Persisted tool record managed by `/speckit.tools`.

**Fields**:
- `tool_name`: Stable record name
- `tool_type`: One of `mcp-call`, `project-script`, `system-binary`, `shell-function`
- `record_path`: Workspace-relative path to the ToolRecord markdown file
- `resource_id`: Associated `ResourceId`
- `source_identifier`: Native source locator for the underlying tool
- `aliases`: Optional alternative user-facing names
- `record_status`: `complete`, `incomplete`, or `verified`

**Relationships**:
- Owns exactly one active `ResourceId`
- May be referenced by many `ResolutionRequest` items over time

### 3. SkillArtifact

**Purpose**: Persisted skill asset managed by `/speckit.skills`.

**Fields**:
- `skill_name`: Stable skill name
- `skill_root_path`: Workspace-relative root directory path for the skill
- `skill_file_path`: Workspace-relative path to `SKILL.md`
- `resource_id`: Associated `ResourceId`
- `description`: Trigger-oriented summary for discovery
- `artifact_status`: `active`, `refreshed`, or `stale`

**Relationships**:
- Owns exactly one active `ResourceId`
- May be referenced by many `ResolutionRequest` items over time

### 4. ResolutionRequest

**Purpose**: User or workflow attempt to resolve a tool or skill.

**Fields**:
- `requested_id`: Optional canonical ID provided by the user
- `requested_text`: Optional natural-language description provided by the user
- `expected_type`: Optional `tool` or `skill`
- `origin`: `command`, `document`, or `conversation`
- `requested_at`: ISO timestamp

**Validation Rules**:
- At least one of `requested_id` or `requested_text` MUST be present
- If `expected_type` is present, resolved artifact type MUST match it

### 5. ResolutionResult

**Purpose**: Output of the artifact resolution flow.

**Fields**:
- `result_type`: `resolved`, `fallback`, `conflict`, or `error`
- `resolved_id`: Canonical ID when resolution succeeds
- `resolved_path`: Canonical workspace-relative path when resolution succeeds
- `resolved_type`: `tool` or `skill` when resolution succeeds
- `message`: User-facing explanation
- `fallback_used`: Boolean indicating whether natural-language fallback was used

## Invariants

- Canonical IDs are scoped to the current workspace
- Canonical IDs are deterministic for a given persisted artifact location
- Resolution by valid ID takes precedence over fuzzy discovery
- Natural-language discovery remains available when ID-based resolution is absent or invalid
- Conflicts never auto-resolve silently; they require an explicit user-visible stop or confirmation path
