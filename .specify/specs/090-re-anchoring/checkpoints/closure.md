# Closure — 090-re-anchoring

## Terminal goal degree

| criterion | degree | evidence_ptr |
|---|---|---|
| SC-001 five surfaces present + pointer cross-references | 100% | verification.md SC-001_status=pass |
| SC-002 rules-first ordering pinned by a red-when-reversed test | 100% | verification.md SC-002_status=pass; ordering-red-control.txt |
| SC-003 count pins co-move; zero new failures vs the 49-name baseline | 100% | verification.md SC-003_status=pass; contract-baseline-comparison.txt |
| SC-004 T0/T1/T2 agree on both surfaces | 100% | verification.md SC-004_status=pass |

## Closure verdict

`closure-acceptance-check.py --spec-dir .specify/specs/090-re-anchoring --repo .` → **accept**; completion conditions: every_final_path_pass true (4/4), no_open_rows true (39 closed), status_row_per_criterion true.

## Archived team state

The spec-local temporary team (`team/090-re-anchoring/team.md`) is archived with the feature; its seats are reusable role templates, none instantiated.

## Disclosures

- The 090 line was developed directly on `master` after its pre-landed merge; the driver's U6 merge step is therefore a no-op and is recorded as such.
- Two pre-existing baseline failures (`test_i11…`, `test_g9…`) and one historical-face failure (`test_goal_migration::test_user_directive…`) are outside this feature's acceptance; the smoke record excludes the first two by node id and points at the baseline.
