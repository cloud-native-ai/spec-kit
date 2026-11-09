# Red-first evidence — Feature 094 goal/team parallel

Owner of the format: this file. Every red-first row appends one entry below the divider.
Each entry carries the row id, the date, the exact command, the real (unfiltered) output
excerpt, and the process exit status. A green reading that does not name the red reading it
replaced is not evidence (Constitution IV; `shared/workflows/feedback-step.md`).

## Entry format (copy this block; never invent a second shape)

```text
### <row id> — <subject>
- date: <YYYY-MM-DD>
- command: <the exact command line>
- exit status: <integer>
- output (verbatim excerpt):
  <real output, unfiltered by any post-processing except line selection>
```

---

<!-- Append new entries below this line, newest last. -->

### T005 — binding-record reader and the module's first red reading
- date: 2026-11-09
- command: `python3 -m pytest tests/contract/test_binding_model.py -q`
- exit status: 1
- output (verbatim excerpt):
```text
FAILED tests/contract/test_binding_model.py::test_a_definition_without_a_complete_binding_is_uninterpretable
FAILED tests/contract/test_binding_model.py::test_owner_outside_the_closed_three_values_is_refused
FAILED tests/contract/test_binding_model.py::test_owner_id_is_validated_by_shape_and_the_grammar_is_cited_not_restated
FAILED tests/contract/test_binding_model.py::test_origin_naming_a_non_existent_spec_directory_is_refused
FAILED tests/contract/test_binding_model.py::test_rebind_changes_only_the_binding_block
FAILED tests/contract/test_binding_model.py::test_a_hand_edited_binding_block_is_reported_not_trusted
FAILED tests/contract/test_binding_model.py::test_a_terminal_goal_refuses_a_new_team_binding
FAILED tests/contract/test_binding_model.py::test_ownership_is_answered_by_the_read_action_not_by_the_path
FAILED tests/contract/test_binding_model.py::test_scope_spec_is_removed_and_no_alias_exists
FAILED tests/contract/test_binding_model.py::test_both_archive_roots_resolve_in_one_call_and_auto_is_read_only
FAILED tests/contract/test_binding_model.py::test_a_cross_layer_write_is_refused_and_names_both_layers
FAILED tests/contract/test_binding_model.py::test_a_bound_goal_is_writable_only_by_human
12 failed in 0.63s
```
- full reading: `test-evidence/wp01-T005-red.txt`

### T028–T030, T035–T039, T041 — unified-archive migration module
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/contract/test_archive_migration.py -q`
- exit status: 1
- output (verbatim excerpt):
```text
FAILED tests/contract/test_archive_migration.py::test_a_conflict_names_both_candidates_and_never_overwrites
FAILED tests/contract/test_archive_migration.py::test_every_source_file_is_readable_under_trees_after_migration
FAILED tests/contract/test_archive_migration.py::test_the_receipt_carries_every_mandatory_field
FAILED tests/contract/test_archive_migration.py::test_a_binding_only_difference_is_not_a_conflict
FAILED tests/contract/test_archive_migration.py::test_migration_moves_the_tree_and_leaves_an_archive_not_delete_receipt
FAILED tests/contract/test_archive_migration.py::test_archive_and_migration_receipts_are_distinguishable_and_not_a_read_surface
FAILED tests/contract/test_archive_migration.py::test_origin_is_set_and_no_lineage_is_rebuilt
FAILED tests/contract/test_archive_migration.py::test_the_dry_run_writes_nothing_and_agrees_with_the_real_run
FAILED tests/contract/test_archive_migration.py::test_the_residual_probe_is_read_only_and_ignores_the_run_scratch_area
FAILED tests/contract/test_archive_migration.py::test_a_second_run_writes_nothing_and_is_a_noop
10 failed, 1 passed in 6.30s
```
- failure form: the engine's declared-option guard answers `error: unrecognized option: --apply|--dry-run` with exit 2, and the missing actions appear in the `--help` roster — the red is the absent action, not a test-side assumption. The single pass is `test_no_other_action_invokes_the_migration` (an inert regression guard until the action exists).
- full reading: `test-evidence/wp02-T028-red-archive-migration.txt`
- green reading: `test-evidence/wp02-green-archive-modules.txt`, `test-evidence/wp02-T028-green.txt` … `wp02-T041-green.txt`

### T031 / T040 — interrupted migration module
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/contract/test_migration_interruption.py -q`
- exit status: 1
- output (verbatim excerpt):
```text
FAILED tests/contract/test_migration_interruption.py::test_an_interrupted_run_reports_its_step_and_resumes_without_a_second_move
1 failed in 6.18s
```
- failure form: `assert 2 == 3` — the engine refused the undeclared `--apply` option at exit 2 instead of reporting an interruption at exit 3.
- full reading: `test-evidence/wp02-T031-red-interruption.txt`
- green reading: `test-evidence/wp02-T031-green.txt`, `wp02-T040-green.txt`

### T032 — real-tree-shape integration module
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/integration/test_archive_migration_real_data.py -q`
- exit status: 1
- output (verbatim excerpt):
```text
FAILED tests/integration/test_archive_migration_real_data.py::test_every_source_tree_stays_readable_after_migration
1 failed in 6.18s
```
- failure form: the probe subcommand was absent from the engine's `--help` roster (no JSON payload to compare against the fixture's residual counts).
- full reading: `test-evidence/wp02-T032-red-real-data.txt`
- green reading: `test-evidence/wp02-T032-green.txt`

### T081 / T082 — resident backfill module (red before T082 exists)
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/contract/test_resident_backfill.py -q`
- exit status: 1
- output (verbatim excerpt):
```text
FAILED tests/contract/test_resident_backfill.py::test_every_archive_resident_carries_a_binding_after_backfill
FAILED tests/contract/test_resident_backfill.py::test_a_second_backfill_writes_nothing_and_refuses_an_incomplete_binding
2 failed in 6.23s
```
- failure form: `error: unrecognized option: --dry-run` (exit 2) — the action did not exist.
- full reading: `test-evidence/wp02-T082-red-backfill.txt`
- green reading: `test-evidence/wp02-T081-green.txt`, `wp02-T082-green.txt`

### T042 — peer-lines contract module (guard rows T042, T045–T048)
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/contract/test_parallel_lines.py -q`
- exit status: 1
- output (verbatim excerpt):
```text
FAILED tests/contract/test_parallel_lines.py::test_authorize_records_the_archive_layer_not_a_scope_name
FAILED tests/contract/test_parallel_lines.py::test_neither_line_requires_the_other_to_exist
FAILED tests/contract/test_parallel_lines.py::test_run_checks_carries_the_binding_and_keeps_its_resolution_keys
FAILED tests/contract/test_parallel_lines.py::test_no_owner_is_derived_from_a_path_prefix
FAILED tests/contract/test_parallel_lines.py::test_many_teams_may_bind_one_goal_and_no_goal_content_is_copied
5 failed in 6.41s
```
- failure forms: `handoff-decision` had no declaration fact in the self-contained fixture; the authorize record carried `scope` instead of `archive_layer`; `run-checks` carried no `binding` key; the team mechanism still named a spec-local team store; `run-checks` accepted a team lifecycle outside active/archived.
- full reading: `test-evidence/wp05-T042-t045-t048-red.txt`

### T044 — injected-precondition mutation (the peer assertion is not blind)
- date: 2026-11-09
- command: `python3` drill script (recorded verbatim in the evidence file)
- exit status: 0 (the drill asserts the two readings below)
- output (verbatim):
```text
clean exit: 0 | verdict: ok
mutated exit: 2 | error: injected-requires-spec-line
MUTATION TURNS THE PEER-B PATH RED: yes
```
- reading: `test-evidence/wp05-T044-mutation.txt`

### T063–T065 — US5 guard readings
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/contract/test_binding_model.py -q` (14 passed, includes T063's `test_rebind_changes_only_the_binding_block`)
- T065 red reading: `test-evidence/wp05-T065-disposal-red.txt` (the recorded post-disposal reading did not exist yet)
- T066 mutation reading: `test-evidence/wp05-T066-mutations.txt` — a re-injected criterion phrase hits the scan predicate (`temporary-goal-team`), and a position-inferring engine mutant answers `human` where the record answers `command-run`.

### T064 / T069–T070 — criterion vocabulary scan turned green
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/contract/test_criterion_vocabulary_scan.py -q`
- exit status: 0
- output (verbatim excerpt):
```text
3 passed in 6.70s
```
- red reading (29 classification hits across seven surfaces) is reproduced in the module docstring and was re-measured at fork entry; the surfaces reworded are the wp05-owned ones plus `skills/internal/create-team/references/create-mode.md` (the sweep disclosed in `notes/implement-wp03.md` §5).

### T073 — framework-map rows (red → green)
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/contract/test_framework_map_archive_row.py -q`
- exit status (red): 1 — the Goals row still named `.specify/goal/<slug>/` and no archive row named `.specify/archive/goal-team/`; reading: `test-evidence/wp06-red-guards-2.txt`
- exit status (green): 0 — 1 passed (in the 9-guard run `test-evidence/wp06-green-guards-3.txt`)

### T074 — goal/team command templates (red → green)
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/contract/test_goal_command_template.py -q`
- exit status (red): 1 — the goal template exposed no `migrate-archive` mode and kept the spec-scoped positioning; the team template still named `<spec-dir>/team/`; reading: `test-evidence/wp06-red-guards-2.txt`
- exit status (green): 0 — 2 passed (same 9-guard reading)

### T075 — the three management skills (red → green)
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh "tests/contract/test_binding_model.py::test_the_three_management_skills_cite_owners_and_restate_no_arguments" -q`
- exit status (red): 1 — manage-goal and run-team still named `.specify/goal/`; manage-goal carried no `migrate-archive` mode and no archive-layer citation; reading: `test-evidence/wp06-red-guards-2.txt`
- exit status (green): 0 — 1 passed (same 9-guard reading)

### T076 / T077 — the write-path invariant and its mutation arms (red → green)
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh tests/contract/test_no_spec_local_writes.py -q`
- exit status (red): 1 — the sanitize template lacked the read-only residual reading; the two mutation arms already passed, proving the checkers catch a reverted surface; reading: `test-evidence/wp06-red-guards-2.txt`
- exit status (green): 0 — 4 passed (same 9-guard reading). Mutation arms: engine root reverted in memory → `ARCHIVE_DIRNAME` violation; create-mode persistence target reverted in memory → prose hit; re-injected `temporary goal` phrase → C-107 pattern hit.

### T078 — residual probe and the sanitize reading surface
- date: 2026-11-09
- command: `bash scripts/bash/run-tests.sh "tests/contract/test_archive_migration.py::test_the_residual_probe_is_read_only_and_ignores_the_run_scratch_area" -q`
- exit status: 0 — 1 passed (the engine half landed in wp02; the wp06 half is the sanitize template's read-only rendering, guarded by `test_no_spec_local_writes.py::test_the_sanitize_template_renders_the_probe_without_migrating`)
