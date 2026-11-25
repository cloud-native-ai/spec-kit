# Contract — Store Layout: target roots, ownership, registration, ignores

**Spec**: `requirements.md` FR-001…FR-006, FR-009, FR-017, FR-019…FR-021, FR-025 · **Plan**: `plan.md` WP01/WP02/WP04/WP05/WP06 · **Date**: 2026-11-25

This contract fixes the target layout and its normative properties. The store roster has one machine owner (C-6); this document defines shape and obligations, never a second roster.

## C-1 Target layout

Each runtime store is a first-class top-level root `.specify/<name>/`. The closed set and every member's disposition are owned by requirements § Store Inventory (baseline) and by `shared/declarations/facts/runtime-store-layout.yaml` (machine). This contract states only the classes:

- **Memory tiers** — `session`, `knowledge`: seeded by `specify init`; owned by the memory engine; the only stores whose existence is guaranteed after a fresh init.
- **Runtime stores** — `feedback`, `evidence`, `exec-quant`, `trigger`, `retention`, `renumber`, `sanitize`, `housekeeping`, `coaching`, `todo`, `tools`, `migrate`: created lazily by their single owner; never seeded with content by init.
- **Retired** — `draft` (no new home) and the container `.specify/memory/`.
- **Non-store** — `git-workflow.md` (legacy single file; owner: git-utils/sanitize legacy rule).

MUST: no store is nested under another store; no grouping directory is introduced; names are unchanged from the baseline child names (A-4).

## C-2 Retired container

`.specify/memory/` is a retired store root.

- MUST NOT be created by `specify init`, any engine, skill, template, or test fixture except the migration/residue readers.
- MUST NOT be read or written as a live store; no runtime dual-path fallback (A-8).
- Its only current meaning is the tombstone row in `shared/definitions/framework-map.md`, worded as A-2 states: historical catch-all bucket; retired; agent-context memory is carried by `.specify/session/` (short-term) and `.specify/knowledge/` (long-term); no engine may treat it as a live store.
- After a completed migration the directory MUST be absent; empty residue is removed; non-empty residue is reported and preserved (FR-015), never silently deleted.

## C-3 Ownership

- Exactly one owning component per store, named in the declaration and in the framework-map row (FR-005).
- Existing writer relationships are preserved: memory only through the memory engine, feedback only through the feedback engine, evidence only through the evidence engine, etc.
- MUST NOT introduce a second writer or cross-store writes.

## C-4 Ignore and tracking matrix

| Store | Tracking / ignore | Owner of the rule |
|---|---|---|
| `session`, `knowledge`, `feedback`, `evidence`, `exec-quant`, `retention`, `renumber`, `housekeeping`, `coaching`, `todo`, `migrate` | entries tracked; ephemeral lock files ignored per store owner | existing owners + `.specify/.gitignore` |
| `trigger` | `index.json` tracked; `telemetry.jsonl` ignored | `.specify/.gitignore` |
| `sanitize` | whole store is machine-regenerable cache → ignored | `.specify/.gitignore` |
| `tools` | `*.md` records tracked; `*.json` discovery inventories ignored | `.specify/.gitignore` + `generate-instructions.sh` |

- `templates/gitignore-specify-template` and the installed `.specify/.gitignore` MUST be byte-identical and MUST land in the same change (FR-020).
- The template MUST carry `tools/*.json` (not `tools/`), `sanitize/` (not `memory/sanitize/`), and `trigger/telemetry.jsonl` (not `memory/trigger/telemetry.jsonl`).
- `templates/claudeignore-template` and `templates/codexignore-template` MUST release the new top-level store roots instead of `!.specify/memory/`.
- A store directory that exists but is unignored where C-4 says ignored — or ignored where C-4 says tracked — is a defect measured by `git check-ignore -v` in a fixture.

## C-5 Registration (directory governance)

- Every new top-level store MUST gain one framework-map row carrying owner, lifecycle, and content class; the row MUST point at the store's owner document/engine, never restate another file's rules.
- The retired container MUST be recorded as a tombstone row and MUST NOT keep a live-map row.
- `.specify/instructions.md` (generated from `templates/instructions-template.md`) and `.specify/glossary.md` MUST name the new paths for every live entry (FR-021). The `Memory Layer`, `Session(消歧)`, `三捕获机制`, `自省报告`, `Evaluation Form`, `Renumber Lane`, `Coaching Run` entries are in scope.
- A proposed `Runtime Store` glossary entry is an implementation-run proposal recorded in that run's evidence; it MUST NOT be written into `.specify/glossary.md` without user confirmation (A-16). No acceptance criterion depends on it.

## C-6 Machine declaration

`shared/declarations/facts/runtime-store-layout.yaml` is the single machine-readable owner of the store set (shape: `data-model.md` E-10).

- `kind: mapping`; registered in `shared/declarations/contract.yaml` before any consumer reads it.
- Consumers that enumerate more than their own store MUST read it through `scripts/python/declaration_reader.py`: `scripts/python/sanitize-utils.py`, `renumber-utils.py`, `seal-utils.py`, `concurrency-check.py`, the `specify migrate` planner, and the init seeder.
- `shared/declarations/facts/non-disposable-review-surface.yaml` remains the closed-set owner of the historical review roots; it lists the new store roots as its own statement (it is not a reader of this declaration) and a guard asserts its store members equal the declaration's store set.
- A consumer whose read degrades (declaration absent) MUST use the reader's `absent_label` and MUST NOT invent a fallback roster. A single-store engine MAY keep its own root constant (its store is its own fact); the declaration does not replace those constants.
- Guard: a contract test asserts the declaration membership equals the code consumer sets and equals the requirements' Store Inventory dispositions (`tests/contract/test_runtime_store_layout.py`).

## C-7 Fresh initialization

- The packaged seed root is `seed/` (source; wheel `specify_cli/seed`), containing the two anchor placeholders and `session/`, `knowledge/` placeholders. The old package seed directory `memory/` MUST be removed in the same change: no shipped asset directory is named `memory`.
- `specify init` MUST seed `.specify/session/` and `.specify/knowledge/`, MUST seed anchors at `.specify/` as today, and MUST NOT create `.specify/memory/` (FR-017).
- Init MUST NOT move legacy store content: when legacy content is detected it stays in place and the output points at `specify migrate` (FR-013's executor ruling).
- `_CORE_SPECIFY_ASSETS` MUST replace the `.specify/memory` member with `.specify/session` and `.specify/knowledge`.
- `rewrite_paths()` MUST NOT carry the generic `memory` segment nor any `memory/<anchor>` special rule; the packaged sources carry runtime-form `.specify/<store>/` paths.

## C-8 Non-goals (normative)

- No entry-format, write-protocol, or consumption-semantics change for any store (FR-025; 055 protocol unchanged).
- No new store engine, registry, scheduler, scoring, or second context-injection mechanism (A-14, FR-012).
- No store format migration, no database, no shared aggregate.
