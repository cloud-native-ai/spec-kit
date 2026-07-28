# Implementation Plan: /speckit.docs 文档规范与管理命令

**Branch**: `033-docs-command` | **Date**: 2026-07-28 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `033-docs-command` → Feature 037 Docs Command
**Input**: Specification from `.specify/specs/033-docs-command/requirements.md`

## Summary

新增 `/speckit.docs` 聊天命令（第 19 个命令模板），按 `shared/patterns/reconcile-pattern.md` 实现为单一调谐引擎，管理文档空间（大写特殊名根目录薄层 + 六类 taxonomy `docs/` 厚层 + notes 生命周期临时区）。技术路径完全复用既有命令precedent：`templates/commands/docs.md` 源模板 + `regen-command-copies.py` 分发（零 CLI 源码改动）+ `scripts/python/docs-utils.py` 确定性引擎（`--action` JSON 模式，仿 history-utils.py）+ `shared/workflow/docs-step.md` 文档同步步骤约定（仿 feedback-step.md，注入核心命令模板）+ `docs/commands/docs.md` 参考文档。实现后对 Spec Kit 自身执行激进重组基调的 dogfooding 调谐（FR-008）。

## Clarifications

（需求层澄清见 requirements.md `## Clarifications`；本计划无新增未决项。）

## Technical Context

**Language/Version**: Python >= 3.8（引擎脚本 docs-utils.py，标准库-only，与 feedback-utils.py/history-utils.py 一致）；Markdown 提示模板（命令本体为 prompt 指令，非运行时代码）  
**Primary Dependencies**: 无新增第三方依赖（引擎脚本仅标准库：argparse/json/pathlib/datetime/re）；命令分发复用 `scripts/python/regen-command-copies.py` 与 `generate_commands()` 的 glob 机制  
**Storage**: 文件系统——管理区 = 项目根入口文件 + `docs/`（含 `docs/archive/` 归档区）；运行产物 = `.specify/docs/`（命令工作区：干跑计划、审计日志）；notes frontmatter = YAML 头（sed/regex 可解析的扁平键值）  
**Testing**: pytest（`contract` marker 钉模板结构/镜像一致性/共享字符串，`integration` marker 走样例夹具生命周期演练）；基线纪律：先跑全量记录基线（历史存在 ~106F/13E 的既有失败）再动手  
**Target Platform**: 开发者本地（Linux/macOS shell + 8 个受支持 AI 工具的聊天环境）
**Project Type**: 模板/提示框架（template-only feature per constitution VII gate）——命令 = prompt 模板；确定性能力 = 独立 Python 脚本  
**Performance Goals**: N/A（交互式提示流；docs-utils.py 扫描量级为数百文件，无性能敏感点）  
**Constraints**: 零新增循环机器（FR-009/FR-011e，contract 钉死 feedback 引擎动作集不变）；文档同步步骤为轻量增量评估、不阻断收尾（FR-011b/d）；正式区只归档不删除；`create-new-plan.sh` 不得在修订时重跑（覆写风险）  
**Scale/Scope**: 1 个新命令模板 ×（1 源 + 1 `.specify` 镜像 + 8 工具运行时副本）；1 个新引擎脚本 ×2 镜像；1 个新 shared 约定文档 ×2 镜像；13 个复杂命令模板注入文档同步步骤（×各自镜像/副本）；1 篇命令参考文档；≥3 个测试文件新增/修改；1 次 dogfooding 全量调谐（docs/ 现有 18 文件 + 7 子目录激进重组）

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.6.0):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 本计划全部技术决策回溯 requirements.md FR-001…011（各节标注 FR 编号） |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 037（feature-ref.md）；features.md 于本阶段推进 Draft → Planned |
| III | Intent-Driven Development | ✅ Pass | 先有两份设计笔记 + reconcile 模式协议，spec 蒸馏 WHAT/WHY，本计划才落 HOW |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | Template-only feature：无运行时代码的部分以模板内容/路径/结构契约测试代替；docs-utils.py 为纯脚本，MUST 有先行契约/单元测试 |
| V | AI Agent Integration Standards | ✅ Pass | 分发复用 `generate_commands()` glob 与 `regen-command-copies.py`，8 工具全覆盖，零新增工具假设 |
| VI | Continuous Quality & Observability | ✅ Pass | 审计日志/残差报告为强制产物（FR-003）；docs-utils.py 输出结构化 JSON；语义化版本随 CLI |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本次即该工作流；Pre-Status-Flip Gate 与 deferred 纪律由 tasks/implement 阶段承接 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 探索阶段以 src/specify_cli/generate_commands()、regen-command-copies.py 实际行为为准（确认零 CLI 源码改动），未信文档推测 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 命令 = prompt 指令 + 确定性辅助脚本；无运行时平台/调度器；CI 集成显式列为范围外（spec Assumptions） |
| X | Documentation Naming & Location Conventions | ✅ Pass | FR-010 将本原则的 ALL-CAPS 保留名规则上升为引擎校验维度；新文件全部 kebab-case（docs-utils.py、docs-step.md、docs.md） |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本功能经自身 SDD 工作流开发；FR-008 dogfooding 调谐 + FR-009 feedback 步骤；零新增循环机器 |

**Gates Status**: ✅ All gates pass（IV 为 constitution VII 明文允许的 template-only Partial，已豁免登记于 Complexity Tracking）

**Re-check after Phase 1**: 2026-07-28 — 设计产物（data-model.md、contracts/、quickstart.md）生成后复检：契约文件为声明式规范、quickstart 命令示例经真实执行校验、无新增违规项；结论不变（IV Partial 豁免维持）。

## Phase 0: Research Review

No standalone research.md — findings inlined below (internal investigation only).

**探索结论（代码为准，Principle VIII）**：

1. **命令分发零源码改动**：`src/specify_cli/__init__.py` 的 `generate_commands()` glob `templates/commands/*.md`，无硬编码命令清单；打包经 pyproject `force-include`。新增 `templates/commands/docs.md` 后仅需跑 `python3 scripts/python/regen-command-copies.py` 生成 `.specify/templates/commands/` 镜像 + 各工具运行时副本（frontmatter 剥离、`{SCRIPT}` 替换、`shared/` → `.specify/shared/` 路径重写）。
2. **命令模板结构**（以 `templates/commands/history.md` 为准）：frontmatter（`description`、`handoffs`、`scripts.sh`）+ `## User Input`（User Input Protocol 引用）+ `## Outline` + `## Feedback`（feedback-step.md 约定）+ `## Handoffs`。
3. **引擎脚本 precedent**：`scripts/python/history-utils.py` / `feedback-utils.py`——canonical 在 `scripts/python/`，镜像在 `.specify/scripts/python/`；单一 argparse `--action choices=[...]`，stdout 输出单个 JSON 对象。
4. **测试钉点**：`tests/contract/test_feedback_command_classification.py` 硬编码 `COMPLEX_COMMANDS`（13）/`SIMPLE_COMMANDS`（4）清单与计数——docs 须加入 COMPLEX 并更新计数（13→14）；`test_shared_reference_rewrite.py` 要求源模板用根相对 `shared/...` 引用；glob 型测试（`test_ai_tools_command_coverage.py` 等）自适应无需改。
5. **现状**：根目录无 `ARCHITECTURE.md`/`CONTRIBUTING.md`（bootstrap 将创建）；无任何 docs 生命周期工具；`shared/patterns/reconcile-pattern.md` 已存在双镜像；`docs/` 现有 18 文件 + 7 子目录（agents/assets/cli/commands/history/notes/skills/summary/teams…）待激进重组。
6. **文档同步步骤载体**：仿 `shared/workflow/feedback-step.md` 新建 `shared/workflow/docs-step.md`（+ `.specify/shared/` 镜像）；13 个复杂命令模板在 `## Feedback` 后追加 `## Documentation` 引用节（同一收尾点，FR-011）。docs 命令自身也携带该步骤（含 Feedback），列入 COMPLEX_COMMANDS。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/033-docs-command/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── docs-command-template.md   # 命令模板结构契约
│   ├── docs-utils-cli.md          # 引擎脚本 CLI 契约
│   └── docs-step-injection.md     # 文档同步步骤注入契约
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

No standalone research.md — findings inlined under `## Phase 0: Research Review`.

### Source Code (repository root)

```text
templates/commands/docs.md            # 新增：/speckit.docs 源模板（薄调度层：作用域判定+分级确认+引用引擎/参考文档）
templates/commands/<13 复杂命令>.md    # 修改：追加 ## Documentation 文档同步步骤引用节（FR-011）
shared/workflow/docs-step.md          # 新增：文档同步步骤约定单一事实源（仿 feedback-step.md）
shared/patterns/                      # 只读：reconcile-pattern.md 为设计依据，不修改
scripts/python/docs-utils.py          # 新增：确定性引擎（notes 生命周期 + 命名/链接/尺寸校验 + 审计落盘，--action JSON 模式）
docs/commands/docs.md                 # 新增：命令参考文档；docs/quickstart.md 命令表加行
docs/                                 # dogfooding 重组对象（US4/FR-008：向六类 taxonomy 收敛 + notes 退场 + 归档区 docs/archive/）
README.md / ARCHITECTURE.md / CONTRIBUTING.md / CHANGELOG.md  # dogfooding：薄层入口收敛（后两者 bootstrap 新建）
tests/contract/                       # 新增 test_docs_command_*.py；修改 test_feedback_command_classification.py（13→14）
tests/integration/                    # 新增样例夹具生命周期/骨架演练测试
.specify/docs/                        # 运行产物工作区（干跑计划、审计日志——运行时生成，非本仓库交付物）
```

**Structure Decision**: 扩展既有"模板/提示框架"形态——命令为第 19 个 `templates/commands/*.md` 模板（薄调度层，引擎细节沉入 shared 约定与参考文档，遵循 reconcile-pattern §Applying 第 6 条）；确定性能力为第 7 个 `scripts/python/*-utils.py` 脚本；无新增顶层目录（`docs/archive/` 与 `.specify/docs/` 均在既有顶层目录内）。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/docs.md`（新增） | `.specify/templates/commands/docs.md`；运行时副本 `.claude/commands/speckit.docs.md`、`.github/prompts/speckit.docs.prompt.md`、`.qoder/commands/speckit.docs.md`、`.qwen/`、`.opencode/`、`.codex/`、`.hermes/`、`.iflow/` 等既存工具目录 | `python3 scripts/python/regen-command-copies.py --check` 零漂移 |
| `templates/commands/<13 复杂命令>.md`（注入 Documentation 节） | 同上模式：各自 `.specify/templates/commands/` 镜像 + 全部工具运行时副本 | 同上 `--check`；contract 扫描步骤存在性 |
| `shared/workflow/docs-step.md`（新增） | `.specify/shared/workflow/docs-step.md` | `diff -q` 字节一致 |
| `scripts/python/docs-utils.py`（新增） | `.specify/scripts/python/docs-utils.py` | `diff -q` 字节一致 |
| `templates/commands/requirements.md` 等如引用注册表 | （若期望态基线常量沉入 `shared/constants/`，同样双镜像） | `diff -q` |

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| IV Test-First = Partial（template-only） | 命令本体是 prompt 模板，无可执行运行时；constitution VII 明文规定此类 feature 以模板内容/路径/结构契约测试代替 | "为提示词写行为单测"不可行；docs-utils.py 作为唯一可执行件仍走完整 Test-First（契约测试先行） |
