# In-Process Conversion Manifest — 098-suite-speed-optimizations

Carrier owned by `contracts/inprocess-conversion.contract.md`; generated from the AST
census over `tests/**/*.py` (the guard's `scan_sites`) and completed by hand for the
verdicts. One row per discovered `subprocess.run` call site.

Classification reading of the closed boundary set (C-002): `other-interpreter` covers a
non-Python program under test (bash, grep, cp); `process-isolation-subject` covers a
child whose process is itself the subject (pytest runs, fixture drivers).

| file | call_site | verdict | boundary_class | reason |
|------|-----------|---------|----------------|--------|
| `tests/conftest.py` | `_w2_clone_dir :: cp` | keep | other-interpreter | the platform clone helper (cp -cR) is itself the subject |
| `tests/contract/test_archive_migration.py` | `_run :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_binding_model.py` | `_run :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_clause_coverage.py` | `_freeze :: account-clause-coverage.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_clause_coverage.py` | `_run :: account-clause-coverage.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_clause_coverage.py` | `test_c24_the_idiom_is_a_sorted_name_list_consumed_by_comm_not_a_second_form :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_clause_coverage.py` | `test_c24b_the_baseline_is_codepoint_sorted_so_comm_can_consume_it :: python-inline` | keep | process-isolation-subject | an inline python -c probe; its process-local state is the subject |
| `tests/contract/test_clause_coverage.py` | `test_c25_the_baseline_is_not_the_gate_scanner_broken_json_shape :: account-clause-coverage.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_clause_coverage.py` | `test_c5_gate_budget_is_unchanged_by_the_owner_document :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_clause_coverage.py` | `test_c6_the_cap_is_pinned_in_three_forms_with_meta_pins :: grep` | keep | other-interpreter | the named external program is the subject; its own process is required |
| `tests/contract/test_command_family.py` | `_lookup :: flow-class-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_command_family.py` | `_run_engine :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_compile_propagation_order.py` | `test_propagation_chain_is_green_in_canonical_order :: regen-command-copies.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_compile_propagation_order.py` | `test_propagation_chain_is_green_in_canonical_order :: sync-mirrors.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_class_table.py` | `_run_engine :: concurrency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_declarations.py` | `_cli :: declaration_reader.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_declarations.py` | `_engine :: concurrency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_dispatch_capability.py` | `_run_engine :: concurrency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_disposal.py` | `_run_engine :: concurrency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_high_order.py` | `_run_engine :: concurrency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_high_order.py` | `test_stage_runner_help_carries_the_invocation_shape :: stage-runner.sh` | keep | other-interpreter | the bash script is the subject; a bash process is required |
| `tests/contract/test_concurrency_real_run_evidence.py` | `_run_engine :: concurrency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_reproduction_092.py` | `_capability :: concurrency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_serial_reason.py` | `_run_engine :: concurrency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_concurrency_units.py` | `_gate_plan :: wp-gate.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_concurrency_units.py` | `_run_engine :: concurrency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_confirmation_gates_sweep.py` | `run_scanner :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_criterion_subject.py` | `_run :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_criterion_subject.py` | `test_c18_the_engine_suite_that_reads_the_owner_doc_stays_green :: test_goal_targets_engine.py` | keep | process-isolation-subject | the child is a pytest run of another suite; the test process is the subject |
| `tests/contract/test_criterion_subject.py` | `test_c19_the_gate_budget_survives_the_new_section :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_criterion_subject.py` | `test_c4_the_owner_doc_is_still_linked_not_parsed_and_its_pins_still_hold :: <computed>` | keep | process-isolation-subject | the child is a pytest run of another suite; the test process is the subject |
| `tests/contract/test_declaration_facts.py` | `_run :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_delegation_classes.py` | `_run :: flow-class-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_doc_consistency_checker.py` | `_git :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_doc_consistency_checker.py` | `_run :: doc-consistency-check.py` | keep | global-state-unrecoverable | cwd= callers resolve a relative --path inside the child; cwd-free calls take the in-process branch (C-004) |
| `tests/contract/test_doc_consistency_checker.py` | `test_c04_evidence_asof_fresh_against_last_commit :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_doc_consistency_checker.py` | `test_c04_evidence_clean_annotation_passes :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_doc_consistency_checker.py` | `test_client_shape_duplicate_face_compares_against_mirror_owners :: doc-consistency-check.py` | keep | copy-topology | the subject is the client project's projected .specify/ engine copy and its resolution |
| `tests/contract/test_doc_consistency_checker.py` | `test_client_shape_resolves_every_owner_from_the_mirror :: doc-consistency-check.py` | keep | copy-topology | the subject is the client project's projected .specify/ engine copy and its resolution |
| `tests/contract/test_document_structure_gate.py` | `_run :: doc-consistency-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_expression_compatibility.py` | `_git :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_expression_compatibility.py` | `_lookup :: flow-class-check.py` | keep | copy-topology | the subject is the client project's projected engine copy, run from the client root |
| `tests/contract/test_expression_faces.py` | `_run :: flow-class-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_expression_faces.py` | `_run_duplicate :: <computed>` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_fast_fail_discipline.py` | `_scan_json :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_fast_fail_discipline.py` | `test_g3_counting_unit_is_matching_lines :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_fast_fail_discipline.py` | `test_x19_ufc_class_eleven_gains_fast_fail_path :: test_user_facing_comprehension_doc.py` | keep | process-isolation-subject | the child is a pytest run of another suite; the test process is the subject |
| `tests/contract/test_fast_fail_discipline.py` | `test_x21_ufc_override_column_unchanged :: test_user_facing_comprehension_doc.py` | keep | process-isolation-subject | the child is a pytest run of another suite; the test process is the subject |
| `tests/contract/test_flow_class_correctness.py` | `_run :: flow-class-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_flow_class_ledger.py` | `_run :: flow-class-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_flow_class_ledger.py` | `_tracked_files :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_flow_class_spec_declaration.py` | `_run :: flow-class-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_git_closeout_contract.py` | `_advance_remote :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_git_closeout_contract.py` | `_advance_remote :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_git_closeout_contract.py` | `live_gate_ids :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_git_closeout_contract.py` | `test_the_wrap_up_handler_row_exists_at_order_sixty :: probe-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_git_workflow_observe.py` | `_git :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_git_workflow_observe.py` | `_run :: git-workflow-observe.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_git_workflow_observe.py` | `test_assess_dispatches_the_registered_situation_handler :: trigger-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_git_workflow_observe.py` | `test_registry_validation_and_wrap_up_face_stay_green :: probe-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_handoff_contract.py` | `_run :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_isomorphism_map.py` | `_engine :: flow-class-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_ledger_reconciliation.py` | `_run :: flow-class-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_loop_state_contract.py` | `_run :: loop-state.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_measure.py` | `_run :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_migration_interruption.py` | `_run :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_neutrality_budget.py` | `_git :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_neutrality_budget.py` | `_summary :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_neutrality_budget.py` | `test_c14_the_two_channel_trigger_set_is_closed_and_ci_is_not_available :: grep` | keep | other-interpreter | the named external program is the subject; its own process is required |
| `tests/contract/test_neutrality_budget.py` | `test_c14_the_two_channel_trigger_set_is_closed_and_ci_is_not_available :: grep` | keep | other-interpreter | the named external program is the subject; its own process is required |
| `tests/contract/test_no_spec_local_writes.py` | `_help_actions :: goal-utils.py` | keep | cli-contract | the case reads --help output; the console-entry contract is the subject |
| `tests/contract/test_non_disposable_contract.py` | `_porcelain :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_non_disposable_contract.py` | `_run :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_non_disposable_contract.py` | `porcelain.test_t089_read_only_leg_can_go_red_when_a_tracked_path_is_touched :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_non_disposable_contract.py` | `test_t089_read_only_leg_can_go_red_when_a_tracked_path_is_touched :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_non_disposable_contract.py` | `test_t089_read_only_leg_can_go_red_when_a_tracked_path_is_touched :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_non_disposable_contract.py` | `test_t092_the_mirror_is_the_generators_copy_and_carries_no_hand_edit :: sync-mirrors.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_non_regression_064.py` | `test_ng_04_watcher_exit_codes_unchanged :: watch-target.sh` | keep | other-interpreter | the bash script is the subject; a bash process is required |
| `tests/contract/test_non_regression_064.py` | `test_ng_08_mirror_no_new_drift :: sync-mirrors.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_non_regression_064.py` | `test_ng_08_mirror_no_new_drift :: sync-mirrors.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_non_regression_064.py` | `test_ng_08_mirror_no_new_drift :: sync-mirrors.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_parallel_lines.py` | `_run :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_parallel_lines.py` | `test_authorize_records_the_archive_layer_not_a_scope_name :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_parallel_lines.py` | `test_authorize_records_the_archive_layer_not_a_scope_name :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_parallel_lines.py` | `test_authorize_records_the_archive_layer_not_a_scope_name :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_phase2_bindings.py` | `test_validate_green_with_phase2_rows :: probe-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_phase2_bindings.py` | `test_wrap_up_compile_unaffected_by_phase2_rows :: probe-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_proactive_trigger_section.py` | `installed_project :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_proactive_trigger_section.py` | `run_generator :: generate-instructions.sh` | keep | other-interpreter | the bash script is the subject; a bash process is required |
| `tests/contract/test_proactive_trigger_section.py` | `test_c11_gate_scan_total_unchanged :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_resident_backfill.py` | `_run :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_run_checks.py` | `_run :: <computed>` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_run_checks.py` | `test_c11_json_is_accepted_on_either_side_of_the_action_and_goes_through__emit :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_run_checks.py` | `test_c11_json_is_accepted_on_either_side_of_the_action_and_goes_through__emit :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_run_checks.py` | `test_c27_every_prose_surface_points_at_the_same_invocation :: regen-command-copies.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_run_checks.py` | `test_c4_the_help_line_is_labelled_read :: goal-utils.py` | keep | cli-contract | the case reads --help output; the console-entry contract is the subject |
| `tests/contract/test_run_skills_wiring.py` | `test_c9_compile_embeds_zero_drift_75_units :: probe-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_scan_confirmation_gates.py` | `run_scanner :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_scope_resolution.py` | `_run :: goal-utils.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_script_interface_contract.py` | `_added_paths :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_script_interface_contract.py` | `_checker_exceptions_payload :: script-interface-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_script_interface_contract.py` | `_collect_only :: <computed>` | keep | process-isolation-subject | the child is a pytest --collect-only run; its collection is the subject |
| `tests/contract/test_script_interface_contract.py` | `_consumers_of_the_guard :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_script_interface_contract.py` | `_feature_base :: requires_action.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_script_interface_contract.py` | `_git :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_script_interface_contract.py` | `_git_paths :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_script_interface_contract.py` | `_run_checker :: script-interface-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_script_interface_contract.py` | `_run_engine :: <computed>` | keep | cli-contract | the engine is run as a script so its console-entry shape and exit codes are the subject |
| `tests/contract/test_script_interface_contract.py` | `_run_in_python :: open-ended.sh` | keep | other-interpreter | the bash script is the subject; a bash process is required |
| `tests/contract/test_script_interface_contract.py` | `_run_in_tree :: open-ended.sh` | keep | other-interpreter | the bash script is the subject; a bash process is required |
| `tests/contract/test_script_interface_contract.py` | `_run_sync :: sync-mirrors.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_script_interface_contract.py` | `_tree_snapshot :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_script_interface_contract.py` | `snapshot.test_c15_the_engine_writes_nothing_inside_the_repository :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_script_interface_contract.py` | `test_c13_probe_inconclusive_names_its_finding_at_exit_1 :: both.py` | keep | copy-topology | the subject is a projected script copy; its path identity and self-sufficiency are asserted |
| `tests/contract/test_script_interface_contract.py` | `test_c1_walk_only_is_reported_as_its_own_source :: both.py` | keep | copy-topology | the subject is a projected script copy; its path identity and self-sufficiency are asserted |
| `tests/contract/test_script_interface_contract.py` | `test_c20_the_mirror_copy_resolves_to_its_own_root :: projected.py` | keep | copy-topology | the subject is a projected script copy; its path identity and self-sufficiency are asserted |
| `tests/contract/test_script_interface_contract.py` | `test_c20_the_mirror_copy_resolves_to_its_own_root :: script-interface-check.py` | keep | copy-topology | the subject is a projected script copy; its path identity and self-sufficiency are asserted |
| `tests/contract/test_script_interface_contract.py` | `test_c36_the_projection_is_self_sufficient :: helper.py` | keep | copy-topology | the subject is a projected script copy; its path identity and self-sufficiency are asserted |
| `tests/contract/test_script_interface_contract.py` | `test_c36_the_projection_is_self_sufficient :: helper.py` | keep | copy-topology | the subject is a projected script copy; its path identity and self-sufficiency are asserted |
| `tests/contract/test_script_interface_contract.py` | `test_c36_the_projection_is_self_sufficient :: helper.py` | keep | copy-topology | the subject is a projected script copy; its path identity and self-sufficiency are asserted |
| `tests/contract/test_script_interface_contract.py` | `test_t076_the_projection_inlines_the_body_through_the_sentinel :: guard-only.sh` | keep | other-interpreter | the bash script is the subject; a bash process is required |
| `tests/contract/test_script_interface_contract.py` | `test_t076_the_projection_inlines_the_body_through_the_sentinel :: guard-only.sh` | keep | other-interpreter | the bash script is the subject; a bash process is required |
| `tests/contract/test_script_interface_contract.py` | `test_t076_the_version_text_function_is_published_and_defaults_its_own_constants :: script-interface.sh` | keep | other-interpreter | the bash script is the subject; a bash process is required |
| `tests/contract/test_script_interface_contract.py` | `test_t078_no_command_gate_or_second_checker_was_added :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_script_interface_contract.py` | `test_t078_no_command_gate_or_second_checker_was_added :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_script_interface_contract.py` | `test_t078_the_new_executable_artifacts_are_exactly_what_c32_names :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_script_interface_contract.py` | `test_t084_the_live_goal_utils_position_is_read_and_judged :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_script_interface_contract.py` | `test_t084_the_live_goal_utils_position_is_read_and_judged :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_script_interface_contract.py` | `test_t084_the_live_goal_utils_position_is_read_and_judged :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_scripts_distribution_parity.py` | `test_repo_has_no_orphan_or_drifted_scripts :: sync-mirrors.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_sdd_compat_containment.py` | `_gate_report :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_sdd_compat_containment.py` | `test_c11_the_flow_class_inventory_stays_clean :: flow-class-check.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_sdd_compat_containment.py` | `test_c7_the_routing_engine_keeps_one_closed_action_set :: sdd-route.py` | keep | cli-contract | the case asserts the engine's --help action line; the process contract is the subject |
| `tests/contract/test_sdd_diffusion.py` | `test_trigger_edit_moves_no_gate :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_sdd_loop_driver_cli_profiles.py` | `observe.test_clp_10_observation_fixture_cardinality :: cli_observation.py` | keep | process-isolation-subject | the observation fixture is exercised as a standalone script; its process is the subject |
| `tests/contract/test_sdd_loop_driver_cli_profiles.py` | `test_clp_10_observation_fixture_cardinality :: feedback-utils.py` | keep | copy-topology | the subject is the .specify/ mirror copy of the engine |
| `tests/contract/test_sdd_loop_driver_cli_profiles.py` | `test_clp_11_marker_retrievable :: feedback-utils.py` | keep | copy-topology | the subject is the .specify/ mirror copy of the engine |
| `tests/contract/test_sdd_loop_driver_cli_profiles.py` | `test_clp_11_marker_retrievable :: feedback-utils.py` | keep | copy-topology | the subject is the .specify/ mirror copy of the engine |
| `tests/contract/test_sdd_loop_driver_cli_profiles.py` | `test_clp_12_probe_object_registered :: probe-utils.py` | keep | copy-topology | the subject is the .specify/ mirror copy of the engine |
| `tests/contract/test_sdd_loop_driver_cli_profiles.py` | `test_clp_17_no_063_duplicate_owner :: check-063-overlap.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_sdd_loop_driver_cli_profiles.py` | `test_clp_17_no_063_duplicate_owner :: check-063-overlap.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_status_digest.py` | `_run_digest :: status-digest.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_status_digest.py` | `test_c42_the_generator_reports_no_drift :: regen-command-copies.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_sync_mirrors_only.py` | `_run :: sync-mirrors.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_temp_goal_contract.py` | `test_goal_engine_validates_the_archive_definition :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_temp_goal_contract.py` | `test_list_names_the_migrated_goal_and_never_the_spec_tree :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_temp_goal_contract.py` | `test_resolve_scope_returns_the_archive_roots :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_temp_goal_contract.py` | `test_retired_spec_scope_is_refused :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_temp_team_schema.py` | `test_authorize_resolves_the_team_from_the_archive :: sdd-route.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_temp_team_schema.py` | `test_retired_team_scopes_are_refused :: sdd-route.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_temp_team_schema.py` | `test_run_checks_resolves_the_team_from_the_archive :: goal-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_trigger_engine.py` | `run_cli :: trigger-utils.py` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/contract/test_trigger_engine.py` | `test_c2_sync_mirrors_check_clean :: sync-mirrors.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_trigger_engine.py` | `test_c7_mirror_invocation_resolves_the_repo_not_specify :: trigger-utils.py` | keep | copy-topology | the subject is the .specify/ mirror copy and the root it resolves to |
| `tests/contract/test_user_facing_comprehension_doc.py` | `_changed_files :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_user_facing_comprehension_doc.py` | `_changed_files :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/contract/test_user_facing_comprehension_doc.py` | `test_gn_c2_gate_scan_total_unchanged :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/contract/test_wrap_up_wording_gate_safe.py` | `test_confirmation_gate_budget_unchanged :: scan-confirmation-gates.py` | convert | — | in-process main(argv) with the same stdout/stderr and exit-code assertions (C-003) |
| `tests/fixtures/cli_observation.py` | `record_feedback :: <computed>` | keep | copy-topology | the default engine is the .specify/ mirror copy; the delivered copy is the subject |
| `tests/fixtures/client_project.py` | `git :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/client_project.py` | `run_engine :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/fixtures/client_project.py` | `run_script :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/fixtures/git_closeout/repo.py` | `_git :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/line_fixtures.py` | `git :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/line_fixtures.py` | `make_git_repo :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/line_fixtures.py` | `make_git_repo :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/line_fixtures.py` | `make_git_repo :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/line_fixtures.py` | `make_git_repo :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/line_fixtures.py` | `make_git_repo :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/line_fixtures.py` | `process_token :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/fixtures/line_fixtures.py` | `run_engine :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/fixtures/line_fixtures.py` | `run_watcher :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/fixtures/nested_sdd.py` | `run_authorize :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/fixtures/review_git_repo.py` | `git :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/review_git_repo.py` | `run_script :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` | `git_commit :: git` | keep | git-external | git is the external command under test (history or fixture state) |
| `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` | `run_watcher :: <computed>` | keep | global-state-unrecoverable | the invocation reads cwd/env (or the fixture sets it on the child) and the engine walks it (C-004) |
| `tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` | `run_watcher :: bash` | keep | other-interpreter | the named external program is the subject; its own process is required |
| `tests/script_api.py` | `run_generate_instructions :: generate-instructions.sh` | keep | other-interpreter | the bash generator is the subject; a bash process is required |
