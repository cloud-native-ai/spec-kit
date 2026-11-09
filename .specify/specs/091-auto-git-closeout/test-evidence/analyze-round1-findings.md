# Analyze Round 1 — Findings and Repair Brief (2026-11-09)

Stage: analyze (read-only). Base commit: 1e49534a. Findings: 1 CRITICAL / 4 HIGH / 13 MEDIUM / 4 LOW (+2 feature-linkage) = 20. The CRITICAL/HIGH validation wave was not dispatched (worker has no dispatch authority); severities are cap-of-record, unconfirmed.

## Blocking findings (implement entry)

- **C-01 (CRITICAL, coverage)**: FR-020, FR-021, FR-022, FR-027 are cited by ZERO contract clause. `feature-ref.md` § FR→contract map is the sole evidence for "every FR is discharged"; four map rows point at clauses with a different subject. Fix: add clauses — `contracts/closeout-lifecycle.contract.md` (extend C-1 + new C-8 for FR-020/021; FR-022 pointer duty), `contracts/closeout-executor.contract.md` C-1 (add the five FR-027 non-goals as an owned negative assertion), `contracts/closeout-verification.contract.md` C-5 (FR-022 pointer duty); correct the map; re-adjudicate `tasks.md` § FR lane note.
- **H-01 (HIGH, inconsistency/containment)**: C-2/C-6 vs T008/T013/T014 — the "no second branch table" guard is scoped only to the shipped asset; the instance file already carries model facts. Fix: narrow C-2's guard scope or parameterise T013/T014 over both surfaces.
- **H-02 (HIGH, underspecification)**: the strongest authorization value is settled by a placeholder edit (T021); the four-value domain has no behaviour-level guard and US1/US3 fixtures bypass `format` via `ask`. Fix: settle whether the strength lives in C-7's text or in a runnable transition; clear the placeholder rows or reframe the transition.
- **H-03 (HIGH, inconsistency)**: C-3 requires a per-covered-record commit hash, but data-model E-4 carries a single `commit` field and says receipt+records+artifacts are one commit. Fix: make E-4 per-entry (or state one commit for all) and settle the commit split in C-2/C-3.
- **H-04 (HIGH, zero-write/commit)**: C-4 ("empty list degrades to skipped") vs C-5 (read-only row skips the close-out); C-5 merges "block unread" and "declared but no remotes" into one row. Fix: split the row and show the relation to the `ask`/absent axis.

## Other findings to address as feasible

- M-01 invalid contract link (`openapi-format-per-clause` references a nonexistent clause); M-02 C-1 file-read-only vs C-4/C-5 subprocess; M-03 invocation token unnamed; M-04 state-set closure (4 terminal states vs 5 edge cases); M-05 value grammar only downstream and already contradictory ("empty or absent" vs "explicitly empty"); M-06 per-value effect table missing; M-07 receipt home `.specify/memory/retention/closeout/` is a new store (retention/ holds only plans/) — make the referent decidable or re-justify on a measured statement; M-08 six FR→contract map rows point at clauses with a different subject; M-09 fixture roster duplicated across SC-001/002/003 and data-model E-6; M-10 feature detail lacks `## Status Tracking`; M-11 stage record stops at plan; L-01 edge case "only-read-only remote" unreachable; L-02/L-03/L-04 naming/ID/orthography nits.
- Checklist fail items: 10 STILL-VALID / 5 PARTIAL; the dispositions are in the analyze report (CHK009/011/016/020/023/036/038/040/045/046 still valid; CHK010/012/017/021/028 partial). Fold the owner-text fixes into the repair.

## Implement-entry precondition list (R-1..R-13)

R-1 C-01 clauses+map; R-2 H-01 guard scope; R-3 H-02 authorization carrier; R-4 H-03 receipt commit; R-5 H-04 row split; R-6 M-07 receipt home; R-7 M-08 map re-verification; R-8 M-10/M-11 feature registry/detail; R-9 CHK010 FR-008 machine form; R-10 CHK012/CHK017 two readings; R-11 CHK036 RS-001 capability set; R-12 CHK023 A20 pointer from SC-004; R-13 CHK046 Readers/Reading scenario on requirements.

## Repair scope

Edit only `.specify/specs/091-auto-git-closeout/**` and `.specify/memory/features*` (no framework source). Re-run `validate-requirements.py`, `pre-analyze-check.py --stage requirements`, `pre-analyze-check.py --stage plan`, `validate-decision-tensions.py`, `decomposition-check.py --mode plan`; commit the repair with explicit paths; no push; run wrap-up accounting. Return the resolved/residual findings.
