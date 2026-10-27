# Red-First Evidence — Feature 071 (implement stage)

**Opened**: 2026-10-27 at implement part 1 (T001), HEAD `30391ec38ac6de1466254d76febb66cb3ee54710`
**Owner of the obligation**: `contracts/tests-and-docs-sync.md` **C-66** — red-first is a duty of *each of the six groups*, not of the suite as a whole; each group is run before the mechanism it pins exists, and its failing run is recorded with **command line, real output, exit code, failing count**, reviewably rather than asserted. A group that cannot go red when its subject breaks is a fast-fail finding, never coverage.

**Status of this file**: the six group sections below are *scaffolding opened by T001 and filled by their own rows* — T004, T005, T010, T014, T019, T024 write the red run; T009, T013, T018, T023, T028 (plus T027's neighbouring re-run and T030's pin) write the red→green transition. No group may be counted as covered while its section still reads `pending`. Nothing in this file is a claim until it carries a real command, a real exit code, and a real failing count.

## The six new contract test files (C-65 a–f)

| # | Test file | Contract file it pins | C-65 group | Red run written by | Subject that must be able to break |
|---|---|---|---|---|---|
| 1 | `tests/contract/test_review_code_composition.py` | `contracts/command-orchestration.md` | (a) the command template's two segments and their fixed order; (b) the three applicability values | T004 (red) → T009 (green) | the composed surface of `templates/commands/review.md` — segments, order, triage values, two-artifact rule, report subsection content |
| 2 | `tests/contract/test_review_docs_isomorphism.py` | `contracts/tests-and-docs-sync.md` (declared-surface isomorphism) | (f) documentation/template isomorphism | T005 (red) → T034 (green) | the declared surface of `docs/reference/commands/review.md` vs `templates/commands/review.md`; red by construction while the page still describes a process-only review |
| 3 | `tests/contract/test_code_review_skill_contract.py` | `contracts/code-review-skill.md` | (e) the base-resolution rule; (a) triage predicate and empty-delta rule; renderer-mode selection | T010 (red) → T013 (green, base band) and T016/T017 (green, US3 bands) | `skills/internal/code-review/scripts/git-delta-review.sh` `base`/`triage` and the skill's renderer-absence clause |
| 4 | `tests/contract/test_coverage_receipt.py` | `contracts/coverage-receipt.md` | (d) the receipt's exit `1` on a gap and exit `2` on a state it cannot evaluate | T014 (red) → T018 (green) | the `receipt` subcommand — block grammar, closed exit alphabet, gap-vs-skip, three-way count agreement |
| 5 | `tests/contract/test_status_gate_owner.py` | `contracts/status-gate-ownership.md` | (c) the state-machine gate conditions | T019 (red) → T023 (green) | the `Implemented → Ready for Review` owner row and the two initiating rows that reference it |
| 6 | `tests/contract/test_review_feedback_boundary.py` | `contracts/feedback-and-boundaries.md` | (coupled to (a)/(c)) the feedback classification duty and the closing-face invariants | T024 (red) → T028 (green) | the classification duty on both surfaces, the three-unit census, the unchanged closing step set |

**Absence check at T001**: all six files are absent from the tree (they are created by T004/T005/T010/T014/T019/T024), which is the state a red run requires.

## Group 1 — `tests/contract/test_review_code_composition.py`

- Red run (T004): **2026-10-27** at implement part 2, HEAD `b7f0cadc` (clean tree), before any
  edit of `templates/commands/review.md` or `templates/review-template.md`.
- Command line: `python3 -m pytest -q tests/contract/test_review_code_composition.py`
- Real output (tail): `26 failed, 5 passed in 0.19s`
- Failing tests (26, by name): `test_c01_exactly_two_segments_in_a_fixed_order`,
  `test_c01_no_parameter_selects_one_segment_over_the_other`,
  `test_c02_the_two_severity_vocabularies_are_never_merged`,
  `test_c03_process_segment_runs_on_every_invocation`,
  `test_c04_both_segments_are_delegated_by_named_runtime_path`,
  `test_c05_process_abort_does_not_suppress_the_code_segment`,
  `test_c05_the_command_authors_a_minimal_report_when_none_exists`,
  `test_c06_triage_is_a_closed_three_value_set`,
  `test_c06_not_applicable_needs_a_basis_and_not_evaluated_a_reason`,
  `test_c07_the_code_path_predicate_has_exactly_one_owner`,
  `test_c07_an_empty_delta_is_triaged_before_the_receipt_runs`,
  `test_c08_review_object_is_the_committed_delta`,
  `test_c08_uncommitted_changes_are_excluded_and_disclosed`,
  `test_c11_two_artifacts_that_never_overwrite_each_other`,
  `test_c11_record_existence_follows_the_triage_value`,
  `test_c12_rotation_uses_the_utc_second_timestamp_form`,
  `test_c13_the_record_is_reachable_from_the_feature_side`,
  `test_c14_two_verifiable_carriers_and_a_presentational_closing_summary`,
  `test_c15_a_code_finding_keeps_severity_plus_location`,
  `test_c16_handoffs_keeps_its_registration_obligation`,
  `test_c09_the_report_carries_a_code_segment_subsection`,
  `test_c09_subsection_content_list_is_closed`,
  `test_c09_the_four_counts_are_copied_from_the_receipt_block`,
  `test_c10_no_opinion_bodies_and_no_per_item_counts_are_copied`,
  `test_c05_the_subsection_is_fillable_as_the_whole_minimal_report`,
  `test_c09_every_placeholder_in_the_subsection_is_glossed`
- Exit code: `1`
- Failing count: **26 of 31** (the 5 that pass are the negative / unchanged-surface assertions —
  `test_c04_no_skill_methodology_is_inlined`, the three `test_c16_*` rows and
  `test_c09_existing_top_level_section_numbers_are_stable`. They are green on the
  pre-composition tree **by construction**: they pin what the feature must NOT change or
  inline. They are the group's regression half, so their greenness is the expected state on
  both sides of the change, not evidence of coverage.)
- Red → green (T009): **green on 2026-10-27** after T006 (`templates/commands/review.md`
  composition + triage), T007 (`templates/review-template.md` `### 2.1`) and T008 (output /
  placement / closing rules).
  - Command line: `python3 -m pytest -q tests/contract/test_review_code_composition.py`
  - Real output: `31 passed in 0.11s`
  - Exit code: `0`
  - Failing count: `0` (was 26). No assertion was relaxed, renamed away or deleted between the
    two runs: the diff between red and green is the two templates only.
  - The five assertions that were already green at red time stayed green, so the group's
    regression half did not move while its behaviour half flipped.

### T009 — quickstart coverage of Scenario B and Scenario C

Scenario B's four observable results, each against a passing assertion in group 1 (the command
is a prompt, so the assertion pins the text, which is what `quickstart.md` declares as the
scenario's status):

| # | Scenario B observable result | Passing assertion |
|---|---|---|
| 1 | `review.md` is written first (process segment), then `code-review.md` (code segment) | `test_c01_exactly_two_segments_in_a_fixed_order` (the two `### Segment N —` declarations must be process-then-code in that order) |
| 2 | `review.md` § 2.1 carries the closed content list, with the four counts **copied from the receipt block** | `test_c09_the_report_carries_a_code_segment_subsection`, `test_c09_subsection_content_list_is_closed`, `test_c09_the_four_counts_are_copied_from_the_receipt_block`, `test_c09_every_placeholder_in_the_subsection_is_glossed` |
| 3 | The two verifiable carriers are that subsection and the feature detail's `## Latest Review` entry; the closing summary is a presentation, not a third artifact | `test_c13_the_record_is_reachable_from_the_feature_side`, `test_c14_two_verifiable_carriers_and_a_presentational_closing_summary` |
| 4 | The code severity words appear only in `code-review.md`; the process report shows `P0`/`P1`/`P2` only | `test_c10_no_opinion_bodies_and_no_per_item_counts_are_copied` (zero code-vocabulary literals in § 2.1) plus `test_c02_the_two_severity_vocabularies_are_never_merged` (no row pairs the two families) |

Scenario C's `not-applicable` path:

| Expected | Assertion, or the recorded reason it is not asserted here |
|---|---|
| the code segment is recorded `not-applicable` **with the predicate's basis** | `test_c06_not_applicable_needs_a_basis_and_not_evaluated_a_reason`, `test_c07_an_empty_delta_is_triaged_before_the_receipt_runs` |
| **no** `code-review.md` is created — not even an empty one | `test_c11_record_existence_follows_the_triage_value` |
| `review.md` § 2.1 still carries the verdict and the reason | `test_c09_subsection_content_list_is_closed` (the `not-evaluated`/basis rows are part of the closed list), `test_c05_the_subsection_is_fillable_as_the_whole_minimal_report` |
| the feature detail entry repeats it | `test_c13_the_record_is_reachable_from_the_feature_side` |
| **the process segment's reader-baseline conclusion is unchanged** | recorded reason, not asserted here: that conclusion is owned by `shared/workflow/expression-gates.md` and pinned by `tests/contract/test_expression_gates_doc.py`, whose C-8 row is the reader-baseline owner. Asserting it a second time in this group would be the duplicate-criteria shape this feature removes. Measured instead: `python3 -m pytest -q tests/contract/test_review_p1_review_loop.py tests/contract/test_expression_gates_doc.py` → `28 passed in 0.07s` (10 + 18, equal to the frozen per-file counts) **after** both template edits, so the reader-baseline face is untouched by them. T027 re-runs the neighbouring net formally. |

## Group 2 — `tests/contract/test_review_docs_isomorphism.py`

- Red run (T005): **2026-10-27** at implement part 2, HEAD `b7f0cadc`, same tree as group 1.
- Command line: `python3 -m pytest -q tests/contract/test_review_docs_isomorphism.py`
- Real output (tail): `4 failed, 5 passed in 0.08s`
- Failing tests (4, by name): `test_the_two_segments_are_declared_on_both_sides`,
  `test_the_two_artifacts_are_declared_on_both_sides`,
  `test_the_three_applicability_values_are_declared_on_both_sides`,
  `test_the_code_severity_family_is_declared_on_both_sides`
- Exit code: `1`
- Failing count: **4 of 9**
- Reading: the failures are exactly the declared-surface axes the page does not carry —
  `docs/reference/commands/review.md` still documents a process-only review (no `code
  segment`, no `code-review.md`, no `blocked`/`not-*` triage values, no code severity family).
  The two self-checks (`test_the_comparison_tolerates_a_cosmetic_reword`,
  `test_the_comparison_detects_a_deleted_segment`) pass, which is the group's own proof that it
  reds on a deletion and not on a reword (C-65's "would stay green when its subject breaks"
  test).
- Red → green (T034): pending — stays red by design until T031 rewrites the docs page.
  Intermediate state measured after part 2 (T006/T007/T008 landed, page not yet rewritten):
  `python3 -m pytest -q tests/contract/test_review_docs_isomorphism.py` → `5 failed, 4 passed
  in 0.08s`, exit `1`. The four per-axis failures plus `test_the_declared_surfaces_are_equal`
  are all the page's side now — the template declares `{process segment, code segment}`,
  `{review.md, code-review.md}`, the three triage values and `{blocking, praise}`, and the page
  declares none of them. The group therefore still reds for its own reason and not because a
  template sentence changed.


## Group 3 — `tests/contract/test_code_review_skill_contract.py`

- Red run (T010): **2026-10-27** at implement part 3, HEAD `a6625f32` (clean tree),
  before any edit of `skills/internal/code-review/scripts/git-delta-review.sh` or of
  `skills/internal/code-review/SKILL.md`.
- Command line: `python3 -m pytest -q tests/contract/test_code_review_skill_contract.py`
- Real output (tail): `38 failed, 1 passed in 1.81s`
- Failing tests (38, by name): `test_us2_base_source_vocabulary_is_closed_and_reachable`,
  `test_us2_an_explicit_base_wins_the_first_tier`,
  `test_us2_the_feature_tier_uses_the_first_add_and_not_the_latest_commit`,
  `test_us2_the_same_repository_state_resolves_the_same_base_twice`,
  `test_us2_the_feature_tier_never_consults_the_scripts_builtin_default`,
  `test_us2_the_trunk_tier_is_reached_only_after_the_feature_tier`,
  `test_us2_no_tier_resolves_to_not_evaluated_with_the_failing_command`,
  `test_us2_a_trunk_shaped_branch_participates_only_when_explicitly_named`,
  `test_us2_trunk_order_ignores_the_remote_origin_happens_to_point_at`,
  `test_us2_trunk_order_ignores_the_most_recently_active_branch`,
  `test_us2_trunk_order_prefers_a_resolvable_origin_head_over_a_local_main`,
  `test_us2_an_explicit_trunk_beats_a_resolvable_origin_head`,
  `test_us2_head_is_the_explicit_value_when_given`,
  `test_us2_head_is_read_once_and_fixed_for_the_whole_run`,
  `test_us2_base_offers_a_machine_readable_form`,
  `test_us2_the_feature_tier_never_derives_from_the_latest_commit_over_the_spec`,
  `test_us2_the_non_interactive_path_is_four_steps_read_as_four`,
  `test_us2_base_start_and_note_complete_without_a_prompt_or_a_tty`,
  `test_us2_the_record_header_has_one_form_in_a_fixed_field_order`,
  `test_us2_start_reports_the_range_the_base_step_resolved`,
  `test_us2_a_first_run_creates_the_record_and_reports_no_archive`,
  `test_us2_a_rerun_rotates_the_previous_record_under_the_utc_second_form`,
  `test_us2_a_same_second_rerun_never_overwrites_an_archive`,
  `test_us2_a_triage_value_other_than_run_creates_no_record`,
  `test_us2_triage_runs_when_the_delta_contains_a_code_path`,
  `test_us2_triage_is_not_applicable_for_a_spec_only_delta`,
  `test_us2_triage_answers_an_empty_delta_before_any_receipt_runs`,
  `test_us2_the_default_code_path_set_treats_docs_and_memory_as_non_code`,
  `test_us2_the_code_paths_override_narrows_the_predicate`,
  `test_us2_the_code_paths_override_widens_the_predicate`,
  `test_us2_triage_reports_not_evaluated_when_the_range_cannot_resolve`,
  `test_c22_the_rendered_marker_needs_the_renderer_and_a_terminal`,
  `test_c23_the_four_forbidden_phrases_are_quoted_verbatim_as_a_prohibition`,
  `test_c24_the_renderer_absence_clause_is_rewritten_not_deleted`,
  `test_c25_the_receipt_is_the_only_evidence_form_for_reading_the_whole_diff`,
  `test_c26_the_verdict_keeps_the_script_as_its_only_source`,
  `test_c27_an_omitted_record_path_labels_its_selection_as_implicit`,
  `test_c29_both_skills_declare_distinct_judgment_objects_composed_by_the_command`
- Exit code: `1`
- Failing count: **38 of 39** (the one that passes is
  `test_us2_additional_subcommands_do_not_break_the_existing_closed_loop` — the
  group's regression half: it pins `diff`/`review`/`note`/`report` staying
  documented and `diff --stat` staying drivable, so it is green on both sides of
  the change by construction and is not evidence of coverage)
- Reading: the failures are the obligations the script does not carry yet — the
  `base`/`triage`/`start` subcommands do not exist (the script answers `未知命令`),
  so every behavioural case reds on a real invocation rather than on a missing
  file; the skill body still says "环境缺失即停" and "No overlap — keep the two
  separate", so the C-23/C-24/C-25/C-29 bands red on text that is measurably
  present today.
- Disclosed transient (T012 lands `start`, T015 lands `receipt`): the four-step
  enumeration is asserted from the usage block, so `receipt` is declared as step 4
  one part before its implementation arrives. The declaration is the plan's
  four-step path (FR-021, research § R7); the subcommand's non-interactive
  behaviour is pinned by group 4 (`test_coverage_receipt.py`, T014/T018), and its
  reachability is asserted there, not here.
- Red → green (T013 for C-17…C-21; T016/T017 for the US3 bands, T031 for C-29):
  **the US2 band is green on 2026-10-27** after T011 (`base` + `triage`) and T012
  (`start`) added the three subcommands to the existing script entity.
  - Command line: `python3 -m pytest -q tests/contract/test_code_review_skill_contract.py -k us2`
  - Real output: `32 passed, 7 deselected in 1.74s`
  - Exit code: `0`
  - Failing count: `0` (was 31 of the 32 in the red run's US2 half — the one US2 case
    that was green at red time, `test_us2_additional_subcommands_do_not_break_the_existing_closed_loop`,
    is the regression half and stayed green). Three edits were made to this file between
    the red run and the green run, and none of them relaxes an obligation: (1) the
    `git log -1` search now skips comment lines, so a comment may name the forbidden
    instrument while its use still reds; (2) the C-17 enumeration no longer demands a
    `COMMANDS` entry for `receipt` one part before that subcommand exists (its behaviour
    is group 4's obligation); (3) the two origin-HEAD tests were given a history in which
    tier 2 and tier 3 measurably disagree (`develop` branches off the seed while `main`
    moves on), so "origin/HEAD beats local main" is a discriminating assertion instead of
    an accidental equality. Both restructured cases were in the recorded red run's failing
    list and fail for the same reason there (the subcommand did not exist).
  - Whole-group state after this part:
    `python3 -m pytest -q tests/contract/test_code_review_skill_contract.py` →
    `7 failed, 32 passed in 1.98s`, exit `1`. The seven are exactly the sibling bands
    authored in this same file and claimed by later rows — `test_c22_*`, `test_c23_*`,
    `test_c24_*`, `test_c25_*` (T016), `test_c26_*`, `test_c27_*` (T017), `test_c29_*`
    (T031). They are red on the surfaces those rows own (the skill body still says
    "环境缺失即停" and "No overlap — keep the two separate"; `report --summary` has no
    `--file` and always exits 0), not on anything this part was asked to deliver.

### T013 — US2 verification (quickstart Scenario A, determinism, the three triage answers)

- Scenario A, live on this repository (no test substitute):
  `git log --diff-filter=A --format='%H %ad %s' --date=short -- .specify/specs/071-review-code-integration/requirements.md`
  → `8d18265b… 2026-10-27 docs(071-review-code-integration): land the review × code-review
  composition requirements`; then
  `bash skills/internal/code-review/scripts/git-delta-review.sh base --spec .specify/specs/071-review-code-integration`
  → `base=e57052efa1c16871da4e24a56eabf7402b6fd87e`, `head=a6625f32ead981a6064db166dc3e1ce175a21fb2`,
  `base_source=feature-first-commit`, exit `0` — which is exactly what `quickstart.md`
  Scenario A declares (`base_source=feature-first-commit`, base `e57052ef…`, head = the
  `HEAD` read once at run start). The base equals the parent of the requirements first-add
  commit, i.e. the feature freeze point, not a branch-tip.
- Same repository state, two resolutions: the same command run twice printed the identical
  `base` / `head` / `base_source` triple (FR-022). The assertion form of the same property
  is `test_us2_the_same_repository_state_resolves_the_same_base_twice`.
- The three triage answers, live in a disposable repository built by the T003 fixture:

  | delta shape | `changed_files` | `triage` | `basis` |
  |---|---|---|---|
  | code (`src/fixture_demo.py` + a spec artifact) | 2 | `run` | `code path in the committed delta: src/fixture_demo.py` |
  | spec-only (`plan.md` only) | 1 | `not-applicable` | `no code deliverable: the committed delta contains no code path` |
  | empty (`base` == `head`) | 0 | `not-applicable` | `no committed code delta` |

  No record file was created by any of the three invocations
  (`record created by triage? False`), which is the `V29` half of the same rule. The same
  three shapes are asserted by `test_us2_triage_runs_when_the_delta_contains_a_code_path`,
  `test_us2_triage_is_not_applicable_for_a_spec_only_delta` and
  `test_us2_triage_answers_an_empty_delta_before_any_receipt_runs`; the override directions
  and the unresolvable-range exit `2` are asserted by
  `test_us2_the_code_paths_override_narrows_the_predicate`,
  `test_us2_the_code_paths_override_widens_the_predicate` and
  `test_us2_triage_reports_not_evaluated_when_the_range_cannot_resolve`.
- Live on this repository the triage answers `run` over `103` changed files with three code
  paths named — the framework repo's own feature slice really does contain code, so the
  predicate is not vacuous here either.


## Group 4 — `tests/contract/test_coverage_receipt.py`

- Red run (T014): **2026-10-27** at implement part 4, HEAD `7a0a5a920750e99f034812a55318475e7176eecd`
  (clean tree), before any edit of `skills/internal/code-review/scripts/git-delta-review.sh`,
  `skills/internal/code-review/SKILL.md` or `skills/internal/code-review/references/delta-setup.md`.
- Command line: `python3 -m pytest -q tests/contract/test_coverage_receipt.py`
- Real output (tail): `19 failed, 1 passed in 1.68s`
- Failing tests (19, by name): `test_c31_the_receipt_is_one_delimited_block_inside_the_record`,
  `test_c32_the_block_name_set_is_closed`,
  `test_c33_the_rows_are_sorted_and_zero_padded_and_a_rerun_is_byte_identical`,
  `test_c42_the_grammar_needs_no_heuristic`,
  `test_the_exit_alphabet_is_closed_at_three_with_one_meaning_each`,
  `test_c35_exit_2_writes_no_block_and_names_its_reason`,
  `test_c36_a_legal_skip_is_disclosed_and_earns_no_coverage`,
  `test_c36_the_five_value_reason_set_is_read_from_its_owner`,
  `test_c36_an_unrecognised_skip_reason_is_a_gap_not_a_legal_skip`,
  `test_c37_c38_the_verdict_is_the_conjunction_of_the_three_signals`,
  `test_c38_the_blocking_signal_is_a_presence_test_not_a_resolved_state`,
  `test_c38_an_empty_delta_never_reaches_the_receipt`,
  `test_c40_the_block_renderer_equals_the_record_header_marker`,
  `test_c41_the_line_counts_are_measured_from_numstat`,
  `test_sc002_the_gap_drill_deletes_one_entry_and_the_rerun_goes_red`,
  `test_c74_the_four_counts_agree_three_ways`,
  `test_c43_a_non_zero_gap_or_skip_count_is_surfaced_outside_the_block`,
  `test_c44_a_dirty_tree_is_disclosed_on_both_carriers_without_a_conclusion`,
  `test_t018_an_illegal_skip_reason_exits_1_and_an_unresolvable_range_exits_2`
- Exit code: `1`
- Failing count: **19 of 20**. The one that passes is
  `test_t018_the_interactive_walk_and_the_six_level_validation_are_intact` — the group's
  regression half (C-28): it drives `review --yes` and the six-level `note` validation, both of
  which already exist, so it is green on both sides of the change by construction and is **not**
  evidence of coverage.
- Reading: every failing case reds on a real invocation of the missing subcommand, not on a missing
  file — the script answered `✗ 未知命令: receipt (使用 --help 查看用法)` at red time, so the
  carrier, the alphabet and the derivation were all unimplemented obligations rather than typos.
- Red → green (T018): **green on 2026-10-27** after T015 (`receipt`), T016 (the renderer-absence
  rewrite) and T017 (`report --file`).
  - Command line: `python3 -m pytest -q tests/contract/test_coverage_receipt.py`
  - Real output: `20 passed in 2.58s`
  - Exit code: `0`
  - Failing count: `0` (was 19). Two assertions were corrected between the red and the green run
    and neither relaxes an obligation: the zero-padding case now checks
    `ordinal_token == str(ordinal).zfill(width)` (its first form demanded a leading `0` from every
    token, which would have failed a correctly padded `10`), and the exit-alphabet case now passes
    an explicit `--since/--head` (its first form ran the default range, which resolves to an empty
    delta and would have measured the `2` branch while believing it measured the gap branch). Both
    were in the recorded failing list and fail there for the unimplemented-subcommand reason.

### T018 — US3 verification

- Targeted set, final state:

  | Suite | Command | Result |
  |---|---|---|
  | this group | `python3 -m pytest -q tests/contract/test_coverage_receipt.py` | `20 passed`, exit `0` |
  | the sibling group's US3 bands | `python3 -m pytest -q tests/contract/test_code_review_skill_contract.py -k "c22 or c23 or c24 or c25 or c26 or c27"` | `6 passed, 33 deselected`, exit `0` |
  | the sibling group whole-file | `python3 -m pytest -q tests/contract/test_code_review_skill_contract.py` | `38 passed, 1 failed`, exit `1` |
  | composed-command guard | `python3 -m pytest -q tests/contract/test_review_code_composition.py` | `31 passed`, equal to the part-2 measurement |
  | neighbouring pins | `python3 -m pytest -q tests/contract/test_review_p1_review_loop.py` | `10 passed`, equal to T001's count |

  The single red in the whole-file run is `test_c29_*` (T031's row, the sibling-boundary wording),
  exactly as part 3 declared. `test_expression_compatibility.py` carries one red that is **not**
  this part's (see the anomaly section at the end of this file).

- **Quickstart Scenario D, live** (disposable repository from the T003 fixture; the command lines are
  the ones below with `<spec>` = `.specify/specs/071-fixture-demo`):

  ```text
  DELTA_BIN=/tmp/review-git-repo-*/\.delta-missing bash .../git-delta-review.sh receipt \
    --review-file <spec>/code-review.md --renderer text --since <seed> --head <feature>
  → rc=0  renderer=text changed_files=2 judged_files=2 skipped_files=0 gap_files=0 verdict=pass
  → record header: | **渲染模式** | `renderer: text` |
  → forbidden four-phrase list present in the record: none
  ```

  **The no-TTY case (the one that actually happens)** — the host *does* have the renderer
  (`/home/agent/.cargo/bin/delta`) and the call is made through pipes:

  ```text
  bash .../git-delta-review.sh receipt --review-file <spec>/code-review.md --since <seed> --head <feature>
  → rc=0  renderer=text   (never `renderer: delta`)
  → record header: | **渲染模式** | `renderer: text` |
  ```

  A renderer present on `PATH` therefore does not by itself earn the rendered marker: the second
  condition (an interactive terminal) is what the mode keys on. Pinned by
  `test_c40_the_block_renderer_equals_the_record_header_marker`.

- **Quickstart Scenario E, live** (the gap drill, in order):

  | Step | Command | rc | changed / judged / skipped / gap | verdict |
  |---|---|---|---|---|
  | 3 — write the receipt | `receipt --review-file <record> --since <seed> --head <feature>` | `0` | 2 / 2 / 0 / 0 | `pass` |
  | 4 — delete one `file.02.*` entry group, re-run step 3 | same | `1` | 2 / 1 / 0 / 1 | `not-evaluated` |
  | restore the entry, re-run step 3 | same | `0` | 2 / 2 / 0 / 0 | `pass` |

  The rewritten block carries `gap_files` equal to the number of unjudged files, so the shortfall is
  mechanical rather than editorial — which is why the per-file verdicts are **carried forward** from
  the block already in the record instead of being re-derived on every run. Had a re-run re-derived
  the judged set, deleting an entry would have been silently repaired and `SC-002`'s drill could not
  go red at all.

- **Quickstart Scenario F, live**: `receipt --review-file <record> --skip-with-reason "src/*"
  --reason size-guard-focus-not-reviewed` → rc `0`, `skipped_files=1`, `judged_files=1`,
  `gap_files=0`, verdict `not-evaluated` (no `blocking` entry in the record), and the per-file row
  reads `file.02.path=src/fixture_demo.py`, `file.02.verdict=skipped`,
  `file.02.reason=size-guard-focus-not-reviewed`. A skip is legal (exit `0`) and still forbids
  `pass` (C-37).

- **The two cases the closed alphabets require** (both now in this group, driven live):
  a skip reason outside the five legal values → rc `1`, `gap_files=1`, `skipped_files=0`
  (`test_t018_an_illegal_skip_reason_exits_1_and_an_unresolvable_range_exits_2`), and an
  unresolvable range → rc `2` with the record left byte-identical and no block written
  (`test_c35_exit_2_writes_no_block_and_names_its_reason`).

- **The interactive per-file walk and its six-level validation**, driven end to end against the
  disposable repository rather than read off the script: `review --yes --since <seed> --head <feature>`
  → rc `0`, one report written under `REVIEW_DIR`, every changed file rendered and the statistics
  table present; then `note -s <level>` accepted for all six of
  `blocking / important / suggestion / nitpick / question / praise` and rejected for `critical`.
  Pinned by `test_t018_the_interactive_walk_and_the_six_level_validation_are_intact`.

- **A non-zero gap or skip count outside the block, on both carriers** (C-43): with
  `skipped_files=1` the command itself reports `skipped_files=1` as a field (the value the process
  report copies), and the report's `### 2.1` rendered from `templates/review-template.md` carries
  `2 / 1 / 1 / 0` in its own row — outside the block, copied field by field, equal to the block's
  fields (`test_c43_*`, `test_c74_the_four_counts_agree_three_ways`).

  **What C-74's three-way agreement is measured against**: the block comes from the real script, the
  report subsection comes from the real `templates/review-template.md` § 2.1, and the feature-detail
  entry is rendered by the same field-by-field copy act the command performs (that carrier is
  free prose — `[FEATURE_LATEST_REVIEW_SUMMARY]` — so no run-time instance of it exists in this
  fixture). One reconciliation function reads all three, and it is then run against a **tampered**
  copy which it must reject; a check that stayed green there would prove nothing, so the negative
  control is part of the case.

- **The dirty tree** (C-44): with two uncommitted paths, `changed_files` stays `2` (the committed
  delta — the uncommitted scope is never folded in), the record carries exactly one
  `> **未提交范围（未评审）**` line naming the excluded paths with no conclusion over them, the
  command reports `uncommitted_scope=2` for the report carrier, and a clean tree leaves no stale
  disclosure behind. Pinned by
  `test_c44_a_dirty_tree_is_disclosed_on_both_carriers_without_a_conclusion`.

- **Implementation decisions this part had to fix** (recorded because the plan names the obligations
  but not these mechanisms):
  1. *The judged set is the block's per-file entries* (carried forward), with the first write —
     a record that carries no block yet — treating its own invocation as the caller's assertion that
     the delta was read. This is what makes the gap drill able to go red (see Scenario E above) and
     what keeps two runs over one repository state byte-identical (C-33). A new commit after a
     receipt therefore goes through `start` again, which is exactly the four-step path's step 2.
  2. *`receipt` rewrites the record's renderer marker* to the mode it actually used, so the marker
     and the block cannot disagree (C-40) — measured by starting the record with `--renderer delta`
     and watching a piped `receipt` move both forms to `text` together.
  3. *`receipt` writes the uncommitted-scope disclosure* into the record and reports it as a field,
     because it is the step that resolves the range and is therefore the only place that knows what
     the committed delta excluded.

## Group 5 — `tests/contract/test_status_gate_owner.py`

- Red run (T019): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T023): pending

## Group 6 — `tests/contract/test_review_feedback_boundary.py`

- Red run (T024): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T028): pending

## Neighbouring-suite re-runs (regression nets, not red-first)

These exercise behaviour that already exists or fully lands before they run, so they carry `[blockedBy:]` instead of a red-first claim (the create-tasks migration/regression exception).

- T027 — `python3 -m pytest -q tests/contract/test_expression_gates_doc.py` against the plan-stage pre-change count of **18 passed** (re-measured at implement start in `notes/pre-change-measurements.md` § PM-6): pending
- T030 — the one intentional pin `tests/contract/test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition` under FR-027's single authorization: pending
- T033 / T036 — mirror verification and final closure comparison against the T001 measurements and the T002 baseline: pending

## Fast-fail findings on the red-first obligation (T029 collects these)

None recorded. Every group either has its red run recorded above or is still `pending` by its own
row's schedule; no group was counted as covered while red.

## Neighbouring pin reddened by the feature's own edits — handed up, not repaired (part 4)

**Measured** (fast-fail, decision-class): `tests/contract/test_expression_compatibility.py::test_c5_non_wiring_files_keep_their_frozen_hashes`
freezes the sha256 of 74 non-wiring sources, and two of them are files this feature must edit —
`templates/commands/review.md` and `skills/internal/code-review/SKILL.md`. Reading the manifest in
`.specify/specs/069a-flow-classification-docs-gates/notes/pre-change-file-hashes.txt` against
`git show HEAD:<path>`:

| File | Manifest hash | HEAD `7a0a5a92` blob | State |
|---|---|---|---|
| `templates/commands/review.md` | `30ed9f12…` | `ddb3c8f2…` | **drifted at HEAD, i.e. already red before part 4** (part 2's T006/T008 edit) |
| `skills/internal/code-review/SKILL.md` | `c0d0a6af…` | `c0d0a6af…` | not drifted at HEAD; part 4's T016 edit makes it the second drifted file |

Consequence: the assertion reports `drifted: ['skills/internal/code-review/SKILL.md',
'templates/commands/review.md']`, and it is **not** in `baseline-failed.txt`, so by SC-006's
name-level comparison it is a NEW failure — one this part widens rather than causes.

**Why this was not repaired in place.** The test ships its own declared mechanism
(`ALLOWED_POST_BASELINE_CHANGES`, "names every post-baseline drift with its reason"), so a repair is
mechanically available. It is still not a correction: `requirements.md` FR-027 authorizes **exactly
one** existing-assertion change (`test_review_p1_review_loop.py::test_c15`) and states in the same
breath that the authorization is a closed single-point exception which "MUST NOT be cited as a
basis by analogy". Allowlisting two frozen hashes is a governance-visible exception that no
artifact of this feature records, and the choice between *allowlist them*, *leave the pin red and
carry it into T035/T036's closure comparison*, and *treat the C-5 manifest as one of the mirrors
C-67 already schedules* is a choice between readings the artifacts do not decide. Per
`shared/guidelines/fast-fail.md` that is decision-class: the anomaly stops here and goes back to the
orchestrator with this measurement, rather than being flattened into the tree.

**Also measured, for the same closure comparison** (both pre-existing, both named in
`baseline-failed.txt`, therefore no NEW failure):
`tests/contract/test_scripts_distribution_parity.py::TestScriptsDistributionParity::test_repo_has_no_orphan_or_drifted_scripts`
reports the four per-tool `speckit.review` copies plus five mirror `DIFF` lines — the expected
"mirrors last" state that T032/T033 close.
