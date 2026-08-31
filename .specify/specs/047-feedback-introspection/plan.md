# Implementation Plan: Feedback 自省流程(Feedback Introspection)

**Branch**: `047-feedback-introspection` | **Date**: 2026-08-28 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `047-feedback-introspection` → Feature 028 Feedback Mechanism
**Input**: Specification from `.specify/specs/047-feedback-introspection/requirements.md`

## Summary

在既有 feedback 本地闭环的"记录(事实)→打包上行→消费侧设计"之间插入 **Introspection(自省)** 阶段:客户项目内按需触发(`/speckit.feedback` 新增 `introspect` [[STR-001]] 模式),agent 回到真实场景对 open 条目逐条核验、同根因聚类为"问题(Finding)",产出含五要素(陈述/根因/证据锚点/分流决定/优化方案)的**自省报告**;报告确认后批量写回条目处置并建立条目↔问题关联;打包上行时默认提议附入覆盖条目的报告,使消费方收到"事实+核验+根因+方案"。实现面 = 单引擎(`feedback-utils.py`,双镜像)新增少量确定性动作 + 命令模板新增一个模式(模板+镜像+4 份生成副本)+ 契约测试;分析本身是 agent 推理,不落入引擎(程序优先纪律)。

## Technical Context

**Language/Version**: Python ≥3.8(引擎,stdlib-only);Markdown(模板/文档/报告)
**Primary Dependencies**: 无新增 — 引擎维持 stdlib(argparse/json/zipfile/re);不触 typer/rich/httpx
**Storage**: feedback-as-files — 条目 `.specify/memory/feedback/*.md`(YAML frontmatter)+ `index.json`(元数据+条目镜像);**新增** `introspection/` 子目录存自省报告(必须放子目录:`reindex` 对存储根做 `*.md` glob,报告若落根目录会被当成条目吸入索引);上行包 `packages/feedback-<ts>.zip`
**Testing**: pytest(marker: contract/integration),既有 `tests/contract/test_feedback_utils_cli.py` 扩展 + 新增契约文件;`tests/fixtures` + `tests/script_api.py` 惯例;全量基线纪律(先记基线,区分既有失败)
**Target Platform**: 任意客户项目的 Linux/macOS CLI 环境(本仓 `.specify/` 自用运行时同源)
**Project Type**: single(CLI toolkit + 模板/脚本框架源)
**Performance Goals**: 引擎动作为确定性文件/文本处理,≤ 数百条目规模下单次动作 <1s;自省分析为 agent 侧推理,不设时延指标
**Constraints**: 四条红线不破(无网络、无自动传输、外部条目永不上行、条目正文不被改写——处置只动 frontmatter/索引);Token 效率纪律(引擎只出摘要/投影,分析材料由 agent 按升级阶梯自取);`introspect` 关键字全仓无冲突(已查)
**Scale/Scope**: 1 个引擎文件 ×2 镜像;1 个命令模板 ×(1 镜像 + 4 生成副本);1 个新引擎动作(introspect-register)+ 2 个既有动作扩展(dispose/package);2 个 docs 文件;新增 1 个运行时子目录

## Phase 0: Research Review

No standalone research.md — findings inlined below(全部来自仓内实测,无外部调研)。

**探查结论(2026-08-28,对源码实测)**:

1. **引擎现状**:`feedback-utils.py` 1557 行,14 个动作函数分派;条目 = frontmatter(id/unit_id/run_id/probe/kind/slice/disposition/created/summary)+ `## Review` + `## Optimization Points`;`index.json` 为存储元数据 + 条目镜像;`dispose` 单条写回(索引 + 文件 frontmatter,正文不动)。
2. **打包先例**:`write_package` 已支持包内附加文件(`SUBMISSION-NOTES.md`,mark_submitted 的 notes 参数)——自省报告随包上行复用同一模式,无需发明新zip 结构。
3. **关键约束发现**:`action_reindex` 对存储根 `glob("*.md")` 重建索引 → 自省报告 MUST NOT 落在存储根,落 `introspection/` 子目录天然隔离。
4. **命令模板面**:`templates/commands/feedback.md` 四模式结构,Mode 4 以 `$ARGUMENTS` 含 `consume` 触发——新模式沿用同一关键字触发惯例;生成副本经 `regen-command-copies.py` 产出 4 份(.claude/.qoder/.opencode/.github)。
5. **Probe 注册**:probe object 按"命令 × 生命周期点"注册(`speckit-feedback-wrapup` @ wrap-up),**不随模式细分** → 新模式零注册表变更。
6. **既有测试惯例**:`tests/contract/test_feedback_utils_cli.py` 以 `--workspace-root` 指向临时工作区驱动引擎,断言 C-N 规则;probe 注册表另有 `test_feedback_probe_registry.py`。

**User Story → 设计产物映射**:US1(场景化自省)→ 命令新模式流程 + 报告 schema(data-model + contract: introspection-report);US2(分流与处置)→ dispose 扩展(reason/ref)+ 条目↔问题关联(contract: engine-cli);US3(上行包富化)→ package 扩展 + MANIFEST 富化(contract: package-enrichment,并入 engine-cli)。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.10.0.001):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 需求 047 spec 先行,本计划全部设计可回溯至 FR-001..012 |
| II | Feature-Centric Development | ✅ Pass | 绑定既有 Feature 028(clarify 裁定),features/028.md 已反向登记 047 |
| III | Intent-Driven Development | ✅ Pass | spec 以用户故事/FR 表达 what/why,本计划承接 how |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 契约先行(contracts/ 三份),实现任务将按 TDD 排序(tasks 阶段) |
| V | AI Agent Integration Standards | ✅ Pass | 不新增 agent 工具;4 份 per-tool 副本经既有 regen-command-copies.py 生成 |
| VI | Continuous Quality & Observability | ✅ Pass | 处置/关联落 index.json 结构化元数据;报告承继关系可审计 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | Feature reuse-first 满足(028 递进,非新建);无状态回退:Feature 028 保持 Implemented(036/041 先例,plan 阶段不动 Implemented) |
| VIII | Code as the Single Source of Truth | ✅ Pass | 现状锚点与 Phase 0 探查均对引擎/模板源码实测(reindex glob、SUBMISSION-NOTES 先例等关键设计约束来自代码而非文档) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 复用单引擎+既有命令,无新子系统/新命令面/新运行时;报告为 Markdown 文件,分析留给 agent 推理(对比 041 新增整个命令面裁定 Partial,本需求收敛度更高) |
| X | Documentation Naming & Location Conventions | ✅ Pass | 仅更新既有 docs/reference/{commands,skills}/feedback.md;报告存 `.specify/` 运行时域,不占保留文件名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本特性即 Loop A/B 增强;两顶帽子:框架源(templates/scripts)+ 镜像经 sync-mirrors 收敛,不手改 `.specify/` 运行时副本 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 feedback-utils 引擎与既有脚本;无一次性脚本需求 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 强化 Learning Capture 维度(反馈从事实记录升级为场景化学习);证据纪律:核验结论须附证据锚点(SC-003);不新增评分/报告机器 |

**Gates Status**: ✅ All gates pass(13/13 Pass,无 Complexity Tracking 条目)

**Re-check after Phase 1**: 2026-08-28 — 设计产物落盘后复核,13/13 维持 Pass(详见文末复核表)。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/047-feedback-introspection/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── checklists/          # 需求质量检查单(/speckit.requirements 产出,已存在)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

No standalone research.md — findings inlined above.

### Source Code (repository root)

```text
scripts/python/feedback-utils.py        # 框架源:引擎扩展(新动作 + dispose/package 扩展)
.specify/scripts/python/feedback-utils.py  # 引擎镜像(经 sync-mirrors 收敛,不手改)
templates/commands/feedback.md          # 框架源:新增 introspect 模式章节(.specify/templates/commands 镜像已退役,见 sync-mirrors.py exclude_parts)
.claude/commands/speckit.feedback.md    # 生成副本(regen-command-copies.py)
.qoder/commands/speckit.feedback.md     # 生成副本
.opencode/command/speckit.feedback.md   # 生成副本
.github/prompts/speckit.feedback.prompt.md  # 生成副本
tests/contract/                         # 引擎/命令模板契约测试(test_feedback_utils_cli.py 扩展 + 新文件)
docs/reference/commands/feedback.md     # 命令文档:新模式章节
docs/reference/skills/feedback.md       # 系统文档:Layout/Engine/流程章节补自省
.specify/memory/features/028.md         # Feature 详情:047 递进记录(已在 clarify 登记,plan 阶段补设计注记)
```

**Structure Decision**: 扩展现有 feedback 子系统——引擎单文件内新增动作函数(沿用 `action_*` 分派),命令模板新增一个模式章节(沿用 `$ARGUMENTS` 关键字惯例),报告落存储域新子目录 `.specify/memory/feedback/introspection/`(运行时创建;隔离 reindex 的根部 glob)。无新顶层目录。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/feedback-utils.py` | `.specify/scripts/python/feedback-utils.py` | `sync-mirrors.py --check` exit 0 + `diff -q` |
| `templates/commands/feedback.md` | `.claude/commands/speckit.feedback.md`、`.qoder/commands/speckit.feedback.md`、`.opencode/command/speckit.feedback.md`、`.github/prompts/speckit.feedback.prompt.md`(生成副本;`.specify/templates/commands/` 镜像已退役) | 经 `regen-command-copies.py` 重生成后 4 份副本均含新模式章节(grep 断言) |

## Complexity Tracking

N/A — Constitution Check 13/13 Pass,无违规需 justify。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](data-model.md) | 4 实体(IntrospectionReport / Finding / RoutingDecision / FeedbackEntry 扩展)+ 报告生命周期三态 |
| Contracts | [`contracts/`](contracts/) | 3 份:introspection-report.md(报告 schema)、engine-cli.md(引擎动作契约)、command-mode.md(命令模式契约) |
| Quickstart | [`quickstart.md`](quickstart.md) | 1 条端到端场景(造条目→自省→确认处置→富化打包→验包),全部命令经真实引擎执行验证 |
| Feature binding | [`feature-ref.md`](feature-ref.md) | Feature 028 映射 |

## Clarifications

### Session 2026-08-28

- 入口形态与 Feature 绑定经 `/speckit.clarify` 裁定(见 requirements.md ## Clarifications Session 2026-08-27):绑定 Feature 028;`/speckit.feedback` 新增 introspect 模式。本计划无新增 NEEDS CLARIFICATION。
