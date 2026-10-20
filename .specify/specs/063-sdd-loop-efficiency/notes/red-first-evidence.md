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
