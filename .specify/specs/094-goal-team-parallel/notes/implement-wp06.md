# Implement wp06 — owners and guards

**Package**: `wp06-owners-guards` · **Rows**: T073–T078 (6/6) ·
**Branch**: `094-wp06` (base `f4e9ae4c1`, master @ wp01–wp05) ·
**Date**: 2026-11-09

**ANOMALY: the full-tree `sync-mirrors.py --check` exits 2 on two pre-existing wp04 source files whose mirrors are absent from HEAD — `skills/internal/create-team/references/handoff-contract-template.md` and `skills/internal/create-team/scripts/territory-check.py` (verified with `git ls-tree HEAD`: both sources tracked, both `.specify/skills/...` mirrors untracked) — so `test_mirror_parity_suite.py` reads 2 failed at fork entry; the wp06 scoped check is clean and this fork did not project another package's files.**

## Rows closed — 6 / 6

| Row | What landed | Guard / reading |
|-----|-------------|-----------------|
| T073 | framework-map Goals row → `.specify/anchoring/<slug>/`; Teams row already named `.specify/teams/<slug>/`; new "Goal/team archive history" row names `.specify/archive/goal-team/` (`receipts/` + `trees/`, archive-not-delete, never a read surface); Feature specs row now explicitly denies a goal/team subdirectory | `test_framework_map_archive_row.py::test_the_framework_map_names_the_unified_archive_and_drops_spec_local_goal_team` — green in `wp06-final-guards.txt` |
| T074 | goal template exposes `migrate-archive` (argument hint, seven-mode delegation, a mode paragraph citing the engine's action table); positioning drops the spec-scoped framing; both templates cite the scope owner by pointer and restate no value set; team template drops `<spec-dir>/team/` and gains no migration mode | `test_goal_command_template.py` 2 guards (goal + team) — green; red in `wp06-red-guards-2.txt` |
| T075 | manage-goal: seven modes incl. `migrate-archive`, create writes `.specify/anchoring/<slug>/goal.md`, archive resolved to `REPO_ROOT/.specify/anchoring/`, `probe-residual` read group, exit codes 0/2/3/4/5 cited to the engine, new § 7 `migrate-archive`. run-team: summary lands at `.specify/anchoring/<goal-slug>/summary/`, `run-checks` payload's additive `binding` key documented (T048's delegated half). improve-team verified already compliant (conceptual-model + create-mode cited; no old paths in SKILL.md) — no edit | `test_binding_model.py::test_the_three_management_skills_cite_owners_and_restate_no_arguments` — green; red in `wp06-red-guards-2.txt` |
| T076 | `test_no_spec_local_writes.py`: parses the engine's action table from the module docstring and `--help`, pins the nine write actions, pins the three sanctioned roots (`ARCHIVE_DIRNAME` / `TEAM_DIRNAME` / `ARCHIVE_HISTORY_DIRNAME`), AST-asserts that no function performing a write references `_specs_root` / `.specify/specs`, scans the create-team persistence step (SKILL.md + create-mode.md) and the driver instructions (SKILL.md + checkpoint-protocol.md) for spec-local targets | `test_no_writing_surface_targets_a_spec_local_goal_or_team` — green |
| T077 | Mutation arms in the same module: an engine root reverted in memory (`ARCHIVE_DIRNAME` → `.specify/specs/900-fixture/goal`) produces a constant violation; the create-mode persistence target reverted in memory produces a prose hit; a re-injected `temporary goal` phrase hits the C-107 pattern set imported from wp05's module. No tree edits | `test_the_guard_goes_red_when_one_surface_is_reverted` + `test_the_vocabulary_scan_goes_red_when_one_old_phrase_is_re_injected` — both passed at red time and after |
| T078 | Engine half (`probe-residual`, readonly, scratch-area exclusion) pre-landed by wp02; this package adds the `/speckit.sanitize` read surface: `probe-residual` rendered verbatim with per-kind counts, residuals never read as current definitions, no migration action or side effect, `.specify/.tmp/` excluded, migration entry pointed to `/speckit.goal` | wp02's `test_archive_migration.py::test_the_residual_probe_is_read_only_and_ignores_the_run_scratch_area` (green) + `test_no_spec_local_writes.py::test_the_sanitize_template_renders_the_probe_without_migrating` (red before the template edit, green after) |

## Readings (one file per reading, under `test-evidence/`)

- `wp06-red-guards.txt` — first red run; contains the parser's own help-regex defect (kept, not rewritten).
- `wp06-red-guards-2.txt` — corrected red: **6 failed, 2 passed** (the two mutation arms pass by construction).
- `wp06-green-guards.txt`, `wp06-green-guards-2.txt` — intermediate runs that surfaced the missing `.specify/teams/<slug>` landing in manage-goal (kept as dated readings).
- `wp06-green-guards-3.txt` — **9 passed**, exit 0: the three new modules (1+2+4), T075's guard, wp02's residual-probe guard.
- `wp06-final-guards.txt` — **32 passed**, exit 0: the 9 guards plus `test_directory_governance.py` (23) after the mirror projection.
- `wp06-neighbourhood.txt` — 5 failed / 151 passed at first pass: the stale governance pin (fixed) + 4 pre-existing `test_migration_distribution.py` failures caused by the missing `.specify/specs/069b-isomorphism-migration-metrics/` tree at HEAD (not this package).
- `wp06-neighbourhood-2.txt` — **138 passed** across binding model, criterion vocabulary, driver skill, checkpoint protocol, archive migration, targets engine, run-skills wiring, skill visibility, directory governance (plus the 1 serial-only pass), exit 0.
- `wp06-mirror-check.txt` — full-tree check: 2 MISS (the disclosed wp04 drift) + every other pair byte-identical; exit 2.
- `wp06-mirror-check-scoped.txt` / `-2.txt` — wp06 scoped check: 2+1 files byte-identical, exit 0.
- `wp06-copy-check.txt` — `regen-command-copies.py --check`: OK, exit 0.
- `wp06-mirror-parity.txt` — `test_mirror_parity_suite.py`: 2 failed / 834 passed; both failures are the disclosed wp04 drift.

## Commits

- `e1cf741c1` — `feat(094-wp06): owners, guards and the residual read surface (T073–T078)` (25 files).
- `e324de76d` — `chore(094-wp06): project the mirrors and the regenerated command copies` (15 files).
- this close-out commit carrying the note. No push.

## Write-domain adjudications (disclosed, not silent)

The dispatch enumerated six paths. Five edits sit outside that enumeration; each is the
minimal change an assigned row names, and none touches a path another concurrent package
(`wp04b`) owns:

1. `templates/commands/goal.md` and `templates/commands/team.md` — named by T074's evidence
   column and clause C-97/C-98; wp05 had already rewritten their scope lines, but the
   `migrate-archive` mode, the spec-scoped positioning and the `<spec-dir>/team/` hint were
   still open. The guard module (`test_goal_command_template.py`) is in the enumerated set,
   and it cannot go green without these two edits.
2. `tests/contract/test_binding_model.py` — the § Mutable-state map lists wp06 (T075) as an
   append owner of this module; the guard function is appended at the end.
3. `tests/contract/test_directory_governance.py` — its framework-map pin asserted
   `` `.specify/goal/<slug>/` ``, a fact FR-029 retires; without the one-line update the
   module turns newly red against the plan baseline (C-104). This pin belongs to no
   package's declared domain.
4. `skills/internal/improve-team/SKILL.md` — named by T075's evidence but **not edited**:
   the file already cites the concept and create-mode owners and names no retired path, so
   the guard passes on it unchanged.
5. `templates/commands/sanitize.md` — enumerated (T078's owned half).

## Residual risks / follow-ups for the driver

1. **Full mirror check is red on wp04's two unprojected files** (the ANOMALY). Projection is
   `sync-mirrors.py --write` at integration — a one-command fix, but it belongs to wp04's
   file set, and wp04b is concurrently based on the same commit.
2. **Stale `.specify/goal/` literals outside every package's domain**: `create-team/SKILL.md`
   § Run Workspace and five `create-team/references/*` files (summary delivery paths),
   `improve-team/references/goal-editing.md`, and the generator `build-summary-input.py`
   (its delivery root constant). None is a goal/team *definition* write target, none is a
   FR-022 criterion hit (the wp05 scan is green), and T073–T078 name none of them. They are
   the same class wp05 disclosed; the directory rename's full sweep remains unowned.
3. **The engine's docstring action table omits `resolve-scope`** (a read action). The
   structural invariant pins the *write* set, so this is legal by C-106's subject; recorded
   here as a measured observation rather than an engine edit (outside every package's
   domain).
4. **`test_migration_distribution.py` 4 failures** are pre-existing: the referenced
   `.specify/specs/069b-isomorphism-migration-metrics/` tree is absent at HEAD (a
   consolidation-archive effect, unrelated to this package).
5. **`test_run_checks.py::test_c1_…` roster pin** remains red from wp01/wp02 (disclosed by
   both); wp06 does not touch it.
