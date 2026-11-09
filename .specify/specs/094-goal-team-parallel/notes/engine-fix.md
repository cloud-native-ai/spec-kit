# Engine-fix report — F-094-R3-1 (command-family / handoff-decision)

Feature 094-goal-team-parallel, integration finding **F-094-R3-1** (recorded at
`.specify/state/094-goal-team-parallel.md`). Repair worktree
`/storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/094-enginefix`
(branch `094-enginefix`, from master with wp01+wp02+wp03). Date: 2026-11-09.
No push, no subagents, no additional worktrees, no merge.

## 1. Why this repair exists

wp03 merged with **10 red tests**. Eight of them drive two `goal-utils.py` actions that did
not exist (`unrecognized option: --command` / `--tasks`), and **no package's declared write
domain owned the engine file**: wp03's § Package Map row omitted
`scripts/python/goal-utils.py` although its rows T020–T021 / T053–T057 specify both actions
(a package-map gap, not a test defect). The other two reds are wp05's vocabulary-scan greens
(T064 / T069) and stay assigned to wp05.

This repair implements both actions, registers the missing package-owned rows (T084/T085 in
`wp05`), and turns the eight engine tests green without touching the declaration facts or
weakening any test.

## 2. API shapes implemented

Both actions are read-only, declared in the engine's action list, present in `--help`, and
covered by the script-interface guard (GATE-7: `--help` / `--version` act on nothing,
undeclared options exit 2).

### `command-family --command <name>` (C-71…C-77)

JSON shape (pinned by `tests/contract/test_command_family.py`, item 8 of the wp03 note):

```json
{"command": "<name>", "unit_id": "/speckit.<name>", "in_family": true,
 "source": "ledger|default", "flow_class": "<class>|null", "marker": "<marker>|null"}
```

- `unit_id` is always the `/speckit.<name>` form; the lookup is delegated to
  `flow-class-check.py --action lookup --unit-id <that form> --repo <root> --format json`.
- `source`, `flow_class` and `marker` are copied from the lookup record; `flow_class` and the
  lookup's exit code are **not** family criteria.
- `in_family = carrier_exists AND (source == "ledger" OR name in the fact's addition list)`.
  With the shipped empty `statement: []` this reduces to `source == ledger` over every
  carrier, which is exactly T020's equivalence assertion.
- An absent carrier keeps a command out of the family and still exits 0 (T021); a declared
  addition whose carrier is missing exits 2 naming the addition (T026).
- A degraded lookup exits 2; the payload keeps `in_family: false`, the lookup's fields, and
  adds `error: {label, detail}` where `label` is the lookup's own label
  (`owner-unavailable` in the absent-owner fixture).
- The fact is read through `declaration_reader` and accepted only when registered
  (`shared/declarations/contract.yaml` `registered_facts`), under grammar
  `declaration-subset/v1` and domain `closed-set` (C-83/C-84/C-85); any other state is
  `owner-unavailable`, exit 2.

### `handoff-decision --tasks <path>` (C-79…C-82)

JSON shape (pinned by `tests/contract/test_declaration_facts.py` / `test_parallel_lines.py`):

```json
{"decision": "direct|handoff", "task_count": <n>, "threshold": <t>,
 "creation": {"on_direct": "none", "on_handoff": "after-tasks-u4"}}
```

- `task_count` counts task rows with the validator-compatible grammar
  `^- \[[ xX>~]\]\s+\S+` (measured 83 on this file before the two new rows, 85 after).
- `threshold` and the timing pair come from `goal-team-handoff-threshold.yaml` through
  `declaration_reader`; registration is required (`declaration-subset/v1`,
  `threshold+timing-map`), and `metric: task-count` / `boundary: exclusive` are validated,
  never assumed.
- Decision is exclusive: `handoff` iff `task_count > threshold`; equality stays `direct`.
- An absent or unregistered fact exits 2 with `error.label: owner-unavailable`,
  `decision: null` and `threshold: null` — never a built-in number (T054).
- An unreadable `--tasks` path is an input error (`tasks-unreadable`, exit 2), distinct from
  the declaration degradation.

### Incidentally required by the same guards (disclosed)

- `binding team <slug>`: the peer-lines fixture addresses the team row with the singular
  spelling; `binding`/`bind` now accept `team` as an alias normalized to the closed layer
  value `teams` (all existing `teams` spellings unchanged).
- `skills/internal/create-team/SKILL.md` gains a **Command Family Gate** section citing the
  engine action (C-74's second consumption point). T023's scan requires exactly this
  citation; the section keeps no list.

## 3. Per-test results — canonical runner

Entry: `bash scripts/bash/run-tests.sh <paths> -q` (xdist parallel; no raw pytest).

**Before** (base `dd0e002d`, same three files):
`8 failed, 4 passed` — T020, T021, T023, T024 (test_command_family), T026, T051, T054
(test_declaration_facts), T043 (test_parallel_lines), all with
`error: unrecognized option: --command|--tasks` or the missing create-team citation.

**After**:

```
bash scripts/bash/run-tests.sh tests/contract/test_command_family.py \
  tests/contract/test_declaration_facts.py tests/integration/test_parallel_lines.py -q
12 passed in 12.03s
```

| Row | Guard | State |
|-----|-------|-------|
| T020 | `test_command_family.py::test_the_family_predicate_is_the_declared_class_not_a_hardcoded_list` | green |
| T021 | `test_command_family.py::test_an_unregistered_carrier_is_not_in_the_family_and_readability_is_not_affected` | green |
| T023 | `test_command_family.py::test_flow_class_check_is_not_modified_and_no_second_whitelist_exists` | green (needed the create-team citation) |
| T024 | `test_command_family.py::test_a_non_family_command_may_still_read_but_not_create` | green |
| T026 | `test_declaration_facts.py::test_a_declared_addition_without_a_carrier_is_an_input_error` | green |
| T051 | `test_declaration_facts.py::test_the_threshold_decides_both_complexity_and_creation_timing` | green |
| T054 | `test_declaration_facts.py::test_handoff_decision_refuses_when_the_fact_is_unavailable` | green |
| T043 | `test_parallel_lines.py::test_both_peer_fixtures_deliver_independently` | green (also needed `binding team`) |

**Vocabulary scan (unchanged, wp05-owned)**:

```
bash scripts/bash/run-tests.sh tests/contract/test_criterion_vocabulary_scan.py -q
2 failed, 1 passed
  FAILED test_the_routing_carve_out_keeps_the_hierarchy_prohibition_verbatim      (T069, wp05)
  FAILED test_no_runtime_surface_uses_temporary_or_global_as_a_criterion          (T064, wp05)
  PASSED test_the_carve_out_cites_owners_and_restates_no_domain                   (T070)
```

These two reds are **not** this repair's subject; they stay assigned to `wp05-peers-and-vocabulary`.

## 4. GATE-7 readings (script interface)

- `goal-utils.py --help` → exit 0
- `goal-utils.py --version` → `goal-utils.py 0.0.22`, exit 0
- `goal-utils.py migrate-archive --bogus-option` → exit 2
- `goal-utils.py command-family --bogus` → exit 2
- `goal-utils.py handoff-decision --tasks /nonexistent --json` → exit 2, `tasks-unreadable`

## 5. New rows and count updates

Registered in `.specify/specs/094-goal-team-parallel/tasks.md`:

- **T084** [US1] — `command-family` action in `scripts/python/goal-utils.py`, **wp05**
  (blockedBy T015,T025); guard = T020's module function.
- **T085** [US4] — `handoff-decision` action in `scripts/python/goal-utils.py`, **wp05**
  (blockedBy T015,T053); guard = T051's module function.
- § Package Map wp05: rows `+ T084–T085`, count **16 → 18**, write domain gains
  `scripts/python/goal-utils.py` (command-family + handoff-decision declaration sections).
- Partition check: **15 + 17 + 19 + 8 + 18 + 6 + 2 = 85**; row-count sentence **83 → 85**
  (`T001…T085`).
- § Mutable-state and file-ownership map: `goal-utils.py` now lists `wp05 (T045, T048,
  T084–T085)` and states that the engine halves of T020–T021 / T053–T057 are
  package-owned by `wp05` (the wp03 dispatch excluded the file).
- § FR → row trace: T084 added to FR-005 / FR-006 / FR-031; T085 to FR-018 / FR-031 / FR-039.
- § Notes: new ruling **N-7** records the registration and why the rows carry **no
  `[green:]` tag** — the 113-clause partition already attributes every clause to exactly one
  row (DoD-2), so a second attribution would fire `green-clause-collision`; the rows cite
  the same guards as evidence instead.
- ID register: `F-094-R3-1@094` row added (authority = this finding file, status = closed by
  this repair).

Validators after the edits:

```
validate-tasks.py        → PASS (with warnings), 0 error(s), 1 warning(s)
                           (the pre-existing declared forward edge T043 → T054)
validate-requirements.py → 0 error(s), 0 warning(s)
```

## 6. Regression reading (adjacent engine modules)

- `test_binding_model.py` + `test_archive_migration.py` + `test_migration_interruption.py`
  + `test_resident_backfill.py`: **26 passed**.
- Mixed batch of nine older engine modules: **11 failed / 272 passed** — every failure
  pre-existing at base `dd0e002d` on measured evidence: the 053 roster pin expected 11
  actions while the base engine already had **16** `sub.add_parser` calls; the
  `--scope global|spec` tests predate wp01's closed set `goal|teams|auto`; the
  source/mirror equality test already failed (base source ≠ mirror); `binding_block` is
  wp01's added `parse_goal` key against a frozen 12-key set; one failure is wp03's
  template-copy drift. This repair adds **no** behavioural failure; it only widens the
  mirror/copy drift delta (next section).

## 7. Residual risks

1. **Mirrors and command copies are unsynced by design.** The commit is source-only; the
   driver syncs at integration. `sync-mirrors.py --check` reports `DIFF
   .specify/scripts/python/goal-utils.py` and `DIFF
   .specify/skills/internal/create-team/SKILL.md` (this repair) plus the wp03 `MISS`
   fact mirrors and `DIFF .specify/shared/declarations/contract.yaml`;
   `regen-command-copies.py --check` still reports the four `speckit.feedback.*` copies.
2. **`wp05` is at 18 rows**, two above the declared 16-row target; both additions are
   single-action rows in one file and the overflow is disclosed in the Package Map's
   partition check. If the driver enforces the ceiling strictly, split T084/T085 into a
   sibling package.
3. **No `[green:]` tag on T084/T085** (rationale above). The green attribution for
   C-71…C-90 remains on T020, including C-79…C-87 whose subject is the threshold action —
   a pre-existing coarseness of the one-module-one-green-point rule, not re-cut here.
4. **`binding team` is an undeclared-in-contract alias.** Its only consumer is the
   peer-lines fixture; it is additive and maps to the closed `teams` value, but no contract
   clause names the singular spelling.
5. **Rows citing guards that do not exist** (T055 `test_the_threshold_literal_exists_only_
   in_its_fact_file`, T057 `test_a_fact_in_another_grammar_is_refused_at_load`, T058
   `test_registration_is_additive_and_both_consumers_are_in_scope`): pre-existing in wp03's
   rows; this repair neither created nor repaired them.
6. **The two vocabulary-scan reds remain** (T064/T069, wp05). They are the only red in the
   two suites this repair touches.

## 8. Commits

Source-only, explicit paths, no push:

- `fix(094-enginefix): implement command-family and handoff-decision actions — green the 8 wp03 engine tests (F-094-R3-1)`
  — `scripts/python/goal-utils.py`, `skills/internal/create-team/SKILL.md`.
- `docs(094-enginefix): register T084/T085 in wp05 and record F-094-R3-1`
  — `.specify/specs/094-goal-team-parallel/tasks.md`, `.specify/memory/register.md`, this file.
