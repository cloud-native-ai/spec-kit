# Pre-change measurements — Feature 088 (implement stage, Part 1)

**Capture date**: 2026-11-06T06:42:05Z (UTC)
**Capture point**: before any implement-stage write to a framework source tree on this line
**Owner of the baseline form**: `/speckit.implement` step 6 `**Test runs**` bullet (this file points at it; it does not
define a second form)

This file is the **name-list** baseline for the one pre-existing suite Feature 088's zero-NEW-failure criterion is
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

## Pre-change side closure — `status=not-run-docs-only` (T045)

status=not-run-docs-only
status_note=Written by `/speckit.implement` Part 6 (T045) to close the pre-change side of this file. The **full suite** was not re-run by any row of this feature beyond the single implement-start shot recorded above (state spine test-budget `seq=1`, `passed=7473`, `failed=27`, `skipped=1`, evidence `test-evidence/baseline-full-suite-20261106T063158Z.log`). Every later reading this feature took is a **targeted** set: the seven progress-reporting node ids above, the six C-51 suites compared by node-id set (`test-evidence/cl-01-closure.txt` § 1), and the four contract suites plus the unit suite (127 + 29 passed, `test-evidence/us4-guard-verdict.txt` § 5). The closure full-suite slot belongs to the driver after review, per the test budget — so this file's pre-change side is closed as "not run beyond the one start-of-run shot", not as "green".
status_readings=pre-change progress-reporting baseline 7 ids all green (above); pre-change affected suites 91 ids, 91 passed (`cl-01-closure.txt` § 1); pre-change full suite 7473 passed / 27 failed / 1 skipped (state spine seq=1)
status_owner=the baseline form is `/speckit.implement` step 6 bullet `**Test runs**` (`.specify/skills/internal/implement-feature/SKILL.md`); this file points at it and defines no second form
