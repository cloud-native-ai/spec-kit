# Pre-change measurements — Feature 061 (T001/T002)

Dated record, captured at implementation start on 2026-10-18, before any 061 source edit.
All commands ran from the repo root (`/Users/liuqiming.lqm/project/cloud-native-ai/spec-kit`).

## T001 — Generation-face baseline

```text
$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (21 files)
ok    skills/external/ == .specify/skills/ (369 files)
ok    skills/internal/ == .specify/skills/internal/ (136 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (108 files)
ok    shared/ == .specify/shared/ (51 files)
# exit 0

$ python3 scripts/python/regen-command-copies.py --check
OK: all per-tool command copies match the source templates.
# exit 0

$ python3 scripts/python/probe-utils.py --action compile-embeds --check
compile-embeds --check: 73 units, zero drift
# exit 0
```

**Trap note (shared count)**: the current `shared` count is **51**, not the 50 recorded in
plan.md's dated record. The extra pair is the untracked `shared/guidelines/progress-reporting.md`
(+ its `.specify/` mirror), which is **excluded from 061**. 061's verify criterion is zero NEW
drift on its own touched pairs, never the absolute shared count.

**Trap note (generation-time test tree)**: tasks.md's generation-time measurement read
`3287 passed` (plan's dated record says 3278) because the untracked
`tests/contract/test_progress_reporting.py` is collected. The T002 re-freeze below is the
baseline of record for implementation.

## T002 — Failing-test baseline (plan-time record preserved, then re-frozen)

Plan-time frozen list (`.specify/specs/061-subagent-cli-config/notes/baseline-failed.txt`,
captured 2026-10-18 before implement): **25 FAILED**, **7** of them in
`tests/contract/test_exec_quant_engine.py` (the affected-file set: qoder reader, endpoint,
masking, size cap, agent collection). The full plan-time list is preserved verbatim in
`notes/baseline-failed.txt` as it was frozen.

Generation-time known swap (from tasks.md's Premise Measurements): compared with the frozen
record, one unrelated node appeared and one disappeared:

- appeared: `tests/contract/test_goal_migration.py::TestLiveSurfacesAreMigrated::test_no_live_face_file_retains_the_old_path`
  — measured cause: a transient `.baseline-check/` directory existed during that run; the
  node passes when re-run alone;
- disappeared: `tests/contract/test_instructions_section_propagation.py::test_c1_live_instructions_carry_all_template_sections`
  — consistent with the excluded dirty instructions changes.

Neither is caused by 061. T002 therefore re-freezes the spec-dir baseline against the current
tree so T027 compares like with like.

Re-freeze run (current tree, 2026-10-18):

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract tests/integration -q --no-header -p no:cacheprovider
```

See `## T002 result` below and `notes/baseline-failed.txt` for the sorted nodeid list of
record used by T027's `comm -13`.

### Plan-time frozen list (25 nodes; preserved verbatim from the pre-implement record)

```text
FAILED tests/contract/test_clause_coverage.py::test_c5_gate_budget_is_unchanged_by_the_owner_document
FAILED tests/contract/test_clause_forms.py::test_the_four_md_forms_never_co_occur_in_one_file
FAILED tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target
FAILED tests/contract/test_constitution_double_landing.py::test_c1_template_carries_both_new_principles
FAILED tests/contract/test_criterion_subject.py::test_c19_the_gate_budget_survives_the_new_section
FAILED tests/contract/test_exec_quant_engine.py::TestAgentCollection::test_resolved_agent_fields_from_wrapper_host
FAILED tests/contract/test_exec_quant_engine.py::TestCredentialDefense::test_engine_masks_credential_shaped_config_values
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_endpoint_candidates_origin_only
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_missing_config_face_degrades_to_marker
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_qoder_adapter_reads_config_face
FAILED tests/contract/test_exec_quant_engine.py::TestLLMCollection::test_qoder_adapter_reads_per_model_effort_when_set
FAILED tests/contract/test_exec_quant_engine.py::TestSizeCap::test_oversized_record_is_field_truncated_and_capped
FAILED tests/contract/test_fast_fail_discipline.py::test_a7_section_counts_20_to_21_and_21_to_22
FAILED tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline
FAILED tests/contract/test_fast_fail_discipline.py::test_i11_channel_two_mirrors_and_per_tool_copies
FAILED tests/contract/test_fast_fail_discipline.py::test_x13_double_landing_three_count_pins
FAILED tests/contract/test_fast_fail_discipline.py::test_x19_ufc_class_eleven_gains_fast_fail_path
FAILED tests/contract/test_fast_fail_discipline.py::test_x21_ufc_override_column_unchanged
FAILED tests/contract/test_instructions_section_propagation.py::test_c1_live_instructions_carry_all_template_sections
FAILED tests/contract/test_neutrality_budget.py::test_c4_budget_total_and_violations_after_the_feature_landed
FAILED tests/contract/test_neutrality_budget.py::test_c5_the_cap_leaves_zero_integer_headroom
FAILED tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged
FAILED tests/contract/test_token_efficiency_discipline.py::test_cd5_headings_only_in_discipline_doc
FAILED tests/contract/test_user_facing_comprehension_doc.py::test_gn_c2_gate_scan_total_unchanged
FAILED tests/contract/test_wrap_up_wording_gate_safe.py::test_confirmation_gate_budget_unchanged
```

## T002 result — re-frozen against the current tree

Commands:

```text
$ /Users/liuqiming.lqm/project/profiles/.venv/bin/python -m pytest tests/contract tests/integration -q --no-header -p no:cacheprovider
24 failed, 3288 passed, 1 skipped, 1 warning in 171.78s (0:02:51)
```

The three new 061 files (engine, defaults template, US1 contract test) were parked inside
the feature's spec directory for this capture, so the tree matched pre-061 reality.

Difference from the plan-time 25-list (set comparison):

- **gone**: `tests/contract/test_instructions_section_propagation.py::test_c1_live_instructions_carry_all_template_sections`
  — consistent with the excluded dirty instructions changes (not 061);
- **transient goal-migration node absent**: the generation-time measurement had one extra
  node (`test_goal_migration.py::TestLiveSurfacesAreMigrated::test_no_live_face_file_retains_the_old_path`)
  caused by a transient `.baseline-check/` directory; it passes on the clean tree and is not
  in this baseline;
- the **7 affected-file nodes** in `tests/contract/test_exec_quant_engine.py` are present
  exactly as in the plan-time list (TestAgentCollection, TestCredentialDefense,
  TestLLMCollection ×4, TestSizeCap).

`notes/baseline-failed.txt` now carries this sorted 24-node list of record for T027.

