# P3 transient reds — disclosed, all owned by declared later tasks

- Date: 2026-11-25
- Package: implement P3 (T017–T024), run `r20261125T022857Z-06dd`
- Full fast tier: `1150 failed, 9089 passed, 4 skipped, 9 errors in 67.06s`
  (log `p3-final-run.txt`, names `p3-final-failed.txt`; P2 baseline names `p2-final-failed.txt`, 1145)
- Name-level delta vs P2: **5 new failure names, 0 repaired** (computed with
  `comm -13 <(sort p2-final-failed.txt) <(sort p3-final-failed.txt)`)

## The five new names and their attribution

| New failure | Class | Owner of the closure |
|---|---|---|
| `tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[scripts/python/skills-utils.py->.specify/scripts/python/skills-utils.py]` | source edited in T022, mirror not yet regenerated | T031 (`sync-mirrors.py --write`, the feature's single regeneration point) |
| `tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[templates/claudeignore-template->.specify/templates/claudeignore-template]` | source edited in T023, mirror not yet regenerated | T031 |
| `tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[templates/codexignore-template->.specify/templates/codexignore-template]` | source edited in T023, mirror not yet regenerated | T031 |
| `tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[templates/gitignore-specify-template->.specify/templates/gitignore-specify-template]` | source edited in T023, mirror not yet regenerated | T031 |
| `tests/integration/test_resource_id_resolution.py::test_resolution_fallback_when_id_missing` | live-target fixture: the test builds its discovery fixture under the retired `memory/tools/` home while T022 moved discovery to `.specify/tools/` | T029 (test live-reference classification per L-3) |

None of the five is an unrepaired subject defect: four are the declared "mirrors regenerate once, at
T031, after all source edits" sequencing, one is the declared US5 test-live-reference pass.

## Mirror drift member-set reading (`p3-sync-mirrors-check.txt`)

- `sync-mirrors.py --check` → rc 2, **457 DIFF**, 0 MISS / 0 ORPHAN (baseline `sync-mirrors-baseline.txt`: 450 DIFF).
- Member-set delta vs the baseline (the baseline file's last DIFF line has the
  `regen --check` OK line appended without a newline — a capture artifact, not a member):
  new members **7**, cured **0**:
  - `.specify/scripts/python/memory-utils.py`, `.specify/scripts/python/record-retention.py`,
    `.specify/scripts/python/renumber-utils.py` — P1 source edits (T004/T005) with the pre-105
    mirrors kept in place by design until T031;
  - `.specify/scripts/python/skills-utils.py`, `.specify/templates/claudeignore-template`,
    `.specify/templates/codexignore-template`, `.specify/templates/gitignore-specify-template` —
    this package's source edits (T022/T023), same declared sequencing.
- T031's convergence pass is the owner of restoring "no new drift members"; this package records the
  delta instead of hand-editing mirrors (A-12 / FR-022).

## Setup errors

The 9 setup errors are byte-identical to the P1-disclosed set (live-target fixtures owned by T029);
no new error name appears.
