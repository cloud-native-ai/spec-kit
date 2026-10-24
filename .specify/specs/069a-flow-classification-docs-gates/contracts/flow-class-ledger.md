# Contract: 流程分类所有者与台账（Flow-Class Owner & Ledger）

**Feature**: 069a（父 069） | **File scope**: `shared/definitions/flow-class-definitions.md`、`scripts/python/flow-class-check.py` | **FR served**: FR-001、FR-002、FR-005、FR-007、FR-008、FR-009、FR-010、FR-011、FR-015、FR-016、FR-017、FR-025

条款形态遵循 `shared/definitions/contract-clause-definitions.md` § 3 的规范形态（`**C-N**`）。本契约不复述判据正文——判据归 owner；这里只钉住**位置、形态与机械判定**。

- **C-1** 唯一所有者位置

分类的唯一所有者是 `shared/definitions/flow-class-definitions.md`。它 MUST 拥有：判据、两个取值、边界例、逐流程台账、类中立封闭清单、命名空间消歧、变更记录。
其他任何位置 MUST NOT 以表格、YAML、JSON 或代码常量的形式再声明一份「单元 → 类别」的映射（镜像除外）。
仓库中 MUST NOT 出现第二份分类数据文件。

- **C-2** 判据不被复述

凡消费分类的文档 MUST 以路径 + 章节锚引用所有者，MUST NOT 复述判据句或取值定义。
合同测试 MUST 以「owner 中的判据段落是否在消费方被逐字/近逐字重现」为负向断言；命中即失败。

- **C-3** 取值与命名空间键

`flow_class` 是机器可读键（列名、JSON 键、CLI 参数统一用它）。取值仅两个：`[[STR-001]]` 与 `[[STR-002]]`。
`execution` 出现在 `flow_class` 之外的语境时不得被读作本分类（与 Agent Execution 同词异义，消歧归 owner § 命名空间）。
`[[STR-001]]` / `[[STR-002]]` / `[[STR-004]]` 的字面量唯一落 `requirements.md` § Shared Strings；实现与测试引用该表（测试内固定字面量属「防漂移的固定副本」，合法）。

- **C-4** 台账行语法

台账是一张 Markdown 表，**一行一个流程单元**，首格为该单元 id：

```text
| unit_id | flow_class | basis | neutral | notes |
```

- `unit_id`：命令为 `/speckit.<stem>`，技能为 `skill:<dir-name>`。
- `basis`：`behavior-oracle` / `reader-oracle` / `mixed-oracle`。
- `neutral`：`yes` 或缺省。
- 列数不符、缺必选列、单元 id 形态非法 → `row-malformed`。解析器 MUST NOT 猜列。

- **C-5** 完备性与反空真下限

对账 MUST 以仓库清单为准：`templates/commands/*.md`（命令）与 `skills/external|internal/*/SKILL.md`（技能）。
清单单元集与台账单元集 MUST 双向覆盖：清单有而台账无 → `missing`；台账有而清单无 → `unknown`。两者任一非空即失败。
反空真下限 MUST 是实测常量（命令 27 / 技能 51）；清单实际规模低于下限 → `inventory-truncated`（失败），使「零缺口因为表完整」与「零缺口因为没解析到」可区分。
`--action check` 的 `--repo` 默认取脚本自身解析出的仓库根；MUST NOT 在客户项目里因缺少 `skills/` 目录而静默返回零缺口——此时报 `inventory-truncated`。

- **C-6** 互斥与唯一

同一 `unit_id` 在台账中 MUST 恰好出现一次；重复 → `duplicate`。
同一 `unit_id` 的两行取值相反（或存在独立来源给出相反取值）→ `dual-class`。
`invalid-class`：取值不在两值之内。以上三类 MUST 各自独立报告，不得合并成一个"有错"。

- **C-7** 未声明默认与标记

未登记单元 `--action lookup` MUST 返回 `flow_class = [[STR-001]]`、`source = default`、`marker = [[STR-004]]`，退出码 0（不中断流程）。
已登记单元 MUST 返回 `source = ledger`、`marker = null`——不得把已判定伪装成默认，也不得把默认伪装成已判定。
owner 不可解析 / 版本不兼容（如台账表头缺失）时，`lookup` MUST 降级为默认并保留 `marker`，同时在 stderr 报 `owner-unparsable`；MUST NOT 静默切换门禁集。

- **C-8** 类中立封闭清单

类中立条目 MUST 满足：在台账中存在且有二值类别；`neutral: yes`；`category ∈ {memory, feedback, evidence, session}`；带一句 `rationale`。
清单外出现 `neutral: yes` → `neutral-unlisted`；清单内的技能 MUST 存在于技能清单。
类中立只豁免「命令与其委托技能同类」这一条约束，**不豁免任何门禁**（FR-010 后半句）。本合同不定义命令↔技能的机械核验形态（该形态由 069b 承接）。

- **C-9** 读取点与模板零副本

门禁在判定之前 MUST 经 `flow-class-check.py --action lookup` 读取类别。
`templates/commands/**` 与 `skills/**/SKILL.md` MUST NOT 出现类别赋值字面量（`flow_class = <value>`、`flow_class: <value>` 形态）；
出现即失败。类别 MUST 在无 wrap-up 面的流程（如 `/speckit.humanize`）中同样可读——读取不经 wrap-up，故该断言由「模板零副本 + lookup 可用」共同满足。

- **C-10** 阶段不变量

本分类 MUST NOT 改变阶段集合；`/speckit.analyze` 与 `/speckit.review` 的调用率 MUST 为 100%；
阶段完整性判定 MUST NOT 读取类别。分类只选择门禁算子集（详见 `expression-gate-operators.md` C-1/C-3/C-11）。
台账或 owner 中 MUST NOT 出现「表达类可跳过/缩短某阶段」的表述；该表述出现即失败。

- **C-11** 首批成员

台账 MUST 登记 `/speckit.docs` 与 `/speckit.humanize` 为 `[[STR-002]]`，且二者的既有门禁与行为不被本切片修改：
`templates/commands/docs.md`、`templates/commands/humanize.md`、`skills/external/create-docs/**`、`skills/external/humanize/**` 在本切片中 MUST 零改动。

- **C-12** 变更审计

台账的每次类别变更 MUST 在 owner § 变更记录 留一行：`date | unit_id | before → after | basis | 依据`。
缺记录的变更视为静默改行为（FR-017）。变更记录 MUST NOT 被当作当前取值来源——当前取值只从台账主表读。

- **C-13** 命令面与退出码

```text
python3 scripts/python/flow-class-check.py --action check  [--repo <root>] [--format text|json]
python3 scripts/python/flow-class-check.py --action lookup --unit-id <id> [--repo <root>] [--format text|json]
```

- `check`：0 = 零 finding；1 = 任一 finding（`missing/unknown/duplicate/dual-class/invalid-class/row-malformed/neutral-unlisted/inventory-truncated`）；2 = 输入或解析错误（owner 文件缺失、表头缺失）。
- `lookup`：0 = 解析成功（含默认降级）；2 = 单元 id 非法或 owner 不可解析。
- `--format json` 的输出 MUST 至少含 `action`、`findings[]`（或 `unit_id/flow_class/source/marker`）与 `checked_at`（ISO-8601 Z）。
- 两个动作 MUST 只读：不写任何文件、不修改台账。

- **C-14** 客户项目侧的所有权

分类所有权归框架；客户项目 MUST NOT 覆盖框架流程的类别。
`--action check` 在客户项目中运行时报 `unknown`/`inventory-truncated` 而非"通过"——客户项目没有 `templates/commands` 源树，属预期形态；客户自建技能的类别声明面本切片不提供（父 A7 / FR-011 的 `MAY` 留给后续特性）。
