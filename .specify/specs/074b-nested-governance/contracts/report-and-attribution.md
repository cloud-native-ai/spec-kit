# Contracts: Report section and Goal attribution (C-21…C-30)

**Requirement → Feature**: `074b-nested-governance` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the one mandatory section added to the team run-report contract and the
attribution boundary between a nested run and the Goal layer. The report contract is owned by
`skills/internal/create-team/SKILL.md` § Report contract and is amended once, in place; the Goal,
Target and Goal–Team binding model is owned by `shared/definitions/goal-definitions.md` and is only
referenced; the handoff field set is owned by
`skills/external/sdd-loop-driver/references/nested-invocation.md` (delivered by `074a`).
**Pinned by**: `tests/contract/test_nested_run_report.py` (planned)
**Measures**: SC-002
**Parent source**: `parent C-47`, `parent C-48`, `parent C-49`, `parent C-50`, `parent C-51`,
`parent C-52`, `parent C-53`, `parent C-54` (report-section facet); `parent C-41` is cited
(delivered by `074a`).

**C-21**: The team run-report contract gains exactly one mandatory section, whose heading literal is
`[[STR-007]]`, stated verbatim. The section is mandatory for every run, in both bounded and continuous
patterns, and its addition does not rename, merge, or reorder any existing mandatory section — the
existing list stays in its existing order with the new heading appended (FR-002). *(parent C-47)*

**C-22**: The section lists, per invocation: an outcome value of `[[STR-004]]`, `[[STR-005]]`, or
`[[STR-006]]`; the artifact paths; the evidence paths; the routing-verdict reference; and the
anomalies. Paths are carried as paths — the section never inlines artifact bodies, and never
summarizes a blocked or failed run into a successful-sounding sentence (FR-002). *(parent C-48)*

**C-23**: A run with no nested invocation MUST state that explicitly inside the section rather than
omitting the section. An omitted section is a contract violation even when the correct content would
have been "none" (FR-002). *(parent C-49)*

**C-24**: The team supervisor is the sole writer of the section and of every other tracked artifact in
the run. A nested run writes no tracked artifact: no report edit, no goal-archive write, no
spec-directory write. Its product is the returned handoff, consumed by the supervisor (FR-001).
*(parent C-50)*

**C-25**: At report time the team supervisor appends exactly one ledger item carrying the existing
Target reference, using the ledger's existing attribution field. On each of these the section is a
consumer, not an owner: no new Goal field, no structural link from a Goal to a requirements
specification, and no write to the Goal definition (FR-001). *(parent C-51)*

**C-26**: The parsed Goal field set is identical before and after a nested run. Attribution is
observational only: it appears through the existing ledger reference and the run report, never as a
Goal-scoped field, and no Target is invented for a run that declared none — such a run's row omits the
attribution field, which is the existing Goal-wide form (FR-001, SC-002). *(parent C-52)*

**C-27**: The other mandatory report sections keep their existing content obligations. The nested
section is a peer of the verification section, not a replacement: a nested run's own verification
evidence does not discharge the enclosing run's verification duty, and the enclosing run's verification
standard applies unchanged (FR-002). *(parent C-53)*

**C-28**: The routing-verdict reference required per invocation is a **reference** to the verdict
`074a` recorded in the Agent execution evidence; the section carries no re-derived verdict and no copy
of the input set, the verdict table, or the reason-code vocabulary. When the recorded verdict cannot be
located, the section records the reference as missing and the outer layer MUST NOT re-derive it; a
fabricated or re-computed reference is a contract violation (FR-002). *(parent C-54, report-section
facet; D-2)*

**C-29**: The section reads the handoff's closed field set by reference and adds no field of its own: a
field the section lists that the handoff does not carry is recorded as missing, never filled in from
the invoking agent's own prose. A `[[STR-005]]` or `[[STR-006]]` outcome is carried through to the
outer layer unchanged, so a blocked or failed nested run can never be reported as success (FR-002).
*(parent C-41 cited, delivered by `074a`)*

**C-30**: The report contract has exactly one owner (`create-team/SKILL.md` § Report contract); the
`run-team` report duty keeps delegating to it and gains no second statement of the section. This slice
therefore edits one document for this face, and any later reader reaches the obligation at that path
(FR-002).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-21, C-22, C-23, C-27, C-30 | FR-002 | — | `skills/internal/create-team/SKILL.md` § Report contract |
| C-24, C-25, C-26 | FR-001 | SC-002 | supervisor write duty; `shared/definitions/goal-definitions.md` (cited); team ledger `items.jsonl` (cited) |
| C-28, C-29 | FR-002 | — | `skills/external/sdd-loop-driver/references/nested-invocation.md` (cited, `074a`) |
