# Phase 0 Research Review — /speckit.migrate 一次性迁移收尾命令

**Spec**: `.specify/specs/097-speckit-migrate-command/requirements.md`
**Date**: 2026-11-10
**Scope**: 为 plan 提供可引用的既有事实读数；不含新设计，只固化「入口形态、期望态来源、可复用引擎与装配面」的调查结论。

## R-1 入口形态调查（A2 落地的仓库事实）

现行 `specify` CLI 只有三个子命令，没有任何 migrate/upgrade 面：

- `app = typer.Typer(...)`（`src/specify_cli/__init__.py:2785-2791`，`invoke_without_command=True`，`cls=BannerGroup`）。
- `@app.command()` 模块级函数：`init`（:2990-2991）、`check`（:3330-3331）、`render_agents`（:3373-3380）；`main()` 只调用 `app()`（:3409-3410）。
- 新增子命令的既定形态：模块级 `def <name>(...)` + `@app.command()`；Typer 由函数名推导命令名（`render_agents` → `render-agents`）。

既有「干跑/应用」安全默认先例（requirements A2 引用的证据面）：

- `goal-utils.py migrate-archive`：`--dry-run|--apply` 互斥且必填（`scripts/python/goal-utils.py:2729-2738`）；两种模式共享同一计划（:2050-2056）；冲突在写入前拒绝（:2058-2066）；中断应用退出 3（:2534-2536）。
- `sanitize-utils.py apply`：要求计划 `confirmed: true`（:959-989），可执行处置封闭集 `{delete, archive, repair, dismiss}`（:956）；退出码 0 ok / 1 CliError / 2 VerificationError（:1110-1118）。
- `anchor-layout-migrate.py`：`--action {check,apply}`（:109-112），check 有发现退出 1、apply 成功 0、参数/环境错误 2（:9-17、:125、:139）。

结论（与 requirements A2 一致，不再另择）：`specify migrate` 是唯一确定性可执行体；`/speckit.migrate` 模板是驱动同一 CLI 的薄投影。用户三步流程处于 CLI 上下文。

## R-2 期望态读取入口逐项核实（FR-005）

| 维度 | 既有 owner | 位置 | 只读性 |
|------|-----------|------|--------|
| 退役资产清单 | `OBSOLETE-ASSET-REGISTRY` 标记块 | `src/specify_cli/__init__.py:851-973`（`_OBSOLETE_SKILLS` 34 名、`_OBSOLETE_SKILL_FILES` 16 项、`_OBSOLETE_COMMANDS` 4 个 stem、`_OBSOLETE_TEMPLATES` 27 项）；`sanitize-utils.py:609-644` 为受漂移测试钉住的镜像 | 纯常量，只读 |
| 迁移残留 | `check_legacy_install_residue` | `scripts/python/sanitize-utils.py:659`（legacy flat skills / 旧 git-workflow 状态文件 / `.specify/tools`） | 纯函数，`root: Path -> list[dict]` |
| 平铺内部技能重复 | `check_flat_internal_duplicates` | `sanitize-utils.py:711` | 纯函数，完全可推导（无名单） |
| 兼容链接 | `check_broken_symlinks` | `sanitize-utils.py:512`；声明 `COMPAT_SYMLINKS` :75-79、`COMPAT_SYMLINK_EXPECTATIONS` :82-90 | 纯函数；修复动作指向 `/speckit.instructions`（findings.disposition=`delegate`） |
| 镜像漂移 | `check_mirror_drift` → `run_sync_mirrors_check` | `sanitize-utils.py:738`、:533-549；后者仅在 `root == script_repo` 时运行（客户端项目自动跳过） | 子进程 `--check`，从不写入 |
| 锚点布局 | `anchor-layout-migrate.py plan/apply` | `scripts/python/anchor-layout-migrate.py:64-101`；`main(argv=None)` :104 | check 只读；apply 仅 `os.replace` 重命名、拒绝覆盖、从不删除 |
| 生成副本 | `regen-command-copies.py --check` | `scripts/python/regen-command-copies.py:103-132`；漂移 exit 1 | `--check` 不写入（临时目录再 diff） |
| 镜像一致性 | `sync-mirrors.py --check` | `scripts/python/sync-mirrors.py`：`MIRROR_PAIRS` :93-100、`--check` :690、漂移/孤儿 exit 2、从不写入 | 只读 |
| 框架资产刷新/退役 | `cleanup_obsolete_framework_assets`、`migrate_flat_internal_skills` | `src/specify_cli/__init__.py:2011-2015`、:2097-2100；init 调用点 :2494、:2638 | 模块级可导入；`tracker=None` 允许 |

`sanitize-utils.py` 的发现项形态（`_finding`, :300-314）：`id`（sha1(category|target)[:12]）、`category`、`target`、`severity`、`summary`、`evidenceRefs`、`detection`、`disposition`、`reversibility`、`state`。检查器全部可进程内导入（先例：`tests/script_api.py:18-33` 按路径装载 `sanitize_utils`；`sanitize-utils.py:755-768` 同样装载 `docs-utils.py`）。`--action collect` 会写 `.specify/memory/sanitize/findings.json` 台账（:49、:904），因此按 FR-010 只能导入检查器，不能以 collect 作为计划输入。

## R-3 init 的复制语义（期望态投影的唯一机制）

`copy_local_templates`（`src/specify_cli/__init__.py:2229` 起）的执行顺序与合并策略：

1. memory：锚点 `constitution.md`、`features.md` 复制到 `.specify/` 根（:2256-2289），其余子目录逐文件 create-only（:2290-2311）。
2. `scripts/` → `.specify/scripts/`，`copy_tree_with_rewrite`（:2313-2321）。
3. `templates/`（排除 `commands/`）→ `.specify/templates/`（:2323-2338）；`tools.md`、`workflow/git.md` create-only 种子（:2340-2357）。
4. 命令副本：`generate_commands` 按所选 assistant 生成到各工具目录（:2359-2414）；未知工具回退 `.specify/templates/commands`。
5. `migrate_flat_internal_skills` 在技能复制**之前**运行（:2482-2495，顺序是承重的）。
6. `skills/external/*` 平铺、`skills/internal/*` 嵌套复制，均经 `copy_tree_with_rewrite`（:2497-2517）。
7. `agents/` → `.specify/agents/templates/`（`ensure_agent_layer_dirs`，:2519-2540）；`shared/` → `.specify/shared/`（:2542-2551）。
8. 所选 assistant 的 `<tool>/skills` 目录级符号链接（`ensure_specify_symlink`，:1914-1944；:2553-2617）。
9. 可渲染工具的 agent 分发（:2619-2652）。
10. `cleanup_obsolete_framework_assets` 最后执行（:2654-2638 区块）。

投影函数：`rewrite_paths(content)`（:1554-1598）把 source 形态路径改写为 `.specify/` 运行时形态。**实测**（2026-11-10，本 worktree）：对 `skills/external/database-utils/SKILL.md`、`skills/internal/memory-record/SKILL.md`、`shared/definitions/framework-map.md`、`scripts/python/sanitize-utils.py` 调用 `rewrite_paths` 均产生非零 delta；而仓库内 `.specify/` 镜像与 source 逐字节相同（`diff -q` 全部无输出）。

结论：**客户端项目的期望态是 init 投影形态（rewrite 形态），不是 sync-mirrors 的字节形态**。本仓自身的 `.specify/` 由 sync-mirrors 以字节形态维护。二者语义不同，migrate 必须以工作区形态区分（见 plan T-002），不得用单一比较器套两层语义。

## R-4 装配面与分发基线（FR-021）

- 源模板：`templates/commands/*.md`，实测 **29** 个；frontmatter 仅 `description` + `short-description`（`templates/commands/sanitize.md:1-4`）。副本由 `generate_commands` 生成（:1599 起）：剥离 frontmatter、注入 `AUTO-GENERATED` 标记、Qoder 由 `short-description` 生成 `description`（:821-824，契约测试 `tests/contract/test_qoder_command_frontmatter.py`）。
- 四个运行期副本树（实测各 29 份）：`.github/prompts/*.prompt.md`、`.claude/commands/speckit.*.md`、`.qoder/commands/speckit.*.md`、`.opencode/command/speckit.*.md`。`regen-command-copies.py` 按 `_ASSISTANT_COMMAND_DIRS`/`_ASSISTANT_EXTENSIONS`（`__init__.py:802-819`）只处理已存在的目录。
- 命令文档：`docs/reference/commands/*.md` 实测 **27** 个（无索引文件；`tests/contract/test_goal_targets_engine.py:330-334` 钉住「无嵌套 README」惯例）。
- 冻结名单基线：`tests/contract/test_migration_distribution.py` `COMMAND_BASELINE`（:98-106）与 `assert len(COMMAND_BASELINE) == 29`（:127）——新增命令须同步改为 30。
- `.specify/templates/commands/` 已退役：templates 镜像对排除 `commands`（`sync-mirrors.py:93-100`），命令副本只经 regen 分发。

## R-5 回执的版本字段（FR-020、SC-004）

- `specify init` 每次调用 `write_source_stamp(project_path)`（`__init__.py:3257`），写 `<project>/.specify/source.json` = `{framework, commit, stamped_at}`；不可得时 `commit="unavailable"` + `reason`（:606-631，043 契约 `source-stamp-write`）。
- 目标版本：已安装 CLI 自身的版本与来源 commit（`importlib.metadata.version("specify-cli")` 与 `resolve_source_commit()`，:600-603）。
- 旧项目可能早于 043 而没有 `.specify/source.json`：回执的 source 字段必须允许缺席（记录 `unavailable` 与原因），且按 FR-020 只作记录、不参与任何处置判定。

## R-6 打包与资源定位（期望态取「当前已安装版本」）

- wheel `force-include`：`scripts/`、`templates/`、`shared/`、`agents/`、`memory/` → `specify_cli/<name>`；`skills/` 由 `src/hatch_build.py` 暂存复制（剥离 `site` 组件）后注入（`pyproject.toml:47-56`、`src/hatch_build.py:1-40`）。
- `get_resource_path()`（`__init__.py:1512-1570`）：先 `MODULE_DIR/templates`，否则开发检出回退（受 `src/specify_cli/__init__.py` 存在性门控）。
- **检查引擎的装载点随工作区形态不同（重要）**：
  - 客户端工作区：`sanitize-utils.py` 与 `anchor-layout-migrate.py` 取自 `get_resource_path()/scripts/python/`（= 当前已安装版本），因为工作区自己的 `.specify/scripts/` 可能正是待收敛的旧副本。
  - 框架源工作区：取自工作区自身的 `.specify/scripts/python/` 副本。`sanitize-utils.run_sync_mirrors_check` 只在 `root == script_repo` 时执行（R-2），而脚本按自身位置解仓根（`.specify` 目录名有防护，`sync-mirrors.py:63-68`）；只有工作区副本能命中这一条件。此处工作区副本由 sync-mirrors 维护、与本仓 `scripts/` 同步，不存在「旧副本」问题。
- 由此得到一个关键性质：框架仓模式与客户端模式的检查行为可按工作区形态确定，不需要 migrate 自己猜脚本位置。

## R-7 目录与长期状态

- `.specify/memory/` 子目录登记在 `shared/definitions/framework-map.md` 的 Project memory 行（:9），镜像 `.specify/shared/definitions/framework-map.md` 由 sync-mirrors 维护；登记义务见 `shared/guidelines/directory-governance.md` §3。
- 已有归档布局先例：`.specify/archive/spec/`（sanitize archive-spec）、`.specify/archive/goal-team/`（`goal migrate-archive` 的 `receipts/` + `trees/`）。migrate 的归档沿用 `.specify/archive/` 家族。
- 回执落点按 FR-018 定名 `.specify/memory/migrate/receipts/`；逐运行一文一件（并发开发安全纪律）。

## R-8 基线读数（2026-11-10，本 worktree，可供 Mirror Obligations 的 NO-NEW-DRIFT 判据引用）

- `python3 scripts/python/regen-command-copies.py --check` → exit 0，`OK: all per-tool command copies match the source templates.`
- `python3 scripts/python/sync-mirrors.py --check` → exit 0，末行 `ok    shared/ == .specify/shared/ (111 files, byte-identical)`，投影行全部 `ok`。
- `python3 scripts/python/anchor-layout-migrate.py --help` → exit 0（`--action {check,apply}`、`--workspace`、`--json`、`--version`）。
- `specify --help` → 子命令仅 `init` / `check` / `render-agents`。

## R-9 交给 plan 的设计结论

1. **期望态构建**：客户端模式以「运行 init 的同一复制机制到临时参照树、再逐文件对照」为唯一投影；不逐文件重写比较（T-001）。
2. **双工作区语义**：框架源工作区（`skills/external/` 存在，与 sanitize 既有 guard 同源）委托 `sync-mirrors.py --check` 与 `regen-command-copies.py --check`；客户端模式用参照树对照（T-002）。
3. **处置与安全**：差异项映射进 FR-014 六值封闭集；移动（锚点、平铺内部技能）归 `archive`（可找回的搬迁），有别处既有目标的归 `refuse`；未确认破坏桶归 `blocked`。
4. **回执**：apply 落盘 `.specify/memory/migrate/receipts/<run-id>.json`；dry-run 为零写入，回执体随 stdout/`--format json` 输出。
5. **归档**：`.specify/archive/migrate/<run-id>/<相对路径>`。
6. **无遗留 NEEDS CLARIFICATION**。
