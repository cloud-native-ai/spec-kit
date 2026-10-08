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

## T009 red capture — 2026-10-08

Command: `scripts/bash/run-tests.sh tests/contract/test_teaching_surfaces.py`
Real output: `10 failed, 1 passed in 0.06s`. Red set: 5× retired-symlink-sentence present (agents.md source + 4 tool copies), 2× SKILL retired phrases present (source + mirror), trigger-truth absent ×2, team-scope absent, real-model absent. The single pass (identified in the -v run pasted above) is a legitimate pre-state green (a copy whose sentence form differs) — re-verified at T013 alongside the rest of the suite.

## T013 green + mutation drill — 2026-10-08

Green: `scripts/bash/run-tests.sh tests/contract/test_teaching_surfaces.py` → `11 passed in 0.02s` (mirror synced first: `sync-mirrors.py --write --only skills` → 1 file DIFF; `--check` all ok, no NEW drift vs 2026-10-08 baseline).
Loose-assertion fix en route (disclosed): test_c1 first used "real files" (incidentally green — the phrase pre-existed elsewhere); tightened to the distinctive fragment "renderer-produced real files", full-red confirmed (11 failed) before landing T010.
Mutation drill: plant `real filez` (1-char) in templates/commands/agents.md → guard RED on exactly test_c1_real_model_taught_in_agents_command (1 failed, 10 passed) → EXACT reverse substitution with count==1 asserted → `diff -q` vs pre-mutation copy BYTE-EQUAL → recovery re-run `11 passed`; the file's remaining `git diff` (2 insertions/2 deletions) is the T010 teaching edit itself, not the mutation.
