# Contract — State Vocabulary and Transitions

**Status**: designed (this stage); implemented by `/speckit.implement`
**Owner of every literal below**: `shared/workflow/acceptance-hardening.md` (§ Feature Status / § Verification Vocabulary / § Gates). This contract states **which carrier must contain which value** and **which guard must change**; it does not create a second definition point.

## The four `blocked` literals are four unrelated facts (Assumptions A5)

- **SV-01**: The character sequence `blocked` appears in four independent closed sets with four owners, and this feature MUST treat them as unrelated: feature status `Blocked` (owner `templates/feature-details-template.md` § Canonical Status State Machine), verification status `blocked` (owner `templates/verification-log-template.md`), line state `blocked` (owner `skills/external/sdd-loop-driver/scripts/line-registry.py`), and the task dependency tag `[blockedBy: …]` (owner `templates/tasks-template.md` — a **tag**, not a state). No third meaning may be introduced.
- **SV-02**: The reconciliation of the four literals MUST be written once, in the owner document, and MUST NOT be restated in any of the four carriers.

## Feature status (`Blocked`) — SM-1

- **SV-03**: `templates/feature-details-template.md` § Canonical Status State Machine MUST carry the `Blocked` row set as defined by the schema owner `shared/workflow/acceptance-hardening.md` § Feature Status ([[STR-017]]) — including the explicit **illegal** `Blocked → Ready for Review` — and MUST express `Planned → Implemented` as four conjunctive conditions. This contract designates no row set of its own, and neither does `data-model.md` § E-8: both point at the owner and MUST NOT restate the `From | To | Allowed | Condition` rows.
- **SV-04**: The `Implemented → Blocked` transition MUST be permitted only as an audit correction and MUST require cited evidence; every other backward transition remains illegal, and the never-regress rule carries exactly that one narrow exception.
- **SV-05**: The `Implemented → Ready for Review` gate MUST state its fourth condition (no `final`-path SC in `blocked`/`deferred`/`fail` without an explicit **user** waiver) **in that owner block only**; `/speckit.review`, `/speckit.checklist` and `shared/workflow/feature-integration.md` § Pre-Status-Flip Gate MUST reference the block and MUST NOT restate the condition.
- **SV-06**: `templates/feature-index-template.md` and `skills/internal/manage-features/SKILL.md` MUST each carry `Blocked` in their own status vocabulary; neither may point at another file *instead of* carrying the value, because each is the vocabulary of a distinct consumer (index row / management skill). Measured state recorded so the obligation is not read as an insertion: `templates/feature-index-template.md` is a 21-line file whose only status surface is the `Status` **column header** of its index table — it carries **no value-domain list** today, so its obligation is to **add** a closed status vocabulary containing `Blocked`, not to insert one value into an existing list. The transition rows and the row-level semantics stay with the owner named in SV-03.
- **SV-07**: A waiver of the fourth condition MUST be a user-authored artifact or the user's own ruling; a driver's or agent's confirmation, and the absence of objection, are never waivers.

## Verification vocabulary — SM-3

- **SV-08**: `templates/verification-log-template.md` MUST declare the six-value set `pass` / `fail` / `partial` / `blocked` / `deferred` / `unknown` and MUST distinguish `blocked` from `deferred` in one sentence each (feature not acceptable vs feature still acceptable on a `supporting` path).
- **SV-09**: The same file MUST carry the five ladder fields under their `SC-NNN_`-prefixed names (`SC-NNN_blocked_at`, `SC-NNN_reduced_measurement`, `SC-NNN_reduced_measurement_run`, `SC-NNN_why_reduced_insufficient`, `SC-NNN_unblock`) and the illegal-row rule, whose trigger is mechanical: `SC-NNN_reduced_measurement` non-empty AND `SC-NNN_reduced_measurement_run=no`.
- **SV-10**: The same file MUST carry the three-field smoke record (command / exit code / evidence path) and the "exactly one per feature" rule.
- **SV-11**: No gate, DoD row or task row MAY narrow the vocabulary to a subset of the six values.

## Line state (`blocked`) — SM-2

- **SV-12**: `skills/external/sdd-loop-driver/scripts/line-registry.py` `STATE_VALUES` MUST become eight values with `blocked` added; `ACTIVE_STATES` and `HOLDING_STATES` MUST stay unchanged.
- **SV-13**: The eight dispositions are owned by `requirements.md` § Assumptions A6 items 1–8; their implementation lands in `skills/external/sdd-loop-driver/scripts/line-registry.py` and each one MUST be pinned by at least one assertion in `tests/contract/test_line_state_blocked.py` — including the invariant that `state=blocked` with `merge_ready=true` is rejected, and that the terminal guard set stays three-valued. Neither `data-model.md` § E-9 nor `plan.md` § D6 restates the dispositions: E-9 keeps only the entity boundary, and D6 keeps only the landing map (which symbol/guard each A6 item touches, with the measured line numbers).
- **SV-14**: The `blocked` transfer MUST release the lease and clear `holder_line_id` / `waiting_reason` / `queued_at`, mirroring the `closed` cleanup; a `blocked` line MUST NOT hold a reservation or an ownership claim.
- **SV-15**: Recovery MUST be `update --state active` with a recorded unblock reason, and it MUST still pass the ownership gate; `promote-waiting` and the `integration-*` actions MUST remain unreachable from `blocked`.
- **SV-16**: `stale_from_state` MUST be documented and tested as able to carry `blocked`; no enum expansion is introduced for it.
- **SV-17**: No line-level never-regress rule may be added by this feature.

## Traceability

| FR | Clauses | Test |
|---|---|---|
| FR-001 | `contracts/artifact-schemas.contract.md` AS-01…AS-04 (the `Path` marker); no clause here | `tests/contract/test_requirements_checker.py` |
| FR-002 | SV-03 | `tests/contract/test_acceptance_state_machine.py` |
| FR-003 | SV-03, SV-04 | `tests/contract/test_acceptance_state_machine.py` |
| FR-004 | SV-08, SV-09, SV-11 | `tests/contract/test_acceptance_state_machine.py`, `test_closure_acceptance_check.py` |
| FR-016 | SV-05, SV-07 | `tests/contract/test_acceptance_state_machine.py` |
| FR-017 | SV-12…SV-17 | `tests/contract/test_line_state_blocked.py` |
| FR-018 | SV-06, SV-04 | `tests/contract/test_acceptance_state_machine.py` |
| FR-019 | SV-01, SV-02 | `tests/contract/test_acceptance_state_machine.py::test_the_four_blocked_literals_stay_four` |
