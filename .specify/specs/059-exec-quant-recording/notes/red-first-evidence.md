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

## 第三节 — T010 `tests/contract/test_exec_quant_engine.py` US2 分区(list/score)

- 日期:2026-10-16
- **偏差披露(born-green)**:T005 引擎一次成型时已包含 list-records/score 实现(超出 T005「spine + collect」任务面),US2 分区测试落笔时行为面已存在——**born-red 不可后补**,不以演练输出冒充出生红。作为替代,按仓库变异演练纪律(exec-quant 同类先例)证明分区判别力:
  - 演练:`scripts/python/exec-quant.py` 中 `if not (1 <= args.score <= 5):` 临时改写为 `if False and not …`(移除上界检查);
  - 演练运行:`pytest tests/contract/test_exec_quant_engine.py::TestScoreAction -q` → **1 failed**(`test_score_bounds`:score 6 被接受,exit 0 ≠ 2),4 个不涉边界的测试保持绿——红由被移除的守护自身引起,归因明确;
  - 恢复:按精确逆替换恢复原行;`git diff scripts/python/exec-quant.py` 输出 **0 行**(恢复零漂移,非 cp 退出码推断);复跑全文件 **38 passed**。
- 结论:US2 分区 13 项测试对契约条款具备判别力(演练实证 1 项;其余条款由引擎行为面与既有 US1 red 取证共同覆盖);born-red 义务未能满足的事实已如实记录,不以绿充红。
