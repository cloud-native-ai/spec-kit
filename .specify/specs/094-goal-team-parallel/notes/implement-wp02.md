# Implement report — wp02-archive-migration (094-goal-team-parallel)

Package: `wp02-archive-migration`, rows T028–T041 and T081–T083
Tree: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/094-wp02`
(branch `094-wp02`, based on `master` which contains wp01)
Date: 2026-11-09
Write domain used: `scripts/python/goal-utils.py` (migrate-archive + probe-residual +
resident-backfill sections), `tests/contract/{test_archive_migration,test_migration_interruption,test_resident_backfill}.py`,
`tests/integration/test_archive_migration_real_data.py`, `notes/`, `test-evidence/`, and the T083
row's own declared action (the 18 resident definitions under `.specify/anchoring/` and
`.specify/teams/`). Nothing else was edited; `shared/declarations/contract.yaml`, all other
packages' paths and `templates/commands/sanitize.md` were not touched.

## Per-row closure

| Row | Status | Evidence |
|-----|--------|----------|
| T028 | closed | red `test-evidence/wp02-T028-red-archive-migration.txt` (10F/1P), green `wp02-T028-green.txt`; guard `test_archive_migration.py::test_migration_moves_the_tree_and_leaves_an_archive_not_delete_receipt`; engine section "unified archive: migration, residual probe, resident backfill" |
| T029 | closed | `wp02-T029-green.txt`; guard `test_a_second_run_writes_nothing_and_is_a_noop` |
| T030 | closed | `wp02-T030-green.txt`; guard `test_a_conflict_names_both_candidates_and_never_overwrites` |
| T031 | closed | red `wp02-T031-red-interruption.txt` (1F), green `wp02-T031-green.txt`; guard `test_migration_interruption.py::test_an_interrupted_run_reports_its_step_and_resumes_without_a_second_move` |
| T032 | closed | red `wp02-T032-red-real-data.txt` (1F), green `wp02-T032-green.txt`; guard `test_archive_migration_real_data.py::test_every_source_tree_stays_readable_after_migration` |
| T033 | closed | `notes/red-first-evidence.md` § T028–T030/T035–T039/T041, T031/T040, T032, T081/T082; the four red readings under `test-evidence/wp02-*-red-*.txt` |
| T034 | closed | `wp02-T034-green.txt` (same guard as T028); `migrate_archive` action in `goal-utils.py` |
| T035 | closed | `wp02-T035-green.txt`; guard `test_the_receipt_carries_every_mandatory_field` |
| T036 | closed | `wp02-T036-green.txt`; guard `test_archive_and_migration_receipts_are_distinguishable_and_not_a_read_surface` |
| T037 | closed | `wp02-T037-green.txt`; guard `test_origin_is_set_and_no_lineage_is_rebuilt` |
| T038 | closed | `wp02-T038-green.txt`; guard `test_every_source_file_is_readable_under_trees_after_migration` |
| T039 | closed | `wp02-T039-green.txt`; guard `test_a_second_run_writes_nothing_and_is_a_noop` |
| T040 | closed | `wp02-T040-green.txt`; interrupted/resume path in `goal-utils.py` |
| T041 | closed | `wp02-T041-green.txt`; guard `test_the_dry_run_writes_nothing_and_agrees_with_the_real_run` |
| T081 | closed | `wp02-T081-green.txt`; guard `test_resident_backfill.py::test_every_archive_resident_carries_a_binding_after_backfill` (mutation over a fixture copy turns it red) |
| T082 | closed | red `wp02-T082-red-backfill.txt` (2F), green `wp02-T082-green.txt`; guard `test_a_second_backfill_writes_nothing_and_refuses_an_incomplete_binding`; `backfill_bindings` action |
| T083 | closed | `resident-backfill.json` (dry run), `resident-backfill-applied.json` (apply + 18/18 existence assertions), `resident-backfill-second-run.txt`, `wp02-T083-probe-before.json`, `wp02-T083-byte-rule.txt`, `wp02-T083-mutation.txt` |

Boundary note (not a row of this package): the engine half of T078 (`probe-residual`) and its
guard `test_the_residual_probe_is_read_only_and_ignores_the_run_scratch_area` landed here because
the probe section is in this package's write domain. T078's own row remains open for
`templates/commands/sanitize.md`, which belongs to wp06 and was not touched.
Reading: `test-evidence/wp02-T078-engine-green.txt`.

## Test readings

All suite runs went through the canonical runner
`bash scripts/bash/run-tests.sh <paths> -q` (pytest-xdist `-n auto --dist load`).

- Red-first (before the actions existed):
  - `tests/contract/test_archive_migration.py`: **10 failed, 1 passed**, exit 1 —
    `wp02-T028-red-archive-migration.txt`. The single pass is the inert
    `test_no_other_action_invokes_the_migration` guard; the red form is the engine's own
    `unrecognized option: --apply` (exit 2) plus the missing roster entries.
  - `tests/contract/test_migration_interruption.py`: **1 failed**, exit 1 —
    `wp02-T031-red-interruption.txt`.
  - `tests/integration/test_archive_migration_real_data.py`: **1 failed**, exit 1 —
    `wp02-T032-red-real-data.txt`.
  - `tests/contract/test_resident_backfill.py`: **2 failed**, exit 1 —
    `wp02-T082-red-backfill.txt`.
- Green (final engine):
  - four modules together: **15 passed, exit 0** (`wp02-green-all-modules.txt`); the two
    contract modules alone read 12 passed (`wp02-green-archive-modules.txt`).
  - per-row focused runs: 16 files `wp02-T0*-green.txt`, every one `EXIT=0`.
- Engine-adjacent regression (disclosure, not a gate): `test_binding_model.py`,
  `test_run_checks.py`, `test_goal_definition.py`, `tests/unit/test_goal_utils.py` →
  **157 passed, 1 failed**. The one failure is the action-roster pin (§ Residual risks 1).
- Mirror check: `wp02-mirror-check.txt` — exactly one drift, `.specify/scripts/python/goal-utils.py`,
  the projection of this package's engine edit (same class wp01 disclosed).
- Real-tree migration dry run (read-only pre-check, not T079's evidence): 17 decisions, all
  `migrated`, **0 conflicts**, `.specify/archive/goal-team/` not created. T079 (wp07) owns the
  dated dry-run/apply evidence for the real migration.

## Real-tree backfill readings (T083)

- Probe before: `.specify/specs/*/goal/*/goal.md` 9, `.specify/specs/*/team/*/team.md` 8
  (`wp02-T083-probe-before.json`).
- Denominator: `.specify/anchoring/*/goal.md` 6 + `.specify/teams/*/team.md` 12 = 18
  (`resident-backfill-applied.json`), matching `analyze-repair2-resident-measurement.txt`.
- Dry run: 18 `backfilled`, 0 `already-bound` (`resident-backfill.json`).
- Apply: 18 backfilled; the engine's `binding` read action answers complete
  (human / human / null) for **18/18** (`resident-backfill-applied.json`).
- Second run: 18 `already-bound` lines, zero writes, exit 0
  (`resident-backfill-second-run.txt`).
- Byte rule: each resident minus its binding block is identical to its HEAD bytes, **18/18**
  (`wp02-T083-byte-rule.txt`).
- Mutation (fixture copy, no tree edit): removing one binding block turns the T081
  exhaustiveness sensor red — `binding-missing`, exit 2 (`wp02-T083-mutation.txt`).

## Commits

- `3c7d3433` — `feat(094-wp02): migrate-archive, probe-residual and backfill engine + guards (T028–T041, T081–T082)`
- `9e072ddc` — `feat(094-wp02): backfill the resident bindings on the real tree (T083)`
- the report itself rides a third commit (`feat(094-wp02): implement report …`). No push.

## Disclosed decisions (recorded, not inferred silently)

1. **Binding values written by the migration.** No contract clause names `owner` / `owner_id`
   for migrated definitions; C-1 requires a complete record and C-36 requires `origin`. A
   migration is a human-invoked `/speckit.goal` action with no run id, so the migrated record is
   `owner: human`, `owner_id: human`, `origin: <source spec>` — the same closed-set reading as
   the Q14 backfill ruling, with `origin` non-null. An existing canonical binding on the source
   keeps its `owner` / `owner_id`; only `origin` is set.
2. **Equivalent target semantics.** When the target slug already exists with the same concept
   payload (binding excluded), the migration does not overwrite it (C-38); it archives the source
   tree under `trees/`, writes the receipt, and leaves the target bytes untouched. Such a target
   is a pre-existing resident, not this migration's write; `backfill-bindings` is what makes it
   interpretable.
3. **Team concept payload.** C-40 lists goal-shaped fields (Objective / Success Criteria /
   Lifecycle status / Targets). For teams the nearest concept fields are compared —
   `description`, the inline `goal:` folded text, `goal_slug`, `lifecycle_state`; territory and
   the binding block stay outside the comparison.
4. **Interrupted receipts are completed in place.** C-33 calls receipts immutable once written
   while C-39 says the resume "finishes the receipt". Read together: final receipts
   (`migrated` / `noop` / `conflict` / `archived`) are immutable and never rewritten; the
   `interrupted` marker is a state record that the resuming call replaces with the final
   outcome in the same per-definition path.
5. **Interruption seam.** `GOAL_UTILS_FAULT_AFTER` (`target-write` / `source-move`) is a
   declared, closed, side-effect-free test seam used by T031's module; unset in production.

## Residual risks and disclosed boundaries

1. **Action-roster pin is unowned and now reads 16.** `tests/contract/test_run_checks.py::test_c1_the_action_exists_and_the_roster_grew_by_exactly_one`
   pins `sub.add_parser == 11`; wp01 disclosed it at 13, and this package's three actions move it
   to 16. The module is outside every package's write domain; the pin needs an explicit driver
   ruling rather than a silent edit. (`test_c24`'s exit-code line passes: the table stayed on one
   line and still carries 0/2/3/4/5 with 5 labelled `blocked`.)
2. **Mirror projection is pending the driver's integration step.** `sync-mirrors.py --check`
   reports exactly one drift, `.specify/scripts/python/goal-utils.py` — the projection of this
   package's edit. Fix is `sync-mirrors.py --write` at integration, not a hand edit (wp01's
   precedent).
3. **Two one-level team files stay outside the probe by design.** `.specify/specs/088-speckit-visualization/team/team.md`
   and `.specify/specs/092-non-disposable/team/team.md` are not in C-43's declared form
   (`*/team/*/team.md`), so neither the probe nor the migration enumerates them. After T079 the
   probe will read zero while these two files remain on disk. This was disclosed by plan EP-002
   and requirements A6; resolving it needs a contract/plan ruling (the engine must not invent a
   slug for a non-conforming path).
4. **Receipt path is per `kind`+`slug`, not per source spec.** Two different specs migrating the
   same slug would collide on `receipts/<kind>-<slug>.yaml`. The measured collision count is zero
   (EP-002 overlay) and a differing target payload is refused as a conflict (exit 4), so the
   collision is unreachable on this tree; it is stated here rather than claimed away.
5. **Full-suite baseline not re-run in this package.** GATE-1 belongs to wp07 after fixture and
   worktree teardown (execution lesson 2). This package's readings are the targeted modules plus
   the engine-adjacent regression set above.
