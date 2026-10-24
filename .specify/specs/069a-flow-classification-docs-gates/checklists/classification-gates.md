# 分类本体与文档型门禁 Checklist: 执行/表达二元分类与文档型门禁（Feature 069 / Slice 069a）

**Purpose**: 对 069a 的**需求（What）**做质量审查——判据是否可复现、门禁不变量是否封死、六面文档型门禁与最小接线（W1–W4）是否被完整且无冲突地要求、27 FR / 8 SC / 50 条款能否被 36 个任务覆盖并被证伪。本清单不评判实现好坏，只评判要求写得是否可判定、可测量、可追溯。
**Created**: 2026-10-24
**Feature (Requirement Scope)**: Feature 069（`.specify/memory/features.md` 第 77 行 / `.specify/memory/features/069.md`）；本清单只覆盖切片 `069a-flow-classification-docs-gates`
**Requirements (What)**: [requirements.md](../requirements.md)（27 FR / 8 SC / 4 Shared Strings）
**Specifications (How, context only)**: [plan.md](../plan.md)、[tasks.md](../tasks.md)、[data-model.md](../data-model.md)、[contracts/](../contracts/)（50 条款）、[quickstart.md](../quickstart.md)、[research.md](../research.md)、[notes/parent-fr-mapping.md](../notes/parent-fr-mapping.md)

**Note**: 本清单由 `/speckit.checklist` 生成，用于校验 **需求（What）** 的质量。**规格（How）** 只在两种情况下被引用：暴露需求缺口/歧义/冲突，或核对关键设计决策能否回溯到需求——不用于测试实现行为。

**勾选语义（本次评审的 disposition）**：`[x]` = 要求本身成立，且（如原为问题）已在规格中处置并留可复算证据，行尾以 `→ 已处置: <依据>` 标注；`[ ]` = 仍待处置但**必须带 disposition**：`→ disposition: out-of-slice（069b）: <理由>`（归属后续切片/非本切片范围）或 `→ disposition: verify-in-implementation: <核对点>`（只能实现期验证）。本清单**不允许**无 disposition 的 `[ ]`。

## A. 分类本体与判据可复现性

- [x] CHK001 两个取值是否被封闭声明为仅 `[[STR-001]]` / `[[STR-002]]`、判据是否只回答一个问题（主交付物的验收由机器行为还是人的理解判定）且以 oracle 而非介质表述、类中立是否被明确排除在第三取值之外？[Completeness, Req §FR-001–§FR-002 / §FR-008; research R2; data-model E2/E3]
- [x] CHK002 「主交付物」本身是否被定义到可判定的程度——多交付物时择一的规则是否唯一，§Edge Cases 追加的「失败不可逆性」与 §FR-002 的单一 oracle 问句是什么关系？[Ambiguity, Req §FR-002 / §Edge Cases 第 1 条; 现象: 两个判别量并存] → 已处置: requirements **SA-9** 定义「主交付物 = 验收时会被实际运行/观测其行为的产物」，两个产物都必须验收时按父编号 038（混合 oracle → `execution`）交 069b；FR-002 明文「失败不可逆性 MUST NOT 构成第二个判别问题」，§Edge Cases 首条同步改为「仅 tie-break」。判别量回到唯一 oracle 问句。
- [x] CHK003 判据的非介质性是否有规范性示例，且理由指向 oracle 而非扩展名（Markdown 架构文档→表达；须生成并编译 SDK 的 OpenAPI→执行；站点构建通过不改判定）？[Completeness, Req §FR-003]
- [x] CHK004 §FR-006 / §SC-001 的「两名独立判定者一致率 100%」是否规定了独立性判据（不同人、不同会话、判定时互不可见）与不一致时的处置顺序（改判据而非逐案裁定）？[Measurability, Req §FR-006 / §SC-001; Measurement Sources 只写「分别落盘后比对」] → 已处置: FR-006 增补「独立 = 不同的人 / 不同的会话 / 判定时互不可见（结论分别落盘后比对）」，处置顺序固定为「先修判据、再重判」，且**修正后对全部样本重判一次**；§Measurement Sources 的 SC-001 Source 同步重写（机器核验优先、两人演练并列）。

## B. 唯一所有者、台账与命名空间

- [x] CHK005 所有者是否被声明为唯一，且明列它拥有什么（判据、两取值、边界例、逐流程台账、类中立封闭清单、命名空间、变更记录）？[Completeness, Req §FR-005; contracts `flow-class-ledger.md` C-1]
- [x] CHK006 机器键 `flow_class` 的字面量归属是否自洽——§Assumptions SA-3 声明「本切片不声明 STR-003、也不得复述其字面量」，而 069a 的 contracts / data-model / plan / tasks 合计出现 27 处该字面量，且台账列头必须用它？[Conflict, Req §Assumptions SA-3 / §Shared Strings; data-model E2/E9; contracts C-3] → 已处置: 裁定**由切片声明** `STR-003`（`"flow_class"`，复用父 STR-003 的字面量与语义并标注父来源父编号 036）；SA-3 改写为「本切片声明 STR-001/002/003/004，消费方一律写 `[[STR-003]]`」；§Shared Strings 增行（4 行）与 Citation convention 同步；contracts C-3/C-4/C-7/C-9/C-13、data-model E2/E9、plan 与 tasks 的正文提及均改为引用 `[[STR-003]]`（测试正则/字段名处的字面量属「防漂移的固定副本」，已就地注明）。
- [x] CHK007 `execution` / `expression` 与既有 `Agent Execution`（Agent 三层分类法第三层）的消歧是否有 requirement 级依据（现仅在契约 C-3、research R5 与 `glossary.md` 第 54/173/177 行），而本切片已经开始生产台账列？[Traceability, Req §FR-001–§FR-002; glossary 同名不同义] → 已处置: FR-001 增补 requirement 级条款——「`execution` 与 Agent 三层分类法中的 `Agent Execution` 同词异义，消歧 MUST 在所有者 § 命名空间 与 `.specify/memory/glossary.md` 两处显式声明」；plan/contracts 的落点保持不变。
- [x] CHK008 台账的 `basis` 列（`behavior-oracle` / `reader-oracle` / `mixed-oracle`）能否回溯到某条 FR/SC——它承担 FR-002 与 FR-006 的判定依据，但 requirements 从未定义该字段？[Traceability, data-model E2; contracts C-4] → 已处置: FR-002 增补「台账每行 MUST 记录判定依据 `basis`，取值 `behavior-oracle` / `reader-oracle` / `mixed-oracle`；`mixed-oracle` 的归属裁决不在本切片（父编号 038 → 069b）」；data-model E2 的 `basis` 行与 contracts C-4 同步声明其为 FR-002 的判定依据列。
- [x] CHK009 台账完备性是否写成「与清单双向覆盖 + 反空真下限」，且互斥类缺陷（`duplicate` / `dual-class` / `invalid-class`）是否被要求各自独立报告而非合并为「有错」？[Completeness, Req §FR-007–§FR-008; contracts C-5/C-6；实测量级 27 命令 / 51 技能 / 78 单元已复测一致]
- [x] CHK010 「两份分类定义并存」与「客户项目 MAY 为自己新增流程声明类别」两条边界是否有归宿——前者只在 §Edge Cases 要求「副本由生成/刷新产生并带漂移检查」，后者被契约 C-14 明确为「本切片不提供声明面」，却与「零项目侧存储」并存？[Coverage, Req §Edge Cases 第 8 条 / §FR-011; compatibility C-2; flow-class-ledger C-14] → 已处置: FR-011 增补「客户侧**声明机制**不在本切片（迁移与兼容归 069b）；本切片只固定『两份定义并存时以所有者为准，副本由生成/刷新产生并带漂移检查』与『框架流程类别不可被项目覆盖』」；§Edge Cases 同条补「分发机制（父编号 033–035）归 069b」。「零项目侧存储」只约束本切片的读取/缓存，不承诺客户声明面。

## C. 默认类与降级

- [x] CHK011 未声明默认（`execution`）、消费点固定标记（`[[STR-004]]`）与「不得把默认呈现为已判定」是否三者齐备，并落到可机械断言的返回字段？[Completeness, Req §FR-009; contracts C-7; data-model E9 invariant]
- [x] CHK012 「消费点」与 SC-002 的「被检查样本」是否被定义为可枚举对象——标注率 100% 的分母是全部 78 个单元、全部门禁读取点，还是接线后的 4 个入口？[Measurability, Req §FR-009 / §SC-002] → 已处置: FR-009 定义「消费点 = 门禁读取点，本切片的消费点 = 接线封闭集入口（W1–W4）」，其余单元的标注义务随接线扩面（069b）；SC-002 改为「被检查样本 = W1–W4 触发的运行时消费点；分母不是 78 个单元的静态总数」。
- [x] CHK013 「版本不兼容」是否有可判据的载体——台账行与解析结果都没有 version / schema 字段，契约 C-7 以「台账表头缺失」代称版本不兼容？[Clarity, Req §FR-016; contracts C-7; data-model E2/E9] → 已处置: FR-016 明确「『版本不兼容』以**所有者台账的表头/列集合与解析器期望不符**为判据（不引入 version 字段；版本化属 069b 的落地口径）」；data-model E9 增补降级标签互斥说明，contracts C-7 的「台账表头缺失」成为该判据的一份具例。
- [x] CHK014 降级标签有两个（`[[STR-004]]` 标记 与 `owner-unavailable`），requirements 未写明二者是「二选一」还是「同时出现」，也未写「降级不得被当作通过」是否适用于全部降级路径？[Consistency, Req §FR-016; contracts C-7/C-15] → 已处置: FR-016 增补「两个降级标签**互斥**：owner 可解析但单元未登记 → `source: default` + 标记；owner 或引擎不可解析/缺席 → `owner-unavailable`（并保留默认类语义）」与「『降级不得被当作通过』适用于**全部**降级路径」；data-model E9 增 `Degradation labels（互斥）` 段，contracts C-15 第 2 条与之一致。

## D. 门禁不变量（分类只换算子）

- [x] CHK015 阶段集合是否被固定为 8 阶段且不因分类改变、clarify 的既有跳过规则是否被排除在「分类影响」之外、analyze 与 review 的 100% 调用率与「阶段完整性判定 MUST NOT 读取类别」是否写明且拒绝规则不带例外？[Completeness, Req §FR-012 / §FR-014; contracts C-10/C-11]
- [x] CHK016 「只选择算子集、不减少门禁数量、不降 P0/P1、不改阈值」与「与复杂度轴正交」是否有可测分母——本切片的三条基线是调用/确认/墙钟，不含逐阶段门禁数，也没有表达类与执行类的门禁数对照？[Measurability, Req §FR-004 / §FR-013; SC-004–SC-006] → disposition: out-of-slice（069b）: 门禁数与阈值的对照仪器是父 §G 区父编号 041 的「三项基线的仪器与 not-evaluated 降级」，本切片不新增逐阶段门禁计数面（新增即扩范围）。069a 的残余可验证面已落在不变量文本与运行面：FR-013/FR-014 的「不减数量/不降 P0-P1/不读类别」+ T031（明文在场与零读取审计）+ T035（三项基线对照，无来源记 not-evaluated）；逐阶段门禁数的表达类↔执行类对照随 069b 的仪器落地。
- [x] CHK017 §FR-015「门禁 MUST 在判定之前从唯一所有者读取类别」是全称要求，而本切片只接线 78 个单元中的 4 个入口；该要求的适用面（仅首批成员 / 仅接线面）是否应写进 requirements，而不是只写在契约 C-9/C-15 与 plan？[Ambiguity, Req §FR-015 / §FR-025] → 已处置: FR-015 增补「适用面是**门禁执行面**：本切片的执行面 = 接线封闭集四个入口（W1–W4），其余单元的读取义务随接线扩面（069b）」；FR-025 同步固定 humanize 的 Simple 形态与 W2/W4 分工，C-9/C-15 只作机械化，不再是唯一出处。

## E. 六面文档型门禁

- [x] CHK018 六面是否各有且仅有一个可解析 `owner_pointer`，且本切片只新增「证据分级与 as-of」「事实一致性」两面（其余四面指向既有 owner）？[Completeness, Req §FR-018; contracts `expression-gate-operators.md` C-1；全部 owner 路径已实测存在]
- [x] CHK019 六面集合是开放还是封闭——§FR-018 写「至少覆盖六面」，data-model E4 的不变量写「覆盖面 = 6」，而契约 C-14 又要求「沿用 C-1 的六个 face id」，但 C-1 只列中文面名、未定义任何 face id？[Conflict, Req §FR-018; data-model E4; contracts C-1/C-14] → 已处置: 裁定**封闭六面（恰好 6）**。FR-018 改为「本切片恰好六面……新增面 MUST 由后续特性修订门禁 owner 与本条」；新增 SA-7；contracts C-1 增 face id 列（`requirements-clarity` / `reader-purpose` / `evidence-asof` / `structure-links-build` / `fact-consistency` / `review`）并写「面数 MUST = 6（多于 6 = 扩面，少于 6 = 缺面）」；data-model E4 不变量改「恰好 = 6」；C-14 的「沿用 C-1 六个 face id」由此有定义可引；plan A/T013 按 exactly 6 断言。
- [x] CHK020 「文档型交付物」的范围是否被定义（规格产物？技能 `SKILL.md`？命令模板？站点文档？），否则 §FR-019 的阻断面无法枚举，检查器的 S1/S2 集合就成了事实上的定义？[Clarity, Req §FR-019; contracts `doc-consistency-checker.md` C-2/C-4] → 已处置: FR-019 增补定义——「表达类流程产出的、以人阅读验收的 Markdown 产物：规格产物（requirements/plan/tasks/data-model/research/quickstart/feature-ref/contracts/checklists）、技能 `SKILL.md`、命令模板、站点文档；检查器 S1/S2 是可枚举子集，**不构成定义**」。检查器集合成为实现的取样面而非规范面。
- [x] CHK021 §FR-020 要求证据「可复算（含命令、退出状态或可定位来源）」，而 data-model E6 把 `source` 定为可选、契约 C-5 只强制 grade/as-of 配对——强制面是否应包含来源？[Conflict, Req §FR-020; data-model E6; contracts C-5] → 已处置: 裁定 `source` **必填**。FR-020 改为「等级 / as-of / 来源三件套成组；`实测`/`推断` 的 source = 可复算命令或退出状态，`引用` 的 source = 引文出处」；data-model E6 的 `source` 由「可选」改「必选」并写 `source-missing`；contracts C-5 与 doc-consistency-checker C-3 增 `source-missing`（blocking）规则；tasks T020 与 T013/T014 的断言面同步。
- [x] CHK022 「无标注的事实断言不得进入交付」的可判定边界在哪——research R7 已拒绝「每句都标」并把机械面收敛为配对规则，这个强弱差是有意让步还是待补的判定定义？[Clarity, Req §FR-020; research R7; contracts C-5] → 已处置: FR-020 明文承认这是**有意的判定边界**——「逐句强制标注被明确排除（R7）：未被标注的断言**不构成可援引的事实主张**」；配对/三件套规则是可机械判定的那一半，语义「是否事实性断言」交评审面。强弱差由需求承认，不再是隐含让步。
- [x] CHK023 新增「证据等级/as-of」面与既有证据机制的对象差异是否在 requirement 层写明（`evidence-step.md` 描述机制七态、`single-run-evidence.md` 描述一次执行的留存），以免被读成重定义或收窄？[Consistency, Req §FR-020; data-model E6; research R6] → 已处置: FR-020 增补对象边界——「本条的**对象**是文档断言；`shared/workflow/evidence-step.md` 的机制七态与 `shared/guidelines/single-run-evidence.md` 的运行记录留存 MUST NOT 被本条重定义、收窄或并入」；data-model E6 与 contracts C-5 的同名条款保持指向该 requirement。
- [x] CHK024 「结构/链接/构建只是必要条件」「判据为零新增违规（基线 3 条既有违规）」「站点层缺席记 `not-applicable`」是否三者齐备且互相不矛盾？[Completeness, Req §FR-021; contracts C-6；基线 `violations=3`（broken-link 2 + note-frontmatter 1）已复测]
- [x] CHK025 §FR-022 的绝对判据（同一事实 ≥2 处手写即缺陷）与其机械实现（完全相等且 ≥24 字符，或 ratio ≥0.90 且 ≥40 字符）之间的落差是否被承认——低于阈值的真副本按设计不会被报出？[Measurability, Req §FR-022; contracts `doc-consistency-checker.md` C-5] → 已处置: FR-022 明文「机械检测有**下限**……低于下限的真副本按设计不被机械报出——这是已声明的检测下限，不是判据放宽；人评审面仍按本条全量判定」；contracts `doc-consistency-checker.md` C-5 第 5 条同步（低于下限者交评审面）。
- [x] CHK026 评审门禁的判定者身份与三项基线的「开工前」时点是否被定义——§FR-023 的「人工评审」是否允许代理执行、如何与代码评审的判定对象机械区分；§FR-024 的冻结时点以哪个工件的哪次记录为准（SC-006 用 requirements 首次提交，另两项未定）？[Ambiguity, Req §FR-023–§FR-024; contracts C-8/C-9; data-model E8] → 已处置: FR-023 增补「判定者 MUST 是人工评审者或受其委托的评审代理；判定对象 MUST 是读者理解与事实相符（编译/测试/覆盖率 MUST NOT 作为该判定对象）」；FR-024 增补「『开工前』= 该特性 `requirements.md` 首次提交的时点（三项共用同一起点，记录 `frozen_commit`）」，data-model E8 的 `frozen_at`/`frozen_commit` 与 contracts C-9 同口径。

## F. 表达类首批成员与既有特性

- [x] CHK027 §FR-025 是否同时固定了三件事：`/speckit.docs` 与 `/speckit.humanize` 登记为表达类、既有门禁「只补强不削弱」、补强形态封闭为最小接线（4 入口，每处只加 lookup 与 owner 指针）？[Completeness, Req §FR-025; contracts C-11/C-12/C-15]
- [x] CHK028 §FR-026–§FR-027 是否给出可复算分母与禁止项（062/067/068 `requirements.md` 字节不变；效率度量复用 068 通道、不新建统计/评分/台账）？[Measurability, Req §FR-026–§FR-027, §SC-008；三份 sha256 已复测一致]

## G. 接线（W1–W4）与兼容分发

- [x] CHK029 W2 在 `templates/commands/humanize.md` 增加一次脚本调用（lookup），而复杂度判据的 owner 定义「命令 invoke scripts/CLI tools ⇒ complex」，且 complex 命令按该 owner 应带 wrap-up 面；这与契约 C-15 / compatibility C-5「humanize 保持 Simple、无 `## Wrap-up`」及既有 `test_c01_thin_entry_shape` 直接冲突——哪一侧让步？[Conflict, Req §FR-004 / §FR-025; `shared/workflow/feedback-step.md` 开篇; contracts C-15/C-5] → 已处置: **复杂度判据胜出，humanize 保持 Simple**。裁定：`templates/commands/humanize.md` 只加 **owner 指针**、不调用任何脚本（新增 SA-8、FR-025 后半句）；该流程唯一的 lookup 与最小算子集执行移入 `skills/external/humanize/SKILL.md` 的 **Stage 6 执行体**（W4）。同步改写：plan §Minimal Designated Wiring W2/W4 与接线语义、A2/A6 断言、§既有表面契约硬约束（新增「humanize.md 不得出现任何脚本调用」行）；contracts `flow-class-ledger.md` C-9/C-15、`expression-gate-operators.md` C-14（W2 行改为「不读取」、W4 行承载唯一 lookup）与 C-15、`compatibility-distribution.md` C-4/C-5/C-6/C-7/C-10；data-model E10（`/speckit.humanize` 行 `lookup: none`、`skill:humanize` 行必选 lookup）；tasks T024（W2）/T025（W4，`blockedBy: T010,T024`）/T026（副本形态）；quickstart 场景 4 的 grep 期望；research R4 修订段。**实测**：`test_humanize_command_surface.py` 10 passed，模板非表格行 40（上限 120）、无 `## Wrap-up`、`SKILL.md` 唯一一处、零 `flow-class-check` 引用——Simple 形态未被触碰。
- [x] CHK030 「未刷新项目无调用点、行为不变」与「刷新后副本与 owner/引擎同包到位」两态是否有可核对的构成，接线封闭集（4 入口 + `feedback-step.md` 一行指针；其余 25 模板与 49 技能零引用）是否可机械核对，且命令副本是否被定义为生成物并配「先重生成再 `--check`」+「副本正文含接线」两道判据（防「只改模板、未重生成」假绿）？[Completeness, contracts `compatibility-distribution.md` C-3–C-7; plan § Test Strategy A6; 8 个副本当前均存在]

## H. 验收判据的可测量性

- [x] CHK031 8 条 SC 是否各有测量源、且每条都能回到支撑它的 FR（含「无来源记 not-evaluated，不记 0、不记达成」的诚实条款）？[Completeness, Req §Success Criteria / §Measurement Sources; tasks T035]
- [x] CHK032 §SC-005 的「单阶段人工确认 ≤3 次」是否有对应 FR——§FR-024 只要求冻结与对照基线，从未设上限？[Traceability, Req §SC-005 / §FR-024] → 已处置: FR-024 增补「单阶段人工确认次数 MUST ≤3，超出即判该阶段门禁设计缺陷」，SC-005 的上限由此有 FR 支撑；data-model E8 与 contracts C-9 的基线口径不变（上限属判定阈值，不是基线量）。
- [x] CHK033 §SC-003 的「3 个真实文档型特性」如何选取、不足 3 个时如何处置（tasks T035 允许 not-evaluated，SC 本身未写）？[Measurability, Req §SC-003; tasks T035] → 已处置: SC-003 增补样本选取规则——「本特性登记后最近 3 个已完成的表达类特性（按 `features.md` 登记顺序）；不足 3 个时记 `not-evaluated` + reason（不记 0、不记达成）」；§Measurement Sources 的 SC-003 Source 同步。
- [x] CHK034 §SC-004 / §SC-005 / §SC-006 的「同类规模、同类读者面」用什么量刻画，且「门禁调用次数」能否从按单元记录（exec-quant 记录粒度是命令/技能运行，不是单次检查）中分离出来——被过滤的门禁单元集是否已在开工前冻结？[Measurability, Req §SC-004–§SC-006; contracts C-9] → 已处置: §Measurement Sources 增补可比性与可分离口径——「同类规模 = 规格产物文件数与 FR/SC 数各在基线 ±30% 内；同类读者面 = 同一基准读者声明；门禁调用次数的**过滤集合** = 开工前与三项基线一同冻结的声明门禁单元集（门禁 owner 调用点表的算子名 → 单元 id 映射），冻结物写入 `notes/expression-baseline.md`」。计数粒度（按运行记录过滤到声明的单元集）因此可复算。

## I. 任务覆盖与红先证据

- [x] CHK035 27 FR 与 8 SC 是否全部进入覆盖表、50 条款是否恰各被一行 `[green:]` 认领、任务分布是否与声明一致？（机械复算：unmapped FR/SC = 0；green 50/50 无重复无缺失；3/8/15/4/5 = 35；11 行义务行已在覆盖表外显式声明） → 已处置（checklist 修复轮重算）: 任务分布改为 **3/9/15/4/5 = 36**（新增 T005 后 US1 由 8 变 9，其余任务号顺延一位）；`[green:]` 条款分区随号平移后仍 50/50 无重复无缺失，unmapped FR/SC 仍为 0（`validate-tasks.py` 与 `pre-analyze-check.py --stage tasks` 均 exit 0）。
- [x] CHK036 7 支新测试能否**证伪**本切片的主张——现有断言面全是「在场/缺席」的结构断言，任一把单元判错类、把阶段映射接错面都不会被任何测试判红；FR-006 / SC-001 的两人一致演练仍是人工且允许「写明未执行的 reason」？[Measurability, Req §FR-006 / §SC-001; plan § Test Strategy] → 已处置: 新增第 8 支测试 `tests/contract/test_flow_class_correctness.py`（T005，US1 红先行）：固定 fixture ≥10 个流程单元（两类各 ≥3 / 未声明 ≥1 / 类中立 ≥1 / 混合 oracle ≥1），逐单元断言 lookup 的类别/来源/依据/标记与**独立书写的 oracle** 相符；再加**变异断言**——临时副本中把一个单元的类别改错后重跑，比对 MUST 转红（改对回绿），使「判错类」能被机器证伪。SC-001 改为「可由该 fixture 机械核验」，两人演练降为并列人工证据（未执行记 not-evaluated）。plan（Scale/Scope、Test Strategy 清单）、tasks（DoD-4、T005、T012、覆盖表、分布）、feature-ref（Test Mapping、SC-001）与 quickstart（场景 1）同步。
- [x] CHK037 红先（Red-first）是否有落点与判据（每支测试一条命令、真实输出、退出码，先红后绿），而非以「实现后再写测试」代替？[Completeness, tasks §Tests Mode ON / §Tests；`notes/red-first-evidence.md` 为实现期落点]

## J. 事实一致性与证据等级

- [x] CHK038 实测数字与路径事实是否一致且可复算？（本次复测：命令 27 / 技能 51 / 单元 78 / 条款 50（15+15+10+10）/ 任务 35 / FR 27 / SC 8 / `pytest --collect-only tests` 5361 / `tests/contract` 4190 / 189 文件·1974 函数 / 307 文件·2915 函数 / `violations=3` / 8 个副本存在 / 三份前序规格 sha256 一致 / 31 条基线 node id 全部可解析 / `MIRROR_PAIRS` 在 `sync-mirrors.py:82` / shared 拷贝段在 `src/specify_cli/__init__.py:2462`）[Consistency, tasks §Measured Premises] → 已处置（checklist 修复轮重算）: 任务数由 35 变 **36**（其余数字不变：命令 27 / 技能 51 / 单元 78 / 条款 50 / FR 27 / SC 8 / 4 Shared Strings）；新增一条实测前提「humanize 命令形态 = Simple（`test_humanize_command_surface.py` 10 passed；非表格行 40、无 `## Wrap-up`、`SKILL.md` 唯一一处、零 `flow-class-check` 引用）」，已写入 tasks §Measured Premises 与 §Environment Prerequisites。
- [x] CHK039 两处不可执行/不可复现的字面量是否已按同作者门修正（`sync-mirrors.py --only a,b,c` → 可重复旗标；「非表格行 ≤ 120 字符」→ 非表格行**数** ≤ 120；`pre-analyze advisories=0` 标注为 requirements 阶段值并给出 79 条 missing-path 复测值）？[Clarity, tasks T015/T033；quickstart 场景 0/4；plan §Phase 0] → 已处置（任务号随本轮顺延；`advisories` 现为 90，见 Notes）
- [x] CHK040 requirements 自身的事实性断言是否按 §FR-020 标注证据等级与 as-of——本文件与 SC 的测量源大量引用实测命令，但 requirements.md 全文没有 `实测/推断/引用` 与日期标注（FR-020 只约束「表达类流程的文档型交付物」，未说明规格产物是否在内）？[Consistency, Req §FR-020 / §Measurement Sources] → 已处置: 裁定 FR-020 **只约束表达类流程的文档型交付物**，规格产物不在其强制标注面内；本切片自判 `execution`（research R12），故 `requirements.md` 不受逐条标注约束，其「可复算」由 §Measurement Sources 的命令与捕获日期承担。新增 SA-10 明文记录该边界，避免把执行类规格误纳入表达类门禁。

## Notes

- **本清单之外的规格修正（首轮已落盘，均属 correction 而非 decision）**：① `tasks.md` 与 `quickstart.md` 场景 4 的 `sync-mirrors.py --only shared,scripts,skills` 改为可重复旗标（实测逗号形式 exit 2：`--only prefix matches no mirror pair or regen surface`）；② `tasks.md` 与 `plan.md`/`research.md` 的「非表格行 ≤ 120 字符」改为「非表格行**数** ≤ 120」（`test_c01_thin_entry_shape` 断言的是行条数，当前 40 条）；③ `data-model.md` E7 的 `rule` 取值补 `grade-invalid`（契约 C-3 有四条 evidence 规则，E7 原缺一）；④ `tasks.md` §Requirement Coverage Map 的「义务行」枚举补 `T004`（该行确未映射 FR/SC）；⑤ `research.md` R1 的「glossary 两行登记 owner」更正为「仅 `流程分类 (Flow Class)` 行登记路径，同批三行只命名概念」；⑥ `plan.md` §Phase 0 与 `quickstart.md` 场景 0 的 `advisories=0` 加注 requirements 阶段语义与 checklist 阶段复测值（79 条 `missing-path`，decision 仍 pass）。
- **checklist 修复轮（本轮，2026-10-24）落盘的规格变更**：
  ① **humanize 复杂度翻转**——W2 改为只加 owner 指针（零脚本调用），lookup 与门禁执行落 W4 技能 Stage 6（对应 CHK029；联动 plan / 4 份契约 / data-model E10 / tasks T024–T026 / quickstart / research R4）。
  ② **`flow_class` 归属**——切片 Shared Strings 增 `STR-003`（父来源父编号 036），SA-3 改写，正文提及改引用（CHK006）。
  ③ **六面封闭**——FR-018 改「恰好六面」+ SA-7；契约 C-1 增 face id 列，C-14/E4 按 exactly 6（CHK019）。
  ④ **证据 `source` 必填**——FR-020 三件套，E6/C-5/checker `source-missing`/tasks 同步（CHK021）。
  ⑤ **分类正确性测试**——新增 `tests/contract/test_flow_class_correctness.py` 与 T005（oracle 比对 + 变异断言），SC-001 改机械可核验；任务规模 35 → 36（CHK036）。
  ⑥ **其余最小补写**——FR-001/002/006/009/011/015/016/019/020/022/023/024/025 与 SA-8/SA-9/SA-10、SC-002/SC-003/SC-004–SC-006 测量源（覆盖 CHK002/004/007/008/010/012/013/014/017/020/022/023/025/026/032/033/034/040）。
  ⑦ **计数同步**——Shared Strings 3 → 4；任务 35 → 36；测试文件 7 → 8；其余计数（27 FR / 8 SC / 50 条款 / 78 单元 / 27 命令 / 51 技能）不变；本轮复测 `validate-requirements.py`（0 error / 0 warning）、`validate-tasks.py`（PASS）、`pre-analyze-check.py --stage requirements|tasks`（均 decision=pass，advisories=90，全部为 `missing-path` 指向待创建的新文件）、`decomposition-check.py --mode tasks`（proceed，task_count=36 ≤ 40）。
- **Assumptions（首轮自裁决，未向用户提问）**：A-1 同作者门未触发——首轮为 fresh-context 只读评审，且本环境无子代理派发工具，按 `.specify/shared/workflow/objective-analysis-gate.md` § 7 以降级形式记录；A-2 范围严格限于 069a，未打开 069b 目录、未改父规格；A-3 只写本清单与上列规格修正，未改任何实现代码/模板/技能/命令副本，未 push；A-4 未重跑 201 s 的 `pytest tests/contract` 全量（该基线与「零新增失败」判据属 `/speckit.implement` 起点动作），本轮只复算采集面与基线 node id 可解析性。
- **Assumptions（修复轮自裁决）**：B-1 本轮由用户委派「修复 checklist 待处置项」并要求「访谈式问题按裁定执行并记录假设」，故未再发起访谈；五条高风险项的裁定原文已写入 requirements §Clarifications（Session 2026-10-24 第二批）与 SA-7…SA-10。B-2 只改 069a 规格/清单与 `notes/parent-fr-mapping.md`（补 STR-003 来源与澄清表），未改父规格、未改任何实现文件、未 push。B-3 任务号采用**全量顺延**（T005 插入为分类正确性测试，原 T005–T035 → T006–T036）而非字母后缀，原因是 `pre-analyze-check.py` 的任务正则只捕获 `T\d{3}`，`T005a` 会被判为 T005 的重复 ID；投影与条款认领随号平移并在 feature-ref 记录。B-4 `feature-ref.md` 的「35 任务行」等计数已同步为 36，`pre-analyze-check.py` 的 count-claim 检查复测为零 error。
- **Disposition 汇总**：40 项 = 已核对成立 **39** 项（`[x]`：首轮 16 + 本轮处置 23）+ 待处置 **1** 项（`[ ]`，`out-of-slice（069b）`：CHK016 的门禁数对照仪器 = 父编号 041）。**无无 disposition 的 `[ ]`；无 `verify-in-implementation` 项**——本轮所有可写的判定定义都已落 requirements/contracts/tasks，剩余实现期动作由 tasks 的 T031/T035 承载，不构成「无法现在下判」的清单项。
- 勾选方式：完成一项后在方括号内写 `x`；发现项已处置时在该行尾追加 `→ 已处置: <依据>`，不要删除原行（保留历史）。
