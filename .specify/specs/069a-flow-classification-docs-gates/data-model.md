# Data Model — 069a 执行/表达分类与文档型门禁

**Phase 1 output**（`/speckit.plan`，2026-10-24）。本文件只定义**本切片新增或触碰**的实体与字段；
判据正文、取值语义、门禁规则归各自 owner（`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`），本文件不复制。
`[[STR-001]]` / `[[STR-002]]` / `[[STR-004]]` 是 `requirements.md` § Shared Strings 的引用记号，字面量只在该表维护。

存储形态说明：本切片**没有数据库、没有项目侧数据文件**。E1–E5、E9、E10 是「文档内声明 + 派生解析」；E6–E7 是「文档内的标注 + 检查器输出」；
E8 是每特性一份的 Markdown 记录（随规格入库）。

---

## E1 — Flow Unit（流程单元，派生）

被分类的最小对象。**不落盘**：由检查器扫描仓库得到。

| Field | Type | Source | Notes |
|-------|------|--------|-------|
| `unit_id` | string | 派生 | 命令 = `/speckit.<stem>`；技能 = `skill:<dir-name>`（与 exec-quant 的 `unit_id` 同形，便于基线取数） |
| `kind` | enum | 派生 | `command` \| `skill` |
| `layer` | enum | 派生 | commands / external / internal（仅用于定位源文件，不入台账） |
| `source_path` | string | 派生 | 仓库相对路径：`templates/commands/<stem>.md` 或 `skills/{external,internal}/<name>/SKILL.md` |

**Derivation rules（实测口径）**
- 命令：`templates/commands/*.md` 的每个文件 → 1 个单元（2026-10-24 实测 27 个）。
- 技能：`skills/external/*/SKILL.md`（14）与 `skills/internal/*/SKILL.md`（37）→ 51 个单元；两层无同名冲突（`comm -12` 空）。
- **排除**：`.specify/skills/**`（镜像，不是源）、`skills/*/site/**`（运行期数据）。

**Validation**
- 单元 id 全局唯一（扫描后重复即 `duplicate`）。
- 清单规模低于反空真下限（命令 27 / 技能 51）→ `inventory-truncated`，检查器非零退出。

---

## E2 — Class Assignment（分类登记行，owner 内 Markdown 表）

台账的一行。**落盘**于 `shared/definitions/flow-class-definitions.md` § 逐流程台账。

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `unit_id` | string | 必选 | 形如 `/speckit.docs` / `skill:humanize`；见 E1 |
| `flow_class` | enum | 必选 | `[[STR-001]]` / `[[STR-002]]`；其他值 → `invalid-class` |
| `basis` | enum | 必选 | `behavior-oracle` \| `reader-oracle` \| `mixed-oracle`；`mixed-oracle` 行 MUST 附带父规格指针（本条取自父 §Edge Cases 首条，规范条款由 069b 承接，本 owner 不复述） |
| `neutral` | enum | 可选 | `yes` 或缺省；`yes` 表示该技能登记在类中立封闭清单（E3） |
| `notes` | string | 可选 | 一行依据/边界提示；不得复述判据正文 |

**Row grammar（可解析，不可含糊）**: `| <unit_id> | <flow_class> | <basis> | <neutral?> | <notes> |`。
首格是单元 id（与 `contract-clause-definitions.md` § 2 的「表格首格即声明」同构）；缺列或列数不符 → `row-malformed`。

**Cardinality**: 一个 `unit_id` 恰一行（FR-008）。同一 id 出现两行 = `duplicate`；两行取值相反 = `dual-class`（缺陷）。
**Completeness**: 台账单元集 ⊇ 清单单元集且 ⊆（无 `unknown` 行），两侧差集必须为空（FR-007）。

---

## E3 — Neutral Skill Entry（类中立条目）

封闭清单的一项，落 owner § 类中立清单。

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `unit_id` | string | 必选 | 必须是已存在的技能单元（E1） |
| `category` | enum | 必选 | `memory` \| `feedback` \| `evidence` \| `session`（封闭四值，回答「它承载谁的产物」） |
| `rationale` | string | 必选 | 一句话：为什么它没有自己的交付物 |

**Validation**
- 清单 ⊆ 台账且台账该行 `neutral: yes`；清单外出现 `neutral: yes` → `neutral-unlisted`。
- **类中立只豁免 FR-010 的同类约束**，不改变该单元自身的 `flow_class`（E2 仍是一个二值），也不豁免任何门禁（FR-010 后半句）。

---

## E4 — Gate Operator（门禁算子）

某类别在某阶段用来证明同一不变量的一项检查。**落盘**于 `shared/workflow/expression-gates.md` § 阶段算子表。

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `operator` | string | 必选 | 可执行入口（脚本 + 动作）或点名的既有流程，如 `validate-requirements.py`、`doc-consistency-check.py --faces reader,evidence` |
| `face` | enum | 必选 | `requirements-clarity` \| `reader-purpose` \| `evidence-asof` \| `structure-links-build` \| `fact-consistency` \| `review` |
| `stages` | list | 必选 | 取自 8 阶段名册的子集；不得为空 |
| `class` | enum | 必选 | `expression`（本切片只登记表达类算子；执行类算子集合不在本切片范围内） |
| `blocking` | enum | 必选 | `blocking` \| `advisory`；文档型门禁的阻断项 MUST NOT 低于既有 P0/P1 |
| `owner_pointer` | string | 必选 | 该面判据的唯一 owner（路径 + 章节锚） |

**Invariants**: 覆盖面 `= 6`；每面至少一个 operator；`blocking` 为 `advisory` 的 operator 不得是六个面中任一面的**唯一** operator。

---

## E5 — Reader Declaration（读者声明）

文档型交付物头部的两行声明。**落盘**在被检查文档内。

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `readers` | string | 必选 | 目标读者（沿用 `user-facing-comprehension.md` § 基准读者与覆盖协议 的基准读者，不新建第二套读者定义） |
| `reading_scenario` | string | 必选 | 阅读场景/要做的决定 |

**Form**: `**Readers**: <text>` 与 `**Reading scenario**: <text>`，位于文档前 40 个非空行内。
**State transition**: 缺失 → `reader-declaration-missing`（阻断，FR-019）；两行存在但值为空 → 同一 finding。

---

## E6 — Evidence Annotation（证据标注）

事实性断言上的等级与时间戳。**落盘**在断言所在行内。

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `grade` | enum | 条件必选 | `实测` \| `推断` \| `引用`；三值封闭 |
| `as_of` | date | 条件必选 | `YYYY-MM-DD` |
| `source` | string | 可选 | 可复算来源（命令 / 退出状态 / URL / 路径） |

**Pairing rule**: 一条断言只要出现 `grade` 或 `as_of` 任一，另一项必须同时出现（FR-020）。
**Object boundary（不得混淆）**: 本实体描述**文档断言**；`shared/workflow/evidence-step.md` 的七态描述**机制证据**，`shared/guidelines/single-run-evidence.md` 描述**一次执行的记录留存**。三者取值域互不重定义。

---

## E7 — Consistency Finding（一致性发现，检查器输出）

**不落盘为持久存储**（除实现期证据文件外）；由 `doc-consistency-check.py` 输出到 stdout / `--json-out`。

| Field | Type | Notes |
|-------|------|-------|
| `face` | enum | `reader` \| `evidence` \| `duplicate` \| `count` |
| `rule` | string | `reader-declaration-missing` \| `as-of-malformed` \| `as-of-stale` \| `grade-asof-unpaired` \| `grade-invalid` \| `duplicate-fact` \| `count-mismatch`（取值集合与 `contracts/doc-consistency-checker.md` C-3/C-4/C-5/C-6 一一对应） |
| `path` | string | 仓库相对路径 |
| `line` | int | 起始行（1 基） |
| `snippet` | string | ≤ 120 字符的定位片段 |
| `counterpart` | string \| null | `duplicate-fact` 时的另一处 `path:line` |
| `fix_direction` | string | 一律「改为对唯一 owner 的引用」或「补齐标注」，不是「改措辞使其一致」 |

**Degradation**: 计数面委派不可用时输出 `count_check: {status: "not-run", reason}`；`--strict` 下该状态计为失败（不静默绿）。

---

## E8 — Baseline Record（表达类特性的三项基线）

**落盘**为 `<spec-dir>/notes/expression-baseline.md`（每特性一份，随规格入库；不是全局台账）。

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `feature` | string | 必选 | 规格目录 key |
| `frozen_at` / `frozen_commit` | date / sha | 必选 | 开工前冻结点（FR-024） |
| `gate_calls` | object | 必选 | `{value \| null, reason, derivation}`；来源 = `exec-quant.py --action list-records --since` + 声明的门禁单元集 |
| `confirmations` | object | 必选 | 同上；来源 = 门控观察记录（`--lifecycle-point gate-*`）+ clarify 提问轮次 |
| `wall_clock` | object | 必选 | `{value_minutes \| null, from_commit, to_record, derivation}`；来源 = requirements 首次提交 author date → analyze 完成记录时间戳 |
| `compared_at` | date | 收尾必选 | 与冻结值逐项对照的日期与结论（下降/持平/上升） |

**Validation**: 任一量无来源时 `value: null` + `reason`，**不得**记 0 或"达标"；收尾缺 `compared_at` 判不可验收。
**Owner boundary**: 仪器口径与 `not-evaluated` 降级的规范条款归 069b（父编号 041）；本实体只承载 069a 的冻结/对照要求。

---

## E9 — Class Lookup Result（类别解析结果）

`flow-class-check.py --action lookup` 的输出对象。

| Field | Type | Notes |
|-------|------|-------|
| `unit_id` | string | 请求的单元 |
| `flow_class` | enum | `[[STR-001]]` / `[[STR-002]]` |
| `source` | enum | `ledger` \| `default` |
| `marker` | string \| null | `source: default` 时恒为 `[[STR-004]]`；`ledger` 时为 null（FR-009：不得呈现为已判定） |
| `basis` | string \| null | 台账行的 `basis`；默认时为 null |
| `neutral` | bool | 是否命中类中立清单 |

**Exit codes**: 0 = 解析成功（含默认降级）；2 = 单元 id 形态非法或 owner 不可解析。
**Invariant**: `source: default` 时 `marker` MUST 非 null——这是 FR-016「不得静默切换」的机械面。

---

## E10 — Gate Call Site（门禁调用点）

某个入口在某个时点执行哪些门禁算子的登记行。**落盘**于 `shared/workflow/expression-gates.md` § 调用点表；
它是 E4（单个算子）到「谁在什么时候跑它」的绑定，不重复 E4 的面与阻断级别。

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `entry` | string | 必选 | 单元 id（`/speckit.docs`、`skill:create-docs`、`/speckit.humanize`、`skill:humanize`）——与 E1 同形 |
| `site` | string | 必选 | 入口内的时点：`docs` = `## Outline` 内分派之前；`create-docs` = R6 verify（两处）；`humanize` = Stage 6/Stage 7 |
| `lookup` | string | 条件必选 | 命令入口必选（`flow-class-check.py --action lookup --unit-id <id>`）；技能入口沿用调用方结果时可写 `inherit` |
| `operators` | list | 必选 | 本调用点执行的算子名（E4 引用）；docs 行为六面全集，humanize 行为 `062-*` 最小集 |
| `blocking` | enum | 必选 | `blocking` \| `advisory`；humanize 行以 062 的保真两项为 blocking |
| `owner_pointer` | string | 必选 | 门禁 owner 路径 + 章节锚（`shared/workflow/expression-gates.md`） |

**Invariants**
- 调用点集合 MUST 等于接线封闭集（`flow-class-ledger.md` C-15）的四个入口；新增行 = 扩面。
- 同一 `entry` 只登记一行（`create-docs` 的两处 R6 合成一行，`site` 注明两处）。
- `operators` MUST NOT 被命令模板或技能复制；模板只出现 `lookup` 与 `owner_pointer`。
- docs 行的算子集合 MUST 覆盖六面（C-3 的阻断底线作用于该行）；humanize 行 MUST NOT 含六面全集。
