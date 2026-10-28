# Contracts: Report section and Goal attribution (C-47…C-54)

**Requirement → Feature**: `074-goal-team-sdd-unification` → Feature 074 Goal/Team/Agent 与 SDD 开发流程统一
**Owner**: this file owns the one mandatory section added to the team run-report contract and the
attribution boundary between a nested run and the Goal layer. The report contract is owned by
`skills/internal/create-team/SKILL.md` § Report contract and is amended in place; the Goal,
Target, and Goal–Team binding model by `shared/definitions/goal-definitions.md` and is only
referenced.
**Pinned by**: `tests/contract/test_nested_run_report.py` (planned)
**Measures**: SC-003, SC-008

**C-47**: The team run-report contract gains exactly one mandatory section, `## Nested SDD Runs`,
stated by its verbatim heading literal. The section is mandatory for every run, in both bounded
and continuous patterns, and its addition does not rename, merge, or reorder any existing
mandatory section (FR-021).

**C-48**: The section lists, per invocation: the outcome value, the artifact paths, the evidence
paths, the routing-verdict reference, and the anomalies. Paths are carried as paths — the section
never inlines artifact bodies, and never summarizes a failed run into a successful-sounding
sentence (FR-021, SC-003).

**C-49**: A run with no nested invocation MUST state that explicitly inside the section rather
than omitting the section. An omitted section is a contract violation even when the correct
content would have been "none" (FR-021).

**C-50**: The team supervisor is the sole writer of the section and of every other tracked
artifact in the run. A nested run writes no tracked artifact: no report edit, no goal-archive
write, no spec-directory write. Its product is the returned handoff, consumed by the
supervisor (FR-020).

**C-51**: At report time the team supervisor appends exactly one ledger item carrying the
existing Target reference. The reference uses the ledger's existing attribution field; no new
Goal field, no structural link to a requirements specification, and no write to `goal.md` is
introduced (FR-020, SC-008).

**C-52**: The parsed Goal field set is identical before and after a nested run. Attribution is
observational only: it appears through the existing ledger reference and the run report, never as
a Goal-scoped field, and no Target is invented for a run that declared none (FR-020, SC-008).

**C-53**: The other mandatory report sections keep their existing content obligations. The nested
section is a peer of the verification section, not a replacement: a nested run's own verification
evidence does not discharge the enclosing run's verification duty (FR-021).

**C-54**: The routing verdict required by the routing decision's per-duty application is consumed
by the outer layer through the report section's verdict reference or through the Agent execution
evidence. The two carriers carry a reference to the recorded verdict, never a re-derived one, so
the outer layer reads the same verdict the duty acted on (FR-013, FR-021).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-47, C-48, C-49, C-53 | FR-021 | SC-003 | `skills/internal/create-team/SKILL.md` § Report contract |
| C-50, C-51, C-52 | FR-020 | SC-008 | supervisor write duty; `goal-definitions.md` (referenced) |
| C-54 | FR-013, FR-021 | — | report section § verdict reference |
