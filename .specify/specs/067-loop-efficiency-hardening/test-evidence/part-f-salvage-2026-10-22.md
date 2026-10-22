# Part F Salvage Record — 2026-10-22

Dated record of the implement part F (T025–T029) budget exhaustion and the driver-side salvage.

## What happened

- The part F subagent reached its 120-turn budget after:
  - committing `bc5c443a` — Class 2 triage (stale pins, test-local isolation, 6 dated debt records; 9 test files touched, no test deleted);
  - writing `test-evidence/injection-drill-2026-10-22.md` (FB-08/FB-09 drill: hit / localize / reproduce / restore all passed; suite 723 passed after restore);
  - but before adding the 33 Class 2 rows to the triage table, marking T025–T029, and committing the drill evidence.
- Its last output was “清理完毕 — 没有注入残留。正在提交 1：” — no anomaly, budget-exhausted only.

## Driver salvage

- Independently reran all 33 Class 2 node ids from `class2-set-2026-10-22.txt`:
  `33 tests → 19 passed, 14 failed in 7.36s`.
- The 14 failures are exactly the debt-registered groups and all are in the T007 in-stage baseline (pre-existing, not introduced by 067):
  - clause-forms archive (1); SC-002 cap breach (2); exec-quant darwin `/proc` (7); gate-budget re-freeze (2); shipped-surface 065 refs (1); cd5 heading collision (1).
- Added the 33 individual rows to `failure-triage-2026-10-22.md` with dispositions:
  - 10 `pin-updated+rationale` (owner facts moved pre-067; equality strength kept; `bc5c443a`);
  - 5 `mechanism-fixed` (test-local isolation; assertions unchanged; `bc5c443a`);
  - 4 `synced` (mirror sync `1d40ebeb`, green in the Class 2 rerun);
  - 14 `debt-registered` (dated debt records, pre-existing).
- Verified V-E5-1: the triage table now has 83 unique original ids — exactly the T007 in-stage baseline set, 0 missing.
- Injection drill evidence committed with this record; `tests/contract/test_mirror_parity_suite.py` is byte-identical to the committed state (suite 723 passed; no injection residue).

## Budget accounting

- Part F: 1 dispatch, 120 turns, budget-exhausted; salvaged in-session without a second full dispatch.
- No full-suite run in part F (T034 owns the closure slot).
- The post-067 suite is green in the mirror-parity suite; the 14 debt failures remain known baseline names, so the closure name-level diff can still be 0 NEW.

## Residual risks

- The 14 debt failures are real pre-existing reds; SC-008 accepts them only because they are in the T007 baseline. They are not claimed green.
- If the closure run exposes a new failure outside these names, it must be fixed or explicitly attributed before merge.
