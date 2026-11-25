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

## T017 — `tests/integration/test_memory_preservation.py` (authoring run)

- Date: 2026-11-25
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_memory_preservation.py -q`
- Exit code: **0** — `5 passed in 6.49s` (full log `test-evidence/t017-authoring-run.txt`)
- Reading — honest disclosure, not a fabricated red: the five assertions (session record→recall
  round-trip under `.specify/session/`, knowledge upsert-by-slug under `.specify/knowledge/`, prune
  age/count bounds, reindex legacy-index retirement, determination persistence + history + pinned
  schema keys) went green at authoring time because **P1's T004 front-loaded this substance** — the
  memory engine's root constants were re-pointed to `.specify/<scope>/` in the foundational phase,
  and `run-determination` persists through that engine (P-2 wiring unchanged). The red capability of
  the root move itself is already on record: the P1 live-target set (`test-evidence/p1-final-failed.txt`,
  404 names incl. `tests/unit/test_memory_utils.py`, which asserts the old literal and is owned by
  T029) is exactly the suite that goes red when the root flips. Per the front-loading-closure
  discipline this row is closed by re-verifying the assertion set against the current tree, not by
  reverting-then-rewriting; the assertions discriminate (path prefix + retired-root absence would
  fail if the engine still wrote under `.specify/memory/`).
- Residual surface this file does NOT cover: the two memory skills' path text — that red belongs to
  T018's authoring run below and is what T019 fixes.

## T018 — `tests/integration/test_dispatch_injection_paths.py` (red)

- Date: 2026-11-25
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_dispatch_injection_paths.py -q`
- Exit code: **1** — `1 failed, 6 passed in 6.48s` (full log `test-evidence/t018-red-run.txt`)
- Red (decisive excerpt):

```text
FAILED tests/integration/test_dispatch_injection_paths.py::test_memory_skill_text_names_only_the_new_roots
E       AssertionError: skills/internal/memory-record/SKILL.md still injects a reference to the retired root
E         '.specify/memory/' is contained here:
E           ontext to .specify/memory/session/ and long-term distilled knowledge to .specify/memory/knowledge/.
```

- Reading: the two memory skills still name `.specify/memory/session/` and
  `.specify/memory/knowledge/` in their description and Path Conventions — the injection surface a
  `memory-recall`-declaring child loads. Fix side: the subject (T019 skill-text wiring), not the
  assertion; P-3 requires every injected memory reference to resolve under the new roots.
- Already green at authoring (structural + behavioural half of the fixture): the owner protocol keeps
  exactly the seven downlink ids, four injection owner pointers and five uplink elements; the
  `agents/reporter.agent.md` child still declares `memory-recall` and both seeded entries are returned
  under the new roots; the reverse fixture's unique token written only to `.specify/feedback/` +
  `.specify/exec-quant/` is not returned by `--action recall`; the scope closed set stays
  `("session", "knowledge")` and `--action list --scope all` returns memory-store paths only.

## T019 — memory-surface wiring (subject fixed)

- Date: 2026-11-25
- Changed subjects: `skills/internal/memory-record/SKILL.md` and
  `skills/internal/memory-recall/SKILL.md` (description + Path Conventions now name
  `.specify/session/` / `.specify/knowledge/`; recall gains the P-1 search-boundary statement: only the
  two memory stores are read, runtime stores are never traversed); `shared/declarations/facts/memory-types.yaml`
  `note` path parentheticals updated to the new roots. In-passing correction (disclosed): the record
  skill's "maintains an `index.json` per scope" sentence was already false since the 055
  scan-derived-index protocol and is repaired in the same bullet it lived in.
- `scripts/python/memory-utils.py` needs no code change: the two tier roots resolve as
  `.specify/<scope>` where the scope names are the declaration-layer fact (`memory-types`, read through
  `declaration_reader`), and the `.specify` container is the engine's own root constant — the C-6
  single-store-engine allowance. `scripts/python/run-determination.py`'s persistence adapter note already
  names `.specify/session/` (P-2 wiring untouched; memory-utils is its only writer).
- No scope renamed, no action added, no second memory source (FR-006 / FR-009 / FR-012 preserved).

## T020 — US3 turn-green readings

- Date: 2026-11-25
- Package gate command:
  `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_memory_preservation.py tests/integration/test_dispatch_injection_paths.py -q`
- Exit code: **0** — `12 passed in 6.49s` (full log `test-evidence/t020-us3-gate-run.txt`)
- Fixture readings (`test-evidence/t020-us3-readings.txt`, one run over a throwaway
  `.specify/.tmp/p3-readings-105/` workspace, removed at teardown):

```text
SESSION record path=.specify/session/20261125T060056Z-roundtrip-probe.md
SESSION recall matches=['.specify/session/20261125T060056Z-roundtrip-probe.md']
KNOWLEDGE record path=.specify/knowledge/durable-probe.md upsert_path=.specify/knowledge/durable-probe.md same=True
KNOWLEDGE files=['durable-probe.md']
DETERMINATION persisted=True path=.specify/session/20261125T060057Z-run-determination-skill-probe-probe-run-1.md
DETERMINATION history total=1 runs=['probe-run-1']
DETERMINATION entry exists=True
REVERSE token returned=False matches=3
INJECTION source paths=['.specify/knowledge/durable-probe.md', '.specify/session/20261125T060056Z-roundtrip-probe.md', '.specify/session/20261125T060057Z-run-determination-skill-probe-probe-run-1.md']
RETIRED root created=False
```

- Reading: record→recall round-trip lands a single entry under `.specify/session/` and recall returns
  the same path; knowledge upsert keeps one file (`durable-probe.md`) for the repeated title;
  the determination record persists through the memory engine into `.specify/session/` and
  `--action history` retrieves the run (schema pinned by the test's literal key set); the reverse
  token written only to feedback + exec-quant is not returned by any memory recall (the three matches
  are the memory entries that share the ordinary word "token" — the unique token string itself never
  appears); every injected/list-injected memory reference resolves under the two memory roots; the
  retired container is never created.

## T025 — `tests/contract/test_store_layout_live_refs.py` (red)

- Date: 2026-11-25
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_store_layout_live_refs.py -q`
- Exit code: **1** — `3 failed, 1 passed in 6.24s` (full log `test-evidence/t025-red-run.txt`)
- Output (decisive excerpt):

```text
FAILED tests/contract/test_store_layout_live_refs.py::test_product_class_occurrence_sets_equal_the_allowlist
E  AssertionError: framework-source: unexpected=['shared/declarations/facts/non-disposable-review-surface.yaml', ...,
   'templates/instructions-template.md', 'templates/tools.md'] missing=[]
FAILED tests/contract/test_store_layout_live_refs.py::test_allowlisted_files_keep_only_allowed_lines
FAILED tests/contract/test_store_layout_live_refs.py::test_tests_literal_confined_to_declared_set
```

- Reading: the pinned-copy function is green (the in-test allowlist equals the contract L-5 table);
  the occurrence set is red with 90 measured carriers — 69 framework-source files (the 4 allowlisted
  files plus 65 live carriers), 2 runtime-guide files and 19 current-docs files — exactly the live
  surface US5 rewrites; the line-rule function is red because the declaration's prose note and
  header comment still spell the literal outside the `retired_container` key; the tests-class
  function is red with 83 live carriers (91 measured files minus the declared legacy/guard set of
  8). Fix side: T026–T031 (subjects), never the assertions.

## T032 — guard closure (C-6) and the four L-5 mutation drills

- Date: 2026-11-25
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_store_layout_live_refs.py tests/contract/test_runtime_store_layout.py -v`
- Exit code: **1** — `1 failed, 9 passed in 6.62s` (full log `test-evidence/t032-guard-run.txt`)
- Per-function results:

```text
PASSED test_store_layout_live_refs.py::test_allowlist_pinned_copy_equals_the_contract_table
PASSED test_store_layout_live_refs.py::test_product_class_occurrence_sets_equal_the_allowlist
PASSED test_store_layout_live_refs.py::test_allowlisted_files_keep_only_allowed_lines
PASSED test_store_layout_live_refs.py::test_tests_literal_confined_to_declared_set
PASSED test_runtime_store_layout.py::test_inventory_is_closed
PASSED test_runtime_store_layout.py::test_declaration_equals_inventory_and_consumer_sets
PASSED test_runtime_store_layout.py::test_framework_map_rows_and_tombstone
PASSED test_runtime_store_layout.py::test_two_writers_distinct_paths
PASSED test_runtime_store_layout.py::test_mirror_member_set
FAILED test_runtime_store_layout.py::test_repo_has_no_retired_root
```

- Reading: allowlist equality holds both directions (framework-source measured set == the four
  declared files; runtime-guide and current-docs empty); every allowlisted line satisfies its rule
  (tombstone row and `retired_container` key exactly once); the tests-class set equals the declared
  legacy/guard set of 12 carriers; the mirror member set carries **no new member** vs the 450-DIFF
  baseline (current 369 members / 75 cured, `test-evidence/p4-sync-mirrors-check.txt`). The one red
  is `test_repo_has_no_retired_root` — the dogfood guard T033 closes; recorded, not suppressed.
- Mutation drills D1–D4 executed and restored (readings: `test-evidence/mutation-drill.md`); each
  mutation turned exactly its named function red, each restore returned green with checksum
  equality.

## T029 — tests live-reference classification and update

- Date: 2026-11-25
- Re-measured inventory: `grep -rl '\.specify/memory' tests/` (literal form) = 90 files / 219
  hits at P4 start; the tree reading is not a contract (R-2.5) and the fragment-built old-root
  fixtures were found and fixed in the same pass (Path joins and `"memory"` segments are
  invisible to the literal grep).
- Classification (L-3 / R-2.5), final measured carrier set = 12 files:
  - legacy-fixture (kept, 6): `tests/fixtures/migrate-097/builders.py`,
    `tests/integration/test_migrate_us1_converge.py`, `tests/integration/test_migrate_us2_safety.py`,
    `tests/integration/test_store_layout_migration_us1_us2.py`, `tests/unit/test_migrate_planner.py`,
    `tests/unit/test_sanitize_checks_migration.py` (sanitize legacy-residue check);
  - guard set (6): `tests/contract/test_runtime_store_layout.py`,
    `tests/contract/test_store_layout_live_refs.py`, `tests/contract/test_tools_domain.py`,
    `tests/integration/test_dispatch_injection_paths.py`, `tests/integration/test_init_new_layout.py`,
    `tests/integration/test_memory_preservation.py`;
  - live-target rewrites across 76 modules; stale repairs for `.specify/memory/features…` and
    anchor paths; non-disposable corpora renamed `.specify/memory` → `.specify/session` (fixture
    data only), `tests/fixtures/client_project.py` feedback_dir → `.specify/feedback`.
- Batch gate: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh <76 touched
  modules> -q` → **224 failed, 1138 passed, 1 skipped, 4 pre-existing setup errors** (full log
  `test-evidence/p4-t029-batch-run.txt`).
- Name-level delta vs the P3 baseline (`p3-final-failed.txt`): **3 new names, all dogfood-ordered
  transients** — `test_coaching_wiring_contract.py::test_c6…[.specify/feedback/probe-map.md]`,
  `test_goal_migration.py::…[.specify/tools/build-summary-input.py.md]`,
  `test_no_retired_draw_skill_refs.py::test_the_superseded_knowledge_ledger_carries_its_banner` —
  each reads a real repo artifact that still sits under the retired root until T033 moves it. The
  4 setup errors are byte-identical to the P1/P3-disclosed set.

## T021 — `tests/contract/test_tools_domain.py` + `tests/contract/test_specify_gitignore_template.py` (red)

- Date: 2026-11-25
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_tools_domain.py tests/contract/test_specify_gitignore_template.py -q`
- Exit code: **1** — `6 failed, 2 passed in 6.47s` (full log `test-evidence/t021-red-run.txt`)
- Red (decisive excerpt):

```text
FAILED tests/contract/test_specify_gitignore_template.py::test_template_uses_specify_relative_patterns
FAILED tests/contract/test_tools_domain.py::test_template_and_installed_copy_are_byte_identical_with_narrow_rules
FAILED tests/contract/test_specify_gitignore_template.py::test_retired_whole_directory_and_memory_rules_are_gone
FAILED tests/contract/test_tools_domain.py::test_same_basename_record_and_inventory_coexist
FAILED tests/contract/test_tools_domain.py::test_tools_records_are_tracked_and_inventories_ignored
FAILED tests/contract/test_tools_domain.py::test_claude_and_codex_templates_release_every_store_root
```

- Reading: the template still ignores the whole `tools/` directory (records would be silently
  dropped), still carries `memory/sanitize/` and `memory/trigger/telemetry.jsonl`, and both
  claude/codex templates still release `!.specify/memory/` instead of the 14 store roots. The two
  green tests are `test_template_exists` and `test_installed_copy_is_byte_identical_to_the_template`
  (the pair is identical today — they drift only if the update is asymmetric). Fix side: T022/T023
  (subject), not the assertions.

## T022 — tools domain implementation (subject fixed)

- Date: 2026-11-25
- Changed subjects: `scripts/python/tools-utils.py` (canonical-layout docstring → `<workspace>/.specify/tools`);
  `scripts/python/skills-utils.py` (`infer_resource_type_from_path` prefix and `_discover_by_text` tools dir);
  `scripts/bash/create-new-tools.sh` (effects text, `TOOLS_MEMORY_DIR`, canonical path);
  `shared/definitions/tool-definitions.md` (5 path references; the inventories sentence and the
  hand-maintained `.specify/tools.md` statements preserved);
  `scripts/python/sanitize-utils.py` (the inverted `legacy-tools-registry` check removed per M-7;
  `MATERIAL_ROOTS` entry renamed `tools-domain` over `.specify/tools` — the domain is scanned, never
  flagged as residue). Assertion-side follow-up (required, cited): `tests/unit/test_sanitize_checks_migration.py`
  pinned the removed behaviour; its C-22 section now asserts the tools domain is never residue.
- Behavioral execution (not only a text scan): a throwaway workspace got `save_record` → saved
  `.specify/tools/probe-tool.md`, `tool_id <TOOL:.specify/tools/probe-tool.md>`, text discovery
  `fallback` resolving the same id, `infer_resource_type_from_path(".specify/tools/probe-tool.md") == "tool"`.
- `py_compile` exit 0 on the three engines; `bash -n` exit 0 on `create-new-tools.sh`;
  `--version`/`--help` answer on all four faces.

## T024 — US4 turn-green readings

- Date: 2026-11-25
- Package gate command:
  `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_memory_preservation.py tests/integration/test_dispatch_injection_paths.py tests/contract/test_tools_domain.py tests/contract/test_specify_gitignore_template.py -q`
- Exit code: **0** — `20 passed in 6.56s` (full log `test-evidence/p3-package-gate-run.txt`)
- US4 fixture readings (`test-evidence/t024-us4-readings.txt`, throwaway git workspace removed at
  teardown):

```text
== git check-ignore -v .specify/tools/system.json ==
.specify/.gitignore:16:tools/*.json	.specify/tools/system.json
== git check-ignore -v .specify/tools/kubectl-get.json ==
.specify/.gitignore:16:tools/*.json	.specify/tools/kubectl-get.json
== git check-ignore -q .specify/tools/kubectl-get.md ==
rc=1 (1 = not ignored)
== git ls-files .specify/tools ==
.specify/tools/kubectl-get.md
== cmp templates/gitignore-specify-template .specify/.gitignore ==
cmp_rc=0 (0 = byte-identical, no output)
```

- Reading: only the generated inventories match the narrow `tools/*.json` rule; the record with a
  colliding basename stays tracked and is the only file `git add -A` stages; template and installed
  copy are byte-identical; both claude/codex templates release exactly the 14 declared store roots
  (plus the pre-existing `instructions.md` and `specs/` lines) and carry zero `!.specify/memory/`
  occurrences.

## T034 — failure-surface fixtures (builders extended)

- Date: 2026-11-25
- `tests/fixtures/store-layout-105/builders.py` gains `build_residue` (`draft/` + stray
  `git-workflow.md` under the retired container), `build_symlink` (one store's legacy path replaced
  by a symlink to `sibling-content/<store>`), `build_readonly` (one store's target root pre-created
  `0o555`; the target parent of every relocated entry) and `build_partial` (a real dry-run plan whose
  upper-half entries are physically relocated and whose rows are flipped to `status=moved`, landed in a
  `running` receipt via the engine's own `create_migrate_receipt`/`update_migrate_receipt` so the resume
  oracle is engine-shaped; `archives[]` stays empty — an interruption persists manifest snapshots only).
- All fixtures stay declaration-driven (no second roster, no store-name literal).

## T035 — `tests/integration/test_store_layout_migration_us3_us6.py`

- Date: 2026-11-25
- Classification: migration/regression exception (tasks.md § Tests Mode). The guarded executor behaviour
  was delivered by T014; red ability is proven by D5/D6 in `test-evidence/mutation-drill.md`, and every
  assertion group carries its mutation pairing in the module docstring.
- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_store_layout_migration_us3_us6.py -q`
- Exit code: **0** — `4 passed in 9.64s`.
- Fixture readings (seed probe, re-confirmed by the module):
  - residue: apply exit **3** / `blocked`; 14 store items `done`; container item `refused`,
    `unknown-residue` naming `.specify/memory/draft/`, `.specify/memory/draft/parked-idea.md`,
    `.specify/memory/git-workflow.md`; container + both files byte-identical after the run (zero deletion).
  - symlink: apply exit **3** / `blocked`; `.specify/feedback` item `refused`, `symlink-source`, path named;
    link readable and unchanged (`os.readlink` equal), sibling bytes unchanged, `.specify/feedback` never created.
  - readonly (uid 1001; root-run records the platform fact and skips): apply exit **3** / `blocked`;
    feedback item `refused permission-denied` naming both paths; old side hash map unchanged and the
    pre-created target root still empty (no partial success); other stores converge.
  - partial: apply exit **0** / `applied`; previously moved entries verified in place with identical raw
    bytes and no second move; remainder moved; container absent; two receipts, one per run; the
    interrupted receipt is byte-identical (read-only resume input) and carries `archives: []`; the
    completing receipt has unique entry relpaths, all rows `moved`, unique archive records keyed by
    `from` (one record per object), `len(recover) == len(archives)`, and zero `.specify/archive/` bytes.
- Disclosed observation (no assertion; spec-side decision needed): a THIRD `--apply` after a completed
  resume still reads the stale `status=running` receipt as the resume oracle, so it re-emits the 14 store
  items (all rows verified `moved`, 32 archive rows again) and reports `applied`, not `clean` — M-6's
  idempotence sentence ("after a completed run, a second apply … exits `clean`") is not met for the
  crash→resume→rerun sequence. No data movement or loss occurs; the run only re-records. Reported as an
  anomaly to the driver rather than repaired here (marking the interrupted receipt superseded is a
  design decision, not a correction).

## T042 — FR-027 / SC-009 inventory closure guard

- Date: 2026-11-25
- Subject: `tests/contract/test_runtime_store_layout.py::test_backward_incompatible_inventory_is_closed`
  (migration/regression exception per tasks.md: it guards the already-landed plan inventory and T016's
  delivered migration behaviour; red ability is proven by the drills below, not by a red-first pass).
- Guard scope decisions:
  - (d) forbidden-word scope = the **Behavior cell only** (U-03): BC12's change cell legitimately names
    `todo/`, and the test pins that fact (`"todo/" in BC12.change`) so the scope choice stays honest.
  - (c) evidence pointers resolve transitively: evidence cells that say `同 BC01` expand through the
    named row before resolution; every extracted test path must exist, every `T0NN` must be a tasks.md
    row, every `M-n` / `C-n` must have a heading in its contract.
  - (a) state-changing Store Inventory rows are derived from the table's disposition cell (a
    `.specify/` target, `退役`, or `墓碑行`, excluding the `非存储` row) and must equal
    `{1…15, 17}` exactly once across the BC rows (18 rows, contiguous BC01…BC18).
- Green run: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_runtime_store_layout.py::test_backward_incompatible_inventory_is_closed -q`
  → `1 passed in 9.74s`, exit **0**.
- Drill A (delete one row) — plan.md pre-drill sha256 `7a7baac8362ce8a8…`; the BC13 row removed:
  exit **1**, `AssertionError: the inventory must be a contiguous, duplicate-free BC01…BCNN set`
  (`At index 12 diff: 'BC14' != 'BC13'`). Restore = exact line re-insertion at its original index;
  sha equal; green re-run exit **0**.
- Drill B (forbidden word) — BC01's Behavior cell `migrate:relocate` → `manual`:
  exit **1**, `AssertionError: BC01: behavior 'manual' is outside the closed class set`. Restore =
  exact reverse substitution; sha equal; green re-run exit **0**; `git diff -- plan.md` empty.
- Territory disclosure: the drill required temporary edits to `plan.md` (forbidden as a work product).
  Both were reverse-substituted exactly, checksum-equal, and `git diff` on the file is empty; no plan
  content changed.

## T041 — final gate readings

- Date: 2026-11-25
- Full fast tier (runner passes=2): **218 failed, 10040 passed, 3 skipped, 0 setup errors** in
  64.05 s — `test-evidence/p5-full-run.txt`, names `test-evidence/p5-full-failed.txt`.
- Name-level delta vs the implement entry baseline (`implement-baseline-failed.txt`, 748 names):
  `comm -13` **0 new failures** (`test-evidence/p5-new-vs-baseline.txt` is empty), `comm -23`
  **530 repaired** baseline reds. The remaining 218 are all pre-existing baseline reds and are
  named by the file.
- The 351-new-name class carried from P1–P4 was a fragment-built-path blind spot of T029's literal
  search; it is repaired on the assertion/fixture side under T041's "attributed or fixed" clause.
  Per-module changes, root cause and before/after readings: `test-evidence/t041-stale-live-target-repair.md`.
- Guard re-runs: `test_store_layout_live_refs.py` + `test_runtime_store_layout.py` (including
  `test_backward_incompatible_inventory_is_closed`) → 11 passed.
- `sync-mirrors.py --check` exit **0**, **0** DIFF members today (baseline file: 444 DIFF; member-set
  delta new=0 / cured=all); `regen-command-copies.py --check` exit **0**.
- `test ! -e .specify/memory` exit **0**.
- `grep -cE '^- \[[ >]\]' tasks.md` = **43** — every row, including this package's, is still in the
  open form at executor hand-back; tasks.md is on this seat's forbidden-write list, so row marking
  and the GATE-8 evaluation belong to the driver after it collects the writebacks.
- All readings: `test-evidence/t041-final-gate.txt`.
