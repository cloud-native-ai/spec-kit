# Contracts: Status-gate ownership and severity separation (C-45…C-54)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner**: this file owns the single-owner rule for the `Implemented → Ready for Review` transition, the content that owner row must carry, the convergence of the duplicate summary row, and the prohibition on vocabulary mapping. It does not own the two severity vocabularies themselves, and it does not re-state the transition's criteria — the owner row it names does.
**Pinned by**: `tests/contract/test_status_gate_owner.py` (plus the updated pin in `tests/contract/test_review_p1_review_loop.py`, disclosed in `research.md` § R5)
**Measures**: SC-004

**C-45**: The normative statement of the `Implemented → Ready for Review` gate is owned by `templates/feature-details-template.md` § Canonical Status State Machine — the section that declares itself the authoritative transition table. No other file carries a second criteria wording for that transition (FR-008).

**C-46**: That owner row carries three conjunctive conditions: every deferred `[~]` task is resolved or explicitly waived; review evidence has been produced; and the current code-segment record contains no `blocking` entry. The third condition is an **existence** test over the current [[STR-004]] only: at least one `blocking` heading blocks, and a later run whose record carries zero `blocking` no longer blocks. No "clearing" action and no "cleared" state exists, so no artifact explains how an entry becomes cleared, and a run that merely rewrites the record is the whole of the mechanism. The condition is judged by reading the six-level vocabulary directly — relabelling it as `P0`/`P1`/`P2` before judging is forbidden, because a relabel is a second vocabulary and the mapping does not exist (FR-008, SC-004).

**C-47**: The `/speckit.review` summary row in `shared/workflow/feature-integration.md` § Status State Machine becomes a reference to the owner row: it names the transition, names the owner section, and states that the criteria are not restated there. The duplicated wording is removed rather than reworded to agree (FR-008).

**C-48**: The gate is a property of the transition, not of one command: every path that initiates this transition cites the same owner criterion and MUST NOT carry its own copy of the conditions. `/speckit.review` is an unconditional initiator. `/speckit.checklist`'s same-named row is a **conditional** initiator: it initiates the transition only when the checklist runs after `/speckit.implement`, and then it cites the same owner criterion; when it runs before implement it initiates nothing, MUST NOT error for the absence of a code-segment conclusion, and MUST NOT manufacture one (FR-008).

**C-49**: With only `important` items open and none of them `blocking`, the transition is allowed and each `important` item must be answered. `suggestion`, `nitpick`, `question`, and `praise` never block the transition (FR-008, SC-004).

**C-50**: This feature introduces no numeric conversion, mapping matrix, or unified score between the process severity vocabulary and the code severity vocabulary. A request to relabel the six-level set as `P0`/`P1`/`P2` is rejected by this specification, and no artifact of this feature provides a place to store such a mapping (FR-007).

**C-51**: A waiver of a `blocking` entry is accepted only from an explicit user ruling — a user-authored waiver artifact, or the user's own ruling in the session. A driver's or orchestrator's confirmation is an agent's confirmation and MUST NOT be read as a user ruling. The agent MUST NOT downgrade, merge, or exclude a `blocking` entry inside the gate judgement. The unattended disposition is **halt-and-report**: the command stops before the transition, reports the block, and records [[STR-010]] as the named refusal literal in the process report's code subsection and in the conclusion it returns. It MUST NOT infer a waiver from the absence of objection, and MUST NOT leave the status at `Implemented` while presenting the run as a completed review (FR-009).

**C-52**: [[STR-001]] and [[STR-002]] do not block the transition, but each MUST be disclosed on both verifiable carriers: the process report's code subsection and the feature detail's `## Latest Review` review-record entry. The closing summary MAY restate it and carries no obligation of its own. A silent non-conclusion is the failure this clause prevents (FR-008, FR-019).

**C-53**: A refused transition leaves the status at `Implemented` and writes the refusal reason into both carriers — the report's code subsection and the feature detail's review-record entry. The reason names the condition that failed: a `blocking` entry in the current code-segment record, missing review evidence, or unresolved deferred tasks — not merely that the transition was refused (FR-008).

**C-54**: The transition is judged once, after both segments have finished and both artifacts are on disk. Because the code segment's conclusion is one of the inputs, the status MUST NOT flip before the code segment completes; an early flip is a violation even when the process segment already passed (FR-008).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-45 | FR-008 | — | state-machine owner + integration protocol |
| C-46 | FR-008 | SC-004 | state-machine owner |
| C-47 | FR-008 | — | integration protocol + pin update |
| C-48 | FR-008 | — | integration protocol (both initiators, checklist conditional) |
| C-49 | FR-008 | SC-004 | state-machine owner |
| C-50 | FR-007 | — | command + owner |
| C-51 | FR-009 | — | owner + report + returned conclusion |
| C-52 | FR-008, FR-019 | — | report + feature detail |
| C-53 | FR-008 | — | report + feature detail |
| C-54 | FR-008 | — | command |

## Amendment log — remediation round 1 (2026-10-27)

Trigger: `test-evidence/analyze-report.md` (`GATE: CRITICAL=0 HIGH=6`) and `notes/remediation-round-1.md`. Clause ids are unchanged; no obligation was dropped.

| Clause | Change | Why (finding) |
|--------|--------|---------------|
| C-46 | the third condition becomes an existence test over the current record; "unresolved"/"cleared" removed | A-05 |
| C-48 | `/speckit.checklist` is named a **conditional** initiator, with its before-implement behaviour stated | A-18 |
| C-51 | unattended disposition = halt-and-report with [[STR-010]]; a driver confirmation is not a user ruling | A-19 |
| C-52 | the three disclosure places become the two verifiable carriers | A-01 |
| C-53 | refusal reason lands on both carriers, and the named failing conditions lose "unresolved" | A-01, A-05 |
