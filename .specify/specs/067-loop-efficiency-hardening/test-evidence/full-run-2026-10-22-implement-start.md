# Full-Run Measurement — 2026-10-22 implement-start slot (E1)

**Slot**: implement-start baseline (063 TB-03) · **Purpose**: process measurement after T001–T006; not the SC-006 closure claim.

## E1 fields

| Field | Value |
|---|---|
| command | `bash scripts/bash/run-tests.sh -q --durations=50 --names-out .specify/specs/067-loop-efficiency-hardening/test-evidence/baseline-failures-2026-10-22-implement-start.txt` |
| command core (MP-02) | `bash scripts/bash/run-tests.sh -q --durations=50` — identical pytest-facing flags; `--names-out` is the runner-level reporting extension mandated by TB-03 and does not change what pytest executes |
| host | macOS arm64 (macOS 26.6.2 / Darwin 25.6.0), runner-resolved Python 3.14.6 + pytest 9.1.1 |
| date | 2026-10-22 |
| git_commit | `fe5f1e62` (working tree clean at start) |
| cache_clear | `rm -rf .pytest_cache` + `find tests src -type d -name __pycache__ -prune -exec rm -rf {} +`, immediately before the run at start epoch 1792654770 |
| start_epoch / end_epoch | 1792654770 / 1792655304 |
| wall_seconds | **534** (budget number, epoch delta) |
| exit_code | 1 (83 pre-existing failures) |
| layer_counts | contract: 3346 passed / 80 failed / 0 skipped; unit: 733 passed / 3 failed / 0 skipped; integration: 390 passed / 0 failed / 1 skipped |
| pytest_summary | `83 failed, 4469 passed, 1 skipped, 4 warnings in 532.39s (0:08:52)` |
| evidence_log | `.specify/specs/067-loop-efficiency-hardening/notes/full-run-2026-10-22-implement-start.log` (machine-local; `*.log` gitignored) |
| failed_names_path | `.specify/specs/067-loop-efficiency-hardening/test-evidence/baseline-failures-2026-10-22-implement-start.txt` (83 entries) |
| baseline_pointer | `.specify/specs/067-loop-efficiency-hardening/test-evidence/baseline-full-2026-10-22.md` |
| validity | single runner invocation; no path / `-k` / `-m` filters; three layers executed; collection and fixtures included; 0 deselected (MP-05) |

## Result

- Pre-change baseline: 750 s wall / 748.56 s pytest, 83 failed / 4467 passed / 1 skipped.
- Implement-start: **534 s wall / 532.39 s pytest**, 83 failed / 4469 passed / 1 skipped.
- Delta: **−216 s (−28.8%)**; the +2 passed are the new admission sibling parameter rows (T005).
- Name-level diff vs the pre-stage baseline: **0 NEW, 0 FIXED** — the same 83 names (RC-07 introduced no suite-wide regression).
- Slowest calls after the change: watch-target self-test 28.13 s (fixed cost outside the delivery surface), session-kill reattach 8.79 s, instructions-size idempotent 8.53 s, worktree merge+replay 6.53 s (was 27.13 s).

## Boundary

- This is an implement-start process record. SC-006 (≤600 s on the post-change tree) is claimed only from the closure slot after review, per MP-08.
- The 83 failures are pre-existing debt; the failure set is unchanged and is the in-stage baseline for the closure name-level diff.
- No test is claimed green beyond what the actual run reported; the exit code is 1.
