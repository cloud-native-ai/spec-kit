# Debt — SC-002 cap breached by later legal gate growth — 2026-10-22

**Status**: registered (FB-06). **Not introduced by this scope** (067-loop-efficiency-hardening).

## Failing pinned tests

- `tests/contract/test_neutrality_budget.py::test_c5_the_cap_leaves_zero_integer_headroom`
- `tests/contract/test_confirmation_gates_sweep.py::test_residual_total_within_sc002_target`

## Failure shape

Both pin the SC-002 improvement target: residual blocking gates ≤ 25% of the frozen 044 baseline
(`.specify/specs/044-reduce-confirmation-flows/baseline.json`, total = 93 → cap 23.25, integer
headroom zero at 23). Live total is 27 > 23.25.

## Why not repaired here

1. The cap is a **target set by feature 044**, derived from a frozen dated baseline. The
   framework pins the derivation itself ("the derived cap and every pin keyed on it must be
   re-derived together, not adjusted to fit") and the freeze (`test_g11`-style anti-refreeze
   guards; the sweep's baseline is likewise pinned at 93). Lowering the target or re-freezing
   the baseline to pass would weaken the assertion — forbidden (FB-06/FB-07 discipline).
2. The breach **predates this scope**: 27 blocking gates already at branch point `7f9033ec`
   (scanner run in a throwaway worktree at that commit, 2026-10-22); the growth 23 → 27 came
   from pre-067 features (latest contributing change `7e738423`, 2026-10-20, feature 063).

## Repair path (owned elsewhere)

Either reduce blocking-pattern wording in the scanned surface back under the cap, or have the
044/SC-002 budget owner re-derive cap and every keyed pin together through its own flow.
