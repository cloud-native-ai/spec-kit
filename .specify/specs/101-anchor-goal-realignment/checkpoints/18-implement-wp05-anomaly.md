# Checkpoint 18 — implement WP-05 (live-residue anomaly and ruling)

## 1. Artifact verification

- sentinel: **none** — WP-05 delivered its guards/evidence but ended with `ANOMALY: FR-067/SC-001 unmet — C1=2 (derivation-definitions.md:414 + .specify/shared mirror) and C4=1 (build-summary-input.py.md:35) remain on the live tree; both owned outside WP-05 territory, guards not weakened, decision needed.`
- delivered: commit `773e1c6dc` (87 files: 11 guard modules, fixtures, 20 evidence artifacts, `notes/quickstart-run.md`, red-first § WP-05) + `6419de99b` (`.specify/goal/**` prohibition-field classification). Guard readings: **110 passed / 1 failed**, the single red `test_live_semantic_residue::test_live_tree_has_no_old_semantic_residue`; no failure outside the E2 baseline. The 2 base-from-WP-03 `test_goal_writeset` reds were aligned test-side (2 failed/46 → **48 passed**).
- SC-008 docs-build limb recorded `not-evaluated` with the EP-006 measurement; the other limbs measured.
- `.specify/goal/**` in 12 live team.md files classified as a stale address in a **forbidden-path prohibition field** (not a binding/definition reference); the closed C1–C7 classes do not cover prohibition fields; owner = the team-definition surface; recorded, not edited.
- new guards: command-surface (anchor/goal), anchor-definitions, goal-store write boundary, binding rename, live semantic residue, cleanup idempotency/resume, protected paths, convergence, command-family; fixtures under `tests/fixtures/anchor-goal-realignment/`.
- wrap-up: `skill:implement-feature` records for `r20261112T064607Z-b101`; duplicates counted as satisfied.
- working tree: only the pre-existing `smoke-081.txt` and `.specify/.specify/` remain outside the committed WP-05 files.

## 2. Ruling

1. **C1** — `shared/definitions/derivation-definitions.md:414` still defines **Goal** as “Project-level authored end state, measured by degree” and points at `goal-definitions.md`. Under the new model the project-level long-term concept is **Anchor**; correct the row to `**Anchor** … anchor-definitions.md` (live definition, not a dated record) and sync the `.specify/shared` mirror.
2. **C4** — `.specify/memory/tools/build-summary-input.py.md:35` still declares the default `--out` as `.specify/goal/<goal-slug>/summary/data/project-input.yaml`; the engine (WP-01b/T022) now writes `.specify/anchoring/<slug>/summary/`. Correct the tool record to the live path.
3. Re-run the `test_live_semantic_residue.py` guard; C1/C4 → 0; the guard suite passes; commit the two live fixes + evidence. Do not weaken the guard, do not edit dated records, do not touch team definitions for the `.specify/goal/**` prohibition classification.
4. The WP-05b repair is a bounded correction, not a new design; after it, WP-06 (registry/close) runs the final full-suite closure.

## 3. Next stage concurrency / roster

- requested: 24; effective: 1; effective_reason: `dependency-edge` — WP-05b is the guard closure on two live files; verifier reserve: 1.
- next package: **WP-05b**, then **WP-06 (T078–T081)**.

## 4. Direction audit

- reload tier: T0 + T1.
- Q1 rules: unattended / no approval request / U4 → next stage / spine written before acting / workspace guard / fast-fail / gate discipline / budget / report discipline — all in force.
- Q2 process: `correction-applied` — the executor routed the two live residues instead of weakening the guard or editing out-of-territory files; the driver ruled the minimal live-surface corrections.
- Q3 next action: pass — WP-05b closes the guard, then WP-06.
- Q4 spine freshness: pass — spine will record attempt 2 before the repair dispatch.
- Q5 territory/workspace: pass — WP-05 wrote only its guard/fixture/evidence paths; the pre-existing dirty files remain untouched.
- verdict: `correction-applied`.
- 5b published-state: `n/a — no history correction`.
