# Contract: Reporting Obligations (the owner document)

**Feature**: 087 | **Covers**: FR-001, FR-002, FR-003, FR-004, FR-013, FR-014, FR-015, FR-016, FR-018, FR-020, FR-021
**Contract object**: the normative content of `shared/guidelines/reporting-obligations.md` (framework source) and its
mirror `.specify/shared/guidelines/reporting-obligations.md`. Clauses are judged by reading the delivered owner
document and, where a clause says "MUST", by the guard `status-digest.py --action guard`.

Clause ids are dense (`RO-01`…`RO-13`) and are cited verbatim by `/speckit.tasks`. A clause that the guard cannot
decide states that explicitly and names the reading surface instead.

---

## C-01 · RO-01 — The document declares itself the single owner of exactly five facts

The owner MUST open with a single-source-of-truth declaration naming the five facts it owns and no others:

1. the obligation's **scope predicate** (RO-02),
2. the **long-run cadence default** (RO-03),
3. the **reporter-seat obligation** (RO-04),
4. the **master-reporting duty and the stall judgement reference** (RO-06),
5. the **digest contract** (RO-09).

The declaration MUST name what it explicitly does **not** own, with the owner path for each: the cadence anchor,
content floor, deferral rule and interactive default (`shared/guidelines/progress-reporting.md`); the artifact
triplet and execution modes (`shared/definitions/subagent-definitions.md`); the stall threshold numbers
(`skills/internal/create-team/references/patterns.md`); the registry state vocabulary
(`skills/external/sdd-loop-driver/scripts/line-registry.py`).

*Judged by*: guard proposition RO-01.

## C-02 · RO-02 — Scope is a decidable predicate

The owner MUST state scope as a predicate that two independent readers apply to one flow and reach the same
verdict:

> A flow is **in scope** when it dispatches two or more concurrent units, **or** holds one or more asynchronous
> delegations that it continues past their dispatch.

MUST additionally state: a single synchronous step is out of scope; an out-of-scope flow MAY say so in one line
rather than emitting an empty report; and no per-flow exempt roster is maintained (`requirements.md` A3, A9).

*Judged by*: guard proposition RO-02 over a seeded flow sample.

## C-03 · RO-03 — The long-run cadence default has exactly one definition site

The owner MUST contain the long-run profile's default value as a literal **once**, and MUST state that the value is
overridable per run and per structure without a source edit (`FR-003`). No other framework-source file may carry an
*interval definition* of this value; the only other legal occurrences are a user-supplied value for one run and a
dated record (`SC-006`).

*Judged by*: guard proposition RO-03 (owner-literal scan) — the scan MUST report exactly one definition site and
MUST fail when a second is seeded.

## C-04 · RO-04 — The reporter-seat obligation and its two escape paths

The owner MUST state: every team created through the framework's team-creation entry carries exactly one reporter
seat bound to the shipped reporting template, with the reporter's territory declared; a missing seat is a **named
defect** naming the seat; and exactly two escape paths exist, each requiring a recorded reason — the roster-level
reason (`FR-006`) and the runtime-omission condition (`FR-021`: all lanes executed by the current session and the
whole run expected to finish inside one cadence interval, in which case the orchestrating session carries the duty
itself).

*Judged by*: guard proposition RO-04 (roster read + named defect) and `contracts/reporter-seat.contract.md`.

## C-05 · RO-05 — Every report carries the four content elements by reference

The owner MUST require the four content elements (position, delta, remainder, blocker status with `no blocker`
written explicitly) **by section anchor** to
`shared/guidelines/progress-reporting.md` § 汇报内容下限, and MUST NOT restate the element definitions. The owner
MAY name the elements as a list of labels, because a consumer that cannot name what it must emit cannot comply.

*Judged by*: guard proposition RO-05 (the owner contains the anchor and contains no copy of the element
descriptions).

## C-06 · RO-06 — The master-reporting duty, stated over every dispatched sub-flow

The owner MUST state: a supervising flow reports **every** dispatched sub-flow at least once per cadence tick, with
each sub-flow's identity, its state (running / completed / stalled / failed), and the age of its last observed
activity (`FR-008`); and that a flow which dispatches exactly one subordinate per run is in scope and names that one
subordinate rather than reporting an empty set.

*Judged by*: guard proposition RO-06 and `contracts/supervision-report.contract.md` MV-01, MV-02.

## C-07 · RO-07 — Stall judgement references one declared threshold table

The owner MUST require the stall judgement to be made against a **declared** threshold and MUST reach the numbers
by path plus anchor to `skills/internal/create-team/references/patterns.md` § Monitoring → **Stall Detection**. It
MUST state that "slower than the threshold" and "stalled" are distinguished, and that the report names which
threshold row the judgement used (`FR-009`). The owner MUST NOT define a second numeric threshold set.

*Judged by*: guard proposition RO-07 (owner carries the anchor and zero numeric duration literals attributable to
this judgement).

## C-08 · RO-08 — Out-of-cadence reporting on a significant transition

The owner MUST require an immediate report — before the next tick — when the supervising flow observes a sub-flow
failure, a stall crossing, or a dispatch failure (`FR-010`), and MUST state that the transition never waits for the
clock.

*Judged by*: guard proposition RO-08 (owner text names all three transition classes).

## C-09 · RO-09 — The digest contract, by shape

The owner MUST define the digest's contract as: one bounded summary of active lines and their states, dispatched
agents with last-observed activity and its age, and the most recent completions; read from state artifacts, never
requiring a reporter process to be alive; stale entries marked with their age; an explicit "nothing running" state;
and a declared entry cap with the omitted count stated on truncation (`FR-011`, `FR-012`). The owner MUST name the
command and script that provide it once the plan fixes them, and MUST NOT describe a second renderer.

*Judged by*: guard proposition RO-09 and `contracts/status-digest.contract.md`.

## C-10 · RO-10 — Reporting is a one-way statement

The owner MUST state that a status report never awaits a response, never becomes an approval request, and that its
presence authorizes no action (`FR-015`), and MUST point at
`shared/guidelines/confirmation-gates.md` for the gate discipline rather than restating it.

*Judged by*: guard proposition RO-10 (owner text + the pointer's resolvability).

## C-11 · RO-11 — A reporting failure is surfaced, not swallowed

The owner MUST require that a run whose reporting loop cannot emit surfaces that as a named condition, and MUST
state that absence of a line is never readable as health (`FR-016`). The owner MUST state that a **stalled
reporter** is detected by the orchestrator's existing liveness signal and threshold table, not by a second
detector (`requirements.md` A15).

*Judged by*: guard proposition RO-11.

## C-12 · RO-12 — The duty holds in every execution mode, with the already-declared carrier

The owner MUST state that the obligation binds all three execution modes of
`shared/definitions/subagent-definitions.md` § Three Execution Modes equally; that a mode without a native live
surface uses its already-declared stream carrier; that the run record names the mode and the carrier; and that no
fourth mode and no second carrier is introduced (`FR-014`).

*Judged by*: guard proposition RO-12.

## C-13 · RO-13 — Zero new machinery, stated as a prohibition the guard checks

The owner MUST state, in one clause: no scheduler, no timer service, no daemon, no third-party dependency, no new
persistent store, no new console channel, no second registry, no second state spine, no ledger (`FR-018`). The
clause MUST be phrased as a prohibition the changed-file audit can test, not as an aspiration.

*Judged by*: guard proposition RO-13 plus `contracts/ownership-map.contract.md` OM-05.
