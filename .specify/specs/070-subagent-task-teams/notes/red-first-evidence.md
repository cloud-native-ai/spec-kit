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

## T009 + T010 — WP model contract tests and plan-check unit tests (red)

- **Date**: 2026-10-24T17:20Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed paths (new, test-only)**:
  - `tests/contract/test_sdd_loop_driver_wp_model.py` (new)
  - `tests/unit/test_wp_gate.py` (extended; `--check plan` section)
  - `tests/fixtures/wp_fixtures.py` (E4 event builders, single-package plan)
- **Command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_model.py tests/unit/test_wp_gate.py
  ```
- **Real output (summary)**:
  ```text
  39 failed, 59 passed in 2.42s
  ```
- **Exit code**: `1`
- **Failing groups (real)**:
  - Model contract (18): `test_wp_02`, `test_wp_03`, `test_wp_04`, `test_wp_05`, `test_wp_06`, `test_wp_07`, `test_wp_08`, `test_wp_09`, `test_wp_10`, `test_wp_11`, `test_wp_12`, `test_wp_13`, `test_wp_14`, `test_wp_15`, `test_wp_16`, `test_wp_17`, `test_wp_18`, `test_or_02`.
  - Plan checks (21): duplicate/dangling/cycle, three orphan-output shapes, duplicate output (package claim and integrator claim), integrator entry outside `required_outputs`, three boundedness rejects, three kind cases, seven pattern cases, and the `not-beneficial` advisory.
- **Root cause**: `wp-gate.py` has no graph/output/bounded/kind/pattern/benefit checks and emits no `dispatch_layers`/`integration_order`; `references/decomposition-model.md` does not exist, so every runtime-owner citation assertion fails.
- **Disclosed greens**: 39 cases pass in the red run and are **not** cited as new-behaviour evidence: the 18 `WP-01` schema cases, the `OR-01`/`OR-03`…`OR-16` contract-text pins (anti-drift guards on already-landed owner contracts), the `E4` field-set fixtures, and the consumed-intermediate positive case. They discriminate on owner/fixture edits but do not prove the missing gate behaviour.

## T011 + T012 — plan checks and runtime-owner part 1 (green)

- **Date**: 2026-10-24T17:24Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed paths (implementation)**:
  - `skills/external/sdd-loop-driver/scripts/wp-gate.py` (WG-06…WG-13 plan checks, `dispatch_layers`, `integration_order`)
  - `skills/external/sdd-loop-driver/references/decomposition-model.md` (new runtime-owner part 1)
- **T011 command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_gate.py tests/unit/test_wp_gate.py
  ```
- **T011 real output**: `52 passed in 1.70s`; exit code `0`.
- **T012 command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_model.py
  ```
- **T012 real output**: `57 passed in 1.38s`; exit code `0`.
- **Transition**: `39 failed, 59 passed` (T009+T010 red, before the implementation) → `52 passed` for the gate pair → `57 passed` for the model contract after the runtime owner landed.
- **In-scope defect disclosed**: the red run exposed that the amendment hash chain was validated against the *effective* plan hash rather than the base plan fence hash. `_load_plan` now carries `base_plan_hash` and `_amendment_hash_findings` starts the chain there. No contract or plan-owned artifact changed; the contract (WP-07/V-AMD.2) already required the base chain.
- **Interpretation recorded**: WG-13's "declared budgets" weight are each package's `max_turns` for the critical-path comparison; this is the only declared budget quantity in E1/E2. A gate verdict of `single-package` for a non-beneficial multi-package candidate is the `auto` resolution input (FN-04); the driver remains responsible for rewriting the plan decision and for the `on` precedence (FN-02).
- **Non-regression**: the existing driver targeted suite (`test_decomposition_check.py`, `test_pre_analyze_check.py`, `test_overlap_check.py`, `test_sdd_loop_driver_gates.py`, `test_sdd_loop_driver_skill.py`) is `65 passed in 18.04s`, identical to the pre-change baseline.

## T013 — US1 verification (green)

- **Date**: 2026-10-24T17:25Z
- **Command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_model.py tests/unit/test_wp_gate.py
  ```
- **Real output**: `98 passed in 2.63s`; exit code `0`.
- **US1 green points**: WG-06 schema, WG-07 graph, WG-08 output coverage (including the authoritative integrator carve-out), WG-09 boundedness, WG-10 kind, WG-11 pattern, WG-12 hash/amendment chain, WG-13 benefit/advisory; WP-01…WP-18 and OR-01/OR-02 runtime-owner citations; E4 event field sets and fixtures; single-package representation.
- **Quickstart Scenario A**: executed the documented command against a fixture plan (`--spine` + `--plan-json` + `--json-out`) → `verdict=admit`, `findings=[]`, `dispatch_layers=[["plan-wp01","plan-wp02"]]`, `integration_order=["plan-wp01","plan-wp02"]`, exit `0`; the `--json-out` file is byte-equivalent to stdout JSON. Pinned in `test_sdd_loop_driver_wp_gate.py::test_json_envelope_shape` and `test_sdd_loop_driver_wp_model.py::test_wp_04`.
- **Quickstart Scenario B**: the plan-check portion rejects a cyclic, orphaned fixture with `cycle` + `orphan-output`, exit `1` (pinned in `test_wp_gate.py::test_dependency_cycle_rejects` and `test_orphan_required_output_rejects`). The third expected finding, `path-overlap`, belongs to `--check preflight` (WG-15) and is recorded as deferred to T017 (US2); the current build exits `2` for that check by design, which the driver treats as `decomposition-unavailable`, never as a plan rejection.
- **Disclosed coverage boundary**: the OR-03…OR-16 pins in the model contract test are anti-drift assertions on the already-landed owner contract and E4/E11/E12 schema; behavioural metric computation is exercised by `tests/unit/test_wp_report.py` in T027/T028. They are not cited as evidence for the plan-gate behaviour.
- **E3 stage-status row**: appended to `test-evidence/implement-stage-status.jsonl` with this command, the selected paths, rc 0, 98 passed, and the E2 baseline pointer.
