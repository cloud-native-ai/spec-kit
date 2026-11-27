# Requirements-Quality Checklist: Batch Decision Panel — 待决策项集中呈现、建议默认与异议式裁决

**Purpose**: 检验 Feature 112 需求文本（`requirements.md`）的**写作质量**——封闭来源清单的候选存在与去重身份是否可机器判定、入口面与引擎接口是否可验收、建议默认值与接地的推导是否封闭可解析、异议式应答与沉默接受的判定口径是否成立、处置是否落进既有载体并只凭记录可重放、完备性与拒绝是否诚实、人工与 `ai-autonomous` 是否干净分离、面向用户的呈现是否可读、重决是否与既有取代/记录规则相容，以及每条需求与成功标准是否可追溯到条款与证据。每条都是对需求文本（或它点名的 owner 行 / 契约条款 / plan 前提）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-27
**Feature (Requirement Scope)**: Feature 112 Batch Decision Panel（批量决策面板）— `.specify/features.md` 行 112（详情 `.specify/features/112-decision-batch-panel.md`），状态 `Planned`。本清单位于 `/speckit.implement` 之前，按 Feature Integration Protocol 不发起 `Implemented → Ready for Review` 迁移，也不编辑 registry。
**Requirements (What)**: [../requirements.md](../requirements.md) — 本轮机械读数（2026-11-27，`validate-requirements.py`，逐字输出见 `../test-evidence/checklist-requirements-validator.txt`）：`status: ok`，**437 行 / 55 definition rows / 15 shared strings / 0 error / 0 warning**；程序计数（`../test-evidence/checklist-spec-readings.txt`）：**45 FR**（FR-001…FR-045）、**10 SC**（SC-001…SC-010）、**15 STR**（STR-001…STR-015，正文引用 15/15 全部解析）、**25 条 A 裁定**（A-1…A-25）、**5 个用户故事**、**24 条 Edge Cases**、**8 行 Runtime Stack**（RS-001…RS-008）、**2 段 Clarifications 会话 / 16 条 `- Q:` 行**（plan/tasks/feature-ref 头部写「13 clarification rows」，与本节实测的 11 + 5 = 16 不符；以要件正文的 16 条为准，差异作为读数披露记录，不改写既有制品）。
**Specifications (How, context only)**: [../plan.md](../plan.md)（23 行宪法检查 / PA1–PA6 / EP-001…EP-007）、[../tasks.md](../tasks.md)（**58** 任务行 / 11 个 `[P]` / 5 个验证行承载 54 条 `[green:]` 认领）、[../contracts/](../contracts/)（**6 文件 / 54 条款**：source-roster C-101…C-110 / presentation C-201…C-208 / default-derivation C-301…C-307 / objection-reply C-401…C-409 / record-replay C-501…C-512 / completeness-refusal C-601…C-608）、[../data-model.md](../data-model.md)（**13 实体 / 22 不变量 / 5 个状态域**）、[../quickstart.md](../quickstart.md)（**7 场景**）——**只**用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。
**Readers**: 按 `.specify/shared/guidelines/user-facing-comprehension.md` 的全局基准读者判定——需要决定「本需求集能否从 checklist 放行进 analyze / implement」的框架维护者与项目所有者；不新建读者基准。
**Reading scenario**: 复核者打开本文件，决定三件事：(1) 哪几条需求缺陷必须在 analyze / implement 之前修掉；(2) 哪些项可登记为「已裁定、由下游承载」而放行；(3) 哪些项因判据依赖尚未落地的机制（所有者页、引擎、批次记录）而保持观察。按条末的 `[Req §…]` / `C-NNN` / `SC-NNN` 锚回到正文逐字核对。
**Focus / Depth / Audience**: Focus = 阶段简报的九组聚焦簇（来源清单完备性与去重 reconciliation · 入口面 · 证据接地的默认推导与无证据标注 · 仅异议应答与沉默即接受 · 经既有载体的记录与重放 · 批次完备性与拒绝 · 人工 / `ai-autonomous` 边界 · 可读性 · 重决规则）叠加 taxonomy 的九个质量维度；Depth = **Deep**（简报把上述簇写成必覆盖集并要求每个 FR 与 SC 至少被覆盖一次，默认 Standard 不足以承载）；Audience = **Reviewer**。阶段简报已使意图明确，技能 §2 的三个意图澄清问题按「已预答」跳过；默认值与升深理由记录于此。
**Detection path**: same-author 条件**不成立**——`requirements.md` / `plan.md` / `tasks.md` 由本无人值守 SDD 线内的独立阶段执行体撰写，本执行体未曾撰写所分析的任何制品；按 `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 的「作者不同」分支，门不触发，未派发 fresh-context 检测代理（角色模板与派发均明令不得再派发代理）。缺口扫描由本执行体直接完成；可机械核对的前提（FR / SC / STR / A / 边界案例 / 条款 / 任务 / EP / 实体 / 场景 / register open 行 / PENDING 块）均以程序读数当场取证，见 Notes 与 `../test-evidence/checklist-spec-readings.txt`。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成；方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`，结构模板为 `.specify/templates/checklist-template.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner 行 / 契约条款 / plan 前提）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，不是一条实现任务。

## 一、来源清单完备性与去重 reconciliation

- [ ] CHK001 - 两个来源的**候选存在谓词**是否可机器判定到实现无关的程度——`register-open-decision-row` 的「去 markdown 强调」具体剥离哪些记号（`*` / `**` / `_` / `` ` ``）、行 id 与状态单元格的前导空白与词边界 `open` 判定、`authored-pending-item` 的 `### PENDING —` 标题前缀与围栏代码块排除、以及「tracked Markdown 载体」以 git 跟踪还是工作树在场为基准，是否逐项写明？[Clarity, Completeness, Req §Pending-Source Roster, Req §FR-006, C-101, SC-001]
- [ ] CHK002 - register 行的**权威路径落在哪个单元格、以何种可解析形态**是否被钉死——roster 只说「该行单元格中的显式仓库相对路径」，未指名列、未说明多个单元格或多路径如何取舍、未写路径基准与列序假设，「恰有一个匹配块」能否在任意 register 表形态上被唯一判定？[Ambiguity, Gap, Req §Pending-Source Roster, Req §A-22, Req §FR-010, C-105]
- [ ] CHK003 - **去重身份**的边界是否穷尽——两个 `subject` 逐字节相同但都带 `resource_locator` 而 `same_name_conflict` 未声明为 true 时是否仍按「同名族」比较定位值；一个带定位、一个不带定位时「不合并」的读法是否与「同名族成对在场」相容；合并行的「全部来源」是否包含被并掉的 register 行与其它引用？[Ambiguity, Consistency, Req §A-22, Req §FR-009, Req §Pending Item Block, C-104]
- [ ] CHK004 - **候选存在 vs 资格的缺陷分层**是否在需求文本内自洽——「无块、权威路径不可解析」在 FR-011 被归为类别未知并点名 `class-missing`，而 §Pending-Source Roster 与 FR-010 对同一情形点名 `authority-unresolved` / `ambiguous-link`；哪一个是唯一原因词，类别判定失败与联接失败同时成立时是否并列点名？[Conflict, Req §FR-010, Req §FR-011, Req §A-21, Req §A-23, C-105, C-106]
- [ ] CHK005 - **排除族与已解决族**的计数归属是否闭合——`not-human-held` / `already-resolved` / `duplicate-merged` 是否穷尽全部「不呈现」的原因；同一候选同时命中「已解决」与「非人持有」时哪个原因计入记账；一个既不能呈现也不能具名排除的候选是否被 FR-016 的拒绝承接而不是静默消失？[Completeness, Req §FR-007, Req §FR-012, Req §Batch States, C-107, C-108, C-606, SC-001]

## 二、入口面与单所有者扩展（entry surface & single-owner extension）

- [ ] CHK006 - 入口的**用户可见调用面**是否被需求钉住——`/speckit.decide` 的调用形态（无参扫描？批次中如何提交应答？）与命令 / 技能 / 引擎三者的职责边界是否有需求级锚点，而不仅出现在交付路径清单；「交互授权级别 MUST 由调用方显式声明」中的「调用方」被定义为用户、命令还是技能，级别取值域是否为封闭集？[Gap, Ambiguity, Req §A-5, Req §FR-039, Req §FR-040, C-406, C-608]
- [ ] CHK007 - 引擎接口面与**落地闭环**是否按可验收项写全——封闭动作集 `scan` / `record` / `replay`、未声明选项非零拒绝、`-h` / `--help` / `--version`、只读/写入面与退出码（0 成功含 `nothing-pending`、1 具名拒绝、2 用法/环境错误）在帮助正文与 `docs/reference/commands/decide.md` 两面是否被要求一致；命令模板、技能、引擎、命令文档、框架地图、冻结命令/技能名基线、镜像与每工具副本是否同一变更收口，fresh `specify init` 是否被要求收到命令与技能？[Completeness, Measurability, Req §A-15, Req §FR-039, Req §FR-042, Req §FR-043, C-511, C-608, SC-009]
- [ ] CHK008 - **单所有者扩展**是否被写成加法式且无第二定义点——全部批次规则面（新词、P-13、条件层三字段、边界）是否只由既有决策治理所有者页 [[STR-001]] 拥有，其他面以指针抵达且不复述判据表；是否禁止第二所有者页、第二登记/队列/存储/schema/调度器；既有记录与既有词汇含义是否零改写；零网络、零自动传输、零反馈存储写入与不与 ai-harness 091 对齐是否同文？[Completeness, Non-Functional, Req §FR-001, Req §FR-002, Req §FR-003, Req §FR-004, Req §FR-005, C-511, C-512]

## 三、建议默认值与证据接地

- [ ] CHK009 - **默认值来源**是否被钉到单一可判定命题——唯一 `default: yes` 成员、零个或多个默认的 `no-default` 结局、面板「不得发明」的边界（默认标签、选项、后果、可逆性、证据）是否逐项写出，并与 107 选项集契约保持指针关系而非第二套规则？[Completeness, Consistency, Req §FR-021, Req §FR-024, Req §Pending Item Block, C-301, C-302, SC-002]
- [ ] CHK010 - **接地联接的封闭输入**是否完整且互斥——(a) 默认选项 `evidence` 指针、(b) `context` 逐字包含主体全名的既往记录、(c) 其引用的 `T-NNN`，与既往经验载体闭集（四扫描根决策记录、批次记录、`T-NNN`、history、feedback、knowledge）是否一一对应；「逐字包含」的匹配基准（大小写、空白、Unicode）与「既往记录」是否包含本批次记录是否写明；联接与冲突判定是否明确由确定性引擎而非模型完成？[Clarity, Completeness, Req §A-6, Req §FR-022, Req §FR-039, C-303, C-307, SC-003]
- [ ] CHK011 - **`grounded` 的「可解析」**是否被量化——路径存在即算，还是要求锚点可找到；需求文本只说「可解析指针」，契约 C-304 增加「给出锚点时锚点可找到」，该增量是否经指针回到同一 owner；`basis` 不计证据的规则是否在块字段表、FR-022 与条款三处一致？[Ambiguity, Measurability, Req §FR-022, Req §Pending Item Block, C-304, SC-003]
- [ ] CHK012 - **`no-evidence` 与 `incomplete` 的关系**是否穷尽——默认选项的 `evidence` 指针不可解析时，Edge Case 判块 `incomplete`（缺失要素），而 FR-022 只允许输出 `grounded` / `no-evidence`；该行的接地状态应读哪一个、是否允许 `incomplete` 行同时带 `no-evidence`、这是否仍满足「不得暗示经验支持」？[Conflict, Edge Case, Req §FR-022, Req §Edge Cases, Req §Batch States, C-305, SC-003]
- [ ] CHK013 - **前例冲突**的判定与否证是否完整——主体全名逐字命中多条既往记录且所选选项有同有异时的冲突判定；既往记录载体不可读时是呈现冲突、拒绝还是披露；冲突项「不得经沉默结案」是否与资格合取式（FR-024）逐字一致？[Gap, Consistency, Req §FR-023, Req §FR-024, Req §A-7, C-306, SC-006]

## 四、仅异议应答与沉默即接受

- [ ] CHK014 - **「应答」的判定口径**是否封闭到可判定——「显式回复（含「无异议」、点名异议或暂缓）」中的「含」是穷举还是示例；「好的 / 同意 / 都行」等肯定式回复与对某项的评论算不算应答；追问不构成应答的规则由谁判定（技能行为还是引擎结构），是否说明该判断属行为类而原文仍逐字留痕？[Ambiguity, Req §A-25, Req §FR-027, C-401, C-402, SC-004]
- [ ] CHK015 - **沉默接受的资格合取式**是否与呈现状态一一对应——`human-interactive`、块完整、恰一个默认、默认可逆、无 `source-conflict`、无 `prior-decision-conflict`、未被先前批次解决七项，是否与 §Batch States 的六种呈现状态及各排除状态互补且无缺口；「交互式批次且已获应答」的批次级条件是否与项级条件分开表述，且不跨批次预授权默认值？[Completeness, Consistency, Req §FR-024, Req §FR-027, Req §FR-031, C-404, C-409, SC-004]
- [ ] CHK016 - **应答校验与零写入**是否覆盖全部拒绝形态——未知身份、重复条目、非成员标签、`other` 无 `path` 时的新选项、对已解决项的异议、对不合格项的改选（仅当选项集文法完整且 `subject` / `context` 可解析时允许）是否各有具名结局，且校验在写任何记录之前完成？[Completeness, Edge Case, Req §FR-026, Req §Edge Cases, C-403, C-407, SC-004]
- [ ] CHK017 - **暂缓（park）** 的语义是否完整——不产生决策记录、项保持待定、批次记录留下暂缓行、下次批次重新呈现、不发选择信号五件事是否齐备；暂缓项在 register 保持 `open` 并标注批次、来源块不改写是否写明？[Completeness, Clarity, Req §FR-028, Req §FR-030, Req §FR-034, C-405, C-408, SC-004]
- [ ] CHK018 - **无人值守与授权级别**的处置是否无缺口——未声明授权级别按无人值守处理、无人值守可只读扫描但记录接受被具名拒绝、不得从终端形态/环境/沉默推断授权；「拒绝记录」的退出语义与「被拒尝试零痕迹」是否与 A-24 一致？[Consistency, Req §FR-040, Req §A-24, Req §Edge Cases, C-406, SC-007]
- [ ] CHK019 - **处置闭集与信号复用**是否单一权威——`accepted-default` / `objected-alternative` / `objected-parked` 三值与 `pending`（非处置）的边界；处置→门控观察信号的映射（`approved-as-is` / `modified`，park 无信号）是否只以指针抵达 `confirmation-gates.md` 而不在规格内另立第二词表？[Consistency, Completeness, Req §FR-028, Req §FR-030, C-405, C-408]

## 五、经既有载体的记录、登记与重放

- [ ] CHK020 - **批次记录**的载体与内容是否闭合——既有 knowledge 存储一文件一批次、经记忆引擎写入、标题前缀与批次编号、批次头（编号 / 时点 / 工具版本 / 逐来源计数 / 完备性判定 / 授权 / 原文引用块）、逐项行表、已决记录块；「不是第二存储或共享可变聚合」是否与 A-11 / FR-004 一致，frontmatter schema 是否明确归记忆引擎所有而不在本规格复制？[Completeness, Consistency, Req §A-11, Req §FR-004, Req §FR-032, Req §FR-037, C-503, SC-005]
- [ ] CHK021 - **决策记录与批次族字段**是否加法且可读旧记录——三字段必须同时出现且仅批次产生的记录携带；既有记录零改写、继续按 legacy/现行规则读取；`rationale` 要点与原文层（批次记录引用块）的分工在 FR-032 / FR-033 两处是否一致；`evidence` 必须含接地、来源项与批次记录三个指针是否完整；传递实施是否复用 107 审计链而不产生第二条记录或传输路径？[Consistency, Completeness, Req §A-12, Req §FR-033, Req §FR-038, Req §A-25, C-504, C-509, SC-005]
- [ ] CHK022 - **register 反映**的可判定性是否足够——已决行「点名批次与决策编号」的**状态单元格取值文法**是否有单一形态（否则「起始词 `open`」的扫描谓词与人工修复没有共同解析基准）；追加行的「载体+区间」分组是否有可解析格式；「除状态单元格与追加行外零改写」的边界是否与 register 缺席时「按既有头部形态创建」相容？[Ambiguity, Measurability, Req §FR-034, Req §FR-012, C-505, SC-005]
- [ ] CHK023 - **来源状态同步与失败披露**是否落地到可审计载体——`resolution` 值形状固定为 `<batch_id> -> <D-NNN>` 且块内容零改写；批次记录写入成功后 register 更新失败的「披露」写到哪里（批次记录追加？下一批次输出？仅控制台？），该披露是否留痕到可重放载体，读时联接如何阻止重复呈现？[Gap, Measurability, Req §FR-035, Req §FR-012, Req §Edge Cases, C-506, SC-005]
- [ ] CHK024 - **重放**是否只凭记录即可重建且不静默跳过——重建对象（项集、完备性、默认值与接地、异议与处置、决策记录）、只读与确定性、任一不可解析指针非零退出、不得用对话记忆补足；重放的**输入定位**（如何从批次编号找到批次记录、是否需要 register）是否在需求中写明？[Completeness, Clarity, Req §FR-036, Req §A-11, C-508, SC-005]
- [ ] CHK025 - **幂等、并发与扫描确定性**是否完整——同批次编号第二次记录在写面之前拒绝且绝不 upsert；不同批次不同路径且互不读写；register 编号冲突按既有 renumber 修复而非静默改号；批次编号形态与铸造时点（全部前置校验通过后、首条写入前）；被拒尝试零编号、零登记、零记录；扫描在应答被记录前零写入且相同输入重复扫描逐字段一致？[Completeness, Measurability, Req §A-24, Req §FR-013, Req §FR-014, Req §FR-037, C-110, C-206, C-501, C-502, C-507, SC-010]

## 六、批次完备性与拒绝

- [ ] CHK026 - **完备性断言的封闭清单要件**是否齐备——参照物（本次扫描）、比较单元（逐候选处置分类）、允许差集恒为空、记账恒等式「候选 = 呈现行来源 + 合并引用 + 具名排除」、逐来源计数与判定入批次记录头；「一次调用产出一次呈现、顺序确定（来源清单 → 载体路径 → 块出现序）」是否同一套要求内表述，且以指针抵达 `closed-set-claims.md` 而非复述其判据表？[Completeness, Measurability, Req §FR-014, Req §FR-015, Req §A-8, C-201, C-601, C-602, SC-001]
- [ ] CHK027 - **记账恒等式的项语义**是否唯一可判——「呈现行来源」数的是行还是来源引用、「合并引用」计入被并掉的 register 行还是第二种引用、「具名排除」是否包含缺席来源；一个身份合并三来源时恒等式两侧能否按任意夹具唯一算平（否则完备性断言不可复算）？[Ambiguity, Measurability, Req §FR-009, Req §FR-015, C-104, C-602, SC-001]
- [ ] CHK028 - **载体级拒绝与块级缺陷的分界**是否在每处一致——只有文件 I/O 失败、register 表结构无法按列解析、候选无法枚举才拒绝整批；未知/重复/畸形字段与声明计数不符是块级 `incomplete`；扫描根中**单个**文件不可读时是「来源不可枚举」拒绝还是该文件的候选单独失败（需求的粒度未写明）；围栏代码块内的块不计是否与 107 围栏规则同源？[Consistency, Edge Case, Req §A-21, Req §FR-008, Req §FR-016, C-102, C-103, C-109, C-603]
- [ ] CHK029 - **缺席与空集**的语义是否分离——缺席来源（文件/目录不存在）记带原因的空来源、不拒绝、不得读成「干净」，完备性判定如实标注；零候选 → `nothing-pending` 成功且不建批次记录；「零候选」是否包含全部候选被排除的情形，`nothing-pending` 输出是否必须携带缺席披露（否则与 FR-017 的「不得读成干净」冲突），部分完备是否只能以拒绝收场？[Consistency, Clarity, Req §FR-016, Req §FR-017, Req §FR-018, C-604, C-605, C-607, SC-001]

## 七、人工 / `ai-autonomous` 边界

- [ ] CHK030 - **类别门**的三条分支是否互斥且穷尽——已声明 `ai-autonomous` → `not-human-held` 排除（永不呈现 / 转换 / 结案）；类别未知（无块、路径不可解析、缺字段、值域外）→ `incomplete` 并点名 `class-missing`；同一身份多来源类别冲突 → 从严 `not-human-held` 并具名披露；三者的记账归属是否与 §Batch States 闭集一致，「未知 ≠ 自主」的裁定在 FR-011 与 A-23 是否同文？[Completeness, Consistency, Req §FR-011, Req §A-13, Req §A-23, C-106, C-207, SC-007]
- [ ] CHK031 - **自主决策的路径保持**是否写成禁止性闭合——批次不得呈现、转换或授权 `ai-autonomous`；人类默认不得流入自主记录；无人值守不得把无人应答读作沉默；这些禁令是否各有可判定的承接面（呈现计数为零、记账排除、具名拒绝）而非仅原则陈述？[Coverage, Measurability, Req §FR-040, Req §FR-041, C-207, C-512, SC-007]
- [ ] CHK032 - **人类选择信号与类别的联动**是否唯一——只有人持有的处置产生既有门控观察信号，`objected-parked` 无信号；信号词表以指针抵达既有 owner；类别不明项不产生任何信号或记录；需求是否说明「信号归属」属于哪一面（批次记录、门控观察还是两者）？[Ambiguity, Consistency, Req §FR-030, Req §A-13, C-408]

## 八、可读性与行为边界

- [ ] CHK033 - **批次呈现的完整性下限**是否齐备——批次级五问（为何此刻出现、沉默意味着什么、如何异议 / 暂缓、哪些项保持待定及原因、完备性披露含缺席来源）与「长批次不设上限、不截断、不以摘要替代项」是否同文，且「读者无需打开其他工件」是否在需求文本内表达（而非只出现在契约或 SC 中）？[Completeness, Req §FR-020, Req §FR-025, C-203, C-205, SC-008]
- [ ] CHK034 - **面向用户正文的内部标识符边界**是否可判定——FR-020 禁止字段名 / 脚本名 / 状态码进入正文，而 FR-019 要求每项携带来源指针、接地指针、资格状态与原因；哪些属于「结构化载荷」、哪些进入正文、路径是否算内部标识符、状态（如 `incomplete`）在正文中如何用平实语言表达，是否有单一裁定？[Ambiguity, Conflict, Req §FR-019, Req §FR-020, C-202, C-204, SC-008]
- [ ] CHK035 - **机器 / 行为边界**是否诚实且承接面具名——机器只判结构命题（在场、文法、闭集、计数、成员、指针可解析）；建议合理性、后果真实性、名称完整性、理由充分性归既有评审面；需求是否点名承接面并禁止任何文档或测试声称机器覆盖？[Consistency, Coverage, Req §FR-045, Req §A-8, C-208, C-512, SC-008]

## 九、重决规则

- [ ] CHK036 - **重决与取代**是否与既有记录的写入规则相容——旧记录追加 `superseded_by` 且「内容零改写」；批次产生的决策记录位于**永不覆盖**的批次记录之内时两者是否冲突（追加即视作改写批次记录，不追加则取代链断裂）；旧载体不可写即拒绝重决的规则在这种载体上是否等于「永不重决」？[Conflict, Req §FR-029, Req §FR-037, Req §A-7, C-502, C-503, C-510, SC-006]
- [ ] CHK037 - **重决的呈现与登记投影**是否完整——`prior-decision-conflict` 呈现必须给旧记录指针与所选选项；用户显式改选后新记录、旧记录 `superseded_by`、旧内容零改写三件套；register 与来源状态在新旧记录之间如何反映（旧行状态是否保持已决、新决策编号如何追加）是否写明，冲突未处理时批次收尾逐项说明是否可判？[Gap, Completeness, Req §FR-023, Req §FR-029, Req §FR-034, C-306, C-510, SC-006]

## 十、可追溯性、依赖与前提

- [ ] CHK038 - 每个 FR（45/45）与每个 SC（10/10）是否至少被一个用户故事场景、独立测试或验收读数覆盖，`final` / `supporting` 路径分类是否完整（SC-001…SC-007、SC-010 为 final，SC-008 / SC-009 为 supporting），每个 `[[STR-NNN]]` 引用是否解析到 Shared Strings 行，每个 SC 是否点名测量来源与二值/阈值判据？[Traceability, Measurability, Req §FR-001…FR-045, Req §SC-001…SC-010, Req §Shared Strings, Req §Measurement Sources]
- [ ] CHK039 - **Runtime Stack** 的八行是否每行具备 owner / pin / contract / joint acceptance，`Form` 取值落在闭集，`FR` 与 `Premises` 单元格可解析，「零新增第三方依赖」可机械判定；记忆引擎（RS-004）与决策检查器（RS-005）作为签名契约的边界是否与 FR-032 / FR-033 / FR-044 的义务一致？[Dependency, Completeness, Req §Runtime Stack & Dependency Ownership, Req §FR-032, Req §FR-033, Req §FR-044, C-504, C-511]
- [ ] CHK040 - **假设与裁定**是否可追溯且无第二定义点——A-1…A-25 是否覆盖 brief 的全部歧义并各有理由；clarify 的五条裁决（A-21…A-25）是否与被修订的正文（FR-008 / FR-010 / FR-011 / FR-027 / FR-037 / FR-040）同文；承重决策「沉默语义」是否按 `decision-tension.md` 六字段记录并给出反指标与重开条件？[Assumption, Completeness, Req §A-1…A-25, Req §A-10, Req §Clarifications, Req §FR-027, SC-004]

## Notes

- **勾选与判读**：`[x]` 表示该问题已依据需求文本（或点名的 owner 行 / 契约条款 / plan 前提）得到回答；答「否」即对 `requirements.md` 的 finding，不是一条实现任务。本阶段交付的是清单器械；逐条作答属于 analyze / review 的判定职责。
- **计数（footer）**：共 **40 条**，CHK001…CHK040；**40/40（100%）** 携带至少一个追溯锚（`[Req §…]` / `C-NNN` / `SC-NNN` / `[Gap]` / `[Ambiguity]` 等），满足 ≥80% 下限；soft cap 40 未超出；CHK 编号唯一且顺序连续；无 `Verify` / `Test` / `Confirm` / `Check` 开头的实现检验式条目；无仅能靠运行产品回答的条目。
- **维度计数（按每条的主维度，程序读数）**：Completeness **13**（CHK005 / 007 / 008 / 009 / 015 / 016 / 017 / 020 / 024 / 025 / 026 / 030 / 033）、Ambiguity **8**（CHK002 / 003 / 011 / 014 / 022 / 027 / 032 / 034）、Consistency **6**（CHK018 / 019 / 021 / 028 / 029 / 035）、Gap **4**（CHK006 / 013 / 023 / 037）、Conflict **3**（CHK004 / 012 / 036）、Clarity **2**（CHK001 / 010）、Coverage **1**（CHK031）、Traceability **1**（CHK038）、Dependency **1**（CHK039）、Assumption **1**（CHK040）＝ **40**；次级标签另覆盖 Measurability（CHK011 / 022 / 025 / 026 / 031）、Edge Case（CHK012 / 016 / 028）、Non-Functional（CHK008）——taxonomy 九维全部出现。逐条归属见 `../test-evidence/checklist-selfcheck.txt`。
- **章节计数**：一 5（CHK001–CHK005）/ 二 3（CHK006–CHK008）/ 三 5（CHK009–CHK013）/ 四 6（CHK014–CHK019）/ 五 6（CHK020–CHK025）/ 六 4（CHK026–CHK029）/ 七 3（CHK030–CHK032）/ 八 3（CHK033–CHK035）/ 九 2（CHK036–CHK037）/ 十 3（CHK038–CHK040）＝ **40**。
- **覆盖矩阵（FR）**：**45/45**——FR-001 CHK008,038；FR-002 CHK008；FR-003 CHK008；FR-004 CHK008,020；FR-005 CHK008；FR-006 CHK001；FR-007 CHK005；FR-008 CHK028,040；FR-009 CHK003,027；FR-010 CHK002,004,040；FR-011 CHK004,030,040；FR-012 CHK005,022,023；FR-013 CHK025；FR-014 CHK025,026；FR-015 CHK026,027；FR-016 CHK005,028,029；FR-017 CHK029；FR-018 CHK029；FR-019 CHK034；FR-020 CHK033,034；FR-021 CHK009；FR-022 CHK010,011,012；FR-023 CHK013,037；FR-024 CHK009,013,015；FR-025 CHK033；FR-026 CHK016；FR-027 CHK014,015,040；FR-028 CHK017,019；FR-029 CHK036,037；FR-030 CHK017,019,032；FR-031 CHK015；FR-032 CHK020,021,039；FR-033 CHK021,039；FR-034 CHK017,022,037；FR-035 CHK023；FR-036 CHK024；FR-037 CHK020,025,036,040；FR-038 CHK021；FR-039 CHK006,007,010；FR-040 CHK006,018,031,040；FR-041 CHK031；FR-042 CHK007；FR-043 CHK007；FR-044 CHK039；FR-045 CHK035,038。
- **覆盖矩阵（SC）**：**10/10**——SC-001 CHK001,005,026,027,029,038；SC-002 CHK009；SC-003 CHK010,011,012；SC-004 CHK014,015,016,017,040；SC-005 CHK020,021,022,023,024；SC-006 CHK013,036,037；SC-007 CHK018,030,031,038；SC-008 CHK033,034,035,038；SC-009 CHK007,038；SC-010 CHK025,038。
- **覆盖矩阵（契约条款）**：**54/54**——source-roster C-101 CHK001；C-102 CHK028；C-103 CHK028；C-104 CHK003,027；C-105 CHK002,004；C-106 CHK004,030；C-107 CHK005；C-108 CHK005；C-109 CHK028；C-110 CHK025；presentation C-201 CHK026；C-202 CHK034；C-203 CHK033；C-204 CHK034；C-205 CHK033；C-206 CHK025；C-207 CHK030,031；C-208 CHK035；default-derivation C-301 CHK009；C-302 CHK009；C-303 CHK010；C-304 CHK011；C-305 CHK012；C-306 CHK013,037；C-307 CHK010；objection-reply C-401 CHK014；C-402 CHK014；C-403 CHK016；C-404 CHK015；C-405 CHK017,019；C-406 CHK006,018；C-407 CHK016；C-408 CHK017,019,032；C-409 CHK015；record-replay C-501 CHK025；C-502 CHK025,036；C-503 CHK020,036；C-504 CHK021,039；C-505 CHK022；C-506 CHK023；C-507 CHK025；C-508 CHK024；C-509 CHK021；C-510 CHK036,037；C-511 CHK007,008,039；C-512 CHK008,031,035；completeness-refusal C-601 CHK026；C-602 CHK026,027；C-603 CHK028；C-604 CHK029；C-605 CHK029；C-606 CHK005；C-607 CHK029；C-608 CHK006,007。
- **机械读数（2026-11-27，本阶段当场取证）**：`validate-requirements.py` → `status: ok`，**437 行 / 55 definition rows / 15 shared strings / 0 error / 0 warning**（`../test-evidence/checklist-requirements-validator.txt`）；程序计数（`../test-evidence/checklist-spec-readings.txt`）：45 FR / 10 SC / 15 STR（正文引用 15/15 解析、0 未解析）/ 25 A / 5 US / 24 Edge Cases / 8 RS / 2 Clarifications 会话（16 条 `- Q:` 行；plan/tasks/feature-ref 头部的「13 clarification rows」为陈旧读数，本清单以正文实测 16 为准）；`contracts/` 6 文件 54 条款（10 + 8 + 7 + 9 + 12 + 8）；`plan.md` 23 宪法行 / PA1–PA6 / EP-001…EP-007；`data-model.md` 13 实体 / 22 不变量 / 5 状态域；`quickstart.md` 7 场景；`tasks.md` 58 任务行 / 11 个 `[P]` / 5 个验证行承载 54 条 `[green:]` 认领（60 次 `[green:` 记号含 Format 与 Notes 的说明文本）；register 谓词派生的 open 待决策行为 **17** 条；四个扫描根中 `### PENDING —` 块为 **0**（首轮真实批次呈现 17 行 `incomplete`、零项可结案，A-16/EP-007 fallback）。
- **清单自检**：`../test-evidence/checklist-selfcheck.txt` 记录本文件的程序读数（条目数、追溯锚覆盖、FR/SC/条款覆盖、禁用开头、编号连续性、主维度直方图与逐条归属）。
- **same-author 检测门**：不成立（见 Detection path）；未派发 fresh-context 检测代理（角色模板与派发均明令不得再派发），检测路径如实记录，不以委托路径冒充直接读。
- **新增而非覆盖**：本文件为 checklist 阶段**新增**清单；requirements 阶段产出的 `checklists/requirements.md` 保持原样（未被覆盖、未刷新）。同轮不生成 recheck 文件（本阶段无「回答早前条目」的动作）。
- **待下游裁定的观察（不阻塞本阶段）**：本清单的 `[Gap]` / `[Ambiguity]` / `[Conflict]` 条目指出的候选确认点——去强调与 tracked 定义（CHK001）、register 路径单元格（CHK002）、同名族定位比较（CHK003）、`class-missing` vs `authority-unresolved` 原因冲突（CHK004）、调用方与授权值域（CHK006）、`grounded` 可解析的锚点语义（CHK011）、`no-evidence` 与 `incomplete` 的关系（CHK012）、多条既往记录/旧载体不可读时的冲突判定（CHK013）、应答口径的封闭性（CHK014）、register 状态单元格文法（CHK022）、失败披露的留痕载体（CHK023）、记账恒等式的项语义（CHK027）、信号归属面（CHK032）、正文内部标识符边界（CHK034）、**重决与批次记录 create-only 的冲突（CHK036）**、重决的 register 投影（CHK037）——由 `/speckit.analyze` 或实现阶段按判据取证，不在本阶段预先裁定。
- **Feature 状态**：本轮位于 `/speckit.implement` 之前，按 Feature Integration Protocol，checklist 不发起 `Implemented → Ready for Review` 迁移，仅产出清单；`.specify/features.md` 行 112 维持 `Planned`。
- **PLAN-EDIT**：无。本文件位于 `checklists/`；`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md` / `requirements.md` / `tasks.md` 未被触碰，故无 `PLAN-EDIT:` 声明。
- **Workspace guard**：撰写前快照 `../test-evidence/workspace-checklist.json`（对 tasks 阶段签名 `workspace-tasks.json` 复核 `clean`，rc 0）；收尾复核见 `../test-evidence/workspace-checklist-readings.txt`。