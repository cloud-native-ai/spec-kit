# Data Model: Skill Install Layout

## Overview

[CN]“`.specify/skills/` [CN] + [CN]”[CN]

## Entities

### 1. SkillPrimaryCopy

**Purpose**: The sole master copy entity for project-level skills.

**Fields**:
- `skill_name`: canonical skill name (directory name)
- `root_path`: `.specify/skills/<skill-name>/`
- `skill_file_path`: `.specify/skills/<skill-name>/SKILL.md`
- `content_fingerprint`: [CN]
- `state`: `active` | `migrating` | `conflict`
- `updated_at`: ISO [CN]

**Validation Rules**:
- `root_path` [CN] `.specify/skills/` [CN]
- [CN] `skill_name` [CN] `active` [CN]
- `skill_file_path` [CN]

### 2. CompatibilityEntryPoint

**Purpose**: [CN]

**Fields**:
- `tool_key`: `github` [CN]
- `entry_path`: [CN] `.github/skills/<skill-name>`
- `target_primary_path`: [CN] `.specify/skills/<skill-name>/`
- `entry_mode`: `symlink` | `placeholder`
- `status`: `created` | `skipped` | `failed` | `conflict`
- `reason`: [CN]/[CN]

**Validation Rules**:
- `target_primary_path` [CN] `.specify/skills/` [CN]
- `entry_mode=placeholder` [CN] skill [CN]
- [CN]

### 3. ToolSupportProfile

**Purpose**: [CN]

**Fields**:
- `supported_tools`: [CN]
- `enabled_entry_roots`: [CN]
- `detected_at`: ISO [CN]

**Validation Rules**:
- [CN] Spec Kit [CN]
- [CN] `skipped`[CN]

### 4. BackupArtifact

**Purpose**: [CN]

**Fields**:
- `source_path`: [CN] `.github/skills/<skill-name>`[CN]
- `backup_path`: [CN]
- `status`: `created` | `failed`
- `message`: [CN]
- `created_at`: ISO [CN]

**Validation Rules**:
- [CN]
- `status=failed` [CN]

### 5. MigrationSession

**Purpose**: [CN]

**Fields**:
- `skill_name`: [CN] skill
- `legacy_path`: [CN] `.github/skills/<skill-name>`[CN]
- `primary_copy_path`: [CN]
- `backup`: [CN] `BackupArtifact`
- `delete_legacy_attempted`: [CN]
- `delete_legacy_status`: `deleted` | `skipped` | `failed`
- `session_state`: `completed` | `partial` | `manual-required`

**Validation Rules**:
- [CN]
- [CN]
- [CN] `session_state` [CN] `manual-required`

### 6. InstallOutcome

**Purpose**: [CN]/[CN]/[CN]

**Fields**:
- `operation`: `install` | `refresh` | `migrate`
- `skill_name`: [CN] skill
- `primary_copy_status`: `created` | `reused` | `failed`
- `entrypoints`: `CompatibilityEntryPoint[]`
- `migration`: [CN] `MigrationSession`
- `overall_status`: `success` | `partial-success` | `failed`
- `messages`: [CN]

**Validation Rules**:
- `overall_status=success` [CN]
- [CN] `partial-success`[CN]
- [CN]

## State Transitions

- `SkillPrimaryCopy`: `active` → `conflict`[CN]
- `CompatibilityEntryPoint`: `failed` → `created`[CN]
- `MigrationSession`: `partial` → `completed`[CN]
- `InstallOutcome`: `partial-success` → `success`[CN]

## Invariants

- `.specify/skills/` [CN] skill [CN]
- [CN]
- [CN]
- [CN]
- [CN]/[CN]
