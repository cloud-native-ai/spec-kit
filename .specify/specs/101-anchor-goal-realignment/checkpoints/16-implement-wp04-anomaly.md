# Checkpoint 16 — implement WP-04 (cleanup anomaly and ruling)

## 1. Artifact verification

- sentinel: **none** — WP-04 halted after T048–T057 with a decision-level anomaly before T058–T060.
- executed: T048 classification evidence (9 anchor / 3 action-goal / 2 obsolete); T049 `cleanup --check` ok/zero writes; T050 9 `goal.md`→`anchor.md` + A-N normalization + 9 body receipts (digests equal); T051 3 migrations + receipts (088 two Targets preserved); T052 2 archives + receipts; T053 R2 `visualization-skill-selection`; T054 2 summary trees moved (13+9 files), 3 to regenerate; T055 16 renames (8 rename / 8 rename+normalize), 4 unbound byte-identical; T056 declared N-rules, C6 team pointer → 0; T057 7 dispositions all `apply` (6 R3 + R2), 091 binding removed.
- live stores: `.specify/anchoring` = 10 anchors (9 original + R2), 0 `goal.md`; `.specify/goals` = 3; `.specify/archive/anchoring` = 2; receipts 9+3+2+16+7; 10/10 `anchor_slug` resolve; 6 R3 binding lines removed.
- idempotency: the read-only post-apply check reports `already-migrated` 3, `already-archived` 2, `already-normalized` 9, teams 16, dispositions `already-satisfied` 7; the second apply was not run (the package halted before T058–T060).
- targeted tests: 3 failed / 53 passed / 1 skipped — one E2 baseline id, two pre-existing at base from WP-03's `summary-mapping.md` rewrite (not WP-04 edits).
- wrap-up: `/speckit.implement` engines deduped to WP-01a's records; the WP-04 review text is preserved in the evidence, a known store-schema fact.

## 2. Anomalies and ruling

1. **2 `goal_slug` tokens remain in live team frontmatter** (`draw-diagram-interactive/team.md:8`, `command-logic-as-classified-skills/team.md:72`). C-46 N-1 is body-scoped and cannot reach frontmatter. Ruling: extend the cleanup contract with **N-8** (frontmatter `goal_slug` → `anchor_slug`), implement it in the engine, re-run the cleanup; the live team definitions must reach 0.
2. **15 live team-definition lines in 9 teams still cite a `goal.md`** renamed/moved by P1/P2; C-46 N-2 only matches `.specify/goal/<slug>/goal.md`, not the already-anchored `.specify/anchoring/<slug>/goal.md` form. Ruling: extend the contract with **N-9** (both forms → the new file) and re-run.
3. **5 live team frontmatter `delivery_dir` values still name `.specify/goal/<slug>/summary/`** (FR-058); body-scoped N-3 cannot reach them and the engine’s own checks report converged. Ruling: extend the contract with **N-10** (`delivery_dir` → `.specify/anchoring/<slug>/summary/`), implement the frontmatter normalization, re-run.
4. **SC-005 expects every still-bound team to read `ok/false/0`, but 4 bound teams read `goal-terminal/true/5`** because their Anchors are `achieved`; `run-checks` derives this from the unchanged Anchor lifecycle. Ruling: correct SC-005’s wording/reading — non-achieved bound teams `ok/false/0`; achieved-anchor teams `goal-terminal/true/5` with the measured reading. This is a requirements/SC correction (rebaseline/PLAN-EDIT), not a cleanup defect.
- The package correctly refused to hand-edit a team definition or weaken the FRs. The driver authorizes a bounded WP-04b repair: extend the contract/engine, re-run the cleanup idempotently, correct SC-005, complete T058–T060, and commit.

## 3. Next stage concurrency / roster

- requested: 24; effective: 1; effective_reason: `dependency-edge` — WP-04b completes the interrupted cleanup; one process on the live stores; verifier reserve: 1.
- next package: **WP-04b** (contract/engine N-8…N-10 + SC-005 correction + cleanup completion/T058–T060), then WP-05.

## 4. Direction audit

- reload tier: T0 + T1.
- Q1 rules: unattended / no approval request / U4 → next stage / spine written before acting / workspace guard / fast-fail / gate discipline / budget / report discipline — all in force.
- Q2 process: `decision-needed` was surfaced by the executor, not smoothed; the driver resolved it as a contract/engine correction consistent with FR-047/FR-058/FR-066 plus an SC-005 reading correction; no data deleted, no definition hand-edited.
- Q3 next action: pass — WP-04b completes the cleanup and T058–T060.
- Q4 spine freshness: pass — spine will record attempt 2 before the repair dispatch.
- Q5 territory/workspace: pass — the live cleanup is uncommitted but contained: 10 anchors, 3 goals, 2 archives, receipts; the pre-existing `smoke-081.txt`/`.specify/.specify/` untouched.
- verdict: `correction-applied`.
- 5b published-state: `n/a — no history correction`.
