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
