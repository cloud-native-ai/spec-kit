# Contract: 推导模型执行面(Derivation Model Enforcement)(需求 048 / Feature 049)

**Requirement → Feature**: `048-derive-command` → Feature 049 Derivation Command
**概念真源**: `shared/definitions/derivation-definitions.md` —— record schema、四级溯源等级、链完整性规则 C1–C7、自审集 A1–A14、封闭禁用论证集、能力降级规则的**唯一定义点**。本契约 MUST NOT 复述其规则文本;它只规定**引擎如何机械执行**这些规则,凡涉及规则含义一律以「路径 + 节名」引用。
**消费方**: `scripts/python/derive-utils.py`(`validate`)、`templates/commands/derive.md`、`tests/unit/test_derive_validate.py`、`tests/contract/test_derive_model_enforcement.py`、概念锚漂移守卫测试

## 1. 执行面总则

- C-1 概念锚拥有**规则**,本契约拥有**执行机制**(错误码、违例输入形态、判定算法、语义残差归属)。二者冲突时以概念锚为准,并按 `shared/guidelines/one-source-of-truth.md` 的分歧程序修正本契约。
- C-2 每条违例 MUST 产出一个 error 对象,键固定为 `rule`(概念锚规则编号,如 `C3`/`A7`;自审表自身的形状违例用未编号的 `A0`)、`code`(本契约定义的稳定 kebab-case 标识)、`locator`(可定位串:`D-004.derivation` / `S-002.verification` / `A-3.derived-from` / `moves.md#M-012`)、`message`(一句话,含触发值)。信封形状见 `contracts/derive-engine.md` §4。
- C-3 一个事实 MUST 只产出一个 error 对象,**去重键为 `(rule, locator)` 二元组**:同时命中 C 规则与 A 检查时 `rule` 取 C 编号,A 结果由 error 列表**派生**(§5),MUST NOT 二次记账。故同一处孤儿前提被 C1、A2、A4 三条规则同时指向时,`errors[]` 里只有一条(`rule: C1`,locator 相同),A2/A4 的 `result` 由该条派生为 `fail`。
- C-4 引擎 MUST 区分 error 与 warning:`errors[]` 非空 → `validate` 退出码 4([[STR-004]]);warning 只呈现,不改退出码、不进自审表 result 列。warning code 集由 C-44 穷举,引擎 MUST NOT 自行新增。
- C-5 一切机械判定 MUST 在单次 `validate` 调用内完成:零网络、零子进程、零对 agent 的提问。

## 2. 溯源等级与锚定规则

- C-6 `grade` 为**封闭四值枚举**(概念锚 §Provenance Grades)。引擎 MUST 校验成员资格:空值、拼写变体、大小写变体(`Primary`)、任何第五值一律 error `rule: C1`, `code: grade-not-in-enum`。枚举 MUST NOT 由 CLI flag、环境变量或产物字段扩充。
- C-7 **锚定规则**(概念锚同节「Anchor rule」):步骤 `premises` 中每个 `S-<k>` 的 grade MUST ∈ {`primary`, `authoritative-secondary`};否则 error `code: premise-grade-ineligible`(`rule: C1`),locator 记 `D-<k>.premises:S-<j>`。
- C-8 `leads` 为可选字段,MAY 携带 `community` / `unverified` 行,但每个 `S-<k>` MUST 仍存在于 `## Sources`,否则 error `code: unresolved-lead`(`rule: C1`)。`leads` 中的等级 MUST NOT 参与 C-7 判定,也 MUST NOT 参与置信度传播(§7)。
- C-9 `authoritative-secondary` MUST NOT 作为「与 primary 相冲突主张」的唯一锚点(概念锚同节)。机械可检的近似形态:步骤 `confidence == contested` 且其 `premises` 中无 grade=`primary` 的行 → warning `code: secondary-sole-anchor`。**取 warning 而非 error**:该规则的完整形态需要知道 primary 究竟反驳了什么(语义),引擎只检出结构可疑形。
- C-10 等级由**内容**而非救回方式决定(概念锚「Grade is capped by content, not by rescue」):引擎 MUST NOT 因 `access` 为 `wayback:<ts>` 或 `resolved_via == wayback` 而调整或质疑 `grade`;`wayback` + `primary` 是合法组合,MUST NOT 报警。`access` 与 `grade` 仅有的强制耦合来自概念锚 §Dead-Link Protocol:`access: unknown`(探活未能运行)而行 grade ≠ `unverified` → error `rule: A1`, `code: unknown-access-with-verified-grade`(引擎只报告,MUST NOT 自行改写 grade,同 C-35 的分工);`access: paywalled` 的等级按**公开摘要**判定,摘要是否足以支撑某个算子抽取是语义残差(C-50),引擎 MUST NOT 就此报警。

## 3. C1–C7 机械执行

| 规则 | 构成违例的输入(机械可判) | error `code`(`rule` = 该 C 编号) | 残差(归 agent 语义判断) |
|---|---|---|---|
| C1 | `premises` 的 `S-<k>` 不在 `## Sources` | `orphan-source-premise` | — |
| C1 | `premises` 的 `S-<k>` 等级不达标 | `premise-grade-ineligible`(C-7) | grade 本身的判定 |
| C1 | `premises` 的 `D-<j>`:`j > k` / `j == k` | `forward-step-reference` / `self-referential-step` | — |
| C2 | `move` 缺失、为空、或解析出的 `M-<nnn>` 计数 ≠ 1 | `move-count-not-one`(message 携带实际计数) | 该算子是否真适配本步 |
| C3 | `derivation` 或 `conclusion` 命中 `BANNED_JUSTIFICATIONS`(§4) | `banned-justification`(message 携带字面量 + 字段名) | — |
| C4 | `falsification` 去空后 ∈ {`none`,`n/a`,`na`,`-`,`—`,`无`} 或长度 0 | `falsification-vacuous-literal` | 是否为**真**反驳条件 |
| C4 | 归一化(C-22)后 `falsification` == `conclusion`,或一方包含另一方且长度差 ≤ 20% | `falsification-restates-conclusion` | 近义复述 |
| C5 | `confidence == contested` 而 `contested-with` 缺失/为空 | `contested-without-link` | 判别性问题的内容 |
| C5 | `contested-with: D-<m>` 不存在,或 `D-<m>` 未回指 `D-<k>` | `contested-link-unresolved` / `contested-link-not-reciprocal` | — |
| C5 | `contested` 步骤未被任何 `Q-<k>.why-undetermined` 以 `D-<k>` 字面量提及 | `contested-not-routed` | — |
| C5 | `confidence == derived` 的步骤其 `premises` 含 `contested` 步骤 | `contested-premise-in-derived-step` | — |
| C5 | 步骤 confidence 秩 > 其全部 `D-` 前提的最小秩(§7) | `step-confidence-above-premise-min` | — |
| C6 | `## Termination` 缺 `condition:` 行,或值 ∉ {`a`,`b`} | `termination-condition-absent` | 究竟是 (a) 还是 (b) |
| C6 | `## Termination` 声明的 budget ≠ 本次生效预算(生效次序归 `contracts/derive-engine.md` C-9) | `step-budget-diverges` | — |
| C6 | 步骤数 > 生效预算 | `step-budget-exceeded`(error) | — |
| C6 | 步骤数 == 生效预算 | warning `step-budget-reached` | — |
| C7 | `derivation` 去空后 < 40 个 Unicode 码点 | `derivation-empty-or-short` | 一般形态的结论洗白 |
| C7 | 归一化 `conclusion` == 归一化 `claimed_title` 或 `resolved_title`(任一被引来源) | `conclusion-equals-source-title` | — |

- C-11 C3 的扫描范围 MUST 恰为 `derivation` 与 `conclusion` 两字段(概念锚 §Banned Justifications)。引擎 MUST NOT 扫描 `prevents` / `applies_when` / `falsification` / `A-<k>.statement`:算子的 `prevents` 合法地**引用**禁用短语来命名它挡住的失败模式(如 “treating `best practice` as a justification”),扫这些字段会把护栏本身判成违例。
- C-12 C4「近同一」MUST 只用 C-22 归一化后的字符串相等或包含 + 长度差 ≤ 20%;MUST NOT 引入相似度阈值、编辑距离或任何需调参的度量。
- C-13 C7 的下限按 Unicode 码点计数,不按字节,中英混排同判。**实现期修订**:本条原先规定「< 40 码点**或**少于 2 行」双下限取或,但档案的记录形态是单行 `- derivation: <value>` 字段(见 `data-model.md` §持久化形态),一个 derivation 在结构上不可能跨两行,故第二肢不可满足、无任何实现能执行它。修订为仅保留码点下限;若将来把 derivation 改为多行块字段,须同时恢复第二肢并改引擎。
- C-14 `## Termination` 为引擎可解析的终止声明节:节标题与节内两行字面量归 [[STR-008]],其在档案中的位置归 `data-model.md` §持久化形态(冻结节序),`init` MUST 脚手架出该节。**为何需要它**:概念锚要求「运行声明触发的是哪一个条件」,但一个未被结构化的声明无法被程序校验;把它落成两行是 C6/A12 可测的最小形态。A12 据此分半 —— 步数对预算的计数归引擎,(a) 与 (b) 之别归 agent 声明,引擎只校验该声明存在且取值合法。

## 4. 禁用论证字面量集(引擎钉定副本)

- C-15 概念锚 §Banned Justifications 是该封闭集的**概念所有者**,`requirements.md` 以 [[STR-001]] 引用它。引擎 MUST 将其钉为模块级不可变常量 `BANNED_JUSTIFICATIONS`,取值逐字如下 —— 本清单是**引擎钉定副本**,不是第二处定义:

```python
BANNED_JUSTIFICATIONS = (
    "best practice", "best practices", "industry standard", "commonly accepted",
    "it is generally agreed", "everyone knows", "as is well known", "obviously",
    "业界通用", "业界最佳实践", "最佳实践", "众所周知", "经验之谈", "权威做法",
    "不言而喻",
)
```

- C-16 漂移守卫测试 MUST 断言三处集合逐字相等:引擎常量、概念锚 §Banned Justifications 的字面量行(按 ` · ` 分隔解析)、`requirements.md` 的 [[STR-001]] 行。任一处单独修改 MUST 使该测试失败。
- C-17 匹配算法:MUST 子串匹配(非词边界),故 `industry best practices` 同时含 `best practice` 与 `best practices`;MUST 只报**最长**命中字面量,避免同一片段重复记账(违反 C-3)。拉丁字面量 MUST 大小写不敏感(两侧 `str.casefold()`);CJK 字面量按原样比较(`casefold` 对 CJK 恒等,实现上可统一 casefold)。
- C-18 该集为**封闭集**:扩充 MUST 同时修改概念锚与引擎(C-16 的测试即该约束的执行面),MUST NOT 由 CLI flag、产物字段或单次运行决定。

## 5. A1–A14 执行归属

- C-19 `## Self-Audit` 为固定表,其列头字面量由 [[STR-002]] 定义。引擎 MUST 校验表头逐字等于该定义,行 ID 集恰为 `A1`…`A14`(14 行,无缺无多);不符 → error `rule: A0`, `code: audit-table-shape`。
- C-20 A1–A10、A12、A13 的 `result` MUST 由引擎**派生**:该 A 编号映射的 code 集(下表)在 `errors[]` 中命中数为 0 → `pass`,否则 `fail`。agent MUST NOT 手写这 12 行;产物值与派生值不符 → error `rule: A0`, `code: audit-result-diverges`(message 携带期望值)。
- C-21 A11 与 A14 MUST 由 agent 显式背书,`result` 取值封闭为 `attested` / `not-attested` / `pending`;引擎 MUST NOT 判其为 `pass`,也 MUST NOT 因 `pending` 报 error(它是待办,不是失败)。二者的 `method` 列 MUST 为可核查的一句话,MUST NOT 为 `engine` / `n/a` / 空 → warning `code: attestation-method-degenerate`。

| A | 映射 code 集(命中即 `fail`) | 执行备注 |
|---|---|---|
| A1 | `grade-not-in-enum`, `title-mismatch-*`, `verification-*`(§6 全部), `unknown-access-with-verified-grade`(C-10) | 每行 grade + 非空非泛化 verification |
| A2 | `premise-grade-ineligible`, `unverified-source-unrecorded` | 与 C1 同源(C-3);后者执行 FR-005(每个 `unverified` 来源 MUST 出现在 `## Unverifiable Sources` 并附理由)——实现期发现该 FR 原先无任何 error code 归属,故在此补入 A2 的映射集 |
| A3 | `resolved-title-not-cited` | 见 C-23 |
| A4 | `orphan-source-premise`, `unresolved-lead`, `forward-step-reference`, `self-referential-step` | 与 C1 同源 |
| A5 | `banned-justification` | 与 C3 同源 |
| A6 | `falsification-vacuous-literal`, `falsification-restates-conclusion` | 与 C4 同源 |
| A7 | `element-derived-from-missing`, `element-derived-from-unresolved` | 硬失败(C-24) |
| A8 | `element-confidence-not-minimum` | contested→derived 洗白是其实例 |
| A9 | `move-not-in-library`, `unmarked-move-copy`, `divergent-move-projection`, `superseded-move-applied` | 库侧不变量见 `contracts/move-library.md` |
| A10 | `open-question-link-unresolved`, `blocked-element-not-downgraded`, `contested-not-routed` | 双向可解析 |
| A11 | — | **agent 背书** |
| A12 | `termination-condition-absent`, `step-budget-diverges`, `step-budget-exceeded` | 引擎判「步数对生效预算」与声明的形状/取值;究竟 (a) 还是 (b) 为真归 agent(C-50),故本行判 `pass` 只表示声明齐备且计数合规 |
| A13 | `moves-library-hand-edited`(C-40), `newly-issued-move-unresolved`(C-41) | 独写者约束 + 「本次报告为新发放的算子都能解析到库行」 |
| A14 | — | **agent 背书** |

- C-22 **归一化函数 `normalize_text(s)`**(A3/C4/C7/A9 共用)MUST 按固定次序执行,任何实现都 MUST 逐字复现:① `unicodedata.normalize("NFKC", s)`;② `str.casefold()`;③ 删除 Unicode 类别以 `P`(标点)或 `S`(符号)开头的码点,以及 `\u200b`、`\ufeff`;④ 空白连续段 `\s+` 折叠为单空格后 `strip()`;⑤ 结果为空串时返回 `None`(表示「无可比内容」)。MUST NOT 引入相似度阈值或编辑距离。
- C-23 A3:对每个 `title_mismatch: true` 的来源行,凡 `premises` 或 `leads` 含该 `S-<k>` 的步骤,其 `derivation` 文本 MUST 逐字包含该行 `resolved_title`;缺失 → error `rule: A3`, `code: resolved-title-not-cited`。此处 MUST 大小写敏感逐字包含,**不用** C-22 归一化:标题是证据,归一化会抹掉改标题的差异本身。
- C-24 A7 为**硬失败**:`derived-from` 缺失/为空 → `element-derived-from-missing`;其中任一 `D-<k>` 不存在 → `element-derived-from-unresolved`。二者 MUST 使整个文件被拒(退出码 4),MUST NOT 降级为 warning。
- C-25 A10:`Q-<k>.would-resolve` 中每个 `A-<x>` MUST 存在,且 `A-<x>.open-questions` MUST 反列 `Q-<k>`;任一方向断链 → `open-question-link-unresolved`(locator 记断链方向)。被任何 `Q-` 阻塞的元素其 confidence MUST ∈ {`provisional`, `contested`},否则 `blocked-element-not-downgraded`。**与 C-38 的相容性(实现期发现并裁定)**:C-38 要求元素 confidence **等于**其 `derived-from` 各步骤的最小秩,而本条要求被阻塞元素为 `provisional` / `contested`;若某元素的步骤全为 `derived` 而它又被未决问题阻塞,两条规则**联立不可满足**。裁定:不给任一条开例外——未决问题真的落在某元素上,就意味着支撑它的链尚不完整,故该问题所依附的**步骤本身**MUST 为 `provisional`,元素经最小值传播自然继承 `provisional`,两条规则同时成立。若改为给 C-38 开例外,`provisional` 就会退化成可随手标注的装饰,而这正是 C-38 取「等于」而非「至多」所要防的。

## 6. `title_mismatch` 与 `verification`

- C-26 `title_mismatch` MUST 由引擎计算;agent 写入的值 MUST 被忽略并重算,产物值与重算值不符 → error `rule: A1`, `code: title-mismatch-asserted`。
- C-27 `title_mismatch = (normalize_text(claimed) != normalize_text(resolved))`,两侧均非 `None`。相等/不等是唯一判据,MUST NOT 有第三态。
- C-28 `resolved_title` 为空(死链无快照且归属搜索未命中)时 MUST 置 `title_mismatch = false` 并给 warning `code: unresolved-title`。**理由**:mismatch 是一个**双标题**断言;只有一个标题时报「不一致」会把「无从核实」误报成「被改标题」,恰好掩盖 SC-001 要检出的两类缺陷之一。
- C-29 `title_mismatch == true` 时 `claimed_title` 与 `resolved_title` MUST 双双非空,任一为空 → error `code: title-mismatch-without-both-titles`。
- C-30 同一 URL 的多个清单变体 MUST 去重为一行(URL 为来源身份键),变体在 `claimed_title` 单元格内以 Markdown 转义竖线 `\|` 分隔;列切分 MUST 用 `(?<!\\)\|`。此时 `title_mismatch` = **任一**变体归一化后 != `resolved_title` 归一化。
- C-31 `verification` MUST 是具体证据引用(概念锚 §Source Record)。引擎 MUST 施加两道硬检 + 一道软检,**次序为「裸断言 → 长度 → 证据记号」**:① `normalize_text` 后整串 ∈ `BARE_ATTESTATIONS`(C-32)→ error `rule: A1`, `code: verification-bare-attestation`;② 去空后 Unicode 码点数 < 16 → error `code: verification-too-short`;③ 不含任一**证据记号**(C-33)→ warning `code: verification-evidence-token-absent`。**实现期修订次序**:本条原先规定长度检查在前,但 `BARE_ATTESTATIONS` 的每个成员都不足 16 码点,长度检查会恒先命中而使 ① 永不可达——一个不可达的 error code 等于没有该检查。改为先判裸断言(更具体、信息量更大),再判长度下限,两道硬检遂各自可达。
- C-32 `BARE_ATTESTATIONS` 为引擎钉定的封闭集:`verified` / `checked` / `confirmed` / `ok` / `fine` / `good` / `n/a` / `na` / `none` / `-` / `—` / `已核实` / `已确认` / `已检查` / `无` / `略` / `经分析` / `见上`。概念锚只点名 `verified`;本集是执行面为「裸断言」这一**类**给出的封闭枚举,扩充纪律同 C-18。
- C-33 **证据记号**(命中任一即视为携带具体证据):`http://` 或 `https://` 开头的 URL;三位 HTTP 状态码 `\b[1-5]\d{2}\b`;wayback 快照时间戳 `\b(?:19|20)\d{12}\b`;搜索结果定位串 `search:\s*\S+` 或 `result #\d+`。
- C-34 最小长度取 16 的理由:`HTTP 200 on 2026-09-05` 这类最短的**真**证据也有 20+ 码点,而任何 ≤ 15 码点的串在该字段里都不可能是证据引用;16 是同时满足「不误伤真证据」与「拦下一切单词级断言」的最小整数阈值。
- C-35 C-31 任一硬检失败且 grade ≠ `unverified` 时,error 的 message MUST 附「honest grade is `unverified`」提示,但引擎 MUST NOT 自行改写 grade(等级判断归 agent,概念锚 §Script / Prompt Boundary)。

## 7. 置信度最小值传播

- C-36 `confidence` 为封闭三值枚举 `derived` / `provisional` / `contested`,秩 `RANK = {"derived": 2, "provisional": 1, "contested": 0}`;枚举外值 → error `rule: C5`, `code: confidence-not-in-enum`。
- C-37 **步骤级**(C5):`D-<k>.confidence` 的秩 MUST ≤ 其 `premises` 中全部 `D-<j>` 的最小秩;`premises` 只含 `S-` 时无此约束。违例 → `step-confidence-above-premise-min`(message 携带期望上界)。
- C-38 **元素级**(A8,概念锚 §Traceability Rule):`A-<k>.confidence` MUST **等于**(不只是 ≤)其 `derived-from` 各步骤的最小秩;不等 → `element-confidence-not-minimum`,message MUST 给出引擎计算的期望值。取「等于」而非「至多」:允许元素比其步骤更保守会让 `provisional` 变成可随手标注的装饰,读者无法从 confidence 反推链的真实强度,最小值是唯一可反推的取值。
- C-39 来源事后被降级时,最小值传播 MUST 自动拉低全部下游步骤与元素:引擎 MUST 在单次 `validate` 内按步骤序(C1 保证其为拓扑序)重算,C-37/C-38 的 error 即该情形的检出形态,MUST NOT 另设「降级传播」检查。

## 8. 算子库侧执行面(A9 / A13)

- C-40 A13 的机械形态 = 库独写者不变量:表头与分隔行逐字、每行恰 7 列、`M-\d{3,}` 语法、ID 严格单调递增、无重复 ID、无重复归一化 `inference_form`、`anchor` 为限定形式(概念锚 §Move Record)、引擎写入标记存在。任一不成立 → error `rule: A13`, `code: moves-library-hand-edited`,message MUST 指明子因(`row-shape` / `id-grammar` / `id-not-monotonic` / `duplicate-id` / `duplicate-form` / `anchor-form` / `header-marker-missing`)。引擎 MUST NOT 尝试修复库,只检出并报告。本契约只拥有该 error 的 code 与子因名;每项不变量的定义与判定细节归 `contracts/move-library.md` §1–§4,MUST NOT 在此复制。
- C-41 产物引用的每个 `M-<nnn>` MUST 存在于库中,否则 error `rule: A9`, `code: move-not-in-library`。A13 的精确判据(概念锚 §Self-Audit A13)由此派生:`## Reasoning Moves Applied` 中处置列为 `new` 的每一行,其 `M-<nnn>` MUST 解析到库中的一行 —— 即它经 `moves-add`(唯一写入者)落库,而不是被手写进产物;未解析 → error `rule: A13`, `code: newly-issued-move-unresolved`。
- C-42 **投影 vs 复写**(概念锚 §Projection, Not Copy):`## Reasoning Moves Applied` 中任何匹配 `^\| M-\d{3,} \|` 的行视为**复写行**,MUST 在紧邻上一行携带字面标记 `<!-- projection of moves.md#M-<nnn> -->` 且标记 ID 与行首 ID 相同。无标记 → `unmarked-move-copy`;有标记但归一化 `inference_form` 与库中同 ID 行不等 → `divergent-move-projection`。仅以 `M-<nnn>` 身份引用而不复写整行恒合法。该节复写的是**本次运行的处置**(运行相对,归 `data-model.md` §持久化形态),MUST NOT 复写库的 `status` 列。
- C-43 引用 `status: superseded` 的算子 → error `code: superseded-move-applied`。**理由**:`status` 是持久二值状态(概念锚 §Move Record),`superseded` 表示后续运行已判定该算子有误且为**终态**——它让该算子永久不可引用,再套用等于把已知缺陷重新导入链;确需该形状时 MUST 由 `moves-add` 落一条新行,MUST NOT 复活旧行。

## 9. warning 集(穷举)与无在线能力降级

- C-44 引擎 `validate` MAY 产出的 warning code 恰为六个,MUST NOT 增删:`secondary-sole-anchor`(C-9)、`unresolved-title`(C-28)、`verification-evidence-token-absent`(C-31)、`step-budget-reached`(C6 表)、`attestation-method-degenerate`(C-21)、`degraded-run`(C-46)。
- C-45 降级判据(MUST 全部成立):`## Sources` 非空且每行 grade == `unverified`;每行 `verification` 归一化后**等于** [[STR-007]] 字面量;`## Derivation Chain` 无任何 `D-` 步骤;`## Derived Architecture` 为空或整节不存在。
- C-46 满足 C-45 时 `validate` MUST 退出 0,`payload.degraded` MUST 为 `true`,`notes[]` MUST 含一行以 [[STR-007]] 开头的降级说明,并给 warning `code: degraded-run`。**理由**:诚实的空产物不是失败;判成 error 会诱导 agent 编造核实来「变绿」,那是本命令存在的唯一理由的反面。
- C-47 部分降级 MUST NOT 被当作降级:任一行 grade ≠ `unverified`,或存在任何 `D-` 步骤,则 C-45 不成立,常规检查全部照常执行。特别地,`unverified` 来源出现在任何 `premises` 中 MUST 报 `premise-grade-ineligible`(C-7)—— 降级契约 MUST NOT 成为绕过锚定规则的后门。
- C-48 降级运行时可锚定步骤数 MUST 为 0(SC-005 的机械锚点):`payload.steps.total == 0` 且 `payload.steps.anchorable == 0`。

## 10. 语义残差与背书契约

- C-49 `validate` MUST 在信封顶层返回 `semanticChecksPending`,其值恒为字面量 `["A11", "A14"]`([[STR-002]]),**与产物当前背书状态无关**。该键的语义是「这两项永远不可被继承为绿」;逐项背书状态另由 `payload.audit.semantic` 给出(`attested` / `not-attested` / `pending`)。
- C-50 以下为**不可程序化**的语义残差,引擎 MUST NOT 假装判定,命令模板 MUST 交给 agent:A11(本次是否真的联网核实)、A14(产物陈述的是思维方式还是内容摘要)、grade 的最终判定、`paywalled` 来源的公开摘要是否足以支撑某个算子(摘要可支撑归属判定,MUST NOT 支撑需要完整论证的抽取;概念锚 §Dead-Link Protocol 第 1 步)、`applies_when` 过度使用护栏是否成立、`falsification` 是否为真反驳条件、C5 判别性问题的内容、C6 的 (a) 与 (b) 之别、`inference_form` 是否通过槽位测试(概念锚 §Litmus tests 2)。
- C-51 任一引擎检查为红时,产物 MUST NOT 把 `## Derived Architecture` 作为已推导结果呈现(FR-031);该义务的执行面是命令模板的收尾报告(`contracts/derive-command-template.md`),引擎侧的对应物是 `ok: false` + 退出码 4,MUST NOT 输出「部分成功」这类中间态。

## 11. 契约测试锚点

- C-52 参数化测试 MUST 遍历 [[STR-001]] 的每个字面量,对注入该字面量的 fixture 断言退出码 4 且 `errors[]` 含 `rule: C3`(SC-004)。
- C-53 逐规则夹具 MUST 覆盖上表每一行的违例输入形态,断言 `code` 与 `locator` 精确匹配;逐 A 编号夹具 MUST 断言 C-20 的派生结果与产物 `result` 列一致。夹具 MUST 含 `unknown-access-with-verified-grade`(C-10)与 `newly-issued-move-unresolved`(C-41)各一例,并 MUST 有一例断言 C-3 的 `(rule, locator)` 去重:同一处孤儿前提只产出一条 error 而 A2/A4 均派生为 `fail`。
- C-54 归一化函数 MUST 有独立单测钉死 C-22 的五步次序(全角折半、大小写、标点剥离、空白折叠、空串→`None`),因为 A3/C4/C7/A9 四处判定共用它,任一实现漂移都会同时改变四条规则的语义。
- C-55 warning 集 MUST 有穷举断言:对全部夹具运行后收集到的 warning code 集 MUST 是 C-44 六元集的子集,且六个 code 各有至少一个夹具触发它。
