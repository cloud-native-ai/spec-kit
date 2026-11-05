# Implement part 4/10 — E3 stage-status evidence

**Part scope**: T019-T023 (US2 tests + instructions template section + budget constant)
**Date**: 2026-11-05
**Stage base**: `2161ac40` (part 3 checkpoint)

## E3 stage-status row

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T019-T023 |
| status | tests-green, template landed, budget raise **undecided** (two readings) |
| command | `python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q` → **rc 0**, 13 passed |
| | `python3 -m pytest tests/contract/test_instructions_section_propagation.py -q` → **rc 1**, 5 passed / 1 failed (`test_c1_live_instructions_carry_all_template_sections`) |
| | `python3 -m pytest tests/contract/test_instructions_size_budget.py -q` → **rc 0**, 13 passed |
| selection_basis | targeted-set-v1 — the three commands the dispatch brief names verbatim: the new US2 carrier, the file that owns the template/live propagation guard, and the budget carrier whose subject T021/T023 edit |
| selected_paths | `tests/contract/test_instructions_section_propagation.py`, `tests/contract/test_instructions_size_budget.py`, `tests/contract/test_self_explanatory_constitution.py` (the C-21 green the brief requires to be re-measured after T022) |
| sufficiency | those three are the only guards judging the surfaces this part edits (`templates/instructions-template.md`, `scripts/bash/generate-instructions.sh`, and the two test files). Sufficiency is claimed for the **edit set**; the full-suite verdict belongs to the Completion Gate and is not run here (TEST BUDGET) |
| rc | 0 / 1 / 0 |
| passed / failed | 13 + 5 + 13 passed; 1 failed |
| new_failures | **exactly one**, and it is the deferred C-15 obligation: `test_c1_live_instructions_carry_all_template_sections` now reports the missing `## Self-Explanatory Structure (不言自明)` in the live file. That state is the designed consequence of T022 landing the template section while T024 owns the live reconcile. The same test **passed** at `2161ac40` (verified by `git show HEAD:…`), so it is attributable to this part, and it closes at T024 — not a regression this part may paper over |
| baseline | `baseline-failed.txt` (26 entries from E2). The single new failure above is above the baseline and is named here rather than folded into it |
| evidence_ptr | this file; red/green capture and the C-21 shape finding in `notes/red-first-evidence.md` § R-4; measurements in § Measurements below |

### Additional confirmation (not a second full suite)

Combined run of the four carriers this part touches or depends on, with only the deferred case
deselected:

```text
$ python3 -m pytest tests/contract/test_self_explanatory_constitution.py \
    tests/contract/test_instructions_section_propagation.py \
    tests/contract/test_instructions_size_budget.py \
    tests/contract/test_constitution_double_landing.py -q \
    --deselect tests/contract/test_instructions_section_propagation.py::test_c1_live_instructions_carry_all_template_sections
50 passed, 1 deselected in 8.11s
```

Including the US1 carrier (`test_constitution_double_landing.py`, 19 tests) proves part 3's
landing is undisturbed by this part's template edit.

## Red / green capture (T019/T020/T021, before any artifact changed)

```text
$ python3 -m pytest tests/contract/test_instructions_section_propagation.py -q     # before T022
FAILED ...::test_c10_template_carries_the_section_and_its_runtime_pointer
FAILED ...::test_c11_section_is_summary_plus_pointer_not_a_copy
FAILED ...::test_c14_template_side_presence_survives_rendering
3 failed, 3 passed in 1.67s   rc=1

$ python3 -m pytest tests/contract/test_instructions_size_budget.py -q              # before T023
13 passed in 6.46s            rc=0
```

After T022 (`templates/instructions-template.md` carries the section):

```text
$ python3 -m pytest tests/contract/test_instructions_section_propagation.py -q -k "c10 or c11 or c14"
4 passed, 2 deselected in 0.05s   rc=0
$ python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q
13 passed in 0.06s                rc=0     # C-21 green, as the brief predicted after T022
```

The C-17 assertion is green before and after this part by design — see the ordering note in
`notes/red-first-evidence.md` § R-4.

## Measurements

| quantity | before this part | after T022 | source |
|----------|------------------|------------|--------|
| live `.specify/instructions.md` | 32739 B | 32739 B (unchanged — T024 owns the reconcile) | `wc -c` |
| template section cost | — | 618 B (1 summary sentence + 1 pointer line) | section slice of `templates/instructions-template.md` |
| simulated post-injection live size | — | **33357 B** | generator run on a `mktemp -d` fixture holding a copy of the current live file + the current template |
| fixture re-run (idempotence) | — | `Section reconcile: live instructions already carry all template sections.` | same fixture, second run |
| budget constant | 32768 | **34816** (applied) | `grep -n '^INSTRUCTIONS_BUDGET_BYTES=' scripts/bash/generate-instructions.sh` |
| generator verdict at 34816 | `over` (size 33357 ≥ 32768) | `Instructions size: 33357 B (budget 34816 B, 1459 B headroom)` | fixture run under the new constant |
| alternative: short-body template | — | 33233 B → **33792 leaves 558 B headroom**, also compliant | same fixture with a one-sentence-body template copy |

`over` fires at `size >= budget`, so headroom as `budget - 1 - size`. Both candidate constants
satisfy the letter of the T-001 rule; see the part checkpoint for the open reading.

## Scenario coverage

T022's task text requires the section body to be "≤ 2 summary sentences". The section carries **one**
summary sentence plus the pointer, which satisfies the bound. The second summary sentence drafted
first was dropped because the C-21 carrier removes whole lines containing the pointer path before
counting, and because that sentence restated owner rules (the duplication C-20/C-21 exist to
prevent). Recorded as an in-passing correction with the transcript in `notes/red-first-evidence.md`.

## Not done in this part (by design)

- No live reconcile (`bash scripts/bash/generate-instructions.sh`) on the repository — T024.
- No symlink check (T025), no mirror sync (T026), no M-3/M-4 mutation legs (T027): mirrors and the
  live file are part 5's scope.
- No Completion Gate, no Feature status flip, no implement Feedback/Wrap-up, no push.
- No plan-owned artifact touched (`PLAN-EDIT: none`).
