# Specification Quality Checklist: Team View Degradation Hardening — 真实团队定义下的诚实呈现与降级语义

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-26
**Feature**: [requirements.md](../requirements.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Stability / containment claims name a baseline referent and a derivable allowed-delta set (owner: `.specify/shared/guidelines/closed-set-claims.md`)
- [x] Every required outcome from the brief has at least one functional requirement (report recognition FR-001…FR-006; missing artifacts FR-007…FR-010; binding/goal normalization FR-011…FR-014; roster matrix FR-015…FR-016; exit-code/degradation semantics FR-017…FR-020; preserved healthy behavior & one engine FR-021…FR-025)
- [x] Backward-incompatible changes are closed over migration/refusal behaviors (FR-023; A-11; no schema or naming-owner change, so existing teams need no migration)
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- **Checker run (authoritative for structural propositions; counts below derive from this run, never hand-typed)**: `python3 .specify/scripts/python/validate-requirements.py .specify/specs/108-team-view-degradation/requirements.md` → `status: ok`, `0 error(s), 0 warning(s)`, scanned **228 lines, 33 definition rows, 3 shared strings**; verbatim output at `test-evidence/requirements-validator.txt` (one repair iteration consumed: STR-003's `Consumed by` cell named SC-001 without SC-001 citing it; cell corrected and the re-run is the recorded one).
- **Driver gate self-check**: `pre-analyze-check.py --spec-dir .specify/specs/108-team-view-degradation --stage requirements --repo .` → `decision=pass errors=0 advisories=0 waived=0`, summary `fr=25 sc=8`; captured verbatim at `test-evidence/pre-analyze-requirements.json`.
- **Decomposition gate**: `decomposition-check.py --mode plan --requirements .specify/specs/108-team-view-degradation/requirements.md` → `decision=proceed`, `fr_count=25`, `fr_ceiling=120`; captured verbatim at `test-evidence/decomposition-requirements.json`.
- **Judgement notes (why the generic wording above is satisfied in this framework-source feature)**:
  - "No implementation details" / "non-technical stakeholders": the feature's product surface *is* the framework's read-only view; path-level statements name product surfaces (as in 103 / 104 / 107), not incidental implementation; the readers baseline is declared in the header.
  - Containment claim (FR-022 / SC-004): baseline referent = the program at commit `54c6efa8c` run on the same healthy fixture (`git show 54c6efa8c:scripts/python/team-view.py`); observation = byte-level stdout diff + exit-code comparison inside the test; allowed delta for the healthy predicate = empty, and non-healthy inputs carry the named corrections enumerated in A-11/FR-022 — no undefined aggregate ("其余"/"unaffected") carries acceptance semantics.
  - Scope: `Related Feature` remains `Need clarification`; binding is deferred to `/speckit.clarify` per the Feature Integration Protocol.
  - `execution` class duties: § Runtime Stack & Dependency Ownership present with 5 rows (`RS-001`…`RS-005`), `Form` cells inside the closed domain, `FR` cells resolving, `Premises` cells naming `EP-001`…`EP-003` (the plan stage owns their definitions; this stage carries the references).
- **Sanctioned variant applied**: no `[NEEDS CLARIFICATION]` markers were needed; the adjudications and the scaffold deviation are recorded under `## Clarifications` > `### Session 2026-11-26`, and the checklist passes green on its first stamped pass (after the one validator repair above, which changed no semantic content).
- **Scaffold deviation (disclosed)**: `create-new-requirements.sh` counts the current local branch `108-team-view-degradation` as a used number, would derive 109 and create a second branch; per A-16 the spec was scaffolded manually from `.specify/templates/requirements-template.md`, staying on branch `108-team-view-degradation` with number 108. Recorded in `test-evidence/requirements-stage-2026-11-26.md`.
- **Evidence base**: production facts are the user-supplied client output (client project not in this repo); the in-repo measured corpus (46 run-directory files, 28 conforming / 16 stamped-non-conforming / 2 unstamped; three teams with zero recognized reports) is recorded in the Overview and reproduced by the acceptance fixtures. Live counts are a dated baseline, not an acceptance oracle.
- **No failing items; one validator repair iteration consumed (well under the max of 3).**
