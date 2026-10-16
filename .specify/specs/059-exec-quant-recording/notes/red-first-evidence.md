# Red-First Evidence(Feature 059)

红先取证纪律:US1/US2 分区测试在引擎实现前运行并记录真实失败;US3 分区按迁移/回归例外置于实现后(无红先义务,tasks.md A-tasks-6)。

## 第一节 — T003 `tests/contract/test_exec_quant_engine.py`(US1 分区,red-first)

- 日期:2026-10-16
- 命令:`bash scripts/bash/run-tests.sh tests/contract/test_exec_quant_engine.py -q`(canonical runner)
- 退出码:`1`
- 真实输出尾部:

```text
FAILED tests/contract/test_exec_quant_engine.py::TestActionClosedSet::test_choices_exact
FAILED tests/contract/test_exec_quant_engine.py::TestActionClosedSet::test_missing_action_is_usage_error
FAILED tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_writes_storage_and_record
FAILED tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_explicit_run_id
FAILED tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_synthesized_without_determination
FAILED tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_adopts_recent_determination_run_id
FAILED tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_explicit_run_id_carries_matching_record
FAILED tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_ignores_determination_outside_recent_window
FAILED tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_counts_errors_from_declared_sources
FAILED tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_idempotent_duplicate
FAILED tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_write_failure_exits_1_with_visible_stderr
FAILED tests/contract/test_exec_quant_engine.py::TestIdentityForms::test_invalid_unit_id_is_usage_error
FAILED tests/contract/test_exec_quant_engine.py::TestIdentityForms::test_missing_unit_id_is_usage_error
FAILED tests/contract/test_exec_quant_engine.py::TestIdentityForms::test_unit_type_mismatch_is_usage_error
FAILED tests/contract/test_exec_quant_engine.py::TestIdentityForms::test_skill_form_infers_skill_type
FAILED tests/contract/test_exec_quant_engine.py::TestIdentityForms::test_custom_form_infers_custom_unit_type
FAILED tests/contract/test_exec_quant_engine.py::TestIdentityForms::test_custom_form_accepts_explicit_custom_unit_type
FAILED tests/contract/test_exec_quant_engine.py::TestFieldBinaryLaw::test_degraded_record_holds_the_law
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_endpoint_candidates_origin_only
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_endpoint_candidates_absent_marker
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_qoder_adapter_reads_config_face
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_qoder_adapter_reads_per_model_effort_when_set
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_missing_config_face_degrades_to_marker
FAILED tests/contract/test_exec_quant_engine.py::TestAgentCollection::test_resolved_agent_fields_from_wrapper_host
FAILED tests/contract/test_exec_quant_engine.py::TestAgentCollection::test_version_measured_from_wrapper_host_binary

25 failed in 1.01s
```

- 失败归因:**subject 缺失**(引擎 `scripts/python/exec-quant.py` 不存在,subprocess 报 `No such file or directory`)——断言面本身无缺陷;rc-2 类断言同时核验 `usage:` 词形,故引擎缺席时不产生假绿(非空真判别成立)。
- 判别性佐证摘录(red 输出真实片段):`Can't open file '/storage/project/cloud-native-ai/spec-kit/scripts/python/exec-quant.py': [Errno 2] No such file or directory`。

## 第二节 — T004 `tests/contract/test_probe_engine_action_sets.py` 扩展(red-first)

- 日期:2026-10-16
- 命令:`bash scripts/bash/run-tests.sh tests/contract/test_probe_engine_action_sets.py -q`
- 退出码:`1`
- 真实输出尾部:

```text
FAILED tests/contract/test_probe_engine_action_sets.py::test_exec_quant_action_set_exact
1 failed, 4 passed in 0.11s
```

- 失败归因:**subject 缺失**(引擎文件不存在,exact-pin 的 `is_file()` 前置断言即红);既有 4 测试(probe/feedback exact-pin、disjoint、union-hit)全绿——扩展未破坏既有面。
- 契约勘正(probe-registration.md §3 行内 `{collect, list, score}` 系笔误):exact-pin 按 D1 已裁决动作名钉 `{collect, list-records, score}`,与 tasks.md T004 行一致。
