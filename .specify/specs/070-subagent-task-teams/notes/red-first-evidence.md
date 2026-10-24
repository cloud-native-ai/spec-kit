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

## T014 — SD-01…SD-16 coordination contract tests (red)

- **Date**: 2026-10-25T01:40Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed path (new, test-only)**: `tests/contract/test_sdd_loop_driver_wp_coordination.py`
- **Command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_coordination.py
  ```
- **Real output (summary)**: `17 failed, 17 passed in 0.22s`; exit code `1`.
- **Failing groups (real)**: `test_model_doc_carries_the_runtime_projection` (the scheduler/retry sections do not exist yet) and the 16 `test_sd_01…test_sd_16` behavioural cases (`wp_driver_sim.schedule` is a T018 stub raising `NotImplementedError`; the preflight-dependent SD-14 case also exits 2 in the current build).
- **Disclosed greens**: the 16 parametrized `test_sd_contract_clause_keeps_its_normative_content` cases plus `test_sd_contract_file_covers_the_closed_clause_set` pin the already-landed `contracts/scheduler-and-dispatch.md`; they discriminate on owner edits but are not cited as new-behaviour evidence.

## T015 — coordination integration dry runs (red)

- **Date**: 2026-10-25T01:41Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed path (new, test-only)**: `tests/integration/test_wp_coordination_dry_runs.py`
- **Command**:
  ```sh
  python3 -m pytest -q tests/integration/test_wp_coordination_dry_runs.py
  ```
- **Real output**: `5 failed in 0.09s`; exit code `1`.
- **Failing cases (real)**: `test_concurrent_read_only_dispatch_overlaps_intervals`, `test_write_serialization_holds_for_the_dependent_write`, `test_ownership_path_rejection_blocks_dispatch`, `test_dependency_unlocks_only_on_a_pass_verdict`, `test_failure_isolation_leaves_unrelated_work_complete` — all blocked on the `wp_driver_sim.schedule` T018 stub; the ownership case additionally depends on the T017 preflight check.

## T016 — preflight and retry gate unit tests (red)

- **Date**: 2026-10-25T01:42Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed path (test-only)**: `tests/unit/test_wp_gate.py` (T016 section)
- **Command**:
  ```sh
  python3 -m pytest -q tests/unit/test_wp_gate.py
  ```
- **Real output (summary)**: `39 failed, 44 passed in 3.17s`; exit code `1`. The 44 passing cases are the 41 pre-existing T006/T010 unit cases plus 3 disclosed accidental greens.
- **Failing groups (real)**: 12 preflight cases (coverage/forbidden/normalization, write-write and read-write overlap, ordered allow, slot cap, isolation, plan-check inclusion) and 27 retry cases (attempt-1 admission, unchanged, budget/scope/topology deltas, malformed delta, exhaustion, split inheritance and split-depth-one).
- **Disclosed accidental greens (not evidence)**: `test_preflight_exit_two_for_unreadable_manifest`, `test_preflight_exit_two_for_malformed_manifest`, and `test_retry_attempt_must_be_positive` pass only because the current build exits 2 unconditionally for `--check preflight|retry`; after T017 they still discriminate through the explicit input guards. No green here is cited for preflight or retry behaviour.

## T017 — preflight and retry gate checks (green)

- **Date**: 2026-10-25T01:55Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed paths (implementation)**:
  - `skills/external/sdd-loop-driver/scripts/wp-gate.py` (WG-14…WG-17 preflight/retry checks, shared plan-check/verdict path, WG-16 owns the `slot_cap` lower bound)
  - `skills/external/sdd-loop-driver/references/decomposition-model.md` (§12 preflight/retry pointers)
  - `tests/unit/test_wp_gate.py` (Scenario B assertion adds `path-overlap`)
- **Command**:
  ```sh
  python3 -m pytest -q tests/unit/test_wp_gate.py
  ```
- **Real output**: `83 passed in 2.93s`; exit code `0`.
- **Adjacent green**:
  - `python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_gate.py tests/contract/test_sdd_loop_driver_wp_model.py` → `68 passed in 1.97s`.
  - Existing driver targeted suite (`test_decomposition_check.py`, `test_pre_analyze_check.py`, `test_overlap_check.py`, `test_sdd_loop_driver_gates.py`, `test_sdd_loop_driver_skill.py`) → `65 passed in 17.02s`, identical to the pre-change baseline.
- **Transition**: `39 failed, 44 passed` (T016 red) → `83 passed`.
- **Quickstart Scenario B (manual, real command shape)**: a fixture with a cycle, an unowned required output, and two unordered writes on `src/generated/` → `verdict=reject`, rc `1`, codes `cycle`, `orphan-output`, `path-overlap`, `write-write-unordered`; `--json-out` is byte-equivalent to stdout JSON. The `path-overlap` finding deferred at T013 is now exercised.
- **Quickstart Scenario D (manual, retry portion)**: with one dispatch in the ledger, attempt 2 without a delta → `retry-unchanged`, rc `1`; attempt 3 → `retry-exhausted`, rc `1`.
- **Disclosed in-scope contract mapping**: WG-06's `slot_cap` schema predicate now checks the type only; WG-16 owns the `1..ceiling` bound, matching the clause split. No plan-owned or contract artifact changed.

## T018 — scheduler model and coordination simulator (green)

- **Date**: 2026-10-25T02:10Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed paths (implementation)**:
  - `tests/fixtures/wp_driver_sim.py` (SD-01…SD-12 logical-clock scheduler, SD-13 prompt check, SD-16 re-entry; `verify`/`integrate` remain T022 stubs)
  - `skills/external/sdd-loop-driver/references/decomposition-model.md` (§13 scheduler/dispatch, §14 retry/escalation, §15 non-regression)
  - `tests/contract/test_sdd_loop_driver_wp_coordination.py` (re-entry order corrected to write priority)
  - `tests/integration/test_wp_coordination_dry_runs.py` (SC-008 nested-driver dry run)
- **Command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_coordination.py tests/integration/test_wp_coordination_dry_runs.py tests/unit/test_wp_gate.py tests/contract/test_sdd_loop_driver_wp_model.py tests/contract/test_sdd_loop_driver_wp_gate.py
  ```
- **Real output**: `191 passed in 5.03s`; exit code `0`.
- **Transition**: T014 `17 failed, 17 passed` and T015 `5 failed` → the two US2 files report `40 passed` (34 coordination contract + 6 dry runs).
- **Quickstart Scenario C**:
  ```sh
  python3 -m pytest -q tests/integration/test_wp_coordination_dry_runs.py -k "concurrent_read_only or write_serialization"
  ```
  → `2 passed, 4 deselected in 0.03s`; the read-only intervals overlap and the write starts after every read ends.
- **Quickstart Scenario G (nested-driver half)**: `-k "nested_driver"` → `1 passed, 5 deselected`; the `no_team_directory` half lands with T026.
- **Non-regression**: the existing driver targeted suite → `65 passed in 17.03s`, identical to the pre-change baseline.
- **Simulator interpretations (disclosed)**:
  - Durations are deterministic logical ticks (default 10); E1 declares no duration field, and every assertion is an interval relation, not wall-clock.
  - SD-10 verification is modeled as an instantaneous step with a fresh `verifier-N` execution id after a complete result. It proves dispatch/wait ordering only; VI-01…VI-06 independence remains the T022 implementation (`verify()` still raises `NotImplementedError`).
  - Write priority is absolute: a ready write dispatches before newly available reads, including on re-entry when its dependency is already verified from the spine.
  - A prompt that fails SD-13 is not dispatched and is marked failed; its dependents stay blocked and the block is recorded.

## T019 — US2 verification (green)

- **Date**: 2026-10-25T02:15Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_coordination.py tests/integration/test_wp_coordination_dry_runs.py tests/unit/test_wp_gate.py
  ```
- **Real output**: `123 passed in 3.07s`; exit code `0`.
- **Red-to-green**: T014 `17 failed, 17 passed` + T015 `5 failed` + T016 `39 failed, 44 passed` → `123 passed` after T017/T018.
- **Quickstart Scenario C**:
  ```sh
  python3 -m pytest -q tests/integration/test_wp_coordination_dry_runs.py -k "concurrent_read_only or write_serialization"
  ```
  → `2 passed, 4 deselected in 0.03s`; the interval assertion reads at least two overlapping read-only intervals and a write interval that begins after every read interval ends.
- **US2 green points**: SD-01 sole coordinator, SD-02 verified readiness, SD-03 write-alone, SD-04 slot cap, SD-05 deterministic order, SD-06 no starvation, SD-07 local native/serial fallback, SD-08 detached runners, SD-09 result collection, SD-10 verifier dispatch, SD-11 failure isolation, SD-12 pass-only unlock, SD-13 anti-nesting, SD-14 resource isolation, SD-15 no new mechanism, SD-16 re-entry; WG-14 manifest coverage/forbidden, WG-15 territory overlaps, WG-16 slot cap/isolation, WG-17 retry admission/delta/inheritance/exhaustion.
- **Adjacent green (already recorded above)**: gate + model contract `68 passed`; existing driver targeted suite `65 passed`, identical to baseline.
- **Disclosed coverage boundary**: VI-01…VI-14 (T020…T022), the report metrics (T027…T030), the preset/adapter (T024…T026), and fallback/non-regression (T034…T036) remain deferred and are not claimed green here.
- **E3 stage-status row**: appended to `test-evidence/implement-stage-status.jsonl` (`substage=impl-s3-us2-coordination`, command above, rc 0, 123 passed, E2 baseline pointer).





## T020 — VI-01…VI-14 contract pins and behavior tests (red)

- **Date**: 2026-10-24T17:45Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed path (test)**: `tests/contract/test_sdd_loop_driver_wp_coordination.py` (VI contract pins, model-doc projection, fourteen behavioral cases)
- **Command**:
  ```sh
  python3 -m pytest -q tests/contract/test_sdd_loop_driver_wp_coordination.py -k "vi_"
  ```
- **Real output (summary)**: `18 failed, 15 passed, 34 deselected in 0.31s`; exit code `1`.
- **Failing groups (real)**: the model-doc projection (the runtime owner has no verification/integration section) and every behavioral VI case — `results_from_schedule`, `verify`, `integrate`, and `run_stage` do not exist yet (`AttributeError`), so VI-01…VI-14 behavior is unimplemented.
- **Disclosed non-evidence greens**: the 15 passing cases are the fourteen clause-content pins and the closed-clause-set pin. They read the unchanged owner contract, so they pass before implementation by design and are anti-drift pins, not new-behaviour evidence.
- **Red-first claim**: every VI behavior assertion fails for a missing implementation, not for a weak or skipped assertion.

## T021 — verification/integration dry runs (red)

- **Date**: 2026-10-24T17:46Z
- **Host**: Linux x86_64 / Python 3.11.11 / pytest 8.4.2
- **Changed path (test)**: `tests/integration/test_wp_coordination_dry_runs.py` (missing output, contradictory output, deterministic integration order, package-sentinel non-promotion, post-integration U4, driver-u4 capability fallback)
- **Command**:
  ```sh
  python3 -m pytest -q tests/integration/test_wp_coordination_dry_runs.py -k "missing_output or contradictory or integration_order_is_deterministic or package_sentinel or stage_u4_runs or driver_u4"
  ```
- **Real output**: `6 failed, 6 deselected in 0.08s`; exit code `1`.
- **Failing group (real)**: every case fails with `AttributeError: module 'fixtures.wp_driver_sim' has no attribute 'results_from_schedule'` (or `run_stage`/`verify`/`integrate`); the verification/integration dry-run path is unimplemented.
- **Red-first claim**: all six scenario assertions are red before T022 and none is skipped or weakened.
