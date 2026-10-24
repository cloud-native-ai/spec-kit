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

---

# Green run — 069a US1 定向转绿与取证（T012）

**Captured**: 2026-10-24T13:55:52Z | **Branch**: `069-execution-expression-sdd` | **HEAD**: `e39cb05ba3a068f46690e94d0afad3a7fc0c6c5f`（实现提交见本条段末 `git log -1`）
**Interpreter**: `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`（pytest 9.1.1）；真实运行 `python3` = 3.9.6（系统解释器，引擎按 ≥3.8 stdlib-only 编写）

## 8. 三支 US1 测试转绿

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
  tests/contract/test_flow_class_ledger.py \
  tests/contract/test_flow_class_correctness.py \
  tests/unit/test_flow_class_check.py \
  -q -p no:cacheprovider
# exit code: 0
# 39 passed in 7.55s
```

实现前基线为 `30 failed, 9 passed`（owner 已在 T007/T008 落盘，故 owner 族 6 支已绿；其余 30 支全因引擎缺失）
→ 实现后 `39 passed`。正确性测试的变异断言（`test_mutating_one_class_turns_the_same_comparison_red`）
随同一批转绿：改错一类转红、改回回绿。

## 9. 引擎实跑（真实仓库，无 `--repo`，验证 C-5 自定位）

```bash
$ python3 scripts/python/flow-class-check.py --action check --format json
{
  "action": "check",
  "checked_at": "2026-10-24T13:55:34Z",
  "repo": "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit",
  "units": 78,
  "inventory": {"commands": 27, "skills": 51, "floors": {"commands": 27, "skills": 51}},
  "findings": [],
  "error": null
}
# exit code: 0

$ python3 scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.docs" --format json
{
  "action": "lookup", "checked_at": "2026-10-24T13:55:34Z", "unit_id": "/speckit.docs",
  "flow_class": "expression", "source": "ledger", "marker": null,
  "basis": "reader-oracle", "neutral": false, "error": null
}
# exit code: 0

$ python3 scripts/python/flow-class-check.py --action lookup --unit-id "/speckit.never-registered" --format json
{
  "action": "lookup", "checked_at": "2026-10-24T13:55:35Z", "unit_id": "/speckit.never-registered",
  "flow_class": "execution", "source": "default", "marker": "未声明·按默认",
  "basis": null, "neutral": false, "error": null
}
# exit code: 0
```

降级分支实测（临时空树，无 owner）：

```bash
$ python3 scripts/python/flow-class-check.py --action lookup --repo "$TMPD" --unit-id "/speckit.docs" --format json
owner-unavailable: owner document unreadable: <TMPD>/shared/definitions/flow-class-definitions.md (...)
{ "flow_class": "execution", "source": "default", "marker": null, "basis": null,
  "error": {"label": "owner-unavailable", ...} }
# exit code: 2  —— 默认类语义保留、marker 为 null、与「未登记」的 未声明·按默认 标记互斥
```

## 10. T010 定案的两处边界（实现即裁定）

1. **降级标签统一为 `owner-unavailable`**（§6.1 遗留项）：owner 不可解析/缺席 → stderr `owner-unavailable`
   + 默认类语义 + `marker=null`；「未登记」→ `source=default` + `marker=未声明·按默认`。
   测试、契约 C-7、data-model E9、tasks T006/T010/T027、feature-ref FR-016 已同步为单一标签，语义不变。
2. **表头缺失 vs 行级缺陷**：整张表/必选列缺失 → `check` exit 2（C-13 解析错误）；
   列数不符 / 必选值为空 / 单元 id 非规范 / `basis` 越界 → `row-malformed`（exit 1），且该行不进单元集
   （不再被二次判为 missing/unknown/invalid-class）。

## 11. 未关闭项（本段不修，按任务归属登记）

| 项 | 现状 | 归属 |
|----|------|------|
| 镜像漂移 `test_mirror_parity_suite` | `scripts/python/flow-class-check.py` 与 `shared/definitions/flow-class-definitions.md` 两对镜像缺失 → 2 failed / 726 passed（实跑） | T033（镜像义务段） |
| US2（文档型门禁与接线） | 未进入；T013+ 保持未勾选 | T013 起 |
| `validate-tasks.py` / 条款覆盖核对 | 本段未重跑；T004–T008 勾选状态由前段负责 | T034 / 收尾 |

## 12. 本段提交

commit: 见 `git log -1 --format=%H` 于 `069-execution-expression-sdd`（本文件与引擎、三支测试、
契约 C-7、data-model E9、feature-ref FR-016、tasks T006/T009–T012 同一提交）。

---

# Red-first evidence — 069a US2 前半（T013 / T014 / T015）与门禁 owner 转绿（T016–T019）

**Feature**: 069a-flow-classification-docs-gates（父 069） | **Scope**: US2 的三支红先测试 + `shared/workflow/expression-gates.md`
**Branch**: `069-execution-expression-sdd` | **HEAD（本段开始）**: `6c519ae173548e7dffd0004695eb41c15b5e2111`
**Interpreter**: `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`（pytest 9.1.1）
**Captured**: 2026-10-24T14:05:44Z

## 13. 红跑：三支 US2 测试（owner 落盘前）

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
  tests/contract/test_expression_gates_doc.py \
  tests/contract/test_doc_consistency_checker.py \
  tests/unit/test_doc_consistency_rules.py \
  tests/contract/test_expression_gate_wiring.py \
  -q --tb=line -p no:cacheprovider
# exit code: 1
# 64 failed, 6 passed in 0.73s   （捕获时 70 支；T014 随后补入 1 支 S3 对照侧测试，
#                                  同属 engine-missing 族，故当前为 71 支 / 65 failed）
```

采集面自检（同一解释器、同一树）：

```text
pytest <四文件> --collect-only -q  →  70 tests collected (exit 0)
python -m py_compile <四文件>       →  COMPILE-OK (exit 0)
```

红的原因（三族，均为「目标产物缺失」，无 collection / import / 语法错误）：

| 断言族 | 触发点 | 失败数 | 交付行 |
|--------|--------|--------|--------|
| owner missing | `_read_owner()` → `shared/workflow/expression-gates.md` 不存在 | 18 | T016 / T017 / T018 / T019 |
| engine missing | `_run()` → `scripts/python/doc-consistency-check.py` 不存在 | 38（契约 24 + 单元 14；补入 1 支后为 39） | T020 / T021 |
| wiring missing | `_outline_wiring_section()` / 技能 token 段 / 命令副本 | 8 | T022 / T023 / T024 / T025 |
| **合计** | | **64** | 与 `64 failed` 一致 |

逐字输出（三族各取首条）：

```text
E   AssertionError: expression-gate owner missing: shared/workflow/expression-gates.md — expected at
    T016/T017/T018/T019 (069a). Red is the intended pre-implementation state for T013.
E   AssertionError: doc-consistency checker missing: scripts/python/doc-consistency-check.py — expected
    at T020/T021 (069a). Red is the intended pre-implementation state for T014.
E   AssertionError: wiring subsection missing in docs.md — expected a `###` block under `## Outline`
    naming shared/workflow/expression-gates.md or the engines (T022/T025, 069a). Red is the pre-wiring state.
```

### 13.1 实现前即通过的 6 支（负向守卫，不是「已实现」）

| 测试 | 现在为何通过 | 实现后仍须保持 |
|------|--------------|----------------|
| `test_expression_gate_wiring.py::test_a1_docs_template_keeps_its_top_level_sections` | docs 模板顶级章节未动 | 接线只新增 `###` 小节，不改 `## ` 序列 |
| `…::test_a2_humanize_template_stays_simple` | 现模板 1 处 `SKILL.md`、无 `## Wrap-up`、非表格行 ≤ 120 | W2 只加 owner 指针，保持 Simple |
| `…::test_a5_no_class_key_assignment_or_ledger_row` | 四个接线文件零类别键赋值、零台账样式行 | 接线只写 lookup 与指针 |
| `…::test_a6_wiring_set_is_closed` | 其余 25 模板 / 49 技能零引擎与 owner 引用 | 接线封闭集只有 W1–W4 |
| `…::test_a6_wiring_inventory_matches_the_frozen_denominator` | 实测 27 模板 + 51 技能 | 分母不变 |
| `…::test_pre_completion_specs_stay_byte_identical` | 062 / 067 / 068 `requirements.md` sha256 与冻结值一致 | SC-008 |

## 14. 绿跑：T016–T019 门禁 owner

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
  tests/contract/test_expression_gates_doc.py -q -p no:cacheprovider
# exit code: 0
# 18 passed in 0.33s
```

owner 落地后同一批四文件的逐文件状态（红仍是「实现缺失」，不是测试缺陷）：

```text
tests/contract/test_expression_gates_doc.py      18 passed                      （T013 转绿）
tests/contract/test_doc_consistency_checker.py   25 failed                      （T020/T021 交付前保持红；含事后补入的
                                                                                  `test_c05_s3_owner_set_is_the_reference_side_only`，
                                                                                  同属 engine-missing 族）
tests/unit/test_doc_consistency_rules.py         14 failed                      （T020/T021 交付前保持红）
tests/contract/test_expression_gate_wiring.py     6 passed / 8 failed           （8 支全部等 T022–T025 接线）
```

8 支红全部依赖接线本体：A1/A2 取 `## Outline` 内的接线小节，A3/A4 取技能内的 owner/引擎 token 段，
A5 依赖 `_wiring_texts()`（接线出现前无从取样），A7 依赖重生成后的 8 个命令副本。故它们与接线同批转绿
（归属 T022–T025），不属 T016–T019 的绿义务。

## 15. 本段落地物与判据

| 交付行 | 落点 | 该行绿义务 |
|--------|------|-----------|
| T013 | `tests/contract/test_expression_gates_doc.py`（18 支） | 自身为红先测试；T016–T019 落地后 18/18 转绿 |
| T014 | `tests/contract/test_doc_consistency_checker.py`（24 支）+ `tests/unit/test_doc_consistency_rules.py`（14 支） | 交付 T020/T021 后转绿 |
| T015 | `tests/contract/test_expression_gate_wiring.py`（14 支，A1–A7 + 两条守卫 + SC-008） | 交付 T022–T025 后 8 支转绿 + 6 支守卫保持绿 |
| T016 | `shared/workflow/expression-gates.md` § 六面（封闭集） | C-1 |
| T017 | 同上 § 阶段算子表 / § 阻断级别 | C-2 / C-3 |
| T018 | 同上 § 读者声明 / § 证据分级与 as-of / § 结构… / § 事实一致性 / § 评审 / § 三项基线 / § 算子去重 | C-4…C-10 |
| T019 | 同上 § 阶段不变量 / § 与复杂度轴正交 / § 调用点表 / § 调用时机与降级 / § 与首批成员的关系 | C-11…C-15 |

## 16. 本段自行裁决的三处实现接口（测试即规格，记录以便 T020+ 复用）

1. **证据标注的行语法**：一行只有出现标记 `证据：` 才被视为带标注的断言行；等级取标记后第一个 token，
   `as-of <YYYY-MM-DD>`，`source: <文本>` 必填。理由：若以裸 `实测 / 推断 / 引用` 判定，规格产物里
   大量「实测」叙述会被误判为标注行。语法已写入门禁 owner § 证据分级与 as-of（判据 owner 是本文件，
   故语法不属第二来源）。
2. **「接线小节」的定位方式**：命令模板按内容锚定——`## Outline` 内第一个提到 owner 路径或引擎的
   `###` 小节；技能按 token 所在 `###` 块提取。这样 W1/W2 的小节标题由实现者自选，位置与内容仍被钉住。
3. **`--faces` 缺省 = 四面**、`--path` 缺省时 `reader` 面为 `not-applicable`、无 `--spec-dir` 时 `count`
   为 `not-run`（带 reason）：三项均取自契约 C-1 / C-4 / C-6 的既有措辞，未新增语义。

## 17. 未关闭项（本段不修，按任务归属登记）

| 项 | 现状 | 归属 |
|----|------|------|
| `doc-consistency-check.py` | 不存在；38 支测试保持红属预期 | T020 / T021 |
| W1–W4 接线与 8 个命令副本 | 未动；8 支接线测试保持红属预期 | T022–T025 |
| 镜像漂移 | `shared/workflow/expression-gates.md` 尚无 `.specify/shared/` 镜像（与既有两对同类） | T033 |
| `shared/workflow/feedback-step.md` 一行指针 | 未加：本段只声明正交契约（C-13）；指针行本体与 `shared/` 镜像同批落地，避免制造第二处未镜像漂移 | T033 |

## 18. 全量契约套件对照（相对 `notes/test-baseline-contract.txt`）

命令（排除本段三支新契约测试，避免把「红先」计成回归）：

```bash
/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest tests/contract -q --tb=no -p no:cacheprovider \
  --ignore=tests/contract/test_expression_gates_doc.py \
  --ignore=tests/contract/test_doc_consistency_checker.py \
  --ignore=tests/contract/test_expression_gate_wiring.py
# 39 failed, 4189 passed, 5 skipped, 1 warning in 225.69s
```

冻结基线是 33 条 node id。差值 6 条，**全部由缺少 `.specify/` 镜像引起**（归属 T033，本段按任务边界不写镜像）：

| 新增失败 node id | 直接原因 | provenance |
|------------------|----------|-----------|
| `test_mirror_parity_suite…[scripts/python/flow-class-check.py->…]` | 引擎无镜像 | US1（本段之前已红） |
| `test_mirror_parity_suite…[shared/definitions/flow-class-definitions.md->…]` | 分类 owner 无镜像 | US1（本段之前已红） |
| `test_mirror_parity_suite…[shared/workflow/expression-gates.md->…]` | 门禁 owner 无镜像 | 本段新增文件 |
| `test_trigger_engine.py::test_c2_sync_mirrors_check_clean` | `sync-mirrors --check` exit 2 | 同上（三处 MISS） |
| `test_scripts_distribution_parity.py::…test_repo_has_no_orphan_or_drifted_scripts` | 同上 | 同上 |
| `test_compile_propagation_order.py::test_propagation_chain_is_green_in_canonical_order` | 同上（第 3 步 sync --check） | 同上 |

一处**本段引入并已当场修复**的回归（属 Fast Fail 的 in-passing 修复，披露于此）：

- `test_one_source_of_truth.py::test_c6_single_source_sweep` 曾因门禁 owner 的 `owner_pointer` 写成
  「`one-source-of-truth.md` § Declare the owner」而转红——该测试把 `Declare the owner` 视为只允许
  出现在纪律文档里的章节名。修复：事实一致性面的指针改为「整文件即判据，无单章节锚」（该 owner 的
  T016 原文本来也只给路径），修复后 `test_one_source_of_truth.py` 33 passed。

结论：除上述 6 条镜像类（T033 义务）外，**零新增失败**；既有 33 红按纪律不修、不掩盖。

---

# Green run — 069a US2 检查器（T020 / T021）

**Feature**: 069a-flow-classification-docs-gates（父 069） | **Scope**: `scripts/python/doc-consistency-check.py`（四面）+ 契约 C-6/C-7 两处补全
**Branch**: `069-execution-expression-sdd` | **HEAD（本段开始）**: `854caf1a`
**Interpreter**: `/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest`（pytest 9.1.1；Python 3.14）
**Captured**: 2026-10-24T14:30:00Z

## 19. 绿跑：T014 的两支测试 39 支全绿

```bash
cd /Users/liuqiming.lqm/project/cloud-native-ai/spec-kit
/Users/liuqiming.lqm/project/profiles/.venv/bin/pytest \
  tests/contract/test_doc_consistency_checker.py \
  tests/unit/test_doc_consistency_rules.py \
  -q --tb=short -p no:cacheprovider
# exit code: 0
# 39 passed in 3.85s
```

逐文件：

```text
tests/contract/test_doc_consistency_checker.py   25 passed in 2.84s   （T020 C-1…C-4 + T021 C-5…C-8 的契约面）
tests/unit/test_doc_consistency_rules.py         14 passed in 1.23s   （归一化/阈值/排除项/委派降级/--faces/--json-out）
pytest --collect-only -q <两文件>                → 39 tests collected (exit 0)
python3 -m py_compile scripts/python/doc-consistency-check.py → COMPILE-OK
```

解释器覆盖面：测试解释器为 Python 3.14；另有系统 `python3`（3.9.6）实跑四支 CLI 冒烟（reader/evidence/
count/strict），行为一致——引擎只用 `argparse/json/re/subprocess/time/collections/difflib/pathlib`，符合
plan § Language/Version 的 Python ≥ 3.8 下限。

## 20. 本段自行裁决的实现接口（测试即规格，记录以便 T022+ 复用）

1. **测试侧缺一件辅助函数（Fast Fail 的 in-passing 修复，披露于此）**：首次绿跑为 `1 failed, 38 passed`，
   失败不是引擎行为而是 `test_c05_s3_owner_set_is_the_reference_side_only` 调用的 `_duplicates()` 在
   `tests/contract/` 内未定义（`NameError`；单元测试文件有同名实现）。按最小修正补入同名 helper
   （`[f for f in _findings(doc) if f.get("rule") == "duplicate-fact"]`），语义由该测试名与其文档串唯一确定，
   未改断言、未放宽阈值。修正后 39/39。
2. **委派不带 `--json-out`**：C-1 的「除 `--json-out` 外零写入」与 C-6 的调用形式在「回收 delegate 报告」上冲突；
   该引擎的 stdout 就是同一份 JSON 记录，故按只读优先执行，并把这一条写回 C-6（契约补全，不改语义）。
3. **`not-evaluated` 的理由载体**：C-3/C-8 要求降级「附 `reason`」，而 C-7 的报文字段里没有位置。实现输出
   顶层 `degradations[]`（`face/status/path/line/reason`），`faces` 的取值仍是三态字符串；契约 C-7 同步补一行。
4. **`evidence` 面的对象边界**：`shared/workflow/evidence-step.md` 与 `shared/guidelines/single-run-evidence.md`
   是另两套证据取值域的 owner（data-model E6 的 object boundary），显式排除在 evidence 面之外。
5. **S3 只作对照侧**：`duplicate` 面比较 `S1∪S2 ↔ S1∪S2` 与 `S1∪S2 ↔ S3`，从不做 S3 自比对——owner 之间
   合法的机器重生成块（如编译后的 Wrap-up 步骤表）因此不会被误报为手写副本。
6. **`path` 口径**：仓库内文件用仓库相对路径（E7 的 `path` 定义），仓库外（测试夹具在 `tmp_path`）用绝对路径；
   字典序取首处/第二处因此确定且可复现。
7. **`count` 的阶段选择**：有 `plan.md` 走 `--stage plan`，仅有 `tasks.md` 走 `--stage tasks`（由 delegate 自己
   以 exit 2 报缺 `plan.md`，其 stderr 落进 `count_check.reason`）；**不**回退 `--stage requirements`——那会让
   「只有 requirements.md」的夹具静默变绿，正是 C-6 要挡的假通过。
8. **`reader` 窗口**：前 40 个**非空行**（围栏代码行计入行数、但不在其中解析声明），两行任一缺失或值为空即
   `reader-declaration-missing`。

## 21. 真实仓库实跑（只读，自证不误报）

```bash
python3 scripts/python/doc-consistency-check.py --action verify \
  --spec-dir .specify/specs/069a-flow-classification-docs-gates --format json
# exit code: 0    （12 files；findings: 0）
# faces: reader=not-applicable evidence=pass duplicate=pass count=pass
# count_check: {"status": "delegated", "reason": null, "stage": "plan",
#               "delegate": "skills/external/sdd-loop-driver/scripts/pre-analyze-check.py"}
```

即本特性自己的 12 份形式产物同时通过四个面（含对 9 个 owner 对照侧的跨文件手写副本比对），
检查器不是「只会红」的夹具级实现。

## 22. 全量契约套件对照（相对 `notes/test-baseline-contract.txt`）

本段只新增/修改两个文件，可影响的结构面测试仅「脚本集 × 镜像」三类。用「移走新脚本再跑」的方式做
归因测量（同一棵树、同一解释器）：

```text
不带 scripts/python/doc-consistency-check.py：
  test_scripts_distribution_parity.py           1 failed   （US1 三处镜像缺失，本段之前已红）
  test_trigger_engine.py::test_c2_..._clean     1 failed   （同上）
  test_mirror_parity_suite.py                   3 failed   （flow-class-check.py / flow-class-definitions.md / expression-gates.md）
带该脚本：
  同上 5 条 + test_mirror_parity_suite.py::test_mirror_file_byte_identical[
      scripts/python/doc-consistency-check.py->.specify/scripts/python/doc-consistency-check.py]
```

结论：本段相对「本段开始时的树」只新增 **1 条**失败 node id，且它是 `.specify/scripts/python/` 镜像尚未
生成所致——与 US1、US2-前半留下的三处镜像漂移同源，归属 T033（镜像同步先于 T034 全量核验）。按任务边界
（不做接线、不写镜像）本段不生成该镜像。

## 23. 未关闭项（本段不修，按任务归属登记）

| 项 | 现状 | 归属 |
|----|------|------|
| `doc-consistency-check.py` 的 `.specify/scripts/` 镜像 | 不存在；parity 套件因此多 1 条红 | T033 |
| W1–W4 接线与 8 个命令副本 | 未动；`test_expression_gate_wiring.py` 的 8 支保持红属预期 | T022–T027 |
| `--strict` 对 `reader=not-applicable` | 不升级为失败：C-4 明写 `not-applicable` 是「没有 `--path`」的显式态，不是 `not-evaluated` | 已有裁定，无需后续动作 |

## 24. 本段提交

本段唯一提交含：检查器（新）、契约测试的一件 helper 修正、契约 C-6/C-7 两处补全、`tasks.md` 的
T020/T021 勾选与本文件。commit 见 `git log -1 --format=%H`（分支 `069-execution-expression-sdd`）。
