# Contract — Flow Obligations（两个写入流程的配套图义务）

**Feature**: 087 架构图为核心的文档空间 | **Date**: 2026-11-06
**Surfaces carrying these obligations**: `skills/external/create-docs/SKILL.md`（§ Desired-State Baseline、
§ Authoring Flow R2/R5/R6）、`skills/external/improve-docs/SKILL.md`（§ Workflow 2/3/4/5/6）、
`templates/commands/docs.md`（§ Outline 的分派与产出段）
**FR served**: FR-005, FR-006, FR-007, FR-009, FR-010, FR-012, FR-017, FR-022
**Owner of this contract**: this file. The checker vocabulary the flows *call* is owned by
`contracts/diagram-obligation.contract.md`; this file MUST NOT restate it (it cites `[D-nnn]`).
The drawing capability's own rules are owned by `skills/external/draw-diagram/` and are cited, never paraphrased.

---

## A. 义务内容（两个流程的共同面）

- **C-001** 一次产出 = **四件在盘产物**，缺一即该运行 MUST NOT 报完成：载体文档、图的**可再编辑源**、
  **渲染产物**（交付契约对该引擎层要求的全部格式）、文档内**解析得到的相对引用**。四件的清单与
  「两面分为两面报告」的形态引 `[D-007]`（两组证据清单是它的实例）。
- **C-002** 图 MUST 由 `skills/external/draw-diagram` **按引用**产生：文档流程 MUST NOT 复制它的语义模型、
  路由判据或交付契约条文，MUST NOT 自建第二条渲染路径。**反例清单（闭集）**：新增绘图脚本、新增引擎选择表、
  新增交付契约副本、直接调用某引擎脚本绕过前门。
- **C-003** 追溯记录 MUST 在**同一次运行**里落盘，schema 引 `[D-010]`；缺记录的图在检查器眼里是
  `not-evaluated`（`[D-005]` 的 `no-trace-record`），不是 `satisfied`。
- **C-004** 引擎拒绝（前门 Step 2 的 preflight 失败 / Step 2.5 的后端不可达 / Step 4 的覆盖不通过）
  MUST 被**原样上抛**：文档流程 MUST NOT 把它改写成「文档已写完，图跳过」，MUST NOT 本地即兴渲染，
  MUST NOT 把运行标成完成。上抛形态 = 该技能既有的「提示并中断」语义，措辞归 `draw-diagram`。
- **C-005** 共享图：多份文档可以引用同一张图（FR-009），但该图 MUST 只有**一个**源文件与**一条**追溯记录条目；
  更新 MUST NOT fork 成逐文档副本。机械信号：同一 `rendered[].path` 被 ≥ 2 份文档引用时，
  记录里 MUST 只有一条同路径条目（`[D-010]` 的 `diagrams[]` 去重）。
- **C-006** 既有图 MUST 保持其引擎层与源（FR-010）：该图的追溯记录已存在时，更新 MUST 复用记录里的
  `engine`，MUST NOT 重新路由。**新图**才走前门路由。机械信号：更新后记录的 `engine` 与更新前一致。

## B. 适配面：`create-docs`

- **C-007** 义务的**唯一落点**是 § Desired-State Baseline：追加「配套架构图或具名豁免」为正式文档
  **合规的必要条件**，用一节、以「载体集合 + 义务 + 豁免」三项写出，并**引** `[D-003]` 的载体表而非重列。
  该节 MUST NOT 复述检查器的 verdict 词表（那是 `[D-004]`）。
- **C-008** § Authoring Flow 三处接线：
  - **R2 期望态**追加一项：本批新文档各自配套图的**规划**（图类意图、预计引擎层、源与渲染产物的落点）；
  - **R5 写作收敛**追加一条：调 `draw-diagram` 产出两面 + 文档引用 + 追溯记录（C-001…C-004）；
  - **R6 验证**追加一次 `docs-utils.py --action obligation`（`--record` 指向本次运行记录）并把 verdict
    并入残差报告；`missing` / `stale` / `not-evaluated` 任一非零 ⇒ MUST NOT 报「收敛完成」。
- **C-009** 图产物 MUST 落在**既有 taxonomy 内**（与文档同目录的 `diagrams/` 子树，或文档同级），
  MUST NOT 触发新建顶层文档类型目录（FR-002）。`diagrams/` 是既有目录下的子目录，不是新分类。
- **C-010** § Tiered Confirmation **一格不加**：写图仍是 safe local writes（自动执行）；移动 / 归档 / 重构
  仍是 stop-and-confirm。本契约 MUST NOT 引入第三档。

## C. 适配面：`improve-docs`

- **C-011** § Workflow step 2（证据）追加一项：读该文档的追溯记录 `[D-010]`（存在时），作为「这张图是什么、
  哪个引擎、哪两面」的机器证据。
- **C-012** § Workflow step 3（分类）追加**一行**到既有分类表：**Diagram-sync**——
  「改进改到了图所描绘的事实（组件名、关系、步骤顺序）」；**验证后果**：「同一次运行更新图或报具名
  staleness finding，二者必居其一」。表本身由该技能拥有，本契约只登记这一行必须存在（不复制表格）。
- **C-013** § Workflow step 4（最小编辑）追加：命中 Diagram-sync 时，按 C-001…C-004 更新；**不命中时**
  MUST 在原处打一行「本次无需图工作」并在报告里重复一次（FR-007：MUST NOT 为表演活动而重渲染）。
- **C-014** § Workflow step 5（验证）追加：`docs-utils.py --action obligation --only <该文档>` 的 verdict 必须是
  `satisfied` 或有效的 `recorded-exemption`；`stale` / `missing` / `not-evaluated` ⇒ MUST NOT 报改进完成。
- **C-015** 无法重渲染（引擎层不可用）⇒ MUST 报**具名** staleness finding 并保留源文件不动
  （FR-006 后半 + C-004）。MUST NOT 把源回滚成「看起来一致」的形态。

## D. 适配面：`templates/commands/docs.md`

- **C-016** § Outline 的分派段 MUST 增加一句：写作（authoring）与内容（content）两条路径**都**受配套图义务约束，
  义务正文**只引**两个技能（`create-docs` § Desired-State Baseline / § Authoring Flow、`improve-docs` § Workflow），
  MUST NOT 在命令里复述义务条文。
- **C-017** 产出段（「产出: audit log + 残差报告」）MUST 把图维度并进残差报告的分组：
  `satisfied` / `missing` / `stale` / `exempted` / `not-evaluated` 五个计数按**技能归口**分组（FR-022）。
  MUST NOT 新增第六个残差分组名。
- **C-018** 硬约束（由既有守卫钉住，MUST 逐条保持）：
  - 顶层章节序列不变（`## User Input` / `## Glossary` / `## Outline` / `## Wrap-up` / `## Handoffs`）；
  - `stop-and-confirm` 字面量保留在分派段；
  - `skills/external/improve-docs/SKILL.md` 字面量保留；
  - W1 的类别读取小节**逐字不动**（新内容 MUST 落在它之后）。
- **C-019** MUST NOT 新增 `/speckit.*` 命令、MUST NOT 新增确认档、MUST NOT 改四技能的职责划分（FR-017/FR-018/FR-019）。

## E. 读者面：`docs/concepts/documentation-model.md`

- **C-020** 追加一节（≤ 12 行）回答「读者在文档空间里会遇到什么图」，内容只包含：图随文档交付、
  无结构可绘时有一条**可见**豁免、图与文档失步会被报出。MUST NOT 复述 verdict 词表、MUST NOT 复述载体表、
  MUST NOT 成为第二本规则书（FR-001 原文）。
- **C-021** 该文件 MUST 留在 `docs/concepts/` 且路径不变（目录治理 owner 的 area-map 清单引用它）。

## F. 证据与负向可观测

- **C-022** 每次运行的运行报告 MUST 含 FR-022 的四件：源路径、渲染产物路径（可多条）、文档引用、
  追溯记录路径。缺任一件的「已完成」结论 MUST NOT 被写成证据。
- **C-023** 负向可观测（FR-023）由**夹具 + 检查器**承担，不需要真渲染：删掉渲染产物 ⇒ 下一次
  `--action obligation` 报 `missing` / `orphan-source`；删掉源 ⇒ 报 `missing` / `orphan-source`；
  触碰源使其 mtime 更新 ⇒ 报 `stale` / `source-newer-than-render`。三种都必须**转红**；
  一直绿即「未验证」而非「满足」。
