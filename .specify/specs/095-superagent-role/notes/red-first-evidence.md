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
