# Contract: Mirror Parity and Distribution

**Feature**: 082-self-explanatory-integration | **Contract file**: `contracts/mirror-distribution.contract.md`
**Guard carriers**: `tests/contract/test_mirror_parity_suite.py` (reused unchanged) plus the docs-link
assertion placed in an existing suite
**FR coverage**: FR-006, FR-007, FR-010, FR-012, and the shared clause C-20 for FR-001/FR-004

The owner documents must arrive at a client project's runtime through the same two steps every
framework document uses — mirror, then `specify init` — and the guard must fail on a missing or drifted
mirror.

## C-20 — No verbatim copy of the owner body (shared by both landing contracts)

For each projected surface that points at the concept owner (`templates/constitution-template.md`,
`templates/instructions-template.md`), the surface MUST NOT contain the owner's own level-2 heading
lines. The carrier parses the owner's headings from `shared/definitions/self-explanatory-definitions.md`,
from its mirror, and asserts that none appears in either surface. This is the decidable form of
"reference, not copy"; it holds regardless of how the projected prose is worded.

## C-21 — Summary bound

The instructions section's summary MUST be at most two sentences before the pointer. The carrier
counts sentences by the house rule (split on terminal punctuation followed by whitespace) over the
section body after the pointer lines are removed, and asserts the count is `<= 2`.

## C-22 — Three mirror pairs are byte-identical

Each of the three pairs MUST be byte-identical:

| Source | Mirror |
|--------|--------|
| `shared/definitions/self-explanatory-definitions.md` | `.specify/shared/definitions/self-explanatory-definitions.md` |
| `shared/guidelines/self-explanatory.md` | `.specify/shared/guidelines/self-explanatory.md` |
| `shared/workflow/best-practice-optimization.md` | `.specify/shared/workflow/best-practice-optimization.md` |

The carrier used is the existing parametrized suite; it derives one parameter per **source** file from
the engine's `MIRROR_PAIRS` table, so the three new documents are covered without editing the suite.
This contract MUST NOT introduce a second table of pairs — the engine owns the enumeration.

## C-23 — The engine reports parity

`python3 scripts/python/sync-mirrors.py --check` MUST exit `0` with no `MISS` and no `DIFF` lines for
the three pairs. The baseline is measured twice in the plan stage and both readings are kept
(research.md B-1, B-7): an early reading was exit `2` with exactly this feature's three `MISS` lines,
a later reading in the same stage was exit `0` with `shared/ == .specify/shared/` reported `ok`
(65 files). The applying baseline is the later one, so the obligation stated here is **keep exit 0**:
the implementation MUST NOT let a later edit reintroduce a `MISS` or `DIFF` line for these three pairs,
and MUST re-measure before claiming the clause (research.md § Re-measure list).

## C-24 — Mirror drift fails the guard

If a mirror copy is modified so it differs from its source, the parity carrier MUST fail, and the
failure message MUST name the source→mirror file pair so the node id is directly re-runnable.

## C-25 — A mirror-only file is never treated as a source

A file present under `.specify/shared/` with no counterpart under `shared/` MUST NOT be presented as
distributed. The engine reports it as an extra (note for the lenient `shared` pair, orphan for strict
pairs) and this feature's acceptance MUST NOT read "present in `.specify/shared/`" as "ships".

## C-26 — `specify init` distributes the three documents

In a fresh temporary directory, `specify init` (the installed entry point) MUST produce
`.specify/shared/definitions/self-explanatory-definitions.md`,
`.specify/shared/guidelines/self-explanatory.md`, and
`.specify/shared/workflow/best-practice-optimization.md`. The assertion lists the three paths and
reports each one's presence; any missing path fails the clause. The distribution input is the
packaged `shared/` source tree — a file that exists only in the repository's mirror can never satisfy
this clause (plan EP-002, research.md R-5).

## C-27 — The docs page's pointers resolve

`docs/concepts/self-explanatory.md` MUST reference, at minimum, the framework-source owner path
`STR-002` and the optimization-workflow owner path
`shared/workflow/best-practice-optimization.md`. The guard extracts every repository-relative `.md`
path written in inline code inside the page and asserts each one exists **in the source tree and in
its mirror tree**. The guard reuses the house pytest + mirror-parity surface; it MUST NOT introduce a
standalone link-checking engine (FR-012). A path that legitimately has no mirror (for example a page
under `docs/`, which is not distributed) is asserted in the source tree only, and the exclusion is
written in the guard as an explicit allow-list with a one-line reason.

## C-28 — Distribution is not wiring

No clause in this contract may be read as asserting that `/speckit.improve` consults
`shared/workflow/best-practice-optimization.md`. That wiring is registered as `OI-082-01` and belongs
to a later improvement; `templates/commands/improve.md` MUST remain untouched by this feature, and the
carrier asserts that it contains no reference to the optimization-workflow path after the change.

## Mutation legs owned by this file

| Leg | Mutation | Assertion that must go red |
|-----|----------|---------------------------|
| M-5 | Modify one byte in a copy of a mirror file inside a temp mirror tree the engine compares | C-22's byte-identity assertion for that pair (the suite's own compare path, exercised on the copy) |
| M-6 | Delete the `STR-002` inline path from a copy of the docs page and run the link guard against the copy | C-27's path extraction → existence assertion |

Both legs operate on temp copies; the carriers assert afterwards that the real files are unchanged.
