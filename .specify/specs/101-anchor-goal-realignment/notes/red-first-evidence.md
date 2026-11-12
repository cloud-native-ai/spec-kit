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
