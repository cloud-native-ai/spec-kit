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

- Red run (T010): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T013 for C-17…C-21; T016/T017 for the US3 bands): pending

## Group 4 — `tests/contract/test_coverage_receipt.py`

- Red run (T014): pending
- Command line: pending
- Real output: pending
- Exit code: pending
- Failing count: pending
- Red → green (T018): pending

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

None recorded yet. A group whose red run is missing, or that could not be made to go red, is recorded **here** rather than cited as coverage.
