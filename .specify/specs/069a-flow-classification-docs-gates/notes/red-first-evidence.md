# Red-first evidence — 069a US1 测试先行段（T004 / T005 / T006）

**Feature**: 069a-flow-classification-docs-gates（父 069） | **Scope**: US1 的三支新增测试
**Discipline**: Constitution IV / `tasks.md` § Tests Mode ON — 测试先落盘，实现（T007–T011）尚不存在；
红必须是「实现缺失 / 行为不符」，不是测试自身的 import、语法或采集错误。
**Captured**: 2026-10-24T13:37:04Z（+0800 21:37）；测试内容最终版复跑同结果（3 次，36 failed / 3 passed，0.72–0.73s，node id 完全一致）
**Branch**: `069-execution-expression-sdd` | **HEAD**: `f0b8eaedb39c93a0b9360c9d8193bbb592d20b4a`
**Interpreter**: `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`（pytest 9.1.1；本仓 `.venv` 无 pytest，实测 `No module named pytest`）

## 1. 命令、输出摘要与退出码

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
  tests/contract/test_flow_class_ledger.py \
  tests/contract/test_flow_class_correctness.py \
  tests/unit/test_flow_class_check.py \
  -q --tb=short -p no:cacheprovider
# exit code: 1
# 36 failed, 3 passed in 0.72s（复跑 0.72–0.73s，失败 node id 完全一致）
```

采集面自检（同一解释器、同一树）：

```text
pytest <三文件> --collect-only -q  →  39 tests collected in 0.10s (exit 0)
python -m py_compile <三文件>       →  COMPILE-OK (exit 0)
```

结论：三支测试可被正常采集与编译；36 条失败全部是断言级失败（见 §2），不存在 collection error、
import error 或测试自身语法错误。

## 2. 红的原因（两族，均为「目标产物缺失」）

| 断言族 | 触发点 | 失败次数 | 交付行 |
|--------|--------|----------|--------|
| owner missing | `_read_owner()` → `shared/definitions/flow-class-definitions.md` 不存在 | 6 | T007 / T008 |
| engine missing | `_run()` → `scripts/python/flow-class-check.py` 不存在 | 30 | T009 / T010 |
| **合计** | | **36** | 与 `36 failed` 一致，无第三种失败原因 |

真实输出（首条 owner 族，逐字）：

```text
E   AssertionError: flow-class owner missing: shared/definitions/flow-class-definitions.md — expected at T007/T008 (069a). Red is the intended pre-implementation state for T004.
E   assert False
E    +  where False = is_file()
```

真实输出（engine 族，逐字）：

```text
E   AssertionError: flow-class engine missing: scripts/python/flow-class-check.py — expected at T009/T010 (069a). Red is the intended pre-implementation state for T006.
E   assert False
```

两族都由 `_read_owner()` / `_run()` 的显式存在性前置断言产生：引擎与 owner 缺席时测试以可读断言停下，
不会退化成 `FileNotFoundError` 或 collection crash。

## 3. 逐文件失败 node id（36 条，逐行一个）

### `tests/contract/test_flow_class_ledger.py` — 9 failed / 2 passed

```text
tests/contract/test_flow_class_ledger.py::test_owner_exists_and_declares_required_sections
tests/contract/test_flow_class_ledger.py::test_ledger_has_78_rows_covering_inventory_bidirectionally
tests/contract/test_flow_class_ledger.py::test_ledger_values_are_binary_and_basis_is_closed
tests/contract/test_flow_class_ledger.py::test_first_batch_members_are_registered_as_expression
tests/contract/test_flow_class_ledger.py::test_check_reports_78_units_and_zero_gaps
tests/contract/test_flow_class_ledger.py::test_lookup_unregistered_unit_returns_default_with_marker
tests/contract/test_flow_class_ledger.py::test_lookup_registered_unit_returns_ledger_source_without_marker
tests/contract/test_flow_class_ledger.py::test_neutral_list_is_closed_against_ledger
tests/contract/test_flow_class_ledger.py::test_change_log_row_form
```

### `tests/contract/test_flow_class_correctness.py` — 3 failed / 1 passed

```text
tests/contract/test_flow_class_correctness.py::test_lookup_matches_independent_oracle
tests/contract/test_flow_class_correctness.py::test_mutating_one_class_turns_the_same_comparison_red
tests/contract/test_flow_class_correctness.py::test_source_and_marker_invariants_hold_for_every_unit
```

### `tests/unit/test_flow_class_check.py` — 24 failed / 0 passed

```text
tests/unit/test_flow_class_check.py::test_clean_full_fixture_exits_0_with_no_findings
tests/unit/test_flow_class_check.py::test_missing_ledger_row_reports_missing
tests/unit/test_flow_class_check.py::test_ledger_row_absent_from_inventory_reports_unknown
tests/unit/test_flow_class_check.py::test_repeated_row_reports_duplicate
tests/unit/test_flow_class_check.py::test_opposite_values_report_dual_class
tests/unit/test_flow_class_check.py::test_out_of_domain_value_reports_invalid_class
tests/unit/test_flow_class_check.py::test_row_with_wrong_cell_count_reports_row_malformed
tests/unit/test_flow_class_check.py::test_row_with_empty_required_value_reports_row_malformed
tests/unit/test_flow_class_check.py::test_non_canonical_unit_ids_report_row_malformed
tests/unit/test_flow_class_check.py::test_neutral_flag_outside_closed_list_reports_neutral_unlisted
tests/unit/test_flow_class_check.py::test_inventory_truncated_below_command_floor
tests/unit/test_flow_class_check.py::test_inventory_truncated_below_skill_floor
tests/unit/test_flow_class_check.py::test_repo_without_skills_directory_is_not_silently_green
tests/unit/test_flow_class_check.py::test_repo_with_empty_skills_directory_is_not_silently_green
tests/unit/test_flow_class_check.py::test_exit_code_ladder
tests/unit/test_flow_class_check.py::test_check_exit_2_when_owner_missing
tests/unit/test_flow_class_check.py::test_check_exit_2_when_ledger_header_missing
tests/unit/test_flow_class_check.py::test_parser_reads_columns_by_header_and_does_not_guess
tests/unit/test_flow_class_check.py::test_unit_ids_are_normalised_to_the_two_canonical_forms
tests/unit/test_flow_class_check.py::test_lookup_unregistered_keeps_the_marker_non_empty
tests/unit/test_flow_class_check.py::test_lookup_owner_missing_keeps_default_semantics
tests/unit/test_flow_class_check.py::test_lookup_owner_without_ledger_table_keeps_default_semantics
tests/unit/test_flow_class_check.py::test_default_marker_and_owner_degradation_label_are_mutually_exclusive
tests/unit/test_flow_class_check.py::test_check_and_lookup_are_read_only
```

## 4. 实现前即通过的 3 支（负向守卫，不是「已实现」）

| 测试 | 现在为何通过 | 实现后仍须保持 |
|------|--------------|----------------|
| `test_flow_class_ledger.py::test_no_second_classification_data_file` | 当前仓库确实不存在第二份 `unit → class` 数据（Markdown 台账行 / YAML·JSON 数据 / 代码常量三形态均为零命中） | T007/T008 落地后仍只允许 owner 一处；任何侧车数据文件出现即转红 |
| `test_flow_class_ledger.py::test_templates_and_skills_never_assign_class_key` | 78 个模板/技能当前零 `flow_class` 键赋值、零台账样式行 | W1–W4 接线只能写 lookup 与 owner 指针，不能内联类别 |
| `test_flow_class_correctness.py::test_fixture_matrix_is_not_vacuous` | 只检查测试内 oracle 矩阵（≥10 单元 / 两类各 ≥3 / 未注册 ≥1 / 类中立 ≥1 / mixed ≥1）与夹具自洽，不触达引擎 | 作为「这条测试本身不空真」的自检长期保留 |

## 5. 三支测试钉住的断言面（与任务原文逐项对应）

| 任务断言面 | 落点（node id 摘要） |
|-----------|----------------------|
| 台账 78 行、逐行两值之一、列头逐字 `flow_class` | `test_ledger_has_78_rows_covering_inventory_bidirectionally`、`test_ledger_values_are_binary_and_basis_is_closed` |
| 台账 ↔ 清单双向相等（27 命令 + 51 技能）、零重复 | `test_ledger_has_78_rows_covering_inventory_bidirectionally` |
| `/speckit.docs` 与 `/speckit.humanize` 为表达类首批成员 | `test_first_batch_members_are_registered_as_expression` |
| 未登记单元 → 默认类 + `[[STR-004]]` 标记 + `source=default`（不得呈现为已判定） | `test_lookup_unregistered_unit_returns_default_with_marker`、`test_lookup_registered_unit_returns_ledger_source_without_marker`、`test_lookup_unregistered_keeps_the_marker_non_empty` |
| 仓库内零第二份分类数据（表格 / YAML / JSON / 代码常量） | `test_no_second_classification_data_file` |
| 类中立清单封闭（枚举 + rationale + 与 `neutral: yes` 互为子集） | `test_neutral_list_is_closed_against_ledger` |
| § 变更记录 行形态 `date \| unit_id \| before → after \| basis \| 依据` | `test_change_log_row_form` |
| `templates/commands/**` 与 `skills/**/SKILL.md` 零类别键赋值 | `test_templates_and_skills_never_assign_class_key` |
| 正确性 fixture ≥10 单元（两类各 ≥3 / 未声明 / 类中立 / 混合 oracle） | `test_fixture_matrix_is_not_vacuous`、`test_lookup_matches_independent_oracle` |
| 变异断言（改错一类 → 比对转红；改回 → 回绿） | `test_mutating_one_class_turns_the_same_comparison_red` |
| 解析器八类 finding 各自独立 | `test_missing…` / `test_ledger_row_absent…unknown` / `test_repeated_row…duplicate` / `test_opposite_values…dual_class` / `test_out_of_domain…invalid_class` / `test_row_with_wrong_cell_count…` + `test_row_with_empty_required_value…` + `test_non_canonical_unit_ids…row_malformed` / `test_neutral_flag_outside…neutral_unlisted` / `test_inventory_truncated_…` ×2 |
| 单元 id 归一化（`/speckit.<stem>` / `skill:<dir>`） | `test_unit_ids_are_normalised_to_the_two_canonical_forms` + 干净夹具的 `units=78` |
| 反空真下限（命令 27 / 技能 51）与客户树形态 | `test_inventory_truncated_below_command_floor`、`…below_skill_floor`、`test_repo_without_skills_directory_is_not_silently_green`、`test_repo_with_empty_skills_directory_is_not_silently_green` |
| 退出码阶梯（check 0/1/2、lookup 0/2） | `test_exit_code_ladder`、`test_check_exit_2_when_owner_missing`、`test_check_exit_2_when_ledger_header_missing` |
| `lookup` 降级分支与两标签互斥（FR-016） | `test_lookup_owner_missing_keeps_default_semantics`、`test_lookup_owner_without_ledger_table_keeps_default_semantics`、`test_default_marker_and_owner_degradation_label_are_mutually_exclusive` |
| 只读（不写任何文件） | `test_check_and_lookup_are_read_only` |

## 6. 实现期必须知道的三处边界裁定（测试即规格）

1. **降级标签的两个名字**：契约 C-7 写 `owner-unparsable`，data-model E9 写 `owner-unavailable`。
   两支降级测试接受**任一**标签（`any(label in stderr for label in (...))`）；承重断言是
   `exit 2` + 默认类语义 + `marker=null`，以及它与「未登记 → `marker=[[STR-004]]`」互斥。
   这是本阶段发现的产物间措辞分歧，未改任何规格文件（越界），留给 T010 落地时统一。
2. **「表头缺失」与「缺必选列」的分界**：整张表/表头不存在 → `check` exit 2（C-13 的解析错误）；
   行级缺陷（列数不符 / 必选值为空 / 单元 id 形态非法）→ `row-malformed` finding + exit 1（T006 原文）。
3. **解析按表头绑定，不按位置猜列**：`test_parser_reads_columns_by_header_and_does_not_guess`
   用同一批数据 + 置换列序的台账要求仍 exit 0（T006「解析器不猜列」）。规范台账仍是
   `| unit_id | flow_class | basis | neutral | notes |`，置换只用于验证解析器不猜列。

另外两条实现接口约定：`--action check --format json` 的干净运行须带 `units == 78`（T012 期望）
与 ISO-8601 Z 的 `checked_at`；真实仓库的 `check` 测试**不带** `--repo`，以覆盖 C-5 的默认自定位。

## 7. 转绿义务（green obligations，下一段执行）

| 交付行 | 使哪些 node id 转绿 |
|--------|---------------------|
| T007 owner 判据 / 边界例 / 命名空间骨架 + 变更记录空表 | `test_owner_exists_and_declares_required_sections`、`test_change_log_row_form` |
| T008 台账 78 行 + `basis` / `neutral` 列 | `test_ledger_has_78_rows…`、`test_ledger_values…`、`test_first_batch_members…` |
| T009 `--action check`（八类 finding、下限、退出码、JSON、只读） | 单元套件 24 支中的 20 支 + `test_check_reports_78_units_and_zero_gaps` |
| T010 `--action lookup`（默认/已登记/降级） | `test_lookup_unregistered_…`、`test_lookup_registered_…`、`test_lookup_owner_*`、`test_default_marker_and_owner_degradation_label_are_mutually_exclusive`、`test_unit_ids_are_normalised_…` |
| T011 类中立封闭清单 | `test_neutral_list_is_closed_against_ledger`、`test_neutral_flag_outside_closed_list_reports_neutral_unlisted` |
| T005 正确性 oracle | `test_lookup_matches_independent_oracle`、`test_mutating_one_class…`、`test_source_and_marker_invariants…` |
| T012 US1 定向转绿 | 上述三文件 39/39 全绿；绿证据追加到本文件 |

**判据声明**：本文件只冻结「实现前红」的事实与逐条 node id；转绿后必须在同一文件追加绿跑（命令、
输出摘要、退出码），不得覆盖本节。
