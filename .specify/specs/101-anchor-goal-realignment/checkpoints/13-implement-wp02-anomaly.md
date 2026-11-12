# Checkpoint 13 — implement WP-02 (decision anomaly and resolution)

## 1. Artifact verification

- sentinel: **none** — the WP-02 package ended with `ANOMALY: 027 command-classification contract cannot absorb /speckit.anchor without violating FR-061 (byte-identical dated specs) — needs a spec-level ruling on whether that contract is living or frozen.`
- partial commit: `52299e61a` (29 files: `templates/commands/anchor.md` seven modes, `templates/commands/goal.md` four modes, `skills/internal/manage-anchor/SKILL.md`, rewritten `manage-goal/SKILL.md`, eight per-tool copies, two reference pages, seven test repins, evidence `implement-wp02.md` + red-first section).
- readings: `command-mode` anchor ×7 / goal ×4 rc 0; Goal + Anchor-only modes rc 2 `anchor-only-mode` pointing to `/speckit.anchor`; `unknown-mode` rc 2. Copies/mirrors: `regen --check` rc 0; `sync --check` rc 0 (skills/internal 138 files byte-identical). Targeted 13 modules: **15 failed / 525 passed** — 9 E2 pre-existing, 5 downstream (3 flow-class → T039; compile census + propagation → T040), 1 decision (the 027 classification test).
- wrap-up duplicates for `/speckit.implement` (WP-01a records); the review text is preserved in the evidence.

## 2. Decision and resolution

- The 027 contract is a **dated record** and is frozen (FR-061, baseline `d7c9da7a3`). The live test must not derive its expected set from a dated contract without a live overlay.
- Driver ruling: add a **live overlay** `anchor: Complex` to `tests/contract/test_feedback_command_classification.py`; live counts 27/5; keep the 027 `**Result**` 26/5 as the historical reading; do not edit 027; do not weaken coverage. The anchor feedback-face assertion remains a **T040-owned** red until the probe compile adds the AUTO-GENERATED wrap-up face.
- Record: `notes/wp02-decision-resolution.md`.

## 3. Next stage concurrency / roster

- requested: 24; effective: 1; effective_reason: `dependency-edge` — WP-02b (the decision repair) follows the WP-02 partial package; verifier reserve: 1.
- next package: **WP-02b** (classification-test live overlay + targeted rerun), then WP-03.

## 4. Direction audit

- reload tier: T0 + T1.
- Q1 rules: unattended / no approval request / U4 → next stage / spine written before acting / workspace guard / fast-fail / gate discipline / budget / report discipline — all in force.
- Q2 process: `decision-needed` was surfaced by the executor, not smoothed over; the driver resolved it as a correction consistent with FR-061 and dispatched a bounded repair. The 5 downstream reds remain owned by T039/T040.
- Q3 next action: pass — WP-02b is the package’s repair before WP-03.
- Q4 spine freshness: pass — spine will record attempt 2 before the repair dispatch.
- Q5 territory/workspace: pass — the partial commit contains only WP-02 files; the pre-existing `smoke-081.txt` and `.specify/.specify/` were untouched.
- verdict: `correction-applied`.
- 5b published-state: `n/a — no history correction`.
