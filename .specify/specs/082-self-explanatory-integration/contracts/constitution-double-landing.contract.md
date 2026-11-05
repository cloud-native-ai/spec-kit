# Contract: Constitution Double Landing

**Feature**: 082-self-explanatory-integration | **Contract file**: `contracts/constitution-double-landing.contract.md`
**Guard carrier**: `tests/contract/test_constitution_double_landing.py`
**FR coverage**: FR-001, FR-002, FR-003, FR-008

One title (`STR-001`) must land on three surfaces and nowhere else, and the guard must be able to go
red on any of them. Clauses below are normative; `C-N` maps one-to-one onto a test in the carrier file.

## C-1 — Template carries the principle

`templates/constitution-template.md` MUST contain a level-3 heading whose title, after its numeral, is
`STR-001` verbatim. The title MUST be a member of the template's title set (set membership, never
substring containment — `Code as the Single Source of Truth` and `One Source of Truth (Authority &
Reference Discipline)` share a substring and must stay distinct).

## C-2 — The principle block satisfies the house shape

The block from the heading to the next `### ` or `## ` MUST satisfy all of:

- (a) heading form `### <numeral>. <title>`;
- (b) the sentence between the heading and the first bullet ends with a colon;
- (c) 3–6 logical bullets, each containing the literal `MUST` (logical, i.e. after joining
  hard-wrapped continuation lines);
- (d) no physical line of 100 characters or more;
- (e) `Rationale:` follows the last bullet after exactly one blank line, with nothing between;
- (f) the `Rationale:` paragraph is 1–4 sentences;
- (g) no unresolved bracket placeholder of the form `[UPPER_SNAKE_CASE]` remains.

## C-3 — Numerals are per-surface and not pinned

The template's numeral for the new principle MUST be the template's next free numeral at landing
time, and the live constitution's numeral MUST be that surface's next free numeral. Because the two
rosters have different sizes (measured at plan time: template 17, live 18), the two numerals MAY
differ. No clause, test, or plan row in this feature may assert a particular numeral value.

## C-4 — Matchers stay numeral-agnostic

The title matchers used by the carrier MUST accept both roman and arabic numerals and MUST NOT
contain a pinned numeral literal. This clause is asserted by running the matchers over a synthetic
roster that uses a numeral this repository has never used.

## C-5 — Mandate-list entry

`skills/internal/manage-constitution/SKILL.md` MUST carry a sub-entry of the form
`  - **STR-001** — …` inside its `- **MUST include**` block, and the block's entry count MUST equal
the count asserted by the carrier (`COMMAND_COUNT` raised by one). The entry MUST carry both the
truth-document anchor and the referenced-not-restated rule.

## C-6 — Content obligations of the principle

The principle's normative text MUST cover, each as a bullet, all five:

1. the **user's view** decides, not implementation-internal clarity;
2. the **ceiling** is that the user sees the information directly, the **floor** is one simple
   command, and the floor is sufficient to support a change;
3. the principle MUST NOT be used to justify preventive redesign — a concrete user information need
   is required;
4. each optimization task raises at most **one** information dimension, and reconciliation is how
   that dimension lands;
5. an encoded attribute keeps its original source of truth; names and paths are projections
   reconciled to it.

The principle MUST point at the runtime owner path `STR-004` as the location of the full definition,
and MUST state that the owner is referenced, not restated. The framework-source path `STR-002` MAY
appear only as the framework's own owner location.

## C-7 — Watchlist membership on both sides

`STR-001` MUST be appended to the carrier's double-landing watchlist, and every watchlist title MUST
be a member of both the template's title set and the generator's mandate-name set.

## C-8 — Gate-budget neutrality

The principle block MUST produce zero hits against the gate scanner's compiled blocking pattern
(`scan-confirmation-gates.py` `BLOCKING_RE`). The same assertion MUST hold for the instructions
section added by `contracts/instructions-propagation.contract.md`, and for the mandate-list entry.
Rationale: the scanner's total is pinned by equality elsewhere, and this feature must not be the
reason it moves. This clause does not depend on the total's current value (see plan EP-003).

## C-9 — Live constitution landing

`.specify/memory/constitution.md` MUST contain the principle, and:

- its `**Version**:` line MUST be strictly greater than the baseline read from
  `git show HEAD:.specify/memory/constitution.md` at implementation time (floor semantics: compare
  the major.minor tuple, never an equality pin);
- a Sync Impact Report MUST be prepended as an HTML comment at the top of the file, stating the
  version change arrow, and the head window of the file MUST name the principle **this** amendment
  added (asserted by deriving the newest watchlist entry, not by a fixed older title);
- the live principle's block MUST satisfy C-2, C-6 and C-8 when the carrier's structure checker runs
  against it.

## C-20 pointer (shared with the instructions contract)

The "no verbatim copy of the owner" rule that this file's C-6 leans on is stated once, as C-20 in
`contracts/mirror-distribution.contract.md`, and is not restated here.

## Mutation legs owned by this file

| Leg | Mutation (on a temp copy, never the repository) | Assertion that must go red |
|-----|------------------------------------------------|---------------------------|
| M-1 | Delete the principle block from a copy of `templates/constitution-template.md` | C-7's template-side membership |
| M-2 | Delete the `- **STR-001** — …` sub-entry from a copy of the mandate list | C-7's mandate-side membership, and C-5's count |

Both legs MUST also assert their anti-vacuity companion (the real file does carry the subject) and
MUST assert afterwards that the repository files are untouched.
