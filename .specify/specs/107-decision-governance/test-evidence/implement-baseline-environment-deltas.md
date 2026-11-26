# Baseline environment deltas (worktree vs trunk) — 107 implement

The 107 implement runs in the git worktree `.specify/.tmp/sdd-loop/worktrees/decision-governance`. Its baseline full suite (221 failed / 10152 passed) contains five failures that are worktree-environment artifacts, each reproduced individually (not parallel flakes) and each expected to pass on the trunk where the branch is merged:

1. `tests/contract/test_ask_record_repeat.py::test_canonical_engine_does_not_self_resolve_to_the_framework_repo` — path-resolution guard tuned for a normal checkout (worktree `.git` is a file).
2. `tests/contract/test_docs_command_template.py::test_c10_runtime_copies_exist_for_every_present_tool` — runtime-copy presence resolution in the worktree.
3. `tests/contract/test_execution_config_engine.py::TestErrorsAndWarnings::test_warning_surface_is_json_and_stderr` — execution-config default resolution in the worktree.
4. `tests/contract/test_settlement_preservation.py::test_test_budget_keeps_one_baseline_and_at_most_one_closure_slot` — reads the state spine from the main repo path.
5. `tests/integration/test_trigger_telemetry.py::test_cli_subprocess_smoke_pins_payload_and_exit_semantics` — CLI subprocess root resolution in the worktree.

Trunk baseline (merge target) remains 217 failed names; at integration the branch is rebased/merged and the closure gate runs on the trunk environment.
