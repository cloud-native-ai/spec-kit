# Implement part 8 — T039-T043 (US4: the glossary entry, and the mirror enumeration it rides on)

- **stage**: implement
- **part**: 8/10
- **part_scope**: `T039-T043`
- **stage_base**: `35a2948b`
- **test_budget**: targeted-set-v1 (E2's single full suite from part 1 stands unchanged: 26 failed /
  7156 passed / 1 skipped; no second full suite is run here)
- **docs-only**: no — one new contract module plus the red-leg driver; no non-test source file is
  edited and the glossary store is byte-identical before and after

## E3 stage-status row (implement part 8)

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T039-T043 |
| status | us4-glossary-entry-guarded-and-mirror-enumeration-proven |
| command | `python3 -m pytest tests/contract/test_self_explanatory_glossary.py -q` then `python3 -m pytest tests/contract/test_glossary_mechanism.py -q` then `python3 -m pytest tests/contract/test_mirror_parity_suite.py -q -k 'self-explanatory or best-practice-optimization'` then `python3 .specify/.tmp/082-part8/red_legs.py` |
| selection_basis | targeted-set-v1 — exactly the surfaces this part writes or asserts on: the new glossary module (T039-T042 all land in it), the mechanism suite it must not disturb (C-31, and T045 re-checks its diff is empty), and the parametrized parity suite whose nodes are derived from the very `MIRROR_PAIRS` table T042 asserts on. The glossary store itself has no other carrier |
| selected_paths | `tests/contract/test_self_explanatory_glossary.py` (new), `tests/contract/test_glossary_mechanism.py` (read-only, must stay green and unmodified), `tests/contract/test_mirror_parity_suite.py` (read-only, subset), `scripts/python/glossary-utils.py` (read-only, import-loaded and invoked), `scripts/python/sync-mirrors.py` (read-only, import-loaded), `.specify/memory/glossary.md` (read-only in effect — the engine's write is idempotent) |
| sufficiency | the three suites are the complete set of automated judges for this part's surfaces: the new module carries every clause T039-T042 claim (C-29, C-30, C-32, C-22/C-24), the mechanism suite is the mechanism guard C-31 names, and the parity subset is the carrier C-22's parameter claim depends on. Sufficiency is claimed for **the edit set**; the full-suite verdict belongs to the Completion Gate, which this part does not run |
| rc | 0 (new module), 0 (mechanism suite), 0 (parity subset), 0 (red-leg driver) |
| passed / failed | 8 passed / 0 failed (new module); 12 passed / 0 failed (mechanism suite); 3 passed / 759 deselected (parity subset); 10 PASS / 0 FAIL (red-leg driver) |
| new_failures | none in the selected set |
| baseline | `.specify/specs/082-self-explanatory-integration/baseline-failed.txt` (26 entries) — no entry in the selected set appears there (0 matches for `glossary`, `self_explanatory`, `mirror_parity`), so no comparison was triggered |
| evidence_ptr | `notes/red-first-evidence.md` § Part 8 (M-1…M-5 verbatim, the idempotent-write transcript, the closed pair table) |

### Command output, verbatim

```console
$ python3 -m pytest tests/contract/test_self_explanatory_glossary.py -q
........                                                                 [100%]
8 passed in 0.08s
EXIT=0

$ python3 -m pytest tests/contract/test_glossary_mechanism.py -q
............                                                             [100%]
12 passed in 0.16s
EXIT=0

$ python3 -m pytest tests/contract/test_mirror_parity_suite.py -q \
      -k 'self-explanatory or best-practice-optimization'
...                                                                      [100%]
3 passed, 759 deselected in 0.08s
EXIT=0

$ python3 .specify/.tmp/082-part8/red_legs.py
[PASS] control: test_c29_entry_exists_with_origin_auto_and_status_proposed is green on the control
[PASS] control: test_c30_no_second_row_carries_the_retired_name_or_canonical_as_canonical is green on the control
[PASS] control: test_c32_meaning_cell_names_an_existing_repository_relative_path is green on the control
[PASS] M-1: test_c30_… is RED — a second row puts the retired name or the canonical string in the
        canonical column: [(161, '望文生义')] (the canonical row is entry index 160)
[PASS] M-2: test_c29_… is RED — expected exactly one entry whose canonical cell is
        '不言自明 (Self-explanatory)', found 2
[PASS] M-2: test_c30_… is RED — same mutation, the row-index assertion fires
[PASS] M-3: test_c32_… is RED — the meaning cell does not name the concept owner
[PASS] M-4: C-22 parameter-presence is RED with the engine enumeration emptied
[PASS] M-5: C-22 byte-identity is RED when the mirrored copy differs — mirror drift:
        shared/workflow/best-practice-optimization.md->.specify/shared/workflow/best-practice-optimization.md
[PASS] isolation: real store sha256 unchanged
VERDICT: PASS — 10 PASS / 0 FAIL
EXIT=0
```

### Companion reading — the store's own engine

```console
$ python3 scripts/python/glossary-utils.py --action detect-conflict \
      --canonical "不言自明 (Self-explanatory)" --variants "望文生义"
{
  "conflict": true,
  "kind": "same-term-diff-meaning",
  "collidesWith": [
    "不言自明 (Self-explanatory)"
  ]
}
EXIT=0

$ python3 scripts/python/glossary-utils.py --action validate
{
  "valid": true,
  "path": "/storage/project/cloud-native-ai/spec-kit/.specify/memory/glossary.md"
}
EXIT=0

$ git diff --stat .specify/memory/glossary.md tests/contract/test_glossary_mechanism.py
(empty)
```

## What each row actually asserted (closure record)

| Row | Clause | Where the assertion lives | State after this part |
|-----|--------|---------------------------|-----------------------|
| T039 | C-29 | `test_c29_entry_exists_with_origin_auto_and_status_proposed`: the table's engine-parsed entries contain **exactly one** row whose canonical cell is `STR-003` verbatim, and that row's `origin` is `auto`, `status` is `proposed`, variants are exactly the retired name | green, 8 passed |
| T040 | C-30 | two assertions: no other row carries the retired name **or** the canonical string in its canonical column (compared by entry index, never by substring), and the engine's `--action validate` exits 0 with `valid: true` | green |
| T041 | C-32 | `test_c32_…`: the canonical row's meaning cell names `shared/definitions/self-explanatory-definitions.md`, **and** every repository-relative path the cell contains resolves to an existing file | green |
| T042 | C-22 / C-24 (+ C-26 co-claim) | `test_c22_new_document_is_enumerated_by_the_engine`, parametrized over the three documents: exactly one `MIRROR_PAIRS` row owns the document by path prefix, the engine's `iter_files` yields it (so the parity suite derives a node), the mirror file exists, and source and mirror are byte-identical — the C-24 failure message names the `source->mirror` pair | green, 3 passed in-module / 3 passed in the suite |
| T043 | C-31 (write) | the entry was registered **through the engine**: `detect-conflict` first (it collides with itself, because the term is already present), then `--action add`, which replaces in place and leaves the file byte-identical (`21482f64…` before and after, 161 entries, empty `git diff`) | green — no hand edit, no second row |

## Two in-passing repairs (corrections, disclosed)

1. **An invented pair id.** T042's first draft derived the expected engine id as
   `dirname(source)->dirname(mirror)`, which for `shared/definitions/x.md` produces the id
   `shared/definitions->.specify/shared/definitions` — a pair the engine never declares. All three
   parameters went red on a repository that is in fact fully covered. Repaired by matching the
   **engine's own vocabulary**: a `MIRROR_PAIRS` row owns the document when `source` is under
   `src_name` and `mirror` is under `dst_name`; the row must be unique, and the derived mirror path
   is then asserted equal to the contract's pair. The assertions were green afterwards without any
   change to the engine or the mirrors.
2. **A red leg that did not reach its own assertion.** The M-5 driver copied the two sides into
   directories whose names were not siblings, so the leg stopped at the enumeration assertion and
   never reached the byte comparison. Repaired by placing both copies under a single root; the leg
   now fails with the drift message naming the pair, which is the assertion C-22/C-24 own.

Both were found by running the code, not by review. Neither weakens a guard: the five mutation legs
and three controls still go red/green on their own subjects.

## Adjacent finding, recorded rather than acted on

`glossary-utils.py` natively replaces an existing entry of the same canonical, so the same write
re-runs without a second row. `detect-conflict` does **not** exclude the existing entry from its own
sweep, so an already-present term reports `conflict: true, kind: same-term-diff-meaning` colliding
with itself. `action_add` does exclude it — which is why the write succeeded — so the engine's two
verbs read the same input differently. This part leaves both behaviours untouched (no engine edit is
in this part's scope, and neither behaviour produced a defect here) and records the reading in the
red-first evidence. Whether `detect-conflict` should suppress the self-collision is a decision for the
engine's owner, not for this feature.

## Out of scope, verified not done

- T044+ not started: no status-persistence note, no unchanged-suite verification row, no
  `/speckit.improve` wiring check, no name-consistency final sweep (C-34 / T053), no mirror-total
  check, no Feature index sync.
- No non-test artifact edited outside `notes/red-first-evidence.md` and this file.
- No plan-owned artifact touched: `requirements.md`, `plan.md`, `data-model.md`, `contracts/`,
  `quickstart.md`, `research.md`, `feature-ref.md` unmodified (`PLAN-EDIT: none`).
- No Completion Gate, no Feature status flip, no implement Feedback / Wrap-up, no push.
