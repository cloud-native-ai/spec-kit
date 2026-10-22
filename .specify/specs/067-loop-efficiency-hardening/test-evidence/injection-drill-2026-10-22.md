# Injection + Localization Drill (FB-08 / FB-09) — 2026-10-22

**Task**: 067 T028. **Acceptance (SC-008 / SC-009)**: name-level diff hits exactly the injected
name; the failure's unique node id reproduces the failure on a targeted rerun; restoration
returns the suite to 0 failed. **The injection is NOT in any commit** (verified below).

## Target

Merged parametrized suite `tests/contract/test_mirror_parity_suite.py` (T019–T022 fold, 723
params). Injected param:
`test_mirror_file_byte_identical[templates/checklist-template.md->.specify/templates/checklist-template.md]`

Injection form: a temporary two-line guard inside `test_mirror_file_byte_identical` that asserts
`False` only for that param (single failure site, no other param affected).

## Step 1 — run with injection, extract name-level list (FB-04 `--names-out`)

```
bash scripts/bash/run-tests.sh --names-out /tmp/067-injection-names.txt tests/contract/test_mirror_parity_suite.py -q
→ 1 failed, 722 passed in 1.09s
# failed-name list written: /tmp/067-injection-names.txt (1 entries)
```

`/tmp/067-injection-names.txt` (verbatim, 1 line):

```
tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[templates/checklist-template.md->.specify/templates/checklist-template.md]
```

## Step 2 — name-level diff against the T007 in-stage baseline (FB-08)

```
comm -13 test-evidence/baseline-failures-2026-10-22-implement-start.txt /tmp/067-injection-names.txt
→ tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[templates/checklist-template.md->.specify/templates/checklist-template.md]
```

**Verdict: HIT** — the diff contains exactly the injected name and nothing else; the suite's
other 722 params stayed green. (The T007 baseline predates the suite's fold, so no suite param
appears in it; the one-line diff is therefore exactly the injected set.)

## Step 3 — localization: rerun by the unique node id (FB-09)

Failure output names exactly one node id (param id carries both file paths, FR-020):

```
FAILED tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[templates/checklist-template.md->.specify/templates/checklist-template.md]
tests/contract/test_mirror_parity_suite.py:82: AssertionError
```

Direct targeted rerun of that node id:

```
bash scripts/bash/run-tests.sh "tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[templates/checklist-template.md->.specify/templates/checklist-template.md]" -q
→ 1 failed in 0.06s   (reproduced)
```

**Verdict: HIT** — the failure reproduces from the printed node id alone.

## Step 4 — restore and confirm

Injection removed (file restored to its committed content):

```
bash scripts/bash/run-tests.sh tests/contract/test_mirror_parity_suite.py -q
→ 723 passed in 1.00s   (0 failed)
git diff --stat tests/contract/test_mirror_parity_suite.py
→ (empty — file byte-identical to the committed state)
```

**Verdict: RESTORED** — suite back to 0 failed; `git status` shows no modification of the suite
file at drill end, so no injection residue can enter any commit.

## Outcome

All three acceptance gates (hit / localize / reproduce + restore) passed; no anomaly. Drill
executed 2026-10-22 during 067 implement part F; no full-suite slot consumed (suite-file-scoped
runs only).
