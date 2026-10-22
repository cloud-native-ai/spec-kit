# Full-Run Measurement — 2026-10-22 closure slot (E1)

**Slot**: closure (063 TB-04) · **Purpose**: SC-006 / SC-008 final post-change measurement.

## E1 fields

| Field | Value |
|---|---|
| command | `bash scripts/bash/run-tests.sh -q --durations=50 --names-out .specify/specs/067-loop-efficiency-hardening/test-evidence/closure-failures-2026-10-22.txt` |
| command core (MP-02) | `bash scripts/bash/run-tests.sh -q --durations=50` — identical pytest-facing flags; `--names-out` is the runner-level reporting extension mandated by TB-04 and does not change what pytest executes |
| host | macOS arm64 (macOS 26.6.2 / Darwin 25.6.0), runner-resolved Python 3.14.6 + pytest 9.1.1 |
| date | 2026-10-22 |
| git_commit | `00287a38` (working tree clean at start) |
| cache_clear | `rm -rf .pytest_cache` + `find tests src -type d -name __pycache__ -prune -exec rm -rf {} +`, immediately before the run at start epoch 1792660505 |
| start_epoch / end_epoch | 1792660505 / 1792661058 |
| wall_seconds | **553** (budget number, epoch delta) |
| exit_code | 1 (14 pre-existing-debt failures; no new names) |
| layer_counts | contract: 4097 passed / 14 failed / 0 skipped; unit: 736 passed / 0 failed / 0 skipped; integration: 391 passed / 0 failed / 1 skipped |
| pytest_summary | `14 failed, 5224 passed, 1 skipped, 4 warnings in 550.62s (0:09:10)` |
| evidence_log | `.specify/specs/067-loop-efficiency-hardening/notes/full-run-2026-10-22-closure.log` (machine-local; `*.log` gitignored) |
| failed_names_path | `.specify/specs/067-loop-efficiency-hardening/test-evidence/closure-failures-2026-10-22.txt` (14 entries) |
| baseline_pointer | `.specify/specs/067-loop-efficiency-hardening/test-evidence/full-run-2026-10-22-implement-start.md` (T007 in-stage baseline, 83 names) |
| validity | single runner invocation; no path / `-k` / `-m` filters; three layers executed; collection and fixtures included; 0 deselected (MP-05) |

## Result — SC-006

- Closure wall **553 s ≤ 600 s** on the 2026-10-22 baseline host; pytest self-report 550.62 s.
- Improvement vs pre-stage baseline: 750 s → 553 s (−197 s, −26.3%); vs implement-start: 534 → 553 s (+19 s, variance; still within budget).
- Slowest call: watch-target self-test 25.95 s (fixed cost outside the delivery surface); the mirror suite (723 params) runs in ~1 s; admission family ~21 s total.

## Result — SC-008 / name-level

- `comm -13` vs the T007 in-stage baseline: **0 NEW**.
- 69 baseline names fixed (mirror sync + triage + suite consolidation).
- 14 remaining names are all pre-existing debt, each with a dated FB-06 record (`debt-*.md`); i11 was fixed in `bc5c443a`.
- No test was deleted to hide a failure; ledger has 0 `deleted` rows.

## Boundary

- This is the post-change closure record; the ≤600 s claim cites this record (MP-08).
- The 14 debt failures are not claimed green; they remain known baseline debt.
