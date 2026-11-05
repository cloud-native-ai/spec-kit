# Requirements Specification: Harness 三重结构（markdown + yaml + script）

**Requirement Branch**: `084-harness-triple-structure`
**Created**: 2026-11-05
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "在所有涉及到harness的流程中, 需要使用 markdown + yaml + script的三重结构来实现, 之前主要使用markdown + script的两层结构."

## Related Feature *(mandatory)*

**Feature ID**: 084
**Feature Name**: Harness 三重结构（markdown + yaml + script）

**Binding verdict（`/speckit.clarify` Mode A，2026-11-05）**: **新建 Feature 084**，未绑定既有 Feature。判据与证据归 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules，本节的候选复核是它的执行记录：

| 候选 Feature | 状态 | 范围一行摘要 | 裁定依据 |
|---|---|---|---|
| 081 更严格的验收与产物审查 | Completed | `Blocked` 一等状态、`Implemented` 四条件、closure 判定脚本、review 四段 + ARC | 范围是**门禁阈值与验收词表**，不含载体分层；本特性只按其 § Closure Verdict 的「取值域单一 owner」意向把 `Path` 取值迁入声明层（见 A8 裁定），不继承其验收责任 |
| 069 执行／表达二元分类与文档型 SDD 同构 | Implemented | 类别判据、取值域、逐流程台账、六面与阶段算子表 | 范围是**分类轴与文档型同构**；它是本特性 FR-018 的**载体**之一（其 owner 文档改为指针），不是本能力的归属者 |
| 053 机器可判定的制品命题 | Implemented | 把制品对自己／兄弟制品的结构性断言从「代理读后声明」改为「程序判定后输出」（`validate-requirements.py` 是该线的产物之一） | 范围是**判定资格**（谁给出 verdict）；本特性是**取值存放位置**（声明层），两者正交 |
| 055 冲突无关的 Feedback/Memory 存储 | Implemented | 一文一件、派生索引即读即建、双写者测试 | 范围是**存储布局**；本特性的声明层**遵守**其判据，不扩展它 |

**Binding-precedent heuristic**: 四个候选各有自己的兄弟规格域（081 → `081-acceptance-hardening`；069 → `069`／`069a`／`069b`；053 → 五个检查器；055 → feedback／memory 存储），无一曾吸收「跨流程单元的声明层 + 覆盖判定引擎」这类工作；`shared/declarations/` 在树内不存在、`grep -rn "shared/declarations" shared/ templates/` 零命中，证明这是一条**尚无 owner 的新能力**。故 create 而非 bind。

**ID 取值 084**: spec key `084` 与 Feature ID 对齐（本仓惯例；081 同一做法，082／083 未占用）。登记已落 `.specify/memory/features.md` 行（`Total Features` 同趟重算 76 → 77）与 `.specify/memory/features/084.md`，状态 `Draft`（`/speckit.requirements` 拥有的状态，不预支 `Planned`）。反向交叉引用写在 `.specify/memory/features/081.md` § Related Files（只引用，不改其状态）。

## Assumptions（本阶段自行裁决，clarify 逐条复核）

裁决语法：**confirmed** = 假设成立且仓内证据可复核；**adopted** = 本阶段作出设计选择并给出理由，clarify 可改判；**deferred** = 明确留给后续阶段裁定，本阶段不预设结论。没有一条被静默丢弃。

**clarify 复核语法（2026-11-05，`/speckit.clarify` Mode A，无人值守零提问）**：每条假设末尾的 `clarify 裁定：` 行是它的**最终裁定**，取值域封闭为三值——**ratified**（原裁决成立，证据已复核）／**revised**（原裁决局部改写，改写内容与受影响条款写明）／**superseded**（原裁决被本轮另一裁定取代，取代者点名）。十轮裁定无一条被静默丢弃，也无一条被降级为「仍待定」。裁定依据与 `## Clarifications` § Session 2026-11-05 的问答行一一对应。

- **A1（类别判定 = `execution`，basis = `behavior-oracle`）— 裁决：confirmed**。主交付物是一组机器读取的声明文件加一个确定性校验引擎，外加把既有散文/常量副本改为指针的迁移；其缺陷最先在机器面暴露（声明不可解析、覆盖集与载体不一致、脚本仍读自己那份常量、门禁对同一事实给出两份取值）。按 `.specify/shared/definitions/flow-class-definitions.md` § 判据，`Flow Type` 写 `-`。本特性产出中 Markdown 占比很高（定义文档、任务、报告），但介质不参与判定（owner § 不参与判定的因素）。**待复核证据**：`flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` 应解析出 `flow_class: execution` / `source: declaration`。**clarify 裁定：ratified**。实跑 `flow-class-check.py --action lookup --unit-id "spec:084-harness-triple-structure"` → `flow_class: execution`／`flow_type: -`／`source: declaration`／`marker: null`／exit 0（逐字输出存 `test-evidence/flow-class-lookup-clarify.txt`）。`source=declaration` 是判据成立的关键：类别由本文件头部声明行解析，不依赖任何注册表行。`basis` 在 spec 类单元上由引擎回 `null`（该轴只对台账单元机械解析），故 `behavior-oracle` 仍是由本规格自陈的判定依据，本条不主张机器已核验它。对产物的影响：类别与 `Flow Type: -` 不变，本阶段门禁集逐字不变、零新增必填章节。

- **A2（「归 yaml 的事实」判据 = 机器消费 ∧ 跨面）— 裁决：adopted**。单一条件「有机器消费者」会把引擎内部常量（如 `run-determination.py` 的文本截断上限）也拖进声明层，制造无价值的声明噪声；单一条件「多面重复」又会漏掉只被两个引擎共享、无人写进散文的事实。故取两条合取，见 FR-006。**为什么需要这条裁决**：没有它，「哪些事实该迁」只能凭手感，而手感正是本特性要消灭的东西。**clarify 裁定：revised（收窄 (i) 的读法，判据本身不变）**。原 (i) 只要求「存在确定性引擎必须读取该值」，把「有一个契约测试钉住该字面量」也算了进去——按那个读法，`validate-requirements.py` docstring 的六个检查项标签集会被判为该迁，而它的唯一消费者是**测试的提取断言**，没有任何引擎判决取决于标签集本身（标签只是消息前缀）。收窄后的 (i)：**机器消费 = 存在一个确定性引擎，其判决结果随该取值改变而改变**（读常量作比较、按封闭集拒绝／放行、按表选门、按 schema 校验）；仅被测试钉住、但没有任何引擎读它作判决的字面量，不构成机器消费。这条收窄是 A8(b) 裁定的直接产物，已同趟写入 FR-006 正文。对产物的影响：`## Initial Scope Adjudication` 中 requirements 单元那一行改写为「`Path` 取值域 in-scope／标签集不迁」，并新增 N7 记录不迁的理由；其余行的 D2 判定不变（每行的事实都有引擎读它作判决）。

- **A3（「harness 流程」的边界用「资产面 ∧ 机器面」判据，不新造流程清单）— 裁决：adopted**。仓内已有两份流程单元名册——`shared/definitions/flow-class-definitions.md`（80 行台账，覆盖 `templates/commands/*.md` 与 `skills/{external,internal}/*/SKILL.md`；原写 79，clarify 实测订正）与 `.specify/shared/definitions/framework-map.md`（目录布局）。本特性 MUST NOT 造第三份名册；边界判据见 FR-002，逐单元处置见 § Initial Scope Adjudication（dated baseline，非 owner）。**理由**：`one-source-of-truth` 与「不得出现第二份分类数据文件」判据同源。**clarify 裁定：ratified（附一处事实更正）**。复核命令与读数：`grep -cE '^\| (/speckit\.|skill:)' shared/definitions/flow-class-definitions.md` → **80**（本行原文写「79 行台账」，实测 80 行；另 5 行为 § 类中立清单 的技能行，不在台账内）；载体侧 `ls templates/commands/*.md | wc -l` → 27、`ls skills/{external,internal}/*/SKILL.md | wc -l` → 53，合计 80，与台账逐一对齐。该计数是被订正的事实陈述，不改变本裁决：台账 + `framework-map.md` 已是两份既有名册，本特性 MUST NOT 造第三份。FR-004 的候选屏幕 S 把 `shared/workflow/*.md`（19 件）也纳入候选集，而这些单元在类别台账中无行——这不是矛盾：台账的职责是**类别归属**，本特性的职责是**处置归属**（一条事实声明或一条排除记录），两者是不同的判据，本特性 MUST NOT 为对齐台账而新增 `flow_class` 行。对产物的影响：仅本行计数与其证据，其余条款不变。

- **A4（YAML 落点 = `shared/declarations/`，随既有镜像分发）— 裁决：adopted**。框架源新增 `shared/declarations/`，经 `scripts/python/sync-mirrors.py` 的既有 `shared → .specify/shared` 映射自动投影为 [[STR-002]]，MUST NOT 手改镜像、MUST NOT 新建顶层目录。**理由**：Directive-Governance 要求新目录在同一变更内登记含义；Two Hats 要求跨项目生效必须落框架源。**clarify 裁定：ratified**。复核 `scripts/python/sync-mirrors.py` `MIRROR_PAIRS` 第 6 项 = `("shared", ".specify/shared", False, set())`，即 `shared/declarations/` 一经落地即被既有镜像机制投影，无需新映射、无需手改镜像；`ls shared/` 与 `grep -rn "shared/declarations" shared/ templates/` 确认该目录今天不存在、无同名占用，故不是「第二套机制」。对产物的影响：无改写。

- **A5（YAML 子集 + stdlib-only，不引入解析库）— 裁决：adopted（bounded）**。仓内既有先例是自写子集解析：`scripts/python/execution-config.py` 的 `parse_yaml_subset()` 与 `gate-check.py` 的行级解析器，`pyproject.toml` 的运行依赖里没有任何 YAML 库。本特性沿用该先例并把子集**明确写下来**（FR-008）。**已知重复、本特性不修**：`execution-config.py` 的内联解析器不并入本特性的共享读取入口，登记为后续项（见 § Non-Goals N4）；EN: 不把「顺手重构」塞进一个已经跨面的特性。**clarify 裁定：ratified（bounded）**。复核三个前提仍成立：`scripts/python/execution-config.py:136 def parse_yaml_subset(path: Path)` 在场；`scripts/python/gate-check.py:48 def parse_gate(text: str)` 为行级解析；`pyproject.toml` 的 `dependencies` 六项（`typer`／`rich`／`httpx[socks]`／`platformdirs`／`readchar`／`truststore`）无任何 YAML 库。故 FR-008／FR-009 的「子集 + stdlib-only」是沿用先例而非新约束。对产物的影响：无改写；N4 保留。

- **A6（派生索引即读即建：不建 ledger 聚合文件）— 裁决：adopted**。单元处置 MUST 由声明文件反投影得出，MUST NOT 维护一份手工总表（`.specify/instructions.md` § Concurrent Development Safety：`派生索引即读即建`）。冲突热点按「一文一件」化解：事实一条一文件；排除记录按**理由**分文件（封闭三值，至多三份），因为排除集近似静态而事实集持续增长。**clarify 裁定：ratified**。与 `.specify/instructions.md` § Concurrent Development Safety 的三条判据逐条对位：记录类数据一文一件（`facts/<fact-slug>.yaml`）✓；派生索引即读即建（单元处置由声明反投影，FR-016 的 `--action lookup` 是读取入口而非存储）✓；单一所有者状态例外（`contract.yaml` 与至多三份排除文件是取值域／近静态集，不是可变处理状态）✓。对产物的影响：无改写；FR-014／FR-015 的「MUST NOT 创建聚合 ledger」保留。

- **A7（`better-harness.md` 的五维表不迁；其内的七态枚举必须迁出为指针）— 裁决：adopted**。五维表的消费方式是散文引用（「本次改进强化了 Change Validation 维度」），没有引擎读它 → 按 FR-006 留在 markdown，它继续是维度名的 owner。相反，该文件 § 证据纪律 第 2 条把七态枚举**全文重列**了一遍（`.specify/shared/guidelines/better-harness.md` § 证据纪律，item 2），而 `evidence-utils.py` 有同内容的常量、`evidence-discipline.md` 是定义 owner → 三面重复且被机器消费，必须迁。**这条裁决用于示范：分层规则对本特性的目标锚点自己也成立。** **clarify 裁定：ratified**。复核证据：`shared/guidelines/better-harness.md` § 证据纪律 item 2 把七态枚举**全文重列**（`Present / Wired / Exercised / Outcome-supported / Missing / Unobserved / Not applicable`）并指向定义 owner；`scripts/python/evidence-utils.py:23 SEVEN_STATES = (` 是同内容的引擎常量；`skills/internal/collect-evidence/references/evidence-discipline.md` 是定义 owner。三面（散文重列 + 引擎常量 + 定义 owner）+ 被机器消费 ⇒ 按 A2 收窄后的判据仍成立，必须迁。反向证据（五维表不迁）：`grep -rn "Change Validation\|五维" scripts/ skills/*/*/scripts/` 对五维表零引擎读取 ⇒ 按 FR-006 (i) 不成立，留在 markdown 继续做维度名 owner。对产物的影响：无改写；该条继续是批 1 与 FR-018 的输入。

- **A8（`Path` 标注与检查项标签集：取值迁 yaml，判据留原 owner）— 裁决：adopted**。`**Path**: final|supporting` 的判据 owner 是 `.specify/shared/workflow/acceptance-hardening.md` § Closure Verdict（081 已落），`validate-requirements.py` 的六个检查项标签集被其 docstring 自述为「pinned label set」。本特性只把**取值集**移入声明层，判据散文与严重度不动，原 owner 获得指向声明的指针。**若 clarify 判定该条越界（改写 081 已验收契约），改判为排除并记 [[STR-008]] + 锚点。** **clarify 裁定：revised（一条拆成两条，同一判据分别适用，结论相反）**。

判定用的**封闭测试**（本轮自设并公开，供反驳）：迁移一条取值域是否「越界改写 081 已验收契约」= 迁移后是否仍满足三条合取——(a) 同一输入集被接受、同一输入集被拒绝；(b) 拒绝理由的字面量与退出码契约逐字不变；(c) 081 既有测试断言零改动。三条全成立 = 不越界；任一不成立 = 越界。

- **A8(a) `Path` 取值域 `{final, supporting}` —— 不越界，保留 in-scope（批 1）**。三条全成立：该取值域今天有三处实体——owner 散文 `.specify/shared/workflow/acceptance-hardening.md` § Closure Verdict（「Input contract — the `Path` marker」）、`scripts/python/validate-requirements.py:98 PATH_VALUES = ("final", "supporting")`、`scripts/python/closure-acceptance-check.py:505 if value not in ("final", "supporting")`——正是 FR-006 的「机器消费 ∧ 跨面」；迁移后两个引擎经 FR-009 的共享入口读同一份声明，**成员集合不变**（取值仍恰为这两个），拒绝消息模板与 exit 2 的输入错误语义由该 § 保留、不动，`tests/contract/test_requirements_checker.py` 的 `path-marker` 族断言输入行为而非常量，故 (c) 成立。**判据散文留在原 owner、只把取值集移入声明层并给原 owner 加指针**，这正是 FR-018 对 069／050 等既有 owner 文档的同一处理。081 是 `Completed`，故本条附带一条硬约束（写入 FR-018）：迁移 MUST NOT 改动 081 的任何测试断言，新增失败必须为 0（SC-006 的封闭集也相应纳入 `closure-acceptance-check.py`）。
- **A8(b) 六个检查项标签集 —— 越界，不迁**。(c) 直接不成立：`validate-requirements.py` docstring 自述「this enumeration IS the pinned label set」，而 `tests/contract/test_requirements_checker.py:105 test_c01_c02_docstring_enumerates_exactly_the_pinned_labels` 用 `^  ([A-Za-z][A-Za-z-]*)\s{2,}` 从该 docstring 提取集合并断言其**等于** `REQUIREMENTS_CHECKS`；迁出标签集就必须改写这条 081 验收测试的断言，或把标签集在 docstring 里留成第二份（则迁移零收益）。而且按 A2 收窄后的 (i)，标签集**没有判决型消费者**：引擎不读它做判定，测试只钉住它。**记录方式**：不写排除记录（[[STR-008]] 是**单元**级理由，而该单元已因 A8(a) 的 in-scope 处置而持有唯一处置记录；再写一行排除记录会违反「一个候选单元 MUST 有且仅有一条处置记录」），改记入 § Non-Goals **N7** 并附可解析锚点（上述测试文件 + docstring 行）。对产物的影响：FR-006 (i) 收窄、FR-018 增补 `acceptance-hardening.md` 与「081 测试零改动」条款、SC-006 纳入 `closure-acceptance-check.py`、`## Initial Scope Adjudication` 该行改写、新增 N7。

- **A9（`specify init` 的分发路径由 plan 钉，本阶段只声明义务）— 裁决：deferred → plan**。要求是「新目录必须随框架分发到客户项目，旧项目缺失时降级而非失败」；具体资产清单与升级动作属实现口径，本阶段不预设。**clarify 裁定：ratified，并把「留待 plan」从一条不做承诺的移交改成可判定的移交**。三条义务已经在文内可判，故不构成 taxonomy 意义上的「仍开放的选择」：① 分发义务 = FR-013（`specify init` MUST 把 [[STR-001]] 分发；旧项目缺 [[STR-002]] 时引擎 MUST 降级为「未接线」并显式标注、MUST NOT 抛异常、MUST NOT 被读作通过）；② 证据义务 = SC-005（临时夹具上跑 `specify init` 后目录存在且 checker 可运行，或按降级契约显式标注后 exit 2 并记录该次读数）；③ 归属义务 = `.specify/memory/features/084.md` 与 FR-013 的 `RS-003` 行（`in-scope`：本仓交付该能力）。因此本阶段**不预设**的只剩 plan 必须产出并登记的**清单产物**（资产名册与升级动作），判定点是它出现在 plan 的交付物里，而非本阶段猜它的内容。对产物的影响：无改写。

- **A10（本阶段无 clarification marker）— 裁决：confirmed**。所有开放点都能在目标仓库内裁决并留证；剩余的真裁定（A8 的越界判定、FR-011 的批次切分）显式交给 clarify / plan，不伪装成已决。**clarify 裁定：ratified（前半）／superseded（后半，已履行）**。前半复核成立：`validate-requirements.py` 的 `marker-count` 判项在本轮全部写回后仍为 `pass (0)`，即规格内 0 个活动澄清标记——本轮没有提出 marker，是因为答案空间被仓内证据闭合，而不是因为没有裁定。后半已被履行并因此退休：A8 的越界判定由本轮裁定（拆成 (a) 不越界／(b) 越界，见 A8 条目）；FR-011 的批次切分仍归 plan，但它已是一条具名 plan 交付物（首批名单 + 每批独立可验收），不是「待定」。对产物的影响：该条不再作为「以后再说」的容器存在。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一条事实只有一个机器读得到的定义点 (Priority: P1)

维护者要把 feedback 的提示阈值从 10 调成 20。今天他必须同时改 `scripts/python/feedback-utils.py` 的常量与 `shared/workflow/feedback-step.md` 的散文，否则引擎与文档各说一套，而两边都有测试守着各自那份。三重结构之后，这个值只在一份声明文件里存在：散文指路径，引擎读声明，改一处、跑一次校验器，双面同时更新且不可能漂移。

**Why this priority**: 这是「两层 → 三层」的原始痛点。没有它，后面所有条款都只是格式偏好；有它，特性立刻兑现可验证的价值。

**Independent Test**: 在只改一份声明文件的前提下运行声明校验器与相关引擎契约测试，断言引擎读到的值等于新值、正文中该旧值字面量命中数为 0（重复字面量判定复用既有 `doc-consistency-check.py` 的 `duplicate` 面，见 FR-010）。

**Acceptance Scenarios**:

1. **Given** 一条已迁入声明层的事实（例如 feedback 提示阈值），**When** 只把声明文件里的值改成新值并运行声明校验器与引擎契约测试，**Then** 校验器退出 0，引擎读到新值，且 markdown 载体中该值字面量的重复命中为 0（不得两边各改一次才对得上）。
2. **Given** markdown 载体仍复述着该事实的旧值，**When** 运行声明校验器，**Then** 输出带该事实与载体路径的重复字面量原因（[[STR-011]]）并以退出码 1 结束，MUST NOT 静默通过。
3. **Given** 一个引擎仍然硬编码了已被声明的事实值，**When** 运行声明校验器，**Then** 该引擎被报为未读取方（三层缺层原因 [[STR-009]]），即使声明文件本身完全合法。

---

### User Story 2 - 封闭集与映射被门禁读取，而不是被脚本抄一份 (Priority: P1)

一条封闭集（流程类别、证据七态、状态取值、检查项名）今天写在散文 owner 里，同时被某个引擎以元组常量再抄一遍。两者的漂移只有靠人发现。三重结构之后，封闭集只在声明层存在一份，散文 owner 保留判据、丢掉取值表，引擎从声明层读，门禁的拒绝理由逐字来自同一份取值域。

**Why this priority**: 封闭集漂移是本仓已经发生过的缺陷类型（多份取值域各自漂移会直接让门禁放行或误杀），风险高于单纯的文档重复。

**Independent Test**: 对每个已迁封闭集，构造一个含越界取值的负夹具：引擎以封闭理由集拒绝（退出码非 0、理由逐字）、散文 owner 内搜不到该取值表的第二份。

**Acceptance Scenarios**:

1. **Given** 封闭集（如流程类别二值、证据七态）已在声明层声明，**When** 在载体中输入一个越界取值并运行对应门禁，**Then** 门禁以既有封闭理由集拒绝，且该理由的字面量与声明层的取值域同源（不是门禁里另写的第二份）。
2. **Given** 某个声明层的封闭集新增一个合法取值，**When** 只改声明文件，**Then** 该门禁立刻接受新取值且无需改脚本；若门禁仍拒绝，则说明脚本仍有第二份取值域，FR-007 判定为未完成。
3. **Given** 散文 owner 与声明层对同一封闭集给出不同成员，**When** 运行声明校验器，**Then** 报双重定义并退出 1，MUST NOT 以「散文优先」或「代码优先」的隐式规则平息。

---

### User Story 3 - 新增 harness 流程时三层结构被强制，未被排除的也说得清 (Priority: P2)

贡献者新增一个会产生证据记录或 feedback 记录的命令。今天他可以只写 markdown + 脚本就合入，三层结构靠评审记性。三重结构之后，覆盖判定会在候选集上重算出这个新单元，它要么被声明（三层齐备才算完成），要么被排除（理由取封闭集且必须携带可解析锚点）；两者都没有，判定失败并点名该单元。

**Why this priority**: 它决定这条纪律一年后是否还成立。没有它，三层结构只在迁移那一天存在。

**Independent Test**: 在临时夹具上加一个带引擎引用的新命令目录，运行覆盖判定，断言它出现在「未归类候选」里并被点名；补一份声明或一份排除记录后判定转绿。

**Acceptance Scenarios**:

1. **Given** 一个新命令的载体引用了某个框架引擎而声明层没有它的任何记录，**When** 运行覆盖判定，**Then** 以 [[STR-013]] 点名该单元并退出 1。
2. **Given** 一个候选单元被判为不在范围内，**When** 运行覆盖判定，**Then** 它必须有一份排除记录，理由取封闭三值之一，且锚点在树内可解析（不可解析报 [[STR-012]]）。
3. **Given** 两个并行分支各新增一条事实声明，**When** 两个分支分别合入，**Then** 两次写入落在不同路径，无冲突，且覆盖判定在两种树上都退出 0。

---

### User Story 4 - 不属于 harness 的流程完全不受影响 (Priority: P2)

大多数命令与技能既不产出 harness 资产，也没有需要机器判定的取值域。它们今天的两层结构继续合法，不需要声明文件、不需要新章节、不需要改一行散文。排除理由必须说得出来并且能在仓库里指到证据。

**Why this priority**: 一个「所有流程都要加一层」的读法会制造大量空声明文件并让纪律变成仪式。把边界写成可判定，是这个特性能否长期维护的前提。

**Independent Test**: 随机抽取若干明确与 harness 无关的技能（制图、项目摘要、访谈），断言它们没有任何声明文件且覆盖判定对它们零报错；再断言它们的排除记录理由与锚点均可解析。

**Acceptance Scenarios**:

1. **Given** 一个既不产出 harness 资产、也没有机器消费取值域的技能，**When** 运行覆盖判定，**Then** 它必须在 [[STR-007]]（无 harness 资产）或 [[STR-006]]（无机器消费事实）下有一条排除记录，且判定不因它而失败。
2. **Given** 一个既有两层结构的单元尚未迁移，**When** 运行覆盖判定，**Then** 它以完整性状态 [[STR-005]] 出现而不是报错；迁移完成后同一条判定转 [[STR-004]]。
3. **Given** 一个技能有自带的 YAML 输入模板（例如结构化入参模板），**When** 运行覆盖判定，**Then** 该模板 MUST NOT 被误判为声明层事实——判定只认 [[STR-001]] 下的声明文件。

### Edge Cases

- **载体被删除或重命名**：声明里引用的载体路径失效。判定 MUST 报未解析的载体引用并退出 1；MUST NOT 把失效引用当作「已不再适用」自动清除。
- **一条事实被两份声明各自声称拥有**：判定 MUST 报双重声明并退出 1。MUST NOT 用文件名字母序或修改时间选一个当赢家。
- **声明使用了子集外的 YAML 构造**（anchor、tag、多文档、块标量）：判定 MUST 以 [[STR-010]] 拒绝，且 MUST NOT 尽力解析后「差不多能用」。
- **声明文件合法但没有任何引擎读取它**：这是最危险的假绿形态——文件存在即被读作「已三层化」。判定 MUST 以 [[STR-009]] 报三层缺层，不因文件存在而转绿。
- **两个面的取值本来就不一致（迁移前已漂移）**：迁移 MUST 按权威顺序（代码 > 生成物 > 作者文档）取一个暂定值并在声明里记明该次修正；MUST NOT 任选一面对齐另一面而不留记录。
- **旧客户项目缺少 [[STR-002]]**：引擎 MUST 降级为「未接线」并显式标注，MUST NOT 抛异常中断消费流程；降级状态 MUST NOT 被读作通过。
- **`.specify/` 运行时副本与框架源不一致**：镜像差异由既有 `sync-mirrors.py --check` 判，本特性 MUST NOT 另造镜像比对。
- **候选屏幕的边界样本**：一个技能只在散文里提到脚本路径、实际并不调用它。屏幕按文本判定会把它算作候选；这是可接受的保守侧，处置为一条排除记录（理由 [[STR-006]]），MUST NOT 为此发明第二套「是否真的调用」的语义判定。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: MUST 新建 `shared/definitions/harness-triple-definitions.md`（框架源 `shared/`，经镜像投影到 `.specify/shared/`）作为本特性的**唯一 owner**，拥有六件事：① 三层各自拥有什么；② 「归 yaml 的事实」判据（FR-006 的正文）；③ 候选屏幕定义（FR-004 的正文）；④ 范围判据（FR-002 的正文）与三个排除理由的**语义**；⑤ 迁移时的权威取值顺序；⑥ 非目标。其他任何位置（命令模板、技能、宪章、指令、契约、测试、门户文档）MUST 以「路径 + 章节锚」引用本文件，MUST NOT 复制其判据句、取值表或理由词义。**三层各自拥有什么**（本行的枚举即该判据的摘要，完整正文在上述 owner）：markdown 拥有「为什么 + 怎么读」——义务、判定顺序、边界叙事，以及指向声明层的指针；yaml 拥有「机器读得到的取值」——阈值、封闭集、有序算子表、映射、记录 schema；script 拥有「确定性执行与判决」——读声明、施加、给退出码，且 MUST NOT 把 yaml 拥有的值再写成一份内联常量。
- **FR-002**: 范围判据 MUST 为两条**合取**且可判定：**(D1) 资产面**——该流程单元的验收交付物包含至少一件由 `shared/guidelines/better-harness.md` § 消费者清单 点名的 harness 资产，且能指认落点，取以下四者之一：(a) 证据记录、(b) feedback／学习记录、(c) 对他人产物的门禁 verdict、(d) 对 `skills/`、`agents/`、`teams/`、`tools/`、`docs/`、宪法或指令的改动；**(D2) 机器面**——该单元至少有一条按 FR-006 判据归属 yaml 的事实。不满足 D1 或 D2 的单元 MUST 有一条排除记录，理由取封闭三值 [[STR-006]]（无机器消费事实）／[[STR-007]]（无 harness 资产）／[[STR-008]]（由上级 owner 显式保留为两层，且 MUST 携带可解析锚点）。三个字面量的取值域由 FR-003 的契约拥有，其语义由 FR-001 的文档拥有；本行不复述语义。
- **FR-003**: [[STR-001]]`contract.yaml` MUST 是下列**机器读取取值**的唯一 owner：五类 fact kind 的封闭集（阈值／封闭集／有序算子表／映射／记录 schema）、完整性状态二值 [[STR-004]] 与 [[STR-005]]、排除理由三值 [[STR-006]]／[[STR-007]]／[[STR-008]]、引擎三退出码（0／1／2）的语义、允许的 YAML 子集标识、声明文件的必填键集、以及本引擎的门禁调用点清单。markdown owner MUST 引用本文件、MUST NOT 再列一份；任何脚本 MUST 经 FR-009 的共享读取入口取这些取值。**理由**：本特性的核心失效是「同一事实两处各写一份」，因此承载封闭集的契约自身 MUST NOT 成为第二处。
- **FR-004**: MUST 定义**候选屏幕 S**（正文归 FR-001 的文档）：一个流程单元的 markdown 载体——`templates/commands/*.md`、`skills/{external,internal}/*/SKILL.md`、`shared/workflow/*.md`——的文本中出现至少一处指向框架内确定性引擎的路径引用（`scripts/python/<name>.py` 或 `skills/<layer>/<name>/scripts/<file>`），即进入候选集。S MUST 由 [[STR-003]] 在树上重算，MUST NOT 以任何手写候选清单代替。`shared/definitions/*.md` **不属于流程单元**、MUST NOT 进入候选集：它们是事实的散文 owner，其事实归属由 FR-006 判定，本身不做 in／out 处置。
- **FR-005**: 声明形态 MUST 为「一文一件、路径即身份」。**in-scope 事实**逐条落 [[STR-001]]`facts/<fact-slug>.yaml`，一条事实一个文件，`<fact-slug>` 即该事实的 grounded 身份（kebab-case，MUST NOT 另起编号命名空间）。必填键：`fact`（与文件名一致的 slug）、`kind`（取 FR-003 的封闭集）、`statement`（机器可读值：标量、序列或映射）、`consumers`（必须读取该事实的引擎路径与载体路径）、`former_carriers`（迁移前写下过该事实的载体路径，用于回修与残留扫描）与可选的 `note`（人读说明）。`consumers` 与 `former_carriers` MUST NOT 混用：前者是「必须读它」，后者是「曾抄过它、现在必须是指针」。`consumers` MUST 至少包含**一个引擎**（`scripts/python/<name>.py` 或 `skills/<layer>/<name>/scripts/<file>` 这类确定性程序，而非只有载体）；一条只列载体的声明是 **schema 错误**（按本行的必填键与 FR-003 的 schema 校验拒绝），MUST NOT 被容忍为一条永久 [[STR-005]]——否则 FR-007 (c) 的「至少一个引擎确实读取」永不可能成立。**排除记录**落 [[STR-001]]`exclusions/<reason>.yaml`，按理由一词一文件，每行 `unit`／`carrier`／`anchor` 三键齐备；锚点 MUST 在树内可解析，不可解析即报 [[STR-012]]。
- **FR-006**: **「归 yaml」判据 = 机器消费 ∧ 跨面**，两条合取：(i) **机器消费**——存在至少一个确定性引擎**必须读取该值才能作出判定**，且该判定结果随取值改变而改变（读常量作比较、比对封闭集、按表选门、按 schema 校验）；一个只被测试钉住、却没有任何引擎读它作判决的字面量（例如某个检查器的标签名）**不构成机器消费**；(ii) **跨面**——该事实至少跨两个面出现（面 = 引擎、markdown 载体、模板、被测试钉住的字面量）。任一不成立即留在原处：引擎内部常量留引擎，读者独有说明留 markdown。**重复出现不是判据**（重复只是该迁移的征兆）；**介质不是判据**。迁移时若各面取值已漂移，MUST 按权威顺序（代码 > 生成物 > 作者文档）取暂定值并在该声明 `note` 记明该次修正，MUST NOT 静默对齐任一侧。**(i) 的收窄由 clarify 裁定（A2，2026-11-05）**：原读法把「有测试钉住」也算机器消费，会让无判决消费者的标签集进入声明层并制造噪声；收窄后判据对每个候选事实给出可判定答案。
- **FR-007**: 每个 in-scope 单元的完整性状态 MUST 为二值且可判定：[[STR-004]] 当且仅当三条件**合取**成立——(a) 该单元的每条事实在 [[STR-001]] 有且仅有一份声明且通过 schema 校验；(b) 该单元的 markdown 载体含指向该事实的指针（声明路径 + 键路径）且不再规范性重述其值——机械判定为既有 `doc-consistency-check.py` 的 `duplicate` 面对该事实零命中；**该判定的调用形态是固定的**：`python3 scripts/python/doc-consistency-check.py --action verify --faces duplicate --spec-dir <spec 目录>`。该面**没有**逐事实选择器，且其读数随传入的 owner 路径而变，故 MUST 逐字使用此形态、MUST NOT 假设可以只扫一条事实、MUST NOT 换用自造变体；**逐事实归因**取自该次运行输出的原因 [[STR-011]]（实例形态 `duplicated-fact-literal: <fact>@<path>` 自带事实 slug 与载体路径），单事实投影用 [[STR-003]] `--action lookup --fact <fact-slug>` 读取。「复用既有面」与「逐事实计数」因此不冲突：面只判「是否被复制」，原因与 `lookup` 负责把命中归到哪条事实；(c) `consumers` 中至少一个引擎**确实读取**该事实（读取点在源码中可定位）。任一不满足 MUST 为 [[STR-005]]，并以封闭原因集点名，缺层报 [[STR-009]]。**假绿红线**：声明文件存在本身 MUST NOT 被读作已三层化——(c) 未成立时即使 (a)(b) 全绿，状态仍为 [[STR-005]]。
- **FR-008**: 声明文件 MUST 只使用 YAML 子集：块映射、块序列、标量（含引号字符串）、注释、2 空格缩进；`[]`／`{}` 仅允许作为空值出现。MUST NOT 使用 anchor／alias、显式 tag、多文档、块标量（`|`、`>`）与任何 flow collection。子集标识由 FR-003 的契约拥有。违反 MUST 以 [[STR-010]] 拒绝，且 MUST NOT 尽力解析后「差不多能用」。
- **FR-009**: MUST 提供一个 **stdlib-only 的共享读取入口**，供 [[STR-003]] 与全部 `consumers` 引擎共用；引擎 MUST 经该入口读取声明，MUST NOT 各自实现解析器。`pyproject.toml` 的 `dependencies` MUST NOT 新增任何 YAML 库，**相对基线**逐字节不变。**基线的参照物在此点名，不在判据内重新推导**：基线 = T001 采集进 `.specify/specs/084-harness-triple-structure/notes/pre-change-measurements.md` 的该条读数（`git diff --name-only <实现起点> -- pyproject.toml` 为空，其 plan 侧同形态先例是 `plan.md` EP-003 的 `git diff --stat 171c2ff8 -- …`）；判据只与该次捕获的读数比较。
- **FR-010**: [[STR-003]] MUST 只判定**声明完整性**（解析、必填键、子集、覆盖与归类、双向一致、残留字面量），MUST NOT 重判既有门禁已拥有的判据。**「既有门禁脚本」的枚举只有本行一处**（本行即其唯一 owner；FR-019、N5、SC-006 与 SC-006 Source 一律按名字引用本行，MUST NOT 再列第二份），并且该枚举**必须按两个角色分开读，两个角色不是同一个集合**：**（一）不得重判侧（六脚本）** = `scripts/python/validate-requirements.py`、`scripts/python/validate-tasks.py`、`scripts/python/gate-check.py`、`scripts/python/flow-class-check.py`、`scripts/python/closure-acceptance-check.py`、`scripts/python/doc-consistency-check.py`——[[STR-003]] MUST NOT 重判它们已拥有的判据，本特性 MUST NOT 改变它们的判据与退出码契约；其中 `doc-consistency-check.py` 是被**复用**的一方（其 `duplicate` 面按 FR-007 (b) 的既定调用形态直接使用），它的面清单以该脚本 `--help` 为 owner，本行不复述也不新增第二套面。**该六元集与 plan C-032 的关系在此点名，避免变成两处计数**：C-032 的重判清单是其中五处（`validate-requirements.py`、`validate-tasks.py`、`gate-check.py`、`flow-class-check.py`、`doc-consistency-check.py`），本行多出的第六处 `closure-acceptance-check.py` 由 SC-006 与 A8(a) 带入，本特性对它承担的是**不得改动**义务（081 的验收面，判据在 FR-018 的硬约束里），不是「允许重判」——集合是 C-032 的超集，不是另一份清单。**（二）零 diff 侧（五脚本）** = 上述六脚本中除去 `doc-consistency-check.py` 后的封闭五元集——这五个脚本的既有测试 MUST 新增失败 0、既有测试文件 MUST 零改动（SC-006 的判据即该侧；`doc-consistency-check.py` 不入该侧，因为本特性对它是复用既有面、新增的是夹具与调用，不是重写它的既有测试）。**两侧不许混读**：`doc-consistency-check.py` 在不得重判侧、不在零 diff 侧；`closure-acceptance-check.py` 两侧都在。重复字面量判定 MUST 复用 `doc-consistency-check.py` 的 `duplicate` 面（调用形态与逐事实归因由 FR-007 (b) 拥有，本行不复述），MUST NOT 新建扫描器。调用点 MUST 挂在既有门宿主上（`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` 与契约测试），MUST NOT 新增并行门禁阶段，MUST NOT 改变既有门禁的退出码契约。
- **FR-011**: 迁移 MUST 分三批且每批**独立可验收**：(批 1) 今天已跨面重复的封闭集与阈值——漂移风险已存在；(批 2) 被门禁消费的映射与有序算子表——决定放行与误杀；(批 3) 记录 schema——只影响证据形态。每批完成时 [[STR-003]] MUST 对该批 0 报错、对未迁单元 0 误红。首批名单与批次切分属 plan 口径，本阶段只钉顺序与「每批独立可验收」。
- **FR-012**: **兼容性 MUST NOT 变成永久态**。迁移期内未迁单元的两层结构 MUST 继续可用；引擎读取声明 MUST 单一来源——声明存在 ⇒ 该引擎的内联值 MUST 被删除（MUST NOT 双读）；声明缺席 ⇒ 允许沿用内联值，但 MUST 在输出中以 [[STR-014]] 显式标注，MUST NOT 静默沿用。`former_carriers` 中的残留字面量由 FR-007 (b) 的零命中守住。本特性关闭时 in-scope 集合内 [[STR-005]] MUST 为 0（见 SC-002）。
- **FR-013**: Two Hats：所有新增与变更 MUST 落**框架源**（`shared/`、`scripts/`、`templates/`、`skills/`、`src/`），`.specify/` 是运行时副本、MUST NOT 手改。镜像 MUST 由既有 `sync-mirrors.py` 生成（`shared → .specify/shared` 已在 `MIRROR_PAIRS` 中），MUST NOT 另造镜像机制或第二套比对。`specify init` MUST 把 [[STR-001]] 分发到客户项目；旧项目缺 [[STR-002]] 时引擎 MUST 降级为「未接线」并显式标注，MUST NOT 抛异常中断消费流程，且降级 MUST NOT 被读作通过。**降级标注的文本是自由的、只判机械项（本轮裁定并披露）**：exit 2 的降级标注 MUST NOT 登记为 Shared String，也 MUST NOT 进 FR-017 的封闭原因集（plan 决策 D7：它是输入错误，不是第七个 finding）；夹具 MUST 只机械判定三件事——退出码为 2、标注文本非空且点名缺失目录 [[STR-002]]、既不抛异常也不打印 traceback；标注的**措辞本身** MUST NOT 被逐字断言。
- **FR-014**: Directory Governance：[[STR-001]]、其 `facts/` 与 `exclusions/` 子目录 MUST 在**同一变更内**登记含义到 `shared/definitions/framework-map.md`；命名 MUST 符合 kebab-case（`^[a-z0-9]+(-[a-z0-9]+)*$`）；MUST NOT 新建顶层目录；MUST NOT 创建聚合 ledger 文件——单元处置由声明反投影派生（派生索引即读即建）。
- **FR-015**: 并发安全：新增存储 MUST 一文一件（一条事实一个文件）；单元处置 MUST 由声明反投影派生、MUST NOT 手工总表。MUST 附**双写者测试**：模拟两个并行分支各新增一条事实声明，断言写入路径不同、覆盖判定在两种树上均退出 0。排除记录按理由分文件（至多三份）是允许的单一所有者状态，但其冲突面 MUST 在测试中被承认：新增单元只追加一行，MUST NOT 重排既有行。
- **FR-016**: [[STR-003]] MUST 支持 `--action coverage`／`verify`／`lookup` 三动作；退出码 0／1／2 的语义由 FR-003 的契约拥有；MUST 只读（无任何写入点）、stdlib-only、不含模型判断。`--action lookup --unit-id <unit>` MUST 输出该单元的处置与事实摘要，供消费流程直接使用而不必读原始声明。**确定性 MUST 覆盖三个动作**（plan C-038 在需求侧的收口；SC-001 (i) 只是 `coverage` 上的读数实例）：同一棵树、同一份声明集下，`coverage`／`verify`／`lookup` 各自两次运行输出逐字节一致，MUST NOT 只对 `coverage` 要求确定而把其余两个留成未定的口径。
- **FR-017**: 失败 MUST **只**以封闭原因集逐字输出：[[STR-009]]、[[STR-010]]、[[STR-011]]、[[STR-012]]、[[STR-013]]、[[STR-014]]；占位符替换后逐字发射，MUST NOT 输出自由文本判读。exit 2 的输入错误与降级标注**不是 finding**、不在本封闭集内（其唯一判据见 FR-013），因此「六原因」与「exit-2 标注」不构成第七个成员。每个原因 MUST 有一份负夹具（构造该失效并断言退出码与逐字原因）与对应正夹具（断言 0 误报）。
- **FR-018**: 受影响 owner 文档 MUST 在同一变更内把取值表改为**指针 + 判据保留**。**集合由一条收口规则定义，不含开放量词**：受影响 owner 文档 = `contracts/migration-batches.contract.md` C-042／C-044／C-045 点名的全部 carrier **∪** 每个 in-scope fact 的每个 markdown carrier（即其 `former_carriers` 中属于 markdown 载体或散文 owner 的每一项）。该并集即全集：不在并集中的 carrier 没有被本特性改写的义务，「是不是漏了一份 owner 文档」只需问「它在不在这个并集里」，不需要再做一次范围判断。下列五处是本阶段已点名的实例（**举例，不是第二份枚举**；枚举 owner 是上述并集）：`shared/guidelines/better-harness.md` § 证据纪律 第 2 条（七态枚举）、`shared/definitions/flow-class-definitions.md`（类别／basis／文档类型取值、台账列）、`shared/workflow/feedback-step.md`（提示阈值默认值）、`shared/workflow/expression-gates.md`（阶段算子表与六面）、`shared/workflow/acceptance-hardening.md` § Closure Verdict（`Path` 取值二值，见 A8(a)）。**081 已验收契约的迁移边界（clarify 裁定 A8(a) 的硬约束）**：对 `acceptance-hardening.md` 的改动 MUST 只把取值集移入 [[STR-001]] 并留下指针，判定散文、拒绝消息模板、退出码语义与 `final`/`supporting` 的成员集合 MUST 逐字不变；`tests/contract/test_requirements_checker.py` 与 `tests/contract/test_checker_form.py` 的既有断言 MUST 零改动，新增失败 MUST 为 0（该断言集是 081 的验收面，不是本特性可重写的东西）。`docs/` 侧入口 MUST 按 `docs/concepts/documentation-model.md` 登记且只放指针；`CHANGELOG.md` MUST 记一条。
- **FR-019**: MUST 新增 `tests/contract/test_harness_triple_structure.py`（覆盖契约、双写者、子集拒绝、六个原因逐字、覆盖判定三态）与正负夹具目录 `tests/fixtures/harness-triple-structure/`（按既有约定一特性一目录）。该测试模块 MUST 另含一条**单一子集解析器守卫腿**，即 `contracts/shared-reader.contract.md` C-058 在需求层的验收面：机械断言 `scripts/` 与 `skills/` 下只有 FR-009 的共享读取入口实现子集解析，两份祖父解析器（`scripts/python/execution-config.py` 的 `parse_yaml_subset`、`scripts/python/gate-check.py` 的 `parse_gate`）由显式 allowlist 豁免（理由 = N4），断言形态是搜索而非语义评审。FR-010 的**「零 diff 侧」五脚本**（枚举见 FR-010，本行不复述）MUST 保持既有测试零新增失败。

### Key Entities *(include if requirement involves data)*

- **事实声明 (Fact Declaration)**：`.yaml` 一件，代表一条归 yaml 的事实。标识 = 其文件路径（`facts/<fact-slug>.yaml`）加上在文件内的键路径；没有第二套编号。属性：`kind`（五类之一）、`statement`（机器可读值）、`consumers`（必须读它的一方）、`former_carriers`（曾抄过它的载体）。关系：一条事实可被多个单元消费；一条事实 MUST 属于且仅属于一份声明。
- **层契约 (Layer Contract)**：`contract.yaml` 一件。拥有五类 kind、二值完整性状态、三值排除理由、三退出码、子集标识、声明必填键集与门禁调用点。它是本特性唯一允许的「聚合」文件，因为它是取值域而非处理状态。
- **排除记录 (Exclusion Record)**：按理由分文件的一条行记录，把某个候选单元判出范围。属性：`unit`、`carrier`、`anchor`——**三键齐备，`reason` 不在属性表内：它由文件名承载**（落地为 `exclusions/<reason>.yaml`，取值取 FR-003 的封闭三值，MUST NOT 在行内再写一份）。关系：一个候选单元 MUST 有且仅有一条处置记录（一条事实声明把它列为 `consumers`，或一条排除行点名它）。
- **流程单元 (Flow Unit)**：候选屏幕 S 的判定对象，以 markdown 载体路径为身份（命令模板、技能 SKILL.md、工作流步骤文档）。关系：单元的处置由其事实声明与排除记录共同派生，MUST NOT 另行存储。
- **三层完整性状态 (Layer Completeness State)**：派生量，二值。不是存储的事实，MUST NOT 被写成手工字段。

### Runtime Stack & Dependency Ownership

本特性自身的运行时栈与依赖所有权表（`execution` 类必填；`Premises` 指向 plan 阶段将定义的执行前提）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | Python 3 解释器（运行 stdlib-only 共享读取入口与 `harness-triple-check.py`） | signed-contract | CPython 上游（本仓只消费） | `requires-python >= "3.8"`（`pyproject.toml` 已声明；新脚本 stdlib-only，无第三方 import） | `pyproject.toml` | 共享读取入口与 checker 在 `>=3.8` 解释器上通过正／负夹具；静态 import 清单为空 | FR-009, FR-016 | EP-001 |
| RS-002 | pytest（契约／单元测试运行器） | signed-contract | pytest 上游（本仓只消费） | `pytest 9.2.0`（2026-11-05 实测 `python3 -m pytest --version`；基线比较前须重新核对） | `scripts/bash/run-tests.sh` | `tests/contract/test_harness_triple_structure.py` 在基线／closure 同一 pin 上全绿，既有测试零新增失败 | FR-019 | EP-001 |
| RS-003 | `specify init`（把 `shared/declarations/` 分发到客户项目） | in-scope | 本仓 `src/` 与 `scripts/` | 仓内 commit（本特性同一提交） | `src/specify_cli/__init__.py` | 在临时夹具执行 `specify init` 后 `.specify/shared/declarations/` 存在，且 `harness-triple-check.py --action lookup` 可读取 | FR-013 | EP-001 |

## Initial Scope Adjudication（日期基线，不是 owner）

**本表的性质**：这是 requirements 阶段按 FR-002 两条判据对代表单元作出的**逐条裁决记录**（dated record）。它 MUST NOT 充当范围的 owner——owner 是 FR-002 的判据加 FR-005 的声明形态，完整范围由 [[STR-003]] 在 plan 阶段首次运行 `--action coverage` 重算并落在证据目录。本表的作用是证明判据可判：每一行都指到仓内证据，没有一个单元落在「相关」「等等」之下。

| 单元（markdown 载体） | 引擎 | D1 资产面 | D2 待迁事实（今天的两处副本） | 处置 |
|---|---|---|---|---|
| `shared/workflow/feedback-step.md`（feedback 回路与 Run Determination） | `feedback-utils.py`、`run-determination.py` | (b) feedback 记录 | 提示阈值默认值：`feedback-utils.py` `DEFAULT_THRESHOLD = 10` ↔ `feedback-step.md` § 阈值协议「defaults to `10`」 | in-scope（批 1） |
| `shared/workflow/evidence-step.md` + `skills/internal/collect-evidence/SKILL.md` | `evidence-utils.py` | (a) 证据记录 | 七态封闭集：`evidence-utils.py` `SEVEN_STATES` ↔ `evidence-discipline.md` ↔ `better-harness.md` § 证据纪律 第 2 条；五泳道：`LANE_NAMES` ↔ 消费点散文 | in-scope（批 1） |
| `shared/definitions/flow-class-definitions.md`（事实 owner；本身不是流程单元） | `flow-class-check.py` | (c) 门禁 verdict | 类别二值 `CLASS_VALUES`、basis 三值 `BASIS_VALUES`、文档类型封闭集 `FLOW_TYPE_VALUES`、台账必需列 `REQUIRED_LEDGER_COLUMNS`、类中立类别 `NEUTRAL_CATEGORIES` —— 每一项在散文 owner 与脚本常量各写一次 | in-scope（批 1；载体只保留判据与指针） |
| `shared/workflow/expression-gates.md` | `flow-class-check.py`、`doc-consistency-check.py` | (c) 门禁 verdict | 六面封闭集、阶段算子表（阶段 × 算子 id × 执行算子 × 对应面 × 阻断级别）：散文表头被 `flow-class-check.py` 以 `required = ("阶段", …, "阻断级别")` 再写一次 | in-scope（批 2） |
| `templates/commands/analyze.md` + `skills/internal/analyze-artifacts/SKILL.md` | `validate-*.py`、`flow-class-check.py` | (c) 门禁 verdict | 严重度取值域与 F 通道封闭集：**实测无引擎读取点**（原写「分析侧 owner 与判定引擎各一份」，2026-11-05 路径 A 复核订正为不可成立），两条事实按 FR-006 (i) 不成立而移出，载体保留原样。锚点：`skills/internal/analyze-artifacts/references/detection-and-severity.md` § Severity assignment、§ The eight passes；读数 `test-evidence/analyze-report-round2-2026-11-05.md` § R2-02 与 `contracts/migration-batches.contract.md` § Facts outside the roster（`no-machine-fact`） | excluded [[STR-006]] (no-machine-fact) |
| `templates/commands/review.md` + `skills/internal/review-sdd-process/SKILL.md` | 同上 | (c) 门禁 verdict | 组合段序列（过程／产物／实现／代码）**移出**（无引擎读取点，2026-11-05 路径 A；锚点：`templates/review-template.md` § 2.1–2.4、`shared/workflow/acceptance-hardening.md` § Review Composition）；ARC 判定**保留** in-scope——引擎侧 `scripts/python/closure-acceptance-check.py` 的 `final_path_counts()` 与 `verdict`，载体 `templates/review-template.md` § 2.4 与 `templates/commands/review.md` § 2.4 拷贝段 | in-scope（批 2；仅 ARC 判定） |
| `shared/workflow/self-improvement-workflow.md` + `shared/definitions/self-improvement-definitions.md` + `skills/internal/self-improvement/SKILL.md` | 复用 evidence／feedback 引擎 | (a)(b) 两件 | SI 阶段序列与「轨道 → 执行者」映射（Bootstrap／Operationalize／Optimize）：**实测无引擎读取点**（三个阶段名在 `.py`／`.sh` 零命中；原写「工作流散文与改进技能族各一份」，2026-11-05 路径 A 复核订正），两条事实移出，载体保留。锚点：`shared/workflow/self-improvement-workflow.md` § Standard Flow、§ SI-4 Route to the Canonical Improver；`shared/definitions/self-improvement-definitions.md` § Self-Improvement Loop | excluded [[STR-006]] (no-machine-fact) |
| `skills/internal/memory-record/SKILL.md` + `memory-recall/` | `memory-utils.py` | (b) 学习记录 | 记忆类型封闭集（session／knowledge）与保留策略阈值 | in-scope（批 3） |
| `skills/internal/manage-history/SKILL.md` | `history-utils.py` | (b) 学习记录 | 增量 manifest 记录 schema **保留**（引擎 `history-utils.py` 的 `_manifest_path()`／`read_manifest()`／`write_manifest()` 与 `sessions` 键集）；分类封闭集（decisions／lessons／TODOs／flows／conflicts）**移出**——五个分类名在 `.py`／`.sh` 零命中，无引擎读取点（2026-11-05 路径 A；锚点：本 SKILL § Step 3 Distill、§ Step 4 Theme Aggregation） | in-scope（批 3；仅 `history-manifest-schema`） |
| `skills/internal/improve-agent/`、`improve-team/`、`improve-tools/`、`skills/external/improve-docs/`、`improve-skills/` | 各技能内脚本 | (d) 改 harness 资产 | 改进轨道三值与「被改动资产类别」映射：**实测无引擎读取点**（improve-\* 技能脚本 `redline-check.py`／`skill-shape.py` 无轨道词表；原写「一份」无实测支撑，2026-11-05 路径 A 复核订正），两条事实移出，五个载体保留。锚点：各 SKILL § Target Classification | excluded [[STR-006]] (no-machine-fact) |
| `skills/external/sdd-loop-driver/SKILL.md` | 同目录 `scripts/`（含 `pre-analyze-check.py`） | (c) 门禁 verdict | 阶段序列、门禁清单、完成哨兵字面量、`STAGE_ARTIFACTS` 名册（今天靠静态解析另一文件的赋值） | in-scope（批 2） |
| probe 载体（`shared/definitions/probe-definitions.md` 及其执行面） | `probe-utils.py`、`exec-quant.py`、`trigger-utils.py` | (c)(b) 两件 | Probe Class × Object／Binding 封闭集、量化记录 schema、触发词状态 schema | in-scope（批 3） |
| `templates/commands/requirements.md` + `skills/internal/create-requirements/SKILL.md` | `validate-requirements.py` | (c) 门禁 verdict | `Path` 取值二值：判据散文在 `acceptance-hardening.md` § Closure Verdict，取值在 `validate-requirements.py:98 PATH_VALUES` 与 `closure-acceptance-check.py:505` 各写一次 —— **取值迁 yaml、判据留原 owner**（A8(a) clarify 裁定：不越界，保留 in-scope）。六个检查项标签集**不迁**（A8(b) 裁定：越界；理由与锚点见 N7） | in-scope（批 1） |
| `shared/guidelines/better-harness.md`（事实 owner 与目标锚点） | 无 | (a)(d) 作为 D1 判据 source | 五维表：**无引擎读取** → 不迁，继续是维度名 owner；其内的七态枚举按 A7 迁为指针 | carrier-only（不建自己的声明文件） |
| `skills/external/draw-diagram/` | 同目录 `scripts/` | 无（作图产物不是 harness 资产） | — | excluded [[STR-007]] |
| `skills/external/database-utils/` | 同目录 `scripts/` | 无 | — | excluded [[STR-007]] |
| `skills/internal/summarize-project/` | 同目录 `scripts/` + 结构化入参模板 | 无 | 自带 `.yaml` 入参模板，但那是**输入模板**而非机器判定取值（边界样本，见 Edge Cases 末条） | excluded [[STR-006]] |
| `skills/external/humanize/` | 同目录 `scripts/` | 无 | 改写散文，无任何引擎须读取的取值域 | excluded [[STR-006]] |

**2026-11-05 路径 A 复核（date record，不是第二份 owner）**：analyze round 2 把「8 条 `engine side = none` 的事实仍留在迁移名册」判为 HIGH（`test-evidence/analyze-report-round2-2026-11-05.md` § R2-02），用户裁定路径 A——这 8 条按 [[STR-006]] 移出 in-scope，理由是**今日树上**不成立（FR-006 (i)：不存在判决随该取值改变的确定性引擎；「迁移时创建读取点」这一读法被 A2 的收窄排除，否则判据自我证成）。同步面同一趟落地：`contracts/migration-batches.contract.md` 的 C-044／C-045 名册（条款总数仍 59，`C-001`…`C-059` 不变）新增 § Facts outside the roster（`no-machine-fact`）逐条记录 8 条事实、其单元、载体与锚点；`tasks.md` 的 T015／T016 收缩（任务总数仍 31）。

本表因此**有 3 行**改判 `excluded [[STR-006]] (no-machine-fact)`（analyze、self-improvement、improve）；另 **2 行**（review、manage-history）**保持 in-scope**，因为它们各留下一条仍被引擎消费的事实（`ARC verdict mapping` → `scripts/python/closure-acceptance-check.py`；`history-manifest-schema` → `scripts/python/history-utils.py`）——把这两行判出范围会制造「同一单元既被一条声明覆盖、又被一条排除行点名」这一 FR-002 与 `data-model.md` E-2 **R-4** 明令禁止的状态（E-5 把该矛盾判为 finding，而不是按文件顺序化解）。8 条事实落 8 个排除单元（2 analyze + 1 self-improvement + 5 improve），故 `shared/declarations/exclusions/no-machine-fact.yaml` 写 8 行；`review-segment-sequence` 与 `history-categories` 所在的单元组仍持有 in-scope 事实，因此不产生排除行，其「未迁移」由本节与迁移契约的那张表记录。两者都是读数：实现阶段先用屏幕 S 与锚点 `grep` 复测再落文件。FR 正文与编号、`Flow Class`、`Path` 均未改动。

## Non-Goals（非目标，每条给判据 owner）

- **N1 不引入配置系统、不引入 YAML 库、不做运行时求值**。声明层只被确定性引擎读取，不被求值、不做表达式、不做继承与覆盖层。判据：FR-008、FR-009；越界信号 = `pyproject.toml` 依赖变化或声明里出现非标量/非集合构造。
- **N2 不建第二套门禁、不做 yaml → markdown 渲染**。渲染会创造第二份呈现层，让「唯一事实源」在一夜之间失效；本特性的方向是散文退让为指针，不是从 yaml 生成散文。判据：FR-010。
- **N3 不迁读者独有的说明性事实**。五维表的维度名、判据句、理由叙述继续留在 markdown。判据：FR-006 (ii)。
- **N4 不重构 `execution-config.py` 的内联子集解析器**（A5）。它是既有重复，本特性登记而不趁手修；拿它开刀会把一个已经跨面的特性扩成解析器重构。
- **N5 不改既有门禁的判据与退出码契约**。FR-010 的**「不得重判侧」六脚本**（枚举见 FR-010，本行不复述）的判定内容与退出码契约不因本特性而变；只允许其取值来源改为读声明。判据：FR-010、SC-006。
- **N6 不新增阶段、不新增特性状态、不改变 `/speckit.*` 命令序列与完成哨兵**。本特性是载体分层，不是流程改造。判据：`.specify/shared/definitions/flow-class-definitions.md` § 不变量指针（类别与分层不得被用作跳过或缩短阶段的开关）。
- **N7 不迁 `validate-requirements.py` 的六个检查项标签集（clarify 裁定 A8(b)，判为越界故不迁）**。理由：该标签集的「机器消费」只是一条测试的提取断言，按 FR-006 (i) 收窄后的判据不成立；且迁出会迫使改写 081 的验收测试 `tests/contract/test_requirements_checker.py` § `test_c01_c02_docstring_enumerates_exactly_the_pinned_labels`（它断言 docstring 的枚举**等于** `REQUIREMENTS_CHECKS`），或把枚举留成第二份而迁移零收益。**可解析锚点**：`scripts/python/validate-requirements.py:8`（docstring 自述 pinned label set）、`tests/contract/test_requirements_checker.py:105`、`tests/contract/test_checker_form.py:304`（`path-marker` 是 081 的第六个标签）。**为什么不写排除记录**：[[STR-008]] 是**单元**级理由，而该单元（`templates/commands/requirements.md` + `skills/internal/create-requirements/SKILL.md`，引擎 `scripts/python/validate-requirements.py`）已因 A8(a) 的 in-scope 处置持有唯一处置记录；再写一行会违反「一个候选单元 MUST 有且仅有一条处置记录」。**本非目标不是豁免口袋**：它点名一项具体事实、给出两个树内锚点，且不改变该单元的 in-scope 处置。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: **封闭集可重算且自洽**。在实现树上连续两次运行 [[STR-003]] --action coverage：(i) 两次输出逐字节一致（确定性 2/2，证明比较对象不是上一轮自己；该性质对三个动作成立见 FR-016，本项只取 `coverage` 作读数实例）；(ii) 候选单元的处置缺失为 0（[[STR-013]] 命中 0 次）；(iii) 每条事实声明的 `consumers` 与载体侧引用**双向一致**——声明点名的一方确实引用它、引用它的一方确实被点名（N/N，N 由该次运行报出的声明条数与候选单元数共同决定，MUST NOT 硬编码）；(iv) 不存在不在候选集内的孤立声明文件（0 个）。**Path**: final
- **SC-002**: **三层完整性达标**。in-scope 集合内每个单元的完整性状态为 [[STR-004]]（N/N，[[STR-005]] 行数为 0）；每条事实在 [[STR-001]] 有且仅有一份声明并通过 schema 校验（N/N）；每条事实的 `former_carriers` 在既有 `doc-consistency-check.py` 的 `duplicate` 面下 `duplicate-fact` 零命中（N/N；调用形态固定在 FR-007 (b)，逐事实归因来自该次运行的原因 [[STR-011]] 的 `<fact>@<path>`，MUST NOT 假设该面有逐事实选择器）。**读数分三段具名，三段 MUST 各自成立（3/3）**：状态侧、声明侧、残留侧，缺任一即该条记 `partial`，MUST NOT 以「声明文件都存在」折算为通过。**Path**: final
- **SC-003**: **失败语义可判**。六个封闭原因 [[STR-009]]／[[STR-010]]／[[STR-011]]／[[STR-012]]／[[STR-013]]／[[STR-014]] 各有一份负夹具：6/6 以退出码 1 输出该原因**逐字**（含占位符替换后的形态），0 处以自由文本代替原因；对应正夹具 1/1 退出 0 且 0 误报。判定 MUST 由 [[STR-003]] 的实际运行日志给出，不得由人读断言。**Path**: supporting
- **SC-004**: **排除可判、不是豁免口袋**。每条排除记录的理由取值落在封闭三值 [[STR-006]]／[[STR-007]]／[[STR-008]] 之一（N/N）；每条的 `anchor` 在树内可解析（N/N，[[STR-012]] 命中 0）；[[STR-008]] 行数与其余两值同标准接受机械校验，其理由**是否充分**归 `/speckit.review`，本特性不声称能机械判定。**Path**: supporting
- **SC-005**: **分发与镜像一致**。`sync-mirrors.py --check` 相对**基线** 0 差异，即框架源与 `.specify/` 副本逐字节一致；**基线的参照物在此点名，不在判据内重新推导**：基线 = T001 采集进 `notes/pre-change-measurements.md` 的 `sync-mirrors.py --check` 读数（含退出码与逐对计数），其 plan 侧同形态先例是 `plan.md` EP-004；在临时夹具上运行 `specify init` 后，[[STR-002]] 存在且 [[STR-003]] 可运行（在该夹具上要么退出 0，要么按 FR-013 的降级契约显式标注后退出 2，记录该次读数）；旧项目缺失该目录时消费流程不中断（1/1 记录）。**Path**: supporting
- **SC-006**: **非目标未越界**。`pyproject.toml` 的 `dependencies` 相对**基线**逐字节一致（0 变化；基线与 FR-009 是**同一条读数**：T001 采集进 `notes/pre-change-measurements.md` 的该条，plan 侧同形态先例是 EP-003 的 `171c2ff8`）；FR-010 的**「零 diff 侧」五脚本**（枚举见 FR-010，本行不复述）既有测试新增失败 0 且其测试文件零改动（`git diff --stat` 对 `tests/` 下这五个脚本的既有测试文件 0 变化；追加新测试文件不算改动既有断言）；`/speckit.*` 命令模板数与特性状态取值数不变（与 T001(c) 采集的基线读数逐一比对，2/2）。**Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 两次 [[STR-003]] --action coverage 的完整 stdout/stderr、退出码与耗时，按单次运行全量捕获后比对；双向一致的判定由该次运行的 JSON 输出（而非人工比对）给出。
- **SC-002 Source**: 三段各一条读数：(i) `--action coverage` 输出中每个单元的状态字段及其计数；(ii) `facts/` 目录的文件数与 schema 校验结果；(iii) FR-007 (b) 的固定调用形态下 `duplicate` 面对 `former_carriers` 集合的运行日志与其 `duplicate-fact`／[[STR-011]] 计数（该面无逐事实选择器，事实归属取自原因文本）。**不接受**以「文件都存在」充当 (ii)。
- **SC-003 Source**: `tests/fixtures/harness-triple-structure/` 下每个原因的正负夹具目录，加 `tests/contract/test_harness_triple_structure.py` 的运行日志与逐条退出码；原因比对用逐字字符串相等，不用人工判读。
- **SC-004 Source**: 排除记录文件的逐行解析结果（理由取值计数）+ 每个 `anchor` 的路径解析结果；`by-owner-decree` 行的锚点文本被人工/评审读取一次，此处只记录机械部分。
- **SC-005 Source**: `sync-mirrors.py --check` 的退出码与差异清单（**基线** = T001(a) 采集进 `notes/pre-change-measurements.md` 的那条读数，不是本行重新推导的第二个基线）；临时夹具上 `specify init` 的命令、退出码、生成树中的 [[STR-002]] 清单与 checker 读数。
- **SC-006 Source**: `git diff` 对 `pyproject.toml` 的逐字节比对（**基线** = T001(e) 的读数）；FR-010「零 diff 侧」五脚本（枚举见 FR-010）的 pytest 定向集运行记录（命令、退出码、通过/失败数、新增失败清单）；命令模板数与状态取值数的两侧计数（**基线** = T001(c)）。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `shared/declarations/` | FR-003, FR-005, FR-007, FR-013, FR-014, SC-002 |
| `STR-002` | `.specify/shared/declarations/` | FR-013, SC-005 |
| `STR-003` | `scripts/python/harness-triple-check.py` | FR-004, FR-007, FR-009, FR-010, FR-011, FR-016, SC-001, SC-003, SC-005 |
| `STR-004` | `complete` | FR-003, FR-007, SC-002 |
| `STR-005` | `pending` | FR-003, FR-005, FR-007, FR-012, SC-002 |
| `STR-006` | `no-machine-fact` | FR-002, FR-003, SC-004 |
| `STR-007` | `no-harness-asset` | FR-002, FR-003, SC-004 |
| `STR-008` | `by-owner-decree` | FR-002, FR-003, SC-004 |
| `STR-009` | `third-layer-missing: <unit>` | FR-007, FR-017, SC-003 |
| `STR-010` | `declaration-outside-subset: <path>` | FR-008, FR-017, SC-003 |
| `STR-011` | `duplicated-fact-literal: <fact>@<path>` | FR-007, FR-017, SC-002, SC-003 |
| `STR-012` | `exclusion-anchor-unresolvable: <unit>` | FR-005, FR-017, SC-003, SC-004 |
| `STR-013` | `unclassified-candidate: <unit>` | FR-017, SC-001 |
| `STR-014` | `declaration-absent: <fact>` | FR-012, FR-017, SC-003 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

**封闭原因集的形态规则（本表即其 owner）**：六个原因里**五条各带一个占位符**（`STR-009` 的 `<unit>`、`STR-010` 的 `<path>`、`STR-012` 的 `<unit>`、`STR-013` 的 `<unit>`、`STR-014` 的 `<fact>`），**一条带两个**（`STR-011` 的 `<fact>` 与 `<path>`，以 `@` 连接），**没有零占位符的模板**（5 + 1 = 6，与上表逐行对齐，任一模板的占位符个数以本句为准）。**实例形态** = 模板原文，把每个 `<…>` 就地替换为对应取值，分隔符 `": "`、`"@"` 与其余字符**逐字节不变**。参数语法：`<unit>` = 该单元的 markdown 载体仓库相对路径；`<path>` = 声明文件的仓库相对路径；`<fact>` = 事实 slug（等于其声明文件名去掉 `.yaml`）。消费方（引擎发射、契约测试断言、夹具期望值）MUST 按此形态判定成员资格，MUST NOT 发明第三套写法或第二条成员规则。

## Constraints（落地约束，判据在外部 owner）

- **分类与阶段不变量**：`.specify/shared/definitions/flow-class-definitions.md` —— 类别只由「主交付物 + 判定面」决定，不得被用作跳过阶段的开关。
- **唯一事实源**：`.specify/shared/guidelines/one-source-of-truth.md` —— 任一事实只有一个 owner；本特性的声明层与散文层之间只允许「指针」，不允许「副本」。
- **封闭清单声明**：`.specify/shared/guidelines/closed-set-claims.md` —— SC-001／SC-002／SC-006 的包含性断言 MUST 满足其五要件（基线参照物、比较单元、允许差异集来源、补集断言与结构不变量、未定义聚合词清零）；本文件不复述其判据。
- **目录治理**：`.specify/shared/guidelines/directory-governance.md` —— 新目录创建即登记，命名 kebab-case，禁止聚合处理状态。
- **并发开发安全**：`.specify/instructions.md` § Concurrent Development Safety —— 记录类数据一文一件、派生索引即读即建、单所有者状态例外、验证再落地（双写者测试）。
- **Two Hats**：`.specify/instructions.md` § Two Hats —— 跨项目生效必须落框架源并定义分发与镜像路径。
- **Task Complexity Rubric**：本特性按 **Complex** 处理（跨 4 类载体、约 20 个面、迁移不可逆面较大、判据本身是交付物）。
- **编号与拓扑**：特性编号 084、spec 目录 `084-harness-triple-structure`、分支已存在；本阶段不新建分支、不改 Feature 注册表。

## Clarifications

本次运行**未提出** clarification marker（见 A10）：所有开放点均在目标仓库内可裁决，裁决逐条记在 `## Assumptions`。显式移交的两项是 A8（`Path`／标签集取值迁出是否越界改写 081 已验收契约）与 A9／FR-011（`specify init` 资产清单与首批迁移名单），它们**留给** `/speckit.clarify` 与 `/speckit.plan`，本阶段不预设结论。`/speckit.clarify` 若仍需提问，答案按 `<question>` → `<answer>` 追加为 `### Session <date>` 小节。

### Session 2026-11-05

本轮为无人值守运行（Mode A），**零提问**：答案空间由仓内证据闭合，每问的依据与读数写在本行与 `## Assumptions` 对应条目内，机械读数全量存于 `test-evidence/clarify-adjudication.txt`。下列六行是本轮**改变产物**的决定；只在 Assumptions 内落地的四条（A1／A4／A5／A6 的 ratified）不在此重复。A1–A10 的逐条裁定语在各自条目末尾。

- Q: 本规格绑到既有 Feature 还是新建？→ A: **新建 Feature 084「Harness 三重结构（markdown + yaml + script）」**。复核 081／069／053／055 四个候选（状态与范围摘要见 § Related Feature 表）均不覆盖「跨流程单元的声明层 + 覆盖判定引擎 + 三层完整性判定」的组合；`shared/declarations/` 在树内不存在、`grep -rn "shared/declarations" shared/ templates/` 零命中 ⇒ 属尚无 owner 的新能力，binding-precedent 启发式也指向 create（四候选各已有兄弟规格域，无一吸收过这类工作）。ID 取 084 与 spec key 对齐（081 同一做法）。已落 `.specify/memory/features.md` 行（`Total Features` 76 → 77 同趟重算）与 `.specify/memory/features/084.md`（状态 `Draft`），反向交叉引用落 `.specify/memory/features/081.md` § Related Files。
- Q: A8 —— 把 081 已验收契约里的 `Path` 取值域与六个检查项标签集迁入 yaml，是否越界？→ A: **一条拆成两条，同一封闭测试给出相反结论**。测试 = 迁移后是否仍 (a) 接受／拒绝同一输入集、(b) 保持拒绝理由字面量与退出码、(c) 使 081 既有测试断言零改动。**`Path` 取值域：不越界，保留 in-scope**（成员仍恰为 `final`／`supporting`，散文、消息、退出码不动，`path-marker` 族测试断言的是输入行为而非常量）。**六个检查项标签集：越界，不迁**（(c) 不成立——`test_c01_c02_docstring_enumerates_exactly_the_pinned_labels` 断言 docstring 枚举等于 `REQUIREMENTS_CHECKS`；且按 A2 收窄后它没有判决型消费者）。标签集不迁的理由记 N7 而非排除记录：`by-owner-decree` 是单元级理由，该单元已因 `Path` in-scope 持有唯一处置记录。
- Q: A2 的「机器消费」要不要收窄？→ A: **收窄**。原读法把「有测试钉住该字面量」也算机器消费，正是它让标签集看起来该迁；收窄为「存在一个确定性引擎，其**判决结果随该取值改变而改变**」。FR-006 (i) 已改写，A2 记为 revised；「跨面」一条与「重复不是判据／介质不是判据」两条不变。
- Q: A8(a) 执行后，哪些既有契约与封闭集主张要同步？→ A: 三处。① FR-018 的受影响 owner 列表增补 `shared/workflow/acceptance-hardening.md` § Closure Verdict，并附硬约束「081 既有测试断言零改动、新增失败为 0」；② SC-006 的封闭集从四个脚本扩到五个（纳入 `closure-acceptance-check.py`，它的内联取值元组同样要被迁走），并把「既有测试文件零改动」写成可判定的 `git diff --stat` 读数；③ `## Initial Scope Adjudication` 的 requirements 单元行改写为「取值 in-scope／标签集不迁」，去掉「待 clarify 复核」这个不可判定尾巴。
- Q: A9 与 FR-011 的移交要不要收口成可判定形态？→ A: **要**。它们不是「仍开放的选择」：分发义务（FR-013：`specify init` MUST 分发、旧项目缺失 MUST 降级且不得读作通过）、证据义务（SC-005：夹具上跑通或按降级契约记录 exit 2）、归属义务（`RS-003` `in-scope`）三条都已在文内可判；留给 plan 的只剩**清单产物**本身（迁移首批名单、`specify init` 资产名册与升级动作），判定点是它出现在 plan 交付物里。A9 记 ratified（附绑定），规格内不再留不可判定的「待定」。
- Q: 一处既成事实读数与规格陈述不符，怎么处置？→ A: **按实测订正并在条目内披露**。A3 原文「79 行台账」，实测 `grep -cE '^\| (/speckit\.|skill:)' shared/definitions/flow-class-definitions.md` = **80**（另 5 行属 § 类中立清单），载体侧 27 命令模板 + 53 技能 = 80 与之逐一对齐；已就地改为 80 并保留出处。这是纠正（一种读法与已记录意图一致、局部可逆），不是裁定，故不阻塞本阶段；A3 的裁决本身不变。

**集成顺序（Mode A 规则）**：先落规格侧全部改动并保存，再落 Feature 登记义务（`features.md` 行 + `features/084.md` + `features/081.md` 反向引用），最后跑 `validate-requirements.py` 复核。若本轮在两者之间中断，恢复点是未完成的 Feature 登记义务。

