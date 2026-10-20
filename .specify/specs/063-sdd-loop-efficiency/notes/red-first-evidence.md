# Red-First Evidence — Feature 063

Each entry records the command, the real output and the exit status of a red
run captured before the implementation it defends. No entry is backfilled.

## T000 — driver-stall-fixture.py (SC-010)

- Date: 2026-10-20
- Command: `python3 tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py --self-test`
- Exit status: `1`
- Output:

```text
Traceback (most recent call last):
  File "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py", line 491, in <module>
    sys.exit(main())
  File "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py", line 473, in main
    return self_test()
  File "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py", line 403, in self_test
    first = run_all_scenarios(str(repo_root), root_dir, 0)
  File "/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit/tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py", line 321, in run_all_scenarios
    raise RuntimeError("driver program not implemented yet (red-first skeleton)")
RuntimeError: driver program not implemented yet (red-first skeleton)
```

- Meaning: the self-test exercises the documented U4/U5 driver program, which
  is still the red-first skeleton. The fully implemented fixture must turn this
  same command green; the T051 driver-stall mutation drill later proves the
  comparison can fail (SB-5 reversal).

## T008 — tests/unit/test_admission_check.py

- Date: 2026-10-20
- Command: `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py -q`
- Exit status: `1`
- Output tail:

```text
FAILED tests/unit/test_admission_check.py::test_multiline_or_branch_mismatch_lines_manifest_rejected
FAILED tests/unit/test_admission_check.py::test_open_clarification_marker_rejected
FAILED tests/unit/test_admission_check.py::test_unresolved_related_feature_rejected
FAILED tests/unit/test_admission_check.py::test_exit_codes_0_1_2 - assert 2 == 0
23 failed in 52.52s
```

- Meaning: `admission-check.py` does not exist yet (every invocation exits 2
  from the interpreter). The same suite must go green after T010.

## T009 — tests/contract/test_sdd_loop_driver_efficiency.py (FL clauses)

- Date: 2026-10-20
- Command: `bash scripts/bash/run-tests.sh tests/contract/test_sdd_loop_driver_efficiency.py -q`
- Exit status: `1`
- Output tail:

```text
FAILED tests/contract/test_sdd_loop_driver_efficiency.py::test_fl_06_reversion_procedure
FAILED tests/contract/test_sdd_loop_driver_efficiency.py::test_fl_07_analyze_review_unchanged
FAILED tests/contract/test_sdd_loop_driver_efficiency.py::test_fl_08_admission_script_interface
FAILED tests/contract/test_sdd_loop_driver_efficiency.py::test_fl_09_definition_owned_and_pinned
FAILED tests/contract/test_sdd_loop_driver_efficiency.py::test_fl_10_self_application_exclusion
10 failed in 0.16s
```

- Meaning: the owner document, the script and the downstream blocks do not exist
  yet. FL tests must go green after T011/T012.
