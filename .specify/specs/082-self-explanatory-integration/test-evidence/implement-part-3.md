# Implement stage evidence — part 3 (`part_scope=T013-T018`)

**Stage**: implement, part 3 of 10 | **Captured**: 2026-11-05 | **Base commit**: `8daf6b65`
**Working dir**: repository root (`/storage/project/cloud-native-ai/spec-kit`)
**Selection**: targeted-set-v1 (TEST BUDGET: the single full-suite run of this stage happened in
part 1 as E2; no second full suite is run here — 26 failed / 7156 passed / 1 skipped remains the
only full-suite reading of this stage)

## E3 stage-status row (implement part 3)

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T013-T018 |
| status | us1-green-and-mutation-legs-proven |
| command | `python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q -k 'not c21'` then `python3 -m pytest tests/contract/test_constitution_double_landing.py -q` |
| selection_basis | targeted-set-v1 — the two commands are exactly the pair the dispatch brief names for this part: the US1 guard subset (whose subject this part completes) and the carrier whose count constants this part owns (T016) |
| selected_paths | `tests/contract/test_self_explanatory_constitution.py` (subject completed: the principle and the mandate entry now exist), `tests/contract/test_constitution_double_landing.py` (edited: T016 raises three counts and appends the watchlist) |
| sufficiency | the two files above are the only guards that judge the surfaces this part edits (`templates/constitution-template.md` via T011/T015, `skills/internal/manage-constitution/SKILL.md` via T013, `.specify/memory/constitution.md` via T017). Two further guards were run because their pinned constants reference the same subjects and would otherwise have been left silently stale: `test_fast_fail_discipline.py` (re-pins the carrier's three counts, the watchlist length and the live version) and `test_confirmation_gates_sweep.py` (pins the gate total, the C-8 subject). Sufficiency is claimed for **the edit set**; the full-suite verdict belongs to the Completion Gate, which this part does not run. |
| rc | 0 (both mandated commands) |
| passed | 12 (US1 subset) + 19 (carrier) |
| failed | 0 in the selected set |
| new_failures | none in the selected set. One declared expected-red remains outside it: `test_self_explanatory_constitution.py::test_c21_instructions_summary_is_at_most_two_sentences` (`-k 'not c21'` excludes it by design; C-21's green is T024's) |
| baseline | `.specify/specs/082-self-explanatory-integration/baseline-failed.txt` (26 entries, full-suite names from E2); comparison is name-level |

### Command output, verbatim

```console
$ python3 -m pytest tests/contract/test_self_explanatory_constitution.py -q -k 'not c21'
............                                                             [100%]
12 passed, 1 deselected in 0.06s
EXIT=0

$ python3 -m pytest tests/contract/test_constitution_double_landing.py -q
...................                                                      [100%]
19 passed in 0.06s
EXIT=0
```

### Sufficiency companion set (run because these guards pin values T016/T017 moved)

```console
$ python3 -m pytest tests/contract/test_fast_fail_discipline.py \
                   tests/contract/test_confirmation_gates_sweep.py \
                   tests/contract/test_self_explanatory_constitution.py -q
3 failed, 160 passed in 3.04s
EXIT=1

$ # name-level comparison against baseline-failed.txt
$ LC_ALL=C comm -13 baseline-sorted.txt current-sorted.txt     # NEW failures not in the baseline
tests/contract/test_self_explanatory_constitution.py::test_c21_instructions_summary_is_at_most_two_sentences

$ LC_ALL=C comm -12 baseline-sorted.txt current-sorted.txt     # still failing, inherited
tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target
tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline
```

The two inherited failures are in `baseline-failed.txt`: `test_residual_total_within_sc002_target`
is the gate-total target pinned by another feature, and `test_g9_total_equals_frozen_baseline` pins
the same frozen total at 23 against a scanner that reports 27. Neither moved on this feature's
account — the scanner total is 27 before and after this part (T002 measured 27 in part 1; T049 will
re-measure it as the terminal check). The only NEW failure is the declared C-21 expected-red.

## What each row actually asserted (closure record)

| Row | Clause | Where the assertion lives | State after this part |
|-----|--------|---------------------------|-----------------------|
| T013 | C-5 | `skills/internal/manage-constitution/SKILL.md` `- **MUST include**` block, 11th sub-entry `  - **Self-Explanatory Structure (不言自明)** — …` carrying the truth anchor, the "referenced, not restated" clause and the no-machinery limit | landed; entry count 10 → 11 |
| T014 | C-24 | `skills/internal/manage-constitution/SKILL.md` and `.specify/skills/internal/manage-constitution/SKILL.md` byte-identical (`cmp`), `sync-mirrors.py --check` exit 0 across all six pairs | green |
| T015 | C-1, C-2, C-3, C-4, C-6, C-7 (template side), C-8, C-20 | `test_self_explanatory_constitution.py` US1 subset | 12 passed |
| T016 | C-7 (mandate side), C-9 | `test_constitution_double_landing.py`: `DOUBLE_LANDING_WATCHLIST` + the new title; `TEMPLATE_COUNT` 17→18, `LIVE_COUNT` 18→19, `COMMAND_COUNT` 10→11, each with its change source in the inline note | 19 passed |
| T017 | C-9 (live landing), C-4 | `.specify/memory/constitution.md` § `### XIX. Self-Explanatory Structure (不言自明)`; `**Version**:` 1.15.0 → 1.16.0 (MINOR); Sync Impact Report prepended, naming this amendment's principle | green; `test_c11`/`test_c12` of the carrier turn green |
| T018 | C-1, C-7 | `notes/red-first-evidence.md` § T018: M-1 and M-2 on `mktemp -d` copies, with anti-vacuity companions and a sha256 unchanged-repository proof | both legs PASS |

## In-passing repairs (corrections, disclosed)

Three collateral guards pinned values that T016/T017 legitimately moved. Each is a **correction**
(one reading consistent with the recorded intent, local, reversible, no downstream premise
falsified) and is disclosed here rather than raised:

1. **`test_fast_fail_discipline.py::test_x13_double_landing_three_count_pins`** — pins the carrier's
   `TEMPLATE_COUNT`/`LIVE_COUNT`/`COMMAND_COUNT` and the artifact-side counts. Raised 17/18/10 → 18/19/11
   and 17/18/10-artifact → 18/19/11-artifact, with the stale-pin note extended. This guard's stated
   job is "the three count pins were raised in the same batch"; leaving it at the old values would
   make it assert the opposite of the landing.
2. **`test_fast_fail_discipline.py::test_x15_watchlist_gains_principle_title`** — pins the watchlist
   length (5 → 6). Repointed at the **derived** newest entry rather than a hard-coded title: this
   module's `PRINCIPLE_TITLE` is rebound to the Fast Fail title at the constitution-export section
   (line ~933 overrides the constant at line ~99), so the old spelling asserted membership of a
   title the append never touches — a check that could not go red on its own subject.
3. **`test_fast_fail_discipline.py::test_x18_downstream_gate_rows_15_to_16`** — pins the live roster
   row count (18 → 19) and its before-state (17 → 18). The amendment added one principle.
4. **`test_fast_fail_discipline.py::test_x5_live_version_minor_bump`** — pins the live `**Version**:`
   literal (1.15.0 → 1.16.0). A version pin must move with the version, or it fails by construction.
5. **`test_fast_fail_discipline.py::test_x6_sync_impact_report_prepended`** — asserted that the
   **Fast Fail** title appears in the first 40 lines of the live constitution. That was true only
   because the 1.15.0 report block happened to sit inside the window; prepending a newer block
   pushes it out, so the assertion failed while every proposition it was written to judge held.
   Repointed at C-12's already-established form: derive the newest `DOUBLE_LANDING_WATCHLIST` entry
   and require the head window to name it. This is the same repair C-12 in the carrier received for
   the same reason, and it is the reason this one is a correction rather than a widened window.

No guard was weakened to make a step green: none of the five asserts less than it did before, and
each keeps its own subject. The two *inherited* failures were left untouched — they are other
features' pins, and repairing them here would be out of this part's scope.

## Out of scope, verified not done

- No plan-owned artifact touched: `requirements.md`, `plan.md`, `data-model.md`, `contracts/`,
  `quickstart.md`, `research.md`, `feature-ref.md` are unmodified (no PLAN-EDIT owed).
- No edit to `templates/instructions-template.md`, `scripts/bash/generate-instructions.sh`,
  `.specify/instructions.md` or the live instructions — all belong to US2 (T019-T028).
- No Completion Gate, no Feature status flip, no implement Feedback / Wrap-up, no push.
