# Contracts: Capture step — code-review findings into the client channel (C-10…C-24)

**Requirement → Feature**: `072-client-self-improvement` → Feature 072 客户项目的持续反馈与自我提升
**Owner**: this file owns the fifth step of the code segment's non-interactive path: its trigger, the pointer payload, the three invariants, and the closed disclosure vocabulary. The record form, the receipt, and the report's code subsection are owned by Feature 071 and are cited here, never re-specified.
**Pinned by**: `tests/contract/test_client_capture.py` (planned)
**Measures**: SC-001, SC-002, SC-007

**C-10**: The code segment's non-interactive path step enumeration is amended exactly once, from four steps to five: base resolution, record creation and rotation, note landing, receipt and verdict, client capture. The amendment records its reason (all capture inputs — record path, applicability value, per-severity counts — exist only after step 4, and co-locating capture in the same deterministic path is the only position where "findings enter the client channel" is a mechanically checkable fact) and its cost (one closed enumeration of the predecessor feature is rewritten once). No other closed surface of the predecessor feature is touched by this amendment (FR-005, SC-007).

**C-11**: Client capture executes as a deterministic subcommand of the code segment's existing script — `capture --review-file <record> --triage <value> [--unit <custom:owner/name>]` — which assembles the entry from deterministic inputs and calls the feedback engine's record action. No new command is added, no closing step is added, and no agent hand-writes a client entry (FR-005, FR-026).

**C-12**: Capture fires only when two conditions hold together: the run's repository is judged a client project, and the code segment's applicability value is `run`. Exactly one capture execution and at most one entry occur in a qualifying run; entries are never written per finding, per file, or per severity (FR-006, SC-001).

**C-13**: In a framework-hat repository (including a client repository that vendored the framework sources, where the hat verdict is framework), capture writes no entry under any armed state. The step's output line states that capture did not run and names the hat verdict as its basis, citing the hat owner. This line never takes the form of any of the five closed client-channel tokens (FR-001, FR-006, SC-003).

**C-14**: When the applicability value is not `run` (`not-applicable` or `not-evaluated`), no record exists to point at; capture writes no entry and discloses `no-capture-object`. It never records an empty entry for such a run (FR-009, SC-002).

**C-15**: The client entry's payload is a pointer with a closed field set: the code-segment record path, this run's applicability value, the six per-severity counts, this run's identifier, and the owning client unit. The entry MUST NOT contain review-comment bodies, per-file verdict lists, the receipt's per-file fields, changed-file totals, or non-code-file counts (FR-007, SC-001).

**C-16**: The six counts are copied verbatim from the existing summary command's machine-readable output — one count for each of the six severity levels (`blocking`, `important`, `suggestion`, `nitpick`, `question`, `praise`), zero values included, no level omitted and no level merged. No human or agent recounts or estimates the numbers (FR-007, SC-001).

**C-17**: The summary command gains an opt-in machine-readable form (`--format json`) carrying the record path, the six counts, the blocking count, and the gate verdict. The existing text output and the exit-code alphabet (`0` allow / `1` deny / `2` unparseable input) are unchanged; the predecessor feature's pinned tests stay green (FR-007, FR-025, SC-001, SC-007).

**C-18**: This run's identifier is the code-segment record header's date stamp (ISO-8601 UTC, second resolution), which is the same stamp used in the archive file name and is overridable via the script's existing run-timestamp environment variable for deterministic tests. Idempotency therefore rests on the engine's existing `(unit, run)` key: a second capture of the same record is answered by the engine's duplicate result, writes no second entry, and is not an error (FR-007, FR-008, SC-001).

**C-19**: Capture keeps three invariants. Idempotent: at most one entry per (unit, run). Non-blocking: capture failure never changes the segment verdict, the merge-gate verdict, or any status transition, and the capture step always exits `0`. No overreach: capture never edits the code-segment record, never rewrites the receipt's field block, and triggers no transmission of any kind (FR-008, SC-001, SC-002).

**C-20**: A merge-gate denial (summary exit `1`, blocking entries present) does not suppress capture: capture is observation, not verdict, and the counts are taken exactly as the summary command reports them (FR-008, SC-001).

**C-21**: A summary exit of `2` (input unparseable) discloses `counts-unavailable` and writes zero entries; the counts are never zero-filled and never reported from memory. An engine record failure or a refused write discloses `counts-unavailable` as well, and the review run is not blocked — the optionality red line outranks capture (FR-009, SC-002).

**C-22**: Every non-interactive run ends with exactly one capture outcome line. In a client project the line's state token is drawn from the closed five-value set `client-channel-armed` / `client-channel-unarmed` / `client-unit-ambiguous` / `no-capture-object` / `counts-unavailable`, followed by the specific detail (recorded unit and entry id, or the reason and one-time guidance). The disclosure appears in the run's human-facing conclusion and is visible together with the run's applicability value (FR-009, SC-002).

**C-23**: In every non-capture case the store gains zero entries: no empty entry, no zero-filled entry, and no "no findings this run" phrasing substitutes for the named reason (FR-009, SC-002).

**C-24**: The capture disclosure lives in the run's closing summary, which is a presentation surface. It is not added to the report's code-subsection field list, which stays byte-identical to the predecessor feature's closed list; the two artifact surfaces never merge (FR-009, FR-025, SC-007).

## Traceability

| Clause | FR | SC | Surface |
|--------|----|----|---------|
| C-10 | FR-005 | SC-007 | skill step enumeration |
| C-11 | FR-005, FR-026 | — | script subcommand |
| C-12 | FR-006 | SC-001 | capture trigger |
| C-13 | FR-001, FR-006 | SC-003 | hat branch |
| C-14 | FR-009 | SC-002 | triage branch |
| C-15 | FR-007 | SC-001 | entry payload |
| C-16 | FR-007 | SC-001 | summary command |
| C-17 | FR-007, FR-025 | SC-001, SC-007 | summary json form |
| C-18 | FR-007, FR-008 | SC-001 | run identifier + idempotency |
| C-19 | FR-008 | SC-001, SC-002 | invariants |
| C-20 | FR-008 | SC-001 | gate-deny branch |
| C-21 | FR-009 | SC-002 | failure disclosure |
| C-22 | FR-009 | SC-002 | disclosure closure |
| C-23 | FR-009 | SC-002 | zero-entry rule |
| C-24 | FR-009, FR-025 | SC-007 | conclusion placement |
