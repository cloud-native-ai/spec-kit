# Data Model: 决策反题与反指标契约（Decision Tension Record）

**Feature**: 076-decision-tension-contract → Feature 076 决策反题与反指标契约（Decision Tension Record）
**Spec**: [requirements.md](requirements.md)
**Note**: 本特性不新增数据库、台账或存储（FR-018）。所有实体都落在既有工件上：计划文件
（`.specify/specs/<key>/plan.md`）、requirements 的测量来源节、SI-4 派发载荷 / SI-7 intervention
记录、ADR 文件。本文件登记字段面与校验规则，是契约测试与两个确定性校验器的判定对象；字段
值域以本文件为 plan 期权威，实现后由脚本常量与契约测试共同钉住。

## 实体一览

| # | 实体 | 承载 | 本特性变更 |
|---|------|------|------------|
| E1 | Decision Tension Record（张力记录） | `plan.md` § Decision Tensions 下的 `### T-NNN` 子节 | 新增 |
| E2 | Binding Constraints（双极约束） | E1 的 `binding_constraints` 字段 | 新增 |
| E3 | Expected Sacrifice Binding（预期代价绑定） | E1 的 `expected_sacrifice` 值 | 新增 |
| E4 | Load-Bearing Predicate（承重判据） | 判定动作，无独立工件 | 新增（判据，非存储） |
| E5 | Falsification Quartet（证伪四元组） | SI-4 派发载荷 / SI-7 intervention 记录 | 新增（搭既有载体） |
| E6 | Rejection Reason（拒收原因） | `validate-falsification-quartet.py` 的判决输出 | 新增（封闭枚举） |
| E7 | Validator Check Label（校验标签） | `validate-decision-tensions.py` 的输出 | 新增（封闭枚举） |
| E8 | ADR Tension Reference（ADR 张力引用） | `docs/decisions/template.md` § Alternatives | 新增（引用位） |

## E1 — Decision Tension Record

**定位**：一条承重决策的可判定记录。生命周期是「写作 → 结构校验 → 分析检测 → 事后被 ADR 引用」，
不落地到任何新载体。

**记录边界**：一条记录以 `plan.md` 内三级标题 `### T-NNN` 起头（`T-` + 三位十进制数字），
至下一条 `### T-NNN` 或下一个 `##`/`###` 标题为止。记录标识 `tension_id` 就是该标题里的
`T-NNN`，不在正文里重复声明——一个标识一个定义点。

**行文法**（校验器的解析面，六个字段各出现一次）：

```text
### T-NNN — <一句话标题>
- **decision**: <单句>
- **antithesis**: <具名方案 + 条件句>
- **binding_constraints**:
  - pole_a: <约束>
  - pole_b: <约束>
- **discriminating_evidence**: <可执行、二值>
- **expected_sacrifice**: <SC-NNN> Source <↓|↑> <阈值/说明>
- **revision_trigger**: <条件 → 动作>
```

标题行承载 `tension_id`；六个字段以 `- **<字段名>**:` 起头（字段名逐字、只出现一次），
`binding_constraints` 的值由其下两行 `- pole_a:` / `- pole_b:` 承载。围栏代码块内的同形行
不计入记录（与契约条款的围栏规则同源，不自立第二套）。

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `tension_id` | `T-NNN`（三位数字） | 同一计划内唯一；按出现顺序递增（1, 2, 3 …）；不得跳号 |
| `decision` | 单句 | 点名被选中的**一极**；不得同时陈述两极为可选 |
| `antithesis` | 具名方案 + 条件句 | 必须可被独立采纳；必须给出至少一条「在什么条件下它更优」；不得是「什么都不做」或被选方案的弱化版 |
| `binding_constraints` | E2 结构 | `pole_a` 与 `pole_b` 均非空；被选方案不得同时满足两极 |
| `discriminating_evidence` | 一次观测/实验 | 一位复核者可执行；结果二值（能判定哪一极更对） |
| `expected_sacrifice` | E3 形态 | 恰解析到一条已声明测量来源；方向记号必须是 `↓` 或 `↑` |
| `revision_trigger` | 条件 + 动作 | 必须写出「指标恶化到什么程度 / 出现什么证据 → 重开」，不得只写「持续观察」 |

**校验规则**（与 `validate-decision-tensions.py` 的标签逐条对应）：

| 规则 | 判据 | 标签 | 违规严重度（analyze） |
|------|------|------|----------------------|
| R1 章节存在与锚点 | `## Constitution Check` → `## Decision Tensions` → `## Project Structure` 三行相邻 | `dtr-anchor` | HIGH（章节缺失时抑制：只报 R2） |
| R2 章节缺失 / 裸 `N/A` | 无该章节，或有章节但 `N/A` 未逐条说明四类触发均不成立 | `dtr-section-missing` | HIGH（与 R1 同红时优先） |
| R3 六字段齐备 | 六个字段标签各出现一次；`decision` / `antithesis` / `discriminating_evidence` / `revision_trigger` 的值非空；`expected_sacrifice` 与两极的值留空归 R5 | `dtr-record-incomplete` | HIGH（空值不在此判，见去重规则 ③） |
| R4 标识形态 | `T-NNN`、唯一、按序递增 | `dtr-tension-id` | HIGH |
| R5 拒绝形态 | 命中 owner 的拒绝清单（含 `expected_sacrifice: none` 或留空、任一极点为空、不可判定措辞） | `dtr-rejected-form` | HIGH |
| R6 代价可映射 | E3 解析成功；字段标签缺失或值留空时不执行本规则 | `expected-sacrifice-unmapped` | HIGH |

**去重规则**：同一记录同一标签只报一条。跨标签优先级三条：① 章节缺失 → 只报
`dtr-section-missing` 并抑制 `dtr-anchor`（三行相邻断言在章节不存在时必然同红，同一根因不计两次）；
② 六个字段标签行任一缺失 → 只报 `dtr-record-incomplete`，且不再叠加 `expected-sacrifice-unmapped`
（缺字段即无可解析值）；③ 值为空（`expected_sacrifice` 值留空、`pole_a` 或 `pole_b` 行缺失或留空）
或 `expected_sacrifice` 恰为 `none` → 只报 `dtr-rejected-form`，抑制 `dtr-record-incomplete` 与
`expected-sacrifice-unmapped`（空值没有可判定内容，否则 SC-001 的反向夹具会被双计数）。六个标签覆盖
锚点断言、三类缺陷与两个记录级形态（标识、拒绝形态），不是与四件事的一一对应。

## E2 — Binding Constraints

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `pole_a` | 单条不可让渡约束（字符串） | 非空；被选中的一极所坚持的约束 |
| `pole_b` | 单条不可让渡约束（字符串） | 非空；反题一极所坚持的约束 |

**判定**：若一个方案能同时满足两极，则该张力不成立（属可求解冲突），MUST 改写为双赢解或
降级为普通取舍，MUST NOT 保留为记录。这条判定是语义的（一位复核者可判），不是脚本判定——
脚本只判「两极是否都非空」。

## E3 — Expected Sacrifice Binding

**形态**：`<SC-NNN> Source <↓|↑>` + 自由说明（阈值/解释，不参与解析）。

| 组成 | 约束 |
|------|------|
| 标识 | `SC-NNN`，且 MUST 在 `requirements.md` § `### Measurement Sources & Collection Methods` 中有以 `**SC-NNN Source**` 起头的条目 |
| 连接词 | 字面 `Source`（与目标行同形，是唯一可直接对上的连接键） |
| 方向 | `↓`（指标变差为下降）或 `↑`（指标变差为上升）；缺省或取其他值判解析失败。**记录性断言**：程序只判取值落在两值内，不断言方向与来源指标的实际语义一致（那是复核者判断），值里也不要求写指标名 |
| 单值 | 一个记录只绑定一条来源；值中出现第二个 `SC-NNN` 判解析失败 |
| 尾部 | 阈值或说明自由书写，不参与解析 |

**解析状态**：`resolved` / `unmapped`（标识不存在、方向缺失或非二值、出现第二个标识、无 `Source`
连接词 → 一律 `unmapped`，MUST NOT 回落为人工阅读判定）。值的归属优先于解析状态：字段标签缺失走
`dtr-record-incomplete`，值留空或恰为 `none` 走 `dtr-rejected-form`，两者都不再报 `unmapped`
（见 E1 去重规则 ② / ③）。

## E4 — Load-Bearing Predicate

**形态**：判定动作，无工件。四类触发任一成立即承重：不可逆（回滚需迁移或重建）、跨团队
（改变他人依赖的契约或接口）、高爆炸半径（故障影响面超出本特性边界）、与宪法原则相关
（触及任一 MUST 条）。

**门控**：复杂度分级引用 `shared/guidelines/task-complexity-rubric.md`；Trivial 级按定义不含
承重决策；分级与承重判据冲突时按该 rubric 的 tie-break 取较高一级，并以承重判据为准。

**反空真**：`/speckit.analyze` 的检测器 MUST NOT 自行判断「计划里是否存在承重决策」——缺少章节
一律判 HIGH（fail-closed），所以这个谓词只服务于**写作侧**与 N/A 说明，不服务于检测侧。

## E5 — Falsification Quartet

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `attempt` | 命令 / grep / 测试 / 测量 | 一位复核者可原样重放；脚本 MUST NOT 重放它，也 MUST NOT 判「可否重放」——可重放性是复核者规则，脚本只判非空 |
| `exit_code` | 整数（0 合法） | 非整数即拒收 |
| `observation` | 以字面 `raw:` 起头的原样摘录 | 无该标记即 `observation-not-raw`（「非转述」的机械代理） |
| `would_go_red_if` | 以第一次出现的字面 `red:` 切分（后续 `red:` 不移动切分点）；输入半：切分点之前的反引号跨度（被改坏的具名输入）；信号半：切分点之后至少一个反引号跨度（断言名 / 检查标签 / 非零退出码） | 缺 `red:` 标记或缺任一半即 `tautology`；只判形状，不判「改坏后是否真会变红」（后者属复核者与 SI-6） |

**载体**：SI-4 派发载荷、SI-7 intervention 记录（既有载体，不新增台账）。

## E6 — Rejection Reason（封闭六值）

| 值 | 触发 |
|----|------|
| `missing-field` | 四键中任一未出现 |
| `empty-field` | 键出现但值（含缩进续行）为空 |
| `exit-code-not-integer` | `exit_code` 值不是整数 |
| `observation-not-raw` | `observation` 值不以 `raw:` 起头 |
| `tautology` | `would_go_red_if` 未同时给出被改坏的具名输入与 `red:` 之后的具名红色信号：缺 `red:` 标记、第一次出现的 `red:` 之前无反引号跨度、该切分点之后无反引号跨度，任一成立即命中（多个 `red:` 以第一次出现切分，切分点唯一）。可重放性缺陷（`attempt` 无法原样重放）**不**在此集内，属复核者非阻断注记 |
| `input-unreadable` | 载荷不可读（退出码 2，按拒收处置） |

**判决者**：`scripts/python/validate-falsification-quartet.py`。接收方 agent MUST NOT 反向覆盖，
也 MUST NOT 在封闭集之外另立拒收理由；额外疑虑只能写成非阻断注记。

## E7 — Validator Check Label（封闭六值）

`dtr-anchor` / `dtr-section-missing` / `dtr-record-incomplete` / `dtr-tension-id` /
`dtr-rejected-form` / `expected-sacrifice-unmapped`。

**输出形态**：人读模式 `status: <ok|error>` + 每标签一行 `[label] pass|fail (count)` + findings；
`--json` 模式 `{"spec","status","checks":[{"label","status","count"}],"errors","warnings","scanned"}`。
退出码 0 无错误（允许 warning）/ 1 发现错误 / 2 输入不可读。

## E8 — ADR Tension Reference

| 字段 | 取值/形态 | 约束 |
|------|-----------|------|
| `tension_id` | `T-NNN` | 指向同一特性计划中的记录；不复制记录字段；不解析到记录即断链错误 |
| 无记录时的表述 | 字面「无承重张力记录」+ 判定结论 | 不得留空，不得只写「不适用」 |

**解析器复用**：断链判定复用 E7 校验器的记录索引函数（一条实现两条消费：validator 的
`dtr-tension-id` 与 ADR 断链契约测试），不新写第二个记录解析器。

## 状态迁移

| 从 | 事件 | 到 | 判据 |
|----|------|----|------|
| 无记录 | 计划含承重决策 | 待写作 | E4 判定成立 |
| 待写作 | 写入 `### T-NNN` + 六字段 | 结构候选 | 六字段齐备（R3） |
| 结构候选 | `validate-decision-tensions.py --spec` | 结构通过 / 结构不通过 | 退出码 0 / 1 |
| 结构通过 | `/speckit.analyze` 结构通道 | 无发现 / HIGH | 三类缺陷各 0 条 / ≥1 条 |
| 结构通过 | 事后写 ADR | 被引用（`tension_id`） | E8 解析成功 |
| 任意 | 后续阶段新增承重决策 | 待写作（复跑必须仍能检出） | 计划更新 |

## 与既有实体的边界

- 承重决策的**判据**（E4）与记录形态（E1）只在 `shared/guidelines/decision-tension.md` 定义；
  本文件是 plan 期的设计投影，实现后由该 owner 与契约测试共同钉住，本文件不复述其判据表。
- 四元组（E5）的字段语义与拒收规则 owner 是 `shared/guidelines/critique-and-self-critique.md`；
  本文件只登记字段面与封闭枚举，供契约测试引用。
- 测量来源（E3 的目标）的 owner 是该特性自己的 `requirements.md` § Measurement Sources，
  本文件不复写其条目清单。
