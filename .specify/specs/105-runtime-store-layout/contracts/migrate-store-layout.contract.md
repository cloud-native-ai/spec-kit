# Contract — `specify migrate` store-layout dimension

**Spec**: `requirements.md` FR-013…FR-016, FR-024, FR-026 · **Plan**: `plan.md` WP07/WP08/WP09/WP13 · **Date**: 2026-11-25

The migration reuses the existing `specify migrate` structure: dry-run plan → single `--apply` authorization → archive-first execution → per-run receipt → deterministic outcomes. This contract defines the added dimension and every decision the planner/executor must make. It does not restate the six-value disposition domain, the outcome/exit-code table, or the archive-first criterion (owners: `097 requirements` FR-014/FR-019, `.specify/shared/guidelines/confirmation-gates.md`).

## M-1 Dimension extension and order

- `MIGRATE_DIMENSIONS` gains exactly one token, `store-layout`, appended last:
  `templates-generated, anchor-layout, compat-links, mirror-consistency, migration-residue, store-layout`.
- The five original tokens remain present, unchanged and in order, as the **prefix**. 097's `data-model.md` E-8 is a dated record and is not rewritten; the live owner of the extension is this contract, and the two 097 dimension-pin tests are re-pointed to assert (a) the prefix equality, (b) the full six-token set equality against this contract's declaration.
- Rationale for last position: anchor relocation removes `constitution.md`/`features.md` from the old container first; store relocation then empties each store; container removal sees only what no other dimension claimed. A project where `anchor-layout` refused still gets its stores relocated; the container is then preserved with the anchor residue reported.
- The store set itself comes from the declaration (C-6), never from a second list in the migration code. The migration code holds only the predicates and the executor.
- `store-layout` runs identically in `client` and `framework-source` workspace kinds; it depends on no reference tree and no tool surface.

## M-2 Planner — state classification

For each declared store, with `old = .specify/memory/<name>` and `new = .specify/<name>`:

1. **Symlink probe** — if `old` or `new` is a symlink: one item, `current=symlink`, `disposition=refuse`, `reason=symlink-source|symlink-target` naming the path. No following, no unlink.
2. **Enumerate entries** — walk `old` without following symlinks. Each entry is classified `authoritative`, `generated`, or `placeholder` by the store's `non_content` predicates from the declaration. `.gitkeep` and `*.lock` are placeholders for every store; per-store generated names cover `sanitize/*`, `trigger/telemetry.jsonl`, `tools/*.json` (and any other declared generated suffix).
3. **Dual content** — if `old` has ≥1 authoritative entry and `new` has ≥1 authoritative entry that is not the acting run's own receipt: one item, `current=dual-content`, `disposition=refuse`, `reason` names both roots and the repair entry ("human adjudication: merge manually or reconfigure"). Nothing moves.
4. **Path collision** — if `old` has an authoritative entry whose same relative path exists under `new` (any class): `disposition=refuse`, `reason=path-collision:<relpath>`. New-side non-content MUST NOT be deleted or overwritten to make room.
5. **Legacy content only** — `old` has ≥1 entry (authoritative or not), `new` has none of the colliding kind: `disposition=archive`, `mechanism=relocate`, `entries[]` = every old entry, classified, digested.
6. **Empty old** — `old` exists but has no entries: no store item; the container pass removes it (M-4).
7. **No old** — no item (converged), including the case where init already seeded a placeholder-only `new`.
8. **Permission** — if the dry-run's `os.access` probe says the target parent (or the source tree needed for the move) is unwritable: `disposition=refuse`, `reason=permission-denied` naming the path. Apply re-checks before acting.
9. **Container item** — if `.specify/memory` exists after the store items: one item `target=.specify/memory`, `current=empty-residue|unknown-residue`, expected `container-absent`. Unknown members are every remaining path not claimed by a store item, the anchor dimension, or the legacy non-store owner. Unknown residue item is `refuse` with `reason=unknown-residue` listing each path; empty residue item is `archive` with `mechanism=none` ("remove empty directory only").

Planner output MUST be deterministic: items sorted by (dimension order, target, relpath); repeated dry-runs on one tree serialize byte-identically (097 FR-006 preserved).

## M-3 Conflict predicate

- Conflict is counted **only** on authoritative entries, on both sides (A-7 as clarified 2026-11-25). The acting run's own receipt file does not count as new-side content.
- Non-content entries never trigger a conflict; they are never overwritten and never deleted. They move only when their relative target path is free; otherwise the item is refused by M-2 rule 4 and the old copy stays in place.
- "Looks identical" is not a merge licence: dual authoritative content refuses even when byte-equal (requirements Edge Cases).
- Old-side-only non-content with no authoritative entry is not a conflict; it relocates with the store (preserved), and never counts as content for the "empty old" case.

## M-4 Executor

For each `archive` store item, in dimension order:

1. Write the item's `entries[]` manifest into the run receipt (status `planned`) **before** the first move. This manifest is the archive record and the resume oracle; no byte copy is made (T-005; the 097 `relocate` precedent records from→to + digest, and a pure move destroys no content).
2. For each entry: if already at `to` with the recorded digest, mark `moved` (resume case); if `to` is occupied by a file not in the manifest, abort with `failed` (path collision discovered at execution is never auto-resolved); else `shutil.move(from, to)`.
3. After all entries: re-walk `old`; any remaining path is `left-in-place` and reported (never deleted).
4. Update the item `done`; append one `recover[]` row per moved entry (`path`=from, `archiveTo`=to, `change=relocated`, `digest`).
5. **Container pass**: after all store items, remove `.specify/memory` only when it is empty (including empty subdirectories left by the anchor dimension); otherwise record the residue item per M-2 rule 9 and leave everything in place.
6. A failure (OSError, digest mismatch, unexpected entry) marks the item `failed`, aborts the run, and leaves `status=aborted`; already-moved entries stay recorded, and the next run resumes from the receipt rather than re-deriving paths (097 C-7). There is no global rollback.

Executor invariants: zero writes in dry-run; no overwrite of any new-side path; no deletion of any object except an empty directory in the container pass; no archive directory under `.specify/archive/` for pure relocation (the manifest is the archive; `.specify/archive/migrate/` is used only by dimensions whose semantics require replacing/removing objects, per 097 C-7).

## M-5 Refusal and blocked classes (closed)

| `reason` token | Trigger | Effect |
|---|---|---|
| `symlink-source` | old store path is a symlink | refuse; name path; no follow |
| `symlink-target` | new store path is a symlink | refuse; name path; no follow |
| `permission-denied` | unwritable source/target per probe/re-check | refuse; name path; no partial success |
| `dual-content` | authoritative entries both sides | refuse; name both roots + repair entry |
| `path-collision:<relpath>` | same relative path both sides with old authoritative | refuse; name the relative path |
| `unknown-residue` | old container has unclaimed members after all stores | refuse; list every path; preserve |
| `no-recovery-path` | an action would be destructive without a recorded recovery | `blocked` (executor safety net) |

A `refuse`/`blocked` item MUST NOT be silently skipped: it stays in the plan and the receipt, and the run outcome is not `applied`.

## M-6 Receipt and resume

- New runs write `receiptVersion=2` receipts at `.specify/migrate/receipts/<run-id>.json` (the store's new root; `migrate_receipts_dir` is updated). The run's own receipt is created with `O_EXCL` before planning-as-applied begins; dry-runs write no receipt.
- Resume input: the most recent `status=running` receipt (or the last `aborted`). Version-1 receipts are read-only inputs during the transition: before the old receipts store has been relocated, the resume scan MAY read `.specify/memory/migrate/receipts/` as a legacy location — this is the migration engine's allowlisted legacy read (A-8), not a runtime fallback.
- Resume decisions use the old receipt's `entries[]`/`recover[]` and the current digests, never paths recomputed from the new run's assumptions.
- Idempotence: after a completed run, a second apply sees no old roots, emits no store items, and exits `clean`. A second dry-run is byte-identical to the first after completion.
- Concurrency: two simultaneous runs produce distinct run-id paths; the store items are guarded by digest/manifest checks, so a concurrent old-version writer produces a digest mismatch → `failed` + `aborted`, never silent loss.

## M-7 Ordering and interactions

- `anchor-layout` remains the only owner of anchor relocation; `store-layout` never moves `constitution.md`, `features.md`, or `features/` entries (they are not store entries).
- `migration-residue` MUST drop the obsolete `legacy-tools-registry` finding (`.specify/tools` flagged when `.specify/memory/tools` exists): the target semantics invert in this feature (A-5). No other residue class changes.
- The `migrate` receipt store is itself a store item (`migrate`); a run's own receipt is excluded from conflict counting (M-3).
- `specify init` never migrates; it seeds the new layout, skips legacy content, and prints the pointer to `specify migrate` (FR-013).
- After completion, no engine reads the old root; the only remaining readers are this migration, the anchor-layout migration, and the sanitize legacy-residue scanner (L-5).

## M-8 Fixtures and red-first acceptance

Fixtures are built from declarations, never from historical snapshots (`tests/fixtures/store-layout-105/builders.py`):

- `build_legacy`: new-layout shell + every store populated under `.specify/memory/` with at least one authoritative entry, a `.gitkeep`, and one generated artifact per store that declares one; no `.specify/<store>` roots.
- `build_seeded_legacy`: `build_legacy` after `specify init` (anchors at root, `session/`+`knowledge/` placeholders, tools inventory JSON) — the A-7 clarification case.
- `build_dual`: `build_legacy` + authoritative content under both roots for one store.
- `build_residue`: `build_legacy` + `draft/` and a stray `git-workflow.md`.
- `build_symlink`: `build_legacy` with one store symlinked to a sibling directory.
- `build_readonly`: `build_legacy` with the target parent mode read-only (skipped when running as root).
- `build_partial`: `build_legacy` after an interrupted apply (receipt `running`, half the entries moved, digests as moved).

Assertions (red-first until the executor exists):

| Fixture | Required reading |
|---|---|
| legacy | dry-run zero writes; apply relocates every entry; `diff -r` byte-identical; old roots gone; receipt v2 per run; container absent |
| seeded-legacy | generated/placeholder entries do not refuse; they are preserved where they are; merge proceeds |
| dual | `refuse`, `dual-content`, both paths named, both trees unchanged |
| residue | store items converge; container preserved; every residue path listed; nothing deleted |
| symlink | `refuse`, named path, link untouched |
| readonly | `refuse`, `permission-denied`, no partial success (root-skip recorded as a platform fact) |
| partial | resume moves only the remainder; no duplicate; no second archive record for moved entries |
| rerun | `clean`, zero moves, no old root recreated |

Each reading MUST have a red-ability drill: a mutation that removes the guard (e.g. deleting the conflict check) makes the corresponding assertion fail; the drill is recorded in `test-evidence/`.

## M-9 Outcome mapping

The existing outcome/exit-code table applies unchanged: `clean` 0 / `planned` 1 / `applied` 0 / `blocked` 3 / input error 2. A `store-layout` `refuse` or `blocked` makes the run `blocked` (3). The plan summary and text output list the new dimension and its items without changing the envelope.
