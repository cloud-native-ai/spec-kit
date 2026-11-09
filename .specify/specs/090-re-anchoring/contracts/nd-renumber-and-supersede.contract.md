# Contract: Renumber and Supersede

**Feature**: 090-re-anchoring · Non-Disposable slice (absorbed from 092) | **Contract file**: `contracts/nd-renumber-and-supersede.contract.md`
**Guard carrier**: `tests/contract/test_non_disposable_contract.py` (ND-C-505 / ND-C-506 carry mutation legs; the renumber
legs additionally read `scripts/python/renumber-utils.py`)
**Owner**: the supersede protocol and the renumber predicate face are owned by
`shared/definitions/non-disposable-definitions.md` § Supersede Protocol / § Renumber-Face. The predicates themselves
are **reused** from `scripts/python/renumber-utils.py` (`EXCLUDED_PREFIXES`, `MACHINE_PREFIXES`, `EVIDENCE_SEGMENTS`,
`DATED_RE`) — this contract MUST NOT restate them; it fixes what a guard may assert about their use.
**FR coverage**: each clause carries its own trailing citation group.

## ND-C-501 — Supersede recovers three landing faces

When one feature supersedes another feature's body, guard or evidence path, the superseding side MUST recover all
three: (i) the body — old text retained **and** marked superseded with a pointer to the new carrier; (ii) the guard —
the old behaviour's assertion replaced or removed; (iii) the evidence path — the old spelling keeps a pointer, never a
second copy of the truth. Recovering two of three is the defect this contract detects.

(FR-015, SC-005)

## ND-C-502 — Incomplete recovery is mechanically detectable

A body marked superseded whose guard still demands the old behaviour, or whose evidence path exists in a second
spelling, or which lacks the pointer, MUST be reported red naming path and line. The guard MUST carry one mutation leg
per landing face (body / guard / evidence path), each asserting red on a copy tree and green after synchronised
recovery.

(FR-016, FR-062, SC-005)

## ND-C-503 — The supersede registry is a readable record, not a session note

A supersede MUST be recorded in the owner page's registry form (superseded item → superseding item → disposition →
evidence path) readable by the engine. A supersede that exists only in a commit message or a session record does not
satisfy this clause and the guard MUST fail when it is the only trace.

(FR-017, SC-005)

## ND-C-504 — Live bindings follow the directory's actual number

A live binding (feature id in an authority file, requirement/feature ids in a task header, the team directory name and
slug, the feature id in a contract header, the lines of a feature reference file, a registry row) that disagrees with
the directory's number MUST be reported red naming file and line. All four live-binding shapes reproduce from the
corpus (C1–C4, 档 I, repaired here).

(FR-022, SC-007)

## ND-C-505 — History records are never rewritten to suit a new number, and rewriting them is detected

History records MUST NOT be rewritten to follow a renumber. The check MUST report red for a history record that
**was** rewritten, and the predicate face splits into two **named** legs because its members are addressed two
different ways:

**Leg 1 — path-addressed records.** Taken from `renumber-utils.py`'s existing predicates, never a new "looks like
history" heuristic: `EXCLUDED_PREFIXES` (`.specify/history/`, `.specify/archive/`, `.specify/specs/.archive/`),
`MACHINE_PREFIXES` (`.specify/memory/sanitize/`, `.specify/memory/retention/`, `.specify/memory/renumber/`),
`EVIDENCE_SEGMENTS` (`test-evidence`) and `DATED_RE` (date-named files). These four cover **paths only**.

**Leg 2 — section-addressed records, which no path predicate can cover.** A `## Clarifications` block is a *section
inside a live spec body*, and the spec body itself is a file a renumber legitimately edits — so `renumber-utils.py`'s
path predicates are structurally blind to it, and ND-C-505 MUST NOT claim otherwise. The predicate for this leg is the
**section position** the owner page states (`## Clarifications` and every heading beneath it, to the next sibling
`##`), read by a Markdown section scanner; a removal of that section's text, or an edit inside it that carries a
renumber, is red. This is the one leg for which this feature owns a predicate of its own, and it is stated here rather
than left to implement time because its absence would make the clause silently weaker than its own wording.

The corpus has no row for either leg (`plan.md` § A–H two-way check); the guard carries both as fixtures.

(FR-023, FR-024, SC-007)

## ND-C-506 — One predicate implementation, quoted by both sides

The engine MUST consume the renumber predicates from `renumber-utils.py` (import or documented subprocess), and MUST
NOT carry a second copy of `EXCLUDED_PREFIXES` / `MACHINE_PREFIXES` / `EVIDENCE_SEGMENTS` / `DATED_RE`. The guard
asserts the engine module contains no duplicate of those literals — a mutation leg edits the predicate module and
expects the engine's classification to move with it.

(FR-024, FR-060, SC-012)

## ND-C-507 — Archive is a move and keeps the old text

`archive` dispositions move the carrier and keep the superseded text intact; deletion is not a disposition. The
disposition record MUST carry the source → archive path mapping so the move is reversible by a single `git` operation
(§ `contracts/nd-disposition.contract.md` ND-C-308). `git status --porcelain` after a repair run MUST show a rename pair for
an archived path, never a deletion.

(FR-034, FR-058, FR-017)
