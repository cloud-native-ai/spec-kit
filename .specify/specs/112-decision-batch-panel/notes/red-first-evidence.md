# Red-first evidence — 112-decision-batch-panel

Owner of the red-first form: this file. Each slot records the **command**, the **real output** (decisive excerpt; full logs below where captured) and the **exit status**. The failing-test baseline **name list** is captured by `/speckit.implement`'s `**Test runs**` owner (`--names-out`) into `notes/red-first-names.txt` and is **referenced** here, never restated.

- Test entry (only entry): `bash scripts/bash/run-tests.sh` with `SPECKIT_PYTHON=/usr/local/bin/python3` (the runner's interpreter ladder resolved a pytest-capable interpreter; the bare `python3` on PATH is `profiles/.venv` without pytest — recorded in § Environment Prerequisites of `tasks.md`).
- Red-first rule: each test MUST fail on its own missing behaviour, never on an import error. The engine module imports cleanly from package P1 on (T006 skeleton); every red run below is an assertion/behaviour failure.
- Status vocabulary: `pending` (slot not yet executed; owning package named) · `red` (executed, failing as intended) · `green` (executed, passing — only after the owning implementation row).

## S1 — Engine interface (C-608 / T005; green at T006, formal clause green T045)

| Slot | Test | Fixture | Command | Run @ 2026-11-27 | rc |
|------|------|---------|---------|------------------|----|
| R-608 | `tests/contract/test_decision_batch_contract.py::test_engine_interface_contract` | none (repo tree) | `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_batch_contract.py::test_engine_interface_contract -q` | **red** (T005): `AssertionError: missing engine: scripts/python/decision-batch.py`; `1 failed in 6.77s`. **green** (T006): `1 passed in 6.63s` | 1 → 0 |

## S2 — US1 scan and presentation legs (T013/T014; green at T023)

All 21 unit tests + 3 contract tests were executed as one red run (command in § Executed runs S2); each fails on its own missing behaviour (the scan core lands with T019…T021, the § Pending Item Block owner section with T016), never on an import error.

| Slot | Test (`tests/unit/test_decision_batch_engine.py::`) | Fixture under `tests/fixtures/decision-batch/` | Run @ 2026-11-27 | rc |
|------|------------------------------------------------------|-----------------------------------------------|------------------|----|
| R-S01 | `test_roster_closed_and_predicates` | `two-source` | red — scan unimplemented | 1 |
| R-S02 | `test_incomplete_block_still_candidate` | `incomplete-block` | red — scan unimplemented | 1 |
| R-S03 | `test_identity_byte_equal_and_merge` | `two-source` | red — scan unimplemented | 1 |
| R-S04 | `test_origin_linkage_states` | `two-source`, `incomplete-block` | red — scan unimplemented | 1 |
| R-S05 | `test_class_gate_states` | `autonomous`, `class-conflict` | red — scan unimplemented | 1 |
| R-S06 | `test_already_resolved_read_time_join` | `resolution-join` | red — scan unimplemented | 1 |
| R-S07 | `test_named_exclusions_counted` | `two-source` | red — scan unimplemented | 1 |
| R-S08 | `test_source_presence_levels` | `absent-root`, `unreadable-register` | red — scan unimplemented | 1 |
| R-S09 | `test_scan_zero_write` | `two-source` | red — scan unimplemented | 1 |
| R-S10 | `test_presentation_order_deterministic` | `two-source` | red — scan unimplemented | 1 |
| R-S11 | `test_row_slots_incomplete_named` | `incomplete-block` | red — scan unimplemented | 1 |
| R-S12 | `test_batch_context_floor` | `two-source` | red — scan unimplemented | 1 |
| R-S13 | `test_no_truncation_all_rows` | `two-source` | red — scan unimplemented | 1 |
| R-S14 | `test_scan_twice_field_identical` | `two-source` | red — scan unimplemented | 1 |
| R-S15 | `test_autonomous_presented_zero` | `autonomous` | red — scan unimplemented | 1 |
| R-S16 | `test_default_is_declared_member` | `two-source` | red — scan unimplemented | 1 |
| R-S17 | `test_no_default_presented_not_settled` | `incomplete-block` | red — scan unimplemented | 1 |
| R-S18 | `test_grounding_join_closed_inputs` | `grounding-grounded` | red — scan unimplemented | 1 |
| R-S19 | `test_grounded_pointers_all_resolve` | `grounding-grounded` | red — scan unimplemented | 1 |
| R-S20 | `test_no_evidence_explicit` | `grounding-none` | red — scan unimplemented | 1 |
| R-S21 | `test_prior_conflict_detected` | `prior-conflict` | red — scan unimplemented | 1 |
| R-C103 | `tests/contract/test_decision_batch_contract.py::test_block_grammar_owner_extension` | owner page § 待决策项块 (T016) | red — the owner section does not exist yet | 1 |
| R-C204 | `tests/contract/test_decision_batch_contract.py::test_presentation_identifier_boundary` | `two-source` | red — `scan --format text` exits 2 (unimplemented) | 1 |
| R-C307 | `tests/contract/test_decision_batch_contract.py::test_skill_does_not_recompute` | `skills/internal/decide-batch/SKILL.md` (T009) | **green at authoring** — the skill predates this row in package order; disclosed, not claimed as red-first | 0 |

## S3 — US2 record legs (T024, 12 tests; green at T032) and contract (T025)

| Slot | Test | Fixture | Run @ 2026-11-27 | rc |
|------|------|---------|------------------|----|
| R-R01 | `test_reply_forms_and_abort_zero_records` | `reply-shapes` | pending — package P2 | — |
| R-R02 | `test_objection_binds_identity_verbatim` | `reply-shapes` | pending — package P2 | — |
| R-R03 | `test_reply_membership_refusals` | `reply-shapes` | pending — package P2 | — |
| R-R04 | `test_silence_eligibility_matrix` | `eligibility-matrix` | pending — package P2 | — |
| R-R05 | `test_park_no_record_stays_pending` | `eligibility-matrix` | pending — package P2 | — |
| R-R06 | `test_unattended_and_missing_authorization_refused` | `eligibility-matrix` | pending — package P2 | — |
| R-R07 | `test_ineligible_explicit_settlement` | `eligibility-matrix` | pending — package P2 | — |
| R-R08 | `test_no_cross_batch_preauthorization` | `drift` | pending — package P2 | — |
| R-R09 | `test_record_drift_refused_zero_write` | `drift` | pending — package P2 | — |
| R-R10 | `test_batch_id_shape_and_duplicate_refusal` | `batch-family` | pending — package P2 | — |
| R-R11 | `test_batch_record_layout_via_memory_engine` | `batch-family` | pending — package P2 | — |
| R-R12 | `test_decision_record_batch_family` | `batch-family` | pending — package P2 | — |
| R-C408 | `tests/contract/test_decision_batch_contract.py::test_signal_mapping_pointer_only` | owner page + confirmation-gates pointer | pending — package P2 | — |

## S4 — US3 replay legs (T033, 5 tests + absent-register case; green at T039)

| Slot | Test | Fixture | Run @ 2026-11-27 | rc |
|------|------|---------|------------------|----|
| R-P01 | `test_register_registration_and_status_update` | `register-updates` | pending — package P3 | — |
| R-P02 | `test_resolution_annotation_and_disclosure` | `register-updates` | pending — package P3 | — |
| R-P03 | `test_two_batches_distinct_paths` | `concurrency` | pending — package P3 | — |
| R-P04 | `test_replay_from_record_only` | `replay-broken` | pending — package P3 | — |
| R-P05 | `test_replay_broken_pointer_nonzero` | `replay-broken` | pending — package P3 | — |
| R-P06 | `test_absent_register_creation` | `register-absent` | pending — package P3 | — |

## S5 — US4 completeness legs (T040, 6 tests; green at T045) and ordered guards (T042)

| Slot | Test | Fixture | Run @ 2026-11-27 | rc |
|------|------|---------|------------------|----|
| R-K01 | `test_completeness_claim_shape` | `two-source` | pending — package P3 | — |
| R-K02 | `test_bookkeeping_identity_holds` | `two-source` | pending — package P3 | — |
| R-K03 | `test_absent_source_named_not_clean` | `absent-root` | pending — package P3 | — |
| R-K04 | `test_nothing_pending_success_no_record` | `empty-project` | pending — package P3 | — |
| R-K05 | `test_unclassifiable_candidate_refused` | `incomplete-block` | pending — package P3 | — |
| R-K06 | `test_no_partial_complete_claim` | `two-source` | pending — package P3 | — |
| R-K07 | `test_unreadable_source_refusal` (ordered guard — subject T019 predates it) | `unreadable-register` | pending — package P3 | — |
| R-K08 | `test_batch_head_completeness` (ordered guard — subject T030 predates it) | `batch-family` | pending — package P3 | — |

## S6 — US5 supersession legs (T046, 2 tests; green at T052) and contract (T047)

| Slot | Test | Fixture | Run @ 2026-11-27 | rc |
|------|------|---------|------------------|----|
| R-X01 | `test_supersession_append_only` | `prior-conflict` | pending — package P4 | — |
| R-X02 | `test_supersession_unwritable_prior_refused` | `unwritable-old-record` | pending — package P4 | — |
| R-C509 | `tests/contract/test_decision_batch_contract.py::test_transmission_reuses_107_chain` | owner page + 107 chain | pending — package P4 | — |
| R-C511 | `tests/contract/test_decision_batch_contract.py::test_owner_extension_single_owner` | owner page + probe + command/skill | pending — package P4 | — |
| R-C512 | `tests/contract/test_decision_batch_contract.py::test_red_lines_and_boundary` | engine + skill + knowledge store | pending — package P4 | — |
| R-C208 | `tests/contract/test_decision_batch_contract.py::test_behavior_surfaces_named` | owner page B rows | pending — package P4 | — |

## S7 — M-10…M-16 reverse samples (T049; executed red at T052)

| Slot | Rule | Reverse sample (under `tests/fixtures/decision-batch/`) | Run @ 2026-11-27 | rc |
|------|------|--------------------------------------------------------|------------------|----|
| R-M10 | M-10 roster/candidate/exclusions/presence | `m10/` | pending — package P4 | — |
| R-M11 | M-11 block grammar/identity/linkage/class/resolution | `m11/` | pending — package P4 | — |
| R-M12 | M-12 ordering/rows/determinism/autonomous zero | `m12/` | pending — package P4 | — |
| R-M13 | M-13 default/grounding/prior conflict | `m13/` | pending — package P4 | — |
| R-M14 | M-14 membership/silence/authorization/zero-write | `m14/` | pending — package P4 | — |
| R-M15 | M-15 batch id/record/fields/register/idempotency | `m15/` | pending — package P4 | — |
| R-M16 | M-16 replay determinism/pointer resolution | `m16/` | pending — package P4 | — |

## Failing-test name list

Captured by `/speckit.implement`'s `**Test runs**` owner at red-run time: `notes/red-first-names.txt` (sorted, de-duplicated FAILED ids, produced with the runner's `--names-out`). This file references that artifact instead of restating the list.

## Executed runs (append-only)

### R-608 — red at T005 (2026-11-27)

Command (exact):
```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_decision_batch_contract.py::test_engine_interface_contract -q \
  --names-out .specify/specs/112-decision-batch-panel/notes/red-first-names.txt
```
Exit status: **1**. Decisive output:
```text
E       AssertionError: missing engine: scripts/python/decision-batch.py
FAILED tests/contract/test_decision_batch_contract.py::test_engine_interface_contract
1 failed in 6.77s
# failed-name list written: .specify/specs/112-decision-batch-panel/notes/red-first-names.txt (1 entries) passes=1
```
The failure is an assertion on the missing engine, not an import error.

### R-608 — green at T006 (2026-11-27)

Command: same selection without `--names-out`. Exit status: **0**. Decisive output:
```text
.                                                                        [100%]
1 passed in 6.63s
```
Direct interface probes on the skeleton: `--help`/`-h` identical (exit 0); `--version` → `decision-batch.py 0.0.22` (entry and every action); `--bogus` → `error: unrecognized option: --bogus` (exit 2); `scan` → declared-but-unimplemented message (exit 2, no writes).
### S2 — US1 red run at T013/T014 (2026-11-27)

Command (exact):
```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py -q \
  --names-out .specify/specs/112-decision-batch-panel/notes/red-first-names.txt
```
Exit status: **1**. Decisive output:
```text
23 failed, 2 passed in 7.69s
# failed-name list written: .specify/specs/112-decision-batch-panel/notes/red-first-names.txt (23 entries) passes=1
AssertionError: scan exited 2 (expected 0): decision-batch.py: action 'scan' is declared but not implemented ...
```
The 23 failing ids are recorded in `notes/red-first-names.txt` (the list owner named in § Failing-test name list); the two passing tests are R-608 (`test_engine_interface_contract`, green since T006) and R-C307 (`test_skill_does_not_recompute`, its subject T009 predates T014 — disclosed).

### T015 owner-page roster — verification (2026-11-27)

Not a test row; the roster section is verified by its presence and by the governance suites staying green: `tests/contract/test_decision_governance_contracts.py` + `test_decision_governance_guards.py` → `34 passed in 9.46s` (rc 0), gate scanner still `30 blocking / 0 violations`, mirrors `--check` rc 0.
