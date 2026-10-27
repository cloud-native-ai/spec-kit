# Contracts: Status-gate ownership and severity separation (C-45…C-54)

**Requirement → Feature**: `071-review-code-integration` → Feature 071 Review 命令与代码评审技能的组合与治理
**Owner**: this file owns the single-owner rule for the `Implemented → Ready for Review` transition, the content that owner row must carry, the convergence of the duplicate summary row, and the prohibition on vocabulary mapping. It does not own the two severity vocabularies themselves, and it does not re-state the transition's criteria — the owner row it names does.
**Pinned by**: `tests/contract/test_status_gate_owner.py` (plus the updated pin in `tests/contract/test_review_p1_review_loop.py`, disclosed in `research.md` § R5)
**Measures**: SC-004

**C-45**: The normative statement of the `Implemented → Ready for Review` gate is owned by `templates/feature-details-template.md` § Canonical Status State Machine — the section that declares itself the authoritative transition table. No other file carries a second criteria wording for that transition (FR-008).

**C-46**: That owner row carries three conjunctive conditions: every deferred `[~]` task is resolved or explicitly waived; review evidence has been produced; and the code segment records no unresolved `blocking` item. The third condition is judged by reading the six-level vocabulary directly — relabelling it as `P0`/`P1`/`P2` before judging is forbidden, because a relabel is a second vocabulary and the mapping does not exist (FR-008, SC-004).

**C-47**: The `/speckit.review` summary row in `shared/workflow/feature-integration.md` § Status State Machine becomes a reference to the owner row: it names the transition, names the owner section, and states that the criteria are not restated there. The duplicated wording is removed rather than reworded to agree (FR-008).

**C-48**: The gate is a property of the transition, not of one command. Every path that initiates this transition — including `/speckit.checklist`'s same-named row — cites the same owner criterion and MUST NOT carry its own copy of the conditions (FR-008).

**C-49**: With only `important` items open and none of them `blocking`, the transition is allowed and each `important` item must be answered. `suggestion`, `nitpick`, `question`, and `praise` never block the transition (FR-008, SC-004).

**C-50**: This feature introduces no numeric conversion, mapping matrix, or unified score between the process severity vocabulary and the code severity vocabulary. A request to relabel the six-level set as `P0`/`P1`/`P2` is rejected by this specification, and no artifact of this feature provides a place to store such a mapping (FR-007).

**C-51**: A waiver of an unresolved `blocking` item is accepted only from an explicit user ruling. The fact of the waiver is written into the review report and into the feature detail, and the agent MUST NOT downgrade, merge, or exclude a `blocking` item inside the gate judgement (FR-009).

**C-52**: [[STR-001]] and [[STR-002]] do not block the transition, but each MUST be disclosed in three places: the process report's code subsection, the closing summary, and the feature detail's review-record row. A silent non-conclusion is the failure this clause prevents (FR-008, FR-019).

**C-53**: A refused transition leaves the status at `Implemented` and writes the refusal reason into the report's code subsection and into the closing summary. The reason names the condition that failed — unresolved `blocking` items, missing review evidence, or unresolved deferred tasks — not merely that the transition was refused (FR-008).

**C-54**: The transition is judged once, after both segments have finished and both artifacts are on disk. Because the code segment's conclusion is one of the inputs, the status MUST NOT flip before the code segment completes; an early flip is a violation even when the process segment already passed (FR-008).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-45 | FR-008 | — | state-machine owner + integration protocol |
| C-46 | FR-008 | SC-004 | state-machine owner |
| C-47 | FR-008 | — | integration protocol + pin update |
| C-48 | FR-008 | — | integration protocol (both initiators) |
| C-49 | FR-008 | SC-004 | state-machine owner |
| C-50 | FR-007 | — | command + owner |
| C-51 | FR-009 | — | owner + feature detail |
| C-52 | FR-008, FR-019 | — | report + summary + feature detail |
| C-53 | FR-008 | — | command + summary |
| C-54 | FR-008 | — | command |
