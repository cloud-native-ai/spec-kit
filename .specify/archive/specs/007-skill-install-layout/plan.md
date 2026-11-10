# Implementation Plan: Skill Install Layout

**Branch**: `007-skill-install-layout` | **Date**: 2026-04-21 | **Spec**: [.specify/specs/007-skill-install-layout/requirements.md](.specify/specs/007-skill-install-layout/requirements.md)
**Input**: Specification from `.specify/specs/007-skill-install-layout/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

将项目级 skills 的主安装目录统一迁移为 `.specify/skills/`，并将 `.github/skills/` 与其他正式支持工具的目录降级为“兼容入口”。实现采用“单主副本 + 多入口链接/占位”的布局：优先创建软链接，无法链接时创建不复制内容的占位目录和指引文件，同时补齐旧版 `.github/skills/<name>` 真实目录迁移、冲突拦截、备份与幂等规则。

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Bash + Python 3.11+（项目安装文档），兼容项目声明 Python >=3.8  
**Primary Dependencies**: Typer、Rich、现有 `scripts/bash/*.sh` 与 `scripts/python/skills-utils.py` 机制  
**Storage**: 本地文件系统（`.specify/skills/` 主副本、工具兼容入口目录、迁移备份目录）  
**Testing**: pytest（`tests/contracts`、`tests/integration`、`tests/unit`）+ 脚本契约验证  
**Target Platform**: Linux/macOS/Windows 工作区文件系统（需处理软链接能力差异）
**Project Type**: single（CLI + templates + scripts + tests）  
**Performance Goals**: 单次 skill 安装/刷新流程在常见工作区中保持与当前同量级耗时（新增布局处理不引入显著额外等待）  
**Constraints**: `.specify/skills/` 必须是唯一主副本；兼容入口禁止复制技能内容；仅覆盖正式支持且目录约定明确的工具；冲突禁止静默覆盖  
**Scale/Scope**: 单仓库内数十级 skills 的安装、重复刷新、旧布局迁移与多工具兼容入口维护

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: 复用 Feature 013（Skills Command）承载本次迭代，不新增重复 Feature。  
- **Specification-Driven Development**: 设计决策直接映射 FR-001~FR-016 与成功标准 SC-001~SC-005。  
- **Intent-Driven Development**: 先约束“主副本位置与兼容入口语义”，再落实具体脚本实现细节。  
- **Test-First & Contract-Driven**: 先定义布局/迁移契约与验证路径，再拆任务进入实现。  
- **AI Agent Integration**: 仅面向已批准助手生态（Copilot/Qwen/opencode/Qoder）以及其已正式支持入口。  
- **Continuous Quality & Observability**: 设计保持最小化，所有失败场景都要求可见错误与迁移结果摘要。  
- **SDD Workflow Compliance**: 本次计划产物覆盖 plan + data model + contracts + quickstart，后续进入 `/speckit.tasks`。

**Additional Constraints from Input**:

- 用户明确要求从 `.github/skills/` 定制路径迁移到 `.specify/skills/` 通用目录。  
- 兼容入口需按“已支持工具”条件创建，不能无差别扩展到草稿/实验工具。  
- 软链接不可用时必须采用“占位目录 + 指引文件”降级策略，不复制内容。  
- 旧版真实目录迁移需先备份，备份失败时禁止删除旧目录。

**Gates Status**: ✅ All gates pass

## Project Structure

### Documentation (this spec)

```text
.specify/specs/007-skill-install-layout/
├── plan.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── skill-install-layout.openapi.yaml
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this spec. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
src/
└── specify_cli/
  └── __init__.py

scripts/
├── bash/
│   └── create-new-skill.sh
└── python/
  └── skills-utils.py

.specify/
├── scripts/
│   ├── bash/
│   │   └── create-new-skill.sh
│   └── python/
│       └── skills-utils.py
└── skills/
  └── <skill-name>/
      ├── SKILL.md
      └── ...

.github/
└── skills/
  └── <skill-name> -> compatibility entry to .specify/skills/<skill-name>

tests/
├── contracts/
├── integration/
└── unit/
```

**Structure Decision**: 保持单仓库结构，不新增子项目。变更集中在 `create-new-skill` 与 `skills-utils` 相关脚本、技能模板/文档、以及测试覆盖；路径策略从“工具目录写入主副本”重构为“.specify 主副本 + 工具兼容入口”。

## Complexity Tracking

N/A

## Phase 0: Research Review & Context

- 当前规格目录无 `research.md`；已通过 `requirements.md`、`.specify/memory/constitution.md`、`README.md`、`docs/*.md`、`.specify/memory/features.md` 与全部 `.specify/memory/features/*.md` 完成上下文收敛。  
- 已确认本次仅为 Feature 013 的新一轮需求迭代，不引入新 Feature，也不淘汰/合并既有 Feature。  
- 已确认与需求对应的关键边界：
  - `/speckit.*` 是对话命令，不在终端直接执行；
  - 支持工具范围严格受宪法与文档约束（已批准助手生态）；
  - 技能目录从工具耦合路径转向通用路径的需求合理且与既有 feature 演进一致。  
- 技术未知项已被澄清问答覆盖（软链接降级策略、旧目录迁移与备份失败处理、支持工具范围）。

## Phase 1: Design & Contracts

### Design Decisions

1. **统一主副本布局**
  - 项目级 skill 的唯一主副本目录为 `.specify/skills/<skill-name>/`。
  - 任意工具目录（如 `.github/skills/<skill-name>`）仅作为兼容入口，不再承载主内容写入。

2. **兼容入口创建策略**
  - 优先创建指向主副本的软链接。
  - 当环境不支持软链接或权限不足时，创建占位目录与指引文件，禁止复制 skill 内容。
  - 仅对“当前正式支持且目录约定明确”的工具入口执行创建逻辑。

3. **迁移与冲突处理策略**
  - 发现旧版 `.github/skills/<skill-name>` 真实目录时，迁移到主副本并尝试收敛为兼容入口。
  - 删除旧目录前强制备份；若备份失败，跳过删除并输出“需人工处理”。
  - 任何入口位点冲突（普通文件/目录/无效链接）均中止自动覆盖并返回明确错误。

4. **幂等与可观察性**
  - 重复安装/刷新同名 skill 时，最终状态始终收敛为一个主副本 + 若干兼容入口。
  - 输出结果必须包含主副本路径、入口创建结果、失败原因、迁移/备份信息。

### Data Model

- 生成 `.specify/specs/007-skill-install-layout/data-model.md`，定义 `SkillPrimaryCopy`、`CompatibilityEntryPoint`、`ToolSupportProfile`、`MigrationSession`、`BackupArtifact`、`InstallOutcome` 等实体及状态转移。

### Contracts

- 生成 `.specify/specs/007-skill-install-layout/contracts/skill-install-layout.openapi.yaml`。
- 契约覆盖安装、迁移、冲突检测、入口创建失败降级、幂等刷新等核心行为。

### Quickstart

- 生成 `.specify/specs/007-skill-install-layout/quickstart.md`，覆盖新安装、重复安装、旧布局迁移、软链接受限、冲突阻断等验收路径。

## Constitution Check (Post-Design Re-check)

- **Feature-Centric Development**: 继续绑定 Feature 013；无新增/淘汰/合并 Feature。  
- **Specification-Driven Development**: 设计内容与 FR-001~FR-016 一一对应，未引入越界需求。  
- **Intent-Driven Development**: 方案围绕“主副本统一 + 兼容入口”核心意图，没有扩展到个人级目录重构。  
- **Test-First & Contract-Driven**: 已先产出数据模型和接口契约，支持后续优先补齐契约与回归测试。  
- **AI Agent Integration**: 仅处理官方支持助手相关路径，不扩展未支持 provider。  
- **Continuous Quality & Observability**: 失败与降级路径均可观察并有用户提示，保持最小必要复杂度。  
- **SDD Workflow Compliance**: plan 阶段产物完整，满足进入 `/speckit.tasks` 的前置条件。

**Post-Design Gates Status**: ✅ All gates pass

## Phase 2: Implementation Planning

1. 调整 `scripts/bash/create-new-skill.sh` 与 `.specify/scripts/bash/create-new-skill.sh`：主写入目录改为 `.specify/skills`，并输出兼容入口创建结果。  
2. 调整 `scripts/python/skills-utils.py` 与 `.specify/scripts/python/skills-utils.py`：skill 类型推断与发现优先支持 `.specify/skills/*/SKILL.md`，保留旧路径迁移兼容。  
3. 更新技能模板与文档描述，将 `.specify/skills` 定义为主目录，将 `.github/skills` 明确为兼容入口。  
4. 实现旧版 `.github/skills` 真实目录迁移流程（备份、删除条件、失败降级、冲突提示）。  
5. 为安装/迁移/冲突/降级/幂等路径补齐 contract、integration、unit 测试，并同步更新 Feature 013 关联说明。
