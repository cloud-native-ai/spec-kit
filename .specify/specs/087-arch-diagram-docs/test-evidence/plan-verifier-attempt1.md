# Independent Plan Verification — Attempt 1

- Object: `.specify/specs/087-arch-diagram-docs/` @ `7663ea5b` (base `24cb4edc`)
- Verifier: fresh-context `SDD Stage Verifier` (read-only; no writes, no commits)
- Verdict: **PLAN-VERIFY: fail**

## Passed dimensions

- Constitution Check: 19/19 rows match the live constitution; no gap/over-count; Complexity Tracking N/A consistent.
- EP-001: defined, `verified` / `resolve-in-scope`, supports all seven RS rows; Inherited Blockers `Dependency set: none` + `(none)` sentinel legal.
- Decision Tensions: 5 records, owner grammar ok (`validate-decision-tensions.py` 0 error).
- Requirement coverage: 23 FR / 10 SC mapped; no scope creep (no new command/engine/second delivery contract/docs backfill).
- Mirror Obligations: six rows cover the four changed sources + doc + tests; false-red typer premise stated; hand-edit prohibition stated.
- Feature status: 087 = Planned; OI-087-01 / D-001 registered with correct owners.
- Overlap: historical overlaps only (033/037/045/049/059/062/063/069/071/072/077/084); no concurrent writer on the four paths; git worktree list shows only master + this line. Recommendation: historical overlap, no overlap block.
- Test plan: fixture inventory covers negative verdicts; baseline-relative criterion declared; no full suite in intermediate stage.
- Baseline red: 6038 passed / 17 failed / 2 skipped disclosed; relative criterion used.

## P1 findings (blocking)

- **P1-1 — Execution-verify violated for quickstart S3/S4/S5.** Unimplemented `--action obligation` commands with expected results and an unlisted `--record` flag; only a file-level disclaimer, not per-example premise lists (owner: `create-plan/SKILL.md` Post-Generation Quality Gate).
- **P1-2 — Scenario S3 fixture / step order conflict.** `quickstart.md:82` deletes a `missing-face` rendered face that has no own fixture; under C-008 rule 1 source-newer-than-render fires before the missing-face rule in C-004 precedence, so the expected `missing / orphan-source` is wrong as written.
- **P1-3 — T-005 vs contract C-010 landing-path disagreement.** T-005/feature-ref say `assets/` (precedent `docs/assets/quickstart-workflow.*`); C-010 example + S3 use `docs/concepts/diagrams/`; C-009 permits three shapes. Two authorities for one fact; needs one ruling carried through T-005, C-009, C-010, data-model E6 and S3.
- **P1-4 — No contract-clause → test mapping.** C-001…C-015 and C-001…C-023 are not enumerated against test assertions/fixtures; C-005/C-012/C-013 have no named assertion, so negative observability is not decidable.
- **P1-5 — Reconcile cannot converge the diagram dimension.** `create-docs` R5 (`mkdir → write → mv → fix-links → audit`) has no diagram-producing action; C-008 only amends Authoring Flow R2/R5/R6 and Reconcile R6 (verification). SC-001/SC-003 require reconcile to reach zero diagram findings; as written, reconcile would report `missing` forever.

## P2 findings (non-blocking but to address or register)

- P2-1: Six skill-ownership claims are unverified/contradicted (section headings R2/R5/R6 in `create-docs`; `improve-docs` step-3 table; `diagram obligation` term anchor; delivery-contract puml → svg+png; FR-004 vs FR-014 anchor; `<venv>` path not created by plan).
- P2-2: Known-red baseline not registered: 23 carriers, one document with a diagram (no trace record) → `not-evaluated` once the checker lands.
- P2-3: `docs/tutorials/quickstart.md` alt text "Core Development" vs intro "Develop" — semantic inconsistency C-009 does not cover; register under D-001.
- P2-4: `test-evidence/plan-stage-status.md` lacks a machine `stage-status` row shape required by the test-budget audit.
- P2-5: argparse error rendering wrapped editorially; capture should be a single line.

## Driver ruling on P1-3 (unattended, disclosed)

Use the existing `docs/assets/` convention for both diagram source and rendered artifacts (precedent: `docs/assets/quickstart-workflow.{puml,svg,png}`), with doc-relative references. Align T-005, C-009, C-010, data-model E6 fixtures, quickstart S3 and feature-ref to this ruling; record the antithesis (per-type `diagrams/` subtree vs global `assets/`) and reopening condition.

## Driver ruling on P1-5

The plan MUST make diagram convergence decidable: either add a production/update step to the reconcile route (with the existing authoring flow / draw-diagram as the producer) or explicitly route missing diagrams to the authoring flow and record that convergence responsibility; add the corresponding contract row and a test assertion. Do not claim SC-003 convergence without a production path.
