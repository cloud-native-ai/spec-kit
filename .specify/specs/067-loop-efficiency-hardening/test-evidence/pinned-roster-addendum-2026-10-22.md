# Pinned Roster Addendum / W-1 Ruling — 2026-10-22

Dated record for the review waiver W-1 (`review.md` §4 P1-1). It binds the T036 pinned-roster check at closure.

## Why this addendum exists

`tasks.md` T036 and DoD-3 originally required `pinned roster (T002) ⊆ post id list` literally. The roster is a 302-id union built before the fold. T020–T022 folded 35 pure byte-identity functions into the shared 723-parameter mirror-parity suite, so their original node ids no longer exist in the post list; the literal subset check is mechanically impossible even though the protection is intact.

## Ruling (W-1)

For each roster id, the closure check accepts either:

1. the id appears in the post-test id list; or
2. the id's original function has a `case-merge` row in `test-consolidation-ledger.md` whose `retained_equivalent_id` is a suite parameter that appears in the post list and is green.

The check is executed as a deterministic ledger join (roster id → ledger row → suite param → post list/green), not as a literal subset. The join result and unmatched count are written into the T036 audit record with a reference to this ruling.

## Evidence that the protection is intact

- Review independently measured the 723-parameter suite: **723 passed**; the case-merge retained equivalents are 35/35 present and green (`review.md` §4; `w3-sync-2026-10-22.md`).
- The fold ledger has 35 case-merge rows and 46 retained rows; `deleted = 0` (review mechanical audit; `test-consolidation-ledger.md`).
- The 44 roster ids covered by the fold are the ones whose original functions are recorded in the ledger; the exact join is recomputed at T036, not trusted from this summary.
- Pin strength did not decrease: T019–T022 kept extra assertions in their own tests and the suite covers all engine pairs (ledger LED-07; review P1-1 evidence).

## Closure expectations

- The T007 in-stage baseline has 83 names. At review time 15 known reds were expected (14 `pre-existing-debt` + `test_i11` stale-pin); `test_i11` was fixed in `bc5c443a`, so the closure run showed **14** (all `pre-existing-debt`) and **0 NEW**. The known-red set is a subset of the T007 baseline; debt names must not be "fixed" during closure.
- Any roster id that is neither in the post list nor ledger-mapped to a green suite param is a real gap and blocks GATE-1.

## References

- `review.md` §4 P1-1 (W-1) and §Closure notes
- `test-evidence/test-consolidation-ledger.md`
- `test-evidence/pinned-roster-2026-10-22.txt` (302 unique ids)
- `tests/contract/test_mirror_parity_suite.py` (723 params)
