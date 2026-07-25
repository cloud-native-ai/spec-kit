# Implementation Plan: Dogfooding Practice Adoption

**Branch**: `032-dogfooding-practice` | **Date**: 2026-07-25 (revised same day) | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `032-dogfooding-practice` → Feature 036 Dogfooding Practice
**Input**: Specification from `.specify/specs/032-dogfooding-practice/requirements.md`

## Summary

Dogfooding 显名化、零新机器：(1) 在 Spec Kit 自身 constitution 新增命名原则（Principle XI "Dogfooding"），内容为核心理念（开发者≈使用者的紧密反馈循环）、两级既存循环的指认（Loop A：下游项目经 Feature 028 反馈链路回流框架；Loop B：下游项目复用框架能力自建产品循环）、框架自用与偏离留档条款、建议性声明；(2) 在 `instructions-template.md` 新增项目无关的 `## Dogfooding Practice` 指引节（Loop A 可操作路径 + Loop B 能力映射 + 反误区 + 分阶段/场景裁剪），经 `/speckit.instructions` 非破坏送达。**明确不做**：feedback-utils 任何扩展、review 等命令模板任何新步骤、任何新存储（FR-004 红线，SC-004 可验证）。

## Clarifications

- Q: 约束强度？ → A: 建议性原则 + 指引；无门禁、无新增节点步骤。
- Q: Feature 绑定？ → A: Feature 036；028 为被指认的既有载体（非扩展对象）。
- 用户修订（2026-07-25）：聚焦框架本身、复用既有循环、不新建机器 → 本 plan 为修订版，替换初版中的引擎扩展与 review 步骤设计。

## Technical Context

**Language/Version**: Markdown（constitution / 模板）；Python >=3.8 仅用于测试（pytest 契约测试）  
**Primary Dependencies**: 无新增；无运行时代码改动  
**Storage**: 无变化 —— 既有 `.specify/memory/feedback/` 等布局原样（SC-004 断言不变性）  
**Testing**: pytest `tests/contract/`（内容契约：constitution 原则、模板节、镜像一致、无新机器断言）  
**Target Platform**: 跨平台 CLI 工作区（同 spec-kit 既有）  
**Project Type**: single（文档/提示词框架）  
**Performance Goals**: N/A —— 纯文本交付  
**Constraints**: FR-004 复用红线（引擎动作集/命令步骤集/存储布局零变更）；`/speckit.instructions` 非破坏刷新；模板中性（指引项目无关）；镜像同步（instructions-template ×2）  
**Scale/Scope**: 1 条 constitution 原则；1 个模板节 × 2 镜像；1 个契约测试文件；2 处 docs 轻量更新

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 交付物逐条追溯 FR-001…005（Summary / contracts/dogfooding-artifacts.md） |
| II | Feature-Centric Development | ✅ Pass | Feature 036 绑定并随修订同步（features.md、feature-ref.md） |
| III | Intent-Driven Development | ✅ Pass | 修订源自用户理念澄清，spec 先行更新，plan 随之 |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | 纯模板/治理文本特性：按 Principle VII "Template-only features" 规则以内容契约测试替代运行时测试（justified） |
| V | AI Agent Integration Standards | ✅ Pass | 不触碰任何命令模板与代理配置 |
| VI | Continuous Quality & Observability | ✅ Pass | constitution 按修订程序 MINOR 升版；变更全部走 SDD 产物留痕 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本次修订即"在既有 spec 上就地修订"而非重铺（in-place amend 纪律） |
| VIII | Code as the Single Source of Truth | ✅ Pass | Loop A 路径描述以 feedback-utils.py 实际动作集（record/status/list/package/upstream/mark-submitted）为准，初版已实测核验 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 本修订的直接体现：裁撤引擎扩展与新命令步骤，FR-004 将"不新建机器"上升为需求红线并由 SC-004 验证 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新增文本均落于既有文件；无新文件名冲突 |

**Gates Status**: ✅ Pass（Principle IV 为 Partial 但按 Principle VII 模板特性规则已豁免，见 Complexity Tracking）。

**Re-check after Phase 1**: 2026-07-25 — 修订版设计产物（data-model.md、contracts/dogfooding-artifacts.md、quickstart.md）重生成后复核：结论不变；原 contracts/feedback-utils-extension.md 已删除，无残留引用。

## Phase 0: Research Review

No standalone research.md — findings inlined below（内部调研，<50 行）。

1. **既有循环机制盘点**（Loop A/B 的载体，全部已存在，零缺口）：
   - **Feedback 机制**（Feature 028）：`feedback-utils.py` 动作 record / status / list / mark-submitted / reindex / package / upstream；阈值触发合并提交提示；**手动**提交安装源仓库（零自动传输）。→ Loop A 回流全链路。
   - **任务记录 / verification**：tasks.md 状态符号 + verification.md SC 状态行 → 迭代闭环证据。
   - **memory（session/knowledge）与 history**：经验沉淀与蒸馏 → Loop B 素材。
   - **review**：全局诊断复盘（自带 Feedback 步骤）→ Loop B 复盘节点（无需为 Dogfooding 加步骤）。
2. **结论**：初版设计的 `--status`/`resolve`/`loop-health` 与 review 新步骤同既有能力重复且违反聚焦方向 → 全部裁撤；被 FR-004 明令禁止。
3. **下游送达先例**：Feature 032（Task Complexity Rubric）的 "instructions-template 节 + 双镜像 + 契约测试" 模式直接复用。
4. **Constitution 修订**：1.5.0.1 → MINOR 升版；含 Sync Impact Report 头注更新；自用与偏离留档条款入原则正文（FR-002 由治理文本承载，无代码）。
5. **镜像义务清单**：仅 instructions-template ×2（`templates/` ↔ `.specify/templates/`）。不涉及命令模板运行时副本、不涉及脚本镜像。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/032-dogfooding-practice/
├── plan.md              # This file (/speckit.plan output, revised)
├── data-model.md        # Phase 1 output (revised)
├── quickstart.md        # Phase 1 output (revised)
├── contracts/
│   └── dogfooding-artifacts.md   # 治理/模板内容契约 C-1…C-7（修订版；feedback-utils-extension.md 已删除）
├── feature-ref.md       # Phase 1 output (revised)
├── tasks.md             # Phase 2 output (/speckit.tasks, revised)
└── verification.md      # Implementation output (/speckit.implement)
```

No standalone research.md — findings inlined above.

### Source Code (repository root)

```text
.specify/memory/constitution.md      # 新增 Principle XI "Dogfooding"（MINOR 升版 + Sync Impact Report）
templates/instructions-template.md   # 新增 `## Dogfooding Practice` 节（Loop A 路径 + Loop B 映射 + 反误区）
.specify/templates/instructions-template.md  # 字节一致镜像
tests/contract/test_dogfooding_practice.py   # 内容契约测试（新建；含 SC-004 无新机器断言）
docs/skills/feedback.md              # 轻量补注：该机制即 Dogfooding Loop A 的载体
```

**Structure Decision**: 纯文档/模板交付——治理文本 + 模板节 + 契约测试；零运行时代码变更、零新文件目录；唯一镜像义务为 instructions-template 双写。

## Complexity Tracking

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle IV Partial（无运行时测试） | 特性为纯治理/模板文本，无可执行行为 | Principle VII 已为 template-only features 明确此豁免路径：以内容契约测试（原则存在性、节内容、镜像一致、动作集不变性）作为测试层 |
