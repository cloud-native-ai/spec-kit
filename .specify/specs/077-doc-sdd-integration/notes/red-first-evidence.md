# Red-First Evidence — Feature 077（T001–T008 段）

每个红先行组在**未改动的树上**跑一次，并把四个字段写进本文件：

| 字段 | 含义 |
|------|------|
| 重放命令 | 可直接复制执行的那一条（含解释器与工作目录前提） |
| 真实输出 | 命令的真实输出摘要（不剪裁失败名与计数行） |
| 退出码 | 该次运行的 shell 退出码 |
| 失败计数 | pytest 的 `N failed` / `N passed` 汇总行读数 |

不补记：每条只在对应测试文件写就、实现尚未落地时采集一次；实现后转绿的同一条命令另记「转绿」行，不改写红记录。

## 本段覆盖的五个红先行文件

| 测试文件 | 被测对象 | 本段是否创建 |
|----------|----------|--------------|
| `tests/unit/test_flow_class_spec_key.py` | `flow-class-check.py --action lookup` 的 `spec:` 键族（键文法、解析位置、九字段记录、三段退出码、owner 先于键、不写台账） | 是（T002） |
| `tests/contract/test_flow_class_spec_declaration.py` | 声明行逐字文法与四个作者错误码、模板字段位置、单一真源 | 是（T003） |
| `tests/contract/test_stage_class_wiring.py` | 七个阶段模板的接线子节与 execution 零变化反向守卫 | 否（T009，P2 段） |
| `tests/contract/test_document_structure_gate.py` | `doc-consistency-check.py --action structure` | 否（T013，P2 段） |
| `tests/contract/test_docs_gate_driver.py` | 驱动载荷四元组、U4 四项、两槽位内容 | 否（T016，P3 段） |

本段（part 1 / 4）只创建前两个；后三个的文件名在此登记，供后续段按同一四字段纪律追加，不预先留空条目。

## 解释器与前提

- 工作目录：仓库根（`/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`）。
- pytest：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest`（仓库自带 `.venv` 未装 pytest，见 `tasks.md` § Environment Prerequisites）。
- 单测夹具：一律在 `tmp_path` 内以字面量构造，不写真实 `.specify/specs/`。

## 条目

### T002 — `tests/unit/test_flow_class_spec_key.py`（red，2026-10-30，HEAD `e14408f7`）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/unit/test_flow_class_spec_key.py -q`（cwd = 仓库根）
- **真实输出**（失败名摘要）：

  ```text
  FAILED tests/unit/test_flow_class_spec_key.py::test_valid_spec_key_is_not_rejected_as_an_invalid_unit_id
  FAILED tests/unit/test_flow_class_spec_key.py::test_resolves_under_the_dot_specify_specs_directory
  FAILED tests/unit/test_flow_class_spec_key.py::test_resolves_when_repo_names_dot_specify_itself
  FAILED tests/unit/test_flow_class_spec_key.py::test_record_carries_exactly_the_nine_unit_key_fields
  FAILED tests/unit/test_flow_class_spec_key.py::test_declared_expression_exits_0_with_declaration_source
  FAILED tests/unit/test_flow_class_spec_key.py::test_undeclared_spec_exits_0_with_the_default_marker
  FAILED tests/unit/test_flow_class_spec_key.py::test_invalid_class_value_exits_1_not_2
  FAILED tests/unit/test_flow_class_spec_key.py::test_owner_resolution_precedes_key_grammar
  8 failed, 16 passed in 6.65s
  ```

- **退出码**：`1`
- **失败计数**：`8 failed / 16 passed`（24 项）
- **红的是什么**：`spec:` 键今天对所有取值走 `invalid unit id` + `flow_class: execution` / `source: default` / `marker: null` / **退出码 2**（与 `test-evidence/plan-resolution-baseline.txt` 一致），因此「已声明 / 未声明 / 取值越界 / 目录不存在」四类输入在今天的引擎上不可区分。16 项已绿的是**格式拒绝**与**降级形态**的回归守卫（今天的 exit 2 恰好满足它们的断言），不是本特性已实现的证明。
- **原始输出留档**：`test-evidence/p1-t002-red.txt`

### T003 — `tests/contract/test_flow_class_spec_declaration.py`（red，2026-10-30，HEAD `e14408f7`）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_flow_class_spec_declaration.py -q`（cwd = 仓库根）
- **真实输出**（失败名摘要）：

  ```text
  FAILED ...::test_well_formed_declaration_is_read_verbatim
  FAILED ...::test_malformed_forms_report_declaration_malformed[full-width-colon]
  FAILED ...::test_malformed_forms_report_declaration_malformed[field-name-case]
  FAILED ...::test_malformed_forms_report_declaration_malformed[trailing-space]
  FAILED ...::test_malformed_forms_report_declaration_malformed[inline-comment]
  FAILED ...::test_value_is_case_sensitive_and_outside_set_reports_invalid_class
  FAILED ...::test_invalid_class_names_the_file_line_and_value
  FAILED ...::test_declaration_after_related_feature_reports_misplaced
  FAILED ...::test_field_in_the_head_region_stays_legal
  FAILED ...::test_second_declaration_reports_duplicate[same-value]
  FAILED ...::test_second_declaration_reports_duplicate[different-values]
  FAILED ...::test_duplicate_outranks_misplaced_for_the_same_root_cause
  FAILED ...::test_the_four_author_error_codes_never_collapse_into_exit_2
  FAILED ...::test_absent_field_is_not_an_author_error
  FAILED ...::test_template_carries_the_field_between_status_and_input
  FAILED ...::test_template_placeholder_does_not_prefill_a_class
  16 failed, 3 passed in 1.13s
  ```

- **退出码**：`1`
- **失败计数**：`16 failed / 3 passed`（19 项）
- **红的是什么**：引擎不认识声明行（四个作者错误码全部不出现在任何一次运行里），模板还没有字段行（`StopIteration`）。3 项已绿的是**单一真源与模板卫生**的现状守卫（索引无类别列 / 详情不存取值 / 模板无判据句），它们必须在实现后仍绿。
- **原始输出留档**：`test-evidence/p1-t003-red.txt`

### T004 — `scripts/python/flow-class-check.py` 的 `spec:` 键族（partial green，2026-10-30）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/unit/test_flow_class_spec_key.py -q`
- **真实输出**：

  ```text
  FAILED tests/unit/test_flow_class_spec_key.py::test_resolves_under_the_dot_specify_specs_directory
  FAILED tests/unit/test_flow_class_spec_key.py::test_declared_expression_exits_0_with_declaration_source
  FAILED tests/unit/test_flow_class_spec_key.py::test_invalid_class_value_exits_1_not_2
  3 failed, 21 passed in 2.18s
  ```

- **退出码**：`1`（文件尚未全绿，属 T004 的预期中间态）
- **失败计数**：`3 failed / 21 passed`（红前 `8 failed / 16 passed`）
- **转绿的是哪一组**：键文法（含裸目录名 / `feature:077` / 路径形拒绝）、两顶帽子下的解析位置、spec 目录缺失与目录内缺 `requirements.md` 的退出码 2、九字段记录与 `basis: null` / `neutral: false`、`source` 永不取 `ledger`、owner 先于键族（`owner-unavailable` 统一标签）、只读。剩余 3 项全部是**声明行读取**（T005）与**取值越界归退出码 1**（T007）的断言。
- **邻近引擎回归**：`pytest tests/unit/test_flow_class_check.py tests/contract/test_flow_class_correctness.py tests/contract/test_flow_class_ledger.py -q` → `45 passed`；`flow-class-check.py --action check` 仍 `ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39`（`spec:` 键不进台账）。
- **原始输出留档**：`test-evidence/p1-t004-partial-green.txt`

### T005 — 引擎内解析声明行（partial green，2026-10-30）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/unit/test_flow_class_spec_key.py tests/contract/test_flow_class_spec_declaration.py -q`
- **真实输出**：

  ```text
  # unit
  FAILED ...::test_invalid_class_value_exits_1_not_2
  1 failed, 23 passed in 2.09s

  # contract
  FAILED ...::test_malformed_forms_report_declaration_malformed[full-width-colon]
  FAILED ...::test_malformed_forms_report_declaration_malformed[field-name-case]
  FAILED ...::test_malformed_forms_report_declaration_malformed[trailing-space]
  FAILED ...::test_malformed_forms_report_declaration_malformed[inline-comment]
  FAILED ...::test_value_is_case_sensitive_and_outside_set_reports_invalid_class
  FAILED ...::test_invalid_class_names_the_file_line_and_value
  FAILED ...::test_declaration_after_related_feature_reports_misplaced
  FAILED ...::test_second_declaration_reports_duplicate[same-value]
  FAILED ...::test_second_declaration_reports_duplicate[different-values]
  FAILED ...::test_duplicate_outranks_misplaced_for_the_same_root_cause
  FAILED ...::test_the_four_author_error_codes_never_collapse_into_exit_2
  FAILED ...::test_template_carries_the_field_between_status_and_input
  FAILED ...::test_template_placeholder_does_not_prefill_a_class
  13 failed, 6 passed in 1.29s
  ```

- **退出码**：`1`（两文件均未全绿，属 T005 的预期中间态）
- **失败计数**：单测 `1 failed / 23 passed`（T004 后 `3 failed / 21 passed`）；契约 `13 failed / 6 passed`（红前 `16 failed / 3 passed`）
- **转绿的是哪一组**：合法声明（`source: declaration` + 声明值 + `marker: null`）、头部区之外不取行、无字段的缺省路径（`execution` + `source: default` + 默认标记 + advisory `declaration-absent`，退出码 0）、模板卫生与单一真源。仍未绿的是**四个作者错误码**（`declaration-malformed` / `declaration-duplicate` / `declaration-misplaced` / `invalid-class`，T007）与模板字段行（T006）。
- **原始输出留档**：`test-evidence/p1-t005-partial-green.txt`

### T006 — `templates/requirements-template.md` 字段行（partial green，2026-10-30）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_flow_class_spec_declaration.py -q`
- **真实输出**：`11 failed, 8 passed in 1.13s`（红前 `13 failed / 6 passed`；模板位置与占位形态两条腿转绿，余下 11 条全是 T007 的四个作者错误码）
- **退出码**：`1`（文件尚未全绿，属 T006 的预期中间态）
- **失败计数**：`11 failed / 8 passed`
- **附带回归**：`pytest tests/contract/test_requirements_convention_entry_points.py tests/contract/test_checker_form.py -q` → `45 passed`（模板结构约束未被新行破坏）；镜像已由 `sync-mirrors.py --write` 产出、`--check` 退出码 0（六对全 `ok`）
- **原始输出留档**：`test-evidence/p1-t006-partial-green.txt`

### T007 — 声明形态发现与阻断（green，2026-10-30）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/unit/test_flow_class_spec_key.py tests/contract/test_flow_class_spec_declaration.py -q`
- **真实输出**：

  ```text
  ...........................................                              [100%]
  43 passed in 3.44s
  ```

- **退出码**：`0`
- **失败计数**：`0 failed / 43 passed`（红前：单测 `8 failed / 16 passed`、契约 `16 failed / 3 passed`）
- **邻近引擎定向集**（16 个既有文件：`test_flow_class_check` / `isomorphism_checker` / `reconciler_extensions` / `delegation_classes` / `expression_compatibility` / `flow_class_ledger` / `expression_gate_wiring` / `expression_gates_doc` / `expression_faces` / `review_feedback_boundary` / `migration_distribution` / `doc_consistency_checker` / `flow_class_correctness` / `ledger_reconciliation` / `sdd_compat_containment` / `isomorphism_map`）：`292 passed in 27.63s`，退出码 0——**零新增失败**（既有的 39 条基线失败不在这 16 个文件内）。
- **一次中间修正（属纠正，非裁定）**：`test_second_declaration_reports_duplicate[different-values]` 起初断言诊断里出现**第一个**取值；实现按契约（C-008）报的是**第二行**（违规行）的取值。契约只要求「点名两处行号」，未规定展示哪一个取值；断言改为取第二行的取值，并保留两处行号断言——测试与契约对齐，未改契约。
- **真机复核**：`spec:077-doc-sdd-integration` → `flow_class: execution` / `source: declaration` / `marker: null` / 退出码 0（本线自用声明行生效）。
- **原始输出留档**：`test-evidence/p1-t007-green.txt`

### T008 — 单一真源与台账边界（green，2026-10-30）

- **重放命令**：
  - `python3 scripts/python/flow-class-check.py --action check`
  - `grep -nE "\|\s*(flow_class|Flow Class)\s*\|" .specify/memory/features.md`
  - `grep -nE "^\*\*Flow Class\*\*:|^\s*[-*]?\s*flow_class\s*[:=]" .specify/memory/features/077.md`
  - `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/unit/test_flow_class_spec_key.py tests/contract/test_flow_class_spec_declaration.py -q`
- **真实输出**：

  ```text
  flow-class check: 79 unit(s) scanned, 0 finding(s) [matched=79 inventory_units=79, clean]
  coverage: ledger_rows=79 matched=79 inventory_units=79 gaps=0 parse_errors=0 floor=39
  # features.md: no class-column match; features/077.md: no value match; pointer present at line 62
  43 passed in 3.34s
  ```

- **退出码**：`0` / `0`（两条 grep 均无匹配，`||` 分支打印说明）/ `0`
- **失败计数**：`0 failed / 43 passed`
- **判定**：台账行集未变（`spec:` 键不进台账，写入即会产生 `unknown` 发现）；索引无类别列；详情只多一条指向声明行的指针、不复制取值。原始输出留档 `test-evidence/tasks-ledger-boundary.txt`。
