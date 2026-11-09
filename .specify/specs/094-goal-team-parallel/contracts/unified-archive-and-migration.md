# Contract — Unified Archive, Migration and Residual Probe

Owner of the executable rules: `scripts/python/goal-utils.py` — the actions `migrate-archive` and
`probe-residual` of the existing engine (RS-003/RS-004). No second executable body is introduced (FR-012).
Command entry: `/speckit.goal` mode `migrate-archive` (FR-030, T-006); `/speckit.sanitize` renders the read-only
probe reading.

## 1. Archive layout

- **C-31**: The unified archive MUST be exactly `.specify/goal/<slug>/` and `.specify/teams/<slug>/` (FR-007).
  A goal definition lives at `.specify/goal/<slug>/goal.md`, a team definition at `.specify/teams/<slug>/team.md`;
  every other file a definition owns (goal `summary/`, team `runs/`, `.work/`) stays inside its own `<slug>/`.

(FR-007)
- **C-32**: The migration destination history MUST live at [[STR-003]] `.specify/archive/goal-team/` with exactly
  two subdirectories: `receipts/` (one YAML file per migrated definition, named `<kind>-<slug>.yaml`) and `trees/`
  (the moved source trees, at `trees/<spec-dir-name>/<kind>/<slug>/`). Two branches migrating different
  definitions MUST write different paths — never a shared index, never a `.jsonl` stream.

(FR-009, FR-010)
- **C-33**: A **migration receipt** MUST carry: `kind` (`goal` | `teams`), `source_spec`, `source_slug`,
  `target_slug`, `target_path`, `archived_path`, `concept_digest`, `result` (`migrated` | `noop` | `conflict` |
  `interrupted`), `at` (UTC ISO-8601), and the literal `delete_policy: archive-not-delete`. Receipts are immutable
  once written; a re-run that changes nothing MUST NOT write a second receipt (C-38).

(FR-009, FR-010)
- **C-34**: An **archive receipt** (the per-definition record left behind when a definition retires in place)
  MUST be written under `.specify/archive/goal-team/receipts/` with `result: archived` and MUST NOT be the read
  surface for current facts.

(FR-010)
## 2. Migration semantics

- **C-35**: `migrate-archive` MUST move, not copy, and MUST move **atomically per definition**: the target
  definition is written and validated first, then the source tree is moved to `trees/`, then the receipt is
  written. If the process stops between steps the receipt records `result: interrupted` with the reached step
  (C-39).

(FR-009, FR-010)
- **C-36**: The migration MUST preserve slug, definition body, lifecycle state and history lines verbatim, and
  MUST set `origin` to the source spec-directory name on every migrated definition (FR-009, A11). It MUST NOT
  rebuild any cross-definition lineage between a migrated team and its migrated goal.

(FR-009)
- **C-37**: archive-not-delete MUST hold for every path: no source file is deleted, the moved tree stays readable
  under `trees/`, and the receipt names where. A migration that would delete MUST refuse before writing anything.

(FR-010)
- **C-38**: `migrate-archive` MUST be idempotent: a second run over an already migrated tree MUST perform zero
  writes, emit `result: noop` for each definition on stdout, write no new receipt, and exit 0. A second run MUST
  NOT overwrite an existing unified-archive definition.

(FR-009)
- **C-39**: On interruption the run MUST report the reached step and the actual state (archived tree name,
  whether the target exists), exit 3 (distinguishable from 0 = complete and 2 = input error), and a second call
  MUST resume from that step: if the target exists and is equivalent it finishes the receipt; if the target is
  absent it finishes the write then the move. A resumed call MUST NOT move a source tree a second time (SC-011).

(FR-009, FR-010)
- **C-40**: Non-equivalent conflict MUST stop the migration for that definition: when the target slug exists and
  its **concept payload** (Objective, Success Criteria, Lifecycle status, Targets text) differs, the engine MUST
  refuse to overwrite, MUST name both candidates (existing path and source path) and MUST exit 4. The binding
  block MUST be excluded from the comparison .

(FR-009, FR-011)
- **C-41**: `concept_digest` in the receipt MUST be computed over the concept payload only (the same fields as
  C-40). The digest is what makes "did this definition change" answerable without re-reading both files, and it
  is what keeps C-38's `noop` decision from depending on the binding block.

(FR-011)
- **C-42**: The migration MUST accept `--dry-run`, which performs every read, computes every decision and prints
  the per-definition plan and the resulting receipt bodies, and writes **nothing** (no archive directory, no
  receipt, no definition). The dry-run and the real run MUST reach the same decisions (FR-042).
## 3. Residual probe

- **C-43**: `probe-residual` MUST be read-only: it enumerates `.specify/specs/*/goal/*/goal.md` and
  `.specify/specs/*/team/*/team.md`, reports one line per finding plus a count per kind, and writes nothing.

(FR-012)
- **C-44**: Residual directories MUST NOT be read as current definitions: every engine action except
  `probe-residual` MUST ignore them, and `list` MUST NOT include them. A residual may only be reported.

(FR-007, FR-012)
- **C-45**: `/speckit.sanitize` MUST render the probe reading verbatim and MUST NOT migrate (T-006). The reading
  carries the exact paths so a reader can act on each one.

(FR-012, FR-030)
## 4. No second write path

- **C-46**: After this feature, the number of code paths that write `.specify/specs/<spec>/goal/**` or
  `.specify/specs/<spec>/team/**` MUST be zero . The guard is a contract test over the writing
  surfaces (engine actions, `create-team` persistence, driver instructions), not a documentation claim.

(FR-007, FR-013)
- **C-47**: Every writing surface MUST be enumerable from one place: the engine's action table. A second
  executable that writes goal/team definitions is a defect, not an alternative.

(FR-007, FR-013)
- **C-48**: The unified archive directory MUST be registered in `shared/definitions/framework-map.md` (Goals /
  Teams rows plus the archive row, FR-029) before the migration can be run on a real tree.

(FR-029)
- **C-49**: Migration MUST NOT touch `.specify/.tmp/` (FR-037): the run scratch area is not an archive layer and
  MUST NOT be enumerated, migrated or reported as residual.

(FR-037)
- **C-50**: A migration MUST NOT run implicitly. No action of any engine, command or driver step MAY invoke
  `migrate-archive` as a side effect (A5); only the explicit `/speckit.goal migrate-archive` entry does.

(FR-009, FR-030)
## 5. Resident backfill (FR-043) and the real-data dry run (FR-042)

- **C-51**: The dry run MUST be executed against this repository's real tree once before the real migration, and
  both readings MUST be recorded as dated evidence under `<spec-dir>/test-evidence/`. The dry run MUST NOT delete
  or move anything.

(FR-042)
- **C-52**: The comparison baseline for the real migration MUST be the recorder probe reading
  `test-evidence/requirements-baseline-probe.txt`; the run MUST report residual before, migrated count, residual
  after (expected zero) and a per-definition existence assertion. The counts MUST be read from that probe run,
  never restated as a constant in a second document (SC-003).

(FR-042)
- **C-112**: The binding record requirement (C-1) MUST hold for **every** definition in the unified archive,
  including the residents that predate this feature. Measured 2026-11-09: `.specify/goal/*/goal.md` carries 6
  definitions and `.specify/teams/*/team.md` 12, and none carries a `binding` block. Those residents are NOT part
  of the migration subject (C-35, FR-009 names spec-local trees only), so a second, separate action owns them:
  `backfill-bindings`, a write action of the same engine with the same closed-subset reader (no second executable,
  FR-012's rule applied to this action too), accepting `--dry-run`, which prints the per-definition plan and writes
  nothing, and whose before/after readings MUST be recorded as dated evidence under `<spec-dir>/test-evidence/`,
  one file per reading.

(FR-043)
- **C-113**: `backfill-bindings` MUST write the record `owner: human`, `owner_id: human`, `origin: null` on every
  resident that has no binding block, MUST refuse (exit 2, naming the definition) a resident whose binding block is
  present but incomplete rather than overwriting it, MUST leave every other byte of the definition identical
  (C-6's comparison, applied to an insertion), and MUST be idempotent: a second run over a backfilled tree performs
  zero writes and reports one `already-bound` line per definition. The action MUST NOT run implicitly (C-50's rule).

(FR-043)
## Requirement coverage

FR-007, FR-009, FR-010, FR-011, FR-012, FR-013, FR-029, FR-030, FR-037, FR-042, FR-043; SC-002, SC-003, SC-004, SC-011, SC-012.
