# Red-first evidence — WP-01a (T006–T015)

Run `r20261112T064607Z-b101`, feature `101-anchor-goal-realignment`, package WP-01a.
Every reading below is a command actually executed in this package; the E2 full-suite baseline
(`test-evidence/suite-baseline-entry.txt`: rc=1, 8900 passed, 192 pre-existing failure ids,
3 skipped) is the comparison point and was **not** re-run.

## T006 — the owner file changes hands through a rename

Task obligation: `git log --follow` readings for both definition files, written into this file.

Staged diff shape (before committing):

```text
$ git diff --cached --stat -M
 shared/definitions/{goal-definitions.md => anchor-definitions.md} | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
```

Post-commit detection (`git show --stat -M --oneline HEAD`):

```text
9d9043502 refactor(101): move the definition owner file from Goal to Anchor (T006)
 shared/definitions/{goal-definitions.md => anchor-definitions.md} | 0
 1 file changed, 0 insertions(+), 0 deletions(-)
 rename shared/definitions/{goal-definitions.md => anchor-definitions.md} (100%)
```

Pre-move blob of the Goal owner (the exact content the Anchor owner inherits and the Goal owner
is later rebuilt from, T008): `3e1c0a4f067915eb3928eb6de43737fb7e296ab9`
(`git rev-parse HEAD:shared/definitions/goal-definitions.md` on stage base `7920dc7b5`).

`git log --follow --oneline -- shared/definitions/anchor-definitions.md` (first ten rows):

```text
9d9043502 refactor(101): move the definition owner file from Goal to Anchor (T006)
8b9030371 refactor(layout): move the project anchors out of memory/ — .specify/{features,constitution,glossary,register,tools}.md + .specify/features/<NNN>-<slug>.md
91a69ed89 feat(094-wp05): peer lines, archive-layer routing and the US5 owner rewrites
377986b84 feat(093-wp3): T135 — target-concurrency paragraph in goal-definitions
8edd955d1 feat(090): anchor rename W1/W2 + 092 merge W3 (working set)
2cb68c446 feat(085): add temporary Goal/Team and stage-level concurrency
1adfa49ab feat(skill-layer-install-separation): internal/external skill layering + install split
1bc043780 feat(053-machine-decidable-artifacts): derive goal criterion subject sets from the repository instead of a retyped member list (Phase 7, US5)
b05209ee6 fix(goal): reject an empty criteria overwrite, add objective/title/boundaries, and label actions read vs write
236105385 feat(goal): add Target decomposition — run-assignable scope slices under Goal (038)
```

The chain reaches the authored history back to `a7fd58c7a finish analysis`; it is not a
"create mode 100644" first commit. `git log --follow` on the retired path
(`shared/definitions/goal-definitions.md`) reports the same chain terminating at the move commit,
which is the measured shape of "content changed owner, not content was rewritten".

Result: **PASS** — the rename is recorded with 100% similarity, and the old path has no second
live copy at this commit (T008 recreates the Goal owner as a new action-level file).

# Red-first evidence — WP-01b (T016–T025)

Run `r20261112T064607Z-b101`, package WP-01b, same E2 baseline
(`test-evidence/suite-baseline-entry.txt`, rc=1, 192 pre-existing failure ids) as the
comparison point; the full suite was **not** re-run.

## Red-before capture

`bash scripts/bash/run-tests.sh <14 modules from the WP-01a measurement> -q` →
`test-evidence/wp01b-red-before.txt`: **rc=1, 56 failed, 293 passed, 1 skipped**. The
count is unchanged from WP-01a because no test had yet been updated for the rename.

## Red → green after T025

Every reading below is a command actually executed through the project runner.

| Module | Red before | After | What the red was |
|---|---|---|---|
| `tests/contract/test_binding_model.py` | 14 | 0 | seeds at `anchoring/<slug>/goal.md` with `# Goal:`; retired `--scope goal`; owner tests pointed at the Goal owner |
| `tests/contract/test_scope_resolution.py` | 5 | 0 | `--scope goal`, old `Scope` API (`goal_root`), `list` answering for the anchor store |
| `tests/unit/test_goal_scope_engine.py` | 5 | 0 | old `Scope` API; `auto` naming a `goal` layer |
| `tests/contract/test_goal_targets_engine.py` | 13 | 0 | fixture path `anchoring/<slug>/goal.md` (incl. the mirror-parity case) |
| `tests/contract/test_goal_definition.py` | 1 | 0 | `create_goal` lands at `anchor.md` (`# Anchor:`) |
| `tests/unit/test_goal_utils.py` | 1 | 0 | heading `# Anchor:` (plus one path fixture) |
| `tests/contract/test_archive_migration.py` | 3 | 0 | migration target is `anchoring/<slug>/anchor.md`; conflict seeds at the live path |
| `tests/integration/test_goal_migration_path.py` | 1 | 0 | summary under `anchoring/<slug>/summary/`; `anchor_slug` payload key; non-equivalent target refusal is exit 4 |
| `tests/contract/test_script_interface_contract.py` | 3 | 0 | `sync-mirrors --check` drift (closed by T024), not by a test edit |
| `tests/contract/test_run_checks.py` | 9 | 3 | fixture `anchor.md` + `TOP_KEYS='anchor_slug'`; 3 remain (see below) |
| `tests/integration/test_archive_migration_real_data.py` | 1 | 1 | live tree awaits the applied migration (T049–T054) |
| `tests/contract/test_goal_targets_check.py` | 6 | 0 | same fixture path rename (module outside the 14-module capture) |
| `tests/contract/test_handoff_contract.py` | 1 | 0 | goal fixture seeded at `goal.md`; engine resolves `anchor.md` |
| `tests/contract/test_no_spec_local_writes.py` | 1 | 0 | the engine's docstring action table lacked the goal-* / `cleanup` write rows; added, and the module's pinned write set grew to match the parser |

Final targeted reading (22 modules):
`429 passed, 6 failed, 2 skipped, rc=1`.

## The 6 remaining reds and their owners

| Failure id | Class |
|---|---|
| `test_run_checks.py::test_c1_the_action_exists_and_the_roster_grew_by_exactly_one` | E2 baseline (line 91) — pre-existing |
| `test_script_interface_contract.py::test_c26_generator_skill_carries_the_mandate_entry` | E2 baseline (line 92) — pre-existing |
| `test_goal_migration.py::TestLiveSurfacesAreMigrated::test_no_live_face_file_retains_the_old_path` | E2 baseline (line 56) — pre-existing |
| `test_run_checks.py::test_c20_the_existing_zero_and_two_branches_still_hold` | live tree awaits the applied migration — T049–T054 |
| `test_run_checks.py::test_the_real_bound_team_reports_the_measured_state` | live tree awaits the applied migration — T049–T054 |
| `test_archive_migration_real_data.py::test_every_source_tree_stays_readable_after_migration` | live tree awaits the applied migration — T049–T054 |

No rename-caused red remains in this package's reach; the three live-tree cases turn green only
after the real `.specify/anchoring/*/goal.md` definitions are migrated by T049–T054.

## WP-02 (T026–T034) — command-surface rename

Pre-edit capture (`test-evidence/wp02-before-names.txt`, 28 candidate modules):
`26 failed, 1774 passed, 1 skipped`. Every one of the 26 id is present in the E2 baseline
recorded by WP-01b, so any id that appears only afterwards is attributable to this package.

Post-edit capture (`test-evidence/wp02-after-final-names.txt`, the 13 modules this package
touches): `15 failed, 525 passed`. Difference against the pre-edit capture over the same
modules: **16 new ids, 10 closed in-package, 6 still owned elsewhere**.

### Closed in-package (10)

| Failure id | What the red was | Closure |
|---|---|---|
| `test_expression_compatibility.py::test_c1_zero_new_commands` | frozen roster 31 | 31 → 32, `/speckit.anchor` enumerated as sanctioned (FR-010) |
| `test_expression_compatibility.py::test_c1_skill_inventory_is_frozen` | frozen roster 58 | 58 → 59, `internal/manage-anchor` enumerated (FR-012) |
| `test_migration_distribution.py::test_command_template_name_set_matches_frozen_baseline` | shipped command set 31 | 31 → 32 |
| `test_migration_distribution.py::test_skill_name_set_matches_frozen_baseline` | shipped skill set 58 | 58 → 59 |
| `test_skill_layer_visibility_guards.py::test_flat_discovery_surfaces_external_layer_only` | internal nested count 40 | 40 → 41 |
| `test_run_skills_wiring.py::test_c12_no_duplicate_semantic_skill_dirs` | internal dir roster | `manage-anchor` added to `BASELINE_INTERNAL` |
| `test_humanize_command_surface.py::test_wc16_command_roster_unchanged` | 062 roster pin 31 | 31 → 32, `anchor.md` sanctioned |
| `test_goal_command_template.py::test_the_goal_template_exposes_migrate_archive_and_cites_the_scope_domain` | pinned the 094 `migrate-archive`/scope obligation on the Goal template | retargeted to `templates/commands/anchor.md` (renamed `…anchor_template…`); the Goal hint is now pinned to exactly the four modes |
| `test_goal_targets_engine.py::test_targets_mode_row_is_documented` | pinned the Targets row on `manage-goal` | retargeted to `manage-anchor` **and** asserts `manage-goal` carries no Targets row (FR-022) |
| `test_goal_targets_engine.py::test_engine_invocation_examples_cover_the_targets_action_group` | `targets <goal-slug>` examples | retargeted to `targets <anchor-slug>` in the anchor skill |

### New ids still owned elsewhere (6)

| Failure id | Owner | Why it cannot close here |
|---|---|---|
| `test_flow_class_ledger.py::test_check_reports_79_units_and_zero_gaps` | T039 | the ledger is `shared/definitions/flow-class-definitions.md`; its counts move with the ledger rows in the same change (C-9) |
| `test_flow_class_ledger.py::test_ledger_has_79_rows_covering_inventory_bidirectionally` | T039 | same |
| `test_flow_class_ledger.py::test_templates_and_skills_never_assign_class_key` | T039 | same module, file-count pin 89 → 91 measured against the same ledger inventory |
| `test_run_skills_wiring.py::test_c9_compile_embeds_zero_drift_75_units` | T040 | `templates/commands/anchor.md` carries the reserved empty `## Wrap-up`; the census reads 85 units and the compile drifts until T040 compiles it |
| `test_compile_propagation_order.py::test_propagation_chain_is_green_in_canonical_order` | T040 | same: step 1 (`compile-embeds --check`) reports drift in 1 of 85 units — `/speckit.anchor` |
| `test_feedback_command_classification.py::test_table_covers_every_command_template` | **decision — see ANOMALY** | the table is parsed from `.specify/specs/027-feedback-mechanism/contracts/command-classification.md`, which FR-061/FR-069 protect byte-for-byte; the test has no sanctioned-addition register, so adding `anchor.md` cannot be absorbed without touching a protected dated spec directory or weakening the global-coverage assertion |

### Pre-existing reds unchanged (9)

`test_expression_compatibility.py::test_c5_wiring_surface_is_closed` (offender
`templates/commands/feedback.md -> flow-class-check.py`), `…::test_c5_non_wiring_files_keep_their_frozen_hashes`
(the 069a dated hash manifest file is absent from the tree), `…::test_c6_feedback_step_edit_is_additive_single_line`,
`test_humanize_command_surface.py::test_c06_registry_rows_resolve` (`.specify/memory/features/062.md` absent),
`…::test_wc07_skill_body_budget`, `…::test_wc10_feature_062_status_held`, `…::test_wc11_feature_row_name_description`,
`…::test_wc13_stage_class_pin_remeasured`, `test_qoder_command_frontmatter.py::test_every_template_has_short_description`
(`research.md`, 78 chars) — all present verbatim in the pre-edit capture / E2 baseline.

## WP-02b (classification live overlay) — decision repair

Same 13-module set, same runner. Pre-edit (red-first): **rc=1, 15 failed, 525 passed**
(reproduces the WP-02 reading id-for-id). Post-edit: **rc=1, 16 failed, 525 passed**;
classification module alone: **2 failed, 34 passed**.

- closed: `test_feedback_command_classification.py::test_table_covers_every_command_template`
  (the WP-02 decision red).
- new: `::test_complex_command_carries_feedback_step[anchor]` and
  `::test_complex_set_equals_measured_feedback_carriers` — the anchor feedback-face
  assertions, T040-owned until the compiled face lands.
- nothing else moved. Full record: `test-evidence/implement-wp02b.md`.

## WP-03 (T035–T047) — live-surface convergence, mirrors, red-first test updates

Red-first captures taken with `bash scripts/bash/run-tests.sh` before each correction.

### Pre-edit (red) readings

| Module / batch | Reading | Red ids |
|---|---|---|
| `tests/contract/test_team_command_routing.py` | 1 failed, 31 passed | `::test_goal_md_zero_write_red_line_is_stated` — `goal.md write-face rule missing` (create-team `references/goal.md` rewritten to `anchor.md`) |
| framework-map + setup + criterion + flow-class + glossary + declaration + reference-matrix batch | 6 failed, 52 passed | `test_framework_map_archive_row.py::test_the_framework_map_names_the_unified_archive_and_drops_spec_local_goal_team` (no `Goals` row); `test_flow_class_ledger.py::{test_ledger_has_79_rows_covering_inventory_bidirectionally,test_templates_and_skills_never_assign_class_key,test_check_reports_79_units_and_zero_gaps}` (89 vs 91); `test_sdd_project_setup_skill.py::test_no_sdd_stage_advancement_and_bootstrap_command_set` (pin `constitution/feature/docs/goal/agents/team`); `test_criterion_vocabulary_scan.py::test_no_runtime_surface_uses_temporary_or_global_as_a_criterion` (6 hits incl. 5 in the renamed `anchor-definitions.md`) |
| handoff batch (`test_handoff_contract.py` + `test_handoff_territory.py` + `tests/integration/test_goal_reference.py`) | 9 failed, 3 passed; 5 of the 9 are E2 baseline (`test_goal_reference.py` lines 137–141) | 4 package-caused: `::test_the_contract_carries_its_eight_sections_in_order` (`goal_slug` missing), `::test_the_three_way_keys_resolve_in_both_directions` (`KeyError: 'goal_slug'`), `::test_the_contract_cites_and_never_copies_task_rows` (`## Goal` cites `anchor_slug`), `::test_a_dangling_handoff_key_is_refused_at_creation` (engine rc 2, `goal_slug ''` unresolved) |
| probe batch (`test_run_skills_wiring.py` + `test_compile_propagation_order.py` + `test_feedback_command_classification.py`) | 3 failed, 45 passed | `compile-embeds` drift in 85/85 units (registry fingerprint moved after WP-02's registry edit; `templates/commands/anchor.md` carried only the reserved empty `## Wrap-up`); `test_c9_compile_embeds_zero_drift_75_units` pinned `84 units`, engine reported 85 after recompile |
| `test_non_disposable_check.py` | 4 failed | all four ids are E2 baseline lines 80–83 — untouched |
| `test_shared_reference_rewrite.py` | 2 failed | both ids are E2 baseline lines 96–97 — untouched |
| `test_criterion_vocabulary_scan.py` after the owner-file exemption update | 1 failed | same baseline id; residual 2 hits are the pre-existing `skills/external/sdd-loop-driver/references/decomposition-model.md:362,369` |

### Post-edit (green) readings

- `test_team_command_routing.py` + `test_handoff_contract.py` + `test_handoff_territory.py` + `test_sdd_house_keeping_skill.py` + `test_feedback_step_reference_form.py`: **316 passed**.
- `test_run_skills_wiring.py` + `test_compile_propagation_order.py` + `test_feedback_command_classification.py`: **48 passed**.
- `test_criterion_vocabulary_scan.py`: 2 passed, 1 failed (baseline id only; 6 hits → 2 pre-existing hits).
- Consolidated 20-module reading: **12 failed, 591 passed**, and every one of the 12 ids is present in `test-evidence/suite-baseline-entry.txt` (4 × `test_non_disposable_check.py`, 2 × `test_shared_reference_rewrite.py`, 5 × `tests/integration/test_goal_reference.py`, 1 × `test_criterion_vocabulary_scan.py`). No new id outside the E2 baseline.

### Updated surfaces (T047)

1. `tests/contract/test_framework_map_archive_row.py` — rows retargeted to `Anchor archive` / `Goal archive` / `Team archive` / `Anchor archive destination`, asserting `.specify/anchoring/<slug>/`, `.specify/goals/<slug>/`, `.specify/teams/<slug>/`, `.specify/archive/anchoring/<slug>/` and the absence of the retired singular `.specify/goal/`.
2. `tests/contract/test_sdd_project_setup_skill.py` — command-set pin `constitution/feature/docs/goal/agents/team` → `constitution/feature/docs/anchor/goal/agents/team`.
3. `tests/contract/test_flow_class_ledger.py` — four pins 89 → 91 and composition 31+58 → 32+59 (`/speckit.anchor` + `skill:manage-anchor`), with dated stale-pin notes.
4. `tests/contract/test_run_skills_wiring.py` — compile census pin 84 → 85 units (`templates/commands/anchor.md` now carries its compiled face).
5. `tests/contract/test_team_command_routing.py` — zero-write red line retargeted from `goal.md` to `anchor.md` (reference filename unchanged).
6. `tests/contract/test_criterion_vocabulary_scan.py` — historical-record exemption widened to the renamed owner pair (`goal-definitions.md` + `anchor-definitions.md`); the baseline id stays red on its pre-existing `decomposition-model.md` hits, status unchanged.

## WP-05 (T061–T077) — guards G-1…G-10, red-first and injection

Every guard was shown able to fail: the subject was broken in an isolated scratch tree and the guard was
run through `bash scripts/bash/run-tests.sh` with `SPECKIT_GUARD_ROOT` pointing at it. The scratch is a
full copy of the working tree under `.specify/.tmp/wp05/rf` (a nested `git init` was added for the
git-hash guard); each mutation was reverted by copying the original file back.

| Guard | Mutation (broken subject) | Red ids observed | Evidence |
|---|---|---|---|
| G-1 / T062 | `templates/commands/anchor.md` `argument-hint` loses `coordinate` | `::test_hint_declares_exactly_the_seven_modes`, `::test_generated_copies_carry_the_inherited_positioning` | `test-evidence/wp05-redfirst-g1.txt` |
| G-2 / T063 | `templates/commands/goal.md` hint adds `targets` | `::test_goal_hint_declares_the_four_goal_modes`, `::test_anchor_only_modes_are_refused_by_the_subprocess_action` (the guard cross-checks hint vs engine refusal) | `test-evidence/wp05-redfirst-g2.txt` |
| G-3 / T064 | delete `.specify/anchoring/086-efficient-test-execution/anchor.md` | `::test_live_anchor_store_is_converged`, `::test_every_anchor_definition_is_non_empty_and_titled` | `test-evidence/wp05-redfirst-g3.txt` |
| G-4 / T065 | no root hook (module audits `REPO_ROOT` directly); red path exercised by the module's own injections | `::test_injection_out_of_engine_definition_write_is_red`, `::test_injection_derived_writer_escape_is_red` (pass in the final run) | `test-evidence/implement-wp05-targeted-tests.txt` |
| G-5 / T066 | insert `goal_slug: draw-two-layer-structure` into `.specify/teams/draw-two-layer-structure/team.md` frontmatter | `::test_live_bindings_are_converged`, `::test_live_teams_carry_no_old_binding_key` | `test-evidence/wp05-redfirst-g5.txt` |
| G-6 / T067 | append `A goal is a project-level objective.` to `docs/reference/commands/anchor.md` | `::test_live_tree_has_no_old_semantic_residue` (C1) | `test-evidence/wp05-redfirst-g6.txt` |
| G-7a / T068 | second-apply no-op / receipt set / digest / target set | `::test_a_duplicate_receipt_turns_the_guard_red`, `::test_a_mismatched_digest_turns_the_guard_red`, `::test_a_dropped_target_turns_the_guard_red` (in-suite injections, real engine) | `test-evidence/implement-wp05-targeted-tests.txt` |
| G-7b / T069 | phase faults `GOAL_UTILS_CLEANUP_FAULT_AFTER=write-target|write-receipt`, receipt-less target | the three tests themselves assert the interrupted / resumed / I5 half-state behaviour, each with a real engine subprocess | `test-evidence/implement-wp05-targeted-tests.txt` |
| G-8 / T070 | append a byte to `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` in the isolated git scratch | `::test_every_baseline_protected_path_is_unchanged_and_present` (`protected paths changed: [...smoke-081.txt]`) | `test-evidence/wp05-redfirst-g8.txt` |
| G-9 / T071 | delete `tests/fixtures/…/pre-convergence/.specify/anchoring/draw-two-layer-structure/goal.md` | `::test_the_fixture_tree_converges` (apply exits nonzero on the missing definition) | `test-evidence/wp05-redfirst-g9.txt` |
| G-10 / T072 | drop the `| /speckit.anchor |` row from `shared/definitions/flow-class-definitions.md` | `::test_ledger_carries_both_command_rows`, `::test_command_family_answers_per_definition_layer[anchor]` | `test-evidence/wp05-redfirst-g10.txt` |

Two first attempts were inconclusive and are disclosed rather than hidden: (a) mutating the protected
path under `SPECKIT_GUARD_ROOT` first stayed green because `git hash-object --stdin-paths` resolves paths
against the enclosing repository root, so the guard read the live file — fixed by giving the scratch its
own `git init`; (b) setting a dangling `goal_slug` inside the pre-convergence fixture stayed green because
the cleanup's binding rename rewrites the value from the classification, so the mutation was overwritten —
the definition-deletion mutation above is the red path.
