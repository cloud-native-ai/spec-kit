# Red-first evidence — Feature 094 goal/team parallel

Owner of the format: this file. Every red-first row appends one entry below the divider.
Each entry carries the row id, the date, the exact command, the real (unfiltered) output
excerpt, and the process exit status. A green reading that does not name the red reading it
replaced is not evidence (Constitution IV; `shared/workflows/feedback-step.md`).

## Entry format (copy this block; never invent a second shape)

```text
### <row id> — <subject>
- date: <YYYY-MM-DD>
- command: <the exact command line>
- exit status: <integer>
- output (verbatim excerpt):
  <real output, unfiltered by any post-processing except line selection>
```

---

<!-- Append new entries below this line, newest last. -->

### T005 — binding-record reader and the module's first red reading
- date: 2026-11-09
- command: `python3 -m pytest tests/contract/test_binding_model.py -q`
- exit status: 1
- output (verbatim excerpt):
```text
FAILED tests/contract/test_binding_model.py::test_a_definition_without_a_complete_binding_is_uninterpretable
FAILED tests/contract/test_binding_model.py::test_owner_outside_the_closed_three_values_is_refused
FAILED tests/contract/test_binding_model.py::test_owner_id_is_validated_by_shape_and_the_grammar_is_cited_not_restated
FAILED tests/contract/test_binding_model.py::test_origin_naming_a_non_existent_spec_directory_is_refused
FAILED tests/contract/test_binding_model.py::test_rebind_changes_only_the_binding_block
FAILED tests/contract/test_binding_model.py::test_a_hand_edited_binding_block_is_reported_not_trusted
FAILED tests/contract/test_binding_model.py::test_a_terminal_goal_refuses_a_new_team_binding
FAILED tests/contract/test_binding_model.py::test_ownership_is_answered_by_the_read_action_not_by_the_path
FAILED tests/contract/test_binding_model.py::test_scope_spec_is_removed_and_no_alias_exists
FAILED tests/contract/test_binding_model.py::test_both_archive_roots_resolve_in_one_call_and_auto_is_read_only
FAILED tests/contract/test_binding_model.py::test_a_cross_layer_write_is_refused_and_names_both_layers
FAILED tests/contract/test_binding_model.py::test_a_bound_goal_is_writable_only_by_human
12 failed in 0.63s
```
- full reading: `test-evidence/wp01-T005-red.txt`
