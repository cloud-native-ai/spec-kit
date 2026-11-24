# Red-first evidence — implement (104-agents-run)

Each entry: the command (unique entry `bash scripts/bash/run-tests.sh`), the decisive
real output, and the exit code captured directly (no pipe). Entries append in run order.

## T002 — `tests/contract/test_agents_run_command_contract.py` (red)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py -q
# test runner: python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_agents_run_command_contract.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
bringing up nodes...

..FFFFFFF.                                                               [100%]
FAILED tests/contract/test_agents_run_command_contract.py::test_c01_template_declares_the_argument_grammar
FAILED tests/contract/test_agents_run_command_contract.py::test_c07_skill_owns_the_missing_task_stop
FAILED tests/contract/test_agents_run_command_contract.py::test_c06_the_three_syntax_faces_agree_verbatim
FAILED tests/contract/test_agents_run_command_contract.py::test_c10_three_error_paths_stop_with_zero_dispatches
FAILED tests/contract/test_agents_run_command_contract.py::test_c03_explicit_verb_priority_team_redirect_and_ambiguity
FAILED tests/contract/test_agents_run_command_contract.py::test_c04_explicit_run_without_agent_name_stops_at_the_command
FAILED tests/contract/test_agents_run_command_contract.py::test_c08_routing_sample_set_proxies
7 failed, 3 passed in 6.59s
rc=1
```

Red for the right reason: no `argument-hint` (C-01), no explicit-verb / team-refusal /
ambiguity sentences (C-03), no `missing agent name` stop (C-04), the docs Syntax face is
unchanged (C-06), the skill input contract lacks `missing task` (C-07), one routing proxy
is unsatisfied (C-08), and the not-found path is not stated as a no-dispatch stop (C-10).
Already holding: C-02 (the three-row delegation table is pre-existing), C-05 (the skill's
no-argument sequence is pre-existing), C-09 (copies are in parity and already carry
`run <agent-name> [task]`). One authoring defect was found and repaired on the test side
before this reading: the first draft counted the table header as a data row.

## T003 — `tests/contract/test_agents_run_skill_wiring.py` (red)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_skill_wiring.py -q
# test runner: python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_agents_run_skill_wiring.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
bringing up nodes...

.F.FFFFFFFFF                                                             [100%]
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c19_run_stays_a_single_unit_and_records_the_reading
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c13_four_injections_travel_by_pointer
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c12_downlink_names_the_seven_role_fields
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c17_multi_child_visibility_points_at_existing_carriers
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c11_presentation_discloses_the_role_relation
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c21_role_is_decided_only_by_the_edge
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c15_uplink_requires_the_five_return_elements
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c22_zero_second_mechanism_and_clause_class_honesty
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c16_child_label_reuses_the_dispatch_convention
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c18_sdd_probe_applicability_is_narrowed
10 failed, 2 passed in 6.23s
rc=1
```

Red for the right reason: the run mode carries no role-relation disclosure (C-11), no
seven-field downlink (C-12), only the fast-fail owner among the four injections (C-13),
no five-element uplink (C-15), no label convention (C-16), no visibility carriers (C-17),
no narrowed probe condition (C-18), no reading triple (C-19), no edge-only role statement
(C-21), and no zero-second-mechanism statement (C-22). Already holding: C-14 (the
role-transition identifier and its literal phrases pre-exist) and C-20 (the anti-nesting
red lines pre-exist). One authoring defect was found and repaired on the test side before
this reading: phrase assertions were defeated by line wrapping, so both modules now
normalise whitespace before matching.

## T009 — US1 turn-green reading (T004–T008 landed)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py tests/contract/test_agents_run_skill_wiring.py -q
# test runner: python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_agents_run_command_contract.py tests/contract/test_agents_run_skill_wiring.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
bringing up nodes...

......FFF...F.FFFF....                                                   [100%]
FAILED tests/contract/test_agents_run_command_contract.py::test_c06_the_three_syntax_faces_agree_verbatim
FAILED tests/contract/test_agents_run_command_contract.py::test_c09_per_tool_copies_are_generated_and_carry_the_run_form
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c16_child_label_reuses_the_dispatch_convention
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c17_multi_child_visibility_points_at_existing_carriers
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c18_sdd_probe_applicability_is_narrowed
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c19_run_stays_a_single_unit_and_records_the_reading
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c22_zero_second_mechanism_and_clause_class_honesty
7 failed, 15 passed in 6.61s
rc=1
```

Per-function reading (all 22 collected ids; `bash scripts/bash/run-tests.sh <two modules> --collect-only -q` → 22 ids):

| Module | Function | Result |
|---|---|---|
| command | test_c01_template_declares_the_argument_grammar | pass (first green) |
| command | test_c02_three_skill_rows_and_run_row_carries_the_explicit_form | pass |
| command | test_c03_explicit_verb_priority_team_redirect_and_ambiguity | pass (first green) |
| command | test_c04_explicit_run_without_agent_name_stops_at_the_command | pass (first green) |
| command | test_c05_no_argument_behaviour_is_unchanged | pass |
| command | test_c06_the_three_syntax_faces_agree_verbatim | **fail — allowed residual: docs Syntax face (T017)** |
| command | test_c07_skill_owns_the_missing_task_stop | pass (first green) |
| command | test_c08_routing_sample_set_proxies | pass (first green; C-08 claimed in T009) |
| command | test_c09_per_tool_copies_are_generated_and_carry_the_run_form | **fail — allowed residual: copies drift after the template edit (T027 regenerates)** |
| command | test_c10_three_error_paths_stop_with_zero_dispatches | pass (first green; C-10 claimed in T009) |
| skill | test_c11_presentation_discloses_the_role_relation | pass (first green) |
| skill | test_c12_downlink_names_the_seven_role_fields | pass (first green) |
| skill | test_c13_four_injections_travel_by_pointer | pass (first green) |
| skill | test_c14_role_transition_self_check_keeps_its_literals | pass |
| skill | test_c15_uplink_requires_the_five_return_elements | pass (first green) |
| skill | test_c16_child_label_reuses_the_dispatch_convention | **fail — allowed residual: US2 (T011)** |
| skill | test_c17_multi_child_visibility_points_at_existing_carriers | **fail — allowed residual: US2 (T011)** |
| skill | test_c18_sdd_probe_applicability_is_narrowed | **fail — allowed residual: US3 (T013)** |
| skill | test_c19_run_stays_a_single_unit_and_records_the_reading | **fail — allowed residual: US3 (T013)** |
| skill | test_c20_anti_nesting_red_lines_are_preserved | pass |
| skill | test_c21_role_is_decided_only_by_the_edge | pass (first green; statement landed in T006) |
| skill | test_c22_zero_second_mechanism_and_clause_class_honesty | **fail — allowed residual: US3 (T013)** |

No failure outside the allowed residual set (C-06, C-09, C-16…C-22) — any other failure
would be a defect. Both runs above went through the unique entry; rc captured directly.
One wording correction during T004: the template's ambiguity sentence said "request the
missing intent" while the contract requires "requests the missing intent"; the template was
corrected to the contract's wording (correction, not a decision).

## P1 guard reading (four named guards + the run-agent mirror param)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_run_skills_wiring.py tests/contract/test_team_command_routing.py tests/contract/test_role_transition_payload.py tests/contract/test_fast_fail_discipline.py -q
FAILED tests/contract/test_fast_fail_discipline.py::test_g9_total_equals_frozen_baseline
FAILED tests/contract/test_fast_fail_discipline.py::test_i10_channel_two_factory_presets_byte_equal
FAILED tests/contract/test_fast_fail_discipline.py::test_x22_cross_discipline_change_recorded
FAILED tests/contract/test_role_transition_payload.py::test_wired_surface_mirror_is_identical[skills/internal/run-agent/SKILL.md]
4 failed, 163 passed in 7.21s
rc=1
```

Classification against `baseline-failed.txt` (name-level):

- The three `test_fast_fail_discipline.py` failures are **in the baseline** (pre-existing; not this feature's).
- `test_role_transition_payload.py::test_wired_surface_mirror_is_identical[skills/internal/run-agent/SKILL.md]`
  is **new at this point of the line** — it asserts the source↔mirror pair is byte-identical, and
  the mirror is regenerated only in the Polish phase (T028; plan § Mirror Obligations defers
  regeneration until every source edit has landed). Same cause, second param:

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_mirror_parity_suite.py -k 'run-agent' -q
FAILED tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[skills/internal/run-agent/SKILL.md->.specify/skills/internal/run-agent/SKILL.md]
1 failed, 1 passed in 6.42s
rc=1
```

Both are the **planned mirror-regeneration ordering transient**, not a subject or assertion
defect: T028 runs `sync-mirrors.py --write --only skills/internal` and then `--check`; the two
params turn green at that point and the closure name-level diff is taken after it. No hand edit
of the mirror was made (a hand edit would be the defect this pair exists to catch).

Note on `targeted-set-v1` sufficiency: the literal algorithm (module stem `SKILL` and short
name `agents-run`) selects 381 test files, i.e. nearly the whole contract/integration surface,
which would collide with the one-full-suite budget. The package therefore ran the task rows'
explicitly named verification sets (the two new modules, then the four named guards plus the
narrow mirror param) and records that deviation openly; the closure slot owns the full
name-level comparison.

## T010 — `tests/contract/test_agents_run_multi_child_edges.py` (regression guard, one run)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_multi_child_edges.py -q
# test runner: python3 -m pytest -n auto --dist load -m "not slow" tests/contract/test_agents_run_multi_child_edges.py -q
# test runner: mode=parallel workers=auto dist=load passes=1 tier=fast excluded_slow=0
bringing up nodes...
bringing up nodes...

....                                                                     [100%]
4 passed in 6.23s
rc=0
```

The module guards pre-existing engine behaviour (migration/regression exception): the fixture
builds same-parent dispatch records in the shape `exec-quant.py --action collect-dispatch`
declares (`unit_type=agent` / `unit_id=agent:root` / `run_id=<label>`) plus the external
triplet, then runs the read-only `role-edge-check.py`. Reading inside the fixture:
2 edges (children `alpha` / `beta`, both depth 1, parent `root` depth 0), 0 violations,
0 conflicts. Mutation leg: two records collapsed onto one label snapshot to **1 edge** (the
red form — the report no longer presents two independent edges). Retry leg: both attempts'
triplets survive byte-identically. The fourth assertion pins `watch-model.md` § 11: the
`stale-run` attribution class and its consumption rule (only `own` events count for verdict,
state and current progress). SC-002 readings are these four assertions' decisive outputs.

## T012 — US2 turn-green reading (T010 + T011 landed)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_multi_child_edges.py tests/contract/test_agents_run_skill_wiring.py -q > /tmp/p2-us2-run.txt 2>&1; rc=$?
rc=1
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c22_zero_second_mechanism_and_clause_class_honesty
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c18_sdd_probe_applicability_is_narrowed
FAILED tests/contract/test_agents_run_skill_wiring.py::test_c19_run_stays_a_single_unit_and_records_the_reading
3 failed, 13 passed in 6.29s
```

C-16 / C-17 first turn green in this run (claimed at T011); the multi-child module is 4/4.
The 3 residual failures are exactly the allowed US3 set (C-18 / C-19 / C-22) — no failure
outside it. Process note: the first invocation of this set piped its output through `tail`,
which masked the runner's exit code; the rc above was re-captured on a second invocation with
direct redirection (same selection, same result) — a measurement-form error, disclosed.

## T015 — US3 turn-green reading + structural audits (T013 + T014 landed)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_scope_contract.py tests/contract/test_agents_run_skill_wiring.py -q > /tmp/p2-us3-run.txt 2>&1; rc=$?
rc=0
....................                                                     [100%]
20 passed in 6.28s
```

C-18 … C-22 all green; the scope module green. One test-side authoring defect was found and
repaired before this reading: the behavior-class honesty scanner matched its own detector
source lines (the phrase appeared in its assertion messages); the phrase is now assembled
from two fragments, so the scanner keeps scanning every new module including itself.

Structural audits:

```console
$ python3 .specify/scripts/python/flow-class-check.py --action check; echo rc=$?
flow-class check: 92 unit(s) scanned, 0 finding(s) [matched=92 inventory_units=92, clean]
coverage: ledger_rows=92 matched=92 inventory_units=92 gaps=0 parse_errors=0 floor=39
rc=0
```

`.specify/state/` and `.specify/memory/` read-only file/root-set comparison against the T001
baseline (`notes/pre-change-measurements.md`): baseline = tracked file set at `b6907ee53`
under `.specify/memory/` + the five untracked files named in the T001 `git status` snapshot,
ancestor-closed for directories; current = `find` over both roots.

- New directories (persistence roots) vs baseline: **0** (ancestor-closed comparison).
- New files under `.specify/memory/`: **2** — `exec-quant/.write.lock` and
  `exec-quant/aggregated/.write.lock`. Both are transient lock files written by the existing
  `exec-quant` mechanism (not records, not stores); 0 new record files.
- `.specify/state/` is git-ignored runtime state; files added since T001 are this line's
  existing stage-runner artifacts (`prompt-` / `status-` / `heartbeat-` / `log-` / `runner-log-` /
  `raw-` prefixed with `104-agents-run` and the stage name). No new storage class or root.

Fast-fail disclosure (measurement-form correction): a first pass compared `git ls-tree -d`
output (top-level entries only) with a recursive `find`, reporting 13 "new" directories;
every one was an intermediate parent of a path already present in the baseline. The
ancestor-closed recomputation above is the corrected reading — a derivation defect on the
measurement side, not a tree defect.

## T016 — `tests/contract/test_agents_run_docs_contract.py` (red)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_docs_contract.py -q > /tmp/p2-t016-red.txt 2>&1; rc=$?
rc=1
FAILED tests/contract/test_agents_run_docs_contract.py::test_c23_one_command_reference_body
FAILED tests/contract/test_agents_run_docs_contract.py::test_c24_opening_description_names_three_capabilities
FAILED tests/contract/test_agents_run_docs_contract.py::test_c25_syntax_block_carries_the_explicit_run_form
FAILED tests/contract/test_agents_run_docs_contract.py::test_c26_intent_table_run_row_and_three_way_ambiguity
FAILED tests/contract/test_agents_run_docs_contract.py::test_c27_companion_skills_lists_three_skills
FAILED tests/contract/test_agents_run_docs_contract.py::test_c28_no_argument_behaviour_matches_the_template
FAILED tests/contract/test_agents_run_docs_contract.py::test_c29_command_and_skills_becomes_three_capability
FAILED tests/contract/test_agents_run_docs_contract.py::test_c30_overview_gains_run_and_the_third_skill
FAILED tests/contract/test_agents_run_docs_contract.py::test_c31_design_gains_run_and_the_third_skill
FAILED tests/contract/test_agents_run_docs_contract.py::test_c32_tutorials_carry_run_and_drop_the_stale_claims
FAILED tests/contract/test_agents_run_docs_contract.py::test_c33_routing_scenario_is_three_capability
FAILED tests/contract/test_agents_run_docs_contract.py::test_c34_stale_literal_set_is_empty_and_history_is_untouched
12 failed in 6.24s
```

Red for the right reason: the command reference is still the three-copy concatenation (heading
count 3, measured before the T017 merge) and every named surface still carries the stale or
two-capability forms. Clause-per-function: C-23…C-34 each one named test, all collected, none
import- or collection-error.

## T017–T020 — US4 front-half reading (four reference surfaces landed)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_docs_contract.py tests/contract/test_agents_run_command_contract.py -q > /tmp/p2-docs-mid.txt 2>&1; rc=$?
rc=1
FAILED tests/contract/test_agents_run_docs_contract.py::test_c33_routing_scenario_is_three_capability
FAILED tests/contract/test_agents_run_docs_contract.py::test_c32_tutorials_carry_run_and_drop_the_stale_claims
FAILED tests/contract/test_agents_run_docs_contract.py::test_c34_stale_literal_set_is_empty_and_history_is_untouched
FAILED tests/contract/test_agents_run_command_contract.py::test_c09_per_tool_copies_are_generated_and_carry_the_run_form
4 failed, 18 passed in 6.61s
```

Green set: C-23 … C-31 (nine docs clauses) and the command contract's C-06 (three syntax faces
agree verbatim — the docs Syntax face now carries [[STR-001]] and the explicit run line).
Residual set is exactly the package boundary: C-32 (tutorials — T021), C-33 (routing scenario —
T022), C-34 (closed stale set — T023) and C-09 (per-tool copies drift until T027 regenerates).
No failure outside it.

Measured after-states for the four edited files (occurrence counts, `grep -oF | wc -l`):

- `docs/reference/commands/agents.md`: `^# /speckit.agents` heading count = **1** (was 3);
  STR-005 = 0, STR-006 = 0, bold variant = 0, STR-008 = 0, ci `generate role-based agents` = 0.
- `docs/reference/agents/command-and-skills.md`: STR-005 = 0, STR-006 = 0, bold variant = 0,
  ci `generate role-based agents` = 0; "three skills" statement in place; run row + routing
  step + `run-agent` section (by pointer) in place.
- `docs/reference/agents/overview.md`: command capability line names 创作 / 优化 / 运行; prose
  "三个技能"; navigation row "三个单 Agent 技能"; the entry diagram's skill layer carries
  `run-agent`.
- `docs/reference/agents/design.md`: capability line, workflow step 4 and the §6.2 single-agent
  skill list carry `run-agent`.

Fast-fail note: none of the four edits required a plan-owned change; the merged reference keeps
copy 1 as its base (deletions d2/d3 per the contract), so no `PLAN-EDIT:` declaration applies.

## Package-2 closing reading (all five agents-run modules)

```console
$ bash scripts/bash/run-tests.sh tests/contract/test_agents_run_command_contract.py tests/contract/test_agents_run_docs_contract.py tests/contract/test_agents_run_skill_wiring.py tests/contract/test_agents_run_multi_child_edges.py tests/contract/test_agents_run_scope_contract.py -q > /tmp/p2-package-run.txt 2>&1; rc=$?
rc=1
FAILED tests/contract/test_agents_run_docs_contract.py::test_c34_stale_literal_set_is_empty_and_history_is_untouched
FAILED tests/contract/test_agents_run_docs_contract.py::test_c33_routing_scenario_is_three_capability
FAILED tests/contract/test_agents_run_docs_contract.py::test_c32_tutorials_carry_run_and_drop_the_stale_claims
FAILED tests/contract/test_agents_run_command_contract.py::test_c09_per_tool_copies_are_generated_and_carry_the_run_form
4 failed, 42 passed in 6.71s
```

The four residual failures are exactly the declared package-3 surface (T021 tutorials /
T022 routing scenario / T023 C-34 close-out / T027 copy regeneration); everything else green.
`validate-tasks.py`: PASS with 0 errors and the one pre-adjudicated C-06/C-10 ordering warning
(tasks.md line 19 records that adjudication).
