# 决策项定义(Decision Definitions)

**本文档是「决策项(Decision Item)」治理规则的唯一所有者(owner)。** 它拥有本特性的封闭词汇表、两类决策的强调与呈现模板、选项集契约、决策记录字段闭集与序列化文法、字段到所有者的映射、档案投影与封闭决策生产者清单、传递与实施回执义务、机器可判与行为类的强制边界，以及旧记录的判别与只读处置规则。其他任何面——instruction 段、决策项模板、技能与 agents、文档、检查器——MUST 以「指针 + 路径」抵达本文档，MUST NOT 复述其判据表；本文档 MUST NOT 复述任何相邻所有者的判据表。本文档不新建第二套登记、队列、存储或调度器；决策档案是既有载体的投影，`.specify/register.md` 保持持久编号的唯一索引。

## 所有权声明(Ownership Declaration)

本文档拥有、且只拥有以下九个面：

1. **决策词汇表(closed vocabulary)** —— § 封闭词汇表 定义的九个词；其他任何页 MUST NOT 另行定义这些词。
2. **类别呈现(class presentation)** —— 两类决策（`human-interactive` / `ai-autonomous`）的判定依据与各自的呈现模板及其强调义务。
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
