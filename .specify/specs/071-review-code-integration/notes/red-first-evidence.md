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

- Red run (T019): **2026-10-27** at implement part 5, HEAD `60f2b915` (clean tree), before any
  edit of `templates/feature-details-template.md`, `shared/workflow/feature-integration.md`,
  `templates/commands/review.md` or `templates/commands/checklist.md`.
- Command line: `python3 -m pytest -q tests/contract/test_status_gate_owner.py`
- Real output (tail): `24 failed, 8 passed in 0.37s`
- Failing tests (24, by name): `test_c45_the_owner_section_declares_itself_the_authority_for_the_transition`,
  `test_c45_no_second_criteria_wording_survives_on_another_surface`,
  `test_c46_the_owner_row_carries_the_three_conjunctive_conditions`,
  `test_c46_the_third_condition_is_an_existence_test_over_the_current_record`,
  `test_c46_no_clearing_action_and_no_cleared_state_are_defined`,
  `test_c46_the_six_level_vocabulary_is_read_directly_not_relabelled`,
  `test_c47_the_review_row_is_a_reference_to_the_owner`,
  `test_c47_the_duplicated_criteria_wording_is_removed_not_reworded`,
  `test_c48_the_checklist_row_is_a_conditional_initiator`,
  `test_c48_the_checklist_row_is_a_reference_to_the_same_owner`,
  `test_c48_no_initiating_row_carries_its_own_copy_of_the_conditions`,
  `test_c49_important_allows_the_transition_but_must_be_answered`,
  `test_c49_the_four_lower_levels_never_block`,
  `test_c50_no_conversion_matrix_or_unified_score_exists`,
  `test_c51_a_waiver_requires_an_explicit_user_ruling`,
  `test_c51_the_agent_never_downgrades_merges_or_excludes_a_blocking_entry`,
  `test_c51_the_unattended_disposition_is_halt_and_report_with_the_named_literal`,
  `test_c52_not_applicable_and_not_evaluated_are_disclosed_on_both_carriers`,
  `test_c52_the_closing_summary_carries_no_obligation_of_its_own`,
  `test_c53_a_refusal_names_the_failed_condition`,
  `test_c53_the_refused_transition_leaves_the_status_at_implemented`,
  `test_c54_the_transition_is_judged_once_after_both_segments`,
  `test_c54_both_artifacts_are_on_disk_before_the_judgement`,
  `test_c54_the_command_states_no_criterion_of_its_own`
- Exit code: `1`
- Failing count: **24 of 32**. The eight that pass are of three kinds, none of them evidence of
  coverage:
  1. the **driven gate cases** — `test_c46_one_blocking_entry_blocks_and_a_fresh_record_allows`,
     `test_c46_an_archived_record_never_keeps_blocking`,
     `test_c46_the_archive_does_not_dilute_a_blocking_current_record`,
     `test_c49_important_only_allows_the_driven_gate` — measure the `report --summary --file`
     mechanism T017 landed in part 4, so they are the group's **regression half**: they pin that
     the existence semantics the owner row must *describe* really hold in the executable gate, and
     they were green before and after by construction;
  2. the **negative sweeps** — `test_c48_the_checklist_command_keeps_its_pointer_and_gains_no_criteria`
     and `test_c51_the_refusal_literal_has_one_spelling` (no variant spelling of the literal exists
     yet) and `test_c50_no_artifact_of_this_feature_stores_a_mapping` (the command template's
     "never merged … mapping table or a conversion" sentence predates this part). A negative guard
     that holds on the pre-change tree is the correct state; it is the tripwire for the edit, not
     a claim about it;
  3. `test_c47_the_owner_the_row_names_really_holds_the_criteria` — the owner path and section
     already exist; this case pins that the rows about to cite them cite something real, and it is
     therefore green on both sides by design (its discriminating partner is
     `test_c47_the_review_row_is_a_reference_to_the_owner`, which is red).
- Reading: the failures are the four obligations no surface carries today — the owner row states
  two conditions and no record existence test, the integration protocol carries a **second**
  criteria wording (`review.md committed AND every deferred item resolved or waived`) and names no
  owner, the command template has no transition section at all, and no surface names a waiver rule,
  the `blocking-unresolved` literal, or a single checkpoint. `templates/commands/checklist.md`
  line 36 already reads as a pointer, which is why its case is green and must stay green.
- Red → green (T023): **green on 2026-10-27** after T020 (`templates/feature-details-template.md`
  row + the gate block), T021 (the two initiating rows in
  `shared/workflow/feature-integration.md`) and T022 (`templates/commands/review.md`
  `## Status Transition`).
  - Command line: `python3 -m pytest -q tests/contract/test_status_gate_owner.py`
  - Real output: `32 passed in 0.21s`
  - Exit code: `0`
  - Failing count: `0` (was 24). No assertion was relaxed, renamed away or deleted between the
    two runs; the only test-side change was correcting one assertion of my own that asserted the
    wrong subject (`test_c45_…_declares_itself_the_authority…` first demanded that the owner file
    name its own repo path — the owner is the file, so what it must say is the *shape* of the
    reference the other surfaces take, `by reference` + `no second wording`). That assertion was
    in the recorded failing list and fails there for the same reason as its replacement.
  - The eight cases that were green at red time stayed green, so the group's regression half (the
    driven gate) and its negative sweeps did not move while its wording half flipped.

### T023 — US4 verification

- Targeted set, final state:

  | Suite | Command | Result |
  |---|---|---|
  | this group | `python3 -m pytest -q tests/contract/test_status_gate_owner.py` | `32 passed`, exit `0` |
  | neighbouring pins over the edited surfaces | `python3 -m pytest -q tests/contract/test_review_p1_review_loop.py tests/contract/test_review_code_composition.py tests/contract/test_coverage_receipt.py` | `1 failed, 60 passed`, exit `1` |
  | the C-5 hash freeze, after the in-passing correction below | `python3 -m pytest -q tests/contract/test_expression_compatibility.py -k c5` | `3 passed`, exit `0` |

  The single red in the neighbouring set is
  `test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition`, and it is
  **T030's row, by design**: T030 is `[blockedBy: T021]` and rewrites that pin (it keeps the subject
  "the row exists and the command owns the transition", stops requiring the duplicated criteria
  wording T021 removed, and gains the owner citation plus a negative assertion that the duplicated
  wording is gone). It is an intermediate state of this part, not a regression: the pin reds on
  exactly the sentence T021 was told to remove. `test_c15_checklist_row_is_annotated_and_keeps_one_transition_per_command`
  — the pin T021 had to preserve — stayed green.

- **Quickstart Scenario G, live** (the two runs, on the disposable repository from the T003
  fixture; the command line is Scenario G's own, with `<record>` = the record the run points at):

  ```text
  bash skills/internal/code-review/scripts/git-delta-review.sh report --summary \
    --file <record>            → rc=1
    [blocking] 1 … blocking_entries=1 … gate=deny
    "✗ 合入门禁: 存在 1 条 [blocking] — 必须解决后方可合入"

  # the rerun writes a fresh record; the blocking entry survives only in the archive
  same command, same path      → rc=0
    [blocking] 0, [suggestion] 1 … blocking_entries=0 … gate=allow
  archive present during run 2: True (code-review-20260101T000000Z.md)
  current record has no `blocking` heading: True
  ```

  Reading: the refusal names the **count** (SC-004's first half), the allow run is the same
  command over a rewritten record (SC-004's second half), and nothing was "cleared" between them —
  the blocking heading was never edited, it simply is not in the record the run points at. That is
  also the "reads only the record the run itself points at" measurement: the archive holding the
  blocking entry was **present** during the allowing run and did not keep it blocked.

- **The four driven cases in the group** (SC-004 and its two neighbours, asserted rather than read
  off prose): `test_c46_one_blocking_entry_blocks_and_a_fresh_record_allows` (deny with the count →
  allow after the rerun), `test_c46_an_archived_record_never_keeps_blocking` (archive holding
  `blocking`, current clean → allow), `test_c46_the_archive_does_not_dilute_a_blocking_current_record`
  (mirror direction: a clean archive cannot offset a blocking current record), and
  `test_c49_important_only_allows_the_driven_gate` (`important`-only → allow, US4 scenario 2).

- **The transition is judged once, after both artifacts exist.** This is a rule about the command's
  execution order and the command is a prompt, so it is pinned as the text that orders it
  (`test_c54_the_transition_is_judged_once_after_both_segments`,
  `test_c54_both_artifacts_are_on_disk_before_the_judgement`) and it now appears on both surfaces
  that must agree: the owner block's item 9 and the command template's `## Status Transition`
  ("judged once, after the process segment and the code segment have both finished and both
  artifacts — `review.md`, and `code-review.md` when the triage value is `run` — are on disk; the
  status MUST NOT flip before that segment completes"). There is no second judgement site anywhere
  in the feature: the merge gate the command calls is a per-record presence test, which is why the
  ordering rule lives in the prompt and the count lives in the script.

- **One measured premise of `tasks.md` refined, not contradicted** (`tasks.md` § Transition
  surfaces, taken from `grep -rn 'Implemented → Ready for Review' templates shared`): that grep is
  scoped to `templates/` + `shared/`, so its three hits are complete for those two layers. Grepping
  the whole framework tree adds one more mention — `skills/internal/create-checklist/SKILL.md`
  `## Feature Integration` — and it is a **pointer**, not a criteria copy: it says "Apply the
  Feature Integration Protocol (`.specify/shared/workflow/feature-integration.md`). This capability
  transitions feature status `Implemented → Ready for Review` when applicable." It carries none of
  the condition phrases, so C-45/C-48 hold across it, and the conditional-initiator semantics it
  defers to are now written on the row it points at. No edit was made there: it is not in this
  row's scope and it violates nothing. (`templates/review-template.md` § 2.1 and
  `skills/internal/summarize-project/references/consistency-rules.md` mention the transition as a
  verdict field and a status-list respectively — neither states criteria.)

## Group 6 — `tests/contract/test_review_feedback_boundary.py`

- Red run (T024): **2026-10-27** at implement part 6, HEAD `f7f8156e` (clean tree), before any
  edit of `templates/commands/review.md` or `skills/internal/code-review/SKILL.md` in this part.
- Command line: `python3 -m pytest -q tests/contract/test_review_feedback_boundary.py`
- Real output (tail): `19 failed, 11 passed in 0.67s`
- Exit code: `1`
- Failing count: **19 of 30**
- Failing tests (19, by name): `test_c55_the_command_states_the_set_is_unchanged_and_adds_no_channel`,
  `test_c56_the_command_limits_the_payload_to_framework_friction`,
  `test_c56_a_code_defect_stays_in_the_record`,
  `test_c57_the_duty_is_written_on_two_surfaces`,
  `test_c57_the_framework_friction_sample_is_judged_legal`,
  `test_c57_the_code_defect_sample_is_judged_a_violation`,
  `test_c57_the_two_samples_are_judged_oppositely`,
  `test_c57_the_store_itself_cannot_enforce_the_duty`,
  `test_c58_the_command_names_the_three_units`,
  `test_c58_the_command_forbids_suppression_backfill_and_substitution`,
  `test_c58_the_code_skill_completes_its_own_closing_record`,
  `test_c59_the_census_is_three_not_two`,
  `test_c62_the_code_segment_is_an_additional_segment`,
  `test_c62_a_no_delta_feature_records_not_applicable_without_short_circuiting`,
  `test_c63_the_receipt_counts_reviewed_files`,
  `test_c63_the_receipt_is_never_test_or_compile_coverage`,
  `test_c63_the_receipt_is_not_evidence_for_the_reader_baseline_judgement`,
  `test_c63_fr027_targets_the_other_object_and_never_forbids_the_receipt`,
  `test_c63_the_two_directions_are_stated_together`.

- **What the 11 green tests are, at red time** — the unchanged-surface half, not coverage of the new
  behaviour: the two compiled closing faces' step tuples (`test_c55_the_command_closing_step_set_is_the_published_six`,
  `test_c55_both_delegated_skill_faces_keep_their_five_step_set`), the "rule text sits outside the
  compiled face" guard, the per-face unit-id ownership
  (`test_c58_each_unit_owns_exactly_one_compiled_closing_face`), the three directly driven
  (unit_id, run_id) cases, and the three C-60/C-61 predecessor sweeps. They are supposed to be green
  before the edit — they measure what must NOT move — and the flip therefore has to come from the two
  surfaces, which is what the red list is made of.

- **The two constructed samples and how they are judged (SC-007).** Both live in the test. The judge
  is *parameterised by the written rule*: `_duty()` parses the legal class (framework friction) and
  the forbidden class (a code defect posted as a feedback entry) out of both surfaces and fails when
  either class is missing, so the sample verdicts cannot survive the deletion of the surface that
  states the rule. A sample carrying a code location plus one of the six code severities is a code
  defect; a sample naming framework mechanisms is friction. Legal side is also driven against the real
  store (one entry, `unit_id` as called, `scope: local`); the violation side is judged from the written
  rule, because the engine deliberately cannot classify — which is the reason C-57 requires the rule in
  words.

- Red → green (T028): **2026-10-27** at implement part 6, HEAD `f7f8156e` plus this part's edit.
  `python3 -m pytest -q tests/contract/test_review_feedback_boundary.py` →
  `30 passed in 0.59s`, exit `0` (red: `19 failed, 11 passed`, exit `1`). The flip came from the two
  surfaces — `templates/commands/review.md` (T025) and `skills/internal/code-review/SKILL.md`
  (T026/T027) — not from an assertion change: no test name was added, dropped or weakened between
  the red run and the green run, and the 11 tests green at red time are still green.

### T028 — US5 verification

- Targeted set, final state:

  | Suite | Command | Result |
  |---|---|---|
  | this group | `python3 -m pytest -q tests/contract/test_review_feedback_boundary.py` | `30 passed`, exit `0` |
  | neighbouring groups over the edited surfaces | `python3 -m pytest -q tests/contract/test_review_code_composition.py tests/contract/test_status_gate_owner.py tests/contract/test_coverage_receipt.py tests/contract/test_code_review_skill_contract.py` | `1 failed, 121 passed`, exit `1` |
  | the expression face's own gate (T027's control) | `python3 -m pytest -q tests/contract/test_expression_gates_doc.py` | `18 passed`, exit `0` — **equal to the plan-stage pre-change count** |
  | the pin under FR-027's single authorization | `python3 -m pytest -q tests/contract/test_review_p1_review_loop.py` | `1 failed, 9 passed` — the red is `test_c15_review_owns_the_ready_for_review_transition`, T030's scheduled rewrite |
  | the docs↔template isomorphism page | `python3 -m pytest -q tests/contract/test_review_docs_isomorphism.py` | `5 failed, 4 passed` — unchanged from part 5, red by design until T031 |
  | the compiled-face guards | `python3 -m pytest -q tests/contract/test_compile_embeds.py tests/contract/test_compile_propagation_order.py` | `1 failed, 5 passed` — the red is `test_propagation_chain_is_green_in_canonical_order`, named in `baseline-failed.txt` |
  | the C-5 hash freeze | `python3 -m pytest -q tests/contract/test_expression_compatibility.py -k c5` | `3 passed`, exit `0` — equal to part 5 |

- **Quickstart Scenario H's two samples, judged as stated** (the samples and the judgement live in the
  test, per SC-007's source line): a framework-friction item ("the receipt step has no non-interactive
  path on a host without the renderer, and the workflow leaves the base ambiguous…") → **legal**, and
  it is additionally *driven* through `feedback-utils.py --action record`, producing one entry whose
  `unit_id` is as called and whose `scope` is `local`. A code defect copied out of the record
  ("`src/specify_cli/__init__.py:412 — blocking: …`") → **violation** of the written classification
  duty. The verdicts are opposite by construction, so a judge that answered one way for both would
  fail. Nothing is transmitted automatically, and the closing step list is unchanged.

- **The closing step set, enumerated from the compiled faces and compared with the pre-change file**
  (`git show f7f8156e:<path>` parsed the same way):

  | Face | Pre-change steps | Now | Equal |
  |---|---|---|---|
  | `templates/commands/review.md` | Run Determination, Exec Quant, Feedback Record, Threshold Notice, Token Reflection, Docs Sync Eval | identical, n=6 | yes |
  | `skills/internal/review-sdd-process/SKILL.md` | the first five of the same list | identical, n=5 | yes |
  | `skills/internal/code-review/SKILL.md` | the first five of the same list | identical, n=5 | yes |

  The compiled marker fingerprint is `7877db82c58c` in all three files, before and after: the
  generated faces were not edited, and the new rule text sits in hand-written sections outside them.

- **The run's units, enumerated**: each face names exactly one unit id —
  `/speckit.review` in the command template, `skill:review-sdd-process` in the process skill,
  `skill:code-review` in the code skill — and no face names another's. The census is therefore
  **three**, and it is measured behaviourally as well: three `run-determination.py` invocations
  sharing one run id leave three session records (one `source` per unit), and three
  `feedback-utils.py --action record` invocations sharing one run id leave **three** entries keyed
  `(unit_id, run_id)`; a repeated call for one unit leaves three, not four.

- **In-passing correction (disclosed) — the C-62 owner citation.** The first green attempt at
  `test_c62_the_code_segment_is_an_additional_segment` required the code-review skill to cite
  `shared/definitions/flow-class-definitions.md` by path. That turned
  `tests/contract/test_expression_compatibility.py::test_c5_wiring_surface_is_closed` red:
  `skills/internal/code-review/SKILL.md -> flow-class-definitions.md`, a **wiring reference outside
  the closed W1–W4 surface** that 067 froze. The resolution has exactly one reading — the
  expression-class owner declares the review face in its own ledger, so the skill states the boundary
  by description and the record walks the other way — and it is local and reversible: the assertion
  now pins the opposite property (the skill MUST NOT acquire a wiring token) and the skill says the
  face is declared by its owner without naming the file. `-k c5` is back to `3 passed`, equal to the
  part-5 measurement. No plan-owned artifact was touched, and no other assertion moved.

## Neighbouring-suite re-runs (regression nets, not red-first)

These exercise behaviour that already exists or fully lands before they run, so they carry `[blockedBy:]` instead of a red-first claim (the create-tasks migration/regression exception).

- T027 — `python3 -m pytest -q tests/contract/test_expression_gates_doc.py` against the plan-stage pre-change count of **18 passed** (re-measured at implement start in `notes/pre-change-measurements.md` § PM-6): **done at part 6 (T027)** — `18 passed`, exit `0`, equal to the frozen count. The expression-class review face is untouched by this feature: the process segment still judges against the declared reader baseline and still may not reuse the code-review object, which is why the code segment could be added as an *additional* segment without editing that face.
- T030 — the one intentional pin `tests/contract/test_review_p1_review_loop.py::test_c15_review_owns_the_ready_for_review_transition` under FR-027's single authorization: pending
- T033 / T036 — mirror verification and final closure comparison against the T001 measurements and the T002 baseline: pending

## Fast-fail findings on the red-first obligation (T029 collects these)

None recorded. Every group either has its red run recorded above or is still `pending` by its own
row's schedule; no group was counted as covered while red.

The one fast-fail item this file has carried — the C-5 hash freeze that part 4 handed up as
decision-class — was resolved at part 5 as a **correction** under the orchestrator's ruling; the
change, its two negative controls, and why it preserves the guard are recorded in § In-passing
correction (driver-ruled) at the end of this file. Nothing else was repaired in passing.

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

### In-passing correction (driver-ruled) — the C-5 post-baseline allowlist (part 5, T019–T023 batch)

The measurement above stands as recorded; the disposition changed at part 5 on the orchestrator's
explicit ruling, which converts it from decision-class to **correction**: the test ships its own
declared maintenance mechanism, so resolving it has exactly one reading.

- **What was changed** (`tests/contract/test_expression_compatibility.py`):
  1. `ALLOWED_POST_BASELINE_CHANGES` entries became `{reason, markers}` records instead of bare
     reason strings. The pre-existing entry
     `skills/external/sdd-loop-driver/SKILL.md` keeps its reason verbatim and gains its own markers
     `("监听签名唯一", "--iter")` — the content it was allowlisted for in 2026-10-25.
  2. Two entries added, each named as this feature's own declared drift:
     `templates/commands/review.md` with markers `("## Composition", "## Applicability triage")`
     (FR-001/FR-003/FR-008's composed surface), and `skills/internal/code-review/SKILL.md` with
     markers `("renderer: text", "receipt --review-file")` (FR-013's rewritten renderer-absence
     clause and FR-023's explicit-record path). Both reasons name Feature 071 as the source and the
     groups that pin them.
  3. The re-assertion loop stopped asserting the one hard-coded pair of literals against every
     entry; it now iterates each entry's own `markers`, so one file's content can no longer vouch
     for another's. One assertion was **added** rather than relaxed: an allowlisted path must also
     be a manifest entry, otherwise the allowance is vacuous (the freeze never covered it).
- **Why this preserves the guard instead of weakening it** — measured with two negative controls,
  run against the real test function in-process:

  | Control | Manipulation | Result |
  |---|---|---|
  | baseline | the extended allowlist as committed | green |
  | 1 — content still asserted | replace `templates/commands/review.md`'s markers with one that does not exist | **red**: "allowed post-baseline change must carry its own intended content … is missing marker '## Marker That Does Not Exist'" |
  | 2 — drift still detected | delete the `templates/commands/review.md` entry (its file HAS drifted) | **red**: "non-wiring source changed (C-5 …). drifted: ['templates/commands/review.md', …]" |

  So the three original properties survive: an unnamed drift still reds, a named drift whose
  intended content is gone still reds, and the historical pre-change hash is untouched (the frozen
  manifest was not re-frozen and `coverage-baseline.txt` was not touched).
- **What this correction is not.** It is not FR-027's pin change: FR-027's single authorized
  assertion change remains `test_review_p1_review_loop.py::test_c15` (T030), and nothing here
  rewrites an existing assertion's subject. It also is not a second-author allowlist habit: the two
  new entries name files a *declared surface* of this feature must edit, and the entry form now
  forces each future drift to state its own markers.
- **Evidence**: `python3 -m pytest -q tests/contract/test_expression_compatibility.py -k c5` →
  `3 passed, 13 deselected`, exit `0` (before the correction: `1 failed, 2 passed`, with
  `drifted: ['skills/internal/code-review/SKILL.md', 'templates/commands/review.md']`).
