# Red-first evidence — 098-suite-speed-optimizations

Each section records one guard file's red run against the pre-change tree, captured
before the behaviour it guards was implemented (run-time output landed outside
`.specify/specs` and was copied here afterwards; corpus-write hazard,
`test-evidence/corpus-write-hazard.txt`).

## WP-1 / T004 — `tests/contract/test_suite_tier_contract.py` (tier-selection §E obligations 1–10)

- Date: 2026-11-10
- Tree state: `scripts/bash/run-tests.sh` unchanged (no `--full`, no tier injection, no
  `tier=`/`excluded_slow=` fields) — the guard file is the only change on disk.
- Command: `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_suite_tier_contract.py -q`
- Exit code: `1`
- Collected: `11` cases (obligation 3 runs both accepted `-m` spellings); `11` failed, `0` passed.
- Full run-time log: `.specify/.tmp/wp1/red-run.log` (this worktree; scratch, not retained).

Failing cases (all 11):

```text
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_1_default_tier_excludes_the_slow_test
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_2_a_tree_without_slow_tests_equals_the_full_selection
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_3_the_caller_m_owns_the_selection[["-m", "contract"]]
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_3_the_caller_m_owns_the_selection[["-m=contract"]]
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_4_path_and_k_do_not_suppress_the_tier
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_5_full_with_a_caller_m_is_still_the_callers_selection
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_6_serial_mode_never_selects_a_tier
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_7_a_serial_and_slow_test_is_excluded_from_both_fast_passes
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_8_empty_after_exclusion_is_a_named_error
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_9_help_lists_full_and_an_undeclared_option_still_exits_non_zero
FAILED tests/contract/test_suite_tier_contract.py::test_obligation_10_the_header_carries_the_injected_expression
```

Decisive excerpts showing each failure blames the missing mechanism, not a broken
assertion:

```text
# obligation 1 / 4 / 6 / 7: the slow test executes because no default exclusion exists
FAILED tree/test_mixed.py::test_slow_fails - assert False
1 failed, 1 passed in 0.40s

# obligation 2 / 3 / 5: the pre-change runner forwards --full to pytest and discloses no tier
ERROR: usage: __main__.py [options] [file_or_dir] [file_or_dir] [...]
__main__.py: error: unrecognized arguments: --full

# obligation 3: the mode line has no tier= field at all
AssertionError: mode line carries no tier= field: 'workers=2 dist=load passes=2'
```

Anomaly line: none in this record — every failure is the expected red of the guard
against the unchanged runner; no in-passing repair was applied to the guard.

## WP-2 / T010 — slow-membership guard cases (slow-membership C-005…C-009)

- Date: 2026-11-10
- Tree state: the guard cases are the only change on disk — `pyproject.toml` has no
  `slow` registration, `test-evidence/slow-members.md` does not exist, and no test
  carries `@pytest.mark.slow` yet.
- Command: `bash scripts/bash/run-tests.sh --serial tests/contract/test_suite_tier_contract.py -q -k "slow_guard"`
- Exit code: `1`
- Collected: `5` slow-guard cases; `2` failed, `3` passed (`11` deselected tier cases).
- Full run-time log: `.specify/.tmp/wp2/red-guard.log` (this worktree; scratch, not retained).
- Mode line: `mode=serial reason=explicit tier=fast excluded_slow=0`

Failing cases (the red this record owns):

```text
FAILED tests/contract/test_suite_tier_contract.py::test_slow_guard_1_the_registry_and_the_collected_marked_set_are_one_to_one
FAILED tests/contract/test_suite_tier_contract.py::test_slow_guard_5_the_membership_evidence_files_are_the_single_carrier
```

Decisive excerpt showing the failure blames the missing registry, not a broken assertion:

```text
E FileNotFoundError: ... .specify/specs/098-suite-speed-optimizations/test-evidence/slow-members.md
E AssertionError: membership carrier missing: .../test-evidence/slow-members.md
E assert False
2 failed, 3 passed, 11 deselected in 18.11s
```

Guards 2 (real-tree collection equality), 3 (disclosure arithmetic) and 4 (guard not a
member) are green on the empty membership by construction; their discriminating power is
proven by the SL-M1…SL-M5 mutation legs (T013), which redden them on membership drift.

Anomaly line: none in this record — every failure is the expected red of the guard
against the tree without a registry; no in-passing repair was applied to the guard.

## WP-3 / T021 — two-subject guard: two-slot `--full` (FR-010) + obligation 11 (C-015)

- Date: 2026-11-10
- Tree state at the red run: neither reference file carries `--full` yet
  (`efficiency-model.md` slot rows and `stage-prompts.md` restatements unchanged), the
  mirror is pre-sync, and `notes/pre-change-measurements.md` does not exist (T003 has
  not recorded the implement-start id set).
- Command: `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_suite_tier_contract.py -q -k "two_slot or obligation_11"`
- Exit code: `1`
- Result: `2 failed in 0.45s` (`16` deselected).
- Full run-time log: `.specify/.tmp/wp3/red-first.log` (this worktree; scratch, not retained).

Failing cases and the decisive excerpts (each failure blames its missing subject):

```text
FAILED ...::test_the_two_slot_commands_request_the_full_tier
E  AssertionError: .../efficiency-model.md: the baseline slot MUST request the full tier,
   or the default tier can silently shrink the budget:
   | `baseline` | ... | `run-tests.sh --names-out <spec-dir>/baseline-failed.txt`，... |

FAILED ...::test_obligation_11_the_full_collection_never_loses_a_baseline_id
E  AssertionError: the implement-start full-tier id set is not recorded:
   .../notes/pre-change-measurements.md is missing. T003 owns that record (tasks.md T003);
   a missing baseline MUST NOT read as equality (tier-selection C-015).
```

After T018/T019 and the T020 mirror sync the doc-assertion case is green
(`-k "two_slot or obligation_11"` → `1 failed, 1 passed in 0.45s`; the remaining failure is
the obligation-11 baseline subject, whose green owner is T022 after T003 records the id
set). The obligation-11 mechanism was proven on a throwaway copy: a baseline equal to the
copy's own reading passes, renaming one existing test reddens it with the old id named, and
recording that id in `full-collection-disposed.txt` restores green. Details and hashes:
`test-evidence/wp3-two-slot-full.txt`.

Anomaly line: none in this record — every failure is the expected red of the guard against
the tree before its subject exists; no in-passing repair was applied to the guards.

## WP-4 / T014 — `tests/contract/test_parallel_consistency_contract.py` (parallel-consistency C-001…C-006, C-009, C-010…C-012)

- Date: 2026-11-10
- Tree state at the red run: the guard file is the only change on disk — neither
  `test-evidence/parallel-consistency-contract.txt` (T015) nor
  `test-evidence/parallel-consistency-noxdist.txt` (T016) exists.
- Command: `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_parallel_consistency_contract.py -q`
- Exit code: `1`
- Result: `3 failed, 1 passed in 3.48s` (4 collected cases).
- Full run-time log: `.specify/.tmp/wp4/red-first.log` (this worktree; scratch, not retained).

Failing cases (the red this record owns — each blames its missing subject):

```text
FAILED tests/contract/test_parallel_consistency_contract.py::test_the_comparison_record_judges_by_failure_names
FAILED tests/contract/test_parallel_consistency_contract.py::test_the_subset_record_does_not_claim_full_suite_safety
FAILED tests/contract/test_parallel_consistency_contract.py::test_the_no_xdist_record_shows_a_complete_serial_run
```

Decisive excerpt (the comparison case; the other two fail on the same missing carrier):

```text
E  AssertionError: the verification record is missing:
   .../test-evidence/parallel-consistency-contract.txt — T015 owns this record
   (C-012: a record missing its fields does not support the claim)
```

The fourth case, `test_non_parallel_safe_fixture_turns_the_comparison_non_empty` (C-009),
passes by design: it constructs its own non-parallel-safe suite and asserts the
parallel-vs-serial name comparison is non-empty, so its output is a red comparison rather
than a failing case. Its captured output (identical construction, one-off reproduction
`python3 .specify/.tmp/wp4/drill-repro.py`, log `.specify/.tmp/wp4/drill/`):

```text
parallel arm: exit=1
mode=parallel workers=2 dist=load passes=1 tier=fast excluded_slow=0
serial arm:   exit=0
mode=serial reason=explicit tier=fast excluded_slow=0
parallel names: ['tree/test_drill.py::test_alpha']
serial names:   []
comm -13 (serial-only):   []
comm -23 (parallel-only): ['tree/test_drill.py::test_alpha']
comparison non-empty: True
```

(The barrier construction makes exactly one parallel test read the other's write: both
writes precede both reads, so the last writer's value is observed by the other test. The
serial arm's barrier yields immediately without a worker environment, so each test reads its
own write and stays green.)

Anomaly line: none in this record — the three failures are the expected red of the guard
against the tree before its evidence carriers exist, and the drill's non-empty comparison is
the intended discriminator output; no in-passing repair was applied to the guard.

## WP-5 / T024 — `tests/contract/test_scan_cache_contract.py` (scan-cache C-001…C-004, C-007, C-010, C-011)

- Date: 2026-11-10
- Tree state at the red run: the guard file is the only change on disk — `tests/conftest.py`
  carries no scan-cache factory (`ScanCache` / `SCAN_SURFACES` / block markers absent), and
  neither converted corpus file consumes a session payload.
- Command: `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_scan_cache_contract.py -q`
- Exit code: `1`
- Result: `4 failed, 3 errors in 0.55s` (7 collected cases).
- Full run-time log: `.specify/.tmp/wp5/red-first.log` (this worktree; scratch, not retained).

Failing/erroring cases (the red this record owns — each blames its missing subject):

```text
FAILED tests/contract/test_scan_cache_contract.py::test_c002_the_managed_surfaces_are_exactly_the_two_declared
FAILED tests/contract/test_scan_cache_contract.py::test_c003_the_factory_keeps_no_mtime_or_persistent_cache
FAILED tests/contract/test_scan_cache_contract.py::test_c007_the_corpus_build_is_in_process_over_the_house_pattern
FAILED tests/contract/test_scan_cache_contract.py::test_c010_a_new_session_observes_a_tampered_corpus
ERROR tests/contract/test_scan_cache_contract.py::test_c001_c011_one_build_and_one_traversal_serve_two_consumers
ERROR tests/contract/test_scan_cache_contract.py::test_c001_the_variant_is_part_of_the_key
ERROR tests/contract/test_scan_cache_contract.py::test_c004_a_consumer_mutation_never_reaches_the_store
```

Decisive excerpts (two representatives; the errors all name the same missing fixture):

```text
# static case: the factory block markers do not exist yet
E  AssertionError: tests/conftest.py MUST bracket the scan-cache factory between
   'scan-cache begin' and 'scan-cache end' comment markers; the static checks below
   judge that block and nothing else

# drill case: the driver session cannot even construct the factory
E  AttributeError: module '_drill_conftest' has no attribute 'ScanCache'

# fixture-backed cases (three ERRORs): the session fixture does not exist
E  fixture 'scan_cache' not found
```

Anomaly line: none in this record — every failure is the expected red of the guard against
the tree before its subject exists; no in-passing repair was applied to the guard.

## WP-6 / T031 — `tests/contract/test_event_wait_contract.py` (event-wait C-001…C-010)

- Date: 2026-11-10
- Tree state at the red run: the guard file is the only change on disk — the six scope
  files still carry their pre-change sleeps, `wait_until` still defaults to `timeout=5.0`,
  `pointer_entry` has no injected-clock parameter, and `test_sdd_loop_efficiency_runner.py`
  still polls inline.
- Command: `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_event_wait_contract.py -q`
- Exit code: `1`
- Collected: `8` cases; `5` failed, `3` passed.
- Full run-time log: `.specify/.tmp/wp6/red-run2.log` (this worktree; scratch, not retained).
- First red run (`.specify/.tmp/wp6/red-run.log`): same five cases plus `test_c003`, whose
  only defect was the guard's own line-wrapped reason comparison — a guard-side defect
  repaired in passing before this record (whitespace-normalised reason match); the red
  inventory below is the post-repair reading.

Failing cases (the red this record owns):

```text
FAILED tests/contract/test_event_wait_contract.py::test_c002_the_scope_files_carry_zero_synchronization_sleep
FAILED tests/contract/test_event_wait_contract.py::test_c006_c007_the_helper_defaults_are_thirty_seconds_and_a_small_interval
FAILED tests/contract/test_event_wait_contract.py::test_c009_adopted_wait_call_sites_assert_a_deadline_and_a_small_interval
FAILED tests/contract/test_event_wait_contract.py::test_c006_no_inline_polling_loop_in_the_scope_files
FAILED tests/contract/test_event_wait_contract.py::test_c004_entry_creation_uses_the_injected_clock
```

Decisive excerpts (each names its missing subject; the sleep scan names all 16 sites):

```text
# C-002 — the pre-change sleep inventory, file and line (16 hits, 6 files)
tests/contract/test_client_metrics.py:338   :391   :394   :400   :432   :458   :463   :671
tests/integration/test_sdd_loop_efficiency_runner.py:128
tests/integration/test_session_kill_reattach.py:173 :291
tests/contract/test_line_envelope_contract.py:303 :310
tests/contract/test_feedback_probe_cli.py:277
tests/contract/test_store_state_protocol.py:325 :332

# C-006/C-007 — the shared default is the measured pre-change 5.0, not the enacted 30 s
E  AssertionError: C-006/C-007: wait_until's default deadline is the enacted 30 s, got 5.0

# C-006 — the inline poll the shared helper must replace
E  tests/integration/test_sdd_loop_efficiency_runner.py:127

# C-009 — two adopted call sites assert without a named failure message
E  tests/integration/test_session_kill_reattach.py:202: the assert MUST carry a named failure message (C-006)
E  tests/integration/test_session_kill_reattach.py:274: the assert MUST carry a named failure message (C-006)

# C-004 — 17 pointer_entry call sites carry no injected clock
E  tests/contract/test_client_metrics.py:243 :267 :337 :341 :393 :397 :435 :457 :462 :469
   :501 :528 :552 :621 :644 :670 :673
```

The three green-by-construction cases are the clause-derived scope identity (C-001), the
closed exemption registry (C-003, already truthful) and the zero skip/xfail scan (C-006);
their discriminating power comes from the EW-M1…EW-M5 mutation legs (T042).

Anomaly line: one in-passing repair — the guard's C-003 reason comparison originally
matched against raw clause text and read a line-wrap as a wording drift; it now compares
whitespace-normalised text. No product file was touched.

## WP-7 / T043 — `tests/contract/test_inprocess_conversion_contract.py` (inprocess-conversion C-001…C-010)

- Date: 2026-11-11
- Tree state at the red run: the guard file is the only change on disk — `tests/script_api.py`
  carries no in-process helper, `test-evidence/inprocess-conversion.md` does not exist, and
  no contract-area `subprocess.run` site has been converted.
- Command: `bash scripts/bash/run-tests.sh --workers 2 tests/contract/test_inprocess_conversion_contract.py -q`
- Exit code: `1`
- Collected: `8` cases; `7` failed, `1` passed.
- Full run-time log: `.specify/.tmp/wp7/red-first.log` (this worktree; scratch, not retained).

Failing cases (the red this record owns — every failure names the missing manifest):

```text
FAILED tests/contract/test_inprocess_conversion_contract.py::test_c005_the_manifest_is_a_pipe_table_with_the_declared_columns
FAILED tests/contract/test_inprocess_conversion_contract.py::test_c003_c008_every_row_carries_a_reason_and_convert_names_its_route
FAILED tests/contract/test_inprocess_conversion_contract.py::test_c002_keep_rows_use_the_closed_class_set_and_convert_rows_use_a_dash
FAILED tests/contract/test_inprocess_conversion_contract.py::test_c001_every_covered_file_classifies_all_of_its_sites
FAILED tests/contract/test_inprocess_conversion_contract.py::test_c004_fixture_layer_helpers_are_keep_with_the_global_state_class
FAILED tests/contract/test_inprocess_conversion_contract.py::test_c010_the_keep_side_sample_covers_the_named_boundary_kinds
FAILED tests/contract/test_inprocess_conversion_contract.py::test_c006_the_full_tree_scan_names_its_uncovered_files
```

Decisive excerpt:

```text
E  AssertionError: the conversion manifest is missing:
   .../test-evidence/inprocess-conversion.md — generated by T045 from the AST census (C-006)
```

The eighth case, `test_c007_a_reverted_conversion_turns_red_and_names_the_site`, passes by
design: it drives the guard's classifier over a synthetic census whose converted site is
still a `subprocess.run`, so the revert detection is exercised without a manifest. After
T045 the manifest exists and the seven cases above turn green except the full-tree
completeness leg, which stays red for the files WP-8/T052 has not classified yet and names
them (295 site keys over 164 files at WP-7 close; recorded in
`test-evidence/inprocess-guard-wp7.txt` and `inprocess-equivalence-wp7.txt`).

Anomaly line: one in-passing repair, disclosed in `test-evidence/inprocess-equivalence-wp7.txt`
— the WP-5 package's leftover `before-tree` clone inside `.specify/.tmp/wp5/`, which made
four corpus-owner guards red, was moved out of the worktree (reversible quarantine). No
guard case and no converted assertion was weakened to obtain a green.

