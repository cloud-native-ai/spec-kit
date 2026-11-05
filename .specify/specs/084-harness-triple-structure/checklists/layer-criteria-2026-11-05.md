# 三重结构判据与判读 — 需求质量检查清单

**Purpose**: 检验 Feature 084「Harness 三重结构（markdown + yaml + script）」需求的**写作质量**——范围判据 D1 ∧ D2 是否可判定、候选屏幕 S 是否可重算、三批迁移是否各自独立可验收、`complete`／`pending` 与封闭原因集是否闭合、双写者与 081 冻结面是否可测量、Two Hats 的镜像与分发路径是否写全、非目标 N1–N7 是否可判。每一条都是对需求文本（或它点名的 owner）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-05
**Feature (Requirement Scope)**: `.specify/memory/features/084.md`（Feature 084 Harness 三重结构）
**Requirements (What)**: [../requirements.md](../requirements.md) — 19 FR / 6 SC / 14 STR / 4 user stories / A1–A10 / N1–N7
**Specifications (How, context only)**: [../plan.md](../plan.md)、[../data-model.md](../data-model.md)、[../contracts/](../contracts/)、[../quickstart.md](../quickstart.md)、[../tasks.md](../tasks.md) —— 只用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成，方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`。勾选一条的唯一依据是**需求文本本身**给出了答案；答「否」产出的是对 `requirements.md`（或该条目点名的 owner）的 finding，不是一条实现任务。
**Detection path**: 本清单的全部条目由**单上下文受限直读**产出（本执行拓扑无法派发只读子代理），依据 `.specify/shared/workflow/objective-analysis-gate.md` 规则 7 的降级路径记录于此，适用于下面每一行。

## 一、范围判据 D1 ∧ D2 的可判定性

- [ ] CHK001 - D1（资产面）与 D2（机器面）是否各自独立可判、且「两条合取、单独任一条都不充分」这条组合规则在文中只陈述一次？[Clarity, Completeness, Req §FR-002]
- [ ] CHK002 - D1 点名的四类交付物 (a) 证据记录／(b) feedback 或学习记录／(c) 门禁 verdict／(d) 改动 harness 资产 是否为封闭枚举，且每一类都能在树内指认落点？[Completeness, Measurability, Req §FR-002]
- [ ] CHK003 - 当某个候选单元只不满足 D1（或只不满足 D2）时，它该取三个排除理由中的哪一个，是否由需求正文判定——还是留给 FR-001 那个尚未存在的 owner 文档，从而使今天的复核者无法回答「这条排除对不对」？[Ambiguity, Gap, Dependency, Req §FR-001, Req §FR-002, Req §FR-003]
- [ ] CHK004 - (d) 类「对 `skills/`、`agents/`、`teams/`、`tools/`、`docs/`、宪法或指令的改动」是否被量化到能区分单元（改动必须落在该单元的验收交付物里？任何改文档的命令都算？），使 D1 保持可判而非近乎恒真？[Ambiguity, Measurability, Req §FR-002]

## 二、候选屏幕 S 与流程单元边界

- [ ] CHK005 - 屏幕的三组载体面（`templates/commands/*.md`、`skills/{external,internal}/*/SKILL.md`、`shared/workflow/*.md`）是否被声明为**穷尽**，从而说清一个引用框架引擎却不属于三面的载体（实测：`templates/review-template.md` 第 148 行引用 `scripts/python/closure-acceptance-check.py`）到底是「不是单元、因此不需处置」还是「漏判」？[Coverage, Gap, Req §FR-004]
- [ ] CHK006 - 屏幕的匹配规则是否被量化（路径子串命中，还是词边界／正则命中；`.specify/scripts/python/x.py` 的客户端形态算不算命中），使两份实现不会在同一棵树上给出不同候选集？[Clarity, Measurability, Req §FR-004]
- [ ] CHK007 - 「载体」（一条事实被指向的 markdown 文件）与「流程单元」（有处置记录的对象）的区分是否被明写，使一个 `templates/*.md` 载体不必为它自己没有处置记录而报错？[Gap, Consistency, Req §FR-004, Req §FR-005]
- [ ] CHK008 - Edge Cases 末条接受屏幕「保守侧」（只在散文里提到脚本路径也算候选）与「一个候选单元 MUST 有且仅有一条处置记录」是否相容——被保守纳入的边界样本，只追加一条排除记录就能退役，而不需要第二套「是否真的调用」的判定？[Consistency, Edge Case, Req §FR-004, Req §FR-005]

## 三、完整性与封闭原因集

- [ ] CHK009 - FR-007 的三条合取条件是否每一条都机械可判，且「部分满足」时状态取唯一个名字（而不是两个读者各判一个）？[Clarity, Measurability, Req §FR-007]
- [ ] CHK010 - 「读取点在源码中可定位」是否被量化到可判的形态（文本定位器：引用共享读取入口 + 该事实 slug），并声明它**不**证明语义正确，使 (c) 不依赖实施者的自述？[Ambiguity, Measurability, Req §FR-007]
- [ ] CHK011 - § Shared Strings 的形态规则内部是否自洽——实测六条原因模板**每条**都带占位符（四条一个、一条两个、一条一个），而该节却称「一条无占位符（STR-013 只有一个 `<unit>`）」？[Conflict, Req §Shared Strings, Req §SC-003]
- [ ] CHK012 - 降级标注（FR-012 的 `[[STR-014]]`、FR-013 的「未接线」标注）与「finding」是否被区分，并交代它对应的退出码——它是六条封闭原因之一（SC-003 按 exit 1 计）还是 exit 2 的输入错误标签？[Conflict, Ambiguity, Req §FR-012, Req §FR-013, Req §FR-017]
- [ ] CHK013 - 降级标签的**逐字形态**有没有一个具名 owner——它在封闭六条之外，因此既不受 § Shared Strings 的形态规则约束，也没有任何表登记它？[Gap, Traceability, Req §FR-013, Req §FR-017]
- [ ] CHK014 - 「六个原因各有一份负夹具、对应正夹具 1/1」这条配对义务是否按**原因**逐一陈述（FR-017）而不是只在 SC-003 汇总为 6/6 + 1/1，使漏做一条可以被指名？[Completeness, Req §FR-017, Req §SC-003]
- [ ] CHK015 - 一条事实的 `consumers` 若只列载体、没有任何引擎（引擎读取点因此永远不成立），这是 schema 违规还是一种合法的长期 `pending`——需求有没有判这一格？[Gap, Ambiguity, Req §FR-005, Req §FR-007]
- [ ] CHK016 - 排除记录里的 `reason` 是**文件名的值**还是**行内键**——FR-005 的「`unit`／`carrier`／`anchor` 三键齐备」与 § Key Entities 把 `reason` 列为属性，二者给出不同的形状？[Conflict, Req §FR-005, Req §Key Entities]

## 四、成功标准的可测量性

- [ ] CHK017 - SC-001 (iii) 双向一致的 `N/N` 分母是否独立于「该次运行报出的条数」之外可定义，使同一棵树上的两次读数可比较？[Measurability, Req §SC-001]
- [ ] CHK018 - SC-002 的三段（状态侧／声明侧／残留侧）是否各自成为独立的通过条件，并明写「声明文件都存在」不得充当声明侧读数？[Measurability, Completeness, Req §SC-002]
- [ ] CHK019 - SC-002 用到的 `partial`（任一段不成立时「该条记 partial」）是否被定义为**标准级**状态并有 owner，从而不与 FR-007 的二值单元状态混用？[Ambiguity, Consistency, Req §SC-002, Req §FR-007]
- [ ] CHK020 - SC-006 的「相对基线」是否点名了基线参照物（某个提交或某份已记录读数），满足封闭清单声明对包含性主张的五要件？[Measurability, Req §SC-006]
- [ ] CHK021 - 「既有门禁脚本」这份封闭集的成员是否只有一个定义——FR-010 列五个（含 `doc-consistency-check.py`）、FR-019 说「四个」、N5 列四个、SC-006 列五个（含 `closure-acceptance-check.py` 而不含 `doc-consistency-check.py`）、SC-006 Source 又写「四个」？[Conflict, Consistency, Req §FR-010, Req §FR-019, Req §N5, Req §SC-006]
- [ ] CHK022 - 「既有测试零新增失败」的作用对象是否由**规则**闭合（哪一批文件、按什么选出），而不是一个会随分支移动的快照计数？[Clarity, Measurability, Req §FR-019, Req §SC-006]
- [ ] CHK023 - 确定性（两次运行逐字节一致）只被写在 SC-001 对 `coverage` 的读数上；`verify` 与 `lookup` 的确定性是**故意不要求**还是遗漏？[Gap, Coverage, Req §FR-016, Req §SC-001]

## 五、迁移批次、兼容性与并发安全

- [ ] CHK024 - 「每批独立可验收」是否由一条可观察读数定义（该批 0 报错 + 未迁单元 0 误红），并且批次切分由一条**写出来的判据**（爆炸半径）而非仅由名单固定？[Measurability, Ambiguity, Req §FR-011]
- [ ] CHK025 - 「未完成的后续批次 MUST NOT 被报成前一批的失败」这条归属规则是否出现在需求正文，还是只存在于 plan 侧的迁移契约？[Gap, Req §FR-011]
- [ ] CHK026 - 双写者验收说的是**哪两棵树**、在迁移的**哪个时点**（批 1 之前只有 `pending`，之后才有 `complete`），使断言可复现？[Ambiguity, Measurability, Req §FR-015]
- [ ] CHK027 - 兼容性是否写成互斥分支——声明缺席 ⇒ 允许内联值但 MUST 带 `[[STR-014]]`；声明存在 ⇒ 内联值 MUST 删除（MUST NOT 双读）——而不是两条可同时成立的许可？[Consistency, Req §FR-012]
- [ ] CHK028 - 「本特性关闭时 in-scope 集合内 `pending` 为 0」（SC-002）与迁移期内合法的 `pending` 是否被明确区分为两个时点的读数，使兼容态不能悄悄成为终态？[Consistency, Req §FR-012, Req §SC-002]

## 六、081 冻结面与非目标

- [ ] CHK029 - 081 的两个验收文件是否被点名，并且「零改动」与「零新增失败」被写成两条各自可判的读数（一个绿套件不能顶替一个未被编辑的文件）？[Completeness, Measurability, Req §FR-018, Req §SC-006]
- [ ] CHK030 - FR-018 的受影响 owner 清单用「至少」限定：这是否使「漏掉一个该迁的 owner 文档」不可判定——需求有没有给出闭合该清单的规则？[Clarity, Gap, Req §FR-018]
- [ ] CHK031 - N1–N7 是否每一条都给出判据 owner 与**证伪信号**（N4、N7 也各自可判），使「非目标未越界」不是一句无法反驳的声明？[Completeness, Traceability, Req §Non-Goals]
- [ ] CHK032 - FR-006 (ii) 的四个「面」（引擎／markdown 载体／模板／被测试钉住的字面量）是否互斥，使「跨面」不能被同一个面里的两份副本满足？[Clarity, Consistency, Req §FR-006]

## 七、Two Hats、镜像与分发

- [ ] CHK033 - 每件新增产物是否都同时写下了框架源路径与镜像路径，并声明唯一的投影路线是既有 `sync-mirrors.py` 配对；新目录的登记是否与创建**同一变更**（含其镜像副本的登记）？[Completeness, Consistency, Req §FR-013, Req §FR-014]
- [ ] CHK034 - 客户项目的 `.specify/` 形态与框架源的源形态是否被区分，并给出同一解析规则覆盖两形态，使一份声明在三份物理副本里都成立？[Clarity, Coverage, Req §FR-013, Req §STR-002]
- [ ] CHK035 - 分发读数以哪条 `specify init` 路由为准是否被写下——实测两条路由给出不同读数（控制台入口 55 个 md，源检出路由 62 个），而 FR-013／SC-005 都没有点名路由？[Ambiguity, Req §FR-013, Req §SC-005]

## 八、跨产物一致性与可追溯性

- [ ] CHK036 - 被复用的 `duplicate` 面的**调用面**是否被固定在需求里，使「零命中」在两位复核者手里是同一个读数——实测同一棵树上只给 `--spec-dir` 得「扫 14 个文件、0 条 finding」，再加 `--path` + `--owner-path` 得「扫 15 个文件、2 条 finding」（2026-11-05 读数，命令见证据文件 § 4(f)）？[Clarity, Measurability, Req §FR-007(b), Req §FR-010]
- [ ] CHK037 - 需求编号命名空间是否在 FR-019 闭合——下游 `tasks.md` 有两处引用 `FR-023`，而本规格只定义到 FR-019：这是规格缺了一组需求，还是引用越界？[Traceability, Gap, Req §Requirements]
- [ ] CHK038 - 「`scripts/` 与 `skills/` 下只允许一个子集解析器、两个既有解析器在白名单内」这条边界守卫是否可追溯到某条 FR（今天只出现在 plan 契约 C-058），使它在需求层也有验收面？[Traceability, Gap, Req §FR-009, Req §FR-019]

## Notes

- **本轮的意图默认值（无人值守，未访谈）**：Depth = Standard · Audience = Reviewer · Focus = 派发简报点名的四个高风险簇——(1) D1∧D2 判据与候选屏幕 S 的可判定性／可重算性；(2) 三批迁移的独立可验收性与并发安全；(3) `complete`／`pending` 与封闭原因集、081 冻结面零改动；(4) Two Hats 镜像路径与非目标 N1–N7。三个意图问题被跳过，因为派发简报已经固定了范围、深度与读者；没有用户自定条目被并入。
- **可追溯性**：38/38 条（100%）带至少一个 `Req §…` 锚或 `Non-Goals` 锚，两种算法都在 80% 下限之上；其中 21 条另带 `[Gap]`／`[Ambiguity]`／`[Conflict]`／`[Coverage]`／`[Dependency]` 标记，其余 17 条是锚在所受判需求上的清晰度、完整性或可测量性提问。全部 38 条为问句形态，无一以「Verify／Test／Confirm／Check + 实现行为」开头。
- **同作者缺口发现的方法学限制**：本技能的规范做法是把缺口发现委派给新鲜上下文的只读子代理，因为本规格与本清单出自同一条运行线，作者盲点会按同样方式复现。本执行拓扑**无法派发子代理**（无该工具），故按 `.specify/shared/workflow/objective-analysis-gate.md` 规则 7 降级为**单上下文受限直读**，并在此明示：这不是覆盖性的主张，`/speckit.analyze`（只读、独立上下文）应复核本清单未命中的缺口。
- **本清单的推理只用已产出的产物**：所有被引用的读数都在本轮实跑中取得（`duplicate` 面的两种调用面、`templates/review-template.md` 的引擎引用行、六条原因模板的占位符计数、`tasks.md` 中 `FR-023` 的两处命中、`better-harness.md` § 消费者清单 的存在），逐字输出见 `../test-evidence/checklist-self-check.txt`；未凭记忆断言任何计数。
- **PLAN CONSTRAINT 已遵守**：本轮没有读取或修改任何 plan-owned 产物（`plan.md`、`data-model.md`、`contracts/`、`quickstart.md`、`research.md`、`feature-ref.md`），也没有触碰 `requirements.md` 与 `tasks.md`；本清单只新增一个文件加证据。任何"需要改 plan"的结论都写成提问，而不是编辑。
- **若只能回答三条，先答这三条**：CHK021（既有门禁脚本的成员在四份文本里给出四/五两种集合——这是本特性"封闭集只应存在一份"主张的对内反例）、CHK011（封闭原因集的形态规则自相矛盾，而 SC-003 要求逐字判定）、CHK012（降级标注与 finding 的退出码未决，FR-012／FR-013／FR-017 三者读法不同）。
- **两条疑似越界的事实，交 analyze 裁决而非在本阶段修平**：CHK037 的 `FR-023` 引用缺失与 CHK021 的门禁集合分歧，都需要在"改 `tasks.md`／改 `requirements.md`"之间做选择；本轮只登记，不修改任何非本阶段产物。
- **判定状态**：每条前面的 `[ ]` 就是它的判定位——未勾选 = 尚未由复核者判定。勾选只在需求文本本身回答了该问题时进行；答「否」按 `.specify/skills/internal/create-checklist/SKILL.md` 第 5 步的复核形态，在**新**的 `recheck-<date>-<topic>.md` 里逐条引用它回答的那行需求（逐字 + 锚），本文件不被就地刷新。
- **类别读取（本阶段唯一一次）**：`python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` → `flow_class: execution` / `flow_type: -` / `source: declaration` / `marker: null` / exit 0，故本阶段门禁集逐字不变、零新增阻断项。
- **确定性自检**：条目数、CHK 编号连续、可追溯比例、禁用开头、重复编号、既有 `requirements.md` 清单未被覆盖，均由一段内联检查程序判定，逐字输出存 `../test-evidence/checklist-self-check.txt`；阶段测试预算读数是 `../test-evidence/stage-status.md` 的 checklist 行。
