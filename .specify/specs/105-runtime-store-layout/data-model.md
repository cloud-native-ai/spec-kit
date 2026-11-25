# Data Model — Runtime Store Layout

**Spec**: `requirements.md` · **Plan**: `plan.md` · **Contracts**: `contracts/` · **Date**: 2026-11-25

This model defines the entities the plan and implementation share. It deliberately contains no third copy of the store roster: the roster is an entity whose *values* are declared once in `shared/declarations/facts/runtime-store-layout.yaml` (C-6 of `contracts/store-layout.contract.md`); this file defines the shape.

## E-1 Runtime Store

One top-level `.specify/<name>/` root with exactly one owning component.

| Field | Type | Constraint |
|---|---|---|
| `name` | string | lowercase kebab-case; one of the closed declaration set (E-10) |
| `target` | path | derived: `.specify/<name>/` |
| `legacy_source` | path | derived: `.specify/memory/<name>/` |
| `lifecycle` | enum | `memory-tier` \| `runtime-record` \| `telemetry` \| `cache` \| `queue` \| `receipt` \| `definition-record` \| `run-report` |
| `owner` | path | exactly one component (e.g. `scripts/python/memory-utils.py`) |
| `content_class` | string | short free text for the framework-map row |
| `non_content` | list | predicates for machine-generated artifacts and installer placeholders that are not conflict content (E-3) |
| `seeded` | bool | true only for `session` and `knowledge` (init seeds the directory); every other store is created lazily by its owner |

Validation: `name` unique; `owner` exists; `seeded` true ⇒ owner is the memory engine; `non_content` patterns are glob names relative to the store root.

## E-2 Store Inventory Row

The closed classification of every baseline member (requirements § Store Inventory).

| Field | Type | Constraint |
|---|---|---|
| `baseline_member` | string | a child name from `git ls-tree -d 23938f22e:.specify/memory`, an engine-declared on-demand store (`sanitize`, `migrate/receipts`), a legacy item (`draft`, `git-workflow.md`), or the container literal |
| `classification` | enum | memory-tier / runtime-record / telemetry / cache / queue / receipt / definition-record / legacy-retired / non-store / retired-container |
| `disposition` | enum | `relocate` \| `retire` \| `non-store` |
| `target` | path? | required iff `disposition = relocate` |
| `note` | string | short |

Validation: every baseline member appears exactly once; a member outside the table is a table defect (FR-001/A-3), repaired by revising the requirements table and the declaration together.

## E-3 Store Relocation Item

One plan item for the `store-layout` dimension. Shape extends the existing `MigrateItem`; the added fields are carried in the item payload, not in a second plan format.

| Field | Type | Constraint |
|---|---|---|
| `dimension` | literal | `store-layout` |
| `target` | path | the new store root `.specify/<name>` (for the container item: `.specify/memory`) |
| `current` | string | measured state token: `absent` \| `empty-residue` \| `legacy-content` \| `dual-content` \| `symlink` \| `unreadable` |
| `expected` | string | `relocated` \| `retained` \| `container-absent` |
| `disposition` | enum | `archive` (relocate) \| `refuse` \| `blocked`; `converged` items are not emitted |
| `mechanism` | enum | `relocate` \| `none` |
| `entries` | list[E-4] | present on `archive` items; the manifest written before any move |
| `reason` | string? | required for `refuse` / `blocked`; names both paths and the repair entry |
| `status` | enum | `planned` \| `done` \| `refused` \| `blocked` \| `failed` |

**Authoritative entry** = a file at the store root or below whose relative path does not match that store's `non_content` predicates (E-1). Conflict, emptiness and residue are decided only on authoritative entries; non-content entries are protected but never decisive (A-7).

State table (old = `legacy_source`, new = `target`):

| old authoritative | new authoritative | disposition | action |
|---|---|---|---|
| none | none | none (converged) | nothing; if old dir exists (only non-content) remove it only when it is empty, else report preserved residue |
| none | any | none (converged) | new is authoritative; never touch; remove an empty old dir if present |
| content | none | `archive` / `relocate` | build E-4 manifest, move each entry, verify digests |
| content | content | `refuse` / `none` | name both paths; move/overwrite/delete nothing |
| old path is a symlink (either side) | any | `refuse` / `none` | `reason = symlink-<side>`; never follow, never unlink |
| target parent unwritable (dry-run `os.access`, apply re-check) | any | `refuse` / `none` | `reason = permission-denied`; no partial success claim |
| any relative path exists on both sides and the old one is authoritative | any | `refuse` / `none` | `reason = path-collision`; names the relative path (new-side non-content is never deleted to make room) |
| unknown member left in the old container after all known stores | — | `refuse` / `none` | `reason = unknown-residue`; lists every remaining path; preserves them |

Exclusion from the new-side content count: receipts written by **the acting run itself** (identified by `run-id`) are the transaction record of this migration, not a competing authority. Every pre-existing receipt counts as content.

## E-4 Store Relocation Entry

One row of a store's pre-move manifest; the archive record for recovery and the resume oracle.

| Field | Type | Constraint |
|---|---|---|
| `relpath` | string | relative to the store root; POSIX separators |
| `class` | enum | `authoritative` \| `generated` \| `placeholder` |
| `digest` | string | SHA-256 via the existing `_migrate_digest` semantics (regular file content; symlink target; directory aggregate) |
| `from` | path | `.specify/memory/<name>/<relpath>` |
| `to` | path | `.specify/<name>/<relpath>` |
| `status` | enum | `planned` \| `moved` \| `left-in-place` |

The manifest is written to the run receipt **before** the first move of that store. `recover` is the ordered inverse: move `to` back to `from` for every `moved` row.

## E-5 Migration Receipt v2

The existing per-run receipt (`<workspace>/.specify/migrate/receipts/<run-id>.json`, one file per run, `O_EXCL`) gains one object; all existing top-level fields keep their meaning.

| Field | Type | Constraint |
|---|---|---|
| `receiptVersion` | int | `2` for new runs; version 1 receipts remain readable as resume inputs (dated records) |
| `items[]` | list | dimension items as today; store items add `entries[]` and the E-3 fields |
| `storeLayout` | object | `{ "stores": N, "resolved": N, "refused": N, "blocked": N, "container": "removed"\|"preserved"\|"absent", "manifestDigest": "..." }` |
| `recover[]` | list | existing shape; for store items each row carries `path`(from), `archiveTo`(to), `change: "relocated"`, `digest` |
| `status` | enum | `running` \| `completed` \| `aborted` (existing domain) |

Validation: `receiptVersion=2` iff a `storeLayout` object exists; every store item's `entries[]` digest set equals its `recover[]` digest set; no path appears in two store items.

## E-6 Retired Store Root

The tombstone entity for `.specify/memory/`.

| Field | Type | Constraint |
|---|---|---|
| `literal` | literal | `.specify/memory/` |
| `tombstone_row` | path | `shared/definitions/framework-map.md`（唯一墓碑行） |
| `allowed_contexts` | closed set | tombstone row · the retired-root declaration (`runtime-store-layout.yaml`) · migration engine and its tests · legacy-residue scanners |
| `forbidden` | list | create / read / write as a live store by any engine, template, skill, doc, or test outside `allowed_contexts`; runtime fallback; second authority |

Validation: a guard test measures the literal's occurrence file set per artifact class against the declared allowlist and asserts equality in both directions (L-5).

## E-7 Memory Tier

Unchanged members of the memory system.

| Field | Type | Constraint |
|---|---|---|
| `scope` | enum | `session` \| `knowledge` — owner `shared/declarations/facts/memory-types.yaml`; not renamed |
| `root` | path | `.specify/session/` \| `.specify/knowledge/` |
| `role` | enum | short-term/forgettable \| long-term/distilled |
| `entry` | file | one Markdown file per record; frontmatter schema unchanged; derived index |
| `actions` | closed set | `record, recall, list, prune, reindex, scope all` — unchanged |

## E-8 Injection Payload

Unchanged dispatch contract; only memory source paths move.

| Field | Type | Constraint |
|---|---|---|
| `downlink` | closed set | `parent_identity, child_label, role_declaration, dispatch_duty, depth_position, authority_ref, return_channel` |
| `injections` | closed set | fast-fail, concurrency obligation, reporting obligation, re-anchoring |
| `uplink` | closed set | five elements |
| `memory_sources` | list[path] | entries retrieved by `memory-recall`; MUST resolve under `.specify/session/` or `.specify/knowledge/` |

## E-9 Live-Reference Record

One row for every file the migration rewrites (inventory is measured in `research.md` R-2; the normative rewrite rules are `contracts/live-reference-migration.md`).

| Field | Type | Constraint |
|---|---|---|
| `path` | path | repository-relative |
| `class` | enum | `framework-source` \| `runtime-guide` \| `current-docs` \| `ignore-template` \| `test` |
| `action` | enum | `rewrite` \| `regenerate` \| `repair-stale` \| `keep-legacy-fixture` \| `dated-record` |
| `old` → `new` | path pairs | drawn only from the E-10 declaration mapping + anchor/store-specific repairs |
| `verify` | command | the command whose output proves the row (contract L-3/L-8) |

## E-10 Runtime Store Layout Declaration

The single machine-readable owner of the store set, at `shared/declarations/facts/runtime-store-layout.yaml` (kind `mapping`, read via `scripts/python/declaration_reader.py`).

| Field | Type | Constraint |
|---|---|---|
| `fact` | literal | `runtime-store-layout` |
| `statement.stores` | mapping | name → `{lifecycle, owner, content_class, non_content, seeded}` |
| `statement.retired_container` | literal | `.specify/memory` |
| `statement.legacy_non_store` | list | `git-workflow.md` |
| `statement.legacy_retired` | list | `draft` |
| `consumers` | list | every engine that enumerates more than its own store (sanitize, renumber, seal, concurrency-check, non-disposable-check, migrate, the init seeder) |
| `former_carriers` | list | the per-consumer literals this declaration replaces |

The declaration is registered in `shared/declarations/contract.yaml` before any consumer reads it (the layer's own rule). Paths are projections: consumers derive `.specify/<name>` and `.specify/memory/<name>` from `name`; they do not carry a second list.

## State transitions

**Store item**: `planned → done` (all entries moved or already converged) · `planned → refused` (pre-condition refusal) · `planned → blocked` (destructive action would have no recovery path) · `planned → failed` (unexpected OS error; receipt records it and the run aborts).

**Run receipt**: `running → completed` (no refused/blocked/failed store item) · `running → aborted` (a store item failed; already-moved entries stay recorded for resume).

**Store state (field-observable, never conversation memory)**:

```
absent ──seed──▶ empty-new ──relocate──▶ relocated
  │                 ▲
  └─legacy-only ────┘
legacy-only + new-content ──▶ dual-conflict (refuse; no state change)
relocated ──re-run──▶ relocated (no-op; idempotence)
```

## Invariants

- **I-1 Zero-write dry-run**: a dry-run writes nothing anywhere, including receipts and temp files (097 I-1 preserved).
- **I-2 No object destroyed**: every entry is present at its old path or its new path after every run step; recovery = apply `recover[]` in reverse.
- **I-3 Idempotence**: a second apply after success moves nothing, creates nothing, and emits no store items.
- **I-4 No silent skip**: every store has a disposition and every item a final status.
- **I-5 Authoritative-only conflict**: non-content entries never make a store "non-empty"; new-side non-content is never overwritten or deleted.
- **I-6 No runtime dual path**: after completion no engine reads the old root; only the allowlisted migration/residue readers may name it.
- **I-7 Receipt per run**: one file per run, distinct run ids, no shared aggregate.
- **I-8 Memory invariance**: two scopes, entry schema, derived index and six actions unchanged; only roots move.
- **I-9 Injection invariance**: seven/four/five field sets unchanged; memory source paths new.
- **I-10 Store disjointness**: every store root is disjoint; two concurrent writers on one store produce distinct per-entry paths (the 055 discipline survives the move).
