# Contract: Instructions Section Propagation

**Feature**: 082-self-explanatory-integration | **Contract file**: `contracts/instructions-propagation.contract.md`
**Guard carrier**: `tests/contract/test_instructions_section_propagation.py` (extended) and
`tests/contract/test_instructions_size_budget.py` (unchanged, must stay green)
**FR coverage**: FR-004, FR-005, FR-009; SC-003, SC-009

The ambient section must reach the template, the live file, and every downstream project — and the
mutation leg must fail on the **template** side, because a live file that still carries an old section
would let a template-side deletion pass unnoticed.

## C-10 — The section exists in the template

`templates/instructions-template.md` MUST contain a top-level heading `## STR-001` verbatim, and its
body MUST contain the runtime owner pointer `STR-004`.

## C-11 — The section is summary plus pointer, not a copy

The section body MUST consist of at most two summary sentences plus the pointer line(s). It MUST NOT
contain any section body of the owner documents: the carrier asserts that none of the owner's own
level-2 heading lines (from `STR-002` and from `STR-004`'s mirrored twin) appears inside the section.

## C-12 — Placement is template order, and the live file is reconciled additively

The generator injects only sections **missing** from the live file, in template order, inserting each
before the next template section that already exists. The section's placement in the template therefore
decides its placement in every future injection; the implementation MUST place it where the reader's
mental model wants it (immediately after the existing `## One Source Of Truth` / `## Closed-Set Claims`
/ `## Grounded Naming` cluster, before `## Bilingual Expression`), and MUST NOT reorder existing
sections to achieve that.

## C-13 — Injection preserves existing content

Given a fixture project whose live `.specify/instructions.md` already carries a custom section and a
customised copy of a template section, running `bash scripts/bash/generate-instructions.sh` MUST:

- inject the missing `## STR-001` section verbatim, and
- leave every pre-existing section byte-identical (customised body and project-specific section both
  preserved), and
- be idempotent — a second run injects nothing and reports that the live file already carries all
  template sections.

## C-14 — The mutation leg fires on the template side

The carrier MUST assert, **without reading the live file**, that the template carries the section and
that the generator's reconcile input (the rendered template) contains the heading. A test that only
asserts the live file's content MUST NOT be counted as satisfying this clause: a template-side
deletion would leave the live copy in place and the assertion would stay green.

## C-15 — The live file carries the section after regeneration

After `bash scripts/bash/generate-instructions.sh` runs on the repository, `.specify/instructions.md`
MUST contain `## STR-001` and its body MUST contain `STR-004`.

## C-16 — The compatibility symlinks stay symlinks

`CLAUDE.md`, `QODER.md`, `AGENTS.md` (and the four tool-directory links the generator maintains) MUST
remain symbolic links whose target resolves to `.specify/instructions.md`. Rewriting any of them as an
independent copy MUST fail this clause. The assertion reads the link's target, not the file's content.

## C-17 — Size stays within the raised budget

After injection, the measured size of `.specify/instructions.md` MUST satisfy
`size <= INSTRUCTIONS_BUDGET_BYTES - 1`, i.e. the generator's report MUST print `within` (its `over`
verdict fires at `size >= budget`). `INSTRUCTIONS_BUDGET_BYTES` MUST remain defined in exactly one
place, `scripts/bash/generate-instructions.sh`, and no test, template, or document may restate its
value.

## C-18 — The raise is recorded with its reason and its magnitude rule

The raise MUST be recorded in the change that adds the section, carrying: the old value, the new value,
the measured live size after injection, the reason (this section), and the raise rule (smallest
multiple of 1024 leaving at least 1024 B of headroom — plan § T-001). A raise without a recorded reason
MUST fail this clause; a raise larger than the rule requires MUST be called out in the tasks-level
notes.

## C-19 — The docs-facing row stays accurate

If the Documentation Map in the template gains or should gain a row for the owner document, the row
MUST point at `STR-004` (runtime path). If the map gains no row, this clause is satisfied by the
recorded decision not to add one — the owner is reachable through the section's pointer.

## Mutation legs owned by this file

| Leg | Mutation (on a temp copy, never the repository) | Assertion that must go red |
|-----|------------------------------------------------|---------------------------|
| M-3 | Delete the `## STR-001` section from a copy of the template | C-14's template-side presence assertion (and C-10 when redirected at the copy) |
| M-4 | Run the generator on a fixture with no template section and assert nothing is injected | C-13's positive half, in its anti-vacuity form |

M-3 MUST run against the copy only; the carrier MUST assert afterwards that the real template still
carries the heading.
