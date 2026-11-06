# Implement part 9 — T044-T047 (US4 remainder: status persistence, the untouched mechanism suite, the unwired command, the name sweep)

- **stage**: implement
- **part**: 9/10
- **part_scope**: `T044-T047`
- **stage_base**: `5085f46f`
- **test_budget**: targeted-set-v1 (E2's single full suite from part 1 stands unchanged: 26 failed /
  7156 passed / 1 skipped; **no second full suite is run here**)
- **docs-only**: no — one contract module gains two assertions; no non-test source file is edited, and
  the glossary store is byte-identical before and after
- **not started by design**: T048+ (Polish) and T053 (C-34, which the part plan places in P10)

## E3 stage-status row (implement part 9)

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T044-T047 |
| status | us4-status-persistence-guarded-unwired-command-proven-name-sweep-green |
| command | (1) `python3 -m pytest tests/contract/test_self_explanatory_glossary.py -q`; (2) `python3 -m pytest tests/contract/test_glossary_mechanism.py -q`; (3) `git diff --stat --exit-code tests/contract/test_glossary_mechanism.py`; (4) `git diff --stat --exit-code templates/commands/improve.md`; (5) `grep -c 'best-practice-optimization' templates/commands/improve.md`; (6) `grep -cF 'Self-Explanatory Structure (不言自明)' <four client-facing outputs>`; (7) `grep -cF '.specify/shared/definitions/self-explanatory-definitions.md' <same four>`; (8) `python3 .specify/.tmp/082-part9/red_legs.py` |
| selection_basis | targeted-set-v1 — exactly the surfaces this part writes or asserts on: the glossary carrier module (T044 lands in it), the mechanism suite the brief names for T045, the two command templates T046/T047 measure (`improve.md` as a subject, the four name-bearing outputs as read-only), and the red-leg driver for the two new assertions |
| selected_paths | `tests/contract/test_self_explanatory_glossary.py` (edited: +2 assertions, +C-33 in the docstring clause list), `tests/contract/test_glossary_mechanism.py` (read-only; must stay green **and unmodified**), `templates/commands/improve.md` (read-only), `.specify/memory/glossary.md` (read-only), `templates/constitution-template.md` / `templates/instructions-template.md` / `.specify/memory/constitution.md` / `.specify/instructions.md` (read-only name sweep) |
| sufficiency | the two suites are the complete automated judge set for this part's surfaces: the glossary carrier owns C-33 and C-29/C-30/C-32 (the same row), the mechanism suite is the guard C-31 names and the one T045 must prove untouched. T046 and T047 are **measurement rows**, not new guards — their evidence is command output (diff emptiness, zero matches, per-file counts), and adding a test that re-runs `git diff` would report the working tree rather than the repository. Sufficiency is claimed for **the edit set**; the full-suite verdict belongs to the Completion Gate, which this part does not run |
| rc | 0 (glossary carrier, 10 passed), 0 (mechanism suite, 12 passed), 0 (mechanism diff, `--exit-code`), 0 (improve.md diff, `--exit-code`), 1 (the `grep -c` for a **wanted** zero), 0 (both name sweeps), 0 (red-leg driver) |
| passed / failed | 10 passed / 0 failed (carrier, was 8); 12 passed / 0 failed (mechanism); 7 PASS / 0 FAIL (red legs, 2 controls + 4 legs + 1 isolation) |
| new_failures | none in the selected set |
| baseline | `.specify/specs/082-self-explanatory-integration/baseline-failed.txt` (26 entries) — no entry in the selected set names `glossary`, `self_explanatory` or `mirror_parity`, so no comparison was triggered |
| evidence_ptr | `notes/pre-change-measurements.md` § T044 / § T046; `notes/quickstart-run.md` § T047; red-leg transcript verbatim in § T044 above and reproduced in this file |

### Command output, verbatim

```console
$ python3 -m pytest tests/contract/test_self_explanatory_glossary.py -q
..........                                                               [100%]
10 passed in 0.12s
EXIT=0

$ python3 -m pytest tests/contract/test_glossary_mechanism.py -q
............                                                             [100%]
12 passed in 0.16s
EXIT=0

$ git diff --stat --exit-code tests/contract/test_glossary_mechanism.py
(no output)   DIFF_EXIT=0        # T045: the mechanism suite is unmodified

$ git diff --stat --exit-code templates/commands/improve.md
(no output)   DIFF_EXIT=0        # T046: the command template is unmodified

$ grep -c 'best-practice-optimization' templates/commands/improve.md
0             GREP_EXIT=1        # T046: no reference to the optimization workflow

$ grep -cF 'Self-Explanatory Structure (不言自明)' templates/constitution-template.md \
      templates/instructions-template.md .specify/memory/constitution.md .specify/instructions.md
templates/constitution-template.md:1
templates/instructions-template.md:1
.specify/memory/constitution.md:2
.specify/instructions.md:1
EXIT=0                            # T047: each ≥ 1 (the live 2 = heading + Sync Impact Report line)

$ grep -cF '.specify/shared/definitions/self-explanatory-definitions.md' <the same four files>
… :1  … :1  … :1  … :1
EXIT=0                            # T047: each client-facing output carries the runtime pointer

$ python3 .specify/.tmp/082-part9/red_legs.py
[PASS] control: status assertion green on the untouched copy
[PASS] control: write-verb assertion green on the untouched copy
[PASS] C-33-a: exactly one row was promoted in the copy: the canonical row only; 131 other rows
       already read 'auto | confirmed' and are untouched
[PASS] C-33-a: status assertion is RED on a promoted copy: the canonical entry reads 'confirmed';
       promotion is a user-authoritative action (data-model.md T-B, requirements.md A6) and no
       automated step of this feature may flip it — not the engine write, not a later verification run
[PASS] C-33-m: the engine's list verb reports the promoted status: engine reads status='confirmed'
[PASS] C-33-b: write-verb assertion is RED when the flow gains a writing verb:
       ('--action add',) — re-read C-33 before letting it run
[PASS] isolation: real store sha256 unchanged: 21482f6444ed… -> 21482f6444ed…
VERDICT: PASS — 7 PASS / 0 FAIL
EXIT=0
```

## What each row actually asserted (closure record)

| Row | Clause | Where the assertion / measurement lives | State after this part |
|-----|--------|-----------------------------------------|-----------------------|
| T044 | C-33 | two assertions in `test_self_explanatory_glossary.py`: the engine's `--action list` reports `status == "proposed"` for the canonical row (and the failure text says *why* a `confirmed` is a violation), and the flow's write-verb set is empty. Redness observed on a **copy** by promoting exactly that row (C-33-a) and by naming a write verb (C-33-b). The decision line 「提升属用户动作(data-model T-B / 需求 A6),本特性不改写」 is recorded in `notes/pre-change-measurements.md` § T044 | green + red leg proven |
| T045 | C-31 | `git diff --stat --exit-code tests/contract/test_glossary_mechanism.py` → `DIFF_EXIT=0` (empty diff), then the suite → 12 passed `EXIT=0` | green, file unmodified |
| T046 | C-28 | `git diff --stat --exit-code templates/commands/improve.md` → `DIFF_EXIT=0`; `grep -c 'best-practice-optimization' …` → `0` (`GREP_EXIT=1` = no match). Both commands and outputs recorded in `notes/pre-change-measurements.md` § T046 under `OI-082-01`, with an explicit "mirrored ≠ wired" boundary and the open item left open | measured; OI-082-01 still `open` |
| T047 | — (name consistency) | two `grep -cF` sweeps over the four client-facing outputs: the bracketed `STR-003` form ≥ 1 per file (`1 / 1 / 2 / 1`) and the runtime owner pointer ≥ 1 per file (`1 / 1 / 1 / 1`); plus a variant scan proving the plural form is absent and the retired name is absent from all four. Output in `notes/quickstart-run.md` § T047 | green |

## Why T044 is not a re-run of T039

T039's `test_c29_…` already asserts `entry["status"] == "proposed"` — a snapshot of the field. C-33 is
a **persistence** claim ("no automated step may flip it"), which a snapshot cannot carry: it cannot
distinguish "still proposed" from "promoted after the snapshot was written", and nothing re-reads the
field after a later flow step. T044 adds the persistence shape — read through the engine's render/parse
round-trip, with its redness demonstrated by mutating a copy — rather than re-running the snapshot and
declaring the clause proven.

## Two in-passing corrections (disclosed)

1. **The first red leg promoted 131 rows.** The leg replaced the substring `"| auto | proposed |"` and
   reported 131 occurrences — most of the store's rows already read `| auto | proposed |`, so the
   blind replace promoted *other* entries and left the mutation's claim vacuous. Repaired by mutating
   the canonical row **by identity** (the line beginning `| 不言自明 (Self-explanatory) |`) and
   asserting that exactly that row — and no other — changed. The corrected leg is what proves
   `C-33-a`.
2. **The leg read the real store instead of its copy.** `load_module()` overrode `mod.STORE`, but the
   assertion path shells out to the engine with `--root ROOT`, so the engine kept reading the real
   repository's store and reported `proposed` on a "promoted" copy (`C-33-m` red while `C-33-a` was
   green-vacuous). Repaired by also deriving the copy tree's root (`root_of()`) and overriding
   `mod.ROOT`; the engine then honestly reported `confirmed` for the promoted copy.

Both were found by running the leg, not by review; neither weakens a guard — the controls still prove
the assertions are green on the untouched copy and red on the mutated one.

## Out of scope, verified not done

- **T048+ not started**: no mirror-total table check, no `regen-command-copies` check, no
  generate-instructions BUDGET re-run, no gate-total re-scan, no Feature index sync, no red-flag
  evidence wrap-up (T051), no `validate-tasks` Completion Gate.
- **T053 not started** (C-34's guard is P10 by the part plan); T047's variant scan is a measurement
  line in a note, **not** the C-34 assertion.
- No plan-owned artifact touched: `requirements.md`, `plan.md`, `data-model.md`, `contracts/`,
  `quickstart.md`, `research.md`, `feature-ref.md` unmodified (`PLAN-EDIT: none`).
- No Completion Gate, no Feature status flip, no implement Feedback / Wrap-up, no push.
- The glossary store is byte-identical (`21482f64…`), asserted independently inside the red-leg driver
  and re-checked with `git diff --stat .specify/memory/glossary.md` (empty) before commit.
