# Full-Run Baseline Measurement — 2026-10-22

Dated record for 067 User Story 5 (FR-012 / SC-006 / SC-008). This is the pre-change baseline, not a passing run.

## Measurement

- **Command**: `bash scripts/bash/run-tests.sh -q --durations=50`
- **Host**: macOS arm64 (Darwin 25.6.0), Python 3.14.6, pytest 9.1.1
- **Started**: 2026-10-22T06:16Z (14:16 local) · **Finished**: 2026-10-22T06:29Z
- **Exit code**: 1
- **Wall clock (wrapper epoch delta)**: 750 s
- **pytest reported time**: 748.56 s (0:12:28)
- **Counts**: 83 failed, 4467 passed, 1 skipped, 4 warnings
- **Collected node ids**: 4553 (contract 3428 / unit 734 / integration 391)

## Evidence pointers

- Complete stdout/stderr: `notes/baseline-full-2026-10-22.log` (machine-local; `*.log` is gitignored, 138 KB)
- Failure name list (83, sorted): `test-evidence/baseline-failures-2026-10-22.txt`
- Slowest 50 durations: `test-evidence/baseline-durations-2026-10-22.txt`

## Concentration

- Slowest 50 tests account for **298.2 s** (≈40% of the 750 s wall clock).
- `tests/unit/test_admission_check.py`: 18 of the slowest 50 (each roughly 3–8 s).
- `tests/integration/test_worktree_integration_queue.py`: 6.
- `tests/contract/test_proactive_trigger_section.py`: 4.
- `tests/integration/test_trigger_telemetry.py`: 3.
- `tests/contract/test_workspace_isolation_contract.py`: 3.

## Baseline failure set

- 83 names; 50 contain a mirror/parity/sync/drift/distribution marker.
- Remaining 33 are gate-total pins, exec-quant cases, and three `tests/unit/test_loop_state_engine.py` cases.
- Per the clarify ruling (`requirements.md` § Clarifications, 2026-10-22), SC-008 "green" is measured **relative to this failure set**: no new name-level failures, and pinned drift tests must not newly appear in it.

## Use

- Pre-change side of SC-006 (≤600 s) and SC-008 (no new failures).
- Not a passing run; do not cite as green. The post-change measurement must use the fixed cold-cache protocol in `test-evidence/measurement-protocol-2026-10-22.md`.
