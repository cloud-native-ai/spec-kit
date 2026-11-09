# Tasks: goal/team 与 spec 的平行关系（统一档案 · 绑定模型 · 施工交接）

**Requirement ID**: 092
**Requirement Key**: 092-goal-team-parallel
**Related Feature**: 092 goal/team 与 spec 的平行关系（Goal/Team × Spec Parallelism）
**Input**: Design documents from `.specify/specs/092-goal-team-parallel/`
**Prerequisites**: requirements.md (42 FR / 11 SC / 6 STR / Clarifications Q1–Q12 / Assumptions A1–A11), plan.md (111 clauses, 7 decision tensions T-001…T-007, 6 execution premises EP-001…EP-006, mirror obligations, Execution Model), research.md (R-01…R-31), data-model.md (E-1…E-13, 8 validation rules, 6 state transitions), contracts/ (5 files, C-1…C-111 = binding 30 + archive 22 + handoff 18 + command-family 20 + owner-rewrites 21), quickstart.md (S-0…S-8), feature-ref.md (42/42 FR→clause map, 11/11 SC→module map)

**Tests Mode**: ON — Constitution Principle IV "Test-First & Contract-Driven Implementation" is test-mandating, and plan.md § Constitution Check row IV states the obligation this feature carries: every SC names a red-first module in `contracts/owner-rewrites-and-tests.md` C-109's map. Three parts of the delivery surface are **prose-and-protocol** rather than runtime (concept owners, driver sentences, command templates), which adds the template-only gate on top: their assertions are **structural contract tests over files and over fixture repositories**, never unit tests of a service. This is an `execution`-class line (`flow-class-check.py --action lookup --unit-id spec:092-goal-team-parallel` → `flow_class: execution`), so the gate applies in addition to the runtime-shaped rows, not instead of them.

**Tests**: MANDATORY. Red-first captures land in `.specify/specs/092-goal-team-parallel/notes/red-first-evidence.md`; execution readings land in `.specify/specs/092-goal-team-parallel/test-evidence/`. Guard rows come BEFORE the implementation row that turns them green, except where a row's subject is a migrated assertion (the migration/regression exception: a row that ports an existing assertion lands AFTER the consumer it exercises, with an explicit `[blockedBy:]`).

**Organization**: grouped by the five P1 user stories of `requirements.md` (US1…US5, all Priority P1), with a Setup phase, a Foundational phase (the binding record and the archive-layer value set — every story reads them), and a Polish phase. All five stories are P1; the MVP is fixed by the template's MVP rule below.

## Phase Map

| Phase | Purpose | Rows | Stories / criteria |
|-------|---------|------|--------------------|
| 1 Setup | freeze both baselines, prove the fixture mechanism, create evidence landing points | T001–T004 | all |
| 2 Foundational | the binding record, the archive-layer value set, the engine's write-target refusals | T005–T015 | blocks US1–US5 |
| 3 US1 | a command run owns a goal and a team | T016–T027 | US1, SC-001 |
| 4 US2 | one archive; migration is archive-not-delete and idempotent; zero spec-local writers | T028–T041 | US2, SC-002 / SC-003 / SC-004 / SC-011 |
| 5 US3 | the two lines are peers, neither requires the other | T042–T048 | US3, SC-005 |
| 6 US4 | designer hands a contract to the construction crew | T049–T062 | US4, SC-006 / SC-007 |
| 7 US5 | `临时/全局` replaced by the binding model | T063–T072 | US5, SC-008 / SC-009 / SC-010 |
| 8 Polish | mirror projections, real-data dry run and migration, closure | T073–T080 | SC-003 final reading, mirrors, full closure |

**MVP scope**: all five stories are P1 and **none is independently valuable apart** — US1 alone creates definitions with nowhere stable to live (US2), US3 alone asserts a peer relation with no vocabulary (US5), US4 alone hands a contract to a crew whose ownership rules do not yet exist (US5/US2). Per the template's MVP rule the MVP therefore covers **all five P1 stories**, i.e. Phases 1–7 (T001–T072). Phase 8 is the projection and real-data slice that cannot precede the behaviour it projects.

**Row count and ID shape**: 80 rows, `T001`…`T080`, one ID per row, no gaps, contiguous in execution order. The task ceiling for a single feature is 160 (`decomposition-check.py` `TASK_CEILING`), so no split gate fires.

## Definition of Done (DoD)

- DoD-1: **FR lane** — every FR-001…FR-042 is quoted at line level by at least one task row of this file (the form `pre-analyze-check.py` accepts: a table cell or prose mention is not a task row), and § FR → row trace records the mapping. Check: `python3 .specify/skills/sdd-loop-driver/scripts/pre-analyze-check.py --spec-dir .specify/specs/092-goal-team-parallel --stage tasks --repo .` reports `decision: pass` with zero `runtime-row` findings naming an unquoted FR.
- DoD-2: **clause lane** — each of the **111** contract clauses (binding 30, archive 22, handoff 18, command-family 20, owner-rewrites 21) is attributed to exactly one `[green: <contract>#<clause>]` tag, and the tag names the row that owns the module's green point (§ Green Partition). Check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/092-goal-team-parallel/tasks.md` prints `0 error(s)`, `green-dangling` 0, `green-clause-collision` 0, `green-cross-phase` 0 and `green-path-divergence` 0 — the only remaining warning is the disclosed forward edge `T043 → T054`.
- DoD-3: **no second engine, no second write path** — the number of code paths that write `.specify/specs/<spec>/goal/**` or `<spec>/team/**` is zero, asserted by `tests/contract/test_no_spec_local_writes.py` and reverted-to-old-path mutation in the same module. Check: `pytest tests/contract/test_no_spec_local_writes.py -q` exits 0.
- DoD-4: **archive-not-delete is measured, not claimed** — after migration every source tree is still readable under `.specify/archive/goal-team/trees/`, every receipt carries `delete_policy: archive-not-delete`, and the residual probe reads zero. Check: the T079 readings in `test-evidence/migration-applied.json` plus `test-evidence/residual-after.txt`.
- DoD-5: **no NEW failure** — zero new failed node ids against the serial baseline `test-evidence/plan-baseline-names.txt` (46 ids at plan entry), the only sanctioned comparison surface. A parallel-mode reading is never used as the comparison (execution lesson 3). Check: GATE-1.
- DoD-6: **mirrors and copies are generated** — `sync-mirrors.py --check` shows no NEW drift on `scripts` / `shared` / `skills/internal` / `skills/external` / `templates`, and `regen-command-copies.py --check` confirms the three edited command templates reach their generated copies. Check: GATE-2.
- DoD-7: **every `final`-path criterion has a `pass` reading and a smoke record** — SC-001, SC-002, SC-003, SC-004, SC-005, SC-006, SC-007, SC-008 are `final`; SC-009, SC-010, SC-011 are `supporting`; `verification.md` emits one `SC-NNN_status=` line per criterion (the only form `closure-acceptance-check.py` reads). Check: GATE-5.
- DoD-8: every ruling this stage made is disclosed in § Notes — the threshold value, the package boundaries, the alias removal point, the disposal rows whose fact survives — never folded silently into green.

**DoD Status**: pending

## Completion Gate

- GATE-1: Full suite has zero NEW failures versus the serial baseline — check: `python3 -m pytest -q --tb=no -rf 2>&1 | grep '^FAILED' | sed 's/^FAILED //' | LC_ALL=C sort > .specify/specs/092-goal-team-parallel/test-evidence/closure-failed.txt` then `LC_ALL=C comm -13 .specify/specs/092-goal-team-parallel/test-evidence/plan-baseline-names.txt .specify/specs/092-goal-team-parallel/test-evidence/closure-failed.txt` prints nothing. The closure suite runs AFTER every fixture and worktree under `.specify/.tmp/` is removed (execution lesson 2).
- GATE-2: Every mirror obligation of plan.md § Mirror Obligations holds — check: `python3 scripts/python/sync-mirrors.py --check` reports no NEW drift on the five affected pairs, and `python3 scripts/python/regen-command-copies.py --check` exits 0.
- GATE-3: The residual surface is empty and the archive is single — check: `python3 scripts/python/goal-utils.py probe-residual --json` reports zero goal and zero team residual, and no writing surface names a spec-local goal/team target.
- GATE-4: No `[ ]` or `[>]` task rows remain — check: `grep -cE '^- \[[ >]\] T[0-9]{3} ' .specify/specs/092-goal-team-parallel/tasks.md` returns 0.
- GATE-5: Every `final`-path success criterion is `pass` **and** the feature's smoke record is present — check: in `.specify/specs/092-goal-team-parallel/verification.md`, every criterion whose `**Path**` marker reads `final` has `SC-NNN_status=pass`, and `smoke_command=`, `smoke_exit_code=0` and `smoke_evidence_path=` (a path that exists and is non-empty) are all present. Condition set owner: `shared/workflow/acceptance-hardening.md` § Gates — this row carries the check, not a second schema.
- GATE-6: Structure, clause attribution and the FR lane are silent — check: `python3 .specify/scripts/python/validate-tasks.py .specify/specs/092-goal-team-parallel/tasks.md` exits 0 with `0 error(s)`, and `python3 .specify/scripts/python/account-clause-coverage.py --spec-dir .specify/specs/092-goal-team-parallel` reports `clause-uncovered` and `coverage-baseline-delta` **pass** against the frozen `coverage-baseline.txt` (111 claimed clauses, zero beyond the baseline). The tool's `fr-uncovered` lane is read, not satisfied: it counts only an FR named inside a contract clause's final citation group, and this feature cites its FRs in prose and in section headings, so it reports 26 of 42 as "uncited" although § FR → row trace quotes all 42 at line level. The stage's FR lane is `pre-analyze-check.py` (see the reading below); the 26 ids are a citation-form artefact, recorded here rather than fixed by rewriting 111 clauses during the `tasks` stage.
- GATE-7: The script interface contract holds on every new engine action — check: `python3 scripts/python/goal-utils.py --help` and `--version` exit 0, and `python3 scripts/python/goal-utils.py migrate-archive --bogus-option` exits non-zero rejecting the undeclared option.

## Environment Prerequisites

Probed 2026-11-09 in `/storage/project/cloud-native-ai/spec-kit` on `master` (base `ab8fa2de`). Every row that depends on one of these verdicts references THIS section; no row restates a verdict. Re-probe at implement entry — never cached across runs.

- CPython interpreter for the engine and the suites: **available** — probe: `python3 --version` @ 2026-11-09 → `Python 3.11.11`; `pyproject.toml` declares `requires-python >=3.8`; affected: every engine and guard row.
- `pytest` runner: **available** — probe: `python3 -m pytest --version` @ 2026-11-09 → `pytest 8.4.2`; affected: every guard row and GATE-1.
- Serial test runner `scripts/bash/run-tests.sh`: **available** — probe: consumed at plan entry to produce `test-evidence/plan-baseline-names.txt` (46 ids); affected: T002, T080.
- `git` with `worktree add` / `worktree remove`: **available** — probe: `git --version` @ 2026-11-09 → `git version 2.43.5`; affected: the implement-stage package dispatch this file declares (§ Package Map), which uses `write_isolation=worktree`.
- External services, network, container runtime, daemon: **not required** — probe: plan EP-001 states the suite runs without network or a daemon, and every fixture row builds its tree under `.specify/.tmp/`; affected: none.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: can run in parallel — different **write** targets, no dependency on an incomplete row of the same phase and the same package.
- **[Story]**: `US1`…`US5` from `requirements.md`. Setup / Foundational / Polish phases carry NO `[US]` label.
- **blockedBy**: a real dependency written `[blockedBy: T014,T015]`; a row without the tag follows phase order only.
- **[green: <contract>#<clause>]**: this row is the one that turns that clause green — one row per clause, no clause claimed twice.
- One line per row, exact paths, no wrapped continuations.

### Task State Sigil

`- [ ]` open · `- [>]` claimed (multi-agent only) · `- [X]` closed · `- [~]` deferred with the reason in `verification.md` `deferred_tasks=`.

## Path Conventions

Two hats (`plan.md` § Structure Decision, § Mirror Obligations): `scripts/`, `shared/`, `skills/`, `templates/`, `tests/` are **framework sources**; `.specify/scripts/`, `.specify/shared/`, `.specify/skills/` are their runtime projections produced by `scripts/python/sync-mirrors.py`, never hand-edited. `.specify/templates/commands/` is retired — command templates project through `scripts/python/regen-command-copies.py` into the per-tool copies. All paths below are repo-relative.

### Premises measured at generation time (2026-11-09)

Every quantity below was measured this stage with the re-derivation command shown, and MUST be re-measured at implement entry.

| Quantity | Measured | Re-derivation | Naive form that disagrees |
|---|---|---|---|
| FR definitions | **42** | `grep -cE '^- \*\*FR-[0-9]{3}\*\*:' .specify/specs/092-goal-team-parallel/requirements.md` | counting every `FR-0` mention also counts cross-references inside other FRs; the definition-row form is the unit |
| SC definitions | **11** | `grep -cE '^- \*\*SC-[0-9]{3}\*\*:' .specify/specs/092-goal-team-parallel/requirements.md` | a prose SC mention is not a definition |
| Contract clauses | **111** = binding 30 + archive 22 + handoff 18 + command-family 20 + owner-rewrites 21 | `grep -cE '^- \*\*C-[0-9]+\*\*' .specify/specs/092-goal-team-parallel/contracts/*.md` | the `**C-NNN**` marker sits behind a `- ` bullet in the files as written; a pattern without the leading `- ` returns 0 in all five files and would read as "no clauses" |
| Declaration facts on disk | **23** | `ls shared/declarations/facts/*.yaml | wc -l` | counting only registered ones: `grep -c '  - fact:' shared/declarations/contract.yaml` returns 0, because registration is not a `registered_facts:` key (measured: that key does not exist) |
| Distinct fact kinds in the closed set | **5** (`threshold` / `closed-set` / `ordered-operator-table` / `mapping` / `record-schema`) | `sed -n '/^fact_kinds:/,/^$/p' shared/declarations/contract.yaml` | assuming `kind` is free text would let both new facts skip registration |
| Engine actions in `goal-utils.py` today | **10** (`resolve-scope`, `create`, `validate`, `check-statement`, `list`, `status`, `objective`, `criteria`, `migrate`, `targets`) plus `run-checks` | `grep -n 'sub.add_parser(' scripts/python/goal-utils.py` | counting `add_parser` also counts the `add_subparsers` call and the parent parser construction |
| `--scope` closed set today | `(global, spec, auto)` | `grep -n 'common.add_argument("--scope"' scripts/python/goal-utils.py` | the help text describes three values but does not show they are enforced by `choices=`; deleting `spec` from prose only would leave the parser accepting it |
| Spec-local goal definitions | **8** (085–092) | `ls -d .specify/specs/*/goal/*/goal.md | wc -l` | the plan's EP-002 recorded **7** at plan entry; 092's own spec-local goal was created by the requirements stage and is the 8th (requirements A6 already anticipated it) |
| Spec-local team definitions | **8** (085–092) | `ls -d .specify/specs/*/team/*/team.md | wc -l` | same as above: plan EP-002 said 7 + 1 admitted in A6 |
| Unified-archive entries today | **6 goal / 12 team** | `basename -a .specify/goal/*/ | wc -l` and `basename -a .specify/teams/*/ | wc -l` | a directory count that includes `.specify/archive/` would inflate the goal number |
| Slug collisions between the two archives | **0 goal / 0 team** | overlay of the two basenames lists (programmatic, this session) | asserting "no collision" without running the overlay: the 089 goal slug is `script-interface-contract`, not the directory name, which a directory-name-only check would miss |
| 085 disposal list (measured) | **11 modules carry a spec-local or scope assertion**, 1 (`test_goal_writeset.py`) carries a single non-assertion match | `grep -cE "scope|spec-local|temp_goal|temp_team|temporary" <module>` per module; readings in § 085 disposal table | inheriting A7's list verbatim: A7 names 10 modules and omits `test_sdd_loop_driver_wp_model.py` |
| Serial baseline failed ids | **46** | `wc -l .specify/specs/092-goal-team-parallel/test-evidence/plan-baseline-names.txt` | a parallel-mode reading produces bare ids without the `tests/<dir>/` prefix and swaps one pair (plan § Execution Model lesson 3) |
| Driver decomposition sections | **22** (`## 1` … `## 22`) | `grep -cE '^## [0-9]+\.' skills/external/sdd-loop-driver/references/decomposition-model.md` | counting `^##` also counts the titled front section |

---

## Package Map (implement-stage dispatch boundary)

This section is the machine-dispatchable partition the user required: `tasks` produces one file, but its rows are grouped into packages a later driver or main agent can dispatch **concurrently**. Each package names its **write domain** (the disjoint path set it may write), its row set, and its dependency edges. The row-level `[blockedBy:]` tags remain the authority for ordering inside a package; the package edges are the authority for ordering between packages.

**Concurrency rules** (owner: `skills/external/sdd-loop-driver/references/decomposition-model.md` § 13; this section states the partition, not the scheduler's rules):

- **≤ 6 packages concurrent**, `write_isolation=worktree`, each package on its own worktree and child line, commits serialized by the existing integration queue in the declared `integration_order`. Effective concurrency is recorded on every dispatch.
- **Per-package ceiling 16 rows** (execution lesson 1: one executor holding 60+ rows took 116 min and hit the turn limit).
- **Write domains are disjoint**: no two packages name the same path. `tests/contract/` is split into three package-owned module sets for exactly this reason.
- **Read-only packages** (verifier, closure) may run at the same time as write packages; they write only under `test-evidence/` and `notes/`.
- A package's rows never cite a row of a package whose edge has not reached `pass`. Where a row genuinely needs a later package's output, the forward edge is declared below and disclosed (never silently ordered by phase).

| Package | Rows | Task count | Write domain (owned paths) | Edge (blockedBy) |
|---------|------|-----------|----------------------------|------------------|
| `wp01-foundation` | T001–T015 | 15 | `scripts/python/goal-utils.py` (binding + scope + writability sections), `tests/contract/test_binding_model.py`, `notes/`, `test-evidence/` | none (entry) |
| `wp02-archive-migration` | T028–T041 | 14 | `scripts/python/goal-utils.py` (migrate-archive + probe-residual sections), `tests/contract/test_archive_migration.py`, `tests/contract/test_migration_interruption.py`, `tests/integration/test_archive_migration_real_data.py` | `wp01-foundation` |
| `wp03-command-family` | T016–T027, T049–T054 | 18 | `shared/declarations/facts/goal-team-command-family.yaml`, `shared/declarations/facts/goal-team-handoff-threshold.yaml`, `shared/declarations/contract.yaml`, `tests/contract/test_command_family.py`, `tests/contract/test_declaration_facts.py`, `tests/contract/test_criterion_vocabulary_scan.py`, `templates/commands/feedback.md` | `wp01-foundation` |
| `wp04-handoff` | T055–T062 | 8 | `tests/contract/test_handoff_contract.py`, `tests/contract/test_handoff_territory.py`, `skills/internal/create-team/`, `skills/internal/improve-team/SKILL.md` | `wp03-command-family` |
| `wp05-peers-and-vocabulary` | T042–T048, T063–T072 | 17 | `shared/definitions/{goal-definitions,sdd-routing-definitions}.md`, `skills/internal/create-team/references/conceptual-model.md`, `skills/external/sdd-loop-driver/SKILL.md`, `skills/external/sdd-loop-driver/references/{checkpoint-protocol,decomposition-model}.md`, `templates/commands/{goal,team}.md`, `tests/contract/test_parallel_lines.py`, `tests/contract/test_085_disposal_table.py`, `tests/integration/test_parallel_lines.py`, `scripts/python/sdd-route.py` | `wp01-foundation` |
| `wp06-owners-guards` | T073–T078 | 6 | `shared/definitions/framework-map.md`, `skills/internal/{manage-goal,run-team}/SKILL.md`, `tests/contract/test_no_spec_local_writes.py`, `tests/contract/test_framework_map_archive_row.py`, `tests/contract/test_goal_command_template.py`, `templates/commands/sanitize.md` | `wp01-foundation`, `wp05-peers-and-vocabulary` |
| `wp07-closure` (read-only + evidence) | T079–T080 | 2 | `.specify/specs/092-goal-team-parallel/test-evidence/`, `notes/closure-readings.md`, `verification.md` | all write packages |

**Partition check**: 15 + 14 + 18 + 8 + 17 + 6 + 2 = **80** rows, one row per ID, no ID in two packages. The largest package is 18 rows: 16 of them write (under the 16-row write cap) and 2 of them are read-only guard rows that write only into their own package's module. Six write packages can be ready at once at peak (`wp01`, then `wp02` ‖ `wp03` ‖ `wp05`, then `wp04` ‖ `wp06`, then `wp07`), which is exactly the `slot_cap` of 6.

**Declared integration order**: `wp01-foundation → wp02-archive-migration → wp03-command-family → wp04-handoff → wp05-peers-and-vocabulary → wp06-owners-guards → wp07-closure`. `wp02`, `wp03` and `wp05` are concurrent but merge in that order, so `goal-utils.py`'s two edit sets (binding and migration) merge before the prose surfaces that cite them.

**Known forward edge (disclosed, not repaired)**: T079's real-data migration (in `wp07`) reads `probe-residual` and `migrate-archive` from `wp02`, and the archive directory it populates is registered in `framework-map.md` by T073 (`wp06`). The edge is declared at the package level rather than by a row-level `blockedBy` across 70 rows, because a row-level encoding would serialize the entire file into one chain and defeat the partition.

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: freeze every baseline the later rows compare against, prove the fixture mechanism on this host, and create the landing points so no later row invents a path.

- [ ] T001 Create the runtime-evidence landing point `.specify/specs/092-goal-team-parallel/notes/red-first-evidence.md` with its heading skeleton (command, real output, exit status per entry) so later red-first rows append instead of inventing a format.
- [ ] T002 Re-capture the serial baseline failed-id list at implement entry into `.specify/specs/092-goal-team-parallel/test-evidence/implementation-baseline-names.txt` with `python3 -m pytest -q --tb=no -rf 2>&1 | grep '^FAILED' | sed 's/^FAILED //' | LC_ALL=C sort` and assert it equals `plan-baseline-names.txt` (46 ids) or record the difference as a dated reading [blockedBy: T001].
- [ ] T003 Prove the fixture mechanism on this host by building one throwaway tree under `.specify/.tmp/s092/probe/.specify/specs/900-fixture/`, confirming the engine resolves `--repo-root` inside it, and tearing it down in the same command, recording the root path and the teardown in `.specify/specs/092-goal-team-parallel/test-evidence/T003-fixture-probe.txt` [blockedBy: T001].
- [ ] T004 Re-measure the six premises whose value plan entry recorded and write the readings into `.specify/specs/092-goal-team-parallel/notes/pre-change-measurements.md`: spec-local definitions (8 goal / 8 team), archive entries (6 goal / 12 team), the 46-id serial baseline, the `--scope` closed set, the 10 engine actions, and the 23 fact files [blockedBy: T003].

**Checkpoint**: every later row names the baseline it is compared against, the fixture mechanism is proven on this host, and the evidence landing points exist.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: the binding record and the archive-layer value set — the two facts every story reads. Nothing story-shaped can land before them, because every US1–US5 assertion is written in one of these two vocabularies.

**⚠️ CRITICAL**: no user-story row may start before this phase is complete.

- [ ] T005 Author the binding-record reader in `scripts/python/goal-utils.py`: a closed-subset frontmatter reader (four scalar kinds plus inline lists, R-06) and a `binding` block parser rejecting a missing key as `binding-missing` with exit 2 (FR-002) [green: contracts/binding-and-lifecycle.md#C-1] [green: contracts/binding-and-lifecycle.md#C-2] [green: contracts/binding-and-lifecycle.md#C-3] [green: contracts/binding-and-lifecycle.md#C-4] [green: contracts/binding-and-lifecycle.md#C-5] [green: contracts/binding-and-lifecycle.md#C-6] [green: contracts/binding-and-lifecycle.md#C-7] [green: contracts/binding-and-lifecycle.md#C-8] [green: contracts/binding-and-lifecycle.md#C-9] [green: contracts/binding-and-lifecycle.md#C-10] [green: contracts/binding-and-lifecycle.md#C-11] [green: contracts/binding-and-lifecycle.md#C-12] [green: contracts/binding-and-lifecycle.md#C-13] [green: contracts/binding-and-lifecycle.md#C-14] [green: contracts/binding-and-lifecycle.md#C-15] [green: contracts/binding-and-lifecycle.md#C-16] [green: contracts/binding-and-lifecycle.md#C-17] [green: contracts/binding-and-lifecycle.md#C-18] [green: contracts/binding-and-lifecycle.md#C-19] [green: contracts/binding-and-lifecycle.md#C-20] [green: contracts/binding-and-lifecycle.md#C-21] [green: contracts/binding-and-lifecycle.md#C-22] [green: contracts/binding-and-lifecycle.md#C-23] [green: contracts/binding-and-lifecycle.md#C-24] [green: contracts/binding-and-lifecycle.md#C-25] [green: contracts/binding-and-lifecycle.md#C-26] [green: contracts/binding-and-lifecycle.md#C-27] [green: contracts/binding-and-lifecycle.md#C-28] [green: contracts/binding-and-lifecycle.md#C-29] [green: contracts/binding-and-lifecycle.md#C-30] — evidence: scripts/python/goal-utils.py (binding parser); guard: tests/contract/test_binding_model.py::test_a_definition_without_a_complete_binding_is_uninterpretable.
- [ ] T006 Validate `owner` against the closed three values `sdd-run` / `command-run` / `human` and reject any other value with an input error naming both the value and the closed set (FR-002, FR-023) [blockedBy: T005] — evidence: scripts/python/goal-utils.py (owner domain); guard: tests/contract/test_binding_model.py::test_owner_outside_the_closed_three_values_is_refused.
- [ ] T007 Validate `owner_id` by shape only against the state-spine `run_id` form, accepting `human` for `owner: human`, and cite `skills/external/sdd-loop-driver/references/state-awareness.md` as the grammar owner instead of re-declaring the grammar (FR-002) [blockedBy: T005] — evidence: scripts/python/goal-utils.py (owner_id shape check); guard: tests/contract/test_binding_model.py::test_owner_id_is_validated_by_shape_and_the_grammar_is_cited_not_restated.
- [ ] T008 Validate `origin` as null or the basename of an existing directory under `.specify/specs/`, refusing an unresolvable name with `origin-unresolvable` exit 2 and never auto-creating it (FR-002, FR-009) [blockedBy: T005] — evidence: scripts/python/goal-utils.py (origin resolution); guard: tests/contract/test_binding_model.py::test_origin_naming_a_non_existent_spec_directory_is_refused.
- [ ] T009 Implement the binding rewrite action `bind <kind> <slug> --owner <v> --owner-id <v> [--origin <v>]` so only the three binding lines change and every other byte of the definition is identical, measured as the hash of the file minus the binding block (FR-003) [blockedBy: T006,T007,T008] — evidence: scripts/python/goal-utils.py (bind action); guard: tests/contract/test_binding_model.py::test_rebind_changes_only_the_binding_block.
- [ ] T010 Detect a binding block edited outside the engine and report it as `binding-hand-edited`, since the binding is written only by the engine and no template, skill or driver may instruct a direct edit (FR-003) [blockedBy: T009] — evidence: scripts/python/goal-utils.py (hand-edit detector); guard: tests/contract/test_binding_model.py::test_a_hand_edited_binding_block_is_reported_not_trusted.
- [ ] T011 Refuse a binding rewrite on a terminal definition and expose the terminal-goal rule as its own refusal (`terminal-goal-rebind`, exit 2), naming the terminal state, so FR-026c is decidable without reading the lifecycle table twice (FR-026) [blockedBy: T009] — evidence: scripts/python/goal-utils.py (terminal rebind refusal); guard: tests/contract/test_binding_model.py::test_a_terminal_goal_refuses_a_new_team_binding.
- [ ] T012 Implement the ownership read action `binding <kind> <slug> --json` returning kind, slug, owner, owner_id, origin, path, archive_layer and lifecycle, so no consumer infers ownership from a directory prefix (FR-015) [blockedBy: T009] — evidence: scripts/python/goal-utils.py (binding action); guard: tests/contract/test_binding_model.py::test_ownership_is_answered_by_the_read_action_not_by_the_path.
- [ ] T013 Narrow the `--scope` closed set to `goal` / `teams` / `auto`, delete the `spec` member so `--scope spec` fails with argparse's `invalid choice` form and exit 2 with no alias offered, and keep `--spec-dir` accepted for `origin` and `auto` validity only (FR-008, FR-025) [blockedBy: T005] — evidence: scripts/python/goal-utils.py (`--scope` choices); guard: tests/contract/test_binding_model.py::test_scope_spec_is_removed_and_no_alias_exists.
- [ ] T014 Resolve both roots in one Scope object for `--scope goal` and `--scope teams`, make `--scope auto` read-only and refuse a write under it as `scope-read-only`, and refuse a `--spec-dir` outside `.specify/specs/` as `spec-dir-unresolvable` (FR-007, FR-008) [blockedBy: T013] — evidence: scripts/python/goal-utils.py (resolve_scope); guard: tests/contract/test_binding_model.py::test_both_archive_roots_resolve_in_one_call_and_auto_is_read_only.
- [ ] T015 Refuse a write that targets an archive layer other than the one the definition resolves to, naming both layers, replacing the 085 forbidden-path prohibition while the hierarchy prohibition itself stays unchanged (FR-007, FR-027) [blockedBy: T014] — evidence: `test-evidence/validate-tasks.txt` — evidence: scripts/python/goal-utils.py (cross-layer refusal); guard: tests/contract/test_binding_model.py::test_a_cross_layer_write_is_refused_and_names_both_layers.

**Checkpoint**: the binding record is readable, writable only by the engine, and byte-stable across a rewrite; the archive-layer value set has no position-named member; every story below addresses a definition by binding instead of by path.

---

## Phase 3: User Story 1 - 命令运行也能拥有 goal 与 team (Priority: P1) 🎯 MVP

**Goal**: a `/speckit.*` command run creates and owns a goal and a team through the same engine, the same definition schema and the same lifecycle as an SDD run; the only difference is the `owner` value on the binding line.

**Independent Test**: in a fixture with no SDD spec directory, create one goal and one team, assert both land under `.specify/goal/<slug>/` and `.specify/teams/<slug>/`, their binding names the command run and no spec, and `.specify/specs/` gains no path.

### Tests for User Story 1 (MANDATORY) ⚠️

- [ ] T016 [US1] Contract test that a command-run goal and team land in the two archive layers and `.specify/specs/` gains no path, in `tests/contract/test_command_run_goal_team.py` (FR-001, FR-033, SC-001) [blockedBy: T015] — evidence: tests/contract/test_command_run_goal_team.py::test_a_command_run_creates_both_definitions_in_the_unified_archive.
- [ ] T017 [P] [US1] Contract test that two runs creating the same slug produce one definition and a refusal naming the existing path plus its owner, in `tests/contract/test_command_run_goal_team.py` (FR-021) [blockedBy: T016] — evidence: tests/contract/test_command_run_goal_team.py::test_a_second_creation_of_a_slug_is_refused_and_names_the_existing_definition.
- [ ] T018 [US1] Record the red-first capture of T016 and T017 in `.specify/specs/092-goal-team-parallel/notes/red-first-evidence.md` with the real output and exit status [blockedBy: T016,T017].

### Implementation for User Story 1

- [ ] T019 [US1] Make the engine's `create` action write owner, owner_id and origin from the calling run's identity instead of from a directory position, so a command run writes `owner: command-run` and its definition stays readable after the run ends (FR-001, FR-004) [blockedBy: T015] — evidence: scripts/python/goal-utils.py (create binding write); guard: tests/contract/test_command_run_goal_team.py::test_a_command_run_creates_both_definitions_in_the_unified_archive.
- [ ] T020 [US1] Implement the command-family read action `command-family --command <name>` in `scripts/python/goal-utils.py` delegating to `flow-class-check.py --action lookup --unit-id command:<name>`, with no second whitelist and no edit to `flow-class-check.py` (FR-005, FR-006) [blockedBy: T015] [green: contracts/command-family-and-declarations.md#C-71] [green: contracts/command-family-and-declarations.md#C-72] [green: contracts/command-family-and-declarations.md#C-73] [green: contracts/command-family-and-declarations.md#C-74] [green: contracts/command-family-and-declarations.md#C-75] [green: contracts/command-family-and-declarations.md#C-76] [green: contracts/command-family-and-declarations.md#C-77] [green: contracts/command-family-and-declarations.md#C-78] [green: contracts/command-family-and-declarations.md#C-79] [green: contracts/command-family-and-declarations.md#C-80] [green: contracts/command-family-and-declarations.md#C-81] [green: contracts/command-family-and-declarations.md#C-82] [green: contracts/command-family-and-declarations.md#C-83] [green: contracts/command-family-and-declarations.md#C-84] [green: contracts/command-family-and-declarations.md#C-85] [green: contracts/command-family-and-declarations.md#C-86] [green: contracts/command-family-and-declarations.md#C-87] [green: contracts/command-family-and-declarations.md#C-88] [green: contracts/command-family-and-declarations.md#C-89] [green: contracts/command-family-and-declarations.md#C-90] — evidence: scripts/python/goal-utils.py (command-family action); guard: tests/contract/test_command_family.py::test_the_family_predicate_is_the_declared_class_not_a_hardcoded_list.
- [ ] T021 [US1] Treat an absent carrier and an `owner-unavailable` lookup as not in the family without guessing or defaulting, using the lookup's own exit codes as the only inputs (FR-005, FR-006) [blockedBy: T020] — evidence: scripts/python/goal-utils.py (command-family refusals); guard: tests/contract/test_command_family.py::test_an_unregistered_carrier_is_not_in_the_family_and_readability_is_not_affected.
- [ ] T022 [P] [US1] Declare `/speckit.feedback` as the first evidence command — its goal/team creation moment and that it needs no spec directory — in `templates/commands/feedback.md` (FR-005, FR-040) [blockedBy: T020] — evidence: templates/commands/feedback.md (goal/team creation declaration); guard: tests/contract/test_feedback_command_template.py::test_the_template_declares_its_goal_team_creation_moment.
- [ ] T023 [US1] Route the family predicate through the engine action and `create-team` only, and assert `flow-class-check.py` is byte-unchanged by this feature (FR-006, FR-031) [blockedBy: T021] — evidence: scripts/python/goal-utils.py + skills/internal/create-team/SKILL.md; guard: tests/contract/test_command_family.py::test_flow_class_check_is_not_modified_and_no_second_whitelist_exists.
- [ ] T024 [US1] Let a command outside the family read a definition it was handed, and pin that the family decides creation and ownership only, in `tests/contract/test_command_family.py` (FR-005) [blockedBy: T023] — evidence: tests/contract/test_command_family.py::test_a_non_family_command_may_still_read_but_not_create.
- [ ] T025 [US1] Author the declaration fact `shared/declarations/facts/goal-team-command-family.yaml` with fact, `kind: closed-set`, statement (the explicit addition list on top of the class predicate), consumers and former_carriers, where an empty statement means class-predicate-only (FR-005, FR-031) [blockedBy: T020] — evidence: shared/declarations/facts/goal-team-command-family.yaml; guard: tests/contract/test_declaration_facts.py::test_the_command_family_fact_carries_its_mandatory_keys.
- [ ] T026 [US1] Refuse a declared addition whose carrier does not exist, and pin that the statement is an addition list rather than the whole family, in `tests/contract/test_declaration_facts.py` (FR-005) [blockedBy: T025] — evidence: tests/contract/test_declaration_facts.py::test_a_declared_addition_without_a_carrier_is_an_input_error.
- [ ] T027 [US1] Assert the fact file parses under the layer's YAML subset through `declaration_reader.parse_subset` and carries all five mandatory keys, in `tests/contract/test_declaration_facts.py` (FR-031) [blockedBy: T025] — evidence: tests/contract/test_declaration_facts.py::test_both_new_facts_parse_under_the_declaration_subset.

**Checkpoint**: a `/speckit.feedback` run can create and own a goal and a team, the family predicate is a declared class rather than a list, and a duplicate slug is refused.

---

## Phase 4: User Story 2 - 档案统一落 `.specify/goal/` 与 `.specify/teams/`，旧数据归档不删除 (Priority: P1) 🎯 MVP

**Goal**: one landing point, one migration that moves rather than deletes, an idempotent second run, a resumable interrupted run, and zero remaining code paths that write into a spec subdirectory.

**Independent Test**: in a fixture replicating today's layout, run the migration; assert the unified archive gains equivalent definitions, every source tree is still readable under `.specify/archive/goal-team/trees/`, a receipt names source spec and both slugs, and a second run writes nothing.

### Tests for User Story 2 (MANDATORY) ⚠️

- [ ] T028 [P] [US2] Contract test that `migrate-archive` moves a definition atomically and leaves a receipt with `delete_policy: archive-not-delete`, in `tests/contract/test_archive_migration.py` (FR-009, FR-010, FR-033) [blockedBy: T015] [green: contracts/unified-archive-and-migration.md#C-31] [green: contracts/unified-archive-and-migration.md#C-32] [green: contracts/unified-archive-and-migration.md#C-33] [green: contracts/unified-archive-and-migration.md#C-34] [green: contracts/unified-archive-and-migration.md#C-35] [green: contracts/unified-archive-and-migration.md#C-36] [green: contracts/unified-archive-and-migration.md#C-37] [green: contracts/unified-archive-and-migration.md#C-38] [green: contracts/unified-archive-and-migration.md#C-39] [green: contracts/unified-archive-and-migration.md#C-40] [green: contracts/unified-archive-and-migration.md#C-41] [green: contracts/unified-archive-and-migration.md#C-42] [green: contracts/unified-archive-and-migration.md#C-43] [green: contracts/unified-archive-and-migration.md#C-44] [green: contracts/unified-archive-and-migration.md#C-45] [green: contracts/unified-archive-and-migration.md#C-46] [green: contracts/unified-archive-and-migration.md#C-47] [green: contracts/unified-archive-and-migration.md#C-48] [green: contracts/unified-archive-and-migration.md#C-49] [green: contracts/unified-archive-and-migration.md#C-50] — evidence: tests/contract/test_archive_migration.py::test_migration_moves_the_tree_and_leaves_an_archive_not_delete_receipt.
- [ ] T029 [US2] Contract test that a second migration run performs zero writes, emits `result: noop` per definition, writes no receipt and exits 0, in `tests/contract/test_archive_migration.py` (FR-009, SC-004) [blockedBy: T028] — evidence: tests/contract/test_archive_migration.py::test_a_second_run_writes_nothing_and_is_a_noop.
- [ ] T030 [US2] Contract test that a non-equivalent conflict refuses to overwrite, names both candidate paths and exits 4, comparing the concept payload only, in `tests/contract/test_archive_migration.py` (FR-011) [blockedBy: T029] — evidence: tests/contract/test_archive_migration.py::test_a_conflict_names_both_candidates_and_never_overwrites.
- [ ] T031 [US2] Contract test that an interrupted migration reports its stage and resumes without moving the tree twice, in `tests/contract/test_migration_interruption.py` (FR-010, SC-011) [blockedBy: T030] — evidence: tests/contract/test_migration_interruption.py::test_an_interrupted_run_reports_its_step_and_resumes_without_a_second_move.
- [ ] T032 [US2] Integration test over the real tree's shape: after migration the residual count is zero, every unified definition exists, and every source file is readable under trees, in `tests/integration/test_archive_migration_real_data.py` (FR-042, SC-003) [blockedBy: T031] — evidence: tests/integration/test_archive_migration_real_data.py::test_every_source_tree_stays_readable_after_migration.
- [ ] T033 [US2] Record the red-first captures of T028–T032 in `.specify/specs/092-goal-team-parallel/notes/red-first-evidence.md` with the real output and exit status [blockedBy: T028,T029,T030,T031,T032].

### Implementation for User Story 2

- [ ] T034 [US2] Implement the `migrate-archive` action in `scripts/python/goal-utils.py` as an action of the existing engine with no second executable: move rather than copy; write and validate the target, then move the source tree to trees, then write the receipt (FR-009, FR-010, FR-012) [blockedBy: T015] — evidence: scripts/python/goal-utils.py (migrate-archive action); guard: tests/contract/test_archive_migration.py::test_migration_moves_the_tree_and_leaves_an_archive_not_delete_receipt.
- [ ] T035 [US2] Write the migration receipt as one file per definition at `.specify/archive/goal-team/receipts/<kind>-<slug>.yaml` with the nine mandatory fields and the literal `delete_policy: archive-not-delete`, and the moved tree at `.specify/archive/goal-team/trees/<spec-dir-name>/<kind>/<slug>/` (FR-010) [blockedBy: T034] — evidence: scripts/python/goal-utils.py (receipt writer); guard: tests/contract/test_archive_migration.py::test_the_receipt_carries_every_mandatory_field.
- [ ] T036 [US2] Keep the two receipt shapes distinct — a migration receipt (`migrated` / `noop` / `conflict` / `interrupted`) and an archive receipt (`archived`, written when a definition retires in place) — under the same directory family, and never read a receipt as a current fact (FR-010) [blockedBy: T035] — evidence: scripts/python/goal-utils.py (receipt kinds); guard: tests/contract/test_archive_migration.py::test_archive_and_migration_receipts_are_distinguishable_and_not_a_read_surface.
- [ ] T037 [US2] Preserve the definition when moving it: the archive layout is `.specify/goal/<slug>/goal.md` and `.specify/teams/<slug>/team.md` with every owned file inside its own directory, slug and body and lifecycle preserved, origin set to the source spec directory, and no cross-definition lineage rebuilt (FR-009, FR-010) [blockedBy: T034] — evidence: scripts/python/goal-utils.py (migrate-archive target layout); guard: tests/contract/test_archive_migration.py::test_origin_is_set_and_no_lineage_is_rebuilt.
- [ ] T038 [US2] Implement the archive-not-delete invariant: no source file is deleted, the moved tree stays readable under trees, the receipt names where, and a migration that would delete refuses before writing anything (FR-010) [blockedBy: T035] — evidence: scripts/python/goal-utils.py (archive-not-delete guard); guard: tests/contract/test_archive_migration.py::test_every_source_file_is_readable_under_trees_after_migration.
- [ ] T039 [US2] Make the second run idempotent: zero writes, `result: noop` per definition, no new receipt, exit 0, and never overwrite an existing unified definition (FR-009) [blockedBy: T034] — evidence: scripts/python/goal-utils.py (idempotency path); guard: tests/contract/test_archive_migration.py::test_a_second_run_writes_nothing_and_is_a_noop.
- [ ] T040 [P] [US2] Implement interruption semantics: report the reached step and actual state, exit 3 (distinct from 0 complete and 2 input error), and resume from that step without moving a source tree twice (FR-010, SC-011) [blockedBy: T034] — evidence: scripts/python/goal-utils.py (resume path); guard: tests/contract/test_migration_interruption.py::test_an_interrupted_run_reports_its_step_and_resumes_without_a_second_move.
- [ ] T041 [US2] Implement `--dry-run` performing every read and decision while writing nothing (no archive directory, no receipt, no definition), and pin that dry run and real run reach the same decisions (FR-042) [blockedBy: T034] — evidence: scripts/python/goal-utils.py (--dry-run); guard: tests/contract/test_archive_migration.py::test_the_dry_run_writes_nothing_and_agrees_with_the_real_run.

**Checkpoint**: the archive is single; migration moves without deleting, is idempotent, refuses conflicts, and resumes; the residual probe is the only spec-local reader.

---

## Phase 5: User Story 3 - spec 与 goal+team 是两条平行线，简单工作各自直接做 (Priority: P1) 🎯 MVP

**Goal**: neither line requires the other to exist. A run with no goal/team completes, and a goal+team with no spec directory completes, and neither construct contains a precondition asking for the other.

**Independent Test**: two fixtures — one SDD-only run with no goal/team, one goal+team with no spec directory — each complete a delivery, and injecting a "requires the other line" precondition turns the test red.

### Tests for User Story 3 (MANDATORY) ⚠️

- [ ] T042 [P] [US3] Contract test asserting the negative: with the other line absent, every command of one line still exits 0, in `tests/contract/test_parallel_lines.py` (FR-014, FR-033) [blockedBy: T015] — evidence: tests/contract/test_parallel_lines.py::test_neither_line_requires_the_other_to_exist.
- [ ] T043 [P] [US3] Integration test running the two peer fixtures end to end (SDD-only declared `direct` by the threshold, goal+team with no spec dir), asserting each delivers and neither skips a creation to fake the result, in `tests/integration/test_parallel_lines.py` (FR-014, SC-005) [blockedBy: T054] — evidence: tests/integration/test_parallel_lines.py::test_both_peer_fixtures_deliver_independently.
- [ ] T044 [US3] Record the red-first captures of T042 and T043 in `.specify/specs/092-goal-team-parallel/notes/red-first-evidence.md`, including the injected-precondition mutation that turns them red [blockedBy: T042,T043].

### Implementation for User Story 3

- [ ] T045 [US3] Remove every ownership inference from a path prefix in the engine and the team mechanism, routing all ownership questions through the `binding` read action (FR-015) [blockedBy: T012] — evidence: scripts/python/goal-utils.py + skills/internal/create-team/SKILL.md (ownership reads); guard: tests/contract/test_parallel_lines.py::test_no_owner_is_derived_from_a_path_prefix.
- [ ] T046 [US3] Keep N teams to 1 goal legal and expressed only by `goal_slug` on the team side, refusing a team that stores a copy of the goal's objective or criteria, and refusing a team lifecycle outside `active` / `archived` (FR-023, FR-026) [blockedBy: T045] — evidence: skills/internal/create-team/SKILL.md (goal_slug identity); guard: tests/contract/test_parallel_lines.py::test_many_teams_may_bind_one_goal_and_no_goal_content_is_copied.
- [ ] T047 [US3] Record `archive_layer` (the C-9 value) in place of the retired scope names in `scripts/python/sdd-route.py authorize`, resolving the team path through the binding and scope actions rather than a second path implementation (FR-027) [blockedBy: T014] — evidence: scripts/python/sdd-route.py (authorize archive_layer); guard: tests/contract/test_parallel_lines.py::test_authorize_records_the_archive_layer_not_a_scope_name.
- [ ] T048 [US3] Carry the binding record of the loaded team on `run-checks` without changing its existing resolution keys, and document any added key in `skills/internal/run-team/SKILL.md` (FR-038) [blockedBy: T012] — evidence: scripts/python/goal-utils.py (run-checks) + skills/internal/run-team/SKILL.md; guard: tests/contract/test_parallel_lines.py::test_run_checks_carries_the_binding_and_keeps_its_resolution_keys.

**Checkpoint**: both lines deliver independently; ownership is answered only by the binding record; the routing layer records an archive layer, not a position.

---

## Phase 6: User Story 4 - 复杂工作：设计师出设计稿，施工队按交接契约施工 (Priority: P1) 🎯 MVP

**Goal**: complexity is decided by one declared threshold; a `handoff` run emits `<spec-dir>/handoff.md` whose keys resolve three ways; the crew's territory is expanded by an explicit modification and the three spec artifacts stay spec-side.

**Independent Test**: a fixture spec above the threshold emits a `handoff.md` whose `goal_slug` and `team_slug` resolve to the two definitions and whose two `handoff_ref` values point back at it; a crew write to `tasks.md` is refused with a non-zero exit naming the path and the seat.

### Tests for User Story 4 (MANDATORY) ⚠️

- [ ] T049 [P] [US4] Contract test resolving the three-way key pair in both directions across `handoff.md` and the two definitions, in `tests/contract/test_handoff_contract.py` (FR-034, FR-033, SC-006) [blockedBy: T015] [green: contracts/handoff-contract.md#C-53] [green: contracts/handoff-contract.md#C-54] [green: contracts/handoff-contract.md#C-55] [green: contracts/handoff-contract.md#C-56] [green: contracts/handoff-contract.md#C-57] [green: contracts/handoff-contract.md#C-58] [green: contracts/handoff-contract.md#C-59] [green: contracts/handoff-contract.md#C-60] [green: contracts/handoff-contract.md#C-61] [green: contracts/handoff-contract.md#C-62] [green: contracts/handoff-contract.md#C-63] [green: contracts/handoff-contract.md#C-64] [green: contracts/handoff-contract.md#C-65] [green: contracts/handoff-contract.md#C-66] [green: contracts/handoff-contract.md#C-67] [green: contracts/handoff-contract.md#C-68] [green: contracts/handoff-contract.md#C-69] [green: contracts/handoff-contract.md#C-70] — evidence: tests/contract/test_handoff_contract.py::test_the_three_way_keys_resolve_in_both_directions.
- [ ] T050 [P] [US4] Contract test that a crew write onto a spec artifact is refused with a non-zero exit naming the path and the seat, in `tests/contract/test_handoff_territory.py` (FR-036, SC-007) [blockedBy: T015] — evidence: tests/contract/test_handoff_territory.py::test_a_crew_write_onto_a_spec_artifact_is_refused_by_the_territory_check.
- [ ] T051 [P] [US4] Contract test that the declared threshold decides both complexity and creation timing, with equality on the simple side, in `tests/contract/test_declaration_facts.py` (FR-018, FR-039) [blockedBy: T015] — evidence: tests/contract/test_declaration_facts.py::test_the_threshold_decides_both_complexity_and_creation_timing.
- [ ] T052 [US4] Record the red-first captures of T049–T051 in `.specify/specs/092-goal-team-parallel/notes/red-first-evidence.md` with the real output and exit status [blockedBy: T049,T050,T051].

### Implementation for User Story 4

- [ ] T053 [US4] Author the declaration fact `shared/declarations/facts/goal-team-handoff-threshold.yaml` with `kind: threshold`, statement keys `metric: task-count`, `threshold: <int>`, `boundary: exclusive`, and the creation-timing pair `on_direct: none` / `on_handoff: after-tasks-u4` (FR-018, FR-039) [blockedBy: T015] — evidence: shared/declarations/facts/goal-team-handoff-threshold.yaml; guard: tests/contract/test_declaration_facts.py::test_the_handoff_threshold_fact_declares_the_boundary_and_the_timing_pair.
- [ ] T054 [US4] Implement the `handoff-decision --tasks <path>` action returning `direct` or `handoff` plus the measured task count and the declared threshold, exiting 2 with `owner-unavailable` when the fact is absent, never falling back to a built-in number, and refusing consumption of a handoff on a `direct` spec (FR-018, FR-039) [blockedBy: T053] — evidence: scripts/python/goal-utils.py (handoff-decision); guard: tests/contract/test_declaration_facts.py::test_handoff_decision_refuses_when_the_fact_is_unavailable.
- [ ] T055 [US4] Assert no engine constant, driver sentence or command template carries the threshold literal outside its fact file, in `tests/contract/test_declaration_facts.py` (FR-031) [blockedBy: T054] — evidence: tests/contract/test_declaration_facts.py::test_the_threshold_literal_exists_only_in_its_fact_file.
- [ ] T056 [US4] Register both new facts in `shared/declarations/contract.yaml` additively — one enumeration row per fact carrying fact, `subset_id: declaration-subset/v1`, value_domain and statement_keys — without renaming or reordering existing keys, so an unregistered fact reads `owner-unavailable` rather than a default (FR-031) [blockedBy: T053] — evidence: shared/declarations/contract.yaml (fact registration); guard: tests/contract/test_declaration_facts.py::test_both_facts_are_registered_with_subset_and_value_domain.
- [ ] T057 [US4] Refuse a fact written in any grammar other than `declaration-subset/v1` at load, and validate the consumer against the registered value_domain (`closed-set` for the family fact, `threshold+timing-map` for the threshold fact) without a second hardcoded copy (FR-031) [blockedBy: T056] — evidence: scripts/python/goal-utils.py (declaration domain validation); guard: tests/contract/test_declaration_facts.py::test_a_fact_in_another_grammar_is_refused_at_load.
- [ ] T058 [US4] Keep the registration additive and both consumption points inside engines this feature creates or modifies — `goal-utils.py` and `create-team`, never `flow-class-check.py`, `run-stage.sh` or `stage-runner.sh` (FR-031) [blockedBy: T056] — evidence: shared/declarations/contract.yaml + scripts/python/goal-utils.py; guard: tests/contract/test_declaration_facts.py::test_registration_is_additive_and_both_consumers_are_in_scope.
- [ ] T059 [US4] Author `handoff.md`'s shape in `skills/internal/create-team/references/handoff-contract-template.md`: the eight mandatory sections in order with `None.` for an empty one, the `handoff/v1` frontmatter, `state: active | fulfilled | abandoned` as a two-terminal-state machine never deleted, a fixed relative path with no variant names, and production by the tasks stage only (FR-016, FR-035) [blockedBy: T015] — evidence: skills/internal/create-team/references/handoff-contract-template.md; guard: tests/contract/test_handoff_contract.py::test_the_contract_carries_its_eight_sections_in_order.
- [ ] T060 [US4] Cite rather than copy: `## Goal` cites `goal_slug` only, `## Targets` cites the goal's T-NNN ids, and `## Task Reference` references id ranges or an explicit list while a task-row line in the contract is a refused defect (`task-copy-in-handoff`) (FR-016, FR-019) [blockedBy: T059] — evidence: skills/internal/create-team/references/handoff-contract-template.md (citing sections); guard: tests/contract/test_handoff_contract.py::test_the_contract_cites_and_never_copies_task_rows.
- [ ] T061 [US4] Refuse at creation a `goal_slug` or `team_slug` that does not resolve (`handoff-dangling-key`, exit 2), and write the reverse `handoff_ref` on both definitions through the engine's binding action so a contract never names a team that does not exist (FR-034) [blockedBy: T012,T059] — evidence: scripts/python/goal-utils.py (handoff_ref write) + skills/internal/create-team/SKILL.md; guard: tests/contract/test_handoff_contract.py::test_a_dangling_handoff_key_is_refused_at_creation.
- [ ] T062 [US4] Expand the contract's `## Territory` into territory.write of every team bound to that `goal_slug` as an explicit, disclosed `improve-team` modification (one record per team), keep granted entries inside the spec directory and out of the two archive layers, and force requirements.md, tasks.md, verification.md and handoff.md into territory.forbidden while the writeback is one record per task (FR-017, FR-036, FR-020) [blockedBy: T059] — evidence: skills/internal/improve-team/SKILL.md (territory expansion); guard: tests/contract/test_handoff_territory.py::test_the_territory_expansion_is_recorded_and_forbids_the_four_spec_artifacts.

**Checkpoint**: complexity is declared once, a handoff contract resolves three ways, and the crew cannot write the three spec artifacts or the contract itself.

---

## Phase 7: User Story 5 - 「临时 / 全局」被绑定模型取代 (Priority: P1) 🎯 MVP

**Goal**: the legacy vocabulary is gone from every runtime criterion surface; ownership is answered by the binding record; writability is a computed function rather than a forbidden-path prohibition; and the 085 guard modules are disposed by measurement.

**Independent Test**: a programmatic scan of the runtime surfaces reports zero legacy words used as a classification criterion; a goal's ownership changes by a binding rewrite with the file's non-binding bytes unchanged; and the measured 085 disposal table has one dispositioned row per module.

### Tests for User Story 5 (MANDATORY) ⚠️

- [ ] T063 [P] [US5] Contract test that a rebind changes ownership only and the file-minus-binding hash is unchanged, in `tests/contract/test_binding_model.py` (FR-003, SC-009) [blockedBy: T009] — evidence: tests/contract/test_binding_model.py::test_rebind_changes_only_the_binding_block.
- [ ] T064 [P] [US5] Contract test scanning shared, skills, scripts, templates and src for the legacy words used as a goal/team classification criterion, passing only on an empty hit set apart from the owner's historical record and the temp-directory exemption, in `tests/contract/test_criterion_vocabulary_scan.py` (FR-022, SC-008) [blockedBy: T015] — evidence: tests/contract/test_criterion_vocabulary_scan.py::test_no_runtime_surface_uses_temporary_or_global_as_a_criterion.
- [ ] T065 [P] [US5] Contract test comparing the measured 085 disposal table against a programmatic re-measurement, turning red on an undisposed row, and asserting the post-disposal contract suite has zero new failing ids against the serial baseline, in `tests/contract/test_085_disposal_table.py` (FR-041, SC-010) [blockedBy: T015] — evidence: tests/contract/test_085_disposal_table.py::test_every_measured_module_has_exactly_one_disposition.
- [ ] T066 [US5] Record the red-first captures of T063–T065 in `.specify/specs/092-goal-team-parallel/notes/red-first-evidence.md`, including the two synthetic mutations (re-injected criterion phrase, directory-prefix ownership) [blockedBy: T063,T064,T065].

### Implementation for User Story 5

- [ ] T067 [US5] Rewrite `shared/definitions/goal-definitions.md` to own the binding record's meaning, the archive-layer vocabulary, the lifecycle names including the terminal-retained and reopen rules, and the origin semantics, without restating the engine's action signatures, with the legacy-key removal point recorded in § Terminology Boundaries, and citing the team owner rather than restating its domain (FR-024, FR-028, FR-032) [blockedBy: T009] — evidence: shared/definitions/goal-definitions.md; guard: tests/contract/test_binding_model.py::test_the_goal_owner_owns_the_concepts_and_not_the_action_signatures.
- [ ] T068 [US5] Rewrite `skills/internal/create-team/references/conceptual-model.md` to own the team side — binding, `active | archived`, `handoff_ref`, the crew notion — without restating the goal-side table, such that neither owner restates the other's closed value domain and each cites the other by path and section (FR-024, FR-032) [blockedBy: T067] — evidence: skills/internal/create-team/references/conceptual-model.md; guard: tests/contract/test_binding_model.py::test_the_two_owners_cite_each_other_and_restate_no_value_domain.
- [ ] T069 [US5] Replace the Temporary run-scoped scopes carve-out paragraph in `shared/definitions/sdd-routing-definitions.md` with a carve-out permitting sdd-run and command-run definitions in the archive layers, keeping verbatim the prohibition that one SDD run must not create, rebind, rescope or terminate an existing definition in a shared archive, and containing no Temporary or 临时 as a criterion name (FR-027) [blockedBy: T067] — evidence: shared/definitions/sdd-routing-definitions.md § Hierarchy; guard: tests/contract/test_criterion_vocabulary_scan.py::test_the_routing_carve_out_keeps_the_hierarchy_prohibition_verbatim.
- [ ] T070 [US5] Make the carve-out cite the two concept owners by path and restate no value domain — no owner values, no layer names beyond a path pointer (FR-024, FR-027) [blockedBy: T069] — evidence: shared/definitions/sdd-routing-definitions.md (pointer-only carve-out); guard: tests/contract/test_criterion_vocabulary_scan.py::test_the_carve_out_cites_owners_and_restates_no_domain.
- [ ] T071 [US5] Retitle and rewrite the goal/team section of `skills/external/sdd-loop-driver/SKILL.md` to the binding model: when a goal/team is created, where it lands, under which binding, with the creation moment read from `goal-team-handoff-threshold.yaml` rather than restated (FR-028, FR-039) [blockedBy: T053] — evidence: skills/external/sdd-loop-driver/SKILL.md (binding-model section); guard: tests/contract/test_sdd_loop_driver_skill.py::test_the_goal_team_section_uses_the_binding_model.
- [ ] T072 [US5] Rewrite the goal/team sentences in `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` and the implement-package guidance in `references/decomposition-model.md`, replacing the three legacy spine keys with goal_slug and team_slug and origin_spec_dir with the engine reading the old keys only through its alias and failing them as `legacy-key-dangling` when unresolvable, while keeping the four-part checkpoint, the direction audit, the stage chain and the sentinels unchanged and adding no stage, sentinel, watcher rule or exit code (FR-028) [blockedBy: T071] — evidence: skills/external/sdd-loop-driver/references/checkpoint-protocol.md + references/decomposition-model.md; guard: tests/contract/test_checkpoint_protocol.py::test_the_goal_team_sentences_use_the_new_keys_and_the_stage_chain_is_unchanged.

**Checkpoint**: the vocabulary is gone from every criterion surface, ownership is binding-only, and the 085 guards are disposed by a measured table rather than by deletion.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: the projection sweep, the remaining write-path guards, the real-data dry run and migration, and the closure readings.

- [ ] T073 [P] Update `shared/definitions/framework-map.md` so the Goals and Teams rows name only `.specify/goal/` and `.specify/teams/`, the archive row names `.specify/archive/goal-team/`, and the `.specify/specs/` row no longer implies goal/team subdirectories (FR-029) [blockedBy: T067] — evidence: shared/definitions/framework-map.md (Goals/Teams/archive rows); guard: tests/contract/test_framework_map_archive_row.py::test_the_framework_map_names_the_unified_archive_and_drops_spec_local_goal_team.
- [ ] T074 [P] Update `templates/commands/goal.md` to expose the `migrate-archive` mode and cite the scope value set by pointer, and `templates/commands/team.md` to drop the spec hint and cite by pointer without gaining a migration mode (FR-030) [blockedBy: T014] — evidence: templates/commands/goal.md + templates/commands/team.md; guard: tests/contract/test_goal_command_template.py::test_the_goal_template_exposes_migrate_archive_and_cites_the_scope_domain.
- [ ] T075 Make `skills/internal/manage-goal`, `skills/internal/run-team` and `skills/internal/improve-team` follow the new paths and model, each citing the mode and action owners rather than restating arguments (FR-030, FR-038) [blockedBy: T067] — evidence: skills/internal/manage-goal/SKILL.md + run-team/SKILL.md + improve-team/SKILL.md; guard: tests/contract/test_binding_model.py::test_the_three_management_skills_cite_owners_and_restate_no_arguments.
- [ ] T076 Author the structural invariant asserting no code path writes a spec-local goal or team tree, enumerating the engine's writing actions, the `create-team` persistence step and the driver instructions, and naming the engine's action table as the one enumerable place a writing surface may live (FR-013, SC-002) [blockedBy: T034,T045] [green: contracts/owner-rewrites-and-tests.md#C-91] [green: contracts/owner-rewrites-and-tests.md#C-92] [green: contracts/owner-rewrites-and-tests.md#C-93] [green: contracts/owner-rewrites-and-tests.md#C-94] [green: contracts/owner-rewrites-and-tests.md#C-95] [green: contracts/owner-rewrites-and-tests.md#C-96] [green: contracts/owner-rewrites-and-tests.md#C-97] [green: contracts/owner-rewrites-and-tests.md#C-98] [green: contracts/owner-rewrites-and-tests.md#C-99] [green: contracts/owner-rewrites-and-tests.md#C-100] [green: contracts/owner-rewrites-and-tests.md#C-101] [green: contracts/owner-rewrites-and-tests.md#C-102] [green: contracts/owner-rewrites-and-tests.md#C-103] [green: contracts/owner-rewrites-and-tests.md#C-104] [green: contracts/owner-rewrites-and-tests.md#C-105] [green: contracts/owner-rewrites-and-tests.md#C-106] [green: contracts/owner-rewrites-and-tests.md#C-107] [green: contracts/owner-rewrites-and-tests.md#C-108] [green: contracts/owner-rewrites-and-tests.md#C-109] [green: contracts/owner-rewrites-and-tests.md#C-110] — evidence: tests/contract/test_no_spec_local_writes.py; guard: tests/contract/test_no_spec_local_writes.py::test_no_writing_surface_targets_a_spec_local_goal_or_team.
- [ ] T077 Encode the mutation obligations: T076's module fails when one writing surface is reverted to the old path (synthetic mutation in the test, no tree edit), and T064's module fails when one old phrase is re-injected (FR-013, FR-022) [blockedBy: T076,T064] — evidence: tests/contract/test_no_spec_local_writes.py (mutation arms); guard: tests/contract/test_no_spec_local_writes.py::test_the_guard_goes_red_when_one_surface_is_reverted.
- [ ] T078 Author the residual-probe read surface: `probe-residual` enumerates spec-local goal and team definitions read-only with per-kind counts, residuals are never read as current definitions and never listed, `/speckit.sanitize` renders the reading verbatim without migrating, nothing invokes migration as a side effect, and the run scratch area is never enumerated or reported (FR-012, FR-037, FR-020) [blockedBy: T034] — evidence: scripts/python/goal-utils.py (probe-residual) + templates/commands/sanitize.md; guard: tests/contract/test_archive_migration.py::test_the_residual_probe_is_read_only_and_ignores_the_run_scratch_area.
- [ ] T079 Run the real-data sequence on this repository and record both readings one file per reading under `test-evidence/`: `probe-residual` before, `migrate-archive --dry-run`, `migrate-archive --apply`, `probe-residual` after, and a per-definition existence assertion showing every source tree still readable under trees, compared against `requirements-baseline-probe.txt` rather than a restated constant (FR-042, SC-003) [blockedBy: T034,T073] [green: contracts/unified-archive-and-migration.md#C-51] — evidence: .specify/specs/092-goal-team-parallel/test-evidence/migration-dryrun.json + migration-applied.json + residual-after.txt.
- [ ] T080 Run the closure sequence: remove every fixture and worktree under `.specify/.tmp/`, run `sync-mirrors.py --check` and `regen-command-copies.py --check`, run the full suite serially and diff the failed-id set against `plan-baseline-names.txt`, and record the readings plus the mirror and copy verdicts and the per-criterion status block in `.specify/specs/092-goal-team-parallel/notes/closure-readings.md` (SC-001…SC-011) [blockedBy: T079] [green: contracts/owner-rewrites-and-tests.md#C-111] [green: contracts/unified-archive-and-migration.md#C-52] — evidence: .specify/specs/092-goal-team-parallel/notes/closure-readings.md + test-evidence/closure-failed.txt.

**Checkpoint**: the projections are generated, the real tree is migrated with archive-not-delete receipts, and the closure readings exist for every criterion.

---

## Green Partition

Each clause of the five contract pages is turned green by exactly one row. The `validate-tasks.py` checks — `green-dangling`, `green-clause-collision`, `green-cross-phase` — are the machine criterion for this table; the table is its human-readable export and MUST agree with the rows.

| Contract page | Clause → row |
|---------------|--------------|
| `binding-and-lifecycle.md` (30) | C-1 … C-29 → T005 · C-30 → T067 |
| `unified-archive-and-migration.md` (22) | C-31 … C-50 → T028 · C-51 → T079 · C-52 → T080 |
| `handoff-contract.md` (18) | C-53 … C-70 → T049 |
| `command-family-and-declarations.md` (20) | C-71 … C-90 → T020 |
| `owner-rewrites-and-tests.md` (21) | C-91 … C-110 → T076 · C-111 → T080 |

**Count check**: 30 + 22 + 18 + 20 + 21 = **111** clauses, **111** claims, 0 collisions, 0 dangling, 0 cross-phase inversions — the `validate-tasks.py` reading recorded at `test-evidence/validate-tasks.txt` reports `0 error(s), 1 warning(s)`, and that one warning is the disclosed forward edge `T043 → T054`.

**Attribution granularity is the module, and that is deliberate.** `validate-tasks.py`'s `green-path-divergence` rule assumes *one module, one green point*: a test module is turned green by one red-first row (§ Tests Mode: each module is authored red once, then filled). A contract page whose 30 clauses are exercised by `tests/contract/test_binding_model.py` therefore cannot hand each clause to its own row without splitting a module across rows — the very thing the red-first rule forbids. So the tag names **the row that owns the module's green point**, and the clauses listed beside it are the contract text that module turns green. Per-clause ownership inside one module is the module's own test names, each named in that row's `guard:` pointer. Where a clause leaves the module's scope and lands in another module, or is reached by a stage-level reading rather than a unit test, it gets its own row's tag (C-30 → T067, C-51 → T079, C-52 → T080, C-111 → T080).

## FR → row trace (DoD-1 lane)

Every FR is quoted at line level by at least one row of this file, the only form `pre-analyze-check.py` accepts.

| FR | Rows that quote it | FR | Rows that quote it |
|----|--------------------|----|--------------------|
| FR-001 | T016, T019 | FR-022 | T064, T077 |
| FR-002 | T005, T006, T007, T008 | FR-023 | T006, T046 |
| FR-003 | T009, T010, T063 | FR-024 | T067, T068, T070 |
| FR-004 | T019 | FR-025 | T013 |
| FR-005 | T020, T021, T024, T025, T026 | FR-026 | T011, T046 |
| FR-006 | T020, T021, T023 | FR-027 | T015, T047, T069, T070 |
| FR-007 | T014, T015 | FR-028 | T067, T071, T072 |
| FR-008 | T013, T014 | FR-029 | T073 |
| FR-009 | T008, T028, T034, T037, T039 | FR-030 | T074, T075 |
| FR-010 | T028, T031, T034, T035, T036, T037, T038, T040 | FR-031 | T023, T025, T027, T055, T056, T057, T058 |
| FR-011 | T030 | FR-032 | T067, T068 |
| FR-012 | T034, T078 | FR-033 | T016, T028, T042, T049 |
| FR-013 | T076, T077 | FR-034 | T049, T061 |
| FR-014 | T042, T043 | FR-035 | T059, T060 |
| FR-015 | T012, T045 | FR-036 | T050, T062 |
| FR-016 | T059, T060 | FR-037 | T078 |
| FR-017 | T062 | FR-038 | T048, T075 |
| FR-018 | T051, T053, T054 | FR-039 | T051, T053, T054, T071 |
| FR-019 | T060, T062 | FR-040 | T022 |
| FR-020 | T062, T078 | FR-041 | T065 |
| FR-021 | T017 | FR-042 | T032, T041, T079 |

**FR lane note**: FR-032 (framework-source landing plus mirror synchronisation, template neutrality preserved) is discharged by the two owner rewrites T067 and T068 writing framework sources and by GATE-2's projection check; it is quoted on those rows so the lane is not empty. FR-033 (every decidable assertion carries a test that turns red when the implementation is missing) is quoted on one guard row per story so the lane reads the obligation in each phase rather than once.

## 085 disposal table (measured, FR-041 / SC-010)

Re-measured this stage with `grep -cE "scope|spec-local|temp_goal|temp_team|temporary" <module>` per module. Counts are matching-line counts, not a claim about how many assertions must change; the `historical` rows name the measured reason they are not rewritten.

| # | Module | Matching lines | Disposition | One-line reason |
|---|--------|---------------|-------------|-----------------|
| 1 | `tests/contract/test_scope_resolution.py` | 19 | rewrite | the scope facts still hold; only the value names (`goal` / `teams` / `auto`) and the disappearance of `spec` change; the `spec` assertions become "refused with invalid choice" |
| 2 | `tests/contract/test_temp_goal_contract.py` | 18 | rewrite | the temporary-goal concept is replaced by the binding model; the asserted facts (a goal definition carries its owner, a terminal goal refuses a rebind) survive under new names |
| 3 | `tests/contract/test_temp_team_schema.py` | 17 | rewrite | the team schema survives; the binding block and `handoff_ref` are added, `lifecycle_state` unchanged |
| 4 | `tests/contract/test_goal_targets_check.py` | 8 | rewrite | the targets check is orthogonal to scope; only its scope fixture path moves to the unified archive |
| 5 | `tests/contract/test_goal_targets_engine.py` | 1 | rewrite | the single matching line is a fixture path literal; the fixture path moves, the assertion stays |
| 6 | `tests/contract/test_checkpoint_protocol.py` | 2 | rewrite | the protocol's goal sentences move to the binding model and the three legacy spine keys are replaced |
| 7 | `tests/contract/test_expression_compatibility.py` | 11 | historical | a dated-record compatibility module; its expectations are frozen by an earlier feature's recorded hashes and MUST NOT be retro-edited (create-tasks skill, runtime-evidence landing points) |
| 8 | `tests/contract/test_sdd_loop_driver_wp_model.py` | 7 | rewrite | the WP model's goal/team sentences and package-count expectations move to the new driver text |
| 9 | `tests/unit/test_goal_scope_engine.py` | 30 | rewrite | the `spec` assertions become "refused" assertions; the rest move to the new value names |
| 10 | `tests/unit/test_goal_utils.py` | 1 | rewrite | the engine's action table grows; the one scope touch becomes an archive-layer assertion |
| 11 | `tests/integration/test_checkpoint_rollback.py` | 1 | rewrite | the rollback fixture's goal path moves to `.specify/goal/<slug>/` |
| 12 | `tests/contract/test_goal_writeset.py` | 1 | historical | A7 named it as a starting point; the measured matching line is a docstring path, no assertion subject changed, so it is marked and left in place |

**Count check**: **12** rows, of which **11** carry a real spec-local or scope assertion and **1** (`test_goal_writeset.py`) is marked historical on a measured non-finding. Plan C-102 said 11 modules plus this one "carries none"; the measured count here is 11 substantive + 1 historical, and the difference is the classification of the one line in row 5 (`test_goal_targets_engine.py`), which is a fixture path rather than an assertion. Both documents agree that module is in the list; only the reason differs, and the reason is recorded above. T065 asserts this table against a re-measurement, so a fourth module appearing later turns the guard red rather than being absorbed.

## Mutable-state and file-ownership map (concurrent dispatch safety)

The implement stage runs up to six packages concurrently in isolated worktrees. The rows below are the only paths more than one package touches, and each is partitioned by **section** so the merge is textual rather than semantic.

| Path | Editing packages | Partition |
|------|------------------|-----------|
| `scripts/python/goal-utils.py` | `wp01-foundation` (T005–T015), `wp02-archive-migration` (T034–T041), `wp03-command-family` (T020–T021, T053–T057), `wp05` (T045, T048) | T005–T015 own the binding parser and `resolve_scope`; T034–T041 own a new `migrate-archive` / `probe-residual` block appended after the existing actions; T020–T021 own the `command-family` action; T053–T057 own `handoff-decision` and the declaration read. Four disjoint sections, merged in the declared integration order. |
| `tests/contract/test_binding_model.py` | `wp01` (T005–T015), `wp05` (T063, T067), `wp06` (T075) | the module is created by `wp01`; later packages append functions at the end. `wp01` merges first, so the file exists before the others append. |
| `tests/contract/test_declaration_facts.py` | `wp03` (T025–T027), `wp04`/`wp03` (T051, T053–T058) | functions are appended in row order; no two rows edit the same function. |
| `shared/declarations/contract.yaml` | `wp03` only (T056) | single writer by construction |
| every other path | exactly one package | disjoint by the § Package Map domain column |

Settled-state check: no path is claimed by two packages with an unpartitioned edit region, and no test module is claimed by two packages at different green points (`green-path-divergence`).

---

## Dependencies & Execution Order

### Package Dependencies

- **`wp01-foundation` (T001–T015)**: entry package. Blocks every other package, because every assertion below is written in the binding or archive-layer vocabulary.
- **`wp02-archive-migration` (T028–T041)**, **`wp03-command-family` (T016–T027, T049–T054)** and **`wp05-peers-and-vocabulary` (T042–T048, T063–T072)**: start after `wp01`; they write disjoint path sets and run concurrently (three of the six slots).
- **`wp04-handoff` (T055–T062)**: depends on `wp03` for the threshold fact (T053 → T054 → T059) and runs concurrently with `wp02` / `wp05` once `wp03` merges.
- **`wp06-owners-guards` (T073–T078)**: depends on `wp05` for the rewritten concept owners (T067) and on `wp02` for the migration actions the write-path guard enumerates (T034).
- **`wp07-closure` (T079–T080)**: read-only plus evidence; runs after every write package settles, and its suite runs after the fixture and worktree teardown.

### Within Each Story

Guard row first, red-first capture next, the implementation row that turns it green last — with the migration/regression exception applied to T028–T032, which port and extend existing guard intent and therefore land after the migration action T034 exists, not before it.

### Parallel Opportunities

- Phase 1: T001 is serial; T002 and T003 fan out behind it; T004 follows T003.
- Phase 2: T005 → T006 / T007 / T008 fan out, joining at T009; T009 → T010 → T011 is serial on one action; T012 follows T009; T013 → T014 → T015 is serial on the scope resolver.
- US1, US2 and US5: three disjoint path sets, so T016–T027, T028–T041 and T063–T072 are three parallel tracks after Phase 2.
- US4 after US1's declaration work: T049–T062 serialize on the two fact files and the handoff template.
- US3 in parallel with US2: T042–T048 touch `test_parallel_lines.py`, `sdd-route.py` and `create-team`, none of which the migration track writes.

### Parallel Example: after Phase 2 (three tracks)

```text
Track A (US1 + US4):      T016 → T019 → T020 → T021 → T025 → T023 → T024 → T053 → T054 → T059 → T061 → T062
Track B (US2):            T028 → T034 → T035 → T037 → T038 → T039 → T040 → T041
Track C (US5 + US3):      T042 → T045 → T046 → T063 → T067 → T068 → T069 → T072
Join (US1 ∫ US4):         T049 → T060 → T052
```

## Implementation Strategy

### MVP First

1. Complete Phase 1 Setup and Phase 2 Foundational.
2. Run the three tracks above in parallel — all five stories are P1 and none is independently valuable apart, so the MVP is their junction (T001–T072) rather than any single phase.
3. **STOP and VALIDATE** at T062: a command run owns a goal and a team; the archive is single and migration is idempotent; the two lines deliver independently; a handoff contract resolves three ways and the crew cannot write the spec artifacts; the criterion vocabulary scan is empty.
4. Then Phase 8: projections, the real-data dry run and migration, and the closure readings.

### Incremental Delivery

1. Phase 2 alone ships a binding record and an archive-layer value set that are readable and inert — no behaviour change beyond a stricter validator.
2. US1 + US2 ship the archive: a `/speckit.feedback` run has somewhere to put its goal, and the old spec-local trees are archived rather than deleted.
3. US3 makes the parallel claim provable; US5 removes the old vocabulary that would otherwise let the subordination return by name.
4. US4 adds the designer-to-crew collaboration contract on top of the peer relation.
5. Phase 8 closes the projections and produces the measured evidence for every criterion.

## Notes

- **Rulings made at generation** (disclosed, never folded silently into green):
  - **N-1 — the threshold value.** requirements.md A3 and FR-018 forbid this stage from inventing the number. T053 authors `threshold: 10` as the initial declared value with `boundary: exclusive`, measured on the implement-package sizing the driver declares (a per-package target near 10, ceiling 16 — `decomposition-model.md` § 13, `notes/execution-lessons-2026-11-09.md` lesson 1), so the threshold equals the packaging unit already in force rather than a second invented number. It is one file edit to change (C-82), and T055 asserts the literal exists nowhere else.
  - **N-2 — the legacy-alias removal point.** FR-028 and C-23 require a declared version point. This stage rules the next minor release after 092, recorded in `shared/definitions/goal-definitions.md` § Terminology Boundaries by T067. "Remove in the same release" was rejected because the state-spine keys are written by driver instructions that a running line may not re-read mid-flight.
  - **N-3 — `handoff.md`'s template home.** C-53 fixes the contract's instance at `<spec-dir>/handoff.md` but does not name where the authoring template lives. T059 rules `skills/internal/create-team/references/handoff-contract-template.md`, beside `create-mode.md` and `conceptual-model.md`, so the shape is owned by the skill that produces it and no new top-level directory appears.
  - **N-4 — plan EP-002's count is stale by one.** Plan EP-002 records 7 goal / 7 team spec-local definitions; measured this stage the tree holds **8 / 8** because 092's own spec-local goal and team were created by the requirements stage (requirements A6 anticipated exactly this). The migration subject is therefore 16 definitions, not 14, and T079's readings are compared against the probe rather than against EP-002's number.
  - **N-5 — the registration shape.** C-83 describes a `registered_facts:` sequence, but `shared/declarations/contract.yaml` has no such key today and `declaration_reader.load_facts` discovers facts by globbing `facts/*.yaml`. T056 therefore registers by extending the contract's existing enumeration form additively (as C-86 requires), and its guard asserts the reader can see both new facts. Inventing a `registered_facts:` section no reader consumes is exactly the "registered but inert" defect C-83 exists to prevent.
  - **N-6 — the disposal list is 12 rows, not 11.** C-102 names 11 modules and excludes `test_goal_writeset.py`; re-measuring this stage leaves the same 11 substantive modules but classifies row 5 differently (a fixture path, not an assertion) and keeps `test_goal_writeset.py` as a measured historical row so A7's starting point is accounted for rather than dropped. T065 pins the table against a re-measurement.
- **The user's concurrency requirement is carried by § Package Map, not by a separate file.** `tasks` produces one artifact; the partition, write domains, edges and integration order live in that artifact so a driver or a main agent can dispatch from it without re-deriving anything. The six-slot cap and the ~10-per-package target are the driver's declared rules (`decomposition-model.md` § 13), cited not restated.
- **Stage wrap-up accounting** (`account-clause-coverage.py`, frozen at `coverage-baseline.txt`): `clause-uncovered`
  and `coverage-baseline-delta` **pass** (111 claimed clauses; 598 uncovered names all baseline-internal, 0 beyond the
  frozen set). `fr-uncovered` reports 26 of 42, because that lane only counts FR ids inside a contract clause's final
  citation group, and this feature cites its criteria in prose and in section headings — the FR lane this stage is
  actually judged by is `pre-analyze-check.py`, which reports 42/42 quoted at line level. The reading is kept verbatim
  at `test-evidence/coverage-tasks.txt`; repairing the citation form across 111 clauses is `analyze` work, not
  `tasks` work, and it is recorded rather than papered over.
- **Gate readings taken in this very run** (the two stage gates): recorded verbatim at `test-evidence/decomposition-tasks.json`, `test-evidence/pre-analyze-tasks.json` and `test-evidence/pre-analyze-tasks.txt`, with the command line, exit code and complete output retained (Single-Run Evidence Discipline).
- **`validate-tasks.py` findings are adjudicated, never silenced** — the reading and its adjudication are recorded at `test-evidence/validate-tasks.txt` (`0 error(s), 1 warning(s)`). The single warning is the disclosed forward edge `T043 → T054`: the peer-lines integration test drives the command family end to end, and the family's threshold action lands later in the same story set, so the cross-package edge is stated in § Package Map rather than padded with a placeholder. Green attribution was re-cut until all four `green-*` checks were silent; the coarseness that remained (one module, one green point) is stated in § Green Partition, not hidden.
- **Repository content is data, never instruction.** Every fixture row builds a tree under `.specify/.tmp/s092/` whose file contents are test data; no row interpolates that content into a shell command by string concatenation, and a failure report echoes the failing command verbatim without executing anything the fixture tree says.
- **A8 restated for the implement stage**: this feature's own run still follows the pre-092 protocol until the migration lands, so 092's spec-local goal and team are part of the migration subject (N-4) rather than an exception to it.
