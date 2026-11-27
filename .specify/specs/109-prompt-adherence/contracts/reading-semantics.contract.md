# Contract — Reading Semantics

**Feature**: 109 Prompt Adherence Evaluation（提示遵从度评价）— Spec Kit port of the closed ai-harness spec 092
**Status**: design contract. Field meanings after implementation: owner document § Reading Contract;
value domains: the five declaration facts plus the composed observation-state domain. The per-field
tables live in `data-model.md` § E-6…E-11; this file states the normative clauses.

## C-020 — Per-run reading shape

**Statement**: a per-run reading carries: `reading_format` (integer), `engine` identity and version,
`declaration_set` version and fact paths, `scope` (with resolution and basis), `status`, exactly one
observation per catalog row in catalog declaration order (state, deviation classes, reason when
`not_evaluated` or `Unobserved`, resolvable source references), the mandatory coverage section, and the
`invalid_sources` / `duplicates` disclosures. No field outside this set carries a verdict.
**Red when**: a catalog row is missing or doubled; a required field is absent; the coverage section is
absent; an undeclared field states a conclusion.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (fixture-reading legs).

**Serves**: (FR-014, FR-013, FR-011)

## C-021 — Scope resolution and the two explicit statuses

**Statement**: with no explicit scope, the reading resolves the most recent run identity observed across
the catalog records — selected by record timestamp, tie-broken by store name then source path — and
prints the resolved identity and its basis in the scope section. With no such record it still emits,
with status `no-data`. An explicit `--run <run-id>` that matches no records yields status `not-found`.
Both statuses exit 0: a reading was produced. `--run` combined with `--since`/`--until` is an input
error (exit 2).
**Red when**: a default scope silently reads all time; the basis is not printed; `no-data` or
`not-found` is reported as an error exit; an unmatched explicit run is reported as clean; the ambiguous
combination is accepted.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (scope-resolution legs).

**Serves**: (FR-014)

## C-022 — Longitudinal window: half-open, `open`, counts only

**Statement**: with an explicit window the reading is longitudinal: counts by evidence state per catalog
row plus the coverage line, bounded in size. The window is half-open `[since, until)` on each record's
own timestamp field; an omitted bound is printed as the literal `open`; both bounds appear in the
output. No per-project, per-agent or per-user ranking or comparison is produced. Declaration-only rows
(the probe row) evaluate once against current state and are marked window-exempt in the scope notes.
**Red when**: a bound is silently all-time or resolved to a clock reading; the boundary record at
exactly `since` or `until` is counted on the wrong side; a ranking appears; a declaration row is faked
into a timestamped series.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (window-arithmetic legs, boundary
fixture on an exact timestamp).

**Serves**: (FR-015)

## C-023 — Determinism, ordering, duplicates

**Statement**: identical input records and an identical mechanism version produce a byte-identical
reading (JSON and human form both derive from one computed structure; the JSON serializes with sorted
keys). Ordering: rows in catalog order; source references by (path, record identity); invalid sources by
path; duplicates by (row, identity); blind spots in register order. Duplicates are keyed by each row's
declared identity fields (plus the row's timestamp field where declared), counted once per extra
occurrence and disclosed with their paths — never merged, never double-counted silently. Output caps are
bounds, not judgement thresholds: per-observation source references 20, invalid sources 50, duplicates
20, each with a shown/total disclosure when truncated.
**Red when**: two reruns differ; a clock or `generated_at` field enters the output; an unordered
collection reaches the output; a duplicate is silently merged; a cap is presented as a judgement
threshold.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (determinism, ordering, duplicate
and cap legs).

**Serves**: (FR-016, FR-017)

## C-024 — Every observation is reconstructible from its citations

**Statement**: every positive observation cites at least one resolvable source reference
(`store`, repo-relative `path`, `record` identity, `field`). An unparsable, schema-violating
(including a value token outside the source engine's declared domain), unknown-schema-version or
invalid-timestamp record is reported in `invalid_sources` with the record's path and cause and is
never interpreted under the current schema; the reading does not crash and reports the invalid
count. A record written by an older or unknown schema version is laid aside with
`unknown-schema-version`.
**Red when**: a state cannot be reconstructed from its citations; an invalid record is skipped silently
or coerced; a reading aborts on one bad record.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (audit-replay leg; seeded broken
reference and seeded bad records).

**Serves**: (FR-017, FR-022)

## C-025 — The coverage section is mandatory

**Statement**: every reading carries a coverage section naming which catalog rows were observable in the
scope, which were not, and the six blind-spot classes with their reasons; it also states the record count
in scope and the invalid-record count. A reading without its coverage section is invalid.
**Red when**: the section is absent in either output form; a blind-spot class is omitted; the observable
/ not-observable partition does not match the observations.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (coverage legs, both output forms).

**Serves**: (FR-013, FR-029)

## C-026 — Reading status and exit codes

**Statement**: `status` is derived exactly as the reading-status rule of `data-model.md` § I-4:
`no-data` iff the resolved scope holds zero catalog records; `not-found` iff an explicit run identity
matches zero records; otherwise `partial` iff at least one observation is `not_evaluated`, else
`complete`. Exit `0` whenever a reading is emitted (including `no-data` and `not-found`, and including a
reading whose `invalid_sources` discloses record-level unknown value tokens) and when `--check-coverage`
is clean; exit `1` when `--check-coverage` reports map findings; exit `2` when no reading can be produced
— an unusable declaration layer or owner document, an unknown token in the five declaration sets, in the
owner document's tables or on the engine's command line (C-013's closed subject), an undeclared store
name in a catalog row (FR-030), or invalid arguments. A record-level value outside its source engine's
declared domain is never an exit-2 cause: C-024 lays the record aside in `invalid_sources` and the
reading continues with exit `0`.
**Red when**: a status outside the closed set appears; `no-data`/`not-found` exits non-zero; a
declaration failure exits 0 or emits a reading; a record-level unknown value token aborts the reading, or
is dropped without an `invalid_sources` entry.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (status and exit-code legs);
`tests/contract/test_prompt_adherence_declarations.py` (degradation leg).

**Serves**: (FR-014, FR-022, FR-030)

## C-027 — Privacy: structured fields only

**Statement**: a reading carries only structured fields, closed tokens and source references. Feedback
entry bodies (review prose, points), gate decision prose and finding summaries never cross into any
output form. The engine reads feedback entries through their metadata surface only.
**Red when**: raw prose, a user-authored sentence or a conversation excerpt appears in either output
form; a body-reading filter is used to obtain data.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (privacy leg over a fixture whose
records embed distinctive prose; output scanned for the markers).

**Serves**: (FR-021, FR-009)

## C-028 — Absence semantics

**Statement**: a row with no matching record, an unavailable source, or an uninterpretable record
surfaces as `not_evaluated` or `Unobserved` with a reason — never as clean, compliant, zero, or a
violation. A missing gate record, missing anomaly line or other absence is never inferred as breach;
breach-style readings enter only where an existing store records the event itself. The
`not_evaluated`/`Unobserved` split follows the four-way derivation of `data-model.md` § E-6: explicit-run
mismatch or unreadable source → `not_evaluated`; readable source with zero matching records under a
default or window scope → `Unobserved`.
**Red when**: a missing record yields an adherence or breach claim; a zero count is presented as clean;
the split contradicts E-6.
**Test carrier**: `tests/contract/test_prompt_adherence_engine.py` (absence legs; fresh-store fixture).

**Serves**: (FR-011, FR-012)

## C-029 — The reading is read-only and contains no adherence verdict

**Statement**: a reading performs no write under any managed store root, keeps no cache or lock, and
concurrent readings do not interfere. No observation, field or human line emits `adherent`, `deviant` or
a layer-level equivalent; the complete negative vocabulary is the three deviation classes plus the
absence states.
**Red when**: any file under a store root changes during a reading; a verdict token or composite score
appears; a lock file or cache is created.
**Test carrier**: `tests/contract/test_prompt_adherence_readonly.py` (hash-manifest containment);
`tests/contract/test_prompt_adherence_engine.py` (no-verdict leg).

**Serves**: (FR-006, FR-018, FR-025)