# Analyze Findings Remediation — 2026-10-22

Dated record. Input: `test-evidence/analyze-findings-2026-10-22.md` (VERDICT: GREEN; 0 CRITICAL / 0 HIGH / 3 MEDIUM / 8 LOW). This record dispositions the MEDIUM items before implement; LOW items are either fixed or explicitly carried.

## M-1 · TB slot ledger gap → resolved by ruling

**Finding**: the pre-stage 750 s run was not booked in the 063 test-budget fence, and T007 (the implement-start slot) originally ran after T003–T006; TB-03's `--names-out` capture was omitted.

**Ruling**: the pre-stage 750 s run is a diagnostic baseline outside implement and does not consume a slot. T007 is the implement-start slot and MUST use `--names-out` to capture `test-evidence/baseline-failures-<date>-implement-start.txt`; T034 is the closure slot. Implement contains exactly two full runs. Closure name-level diff uses the T007 in-stage list as authoritative; the pre-stage 83-name list remains the scope baseline.

**Applied**: `tasks.md` T007, T036, Notes (test-budget ruling).

## M-2 · Count anchor 4553 vs 4551 → resolved by reconciliation duty

**Finding**: the `-q` baseline log has no collected line; 4553 came from the pytest cache, while the run accounted 4551 (83 + 4467 + 1); T001 used 4553 as a stop anchor.

**Applied**: `tasks.md` T001 now records a three-number reconciliation (runner collected, baseline accounted 4551, cache nodeids 4553) and requires an explanation of any difference; no single number is a stop anchor. `tasks.md` Notes records the anchor.

## M-3 · Feature registry linkage → resolved

**Finding**: `features/058.md` 067 entry lacked the US5 test-slimming scope and its header date was stale; `features.md` 058 row had no 067 record.

**Applied**: `features/058.md` Last Updated → 2026-10-22 and the 067 entry now carries the US5 / FR-011…FR-021 / SC-006…SC-010 scope and the 750 s / 83-failed baseline; `features.md` 058 row now records the 067 evolution spec. No Feature ID, count, or status change.

## LOW dispositions

| Finding | Disposition |
|---|---|
| admission red anchor 82.5 s not reproducible | Fixed: tasks use the measured 87.45 s sum (18 durations) and note the earlier number as a discarded partial count. |
| host identity strings (macOS 26.6.2 vs Darwin 25.6.0) | Carried: both are true (product version vs kernel); the measurement record pins Python/pytest and the dated host. No gate depends on the string. |
| MP-02 PIPESTATUS vs "POSIX sh" wording | Carried to implement T007/T034: the measurement wrapper uses bash-compatible `PIPESTATUS`; contract wording can be adjusted in a `PLAN-EDIT:` if needed. |
| FR-014 mapping included T016/T017 | Fixed in tasks Requirements Coverage: FR-014 → T005 / T019–T022; T016/T017 move to FR-016. |
| FR-018 "等同类" open tail vs CHK005 closed | Carried: the pinned roster (T002) is the closed enumeration; FR-018's "同类" is the category rule, not a second roster. The roster is generated from `tests/contract/` and reviewed in T029. |
| P-5 candidate enumeration not persisted | Fixed: `test-evidence/mirror-parity-candidates-2026-10-22.txt` persisted from the narrower regex (36 functions). The P-5 count of 44 used a broader regex; T020–T022 re-scan and record the actual folded set in the ledger. |
| checklist advisory count 8 vs 10 | Carried: the checklist was written when pre-analyze scanned a smaller file set; the added checklist itself produces 9 TB-03/04 advisories. Non-blocking. |
| E1 symbol double namespace preventive note | Carried: E1 consistently means FullRunMeasurement in this spec; no artifact uses E1 for another entity. |

## Boundary

- No tests were run; no pass/fail claim is made.
- Only planning/evidence/registry files changed: `tasks.md`, `features/058.md`, `features.md`, `test-evidence/mirror-parity-candidates-2026-10-22.txt`, this record.
- Implementation remains gated on a fresh implement dispatch; the analyze verdict stays GREEN.
