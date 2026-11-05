# Regression baseline comparison (improve-skills ssh-utils loop)

Run date: 2026-11-05. Target: `skill:sdd-project-setup` → new sibling `skill:ssh-utils`.

## Method

- Full contract suite captured once: `.specify/.tmp/ssh-utils-test/contract-full.log`
  (5728 passed, 23 failed before the loop's count-pin fixes).
- Baseline worktree created at `HEAD` (`git worktree add --detach`), seeded with the
  unrelated pre-existing working-tree changes (the concurrent Feature 083
  skill-reference wiring and agent render changes) and **without** this loop's files.
- The same failing test ids were re-run in both trees.

## Result

| Failure | Baseline worktree | Current tree |
|---------|------------------|--------------|
| `test_clause_forms::test_the_four_md_forms_never_co_occur_in_one_file` | fail | fail (pre-existing) |
| `test_coaching_run_contract::test_c1_inputs_declare_exactly_two_parameters_and_verbatim_work` | fail | fail (pre-existing) |
| `test_coaching_wiring_contract::test_c1_eight_identity_coordinates_all_hold` | fail | fail (pre-existing) |
| `test_confirmation_gates_sweep::test_residual_total_within_sc002_target` | fail (27 > 23.25) | fail (pre-existing) |
| `test_evidence_findings_schema::...package_zip_contains_no_evidence_paths` | fail | fail (pre-existing) |
| `test_exec_quant_engine` (7 tests) | fail | fail (pre-existing environment/config) |
| `test_expression_compatibility::test_c5_non_wiring_files_keep_their_frozen_hashes` | fail (concurrent skill-reference edits) | fail (pre-existing) |
| `test_fast_fail_discipline::test_g9_total_equals_frozen_baseline` | fail (23 → 27) | fail (pre-existing) |
| `test_neutrality_budget::test_c5_the_cap_leaves_zero_integer_headroom` | fail | fail (pre-existing) |
| `test_proactive_trigger_section::test_c11_gate_scan_total_unchanged` | fail | fail (pre-existing) |
| `test_shared_reference_rewrite::test_skills_use_installed_absolute_shared_form` | fail (17 unrelated offenders) | fail (same 17; `ssh-utils` removed from the list) |
| `test_shipped_surface_client_neutrality::...` | fail | fail (pre-existing) |
| `test_token_efficiency_discipline::test_cd5_headings_only_in_discipline_doc` | fail | fail (pre-existing) |

Count-pin failures introduced by the new unit and fixed this loop:

- `test_coaching_wiring_contract::test_c3_probe_compiled_face_is_zero_drift` (76 → 77)
- `test_coaching_wiring_contract::test_c8_the_verification_surface_runs_green` (`matched=80` → 81)
- `test_ledger_reconciliation` (80 → 81)
- `test_probe_nonentity_catalog` (118 → 119)

## Verdict

Current-tree failure set equals the baseline failure set (19 pre-existing failures);
no regression attributable to this loop. The new `tests/contract/test_ssh_utils_skill.py`
passes 11/11.
