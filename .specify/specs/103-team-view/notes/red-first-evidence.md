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

## US2 segment — overview (T022)

- Captured: 2026-11-24 (package 3, before the overview implementation landed)
- Command (unique entry; stdout+stderr redirected whole, no pipeline):
  `bash scripts/bash/run-tests.sh tests/integration/test_team_view_program.py tests/contract/test_team_view_program_contract.py -q`
- rc: **1** · summary: **3 failed, 27 passed in 6.51s**
- Full capture: `.specify/.tmp/us2-red.out` (stage-local; not committed)

| New test | Red shape | Decisive excerpt (verbatim) |
|----------|-----------|-----------------------------|
| `tests/integration/test_team_view_program.py::TestOverview::test_overview_lists_two_teams_sorted_with_seven_fields` | the no-slug path is not implemented | `NotImplementedError: overview extraction and rendering land with US2` |
| `tests/integration/test_team_view_program.py::TestOverview::test_empty_archive_reports_no_teams_found` | same | `assert 1 == 0` on the subprocess returncode with the same traceback |
| `tests/contract/test_team_view_program_contract.py::TestOverviewEnvelope::test_overview_envelope_carries_mode_sorting_and_counts` | same | `NotImplementedError: overview extraction and rendering land with US2` |

The reds are attributable to the subject being absent (the overview branch raises by
design), not to fragile assertions: every existing US1 test in the same two files passed
(27 passed), so the new failures are exactly the three US2 rows.

## US3 segment — routing, docs and per-tool copies (T027)

- Captured: 2026-11-24 (package 3, before the routing flow / docs page / copy regeneration landed)
- Command (unique entry; stdout+stderr redirected whole, no pipeline):
  `bash scripts/bash/run-tests.sh tests/contract/test_team_view_command.py -q`
- rc: **1** · summary: **16 failed, 22 passed in 6.27s**
- Full capture: `.specify/.tmp/us3-red.out` (stage-local; not committed)

| Red group | Tests | Decisive excerpt (verbatim) |
|-----------|-------|-----------------------------|
| routing flow (`TestNoGuessRouting`) | 2 failed | no `view → view-team` routing step; no view+`--target` conflict line in the routing flow |
| ambiguous input (`TestRoutingSamples`) | 1 failed | `ambiguous capability list lacks view` / no `MUST NOT execute any mode` line |
| default behavior (`TestDefaultBehaviorModes`) | 1 failed | `default-behavior summary lacks` the fourth mode; summary still says "three modes" |
| docs page (`TestDocsPage`) | 5 failed | `AssertionError: missing heading: ## View Mode`; docs still `exposes **exactly three modes**` |
| docs run drift (`TestDocsRunDrift`) | 2 failed | run row still delegates to `create-team` (execution path); the three false-claim literals still present |
| docs mode counts (`TestNamedFilesModeCounts[docs]`) | 1 failed | `'exactly three modes'` still in the docs page |
| per-tool copies (`TestPerToolCopies`) | 4 failed | each of the four copies still carries `exactly three modes` |

The passing 22 are the US1 wiring assertions (`C-01`/`C-02`/`C-06`/`C-11` segments) plus the
template-side mode-count row — the template already carries four modes from T016, so the
US3 reds are exactly the not-yet-synchronised surfaces (routing steps, default/ambiguous
lists, docs page, four generated copies).

## US4 segment — error-path navigation (T033)

- Captured: 2026-11-24 (package 4, before the not-found navigation and the corrupt overview
  row landed)
- Command (unique entry; stdout+stderr redirected whole, no pipeline):
  `bash scripts/bash/run-tests.sh tests/integration/test_team_view_program.py -q`
- rc: **1** · summary: **4 failed, 15 passed in 6.47s**
- Full capture: `.specify/.tmp/us4-red.out` (stage-local; not committed)

| New test | Red shape | Decisive excerpt (verbatim) |
|----------|-----------|-----------------------------|
| `TestErrorPaths::test_unknown_slug_reports_not_found` | the not-found path prints only the shared string; no available-slug list, no create suggestion | `assert '- alpha-team' in 'team not found: no-such-team\n'` |
| `TestErrorPaths::test_unknown_slug_in_empty_archive_reports_no_teams_found` | empty archive leg lacks [[STR-002]] and the create suggestion | `'No teams found' not in 'team not found: no-such-team\n'` |
| `TestErrorPaths::test_unknown_slug_list_is_bounded_with_omitted_count` | no bounded list, therefore no omitted count | `assert '省略 1' in 'team not found: no-such-team\n'` |
| `TestErrorPaths::test_overview_lists_every_team_sorted` | the overview drops the corrupt directory instead of labelling its row | `AssertionError: overview skipped row broken-team` |

The two remaining new tests pass because the behaviour they pin already landed with US1:
`test_corrupt_definition_is_not_not_found` (single-mode exit 4 + named path + no six-group
body, built in T010/T013) and `test_near_miss_slug_does_not_match` (exact-directory
resolution, built in T010). Their green is a truthfully recorded reading, not a red claimed
as such; the four reds above are exactly the surfaces T034 still owes.
