# Implementation Plan: 大模型 Token 使用效率纪律(程序优先 + 摘要优先 + 消耗观察反馈)

**Branch**: `035-token-efficiency` | **Date**: 2026-08-02 | **Spec**: [requirements.md](requirements.md)
**Requirement → Feature**: `035-token-efficiency` → Feature 040 Token Efficiency Discipline
**Input**: Specification from `.specify/specs/035-token-efficiency/requirements.md`

## Summary

把 Token 使用效率确立为框架持久纪律:新增单一事实源纪律文档 `shared/guidelines/token-efficiency.md`(程序优先/摘要优先/消耗观察,含判定边界、例外情形、升级阶梯、小文件阈值),经 `templates/instructions-template.md` ambient 引用生效;扩展 `shared/workflow/feedback-step.md` 的 Reflect 步骤加入 Token 效率自评维度(稳定标记 `token-efficiency`),并给 `feedback-utils.py list` 增加 `--contains` 文本过滤(程序侧检索,零新子系统);在 create-*/improve-* 创作检查单中落 Token 效率检查项;对全部命令/技能/共享工作流执行一次两纪律审计产出违规清单(`audit.md`),整改严重度 top 5(候选热点已由探查采样:plan/clarify/tasks/implement/requirements 命令模板的整读式上下文加载)。全程 canonical → mirror 单源同步,contract 测试先行钉住纪律文档、标记与整改后的模板措辞。

## Technical Context

**Language/Version**: Python ≥ 3.8(引擎改动,stdlib-only)+ Markdown(纪律文档、模板、检查单)  
**Primary Dependencies**: 零新增依赖;复用 `feedback-utils.py`、`sync-mirrors.py`、`regen-command-copies.py`  
**Storage**: `.specify/memory/feedback/`(条目 + index.json,现状不变);纪律文档落 `shared/guidelines/`;违规清单落本 spec 目录 `audit.md`  
**Testing**: pytest(`-m contract` 为主;引擎过滤行为附单元/合同测试);既有基线纪律——动手前记录全套基线  
**Target Platform**: 跨平台(框架仓库自身;下游经安装继承 `.specify/` 侧)
**Project Type**: single(框架仓库:templates/ + scripts/ + skills/ + shared/ 多面扇出)  
**Performance Goals**: top 整改项注入量(行/字节代理)较整改前下降 ≥ 50%(SC-003);无运行时性能目标  
**Constraints**: 不新建监控子系统(观察全走既有 Feedback 机制);引擎保持 stdlib-only;不编造 Token 数值(定性/代理口径);镜像模型零单侧修改  
**Scale/Scope**: 审计面 ≈ 17 个命令模板 + 26 个技能 + 10 个共享工作流文档 + 9 个数据引擎(以审计时点动态计数为准);整改配额固定 top 5

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | requirements.md(经 clarify 定稿)驱动本计划;spec→plan→tasks 链路完整 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 040(feature-ref.md);索引/详情同步推进 Draft→Planned |
| III | Intent-Driven Development | ✅ Pass | spec 全程 WHAT/WHY;HOW 收敛于本计划与 contracts/ |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | contracts/ 三份合同 + contract 测试先行钉住纪律文档、标记、整改措辞(见 Phase 1) |
| V | AI Agent Integration Standards | ✅ Pass | 命令模板整改经 regen-command-copies.py 扇出全部 5 套工具副本(Mirror Obligations 表) |
| VI | Continuous Quality & Observability | ✅ Pass | SC-001…005 可测;token-efficiency 标记使消耗观察可检索可聚合 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | 本计划为第二阶段;/speckit.tasks 接续 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 纪律定义唯 token-efficiency.md 一处;各单元仅引用不复制(FR-001) |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新子系统/零新引擎;仅 `--contains` 一个最小过滤参数 + 文档/检查单改动;审计产物为 spec 内 Markdown,不建新存储 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 纪律文档入 shared/guidelines/(约定层);docs/ 空间变化由 wrap-up docs-step 评估 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 审计对象即 Spec Kit 自身;本 spec 流程已产出 2 条真实 token 观察反馈(035/clarify 运行) |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 sync-mirrors.py、regen-command-copies.py、feedback-utils.py;不新写同类脚本 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 纪律即 harness 的效率维度;反馈标记供 improve-* 消费闭环 |

**Gates Status**: ✅ All gates pass

**Re-check after Phase 1**: 2026-08-02 — data-model.md / contracts/ / quickstart.md / feature-ref.md 落盘后复核,13 项结论不变(合同未引入新子系统、未复制纪律定义、镜像表覆盖全部触点)。

## Phase 0: Research Review

No standalone research.md — findings inlined below (internal investigation only).

1. **Canonical 源确认**:根级 `shared/` 为 canonical,`.specify/shared/` 为镜像;feedback-step.md 的自评维度应扩展其 Canonical block 的 step 2(Reflect),嵌入单元零改动(仅引用)。
2. **引擎摘要能力矩阵**(审计输入):feedback-utils(list 带 summary,✅)、memory-utils(recall 评分检索,✅ 参考范式)、evidence-utils(list/latest/compare,✅)、docs-utils(scan/stats,✅)、history-utils(extract 整会话转储,**缺摘要模式**)、glossary-utils(list 全表,小文件豁免候选)、tools-utils/skills-utils(record-load/skill-read 全文——多为编辑目标,例外情形)。
3. **反馈引擎无标记概念**:frontmatter 固定字段无 tags;`list` 仅 unit-id/unit-type/since/limit 过滤。决策:不加 frontmatter 字段,为 `list` 增加 `--contains <text>` 程序侧全文过滤(引擎读原文属程序优先鼓励方向),以优化点内嵌字面量 `token-efficiency` 作为稳定标记。
4. **违规热点采样**(top 5 候选,以正式审计定稿):plan.md 命令"读 features.md + features/ 全部文件"(最重);clarify.md"Load common context"整读;implement.md 一次性加载全部工件;tasks.md 整读 constitution 找关键词;requirements.md 整读最新规格取家规。反例范式:analyze.md"仅加载最小必要上下文"、memory-recall 检索式访问。
5. **创作门槛落点**:create-skills/improve-skills 的 references 检查单为主落点;create-agent/create-team/create-tools 在各自验证步骤加一行检查项引用;`templates/skills-template.md` 无检查单节,不动(检查项归创作流程,不归产物模板——防模板膨胀)。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/035-token-efficiency/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── audit.md             # 实施期产物:两纪律违规清单(FR-006;/speckit.implement 产出)
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

No standalone research.md — findings inlined above.

### Source Code (repository root)

```text
shared/guidelines/            # 新增 token-efficiency.md(纪律单一事实源)
shared/workflow/              # feedback-step.md 扩展 Reflect 步骤(Token 自评 + 标记约定)
templates/                    # instructions-template.md 增 ambient 引用节
templates/commands/           # top-5 整改对象(以 audit.md 定稿;候选 plan/clarify/tasks/implement/requirements)
scripts/python/               # feedback-utils.py list 增 --contains 过滤
skills/create-skills/         # references/skill-creation-quality-checklist.md 增检查项
skills/improve-skills/        # references/skill-quality-checklist.md 增检查项
skills/create-agent/          # SKILL.md 验证步骤增检查项引用(create-team/create-tools 同)
tests/contract/               # 新 contract 测试:纪律文档/标记/引擎过滤/整改措辞钉扎
```

**Structure Decision**: 扩展既有"框架多面扇出"形态——零新顶层目录、零新子系统;一份新纪律文档 + 四类既有面(共享工作流、指令模板、命令模板、创作检查单)的最小编辑 + 引擎单参数增强,全部经现行 canonical → mirror 单源同步落地。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/guidelines/token-efficiency.md`(新增) | `.specify/shared/guidelines/token-efficiency.md` | `sync-mirrors.py --check` |
| `shared/workflow/feedback-step.md` | `.specify/shared/workflow/feedback-step.md` | `sync-mirrors.py --check` |
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md` | `sync-mirrors.py --check`(字节一致) |
| `templates/commands/<top-5 整改命令>.md`(每个) | `.specify/templates/commands/<cmd>.md`;`.claude/commands/speckit.<cmd>.md`;`.github/prompts/speckit.<cmd>.prompt.md`;`.qoder/commands/speckit.<cmd>.md`;`.qwen/commands/speckit.<cmd>.toml`;`.opencode/command/speckit.<cmd>.md` | `sync-mirrors.py --write` 委派 regen 后 `--check`;副本含整改措辞 |
| `scripts/python/feedback-utils.py` | `.specify/scripts/python/feedback-utils.py` | `sync-mirrors.py --check` |
| `skills/create-skills/references/skill-creation-quality-checklist.md` | `.specify/skills/create-skills/references/…` | `diff -rq skills/ .specify/skills/` |
| `skills/improve-skills/references/skill-quality-checklist.md` | `.specify/skills/improve-skills/references/…` | 同上 |
| `skills/create-agent/SKILL.md`、`skills/create-team/SKILL.md`、`skills/create-tools/SKILL.md` | `.specify/skills/<name>/SKILL.md` 各一 | 同上 |

## Complexity Tracking

N/A — 无宪法违规需要豁免。
