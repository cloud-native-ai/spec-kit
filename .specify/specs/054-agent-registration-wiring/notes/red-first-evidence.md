# Red-First Evidence — 054

Every guard: red output (command + exit status) at authoring time; green output after its subject lands; mutation drills (plant-err → red → restore → byte-equal).

## T004 red capture — 2026-10-08

Command: `scripts/bash/run-tests.sh tests/contract/test_render_trigger_cli.py`
Real output tail: `7 failed, 2 passed in 1.42s` — red set: c1_subcommand_exists_and_renders, c2_annotated_tool_rejected_with_legal_values, c4_empty_layers_is_legal_success, c5_placeholder_definition_rejected, c3_delegates_to_renderer_stats_summary, seat_c1_team_scope_key_accepted, seat_c1_team_scope_not_rendered.
2 greens today are incidental, kept deliberately because their post-implementation semantics stay correct: test_c2_unknown_tool_rejected (green now via "No such command" exit 2 — after T007 it must be green via the value-domain error; re-verified at T008) and test_seat_c1_unknown_key_still_rejected (pins EXISTING unknown-key rejection — regression net, not red-first, per the migration/regression exception).

## T008 green capture — 2026-10-08

Command: `scripts/bash/run-tests.sh tests/contract/test_render_trigger_cli.py`
Real output: `9 passed in 0.13s` — all 7 red tests green; 2 regression-net tests still green for the right reasons (test_c2_unknown_tool_rejected now green via the value-domain error listing legal values; test_seat_c1_unknown_key_still_rejected pins pre-existing behavior).

Mid-run failure attribution (recorded per discipline): 6 failures after first implementation were a HARNESS defect (python -m specify_cli — package has no __main__.py), fixed on the assertion side by switching to typer CliRunner; 1 failure (test_c5) was a SUBJECT gap vs contract C-5 (unhandled traceback instead of named error + exit 1), fixed on the subject side by catching AgentMetadataError in the subcommand.
