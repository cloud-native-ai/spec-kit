# Implement part 7 — T034-T038 (US3: the pointer page, its links, and two mutation legs)

- **stage**: implement
- **part**: 7/10
- **part_scope**: `T034-T038`
- **stage_base**: `e5d0ae87`
- **test_budget**: targeted-set-v1 (E2's single full suite from part 1 stands unchanged: 26 failed /
  7156 passed / 1 skipped; no second full suite is run here)
- **docs-only**: no — one test module gains the C-27 clause, one page gains a two-line note, and the
  notes carry both mutation legs

## E3 stage-status row (implement part 7)

| field | value |
|-------|-------|
| stage | implement |
| part_scope | T034-T038 |
| status | us3-docs-links-green-and-both-mutation-legs-proven |
| command | `python3 -m pytest tests/contract/test_self_explanatory_distribution.py -q` then `python3 scripts/python/sync-mirrors.py --check` then `python3 .specify/.tmp/082-part7/m56.py` |
| selection_basis | targeted-set-v1 — exactly the surfaces this part touches or asserts on: the distribution module (T034 writes C-27 into it, T038 mutates its extractor) and the mirror engine (T037 exercises its `compare_pair` and its `--check` enumerates the pairs C-27 resolves through). The docs page itself has no other carrier; the mirror parity suite is the companion set below |
| selected_paths | `tests/contract/test_self_explanatory_distribution.py` (edited, C-27 + M-6 leg), `docs/concepts/self-explanatory.md` (T035's two-line note), `scripts/python/sync-mirrors.py` (read-only, invoked), `shared/definitions/self-explanatory-definitions.md` \+ `.specify/shared/...` (read-only, the M-5 subject copy source) |
| sufficiency | the module and the engine are the only two guards that judge this part's surfaces. The page is prose with no runtime; C-27 is its only automated judgement, and it now has four assertions (floor, resolution, anti-vacuity, no-owner-body) plus the M-6 leg. The parity suite is the companion set below because the C-27 mirror half resolves through the same `MIRROR_PAIRS` the suite enumerates. Sufficiency is claimed for **the edit set**; the full-suite verdict belongs to the Completion Gate, which this part does not run |
| rc | 0 (module), 0 (engine `--check`), 0 (M-5/M-6 driver) |
| passed / failed | 9 passed / 0 failed in the distribution module (4 inherited + 5 new); 6 `ok` pairs from the engine; 13 PASS / 0 FAIL in the mutation driver |
| new_failures | none in the selected set |
| baseline | `.specify/specs/082-self-explanatory-integration/baseline-failed.txt` (26 entries) — no comparison triggered, since nothing in the selected set is a baseline failure |
| evidence_ptr | `notes/pre-change-measurements.md` § Part 7 (T035 review table, C-27 measurements, closed legs), `notes/quickstart-run.md` § Part 7 (T036-a/T036-b probes), `notes/red-first-evidence.md` § Part 7 (M-5/M-6 verbatim + the new R-5 pair) |

### Command output, verbatim

```console
$ python3 -m pytest tests/contract/test_self_explanatory_distribution.py -q
.........                                                                [100%]
9 passed in 6.94s
EXIT=0

$ python3 scripts/python/sync-mirrors.py --check
OK: all per-tool command copies match the source templates.
ok    templates/ == .specify/templates/ (22 files)
ok    skills/external/ == .specify/skills/ (409 files)
ok    skills/internal/ == .specify/skills/internal/ (138 files)
ok    agents/ == .specify/agents/templates/ (3 files)
ok    scripts/ == .specify/scripts/ (119 files)
ok    shared/ == .specify/shared/ (65 files)
EXIT=0

$ python3 .specify/.tmp/082-part7/m56.py
… 13 × [PASS] …
VERDICT: PASS — M-5 turns C-22's byte-identity assertion red on a copy; M-6 turns C-27's
         resolution assertion red on a copy; both real subjects are byte-identical after
         the legs.
EXIT=0
```

### Companion set — the parity suite still derives its parameters, unchanged

`test_mirror_parity_suite.py` is unedited by this part; it is listed because C-27's mirror half reads
the same `MIRROR_PAIRS` it enumerates, so a drift there would break both faces at once. Part 6 recorded
the 3 matching node ids (766 passed); this part re-ran it and it is unchanged.

```console
$ python3 -m pytest tests/contract/test_mirror_parity_suite.py -q \
      -k "self_explanatory or self-explanatory or best-practice-optimization"
3 passed, 759 deselected in 0.09s
EXIT=0
```

## What each row actually asserted (closure record)

| Row | Clause | Where the assertion lives | State after this part |
|-----|--------|---------------------------|-----------------------|
| T034 | C-27 | `tests/contract/test_self_explanatory_distribution.py`: four assertions — the required floor paths are named, every inline `.md` path resolves in source **and** in its engine-derived mirror, the extractor is anti-vacuous over synthetic text, and the page carries none of the owner's `## ` headings. `C27_MIRROR_EXEMPTIONS` is empty **by measurement** (all three pointers live under `shared/`), and a path outside every engine pair fails loudly rather than passing | green, 9 passed |
| T035 | C-28 face | read-only review; the measured page carried the retirement fact but not the variant fact, so the one permitted addition (a two-line `## Naming history` note) was made. No owner text copied (0 of 13 page sentences >24 chars appear in the owner; 0 owner headings) | green — page 1993 B → 2111 B, still a pointer page |
| T036 | C-28 face | `notes/quickstart-run.md` § Part 7: the ambient probe (landing dir present, three documents absent, 59 files) plus its measured cause (installed CLI built from `26731b67`, 271 commits behind), and the alternative reading (`pip install -e` → all three present, 65 files) | green — both readings transcribed |
| T037 | C-24 | M-5 on a copied mirror tree: one byte flipped → `compare_pair` returns the differing pair → the parity suite's byte-identity assertion raises naming `source->mirror`; real pair sha256 unchanged | green — leg PASS, isolation asserted |
| T038 | C-28 face / C-27 | M-6 on a copied page: `STR-002` pointer deleted → extraction loses it → `unresolved_docs_page_paths` reports the mutated path → the guard's own `assert not problems` goes red; real page and all of `docs/concepts/` digest-identical | green — leg PASS |

## The docs `db`-link decision, stated rather than hidden

C-27's contract text requires that a path with no mirror be "asserted in the source tree only, and the
exclusion … written in the guard as an explicit allow-list with a one-line reason". The allow-list is
`C27_MIRROR_EXEMPTIONS`, it carries a written one-line reason template, and it is **empty** because the
page names no docs-internal path. Writing speculative entries would have added a second truth about
which paths may skip the mirror check; leaving it empty keeps the guard's surface equal to its subject.
The exempt case is still decidable: `unresolved_docs_page_paths` reports *"belongs to no mirror pair,
and it is not in C27_MIRROR_EXEMPTIONS"* for any extracted path outside the engine's source dirs, so the
first docs-internal link that lands fails the guard and forces an explicit entry.

## In-passing repairs (corrections, disclosed)

1. **The anti-vacuity sample named a real file.** The synthetic text in
   `test_c27_extraction_is_not_vacuous` first used `docs/concepts/some-other-page.md`, which exists
   (measured: the test failed with `1 == 2` because that path resolves). Repaired by naming a path
   that cannot exist (`shared/definitions/absent-by-construction.md`), so the assertion measures the
   extractor rather than the repository's contents.
2. **A wrong expectation inside the same test, found by running it.** After the repair above the test
   still expected *both* synthetic paths to be reported; only one is absent (the other is the real
   owner path). Corrected to assert exactly one problem, which is the stronger statement: the guard
   must report the absent pointer **and not** a resolving one.

Both were found by the test failing, not by review. Neither weakens a guard: the M-6 leg and the four
C-27 assertions still go red on their own subjects.

## Out of scope, verified not done

- T039+ not started: no glossary rows (US4), no name-consistency sweep, no mirror-total check, no
  Feature index sync.
- No plan-owned artifact touched: `requirements.md`, `plan.md`, `data-model.md`, `contracts/`,
  `quickstart.md`, `research.md`, `feature-ref.md` unmodified (`PLAN-EDIT: none`).
- No Completion Gate, no Feature status flip, no implement Feedback / Wrap-up, no push.
