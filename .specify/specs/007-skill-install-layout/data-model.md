# Data Model: Skill Install Layout

## Overview

本数据模型定义“`.specify/skills/` 为唯一主副本 + 多工具兼容入口”的安装布局与迁移行为，覆盖新安装、重复刷新、旧版目录迁移、冲突处理和软链接降级场景。

## Entities

### 1. SkillPrimaryCopy

**Purpose**: 项目级 skill 的唯一主副本实体。

**Fields**:
- `skill_name`: skill 规范名称（目录名）
- `root_path`: `.specify/skills/<skill-name>/`
- `skill_file_path`: `.specify/skills/<skill-name>/SKILL.md`
- `content_fingerprint`: 可选内容摘要（用于冲突识别）
- `state`: `active` | `migrating` | `conflict`
- `updated_at`: ISO 时间戳

**Validation Rules**:
- `root_path` 必须在工作区内且位于 `.specify/skills/` 前缀下
- 同一 `skill_name` 在同一工作区最多一个 `active` 主副本
- `skill_file_path` 必须存在或由安装流程创建

### 2. CompatibilityEntryPoint

**Purpose**: 面向某个已支持工具暴露的兼容入口。

**Fields**:
- `tool_key`: `github` 或其他正式支持工具标识
- `entry_path`: 例如 `.github/skills/<skill-name>`
- `target_primary_path`: 指向 `.specify/skills/<skill-name>/`
- `entry_mode`: `symlink` | `placeholder`
- `status`: `created` | `skipped` | `failed` | `conflict`
- `reason`: 失败/跳过原因

**Validation Rules**:
- `target_primary_path` 必须存在并落在 `.specify/skills/` 下
- `entry_mode=placeholder` 时必须存在指引文件且不得复制 skill 主内容
- 冲突状态下不得覆盖已有普通文件或目录

### 3. ToolSupportProfile

**Purpose**: 当前工作区已启用且正式支持的工具入口画像。

**Fields**:
- `supported_tools`: 工具集合（仅正式支持范围）
- `enabled_entry_roots`: 每个工具可用的技能入口根路径
- `detected_at`: ISO 时间戳

**Validation Rules**:
- 仅包含 Spec Kit 当前正式支持且技能目录约定明确的工具
- 未启用工具不会触发兼容入口创建失败（应标记 `skipped`）

### 4. BackupArtifact

**Purpose**: 迁移删除前生成的旧目录备份记录。

**Fields**:
- `source_path`: 旧目录路径（如 `.github/skills/<skill-name>`）
- `backup_path`: 备份输出路径
- `status`: `created` | `failed`
- `message`: 备份结果说明
- `created_at`: ISO 时间戳

**Validation Rules**:
- 仅在需要删除旧真实目录时创建备份记录
- `status=failed` 时迁移流程必须跳过删除旧目录

### 5. MigrationSession

**Purpose**: 单次旧布局迁移会话。

**Fields**:
- `skill_name`: 迁移目标 skill
- `legacy_path`: 旧布局路径（通常 `.github/skills/<skill-name>`）
- `primary_copy_path`: 新主副本路径
- `backup`: 关联 `BackupArtifact`
- `delete_legacy_attempted`: 是否尝试删除旧目录
- `delete_legacy_status`: `deleted` | `skipped` | `failed`
- `session_state`: `completed` | `partial` | `manual-required`

**Validation Rules**:
- 迁移前必须完成主副本落盘
- 仅当备份成功且无冲突时允许删除旧目录
- 备份失败时 `session_state` 必须为 `manual-required`

### 6. InstallOutcome

**Purpose**: 单次安装/刷新/迁移执行结果摘要。

**Fields**:
- `operation`: `install` | `refresh` | `migrate`
- `skill_name`: 目标 skill
- `primary_copy_status`: `created` | `reused` | `failed`
- `entrypoints`: `CompatibilityEntryPoint[]`
- `migration`: 可选 `MigrationSession`
- `overall_status`: `success` | `partial-success` | `failed`
- `messages`: 用户可见提示列表

**Validation Rules**:
- `overall_status=success` 必须满足主副本可用
- 入口部分失败时允许 `partial-success`，但必须含明确失败原因
- 所有路径必须可追溯到同一主副本

## State Transitions

- `SkillPrimaryCopy`: `active` → `conflict`（同名内容冲突）
- `CompatibilityEntryPoint`: `failed` → `created`（后续重试成功）
- `MigrationSession`: `partial` → `completed`（人工修复后再次运行）
- `InstallOutcome`: `partial-success` → `success`（入口补齐后）

## Invariants

- `.specify/skills/` 是项目级 skill 内容唯一主副本来源
- 任意兼容入口都必须映射到同一主副本
- 软链接失败时采用占位目录策略，且不复制主内容
- 迁移删除旧目录前必须先备份；备份失败必须阻断删除
- 重复安装/刷新最终收敛到同一主副本与一致入口布局
