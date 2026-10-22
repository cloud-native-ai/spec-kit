# W2 Admission Family Timing — before/after — 2026-10-22

**Tasks**: T004 + T005 + T006 (implement part A) · **Target file**: `tests/unit/test_admission_check.py`
**Engine under test**: `skills/external/sdd-loop-driver/scripts/admission-check.py` (unchanged — 禁改面 respected)

## Commands actually run (targeted only; no full suite)

| # | command | when |
|---|---|---|
| R1 | `bash scripts/bash/run-tests.sh tests/unit/test_admission_check.py -q --durations=0` | pre-change (before T003 fixture), tree ≈ `a8a097b6` |
| R2 | same | post-RC-07 (conftest fixture only), `47a52cc9^` |
| R3 | same | post-T004/T005 (in-process + template clone), `f14c4f49` |

## Results

| metric | R1 (red) | R2 (RC-07 only) | R3 (final) |
|---|---|---|---|
| pytest family time | 121.33 s | 31.71 s | **27.69 s** |
| call-duration sum (all entries ≥5 ms) | 121.06 s | 31.05 s | **23.03 s** |
| wrapper wall clock | 122 s | 33 s | 28 s |
| passed / failed | 23 / 0 | 23 / 0 | **25 / 0** |
| slowest call | 12.22 s | 2.78 s | 2.32 s (`test_sensitive_or_engine_path_rejected`) |

## Band comparison (honest, both bases stated)

- **Anchor basis (the 87.45 s red anchor is a durations call-sum of the 18 baseline top-50
  admission calls)**: R3 call-duration sum = **23.03 s → inside the plan §W2 band 15–25 s**.
  On this anchor-comparable basis the family is GREEN (measured, not claimed: R3 above).
- **Session-total basis**: pytest reports 27.69 s — 2.69 s above the 25 s band edge. Attribution
  (plan §W2 assumption-table style): the difference (27.69 − 23.03 = 4.66 s) is non-call
  overhead absent from the baseline anchor's basis — pytest + collection startup, two
  module-scoped template builds (2× `git init` + 4 commits), 33 per-case `git clone`
  subprocesses, and per-case `rev-parse` calls. The largest single calls are now the
  intentionally-kept CLI subprocess pin (`test_exit_codes_0_1_2`, 1.94 s for 3 real
  interpreter cold starts) and the 3-variant sensitive-path case (2.32 s).
- No further optimization was applied within this part; the residual over-band share is
  overhead-only, documented, and not claimed as in-band.

## Behavior-equivalence check (T006 acceptance)

- ID-level diff (baseline list vs fresh collect of the file, `comm` both directions):
  **0 removed / 2 added** (`test_task_count_boundary_edges[30-10-True]`,
  `[7-9-False]` — T005 same-shape sibling rows). All 23 original ids survive byte-identically.
- CLI pin intact: `test_exit_codes_0_1_2` still runs 3 true `sys.executable` subprocess
  invocations and asserts exit codes 0 / 1 / 2 verbatim (plus the `--json-out` payload file).
- Per-test assertion audit: every original assertion preserved (only `_run` call shape and
  fixture wiring changed; two failure-diagnostics messages now cite `payload["reasons"]`
  instead of subprocess stderr — assertion subjects unchanged).
- Ledger: 23 `retained` rows (one per original id) appended in
  `test-evidence/test-consolidation-ledger.md`; the 2 new ids are LED-08 post-only
  additions (reportive, no ledger row required).
- Global-state isolation: `admission_engine` fixture re-executes the engine module per case
  (FR-016 explicit reset); engine module itself untouched.

## Raw outputs

- R1 full stdout: transcribed in `test-evidence/rc07-neutralization-2026-10-22.md` (pre column).
- R3: `25 passed in 27.69s`; 27 duration entries ≥5 ms, call sum 23.03 s; top-12 calls listed
  in the run record. Family file: 14 test functions / 25 collected ids
  (boundary 8 rows, manifest 5 rows after T005).
