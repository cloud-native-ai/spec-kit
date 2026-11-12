# Data Model — Anchor / Goal Realignment

**Spec**: `.specify/specs/101-anchor-goal-realignment/` | **Date**: 2026-11-12
**Owner note**: this file models the entities this feature introduces or re-shapes. Field meanings
that already have an owner are cited, never restated: the binding record and the lifecycle table are
owned by `shared/definitions/anchor-definitions.md` (FR-002), the archive-layer value set by that
file's § Archive Layers (FR-030), and the classification rules by `requirements.md` FR-036.

## 1. Relationship view

```text
                 ┌───────────────────────────────┐
                 │ Anchor (project-level)        │
                 │ .specify/anchoring/<slug>/    │
                 │   anchor.md                   │
                 │   summary/  (derived)         │
                 └───────┬───────────────┬───────┘
        anchor_slug (N:1)│               │ owns 0..N
                         │               ▼
┌────────────────────┐   │        ┌─────────────┐
│ Team definition    │◄──┘        │ Target T-NNN│
│ .specify/teams/…   │            └─────────────┘
└─────────┬──────────┘
          │ disposition (0..1)
          ▼
┌──────────────────────┐        ┌──────────────────────────┐
│ Team disposition     │        │ Goal (action-level)      │
│ receipt              │        │ .specify/goals/<slug>/   │
└──────────────────────┘        │   goal.md  (no Targets,  │
                                │   no team binding)       │
                                └──────────────────────────┘

  Classification record ──drives──► migration / archive ──emits──► Migration/archive receipt
```

Two stores, two file names, one shared schema: `anchor.md` and `goal.md` carry the same frontmatter
keys and the same binding record; only their **location**, their **section headings**, and their
**permitted contents** differ.

## 2. Entities

### E-1 Anchor

| Aspect | Value |
|--------|-------|
| Identity | directory slug `anchor-slug` under `.specify/anchoring/`; grammar owned by the engine's `is_valid_identity` (FR-007) |
| Definition file | `.specify/anchoring/<anchor-slug>/anchor.md` ([[STR-001]]) |
| Required frontmatter | `status` (`active`/`achieved`/`abandoned`), `created`, `updated`, `binding` (E-3) |
| Required sections | `## Objective` (outcome-shaped, GD-2/GD-3 apply), `## Success Criteria` (≥1, verifiable), `## History` (append-only) |
| Optional | `## Targets` (0..N, E-5), `## Boundaries` |
| Derived | `summary/` subtree, written only by the summary flow (see `research.md` R-06) |
| Mutators | `/speckit.anchor` → `manage-anchor` → `goal-utils.py` (sole definition writer) |
| Invariants | name shape enforced (FR-024); no team binding from the Anchor side; lifecycle terminal states retained, never deleted (FR-025) |

### E-2 Goal (action-level)

| Aspect | Value |
|--------|-------|
| Identity | directory slug `goal-slug` under `.specify/goals/`; same grammar |
| Definition file | `.specify/goals/<goal-slug>/goal.md` ([[STR-002]]) |
| Required frontmatter | `status`, `created`, `updated`, `binding` (E-3) |
| Required sections | `## Guidance` (steps allowed), `## Completion Conditions` (≥1, verifiable), `## History` |
| Optional | `## Migrated Targets` (only for a definition migrated by this feature, R-07) |
| Forbidden | `## Targets` as a live mechanism, team binding inbound, any position in the control hierarchy |
| Mutators | `/speckit.goal` → `manage-goal` → `goal-utils.py` |
| Invariants | MUST NOT be resolvable as an Anchor identity (FR-023); no GD-2 shape check on guidance (FR-024); terminal states retained (FR-025) |

### E-3 Binding record (shared)

Owned by `anchor-definitions.md` (FR-002) — this table is a consumer view only.

| Key | Domain | Notes |
|-----|--------|-------|
| `owner` | `sdd-run` / `command-run` / `human` | closed set (existing engine `OWNER_VALUES`) |
| `owner_id` | run id, or `human` | matches the state spine's `run_id` vocabulary |
| `origin` | `null` or an existing `.specify/specs/<dir>` basename | validated against the tree |

Every Anchor, every Goal, and every team definition carries exactly these three keys, no fourth.
Migration and archival preserve the record byte-for-byte inside the concept digest.

### E-4 Anchor–Team binding (`anchor_slug`)

| Aspect | Value |
|--------|-------|
| Carrier | `team.md` frontmatter, one line: `anchor_slug: <anchor-slug>` ([[STR-003]]) |
| Cardinality | N teams : 1 Anchor; no array, no reverse field on the Anchor |
| Resolution | the slug MUST exist as `.specify/anchoring/<slug>/anchor.md`; a slug present only under `.specify/goals/` MUST NOT resolve |
| Rename | `goal_slug` → `anchor_slug` is a **one-line structural edit**; every other byte of the file is preserved (FR-047) |
| Lifecycle | independent of the Anchor's lifecycle state (an achieved Anchor still resolves) |

### E-5 Target (`T-NNN`)

Unchanged mechanism, carried by the Anchor row: identity `^T-\d{3}$`, states `open` / `done` /
`dropped`, legal transitions owned by the engine (FR-015). Goals never own Targets. Preservation
across migration/archival is E-8's duty (R-07).

### E-6 Lifecycle state

Shared by Anchors and Goals: `active` → `achieved` | `abandoned`; terminal is absorbing for writes
except a `human`-owned reopen (D-3). Owner: `anchor-definitions.md`; consumers MUST NOT re-declare a
second table.

### E-7 Classification record

| Field | Domain / rule |
|-------|---------------|
| `slug` | one of the 14 inventory entries |
| `class` | `anchor` / `action-goal` / `obsolete` |
| `rule` | `FR-036(a)` / `FR-036(b)` / `FR-036(c)` |
| `targets` | integer, read from the definition at decision time |
| `summary` | boolean, whether a `summary/` tree exists |
| `evidence` | free text naming the measured basis (prose record only; not consumed by the engine) |

Machine-readable form: `.specify/specs/101-anchor-goal-realignment/classification.json`
(`schema: 101-classification/v1`), which also carries the team dispositions. It is a **plan
artifact** read verbatim by the cleanup action; implement never edits it.

### E-8 Migration / archive receipt

One JSON file per acted entry, placed **inside the action target**.

| Field | Anchor migration → `.specify/goals/<slug>/migration-receipt.json` | Obsolete archival → `.specify/archive/anchoring/<slug>/migration-receipt.json` |
|-------|-------------------------------------------------------------------|-------------------------------------------------------------------------------|
| `schema` | `101-migration-receipt/v1` | same |
| `action` | `migrate-action-goal` | `archive-obsolete` |
| `source_path` | `.specify/anchoring/<slug>/goal.md` | `.specify/anchoring/<slug>/goal.md` |
| `target_path` | `.specify/goals/<slug>/goal.md` | `.specify/archive/anchoring/<slug>/goal.md` |
| `concept_digest_source` | sha256 (mapped projection of the source) | sha256 (raw normalized projection) |
| `concept_digest_target` | sha256 (same mapping) — MUST equal source | MUST equal source |
| `mapping_version` | `101-mapping-v1` | `101-mapping-v1` (identity mapping) |
| `result_identity` | the `goal-slug` | the archived `slug` |
| `engine` | `goal-utils.py` + version string | same |
| `timestamp` | ISO-8601 UTC | same |
| `delete_policy` | literal `archive-not-delete` ([[STR-005]]) | same |
| `targets` | `[{"id": "T-001", "statement": "…", "status": "open"}]` preserved verbatim | same |
| `summary` | `moved` / `absent` | `moved` / `absent` |

Rules: one receipt per entry (never a shared aggregate); digest computed before and after through
**the same declared mapping**; second run reports `already-migrated` / `already-archived` with no
second receipt and no diff (FR-043); an interruption records the stage reached and resumes it
(FR-044); a slug that already exists with a non-equivalent digest is refused with both candidates
named (FR-045).

### E-9 Archive layers and destinations

| Layer | Read/write root | Definition file | `--scope` member |
|-------|-----------------|-----------------|------------------|
| Anchor store | `.specify/anchoring/<slug>/` | `anchor.md` | `anchor` |
| Goal store | `.specify/goals/<slug>/` | `goal.md` | `goals` |
| Team store | `.specify/teams/<slug>/` | `team.md` | `teams` |
| Read-only resolver | across the three above | — | `auto` |
| Historical destination | `.specify/archive/anchoring/<slug>/` (archived entries) + `.specify/archive/goal-team/` (094's pre-existing destination, untouched) | `goal.md` (as archived) | not a scope member |

The retired member `goal` is not a layer name any more and MUST fail as an invalid value
(FR-030); no alias exists.

### E-10 Team disposition receipt

One file per affected team: `.specify/teams/<slug>/disposition-receipt.json`.

| Field | Value |
|-------|-------|
| `schema` | `101-disposition-receipt/v1` |
| `team_slug` | the team directory name |
| `bound_slug` | the entry the team was bound to before cleanup |
| `disposition` | `R1` / `R2` / `R3` |
| `state` | `apply` / `already-satisfied` |
| `reason` | one line, matching `classification.json` |
| `acted` | what changed: `anchor_slug` written, Anchor created, `lifecycle_state: archived` |
| `timestamp`, `engine` | as E-8 |

### E-11 Stores and their layouts

```text
.specify/anchoring/<anchor-slug>/anchor.md          # definition (engine-written)
.specify/anchoring/<anchor-slug>/summary/           # derived (summary flow)
.specify/goals/<goal-slug>/goal.md                  # definition (engine-written)
.specify/goals/<goal-slug>/migration-receipt.json   # one per migrated entry
.specify/goals/<goal-slug>/summary/                 # moved derived tree (frozen), if any
.specify/archive/anchoring/<slug>/**                # archived tree + migration-receipt.json
.specify/teams/<team-slug>/team.md                  # definition (anchor_slug)
.specify/teams/<team-slug>/disposition-receipt.json # one per affected team
```

Concurrent-writer check: two branches touching different slugs write disjoint paths at every level
above; there is no shared `.jsonl` and no mutable index. `summary/` remains the only non-engine
writer surface, and it is per-slug.

## 3. State transitions

| Entity | From | Event | To |
|--------|------|-------|----|
| Anchor / Goal | `active` | `status --set achieved` / `abandoned` | terminal, retained |
| Anchor / Goal | terminal | `status --set active` (owner `human` only) | `active`, history row appended |
| Anchor | `goal.md` present | `archive-cleanup --apply`, class `anchor` | same slug, file renamed to `anchor.md`, summary regenerated if present |
| Anchor | `goal.md` present | `archive-cleanup --apply`, class `action-goal` | absent from the store; `.specify/goals/<slug>/goal.md` + receipt |
| Anchor | `goal.md` present | `archive-cleanup --apply`, class `obsolete` | absent from the store; `.specify/archive/anchoring/<slug>/` + receipt |
| Team | bound | cleanup rename step | `anchor_slug` (same value) |
| Team | `active` | disposition R3 | `lifecycle_state: archived` (retained on disk) |
| Team | `archived` | explicit modify | `active` (out of scope for this feature) |

## 4. Validation rules (engine-enforced)

1. Identity grammar and path-segment safety on every slug (no `/`, no `\`, no `.`/`..`).
2. Layer→filename resolution: the engine derives the file name from the resolved layer; no caller
   supplies a filename and no module-level single-filename constant survives (FR-029).
3. `--scope auto` requires exactly one candidate layer; zero → exit 2 `not-found`, two → exit 2
   `scope-ambiguous` (FR-031).
4. Every write action names its layer; `auto` is read-only and a write through it exits 2
   (existing `scope-read-only` contract).
5. A cleanup action never writes the other group's store (FR-032): the definition-cleanup group
   touches `.specify/anchoring|goals|archive/anchoring` and team frontmatter; the goal-action group
   touches `.specify/goals` only.
6. Concept-digest equality is the migration's post-condition; `delete_policy` is the only literal
   that survives both layers' variation.
7. A receipt is written before the source is removed and re-read on resume; a source without a
   receipt is a defect the action refuses to create (FR-044).
