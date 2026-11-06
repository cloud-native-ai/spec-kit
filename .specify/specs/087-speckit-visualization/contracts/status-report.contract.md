# Contract: Status Report (content, attribution, carrier, cadence profile)

**Feature**: 087 | **Covers**: FR-003, FR-004, FR-007, FR-014, FR-015, FR-020
**Contract object**: the shape of one emitted status line and the rules that decide *when* and *where* it lands.
This contract is consumed by `data-model.md` E2 and E6 and judged by `status-digest.py --action guard` plus the
contract test.

Clause ids are dense (`SR-01`…`SR-10`) and are cited verbatim by `/speckit.tasks`.

---

## C-22 · SR-01 — Attribution is mandatory and unambiguous

Every status line MUST name the emitting **structure identity**: the structure slug and the run stamp. Two
structures MUST NOT be able to produce a byte-identical unattributed line — the attribution fields are what make
interleaved lines in one session distinguishable (`FR-007`, `requirements.md` Edge Cases "Several teams in one
session").

The run stamp is the one the emitting flow already writes (team run report filename stamp, or the registry
`run_id`); no new stamp format is introduced.

*Judged by*: guard proposition RO-05 over a captured line set; contract test asserts a two-structure fixture yields
two distinguishable lines.

Requirements served: (FR-007).

## C-23 · SR-02 — The four content elements, reached by reference

Every line MUST carry the four elements named in
`shared/guidelines/progress-reporting.md` § 汇报内容下限: position, delta, remainder (with a rough estimate or the
stated reason none can be given), and blocker status. When there is no blocker the line MUST write the explicit
negation (`no blocker` / `无阻塞`) — an absent blocker field is a defect, not an empty value.

This contract names the elements as labels; it MUST NOT restate the owner's descriptions of them.

*Judged by*: guard proposition RO-05 over a captured line set (four labels present, blocker present).

Requirements served: (FR-004, FR-013).

## C-24 · SR-03 — Cadence: the long-run default, overridable per run and per structure

A structure whose E6 `long-run.condition` holds MUST emit at the long-run default cadence; the value MUST be read
from the owner document, never restated in the emitting flow (`FR-003`). An explicit per-run or per-structure value
MAY replace it without a source edit; when present it MUST be recorded next to the line's profile so a reader can
tell an override from the definition.

*Judged by*: guard proposition RO-03 and RO-09 (the value is read from the owner, and the override is recorded next
to the line's profile).

Requirements served: (FR-003).

## C-25 · SR-04 — Two out-of-cadence triggers are legal, and neither resets the cadence

1. A **stage boundary** crossed between two ticks emits an extra line at the boundary; the periodic cadence MUST NOT
   be restarted by it (`requirements.md` US1 AS2).
2. A **significant transition** (sub-flow failure, stall crossing, dispatch failure) emits before the next tick
   (`FR-010`); see `contracts/supervision-report.contract.md` MV-03.

A tick that falls inside an indivisible step is delivered at that step's next boundary **with the delay stated**;
the step MUST NOT be split to keep the clock (`progress-reporting.md` § 不打断原子步骤).

*Judged by*: guard proposition RO-08 (the line set contains both trigger kinds and their stamps show the cadence was
not reset).

Requirements served: (FR-010).

## C-26 · SR-05 — The carrier is recorded, and exactly one of two forms is legal

Every emitting run MUST record which carrier actually received its lines, in the run record the flow **already
writes** (team run report, dispatch record, or supervision record). The carrier value is exactly one of:

- `console` — the host conversation surface the user is watching, or
- the path of the flow's declared stream artifact (the triplet's `.live.log`), when no live console exists.

No third carrier and no newly persisted per-line artifact is permitted (`FR-007`, `FR-014`, `requirements.md`
Out of Scope "Requiring a status line to be persisted as an artifact of its own").

*Judged by*: guard proposition RO-12 and `contracts/ownership-map.contract.md` OM-03 (C-49).

Requirements served: (FR-007, FR-014).

## C-27 · SR-06 — Every execution mode is covered, and the mode is recorded

The obligation binds native, virtual and external execution equally. The run record MUST name the execution mode
and the carrier together, so a reader can tell that the mode's surface was the one used. No mode MUST be left with
neither a live surface nor a declared stream artifact (`SC-004`).

**Premise the test rests on**: mode 2 (virtual) is inline in the visible session and therefore reports through
`console`; mode 3 (external) reports through the triplet's `.live.log` unless a host console is attached. The
contract asserts those two mappings and asserts that mode 1 records `console`.

*Judged by*: `tests/contract/test_reporting_obligations.py` over a three-mode fixture.

Requirements served: (FR-014, SC-004).

## C-28 · SR-07 — A status line is a statement, never a gate

A line MUST NOT contain a question, an approval request, or a waiver solicitation, and emitting one MUST NOT be
treated as authorization for any action (`FR-015`). Destructive actions keep their own front-loaded criterion at
`shared/guidelines/confirmation-gates.md` — reached by path, not restated.

*Judged by*: guard proposition RO-10 — a line set containing an interrogative or an approval verb is red.

Requirements served: (FR-015).

## C-29 · SR-08 — A reporting failure emits a line of its own

When the reporting loop cannot emit at its expected tick, the flow MUST surface that as a named condition
(`trigger: reporter-failure`) rather than falling silent (`FR-016`). The line MUST state what failed and MUST NOT
claim the run is healthy. "No line" is never readable as "progressing".

*Judged by*: guard proposition RO-11 over a fixture whose second tick was suppressed.

Requirements served: (FR-016).

## C-30 · SR-09 — Two profiles, one condition, one selected per run

Each line MUST carry the profile in force (`long-run` or `interactive`). The condition selecting the profile is
E6's; a run MUST NOT mix the two profiles' ticks as if they were one cadence. A mid-run loss of the live receiver
switches to `interactive` at the next boundary **and says so**; the switch is recorded, never silent
(`FR-020`, `requirements.md` Edge Cases "Two cadence profiles in one session").

*Judged by*: guard proposition RO-09 over a fixture that loses its receiver mid-run.

Requirements served: (FR-020).

## C-31 · SR-10 — Every line is readable by a reader who did not take part in the run

A line MUST NOT carry an internal engine identifier where a user-facing name exists (a state spine path, an
internal status code, an engine action name). It MUST carry the facts a reader needs in order to act, and MUST
reach everything else by path reference. The governing discipline is
`shared/guidelines/user-facing-comprehension.md` — reached by path, not restated.

*Judged by*: `tests/contract/test_reporting_obligations.py` — a deny list of internal identifiers over a fixture
line set.

Requirements served: (FR-015).
