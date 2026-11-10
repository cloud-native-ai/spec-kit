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

## wp01 closeout — row-by-row verification (2026-11-10)

Verifier: wp01 closeout pass. Rows audited: T006–T017, T036 (13 rows; write territory
`shared/declarations/facts/journal-format.yaml`, `tests/fixtures/sdd-observer/`,
`scripts/python/journal-utils.py`, `tests/contract/test_journal_engine.py`). No artifact was
missing; nothing was authored in the wp01 write territory during closeout — the only closeout
writes are the 13 task checkboxes and this record.

| Row | Artifact / evidence | Check reading | Verdict |
|-----|--------------------|---------------|---------|
| T006 | `shared/declarations/facts/journal-format.yaml` | `kind: record-schema`; 5 header keys, 9 entry columns in order, 16 event classes with `min_persistent`, retention classes `persistent`/`runtime`, 10 pointer kinds, `-` placeholder, escaping rule; consumed through `declaration_reader` (engine + tests, no second copy) | pass |
| T006 | `test-evidence/journal-format-harness.txt` | `harness-triple-check.py --action verify`: declarations 34 → 35, findings 4 → 4 (identical four advisory `unclassified-candidate` rows, zero NEW). The row's "exit 0" literal is contradicted by the measured exit (1, pre and post); the disclosure in that evidence file stands and the criterion "gains no NEW finding" is met | pass (disclosed slip) |
| T007 | `tests/fixtures/sdd-observer/line_builder.py` | Builds the stub line under caller `tmp_path`: spine with U0 block + observer record section, quartet envelopes, sentinel logs, checkpoints, meta envelopes, git history; stage list + sentinel template read from the fact owners via `declaration_reader`, not restated | pass |
| T008 | `tests/contract/test_journal_engine.py` (US1 slice, 7 cases) | Red run recorded above: `7 failed`, exit 1, all before the engine existed | pass |
| T009 | `scripts/python/journal-utils.py` CLI | Exactly `append` / `check`; `configure_parser` / `guard_argv` with ImportError fallback; C-03 append flags incl. mutually exclusive `--settle` / `--final`; closed exit set; stdlib only | pass |
| T010 | `scripts/python/journal-utils.py` projection | Header written once; nine-column table; closed carrier list projected; stable row identities skip repeats; `seq` continues; `\|` escape / newline collapse from the fact | pass |
| T011 | `scripts/python/journal-utils.py` writer protocol | Non-blocking exclusive `flock` on the journal file itself → exit 3 `concurrent-writer-refused`, writes nothing, no lock file; `check_identity` mismatch → exit 2 before the journal is opened | pass |
| T012 | `test-evidence/us1-journal-coverage.txt` | Declared US1 invocation re-run at closeout: `3 passed in 6.31s`, exit 0 (matches the stored reading) | pass |
| T013 | `test-evidence/sc001-mutations.txt` | Both mutations re-run at closeout: delete-journal → `1 failed`; drop-stage-end:plan → `1 failed` (each exit 1) | pass |
| T014 | `tests/fixtures/sdd-observer/tamper_builder.py` | Five variants: tenth column `recommendation`, `should-improve` outside the closed set, free narrative paragraph, forged persistent pointer, unresolvable commit | pass |
| T015 | `scripts/python/journal-utils.py` gap derivation | `_gap_candidates`: first append of a later execution appends exactly one `observer-gap` (window start = last `observed_at`, window end = new first write); gap drill green, mutated-engine leg turns V-17 red | pass |
| T016 | `tests/contract/test_journal_engine.py` (US2 slice, 8 cases) | Red run recorded above: `7 failed`, exit 1 before T015/T017; now covers five tamper drills, gap drill with teeth, persistent-pointer resolution, free-narrative rejection | pass |
| T017 | `scripts/python/journal-utils.py` `check` | Findings as `code: path:line`; V-1…V-13 and V-17 (V-16 is append-time under C-07); closed sets from the facts; pointer resolution; escaping and free narrative; exit 0/1/2; strictly read-only | pass |
| T036 | `tests/fixtures/sdd-observer/dual_line_builder.py` | Two independent roots, each with its own spec dir, spine and state dir; consumption test owned by wp02 T037 | pass |

Closeout readings (all through `bash scripts/bash/run-tests.sh`):

- Full module `tests/contract/test_journal_engine.py -q` → **15 passed in 6.73s**, exit 0
- US1 declared selection `-k "coverage or append or idempotent or header"` → **3 passed in 6.31s**
- Mutation A `SDD_OBSERVER_MUTATION=delete-journal … -k stage_coverage` → **1 failed** (red as designed)
- Mutation B `SDD_OBSERVER_MUTATION=drop-stage-end:plan … -k stage_coverage` → **1 failed** (red as designed)
- CLI probes: `--help` exit 0, `--version` exit 0 (`journal-utils.py 0.0.22`), `--bogus-option` exit 2

Checkboxes: 13 of 13 wp01 rows flipped `[ ]` → `[X]` in `tasks.md` (no other row touched).

Commits: wp01 artifacts landed in `50cdd6cb5` (T006, T007), `2678448c4` (T014, T036),
`e0074755f` (T008, T016), `81f46a369` (T009–T011, T015, T017), `c5edfc9f8` (T012, T013, T006
harness). This closeout record ships in the closeout commit itself.

Anomaly line: `ANOMALY: none`; in-passing repairs: none during closeout (the T006 exit-code
literal slip was already disclosed in `journal-format-harness.txt` before this pass).

