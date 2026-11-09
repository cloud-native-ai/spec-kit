# Contract: Status and Verification Readability

**Feature**: 092-non-disposable | **Contract file**: `contracts/status-and-verification.contract.md`
**Guard carrier**: `tests/contract/test_non_disposable_contract.py` (RK-2's stub-substitution leg lives here)
**Owner**: the closure verdict, the reason-code vocabulary, the verification vocabulary and the smoke record are
owned by `shared/workflow/acceptance-hardening.md` § Closure Verdict / § Verification Vocabulary, and realised by
`scripts/python/closure-acceptance-check.py`. This file fixes the consumption obligations; it MUST NOT restate a
reason code's meaning and MUST NOT introduce a second vocabulary.
**FR coverage**: each clause carries its own trailing citation group.

**The one prohibition this whole file exists for.** The status check **consumes** the closure engine's verdict. It
MUST NOT re-derive it. A second verdict implementation is the failure mode `T-001`-adjacent RK-2 names, and the guard
proves consumption by substituting the checker with a stub that returns a chosen verdict.

## C-201 — One call, one verdict

The `status-unreadable` class MUST obtain its verdict by invoking `closure-acceptance-check.py --json` as a
subprocess and reading `verdict` + `reasons`. It MUST NOT recompute closure from the spec's own prose, from SC counts
or from the registry row. Exit code and payload shape of the checker are its owner's contract, not this one's.

(FR-028, FR-026)

## C-202 — Contradiction is named by the existing reason code

A registry row claiming `Implemented` / `Ready for Review` while the closure verdict is `block` MUST be reported as
the existing reason code `status-claims-implemented-but-blocked`, naming the feature. The engine MUST emit the
checker's spelling verbatim; it MUST NOT paraphrase it into a new string. A feature whose status agrees with the
verdict is not reported by this class.

The **status domain this clause reads is closed**, and so is the set of cells that count as contradictions. Values are
the registry's own, owned by `templates/feature-details-template.md` § Canonical Status State Machine and carried by
`shared/workflow/feature-integration.md` § Status State Machine: `Draft`, `Planned`, `Implemented`, `Blocked`,
`Ready for Review`, `Completed`. Any other spelling in the registry column is a registry defect, not a status this
class may interpret, and the check MUST exit 2 naming the row rather than mapping it to a neighbour. Two further
prohibitions: `Completed` and the single `Relocated` row are NOT out of scope by accident (see the table's named
exclusion below), and a third closure verdict value would make every cell undecidable — the guard MUST fail first.

The contradiction table is **closed and total** over that domain crossed with the checker's verdicts
`accept` / `block`; a cell marked ✗ is a finding, a cell marked ✓ is not, and no cell may be added at
implementation time. `contracts/acceptance-readability.contract.md` C-802 is the owner of this table and of the
corpus rows that land each ✗ red; this clause fixes only what the status column may contain and which two cells the
named reason code covers.

| status | accept | block |
|---|---|---|
| `Draft` | ✓ | ✓ |
| `Planned` | ✗ | ✓ |
| `Implemented` | ✓ | ✗ `status-claims-implemented-but-blocked` |
| `Ready for Review` | ✓ | ✗ `status-claims-implemented-but-blocked` |
| `Blocked` | ✗ | ✓ |
| `Completed` | ✓ | ✗ |
| `Relocated` | not a live row: excluded by name, reported as `count: 0` with its reason | same |

A ✗ cell outside the two that carry `status-claims-implemented-but-blocked` is still a contradiction and MUST be
reported with an empty `reasons` list plus its `evidence_refs` — the reason-code vocabulary is `closure-acceptance-check.py`'s
and this class MUST NOT extend it to name a contradiction the vocabulary has no code for. The deciding question for
every cell is one sentence: *does the row claim more progress than the verdict grants?*

(FR-026, FR-028, SC-008)

## C-203 — The machine-readable block and the smoke fields are required readings

A feature's `verification.md` MUST carry the per-criterion machine-readable block and the smoke fields, whose names
and value domains are owned by `acceptance-hardening.md` § Verification Vocabulary. The check MUST report the
**missing field names** (not merely "unreadable") when the block or a smoke field is absent. Field names are read from
the owner, never listed in the engine.

(FR-025, SC-008)

## C-204 — A closed-set identity is recomputed, both sides given

When a verification record claims a closed-set identity (for example `applicable + exempt == candidates`), the check
MUST recompute both sides from the record and MUST report **both readings** when they disagree. A record that declares
a closed set with no recomputation available is itself a finding — "declared a closed set, no one recomputed it" is
the defect, not a formatting complaint.

(FR-027, SC-008)

## C-205 — No second reason vocabulary, no second closure ladder

The engine MUST NOT define a reason-code enum of its own, a status enum of its own, or a closure ladder of its own.
Where the check needs a status value it MUST use the values its owner publishes. The guard asserts the engine module
contains no literal reason-code table that duplicates `closure-acceptance-check.py`'s.

(FR-028, SC-012)

## C-206 — The reading is reproducible and named

Every `status-unreadable` finding MUST carry its `evidence_refs` including the invariant of the checker call (the
checker's path and the feature id) so a reader can reproduce the verdict with one command. The reading MUST be
independent of run order and of the concurrency degree of the review.

(FR-004, FR-049, SC-009)

## C-207 — Consumption is proven by substitution

The guard MUST include a leg that replaces the checker with a stub emitting a chosen verdict and asserts the engine's
report reflects **the stub's** verdict. If the engine still reports the tree's real verdict, it re-derived it and the
leg MUST fail. This is RK-2's discriminating reading, and its guard leg is the mutation-leg obligation owned by
`contracts/detection-categories.contract.md` C-107, applied to this class: the subject is broken (the checker is
substituted) and the guard must go red before its green counts. The general obligation's owner is that clause; this
one adds only the substituted-checker shape.

(FR-028, SC-008)

**Where the rest of the status reading lives.** C-201…C-206 fix the consumption obligation for the closure verdict. The
other readable objects on the same path — the registry row, the `tasks` / decision-tension structure and the
`requirements.md` path markers — are judged by `contracts/acceptance-readability.contract.md` C-801…C-804, whose
contradiction table C-802 owns the status × verdict cells this file deliberately does not restate.
