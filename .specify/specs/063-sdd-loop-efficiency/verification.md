# Verification — Feature 063

Evidence class labels: **automated** (CI test), **recorded trace** (non-CI
recording), **driver closure** (owned by the driver after review).

## T002 — implement-start full-suite baseline (only slot consumed in implement)

- State spine: `/tmp/sdd-loop-efficiency/state.md` (`spine_write_mode=direct`)
- E2 ledger fence position: `<!-- test-budget:begin -->` line 1 (`seq=1`, `slot=baseline`)
- Command: `bash scripts/bash/run-tests.sh --names-out .specify/specs/063-sdd-loop-efficiency/notes/baseline-failed-tests.txt`
- Result: `68 failed, 4115 passed, 1 skipped, 4 warnings in 397.21s`; exit `1`
- Failed-name list: `notes/baseline-failed-tests.txt` (68 entries)
- Full log: `/tmp/t002-full-suite.log`
- Failure surface: all 68 are pre-existing mirror-drift / frozen-count contract
  failures; none is in `test_sdd_loop_driver_skill.py` or
  `test_sdd_loop_driver_cli_profiles.py`.
- `baseline_slot=consumed`; closure is driver-owned after review; implement ran
  no second full suite.
- E3 reference copy: `test-evidence/implement.jsonl` carries one legal row that
  references the E2 row; it is a transport/evidence copy, never the ledger.

## T001 — pre-change measurements and SC-010 baseline

- Measurements: `notes/pre-change-measurements.md` (+ raw outputs `notes/baseline-*.txt`)
- SC-010 baseline: `notes/stall-behavior-baseline.json`, `base_commit=a1aac7e5`,
  `initial_retries=0`, recorded before the first behavior-face commit; replay
  pre-check on the current tree: zero differences.
