# 决策项定义(Decision Definitions)

**本文档是「决策项(Decision Item)」治理规则的唯一所有者(owner)。** 它拥有本特性的封闭词汇表、两类决策的强调与呈现模板、选项集契约、决策记录字段闭集与序列化文法、字段到所有者的映射、档案投影与封闭决策生产者清单、传递与实施回执义务、机器可判与行为类的强制边界，以及旧记录的判别与只读处置规则。其他任何面——instruction 段、决策项模板、技能与 agents、文档、检查器——MUST 以「指针 + 路径」抵达本文档，MUST NOT 复述其判据表；本文档 MUST NOT 复述任何相邻所有者的判据表。本文档不新建第二套登记、队列、存储或调度器；决策档案是既有载体的投影，`.specify/register.md` 保持持久编号的唯一索引。

## 所有权声明(Ownership Declaration)

本文档拥有、且只拥有以下九个面：

1. **决策词汇表(closed vocabulary)** —— § 封闭词汇表 定义的九个词；其他任何页 MUST NOT 另行定义这些词。
2. **类别呈现与文本契约(class presentation and text contract)** —— 两类决策（`human-interactive` / `ai-autonomous`）的判定依据与各自的呈现模板及其强调义务，以及决策项文本的两条生产规则（完整名称、同名定位）与按类别的强调义务。
3. **选项集契约(option-set contract)** —— 选项集的封闭性、声明计数与每个选项的五要素。
4. **记录字段闭集(record field closure)** —— 基础层与条件层（same-name / supersession / transmission 三族）字段，以及 `### D-NNN — <标题>` 加单行字段的记录文法。
5. **字段到所有者的映射(field-to-owner mapping)** —— 每个记录字段恰有一个定义所有者，本页提供映射表。
6. **档案投影与封闭生产者清单(archive projection and producer inventory)** —— 「生产者 × 既有载体」的并集加 register 索引；生产者义务的封闭表。
7. **传递与实施回执义务(transmission obligations)** —— 决策块、确认与实施回执在 superagent→subagent 边上的义务。
8. **强制边界(enforcement boundary)** —— 机器可判规则与行为类规则的分工；行为类规则永不被机器声称覆盖。
9. **旧记录规则(legacy rules)** —— 新式记录的最小合格形态、旧记录的只读判别与零改写处置。

**指针义务(pointer-only duty)**：相邻所有者各自保留其事实与判据表，本文档只以路径抵达，MUST NOT 复述它们的表格、阈值或枚举。

| 相邻所有者 | 它拥有什么 | 本文档的抵达方式 |
|-----------|-----------|-----------------|
| `shared/guidelines/confirmation-gates.md` | 是否提问、授权级别轴与观察协议 | 指针（P-01 载体） |
| `shared/guidelines/decision-tension.md` | 承重取舍的六字段与 `T-NNN` 形态 | 指针（承重决策追加记录并交叉引用 `T-NNN`，六字段不复制） |
| `shared/guidelines/fast-fail.md` | 纠正与裁定的分流及上送件形态 | 指针（P-07 载体） |
| `.specify/register.md` | 编号登记行 | 指针（编号在此登记，不在本文档声明） |
| `shared/definitions/superagent-definitions.md` | 角色边、载荷字段与上行 | 指针（决策块随既有载荷同行，不新增角色字段） |

## 封闭词汇表(Closed Vocabulary)

以下九个词是本文档的封闭词汇表；新增一个词 MUST 先修订本节，其他任何页 MUST NOT 定义这些词。

| 词(Term) | 一句话含义 |
|----------|-----------|
| **Decision Item** | 一个被呈现或被持有的选择：某种对象、上下文、封闭选项集与一个持有者。 |
| **Decision Record** | 一个已完成决策项在其生产者既有载体中的档案投影，按 `### D-NNN — 标题` 加单行字段文法落盘。 |
| **Option** | 决策项选项集中的一个具名成员，携带 label、consequences、reversibility、default 与 evidence 五要素。 |
| **Decision Block** | 随既有派发载荷同行的传递单元：`decision_id`、`decision_class`、所选选项全名、实施约束与档案指针五个字段。 |
| **Acknowledgement** | 子代理回传中的确认项：回显 `decision_id`，声明该决策块已被接受并将据以实施，或作为异常上送。 |
| **Implementation Receipt** | 子代理回传中的实施回执：`decision_id`、实施摘要、证据指针与 `divergence`（含理由）四个字段。 |
| **Decision Producer** | 封闭生产者清单中的一行：生产者、既有载体、义务（`record` / `record-when-decision` / `exempt`）与事实所有者。 |
| **Archive Projection** | 「生产者 × 既有载体」的并集加 register 索引；它是既有载体的投影，不是第二套存储。 |
| **Decision Class** | 按持有者判定的类别，取 `human-interactive`（人持有）或 `ai-autonomous`（无人在场的代理持有）之一。 |

## 决策类别(Decision Classes)

**判定依据(按持有者, A-4)**：决策类别按**持有者(holder)**判定，不按呈现媒介判定：`human-interactive` = 决策由人持有（人对选项的选择、人工评审处置）；`ai-autonomous` = 决策由 agent 在无用户在场时持有（无人值守裁决、被委派的实施取舍）。同一个生产者可产出两类。

- **类声明(closed declaration)**：每个决策项 MUST 声明恰一个 `decision_class`，取值 MUST 来自闭集 `human-interactive` / `ai-autonomous`；类缺失、类混合或值域外是缺陷。类别决定适用的模板与检查集；传递不改变类别。

### `human-interactive` 呈现模板

呈现 MUST 以可读性为先，逐项携带：

1. **平实语言的问题(plain-language question)**：用读者能理解的话写出正在选择什么，MUST NOT 只给形式化谓词。
2. **上下文(context)**：为什么现在要选、约束是什么；措辞与上下文规则遵循 `shared/guidelines/user-facing-comprehension.md`。
3. **逐选项的后果(consequences)与可逆性(reversibility)**：每个选项写明后果与是否可逆。
4. **默认项(default)**：恰一个选项标为默认。
5. **完整名称与定位信息(full names and locator)**：主体与每个选项标签用对象的完整名称；同名冲突时按 § 决策文本契约 给出定位信息。

### `ai-autonomous` 呈现模板

呈现 MUST 以严谨性为先，逐项携带：

1. **封闭选项集(closed options)**：选项来自封闭、可枚举的集合。
2. **显式的决策谓词/规则(decision predicate/rule)**：写出据以判定的谓词或规则，MUST NOT 只有散文。
3. **显式假设(assumptions)**：判定依赖的假设逐条写出。
4. **可机器核查的证据指针(evidence pointers)**：证据以可解析指针给出。
5. **确定性结论与重开条件(conclusion and reopening condition)**：同一输入 + 同一谓词重放得同一结论；给出使决策重开的条件。

两个模板都沿用 § 决策文本契约 的完整名称与定位规则。

**呈现与类别不符的承接**：`human-interactive` 只有形式化谓词而无解释由 B-03 承接，`ai-autonomous` 只有散文而无判定规则由 B-04 承接，类别选错由 B-06 承接；三者都是行为类，MUST NOT 被机器声称覆盖。

## 决策文本契约(Decision Text Contract)

### 两条生产规则(最低门槛)

- **R1 完整名称(full names)**：决策主体(decision subject)与每个选项标签(option label) MUST 使用对象的完整名称，MUST NOT 只用简称。已登记简称由 M-08 判（只覆盖 `.specify/glossary.md` 已登记词）；未登记简称的歧义由 B-01 评审面承接。
- **R2 同名定位(same-name locator)**：当可能存在同名冲突时，决策项 MUST 声明 `same_name_conflict: true`，并 MUST 携带机器可解析的 `resource_locator`，其具名维度的下限为业务资源组(business resource group) + region id 这一对；取值形如 `business_resource_group=<组>; region_id=<区域>`。同名对象 MUST NOT 在没有定位信息时被呈现；以 `same_name_conflict: false` 绕过定位是缺陷，不是豁免。定位是否充分由 B-02 评审面判定。

### 按类别的强调

- **`human-interactive`**：强调可读性——平实语言、上下文、每个选项的后果与可逆性、默认项、完整名称与定位信息；措辞与上下文遵循 `shared/guidelines/user-facing-comprehension.md`；MUST NOT 只给形式化谓词而无解释。
- **`ai-autonomous`**：强调严谨性——封闭选项集、明确的决策谓词/规则、显式假设、可机器核查的证据指针、确定性结论与重开条件；MUST NOT 只有散文而没有判定规则。

### 评审承接面

- **B-01** 承接**文本完整性(completeness)**：名称是否完整、解释是否足够。
- **B-02** 承接**定位充分性(locator adequacy)**：具名维度是否足以区分同名对象。
- 二者都是行为类评审面，MUST NOT 被机器声称覆盖；机器只判形态与在场性（M-02 / M-08）。

## 选项集契约(Option-Set Contract)

选项集是决策项的可比较面：封闭、可枚举，每个成员带齐五要素。本节规定的形态由 M-03 判；AI 重放与人的选择信号按各自承接面处理，MUST NOT 机器声称覆盖。

### 封闭可枚举集(closed enumerable set)

- **声明计数(declared count)**：`options` 字段的取值 MUST 以声明计数开头——`- **options**: <N>`；N 是选项集合的声明大小，0/1 退化情形同样声明。声明计数缺失、或与选项条目数不一致，即集合不封闭（M-03）。
- **空集不是决策项**：`options: 0`（或无任何选项条目）不构成决策项（M-03）；没有任何可行选项的情形 MUST 按重开条件处理，MUST NOT 以空集冒充决策。
- **唯一标签(unique labels)**：同一选项集内标签 MUST 唯一（去首尾空白后按字面比较）；重复即缺陷（M-03）。

### 每个选项的五要素(five elements)

每个选项是 `options` 下以 `- label: <完整名称>` 起始的缩进子行，随后以缩进 ≥2 空格的续行逐项给出：

| 要素 | 行形态 | 含义 |
|------|--------|------|
| `label` | `- label: <完整名称>` | 选项的完整名称；与决策主体适用同一完整名称规则（§ 决策文本契约 R1） |
| `consequences` | `consequences: <文本>` | 选择该选项的后果 |
| `reversibility` | `reversibility: <文本>` | 可逆性：`reversible` / `irreversible`，并给出适用条件 |
| `default` | `default: yes|no` | 默认项标记；每个选项集恰一个默认成员 |
| `evidence` | `evidence: <指针>` | 选择所需证据；指针可解析性由 M-09 判 |

五要素缺一即缺陷（M-03）。选项级 `path` 与 `forced` 是 `options` 字段的值形状成员，不是顶格记录字段。

- **`other` 的合法形态**：名为 `other` 的选项只有在携带 `path: <谁/何时/如何新增选项并回写记录>` 子行时才合法；没有 `path` 的 `other` 不是选项（M-03）。
- **单一可行项(forced)**：选项集只有一个成员时，MUST 在 `options` 块内声明 `forced: <理由>`，MUST NOT 伪装成多选；未声明即缺陷（M-03）。`forced` 是集合级声明，不是第六个选项要素。
- **零可行项**：没有任何可行选项时不构成决策项（同空集）。

### 选中项(chosen member)

`chosen_option` MUST 是选项集中的一个具名成员（按 label 匹配；M-03）；不是成员即缺陷。`human-interactive` 决策在 `chosen_option` 中同时记录人的选择信号：取值域归 `shared/guidelines/confirmation-gates.md` § 门控观察协议（指针，不复述；C-108）。

### AI 可重放(replayability duty)

`ai-autonomous` 记录 MUST 记录判定谓词与判定输入——二者是 `rationale` 字段的值形状成员（缩进 ≥2 空格的续行）；把谓词应用到记录输入 MUST 确定性地重推 `chosen_option`，重放不一致是缺陷。重放可复现性由守卫测试演示（`tests/unit/test_validate_decisions.py::test_ai_replay_deterministic`）；谓词是否成立、假设是否缺失归 B-04 评审承接，MUST NOT 声称机器覆盖。

## 决策记录(Decision Record)

决策记录是决策项在其生产者既有载体中的档案投影：一条决策项在完成时恰产生一条记录。记录文法由 M-01 判，编号由 M-04 判，证据指针可解析性由 M-09 判；三条规则的转红条件见 § 强制边界。

### 序列化文法(serialization grammar)

- 记录以三级标题 `### D-NNN — <一行标题>` 承载；编号只在标题中出现一次，不另设顶格字段行。
- 每个字段是一行 `- **<小写字段名>**: <值>`；字段名小写、不加引号、不含空格。
- `options` 的选项是缩进子行（每个选项的五要素各占一行，见 § 选项集契约）；续行 MUST 缩进 ≥2 空格。
- 围栏代码块内的行不计入文法——不解析为记录、标题或字段。

### 分层封闭(layered field closure)

记录字段在每一层封闭；两层之外 MUST NOT 出现任何顶格字段——新增字段 MUST 先修订本节，生产面 MUST NOT 改名。

**基础层(十条，每条记录必填)**：

| 字段 | 含义 |
|------|------|
| `decision_id` | `D-NNN`；由标题承载（标题中出现恰一次） |
| `decision_class` | 闭集 `human-interactive` / `ai-autonomous`（§ 决策类别） |
| `context` | 决策所处情境与约束 |
| `options` | 封闭选项集（§ 选项集契约） |
| `chosen_option` | 选项集中的具名成员；`human-interactive` 时同时承载人的选择信号 |
| `rationale` | 理由；承重决策交叉引用 `T-NNN` 而不复制六字段；`ai-autonomous` 时同时承载判定谓词与记录输入 |
| `evidence` | 证据指针；每一条 MUST 可解析（M-09） |
| `actor` | 持有/实施身份（身份形态归 `shared/definitions/superagent-definitions.md`） |
| `created_at` | ISO-8601 UTC 创建时点，必有值 |
| `transmission_status` | 未传递记录取 `not-transmitted`；值域见 § 状态与时间戳 |

**条件层(按触发族封闭，触发成立时必填)**：

- **同名族**：`same_name_conflict` + `resource_locator`——同名冲突风险存在时成对在场（§ 决策文本契约 R2）。
- **取代族**：`superseded_by`——记录被取代时必填；它的在场即 `superseded` 标记。
- **传递族**：`dispatched_at` / `acknowledged_at` / `implemented_at`——仅当决策被传递，按 `transmission_status` 相位追加：到 `dispatched` 必填 `dispatched_at`，到 `acknowledged` 必填 `acknowledged_at`，`implemented` / `diverged` 必填 `implemented_at`；事件发生时才追加，**未到相位不设占位**；`blocked` 按已达相位判。确认(acknowledgement)与 `implementation_receipt` 是回传项，不是记录字段——它们驱动这些时点与状态相位（§ 传递与实施）。

### 状态与时间戳(state and timepoints)

- `transmission_status` 的封闭值域：`not-transmitted` / `dispatched` / `acknowledged` / `implemented` / `diverged` / `blocked`。相位只能向前推进；`blocked` 自 `acknowledged` 起合法；`diverged` 只与 `divergence: diverged` 的回执同批；向后回退非法；重决是新记录取代旧记录。
- 时点形态 MUST 为 ISO-8601 UTC（`YYYY-MM-DDTHH:MM:SSZ`，可带小数秒或 `+00:00` 偏移）；形态错、后相位时点出现在前相位、或未传递记录携带传递族时点，都是缺陷（M-01）。

### 取代(supersession)

被取代的记录 MUST 保留，`superseded_by` 指向取代件；被取代的编号 MUST NOT 删除或重用。

### 编号(id rules)

`decision_id` MUST 为 `D-NNN`（三位数字），同一载体内**密集**（自 `D-001` 起连续、不重复），永不重用；编号在诞生时登记于 `.specify/register.md`（逐条或按「载体 + 区间」分组行）；跨载体引用 MUST 同时给出**载体指针**。跨载体允许同号出现，但引用必须可回指载体。

### 重建义务(reconstruction duty)

每条记录 MUST 可只凭既有载体 + `.specify/register.md` 重建其**适用层**字段——基础层十条 + 触发成立的条件族；未触发的条件族不在重建范围。无法重建（缺字段、断指针、无记录）即缺陷，MUST NOT 以对话记忆补足。

### 字段到所有者(field ownership)

每字段恰有一个定义所有者；本表只登记所有权，取值域正文归各所有者。

| 层 | 字段 | 定义所有者 | 载体/登记 |
|----|------|-----------|-----------|
| 基础 | `decision_id` 形态 | 本节 | `.specify/register.md`（登记） |
| 基础 | `context` / `options` / `chosen_option` / `rationale` / `evidence` / `created_at` / `transmission_status` | 本节（值形状见各节） | 各载体 |
| 基础 | `actor` | `shared/definitions/superagent-definitions.md`（边身份）/ run 身份 | 各载体 |
| 基础 | 承重决策的 `rationale` 六字段内容 | `shared/guidelines/decision-tension.md` | `T-NNN` 记录 |
| 条件 | `same_name_conflict` / `resource_locator` / `superseded_by` / `dispatched_at` / `acknowledged_at` / `implemented_at` | 本节 | 各载体 |

承重决策的决策记录 MUST 交叉引用对应 `T-NNN`，MUST NOT 复制 `antithesis` / `binding_constraints` / `discriminating_evidence` / `expected_sacrifice` / `revision_trigger` 的内容（C-205；六字段归 `shared/guidelines/decision-tension.md`）。

### 旧记录规则(legacy rules)

- **新式记录的最小合格形态(minimal qualifying form)**：`^### D-\d{3}` 标题 **且** 块内含 ≥1 条 `- **<字段名>**: <值>` 字段行（字段名属 § 分层封闭 的字段集）。达到阈值即为新式记录——**即使不完整**（缺字段是 M-01 的转红）；低于阈值（无字段行的三位数字标题、一/两位数标题）一律 `legacy`。id 形态单凭 `D-001` 之类 register 行不判新式。
- **只读判别(report, never judge)**：本契约落地前的旧记录 MUST 被报告为 `legacy`，保持可读，MUST NOT 被判为无效、MUST NOT 改写或删除。
- **判定范围(scan scope)**：`legacy` 以本次运行的载体集为范围——register 行仅当不与本次扫描到的新式记录 id 相交时才报告 `legacy`；它与新式记录 id 相交时即视为该编号的诞生登记。

## 档案即投影与决策生产者清单(Archive as Projection and Decision Producer Inventory)

**决策档案不是新存储**：它是「生产者 × 既有载体」的持续**并集**，加 `.specify/register.md` 的**编号唯一索引**。每个清单内生产者恰映射一个既有载体；一个 `D-NNN` 编号解析到（载体，标题）。本节是生产者清单的规范主页；需求规格中的同名表是 requirements 阶段的 dated 声明。

- **不是第二套存储**：MUST NOT 新建第二套登记、队列、存储或调度器；档案的「写入」就是在生产者自己的既有载体里按 § 决策记录 写一条记录。
- **清单封闭与修订义务(inventory closure)**：清单外的入口若产出决策项即缺陷，MUST 走清单修订（修订本节与依赖它的测试同批落盘），MUST NOT 静默丢弃记录；新增或删除生产者同样修订单侧同批。
- **只读命令的处置(read-only dispositions)**：只读命令的处置 MUST 写进该命令**自己的报告载体**，MUST NOT 通过修改被分析的工件来归档（C-208）。

| ID | 生产者 | 既有载体 | 义务 | 类别(按持有者) | 事实所有者 |
|----|--------|----------|------|----------------|-----------|
| P-01 | 确认门 / 用户决策 | 门控执行报告 + 门控观察条目（`.specify/feedback/` 既有条目面） | record-when-decision（门控触发即是决策；可逆动作的自动执行不是决策项） | 交互运行 `human-interactive`；无人值守 `ai-autonomous` | `shared/guidelines/confirmation-gates.md`（是否问）；本页（记录形态） |
| P-02 | requirements 阶段裁决（无人值守自裁） | `requirements.md` § Clarifications（Session 行）+ 规格 A 表 | record | `ai-autonomous` | `skills/internal/create-requirements/SKILL.md` |
| P-03 | plan 阶段取舍与承重决策 | `plan.md`（含 § Decision Tensions 的 `T-NNN`） | record（显式呈现的取舍）；承重决策另加 `T-NNN` 并交叉引用 | 通常 `ai-autonomous` | `shared/guidelines/decision-tension.md`（六字段）；本页（决策记录） |
| P-04 | 阶段检查点裁决 | `<spec-dir>/checkpoints/<NN>-<stage>.md` | record-when-decision（并发/名册/方向裁决是决策；纯事实核验不是） | `ai-autonomous` | `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` |
| P-05 | analyze 处置 | analyze findings report | record（每个 carried finding 的 fixed/deferred/rejected + 理由） | `ai-autonomous` | `skills/internal/analyze-artifacts/SKILL.md` |
| P-06 | review 发现处置 | review report（`review.md` 与分段报告） | record-when-decision（接受/修复/拒绝是决策；纯观察不是） | 由持有者定 | `skills/internal/review-feature-quality/SKILL.md`、`skills/internal/review-sdd-process/SKILL.md` |
| P-07 | fast-fail 裁定 | fast-fail 上送件 + 处置回执（执行报告） | record-when-decision（裁定是决策；异常报告本身不是） | 由持有者定（用户裁定 `human-interactive`；无人值守自裁 `ai-autonomous`） | `shared/guidelines/fast-fail.md` |
| P-08 | goal / anchor / team 决策 | `.specify/goals/<slug>/goal.md`、`.specify/anchoring/<slug>/anchor.md`、`.specify/teams/<slug>/team.md` 的既有决策/History 面 | record | 由持有者定 | `shared/definitions/goal-definitions.md`、`anchor-definitions.md`、`agent-definitions.md` |
| P-09 | superagent → subagent 传递决策 | 派发载荷（决策块）+ run report / 角色边载体 | record（被传递决策的唯一记录在其产出载体；传递与回执不生成第二条记录，只更新状态与审计链）+ 传递 + 实施回执 | 随被传递记录的类别 | `shared/definitions/superagent-definitions.md`、`skills/internal/run-agent/SKILL.md`、`skills/internal/run-team/SKILL.md` |
| P-10 | probe / feedback 处置 | `.specify/feedback/` 条目 + probe 注册面 | record-when-decision（阈值提示不是决策；接受/延后/拒绝处置是决策） | 通常 `ai-autonomous` | `shared/definitions/probe-definitions.md`、`shared/workflow/feedback-step.md` |
| P-11 | run determination（运行判定） | session 记忆中的判定记录（`run-determination.py`） | exempt —— 对已完成运行的测量/评估，不是选项间选择的决策项 | n/a | `shared/workflow/feedback-step.md` § Run Determination |
| P-12 | 确定性检查器/门的 verdict | 检查器输出 / 检查点引用 | exempt —— 结果由规则唯一决定，没有选项集；围绕它的处置归 P-04/P-05 | n/a | 各检查器与 `shared/workflow/acceptance-hardening.md` § Gates |


## 传递与实施(Transmission and Implementation)

决策跨过 superagent→subagent 边时，传递的是既有派发载荷中的**任务权威内容**，不是新的角色字段、消息类别或通道。通道字段、四项既有注入与上行规则归 `shared/definitions/superagent-definitions.md` § The super↔sub Protocol（按指针抵达，本节不复述）。本节拥有决策块、确认与实施回执的形态义务。

### 决策块(decision block)

- **搭乘既有载荷**：交办实施的决策 MUST 以 `decision_block` 搭乘既有派发载荷下行；七个角色字段与四项既有注入保持不变，决策块 MUST NOT 被当作第八个角色字段。
- **五个字段(five fields)**：`decision_id`（解析到一条记录）、`decision_class`（与被传递记录的类别一致——传递不改变类别）、所选选项完整标签(`chosen_option`)、实施约束(`implementation_constraints`)、档案指针(`archive_pointer`，载体路径 + 标题锚)。
- **构造处拒绝**：决策 backed 派发缺决策块、或块缺任一字段，MUST 在载荷构造处拒绝（M-06）；非决策派发不带块合法（BC-02 桥）。

### 确认(acknowledgement)

- 子代理回传 MUST 含**确认**：回显 `decision_id`，并声明该决策块已被接受并将据以实施；上下文使决策失效时，同一回传位置给出异常上送（见 § 禁止静默重决）。
- 确认搭乘既有回传，不新增消息类别或通道；父侧据其推进记录的 `acknowledged_at` 与 `transmission_status` → `acknowledged`（§ 决策记录 的传递族时点）。

### 实施回执(implementation_receipt)

- 回传 MUST 含 `implementation_receipt`，四个成员：`decision_id`、实施摘要(`implementation_summary`)、证据指针(`evidence`)、偏离声明(`divergence`：`none` 或 `diverged` + 理由)。
- 回执驱动记录的 `implemented_at`、`transmission_status` 的实施结果维度与 `diverged` 相位（§ 决策记录 的传递族时点）。
- 缺任一项即回传**不完整**：父侧 MUST NOT 消费其结论、MUST NOT 补齐缺项（沿用 `superagent-definitions.md` § The super↔sub Protocol 的上行规则）。
- 传递动作与回执 MUST NOT 生成第二条决策记录——一条决策项恰一条记录。

### 禁止静默重决(no silent re-decision)

- 子代理 MUST NOT 静默重决：上下文变化使决策失效时，MUST 停在异常点并以 fast-fail 上送件形态报告「证伪了什么预期」（分流判据归 `shared/guidelines/fast-fail.md`，指针）。
- 无决策记录/编号的决策 MUST NOT 被派发实施；无法解析的 `decision_id` MUST NOT 被实施。

### 审计链(audit chain)

- 每条传递决策 MUST 留下可审计三段链：**决策记录 → 派发尝试**(角色边身份 / run report)**→ 实施回执**。任一环缺失或编号不一致即断链，MUST 作为可上报的**显式异常**报告，MUST NOT 沉默（M-07）。
- **多跳(multi-hop)**：每一跳的载荷都携带决策块，每一跳的回执都引用同一 `decision_id`；最终回执与原始记录 MUST 连成一条链。

### 重决与取代(re-decision and supersession)

- 重决是**新记录**：父侧新增一条记录，旧记录以条件层 `superseded_by` 指向新编号并**保留**旧记录与旧回执，MUST NOT 删除或改写（§ 决策记录 的取代族）。
- 取代不改变被传递决策的类别；每条记录的审计链分别成立。

## 强制边界(Enforcement Boundary)

本节拥有本特性的**机器可判/行为类分工**：九条机器规则与七条行为规则的封闭名单、逐规则的唯一判据动作与转红条件、以及表—守卫对等和门控中性两项义务。两类规则的反向性质是本节的要点：机器规则 MUST 能被改坏的对象**转红**；行为规则 MUST 被具名评审承接，MUST NOT 被任何文档或测试声称机器覆盖。

### 机器可判规则(M rules, closed)

| 规则 | 判据动作(judge) | 转红条件(red condition) | 覆盖声明 | 逆向样本(reverse sample) |
|------|-----------------|--------------------------|----------|--------------------------|
| M-01 记录分层文法/类取值/时点 | `--action records` | 缺基础层字段、条件层字段在触发成立时缺失、`decision_class` 值域外、`transmission_status` 值域外、时点形态错或与状态相位矛盾 | 机器覆盖 | `tests/fixtures/decision-governance/m01/` |
| M-02 同名冲突的定位信息 | `--action records` | `same_name_conflict: true` 且 `resource_locator` 为空或具名维度少于下限 | 机器覆盖（只判在场与维度数） | `tests/fixtures/decision-governance/m02/` |
| M-03 选项闭集 | `--action records` | 空选项集、重复标签、`other` 无 `path`、五要素缺失、`chosen_option` 非成员 | 机器覆盖 | `tests/fixtures/decision-governance/m03/` |
| M-04 决策编号（只判新式记录） | `--action records` | 新式记录的 `D-NNN` 形态错、同载体不密集、register 不可解析（legacy 标题与 register 行不判） | 机器覆盖 | `tests/fixtures/decision-governance/m04/` |
| M-05 实施回执 | `--action chain` | 回执缺失、`decision_id` 缺失或不可解析 | 机器覆盖 | `tests/fixtures/decision-governance/m05/` |
| M-06 派发决策块 | `--action payload` | 决策 backed 派发缺决策块或块缺字段 | 机器覆盖 | `tests/fixtures/decision-governance/m06/` |
| M-07 审计链 | `--action chain` | 记录、派发尝试、回执三段任一缺失或编号不一致 | 机器覆盖 | `tests/fixtures/decision-governance/m07/` |
| M-08 已登记简称 | `--action records` | 决策主体命中 glossary 已登记 variant 且 canonical 存在 | 机器覆盖（只覆盖已登记词） | `tests/fixtures/decision-governance/m08/` |
| M-09 evidence 指针可解析 | `--action records` | 任一 evidence 指针不可解析（指向的载体路径/锚不存在或不可读） | 机器覆盖（只判可解析，不判证据是否充分） | `tests/fixtures/decision-governance/m09/` |

### 行为类规则(B rules, closed)

| 规则 | 承接面(review surface) | 覆盖声明 |
|------|------------------------|----------|
| B-01 名称完整性 | `/speckit.review` 产物段 + 人工决策评审 | 行为类，不声称机器覆盖 |
| B-02 定位充分性 | `/speckit.review` 产物段 + 人工决策评审 | 行为类，不声称机器覆盖 |
| B-03 人工可读性/后果真实性 | 人工决策评审 + `/speckit.review` 产物段 | 行为类，不声称机器覆盖 |
| B-04 AI 严谨性 | `/speckit.analyze` + `/speckit.review` | 行为类，不声称机器覆盖 |
| B-05 理由充分性 | `/speckit.analyze` + `/speckit.review` | 行为类，不声称机器覆盖 |
| B-06 类别正确性 | `/speckit.review` 产物段 | 行为类，不声称机器覆盖 |
| B-07 保全裁定充分性（受保护产物改动） | `/speckit.analyze` + `/speckit.review` 产物段 | 行为类，不声称机器覆盖 |

### 表—守卫对等(table–guard parity)

- 每条 M 规则恰有**一个**确定性判据动作与**一个**转红条件（上表逐行）；改变判据动作或转红条件 MUST 先修订本节。
- 测试侧的守卫花名册（`tests/contract/test_decision_governance_guards.py` 的 `GUARD_ROSTER`）与本节 M 表 MUST 行集一致；行为面名单与 B 表 MUST 行集一致——任一方向缺一行即缺陷（C-407）。
- 每条 M 规则 MUST 配一个**逆向样本**（把被检查对象改坏后守卫转红）；无逆向样本的守卫视为缺陷（C-403）。
- 每条 B 规则 MUST 有具名承接面；文档与测试 MUST NOT 声称任何 B 规则被机器覆盖（C-402）。

### 门控中性(gate neutrality)

- 本特性 MUST NOT 新增阻塞式门控：`scripts/python/scan-confirmation-gates.py` 的治理后复扫 MUST 相对**有效基线**零新增命中（基线读数与重定基线裁定记录在实现证据中，FR-025）。
- **保全面（containment claim）**：三个受保护所有者产物 MUST 对有效基线逐字节一致，读数由 `git diff --quiet <有效基线>..HEAD -- <三路径>`（零 `--numstat` 行）给出；允许差异集恒为空。任何改动 MUST 与一条记录在案的**重定基线裁定**同批落盘（裁定形态归 requirements FR-025 与其载体）；无裁定的改动由 B-07 承接（评审，永不机器声称）。
