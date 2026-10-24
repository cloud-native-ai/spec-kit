# Research & Decisions — Feature 069 / Slice 069b

**Date**: 2026-10-25 · **Branch**: `069b-isomorphism-migration-metrics` · **Base/HEAD**: `f0df3d0b`
**Scope**: 本切片 plan 阶段的 Phase 0 决策。所有「实测」项均在 2026-10-24/25 同机执行并附命令；
「推断」项显式标注。判据正文（分类判据、六面门禁判据、阶段名册）不在本文件复述——它们的 owner 是
`shared/definitions/flow-class-definitions.md`、`shared/workflow/expression-gates.md`、
`skills/external/sdd-loop-driver/scripts/loop-state.py`。

**Same-author note**: 本运行无子代理派发工具，Constitution Check 与 Post-Generation Quality Gate 的同作者打分
按 `.specify/shared/workflow/objective-analysis-gate.md` § 7 降级为**直接有界复核**（`scored: direct read, subagent unavailable`）。

---

## R1 — 映射与边界的载体：闭合 069a 的交接行，不新建文档

**决策**: 同构映射（8 行 × 3 面）与四类不可同构边界写入 `shared/definitions/flow-class-definitions.md` 的
两个新章节（`## 同构映射（8 阶段 × 3 面）`、`## 不可同构边界`），并同步该文档开篇 owns 列表。

**依据（实测）**: `wc -l shared/definitions/flow-class-definitions.md` → 208 行；第 19 行是交接行
「同构映射（8 阶段 × 3 面）与不可同构边界 | 由 069b 承接；本版只保留这一行指针，不展开映射行」；
开篇 owns 列表不含这两项。本动作是**执行交接**，不是修改父条款（父编号 036 本来就要求该文档同时拥有映射与边界）。

**被否方案**: 新建 `shared/definitions/isomorphism-map.md`——会产生第二个分类相关 owner，且父编号 036 /
切片 FR-001 都写死「唯一载体」。

## R2 — 表形：6 列 × 8 行，阶段行集与名册 owner 对齐

**决策**: 表头逐字取 `| 阶段 | 结构（实体 / 关系 / 边界） | 流程（阶段与门禁角色） | 逻辑（证据 / 契约 / 验收 / 版本 / 所有权） | 强制门禁 | 强制状态 |`；
8 个数据行的首格 MUST 等于阶段名册的阶段集合。

**阶段名册引用（实测）**: `skills/external/sdd-loop-driver/scripts/loop-state.py` 的 `STAGE_ARTIFACTS` 字典键
= `requirements / clarify / plan / tasks / checklist / analyze / implement / review`（8 个）；同文件的注释声明它是
stage → artifacts 的**运行时 owner**，`references/state-awareness.md § Stage Artifact Map` 是其镜像。
测试侧以「从 `loop-state.py` 解析出的键集合」为期望值（这是合法的 drift-guard 字面量，不构成第二份名册）。

**被否方案**: 在映射表里自建阶段清单或加 `version` 字段——违反 FR-001「MUST NOT 新建第二份名册；名册变更时映射跟名册走，不另立版本」。

## R3 — 24 格的格语法：一条 `↔`，两侧都必须落到具体产物

**决策**: 三个面列（结构 / 流程 / 逻辑）的每一格 MUST 形如
`代码型：<产物或判定面> ↔ 文档型：<产物或判定面>`，恰好一个 `↔`，两侧各 ≥ 8 字符。
面的含义由表前一段 legend 一次性声明（结构 = 实体 / 关系 / 边界；流程 = 阶段与门禁角色；
逻辑 = 证据 / 契约 / 验收 / 版本 / 所有权），不塞进每个格。

**依据**: 父编号 018 要求 24 格且「每行给出代码型产物 ↔ 文档型产物的对应」；「两侧都写」是这句要求的最小机械形态。
把面义写进 legend 而不是格里，是为了让格只承载**对应关系**，避免同一含义在 24 格里复制 24 份（事实一致性面）。

## R4 — 强制标注是一个可判定的代理，而不是措辞

**决策**: `强制状态` 取封闭两值 `已强制` / `已声明未强制`。
- `已强制`：`强制门禁` 格 MUST 写出 ≥1 个 face id（来自门禁 owner 的六面表），且每个被指名的
  `(阶段, face)` 对 MUST 在 `shared/workflow/expression-gates.md` § 阶段算子表中存在 `blocking` 算子行。
- `已声明未强制`：`强制门禁` 格 MUST 为空；且该阶段 MUST **不存在任何** `blocking` 算子行。
- 两种违反分别是 `annotation-false-enforced` / `annotation-false-unenforced`；既无门禁也无标注 = 口号行。

**依据（实测）**: 阶段算子表 16 行；逐阶段 `blocking` 行数 = requirements 2 / clarify 2 / plan 2 / tasks 2 /
checklist 2 / analyze 2 / implement 1 / review 2。**8 个阶段全部存在 blocking 算子**，因此本切片交付的映射表
8 行都将是 `已强制`；`已声明未强制` 是一个**已实现、被 fixture 覆盖、但当前无真实行**的合法取值——SC-001 只要求
「未标注行 = 0」，不要求「未强制行 > 0」；SA-8 明确该取值不是豁免。

**被否方案**: 按「该行是否真的检查了 correspondence」逐行人工判断——不可判定，且两名判定者会给出不同答案。
本代理把「真实性」绑定到门禁 owner 的可解析结构上：标注失真的行会转红（FR-002）。

## R5 — 四类不可同构边界：四条封闭行，每条必须绑到一个门禁面

**决策**: `## 不可同构边界` 是 4 行表：`| 边界 | 不可互换的判定面 | 为什么不能互换 | 门禁处理 |`，
`边界` 取 `a` / `b` / `c` / `d` 各一次（对应 FR-003 的验收 oracle / 验证算子 / 失败可见性 / 语义 oracle 缺失）；
`门禁处理` 格 MUST 含 ≥1 个封闭 face id。边界与映射同属一个文档（FR-003 第二句）。

**被否方案**: 边界写成散文清单——无法核对「四类齐全」与「每条可在至少一处门禁设计中指出对应处理」（SC-001 后半句）。

## R6 — 台账「生效版本」的承载形态：文档版本 + 既有变更记录

**决策**: 选「文档版本 + 逐行变更记录」这一形态，并**在所有者内声明一次**：
`**台账版本**: 1（<date>）`，生效版本由该声明与既有 `## 变更记录` 共同承载；**不新增行级 `effective_version` 列**。

**理由**: (a) 78 行台账加列要重写全表，且会改动 069a 的 C-4 行语法与测试；(b) 父 FR-016 的版本不兼容判据是
「表头 / 列集合与解析器期望不符」，加列等于换表头——正是该判据要拦的「第二个版本信号」；(c) `## 变更记录`
已是 069a 落盘的审计形态（`date | unit_id | before → after | basis | 依据`），复用即可满足 FR-010 的「生效版本」语义。

**检查**: 声明缺失 → `ledger-version-missing`（新 finding kind），必须出现且恰好一次。

## R7 — 对账器扩展：floor + coverage + red_kind，且不破 069a 测试

**决策**: `scripts/python/flow-class-check.py --action check` 增量扩展：
1. 新增 finding kind `ledger-truncated`：解析出的台账行数 < `LEDGER_FLOOR = 78`（实测常量，不复算）；
2. JSON 增加 `coverage` 块（`ledger_rows` / `inventory_units` / `matched` / `gaps` / `parse_errors` / `floor`）；
3. JSON 增加 `red_kind`：`clean` / `gap` / `parse-failure` / `owner-unavailable` / `framework-source-required`，
   优先级 `owner-unavailable > framework-source-required > parse-failure > gap > clean`；
4. 既有 8 个 finding kind、退出码阶梯 0/1/2、`lookup` 语义全部不变。

**兼容性实测**: `tests/unit/test_flow_class_check.py` 的行级夹具在注入坏行时仍保留 78 条可解析行
（`_build_repo` 建 78 行，再 `append` 坏行），因此 `ledger-truncated` 不会在那些用例上额外触发；
`test_inventory_truncated_below_*` 建的是 `templates/commands` **存在但数量不足**的树，仍走 `inventory-truncated`。

**被否方案**: 把 `inventory-truncated` 直接换成作用域标签——会破 069a 的 4 条 floor 用例（见 R11）。

## R8 — 委托关系核验：从模板文本解析，不维护第二张委托表

**决策**: 新动作 `--action delegation`。委托边 = 命令模板中出现的技能路径，语法
`(?:\.specify/)?skills/(?:external/|internal/)?<name>/SKILL.md` → 单元 id `skill:<name>`。
每条边 MUST 满足：该技能在台账中存在；其 `flow_class` 等于命令的 `flow_class`，**除非**该技能在类中立清单内。

**实测（2026-10-25）**: 27 个命令模板中 26 个声明了 ≥1 条技能路径（`tools` 没有）；解析出的全部边今天
**零类不一致**；6 条边因类中立豁免（`docs→memory-record`、`feedback→manage-feedback`、`history→memory-record`、
`instructions→memory-recall`、`instructions→memory-record`、`session→archive-session`）。
因此该检查在当前树上应为**绿**，其证伪能力由 fixture（把一个技能改成反类 → 转红）承担。

**被否方案**: 维护一张「命令 → 委托技能」的人工清单——FR-012 明确禁止（「MUST NOT 依赖人工维护的委托清单」）。

## R9 — 六面 owner 指针完整性：一个绑定格，可含「主机制 + 执行件」

**决策**: 新动作 `--action faces`。解析 `shared/workflow/expression-gates.md` § 六面 表：
恰好 6 行、face id 唯一、每行**一个** `owner_pointer` 格（格内 MAY 用 `+` 连接两个路径，仍算**一个绑定**——
实测 `requirements-clarity` 与 `structure-links-build` 就是这样写的）；每个路径 MUST 在仓库内可解析，
带 `§ <anchor>` 时该锚 MUST 能匹配到文件内标题；六面之外的文件里出现「≥3 个 face id 同表」→ 第二绑定表缺陷。

**依据（实测）**: 六面表 6 行；`requirements-clarity` = `scripts/python/validate-requirements.py` +
`requirements-guidelines.md § Specification Quality Validation`，`structure-links-build` = `create-docs/SKILL.md § Desired-State Baseline`
+ `docs-utils.py`，其余四面各一个路径（`fact-consistency` 明确「整文件即判据，无单章节锚」）。

## R10 — 「判据正文在 owner 之外出现 0 次」的可测形态：复用既有 duplicate 面，主体集封闭

**决策**: SC-005 的后半句用 `scripts/python/doc-consistency-check.py --faces duplicate` 测量，但**主体集封闭**为
本切片的产出面（`shared/definitions/flow-class-definitions.md` + 本 spec 的 formal artifacts），比较侧沿用该引擎已声明的
S3 六面 owner 集；要求 `findings = 0`。`shared/workflow/expression-gates.md` 本身是 S3 owner（`evidence-asof` 面），
**不入主体集**。

**理由（实测 + 披露）**: 069a review 的 REC-069a-11 已记录一处**既有**缺陷：`expression-gates.md § 事实一致性`
复述了 `one-source-of-truth.md` 的判据。若把 expression-gates 当主体，SC-005 会继承该既有红；修复它属于重写 069a 规则，
本切片无权做。把它排除在主体集之外不是放宽判据——SC-005 的对象是「本切片不得把判据正文搬出 owner」，
而 `expression-gates.md` 恰好是六个 owner 之一，按「排除集 = 六个 owner 路径本身」它本就在排除侧。

**被否方案**: 全仓 grep 六个 owner 的每一行——不可判定（owner 的普通措辞会与任何文档碰巧相同），且必然命中既有红。

## R11 — 作用域：三个新动作 + `check` 只在框架源仓运行；payload 根给具名状态

**决策**: `check` / `delegation` / `faces` / `isomorphism` 解析失败于「框架源树缺失」时，退出码 2 +
`error.label = framework-source-required`，**不产出 findings、不当绿**。触发条件：仓库既无 `templates/commands/`
又无可解析的 `skills/{external,internal}/`（即客户 payload 根形态）。`lookup` 保持双帽子解析（源码根或 `.specify/` 载荷根均可）。

**依据（实测）**: 客户项目只拿到 `.specify/` 载荷（命令副本 + 扁平 `.specify/skills`），没有 `templates/commands/`；
069a 的 `check` 在该形态下必然报 `inventory-truncated` + 大量 `unknown`（REC-069a-06 的根因）。
本决策选 REC-069a-06 的第二个选项「gate the payload to the framework repo」，并把「不适用」做成具名状态而不是红。
`tests/unit/test_flow_class_check.py` 现有的 floor 用例都建了 `templates/commands/`，不触发该分支。

**披露**: 这仍是一个「在客户项目里没有通过状态」的动作——但它现在**说清楚了自己不属于那里**，
而 `lookup`（客户真正需要的运行时动作）完全可用。本切片不新增项目侧扫描范围与 floor（那会新增第二套分母）。

## R12 — 三项基线：按既有仪器冻结，无样本记 not-evaluated

**实测冻结值（冻结点 = `requirements.md` 首次提交 `f0df3d0b`，author date `2026-10-24`）**:
- `gate_calls` = `0`（冻结前本切片无检查类单元调用记录）：`not-evaluated`（分母 0，降幅不可定义）；
- `confirmations` = `0`（`feedback-utils.py --action list --lifecycle-point gate-` 命中 0 条；clarify 未运行、0 轮提问）：
  绝对值实测，降幅 `not-evaluated`；
- `wall_clock` = `null`（本切片尚无 `/speckit.analyze` 运行判定记录）：`not-evaluated`。

**仪器（全部既有）**: `exec-quant.py --action list-records`、`feedback-utils.py --action list`、
`run-determination.py --action history`、`git log -1 --format=%cs -- <requirements.md>`。无新采集器（FR-014）。

**披露**: 069a 的 `notes/expression-baseline.md` 已在同口径下记过同类 `not-evaluated`；本切片不把它的值当本片前值
（两者样本不同），也不据此声称任何降幅。

## R13 — 客户项目快照：三个未刷新项目，archive 副本，名字级比对

**实测（2026-10-25）**:

| # | 项目 | 路径 | HEAD | 分支 | 工作树脏文件 | 069a 载荷 | 套件命令 |
|---|------|------|------|------|--------------|-----------|----------|
| 1 | xuanji-agent | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-agent` | `3f68b62` | `master` | 195 | 无（未刷新） | `.venv/bin/python -m pytest tests/ -q` |
| 2 | xuanji-cli | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-cli` | `a0c476d` | `xuanji/develop` | 548 | 无（未刷新） | `go test ./...` |
| 3 | xuanji-function | `/Users/liuqiming.lqm/project/kangaroo-xuanji/xuanji-function` | `a2fad18` | `main` | 28 | 无（未刷新） | `.venv/bin/python -m pytest -q`（`pytest.ini` 存在） |

**决策**: 快照 = `git archive <HEAD> | tar -x -C <tmp>` 的**临时副本**；原始项目与工作树脏改动都不参与，
也不被修改（`git archive` 只读）。刷新在副本上进行，跑测前后各采一次 `--names-out` 名字集，`comm -13` 断言为空。
三个项目本机均有 `.venv/bin/python` 与 `go1.27.2`（实测），具备跑测前提。

**披露**: 工作树脏改动被排除是**设计选择**（要可复现的快照），不是遗漏；若某套件依赖未跟踪文件（`.env` 等）而无法启动，
按 FR-014 的降级记 `not-evaluated` + reason，MUST NOT 记 0 新增失败。

## R14 — 不新增采集器、不新增项目侧存储

**决策**: 三项基线只读既有四个通道；新动作全部只读、不写任何文件；基线/样本/测试基线记录都是本 spec 的
`notes/`（每特性一份的 dated 记录），不是运行时存储；本切片不在客户项目新增任何读取点。

**被否方案**: 新建一个「同构映射台账 JSON」或「度量采集脚本」——直接违反 FR-008 / FR-014 与父编号 032。

## R15 — 待处置的既有措辞偏差（实现期动作，本阶段只登记）

| # | 位置 | 现状（实测） | 本切片应做的收敛 | 依据 |
|---|------|--------------|------------------|------|
| P1 | `shared/definitions/flow-class-definitions.md:8` | 四个共享字面量的登记处被指向 **069a** 的 § Shared Strings；语义 owner 是父规格 | 改为「父规格 § Shared Strings 是语义 owner；069a / 069b 的表是同源投影」 | 切片 requirements § Shared Strings Owner 声明 |
| P2 | 同文件 `:19` | 「由 069b 承接；本版只保留这一行指针」 | 由实体章节取代该行（R1） | FR-001 / FR-003 |
| P3 | 同文件 `:88` | 「声明机制不在 069a（迁移与兼容由 069b 承接），本版不提供项目侧声明面」 | 收敛为已裁定语义：客户 MAY 在自己的知识空间记录，**框架不读取**；不提供项目侧声明面与存储/读取点 | FR-008、Clarifications 最后一条 |
| P4 | 同文件台账说明中的两处「069b 承接规范」 | 指向一个当时尚不存在的规范 | 改为指向已落盘的契约条款（`contracts/isomorphism-map.md` C-7 / `contracts/ledger-reconciler.md` C-7） | FR-011 |

这四处只改指针与措辞，不改 069a 的判据正文；P1–P4 都要随 `shared → .specify/shared` 镜像同步（见 plan § Mirror Obligations）。

---

## 未采纳的替代方案（汇总）

| 方案 | 被否理由 |
|------|----------|
| 新建 `isomorphism-map.md` owner | 第二 owner，违反 FR-001 与父编号 036 |
| 行级 `effective_version` 列 | 换表头 = 换版本判据，且重写 78 行（R6） |
| 用「映射行是否检查 correspondence」人工判强制 | 不可判定，两名判定者会分歧（R4） |
| 全仓 grep 判据正文 | 不可判定且继承既有红（R10） |
| 客户 payload 内做台账对账 | 无命令清单分母，只能伪造 floor（R11） |
| 把 069a 的基线值当本片前值 | 样本不同，属跨特性顶替（R12） |
| 修改客户项目工作树做快照 | 不可逆、污染客户仓（R13） |
