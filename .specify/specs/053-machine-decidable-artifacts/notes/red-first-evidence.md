# Red-first evidence — Feature 053

**Purpose**: every test that MUST go red before its subject exists gets its command, real output and exit status recorded here (Tests Mode = ON, Constitution Principle IV). Red-first output is pasted, never predicted.

**Capture date**: 2026-10-03 · **BASE SHA**: see `pre-change-measurements.md`

<!-- entries are appended per task; each carries the task id, the command, the verbatim failing output and the exit code -->

## T004 — tests/contract/test_clause_forms.py (2026-10-03)

```
$ bash .specify/scripts/bash/run-tests.sh -q tests/contract/test_clause_forms.py
^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'clause_extract'
=========================== short test summary info ============================
ERROR tests/contract/test_clause_forms.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.09s
EXIT=2
```

Red for the right reason: the subject module does not exist yet. 24 test functions collected-by-intent (the suite errors at import, so collection is interrupted — that is the expected red form for a missing module, not a syntax defect in the test file).

## T007 — tests/contract/test_checker_form.py (2026-10-03)

```
$ bash .specify/scripts/bash/run-tests.sh -q tests/contract/test_checker_form.py
17 failed, 17 passed, 11 skipped
```

Red for the right reason: `scripts/python/validate-requirements.py` does not exist, and this suite makes an absent in-phase subject a **failure**, not a skip (a skip would have let the suite look green with its subject missing). The 11 skips are the `account-clause-coverage.py` parametrizations, whose owner is T024/T025 in US3 — each skip names that.

Three assertion defects in this suite were found by running it and attributed to the **assertion** side, not the subject:
- C-12's proxy looked for the skeleton criterion in the two contracts; neither states it (and adding a clause would move a pinned count), so the truth source is the checker's own docstring — test rewritten to assert that.
- C-26's grep for `goal_utils.EXIT` matched **this suite's own source** (the needle was written as an instance); the test now excludes itself — the same trap recorded earlier in this feature's history.
- C-28's regex assumed `help=` sits on the `add_parser(` line; it does not, so the extraction returned nothing and would have passed vacuously. Rewritten with `ast`, plus a floor on the number of extracted helps so an empty extraction fails instead of passing.

## T009 / T010 — validate-requirements.py on reality (2026-10-03)

**FR-043 real-artifact run** (this spec's own requirements.md):

```
$ python3 scripts/python/validate-requirements.py .specify/specs/053-machine-decidable-artifacts/requirements.md
file: .specify/specs/053-machine-decidable-artifacts/requirements.md
status: ok
  [id-contiguous] pass (0)
  [doc-order] pass (0)
  [ref-resolvable] pass (0)
  [marker-count] pass (0)
  [dup-id] pass (0)
scanned: 317 lines, 60 definition rows, 10 shared strings
0 error(s), 0 warning(s)
EXIT=0
```

**SC-001 — the four broken copies, built by quickstart 场景 3's block run VERBATIM** (extracted from the file and executed, not retyped). Each names exactly its own class; zero cross-masking:

| copy | construction | labels reported | exit |
|---|---|---|---|
| b1 | `grep -v '^- \*\*FR-030\*\*'` | `id-contiguous` only — "the FR sequence skips FR-030" | 1 |
| b2 | the `REORDER_EOF` heredoc moving SC-002 after SC-005 | `doc-order` only — `ORDER BREAK: SC-002 after SC-005` (the STR-002 literal) | 1 |
| b3 | `sed 's/\[\[STR-005\]\]/[[STR-999]]/'` | `ref-resolvable` only — 4 errors + 1 warning, all that label | 1 |
| b4 | `sed` inserting `[NEEDS CLARIFICATION: probe]` | `marker-count` only | 1 |

Residue after the battery: `\rm -rf $tmp` then `ls -d $tmp | wc -l` → **0**.

**Whole-corpus run (44 specs)** — recorded because it is the honest denominator, not a cherry-picked three:

```
exit 0: 26 specs   ·   exit non-zero: 18 specs
non-zero by label set: {('ref-resolvable',): 14, ('doc-order','ref-resolvable'): 1, ('id-contiguous',): 3}
```

Spot-checked, all **true positives**: `016`/`020` have `Consumed by` cells naming FRs whose rows re-type the literal instead of citing `[[STR-nnn]]` (exactly the drift C-15 exists to catch); `040-agent-metadata-portability:176` really does define `FR-023a`, a letter suffix this spec's own edge cases judge a format violation. So the 18 are pre-existing debt in specs written before the citation convention, not checker noise. GATE-10's "three real specs exit 0" is satisfied from the 26 (first three: `001-unify-command-handoffs`, `003-speckit-agents-command`, `006-add-qoder-support`).

**Consequence worth recording**: FR-012/C-18 make `/speckit.requirements` STOP on any ERROR, so re-running that command against one of the 18 debt-carrying specs will now halt where it previously did not. That is the intended behavior for a newly written spec; the debt itself is out of this feature's scope (FR-027's philosophy — do not require retrofitting existing specs) and is recorded here rather than fixed in passing.

**Two subject defects found by running, and one premise falsified:**
- padding was measured on the parsed integer, so every `FR-001` was reported as unpadded — the digits must be kept as written;
- the Shared Strings table was matched on the code-span-stripped view, where the backticked `` `STR-001` `` cell is erased → 0 strings found and 24 false dangling-reference errors. Structure is matched on the fence-blanked original; only *mention* scanning uses the stripped view;
- the quickstart's b1 originally deleted `FR-023`, which two other rows cite in prose — that would have fired `ref-resolvable` too and broken SC-001's zero-cross-masking. The scenario's premise block had only ever verified "a gap appears", never "only one class reports". Switched to `FR-030` (measured: 20 FR ids have zero non-definition mentions).

## T016 — US1 story checkpoint (2026-10-03)

Independent Test, all three legs run:

1. **Checker on three real specs → exit 0 each**: `001-unify-command-handoffs`, `003-speckit-agents-command`, `006-add-qoder-support` (chosen from the 26 of 44 that pass; the distribution is recorded in the T010 entry above rather than hidden).
2. **Four broken copies → exit 1 each, naming exactly its own class**: see the T010 table (4/4, zero cross-masking, residue 0 after `\rm -rf $tmp`).
3. **Transitional copies retired**: `grep -c '```awk' shared/constants/clarify-taxonomy.md` → **0**; `Until that validator ships` → **0**; `validate-requirements.py` mentioned **2×** in that file (the invariant now points at the checker).

Suite state: `test_clause_forms.py` + `test_checker_form.py` + `test_requirements_checker.py` + `test_clarify_semantic_completeness.py` → **76 passed, 11 skipped, 0 failed** (the 11 skips are `account-clause-coverage.py` parametrizations owned by T024/T025, each naming its owner).

Mirrors: `scripts/python` EXIT=2 with only the recorded pre-existing `trigger-utils.py` (no NEW drift); `shared/guidelines` and `shared/constants` EXIT=0; all three mirrors byte-identical (`cmp`). Per-tool copies regenerated, `regen-command-copies.py --check` EXIT=0, and all 4 `speckit.requirements` copies carry the new invocation line.

Hygiene: `scan-confirmation-gates.py --summary` → **23 / 13 / 10 / 0**. A BLOCKING_RE pass over all 14 files this story touched found **1** hit — `tests/contract/test_clarify_semantic_completeness.py:68`'s `PREEXISTING_GATE_FRAGMENT` constant, which `git diff` confirms this phase did not add, and `tests/` is not in `SCAN_DIRS` (`templates/commands`, `skills`, `shared`), so the budget is unaffected. `templates/commands/requirements.md` repo-name hits: **0**.

**Process deviation, disclosed (Phase 3)**: `gate-check.py` was run BEFORE the edits for Phases 1 and 2, but for Phase 3 it was run only after the edits landed. The retroactive verdict is `allow` for all six paths, EXIT=0 — no DENY or CONFIRM row, so nothing was written that the gate would have blocked; the ordering is still wrong and MUST be carried into `verification.md` `notes=` at T049. Phases 4-8 run the gate before their first edit.

## T017 — `tests/contract/test_green_point_claim.py` red first (2026-10-04)

Command: `python3 -m pytest tests/contract/test_green_point_claim.py -q`
Real tail of the output, before T018/T019 landed:

```text
23 failed, 6 passed in 0.24s
E   AssertionError: counter-sample 'green-dangling' did not fire its own label: []
FAILED …::test_c1_template_defines_the_str001_declaration_surface
FAILED …::test_c5_declaration_lands_in_the_format_section_beside_blockedby
FAILED …::test_c6_json_emits_one_four_field_object_per_claim
FAILED …::test_c7_clause_id_tolerates_dots_and_hyphens_first_hash_wins
FAILED …::test_c8_claim_inside_a_fence_is_not_a_claim
FAILED …::test_c9_missing_contract_file_is_an_error_not_a_warning
FAILED …::test_c9b_contract_path_resolves_from_the_repo_root_too
FAILED …::test_c10_missing_clause_id_is_an_error_naming_file_and_id
FAILED …::test_c11_clause_existence_is_resolved_through_the_owner_extractor
FAILED …::test_c12_inverted_order_yields_a_cross_phase_warning_naming_rows_and_phases
FAILED …::test_c13_cross_phase_compares_monotonic_order_not_a_numeric_phase_index
FAILED …::test_c14_warning_only_file_still_exits_zero
FAILED …::test_c15_two_rows_claiming_one_clause_collide_and_both_are_named
FAILED …::test_c16_path_divergence_is_about_differing_green_points_not_a_shared_path
FAILED …::test_c17_the_two_collision_labels_are_separately_counted
FAILED …::test_c18_implementation_cites_the_registered_glossary_term
FAILED …::test_c19_the_prose_self_check_points_at_the_check_and_keeps_one_criterion
FAILED …::test_c21_claim_path_is_not_a_write_target_but_real_conflicts_still_warn
FAILED …::test_c22_fix_extracts_before_classifying_and_leaves_the_governor_list_closed
FAILED …::test_c23_the_false_positive_mechanism_is_recorded_at_the_implementation_site
FAILED …::test_c25_label_roster_grew_by_exactly_the_four_new_labels
FAILED …::test_c26_new_exit_tiers_follow_the_existing_two_tier_table
FAILED …::test_c27_each_new_label_has_its_own_counter_sample_hitting_only_itself
```

**The 6 that were already green, and why each is not a vacuous pass** — a green-before
row is only meaningful if it can go red, so each is stated with what would break it:

| test | green today because | goes red when |
|---|---|---|
| `test_c2_zero_claims_leaves_a_file_exactly_as_clean_as_today` | the surface does not exist yet, so nothing to trip | T019 makes a claim-free file warn (the surface stops being a pure increment) |
| `test_c3_claim_folded_onto_a_continuation_line_is_a_row_format_error` | the existing wrapped-row check already fires | T019's claim extraction swallows the continuation line before the row check sees it |
| `test_c4_template_surface_is_project_neutral` | measured baseline: `grep -cE 'spec-kit\|specify-cli\|specify_cli\|cloud-native-ai' templates/tasks-template.md` → **0** before T018 | T018's new wording names this repo |
| `test_c12_consistent_order_yields_zero_cross_phase_warnings` | the check does not exist | T019's inversion rule fires on the correct, in-order shape (a false positive) |
| `test_c20_claim_only_row_does_not_trip_row_format` | `row-format` never demanded a path | T019 couples claim parsing to the row-format check |
| `test_c24_scenario_4_runs_the_positive_control_before_judging_the_negative` | quickstart.md 场景 4 was authored POS-before-NEG in the plan phase | the scenario is reordered, or the "先跑 POS" duty sentence is dropped |

C-12 and C-16 are two-directional criteria; only their **negative** halves are
green-before, and their positive halves (`…inverted_order_yields…`,
`…differing_green_points…`) are both red — so the pair as a whole is red-first.

**One semantic under-determination found while authoring, resolved to the criterion
(FR-017 → C-12).** FR-017's prose is "某条款的归属任务集中存在所处阶段晚于声明行的任务时".
Read literally with a per-clause attribution set, C-12's inverted copy (`C-2` claimed in
Phase 1, `C-1` in Phase 2) yields **0** WARN, because each clause then has a single
claiming row — the criterion's second half is unreachable. Read with a per-contract set,
C-12's *consistent* copy warns too, so the first half is unreachable. Exactly one reading
satisfies both halves: within one contract the claims' **clause ordinals must be
non-decreasing in the rows' monotonic `order`**; a strict decrease is the WARN. That is
also the reading under which the four labels' counter-samples stay separable (a
same-clause double claim is an ordinal *tie*, so it fires `green-clause-collision` alone
and not `green-cross-phase` as well), which C-27's per-label battery requires. Recorded
here and annotated onto C-12 in the same phase; D-8's "compare `order`, never a numeric
phase index" holds unchanged under it.

## T019/T020/T022 — US2 landed: the four green-* checks, real output (2026-10-04)

Suite state after T019+T020 in one edit pass:
`test_green_point_claim.py` + `test_validate_tasks_parallel_safety.py` + `test_checker_form.py`
→ **81 passed, 11 skipped, 0 failed** (the 11 skips are the accountant parametrizations
owned by T024/T025, each naming its owner).

### A subject defect found by running, not by reading (FR-020 → C-8 write-back)

`test_checker_form.py::test_c09_precedent_four_keys_are_not_migrated` runs the validator
over **053's own tasks.md** and went red with a claim nobody wrote:

```text
"green_claims": [ { "contract_file": "<contract>", "clause_id": "<clause>",
                    "task_id": "T018",
                    "phase": "## Phase 4: User Story 2 - 绿点归属声明面 (Priority: P1)" } ]
assert 1 == 0   (returncode)
```

T018's row has to **name** the tag in order to define it — ``with the STR-001 literal tag
`[green: <contract>#<clause>]` `` — and the first implementation parsed that mention as a
real declaration against a contract file literally named `<contract>`. So the feature's own
tasks.md failed its own GATE-7 on the row that introduces the surface.

**Attribution: subject defect, and a contract gap.** FR-009 already draws this exact
distinction for references (a backtick-wrapped form is a mention) and C-28 of
`requirements-checker.md` already owns the CommonMark N-backtick-run rule for it; FR-020
only ever named fenced blocks, so the requirement was narrower than the house rule it is an
instance of. Fixed in the subject by feeding the declaration view through the existing
`clause_extract.strip_code_spans` rather than by rewriting T018's row to dodge the literal —
dodging would leave every future document unable to name its own markup. Written back
upstream: FR-020 extended, C-8 of `green-point-claim.md` made two-directional, both recorded
under `## Clarifications` → `### Session 2026-10-04`. Pinned both ways, because a rule that
only ever excludes is indistinguishable from a parser that never parses:
`test_c8b_claim_inside_an_inline_code_span_is_a_mention_not_a_declaration` (exactly the one
bare claim survives two mentions) and `test_c8c_an_unclosed_code_span_leaves_the_claim_a_real_claim`
(an unclosed run is literal text per CommonMark, so the claim after it still declares).
`requirements.md` re-validated after the amendment: `status: ok`, five checks all `pass (0)`,
`0 error(s), 0 warning(s)`.

### 场景 5's seven counter-samples — each hits exactly its own label

Built in `mktemp -d`, run against the real script, then deleted. Contract fixture
`contracts/x.md` declares `**C-1**` and `**C-2**` (`md-bold-closed`).

| sample | real output (decisive line) | label hit | EXIT |
|---|---|---|---|
| `dangling-file` | `ERROR 3: green-dangling: T001 declares [green: contracts/nope.md#C-1] but no such contract file exists (looked beside dangling-file.md, then the repository root, then the working directory) …` | green-dangling ×1 | **1** |
| `dangling-clause` | `ERROR 3: green-dangling: T001 declares contracts/x.md#C-9 but that file contains no clause C-9 — name a clause id the file declares` | green-dangling ×1 | **1** |
| `cross-phase` | `WARN  3: green-cross-phase: T001 (line 3, `## Phase 1: Setup`, order 1) claims contracts/x.md#C-2 while the later T002 (line 5, `## Phase 2: And more`, order 2) claims #C-1 …` | green-cross-phase ×1 | **0** |
| `clause-collision` | `WARN  3: green-clause-collision: T001 (line 3) and T002 (line 4) both claim contracts/x.md#C-1 — … (条款分区 (Clause Partition), .specify/memory/glossary.md) …` | green-clause-collision ×1 | **0** |
| `path-divergence` 正 | `WARN  3: green-path-divergence: T001 (line 3) and T002 (line 5) both write tests/contract/test_x.py but claim different green points (['contracts/x.md#C-1'] vs ['contracts/x.md#C-2']) …` | green-path-divergence ×1 | **0** |
| `path-divergence` 反 | `WARN  3: green-clause-collision: …` and **no** divergence line — `0 error(s), 1 warning(s)` | green-path-divergence **0** | **0** |
| `fenced` | `PASS: … — 0 error(s), 0 warning(s)`; `--json` → `green_claims = []` | (none — 0 claims parsed) | **0** |

Every row above reports exactly one finding, so zero cross-masking is visible in the counts
and not only in the labels. The 反 row is the load-bearing half of C-16: same shared test
path, same green point → the label stays silent, which is what proves it detects *divergence*
rather than *path sharing*. Residue: `\rm -rf $tmp; ls -d $tmp | wc -l` → **0**.

### 场景 4 — the false alarm, positive control first

```text
POS: WARN  3: parallel-safe: [P] tasks T001 (line 3) and T002 (line 4) both WRITE ['docs/a.md']
     in phase `## Phase 1: Setup` — … never by deleting the cited path
     PASS (with warnings): …/pos.md — 0 error(s), 1 warning(s)                   POS_EXIT=0
NEG: PASS: …/neg.md — 0 error(s), 0 warning(s)                                   NEG_EXIT=0
```

`POS` still warns (the guard was not weakened) and `NEG` — two `[P]` rows writing
`docs/a.md` and `docs/b.md` while their `[green:]` tags both point at `contracts/x.md` — is
now completely clean, where the pre-change run recorded in the scenario reported
`both WRITE ['contracts/x.md']`. That is D-7's false alarm gone, and it is gone because
claims are extracted before classification, not because a label prefix was added to
`POINTER_GOVERNOR` (`test_c22…` asserts that table's pattern still contains no `green`).

### T022's own premise, falsified by execution

The task row asserts **"exit 0 today is IMPOSSIBLE"**. Measured after this phase:

```text
$ python3 scripts/python/validate-tasks.py .specify/specs/053-machine-decidable-artifacts/tasks.md
PASS: .specify/specs/053-machine-decidable-artifacts/tasks.md — 0 error(s), 0 warning(s)
VT_EXIT=0
```

So exit 0 is not merely possible, it is the current state. The row's reasoning was also
backwards: a file carrying no `[green:]` claim exits 0 *because* there is nothing for the new
checks to fail on — absence of claims is what makes 0 the expected verdict, not what
forbids it. The row's real intent (paste the counter-sample battery, since there are no
claims of this feature's own to demonstrate until T045) is unaffected and is what the tables
above do. Annotated on the row rather than worked around; this is the same measurement
`/speckit.analyze` recorded as F-25.

## T024 — `tests/contract/test_clause_coverage.py` red first (2026-10-04)

Command: `python3 -m pytest tests/contract/test_clause_coverage.py -q`, before T025 landed:

```text
27 failed, 10 passed in 0.81s
FAILED …::test_c7_relational_sentinel_is_printed_and_holds_never_a_literal_total
FAILED …::test_c8_named_count_tracks_the_owner_coverage_and_is_printed_with_the_form_set
FAILED …::test_c9_named_list_is_collapsible_behind_an_explicit_flag
FAILED …::test_c10_openapi_clauses_are_method_keys_and_the_total_matches_the_census
FAILED …::test_c12_no_pyyaml_dependency_anywhere_in_the_chain
FAILED …::test_c13_parse_doubt_yaml_is_named_and_never_guessed_zero
FAILED …::test_c15_parseable_but_zero_clause_file_is_named_with_a_companion
FAILED …::test_c16_uncovered_is_a_set_difference_with_the_str009_prefix_both_directions
FAILED …::test_c17_an_empty_uncovered_set_carries_a_non_empty_companion
FAILED …::test_c17b_a_zero_denominator_turns_the_sentinel_red
FAILED …::test_c18_the_two_lanes_are_separate_sections_with_separate_counts
FAILED …::test_c18b_deleting_one_citation_from_a_group_makes_that_fr_uncovered
FAILED …::test_c19_uncovered_names_are_sorted_one_per_line_and_comm_consumable
FAILED …::test_c20_the_accountant_writes_nothing_and_changes_no_byte_of_the_corpus
FAILED …::test_c21_baseline_discipline_comm_delta_paired_with_a_non_empty_claim
FAILED …::test_c22_baseline_internal_items_still_print_their_count
FAILED …::test_c23_the_baseline_header_records_the_form_set_and_the_freeze_context
FAILED …::test_c24_the_idiom_is_a_sorted_name_list_consumed_by_comm_not_a_second_form
FAILED …::test_c25_the_baseline_is_not_the_gate_scanner_broken_json_shape
FAILED …::test_c26_every_yaml_contract_is_explicitly_disposed
FAILED …::test_c27_the_sc006_evidence_form_is_three_numbers_and_a_sum_assertion
FAILED …::test_form_str008_attribution_and_four_label_docstring_body
FAILED …::test_form_exit_code_table
FAILED …::test_form_json_key_set_verdict_array_and_status_vocabulary
FAILED …::test_form_human_tail_line_is_the_str003_shape
FAILED …::test_form_positional_artifact_path_is_accepted
FAILED …::test_form_the_script_is_read_only_by_write_point_scan
```

**The 10 green-before, each with what turns it red.** C-1…C-6 are the *owner document*'s clauses
and it landed in Phase 2 (T003); C-11 and C-14 pin `clause_extract.py`, which landed in Phase 2
(T005); the last two pin artifacts that predate this feature:

| test | green before T025 because | goes red when |
|---|---|---|
| `test_c1_owner_doc_exists_declares_ownership_and_points_at_uic` | T003 landed the owner doc | the self-declaration is reworded away, or the UFC pointer becomes a copy of its class table |
| `test_c2_owner_doc_declares_all_six_forms_and_the_three_block_rules` | same | a form or one of the three block rules (boundary / citation group / mentions) is dropped |
| `test_c3_exactly_one_canonical_form_and_legacy_forms_are_read_only` | same | a second form is declared canonical |
| `test_c4_owner_doc_copies_no_clause_body_from_any_contract` | same | the owner doc starts carrying clause bodies (sentinel: it compares >100 clause bodies, so an empty offender list is not an empty scan) |
| `test_c5_gate_budget_is_unchanged_by_the_owner_document` | measured 23 / 0 | any `shared/` wording trips a BLOCKING pattern — integer headroom is 0 |
| `test_c6_the_cap_is_pinned_in_three_forms_with_meta_pins` | pins predate this feature | a pin's wording is edited, which is what the meta-pins exist to catch |
| `test_c11_the_misnamed_yaml_is_judged_by_content_and_yields_its_six_ids` | T005 landed the extractor | the form decision starts using the file extension |
| `test_c14_the_paren_form_file_contributes_the_clauses_a_closed_regex_would_drop` | same | the extractor regresses to the closed-bold regex only (sentinel asserts the fixture still fails that regex) |
| `test_form_ships_via_the_force_include_mapping` | `pyproject.toml` predates this feature | the wheel mapping stops covering `scripts/` |
| `test_the_contract_still_has_the_clause_count_this_suite_pins` | the contract is authored | clause-coverage.md's count moves off 27 |

**Two assertion defects found by the red run, both fixed on the assertion side** (the subjects
were already correct — this is the failure-attribution step, stated so the fix is not read as
"making the subject satisfy a wrong assertion"):

- C-2's regex needles were double-escaped (`r"\*\*C-\\d"`), so they searched for a literal
  backslash-`d` that no document contains. Changed to plain substring checks.
- C-4's probe was "the first 40 characters of the clause body appear in the owner doc". That
  matched `051-user-facing-comprehension/contracts/discipline-doc.md#C-2`, whose body *begins
  with the user-facing-comprehension path* — the same path C-1 **requires** the owner doc to
  carry. C-4 exempts citation forms, so the probe now strips code spans before comparing and
  requires ≥40 characters of prose, plus a sentinel that >100 clause bodies were compared.

## T025/T026/T027/T028 — US3 landed, real output (2026-10-04)

Suite state after T025 + T026: `test_clause_coverage.py` → **39 passed, 0 failed**.

### T028's three counter-samples (temp dir, residue 0)

One corpus, four contract files, each planted to break exactly one proposition:

```text
scanned 4 files: parsed 2 + named-unparseable 2 == 4  [relational sentinel OK]
  per form: md-bold-closed 1 files/1 clauses; yaml-openapi 1 files/0 clauses;
            yaml-assertions 1 files/6 clauses; md-none 1 files/0 clauses
  zero-clause-but-parseable (parse doubt): 1
  .yaml: parsed 1 / total 2 / named 1
  NAMED: 001-alpha/contracts/flow.openapi.yaml
  NAMED: 001-alpha/contracts/prose.md
  [clause-unparsable] fail (2) — 2 files yield no clause id under the owner's forms;
      1 of them declares a positive form, which is parse doubt and is never read as
      zero-and-covered
FR universe: 1 | FR claimed: 1 | FR uncovered: 0
6 error(s), 1 warning(s)   status: uncovered   ACC_EXIT=1
残留计数: 0        (after `\rm -rf $tmp`; `ls -d $tmp | wc -l` → 0)
```

Per-file, form and ids judged by **content**:

| planted file | suffix | form | ids | which clause it breaks |
|---|---|---|---|---|
| `flow.openapi.yaml` — `paths: {/v1/x: {get: …}}` all on one line | `.yaml` | `yaml-openapi` | **0** | **C-13**: stream-style yaml is parse doubt, so it is NAMED and drives `clause-unparsable` to **fail**; it is never counted as "0 clauses, therefore covered" |
| `prose.md` — headings and prose, no clause marker | `.md` | `md-none` | **0** | **C-15**: parseable but zero clauses, so it appears in the named set instead of vanishing from the denominator |
| `definitely-not-openapi.yaml` — the real `013-…` file, **renamed** | `.yaml` | `yaml-assertions` | **6** | **C-11**: the misnomer resolves by content, not by name; its six ids (`no-tool-discovery-step`, `no-tool-template-boilerplate`, `no-mandatory-tool-manifests`, `no-refresh-tools-in-script`, `mirror-parity`, `no-tool-manifest-in-checklist`) entered the universe and surfaced as six real `UNCOVERED:` names |
| `c.md` — the control | `.md` | `md-bold-closed` | **1** | positive control: a well-formed contract parses and its clause is claimed by T001, so `claimed clauses 1` is non-zero and the three rows above are not "nothing parsed at all" |

The control matters: without `c.md` a run where the extractor simply crashed on every file would
print the same `named 2` / `parsed 0` shape and look like a pass (checker-form C-21).

### Two defects found by running US3, both written back rather than worked around

1. **The universe silently lost 24 clauses** (`clause universe: 665` against 689 extracted ids).
   Cause and disposition are in `notes/quickstart-run.md` § 场景 6 and escalated as `research.md`
   **A-8**; the owner document now records the non-uniqueness and the duty to print both numbers,
   without changing the declared syntax (that is the owner's call, not an implementation run's).
2. **`comm -13` reported a delta of 665 where the truth was 182**, with a warning on stderr that
   a piped check would have swallowed. Cause: codepoint-sorted names versus glibc collation, which
   ignores `#`/`/`/`.` — the baseline's two header lines sort after digit-initial names under
   `en_US.UTF-8`. Fixed by specifying `LC_ALL=C` at all three reachability points (baseline header,
   script docstring, `tasks.md` GATE-8), pinned by `test_c24b…`, and `test_c24…` was strengthened:
   its first version compared against an **empty** baseline, where `comm -13` echoes all of file 2
   whatever the ordering — so it passed for a reason that had nothing to do with the idiom working.
   It now runs with both sides non-empty. `contracts/clause-coverage.md` C-19 was amended to say
   which ordering "已排序" means; its citation group is unchanged (`(SC-005、D-10)`), verified by
   re-running the extractor, so `feature-ref.md`'s published mapping does not move.

### Scope note: the accountant is not in `test_checker_form.py`'s per-artifact battery

`NEW_CHECKERS` in that suite listed `account-clause-coverage.py`, and its `_SKIP_ALLOWED` entry was
the only reason that stayed invisible — the skip hid a premise that execution falsifies. That battery
hands a checker one artifact file and expects a verdict on *that file*: `main([requirements.md]) == 0`,
a `skeleton` status for a placeholder-only file, exit 1 for an FR gap. The accountant takes a spec
directory and accounts a whole corpus (FR-023…FR-028), it has no skeleton concept, and FR-gap
detection is `validate-requirements.py`'s job — duplicating it here would create a second owner for
one rule. Its exit-0 state is also unreachable until T045 retro-fits this feature's own claims, so
pinning it there would have been a permanently red test rather than a guard. What it *does* share
with every new script (STR-008 attribution, docstring label body, zero write points, packaging) is
asserted in that suite's `ALL_NEW_SCRIPTS` set, and its own form obligations — label set, exit table,
JSON key set with a verdict array, STR-003 tail, positional-artifact form — are pinned here, which is
what that suite's docstring already claimed.
