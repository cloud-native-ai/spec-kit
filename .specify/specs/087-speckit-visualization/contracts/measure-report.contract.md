# Contract: `/speckit.measure` — the read-only measurement report

**Feature**: 087 | **Covers**: FR-026, FR-027, FR-028, FR-029, SC-013, SC-014
**Contract object**: (a) the thin command `templates/commands/measure.md` (entry `/speckit.measure`) and the
per-tool copies the existing generator produces; (b) the deterministic script `scripts/python/measure.py` with its
declared actions, window, selection, cap, aggregation and closed exit-status set; (c) the one reading it shares
with the visibility surfaces.

Clause ids continue the feature's dense `C-nn` sequence (`C-53`…`C-62`, in the `ME` family) and are
cited verbatim by `/speckit.tasks`. They **do not** renumber or restate `C-01`…`C-52`: where a clause here needs one of those
subjects it names the clause and states only what this file reads.

Every `*Judged by*` line names a surface this file does **not** own; the clause ids, the four exit statuses, the
four exclusion-class names, the printed cap and the declared aggregation words are owned **here**.

---

## C-53 · ME-01 — One command, one script, one reading shared with the visibility surfaces

`/speckit.measure` MUST be a thin command template (`templates/commands/measure.md`) that names the script and the
action and carries no rendering or analysis logic of its own, backed by exactly one stdlib-only script
(`scripts/python/measure.py`). The script MUST obtain its records **by importing the store engine's own read path**
(`scripts/python/exec-quant.py`: `storage_dir()` plus the reader composition `read_jsonl_safe(<legacy stream>)` and
`read_entry_files(<per-record directory>)`), never by re-parsing the record format, never by re-implementing the
legacy-stream compatibility path and never by shelling out to the engine's command line.

The same imported reader MUST serve the efficiency element on the visibility surfaces (`data-model.md` E8), so the
delivered change contains **one** reader of the store and **two** projections over it (FR-028 "one engine and one
reading", reached by path). A second parser, a copied reader, or a second store engine in the changed file set is a
defect.

*Judged by*: `tests/contract/test_measure.py` — an AST audit of `scripts/python/measure.py` for the engine import
and for the absence of a second record-format parser / subprocess call; `tests/unit/test_measure_unit.py` asserts
that the efficiency projection and the report resolve the same imported reader object (see
`efficiency-element.contract.md` C-65, which owns the "one reader, two projections" assertion).

Requirements served: (FR-026, FR-028).

## C-54 · ME-02 — Windows the store's own unit: `--since` from, `--window` span, half-open, stated

The report MUST be computed over one declared window and MUST name the window it actually used.

| Input | Meaning | Rule |
|-------|---------|------|
| `--since <ISO date-or-timestamp>` | the window **start** | parsed exactly as the store engine parses its own `--since` (`_parse_since`); an unparseable value is an input error |
| `--window <duration>` | the window **span**; the end resolves as start + span | same input form the store engine already accepts; a span that does not resolve is an input error |
| neither | **all records the store holds** | the report MUST say so literally (e.g. `window: all records`), never an implied day and never a zero-length window |
| `--since` later than the resolved end | — | **input error** (exit `2`) |

The interval is **half-open**: `start ≤ collected_at < end`. The consequence MUST hold: two adjacent windows over
one store partition it — each record falls in exactly one of them, none dropped and none double-counted
(SC-013).

*Judged by*: `tests/contract/test_measure.py` — a fixture with a fixed record set is measured over two adjacent
windows and the union equals the whole set with an empty intersection; a `--since` after the resolved end exits
`2`; a no-bound run states the all-records window.

Requirements served: (FR-027, SC-013).

## C-55 · ME-03 — Selection is a set of exact unit identities `(unit_id, unit_type)`

`--unit` MAY be supplied one or more times. Each value MUST be matched as an **exact unit identity**, and the
identity's type axis is part of the key: the store holds one `unit_id` under more than one `unit_type`, and the
report MUST present the pair `(unit_id, unit_type)` as **two rows**, never merged into one (FR-027). A value the
store does not hold (after the window and cap rules) MUST be an **input error naming that value** (exit `2`), not
an empty section — silence must not be readable as "no cost".

When no `--unit` is supplied, the selection is **every unit the store holds**, and the report MUST state that.

`--unit` values that name the same identity twice are de-duplicated to one row (a set, not a sequence), so the
selection never inflates a table.

*Judged by*: `tests/contract/test_measure.py` — a fixture that holds one `unit_id` under two `unit_type` values is
measured once with that id supplied and once without, and the report contains two rows in both cases; an identity
absent from the store exits `2` and echoes the value verbatim.

Requirements served: (FR-027, SC-013).

## C-56 · ME-04 — Per-unit figures, with provenance, and the declared distribution

For every selected unit row the report MUST carry:

| Figure | Rule |
|--------|------|
| record count | the number of contributing records in the window (**a sum** over the window, after truncation — see C-57) |
| elapsed time | **median** over the in-window records, with the **minimum** and the **maximum** named beside it; each carries the provenance the records state (`measured` / `carried` / `user-given` / `configured`; a mixed set names each provenance it saw) |
| token count | **a sum** with its provenance and the number of records that carried it |
| invocation count | **a sum** |

A quantity absent from **every** contributing record MUST be reported as **not evaluated** for that unit — never as
`0`, never as a blank, never omitted. A quantity present on **some but not all** contributing records MUST report
its figure **together with the number of records it covered** (e.g. `covered=<k>/<n>`), so a partial figure is never
read as a whole one (FR-027).

The report MUST NOT issue a threshold verdict, a score, a "too slow" judgement or a baseline recommendation: the
figures are measurements and the reader judges them (`requirements.md` A19, `## Out of Scope`).

*Judged by*: `tests/contract/test_measure.py` — a fixture with (i) a unit whose elapsed is `not_evaluated` in every
record, (ii) a unit whose elapsed is present in a strict subset, and (iii) a unit with all quantities present,
asserts the three renderings; a static check asserts no verdict vocabulary (`slow`, `fast`, `score`, `grade`,
`baseline`) appears in the script's output strings.

Requirements served: (FR-027, SC-013).

## C-57 · ME-05 — A declared per-unit cap, printed on every run, truncating by record identity

The script MUST declare **one** default cap for the number of records a single unit contributes to its figures, in
exactly one place, and MUST **print the value it used on every run** — a reader never has to infer which cap
produced a table. `--cap <n>` overrides it per invocation, and the printed value MUST follow the override.

Truncation MUST be applied by the record's own identity (the record file's name stem, which carries its collection
stamp and a stable suffix) in ascending order, so the retained set is stable across runs and across filesystem
enumeration order.

The records the cap dropped MUST be reported as an **omitted count beside the four declared exclusion classes**
(C-58) — `outside-cap` is **not** a fifth reason class; the omitted count is its own printed field, because a record
that was never contributed to a figure is not a record that was excluded for a reason.

*Judged by*: `tests/contract/test_measure.py` — a fixture whose unit holds more records than the default cap prints
that default and an omitted count; `--cap 1` prints `1` and changes the retained set deterministically; two runs
over the same fixture are byte-identical.

Requirements served: (FR-027, SC-014).

## C-58 · ME-06 — Exclusions are counted once, in four named classes

Every record the engine could read but the report did not contribute MUST be counted in exactly one of four
classes, and the report MUST print the count per class (a class with zero is printed as `0`, so a reader can tell
"none" from "not checked"):

| Class | Meaning |
|-------|---------|
| `unreadable` | the engine's reader cannot parse the record (for example a malformed per-record file) |
| `legacy-format` | the record is read only through the engine's compatibility path (its `schema_version` is below the declared schema version the engine writes today) |
| `outside-window` | the record's `collected_at` falls outside the half-open window (C-54) |
| `unknown-unit` | the record carries no usable unit identity, so it cannot be assigned to a row |

A record MUST NOT be counted twice, and the four counts plus the omitted count (C-57) plus the contributed
records MUST sum to the number of records the reader returned — the report MUST be recomputable from its own
printed numbers (SC-013).

*Judged by*: `tests/contract/test_measure.py` — a fixture seeded with one instance of each class asserts the four
counts and the accounting identity `contributed + unreadable + legacy-format + outside-window + unknown-unit +
outside-cap == read`.

Requirements served: (FR-027, SC-013).

## C-59 · ME-07 — A closed exit-status set of exactly four values

The command's exit statuses are **closed** and exactly these four:

| Status | Meaning | Rendered as |
|--------|---------|-------------|
| `0` | a report was produced | the report. **Includes** a report whose window selected records but where **no quantity was measurable** — that is stated as such (`0 figures measurable`) and is **not** the nothing-to-analyse case |
| `2` | input error: unparseable `--since` / `--window`, a start after the resolved end, an unknown `--unit`, unknown `--format` / `--action` | one line naming the offending value |
| `3` | nothing to analyse: the store is **absent**, or holds **no record** inside the resolved window | the explicit `no measurements` statement — never a zero row, never an empty report at status `0` |
| `1` | any other failure | a single plain-language line; MUST NOT be used for either of the two statuses above |

A fifth status, or `1` used for a case the table assigns to `2` or `3`, is a defect (FR-028).

*Judged by*: `tests/contract/test_measure.py` — four fixtures (healthy store, bad input, absent store, empty
window) assert the four statuses and their renderings, and a fixture whose records are all `not_evaluated` asserts
`0` with the stated "no figures measurable" line rather than `3`.

Requirements served: (FR-028, SC-014).

## C-60 · ME-08 — Two closed actions, and the machine-readable render carries the same figures

The script MUST expose a **closed action set**:

| Action | Output |
|--------|--------|
| `summary` | the human-readable report (window, selection, printed cap, per-unit rows, exclusion counts) |
| `json` | the **same** figures as one machine-readable document — window, selection, cap, rows, exclusion counts |

Neither action may compute a figure the other does not carry; the two MUST be projections of one computed result
(a second computation path is the defect C-53 forbids). The JSON document's top-level keys are owned here and MUST
be exactly `window`, `selection`, `cap`, `rows`, `excluded`, `exit_hint`; a row MUST carry `unit_id`, `unit_type`,
`records`, `elapsed`, `tokens`, `invocations`, where each figure object carries `value`, `provenance` and — where
partial — `covered`.

*Judged by*: `tests/contract/test_measure.py` — the two actions over one fixture are compared field by field, and
the key set is asserted exactly.

Requirements served: (FR-028).

## C-61 · ME-09 — Determinism: byte-identical output, no wall-clock text, no enumeration-order dependence

Two invocations over an unchanged store with the same window, selection and cap MUST produce **byte-identical**
output, in both actions. The report MUST NOT contain text derived from the current wall clock beyond the
**window's stated end** (and, when unbounded, no timestamp at all): no render timestamp, no "generated at", no
relative-age wording. Ordering MUST be a declared total order (rows by `(unit_type, unit_id)` ascending; records by
identity ascending) and MUST NOT be left to a hash order or to filesystem enumeration order (FR-028).

*Judged by*: `tests/contract/test_measure.py` — two consecutive runs of each action are compared with a byte-level
diff; a static check asserts no `datetime.now`, `time.time` or `os.listdir`-ordering dependence in the render path.

Requirements served: (FR-028, SC-014).

## C-62 · ME-10 — Read-only, no new machinery, and the standard delivery shape

The delivered set for this capability MUST be exactly: one command template, one stdlib-only script, the per-tool
command copies the existing generator produces, one mirror copy of the script, and the test files that judge it. The
script MUST NOT spawn a subprocess, open a network connection, write any file (no cache, no summary file, no
report persisted), create a directory under `.specify/memory/exec-quant/`, or start a scheduled / background
process; it runs when invoked and exits (FR-026).

The command MUST carry the standard wrap-up delegation the other commands carry (a `## Wrap-up` section generated by
the existing probe compiler), and MUST NOT acquire its own store, its own registry entry or its own long-running
process (FR-029).

*Judged by*: `tests/contract/test_measure.py` — an AST audit over the delivered `.py` file (no `subprocess`,
`os.system`, `os.fork`, `threading`, `asyncio`, socket imports; no `open(..., "w")`), a changed-file audit against
the enumerated delivered list, and a per-file digest comparison of the store before and after a run (SC-012's
measurement surface).

Requirements served: (FR-026, FR-029, SC-014).
