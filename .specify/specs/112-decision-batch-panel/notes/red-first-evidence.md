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
| R-S01 | `test_roster_closed_and_predicates` | `two-source` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S02 | `test_incomplete_block_still_candidate` | `incomplete-block` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S03 | `test_identity_byte_equal_and_merge` | `two-source` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S04 | `test_origin_linkage_states` | `two-source`, `incomplete-block` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S05 | `test_class_gate_states` | `autonomous`, `class-conflict` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S06 | `test_already_resolved_read_time_join` | `resolution-join` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S07 | `test_named_exclusions_counted` | `two-source` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S08 | `test_source_presence_levels` | `absent-root`, `unreadable-register` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S09 | `test_scan_zero_write` | `two-source` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S10 | `test_presentation_order_deterministic` | `two-source` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S11 | `test_row_slots_incomplete_named` | `incomplete-block` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S12 | `test_batch_context_floor` | `two-source` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S13 | `test_no_truncation_all_rows` | `two-source` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S14 | `test_scan_twice_field_identical` | `two-source` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S15 | `test_autonomous_presented_zero` | `autonomous` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S16 | `test_default_is_declared_member` | `two-source` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S17 | `test_no_default_presented_not_settled` | `incomplete-block` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S18 | `test_grounding_join_closed_inputs` | `grounding-grounded` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S19 | `test_grounded_pointers_all_resolve` | `grounding-grounded` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S20 | `test_no_evidence_explicit` | `grounding-none` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-S21 | `test_prior_conflict_detected` | `prior-conflict` | red at T013 (`scan exited 2`, unimplemented) → **green at T023** | 1 → 0 |
| R-C103 | `tests/contract/test_decision_batch_contract.py::test_block_grammar_owner_extension` | owner page § 待决策项块 (T016) | red at T014 (owner section absent) → **green at T023** (section landed in T016) | 1 → 0 |
| R-C204 | `tests/contract/test_decision_batch_contract.py::test_presentation_identifier_boundary` | `two-source` | red at T014 (`scan --format text` exit 2) → **green at T023** | 1 → 0 |
| R-C307 | `tests/contract/test_decision_batch_contract.py::test_skill_does_not_recompute` | `skills/internal/decide-batch/SKILL.md` (T009) | **green at authoring** — the skill predates this row in package order; disclosed, not claimed as red-first | 0 |

## S3 — US2 record legs (T024, 12 tests; green at T032) and contract (T025)

| Slot | Test | Fixture | Run @ 2026-11-27 | rc |
|------|------|---------|------------------|----|
| R-R01 | `test_reply_forms_and_abort_zero_records` | `reply-shapes` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R02 | `test_objection_binds_identity_verbatim` | `reply-shapes` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R03 | `test_reply_membership_refusals` | `reply-shapes` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R04 | `test_silence_eligibility_matrix` | `eligibility-matrix` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R05 | `test_park_no_record_stays_pending` | `eligibility-matrix` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R06 | `test_unattended_and_missing_authorization_refused` | `eligibility-matrix` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R07 | `test_ineligible_explicit_settlement` | `eligibility-matrix` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R08 | `test_no_cross_batch_preauthorization` | `drift` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R09 | `test_record_drift_refused_zero_write` | `drift` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R10 | `test_batch_id_shape_and_duplicate_refusal` | `batch-family` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R11 | `test_batch_record_layout_via_memory_engine` | `batch-family` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-R12 | `test_decision_record_batch_family` | `batch-family` | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |
| R-C408 | `tests/contract/test_decision_batch_contract.py::test_signal_mapping_pointer_only` | owner page + confirmation-gates pointer | red at T024 (record unimplemented, exit 2) → **green after T029/T030** (formal green claim at T032) | 1 → 0 |

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

### T016–T018 owner-page sections + T019–T021 scan core — verification (2026-11-27)

Not separate test rows; verified through the S2/T023 green run below plus the 107 governance suites: `tests/contract/test_decision_governance_contracts.py` + `test_decision_governance_guards.py` → `34 passed` (rc 0), gate scanner still `30 blocking / 0 violations`.

### S2 — US1 green run at T023 (2026-11-27)

Command (exact):
```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py -q
```
Exit status: **0**. Decisive output:
```text
25 passed in 7.30s
```
Full evidence: `notes/us1-green.txt` (mirror pair readings, two-scan equality, grounding/prior-conflict payloads, bookkeeping identity, the 17-row real-tree reading). No anomaly in the run.

### T022 — mirror pairs (2026-11-27)

`sync-mirrors.py --write` projected `shared/definitions/decision-definitions.md` and `scripts/python/decision-batch.py`; `--check` → `ok shared/ == .specify/shared/ (123 files, byte-identical)` rc 0; both `cmp` pairs byte-identical.

### S3 — US2 red run at T024/T025 (2026-11-27)

Command (exact):
```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/unit/test_decision_batch_engine.py -q \
  --names-out .specify/specs/112-decision-batch-panel/notes/red-first-names-us2.txt
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/contract/test_decision_batch_contract.py -q \
  --names-out .specify/specs/112-decision-batch-panel/notes/red-first-names-us2-contract.txt
```
Exit status: **1 / 1**. Decisive output:
```text
12 failed, 21 passed        # the 12 US2 unit tests failed on the unimplemented record action
1 failed, 4 passed          # test_signal_mapping_pointer_only: the § 批次处置 section was absent
```
Failure signatures are behaviour assertions (`an empty reply exited 2, expected 1`, `missing H2
section carrying ('批次处置', 'Batch Disposition')`), never import errors. The failing ids are
recorded in `notes/red-first-names-us2.txt` and `notes/red-first-names-us2-contract.txt`.

### US2 implementation — post-implementation run (2026-11-27; formal green claim at T032)

After T026–T030 landed (owner-page reply/disposition/record sections, the record action, and the
validator's batch-family closure):

```bash
SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh \
  tests/unit/test_decision_batch_engine.py tests/contract/test_decision_batch_contract.py \
  tests/contract/test_decision_governance_contracts.py tests/contract/test_decision_governance_guards.py \
  tests/unit/test_validate_decisions.py -q
→ 44 passed (rc 0)
```
This run is recorded as package evidence; the clause green points for C-401…C-409 and C-501…C-504 stay
with T032's verification row.

### T022/T031 boundary — mirror projections (2026-11-27)

US1 pairs synced and compared at T022 (see § S2). After the US2 edits the same projection ran again
(`sync-mirrors.py --write` → `sync scripts/ -> .specify/scripts/ (2 files)`, `sync shared/ -> .specify/shared/ (1 files)`; `--check` rc 0; `cmp` byte-identical for the owner page, the batch engine and the validator). The formal T031 verification row (cmp set + validator-over-fixture run) remains open for package P3.
