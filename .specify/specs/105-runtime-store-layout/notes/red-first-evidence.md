# Red-first evidence — 105 runtime-store-layout

One entry per test execution: command, real output, exit code. Owner of the comparison form:
`.specify/skills/internal/implement-feature/SKILL.md` § Test runs. Every execution goes through the
unique entry `bash scripts/bash/run-tests.sh` with `SPECKIT_PYTHON=/usr/local/bin/python3`.

## T002 — `tests/contract/test_runtime_store_layout.py` (red)

- Date: 2026-11-25
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_runtime_store_layout.py -q`
- Exit code: **1**
- Output (decisive excerpt):

```text
$ ... (full log: test-evidence/t002-red-run.txt)

=================================== FAILURES ===================================
... test_repo_has_no_retired_root ...
E       AssertionError: .specify/memory is a retired store root; the dogfood migration (US5) must remove it
... test_declaration_equals_inventory_and_consumer_sets ...
E           Failed: declaration-absent: runtime-store-layout: no declaration for fact 'runtime-store-layout'
... test_framework_map_rows_and_tombstone ...
E           Failed: declaration-absent: runtime-store-layout: no declaration for fact 'runtime-store-layout'
... test_inventory_is_closed ...
E           Failed: declaration-absent: runtime-store-layout: no declaration for fact 'runtime-store-layout'
... test_two_writers_distinct_paths ...
E           Failed: declaration-absent: runtime-store-layout: no declaration for fact 'runtime-store-layout'
=========================== short test summary info ============================
FAILED tests/contract/test_runtime_store_layout.py::test_repo_has_no_retired_root
FAILED tests/contract/test_runtime_store_layout.py::test_declaration_equals_inventory_and_consumer_sets
FAILED tests/contract/test_runtime_store_layout.py::test_framework_map_rows_and_tombstone
FAILED tests/contract/test_runtime_store_layout.py::test_inventory_is_closed
FAILED tests/contract/test_runtime_store_layout.py::test_two_writers_distinct_paths
5 failed, 1 passed in 6.72s
```

- Reading: the five declaration-dependent guards fail on the absent fact (`declaration-absent:
  runtime-store-layout`) and the dogfood guard fails on the still-present retired root;
  `test_mirror_member_set` is the one green (the tree is still at its pinned drift set — it turns red
  when T003 adds a source-only file, which is the recorded red-first reading below).

## T006 — `tests/integration/test_init_new_layout.py` (red → green)

- Date: 2026-11-25
- Command (red): `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_init_new_layout.py -q`
- Exit code (red): **1**
- Output (decisive excerpt; full log `test-evidence/t006-red-run.txt`):

```text
E       AssertionError: .specify/memory must not be created by a fresh init (C-2/C-7)
E       assert not True
FAILED tests/integration/test_init_new_layout.py::test_fresh_init_seeds_the_new_layout
1 failed in 8.53s
```

- Fix side: the subject (T008 seeding), not the assertion — the red named exactly the retired
  container the fresh init still created.
- Green reading: see the T009 entry below (`test_fresh_init_seeds_the_new_layout` PASSED).

## T009 — US1 green with the two allowed residual reds

- Date: 2026-11-25
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_init_new_layout.py tests/contract/test_runtime_store_layout.py -v`
- Exit code: **1** (only the two residual reds US5 closes)
- Per-function results (parallel workers, full log `test-evidence/t009-us1-verbose.txt`):

```text
PASSED tests/contract/test_runtime_store_layout.py::test_inventory_is_closed
FAILED tests/contract/test_runtime_store_layout.py::test_repo_has_no_retired_root
PASSED tests/contract/test_runtime_store_layout.py::test_framework_map_rows_and_tombstone
PASSED tests/contract/test_runtime_store_layout.py::test_declaration_equals_inventory_and_consumer_sets
PASSED tests/contract/test_runtime_store_layout.py::test_two_writers_distinct_paths
FAILED tests/contract/test_runtime_store_layout.py::test_mirror_member_set
PASSED tests/integration/test_init_new_layout.py::test_fresh_init_seeds_the_new_layout
2 failed, 5 passed
```

- Residual reds, both owned by US5 and both allowed by the P1 completion criterion:
  - `test_repo_has_no_retired_root` — the dogfood migration (T033) has not run yet; `.specify/memory/`
    still exists in this repository.
  - `test_mirror_member_set` — this package edited four mirrored sources and added one source-only
    fact, so the drift member set gained exactly:
    `.specify/scripts/python/memory-utils.py`, `.specify/scripts/python/record-retention.py`,
    `.specify/scripts/python/renumber-utils.py`, `.specify/shared/declarations/facts/runtime-store-layout.yaml`
    (the three edited files share the mirror pair; the fact is a new MISS). T031 regenerates them.
- Fresh-init tree listing (command + real output, `test-evidence/init-tree-t009.txt`):

```text
$ find .specify -maxdepth 1 -mindepth 1 | sort
.specify/agents
.specify/constitution.md
.specify/features
.specify/features.md
.specify/.gitignore
.specify/knowledge
.specify/scripts
.specify/session
.specify/shared
.specify/skills
.specify/source.json
.specify/templates
.specify/tools.md
.specify/workflow
$ ls -a .specify/session .specify/knowledge
.specify/knowledge: . .. .gitkeep
.specify/session:   . .. .gitkeep
$ test -e .specify/memory
ABSENT
```

- Reading: the two memory tiers are seeded as first-class top-level roots with their packaged
  placeholders, anchors stay at the `.specify/` root, no other runtime store exists, and the retired
  container is absent. C-7's final `[green:]` stays with T038 (SC-005 live reading); this entry is
  US1's turn-green evidence, not the final green point.

## T011 — `tests/integration/test_store_layout_migration_us1_us2.py` (red)

- Date: 2026-11-25
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_store_layout_migration_us1_us2.py -q`
- Exit code: **1** (full log `test-evidence/t011-red-run.txt`)
- Output (decisive excerpt):

```text
FAILED tests/integration/test_store_layout_migration_us1_us2.py::test_fresh_init_plans_no_store_items
FAILED tests/integration/test_store_layout_migration_us1_us2.py::test_rerun_after_success_is_clean_with_one_receipt_per_run
FAILED tests/integration/test_store_layout_migration_us1_us2.py::test_dual_content_refuses_with_both_paths_and_leaves_both_trees
FAILED tests/integration/test_store_layout_migration_us1_us2.py::test_legacy_apply_moves_bytes_identically_and_removes_old_roots
FAILED tests/integration/test_store_layout_migration_us1_us2.py::test_legacy_dry_run_writes_nothing_and_plans_every_store
5 failed in 9.35s
```

- Reading: none of the five behaviours exists yet. The dry-run envelope carries
  `"items": []` / `"outcome": "clean"` / `exit 0` on the legacy fixture (the fifth-dimension engine
  sees no difference at all — the store-layout dimension does not exist), the dry-run receipt has no
  `storeLayout` object, `build_rerun` cannot reach its post-success state, and no store item ever
  names `dual-content`. Each red names the missing store-layout behaviour, not a broken assertion.

## T016 — US2 turn-green readings (dry-run zero-write / byte-identical / dual / rerun)

- Date: 2026-11-25
- Package gate command:
  `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_store_layout_migration_us1_us2.py tests/contract/test_migrate_engine_contract.py tests/unit/test_migrate_planner.py -q`
- Exit code: **0** — `32 passed in 9.84s` (full log `test-evidence/t016-us2-gate-run.txt`)
- End-to-end fixture readings (`test-evidence/t016-us2-readings.txt`, one run over the
  declaration-built fixtures):

```text
DRY-RUN legacy: exit=1 outcome=planned store_items=15 tree_unchanged=True git_status_empty=True receipt_store_created=False
APPLY legacy: exit=0 outcome=applied receiptPath=.specify/migrate/receipts/20261125T054812Z-94e8c6f3.json diff_r_rc=[0] memory_absent=True receiptVersion=2 storeLayout={"stores": 14, "resolved": 14, "refused": 0, "blocked": 0, "container": "removed", "manifestDigest": "aaa45ae9756c2f8df0454bfa318d0078f6329219df0d9ce71661dbb6a7b3009c"} status=completed
DUAL apply: exit=3 outcome=blocked item=refuse/refused old_unchanged=True new_unchanged=True container=refuse/refused container_preserved=True
RERUN apply: exit=0 outcome=clean items=0 receipts=['20261125T054816Z-d15cb0bd.json', '20261125T054817Z-9cef7727.json'] storeLayout={"stores": 0, "resolved": 0, "refused": 0, "blocked": 0, "container": "absent", "manifestDigest": "4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945"} memory_absent=True
```

- Reading:
  - dry-run: 15 store-layout items (14 stores + container), full-tree digest unchanged, `git status`
    empty, no receipt store created — zero writes.
  - apply: `diff -r` rc 0 for every store against its preserved legacy tree; the retired container is
    gone; one v2 receipt names `storeLayout.stores=14 resolved=14 refused=0 blocked=0
    container=removed`; relocation rows carry `change=relocated` with the new-path `archiveTo` (no
    byte copy under `.specify/archive/`).
  - dual: `blocked` (exit 3); the `feedback` item is `refuse/refused` with `dual-content` naming both
    roots and the repair entry; both subtrees hash-identical before/after; the container item flips to
    `refuse/refused` with `unknown-residue` and the container is preserved.
  - rerun: `clean` (exit 0) with zero items; two receipts, one per run, distinct run ids; the retired
    container is not re-created.
- Fault-injection resume reading (injected `OSError` on the 5th store move): run 1 `blocked` with the
  receipt `status=aborted` and the failed item's 4 already-moved entries recorded; run 2 resumes from
  the aborted receipt (`resume:` note names it), ends `applied`, no duplicate `entries[]` relpaths,
  container removed.
- 097 regression batch (`test-evidence/p2-097-batch2.txt`): `87 passed` across the four 097 US
  suites, the three 097 command/contract faces, and the two unit files.
- Full fast tier (clean tree, `--names-out`):
  `1145 failed, 9076 passed, 4 skipped, 9 errors in 64.85s` (log
  `test-evidence/p2-final-run.txt`, names `test-evidence/p2-final-failed.txt`). Name-level delta vs
  the P1 final (`p1-final-failed.txt`, 1150 names): **0 new failures**, **5 repaired**
  (`test_agents_run_command_contract.py::test_c09_…`,
  `test_migrate_distribution_assembly.py::test_regen_check_is_clean`,
  `test_run_checks.py::test_c27_…`, `test_status_digest.py::test_c42_…`,
  `test_user_facing_comprehension_pointers.py::test_c14_…`) — all five were per-tool command-copy
  drift, cured when `regen-command-copies.py` regenerated every copy for this package. The 9 setup
  errors are byte-identical to the P1-disclosed set (live-target fixtures owned by T029).
