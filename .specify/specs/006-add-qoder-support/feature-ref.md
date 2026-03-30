# Feature References: Add Qoder Support

## Primary Feature

### Feature 020 — Qoder Support

- **Role in this plan**: 本次需求的唯一主 Feature。
- **Why primary**: 所有用户价值都围绕“把 Qoder 作为正式受支持助手”展开。
- **Plan impact**: 需要同时覆盖初始化、刷新、校验、文档、分发与治理一致性。

## Related Existing Features

### Feature 008 — Instructions Command

- **Relationship**: Qoder 需要出现在说明生成与兼容链接刷新链路中。
- **Shared assets**:
  - `scripts/bash/generate-instructions.sh`
  - `templates/instructions-template.md`
  - `.ai/instructions.md`

### Feature 015 — CLI Interface

- **Relationship**: `specify init --ai qoder`、错误提示、工具检查与 `check()` 输出都属于 CLI 交互面。
- **Shared assets**:
  - `src/specify_cli/__init__.py`

### Feature 017 — Template Engine

- **Relationship**: Qoder 命令资产需要复用现有模板生成体系，而不是单独维护一套命令文件。
- **Shared assets**:
  - `templates/commands/*.md`
  - `generate_commands()` 调用路径

### Feature 019 — Agents Command

- **Relationship**: 现有模板与治理文案中存在批准助手白名单硬编码，Qoder 纳入后要同步修正共享支持面。
- **Shared assets**:
  - `templates/commands/agents.md`
  - `templates/plan-template.md`

## Feature Review Outcome

- **New feature required?** No
- **Feature merge/split required?** No
- **Feature deprecation required?** No
- **Feature classification change required?** No

## Notes for `/speckit.tasks`

1. 将治理/白名单更新作为先行任务，而不是文档善后任务。
2. 将 CLI 初始化与校验逻辑拆为独立任务，避免与文档改动混杂。
3. 将支持面一致性审计与发布物检查单独建任务，确保 FR-012/FR-013 有明确验收出口。