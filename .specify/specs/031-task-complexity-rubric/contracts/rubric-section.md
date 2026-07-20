# Contract: Task Complexity Rubric Section

**Feature**: 032 Task Complexity Rubric · **Spec**: `031-task-complexity-rubric` · **Date**: 2026-07-20

This contract defines the structural assertions a verification test MUST enforce against the instructions template. It is the acceptance surface for a template-only feature (Constitution Principle IV → Partial, verified structurally).

## Scope

The contract applies to the instructions template in both mirror locations:

- `templates/instructions-template.md`
- `.specify/templates/instructions-template.md`

## Structural Requirements

- **C-1 (heading)**: The template MUST contain the exact heading line `## Task Complexity Rubric` (matches Shared String `STR-001`).
- **C-2 (tier table)**: The section MUST contain a Markdown table.
- **C-3 (tiers)**: The table MUST define exactly four tiers, labeled `Trivial`, `Standard`, `Complex`, and `High-stakes / Ambiguous`. Labels are stable and case-sensitive.
- **C-4 (signals)**: The section MUST name all five signal dimensions: scope/size, uncertainty/novelty, blast radius/reversibility, cross-cutting impact, and requirements clarity.
- **C-5 (thinking depth)**: Each tier row MUST prescribe a thinking-depth behavior referencing effort across exploration, planning, and verification.
- **C-6 (tie-break)**: The section MUST state that when signals span multiple tiers, the higher tier is chosen.
- **C-7 (default tier)**: The section MUST define a default tier for unclassifiable tasks and MUST direct the agent to clarify when the cause is unclear requirements.
- **C-8 (tradeoff)**: The section MUST include an explicit efficiency-vs-quality statement covering both failure modes (under-thinking complex work; over-thinking trivial work).
- **C-9 (neutrality)**: The section MUST NOT contain project-specific identifiers (no `spec-kit`, `specify`, feature IDs, or repository-specific paths); content is valid for any generated project.
- **C-10 (mirror parity)**: The `## Task Complexity Rubric` section MUST be byte-identical between `templates/instructions-template.md` and `.specify/templates/instructions-template.md`.

## Success Criteria Mapping

| Contract check | Success Criterion / Requirement |
|----------------|---------------------------------|
| C-1 present after generation | SC-001, FR-009 |
| C-1…C-10 hold on the template | FR-001…FR-008, FR-012 |
| C-10 mirror parity | Mirror-sync constraint (plan Technical Context) |
| Non-destructive insertion into existing docs | SC-002, FR-010, FR-011 — verified by refresh diff / manual review (not a static template assertion) |
| Reviewer/agent agreement on tiers & depth | SC-003, SC-004 — verified by review artefact, out of scope for the unit test |

## Verification Notes

- C-1…C-10 are statically checkable by reading the two template files; a `pytest` module SHOULD assert them.
- SC-002 (byte-for-byte preservation of other sections on refresh) is verified by a before/after diff of a fixture instructions document, or by manual review, since it exercises the `/speckit.instructions` refresh flow rather than static template content.
- SC-003/SC-004 require human/LLM review and are recorded under the feature directory at acceptance; they are not part of the automated unit test.
