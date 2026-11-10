# Contract — Diagram Obligation Checker（配套图检查器）

**Feature**: 087 架构图为核心的文档空间 | **Date**: 2026-11-06
**Implementing engine**: `skills/external/create-docs/scripts/docs-utils.py`（新动作 `obligation`）
**FR served**: FR-003, FR-004, FR-005, FR-008, FR-013, FR-014, FR-015, FR-016, FR-022, FR-023
**Declared owner of this contract**: this file. It owns the checker's **command surface**, the closed
`verdict` set, the closed `reason` set, the per-document **decision precedence** (`C-016`), the `stale`
per-face criteria, the traceability-record schema and the exemption-record schema. Every other surface (skill text, contract index, tests, the
`docs/concepts/documentation-model.md` reader projection) cites this file by section anchor and
restates **no** value, threshold or enumeration.

**Same facts, second carrier — and which one is the owner**: `skills/external/create-docs/references/diagram-obligation.md`
is the **client-facing projection** of this contract. It exists because this contract does not ship: a client
project installs `.specify/skills/create-docs/` and never receives `.specify/specs/087-…/contracts/`, so the values
a project must apply have to travel with the skill. Its ownership is therefore delegated and one-directional —
**this file is the design record and stays the owner** of every value above; the shipped reference restates those
values for a reader who cannot open this file, and where the two disagree the projection is the defect. The
reference carries the same projection duty in the other direction for the engine: its header says that a
disagreement between the projection and `docs-utils.py --action obligation` **is** the engine winning. No third
carrier of these values exists (`D-001` aside, which is a declared non-coverage, not a value).

**Boundary.** The carrier set, the taxonomy, the reserved root filenames and the confirmation tiers are
**not** owned here — they stay with `skills/external/create-docs/SKILL.md` § Desired-State Baseline
(FR-001/FR-002/FR-003 cite it). The drawing capability's semantic model, engine routing, delivery
contract and refusal semantics stay with `skills/external/draw-diagram/` (FR-011/FR-012 cite it).
This contract owns only what the spec's RS-006 designates as plan-frozen.

**Notation（记号别名，与 `flow-obligations.contract.md` 头部同一条读法）**：本文件的条款代码是 `C-nnn`
（`## C-001` … `## C-016`）。`flow-obligations.contract.md` 用 `[D-nnn]` 引用本文件，`[D-nnn]` 即本文件的
`C-nnn`（`[D-013]` = 本文件 `C-013`）。**这个 `[D-nnn]` 与 `.specify/register.md` 的残差记录 ID
`D-001` / `D-001-a` 是两套不同的命名空间**：带方括号的是契约条款，不带方括号的是登记册里的残差记录。
本特性唯一需要辨析的一处：`plan.md` § Residual Risk 的 `D-001`（图文语义面未覆盖）与 `[D-001]`
（= 本文件 `C-001` 的命令面）互不相干。

---

## C-001 — Command surface

```text
python3 ${SKILL_HOME}/scripts/docs-utils.py --action obligation --root <project-root> \
  [--record <trace-record-file>] [--only <doc-path>] [--json]
```

- **参数集是封闭的**：`obligation` 只接受上表四个选项。`--json` 是**既有动作已隐含的形态**
  （该引擎每次调用都 `json.dump` 一个对象到 stdout，见 `main()`），因此它是**无操作的可读性开关**，
  不给引擎加第二个输出模式；`--record` 单值（可重复出现，后者覆盖前者，不做并集）。
  其余既有选项（`--yes` / `--apply` / `--moves` / `--scope` / `--summary` / `--items-file` /
  `--allow-special`）对 `obligation` **无定义**，实现 MAY 接受并忽略，MUST NOT 赋予语义。
- `--root` 缺省 `.`，与同引擎既有动作一致，取**项目根**（carrier set 的根是项目根，不是 `docs/`）：
  `validate` / `scan` / `audit` 同此口径，文档空间由 `--root` + `docs/` 推出。
- 两个目录常量由本契约固定，其余模块不重复声明：追溯记录
  `<root>/docs/.speckit/runs/`、豁免记录 `<root>/docs/.speckit/exemptions/`（C-010 / C-011）。
  `${SKILL_WORKDIR}` 与 `--root` 在本技能内是同一路径前缀（`SKILL_WORKDIR` 指用户的**项目**根，
  即技能 Path Conventions 对「runtime/user-facing path」的解析结果），因此这两处落点就是
  `docs/.speckit/` 这个**既有 C 区机器目录**下的两个新子目录，MUST NOT 另起第三个机器目录。
- 输出**一个 JSON 对象**到 stdout（与该引擎既有动作同形，`docs-utils.py` 的模块契约）。
- `--record` 给出来源运行记录（C-010）时才可能产出 `satisfied`；缺省时没有任何文档能被判 `satisfied`，
  全部落 `not-evaluated` / `no-trace-record` 或 `missing`（C-007/C-012）。检查器 MUST NOT 凭猜测补一条记录。
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

- **顺序不在本条款声明**：本条款只声明五值构成一个**封闭集**（第五个值即违约）。同一文档可落多值时的
  落档裁决**唯一归 `C-016`** 的九行有序优先级表——本条款 MUST NOT 复述该顺序，也 MUST NOT 给出第二份优先级。
  只举一个非顺序性的例子说明「同值优先于失值」的直觉：带失效豁免且确实无图 ⇒ 记 `not-evaluated`
  并给 `reason: exemption-invalid`，MUST NOT 记 `missing`（失效的豁免是「判不了」，不是「没有」）；
  该例的**位次**仍以 `C-016` 为准。
- **`recorded-exemption` 不是 pass**：`summary.exempted > 0` 时 `summary.clean` MUST 为 `false`，
  payload MUST 单独计数（FR-004：「记录的豁免不是 pass」）。**它不阻断 `summary.converged`**：豁免是合法终态，
  而 `converged` 只问「还有没有待收敛的 `missing` / `stale` / `not-evaluated`」（两谓词的定义点见 `C-013`；
  收敛判据 MUST 用 `converged`，MUST NOT 用 `clean`）。
- 闭集性质：payload 里出现第六种值即契约违规，MUST 由 `tests/unit/test_docs_utils_obligation.py`
  对一组夹具逐值断言（含负向夹具）；断言形态见 `C-016` 与 `plan.md` § Test Plan 的 clause→test 表。
- `not-evaluated` **不是合格态**：它与 `missing` / `stale` 一样使 `clean` 与 `converged` **同时**为 `false`（`C-013`）。

## C-005 — 封闭 `reason` 集（RS-006 的另一半，FR-016）

每条 `documents[]` 条目 MUST 带 `reason`，取值来自与 `verdict` **一一绑定**的下表；闭集之外的值即契约违规。

| `verdict` | 允许的 `reason` 值 | 含义（一句话） |
|-----------|-------------------|----------------|
| `satisfied` | `reference-resolves` | 文档引用解析到渲染产物，且记录齐备一致 |
| `missing` | `no-diagram-reference` | 文档里没有任何指向图渲染产物的相对引用 |
| `missing` | `reference-unresolved` | 有引用但目标在盘上不存在 |
| `missing` | `orphan-source` | 渲染产物在盘、可再编辑源缺失（两面只剩「渲染」一面） |
| `missing` | `orphan-rendered` | 可再编辑源在盘、渲染产物缺失（两面只剩「源」一面） |
| `stale` | `source-newer-than-render` | 源 mtime 晚于渲染产物 mtime（源改过没再渲染） |
| `stale` | `render-digest-mismatch` | 记录里的渲染产物 sha256 与盘上实际文件不等（图被手改） |
| `not-evaluated` | `no-trace-record` | 两面与引用都在，但产生方运行没留下任何追溯记录（FR-013：未接受） |
| `not-evaluated` | `trace-incomplete` | 两面与引用都在、记录也在，但记录里**指不到这张图**：`diagrams[]` 无与文档引用目标同名的一条，或该条缺 `C-010` 必填字段 |
| `not-evaluated` | `exemption-invalid` | 有豁免记录但理由字段缺失或不再适用 |
| `not-evaluated` | `render-unreadable` | 渲染产物存在但读不出来（权限 / 编码） |
| `recorded-exemption` | `exempt-chronological` | 记录的理由是「无结构可绘」类（`C-011` 的闭集） |

- `reason` 与 `verdict` 的配对表即**闭集本身**：新增一行属契约变更，MUST NOT 由实现就地扩面。
- **失面必须报具名的那一面**（FR-008 / FR-023）：源在、渲染产物缺 ⇒ `orphan-rendered`；渲染产物在、
  源缺 ⇒ `orphan-source`。两个值方向相反、不可互换——「点名缺失的面」是 `SC-002` 的判据本体。
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

一个文档判 `satisfied` 当且仅当下列五条**同时**成立（任何一条不成立时**落哪一档由 `C-016` 的有序判定决定**，
不由本节决定）：

1. 文档内至少一条**相对 Link**（`[..](path)`，非 `http(s)://`、非绝对路径）解析到一个存在的文件；
2. 该文件是 `--record` 记录里某条 `rendered[].path` 的**同名**路径；
3. 该图条目的 `source` 与 `rendered[]` 两面**都在盘**；
4. 该图条目所属运行记录齐备（C-010 必填字段非空）；
5. C-008 与 C-009 两条判据都不成立（不 stale）。

**没有记录即 `not-evaluated`**，MUST NOT 因为「两面都在、引用也解析了」而判 `satisfied`
（FR-013：无记录 = 未接受）。

## C-008 — `stale` 第一半：图的两个面彼此不一致（A12 的并集左半）

**前置条件**：记录里存在与文档引用目标同名的一条 `diagrams[]` 条目，且该条目的 `source` 与
全部 `rendered[]` **都在盘**。两面不全时本节不判——失面归 `missing`，且按 `C-016` 的优先级先于本档结算。

判定规则（任一成立即 `stale`，`reason` 取命中的第一条）：

| # | 规则 | `reason` |
|---|------|----------|
| 1 | `os.stat(source).st_mtime > os.stat(rendered).st_mtime`（**严格大于**；相等不算；多面取**最早**的 `rendered` mtime 比较） | `source-newer-than-render` |
| 2 | 记录里该 `rendered[]` 条目的 `sha256` 与盘上文件的 sha256 不等（多面逐个比对，任一不等即命中） | `render-digest-mismatch` |

- 规则 2 **只在记录里带 `sha256` 时**才判；记录无 `sha256` 时该条规则 `not-applicable`。
- **不覆盖**：重渲染后字节不同但语义相同——每次真实重渲染都由产生方重写记录，`sha256` 随之刷新；
  因此规则 2 不会把一次正常重渲染误判成 stale。
- **不覆盖**：渲染产物的内容是否与源**语义**相符（无解析器，见 research R3）。

## C-009 — `stale` 第二半：图与文档就同一事实不一致（A12 的并集右半，**部分覆盖，如实登记**）

**已冻结可判的部分**：

| # | 规则 | 后果 |
|---|------|------|
| 1 | 文档引用的渲染产物被改名 / 移走后，文档仍指向旧路径 | `missing` / `reference-unresolved`（不是 stale） |
| 2 | 文档引用解析到渲染产物，但 `--record` 记录里没有任何一条 `rendered[].path` 与之同名 | `not-evaluated` / `trace-incomplete`（记录不覆盖这张图） |

- 两条都由 `C-016` 的有序判定结算；本节只声明「它们各自落哪一档、不落 `stale`」。
- **`stale` 的判据因此只有一个入口**：`C-008`。`C-009` 冻结部分是「引用与记录不同源」的归类，不是 stale 的第二判据。

**未冻结的部分（显式残差，MUST NOT 读作通过）**：

「图内标签 / 关系与文档正文所述事实一致」**本特性不判定**。判据缺失的理由与代价登记在
`plan.md` § Decision Tensions `T-003` 与 § Residual Risk `D-001`；检查器对这部分 MUST NOT 产出任何 verdict，
其可判定性归评审面（`/speckit.review`）与后续特性。**落实 A12 的退路**：该面被诚实登记为未覆盖，
而不是留一条没有判据的 `stale`。

## C-010 — 追溯记录 schema（FR-013、FR-022 的机器面）

**落点**：每次产出或改动图的**运行**把记录 append 到
`<root>/docs/.speckit/runs/<UTC basic>-<8 hex>-diagram-trace.json`（`<root>` 见 C-001）——一文一件，路径即身份
（Concurrent Development Safety：两个并发的写入运行写不同路径，不共享可变聚合）。
文件名形态在本条款**唯一钉死**，`data-model.md` 的 E4 行与 `quickstart.md` 只是它的发布视图，MUST NOT 另立形态：
`<UTC basic>` = `YYYYMMDDTHHMMSSZ`（`datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')`），
`<8 hex>` = 本次运行 id 的前 8 个十六进制字符（与 `test-evidence/` 的 `exec-quant` 记录同一约定）；
两段之间、段与 `diagram-trace` 之间均为单个 `-`，扩展名恒为 `.json`。

> **文件名形态是 `C-001` 的 `--record` 使用约定，不是检查器的发现机制**：
> 检查器**只读 `--record` 明确点名的文件**（`C-006` 规则 3），不 glob 目录、不按时间戳猜「最新一份」——
> 猜一份就让「记录被改 ⇒ 失步不可发现」重新成立，与 `FR-015` 相悖。流水线里只需
> `--record docs/.speckit/runs/<UTC basic>-<8 hex>-diagram-trace.json`，那是**调用方**的选择。

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
      "source": "docs/assets/foo.mmd",
      "rendered": [
        {"path": "docs/assets/foo.svg", "sha256": "<64 hex>"},
        {"path": "docs/assets/foo.png", "sha256": "<64 hex>"}
      ]
    }
  ]
}
```

必填字段（缺一即 `trace-incomplete`）：`document`、`engine`、`engine_reason`、`ldm_summary`、
`delivery.accepted`、`source`、`rendered[].path`。`rendered[].sha256` 可缺（缺则 C-008 规则 2 不判）。

- **路径一律相对 `<root>`**（与 `C-005` 的 `path` 同口径），因此 `source` / `rendered[].path` 与文档里的
  相对引用可以按同一基准比对。
- **图的落点归 Baseline（T-005）**：本示例里的 `docs/assets/` 取自 `skills/external/create-docs/SKILL.md`
  § Desired-State Baseline 内**由本特性新建**的 `#### Assets` 小节（该小节当前不在盘，尚待实施期落笔——
  它是**新建**的区域约定条目，MUST NOT 被读作既有的 owner 章节）；在此之前，「图的落点」的唯一登记处是
  `flow-obligations.contract.md` `C-009`。本契约只借它作示例、MUST NOT 成为第二个落点 owner。
- 字段**含义**归 `draw-diagram`：`engine` 取自其 `references/routing-matrix.md` 的六引擎层名；
  `ldm_summary` 是 `references/semantic-model.md` 的 Schema 摘要；`delivery` 是
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
- **图的落点不在本条款内**：本条款只拥有「豁免记录放哪、怎么算有效」。图的两面放哪归
  `skills/external/create-docs/SKILL.md` § Desired-State Baseline（该节内 `#### Assets` 小节由本特性实施期新建，当前不在盘；`plan.md` T-005 裁定为 `assets/`），
  MUST NOT 在此复述（宪法 XIV：一个事实一个 owner）。

## C-012 — `not-evaluated` 的封闭四项

只有下列四种情形产出 `not-evaluated`，别的一律落到 `missing` / `stale` / `satisfied`：

1. 有图两面与引用，但**没有**追溯记录（`no-trace-record`）；
2. 记录在但**指不到这张图**——无同名 `diagrams[]` 条目，或该条缺 C-010 必填字段（`trace-incomplete`）；
3. 豁免记录无效或已失效（`exemption-invalid`）；
4. 渲染产物存在但读不出来（`render-unreadable`，`OSError` 归一）。

「引擎不可用」不在此列：检查器**不调用**任何引擎（C-006 无网络、无第三方）——FR-012 的引擎拒绝语义
归产生方运行，不归检查器。

**这一项也就此定死「刚生成、尚未入记录」的图**：两面在、引用解析、却没有一条记录点到它 ⇒ `no-trace-record`
⇒ `converged: false` 且 `clean: false`，直到产生方运行**同一次**写出记录为止（`flow-obligations.contract.md` `C-003`）。
把 `not-evaluated` 读成「暂不追究」是本契约明确禁止的读法（`C-013`）。

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
    "converged": true, "clean": true, "exemption_superseded": 0
  }
}
```

- **两个谓词，两个问题（本条是它们的唯一定义点）**：
  - 记 `judged_scope_has_carrier = (--only 缺省 ? carriers > 0 : true)`：默认全量作用域没有正式文档时
    判据没有对象；`--only` 把作用域缩到 0 个对象是调用方的选择（见下）。
  - `summary.converged` 为 `true` **当且仅当** `judged_scope_has_carrier && missing == 0 && stale == 0 && not_evaluated == 0`。
    它回答「还有没有待收敛的 finding」；**豁免不在它的算式里**——豁免是 `FR-004` 的合法终态，
    它不产生待收敛项。`carriers == 0`（默认作用域）是该谓词的一个合取项，不是例外。
  - `summary.clean` 为 `true` **当且仅当** `converged == true && exempted == 0`（等价于
    `judged_scope_has_carrier && missing == 0 && stale == 0 && not_evaluated == 0 && exempted == 0`）。它回答「这个空间是不是零 finding
    的显式结论」，因此**严格**：有豁免的空间 MUST NOT 报 `clean`（豁免可见，不等于通过，`FR-004`）。
  - ⇒ `exempted > 0 ⇒ clean = false`（硬约束，不变）；`exempted > 0` 与 `converged` **无关**，
    所以「一个具体文档无结构可绘、已具名豁免」的收敛终态是 **`converged=true` + `clean=false`**，这是合法结果，
    不是矛盾（`SC-008`）。**「零图 finding」这句话指 `converged`，不是 `clean`。**
  - 两个字段**同时在场**（字段集固定，`C-006`）：只给 `clean` 会让带豁免的空间无法表达「已收敛」。
- 空载体集合（默认作用域，`carriers == 0`）MUST 报 `converged: false` + `clean: false` + `documents: []`：一个没有正式文档的空间
  不是「合规」，是「判据没有对象」，因此 `judged_scope_has_carrier=false`，两个谓词**都**取假——这是
  `carriers > 0` 合取项的直接结果，不是主算式的例外，防的是 `FR-016` 允许的「零 finding」被一个空判定集合冒充。
  `--only` 缩小后剩下的 0 个对象是**调用方的选择**：`judged_scope_has_carrier=true`，`converged` 与 `clean` 按上式对 0 个条目算得 `true`（没有东西不干净），
  调用方 MUST NOT 把这一次「空 `--only`」读成「空间合规」——`--only` 的判定面只有它点名的那些文档。
- `--only` 只缩小被检对象集合，不改变任何判据；`summary` 只统计被检对象。
- `documents[]` 的字段集固定为 `path` / `line` / `verdict` / `reason` 四个（`C-006` 规则 1 的
  「字段集固定 ⇒ 字节可比」）：MUST NOT 追加第五个字段，MUST NOT 省略任一字段（无引用时 `line` 为 `0`）。

## C-014 — 与既有守卫的关系（实施期 MUST 保持）

本契约不授权改动任何守卫。实现时下列断言 MUST 逐条保持通过（登记面见 `tasks.md` 的 DoD 行——`plan.md` **没有** `§ Definition of Done` 这一节，DoD 的唯一 owner 是 `tasks.md`；契约 `C-014` 在此只引用它，不另立一份）：

| 守卫 | 钉住的字面量 |
|------|--------------|
| `tests/contract/test_expression_gate_wiring.py` A1/A3/A5 | W1 接线小节、`create-docs` 的 R6 文字、禁类别词 |
| `tests/contract/test_docs_command_template.py` C3/C4a | `templates/commands/docs.md` 的顶层章节序列与 `improve-docs` 指针 |
| `tests/contract/test_confirmation_gates_sweep.py` KEEP_LIST | `templates/commands/docs.md` 含 `stop-and-confirm` |
| `tests/contract/test_directory_governance.py` | `docs/concepts/documentation-model.md` 留在 area-map 清单内 |

## C-015 — 与既有 `validate` 动作的关系（不复用、不合并）

`--action validate` 的判据是「文档空间的静态合规」（保留名、一屏上限、断链、ADR 编号、notes frontmatter），
判据**零新增违规**（W1 调用点行原文）。`--action obligation` 的判据是「配套图义务」，两者**输入相同、判据互不相同**，
MUST NOT 合并进一个动作：合并会让「今日合规、明日因新义务全红」的过渡状态无法表达，
也会让 W1 的「零新增违规」判据失去基准。两者在 R6 的验证步骤里**并列执行**，各自出各自的 verdict。

## C-016 — 逐文档判定的有序优先级（唯一的落档裁决）

`C-004` 表内的「有序优先级」在此展开成**可实现的单趟判定**。对一份载体文档，按下列顺序逐条判，
**命中即停、不回溯、不二次覆盖**；每条只在它的前置成立时才有资格出手：

| 序 | 条件 | 落档 | `reason` |
|----|------|------|----------|
| 1 | 存在豁免记录且**有效、未被事实推翻** | `recorded-exemption` | `exempt-chronological` |
| 2 | 存在豁免记录但无效，或已被事实推翻（`C-011`） | `not-evaluated` | `exemption-invalid` |
| 3 | 文档没有任何解析到图文件的相对引用（`C-005`） | `missing` | `no-diagram-reference` |
| 4 | 有引用但目标不在盘（`C-009` 规则 1） | `missing` | `reference-unresolved` |
| 5 | 目标在盘、引用指向**源**扩展名而渲染产物缺失；或两面中**渲染产物在、源缺** | `missing` | `orphan-rendered` / `orphan-source` |
| 6 | 两面齐、但记录里**指不到这张图**，或指到了却缺 `C-010` 必填字段 | `not-evaluated` | `trace-incomplete` |
| 7 | 两面齐、当前**没有** `--record`（或记录里没有任何一条点到它） | `not-evaluated` | `no-trace-record` |
| 8 | 两面齐、记录齐、`C-008` 任一规则成立 | `stale` | `source-newer-than-render` / `render-digest-mismatch` |
| 9 | 两面齐、记录齐、`C-008` 都不成立、引用解析 | `satisfied` | `reference-resolves` |

**为什么失面先于 `stale`，而 `stale` 又先于 `satisfied`**：失面时 `C-008` 的两条规则都**没有可比的第二个面**
（`os.stat` 的对象不存在），因此它根本不可判——把不可判的规则排在可判规则之前，会让一次「删掉渲染面」的负向
用例落到错误的理由上。`C-008` 因此带有显式前置条件（两面都在盘）。这条顺序就是 `F-01` 的修复本体。

**豁免先于一切**：豁免有效性本身就是「判不了 / 已豁免」，与两面在不在无关；`C-004` 的两条附注
（失效豁免 + 确实无图 ⇒ `not-evaluated`）在本表第 2 行得到实现。

**`stale` 只有一个入口**：第 8 行只引用 `C-008`。`C-009` 的冻结部分在第 4、6 行结算，`C-009` 的语义残差
（`D-001`）不产出任何档位。
