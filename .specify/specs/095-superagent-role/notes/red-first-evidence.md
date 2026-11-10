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

