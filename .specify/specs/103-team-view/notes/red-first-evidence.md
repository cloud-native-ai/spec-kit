# Red-first evidence — 103-team-view (T009)

- Captured: 2026-11-24T03:59Z, BEFORE any implementation file existed
  (`scripts/python/team-view.py` absent; `templates/commands/team.md` still three-mode)
- Command (the unique entry; no pipeline, stdout+stderr captured whole):
  `bash scripts/bash/run-tests.sh tests/unit/test_team_view_parsers.py tests/contract/test_team_view_program_contract.py tests/contract/test_team_view_command.py tests/integration/test_team_view_program.py -q`
- rc: **1** · summary: **38 failed, 1 passed, 192 errors in 6.34s**
- Full capture: `.specify/.tmp/red-first-run.out` (stage-local; not committed)

## Per-file readings

| File | Red | Shape | Decisive excerpt (verbatim) |
|------|-----|-------|-----------------------------|
| `tests/unit/test_team_view_parsers.py` | 192 errors | every test errors at module load — the program does not exist | `FileNotFoundError: [Errno 2] No such file or directory: '…/scripts/python/team-view.py'` (raised in `_load_program()` → `spec.loader.exec_module`) |
| `tests/contract/test_team_view_program_contract.py` | 16 failed | every subprocess invocation fails to start the program | `AssertionError: /usr/local/bin/python3: can't open file '…/scripts/python/team-view.py': [Errno 2] No such file or directory` |
| `tests/contract/test_team_view_command.py` | 11 failed, 1 passed | the template still runs the three-mode text | `AssertionError: missing heading: ### View Mode`; `assert len(rows) == 4` fails on the three-row table |
| `tests/integration/test_team_view_program.py` | 11 failed | every scenario fails at the first invocation | `AssertionError: … can't open file '…/scripts/python/team-view.py'` |

The single pass is deliberate and is **not** a false green: `test_other_rows_keep_their_routing_targets`
asserts the pre-existing create/modify/run routing targets, i.e. a behaviour this feature MUST
preserve. It is expected to keep passing after the implementation lands.

## Truthfulness of the reds

- Every red above is attributable to the **subject under test being absent** (no program file,
  no View Mode section), not to a fragile assertion: T005/T006/T008 fail at process/module
  load, and T007 fails on the explicit missing-heading/three-row assertions.
- **Correction in passing (disclosed)**: the first capture of this run showed three T006 tests
  passing **falsely** — a missing script makes CPython exit 2, which coincided with the
  expected input-error code. The three assertions were tightened before this capture so a
  missing/unstartable program cannot look green:
  `test_extra_positional_rejected` now requires `unrecognized arguments`,
  `test_invalid_scope_value_rejected` requires the offending value in stderr, and
  `test_behavioural_exits_stay_inside_the_closed_set` first requires a real `--version`
  answer (`team-view.py <version>`). The capture above is of the tightened files.
- No test was skipped, xfailed, muted or retried to reach these readings.
