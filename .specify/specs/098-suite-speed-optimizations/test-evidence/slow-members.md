# Slow marker membership registry

Owner of the membership propositions: `contracts/slow-membership.contract.md` (C-002…C-004).
This file is the single data carrier; the guard `tests/contract/test_suite_tier_contract.py`
asserts it corresponds one-to-one with `pytest --collect-only -q -m slow` (C-005) and that no
other evidence file restates the table (C-009). Counts are derived at guard time — never
written here. Measurement run: `test-evidence/slow-members-measurement.txt`.

| test_id | category | reason | date |
|---|---|---|---|
| tests/contract/test_clause_coverage.py::test_c10_openapi_clauses_are_method_keys_and_the_total_matches_the_census | corpus-scan | spawns the accountant over the real .specify/specs corpus; measured 10.44 s / 10.06 s | 2026-11-10 |
| tests/contract/test_clause_coverage.py::test_c20_the_accountant_writes_nothing_and_changes_no_byte_of_the_corpus | corpus-scan | hashes every file under .specify/specs and runs the accountant over the same corpus; measured 10.57 s / 10.29 s | 2026-11-10 |
| tests/contract/test_clause_coverage.py::test_c26_every_yaml_contract_is_explicitly_disposed | corpus-scan | spawns the accountant over the real .specify/specs corpus; measured 10.02 s / 10.24 s | 2026-11-10 |
| tests/contract/test_clause_coverage.py::test_c27_the_sc006_evidence_form_is_three_numbers_and_a_sum_assertion | corpus-scan | spawns the accountant over the real .specify/specs corpus; measured 10.15 s / 9.89 s | 2026-11-10 |
| tests/contract/test_clause_coverage.py::test_form_exit_code_table | corpus-scan | runs the accountant in-process over the real .specify/specs corpus; measured 9.86 s / 10.00 s | 2026-11-10 |
| tests/integration/test_sdd_loop_efficiency_runner.py::test_local_nohup_survives_parent_exit | process-boundary | spawns the detached stage-runner under nohup and waits for its status file to outlive the parent shell; measured 6.21 s / 6.21 s | 2026-11-10 |
| tests/integration/test_session_kill_reattach.py::test_delivered_runner_recipe_survives_driver_kill_and_reattaches | process-boundary | spawns the delivered run-stage.sh recipe, SIGHUPs the driver group and waits on heartbeat/status events; measured 1.59 s / 1.60 s | 2026-11-10 |
