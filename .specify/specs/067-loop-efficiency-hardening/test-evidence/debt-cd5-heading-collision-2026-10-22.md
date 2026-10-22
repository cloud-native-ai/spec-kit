# Debt — cd5 heading-name collision with two newer guideline docs — 2026-10-22

**Status**: registered (FB-06). **Not introduced by this scope** (067-loop-efficiency-hardening).

## Failing pinned test

- `tests/contract/test_token_efficiency_discipline.py::test_cd5_headings_only_in_discipline_doc`

## Failure shape

cd5 asserts that none of the token-efficiency discipline doc's H2 headings appear in any other
`shared/` or `templates/` markdown file. Two offenders:

- `shared/guidelines/progress-reporting.md` — `## 判定边界` (line 88)
- `shared/guidelines/single-run-evidence.md` — `## 判定边界` (line 62)

The two sections are **not copies**: their bodies are entirely different (each declares its own
discipline's boundaries and cross-discipline edges). This is a bare-heading-name collision on a
generic section name, introduced when `f1f6e96a` (2026-10-16) landed the two newer guidelines —
predating the 067 branch.

## Why not repaired here

1. Renaming the sections in the two guidelines would edit `shared/` — outside part F's write
   surface, and each guideline is the owner of its own section names.
2. Refining cd5's matcher to content-anchored comparison (heading + distinctive body line)
   would re-invent the pin's detection semantics — an owner-document decision the test's author
   never recorded. Choosing that unilaterally risks silently narrowing the anti-copy guard.
3. Narrowing the offender scan (skipping those files) would weaken the assertion — forbidden.

## Repair path (owned elsewhere)

Either rename `## 判定边界` in the two newer guidelines to discipline-specific headings through
their owning flow, or have the token-efficiency owner re-specify cd5's match rule (content-
anchored) with the change recorded in the discipline doc.
