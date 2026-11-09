# Contract: Disposition

**Feature**: 092-non-disposable | **Contract file**: `contracts/disposition.contract.md`
**Guard carrier**: `tests/contract/test_non_disposable_contract.py` (C-302 / C-305 / C-306 / C-307 carry mutation legs)
**Owner**: the disposition set, the two bridge tables, the unmappable rows and the adjudication rule are owned by
`shared/definitions/non-disposable-definitions.md` § Disposition Set / § Disposition Bridge (FR-008, FR-012,
FR-013, FR-014). This file fixes the guard-addressable obligations; it copies neither table's content nor the
sanitize vocabulary (`sanitize-utils.py` is read for those members, never re-spelled here).
**FR coverage**: each clause carries its own trailing citation group.

## C-301 — Closed disposition set, four members, one owner

An entry in `state: disposed` carries exactly one `disposition` whose value is a member of the owner page's closed
set. The set is owned there and nowhere else: the guard MUST read the four member spellings through the owner page
(not from a literal list in this contract or in the engine) and MUST fail when the engine emits a value outside it.

(FR-008, FR-001)

## C-302 — "Do nothing" is not a disposition

An entry with `disposition = null`, `""`, `"keep"`, `"leave"`, `"none"`, or any free-text value is a finding. The
engine MUST emit it as `state: open` with a non-zero exit code, and the guard MUST include a mutation leg that injects
`"keep"` into a report and asserts red. There is no `kept-as-is` member and no "reviewed by a human" close.

(FR-009, SC-003)

## C-303 — `exempt` carries four fields, all four required

`disposition = exempt` is valid only together with `reason`, `expiry_kind`, `expiry_value`, `expiry_recheck`
(§ `data-model.md` E-3). A missing member makes the disposition invalid: the entry stays `open` and the report names
the missing field. `expiry_kind` is one of the three closed values; a constant-true condition (`condition: true`, an
empty predicate) is rejected as invalid, not as "still valid".

(FR-006, FR-007, SC-017)

## C-304 — Expiry is evaluated, never assumed

`on-condition` predicates MUST be consumed by one engine evaluation. Un-evaluable → `unevaluated` (visible, counted as
not closed), never "still valid". `on-date` / `on-review` compare against an absolute date; once `expiry_recheck` has
passed, the entry re-enters the open set on the next run and the report MUST NOT self-declare closure.

(FR-006, FR-007, FR-005)

## C-305 — Two closed sets coexist; the bridge is exhaustive over their product

The bridge MUST cover **every** pair of the owner page's disposition set and `sanitize-utils.DISPOSITIONS` with a row
whose `relation` is `maps-to` or `unmappable`. No third state. The guard MUST compute the expected pair count from the
two sets' lengths at test time (never from a stored literal), assert the bridge has exactly that many rows, and MUST
fail on a duplicate pair. The set literals in `sanitize-utils.py` are read by the guard and MUST be byte-unchanged.

(FR-012, FR-060, SC-015)

## C-306 — Unmappable values have a named receiving surface, and two prohibitions are explicit

Every `relation = unmappable` row MUST name its `receiving_surface`. Two prohibitions are part of the contract because
they are the ones a reader would otherwise infer wrongly: `exempt` has **no** counterpart in the material-hygiene set
(a hygiene candidate must be disposed, never exempted), and `dismiss` MUST NOT be read as "deferred" (its meaning is
"judged to need no disposition") and therefore MUST NOT be mapped to `exempt`. The guard asserts both prohibitions are
stated in the owner page and that no bridge row contradicts them.

(FR-014, SC-015)

## C-307 — One adjudication rule, written once, quoted by both engines

When one concrete candidate is seen by both engines, the detecting engine decides the disposition vocabulary. The rule
MUST be stated exactly once (owner page) and both engines MUST reference it. The guard MUST contain a mutation leg that
makes both engines claim the same candidate and asserts red — "the same candidate disposed twice" must be mechanically
falsifiable, not merely discouraged.

(FR-013, SC-015)

## C-308 — Disposal acts only through the owner page's pathways

No batch delete, no batch rewrite channel. `archive` is a **move** (`git mv` semantics) that records the source path →
archive path mapping; a deletion is never a disposition (FR-034 iv, FR-058). The guard asserts the disposition record
shape (§ `data-model.md` E-4) carries `moved` for every archive and `irreversible` only where the router says so.

(FR-034, FR-052, FR-058, SC-010)
