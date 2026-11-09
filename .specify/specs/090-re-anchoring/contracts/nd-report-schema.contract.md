# Contract: Report Schema

**Feature**: 090-re-anchoring · Non-Disposable slice (absorbed from 092) | **Contract file**: `contracts/nd-report-schema.contract.md`
**Guard carrier**: `tests/contract/test_non_disposable_contract.py` (ND-C-702 / ND-C-705 carry mutation legs)
**Owner**: the field set of an entry and of a run is owned by `data-model.md` § E-1 / § E-2 / § E-6; the member sets of
`category`, `disposition` and `detection` are owned by the owner page; the closure verdict and its reason codes are
owned by `shared/workflow/acceptance-hardening.md`. This file fixes the **serialisation** obligations: what `--json`
must contain, what the human form must be a projection of, and what the report must never say.
**FR coverage**: each clause carries its own trailing citation group.

## ND-C-701 — One model, two projections

The `--json` document and the human-readable stdout MUST be projections of the same in-memory run (§ `data-model.md`
E-2). The human form MUST NOT introduce a field, a count or a conclusion the JSON does not carry. The guard parses the
JSON and asserts every human-form count appears in it.

(FR-010, FR-011)

## ND-C-702 — The coverage declaration is mandatory and first

The report MUST begin with the coverage declaration, whether or not any candidate exists: the declared roots **in
declaration order**, each with presence and count; the candidate total; the excluded items with reasons; the
missing roots; the unregistered siblings (hints); the declaration path and its `status`. A report with findings but no
coverage declaration is invalid; a report with an empty candidate set MUST state that conclusion and MUST NOT say
`closed: true`.

(FR-011, FR-038, FR-040, FR-041, SC-014, SC-018)

## ND-C-703 — Entry fields

Every entry MUST carry the E-1 field set with these serialisation rules: `entry_id` is the merge key (two entries with
the same id MUST be merged by the engine, never emitted twice); `path` is repository-relative and normalised with one
optional leading `.specify/` stripped, matching `declaration_reader.normalize_path`; `line` is 1-based with `0` reserved
for file-level facts; `evidence_refs` has at least one element and a `semantic` entry has at least two; `detection`
carries the owner page's two values; `state` carries the state machine's values; `disposition` is `null` unless
`state: disposed`.

(FR-004, FR-008, FR-009)

## ND-C-704 — Un-evaluated is a counted, visible state

An `unevaluated` entry and an `unevaluated` shard MUST appear in the report and MUST be counted in the "not closed"
totals. The report MUST NOT emit an `unevaluated` shard as an empty entry list without the mark. The guard asserts the
not-closed total grows when a deterministic input is made unparseable and, separately, when a semantic shard returns a
malformed payload.

(FR-005, FR-048, SC-016)

## ND-C-705 — The report never claims closure it cannot prove

`closed` is derived (§ `data-model.md` E-2) and MUST be `false` when any entry is `open` / `unevaluated` /
`unconfirmed` or any shard is `unevaluated`. The report MUST NOT carry a "reviewed by a human" or "kept as is" field —
those are not states and not dispositions. A mutation leg writes `closed: true` over an open entry and asserts red.

(FR-005, FR-009, FR-033, SC-003, SC-016)

## ND-C-706 — The four reader questions are answerable from the report alone

The report MUST let a reader who did not take part answer: what was looked at (ND-C-702), what was found (path, class,
evidence strength, `detection`), what is proposed (suggested disposition, touched paths, reversibility), and what is
not done (`open` / `unconfirmed` / `unevaluated` counts, stated as not closed). The design-segment face of the command
reuses the same four answers; it does not invent a fifth form (§ `data-model.md` § Human-Facing Output Shape).

(FR-011, FR-042, SC-019)

## ND-C-707 — Status findings quote the owner's vocabulary

A `status-unreadable` entry's machine fields MUST carry the checker's `verdict` and the reason-code spelling verbatim
(including `status-claims-implemented-but-blocked`), plus the identity of the checker call that produced them. The
report MUST NOT translate a reason code into prose in the machine form.

(FR-026, FR-028, SC-008)
