# Phase 0 Research: Goal Registry (037)

**Requirement**: `037-goal-registry` → Feature 041 Goal Registry
**Date**: 2026-08-05
**Method**: codebase exploration pass (Explore subagent) + direct execution (test baseline, path classification). Every count below was measured, not recalled.

## E-1. Migration surface is 24 live source files, not 37

`grep -rl 'project/goal'` over the repo (excluding `.git`, `.venv`) returns **51 text files**. Classified:

| Face | Count | Paths | Disposition |
|------|-------|-------|-------------|
| Canonical source | 4 | `skills/create-team/SKILL.md` (L62, 113, 647, 745); `skills/create-team/references/summary-mapping.md` (L12, 155); `skills/create-team/scripts/build-summary-input.py` (L14 docstring, **L577 live path literal**); `templates/commands/team.md` (L91, 96) | **Rewrite** |
| `.specify/` mirrors | 4 | mirrors of the four above | **Regenerate** via `sync-mirrors.py --write` |
| Per-tool generated copies | 5 | `.claude/commands/speckit.team.md` (L83,88); `.github/prompts/speckit.team.prompt.md` (L83,88); `.qoder/commands/speckit.team.md` (L83,88); `.opencode/command/speckit.team.md` (L83,88); `.qwen/commands/speckit.team.toml` (L106,111) | **Regenerate** — never hand-edit |
| Tests | 9 | `tests/contract/{test_summary_form_generator,test_summary_writeset,test_goal_identity,test_summary_trigger}.py`; `tests/integration/{test_summary_accumulation,test_goal_aggregation,test_goal_concurrent_refresh,test_summary_legacy_backfill,test_summary_four_patterns}.py` | **Rewrite path literals only** (FR-024: assertions must not weaken) |
| User docs | 1 | `docs/reference/commands/team.md` (L68, 80 — layout tables) | **Rewrite** |
| Tool record | 1 | `.specify/memory/tools/build-summary-input.py.md` | **Rewrite** |
| **Live subtotal** | **24** | | |
| Historical (append-only / archived) | 18 | `.specify/specs/036-team-summary/**`; `.specify/specs/037-goal-registry/**`; `.specify/memory/feedback/**`; `.specify/memory/features*` | **MUST NOT rewrite** |
| Build artifacts | 9 | `**/__pycache__/*.pyc` | Ignore |

**Decision D-1**: FR-022 / SC-011 are scoped by face — live residual MUST be 0, historical rewrites MUST be 0. A whole-repo zero is unachievable by construction: the 2026-08-04 Clarifications entry quotes `.specify/project/goal/` verbatim as the user's directive, and rewriting it would falsify the record. Spec corrected accordingly before this plan was filled.

**Decision D-2**: `test_summary_trigger.py:215` asserts `"project/goal/" in text` across the canonical file, its mirror, and all 5 tool copies. It **breaks by design** on migration and must be updated to the new path in the same change — this is the concrete instance of FR-024's "paths updated only, assertions not weakened".

## E-2. The old directory is not materialized — migration carries no data

`.specify/project/` contains only `project.md` plus gantt/milestones/wbs `.puml/.png/.svg` from the `manage-project` era. `.specify/project/goal/` **does not exist**; `build-summary-input.py:602` creates it on demand (`out_path.parent.mkdir(parents=True, exist_ok=True)`, annotated "FG-11 — only here"). `.specify/goal/` does not exist either.

**Decision D-3**: this is a pure code/doc/test migration with no data move and no transitional dual-path state in this repo. The spec's "迁移期新旧路径并存" edge case is retained as a guard for consuming projects but is vacuous here. `tests/integration/test_summary_four_patterns.py:192-200` guards that the real tree stays byte-unchanged, so it doubles as the regression net for the migration.

## E-3. Generator: one construction site, mirror byte-identical

`skills/create-team/scripts/build-summary-input.py` (675 lines); `.specify/` mirror verified byte-identical (`diff` clean).

- **L577** `delivery_dir = repo_root / ".specify/project/goal" / goal_slug` — the **only** construction site.
- L578 default `--out` = `delivery_dir / "data/project-input.yaml"`; L602 the sole `mkdir`; L607 lock `out_path.parent / ".refresh.lock"`; L645–647 `.tmp` + `os.replace` atomic write; L656 report field `delivery_dir`.
- CLI (L529–539): required mutually-exclusive `--goal` | `--team`, plus `--out`, `--baseline`, `--repo-root`, `--json`.
- Exit codes (L37–40): `0` OK, `2` input error, `3` no material, `4` serialized (`LOCK_STALE_SECONDS=900`).

**Decision D-4**: the path migration is a **one-line change plus its derived defaults** (L577 → `.specify/goal/<slug>/summary`), which is why FR-022's risk is concentrated in the *reference surface*, not the generator logic.

## E-4. Territory has zero executable validation today

`skills/create-team/SKILL.md:204-231` "Territory Division" specifies: rules (extract domains → map READ/WRITE sets → **Zero Write Overlap** → read overlap allowed → shared writes to a **Forbidden Write List**, Lead-only), a Territory Manifest (`Task`, `Write Scope`, `Read Scope`, `Forbidden`), and a 4-item validation checklist. Related: L244 dispatch payload, L263-266 worktree isolation, L738 "Territory validation MUST pass before parallel dispatch".

Searching `*.py|*.sh|*.mjs` across `scripts/ skills/ src/ tests/ shared/` for `territory` returns **zero files**.

**Decision D-5**: territory is 100% prose guidance for the LLM, scoped **intra-team and per-member**. So US5 is not "extend a validator" — it is "write the first executable territory validator, at a new (team) scope". This is the largest new-code surface in the requirement and the reason FR-036's normalization rules must be specified rather than assumed.

## E-5. team.md schema is prose-only; only `goal_slug` is validated

Schema lives solely as prose + a fenced YAML example at `skills/create-team/SKILL.md:32-88`. Frontmatter keys (L36-64): `name`, `slug`, `description`, `goal`, `goal_slug`, `pattern`, `preset`, `created`, `updated`, `members[]` (with a **commented-out per-member `territory`** at L51), `config` (incl. `summary.{enabled,every,delivery_dir,interactive}`). Invariant bullets at L83-87.

Executable parsing is limited to `build-summary-input.py`: `split_frontmatter` (L92-103) and `Team.__init__` (L136-143) read `slug`/`name`/`pattern`/`description`/`goal`; `goal_slug` at L148; `members` at L403. **Validation** exists only for `goal_slug` (L187-188, DDL grammar + path safety). There is no team.md schema validator script.

**Decision D-6**: the team-level `territory` key goes after `goal_slug` (L42), with an invariant bullet after L84, in both canonical and mirror. Because nothing validates the schema today, FR-035's declaration needs a **parser extension in `build-summary-input.py`** (the only existing team.md reader) rather than a new standalone parser — reusing the one place that already resolves teams by goal.

## E-6. Ride-along point for overlap detection is exact

- Trigger boundaries table: `SKILL.md:650-658`; continuous phase 9 SUMMARIZE at L599-602; per-pattern hooks at L258 / 386 / 523.
- **Gate order (hard sequence)**: `SKILL.md:660-673` — 1 Budget → 2 Cadence → 3 Material → 4 refresh.
- Status-line contract L675-689; enablement/opt-out L691-699; section header L639-648.
- Contract tests pinning it: `tests/contract/test_summary_trigger.py` (L44-52 SUMMARIZE-after-REPORT; L212-215 delivery-dir disclosure).

**Decision D-7**: prose-side, overlap detection is a step inserted **between gate 3 (Material) and gate 4 (refresh)** — after `SKILL.md:666` — so it runs only when a refresh actually happens, and the status-line vocabulary at L677-679 is extended. Code-side, the ride-along point is `resolve_goal()` (L175-197), which **already collects every team sharing a `goal_slug`** at L190-192; territory comparison belongs there, emitting into `gaps`/`meta` (L512-519) so it surfaces in the report (L653-669). This is what makes FR-041's "zero new trigger machinery" literally true.

## E-7. New command surface: 5 tool copies, no command-count test blocks it

Authoritative fan-out config is `_ASSISTANT_COMMAND_DIRS` / `_ASSISTANT_EXTENSIONS` / `_ASSISTANT_ARG_FORMATS` at `src/specify_cli/__init__.py:132-165` (8 tools), but `regen-command-copies.py:51-58` (`_tool_dirs()`) only regenerates directories that **already exist**. Present today (19 files each): `.github/prompts` (`.prompt.md`), `.claude/commands` (`.md`), `.qwen/commands` (**`.toml`**, `{{args}}`), `.opencode/command` (`.md`), `.qoder/commands` (`.md`). Absent and therefore skipped: `.hermes/commands`, `.iflow/commands`, `.codex/commands`.

Files required for `/speckit.goal`: `templates/commands/goal.md` (source) → `.specify/templates/commands/goal.md` (mirror, `regen-command-copies.py:145-147`) → the 5 per-tool copies → `docs/reference/commands/goal.md` (that directory holds exactly 19 files, 1:1 with templates, **no index.md**) → command-table rows in `docs/tutorials/quickstart.md:224` and `docs/tutorials/installation.md:93`.

**Decision D-8**: no test enumerates or counts all commands strictly, so adding one is safe. `tests/integration/test_ai_tools_command_coverage.py:34-97` globs dynamically and asserts only a core subset. **One test needs a deliberate edit**: `tests/contract/test_feedback_command_classification.py:19-29` hard-codes `COMPLEX_COMMANDS` (14) and `SIMPLE_COMMANDS` (4) with `assert len(...)` pins. `/speckit.goal` is a process-interaction command that creates and modifies artifacts through a confirmation gate, so it belongs in **COMPLEX** (bumping the pin 14→15) and MUST carry the `## Feedback` and `## Documentation` wrap-up steps like `/speckit.team`. `tests/contract/test_team_command_routing.py:24` is the routing-test pattern to clone.

## E-8. Goal guidance files already point at the new home

| File | Size | Current stance |
|------|------|----------------|
| `skills/create-team/references/goal.md` | 3,217 B | Already calls the Goal a "project-level first-class entity at `.specify/goal/<goal-slug>/`" and defers to `goal-definitions.md`; still documents team-side `goal` frontmatter + `## Goal` |
| `skills/improve-team/references/goal-editing.md` | 4,777 B | Inline-goal editing rules; no filesystem home; defers to `create-team/references/goal.md` |
| `skills/create-team/references/optimization-goals.md` | 8,160 B | Classifies optimization goals and picks a team shape; no storage location |
| `shared/definitions/goal-definitions.md` | 9,808 B | The concept authority. L7 "persisted under `.specify/goal/<goal-slug>/`"; L75-79 storage tree; **L80 delegates the layout inside `<goal-slug>/` to the implementing feature** |

All four have same-size `.specify/` mirrors.

**Decision D-9**: FR-019's rewrite is smaller than feared — `references/goal.md` already names the new home and the authority. The work is (a) pointing concept statements at `goal-definitions.md`, (b) pointing goal *content* at the instance definition, and (c) confirming no file re-states the concept as a second account. **D-10**: `goal-definitions.md:80` is the explicit delegation that authorizes this plan's `goal.md` + `summary/` layout — recorded with a line number so it is not re-litigated.

## E-9. Fixtures are the ready-made overlap test bed

`tests/fixtures/teams/` holds 4 teams (`goal-share-a/`, `goal-share-b/`, `parallel-fixture/`, `serial-fixture/`), each with `team.md` + `items.jsonl` + `runs/20260801T090000Z-report.md`, plus a `README.md` documenting the contract ("Fixtures are inputs, never outputs"). All four declare `goal_slug` at `team.md:8`; **`goal-share-a` and `goal-share-b` deliberately share `shared-harvest-goal`**. None declares `territory`.

**Decision D-11**: the two `shared-harvest-goal` fixtures are the natural test bed for FR-036/FR-037 — add `territory` to both (one pair overlapping on writes, one pair read-only-overlapping) rather than authoring new fixtures.

## E-10. Test baseline

Measured before any change: **40 failed / 1308 passed / 1 skipped** (`pytest -q`, 20s). Names frozen in `baseline-failed.txt`.

Diff against 036's merge baseline (39 failed / 1309 passed): exactly one new failure, `tests/contract/test_specify_script_paths.py::TestSpecifyScriptPaths::test_review_prerequisite_flags_are_supported`. Root cause established by running it: it asserts `tasks.md` appears in `AVAILABLE_DOCS`, which is only true when the current spec directory has a `tasks.md`. Branch `037-goal-registry` has none yet.

**Decision D-12**: this is a **branch-state-dependent** assertion, not a defect and not attributable to this requirement; it will pass again once `/speckit.tasks` produces `tasks.md`. Recorded so implementation does not mistake it for a regression. Incidentally it confirms the `Related Feature` binding is machine-readable — the script emitted `"FEATURE_ID":"041"`, `"FEATURE_NAME":"Goal Registry"`.

## Carry-forwards to `/speckit.tasks`

- **O-1** The `--goal-id` naming question (spec Assumptions) resolves to: `/speckit.goal` needs no new script option if the goal engine takes a positional identity; decide when the contract lands.
- **O-2** FR-030 (measured by degree) needs a progress representation decision in the data model — criteria carry no current-value field, since that would be derived data inside an authored file (FR-007).
- **O-3** The two-level territory consistency check (member territory ⊆ team territory) has no home yet: `build-summary-input.py` reads `members`, so it is reachable, but it is a team-run concern rather than a summary concern.
