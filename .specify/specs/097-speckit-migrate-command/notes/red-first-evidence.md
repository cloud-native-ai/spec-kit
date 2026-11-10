# Red-First Evidence — 097 /speckit.migrate 一次性迁移收尾命令

红先取证纪律（tasks.md § Tests / owner `.specify/skills/internal/implement-feature/SKILL.md` § TDD 与 § Test runs）：每条新测试先在被测行为实现前运行，并记录**命令、真实输出、退出码**。本文件 append-only，按任务行（T-row）分节追加，先红后续绿。

**落点所有者**: `.specify/specs/097-speckit-migrate-command/tasks.md` § Path Conventions（运行时证据落点固定：本文件 + `notes/quickstart-run.md` + `notes/pre-change-measurements.md` + `test-evidence/` + `coverage-baseline.txt`）。

- canonical runner（唯一测试入口）: `bash scripts/bash/run-tests.sh <targets> -q`
- 多测试文件整行 run 时允许 `-q` 尾随；单测调试同样经 runner 转发
- 迁移/回归例外（tasks.md § Tests）: 本特性无「移植既有行为」的测试行，全部测试行为新，无 `[blockedBy:]` 后置的迁移型测试
- template-only gate（tasks.md § Tests）: `templates/commands/migrate.md` 与其四个副本的断言是结构契约测试，仍按红先纪律执行

## 记录骨架（每条红一行，逐条追加）

---
### § <T-row> — `<test-file>`（red-first）

- 日期: `<YYYY-MM-DD>`
- 命令: `bash scripts/bash/run-tests.sh <targets> -q`
- 退出码: `<n>`
- 真实输出（尾部/决定性节选，逐字粘贴）:

```text
<verbatim output>
```

- 红判据: <该失败为何证明被测行为尚不存在（而非断言自身缺陷）>

---
（以下由后续包逐行追加）

## pkg02-foundation（T005–T013）

---
### § T005 + T006 — `tests/unit/test_migrate_planner.py` + `tests/unit/test_migrate_receipts.py`（red-first）

- 日期: 2026-11-10
- 命令: `bash scripts/bash/run-tests.sh tests/unit/test_migrate_planner.py tests/unit/test_migrate_receipts.py -q`
- 退出码: `1`（同一命令在 pristine `HEAD` 源上重放实测；完整读数 `.specify/.tmp/pkg02-red-unit.txt`）
- 真实输出（决定性节选，逐字粘贴）:

```text
E       ImportError: cannot import name 'MIGRATE_DIMENSIONS' from 'specify_cli' (...)
E       ImportError: cannot import name 'MigratePlan' from 'specify_cli' (...)
FAILED tests/unit/test_migrate_receipts.py::test_run_id_shape_and_uniqueness
...
18 failed in 6.16s
```

- 红判据: 18 条失败全部为 `ImportError`（被测的差异模型与回执存储尚不存在），无一条来自断言自身缺陷；模型实现后同两文件全绿（`test-evidence/pkg02-foundation-suite.txt` 的 46-passed 合并读数）。

---
### § T007 — `tests/fixtures/migrate-097/builders.py`（fixture 构建 smoke）

- 日期: 2026-11-10
- 命令: importlib 加载 builders，于 `.specify/.tmp/migrate-fixture-probe/` 逐类构建（结束即删）
- 退出码: `0`
- 真实输出: `latest ok 2.2s` / `legacy ok 2.3s` / `mixed ok 2.2s` / `counts: 1161`
- 说明: 每个构造名在构建时对 owner 声明与 checker 输出双重断言——`anchor_engine.ANCHORS`、`_OBSOLETE_SKILLS`、`_OBSOLETE_COMMANDS`、`_FRAMEWORK_INTERNAL_SKILLS`、`COMPAT_SYMLINKS`，以及 `check_legacy_install_residue` / `check_flat_internal_duplicates` / `check_broken_symlinks` 的实际发现输出；任一断言失败即构建失败（FR-023）。

---
### § T008–T012 — model / receipt / workspace-kind / reference tree / 决策函数（green readings）

- 命令: `bash scripts/bash/run-tests.sh tests/unit/test_migrate_planner.py tests/unit/test_migrate_receipts.py tests/contract/test_migrate_engine_contract.py tests/contract/test_cleanup_obsolete_assets.py tests/contract/test_flat_internal_skill_migration.py tests/contract/test_upgrade_end_state.py -q`
- 退出码: `0` — `46 passed in 8.59s`（`test-evidence/pkg02-foundation-suite.txt`）
- init 等价回归: `test_cleanup_obsolete_assets` / `test_flat_internal_skill_migration` / `test_upgrade_end_state` 全绿——T012 的决策函数抽取与 init 调用点改线未改变 init 行为；`tracker=None` 路径保持。

---
### § T013 — `tests/contract/test_migrate_engine_contract.py`（red-first → green）

- 日期: 2026-11-10
- 红 #1（模型已就位、`MIGRATE-ENGINE` 钉住段未加）: `bash scripts/bash/run-tests.sh tests/contract/test_migrate_engine_contract.py -q` → 退出码 `1`，`7 failed, 8 passed`；7 条失败全部为 `expected exactly one MIGRATE-ENGINE:START/END pinned segment`（段缺失），同时 5 条注入变异守卫与 E-8/FR-014 域断言、init↔migrate 等价性均已通过。
- 红 #2（pristine `HEAD` 源重放同一命令）: 退出码 `1`，`10 failed, 5 passed`（模型常量与决策函数缺失额外压红域断言与等价性）。
- 处置: 依红读数在 `src/specify_cli/__init__.py` 的 migrate 段两侧加 `MIGRATE-ENGINE:START/END`，使契约测试钉住非空迁移段。
- 绿: 同命令退出码 `0` → `15 passed in 8.47s`（`test-evidence/pkg02-engine-contract.txt`）。
- 判别力: 五类源码守卫在真实段上判 clean、各自对测试内合成的第二实现判违例（同一套件运行内完成，DoD-3）。

---
### § 包级回归归因（全量套件，pkg02）

- 命令: `bash scripts/bash/run-tests.sh --names-out .specify/specs/097-speckit-migrate-command/test-evidence/pkg02-full-failed.txt -q`
- 读数: 退出码 `1`；失败名 `277` 条（`test-evidence/pkg02-full-failed.txt`）；相对入口基线 278 名：新增 `4`、翻转绿 `5`。
- 归因（完整控制组见 `test-evidence/pkg02-baseline-attribution.txt`）: 4 条新增全部位于 `test_trigger_engine.py`（入口基线已含 59 条该家族红；同源连续两次运行失败集合不同，29 vs 31 名）；pristine `HEAD` 源同树重跑与实现后重跑的名单差全在 trigger 家族内；唯一非 trigger 的临时红（`test_script_interface_contract.py::test_c20…`）根因是 4 个新文件尚未入 git index，staged 后转绿（`test-evidence/pkg02-c20-post-stage.txt`）。pkg02 未引入任何可归因的新失败。

