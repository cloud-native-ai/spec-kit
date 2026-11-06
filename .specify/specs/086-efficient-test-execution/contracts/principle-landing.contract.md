# Contract: Test Execution Efficiency Principle Landing (C-021…C-040)

Owner of the propositions below: this contract. Implementation surfaces: the owner guideline, the two
constitution rosters, the two instructions files, the generator skill, and the guards that pin their counts.

**Inherited, not restated**: the one-source-of-truth discipline is owned by
`shared/guidelines/one-source-of-truth.md`; the constitution amendment procedure and the MUST-include
protocol by `skills/internal/manage-constitution/SKILL.md`; the instructions generation and budget
mechanics by `scripts/bash/generate-instructions.sh`; the double-landing guard's propositions by
`.specify/specs/082-self-explanatory-integration/contracts/constitution-double-landing.contract.md`. Each
is reached by path; none is copied here.

## A. The owner guideline (the only definition point)

- **C-021**: A file MUST exist at `shared/guidelines/test-execution-efficiency.md` (`STR-003`, file name
  `STR-001`) whose header declares that it is the single owner of the rule's normative content, per the
  one-source-of-truth owner-declaration requirement (FR-018).
- **C-022**: The owner MUST contain these six sections, each present and non-empty: (1) why coverage is a
  necessary but not a sufficient condition; (2) the criterion by which execution efficiency is judged a
  quality attribute; (3) the decision rule for process-level parallelism vs asynchronous concurrency vs
  neither, with the discriminating property named; (4) isolation preconditions a suite must satisfy before
  parallel execution is legitimate; (5) how to measure "efficient" on a real suite (same selection, same
  command, name-level comparison); (6) the anti-patterns that are never an admissible way to be faster
  (shrinking the selection, skipping, declaring flakiness, retrying until green) (FR-018).
- **C-023**: The owner MUST state the boundary with existing test-related principles: this rule governs what
  tests **cost to execute**; the pre-existing test-quality rules govern **what test exists and when it is
  written**. An overlapping, contradictory instruction is a contract violation (FR-018, FR-023).
- **C-024**: The owner MUST NOT introduce a new command, script, storage surface or gate; it is a guideline
  document only (FR-017).

## B. Constitution, both surfaces

- **C-025**: `templates/constitution-template.md` MUST gain exactly one principle headed
  `### XIX. Efficient Test Execution (Concurrent by Default)`; `.specify/memory/constitution.md` MUST gain
  exactly one principle headed `### XX. Efficient Test Execution (Concurrent by Default)`. The numerals come
  from each roster's own position; the titles are identical by set membership, not by numeral (FR-019).
- **C-026**: Each principle block MUST satisfy the structural rules already in force for the roster:
  3–6 MUST-bearing bullets, lines under 100 characters, a 1–4 sentence `Rationale:` paragraph, a pointer
  to the owner path `shared/guidelines/test-execution-efficiency.md`, and no machinery introduction
  (FR-019).
- **C-027**: Each principle block MUST state (a) coverage is necessary and not sufficient, (b) test
  execution efficiency is a quality attribute at the same tier as coverage, (c) the rule applies to any
  project that builds a test framework or test cases, not only to this project (FR-019).
- **C-028**: Neither constitution block MAY reproduce the owner's decision table, threshold or
  anti-pattern list. A shared table row or an identical multi-line list in both places is a violation
  (pointer shape, not content shape) (FR-019, FR-023).
- **C-029**: The live constitution MUST record the amendment: version `1.16.0 → 1.17.0` (MINOR, new
  principle), a Sync Impact Report block prepended above the previous one, `**Version**: 1.17.0`, and
  `**Last Amended**:` set to the amendment date (FR-022).

## C. Instructions, both surfaces

- **C-030**: `templates/instructions-template.md` and `.specify/instructions.md` MUST each gain exactly one
  ambient section headed `## Test Execution Efficiency (测试执行效率)`, positioned immediately after
  `## Single-Run Evidence Discipline` (FR-020).
- **C-031**: Each section MUST be summary + pointer shape: a short normative summary (3–5 bullets), the
  owner path `shared/guidelines/test-execution-efficiency.md`, and a runtime-pointer form consistent with
  the sibling sections. It MUST NOT contain any level-2 heading copied from the owner (FR-020).
- **C-032**: The live instructions file MUST be produced by `scripts/bash/generate-instructions.sh`, not by
  hand. A hand-edited live file that the generator would overwrite is a violation even if its text matches
  (FR-020).

## D. Generator MUST-include list

- **C-033**: `skills/internal/manage-constitution/SKILL.md` MUST gain exactly one MUST-include entry for this
  principle (list `11 → 12`), carrying the anchor sub-bullet (where the principle text lives) and the
  no-new-machinery sub-bullet, matching the shape of the 11 existing entries (FR-021).

## E. Count and budget guards, updated in the same change

- **C-034**: `tests/contract/test_constitution_double_landing.py` MUST be updated in the same change:
  `TEMPLATE_COUNT 18 → 19`, `LIVE_COUNT 19 → 20`, `COMMAND_COUNT 11 → 12`, and
  `DOUBLE_LANDING_WATCHLIST` extended with the new title (`6 → 7` entries) (FR-022).
- **C-035**: `tests/contract/test_fast_fail_discipline.py` MUST be updated in the same change: the pinned
  live constitution version `1.16.0 → 1.17.0`, the watchlist length `6 → 7`, and the instruction
  section-count pins (`33 → 34` live, `32 → 33` template) (FR-022).
- **C-036**: `tests/contract/test_instructions_section_propagation.py` MUST still pass with the extra
  section, asserting the live file carries every template section (FR-020, FR-022, FR-032).
- **C-037**: `tests/contract/test_instructions_size_budget.py` MUST still pass: the live file's measured
  byte size MUST be ≤ `INSTRUCTIONS_BUDGET_BYTES = 34816`. The budget MUST be changed only if the measured
  size exceeds it, and then the measured value MUST be recorded in test evidence. The gate-scan ceiling
  itself is unchanged by this feature (FR-022).
- **C-038**: The new principle and guideline MUST add **zero** confirmation-gate hits: the scan total after
  the change MUST NOT exceed the value measured immediately before it (27, per `plan.md` EP-008). Equality
  with the stale frozen baseline (23) is explicitly NOT this feature's criterion — two guard tests assert
  that equality and both are already failing on the serial baseline. The budget-raise rule holds: a guarded
  budget (instructions bytes) is raised only with the measured value recorded, and a gate baseline is never
  rewritten to make a criterion green (FR-022).

## F. Both-sides guard and mutation legs

- **C-039**: `tests/contract/test_test_execution_efficiency.py` (new) MUST assert, for **each** of the five
  surfaces (owner, constitution template, live constitution, instructions template, live instructions) plus
  the generator list: the title/pointer exists, the pointer path is `STR-003`, the owner file exists, and no
  surface other than the owner contains the owner's decision table. Both sides are asserted in one case so a
  one-sided landing cannot pass (FR-018, FR-019, FR-020, FR-021).
- **C-040**: The guard MUST include a red leg per surface: deleting the title from any one of the six
  surfaces makes the corresponding case fail. The mutation MUST be exercised by a test-level probe (a
  doctored in-memory copy), not by editing the real files (FR-018, FR-019, FR-020).

## Mutation Legs

| Leg | Mutation | Must fail |
|-----|----------|-----------|
| M-10 | Remove the title from `templates/constitution-template.md` only | C-025, C-034, C-039 |
| M-11 | Remove the section from `.specify/instructions.md` only | C-030, C-036, C-039 |
| M-12 | Paste the owner's decision table into the live constitution block | C-028, C-039 |
| M-13 | Drop the twelfth MUST-include entry | C-033, C-034 |
| M-14 | Hand-edit the live instructions file instead of regenerating it | C-032 |
| M-15 | Leave the live version at `1.16.0` | C-029, C-035 |
