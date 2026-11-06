# Red-first evidence (Feature 086)

This note closes WP-A4's T005 observation gap (`notes/red-first-evidence.md`).

## Runner contract (WP-A1 / WP-A4)

- WP-A1 wrote the first 23 cases: before the runner change the red leg was **16 failed / 5 passed**;
  after the change **23 passed**.
- WP-A4 appended 15 cases: the file now collects **38** cases and the targeted run is **38 passed**.
- Mutation legs M-1…M-7 were exercised against temporary copies; M-5/M-6 were initially
  non-discriminating and were repaired before the final run.

## Budget ledger parser (WP-A2)

- `tests/unit/test_audit_test_budget.py` → **32 passed**; M-8 (revert both flag sets) and M-9 (drop
  `-n` from the attached matcher) each turn their case red.
- `--dist=loadfile` under M-8 stays green because the pre-change parser already dropped any unknown
  `-x=value` token; the separated forms and `-n4` are the discriminating cases.

## Principle / count pins (WP-B3)

- The B2 landing left six stale literal pins; WP-B3 raises them and the targeted set over the five
  files is **153 passed / 1 failed** — the single failure is
  `test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline`, which is in the T050
  pre-change baseline (frozen 23 vs live 27, the disclosed EP-008 drift), not this feature's.
- The new `tests/contract/test_test_execution_efficiency.py` carries the six-surface title/pointer
  guard plus six in-memory mutation legs.

## Baseline / closure references

- T050 pre-change serial baseline: **7475 passed / 19 failed / 7 skipped / 687.41 s**,
  `test-evidence/baseline-failed.txt` (19 names).
- T047 final closure: pending (WP-C2), compared against the T050 names; the final default-parallel
  run must have zero new failure names after the declared serial exception.
