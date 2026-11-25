# P1 transient test reds — root move landed, live-target test updates follow (T029)

- Date: 2026-11-25
- run_id: `r20261125T022857Z-06dd`
- Scope: package P1 (T001–T009)

## What is red and why

P1 moves the runtime store roots (T004/T005/T008). Existing tests that hardcode the old
`.specify/memory/<store>/` paths are **live-target** carriers that tasks.md schedules for
classification and rewrite in **T029 (US5)**; the full-suite name-level comparison (GATE-5)
runs at **T041**, after that update. Until then these tests fail on their own stale path
expectations, not on an engine defect — one spot-check proves the class:

```console
$ ... run-tests.sh tests/contract/test_exec_quant_engine.py::TestCollectContract::test_collect_writes_storage_and_record -q
E       AssertionError: assert False
E        +  where False = is_dir()
E        +    where is_dir = PosixPath('.../ws/.specify/memory/exec-quant/records')...
1 failed
```

The engine writes `.specify/exec-quant/records`; the test still reads the retired path.

## Final P1 reading (full fast tier, clean tree)

```console
$ SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
    --names-out .specify/specs/105-runtime-store-layout/test-evidence/p1-final-failed.txt
1150 failed, 9066 passed, 4 skipped, 9 errors in (parallel 65.77s + serial pass)
# failed-name list written: .../p1-final-failed.txt (1150 entries) passes=2
```

Name-level delta against the implement-entry baseline (`implement-baseline-failed.txt`, 748 names):

- **404 new** failed names, **2 repaired** (baseline reds that now pass).
- **9 setup errors** are NOT in the names file (the runner's list carries only FAILED nodeids) and are
  disclosed here explicitly, so GATE-5 does not inherit a blind spot:
  `test_exec_quant_channel_boundary.py::{test_aggregated_layer_zero_credential_hits,
  test_package_product_zero_credential_hits, test_payload_carries_only_masked_data,
  test_summary_products_zero_credential_hits}` and
  `test_feedback_probe_cli.py::TestListFiltersAndDispose::{test_dispose_rejects_bad_state,
  test_dispose_sets_disposition_and_filter_finds_it, test_list_filter_by_kind_external,
  test_list_filter_by_kind_internal_excludes_external, test_list_filter_by_slice}`.
  Both groups are fixture-setup writes to `.specify/memory/feedback|exec-quant/...` while the engine
  now reads the new roots — live-target fixtures owned by T029.
- Full log: `test-evidence/p1-final-run.txt`; names: `test-evidence/p1-final-failed.txt`.

All new reds and errors are attributable to the store-root move (T004/T005/T008) and are closed by
T023 (ignore templates), T029 (test live references) and T031 (mirror regeneration); the P1 package
gate itself is the two-file run below.

## Representative batch reading

```console
$ SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
    tests/unit/test_memory_utils.py tests/contract/test_feedback_utils_cli.py \
    tests/contract/test_exec_quant_engine.py tests/contract/test_evidence_utils_cli.py \
    tests/contract/test_trigger_engine.py tests/contract/test_record_retention_engine.py \
    tests/contract/test_sanitize_engine_contract.py tests/contract/test_probe_registry_umbrella.py \
    tests/contract/test_role_edge_engine.py tests/contract/test_seal_engine_contract.py -q
76 failed, 264 passed in 13.00s
```

Name-level comparison against `.specify/specs/105-runtime-store-layout/test-evidence/implement-baseline-failed.txt`:
**73 of the 76** are NEW relative to the implement-entry baseline (the other three were already
red at entry). All 73 are live-target path expectations owned by T029.

Full log retained at `test-evidence/p1-affected-batch.txt` (the complete stdout/stderr of the
batch above).

## P1's own gate (recorded green)

```console
$ SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
    tests/integration/test_init_new_layout.py tests/contract/test_runtime_store_layout.py -q
2 failed, 5 passed in 7.41s
```

The two failures are exactly the allowed residuals — `test_repo_has_no_retired_root`
(dogfood, T033) and `test_mirror_member_set` (mirror regeneration, T031). See
`notes/red-first-evidence.md` § T009 and `test-evidence/t009-us1-verbose.txt`.

## In-passing corrections landed in P1

- `tests/contract/test_anchor_layout_migrate.py` — `PLACEHOLDER_DIR` now points at `seed/`.
- `tests/contract/test_upgrade_end_state.py` — the fake resource tree ships `seed/` (with the two
  tier directories), the external skill's anchor reference is runtime-form `.specify/constitution.md`,
  and the assertion no longer expects the removed `memory` rewrite rule (C-7 forbids it).
- `tests/contract/test_declaration_facts.py` — the 094 pin gains the 105 registration key
  (`runtime-store-layout`) as an append-only addition.
- `tests/contract/test_directory_governance.py` — the map assertion now expects the top-level
  `.specify/housekeeping/` registration (T007's recorded intent); its remaining red is the mirror
  copy, which T031 regenerates.
