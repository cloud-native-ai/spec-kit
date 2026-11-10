# Contract — Journal Engine（单一确定性引擎）

Scope: `scripts/python/journal-utils.py` (+ `.specify/scripts/python/` mirror). Requirements: FR-007, FR-010, FR-011, FR-012, FR-013, FR-014, FR-015, FR-016.

## C-01 — One executable face, two actions

The engine exposes exactly two actions: `--action append` and `--action check`. `append` projects carrier facts into the journal; `check` validates an existing journal. No third action exists; growth is a contract revision.

(FR-015)

## C-02 — Script interface contract

The engine answers `-h` / `--help` and `--version` with zero side effects before any action, rejects an undeclared option non-zero, and follows the wiring of `scripts/python/record-retention.py` (`script_interface_cli.configure_parser` / `guard_argv`, with the ImportError fallback). It is stdlib-only and runs on CPython `>=3.8`.

(FR-015)

## C-03 — Append invocation

`append` takes `--spec-dir`, `--spine`, `--state-dir`, `--repo`, `--line-id`, `--run-id`, `--execution-label` and the flags `--settle` / `--final` (mutually exclusive semantics below). It writes the header when absent and appends the newly derivable rows. `--settle` closes one execution (`observer-settle`); `--final` additionally writes `line-terminal` and `observer-settle`.

(FR-010, FR-015)

## C-04 — Deterministic projection only

Every row is derived from the closed carrier list (E-10): the state spine observer record section and the two narrow prose grammars, runner quartet envelopes, stage logs and sentinels, checkpoint files, git history, meta envelopes, execution records. The engine reads no driver conversation, no stage prompt body, and accepts no free-text entry argument. An unreadable carrier yields no row for that carrier (and, where the journal remains writable, one `observer-error` row naming the path).

(FR-013)

## C-05 — Idempotent append

Each candidate row carries a stable identity (event + natural keys + evidence target); an identity already present in the journal is skipped. Re-running `append` over unchanged carriers appends nothing. `seq` continues from the last row.

(FR-010, FR-013)

## C-06 — Single-writer protocol

The engine opens the journal for append and takes a non-blocking exclusive `flock` on the journal file itself. If another writer holds it, the engine exits `3` with the label `concurrent-writer-refused` and writes nothing. No lock file and no second store is created.

(FR-007)

## C-07 — Identity check

The engine reads the latest state spine observer record section. It requires `state: started`, a matching `line_id` / `run_id` and a matching `execution_label` for the invoking execution; a mismatch (stale or foreign execution) exits `2` with a label and appends nothing. `--final` requires the same match.

(FR-007, FR-010)

## C-08 — Gap derivation

On the first append of an execution (or of a new `execution_label`), if the previous entry's `observed_at` is earlier than the spine record's `started_at`, the engine appends one `observer-gap` row with `event_at` = window start and `observed_at` = window end per journal-format C-10.

(FR-013)

## C-09 — Check invocation and findings

`check` takes `--spec-dir` and `--repo`. It validates every rule in `data-model.md` V-1…V-13 and V-16…V-17 and reports each finding as `code: path:line`, exiting `0` (no finding), `1` (at least one finding) or `2` (input error). The checker never writes.

(FR-014, FR-015)

## C-10 — Exit-code set is closed

`append`: `0` appended/nothing new; `2` input or identity error; `3` concurrent writer refused. `check`: `0` / `1` / `2`. No other code is emitted; no code encodes a verdict about the feature.

(FR-015)

## C-11 — Facts come from the declaration layer

Closed sets (event classes, retention classes, pointer kinds, entry/header keys, the journal filename, the missing placeholder) are read from `journal-format.yaml` through `declaration_reader`; the engine holds no second copy. A missing or unparsable fact is `owner-unavailable` (exit 2 with the label), never a silent default.

(FR-011, FR-012)

## C-12 — Stage names come from the stage-sequence fact

Valid `stage` values are read from `shared/declarations/facts/driver-stage-sequence.yaml#/statement` through the same reader; the engine does not carry a stage list.

(FR-012)

## C-13 — Read-only check and append-only writes

The engine's only write points are the journal (append), the header (once, inside the same append) and nothing else. It creates no directories, rewrites no row, and touches no artifact, spine or registry. `check` is strictly read-only.

(FR-010, FR-015, FR-016)
