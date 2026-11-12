# Contract — `goal-utils.py` (single engine, layer-parameterized)

**Engine**: `scripts/python/goal-utils.py` → `.specify/scripts/python/goal-utils.py` (mirror).
**Scope of this contract**: the executable surface — actions, layers, exit codes, write matrix,
idempotency and the consumers that must move with it. Concept fields are owned by the two definition
files; this contract never restates them.

## C-23 — One engine, three layers, three file names

The engine resolves a definition's file name **from the layer**, never from a module-level constant
(FR-029):

| Layer | Root | Definition file |
|-------|------|-----------------|
| `anchor` | `.specify/anchoring/<slug>/` | `anchor.md` |
| `goals` | `.specify/goals/<slug>/` | `goal.md` |
| `teams` | `.specify/teams/<slug>/` | `team.md` |

`DEFINITION_FILENAME` as a single global MUST NOT survive; every call site that needs a file name
asks the layer. `summary_dir()` is layer-aware in the same way.

## C-24 — `--scope` closed set ([[STR-004]])

`("anchor", "teams", "goals", "auto")`. The value set's owner is
`shared/definitions/anchor-definitions.md` § Archive Layers; `--help` cites that owner and the parser
projects the set mechanically (argparse `choices`). The retired member `goal` MUST fail as an invalid
choice (exit 2) and MUST NOT be aliased; so MUST the retired singular `team` (existing fixtures move
to `teams`).

## C-25 — `auto` resolution

`auto` resolves exactly one layer for a requested slug: zero candidates → exit 2 `not-found`;
two or more → exit 2 `scope-ambiguous` naming the layers. `auto` is read-only: a write action under
`auto` exits 2 `scope-read-only` (existing semantics, three layers now).

## C-26 — Action groups (FR-032)

| Group | Actions | Store it may write |
|-------|---------|--------------------|
| anchor (existing semantics, anchor store) | `create`, `status`, `objective`, `criteria`, `migrate` | `.specify/anchoring/**` definitions (+ the team inline reference for `migrate`) |
| goal (new, clearly prefixed) | `goal-create`, `goal-list`, `goal-view`, `goal-modify`, `goal-status` | `.specify/goals/**` only |
| cleanup (new, independently named) | `cleanup --check` / `cleanup --apply` | `.specify/anchoring|goals|archive/anchoring` + team frontmatter (see C-35) |
| shared reads | `list`, `validate`, `binding`, `targets`, `run-checks`, `command-family`, `handoff-decision`, `probe-residual`, `resolve-scope` | none |
| shared writes | `bind`, `handoff-ref`, `migrate-archive`, `backfill-bindings`, `check-statement` | the layer named by `--kind` / the declared target |

No action in one group may write another group's store. `goal-*` actions default `--scope goals`;
a caller passing `--scope anchor` to a `goal-*` write gets `cross-layer-write` (exit 2).

**Cross-cutting message rule (FR-016)**: every user-facing string this engine emits names the command
that owns the action under the split — hints for `targets` / `migrate` / `migrate-archive` /
`coordinate` say `/speckit.anchor` and never `/speckit.goal`. The sites measured today are eight hints
in `run-checks` / `preview-target-check` (`goal-utils.py:1274, 1294, 1304, 1310, 1360, 1363, 1377,
1393`) plus the mirrored copy; residue class C6 (`research.md` §5) is the guard, so a new hint that
regresses the wording turns the scan red rather than relying on a hand-kept list.

## C-27 — Anchor group (adapted, same semantics)

| Action | Change from today |
|--------|-------------------|
| `create <slug> --objective … [--criterion …] [--boundary …]` | writes `anchor.md`; GD-2/GD-3 unchanged |
| `status <slug> --set <state>` | unchanged (lifecycle owner unchanged) |
| `objective <slug> --set …`, `criteria <slug> [--criterion …|--clear]` | unchanged, prior value recorded in `## History` |
| `migrate <team-slug> [--drop-inline]` | derives an **Anchor** from the team's inline goal (`anchor.md`), not a Goal |
| `list [--scope anchor\|goals]` | default `anchor`; `goals` lists the Goal store. **Measured today**: `list` ignores `--scope` entirely and always enumerates the anchor store — so the default reading is unchanged and the `goals` member is new. `--scope teams` on `list` exits 2 `scope-not-applicable`: no team-listing surface exists today and this feature does not invent one |

## C-28 — Goal group (new)

| Action | Contract |
|--------|----------|
| `goal-create <slug> --guidance <text> --done <text> [--done …] [--title …]` | requires ≥1 `--done`; no GD-2 shape check on guidance; writes `.specify/goals/<slug>/goal.md` with `status: active` and a binding record |
| `goal-list` | read-only enumeration of the Goal store (slug, status, completion-condition count, updated) |
| `goal-view <slug>` | read-only rendering; exit 3 when absent |
| `goal-modify <slug> [--guidance <text>] [--done <text> …] [--clear-done]` | writes; prior value appended to `## History`; `--clear-done` is the one destructive write and requires the explicit flag |
| `goal-status <slug> [--set active|achieved|abandoned]` | no `--set` reports; `--set` transitions under the shared lifecycle table; terminal retained |

Cross-cutting: every `goal-*` action refuses a slug that exists in the anchor store with the same
identity (exit 2, both candidates named — the two stores are distinct namespaces and a collision is
an authoring error, not a merge).

## C-29 — Cleanup group (new)

`cleanup --check --classification <path>` and `cleanup --apply --classification <path>`.
`--check` performs every read and decision and writes nothing. `--apply` executes the plan in the
phase order owned by `contracts/migration-cleanup.contract.md`. `--scope` is not applicable to this
group: passing it exits 2 `scope-not-applicable`.

## C-30 — Exit codes (single meaning each)

| Code | Meaning | Cleanup-specific use |
|------|---------|----------------------|
| 0 | success (including an idempotent no-op) | `already-migrated` / `already-archived` / `already-normalized` |
| 2 | input error | unreadable/invalid/`schema` mismatch classification file, incomplete team set, `--scope` passed, unknown action |
| 3 | not found | a declared entry's source is missing and no receipt explains it |
| 4 | invalid state | target slug exists with a non-equivalent concept digest; a receipt-less half state (I5 below); a definition that cannot be interpreted |
| 5 | blocked | unused by this feature (kept for `run-checks`) |

## C-31 — Single writer (definition surface)

Only `goal-utils.py` writes definition files under `.specify/anchoring/**` and `.specify/goals/**`.
Declared exception, by path suffix: `<slug>/summary/**`, written by the existing summary flow
(`skills/internal/create-team/scripts/build-summary-input.py`) — a derived subtree, not a definition
(FR-011 / FR-028 as corrected in this plan's `PLAN-EDIT` block).

The audit is a contract test that scans every code path under `scripts/`, `skills/` (both mirror
layers), `src/` and `templates/` for write primitives whose resolved target can fall under either
store, with `goal-utils.py` and the declared summary writer as the only allowlisted subjects. The
test also injects a synthetic writer and asserts the audit turns red (SC-006).

## C-32 — Consumers that must move in the same change

| Consumer | Required change |
|----------|-----------------|
| `scripts/python/sdd-route.py` | second projection `--scope choices` → four members |
| `scripts/python/concurrency-check.py` | reads `.specify/anchoring/<slug>/anchor.md` |
| `skills/external/sdd-project-setup/scripts/logical-framework.py` | checks `.specify/anchoring/*/anchor.md`; names `/speckit.anchor` |
| `skills/external/sdd-house-keeping/scripts/logical-framework.py` | same engine, same change |
| `skills/internal/create-team/scripts/build-summary-input.py` | reads/writes `.specify/anchoring/<slug>/summary/`; user-facing text names Anchor |
| `src/specify_cli/__init__.py` | `MIGRATE_STATIC_POINTERS` owner → `/speckit.anchor`; migrate hint text; optional-command list gains `/speckit.anchor` |
| `scripts/python/validate-requirements.py` and peers | no change unless they read the engine's scope list (they do not) |

## C-33 — Declaration-style actions

`command-family --command <name>` answers **per layer**:
`{"command": "...", "in_family": <bool>, "layers": {"anchor": <bool>, "goal": <bool>, "team": <bool>}}`
where `in_family` is the disjunction (FR-027). Existing consumers that read a single boolean move
to `in_family`.

`resolve-scope`, `handoff-decision`, `probe-residual` keep their shapes; `handoff-ref` validates
`anchor_slug` / `team_slug` and writes the reverse `handoff_ref`.

`run-checks` emits the binding identity under the key `anchor_slug` (FR-016 / FR-033). The pre-change
key `goal_slug` MUST NOT survive in its JSON payload; `team_slug`, `identity_kind`, `binding`,
`resolution`, `checks`, `verdict` and `blocked` keep their names and meanings. Callers that read the old
key are updated in the same change (C-32).

## C-34 — Interface contract

`-h` / `--help` and `--version` answer without acting; an undeclared option is rejected
(Constitution XXI, FR-034). The `_sig_guard` declared-option list gains exactly: `--classification`,
`--guidance`, `--done`, `--clear-done`. `--check` / `--apply` already exist and are reused.

## C-35 — Cleanup write matrix (group boundary)

| Step | Writes | Must not write |
|------|--------|----------------|
| anchor rename (`goal.md` → `anchor.md`) | `.specify/anchoring/<slug>/` | any other store |
| anchor body normalization (A-N-1…A-N-4) | matching lines in `.specify/anchoring/<slug>/anchor.md` + `anchor-body-receipt.json` | any non-matching line; any other store |
| action-goal migration | `.specify/goals/<slug>/**` | the anchor store |
| obsolete archival | `.specify/archive/anchoring/<slug>/**` | any live store |
| team structural rename | one frontmatter line in `.specify/teams/<slug>/team.md` | body lines |
| team body normalization | lines matching the declared rewrite table only | anything else in the file |
| disposition R3 | `lifecycle_state` line + removal of the binding line | the rest of the team file |

Every step is per entry and resumable; see the phase machine in
`contracts/migration-cleanup.contract.md` C-44.
