# Red-first evidence — `tests/contract/test_harness_triple_structure.py`

**Task**: `tasks.md` T005 (`blockedBy: T003`) · **Date**: 2026-11-05

## The gate row this evidence binds, quoted verbatim

From `tasks.md` § Completion Gate:

```text
- GATE-1: The contract test module is green — check: `bash scripts/bash/run-tests.sh tests/contract/test_harness_triple_structure.py -q`
```

Quoted in full — id (`GATE-1`), name ("The contract test module is green"), and check command — because a
bare id is not a quote: a later stage must be able to run exactly the command this row names and get the
verdict this module's assertions give.

## The red run, before either subject existed

Command and reading, `T006` (`declaration_reader.py`) and `T007` (`harness-triple-check.py`) both absent:

```bash
python3 -m pytest tests/contract/test_harness_triple_structure.py -q
```

```text
20 failed, 1 passed, 1 warning in 0.41s
exit code: 1
```

Representative failure (identical shape on 17 of the 20 — the engine is invoked as a consumer invokes it,
so an absent engine is an absent command, not an import error):

```text
E       AssertionError: /usr/bin/python3: can't open file '/storage/project/cloud-native-ai/spec-kit/scripts/python/harness-triple-check.py': [Errno 2] No such file or directory
E
E       assert 2 == 0
```

The full output is `.specify/specs/084-harness-triple-structure/test-evidence/red-first-run-2026-11-05.txt`.

**The one passing row is named rather than glossed**: `test_every_reason_has_a_negative_fixture_and_every_
action_a_positive_one` inspects the module's own case table, so it can be green while the engine is absent.
It is a coverage-of-fixtures assertion, not a subject assertion.

## Why this ordering matters here

`tasks.md` § Phase 2 states the rule this file exists to honour: *"T005 authors the assertions **first**;
T006 and T007 close them. A green assertion written after its subject cannot show that the subject was ever
missing."* The red run above is the reading that shows the module was written against absent subjects; the
green run after T007 is recorded in `stage-status.md`, and neither replaces the other.
