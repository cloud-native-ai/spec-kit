# Implementation Plan: /speckit.docs 三段式调协编排(目标结构驱动)

**Branch**: `049-docs-reconcile` | **Date**: 2026-09-01 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `049-docs-reconcile` → Feature 037 Docs Command
**Input**: Specification from `.specify/specs/049-docs-reconcile/requirements.md`

## Summary

把 `/speckit.docs` 从"只委托 create-docs 的薄分发层"改造为**目标结构驱动的三段式调协编排**,三段全部落在既有 `## Outline` 之内(不新增顶层小节、不新增运行模式):① 首次运行设计项目专属**目标结构声明**并持久化到 `.specify/docs/target-structure.md`(受管块形态,沿用 `.specify/git-workflow.md` 先例);② 现状对目标做容忍带先行的差异计算,分解为携带 owning 技能的**分型动作**;③ 结构类动作分发 `create-docs`、内容类动作分发 `improve-docs`——后者**首次进入命令分发链路**。实现期用户修订进一步把编排收敛到两个核心问题:写什么(项目证据 + 当前语境 + 用户输入 + 目标读者)与放哪里(唯一 canonical home + 去重 + 固定检索路径);canonical 文档位置变化时通过 `/speckit.instructions` 刷新 Agent instructions 的 Documentation Map。

技术路径的核心是**零新增运行时代码**:声明是 LLM 撰写的受管块 Markdown(新增一份 `templates/` 制品模板作为骨架),动作分解与分发是命令模板的编排文字,`docs-utils.py` 不增动作、不改契约。**新增确认门控数为 0**——声明批准(FR-003)、隐含结构变更回写(FR-010)、目标重设计提议(FR-015)、扇出规模告知与中止(FR-008)全部并入既有 R4 干跑计划这**同一个**已治理门控,是"单引擎坍缩"纪律在门控维度的同构应用。

## Technical Context

**Language/Version**: Markdown 提示词模板(命令模板 + 技能 + 制品模板);测试为 Python `>=3.8` / pytest
**Primary Dependencies**: 无新增运行时依赖。既有资产:`.specify/shared/patterns/reconcile-pattern.md`(调谐语义唯一真源)、`skills/create-docs/SKILL.md`(静态基线 + 结构收敛 owner)、`skills/improve-docs/SKILL.md`(内容质量 owner)、`scripts/python/docs-utils.py`(确定性发现,**本特性不改**)
**Storage**: 文件系统。目标结构声明 = `.specify/docs/target-structure.md`(已入库受版本控制,`git ls-files` 实测 5 个跟踪文件、未被 `.gitignore` 忽略);既有按次产物仍在 `.specify/docs/plans/`、`.specify/docs/audit/` 两个**子目录**——声明作为**工作区根级单文件**与之天然可区分(满足 FR-002a)
**Testing**: `pytest -m contract`;既有相关套件 `tests/contract/test_docs_command_template.py`(12 测试)、`test_docs_skill_pair.py`、`test_docs_utils_cli.py`、`test_confirmation_gates_sweep.py`、`test_feedback_command_classification.py`
**Target Platform**: 与 CLI 一致(Linux/macOS;命令模板经 `regen-command-copies.py` 分发到 4 个已存在的工具副本目录)
**Project Type**: 代码生成器/框架(templates/ + scripts/ + skills/ + src/specify_cli/)
**Performance Goals**: N/A(提示词编排;唯一规模面是内容动作扇出——按 FR-008 不设上限,以"分发前告知计划文档数 + 可中止"控制体验成本)
**Constraints**:
- **确认门控余量为零(实测)**:`scan-confirmation-gates.py --json` → `total: 23`,`by_class {governance_kept: 10, destructive: 13}`,`violations: 0`;`test_confirmation_gates_sweep.py` 的 SC-002 上限 = baseline 93 × 25% = **23.25**。任何**新增一条**阻塞门控即 24 > 23.25 → 测试失败。本规划以"零新增门控"设计规避,不动 `baseline.json`。
- **必须存活的字面量**(否则既有测试红):`stop-and-confirm`(KEEP_LIST,`test_confirmation_gates_sweep.py:25`)、`reconcile-pattern.md`、`docs-utils.py`、`single source of truth`、`skills/create-docs/SKILL.md`、四件产物名(`观察快照`/`残差报告`/`审计日志`/`干跑计划`)、五个作用域名(`全量`/`单目标`/`写作`/`扇出`/`Bootstrap`)。实测各出现 1 次(Bootstrap 2 次)。
- **必须保持缺席**:`R0 需求解析`(`test_c7_thin_dispatch_references` 断言技能内部写作环不得内联到命令);`.specify/templates/commands/docs.md`(镜像已于 2026-08-17 退役,`test_c1_source_and_mirror` 断言其不存在)。
- **`## Outline` 六章节顺序**保持 6 章不变(三段作为 Outline 内的阶段),故契约 C-3 的章节枚举**无需修订**。
- `docs-utils.py` 不新增 action(其契约 C-1 规定动作集固定、新增即契约变更),且不得出现 `feedback` 字样(`test_c10` 断言)。
**Scale/Scope**: 1 命令模板 + 4 生成副本 · 1 新增制品模板(+1 镜像)· 2 技能各 1 处接口级措辞订正(+2 镜像)· 既有 033 契约 6 条修订 · 3 份新契约 · 1 份用户参考文档更新。零运行时代码改动。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`, v1.11.0 — 14 principles):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | requirements.md 先行(19 FR,含 FR-002a 与实现期 FR-016…FR-018 / 7 SC / 3 story),clarify 决策与实现期用户修订均已集成;本 plan 由其派生 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 037 第四次 follow-up;`features/037.md` 已交叉引用,`features.md` 037 行已载 follow-up 说明 |
| III | Intent-Driven Development | ✅ Pass | 用户意图"先设目标再逐次调协 + 带参叠加"直接映射为三段编排与 FR-009 叠加语义 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | 3 份新契约(orchestration / declaration / action-routing)先于实现产出;既有 033 契约 6 条修订(5 条行为修订 + C-8 事实纠正)与配套断言在 tasks 阶段先写测试 |
| V | AI Agent Integration Standards | ✅ Pass | 命令模板经 `regen-command-copies.py` 分发 4 副本(`.claude`/`.github/prompts`/`.qoder`/`.opencode`);不引入工具专属路径 |
| VI | Continuous Quality & Observability | ✅ Pass | 残差报告按 owning 技能分列(FR-013);审计日志零收敛照写;分发前告知计划文档数 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | requirements → clarify → plan(本文件)顺序执行,未跳阶 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 现状锚点全部以源码实测取得(命令模板 72 行 / improve-docs 出现 0 次 / 门控 total 23 / 声明目录已入库),非依赖文档陈述 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | **零新增引擎/脚本/action、零新增门控、零新增顶层小节、零新增运行模式**;新增面仅 1 份制品模板;声明沿用 git-workflow 受管块先例而非自造机制 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 新模板遵循 `<name>-template.md` 约定(`docs-target-structure-template.md`);声明落 `.specify/docs/` 非 `docs/`,不占用保留文件名 |
| XI | Dogfooding (Self-Application) | ✅ Pass | SC-001…SC-004 的测量源即本仓真实运行(连续两次全量 + 双类漂移 + 带参调用),验证阶段在本仓 docs/ 上实跑 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 复用 `docs-utils.py`(validate/scan/audit/fix-links)、`sync-mirrors.py`、`regen-command-copies.py`、`scan-confirmation-gates.py`;不新写脚本 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 闭合"结构收敛与内容质量互不知晓"的 harness 缺口(improve-docs 首次入分发链路),强化 Task Understanding 与 Learning Capture |
| XIV | One Source Of Truth (Authority & Reference Discipline) | ✅ Pass | 声明**引用**而非复制 create-docs 静态基线(FR-002,SC-005 计数为 0);调谐语义仍单一真源于 reconcile-pattern.md;命令不复制门控判据正文(confirmation-gates.md L5 规定) |

**Gates Status**: ✅ All gates pass — 14/14 Pass,0 Fail,0 Partial。Complexity Tracking 为 N/A。

**Re-check after Phase 1**: 2026-09-01 — Phase 1 产物落盘后复核,14/14 仍 Pass。三份契约均未引入新引擎/门控/顶层模式;data-model 的 3 实体全部为既有文件形态上的结构化描述,未新增运行时存储机制;quickstart 定义 6 个待实现阶段通过 active AI agent CLI command/skill surface 在隔离 worktree 中验证的场景。原则 IX 复核重点(新增面是否蔓延):新增**生产制品**仅 `templates/docs-target-structure-template.md` 及其镜像；另按 Test-First/证据纪律新增契约测试与 feature-local baseline/verification 产物,均已在 Project Structure 与 tasks.md 明示。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/049-docs-reconcile/
├── plan.md              # This file (/speckit.plan command output)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
│   ├── docs-command-orchestration.md
│   ├── target-structure-declaration.md
│   └── action-routing.md
├── feature-ref.md       # Phase 1 output (/speckit.plan command)
├── checklists/
│   └── requirements.md  # /speckit.requirements + clarify 记录
├── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
└── verification.md      # Implementation output (/speckit.implement command)
```

No standalone `research.md` — Phase 0 findings inlined below(内部勘察即可解决,无外部来源评估)。

### Source Code (repository root)

```text
templates/commands/docs.md          # 命令模板:三段式编排改造(唯一权威源)
templates/                          # 新增 docs-target-structure-template.md(声明骨架,含占位符)
skills/create-docs/                 # SKILL.md R0 基线加载处接入声明为输入(接口级)
skills/improve-docs/                # SKILL.md L103 机器管理存储措辞订正(接口级)
docs/reference/commands/            # docs.md 用户参考文档:架构陈述/执行流/产物表更新
tests/contract/                     # 新增编排/声明/路由断言;修订 test_docs_command_template.py
.specify/specs/033-docs-command/contracts/  # 就地修订 C-1/C-4a/C-5/C-7/C-8/C-18(附日期修订note)
```

**Structure Decision**: 本特性**不新增顶层目录**,是对既有"代码生成器/框架"形态的原地增强——改 1 份命令模板、加 1 份 `templates/` 制品模板、对 2 个既有技能各做 1 处接口级措辞订正、更新 1 份用户文档、扩充契约与测试。所有三段编排语义落在命令模板既有 `## Outline` 章节内部,不新增顶层小节(保 C-3 六章节枚举不变),不新增运行模式(守单引擎坍缩纪律)。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

镜像对权威定义见 `scripts/python/sync-mirrors.py` `MIRROR_PAIRS`(templates 对**排除** `commands/` 子树;命令模板只经 `regen-command-copies.py` 扇出到工具副本)。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/commands/docs.md` | `.claude/commands/speckit.docs.md`;`.github/prompts/speckit.docs.prompt.md`;`.qoder/commands/speckit.docs.md`(额外 YAML frontmatter,取自 `short-description`);`.opencode/command/speckit.docs.md` —— 经 `regen-command-copies.py`;**无** `.specify/templates/commands/docs.md` 镜像(2026-08-17 退役,测试断言其缺席) | `python3 scripts/python/regen-command-copies.py --check` exit 0;4 副本各含本次改动与 AUTO-GENERATED 头 |
| `templates/docs-target-structure-template.md`(新增) | `.specify/templates/docs-target-structure-template.md` | `sync-mirrors.py --check` 中 `templates/` 对报 `ok`(现为 20 文件 → 21),无新 `MISS`/`DIFF`;`diff -q` 字节一致 |
| `skills/create-docs/SKILL.md` | `.specify/skills/create-docs/SKILL.md` | `diff -q` 字节一致;`skills/` 对除既有 `git-fleet` 漂移外无新 `MISS`/`DIFF` |
| `skills/improve-docs/SKILL.md` | `.specify/skills/improve-docs/SKILL.md` | `diff -q` 字节一致;同上 |

> 镜像门禁按实测基线设定:`sync-mirrors.py --check` **当前 exit 2**(无关的既有 `git-fleet` 镜像缺失,详见 Phase 0 发现 7),故本特性的判据是"所触及镜像对报 `ok` 且无新增漂移行",而非命令整体 exit 0。

> 路径重写注意(`src/specify_cli/__init__.py` `rewrite_paths()`):仅 `memory/`、`scripts/`、`templates/`、`shared/` 四个前导段会被改写为 `.specify/<seg>/`。`skills/` **不**被改写(故 `skills/improve-docs/SKILL.md` 在工具副本中原样保留,与既有 `skills/create-docs/SKILL.md` 写法一致);`.specify/docs/` 字面量原样通过,声明路径安全。

## Complexity Tracking

N/A — Constitution Check 14/14 Pass,无违规需论证。

## Phase 0: Research Review & Context

无独立 `research.md`;以下为内部勘察结论(证据路径已实测复核)。

### 探索方式

派 Explore 子代理做定向勘察(命令分发机制 / 既有契约与测试 / 引擎写入面 / 受管声明先例 / 门控与探针治理 / 复杂命令分类 / 参考文档结构),随后对**五项高风险结论**亲自复核命令级证据:门控实测总数、baseline 上限、KEEP_LIST 行、必存字面量计数、improve-docs 措辞原文。非降级路径(子代理一次成功)。

### 关键发现(决定设计的七条)

1. **门控余量为零(最强约束)**:实测 `total: 23` vs SC-002 上限 `23.25`。新增任一阻塞门控即测试红。→ 设计上以"零新增门控、新确认并入既有 R4 干跑计划"规避;不采取修改 `baseline.json` 的补偿路径(Feature 047 曾用该路径,此处无必要)。
2. **`improve-docs` 无门控探针**(仅 wrap-up 对象 `skill-improve-docs-wrapup`);`create-docs` 有 2 个(`gate-create-docs-tiered-disposition`、`gate-create-docs-write-plan`);`/speckit.docs` 无任何 `gate-docs-*` 对象。→ 本特性零新增探针,内容分发的确认由 create-docs 既有计划门控覆盖(FR-011 要求门禁原样保留)。
3. **`.specify/templates/commands/` 已退役且被测试断言缺席**;命令模板只有 4 个生成副本(`.hermes`/`.codex` 目录在本仓不存在)。→ 镜像义务表按实测枚举,不写不存在的镜像。
4. **受管声明的最佳先例是 `.specify/git-workflow.md`**:HTML 注释成对标记 + "只替换标记之间内容"写入规则 + `assets/` 骨架模板 + 专用契约测试 + 别处只留指针。→ 声明沿用该形态;骨架改放 `templates/`(制品模板家族,`<name>-template.md` 约定,镜像对已存在),避免给"自称无 assets"的 create-docs 新开资产目录。
5. **`docs-utils.py` 无任何持久配置读写**(`REGISTRY`/`ALLOWED_SPECIAL` 为硬编码常量,唯一扩展点是每次运行的 `--allow-special`),且 `.specify/docs/` 不被任何轮转/清理逻辑覆盖(`sanitize-utils.py` 的 `MATERIAL_ROOTS` 不含该路径)。→ 声明落此处天然满足 FR-002a"不随按次产物轮转";引擎零改动。
6. **既有 033 契约有 6 条需修订(5 条行为修订 + 1 条事实纠正)**:C-1(镜像措辞与测试相反)、C-4a(单技能 SoT → 技能对)、C-5(四件产物 → 五件)、C-7(保留 thin-dispatch 字面量并容纳编排)、C-18(improve-docs 入分发链路);C-8 的 `13→14` 计数在规划时实测为 18 complex / 4 simple；合并上游 `derive` 后分类 owner 为 19/4(`docs` 始终已在复杂集,本特性不改分类)。
7. **镜像基线已实测,存在一处无关既有漂移**:`sync-mirrors.py --check` **当前 exit 2** —— `git-fleet` 技能在 `skills/` 存在但 `.specify/skills/` 缺 6 个镜像文件(上游提交 `fe70862e` 引入),另有 14 条 `.migration-backups/` 镜像侧独有的 `note`(非失败)。本特性将触及的四对镜像实测全部 `ok`(`templates/` 20 文件、`agents/`、`scripts/` 101 文件、`shared/` 32 文件)。→ 本特性的镜像门禁定为**"所触及镜像对无新增漂移"**而非笼统 exit 0;修复 `git-fleet` 漂移不属本特性范围。

### 技术决策(Technical Context 已据此填定)

| 决策 | 结论 | 理由 |
|------|------|------|
| 声明路径 | `.specify/docs/target-structure.md`(工作区**根级单文件**) | FR-001 已定归属面;根级文件与按次子目录 `plans/`、`audit/` 天然可区分,满足 FR-002a 且无需新建目录层 |
| 声明形态 | Markdown + 成对 HTML 注释受管块 | 沿用 git-workflow 先例;标记外内容字节保持,便于人工加注而不冲突 |
| 声明写入方 | LLM(命令编排),**非引擎** | 守 Out of Scope"不新增独立引擎/脚本"与原则 IX;引擎化管理无必需性 |
| 声明骨架 | 新增 `templates/docs-target-structure-template.md` | 与 constitution/plan/requirements 等制品模板同族;`specify init` 自动装到下游项目 |
| 三段落位 | 全部在 `## Outline` 内作为阶段 | 保 6 章节枚举不变(C-3 免修订);守"新需求是同一引擎的新输入"纪律 |
| 新增门控 | **0** | 声明批准/回写/重设计提议/扇出告知全部并入既有 R4 干跑计划;符合"可逆动作自动执行 + 执行报告"判据,且门控余量为零 |
| 引擎改动 | **0** | 声明完整性由契约测试钉(git-workflow 同款做法),不新增 action(避 docs-utils 契约 C-1 变更) |

## Phase 1: Design Artifacts Summary

*(落盘后核实回填,2026-09-01)*

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | `data-model.md` | 3 实体(目标结构声明 / 调协动作 / 分发批次)+ 4 件既有产物复用说明 + 1 个声明状态机 + 13 条验证规则映射 |
| Contracts | `contracts/` | 3 份:`docs-command-orchestration.md`(D-1…D-12)、`target-structure-declaration.md`(T-1…T-10)、`action-routing.md`(A-1…A-9)= 31 条款 |
| Quickstart | `quickstart.md` | 6 场景(Bootstrap / 稳态零收敛 / 双类漂移 / 带参叠加 / 隐含结构变更回写 / 大规模扇出告知与中止)+ 回归核验清单 |
| Feature binding | `feature-ref.md` | Feature 037 第四次 follow-up 映射 + 状态处理偏离说明 + 5 项注册义务清单 |

**核实结果**: 实际产出与 Phase 0 预期零漂移(实体 3、条款 12/10/9、场景 6 均如期)。契约思维痕迹扫描(`Wait —`/`Actually,`/`Hmm,`/`I think` 等 10 类标记)零命中。`quickstart.md` 回归清单中的 5 条 shell 命令已实跑核验(4 条引擎命令 + pytest collect-only);6 个 `/speckit.docs` 场景留待实现阶段做命令表面的人工验证,不得在此前宣称已执行。
