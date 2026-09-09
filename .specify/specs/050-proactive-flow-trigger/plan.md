# Implementation Plan: 主动触发机制(Proactive Flow Trigger)

**Branch**: `050-proactive-flow-trigger` | **Date**: 2026-09-07 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `050-proactive-flow-trigger` → Feature 050 Proactive Flow Trigger
**Input**: Specification from `.specify/specs/050-proactive-flow-trigger/requirements.md`

## Summary

把"用户必须记得 `/speckit.*` 命令名与技能名才能用上框架能力"反转为"框架在每个 agent 的必经指令路径上主动提议下一步流程"。技术取向是**零新增命令、零新增技能、零新增确认门控**:在 `templates/instructions-template.md` 新增一个 `## ` 级章节(紧邻 Documentation Map 的常驻指令,使"先合规、再选流程"成为同一趟分析),章节只承载**摘要 + 指针**;完整纪律落 `shared/guidelines/proactive-trigger.md`(单一真源);确定性部分(情境身份解析、规则匹配、计数、阈值、晋升、漂移检出、遥测)交一个新的 stdlib 引擎 `trigger-utils.py`,语义判断(该不该提、调优提议是否成立)留在 agent;出厂种子规则集以**携带 provenance 的合法副本**形态随 `templates/` 分发,由漂移检出契约测试守卫其与 25 个 `## Handoffs` 散文段的一致性。

顺带闭合一个既有覆盖缺口:`_INSTRUCTIONS_FILE_MAP` 声明 6 条 agent 指令路径而 `generate-instructions.sh` 只生成 4 条(`HERMES.md`、`.opencode/instructions.md` 缺失致 `_check_instructions` 恒 fail)。指令文件既是本特性唯一通道,该缺口即等于这两个 agent 完全没有本机制,故 FR-003 在本计划中是**硬前置**而非整洁性修补。

## Technical Context

**Language/Version**: Python ≥ 3.8(`pyproject.toml` 既有下限),**stdlib only**(argparse / json / pathlib / re / os / sys / datetime);Bash(`generate-instructions.sh` 既有脚本内增量);Markdown(指令章节 + 纪律文档);JSON(种子规则集 + 运行状态)
**Primary Dependencies**: **无新增依赖**。复用既有脚本:`generate-instructions.sh`(additive reconcile + symlink)、`sync-mirrors.py`(镜像扇出)、`run-tests.sh --names-out`(名字级基线比对);`regen-command-copies.py` **不触碰**(本特性不改任何命令模板)
**Storage**: 文件态,两处分离——`.specify/memory/trigger/index.json`(git 跟踪:配置 + 规则集 + 晋升聚合态 + 调优提议)与 `.specify/memory/trigger/telemetry.jsonl`(**git 忽略**:每回合遥测,有保留窗口、可轮转)。种子随包分发于 `templates/proactive-trigger-seed.json`(跟踪 + 镜像)。按**变动频率**切分跟踪边界:规则/配置每会话变数次,遥测每回合变一次
**Testing**: pytest;三层测试面 —— **4 个契约测试文件**(一契约一文件,`tests/contract/`,结构断言)+ **1 个单元测试文件**(`tests/unit/`,引擎纯函数)+ **3 个集成测试文件**(`tests/integration/`,按故事分文件以保 `[P]` 资格)。名字级基线比对(`scripts/bash/run-tests.sh --names-out` + `comm -13 baseline-failed.txt current` 为空);当前最近基线为 `.specify/specs/049-docs-reconcile/baseline-failed.txt`(47 条),本特性开工前须重新冻结自己的 `baseline-failed.txt`。**混合型判定**:Principle VII 的 template-only 门(constitution.md:95)只覆盖本文档/模板制品面(指令章节、纪律文档、种子 JSON → 结构契约测试);`trigger-utils.py` 是**可执行运行时代码**,故 Principle IV 的"Pure functions MUST have unit tests"与"Acceptance scenarios become automated tests"对其完整适用 → 单元测试与集成测试为强制,不得以 template-only 为由豁免
**Target Platform**: 本地 CLI,macOS / Linux(依赖 POSIX symlink);无网络、无运行时服务
**Project Type**: 代码生成器 / 框架(`templates/`、`scripts/`、`src/specify_cli/`)
**Performance Goals**: 每回合引擎调用 ≤ 150ms(wall);每回合 stdout 摘要典型 ≤ 20 行、硬上限 60 行;探测升级率 ≤ 20% 回合数(SC-011);无适用流程回合的用户可见输出 = 0
**Constraints**: ① **确认门控扫描 total 必须保持 23**——`tests/contract/test_confirmation_gates_sweep.py` 断言 `total ≤ baseline.total × 0.25 = 23.25`,**整数余量为 0**,而 `scan-confirmation-gates.py` 的 `SCAN_DIRS` 含 `shared/`、`SCAN_ROOT_FILES` 含 `templates/*.md`,即本特性新增的指令章节与纪律文档**都在扫描范围内**;② 指令章节必须**项目中性**(禁 `spec-kit` / `specify-cli` / `specify_cli` / `Feature 0NN` / 仓库路径字面量,同 `test_task_complexity_rubric.py` C-9);③ `scripts` 镜像对为 **STRICT**(mirror-only 文件报 ORPHAN 并 exit 2);④ additive reconcile 只传播 `## ` 级章节,故新内容必须自成一个 `## ` 章节;⑤ 不新增命令/技能 ⇒ 复杂命令分类(19)、docs-step(16)、probe internal objects(73)**均不变**
**Scale/Scope**: 1 个新 `## ` 章节(+1 镜像)、1 份新纪律文档(+1 镜像,10 个 `## ` 章节)、1 个新引擎(+1 镜像,**11 个 action**,由 `contracts/trigger-engine.md` C-9 钉为封闭枚举)、1 份新种子 JSON(+1 镜像,**13** 条规则覆盖 **13** 个命名情境,派生自 `## Handoffs` 段与少数 owning-section 段落)、`generate-instructions.sh` 增 2 条 symlink 创建、**8 个新测试文件**(4 契约 + 1 单元 + 3 集成)、1 份新 Tool 记录、受控词表 9 阶段 + **12** 信号 + **13** 命名情境

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md` v1.11.0 — 14 principles, dynamically enumerated in source order):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 走完整 spec → plan → tasks → implement;26 FR / 15 SC 全部可追溯到本计划的技术取向与契约文件 |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 050 并完成注册三件套:`features/050.md` 详情、`features.md` 索引行 + 计数 49→50(手工编辑)、相邻 Feature 032 反向交叉引用 |
| III | Intent-Driven Development | ✅ Pass | 设计直接回应用户意图(消除记名负担):P-Q1 裁定管理面也不引入需记忆的命令名,与意图自洽 |
| IV | Test-First & Contract-Driven Implementation | ✅ Pass | Phase 1 先落 **4 份契约**(`contracts/`:trigger-section / trigger-engine / seed-derivation / discipline-doc)再进 tasks;三层测试面(4 契约 + 1 单元 + 3 集成)——引擎是可执行运行时代码,故"Pure functions MUST have unit tests"与"Acceptance scenarios become automated tests"完整适用;TDD 顺序由 `/speckit.tasks` 承接 |
| V | AI Agent Integration Standards | ✅ Pass | 经既有指令面投递,不新增 agent 专属方言;章节项目中性(C-9 式禁用 token);补齐 hermes/opencode 两条声明却未生成的路径,反而**提升**全 agent 一致性 |
| VI | Continuous Quality & Observability | ✅ Pass | 遥测(FR-009②)即本特性的可观测面:SC-011 探测升级率、SC-012 顺序契约均由自产遥测度量,不依赖人工观察 |
| VII | Specification-Plan-Task-Implementation Workflow(含 **Workflow Gates (NON-NEGOTIABLE)**) | ✅ Pass | 本命令只落 `Draft → Planned`;`Planned → Implemented` 的 Pre-Status-Flip Gate(零 `[ ]` 任务 + 每条 SC 在 `verification.log` 有状态行)由 `/speckit.implement` 持有,本计划不代行 |
| VIII | Code as the Single Source of Truth | ✅ Pass | 全部现状锚点经源码实测;本轮探索**推翻并订正**了两处既有记录(spec 的"17 章节"→ 实测 14 个 `## ` 章节;Feature 049 的 sync-mirrors 6 MISS 基线 → 实测已 exit 0 全绿),即以代码为准而非以文档为准 |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | **本计划的核心取向即此原则**:零新命令、零新技能、零新门控、零新依赖;唯一新制品是一个 stdlib 引擎,其必要性由 Program-First 强制(计数/阈值/身份解析/漂移检出都是固定规则判定,不得交给 LLM)。不引入 agent 运行时、调度器或 hook 适配层(首轮 Q1=A 已裁定) |
| X | Documentation Naming & Location Conventions | ✅ Pass | 未占用任何保留文件名(README/ARCHITECTURE/CONTRIBUTING/CHANGELOG);新文件全小写且路径语义化(`shared/guidelines/proactive-trigger.md` = 该主题的纪律、`templates/proactive-trigger-seed.json` = 出厂种子) |
| XI | Dogfooding (Self-Application) | ✅ Pass | 机制落地后即在本仓自身会话中运行;SC-001…SC-015 的度量源明确以本仓 dogfooding 为主;摩擦经既有 Loop A(`feedback-utils.py`)记录,不新增回路 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | **已执行复用门**:查 `.specify/memory/tools/`(9 条记录),最接近的 `feedback-utils.py` 经其 Tool 记录核实**作用域为 feedback 存储 + probe 注册表**,其阈值报告专用于 feedback 提交阈值;把触发计数写入该存储会污染 `--action package` 上行域,故不覆盖本能力 → 新建引擎是预期结果。复用其**范式**(阈值优先级语义)并**新建 Tool 记录** `trigger-utils.py.md`(经 `refresh-tools.sh` 进入 `tools.md` 清单);引擎骨架复用 `derive-utils.py`(最新、含 camelCase 信封 + 原子写 + 分级退出码) |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 本特性**本身就是** harness 改进机制:主动建议是 feedforward,采纳/拒绝记录 + 遥测 + 规则调优是 feedback loop,直接作用于 Agent Work Loop 的"该做什么"维度 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ⚠ **Partial — see Complexity Tracking** | **成立的部分**:指令章节为**摘要 + 指针**(全文归 `shared/guidelines/proactive-trigger.md`);破坏性判据**引用** `confirmation-gates.md` 不复述;纪律文档 C-4 禁止复述种子规则表与信封键集;术语与既有 Feedback Probe / Feedback Introspection 显式区隔;路径计数等易漂移事实已收敛到单一权威条款(`trigger-section.md` C-10)。**不成立的部分(analyze 2026-09-08 订正)**:原记为 Pass 的依据是"种子规则集属 `one-source-of-truth.md` 明列的合法副本类别『a literal pinned in a test to detect drift』"——经逐字核对该指南 §Legitimate duplicates,guard copy 的定义是**"pinned inside a test"**且**"serves the build, never the reader"**,而 `templates/proactive-trigger-seed.json` 是随包分发、被引擎每回合消费、直接面向读者的**运行时制品**,守卫它的是**另一个**文件(`tests/contract/test_trigger_seed_derivation.py`)。它同样不属另两类:非 generator 从 owner 再生(本契约明确禁止散文解析,且规定种子为手写逐字复制),也非 dated record(它在新项目第一天就被当作当前现实消费)。按其 rule of thumb「改一个事实需编辑多个文件即纪律已破」,改写一条 Handoffs 需同时改种子文件及其镜像 → **该副本属 drifting copy,本原则记 Partial**,论证见 Complexity Tracking |

**Gates Status**: ⚠ **13 Pass / 1 Partial(XIV)** — 无 Fail。唯一的 Partial 是 Principle XIV:出厂种子规则集是 `one-source-of-truth.md` 三类合法副本之外的 drifting copy,论证与缓解见 **Complexity Tracking**。按本命令的宪法权威约束,该项**不以重新解释指南的方式清账**;若要把"由漂移检出测试守卫的派生运行时数据"承认为第四类合法副本,须由该指南的 owner 走独立的显式修订。

**Re-check after Phase 1**: 2026-09-07 首次复评记为 14/14 Pass;**2026-09-08 经 `/speckit.analyze` 独立验证后订正为 13 Pass / 1 Partial(XIV)**。订正理由:首次复评的第 ② 点声称"`contracts/seed-derivation.md` 把 provenance + 漂移检出钉为条款,合法副本类别成立"——这是**把"漂移可被检出"误当作"副本类别合法"**;指南的三类合法副本按**制品形态**划分(测试内的字面量 / generator 再生的机械副本 / 不作当前现实引用的 dated record),而种子文件是随包分发的运行时数据,三类皆不符,漂移检出只是**缓解**而非**归类依据**。其余复评要点仍成立:① Principle IX — 契约未引入任何新确认门控,`trigger-section.md` C-6 与 `discipline-doc.md` C-3 把"零 BLOCKING_PATTERNS 命中"钉为条款,门控预算余量 0 得守;③ Principle IV — 4 份契约共 **61 条款**(trigger-section 12 / trigger-engine **23** / seed-derivation 10 / discipline-doc **16**,后两者经 analyze 补强)全部可由对应的 4 个契约测试文件机械断言,引擎运行期行为另由 1 个单元 + 3 个集成测试文件覆盖。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/050-proactive-flow-trigger/
├── plan.md              # 本文件(/speckit.plan 输出)
├── data-model.md        # Phase 1 输出:7 实体 + 状态机 + 校验规则
├── quickstart.md        # Phase 1 输出:6 个端到端走查场景
├── contracts/           # Phase 1 输出:4 份契约(61 条款,含 analyze 补强的 C-19…C-23 与 C-8…C-16)
│   ├── trigger-section.md       # 指令章节形态 + 全 agent 路径覆盖(C-1…C-12)
│   ├── trigger-engine.md        # trigger-utils.py 的 action/信封/状态/语义(C-1…C-18)
│   ├── seed-derivation.md       # 种子规则 schema + provenance + 漂移检出(C-1…C-10)
│   └── discipline-doc.md        # shared/guidelines/proactive-trigger.md 章节与文案安全(C-1…C-7)
├── feature-ref.md       # Phase 1 输出:Feature 050 绑定与映射
├── checklists/
│   └── requirements.md  # 已由 /speckit.requirements + /speckit.clarify 产出并全项通过
├── baseline-failed.txt  # 实现前冻结的名字级失败基线(/speckit.implement 前置)
├── tasks.md             # Phase 2 输出(/speckit.tasks — 本命令不创建)
└── verification.md      # 实现输出(/speckit.implement)
```

**No standalone `research.md`** — Phase 0 findings inlined below(全部为仓库内部调查,无外部来源评估,故不落独立文件)。

### Source Code (repository root)

```text
templates/                            # 出厂分发面(init 时被 copy_local_templates 整体拷贝,commands/ 除外)
├── instructions-template.md          # 【改】新增一个 `## ` 章节(插入 L23,紧邻 Documentation Map 常驻指令之后)
└── proactive-trigger-seed.json       # 【新】出厂种子规则集(每条携带 provenance)

shared/guidelines/
└── proactive-trigger.md              # 【新】触发纪律单一真源(评估节奏/两级证据预算/升级判据/建议形态/晋升语义/遥测与轮转/调优协议/全局开关)

scripts/
├── python/trigger-utils.py           # 【新】stdlib 引擎(11 action,封闭枚举;derive-utils.py 信封与原子写范式)
└── bash/generate-instructions.sh     # 【改】symlink 段(L187–212)补 HERMES.md 与 .opencode/instructions.md 两条路径

src/specify_cli/
└── __init__.py                       # 【核】_INSTRUCTIONS_FILE_MAP(L1090–1097)与生成侧对齐后无需改动;若裁定某 agent 不支持则从此处移除声明

tests/
├── contract/                                    # 一契约一测试文件(避免多故事在同一文件上串行、失去 [P] 资格)
│   ├── test_proactive_trigger_section.py        # 【新】trigger-section C-1…C-12:章节形态/双表面镜像/项目中性/零 BLOCKING/路径覆盖
│   ├── test_proactive_trigger_discipline_doc.py # 【新】discipline-doc C-1…C-7:10 章节封闭集/引用不复述/归属声明/文案安全
│   ├── test_trigger_engine.py                   # 【新】trigger-engine C-1…C-18:信封/退出码/CLI 封闭枚举/每回合语义/晋升与破坏性豁免
│   └── test_trigger_seed_derivation.py          # 【新】seed-derivation C-1…C-10:schema/provenance 可回溯/漂移检出/同构性
├── unit/
│   └── test_trigger_utils_units.py              # 【新】引擎纯函数(Principle IV「Pure functions MUST have unit tests」):情境解析/词表越界/阈值优先级链/遥测行整形/快照长度守卫
└── integration/
    ├── test_trigger_promotion.py                # 【新】US3 端到端:连续采纳晋升/一次拒绝重置/破坏性 10 次采纳零晋升/复位/全局关闭
    ├── test_trigger_telemetry.py                # 【新】遥测有界与轮转零丢失(SC-015)/升级率计算(SC-011)
    └── test_trigger_tuning.py                   # 【新】US4 端到端:提议附证据/小样本守卫/批准前零变更/漏报证据

.specify/memory/tools/
└── trigger-utils.py.md               # 【新】Tool 记录(Principle XII 义务;经 refresh-tools.sh 进入 tools.md 清单)

.specify/memory/trigger/              # 【运行时新建,非本仓提交面】
├── index.json                        # git 跟踪:配置 + 规则集 + 晋升聚合态 + 调优提议
└── telemetry.jsonl                   # git 忽略:每回合遥测(有保留窗口、可轮转)
```

**Structure Decision**: 落在既有的**"代码生成器 / 框架"**形态内,不新增任何顶层目录。四处改动分别是:① 既有模板文件内新增一个章节(`templates/instructions-template.md`);② 三个新文件分别落进既有分发面(`templates/`、`shared/guidelines/`、`scripts/python/`),全部随 init 的既有整体拷贝逻辑自动分发,**无需改 `src/specify_cli/__init__.py` 的拷贝清单**(已核实:`templates/` 走 `iterdir()` 整体拷贝仅排除 `commands`,`shared/` 与 `scripts/` 走 `copytree(dirs_exist_ok=True)`);③ 既有生成脚本内增两条 symlink(`generate-instructions.sh`);④ **8 个新测试文件**落进既有测试树(4 个契约测试 → `tests/contract/`,一契约一文件;1 个单元测试 → `tests/unit/`;3 个集成测试 → `tests/integration/`,按故事分文件以保 `[P]` 资格)。运行时状态目录 `.specify/memory/trigger/` 与既有 `.specify/memory/feedback/` 同层同构,由引擎按需创建。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `templates/instructions-template.md` | `.specify/templates/instructions-template.md`(**字节相同**,sync-mirrors templates 对,lenient,排除 commands/);再经 additive reconcile 注入 `.specify/instructions.md`;再由既有 symlink 抵达 root `AGENTS.md`/`CLAUDE.md`/`QODER.md`/**`HERMES.md`(新)**、`.github/copilot-instructions.md`、`.qoder/project_rules.md`、`.claude/project_rules.md`、**`.opencode/instructions.md`(新)** | `diff -q` 字节相同;`test_instructions_section_propagation.py`(既有)+ 新 `test_proactive_trigger_section.py` C-1/C-10/C-11 |
| `shared/guidelines/proactive-trigger.md` | `.specify/shared/guidelines/proactive-trigger.md`(sync-mirrors shared 对,lenient) | `diff -q` + 新契约 C-1 双表面断言 |
| `scripts/python/trigger-utils.py` | `.specify/scripts/python/trigger-utils.py`(**STRICT 对** — mirror-only 文件报 ORPHAN 并 exit 2) | `sync-mirrors.py --check` exit 0 |
| `scripts/bash/generate-instructions.sh` | `.specify/scripts/bash/generate-instructions.sh`(**STRICT 对**) | `sync-mirrors.py --check` exit 0 |
| `templates/proactive-trigger-seed.json` | `.specify/templates/proactive-trigger-seed.json`(templates 对) | `diff -q` + 新 `test_trigger_seed_derivation.py` C-1 |
| *(不改任何命令模板)* | **无 per-tool 命令副本变动**:`.claude/commands/`、`.qoder/commands/`、`.github/prompts/`、`.opencode/command/` 全部不动;`.specify/templates/commands/` 已退役(templates 对排除 commands/) | `regen-command-copies.py --check` 保持 exit 0(不变即通过) |
| `.specify/memory/tools/trigger-utils.py.md` | `.specify/memory/tools.md`(发现清单,由 `refresh-tools.sh` 再生,**禁手改**);`.specify/tools/{system,shell,project}.json`(同脚本再生) | `refresh-tools.sh --json` 后清单含新 Tool;`generate-instructions.sh` L34–45 的 tools refresh 阶段顺带再生 |

## Phase 0: Research Review

*(findings inlined — 全部经源码实测,由两个并行 Explore 通道采集后逐条复核)*

### D-1 触发段的传播机制:新增 `## ` 章节会自动抵达已初始化项目

`generate-instructions.sh` 的 additive reconcile(L102–129)按 `(?m)^(## .+)$` 切分渲染后的模板,与既有 `.specify/instructions.md` 的 `^## ` 整行集合做差集,**缺失章节按模板顺序锚定插入**(锚点 = 模板中靠后的某个标题在 live 文件里的同名行;否则追加到 EOF),整文件重写但块外字节逐字保留(尾换行归一为 1)。故新增 `## Proactive Flow Trigger` **会**注入每个既有项目的指令文件,无需逐项目手工添加;既有 `## Recurring Operational Lessons`(模板中不存在)不受影响。由 `tests/contract/test_instructions_section_propagation.py` 守卫(C-1 实树、C-2 行为)。

**推论(约束)**:`###` 子节与既有 `##` 章节**内部**的文案改动**不传播**。故触发段的全部内容必须自成一个新 `## ` 章节,不得寄望于改写 Documentation Map 章节内部文字来投递——这直接决定了插入位置只能是"新章节",而 FR-005b 的"紧邻"要求靠**模板顺序**实现(插入 L23,即 Documentation Map 之后、Input Sanity 之前),reconcile 会按该顺序锚定。

### D-2 插入位置与镜像/传播守卫

`templates/instructions-template.md` 124 行、14 个 `## ` 章节;Documentation Map 的常驻指令在 **L22**,故插入点为 **L23**(L22 与 L24 之间)。`.specify/templates/instructions-template.md` 与其**字节相同**(`diff` 为空),由 `sync-mirrors.py` 的 `MIRROR_PAIRS` L67 维持(无专门契约测试断言该对,故新契约需自带字节相同断言,同 `test_task_complexity_rubric.py` C-10 手法)。

### D-3 章节形态:摘要 + 指针,全文归 shared/guidelines/(房式先例)

`test_task_complexity_rubric.py`(139 行,已全文读)确立的形态是:**单一真源文档在 `shared/guidelines/`,指令模板只承载摘要形状 + 指针**,契约把全文钉在文档侧、把摘要形状钉在模板侧。C-1 双表面断言(SRC + MIRROR 都含标题与指针链接)、C-9 **项目中性禁用 token**(`spec-kit`、`specify-cli`、`specify_cli`、`Feature 032`、`cloud-native-ai`)、C-10 字节相同镜像。本计划照此结构:全文 → `shared/guidelines/proactive-trigger.md`,模板章节 → 摘要 + 指针,新契约 `trigger-section.md` 复刻 C-1/C-9/C-10 三类断言。

另一先例 `test_git_workflow_instructions_block.py:33–40` 断言**受管块标记不得出现在指令模板中**、且指针须点名状态文件——本计划同理:触发段只放指针,运行状态与受管内容留 `.specify/memory/trigger/`,满足 FR-002(引用不复制)与 FR-009(状态与指令文件分离)。

### D-4 确认门控预算:整数余量为 0,且新文件全在扫描范围内(最紧约束)

`scan-confirmation-gates.py`:`SCAN_DIRS = ("templates/commands","skills","shared")`(L35)递归 + `SCAN_ROOT_FILES = ("templates",)`(L36)取顶层 `templates/*.md`;`.specify/` 在 `SKIP_DIR_PARTS` 故镜像**不被重复计数**;`shared/guidelines/confirmation-gates.md` 自身被排除(L38)。实测当前 **total 23**(destructive 13 + governance_kept 10)、**violations 0**;`tests/contract/test_confirmation_gates_sweep.py:68` 断言 `total ≤ baseline.total × 0.25`,baseline 取自 `.specify/specs/044-reduce-confirmation-flows/baseline.json`(total 93)→ **cap 23.25,整数余量 0**。

`BLOCKING_PATTERNS`(L46–64,以 `|` 合成 `BLOCKING_RE`)字面量全集:`等待用户确认`、`等待确认`、`用户确认后才`、`确认后才(?:执行|写入|落盘|启动|持久化)`、`显式用户确认|explicit user confirmation`、`wait for user confirmation`、`MUST NOT execute before confirmation`、`stop and confirm`、`after user confirmation|after confirmation`、`[Cc]onfirm before`、`[Pp]roceed[^\n]{0,40}yes/no`、`preview\s*(?:→|->)\s*confirm\s*(?:→|->)\s*execute`、`confirmation gate|确认门[禁控]`、`Confirm and persist|确认并落盘|合并确认`、`Execute on Confirmation`、`interactive confirmation`、`inviting the user to submit collected feedback`。分类降级(`classify()` L106)只在**同一行**含 执行/写入/落盘/启动/继续 时把命中降为 reversible,但**任何命中都计入 total**。`GOVERNANCE_PATH_PATTERNS`(L71–76)按**文件路径**匹配:interview、constitution-template、git-workflow、feedback.md、docs.md、session.md、feature.md、analyze.md、tools.md、operating-loops、project-cluster、gate.yaml、CONFIRM——**新增的 `shared/guidelines/proactive-trigger.md` 不匹配任何一项**,故不享受 governance_kept 豁免。

**裁定(设计规避,不改 baseline、不改扫描器)**:本特性所有新文案(指令章节 + 纪律文档)MUST 零命中上述字面量。可行,因为机制本身即非阻塞:调优批准用「以候选形态呈现,用户批准后写入规则集」「未经用户批准 MUST NOT 变更规则集」(不触发 `确认后才(执行|写入|…)`、`[Cc]onfirm before`、`after confirmation`);破坏性流程的前置确认**引用** `shared/guidelines/confirmation-gates.md` 而不复述其措辞(既满足 Principle XIV 又天然避开字面量);提及治理域名时用路径 `confirmation-gates.md`(连字符)而非 `confirmation gate`(空格)或 `确认门禁`/`确认门控`。该裁定钉为 `contracts/trigger-section.md` C-6 与 `contracts/discipline-doc.md` **C-3**(analyze 2026-09-08 订正:原误引 C-5,而 C-5 是归属声明条款),并在实现收尾复跑扫描器验证 total **等于 T002 冻结的前值**(撰写时实测 23;不硬编码,以免项目侧合法变动时被迫改本计划)(承需求 049 同类处置:以设计规避而非改写 baseline.json)。

### D-5 种子规则:散文不可确定性解析,取"provenance 副本 + 漂移检出"

25/25 命令模板含 `## Handoffs`,其中**条件式**(可派生出 situation→flow 规则)的代表形态(逐字,含出处):

1. `templates/commands/requirements.md:114` — "**After**: If spec has `[NEEDS CLARIFICATION]` or `Related Feature: Need clarification` → `/speckit.clarify`. Otherwise → `/speckit.plan`."
2. `templates/commands/requirements.md:112` — "Optional `/speckit.feature` … **recommended whenever `.specify/memory/features.md` is absent or still a placeholder**"
3. `templates/commands/plan.md:191` — "If `requirements.md` contains any `[NEEDS CLARIFICATION]`, run `/speckit.clarify` first."
4. `templates/commands/analyze.md:245` — "If CRITICAL/HIGH issues found, fix via `/speckit.requirements`, `/speckit.plan`, or `/speckit.tasks` and re-run. Otherwise proceed to `/speckit.implement`."
5. `templates/commands/checklist.md:103` — "If items fail → iterate `/speckit.plan` or `/speckit.tasks`. Once satisfied → `/speckit.implement`."
6. `templates/commands/clarify.md:151` — "Mode A → `/speckit.plan`. Mode B → `/speckit.tasks`. Mode C → `/speckit.implement`."
7. `templates/commands/interview.md:195` — "a converged `requirements.md` → `/speckit.plan`; a converged `plan.md` → `/speckit.tasks`; a converged `tasks.md` → `/speckit.implement`; … anything else → the command that owns the target artifact."
8. `templates/commands/skills.md:36,41` — "If NOT exists … / If EXISTS …"(创建 vs 改进分流)

**同名不同义已核实**:20/25 模板另有 `handoffs:` **frontmatter**,但其条目形状是 `label` / `agent` / `prompt` / `send`——编码的是 **agent dispatch**(如 `instructions.md:4–8` 派 `memory-record`),**不是** situation→flow 条件式;`src/specify_cli/__init__.py:1471` 仅把它当作 `scripts:` 块解析的**终止符 token**,从不消费条目内容(`test_docs_command_template.py:61` 只断言键存在)。故 situation→flow 知识**唯一**存在于散文段。

**裁定(P-Q2=A,经 analyze 2026-09-08 订正)**:散文条件式无法确定性解析,而 Program-First 不允许把散文解析交给 LLM 再称之为"派生"。故取**种子文件一次性撰写 + 每条规则携带 `provenance` + 由契约测试检出漂移**:测试逐条打开 provenance 指向的文件与段落,断言逐字引文与被引流程名都仍在该段内;来源段改写而种子未跟即失败并指名 `ruleId` / `file` / `anchorKind` / 缺失的 `flow`。漂移由**被检出**取代**被防止**。

**订正一(归类)**:原裁定称此形态"落在 `one-source-of-truth.md` 明列的合法副本类别『a literal pinned in a test to detect drift』"——**该归类不成立**。guard copy 的定义是"pinned **inside** a test"且"serves the build, **never the reader**",而种子是随包分发、被引擎每回合消费的运行时制品,守卫它的是另一个文件。三类合法副本均不符,故 Principle XIV 改记 **Partial**,论证与缓解见 §Complexity Tracking(不以重新解释指南的方式清账)。

**订正二(来源两类)**:交叉扫描全部 25 个 Handoffs 段后发现,`/speckit.feedback`、`/speckit.history`、`/speckit.todo`、`/speckit.sanitize`、`/speckit.session`、`/speckit.interview`、`/speckit.research`、`/speckit.derive` 在**任何** Handoffs 段中都不出现。故 `provenance` 增 `anchorKind ∈ {handoffs, owning-section}`:前者取 `## Handoffs` 段,后者取拥有该流程触发条件的段落(如 `/speckit.feedback` 的阈值邀请规则,owner 是 `shared/workflow/feedback-step.md` §Threshold prompt protocol)。FR-022 已同步订正,**实质义务不变**:知识一律来自框架既有文面、零新撰写。

**订正三(13 而非 14)**:初版 14 条 anchor 中 **9 条不成立**(被引段落根本不含所声称的流程名;s14 引的 `skills.md:36,41` 更落在 Handoffs 段之外)。根因是从 8 条已核实样例外推到 14 行而未逐条核验。订正后:7 条改指真实点名该流程的模板(如 `/speckit.checklist` 改指 `tasks.md`、`/speckit.docs` 改指 `sanitize.md`、`/speckit.constitution` 改指 `feature.md`),s14 整条删除(无状态可触发 `/speckit.skills`——`agents.md` 的 Handoffs 是"若 agent 依赖新技能"的**意图驱动**,且保留它会让 `(non-feature, ∅)` 每回合命中,与 quickstart 场景 3 矛盾),s09/s10 转为 `owning-section`。**并把"撰写前逐条机械核验 anchor"固化为义务**(`seed-derivation.md` 实现期义务 ④ + tasks.md T003),否则同类缺陷要等到实现期 C-7 失败才暴露。

**已否决的替代**:给 25 个模板加结构化 frontmatter 键(可得到真正的机械副本)——需改 25 模板 + 再生 100 份 per-tool 副本 + 扩 `src/specify_cli/__init__.py:1466–1473` 的块终止符元组,且与既有 `handoffs:` 键**同名不同义**(那是 agent dispatch),混淆风险高。

### D-6 引擎范式:复制 `derive-utils.py`,阈值语义复用 `feedback-utils.py` 的形状

房式引擎约定(比对 derive/docs/sanitize/feedback/glossary/history-utils.py):单 `--action` 必填 + `choices` 枚举;`--format text|json`;**stdlib only**;workspace-root 解析优先级(显式 > 引擎自定位 `*/.specify/scripts/` > 最近含 `.specify/` 的 CWD 祖先 > CWD);退出码 2 = 校验/用法错误。**最新且最完整的是 `derive-utils.py`**(2026-09-06):`envelope()`(L349–361)返回 `ok` / `action` / `workspaceRoot` / `generatedAt` / `errors[]` / `warnings[]` / `semanticChecksPending[]` / `notes[]` / `payload{}`(**camelCase**,已核实 Feature 049 的记录属实);原子写 `.part` + `os.replace`(L500–506);分级退出码 `EXIT_OK=0 / EXIT_USAGE=1 / EXIT_INPUT_ERROR=2 / EXIT_NOT_FOUND=3 / EXIT_INVALID=4`(L45–49)。注意 `feedback-utils.py` 的 `save_index`(L269–271)**不是**原子写——状态存储照 sanitize/derive,不照 feedback。**一处有意改名**:`derive-utils.py` 的信封键是 `semanticChecksPending`,本引擎改为 `semanticJudgmentPending`(交回 agent 的是**判断**而非待补的语义检查项);实现时照 `contracts/trigger-engine.md` C-3,不要照抄范式源的键名。

**阈值机制复用方式(诚实结论)**:`feedback-utils.py` 的 `DEFAULT_THRESHOLD = 10`(L52)、`should_prompt(count, threshold) = count >= threshold`(L101–102)、`resolve_threshold`(L105–116,优先级 显式 CLI > 环境变量 `SPECKIT_FEEDBACK_THRESHOLD` > 存储 index > 默认)共约 20 行纯函数。文件名带连字符故普通 `import` 失败(`tests/script_api.py:17–32` 用 `importlib.util.spec_from_file_location` 加载),且**当前无任何引擎 import 另一引擎**,而 `scripts` 镜像对是 STRICT 的独立副本——跨引擎 import 会在两个各自独立镜像的副本间建立运行时依赖。故取**复用范式而非复用代码**:本地实现同形状的 ~20 行,环境变量改名 `SPECKIT_TRIGGER_THRESHOLD`,阈值语义(优先级链、`count >= threshold`)与 feedback 域**同构**,满足 FR-021 的"复用既有引擎范式、不新建平行机制"(平行机制指的是**另一套计数语义**,不是另一份 20 行实现)。

### D-7 每回合评估的可负担实现:一次紧凑引擎调用

FR-005a 要求每回合评估、FR-005 要求默认近零证据预算、FR-009② 要求每回合落一行遥测。三者的共同实现是**每回合一次 `trigger-utils.py --action assess` 调用**:agent 只把它从环境上下文已知的**粗粒度信号**作为 flag 传入(如 `--stage requirements --signal needs-clarification`,不做任何文件读取),引擎确定性地解析情境身份、匹配规则、返回建议摘要或显式"无建议",并**顺带追加遥测行**。环境信息不足时 agent 加 `--probe`,由引擎自己跑确定性状态探测并记 `escalated=true`。

该设计把 Program-First 落到实处:LLM 只提供粗观察,**匹配/计数/阈值/身份解析全在程序里**。成本是每回合一次子进程(wall ≤ 150ms),而 FR-005 约束的是**证据/token** 预算(禁注入制品原文),紧凑摘要输出(典型 ≤ 20 行)满足之。遥测因此是**机制自产**而非人工观察,SC-011/SC-012 的分母真实存在(闭合 R2-Q5 发现的缺口)。

### D-8 状态存储与跟踪边界:按变动频率切分

`.specify/memory/trigger/` 与既有 `.specify/memory/feedback/`(index.json + 条目)同层同构。跟踪边界按**变动频率**切:`index.json`(配置 + 规则集 + 晋升聚合态 + 调优提议)每会话变数次 → **git 跟踪**,使用户调优跨 clone 存活(与 `.specify/git-workflow.md`、`.specify/docs/target-structure.md` 同为持久项目契约);`telemetry.jsonl` 每回合变一次 → **git 忽略**(承 `implement-loop.local.md` 先例),避免每回合 churn 污染提交。FR-009a 的轮转只作用于后者,晋升计数作为 `index.json` 里规则上的**聚合态**不受轮转影响(SC-015 据此可测)。

### D-9 接线义务盘点:哪些计数变、哪些不变

| 面 | 是否变动 | 依据 |
|---|---|---|
| 复杂命令分类(19)/ 简单命令(4) | **不变** | `tests/contract/test_feedback_command_classification.py:19–29`;本特性不新增命令(P-Q1=A) |
| docs-step 注入(16) | **不变** | `tests/contract/test_docs_step_injection.py:21–45` |
| probe internal objects(73)/ external(0) | **不变** | `feedback-utils.py --action probes --validate` exit 0;无新命令/技能即无新 wrap-up 单元;机制非阻塞故无新 gate probe |
| per-tool 命令副本(4 树 × 25) | **不变** | 不改任何命令模板;`regen-command-copies.py --check` 保持 exit 0 |
| 确认门控 total(23)/ violations(0) | **必须不变** | 见 D-4;新文案零 BLOCKING 命中 |
| sync-mirrors 五对 | **+4 文件**(2 STRICT) | 见 Mirror Obligations;当前 `--check` exit 0 全绿,**Feature 049 记录的 git-fleet 6 MISS 基线已失效**,故全树 exit-0 门禁可直接用 |
| Tool 记录(9) | **9 → 10** | Principle XII 义务:新引擎须建 `.specify/memory/tools/trigger-utils.py.md`,`refresh-tools.sh` 再生 `tools.md` 与 `.specify/tools/*.json` |
| glossary 词条 | **+8(已落地)** | 本特性两轮已写入 主动触发点/情境评估/建议规则/阈值晋升/触发学习状态/情境身份/回合遥测/种子规则,`validate` 通过 |
| `_INSTRUCTIONS_FILE_MAP` | **不改**(生成侧补齐) | 声明已正确,缺的是 `generate-instructions.sh` 的生成;补齐后 `_check_instructions` 对 hermes/opencode 由 fail 转 pass |
| 基线失败数(47,来自 049) | **须重新冻结** | 本特性开工前跑 `run-tests.sh --names-out baseline-failed.txt` 冻结自己的基线 |

### D-10 遗留未决(不阻塞 plan,交 tasks/implement 处理)

- **受控词表的具体取值集**:`data-model.md` 给出初版(**13** 个命名情境,analyze 2026-09-08 由 14 收敛——删除无状态可触发的 s14),但 FR-023 规定扩展只经用户批准通道,故初版取值属**可修订数据**而非契约常量;契约只钉"身份取自封闭词表 + 跨会话稳定 + 禁止临场造词"。
- **遥测保留窗口的具体数值**:`data-model.md` 给默认值(200 回合)并声明可配置;SC-015 钉"行数不超过已声明窗口",不钉具体数字。
- **探测升级判据的具体规则**:FR-005 要求"显式声明",`data-model.md` 给出判据表;SC-011 钉比率上限 20%。

## Complexity Tracking

> Constitution Check 有 1 项 Partial(XIV),故本节必须论证。

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| **Principle XIV**:`templates/proactive-trigger-seed.json` 是 situation→flow 知识的**第二份副本**,不属 `one-source-of-truth.md` 的三类合法副本(非测试内字面量、非 generator 再生的机械副本、非 dated record),按其 rule of thumb「改一个事实需编辑多个文件即纪律已破」成立 | FR-022 要求新项目**第一天即产出建议**(无冷启动),这需要在 init 时就有一份可被引擎消费的规则数据;而该知识的 owner 是 25 个命令模板的 `## Handoffs` **自然语言散文段**(+ 少数流程的 owning-section 段落)。散文不可确定性解析,而 Program-First(Principle IX / 需求 040)禁止把散文解析交给 LLM 再称之为"派生" —— 故无法用 generator 产出机械副本,只能落一份**携带 provenance 的手写派生副本** | ① **不 ship 种子、纯靠学习积累**:新项目第一天零建议,与本特性目的("用户不记得命令名也能用上框架")自相矛盾,P-Q2 已否决。② **给 25 个命令模板加结构化 frontmatter 键**(可得到真正的机械副本):需改 25 模板 + 再生 100 份 per-tool 副本 + 扩 `src/specify_cli/__init__.py:1466–1473` 块终止符元组,且与既有 `handoffs:` 键**同名不同义**(那是 agent dispatch),混淆风险高;P-Q2 已否决。③ **正则启发式解析散文**:脆弱,改措辞即静默漏规则,且以"确定性派生"之名行不可靠解析之实。④ **运行时由 agent 每次读 Handoffs 自行判断**:每回合注入 25 个模板的散文,直接违反 Summary-First 与 FR-005 的证据预算 |

**缓解措施(使分歧"响亮"而非"静默"—— 这正是 XIV 所要防的失效模式)**:
1. **声明不拥有**:流程知识的 owner 仍是各命令模板的 `## Handoffs` 段与 `owning-section` 段落;种子文件在 `discipline-doc.md` C-4 与 `seed-derivation.md` §明确不属于本契约的事 中被显式剥夺 owner 资格。
2. **每条规则携带 provenance**(`file` / `anchorKind` / `anchor` / `quote` 逐字引文),使副本的每个断言都可回溯到 owner 的具体段落。
3. **机械漂移检出**:`seed-derivation.md` C-6/C-7 断言 `quote` 为来源段落的逐字子串、且规则的 `flow` 值仍出现在该段落内;失败信息指名 `ruleId` + `file` + `anchorKind` + 缺失的 `flow`。owner 一改,测试即红。
4. **维护义务入纪律**:`discipline-doc.md` C-16 ① 把"改 Handoffs 必同步种子、修复方式是同步而非放宽测试"写成常设义务。
5. **撰写前机械预检**:`seed-derivation.md` 实现期义务 ④ + tasks.md T003 要求在写种子前逐条核验 13 个 anchor(该义务来自 analyze 的实测教训:初版 14 条 anchor 有 9 条不成立)。

**残留代价(诚实记录)**:改写一条 Handoffs 事实仍需编辑 2 个文件(种子 + 其镜像),XIV 的 rule of thumb 未被消除,只是把"静默分歧"换成"响亮失败 + 明确的修复指向"。**若项目希望彻底消除该 Partial**,正路是由 `one-source-of-truth.md` 的 owner 显式增列第四类合法副本("由漂移检出测试守卫的派生运行时数据"),那是一次独立的宪法/指南修订,不在本特性范围内(本命令的宪法权威约束禁止以重新解释指南的方式清账)。

**值得记录的反向事实**:除上表这一项外,本计划的取向是主动**收缩**制品面(零新命令、零新技能、零新门控、零新依赖、零 `src/` 逻辑改动),唯一新引擎的必要性由 Program-First 强制。另一处真正的紧约束不是复杂度预算,而是**确认门控整数余量为 0**(D-4)——它以"文案措辞"的形式出现,已用设计规避而非改写 baseline 化解。

## Phase 1: Design Artifacts Summary

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Data model | [`data-model.md`](./data-model.md) | **7 实体**(情境身份 / 建议规则 / 建议事件 / 回合遥测 / 晋升态 / 触发学习状态 / 主动触发点)+ 2 状态机(规则 active→suppressed→promoted;调优提议 proposed→ratified→applied)+ 受控词表(**13 命名情境**、9 生命周期阶段、**12** 待处理信号)+ 探测升级判据表 P1–P5 + **6 组 / 32 条**校验规则(V1…V6,含 analyze 补的 V1.5/V1.6 最具体优先解析、V2.5 标识符文法、V3.4 record 关联、V4.5 度量边界、V5.1…V5.4 晋升态不变量、V6.7/V6.8 会话级抑制) |
| Contracts | [`contracts/`](./contracts/) | **4 份 / 61 条款**:`trigger-section.md`(C-1…C-12)、`trigger-engine.md`(C-1…**C-23**)、`seed-derivation.md`(C-1…C-10)、`discipline-doc.md`(C-1…**C-16**)。C-19…C-23 与 C-8…C-16 由 analyze 2026-09-08 补,把此前只有散文承载的 FR-005…FR-020 义务变成可机械断言的条款 |
| Quickstart | [`quickstart.md`](./quickstart.md) | **6 场景**(全 agent 路径覆盖 / 冷启动首日建议 / 每回合静默与探测升级率 / 阈值晋升与破坏性豁免 / 遥测轮转零丢失 / 漂移检出与调优批准) |
| Feature binding | [`feature-ref.md`](./feature-ref.md) | Feature 050 Proactive Flow Trigger(Draft → **Planned**);映射 26 FR / 15 SC → 4 契约 → 制品面 |
| Research | *(无独立文件)* | Phase 0 findings inlined above(D-1…D-10);全部为仓库内部实测,无外部来源评估 |

**与 Phase 0 预期的漂移**:**有,且由 `/speckit.analyze`(2026-09-08)检出后订正**。三处实质漂移:① 契约条款 47 → **61** —— 十余条 FR 原先只被 `feature-ref.md` 映射到断言**结构属性**的条款(双表面、章节集、文案安全),义务本身落在无编号散文里,故补 `trigger-engine.md` C-19…C-23 与 `discipline-doc.md` C-8…C-16;② 命名情境 14 → **13**、信号枚举 9 → **12** —— 初版词表有 3 处身份冲突(s03/s13 同为 `(no-spec, ∅)`、s05/s06 子集关系无消歧规则、s14 与 quickstart 场景 3 直接矛盾),且 14 条 provenance anchor 中 **9 条不成立**;③ Principle XIV 由 Pass → **Partial**(见 Complexity Tracking)。根因是同一处:受控词表与种子派生表是从 8 条**已核实**的 Handoffs 样例外推到 14 行、而未逐条机械核验其余各行。订正后 13 条 anchor 已全部实测复核(见 `data-model.md` §命名情境表),并把"撰写前机械核验每条 anchor"固化为 `seed-derivation.md` 实现期义务 ④ 与 tasks.md T003。D-10 的三项遗留仍按预期留在 `data-model.md` 的可修订数据层,未被误钉为契约常量。
