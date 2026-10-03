# Red-first evidence — Feature 053

**Purpose**: every test that MUST go red before its subject exists gets its command, real output and exit status recorded here (Tests Mode = ON, Constitution Principle IV). Red-first output is pasted, never predicted.

**Capture date**: 2026-10-03 · **BASE SHA**: see `pre-change-measurements.md`

<!-- entries are appended per task; each carries the task id, the command, the verbatim failing output and the exit code -->

## T004 — tests/contract/test_clause_forms.py (2026-10-03)

```
$ bash .specify/scripts/bash/run-tests.sh -q tests/contract/test_clause_forms.py
^^^^^^^^^^^^^^^^^^^^^^^^^^
E   ModuleNotFoundError: No module named 'clause_extract'
=========================== short test summary info ============================
ERROR tests/contract/test_clause_forms.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
1 error in 0.09s
EXIT=2
```

Red for the right reason: the subject module does not exist yet. 24 test functions collected-by-intent (the suite errors at import, so collection is interrupted — that is the expected red form for a missing module, not a syntax defect in the test file).
