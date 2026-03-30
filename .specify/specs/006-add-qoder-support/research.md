# Research: Add Qoder Support

## Context Summary

本次需求需要把 Qoder 从“仓库中已有部分兼容痕迹”提升为“治理、初始化、刷新、文档与发布均正式承认的一等助手”。研究基于 `README.md`、`docs/**`、`.specify/memory/**`、`src/specify_cli/__init__.py`、`scripts/bash/generate-instructions.sh` 与 `tmp/patches/qoder-main/` 完成。

## Key Findings

### 1. Current assistant architecture is matrix-driven

- CLI 助手定义集中在 `src/specify_cli/__init__.py` 的 `AGENT_CONFIG`。
- 初始化主路径通过 `copy_local_templates()` + `generate_commands()` 为不同助手分发命令资产。
- 当前正式支持的 CLI/IDE 助手只有 `copilot`、`qwen`、`opencode`。
- `scripts/bash/generate-instructions.sh` 已经会创建 `.qoder/project_rules.md`，说明仓库存在 Qoder 兼容预埋，但未完成正式接入。

### 2. Governance and public docs are currently inconsistent with Qoder support

- `.specify/memory/constitution.md` 的批准助手白名单仍只包含 GitHub Copilot、Qwen Code、opencode。
- `README.md` 与 `docs/installation.md` 的支持助手列表未包含 Qoder。
- `templates/plan-template.md` 与 `templates/commands/agents.md` 也硬编码了旧白名单。
- 因此若只改 CLI，会违反 FR-012/FR-013。

### 3. Upstream patch provides a low-risk implementation reference

从 `tmp/patches/qoder-main/non-merge/0001-feat-support-Qoder-CLI.patch` 可提炼的接入事实：

- 助手 key：`qoder`
- 展示名称：`Qoder CLI`
- CLI 命令：`qoder`
- 安装地址：`https://qoder.com/cli`
- 命令目录：`.qoder/commands/`
- 命令文件格式：Markdown
- 说明/上下文文件：`QODER.md` 或 `.qoder/project_rules.md` 属于上游生态常见兼容面

本仓库不需要照搬上游的多助手扩展，只需吸收 Qoder 的最小接入模式，并适配当前精简支持矩阵。

### 4. Existing refresh behavior constrains implementation strategy

- 需求要求支持现有目录初始化和后续刷新。
- 当前仓库对说明同步依赖 `generate-instructions.sh`，对命令资产依赖模板生成。
- 因此实现应以“增量补齐 Qoder 资产”而非“重建整个助手目录”为主，避免误伤其他助手文件。

## Decisions

### Decision 1: Treat Qoder as a CLI-based first-class assistant

**Decision**: Qoder 采用与 `qwen`、`opencode` 相同的 CLI 型助手路径。

**Why**:
- 满足 FR-001、FR-004、FR-005、FR-011。
- 与现有 `AGENT_CONFIG` 结构一致，改动最小。
- 上游补丁已验证该接入方式可行。

### Decision 2: Use `.qoder/commands/` as the generated command directory

**Decision**: 初始化与刷新时，Qoder 命令文件输出到 `.qoder/commands/`。

**Why**:
- 与上游补丁一致。
- 与本仓库已存在的 `.qoder/project_rules.md` 兼容目录保持一致。
- 满足 FR-002、FR-006、FR-007。

### Decision 3: Make governance alignment part of the feature, not a follow-up

**Decision**: 同一 feature 中同步更新宪法白名单、Feature 记录、README、安装文档、帮助文本与模板白名单。

**Why**:
- 需求澄清已要求 Qoder 成为正式批准助手。
- 若延后治理更新，会直接违反 FR-012、FR-013。

### Decision 4: Model support consistency as a releasable contract

**Decision**: 在 `contracts/qoder-support.openapi.yaml` 中显式建模初始化、CLI 校验、刷新与支持面审计行为。

**Why**:
- 有助于将 FR-012 的“一致性要求”转为可执行的 tasks/test cases。
- 让发布审计不只依赖人工对照文档。

## Drift and Risks

### Known drift

- README 指向的部分文档（如升级指南）当前不存在。
- Qoder 目录兼容脚本已存在，但 README/安装文档/宪法未同步。
- 不同文档对 Qwen/opencode 的链接也存在不一致，说明支持面审计应覆盖所有助手命名与链接，而不只覆盖 Qoder。

### Risks to control in implementation

1. **治理先后顺序错误**：先改 CLI、后改宪法会让计划阶段产生暂时违规状态。
2. **帮助文案遗漏**：`--ai` 帮助、错误提示、`check()` 输出若遗漏 Qoder，会造成用户可见不一致。
3. **现有目录覆盖风险**：刷新逻辑若重建目录而非增量补齐，可能破坏其他助手配置。
4. **发布资源遗漏**：模板或脚本改了但 wheel/发布产物未包含，会导致 SC-004 失败。

## Recommended Implementation Order

1. 更新治理与共享模板白名单。
2. 更新 CLI 助手矩阵与初始化/校验逻辑。
3. 更新说明刷新与命令生成输出目录。
4. 更新 README、安装文档、使用文档和帮助文本。
5. 增加合同测试、集成测试和发布审计检查。

## Research Outcome

当前没有阻塞性未知项，`/speckit.plan` 可以直接进入 Phase 1/2；无需额外执行 `/speckit.research`。