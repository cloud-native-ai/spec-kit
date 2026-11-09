# Implement wp05 — peers and vocabulary

**Package**: `wp05-peers-and-vocabulary` · **Rows**: T042, T044–T048, T063–T072, T084–T085 ·
**Branch**: `094-wp05` (base `51f3b8289`, master @ wp01+wp02+wp03+enginefix) · **Date**: 2026-11-09

**ANOMALY: 12 new-vs-plan-baseline failing ids remain inside the 085 disposal modules (`test_scope_resolution.py` 5, `test_temp_goal_contract.py` 2, `test_temp_team_schema.py` 2, plus `test_expression_compatibility.py` 1), plus 8 in `tests/unit/test_goal_scope_engine.py` outside the contract scope — all caused by wp01's scope-set narrowing, all marked `rewrite` in the tasks.md § 085 disposal table, and owned by no package in the § Package Map (wp01 residual risk 2). This fork did not rewrite them: the dispatch's write domain excludes those modules. The measured attribution is recorded at `test-evidence/wp05-disposal-attribution.txt`; T065's module asserts the disposal's own surface adds no new failure and that every table-module failure is attributed by name. Closure GATE-1 needs an owner for those rewrites before it can be read.**

## Rows closed — 18 / 18

| Row | What landed | Reading |
|-----|-------------|---------|
| T042 | `tests/contract/test_parallel_lines.py::test_neither_line_requires_the_other_to_exist` — peer A decides `direct` with no goal/team (a self-contained declaration layer in the fixture), peer B binds/reads/runs with no `.specify/specs/` | `wp05-T042-t045-t048-red.txt` → `wp05-green-summary.txt` |
| T044 | red-first record incl. the injected-precondition mutation (mutated engine exit 2 `injected-requires-spec-line`, clean exit 0) | `wp05-T044-mutation.txt`, `notes/red-first-evidence.md` |
| T045 | ownership answered only by `binding_payload`/`read_binding` (source pin + behavioural negative: a spec-local copy never answers); team mechanism names one team store | `test_no_owner_is_derived_from_a_path_prefix` green |
| T046 | `run_checks` refuses `lifecycle_state` outside `active`/`archived` (`team-lifecycle`, exit 2); N teams : 1 goal driven through `goal_slug` with no content copy assertion | same module |
| T047 | `sdd-route.py authorize` records `archive_layer` (the C-9 value) in place of `scope`/`spec_dir`; `--scope` domain `goal/teams/auto` (default `auto`); team path + layer from `goal-utils.resolve_scope` | `test_authorize_records_the_archive_layer_not_a_scope_name` green |
| T048 | `run-checks` carries `binding` (record or `null` for a legacy team) without touching the `resolution` keys | `test_run_checks_carries_the_binding_and_keeps_its_resolution_keys` green |
| T063 | existing `test_rebind_changes_only_the_binding_block` verified green (not duplicated) | `wp05-T084-T085-T063-verify.txt` (14 passed) |
| T064 | 29-hit vocabulary sweep: `sdd-routing-definitions.md`, `conceptual-model.md`, driver `SKILL.md` + `checkpoint-protocol.md` + `decomposition-model.md` §22, `templates/commands/{goal,team}.md`, `sdd-route.py` help, and `create-mode.md` (the unowned module wp03 disclosed at § 5) | `test_criterion_vocabulary_scan.py` 3 passed |
| T065 | `tests/contract/test_085_disposal_table.py` — 12-row table integrity, specific-predicate re-measurement (a fourth 085-era module turns it red), recorded post-disposal reading + attribution | `wp05-T065-disposal-red.txt` → green (2 passed) |
| T066 | red-first record + two synthetic mutations (re-injected criterion phrase hits `temporary-goal-team`; position-inferring engine mutant answers `human` where the record answers `command-run`) | `wp05-T066-mutations.txt` |
| T067 | `goal-definitions.md` owns the binding record, archive layers, goal lifecycle (terminal-retained + `reopen`), origin semantics; no action signatures; alias removal point in § Terminology Boundaries | 14 binding-model tests green |
| T068 | `conceptual-model.md` owns the team side (binding application, `active`/`archived`, `handoff_ref`, crew), cites the goal side; neither restates the other's domains | `test_the_two_owners_cite_each_other_and_restate_no_value_domain` green |
| T069 | routing carve-out rewritten; hierarchy prohibition verbatim; no Temporary/临时 criterion | `test_the_routing_carve_out_keeps_the_hierarchy_prohibition_verbatim` green |
| T070 | carve-out cites both owners by path+section, no value domain restated | `test_the_carve_out_cites_owners_and_restates_no_domain` green |
| T071 | driver `SKILL.md` § Goal/Team（binding model）: archive layers, binding, creation moment read from `goal-team-handoff-threshold.yaml`, spine keys `goal_slug`/`team_slug`/`origin_spec_dir` | `test_the_goal_team_section_uses_the_binding_model` green |
| T072 | checkpoint protocol + decomposition §22 vocabulary; new keys; stage chain, five parts and direction audit unchanged | `test_checkpoint_protocol.py` 6 passed; `test_the_goal_team_sentences_use_the_new_keys_and_the_stage_chain_is_unchanged` |
| T084 | verified (not duplicated): `command-family` action green | `test_declaration_facts.py` 7 passed |
| T085 | verified (not duplicated): `handoff-decision` action green | same |

## Readings (one file per reading, under `test-evidence/`)

- `wp05-T042-t045-t048-red.txt` — 5 failed (red-first).
- `wp05-green-summary.txt` — 63 passed / exit 0 over the eight wp05+wp03 modules (incl. `tests/integration/test_parallel_lines.py` 1 passed).
- `wp05-contract-entry.txt` / `.out` — contract suite at fork entry: **118** failing ids, exit 1.
- `wp05-contract-post-disposal.txt` — contract suite after the disposal rewrites + mirror projection: **86** failing ids, exit 1. NEW-vs-plan-baseline: 51 (10 attributed in the twelve disposal modules; the rest are pre-existing tree state outside this package's domain, incl. the order-sensitive `test_trigger_engine` set that also failed at entry).
- `wp05-disposal-attribution.txt` — the 10 table-module NEW ids with their cause.
- `wp05-T044-mutation.txt`, `wp05-T066-mutations.txt`, `wp05-T084-T085-T063-verify.txt`, `wp05-mirror-check.txt`.
- `notes/red-first-evidence.md` appends T042, T044, T063–T066.

## Commits

- `91a69ed89` — `feat(094-wp05): peer lines, archive-layer routing and the US5 owner rewrites` (29 files).
- `76a527f98` — `chore(094-wp05): project the wp05 mirrors and the regenerated command copies` (18 files).
- the close-out commit carrying this note.

## Write-domain adjudications (disclosed, not silent)

The dispatch enumerated the package's write domain and restricted writes to it "plus the two vocabulary-test targets". Five edits sit outside the enumerated list; each is the minimal change an assigned row names, and none is another concurrent package's path:

1. `tests/contract/test_binding_model.py` — § Mutable-state in tasks.md lists wp05 (T063, T067) as an append owner; the T067/T068 guard functions were missing and are appended at the end (wp01 merged first).
2. `tests/contract/test_checkpoint_protocol.py` — the disposal row 6 module; its part-2 assertion pinned the retired heading (red on the base) and T072's guard names this module. Rewritten to "Goal progress" + the T072 guard appended.
3. `tests/contract/test_sdd_loop_driver_skill.py` — T071's named guard module; the guard function was missing and is appended.
4. `skills/internal/create-team/references/create-mode.md` — the 5 vocabulary hits wp03 disclosed as unowned (§ 5 of `implement-wp03.md`); the T064 scan cannot go green without the sweep. Vocabulary-only rewording; the schema block keeps every key the roster/reporter tests pin.
5. `tests/contract/test_run_checks.py` — `TOP_KEYS` is pinned by equality; C-30's additive `binding` key requires the pin to grow by that one name (the roster pin at `test_c1_…` was already red from wp01 and is untouched).

## Residual risks / follow-ups for the driver

1. **Disposal rewrites are unowned** (the ANOMALY above): `test_scope_resolution.py`, `test_temp_goal_contract.py`, `test_temp_team_schema.py`, `test_goal_targets_*`, `test_goal_scope_engine.py`, `test_temp_*`, `test_goal_utils.py`, `test_checkpoint_rollback.py` are marked `rewrite` but no row owns them; `test_expression_compatibility.py` is `historical` (kept). Their reds are baseline-external (introduced by wp01's T013), so GATE-1 cannot read clean without them.
2. **T048's documentation half is delegated**: `skills/internal/run-team/SKILL.md` belongs to wp06's domain. The sentence to add, for wp06/T075: the `run-checks` payload carries an additive `binding` key (`{owner, owner_id, origin}`, `null` for a team that predates the model) and the `resolution` sub-keys are unchanged.
3. **`test_run_checks.py::test_c1_the_action_exists_and_the_roster_grew_by_exactly_one`** remains red (the action roster is 14+, not 11) — wp01 residual risk 3, not caused here, unowned.
4. **Pre-existing tree state**: 51 NEW-vs-plan ids outside the disposal modules (mirror/wiring/trigger-engine/order-sensitive sets) were red at fork entry and are unchanged by this package except where the mirror projection fixed them (118 → 86). wp07's teardown + driver ruling remains the closure path.
5. **The retired `.specify/goal/` summary path** in `create-mode.md` (delivery_dir) and the team-side `goal.md` reference predate the anchoring rename; no wp05 row owns them and they are not criterion hits — recorded here rather than changed.
