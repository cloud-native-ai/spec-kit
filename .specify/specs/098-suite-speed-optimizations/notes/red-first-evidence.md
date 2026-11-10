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
