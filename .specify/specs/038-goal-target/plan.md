# Implementation Plan: Goal 的 Target 切片(run 级可指定的子成果分解)

**Branch**: `038-goal-target` | **Date**: 2026-08-11 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `038-goal-target` → Feature 041 Goal Registry
**Input**: Specification from `.specify/specs/038-goal-target/requirements.md`

## Summary

Goal 与团队 run 之间缺少一个粒度层:run 需要的是小时级、可指派、可判定完成的**范围切片**,而 Goal 是月级端态。本计划在 Goal 之下落地 **Target(目标切片)** 机制——概念锚已随规格落定([[STR-004]]),本计划承载全部操作面:

1. **引擎面**:`goal-utils.py` 新增 `targets` 动作组(add / list / 状态迁移),在 `goal.md` 渲染可选的 [[STR-001]] 节;GD-2/GD-3 检测复用 objective 同源文法(FR-003)。
2. **消费面一(run 指派)**:`/speckit.team` run 模式接受可选 `--target` 参数,preview 阶段校验(悬空报错、终态复核二分、跨 goal 拒绝),确认门禁披露,run report 记录(FR-009…FR-012)。
3. **消费面二(台账与总结)**:`items.jsonl` 新增可选 [[STR-003]] 字段;`build-summary-input.py` 折叠时产出切片轴卷积(n/m),与判据轴分列;authored/证据不一致列为待批准项;`done` Target 以来源标记喂给里程碑视图(FR-013…FR-016)。
4. **术语与文档**:词汇表消歧条目 + 下游文档链接概念锚,全部经 `sync-mirrors.py` 扇出(FR-017/FR-018)。

核心不变量:绑定轴保持 team ↔ Goal 静态;run 级变量是 Target——永不改绑、永不改变两级身份解析、永不迁移 summary 交付目录。无 Target 的 goal 与未指定 Target 的 run 逐字节等价于引入前行为(SC-002)。

## Technical Context

**Language/Version**: Python ≥ 3.8(与既有引擎一致,`goal-utils.py` / `build-summary-input.py` 均为 stdlib-only)+ Markdown 命令模板  
**Primary Dependencies**: 无新增运行时依赖;测试用 `pytest`(markers `contract` / `integration`)  
**Storage**: 文件——`goal.md` 的 [[STR-001]] 节(引擎渲染)、`items.jsonl` 的可选 [[STR-003]] 字段、总结输入 YAML(`data/project-input.yaml`)新增 `targets` 块  
**Testing**: pytest(单元 `tests/unit/test_goal_utils.py` 扩展;契约 `tests/contract/` 新增目标契约族;集成 `tests/integration/` 扩展总结折叠族)。基线先行:实施前先跑全套件,区分存量失败与回归  
**Target Platform**: Linux/macOS 开发环境;命令模板经 per-tool 副本被 6 家 AI agent CLI 消费  
**Project Type**: 代码生成器/框架(templates/ + scripts/ + skills/,镜像模型 canonical → `.specify/` → per-tool 副本)  
**Performance Goals**: 单 goal 的 Target 数量为个位至十位级(规格 Assumptions);`## Targets` 内联渲染即可读;折叠为 O(台账行数) 单遍扫描  
**Constraints**: SC-002 零回归(无 Target 时行为逐字节等价);单引擎纪律(不另立第二检测文法、第二渲染器);全部镜像经 `sync-mirrors.py`,禁止手工双写  
**Scale/Scope**: `goal-utils.py` +~120 行;`build-summary-input.py` +~80 行;2 个命令模板(goal/team)+ 各 4 份 per-tool 副本;4 个 create-team references;3 份契约;词汇表 1 条;docs 2 篇;新增/扩展测试约 12 个文件

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, 13 principles in order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 计划完全派生自 038 规格(18 FR / 6 SC);概念事实源 [[STR-004]] 先于操作面落地 |
| II | Feature-Centric Development | ✅ Pass | 挂 Feature 041 Goal Registry(Target 是 Goal 概念组成,非团队属性);feature-ref.md 记录映射 |
| III | Intent-Driven Development | ✅ Pass | `/speckit.team` 意图路由三模式不变;`--target` 是 run 模式的可选参数,不新增意图类别 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 3 份契约先行(`contracts/`);引擎单测、run 契约测试、折叠集成测试在 tasks 阶段置于实现之前 |
| V | AI Agent Integration Standards | ✅ Pass | 命令面变更只经 `templates/commands/` + `sync-mirrors.py` 扇出到既有 4 家 per-tool 副本目录,不新增工具表面 |
| VI | Continuous Quality & Observability | ✅ Pass | 变更记入 goal `## History`;run report 记录指派(含"无");总结产出待批准项清单——全链路可追溯 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify(1 问 1 裁决)→ 本计划 → tasks → implement 顺序执行,校验清单已过 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 切片轴数值只从台账 [[STR-003]] 折叠(出处可验证);目标状态只从 `goal.md` 解析;无缓存回填 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 全部新增面均为既有命令/引擎的模式扩展(goal-utils 加一个动作组、team run 加一个可选参数、折叠加一个可选字段);零新命令、零新技能、零新脚本文件 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 规格/计划/契约落 `.specify/specs/038-goal-target/`;概念表述链接 [[STR-004]] 不复述(FR-001) |
| XI | Dogfooding (Self-Application) | ✅ Pass | 机制自身即被本仓库消费:框架演进类 goal(如既有监控团队场景)可直接切片指派 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `goal-utils.py` 单引擎(FR-007)与 `sync-mirrors.py` 扇出;GD-2/GD-3 检测复用同源函数,不生成第二套 |
| XIII | Better-Harness Orientation | ✅ Pass | Target 把"run 干了哪块"从即兴自然语言升为可聚合结构化事实——Agent Work Loop 的可控点增强,证据链(台账→卷积→待批准项)完整 |

**Gates Status**: ✅ All gates pass(13/13,无 Fail/Partial,Complexity Tracking 为 N/A)

**Re-check after Phase 1**: 2026-08-11——设计工件(data-model.md、3 份契约、quickstart.md、feature-ref.md)落盘后复核:上表逐行仍成立;IX 特别复核——契约未引入新脚本文件或新命令表面,仅既有面扩展,维持 Pass。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/038-goal-target/
├── plan.md              # 本文件(/speckit.plan 输出)
├── research.md          # 无独立文件——Phase 0 决策内联于下方 "## Phase 0: Research Review"
├── data-model.md        # Phase 1 输出
├── quickstart.md        # Phase 1 输出
├── contracts/           # Phase 1 输出(3 份)
│   ├── targets-engine.contract.md        # goal-utils targets 动作组 CLI/渲染/身份契约
│   ├── run-target-assignment.contract.md # /speckit.team run --target 校验与披露契约
│   └── target-ref-ledger.contract.md     # items.jsonl target_ref + 切片轴折叠契约
├── feature-ref.md       # Phase 1 输出(Feature 041 绑定映射)
├── checklists/requirements.md  # /speckit.requirements 校验清单(已全过)
├── tasks.md             # Phase 2 输出(/speckit.tasks,本命令不创建)
└── verification.md      # 实现输出(/speckit.implement)
```

### Source Code (repository root)

```text
scripts/python/                     # goal-utils.py:新增 targets 动作组 + ## Targets 渲染/解析/校验
templates/commands/                 # goal.md(targets 模式行+引擎调用例)、team.md(run 模式 --target 校验与门禁披露)
skills/create-team/                 # scripts/build-summary-input.py(target_ref 折叠、targets 块、切片轴);
                                    # references/{summary-mapping.md,goal.md,execution-guide.md}(契约与操作文档)
skills/summarize-project/           # 不改代码——done Target 以 source 标记进入既有 milestones 组(FR-016,P3)
shared/definitions/                 # goal-definitions.md 概念锚(已随规格落地,本计划只读)
tests/unit/                         # test_goal_utils.py 扩展(targets 动作、渲染、GD-2/GD-3 复用)
tests/contract/                     # 新增目标契约族 3 文件 + goal/team 命令面既有测试扩展
tests/integration/                  # 总结折叠族扩展(target_ref 归属、切片轴、待批准项、里程碑吸收)
docs/reference/commands/            # goal.md、team.md 用户文档
.specify/memory/                    # glossary.md 新增「Goal Target」消歧条目(不镜像)
```

**Structure Decision**: 扩展既有框架的三个既有点——单引擎 `goal-utils.py` 加一个动作组、命令模板 goal/team 各加既有模式的行与步骤、`build-summary-input.py` 折叠加一个可选字段与输出块。**零新顶层目录、零新脚本文件、零新命令**;`skills/summarize-project/` 保持代码不变(里程碑吸收走既有 `source` 字段)。概念层只读引用 [[STR-004]]。

### Mirror Obligations

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `scripts/python/goal-utils.py` | `.specify/scripts/python/goal-utils.py` | `sync-mirrors.py --check` exit 0 |
| `templates/commands/goal.md` | `.specify/templates/commands/goal.md`;`.claude/commands/speckit.goal.md`;`.github/prompts/speckit.goal.prompt.md`;`.qoder/commands/speckit.goal.md`;`.opencode/command/speckit.goal.md` | 同上(扇出经 `regen-command-copies.py`) |
| `templates/commands/team.md` | `.specify/templates/commands/team.md`;`.claude/commands/speckit.team.md`;`.github/prompts/speckit.team.prompt.md`;`.qoder/commands/speckit.team.md`;`.opencode/command/speckit.team.md` | 同上 |
| `skills/create-team/scripts/build-summary-input.py` | `.specify/skills/create-team/scripts/build-summary-input.py` | 同上 |
| `skills/create-team/references/summary-mapping.md` | `.specify/skills/create-team/references/summary-mapping.md` | 同上 |
| `skills/create-team/references/goal.md` | `.specify/skills/create-team/references/goal.md` | 同上 |
| `skills/create-team/references/execution-guide.md` | `.specify/skills/create-team/references/execution-guide.md` | 同上 |
| `docs/reference/commands/goal.md`、`docs/reference/commands/team.md` | 无镜像(docs/ 不镜像) | — |
| `.specify/memory/glossary.md` | 无镜像(memory/ 不在 MIRROR_PAIRS) | — |

## Phase 0: Research Review

无独立 research.md——全部决策可由规格 + 代码库内部证据裁定(探索 pass 已核验)。决策记录:

| # | 决策 | 结论 | 依据 |
|---|------|------|------|
| D1 | run 指派选项名(规格委托计划期) | `--target <T-<nnn> \| <goal-slug>.T-<nnn>>`(局部形优先,限定形接受) | 冲突核验:evidence/interview-utils 的 `--target` 在不同命令表面;`/speckit.team` 表面无占用;满足 FR-017 且不与 `--goal` 冲突 |
| D2 | 引擎动作名(规格委托计划期) | `targets <slug>` 单动作 + 互斥标志 `--add "<statement>"` / `--list` / `--set <open\|done\|dropped> --id <T-nnn>`;与既有扁平动作风格(create/status/criteria)一致 | goal-utils.py 既有 dispatch 为扁平 if/elif;不引入二级子命令 |
| D3 | [[STR-001]] 节渲染文法 | Markdown 表格 `\| ID \| Target \| Status \|`,行正则 `^\| (T-\d{3}) \| (.+) \| (open\|done\|dropped) \|$`;**节整体缺省 = 无 Target**(FR-002 可选装饰件);空表格非法(validate 报错,退出码 4) | 表格对身份/状态/语句三元组解析无歧义;缺省语义使存量 goal 零迁移、逐字节不变 |
| D4 | 切片轴卷积落点 | `build-summary-input.py` 折叠 [[STR-003]] → 表单新增 `targets:` 块(每 Target:状态、归属条目计数、n/m);报告侧与判据轴**分列**呈现;无效 [[STR-003]] 降级计入 goal 整体并声明 | 折叠权威在台账(036 语义);总结引擎(summarize-project)保持只读呈现,不改 |
| D5 | FR-004 判据复述检测 | 确定性归一化等值检查(去空白/标点/大小写后与 criteria 逐条比对,命中即退出码 2 拒绝);语义近似交由撰写人纪律与 review | 程序优先原则(宪法/Token 效率):可判定部分给程序,模糊判断不伪造检测器 |
| D6 | `## History` 记法 | `- YYYY-MM-DD target T-001 added: <statement>` / `- YYYY-MM-DD target T-001 open→done`——承接 037 变更追溯格式 | goal-utils 既有 history 行为扩展 |
| D7 | 里程碑吸收(FR-016, P3)形态 | `done` Target 作为额外 `milestones` 行进入表单,`source` 值取 `goal-target:<goal-slug>/goal.md#T-nnn`,与判据投影(`source` 指向判据行)天然区分;`project-db.py` 与 DDL 不改 | 里程碑表已有 `source` 列(036 设计);来源标记即区分机制 |
| D8 | 终态复核二分(2026-08-11 clarify 裁决)的机制落点 | preview 报出终态并停止;复核由人执行——属实则结束,不符则经 `/speckit.goal targets --set open` 重开后重新指派;run 模式**不提供**终态执行旁路 | Clarifications Session 2026-08-11;authored-only 边界不开口子 |

## Complexity Tracking

N/A——Constitution Check 13/13 全 Pass,无违规需辩护。
