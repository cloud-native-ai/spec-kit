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
