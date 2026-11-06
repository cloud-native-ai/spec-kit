# Contract — Flow Obligations（两个写入流程的配套图义务）

**Feature**: 087 架构图为核心的文档空间 | **Date**: 2026-11-06
**Surfaces carrying these obligations**（章节名逐字取自当前 owner 文件，`grep -n '^###'` 实测 2026-11-06；
两处 `#### Assets` 的指向都是**本特性新建**的那个小节（当前不在盘），见下方读法说明）：
`skills/external/create-docs/SKILL.md`（`### Desired-State Baseline`、本特性在**该节内新建**的 `#### Assets` 小节、
`### Reconcile Loop` 的 R2–R6、`### Authoring Flow（文档写作流程）` 的 R2–R6）、
`skills/external/improve-docs/SKILL.md`（`## Workflow` 的 `### 2. Gather evidence` / `### 3. Classify the improvement`
/ `### 4. Apply the minimal section-level edit` / `### 5. Verify`）、
`templates/commands/docs.md`（`### 分派(本命令保留的编排职责)`）。

> **`#### Assets` 的读法（MUST NOT 读作既有 owner）**：`skills/external/create-docs/SKILL.md` § Desired-State Baseline
> **当前没有** `#### Assets` 小节（实测 2026-11-06：`grep -n '^####'` 无输出，基线只有 1–4 四个编号条目）。
> 它是**本特性在实施期于该节内新建**的小节，建成后才是 `assets/` 区域约定的 owner（`C-009`、`[D-010]` 与
> `plan.md` T-005 都指向它）。在此之前，「图的落点」这一事实的唯一登记处是 `C-009`（本特性自己）；
> 本文件中任何形如「§ Desired-State Baseline 的 `#### Assets` 条目（owner）」的句子，一律读作
> 「本特性在 § Desired-State Baseline 内**新建**的 `#### Assets` 小节（建成后即 owner）」。
**FR served**: FR-005, FR-006, FR-007, FR-009, FR-010, FR-012, FR-017, FR-022
**Owner of this contract**: this file. The checker vocabulary the flows *call* is owned by
`contracts/diagram-obligation.contract.md`; this file MUST NOT restate it (it cites `[D-nnn]`).
The drawing capability's own rules are owned by `skills/external/draw-diagram/` and are cited, never paraphrased.

**引用记号**：`[D-nnn]` = `contracts/diagram-obligation.contract.md` 的 `C-nnn`（`D` 是 Dogfooding/Diagram 的
契约前缀，避免与本文件的 `C-nnn` 撞号；本文件自身条款仍写 `C-nnn`）。三处最常被引用的落点：
`[D-005]` = 该文件的封闭 `reason` 集；`[D-010]` = 追溯记录 schema；`[D-013]` = payload 形态与 `converged` / `clean` 两个谓词的定义点。

> **notation alias（记号别名，读法一次说清）**：本文件的 `[D-nnn]` 是**契约条款代码**——
> `[D-013]` 读作 `diagram-obligation.contract.md` 的 `C-013`，`[D-001]` 读作该文件的 `C-001`。
> 它**不是** `.specify/memory/register.md` 的残差记录 ID：同名记号 `D-001` / `D-001-a` 在那本登记册里
> 是「本特性显式未覆盖的语义面」的记录号（`plan.md` § Residual Risk 的 `D-001`），与契约条款是**两个
> 不同的命名空间**。两种记号在本特性的工件里并存，判据只有一条：带方括号的 `[D-nnn]` 是契约条款，
> 不带方括号的 `D-nnn` 是残差记录。实现者若把 `[D-001]` 读成 register 的 `D-001`，会把「`C-001` 的命令面」
> 误解成「一条未覆盖的残差」，两者的处置方向相反。

---

## A. 义务内容（两个流程的共同面）

- **C-001** 一次产出 = **四件在盘产物**，缺一即该运行 MUST NOT 报完成：载体文档、图的**可再编辑源**、
  **渲染产物**（交付契约对该引擎层要求的全部格式）、文档内**解析得到的相对引用**。四件的清单与
  「两面分为两面报告」的形态引 `[D-007]`（两组证据清单是它的实例）。
  第四件之外的第五件——**追溯记录**——由 `C-003` 单独承担，因为它由运行写、由检查器读，不属「图的两面」。
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
  - **R6 验证**追加一次 `docs-utils.py --action obligation --record <本次运行记录>` 并把 verdict
    并入残差报告；`missing` / `stale` / `not-evaluated` 任一非零 ⇒ MUST NOT 报「收敛完成」。
- **C-008a — Reconcile 的收敛路径（P1-5，**MUST 可判定地收敛到零图 finding**）**
  § Reconcile Loop 的 **R3 差异**与 **R4 干跑计划**、**R5 收敛**各追加一条，使「图」成为一次
  reconcile 可以真正收敛掉的维度，而不是一个永远 `missing` 的观测项：

  | 步骤 | 追加内容 | 判据 |
  |------|----------|------|
  | R3 差异 | 把 `--action obligation --root . --record <最新记录>` 的 verdict **作为差异项**并入差异集（与 `validate` 的违规同级），`missing` / `stale` / `not-evaluated` 三档都进计划 | 三档中任一非零 ⇒ 本轮差异非空 |
  | R4 干跑计划 | 每条差异生成**一条产图/重渲染条目**：`[ ]` 行写文档路径 + 计划图类 + 引擎层（未知则写「待前门路由」）+ 落点（`assets/`，C-009）；这条属**纯写**条目，可与其它纯写条目一起内联展示，**不**进「移动/归档」的逐项 opt-out 清单（写图不是搬迁） | 计划里每条 `missing`/`stale`/`not-evaluated` 文档恰有一条对应条目 |
  | R5 收敛 | 对每条条目调 `draw-diagram` 前门（C-002）产出两面 + 文档相对引用 + **同一次运行**写追溯记录（C-003），落点按 C-009 | 条目执行后该文档的 `--action obligation` verdict 变为 `satisfied` 或有效的 `recorded-exemption` |
  | R6 验证 | 重跑 `--action obligation` 并出**图维度残差报告**（四个计数 + `converged` + `clean` + `exempted`）；`missing` / `stale` / `not-evaluated` 任一非零 ⇒ MUST NOT 报「收敛完成」；`D-001` 的语义面 MUST 在报告里以「未覆盖」字样出现一次 | 收敛后的第二次 reconcile：`converged=true`（按 `C-013` 的 `converged` 谓词：`judged_scope_has_carrier && 三档全零`；不是单看三档）。**收敛判据是 `converged`，不是 `clean`**：`clean` 更严格（`exempted>0 ⇒ clean=false`，`[D-013]`），带具名豁免的文档是 `FR-004` 的合法终态，因此 `converged=true` + `clean=false` 是**合法**的收敛结果；报告 MUST 同时给出 `exempted` 计数，使「靠豁免收敛」与「靠产图收敛」可区分 |

  **收敛责任的归属（单一 owner，MUST NOT 两处都声称）**：产图与重渲染**在 reconcile 的 R5 内完成**，
  经既有 `draw-diagram` 前门、经既有 safe-local-writes 分级（C-010），**不**移交给 Authoring Flow——
  reconcile 的 scope 是「单目标/全量」，不是「写作委托」，二次委派会把一次 reconcile 变成一个无法判定的递归。
  `not-evaluated` **不跳过**：它意味着「尚未被接受」，R5 的条目即「补记录或补图」，补完重判（C-012 的说明段）。
  **永不收敛的一种残差必须显式**：`D-001` 的语义面（不由本机制收敛，MUST 在报告里点名）。
  `exempt-*` 文档**不是**残差：`recorded-exemption` 是合法终态，它只让 `clean=false`（`[D-013]`），
  不阻断 `converged`——报告 MUST 把豁免单独计数，MUST NOT 把它混进「已收敛」以外的任何「未收敛」口径里。
- **C-009** 图产物 MUST 落在**既有 taxonomy 内**，且**只有一个落点约定**（`plan.md` T-005 裁定）：
  载体文档所述结构对应的图，其源与渲染产物落 `<root>/docs/assets/<slug>.<ext>`（本仓先例
  `docs/assets/quickstart-workflow.{puml,svg,png}`），文档以**相对引用**指向它（`../assets/x.png`）。
  - `assets/` 的区域约定与「不是文档」的判定，**建成后**归本特性在 § Desired-State Baseline 内**新建**的
    `#### Assets` 小节（该小节当前不在盘，见本文件头部的读法说明）；本条款只登记「图的落点就是它」，
    MUST NOT 重述该小节的判据，也 MUST NOT 把「它已经是既有 owner」当成写它之前的前提。
  - **MUST NOT** 新建顶层文档类型目录（FR-002）；**MUST NOT** 为图另起一个与该约定并列的第二落点
    （同目录 `diagrams/` 子树即第二落点，已由 T-005 排除）。
  - 跨文档共享一张图时，落点不变（仍是一处 `assets/`），由多份文档各自相对引用（C-005）。
- **C-010** § Tiered Confirmation **一格不加**：写图仍是 safe local writes（自动执行）；移动 / 归档 / 重构
  仍是 stop-and-confirm。本契约 MUST NOT 引入第三档。

## C. 适配面：`improve-docs`

- **C-011** `## Workflow` 的 `### 2. Gather evidence (deterministic sources first)` 追加一项：读该文档的追溯记录
  `[D-010]`（存在时），作为「这张图是什么、哪个引擎、哪两面」的机器证据。
- **C-012** `### 3. Classify the improvement` 的分类表追加**一行**（表本身由该技能拥有，本契约只登记这一行必须存在）：
  **Diagram-sync**——「改进改到了图所描绘的事实（组件名、关系、步骤顺序）」；**验证后果**：
  「同一次运行更新图或报具名 staleness finding，二者必居其一」。
- **C-013** `### 4. Apply the minimal section-level edit` 追加：命中 Diagram-sync 时，按 C-001…C-004 更新；
  **不命中时** MUST 在原处打一行「本次无需图工作」并在报告里重复一次（FR-007：MUST NOT 为表演活动而重渲染）。
- **C-014** `### 5. Verify` 追加：`docs-utils.py --action obligation --only <该文档>` 的 verdict 必须是
  `satisfied` 或有效的 `recorded-exemption`；`stale` / `missing` / `not-evaluated` ⇒ MUST NOT 报改进完成。
  `--only` 收敛到 0 个对象时的 `clean` / `converged` 语义见 `[D-013]` 的附注，本条款不据此放行。
- **C-015** 无法重渲染（引擎层不可用）⇒ MUST 报**具名** staleness finding 并保留源文件不动
  （FR-006 后半 + C-004）。MUST NOT 把源回滚成「看起来一致」的形态。

## D. 适配面：`templates/commands/docs.md`

- **C-016** `### 分派(本命令保留的编排职责)`  MUST 增加一句：写作（authoring）与内容（content）两条路径**都**受配套图义务约束，
  义务正文**只引**两个技能（`create-docs` § Desired-State Baseline / § Authoring Flow、`improve-docs` § Workflow），
  MUST NOT 在命令里复述义务条文。
- **C-017** 同节的产出行（`产出:audit log appended … + residual report grouped by owning skill`）MUST 把图维度并进残差报告的分组：
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
- **C-023** 负向可观测（FR-023）由**夹具 + 检查器**承担，不需要真渲染，逐面点名（`[D-005]` 的 `orphan-*` 两值）：
  删掉**渲染产物** ⇒ `missing` / `orphan-rendered`；删掉**源** ⇒ `missing` / `orphan-source`；
  触碰源使其 mtime 更新（两面都在）⇒ `stale` / `source-newer-than-render`。三种都必须**转红**；
  一直绿即「未验证」而非「满足」。三种的夹具、步序与期望读数**唯一登记处**是
  `plan.md` § Test Plan 的夹具表与 `quickstart.md` S3——本条款只声明义务，不复述步序。
