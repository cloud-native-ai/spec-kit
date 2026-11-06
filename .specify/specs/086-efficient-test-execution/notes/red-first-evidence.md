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
- T047 final closure: **7535 passed / 19 failed / 7 skipped / 284.12 s** plus the serial exception
  pass **1 passed / 7561 deselected / 35.22 s**, `test-evidence/final-failed.txt` (19 names). Both
  `comm` directions against the T050 names are empty — zero new failure names after the declared
  serial exception. Full record: `test-evidence/closure-diff.txt`.

## Mutation leg closure (DoD-2)

All 19 legs M-1…M-19 now have a recorded observation. The readings live in three evidence files:

- `notes/red-first-evidence.md` (this file) — M-1, M-5, M-6, M-7 summaries.
- `test-evidence/mutation-legs-runner.txt` — M-2, M-3, M-4, and M-10…M-15. M-2/M-3/M-4 run the named
  contract cases against doctored runner copies; M-10…M-13 are covered by the parametric six-surface
  case, which also asserts it never writes to a tracked file; M-14/M-15 are read directly
  (byte-identical regeneration of the live instructions; an equality version pin).
- `test-evidence/ledger-parallel-flags.txt` — M-8, M-9.
- `test-evidence/serial-exceptions.txt` — M-17, M-19.
- `test-evidence/parallel-safety-attribution.md` — M-16, M-18.

**Correction recorded honestly**: the `tasks.md` carrier map pointed M-8/M-9 at
`test-evidence/ledger-parallel-flags.txt`, which did not exist when this note was first written; and
M-2/M-3/M-4/M-10…M-15 had carrier tasks but no recorded reading. Both gaps were closed at the
implement closure by producing the evidence, not by weakening the carriers. No tracked source, test or
runner file was edited to obtain any leg.

