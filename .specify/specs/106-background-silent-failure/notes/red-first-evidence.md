# Red-First Evidence — spec 106

Every entry records the command, the real output (decisive excerpt) and the exit code.
The test entry is `scripts/bash/run-tests.sh`; the interpreter override on this host is
`SPECKIT_PYTHON=/usr/local/bin/python3` (measured premise, tasks.md § Environment
Prerequisites).

<!-- entries are appended in execution order -->

## T004 — settlement contract definitions (owner page)

- Command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_settlement_contract_definitions.py -q`
- Exit code: **1**
- Real output (tail): `18 failed, 1 passed in 6.24s` — every owner-text leg fails on
  `AssertionError: § Termination is missing from shared/definitions/superagent-definitions.md
  (the settlement contract owner section, C-01)`; the single pass is the vacuous
  "no second value table" scan (no second table exists yet because the owner table does
  not exist yet).
- Red-first ordering note: the pinning test was authored **before** the owner-section
  amendment (T002/T003) precisely so the red is real, not a missing-file artifact; the
  named assertions quote the contract clauses C-01…C-12.

