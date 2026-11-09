# Contract — Owner Rewrites, Driver Protocol, 085 Test Disposal and Evidence

This file carries the changes that are prose-and-protocol rather than engine behaviour, and the test
obligations that make the other four contracts decidable. Every clause here names the file it changes.

## 1. Routing carve-out (FR-027)

- **C-91**: `shared/definitions/sdd-routing-definitions.md` § Hierarchy MUST replace the paragraph currently
  titled `Temporary run-scoped scopes（追加 carve-out）` with a carve-out that: (a) permits a run to create
  definitions with `owner: sdd-run` or `owner: command-run` landing in the archive layers; (b) keeps verbatim the
  prohibition "一次 SDD 运行 MUST NOT 创建/重绑/改范围/终止共享档案中的既有定义"; (c) contains no occurrence of
  `Temporary` or `临时` as a criterion name.

(FR-027)
- **C-92**: The carve-out MUST cite `shared/definitions/goal-definitions.md` and
  `skills/internal/create-team/references/conceptual-model.md` for the concepts and MUST NOT restate any value
  domain (no `owner` values, no layer names beyond a path pointer).

(FR-024, FR-027)
## 2. Driver protocol and state spine (FR-028)

- **C-93**: `skills/external/sdd-loop-driver/SKILL.md` § Temporary Goal/Team MUST be retitled and rewritten to the
  binding model: when a goal/team is created, where it lands, under which binding, and that the creation moment is
  read from `goal-team-handoff-threshold.yaml` rather than restated.

(FR-028)
- **C-94**: `skills/external/sdd-loop-driver/references/checkpoint-protocol.md` MUST replace its goal/team
  sentences (goal content changes only through the engine; `--scope spec` disappears) with the new model, and MUST
  keep the four-part checkpoint and the direction audit unchanged.

(FR-028)
- **C-95**: The state-spine keys `temp_goal_slug` / `temp_team_slug` / `temp_scope_spec_dir` MUST be replaced by
  `goal_slug` / `team_slug` / `origin_spec_dir` in every driver instruction, and the three old keys MUST remain
  readable only through the engine alias (`binding-and-lifecycle.md` C-21…C-24). The stage chain and the
  completion sentinels MUST NOT change.

(FR-028)
- **C-96**: The driver MUST NOT gain a new stage, a new sentinel, a new watcher rule or a new exit code from this
  feature; the only driver-side change is the vocabulary of the goal/team sentences.

(FR-028)
## 3. Command templates and directory map (FR-029, FR-030)

- **C-97**: `templates/commands/goal.md` MUST expose the `migrate-archive` mode, drop `spec` from its scope hint,
  and cite the scope value set by pointer to its owner.

(FR-030)
- **C-98**: `templates/commands/team.md` MUST drop `spec` from its scope hint and cite the scope value set by
  pointer; it MUST NOT gain a migration mode (team migration runs inside the goal entry).

(FR-030)
- **C-99**: `templates/commands/feedback.md` MUST declare its goal/team creation moment and that it needs no spec
  directory (C-73).

(FR-040)
- **C-100**: `shared/definitions/framework-map.md` MUST update the Goals, Teams and spec-archive rows so that
  goal/team land only in `.specify/goal/` and `.specify/teams/`, the archive row names
  `.specify/archive/goal-team/`, and the `.specify/specs/` row no longer implies goal/team subdirectories.

(FR-029)
- **C-101**: `skills/internal/{create-team,manage-goal,run-team,improve-team}` MUST follow the new paths and model
  in their procedures; each MUST cite the mode/action owners rather than restate arguments.

(FR-029, FR-030)
## 4. 085 test disposal (FR-041, SC-010)

- **C-102**: The disposal list MUST be measured in this stage, not inherited: 11 modules currently carry a
  spec-local or scope assertion — `tests/contract/test_scope_resolution.py`,
  `test_temp_goal_contract.py`, `test_temp_team_schema.py`, `test_goal_targets_check.py`,
  `test_goal_targets_engine.py`, `test_checkpoint_protocol.py`, `test_expression_compatibility.py`,
  `test_sdd_loop_driver_wp_model.py`, `tests/unit/test_goal_scope_engine.py`, `tests/unit/test_goal_utils.py`, and
  `tests/integration/test_checkpoint_rollback.py`. `tests/contract/test_goal_writeset.py` carries none and is
  therefore out of the disposal list (A7 named it as a starting point only).

(FR-041)
- **C-103**: Each row MUST be disposed in exactly one of three ways, each recorded with a one-line reason:
  `rewrite` (the asserted fact still holds, only its location/name changed) / `remove` (the asserted fact no longer
  exists — e.g. "`--scope spec` writes into the spec directory") / `historical` (kept as a dated record and marked).
  A `remove` without a named fact that disappeared is refused.

(FR-041)
- **C-104**: After disposal, `pytest -m contract` MUST be green with respect to the serial baseline
  (`test-evidence/plan-baseline-names.txt`): zero NEW failing ids. An absolute "all green" claim is not a criterion,
  because 46 ids already fail on this tree for unrelated reasons.

(FR-041, FR-033)
- **C-105**: The disposal table MUST be written into `feature-ref.md` § 085 Disposal and mirrored into
  `verification.md` at closure; a row present in one and absent in the other is a defect.

(FR-041)
## 5. Structural and conceptual guards (FR-013, FR-022, SC-002, SC-008)

- **C-106**: A contract test MUST assert that no code path writes `.specify/specs/<spec>/goal/**` or
  `<spec>/team/**`: it enumerates the engine's writing actions, the `create-team` persistence step and the driver
  instructions, and asserts the old path prefix appears in none of them as a write target.

(FR-013)
- **C-107**: A contract test MUST scan the runtime surfaces (`shared/`, `skills/`, `scripts/`, `templates/`,
  `src/`) for `临时` / `temporary` / `全局` used as a **criterion** for goal/team classification, and MUST pass only
  when the hit set is empty apart from the owner's own historical-record and the temp-directory-discipline
  exemption . The scan is programmatic, never a reading.

(FR-022, FR-037)
- **C-108**: The mutation obligation MUST be encoded: C-106's test MUST fail when one writing surface is reverted to
  the old path (synthetic mutation in the test, not a tree edit), and C-107's test MUST fail when one old phrase is
  re-injected.

(FR-013, FR-022, FR-033, FR-032)
## 6. Evidence and closure (FR-033, SC-001…SC-011)

- **C-109**: Every success criterion MUST have one test module named in the map below, and each module MUST turn red
  when its behaviour is removed (a test that only greps for wording does not count as evidence).

(FR-033)
- **C-110**: `verification.md` MUST carry one `SC-NNN_status=` line per criterion plus the evidence pointer, because
  `closure-acceptance-check.py` reads that form; a Markdown table alone reads `unknown`.

(FR-033)
- **C-111**: Every dated reading (baseline, migration dry run, migration apply, migration interruption drill,
  mutation runs) MUST be stored one file per reading under `<spec-dir>/test-evidence/` and MUST NOT be rewritten by a
  later run.

(FR-033)
### SC → red-first module map

| SC | Red-first module | What turns it red |
|----|------------------|-------------------|
| SC-001 | `tests/contract/test_command_run_goal_team.py` | a write landing under `.specify/specs/**` |
| SC-002 | `tests/contract/test_no_spec_local_writes.py` | one writing surface reverted to the old path |
| SC-003 | `tests/integration/test_archive_migration_real_data.py` | deleting a source file, or a missing unified definition |
| SC-004 | `tests/contract/test_archive_migration.py` | a second-run write, or an overwrite on conflict |
| SC-005 | `tests/integration/test_parallel_lines.py` | a "requires the other line" precondition |
| SC-006 | `tests/contract/test_handoff_contract.py` | an unresolvable or mismatched three-way key; a deleted declaration |
| SC-007 | `tests/contract/test_handoff_territory.py` | a crew write that is allowed onto a spec artifact |
| SC-008 | `tests/contract/test_criterion_vocabulary_scan.py` | one re-injected `临时` / `temporary` criterion |
| SC-009 | `tests/contract/test_binding_model.py` | ownership inferred from a directory prefix |
| SC-010 | `tests/contract/test_085_disposal_table.py` | an undisposed row in the measured list |
| SC-011 | `tests/contract/test_migration_interruption.py` | a second call that re-moves the tree or silently succeeds |

## Requirement coverage

FR-013, FR-022, FR-028, FR-029, FR-030, FR-032, FR-033, FR-037, FR-041; SC-001…SC-011.
