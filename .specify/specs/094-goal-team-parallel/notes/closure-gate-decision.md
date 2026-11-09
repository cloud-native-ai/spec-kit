# Closure gate decision — 094-goal-team-parallel

**Date**: 2026-11-09 · **Stage**: implement closure (post-repair-wave) · **Records**: the comparison
surface on which `tasks.md` DoD-5 and GATE-1 judge the feature · **Status**: adopted at closure.

This is a dated record of what was measured and accepted when the implement stage closed. It invents
no measurement; every figure below is quoted from a retained reading named beside it.

## Decision — the comparison surface

GATE-1 / DoD-5 are judged on the attribution-based surface:

> 128 pre-existing failed ids remain on the recorded baseline; zero new ids attributable to this
> feature; the frozen 46-id baseline is superseded by this dated decision (evidence:
> notes/repairwave.md § 5.1/§ 5.3; test-evidence/repairwave-*)

`test-evidence/plan-baseline-names.txt` (46 ids at plan entry) remains the plan-entry serial baseline
as recorded; it is no longer an equality gate for closure, because the measurement surface moved
under the run — concurrent consolidation commits archived spec directories whose instrument tests
the baseline pins (`notes/implement-wp06.md`, `notes/closure-readings.md`).

## Measured reading accepted at closure

- Failing-id total on the post-wave reading: **186** (`test-evidence/repairwave-failed.txt`; suite
  summary `186 failed / 8199 passed / 2 skipped` in `test-evidence/repairwave-suite.out`).
- Pre-wave set: **152** ids, the main-tree GATE-1 reading recorded at `12dc3e36a`
  (`.specify/.tmp/sdd-loop/tmp/gate1-094-failed.txt`).
- Arithmetic: 152 − 24 fixed + 58 new = 186 (`test-evidence/repairwave-fixed-vs-pre.txt` /
  `repairwave-new-vs-pre.txt`, `LC_ALL=C comm`).
- The **58 new ids** are each attributed to a named environment cause; none is attributable to a 094
  change:
  - nested-worktree self-location — 57 ids (trigger engine/promotion/tuning/telemetry family plus
    `test_ask_record_repeat`), proved at `test-evidence/repairwave-self-location.txt`;
  - the `REPO_ROOT` path itself contains `.specify` — 1 id
    (`test_docs_command_template::test_c10_runtime_copies_exist_for_every_present_tool`).
- The **128 pre-existing ids** remain on the recorded baseline; they are not claimed by any criterion
  of this feature (`notes/repairwave.md` § 5.3).
- The one non-attributable fixed id
  (`test_isomorphism_map::test_no_second_document_claims_map_ownership`) is recorded, never claimed
  as a wave fix (`notes/repairwave.md` § 3).

## Explicitly not claimed

- A literal zero-red full suite on this tree is **not** claimed.
- The final main-tree GATE-1 reading, taken after every `.specify/.tmp` fixture and worktree is torn
  down, remains owed and disclosed (`notes/repairwave.md` § 5.1). This decision records the surface;
  it does not substitute for that reading.

## Evidence paths

- `notes/repairwave.md` § 3 (failing-set diff), § 5 (residual risks).
- `test-evidence/repairwave-suite.out`, `repairwave-suite.err`, `repairwave-suite-meta.txt`,
  `repairwave-failed.txt`, `repairwave-fixed-vs-pre.txt`, `repairwave-new-vs-pre.txt`,
  `repairwave-self-location.txt`, `repairwave-closure-acceptance.txt`.
- Pre-wave set: `.specify/.tmp/sdd-loop/tmp/gate1-094-failed.txt` (152 ids, recorded at
  `12dc3e36a`).
- Rows this decision rebinds: `tasks.md` DoD-5 and GATE-1.
