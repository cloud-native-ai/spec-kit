# Red-first evidence — 095-superagent-role

Landing point for every row that must go red before its subject exists. Each instance records: the
command, its real output, and its exit status. When an instance binds a claim to a gate, it quotes the
gate row verbatim (id + name + check command) — a bare gate id is never used.

Every test command runs through the single runner `bash scripts/bash/run-tests.sh` (default
`-n <effective> --dist load`; test paths and arguments are forwarded verbatim). Interpreter-level test
commands are never the entry.

## Instances

### Instance 1 — T004 definitions contract (red-first)

- Date: 2026-11-10
- Command: `bash scripts/bash/run-tests.sh tests/contract/test_superagent_definitions.py -q`
- Exit status: **1**
- Red state: the owner page `shared/definitions/superagent-definitions.md` (and therefore its
  runtime mirror) does not exist yet, and the three sibling pointer lines are absent. Nine of the
  ten legs fail as “artifact missing”; the tenth (`test_agent_definitions_has_no_second_subagent_definition`)
  guards the untouched sibling page and is reported for completeness.

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_superagent_definitions.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...

.FFFFFFFFF                                                               [100%]
=================================== FAILURES ===================================
_______________________ test_three_sibling_pointer_lines _______________________
    def test_three_sibling_pointer_lines():
        """All three sibling pages carry the pointer line / row to the new owner."""
        agent = _read(AGENT_DEFS)
>       assert "superagent-definitions.md" in agent, "agent-definitions.md pointer line missing"
E       AssertionError: agent-definitions.md pointer line missing
tests/contract/test_superagent_definitions.py:192: AssertionError
________________________ test_required_sections_present ________________________
    def test_required_sections_present():
        """The nine model sections land as level-2 headings."""
>       headings = {line.strip() for line in _owner_text().splitlines() if line.startswith("## ")}
tests/contract/test_superagent_definitions.py:113: in _owner_text
    return _read(OWNER_SRC)
tests/contract/test_superagent_definitions.py:108: in _read
>       assert path.is_file(), f"missing required file: {path.relative_to(REPO_ROOT)}"
E       AssertionError: missing required file: shared/definitions/superagent-definitions.md
tests/contract/test_superagent_definitions.py:108: AssertionError
... (the remaining legs fail on the same missing-artifact assertion or on their
    absent page content; full failure list below)
=========================== short test summary info ============================
FAILED tests/contract/test_superagent_definitions.py::test_three_sibling_pointer_lines
FAILED tests/contract/test_superagent_definitions.py::test_required_sections_present
FAILED tests/contract/test_superagent_definitions.py::test_four_message_class_tokens
FAILED tests/contract/test_superagent_definitions.py::test_owner_page_present_on_both_sides
FAILED tests/contract/test_superagent_definitions.py::test_pointer_only_discipline
FAILED tests/contract/test_superagent_definitions.py::test_ownership_declared_up_front
FAILED tests/contract/test_superagent_definitions.py::test_nine_item_closed_list
FAILED tests/contract/test_superagent_definitions.py::test_role_depth_vs_license_chain_sentence
FAILED tests/contract/test_superagent_definitions.py::test_owner_page_avoids_three_layer_marker_literal
9 failed, 1 passed in 6.16s
```

### Instance 2 — T011 role-edge engine contract (red-first)

- Date: 2026-11-10
- Command: `bash scripts/bash/run-tests.sh tests/contract/test_role_edge_engine.py -q`
- Exit status: **1**
- Red state: neither `scripts/python/role-edge-check.py` nor `tests/fixtures/superagent-role/`
  exists yet. Every leg fails on its own named missing-artifact assertion (`engine missing` or
  `fixture missing`) — no import or collection error. The module imports the engine lazily, so
  the absence is reported as an assertion, not as a traceback at collection time.

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_role_edge_engine.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

FFFFFFFFFFFFFFFFFFFF                                                     [100%]
=================================== FAILURES ===================================
_______________________ test_two_runs_are_byte_identical _______________________
[gw16] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_two_runs_are_byte_identical():
>       first = run_engine("--action", "report", *_roots("root-a-b"))
                                                  ^^^^^^^^^^^^^^^^^^

tests/contract/test_role_edge_engine.py:581:
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _
tests/contract/test_role_edge_engine.py:112: in _roots
    base = _fixture(name)
           ^^^^^^^^^^^^^^
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

name = 'root-a-b'

    def _fixture(name: str) -> Path:
        base = FIXTURE_ROOT / name
>       assert base.is_dir(), f"fixture missing: tests/fixtures/superagent-role/{name}"
E       AssertionError: fixture missing: tests/fixtures/superagent-role/root-a-b
E       assert False
E        +  where False = is_dir()
E        +    where is_dir = PosixPath('/storage/project/cloud-native-ai/spec-kit/tests/fixtures/superagent-role/root-a-b').is_dir

tests/contract/test_role_edge_engine.py:105: AssertionError
... (the remaining legs fail on the same two named missing-artifact assertions;
    full failure list below)
=========================== short test summary info ============================
FAILED tests/contract/test_role_edge_engine.py::test_two_runs_are_byte_identical
FAILED tests/contract/test_role_edge_engine.py::test_engine_has_zero_write_points_in_source
FAILED tests/contract/test_role_edge_engine.py::test_fixture_tree_is_byte_identical_after_a_run
FAILED tests/contract/test_role_edge_engine.py::test_query_pair_and_unresolvable_identities
FAILED tests/contract/test_role_edge_engine.py::test_dangling_parent_names_both_sides_and_the_path
FAILED tests/contract/test_role_edge_engine.py::test_violation_fixtures_each_kind_in_isolation[violations/depth-cycle-depth-inconsistent]
FAILED tests/contract/test_role_edge_engine.py::test_mutation_injected_violation_turns_red
FAILED tests/contract/test_role_edge_engine.py::test_mutation_type_based_classification_turns_red
FAILED tests/contract/test_role_edge_engine.py::test_help_version_and_undeclared_option
FAILED tests/contract/test_role_edge_engine.py::test_malformed_row_shape_is_named_and_exits_two
FAILED tests/contract/test_role_edge_engine.py::test_conflict_rows_name_both_paths_and_edge_identity
FAILED tests/contract/test_role_edge_engine.py::test_importable_interface_matches_report
FAILED tests/contract/test_role_edge_engine.py::test_unbacked_superagent_claim_red_and_granted_without_children_green
FAILED tests/contract/test_role_edge_engine.py::test_required_roots_fatal_and_registry_optional
FAILED tests/contract/test_role_edge_engine.py::test_violation_fixtures_each_kind_in_isolation[violations/dangling-parent-dangling-parent]
FAILED tests/contract/test_role_edge_engine.py::test_violation_fixtures_each_kind_in_isolation[violations/self-dispatch-self-dispatch]
FAILED tests/contract/test_role_edge_engine.py::test_violation_fixtures_each_kind_in_isolation[violations/unbacked-claim-unbacked-role-claim]
FAILED tests/contract/test_role_edge_engine.py::test_report_schema_clean_chain
FAILED tests/contract/test_role_edge_engine.py::test_malformed_value_is_named_and_exits_two
FAILED tests/contract/test_role_edge_engine.py::test_empty_set_is_explicit_and_clean
20 failed in 6.15s
```

### Instance 3 — T029 three-form cases (red-first, US3 fixtures absent)

- Date: 2026-11-10
- Command: `bash scripts/bash/run-tests.sh tests/contract/test_role_edge_engine.py -q`
- Exit status: **1**
- Red state: the US1 legs are already green (21 passed); the four appended US3 legs fail
  only because `tests/fixtures/superagent-role/{local-team,remote-topology,fanout-10}/`
  do not exist yet — each fails on the named `fixture missing` assertion.

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_role_edge_engine.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

..FFF.........F..........                                                [100%]
=================================== FAILURES ===================================
...
name = 'fanout-10'

    def _fixture(name: str) -> Path:
        base = FIXTURE_ROOT / name
>       assert base.is_dir(), f"fixture missing: tests/fixtures/superagent-role/{name}"
E       AssertionError: fixture missing: tests/fixtures/superagent-role/fanout-10
E        +  where False = is_dir()
E        +    where is_dir = PosixPath('/storage/project/cloud-native-ai/spec-kit/tests/fixtures/superagent-role/fanout-10').is_dir

tests/contract/test_role_edge_engine.py:105: AssertionError
=========================== short test summary info ============================
FAILED tests/contract/test_role_edge_engine.py::test_three_forms_direction_reversal_turns_red
FAILED tests/contract/test_role_edge_engine.py::test_three_forms_remote_topology
FAILED tests/contract/test_role_edge_engine.py::test_three_forms_local_team
FAILED tests/contract/test_role_edge_engine.py::test_three_forms_fanout_10 - ...
4 failed, 21 passed in 6.21s
```

### Instance 4 — T020 role-transition payload contract (red-first)

- Date: 2026-11-10
- Command: `bash scripts/bash/run-tests.sh tests/contract/test_role_transition_payload.py -q`
- Exit status: **1**
- Red state: the payload fixtures exist (T019) and the payload-side legs are green; the five
  wiring surfaces (run-agent SKILL, team patterns, team SKILL, driver SKILL, stage-prompts)
  stand unchanged, so the six surface legs fail on their own named assertions. Captured in a
  scratch git worktree at `dd7cbbab4` with only the new test module and fixtures copied in, so
  the record reproduces the pre-wiring tree state. (The first attempt in the working tree also
  flagged `test_return_contract_five_items` because of a test-side line-wrap comparison defect;
  that was repaired before any surface edit — disclosed in
  `test-evidence/role-transition-readings.txt` §1.)

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_role_transition_payload.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

_________________ test_team_report_mapping_table_is_mandatory __________________
    def test_team_report_mapping_table_is_mandatory():
        """`## Execution Detail` must carry the five-column dispatch mapping table."""
        text = _read(TEAM_SKILL[0])
        section = _section(text, "### Report contract", "### Verification")
        assert "## Execution Detail" in section
>       assert "每个被派发的执行体一行" in section, "one row per dispatched executor is not required"
E       AssertionError: one row per dispatched executor is not required

=========================== short test summary info ============================
FAILED tests/contract/test_role_transition_payload.py::test_driver_pointer_line_root_superagent
FAILED tests/contract/test_role_transition_payload.py::test_driver_envelope_names_sidecar_and_role_edge
FAILED tests/contract/test_role_transition_payload.py::test_run_agent_pointer_item_and_self_check_extension
FAILED tests/contract/test_role_transition_payload.py::test_seven_downlink_fields_on_each_wired_surface[driver envelope role_edge object-<lambda>]
FAILED tests/contract/test_role_transition_payload.py::test_seven_downlink_fields_on_each_wired_surface[team Per-Agent Payload role_fields row-<lambda>]
FAILED tests/contract/test_role_transition_payload.py::test_team_report_mapping_table_is_mandatory
6 failed, 15 passed in 7.02s
```

### Instance 5 — T034 digest role view contract (red-first)

- Date: 2026-11-10
- Command: `bash scripts/bash/run-tests.sh tests/contract/test_status_digest_roles.py -q`
- Exit status: **1**
- Red state: the contract module (T034) and the `interrupted/` fixture (T035) exist; `status-digest.py`
  carries no role view yet. Every failing leg names its own missing subject — the field helper finds
  `read_carrier_inputs: 0`, the JSON field legs fail on the absent `id` row / absent
  `role_set_marker`, the fan-out leg gets the pre-095 `nothing-running` (exit 3, empty registry),
  and the structural legs report the missing declaration/attachment. Five legs are green by
  construction (`nothing-running` unchanged, marker absent as required for pass-through, the action
  still delegates to the one table renderer, and the mirror equality leg runs green-by-default) —
  they are the guards the change must not break, not legs that weaken the red.
- Note (disclosed when the green run follows): the mirror leg is trivially green while the pair is
  byte-identical, so it only gains force once T037 syncs the runtime copy in the same package.

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_status_digest_roles.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...
bringing up nodes...

...FFFFFFFFF.FFF.F                                                       [100%]
=================================== FAILURES ===================================
________ test_c1_the_digest_adds_no_second_carrier_parser_or_root_scan _________
...
________ test_c1_the_role_model_is_one_materialization_per_run _____________
[gw0] linux -- Python 3.11.11 /usr/local/bin/python3

    def test_c1_the_role_model_is_one_materialization_per_run():
        """C-1: one ``read_carrier_inputs`` + one ``evaluate_role_model`` per digest run, from ``read_state``."""
        source = _engine_source()
        counts = _call_counts(source)
>       assert counts["counts"]["read_carrier_inputs"] == 1, (
            "the role model must be materialized by exactly one carrier read; got %r"
            % counts["counts"]
        )
E       AssertionError: the role model must be materialized by exactly one carrier read; got {'read_carrier_inputs': 0, 'evaluate_role_model': 0, 'read_role_materialization': 0}
E       assert 0 == 1

tests/contract/test_status_digest_roles.py:209: AssertionError
... (the remaining legs fail on their own named assertions; full failure list below)
=========================== short test summary info ============================
FAILED tests/contract/test_status_digest_roles.py::test_c1_the_digest_adds_no_second_carrier_parser_or_root_scan
FAILED tests/contract/test_status_digest_roles.py::test_c7_dropping_a_role_field_turns_the_declaration_check_red
FAILED tests/contract/test_status_digest_roles.py::test_c2_the_four_role_fields_are_declared_once
FAILED tests/contract/test_status_digest_roles.py::test_c1_the_role_model_is_one_materialization_per_run
FAILED tests/contract/test_status_digest_roles.py::test_c5_role_fields_are_attached_without_process_state
FAILED tests/contract/test_status_digest_roles.py::test_c4_one_read_renders_the_parent_and_ten_children
FAILED tests/contract/test_status_digest_roles.py::test_without_carrier_roots_the_role_fields_render_as_empty_not_missing
FAILED tests/contract/test_status_digest_roles.py::test_c4_the_table_carries_the_role_columns
FAILED tests/contract/test_status_digest_roles.py::test_c6_the_existing_json_keys_keep_their_names
FAILED tests/contract/test_status_digest_roles.py::test_c3_omitted_declares_the_truncated_merged_set
FAILED tests/contract/test_status_digest_roles.py::test_the_interrupted_child_renders_stale_interrupted_and_never_completed
FAILED tests/contract/test_status_digest_roles.py::test_c2_line_rows_gain_the_role_fields_and_keep_their_family
FAILED tests/contract/test_status_digest_roles.py::test_c2_executor_rows_outside_the_registry_use_the_role_names
13 failed, 5 passed in 6.19s
```

### Instance 6 — T040 instructions pointer section contract (red-first)

- Date: 2026-11-10
- Command: `bash scripts/bash/run-tests.sh tests/contract/test_instructions_budget_superagent_section.py -q`
- Exit status: **1**
- Red state: the section `## Super Agent (相对逻辑角色)` does not exist in
  `templates/instructions-template.md` yet (T042 adds it), so every leg that reads the section
  fails on its own "section missing" assertion — never on an import error. The budget leg
  (`test_generated_size_stays_under_the_script_owned_budget`) is green at authoring time: it
  guards T043's generated file afterwards and its being green is the pre-change measurement,
  not a weakened red.

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_instructions_budget_superagent_section.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...


    def test_live_file_carries_the_section():
        """C-5: the generator-produced live file carries the section in the same position."""
        live = LIVE.read_text(encoding="utf-8")
        headings = re.findall(r"(?m)^## .+$", live)
>       assert HEADING in headings, (
            "the live .specify/instructions.md does not carry the section — run "
            "bash scripts/bash/generate-instructions.sh after syncing the template mirror"
        )
E       AssertionError: the live .specify/instructions.md does not carry the section — run bash scripts/bash/generate-instructions.sh after syncing the template mirror

=========================== short test summary info ============================
FAILED tests/contract/test_instructions_budget_superagent_section.py::test_section_sits_between_the_two_fixed_neighbours
FAILED tests/contract/test_instructions_budget_superagent_section.py::test_section_is_pointer_form
FAILED tests/contract/test_instructions_budget_superagent_section.py::test_pointer_check_is_not_blind
FAILED tests/contract/test_instructions_budget_superagent_section.py::test_live_file_carries_the_section
4 failed, 1 passed in 6.92s
```

### Instance 7 — T041 zero-second-mechanism audit (red-first)

- Date: 2026-11-10
- Command: `bash scripts/bash/run-tests.sh tests/contract/test_superagent_zero_mechanism.py -q`
- Exit status: **1**
- Red state: five of the six C-3 legs are green against the already-landed P1–P4 sources
  (inventory, registry, renderer, dispatcher, read-only judgement); the owner-rules leg is red
  because its surface scan requires the template pointer section T042 has not added yet. The
  green-by-construction legs are the guards this package must not break; the seeded mutations
  inside each leg prove they are not blind.

```text
# test runner: python3 -m pytest -n auto --dist load tests/contract/test_superagent_zero_mechanism.py -q
# test runner: mode=parallel workers=auto dist=load passes=1
bringing up nodes...


    def _section(text: str, heading: str) -> str:
        parts = re.split(r"(?m)^(## .+)$", text)
        sections = {parts[i]: parts[i] + parts[i + 1] for i in range(1, len(parts) - 1, 2)}
>       assert heading in sections, f"section {heading!r} is missing from the subject file"
E       AssertionError: section '## Super Agent (相对逻辑角色)' is missing from the subject file

=========================== short test summary info ============================
FAILED tests/contract/test_superagent_zero_mechanism.py::test_c3_6_owner_rules_not_copied
1 failed, 5 passed in 6.16s
```


