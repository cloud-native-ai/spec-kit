# Red-first evidence — wp01-journal-core

One entry per red-first run: command · real output · exit status. Appended by the rows of
`wp01-journal-core` (T008, T016); never rewritten.

<!-- entries appended below -->

## T008 — first test slice, red on the tree without the engine

Command: `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py -q`
Exit status: 1

```text
        statement = journal_format()
        fixture = _fresh_line(tmp_path)
>       assert append(fixture).returncode == 0
E       assert 2 == 0
E        +  where 2 = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor...tmp/sdd-loop/worktrees/096-sdd-observer-agent/scripts/python/journal-utils.py': [Errno 2] No such file or directory\n").returncode
E        +    where CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor...tmp/sdd-loop/worktrees/096-sdd-observer-agent/scripts/python/journal-utils.py': [Errno 2] No such file or directory\n") = append({'execution_label': 'line-demo--run-demo--observer', 'journal': PosixPath('/tmp/pytest-of-agent/pytest-6336/popen-gw1/...id': 'line-demo', 'root': PosixPath('/tmp/pytest-of-agent/pytest-6336/popen-gw1/test_body_has_exactly_one_nine0'), ...})

tests/contract/test_journal_engine.py:177: AssertionError
_________________ test_missing_values_use_declared_placeholder _________________
[gw3] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-6336/popen-gw3/test_missing_values_use_declar0')

    def test_missing_values_use_declared_placeholder(tmp_path):
        placeholder = journal_format()["missing_placeholder"]
        fixture = _fresh_line(tmp_path)
>       assert append(fixture).returncode == 0
E       assert 2 == 0
E        +  where 2 = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor...tmp/sdd-loop/worktrees/096-sdd-observer-agent/scripts/python/journal-utils.py': [Errno 2] No such file or directory\n").returncode
E        +    where CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor...tmp/sdd-loop/worktrees/096-sdd-observer-agent/scripts/python/journal-utils.py': [Errno 2] No such file or directory\n") = append({'execution_label': 'line-demo--run-demo--observer', 'journal': PosixPath('/tmp/pytest-of-agent/pytest-6336/popen-gw3/...id': 'line-demo', 'root': PosixPath('/tmp/pytest-of-agent/pytest-6336/popen-gw3/test_missing_values_use_declar0'), ...})

tests/contract/test_journal_engine.py:196: AssertionError
_______________________ test_seq_continues_in_file_order _______________________
[gw2] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-6336/popen-gw2/test_seq_continues_in_file_ord0')

    def test_seq_continues_in_file_order(tmp_path):
        fixture = _fresh_line(tmp_path)
>       assert append(fixture).returncode == 0
E       assert 2 == 0
E        +  where 2 = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor...tmp/sdd-loop/worktrees/096-sdd-observer-agent/scripts/python/journal-utils.py': [Errno 2] No such file or directory\n").returncode
E        +    where CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor...tmp/sdd-loop/worktrees/096-sdd-observer-agent/scripts/python/journal-utils.py': [Errno 2] No such file or directory\n") = append({'execution_label': 'line-demo--run-demo--observer', 'journal': PosixPath('/tmp/pytest-of-agent/pytest-6336/popen-gw2/...id': 'line-demo', 'root': PosixPath('/tmp/pytest-of-agent/pytest-6336/popen-gw2/test_seq_continues_in_file_ord0'), ...})

tests/contract/test_journal_engine.py:188: AssertionError
____________________ test_header_carries_five_declared_keys ____________________
[gw0] linux -- Python 3.11.11 /usr/local/bin/python3

tmp_path = PosixPath('/tmp/pytest-of-agent/pytest-6336/popen-gw0/test_header_carries_five_decla0')

    def test_header_carries_five_declared_keys(tmp_path):
        statement = journal_format()
        fixture = _fresh_line(tmp_path)
        result = append(fixture)
>       assert result.returncode == 0, result.stderr
E       AssertionError: /usr/local/bin/python3: can't open file '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/096-sdd-observer-agent/scripts/python/journal-utils.py': [Errno 2] No such file or directory
E         
E       assert 2 == 0
E        +  where 2 = CompletedProcess(args=['/usr/local/bin/python3', '/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/wor...tmp/sdd-loop/worktrees/096-sdd-observer-agent/scripts/python/journal-utils.py': [Errno 2] No such file or directory\n").returncode

tests/contract/test_journal_engine.py:163: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_journal_engine.py::test_cli_answers_help_version_and_rejects_unknown
FAILED tests/contract/test_journal_engine.py::test_append_idempotent_on_unchanged_carriers
FAILED tests/contract/test_journal_engine.py::test_stage_coverage_over_declared_sequence
FAILED tests/contract/test_journal_engine.py::test_body_has_exactly_one_nine_column_table
FAILED tests/contract/test_journal_engine.py::test_missing_values_use_declared_placeholder
FAILED tests/contract/test_journal_engine.py::test_seq_continues_in_file_order
FAILED tests/contract/test_journal_engine.py::test_header_carries_five_declared_keys
7 failed in 6.18s
```

## T016 — tamper drills, gap drill and pointer resolution, red before T015/T017

Command: `bash scripts/bash/run-tests.sh tests/contract/test_journal_engine.py -q -k "tamper or gap or persistent"`
Exit status: 1

```text
        fixture = _clean_journal(tmp_path)
        rows = row_values(parse_journal(fixture["journal"]))
        first_observed = rows[-1]["observed_at"]
    
        restarted_at = _plus_seconds(first_observed, 60)
        restart_label = fixture["execution_label"] + "-restart"
        line_builder().append_observer_record(
            fixture["spine"], fixture["line_id"], fixture["run_id"], fixture["spec_key"],
            restart_label, restarted_at)
        fixture["execution_label"] = restart_label
        second = append(fixture)
        assert second.returncode == 0, second.stderr
    
        rows = row_values(parse_journal(fixture["journal"]))
        gaps = [row for row in rows if row["event"] == "observer-gap"]
>       assert len(gaps) == 1, [row["event"] for row in rows]
E       AssertionError: ['line-start', 'observer-start', 'stage-start', 'stage-end', 'stage-verdict', 'dispatch', ...]
E       assert 0 == 1
E        +  where 0 = len([])

tests/contract/test_journal_engine.py:316: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_journal_engine.py::test_tamper_drills_turn_check_red[unknown-event-V-5]
FAILED tests/contract/test_journal_engine.py::test_tamper_drills_turn_check_red[forged-pointer-V-10]
FAILED tests/contract/test_journal_engine.py::test_tamper_drills_turn_check_red[free-narrative-V-12]
FAILED tests/contract/test_journal_engine.py::test_tamper_drills_turn_check_red[ten-column-V-11]
FAILED tests/contract/test_journal_engine.py::test_tamper_drills_turn_check_red[unresolvable-commit-V-10]
FAILED tests/contract/test_journal_engine.py::test_persistent_pointers_resolve
FAILED tests/contract/test_journal_engine.py::test_gap_drill_emits_exactly_one_window_row
7 failed in 6.57s
```
