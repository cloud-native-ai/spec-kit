# 分类本体与文档型门禁 Checklist: 执行/表达二元分类与文档型门禁（Feature 069 / Slice 069a）

**Purpose**: 对 069a 的**需求（What）**做质量审查——判据是否可复现、门禁不变量是否封死、六面文档型门禁与最小接线（W1–W4）是否被完整且无冲突地要求、27 FR / 8 SC / 50 条款能否被 35 个任务覆盖并被证伪。本清单不评判实现好坏，只评判要求写得是否可判定、可测量、可追溯。
**Created**: 2026-10-24
**Feature (Requirement Scope)**: Feature 069（`.specify/memory/features.md` 第 77 行 / `.specify/memory/features/069.md`）；本清单只覆盖切片 `069a-flow-classification-docs-gates`
**Requirements (What)**: [requirements.md](../requirements.md)（27 FR / 8 SC / 3 Shared Strings）
**Specifications (How, context only)**: [plan.md](../plan.md)、[tasks.md](../tasks.md)、[data-model.md](../data-model.md)、[contracts/](../contracts/)（50 条款）、[quickstart.md](../quickstart.md)、[research.md](../research.md)、[notes/parent-fr-mapping.md](../notes/parent-fr-mapping.md)

**Note**: 本清单由 `/speckit.checklist` 生成，用于校验 **需求（What）** 的质量。**规格（How）** 只在两种情况下被引用：暴露需求缺口/歧义/冲突，或核对关键设计决策能否回溯到需求——不用于测试实现行为。

**勾选语义（本次评审的 disposition）**：`[x]` = 本次已核对且**要求本身成立**（证据已在本行给出，可复算）；`[ ]` = **仍有待处置的问题**，行尾以 `→` 标注处置类型：`需规格补写`（要求缺项，建议在 requirements/契约补明）、`需裁决`（两种读法都自洽，必须由用户/维护者择一）、`需被测面承认`（要求成立但当前测试/判据无法证伪它）。

## A. 分类本体与判据可复现性

- [x] CHK001 两个取值是否被封闭声明为仅 `[[STR-001]]` / `[[STR-002]]`、判据是否只回答一个问题（主交付物的验收由机器行为还是人的理解判定）且以 oracle 而非介质表述、类中立是否被明确排除在第三取值之外？[Completeness, Req §FR-001–§FR-002 / §FR-008; research R2; data-model E2/E3]
- [ ] CHK002 「主交付物」本身是否被定义到可判定的程度——多交付物时择一的规则是否唯一，§Edge Cases 追加的「失败不可逆性」与 §FR-002 的单一 oracle 问句是什么关系？[Ambiguity, Req §FR-002 / §Edge Cases 第 1 条; 现象: 两个判别量并存] → 需裁决
- [x] CHK003 判据的非介质性是否有规范性示例，且理由指向 oracle 而非扩展名（Markdown 架构文档→表达；须生成并编译 SDK 的 OpenAPI→执行；站点构建通过不改判定）？[Completeness, Req §FR-003]
- [ ] CHK004 §FR-006 / §SC-001 的「两名独立判定者一致率 100%」是否规定了独立性判据（不同人、不同会话、判定时互不可见）与不一致时的处置顺序（改判据而非逐案裁定）？[Measurability, Req §FR-006 / §SC-001; Measurement Sources 只写「分别落盘后比对」] → 需规格补写

## B. 唯一所有者、台账与命名空间

- [x] CHK005 所有者是否被声明为唯一，且明列它拥有什么（判据、两取值、边界例、逐流程台账、类中立封闭清单、命名空间、变更记录）？[Completeness, Req §FR-005; contracts `flow-class-ledger.md` C-1]
- [ ] CHK006 机器键 `flow_class` 的字面量归属是否自洽——§Assumptions SA-3 声明「本切片不声明 STR-003、也不得复述其字面量」，而 069a 的 contracts / data-model / plan / tasks 合计出现 27 处该字面量，且台账列头必须用它？[Conflict, Req §Assumptions SA-3 / §Shared Strings; data-model E2/E9; contracts C-3] → 需裁决
- [ ] CHK007 `execution` / `expression` 与既有 `Agent Execution`（Agent 三层分类法第三层）的消歧是否有 requirement 级依据（现仅在契约 C-3、research R5 与 `glossary.md` 第 54/173/177 行），而本切片已经开始生产台账列？[Traceability, Req §FR-001–§FR-002; glossary 同名不同义] → 需规格补写
- [ ] CHK008 台账的 `basis` 列（`behavior-oracle` / `reader-oracle` / `mixed-oracle`）能否回溯到某条 FR/SC——它承担 FR-002 与 FR-006 的判定依据，但 requirements 从未定义该字段？[Traceability, data-model E2; contracts C-4] → 需规格补写
- [x] CHK009 台账完备性是否写成「与清单双向覆盖 + 反空真下限」，且互斥类缺陷（`duplicate` / `dual-class` / `invalid-class`）是否被要求各自独立报告而非合并为「有错」？[Completeness, Req §FR-007–§FR-008; contracts C-5/C-6；实测量级 27 命令 / 51 技能 / 78 单元已复测一致]
- [ ] CHK010 「两份分类定义并存」与「客户项目 MAY 为自己新增流程声明类别」两条边界是否有归宿——前者只在 §Edge Cases 要求「副本由生成/刷新产生并带漂移检查」，后者被契约 C-14 明确为「本切片不提供声明面」，却与「零项目侧存储」并存？[Coverage, Req §Edge Cases 第 8 条 / §FR-011; compatibility C-2; flow-class-ledger C-14] → 需规格补写

## C. 默认类与降级

- [x] CHK011 未声明默认（`execution`）、消费点固定标记（`[[STR-004]]`）与「不得把默认呈现为已判定」是否三者齐备，并落到可机械断言的返回字段？[Completeness, Req §FR-009; contracts C-7; data-model E9 invariant]
- [ ] CHK012 「消费点」与 SC-002 的「被检查样本」是否被定义为可枚举对象——标注率 100% 的分母是全部 78 个单元、全部门禁读取点，还是接线后的 4 个入口？[Measurability, Req §FR-009 / §SC-002] → 需规格补写
- [ ] CHK013 「版本不兼容」是否有可判据的载体——台账行与解析结果都没有 version / schema 字段，契约 C-7 以「台账表头缺失」代称版本不兼容？[Clarity, Req §FR-016; contracts C-7; data-model E2/E9] → 需规格补写
- [ ] CHK014 降级标签有两个（`[[STR-004]]` 标记 与 `owner-unavailable`），requirements 未写明二者是「二选一」还是「同时出现」，也未写「降级不得被当作通过」是否适用于全部降级路径？[Consistency, Req §FR-016; contracts C-7/C-15] → 需规格补写

## D. 门禁不变量（分类只换算子）

- [x] CHK015 阶段集合是否被固定为 8 阶段且不因分类改变、clarify 的既有跳过规则是否被排除在「分类影响」之外、analyze 与 review 的 100% 调用率与「阶段完整性判定 MUST NOT 读取类别」是否写明且拒绝规则不带例外？[Completeness, Req §FR-012 / §FR-014; contracts C-10/C-11]
- [ ] CHK016 「只选择算子集、不减少门禁数量、不降 P0/P1、不改阈值」与「与复杂度轴正交」是否有可测分母——本切片的三条基线是调用/确认/墙钟，不含逐阶段门禁数，也没有表达类与执行类的门禁数对照？[Measurability, Req §FR-004 / §FR-013; SC-004–SC-006] → 需被测面承认
- [ ] CHK017 §FR-015「门禁 MUST 在判定之前从唯一所有者读取类别」是全称要求，而本切片只接线 78 个单元中的 4 个入口；该要求的适用面（仅首批成员 / 仅接线面）是否应写进 requirements，而不是只写在契约 C-9/C-15 与 plan？[Ambiguity, Req §FR-015 / §FR-025] → 需裁决

## E. 六面文档型门禁

- [x] CHK018 六面是否各有且仅有一个可解析 `owner_pointer`，且本切片只新增「证据分级与 as-of」「事实一致性」两面（其余四面指向既有 owner）？[Completeness, Req §FR-018; contracts `expression-gate-operators.md` C-1；全部 owner 路径已实测存在]
- [ ] CHK019 六面集合是开放还是封闭——§FR-018 写「至少覆盖六面」，data-model E4 的不变量写「覆盖面 = 6」，而契约 C-14 又要求「沿用 C-1 的六个 face id」，但 C-1 只列中文面名、未定义任何 face id？[Conflict, Req §FR-018; data-model E4; contracts C-1/C-14] → 需裁决
- [ ] CHK020 「文档型交付物」的范围是否被定义（规格产物？技能 `SKILL.md`？命令模板？站点文档？），否则 §FR-019 的阻断面无法枚举，检查器的 S1/S2 集合就成了事实上的定义？[Clarity, Req §FR-019; contracts `doc-consistency-checker.md` C-2/C-4] → 需规格补写
- [ ] CHK021 §FR-020 要求证据「可复算（含命令、退出状态或可定位来源）」，而 data-model E6 把 `source` 定为可选、契约 C-5 只强制 grade/as-of 配对——强制面是否应包含来源？[Conflict, Req §FR-020; data-model E6; contracts C-5] → 需裁决
- [ ] CHK022 「无标注的事实断言不得进入交付」的可判定边界在哪——research R7 已拒绝「每句都标」并把机械面收敛为配对规则，这个强弱差是有意让步还是待补的判定定义？[Clarity, Req §FR-020; research R7; contracts C-5] → 需规格补写
- [ ] CHK023 新增「证据等级/as-of」面与既有证据机制的对象差异是否在 requirement 层写明（`evidence-step.md` 描述机制七态、`single-run-evidence.md` 描述一次执行的留存），以免被读成重定义或收窄？[Consistency, Req §FR-020; data-model E6; research R6] → 需规格补写
- [x] CHK024 「结构/链接/构建只是必要条件」「判据为零新增违规（基线 3 条既有违规）」「站点层缺席记 `not-applicable`」是否三者齐备且互相不矛盾？[Completeness, Req §FR-021; contracts C-6；基线 `violations=3`（broken-link 2 + note-frontmatter 1）已复测]
- [ ] CHK025 §FR-022 的绝对判据（同一事实 ≥2 处手写即缺陷）与其机械实现（完全相等且 ≥24 字符，或 ratio ≥0.90 且 ≥40 字符）之间的落差是否被承认——低于阈值的真副本按设计不会被报出？[Measurability, Req §FR-022; contracts `doc-consistency-checker.md` C-5] → 需被测面承认
- [ ] CHK026 评审门禁的判定者身份与三项基线的「开工前」时点是否被定义——§FR-023 的「人工评审」是否允许代理执行、如何与代码评审的判定对象机械区分；§FR-024 的冻结时点以哪个工件的哪次记录为准（SC-006 用 requirements 首次提交，另两项未定）？[Ambiguity, Req §FR-023–§FR-024; contracts C-8/C-9; data-model E8] → 需规格补写

## F. 表达类首批成员与既有特性

- [x] CHK027 §FR-025 是否同时固定了三件事：`/speckit.docs` 与 `/speckit.humanize` 登记为表达类、既有门禁「只补强不削弱」、补强形态封闭为最小接线（4 入口，每处只加 lookup 与 owner 指针）？[Completeness, Req §FR-025; contracts C-11/C-12/C-15]
- [x] CHK028 §FR-026–§FR-027 是否给出可复算分母与禁止项（062/067/068 `requirements.md` 字节不变；效率度量复用 068 通道、不新建统计/评分/台账）？[Measurability, Req §FR-026–§FR-027, §SC-008；三份 sha256 已复测一致]

## G. 接线（W1–W4）与兼容分发

- [ ] CHK029 W2 在 `templates/commands/humanize.md` 增加一次脚本调用（lookup），而复杂度判据的 owner 定义「命令 invoke scripts/CLI tools ⇒ complex」，且 complex 命令按该 owner 应带 wrap-up 面；这与契约 C-15 / compatibility C-5「humanize 保持 Simple、无 `## Wrap-up`」及既有 `test_c01_thin_entry_shape` 直接冲突——哪一侧让步？[Conflict, Req §FR-004 / §FR-025; `shared/workflow/feedback-step.md` 开篇; contracts C-15/C-5] → 需裁决
- [x] CHK030 「未刷新项目无调用点、行为不变」与「刷新后副本与 owner/引擎同包到位」两态是否有可核对的构成，接线封闭集（4 入口 + `feedback-step.md` 一行指针；其余 25 模板与 49 技能零引用）是否可机械核对，且命令副本是否被定义为生成物并配「先重生成再 `--check`」+「副本正文含接线」两道判据（防「只改模板、未重生成」假绿）？[Completeness, contracts `compatibility-distribution.md` C-3–C-7; plan § Test Strategy A6; 8 个副本当前均存在]

## H. 验收判据的可测量性

- [x] CHK031 8 条 SC 是否各有测量源、且每条都能回到支撑它的 FR（含「无来源记 not-evaluated，不记 0、不记达成」的诚实条款）？[Completeness, Req §Success Criteria / §Measurement Sources; tasks T034]
- [ ] CHK032 §SC-005 的「单阶段人工确认 ≤3 次」是否有对应 FR——§FR-024 只要求冻结与对照基线，从未设上限？[Traceability, Req §SC-005 / §FR-024] → 需规格补写
- [ ] CHK033 §SC-003 的「3 个真实文档型特性」如何选取、不足 3 个时如何处置（tasks T034 允许 not-evaluated，SC 本身未写）？[Measurability, Req §SC-003; tasks T034] → 需规格补写
- [ ] CHK034 §SC-004 / §SC-005 / §SC-006 的「同类规模、同类读者面」用什么量刻画，且「门禁调用次数」能否从按单元记录（exec-quant 记录粒度是命令/技能运行，不是单次检查）中分离出来——被过滤的门禁单元集是否已在开工前冻结？[Measurability, Req §SC-004–§SC-006; contracts C-9] → 需被测面承认

## I. 任务覆盖与红先证据

- [x] CHK035 27 FR 与 8 SC 是否全部进入覆盖表、50 条款是否恰各被一行 `[green:]` 认领、任务分布是否与声明一致？（机械复算：unmapped FR/SC = 0；green 50/50 无重复无缺失；3/8/15/4/5 = 35；11 行义务行已在覆盖表外显式声明）[Completeness, tasks §Requirement Coverage Map / §Task Distribution]
- [ ] CHK036 7 支新测试能否**证伪**本切片的主张——现有断言面全是「在场/缺席」的结构断言，任一把单元判错类、把阶段映射接错面都不会被任何测试判红；FR-006 / SC-001 的两人一致演练仍是人工且允许「写明未执行的 reason」？[Measurability, Req §FR-006 / §SC-001; plan § Test Strategy] → 需被测面承认
- [x] CHK037 红先（Red-first）是否有落点与判据（每支测试一条命令、真实输出、退出码，先红后绿），而非以「实现后再写测试」代替？[Completeness, tasks §Tests Mode ON / §Tests；`notes/red-first-evidence.md` 为实现期落点]

## J. 事实一致性与证据等级

- [x] CHK038 实测数字与路径事实是否一致且可复算？（本次复测：命令 27 / 技能 51 / 单元 78 / 条款 50（15+15+10+10）/ 任务 35 / FR 27 / SC 8 / `pytest --collect-only tests` 5361 / `tests/contract` 4190 / 189 文件·1974 函数 / 307 文件·2915 函数 / `violations=3` / 8 个副本存在 / 三份前序规格 sha256 一致 / 31 条基线 node id 全部可解析 / `MIRROR_PAIRS` 在 `sync-mirrors.py:82` / shared 拷贝段在 `src/specify_cli/__init__.py:2462`）[Consistency, tasks §Measured Premises]
- [x] CHK039 两处不可执行/不可复现的字面量是否已按同作者门修正（`sync-mirrors.py --only a,b,c` → 可重复旗标；「非表格行 ≤ 120 字符」→ 非表格行**数** ≤ 120；`pre-analyze advisories=0` 标注为 requirements 阶段值并给出 79 条 missing-path 复测值）？[Clarity, tasks T014/T032；quickstart 场景 0/4；plan §Phase 0]
- [ ] CHK040 requirements 自身的事实性断言是否按 §FR-020 标注证据等级与 as-of——本文件与 SC 的测量源大量引用实测命令，但 requirements.md 全文没有 `实测/推断/引用` 与日期标注（FR-020 只约束「表达类流程的文档型交付物」，未说明规格产物是否在内）？[Consistency, Req §FR-020 / §Measurement Sources] → 需裁决

## Notes

- **本清单之外的规格修正（本轮已落盘，均属 correction 而非 decision）**：① `tasks.md` T032 与 `quickstart.md` 场景 4 的 `sync-mirrors.py --only shared,scripts,skills` 改为可重复旗标（实测逗号形式 exit 2：`--only prefix matches no mirror pair or regen surface`）；② `tasks.md` T014/T023 与 `plan.md`/`research.md` 的「非表格行 ≤ 120 字符」改为「非表格行**数** ≤ 120」（`test_c01_thin_entry_shape` 断言的是行条数，当前 40 条）；③ `data-model.md` E7 的 `rule` 取值补 `grade-invalid`（契约 C-3 有四条 evidence 规则，E7 原缺一）；④ `tasks.md` §Requirement Coverage Map 的「义务行」枚举补 `T004`（该行确未映射 FR/SC）；⑤ `research.md` R1 的「glossary 两行登记 owner」更正为「仅 `流程分类 (Flow Class)` 行登记路径，同批三行只命名概念」；⑥ `plan.md` §Phase 0 与 `quickstart.md` 场景 0 的 `advisories=0` 加注 requirements 阶段语义与 checklist 阶段复测值（79 条 `missing-path`，decision 仍 pass）。
- **Assumptions（本轮自裁决，未向用户提问）**：A-1 同作者门未触发——本轮为 fresh-context 只读评审，且本环境无子代理派发工具，按 `.specify/shared/workflow/objective-analysis-gate.md` § 7 以降级形式记录；A-2 范围严格限于 069a，未打开 069b 目录、未改父规格；A-3 只写本清单与上列规格修正，未改任何实现代码/模板/技能/命令副本，未 push；A-4 未重跑 201 s 的 `pytest tests/contract` 全量（该基线与「零新增失败」判据属 `/speckit.implement` 起点动作），本轮只复算采集面与基线 node id 可解析性。
- **Disposition 汇总**：40 项 = 已核对成立 **16** 项（`[x]`）+ 待处置 **24** 项（`[ ]`；其中 `需规格补写` 13、`需裁决` 7、`需被测面承认` 4）。最需要先决的两项是 CHK029（humanize 因接线由 Simple 变 Complex，与既有契约/测试正面冲突）与 CHK006（`flow_class` 字面量归属与 SA-3 自相矛盾）：二者都会在实现期直接决定「哪些文件能改、改到什么程度」。
- 勾选方式：完成一项后在方括号内写 `x`；发现项已处置时在该行尾追加 `→ 已处置: <依据>`，不要删除原行（保留历史）。
