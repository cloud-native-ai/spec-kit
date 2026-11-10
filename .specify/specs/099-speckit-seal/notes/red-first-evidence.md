# Red-First Evidence — Feature 099（implement 阶段）

> 只记录**红先读数**：命令 verbatim、退出码与完整输出。实现转绿后的读数落 `test-evidence/`。
> 本文件是 T003 起各红先行共享的追加槽（tasks.md § Notes：写本文件的行不标 `[P]`）。

## 1. T003 红先漂移守卫 `tests/contract/test_sealed_status_domain.py`

**采集点**：T003 落地、T006–T013 任何 carrier/消费面修改之前（工作树仅新增该测试文件）。

**命令（verbatim）**：

```bash
bash scripts/bash/run-tests.sh tests/contract/test_sealed_status_domain.py -q
```

**退出码**：1（10 failed）。

**完整 stdout/stderr（verbatim）**：

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_sealed_status_domain.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

FFFFFFFFFF                                                               [100%]
=================================== FAILURES ===================================
_ test_feature_integration_carries_the_seal_protocol_row_and_closes_completed __
[gw5] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_feature_integration_carries_the_seal_protocol_row_and_closes_completed():
        """C-029 surface 5: § Status State Machine's `/speckit.seal` protocol row."""
        table = _integration_table()
        rows = [l for l in table.splitlines() if l.startswith("| `/speckit.seal`")]
>       assert len(rows) == 1, (
            "shared/workflow/feature-integration.md § Status State Machine MUST carry exactly one "
            "`/speckit.seal` protocol row; found %d (C-029 surface 5, FR-001)" % len(rows)
        )
E       AssertionError: shared/workflow/feature-integration.md § Status State Machine MUST carry exactly one `/speckit.seal` protocol row; found 0 (C-029 surface 5, FR-001)
E       assert 0 == 1
E        +  where 0 = len([])

tests/contract/test_sealed_status_domain.py:227: AssertionError
______ test_template_feature_status_token_and_status_bullet_admit_sealed _______
[gw2] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_template_feature_status_token_and_status_bullet_admit_sealed():
        """C-029 surface 2: the `[FEATURE_STATUS]` glossary row and the `**Status**` bullets."""
        text = _read(DETAILS)
        token = next((l for l in text.splitlines()
                      if l.startswith("|") and "[FEATURE_STATUS]" in l), None)
        assert token, (
            "templates/feature-details-template.md lost its `[FEATURE_STATUS]` glossary row — "
            "the surface this guard names is gone"
        )
>       assert SEALED in token, (
            "the `[FEATURE_STATUS]` glossary row does not admit `Sealed`: %r "
            "(C-029 surface 2, FR-001)" % token
        )
E       AssertionError: the `[FEATURE_STATUS]` glossary row does not admit `Sealed`: '| [FEATURE_STATUS] | Draft | Planned | Implemented | Blocked | Ready for Review | Completed |' (C-029 surface 2, FR-001)
E       assert 'Sealed' in '| [FEATURE_STATUS] | Draft | Planned | Implemented | Blocked | Ready for Review | Completed |'

tests/contract/test_sealed_status_domain.py:175: AssertionError
_________________ test_index_template_vocabulary_admits_sealed _________________
[gw3] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_index_template_vocabulary_admits_sealed():
        """C-029 surface 3: templates/feature-index-template.md's closed status vocabulary."""
        lines = [l for l in _read(INDEX_TEMPLATE).splitlines()
                 if re.search(r"(?i)status vocabulary", l)]
        assert lines, (
            "templates/feature-index-template.md carries no status vocabulary line — the surface "
            "this guard names is gone"
        )
        declared = " ".join(lines)
>       assert re.search(r"`%s`" % SEALED, declared), (
            "templates/feature-index-template.md's status vocabulary does not admit `Sealed`: %r "
            "(C-029 surface 3, FR-001)" % declared
        )
E       AssertionError: templates/feature-index-template.md's status vocabulary does not admit `Sealed`: '**Status vocabulary** (closed — these six values are the entire domain a `Status` cell may carry): `Draft` | `Planned` | `Implemented` | `Blocked` | `Ready for Review` | `Completed`.' (C-029 surface 3, FR-001)
E       assert None
E        +  where None = <function search at 0x7fc9351ee3e0>(('`%s`' % 'Sealed'), '**Status vocabulary** (closed — these six values are the entire domain a `Status` cell may carry): `Draft` | `Planned` | `Implemented` | `Blocked` | `Ready for Review` | `Completed`.')
E        +    where <function search at 0x7fc9351ee3e0> = re.search

tests/contract/test_sealed_status_domain.py:198: AssertionError
___________ test_non_disposable_check_engine_judges_the_sealed_cells ___________
[gw8] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_non_disposable_check_engine_judges_the_sealed_cells():
        """C-029 surface 6c: scripts/python/non-disposable-check.py's status × verdict table."""
        source = _read(NON_DISPOSABLE_ENGINE)
        table = re.search(r"def contradiction\(.*?\n(.*?)\n\s*return table\.get", source, re.S)
        assert table, (
            "scripts/python/non-disposable-check.py no longer carries its `contradiction` table — "
            "the surface this guard names is gone"
        )
        body = table.group(1)
>       assert re.search(r'\("Sealed", "accept"\):\s*False', body), (
            "scripts/python/non-disposable-check.py's status × verdict table has no consistent "
            "`Sealed × accept` cell (C-029 surface 6c, FR-001)"
        )
E       AssertionError: scripts/python/non-disposable-check.py's status × verdict table has no consistent `Sealed × accept` cell (C-029 surface 6c, FR-001)
E       assert None
E        +  where None = <function search at 0x7f766530e3e0>('\\("Sealed", "accept"\\):\\s*False', '    """C-802\'s closed table: `True` clash, `False` agree, `None` unknown spelling."""\n    table = {\n        ("Draf...   ("Blocked", "block"): False,\n        ("Completed", "accept"): False,\n        ("Completed", "block"): True,\n    }')
E        +    where <function search at 0x7f766530e3e0> = re.search

tests/contract/test_sealed_status_domain.py:320: AssertionError
_____________ test_non_disposable_owner_domain_line_admits_sealed ______________
[gw6] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_non_disposable_owner_domain_line_admits_sealed():
        """C-029 surface 6a: the Status Readability registry-status domain line."""
        line = next((l for l in _read(NON_DISPOSABLE_OWNER).splitlines()
                     if "注册表状态值域" in l), None)
        assert line, (
            "shared/definitions/non-disposable-definitions.md carries no 注册表状态值域 row — the "
            "surface this guard names is gone"
        )
>       assert SEALED in line, (
            "the Status Readability domain row does not admit `Sealed`: %r "
            "(C-029 surface 6a, FR-001)" % line
        )
E       AssertionError: the Status Readability domain row does not admit `Sealed`: '| 注册表状态值域（`Draft` / `Planned` / `Implemented` / `Blocked` / `Ready for Review` / `Completed` / `Relocated`） | `shared/workflow/feature-integration.md` § Status State Machine；载体声明在 `templates/feature-details-template.md` § Canonical Status State Machine |' (C-029 surface 6a, FR-001)
E       assert 'Sealed' in '| 注册表状态值域（`Draft` / `Planned` / `Implemented` / `Blocked` / `Ready for Review` / `Completed` / `Relocated`） | `shared...ntegration.md` § Status State Machine；载体声明在 `templates/feature-details-template.md` § Canonical Status State Machine |'

tests/contract/test_sealed_status_domain.py:281: AssertionError
______________ test_closure_completion_claim_family_admits_sealed ______________
[gw9] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_closure_completion_claim_family_admits_sealed():
        """C-029 surface 7: CLAIMED_IMPLEMENTED and the AUDIT_FAMILY that follows it."""
        source = _read(CLOSURE_ENGINE)
        claimed = re.search(r"(?m)^CLAIMED_IMPLEMENTED = \(([^)]*)\)", source)
        assert claimed, (
            "scripts/python/closure-acceptance-check.py no longer defines `CLAIMED_IMPLEMENTED` — "
            "the surface this guard names is gone"
        )
        members = [m.strip().strip('"\'') for m in claimed.group(1).split(",") if m.strip()]
>       assert SEALED in members, (
            "`CLAIMED_IMPLEMENTED` does not admit `Sealed`; a sealed row would not be read as a "
            "completion claim (C-029 surface 7, plan § Disclosed Rulings 3): %r" % members
        )
E       AssertionError: `CLAIMED_IMPLEMENTED` does not admit `Sealed`; a sealed row would not be read as a completion claim (C-029 surface 7, plan § Disclosed Rulings 3): ['Implemented', 'Ready for Review']
E       assert 'Sealed' in ['Implemented', 'Ready for Review']

tests/contract/test_sealed_status_domain.py:343: AssertionError
________________ test_manage_features_vocabulary_admits_sealed _________________
[gw4] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_manage_features_vocabulary_admits_sealed():
        """C-029 surface 4: skills/internal/manage-features/SKILL.md's status vocabulary."""
        row = next((l for l in _read(MANAGE_FEATURES).splitlines()
                    if re.match(r"^\s*-\s*Status vocabulary:", l)), None)
        assert row, (
            "skills/internal/manage-features/SKILL.md carries no `Status vocabulary` line — the "
            "surface this guard names is gone"
        )
        members = [v.strip().strip("`") for v in row.split(":", 1)[1].split("|")]
>       assert SEALED in members, (
            "skills/internal/manage-features/SKILL.md's `Status vocabulary` line does not admit "
            "`Sealed`: %r (C-029 surface 4, FR-001)" % members
        )
E       AssertionError: skills/internal/manage-features/SKILL.md's `Status vocabulary` line does not admit `Sealed`: ['Draft', 'Planned', 'Implemented', 'Blocked', 'Ready for Review', 'Completed'] (C-029 surface 4, FR-001)
E       assert 'Sealed' in ['Draft', 'Planned', 'Implemented', 'Blocked', 'Ready for Review', 'Completed']

tests/contract/test_sealed_status_domain.py:213: AssertionError
____ test_non_disposable_owner_status_verdict_table_carries_the_sealed_row _____
[gw7] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_non_disposable_owner_status_verdict_table_carries_the_sealed_row():
        """C-029 surface 6b: the closed status × verdict table's `Sealed` row."""
        rows = _non_disposable_status_rows()
>       assert SEALED in rows, (
            "the status × verdict table carries no `Sealed` row — the value falls outside the "
            "judged range instead of being judged (C-029 surface 6b, FR-001)"
        )
E       AssertionError: the status × verdict table carries no `Sealed` row — the value falls outside the judged range instead of being judged (C-029 surface 6b, FR-001)
E       assert 'Sealed' in {'---': ['---', '---'], 'Blocked': ['**✗ 矛盾**——注册表记了一个检查器看不见的阻断', '一致，且为绿'], 'Completed': ['一致', '**✗ 矛盾**——闭环为 `block` 的已完成特性'], 'Draft': ['**✗ 矛盾**——还在草案的特性不算闭环', '一致'], ...}

tests/contract/test_sealed_status_domain.py:290: AssertionError
_ test_template_transition_table_carries_the_sealed_edges_and_seven_state_set __
[gw1] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_template_transition_table_carries_the_sealed_edges_and_seven_state_set():
        """C-029 surface 1: § Canonical Status State Machine's transition table."""
        transitions = _transitions(_template_state_machine())
        assert transitions, (
            "templates/feature-details-template.md § Canonical Status State Machine carries no "
            "parseable transition rows — the surface this guard names is gone"
        )
        states = {s for frm, to, _ in transitions for s in (frm, to) if s and s != "(n/a)"}
>       assert states == SEVEN_STATUSES, (
            "templates/feature-details-template.md § Canonical Status State Machine transition table "
            "MUST carry the seven-status set; measured %r (C-029 surface 1, FR-001)"
            % sorted(states)
        )
E       AssertionError: templates/feature-details-template.md § Canonical Status State Machine transition table MUST carry the seven-status set; measured ['Blocked', 'Completed', 'Draft', 'Implemented', 'Planned', 'Ready for Review'] (C-029 surface 1, FR-001)
E       assert {'Blocked', '...y for Review'} == {'Blocked', '... Review', ...}
E         
E         Extra items in the right set:
E         'Sealed'
E         Use -v to get more diff

tests/contract/test_sealed_status_domain.py:151: AssertionError
__________ test_schema_owner_defines_sealed_and_its_single_transition __________
[gw0] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_schema_owner_defines_sealed_and_its_single_transition():
        """C-025: the value and the transition are decided in § Feature Status, not in a carrier."""
        body = _owner_feature_status()
>       assert SEALED in body, (
            "shared/workflow/acceptance-hardening.md § Feature Status does not define `Sealed`; "
            "the schema owner MUST decide the value before any carrier projects it (C-025)"
        )
E       AssertionError: shared/workflow/acceptance-hardening.md § Feature Status does not define `Sealed`; the schema owner MUST decide the value before any carrier projects it (C-025)
E       assert 'Sealed' in '\n\n`Blocked` is a **first-class feature status**, not "`Implemented` with a note attached". It says: the work that\n... user did not object", an agent\'s own confirmation, or a later\ndiscovery that nobody wrote down is not evidence.\n\n'

tests/contract/test_sealed_status_domain.py:112: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_sealed_status_domain.py::test_feature_integration_carries_the_seal_protocol_row_and_closes_completed
FAILED tests/contract/test_sealed_status_domain.py::test_template_feature_status_token_and_status_bullet_admit_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_index_template_vocabulary_admits_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_non_disposable_check_engine_judges_the_sealed_cells
FAILED tests/contract/test_sealed_status_domain.py::test_non_disposable_owner_domain_line_admits_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_closure_completion_claim_family_admits_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_manage_features_vocabulary_admits_sealed
FAILED tests/contract/test_sealed_status_domain.py::test_non_disposable_owner_status_verdict_table_carries_the_sealed_row
FAILED tests/contract/test_sealed_status_domain.py::test_template_transition_table_carries_the_sealed_edges_and_seven_state_set
FAILED tests/contract/test_sealed_status_domain.py::test_schema_owner_defines_sealed_and_its_single_transition
10 failed in 6.17s
```

**读数**：10/10 红，逐腿点名 7 个 C-029 surface + schema owner + non-disposable 引擎表 + closure completion-claim 家族；红由「面尚未携带 `Sealed`」引起（消息逐条给出实测成员表），不是解析崩溃。

## 2. T016 红先引擎契约测试 `tests/contract/test_seal_engine_contract.py`

**采集点**：T016 落地、`scripts/python/seal-utils.py`（T017）创建之前（工作树仅新增该测试文件）。

**命令（verbatim）**：

```bash
bash scripts/bash/run-tests.sh tests/contract/test_seal_engine_contract.py -q
```

**退出码**：1（31 errors —— 31/31 用例全部在 `engine` fixture 处红，无一条是解析/收集错误）。

**完整 stdout/stderr（verbatim 头部 + 首块 + 完整 summary；其余 30 块与首块除用例名与 worker 外逐字相同，故显式省略）**：

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_seal_engine_contract.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE                                          [100%]
==================================== ERRORS ====================================
_________ ERROR at setup of test_c010_json_and_human_renderings_agree __________
[gw29] linux -- Python 3.11.11 /usr/local/bin/python3

    @pytest.fixture(scope="module")
    def engine() -> Path:
>       assert ENGINE.is_file(), (
            "engine missing: scripts/python/seal-utils.py has not landed (T017); "
            "this is the expected red-first reading for T016"
        )
E       AssertionError: engine missing: scripts/python/seal-utils.py has not landed (T017); this is the expected red-first reading for T016
E       assert False
E        +  where False = is_file()
E        +    where is_file = PosixPath('/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/scripts/python/seal-utils.py').is_file

tests/contract/test_seal_engine_contract.py:96: AssertionError

[… 29 个同构 fixture-setup 块省略：每块都是同一断言 `engine missing: scripts/python/seal-utils.py has not landed (T017)`，仅用例名与 worker 行不同 …]

=========================== short test summary info ============================
ERROR tests/contract/test_seal_engine_contract.py::test_c010_json_and_human_renderings_agree
ERROR tests/contract/test_seal_engine_contract.py::test_c003_undeclared_option_is_rejected_before_any_action[argv1]
ERROR tests/contract/test_seal_engine_contract.py::test_c003_help_answers_zero_side_effect_and_carries_four_labels
ERROR tests/contract/test_seal_engine_contract.py::test_c002_every_invocation_family_stays_inside_the_domain
ERROR tests/contract/test_seal_engine_contract.py::test_c006_read_only_actions_persist_nothing
ERROR tests/contract/test_seal_engine_contract.py::test_c008_no_move_delete_rename_or_push_in_source
ERROR tests/contract/test_seal_engine_contract.py::test_c009_an_ancestor_specify_is_not_the_mirror_signal
ERROR tests/contract/test_seal_engine_contract.py::test_c009_mirror_copy_refuses_write_actions
ERROR tests/contract/test_seal_engine_contract.py::test_c009_spec_dir_shape_is_not_a_numeric_prefix
ERROR tests/contract/test_seal_engine_contract.py::test_c010_json_payload_keeps_non_ascii_readable
ERROR tests/contract/test_seal_engine_contract.py::test_c005_read_only_and_write_actions_partition_the_closed_set
ERROR tests/contract/test_seal_engine_contract.py::test_c009_spec_dir_must_exist_and_contain_requirements
ERROR tests/contract/test_seal_engine_contract.py::test_c003_undeclared_option_is_rejected_before_any_action[argv0]
ERROR tests/contract/test_seal_engine_contract.py::test_c006_refusal_report_is_rerun_stable
ERROR tests/contract/test_seal_engine_contract.py::test_c004_spec_dir_is_required_with_no_default
ERROR tests/contract/test_seal_engine_contract.py::test_c006_read_only_reports_go_to_stdout_only
ERROR tests/contract/test_seal_engine_contract.py::test_c003_version_answers_one_line_identity_zero_side_effect
ERROR tests/contract/test_seal_engine_contract.py::test_c004_option_surface_is_closed
ERROR tests/contract/test_seal_engine_contract.py::test_c009_read_actions_are_not_refused_by_the_mirror_guard
ERROR tests/contract/test_seal_engine_contract.py::test_fr021_engine_is_stdlib_only
ERROR tests/contract/test_seal_engine_contract.py::test_c001_undeclared_action_is_rejected_with_exit_two_and_echoes_name
ERROR tests/contract/test_seal_engine_contract.py::test_c003_undeclared_option_is_rejected_before_any_action[argv2]
ERROR tests/contract/test_seal_engine_contract.py::test_c008_write_path_allowlist_is_declared_and_closed
ERROR tests/contract/test_seal_engine_contract.py::test_c007_engine_declares_no_lock_file_concurrency
ERROR tests/contract/test_seal_engine_contract.py::test_c005_seal_declares_evaluate_before_apply
ERROR tests/contract/test_seal_engine_contract.py::test_c002_exit_code_domain_is_exactly_three_values
ERROR tests/contract/test_seal_engine_contract.py::test_c001_dispatch_table_covers_exactly_the_four
ERROR tests/contract/test_seal_engine_contract.py::test_c001_action_set_is_exactly_the_four
ERROR tests/contract/test_seal_engine_contract.py::test_c004_no_bypass_flags_exist
ERROR tests/contract/test_seal_engine_contract.py::test_c004_missing_spec_dir_exits_two
ERROR tests/contract/test_seal_engine_contract.py::test_c010_json_payload_is_canonical_and_matches_the_exit_code
31 errors in 8.39s
```

**读数**：31/31 红，全部落在同一 `engine` fixture 的 `ENGINE.is_file()` 断言上（红由「引擎尚不存在」引起，不是语法/收集失败）；用例面覆盖 C-001…C-010 + FR-021 stdlib-only 附加腿。

## 3. T019 红先契约测试 `tests/contract/test_seal_merge_plan.py`

**采集点**：T018 夹具树与 T019 测试落地之后、T020 `merge-plan` 动作体落地之前（工作树仅新增 `tests/fixtures/seal/` 与该测试文件；引擎仍是 P2 骨架，`merge-plan` 走 `_pending`）。

**命令（verbatim）**：

```bash
bash scripts/bash/run-tests.sh tests/contract/test_seal_merge_plan.py -q
```

**退出码**：1（18 failed — 15 个 `KeyError: 'plan'`（骨架 payload 无 `plan` 键），3 个退出码断言（`assert 2 == 1` ×2、`assert 2 == 0` ×1，骨架统一返回 `2`））。

**完整 stdout/stderr（verbatim；`-n auto --dist load` 使失败块顺序非确定）**：

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_seal_merge_plan.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

FFFFFFFFFFFFFFFFFF                                                       [100%]
=================================== FAILURES ===================================
_________________ test_c017_factory_doc_slice_local_detection __________________
[gw12] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-7800/popen-gw12/test_c017_factory_doc_slice_lo0')

    def test_c017_factory_doc_slice_local_detection(tmp_path):
        proc, payload = _run_plan(_copy_fixture("factory-doc", tmp_path))
>       plan = payload["plan"]
               ^^^^^^^^^^^^^^^
E       KeyError: 'plan'

tests/contract/test_seal_merge_plan.py:382: KeyError

[… 14 个同构 `KeyError: 'plan'` 失败块省略：`_plan()` / `payload["plan"]` 取值失败，根因同为「动作体未实现」；
另 3 个失败为退出码断言（`test_c016_unmapped_entry_is_a_conflict`、`test_merge_plan_is_rerun_stable` 的
`assert 2 == 1` 与 `test_merge_plan_exit_semantics` 的 `assert 2 == 0`），同样由骨架 `_pending` 的 exit 2 引起 …]

=========================== short test summary info ============================
FAILED tests/contract/test_seal_merge_plan.py::test_c017_factory_doc_slice_local_detection
FAILED tests/contract/test_seal_merge_plan.py::test_c012_split_record_order_with_basis_and_source
FAILED tests/contract/test_seal_merge_plan.py::test_c013_mandatory_floor_pointer_views
FAILED tests/contract/test_seal_merge_plan.py::test_c013_directory_candidates_are_file_level_units
FAILED tests/contract/test_seal_merge_plan.py::test_c015_id_maps_families - K...
FAILED tests/contract/test_seal_merge_plan.py::test_c013_dated_records_are_pointer_inclusions
FAILED tests/contract/test_seal_merge_plan.py::test_c017_same_number_different_meaning_conflict
FAILED tests/contract/test_seal_merge_plan.py::test_c011_slice_set_uses_both_conditions
FAILED tests/contract/test_seal_merge_plan.py::test_merge_plan_is_read_only
FAILED tests/contract/test_seal_merge_plan.py::test_merge_plan_exit_semantics
FAILED tests/contract/test_seal_merge_plan.py::test_c013_candidate_universe_is_the_closed_fifteen
FAILED tests/contract/test_seal_merge_plan.py::test_c015_id_maps_are_rerun_stable
FAILED tests/contract/test_seal_merge_plan.py::test_c011_half_condition_candidates_are_named_conflicts
FAILED tests/contract/test_seal_merge_plan.py::test_c016_unmapped_entry_is_a_conflict
FAILED tests/contract/test_seal_merge_plan.py::test_c018_same_anchor_dual_edit_is_a_conflict
FAILED tests/contract/test_seal_merge_plan.py::test_c017_cross_registry_ambiguity_is_a_conflict
FAILED tests/contract/test_seal_merge_plan.py::test_c012_letter_order_fallback_leaves_a_trace
FAILED tests/contract/test_seal_merge_plan.py::test_merge_plan_is_rerun_stable
18 failed in 6.20s
```

**读数**：18/18 红、无一静默通过；红因「动作体缺失」而非语法/收集错误。用例面覆盖 C-011…C-018 的 plan 面，外加 C-001（只读零写盘）、C-002/C-010（退出码与 verdict 一致）与 C-006（stdout-only、重跑稳定）的守护腿。夹具覆盖三种树：干净双片（`split-pair/`）、逐类冲突注入（`conflict-injections/`）、出厂文档引用（`factory-doc/`）。

## 4. T021 红先契约测试 `tests/contract/test_seal_merge_apply.py`

**采集点**：P4 两个测试文件落地之后、T023 `merge-apply` 动作体落地之前（工作树仅新增该测试与 `test_seal_merge_determinism.py`；引擎仍是 P2/P3 形态，`merge-apply` 走 `_pending`）。

**命令（verbatim）**：

```bash
bash scripts/bash/run-tests.sh tests/contract/test_seal_merge_apply.py -q
```

**退出码**：1（14 failed）。

**完整 stdout/stderr（verbatim；`-n auto --dist load` 使失败块顺序非确定）**：

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_seal_merge_apply.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

FFFFFFFFFFFFFF                                                           [100%]
=================================== FAILURES ===================================
__________ test_requirements_merge_rewrites_ids_and_keeps_parent_text __________
[gw…] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-7821/popen-gw…/test_requirements_merge_rew0')

    def test_requirements_merge_rewrites_ids_and_keeps_parent_text(tmp_path):
        repo = _copy_fixture("split-pair", tmp_path / "repo")
        _run_apply(repo)
        text = (_spec(repo) / "requirements.md").read_text(encoding="utf-8")
>       assert "- **FR-001**: Parent alpha requirement, owned by the parent." in text, (
            "C-016: a mapped entry keeps the parent phrasing (localization)"
        )
E       AssertionError: C-016: a mapped entry keeps the parent phrasing (localization)

[… 11 个同构失败块省略：动作体未实现使 `read_text()` 指向尚未生成的父级产物（`merge-manifest.json` /
`verification.md` / 合并后的 `requirements.md` 等）或 `apply` 键不存在；另 2 个失败为退出码断言
（`assert 2 == 0` ×2，`_pending` 统一返回 2；其中 validator/hash-stability 两例的失败消息把该原因
逐字写为 “the … assertion is only meaningful on a completed merge; exit=2 … not-implemented”）…]

=========================== short test summary info ============================
FAILED tests/contract/test_seal_merge_apply.py::test_requirements_merge_rewrites_ids_and_keeps_parent_text
FAILED tests/contract/test_seal_merge_apply.py::test_tasks_merge_supersedes_pre_split_rows
FAILED tests/contract/test_seal_merge_apply.py::test_merged_parent_passes_the_existing_validators
FAILED tests/contract/test_seal_merge_apply.py::test_prose_artifacts_append_unique_sections_with_source_markers
FAILED tests/contract/test_seal_merge_apply.py::test_factory_doc_reference_is_repointed_and_recorded
FAILED tests/contract/test_seal_merge_apply.py::test_contract_merge_appends_clauses_and_creates_slice_only_file
FAILED tests/contract/test_seal_merge_apply.py::test_open_conflicts_refuse_and_write_nothing
FAILED tests/contract/test_seal_merge_apply.py::test_dated_records_are_hash_stable_across_the_run
FAILED tests/contract/test_seal_merge_apply.py::test_unclosed_slice_tasks_refuse_and_write_nothing
FAILED tests/contract/test_seal_merge_apply.py::test_each_slice_carries_exactly_one_merged_into_line
FAILED tests/contract/test_seal_merge_apply.py::test_clean_split_pair_applies_with_exit_zero
FAILED tests/contract/test_seal_merge_apply.py::test_directory_candidates_merge_and_create_at_file_level
FAILED tests/contract/test_seal_merge_apply.py::test_manifest_schema_is_stable_and_self_digested
FAILED tests/contract/test_seal_merge_apply.py::test_pointer_views_and_dated_record_pointer_inclusions
14 failed in 6.50s
```

**读数**：14/14 红、无一静默通过。首次运行时 `test_merged_parent_passes_the_existing_validators` 与
`test_dated_records_are_hash_stable_across_the_run` 因未先断言 apply 成功而真空通过（对未合并夹具校验 /
零写入前后恒等），已补 `assert proc.returncode == 0` 前置断言后转红——绿必须来自合并产物本身。用例面覆盖
C-013…C-023 的 apply 面：动作三态（merge/create/keep）、dated-record 指针纳入与原件字节不变、引用改写、
拆前行 supersede、恰一行 `**Merged into**:`、manifest schema/自摘要/`checks`、既有验证器证成，以及两条
零持久化拒绝腿（开放冲突、分片未闭合）。

## 5. T022 红先集成测试 `tests/integration/test_seal_merge_determinism.py`

**采集点**：同 T021（动作体未实现期，`merge-apply` 走 `_pending`）。

**命令（verbatim）**：

```bash
bash scripts/bash/run-tests.sh tests/integration/test_seal_merge_determinism.py -q
```

**退出码**：1（3 failed）。

**完整 stdout/stderr（verbatim）**：

```text
# test runner: python3 -m pytest -n auto --dist load tests/integration/test_seal_merge_determinism.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

FFF                                                                      [100%]
=================================== FAILURES ===================================
_________ test_return_time_sort_key_mutation_turns_the_comparison_red __________
[gw16] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-7820/popen-gw16/test_return_time_sort_key_muta0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x7f15eebdf710>

    def test_return_time_sort_key_mutation_turns_the_comparison_red(tmp_path, monkeypatch):
        """Inject the canonical mutation: an ordering key that reads the return time.

        The comparison used by the determinism tests is the per-file sha256 map. If a
        sort key were replaced with ``time.time()``, two runs would disagree; this
        test proves the comparison reports that disagreement (i.e. the guard is not
        vacuous), rather than only asserting that today's engine is deterministic.
        """
        module = _load_engine()
        real_classify = module._classify_artifacts

        def time_keyed(repo, spec_dir, slices):
            rows = real_classify(repo, spec_dir, slices)
            stamp = time.time()
            for row in rows:
                row["order_stamp"] = stamp
            return sorted(rows, key=lambda row: row["order_stamp"])

        monkeypatch.setattr(module, "_classify_artifacts", time_keyed)

        first = _copy_fixture(tmp_path / "first")
>       _run_engine_in_process(module, first)

tests/integration/test_seal_merge_determinism.py:169:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

module = <module 'seal_utils_determinism' from '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/099-speckit-seal/scripts/python/seal-utils.py'>
repo = PosixPath('/tmp/pytest-of-agent/pytest-7820/popen-gw16/test_return_time_sort_key_muta0/first')

    def _run_engine_in_process(module, repo: Path) -> str:
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
…
E       AssertionError: in-process apply exited 2: '{\n  "action": "merge-apply",\n  "conditions": [\n    {\n      "code": "not-implemented",\n      "evidence": "the merge-apply action body is not implemented on this skeleton",\n      "fix_path": "run the action once its implementing work package lands",\n      "rerun": "rerun the same command after the action body is implemented"\n    }\n  ],\n  "exit_code": 2,\n  "spec_dir": "/tmp/pytest-of-agent/pytest-7820/popen-gw16/test_return_time_sort_key_muta0/first/.specify/specs/099-fixture-parent",\n  "verdict": "error"\n}\n'

[… 2 个同构失败块省略：`test_two_fresh_runs_are_byte_identical` 与 `test_rerun_in_place_is_zero_diff`
均因 `merge-apply` 返回 `exit 2 / not-implemented` 而在退出码断言处失败…]

=========================== short test summary info ============================
FAILED tests/integration/test_seal_merge_determinism.py::test_return_time_sort_key_mutation_turns_the_comparison_red
FAILED tests/integration/test_seal_merge_determinism.py::test_rerun_in_place_is_zero_diff
FAILED tests/integration/test_seal_merge_determinism.py::test_two_fresh_runs_are_byte_identical
3 failed in 6.19s
```

**读数**：3/3 红。两条确定性腿（两次全新运行逐字节一致、成功重跑零 diff）与「返回时刻排序键」变异腿
（同一 sha256 快照比较在注入时间键后必须报告差异，并附未变异引擎仍逐字节一致的对照断言）都因动作体缺失
而红，红因是「动作体未实现」而非收集/语法错误。
