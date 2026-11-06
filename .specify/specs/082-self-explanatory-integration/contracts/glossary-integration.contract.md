# Contract: Glossary Integration

**Feature**: 082-self-explanatory-integration | **Contract file**: `contracts/glossary-integration.contract.md`
**Guard carriers**: `tests/contract/test_glossary_mechanism.py` (must stay green, unmodified) plus the
entry assertions below placed in a suite of the same kind
**FR coverage**: FR-011; SC-007

The term must be findable by the name a later reader will actually type, and the retired name must
never become a second canonical entry.

## C-29 — The canonical entry exists with the ratified fields

`.specify/memory/glossary.md` MUST carry exactly one entry whose canonical column is `STR-003`
verbatim, and that entry's `origin` MUST be `auto` and its `status` MUST be `proposed`. The entry is
written through the store's own engine (`glossary-utils.py --action add`), never by hand-editing the
table, so the row shape stays the store's.

## C-30 — The retired name is a variant, never a second canonical

The retired name `望文生义` MUST appear only inside the `variants` column of the canonical entry.
The carrier MUST parse the store's rows and assert:

1. no row other than this one has `望文生义` (or the canonical string) in its canonical column;
2. the retired name is present in the canonical entry's variants column;
3. `glossary-utils.py --action validate` exits `0` after the write.

Substring search over the file is not an acceptable assertion for (1): the retired name legitimately
appears in the variants column of the same row.

## C-31 — The existing mechanism suite stays green

`tests/contract/test_glossary_mechanism.py` MUST pass unchanged. It guards the mechanism (template
present and mirrored, required structure, Documentation Map row, init round-trip), and none of its
clauses enumerate terms — so a failure there after this change is a real regression, not a stale pin.

## C-32 — The meaning points at the owner

The entry's meaning cell MUST point at the concept owner by path (`STR-002`/`STR-004`), so a reader
who lands on the glossary row reaches the single definition point rather than a second description.
The carrier asserts the cell contains a repository-relative path that exists.

## C-33 — Status is not promoted by the flow

The entry MUST stay `proposed`. No automated step in this feature may flip it to `confirmed`; the
promotion is a user-authoritative action (plan `data-model.md` § T-B, spec Assumption A6).

## C-34 — Term discovery is not a second vocabulary

No document added by this feature may define a competing canonical form (for example
`Self-explanatory Structures`, `Self-Explanatory Structure (without the 不言自明 form)`,
`望文生义` as a current name). The carrier asserts that the literal `STR-001` and the literal
`STR-003` agree on their shared portion, and that no surface introduces a third form.
