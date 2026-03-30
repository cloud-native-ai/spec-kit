# Implementation Plan: Add Qoder Support

**Branch**: `006-add-qoder-support` | **Date**: 2026-03-29 | **Spec**: [.specify/specs/006-add-qoder-support/requirements.md](.specify/specs/006-add-qoder-support/requirements.md)
**Input**: Specification from `.specify/specs/006-add-qoder-support/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

为 Spec Kit 增加 Qoder 一等支持，使其在 `specify init`、现有目录初始化、依赖校验、说明刷新、文档展示和发布分发中与当前已支持助手保持同等体验。技术路径复用现有助手矩阵与命令模板生成机制，以 `tmp/patches/qoder-main/` 中的上游补丁作为低风险参考，同时先完成治理白名单与 Feature 记录对齐，避免“代码支持了但制度/文档仍不承认”的漂移。

## Technical Context

**Language/Version**: Python >=3.8（项目声明），按文档与运行环境优先兼容 Python 3.11+  
**Primary Dependencies**: Typer、Rich、httpx[socks]、readchar、现有 Bash 脚本与 Markdown 模板体系  
**Storage**: 本地文件系统中的模板、说明、特性记忆与生成产物（`.specify/`、`.github/`、`.qoder/` 等）  
**Testing**: pytest（`tests/contract`、`tests/integration`、`tests/unit`）+ 计划产物驱动的文档/分发审计  
**Target Platform**: Linux/macOS/Windows 上的 CLI 初始化流程；当前仓库以 Linux 开发环境为主
**Project Type**: single（单仓库 Python CLI + 模板 + 脚本 + 文档）  
**Performance Goals**: 新增 Qoder 后，初始化与刷新流程应保持现有助手同量级开销；标准发布打包一次性产出包含 Qoder 的模板变体；文档/帮助/分发审计在一次候选发布检查中完成  
**Constraints**: 必须保留 Copilot/Qwen/opencode 现有行为；Qoder 必须复用 `--ignore-agent-tools`；刷新 Qoder 资产不得覆盖其他助手资产；治理白名单、文档、模板、脚本、打包输出必须同步；以上游补丁为参考但以当前需求与宪法为准  
**Scale/Scope**: 影响 1 个 CLI 入口、1 套命令模板系统、若干说明/文档/脚本/发布清单，以及 Feature 020 的治理闭环

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance**:

- **Feature-Centric Development**: 继续绑定 Feature 020，不新增重复 Feature；同时复核 Feature 008、015、017、019 的交叉影响。
- **Specification-Driven Development**: 设计直接追踪 FR-001~FR-013 与 SC-001~SC-005，避免把上游 patch 机械照搬为需求。
- **Intent-Driven Development**: 先解决“Qoder 在哪些用户旅程必须等价可用”，再映射到 CLI、模板、脚本和文档改动。
- **Test-First & Contract-Driven**: 先定义助手矩阵、初始化/刷新/校验/审计契约，再在 tasks/implement 阶段落具体测试。
- **AI Agent Integration**: 当前宪法白名单尚未包含 Qoder；本次 feature 范围明确要求先完成治理扩展，再落地代码与分发支持。
- **Continuous Quality & Observability**: 将不一致支持视为发布阻塞缺陷，要求帮助文本、README、安装文档、说明生成与发布清单统一审计。
- **SDD Workflow Compliance**: 已完成 requirements 与 checklist，当前 plan 将输出研究结论、数据模型、合同、快速验证与 feature 关联设计。

**Additional Constraints from Specification Context**:

- 需求已明确将 `tmp/patches/qoder-main/` 作为核心实现参考来源，但不替代当前仓库治理规则。
- 需求澄清已确认：Qoder 必须成为正式批准的受支持助手，而不仅是实验性兼容目录。
- 发布前任何支持面不一致都按 FR-012 视为阻塞问题，而不是文档瑕疵。

**Gates Status**: ✅ All gates pass（前提是实现阶段首先修改宪法/白名单/文档治理，再推进代码与分发支持）

## Project Structure

### Documentation (this spec)

```text
.specify/specs/006-add-qoder-support/
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── qoder-support.openapi.yaml
├── feature-ref.md
├── checklists/
│   └── requirements.md
└── tasks.md
```

### Source Code (repository root)

```text
src/
└── specify_cli/
  └── __init__.py

templates/
├── plan-template.md
├── instructions-template.md
└── commands/
  ├── agents.md
  ├── instructions.md
  └── *.md

scripts/
└── bash/
  ├── generate-instructions.sh
  └── *.sh

docs/
├── installation.md
├── quickstart.md
├── usage.md
├── upstream.md
├── skills/
└── speckit/

.specify/
├── memory/
│   ├── constitution.md
│   ├── features.md
│   └── features/020.md
└── specs/
  └── 006-add-qoder-support/

tmp/
└── patches/
  └── qoder-main/

tests/
├── contract/
├── integration/
└── unit/
```

**Structure Decision**: 保持现有单仓库 CLI 结构，不引入新子项目。改动集中在 `src/specify_cli/__init__.py` 的助手配置与初始化逻辑、`templates/` 的命令/计划模板、`scripts/bash/generate-instructions.sh` 的说明刷新、`docs/` 的用户可见支持面、`.specify/memory/` 的治理记录，以及后续补充的测试与发布审计。

## Complexity Tracking

N/A

## Phase 0: Research Review & Context

- 当前 spec 目录不存在 `research.md`；本次已通过阅读 `README.md`、`docs/**`、`.specify/memory/features.md`、`.specify/memory/features/*.md`、`.specify/memory/constitution.md` 与 `tmp/patches/qoder-main/` 完成研究收敛。
- 已确认项目是以 `src/specify_cli/__init__.py` 为主入口的 Python CLI，助手能力通过 `AGENT_CONFIG`、`copy_local_templates()` 与 `generate_commands()` 实现分发。
- 已确认仓库已有 `.qoder/project_rules.md` 兼容链接生成逻辑，但公开文档、CLI 帮助、宪法白名单、模板治理文本仍未正式纳入 Qoder，存在显著漂移。
- 已从上游补丁中提炼出最小可信接入模式：CLI 命令为 `qoder`、安装地址为 `https://qoder.com/cli`、命令资产目录为 `.qoder/commands/`、命令文件格式为 Markdown、参数占位符可沿用 `$ARGUMENTS`。
- Feature 复核结果：本次不新增/合并/淘汰 Feature，继续推进 Feature 020；但会触达 Feature 008（Instructions）、015（CLI Interface）、017（Template Engine）、019（Agents Command）对应的共享资产。
- 技术未知项已消除，无需额外中止并回退到 `/speckit.research`。

**Phase 0 Output**: 已生成 `research.md`，固化文档漂移、治理差距、上游补丁映射与计划决策依据。

## Phase 1: Design & Contracts

### Design Decisions

1. **助手矩阵扩展而非分支特判堆叠**
   - 在现有 `AGENT_CONFIG` 与命令生成分发逻辑中新增 `qoder` 条目。
   - Qoder 采用与 Qwen/opencode 相同的 CLI 型助手处理路径：可选 CLI 检查、允许 `--ignore-agent-tools` 绕过、初始化时生成专属命令目录。

2. **Qoder 资产集最小定义**
   - 初始化或刷新后，Qoder 资产集至少包含：`.qoder/commands/*` 命令文件、`.qoder/project_rules.md` 兼容说明链接，以及所有列出支持助手的帮助/文档面中的一致命名与安装指引。
   - 对现有目录初始化采取“补齐缺失/过期 Qoder 资产，不碰其他助手目录”的增量策略。

3. **治理与公开支持面同步落地**
   - 宪法批准助手白名单、README、安装文档、说明模板、计划模板、相关命令模板必须同步加入 Qoder。
   - 任何仅修改 CLI 但未更新治理/文档/发布清单的实现都不满足 FR-012/FR-013。

4. **分发与发布审计前置建模**
   - 将“支持助手矩阵”“初始化输出清单”“公开支持面清单”抽象为合同与数据模型，供 tasks/implement 阶段生成测试与发布校验。
   - 发布物必须覆盖所有声称支持的 CLI 型助手模板变体，避免 wheel/模板包缺项。

### Planned Design Artifacts

- `data-model.md`: 定义 `SupportedAssistant`、`AssistantAssetSet`、`AssistantValidationRule`、`SupportSurface`、`DistributionVariant` 等实体与状态转换。
- `contracts/qoder-support.openapi.yaml`: 以 OpenAPI 风格定义初始化、校验、刷新、支持面审计等行为合同。
- `quickstart.md`: 提供新项目、现有目录、缺少 CLI、忽略校验、刷新说明与发布审计的验证路径。
- `feature-ref.md`: 记录 Feature 020 与相关共享 Feature/文件的影响边界，便于 `/speckit.tasks` 拆分。

## Constitution Check (Post-Design Re-check)

- **Feature-Centric Development**: 仍然只推进 Feature 020，且已记录对共享 Feature 资产的触达范围。
- **Specification-Driven Development**: 设计产物逐项覆盖初始化、刷新、校验、文档、分发、治理要求。
- **Intent-Driven Development**: 设计围绕“把 Qoder 作为正式受支持助手”展开，没有扩展到新的助手框架重构。
- **Test-First & Contract-Driven**: 已先输出研究结论、数据模型、OpenAPI 合同与快速验证脚本思路，便于后续先补测试/审计。
- **AI Agent Integration**: 通过将宪法与模板白名单纳入同一 feature 范围，消除了“新增助手违反现行治理”的初始冲突。
- **Continuous Quality & Observability**: 文档/帮助/分发一致性被建模为显式审计对象，可在实现阶段转为自动检查。
- **SDD Workflow Compliance**: plan 阶段所需设计产物完整，可直接进入 `/speckit.tasks`。

**Post-Design Gates Status**: ✅ All gates pass

## Phase 2: Implementation Planning

1. 更新 `.specify/memory/constitution.md`、相关模板和公开文档中的批准助手列表，将 Qoder 纳入正式支持范围。
2. 更新 `src/specify_cli/__init__.py` 中的 `AGENT_CONFIG`、`--ai` 帮助文案、CLI 检查、初始化命令生成分支与 `check()` 输出，确保 Qoder 行为与其他 CLI 型助手一致。
3. 将 Qoder 命令资产纳入模板生成与刷新链路，覆盖新项目初始化、现有目录初始化和 `.qoder/project_rules.md` 说明同步。
4. 更新 `templates/commands/*.md`、`templates/plan-template.md`、`templates/instructions-template.md` 等共享模板，消除硬编码的三助手白名单。
5. 更新 `README.md`、`docs/installation.md`、`docs/usage.md` 及其他列出支持助手的文档，使命名、安装链接和示例保持一致。
6. 审核打包/发布相关脚本与资源清单，确保所有应包含 CLI 型助手变体的发布产物覆盖 Qoder。
7. 为助手矩阵、CLI 校验提示、初始化输出、现有目录刷新与支持面一致性补充 contract/integration/unit 测试。
8. 在实现完成后复核 Feature 020 的状态、关键变化与相关文件列表，确保 Feature Memory 与交付物一致。
