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
