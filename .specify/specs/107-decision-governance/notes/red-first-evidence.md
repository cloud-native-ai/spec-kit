# Red-first evidence — 107-decision-governance

**Owner of the failing-test baseline name list**: `/speckit.implement` `**Test runs**` (the list is written by the single test entry at `.specify/specs/107-decision-governance/baseline-failed.txt`; it is referenced here, never restated).
**Single test entry**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh …` (no interpreter-level test command is ever the entry).
**Rule**: one slot per planned red-first test. A slot is filled only with a real command, the real output and the real exit status captured at run time; a slot never carries an estimate. Slots fill as their owning task runs; this skeleton lands with package P1 and is appended by later packages.

## Slot index

| Slot | Test node | Owning task | State |
|------|-----------|-------------|-------|
| S-00 | `tests/unit/test_validate_decisions.py::test_cli_surface` | T006 (red) / T007 (green) | pending |
| S-01 | `tests/unit/test_validate_decisions.py::test_m01_field_closure_reverse_samples` | T023 | pending |
| S-02 | `tests/contract/test_decision_governance_guards.py::test_m02_locator_red_then_green` | T010 | pending |
| S-03 | `tests/unit/test_validate_decisions.py::test_m03_option_set_reverse_samples` | T018 | pending |
| S-04 | `tests/unit/test_validate_decisions.py::test_m04_id_density_register` | T023 | pending |
| S-05 | `tests/contract/test_decision_governance_guards.py::test_m05_receipt_reverse_samples` | T032 | pending |
| S-06 | `tests/contract/test_decision_governance_guards.py::test_m06_block_completeness` | T032 | pending |
| S-07 | `tests/contract/test_decision_governance_guards.py::test_m06_dispatch_without_block_refused` | T032 | pending |
| S-08 | `tests/contract/test_decision_governance_guards.py::test_m07_chain_three_segments` | T032 | pending |
| S-09 | `tests/contract/test_decision_governance_guards.py::test_m08_registered_variant_red` | T010 | pending |
| S-10 | `tests/contract/test_decision_governance_guards.py::test_broken_pointer_red` (M-09 / C-204) | T024 | pending |
| S-11 | `tests/contract/test_decision_governance_contracts.py::test_full_name_minimum_bar_four_surfaces` (C-102 four-surface) | T009 | pending |
| S-12 | `tests/unit/test_validate_decisions.py::test_ai_replay_deterministic` (C-107 replay) | T018 | pending |
| S-13 | `tests/contract/test_decision_governance_guards.py::test_no_tension_field_copy` (C-205) | T024 | pending |
| S-14 | `tests/contract/test_decision_governance_guards.py::test_legacy_two_digit_reported_legacy` (C-206) | T024 | pending |
| S-15 | `tests/contract/test_decision_governance_guards.py::test_acknowledgement_present` (payload/return snapshots) | T032 | pending |
| S-16 | `tests/contract/test_decision_governance_guards.py::test_silent_redecision_is_anomaly` (payload/return snapshots) | T032 | pending |
| S-17 | `tests/contract/test_decision_governance_guards.py::test_multi_hop_same_id` (chain fixtures) | T032 | pending |
| S-18 | `tests/contract/test_decision_governance_guards.py::test_supersession_preserves_old` (chain fixtures) | T032 | pending |
| S-19 | `tests/contract/test_decision_governance_guards.py::test_reconstruct_from_register_and_carriers` (four-carrier fixtures) | T024 | pending |
| S-20 | `tests/contract/test_decision_governance_guards.py::test_every_guard_has_reverse_sample` (C-403) | T039 | pending |

## Slots

### S-00 — `test_cli_surface` (T006 red → T007 green)

- command (red): `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_cli_surface -q`
- red output: (filled by T006 run)
- exit status (red): (filled by T006 run)
- command (green): `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_cli_surface -q`
- green output: (filled by T007 run)
- exit status (green): (filled by T007 run)

### S-01 — `test_m01_field_closure_reverse_samples` (T023)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_m01_field_closure_reverse_samples -q`
- red output: pending (author lands with T023)
- exit status: pending

### S-02 — `test_m02_locator_red_then_green` (T010)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m02_locator_red_then_green -q`
- red output: pending (author lands with T010; fixtures `tests/fixtures/decision-governance/m02/`)
- exit status: pending

### S-03 — `test_m03_option_set_reverse_samples` (T018)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_m03_option_set_reverse_samples -q`
- red output: pending (author lands with T018; fixtures `tests/fixtures/decision-governance/m03/`)
- exit status: pending

### S-04 — `test_m04_id_density_register` (T023)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_m04_id_density_register -q`
- red output: pending (author lands with T023; fixtures `tests/fixtures/decision-governance/m04/`)
- exit status: pending

### S-05 — `test_m05_receipt_reverse_samples` (T032)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m05_receipt_reverse_samples -q`
- red output: pending (author lands with T032; fixtures `tests/fixtures/decision-governance/m05/`)
- exit status: pending

### S-06 — `test_m06_block_completeness` (T032)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m06_block_completeness -q`
- red output: pending (author lands with T032; fixtures `tests/fixtures/decision-governance/m06/`, `payload/`)
- exit status: pending

### S-07 — `test_m06_dispatch_without_block_refused` (T032)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m06_dispatch_without_block_refused -q`
- red output: pending (author lands with T032; fixtures `tests/fixtures/decision-governance/m06/`, `payload/`)
- exit status: pending

### S-08 — `test_m07_chain_three_segments` (T032)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m07_chain_three_segments -q`
- red output: pending (author lands with T032; fixtures `tests/fixtures/decision-governance/m07/`, `chain/`)
- exit status: pending

### S-09 — `test_m08_registered_variant_red` (T010)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m08_registered_variant_red -q`
- red output: pending (author lands with T010; fixtures `tests/fixtures/decision-governance/m08/` with a stubbed glossary variant)
- exit status: pending

### S-10 — `test_broken_pointer_red` (T024; M-09 / C-204)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_broken_pointer_red -q`
- red output: pending (author lands with T024; fixtures `tests/fixtures/decision-governance/m09/`)
- exit status: pending

### S-11 — `test_full_name_minimum_bar_four_surfaces` (T009; C-102 four-surface)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_contracts.py::test_full_name_minimum_bar_four_surfaces -q`
- red output: pending (author lands with T009; each surface asserted separately)
- exit status: pending

### S-12 — `test_ai_replay_deterministic` (T018; C-107 replay)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_ai_replay_deterministic -q`
- red output: pending (author lands with T018)
- exit status: pending

### S-13 — `test_no_tension_field_copy` (T024; C-205)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_no_tension_field_copy -q`
- red output: pending (author lands with T024)
- exit status: pending

### S-14 — `test_legacy_two_digit_reported_legacy` (T024; C-206)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_legacy_two_digit_reported_legacy -q`
- red output: pending (author lands with T024; fixtures `tests/fixtures/decision-governance/legacy/`)
- exit status: pending

### S-15 — `test_acknowledgement_present` (T032; payload/return snapshots)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_acknowledgement_present -q`
- red output: pending (author lands with T032; fixtures `tests/fixtures/decision-governance/payload/`)
- exit status: pending

### S-16 — `test_silent_redecision_is_anomaly` (T032; payload/return snapshots)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_silent_redecision_is_anomaly -q`
- red output: pending (author lands with T032)
- exit status: pending

### S-17 — `test_multi_hop_same_id` (T032; chain fixtures)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_multi_hop_same_id -q`
- red output: pending (author lands with T032; fixtures `tests/fixtures/decision-governance/chain/`)
- exit status: pending

### S-18 — `test_supersession_preserves_old` (T032; chain fixtures)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_supersession_preserves_old -q`
- red output: pending (author lands with T032; fixtures `tests/fixtures/decision-governance/chain/`)
- exit status: pending

### S-19 — `test_reconstruct_from_register_and_carriers` (T024; four-carrier fixtures)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_reconstruct_from_register_and_carriers -q`
- red output: pending (author lands with T024; fixtures `tests/fixtures/decision-governance/reconstruct/`)
- exit status: pending

### S-20 — `test_every_guard_has_reverse_sample` (T039; C-403)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_every_guard_has_reverse_sample -q`
- red output: pending (author lands with T039)
- exit status: pending
