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

## C-206 — Consumption is proven by substitution

The guard MUST include a leg that replaces the checker with a stub emitting a chosen verdict and asserts the engine's
report reflects **the stub's** verdict. If the engine still reports the tree's real verdict, it re-derived it and the
leg MUST fail. This is RK-2's discriminating reading and the reason the class is admissible as `deterministic`.

(FR-028, FR-062, SC-008)

## C-207 — The reading is reproducible and named

Every `status-unreadable` finding MUST carry its `evidence_refs` including the invariant of the checker call (the
checker's path and the feature id) so a reader can reproduce the verdict with one command. The reading MUST be
independent of run order and of the concurrency degree of the review.

(FR-004, FR-049, SC-009)
