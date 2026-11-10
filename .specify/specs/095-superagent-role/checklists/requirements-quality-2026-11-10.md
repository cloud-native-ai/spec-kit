# Requirements-Quality Checklist: Super Agent Role（相对逻辑角色：定义、协议与 harness 落点）

**Purpose**: 检验 Feature 095 需求文本（`requirements.md`）的**写作质量**——相对角色与边谓词是否可判定、super↔sub 协议与九项身份转变注入是否闭合且按指针归属、并发 / 状态同步 / 状态跟踪 / 可视化四问是否只有一套既有机制、harness 落点与指令预算是否有可验证判据、080–094 观测附录是否拒绝「运行顺利即有效」。每条都是对需求文本（或它点名的 owner 行）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-10
**Feature (Requirement Scope)**: `.specify/features/095-superagent-role.md`（Feature 095，状态 Planned）
**Requirements (What)**: [../requirements.md](../requirements.md) — 本轮机械读数（2026-11-10）：287 行 / 53,696 B；**38 FR**（FR-001…FR-038）；**10 SC**（SC-001…SC-010；final 7 / supporting 3）；**6 Shared Strings**（STR-001…STR-006）；5 个用户故事；10 条 Edge Cases；16 条 Clarification Q（6 条 requirements 会话 + 10 条 clarify 会话）；15 条 Assumptions（A1–A15）。
**Specifications (How, context only)**: [../plan.md](../plan.md)（247 行 / 40,367 B；D-1…D-14；T-001 / T-002）、[../tasks.md](../tasks.md)（341 行 / 46,455 B；54 任务行）、[../data-model.md](../data-model.md)、[../contracts/](../contracts/) — **只**用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。
**Readers**: 需要判定「095 的需求是否足以从 checklist 放行进 analyze / implement」的复核者——`/speckit.analyze` 的检测者、`/speckit.implement` 的协调者，以及后续接手本线的编写者；他们不会重读 owner 文档或测试源码，只依据本清单、被引用的需求行与 `test-evidence/` 的机读读数取结论。
**Reading scenario**: 复核者打开本文件，要决定三件事：(1) 哪几条需求缺陷必须在 analyze / implement 之前修掉；(2) 哪些项可登记为「已裁定、由下游承载」而放行；(3) 哪些项因判据依赖尚未落地的机制而保持 `not_evaluated`。他们按条末的 `[Req §…]` 锚回到需求正文逐字核对。
**Focus / Depth / Audience**: Focus = 阶段简报的六个聚焦簇（定义可判定性 / 九项注入闭合与 owner 指针 / 协议归属与可观测面 / 四问唯一 owner 与零第二机制 / harness 落点与字节预算 / 收尾附录读数 / 术语与指针形态）；Depth = **Standard**（默认）；Audience = **Reviewer**（默认）。本轮 `$ARGUMENTS`（阶段简报）已使意图明确，技能 §2 的三个意图澄清问题按「已预答」跳过，默认值记录于此。
**Detection path**: same-author 条件**成立**——`requirements.md` / `plan.md` / `tasks.md` 由本轮无人值守 SDD 线内的前序阶段代理撰写，共享同一模型与同一套约定。缺口发现按 `.specify/shared/workflow/objective-analysis-gate.md` 派发 **3 路 fresh-context 只读检测代理**，作用域不相交：Detector A = FR-001…FR-021 + US1–US3 + 相关 Edge Cases；Detector B = FR-022…FR-037 + SC-004…SC-009 + plan/tasks 缺口检测；Detector C = SC-001…SC-010 + Measurement Sources + Shared Strings + Clarifications + Assumptions + FR-038。三路共输出 **35 行**检测结果；逐行按门禁规则 4（映射表即断言）复核后：**1 行经实测反驳**（A10 声称 US2 场景一缺 (c)——原文九项齐全，删除该行）、**1 条验证注记经程序复核纠正**（STR-004 的 `Consumed by` 与正文并不一致，见 CHK036）、其余按同一判据合并为 **29 个追溯条目**（3 组为双检测器重叠合并），另由编排者按简报六个聚焦簇补 **10 个结构条目**（含 CHK039 自检），共 **39 条**。同一轮未另设验证波次（本技能只定义一次检测）；**拒绝率 1/35 = 2.9%**；本技能无严重度分级，追溯锚是其局部等价物，故无「降级」计数。程序优先读数（计数、Shared Strings 引用 / `Consumed by` 双向、预算字节、切片集）见 `../test-evidence/checklist-readings-2026-11-10.txt`。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成，方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`，结构模板为 `.specify/templates/checklist-template.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner 行）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，不是一条实现任务。判据落在需求之外（下游文档 / 工具）时登记为**观察**；判据依赖尚未落地的机制时登记为 `not_evaluated`。

## 一、定义、角色集与判定面

- [ ] CHK001 - 分类「只由边决定」的排除输入（执行体类型、模型、工具列表、提示词措辞、个人描述）是否已逐项列举，且每一项都能在既有运行记录上判定？[Completeness, Measurability, Req §FR-001, Req §FR-002]
- [ ] CHK002 - 角色集的机读形态是否唯一——是 `{superagent, subagent}` 集合加 `dual-role` 组合标记，还是 Key Entities 所列的 `superagent / subagent / dual-role` 三个并列取值？[Ambiguity, Consistency, Req §FR-002, Req §Key Entities, Req §SC-001]
- [ ] CHK003 - 违例集合是否已闭合且各处一致——FR-005 列四类（含「深度越界」），US1 与 SC-001 只判三类；「深度越界」在角色深度无上限的前提下如何定义、由哪条 SC 覆盖？[Conflict, Coverage, Req §FR-004, Req §FR-005, Req §SC-001]
- [ ] CHK004 - 「无对应边的角色声明」违例的比较对象是否已具名——superagent 声明由哪一份既有记录承载，使「没有对应边」可以被判定而不是按提示词采信？[Gap, Req §FR-005, Req §Edge Cases]
- [ ] CHK005 - 只读判定面的输入范围是否已定义——读取哪些既有记录、如何界定一棵执行树（单一根？多根？跨 run 的无关记录如何隔离），使「一条边」与「深度」有确定的图边界？[Ambiguity, Req §FR-005]
- [ ] CHK006 - 多载体冲突的结果是否进入判定面的输出契约——FR-003 要求报 conflict 并点名两处路径，但 FR-005 的输出清单只有四类违例；conflict 是独立输出并计入非零退出，还是归入某一类？[Consistency, Req §FR-003, Req §FR-005]
- [ ] CHK007 - 根执行体身份的取值优先级是否已声明——「状态脊 `run_id` 或 line registry `line_id`」在两者同时存在时取哪个，或已明确委托给 plan？[Ambiguity, Traceability, Req §FR-003, Req §A11]
- [ ] CHK008 - 派发尝试标识是否解析到具体的既有标识符（如 `parent` 与 `label` 那样），使「重试 = 新尝试」与「stale attempt 不消费」有可核对的字段？[Gap, Req §FR-003, Req §FR-013]

## 二、super↔sub 协议与身份转变注入

- [ ] CHK009 - 下行载荷的每个角色字段是否都能在既有记录或既有 owner 上被观测（父身份、子 label、角色声明、深度位置、授权依据引用、结果契约、回传通道），且「角色声明」被写明只是声明、不构成角色判定？[Completeness, Consistency, Req §FR-008, Req §FR-002]
- [ ] CHK010 - 九项注入的每一项是否都指向具名的既有 owner 路径与章节——(d) 的 slot / reserve 事实、(e) 的 reporter 义务、(g) 的注意力分类在 FR-017 中是否给出了与 (f) / (h) 同等的可解析指针？[Gap, Req §FR-017]
- [ ] CHK011 - 九项清单的量化约束是否自洽——「MUST 至少包含」与「九项即封闭清单」在同一条 FR 内并用，允许增项还是禁止增项？[Conflict, Req §FR-017]
- [ ] CHK012 - 逐项缺失是否真的可被阻断——FR-018 只声明按 `[[STR-003]]` 子串判定，而 SC-002 要求「删去任一项时派发前自检阻断」；九项是否各有可匹配的机读句柄？[Conflict, Measurability, Req §FR-018, Req §SC-002]
- [ ] CHK013 - 消息分类集是否闭合且 owner 具名——FR-010 的「封闭分类集」与「最少区分四类」并用，四类之外是否允许增类，单点声明 owner 是哪一份文档？[Ambiguity, Consistency, Req §FR-010]
- [ ] CHK014 - 四类消息是否各有既有载体——在 FR-016 禁止新增通道的前提下，`ack` 与 `attention-escalation` 沿哪条既有载荷 / 回传通道往返，还是某类没有载体？[Conflict, Gap, Req §FR-010, Req §FR-016]
- [ ] CHK015 - 边的终止状态词表是否落到既有载体——`completed / failed / cancelled` 中 `cancelled` 由哪一份既有记录承载并可被父读回？[Gap, Req §FR-015]
- [ ] CHK016 - 「既有」的引用是否指到 owner——FR-012 的停滞阈值与 slow / stalled 区分、FR-013 的 attribution 取值（`own / foreign / stale-run / unattributed / legacy`）是否给出 owner 路径而不是内联副本？[Gap, Traceability, Req §FR-012, Req §FR-013]
- [ ] CHK017 - 聚合回传的行形态是否已定义——FR-020 的「逐子归属 + 每子证据路径」与 FR-009 的五项必备字段如何组合，聚合记录是否可以按需下钻到子项证据？[Completeness, Consistency, Req §FR-009, Req §FR-020]
- [ ] CHK018 - 非 SDD 扇出的授权面是否被覆盖——FR-014 援引的 agent 能力键 / 席位策略 / team territory 是否能为第三个真实场景的 10 子项派发给出可解析的授权依据？[Ambiguity, Req §FR-007, Req §FR-014]

## 三、并发、状态同步与恢复

- [ ] CHK019 - 双重角色执行体的扇出归哪个既有并发类别与单元集——`concurrency-class.yaml` 是否已有适用于「team 成员再扇出」的类别，且该扇出与父自身运行计入同一容量口径？[Gap, Dependency, Req §FR-022, Req §FR-024]
- [ ] CHK020 - 串行降级的读数是否可判定——SC-004 的「读数三元组逐 grain 记录」中 grain 指哪一级单元，「MUST NOT 把降级写成 `effective` 的数字」禁止写入哪个字段？[Clarity, Measurability, Req §FR-023, Req §SC-004]
- [ ] CHK021 - 单写者边界是否落到具体载体——父记录「边 + 已收到返回」时写哪一份既有 per-entry 文件（run report 是单文件产物），且「下一个外部可见动作」是否为封闭集合（再派发 / 向上汇报 / 合并）？[Gap, Clarity, Req §FR-025]
- [ ] CHK022 - 三层事实与「同一次状态读取」是否相容——FR-026 要求宿主事件层（pid / heartbeat / liveness）参与派生，FR-029 又要求 digest 只做一次状态读取；哪几层必须被这一次读取覆盖？[Consistency, Req §FR-026, Req §FR-029]
- [ ] CHK023 - SC-005 的「第二来源」是否被定义——它是否就是 FR-026 禁止的对话记忆 / 子会话正文 / 进程扫描，结构断言的目标是否具名？[Measurability, Req §FR-026, Req §SC-005]
- [ ] CHK024 - `interrupted` 与 `attention` 是否是有 owner 的既有状态值——哪个词表 / 载体定义并承载这两个标记，使恢复输出可被契约测试比对？[Gap, Req §FR-027, Req §SC-005]
- [ ] CHK025 - resume 前的授权重验证是否可观测——哪一份记录能区分「已重验证的恢复」与「未验证的恢复」，它与派发拒绝记录是否同形？[Gap, Measurability, Req §FR-028, Req §SC-005]

## 四、状态跟踪与可视化

- [ ] CHK026 - digest 的「有界」指哪一级——是单条长度上限、整集 cap，还是两者并存；截断时的 `omitted` 在哪个集合上声明，扇出形状（父一行 + 逐子）是否可能被静默截掉？[Ambiguity, Clarity, Req §FR-029, Req §FR-031]
- [ ] CHK027 - 运行报告映射表与 digest 字段是否一致——FR-030 的 `label → 角色 → 工作区` 没有父身份列，FR-029 又要求每行显示父边身份；父身份从哪一列派生而不触发第二来源？[Consistency, Req §FR-029, Req §FR-030]

## 五、harness 落点与零第二机制

- [ ] CHK028 - owner 文档的内容清单是否闭合且可判——FR-032 的十项模型内容是否逐项可断言，「术语边界」是否点名要消歧的对象（agent execution / driver / orchestrator）？[Completeness, Clarity, Req §FR-032]
- [ ] CHK029 - 「MUST NOT 复制规则」是否有客观判据——对三处分类法的指针行与 instructions 指针段，什么形态算「指针」、什么算「复制」，能否由结构断言而非措辞判断？[Measurability, Req §FR-032, Req §FR-033, Req §SC-007]
- [ ] CHK030 - 「余量不足」的触发条件是否已定义——它是否就是生成器预算报告的 `over`（`size >= budget`）；A13 的 37,454 / 32,975 / 38,400 B 与 946 B 余量是否有可复现命令的日期化记录？[Clarity, Measurability, Req §FR-033, Req §A7, Req §A13]
- [ ] CHK031 - FR-034 的派发面接线是否有成功标准覆盖——run-agent 注入清单、team 载荷与 driver 阶段载荷的角色字段由哪条 SC 验证，SC-002 / SC-003 / SC-007 是否足以覆盖？[Coverage, Req §FR-034, Req §SC-002, Req §SC-003]
- [ ] CHK032 - 测试处置与执行口径是否可判——「全套契约测试」指 `contract` 标记、整个 `tests/` 还是具名模块清单，处置台账（改写 / 保持 / 移除）由哪条 SC 或结构断言覆盖，绿在哪个解释器版本上产生？[Clarity, Measurability, Coverage, Req §FR-036, Req §FR-037, Req §SC-009]
- [ ] CHK033 - 零第二机制是否以可重复的结构断言取证——FR-035 / SC-008 的「变更集审计」是否给出具名计数（持久化根 / registry / renderer / 写点）与转红注入，而不是一次性叙述？[Measurability, Req §FR-035, Req §SC-008]

## 六、SC、Shared Strings、裁定落点与观测附录

- [ ] CHK034 - SC-003 的「SSH 远端夹具 / 端到端」与 A3 的「不在测试套件内真实铺设 SSH 主机」是否一致——验收要求的究竟是真实主机、合成记录还是既有 external-dispatch recipe 产物？[Ambiguity, Consistency, Req §SC-003, Req §A3]
- [ ] CHK035 - 声明「FR-xxx 已按本裁定补句」的澄清裁定是否真的落入正文——以 FR-033 的段落位置（`## Spec Kit Framework Map` 之后、`## Spec Kit Runtime & Symlink Model` 之前）与 FR-038 的「切片机制主张 / `not-observed` 理由」为实测反例，这两处是否仍然只存在于 Clarifications？[Traceability, Req §Clarifications, Req §FR-033, Req §FR-038]
- [ ] CHK036 - Shared Strings 的 `Consumed by` 是否双向完整——实测缺口：STR-002 未列 FR-005，STR-003 未列 FR-034，STR-004 未列 FR-004 / FR-034；引用约定所称的 CI / analyze 检查是否包含这个反向方向？[Traceability, Req §Shared Strings]
- [ ] CHK037 - 观测附录的读数是否可复核——「可解析证据路径」的判据是什么（文件存在、内容可解析还是命令可复现），哪些情形必须记 `not-observed`（含理由），080–094 的 14 个存在切片是否钉在其一测量时点 / commit 上？[Measurability, Req §FR-038, Req §SC-010]

## 七、术语与假设纪律

- [ ] CHK038 - 术语形态是否全篇一致——正文 `super agent`、机读 `superagent`（[[STR-001]]）、组合标记 `dual-role`（[[STR-002]]）、别名 `super-agent` 是否按 A15 的规定在 Requirements / SC / Clarifications / Assumptions 各处一致，没有把组合标记写成第三种角色值？[Consistency, Req §A15, Req §Clarifications]
- [ ] CHK039 - 本清单自身是否守住了边界——39 条是否都能只凭需求文本（或它点名的 owner 行）回答，没有一条要求运行产品，也没有一条在为 plan / tasks 打分？[Consistency, Gap]

## Notes

- 条目分布：引言与判定面 8 条、协议与注入 10 条、并发 / 状态 / 恢复 7 条、跟踪与可视化 2 条、harness 与零第二机制 6 条、SC / 字符串 / 裁定 / 附录 4 条、术语与自检 2 条，合计 **39 条**（`grep -c '^- \[ \] CHK'` 可复算）。
- 追溯率：**39/39 = 100%**（每条都带 `[Req §…]` 锚或 `[Gap]` / `[Ambiguity]` / `[Conflict]` 标记），高于方法论要求的 ≥80%。
- 未超软上限 40 条；无条目以「Verify / Test / Confirm / Check + 实现行为」开头；`plan.md` / `tasks.md` 只在 CHK017 / CHK019 / CHK026 / CHK027 / CHK032 / CHK034 / CHK035 中用于暴露需求缺口，没有一条评价它们自身。
- 勾选一条的唯一依据是需求文本（或该条目点名的 owner 行）给出了答案；`fail` 产出的是对 `requirements.md` 的 finding，不是一条实现任务。
- 本清单不刷新既有条目：下一轮复检请新建 `recheck-<date>-<topic>.md`，逐条引用本轮所答的需求行原文并带锚（`create-checklist` § 5 Recheck form）。
- 既有 `checklists/requirements.md`（2026-11-10，4,495 B）是 requirements 阶段自带的规格质量门禁记录，本清单不覆盖它。
- 全部计数、引用核对、预算与切片读数来自本轮实跑：`../test-evidence/checklist-readings-2026-11-10.txt`。
