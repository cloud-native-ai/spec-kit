# Red-First Evidence — Feature 070 implement

Append-only record of each new-behavior test row's failing run and its red-to-green transition. A green check that would not turn red when its subject breaks is not cited as proof.

## T005 + T006 — foundational gate contract and unit tests (red)

- **Date**: 2026-10-24T17:12Z
- **Host**: Linux 5.10.134-15.2.al8.x86_64 x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed paths (new, test-only)**:
  - `tests/contract/test_sdd_loop_driver_wp_gate.py`
  - `tests/unit/test_wp_gate.py`
  - `tests/fixtures/wp_fixtures.py` (T004 support)
- **Command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_gate.py tests/unit/test_wp_gate.py
  ```
- **Real output (tail)**:
  ```text
  FFFFFFFFFFFFFFFFFFF.FFF                                                  [100%]
  =============================== short test summary info ================================
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_script_path_and_stdlib_only
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_cli_grammar_and_defaults
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_plan_json_takes_precedence_over_spine
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_stage_attempt_defaults_to_highest_in_spine
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_preflight_requires_manifest_when_owned_paths_exist
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_json_envelope_shape
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_evidence_ptr_is_null_without_json_out
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_exit_codes_cover_zero_one_two
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_finding_order_is_stable_and_sorted
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_gate_never_writes_spine_or_plan
  FAILED tests/contract/test_sdd_loop_driver_wp_gate.py::test_retry_check_requires_wp_arguments
  FAILED tests/unit/test_wp_gate.py::test_read_spine_reads_plan_amendment_and_ledger
  FAILED tests/unit/test_wp_gate.py::test_effective_plan_applies_amendments_in_seq_order
  FAILED tests/unit/test_wp_gate.py::test_canonical_hash_excludes_hash_slot_keys_and_timestamps
  FAILED tests/unit/test_wp_gate.py::test_canonical_hash_is_sha256_hex
  FAILED tests/unit/test_wp_gate.py::test_schema_missing_for_absent_required_field
  FAILED tests/unit/test_wp_gate.py::test_schema_failures_skip_the_hash_check
  FAILED tests/unit/test_wp_gate.py::test_plan_hash_mismatch_is_a_reject
  FAILED tests/unit/test_wp_gate.py::test_exit_two_when_neither_spine_nor_plan_json
  FAILED tests/unit/test_wp_gate.py::test_exit_two_on_malformed_ledger_line
  FAILED tests/unit/test_wp_gate.py::test_exit_two_when_no_plan_fence_matches
  FAILED tests/unit/test_wp_gate.py::test_ledger_stage_attempt_contributes_to_the_default
  22 failed, 1 passed in 0.49s
  ```
- **Exit code**: `1`
- **Root cause**: `skills/external/sdd-loop-driver/scripts/wp-gate.py` does not exist yet; every case fails on the missing script.
- **Disclosed false green**: the single passing case is `test_exit_two_on_malformed_plan_json`. It passed because CPython itself exits 2 when told to open a nonexistent script file, not because the gate handled malformed JSON. Once the script exists the assertion still discriminates (a traceback would exit 1), so the case is kept; it is not cited as red evidence for gate behaviour.

## T007 + T008 — foundational gate green

- **Date**: 2026-10-24T17:20Z
- **Changed path (new, implementation)**:
  - `skills/external/sdd-loop-driver/scripts/wp-gate.py`
- **Command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_gate.py tests/unit/test_wp_gate.py
  ```
- **Real output**: `....................... [100%]` / `23 passed in 0.66s`
- **Exit code**: `0`
- **Transition**: `22 failed, 1 passed` (script absent) → `23 passed` (foundational layer landed). The one red-run green (`test_exit_two_on_malformed_plan_json`) now passes through the gate's own `InputError` path, not CPython's missing-file exit.
- **Scope note**: this green covers WG-01…WG-05 (path, stdlib-only, CLI grammar and defaults, plan-json precedence, stage-attempt default, preflight manifest input requirement, JSON envelope, exit 0/1/2, deterministic finding order, never-writes-spine) and the foundational core (plan/amendment/ledger fence reading, required-field `schema-missing`, schema-before-hash ordering, canonical hash exclusions, exit-2 inputs). Graph checks, preflight checks, and retry checks remain unimplemented and return exit 2 until T011/T017; they are not claimed green here.
