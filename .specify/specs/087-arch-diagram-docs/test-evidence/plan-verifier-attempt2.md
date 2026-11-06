# Independent Plan Verification — Attempt 2 (after repair c7b58681)

- Object: `.specify/specs/087-arch-diagram-docs/` @ `c7b58681` (base `7663ea5b` / `24cb4edc`)
- Verifier: fresh-context `SDD Stage Verifier` (read-only)
- Verdict: **PLAN-VERIFY: fail**

## Closed

- P1-1: per-example premises present (S3/S4/S5/S9); `--record` registered in `C-001` closed parameter set; no unregistered flags.
- P1-2: `C-016` nine-row precedence; `data-model.md` E6 11-row fixtures; S3/S9 consistent; no remaining priority conflict (data-model:167 defers to C-016).
- P1-3: single `<root>/docs/assets/<slug>.<ext>` landing across T-005 / C-009 / C-010 / data-model / quickstart / feature-ref; antithesis/evidence/reopening present; second landing absent.
- P1-4: clause→test map covers C-001…C-016 (16 rows) and C-001…C-023 (23 rows); C-005/C-012/C-013 named assertions present.

## P1-A (blocking)

`C-008a` R6 convergence criterion "four counts zero AND `clean=true`" directly conflicts with `C-013`'s `exempted>0 ⇒ clean=false`. `C-008a` R5 itself accepts a valid `recorded-exemption` as a terminal state, but R6 excludes it from convergence. Consequence: a compliant "no structure to draw" document (FR-004 / US1 scenario 3 / SC-008) keeps `clean=false` forever, so "convergence" has no unique reading; SC-003 reachability depends on an unwritten premise that the fixture space contains no exemption. Evidence: `contracts/diagram-obligation.contract.md:85-86,282-284`; `contracts/flow-obligations.contract.md:59-60,66-67`; `quickstart.md:299,303`.

## P2 residuals

- P2-1: `#### Assets` subsection is cited as an existing owner (`plan.md:438,445`; `contracts/flow-obligations.contract.md:5,71`) but does not exist on disk; it is an implementation-time new subsection. Rephrase as "created by this feature".
- P2-2: `C-007` row's assertion names are swapped (`plan.md:422`): `test_c007_no_second_precedence_owner` describes single-pass C-016 behavior; `test_c016_no_backtracking` belongs to the C-007/C-016 boundary; `red-when` is attached to the wrong clause.
- P2-3: `test_protected_gate_preserved` is 16 parameterized instances; only one is the `docs.md` `stop-and-confirm` guard. The quickstart selector is lenient (it can go green on unrelated guards). Narrow the selector or state the broader guard explicitly.
- P2-4: `plan.md:373` Evidence List still says "23 carriers" while `plan.md:503` says 85; the source cites quickstart S2 (85). Delete the stale count copy (constitution XIV) rather than correcting the number.
- P2-5: `plan-stage-status.md` changed_paths includes `features.md`, `features/087.md`, `register.md`, but §1/§2 has no reading covering them; add a coverage line or narrow the field.

## Driver ruling for attempt 3

Introduce a **`converged`** predicate separate from `clean`:
- `converged` = `missing == 0 && stale == 0 && not_evaluated == 0` (exemptions allowed as terminal).
- `clean` remains strict (`exempted > 0 ⇒ clean = false`).
- `C-008a` R6 uses `converged=true`; `clean` is reported separately. SC-003 "zero diagram findings" maps to `converged`, not `clean`.
- Update C-008a, C-013, quickstart S9, plan Test Plan, data-model summary, and `I::test_c008a_second_reconcile_zero_findings` to assert `converged=true` with at least one exemption fixture and `clean=false` allowed.
Fix the four P2 residuals in the same pass; no FR/SC changes, no scope expansion.
