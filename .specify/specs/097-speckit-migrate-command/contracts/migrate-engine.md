# Contract — 迁移引擎：期望态、复用边界、安全与幂等

**Spec**: `requirements.md` FR-005…FR-018、FR-023…FR-025 · **Plan**: `plan.md` WP02–WP07、WP11–WP13 · **Date**: 2026-11-10

本契约固定「探测什么、从哪里读、怎么处置、怎么找回」的可判定规则。处置域（FR-014）、五维语义（FR-007）、破坏性判据（confirmation-gates owner）均按路径引用，不复述。

## C-1 维度集合与顺序

`dimension` 的 machine token 与顺序归 `data-model.md` E-8（唯一 owner）；语义边界 owner = FR-007。维度集合是封闭集，扩维须修订 requirements；契约与实现 MUST 引用 E-8，不得另行维护 token 清单。

## C-2 期望态读取（不另立来源）

| 来源 | 客户端工作区（`client`） | 框架源工作区（`framework-source`） |
|------|--------------------------|-----------------------------------|
| 框架资产投影 | 由当前安装资产运行**同一** init 复制机制到临时参照树：`copy_local_templates` + `rewrite_paths` + `generate_commands`（模块内既有函数） | `sync-mirrors.py --check` 的六个镜像对 + `regen-command-copies.py --check`；资产根 = 工作区根 |
| 退役清单 | CLI 模块常量（当前已安装版本） | 工作区 `src/specify_cli/__init__.py` 标记块（经 `sanitize-utils.load_obsolete_registry`；工作区无 `src/` 树时回退模块常量） |
| 残留/链接/平铺重复 | 已安装副本的 `sanitize-utils.py` 检查器（进程内导入） | 工作区自身 `.specify/scripts/python/sanitize-utils.py` 的检查器（镜像 lane 只在自身仓根生效） |
| 锚点布局 | 已安装副本的 `anchor-layout-migrate.py --action check`（CLI 动作） | 工作区自身 `.specify/scripts/python/anchor-layout-migrate.py --action check` |
| 镜像/生成副本 | 参照树逐文件对照（见 C-4） | `sync-mirrors.py --check` + `regen-command-copies.py --check`（解析 `MISS/DIFF/ORPHAN` 与漂移行） |

引擎装载点（承重）：客户端模式一律取 `get_resource_path()/scripts/python/`（= 当前已安装版本，不读工作区可能过期的 `.specify/scripts/` 副本）；框架源模式一律取工作区自身 `.specify/scripts/python/`（`run_sync_mirrors_check` 只在 `root == script_repo` 时运行，只有工作区副本满足）。本命令的 Typer 子命令始终是已安装 CLI 的那一份。

**禁止**：按项目版本号/模板指纹/内置旧结构清单选择路径（FR-005、FR-020）；新增 `.specify/version` 类判据。

## C-3 处置映射（值域引用 FR-014）

| 差异类 | disposition | mechanism | 归档 |
|--------|-------------|-----------|------|
| 期望文件缺失 | `write` | `copy` / `symlink` | 无 |
| 期望文件存在但内容不等 | `replace` | `replace` | 必归档旧对象 |
| 注册表退役项、旧代状态文件、旧工具目录、平铺重复（嵌套已存在） | `archive` | `archive` | 必归档 |
| 锚点搬迁、平铺→嵌套搬迁（目标不存在） | `archive` | `relocate` / `anchor-engine` | 内容保留在目标位置；回执记录 from→to，`recover` 说明回迁方式 |
| 冲突（目标已存在且内容不等价） | `refuse` | `none` | 不执行；回执指名两个候选 |
| 破坏性未获第二把钥匙 | `blocked` | `none` | 不执行 |
| 平台不支持符号链接 | `refuse` | `none` | 原因 `platform-no-symlink` |
| 已在期望态 | `converged` | `none` | 无（`converged` 项只在 apply 的内部收束判断中出现，`converged` 的差异项不进入计划项——计划只列真实差异） |

补充规则：
- 内容不等的既有框架文件一律走 `replace`（先归档再写），无法区分「用户手改」与「旧版本资产」时不冒险直写（FR-016、A11）。
- 非 strict 镜像对的镜像侧多余文件不处置（用户技能与项目扩展永不在候选内）；strict 对（`.specify/scripts`）的多余文件走 `archive`。
- 退役判断只认注册表与既有检查器的发现；`_OBSOLETE_COMMANDS` 只匹配对应工具命令目录中的同 stem 文件。

## C-4 客户端参照树对照规则

- 对照面：`.specify/templates/`（不含 `commands/`）、`.specify/skills/`、`.specify/agents/templates/`、`.specify/scripts/`、`.specify/shared/`、每个已探测工具的命令目录（`templates-generated` 与 `mirror-consistency` 按 data-model E-8 的映射归属）。
- 只比较「参照树中存在的文件」集合；参照树没有的文件**不是**待删项（除非注册表/检查器另有发现）。
- 目录级忽略：`__pycache__`、`node_modules`、`.DS_Store`（沿用 `COPY_TREE_IGNORE_NAMES`）；`.specify/skills/**/site/` 为调用方运行时数据，不比较。
- 项目自有面不比较：`.specify/memory/**`、`.specify/agents/instances|execution/**`、锚点文件、`tools.md`、`workflow/git.md`、`.specify/source.json`、`.specify/.gitignore`、用户自建技能。
- 参照树在 `tempfile.TemporaryDirectory` 中构建并清理；不写工作区。
- 降级事实：可判对象的降级（如平台无符号链接）以 `refuse` item 表达并阻止 clean；无可判对象的降级（如无工具命令目录）只记入计划与回执 `notes`（`command-copies: no tool surface detected`），MUST 可见，不得被静默当作「已检查且无差异」。

## C-5 复用边界（禁止第二实现）

| 能力 | 唯一 owner | migrate 的消费方式 | 结构守卫 |
|------|-----------|--------------------|----------|
| 资产投影（rewrite/命令生成） | `copy_local_templates` / `rewrite_paths` / `generate_commands` | 直接调用 | 源码检查：migrate 段内不得出现自写路径改写正则或第二套命令渲染 |
| 退役资产与平铺收敛的**决策** | `cleanup_obsolete_framework_assets` / `migrate_flat_internal_skills`（WP07 拆出纯决策函数，两入口共享） | 调用决策函数；执行策略由 migrate 的归档层承担 | 等价性测试：同一夹具上 init 与 migrate 的判定集合相同 |
| 残留/链接检查 | `sanitize-utils.py` 检查器 | 进程内导入调用 | 禁止 `--action collect`；禁止读写 `.specify/memory/sanitize/` |
| 锚点布局 | `anchor-layout-migrate.py` check/apply | CLI 动作调用 | 源码检查：无布局判定/移动实现 |
| 兼容链接修复 | 声明：`sanitize-utils.COMPAT_SYMLINKS` + `COMPAT_SYMLINK_EXPECTATIONS`（与 `shared/workflow/symlink-model.md` 同源）；目录级链接动作复用 `ensure_specify_symlink` | 指令文件链接按声明目标创建符号链接（无既有 Python 动作；`generate-instructions.sh` 的 `ln -sf` 集合与声明同源） | 链接名单与目标一律从 sanitize 声明导入；源码检查：migrate 段内不得出现第二份链接名单 |

链接修复的职责说明：`/speckit.sanitize` 对链接发现只给 `delegate`（修复交给 `/speckit.instructions`）；migrate 的职责是一次性收尾，按同一份声明直接创建/修复链接，不复制任何检查实现。二者是同一维度在不同职责下的两种消费，不构成第二套检查。
| 镜像与生成副本（框架源） | `sync-mirrors.py --check`、`regen-command-copies.py --check` | 探测：子进程只读；写：镜像对以计划项源路径为 `--only` 前缀调用 `--write`（未确认项不进入该批），命令副本由 `generate_commands` 写入各工具目录（与 init 同一生成器；`regen --check` 只作探测与回验） | 禁止第二份镜像对清单；镜像对从 `sync-mirrors.MIRROR_PAIRS` 导入 |
| goal/team 档案迁移 | `/speckit.goal` `migrate-archive` | 只输出 E-9 静止指针 | 计划/回执无该类 item；SC-007 测试 |
| 周期治理（保留期、pending 台账、重排） | `/speckit.sanitize` | 不消费、不写 | migrate 计划不含 dead-reference / index-inconsistency 维度 |

## C-6 安全与确认（引用 owner）

- 破坏性/不可逆动作的清单与判据：`.specify/shared/guidelines/confirmation-gates.md`（本契约不复述）。
- 双键：`--apply`（第一把）+ 交互终端一次单批确认（第二把）；无人值守行（该 owner 的矩阵）决定非交互时破坏项 `blocked`。
- `refuse` 不择一胜出；该 item 保留原状并在回执中指名两个候选（现状对象、期望对象）。
- 用户内容保护：替换/移除前必归档；用户自建技能、项目专属扩展、`site/` 数据永不入选。

## C-7 归档、回执、幂等与续跑

- 归档布局：`.specify/archive/migrate/<run-id>/<rel>`，`<rel>` 为对象相对工作区路径（剥离前导 `.specify/`），与 sanitize archive 布局同构。
- 回执：`.specify/memory/migrate/receipts/<run-id>.json`，逐运行一文一件；apply 开始时写 `status=running`，逐项更新 `items[].status` 与 `archives[]`，收束写 `completed`。两并发运行产生不同 `run-id` 路径（单元测试钉住）。
- 干跑回执只走输出流，零落盘。
- 幂等：apply 后重跑为 `clean` 且零写入。
- 续跑（承重）：启动时扫描本工作区回执，若存在 `status=running` 的最近回执，则报告中断阶段（计划 `notes` + 新回执 `resumedFrom`）。逐项判断以**该旧回执自己的记录**为准，绝不以新运行自己计算的路径推断：旧回执 `items[].status=done` 且目标已等于期望 → 记 `converged`；旧回执 `archives[]` 条目存在、其 `archiveTo`（搬迁类为 `to`）已存在而目标缺失 → 直接完成写入，不二次归档/搬迁；新归档只落新 run-id 且仅限旧回执未覆盖的项。
- 不提供全局回滚/undo；失败语义为前向续跑 + 逐项按 `recover` 找回（FR-017）。
- 框架源模式的执行细节：投影文件（`PROJECTED_FILES` 行）只经 `sync-mirrors.py --write` 写入（不得用裸拷贝覆盖 bridge/guard 块）；严格镜像对的孤儿先归档，再由 `--only` 限定批次确认其余项均已收敛；命令副本写完后以 `regen-command-copies.py --check` 回验退出 0。

## C-8 验收夹具（由声明生成，非历史快照）

- `build_latest_project`：以当前安装资产运行 init 复制机制生成「已最新」项目（含 `.specify/source.json`）。
- `build_legacy_project`：从「已最新」按**声明构造**旧态——把五个锚点移入 `.specify/memory/`（锚点维度）、为 `_OBSOLETE_SKILLS` 中若干名建立平铺技能目录（残留维度）、放入 `_OBSOLETE_COMMANDS` 的旧命令副本（模板与生成物维度）、复制一份内部技能为平铺重复（残留维度）、移除一个兼容链接（链接维度）、改写一份 `.specify/templates/` 文件与删除一份 `.specify/scripts/` 文件（前者归模板与生成物、后者归镜像维度），使五个维度至少各有一项。
- `build_mixed_project`：已最新 + 上述构造的子集（模拟「部分 init 后」）。
- 夹具构造只允许引用 R-2 钉名的声明与检查器认识的对象类；测试断言每个构造名都能在对应 owner 列表中找到（禁止命令内猜测清单）。
- 「最新」夹具在干跑/重跑均 `clean`；旧版与混杂夹具干跑 `planned`、应用后逐项零差异、再跑 `clean`。
