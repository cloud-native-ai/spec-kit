# Red-first evidence — US1 wrapper (102, T008)

Recorded 2026-11-16, **before** `scripts/bash/line-run.sh` existed. The wrapper was moved aside
to the sanctioned scratch root (`.specify/.tmp/line-run-hold/`) for the two runs and put back
afterwards; `sha256sum` before and after are identical
(`ae4d1487…1a0a5`), so the red reading is not an artifact of a modified tree.

Both runs go through the unique entry `scripts/bash/run-tests.sh` (parallel default, `-q`).

## R-1 — Contract test `tests/contract/test_line_run_contract.py`

```bash
bash scripts/bash/run-tests.sh tests/contract/test_line_run_contract.py -q
```

Runner mode line: `mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0`

Representative failure (first in the report; every case fails for the same cause):

```text
__________________ test_c02_opt_equals_value_form_is_refused ___________________
>       assert proc.returncode == 2, proc.stdout + proc.stderr
E       AssertionError: bash: /cws_data/cloud-native-ai/spec-kit/scripts/bash/line-run.sh: No such file or directory
E         assert 127 == 2
E        +  where 127 = CompletedProcess(args=['bash', '/cws_data/cloud-native-ai/spec-kit/scripts/bash/line-run.sh', ...]).returncode
tests/contract/test_line_run_contract.py:114: AssertionError
```

Summary:

```text
FAILED tests/contract/test_line_run_contract.py::test_c01_c05_help_answers_zero_without_registry_side_effects[-h]
FAILED tests/contract/test_line_run_contract.py::test_c01_c05_help_answers_zero_without_registry_side_effects[--help]
FAILED tests/contract/test_line_run_contract.py::test_c01_c05_version_answers_zero_without_registry_side_effects
FAILED tests/contract/test_line_run_contract.py::test_c02_opt_equals_value_form_is_refused
FAILED tests/contract/test_line_run_contract.py::test_c03_a_flag_after_the_separator_belongs_to_the_wrapped_command
FAILED tests/contract/test_line_run_contract.py::test_c04_undeclared_option_is_refused_and_the_command_never_runs
FAILED tests/contract/test_line_run_contract.py::test_c04_missing_option_value_is_refused
FAILED tests/contract/test_line_run_contract.py::test_c04_missing_bare_separator_is_refused
FAILED tests/contract/test_line_run_contract.py::test_c04_empty_command_is_refused
FAILED tests/contract/test_line_run_contract.py::test_c19_the_wrapper_never_reaches_for_the_journal_writer
10 failed in 2.01s
```

rc = 1.

## R-2 — Behaviour test `tests/integration/test_line_run_behavior.py`

```bash
bash scripts/bash/run-tests.sh tests/integration/test_line_run_behavior.py -q
```

Runner mode line: `mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0`

Representative failure — the registry never receives an entry because no wrapper ran:

```text
E       AssertionError: entry demo-kill-r20261116T090000Z-a001 never reached state=active;
        last read={}; registry=['runtime']
tests/integration/test_line_run_behavior.py:90: AssertionError
```

Summary:

```text
FAILED ...::test_success_registers_active_runs_the_command_and_closes_completed
FAILED ...::test_failed_command_propagates_its_status_and_closes_failed
FAILED ...::test_digest_lists_the_line_while_running_and_renders_nothing_running_after
FAILED ...::test_registration_failure_never_starts_the_command
FAILED ...::test_no_git_toplevel_exits_four_and_never_starts_the_command
FAILED ...::test_double_failure_keeps_the_command_status_and_surfaces_the_close_failure
FAILED ...::test_close_failure_over_a_successful_command_exits_with_the_engine_status
FAILED ...::test_a_killed_wrapper_leaves_the_entry_active_and_visible
8 failed in 21.91s
```

rc = 1.

## Why this is a true red leg

Both files collect and execute (no import or collection error), and every failure names the
behaviour the wrapper must provide — a missing wrapper answers `127`, so even the usage cases
cannot pass. There is no migration-style test here: nothing in this feature can turn these
assertions green except the implementation (FR-021, Constitution IV).

## Post-red tightening (disclosed)

After the implementation landed, two stderr assertions in R-2 were strengthened to the measured
engine status: the double-failure leg now asserts `engine exit 6` is visible, and the
close-failure-with-child-0 leg asserts the wrapper's status equals `6` (observed: engine
`EXIT_IO`). Both changes only add assertions; the red legs above still fail on them for the
same missing-wrapper cause.
