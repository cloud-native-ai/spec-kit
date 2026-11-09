# Implement report — wp04-handoff (094-goal-team-parallel)

Package: `wp04-handoff`, rows **T055–T062** (8 rows) of `tasks.md` § Package Map, plus
**T049/T050**, whose guard modules (`tests/contract/test_handoff_contract.py`,
`tests/contract/test_handoff_territory.py`) are this package's declared write domain and
which wp03 explicitly delegated to wp04 (`notes/implement-wp03.md` § Residual risks item 3).
Tree: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/094-wp04`
(branch `094-wp04`, base `51f3b8289` — master with wp01 + wp02 + wp03 + enginefix).
Date: 2026-11-09. No push, no subagents, no additional worktrees, no merge, no `--force`.

Write domain used — exactly the dispatch's four surfaces:
`tests/contract/test_handoff_contract.py`, `tests/contract/test_handoff_territory.py`,
`skills/internal/create-team/` (new template + new script + SKILL.md section),
`skills/internal/improve-team/SKILL.md` — plus this package's `notes/` and
`test-evidence/` outputs. `scripts/python/goal-utils.py`,
`shared/declarations/contract.yaml`, `tests/contract/test_declaration_facts.py`,
`templates/`, and every mirror under `.specify/` were **not touched**.

## Per-row closure

| Row | Status | Evidence |
|-----|--------|----------|
| T049 | **closed** (delegated from wp03 by domain) — three-way key pair resolves in both directions over a fixture whose handoff instance is instantiated from the authored template. | `test-evidence/wp04-T049-T059-T060-test_the_three_way_keys_resolve_in_both_directions.txt`; red reading in `wp04-red-handoff-modules.txt` |
| T050 | **closed** (delegated from wp03 by domain) — the four spec artifacts are refused by `territory-check.py` with non-zero exit naming the path and the seat; a granted path is allowed; archive layers refuse; a broad write grant still loses to `territory.forbidden`. | `wp04-T050-T062-test_a_crew_write_onto_a_spec_artifact_is_refused_by_the_territory_check.txt` |
| T055 | **blocked — module outside the dispatch domain** — the guard lives in `tests/contract/test_declaration_facts.py`, which wp03 owned and which the dispatch excludes (see ANOMALY). The threshold literal stays a one-file edit: no file this package authored pins the number (the template cites no threshold; the action is never named with a number). | — |
| T056 | **closed by wp03** (domain-assigned: `shared/declarations/contract.yaml` is "wp03 only" in the Mutable-state map). Verified still green in this package's neighbourhood run. | `wp04-package-neighbourhood.txt` (test_declaration_facts.py green) |
| T057 | **blocked — engine + test module outside the dispatch domain** — the *engine half* is already implemented by the enginefix and verified here: a registration rewritten to `subset_id: yaml/v0` makes `handoff-decision` exit 2 with `declaration-invalid` naming both grammars. The row's guard (`test_a_fact_in_another_grammar_is_refused_at_load`) is in `test_declaration_facts.py` and is not authored by this package. | `wp04-T057-engine-grammar-refusal.txt` |
| T058 | **blocked — same domain gap** — the additive registration exists (wp03) and both consumers are in scope (`goal-utils.py` actions; `create-team` citations); the row's guard (`test_registration_is_additive_and_both_consumers_are_in_scope`) is in `test_declaration_facts.py`. | `wp03-T056-green.txt`; § Residual risks |
| T059 | **closed** — `handoff-contract-template.md` authored: eight mandatory sections in order, `handoff/v1` frontmatter, two-terminal-state machine retained-never-deleted, fixed `<spec-dir>/handoff.md`, production by `tasks` only, `None.` for an empty section. | `wp04-T049-T059-T060-test_the_contract_carries_its_eight_sections_in_order.txt` |
| T060 | **closed** — cite-not-copy: `## Goal` cites `goal_slug`, `## Targets` cites `T-NNN`, `## Task Reference` uses id ranges, and a `- [ ] T` line is labelled the refused defect `task-copy-in-handoff`. | `wp04-T049-T059-T060-test_the_contract_cites_and_never_copies_task_rows.txt` |
| T061 | **partial — artifact closed, guard authored red, engine half unowned** — the `create-team` SKILL.md now carries the handoff discipline (creation timing, `handoff-dangling-key` refusal through the engine, reverse `handoff_ref` written by the engine's binding action, territory expansion, writeback). The guard `test_a_dangling_handoff_key_is_refused_at_creation` drives the engine action `handoff-ref --handoff <path>`; `goal-utils.py` is outside this package's write domain, so the guard is red until that action lands. | `wp04-T061-red-engine-unowned.txt`; § Residual risks |
| T062 | **closed** — `improve-team/SKILL.md` gains `## Handoff Territory Expansion`: one record per team, `## Territory` → `territory.write`, the four spec artifacts forced into `territory.forbidden`, granted entries inside the spec dir and out of the two archive layers, writeback one record per task. | `wp04-T050-T062-test_the_territory_expansion_is_recorded_and_forbids_the_four_spec_artifacts.txt` |

**Rows closed by this fork: 5 of 8 package rows** (T059, T060, T062 fully; T061 artifact-half)
**plus 2 delegated guards** (T049, T050) = **7 guards green**; T055/T057/T058 are blocked by
the dispatch's domain boundary, not by missing behaviour (T056 is already closed by wp03).

## Test readings

TEST ENTRY: every run below went through `bash scripts/bash/run-tests.sh <paths> -q`
(pytest-xdist defaults `-n auto --dist load`); no raw pytest invocation was used.

- **Red-first (before any artifact)** — 6 failed, exit 1: every guard failed on the missing
  template / missing territory check / missing improve-team section / missing engine action.
  `test-evidence/wp04-red-handoff-modules.txt`.
- **Package modules after the artifacts** — **5 passed, 1 failed**, exit 1:
  `wp04-T049T050T059T060T062-green-T061-red.txt`. The single failure is T061's guard, red by
  design (`error: unrecognized option: --handoff` — the engine action is unowned).
- **Per-row green readings** — 5 runs, 1 passed each, exit 0
  (`wp04-T049-T059-T060-*.txt`, `wp04-T050-T062-*.txt`).
- **T061 red reading** — `wp04-T061-red-engine-unowned.txt` (exit 1).
- **Package neighbourhood** — `test_handoff_contract.py`, `test_handoff_territory.py`,
  `test_declaration_facts.py`, `test_command_family.py`, `test_parallel_lines.py`,
  `test_team_territory.py`, `test_territory_containment.py`, `test_overlap_verdicts.py`:
  **42 passed, 1 failed** (T061), exit 1 — `wp04-package-neighbourhood.txt`.
- **Skill-adjacent collateral** (flat-internal migration, no-nested-skills, skill-reference
  command surface + failures, harness triple structure, feedback conformance, mechanism
  policy wiring, team command routing, nested SDD invocation): **167 passed, 1 failed** —
  the failure is `test_nested_sdd_invocation.py::test_nested_run_reaches_review_zero_merge_zero_push`,
  pre-existing and structural: `sdd-route.py` still asks the engine for `--scope global`,
  which wp01's C-9 closed set no longer accepts; T047 (wp05) is the row that fixes it.
- **Criterion-vocabulary / expression-compatibility / compile-embeds failures** — all
  pre-existing and NOT in the plan baseline's failing-id list: `test_criterion_vocabulary_scan.py`
  (T064/T069, wp05-owned) plus the 069a frozen-hash module (71 of 74 manifest entries already
  drifted repo-wide at base; its 085 disposal row is `historical`) and the compile-embeds
  sandbox failures. Measured against a `git archive 51f3b8289` copy: the same node ids fail
  there, and this fork adds none of them (the base copy fails one extra because it lacks `.git`).
- **Script interface** — `territory-check.py --help` 0, `--version` 0 (`territory-check.py 0.0.22`),
  `--bogus` 2, `--bogus --help` 2 (an undeclared option is never rescued), no-args 2.

## Artifacts delivered

- `skills/internal/create-team/references/handoff-contract-template.md` — the `handoff/v1`
  shape (single ```markdown block: frontmatter + the eight sections), production/consumption
  timing, the state machine, the cite-never-copy rules, and the territory expansion pointer
  (N-3's ruled home).
- `skills/internal/create-team/scripts/territory-check.py` — the territory refusal surface
  pinned by `quickstart.md` S-7. Scope grammar imported from `build-summary-input.py`
  (`expand_scopes` / `scopes_overlap`) — zero second grammar. `--team --path [--seat]
  [--repo-root] [--json]`; forbidden wins over write; undeclared territory refuses; exit
  0 allowed / 1 refused / 2 input error; script-interface guard block included.
- `skills/internal/create-team/SKILL.md` — new `## Handoff Contract (designer → construction
  crew, 094)` section (T061 evidence: creation timing, dangling-key refusal through the
  engine, reverse `handoff_ref` via the binding action, territory expansion via improve-team,
  writeback discipline); resource rows for the template and the script.
- `skills/internal/improve-team/SKILL.md` — new `## Handoff Territory Expansion` section
  (T062): one record per team, expansion into `territory.write`, the four artifacts into
  `territory.forbidden` with the mechanical `territory-check.py` refusal, writeback per task,
  design-face ownership retained by the spec side.
- `tests/contract/test_handoff_contract.py` — T049/T059/T060/T061 guards; the fixture
  handoff instance is instantiated from the authored template; the T061 guard pins the
  engine entry `handoff-ref --handoff <path>` (see Residual risks item 2).
- `tests/contract/test_handoff_territory.py` — T050/T062 guards; fixture crew under
  `.specify/.tmp/s094/`, refusal measured by exit code and text (path + seat).

## Commits

Committed explicitly by path (never `git add -A`); no push.

- `feat(094-wp04): handoff contract template, territory check and skill discipline (T049, T050, T059–T062)`
  — `skills/internal/create-team/SKILL.md`, `skills/internal/create-team/references/handoff-contract-template.md`,
  `skills/internal/create-team/scripts/territory-check.py`, `skills/internal/improve-team/SKILL.md`,
  `tests/contract/test_handoff_contract.py`, `tests/contract/test_handoff_territory.py`.
- `docs(094-wp04): record the wp04 readings — 5 rows closed, T055/T057/T058 blocked by domain`
  — `notes/implement-wp04.md` and the `test-evidence/wp04-*` files.

## Residual risks and disclosed boundaries

1. **Row/domain mismatch for T055, T057, T058 (the package's declared ANOMALY).** The rows
   sit in wp04's row list but write `tests/contract/test_declaration_facts.py`,
   `shared/declarations/contract.yaml` and `scripts/python/goal-utils.py` — none of which is
   in this package's § Package Map write domain, and the dispatch pinned the four-surface
   domain explicitly. The Mutable-state map's cell `wp04/wp03 (T051, T053–T058)` says these
   guards belong partly to wp04's pen, so the tasks file contradicts itself. Following the
   dispatch (and wp03's precedent for delegated guard modules), the engine/registration facts
   are verified read-only here (`wp04-T057-engine-grammar-refusal.txt`) but the three guard
   functions are not authored. The driver must assign them or re-scope the rows; the
   declaration module currently holds no function for any of the three names.
2. **T061's engine half is unowned.** `handoff-ref` (validate `goal_slug`/`team_slug`;
   refuse `handoff-dangling-key`, exit 2; insert `handoff_ref` into both definitions with
   every other byte identical) does not exist in `goal-utils.py`, and that file is outside
   this package's write domain. The guard is authored red-first and pins the entry name
   `handoff-ref --handoff <path>` — no contract clause fixes the entry's name, so a later
   implementer may rename it by changing the one test in the same edit (the same disclosure
   wp03 made for its pinned JSON shapes). A separate action is required by C-6: a `bind`
   call that also wrote `handoff_ref` would change a non-binding byte.
3. **Mirror projection is pending the driver's integration step.** `sync-mirrors.py --check`
   reports `MISS` for the new template and script, `DIFF` for the two edited SKILL.md files,
   and the pre-existing `DIFF .specify/scripts/python/goal-utils.py` (wp01 drift).
   `regen-command-copies.py --check` exits 0 (no command template touched).
   `test-evidence/wp04-mirror-check.txt`, `wp04-copy-check.txt`. Per wp01/wp02/wp03 precedent
   the projection is the driver's (`sync-mirrors.py --write`), never hand-edited from a fork.
4. **`create-mode.md` still carries the legacy vocabulary** in wp04's directory (5 hits:
   `scope: global | spec`, spec-scoped temporary teams). No row declares its rewrite; wp03
   flagged this in its note, and T064 (wp05) stays red on it until someone owns the edit.
   Recorded rather than absorbed: rewriting it is not a row of this package.
5. **T052's red-first recording** (T049–T051 into the shared `notes/red-first-evidence.md`)
   is a wp03-row duty that was never discharged. This fork records its own red readings under
   `test-evidence/wp04-*` and leaves the shared file untouched (cross-package file, matching
   wp03's decision).
6. **The T049 fixture is instantiated from the authored template**, so the test proves the
   *shape* resolves, not that a producer exists. Production by the `tasks` stage is declared
   in the template and the create-team SKILL.md, and no command-template row for
   `templates/commands/tasks.md` exists in the package map — a gap the driver should note
   (C-68 has no owned surface yet).
7. **The threshold literal stays a one-file edit**: no artifact this package authored pins
   the number (the template cites no threshold; the territory check has no threshold input).
8. **Fast-fail accounting**: no anomaly was patched over quietly; the two domain gaps above
   were surfaced, not worked around. The `territory-check.py` glob matching reuses the shared
   conservative prefix grammar — it errs toward refusing (forbidden) and, on the allow side,
   toward prefix containment, which is the grammar's documented direction and not a new rule.
