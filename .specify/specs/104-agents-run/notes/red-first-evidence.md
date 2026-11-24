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
