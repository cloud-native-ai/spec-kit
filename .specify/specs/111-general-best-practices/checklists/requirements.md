# Specification Quality Checklist: General Best Practices — 通用最佳实践模块（四分类封闭集 + 渐进积累）

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-11-27
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
- [x] Every required outcome from the brief has at least one functional requirement (module five documents FR-001 / FR-002; first entry FR-003; accumulation by pointer FR-004; distribution wiring FR-005 / FR-006; contract guard FR-007; naming adaptation & zero residue FR-008; containment FR-009)
- [x] Backward-incompatible changes are closed over migration/refusal behaviors (none: additive documentation only; no engine, template, skill, store layout or decision-governance surface changes — FR-009; existing `shared/` refresh semantics unchanged — A-14)
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

- **Checker run (authoritative for structural propositions; counts below derive from this run, never hand-typed)**: `python3 .specify/scripts/python/validate-requirements.py .specify/specs/111-general-best-practices/requirements.md` → `status: ok`, `0 error(s), 0 warning(s)`, scanned **200 lines, 16 definition rows, 7 shared strings**; verbatim output at `test-evidence/requirements-validator.txt`. One repair iteration was consumed before this stamped run: STR-002…STR-005 `Consumed by` cells named SC-001 while SC-001 did not cite the ids; SC-001 now cites all four strings and the re-run is the recorded one.
- **Driver gate self-check**: `pre-analyze-check.py --spec-dir .specify/specs/111-general-best-practices --stage requirements --repo .` output captured at `test-evidence/pre-analyze-requirements.json`; the only expected advisories are the not-yet-created deliverable paths (`shared/best-practices/**`, `tests/contract/test_general_best_practices.py`) — deliverables land in the implement stage.
- **Decomposition gate**: `decomposition-check.py --mode plan --requirements .specify/specs/111-general-best-practices/requirements.md` output captured at `test-evidence/decomposition-requirements.json` (9 FR definition rows, far below the ceiling).
- **Judgement notes (why the generic wording above is satisfied in this framework-source feature)**:
  - "No implementation details" / "non-technical stakeholders": the product surface *is* shipped documentation plus one framework-map registration; path-level statements name product surfaces (as in 103 / 104 / 107 / 108), not incidental implementation; readers are declared in the header.
  - Containment claim (FR-009 / SC-006): baseline referent = commit `0419adae5`; allowed delta = the FR-009 path set (spec artifacts, `shared/best-practices/**`, its mirror, framework-map row + mirror, the guard, the wrap-up accounting records identified by the record-body predicate) plus the later feature-registration exception; all other paths carry an empty allowed delta — decidable by `git diff --name-only 0419adae5..HEAD` plus the record-body check for the three accounting stores.
  - `execution` class duties: § Runtime Stack & Dependency Ownership present with three rows (`RS-001`…`RS-003`), `Form` cells inside the closed domain, `FR` cells resolving, `Premises` cells naming `EP-001`…`EP-003` (the plan stage owns their definitions; this stage carries the references).
- **Sanctioned variant applied**: no clarification markers were needed; the brief's ambiguity list was adjudicated one-by-one under `## Assumptions & Decisions` (A-1…A-14) and `## Clarifications` > `### Session 2026-11-27`, and the checklist passes green on its first stamped pass (after the one validator repair above, which changed no semantic content).
- **Scaffold deviation (disclosed)**: `create-new-requirements.sh` counts local branches `109-prompt-adherence` / `110-context-management` / `111-general-best-practices` in the numbering space, would derive 112 and create a second branch; per A-9 and the 108 A-16 precedent, the spec was scaffolded manually from `.specify/templates/requirements-template.md`, staying on branch `111-general-best-practices` with number 111. Recorded in `test-evidence/requirements-stage-2026-11-27.md`.
- **Source verification (before adding wiring)**: the ai-harness 087 source set was read in full (requirements / plan / tasks / contract / verification + the five module documents). Measured: the source shipped the manifest + four category files + first entry + guard + mirror, and added **no** framework-map row and **no** instructions pointer (whole-repo `best-practices` search zero hits outside the module and its spec). Target governance (`shared/guidelines/directory-governance.md` § 3) nevertheless requires same-change registration in the framework map, so FR-005 adds exactly that row; instructions stay untouched (A-6).
- **Scope discipline**: this stage wrote only `.specify/specs/111-general-best-practices/**`; no spine, feature-registry, glossary or mirror edits (A-10). Glossary candidates ("best practice / 最佳实践", "progressive accumulation / 渐进积累") are recorded in the spec for the clarify stage to propose, not registered here.
- **No failing items; one validator repair iteration consumed (well under the max of 3).**