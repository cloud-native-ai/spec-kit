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
