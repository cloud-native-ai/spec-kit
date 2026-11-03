# Quickstart Run — Feature 081, slice 081a (smoke record, T019)

**Measured**: 2026-11-03 at implement part 4 on branch `081-acceptance-hardening` (parent commit `da5e4480`),
on the post-T018 tree — i.e. after every 081a source edit and both regenerations.

**Owner of the shape**: `templates/verification-log-template.md` § THE SMOKE RECORD — three fields, exactly
one record per feature. This note is the human-readable companion of the machine-readable record seeded into
`verification.md` (T020); the two carry the same three values and no fourth.

## The record (three fields, verbatim)

| Field | Value |
|---|---|
| `smoke_command` | `bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q` |
| `smoke_exit_code` | `0` |
| `smoke_evidence_path` | `.specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt` |

## The two runs (T019 requirement: identical exit status)

```text
$ bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q
# test runner: .venv/bin/python -m pytest tests/integration/test_acceptance_smoke.py -q
.                                                                        [100%]
1 passed in 1.27s
EXIT=0

$ bash scripts/bash/run-tests.sh tests/integration/test_acceptance_smoke.py -q
# test runner: .venv/bin/python -m pytest tests/integration/test_acceptance_smoke.py -q
.                                                                        [100%]
1 passed in 1.23s
EXIT=0
```

- Run 1 exit status: `0`
- Run 2 exit status: `0`
- Identical: **yes** (2/2) — the SC-008 clause 「同一命令连跑两次退出码相同」 holds, and the wall-clock
  difference between the two runs (`1.27s` vs `1.23s`) is elapsed time, not a declared value, so nothing in
  the assertion depends on it.

## What the smoke covers (FR-005's three subjects)

The evidence file the run rewrites each time it executes records all three sub-checks and their exit codes:

1. `specify init` from the checkout's own templates builds a `.specify/` tree — exit `0`;
2. the closure checker on both fixture sets — `positive` → `accept` / exit `0`; `negative` → `block` /
   exit `1` with `zero-final-path-pass`;
3. `regen-command-copies.py --check` — exit `0`, no mismatch.

No network, no wall clock, no cluster: the command is deterministic on local fixtures, which is what keeps
"cannot run the smoke" from being an acceptable excuse for the feature's own acceptance record.

## Assumption recorded (no confirmation asked)

The brief does not say whether the two runs should be bracketed by tree changes. They were run back to back
on the same tree, because a smoke whose second run describes a different tree would not demonstrate
reproducibility. Nothing was edited between the two invocations.
