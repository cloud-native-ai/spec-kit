# Implementation Plan: 快速失败纪律——异常分流而非静默兜底(Fast Fail)

**Branch**: `052-fast-fail-principle` | **Date**: 2026-09-23 | **Spec**: [requirements.md](./requirements.md)
**Requirement → Feature**: `052-fast-fail-principle` → Feature 052 快速失败纪律(Fast Fail)
**Input**: Specification from `.specify/specs/052-fast-fail-principle/requirements.md`

## Summary

把框架今天分散在十余个互不引用点位上的"停下来"规矩,收敛成一条**有名、有真源、有守卫**的纪律:执行期发现与已记录预期不符的状态时,按「解决它需要**纠正**还是需要**裁定**」二值分流——只需纠正且局部可逆的顺手修完并在收尾披露,需要裁定的停在异常点、把四要素上送件交用户裁定。两份封闭清单(fast fail / 顺手修复)的首版条目全部取自本仓已实测的失效(盲检四成因、`git diff` 三形态、`&&` 链空转、脚手架覆盖、两顶帽子错位、两振停滞),不用假想案例。

技术路径与 Feature 040(Token Efficiency)、051(User-Facing Comprehension)同形,故**工件形态一律照 051 的最新约定**:纪律真源文档落 `shared/guidelines/fast-fail.md` 并镜像到 `.specify/shared/guidelines/`;指令模板新增**顶级** `## Fast Fail Discipline` 常驻章节(增量调谐只按整章节传播);宪章模板新增原则 XIV + 宪章命令 `MUST include` 清单新增条目构成**双落点**,活动宪章新增原则 XVI 并 MINOR 递增到 1.13.0;新增契约守卫 `tests/contract/test_fast_fail_discipline.py`,并同批上调三处既有钉子。

**本特性独有的一面是子代理派发注入**:子代理的提示派生自其 Agent 定义与派发载荷、**不来自编排者的对话**(`shared/definitions/subagent-definitions.md:13`),团队上下文隔离规则另把"不传对话历史给子代理"定为有意屏障——所以常驻层结构性到不了子代理,规则必须在**派发那一刻物理注入**。控制点只有两个:派发之前(自检子句在场)与回传之时(显式异常行,使沉默不可被读作干净)。

**最硬的机械约束是门控预算整数余量为 0**:扫描器实跑 `total = 23` 且被既有契约测试钉成**相等**(钉子集合的数目与形态由 `contracts/gate-neutrality.md` C-10 单点拥有,本文不重抄),而本特性全部新增文本都落在扫描面内。处置取**设计规避**(零命中措辞 + 扫描器零改动),不扩大豁免集。已实测草稿注入子句 8 行 / 933 字节 / `BLOCKING_RE` **0 命中**。

**零新增机制、零引擎改动**:观察闭环复用既有反馈引擎与既有 probe;注入是调用方的内容义务,不改派发包装器;不新增共享 agent 资产目录、不新增 probe 类或对象、不新增面向用户界面类。

## Technical Context

**Language/Version**: Python `>=3.8`(per `pyproject.toml`);纪律真源文档、常驻章节、宪章原则、注入子句均为 Markdown 文本制品,无编译期。
**Primary Dependencies**: `pytest`(带 `contract` marker,见 `pyproject.toml` → `[tool.pytest.ini_options]`)。**零新增运行时依赖**;复用既有引擎且**不修改**:`sync-mirrors.py`、`regen-command-copies.py`、`generate-instructions.sh`、`scan-confirmation-gates.py`、`feedback-utils.py`、`skills/create-team/scripts/dispatch.sh`。
**Storage**: 文件制品。新增 1 份纪律真源文档 + 1 份其 `.specify/` 镜像副本;新增 1 个契约测试文件。无数据库、无状态存储、无新增台账或注册表(FR-007 的范围限制子句禁止)。
**Testing**: `pytest -m contract`。新增 `tests/contract/test_fast_fail_discipline.py`(承载 FR-035 的 22 项封闭断言集);**上调三处既有钉子**:`test_constitution_double_landing.py` 的 `TEMPLATE_COUNT` 13→14、`LIVE_COUNT` 15→16、`COMMAND_COUNT` 7→8、`MIN_VERSION` (1,12)→(1,13);`test_user_facing_comprehension_doc.py:400` 的 C-14 去重规则真源路径数 8→9。回归判据取**名字级**(`run-tests.sh --names-out` + `comm -13` 输出为空),不取条数级。
**Target Platform**: 任意宿主 AI agent CLI(Claude Code / Codex CLI / Qoder CLI / opencode / Hermes Agent / GitHub Copilot)。纪律文本 MUST 项目中立(不含 `spec-kit` / `specify-cli` / `specify_cli` / `cloud-native-ai`),以便随包发布到任意下游项目。
**Project Type**: 代码生成器 / 框架(`templates/`、`scripts/`、`src/<package>/`、`shared/`、`skills/`、`agents/`)。本特性只改文档制品与测试,不改 `src/specify_cli/`。
**Performance Goals**: 注入子句 **≤ 10 行 且 ≤ 1,200 字节**(D-2;实测草稿 8 行 / 933 字节)。理由:子句随每一次派发复制,6 成员团队一轮 ≈ 5.6 KB;而活动指令文件实测 28,168 B、预算 32,768 B、余量仅 4,600 B。
**Constraints**:
- **门控预算中立(硬约束)**:全部新增文本对 `BLOCKING_PATTERNS` 逐行零命中;`scan-confirmation-gates.py` 零改动;实跑 `total` 与冻结基线 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json`(`total: 23`、`integerHeadroom: 0`)**相等**。钉子集合(位置、形态、各自的解除路径)由 `contracts/gate-neutrality.md` C-10 单点拥有,本文 MUST NOT 另抄一份数目——实现期已实测该数目为**三**而非规划期记的二,漏计的第三处是"派生上限"形态,grep `== 23` 找不到它。
- **两处已实测的必踩陷阱**:① 相邻纪律的中文名「确认门控治理」逐字命中 `确认门[禁控]`,故真源文档 MUST 以**路径**指称它;② 停止语义 MUST 用「停在异常点并上送用户裁定」这类形态,MUST NOT 用「等待用户确认」「stop and confirm」「确认后执行」「确认门禁」「explicit user confirmation」。
- **常驻章节插入位置受两处既有守卫约束**(D-1):`test_c8` 断言 `Token Efficiency < UFC < Dogfooding` 的**严格排序**(非相邻),`test_c7` 断言 Documentation Map / Proactive Flow Trigger / Fact Checks 三节连续。裁定插在 UFC 之后、Dogfooding 之前。
- **镜像基线已有漂移**:`sync-mirrors.py --check --only shared` 改前实测 **EXIT=2 / 恰 2 条 DIFF**(`.specify/shared/workflow/feedback-step.md`、`runtime-mode.md`),二者先于本特性。故判据取"改后仍是这同 2 条、无新增",**MUST NOT** 取绝对判据(EXIT=0)——那在本仓不可通过。
- **`fail-fast` 词序不可用**:反序在权威源上有 9 处占用、跨三种语义;本纪律取 `fast-fail`(该系列字面量框架目录零命中)。
- **三个稳定字面量 MUST 互不为子串**(FR-063):`[fast-fail]` / `fast-fail-clause` / `ANOMALY:` / 纪律路径,六对组合已逐一实测零违规(D-5、D-6)。
**Scale/Scope**: 1 份新真源文档(9 个 H2 节,D-10);`shared/guidelines/` 12 → **13** 份;指令模板 `## ` 章节 18 → **19**(活动文件 19 → 20);宪章模板原则 13 → **14**;活动宪章原则 15 → **16**、版本 1.12.0 → **1.13.0**;命令 `MUST include` 条目 7 → **8**;Per-Agent Payload 字段 5 → **6**;出厂 Agent 预设 **2** 份各携一份子句副本;新增契约测试 **1** 个文件、上调既有钉子 **5** 处;收敛既有实例点位 **十余处**(FR-029 点名者,各加一行指针,正文不改)。

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**Core Principles Compliance** (rendered from `.specify/memory/constitution.md`,15 principles enumerated in source order — no hard-coded list, no inheritance from a prior spec's plan):

| # | Principle | Compliance | Evidence |
|---|-----------|------------|----------|
| I | Specification-Driven Development (SDD) as Foundation | ✅ Pass | 本计划完全由 `requirements.md`(78 FR / 15 SC / 13 STR)驱动;每条设计决策在 `research.md` D-1…D-17 中回溯到具体 FR |
| II | Feature-Centric Development | ✅ Pass | 绑定 Feature 052(`Draft`,本轮推进为 `Planned`);`feature-ref.md` 载 FR→契约条款映射;注册表义务已于 clarify 轮履行 |
| III | Intent-Driven Development | ✅ Pass | 意图链完整:用户原始描述 → 追加输入(逐字记录) → 4 项 clarify 裁定 → 3 项 plan 裁定(D-2/D-3/D-4),无一处设计是凭空发明 |
| IV | Test-First & Contract-Driven Implementation | ⚠ Partial — see Complexity Tracking | `contracts/` 五份先于实现落地,条款与 `test_*` 函数名一一对应;但本计划的契约描述**部分**制品尚不存在,red-first 取证须在实现期完成 |
| V | AI Agent Integration Standards | ✅ Pass | 纪律文本项目中立(FR-008,守卫断言 `FORBIDDEN_NAMES`);注入义务对 native / virtual / external 三种执行模式同等成立(FR-057);不绑定任何宿主专有能力 |
| VI | Continuous Quality & Observability | ✅ Pass | 观察闭环以 `[fast-fail]` 标记经既有引擎检索(FR-040);SC-015 的三个数全部由既有存据导出,零新增计数器(D-16);干净运行也 MUST 显式说一句(FR-067),使"因干净而空"与"因未受治理而空"可区分 |
| VII | Specification-Plan-Task-Implementation Workflow | ✅ Pass | `requirements.md` → `research.md` + `plan.md` → `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md` → 待 `/speckit.tasks` |
| VIII | Code as the Single Source of Truth | ✅ Pass(经一次订正) | 全部数值锚点于本日实跑重算(D-17 十一项逐一核对相符);计划期内测得的两处上游陈述错误(`test_c8` 非相邻而是严格排序;`fail-fast` 占用 5→9 处)均按源码订正并记入 `research.md`。**委托评分曾判本行 Partial**:Phase 1 摘要印的派生命令 `grep -c '^## 场景'` 实跑得 10 而非所印的 9(该模式同时匹配 `## 场景覆盖表`)——与本文件自己记录的漂移①同类。已订正为带 `[0-9]` 的模式并实跑复核得 **12**,见下方 Re-check |
| IX | Framework Scope Discipline (No Over-Engineering) | ✅ Pass | 零新机制:FR-007 的范围限制子句点名拒绝异常检测引擎、分流评分器、成熟度报告、台账/注册表;不新增 probe 类或对象、不新增界面类、不改任何引擎源码 |
| X | Documentation Naming & Location Conventions | ✅ Pass | 真源文档落 `shared/guidelines/fast-fail.md`(kebab-case,与既有 12 份同形);制品落 `.specify/specs/052-fast-fail-principle/`;无新增顶级目录 |
| XI | Dogfooding (Self-Application) | ✅ Pass | 本特性自身受本纪律约束:clarify 轮的 4 路委托检测按本规格正在规定的形态注入了子句并要求显式异常回传行,三路回传 `ANOMALY:`、一路回传"no anomaly";两处自身缺陷(3 条未被引用的 STR、一个凭记忆写成 20 实为 19 的计数)由机械复核而非阅读发现并订正 |
| XII | Tool Reuse Over Ad-Hoc Generation | ✅ Pass | 零新脚本代码;复用 6 个既有引擎且不修改;`.specify/memory/tools/` 下无值得提升为 Tool 的新重复能力 |
| XIII | Better-Harness Orientation (Improvement North Star) | ✅ Pass | 本纪律直接服务前馈侧:把"错误被就地修平、用户看不见、下游当已验证前提引用"这一失效模式变成可判定、可守卫、可观测的规则;清单双向生长规则(FR-044)+ 过度触发度量(SC-015)构成其反馈侧 |
| XIV | One Source of Truth (Authority & Reference Discipline) | ✅ Pass | 分流判据、两份清单、注入子句字面量、处置集、爆炸半径定义均单点拥有于真源文档;五处相邻纪律一律以指针接入(FR-028);子句副本属"守卫钉死的合法重复"且以成对定界符使字节相等可机械断言(D-9);计数一律派生不手写 |
| XV | User-Facing Comprehension (No Jargon, With Context) | ✅ Pass | 上送件归界面类 **⑪ 失败如实报告**(D-4 显式登记并上调 051 的 C-14 钉子 8→9);真源文档携 canonical 指针行(FR-074);四要素 + 封闭处置集(FR-068)使读者不打开其他工件即可选择;SC-008 的通过条件已从"标题齐备"改为"能选出一项并说明理由" |

**Gates Status**(Phase 0 初评): ⚠ 1 项 Partial(Principle IV) — 见 Complexity Tracking;其余 14 项 Pass,无 Fail。

**Gates Status**(Phase 1 后委托重评,2026-09-23): ⚠ 1 项 Partial(Principle IV,维持) — 委托评分另将 Principle VIII 判为 Partial,其唯一依据(一条印出的派生命令实跑不副)已在本轮订正并复核,故重评后为 **14 Pass / 1 Partial / 0 Fail**;订正过程与委托评分的完整结论见下方 Re-check 段,**未把该次降级悄悄抹掉**。

**Re-check after Phase 1**: 2026-09-23 — Phase 1 五份设计制品(`research.md` / `data-model.md` / `contracts/` ×5 / `quickstart.md` / `feature-ref.md`)落地后重评。

**同作者条件成立**(本计划与其全部设计制品由同一 agent 在同一会话写成),故按 `objective-analysis-gate.md` 把两次自评分**委托给新鲜上下文只读子代理**:一个重评 Constitution Check 的 15 行,一个执行 Post-Generation Quality Gate。两个简报都点名了同作者条件、要求"假定合规主张偏乐观并找出站不住的那些",并按本特性正在规定的形态注入了 fast-fail 子句与显式异常回传行要求。二者均回传了 `ANOMALY:` 行。

委托重评结论(逐项复核后采纳):

| 面 | 委托结论 | 处置 |
|---|---|---|
| 原则枚举完整性 | 活动宪章 15 条,计划表 15 行,**同序、无遗漏、无上一份规格的残留** | 采纳,无需改动 |
| Principle IV(Test-First) | **维持 Partial,不是 Fail**——依据是宪章 Principle VII 自身规定"仅模板类特性判 Test-First 为 Partial(justified)";107 条条款先于实现落地,且诚实区分了制品类/行为类 | 采纳;Complexity Tracking 已载明,**破坏面为 `tasks.md`**(MUST 承载 red-first 与变异演练的取证任务) |
| Principle VIII(Code as SSOT) | **降为 Partial**:5 项抽查中 4 项复现,1 项不复现——Phase 1 摘要印的 `grep -c '^## 场景'` 实跑得 **10** 而非所印 **9** | **已订正**:模式加 `[0-9]`,实跑复核得 **12**(补齐三条缺失演练后的新值);摘要与覆盖表同步更新 |
| Principle XIV(One Source of Truth) | Pass,但**披露**两处双重枚举:封闭处置集同时在 `data-model.md` E6 与 `discipline-doc.md` C-17(b) 全文列出;子句长度上限同时在 `data-model.md` E12 与 `dispatch-injection.md` C-5 | 采纳其判定(契约侧属"钉在测试里的字面量"这一合法重复,数据模型侧引用了 D-15/D-2 裁定,二者无分歧);**新增锁步义务**:任一处改动 MUST 同批改另一处,已记入下方遗留义务 |
| Principle III(Intent-Driven) | Pass,但**薄弱点**:三项 plan 期裁定的"经用户裁定"归属只存在于 `plan.md` 散文,无 Q→A 制品痕迹 | **已订正**:`research.md` 的 D-2 / D-3 / D-4 各增一行"裁定方式",记录提问轮次与全部选项 |
| Principle XI / XV | 二者均为**earned 而非装饰性**(逐条与带日期的反馈记录、UFC 类表与 C-14 钉子核对) | 采纳 |
| Gates Status 行 | 与表内一致,但按重评**少报一项** | 已改为双行(初评 / 重评),不覆盖初评记录 |

Post-Generation Quality Gate 的委托结论与处置:

| 发现 | 材料性 | 处置 |
|---|---|---|
| `quickstart.md` 场景 8 的清理命令**不可用**:`--action cleanup` 实测要求 `--package`(`feedback-utils.py:1389` 抛 `FeedbackError`),`dispose` 只翻元数据不删文件;照初版执行会把演练条目**永久留在真实存据**,从而伪化基线总表第 18 行的 `count: 0`,让下一个执行者撞上一条他自己没造成的基线冲突 | **材料** | 已改为 `--workspace-root` 一次性隔离,**并于 2026-09-23 实跑验证**(隔离根内 `count: 1`、真实存据仍 `count: 0`、`rm -rf` 后目录不存在);场景内并加一条反空真哨兵断言真实存据未被污染 |
| `dispatch-injection.md` C-24 要求**四条**演练场景,而 `quickstart.md` 只有一条 ⇒ FR-066 / FR-055 / FR-067 无取证路径 | **材料** | 已补场景 **10 / 11 / 12**,场景数 9 → **12**;覆盖表与 SC-013/SC-014/SC-009 的取证指向同步更新 |
| 场景 6 **演练了错误的对象**:C-24 第 1 行指定通道一的 outgoing 提示,初版却拿通道二的 Agent 预设配 `grep` 演练,只证明了可检测性、未触及"派发前"这一时序 | **材料** | 已重写:从**拥有者**取子句写入一份模拟 outgoing 提示再演练;并显式声明时序属性属程序性义务、由评审强制,本场景 MUST NOT 声称已证明它 |
| `discipline-doc.md:107` 对 FR-026 / FR-027 / FR-028 的归属**与 `feature-ref.md` 矛盾**(前二者其实无任何条款,FR-028 由本文件 C-7 承载) | **材料** | 已订正,并把"未覆盖 FR 清单"的唯一拥有者指回 `feature-ref.md`,本文件 MUST NOT 另列一份 |
| `gate-neutrality.md` C-1 引用的扫描器输出行 `blocking confirmation gates: 23` **自身命中** `confirmation gate` 模式;而 C-14 要求把已接受代价写进真源文档(在扫描面内)⇒ 原样粘贴会使 total +1 并打爆 C-10 枚举的全部钉子 | **材料** | 已新增 **C-1(a)**:该引文 MUST NOT 被复制进任何被扫描的文件;真源文档载明代价时 MUST 用散文,同一约束适用于 C-7 列出的 17 个模式字面量 |
| `feature-ref.md` 的覆盖统计命令实跑得 85 而非所印 78(主映射表与"未覆盖"表各含一次那 7 条 FR) | **材料** | 已订正为去重命令并实跑复核得 **78**;7 条再分两档(3 条完全无条款 / 4 条仅节级或间接) |
| 三处引用漂移:`ambient-section.md` 的 `PARAM_PATTERNS` 行号 `:69`(实为 `:65`,使用点 `:170`)、`dispatch-injection.md:77` 的裸 `C-19`(应为 `ambient-section.md C-19`)、`discipline-doc.md:95` 的未限定文件引用 | 外观 | 三处均已订正 |
| `dispatch-injection.md` C-5 的"实测草稿 8 行 / 933 字节"无可复现命令(草稿不落盘) | 外观 | 已加说明:该三数只是上限的**推导依据**、不是可断言判据;可断言的只有 ≤10 行与 ≤1,200 字节 |
| 基线总表第 18 / 19 行的呈现口径(前者实为多行 pretty-printed JSON,后者"解析该表"未指明按列) | 外观 | 两行均已注明口径;第 19 行明确"按规则真源列取路径,口径同 `test_user_facing_comprehension_doc.py:394-397`,按整行取则得 9,不可混用" |

**25 行改前基线全部复现**:委托方独立重跑 22 条命令覆盖全部 25 行,**无一项与实况冲突**;唯一不复现的是上面那条派生命令(属计划正文,不属基线表)。

**遗留义务(交给 `/speckit.tasks`)**:① `tasks.md` MUST 承载 red-first 与变异演练的取证任务(Principle IV 的 Partial 破坏面);② 封闭处置集与子句长度上限各有两处全文枚举,任一处改动 MUST 同批改另一处;③ `tasks.md` MUST 继承"计数一律由命令派生、派生命令 MUST 实跑"这条——本轮共查出 **3 处**"印了一个派生命令或数字却没有实跑它"的同类缺陷(`feature-ref.md` 的 85/78、`plan.md` 的 10/9、以及被它连带暴露的场景计数),同一根因。

## Project Structure

### Documentation (this spec)

```text
.specify/specs/052-fast-fail-principle/
├── requirements.md      # /speckit.requirements + /speckit.clarify(3 轮)+ /speckit.plan Phase 0 一处字面量回写
├── plan.md              # 本文件(/speckit.plan 输出)
├── research.md          # Phase 0 输出:D-1…D-17,每条附实测证据
├── data-model.md        # Phase 1 输出
├── quickstart.md        # Phase 1 输出
├── feature-ref.md       # Phase 1 输出:Feature 052 绑定与 FR→条款映射
├── contracts/           # Phase 1 输出:5 份
├── checklists/
│   └── requirements.md  # 规格质量清单(3 轮验证,第 3 轮为 operative)
├── tasks.md             # Phase 2 输出(/speckit.tasks — 本命令不创建)
└── verification.md      # 实现输出(/speckit.implement — 本命令不创建)
```

No standalone research.md 的例外**不适用**:本特性的 Phase 0 研究超过 50 行且含大量实测证据,故按 051 约定独立成 `research.md`。

### Source Code (repository root)

```text
shared/guidelines/                 # 新增 fast-fail.md(纪律唯一真源,9 个 H2 节;12 → 13 份)
shared/definitions/                # subagent-definitions.md 增派发期注入义务(与既有可见性契约并列)
templates/                         # instructions-template.md 新增顶级 ## Fast Fail Discipline 章节;constitution-template.md 新增原则 XIV
templates/commands/                # constitution.md 新增 MUST include 条目(7 → 8);agents.md Run Mode 增注入义务(通道二命令侧落点)
skills/create-team/references/     # patterns.md Per-Agent Payload 新增第六字段行 fast_fail_clause(通道三落点)
skills/create-agent/               # SKILL.md 创作契约增"注入子句 MUST 在场"要求(通道二制作者侧落点)
agents/                            # 2 份出厂预设各携一份子句副本(成对定界符包围)
tests/contract/                    # 新增 test_fast_fail_discipline.py;上调 test_constitution_double_landing.py 四钉;上调 test_user_facing_comprehension_doc.py 的 C-14 8 → 9
scripts/                           # 不改动 —— scan-confirmation-gates.py 的 POLICY_DOCS / SELF_REL / BLOCKING_PATTERNS 刻意不动(D-8 取设计规避)
src/specify_cli/                   # 不改动
.specify/                          # 仅再生镜像与指令文件,一律不手改
.claude/ .github/ .qoder/ .opencode/   # 仅再生按工具命令副本与 agent 副本,一律不手改
```

**Structure Decision**: 本特性落在框架既有的"**纪律三表面 + 宪章双落点 + 派发三通道**"形态上,不新增任何顶级目录。三个表面为:真源文档(`shared/guidelines/`)→ 指令模板常驻顶级章节(`templates/`)→ 契约测试(`tests/contract/`);双落点为宪章模板原则 + 宪章命令 `MUST include` 条目;三通道为编排者内联提示(经常驻层抵达,不落制品)、Agent 定义制品(制作者要求 + 2 份出厂预设)、团队 Per-Agent Payload(第六字段行)。唯一的新文件是 `shared/guidelines/fast-fail.md` 与其镜像、`tests/contract/test_fast_fail_discipline.py`,以及本 spec 目录下的 Phase 0/1 制品。

### Mirror Obligations *(mandatory when any changed file has mirrors or generated copies)*

**基线(2026-09-23 改前实测,判据据此写成相对形态)**:
- `sync-mirrors.py --check` 全树:`DRIFT detected`,**EXIT=2**(大量 `.specify/skills/*` DIFF + `.specify/scripts/python/trigger-utils.py` + `.specify/shared/workflow/{feedback-step,runtime-mode}.md`);`agents/ == .specify/agents/templates/ (2 files)` 为 `ok`。
- `sync-mirrors.py --check --only shared`:`scope --only: shared`,**恰 2 条 DIFF**(`feedback-step.md`、`runtime-mode.md`),**EXIT=2**。
- `regen-command-copies.py --check`:列出大量 `.qoder/commands/*` 为待再生(既有漂移)。
- 四棵按工具命令树各 **25** 文件;四棵按工具 agent 树各 **2** 条目(`.claude/agents`、`.qoder/agents`、`.github/agents`、`.opencode/agents`)。实现期订正:实为**四棵**(`.claude/agents`、`.qoder/agents`、`.github/agents`、`.opencode/agents`,各 2 条目);规划期误记为三棵,且把第四棵路径写成单数 `.opencode/agent` 而测得 0;指令兼容性符号链接实测 **4** 条(`AGENTS.md`、`CLAUDE.md`、`QODER.md` → `.specify/instructions.md`;`.github/copilot-instructions.md` → `../.specify/instructions.md`)。

⇒ **判据一律为"本特性触及的对/树上无新增漂移",MUST NOT 用绝对判据**(全绿 / EXIT=0)——既有漂移先于本特性存在,绝对判据在本仓不可通过,写下去就是发运一条没人度量过的判据。

| Source file (edited) | Mirror / generated copies (must land identically) | Verify |
|----------------------|---------------------------------------------------|--------|
| `shared/guidelines/fast-fail.md`(**新**) | `.specify/shared/guidelines/fast-fail.md`(`MIRROR_PAIRS` 的 `("shared", ".specify/shared", False, set())` 全树 rglob 自动拾取,无 manifest) | `sync-mirrors.py --check --only shared` 改后仍**恰为改前那 2 条 DIFF**、无新增行;新测试断言源与镜像 `read_bytes()` 逐字节相等 |
| `shared/definitions/subagent-definitions.md` | `.specify/shared/definitions/subagent-definitions.md`(同上 `shared` 对) | 同上;并断言既有 `## External Dispatch Visibility Contract` 的 5 条编号义务逐字未变 |
| `templates/instructions-template.md` | ① `.specify/templates/instructions-template.md`(`("templates", ".specify/templates", False, {"commands"})` 对);② 再生成的 `.specify/instructions.md`;③ 4 条兼容性符号链接指向该活动文件 | `--check --only templates` 无新增漂移;`generate-instructions.sh` 再生后活动文件 `## ` 节数 19→20 且新章节在 UFC 与 Dogfooding 之间;`test_c7`/`test_c8` 两处位置钉子仍绿;4 条链接仍为符号链接(`test -L`) |
| `templates/constitution-template.md` | `.specify/templates/constitution-template.md`(同上 `templates` 对) | `--check --only templates` 无新增漂移;`test_constitution_double_landing.py` 的 `TEMPLATE_COUNT` 上调为 14 后相等断言通过;新原则块折行 <100 字符 |
| `templates/commands/constitution.md` | `.claude/commands/speckit.constitution.md`、`.github/prompts/speckit.constitution.prompt.md`、`.qoder/commands/speckit.constitution.md`、`.opencode/command/speckit.constitution.md`(经 `regen-command-copies.py`;**无** `.specify/templates/commands/` 镜像——该对已退役) | 再生后 4 份副本各含新条目;`COMMAND_COUNT` 上调为 8 后相等断言通过;`regen-command-copies.py --check` 相对改前**无新增**待再生项 |
| `templates/commands/agents.md` | 同上四棵按工具树的 `speckit.agents.*` | 同上;Run Mode 的既有 4 步序列与 `**Scope boundary**` 逐字未变,仅新增注入义务 |
| `skills/create-team/references/patterns.md` | `.specify/skills/create-team/references/patterns.md`(`("skills", ".specify/skills", False, {"site"})` 对) | `--check --only skills` 相对改前无新增漂移;Per-Agent Payload 表由 5 行变 6 行,Context Isolation Rules 4 条逐字未变 |
| `skills/create-agent/SKILL.md` | `.specify/skills/create-agent/SKILL.md`(同上 `skills` 对) | 同上;既有"六个必备正文节"与 Self-Improvement Contract 恰好一次的要求逐字未变 |
| `agents/skill-verifier.agent.md`、`agents/structure-adjuster.agent.md` | ① `.specify/agents/templates/`(`("agents", ".specify/agents/templates", False, set())` 对);② **四棵**按工具 agent 树 `.claude/agents/`、`.qoder/agents/`、`.github/agents/`、`.opencode/agents/`(各 2 条目)——实现期订正:规划期误记为三棵且把第四棵路径写成单数 `.opencode/agent` 而测得 0;渲染键为 `claude`/`qoder`/**`copilot`**/`opencode`(`.github/agents` 的键是 `copilot`,且未知键静默返回 `rendered: 0`) | `--check --only agents` 改后为 `ok`(改前即 `ok`,2 files);两份预设各含**恰好一对**定界符且区间内文本与真源文档拥有者字面量逐字节相等 |
| `tests/contract/test_fast_fail_discipline.py`(**新**) | 无镜像 | `pytest -m contract` 该文件全绿;全量套件名字级回归 `comm -13 baseline current` 输出为空 |
| `tests/contract/test_constitution_double_landing.py`、`tests/contract/test_user_facing_comprehension_doc.py` | 无镜像 | 上调后各自全绿;`MIN_VERSION` 为下限语义(`>=`),1.13.0 本就通过,上调至 `(1,13)` 是为把下限推到本特性之后 |

**不改动但需再生核验的**:`.specify/instructions.md` 由 `generate-instructions.sh` 按整章节增量注入再生——它**不做**镜像同步(D-17 与 FR-077 的实测依据),故真源文档的 `.specify/` 副本 MUST 由 `sync-mirrors.py` 单独同步,两者顺序不可颠倒(先同步镜像,再再生指令文件,否则常驻章节的指针在再生那一刻悬空)。

## Complexity Tracking

> Principle IV(Test-First & Contract-Driven Implementation)标为 **Partial**,理由与拒绝的更简方案如下。

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Principle IV 判为 Partial:`contracts/` 的五份条款中,相当一部分断言的对象(`shared/guidelines/fast-fail.md`、常驻章节、宪章原则 XIV/XVI、注入子句副本)在本计划写就时**尚不存在**,故 red-first 取证(先看到测试因制品缺失而红、再实现使其转绿)只能在实现期完成,计划期无法给出"已红"的证据 | 这是文档治理类特性的固有顺序:契约条款描述的是制品的**结构性质**(某文件存在、某标题恰好一次、某区间逐字节相等),制品不存在时条款无从断言。051 同形,其 `notes/red-first-evidence.md` 记录了 `28 failed / 6 passed` 且失败原因全为制品缺失(17 × FileNotFoundError + 10 × 标题不存在,零导入错误)——本特性沿用该取证形态 | **"等制品写完再补测试"被拒**:那正是 Principle IV 要防的顺序,且会失去 red-first 的证据力(改前即绿的条款无法证明它能红)。051 的实测教训更硬——其守卫里发现 6 处缺陷、5 处同一形态("一条验证命令返回的答案与它要判的命题无关"),**每一处都靠实跑发现,不靠阅读**;没有 red-first + 变异演练,这类盲检会直接 shipped。**"把 Partial 记为 Pass"亦被拒**:模板要求任何 Partial 有对应的 Complexity Tracking 条目,粉饰为 Pass 会让 `/speckit.implement` 失去取证义务 |

**配套义务(把 Partial 变成可收口的)**:实现期 MUST 为每条守卫负面命题的条款取一次**变异演练**证据(弄坏被守物 → 确认变红 → 复原 → 确认恢复绿),演练用临时文件 MUST 删净并复核计数归零;每条"过滤后集合为空"的断言 MUST 配一条**反空真哨兵**(断言某个相关量非空),使"因正确而空"与"因失明而空"可区分。这两条手法是本仓已实测的既有对策(`docs/reference/history/00-cross-cutting-lessons.md:85-86`),本特性 MUST 援引而非重新发明(FR-015)。

## Feature List Review

**本计划是否引入新 Feature、废弃或合并既有 Feature?**

- **引入新 Feature:无。** Feature 052 已于 clarify 轮创建并登记(索引行 + `features/052.md` + 051 的反向交叉引用),本轮只推进其状态 `Draft → Planned`。
- **废弃 / 合并既有 Feature:无。** 五个被消费的 Feature(028 / 040 / 046 / 051 / 032)能力范围均不变。
- **跨 Feature 交付效应 2 项**(归属在对方、052 为交付方,均需在 `features/<ID>.md` 留痕):
  1. **Feature 051**:D-4 把 `shared/guidelines/fast-fail.md` 登记进其类 ⑪ 的规则真源列,并上调其 `test_user_facing_comprehension_doc.py:400` 的 C-14 钉子 8 → 9。这是**显式列出的跨纪律改动**(FR-024 要求),已在其类映射表中使类 ⑪ 的规则拥有者完整可发现(读者顺表能找到四要素与封闭处置集,不再只看到 `confirmation-gates.md` 的三要素)。
  2. **Feature 050**:门控预算 `total = 23` 的相等钉子由 `test_proactive_trigger_section.py:352` 持有;本特性以设计规避使其**不变**,故不产生交付效应,但**依赖**该钉子继续成立——已记入 052 的约束面。
- **功能 / 非功能分类是否仍一致?** 一致。Feature 052 属**框架纪律类**(与 031 / 032 / 040 / 046 / 050 / 051 同类),非用户可见能力类;其索引行的描述与详情文件的 Status Tracking 均按此归类。
- **上游缺陷 4 项(检出但不修,归属在各自拥有者)**:`feature-integration.md` 的死指针 `memory/feature-index.md` 与状态自相矛盾;其他常驻章节沿用的"刷新指令即恢复镜像副本"假承诺句式(`generate-instructions.sh` 实测无镜像同步);`反空转哨兵` / `反空真哨兵` 词形不一致;`agent-definitions.md:50` 称 "seven shipped role agents" 而实测 `agents/*.agent.md` 为 **2**。另附本轮新检出 2 项:两处裸观察标记(`token-efficiency`、`user-facing-comprehension`)与其纪律路径存在同类子串碰撞;`templates/commands/constitution.md:64-70` 要求 4 段版本号而活动宪章与守卫解析口径均为 3 段/2 段。6 项均已记入 `features/052.md` › Future Evolution Suggestions。

## Phase 0: Research Review

Phase 0 研究独立成文:[`research.md`](./research.md),含 **D-1…D-17** 共 17 条决策,每条附实测证据(命令 + 输出 + 行号)。其中 3 条经用户裁定(D-2 子句上限、D-3 通道三落点、D-4 类 ⑪ 登记),其余由仓库实况与既有先例唯一确定。

**证据路径声明**:Phase 0 的代码库探查**委托给一个新鲜上下文只读子代理**(非降级路径——派发一次即成功)。该子代理按 `objective-analysis-gate.md` 的规则 2 在简报中被点名了"同作者条件",并按本特性正在规定的形态注入了 fast-fail 子句与显式异常回传行要求;它回传了 **2 条 `ANOMALY:`**——一条证伪了简报自身的前提(`.specify/specs/040-*/` 并非 Token Efficiency 的规格目录,实为 `035-token-efficiency/`),一条上送了版本号形态的上游分歧(已裁为 D-7)。两条均已按分流处置:前者为纠正类(就地采用正确目录并披露),后者为裁定类(取 3 段 MINOR 先例并记录分歧)。

**规格假设的确认与推翻**(一轮内完成,不留到设计中途):

| 规格所载假设 | Phase 0 实测结论 |
|---|---|
| `fast-fail` 系列字面量全仓零命中 | **确认**(含 `[fast-fail]`、`ff-triage` 亦零命中) |
| `fail-fast` 被 5 处可写性探针占用 | **推翻并订正**:权威源上 **9 处**,其中 3 处不指可写性探针(clarify 轮已订正) |
| 门控预算 total 23、余量 0 | **确认**(实跑 + 冻结基线 + C-10 枚举的钉子集合;实现期订正为**三**处,漏计的第三处是派生上限形态) |
| 新增 `shared/guidelines/*.md` 被镜像自动拾取 | **确认**(`MIRROR_PAIRS` 全树 rglob,无 manifest) |
| `test_shared_reference_directory.py` 对新 guideline 静默通过 | **确认**(`TYPED_DOCS` 为 `issubset` 断言,无需登记) |
| 常驻章节可插在纪律章节群中任意位置 | **部分推翻**:`test_c8` 是**严格排序**而非相邻(故 UFC 与 Dogfooding 之间合法),但 `test_c7` 的三节连续窗口与 `test_c8` 的排序共同限定了可插区间 → D-1 |
| Per-Agent Payload 字段数无测试钉子 | **确认**(`tests/contract/` 对三个字段名与表本身零命中)→ D-3 可自由新增第六行 |
| 类 ⑪ 登记无需改动既有守卫 | **推翻**:`test_user_facing_comprehension_doc.py:400` 钉死去重路径数**恰为 8** → D-4 需上调为 9 |
| 三个稳定字面量已互斥 | **推翻**:`fast-fail` ⊂ `fast-fail-clause` 且 ⊂ 纪律路径 → D-5 改 `[fast-fail]`;`ANOMALY:` 出现在子句正文 → D-6 改行首锚定 |
| 子句副本可由既有引擎再生 | **推翻**:无引擎再生 `patterns.md` 或 `.agent.md` → D-9 取"守卫钉死 + 手工重灌 + 成对定界符" |

## Phase 1: Design Artifacts Summary

本节于 Phase 1 五份制品**落盘之后**回填(模板要求:never pre-write counts)。下列计数全部由命令派生,派生方式一并给出。

| Artifact | Path | Count / Scope |
|----------|------|---------------|
| Phase 0 研究 | [`research.md`](./research.md) | **17** 条决策 D-1…D-17(`grep -c '^## D-'`),其中 3 条经用户裁定、14 条由仓库实况唯一确定 |
| 数据模型 | [`data-model.md`](./data-model.md) | **19** 个实体标题 E1…E19(`grep -c '^## E'`),覆盖规格 19 行 Key Entities;其中 E5 与 E19 各为一条标题覆盖一对实体,故**实体数为 21**、标题数为 19(该差值由 data-model.md 开头声明,不设第二处计数)。另 **7** 条校验规则 V1…V7、**3** 个状态机 S1…S3 |
| 契约 | [`contracts/`](./contracts/) | **5** 份 / **107** 条条款:`discipline-doc.md` 22、`ambient-section.md` 19、`dispatch-injection.md` 26、`constitution-export.md` 23、`gate-neutrality.md` 17(`grep -cE '^\*\*C-[0-9]+\*\*' contracts/*.md`) |
| Quickstart | [`quickstart.md`](./quickstart.md) | **12** 个场景(`grep -c '^## 场景 [0-9]'`;**MUST 带 `[0-9]`**——不带则同时匹配 `## 场景覆盖表` 而得 13)+ 1 张改前基线总表(25 行实测值)+ 1 张场景覆盖表 |
| Feature 绑定 | [`feature-ref.md`](./feature-ref.md) | FR→条款映射 **78** 行(去重后,与规格 FR 总数相等);其中 71 条条款级承载、7 条列入"未覆盖"表(3 条完全无条款、4 条仅节级/间接);SC→度量映射 **15** 行;交付面清单 **16** 行 |

**条款总数派生**:`grep -cE '^\*\*C-[0-9]+\*\*' contracts/*.md` 逐文件相加 = 22 + 19 + 26 + 23 + 17 = **107**。条款号在**每份文件内独立编号**,故跨文件引用 MUST 写作 `<file>.md C-N`(沿用 Feature 051 的约定)。

**与 Phase 0 预期的漂移**:两处,均已就地订正并记录理由,不留待实现期发现——

1. **`feature-ref.md` 的覆盖统计命令与数值不符**(自查发现):初版写 `grep -cE '^\| FR-[0-9]{3} \|'` = 78,但该文件的主映射表与"未覆盖"表**各含一次**那 7 条 FR,按行计数实得 **85**。已改为去重命令 `grep -oE … | sort -u | wc -l` → **78**,并把 7 条再分两档(3 条完全无条款 / 4 条仅节级或间接)。这是"写下一个派生命令却没有实跑它"的实例——正是本特性 SC-002 与 [[STR-006]] 要治理的形态。
2. **`data-model.md` 的实体数有两个合法口径**(标题数 19 vs 实体数 21,因两条标题各覆盖一对实体):已在该文件开头声明差值来源,MUST NOT 在两处各写一个数字。

**执行核验状态**(plan 命令的 Post-Generation Quality Gate 要求):`quickstart.md` 的 9 个场景中,**改前基线部分的全部命令已于 2026-09-23 实跑**,期望值取自实跑输出(见其"改前基线总表"25 行);**改后判据部分逐场景标注为"改前不可实跑"**并给出改前等价基线——标注是**逐场景**的,不是文件级免责声明。其中场景 4(门控预算中立)的改后判据**在改前即可完整实跑**,因其判据是不变量;场景 8 的三标记互斥性亦然(纯字符串运算,不依赖制品)。

**未被 quickstart 覆盖的 SC 及其取证方式**:SC-001 与 SC-008 要求未参与本特性实现的评审者,单会话不可得,实现期由独立子代理取证,不可得时 MUST 记 `[~]` 并说明、MUST NOT 编造通过率;SC-013 子代理侧与 SC-015 为度量而非门禁;SC-014 为行为类,由场景 6 同款变异演练取证。详见 `quickstart.md` 末段与 `feature-ref.md` › SC 映射表。

