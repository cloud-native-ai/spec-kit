# Implement report — wp03-command-family (094-goal-team-parallel)

Package: `wp03-command-family`, rows T016–T027, T043, T049–T054 (19 rows) plus T056,
which `tasks.md` § "Mutable-state and file-ownership map" assigns to `wp03` by domain
(`shared/declarations/contract.yaml` — "wp03 only").
Tree: `/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/094-wp03`
(branch `094-wp03`, base `eee176c6` — master with wp01 landed; wp02 running separately).
Date: 2026-11-09.

Write domain used — exactly the eight paths of `tasks.md` § Package Map (wp03):
`shared/declarations/facts/goal-team-command-family.yaml`,
`shared/declarations/facts/goal-team-handoff-threshold.yaml`,
`shared/declarations/contract.yaml`, `templates/commands/feedback.md`,
`tests/contract/test_command_family.py`, `tests/contract/test_declaration_facts.py`,
`tests/contract/test_criterion_vocabulary_scan.py`,
`tests/integration/test_parallel_lines.py` — plus this package's `notes/` and
`test-evidence/` outputs. **`scripts/python/goal-utils.py`, the driver skill
references and every other package's paths were not touched** (dispatch ruling).
No push, no subagents, no additional worktrees, no merge, no `--force`.

## Per-row closure

| Row | Status | Evidence |
|-----|--------|----------|
| T016 | **blocked** — `tests/contract/test_command_run_goal_team.py` is outside the fork's eight-path domain and is unowned by any package in § Package Map; T019's engine edit is also out of domain. Not authored. | — |
| T017 | **blocked** — same module, depends on T016. Not authored. | — |
| T018 | **blocked** — red-first capture of T016/T017; nothing authored to capture. | — |
| T019 | **blocked** — engine `create` binding write lives in `goal-utils.py`, excluded by the dispatch. Not edited. | — |
| T020 | **blocked (guard authored red)** — `command-family` action is an engine row outside the domain. This module's green point (`[green:]` C-71…C-90) was authored red-first first. | `test-evidence/wp03-T020-red.txt`, `wp03-T020T021T023T024-red.txt` |
| T021 | **blocked (guard authored red)** — engine refusals outside the domain; the guard pins absent carrier / `source: default` / `owner-unavailable`. | `test-evidence/wp03-T021-red.txt` |
| T022 | **artifact closed, guard pending** — `templates/commands/feedback.md` declares the creation moment and "no spec directory"; the named guard module `tests/contract/test_feedback_command_template.py` is outside the domain. | `test-evidence/wp03-T022-template.txt`, `wp03-T022-collateral.txt` |
| T023 | **blocked (guard authored red)** — engine routing and the `create-team` citation are out of domain; the byte pin of `flow-class-check.py` and the no-second-whitelist scan are in place and already pass. | `test-evidence/wp03-T023-red.txt` |
| T024 | **blocked (guard authored red)** — readability assertions pass; the family verdict needs the absent engine action. | `test-evidence/wp03-T024-red.txt` |
| T025 | **closed** — fact authored; guard green. | `test-evidence/wp03-T025-green.txt` |
| T026 | **blocked (guard authored red)** — refusal at read time belongs to the absent engine action. | `test-evidence/wp03-T026-red.txt` |
| T027 | **closed** — both facts parse under `parse_subset`, carry the five mandatory keys, and are discovered by the reader. | `test-evidence/wp03-T027-green.txt` |
| T043 | **blocked (guard authored red)** — integration module authored; red exactly at the missing `handoff-decision` (T054). Peer B (goal+team, no spec dir) was smoke-verified green by hand before the peer-A gate. | `test-evidence/wp03-T043-red.txt` |
| T049 | **delegated by domain** — `tests/contract/test_handoff_contract.py` is `wp04-handoff`'s declared domain; the row executes with wp04. | § Package Map (wp04) |
| T050 | **delegated by domain** — `tests/contract/test_handoff_territory.py` is `wp04`'s domain. | § Package Map (wp04) |
| T051 | **blocked (guard authored red)** — threshold read from the fact (never a literal); equality→`direct`, above→`handoff`; needs `handoff-decision`. | `test-evidence/wp03-T051-red.txt` |
| T052 | **partial** — T051's red capture recorded here; T049/T050 were not authored by this fork and the shared `notes/red-first-evidence.md` was left untouched (cross-package file, per row T044/T052/T066 ownership). | `test-evidence/wp03-T051-red.txt` |
| T053 | **closed** — threshold fact authored (N-1 value, `exclusive`, timing pair); guard green. | `test-evidence/wp03-T053-green.txt` |
| T054 | **blocked (guard authored red)** — engine `handoff-decision` outside the domain; the guard pins exit 2 / `owner-unavailable` / no fallback number. | `test-evidence/wp03-T054-red.txt` |
| **T056** | **closed** (domain-assigned to wp03) — additive `registered_facts:` registration; guard green. | `test-evidence/wp03-T056-green.txt` |

Rows whose modules this package owns but whose guard functions are other packages' rows
(the Package Map assigns the module, the row list assigns the guard):

| Row | Module function authored | State |
|-----|--------------------------|-------|
| T064 (wp05) | `test_criterion_vocabulary_scan.py::test_no_runtime_surface_uses_temporary_or_global_as_a_criterion` | red-first: baseline 29 hits on 8 surfaces (measured 2026-11-09) |
| T069 (wp05) | `...::test_the_routing_carve_out_keeps_the_hierarchy_prohibition_verbatim` | red — the verbatim C-91 prohibition and the criterion-free carve-out are not in place yet |
| T070 (wp05) | `...::test_the_carve_out_cites_owners_and_restates_no_domain` | green today; stays green iff the wp05 rewrite keeps citing both owners and no value-domain triple |

## Test readings

TEST ENTRY: every run below went through `bash scripts/bash/run-tests.sh <paths> -q`
(pytest-xdist defaults `-n auto --dist load`); no raw pytest invocation was used.

- **New modules, one consolidated run** — 10 failed, 5 passed, exit 1
  (`test-evidence/wp03-new-modules-full.txt`). The 10 red are exactly the
  engine/foreign-surface rows above (T020, T021, T023, T024, T026, T043, T051, T054,
  T064, T069); the 5 green are T025, T027, T053, T056, T070.
- **Green readings per row**: T025 / T027 / T053 / T056 / T070 — 1 passed each
  (`wp03-T025-green.txt`, `wp03-T027-green.txt`, `wp03-T053-green.txt`,
  `wp03-T056-green.txt`, `wp03-T070-green.txt`).
- **Red readings per row**: T020, T021, T023, T024, T026, T051, T054 — 1 failed each
  (`wp03-T<row>-red.txt`). Their failure is the same missing engine action
  (`unrecognized option: --command` / `--tasks`) or the missing wp05 rewrite.
- **Declaration-side red**: `wp03-T025T027T053T056-green-T051T054T026-red.txt`
  (4 passed, 3 failed) — the three engine-dependent guards red, the four
  declaration-shape guards green.
- **T064's measured hit set** (recorded in `wp03-T064-red.txt`): 29 hits, all in
  `shared/definitions/sdd-routing-definitions.md`, `skills/internal/create-team/
  references/{create-mode,conceptual-model}.md`, `skills/external/sdd-loop-driver/
  SKILL.md` + `references/{checkpoint-protocol,decomposition-model}.md`,
  `templates/commands/{goal,team}.md`, `scripts/python/sdd-route.py`. All but
  `create-mode.md` are wp05/wp04 row-owned surfaces; `create-mode.md` is inside wp04's
  directory but no row declares its rewrite — see residual risks.
- **T043's red point** (recorded): exit 2 `unrecognized option: --tasks` — the missing
  `handoff-decision` (T054), i.e. the blockedBy edge behaves as declared.
- **Collateral (not a gate)**: `test_feedback_command_template.py` +
  `test_harness_triple_structure.py` + T070 guard — **75 passed**
  (`wp03-T022-collateral.txt`). The registration is additive; the triple-structure
  fixtures copy the shipped `contract.yaml` and stay green.
- **Pre-change baseline of the same collateral**: 2 failed / 89 passed — both failures
  pre-existing and caused by wp01's `goal-utils.py` mirror drift
  (`sync-mirrors.py --check` exit 2), not by this package.
- **Generator drift (driver-owned, disclosed)**: `sync-mirrors.py --check` exit 2 —
  wp01's engine drift plus this package's `MISS` two fact mirrors and `DIFF
  .specify/shared/declarations/contract.yaml`; `regen-command-copies.py --check` exit 1
  — the four per-tool `speckit.feedback.*` copies. Reading:
  `test-evidence/wp03-mirror-and-copy-drift.txt`. Following wp01's precedent these
  generated projections are left to the driver's integration step (`sync-mirrors.py
  --write` / `regen-command-copies.py`), not hand-edited from a package fork.

## Artifacts delivered

- `shared/declarations/facts/goal-team-command-family.yaml` — `kind: closed-set`,
  `statement: []` (class predicate only; the empty addition list is legal per C-76),
  `consumers` naming the two C-74 consumption points, `former_carriers: []`.
- `shared/declarations/facts/goal-team-handoff-threshold.yaml` — `kind: threshold`,
  `statement` with `metric: task-count`, `threshold: 10` (ruling N-1), `boundary:
  exclusive`, `on_direct: none`, `on_handoff: after-tasks-u4`.
- `shared/declarations/contract.yaml` — additive `registered_facts:` sequence, one row
  per fact, each with `subset_id: declaration-subset/v1`, the registered `value_domain`
  (`closed-set` / `threshold+timing-map`) and its `statement_keys`; no existing key
  renamed, reordered or removed (N-5's reader-visible registration).
- `templates/commands/feedback.md` — new `## Goal/Team (command family)` section: first
  evidence command, creation moment (after the routing judgement, before the chosen
  path executes, through the engine's `create`), and "no spec directory required" with
  the two archive-layer landing points.
- `tests/contract/test_declaration_facts.py` — T025/T026/T027/T051/T053/T054/T056
  guards; threshold read from the fact (no literal), fixtures under
  `.specify/.tmp/s094/`.
- `tests/contract/test_command_family.py` — T020/T021/T023/T024 guards; pins the
  `command-family` JSON shape (`command`, `unit_id`, `in_family`, `source`,
  `flow_class`, `marker`), the `/speckit.<name>` unit-id form, the
  `in_family == (source == ledger)` equivalence over all 29 carriers, a byte pin of
  `flow-class-check.py` (`c336bf2…f401`), and the read-path-is-not-gated scan.
- `tests/contract/test_criterion_vocabulary_scan.py` — T064/T069/T070 guards; a
  criterion-only scan (classification phrases, not words), with the owner's historical
  record and the temp-directory exemption.
- `tests/integration/test_parallel_lines.py` — T043: two peer fixtures under
  `.specify/.tmp/s094/`, neither requiring the other line; threshold read from the
  fact.

## Commits

Committed explicitly by path (never `git add -A`); no push.

- `eb515227` — `feat(094-wp03): declaration facts, contract registration and feedback declaration (T022, T025, T053, T056)`
- `668bf584` — `feat(094-wp03): command-family, declaration, vocabulary and parallel-line tests (T020–T024, T026–T027, T043, T051, T054, T064, T069–T070)`
- the close-out commit that carries this note and the `wp03-*` evidence files — `feat(094-wp03): close-out readings for wp03` (its hash is reported in the fork's final message; a commit cannot name itself).

## Residual risks and disclosed boundaries

1. **Nine engine-dependent rows cannot close inside this fork.** `goal-utils.py` was
   excluded from the package's write domain by the dispatch. Rows T019, T020, T021,
   T054 (and the guard halves of T023, T024, T026, T043, T051) need those engine
   sections. The guard tests are authored and red-first; the implementer lands the
   engine edits against them.
2. **T016/T017/T018's module is unowned.** `tests/contract/test_command_run_goal_team.py`
   appears in no package's § Package Map domain column. It is a tasks-file gap: the
   driver must assign the module (and T019's engine edit) or re-scope the rows.
3. **T049/T050 row-vs-domain mismatch.** The rows are listed under wp03, but their
   modules (`test_handoff_contract.py`, `test_handoff_territory.py`) are wp04's declared
   domain. This fork authored neither module; wp04 must produce them (its own rows
   T059–T062 guard there too).
4. **T022's guard module is unowned by any package.** `test_feedback_command_template.py`
   is outside the eight-path domain, so the row's artifact is delivered but the named
   guard function is not. The existing template tests stay green (6 passed).
5. **T064's green depends on a surface no row owns.** The scan flags
   `skills/internal/create-team/references/create-mode.md` (5 classification hits) —
   inside wp04's directory, but no row declares its rewrite. wp05's T067–T070 cover the
   other 24 hits. If `create-mode.md` is not rewritten by wp04/wp05, T064 stays red; the
   driver should assign it rather than weaken the scan.
6. **The green partition's `[green:]` attribution for C-71…C-90 sits on T020.** That
   module is authored here red-first; the clause tags turn green only with the engine
   action (C-71…C-87) and the wp05 owner rewrites (C-88…C-90).
7. **Mirror and command-copy projection is pending the driver's integration step**
   (`test-evidence/wp03-mirror-and-copy-drift.txt`). The `sync-mirrors.py --write` /
   `regen-command-copies.py` runs are the driver's, following wp01's precedent; no
   mirror was hand-edited from this fork.
8. **The `command-family` / `handoff-decision` JSON shape is pinned by the tests, not
   by a contract clause.** No clause fixes the keys; this package chose
   `{command, unit_id, in_family, source, flow_class, marker}` and
   `{decision, task_count, threshold, creation: {on_direct, on_handoff}}` and says so
   in the module docstrings. If a later design fixes a different shape, change the two
   tests in the same edit — the contracts leave it open.
9. **The threshold literal stays a one-file edit.** No test or report artifact outside
   the fact file pins the number: T051/T043 read it through the declaration reader.
