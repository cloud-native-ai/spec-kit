# Red-First Evidence — 110-context-management

**Purpose**: T005 skeleton — one slot per guard file (five) and one slot per `check` rule (nine), each recording a command, the real output and the exit status when its observation happens. A slot left `open` means its observation has not happened yet; it MUST NOT be read as a green or a red.
**Failing-name baseline owner**: the implement command's **Test runs** bullet (path and flag owned there and referenced, never restated here). This file cites that owner and carries no copy of its path or flag.
**Test entry**: every command below runs through `scripts/bash/run-tests.sh` (single entry; `SPECKIT_PYTHON=/usr/local/bin/python3` fixed at implement entry).

## A. Per-guard-file slots

### A-1 `tests/contract/test_context_management_owner.py` (T009)

- status: red (observed 2026-11-27, before any owner-document edit)
- red sink: `test-evidence/red-owner.txt`
- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_context_management_owner.py > .specify/specs/110-context-management/test-evidence/red-owner.txt 2>&1`
- real output (decisive excerpt): `FAILED …::test_owner_document_is_the_single_model_home` — `AssertionError: owner document missing: …/shared/definitions/context-management-definitions.md`; `============================== 18 failed in 6.62s ==============================`
- exit status: 1

### A-2 `tests/contract/test_context_management_declarations.py` (T010)

- status: red (observed 2026-11-27, before any declaration-fact edit)
- red sink: `test-evidence/red-declarations.txt`
- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_context_management_declarations.py > .specify/specs/110-context-management/test-evidence/red-declarations.txt 2>&1`
- real output (decisive excerpt): `FAILED …::test_four_facts_carry_mandatory_keys_and_kinds` — `AssertionError: declaration fact missing: …/shared/declarations/facts/context-categories.yaml`; `============================== 12 failed in 6.28s ==============================`
- exit status: 1

### A-3 `tests/contract/test_context_management_engine.py` (T011)

- status: open
- red sink: `test-evidence/red-engine.txt`
- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_context_management_engine.py > .specify/specs/110-context-management/test-evidence/red-engine.txt 2>&1`
- real output: —
- exit status: —

### A-4 `tests/contract/test_context_management_readonly.py` (T012)

- status: open
- red sink: `test-evidence/red-readonly.txt`
- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_context_management_readonly.py > .specify/specs/110-context-management/test-evidence/red-readonly.txt 2>&1`
- real output: —
- exit status: —

### A-5 `tests/integration/test_context_management_init.py` (T013)

- status: open
- red sink: `test-evidence/red-init.txt`
- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/integration/test_context_management_init.py > .specify/specs/110-context-management/test-evidence/red-init.txt 2>&1`
- real output: —
- exit status: —

## B. Per-`check`-rule slots (mutation drill, T034)

Each slot's observable is the **guard test's verdict** under the rule's own mutation, never the engine's finding output (C-040). Slots open until the drill at T034; per-rule command, real output and exit status are captured into `test-evidence/mutation-drill.txt` and echoed here.

| # | Rule | Seeded fixture | Guard-test carrier (authored in T011) | Status |
|---|------|----------------|---------------------------------------|--------|
| 1 | `roster-mismatch` | `tests/fixtures/context-management/violation-roster-mismatch/` | `test_context_management_engine.py` | open |
| 2 | `roster-order` | `tests/fixtures/context-management/violation-roster-order/` | `test_context_management_engine.py` | open |
| 3 | `unknown-layer` | `tests/fixtures/context-management/violation-unknown-layer/` | `test_context_management_engine.py` | open |
| 4 | `unknown-form` | `tests/fixtures/context-management/violation-unknown-form/` | `test_context_management_engine.py` | open |
| 5 | `layer-form-illegal` | `tests/fixtures/context-management/violation-layer-form/` | `test_context_management_engine.py` | open |
| 6 | `duplicate-class` | `tests/fixtures/context-management/violation-duplicate-class/` | `test_context_management_engine.py` | open |
| 7 | `empty-layer` | `tests/fixtures/context-management/violation-empty-layer/` | `test_context_management_engine.py` | open |
| 8 | `cap-missing` | `tests/fixtures/context-management/violation-cap-missing/` | `test_context_management_engine.py` | open |
| 9 | `category-column` | `tests/fixtures/context-management/violation-category-column/` | `test_context_management_engine.py` | open |

## C. Record of filled slots

Filled slots append one record each in the form `slot | command | real output (decisive excerpt) | exit status`, date-stamped.

- A-1 | `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_context_management_owner.py` | 18 failed; first failure `owner document missing` | exit 1 | 2026-11-27
- A-2 | `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_context_management_declarations.py` | 12 failed; first failure `declaration fact missing: context-categories.yaml` | exit 1 | 2026-11-27