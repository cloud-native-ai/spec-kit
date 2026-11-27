# 决策项定义(Decision Definitions)

**本文档是「决策项(Decision Item)」治理规则的唯一所有者(owner)。** 它拥有本特性的封闭词汇表、两类决策的强调与呈现模板、选项集契约、决策记录字段闭集与序列化文法、字段到所有者的映射、档案投影与封闭决策生产者清单、传递与实施回执义务、机器可判与行为类的强制边界，以及旧记录的判别与只读处置规则。其他任何面——instruction 段、决策项模板、技能与 agents、文档、检查器——MUST 以「指针 + 路径」抵达本文档，MUST NOT 复述其判据表；本文档 MUST NOT 复述任何相邻所有者的判据表。本文档不新建第二套登记、队列、存储或调度器；决策档案是既有载体的投影，`.specify/register.md` 保持持久编号的唯一索引。

## 所有权声明(Ownership Declaration)

本文档拥有、且只拥有以下十个面：

1. **决策词汇表(closed vocabulary)** —— § 封闭词汇表 定义的十七个词；其他任何页 MUST NOT 另行定义这些词。
2. **类别呈现与文本契约(class presentation and text contract)** —— 两类决策（`human-interactive` / `ai-autonomous`）的判定依据与各自的呈现模板及其强调义务，以及决策项文本的两条生产规则（完整名称、同名定位）与按类别的强调义务。
3. **选项集契约(option-set contract)** —— 选项集的封闭性、声明计数与每个选项的五要素。
4. **记录字段闭集(record field closure)** —— 基础层与条件层（same-name / supersession / transmission 三族）字段，以及 `### D-NNN — <标题>` 加单行字段的记录文法。
5. **字段到所有者的映射(field-to-owner mapping)** —— 每个记录字段恰有一个定义所有者，本页提供映射表。
6. **档案投影与封闭生产者清单(archive projection and producer inventory)** —— 「生产者 × 既有载体」的并集加 register 索引；生产者义务的封闭表。
7. **传递与实施回执义务(transmission obligations)** —— 决策块、确认与实施回执在 superagent→subagent 边上的义务。
8. **强制边界(enforcement boundary)** —— 机器可判规则与行为类规则的分工；行为类规则永不被机器声称覆盖。
9. **旧记录规则(legacy rules)** —— 新式记录的最小合格形态、旧记录的只读判别与零改写处置。
10. **批量决策面(batch faces)** —— § 待决策项来源清单、§ 待决策项块、§ 批次状态、§ 批次呈现契约、§ 建议默认值与依据、§ 决策批次与应答、§ 批次处置与沉默接受默认、§ 批次记录契约、§ 批次登记与来源更新、§ 重放契约、§ 完备性与拒绝、§ 重决与取代 所定义的批量决策规则面（112 加法扩展）；其他任何面 MUST 以指针抵达，MUST NOT 复述其判据表。

**指针义务(pointer-only duty)**：相邻所有者各自保留其事实与判据表，本文档只以路径抵达，MUST NOT 复述它们的表格、阈值或枚举。

| 相邻所有者 | 它拥有什么 | 本文档的抵达方式 |
|-----------|-----------|-----------------|
| `shared/guidelines/confirmation-gates.md` | 是否提问、授权级别轴与观察协议 | 指针（P-01 载体） |
| `shared/guidelines/decision-tension.md` | 承重取舍的六字段与 `T-NNN` 形态 | 指针（承重决策追加记录并交叉引用 `T-NNN`，六字段不复制） |
| `shared/guidelines/fast-fail.md` | 纠正与裁定的分流及上送件形态 | 指针（P-07 载体） |
| `.specify/register.md` | 编号登记行 | 指针（编号在此登记，不在本文档声明） |
| `shared/definitions/superagent-definitions.md` | 角色边、载荷字段与上行 | 指针（决策块随既有载荷同行，不新增角色字段） |

## 封闭词汇表(Closed Vocabulary)

以下十七个词是本文档的封闭词汇表；新增一个词 MUST 先修订本节，其他任何页 MUST NOT 定义这些词。

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
| **Pending Decision Item（待决策项）** | 一个尚未裁决、由人持有的决策项：身份（主体完整名称 + 可选定位）、来源引用集、待决策项块与资格状态。 |
| **Pending Item Block（待决策项块）** | 承载待决策项的 `### PENDING —` 块（字段闭集见 § 待决策项块）；它不是决策记录。 |
| **Decision Batch（决策批次）** | 一次扫描—呈现—应答—记录的完整会话：批次编号、扫描时点、来源计数、完备性判定与应答原文。 |
| **Batch Record（批次记录）** | 决策批次在既有 knowledge 存储中的一条日期化记录，含批次头、逐项行表与已决项记录块；审计与重放的唯一入口。 |
| **Recommended Default（建议默认值）** | 项自身声明的唯一默认选项；面板从不发明默认值或选项。 |
| **Recommendation Grounding（建议依据）** | 对封闭既往经验载体集的确定性联接结果：`grounded`（至少一条可解析指针）或 `no-evidence` 明示；`basis` 本身不是证据。 |
| **Batch Disposition（批次处置）** | 一次批次中一项的处置闭集成员：`accepted-default` / `objected-alternative` / `objected-parked`（暂缓不产生记录）。 |
| **Acceptance by Silence（沉默接受默认）** | 在一次已获用户应答的交互式批次内，未被点名的 `eligible` 项按建议默认值结案；资格合取与适用边界见 § 批次处置与沉默接受默认。 |

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
- **批次族**：`batch_id` / `batch_disposition` / `recommendation_grounding`——仅当记录由决策批次产生时**三者同批在场**（§ 批次记录契约；非批次记录 MUST NOT 携带）；取值域归 § 批次记录契约。
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
| P-13 | 批量决策面板（`/speckit.decide` 批次会话） | 批次记录（既有 knowledge 存储中的日期化条目） | record-when-decision（已决项记录；暂缓与不完整不是决策） | 仅 `human-interactive` | 本页 § 批量决策面（`shared/definitions/decision-definitions.md`）；入口面 `templates/commands/decide.md`、`skills/internal/decide-batch/SKILL.md`、`scripts/python/decision-batch.py` |


## 待决策项来源清单（Pending Source Roster）

本节是批次面的**来源所有者**：待决策项（Pending Decision Item）只从下列两个封闭来源派生；增删来源或扫描根 MUST 以本节修订进行，MUST NOT 静默增加第三来源。

### 两个封闭来源（closed two-source roster)

| 来源 id | 既有载体 | 候选存在条件（机器可检） |
|---------|----------|--------------------------|
| `register-open-decision-row` | `.specify/register.md` 的表格行 | 行 id 单元格去 markdown 强调后以 `OI-` 或 `D-` 起头，且状态单元格去强调与前导空白后以**词边界** `open` 为起始词（`resolved-for-v1`、`openness-pending` 一类前缀不是 `open`） |
| `authored-pending-item` | 四个封闭扫描根下的 tracked Markdown 载体：`.specify/specs/`、`.specify/goals/`、`.specify/anchoring/`、`.specify/teams/` | 存在标题前缀为 `### PENDING —` 的块（围栏代码块内不计） |

扫描根是**封闭清单**；根缺席记为带原因的缺席空来源（见 § 来源在场读数）。

### 候选与资格分层（candidacy ≠ qualification）

- **候选存在**只由本节的机器可检谓词判定。字段齐备性、块级文法缺陷（未知/重复/畸形字段、声明计数与条目数不符）与类别判定 MUST NOT 成为候选存在条件——它们是呈现资格（`incomplete` 及其具名原因）或具名排除。
- 块级缺陷 MUST NOT 触发整批拒绝；只有**载体级**不可读、不可解析或不可枚举才触发拒绝（判据归 § 完备性与拒绝，指针）。

### 具名排除族（named exclusion families）

以下族 MUST 以具名理由计入记账，MUST NOT 被静默丢弃，MUST NOT 被改写成「不存在」：已触发的交互门（当场问答，不跨调用挂起）、澄清标记（`/speckit.clarify` 拥有）、parked idea（`.specify/todo/`，想法队列不是决策项）、`ai-autonomous` 检查点裁决（不属人持有）、`REC-` 行（建议是决策的输入，不是决策项）、已在先前批次解决的身份。排除计数与候选计数分列；记账恒等式只含候选。

### register ↔ 块联接（deterministic linkage）

- 联接键 = 块 `origin` 中**逐字出现的** register 行 id（独立 token），且该行单元格给出的**显式仓库相对路径**上**恰有一个** `### PENDING —` 块。
- `同上`、`Open items § …` 一类相对表述 MUST NOT 被解析为路径，也不作为路径候选。
- 0 个匹配 → 该行以 `incomplete` 呈现并点名 `authority-unresolved`；多于 1 个匹配 → `incomplete` 点名 `ambiguous-link`。面板 MUST NOT 任选一块、MUST NOT 补全。
- 未能解析到块的 register 行以**行 id 为单独身份**呈现 `incomplete`，不并入任何块身份。

### 身份与去重（identity and dedupe）

- 身份 = `subject` 去首尾空白后的**逐字节**相等，加同名族的 `resource_locator` 值相等。
- 重复引用 MUST 合并为一行并列出全部来源引用；同身份而选项标签集不同 → 一行呈现并标 `source-conflict`，要求显式选择。
- MUST NOT 做大小写折叠、Unicode 归一、标题相似或语义合并；缺定位与有定位的同拼写主体 MUST NOT 合并。

### 来源在场读数（source presence）

- 每个来源记一个在场读数：`read`（成功读取）/ `absent`（载体不存在：记为带原因的缺席空来源，不拒绝，也不读作「干净」）/ `unreadable`（载体级存在但不可读或不可解析 → 触发整批拒绝）。
- **层级分界**：块级文法缺陷不是 `unreadable`；文件 I/O 失败、register 表结构无法按列解析、或候选无法枚举才是载体级。

## 待决策项块（Pending Item Block）

本节拥有待决策项块（Pending Item Block）的语法与块级缺陷规则。待决策项块是待决策项的既定载体形态，**不是决策记录**（Decision Record）：它没有 `chosen_option`，不按 § 决策记录 的文法判定；记录文法 MUST NOT 把待决策项块判为不完整记录，待决策项块检查 MUST NOT 判 `### D-NNN` 记录。两侧的标题前缀不同（`### PENDING —` 与 `### D-NNN`），互不判定。

### 标题与字段行(heading and field lines)

- 标题行：`### PENDING — <主体完整名称>`；主体 MUST 使用完整名称（§ 决策文本契约 R1）。围栏代码块内的同名行 MUST NOT 被计为待决策项块。
- 每行字段：`- **<小写字段名>**: <值>`；续行 MUST 缩进 ≥2 空格（`options` 的选项子行同此）。
- 字段闭集（closed field set）：

| 字段 | 层级 | 含义 |
|------|------|------|
| `decision_class` | 必填 | `human-interactive` / `ai-autonomous`；缺失或值域外记 `incomplete`（`class-missing`） |
| `subject` | 必填 | 决策主体的完整名称 |
| `same_name_conflict` / `resource_locator` | 条件（同名族） | 同名冲突风险存在时成对在场；维度下限沿用 § 决策文本契约 R2 |
| `context` | 必填 | 决策所处情境与约束（含为何此刻要选） |
| `options` | 必填 | 声明计数开头；每选项五要素；恰一个 `default: yes`；`other` 的 `path` 与单可行项的 `forced` 规则沿用 § 选项集契约 |
| `basis` | 必填 | 建议默认值的一行理由；本身不是证据（§ 建议默认值与依据） |
| `origin` | 必填 | 该块的产出身份；register 来源的块 MUST 逐字包含该 register 行 id 作为独立 token（§ 待决策项来源清单） |
| `created_at` | 必填 | ISO-8601 UTC 创建时点 |
| `resolution` | 条件（解决族） | 解决后追加：`<batch_id> -> <D-NNN>`；块内容不因解决而改写 |

新增或删除字段 MUST 先修订本节；字段闭集之外的名字是块级缺陷，不是扩展点。

### 块级文法缺陷(block-level grammar defects)

下列缺陷属于**块级**（该候选仍被枚举，以 `incomplete` 呈现并逐项点名），MUST NOT 触发整批拒绝，MUST NOT 被静默忽略：

- `unknown-field`：字段名不在上表闭集内。
- `duplicate-field`：同一字段在本块内出现多于一次。
- `malformed-field`：顶格 `- ` 行不匹配字段行文法，或 `options` 值不是声明计数形态，或选项标签重复。
- `option-count-mismatch`：`options` 声明计数与选项条目数不一致。
- `option-element-missing`：某选项缺五要素之一；`other` 无 `path`；单可行项未声明 `forced`。

### 不完整判定(incompleteness)

任一必填字段缺失、选项五要素缺失、存在上条块级缺陷、或某选项的 `evidence` 指针不可解析（路径不存在，或给出的锚不可寻）——该候选记 `incomplete` 并逐项点名缺失或畸形要素；它 MUST NOT 进入沉默接受资格，但其**全部现有内容** MUST 照实呈现（§ 批次呈现契约）。`incomplete` 是合法的呈现状态，不是缺陷；面板 MUST NOT 补写缺失字段或发明选项。

## 批次状态（Batch States）

本节拥有批次呈现行的状态闭集及判定顺序。每个来源候选 MUST 被恰好分类一次（闭集：`presented` / `duplicate-merged` / `not-human-held` / `already-resolved`）；每个被呈现的身份（identity）恰好获得一个资格状态。状态与原因由引擎确定性判定，MUST NOT 由呈现层改写。

### 资格状态与优先序(qualification states and precedence)

闭集：`incomplete` / `source-conflict` / `no-default` / `irreversible-default` / `prior-decision-conflict` / `eligible`，按从左到右的优先序取**第一个**命中的状态（每条呈现行恰一个状态）：

1. `incomplete` —— 必填字段缺失、块级文法缺陷、类别未知（`class-missing`）、来源行未能联接到唯一块（`authority-unresolved` / `ambiguous-link`），或选项证据指针不可解析（`evidence-unresolvable`）。
2. `source-conflict` —— 同一身份的多来源块给出的选项标签集不一致；MUST 要求显式选择，MUST NOT 任选一侧默认。
3. `no-default` —— 默认标记数不是恰一个（`default-missing` / `multiple-defaults`）。
4. `irreversible-default` —— 唯一默认选项的 `reversibility` 以 `irreversible` 起头（`default-irreversible`）；不可逆/破坏性动作的显式确认义务归 `shared/guidelines/confirmation-gates.md`（指针，不复述）。
5. `prior-decision-conflict` —— 主体全名逐字命中既往决策记录的 `context`，且既往选中项与当前建议默认不同（§ 建议默认值与依据）。
6. `eligible` —— 以上皆不命中。

只有 `eligible` 项可经沉默结案（§ 批次处置与沉默接受默认）。`no-default`、`irreversible-default`、`source-conflict`、`prior-decision-conflict` 与 `incomplete` 项 MUST 保持待定，除非用户显式点选。`incomplete` 的原因词表是闭集：`authority-unresolved` / `ambiguous-link` / `class-missing` / `malformed-field` / `unknown-field` / `duplicate-field` / `option-count-mismatch` / `missing-field` / `option-element-missing` / `evidence-unresolvable`；其余状态的原因词表随本节修订增长，MUST NOT 新增状态。

### 排除状态(exclusion states)

`not-human-held`（已声明 `ai-autonomous`，或同一身份的多来源类别声明冲突——按存疑从严）、`already-resolved`（块带 `resolution`，或读时联接到既往批次记录中的已决身份）、`duplicate-merged`（同一身份的重复引用并入一行）。排除项 MUST NOT 被呈现、转换或授权；每一项 MUST 以具名理由计入记账（§ 完备性与拒绝）。

### 接地状态(grounding states)

闭集 `grounded` / `no-evidence`；判定规则归 § 建议默认值与依据。接地状态不影响资格状态，但 `grounded` 的每条指针 MUST 可解析。

## 批次呈现契约（Batch Presentation Contract）

本节拥有「一次呈现必须携带什么、按什么顺序、哪些内容不许补造」的规则。一次调用 MUST 产出**一次**呈现，覆盖本次扫描的全部呈现行；可读性判断（读者是否读得懂）归评审承接面，机器只判槽位在场与结构。

### 确定顺序(deterministic order)

呈现顺序 MUST 为：来源清单顺序（`register-open-decision-row` 先于 `authored-pending-item`）→ 载体仓库相对路径 → 载体内的出现位置（register 行序；块起始行）。同一呈现行的来源引用 MUST 按同一顺序列出。相同输入重复扫描 MUST 得到相同项集、相同顺序与相同逐字段内容，仅扫描时间戳不同；呈现摘要 MUST 对去除时间戳后的投影计算。

### 逐项槽位(per-item slots)

每行 MUST 携带 107 `human-interactive` 呈现模板的全部要素——平实语言的问题、上下文、每个选项的后果与可逆性、唯一默认、完整名称与同名定位（适用时）、选项证据——加上：来源指针集、`decision_class`、`basis`、接地状态与指针、资格状态与具名原因、以及本项的异议/暂缓方式。缺值项 MUST 展示其**全部现有内容**并逐项点名缺失要素；MUST NOT 用补造值填满槽位，MUST NOT 以摘要替代本项。

### 批次级上下文下限(batch-level context floor)

呈现 MUST 一次性回答五个问题，使读者无需打开其他工件：为何这些事项此刻出现；沉默将意味着什么；如何提出异议或暂缓；哪些事项保持待定及各自的具名原因；完备性披露（含缺席来源）。面向用户的措辞 MUST 遵循 `shared/guidelines/user-facing-comprehension.md`（指针）。

### 用户面标识边界(identifier boundary)

面向用户的正文 MUST NOT 出现内部标识符——字段名、脚本名、状态词与原因词；结构化 payload 可携带这些标识符，它是机器通道。正文用平实语言转述状态与原因。

### 不截断与不自称完备(no truncation, no partial claims)

每个呈现项 MUST 完整呈现，长度 MUST NOT 被人为封顶；任何省略 MUST 是整批拒绝，而不是缩短的批次。`ai-autonomous` 项的呈现数恒为零（§ 待决策项来源清单 的类别门）。呈现是否易懂、后果陈述是否真实、建议理由是否充分是行为类判断，由 B-03 / B-08 / B-09 评审承接，MUST NOT 被任何文档或测试声称机器覆盖。

## 建议默认值与依据（Recommended Default & Grounding）

本节拥有建议默认值（Recommended Default）与建议依据（Recommendation Grounding）的生成规则。建议默认值 MUST 是该选项集声明的**唯一**默认成员；面板 MUST NOT 发明默认值、选项、选项后果、可逆性或证据。`no-default` 项照常呈现且 MUST NOT 经沉默结案。

### 确定性接地联接(deterministic grounding join)

接地 MUST 由引擎对下列**封闭输入**做确定性联接，联接结果只有 `grounded` 与 `no-evidence` 两个取值：

- (a) 默认选项的 `evidence` 指针中，可解析且落在既往经验载体上的那些；
- (b) 主体全名**逐字**出现在其 `context` 中的既往决策记录（含既往批次记录内的记录块）；
- (c) 这些记录引用的 `T-NNN` 标识符（其张力记录可解析时）。

既往经验载体是闭集：四个扫描根下的决策记录载体、knowledge 存储中的批次记录、`T-NNN` 张力记录、`.specify/history/` 条目、`.specify/feedback/` 条目与 `.specify/knowledge/` 条目。指针解析的读法与 M-09 一致：路径存在，且给出锚时锚可在载体中找到。`basis` 是作者撰写的一行理由，MUST NOT 被计为证据。

- **`grounded`**：至少一条可解析的既往经验指针；发出的每条指针 MUST 可解析。一条不可解析的候选指针 MUST NOT 被发出。
- **`no-evidence`**：没有可解析的既往经验指针；呈现 MUST 明示这一点，且 MUST NOT 暗示经验支持。

### 前例冲突(prior-decision conflict)

当一条既往决策记录的 `context` 逐字包含主体全名、且其 `chosen_option` 与当前建议默认的标签不同时，该行 MUST 呈现 `prior-decision-conflict`，给出该既往记录的载体指针与其选中标签，并 MUST NOT 经沉默结案。用户显式推翻既往决策时走既有取代规则（§ 传递与实施 的取代规则；批次记录的写后追加边界见 § 批次记录契约）。

### 引擎判定边界(engine judges)

联接、指针解析与前例冲突检出 MUST 由确定性引擎计算；技能 MAY 转述引擎判定，MUST NOT 做语义检索、推断额外证据或在呈现期改写已判定状态。建议是否合理是行为类判断，归 B-09 评审承接，MUST NOT 被机器声称覆盖。

## 决策批次与应答（Decision Batch & Reply）

本节拥有一次决策批次（Decision Batch）的应答语义：什么算一次应答、授权级别从哪里来、异议如何绑定与校验、原文与要点各落在哪里。

### 应答的定义(reply definition)

应答 MUST 是对**本次呈现**的显式回复：无异议、点名异议或暂缓。对呈现内容的追问不构成应答——承接方回答后继续等待。中止会话、关闭会话或只有追问的对话 MUST 产出**零条记录**。一次批次 MUST 只绑定一次呈现；呈现之外的内容不构成本次批次的应答。

### 授权级别(authorization)

交互授权级别 MUST 由调用方在记录动作上显式声明并传入，取值闭集 `interactive` / `unattended`；级别缺失 MUST 按 `unattended` 处理。无人值守调用 MAY 只读扫描，但 MUST 在记录动作处被具名拒绝——无人应答 MUST NOT 被读作沉默接受。授权级别 MUST NOT 被从终端形态、环境或沉默推断。

### 按身份绑定(binding by identity)

每条异议 MUST 绑定到一项的**身份**（`subject` 去首尾空白后逐字节相等；同名族另比较 `resource_locator` 值），MUST NOT 按位置、顺序或相似度猜测。同一身份在一次应答中重复出现、身份无法匹配到本次呈现的任何一项、或同名族未给定位而无法唯一匹配，都是具名拒绝。

### 写入前校验(validation before any write)

全部应答校验 MUST 在写任何载体之前完成：每条改选 MUST 指向该选项集的具名成员（完整标签）；点名新选项只有在该项声明了带 `path` 的 `other` 选项时才按该路径处理，否则 MUST 以路径规则具名拒绝；暂缓 MUST 由该项声明。任一校验失败 → 整次记录被拒绝、零写入、不铸造批次编号；同一呈现可在更正应答后重试。

### 原文层与要点层(verbatim layer and key points)

批次记录 MUST 以**逐字引用块**保存用户应答原文；107 决策记录的 `rationale` MUST 只保存要点（建议依据 + 沉默或改选的要点转述），MUST NOT 复述原文层。原文层是重放与审计的真源。

## 批次处置与沉默接受默认（Batch Disposition & Acceptance by Silence）

本节拥有批次处置（Batch Disposition）的闭集与沉默接受默认（Acceptance by Silence）的适用边界。机器只判处置结构与成员集合；「人是否已回答」由承接方判断并逐字留痕。

### 处置闭集(closed dispositions)

处置 MUST 取闭集：`accepted-default`（按建议默认值结案）、`objected-alternative`（按用户点名的具名选项结案）、`objected-parked`（暂缓）。「保持待定」是**没有处置**，不是第四个取值。

### 沉默接受资格(eligibility for silence)

未被点名的项 MUST 只在**一次已获用户应答的交互式批次**内、且同时满足下列全部条件时记为 `accepted-default`：类别为 `human-interactive`；块完整；恰一个默认选项；默认选项可逆；无来源冲突；无前例冲突；未被先前批次解决。任一条件不满足 → 该项保持待定，并以对应的资格状态与具名原因呈现（§ 批次状态）。

### 不合格项的显式结案(explicit settlement)

用户对 `no-default`、`irreversible-default`、`source-conflict` 或 `prior-decision-conflict` 项显式点名具名选项时，该项 MUST 以 `objected-alternative` 结案并记录，其资格状态与原因 MUST 保留在批次行中。对 `incomplete` 项，只有呈现的选项集文法完整（声明计数、五要素、唯一标签齐备）且 `subject` / `context` 可解析时才接受改选；否则 MUST 具名拒绝——由此形成的记录会违反 107 文法。

### 暂缓(park)

`objected-parked` MUST NOT 产生决策记录；项保持待定，批次记录 MUST 保留该暂缓行，下一次批次 MUST 重新呈现该项。暂缓不是拒绝，也不是接受。

### 无未处置结案、无跨批次预授权(no unhandled settlement)

面板 MUST NOT 结案用户未处置的项（沉默规则除外），MUST NOT 从「无用户回合」推断接受，MUST NOT 预授权未来同类项，MUST NOT 记忆用户偏好并自动套用——每次批次重新呈现并等待应答。

### 选择信号(choice signal)

人的选择信号 MUST 复用既有门控观察词表，按下列映射以指针抵达 `shared/guidelines/confirmation-gates.md`（该所有者拥有信号取值域，本节不复述）：`accepted-default` → `approved-as-is`；`objected-alternative` → `modified`；`objected-parked` 不产生选择信号。MUST NOT 另立第二套信号词表。

## 批次记录契约（Batch Record Contract）

本节拥有批次记录（Batch Record）的载体、写前前置与内容契约，以及批次的跨批次读写边界。

### 载体与创建语义(carrier and create-only)

- 批次记录 MUST 是既有 `.specify/knowledge/` 存储中的**一条日期化记录**，经既有记忆引擎的写入面落盘；一文件一批次，标题为 `decision-batch-<batch_id>`；批次编号形态为 `B-<YYYYMMDDTHHMMSSZ>-<8 位小写十六进制>`。
- 批次编号 MUST 在全部记录前置校验通过之后、首条写入之前铸造；被拒绝的尝试 MUST NOT 铸造编号、登记或留下本特性的任何记录/状态文件。
- 批次记录是**create-only**：同一批次编号的第二次写入 MUST 在写入面运行之前被拒绝，MUST NOT 覆盖或 upsert 既有记录（记忆引擎按 slug upsert，故创建性前置由批次引擎自己判定）。
- 批次记录 MUST NOT 是第二存储或共享可变聚合。其唯一受许的写后变更是既有取代规则要求的 `superseded_by` 单字段追加（A-27）：仅追加该字段，既有字节逐字节不变；追加形态与条件随重决规则面（§ 重决与取代）同页声明。

### 批次头(batch head)

批次头 MUST 携带：批次编号；扫描时点；工具版本；来源清单与逐来源在场读数及候选计数（含缺席来源与原因）；完备性判定（记账恒等式与判定结果）；授权级别；以及**用户应答原文的逐字引用块**。

### 逐项行表(item rows)

批次记录 MUST 携带逐项行表，每呈现行一行：项身份（主体 + 适用时的定位）；来源引用集；资格状态与具名原因；接地状态与指针；建议默认值标签；处置（§ 批次处置；无处置记 `pending`）；决策编号（已决项）或空。

### 决策记录(decision records)

- 每个已决项 MUST 恰产生一条 107 决策记录，文法与分层闭集不变；记录块位于批次记录之内（P-13 的既有载体），id 在该载体内稠密。
- 每条记录 MUST 同时携带批次族条件字段 `batch_id` / `batch_disposition` / `recommendation_grounding`（三者同批在场，仅批次产生的记录携带）；`batch_disposition` 取 `accepted-default` / `objected-alternative`，`recommendation_grounding` 取 `grounded` / `no-evidence`。
- `rationale` MUST 陈述建议依据与应答要点；`actor` MUST 按既有身份形态在场；`transmission_status` MUST 从 `not-transmitted` 起；`evidence` MUST 含接地指针、来源项指针与批次记录指针。
- 选择信号 MUST NOT 被写进 `chosen_option`（其值 MUST 保持为选项集中具名成员的精确标签）。

### 跨批次读写边界(cross-batch boundary, A-26)

- **写侧**：不同批次编号 MUST 写不同知识路径；一个批次 MUST NOT 写入、修改或删除他批记录（唯一例外 = 上款 `superseded_by` 追加），且 MUST NOT 依赖他批的**在途**状态。
- **读侧**：对他批**已落盘**批次记录的读取只允许服务于声明的只读用途——已解决排除（§ 重放契约 之外的读时联接规则见 § 批次状态）、接地联结（§ 建议默认值与依据）、前例冲突检出（同上）与重放指针解析（§ 重放契约）——且 MUST 只读。
- `.specify/register.md` 保持持久编号的唯一索引；编号冲突按既有 renumber 机制修复，MUST NOT 静默改号。

## 批次登记与来源更新（Register Reflection & Source Updates）

本节拥有批次对既有登记与来源载体的更新义务：登记什么、何时登记、状态单元格如何更新、`resolution` 如何追加、失败如何披露。

### 登记时点与形态(birth registration)

- 批次编号（`B-…` 形态）与各决策编号 MUST 在诞生时登记于 `.specify/register.md`（逐条或按「载体 + 区间」分组行合法）；登记行 MUST 指向批次记录载体路径，使编号可回指其陈述。
- `.specify/register.md` 保持持久编号的唯一索引（指针：`.specify/instructions.md` § ID Register）；编号冲突按既有 renumber 机制修复，MUST NOT 静默改号。
- 登记动作面只追加行：批次编号行与决策编号行是批次向 register 追加的全部新行。

### 状态单元格(status cells)

- 已决项的 register 来源行 MUST 只更新**状态单元格**：新的状态以 `resolved` 起头并点名批次编号与决策编号；该行的其余单元格 MUST 逐字节不变；行 MUST NOT 被删除。
- 暂缓项的 register 来源行 MUST 保持以 `open` 为起始词（保持下一批次可枚举）并标注批次编号；除状态单元格外的字节不变。
- 除状态单元格与追加行外 MUST NOT 改写 register 的任何字节；历史行（含已解决行）MUST NOT 被触碰。

### 来源块追加(source block annotation)

- 已决项的待决策项块 MUST 追加条件字段 `resolution`，取值 `<batch_id> -> <D-NNN>`；块内容 MUST NOT 因解决而改写或删除，该追加是块的唯一写后变化。
- 暂缓项的块 MUST NOT 被追加 `resolution`，下一次批次 MUST 重新呈现该项。

### 缺席登记册(absent register)

- register 缺席时 MUST 先按既有四列表头形态创建，再执行登记；创建后的文件与既有登记形态一致，MUST NOT 新增索引或第二登记。

### 失败披露与读时联接(failure disclosure and read-time join)

- 任一来源更新失败（register 或来源块不可写）MUST 被披露，点名载体与原因；MUST NOT 被静默吞掉，MUST NOT 使已落盘的批次记录回滚或改写。
- 读时联接（§ 批次状态 的 `already-resolved`）MUST 阻止已决身份因来源更新失败而被重复呈现——批次记录本身即足以排除，登记与块字段只是来源侧的镜像。

## 重放契约（Replay Contract）

本节拥有重放（replay）的定义与义务：重放只凭已记录载体重建整批，只读、确定、不补足。

### 定义(definition)

- 重放 MUST 只凭**批次记录 + 可解析指针**重建整批；重建范围 MUST 覆盖：项集（逐项行表）、完备性记账（逐来源计数、分区恒等式与判定）、建议默认值与接地状态、异议与处置、以及全部决策记录（含批次族字段）。
- 重放 MUST NOT 读取呈现载荷、应答工件或对话记忆来补足记录缺失的字段；记录未携带的内容 MUST NOT 被重放推测或补造。

### 指针与失败(pointers and failure)

- 重放 MUST 解析决策记录 `evidence` 字段与选项 `evidence` 子行的每一条指针（读法与 M-09 一致：路径存在；给出锚时锚可在载体中找到）。
- 任一不可解析指针 MUST 被点名报告，重放 MUST 以非零退出；MUST NOT 跳过坏指针，MUST NOT 以其可解析部分冒充完整重建。
- 记录自相矛盾（逐项行表的已决处置没有对应决策记录、决策记录的批次编号与批次头不一致、批次族字段缺失或取值在域外）MUST 作为具名拒绝以非零退出，MUST NOT 猜测修复。

### 确定性与只读(determinism and read-only)

- 同一记录与同一工作区重复重放 MUST 产出逐字节一致的输出；重放 MUST NOT 写入任何载体。
- 重放属于 § 批次记录契约 声明的跨批次只读用途之一（重放指针解析）；他批已落盘记录的读取只可服务于该用途。

### 机器判定边界(engine judges)

- 项集、记账、处置与决策记录的重建、指针解析与自洽判断 MUST 由确定性引擎完成；「记录是否易读、重建是否宜用」是行为类判断，由评审承接面判定（名单见 § 强制边界 的 B 表，指针），MUST NOT 被机器声称覆盖。

## 完备性与拒绝（Completeness & Refusal）

本节拥有「完备性凭什么成立、什么情况整批拒绝、空集与缺席如何明说、引擎的退出语义」的规则。完备性是封闭清单声明（判据 owner：`shared/guidelines/closed-set-claims.md`，指针），不是观感。

### 完备性声明(completeness claim)

- 完备性 MUST 以封闭清单声明表达，逐要素为：**参照物** = 本次扫描的来源清单与候选集；**比较单元** = 每个候选的处置分类；**允许差集** = 恒为空集；声明 MUST 以指针携带判据 owner 的元素要求，MUST NOT 用未定义的聚合词（「其余」「未受影响」一类）充当比较单元或承载验收语义。
- 每个候选 MUST 被恰分类一次；记账恒等式「扫描候选 = 呈现行来源 + 合并引用 + 具名排除」MUST 成立；分区计数（`presented_rows` / `duplicate_merged` / `not_human_held` / `already_resolved`）之和 MUST 等于候选数。
- 完备性声明与逐来源计数 MUST 同时出现在扫描 payload 与批次记录头中；判定与计数 MUST 由引擎计算，MUST NOT 由呈现层改写。

### 拒绝(carrier-level refusal)

- 任一来源或候选**载体**存在但不可读或不可解析（文件 I/O 失败、目录不可枚举、register 表结构无法按列解析）MUST 触发整批拒绝：不呈现、不记录任何处置、给具名来源与原因、以文档化退出码退出。
- 拒绝 MUST NOT 呈现半批并称完备；被拒绝的尝试 MUST NOT 写任何载体。

### 块级缺陷(block-level defects)

- 块级文法缺陷（未知/重复/畸形字段、声明计数与条目数不符、选项五要素缺失）不触发拒绝，按 `incomplete` 呈现并逐项点名（指针：§ 待决策项块 / § 批次状态）。

### 缺席与空集(absence and emptiness)

- 来源缺席（文件/目录不存在）MUST 记为带原因的缺席空来源，MUST NOT 使整批拒绝，MUST NOT 被读成「干净」；完备性声明 MUST 具名列出缺席来源，判定 MUST 如实标注缺席。
- 零候选 MUST 产出显式 `nothing-pending` 成功结果（退出 0），MUST NOT 是空输出，MUST NOT 创建批次记录，MUST NOT 呈现空壳。

### 不静默丢弃(no silent drop)

- 既不能被呈现、也不能被具名排除的候选 MUST 是拒绝，MUST NOT 被静默省略；遗漏任何候选时，完备性声明 MUST NOT 被发出。

### 退出语义(exit semantics)

- 引擎退出码闭集：`0` 成功（含 `nothing-pending`）、`1` 文档化拒绝、`2` 用法或环境错误；退出码 MUST 在引擎 `--help` 正文与命令文档（指针：`docs/reference/commands/decide.md`）同批声明，形态遵循 `shared/definitions/script-interface-definitions.md`（指针）。

## 重决与取代（Redecision & Supersession）

本节拥有重决（redecision）的写入形态与取代链义务；决策记录文法归 § 决策记录，批次记录的 create-only 与写后边界归 § 批次记录契约，传递与回执义务归 § 传递与实施（指针）。

### 新增记录，绝不覆盖(add a record, never overwrite)

- 重决 MUST 产生一条**新**的 107 决策记录（文法与分层闭集不变；批次产生的记录携带批次族三字段），MUST NOT 修改、删除或静默改写旧记录的既有内容。
- 新记录 MUST 恰对应被重决的那一项；一条决策项在一次批次内恰产生一条记录。

### 取代字段(superseded_by)

- 被推翻的旧记录（其 `chosen_option` 与新选择不同）MUST 追加条件层字段 `superseded_by: <新 D-NNN> (<新记录载体路径>)`；该行是旧记录的唯一追加，追加前的既有字节 MUST 逐字节不变。
- 已携带 `superseded_by` 的旧记录 MUST NOT 被重复追加——取代链只能向前延伸；一次重决只追加当前链尾的旧记录。
- 当旧记录位于某条批次记录文件之内时，该单行追加是该批次记录唯一受许的写后变更（A-27）：它不是同一批次编号的第二条批次记录，不构成对 create-only 或跨批次写边界的违反，且不改变该文件的批次头、逐项行表与其余记录块。
- 旧载体不可读或不可写 MUST 具名拒绝该项的重决：整次记录零写入、不铸造批次编号、不登记，MUST NOT 把重决降级为「全新决策」。

### 传递与边界(transmission and boundaries)

- 重决不改变决策类别；每条记录的审计链分别成立。
- 批次决策被传递实施时 MUST 沿用 107 的审计链（记录 → 派发尝试 → 实施回执）与 § 传递与实施 的形态义务；批次 MUST NOT 生成第二条记录或第二条传输路径。
- 本节的批量决策面 MUST NOT 与 ai-harness 091 或任何外部决策治理能力对齐；批次 MUST NOT 访问网络、MUST NOT 写入反馈存储、MUST NOT 自动传输任何内容（零网络、零反馈存储写入、零自动传输）；`ai-autonomous` 决策 MUST NOT 被呈现、转换或授权（指针：§ 待决策项来源清单 的类别门）。
- 机器判定边界：追加形态、单行追加与既有字节保全是机器可判命题（M-15）；重决理由是否充分归 B-05 评审承接，取代时机是否恰当由人工决策评审承接，二者 MUST NOT 被机器声称覆盖。

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

本节拥有本特性的**机器可判/行为类分工**：十六条机器规则与九条行为规则的封闭名单、逐规则的唯一判据动作与转红条件、以及表—守卫对等和门控中性两项义务。两类规则的反向性质是本节的要点：机器规则 MUST 能被改坏的对象**转红**；行为规则 MUST 被具名评审承接，MUST NOT 被任何文档或测试声称机器覆盖。

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
| M-10 待决策来源清单与候选枚举 | `scan` | 载体存在但不可读或不可解析却未整批拒绝；候选被静默丢弃；缺席来源被读作「干净」 | 机器覆盖（只判在场读数与计数恒等） | `tests/fixtures/decision-batch/m10/` |
| M-11 待决策项块文法与身份联接 | `scan` | 块级缺陷未以具名原因点名；身份未逐字节合并；类别门未排除 `ai-autonomous`；`resolution` 字段或读时联接未阻止已决身份 | 机器覆盖（只判结构与具名原因在场） | `tests/fixtures/decision-batch/m11/` |
| M-12 批次呈现形态与记账恒等式 | `scan` | 呈现顺序非确定；逐项行数与记账恒等式不一致；`ai-autonomous` 呈现数非零 | 机器覆盖 | `tests/fixtures/decision-batch/m12/` |
| M-13 建议默认值与接地联接 | `scan` | 建议默认值不是声明的唯一默认成员；接地指针不可解析；前例冲突未检出 | 机器覆盖（只判联接与指针可解析性） | `tests/fixtures/decision-batch/m13/` |
| M-14 应答成员性与沉默资格 | `record` | 非成员或未知身份的应答未被具名拒绝；非 `eligible` 项被沉默结案；无人值守或未声明授权未被拒绝 | 机器覆盖 | `tests/fixtures/decision-batch/m14/` |
| M-15 批次记录结构与创建性 | `record` | 批次编号形态错；同编号二次写入未被拒绝；批次族字段缺失或不同批在场；登记与来源更新越出状态单元格与追加行 | 机器覆盖（只判结构与字节边界） | `tests/fixtures/decision-batch/m15/` |
| M-16 重放确定性与指针解析 | `replay` | 重放写入载体；同一记录两次重放输出不一致；任一不可解析指针却以 0 退出 | 机器覆盖（只判结构与可解析性） | `tests/fixtures/decision-batch/m16/` |

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
| B-08 批次呈现可读性与后果真实性 | 人工决策评审 + `/speckit.review` 产物段 | 行为类，不声称机器覆盖 |
| B-09 建议理由充分性 | `/speckit.analyze` + `/speckit.review` | 行为类，不声称机器覆盖 |

### 表—守卫对等(table–guard parity)

- 每条 M 规则恰有**一个**确定性判据动作与**一个**转红条件（上表逐行）；改变判据动作或转红条件 MUST 先修订本节。
- 判据动作取两种形式：107 的九条规则取 `--action <动作>` 形式；批量规则（M-10…M-16）取批次引擎的文档化位置动作形式（`scan` / `record` / `replay`），逐行仍恰有一个动作。测试按两种形式分别断言（`tests/contract/test_decision_governance_guards.py`）。
- 测试侧的守卫花名册（`tests/contract/test_decision_governance_guards.py` 的 `GUARD_ROSTER`）与本节 M 表 MUST 行集一致；行为面名单与 B 表 MUST 行集一致——任一方向缺一行即缺陷（C-407）。
- 每条 M 规则 MUST 配一个**逆向样本**（把被检查对象改坏后守卫转红）；无逆向样本的守卫视为缺陷（C-403）。
- 每条 B 规则 MUST 有具名承接面；文档与测试 MUST NOT 声称任何 B 规则被机器覆盖（C-402）。

### 门控中性(gate neutrality)

- 本特性 MUST NOT 新增阻塞式门控：`scripts/python/scan-confirmation-gates.py` 的治理后复扫 MUST 相对**有效基线**零新增命中（基线读数与重定基线裁定记录在实现证据中，FR-025）。
- **保全面（containment claim）**：三个受保护所有者产物 MUST 对有效基线逐字节一致，读数由 `git diff --quiet <有效基线>..HEAD -- <三路径>`（零 `--numstat` 行）给出；允许差异集恒为空。任何改动 MUST 与一条记录在案的**重定基线裁定**同批落盘（裁定形态归 requirements FR-025 与其载体）；无裁定的改动由 B-07 承接（评审，永不机器声称）。
