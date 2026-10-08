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

## T014 red capture — 2026-10-08

Command: `scripts/bash/run-tests.sh tests/contract/test_seat_instantiation_flow.py`
Verdict: 6/6 red after marker tightening. First run was 5/6 red — test_c4 was incidentally green because its two markers ("create-agent", "team-scope") pre-exist in create-team SKILL.md ("team-scoped responsibility" at :17 substring-matches "team-scope"); disclosed and fixed on the assertion side by pinning the new step's distinctive name "seat instantiation" (count 0 pre-authoring), full-red confirmed. All markers absent: no seat-instantiation step, no render trigger, no failure-disclosure wording; create-mode schema note has neither team-scope nor the two-form member clause; improve-team has no backfill step; guidance line absent from both.

## T018 green + mutation drill — 2026-10-08

Green: `scripts/bash/run-tests.sh tests/contract/test_seat_instantiation_flow.py` → `6 passed in 0.02s` after T015 (create-team SKILL.md step 4 seat-instantiation + new step 7 render trigger with failure-disclosure + guidance line; create-mode.md step 4, new step 7, schema-note member-resolution clause rewritten) and T016 (improve-team new step 6 seat backfill + step 7 report distinguishing existing/backfilled/render-stats + guidance line); T017 mirror sync (3 files), `--check` all ok, no NEW drift vs baseline.
Mutation drill: plant `render-agentz` (1-char) in skills/create-team/SKILL.md → guard RED on exactly test_c8_create_team_create_flow_runs_render_trigger (1 failed, 5 passed) → EXACT reverse substitution count==1 → `diff -q` BYTE-EQUAL vs pre-mutation copy → mirror re-synced → recovery `6 passed`.

## T019 red capture — 2026-10-08

Command: `scripts/bash/run-tests.sh tests/contract/test_agent_surface_docs.py`
Verdict: 5/5 red (concept section absent from agent-definitions.md; provenance URLs + date absent from symlink-model.md; qoder agent-surface note absent from supported-agent-tools.md).

## T024 green + mutation drill — 2026-10-08

Green: `scripts/bash/run-tests.sh tests/contract/test_agent_surface_docs.py` → `5 passed in 0.02s` after T020 (agent-definitions.md gains `## Host Registration Surface` owner section + Seat Instance taxonomy entry), T021 (symlink-model.md agent-surface bullet with both provenance URLs + verification date + owner pointer), T022 (supported-agent-tools.md qoder agent-surface section — inserted mid-sentence on first attempt, caught by re-reading and relocated after the Tier 2 bullet, disclosed), T023 (shared mirror sync 2 files, `--check` all ok, no NEW drift).
Mutation drill: planted a C-8 violation (restated the `## Host Registration Surface` heading inside symlink-model.md) → guard RED on exactly test_c8_pointer_discipline_no_restatement (1 failed, 4 passed) → exact reverse restore → `diff -q` BYTE-EQUAL → mirror re-synced → recovery `5 passed`.

## T025–T027 aggregate guards + drills — 2026-10-08

T025 front-loaded closure (subjects landed in Phases 2/4; component reds captured at T004/T009/T014): `scripts/bash/run-tests.sh tests/contract/test_agent_chain_guards.py` → `4 passed in 0.10s` — chain closure (seat renders onto `.qoder/agents/` with tools/maxTurns + manifest entry), manifest↔definition correspondence (glob-derived, no hand list), foreign-file edge (user asset neither in manifest nor pruned by re-render).

T026 mutation drills (all plant → red → exact restore → byte-equal → green):
- CLI guard: `rendered `→`renderd` (1-char, src/specify_cli summary) → `2 failed, 7 passed` (test_c4 + test_c3) → restored → `9 passed`.
- Chain guard wiring: first attempt `seat instantiation`→`…instantiationz` did NOT go red — substring assertions are insensitive to suffix-append mutations (drill finding, disclosed); re-drilled with the deletion form `…instantiatio` → `1 failed, 3 passed` (test_c9) → restored → mirror re-synced → `10 passed` (both wiring files).
- C-10 correspondence: dropped layer prefix from source recording (`f"{layer}/{entry.name}"`→`f"{entry.name}"`) → `2 failed, 2 passed` (both correspondence tests) → restored count==1 → `diff -q` BYTE-EQUAL → chain guards + existing test_agent_render.py `19 passed` (no regression in the pre-existing suite).

T027 suite green: all five guard files in one run → see the line pasted at the top of this block.
