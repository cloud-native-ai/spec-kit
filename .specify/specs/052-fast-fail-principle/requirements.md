# Requirements Specification: 快速失败纪律——异常分流而非静默兜底(Fast Fail)

**Requirement Branch**: `052-fast-fail-principle`
**Created**: 2026-09-22
**Status**: Draft
**Input**: User description: "在整个框架中增加fast fail原则, 在使用agent执行动作的时候发现不符合预期的部分应该快速失败而不是强行进行修复继续执行,导致错误的逻辑没有及时被用户发现,进而逐步扩散到整个系统中. 这里的关键是需要区分哪些错误是可以顺手修复的,哪些错误是需要明确知会用户进行确认的. 可以维护一个fast fail列表, 随着使用通过feedback和自省机制逐步进行完善和提升."

## Related Feature *(mandatory)*

**Feature ID**: 052  
**Feature Name**: 快速失败纪律(Fast Fail)

绑定依据(clarify 2026-09-22 Mode A,用户裁定):**新建 Feature 052**,Status = `Draft`,不绑定既有 Feature。按 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules 的**同胞吸收启发式**逐个核验候选后,结论是**无既有 Feature 拥有本需求引入的能力**:

| 候选 Feature | Status | 同胞 specs | 与 052 的实际关系 |
|---|---|---|---|
| 028 Feedback Mechanism | Implemented | **3**(027/041/047) | 注册表中**同胞吸收能力最强**的候选,但三个同胞讲的都是反馈机制本身;052 只**消费**其引擎与自省路径,且 FR-040/FR-043/FR-046 明令不扩展其引擎能力、probe 类与自省入口——绑入会名不副实 |
| 046 Confirmation Gate Governance | Implemented | 1(044) | 052 消费其执行报告与门控观察协议,但 FR-028 判定二者**正交**(门控治理按动作可逆性裁授权;本纪律按发现是否证伪前提裁继续),且明令不向其治理保留清单增行——绑入与本规格方向相反 |
| 051 User-Facing Comprehension | Implemented | 1(自身) | 052 消费其界面类封闭集(FR-023/FR-024)且 MUST NOT 扩展之;是**被消费的拥有者**,不是超集 |
| 040 Token Efficiency Discipline | Implemented | 1(035) | `features/040.md:59` 把它记为 051 的「最接近的结构先例」,而 051 当时被判**新建而非绑定**——这是本形态(纪律真源文档 + 常驻章节 + 契约守卫)在注册表中的**既有裁定先例** |
| 032 Task Complexity Rubric | Implemented | 1(031) | 同为经指令文件非破坏投递的行为纪律,却各自成为独立 Feature(`features/032.md:18` 亦判新建)——确立"以指令段形式嵌入是**投递事实**,不是**归属事实**" |
| — one-source-of-truth / ask-record-repeat / self-improvement / objective-analysis-gate | — | — | 这四份纪律真源文档**在注册表中没有对应 Feature 行**,故无一可吸收 052 |

决定性先例是 **040 与 032**(以及据其裁定的 **051**):投递载体与文件形态与本需求完全相同,却都各自成为独立 Feature。此外 052 引入既有 Feature 范围均不覆盖的持久面——**分流判据与机械测试**、**两份封闭清单**、**派发期注入义务与派发前自检**、**异常回传行**——归属新建。上表候选以**交叉引用**(消费关系)记入 `.specify/memory/features/052.md`,不构成归属。

> **编号巧合声明**:Feature ID `052` 与需求键 `052-fast-fail-principle` 数值相同纯属巧合——两者是**独立编号空间**(Feature 注册表 ID vs 规格目录键),互不派生、互不覆盖。
>
> **上游缺陷(不属本特性修复范围,如实上报)**:`feature-integration.md` 自相矛盾——`:33` 的状态机规定 `/speckit.requirements` 为 `(none) → Draft or keep existing`,而 `:68` 的整合职责规定 `keep Status at least Planned`。本轮取**更具体的一方**(状态机逐命令列出了 `/speckit.requirements` 这一行),故写 `Draft`;该选择在 `/speckit.plan` 阶段本就会翻为 `Planned`,可逆且低爆炸半径。同文 `:58,68` 指向的 `memory/feature-index.md` **不存在**,真实注册表是 `.specify/memory/features.md`。两处均建议单独修订该拥有者文档。

## Overview

框架今天**已经在很多点位要求 agent 停下来,却从未定义"什么时候该停、什么时候可以顺手修完继续"**:实测在 `templates/commands/`、`shared/`、`skills/` 中找到十余处彼此独立、互不引用的停止/上报规则(可写性探针、前提证伪回写、门控判定不得绕、非并行任务失败即停、两振停滞升级、只读命令缺件即中止、标记不配对即停、悬空引用不得静默降级),而**真源文档数量为 0**,`fast fail` / `快速失败` 作为一条纪律的名字在仓库中的出现次数也是 0。

后果不是"没有规矩",而是**规矩只存在于它被写下的那一个点位**:

- 同一类异常在 `implement` 里 MUST 停,在别的流程里没有对应条款,于是被就地修掉;
- 修掉的痕迹不进任何报告,用户看不见;
- 看不见的错误逻辑被下游工件当作已验证的前提继续引用,**逐层扩散**。

本仓最贵的一类缺陷正是这个形状的实例。`docs/reference/history/00-cross-cutting-lessons.md` §十二 记录了四种已实测成因:一条 `git diff --stat | grep -E '\.(py|sh)$'` 在 6 个提交、16 个真实新增 `.py` 上命中数**恒为 0** 而无人察觉;一条 `git diff HEAD` 断言在洁净检出下**无条件通过**;一条可达范围小于命题范围的检查把未跟踪新增脚本**静默放过**;一条瞄准错误树的守卫在运行时副本被移走后**仍报 `1 passed`**。四次的共同点不是"检查失败",而是**检查成功了,而那次成功不是关于它被写来判定的那个命题的**。§十二 自己的判词是:「看着绿的假通过比红着更贵——红会被人修,绿会被下游当证据引用。」

**这就是本需求要闭合的失效:静默兜底(silent fallback)。** `shared/patterns/explicit-implicit-pattern.md:89` 已经给这个反模式起了名字,但它的处置规则只覆盖"隐式推断"这一种形态,不覆盖执行期发现的异常。

本特性把这条无名规矩**命名、定界、并给出可判定的分流判据**:

1. **定名与定源**:在 `shared/guidelines/` 建立唯一真源文档 [[STR-002]],命名该纪律为 **Fast Fail(快速失败)** [[STR-008]],并按三层表面模式(真源文档 → 指令文件常驻顶级章节 [[STR-003]] → 契约测试 [[STR-007]])使其常驻可见、可守。
2. **给出分流判据(本需求的关键)**:用户明确要求区分"可以顺手修复的"与"需要明确知会用户的"。判据 MUST 落在**可判定**的形态上——不是"错误有多严重",而是「**解决它需要谁的意图**」:只需**纠正**(恰有一种与已记录意图一致的读法)→ 顺手修复并在收尾披露;需要**裁定**(在多种读法间选择,或发明任何工件都未记录的意图)→ 快速失败。配一条第三方可复现的机械测试 [[STR-005]]。
3. **维护两份封闭清单**:fast fail 清单( MUST 上送的异常类)与顺手修复清单(MAY 就地修完的异常类),均**保守、可枚举**,扩展 MUST 只经修订真源文档。清单首版以本仓已实测的失效为种子(盲检四成因、空转链、脚手架覆盖、两顶帽子错位、两振停滞)。
4. **让它随使用生长**:复用既有反馈引擎与既有 probe,以稳定观察标记 [[STR-001]] 积累证据,配一条**提升规则**(观察达阈值或经一次用户直接纠正 → MUST 提升进清单,原处措辞 MUST 收敛为指针),并明令 MUST NOT 静默调参直到出现有利结果。
5. **在派发子代理的那一刻就把规则注入进去**(2026-09-22 追加输入,用户点名**重点关注**):子代理是这条纪律最尖锐的失效面,因为**常驻层根本到不了它**——`shared/definitions/subagent-definitions.md:13` 明写子代理的提示与配置「derived from its **Agent Instance** definition … plus its dispatch config … or dispatch payload, not from the orchestrator's conversation」,`:14` 又明写它「receives exactly one task brief … never the orchestrator's full history」,而 `skills/create-team/references/patterns.md:105-109` 的上下文隔离规则更是把「NO conversation history passed to child agents」定为**有意设置的屏障**。⇒ 一个未被注入的子代理不是"可能不守规矩",而是**结构性地收不到规矩**;它启动后即不受编排者中途干预,唯一的控制点是**派发之前**与**回传之时**。本特性因此要求:注入子句 MUST 在派发时就物理存在于子代理读得到的地方;派发前 MUST 自检该子句确实在场;回传 MUST 带一条显式异常行,使"因为干净所以没报"与"因为没收到规则所以没报"可区分。

**两个落地层(用户输入为理念级材料,此处按可落地切片拆分)**:

- **层 A — 框架自身**:真源文档 + 常驻章节 + 两份清单 + 契约守卫 + 与四条相邻纪律的边界落位 + 既有分散实例收敛为指针 + 门控预算中立 + **子代理派发注入(三条派发面:内联提示 / Agent 定义制品 / 团队载荷)**。
- **层 B — 下游项目**:经 `templates/constitution-template.md` 新增原则 [[STR-004]] + `templates/commands/constitution.md` 的 `MUST include` 清单**双落点**导出,使每个下游项目 bootstrap 即得,并自动进入其 `/speckit.plan` 门控的动态枚举。

### 现状锚点(以源码实测为准)

> 本节数值均为 2026-09-22 实测。他处一律以指针引用而不复述字面量;守卫 MUST NOT 钉死本节中的计数(宪章原则数除外——该数由既有双落点测试拥有并 MUST 同批上调,见 FR-032)。

- **停止/上报规则分散在十余个点位,互不引用**(本纪律今天的**事实**分布):
  - `templates/commands/implement.md:45` `**Writability pre-probe (fail fast)** … do NOT let a phase discover an unwritable target mid-run.`——已按 ENOENT / EACCES 区分修复类,是全仓最接近"分流"的既有形态;
  - `templates/commands/implement.md:47` `re-measure before acting, and write a premise falsified by execution back into the task row / upstream artifact instead of silently working around it.`——**最强的单条先例**,但作用域仅 implement;
  - `templates/commands/implement.md:51` `exit 3 (gate unreadable) → surface the problem, do not silently proceed. The gate verdict is mechanical — never argue around it in prose.`;
  - `templates/commands/implement.md:73` `Halt on non-parallel task failure; for [P] continue successful, report failed`;
  - `templates/commands/implement.md:102` `**Stagnation two-strike** … Two consecutive strikes → STOP and escalate (something is structurally blocked; more iterations won't fix it).`;
  - `templates/commands/todo.md:171` `If a task fails, stop and report — do NOT continue to subsequent tasks`;
  - `templates/commands/analyze.md:57` `Abort with an error message if any required file is missing`;
  - `templates/commands/docs.md:38` `On missing, unpaired, or unparseable markers, stop and request repair or explicit rebuild authorization; never overwrite the whole file.`;
  - `templates/commands/docs.md:56` `MUST NOT truncate or silently defer the tail … announce the full document count so the user can **abort before dispatch**.`;
  - `templates/commands/clarify.md:47` `If no requirements.md at all → abort`;`:76` `**Escalation**: … stop and recommend /speckit.interview … Do not silently exceed the cap, do not fabricate the remainder`;
  - `templates/commands/interview.md:84` `if it cannot be resolved, stop and ask for it rather than interviewing against a vague subject`;`:152` `**Surface conflicts; never resolve them silently.**`;
  - `shared/patterns/interview-pattern.md:218` `A non-zero exit is a **verdict** — report it, never argue around it.`;
  - `skills/create-team/references/create-mode.md:26` `**Dangling reference** … zero artifacts, zero writes — MUST NOT silently degrade to inline goal creation.`;
  - `skills/draw-diagram/SKILL.md:62` `**不得**静默降级、**不得**即兴用本地工具…自渲染绕过.`;
  - `scripts/python/regen-command-copies.py:26` `Fail fast with a pointer to the canonical copy instead of crashing mid-run.`
- **输入侧已有两级升级规则,但只覆盖"行动前"**:`templates/instructions-template.md:47-48`(镜像于 `.specify/instructions.md:56-57`)`If the suspected error impacts correctness, security, data loss, or large refactors: **pause and ask a clarifying question**.` / `If the issue is low-risk and the fix is obvious: proceed with the correction and mention it briefly.`——**这是本纪律分流判据的直接形态先例**,但其作用域明写为 `Fact, Correctness & Logic Checks (Input Sanity)`,即**消费输入与继承前提之前**;它不覆盖"动作已执行、异常已出现"的执行期。`:41` 另有 `**Inherited premises**: … is also a hypothesis, not a fact — re-measure it … before acting on it`。
- **确认门控治理与本纪律正交,且不管中途异常**:`shared/guidelines/confirmation-gates.md` 全文两级判据(`:11-12`,按**动作**可逆性裁"是否需前置授权")、破坏性动作清单(`:16-23`)、治理保留清单(`:25-43`)、存疑从严(`:45-47`)、回流约束(`:49-54`)、执行报告(`:56-70`)、门控观察协议(`:72-101`)。与执行期异常沾边的只有两处:`:68` `**失败如实报告**:自动执行中途失败 MUST 报告失败点、原因与已产生的中间产物,MUST NOT 静默跳过或掩盖.`(**只要求报告,不给分类判据**),与 `:47` `宁可多一次确认,MUST NOT 多一次不可撤销的损失。`
- **门控预算整数余量为 0(最硬的机械约束)**:`scripts/python/scan-confirmation-gates.py` 实跑 `total = 23`(destructive 13 + governance_kept 10)、`violations = 0`;冻结基线 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json:15-21` 载 `"total": 23`、`"integerHeadroom": 0`、`"cap": 23.25`。其 `SCAN_DIRS = ("templates/commands", "skills", "shared")`、`SCAN_ROOT_FILES = ("templates",)` ⇒ **本特性的新增文本(真源文档在 `shared/`、常驻章节与宪章原则在根级 `templates/*.md`、以及 FR-062 的两个结构性落点 `skills/create-team/references/patterns.md` 与 `shared/definitions/subagent-definitions.md`)全部落在扫描范围内**;`SKIP_DIR_PARTS` 含 `.specify` 故镜像不重复计数。
  - **计数单位是"命中的行",不是"文件"或"门控"**:`scan()` 逐行 `if not BLOCKING_RE.search(line): continue` 后 `gates.append(...)`,故**任何被扫描文件里的任何一行只要含一个阻塞模式就 +1**;`classify()` 再按 `GOVERNANCE_PATH_PATTERNS`(含 `constitution-template`,故宪章模板中的命中归 `governance_kept`)与 `DESTRUCTIVE_KEYWORDS` 分类,但**两类都计入 total**。
  - **由此推出本特性最尖锐的一个陷阱(clarify 2026-09-22 第二轮实测发现)**:`BLOCKING_PATTERNS` 含 `r"confirmation gate|确认门[禁控]"`,而本规格 FR-012 与 FR-028 **要求**真源文档写出相邻纪律的名字「**确认门控治理**」——该词含 `确认门控`,**逐字命中**。`shared/guidelines/fast-fail.md` 不在 `SELF_REL`、也不在 `POLICY_DOCS`(现恰 2 项:`reconcile-pattern.md`、`interview-pattern.md`),而 FR-037 禁止扩大该豁免集。⇒ **照本规格原文写边界一节,total 会从 23 变 24,直接打爆 FR-038 的相等断言。** 唯一合法出路是措辞规避:真源文档 MUST 以**路径**(`shared/guidelines/confirmation-gates.md`)而非中文名指称该相邻纪律——路径中的 `confirmation-gates` 带连字符,不命中 `confirmation gate`(空格形态)。此约束已由 FR-036 承载。
  - **守卫强度**:`tests/contract/test_proactive_trigger_section.py:338` `test_c11_gate_scan_total_unchanged` 以 `:352` `assert payload["total"] == frozen["total"]` 钉死**相等**(断言消息自陈 `the integer headroom on the budget is 0`),`tests/contract/test_confirmation_gates_sweep.py:161` 另有 `cap = baseline["total"] * 0.25`(044 基线 total 93 ⇒ cap 23.25)。词汇表已把这条约束登记为 `门控预算整数余量 (Gate Budget Integer Headroom)`,并记载 Feature 050 与 051 均撞上它;`设计规避 (Design Avoidance)` 条记载了房子对它的既定处置。
- **房子对该约束的既定处置是「设计规避」而非扩大豁免**:词汇表 `设计规避 (Design Avoidance)` 条记载——Feature 050 的两份新文案做到零 `BLOCKING_PATTERNS` 命中并钉为契约条款;Feature 051 沿用,`.specify/specs/051-user-facing-comprehension/plan.md:20` `处置取**设计规避**(零命中 + 测试钉死),而非扩大扫描器豁免集`,`:36` `scan-confirmation-gates.py 的 POLICY_DOCS **不修改**`,`contracts/gate-neutrality.md:13` 断言 `POLICY_DOCS`、`SELF_REL` 字面量与 `len(BLOCKING_PATTERNS) == 17` 均未变,`:65` 要求 `total == 23` 且 `violations == []` 以**相等**断言。取舍依据(词汇表原文):扩大豁免集会掩盖其中真实门控回流,豁免面过宽。⇒ **本特性 MUST NOT 把新真源文档加进 `POLICY_DOCS`;MUST 以零命中措辞写作。**
- **封闭清单 + 扩展规则有四个房子先例**:
  - `shared/guidelines/confirmation-gates.md:18` `保守、可枚举;扩展 MUST 以修订本文档的形式进行,MUST NOT 分散到各命令模板:`(双清单形态:破坏性清单 + 治理保留清单);
  - `shared/guidelines/user-facing-comprehension.md:90` `本纪律约束的界面类为**封闭集**(closed set):扩展 MUST **只经修订**本文档,MUST NOT 分散到各命令模板自行增类。`;`:19` `**白名单之外的行话一律按违规处理**——不存在「尽量少用」这类不可判定的中间档`;`:26` 黑名单**提升规则** `该清单 MUST 被提升进本节 … 提升后原处 MUST 收敛为指针,MUST NOT 保留第二份独立黑名单`;
  - `shared/guidelines/token-efficiency.md:28` `数据访问按三级逐级放宽,**MUST NOT 跳级**`;`:38` `本节是该阈值的**唯一定义点**,他处仅引用`;
  - `shared/guidelines/one-source-of-truth.md:29` 经验法则(可当机械测试用) `**if changing the fact would require editing more than one file, the discipline is already broken**`;`:33` 三类合法重复;`:51` `On finding a stale count, **remove the copy; do not correct the number**.`
- **盲检类已有配套手法,可直接作为清单条目的判据**:`docs/reference/history/00-cross-cutting-lessons.md:85` **变异演练(mutation drill)** `凡守卫负面命题的用例,取证 MUST 含一次「把被守物弄坏 → 确认变红 → 复原 → 确认恢复绿」的实跑`;`:86` **反空转哨兵(anti-vacuity sentinel)** `凡断言"过滤后的集合为空",在同处再断言一个**必须非空**的伴生量`;`:72` 自问句 `**被守物真的坏掉时,这条会不会变红?** 答不上来就是没写完`。两条手法与自问句均已在词汇表登记(`盲检 (Blind Check)`、`反空真哨兵 (Anti-Vacuity Sentinel)`)。**词形说明**:教训正文用 `反空转哨兵`,而词汇表 canonical 为 `反空真哨兵`、`反空转哨兵` 登记为其 variant;本规格引文保留原词形,正文一律用 canonical(按词汇表协议的变体→canonical 映射,此为一处**上游不一致**,建议单独修订教训正文或词汇表二者之一)。§十三 另记 `git diff` 三形态陷阱与 `&&` 链空转(`grep -c` 零命中退出码 1 → `链会静默中断,其后的提交动作根本不会发生,而检查本身还报告成功`)。§十四 记 `create-new-plan.sh` 无条件覆盖 `plan.md`(代码侧守卫 `scripts/bash/create-new-plan.sh:56-59`)。
- **观察标记机制有两个活先例**:
  - `shared/guidelines/token-efficiency.md:54` `对应优化点条目行 MUST 内嵌字面量 **`token-efficiency`**(稳定标记,供 feedback-utils.py --action list --contains token-efficiency 检索聚合…)。干净运行 MUST NOT 追加空洞观察条目。`,并禁止编造数值;载体是 `shared/workflow/feedback-step.md` 的 Reflect 步;
  - `shared/guidelines/confirmation-gates.md:72-101` §门控观察协议:`:76` 时机(裁定后记录,MUST NOT 替用户作答)、`:78-83` 记录字段(`gate_id` / `fired_during` / 一句话上下文 / 决定信号 ∈ approved-as-is · modified · asked-questions · denied)、`:98-101` 红线(只自动记录、不追加提问、不阻塞宿主、记录失败 MUST NOT 使宿主流程失败)。
- **引擎侧无需改动**:`scripts/python/feedback-utils.py` 已支持 `--action list --contains <marker>`(`action_list:664`,`:691-696` 大小写不敏感子串匹配 summary 与条目全文,`:701-703` 按新到旧返回);`--action` 全集含 `record / status / list / dispose / mark-submitted / reindex / package / cleanup / upstream / probes / map / migrate-legacy / probe-inject / introspect-register`。自省入口已存在:`templates/commands/feedback.md:101-115` 的 Path A3(报告落 `.specify/memory/feedback/introspection/<report-id>.md`,`--action introspect-register` 校验,违规退出码 2)。证据泳道由 `skills/collect-evidence/` 提供。
- **提升规则的证据资格判据已有拥有者**:`shared/guidelines/self-improvement.md:42` `Direct user correction is valid assisted evidence. It does not need repeated occurrence`;`:56` `Changes MUST be minimal and reversible`;`:86` `and MUST NOT silently tune until a favorable result appears.`——本纪律的提升规则 MUST 引用其资格判据,MUST NOT 另立一套。
- **相邻纪律的边界必须显式落位,否则构成复述**:`shared/workflow/objective-analysis-gate.md:27` `**Subagent-unavailable fallback** … Never let the fallback pass silently as the delegated path.`(降级不可静默冒充);`shared/guidelines/task-complexity-rubric.md:19` 需求不明本身即 High-stakes 信号,`clarify before proceeding rather than guessing`;`shared/guidelines/ask-record-repeat.md:28` `当一个**吃重**的事实未知或有歧义时,提问;不要猜`,`:44` `猜错最贵的地方不是错本身,而是**错得很安静**`,`:40` `只有一个合理答案、且改动可逆的,直接做并在报告里说明所采用的解读`(**顺手修复极的既有表述**),`:15` 自陈这些是理念而非机械可判规则,`:86` 三层表面模式,`:117` `给一条规矩新增表面时,MUST 同批加守卫`;`shared/patterns/reconcile-pattern.md:52` **Tolerance band**(阈值内差异标 `consistent (tolerated)`,永不进入收敛计划),`:95` R5(任一 `mv` 失败 → 停余下、保已成、记录、请人复核)。
- **常驻暴露通道的硬约束**:`scripts/bash/generate-instructions.sh:131-136` 只把**模板中存在而活动文件中缺失的顶级 `## ` 章节**整体注入,`:120-122` `never renders the template over it and never modifies or removes existing sections`;机制在 `:177` 按 `^(## .+)$` 切分、`:180` 取缺失集、`:186-192` 按模板序插入;守卫 `tests/contract/test_instructions_section_propagation.py:35,46`。`shared/guidelines/proactive-trigger.md:3` 已明写结论:指针不依赖在既有章节内部新增一行,因为增量调谐只按整章节传播。⇒ **本纪律 MUST 以新增顶级 `## ` 章节暴露;只往文档地图表加一行不会抵达任何已初始化项目。**
- **宪章双落点与四个硬钉子**:`templates/constitution-template.md` 现有 **13** 条原则(I–XIII,`:14`–`:169`),其中三条援引 `shared/guidelines/` 文档(IX `:98`、XII `:143` 引 `one-source-of-truth.md`、XIII `:169` 引 `user-facing-comprehension.md`);单条结构为 `### <罗马数字>. <Title>` → 以冒号结尾的主张句 → 携 MUST / MUST NOT 的 `- ` 要点(含一条 guidelines 指针要点与一条"不新增机制"要点)→ 空行 → `Rationale:` 段;折行宽度 <100 字符(`tests/contract/test_constitution_double_landing.py:167`)。`templates/commands/constitution.md` 的 `MUST include` 清单现有 **7** 条(`:77,87,91,100,111,126,137`);`:66` 规定新增原则 = **MINOR** 递增。活动宪章 `.specify/memory/constitution.md` 现有 **15** 条(I–XV,`:27`–`:168`),版本 `:254` `1.12.0`。守卫测试的四个钉子 MUST 同批上调:`TEMPLATE_COUNT = 13`(`:65`)、`LIVE_COUNT = 15`(`:66`)、`COMMAND_COUNT = 7`(`:67`)、`MIN_VERSION = (1, 12)`(`:68`,下限语义而非相等)。`templates/plan-template.md:37` 明写 `Do NOT hard-code principle names here`,按 `### <numeral>. <name>` 动态枚举(`:40` 每条渲染一行)⇒ **新原则一旦进入宪章即自动抵达每次 `/speckit.plan` 门控,plan 模板无需改动。**
- **镜像与副本机制无需注册**:`scripts/python/sync-mirrors.py:77` 的 `MIRROR_PAIRS` 含 `("shared", ".specify/shared", False, set())`,`:86` 以 rglob 发现全部文件(`:83` 是其所在函数 `iter_files` 的定义行)——**无 manifest、无逐文件清单**,新增 `shared/guidelines/fast-fail.md` 自动被拾取;`pyproject.toml:37` 的 `"shared" = "specify_cli/shared"` 为目录级,打包无需改动。`scripts/python/regen-command-copies.py` 从 `templates/commands/*.md` 再生 `.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/` ⇒ **命令模板改动后 MUST NOT 手工批改副本。**
- **可复用的守卫样板**:`tests/contract/test_one_source_of_truth.py`(C-1..C-9:文档存在 + 镜像逐字节一致 `:64-67`;前 **8** 行声明所有权且含 `"single source of truth"` + `"MUST NOT copy"` `:72-76`;节齐备 `:79`;MUST/MUST NOT 关键词 `:106`;两份副本各含且仅含一次标题与指针 `:114-120`;模板**不内联**文档节名 `:125-131`;`shared/` + `templates/` 单源扫描 `:142-153`;项目中立性 `FORBIDDEN = ["spec-kit","specify-cli","specify_cli","cloud-native-ai"]` `:37,158-163`;宪章含该原则 + 版本下限 `:168-180`)。同形守卫:`test_token_efficiency_discipline.py`(`SECTION_HEADINGS:21-28`,`test_cd5_headings_only_in_discipline_doc:94`)、`test_user_facing_comprehension_doc.py`(`test_c4_ownership_declaration_in_first_eight_lines:226`、`test_c5_failure_statement_covers_both_surfaces:240` 前 **20** 行、`test_c7_rfc2119_keywords_present:260`、`test_c8_scope_limit_clause_present:267` 须点名拒绝的机制)、`test_ask_record_repeat.py`、`test_task_complexity_rubric.py`、`test_proactive_trigger_section.py`、`test_dogfooding_practice.py`。
- **命名占用实测(保留标识符检查)**:`fast-fail` / `fast_fail` / `fastfail` / `FAST_FAIL` / `fast-fail-list` 全仓(`.md/.py/.sh/.toml/.json/.yaml`,排除 `node_modules` 与 `.specify/teams/.work/`)**零命中**;`FF-` 作为标识符前缀零命中;`anomaly` 仅出现在随包发布的第三方工具文档中(`docs/reference/cli/opencode.md:24` 一个 Homebrew tap 名、`docs/concepts/security.md:210,237`),非框架标识符。**反序 `fail-fast` 已被散文占用**(非标识符)。需求阶段初记为 5 处且"全部指可写性探针",clarify 2026-09-22 第二轮由独立检测**证伪并订正**:在**权威源**(排除 `.claude/ .qoder/ .opencode/ .github/ dist/` 等再生副本)上重测得 **9 处**,其中 **3 处不是可写性探针**——连字符形态 2 处(`scripts/bash/check-prerequisites.sh:150` 可写性探针;`skills/manage-agents/references/intents/agent-setup.md:23` `保证：fail-fast 无部分写入；幂等；非破坏`,**配置写入原子性**,初记漏列),空格形态 7 处(`templates/commands/implement.md:45`、`interview.md:86`、`clarify.md:52`、`scripts/python/regen-command-copies.py:26` 均为可写性/再生前置探测;`tests/contract/test_hugo_scaffold_contract.py:153` `an unknown platform must fail fast` 为**平台校验**、`skills/manage-agents/scripts/config-agent.sh:691` `Validation gate — fail fast, write nothing.` 为**配置校验门**、`skills/create-skills/SKILL.md:57` `**Writability pre-flight (fail fast)**` 为可写性预检,后三处初记漏列)。⇒ **本纪律取 `fast-fail` 词序**,与用户输入一致,且与那 9 处既有语义不冲突;**该裁定不因订正而改变**(`fast-fail` 系列字面量仍全仓零命中,STR-001/009/010 均可用)。若用户偏好 `fail-fast`,消解歧义的负担比初记大近一倍且跨**三种**互不相干的语义(可写性探测 / 平台与配置校验 / 配置写入原子性),见 Assumptions。
- **子代理派发面:三条异质通道,且没有任何既有纪律规定自己如何抵达子代理**(2026-09-22 追加输入后实测):
  - **概念拥有者已存在**:`shared/definitions/subagent-definitions.md:3` `This file is the single source of truth for the Subagent concept`;`:9` 定义子代理为 `task-scoped delegated worker`,交付经 `returned message, result manifest, or declared output paths` 三种结果契约之一;`:25-27` 三种执行模式(**native** 运行时托管隔离 / **virtual** 无子代理能力时会话内模拟、`None — shares the session's context` / **external** 真独立进程、`Full process & context isolation`);`:50-73` **External Dispatch Visibility Contract** 是**全框架唯一一处挂在"派发"这个动作本身上的 MUST**(`:60` `Every external subagent dispatch MUST therefore:` 后接 5 条编号义务),其 `:52` 自陈动机为 `**The silent anti-pattern** (observed in real team runs)`、`:58` 判词 `A dispatch you cannot observe is a dispatch you cannot operate.` ⇒ **这是本特性派发期义务的直接形态先例**(同为"派发时必须满足的编号义务 + 一句失效判词")。
  - **常驻层结构性到不了子代理**:`:13` 子代理提示与配置 `derived from its **Agent Instance** definition … plus its dispatch config … or dispatch payload, not from the orchestrator's conversation`;`:14` `it receives exactly one task brief (plus its territory manifest in team runs), never the orchestrator's full history`;`skills/create-team/references/patterns.md:105-109` Context Isolation Rules `NO conversation history passed to child agents` / `Child agents receive only their territory manifest`。三条合起来是**有意设置的屏障**,不是疏漏。
  - **不允许发明"共享前导文件"**:`shared/definitions/agent-definitions.md:40` `Agent definition files are **self-contained** — there is no shared-assets directory under the agent stores; anything a definition depends on is either inlined or referenced from its owning document (shared/, skill references).` ⇒ 注入 MUST 走"内联有界字面量"或"引用拥有者文档"两种形态,MUST NOT 新增一个所有 agent 继承的共享资产目录。同文 `:25` 另有编辑路由规则 `A misbehaving Execution is terminated or re-dispatched; the fix lands in the layer below.`——即**执行层不可就地修**,与本纪律"停下上送而非强行修复"同取向。
  - **既有"必须在提示里写某内容"的唯一先例**:`shared/workflow/objective-analysis-gate.md:22` 规则 2 `**Name the same-author condition in the brief** — a subagent that does not know the artifacts are self-authored will not hunt the defect class that dominates them.`——**这正是本特性注入义务的同型先例**:不告知条件,子代理就不会去猎那一类缺陷。`:27` 规则 7 另定 `if dispatch fails twice in a row (upstream error), degrade to a direct bounded read and mark every resulting row … Never let the fallback pass silently as the delegated path.`(降级 MUST 标注,不得静默冒充)。
  - **三条派发通道,注入点各不相同**:① **编排者当场撰写的内联提示**(占多数:`templates/commands/instructions.md:45`、`plan.md:69,114`、`review.md:82-91`、`analyze.md:179-190`、`history.md:71,81`、`interview.md:114,164`、`skills/study-project/SKILL.md:150-166`、`skills/create-skills/SKILL.md:170`、`skills/document-utils/SKILL.md:90`);② **Agent 定义制品**(`templates/commands/agents.md:65-75` Run Mode `turns the Agent Instance definition into a new, independent Agent Execution (subagent)`,读 `.specify/agents/{templates,instances}/<name>.agent.md` 与 `execution/configs/<name>.yaml`);③ **团队载荷**(`skills/create-team/references/patterns.md:96-103` 的 Per-Agent Payload 五字段表 `task_brief` / `territory` / `forbidden_files` / `output_convention` / `model_hint`,与 `scripts/dispatch.sh` 外部派发包装器)。
  - **无共享派发前导机制**:`shared/patterns/` 恰 4 个文件(`explicit-implicit-pattern.md`、`interview-pattern.md`、`reconcile-pattern.md`、`self-improvement-pattern.md`)、`shared/constants/` 恰 3 个(`clarify-taxonomy.md`、`dfx-catalog.md`、`ignore-patterns.md`),**均不拥有派发提示格式**;仓库亦无"像给刚进门的同事交底那样写提示"这类通则(`cold` / `like a colleague` 零命中)。最接近的三处碎片是 `objective-analysis-gate.md:22`、`subagent-definitions.md:14`、`patterns.md:105-109`。
  - **包装器只管机制、内容归调用方**:`subagent-definitions.md:73` `the label convention of point 5 is the caller's responsibility` ⇒ 注入子句作为**提示内容**,其责任落点与标签约定同侧(调用方),而非包装器。
  - **守卫可表达**:`tests/contract/` 已有 12 个 agent/team 相关测试(`test_agent_render.py`、`test_shipped_agent_presets.py`、`test_single_agent_purity.py`、`test_team_territory.py` 等),房式断言形态为"文件存在 + frontmatter 键在场 + 字面量/标题在文件中命中 + 镜像逐字节相等"(`test_shipped_agent_presets.py:26-46`、`test_ask_record_repeat.py:116-137,174-178`)⇒ "注入子句在派发面在场"这一命题可用同一惯用法钉死。
  - **命名占用实测(追加项)**:`派发注入`、`注入子句`、`fast-fail-clause`、`ANOMALY:` 全仓零命中,均可用;`pre-dispatch` / `派发前` 仅以自然语言散文出现在无关工件中,非保留标识符。
- **既有 guideline 文档的房子骨架**(新文档 MUST 对齐):H1 取 `# <中文名>(<English Name>)` 或 `# <English Name>`;前 3–8 行声明所有权三要素(owns 什么 / 谁以路径引用它 / MUST NOT 复制);紧接一段"防的是哪种失效"(先例:`one-source-of-truth.md:7` `The failure this prevents is not disagreement, it is *silent* disagreement.`;`user-facing-comprehension.md:5` `本纪律防两种失效:`);H2 分节(实质规则 → 边界 → 程度 → 程序 → 与相邻原则的关系),末尾一条范围限制/不新增机制子句(先例:`user-facing-comprehension.md:122` 点名拒绝 lint 引擎 / 评分器 / 报告生成器 / 台账注册表;`one-source-of-truth.md:70` `MUST NOT be used to justify a duplicate-fact scanner, an authority registry, or any other new tracking machinery.`);全文 RFC-2119 大写关键词。

**与现状的差异(本需求要闭合的缺口)**:

| 缺口 | 今天的状态 | 本需求交付 |
|---|---|---|
| 命名与真源 | 纪律无名,真源文档数 0,十余处独立措辞 | 一份真源文档 + 一个名字 + 三层表面 |
| 分流判据 | 只有**输入侧**两级升级(`instructions-template.md:47-48`),执行期无判据 | 执行期可判定判据 + 机械测试 [[STR-005]] |
| 异常分类 | 无清单;`confirmation-gates.md:68` 只要求"如实报告",不分类 | 两份封闭清单(上送极 / 顺手修复极)+ 扩展规则 |
| 盲检类 | 只活在 `docs/reference/history/` 的教训正文里,指令文件按主题点名而不载规则 | 提升为清单条目,配两条已实测手法作判据 |
| 生长闭环 | 无标记、无提升规则 | 观察标记 [[STR-001]] + 提升规则 + 禁止静默调参 |
| 子代理派发面 | 既有纪律对"自己如何抵达子代理"**全部零表述**(实测 `shared/guidelines/` 12 份中 0 份提及子代理);派发期唯一的框架级 MUST 是可见性契约(管观测,不管行为) | 派发期注入义务 + 派发前自检 + 回传显式异常行,覆盖三条派发通道 |
| 下游导出 | 无原则、无 MUST include 条目 | 双落点导出,自动进入下游 plan 门控 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 执行中发现异常时,agent 按可判定判据分流,而不是就地修掉继续跑 (Priority: P1)

一位用户让 agent 执行一批动作。中途 agent 撞见一处与预期不符的状态。今天它多半会就地把它修平、继续跑完,并在收尾报告里呈现一个干净的结果——用户看不到那次修复,也看不到被修掉的东西原本意味着什么。本特性之后:agent 先按真源文档的判据问一句「**解决它需要纠正,还是需要裁定?**」,只需纠正且局部可逆的就顺手修完并在收尾逐项披露;需要裁定的就**停在异常点**,把「发现了什么 / 为何吃重 / 已产生的中间产物 / 可选处置」四要素交给用户,由用户决定怎么走。

**Why this priority**: 这是用户点名的"关键"。没有这条判据,后面所有的清单、守卫、导出都只是在给一个未定义的行为写文档。它单独落地即已消除"静默兜底"这一失效。

**Independent Test**: 只需真源文档存在并载有判据、两份清单与机械测试 [[STR-005]],即可用一组异常场景样本做**双评审者一致性**验证(见 SC-001),并可用房子历史中的 4 种盲检成因做**回归覆盖**验证(见 SC-002)——不依赖常驻章节、宪章导出或观察闭环。

**Acceptance Scenarios**:

1. **Given** 一条检查报告"绿",但把被守物弄坏它也不会变红,**When** agent 判定该异常类别,**Then** 它 MUST 归入 fast fail 清单(盲检类),停在异常点并上送,MUST NOT 把这次绿当证据继续。
2. **Given** 一个路径参数里的明显拼写错误,且纠正后恰有一种与已记录意图一致的读法,**When** agent 判定该异常类别,**Then** 它 MAY 顺手修复、继续执行,并在所属流程的收尾报告里逐项披露该修复与所采用的解读。
3. **Given** 一处异常既未命中 fast fail 清单也未命中顺手修复清单,**When** agent 判定该异常类别,**Then** 它 MUST 按快速失败处理(存疑从严),MUST NOT 自行推断一种读法后继续。
4. **Given** 一次顺手修复的说明里必须出现「假定」一词,**When** 复核者应用机械测试 [[STR-005]],**Then** 该次处置 MUST 被判定为一次误分类的快速失败,而非合规修复。
5. **Given** 上游工件传来一个计数,实测与工件所载不符,而下游任务建立在该计数上,**When** agent 发现该前提被证伪,**Then** 它 MUST 快速失败并把证伪结果回写到上游工件所在处,MUST NOT 只在本地绕过。

---

### User Story 2 - 这条纪律获得名字、唯一真源、常驻可见性与防漂移守卫 (Priority: P1)

框架维护者要让这条规矩**在每个会话里都够得着**,而不是只在被写下的那个命令模板里生效。本特性之后:纪律有一个名字(Fast Fail / 快速失败 [[STR-008]])、一份声明自己为唯一真源的文档 [[STR-002]]、一个随指令文件增量调谐抵达所有已初始化项目的顶级常驻章节 [[STR-003]]、以及一组契约测试 [[STR-007]] 保证三者不各自漂移。

**Why this priority**: 房子已两次证明(040 Token Efficiency、051 User-Facing Comprehension)——**没有第三层守卫的重复会各自漂移,最后三处说法不一,比重复之前更糟**(`ask-record-repeat.md:86`),且 `:117` 明写"给一条规矩新增表面时,MUST 同批加守卫"。判据(US1)与可达性(US2)必须同批交付,否则 US1 的成果会在下一次会话里够不着。

**Independent Test**: 可独立验证——断言真源文档存在且与镜像逐字节一致、前 8 行声明所有权且含既有守卫所断言的字面量、必备 H2 节齐备、常驻章节在模板与活动指令文件中各出现且仅出现一次、模板不内联文档节名、`shared/` + `templates/` 单源扫描无第二处定义点、文档项目中立。全部为既有守卫样板的同形断言。

**Acceptance Scenarios**:

1. **Given** 仓库检出后运行契约测试套件,**When** 真源文档缺失、或其与 `.specify/` 镜像副本不逐字节一致,**Then** 守卫 MUST 变红。
2. **Given** 一个已初始化的下游项目运行指令再生,**When** 其活动指令文件缺少 [[STR-003]] 章节,**Then** 该章节 MUST 被整体注入(增量调谐按整章节传播),且既有章节 MUST NOT 被改动。
3. **Given** 有人在某个命令模板里重新写了一遍分流判据正文,**When** 单源扫描运行,**Then** 守卫 MUST 变红并指出该复述点位。
4. **Given** 真源文档被改写,**When** 复核其前 8 行,**Then** 它 MUST 声明自己为唯一真源、点名常驻章节所在文件与标题、并写明消费者 MUST 引用而 MUST NOT 复制。

---

### User Story 3 - 下游项目的宪章收到这条原则,并在 plan 门控里被逐条枚举 (Priority: P1)

一位下游项目负责人用框架 bootstrap 自己的项目。本特性之后,他的宪章里会有一条 Fast Fail 原则 [[STR-004]],因为 `templates/constitution-template.md` 与 `templates/commands/constitution.md` 的 `MUST include` 清单**双落点**都载有它;并且由于 plan 模板按宪章动态枚举原则,他每次跑 `/speckit.plan` 都会在 Constitution Check 门控里看到这一条被逐项核对——无需任何额外接线。

**Why this priority**: 用户要求的是"在**整个框架**中增加",而不只是本仓自用。层 B 是这条纪律真正扩散到别人项目的唯一通道。房子已有同型前车之鉴:一条原则只落活动宪章、未回流模板,结果是**没有任何下游项目收到它**(`.specify/memory/constitution.md:7` 记载了这次回流与其修复),051 因此把双落点写成硬要求。

**Independent Test**: 可独立验证——断言模板原则数与命令 `MUST include` 条目数各 +1、双落点标题一致、新增原则块符合既有结构(冒号结尾主张句 / MUST·MUST NOT 要点 / guidelines 指针要点 / 不新增机制要点 / `Rationale:` 段 / 折行 <100 字符)、活动宪章原则数 +1 且版本 ≥ 1.13、`plan-template.md` 零改动而枚举行数 +1。

**Acceptance Scenarios**:

1. **Given** 一个新下游项目按宪章命令 bootstrap,**When** 其宪章生成完成,**Then** 它 MUST 含一条 Fast Fail 原则,且该原则 MUST 以路径援引真源文档而非复述其规则。
2. **Given** 该下游项目随后运行 `/speckit.plan`,**When** Constitution Check 渲染,**Then** Fast Fail 原则 MUST 作为独立一行出现在门控表中,且 `templates/plan-template.md` MUST NOT 因本特性被改动。
3. **Given** 本仓活动宪章,**When** 新原则落位,**Then** 版本号 MUST 按 MINOR 递增(1.12.0 → ≥ 1.13),且既有双落点测试的四个计数/下限钉子 MUST 在同一批变更中上调。

---

### User Story 4 - 子代理在启动那一刻就带上规则:异常回抛给编排者,而不是在自己的黑盒里修平 (Priority: P1)

一位用户让主会话把一个任务派发给子代理。子代理一旦启动,主会话就**无法中途干预**它;而按框架自己的定义,子代理的提示来自它的 Agent 定义与派发载荷,**不来自编排者的对话**——所以主会话读到的常驻指令**根本传不进去**。今天的结果是:子代理撞见异常时,多半就地修平、交回一个看起来干净的结论,主会话无从分辨"真的干净"与"没人告诉它要报"。

本特性之后:编排者在**派发之前**就把一段固定形态的注入子句放进子代理读得到的地方(内联提示 / Agent 定义制品 / 团队载荷三者之一),并**先自检该子句确实在场**才发出;子代理撞见需要裁定的异常时**停在自己那一层**,用固定前缀 [[STR-010]] 把异常回抛给编排者,由编排者组装面向用户的上送件;每次回传都 MUST 带一条显式异常行——没有异常也要明说"未发现异常",使沉默不再被当作干净。

**Why this priority**: 用户在追加输入中点名**重点关注**这一面,理由是"一个 subagent 启动之后它的行为就不受控"。这个判断经源码核实成立且比直觉更硬:常驻层到不了子代理不是疏漏而是**有意设置的隔离屏障**,所以未注入的子代理是**结构性地**收不到规则。同时,派发期唯一既有的框架级 MUST(外部派发可见性契约)只管"能不能观测",不管"守不守规矩"——既有纪律对"自己如何抵达子代理"全部零表述(实测 `shared/guidelines/` 12 份中 0 份提及子代理)。控制点只有两个:**派发之前**与**回传之时**。

**Independent Test**: 可独立验证,不依赖宪章导出或观察闭环——断言真源文档载有注入子句的拥有者定义与三条通道的落点;断言 Agent 定义制品与团队载荷模式各携该子句且与拥有者逐字节一致;断言派发前自检与回传显式异常行两条义务在文档中在场;再对一个真实派发做变异演练(移除子句 → 自检应变红 → 复原)。

**Acceptance Scenarios**:

1. **Given** 编排者准备派发一个子代理,**When** 派发**前**的自检发现待发出的提示/载荷缺少注入子句的固定标识 [[STR-009]],**Then** 编排者 MUST 补齐子句后照常派发,并把这次补齐并入收尾报告披露——此时它是**顺手修复**(恰有一种读法、改动局部可逆、补齐后无证伪前提残留、半径不越本动作);MUST NOT 先派发再指望事后补救。
2. **Given** 同一次派发,**When** 子句缺失是**派发之后**才被发现的,**Then** 它 MUST 被当作一次**快速失败**:子代理已经不受治理地跑过了,改提示无法撤销这件事,而"已完成的那部分工作是受治理的"这一前提已被证伪。编排者 MUST 停下上送,MUST NOT 把该子代理的产出当作可信证据继续消费。
3. **Given** 一个子代理在执行中撞见需要裁定的异常,**When** 它按注入子句处置,**Then** 它 MUST 停在自己的任务范围内、以前缀 [[STR-010]] 把异常回抛给编排者,MUST NOT 就地修平后交回一个看起来干净的结论;面向用户的上送件由编排者组装,子代理 MUST NOT 假定自己拥有用户通道。
4. **Given** 一个子代理执行完毕且未发现任何异常,**When** 它回传结果,**Then** 回传 MUST 含一条显式的"未发现异常"陈述;编排者 MUST NOT 把缺少异常行的回传读作干净(缺行本身的处置见 FR-066)。
5. **Given** 编排者收到一个带 [[STR-010]] 前缀的回传,**When** 它决定下一步,**Then** 它 MUST 把该回传判为"异常停"而非"普通失败",MUST NOT 原样重派或要求其"再试一次"——重派一次异常停,等于在上一层重新犯下静默兜底。
6. **Given** 三种执行模式(native / virtual / external)中的任意一种,**When** 注入义务被应用,**Then** 它 MUST 对该模式同样成立;注入 MUST 是**调用方的内容义务**,MUST NOT 被实现为外部派发包装器的行为(包装器只覆盖 external 一种模式,且其既有分工是"机制归包装器、内容归调用方")。
7. **Given** 一份 Agent 定义制品携带了注入子句,**When** 守卫比对该副本与真源文档中拥有者的字面量,**Then** 二者 MUST 逐字节一致;不一致 MUST 变红(该副本受守卫钉死,不是可各自改写的第二定义点)。

---

### User Story 5 - 两份清单随使用**双向**生长:观察留痕、达阈值提升或降级、并度量过度触发 (Priority: P2)

一位用户在多次使用后注意到:某类异常反复出现,而清单里没有它;又或者某类东西被上送得太频繁,他每次都想"这个你顺手修掉就行"。本特性之后,每次触发快速失败或顺手修复都会在反馈条目里带上稳定标记 [[STR-001]];用户(或自省流程)可以按标记把这类观察捞出来聚合;一个异常类被独立观察命中达阈值、或被用户直接纠正命中一次,它就 MUST 被移进对应的那一份清单——**纠正朝哪个方向,就往哪个方向生长**,降到顺手修复清单与升到 fast fail 清单是同一套证据资格。原先散落的那处局部措辞 MUST 收敛为指针。反过来,清单 MUST NOT 被静默调整到出现有利结果为止;而"这条纪律被上送得太频繁以致被绕过" MUST 是可观测的,不是靠印象。

**Why this priority**: 用户明确要求的第三件事("随着使用通过 feedback 和自省机制逐步进行完善和提升")。它是让 US1 的判据长期有效的机制,但**在 US1+US2 交付之后才有意义**——没有真源文档,提升无处可落。

**Independent Test**: 可独立验证——写入一条含标记的反馈条目后,`feedback-utils.py --action list --contains` 加该标记 MUST 能检索到它;清单每次提升 MUST 能在反馈存据或用户纠正记录中找到对应证据;守卫 MUST 断言真源文档载有标记字面量、提升规则、以及"干净运行 MUST NOT 追加空洞观察条目 / MUST NOT 编造数值"两条红线。

**Acceptance Scenarios**:

1. **Given** 一次运行触发了快速失败,**When** 该运行进入反馈收尾,**Then** 其优化点条目行 MUST 内嵌标记 [[STR-001]],且 MUST 可被引擎按该标记检索。
2. **Given** 一次运行干净、无异常,**When** 反馈收尾,**Then** MUST NOT 追加空洞的观察条目。
3. **Given** 同一异常类被两次独立观察命中,**When** 复核者应用提升规则,**Then** 该类 MUST 被提升进真源文档的 fast fail 清单(以修订该文档的形式),且原处的局部措辞 MUST 收敛为指针,MUST NOT 保留第二份独立清单。
4. **Given** 用户直接纠正了某次分流结论——**无论纠正方向是"这个本该上送"还是"这个你本该顺手修掉"**,**When** 复核者应用提升/降级规则,**Then** 该一次纠正即构成充分证据,MUST NOT 要求重复出现(引用 `self-improvement.md:42` 的既有资格判据),且该异常类 MUST 被移进纠正所指的那一份清单;两份清单的证据资格 MUST 对称,MUST NOT 只存在朝"停止"一侧的单向通道。
5. **Given** 一段时期内快速失败被频繁触发、且用户频繁推翻其结论,**When** 复核者按标记聚合观察,**Then** 该过度触发状态 MUST 可被度量并进入报告,使"这条纪律正在被绕过"成为一个有数字的信号而非印象(见 SC-015)。
6. **Given** 有人提议调整清单以便某个门禁通过,**When** 该调整缺乏观察证据或用户纠正,**Then** 它 MUST 被拒绝并如实记录(MUST NOT 静默调参直到出现有利结果)。

---

### User Story 6 - 与四条相邻纪律的边界落位,既有分散实例收敛为指针,且门控预算保持中立 (Priority: P2)

一位维护者担心两件事:这条新纪律会不会和确认门控治理、输入健全性检查、同作者检测委托、自我提升治理**说出第二套互相矛盾的话**;以及它会不会因为"要求停下来"而被门控扫描器计成一个新的阻塞门控,从而打爆已经把余量用尽的既有契约测试(其数目与形态不在本规格内枚举,由 `contracts/gate-neutrality.md` C-10 单点拥有)。本特性之后:真源文档用一节显式声明五条边界(各纪律各自拥有什么、本纪律 MUST NOT 重定义什么),把 US1 提到的十余处既有实例点名为**实例**并以单行指针接入,并且所有新增文本对扫描器的阻塞模式**零命中**、扫描器源码零改动、实跑 total 与冻结基线相等。

**Why this priority**: 这是让前五个故事**不与既有治理打架**的收口工作。它不新增用户可见能力,但缺了它,US1–US5 的产物会在 CI 上直接变红(门控预算余量为 0),或在文档空间里制造第二套判据(违反 One Source of Truth)。

**Independent Test**: 可独立验证——实跑扫描器断言 total 与冻结基线**相等**且 violations 为空;断言 `scan-confirmation-gates.py` 的 `POLICY_DOCS`、`SELF_REL`、`BLOCKING_PATTERNS` 条数均未变;断言真源文档载有五处边界声明且不内联相邻纪律的判据正文;断言被点名的既有实例点位各含一行指向真源文档的指针。

**Acceptance Scenarios**:

1. **Given** 本特性的全部新增文本已落位,**When** 实跑 `scan-confirmation-gates.py`,**Then** total MUST 与 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` 的冻结值**相等**,violations MUST 为空。
2. **Given** 同一次运行,**When** 检查扫描器源码,**Then** `POLICY_DOCS`、`SELF_REL` 字面量与 `len(BLOCKING_PATTERNS)` MUST 与变更前一致(取**设计规避**,MUST NOT 扩大豁免集)。
3. **Given** 真源文档需要表述"停在异常点并交用户裁定",**When** 复核其措辞,**Then** 它 MUST NOT 命中扫描器的任何阻塞模式(即 MUST NOT 使用「等待用户确认」「stop and confirm」「确认后执行」「确认门禁」「explicit user confirmation」等形态),MUST 改用不命中等价表述。
4. **Given** 一个动作本身可逆、但执行中发现其前提被证伪,**When** 两条纪律同时适用,**Then** 确认门控治理裁"该动作可否不经前置授权执行"(按动作可逆性),本纪律裁"该发现之后可否继续"(按前提是否被证伪/是否需要裁定);真源文档 MUST 声明这一正交关系,MUST NOT 重定义门控判据,MUST NOT 向治理保留清单新增行。
5. **Given** `templates/commands/implement.md` 等既有实例点位,**When** 本特性收敛完成,**Then** 每个被点名的点位 MUST 保留其原有行为正文,并各增一行指向真源文档的指针,MUST NOT 复制判据正文。

---

### Edge Cases

- **异常出现在只读命令中**(如跨产物一致性分析):该命令本无写权限,快速失败的上送 MUST 走"报告 + 请求批准"形态,与既有只读命令的补救批准例外同型;MUST NOT 因为"只读所以无害"而降级为顺手修复。
- **异常出现在子代理内**:MUST 按 US4 的注入子句处置——停在自己的任务范围内、以固定前缀 [[STR-010]] 回抛编排者,MUST NOT 在子代理内自行消化;若委托通道不可用而降级为直接读取,该降级 MUST 被标注,MUST NOT 静默冒充委托路径(引用 `objective-analysis-gate.md:27` 的既有先例)。
- **子代理是 virtual 模式**(执行工具无子代理能力,由当前会话模拟):此时会话**确实**持有常驻层,但按定义它"adopts the agent definition's independent prompt/config",隔离是**约定**而非运行时强制。注入义务 MUST 同样成立——该模式的价值就在于模拟出独立提示;若因"反正常驻层在"而跳过注入,那条边界就是假的。
- **子代理是只读的**(检测/验证类派发,无写权限):注入子句 MUST 仍然在场。只读子代理的"快速失败"表现为**在回传里标注异常**而非停写——它本来就不写;但"发现异常而当噪声略过"与"发现异常并回抛"的差别,只在注入之后才存在。
- **注入子句与子代理自身 Agent 定义正文冲突**(定义写着"尽力完成、不要中途返回"):真源文档 MUST 声明裁决顺序——注入子句优先,因为它是框架级纪律而定义是角色级约定;该冲突本身 MUST 被回抛给编排者作为一次异常,MUST NOT 由子代理自行择一。
- **编排者并行派发多个子代理,其中一个回抛异常**:与该异常无关的其余子代理按既有并行规则处理(成功者继续、失败者上报),但汇总 MUST 把该异常呈现为**未决项**,MUST NOT 因多数已回传而把结果当作完整。
- **注入子句在派发链的第二节丢失**(编排者 A 派发 B,B 再派发 C):注入义务 MUST 随派发链传递——B 派发 C 时 MUST 重新注入,MUST NOT 假定"我收到过所以下游也有";每一跳都是一次新的隔离边界。
- **快速失败本身无法上送**(无交互通道、批处理环境):MUST 把四要素上送件落盘为可追溯的失败报告并终止该动作链,MUST NOT 因上送失败而转为静默继续。
- **用户对上送件的裁定是"照原样继续"**:该裁定 MUST 被记录(沿用既有门控观察协议的四值决定信号词汇),且 MUST NOT 被回写为清单的通用例外——一次裁定只豁免这一次。
- **同一异常在一次运行内第二次出现**:MUST 升级为快速失败(两振停滞),MUST NOT 再按顺手修复处理,理由是"结构性阻塞,更多迭代不会修好它"。
- **一处异常同时命中两份清单**(既像可顺手修的拼写错、又证伪了下游前提):MUST 按快速失败处理——上送极优先,理由是爆炸半径判据压倒局部性判据。
- **顺手修复的披露时机**:多个自动处置 MUST 合并为一次收尾呈现、逐项列出,MUST NOT 逐动作打断用户;单个琐碎修复 MUST NOT 独立出完整报告(引用既有执行报告的粒度规则,不复述)。
- **派发前自检本身失败**(编排者发现自己无法把子句放进 outgoing 提示,例如宿主工具不透出提示构造面):这 MUST 被当作一次快速失败,MUST NOT 降级为"那就直接派发";理由是缺失注入的派发等价于派发一个不受治理的执行体。
- **清单未覆盖的全新异常类**:按存疑从严归快速失败,并 MUST 成为 US5 提升规则的候选输入。
- **下游项目缺少真源文档**:该文档随框架发布(`pyproject.toml` 以目录级条目打包整个 `shared/`),其运行时副本由 **CLI 的资产复制路径**恢复——实测该复制发生在 `src/specify_cli/__init__.py` 的 `copy_local_templates()`(`:2202-2216` 把 `shared/` 复制到 `.specify/shared/`,由 `init()` 于 `:2866` 调用;`_CORE_SPECIFY_ASSETS` 于 `:1081` 含 `.specify/shared`)。⚠️ **`/speckit.instructions` 不做这件事**:实测 `scripts/bash/generate-instructions.sh` 只按整章节增量注入指令文件,全文无任何镜像同步调用,`templates/commands/instructions.md` 亦只把自身描述为对"指令空间"的调谐引擎。⇒ 一个较旧的下游项目若只跑指令刷新,会得到常驻章节 [[STR-003]] 而其指针 [[STR-002]] **悬空**;按房子既有规则,悬空引用 MUST NOT 静默降级,故命中它的命令会中止。FR-077 承载此缺口。MUST NOT 凭记忆重建规则或按摘要行事。
- **既有实例点位与新判据冲突**(某处已写"失败即停",而新判据判为可顺手修):真源文档 MUST 声明裁决顺序,冲突 MUST 在该文档内解决,MUST NOT 让两处各自生效。
- **门控预算被打爆的诱惑**:若某条清单条目无法以零命中措辞表达,MUST 改写措辞或改写条目,**MUST NOT** 通过扩大扫描器豁免集或调整冻结基线来通过。

## Requirements *(mandatory)*

### Functional Requirements

#### 真源、命名与常驻可见性

- **FR-001**: 系统 MUST 建立唯一真源文档 [[STR-002]],命名该纪律为 **Fast Fail(快速失败)** [[STR-008]];该文档 MUST 是分流判据、两份清单、上送件形态、双向生长规则与五处边界声明的**唯一定义点**。
- **FR-002**: 真源文档 MUST 在前 8 行内声明所有权三要素:它拥有什么、哪个文件的哪个常驻章节以指针引用它、消费者 MUST 以路径引用而 MUST NOT 复制其规则文本。
- **FR-003**: 真源文档 MUST 在开头紧随所有权声明处,用一段话陈述**它防的是哪种失效**(静默兜底:错误被就地修平、用户看不见、下游把它当已验证前提继续引用),形态对齐既有真源文档的先例。
- **FR-004**: 真源文档 MUST 与 `.specify/shared/guidelines/` 下的镜像副本逐字节一致;新增文件 MUST 由既有同步引擎自动拾取,MUST NOT 需要任何 manifest 或逐文件清单登记,MUST NOT 手工编辑镜像副本。
- **FR-005**: 系统 MUST 在 `templates/instructions-template.md` 新增一个**顶级** `## ` 章节 [[STR-003]],承载摘要 + 指针;该章节 MUST 是新增顶级章节(因为指令再生只按整章节增量注入,既有章节内部的改动抵达不到已初始化项目),MUST NOT 以在文档地图表内新增一行的方式替代。
- **FR-006**: 常驻章节 MUST 只承载摘要与指向真源文档的指针,MUST NOT 内联真源文档的节名、清单条目或阈值字面量。
- **FR-007**: 真源文档 MUST 采用房子骨架:双语 H1、RFC-2119 大写关键词、H2 分节顺序为"实质规则 → 边界 → 程度 → 程序 → 与相邻原则的关系",并以一条**范围限制/不新增机制**子句收尾,点名本纪律拒绝引入的机制(异常检测引擎、分流评分器、清单成熟度报告、独立跟踪台账或注册表)。
- **FR-008**: 真源文档 MUST 项目中立:MUST NOT 含本仓专名(`spec-kit`、`specify-cli`、`specify_cli`、`cloud-native-ai`),以便随包发布到任意下游项目。

#### 分流判据(双向边界)

- **FR-009**: 真源文档 MUST 给出执行期异常的**二值**分流判据,判据 MUST 落在「解决该异常需要**纠正**还是需要**裁定**」这一轴上:MUST NOT 采用"错误严重程度"这类不可判定的连续量,MUST NOT 留下"尽量顺手修"这类不可判定的中间档。
- **FR-010**: 顺手修复极 MUST 要求**全部**条件同时成立:(a) 恰有一种与已记录意图一致的读法;(b) 改动局部且可逆;(c) 未证伪任何下游工作所依赖的前提;(d) 爆炸半径未越过本动作声明的范围。任一不成立 MUST 归快速失败。
- **FR-011**: 真源文档 MUST 载明分流判据的**机械测试** [[STR-005]],使两个独立复核者对同一次处置得出同一结论;判定不可复现 MUST 被视为判据本身需要修订的信号,而不是"两位复核者都对"。
- **FR-012**: 真源文档 MUST 载明**存疑从严**默认:既未命中 fast fail 清单、也未命中顺手修复清单的异常 MUST 按快速失败处理。该默认 MUST 以指针说明它与确认门控治理同名规则的取向一致而作用面不同(动作侧 vs 发现侧),MUST NOT 复述其正文。
- **FR-013**: 真源文档 MUST 声明**上送极优先**的裁决顺序:一处异常同时命中两份清单时 MUST 按快速失败处理。
- **FR-014**: 真源文档 MUST 声明**两振升级**:同一异常在一次运行内第二次出现 MUST 升级为快速失败,MUST NOT 再按顺手修复处理。"同一"按**复发键 = `被证伪的预期` 单键**认定,**不含发现点**(2026-09-23 用户裁定,见 `## Clarifications`)。理由:复发几乎总出现在**不同的发现点**,把发现点纳入键会使二元组不相等、计数不增,本规则在最常见形态下**不可达**——该不可达性由两位互不共享上下文的独立评审者在同一场景上各自发现(`notes/sc001-dual-review.md` §2)。
- **FR-015**: 判据 MUST 同时覆盖**机器给出的绿**:一条检查报告通过、但被守物损坏时它不会变红,该次通过 MUST 被判为快速失败而非证据。真源文档 MUST 载明这一条的机械测试 [[STR-006]],并 MUST 援引房子已有的两条配套手法(变异演练、反空真哨兵)作为其判据,MUST NOT 重新发明它们。

#### 两份封闭清单

- **FR-016**: 真源文档 MUST 载有 **fast fail 清单** [[STR-011]]:一组保守、可枚举的异常类,命中即 MUST 上送。清单 MUST 至少覆盖以下已在本仓实测到过的失效形态:前提被证伪且下游依赖它、盲检、`&&` 链中合法结果为零导致的静默截断、意图缺口(需在 ≥2 种合理读法间选择)、爆炸半径越界(定义见 FR-073)、两顶帽子错位(编辑了错误的那棵树)、覆盖式脚手架将清空既有制品、两振停滞、以及"仅不可撤销动作方可通过"(该条 MUST 委托 `shared/guidelines/confirmation-gates.md` 并以其判据为准,MUST NOT 复制其清单)。为使 FR-020 的守卫与 SC-002 的度量指向**同一个**封闭集合,其中"盲检"一项 MUST 在清单里**逐条展开**为其四种已实测成因,且 `git diff` 取"本次改了什么"的三种形态陷阱 MUST 一并列入点名集合(而非仅以路径引用出现)——合计点名的已实测失效形态为 **7 项**(盲检四成因 + `git diff` 三形态),与 SC-002 的分母一致。清单总条数仍可多于 7(它可生长),但这点名的 7 项 MUST 逐项可定位,守卫按此 7 项断言覆盖,不按清单总条数断言。
- **FR-017**: 真源文档 MUST 载有 **顺手修复清单** [[STR-012]]:一组保守、可枚举的异常类,命中即 MAY 就地修完并继续。清单 MUST 至少覆盖:明显拼写/近似错(路径、旗标、选项名)且纠正后的解读被显式陈述、镜像漂移(以既有同步引擎修复)、按工具副本过期(以既有再生脚本修复)、机器生成物缺失或过期(再生)、纯格式与折行且零语义变更、以及恰有一种取值与已记录意图一致的缺省补全。
- **FR-018**: 两份清单 MUST 为**封闭集**:扩展 MUST 只经修订真源文档,MUST NOT 分散到各命令模板或技能自行增类。
- **FR-019**: 两份清单的每一条 MUST 携一句**判据**(如何认定命中),MUST NOT 只有类名;判定 MUST 可由第二位复核者独立复现。
- **FR-020**: 清单条目数 MUST NOT 被任何守卫钉死为相等(清单是设计为可生长的);守卫 MUST 只断言"清单存在、非空、每条携判据、且首版覆盖 FR-016 点名的已实测失效形态"。
- **FR-021**: 真源文档 MUST NOT 复述既有教训正文:对盲检类与 `git diff` 形态陷阱,MUST 以路径引用 `docs/reference/history/` 的对应小节作为实证来源,只把**判据**写进清单。

#### 上送件形态与粒度

- **FR-022**: 快速失败 MUST 停在异常点并向用户交付一份**上送件**,四要素缺一不可:发现了什么、为何吃重(它证伪了什么前提/影响哪些下游)、已产生的中间产物(逐项可定位)、可选处置。
- **FR-023**: 上送件 MUST 让用户**无需打开其他工件即可作出处置**;其余一切 MUST 以路径引用抵达。其措辞与上下文的下限/上限 MUST 引用面向用户可理解性纪律,MUST NOT 在本真源文档内另立一套。
- **FR-024**: 上送件所属的界面类 MUST 归入面向用户可理解性纪律已枚举的封闭集,并 MUST 使用**该拥有者的类名**而非本规格的近似说法:上送件归 **⑪ 失败如实报告**,MUST NOT 归 **① 门控确认提示**。理由是实质的而非命名的——类 ① 的规则真源是 `shared/guidelines/confirmation-gates.md`,且该纪律另要求门控类界面载明不可撤销后果与可逆性;把上送件归入 ① 会使它成为一个门控提示,与 FR-028"本纪律不新增门控、不向治理保留清单增行"直接矛盾,也会使 SC-005 的零命中主张不再安全。本特性 MUST NOT 向该封闭集新增类别。因类 ⑪ 的既有规则真源文件是 `shared/guidelines/confirmation-gates.md`,本特性的真源文档 MUST NOT 成为类 ⑪ 的**第二个**规则真源(那会被该纪律的封闭集规则禁止):上送件的**四要素内容下限**由本真源文档拥有(四要素是本纪律特有的),类 ⑪ 的**措辞与上下文规则**仍归其既有拥有者,本真源文档 MUST 以 FR-074 要求的 canonical 指针行声明它覆盖类 ⑪ 的哪一部分。该分工 MUST 在 `/speckit.plan` 期与该纪律的界面类映射表核对;若需改动那张表,MUST 显式列为一次跨纪律改动,不得默默发生。
- **FR-025**: 顺手修复 MUST 在所属流程的收尾报告中**逐项披露**(修了什么、为何是纠正而非裁定、所采用的解读);披露的粒度与合并规则 MUST 引用确认门控治理的执行报告节,MUST NOT 复述其三要素与粒度条款。
- **FR-026**: 快速失败的停止粒度 MUST 为:停在异常动作及其依赖者;与该异常无关的独立并行工作按既有规则处理(成功者继续、失败者上报),该既有规则 MUST 以指针引用,MUST NOT 复述。
- **FR-027**: 上送通道不可用时,MUST 把上送件落盘为可追溯的失败报告并终止该动作链;MUST NOT 因上送失败而转为静默继续。

#### 与相邻纪律的边界

- **FR-028**: 真源文档 MUST 载有一节显式声明与**五条**相邻纪律的边界,每条 MUST 写明"对方拥有什么 / 本纪律拥有什么 / MUST NOT 重定义什么":
  - **确认门控治理**:它按**动作**可逆性裁"可否不经前置授权执行";本纪律按**发现**是否证伪前提裁"可否继续"。两轴正交。本纪律 MUST NOT 重定义其判据、MUST NOT 复制其两份清单、MUST NOT 向其治理保留清单新增行。
  - **输入健全性检查**:它拥有"行动前跑哪些检查";本纪律拥有"检查失败或执行中途出现异常时如何分流"。其两级升级规则的**形态**被复用,其文本 MUST NOT 被复述。
  - **同作者检测委托**:它拥有"同作者检测须委托新鲜上下文子代理"这一触发条件、七条门控规则与严重度上限;本纪律 MUST NOT 改动其中任何一条,只在其**派发面**上新增注入义务(归下方 `#### 子代理派发注入` 一组),并复用其既有先例"降级 MUST 被标注,MUST NOT 静默冒充委托路径"。
  - **自我提升治理**:它拥有证据资格判据(含"用户直接纠正即充分,不需重复出现")与"变更须最小可逆";本纪律的双向生长规则 MUST 引用其资格判据,MUST NOT 另立一套。
  - **问一次、记下来、说三遍**(clarify 2026-09-22 第二轮补入):它拥有"一个吃重事实未知或有歧义时提问、不猜"的理念,以及"同一个问题不需要问第二遍"的记录义务。本纪律 MUST 引用后者:上送前 MUST 先检索该类异常是否已有既往裁定(FR-075(c)),否则一次运行内的反复上送会与"一次裁定只豁免这一次"合起来造成无界往返。其理念层文本 MUST NOT 被复述——该文档自陈其规则是理念而非机械可判,本纪律**不沿用**那一形态(见 Assumptions),但 MUST 承认其理念层的优先性。
- **FR-029**: 既有分散实例点位(`templates/commands/implement.md` 的可写性探针、前提证伪回写、门控判定不得绕、非并行失败即停、两振停滞;`todo.md` 的失败即停;`analyze.md` 的缺件即中止;`docs.md` 的标记不配对即停与尾部不得静默延迟;`clarify.md` 的缺件即中止与超上限即停;`interview.md` 的冲突不得静默解决;`skills/create-team` 的悬空引用不得静默降级;`skills/draw-diagram` 的不得静默降级)MUST 被真源文档**点名为实例**,并各以一行指针接入;各点位 MUST 保留其原有行为正文,MUST NOT 被改写为判据复述。
- **FR-030**: 本特性 MUST NOT 对既有命令与技能做全仓措辞清扫;收敛范围 MUST 限于 FR-029 点名的点位(见 Out of Scope)。

#### 下游导出(双落点)

- **FR-031**: 系统 MUST 在 `templates/constitution-template.md` 新增一条原则 [[STR-004]],并在 `templates/commands/constitution.md` 的 `MUST include` 清单新增对应条目——**双落点缺一即视为未完成**;新增原则块 MUST 符合既有结构(以冒号结尾的主张句、携 MUST/MUST NOT 的要点、一条以路径援引真源文档的指针要点、一条"不新增机制"要点、`Rationale:` 段、折行 <100 字符)。
- **FR-032**: 本仓活动宪章 `.specify/memory/constitution.md` MUST 同批新增对应原则,版本号 MUST 按 MINOR 递增(自 1.12.0 起 ≥ 1.13);既有双落点守卫的四个钉子(`TEMPLATE_COUNT`、`LIVE_COUNT`、`COMMAND_COUNT`、`MIN_VERSION`)MUST 在同一批变更中上调,MUST NOT 留到后续特性。
- **FR-033**: `templates/plan-template.md` MUST NOT 被改动:其 Constitution Check 按宪章动态枚举原则,新原则自动抵达下游每次 plan 门控。
- **FR-034**: 宪章原则与命令条目 MUST 以路径援引真源文档,MUST NOT 复述分流判据或清单条目。

#### 漂移守卫与门控预算中立

- **FR-035**: 系统 MUST 新增契约测试 [[STR-007]],与既有纪律守卫同批落地(MUST NOT 先加表面后加守卫)。**断言集 MUST 逐条对应下列义务——本条是封闭枚举,凡本规格要求真源文档载明而未列入者,即构成一处"文档没写也照样绿"的盲检**(clarify 2026-09-22 第二轮把枚举从 10 项扩到 22 项,正是为消除该盲检):
  1. 真源文档存在,且与 `.specify/` 镜像副本逐字节一致;
  2. 前 8 行所有权声明含既有守卫所断言的字面量;
  3. FR-003 要求的"防的是哪种失效"陈述在前 20 行内在场;
  4. FR-007 要求的双语 H1、必备 H2 节、以及收尾的范围限制子句(**须点名拒绝的四类机制**)均在场;
  5. MUST 与 MUST NOT 关键词齐备;
  6. 两份清单存在、非空、**每条携判据**(判定形态见 FR-076);
  7. FR-016 点名的 **7 项**已实测失效形态在清单中逐项可定位;
  8. 机械测试 [[STR-005]] 与 [[STR-006]] 在文档中各出现;
  9. FR-073 要求的爆炸半径可判定定义在场;
  10. FR-068 要求的封闭处置集在场;
  11. FR-067 要求的干净运行显式陈述义务在场;
  12. FR-063 要求的标记互斥性规则在场;
  13. FR-070 要求的"判据优先于清单命中"顺序声明在场;
  14. FR-071 要求的"异常停不计入既有失败规则"排除声明在场;
  15. FR-074 要求的 canonical 指针行恰好一行,且声明所覆盖的界面类编号;
  16. FR-040 的观察标记字面量 [[STR-001]] 在场,且 FR-041 的两条红线(干净运行不追加空洞条目、不编造数值)在场;
  17. FR-044 的双向生长规则与 FR-045 的留痕要求在场;
  18. FR-029 点名的既有实例点位各含且仅含一行指针;
  19. 常驻章节 [[STR-003]] 在模板与活动指令文件中各出现且仅出现一次;
  20. 模板不内联真源文档的节名;
  21. `shared/` + `templates/` 单源扫描无第二处定义点;
  22. 文档项目中立。
- **FR-036**: 本特性的**全部新增文本**MUST 对门控扫描器的阻塞模式**逐行零命中**。新增文本的封闭枚举为:真源文档、常驻章节、宪章原则与命令 `MUST include` 条目、FR-029 新增的指针行、以及 FR-062 的三个结构性落点(其中两个——团队载荷模式与子代理概念文档——本身就在扫描范围内)。因扫描器**以"命中的行"为计数单位**,零命中的判据是逐行的,不是逐文件的。具体 MUST 规避两类形态:
  - **停止语义**:表达"停在异常点并交用户裁定"时 MUST 用不命中等价表述,MUST NOT 使用「等待用户确认」「stop and confirm」「确认后执行」「确认门禁」「explicit user confirmation」等命中形态。
  - **相邻纪律的名字**(clarify 2026-09-22 第二轮补入):阻塞模式含 `确认门[禁控]`,而「确认门控治理」逐字命中它。真源文档 MUST 以**路径**(`shared/guidelines/confirmation-gates.md`)指称该相邻纪律,MUST NOT 在真源文档、常驻章节或宪章原则正文中写出其中文名;本规格与 `contracts/` 属 `.specify/` 下、不在扫描范围,故可自由使用该名。规避改写的两条配套义务见 FR-064 与 FR-065。
- **FR-037**: 本特性 MUST NOT 修改门控扫描器源码:`POLICY_DOCS`、`SELF_REL` 字面量与 `BLOCKING_PATTERNS` 条数 MUST 保持不变;处置取**设计规避**,MUST NOT 通过扩大豁免集或调整冻结基线来通过门禁。
- **FR-038**: 变更后实跑门控扫描器,MUST 满足 total 与 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json` 的冻结值**相等**(而非 ≤)且 violations 为空;该冻结基线文件是 total 的唯一拥有者,本规格与守卫 MUST NOT 复述其数值字面量。
- **FR-039**: 镜像同步与按工具副本再生 MUST 由既有引擎完成;命令模板改动后 MUST NOT 手工批改 `.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/` 下的副本。

#### 观察与提升闭环

- **FR-040**: 触发快速失败或执行顺手修复的运行,MUST 在其反馈优化点条目行内嵌稳定观察标记 [[STR-001]],使其可被既有反馈引擎按该标记检索聚合;MUST NOT 为此新增引擎能力或标记注册表。
- **FR-041**: 干净运行 MUST NOT 追加空洞的观察条目;MUST NOT 编造任何数值。
- **FR-042**: 快速失败上送后用户作出裁定时,决定信号 MUST 沿用既有门控观察协议的四值词汇(approved-as-is / modified / asked-questions / denied),该词汇 MUST 以指针引用,MUST NOT 复述其记录字段与红线。
- **FR-043**: 观察记录 MUST 复用**触发单元既有的 probe** 加标记的方式;MUST NOT 向 probe 注册表新增 probe 类或 probe 对象。
- **FR-044**: 真源文档 MUST 载明**双向生长规则**(clarify 2026-09-22 用户裁定,取代原单向提升规则):一个异常类被两次独立观察命中("两次独立观察"按**独立键 = `(发现点, 被证伪的预期)` 二元组**认定——独立性恰恰要求发现点**不同**,故本键 MUST NOT 与 FR-014 的复发键混用;2026-09-23 用户裁定)、或被一次用户直接纠正命中,MUST 被移进**纠正/观察所指的那一份**清单——升到 fast fail 清单与降到顺手修复清单走同一套证据资格,以修订真源文档的形式进行;移动后原处的局部措辞 MUST 收敛为指针,MUST NOT 保留第二份独立清单。**两份清单的证据资格 MUST 对称**:MUST NOT 只存在朝"停止"一侧的通道,因为单向棘轮会使清单朝"越来越多东西要停"漂移,而一条停得太频繁的纪律最终会被绕过。
- **FR-045**: 每次清单移动(升级或降级)MUST 留痕:能对应到至少一条含标记的观察记录,或一次**可定位的**用户直接纠正("可定位"= 能指向具体的反馈条目 ID、提交、或会话中的一句原话);MUST NOT 静默调整清单直到出现有利结果。
- **FR-046**: 自省入口 MUST 复用既有的反馈自省路径消费该标记,MUST NOT 新增自省命令或流程。

#### 子代理派发注入(2026-09-22 追加输入)

- **FR-047**: 真源文档 MUST 载明一条**派发期义务**:每一次子代理派发 MUST 使注入子句在子代理读得到的位置**物理在场**。该义务的形态对齐既有的外部派发可见性契约(同为挂在"派发"这个动作本身上的编号 MUST + 一句失效判词),但 MUST NOT 复述其内容——可见性契约拥有"这次派发是否**可观测**",本条拥有"这次派发是否**受治理**"。
- **FR-048**: **注入子句**MUST 是一段**有界的固定形态字面量**,其文本由真源文档**单点拥有**;它 MUST 至少承载三件事:二值分流判据(纠正 vs 裁定)、"需要裁定时停在本层并回抛编排者、MUST NOT 就地修平"的义务、以及异常回传的固定前缀 [[STR-010]]。它 MAY 另携真源文档路径 [[STR-002]] 以抵达完整清单,但 MUST NOT 以"路径可达"**替代**上述三项中的任何一项——一个必须先打开文件才知道该不该停的子代理,已经失去了这条保证。子句的**长度上限**由真源文档作为唯一定义点拥有(本规格不设数值);该上限 MUST 与 Token 效率纪律相容,因为子句随每一次派发复制。
- **FR-049**: 注入子句 MUST 携一个固定标识字面量 [[STR-009]],使"子句是否在场"成为一次**子串判定**而非语义判断(可判定的事交给程序,不交给模型裁量)。
- **FR-050**: 注入 MUST 覆盖**三条派发通道**(三者**不互斥**——一次派发可同时经由通道一撰写提示并携带通道二的制品,派发链的后续跳亦然),并按"谁撰写提示"分流落点:
  - **通道一 · 编排者当场撰写的内联提示**(占派发面多数):义务经常驻章节 [[STR-003]] 抵达编排者——编排者本身读得到常驻层;真源文档 MUST 规定子句在该提示中的落点与形态。
  - **通道二 · Agent 定义制品**(Template / Instance / 派发配置):其执行进程**读不到**常驻层,故子句 MUST 物理存在于该制品中。**义务的绑定对象是"制作者要求",不是一份被枚举的文件清单**(clarify 2026-09-22 用户裁定):落点为 `/speckit.agents` 命令模板的 Run Mode、`create-agent` 技能的创作契约、以及随包出厂的 Agent 预设;日后新建的 Instance 因**经这条创作路径产生**而自动携带。理由:实测 `.specify/agents/instances/` 与 `execution/configs/` **今天均为空**且由用户日后创建,守卫无法枚举一个无界集合;绑定制作者要求使守卫面对的是一个**有界**集合(出厂预设 + 创作要求文本)。
  - **通道三 · 团队 Per-Agent Payload**:子句 MUST 进入既有载荷模式并在该模式中被点名,使团队派发与普通派发受同一约束;MUST NOT 为它另立一套团队专用规则。其在五字段表中的落点(新增第六字段 vs 并入 `task_brief` 的内容规则)由 `/speckit.plan` 裁定,但 MUST 使守卫能判别该子句在场与否。
- **FR-051**: 注入 MUST NOT 通过新增"所有 agent 继承的共享资产/前导文件"实现:Agent 定义制品按既有定义为**自包含**且其存储下无共享资产目录。子句 MUST 以**内联有界字面量**落地;真源文档路径 MAY 作为**附加**引用随行,但 MUST NOT 作为子句三项必备内容的替代(见 FR-048)。
- **FR-052**: 通道二与通道三中的子句副本属**守卫钉死的合法重复**(唯一真源纪律三类合法重复中的第二类:钉在测试里以探测漂移),**不是**机器可再生的副本——实测无任何既有引擎会再生它们(`regen-command-copies.py` 只处理 `templates/commands/*.md`,Agent 渲染方向是 canonical → 按工具副本,与本方向相反)。因此:副本 MUST 与真源文档中拥有者的字面量**逐字节一致**,守卫 MUST 断言该一致性;拥有者字面量 MUST 由**成对定界符**包围,使守卫能从宿主文件中机械提取被比对的子串(否则"逐字节一致"无从断言);漂移的修复路径 MUST 是**从拥有者手工重灌**,MUST NOT 就地改写副本而成为第二定义点。
- **FR-053**: **派发前自检**:编排者 MUST 在发出派发**之前**确认 outgoing 提示/载荷含 [[STR-009]]。该义务形态对齐既有的可写性预探针("MUST NOT 让一个阶段在中途才发现目标不可写")。**缺失的处置按发现时点分流**(clarify 2026-09-22 用户裁定):
  - **派发前发现** → **顺手修复**:补齐子句后照常派发,并把补齐并入收尾报告披露。此时 FR-010 的四条同时成立(恰有一种读法、改动局部可逆、补齐后无证伪前提残留、半径不越本动作)。
  - **派发后才发现** → **快速失败**:子代理已不受治理地跑过,改提示无法撤销该事实,而"已完成的那部分工作是受治理的"这一前提已被证伪。编排者 MUST 停下上送,MUST NOT 把该子代理的产出当作可信证据继续消费。
- **FR-054**: **回传显式异常行**:每个子代理的回传 MUST 含一条显式异常陈述——有异常则逐条以 [[STR-010]] 前缀列出,无异常则明写 [[STR-013]]。编排者 MUST NOT 把缺少异常行的回传读作干净。这是**反空真哨兵**在派发面上的应用:使"因干净而空"与"因没收到规则而空"可区分。
- **FR-055**: **异常停 ≠ 普通失败**:编排者收到带 [[STR-010]] 的回传 MUST 判为"异常停",MUST NOT 原样重派或要求其"再试一次";既有的两振停滞与"连续两次派发失败即降级"规则 MUST NOT 把一次异常停计为上游失败(那两条针对的是 upstream error 与结构性停滞)。重派一次异常停,等于在上一层重新犯下静默兜底。
- **FR-056**: **子代理不拥有用户通道**:面向用户的四要素上送件 MUST 由编排者组装。上送件的所有权因此分层——子代理拥有"异常事实",编排者拥有"上送件";注入子句 MUST 让子代理回抛编排者,而非尝试直接面向用户。
- **FR-057**: 注入义务 MUST 对三种执行模式(native / virtual / external)**同等成立**;virtual 模式 MUST NOT 因"会话本身持有常驻层"而豁免——该模式的隔离是**约定**而非运行时强制,跳过注入会使那条边界变成假的。
- **FR-058**: 注入 MUST 是**调用方的内容义务**,MUST NOT 被实现进外部派发包装器:包装器只覆盖 external 一种模式(无法覆盖 native 与 virtual),且其既有分工为"机制归包装器、内容归调用方"。据此本特性 MUST NOT 修改派发包装器或其流过滤脚本,亦 MUST NOT 修改任何既有引擎源码。
- **FR-059**: **派发链传递**:注入义务 MUST 随派发链**逐跳重新履行**;被派发的子代理再派发下一跳时 MUST 重新注入,MUST NOT 假定"我收到过所以下游也有"——每一跳都是一次新的隔离边界。
- **FR-060**: 真源文档 MUST 声明注入子句与 Agent 定义正文冲突时的**裁决顺序**(框架级纪律优先于角色级约定),且该冲突本身 MUST 作为一次异常回抛编排者,MUST NOT 由子代理自行择一。
- **FR-061**: 守卫 [[STR-007]] MUST 增断言:注入子句的拥有者定义在真源文档中在场;通道二与通道三各携该子句且与拥有者**逐字节一致**——通道二的断言对象是**有界集合**(随包出厂的 Agent 预设 + `/speckit.agents` 命令模板 Run Mode 与 `create-agent` 创作契约中的制作者要求文本),MUST NOT 试图枚举 `.specify/agents/instances/`(实测为空且由用户日后创建,枚举一个无界集合的守卫要么漏要么恒红);[[STR-009]] 与 [[STR-010]] 两个字面量在真源文档中各出现;FR-047 的派发期义务、FR-052 的成对定界符、FR-053 的派发前自检与时点分流、FR-054 的回传显式异常行、FR-059 的派发链逐跳、FR-060 的裁决顺序——六条义务均 MUST 被断言在文档中在场。
- **FR-062**: 注入侧的收敛范围 MUST 有界:本特性 MUST 把义务写进真源文档 + 三条通道的**结构性落点**(Agent 定义制品的制作者要求、团队载荷模式、子代理概念文档的派发期义务处),MUST NOT 逐个改写现状锚点中点名的内联派发点位——那些点位由编排者当场撰写,义务经常驻层抵达(FR-050 通道一)。**通道一的合规性不可被契约测试观测**(编排者当场撰写的提示不落盘,无制品可断言),故它由**评审**而非测试强制;真源文档与 `/speckit.plan` MUST 如实标注这一边界,MUST NOT 声称"三条通道均由守卫覆盖"——声称覆盖了实际覆盖不到的东西,正是本纪律要治理的盲检类失效。

#### clarify 2026-09-22 第二轮补入(四路检测发现的缺口)

- **FR-063**: **标记互斥性**——三个稳定字面量 MUST 互不为子串,且 MUST NOT 出现在承载它们的规则正文里。实测缺陷:`fast-fail` [[STR-001]] 是 `fast-fail-clause` [[STR-009]] 与路径 [[STR-002]] 的子串,而引擎按大小写不敏感子串匹配,故任何只是**提到**该纪律或其路径的反馈行都会被计为一次观察命中,使 FR-041"干净运行 MUST NOT 追加空洞条目"在机械上不可判别;另一侧,FR-048 要求子句本身携带 [[STR-010]],于是**引用子句原文**的回传会命中 FR-055 的"收到带该前缀的回传 MUST 判为异常停"。真源文档 MUST 为三者规定互斥形态(例如各自带不可被另一方包含的定界),并使"提到纪律"与"报告一次观察/异常"在机械上可区分。
- **FR-064**: 为规避门控扫描器而做的改写 MUST 限于**措辞**;MUST NOT 通过改写清单条目或边界规则的**语义**来达成零命中。语义漂移是本特性唯一没有守卫的修改路径,故 FR-065 使其可观测。
- **FR-065**: 任何因规避扫描器而发生的措辞改写 MUST 触发 SC-001 的双评审者一致性复跑(与"清单每次移动后复跑"同等对待),并 MUST 在真源文档的修订记录中留痕,注明是为规避哪一个模式。
- **FR-066**: **回传缺少异常行本身即一次异常**——它既不是"异常停"(无 [[STR-010]] 前缀)也不是"干净"(无"未发现异常"陈述),MUST NOT 被默认为后者。编排者 MUST 按存疑从严处理:把该回传判为**不完整**,MUST NOT 消费其结论作为证据。是否重派由 FR-071 约束(重派 MUST NOT 用来"再试一次"以绕过异常停)。
- **FR-067**: **干净运行也要显式说一句**——当一次运行既无快速失败也无顺手修复时,其收尾报告 MUST 含一条显式陈述,以 [[STR-013]] 起首并明写"无就地修复"。反空真哨兵 MUST 应用到**最外层面向用户的那一面**,而不只应用在子代理回传上:否则一次干净运行与一次完全没受治理的运行对用户不可区分——那正是本特性要消除的混淆,在最外层复现。
- **FR-068**: **可选处置集 MUST 封闭且由真源文档拥有**——上送件第四要素"可选处置"MUST 从真源文档所载的一个封闭处置集中取值(至少含:按建议处置 / 改为顺手修复并继续 / 照原样继续 / 终止本次运行),MUST NOT 由报告方临时发明。理由:临时发明处置就是在发明工件未记录的意图,而那按本纪律自己的判据属快速失败。
- **FR-069**: **观察记录 MUST NOT 依赖运行活到收尾**——快速失败会终止动作链(FR-027),故含标记 [[STR-001]] 的观察 MUST 由**上送件自身**承载(上送件落盘即留痕),而不是等到反馈收尾步才记录;否则价值最高的那批观察会被系统性丢失,提升/降级闭环因此断粮。
- **FR-070**: **判据优先于清单命中**——FR-010 的四条是**必要条件**:即使一处异常命中顺手修复清单,只要四条中任一条不成立,MUST 归快速失败。清单命中 MUST NOT 被读作充分条件。此顺序 MUST 在真源文档中显式声明,因为两位复核者按"清单优先"与"判据优先"会得出相反结论,而 SC-001 把分歧判为判据缺陷。
- **FR-071**: **异常停不计入既有的任何失败规则**——除 FR-055 已排除的两振停滞与"连续两次派发失败即降级"之外,异常停同样 MUST NOT 被计为既有"非并行任务失败即停/并行任务成功者继续、失败者上报"规则中的一次**失败**;它是一次**上送**,不是一次失败。真源文档 MUST 点名该规则并声明这一排除,否则"异常停在被委托规则下算什么"没有答案,而两种读法给出相反的下游行为。
- **FR-072**: 两条今天只存在于边界情形、没有 FR 载体的义务 MUST 获得载体:(a) 异常出现在**只读命令**中时,上送 MUST 走"报告 + 请求批准"形态,与既有只读命令的补救批准例外同型;(b) **既有实例点位与新判据冲突**时(某处已写"失败即停"而新判据判为可顺手修),真源文档 MUST 声明裁决顺序,冲突 MUST 在该文档内解决。
- **FR-073**: **爆炸半径 MUST 被定义**——它是 FR-010(d) 的四条必要条件之一,又是 FR-013 的裁决理由,却在今天只作为一个裸属性出现。真源文档 MUST 给出可判定定义(建议形态:本次修复会触及的工件集合是否超出**当前动作在其所属工件中声明的范围**),并 MUST 使两位复核者能独立复现该判定;未定义时 SC-001 的 100% 一致率不可达。
- **FR-074**: 真源文档 MUST 满足面向用户可理解性纪律对**规则真源文件**的既有要求:在其头部所有权区携带**恰好一行** canonical 指针,声明本文件覆盖该纪律界面类封闭集中的哪几类。FR-002/FR-007/FR-035 今天均未要求它。
- **FR-075**: 真源文档 MUST 载明四条今天缺失的处置规则:(a) **一次运行内多处并发异常**——上送件 MUST 合并还是逐条,以及第二处异常在第一处待裁定期间出现时的处置;(b) **裁定 ping-pong 的上限**——同一异常在一次运行内被反复上送/裁定 MUST 有上限,超限即升级(否则 FR-014 的两振规则与"一次裁定只豁免这一次"合起来会造成无界往返);(c) **跨会话既有裁定的检索**——上送前 MUST 先查该类异常是否已有既往裁定,因为"同一个问题不需要问第二遍"是既有纪律的要求,而该纪律今天不在 FR-028 的边界清单里;(d) **真源文档自身出现异常**(两份清单互相矛盾、判据不可读)时的处置——MUST 上送,MUST NOT 择一执行,形态对齐既有的"门禁不可读即上报"先例。
- **FR-076**: 为使 FR-035 第 6 项可机械断言,两份清单的条目 MUST 采用**固定条目语法**(每条一行、以统一前缀起始、类名与判据以固定分隔符分开),该语法由真源文档拥有。没有条目语法,"每条携判据"就只能退化为"该节非空"——那正是本规格在 [[STR-006]] 里禁止的空转断言。
- **FR-077**: **常驻章节 MUST NOT 声称一个不存在的恢复能力**(clarify 2026-09-22 第二轮补入,由检测证伪一处既有房式措辞而来)。实测:`/speckit.instructions` 与其生成脚本**不做**镜像同步,`shared/` → `.specify/shared/` 的复制只发生在 CLI 的资产复制路径(`copy_local_templates()`,由 `specify init` 调用)。因此常驻章节在表述"真源文档缺失时如何恢复"时,MUST 指名**真实的恢复路径**(重新执行 CLI 的初始化/资产复制),MUST NOT 沿用既有纪律常驻章节里"刷新项目指令即连同其镜像副本一并恢复"这一句式——该句式经本轮实测**不成立**,照抄会把一条假承诺送进每个下游项目,而悬空指针按房子规则会导致命中它的命令中止。本特性 MUST NOT 为此修改 `generate-instructions.sh`(Out of Scope);该既有句式在本仓其他常驻章节中的同类问题属**上游缺陷**,MUST 单独上报,MUST NOT 由本特性顺手改写(那会是一次未获授权的爆炸半径越界)。
- **FR-078**: 真源文档 MUST 载明**已接受的代价**:因门控预算整数余量为 0 而取设计规避(FR-036/FR-037),本纪律的措辞从此**永久受制于一个与本纪律无关的扫描器的模式清单**——日后每一次修订真源文档都要先躲开那 17 条模式。该代价 MUST 被显式记为已接受(而非隐含),并 MUST 由 FR-064/FR-065 约束其唯一的恶性形态(为躲模式而改语义)。一条未被写下的代价会在下一次修订时被当作"莫名其妙的约束"而被绕过。

### Key Entities *(include if requirement involves data)*

- **真源文档 (Truth-Source Doc)**: 本纪律的唯一拥有者制品 [[STR-002]]。属性:所有权声明、必备 H2 节集、范围限制子句、canonical 指针行(FR-074);关系:与 `.specify/` 镜像副本逐字节一致(FR-004),被常驻章节以指针引用(FR-005/FR-006),被宪章原则以路径援引(FR-034)。它是本模型中唯一"被多方引用而不引用他方规则正文"的节点。
- **异常 (Anomaly)**: 执行期发现的、与已记录预期不符的状态。属性:发现点(哪个单元/哪个动作)、被证伪的预期、爆炸半径(FR-073 定义)、是否可逆、分流结论、**所属异常类**。**同一性键(2026-09-23 用户裁定:拆为两个键,不再共用一个)**:**复发键 = `被证伪的预期` 单键**,供 FR-014 的"同一异常第二次出现"判定——复发看的是同一个被推翻的预期,与在哪里再次撞到它无关;**独立键 = `(发现点, 被证伪的预期)` 二元组**,供 FR-044 的"两次独立观察"判定——独立性恰恰要求发现点不同。初版把两者合为一个二元组,使 FR-014 在跨发现点复发(即最常见形态)下不可达;两条规则需要的粒度本就相反,故 MUST 各用其键。
- **异常类 (Anomaly Class)**: 清单的一行;异常按类归类,清单按类生长。属性:类名、判据一句、所属清单(上送极/修复极)、条目语法下的固定形态(FR-076)。关系:一个异常归属恰好一个类;未归入任何类的异常按存疑从严归快速失败(FR-012),并成为生长规则的候选输入。**这是本模型的核心节点**——"命中"这个动词(整套判据围绕它转)只在类这一层有意义,异常实例本身不被清单直接命中。
- **分流结论 (Classification Verdict)**: 二值——顺手修复 / 快速失败。MUST 可由第二位复核者独立复现。**生命周期**:初判 → (双评审分歧) → 判据缺陷待修订(FR-011 使不可复现成为修订触发器,故该状态 MUST 可表达,而不是被当作"两位评审者都对")。
- **fast fail 清单 / 顺手修复清单**: 两个封闭、可枚举、保守的异常类集合,同住真源文档;每条携一句判据;扩展只经修订该文档。二者是**同一个模型的两极**,不是两个独立实体:一个异常类在任一时刻归属其中之一,生长规则(FR-044)可在两极间移动它。
- **上送件 (Surface Report)**: 快速失败时交付用户的消息,四要素(发现了什么 / 为何吃重 / 已产生的中间产物 / 可选处置);第四要素从真源文档拥有的**封闭处置集**取值(FR-068);界面类归 ⑪ 失败如实报告(FR-024);**自身携观察标记** [[STR-001]],使其落盘即留痕、不依赖运行活到反馈收尾(FR-069)。
- **披露条目 (Disclosure Row)**: 顺手修复在收尾报告中的一行,承载"修了什么 + 为何是纠正而非裁定 + 所采用的解读"。干净运行时该行位置 MUST 由一条显式的"未发现异常、无就地修复"陈述占据(FR-067)。
- **观察条目 (Observation Entry)**: 携标记 [[STR-001]] 的反馈条目;生长规则的证据来源。**生命周期**:`open` → `已计入一次清单移动` → `已消费`;终态 MUST 可表达,否则同一条观察可被 FR-044 计入两次移动。
- **清单移动 (List Move)**: 一次把某异常类在两极间移动(升级或降级)的变更,取代原单向的"提升"。**生命周期**:`proposed`(有证据) → `moved`(已修订真源文档) / `rejected`(证据不足);`rejected` 态 MUST 可表达且 MUST 被如实记录(边界情形"有人提议调整清单以便某个门禁通过"要求它存在)。MUST 留痕到证据或用户纠正(FR-045)。
- **裁决记录 (Decision Record)**: 用户对一次上送件的裁定及其决定信号(四值词汇引用既有门控观察协议)。由 **FR-042**(信号词汇)、**FR-075(b)**(裁定 ping-pong 上限)与边界情形"一次裁定只豁免这一次"共同消费;只豁免该次,MUST NOT 回写为清单通用例外——但 MUST 可被下一次上送前的检索命中(FR-075(c)),否则"同一个问题不需要问第二遍"不成立。
- **用户直接纠正 (Direct User Correction)**: 生长规则的第二类证据,与"两次独立观察"并列且**一次即充分**(引用既有资格判据)。属性:纠正方向(朝上送极 / 朝修复极)、可定位指针(反馈条目 ID / 提交 / 会话原话)。方向决定清单移动的朝向(FR-044)。
- **编排者 (Orchestrator) 与 子代理 (Subagent)**: 一对角色,上送件所有权按层分置于二者之间(FR-056)——子代理拥有"异常事实",编排者拥有"上送件"。关系:编排者派发子代理并消费其回传;子代理 MUST NOT 假定自己拥有用户通道。
- **Agent 定义制品 (Agent Definition Artifact)**: 通道二的物理载体(Template / Instance / 派发配置)。属性:所属层、是否出厂预设、是否携注入子句。关系:义务绑定的是**制作者要求**而非制品清单(FR-050 通道二),故守卫面对的是一个有界集合(FR-061)。
- **执行模式 (Execution Mode)**: 三值枚举 native / virtual / external,取自既有子代理概念文档。注入义务对三者同等成立(FR-057);virtual 模式的隔离是**约定**而非运行时强制,故不因"会话本身持有常驻层"而豁免。
- **派发链跳 (Dispatch Hop)**: 派发链上的一次派发。注入义务**逐跳重新履行**(FR-059):每一跳都是一次新的隔离边界,上游收到过子句不构成下游也有。
- **注入子句 (Injection Clause)**: 一段有界、固定形态、由真源文档单点拥有的字面量,在派发时物理进入子代理读得到的位置;携固定标识 [[STR-009]] 以便子串判定,并由**成对定界符**包围以便守卫从宿主文件中机械提取比对(FR-052)。承载分流判据 + 回抛义务 + 回传前缀三件事;长度上限由真源文档单点拥有(FR-048)。
- **派发前自检 (Pre-Dispatch Probe)**: 编排者在发出派发之前对 outgoing 提示/载荷做的一次子串判定。与既有可写性预探针同型——把失败发现点从中途移到事前。**缺失的处置按发现时点分流**(FR-053):派发前发现属顺手修复,派发后才发现属快速失败。
- **异常回传行 (Anomaly Return Line)**: 子代理回传中必须出现的显式陈述,有异常则以 [[STR-010]] 前缀逐条列出、无异常则明写"未发现异常";使沉默不可被读作干净。**缺行本身即一次异常**(FR-066),构成第三态,既非异常停也非干净。
- **派发通道 (Dispatch Channel)**: 三条注入落点——编排者当场撰写的内联提示 / Agent 定义制品 / 团队 Per-Agent Payload。三者**不互斥**:一次派发可同时经由通道一撰写提示并携带通道二的制品,派发链的后续跳亦然(FR-050)。通道决定子句是经常驻层抵达还是必须物理内联;通道一不可被测试观测(FR-062)。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对一组不少于 10 个异常场景样本(清单命中与未命中各占约一半),两位互不通气的独立复核者按真源文档得出的分流结论一致率为 **100%**;出现分歧即判据需修订,而非样本 ambiguous。
- **SC-002**: 房子历史中已实测的失效形态——盲检四成因与 `git diff` 三形态陷阱(合计 7 项)——在 fast fail 清单中的覆盖率为 **7/7**(每项或对应一条清单条目,或可归入某条并在其判据中被点名)。
- **SC-003**: 该纪律在仓库内的**独立措辞定义点数为 1**;守卫对 `shared/` 与 `templates/` 的复述扫描命中数为 **0**(真源文档自身除外)。
- **SC-004**: 指令模板与活动指令文件的顶级章节集合差为 **0**,即新增常驻章节抵达所有已初始化项目;既有章节被改动的数量为 **0**。
- **SC-005**: 变更后实跑门控扫描器:total 与冻结基线**相等**、violations 为 **0**、扫描器源码 diff 为**空**;新增文本对阻塞模式的命中数为 **0**。
- **SC-006**: 下游即得——宪章模板与命令 `MUST include` 清单中该原则各命中 **1** 次;活动宪章原则数 **+1** 且版本 **≥ 1.13**;`plan-template.md` 改动为 **0** 而其渲染出的门控行数 **+1**。
- **SC-007**: 观察闭环可用——写入一条含标记的反馈条目后,按该标记检索的命中数为 **1**;清单每次提升对应至少 **1** 条观察记录或 **1** 次可定位的用户纠正,留痕率 **100%**。
- **SC-008**: 上送可行动——对上送件样本做读者测试,读者**在未打开任何其他工件**的情况下能够从所提供的处置集中**选出一项并说明选择理由**的比例为 **100%**。判定 MUST NOT 以"四要素标题齐备"为通过条件(那是循环判定:一份把读者逼进死胡同的报告同样有四个标题),而 MUST 以"读者能否据此行动"为条件;处置集取值合法性按 FR-068 核对。
- **SC-009**: 零静默兜底——一次运行内全部顺手修复在收尾报告中逐项可见,披露率 **100%**;收尾报告因披露而新增的打断次数为 **0**(琐碎修复合并呈现);**干净运行的显式陈述在场率为 100%**(FR-067),使干净运行与未受治理的运行对用户可区分。
- **SC-010**: 既有实例点位(FR-029 点名者)各含且仅含 **1** 行指向真源文档的指针,其行为正文被改写的行数为 **0**。
- **SC-011**: 派发面覆盖率为 **3/3**——三条派发通道各有一个结构性落点携注入子句;通道二与通道三所携副本与真源文档中拥有者的逐字节一致率为 **100%**。
- **SC-012**: 派发前自检经一次完整**变异演练**取证:从 outgoing 提示中移除标识字面量 [[STR-009]] 后自检报缺失、复原后自检通过,四步(弄坏 → 变红 → 复原 → 恢复绿)取证齐全,演练用临时制品清理干净且计数归零。
- **SC-013**: 回传纪律分两侧度量,因为二者的可达性不同(clarify 2026-09-22 第二轮修正:原文对子代理侧要求 100% 且无补救路径,而子代理是模型执行体,一条无容差带、无补救路径的 100% 判据不可达,也就不可守):
  - **编排者侧(可控,MUST 达 100%)**:缺少异常行的回传被编排者判为**不完整**、且其结论未被当作证据消费的比例为 **100%**——这是编排者自己的行为,可断言。
  - **子代理侧(概率性,度量而非门禁)**:含显式异常行的回传比例被**记录并报告**,不设通过阈值;该比例是注入子句有效性的观测信号,其下降 MUST 触发对子句文本的复核(FR-065 同款留痕),而不是触发一次红的门禁。
- **SC-014**: 对带 [[STR-010]] 前缀的回传,编排者**原样重派**的次数为 **0**;每次异常停的后续动作为"上送用户"或"记录为未决项"二者之一。
- **SC-015**: 过度触发可观测(clarify 2026-09-22 用户裁定新增)——一段时期内必须同时报告三个数:**快速失败率**(快速失败次数 / 分流判定总次数)、**用户推翻率**(裁定为"本该顺手修"的次数 / 快速失败次数)、**清单净生长方向**(升至上送极的类数 − 降至修复极的类数)。三者 MUST 可由含标记 [[STR-001]] 的反馈条目聚合得出,不设通过阈值;其作用是使"这条纪律正在被绕过"成为有数字的信号——**用户推翻率持续偏高而清单净生长仍为正**,即单向棘轮正在生效的判据。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 场景样本集由本特性的验证工件承载(取自 `docs/reference/history/00-cross-cutting-lessons.md` §十二–§十四 的已实测案例 + 清单未命中的构造案例);双评审在两个互不共享上下文的只读子代理中独立进行,结论以逐场景对照表落盘。基线:不适用(该判据今天不存在)。测量时机:实现完成时一次,清单每次提升后复跑。
- **SC-002 Source**: 契约测试 [[STR-007]] 中的覆盖断言——对 7 项已实测失效形态逐项断言其在清单中可定位(按判据文本或按指向教训文档小节的引用)。基线:今天为 0/7(清单不存在)。每次运行契约套件时测量。
- **SC-003 Source**: 契约测试的单源扫描(对 `shared/` 与 `templates/` 递归,跳过真源文档自身),断言判据关键句与清单节名的命中数为 0。同形先例:`test_one_source_of_truth.py:142-153`、`test_token_efficiency_discipline.py:94`。每次运行契约套件时测量。
- **SC-004 Source**: 既有守卫 `tests/contract/test_instructions_section_propagation.py` 加本特性新增断言(章节各出现且仅出现一次);指令再生实跑后比对模板与活动文件的顶级章节集合。每次运行契约套件时测量。
- **SC-005 Source**: 实跑 `scripts/python/scan-confirmation-gates.py` 并与其 `--baseline` 模式对照冻结基线 `.specify/specs/050-proactive-flow-trigger/baseline-gates.json`;扫描器源码 diff 由版本控制实测;零命中由契约测试对新增文本逐个断言。基线:2026-09-22 实测 total = 23(该数值的唯一拥有者是冻结基线文件,本行仅作日期化记录)。测量时机:实现完成时、以及任何后续新增文本落位后。
- **SC-006 Source**: 既有守卫 `tests/contract/test_constitution_double_landing.py`(四个钉子同批上调后实跑)+ plan 门控渲染实测(对一个样例项目跑 plan 模板枚举逻辑,数行数)。每次运行契约套件时测量。
- **SC-007 Source**: 既有反馈引擎按标记检索的实跑结果(写入一条 → 检索命中 1 条);提升留痕由真源文档的修订记录与反馈存据交叉核对。测量时机:实现完成时一次,此后每次清单提升时。
- **SC-008 Source**: 上送件样本的读者测试——以面向用户可理解性纪律的**基准读者定义**为准(引用,不复述),由独立子代理在只有该消息、无其他工件的条件下**选出一项处置并说明理由**;判定记录"能否选择",不判定"标题是否齐备"。样本取自 SC-001 的场景集中判为快速失败者。基线:今天不存在上送件这一制品。测量时机:实现完成时一次,处置集每次修订后复跑。
- **SC-009 Source**: 对一次含多处顺手修复的真实运行做收尾报告核对(逐项可见性 + 打断次数),外加对一次**干净**运行核对其显式陈述是否在场。基线:今天的收尾报告既不含修复披露项、也不含干净运行的显式陈述。测量时机:实现完成时一次(须含干净与含修复两种运行各一),此后抽样。
- **SC-010 Source**: 契约测试逐点位断言"含且仅含一行指针"与"行为正文未被改写"(以变更前冻结的正文快照为对照)。测量时机:实现完成时。
- **SC-011 Source**: 契约测试 [[STR-007]] 逐通道断言——通道一断言真源文档载明内联提示中的落点与形态;通道二断言 Agent 定义制品携子句且与拥有者字节相等(复用既有 `DOC.read_bytes() == MIRROR.read_bytes()` 惯用法);通道三断言团队 Per-Agent Payload 模式点名该子句。基线:今天为 **0/3**——既有纪律对"自己如何抵达子代理"全部零表述(实测 `shared/guidelines/` 12 份中 0 份提及子代理),派发期唯一的框架级 MUST 是可见性契约(管观测,不管行为)。每次运行契约套件时测量。
- **SC-012 Source**: 变异演练实跑取证(房子既有手法,见 `docs/reference/history/00-cross-cutting-lessons.md` §十二 配套手法一);临时制品清理以计数归零复核。基线:今天不存在派发前自检,故无演练对象。测量时机:实现完成时一次,注入子句文本每次修订后复跑。
- **SC-013 Source**: 对一次真实并行派发的回传集逐条核对;取样面为团队运行报告既有的 label → CLI → member → workspace 映射表(该表由既有可见性契约第 5 点规定,是本特性可直接复用的现成索引)。**编排者侧**由契约测试断言(把一条缺异常行的回传喂给处置逻辑,断言其被判为不完整且结论未被消费——这是一条可机械化的断言,与 SC-001 的双评审测试不同);**子代理侧**由上述回传集统计得出并记入报告,不进任何门禁。基线:今天的回传不含异常行,沉默被默认读作干净。测量时机:实现完成时一次,此后抽样。
- **SC-014 Source**: 与 SC-013 同批取样,核对编排者对每条异常停回传的后续动作(原样重派 / 上送用户 / 记为未决项 三分类),由运行报告与提交历史交叉核对。基线:今天异常停与普通失败在回传上不可区分,故重派无从避免。测量时机:与 SC-013 同批。
- **SC-015 Source**: 三个数全部由既有反馈引擎按标记 [[STR-001]] 聚合得出——快速失败率与用户推翻率取自观察条目与裁决记录的决定信号(四值词汇中 `modified` 与 `denied` 计入推翻),清单净生长方向取自真源文档的修订记录(每次清单移动 MUST 留痕,FR-045,故可数)。MUST NOT 为此新增计数器、台账或仪表盘(Out of Scope 的零新机制约束);三个数是**由既有存据导出的**,不是被另行维护的。基线:不适用(今天无标记、无裁决记录、无清单)。测量时机:每次清单移动后,以及 `/speckit.feedback` 自省路径运行时。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "[fast-fail]" | FR-040, FR-063, FR-069, SC-007, SC-015, 契约测试的观察标记断言(FR-035 第 16 项), 反馈条目优化点行, 上送件自身 |
| `STR-002` | "shared/guidelines/fast-fail.md" | FR-001, FR-004, FR-031, FR-034, 契约测试的文档路径与镜像断言, 宪章原则的指针要点, 常驻章节的指针行 |
| `STR-003` | "## Fast Fail Discipline" | FR-005, FR-006, SC-004, 契约测试的"各出现且仅出现一次"断言 |
| `STR-004` | "Fast Fail (Surface Load-Bearing Anomalies, Repair the Rest)" | FR-031, FR-032, SC-006, 双落点守卫的标题一致性断言 |
| `STR-005` | "如果这次修复的说明里必须出现「假定」,它就不是一次修复,而是一次快速失败。" | FR-011, SC-001, 契约测试的机械测试在文档中断言 |
| `STR-006` | "被守物真的坏掉时这条检查会不会变红?答不上来,这次绿就不是证据。" | FR-015, SC-002, 契约测试的机械测试在文档中断言 |
| `STR-007` | "tests/contract/test_fast_fail_discipline.py" | FR-035, SC-002, SC-003, SC-010, 任务清单的守卫任务 |
| `STR-008` | "快速失败" | FR-001, 词汇表 canonical 术语, 常驻章节摘要, 宪章原则正文 |
| `STR-009` | "fast-fail-clause" | FR-049, FR-052, FR-053, FR-061, FR-063, SC-012, 注入子句的固定标识(派发前自检按子串判定), Agent 定义制品与团队载荷所携副本 |
| `STR-010` | "ANOMALY:" | FR-048, FR-054, FR-055, FR-056, FR-063, SC-013, SC-014, 子代理回传异常行的固定前缀(编排者据此区分"异常停"与"普通失败");检测 MUST 以**行首**为判据,因为该前缀本身会被注入子句正文引用 |
| `STR-011` | "## Fast Fail List(快速失败清单)" | FR-016, FR-018, FR-020, FR-035 第 6/7 项, SC-003 的单源扫描节名, 真源文档 H2 标题 |
| `STR-012` | "## In-Passing Repair List(顺手修复清单)" | FR-017, FR-018, FR-020, FR-035 第 6 项, SC-003 的单源扫描节名, 真源文档 H2 标题 |
| `STR-013` | "未发现异常" | FR-054, FR-066, FR-067, SC-009, SC-013, 子代理回传与编排者收尾报告的显式陈述字面量 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-09-22(追加输入 — `/speckit.requirements` 收尾后到达的 scope addendum)

按 `.specify/shared/workflow/user-input-protocol.md` § Mid-Run Addendum Input 处理:该输入是本命令的**追加参数**,不是一次新调用;它改变需求范围,故落在上游工件(本文件)并**重跑验证门**。逐字记录如下。

- **追加输入(逐字)**:「在需求中补充: 重点关注subagent的行为,通常一个subagent启动之后它的行为就不受控的,因此在启动subagent的时候就要把fastfail的规则注入进去」
- Q: 子代理是这条纪律需要单独治理的一面,还是可经常驻层自动继承? → A: **需要单独治理,且不能靠继承。** 经源码核实:子代理的提示与配置「derived from its **Agent Instance** definition … plus its dispatch config … or dispatch payload, not from the orchestrator's conversation」(`shared/definitions/subagent-definitions.md:13`),团队上下文隔离规则另明写「NO conversation history passed to child agents」(`skills/create-team/references/patterns.md:105-109`)。常驻层结构性到不了子代理,且这是**有意设置的屏障**而非疏漏——用户"启动后不受控"的判断成立,理由比直觉更硬。
- Q: 注入应在哪一层实现? → A: **调用方的内容义务**,覆盖三条派发通道(编排者当场撰写的内联提示 / Agent 定义制品 / 团队 Per-Agent Payload)。MUST NOT 实现进外部派发包装器(它只覆盖 external 一种模式,无法覆盖 native 与 virtual;且其既有分工是"机制归包装器、内容归调用方",见 `subagent-definitions.md:73`);MUST NOT 新增"所有 agent 继承的共享前导文件"(Agent 定义制品按既有定义为**自包含**,其存储下无共享资产目录,见 `agent-definitions.md:40`)。→ FR-050、FR-051、FR-058。
- Q: 子代理"快速失败"的上送对象是谁? → A: **编排者,不是用户。** 子代理不拥有用户通道(其结果契约是 returned message / result manifest / declared output paths);它回抛**异常事实**,编排者组装面向用户的四要素上送件。上送件所有权因此分层。→ FR-056。
- Q: 既然启动后不受控,控制点在哪? → A: 只有两个——**派发之前**(自检注入子句确实在场,缺失本身即一次快速失败,形态对齐既有可写性预探针)与**回传之时**(必须含显式异常行,使"因干净而空"与"因没收到规则而空"可区分;异常停 MUST NOT 被当作普通失败原样重派)。→ FR-053、FR-054、FR-055。
- ### Session 2026-09-23(第三轮 — `/speckit.plan` Phase 0 对 FR-063 的落地裁定)

`/speckit.plan` 的 Phase 0 在把 FR-063(三个稳定字面量 MUST 互不为子串)落成具体字面量时,**证伪了 STR-001 的原值**:实测 `fast-fail` 是 `fast-fail-clause` 与 `shared/guidelines/fast-fail.md` 的子串,而反馈引擎按大小写不敏感**子串**匹配,故任何只是提到该纪律路径的反馈行都会被计为一次观察命中,FR-041"干净运行 MUST NOT 追加空洞条目"在机械上不可判别。按 FR-063 自己给出的 remedy(「各自带不可被另一方包含的定界」)修正:

- Q: STR-001 的观察标记取什么字面量? → A: **`[fast-fail]`**(加方括号定界)。实测该字面量在框架目录零命中,且与 `fast-fail-clause`、`ANOMALY:`、`shared/guidelines/fast-fail.md` 三者**互不为子串**(六对组合逐一验过)。保留 `fast-fail` 可读性(读者在反馈条目里能认出纪律名),同时使"提到纪律"不再等于"报告一次观察"。**未改引擎**(`--contains` 仍为子串匹配,Out of Scope 的零引擎改动约束保持不变)。
- Q: 是否改用与纪律名无关的裸记号(如 `ff-triage`)? → A: 否。房子两处先例(`token-efficiency`、`user-facing-comprehension`)用裸记号,但二者其实**有同一处潜在碰撞**——其纪律路径都包含其标记字面量。取带定界的 `[fast-fail]` 而非另造一个不可读的记号,既满足 FR-063,又保留可读性;与裸记号先例的**形态偏离已在 plan.md 的 Phase 0 决策中记录理由**。(附带观察:那两处先例的潜在碰撞属上游缺陷,不属本特性修复范围,已记入 `features/052.md` 的 Future Evolution Suggestions。)
- Q: STR-010 `ANOMALY:` 本身会出现在注入子句正文里(子句必须告诉子代理用这个前缀),如何满足 FR-063 的"MUST NOT 出现在承载它们的规则正文里"? → A: 该前缀无法不被子句引用,故改以**位置**作判据:异常行 MUST 以行首 `ANOMALY:` 起始,而子句对它的提及是行内反引号引用。STR-010 行已补此判据,FR-063 的互斥要求相应以"行首锚定 + 定界"两种手段共同满足。
- **本轮结构变更**:仅改 Shared Strings 两行(STR-001 值、STR-010 的判据说明)并把 STR-001/STR-010 补入 FR-063 的消费者列;FR 编号与其余正文未动。

**本轮结构变更(可审计)**:新增 User Story 4(P1,子代理派发注入),原 US4/US5 顺延为 US5/US6(含 US6 正文中对前序故事的引用同步改为 US1–US5);新增 FR 组 `#### 子代理派发注入`(FR-047–FR-062,共 16 条);新增 6 条边界情形、4 条 Key Entities、SC-011–SC-014 及其测量源、STR-009 与 STR-010;更新 Overview(新增第 5 项、层 A 表述)、现状锚点(新增"子代理派发面"一组 8 条锚点)、差异表(新增一行)、FR-028 第三条边界(改为指向新 FR 组)、Out of Scope(3 项)、Assumptions(3 项)。质量检查清单已按新内容重跑。
- **未改动**:FR-001–FR-046 的编号与正文(FR-028 第三条边界除外)、STR-001–STR-008、SC-001–SC-010、`Related Feature` 仍为 `Need clarification`(绑定归 `/speckit.clarify`)。

### Session 2026-09-22(第二轮 — `/speckit.clarify` Mode A)

**同作者检测已委托**:本规格由本会话同一 agent 写成,故按 `.specify/shared/workflow/objective-analysis-gate.md` 把覆盖扫描委托给 **4 个新鲜上下文只读子代理**(分工互不重叠:Feature 绑定与术语 / 功能范围与数据模型 / 交互·非功能·边界·取舍 / 现状锚点逐条重验)。每个简报都**点名了同作者条件**并要求"假定缺陷存在并定位它,不要报告制品是健全的"。四路共回传约 60 项发现,其中 **1 项经我复核为检测方自身错误**(见下"被证伪的检测发现"),其余按材料性分流:**4 项需用户裁定**(已提问并获裁定)、**约 30 项为纠正类**(恰有一种读法,已就地整合并在本报告披露)、其余为非材料项(记录不改)。

**用户裁定的四项(均为独立问题,一次批量提问):**

- Q: 这份规格绑定到哪个 Feature? → A: **新建 Feature 052「快速失败纪律(Fast Fail)」,Status = `Draft`**,不绑定既有 Feature。依据与候选逐个核验表已写入 `## Related Feature`。随之履行注册义务:分配 ID 052、在 `.specify/memory/features.md` 增索引行、建 `.specify/memory/features/052.md` 详情文件、并在其中记对相邻 Feature 的反向交叉引用。
- Q: 派发前发现"注入子句不在场",算顺手修复还是快速失败? → A: **按发现时点分流**——派发**前**发现属顺手修复(补齐后照常派发、收尾披露,FR-010 四条同时成立);派发**后**才发现属快速失败(子代理已不受治理地跑过,改提示无法撤销,而"已完成的那部分工作是受治理的"这一前提已被证伪)。→ 改写 US4 验收场景 1(拆为 1、2 两条,该故事验收场景 6→7 条)、FR-053 增时点分流。
- Q: "Agent 定义制品必须物理携带注入子句"绑定到哪个集合? → A: **绑定制作者要求,不绑定被枚举的文件清单**——落点为 `/speckit.agents` 命令模板的 Run Mode、`create-agent` 技能的创作契约、以及随包出厂的 Agent 预设;日后新建 Instance 因经这条创作路径而自动携带。理由:实测 `.specify/agents/instances/` 与 `execution/configs/` **今天均为空**且由用户日后创建,守卫无法枚举无界集合。→ 改写 FR-050 通道二、FR-061 的断言对象改为有界集合。
- Q: 清单只能往"快速失败"一侧生长吗? → A: **改为双向,并新增过度触发度量**——纠正朝哪个方向就往哪侧生长,两份清单证据资格对称;新增 SC-015 同时报告快速失败率、用户推翻率、清单净生长方向,使"这条纪律正在被绕过"成为有数字的信号。→ 改写 US5 标题与验收场景(5→6 条)、FR-044/FR-045、新增 SC-015 及其测量源、Key Entities 的"清单提升"更名为"清单移动"并补 `rejected` 态。

**纠正类整合(不需裁定,恰有一种与已记录意图一致的读法;逐项披露):**

| # | 缺陷 | 处置 |
|---|---|---|
| C-1 | FR-036 的新增文本枚举**过期**(冻结于追加输入前),漏掉 FR-062 的两个落点,而那两处在扫描范围内 | FR-036 枚举改为封闭并重列;补"计数单位是命中的行"这一实测事实 |
| C-2 | **本规格自己要求的措辞会打爆门控预算**:FR-012/FR-028 要求真源文档写出「确认门控治理」,而该词逐字命中阻塞模式 `确认门[禁控]`,新文档在 `shared/` 下、不在豁免集、FR-037 又禁止扩大豁免集 ⇒ 照原文写 total 会从 23 变 24,打爆 FR-038 的**相等**断言 | FR-036 增"相邻纪律的名字 MUST 以路径指称"一款;新增 FR-064/FR-065(不得为躲模式而改语义;规避改写触发 SC-001 复跑并留痕)、FR-078(把这份永久代价显式记为已接受) |
| C-3 | FR-051 许可的"引用拥有者文档"形态与 FR-048 的"MUST NOT 以路径可达替代三项内容"互斥,且使 FR-052 的逐字节断言无从书写 | FR-051 收窄为"内联有界字面量",路径引用降为**附加** |
| C-4 | FR-052 称副本为"机器可再生的合法重复"——**实测为假**:无任何引擎会再生 `patterns.md` 或 `.agent.md`(再生脚本只处理 `templates/commands/*.md`,Agent 渲染方向相反) | 改为"守卫钉死的合法重复"(唯一真源纪律三类合法重复的第二类),并要求拥有者字面量由**成对定界符**包围以便机械提取;修复路径为从拥有者手工重灌 |
| C-5 | FR-010(四条必要条件)与 FR-017(清单命中即可修)优先级未定,两位复核者会得出相反结论,而 SC-001 把分歧判为判据缺陷 | 新增 FR-070:判据优先于清单命中,清单命中不是充分条件 |
| C-6 | FR-024 用了两个**不属于拥有者封闭集**的类名("失败报告 / 门控提示"),且把选择推给"拥有者裁定";而归入 ①门控确认提示 会与 FR-028 直接矛盾 | 定为 **⑪ 失败如实报告**,写明排除 ① 的实质理由;并声明本真源文档 MUST NOT 成为类 ⑪ 的第二规则真源(四要素内容下限归本纪律,措辞与上下文规则仍归既有拥有者) |
| C-7 | FR-020 把守卫钉在"FR-016 点名的失效形态",但 `git diff` 三形态只出现在 FR-021 的路径引用里 ⇒ 守卫无法断言 SC-002 度量的那 7 项 | FR-016 展开盲检四成因并把 `git diff` 三形态列入点名集合,合计 **7 项**与 SC-002 分母一致;守卫按 7 项断言、不按清单总条数断言 |
| C-8 | FR-035 的守卫枚举只有 10 项,漏掉 FR-003/007/029/040/041/044 等约 8 条本规格自己要求的义务 ⇒ **文档没写也照样绿**,正是本特性要治理的盲检 | FR-035 枚举扩为 **22 项封闭清单**并声明"凡要求载明而未列入者即构成一处盲检";新增 FR-076 固定清单条目语法,使"每条携判据"不退化为"该节非空" |
| C-9 | 三个稳定字面量**互不互斥**:`fast-fail` ⊂ `fast-fail-clause` ⊂ 路径,而引擎按子串匹配 ⇒ 任何提到该纪律的反馈行都被计为观察命中,FR-041 不可判别;另一侧子句本身携 `ANOMALY:` ⇒ 引用子句原文的回传会被误判为异常停 | 新增 FR-063:三字面量 MUST 互不为子串且 MUST NOT 出现在承载它们的规则正文里 |
| C-10 | 两条控制点只在子代理侧设了反空真哨兵,**最外层没有**:干净运行与完全未受治理的运行对用户不可区分——本特性要消除的混淆在最外层复现 | 新增 FR-067(干净运行也 MUST 显式说一句),SC-009 增该在场率、其测量源要求干净与含修复两种运行各取一次 |
| C-11 | 上送件第四要素"可选处置"**从未被枚举**,而 SC-008 的通过条件是"四要素齐备"⇒ 一份把读者逼进死胡同的报告同样通过(循环判定) | 新增 FR-068(封闭处置集,至少四项);SC-008 通过条件改为"能选出一项并说明理由",显式禁止以标题齐备为通过 |
| C-12 | FR-040 的观察记录假定运行能活到反馈收尾,但快速失败会终止动作链(FR-027)⇒ 价值最高的观察被系统性丢失,生长闭环断粮 | 新增 FR-069:观察 MUST 由**上送件自身**承载(落盘即留痕) |
| C-13 | 回传缺异常行时只有禁止、没有处置(既非异常停也非干净的**第三态**悬空) | 新增 FR-066:缺行即一次异常,判为**不完整**、结论 MUST NOT 被当证据消费;SC-013 拆为编排者侧(可断言 100%)与子代理侧(度量不设阈值) |
| C-14 | FR-055 只把异常停从**两条**既有规则里排除,未排除"非并行任务失败即停",而 FR-026 恰恰委托了它 ⇒ 异常停在被委托规则下算什么没有答案 | 新增 FR-071:异常停不计入既有的**任何**失败规则,它是一次上送而非一次失败 |
| C-15 | 两条边界情形写着 MUST 却无 FR 载体(只读命令的上送形态、既有实例点位与新判据冲突) | 新增 FR-072 承载二者 |
| C-16 | `爆炸半径` 是 FR-010(d) 的必要条件之一、又是 FR-013 的裁决理由,却只作为裸属性出现 ⇒ SC-001 的 100% 一致率不可达 | 新增 FR-073 要求给出可判定定义并指定拥有者 |
| C-17 | 面向用户可理解性纪律要求每个规则真源文件携**恰好一行** canonical 指针声明所覆盖的界面类,FR-002/007/035 均未要求 | 新增 FR-074,并纳入 FR-035 第 15 项 |
| C-18 | 四条处置规则缺失:并发异常、裁定 ping-pong 无上限、跨会话既有裁定无检索步骤(与"同一个问题不需要问第二遍"冲突)、真源文档自身出现异常 | 新增 FR-075 四款;FR-028 相应从四条边界扩为**五条**(补入"问一次、记下来、说三遍") |
| C-19 | Key Entities 缺 **异常类**(整套判据围绕"命中"这个动词转,而它只在类这一层有意义)、Agent 定义制品、编排者/子代理、执行模式、派发链跳、用户直接纠正、真源文档;`裁决记录` 无任何 FR 消费(死重);三个实体缺生命周期;`派发通道` 误称"三条互斥" | 补齐 7 个实体;`裁决记录` 接到 FR-042/FR-075(b)/(c);`分流结论`/`观察条目`/`清单移动` 各补生命周期与终态;`派发通道` 改为不互斥;`异常` 补同一性键 `(发现点, 被证伪的预期)` |
| C-20 | **一处既有房式措辞经实测为假**:"刷新项目指令即连同其镜像副本一并恢复"——`generate-instructions.sh` 全文无镜像同步调用,`shared/` → `.specify/shared/` 的复制只在 CLI 的 `copy_local_templates()`(由 `specify init` 调用)里发生 ⇒ 旧下游项目只刷指令会得到**悬空指针** | 改写该边界情形为真实路径;新增 FR-077 禁止常驻章节沿用该句式,并明令 MUST NOT 顺手改写其他章节的同类问题(那是一次未获授权的爆炸半径越界,属上游缺陷、单独上报) |
| C-21 | 引文与计数漂移:三处引文带**原文没有的粗体**;`sync-mirrors.py` 的 rglob 实在 `:86`(`:83` 是函数定义行);子代理结果契约三通道的枚举只在 `:9`;`fail-fast` 占用实测为**权威源上 9 处**且 3 处不指可写性探针(初记 5 处);差异表把分母写作"六条既有纪律"(实测 `shared/guidelines/` 12 份中 0 份提及子代理) | 逐项订正;`fail-fast` 订正**不改变**命名裁定(`fast-fail` 系列仍零命中),但把"若用户改选 `fail-fast`"的消歧成本如实上调并写明跨三种语义 |
| C-22 | Overview 的"见 FR-031"指向错误(四个钉子同批上调是 FR-032);FR-001 仍写"提升规则与四条边界";两份清单没有 STR 行,而 SC-003 要断言"清单节名命中数为 0"却无字面量可断 | 订正指针;FR-001 改"双向生长规则与五处边界";新增 STR-011/STR-012(两份清单的 H2 标题字面量)与 STR-013(`未发现异常`) |

**被证伪的检测发现(如实记录,不采纳):** 一路检测主张 FR-024 应把上送件归入"门控提示"类并由拥有者裁定。经我复核该类 ① 的规则真源与其附加要求(门控类界面另须载明不可撤销后果与可逆性),归入 ① 会与 FR-028"不新增门控、不向治理保留清单增行"及 SC-005 的零命中主张直接矛盾;故取 ⑪ 并把排除 ① 的理由写进 FR-024,而不是把选择推给下游。

**编号说明(有意偏离房式连续性,已披露):** 本轮新增的 FR 一律追加为 **FR-063–FR-078** 并归入末尾的 `#### clarify 2026-09-22 第二轮补入` 组,而**不**重排 FR-001–FR-062。理由是重排会迫使约 30 处 `FR-nnn` 交叉引用同步改写,而"机械改写一批编号再逐处核对"本身就是本纪律点名要治理的高危操作;追加式编号保持全部既有引用有效,代价是文档内 ID 与位置不完全同序。中途三次误用的字母后缀 ID(FR-016a、FR-024a、FR-062a)已全部折回其主 FR,当前无字母后缀 ID。

**本轮结构变更(可审计)**:FR 46→**78**(新增 FR-063–FR-078 共 16 条,并改写 FR-016/024/028/035/036/044/045/048/050/051/052/053/061/062);SC 14→**15**(新增 SC-015,改写 SC-008/009/013 及其测量源);STR 10→**13**;Key Entities 13→**19 条**(其中 2 条各覆盖一对实体,故实体数多于条目数);边界情形 17→**17**(其中 2 条改写);US4 验收场景 6→**7**、US5 5→**6**;`Related Feature` 由 `Need clarification` 解析为 **Feature 052 / Draft**;Overview 与现状锚点新增/订正若干实测条目。

### Session 2026-09-23(实现期 — `/speckit.implement` Phase 3 中途上送,用户裁定)

**触发方式**:T013 的 SC-001 双评审者取样。两个互不共享上下文的只读子代理对同一场景(S9:已顺手修过的异常在本次运行**另一点**再次出现)**各自独立**上报同一条 `ANOMALY:`——`两振升级` 把"同一"认定为 `(发现点, 被证伪的预期)` 二元组,而复发出现在不同发现点时二元组不相等、计数不增,规则不可达;二者都只能退回 `存疑从严` 才得出结论。判定级一致率 12/12,规则级仅 11/12。按本纪律自己的判据,这是**裁定**而非**纠正**(至少三种读法都与已记录意图相容,无一种被工件选定),故停在异常点上送,取证见 `notes/sc001-dual-review.md`。

- Q: FR-014 两振升级的同一性键如何处置? → A: **按建议处置——拆成两个键**。FR-014 的"同一异常"改用**复发键 `被证伪的预期` 单键**(复发看的是同一个被推翻的预期,与在哪里再次撞到它无关);FR-044 的"两次独立观察"保留**独立键 `(发现点, 被证伪的预期)` 二元组**(独立性恰恰要求发现点不同)。用户选定时附带的预期结果原文:「FR-014 复发键 = (被证伪的预期) / FR-044 独立键 = (发现点, 被证伪的预期) / → 两振升级在跨发现点复发时也能触发」。

**被拒绝的读法(记录理由,防止下一次重新发明)**:① 放粗 `发现点` 的定义到"单元/阶段"层——改动面更小,但"单元"本身需要新定义,且跨单元的复发仍不可达;② 照原样继续并把"跨发现点复发不升级"记为已接受代价——零上游改动,但两振保护在大多数真实形态下仍不生效,等于保留一条写了却永不触发的规则。

**该裁定绑定的代价(按"张力必须被写入而非丢弃"的规则)**:两个键并存意味着"同一异常"在本规格内**有两个含义**,取决于它服务于复发判定还是独立性判定。因此:任何消费该键的制品 MUST 写明它用的是哪一个键;守卫 MUST 分别断言两个键在场且**互不替代**(`test_c10` 断言复发键不含发现点、`test_c18`/生长闭环侧断言独立键含发现点)。若日后再把两者合并回单键,FR-014 的不可达性会**静默**回归,而现有守卫的字符串在场断言不会变红——这是本次裁定留下的、唯一没有机械守卫的回归路径,已记入 `features/052.md` 的 Future Evolution Suggestions。

**本轮结构变更(可审计)**:改写 FR-014、FR-044、Key Entities › 异常(Anomaly)的同一性键;FR 计数不变(**78**),无重编号;级联改动落在 `data-model.md` E2、`contracts/discipline-doc.md` C-10(g)、真源文档 `### 三条裁决顺序`、`test_c10` 断言体,并以**新任务号 T063** 追加到 `tasks.md`(不重排既有 ID)。

## Out of Scope

- **不新增机制**(对齐房子范围限制子句):MUST NOT 引入异常检测引擎、分流评分器、清单成熟度报告生成器、独立跟踪台账或注册表;MUST NOT 引入运行时异常捕获代码或框架。本纪律是一种**写法与处置约定**,由既有引擎承载观察、由契约测试守卫。
- **不重定义相邻纪律的判据**:确认门控治理的"是否门控"两级判据、其破坏性动作清单与治理保留清单;输入健全性检查的检查项清单;同作者检测委托的触发条件与严重度上限;自我提升治理的证据资格判据——四者均 MUST 保持其原拥有者不变,本特性只引用。
- **不修改任何既有引擎源码与派发机制**:`scan-confirmation-gates.py`(含 `POLICY_DOCS` / `SELF_REL` / `BLOCKING_PATTERNS`)、`sync-mirrors.py`、`regen-command-copies.py`、`generate-instructions.sh`、`feedback-utils.py`、`skills/create-team/scripts/dispatch.sh` 与其流过滤脚本全部零改动。注入是**调用方的内容义务**,不是包装器行为(FR-058)。
- **不新增共享 agent 资产或派发前导文件**:MUST NOT 建立"所有 agent 继承"的共享资产目录、前导文件或模板头——Agent 定义制品按既有定义为自包含且其存储下无共享资产目录;注入 MUST 走"内联有界字面量"或"引用拥有者文档"两种既有许可形态(FR-051)。
- **不逐个改写内联派发点位**:现状锚点点名的十余处内联派发提示(命令模板与技能正文)由编排者**当场撰写**,义务经常驻章节抵达(FR-050 通道一);本特性 MUST NOT 逐处插入子句正文,只在真源文档中规定其落点与形态。
- **不做全仓措辞清扫**:收敛范围限于 FR-029 点名的既有实例点位;对仓库中其余提及"失败/停止"的散文(含 `docs/`、`agents/`、其余技能正文)本特性不改写,留待各自修订时自然收敛为指针。
- **不新增 probe 类或 probe 对象**:观察复用触发单元既有 probe 加标记。
- **不新增面向用户界面类**:上送件归入面向用户可理解性纪律已枚举的封闭集。
- **不改按工具副本**:`.claude/commands/`、`.github/prompts/`、`.qoder/commands/`、`.opencode/command/` 由既有再生脚本自动产出。
- **不改 `templates/plan-template.md`**:其 Constitution Check 已动态枚举。
- **不追溯重构既有已实现特性**:050 / 051 等已落地的纪律不因本特性回改。

## Assumptions

- **命名取 `fast-fail` 词序**(与用户输入一致)。实测依据:`fast-fail` / `fast_fail` / `FAST_FAIL` / `fast-fail-list` / `派发注入` / `注入子句` / `fast-fail-clause` / `ANOMALY:` 全仓零命中(排除本轮自身产物:本特性目录、词汇表、反馈存据),故 STR-001/009/010 均可用。反序 `fail-fast` 已被散文占用**且占用面比需求阶段初记的大**:初记 5 处、订正为权威源上 **9 处**,其中 3 处不指可写性探针(详见 Overview 的命名占用锚点)。若用户偏好 `fail-fast`,消解歧义的负担跨**三种**互不相干的语义(可写性探测 / 平台与配置校验 / 配置写入原子性),约为初记的两倍;此为**用户可覆盖**的命名裁定,但覆盖的成本已如实标出。
- **上送形态是阻塞的**:快速失败 MUST 停在异常点等用户裁定,这正是用户输入"快速失败而不是强行进行修复继续执行"的直接含义。它之所以不违反确认门控治理的回流约束,是因为该约束治理的是**动作授权**类门控("这个可逆动作可不可以不等批准就做"),而快速失败是**错误升级**——与既有的"非并行任务失败即停""两振停滞即升级""缺件即中止"同型,而那些既有的停止点位今天均**未**被登记为治理保留清单中的门控。故本特性 MUST NOT 向治理保留清单新增行(FR-028)。此为本规格作出的**裁定**,若 `/speckit.clarify` 判定应登记为门控,则 FR-028、FR-037、SC-005 需相应调整。
- **停止粒度**取"停在异常动作及其依赖者,无关的独立并行工作按既有规则处理",依据是 `implement.md:73` 的既有形态。未取"整条运行一律中止",因为那会使并行工作的已完成部分白费。
- **分流判据是可判定的写法约定**,不是"尽量少停"这类不可判度的中间档——依据是房子在可理解性纪律上已作过同一取舍(`user-facing-comprehension.md:19` 明写"不存在「尽量少用」这类不可判定的中间档")。`ask-record-repeat.md:15` 自陈其规则为理念而非机械可判,本纪律**不沿用**那一形态,因为用户点名要求"关键是需要区分",区分必须可判定才可守。
- **清单首版条目取自本仓已实测的失效**,不取假想案例;这是 SC-002 可测的前提,也符合"证据优先"的房子取向。
- **提升阈值取"两次独立观察 或 一次用户直接纠正"**:后半直接引用 `self-improvement.md:42` 的既有资格判据;前半取最小可防偶发的整数。阈值本身住在真源文档(唯一定义点),本规格不复述为契约字面量。
- **落地范围取"真源 + 常驻 + 守卫 + 双落点 + 点名点位收敛"**,不取全仓清扫。理由:全仓清扫的收益随时间自然兑现(各点位修订时收敛为指针),而一次性清扫会把本特性的变更面放大到难以复核。
- **数字锚点的拥有者**:宪章原则数与命令 `MUST include` 条目数由既有双落点测试拥有(本特性 MUST 同批上调其钉子);门控 total 由冻结基线文件拥有;fast fail 清单条目数**无拥有者且不设钉子**(FR-020)。本规格 Overview 中出现的一切计数均为 2026-09-22 的日期化实测记录,MUST NOT 被下游工件当作当前现实引用。
- **注入取"调用方内容义务",不取"包装器注入"**:理由是外部派发包装器只覆盖 external 一种模式,而注入义务 MUST 对 native / virtual / external 三者同等成立(FR-057)——只有调用方侧的形态能同时覆盖三种。该裁定与既有分工一致(`subagent-definitions.md:73` 明写标签约定"是调用方的责任")。若 `/speckit.clarify` 认为应在包装器侧再加一道机械兜底(程序优先取向),那是一次**范围扩张**(需改既有脚本),MUST 显式裁定,MUST NOT 默认发生。
- **注入子句取"短而有界、自足于分类决定"**,不取"整份纪律的副本":一个必须先打开文件才知道该不该停的子代理,已经失去了这条保证(FR-048)。该取舍同时把 One Source of Truth 的张力限定在一段**可逐字节比对**的短字面量上——通道二/三所携副本因此是"机器可再生的合法重复",而不是各自漂移的第二定义点(FR-052)。
- **子代理的快速失败上送对象是编排者,不是用户**:依据是既有事实而非取舍——子代理的结果契约只有三种回传通道(returned message / result manifest / declared output paths,枚举于 `subagent-definitions.md:9`;`:15` 只载明"结果契约"这一属性本身),不含用户通道。若某宿主工具确实给了子代理一条用户通道,该能力 MUST NOT 被本纪律依赖,否则纪律就绑定在了不可移植的宿主特性上。
- **本特性自身受本纪律约束**:实现过程中若撞见与本规格预期不符的状态(如某个钉子数值与规格所载不符、某个点位已存在同名文件),实现方 MUST 按快速失败上送并把证伪结果回写本规格,而不是就地绕过——这是本纪律的第一次自证。**本轮已有一次真实样本**:需求阶段派发的研究子代理回传了一份可信但含错的锚点汇总(把 `one-source-of-truth.md` 的一句引文标为 `:49`,实为 `:51`),编排者逐条复核后订正。子代理回传的"看起来对"与"核对过"之间的差,正是 FR-054 要求显式异常行、FR-055 禁止把异常停当普通失败重派所要治理的同一类风险——只不过本轮它以良性的形式出现。
