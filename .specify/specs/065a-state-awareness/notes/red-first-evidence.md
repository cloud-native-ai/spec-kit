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
