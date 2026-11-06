# Contract: Supervision Report and the Coaching Payload Amendment

**Feature**: 087 | **Covers**: FR-008, FR-009, FR-010, FR-013, FR-019
**Contract object**: (a) the master-reporting duty's content over `skills/external/coaching-skills/SKILL.md`
§ Dispatch Payload and over any supervising master; (b) the closed-set amendment to that payload.

Clause ids are dense (`MV-01`…`MV-09`) and are cited verbatim by `/speckit.tasks`.

---

## C-32 · MV-01 — The duty is over sub-flows, not over the master

A supervising report MUST describe **every dispatched sub-flow**, not the master's own progress alone. The report
MUST name each sub-flow's identity, its state, and the age of its last observed activity (`FR-008`).

The duty's owner is `shared/guidelines/reporting-obligations.md` (C-06, C-07, C-08). This contract fixes the shape
the shipped example demonstrates; it MUST NOT become the definition of the duty.

*Judged by*: guard proposition RO-06 over a two-sub-flow fixture.

## C-33 · MV-02 — Presence is a closure requirement

Every dispatched sub-flow MUST appear in the master's report **at least once** per cadence tick while it is
dispatched. A sub-flow omitted from a tick is a defect named by its label — an omission is not a sampling decision
(`requirements.md` US2 AS1). When a sub-flow completes between ticks it still appears in the tick that observes the
completion (as `completed`), and only then MAY leave the active set.

*Judged by*: guard proposition RO-11 over a fixture where one of two sub-flows finishes mid-interval.

## C-34 · MV-03 — A significant transition reports before the clock

A sub-flow failure, a stall crossing and a dispatch failure each MUST produce a report **before** the next tick
(`FR-010`). The report MUST identify the sub-flow's label and the transition, and MUST NOT wait for the cadence.

*Judged by*: guard proposition RO-08 over a fixture whose sub-flow exits non-zero at t = 40 % of the interval.

## C-35 · MV-04 — Stall versus slow, with the threshold named

Each judgement MUST state which declared threshold row it used and the measured silence. A sub-flow below the
threshold is reported as **slow** (a qualifier on `running`), not as `stalled`, and a sub-flow beyond it is
`stalled` — the two MUST NOT be merged (`FR-009`, `requirements.md` Edge Cases "Stall versus slow").

The numeric values MUST come from `skills/internal/create-team/references/patterns.md` § Monitoring → **Stall
Detection** at render time; this contract carries no number.

*Judged by*: guard proposition RO-07 and `tests/contract/test_coaching_reporting_duty.py` (a fixture pair at
just-under and just-over the threshold yields `slow` and `stalled`).

## C-36 · MV-05 — The coaching skill's single dispatch is in scope and named

`skills/external/coaching-skills` dispatches exactly one subagent per run. Its report MUST name that one Trainee
dispatch with its state and age — not an empty set and not merely the coach's own progress
(`requirements.md` A9, Edge Cases "A single-dispatch supervisor judged against the predicate").

*Judged by*: `tests/contract/test_coaching_reporting_duty.py` asserts the skill's report section names the Trainee
dispatch as the reported sub-flow.

## C-37 · MV-06 — The payload's closed field set gains EXACTLY one field

`skills/external/coaching-skills/SKILL.md` § Dispatch Payload MUST gain exactly one row:

| Field | Content | Rule |
|-------|---------|------|
| `reporting-cadence` | the tick value in force for this run, plus the attribution pair (structure slug + run stamp) the subordinate's own lines must carry | the value is the resolved profile's cadence; the subordinate reports its own progress on it and the coach reports the subordinate's state on it |

The preamble clause "the payload is a closed field set; anything not listed below is forbidden" MUST remain in
place, unchanged. The set is **extended, never widened** — no "any reporting field" allowance is introduced
(`FR-019`).

*Judged by*: `tests/contract/test_coaching_dispatch_contract.py` (its `REQUIRED_FIELDS` tuple gains the new name in
the same change) plus `tests/contract/test_coaching_reporting_duty.py` (the preamble still forbids unlisted fields).

## C-38 · MV-07 — One added forbidden-content class and one added return-handling clause

The forbidden-content list MUST gain: the coach's own status lines or the expected subordinate-state conclusions
(the subordinate must not be told what its state will be judged as). The return contract MUST gain: the
subordinate's own reported state at return, so the coach can cite it as `self-report` rather than infer it.

Both MUST be additions; no existing forbidden class and no existing return-contract item is removed or weakened.

*Judged by*: `tests/contract/test_coaching_reporting_duty.py` asserts the four pre-existing forbidden classes are
still present plus the new one, and that the return contract still names every pre-existing item.

## C-39 · MV-08 — The example demonstrates the duty; the owner document defines it

`coaching-skills/SKILL.md` MUST reference `shared/guidelines/reporting-obligations.md` for the duty's definition and
MUST NOT restate the scope predicate, the cadence default, the threshold numbers or the transition classes. A
restatement inside the skill is a defect, because it would make the shipped example a second definition of the
obligation (`FR-013`, `FR-019`).

*Judged by*: `tests/contract/test_coaching_reporting_duty.py` — a scan over the skill for the owner's exclusive
literals (the cadence value and the threshold numbers) must find zero hits.

## C-40 · MV-09 — Any supervising master carries the same duty through the same payload channel

A flow that dispatches and watches sub-flows without being a team does not need a new mechanism: it carries the
same obligation by injecting the reporting duty into its dispatch payload, exactly as the fast-fail clause is
injected (`shared/definitions/subagent-definitions.md` § Dispatch-Time Governance Obligation, reached by reference).
`shared/workflow/external-dispatch-recipes.md` gains **one pointer line** to the new owner; its recipes are
unchanged.

*Judged by*: `tests/contract/test_reporting_obligations.py` asserts both files carry the pointer and that the
recipes' command shapes are unchanged from the pre-change baseline.
