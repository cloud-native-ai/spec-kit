# Pre-change measurements — Feature 087 (implement stage, Part 1)

**Capture date**: 2026-11-06T06:42:05Z (UTC)
**Capture point**: before any implement-stage write to a framework source tree on this line
**Owner of the baseline form**: `/speckit.implement` step 6 `**Test runs**` bullet (this file points at it; it does not
define a second form)

This file is the **name-list** baseline for the one pre-existing suite Feature 087's zero-NEW-failure criterion is
measured against (`tasks.md` GATE-1, `plan.md` EP-010). It records node ids, never only a count, because a count
cannot distinguish "the same seven green" from "six green plus one renamed".

## T002 — The progress-reporting suite node-id baseline

**Command (verbatim)**:

```bash
python3 -m pytest -q --collect-only tests/contract/test_progress_reporting.py
```

**Tool versions at capture time**:

```text
python3 --version  -> Python 3.11.11
pytest --version   -> pytest 8.4.2
```

**Actual output (verbatim, complete)**:

```text
tests/contract/test_progress_reporting.py::test_heading_and_pointer_present_in_both_template_copies
tests/contract/test_progress_reporting.py::test_ambient_section_carries_the_five_keywords
tests/contract/test_progress_reporting.py::test_doc_defines_the_load_bearing_clauses
tests/contract/test_progress_reporting.py::test_doc_ships_no_machinery
tests/contract/test_progress_reporting.py::test_default_interval_agrees_between_owner_and_reachability_surface
tests/contract/test_progress_reporting.py::test_command_template_points_at_the_owner_without_restating_the_interval
tests/contract/test_progress_reporting.py::test_section_and_doc_are_project_neutral
```

```text
7 tests collected in 0.02s
```

**Green reading at the same point** (`python3 -m pytest -q tests/contract/test_progress_reporting.py`):

```text
.......                                                                  [100%]
7 passed in 0.05s
```

**Reading**: the baseline is **7 node ids, all green**. The comparison this baseline feeds is a node-id set
difference (`comm -13 baseline current`), not an exit code: a post-change run may add node ids (that is not a
regression), but an id present here and absent there, or present and red there, is a NEW failure.

## Pre-change verdict for the whole suite

The driver's implement-start full-suite run is the other half of the pre-change picture and is recorded in the state
spine's test-budget block (`seq=1`, `rc=1`, `passed=7473`, `failed=27`, `skipped=1`, evidence
`test-evidence/baseline-full-suite-20261106T063158Z.log`). This Part-1 execution does **not** re-run the full suite
(test budget: the implement start ran it once; every later reading is a targeted set).

**Doctests / collection note**: the command above is a pure collection, so its exit status reflects importability
only — the seven ids were also confirmed green by the same-file run quoted above, so none of them is a collection-only
ghost.
