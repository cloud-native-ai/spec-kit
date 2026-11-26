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
