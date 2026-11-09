# Contract: The efficiency element on the two visibility surfaces

**Feature**: 088 | **Covers**: FR-023, FR-024, FR-025, SC-011, SC-012
**Contract object**: the one bounded efficiency element a status line and a digest entry each carry per step, the
read-only store access behind it, and the source of its elapsed quantity.

Clause ids continue the feature's dense `C-nn` sequence (`C-63`…`C-71`, in the `EF` family) and are
cited verbatim by `/speckit.tasks`. They add to `C-01`…`C-62` and renumber none of them.

**What this file does not own** — and MUST NOT restate: the surface shapes and their entry bound
(`status-report.contract.md` C-23, `status-digest.contract.md` C-43), the line's attribution (`C-22`), the
digest's cap / staleness / exit statuses (`C-43`…`C-45`), the store's schema, fields, vocabularies and write path
(`shared/declarations/facts/quant-record-schema.yaml` — reached by path and never copied here), and the store's read
path (`scripts/python/exec-quant.py`).

---

## C-63 · EF-01 — Exactly two surfaces, one element per step, and no third surface

The efficiency dimension MUST appear on exactly two surfaces — the periodic status line (`status-report.contract.md`
C-22…C-31) and the current-state digest (`status-digest.contract.md` C-41…C-46) — and on no third one. On each, it
MUST be the **content** of an entry the surface already renders: no extra line, no extra entry, no extra section,
no second cadence and no additional unit. The element's unit is the **step** — the `(unit_id, unit_type)` identity
the exec-quant record itself carries, never a row of a listing (`requirements.md` Clarifications Q4). The number of
efficiency elements on a render MUST equal the number of steps that surface names (the emitting step for the line,
this run's or the most recent steps inside the digest's cap for the digest), and the element MUST NOT introduce a
step the surface did not already name (FR-023).

*Judged by*: `tests/contract/test_efficiency_element.py` — a status line and a digest rendered over one fixture
have equal element counts and equal step sets; a render naming `n` steps carries `n` elements in the status-line
case and no more than the digest's cap (`C-43`) in the digest case.

Requirements served: (FR-023, SC-011).

## C-64 · EF-02 — The element's shape: elapsed first and unconditional; tokens and invocations appended and uniformly degradable

Within one element the quantities appear in this fixed order:

1. the **step identity** — the record's `(unit_id, unit_type)` in a user-facing name, never a bare internal engine
   identifier (`data-model.md` INV-05; `status-report.contract.md` C-31);
2. the **elapsed** quantity — **unconditional** and **first**;
3. the **token** count and the **invocation** count — **appended only while the whole element stays inside the
   surface's own entry bound**.

Each rendered quantity MUST carry the provenance the record states (`measured` / `carried` / `user-given` /
`configured`, quoted from the schema's declared vocabulary — never re-enumerated here) and MUST render the explicit
**not-evaluated marker** where the record carries no value — never `0`, never an averaged substitute, never an
omission (FR-023).

**Degradation is all-or-nothing per render**: when the token and invocation quantities cannot fit the surface's
existing bound, they are withdrawn from **every** step on **that render together**, and the withdrawn quantity is
named in that render's **existing omitted summary**. Per-step depth differences — one step shown with tokens while
a neighbour is shown without — are a defect, because two steps described to different depths cannot be compared
(FR-023; Clarifications Q2).

*Judged by*: `tests/contract/test_efficiency_element.py` — a tight-bound fixture asserts every element carries
elapsed and none carries tokens, with the omitted summary naming the withdrawn quantity; a wide-bound fixture
asserts every element carries all three in the declared order; a fixture mixing a valued and a not-evaluated record
asserts the marker appears for the second and `0` never appears.

Requirements served: (FR-023, SC-011).

## C-65 · EF-03 — One reader, two projections; the element never folds records

Both consumers — the element (through the script that renders the surfaces) and the `/speckit.measure` report —
MUST resolve **one** imported reader: `scripts/python/exec-quant.py`'s read path, imported in-process by path.
Neither consumer MAY re-parse the record format, re-implement the legacy-stream compatibility path, shell out to
the engine's command line, or keep a cache between invocations (FR-028 "one engine and one reading"; the measure
side is `measure-report.contract.md` C-53).

The two consumers MUST NOT borrow each other's selection: the element reports the **latest record** (C-66) and the
report **aggregates over a window** (`measure-report.contract.md` C-54/C-56). A lifetime or windowed figure on a
status line, or a latest-record-only figure in a window report, is the defect this clause names.

*Judged by*: `tests/unit/test_measure_unit.py` — the element projection and the report are driven from the same
fixture store and asserted to call the same imported reader; an AST check asserts neither delivered script
contains a record-format parser of its own.

Requirements served: (FR-024, FR-028).

## C-66 · EF-04 — Record selection is one rule: the latest by `collected_at`, ties by record identity

For a step the surface names, the element MUST report the record with the **latest `collected_at`** among that
step's records — the step being the **record's own `(unit_id, unit_type)`**, never the record's `run_id` (one run's
id is shared across many steps) — selected in exactly one declared way:

- records of the same step are not folded — no average, no sum, no ranking, no lifetime aggregate;
- a tie on `collected_at` is resolved by the record's **own identity in ascending, byte-stable order** (the record
  file's name stem), never by filesystem enumeration order;
- the element MUST NOT widen the surface's step limit: it is rendered for at most the steps that surface already
  names — the emitting step on the line, this run's or the most recent steps inside the digest's cap.

This rule is owned **here** and is the element's own; the report's window aggregation is owned by
`measure-report.contract.md` C-54/C-56 and is a different question, not a second statement of this one (FR-024;
Clarifications Q3).

*Judged by*: `tests/unit/test_measure_unit.py` — a fixture holding three records for one step with increasing
`collected_at` selects the newest; a fixture with two records sharing the newest `collected_at` selects the same
one under a shuffled enumeration order.

Requirements served: (FR-024).

## C-67 · EF-05 — A step with no record renders the not-evaluated marker, never an omission

A step the surface names for which the store holds **no record at all** MUST still carry the element, rendering the
**not-evaluated marker** for the elapsed quantity. Dropping the element for such a step is a defect: an omission
beside a neighbouring step's number reads as "faster", which is the misreading FR-023's rule exists to prevent
(FR-024 final sentence; SC-011).

*Judged by*: `tests/contract/test_efficiency_element.py` — a fixture where the surface names two steps and the
store holds a record for only one asserts both elements are present and one carries the marker.

Requirements served: (FR-023, FR-024, SC-011).

## C-68 · EF-06 — Store availability is never a precondition of the surfaces

When the store is **absent** or **holds no record**, the surfaces MUST render the explicit **"no measurements"**
state and MUST leave the rest of the line / digest unchanged: same units, same content floor, same ordering, same
bound, same exit status as a render with no efficiency dimension at all. An absent store MUST NOT fail the line,
MUST NOT change the digest's exit status, and MUST NOT be reported as an error (FR-024).

*Judged by*: `tests/contract/test_efficiency_element.py` — a render against a nonexistent store path and a render
against an empty store path both produce the "no measurements" state with the entry set byte-identical to the
pre-change render apart from the element's stated absence.

Requirements served: (FR-024, SC-011).

## C-69 · EF-07 — Read-only: both reads leave the store byte-identical, and add no path

Reading the store for the element and for the report MUST leave it unchanged: every file under
`.specify/memory/exec-quant/` MUST compare equal before and after both reads (including the legacy stream files),
and **no new path** MAY be created anywhere under it by either read. No cache file, no derived index, no lock file,
no migration marker (FR-024).

*Judged by*: a per-file digest of `.specify/memory/exec-quant/` taken before and after both reads, plus a
directory listing taken after, stored verbatim in `test-evidence/` (SC-012 Source); `tests/contract/test_measure.py`
re-asserts the same property over a fixture store.

Requirements served: (FR-024, SC-012).

## C-70 · EF-08 — The elapsed source is the existing collection path; no recorder and no schema extension

The element's elapsed quantity MUST be read from the record's `quality.elapsed_ms` node — a field the **declared
schema already carries** (`shared/declarations/facts/quant-record-schema.yaml`, schema version 2) and that the
engine's existing collection paths populate: `collect-dispatch` as `measured`, `collect` as `carried` when the
adjacent run-determination record supplies it. This feature MUST open **no recorder of its own**, MUST add **no
second write path** to the store, and MUST NOT extend the schema: the extension route is closed for this feature
(FR-025).

Where the collection path leaves the quantity `not_evaluated`, that is a **data condition** rendered under C-64's
marker, never a reason to populate it here (FR-025; Clarifications Q1).

*Judged by*: `tests/contract/test_efficiency_element.py` — a static check asserts the delivered scripts name no
schema version, field slot or `quality` sub-key of their own beyond reading the node the engine returns; the
engine's own suite (`tests/contract/test_exec_quant_engine.py`) stays green, proving no write-path change; the
schema declaration file is absent from the changed-file set.

Requirements served: (FR-025).

## C-71 · EF-09 — The record's schema, fields and vocabularies are reached by path, never restated

`data-model.md` E8 and this file's clauses MUST name the store's field paths, its closed vocabularies and its
schema version **via the declaration owner**
(`shared/declarations/facts/quant-record-schema.yaml#/statement` and `scripts/python/exec-quant.py`) and MUST NOT
copy that owner's enumerations. A second literal copy of the provenance list, the unit-type list or the schema
version in any delivered artifact is a defect under constitution XIV (FR-024, FR-025).

*Judged by*: `tests/contract/test_efficiency_element.py` — a scan over the changed spec documents asserts that the
provenance and unit-type enumerations appear exactly where the declaration owner puts them and only by reference
elsewhere; the same scan is the measurement `contracts/ownership-map.contract.md` C-47's new rows are judged by.

Requirements served: (FR-024, FR-025).
