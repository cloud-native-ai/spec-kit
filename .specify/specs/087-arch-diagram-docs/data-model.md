# Data Model — 087 架构图为核心的文档空间

**Feature**: 087 | **Date**: 2026-11-06 | **Stage**: plan (Phase 1)
**Authority**: 本文件**不拥有**任何取值域。实体字段、封闭 verdict / reason 集、逐文档判定的有序优先级、
`stale` 逐面判据、追溯记录与豁免记录的 schema 的 owner 是 `contracts/diagram-obligation.contract.md`（下文以 `C-NNN` 引用）；
载体集合的分类含义与**图的落点区域**归 `skills/external/create-docs/SKILL.md` § Desired-State Baseline；
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
| `source` | `C-010` `source`；扩展名表归 `references/delivery-contract.md` § D2 | 可编辑源，**每图恰一份**（`FR-009`）；落点 `docs/assets/`（T-005） |
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
| `summary.*` | `C-013` | 五个计数 + `converged` + `clean` + `exemption_superseded` |

**状态判定（有序，命中即停）**：唯一登记处是 `C-016` 的九行表（`recorded-exemption` → 失效豁免 →
`no-diagram-reference` → `reference-unresolved` → `orphan-*` → `trace-incomplete` → `no-trace-record` →
`stale` → `satisfied`）。本文件不复述该表，只登记它在实现上的落法：单趟顺序判断，**不回溯**、不二次覆盖。

**两个谓词，两个问题**（定义点在 `C-013`，本文件只登记它们的区别，不复述算式）：

| 字段 | 回答的问题 | 豁免的角色 |
|------|-----------|-----------|
| `converged` | 还有没有**待收敛**的 finding（`missing` / `stale` / `not_evaluated`） | 不阻断——豁免是 `FR-004` 的合法终态 |
| `clean` | 这个空间是不是**零 finding** 的显式结论 | 阻断——`exempted > 0` ⇒ `clean=false`（`FR-004` / `FR-016` 的假绿防线） |

⇒ **收敛判据用 `converged`**（`flow-obligations` `C-008a` R6、`SC-003`）；「零图 finding」= `converged`
「一个文档无结构可绘、已具名豁免」的收敛终态是 `converged=true` + `clean=false`，合法且不矛盾（`SC-008`）。
`carriers == 0` 使两个谓词**都**为假（判据没有对象，不是零 finding）。
`--only` 收敛到 0 个对象时两个谓词按公式都算得 `true`，但**那不是**空间合规的结论（`C-013` 的附注）。

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

**生命周期**：无记录 → `missing`；记录有效 → `recorded-exemption`（可见，不计 pass，但**不阻断** `converged`，只使 `clean=false`）；记录缺字段或 `justification` 不足 → `not-evaluated` / `exemption-invalid`；记录仍有效但其文档**已带解析到渲染产物的引用** → `exemption-invalid` + `summary.exemption_superseded` 计数（`FR-004` 后半的唯一机械信号）。**这四档里只有前两档是「已收敛」，后两档落 `not-evaluated`，因此使 `converged=false`**。

## E6 — Fixture Space（夹具空间）

全部纯文件（research `R5`：不依赖渲染后端、不依赖网络、不依赖 `pytest` 之外的东西）。**落点与形态**：
`tests/fixtures/docs-obligation/<name>/`，每个夹具是一棵**完整的迷你文档空间**（根 `README.md` +
`docs/<六类目录>/` + `docs/assets/` + `docs/.speckit/`），判据是 `--root` 指向该目录；
**每个产生写入的用例先把夹具 `shutil.copytree` 到 `tmp_path` 再操作**，因此仓库里的夹具永远是**删除前的绿灯态**
（先例：`tests/integration/test_docs_command_scenarios.py` 的 `make_skeleton(tmp_path)` 同形）。

| 夹具 | 构成 | `--record` | 断言的目标状态（`C-016` 的档位） |
|------|------|-----------|----------------------------------|
| `clean/` | 1 份正式文档 + 1 图两面（`docs/assets/foo.{mmd,svg,png}`）+ 引用解析 + 记录齐备 | 本夹具记录 | `satisfied` / `reference-resolves`；`summary.converged=true`、`summary.clean=true` |
| `no-diagram/` | 同 `clean/`，文档无任何指向图渲染产物的引用 | 本夹具记录 | `missing` / `no-diagram-reference`；`converged=false`、`clean=false` |
| `deleted-rendered/` | 同 `clean/`，渲染产物已删、源在、引用仍指向被删的渲染面 | 本夹具记录 | `missing` / `reference-unresolved`（`C-016` 序 4 **先于**失面序 5） |
| `orphan-rendered/` | 同 `clean/`，渲染产物已删、源在、**引用指向源**（解析成功） | 本夹具记录 | `missing` / `orphan-rendered`（`C-016` 序 5） |
| `orphan-source/` | 同 `clean/`，源已删、渲染产物在 | 本夹具记录 | `missing` / `orphan-source`（`C-016` 序 5） |
| `stale-source/` | 同 `clean/`，两面**都在**，源 mtime 严格晚于最早的渲染面 | 本夹具记录 | `stale` / `source-newer-than-render`（`C-016` 序 8） |
| `no-trace/` | 同 `clean/`，两面与引用都在，**不给** `--record` | 缺省 | `not-evaluated` / `no-trace-record`（序 7）；`converged=false` |
| `trace-incomplete/` | 同 `clean/`，记录在但 `diagrams[]` 无同名条目 / 缺必填字段 | 本夹具记录 | `not-evaluated` / `trace-incomplete`（序 6） |
| `exempt-ok/` | `C-011` 三字段齐备的豁免记录，文档无图 | — | `recorded-exemption` / `exempt-chronological`；`exempted=1`；**`converged=true`**、`clean=false`（`C-008a` 的豁免收敛夹具） |
| `exempt-bad/` | 豁免记录缺 `justification`（或长度 < 8） | — | `not-evaluated` / `exemption-invalid`（序 2）；`converged=false` |
| `exempt-superseded/` | 豁免记录齐备，但文档**已带**解析到渲染产物的引用 | 本夹具记录 | `not-evaluated` / `exemption-invalid` + `summary.exemption_superseded=1`；`converged=false` |

**mtime 必须是夹具的显式事实，不是检出顺序的副产品**：`stale-source/` 在 `conftest` 的建造步骤里用
`os.utime` 把 `source` 设为「渲染面 mtime + 60s」（写在 `.gitattributes` 之外，不进版本库），
否则 `git checkout` 的写入顺序会让该夹具随机器而红或绿——一条会自己变色的判据等于没有判据。

夹具同时是 `FR-023` 的「可观测负向」载体：同一夹具在删除一个面后 MUST 由绿转红，且 finding 点名该面。

## E7 — Flow Obligation Surface（义务落点）

不是数据实体，而是**被改动的文本落点集合**（义务落地的唯一登记处）：

| 落点 | 追加内容 | owner 边界 |
|------|----------|------------|
| `skills/external/create-docs/SKILL.md` § Desired-State Baseline（+ 其 `#### Assets` 条目） | 配套图义务的一条基线条目；图的落点按该条目（T-005） | 分类 / 保留名 / 一屏上限仍归本节 |
| 同上 § Reconcile Loop R3/R4/R5/R6 · § Authoring Flow R2/R5/R6 | 图作为差异项与交付物、R5 **产图/重渲染**（收敛路径 `flow-obligations` C-008a）、两面具名报告、检查器并列执行 | 确认分级、容忍带、归档不删除不动 |
| `skills/external/improve-docs/SKILL.md` § Workflow 2–5 | 命名分类行 + 最小编辑规则 | § Ownership boundary 不动 |
| `templates/commands/docs.md` § Outline 的 `### 分派` | 义务指针（新增一节，不改 W1 接线小节） | 顶层章节序列不动 |
| `docs/concepts/documentation-model.md` | 读者面投影一段 | 只引 owner，不定义规则 |

数量：**5 处落点、4 个文件**（`create-docs` 两个小节族同文件）。契约侧条款见 `contracts/flow-obligations.contract.md` 的 A–E 组；
其中 **B 组的 `C-008a` 是「reconcile 能把图维度收敛掉」的唯一登记处**——缺了它，`SC-003` 的「收敛后二次运行零图 finding」
在文本上不可达（这正是 attempt 1 的 P1-5）；而它的判据必须是 `converged`，**不是** `clean`——用 `clean` 会让
「靠具名豁免收敛」的文档永远不收敛，收敛于是没有唯一读法（这是 attempt 2 的 P1-A）。

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
none          --引用指向的渲染产物缺失--------> missing / reference-unresolved
two faces ok  --无追溯记录（或未给 --record）--> not-evaluated / no-trace-record
two faces ok  --记录在但指不到这张图/缺字段---> not-evaluated / trace-incomplete
two faces ok  --记录齐备 + 引用解析------------> satisfied / reference-resolves
satisfied     --源 mtime > 最早渲染 mtime-----> stale / source-newer-than-render
satisfied     --盘上 sha ≠ 记录 sha-----------> stale / render-digest-mismatch
源在、渲染缺  （引用指向源，解析成功）--------> missing / orphan-rendered
源缺、渲染在  （两面只剩渲染）-----------------> missing / orphan-source
any           --豁免有效且未被事实推翻--------> recorded-exemption / exempt-chronological
any           --豁免失效（已带解析引用）------> not-evaluated / exemption-invalid (+superseded)
any           --渲染产物读不出----------------> not-evaluated / render-unreadable
```

**这张表是 `C-016` 有序判定的另一种读法**（按触发面），不是第二套判据：冲突时以 `C-016` 为准。
两处顺序值得点名，因为它们各自是一次真实的误判来源：**失面（`orphan-*`）先于 `stale`**——`C-008` 的两条规则
在缺少一个面时对象不存在、不可判；**引用解析（`reference-unresolved`）先于失面**——目标整个不在盘时
根本走不到「两面里缺哪一个」这一步。
