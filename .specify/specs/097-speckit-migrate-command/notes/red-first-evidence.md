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


## pkg03-us1-engine（T014–T022）

---
### § T014 + T015 — `tests/contract/test_migrate_cli_surface.py` + `tests/integration/test_migrate_us1_converge.py`（red-first）

- 日期: 2026-11-10
- 命令: `bash scripts/bash/run-tests.sh tests/contract/test_migrate_cli_surface.py tests/integration/test_migrate_us1_converge.py -q`
- 退出码: `1`（完整读数 `.specify/.tmp/pkg03/red-suite.txt`）
- 真实输出（决定性节选，逐字粘贴）:

```text
E       AttributeError: module 'specify_cli' has no attribute 'MIGRATE_OUTCOME_EXIT_CODES'
E       AttributeError: <module 'specify_cli' ...> has no attribute 'migrate_interactive_terminal'
E       AssertionError: exit 2, expected 1
E         │ No such command 'migrate'.                                   │
E       assert 'No such option' in "Usage: specify [OPTIONS] COMMAND [ARGS]......"
...
14 failed in 8.57s
```

- 红判据: 14 条失败全部为「被测行为尚不存在」——`specify migrate` 子命令未注册（框架以 “No such command 'migrate'” 退出 2）、结局映射常量与交互判定接缝不存在（AttributeError）；无一条来自断言自身缺陷。实现后同两文件全绿（`test-evidence/us1-converge.txt`）。

---

## pkg04-us2-safety（T023–T028）

---
### § T023 — `tests/integration/test_migrate_us2_safety.py`（red-first）

- 日期: 2026-11-10
- 命令: `bash scripts/bash/run-tests.sh tests/integration/test_migrate_us2_safety.py -q`
- 退出码: `1`（完整读数 `.specify/.tmp/pkg04/red-suite.txt`）
- 真实输出（决定性节选，逐字粘贴）:

```text
E       AttributeError: <module 'specify_cli' ...> has no attribute 'migrate_symlink_supported'   (×8, test-side probe monkeypatch)
E       AttributeError: module 'specify_cli' has no attribute 'migrate_symlink_supported'         (×1, zero-write probe call)
E       AttributeError: module 'specify_cli' has no attribute 'MIGRATE_DESTRUCTIVE_CRITERIA_POINTER' (×1, destructive classifier)
...
10 failed, 1 passed in 10.73s
```

- 红判据: 10 条失败全部为「被测行为尚不存在」——破坏性判据 owner 指针常量与
  `migrate_symlink_supported` 平台探测未实现（AttributeError），无一条来自断言自身缺陷。
  唯一通过项是 `test_mutation_weakening_to_existence_only_would_miss_content_corruption`
  （只消费 pkg03 已交付的比较面，不触碰新增接缝），符合预期。

---
### § T024–T027 — 安全层实现（green readings）

- 命令: `bash scripts/bash/run-tests.sh tests/integration/test_migrate_us2_safety.py -q`
- 退出码: `0` → `11 passed in 13.78s`（`test-evidence/us2-safety.txt`）
- 实现落点: `MIGRATE_DESTRUCTIVE_CRITERIA_POINTER` + `migrate_is_destructive()`（owner 指针
  `.specify/shared/guidelines/confirmation-gates.md`，双键两条路径统一经该判据）；
  `migrate_symlink_supported()` 零写入探测 + `make_platform_refuse_item()`（compat-links
  规划期接入，`platform-no-symlink` 原因）；归档/恢复枚举与用户内容保护沿用 pkg03 执行器，
  由本包套件逐项实测（9/9 归档存在且摘要一致；用户文件逐字节不变）。

---
### § 相邻套件回归（pkg04 实现后）

- 命令: `bash scripts/bash/run-tests.sh tests/contract/test_migrate_engine_contract.py tests/contract/test_migrate_cli_surface.py tests/integration/test_migrate_us1_converge.py tests/unit/test_migrate_planner.py tests/unit/test_migrate_receipts.py -q`
- 退出码: `0` → `47 passed in 22.00s`（`.specify/.tmp/pkg04/regression.txt`）
- 引擎契约的五类源码守卫在本包新增代码上保持 clean（owner 指针不是第二份清单）。

---

## pkg05-us3-crossversion（T029–T032）

---
### § T029 — `tests/integration/test_migrate_us3_crossversion.py`（red-first）

- 日期: 2026-11-10
- 命令: `bash scripts/bash/run-tests.sh tests/integration/test_migrate_us3_crossversion.py -q`
- 退出码: `1`（完整读数 `.specify/.tmp/pkg05/red-suite.txt`）
- 真实输出（决定性节选，逐字粘贴）:

```text
E       KeyError: 'stampFile'
E       KeyError: 'stampFile'
E       AttributeError: <module 'specify_cli' ...> has no attribute '_migrate_resume_complete_write'
E       AssertionError: the resumed run must name the interrupted receipt it continued from
E       assert None == '20261110T145903Z-a964a807'
...
4 failed, 1 passed in 19.86s
```

- 红判据: 4 条失败全部为「被测行为尚不存在」——回执 `source` / `target` 记录仍是占位
  `{}`（KeyError `stampFile`，T030 未实现）、中断续跑路径未实现（`resumedFrom` 仍为
  None；续跑完成接缝 `_migrate_resume_complete_write` 不存在，AttributeError），无一条
  来自断言自身缺陷。唯一通过项是
  `test_mutation_selecting_paths_by_source_version_turns_plan_identity_red`
  （只消费 pkg03 已交付的计划面，不触碰新增接缝），符合预期。

---
### § T030–T031 — 版本记录与续跑实现（green readings）

- 命令: `bash scripts/bash/run-tests.sh tests/integration/test_migrate_us3_crossversion.py -q`
- 退出码: `0` → 见 `test-evidence/us3-crossversion.txt`（T032 读数）
- 实现落点: `migrate_source_record()` / `migrate_target_record()` /
  `migrate_cli_version()`（回执 source/target 字段，record-only，FR-020）；
  `load_migrate_resume_state()`（扫描最近 `status=running` 回执）+
  `migrate_resume_archive_entry()` / `_migrate_resume_complete_write()`
  （按旧回执自身 `archives[].archiveTo` 判断，目标缺失则只补写、不二次搬移，C-7）。

---

## pkg06-us4-template（T033–T040）

---
### § T033 + T034 — `tests/contract/test_migrate_template.py` + `tests/integration/test_migrate_us4_equivalence.py`（red-first）

- 日期: 2026-11-10
- 命令: `bash scripts/bash/run-tests.sh tests/contract/test_migrate_template.py tests/integration/test_migrate_us4_equivalence.py -q --names-out .specify/.tmp/pkg06-red-us4-names.txt`
- 退出码: `1`（失败名清单 `.specify/.tmp/pkg06-red-us4-names.txt`，12 条）
- 真实输出（决定性节选，逐字粘贴）:

```text
E       AssertionError: templates/commands/migrate.md is missing — T035 authors the projection
E       AssertionError: templates/commands/migrate.md is missing — the template entry has no declared commands to run (T035 authors it)
...
FAILED tests/contract/test_migrate_template.py::test_frontmatter_carries_exactly_two_keys
FAILED tests/contract/test_migrate_template.py::test_required_sections_are_present_as_headings
FAILED tests/contract/test_migrate_template.py::test_template_declares_the_two_delegated_commands
FAILED tests/contract/test_migrate_template.py::test_template_carries_no_implementation_symbol
FAILED tests/contract/test_migrate_template.py::test_template_has_no_inspection_code_fence
FAILED tests/contract/test_migrate_template.py::test_template_passes_no_confirmation_class_flag
FAILED tests/contract/test_migrate_template.py::test_outcome_and_exit_code_table_is_restated_verbatim
FAILED tests/contract/test_migrate_template.py::test_receipt_and_archive_pointers_are_named
FAILED tests/contract/test_migrate_template.py::test_boundary_names_the_init_repair_entry
FAILED tests/integration/test_migrate_us4_equivalence.py::test_template_dry_run_matches_the_direct_cli_plan
FAILED tests/integration/test_migrate_us4_equivalence.py::test_template_apply_matches_the_direct_cli_result
FAILED tests/integration/test_migrate_us4_equivalence.py::test_mutation_template_inlining_an_inspection_command_turns_equivalence_red
12 failed, 1 passed in 10.99s
```

- 红判据: 12 条失败全部为「被测载体尚不存在」——`templates/commands/migrate.md`
  缺失，契约断言在 `_read_template()` / `_template_text()` 的前置断言上失败，等价性
  断言在「无声明命令可执行」上失败，无一条来自断言自身缺陷。唯一通过项是
  `test_qoder_frontmatter_is_covered_by_the_generic_contract`（只钉通用契约测试存在，
  不触碰新模板），符合预期。T035 落地后同一命令转绿（读数见
  `test-evidence/us4-equivalence.txt`）。

---
