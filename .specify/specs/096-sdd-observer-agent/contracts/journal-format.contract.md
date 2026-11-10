# Contract — Journal Format（记录格式，owner: journal-format.yaml）

Scope: `shared/declarations/facts/journal-format.yaml` and every consumer of it. Requirements: FR-010, FR-011, FR-012, FR-013, FR-014. This page states the information face; the fact file owns the spellings.

## C-01 — One owner for the spelling face

Field keys, event-class literals, retention classes, pointer kinds, the missing placeholder, the escape rule and the journal filename are owned by `shared/declarations/facts/journal-format.yaml#/statement` and read through `scripts/python/declaration_reader.py`. No consumer carries a second copy; tests may pin a literal only to fail when the owner changes.

(FR-011, FR-012)

## C-02 — Journal location and title

The journal is `<spec-dir>/journal.md` (STR-001). Its first line is `# SDD Journal — <spec-key>`. No second record file or second record store is introduced by this feature.

(FR-010)

## C-03 — Header

The header carries exactly five keys — `line_id`, `run_id`, `spec`, `observer_instance`, `created_at` (UTC ISO-8601 seconds) — written once by the engine on first append.

(FR-010)

## C-04 — Exactly one table, nine columns

The body contains exactly one markdown table whose header row is `| seq | observed_at | event_at | stage | event | command | artifact | exit | evidence |` with the separator row beneath it. Entry rows use exactly these nine columns in this order.

(FR-011)

## C-05 — Field domains

`seq` is an engine-assigned integer starting at 1 and strictly increasing by 1 in file order. `observed_at` is the engine clock in UTC ISO-8601 seconds. `event_at` is carrier-provided in the same form or `-`. `stage` is a stage literal from `shared/declarations/facts/driver-stage-sequence.yaml#/statement` or `-` for line-level and observer events. `command` is literal command text or `-`. `artifact` is a repo-relative path or `-`. `exit` is an integer or `-`.

(FR-011)

## C-06 — Closed event-class set

The event classes are exactly the sixteen declared by the fact file: `line-start`, `line-terminal`, `stage-start`, `stage-end`, `stage-verdict`, `checkpoint`, `commit`, `anomaly`, `stall`, `retry`, `dispatch`, `artifact-write`, `observer-start`, `observer-settle`, `observer-gap`, `observer-error`. Growth is a fact-file revision, never an inline invention.

(FR-012)

## C-07 — Evidence pointers and retention classes

`evidence` carries one or more pointers separated by `; `, each of the form `<retention>:<kind>:<target>[#<anchor>]` with `retention ∈ {persistent, runtime}` and `kind` in the closed set owned by the fact file. A persistent path pointer resolves relative to the repository root; a commit pointer resolves through `git cat-file -e`. Runtime pointers are marked; where the same fact has a persistent carrier, a runtime pointer MUST NOT be the only evidence.

(FR-014)

## C-08 — Minimum persistent evidence per event

Each event class declares `min_persistent` in the fact file (`0` or `1`). A row whose class declares `1` MUST carry at least one persistent pointer; a row with no pointer at all is a finding for every class.

(FR-014)

## C-09 — Append-only and file order

Rows are appended; no existing row is rewritten or deleted. File order is the authority for same-second ordering: `seq` follows row order, never a timestamp comparison. The checker never mutates the journal.

(FR-010, FR-011)

## C-10 — The gap row uses the two time columns as its window

An `observer-gap` row encodes its window as `event_at` = window start (previous entry's `observed_at`, or the spine record's `started_at` when no entry exists) and `observed_at` = window end (the new execution's first write). No inferred event may fill the window.

(FR-013)

## C-11 — Escaping

A literal `|` inside a value is escaped as `\|`; newlines and carriage returns collapse to one space. Copying the rendered journal into another document is not a re-parse target.

(FR-011)

## C-12 — Free narrative is not an entry

A non-table paragraph, list or fenced block inside the journal body is a finding. Evaluation, suggestion, causal inference, severity or recommendation has no column to occupy (FR-013, SC-004).

## C-13 — Committed with the line

The journal may be swept into intermediate stage commits and is not required to have a commit of its own; the line's closing commit carries the final entries so the record survives worktree cleanup. The journal is NOT added to any stage's required artifact set, `STAGE_ARTIFACTS` mapping or U4 completion condition.

(FR-010)
