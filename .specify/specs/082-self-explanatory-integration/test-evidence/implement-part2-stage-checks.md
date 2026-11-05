# Implement stage evidence — part 2 (`part_scope=T007-T012`)

**Stage**: implement, part 2 of 10 | **Captured**: 2026-11-05 | **Base commit**: `1cec4933`
**Working dir**: repository root (`/storage/project/cloud-native-ai/spec-kit`)
**Selection**: targeted-set-v1 (TEST BUDGET: the single full-suite run of this stage happened in
part 1 as E2; no second full suite is run here)

## E3 stage-status row (implement part 2)

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T007-T012 |
| status | us1-tests-and-first-implementation-landed |
| command | `bash scripts/bash/run-tests.sh --names-out <scratch>/current2.txt <9 targeted paths> -q` |
| selection_basis | targeted-set-v1 — every path is either a file this part edited, a file whose subject this part changed, or a guard that pins a value this part touched |
| selected_paths | `tests/contract/test_self_explanatory_constitution.py` (edited: T007-T010), `tests/contract/test_constitution_double_landing.py` (pins `TEMPLATE_COUNT`), `tests/contract/test_instructions_section_propagation.py` (template heading set), `tests/contract/test_one_source_of_truth.py` (template section shape), `tests/contract/test_confirmation_gates_sweep.py` (pins the gate total), `tests/contract/test_user_facing_comprehension_section.py` (guideline-pointer coverage), `tests/contract/test_instructions_size_budget.py` (template size), `tests/contract/test_mirror_parity_suite.py` (byte parity of every source/mirror pair), `tests/contract/test_bilingual_expression.py` (sweeps `templates/` for STR literals and enumeration keywords) |
| sufficiency | the three surfaces this part can affect are (1) the constitution template, (2) its mirror, (3) the generator's downstream consumption. Every targeted path asserts one of those; the residual risk is a guard outside these nine that reads `templates/constitution-template.md`, and that population was checked to be exactly these files by the part's edit set. Sufficiency is claimed for **the edit set**, not for the whole suite — the full-suite verdict belongs to the Completion Gate (not run in this part). |
| rc | 1 |
| passed | 892 |
| failed | 4 |
| new_failures | 2 (both expected/declared, named below) |
| baseline | `.specify/specs/082-self-explanatory-integration/baseline-failed.txt` (26 entries, full-suite names from E2); comparison is name-level, `LC_ALL=C comm -13` on sorted copies |

### Name-level comparison (the only honest form: the baseline is a full-suite list)

```console
$ LC_ALL=C comm -13 baseline-sorted.txt current2-sorted.txt     # NEW failures not in the baseline
tests/contract/test_constitution_double_landing.py::test_c1_template_carries_both_new_principles
tests/contract/test_self_explanatory_constitution.py::test_c21_instructions_summary_is_at_most_two_sentences

$ LC_ALL=C comm -12 baseline-sorted.txt current2-sorted.txt     # still failing, inherited
tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target
tests/contract/test_user_facing_comprehension_section.py::test_c11_no_dangling_guideline_pointer_on_either_instruction_surface
```

### The two new failures, both declared before they were measured

1. **`test_constitution_double_landing.py::test_c1_template_carries_both_new_principles` —
   EXPECTED-RED, declared by `tasks.md` T016.** The template now carries 18 principles; that
   carrier's `TEMPLATE_COUNT` is a load-time constant pinned at 17, and T016 is the row that raises
   `TEMPLATE_COUNT` 17→18 / `LIVE_COUNT` 18→19 / `COMMAND_COUNT` 10→11 together with the watchlist
   append. Measured proof that the red is the **count pin** and not the new title: in the same file,
   `-k "c7 or c5 or c10"` is 4 passed, and the other 20 tests of both pre-existing suites pass
   (21 collected, 1 failed). The principle itself lands green.
2. **`test_self_explanatory_constitution.py::test_c21_instructions_summary_is_at_most_two_sentences` —
   EXPECTED-RED, waiting on T022.** C-21 bounds the summary of the **instructions** section, which
   `tasks.md` T022 (part 3) creates; this module owns the assertion. The failure text names the
   missing artifact verbatim ("`templates/instructions-template.md` has no `## Self-Explanatory
   Structure (不言自明)` section"), so the red is attributable to an absent subject rather than to a
   mistyped assertion.

Neither red is counted as a regression, and neither is "fixed" by weakening the guard: both close
by the artifact landing, in the parts that own them.

### Not-the-red / calibration note

`tasks.md` grouped T010's two clauses (C-20, C-21) into one row because they are "both read-only
assertions inside the same new module". C-20's mechanism is cross-surface (owner headings absent
from both templates) and is green now; C-21's subject does not exist until T022. The row's own
premise — that both clauses land in this part — therefore holds for the **assertion**, not for the
green. Recorded here so a later reader does not read the single red as a missing clause.

## What each row actually asserted (closure record)

| Row | Clause | Where the assertion lives | State after this part |
|-----|--------|---------------------------|-----------------------|
| T007 | C-1, C-3, C-4 | `test_c1_template_carries_the_principle`, `test_c3_matcher_resolves_the_principle_under_an_unused_numeral`, `test_c4_no_pinned_numeral_where_this_principle_lands` | green |
| T008 | C-2, C-6 | `test_c2_the_principle_block_satisfies_the_house_shape` + three C-6 tests | green |
| T009 | C-7 (both-sided set judgement) | template side in the new module (`test_c7_template_side_membership_of_every_watchlist_title`, `test_c7_mutation_leg_m1_…`); generator-mandate side in the carrier (owner of the mandate set and its count) | template side green; mandate side EXPECTED-RED until T013 — by design, not duplicated here |
| T010 | C-20, C-21 | `test_c20_no_owner_heading_is_copied_onto_a_projected_surface` (both surfaces, parametrized), `test_c21_instructions_summary_is_at_most_two_sentences` | C-20 green on both surfaces; C-21 EXPECTED-RED until T022 |
| T011 | C-2 artifact | `templates/constitution-template.md` § `### XVIII. Self-Explanatory Structure (不言自明)` | landed, 6 logical bullets, all under 100 chars |
| T012 | C-8 | `notes/pre-change-measurements.md` § T012 (`hits: []`) | `hits: []`, whole-scan total 27 (unchanged) |

## C-7 is one-sided here on purpose

The new module asserts the **template** half of C-7; the **generator-mandate** half stays in
`tests/contract/test_constitution_double_landing.py`, which owns the MUST-include set and the
`COMMAND_COUNT` constant that goes with it. Asserting it in both places would create a second
spelling of the same rule — the exact defect the parent principle forbids. Consequence, stated
plainly: C-7 as a whole is not green after this part; its mandate half turns green at T013.

## Contract-test red-first correction (in-passing repair, disclosed)

Two drafts of the new module were red for a reason that was **not** the missing artifact, and both
were repaired rather than accepted:

1. `test_c1_…`-adjacent self-check `test_c4_…` originally searched the module's **own source text**
   for a `### <numeral>. Self-Explanatory` pattern. C-3 requires the module to carry exactly such
   a probe under an unused numeral, so the check could never go green while the required probe
   existed — it forbade the thing it was guarding. Repointed at the compiled matcher instead.
2. The obligation table's uniqueness search passed compiled patterns through a nested
   comprehension. A generator-expression scope can rebind the row's second element to a stale match
   object, and the symptom was a **coverage** failure ("obligation X uncovered") caused by a
   **search** defect — the worst kind of diagnostic, since it points at the artifact. Replaced with
   string markers and an explicit "unplaced, continue" loop, so a non-distinctive marker is
   reported as its own failure instead of blaming a downstream obligation.

Both are corrections (one reading consistent with the contract, local, reversible), so they were
repaired in place and are listed here rather than raised as upsends.

## Out of scope, verified not done

- No plan-owned artifact touched: `requirements.md`, `plan.md`, `data-model.md`, `contracts/`,
  `quickstart.md`, `research.md`, `feature-ref.md` are unmodified (no PLAN-EDIT owed).
- No edit to `skills/internal/manage-constitution/SKILL.md` and no edit to the live constitution —
  both belong to T013/T017.
- No Completion Gate, no Feature status flip, no implement Feedback / Wrap-up, no push.
