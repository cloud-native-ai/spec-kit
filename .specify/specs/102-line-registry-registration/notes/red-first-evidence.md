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

## R-3 — Injection recheck: the failure close reason is load-bearing (T018)

Recorded 2026-11-16 after T014/T015 put the wrapper and its generator-produced mirror in place.
The guard is proven to have teeth by breaking the subject and observing the red leg, then
restoring it and proving the restore is byte-exact.

1. Backup before injection (sanctioned scratch, `.specify/.tmp/`):

   ```bash
   $ cp scripts/bash/line-run.sh .specify/.tmp/line-run-t018.sh
   $ sha256sum scripts/bash/line-run.sh .specify/.tmp/line-run-t018.sh
   ae4d148708f40636221d0bcd71ea0fda9ed295147e4cf09fc1adc2711211a0a5  scripts/bash/line-run.sh
   ae4d148708f40636221d0bcd71ea0fda9ed295147e4cf09fc1adc2711211a0a5  .specify/.tmp/line-run-t018.sh
   ```

2. Injection — the non-zero branch's `close_reason="failed"` was changed to `"completed"`:

   ```diff
   @@ -141,7 +141,7 @@ child_status=$?
    if [ "$child_status" -eq 0 ]; then
        close_reason="completed"
    else
   -    close_reason="failed"
   +    close_reason="completed"
    fi
   ```

3. Red reading (unique entry, one node through the runner):

   ```bash
   $ bash scripts/bash/run-tests.sh tests/integration/test_line_run_behavior.py::test_failed_command_propagates_its_status_and_closes_failed -q
   ...
   >       assert entry["last_event"] == "failed"
   E       AssertionError: assert 'completed' == 'failed'
   tests/integration/test_line_run_behavior.py:125: AssertionError
   FAILED tests/integration/test_line_run_behavior.py::test_failed_command_propagates_its_status_and_closes_failed
   1 failed in 2.11s
   ```

   rc = 1. The failure-path leg is the one that turns red; the success leg does not depend on
   this branch, which is why only the named node was run.

4. Restore + proof:

   ```bash
   $ cp .specify/.tmp/line-run-t018.sh scripts/bash/line-run.sh
   $ sha256sum scripts/bash/line-run.sh .specify/scripts/bash/line-run.sh
   ae4d148708f40636221d0bcd71ea0fda9ed295147e4cf09fc1adc2711211a0a5  scripts/bash/line-run.sh
   ae4d148708f40636221d0bcd71ea0fda9ed295147e4cf09fc1adc2711211a0a5  .specify/scripts/bash/line-run.sh
   $ git diff -- scripts/bash/line-run.sh
   (no output; exit 0)
   ```

   Source and generated mirror are byte-identical to the committed wrapper again.

5. Green rerun of the same node:

   ```text
   1 passed in 2.08s        (rc = 0)
   ```

Both readings (red under injection, green after restore) are from the same command shape, so
the guard is proven to respond to the behaviour it claims to pin, not to a permanently red or
permanently green state.

## R-4 — Scanner contract + live tests are red before the scanner exists (T021)

Recorded 2026-11-16, after T019/T020 authored the two files and **before** any
`scripts/python/line-registration-scan.py` exists (T022 is the next package).

```bash
$ bash scripts/bash/run-tests.sh \
    tests/contract/test_line_registration_scan.py \
    tests/integration/test_line_registration_scan_live.py \
    -q --names-out .specify/specs/102-line-registry-registration/test-evidence/us2-red-failed.txt
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
```

Representative failure (every node fails for the same cause; representative from the live test):

```text
__________ test_an_absent_root_is_an_input_error_not_a_clean_reading ___________
    def test_an_absent_root_is_an_input_error_not_a_clean_reading():
>       _require_scanner()
...
E       AssertionError: scanner not implemented yet: /cws_data/cloud-native-ai/spec-kit/scripts/python/line-registration-scan.py (T022 authors it; this test stays red until then)
E       assert False
E        +  where False = is_file()
tests/integration/test_line_registration_scan_live.py:54: AssertionError
```

Summary:

```text
FAILED tests/integration/test_line_registration_scan_live.py::test_an_absent_root_is_an_input_error_not_a_clean_reading
FAILED tests/integration/test_line_registration_scan_live.py::test_the_declared_live_roots_read_clean_and_the_reading_is_recorded
FAILED tests/contract/test_line_registration_scan.py::test_c05_non_directory_root_is_an_input_error_naming_the_root
FAILED tests/contract/test_line_registration_scan.py::test_c01_help_answers_zero_and_names_the_root_option
FAILED tests/contract/test_line_registration_scan.py::test_c05_a_root_with_no_judged_file_is_an_input_error
FAILED tests/contract/test_line_registration_scan.py::test_c02_missing_option_value_exits_two
FAILED tests/contract/test_line_registration_scan.py::test_c05_root_outside_the_repository_is_an_input_error
FAILED tests/contract/test_line_registration_scan.py::test_c05_missing_root_is_an_input_error_naming_the_root
FAILED tests/contract/test_line_registration_scan.py::test_c10_marker_without_a_compliant_invocation_is_a_violation
FAILED tests/contract/test_line_registration_scan.py::test_c12_owner_skip_is_named_on_the_declared_roots
FAILED tests/contract/test_line_registration_scan.py::test_c13_and_c14_the_reading_is_deterministic_and_read_only
FAILED tests/contract/test_line_registration_scan.py::test_c10_the_same_file_with_a_compliant_invocation_is_clean
FAILED tests/contract/test_line_registration_scan.py::test_c10_self_declaration_is_a_hit_not_an_exemption
FAILED tests/contract/test_line_registration_scan.py::test_c07_markdown_files_do_not_enter_judgement
FAILED tests/contract/test_line_registration_scan.py::test_c07_symlinks_are_skipped_and_never_followed
FAILED tests/contract/test_line_registration_scan.py::test_c08_the_four_criterion_constants_exist_and_are_populated
FAILED tests/contract/test_line_registration_scan.py::test_c02_undeclared_option_exits_two
17 failed in 2.10s
```

rc = 1; the runner wrote 17 failed names to `test-evidence/us2-red-failed.txt`.

Why this is a true red leg: both files collect and every node executes its body. The failure is
the subject's absence, not a syntax error, and no path in the feature can make these assertions
pass without the scanner (FR-021). The first draft used a fixture-level assertion and pytest
reported all 17 as setup **errors**, which `--names-out` does not record; the files were then
tightened so the absence asserts inside each test body and the red names are visible to the
name-level baseline comparison. `LC_ALL=C comm -13 baseline-failed.txt us2-red-failed.txt`
yields 17 — all are new names belonging to this not-yet-implemented stage, not pre-existing
failures.

After the scanner lands (T022–T025), this same command must turn green; that reading belongs to
the next package.

## R-5 — Wiring guard segment 1 is red before the four surfaces are edited (T029)

Recorded 2026-11-16, after T028 authored the first segment of
`tests/contract/test_line_registration_wiring.py` (C-01…C-09) and **before** any of the four
surfaces was edited. The pre-edit baseline is `0` hits for every pinned pattern
(`test-evidence/wiring-pre-edit-baseline.txt`; contract E-2).

```bash
$ bash scripts/bash/run-tests.sh tests/contract/test_line_registration_wiring.py \
    -q --names-out .specify/specs/102-line-registry-registration/test-evidence/us3-wiring-red-failed.txt
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
```

Representative failure (the live instructions carry no pointer bullet yet):

```text
    def test_c09_the_live_instructions_carry_the_bullet_once_and_the_links_resolve():
>       assert section.count(AMBIENT_BULLET) == 1, (
E       AssertionError: .specify/instructions.md must carry the pointer bullet exactly once (via the
E       section-level refresh, never a hand edit)
E       assert 0 == 1
tests/contract/test_line_registration_wiring.py:179: AssertionError
```

Summary:

```text
FAILED ...::test_c01_c03_the_owner_section_states_the_criterion_and_its_boundary
FAILED ...::test_c01_the_owner_names_the_carrier_and_the_registry_writer
FAILED ...::test_c03_the_owner_states_the_digest_invariant
FAILED ...::test_c05_the_status_template_carries_the_single_source_sentence_verbatim
FAILED ...::test_c06_the_status_template_keeps_its_action_set_and_adds_no_second_surface
FAILED ...::test_c07_the_template_has_exactly_one_pointer_bullet_after_exemptions
FAILED ...::test_c09_the_live_instructions_carry_the_bullet_once_and_the_links_resolve
7 failed, 2 passed in 1.97s
```

rc = 1; the seven failed names were written to `test-evidence/us3-wiring-red-failed.txt`.

Why this is a true red leg: each of the seven nodes asserts a **positive** surface fact (owner
§ 九 carries the criterion and threshold; status template carries the verbatim C-05 sentence;
template carries the verbatim C-07 bullet immediately after `Exemptions and precedence`; live
file carries it exactly once), and none of them can pass while the surfaces are unedited. The
two passing nodes are negative-only assertions (`test_c03_…restate_the_mechanical_marker_members`,
`test_c08_…does_not_restate_the_criterion`): they are drift guards that hold vacuously before
the edits and must keep holding after them — they are deliberately not counted as red legs.

T030–T036 land the four edits; T037 turns these seven nodes green. Segment 2 (C-10…C-13,
run-team) is appended by T039 and has its own red reading.

## R-6 — Wiring guard segment 2 is red before the run-team skill is wired (T040)

Recorded 2026-11-16, after T039 appended the C-10…C-13 segment to
`tests/contract/test_line_registration_wiring.py` and **before** any edit to
`skills/internal/run-team/SKILL.md` (T041–T043 belong to the next package). Full capture:
`test-evidence/us4-wiring-red-full.txt`.

```bash
$ bash scripts/bash/run-tests.sh tests/contract/test_line_registration_wiring.py \
    -q --names-out .specify/specs/102-line-registry-registration/test-evidence/us4-wiring-red-failed.txt
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
```

Representative failure (the §7 body carries none of the close obligation):

```text
    def test_c12_section_7_closes_before_the_report_and_carries_the_line_id():
        body = _subsection(_read(RUN_TEAM), "### 7.")
>       assert "deregister" in body, "§7 must close the run's line through the engine (C-12)"
E       AssertionError: §7 must close the run's line through the engine (C-12)
E       assert 'deregister' in '### 7. Report\n\n执行结束后把带日期的运行报告写入 ...'
tests/contract/test_line_registration_wiring.py:288: AssertionError
```

Summary:

```text
FAILED ...::test_c10_section_5_fails_closed_before_dispatching_any_seat
FAILED ...::test_c11_section_6_refreshes_at_each_step_boundary_with_no_second_channel
FAILED ...::test_c10_section_5_registers_the_line_at_both_engine_candidates
FAILED ...::test_c12_section_7_closes_before_the_report_and_carries_the_line_id
4 failed, 11 passed in 2.00s
```

rc = 1; the four failed names were written to `test-evidence/us4-wiring-red-failed.txt` (4 entries).
The 11 passes are segment 1 (green since T037) plus the two C-13 negative guards
(`…create_team_report_contract_is_not_touched`, `…skill_carries_no_engine_parameter_table`), which
hold **vacuously** before the wiring lands — they are drift guards, deliberately not counted as red
legs (same disclosure shape as R-5).

Why this is a true red leg: each of the four failing nodes asserts a positive fact that only the
§5 register / §6 update / §7 close steps can supply — engine candidate paths, `RUN_ID_RE`, `--help`
pointer, fail-closed before dispatch, `--last-event` refresh with the no-second-channel sentence,
`deregister` plus the `line_id` report obligation. The skill still carries none of them (measured
2026-11-16). T041–T043 land the wiring; T045 records the green reading and the removal injections.

Re-confirmed in attempt 2 of this package from the resumed tree (rc 1; 4 failed, 11 passed; the same
four names, recorded in `test-evidence/implement-p4.jsonl`).


## Post-red tightening (disclosed)

After the implementation landed, two stderr assertions in R-2 were strengthened to the measured
engine status: the double-failure leg now asserts `engine exit 6` is visible, and the
close-failure-with-child-0 leg asserts the wrapper's status equals `6` (observed: engine
`EXIT_IO`). Both changes only add assertions; the red legs above still fail on them for the
same missing-wrapper cause.
