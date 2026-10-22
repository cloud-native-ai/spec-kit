# Debt — clause-form co-occurrence inside feature 060's archived contracts — 2026-10-22

**Status**: registered (FB-06). **Not introduced by this scope** (067-loop-efficiency-hardening).

## Failing pinned test

- `tests/contract/test_clause_forms.py::test_the_four_md_forms_never_co_occur_in_one_file`

## Failure shape

The test walks `.specify/specs/*/contracts/*.md` and asserts no file contains more than one md
clause form. Two files co-occur `md-bold-closed` + `md-heading`:

- `.specify/specs/060-decompose-subagent-dispatch/contracts/delegation-parity.md`
- `.specify/specs/060-decompose-subagent-dispatch/contracts/skill-enhancements.md`

## Why not repaired here

1. The offenders are **another feature's archived spec contracts** (dated records of feature 060,
   landed `e7c2ed0c` / `31780ada`, 2026-10-17 — both predate the 067 branch). Rewriting another
   feature's archived contracts is outside this part's write surface and would falsify dated
   records.
2. Narrowing the test's corpus glob to skip 060 would shrink the assertion surface (weakening) —
   forbidden.

## Repair path (owned elsewhere)

Either normalize the clause form inside 060's two contract files through an owning maintenance
flow, or have the clause-definitions owner rule on whether archived pre-053 contracts are in the
corpus at all (an owner-document decision, not a triage-part edit).
