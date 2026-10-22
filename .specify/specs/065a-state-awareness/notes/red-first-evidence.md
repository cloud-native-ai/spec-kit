# Red-First Evidence — 065a-state-awareness

Append-only record of red (failing) test runs taken BEFORE the corresponding
implementation. Format per task: command, real output, exit code, failure
attribution.

## T003 — contract CLI/envelope tests (2026-10-22)

```
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  bash scripts/bash/run-tests.sh -q tests/contract/test_loop_state_contract.py
FAILED tests/contract/test_loop_state_contract.py::test_help_lists_actions_params_exit_ladder_and_watcher_data_note
FAILED tests/contract/test_loop_state_contract.py::test_not_implemented_action_refusal_envelope[recover-065c]
FAILED tests/contract/test_loop_state_contract.py::test_not_implemented_action_refusal_envelope[check-spine-065b]
FAILED tests/contract/test_loop_state_contract.py::test_snapshot_envelope_required_fields_and_decision_consistency
FAILED tests/contract/test_loop_state_contract.py::test_spine_consistency_nested_only
FAILED tests/contract/test_loop_state_contract.py::test_out_side_effects_and_boundary
FAILED tests/contract/test_loop_state_contract.py::test_snapshot_readonly_mtime_audit
FAILED tests/contract/test_loop_state_contract.py::test_derived_mapping_owner_is_fr004_everywhere
8 failed in 0.70s
RED_EXIT=1
```

Attribution: subject-side (T004 engine + T018 reference not yet created); assertions
mirror `contracts/loop-state-cli.md` C-1..C-6 wording verbatim, no assertion defect.

## T005–T007 — unit test gaps filled (2026-10-22)

Command (all runs below use the same canonical runner and interpreter):

```
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  bash scripts/bash/run-tests.sh -q tests/unit/test_loop_state_engine.py
51 failed, 4 passed in 24.23s
RUN_EXIT=1
```

Progression of the same file as the T005/T006 groups were appended (each line is a
real run taken right after the edit):

| after | tests | result |
|-------|-------|--------|
| pre-existing file (T005 + first T006 group) | 20 | 17 failed, 3 passed |
| added T005 resolution/legacy gaps + T006 artifact/checklist/commit/false-completion | 30 | 26 failed, 4 passed |
| added T007 derived ladder + detectors + watcher tri-state/attribution | 41 | 37 failed, 4 passed |
| added T007 IA-14/attempt/salvage/probe/SC-001 | 53 | 49 failed, 4 passed |
| added clarify no-change, unknown-baseline terminal states, watchbeat `event`, deadline inverse (final) | 55 | 51 failed, 4 passed |

Representative first failure lines (subject-side, engine still a skeleton):

```
E       AssertionError: pid
E       assert 'na' == 'missing'            # C-6 evidence-source projection (T010)
E       AssertionError: assert 'unknown' == 'known'   # legacy spine parse (T009)
E       AssertionError: assert 'na' == 'unknown'      # commits baseline (T011)
E       AssertionError: assert False is True          # false_completion (T011/T014)
E       AssertionError: assert 'UNKNOWN' == 'DONE'    # derived ladder (T013)
E       AssertionError: assert 'UNKNOWN' == 'STALLED' # watcher verbatim rule (T013)
E       AssertionError: provable attribution must pass --line-id/--run-id
                                                      # C-14 attribution form (T012)
E       AssertionError: error: --probe consumption is not implemented in this build
                                                      # probe shapes (T016)
```

Attribution: all 49 reds are subject-side (T009–T016 not implemented). No assertion
defect found; every literal asserted is owned by `contracts/*.md`, `data-model.md` or
`requirements.md` FR-004. The 4 already-passing tests are honest pre-existing greens
(not-dispatched short-circuit, na projection, single-line isolation, null path
projection) and are kept as regression guards.

## T003/T008 — contract test additions (2026-10-22)

```
$ SPECKIT_PYTHON=/Users/liuqiming.lqm/project/profiles/.venv/bin/python \
  bash scripts/bash/run-tests.sh -q tests/contract/test_loop_state_contract.py
FAILED tests/contract/test_loop_state_contract.py::test_derived_mapping_owner_is_fr004_everywhere
FAILED tests/contract/test_loop_state_contract.py::test_probe_shapes_a_and_b_are_accepted
FAILED tests/contract/test_loop_state_contract.py::test_probe_does_not_read_local_evidence
FAILED tests/contract/test_loop_state_contract.py::test_stage_artifacts_match_reference_five_dimensions
FAILED tests/contract/test_loop_state_contract.py::test_derived_mapping_is_three_way_identical
5 failed, 20 passed in 2.47s
RUN_EXIT=1
```

Per-clause attribution of the 5 reds:

- `test_probe_shapes_a_and_b_are_accepted`, `test_probe_does_not_read_local_evidence`
  — C-11/C-13 shape consumption未实现（T016）；引擎当前对 `--probe` 直接 exit 2。
- `test_stage_artifacts_match_reference_five_dimensions` — C-50 两端同时缺失：
  脚本 `STAGE_ARTIFACTS`（T011）与 `references/state-awareness.md`
  §Stage Artifact Map（T018）。
- `test_derived_mapping_is_three_way_identical` — 脚本 `DERIVED_MAPPING`（T013）与
  reference §Derived Mapping（T018）缺失；FR-004 一侧解析成功（8 条子句）。
- `test_derived_mapping_owner_is_fr004_everywhere` — 唯一的 reference 缺失红（T018），
  与本段开始前一致，保留。

Honest greens added by T008 (pre-existing correct behavior, NOT claimed red):
`--line-id` 缺失 exit 2、`--probe` 四类拒绝 exit 2、`--probe` 与五个本地参数互斥 exit 2、
证据源不可读 → `status=missing` + exit 0、`--self-test` 输出契约、确定性（仅
`evaluated_at` 差异）。直接跑引擎自测：

```
$ python3 skills/external/sdd-loop-driver/scripts/loop-state.py --self-test
ok help-ladder
ok help-watcher-codes-are-data
ok refusal-check-spine
ok refusal-recover
SELF-TEST: 4 passed, 0 failed
EXIT=0
```

