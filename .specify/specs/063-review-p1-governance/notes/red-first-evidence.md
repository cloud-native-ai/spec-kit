# Red-first evidence

Owner: T005 / T016 / T025 / T030 / T035 / T040. Each section records the command,
the real exit code, and the real red output. Red is only valid when the failure reason
is the missing artifact/behaviour — not a mis-written assertion.

---

## T005 — US1 red (C-1..C-10)

Date: 2026-10-19 (UTC). Repo root: `/storage/project/cloud-native-ai/spec-kit`.

Command:

```
python3 -m pytest tests/contract/test_clause_forms.py tests/contract/test_clause_coverage.py \
  tests/contract/test_review_p1_checklist_governance.py \
  tests/contract/test_review_p1_recheck_waiver.py -q --tb=line
```

Exit code: **1** — `26 failed, 67 passed in 25.88s`.

Of the 26 failures, **2 are the frozen baseline failures** already listed in
`notes/baseline-failed-tests.txt` (lines 4–5):

```
tests/contract/test_clause_coverage.py::test_c5_gate_budget_is_unchanged_by_the_owner_document
tests/contract/test_clause_forms.py::test_the_four_md_forms_never_co_occur_in_one_file
```

The remaining **24 are the deliberately red new assertions**. Real one-line reasons:

```
tests/contract/test_clause_forms.py:324: AssertionError: owner § 4 rule 2 MUST name the delimiter '（'
tests/contract/test_clause_forms.py:337: AssertionError: assert [] == ['FR-001']
tests/contract/test_clause_forms.py:345: AssertionError: assert [] == ['外层（FR-018）尾部']
tests/contract/test_clause_forms.py:356: AttributeError: module 'clause_extract' has no attribute 'malformed_parentheticals'
tests/contract/test_clause_forms.py:368: AttributeError: module 'clause_extract' has no attribute 'malformed_parentheticals'
tests/contract/test_clause_forms.py:378: AttributeError: module 'clause_extract' has no attribute 'malformed_parentheticals'
tests/contract/test_clause_coverage.py:1057: AssertionError: analyze MUST name the coverage accountant (C-5)
tests/contract/test_clause_coverage.py:1078: AssertionError: Delegation Inputs MUST name the checklist surface (C-3)
tests/contract/test_clause_coverage.py:1091: AssertionError: the freeze duty MUST land in Runtime-evidence landing points (C-6)
tests/contract/test_review_p1_checklist_governance.py:49: AssertionError: the load table MUST gain exactly one `checklists/*.md` row; got []
tests/contract/test_review_p1_checklist_governance.py:65: AssertionError: Delegation Inputs MUST name the checklist surface (C-3)
tests/contract/test_review_p1_checklist_governance.py:76: AssertionError: the pass MUST name the [Gap] tag
tests/contract/test_review_p1_checklist_governance.py:85: AssertionError: the marker MUST carry a machine-readable key
tests/contract/test_review_p1_checklist_governance.py:107: AssertionError: the report MUST make the undispositioned count observable
tests/contract/test_review_p1_recheck_waiver.py:49: AssertionError: the recheck filename form MUST be declared literally
tests/contract/test_review_p1_recheck_waiver.py:62: AssertionError: every answered entry MUST quote the requirement line it answers
tests/contract/test_review_p1_recheck_waiver.py:83: AssertionError: the third branch MUST be driven by the recheck record
tests/contract/test_review_p1_recheck_waiver.py:93: AssertionError: assert None
tests/contract/test_review_p1_recheck_waiver.py:104: AssertionError: the waiver format MUST carry the `Scope` part
tests/contract/test_review_p1_recheck_waiver.py:112: AssertionError: the `Closed` part MUST be described
tests/contract/test_review_p1_recheck_waiver.py:120: AssertionError: assert None
tests/contract/test_clause_coverage.py::test_c5_baseline_missing_is_phase_visible_with_its_remedy
tests/contract/test_clause_coverage.py::test_c7_both_sides_name_the_accountants_same_default_path
tests/contract/test_review_p1_recheck_waiver.py::test_c8_original_checklist_is_never_refreshed_in_place
```

Attribution check (sample `-q --tb=short` for the two headline mechanisms):

```
test_cross_width_pairing_is_malformed_never_a_citation
  AttributeError: module 'clause_extract' has no attribute 'malformed_parentheticals'
test_c3_load_table_has_a_checklists_row
  AssertionError: the load table MUST gain exactly one `checklists/*.md` row; got []
```

Both name an absent artifact/API, not a faulty expectation. Red is valid.

---

## T016 — US2 red (C-11..C-15)

Date: 2026-10-19 (UTC).

Command:

```
python3 -m pytest tests/contract/test_review_p1_review_loop.py -q --tb=line
```

Exit code: **1** — `10 failed in 0.04s` (no baseline failures: this is a new file).

Real one-line reasons (all name an absent artifact/behaviour):

```
test_c11_handoff_after_names_the_registration_obligation
  AssertionError: the ownerless sentence MUST be replaced
test_c12_id_register_enumeration_adds_rec
  AssertionError: the enumeration MUST add the recommendation identifier
test_c12_live_instructions_received_rec_through_the_generator
  AssertionError: the live .specify/instructions.md MUST carry REC- (generated, never hand-edited)
test_c13_scope_guard_keeps_local_and_names_the_existing_intake
  AssertionError: the legal intake MUST be named
test_c14_section_5_and_rule_3_make_repo_relative_primary
  AssertionError: § 5 MUST name the repo-relative primary form
test_c14_external_targets_are_marked_with_a_reason
  AssertionError: a target with no repo-relative form MUST be marked `external`
test_c14_absolute_only_instruction_is_not_reintroduced
  AssertionError: the header MUST NOT keep the absolute-only instruction
test_c15_review_owns_the_ready_for_review_transition
  AssertionError: the review transition row MUST be present
test_c15_checklist_row_is_annotated_and_keeps_one_transition_per_command
  AssertionError: the checklist row MUST carry the annotation
test_c15_top_command_list_includes_review
  AssertionError: the document's top command list MUST include /speckit.review
```

Red is valid: every failure names content that has not landed yet.

## US3 — T023/T024 red run (2026-10-20, implement attempt 2 续跑)

Command:

```
python3 -m pytest tests/contract/test_probe_engine_action_sets.py tests/contract/test_engine_face_contract.py -q
```

Result: **17 failed, 7 passed** (exit 1). The 7 green legs are the C-24
"must-remain byte-for-byte" pins (duplicate → `{"duplicate": true}` exit 0,
no second record, no run-id minting — existing behavior already satisfies the
clause, so green-before-and-after is the correct shape for an idempotivity
pin) plus the renderer-no-handwritten-table structural pin over the CURRENT
renderer.

Failed (artifact-missing reasons, verbatim assertion tails):

```
test_feedback_utils_action_set_exact
  AssertionError: feedback-utils.py --action set drifted: missing=['args-manifest']
test_rundet_action_set_exact
  AssertionError: run-determination.py ACTIONS set drifted: missing=['args-manifest']
test_exec_quant_action_set_exact
  AssertionError: exec-quant.py action set drifted: missing=['args-manifest']
test_c22_all_wrap_up_engines_expose_args_manifest
  AssertionError: run-determination.py --action args-manifest failed (rc=2):
  … error: argument --action: invalid choice: 'args-manifest' (choose from 'determine', 'settle', 'history')
test_c22_manifest_flags_live_on_the_engine_parser
  (same missing-action cause)
test_c22_determine_manifest_carries_the_normative_sets
  (same missing-action cause)
test_c22_record_manifest_required_set
  (same missing-action cause)
test_c20_face_renders_required_and_source_placeholders
  AssertionError: the determine line MUST render the required set as placeholders
  (rendered line today: `… --action determine --unit-id "/speckit.sandbox-a" --unit-type command` — no args tail)
test_c20_convention_is_declared_in_the_registry_note
  AssertionError: the placeholder convention MUST be declared in the registry § Handler note
test_c20_convention_line_rendered_once_verbatim
  (no convention line rendered today)
test_c20_no_placeholder_free_section_carries_no_convention
  (registry note lacks the declaration the negative leg reads)
test_c21_rendered_flags_are_exactly_the_manifest_set
  (manifests missing; rendered set today = base pair + --action only)
test_c22_missing_manifest_fails_the_compile_loudly
  AssertionError: mutation must actually strip the manifest action
  (engines carry no "args-manifest" literal yet — the strip is a no-op)
test_c20_repo_compiled_face_carries_the_full_argument_form
  AssertionError: '--run-id <RUN_ID>' in <templates/commands/implement.md ## Wrap-up> is False
test_c23_determine_lists_all_missing_args_in_one_error
  AssertionError: '--complexity' in 'error: --run-id is required: the key is (unit_id, run_id)' is False
  (sequential one-at-a-time error today — the exact C-23 defect)
test_c23_determine_missing_unit_id_joins_the_one_error
  (same sequential cause)
test_c23_record_lists_all_missing_args_in_one_error
  AssertionError: missing --review MUST be named in the one error:
  error: --run-id is required.  (sequential one-at-a-time error today)
```

Red is valid: every failure names a mechanism that has not landed yet
(args-manifest actions, manifest-driven rendering, registry convention
declaration, one-shot missing-arg errors), not a mis-written assertion.

## US4 — T029/T030 red run (2026-10-20, implement attempt 2 续跑)

Command:

```
python3 -m pytest tests/contract/test_evidence_binding_contract.py -q --no-header
```

Result: **17 failed, 2 passed** (exit 1).

The 2 green legs are must-remain pins, not mis-written assertions:
- `test_c26_existing_sections_preserved_additive_only` — the template's pre-existing
  section set is intact (the additive-only baseline holds now and MUST hold after the
  landing);
- `test_c27_reuses_the_existing_handler_no_new_subsystem` — with the gate unregistered,
  no new handler exists; after the landing it MUST stay green by reusing the existing
  `h-gate-evidence` handler id.

All 17 red legs fail for artifact-missing reasons (assertion tails, verbatim):

- C-26 template legs (5) — `templates/verification-log-template.md` lacks the section:
  - `test_c26_section_sits_between_results_and_sc_evaluation` →
    `ValueError: substring not found` on `"# -- Evidence records"` (text.index)
  - `test_c26_declares_the_four_record_fields` →
    `AssertionError: verification-log-template.md lacks the `# -- Evidence records ... --`
    section (C-26: it MUST sit between the implement-results and SC evaluation markers)`
    (via `_evidence_section`)
  - `test_c26_declares_sha256_over_the_archived_files_bytes` /
    `test_c26_evidence_path_is_declared_repo_relative` /
    `test_c26_pass_requires_a_complete_evidence_row` → same `_evidence_section` assertion
- C-27 registration legs (4) — registry rows and skill reference absent:
  - `test_c27_gate_row_registered_beside_the_checklist_waiver` →
    `ValueError: '| gate-implement-evidence-binding | command-gate | /speckit.implement |
    gate-implement-evidence-binding |' is not in list`
  - `test_c27_handler_binding_row_at_confirm_gate` →
    `AssertionError: the h-gate-evidence HandlerBinding MUST subscribe to this gate at
    @point:confirm-gate`
  - `test_c27_skill_step9_references_the_gate` →
    `AssertionError: implement-feature Step 9 (the verification-log step) MUST reference
    the gate — the skill has no per-feature GATE numbering; this step owns the evidence
    the gate checks`
  - `test_c27_skill_step9_states_the_check_and_the_observation_protocol` →
    `AssertionError` on the exists/non-empty/SHA-256/门控观察协议/--lifecycle-point
    declarations in Step 9
- C-28 drill legs (8) — the checker derives its parser from the template's declared
  section, so the absent section fails every drill:
  - `test_c28_matching_pass_is_green_and_only_that` /
    `test_c28_missing_artifact_is_red_naming_sample_and_reason` /
    `test_c28_empty_artifact_is_red_naming_sample_and_reason` /
    `test_c28_hash_mismatch_is_red_naming_sample_and_reason` /
    `test_c28_non_pass_verdict_carries_no_binding_duty` /
    `test_c28_pass_without_evidence_section_is_unverified` /
    `test_c28_incomplete_evidence_row_is_unverified` →
    `_evidence_section` assertion (the template lacks the declared section)
  - `test_c28_red_is_not_downgraded_anywhere` → same `_evidence_section` assertion
    (the no-downgrade rule cannot be read from a section that does not exist)

Red is valid: every failure names a mechanism that has not landed yet (the template's
evidence-record section, the registry gate row + HandlerBinding, the Step 9 gate
reference), not a mis-written assertion.

## US5 — T034/T035 red run (2026-10-20, implement attempt 2 续跑)

Command:

```
python3 -m pytest tests/contract/test_baseline_preflight_contract.py -q --no-header
```

Result: **9 failed, 0 passed** (exit 1).

All 9 legs fail for artifact-missing reasons (assertion tails, verbatim):

- C-29 legs (8) — `skills/internal/implement-feature/SKILL.md` has no pre-flight step
  before Step 1; every leg fails at `_preflight_step`:
  `AssertionError: implement-feature SKILL.md lacks a pre-flight step before Step 1
  (C-29: the baseline re-capture MUST run before any other workflow step)`
  (legs: sits_before_step1 / directory_derived_set / write_back_citing_rows /
  classification_before_verdict / git_log_provenance / undecidable_explicit /
  missing_baseline_first_capture)
- C-30 legs (2) — `templates/commands/implement.md` states no pre-flight duty:
  - `test_c30_command_face_states_the_preflight_duty_before_the_how_to_call` →
    `AssertionError: templates/commands/implement.md MUST state the pre-flight duty
    in its Skill Delegation inputs (C-30)`
  - `test_c30_command_face_carries_the_same_obligation_shape` →
    `AssertionError: the pre-flight duty paragraph must be locatable in the command
    face`

Red is valid: every failure names a mechanism that has not landed yet (the skill's
pre-flight step, the command-face duty statement), not a mis-written assertion.

## US6 — T039/T040 red run (2026-10-20, implement attempt 2 续跑)

Command:

```
python3 -m pytest tests/contract/test_premise_carrier_contract.py -q --no-header
```

Result: **9 failed, 2 passed** (exit 1).

The 2 green legs are must-remain pins, not mis-written assertions:
- `test_c16_item2_keeps_the_reference_instead_of_restate_duty` — the existing duty
  survives now and MUST survive the carrier-list opening;
- `test_c19_producer_side_recapture_obligation_retained` — the producer-side
  re-capture obligation exists now and MUST be retained when the timing text is
  re-pointed.

All 9 red legs fail for artifact-missing reasons (assertion tails, verbatim):

- C-16 (2) — item 2 still carries the closed enumeration and lacks the open carriers:
  - `test_c16_item2_no_longer_names_only_the_two_closed_carriers` →
    `AssertionError: item 2 still carries the closed two-carrier enumeration — the
    duty must not be escapable by sitting in an unlisted carrier`
  - `test_c16_item2_covers_assumption_decision_and_free_prose` →
    `AssertionError: the open list MUST cover assumptions` (first missing carrier)
- C-17 (3) — the ACTION REQUIRED comment lacks the date+pointer rule:
  - `test_c17_action_required_declares_date_and_pointer` →
    `AssertionError: the ISO date stamp MUST be required`
  - `test_c17_both_together_neither_alone` →
    `AssertionError: the rule MUST state both requirements together — either alone is
    non-compliant (Edge Cases)`
  - `test_c17_rule_reaches_any_carrier` →
    `AssertionError: the date+pointer rule MUST apply to rows in ANY carrier, not only
    the two originally listed`
- C-18 (3) — the red-first note shape rule lacks the verbatim-quote duty:
  - `test_c18_note_shape_rule_requires_verbatim_gate_row_quote` →
    `AssertionError: a note binding a claim to a gate MUST quote the gate row verbatim`
  - `test_c18_bare_gate_id_alone_is_forbidden` →
    `AssertionError: a bare gate id alone MUST NOT be usable, so renumbering produces
    a visible mismatch`
  - `test_c18_forward_applicable_only_062_out_of_scope` →
    `AssertionError: the rule MUST be declared forward-applicable only`
- C-19 (1) — the timing text does not point at the implement-side consumer:
  - `test_c19_refreeze_points_at_the_implement_preflight` →
    `AssertionError: Re-freeze timing MUST point at the implement-side consumer step
    (the C-29 pre-flight) instead of describing a duty this command cannot execute`

Red is valid: every failure names a mechanism that has not landed yet (the open
carrier list, the date+pointer rule, the verbatim gate-row quote, the consumer-side
pointer), not a mis-written assertion.
