# Red-first evidence — 107-decision-governance

**Owner of the failing-test baseline name list**: `/speckit.implement` `**Test runs**` (the list is written by the single test entry at `.specify/specs/107-decision-governance/baseline-failed.txt`; it is referenced here, never restated).
**Single test entry**: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh …` (no interpreter-level test command is ever the entry).
**Rule**: one slot per planned red-first test. A slot is filled only with a real command, the real output and the real exit status captured at run time; a slot never carries an estimate. Slots fill as their owning task runs; this skeleton lands with package P1 and is appended by later packages.

## Slot index

| Slot | Test node | Owning task | State |
|------|-----------|-------------|-------|
| S-00 | `tests/unit/test_validate_decisions.py::test_cli_surface` | T006 (red) / T007 (green) | filled |
| S-01 | `tests/unit/test_validate_decisions.py::test_m01_field_closure_reverse_samples` | T023 | filled (red -> green at T029/T031) |
| S-02 | `tests/contract/test_decision_governance_guards.py::test_m02_locator_red_then_green` | T010 | filled (red -> green at T013/T017) |
| S-03 | `tests/unit/test_validate_decisions.py::test_m03_option_set_reverse_samples` | T018 | filled (red -> green at T020/T022) |
| S-04 | `tests/unit/test_validate_decisions.py::test_m04_id_density_register` | T023 | filled (red -> green at T029/T031) |
| S-05 | `tests/contract/test_decision_governance_guards.py::test_m05_receipt_reverse_samples` | T032 | filled (red captured 2026-11-26; green at T038) |
| S-06 | `tests/contract/test_decision_governance_guards.py::test_m06_block_completeness` | T032 | filled (red captured 2026-11-26; green at T038) |
| S-07 | `tests/contract/test_decision_governance_guards.py::test_m06_dispatch_without_block_refused` | T032 | filled (red captured 2026-11-26; green at T038) |
| S-08 | `tests/contract/test_decision_governance_guards.py::test_m07_chain_three_segments` | T032 | filled (red captured 2026-11-26; green at T038) |
| S-09 | `tests/contract/test_decision_governance_guards.py::test_m08_registered_variant_red` | T010 | filled (red -> green at T013/T017) |
| S-10 | `tests/contract/test_decision_governance_guards.py::test_broken_pointer_red` (M-09 / C-204) | T024 | filled (red -> green at T029/T031) |
| S-11 | `tests/contract/test_decision_governance_contracts.py::test_full_name_minimum_bar_four_surfaces` (C-102 four-surface) | T009 | filled (red -> green at T011/T012/T014/T017) |
| S-12 | `tests/unit/test_validate_decisions.py::test_ai_replay_deterministic` (C-107 replay) | T018 | filled (red -> green at T020/T022) |
| S-13 | `tests/contract/test_decision_governance_guards.py::test_no_tension_field_copy` (C-205) | T024 | filled (red -> green at T029/T031) |
| S-14 | `tests/contract/test_decision_governance_guards.py::test_legacy_two_digit_reported_legacy` (C-206) | T024 | filled (red -> green at T029/T031) |
| S-15 | `tests/contract/test_decision_governance_guards.py::test_acknowledgement_present` (payload/return snapshots) | T032 | filled (red captured 2026-11-26; green at T038) |
| S-16 | `tests/contract/test_decision_governance_guards.py::test_silent_redecision_is_anomaly` (payload/return snapshots) | T032 | filled (red captured 2026-11-26; green at T038) |
| S-17 | `tests/contract/test_decision_governance_guards.py::test_multi_hop_same_id` (chain fixtures) | T032 | filled (red captured 2026-11-26; green at T038) |
| S-18 | `tests/contract/test_decision_governance_guards.py::test_supersession_preserves_old` (chain fixtures) | T032 | filled (red captured 2026-11-26; green at T038) |
| S-19 | `tests/contract/test_decision_governance_guards.py::test_reconstruct_from_register_and_carriers` (four-carrier fixtures) | T024 | filled (red -> green at T029/T031) |
| S-20 | `tests/contract/test_decision_governance_guards.py::test_every_guard_has_reverse_sample` (C-403) | T039 | filled (red captured 2026-11-26; green at T045) |
| S-21 | `tests/contract/test_decision_governance_guards.py::test_inventory_closure` (C-406) | T039 | filled (red captured 2026-11-26; green at T045) |
| S-22 | `tests/contract/test_decision_governance_guards.py::test_table_guard_parity` (C-407) | T039 | filled (red captured 2026-11-26; green at T045) |
| S-23 | `tests/contract/test_decision_governance_contracts.py::test_behavior_surfaces_named` (C-402) | T039 | filled (red captured 2026-11-26; green at T045) |
| S-24 | `tests/contract/test_decision_governance_contracts.py::test_gate_neutrality` (C-405) | T039 | filled (red captured 2026-11-26; green at T045) |
| S-25 | `tests/contract/test_decision_governance_contracts.py::test_review_surfaces_named` (C-109) | T039 | filled (red captured 2026-11-26; green at T045) |

## Slots

### S-00 — `test_cli_surface` (T006 red → T007 green)

- command (red): `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_cli_surface -q`
- red output (verbatim tail):

```text
    def test_cli_surface() -> None:
>       assert ENGINE.is_file(), f"missing checker: {ENGINE}"
E       AssertionError: missing checker: /storage/project/cloud-native-ai/spec-kit/.specify/.tmp/sdd-loop/worktrees/decision-governance/scripts/python/validate-decisions.py
E       assert False
tests/unit/test_validate_decisions.py:75: AssertionError
FAILED tests/unit/test_validate_decisions.py::test_cli_surface - AssertionErr...
1 failed in 6.20s
```

- exit status (red): `1` — fails on its own missing-surface assertion, never an import error.
- command (green): `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_cli_surface -q`
- green output (verbatim): `. [100%]` / `1 passed in 6.31s`
- exit status (green): `0`
- interface verification beside the test (T007; manual runs of `python3 scripts/python/validate-decisions.py`):
  - `--action records|payload|chain|inventory` → each exits `2` with `error: action '<a>' is declared but not implemented yet (read-only skeleton)` (an unimplemented check can never read as a pass);
  - `--version` → `validate-decisions.py 0.0.22` (one line, exit 0; version read from `pyproject.toml` at run time — no version literal in the file);
  - `-h` vs `--help` → `cmp` identical (byte-equal help bodies);
  - `--action records --json` → one JSON line `{"action": "records", "status": "not-implemented", "root": "<worktree root>"}` on stdout, message on stderr, exit 2 — the root resolves from the module's own path to the repository root (mirror guard: a directory named `.specify` is never the root).

### S-01 — `test_m01_field_closure_reverse_samples` (T023 red → T029/T031 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_m01_field_closure_reverse_samples -q`
- red output (verbatim tail, captured 2026-11-26 before T029; raw log `test-evidence/us3-red-first.txt`):

```text
>           assert red.returncode == 1, (
                f"{name} exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
            )
E           AssertionError: red-missing-actor.md exited 0, expected 1: PASS: 0 violation(s) (rules: M-02, M-03, M-08)
E           assert 0 == 1
tests/unit/test_validate_decisions.py:281: AssertionError
FAILED tests/unit/test_validate_decisions.py::test_m01_field_closure_reverse_samples
1 failed in 6.76s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the M-01 leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/m01/` — missing base field(`actor`), conditional field missing while `transmission_status: dispatched`, class outside the closed set, malformed `created_at`, a later-phase timepoint on an earlier phase, a placeholder on a `not-transmitted` record; green samples `green-complete.md` / `green-tension-ref.md`.
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us3-green-slots.txt`): `....................... [100%]` / `23 passed in 7.96s`
- exit status (green): `0`. The six M-01 reverse-sample engine verdicts (exit 1 each) are recorded in `notes/us3-green.txt` § SC-005.

### S-02 — `test_m02_locator_red_then_green` (T010 red → T017 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m02_locator_red_then_green -q`
- red output (verbatim tail, captured 2026-11-26 before T013; raw log `test-evidence/us1-red-first.txt`):

```text
E       AssertionError: empty resource_locator exited 2, expected 1: error: action 'records' is declared but not implemented yet (read-only skeleton)
tests/contract/test_decision_governance_guards.py:73: AssertionError
FAILED tests/contract/test_decision_governance_guards.py::test_m02_locator_red_then_green
1 failed in 6.24s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the `records` leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/m02/` — `red-empty-locator.md` (`same_name_conflict: true` + empty `resource_locator`), `red-single-dimension.md` (region id only), `green-complete.md` (business resource group + region id).
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us1-green-slots.txt`):

```text
.                                                                        [100%]
1 passed in 6.58s
```

- exit status (green): `0`. The M-02 red -> green engine verdicts (exit 1 on both red fixtures, exit 0 on the completed locator) are recorded in `notes/us1-green.txt` § SC-002.

### S-03 — `test_m03_option_set_reverse_samples` (T018 red → T020/T022 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_m03_option_set_reverse_samples -q`
- red output (verbatim tail, captured 2026-11-26 before T020; raw log `test-evidence/us2-red-first.txt`):

```text
        for name, needle in red_samples.items():
            path = M03 / name
            assert path.is_file(), f"missing fixture: {path}"
            red = run_records("--carrier", str(path))
>           assert red.returncode == 1, (
                f"{name} exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
            )
E           AssertionError: red-empty-set.md exited 0, expected 1: PASS: 0 violation(s) (rules: M-02, M-08)
E           assert 0 == 1
tests/unit/test_validate_decisions.py:191: AssertionError
FAILED tests/unit/test_validate_decisions.py::test_m03_option_set_reverse_samples
1 failed in 6.23s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the M-03 leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/m03/` — red samples for empty set, duplicate label, `other` without `path`, missing `reversibility`, missing `evidence`, single option without `forced`, declared-count mismatch, chosen option outside the set; green samples `green-complete.md` / `green-single-forced.md`.
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us2-green-slots.txt`): `............ [100%]` / `12 passed in 7.91s`
- exit status (green): `0`. The M-03 reverse-sample engine verdicts (exit 1 on each degenerate form, exit 0 on the completed sets) are recorded in `notes/us2-green.txt` § SC-004.

### S-04 — `test_m04_id_density_register` (T023 red → T029/T031 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_m04_id_density_register -q`
- red output (verbatim tail, captured 2026-11-26 before T029; raw log `test-evidence/us3-red-first.txt`):

```text
>   assert red_form.returncode == 1, (
        f"malformed id exited {red_form.returncode}, expected 1: {red_form.stdout} {red_form.stderr}"
    )
E   AssertionError: malformed id exited 0, expected 1: PASS: 0 violation(s) (rules: M-02, M-03, M-08)
E   assert 0 == 1
tests/unit/test_validate_decisions.py:314: AssertionError
FAILED tests/unit/test_validate_decisions.py::test_m04_id_density_register
1 failed in 6.76s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the M-04 leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/m04/` — `register.md` / `register-missing.md` stubs, `green-dense.md`, `red-form.md` (`D-001-a`), `red-non-dense.md` (`D-001` + `D-003`), `red-unregistered.md`.
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us3-green-slots.txt`): `....................... [100%]` / `23 passed in 7.96s`
- exit status (green): `0`. The M-04 engine verdicts (form / non-dense / unregistered, exit 1 each; green dense set exit 0) are recorded in `notes/us3-green.txt` § SC-005.

### S-05 — `test_m05_receipt_reverse_samples` (T032 red → T038 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m05_receipt_reverse_samples -q`
- red output (verbatim, captured 2026-11-26 in the combined US4 red run before T033/T036; raw log `test-evidence/us4-red-first.txt`):

```text
E       AssertionError: missing H2 section carrying ('传递与实施', 'Transmission and Implementation')
E       assert None is not None
FAILED tests/contract/test_decision_governance_guards.py::test_m05_receipt_reverse_samples
```

- exit status (red): `1` — fails on its own missing-surface assertion (the owner page section and the not-yet-implemented `chain` leg), never an import error.
- fixtures: `tests/fixtures/decision-governance/m05/` — `red-no-receipt.md` (record + dispatch, no receipt), `red-no-id.md` (receipt without `decision_id`), `red-unresolvable.md` (no record segment resolves the receipt id); green chain `chain/green-complete.md`.
- command (green): same single-test command, run as part of the US4 phase run `tests/contract/test_decision_governance_guards.py` on 2026-11-26.
- green output (verbatim tail, raw log `notes/us4-green-slots.txt`): `.............. [100%]` / `14 passed in 6.61s`
- exit status (green): `0`. The US4 SC-006 readings (complete block, refusal, receipt and chain reverse outputs, silent-redecision anomaly, multi-hop, supersession) are recorded in `notes/us4-green.txt` § SC-006.

### S-06 — `test_m06_block_completeness` (T032 red → T038 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m06_block_completeness -q`
- red output (verbatim, captured 2026-11-26 in the combined US4 red run before T033/T036; raw log `test-evidence/us4-red-first.txt`):

```text
E       AssertionError: missing H2 section carrying ('传递与实施', 'Transmission and Implementation')
E       assert None is not None
FAILED tests/contract/test_decision_governance_guards.py::test_m06_block_completeness
```

- exit status (red): `1` — fails on its own missing-surface assertion (the owner page section and the not-yet-implemented `payload` leg), never an import error.
- fixtures: `tests/fixtures/decision-governance/payload/complete.md` (five-field block) and `m06/red-missing-{id,class,chosen,constraints,archive}.md` (one omission each).
- command (green): same single-test command, run as part of the US4 phase run `tests/contract/test_decision_governance_guards.py` on 2026-11-26.
- green output (verbatim tail, raw log `notes/us4-green-slots.txt`): `.............. [100%]` / `14 passed in 6.61s`
- exit status (green): `0`. The US4 SC-006 readings (complete block, refusal, receipt and chain reverse outputs, silent-redecision anomaly, multi-hop, supersession) are recorded in `notes/us4-green.txt` § SC-006.

### S-07 — `test_m06_dispatch_without_block_refused` (T032 red → T038 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m06_dispatch_without_block_refused -q`
- red output (verbatim, captured 2026-11-26 in the combined US4 red run before T036; raw log `test-evidence/us4-red-first.txt`):

```text
E       AssertionError: a decision-backed dispatch without a block exited 2, expected 1:  error: action 'payload' is declared but not implemented yet (read-only skeleton)
E       assert 2 == 1
FAILED tests/contract/test_decision_governance_guards.py::test_m06_dispatch_without_block_refused
```

- exit status (red): `1` — fails on its own missing-surface assertion (the `payload` leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/m06/red-no-block.md` (decision-backed, no block) and `payload/non-decision.md` (BC-02 bridge: legal without a block).
- command (green): same single-test command, run as part of the US4 phase run `tests/contract/test_decision_governance_guards.py` on 2026-11-26.
- green output (verbatim tail, raw log `notes/us4-green-slots.txt`): `.............. [100%]` / `14 passed in 6.61s`
- exit status (green): `0`. The US4 SC-006 readings (complete block, refusal, receipt and chain reverse outputs, silent-redecision anomaly, multi-hop, supersession) are recorded in `notes/us4-green.txt` § SC-006.

### S-08 — `test_m07_chain_three_segments` (T032 red → T038 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m07_chain_three_segments -q`
- red output (verbatim, captured 2026-11-26 in the combined US4 red run before T036; raw log `test-evidence/us4-red-first.txt`):

```text
E       AssertionError: the complete chain exited 2, expected 0:  error: action 'chain' is declared but not implemented yet (read-only skeleton)
E       assert 2 == 0
FAILED tests/contract/test_decision_governance_guards.py::test_m07_chain_three_segments
```

- exit status (red): `1` — fails on its own missing-surface assertion (the `chain` leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/chain/green-complete.md` and `m07/red-missing-{record,dispatch,receipt}.md` plus `m07/red-inconsistent-id.md`.
- command (green): same single-test command, run as part of the US4 phase run `tests/contract/test_decision_governance_guards.py` on 2026-11-26.
- green output (verbatim tail, raw log `notes/us4-green-slots.txt`): `.............. [100%]` / `14 passed in 6.61s`
- exit status (green): `0`. The US4 SC-006 readings (complete block, refusal, receipt and chain reverse outputs, silent-redecision anomaly, multi-hop, supersession) are recorded in `notes/us4-green.txt` § SC-006.

### S-09 — `test_m08_registered_variant_red` (T010 red → T017 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_m08_registered_variant_red -q`
- red output (verbatim tail, captured 2026-11-26 before T013; raw log `test-evidence/us1-red-first.txt`):

```text
E       AssertionError: registered-variant subject exited 2, expected 1:  error: action 'records' is declared but not implemented yet (read-only skeleton)
tests/contract/test_decision_governance_guards.py:121: AssertionError
FAILED tests/contract/test_decision_governance_guards.py::test_m08_registered_variant_red
1 failed in 6.23s
```

- exit status (red): `1` — fails on its own missing-surface assertion, never an import error.
- fixtures: `tests/fixtures/decision-governance/m08/` — `glossary.md` (stubbed variant row), `red-variant.md` (subject uses `spec-kit`), `green-full-name.md` (`Spec Kit`), `green-unregistered.md` (`SK`, unregistered → covered by B-01 only).
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us1-green-slots.txt`):

```text
.                                                                        [100%]
1 passed in 6.27s
```

- exit status (green): `0`. The M-08 red -> green engine verdicts (exit 1 on the variant subject, exit 0 on the full name and on the unregistered abbreviation) are recorded in `notes/us1-green.txt` § SC-002.

### S-10 — `test_broken_pointer_red` (T024 red → T029/T031 green; M-09 / C-204)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_broken_pointer_red -q`
- red output (verbatim tail, captured 2026-11-26 before T029; raw log `test-evidence/us3-red-first.txt`):

```text
>   assert red.returncode == 1, (
        f"a broken pointer exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
    )
E   AssertionError: a broken pointer exited 0, expected 1: PASS: 0 violation(s) (rules: M-02, M-03, M-08)
E   assert 0 == 1
tests/contract/test_decision_governance_guards.py:198: AssertionError
FAILED tests/contract/test_decision_governance_guards.py::test_broken_pointer_red
1 failed in 6.76s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the M-09 leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/m09/` — `green-resolvable.md`, `red-broken.md` (missing carrier path), `red-broken-anchor.md` (missing anchor in an existing carrier).
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us3-green-slots.txt`): `....................... [100%]` / `23 passed in 7.96s`
- exit status (green): `0`. The M-09 engine verdicts (path and anchor variants, exit 1 each; resolvable pair exit 0) are recorded in `notes/us3-green.txt` § SC-005.

### S-11 — `test_full_name_minimum_bar_four_surfaces` (T009 red → T017 green)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_contracts.py::test_full_name_minimum_bar_four_surfaces -q`
- red output (verbatim tail, captured 2026-11-26 before T011/T012/T014; raw log `test-evidence/us1-red-first.txt`):

```text
E       AssertionError: missing H2 section carrying ('决策文本契约', 'Decision Text Contract')
tests/contract/test_decision_governance_contracts.py:107: AssertionError
FAILED tests/contract/test_decision_governance_contracts.py::test_full_name_minimum_bar_four_surfaces
1 failed in 6.24s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the text-contract section does not exist yet), never an import error.
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us1-green-slots.txt`):

```text
.                                                                        [100%]
1 passed in 6.25s
```

- exit status (green): `0`; the four surfaces are asserted separately inside the test (owner page, instruction section, decision-item templates, guard fixtures + named B-01/B-02 review surfaces).

### S-12 — `test_ai_replay_deterministic` (T018 red → T020/T022 green; C-107 replay)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/unit/test_validate_decisions.py::test_ai_replay_deterministic -q`
- red output (verbatim tail, captured 2026-11-26 before T020; raw log `test-evidence/us2-red-first.txt`):

```text
        # The chosen option is a named member of the closed set (M-03 membership leg).
        not_member = run_records("--carrier", str(M03 / "red-chosen-not-member.md"))
>       assert not_member.returncode == 1, (
            f"a chosen option outside the set exited {not_member.returncode}, expected 1: "
            f"{not_member.stdout} {not_member.stderr}"
        )
E       AssertionError: a chosen option outside the set exited 0, expected 1: PASS: 0 violation(s) (rules: M-02, M-08)
E       assert 0 == 1
tests/unit/test_validate_decisions.py:240: AssertionError
FAILED tests/unit/test_validate_decisions.py::test_ai_replay_deterministic
1 failed in 6.23s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the membership leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/m03/ai-replay-green.md` (recorded `predicate: min(downtime_minutes)` + `inputs: plan-a=30; plan-b=45`, chosen `plan-a`), `ai-replay-mismatch.md` (chosen `plan-b`, same inputs), `red-chosen-not-member.md`.
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us2-green-slots.txt`): `............ [100%]` / `12 passed in 7.91s`
- exit status (green): `0`. The replay demonstration (two identical replays, comparison with the recorded choice, and the detectable mismatch) and the membership verdict are recorded in `notes/us2-green.txt` § SC-004.

### S-13 — `test_no_tension_field_copy` (T024 red → T029/T031 green; C-205)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_no_tension_field_copy -q`
- red output (verbatim tail, captured 2026-11-26 before T029; raw log `test-evidence/us3-red-first.txt`):

```text
>   assert red.returncode == 1, (
        f"a copied tension field exited {red.returncode}, expected 1: {red.stdout} {red.stderr}"
    )
E   AssertionError: a copied tension field exited 0, expected 1: PASS: 0 violation(s) (rules: M-02, M-03, M-08)
E   assert 0 == 1
tests/contract/test_decision_governance_guards.py:225: AssertionError
FAILED tests/contract/test_decision_governance_guards.py::test_no_tension_field_copy
1 failed in 6.76s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the layered-closure leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/m01/red-tension-copy.md` (copies `antithesis` / `binding_constraints`), `green-tension-ref.md` (cross-references `T-020` only).
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us3-green-slots.txt`): `....................... [100%]` / `23 passed in 7.96s`
- exit status (green): `0`. The engine verdicts (two out-of-layer field verdicts on the copy; green on the cross-reference) and the owner-page cross-reference duty read are recorded in `notes/us3-green.txt` § SC-005.

### S-14 — `test_legacy_two_digit_reported_legacy` (T024 red → T029/T031 green; C-206)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_legacy_two_digit_reported_legacy -q`
- red output (verbatim tail, captured 2026-11-26 before T029; raw log `test-evidence/us3-red-first.txt`):

```text
    headings = [e for e in payload["legacy"] if e["kind"] == "heading"]
>   KeyError: 'legacy'
tests/contract/test_decision_governance_guards.py:263: KeyError
FAILED tests/contract/test_decision_governance_guards.py::test_legacy_two_digit_reported_legacy
1 failed in 6.76s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the JSON output carries no `legacy` report yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/legacy/` — `legacy.md` (one/two-digit headings, a three-digit heading with zero field lines), `incomplete-new-form.md` (one C-201 field line), `register.md` (legacy rows `D1–D9`, `D-001`, `D-001-a`).
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us3-green-slots.txt`): `....................... [100%]` / `23 passed in 7.96s`
- exit status (green): `0`. The legacy report (three headings + three register rows, never judged) and the incomplete new-form block's M-01 red are recorded in `notes/us3-green.txt` § SC-005.

### S-15 — `test_acknowledgement_present` (T032 red → T038 green; payload/return snapshots)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_acknowledgement_present -q`
- red output (verbatim, captured 2026-11-26 in the combined US4 red run before T033/T035; raw log `test-evidence/us4-red-first.txt`):

```text
E       AssertionError: missing H2 section carrying ('传递与实施', 'Transmission and Implementation')
E       assert None is not None
FAILED tests/contract/test_decision_governance_guards.py::test_acknowledgement_present
```

- exit status (red): `1` — fails on its own missing-surface assertion (the owner page section and the producer duties), never an import error.
- fixtures: `tests/fixtures/decision-governance/payload/returns/return-acknowledged.md` (acknowledgement echoing `D-001` + the four-member receipt).
- command (green): same single-test command, run as part of the US4 phase run `tests/contract/test_decision_governance_guards.py` on 2026-11-26.
- green output (verbatim tail, raw log `notes/us4-green-slots.txt`): `.............. [100%]` / `14 passed in 6.61s`
- exit status (green): `0`. The US4 SC-006 readings (complete block, refusal, receipt and chain reverse outputs, silent-redecision anomaly, multi-hop, supersession) are recorded in `notes/us4-green.txt` § SC-006.

### S-16 — `test_silent_redecision_is_anomaly` (T032 red → T038 green; payload/return snapshots)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_silent_redecision_is_anomaly -q`
- red output (verbatim, captured 2026-11-26 in the combined US4 red run before T033/T036; raw log `test-evidence/us4-red-first.txt`):

```text
E       AssertionError: a silent re-decision exited 2, expected 1:  error: action 'chain' is declared but not implemented yet (read-only skeleton)
E       assert 2 == 1
FAILED tests/contract/test_decision_governance_guards.py::test_silent_redecision_is_anomaly
```

- exit status (red): `1` — fails on its own missing-surface assertion (the `chain` leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/chain/red-silent-redecision.md` (receipt claims completion under `D-002`) and `payload/returns/return-escalated.md` (the correct explicit-anomaly form: no receipt, `ANOMALY:` line).
- command (green): same single-test command, run as part of the US4 phase run `tests/contract/test_decision_governance_guards.py` on 2026-11-26.
- green output (verbatim tail, raw log `notes/us4-green-slots.txt`): `.............. [100%]` / `14 passed in 6.61s`
- exit status (green): `0`. The US4 SC-006 readings (complete block, refusal, receipt and chain reverse outputs, silent-redecision anomaly, multi-hop, supersession) are recorded in `notes/us4-green.txt` § SC-006.

### S-17 — `test_multi_hop_same_id` (T032 red → T038 green; chain fixtures)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_multi_hop_same_id -q`
- red output (verbatim, captured 2026-11-26 in the combined US4 red run before T036; raw log `test-evidence/us4-red-first.txt`):

```text
E       AssertionError: the multi-hop chain exited 2, expected 0:  error: action 'chain' is declared but not implemented yet (read-only skeleton)
E       assert 2 == 0
FAILED tests/contract/test_decision_governance_guards.py::test_multi_hop_same_id
```

- exit status (red): `1` — fails on its own missing-surface assertion (the `chain` leg does not exist yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/chain/multi-hop-green.md` (two hops, five `D-001` references) and `chain/red-multi-hop-id.md` (hop 2 switches to `D-002`).
- command (green): same single-test command, run as part of the US4 phase run `tests/contract/test_decision_governance_guards.py` on 2026-11-26.
- green output (verbatim tail, raw log `notes/us4-green-slots.txt`): `.............. [100%]` / `14 passed in 6.61s`
- exit status (green): `0`. The US4 SC-006 readings (complete block, refusal, receipt and chain reverse outputs, silent-redecision anomaly, multi-hop, supersession) are recorded in `notes/us4-green.txt` § SC-006.

### S-18 — `test_supersession_preserves_old` (T032 red → T038 green; chain fixtures)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_supersession_preserves_old -q`
- red output (verbatim, captured 2026-11-26 in the combined US4 red run before T033; raw log `test-evidence/us4-red-first.txt`):

```text
E       AssertionError: missing H2 section carrying ('传递与实施', 'Transmission and Implementation')
E       assert None is not None
FAILED tests/contract/test_decision_governance_guards.py::test_supersession_preserves_old
```

- exit status (red): `1` — fails on its own missing-surface assertion (the owner page section), never an import error.
- fixtures: `tests/fixtures/decision-governance/chain/carriers/redecision.md` (old `D-001` with `superseded_by: D-002` + receipt state, new `D-002`), `carriers/redecision-lossy.md` (the old record rewritten and its `implemented_at` lost), `carriers/register.md`.
- command (green): same single-test command, run as part of the US4 phase run `tests/contract/test_decision_governance_guards.py` on 2026-11-26.
- green output (verbatim tail, raw log `notes/us4-green-slots.txt`): `.............. [100%]` / `14 passed in 6.61s`
- exit status (green): `0`. The US4 SC-006 readings (complete block, refusal, receipt and chain reverse outputs, silent-redecision anomaly, multi-hop, supersession) are recorded in `notes/us4-green.txt` § SC-006.

### S-19 — `test_reconstruct_from_register_and_carriers` (T024 red → T029/T031 green; four-carrier fixtures)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_reconstruct_from_register_and_carriers -q`
- red output (verbatim tail, captured 2026-11-26 before T029; raw log `test-evidence/us3-red-first.txt`):

```text
    records = payload["records"]
>   KeyError: 'records'
tests/contract/test_decision_governance_guards.py:301: KeyError
FAILED tests/contract/test_decision_governance_guards.py::test_reconstruct_from_register_and_carriers
1 failed in 6.76s
```

- exit status (red): `1` — fails on its own missing-surface assertion (the JSON output carries no reconstructed-records array yet), never an import error.
- fixtures: `tests/fixtures/decision-governance/reconstruct/` — one complete record per carrier (`requirements.md`, `plan.md`, `checkpoints/02-implement.md`, `run-report.md`) plus a register stub; the requirements carrier triggers the same-name conditional family.
- command (green): same single-test command.
- green output (verbatim tail, captured 2026-11-26; raw log `test-evidence/us3-green-slots.txt`): `....................... [100%]` / `23 passed in 7.96s`
- exit status (green): `0`. The four-record reconstruction output (ids, carriers, classes, base fields, triggered family) is recorded in `notes/us3-green.txt` § SC-005.

### S-20 — `test_every_guard_has_reverse_sample` (T039 red → T045 green; C-403)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_every_guard_has_reverse_sample -q`
- red output (verbatim, captured 2026-11-26 in the combined US5 red run before T040; raw log `test-evidence/us5-red-first.txt`):

```text
E       AssertionError: missing H2 section carrying ('强制边界', 'Enforcement Boundary')
E       assert None is not None
FAILED tests/contract/test_decision_governance_guards.py::test_every_guard_has_reverse_sample
```

- exit status (red): `1` — fails on its own missing-surface assertion (the owner page declares no reverse-sample table yet), never an import error.
- fixtures: the nine roster samples — `m01/red-missing-actor.md`, `m02/red-empty-locator.md`, `m03/red-empty-set.md`, `m04/red-form.md`, `m05/red-no-id.md`, `m06/red-no-block.md`, `m07/red-missing-dispatch.md`, `m08/red-variant.md`, `m09/red-broken.md`.
- command (green): same single-test command; output and exit status recorded at T045 in `notes/us5-green.txt`.

### S-21 — `test_inventory_closure` (T039 red → T045 green; C-406)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_inventory_closure -q`
- red output (verbatim, captured 2026-11-26 in the combined US5 red run before T042; raw log `test-evidence/us5-red-first.txt`):

```text
E       AssertionError: the inventory action exited 2, expected 0:  error: action 'inventory' is declared but not implemented yet (read-only skeleton)
E       assert 2 == 0
FAILED tests/contract/test_decision_governance_guards.py::test_inventory_closure
```

- exit status (red): `1` — fails on its own missing-surface assertion (the `inventory` leg does not exist yet), never an import error.
- observation: the test runs the documented code-face scan (grep for the owner-page path over `templates/ skills/ agents/ scripts/ src/`, recorded in the checker docstring) and feeds the output to the action; mutations add an unregistered face and remove a declared producer's owner face.
- command (green): same single-test command; output and exit status recorded at T045 in `notes/us5-green.txt`.

### S-22 — `test_table_guard_parity` (T039 red → T045 green; C-407)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_guards.py::test_table_guard_parity -q`
- red output (verbatim, captured 2026-11-26 in the combined US5 red run before T040; raw log `test-evidence/us5-red-first.txt`):

```text
E       AssertionError: missing H2 section carrying ('强制边界', 'Enforcement Boundary')
E       assert None is not None
FAILED tests/contract/test_decision_governance_guards.py::test_table_guard_parity
```

- exit status (red): `1` — fails on its own missing-surface assertion (the owner page carries no M/B tables yet), never an import error.
- comparison unit: the owner page's M/B table row sets against the test-side `GUARD_ROSTER` / `B_RULES`, plus each M row's single judge action against the roster's action.
- command (green): same single-test command; output and exit status recorded at T045 in `notes/us5-green.txt`.

### S-23 — `test_behavior_surfaces_named` (T039 red → T045 green; C-402)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_contracts.py::test_behavior_surfaces_named -q`
- red output (verbatim, captured 2026-11-26 in the combined US5 red run before T040; raw log `test-evidence/us5-red-first.txt`):

```text
E       AssertionError: missing H2 section carrying ('强制边界', 'Enforcement Boundary')
E       assert None is not None
FAILED tests/contract/test_decision_governance_contracts.py::test_behavior_surfaces_named
```

- exit status (red): `1` — fails on its own missing-surface assertion (the B table does not exist yet), never an import error.
- comparison unit: each B row's surface cell and its explicit no-machine-coverage statement; the M table's complementary machine-coverage claim; the guards module quotes no behavior rule id.
- command (green): same single-test command; output and exit status recorded at T045 in `notes/us5-green.txt`.

### S-24 — `test_gate_neutrality` (T039 red → T045 green; C-405)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_contracts.py::test_gate_neutrality -q`
- red output (verbatim, captured 2026-11-26 in the combined US5 red run before T043; raw log `test-evidence/us5-red-first.txt`):

```text
E       AssertionError: missing file: …/.specify/specs/107-decision-governance/test-evidence/gate-neutrality.txt
E       assert False
FAILED tests/contract/test_decision_governance_contracts.py::test_gate_neutrality
```

- exit status (red): `1` — fails on its own missing-surface assertion (the re-baselined gate record does not exist yet), never an import error.
- comparison unit: the live scan summary against the recorded effective baseline (re-baselined 31 → 30 on the merged tree), the touched-face hit membership, the FR-025 three-path containment against `fbab7a45c`, and the EP-002 payload field counts.
- command (green): same single-test command; output and exit status recorded at T045 in `notes/us5-green.txt`.

### S-25 — `test_review_surfaces_named` (T039 red → T045 green; C-109)

- command: `SPECKIT_PYTHON=/usr/local/bin/python3 bash scripts/bash/run-tests.sh tests/contract/test_decision_governance_contracts.py::test_review_surfaces_named -q`
- red output (verbatim, captured 2026-11-26 in the combined US5 red run before T040; raw log `test-evidence/us5-red-first.txt`):

```text
E       AssertionError: missing H2 section carrying ('强制边界', 'Enforcement Boundary')
E       assert None is not None
FAILED tests/contract/test_decision_governance_contracts.py::test_review_surfaces_named
```

- exit status (red): `1` — fails on its own missing-surface assertion (the B rows and the producer-side review-surface pointers do not exist yet), never an import error.
- comparison unit: B-03/B-04/B-06 surfaces in the owner tables and § Decision Classes, plus the analyze/review skill pointer blocks.
- command (green): same single-test command; output and exit status recorded at T045 in `notes/us5-green.txt`.
