# Independent Plan Verification — Attempt 3 (after 3cff4a03)

- Object: `.specify/specs/087-arch-diagram-docs/` @ `3cff4a03`
- Verifier: fresh-context `SDD Stage Verifier` (read-only)
- Verdict: **PLAN-VERIFY: fail**

## Closed

- P1-A主体：`C-013` defines `converged`/`clean` as separate predicates; `C-008a` R6 uses `converged`; no second site uses `clean` as a convergence criterion; exemption fixture `converged=true` + `clean=false`; SC-003 maps to `converged`; SC-008 no longer conflicts.
- P2-1: `#### Assets` marked as implementation-time new subsection in flow-obligations and plan.
- P2-2: C-007/C-016 assertion rows fixed in the diagram-obligation table.
- P2-3: quickstart uses exact node id for `test_protected_gate_preserved`.
- P2-4: stale 23-carrier copy removed; 85/84 accepted as a current S2 citation (not a stale copy).
- P2-5: plan-stage-status coverage table added.

## P1-1 (blocking)

`C-013` says `converged` iff `missing==0 && stale==0 && not_evaluated==0`, but also says `carriers==0 ⇒ converged=false`. The "iff" formula and the empty-carrier exception contradict each other; `C-008a` R6, data-model and plan repeat the pure "three counts zero" formula. The predicate is not a single-valued function; an implementer following R6 would compute `converged=true` for an empty space, violating C-013.

## P2 residuals (fixed by the driver correction)

- P2-1: plan Test Plan flow-obligations `C-007` row described the `--record` call site instead of the Baseline single-landing clause.
- P2-2: `feature-ref.md:55` said "16 items" for SC-009, conflicting with the narrowed exact node id.
- P2-3: `diagram-obligation.contract.md:248` cited `#### Assets` as an existing owner without the "not on disk / created by this feature" qualifier.
- P2-4: `diagram-obligation.contract.md:41` used `unrecorded-trace`, outside the closed verdict/reason set; correct is `not-evaluated` / `no-trace-record`.

## Driver correction applied (disclosed)

- `converged` predicate now includes `judged_scope_has_carrier = (--only absent ? carriers > 0 : true)`; the empty-carrier rule is a conjunct, not an exception; `clean = converged && exempted==0`.
- `C-008a` R6 cites the C-013 predicate instead of restating "three counts zero"; plan/data-model references aligned.
- Added `U::test_c013_empty_scope_not_converged` (default empty scope false; `--only` empty vacuous true).
- Fixed the four P2 residuals above.

No FR/SC changes, no scope expansion. A fresh independent verifier must confirm this correction before plan U4 passes.
