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

## T017 — `tests/contract/test_coaching_observation_contract.py` + `tests/contract/test_coaching_dispatch_contract.py`

- Command: `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q tests/contract/test_coaching_observation_contract.py tests/contract/test_coaching_dispatch_contract.py`
- Exit code: `1`
- Failure count: `13 failed, 12 passed`
- Output slice:

```text
FAILED tests/contract/test_coaching_observation_contract.py::test_c1_template_declares_the_five_sections_in_order
FAILED tests/contract/test_coaching_observation_contract.py::test_c1_dispatch_block_carries_the_five_record_fields
FAILED tests/contract/test_coaching_observation_contract.py::test_c2_step_table_carries_the_nine_columns
FAILED tests/contract/test_coaching_observation_contract.py::test_c2_consistency_is_observation_only
FAILED tests/contract/test_coaching_observation_contract.py::test_c3_sources_are_closed_and_host_event_wins_on_conflict
FAILED tests/contract/test_coaching_observation_contract.py::test_c4_gap_marker_lives_only_on_step_rows
FAILED tests/contract/test_coaching_observation_contract.py::test_c5_failure_timeout_and_refusal_keep_their_coordinates
FAILED tests/contract/test_coaching_observation_contract.py::test_c6_no_observation_still_produces_the_record
FAILED tests/contract/test_coaching_dispatch_contract.py::test_c1_every_required_field_is_named_with_its_rule
FAILED tests/contract/test_coaching_dispatch_contract.py::test_c2_the_four_forbidden_classes_are_declared
FAILED tests/contract/test_coaching_dispatch_contract.py::test_c3_single_payload_and_no_retry_with_a_modified_payload
FAILED tests/contract/test_coaching_dispatch_contract.py::test_c4_return_is_recorded_and_never_inflated
FAILED tests/contract/test_coaching_dispatch_contract.py::test_c5_transport_and_payload_reference_are_recorded
```

- Cause: `references/prompt-templates.md` carries only the expectation-side sections, so
  the observation skeleton, the nine-column step table and the gap rules are absent;
  `SKILL.md` has no `## Dispatch Payload` section, so every payload clause is unclaimed.
  The 12 passing tests are the two validators' compliant/counterexample drills (they
  exercise the test helpers, not the skill content).

## T020 — `tests/contract/test_coaching_wiring_contract.py`

- Command: `/Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest -q tests/contract/test_coaching_wiring_contract.py`
- Exit code: `1`
- Failure count: `12 failed, 5 passed`
- Output slice:

```text
FAILED tests/contract/test_coaching_wiring_contract.py::test_c1_eight_identity_coordinates_all_hold
FAILED tests/contract/test_coaching_wiring_contract.py::test_c6_the_old_literal_has_no_live_occurrence_in_the_wiring_surface
FAILED tests/contract/test_coaching_wiring_contract.py::test_c6_the_single_permitted_occurrence_is_the_obsolete_skills_entry
FAILED tests/contract/test_coaching_wiring_contract.py::test_c6_each_named_face_carries_zero_occurrences[.qoder/agents]
FAILED tests/contract/test_coaching_wiring_contract.py::test_c6_each_named_face_carries_zero_occurrences[.specify/agents/templates]
FAILED tests/contract/test_coaching_wiring_contract.py::test_c6_each_named_face_carries_zero_occurrences[.specify/shared/definitions]
FAILED tests/contract/test_coaching_wiring_contract.py::test_c6_each_named_face_carries_zero_occurrences[.specify/memory/feedback/probe-map.md]
FAILED tests/contract/test_coaching_wiring_contract.py::test_c6_the_old_mirror_directory_is_gone_and_the_new_one_exists
FAILED tests/contract/test_coaching_wiring_contract.py::test_c3_mirrors_and_command_copies_are_zero_drift
FAILED tests/contract/test_coaching_wiring_contract.py::test_c4_cleanup_removes_the_entity_directory
FAILED tests/contract/test_coaching_wiring_contract.py::test_c7_the_four_frozen_rosters_carry_the_new_name
FAILED tests/contract/test_coaching_wiring_contract.py::test_c8_the_verification_surface_runs_green
```

- Cause: the route row still names the retired skill (coordinate 7), the shared mirrors
  and the old mirror directory are not regenerated yet (C-3, C-6), the retired directory
  name is not in `_OBSOLETE_SKILLS` yet (C-4), and the four frozen rosters still carry
  the old name (C-7, owned by T027). The 5 passing tests are the face-derivation drills.
