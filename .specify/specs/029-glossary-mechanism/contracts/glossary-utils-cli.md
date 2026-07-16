# Contract: glossary-utils.py CLI

**Engine**: `scripts/python/glossary-utils.py` (stdlib-only, Python ≥ 3.8) — deterministic file operations on `.specify/memory/glossary.md`. Models the existing `feedback-utils.py` / `history-utils.py` engine style. Fuzzy judgment (homophone matching, meaning-conflict decisions) is NOT in scope for the engine — it is prompt-side.

Invocation: `python3 scripts/python/glossary-utils.py --action <action> [options]`. Output is JSON on stdout; errors go to stderr with a non-zero exit code.

## C-1 `--action init`

- Options: `--from-template <path>` (default `templates/glossary-template.md`), `--force` (optional).
- Behavior: create `.specify/memory/glossary.md` from the template **only if absent**. Without `--force`, an existing file is left untouched (non-destructive) and the action reports `{"created": false, "reason": "exists"}`.
- MUST NOT overwrite an existing glossary unless `--force` is given.

## C-2 `--action list`

- Returns `{"count": N, "entries": [ {canonical, variants[], meaning, origin, status}, ... ]}` parsed from the table.
- On a malformed file, exits non-zero with a validation message.

## C-3 `--action add`

- Options: `--canonical <str>` (required), `--variants <csv>`, `--meaning <str>` (required), `--origin auto|user` (default `auto`), `--status proposed|confirmed` (default `proposed`).
- Preconditions: MUST run a conflict check first (C-5). If a conflict is detected AND `--confirmed-resolution` is absent, the action MUST refuse to write and exit non-zero with the conflict payload (enforces FR-009).
- Precedence: adding an `auto` entry whose canonical already exists as `user` MUST refuse to overwrite (FR-011).

## C-4 `--action remove`

- Options: `--canonical <str>`.
- Removes the matching row. Removing a non-existent term is a no-op success. Downstream references are unaffected (edge case: removed-term-still-referenced).

## C-5 `--action detect-conflict`

- Options: `--canonical <str>`, `--variants <csv>`.
- Returns `{"conflict": bool, "kind": "same-term-diff-meaning"|"homophone/near-duplicate"|"ambiguous-variant"|null, "collidesWith": [canonical, ...]}`.
- Detects only **exact/structural** collisions (identical canonical, or a variant already bound to a different canonical). Phonetic/near-duplicate similarity is advisory input for the prompt layer, which makes the final judgment; the engine MUST NOT auto-resolve.

## C-6 `--action validate`

- Validates the file against `glossary-file-format.md` (C-2, C-3). Returns `{"valid": true}` or exits non-zero with the first violation.

## C-7 General

- All actions are idempotent where applicable and MUST NOT introduce non-stdlib dependencies.
- No action may write a conflicting change without an explicit resolution flag (single enforcement point for FR-009).
