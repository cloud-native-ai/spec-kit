# Contract — Diagram Obligation Checker（配套图检查器）

**Feature**: 087 架构图为核心的文档空间 | **Date**: 2026-11-06
**Implementing engine**: `skills/external/create-docs/scripts/docs-utils.py`（新动作 `obligation`）
**FR served**: FR-003, FR-004, FR-005, FR-008, FR-013, FR-014, FR-015, FR-016, FR-022, FR-023
**Declared owner of this contract**: this file. It owns the checker's **command surface**, the closed
`verdict` set, the closed `reason` set, the `stale` per-face criteria, the traceability-record schema
and the exemption-record schema. Every other surface (skill text, contract index, tests, the
`docs/concepts/documentation-model.md` reader projection) cites this file by section anchor and
restates **no** value, threshold or enumeration.

**Boundary.** The carrier set, the taxonomy, the reserved root filenames and the confirmation tiers are
**not** owned here — they stay with `skills/external/create-docs/SKILL.md` § Desired-State Baseline
(FR-001/FR-002/FR-003 cite it). The drawing capability's semantic model, engine routing, delivery
contract and refusal semantics stay with `skills/external/draw-diagram/` (FR-011/FR-012 cite it).
This contract owns only what the spec's RS-006 designates as plan-frozen.

---

## C-001 — Command surface

```text
python3 ${SKILL_HOME}/scripts/docs-utils.py --action obligation --root <project-root> \
  [--record <run-record-path>]... [--only <doc-path>]... [--json]
```

- `--root` 缺省 `.`，与同引擎既有动作一致，取**项目根**（carrier set 的根是项目根，不是 `docs/`）：
  `validate` / `scan` / `audit` 同此口径，文档空间由 `--root` + `docs/` 推出。
- 两个目录常量由本契约固定，其余模块不重复声明：追溯记录
  `<root>/docs/.speckit/runs/`、豁免记录 `<root>/docs/.speckit/exemptions/`（C-010 / C-011）。
  `${SKILL_WORKDIR}` 与 `--root` 在本技能内是同一路径前缀（`SKILL_WORKDIR` 指用户的**项目**根，
  即技能 Path Conventions 对「runtime/user-facing path」的解析结果），因此这两处落点就是
  `docs/.speckit/` 这个**既有 C 区机器目录**下的两个新子目录，MUST NOT 另起第三个机器目录。
- 输出**一个 JSON 对象**到 stdout（与该引擎既有动作同形，`docs-utils.py` 的模块契约）。
- `--record` 给出来源运行记录（C-010）时才可能产出 `satisfied`；缺省时没有任何文档能被判 `satisfied`，
  全部落 `unrecorded-trace` 或 `missing`（C-007）。检查器 MUST NOT 凭猜测补一条记录。
- 退出码：`0` = 已完成判定（**不论是否干净**）；`2` = 输入错误（`--root` 不存在、`--record` 给了但不可读）。
  「干净与否」只在 payload 的 `verdict` 里，MUST NOT 由退出码承载——否则「干净」与「跑完」两种事实会被压成一个。
- 一个动作、一个调用方族（`skill:create-docs` 的两处 R6，见
  `shared/workflow/expression-gates.md` § 调用点表 `skill:create-docs` 行）。MUST NOT 新增 `/speckit.*` 命令
  （FR-017）。

## C-002 — Read-only by construction（FR-015）

MUST NOT 打开任何文件用于写入。允许的副作用集合是**空集**：不写文件、不建目录、不 append 审计日志、
不写 LDM 摘要、不写交付契约摘要、不落缓存。实现 MUST 通过在 `main()` 里把 `obligation` 分支接到一个
只读 helper 来保证，并由 `tests/unit/test_docs_utils_obligation.py` 的只读断言钉住（C-006）。

## C-003 — Carrier set（判什么）

被判定对象 = 载体集合；集合的**定义**归 `skills/external/create-docs/SKILL.md` § Desired-State Baseline
（基线第 1 项登记保留根文件名与其固定语义，第 2 项登记六类正式目录）。本契约只登记**判定的读法**：

| 载体 | 参判 | 说明 |
|------|------|------|
| 六类正式目录内的 `*.md` | 是 | `concepts/` `tutorials/` `tasks/` `reference/` `decisions/` `contribute/`（含各自 `index.md`） |
| 根 `ARCHITECTURE.md` | 是 | 语义本身就是结构的一页摘要（A11） |
| 根 `README.md` / `CONTRIBUTING.md` / `CHANGELOG.md` | **否** | 承 FR-001 的指针义务，MUST NOT 被判 `missing`，也 MUST NOT 被记成豁免 |
| `docs/notes/**` | **否** | 临时区，无稳定性保证（FR-003） |
| `docs/archive/**`、`docs/.speckit/**` | **否** | 归档区 / C 区运行产物 |
| 站点工具目录（`layouts/` `static/` `public/` `resources/` `themes/` `archetypes/` 与点目录） | **否** | 非文档（基线 C 区） |

非载体文档 MUST NOT 出现在 `documents[]` 里——它们既不通过也不失败，是**不可见**，不是「通过」。

## C-004 — 封闭 verdict 集（RS-006 的一半，FR-014/FR-016）

`verdict` ∈ 且仅 ∈ 下列五值，逐文档一个：

| `verdict` | 含义 | 一票否决条件 |
|-----------|------|--------------|
| `satisfied` | 两面齐备、引用解析、追溯记录齐备且与盘上一致 | — |
| `missing` | 载体文档没有配套图 | — |
| `stale` | 图在，但与自身另一面或与文档失步（C-008 / C-009） | — |
| `recorded-exemption` | 文档带**有效**具名豁免记录（C-011） | — |
| `not-evaluated` | 无法判定（C-012 的封闭四项） | — |

- 五值**有序优先级**：`recorded-exemption` > `missing` > `not-evaluated` > `stale` > `satisfied`。
  优先级只在同一文档可落多值时才起作用（例如带失效豁免且确实无图 ⇒ 记 `not-evaluated`
  并给 `reason: exemption-invalid`，MUST NOT 记 `missing`——失效的豁免是「判不了」，不是「没有」）。
- **`recorded-exemption` 不是 pass**：`summary.exempted > 0` 时 `summary.clean` MUST 为 `false`，
  payload MUST 单独计数（FR-004：「记录的豁免不是 pass」）。
- 闭集性质：payload 里出现第六种值即契约违规，MUST 由 `tests/unit/test_docs_utils_obligation.py`
  对一组夹具逐值断言（含负向夹具）。

## C-005 — 封闭 `reason` 集（RS-006 的另一半，FR-016）

每条 `documents[]` 条目 MUST 带 `reason`，取值来自与 `verdict` **一一绑定**的下表；闭集之外的值即契约违规。

| `verdict` | 允许的 `reason` 值 | 含义（一句话） |
|-----------|-------------------|----------------|
| `satisfied` | `reference-resolves` | 文档引用解析到渲染产物，且记录齐备一致 |
| `missing` | `no-diagram-reference` | 文档里没有任何指向图渲染产物的相对引用 |
| `missing` | `reference-unresolved` | 有引用但目标在盘上不存在 |
| `missing` | `orphan-source` | 图的源在盘、渲染产物缺失（两面只剩一面） |
| `stale` | `source-newer-than-render` | 源 mtime 晚于渲染产物 mtime（源改过没再渲染） |
| `stale` | `render-digest-mismatch` | 记录里的渲染产物 sha256 与盘上实际文件不等（图被手改） |
| `not-evaluated` | `no-trace-record` | 有图但产生方运行没留下追溯记录（FR-013：未接受） |
| `not-evaluated` | `trace-incomplete` | 记录在但缺字段（引擎层 / 理由 / LDM 摘要 / 交付契约结论） |
| `not-evaluated` | `exemption-invalid` | 有豁免记录但理由字段缺失或不再适用 |
| `not-evaluated` | `render-unreadable` | 渲染产物存在但读不出来（权限 / 编码） |
| `recorded-exemption` | `exempt-chronological` | 记录的理由是「无结构可绘」类（C-011 的闭集） |

- `reason` 与 `verdict` 的配对表即**闭集本身**：新增一行属契约变更，MUST NOT 由实现就地扩面。
- 每条条目 MUST 带 `path`（**相对 `--root` 的 POSIX 路径**）与 `line`（引用所在行；无引用时为 `0`）。
  「逐文档路径具名」是 FR-016 的原文要求，MUST NOT 只给计数。

## C-006 — 确定性、幂等、零写（FR-015）

1. **确定性**：同一输入两次运行的 `documents[]` 排序 MUST 相同（按 `path` 字典序），MUST NOT 依赖
   `os.walk` 的返回序或 mtime 精度以外的随机量；未声明 `--record` 的字段 MUST 为 `null` 而不是省略
   （字段集固定 ⇒ 两次运行字节可比）。
2. **幂等**：不改动空间时零写（C-002）⇒ 第二次运行必然同 verdict。
3. **无隐藏输入**：只读 `--root` 下的文件与被 `--record` 点名的文件；MUST NOT 读 `git`、MUST NOT 读网络、
   MUST NOT 读 `.specify/memory/`（FR-015 的「记录只是输入，不是发现机制」）。

## C-007 — `satisfied` 的合取条件

一个文档判 `satisfied` 当且仅当下列五条**同时**成立：

1. 文档内至少一条**相对 Link**（`[..](path)`，非 `http(s)://`、非绝对路径）解析到一个存在的文件；
2. 该文件是 C-010 记录里某条 `rendered[].path` 的**同名**路径；
3. 该图条目的 `source` 与 `rendered[]` 两面**都在盘**；
4. 该图条目所属运行记录齐备（C-010 必填字段非空）；
5. C-008 与 C-009 两条判据都不成立（不 stale）。

任一不成立 ⇒ 按 C-005 的配对落到对应 `verdict`/`reason`。**没有记录即 `not-evaluated`**，
MUST NOT 因为「两面都在、引用也解析了」而判 `satisfied`（FR-013：无记录 = 未接受）。

## C-008 — `stale` 第一半：图的两个面彼此不一致（A12 的并集左半）

判定规则（任一成立即 `stale`，`reason` 取命中的第一条）：

| # | 规则 | `reason` |
|---|------|----------|
| 1 | `os.stat(source).st_mtime > os.stat(rendered).st_mtime`（**严格大于**；相等不算） | `source-newer-than-render` |
| 2 | 记录里该 `rendered[]` 条目的 `sha256` 与盘上文件的 sha256 不等 | `render-digest-mismatch` |

- 规则 2 **只在记录里带 `sha256` 时**才判；记录无 `sha256` 时该条规则 `not-applicable`，
  不计入 stale（缺字段本身已由 C-007 第 4 条挡在 `satisfied` 之外）。
- **不覆盖**：重渲染后字节不同但语义相同——每次真实重渲染都由产生方重写记录，`sha256` 随之刷新；
  因此规则 2 不会把一次正常重渲染误判成 stale。
- **不覆盖**：渲染产物的内容是否与源**语义**相符（无解析器，见 research R3）。

## C-009 — `stale` 第二半：图与文档就同一事实不一致（A12 的并集右半，**部分覆盖，如实登记**）

**已冻结可判的部分**：

| # | 规则 | 后果 |
|---|------|------|
| 1 | 文档引用的渲染产物被改名 / 移走后，文档仍指向旧路径 | `missing` / `reference-unresolved`（不是 stale） |
| 2 | 文档引用的图，其记录的 `rendered[].path` 与文档引用目标不是同一路径 | `stale` / `render-digest-mismatch` 不作此用；本条落 `not-evaluated` / `trace-incomplete` |

**未冻结的部分（显式残差，MUST NOT 读作通过）**：

「图内标签 / 关系与文档正文所述事实一致」**本特性不判定**。判据缺失的理由与代价登记在
`plan.md` § Decision Tensions `T-003` 与 § Residual Risk `D-001`；检查器对这部分 MUST NOT 产出任何 verdict，
其可判定性归评审面（`/speckit.review`）与后续特性。**落实 A12 的退路**：该面被诚实登记为未覆盖，
而不是留一条没有判据的 `stale`。

## C-010 — 追溯记录 schema（FR-013、FR-022 的机器面）

**落点**：每次产出或改动图的**运行**把记录 append 到
`<root>/docs/.speckit/runs/<UTC 时间戳>-diagram-trace.json`（`<root>` 见 C-001）——一文一件，路径即身份
（Concurrent Development Safety：两个并发的写入运行写不同路径，不共享可变聚合）。

```json
{
  "run_id": "<UTC timestamp>-<8 hex>",
  "feature": "<feature key or null>",
  "diagrams": [
    {
      "document": "docs/concepts/foo.md",
      "engine": "mermaid",
      "engine_reason": "<路由命中：独占登记 / 图类矩阵行 / tie-break>",
      "ldm_summary": "<diagram_class + elements/relations/zones 的一句话摘要>",
      "delivery": {
        "accepted": true,
        "unmet": []
      },
      "source": "docs/concepts/diagrams/foo.mmd",
      "rendered": [
        {"path": "docs/concepts/diagrams/foo.svg", "sha256": "<64 hex>"},
        {"path": "docs/concepts/diagrams/foo.png", "sha256": "<64 hex>"}
      ]
    }
  ]
}
```

必填字段（缺一即 `trace-incomplete`）：`document`、`engine`、`engine_reason`、`ldm_summary`、
`delivery.accepted`、`source`、`rendered[].path`。`rendered[].sha256` 可缺（缺则 C-008 规则 2 不判）。

- 字段**含义**归 `draw-diagram`：`engine` 取自其 `references/routing-matrix.md` 的六引擎层名；
  `ldm_summary` 是 `references/semantic-model.md` schema 的摘要；`delivery` 是
  `references/delivery-contract.md` § D6 自检表的结论。本契约只登记**字段名与必填性**，MUST NOT 复述那三份 owner 的判据。
- 记录由**产生方运行**写（FR-015：只读检查 MUST NOT 写它）；检查器只读。

## C-011 — 豁免记录 schema（FR-004）

**落点**：`<root>/docs/.speckit/exemptions/<相对文档路径>.md`（`<root>` 见 C-001），一文一件。示例
`docs/.speckit/exemptions/concepts/changelog-shaped.md`：

```markdown
---
document: docs/concepts/changelog-shaped.md
reason: exempt-chronological
recorded_at: 2026-11-06
justification: "按时间排序的发布流水，没有可绘的结构"
---
```

- `reason` 闭集：`exempt-chronological`（时间线 / 变更流水）、`exempt-flat-reference`（纯平铺参考表，无可绘结构）、
  `exempt-licence`（许可 / 法律文本）。三个值都是「本文件没有结构可绘」，MUST NOT 被用成「这图太难画」。
- **有效性**：`document` 必须等于被豁免文档的相对路径；`justification` 非空且长度 ≥ 8 字符；
  `recorded_at` 为 `YYYY-MM-DD`。任一条不成立 ⇒ `not-evaluated` / `exemption-invalid`（可见，不是静默通过）。
- **失效可报（FR-004 后半）**：被豁免文档在同一次运行里**已经带一条解析到渲染产物的引用**时，
  豁免已被事实推翻 ⇒ `not-evaluated` / `exemption-invalid` 并在 `summary.exemption_superseded` 计数。
  这是「豁免理由不再成立」的**唯一**机械信号；理由的语义变化 MUST NOT 被自动推断。

## C-012 — `not-evaluated` 的封闭四项

只有下列四种情形产出 `not-evaluated`，别的一律落到 `missing` / `stale` / `satisfied`：

1. 有图两面与引用，但**没有**追溯记录（`no-trace-record`）；
2. 记录在但缺 C-010 必填字段（`trace-incomplete`）；
3. 豁免记录无效或已失效（`exemption-invalid`）；
4. 渲染产物存在但读不出来（`render-unreadable`，`OSError` 归一）。

「引擎不可用」不在此列：检查器**不调用**任何引擎（C-006 无网络、无第三方）——FR-012 的引擎拒绝语义
归产生方运行，不归检查器。

## C-013 — Payload 形态

```json
{
  "action": "obligation",
  "root": "<abs>",
  "record": "<abs or null>",
  "carriers": 12,
  "documents": [
    {"path": "docs/concepts/foo.md", "line": 14, "verdict": "satisfied", "reason": "reference-resolves"}
  ],
  "summary": {
    "satisfied": 1, "missing": 0, "stale": 0, "exempted": 0, "not_evaluated": 0,
    "clean": false, "exemption_superseded": 0
  }
}
```

- `summary.clean` 为 `true` **当且仅当** `missing == 0 && stale == 0 && not_evaluated == 0 && exempted == 0`。
  干净空间因此是「零 finding 的显式结论」，不是「空输出」（FR-016）；有豁免的空间 MUST NOT 报 `clean`
  （豁免可见，不等于通过）。
- 空载体集合（`carriers == 0`）MUST 报 `clean: false` + `documents: []`：一个没有正式文档的空间
  不是「合规」，是「判据没有对象」。这条防的是 `FR-016` 允许的假绿。
- `--only` 只缩小被检对象集合，不改变任何判据；`summary` 只统计被检对象。

## C-014 — 与既有守卫的关系（实施期 MUST 保持）

本契约不授权改动任何守卫。实现时下列断言 MUST 逐条保持通过（读数见 `plan.md` § Definition of Done）：

| 守卫 | 钉住的字面量 |
|------|--------------|
| `tests/contract/test_expression_gate_wiring.py` A1/A3 | W1 接线小节与 `create-docs` 的 R6 文字 |
| `tests/contract/test_docs_command_template.py` C3/C4a | `templates/commands/docs.md` 的顶层章节序列与 `improve-docs` 指针 |
| `tests/contract/test_confirmation_gates_sweep.py` KEEP_LIST | `templates/commands/docs.md` 含 `stop-and-confirm` |
| `tests/contract/test_directory_governance.py` | `docs/concepts/documentation-model.md` 留在 area-map 清单内 |

## C-015 — 与既有 `validate` 动作的关系（不复用、不合并）

`--action validate` 的判据是「文档空间的静态合规」（保留名、一屏上限、断链、ADR 编号、notes frontmatter），
判据**零新增违规**（W1 调用点行原文）。`--action obligation` 的判据是「配套图义务」，两者**输入相同、判据互不相同**，
MUST NOT 合并进一个动作：合并会让「今日合规、明日因新义务全红」的过渡状态无法表达，
也会让 W1 的「零新增违规」判据失去基准。两者在 R6 的验证步骤里**并列执行**，各自出各自的 verdict。
