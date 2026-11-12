# Contract — Migration / Archival / Team Disposition (`cleanup`)

**Engine action group**: `goal-utils.py cleanup --check|--apply --classification <path>`.
**Input record**: `.specify/specs/101-anchor-goal-realignment/classification.json`
(`schema: 101-classification/v1`) — a **plan artifact**, read verbatim, never edited by implement.
**Concept**: `data-model.md` E-7…E-11; classification rules: `requirements.md` FR-036.

## C-36 — Input validation (before any write)

1. The file must parse and carry `schema: 101-classification/v1`; anything else → exit 2.
2. Every `entries[*].class` must be one of `anchor` / `action-goal` / `obsolete`; `rule` must be one
   of `FR-036(a|b|c)`; a class/rule pair outside the mapping → exit 2.
3. **Completeness cross-check**: the entry set must equal the directory listing of
   `.specify/anchoring/*/` at run time, and the team set must equal the set derived from the
   classification × live `team.md` bindings plus the two recorded dangling bindings. A missing or
   extra row in either set → exit 2 naming the difference. The engine never invents a class.
4. `mapping_version` must be `101-mapping-v1`; a different value → exit 2.

## C-37 — Per-class actions

| Class | Action | Destination |
|-------|--------|-------------|
| `anchor` | rename in place `goal.md` → `anchor.md`; if `summary/` exists, mark it for regeneration (the summary flow rewrites it; the cleanup never hand-edits it) | same directory |
| `action-goal` | field-mapped migration (C-38) + receipt | `.specify/goals/<slug>/goal.md` |
| `obsolete` | identity-mapped archival (C-38) + receipt | `.specify/archive/anchoring/<slug>/` |

No action deletes a definition. Removal of the source is the last step of a move (C-42), and the
receipt always precedes it.

## C-38 — Field mapping (closed)

For `action-goal`: exactly three things change — file location, `## Objective` → `## Guidance`,
`## Success Criteria` → `## Completion Conditions`. Frontmatter keys (`status`, `created`, `updated`,
`binding`) are preserved byte-for-byte and **not bumped** (a bump would break the digest equality
required by FR-043). `## History` is preserved verbatim.

`## Targets` (FR-040): extracted from the body into the receipt's `targets` array with
`{id, statement, status}` verbatim, and **also** re-rendered into the migrated file under one fixed
heading `## Migrated Targets` as one bullet per statement (the id is not re-rendered; the receipt is
the identity record). A migration that would drop a statement is a hard failure, not a warning.

For `obsolete`: identity mapping (no section rename); `targets` recorded in the receipt; the whole
directory tree moves.

For `anchor`, two declared sub-steps, in this order:

1. **Rename (structural, byte-asserted)**: `goal.md` → `anchor.md`; the rename is the only change and
   every other byte is identical. The verifier asserts the two trees differ by file name only.
2. **Body normalization (line-scoped, receipted)** — the rule table below. Only matching lines are
   rewritten; each rewrite is recorded in
   `.specify/anchoring/<slug>/anchor-body-receipt.json` as `{path, line, rule, before, after}`, and a
   non-matching line MUST be byte-identical. This step is what makes FR-005 / SC-001 satisfiable for
   the retained anchors: without it the archive would keep speaking the retired terminology.

| Rule | Match | Rewrite |
|------|-------|---------|
| A-N-1 | `^\#\s*Goal:` | `# Anchor:` |
| A-N-2 | `.specify/goal\|teams` | `.specify/anchoring\|teams` |
| A-N-3 | `.specify/goal/<slug>/**` (incl. `/goal.md`, `/summary/`) | `.specify/anchoring/<slug>/**` |
| A-N-4 | `/speckit.goal` on a line that also matches A-N-1…A-N-3 | `/speckit.anchor` |

Measured surface at plan time: **9** A-N-1 lines (one per retained anchor) and **4** A-N-2/A-N-3
hits, all four inside `094-goal-team-parallel`. Zero hits means the step is a no-op for that entry,
recorded as `already-normalized` (exit 0).

## C-39 — Concept digest

```
projection(text) :=
  normalize( frontmatter_projection(text) + "\n\n" + body_without_targets(text) )

frontmatter_projection := the three preserved keys in fixed order (status, created, updated)
                           followed by the binding block rendered as
                           "binding:\n  owner: …\n  owner_id: …\n  origin: …"
body_without_targets    := body after the C-38 mapping, with the "## Targets" / "## Migrated Targets"
                           section removed entirely and with "## History" retained
normalize(s)            := CRLF→LF; rstrip each line; strip leading/trailing blank lines; ensure exactly one trailing "\n"

digest(text) := sha256( projection(text).encode("utf-8") ).hexdigest()
```

`concept_digest_source` is computed from the source **through the same mapping** used for the target,
which is what makes equality meaningful. For `anchor` entries that mapping includes the A-N rules, so
the digest is computed **before** the normalization step on the projected text and again after it —
the two readings MUST be equal, and the receipt records that pair. Both the source and the target
digest are written to the receipt; a mismatch after the move is a hard failure (exit 4) and the source
is not removed.

## C-40 — Receipt

One JSON per acted entry, inside the action target, named `migration-receipt.json` with the fields
fixed by `data-model.md` E-8 and the literal `delete_policy: archive-not-delete` ([[STR-005]]).
Summary disposition is recorded (`moved` / `absent`) and the moved tree is listed. Receipts are
per-entry files; there is no shared index.

## C-41 — Idempotency

The judgement is **target exists AND receipt exists AND digest matches**:

| Observed state | Result |
|----------------|--------|
| source present, target absent, no receipt | act |
| source present, target present, receipt present, digests equal | finish the move (remove source) → `already-migrated` |
| source absent, target present, receipt present, digests equal | `already-migrated`, zero writes |
| source absent, target present, no receipt | exit 4 `half-state` (a receipt-less target is a defect, never silently blessed) |
| target present, receipt present, digests differ | exit 4 `conflict` naming both paths |

A second full run after success therefore produces **zero diff and zero new receipts** (SC-007).

## C-42 — Interruption and resumption

Phases per entry, in this order: `read → project → write-target → write-receipt → remove-source`.
Each phase is observable on disk; a re-invocation reads the state and resumes at the first
incomplete phase, reporting `resumed-at: <phase>`. The receipt records the phase reached. No phase
removes a source before the receipt exists in the target.

## C-43 — Conflict

Target slug exists with a non-equivalent concept payload → **stop**, name both candidate paths,
write nothing (exit 4). Never overwrite, never pick a winner, never fall back to a suffix.

## C-44 — Phase order (global)

| Phase | Work | Resumable unit |
|-------|------|----------------|
| P1 | anchor renames (9 entries) **and** the declared body normalization (C-38 A-N-1…A-N-4) | one entry, one line |
| P2 | action-goal migrations (3) and obsolete archival (2) | one entry |
| P3 | R2 Anchor creation for `viz-skill-arena` (engine `migrate`) | one team |
| P4 | summary moves for migrated/archived entries (FR-049) | one entry |
| P5 | team structural rename for all 16 bound teams (C-45) | one team |
| P6 | team body normalization (C-46) | one team, one line |
| P7 | team dispositions R3 (C-47) | one team |
| P8 | self-checks: zero `action-goal` left in `.specify/anchoring/`, every `anchor_slug` resolves, every receipt present, no orphan `summary/` | whole run |

P2 precedes P3/P6 because normalized references and the R2 binding must point at existing targets.
P5 precedes P6 because the body rewrite must not race the frontmatter edit.

## C-45 — Structural rename (byte assertion)

For each of the 16 teams with `goal_slug`: change **only** the frontmatter key on that line to
`anchor_slug`. The verifier asserts that the unified diff of the step contains exactly one changed
line per file and that line is the binding line. The 4 unbound teams are byte-identical outputs.
`runs/**` is never touched.

For a team whose disposition is R3, the renamed line is removed by P7; the receipt records
`bound_slug`, so provenance survives and the FR-066 resolution assertion stays satisfiable.

## C-46 — Body normalization (declared rewrite table, line-scoped)

Only lines matching this table are rewritten; every rewrite is recorded in the team's
`binding-rename-receipt.json` as `{path, line, rule, before, after}`.

| Rule | Match | Rewrite |
|------|-------|---------|
| N-1 | `\bgoal_slug\b` in body text | `anchor_slug` |
| N-2 | `.specify/goal/<slug>/goal.md` | anchor class → `.specify/anchoring/<slug>/anchor.md`; action-goal → `.specify/goals/<slug>/goal.md`; obsolete → `.specify/archive/anchoring/<slug>/goal.md` |
| N-3 | `.specify/goal/<slug>/summary/` | anchor → `.specify/anchoring/<slug>/summary/`; action-goal → `.specify/goals/<slug>/summary/`; obsolete → `.specify/archive/anchoring/<slug>/summary/` |
| N-4 | `.specify/goal/<slug>/**` | same layer mapping, `**` preserved |
| N-5 | `.specify/goal/**` (no slug) | `.specify/anchoring/**` |
| N-6 | `/speckit.goal` on a line that also matches N-1…N-5 or contains `goal.md` | `/speckit.anchor` |

Out of scope by decision (recorded, not silently skipped): a team's `forbidden` list gains no new
`.specify/goals/**` entry; the engine's sole-writer invariant, not team territory, is what protects
the Goal store (`research.md` R-05 / FR-032).

## C-47 — Team dispositions (FR-046 / FR-048)

- **R1** — repoint `anchor_slug` to an existing Anchor; record evidence on the receipt. (No team
  qualifies in this feature: `classification.json` carries none.)
- **R2** — create the Anchor through the engine `migrate` action from the team's inline goal;
  the existing binding then resolves. `viz-skill-arena` only.
- **R3** — set `lifecycle_state: archived` **and remove the binding line**. Rationale: an archived
  team serves nothing, and FR-066 requires every `anchor_slug` on disk to resolve — repointing to an
  Anchor that does not cover the team's theme would be a false claim, and leaving the line would
  leave a dangling reference. Provenance lives in `disposition-receipt.json` (`bound_slug`, `reason`,
  `acted`). `091-auto-git-closeout` already carries `lifecycle_state: archived` but still carries its
  binding line and has no receipt; `classification.json` therefore records it as `apply`, and P7
  removes the binding line and writes the receipt — R3's terminal state includes the removal, and
  `already-satisfied` would have been a green on a team still holding a retired field.
- An undecidable disposition (not in the input file) is exit 2; the engine never guesses.

## C-48 — Summary trees (FR-049)

- anchor class: tree stays; regeneration is the summary flow's job, recorded as `regenerate` in the
  check output (never hand-edited here).
- action-goal / obsolete: the tree moves with the definition (`.specify/goals/<slug>/summary/` or
  the archive destination) and the receipt records `summary: moved`.
- A `summary/` whose definition is gone and which no disposition accounts for → exit 4
  `orphan-summary`, named. Nothing is deleted.

## C-49 — Evidence and guards

- `cleanup --check` output is captured in full to
  `test-evidence/cleanup-check-<date>.json` at first run (Single-Run Evidence); the apply run and a
  second apply are captured the same way.
- Guards: FR-064 (no `goal.md` remains in the anchor store, no action-goal entry left), FR-065
  (single **definition-file** writer; `summary/**` is the declared derived exception), FR-066 (no
  `goal_slug`, every `anchor_slug` resolves), FR-068 (idempotency, interruption, receipt completeness,
  digest equality, zero deletions), FR-069 (protected paths equal to `d7c9da7a3` —
  **baseline-existing entries only**; the `.specify/archive/anchoring/**` subtree this feature creates
  is an addition and is listed separately by the guard, per PLAN-EDIT 4).
- Post-convergence residue classes C5 (retained-anchor body: `^# Goal:` / retired `.specify/goal`
  refs), C6 (retired-mode hints still naming `/speckit.goal`) and C7 (`.specify/features.md` rows
  stating the old model) are declared with roots and baselines in `research.md` §5 and asserted by
  `tests/contract/test_live_semantic_residue.py`; the cleanup's own output is not exempt from them.
- `git status --porcelain` over the four stores before and after a second apply shows no new entry
  (the only allowed change between runs is nothing at all).
