# Data Model — 087 架构图为核心的文档空间

**Feature**: 087 | **Date**: 2026-11-06 | **Stage**: plan (Phase 1)
**Authority**: 本文件**不拥有**任何取值域。实体字段、封闭 verdict / reason 集、`stale` 逐面判据、
追溯记录与豁免记录的 schema 的 owner 是 `contracts/diagram-obligation.contract.md`（下文以 `C-NNN` 引用）；
载体集合的分类含义归 `skills/external/create-docs/SKILL.md` § Desired-State Baseline；
图的语义模型 / 路由 / 交付契约归 `skills/external/draw-diagram/`。本文件只登记**实体、关系与状态迁移**，
每个字段以 owner 的锚点引用，MUST NOT 复述取值。

实体总数：**8**（E1–E8）。状态机：**2** 个（E3 的 verdict 判定、E4/E5 的记录生命周期）。

---

## E1 — Carrier Document（被判定文档）

| 字段 | 来源 / owner | 说明 |
|------|--------------|------|
| `path` | 盘上事实 | 相对项目根的 POSIX 路径（`C-005`） |
| `kind` | Baseline § Desired-State Baseline 第 1–2 项 | 六类正式目录内文档 / `ARCHITECTURE.md` / 非载体保留根文件 / notes / 归档 / 站点工具目录 |
| `in_carrier_set` | `C-003` 的载体表 | `false` 的文档**不进入** `documents[]`（不可见 ≠ 通过） |
| `references[]` | 文档正文的 Markdown 相对链 | 每条含 `target`（相对路径）与 `line`（行号，无引用时 `0`） |

关系：E1 1..* — E2（一个文档可引用多张图，`FR-009`）/ E1 0..1 — E5（豁免记录与文档路径一一对应）。

## E2 — Accompanying Diagram（配套图，两面一体）

| 字段 | 来源 / owner | 说明 |
|------|--------------|------|
| `source` | `C-010` `source`；扩展名表归 `references/delivery-contract.md` § D2 | 可编辑源，**每图恰一份**（`FR-009`） |
| `rendered[]` | `C-010` `rendered[]` | 渲染产物面；引擎不同则条数不同（`D2` 的表，本文件不复述） |
| `engine` | `C-010` `engine`；闭集归 `references/routing-matrix.md` | 引擎层名 |
| `engine_reason` | `C-010` `engine_reason` | 路由命中理由（独占登记 / 图类矩阵行 / tie-break） |
| `ldm_summary` | `C-010` `ldm_summary`；schema 归 `references/semantic-model.md` | 语义模型摘要 |
| `delivery.accepted` / `unmet[]` | `C-010` `delivery`；判据归 `references/delivery-contract.md` § D6 | 交付契约验收结论 |

不变量：
- **一面一身份**：`source` 与 `rendered[]` 是同一交付物的两个面，缺任一面即 `FR-008` 的失面报告对象；
- **单源不分叉**：多文档引用同一图时 `source` 只有一份（`FR-009`），更新 MUST NOT 生成副本；
- **引擎粘性**：既有图更新时 `engine` 与 `source` MUST 保持不变（`FR-010`），选引擎只发生在**新建图**。

## E3 — Verdict Record（逐文档判定）

| 字段 | owner | 说明 |
|------|-------|------|
| `path` / `line` | `C-005` | 逐文档具名（`FR-016`） |
| `verdict` | `C-004`（封闭五值 + 有序优先级） | `satisfied` / `missing` / `stale` / `recorded-exemption` / `not-evaluated` |
| `reason` | `C-005`（与 verdict 一一绑定的封闭表） | 闭集外的值是契约违规 |
| `summary.*` | `C-013` | 计数 + `clean` + `exemption_superseded` |

**状态判定（有序，命中即停）**：`recorded-exemption`（有效豁免）→ `missing`（含 `reference-unresolved` / `orphan-source`）→ `not-evaluated`（`C-012` 的四项）→ `stale`（`C-008` / `C-009`）→ `satisfied`（`C-007` 五条合取）。
优先级在 `C-004` 已冻结，本文件只登记它在实现上的落法：单趟顺序判断，**不回溯**、不二次覆盖。

`clean` = 四个计数全零（`C-013`）；`exempted > 0` 与 `carriers == 0` 都 MUST 使 `clean=false`（`FR-004` / `FR-016` 的假绿防线）。

## E4 — Diagram Trace Record（追溯记录）

| 字段 | owner | 说明 |
|------|-------|------|
| `run_id` / `feature` | `C-010` | 一次产生方运行一件 |
| `diagrams[]` | `C-010` | 每图一条，含 E2 的全部字段 |
| 落点 | `C-001` + `C-010` | `<root>/docs/.speckit/runs/<UTC>-diagram-trace.json`，一文一件 |

**生命周期**：由**产生方运行**写（文档流程的 R5/R6），检查器只读（`C-002`）。`FR-013` 的「未接受」= 记录缺失或不齐 ⇒ E3 落 `not-evaluated`，不是 `missing`（图在、只是没被接受）。

## E5 — Exemption Record（具名豁免记录）

| 字段 | owner | 说明 |
|------|-------|------|
| `document` / `reason` / `recorded_at` / `justification` | `C-011` | `reason` 封闭三值 |
| 落点 | `C-011` | `<root>/docs/.speckit/exemptions/<相对文档路径>.md` |

**生命周期**：无记录 → `missing`；记录有效 → `recorded-exemption`（可见，不计 pass）；记录缺字段或 `justification` 不足 → `not-evaluated` / `exemption-invalid`；记录仍有效但其文档**已带解析到渲染产物的引用** → `exemption-invalid` + `summary.exemption_superseded` 计数（`FR-004` 后半的唯一机械信号）。

## E6 — Fixture Space（夹具空间）

四段，全部纯文件（research `R5`：不依赖渲染后端、不依赖网络、不依赖 `pytest` 之外的东西）：

| 夹具 | 构成 | 断言的目标状态 |
|------|------|----------------|
| `clean/` | 1 份正式文档 + 1 图两面 + 追溯记录 + 解析引用 | 全 `satisfied`，`summary.clean=true` |
| `missing-face/` | 同 `clean/`，删渲染产物 | `missing` / `orphan-source`；删源则 `missing` / `orphan-source` 的对应面（`FR-023` 的负向） |
| `no-diagram/` | 同 `clean/`，删引用与两面 | `missing` / `no-diagram-reference` |
| `stale-source/` | 同 `clean/`，把源 mtime 推到渲染产物之后 | `stale` / `source-newer-than-render` |
| `exempt-ok/` `exempt-bad/` `exempt-superseded/` | 三条豁免记录各一（有效 / 缺 justification / 文档已带引用） | `recorded-exemption` / `not-evaluated` / `not-evaluated` + 计数 |

夹具同时是 `FR-023` 的「可观测负向」载体：同一夹具在删除一个面后 MUST 由绿转红，且 finding 点名该面。

## E7 — Flow Obligation Surface（义务落点）

不是数据实体，而是**被改动的文本落点集合**（义务落地的唯一登记处）：

| 落点 | 追加内容 | owner 边界 |
|------|----------|------------|
| `skills/external/create-docs/SKILL.md` § Desired-State Baseline | 配套图义务的一条基线条目 | 分类 / 保留名 / 一屏上限仍归本节 |
| 同上 § Authoring Flow R2/R5/R6 · § Reconcile Loop R6 | 图作为交付物、两面具名报告、检查器并列执行 | 确认分级、容忍带、归档不删除不动 |
| `skills/external/improve-docs/SKILL.md` § Workflow | 命名分类行 + 最小编辑规则 | § Ownership boundary 不动 |
| `templates/commands/docs.md` § Outline | 义务指针（新增小节，不改 W1 接线小节） | 顶层章节序列不动 |
| `docs/concepts/documentation-model.md` | 读者面投影一段 | 只引 owner，不定义规则 |

数量：**5 处落点、4 个文件**（`create-docs` 两个小节族同文件）。契约侧条款见 `contracts/flow-obligations.contract.md` 的 A–E 组。

## E8 — Guard Assertion Set（实施期必须保持的守卫）

| 守卫 | 钉住的字面量 | 契约锚 |
|------|--------------|--------|
| `test_expression_gate_wiring.py` A1 / A3 / A5 | W1 接线小节、`create-docs` 的 R6 文字、禁类别词 | `C-014` |
| `test_docs_command_template.py` C3 / C4a | `docs.md` 顶层章节序列、`improve-docs` 指针 | `C-014` |
| `test_confirmation_gates_sweep.py` KEEP_LIST | `stop-and-confirm` | `C-014` |
| `test_directory_governance.py` | `documentation-model.md` 留在 area-map | `C-014` |
| `test_expression_compatibility.py` C5 | 冻结清单哈希 + `ALLOWED_POST_BASELINE_CHANGES` 条目的 key 必须是 manifest 条目 | `plan.md` T-001 |

判据形态：**相对基线无新失败**（research `R6` 的实测基线：`tests/contract` 6038 passed / 17 failed / 2 skipped，其中 `test_residual_total_within_sc002_target` 先于本特性存在），MUST NOT 写成「全绿」。

---

## 关系图（实体间，文本形态）

```text
CarrierDocument (E1) --references--> RenderedArtifact (E2.rendered[])
        |                                    ^
        |                                    | same path (C-007 条件 2)
        v                                    |
  VerdictRecord (E3) <---judged with--- DiagramTraceRecord (E4)
        ^                                    ^
        |                                    | written by the producing run only (FR-013/FR-015)
        +---overridden by--- ExemptionRecord (E5)

FixtureSpace (E6) --instantiates--> E1..E5      FlowObligationSurface (E7) --lands on--> E2/E3/E4/E5 text
GuardAssertionSet (E8) --constrains edits to--> E7
```

## 状态迁移（E3 × E5，逐文档）

```text
none          --文档无引用--------------------> missing / no-diagram-reference
none          --引用存在但目标缺失------------> missing / reference-unresolved
none          --源在、渲染面缺----------------> missing / orphan-source
two faces ok  --无追溯记录--------------------> not-evaluated / no-trace-record
two faces ok  --记录缺必填字段----------------> not-evaluated / trace-incomplete
two faces ok  --记录齐备 + 引用解析------------> satisfied / reference-resolves
satisfied     --源 mtime > 渲染 mtime---------> stale / source-newer-than-render
satisfied     --盘上 sha ≠ 记录 sha-----------> stale / render-digest-mismatch
any           --豁免有效且未被事实推翻--------> recorded-exemption / exempt-chronological
any           --豁免失效（已带解析引用）------> not-evaluated / exemption-invalid (+superseded)
any           --渲染产物读不出----------------> not-evaluated / render-unreadable
```

迁移表是 `C-004` 优先级与 `C-005` 配对表的**同一份事实的两种读法**（按触发面 vs 按 verdict 优先级）；
冲突时以 `C-004`/`C-005` 为准。
