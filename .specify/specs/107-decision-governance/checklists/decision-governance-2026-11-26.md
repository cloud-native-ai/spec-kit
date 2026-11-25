# Requirements-Quality Checklist: Decision Governance — 决策项的文本、选项、归档、传递与两类强调

**Purpose**: 检验 Feature 107 需求文本（`requirements.md`）的**写作质量**——决策项文本与选项集是否按类规定到可判定、封闭决策生产者清单与既有载体归档投影是否闭合到可重建、superagent→subagent 的决策块/确认/实施回执是否把结果钉回 `decision_id`、两类决策的强调与 M/B 强制边界是否诚实分离、迁移与旧记录保全是否闭包、以及每条需求与成功标准是否可追溯到条款与证据。每条都是对需求文本（或它点名的 owner 行 / 条款行）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-26
**Feature (Requirement Scope)**: Feature 107 Decision Governance（AI Agent 决策项治理）— `.specify/features.md` 行 107（详情 `.specify/features/107-decision-governance.md`），状态 `Planned`。本清单位于 `/speckit.implement` 之前，按 Feature Integration Protocol 不发起 `Implemented → Ready for Review` 迁移，也不代评 code-segment 结论。
**Requirements (What)**: [../requirements.md](../requirements.md) — 本轮机械读数（2026-11-25T16:04Z @ `a954f64a3`；`validate-requirements.py` 逐字输出见 `../test-evidence/checklist-requirements-validator.txt`）：`status: ok`，**0 error / 0 warning**，**394 行 / 40 definition rows / 9 shared strings**；实测 **30 FR**（FR-001…FR-030）、**10 SC**（SC-001…SC-010；final 7 / supporting 3）、**9 Shared Strings**（STR-001…STR-009）、**14 条假设裁定**（A-1…A-14）、**6 个用户故事**、**12 行封闭 Decision Producer Inventory**（P-01…P-12）、**9 条 M 规则 / 6 条 B 规则**（analyze 修复 2026-11-26 由 8 条扩为 9 条：新增 M-09 evidence 指针可解析）、**11 条 Edge Cases**。全部计数读数见 `../test-evidence/checklist-spec-readings.txt`。
**Specifications (How, context only)**: [../plan.md](../plan.md)（**6 行**封闭 § Backward-Incompatible Change Inventory，BC-01…BC-06；T-001…T-003 张力；EP-001…EP-007）、[../tasks.md](../tasks.md)（**56** 任务行）、[../contracts/](../contracts/)（**38 条款**：C-101…C-109 / C-201…C-208 / C-301…C-308 / C-401…C-407 / C-501…C-506）、[../data-model.md](../data-model.md)（E1…E9 / I-01…I-14）——**只**用于暴露需求的缺口、歧义与冲突，从不替 plan/tasks 自身打分。
**Readers**: 需要判定「107 的需求是否足以从 checklist 放行进 analyze / implement」的复核者——`/speckit.analyze` 的检测者、`/speckit.implement` 的协调者与后续接手本线的编写者；他们依据本清单、被引用的需求行与 `test-evidence/` 的机读读数取结论。
**Reading scenario**: 复核者打开本文件，决定三件事：(1) 哪几条需求缺陷必须在 analyze / implement 之前修掉；(2) 哪些项可登记为「已裁定、由下游承载」而放行；(3) 哪些项因判据依赖尚未落地的机制（owner page、`validate-decisions.py`）而保持 `not_evaluated`。按条末的 `[Req §…]` / 条款 ID / `plan §…` 锚回到正文逐字核对。
**Focus / Depth / Audience**: Focus = 阶段简报的八组聚焦簇（决策文本与选项的按类规范 / 归档与审计 / superagent→subagent 传递与实施 / 两类决策的强调与检查 / M/B 强制边界 / 迁移与兼容 / 行为保持 / 可追溯性）；Depth = **Deep**（简报把八组簇写成必覆盖集并要求每个 FR 与 SC 至少被覆盖一次，默认 Standard 不足以承载）；Audience = **Reviewer**。阶段简报已使意图明确，技能 §2 的三个意图澄清问题按「已预答」跳过，默认值与升深理由记录于此。
**Detection path**: same-author 条件**不成立**——`requirements.md` 与 plan/tasks 由本线先前阶段的独立执行体撰写，本执行体未撰写所分析的任何制品，也未继承其会话；按 `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 的「作者不同 / 先于本会话」分支，门不触发，未派发 fresh-context 检测代理（本派发亦明令不得再派发）。缺口扫描由本执行体直接完成；可机械核对的前提（FR / SC / STR / P / M / B / BC / 条款 / 任务计数）均以程序读数当场取证，读数见 Notes 与 `../test-evidence/checklist-spec-readings.txt`。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成，方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`，结构模板为 `.specify/templates/checklist-template.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner 行 / 条款行）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，不是一条实现任务。判据落在下游文档（owner page、数据模型、检查器）时登记为**观察**；判据依赖尚未落地的机制时登记为 `not_evaluated`。

## 一、决策项文本与两类强调

- [ ] CHK001 - 需求是否强制每个决策项声明**恰一个** `decision_class`，值域闭集为 `human-interactive` / `ai-autonomous`，类缺失、类混合、值域外均为缺陷，且类决定适用的模板与检查集？[Completeness, Req §FR-006, Req §FR-011, C-101, SC-003]
- [ ] CHK002 - 两条生产规则（完整名称；同名冲突时的完整定位）是否被写成**最低门槛**并点名四个落地点（所有者页、instruction 段、决策项模板、守卫/评审面），而不是 instruction 模板一处修改？[Completeness, Req §A-8, Req §FR-007, Req §FR-010, C-102, SC-002, SC-010]
- [ ] CHK003 - 完整名称规则的**适用范围**是否被钉死——它约束决策主体与全部选项标签，还是也覆盖后果/上下文/理由散文——且机器守卫的扫描面（M-08 只判"结构化决策主体"）与该范围一致，未登记简称明确留给 B-01？[Clarity, Req §FR-007, Req §FR-022 (M-08), C-102, Req §Enforcement Boundary B-01]
- [ ] CHK004 - 同名定位是否量化到可判定下限（具名维度不少于两个：业务资源组 + region id），机器能判部分（在场/维度数，M-02）与充分性判定（B-02）是否分离，且"同名冲突实际存在却声明 `same_name_conflict: false`"这一 Edge Case 是否被指派到具名裁定面而不是无承接的缺陷声明？[Measurability, Req §FR-007, Req §Edge Cases, C-103, Req §Enforcement Boundary M-02 / B-02]
- [ ] CHK005 - `human-interactive` 决策项的呈现要素是否逐项枚举（平实语言的问题、上下文、每个选项的后果与可逆性、默认项、完整名称与定位），措辞/上下文规则以指针抵达 `user-facing-comprehension.md`，真实性检查指派给 B-03？[Completeness, Req §FR-008, Req §FR-011, C-104, SC-003]
- [ ] CHK006 - `ai-autonomous` 决策项的呈现要素是否逐项枚举（封闭选项集、明确决策谓词/规则、显式假设、可机器核查的证据指针、确定性结论、重开条件），只有散文而无判定规则是否被声明为 B-04 上的缺陷？[Completeness, Req §FR-009, Req §FR-011, C-105, SC-003]
- [ ] CHK007 - 呈现与类别不符是否干净地拆到 B-03 / B-04 / B-06 三面且均不声称机器覆盖，同时无人值守运行中的 `human-interactive` blocked 姿态（现仅见 Edge Cases：保持类别、报 `blocked`、停等）是否在某个功能需求中有锚点而不是只活在边角情形？[Coverage, Gap, Req §FR-011, Req §Edge Cases, C-109, Req §Enforcement Boundary B-06, SC-003]

## 二、选项集与选中项

- [ ] CHK008 - 每个退化选项形态是否各有预期结局——空集（不构成决策项）、重复标签、`other` 无 `path`、单可行选项未声明 `forced` + 理由、零可行选项——且全部落在 M-03 的机器判定范围内？[Edge Cases, Req §FR-012, C-106, Req §Enforcement Boundary M-03, SC-004]
- [ ] CHK009 - 五要素选项契约（label、consequences、reversibility、default 标记、evidence）是否完整，`default` 的基数是否被量化（恰一个 / 至多一个 / 哪些情形允许零个），`other.path` 是否给出"谁、何时、如何新增选项并回写记录"的 owner？[Clarity, Req §FR-012, C-106]
- [ ] CHK010 - 选中项的三条义务是否按类分置——所有决策的选中项须是选项集中的具名成员、`ai-autonomous` 须可由记录输入 + 谓词确定性重放、`human-interactive` 须记录人的选择信号（信号词汇以指针抵达既有门控观察协议、不复述）？[Consistency, Req §FR-013, C-107, C-108, SC-004]
- [ ] CHK011 - 文本/选项规则引入的辅助声明——单选项的 `forced` 标记、`other` 选项的 `path`、人的选择信号——是否在分层封闭记录文法（FR-014 基础层十字段 + 条件层三族）中有被声明的落位（作为 `options` / `chosen option` 的值形状成员，还是顶格字段），从而字段闭包不留无处安放的声明？[Conflict, Req §FR-012, Req §FR-013, Req §FR-014, C-201, C-202]

## 三、归档、审计与单一所有者

- [ ] CHK012 - 需求是否声明单一所有者页 [[STR-001]] 并列出它拥有的全部面（词汇闭集、按类强调、选项契约、记录字段闭包、传递义务、M/B 边界、字段→所有者映射），同时禁止其他面复述其判据表（指针形）？[Completeness, Req §FR-001, Req §FR-002, Req §A-2]
- [ ] CHK013 - "一个决策项完成时恰产生一条记录、落在其生产者的既有载体"是否与投影安全义务成对——不新建第二套登记/队列/存储/调度器、无载体的生产者走清单修订（不得静默丢弃）、只读命令的处置只进自己的报告、并行分支按载体逐文件/逐条目写入且 register 为手工唯一写入者（冲突按 renumber 修复）？[Completeness, Non-Functional, Req §FR-014, Req §FR-004, Req §A-3, Req §Edge Cases, C-207, C-208]
- [ ] CHK014 - 记录字段闭包是否分层权威（FR-014 基础层十字段 + 条件层三族），每个条件族的触发条件是否精确（同名族在 C-103 触发条件成立时；`superseded_by` 在被取代时；传递族时点按 `transmission_status` 相位追加），非传递记录只带 `created_at`、无占位字面量的义务是否写明？[Completeness, Req §FR-014, C-202, SC-005, data-model.md E2]
- [ ] CHK015 - 字段→所有者表是否给每个记录字段**恰一个**定义所有者，且 clarify 裁定（implementation status 是 `transmission_status` 状态面的实施结果维度、不是第 11 个记录字段）是否在 FR-014、FR-019 与字段表三处一致？[Consistency, Req §FR-002, Req §FR-014, Req §Decision Record Field Ownership, Req §Clarifications]
- [ ] CHK016 - 编号可判定性是否从头到尾写清——`D-NNN` 三位形态、按载体密集且唯一、不复用、诞生时登记、跨载体重复的语义（同一决策的两次投影，还是两个决策允许撞号）、密度计算的"载体"单位、以及"载体 + 区间"分组 register 行在 M-04 下如何保持可解析？[Ambiguity, Consistency, Req §FR-015, Req §A-6, Req §Edge Cases, C-203, Req §Enforcement Boundary M-04]
- [ ] CHK017 - 可重建性是否定义到可测量——要重建的字段全集、指针解析基准与允许的指针形态、evidence 指针全部可解析、不得以对话记忆补足——并且给定 A-9 把"引用可解析"划入机器可判集、FR-016 把不可解析指针定为缺陷，封闭 M 表（M-01…M-09）由 M-09 承接指针可解析性（只判解析、不判充分性）？[Measurability, Gap, Req §FR-016, Req §FR-022, Req §A-9, Req §Enforcement Boundary, C-204, SC-005]
- [ ] CHK018 - 承重决策是否被写成"只交叉引用"——记录引用对应 `T-NNN`、六个张力字段不复制——且六字段以所有者指针抵达而不是在决策契约里成为第二定义点？[Consistency, Req §FR-017, C-205]

## 四、superagent→subagent 传递与实施

- [ ] CHK019 - 决策块五字段（`decision_id`、`decision_class`、选中项完整标签、实施约束、档案指针）是否规定为搭乘既有派发载荷，且七角色字段与四项既有注入保持不变、决策块不作第八个角色字段？[Completeness, Req §FR-018, Req §A-7, C-301, SC-006]
- [ ] CHK020 - 决策 backed 派发在**缺失决策块时**是否仍可被识别与拒绝（构造期声明的意图标记 vs 事后工件检查），且"无决策记录/编号不得派发""无法解析的 `decision_id` 不得实施"两条禁令是否各有具名判定面？[Ambiguity, Gap, Req §FR-018, Req §FR-020, C-302, C-305, Req §Enforcement Boundary M-06, SC-006]
- [ ] CHK021 - 回传的确认与 `implementation_receipt` 四字段（`decision_id`、实施摘要、证据指针、偏离声明 `none` / `diverged` + 理由）是否逐项要求，回执是否被规定更新记录的 `transmission_status` 实施结果维度？[Completeness, Req §FR-019, C-303, C-304, SC-006]
- [ ] CHK022 - 回传缺任一项时父侧不得消费或补齐，是否同时声明了既有**五要素上行**的要素数在此变更下保持不变（或明确扩展），而不是只保护下行七字段/四注入？[Conflict, Gap, Req §FR-019, Req §A-7, shared/definitions/superagent-definitions.md（指针）, SC-006]
- [ ] CHK023 - 子代理静默重决是否被禁止并以 fast-fail 上送收口，取代/推翻是否要求"保留原件 + 取代件、原件标 superseded 指向新编号、推翻本身也是一条决策记录"三件套同时成立？[Completeness, Req §FR-020, Req §Edge Cases, C-305, C-308, SC-006]
- [ ] CHK024 - 审计链三段（记录 → 派发尝试（角色边身份 / run report）→ 实施回执）是否规定为必须可解析，断链是否为显式可上报异常；多跳链"每跳载荷都带决策块、每跳回执引用同一 `decision_id`"是否锚定在功能需求而非仅 Edge Cases/条款？[Coverage, Req §FR-021, Req §Edge Cases, C-306, C-307, SC-006]

## 五、强制边界：M 规则、B 规则与行为保持

- [ ] CHK025 - 九条 M 规则是否逐条各配**恰一个**确定性判定器与一个转红条件，每条守卫有逆向样本，全部经唯一测试入口执行，且守卫清单与两张表逐行一致（表—守卫等价）？[Completeness, Req §FR-022, Req §FR-024, C-401, C-403, C-404, C-407, SC-007]
- [ ] CHK026 - 六条 B 规则是否逐条点名评审承接面（analyze / review 段 / 人工决策评审），文档与测试是否都不得声称其中任何一条被机器覆盖？[Coverage, Req §FR-023, C-402, SC-007]
- [ ] CHK027 - 机器/行为分野是否按 A-9 一致施加——每处"缺陷"措辞都有对应的 M 或 B 承接面——尤其 M-08 的"已登记 variant"是否与术语只做 `status=proposed` 提案的规则（FR-005 / A-11）相容（"已登记"是否包含未确认的提案条目）？[Consistency, Req §A-9, Req §FR-005, Req §FR-022 (M-08), Req §A-11]
- [ ] CHK028 - FR-025 的保全命题（哨兵字面量 / watcher verdict 与退出码 / 两槽测试预算）是否给出基线参照物（`fbab7a45c`，记录于 requirements-stage 证据）、比较单元（三个所有者产物全文逐字节）、默认空的允许差异集与补集断言（三路径 `git diff --quiet` rc 0、`--numstat` 零行），且"除非有记录在案的裁定"是否规定了裁定的记录位置与形态（FR-014 `D-NNN` 决策记录或阶段检查点中的具名裁决）？[Measurability, Req §FR-025, SC-007] — **pass**（2026-11-26 analyze 修复第三轮：五要件已逐项写入 FR-025 与 C-405）。
- [ ] CHK029 - 不新增阻塞式确认门控是否以可复算读数表达（`scan-confirmation-gates.py` 相对具名基线 `test-evidence/scan-confirmation-gates-baseline.txt` 的**零新增命中**），且与 FR-025 的哨兵 / watcher / 两槽预算三产物零漂移读数共同构成确认纪律的保持声明？[Measurability, Req §FR-025, C-405, SC-008] — **pass**（2026-11-26 analyze 修复第三轮：门控基线与三产物基线均已具名，SC-008 与 SC-008 Source 同步）。

## 六、落地、分发与客户接收

- [ ] CHK030 - instruction 新段是否规定为指针形（两条生产规则 + 每类一行强调 + 指向所有者页），声明段级字节上限 1,500 B 且判据含生成后实测增量，模板、活副本与每工具兼容副本逐字一致；新段计入的预算口径与总预算变更是否需要记录在案的裁定？[Completeness, Measurability, Req §FR-010, Req §FR-026, Req §A-13, SC-010]
- [ ] CHK031 - 镜像与每工具命令副本是否要求**同一变更内**再生成，并以可测口径表达——`regen-command-copies.py --check` rc 0、`sync-mirrors.py --check` 相对基线无新增漂移成员（绝对读数如实报告）、不得手改镜像面？[Measurability, Req §FR-027, C-506, SC-008]
- [ ] CHK032 - 框架文档与登记面是否要求以指针抵达所有者页（框架地图新行 + docs 一行），glossary 新词只以 `origin=auto`、`status=proposed` 留在 run 证据且未确认不写入，`Related Feature` 绑定状态按实际结果收口？[Completeness, Req §FR-030, Req §FR-005, Req §A-11]

## 七、迁移、兼容与旧记录保全

- [ ] CHK033 - 新契约是否只约束落地后创建的记录，旧形态记录是否被逐类枚举（一/两位 `D-` 标题、`D1–D9`/`D-A`/`D-B`/`D-001` 等 register 行）并规定"报告 `legacy`、可解析、不判无效、零改写"，且零改写的基线提交是否钉为单一不可替换的参照物（后续阶段能否改用另一个 base）？[Clarity, Measurability, Req §FR-028, Req §SC-009, C-206, C-502]
- [ ] CHK034 - 向后不兼容变更清单是否声明为封闭集 `{BC-01…BC-06}`，每行是否具备具名的迁移或确定性拒绝行为与钉住它的测试，是否有行仅靠运行时双路径回退或人工说明解决（应转红），且 `/speckit.migrate` 的维度集是否明确不扩宽？[Completeness, Req §FR-029, Req §SC-009, C-501, C-503, C-504, C-505]

## 八、决策生产者清单与类/义务词汇

- [ ] CHK035 - 封闭清单命题是否可判定——声明集（本规格 §Decision Producer Inventory）、观测集（实现期代码面扫描的具体路径与命令）、允许差异（显式 `exempt` 行）三者齐备，清单外生产者产出决策项即缺陷，扩展只能以修订清单/所有者页进行？[Completeness, Measurability, Req §FR-003, Req §SC-001, C-406]
- [ ] CHK036 - 每行生产者的义务与类别单元格是否能解析到封闭取值——`record` / `record-when-decision` / `exempt` 三值各自的判据是否齐全（`record-when-decision` 行是否都给出"何时算决策"的判据），`record（显式呈现的取舍）` 这类带限定的 `record` 是否应读作 `record-when-decision`，`通常 ai-autonomous` 与 `由持有者定` 是否是类列允许的取值？[Consistency, Clarity, Req §FR-003, Req §A-4, Req §Decision Producer Inventory P-03]
- [ ] CHK037 - P-09（superagent→subagent 传递决策）的类列是否随被传递决策记录的类别（A-4）——人已批准/选择的决策被交办实施仍为 `human-interactive`，父侧无人值守自主交办为 `ai-autonomous`——且传递与回执不生成第二条决策记录（FR-014、FR-018）？[Conflict, Req §A-4, Req §Decision Producer Inventory P-09, Req §FR-018]

## 九、可追溯性、可测量性与依赖

- [ ] CHK038 - 是否每个 FR（30/30）与每个 SC（10/10）至少被一处验收场景、独立测试或条款行覆盖，每条 `[[STR-NNN]]` 引用是否解析到 Shared Strings 行，每个 SC 是否点名测量来源与二值/阈值判据且 `final` / `supporting` 路径分类齐全？[Traceability, Measurability, Req §FR-001…FR-030, Req §SC-001…SC-010, Req §Shared Strings, Req §Measurement Sources]
- [ ] CHK039 - `execution` 类必填的六行 Runtime Stack 是否每行具备 owner / pin / contract / joint acceptance、`Form` 值落在闭集、`FR` 单元格可解析、`Premises` 以指针引用 plan 阶段的 `EP-NNN`（本阶段不定义），且"零新增第三方依赖"是否可被机械判定？[Dependency, Req §Runtime Stack & Dependency Ownership, Req §FR-022, Req §FR-024]

## Notes

- **勾选与判读**：`[x]` 表示该问题已依据需求文本（或点名的 owner 行 / 条款行）得到回答；答「否」即对 `requirements.md` 的 finding，不是一条实现任务。本阶段交付的是清单器械，逐条作答属于 analyze / review 的判定职责。
- **计数（footer）**：共 **39 条**，CHK001…CHK039；**39/39（100%）** 携带至少一个追溯锚（`[Req §…]` / `C-NNN` / `SC-NNN` / `[Gap]`），满足 ≥80% 下限；soft cap 40 未超出；无 `Verify` / `Test` / `Confirm` / `Check` 开头的实现检验式条目；无仅能靠运行产品回答的条目。
- **维度计数（footer，按每条的主维度）**：Completeness **15**（CHK001/002/005/006/012/013/014/019/021/023/025/030/032/034/035）；Clarity **3**（CHK003/009/033）；Measurability **5**（CHK004/017/028/029/031）；Consistency **5**（CHK010/015/018/027/036）；Coverage **3**（CHK007/024/026）；Edge Cases **1**（CHK008）；Conflict **3**（CHK011/022/037）；Ambiguity **2**（CHK016/020）；Traceability **1**（CHK038）；Dependency **1**（CHK039）。合计 39。
- **章节计数**：一 7 / 二 4 / 三 7 / 四 6 / 五 5 / 六 3 / 七 2 / 八 3 / 九 2 = 39。
- **覆盖矩阵（FR）**：FR-001 CHK012；FR-002 CHK012,015；FR-003 CHK035；FR-004 CHK013；FR-005 CHK027,032；FR-006 CHK001,036；FR-007 CHK002,003,004；FR-008 CHK005；FR-009 CHK006；FR-010 CHK002,030；FR-011 CHK007；FR-012 CHK008,009,011；FR-013 CHK010,011；FR-014 CHK011,013,014,015；FR-015 CHK016；FR-016 CHK017；FR-017 CHK018；FR-018 CHK019,020,037；FR-019 CHK021,022；FR-020 CHK020,023；FR-021 CHK024；FR-022 CHK003,017,025,027；FR-023 CHK026,027；FR-024 CHK025；FR-025 CHK028,029；FR-026 CHK030；FR-027 CHK031；FR-028 CHK033；FR-029 CHK034；FR-030 CHK032。**30/30** 覆盖。
- **覆盖矩阵（SC）**：SC-001 CHK035；SC-002 CHK002；SC-003 CHK001,005,006,007；SC-004 CHK008,010；SC-005 CHK014,017；SC-006 CHK019,020,021,022,023,024；SC-007 CHK025,026,029；SC-008 CHK029,030,031；SC-009 CHK033,034；SC-010 CHK002,030。**10/10** 覆盖。
- **覆盖矩阵（契约条款）**：C-101 CHK001；C-102 CHK002,003；C-103 CHK004；C-104 CHK005；C-105 CHK006；C-106 CHK008,009；C-107 CHK010；C-108 CHK010；C-109 CHK007；C-201 CHK011；C-202 CHK014；C-203 CHK016；C-204 CHK017；C-205 CHK018；C-206 CHK033；C-207 CHK013；C-208 CHK013；C-301 CHK019；C-302 CHK020；C-303 CHK021；C-304 CHK021；C-305 CHK020,023；C-306 CHK024；C-307 CHK024；C-308 CHK023；C-401 CHK025；C-402 CHK026；C-403 CHK025；C-404 CHK025；C-405 CHK029；C-406 CHK035；C-407 CHK025；C-501 CHK034；C-502 CHK033；C-503 CHK034；C-504 CHK020,034；C-505 CHK034；C-506 CHK031。**38/38** 条款被至少一条 CHK 引用。
- **新增而非覆盖**：本文件为 checklist 阶段**新增**清单；requirements 阶段产出的 `checklists/requirements.md` 保持原样（未被覆盖、未刷新）。同轮不生成 recheck 文件（本阶段无「回答早前条目」的动作）。
- **机械读数（2026-11-25T16:04Z @ `a954f64a3`）**：`validate-requirements.py` → `status: ok`，0 error / 0 warning，394 行 / 40 definition rows / 9 shared strings（逐字：`../test-evidence/checklist-requirements-validator.txt`）；requirements 实测 30 FR / 10 SC（final 7 / supporting 3）/ 9 STR / 14 A / 6 US / 12 P / 9 M（analyze 修复 2026-11-26 加入 M-09）/ 6 B / 11 Edge Cases；`plan.md` 实测 6 行 BC（BC-01…BC-06）；`tasks.md` 实测 56 任务行；`contracts/` 实测 5 份 / 38 条款（9+8+8+7+6）。全部命令与输出：`../test-evidence/checklist-spec-readings.txt`。
- **same-author 检测门**：不成立（见 Detection path）；未派发 fresh-context 检测代理（本派发明令不得再派发），检测路径如实记录，不以委托路径冒充直接读。
- **Feature 状态**：本轮位于 `/speckit.implement` 之前，按 Feature Integration Protocol，checklist 不发起 `Implemented → Ready for Review` 迁移，仅产出清单；`features.md` 行 107 维持 `Planned`。
- **PLAN-EDIT**：无。本阶段未改动任何 plan-owned 路径（plan.md / data-model.md / contracts/ / quickstart.md / research.md / feature-ref.md 均只读）。
