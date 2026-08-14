# Implementation Plan: Feedback 机制的 Probe 化重构(反馈插点 + 切片定向 + 三模式管理命令 + 外部 probe)

**Branch**: `041-refactor-feedback-probe` | **Date**: 2026-08-14 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `041-refactor-feedback-probe` → Feature 028 Feedback Mechanism
**Input**: Specification from `.specify/specs/041-refactor-feedback-probe/requirements.md`

**Note**: This template is filled in by the `/speckit.plan` command, which **replaces** every `[PLACEHOLDER]` token in place — it MUST NOT append a second copy of this template below the filled content. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

把反馈机制从「隐式埋点 + 全局视角自由文本」重构为显式建模的 Feedback Probe 体系:新增 probe 真源 `shared/definitions/probe-definitions.md`(Class/Object 两层 + internal/external 类别),既有 49 个 wrap-up 埋点(31 skills + 18 复杂命令)重构为 Object 并归类到两个内部 Class(`command-wrapup` / `skill-wrapup`);`feedback-utils.py` 引擎扩展 probe 解析、切片过滤、外部条目打包排除、打包后清理与 probe 结构图重建;新增复杂命令 `templates/commands/feedback.md`(三模式:无参数 probe 总览 / 处理含打包后清理 / 注入外部 probe)分发到 6 家工具命令副本;旧格式条目一次性整体 review 收敛(已合入删除/有价值重登记,处置留痕)。四条红线按内外类别分级保留,零自动传输不变。

## Technical Context

**Language/Version**: Python >= 3.8(引擎 stdlib-only,与现行 `feedback-utils.py` 一致);命令/定义为 Markdown 模板
**Primary Dependencies**: 无新增第三方依赖 — 扩展现有 `scripts/python/feedback-utils.py`(763 行,argparse 单文件引擎);镜像经 `sync-mirrors.py` + `regen-command-copies.py`
**Storage**: files-based(维持)—— probe 真源 `shared/definitions/probe-definitions.md`(框架内部 Class/Object,机器可解析 Markdown 表);项目外部 probe `.specify/memory/feedback/probes/*.md`(YAML frontmatter,一个 probe 一文件,与 memory-as-files / `*.agent.md` 同构);条目与 index 沿用 `.specify/memory/feedback/`
**Testing**: pytest(`tests/contract/`,沿 `test_feedback_*.py` 6 文件先例新增 probe 契约测试;全量基线对比零新增失败)
**Target Platform**: 跨平台 CLI(Python / 6 家 agent CLI 的命令副本);Linux 为验证平台
**Project Type**: framework / code-generator(templates + scripts + src 三层)
**Performance Goals**: probe 总览/过滤/重建为本地文件操作,秒级;无网络
**Constraints**: 零自动传输(红线);引擎 stdlib-only;旧条目 review 处置一次性完成且留痕
**Scale/Scope**: 内部 Object 49 既有(31+18)+ 1 新增(feedback 命令自身,交付时 50)、3 个初始 Class(2 内部 + 1 外部基类)、21 条 FR、6 个故事、8 条 SC;新增 1 个命令模板 ×6 工具副本、1 个定义文件、5 个新引擎动作 + record/list 旗标扩展

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 每 FR 追溯到 spec 条目;plan/contracts/data-model 均由 requirements.md(21 FR/8 SC)派生 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 028;feature-ref.md 记录映射;features/028.md 增补 Planned 条目 |
| III | Intent-Driven Development | ✅ Pass | 三模式与外部 probe 直接承载用户三轮输入的意图(冗余消除/本地处置/自定义单元反馈) |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | contracts/ 4 份(注册表 schema、引擎 CLI、条目 schema、命令行为);契约测试先行任务在 tasks 阶段置顶 |
| V | AI Agent Integration Standards | ✅ Pass | 新命令经 `regen-command-copies.py` 分发 6 家工具副本;probe 步骤对 6 家工具语义一致 |
| VI | Continuous Quality & Observability | ✅ Pass | 处置留痕(迁移日志/清理记录)、probe 零产出可观测、SC-001~008 全部可程序判定 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → plan(本文件)→ tasks → implement 标准链;旧条目处置走迁移日志而非跳步 |
| VIII | Code as the Single Source of Truth | ✅ Pass | probe 单一真源 + 结构图为派生物(重建零差异);条目 probe/kind/slice 由引擎自真源解析,不手工双写 |
| IX | Framework Scope Discipline (No Over-Engineering) | ⚠ Partial — see Complexity Tracking | 新增命令面 + 引擎动作扩展;以复用既有引擎/真源模式收敛,无新运行时设施 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 定义入 `shared/definitions/`、命令文档入 `docs/reference/commands/feedback.md`、机制文档更新 `docs/reference/skills/feedback.md` |
| XI | Dogfooding (Self-Application) | ✅ Pass | Loop A(内部 probe→框架上送)与 Loop B(外部 probe→宿主项目自优化)在同一机制内闭合 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 扩展 `<TOOL:.specify/memory/tools/feedback-utils.py.md>` 而非新脚本;镜像走 `sync-mirrors.py` 单命令 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Learning Capture 维度:切片定向使反馈可定向消费,外部 probe 把学习环扩展到宿主项目 |

**Gates Status**: ⚠ 唯一 Partial 为原则 IX,有正当理由(见 Complexity Tracking),无阻断失败。

**Re-check after Phase 1**: 2026-08-14 — Phase 1 产物(data-model.md / contracts×4 / quickstart.md / feature-ref.md)落盘后复查:IX 仍为 Partial(理由不变,新增面已被「复用 feedback-utils.py 单引擎 + 单定义文件」收敛),其余 12 项 Pass 不变。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/041-refactor-feedback-probe/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── probe-registry.md
│   ├── engine-cli.md
│   ├── entry-schema.md
│   └── feedback-command.md
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── checklists/requirements.md  # 已存在(requirements 阶段产出)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

No standalone research.md — findings inlined below (## Phase 0).

### Source Code (repository root)

```text
shared/definitions/probe-definitions.md        # probe 真源:3 Class + 49 内部 Object 表 + 外部 probe 登记契约
templates/commands/feedback.md                 # 新复杂命令:三模式 + ## Feedback + ## Documentation
shared/workflow/feedback-step.md               # canonical 步骤改版:record 经 probe 解析(自动按 unit_id 解析 Object)
scripts/python/feedback-utils.py               # 引擎扩展:probes/probe-inject/map/cleanup/delete 动作 + probe/kind/slice 字段与过滤 + package 排除外部
docs/reference/commands/feedback.md            # 新命令用户文档
docs/reference/skills/feedback.md              # 机制文档更新(probe 模型、三模式、内外分级红线)
.specify/memory/feedback/probes/               # (下游项目运行时)宿主项目外部 probe 登记,模式三写入
src/specify_cli/__init__.py                    # 无改动(命令为模板分发,不进 CLI 包)
tests/contract/test_feedback_probe_*.py        # 新增契约测试(注册表/引擎/命令/排除)
```

**Structure Decision**: 扩展现有 framework/code-generator 形态 —— 新增 1 个定义文件(`shared/definitions/probe-definitions.md`,沿 agent/goal/subagent/tool-definitions 先例)+ 1 个命令模板(`templates/commands/feedback.md`,分发 6 家工具副本)+ 既有引擎与 canonical 步骤的就地扩展。不新增顶层目录;`.specify/memory/feedback/probes/` 为下游项目运行时目录(由引擎按需创建,非本仓库源码)。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/definitions/probe-definitions.md` | `.specify/shared/definitions/probe-definitions.md` | `sync-mirrors.py --check`(exit 0) |
| `templates/commands/feedback.md` | `.specify/templates/commands/feedback.md`; 仓库现存工具副本面(实测 4):`.claude/commands/speckit.feedback.md`、`.github/prompts/speckit.feedback.prompt.md`、`.qoder/commands/speckit.feedback.md`、`.opencode/command/speckit.feedback.md`;codex/hermes 副本由 `specify init` 下游分发,不在本仓生成 | `sync-mirrors.py --write` 后 `--check`;逐副本含 AUTO-GENERATED 头 |
| `shared/workflow/feedback-step.md` | `.specify/shared/workflow/feedback-step.md` | `sync-mirrors.py --check` |
| `scripts/python/feedback-utils.py` | `.specify/scripts/python/feedback-utils.py` | `sync-mirrors.py --check` |
| 既有 18 个命令模板的 Feedback 步骤措辞(如受 canonical 步骤改版牵连) | `.specify/templates/commands/*.md` + 各工具命令副本(经 `regen-command-copies.py` 再生) | 再生副本含编辑;`--check` exit 0 |

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| 原则 IX Partial:新增 1 个命令面 + 引擎 6 处动作/旗标扩展(超出「纯重构」) | 用户明确裁定三模式管理命令与外部 probe 注入为本需求范围(2026-08-14 第二轮指令);外部 probe 是 Loop B 的一等能力缺口 | 仅做 probe 建模不加命令 = 用户痛点 2(无本地管理接口)无解;另起独立引擎/脚本 = 违反 XII 工具复用且双引擎漂移 |
| 旧条目收敛处置引入删除语义(偏离「source files untouched」现状) | 用户裁定不保留旧格式残留;删除以处置留痕(迁移日志)与包内留档为约束 | 保留全部旧条目 + 未分类桶 = 用户已否决(2026-08-14 第一轮 Q3 答复) |

## Phase 0: Research Review

Phase 0 由本仓库源码与文档内联考察完成(<50 行,无外部源),要点:

- **引擎现状**:`feedback-utils.py`(763 行,stdlib-only)动作集 `record/status/list/mark-submitted/reindex/package/upstream`;`--unit-id` 校验 `^(?:/speckit\.[a-z0-9._-]+|skill:[a-z0-9._-]+)$`;`(unit_id, run_id)` 去重;`mark-submitted` 已是 archive-then-reset(批次 zip 进 `packages/` 后复位计数)——「打包后的清理」以 `cleanup` 动作补齐「活跃库移除已打包条目」一步,与该语义衔接而非替换。
- **嵌入面实测**:31 个 `skills/*/SKILL.md` + 18 个 `templates/commands/*.md` 嵌 `## Feedback`(49 个隐式点);`docs/reference/skills/feedback.md` 分类表(13 复杂/4 简单)已滞后,实施时同步修订。
- **关键设计——免模板风暴的 probe 解析**:49 个嵌入单元与 probe Object 一一对应,故 canonical 步骤的 `record --unit-id` 可由引擎按 unit_id 自动解析出 Object→Class(切片/类别),模板正文只需随 `feedback-step.md` 一次改版,不必逐个改写 49 份模板的参数行(归档 SC-001 的对账脚本另负责漂移检测)。
- **Class 划分**(覆盖全部既有插入形态):`command-wrapup`(内部,slice=commands,18)/`skill-wrapup`(内部,slice=skills,31)/`external-custom`(外部,宿主自定义单元,0 个初始 Object,模式三注入)。两内部类处理流程相同(record→threshold→package→手动投递→mark-submitted),外部类处理流程为 record→本地消费(排除 package)。
- **真源载体先例**:`shared/definitions/{agent,goal,subagent,tool}-definitions.md` 均为「概念权威」定义文件模式;probe 沿用该模式,外部 probe 走项目侧 `.specify/memory/feedback/probes/*.md`(frontmatter 一文件一 probe,与 `*.agent.md` 同构)。
- **测试面**:`tests/contract/` 已有 6 个 `test_feedback_*.py`(76 用例基线);`test_feedback_command_classification.py` 的分类计数断言需随 +1 命令更新。
- **Feature 记账**:Feature 028 状态 Implemented 不回退(036 先例);requirements 041 的 Planned 条目追加进 `features/028.md`,features.md 行更新 Last Updated 与 Notes。

## Phase 1: Design & Contracts

产物已落盘(计数以实际文件为准,见 Project Structure):

- `data-model.md` — 6 实体(Probe Class / Probe Object / External Probe / System Slice / Feedback Entry / Probe Map)+ 两个登记文件 schema 与状态迁移。
- `contracts/` ×4 — `probe-registry.md`(真源格式与不变量)、`engine-cli.md`(动作/旗标/JSON 输出/退出码)、`entry-schema.md`(条目 frontmatter 扩展)、`feedback-command.md`(三模式行为 + 模板/镜像义务)。
- `quickstart.md` — 三模式端到端演练(命令示例由 tasks 中的契约测试钉住,符合 Phase 1 清理门第 4 条选项 b)。
- `feature-ref.md` — 绑定 Feature 028 与映射表。

Constitution 复查(Phase 1 后):12 Pass + IX Partial(理由同上),无新增违规。
