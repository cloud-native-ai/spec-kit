# Contract: Detection Categories

**Feature**: 090-re-anchoring · Non-Disposable slice (absorbed from 092) | **Contract file**: `contracts/nd-detection-categories.contract.md`
**Guard carrier**: `tests/contract/test_non_disposable_contract.py` (one test per class, each with a mutation leg)
**Owner**: the closed class set, each class's predicate and each class's `deterministic`/`semantic` subject are owned
by `shared/definitions/non-disposable-definitions.md` § Detection Categories (FR-001). This file fixes **what a guard
may assert** about the eight classes; it restates none of the predicates, and it deliberately carries no copy of the
class list beyond the ids the clauses need to be addressable.
**FR coverage**: each clause carries its own trailing citation group; that group, not this header, owns the mapping.

The eight classes are the closed set FR-003 / FR-010 require. A ninth class is a contract change (owner page first,
then this file), never an engine-only addition.

## ND-C-101 — Closed set, one owner, no engine-local extension

The engine MUST read the class set from the owner page (or from a fact the owner page names) and MUST report an
`unknown-class` finding if a class it emits is absent there. The engine MUST NOT introduce a class that the owner page
does not declare, and MUST NOT add a class to `sanitize-utils.py`'s `CATEGORIES` — that set belongs to Feature 047.

*Class ids this contract addresses*: `superseded-live`, `multi-owner`, `renumber-live-binding`, `status-unreadable`,
`false-closed-set`, `stale-constant`, `orphan-path`, `deferral-marker`.

(FR-001, FR-010, FR-060)

## ND-C-102 — One class per entry, no class stacking

An entry carries exactly one `category`. A defect that reads as two classes MUST be reported twice with two distinct
`entry_id`s (the ids differ by the class segment) — never once with a joined class string. The guard asserts that the
`category` value of every emitted entry is a single member of the closed set (no `+`, no `,`, no `|`).

(FR-002, FR-008)

## ND-C-103 — Each class names its observable reading

A class is admissible only if its owner-page predicate lands on a reading a program can take (file / line / field /
literal / count / path / resolvable reference). The guard asserts, per class, that the entry carries `path`, `line`,
and at least one `evidence_refs` element whose `path` exists in the tree — i.e. every class in the closed set is
individually re-checkable without re-running the engine.

(FR-002, FR-003, FR-004)

## ND-C-104 — The four structure classes

| Class | What the clause requires of the guard | Corpus rows that must reproduce |
|-------|---------------------------------------|---------------------------------|
| `superseded-live` | a body marked superseded whose old text is still asserted by a live guard, or whose successor pointer is absent → red, naming body path:line **and** the guard path:line | B1, B2, B3, G1, G3 |
| `multi-owner` | the same name/constant independently assigned or independently stated on one axis → red, naming **both** sites and **both** values | D1–D6, F4 |
| `orphan-path` | a referenced path that does not exist → red, naming the referring path:line and the missing target | B4, B5, H1, H2 |
| `renumber-live-binding` | a live binding carrying a feature id that is not the directory's → red, naming file:line | C1–C4 |

A class whose corpus rows all reside in 档 II (repaired by another line) still MUST reproduce here; detection is this
feature's deliverable in both tiers, only the repair moves (see `feature-ref.md` § Shift List).

(FR-015, FR-016, FR-017, FR-018, FR-019, FR-020, FR-021, FR-022, FR-023, FR-024)

## ND-C-105 — The four state classes

| Class | What the clause requires of the guard | Corpus rows that must reproduce |
|-------|---------------------------------------|---------------------------------|
| `status-unreadable` | a registry status that disagrees with the closure verdict, or a `verification.md` missing the machine-readable block / smoke fields → red, naming the feature and the missing field | A1–A6 |
| `false-closed-set` | a claimed closed-set identity whose two sides do not hold → red, giving **both** readings | A2, E1–E6 |
| `stale-constant` | the same constant declared with two live values where one site is not the value owner → red, naming both sites and the owner | F1, F2, F3, F5 |
| `deferral-marker` | a retention statement with no expiry condition → red, naming path:line and quoting the marker | (no corpus row — see below) |

(FR-006, FR-007, FR-025, FR-026, FR-027, FR-005)

## ND-C-106 — `deferral-marker` is proven by construction, not by corpus

The A–H corpus never specifically looked for retention wording, so no corpus row carries this class (recorded in
`plan.md` § A–H Corpus Mapping two-way check). The guard therefore MUST prove it on a **fixture** tree, and the
fixture MUST be stated in the guard's own data so the missing corpus row is visible to the next reader rather than
read as full coverage. The class MUST still be in the closed set and MUST still be emitted by the engine on the real
tree when one exists.

(FR-002, FR-003, FR-006, FR-053)

## ND-C-107 — Mutation leg per class

For every class in the closed set the guard MUST contain one mutation leg: a copy-tree edit that creates the defect,
asserting the engine goes red and names the expected path:line; plus the inverse (repair the copy tree, assert green).
A class with only a green assertion does not satisfy this contract — a green that cannot go red is not evidence.

(FR-062, SC-001, SC-005, SC-006, SC-007, SC-008)

## ND-C-108 — Reproduction is per class, and a class that finds nothing says so

The engine MUST be able to report, per class, `count: 0` **with** the roots it searched. A class that is silent is
reported as zero findings over a stated surface, not omitted from the report. `quickstart.md` § 2 names the class
whose corpus rows do not reproduce on this tree today and why.

(FR-011, FR-055)
