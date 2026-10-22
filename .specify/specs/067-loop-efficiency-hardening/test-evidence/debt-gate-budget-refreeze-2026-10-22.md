# Debt — gate-budget re-freeze required (G-9 / GN-C11) — 2026-10-22

**Status**: registered (FB-06). **Not introduced by this scope** (067-loop-efficiency-hardening).

## Failing pinned tests

- `tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline`
- `tests/contract/test_proactive_trigger_section.py::test_c11_gate_scan_total_unchanged`

## Failure shape

Both pins compare the live `scan-confirmation-gates.py` total against the frozen value in
`.specify/specs/050-proactive-flow-trigger/baseline-gates.json` (`confirmationGates.total = 23`).
Live total is 27 (destructive 20 / governance-kept 7, violations 0).

## Why not repaired here

1. The expected value lives in a **budget-freeze artifact of feature 050**, outside this part's
   write surface. Re-freezing it is exactly what the framework's own guard forbids in passing:
   `test_g11_pins_and_baselines_not_modified` pins `frozenAt == 2026-09-08` and
   `(23, 13, 10)` — "re-freezing disguises a breach as the new normal". The budget owner must
   re-adjudicate first (the pin's own failure message states this).
2. The movement **predates this scope**: the scanner already reports 27 at the 067 branch point
   `7f9033ec` (verified by running the scanner in a throwaway worktree at that commit, 2026-10-22);
   the last contributing change is `7e738423` (2026-10-20, feature 063), an ancestor of the branch
   point. Evidence: triage rows for the two names.

## Repair path (owned elsewhere)

Budget-owner adjudication: re-freeze `050-proactive-flow-trigger/baseline-gates.json` through the
owning feature's flow together with every pin keyed on it (`test_g9`, `test_c11`, `test_g10`
row-two source pin, `test_g11` freeze pin), or reduce the blocking-gate wording in the scanned
surface. Neither is a 067 implement-part F action.
