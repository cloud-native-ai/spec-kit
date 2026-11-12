# Implement evidence — WP-01a (T006–T015)

Run `r20261112T064607Z-b101`; feature `101-anchor-goal-realignment`; package WP-01a
(tasks T006–T015); stage base commit `7920dc7b5`.

**Comparison baseline (E2, not re-run):** `test-evidence/suite-baseline-entry.txt` — rc=1,
8900 passed, 192 pre-existing failure ids, 3 skipped. Every reading below is targeted; a
pre-existing failure id counts as "not regressed" when it is absent from the selected paths of
these runs.

## T006 — owner file move (commit `9d9043502`)

| Field | Value |
|-------|-------|
| Command | `git mv shared/definitions/goal-definitions.md shared/definitions/anchor-definitions.md`; then `git diff --cached --stat -M`; `git show --stat -M --oneline HEAD` |
| rc | 0 |
| Selected paths | `shared/definitions/anchor-definitions.md` |
| Result | rename detected at 100% similarity (`{goal-definitions.md => anchor-definitions.md} | 0`); no content byte changed at this commit |
| Follow readings | recorded in `notes/red-first-evidence.md` (both files' `git log --follow`) |

Correction disclosed: the first attempt staged the move **and** a reconstructed `goal-definitions.md`
in one commit; git then recorded a plain file creation instead of a rename (the old path still
existed with identical content). The commit was re-made (it was local, unpushed, seconds old) as a
pure rename so the T006 evidence obligation is measurable. T008 recreates the Goal owner from blob
`3e1c0a4f0`, which is what keeps "content changed owner" readable in history.

## T007 — Anchor owner rewrite (FR-001, FR-002, FR-007, FR-008, FR-009, FR-030)

| Field | Value |
|-------|-------|
| Command | heading + terminology assertion over `shared/definitions/anchor-definitions.md` (inline `python3 -`) |
| rc | 0 |
| Selected paths | `shared/definitions/anchor-definitions.md` |
| Result | required headings all present — `# Anchor Definitions Reference`, `## What an Anchor Is`, `### Archive Layers`, `### The Binding Record`, `### Lifecycle`, `## Target Decomposition (目标切片)`, `## Anchor–Team Binding`, `## Terminology Boundaries` → `headings: PASS` |
| G-3 heading assertion | `PASS` — the headings the later `tests/contract/test_anchor_definitions.py` (T064) keys on exist in the owner itself; the store-side half of G-3 is out of this package |
| SC-010 restatement material | each of the four confusable terms has exactly one dedicated table row: `**Anchor** (锚点)` → 1, `**anchoring archive** (锚点档案)` → 1, `**Re-Anchoring** (重新锚定)` → 1, `**action-level Goal** (行动级目标)` → 1; each row states both the referent and what it is NOT |
| Scope ownership | § Archive Layers carries the four-member closed set `anchor` / `teams` / `goals` / `auto`, states the retired member `goal` fails as an invalid value with no alias, and says the engine `--help` cites this section by path |
| Sole-owner split | binding record (three keys) and lifecycle (three values + transition discipline) are declared owned here; the Goal owner is cited by path and MUST NOT restate them |

## T008 — Goal owner rewrite (FR-003, FR-004, FR-005, FR-024)

Rebuilt from the pre-move blob (`3e1c0a4f0`) as a **new** action-level file; the pre-move
content stays readable on the Anchor path through the T006 rename.

| Field | Value |
|-------|-------|
| Command | C1 residue patterns (research §5, four regexes) over `shared/definitions/goal-definitions.md` and over the pre-move blob; plus retired-path / authoring-entry greps |
| rc | 0 |
| Selected paths | `shared/definitions/goal-definitions.md` |
| Result — C1 | pre-move blob **0**, rewritten file **0** (these regexes never matched this file's old "first-class concept" phrasing; the convergence is the semantic rewrite, recorded below) |
| Result — semantic residue | `first-class` → **0** occurrences; `project-level` / `long-horizon` occur only where they name the **Anchor** as the different concept or in the retirement mapping — never as a predicate of a Goal |
| Result — retired paths | `.specify/goal` (not followed by `s`) → **0**; `/speckit.goal` → **0** |
| Result — schema closure | frontmatter key set `status` / `created` / `updated` / `binding`; section set `## Guidance` / `## Completion Conditions` / `## History` required, `## Migrated Targets` / `## Boundaries` carry-over only; the file states the `anchor_ref` refusal and exit 2 |
| Result — no restatement | the three-key record and the lifecycle table are cited to `anchor-definitions.md` § The Binding Record / § Lifecycle; no key domain or transition is re-enumerated in this file |

## T009–T011 — layer filenames, the closed `--scope`, and `auto`

All readings below are actual commands; `G` is `scripts/python/goal-utils.py`, run from a
scratch repo under `.specify/.tmp/wp01a/` seeded with two anchors (`alpha`, `gamma`) and two
Goals (`beta`, `quick-task`).

| Obligation | Command | rc | Result |
|---|---|---|---|
| interface contract | `python3 $G --version` | 0 | `goal-utils.py 0.0.22` |
| interface contract | `python3 $G --help` | 0 | roster shows the new groups; `--scope {anchor,teams,goals,auto}` and the help text cites `shared/definitions/anchor-definitions.md § Archive Layers` by path |
| layer filenames (C-23) | `grep -n "DEFINITION_FILENAMES\|def definition_filename" $G` | 0 | `{"anchor": "anchor.md", "goals": "goal.md", "teams": "team.md"}`; `definition_filename()` is the only accessor and `layer_root()`/`summary_dir()` go through it |
| T010 retired `goal` | `python3 $G goal-view gamma --scope goal` | 2 | `invalid choice: 'goal' (choose from 'anchor', 'teams', 'goals', 'auto')` — no silent fallback |
| T010 retired `team` | `python3 $G goal-view gamma --scope team` | 2 | `invalid choice: 'team'` (the closed set has plural `teams` only) |
| T011 auto, one layer | `python3 $G goal-view beta --scope auto` | 0 | resolves the goals layer and renders the definition |
| T011 auto, missing | `python3 $G goal-view nope --scope auto` | 2 | `not-found: no archive layer contains slug 'nope' (checked .specify/anchoring, .specify/goals and .specify/teams)` |
| T011 auto, two layers | `python3 $G goal-view gamma --scope auto` (both `anchoring/gamma` and `goals/gamma` seeded) | 2 | `scope-ambiguous: … (anchor, goals) …` — no guess is made |
| T011 write under auto | `python3 $G goal-create auto-goal --guidance "run the report" --done "the report exists" --scope auto` | 2 | `scope-read-only: --scope auto resolves a single archive layer for reads only …`; `ls .specify/goals` unchanged (zero writes) |

## T012 — the action-level Goal group

| Obligation | Command | rc | Result |
|---|---|---|---|
| create writes only `goals/<slug>/goal.md` | `python3 $G goal-create beta --guidance "run the weekly check" --done "the check ran" --done "the report exists" --title Beta` | 0 | `created: .specify/goals/beta/goal.md`; frontmatter `status/created/updated/binding`, sections Guidance / Completion Conditions / History |
| list | `python3 $G goal-list` | 0 | `beta active done=1`, `quick-task active done=1`, `steps-ok active done=1` |
| view | `python3 $G goal-view beta` | 0 | renders guidance, `conditions: ['the check ran', 'the report exists']`, `migrated_targets: []`, history |
| modify records the prior value | `python3 $G goal-modify beta --guidance "run the daily check" --done "the check ran"` | 0 | history gains `guidance changed; prior value: run the weekly check` and `completion conditions changed; prior value: the check ran | the report exists`; conditions are the replacement set, not an append |
| clear conditions allowed | `goal-modify … --clear-done` | 0 | the conditions section renders the explicit no-criteria marker (FR-019); a Goal is not forced to keep one condition on modify |
| status reports without `--set` | `python3 $G goal-status beta` | 0 | `status: active`, `changed: False` |
| terminal is absorbing | `goal-status beta --set achieved`; `goal-modify beta --guidance again`; `goal-status beta --set active` | 0 / 2 / 0 | the modify is refused (`terminal-goal … only a human-owned reopen`), the record is retained in place (not deleted), and the explicit reopen is accepted |
| cross-layer write refused, both layers named | `python3 $G goal-create gamma --guidance "step one" --done done` with `anchoring/gamma/anchor.md` present and no `goals/gamma` | 2 | `cross-layer-collision: slug 'gamma' already names the Anchor .specify/anchoring/gamma/anchor.md … .specify/goals/gamma/goal.md is refused and nothing is written` |
| Anchor pointer key refused | `goal-view bad` over a Goal carrying `anchor_slug` | 4 | `goal-schema: … declares Anchor pointer key(s) anchor_slug; an action-level Goal carries no Anchor reference — the only cross-reference is the binding record's origin` |
| slug collision check covers both files | `_assert_goal_identity_free` reads `goal.md` **and** `anchor.md` in the anchor layer | — | an un-migrated anchor stored as `goal.md` also blocks the Goal write (pre-rename state is not a bypass) |

`auto` still resolves a pre-rename anchor (`anchoring/<slug>/goal.md`) as the anchor layer —
`_anchor_layer_contains` accepts either filename — so the transition window does not make an
existing anchor unreachable.

## T013–T015 — the cleanup shell, mapping/digests/receipts, idempotency and resume

Fixture method: a full clone of the repository with `.git` under `.specify/.tmp/wp01a-clean/`
(the classification's `baseline_commit` resolves there), plus a fault fixture. Readings:

| Obligation | Command | rc | Result |
|---|---|---|---|
| real tree, read-only | `python3 $G cleanup --check --classification .specify/specs/101-anchor-goal-realignment/classification.json --repo-root .` | 0 | `check {'archive': 2, 'migrate': 3, 'rename+normalize': 9}` — exactly the 9+3+2 split; zero writes to the live tree |
| T013 input verdict | `cleanup --apply` with an incomplete classification (entries not covering the live anchor store) | 2 | `classification-invalid: … ; not on disk: …` / `unclassified: …` — nothing written |
| T013 `--scope` refused | `cleanup --check … --scope anchor` | 2 | `scope-not-applicable: … --scope does not apply to it and nothing is written` |
| full apply | `GOAL_UTILS_CLEANUP_FAULT_AFTER` unset, `cleanup --apply` on the clone | 0 | 9 `anchor.md` + 0 `goal.md` in the anchor store, 3 migrated Goals, 2 archived obsolete trees, 5 receipts + 9 body receipts |
| T014 mapping | per-entry diff of receipt pairs | — | only the three FR-039 changes: location, `## Objective`→`## Guidance`, `## Success Criteria`→`## Completion Conditions`; `## Targets` re-rendered under `## Migrated Targets` (088's two statements survive verbatim; receipt carries `{id, statement, status}`) |
| T014 digest | recompute `migration_digest()` over source and target with the mapping applied | 0 | every `concept_digest_source == concept_digest_target` (C-39: sha256 over normalized frontmatter projection + `\n\n` + body without Targets) |
| T015 second apply | `cleanup --apply` again on the same clone | 0 | `git status --porcelain` = 0 lines; results `already-normalized` ×9, `already-migrated` ×3, `already-archived` ×2 (C-41 three-condition rule) |
| T015 half-state | delete one receipt, keep the target, source already removed | 4 | `half-state: .specify/goals/091-auto-git-closeout/goal.md exists without …/migration-receipt.json and its source is gone …` |
| T015 digest conflict | append one line to a migrated target | 4 | `conflict: … does not match its receipt … (recorded digest …, measured …); both paths are named and nothing is rewritten` |
| T015 target loss | drop one Targets row in a source while the classification declares 2 | 4 | `migration-target-loss: … declares 2 Target(s) but 1 could be carried into the migration … (FR-040)` |
| T015 resume at `write-target` | `GOAL_UTILS_CLEANUP_FAULT_AFTER=write-target cleanup --apply` | 3 | `result: interrupted`, `reached_phase: write-target`, `target_exists: true`, no receipt, source present |
| T015 resume at `write-receipt` | plain re-invocation | 0 | decision `action: resume-receipt`, `resumed_at: write-receipt`; target + receipt written, source removed |
| T015 resume at `remove-source` | `GOAL_UTILS_CLEANUP_FAULT_AFTER=write-receipt cleanup --apply` then plain re-invocation | 3 / 0 | fault leaves receipt + source; the resume reports `already-migrated` with `resumed_at: remove-source` and removes the source |

Corrections found by these runs and repaired in place (all disclosed per the fast-fail rule):

- `layer_root()` looked up `<layer>_root`, but `Scope` exposes `anchor_root` / `goals_root` /
  `team_root`; the mismatch raised `AttributeError` for every legacy action (`run-checks`,
  `migrate`, `migrate-archive`, `binding`). Fixed with an explicit layer→attribute map.
- The cleanup receipt builder was named `_receipt_body`, colliding with the 094
  `migrate-archive` receipt builder of the same name (the later definition silently won and
  broke `migrate-archive` with `TypeError`). Renamed to `_migration_receipt_body`; the legacy
  function is untouched.
- The legacy `bind` / `binding` actions pass their own kind vocabulary (`goal` / `team`);
  mapping it straight into `--scope` made the retired member kill a working legacy call. The
  kind now translates to `anchor` / `teams`; only an explicit `--scope goal` still fails at
  exit 2.
- The coverage pre-check swallowed the T015 half-state: a receipt-less target was reported as
  "not on disk" (exit 2) instead of reaching the exit-4 `half-state`. Coverage now treats a
  present target as accounted for, so the state table decides.

## Targeted test readings (E2 baseline not re-run)

Command (through the project runner, never a bare test CLI):

```text
bash scripts/bash/run-tests.sh tests/unit/test_goal_utils.py tests/unit/test_goal_scope_engine.py \
  tests/contract/test_script_interface_contract.py tests/contract/test_goal_definition.py \
  tests/contract/test_goal_targets_engine.py tests/contract/test_archive_migration.py \
  tests/contract/test_migration_interruption.py tests/contract/test_binding_model.py \
  tests/contract/test_scope_resolution.py tests/integration/test_goal_migration_path.py \
  tests/integration/test_archive_migration_real_data.py tests/contract/test_goal_command_template.py \
  tests/contract/test_run_checks.py tests/contract/test_focus_target_resolution.py -q
```

Reading: **rc=1, 293 passed, 56 failed, 1 skipped**. All 56 are the transition class — tests
still encoded to the pre-inversion contract, owned by later tasks, and none is a behavioral
regression of the four repaired defects above (those now pass):

| Group | Count | Why red | Owner / closes at |
|---|---|---|---|
| `test_binding_model.py` | 14 | asserts the Goal owner text and the old scope surface | T025 (WP-01b) |
| `test_scope_resolution.py` | 5 | `--scope goal` and the old `Scope` API (`goal_root`) | T025 |
| `test_goal_targets_engine.py` | 13 | reads `anchoring/<slug>/goal.md` (incl. the mirror `engine == mirror`, unsynced) | T017/T018 (mirror sync), T025 |
| `test_run_checks.py` | 9 | fixtures seed `goal.md`; the live-repo cases also wait for the applied migration | T025, T049–T054 |
| `test_archive_migration.py` | 3 | asserts `anchoring/<slug>/goal.md` after the legacy migration | T025, T049–T054 |
| `test_script_interface_contract.py` | 3 | `sync-mirrors --check` sees the edited source vs the not-yet-synced mirror | T017/T018 |
| `test_goal_migration_path.py` | 1 | asserts the retired `.specify/goal/<slug>/summary/` path | T025 |
| `test_goal_definition.py` | 1 | asserts `anchoring/<slug>/goal.md` | T025 |
| `test_archive_migration_real_data.py` | 1 | reads the live repo before the migration is applied | T049–T054 |
| `test_goal_scope_engine.py` | 5 | old Scope API / `auto` picking a `goal` layer | T025 |
| `test_goal_utils.py` | 1 | asserts `anchoring/<slug>/goal.md` | T025 |

Every failing node is absent from the E2 baseline by construction (it was green when the
baseline was captured, i.e. before the concept inversion landed in this branch).

## Forward overlaps disclosed

- The derived `summary/**` move is performed inside the P2 entry action (T013–T015 work) so the
  E-8 `moved`/`absent` field is recorded truthfully at action time (C-40); T054 remains the
  verifying and repair step.
- Team rename, dispositions and final self-checks (FR-046…FR-049) are T016 (WP-01) and were
  not implemented here; the classification validator only checks that the affected team set
  and its disposition vocabulary are complete.
- The live tree was never written: all `--apply` runs happened on clones under
  `.specify/.tmp/`; the real-tree reading is `--check` only.
