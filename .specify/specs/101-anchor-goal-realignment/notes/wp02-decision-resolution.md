# WP-02 decision resolution — 027 contract vs live classification test

## The anomaly (from WP-02 T034, 2026-11-12)

`tests/contract/test_feedback_command_classification.py` derives its expected
Complex/Simple table from the **dated** contract
`.specify/specs/027-feedback-mechanism/contracts/command-classification.md`.
Adding the new `/speckit.anchor` command can only satisfy that test by editing the
027 contract — which FR-061 protects byte-identical at baseline `d7c9da7a3` — or by
weakening the test’s coverage assertion. The two readings cannot both hold. The
package halted with `ANOMALY:` instead of choosing.

## Ruling (driver, FR-061-consistent)

- **The 027 contract is a dated record — frozen.** It is not edited, not rewritten,
  and its `**Result**: 26 complex / 5 simple` line remains the historical reading.
- **The live test adapts to live facts.** `tests/contract/test_feedback_command_classification.py`
  gains a small, explicit **live overlay** `anchor: Complex`. The live expected set is the
  027 rows plus the overlay; the live counts become **27 complex / 5 simple**.
  The test keeps its actual coverage: every `templates/commands/*.md` stem, including
  `anchor`, is classified; the 027 table is still read as the historical baseline.
- **The anchor feedback face is T040-owned.** The new `templates/commands/anchor.md`
  carries a reserved empty `## Wrap-up`; the compiled AUTO-GENERATED face is added by
  the probe compile/propagation task T040 (WP-03). Until then the anchor entry is
  classified Complex but its feedback-face assertion is a named T040 downstream red,
  not a decision and not a weakening of the test.
- **Why this is a correction, not a new decision:** FR-061 already records the intent
  “dated records are frozen”; the live test’s expected set is the only surface that
  must move to include a new live command. Editing the dated contract would contradict
  an explicit FR; weakening the test would remove a coverage fact. The overlay adds
  coverage and preserves both recorded intents.

## Downstream ownership

- 3 flow-class reds → T039 (live flow-class ledger `/speckit.anchor` row).
- compile census + propagation → T040 (probe registry/compiled wrap-up face).
- The classification test’s anchor feedback-face assertion → T040 (same compiled face).
- 9 E2 pre-existing failure ids remain baseline; no random regression.
