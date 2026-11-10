# Data Model — /speckit.migrate

**Spec**: `requirements.md` · **Plan**: `plan.md` · **Date**: 2026-11-10

本模型只记录**本命令自有的数据形态**。处置值域与期望态检查项的 owner 在 requirements / 既有引擎，本文件不复述：

- 处置（Disposition）的封闭取值域：owner = `requirements.md` FR-014。本文件的字段声明仅写「取值域见 FR-014」，映射表使用其 machine token 作为值。
- 五类维度的语义边界：owner = `requirements.md` FR-007。本文件只固定其 machine token 与排序。
- 退役清单、残留类别、链接清单、镜像对：owner = `research.md` R-2 钉名的既有声明与引擎，本文件不另列。

## E-1 DiffItem — 差异项

最小可审阅单位；计划与回执的逐项载体（requirements Key Entities）。

| 字段 | 类型 | 约束 |
|------|------|------|
| `id` | string | `sha1(dimension + "\|" + target)[:12]`，与 sanitize 发现项同构；同一计划内唯一 |
| `dimension` | enum | `templates-generated` \| `anchor-layout` \| `compat-links` \| `mirror-consistency` \| `migration-residue`（排序即此列顺序） |
| `target` | string | 项目工作区相对路径（POSIX 分隔符）；链接项指向链接路径本身 |
| `current` | string | 当前态的可判定描述（如 `missing`、`differs`、`symlink-broken`、`legacy-location`、`registry-listed`） |
| `expected` | string | 期望态描述（如 `byte-equal to installed asset`、`moved-to: <path>`、`symlink -> .specify/instructions.md`、`absent`） |
| `disposition` | enum | 取值域见 FR-014；本项拟执行的处置 |
| `mechanism` | enum | 执行机制：`copy` \| `replace` \| `archive` \| `relocate` \| `symlink` \| `anchor-engine` \| `mirror-engine` \| `none` |
| `evidence` | string[] | 依据路径：owner 文件/检查器/引擎路径（FR-006 的「依据路径」） |
| `archiveTo` | string \| null | 归档目标（`.specify/archive/migrate/<run-id>/<rel>`）；无归档时 null |
| `status` | enum | `planned` \| `done` \| `refused` \| `blocked` \| `failed`（`converged` 项不进入计划，见 E-2；不设 `skipped`——跳过即违约 I-4） |
| `reason` | string \| null | `refused` / `blocked` / `failed` 时必须非空 |

**验证规则**
- 同一计划内 `(dimension, target)` 唯一（合并去重，不双报）。
- 排序稳定：先 `dimension` 的固定顺序，再 `target` 字典序；同输入重复干跑逐字节相同。
- `disposition=refuse` 时 `archiveTo=null`，`reason` 必须指名冲突双方（两个候选路径）。
- `disposition=blocked` 时 `status=blocked`，`reason` 必须写明「未获第二把钥匙」或「非交互环境」。

## E-2 Plan — 差异计划

| 字段 | 类型 | 约束 |
|------|------|------|
| `planVersion` | int | 常量 `1` |
| `mode` | enum | `dry-run` \| `apply` |
| `workspace` | string | 绝对路径（回执中记录；不进入排序键） |
| `workspaceKind` | enum | `framework-source` \| `client`（判定：`skills/external/` 存在性与 sanitize 既有 guard 同源） |
| `items` | DiffItem[] | 见 E-1 |
| `summary` | object | `{total, byDimension: {<dimension>: n}, byDisposition: {<disposition>: n}}` |
| `notes` | string[] | 降级事实（`command-copies: no tool surface detected` 等）。可判对象存在的降级（如平台无符号链接）以 `refuse` item 表达并阻止 clean；无可判对象的降级只作可见提示，不阻止 clean，但 MUST 出现在输出与回执 |
| `pointers` | Pointer[] | 见 E-9；FR-013 的静止责任方指针，恒定出现，不探测、不处置 |

**状态转移**：Plan 本身无状态机；`dry-run` 计划只存在于内存与输出流，`apply` 计划随 E-4 回执固化。

## E-3 Receipt — 迁移回执（逐运行一文一件）

落点：`.specify/memory/migrate/receipts/<run-id>.json`（apply 模式）。干跑零写入：同一结构作为 `receipt` 字段随 stdout / `--format json` 输出，**不落盘**。

| 字段 | 类型 | 约束 |
|------|------|------|
| `receiptVersion` | int | 常量 `1` |
| `runId` | string | `<UTC compact stamp>-<8 hex>`，例 `20261110T093012Z-1a2b3c4d`；文件名 = `<run-id>.json` |
| `mode` | enum | `dry-run` \| `apply` |
| `status` | enum | `running` \| `completed` \| `aborted`（apply 开始时写 `running`，正常收束写 `completed`；崩溃留下 `running` 供续跑识别） |
| `startedAt` / `finishedAt` | string \| null | ISO-8601 UTC；`running` 时 `finishedAt=null` |
| `resumedFrom` | string \| null | 续跑时指向被接续的 `runId` |
| `source` | object | `{stampFile: ".specify/source.json" \| null, frameworkCommit: string \| "unavailable", stampedAt: string \| null, reason: string \| null}`；只作记录（FR-020） |
| `target` | object | `{cliVersion: string, frameworkCommit: string \| "unavailable", origin: "git" \| "embedded" \| "unavailable"}` |
| `outcome` | enum | `clean` \| `planned` \| `applied` \| `blocked`（见 E-5） |
| `exitCode` | int | 与 outcome 一一对应（E-5） |
| `items` | DiffItem[] | 逐项处置与最终 status |
| `archives` | ArchiveEntry[] | 见 E-4；替换/移除/搬迁类均产生条目；`refused` / `blocked` 项不产生条目 |
| `recover` | string[] | 人类可读的恢复路径说明，逐归档/搬迁条目一条 |
| `notes` | string[] | 同 E-2 的降级事实 |
| `pointers` | Pointer[] | 同 E-2；回执同样承载静止指针（FR-013） |

**验证规则**
- 并发安全：两个并发运行产生不同 `runId` → 不同文件路径；运行期内只改本运行自己的文件，不触碰其他回执。
- 恢复路径可枚举：每个 `archives[]` 条目都能在 `archiveTo` 找到对象（`change=relocated` 的对象位于新位置）；存在性断言由测试执行。
- 干跑回执 `status=completed`、`outcome=planned`（或 `clean`）、`archives=[]`。
- **FR-018 解释记录**：干跑受 FR-006「零写入」绝对约束，回执以输出流形态（`receipt` 字段）承载全部字段，落盘仅发生于 apply；前置条件/输入错误（`error`）按 FR-003「零文件创建」不产回执。两处均在此记录为对 FR-018 的确定性解释。
- **续跑键**：新运行不按自己计算的 `archiveTo` 判断既有归档（run-id 不同），而是读取最近 `status=running` 回执中逐项的 `archiveTo` 与 `items[].status`（见契约 `migrate-engine.md` C-7）。

## E-4 ArchiveEntry — 归档条目

| 字段 | 类型 | 约束 |
|------|------|------|
| `path` | string | 被处置对象的工作区相对路径（搬迁时为源路径） |
| `archiveTo` | string | 归档：`.specify/archive/migrate/<run-id>/<rel>`；搬迁：目标规范位置（`to`）。两者都是「找回入口」 |
| `change` | enum | `replaced` \| `archived` \| `removed-stale` \| `relocated` |
| `digest` | string | 处置前对象的 `sha256`（目录对象取清单式哈希，见实现说明） |

**续跑与恢复**
- `relocated`：对象内容在新位置；`recover` 说明回迁方式（把 `archiveTo` 移回 `path`）。续跑时若 `archiveTo` 存在且 `path` 缺失 → 视为搬迁已完成，不重复移动。
- 归档类条目（`replaced` / `archived` / `removed-stale`）：续跑只认**产生该条目的回执**（`status=running` 的最近回执）里的 `archiveTo`，不得用新运行自己的 run-id 路径推断。

## E-5 RunOutcome — 运行结局与退出码

| outcome | 语义 | exitCode | 触发 |
|---------|------|----------|------|
| `clean` | 无差异 | 0 | 计划为空（干跑与 apply 均可） |
| `planned` | 有差异的干跑 | 1 | dry-run 且 items 非空 |
| `applied` | 应用完成或已无剩余差异 | 0 | apply 且无 `refused` / `blocked` / `failed` 项 |
| `blocked` | 因确认门或冲突未完成 | 3 | apply 后仍存在 `blocked` / `refused` / `failed` 项（执行期 I/O 失败并入此结局，原因写入对应 item 的 `reason`；绝不报 applied） |
| `error` | 输入或前置条件错误 | 2 | 缺 `.specify/`、非法选项、`--apply` 与 `--dry-run` 互斥冲突等；不产生回执 |

映射为封闭表；实现常量由契约测试与 requirements FR-019 对齐（`contracts/migrate-cli.md` § C-3）。

## E-6 WorkspaceKind — 工作区形态

| 值 | 判定 | 影响 |
|----|------|------|
| `framework-source` | `<workspace>/skills/external/` 为目录（与 `sanitize-utils.check_legacy_install_residue` 的 guard 同源） | 镜像/生成副本维度委托 `sync-mirrors.py --check` 与 `regen-command-copies.py --check`；模板/技能/代理参照面对照仍可用（见契约 C-4） |
| `client` | 其余情形 | 五维全部由参照树对照（模板/技能/代理/命令副本/脚本/shared）与检查器组成 |

## E-7 ReferenceTree — 临时参照树（瞬态，不持久化，仅客户端工作区）

- 构建条件：`workspaceKind=client`。框架源工作区的资产维度由工作区自身引擎直接回答（契约 `migrate-engine.md` C-2），不建参照树。
- 位置：`tempfile.TemporaryDirectory(prefix="specify-migrate-")`，同一次运行内创建、`finally` 清理；不写工作区（干跑零写入的前提）。
- 内容：`copy_local_templates(reference_root, <detected assistant>, <detected script variant>)` 产出的 `.specify/` 投影 + 每个已探测工具目录的 `generate_commands` 产物。
- 工具探测：`_ASSISTANT_COMMAND_DIRS` 与工作区实际存在目录的交集；为空时在计划 `notes` 记录 `command-copies: no tool surface detected`（无可判对象，作可见提示，不伪装成「已检查且无差异」）。
- 脚本变体探测：现有生成副本中出现 `.ps1` 引用 → `ps`，否则 `sh`。

## E-8 维度 token 与来源映射（仅映射，不复制检查清单）| dimension | 检查来源（owner 路径） | 处置来源 |
|-----------|------------------------|----------|
| `templates-generated` | 客户端：参照树对照 `.specify/templates`（除 commands）、`.specify/skills`、`.specify/agents/templates`、各工具命令副本；框架源：`sync-mirrors.py --check` 的 templates / skills / agents 三个镜像对 + `regen-command-copies.py --check`（命令副本）。框架源模式**不**建参照树 | 缺失→`write`；存在且不等→`replace`；退役命令副本→`archive` |
| `anchor-layout` | `anchor-layout-migrate.py --action check`（`plan()` 的 `move` / `refuse-existing-target`） | `move`→`archive`（`mechanism=relocate`）；`refuse-existing-target`→`refuse` |
| `compat-links` | `sanitize-utils.check_broken_symlinks`（含 `COMPAT_SYMLINK_EXPECTATIONS` 的所属工具期望） | 缺失/断链→`write`（`mechanism=symlink`）；普通文件占位→`replace`；平台不支持→`refuse` |
| `mirror-consistency` | 客户端：参照树对照 `.specify/scripts`、`.specify/shared`；框架源：`sync-mirrors.py --check` 的 scripts / shared 两个镜像对（MISS/DIFF/ORPHAN） | MISS→`write`；DIFF→`replace`；strict ORPHAN→`archive`；非 strict 额外文件不动 |
| `migration-residue` | `sanitize-utils.check_legacy_install_residue` + `check_flat_internal_duplicates` + init 决策函数（退役资产、平铺内部技能） | 残留→`archive`；平铺→嵌套存在则 `archive`，不存在则 `archive`（`mechanism=relocate`） |

## E-9 Pointer — 静止责任方指针（FR-013）

| 字段 | 类型 | 约束 |
|------|------|------|
| `topic` | string | 固定 `goal-team-archive-migration` |
| `ownerCommand` | string | 固定 `/speckit.goal` 的 `migrate-archive` |
| `ownerEngine` | string | 固定 `scripts/python/goal-utils.py --action migrate-archive` |
| `note` | string | 一句话：本命令不探测、不处置该迁移 |

指针是常量输出，不随工作区变化；测试断言计划与回执都含该指针，且 migrate 不产生任何 goal/team 迁移项（SC-007）。

**不变量**
- I-1：`dry-run` 对工作区的写入次数为 0（含临时文件、回执、归档）。
- I-2：任何被执行的对象在被替换/移除前必有一份可枚举归档；搬迁类对象内容保留在目标位置。
- I-3：已归档对象在重跑中不被二次搬移（归档路径与 `runId` 绑定；续跑识别既有归档）。
- I-4：不存在静默跳过的差异项——每个 item 必有一个 disposition 与最终 status。
- I-5：六值处置域与 FR-014 逐字一致（契约测试从 requirements.md 提取 token 比对）。
