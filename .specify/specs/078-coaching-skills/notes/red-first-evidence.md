# Red-First Evidence — Feature 078

Each entry records the command, a representative slice of the real output, the exit
code and the failure count. Readings were taken on the pre-implementation tree of the
part-2 segment (base `a7aa0793`), with the test files present and the skill content
not yet written.

Re-confirmation after the green phase (same test files, implementation temporarily
restored from `HEAD` and then byte-verified back): combined run `22 failed, 8 passed`,
exit code `1` — the per-file readings below (15/5 and 7/3) are unchanged.

## T009 — `tests/contract/test_coaching_run_contract.py`

- Command: `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q tests/contract/test_coaching_run_contract.py`
- Exit code: `1`
- Failure count: `15 failed, 5 passed`
- Output slice:

```text
FAILED tests/contract/test_coaching_run_contract.py::test_c1_inputs_declare_exactly_two_parameters_and_verbatim_work
FAILED tests/contract/test_coaching_run_contract.py::test_c2_resolution_reuses_the_run_skills_ladder_without_a_second_rule
FAILED tests/contract/test_coaching_run_contract.py::test_c2_hit_counting_and_fail_closed_cases
FAILED tests/contract/test_coaching_run_contract.py::test_c3_run_id_shape_directory_and_fail_closed_on_existing_directory
FAILED tests/contract/test_coaching_run_contract.py::test_c4_four_artifacts_in_order_with_dispatch_evidence
FAILED tests/contract/test_coaching_run_contract.py::test_c5_execution_is_primary_and_optimization_never_shortens_it
FAILED tests/contract/test_coaching_run_contract.py::test_c6_exactly_one_dispatch_and_no_retry_after_failure
FAILED tests/contract/test_coaching_run_contract.py::test_c7_both_dimensions_evidence_and_two_deviation_classes
FAILED tests/contract/test_coaching_run_contract.py::test_c8_entries_name_a_location_and_are_still_produced_without_evidence
FAILED tests/contract/test_coaching_run_contract.py::test_c9_optimization_uses_the_entry_and_points_at_the_single_claim_owner
FAILED tests/contract/test_coaching_run_contract.py::test_c10_closed_domains_recording_location_and_fr017_boundary
FAILED tests/contract/test_coaching_run_contract.py::test_c11_ladder_is_closed_and_zero_observation_keeps_the_plan
FAILED tests/contract/test_coaching_run_contract.py::test_c12_one_dispatch_mechanism_with_a_recorded_mode
FAILED tests/contract/test_coaching_run_contract.py::test_c13_skill_stays_external_and_new_lines_add_no_blocking_gate
FAILED tests/contract/test_coaching_run_contract.py::test_c14_payload_carries_only_the_two_readings_and_never_the_coach_conclusions
```

- Cause: the skill body still carries the pre-rename static-simulation sections
  (`## Workflow`, `## Output Template`); every required coaching-run section is absent.
  The five passing tests are the artifact-shape validator's own compliant/counterexample
  drills, which exercise the test helper rather than the skill body.

## T014 — `tests/contract/test_coaching_expectation_contract.py`

- Command: `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q tests/contract/test_coaching_expectation_contract.py`
- Exit code: `1`
- Failure count: `7 failed, 3 passed`
- Output slice:

```text
FAILED tests/contract/test_coaching_expectation_contract.py::test_c1_template_carries_every_mandatory_heading_in_order
FAILED tests/contract/test_coaching_expectation_contract.py::test_c1_expectation_path_and_dispatch_ordering_are_declared
FAILED tests/contract/test_coaching_expectation_contract.py::test_c2_closed_acceptance_forms_and_oc1_primary_deliverable
FAILED tests/contract/test_coaching_expectation_contract.py::test_c3_pe_columns_magnitude_profile_retries_and_critical_path
FAILED tests/contract/test_coaching_expectation_contract.py::test_c4_derivation_reuses_the_mental_simulation_contract_and_logic_audit
FAILED tests/contract/test_coaching_expectation_contract.py::test_c4_audit_result_is_recorded_in_the_expectation_file
FAILED tests/contract/test_coaching_expectation_contract.py::test_c5_expectation_phase_declares_the_four_prohibitions
```

- Cause: `references/prompt-templates.md` still holds the retired thought-experiment
  fragments; none of the expectation skeleton, derivation method or zero-side-effect
  sections exists. The three passing tests are the document validator's drills.
