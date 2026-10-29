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

---

## Part 2 / 4 段（T009–T015）

本段开头复核：`tests/contract/test_expression_compatibility.py` 与
`tests/contract/test_expression_gate_wiring.py` 在改动前均为绿（`32 passed`，退出码 0），
二者属 P1 段登记的 16 文件邻近引擎定向集，因此本段对它们承担「零新增失败」义务。

### T009 — 七模板接线与 execution 零变化反向守卫（red，2026-10-30，HEAD `8ad9d871`）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_stage_class_wiring.py -q`（cwd = 仓库根）
- **真实输出**（失败名摘要，完整留档见原始输出文件）：

  ```text
  FAILED ...::test_each_stage_template_carries_exactly_one_wiring_card[requirements|clarify|plan|tasks|checklist|analyze|implement]
  FAILED ...::test_the_card_calls_the_single_lookup_once[...7...]
  FAILED ...::test_the_card_points_at_both_owners[...7...]
  FAILED ...::test_the_card_states_the_two_branches_and_the_degradation[...7...]
  FAILED ...::test_the_card_stops_on_author_input_errors[...7...]
  FAILED ...::test_the_card_carries_no_copied_tables_or_allow_lists[...7...]
  FAILED ...::test_each_generated_command_copy_carries_the_card[...7...]
  FAILED ...::test_stripping_the_card_restores_the_baseline_bytes[...7...]
  FAILED ...::test_the_card_is_not_inside_another_section[...7...]
  63 failed, 8 passed in 0.43s
  ```

- **退出码**：`1`
- **失败计数**：`63 failed / 8 passed`（71 项）
- **红的是什么**：七个模板今天对 `flow_class|flow-class|expression` 零命中（`test-evidence/plan-stage-template-zero-hit.txt`），故 63 项接线断言全红；8 项已绿的是两条**回归守卫**——整模板不含特性号（7）与 `docs.md` / `humanize.md` 保持基线字节（1）。反向守卫的红另有其义：树上没有子节可剥离，正是「无接线即不得空绿」这条性质本身。
- **原始输出留档**：`test-evidence/p2-t009-red.txt`

### T010 / T011 / T012 — 接线、owner 追加与闭合集名册（green，2026-10-30）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_stage_class_wiring.py tests/contract/test_expression_gate_wiring.py -q`
- **真实输出**：

  ```text
  ...............................................................         [100%]
  87 passed in 1.49s
  ```

- **退出码**：`0`；**失败计数**：`0 failed / 87 passed`（T009 的同一文件红前为 `63 failed / 8 passed`）
- **owner 面复核**：`flow-class-check.py --action check` → `79 unit(s) scanned, 0 finding(s)`、`ledger_rows=79 matched=79 inventory_units=79 gaps=0`；`--action faces` → `6 face(s) parsed, 0 finding(s)`；`--action isomorphism` → `8 stage row(s), 6 gate face(s), 0 finding(s)`；`--action lookup --unit-id "spec:077-doc-sdd-integration"` → `execution` / `source: declaration`。两份 owner 的既有条款零删除、零改写（只增节与行）。
- **分发两态**：`regen-command-copies.py` 产出四个工具的七份副本（`.claude` / `.github` / `.opencode` / `.qoder`）；`sync-mirrors.py --write` 后 `--check` 六对全 `ok`、`regen-command-copies.py --check` 输出 `OK: all per-tool command copies match the source templates.`，退出码均 0。
- **确认门预算**：`scan-confirmation-gates.py --summary` → `blocking confirmation gates: 27`（destructive 20 / governance_kept 7）、`violations 0`——与改动前读数**相等**（R-12 的零余量预算未动）。

### 偏差 D-1 — 069a 的 `test_expression_compatibility.py` 名册与冻结哈希（已作最小修复，需复核）

- **事实**：`templates/commands/` 的七个阶段模板一旦带上接线卡，`tests/contract/test_expression_compatibility.py` 的两条腿必然转红（实测：`test_c5_non_wiring_files_keep_their_frozen_hashes` 与 `test_c5_wiring_surface_is_closed`，2 FAILED）。该文件属 P1 段登记的 16 文件邻近定向集，改动前全绿，且不在 `baseline-failed.txt` 的 39 条既有失败内——留着就是 GATE-5 的**新增失败**。
- **为何不删/不放宽**：两条断言承载的命题（「引擎与 owner 只可出现在被指定的名册里」「未被指定的源保持冻结」）没有被本特性废除，只被**扩大名册**。这与 `research.md` R-8 对 `test_expression_gate_wiring.py` 的裁决同源。
- **实际改法（只增不改）**：① 新增 `POST_077_WIRING_TEMPLATES`（七个阶段模板）并只让 `test_c5_wiring_surface_is_closed` 跳过它——`WIRING_TEMPLATES` 仍是 W1–W4，故「25 模板 + 49 技能」的冻结清单与其补集断言原样保留；② 用该文件**自带的** `ALLOWED_POST_BASELINE_CHANGES` 机制，为七个模板各登记一条（reason + 必须在场的三枚 marker：`spec:<spec 目录名>` / `--action lookup` / `owner-unavailable`），冻结哈希的数量断言（74 / 25 / 49）与漂移判定一律未动。
- **未动**：没有任何断言被删除或放宽；`test_c5_untouchable_framework_paths_are_unchanged`、C-1 冻结分母、C-4 未刷新形态等其余腿逐字未改。
- **复核后**：两文件 `32 passed`，退出码 0。

### T013 — 结构门禁契约测试（red，2026-10-30，HEAD `8ad9d871`；两组腿一次写全）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_document_structure_gate.py -q`
- **真实输出**（失败名摘要，完整留档见原始输出文件）：

  ```text
  FAILED ...::test_structure_action_exists_and_needs_a_spec_dir
  FAILED ...::test_default_run_is_plan_side_only_and_says_two_way_not_run
  FAILED ...::test_subsections_and_columns_are_checker_constants
  FAILED ...::test_the_code_set_is_exactly_the_four_families
  FAILED ...::test_expression_line_with_a_complete_plan_passes
  ...（结构语法 4 例 / 证据面 5 例 / owner 面 3 例 / 两向 2 例 / NA·降级·作者错误 / 基线两例 / --freeze / 重跑稳定）
  FAILED ...::test_a_missing_baseline_reads_as_the_empty_set
  FAILED ...::test_same_plan_yields_the_same_violation_set
  25 failed, 1 passed in 1.82s
  ```

- **退出码**：`1`
- **失败计数**：`25 failed / 1 passed`（26 项）
- **红的是什么**：今天 `--action structure` 被 argparse 以 `invalid choice` 拒绝、退出码 2（与 `test-evidence/plan-resolution-baseline.txt` 一致），因此四子节、四族码、两向比对、基线、NA/降级/作者错误全部不可达。唯一已绿的是 `test_faces_and_parse_faces_are_unchanged`——**回归守卫**，今天成立且实现后也必须成立。
- **一次中间修正（属纠正）**：`test_the_cli_rejects_structure_as_a_face` 起初在红树上「通过」，但原因是**整个动作**被拒而非 `--faces structure` 被拒（空绿）。改为先跑一次 `--faces reader` 作对照（同样为 `--action structure`，必须能跑）、再断言 `--faces structure` 退出 2，红计数由 24 变 25。
- **原始输出留档**：`test-evidence/p2-t013-red.txt`

### T014 / T015 — `--action structure` 与两向比对（green，2026-10-30）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_document_structure_gate.py tests/contract/test_stage_class_wiring.py tests/contract/test_expression_gate_wiring.py -q`
- **真实输出**：

  ```text
  .........................................                              [100%]
  113 passed in 6.73s
  ```

- **退出码**：`0`；**失败计数**：`0 failed / 113 passed`（结构门禁 26 / 接线 71 / 闭合集 16）
- **真机复核**（本线自身是 `execution`，故结构门禁对它应报不适用而不是通过）：
  `python3 scripts/python/doc-consistency-check.py --action structure --spec-dir .specify/specs/077-doc-sdd-integration`
  → `class=execution source=declaration` / `status: not-applicable` / `two-way: not-run` / `files_scanned: 1` / `not-applicable: 结构门禁只适用于表达类…`，退出码 0。
- **四面未动**：`--faces` 的取值集仍是 `reader` / `evidence` / `duplicate` / `count`；`--action` 的 choices 为 `{verify, structure}`；六面 owner 与阶段算子表一行未改（`--action faces` 仍 `6 face(s) parsed, 0 finding(s)`）。
- **一次中间修正（属纠正）**：`Reader Baseline` 两行在 plan 与落文里逐字相同，被复用的 `duplicate` 面按机械下限判成 `duplicate-fact`（假阳性——读者声明是**结构标记**，plan 与落文都必须携带，不是手写事实副本）。修法是在重复判定前剔除两枚 reader 标记行，阈值与码一律未动（MUST NOT 自建第二套阈值）。
- **原始输出留档**：`test-evidence/p2-t015-green.txt`、`test-evidence/p2-t009-t015-green.txt`

---

## Part 3 / 4 段（T016–T022）

### T016 — 驱动载荷 / U4 / 两槽位契约测试（red，2026-10-30，HEAD `0970c519`）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_docs_gate_driver.py -q`（cwd = 仓库根）
- **真实输出**（失败名摘要，完整留档见原始输出文件）：

  ```text
  FAILED ...::test_the_stage_prompt_skeleton_carries_the_class_quartet
  FAILED ...::test_the_payload_value_domains_are_closed
  FAILED ...::test_the_quartet_is_one_rule_for_both_topologies
  FAILED ...::test_a_missing_quartet_key_is_a_dispatch_construction_defect
  FAILED ...::test_the_stage_subagent_may_not_infer_or_default_the_class
  FAILED ...::test_the_error_slot_domain_excludes_the_advisory_code
  FAILED ...::test_an_empty_marker_is_missing_only_outside_the_degraded_shape
  FAILED ...::test_the_class_value_comes_from_the_requirements_declaration_each_time
  FAILED ...::test_u4_adds_four_blocking_checks_for_expression_lines
  FAILED ...::test_u4_counts_operators_from_the_operator_table_only
  FAILED ...::test_u4_evidence_is_existence_and_non_empty_without_hash_comparison
  FAILED ...::test_u4_compares_the_payload_class_with_the_on_the_spot_parse
  FAILED ...::test_u4_routes_the_owner_unavailable_payload_away_from_the_expression_checks
  FAILED ...::test_u4_requires_the_stage_status_row
  FAILED ...::test_gate_evidence_missing_is_incomplete_and_blocks_the_next_dispatch
  FAILED ...::test_a_build_sub_row_failure_turns_the_operator_verdict_fail
  FAILED ...::test_a_not_applicable_build_sub_row_is_listed_separately
  FAILED ...::test_the_slot_skeleton_is_unchanged
  FAILED ...::test_expression_lines_use_the_docs_gate_selection_basis
  FAILED ...::test_the_rc_column_is_the_aggregated_exit_code
  FAILED ...::test_passed_and_failed_count_operator_level_rows_only
  FAILED ...::test_not_applicable_is_not_a_cross_level_equation
  FAILED ...::test_closure_baseline_compare_is_a_name_level_operator_id_diff
  FAILED ...::test_an_unrun_slot_writes_no_row_and_records_no_zero
  FAILED ...::test_the_audit_and_the_slot_semantics_are_unchanged
  FAILED ...::test_the_class_branch_moves_nothing_but_operators_and_slots
  FAILED ...::test_the_skill_hard_requirements_carry_the_class_branch
  FAILED ...::test_the_skill_declares_the_invariants_the_class_may_not_move
  FAILED ...::test_the_class_branch_lives_in_the_three_declared_files
  FAILED ...::test_the_driver_names_the_implement_operator_and_copies_no_other[path0]
  FAILED ...::test_the_driver_names_the_implement_operator_and_copies_no_other[path1]
  31 failed, 2 passed in 0.21s
  ```

- **退出码**：`1`；**失败计数**：`31 failed / 2 passed`（33 项）
- **红的是什么**：驱动技能与 `references/` 对**收窄 token 集** `flow_class|flow-class` 零命中（`grep -rn -E "flow_class|flow-class" skills/external/sdd-loop-driver/` 退出码 1）；骨架无类别四元组、U4 无表达类四项、efficiency-model §2 无 `docs-gate-full` 分支、`SKILL.md` 的 `## Hard Requirements` 无类别分支——31 条断言因此全红。
- **两绿的是回归守卫**（今天成立且实现后必须成立）：U4 的既有四条件（哨兵/产物/纪律/记账）与八阶段链 + 哨兵字面量。
- **token 集收窄的证据**：`expression` 不纳入——`skills/external/sdd-loop-driver/references/watch-model.md:158` 有无关的 `integer expression expected`，纳入即产出假阳性（该反例已随红记录留档）。
- **原始输出留档**：`test-evidence/p3-t016-red.txt`。

### T017 / T018 / T019 / T020 — 四文件类分支落地（green，2026-10-30）

- **重放命令**：`/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract/test_docs_gate_driver.py -q`
- **真实输出**：`33 passed in 0.06s`，退出码 `0`（红前同一文件 `31 failed / 2 passed`）
- **转绿的是哪一组**：T017 → 第①段四元组 + 本地/远端同规 + 缺键即派发构造缺陷 + `error` 值域与 advisory 排除 + `marker` 收窄 + 每次派发前从声明行解析；U4 四项 blocking（算子表分母 / 证据存在且非空不做哈希 / 载荷与当场解析一致且 `owner-unavailable` 分支 / `stage-status` 在场）与「门禁证据缺失 = 未完成」。T018 → implement 证据面（四面 + `structure` 子步 + `face=build` 子行 + 唯一证据来源 + SC 记法）与 U4 的「四面 ≠ 算子表四行」读法。T019 → efficiency-model §2.8 的 `docs-gate-full` 槽位内容（`selection_basis` / `command` / 聚合 `rc` / 算子级 `passed`/`failed` / 名称级 `baseline_compare` / `not-applicable` 单列 / 未运行不写行）。T020 → `SKILL.md` Hard Requirement 13（四元组、U4 门禁证据、`owner-unavailable` 分支、两条 references 指针、阶段序列与 100% 调用率不动）。
- **邻近定向集**：18 个文件 `411 passed`，退出码 `0`——含 `test_sdd_loop_driver_efficiency`（TB-01…TB-10 全绿，§2 骨架未被改写）、`test_sdd_loop_driver_skill`（H2 清单与镜像字节）、`test_expression_compatibility`（SKILL.md 的 `ALLOWED_POST_BASELINE_CHANGES` 三枚 marker 仍在场）、`test_migration_distribution`（skills 未新增 `--action check|delegation|faces|isomorphism` 调用点）。
- **原始输出留档**：`test-evidence/p3-t016-t020-green.txt`。

### 本段五次「纠正」（非裁定；均为测试断言与契约字面量的对齐，未改契约）

1. `test_the_driver_names_the_implement_operator_and_copies_no_other` 起初只断言「id 集合 ⊆ {`G-implement-structure`}」——空集时**空绿**。改为同时要求该 id 在场（U4(a) 的分母必须可寻），红计数由 29 failed 变 31 failed。
2. `assert "review 通过之后"` 与实现里的 `` `review` 通过之后 `` 因反引号不相邻而失配——断言语义正确、字面形态错误；改为 `"review"` 与 `"通过之后"` 两条并存。
3. `("不新增聚合脚本",)` 与实现句「MUST NOT 为此新增聚合脚本」不相邻——改为 `("MUST NOT", "新增聚合脚本")`，与 C-006 的否定形态一致。
4. `("之和", …)` 与实现里的 `两值之**和**` 因加粗标记拆断——把实现改成 `两值之和`（措辞未变义）。
5. 载体守卫起初要求三个文件都出现 `flow_class`——但 T019 只要求 efficiency-model 出现 `docs-gate-full`（槽位 owner 不复述类别键）；改为**按文件登记各自 marker**，stray 扫描仍用 `flow_class|flow-class`。

### T021 / T022 — 零新增机制与分发收尾（green，2026-10-30）

- **T021**：`/speckit.*` 命令清单（`templates/commands` ∪ 四个 per-tool 副本目录）基线 27 / 当前 27、差集 `[]`；依赖清单 6 / 6、`pyproject.toml` blob 逐字相同；进程清单 19 / 19（`while True|serve_forever|socketserver|APScheduler|schedule.every|daemon=True` 于 `*.py`/`*.sh`）、服务声明文件空集对空集；`doc-consistency-check.py` 的 `FACES` 仍四面、`--faces structure` 以退出码 2 被拒；`scan-confirmation-gates.py --summary` 两次读数同为 `blocking confirmation gates: 27`。`allowed difference set = []`、新增命令/依赖/常驻进程/确认门均 0。留档 `test-evidence/tasks-scope-set-difference.txt`、`test-evidence/zero-new-mechanism.txt`。
- **T022**：经 profiles venv 跑 `sync-mirrors.py --write` 后 `--check` 六对全 `ok`、退出码 0，文件数与基线逐对相同（22 / 406 / 136 / 3 / 117 / 60）；`regen-command-copies.py --check` 报 `OK: all per-tool command copies match the source templates.`、退出码 0；副本套数为本仓实存的四个目标（`.claude` / `.github` / `.qoder` / `.opencode`），`templates/commands/**` 不在 templates 镜像对内。留档 `test-evidence/tasks-distribution-after.txt`、`test-evidence/sync-mirrors-check-after.txt`。
