# Code Review Report — 代码段 (code segment)

| 属性 | 值 |
|------|-----|
| **分支** | `098-suite-speed-optimizations` |
| **基准** | `b3da3a26dfba209057f65c2b17962b9516812c39` (`b3da3a26d`) |
| **目标** | `f129eb8019ac11bef74c3931271a0aec4d6d145b` (`f129eb801`) |
| **基准来源** | `feature-first-commit` |
| **渲染模式** | `renderer: text` |
| **Reviewer** | `Qiming Liu (John)` |
| **日期** | `2026-11-10T18:55:47Z` |

## 变更概览

```
 .specify/constitution.md                           |   16 +-
 .specify/features.md                               |    4 +-
 .specify/features/086-efficient-test-execution.md  |   12 +-
 .specify/glossary.md                               |    2 +
 .specify/register.md                               |   10 +
 .specify/scripts/bash/run-tests.sh                 |  205 +-
 .specify/scripts/python/feedback-utils.py          |   39 +-
 .specify/shared/guidelines/better-harness.md       |    4 +-
 .../code-review/scripts/git-delta-review.sh        |   21 +-
 .../sdd-loop-driver/references/efficiency-model.md |    4 +-
 .../sdd-loop-driver/references/stage-prompts.md    |    4 +-
 .../baseline-failed.txt                            |  287 +
 .../checklists/requirements.md                     |   52 +
 .../checklists/suite-speed-2026-11-10.md           |   72 +
 .../checkpoints/04-tasks.md                        |   31 +
 .../checkpoints/05-checklist.md                    |   24 +
 .../checkpoints/06-analyze.md                      |   27 +
 .../checkpoints/07-implement.md                    |   42 +
 .../checkpoints/08-review.md                       |   41 +
 .../098-suite-speed-optimizations/code-review.md   |  925 +++
 .../contracts/event-wait.contract.md               |   64 +
 .../contracts/inprocess-conversion.contract.md     |   58 +
 .../contracts/parallel-consistency.contract.md     |   64 +
 .../contracts/scan-cache.contract.md               |   63 +
 .../contracts/slow-membership.contract.md          |   54 +
 .../contracts/tier-selection.contract.md           |  121 +
 .../coverage-baseline.txt                          |  642 ++
 .../098-suite-speed-optimizations/data-model.md    |  121 +
 .../098-suite-speed-optimizations/feature-ref.md   |   66 +
 .../notes/pre-change-measurements.md               | 8688 ++++++++++++++++++++
 .../notes/quickstart-run.md                        |  297 +
 .../notes/red-first-evidence.md                    |  344 +
 .../specs/098-suite-speed-optimizations/plan.md    |  366 +
 .../098-suite-speed-optimizations/quickstart.md    |  193 +
 .../098-suite-speed-optimizations/requirements.md  |  266 +
 .../098-suite-speed-optimizations/research.md      |  137 +
 .../specs/098-suite-speed-optimizations/review.md  |  379 +
 .../specs/098-suite-speed-optimizations/tasks.md   |  407 +
 .../analyze-coverage-accounting-2026-11-10.txt     | 1348 +++
 ...alyze-coverage-accounting-round2-2026-11-10.txt | 1337 +++
 ...alyze-coverage-accounting-round3-2026-11-10.txt | 1310 +++
 .../test-evidence/analyze-findings-W1.md           |  110 +
 .../test-evidence/analyze-findings-W2.md           |   52 +
 .../test-evidence/analyze-findings-W3.md           |   34 +
 .../test-evidence/analyze-findings-r3-W13.md       |   25 +
 .../test-evidence/analyze-findings-r3-W2.md        |   21 +
 .../test-evidence/analyze-findings-round2-W1.md    |   92 +
 .../test-evidence/analyze-findings-round2-W2.md    |  106 +
 .../test-evidence/analyze-findings-round2-W3.md    |   36 +
 .../test-evidence/analyze-merged-2026-11-10.md     |  206 +
 .../test-evidence/analyze-merged-r3-2026-11-10.md  |  207 +
 .../analyze-merged-round2-2026-11-10.md            |  261 +
 .../analyze-repair-dispositions-2026-11-10.md      |   95 +
 .../analyze-repair-dispositions-r3-2026-11-10.md   |   67 +
 .../analyze-repair-gates-2026-11-10.txt            |   86 +
 .../analyze-repair-gates-r3-2026-11-10.txt         |  106 +
 .../test-evidence/cache-counts.txt                 |  137 +
 .../test-evidence/cache-green.txt                  |   40 +
 .../test-evidence/cache-mutations.txt              |   90 +
 .../test-evidence/checklist-gates.txt              |   40 +
 .../test-evidence/corpus-write-hazard.txt          |  111 +
 .../test-evidence/event-wait-green.txt             |  136 +
 .../test-evidence/event-wait-mutations.txt         |   85 +
 .../test-evidence/forbidden-shortcuts.txt          |   77 +
 .../test-evidence/full-collection-diff.txt         |   87 +
 .../test-evidence/full-collection-disposed.txt     |    1 +
 .../test-evidence/index.md                         |   60 +
 .../test-evidence/inprocess-conversion.md          |  520 ++
 .../inprocess-equivalence-wp7-after-a.txt          |  914 ++
 .../inprocess-equivalence-wp7-after-b.txt          |  608 ++
 .../inprocess-equivalence-wp7-after-c.txt          |    7 +
 .../inprocess-equivalence-wp7-before-a.txt         |  592 ++
 .../inprocess-equivalence-wp7-before-b.txt         |  438 +
 .../inprocess-equivalence-wp7-before-c.txt         |    7 +
 .../inprocess-equivalence-wp7-pilot-after.txt      |    4 +
 .../inprocess-equivalence-wp7-pilot-before.txt     |    4 +
 .../test-evidence/inprocess-equivalence-wp7.txt    |  102 +
 .../inprocess-equivalence-wp8-after-contract.txt   |  534 ++
 ...inprocess-equivalence-wp8-after-integration.txt |  424 +
 .../inprocess-equivalence-wp8-after-unit.txt       |  158 +
 .../inprocess-equivalence-wp8-before-contract.txt  |  540 ++
 ...nprocess-equivalence-wp8-before-integration.txt |  424 +
 .../inprocess-equivalence-wp8-before-unit.txt      |  158 +
 .../test-evidence/inprocess-equivalence.txt        |   87 +
 .../test-evidence/inprocess-guard-wp7.txt          |   34 +
 .../test-evidence/inprocess-guard-wp8.txt          |    7 +
 .../test-evidence/inprocess-mutations.txt          |  344 +
 .../test-evidence/interface-evidence.txt           |   50 +
 .../test-evidence/overlap-check-plan.txt           |    5 +
 .../parallel-consistency-contract.txt              |  432 +
 .../test-evidence/parallel-consistency-noxdist.txt |  197 +
 .../parallel-contract-parallel-names.txt           |  160 +
 .../parallel-contract-serial-names.txt             |  160 +
 .../test-evidence/parallel-mutations.txt           |   95 +
 .../test-evidence/parallel-noxdist-names.txt       |  157 +
 .../test-evidence/plan-baseline-probe.txt          |   29 +
 .../test-evidence/plan-execution-reading.yaml      |    3 +
 .../test-evidence/plan-gates.txt                   |   54 +
 .../test-evidence/plan-verification.txt            |   53 +
 .../test-evidence/quickstart-s4-parallel-names.txt |  157 +
 .../test-evidence/quickstart-s4-serial-names.txt   |  159 +
 .../test-evidence/requirements-baseline-probe.txt  |   64 +
 .../review-repair-dispositions-r1-2026-11-11.md    |  170 +
 .../test-evidence/review-repair-final-failed.txt   |  254 +
 .../review-repair-prechange-failed.txt             |  279 +
 .../review-repair-r1-closure-payload.json          |   51 +
 .../review-repair-r1-closure-verdict.txt           |   47 +
 .../test-evidence/review-repair-r1-f6-receipt.txt  |   40 +
 .../test-evidence/review-repair-r1-sc002-comm.txt  |   52 +
 .../test-evidence/review-repair-r1-sc005-walls.txt |   64 +
 .../test-evidence/review-repair-r1-trigger-fix.txt |   36 +
 .../review-repair-s4-parallel-names.txt            |  137 +
 .../review-repair-s4-serial-names.txt              |  137 +
 .../test-evidence/review-smoke-098.txt             |   28 +
 .../test-evidence/run-logs/default-parallel.log.gz |  Bin 0 -> 89195 bytes
 .../test-evidence/run-logs/default-serial.log.gz   |  Bin 0 -> 82396 bytes
 .../run-logs/review-repair-final-full.log.gz       |  Bin 0 -> 86564 bytes
 .../run-logs/review-repair-prechange-full.log.gz   |  Bin 0 -> 90089 bytes
 .../run-logs/review-repair-s4-parallel.log.gz      |  Bin 0 -> 54424 bytes
 .../run-logs/review-repair-s4-serial.log.gz        |  Bin 0 -> 57784 bytes
 .../test-evidence/run-logs/slot1-full.log.gz       |  Bin 0 -> 91739 bytes
 .../test-evidence/runner-contract-pretest.txt      |   12 +
 .../test-evidence/session-fixture-probe.txt        |   31 +
 .../test-evidence/setup-freeze-check.txt           |   95 +
 .../test-evidence/slow-members-measurement.txt     |  141 +
 .../test-evidence/slow-members.md                  |   17 +
 .../test-evidence/slow-registry-wp2-green.txt      |   52 +
 .../test-evidence/targeted-pretest-baseline.txt    |   76 +
 .../test-evidence/tasks-gates.txt                  |   21 +
 .../test-evidence/tasks.jsonl                      |    1 +
 .../test-evidence/tier-contract-green.txt          |   67 +
 .../test-evidence/tier-measurements.txt            |   55 +
 .../test-evidence/tier-mechanism-wp1-green.txt     |   70 +
 .../test-evidence/tier-mutations.txt               |  236 +
 .../test-evidence/verification-smoke-098.txt       |    8 +
 .../test-evidence/wp3-two-slot-full.txt            |  152 +
 .../098-suite-speed-optimizations/verification.md  |  188 +
 pyproject.toml                                     |    1 +
 scripts/bash/run-tests.sh                          |  198 +-
 scripts/python/feedback-utils.py                   |   39 +-
 shared/guidelines/better-harness.md                |    4 +-
 .../sdd-loop-driver/references/efficiency-model.md |    4 +-
 .../sdd-loop-driver/references/stage-prompts.md    |    4 +-
 .../code-review/scripts/git-delta-review.sh        |   21 +-
 test-evidence/requirements-gate-repair.txt         |    4 +
 tests/conftest.py                                  |  187 +
 tests/contract/test_acceptance_premises.py         |    6 +-
 tests/contract/test_archive_migration.py           |    6 +-
 tests/contract/test_bilingual_expression.py        |    8 +-
 tests/contract/test_binding_model.py               |    6 +-
 tests/contract/test_checker_form.py                |    6 +-
 .../contract/test_clarify_semantic_completeness.py |    5 +-
 tests/contract/test_clause_coverage.py             |   53 +-
 tests/contract/test_clause_forms.py                |    1 +
 tests/contract/test_client_metrics.py              |   90 +-
 tests/contract/test_command_family.py              |   14 +-
 tests/contract/test_compile_propagation_order.py   |   14 +-
 tests/contract/test_concurrency_class_table.py     |    7 +-
 tests/contract/test_concurrency_declarations.py    |   12 +-
 .../test_concurrency_dispatch_capability.py        |    7 +-
 tests/contract/test_concurrency_disposal.py        |    7 +-
 tests/contract/test_concurrency_high_order.py      |    7 +-
 .../contract/test_concurrency_real_run_evidence.py |    7 +-
 .../contract/test_concurrency_reproduction_092.py  |    9 +-
 tests/contract/test_concurrency_serial_reason.py   |    7 +-
 tests/contract/test_concurrency_units.py           |    7 +-
 tests/contract/test_confirmation_gates_sweep.py    |    9 +-
 tests/contract/test_coverage_receipt.py            |   85 +-
 tests/contract/test_criterion_subject.py           |    8 +-
 tests/contract/test_decision_tension_contract.py   |    8 +-
 tests/contract/test_decision_tension_validator.py  |    7 +-
 tests/contract/test_declaration_facts.py           |    6 +-
 tests/contract/test_delegation_classes.py          |    9 +-
 tests/contract/test_doc_consistency_checker.py     |    6 +-
 tests/contract/test_docs_utils_cli.py              |   17 +-
 tests/contract/test_document_structure_gate.py     |    9 +-
 tests/contract/test_engine_face_contract.py        |   11 +-
 tests/contract/test_event_wait_contract.py         |  294 +
 tests/contract/test_exec_quant_aggregate.py        |    8 +-
 tests/contract/test_exec_quant_engine.py           |    9 +-
 tests/contract/test_expression_faces.py            |   13 +-
 .../test_falsification_quartet_validator.py        |    7 +-
 tests/contract/test_fast_fail_discipline.py        |   17 +-
 tests/contract/test_feedback_probe_cli.py          |   20 +-
 tests/contract/test_flow_class_correctness.py      |    9 +-
 tests/contract/test_flow_class_ledger.py           |    9 +-
 tests/contract/test_flow_class_spec_declaration.py |    9 +-
 tests/contract/test_git_closeout_contract.py       |    7 +-
 tests/contract/test_git_workflow_observe.py        |    8 +-
 tests/contract/test_glossary_mechanism.py          |    6 +-
 tests/contract/test_handler_registry.py            |   13 +-
 tests/contract/test_handoff_contract.py            |    6 +-
 tests/contract/test_humanize_command_surface.py    |    7 +-
 .../contract/test_inprocess_conversion_contract.py |  499 ++
 tests/contract/test_isomorphism_map.py             |   10 +-
 tests/contract/test_knowledge_promotion.py         |   11 +-
 tests/contract/test_ledger_reconciliation.py       |    9 +-
 tests/contract/test_line_envelope_contract.py      |   18 +-
 tests/contract/test_merge_provenance_gate.py       |    4 +-
 tests/contract/test_neutrality_budget.py           |    5 +-
 tests/contract/test_non_disposable_contract.py     |    5 +-
 tests/contract/test_non_regression_064.py          |   23 +-
 .../contract/test_parallel_consistency_contract.py |  504 ++
 tests/contract/test_parallel_lines.py              |    6 +-
 tests/contract/test_proactive_trigger_section.py   |   10 +-
 tests/contract/test_record_retention_engine.py     |    9 +-
 tests/contract/test_requirements_checker.py        |    5 +-
 tests/contract/test_resident_backfill.py           |    6 +-
 tests/contract/test_review_feedback_boundary.py    |   17 +-
 tests/contract/test_roster_reporter_seat.py        |    7 +-
 tests/contract/test_run_checks.py                  |   17 +-
 tests/contract/test_sanitize_renumber_lane.py      |    6 +-
 tests/contract/test_sanitize_retention_lane.py     |    6 +-
 tests/contract/test_scan_cache_contract.py         |  295 +
 tests/contract/test_scan_confirmation_gates.py     |    9 +-
 tests/contract/test_scope_resolution.py            |    6 +-
 tests/contract/test_script_interface_contract.py   |   28 +-
 tests/contract/test_scripts_distribution_parity.py |    9 +-
 tests/contract/test_sdd_compat_containment.py      |   14 +-
 tests/contract/test_sdd_diffusion.py               |    8 +-
 .../contract/test_sdd_loop_driver_cli_profiles.py  |   12 +-
 tests/contract/test_sdd_loop_driver_efficiency.py  |    6 +-
 .../test_sdd_loop_driver_wp_coordination.py        |    5 +-
 tests/contract/test_sdd_loop_driver_wp_gate.py     |    5 +-
 tests/contract/test_sdd_loop_driver_wp_model.py    |    5 +-
 tests/contract/test_self_explanatory_glossary.py   |    6 +-
 tests/contract/test_ssh_utils_skill.py             |    6 +-
 tests/contract/test_store_state_protocol.py        |   19 +-
 tests/contract/test_suite_tier_contract.py         |  710 ++
 tests/contract/test_sync_mirrors_only.py           |    6 +-
 tests/contract/test_team_command_routing.py        |   15 +-
 tests/contract/test_team_item_ledger.py            |   30 +-
 tests/contract/test_temp_directory_discipline.py   |   16 +-
 tests/contract/test_token_efficiency_feedback.py   |    5 +-
 tests/contract/test_trigger_engine.py              |   13 +-
 .../contract/test_user_facing_comprehension_doc.py |    7 +-
 .../test_user_facing_comprehension_pointers.py     |    5 +-
 tests/contract/test_wrap_up_wording_gate_safe.py   |    5 +-
 tests/fixtures/line_fixtures.py                    |    8 +-
 tests/integration/test_coordination_round.py       |   13 +-
 tests/integration/test_docs_command_scenarios.py   |   13 +-
 tests/integration/test_docs_notes_lifecycle.py     |    5 +-
 .../integration/test_docs_obligation_scenarios.py  |    5 +-
 tests/integration/test_expression_line_pilot.py    |    5 +-
 tests/integration/test_goal_definition_sourcing.py |   11 +-
 tests/integration/test_goal_migration_path.py      |   17 +-
 tests/integration/test_goal_progress_state.py      |   14 +-
 tests/integration/test_goal_reference.py           |   26 +-
 tests/integration/test_goal_roster.py              |   13 +-
 tests/integration/test_hugo_scaffold_scenarios.py  |   16 +-
 tests/integration/test_sdd_house_keeping_flow.py   |    5 +-
 .../test_sdd_loop_efficiency_regression.py         |    8 +-
 .../integration/test_sdd_loop_efficiency_runner.py |   12 +-
 tests/integration/test_session_kill_reattach.py    |   32 +-
 tests/integration/test_temp_team_worktree_queue.py |   11 +-
 .../integration/test_worktree_integration_queue.py |   10 +-
 tests/integration/test_wp_coordination_dry_runs.py |    8 +-
 tests/script_api.py                                |   97 +
 tests/unit/test_audit_plan_changes.py              |    6 +-
 tests/unit/test_audit_test_budget.py               |    6 +-
 tests/unit/test_concurrency_check_engine.py        |    6 +-
 tests/unit/test_decomposition_check.py             |    5 +-
 tests/unit/test_derive_live_log.py                 |    7 +-
 tests/unit/test_doc_consistency_rules.py           |    6 +-
 tests/unit/test_docs_obligation_reuse.py           |    6 +-
 tests/unit/test_docs_utils_carriers.py             |    6 +-
 tests/unit/test_docs_utils_obligation.py           |    5 +-
 tests/unit/test_flow_class_check.py                |    9 +-
 tests/unit/test_flow_class_spec_key.py             |    8 +-
 tests/unit/test_glossary_utils.py                  |    6 +-
 tests/unit/test_isomorphism_checker.py             |    9 +-
 tests/unit/test_overlap_check.py                   |    6 +-
 tests/unit/test_pre_analyze_check.py               |    8 +-
 tests/unit/test_reconciler_extensions.py           |    9 +-
 tests/unit/test_workspace_guard.py                 |    5 +-
 tests/unit/test_wp_gate.py                         |    5 +-
 tests/unit/test_wp_report.py                       |   15 +-
 277 files changed, 34151 insertions(+), 804 deletions(-)
```

---

## Review 意见


### 🟠 [IMPORTANT] scripts/bash/run-tests.sh (Line 372)

> Recurred from round 1 (open): `tier=caller` skips the 086 C-010/C-011 serial two-pass entirely, while tier-selection C-012 declares the serial exclusion model unchanged. The implementation follows C-003 (single `-m`, no second marker expression), so the fix is a contract-wording narrowing plus a guard for a serial-marked test inside a caller `-m` selection — not a code change this review may make. Answered: agree; not blocking.

<sub>02:57:30</sub>


### 🟢 [SUGGESTION] scripts/bash/run-tests.sh (Line 242)

> Recurred from round 1 (open): `collect_slow_count` treats every pytest status other than 5 as a count and never surfaces exit 2/4 (usage/collection error), so a broken collection can read as `excluded_slow=0`. Record the non-{0,5} status as a named stderr line instead of silently counting output lines.

<sub>02:57:30</sub>


### 👍 [PRAISE] tests/contract/test_trigger_engine.py (Line 149)

> The review-repair r1 fixture-isolation fix is a true root-cause repair: it names the C-7 priority and passes `--workspace <cwd>` unless the call already names one; the file runs 145/145 green and SC-002 re-measured empty in both directions. The receipt fix in `git-delta-review.sh` (skip selectors before binary line measurement) is mirrored byte-identically and drilled positive/negative.

<sub>02:57:30</sub>




> **未提交范围（未评审）**: 48 个未提交路径未计入本次评审对象（.specify/memory/session/20261106T041123Z-run-determination-skill-clarify-artifact-r20261106t033959z-0.md, .specify/memory/session/20261109T064508Z-run-determination-speckit-requirements-r20261109t064500z-092.md, .specify/memory/session/20261109T075446Z-run-determination-skill-clarify-artifact-093-clarify-a1.md, .specify/memory/trigger/index.json, .specify/specs/081-acceptance-hardening/test-evidence/smoke-081.txt, .specify/memory/exec-quant/records/20261110T083347598651Z-f7bb5a55.json, .specify/memory/exec-quant/records/20261110T084641565115Z-fa5487c4.json, .specify/memory/exec-quant/records/20261110T092148689396Z-741159cb.json, .specify/memory/exec-quant/records/20261110T094030389410Z-d20a3410.json, .specify/memory/exec-quant/records/20261110T094634168349Z-4d326abc.json, .specify/memory/exec-quant/records/20261110T100534762638Z-82883ffb.json, .specify/memory/exec-quant/records/20261110T104050182662Z-6efbafa2.json, .specify/memory/exec-quant/records/20261110T124542593806Z-34a30d3b.json, .specify/memory/exec-quant/records/20261110T153021935633Z-84782d9b.json, .specify/memory/exec-quant/records/20261110T181634080403Z-32f6b82f.json, .specify/memory/exec-quant/records/20261110T181634446648Z-b4ae0c6f.json, .specify/memory/exec-quant/records/20261110T181634814657Z-b339aa35.json, .specify/memory/exec-quant/records/20261110T181635181759Z-8eb72752.json, .specify/memory/feedback/20261110T083354Z-speckit-requirements.md, .specify/memory/feedback/20261110T084651Z-skill-clarify-artifact.md, .specify/memory/feedback/20261110T092234Z-speckit-plan.md, .specify/memory/feedback/20261110T094035Z-speckit-tasks.md, .specify/memory/feedback/20261110T094653Z-speckit-checklist.md, .specify/memory/feedback/20261110T100544Z-speckit-analyze.md, .specify/memory/feedback/20261110T104058Z-speckit-analyze.md, .specify/memory/feedback/20261110T124552Z-speckit-analyze.md, .specify/memory/feedback/20261110T134849Z-speckit-implement.md, .specify/memory/feedback/20261110T140122Z-speckit-implement.md, .specify/memory/feedback/20261110T153011Z-speckit-implement.md, .specify/memory/feedback/20261110T181649Z-skill-review-feature-quality.md, .specify/memory/feedback/20261110T181649Z-skill-review-sdd-process.md, .specify/memory/feedback/20261110T181649Z-speckit-review.md, .specify/memory/session/20261110T083342Z-run-determination-speckit-requirements-r20261110t081104z-b09.md, .specify/memory/session/20261110T084636Z-run-determination-skill-clarify-artifact-r20261110t084536z-b.md, .specify/memory/session/20261110T092146Z-run-determination-speckit-plan-r20261110t081104z-b098.md, .specify/memory/session/20261110T094017Z-run-determination-speckit-tasks-r20261110t081104z-b098.md, .specify/memory/session/20261110T094632Z-run-determination-speckit-checklist-098-checklist-20261110t1.md, .specify/memory/session/20261110T100530Z-run-determination-speckit-analyze-098-analyze-20261110t18053.md, .specify/memory/session/20261110T104045Z-run-determination-speckit-analyze-098-analyze-r2-20261110t10.md, .specify/memory/session/20261110T124538Z-run-determination-speckit-analyze-098-analyze-r3-20261110t12.md, .specify/memory/session/20261110T152950Z-run-determination-speckit-implement-098-implement-wp4-202611.md, .specify/memory/session/20261110T181640Z-run-determination-skill-code-review-r20261110t081104z-b098.md, .specify/memory/session/20261110T181640Z-run-determination-skill-review-feature-quality-r20261110t081.md, .specify/memory/session/20261110T181640Z-run-determination-skill-review-sdd-process-r20261110t081104z.md, .specify/memory/session/20261110T181640Z-run-determination-speckit-review-r20261110t081104z-b098.md, .specify/specs/098-suite-speed-optimizations/checkpoints/01-requirements.md, .specify/specs/098-suite-speed-optimizations/checkpoints/02-clarify.md, .specify/specs/098-suite-speed-optimizations/checkpoints/03-plan.md）；本回执不对该范围给出任何结论。

<!-- coverage-receipt:begin -->
receipt_version=1
base=b3da3a26dfba209057f65c2b17962b9516812c39
head=f129eb8019ac11bef74c3931271a0aec4d6d145b
base_source=feature-first-commit
renderer=text
changed_files=277
judged_files=139
skipped_files=138
gap_files=0
lines_added=3705
lines_deleted=786
file.001.path=.specify/constitution.md
file.001.verdict=skipped
file.001.reason=non-code-file
file.002.path=.specify/features.md
file.002.verdict=skipped
file.002.reason=non-code-file
file.003.path=.specify/features/086-efficient-test-execution.md
file.003.verdict=skipped
file.003.reason=non-code-file
file.004.path=.specify/glossary.md
file.004.verdict=skipped
file.004.reason=non-code-file
file.005.path=.specify/register.md
file.005.verdict=skipped
file.005.reason=non-code-file
file.006.path=.specify/scripts/bash/run-tests.sh
file.006.verdict=reviewed
file.007.path=.specify/scripts/python/feedback-utils.py
file.007.verdict=reviewed
file.008.path=.specify/shared/guidelines/better-harness.md
file.008.verdict=skipped
file.008.reason=non-code-file
file.009.path=.specify/skills/internal/code-review/scripts/git-delta-review.sh
file.009.verdict=reviewed
file.010.path=.specify/skills/sdd-loop-driver/references/efficiency-model.md
file.010.verdict=skipped
file.010.reason=non-code-file
file.011.path=.specify/skills/sdd-loop-driver/references/stage-prompts.md
file.011.verdict=skipped
file.011.reason=non-code-file
file.012.path=.specify/specs/098-suite-speed-optimizations/baseline-failed.txt
file.012.verdict=skipped
file.012.reason=non-code-file
file.013.path=.specify/specs/098-suite-speed-optimizations/checklists/requirements.md
file.013.verdict=skipped
file.013.reason=non-code-file
file.014.path=.specify/specs/098-suite-speed-optimizations/checklists/suite-speed-2026-11-10.md
file.014.verdict=skipped
file.014.reason=non-code-file
file.015.path=.specify/specs/098-suite-speed-optimizations/checkpoints/04-tasks.md
file.015.verdict=skipped
file.015.reason=non-code-file
file.016.path=.specify/specs/098-suite-speed-optimizations/checkpoints/05-checklist.md
file.016.verdict=skipped
file.016.reason=non-code-file
file.017.path=.specify/specs/098-suite-speed-optimizations/checkpoints/06-analyze.md
file.017.verdict=skipped
file.017.reason=non-code-file
file.018.path=.specify/specs/098-suite-speed-optimizations/checkpoints/07-implement.md
file.018.verdict=skipped
file.018.reason=non-code-file
file.019.path=.specify/specs/098-suite-speed-optimizations/checkpoints/08-review.md
file.019.verdict=skipped
file.019.reason=non-code-file
file.020.path=.specify/specs/098-suite-speed-optimizations/code-review.md
file.020.verdict=skipped
file.020.reason=non-code-file
file.021.path=.specify/specs/098-suite-speed-optimizations/contracts/event-wait.contract.md
file.021.verdict=skipped
file.021.reason=non-code-file
file.022.path=.specify/specs/098-suite-speed-optimizations/contracts/inprocess-conversion.contract.md
file.022.verdict=skipped
file.022.reason=non-code-file
file.023.path=.specify/specs/098-suite-speed-optimizations/contracts/parallel-consistency.contract.md
file.023.verdict=skipped
file.023.reason=non-code-file
file.024.path=.specify/specs/098-suite-speed-optimizations/contracts/scan-cache.contract.md
file.024.verdict=skipped
file.024.reason=non-code-file
file.025.path=.specify/specs/098-suite-speed-optimizations/contracts/slow-membership.contract.md
file.025.verdict=skipped
file.025.reason=non-code-file
file.026.path=.specify/specs/098-suite-speed-optimizations/contracts/tier-selection.contract.md
file.026.verdict=skipped
file.026.reason=non-code-file
file.027.path=.specify/specs/098-suite-speed-optimizations/coverage-baseline.txt
file.027.verdict=skipped
file.027.reason=non-code-file
file.028.path=.specify/specs/098-suite-speed-optimizations/data-model.md
file.028.verdict=skipped
file.028.reason=non-code-file
file.029.path=.specify/specs/098-suite-speed-optimizations/feature-ref.md
file.029.verdict=skipped
file.029.reason=non-code-file
file.030.path=.specify/specs/098-suite-speed-optimizations/notes/pre-change-measurements.md
file.030.verdict=skipped
file.030.reason=non-code-file
file.031.path=.specify/specs/098-suite-speed-optimizations/notes/quickstart-run.md
file.031.verdict=skipped
file.031.reason=non-code-file
file.032.path=.specify/specs/098-suite-speed-optimizations/notes/red-first-evidence.md
file.032.verdict=skipped
file.032.reason=non-code-file
file.033.path=.specify/specs/098-suite-speed-optimizations/plan.md
file.033.verdict=skipped
file.033.reason=non-code-file
file.034.path=.specify/specs/098-suite-speed-optimizations/quickstart.md
file.034.verdict=skipped
file.034.reason=non-code-file
file.035.path=.specify/specs/098-suite-speed-optimizations/requirements.md
file.035.verdict=skipped
file.035.reason=non-code-file
file.036.path=.specify/specs/098-suite-speed-optimizations/research.md
file.036.verdict=skipped
file.036.reason=non-code-file
file.037.path=.specify/specs/098-suite-speed-optimizations/review.md
file.037.verdict=skipped
file.037.reason=non-code-file
file.038.path=.specify/specs/098-suite-speed-optimizations/tasks.md
file.038.verdict=skipped
file.038.reason=non-code-file
file.039.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-coverage-accounting-2026-11-10.txt
file.039.verdict=skipped
file.039.reason=non-code-file
file.040.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-coverage-accounting-round2-2026-11-10.txt
file.040.verdict=skipped
file.040.reason=non-code-file
file.041.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-coverage-accounting-round3-2026-11-10.txt
file.041.verdict=skipped
file.041.reason=non-code-file
file.042.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-findings-W1.md
file.042.verdict=skipped
file.042.reason=non-code-file
file.043.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-findings-W2.md
file.043.verdict=skipped
file.043.reason=non-code-file
file.044.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-findings-W3.md
file.044.verdict=skipped
file.044.reason=non-code-file
file.045.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-findings-r3-W13.md
file.045.verdict=skipped
file.045.reason=non-code-file
file.046.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-findings-r3-W2.md
file.046.verdict=skipped
file.046.reason=non-code-file
file.047.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-findings-round2-W1.md
file.047.verdict=skipped
file.047.reason=non-code-file
file.048.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-findings-round2-W2.md
file.048.verdict=skipped
file.048.reason=non-code-file
file.049.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-findings-round2-W3.md
file.049.verdict=skipped
file.049.reason=non-code-file
file.050.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-merged-2026-11-10.md
file.050.verdict=skipped
file.050.reason=non-code-file
file.051.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-merged-r3-2026-11-10.md
file.051.verdict=skipped
file.051.reason=non-code-file
file.052.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-merged-round2-2026-11-10.md
file.052.verdict=skipped
file.052.reason=non-code-file
file.053.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-repair-dispositions-2026-11-10.md
file.053.verdict=skipped
file.053.reason=non-code-file
file.054.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-repair-dispositions-r3-2026-11-10.md
file.054.verdict=skipped
file.054.reason=non-code-file
file.055.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-repair-gates-2026-11-10.txt
file.055.verdict=skipped
file.055.reason=non-code-file
file.056.path=.specify/specs/098-suite-speed-optimizations/test-evidence/analyze-repair-gates-r3-2026-11-10.txt
file.056.verdict=skipped
file.056.reason=non-code-file
file.057.path=.specify/specs/098-suite-speed-optimizations/test-evidence/cache-counts.txt
file.057.verdict=skipped
file.057.reason=non-code-file
file.058.path=.specify/specs/098-suite-speed-optimizations/test-evidence/cache-green.txt
file.058.verdict=skipped
file.058.reason=non-code-file
file.059.path=.specify/specs/098-suite-speed-optimizations/test-evidence/cache-mutations.txt
file.059.verdict=skipped
file.059.reason=non-code-file
file.060.path=.specify/specs/098-suite-speed-optimizations/test-evidence/checklist-gates.txt
file.060.verdict=skipped
file.060.reason=non-code-file
file.061.path=.specify/specs/098-suite-speed-optimizations/test-evidence/corpus-write-hazard.txt
file.061.verdict=skipped
file.061.reason=non-code-file
file.062.path=.specify/specs/098-suite-speed-optimizations/test-evidence/event-wait-green.txt
file.062.verdict=skipped
file.062.reason=non-code-file
file.063.path=.specify/specs/098-suite-speed-optimizations/test-evidence/event-wait-mutations.txt
file.063.verdict=skipped
file.063.reason=non-code-file
file.064.path=.specify/specs/098-suite-speed-optimizations/test-evidence/forbidden-shortcuts.txt
file.064.verdict=skipped
file.064.reason=non-code-file
file.065.path=.specify/specs/098-suite-speed-optimizations/test-evidence/full-collection-diff.txt
file.065.verdict=skipped
file.065.reason=non-code-file
file.066.path=.specify/specs/098-suite-speed-optimizations/test-evidence/full-collection-disposed.txt
file.066.verdict=skipped
file.066.reason=non-code-file
file.067.path=.specify/specs/098-suite-speed-optimizations/test-evidence/index.md
file.067.verdict=skipped
file.067.reason=non-code-file
file.068.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-conversion.md
file.068.verdict=skipped
file.068.reason=non-code-file
file.069.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp7-after-a.txt
file.069.verdict=skipped
file.069.reason=non-code-file
file.070.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp7-after-b.txt
file.070.verdict=skipped
file.070.reason=non-code-file
file.071.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp7-after-c.txt
file.071.verdict=skipped
file.071.reason=non-code-file
file.072.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp7-before-a.txt
file.072.verdict=skipped
file.072.reason=non-code-file
file.073.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp7-before-b.txt
file.073.verdict=skipped
file.073.reason=non-code-file
file.074.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp7-before-c.txt
file.074.verdict=skipped
file.074.reason=non-code-file
file.075.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp7-pilot-after.txt
file.075.verdict=skipped
file.075.reason=non-code-file
file.076.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp7-pilot-before.txt
file.076.verdict=skipped
file.076.reason=non-code-file
file.077.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp7.txt
file.077.verdict=skipped
file.077.reason=non-code-file
file.078.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp8-after-contract.txt
file.078.verdict=skipped
file.078.reason=non-code-file
file.079.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp8-after-integration.txt
file.079.verdict=skipped
file.079.reason=non-code-file
file.080.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp8-after-unit.txt
file.080.verdict=skipped
file.080.reason=non-code-file
file.081.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp8-before-contract.txt
file.081.verdict=skipped
file.081.reason=non-code-file
file.082.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp8-before-integration.txt
file.082.verdict=skipped
file.082.reason=non-code-file
file.083.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence-wp8-before-unit.txt
file.083.verdict=skipped
file.083.reason=non-code-file
file.084.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-equivalence.txt
file.084.verdict=skipped
file.084.reason=non-code-file
file.085.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-guard-wp7.txt
file.085.verdict=skipped
file.085.reason=non-code-file
file.086.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-guard-wp8.txt
file.086.verdict=skipped
file.086.reason=non-code-file
file.087.path=.specify/specs/098-suite-speed-optimizations/test-evidence/inprocess-mutations.txt
file.087.verdict=skipped
file.087.reason=non-code-file
file.088.path=.specify/specs/098-suite-speed-optimizations/test-evidence/interface-evidence.txt
file.088.verdict=skipped
file.088.reason=non-code-file
file.089.path=.specify/specs/098-suite-speed-optimizations/test-evidence/overlap-check-plan.txt
file.089.verdict=skipped
file.089.reason=non-code-file
file.090.path=.specify/specs/098-suite-speed-optimizations/test-evidence/parallel-consistency-contract.txt
file.090.verdict=skipped
file.090.reason=non-code-file
file.091.path=.specify/specs/098-suite-speed-optimizations/test-evidence/parallel-consistency-noxdist.txt
file.091.verdict=skipped
file.091.reason=non-code-file
file.092.path=.specify/specs/098-suite-speed-optimizations/test-evidence/parallel-contract-parallel-names.txt
file.092.verdict=skipped
file.092.reason=non-code-file
file.093.path=.specify/specs/098-suite-speed-optimizations/test-evidence/parallel-contract-serial-names.txt
file.093.verdict=skipped
file.093.reason=non-code-file
file.094.path=.specify/specs/098-suite-speed-optimizations/test-evidence/parallel-mutations.txt
file.094.verdict=skipped
file.094.reason=non-code-file
file.095.path=.specify/specs/098-suite-speed-optimizations/test-evidence/parallel-noxdist-names.txt
file.095.verdict=skipped
file.095.reason=non-code-file
file.096.path=.specify/specs/098-suite-speed-optimizations/test-evidence/plan-baseline-probe.txt
file.096.verdict=skipped
file.096.reason=non-code-file
file.097.path=.specify/specs/098-suite-speed-optimizations/test-evidence/plan-execution-reading.yaml
file.097.verdict=skipped
file.097.reason=non-code-file
file.098.path=.specify/specs/098-suite-speed-optimizations/test-evidence/plan-gates.txt
file.098.verdict=skipped
file.098.reason=non-code-file
file.099.path=.specify/specs/098-suite-speed-optimizations/test-evidence/plan-verification.txt
file.099.verdict=skipped
file.099.reason=non-code-file
file.100.path=.specify/specs/098-suite-speed-optimizations/test-evidence/quickstart-s4-parallel-names.txt
file.100.verdict=skipped
file.100.reason=non-code-file
file.101.path=.specify/specs/098-suite-speed-optimizations/test-evidence/quickstart-s4-serial-names.txt
file.101.verdict=skipped
file.101.reason=non-code-file
file.102.path=.specify/specs/098-suite-speed-optimizations/test-evidence/requirements-baseline-probe.txt
file.102.verdict=skipped
file.102.reason=non-code-file
file.103.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-dispositions-r1-2026-11-11.md
file.103.verdict=skipped
file.103.reason=non-code-file
file.104.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-final-failed.txt
file.104.verdict=skipped
file.104.reason=non-code-file
file.105.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-prechange-failed.txt
file.105.verdict=skipped
file.105.reason=non-code-file
file.106.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-r1-closure-payload.json
file.106.verdict=skipped
file.106.reason=non-code-file
file.107.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-r1-closure-verdict.txt
file.107.verdict=skipped
file.107.reason=non-code-file
file.108.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-r1-f6-receipt.txt
file.108.verdict=skipped
file.108.reason=non-code-file
file.109.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-r1-sc002-comm.txt
file.109.verdict=skipped
file.109.reason=non-code-file
file.110.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-r1-sc005-walls.txt
file.110.verdict=skipped
file.110.reason=non-code-file
file.111.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-r1-trigger-fix.txt
file.111.verdict=skipped
file.111.reason=non-code-file
file.112.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-s4-parallel-names.txt
file.112.verdict=skipped
file.112.reason=non-code-file
file.113.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-repair-s4-serial-names.txt
file.113.verdict=skipped
file.113.reason=non-code-file
file.114.path=.specify/specs/098-suite-speed-optimizations/test-evidence/review-smoke-098.txt
file.114.verdict=skipped
file.114.reason=non-code-file
file.115.path=.specify/specs/098-suite-speed-optimizations/test-evidence/run-logs/default-parallel.log.gz
file.115.verdict=skipped
file.115.reason=binary
file.116.path=.specify/specs/098-suite-speed-optimizations/test-evidence/run-logs/default-serial.log.gz
file.116.verdict=skipped
file.116.reason=binary
file.117.path=.specify/specs/098-suite-speed-optimizations/test-evidence/run-logs/review-repair-final-full.log.gz
file.117.verdict=skipped
file.117.reason=binary
file.118.path=.specify/specs/098-suite-speed-optimizations/test-evidence/run-logs/review-repair-prechange-full.log.gz
file.118.verdict=skipped
file.118.reason=binary
file.119.path=.specify/specs/098-suite-speed-optimizations/test-evidence/run-logs/review-repair-s4-parallel.log.gz
file.119.verdict=skipped
file.119.reason=binary
file.120.path=.specify/specs/098-suite-speed-optimizations/test-evidence/run-logs/review-repair-s4-serial.log.gz
file.120.verdict=skipped
file.120.reason=binary
file.121.path=.specify/specs/098-suite-speed-optimizations/test-evidence/run-logs/slot1-full.log.gz
file.121.verdict=skipped
file.121.reason=binary
file.122.path=.specify/specs/098-suite-speed-optimizations/test-evidence/runner-contract-pretest.txt
file.122.verdict=skipped
file.122.reason=non-code-file
file.123.path=.specify/specs/098-suite-speed-optimizations/test-evidence/session-fixture-probe.txt
file.123.verdict=skipped
file.123.reason=non-code-file
file.124.path=.specify/specs/098-suite-speed-optimizations/test-evidence/setup-freeze-check.txt
file.124.verdict=skipped
file.124.reason=non-code-file
file.125.path=.specify/specs/098-suite-speed-optimizations/test-evidence/slow-members-measurement.txt
file.125.verdict=skipped
file.125.reason=non-code-file
file.126.path=.specify/specs/098-suite-speed-optimizations/test-evidence/slow-members.md
file.126.verdict=skipped
file.126.reason=non-code-file
file.127.path=.specify/specs/098-suite-speed-optimizations/test-evidence/slow-registry-wp2-green.txt
file.127.verdict=skipped
file.127.reason=non-code-file
file.128.path=.specify/specs/098-suite-speed-optimizations/test-evidence/targeted-pretest-baseline.txt
file.128.verdict=skipped
file.128.reason=non-code-file
file.129.path=.specify/specs/098-suite-speed-optimizations/test-evidence/tasks-gates.txt
file.129.verdict=skipped
file.129.reason=non-code-file
file.130.path=.specify/specs/098-suite-speed-optimizations/test-evidence/tasks.jsonl
file.130.verdict=skipped
file.130.reason=non-code-file
file.131.path=.specify/specs/098-suite-speed-optimizations/test-evidence/tier-contract-green.txt
file.131.verdict=skipped
file.131.reason=non-code-file
file.132.path=.specify/specs/098-suite-speed-optimizations/test-evidence/tier-measurements.txt
file.132.verdict=skipped
file.132.reason=non-code-file
file.133.path=.specify/specs/098-suite-speed-optimizations/test-evidence/tier-mechanism-wp1-green.txt
file.133.verdict=skipped
file.133.reason=non-code-file
file.134.path=.specify/specs/098-suite-speed-optimizations/test-evidence/tier-mutations.txt
file.134.verdict=skipped
file.134.reason=non-code-file
file.135.path=.specify/specs/098-suite-speed-optimizations/test-evidence/verification-smoke-098.txt
file.135.verdict=skipped
file.135.reason=non-code-file
file.136.path=.specify/specs/098-suite-speed-optimizations/test-evidence/wp3-two-slot-full.txt
file.136.verdict=skipped
file.136.reason=non-code-file
file.137.path=.specify/specs/098-suite-speed-optimizations/verification.md
file.137.verdict=skipped
file.137.reason=non-code-file
file.138.path=pyproject.toml
file.138.verdict=reviewed
file.139.path=scripts/bash/run-tests.sh
file.139.verdict=reviewed
file.140.path=scripts/python/feedback-utils.py
file.140.verdict=reviewed
file.141.path=shared/guidelines/better-harness.md
file.141.verdict=skipped
file.141.reason=non-code-file
file.142.path=skills/external/sdd-loop-driver/references/efficiency-model.md
file.142.verdict=skipped
file.142.reason=non-code-file
file.143.path=skills/external/sdd-loop-driver/references/stage-prompts.md
file.143.verdict=skipped
file.143.reason=non-code-file
file.144.path=skills/internal/code-review/scripts/git-delta-review.sh
file.144.verdict=reviewed
file.145.path=test-evidence/requirements-gate-repair.txt
file.145.verdict=skipped
file.145.reason=non-code-file
file.146.path=tests/conftest.py
file.146.verdict=reviewed
file.147.path=tests/contract/test_acceptance_premises.py
file.147.verdict=reviewed
file.148.path=tests/contract/test_archive_migration.py
file.148.verdict=reviewed
file.149.path=tests/contract/test_bilingual_expression.py
file.149.verdict=reviewed
file.150.path=tests/contract/test_binding_model.py
file.150.verdict=reviewed
file.151.path=tests/contract/test_checker_form.py
file.151.verdict=reviewed
file.152.path=tests/contract/test_clarify_semantic_completeness.py
file.152.verdict=reviewed
file.153.path=tests/contract/test_clause_coverage.py
file.153.verdict=reviewed
file.154.path=tests/contract/test_clause_forms.py
file.154.verdict=reviewed
file.155.path=tests/contract/test_client_metrics.py
file.155.verdict=reviewed
file.156.path=tests/contract/test_command_family.py
file.156.verdict=reviewed
file.157.path=tests/contract/test_compile_propagation_order.py
file.157.verdict=reviewed
file.158.path=tests/contract/test_concurrency_class_table.py
file.158.verdict=reviewed
file.159.path=tests/contract/test_concurrency_declarations.py
file.159.verdict=reviewed
file.160.path=tests/contract/test_concurrency_dispatch_capability.py
file.160.verdict=reviewed
file.161.path=tests/contract/test_concurrency_disposal.py
file.161.verdict=reviewed
file.162.path=tests/contract/test_concurrency_high_order.py
file.162.verdict=reviewed
file.163.path=tests/contract/test_concurrency_real_run_evidence.py
file.163.verdict=reviewed
file.164.path=tests/contract/test_concurrency_reproduction_092.py
file.164.verdict=reviewed
file.165.path=tests/contract/test_concurrency_serial_reason.py
file.165.verdict=reviewed
file.166.path=tests/contract/test_concurrency_units.py
file.166.verdict=reviewed
file.167.path=tests/contract/test_confirmation_gates_sweep.py
file.167.verdict=reviewed
file.168.path=tests/contract/test_coverage_receipt.py
file.168.verdict=reviewed
file.169.path=tests/contract/test_criterion_subject.py
file.169.verdict=reviewed
file.170.path=tests/contract/test_decision_tension_contract.py
file.170.verdict=reviewed
file.171.path=tests/contract/test_decision_tension_validator.py
file.171.verdict=reviewed
file.172.path=tests/contract/test_declaration_facts.py
file.172.verdict=reviewed
file.173.path=tests/contract/test_delegation_classes.py
file.173.verdict=reviewed
file.174.path=tests/contract/test_doc_consistency_checker.py
file.174.verdict=reviewed
file.175.path=tests/contract/test_docs_utils_cli.py
file.175.verdict=reviewed
file.176.path=tests/contract/test_document_structure_gate.py
file.176.verdict=reviewed
file.177.path=tests/contract/test_engine_face_contract.py
file.177.verdict=reviewed
file.178.path=tests/contract/test_event_wait_contract.py
file.178.verdict=reviewed
file.179.path=tests/contract/test_exec_quant_aggregate.py
file.179.verdict=reviewed
file.180.path=tests/contract/test_exec_quant_engine.py
file.180.verdict=reviewed
file.181.path=tests/contract/test_expression_faces.py
file.181.verdict=reviewed
file.182.path=tests/contract/test_falsification_quartet_validator.py
file.182.verdict=reviewed
file.183.path=tests/contract/test_fast_fail_discipline.py
file.183.verdict=reviewed
file.184.path=tests/contract/test_feedback_probe_cli.py
file.184.verdict=reviewed
file.185.path=tests/contract/test_flow_class_correctness.py
file.185.verdict=reviewed
file.186.path=tests/contract/test_flow_class_ledger.py
file.186.verdict=reviewed
file.187.path=tests/contract/test_flow_class_spec_declaration.py
file.187.verdict=reviewed
file.188.path=tests/contract/test_git_closeout_contract.py
file.188.verdict=reviewed
file.189.path=tests/contract/test_git_workflow_observe.py
file.189.verdict=reviewed
file.190.path=tests/contract/test_glossary_mechanism.py
file.190.verdict=reviewed
file.191.path=tests/contract/test_handler_registry.py
file.191.verdict=reviewed
file.192.path=tests/contract/test_handoff_contract.py
file.192.verdict=reviewed
file.193.path=tests/contract/test_humanize_command_surface.py
file.193.verdict=reviewed
file.194.path=tests/contract/test_inprocess_conversion_contract.py
file.194.verdict=reviewed
file.195.path=tests/contract/test_isomorphism_map.py
file.195.verdict=reviewed
file.196.path=tests/contract/test_knowledge_promotion.py
file.196.verdict=reviewed
file.197.path=tests/contract/test_ledger_reconciliation.py
file.197.verdict=reviewed
file.198.path=tests/contract/test_line_envelope_contract.py
file.198.verdict=reviewed
file.199.path=tests/contract/test_merge_provenance_gate.py
file.199.verdict=reviewed
file.200.path=tests/contract/test_neutrality_budget.py
file.200.verdict=reviewed
file.201.path=tests/contract/test_non_disposable_contract.py
file.201.verdict=reviewed
file.202.path=tests/contract/test_non_regression_064.py
file.202.verdict=reviewed
file.203.path=tests/contract/test_parallel_consistency_contract.py
file.203.verdict=reviewed
file.204.path=tests/contract/test_parallel_lines.py
file.204.verdict=reviewed
file.205.path=tests/contract/test_proactive_trigger_section.py
file.205.verdict=reviewed
file.206.path=tests/contract/test_record_retention_engine.py
file.206.verdict=reviewed
file.207.path=tests/contract/test_requirements_checker.py
file.207.verdict=reviewed
file.208.path=tests/contract/test_resident_backfill.py
file.208.verdict=reviewed
file.209.path=tests/contract/test_review_feedback_boundary.py
file.209.verdict=reviewed
file.210.path=tests/contract/test_roster_reporter_seat.py
file.210.verdict=reviewed
file.211.path=tests/contract/test_run_checks.py
file.211.verdict=reviewed
file.212.path=tests/contract/test_sanitize_renumber_lane.py
file.212.verdict=reviewed
file.213.path=tests/contract/test_sanitize_retention_lane.py
file.213.verdict=reviewed
file.214.path=tests/contract/test_scan_cache_contract.py
file.214.verdict=reviewed
file.215.path=tests/contract/test_scan_confirmation_gates.py
file.215.verdict=reviewed
file.216.path=tests/contract/test_scope_resolution.py
file.216.verdict=reviewed
file.217.path=tests/contract/test_script_interface_contract.py
file.217.verdict=reviewed
file.218.path=tests/contract/test_scripts_distribution_parity.py
file.218.verdict=reviewed
file.219.path=tests/contract/test_sdd_compat_containment.py
file.219.verdict=reviewed
file.220.path=tests/contract/test_sdd_diffusion.py
file.220.verdict=reviewed
file.221.path=tests/contract/test_sdd_loop_driver_cli_profiles.py
file.221.verdict=reviewed
file.222.path=tests/contract/test_sdd_loop_driver_efficiency.py
file.222.verdict=reviewed
file.223.path=tests/contract/test_sdd_loop_driver_wp_coordination.py
file.223.verdict=reviewed
file.224.path=tests/contract/test_sdd_loop_driver_wp_gate.py
file.224.verdict=reviewed
file.225.path=tests/contract/test_sdd_loop_driver_wp_model.py
file.225.verdict=reviewed
file.226.path=tests/contract/test_self_explanatory_glossary.py
file.226.verdict=reviewed
file.227.path=tests/contract/test_ssh_utils_skill.py
file.227.verdict=reviewed
file.228.path=tests/contract/test_store_state_protocol.py
file.228.verdict=reviewed
file.229.path=tests/contract/test_suite_tier_contract.py
file.229.verdict=reviewed
file.230.path=tests/contract/test_sync_mirrors_only.py
file.230.verdict=reviewed
file.231.path=tests/contract/test_team_command_routing.py
file.231.verdict=reviewed
file.232.path=tests/contract/test_team_item_ledger.py
file.232.verdict=reviewed
file.233.path=tests/contract/test_temp_directory_discipline.py
file.233.verdict=reviewed
file.234.path=tests/contract/test_token_efficiency_feedback.py
file.234.verdict=reviewed
file.235.path=tests/contract/test_trigger_engine.py
file.235.verdict=reviewed
file.236.path=tests/contract/test_user_facing_comprehension_doc.py
file.236.verdict=reviewed
file.237.path=tests/contract/test_user_facing_comprehension_pointers.py
file.237.verdict=reviewed
file.238.path=tests/contract/test_wrap_up_wording_gate_safe.py
file.238.verdict=reviewed
file.239.path=tests/fixtures/line_fixtures.py
file.239.verdict=reviewed
file.240.path=tests/integration/test_coordination_round.py
file.240.verdict=reviewed
file.241.path=tests/integration/test_docs_command_scenarios.py
file.241.verdict=reviewed
file.242.path=tests/integration/test_docs_notes_lifecycle.py
file.242.verdict=reviewed
file.243.path=tests/integration/test_docs_obligation_scenarios.py
file.243.verdict=reviewed
file.244.path=tests/integration/test_expression_line_pilot.py
file.244.verdict=reviewed
file.245.path=tests/integration/test_goal_definition_sourcing.py
file.245.verdict=reviewed
file.246.path=tests/integration/test_goal_migration_path.py
file.246.verdict=reviewed
file.247.path=tests/integration/test_goal_progress_state.py
file.247.verdict=reviewed
file.248.path=tests/integration/test_goal_reference.py
file.248.verdict=reviewed
file.249.path=tests/integration/test_goal_roster.py
file.249.verdict=reviewed
file.250.path=tests/integration/test_hugo_scaffold_scenarios.py
file.250.verdict=reviewed
file.251.path=tests/integration/test_sdd_house_keeping_flow.py
file.251.verdict=reviewed
file.252.path=tests/integration/test_sdd_loop_efficiency_regression.py
file.252.verdict=reviewed
file.253.path=tests/integration/test_sdd_loop_efficiency_runner.py
file.253.verdict=reviewed
file.254.path=tests/integration/test_session_kill_reattach.py
file.254.verdict=reviewed
file.255.path=tests/integration/test_temp_team_worktree_queue.py
file.255.verdict=reviewed
file.256.path=tests/integration/test_worktree_integration_queue.py
file.256.verdict=reviewed
file.257.path=tests/integration/test_wp_coordination_dry_runs.py
file.257.verdict=reviewed
file.258.path=tests/script_api.py
file.258.verdict=reviewed
file.259.path=tests/unit/test_audit_plan_changes.py
file.259.verdict=reviewed
file.260.path=tests/unit/test_audit_test_budget.py
file.260.verdict=reviewed
file.261.path=tests/unit/test_concurrency_check_engine.py
file.261.verdict=reviewed
file.262.path=tests/unit/test_decomposition_check.py
file.262.verdict=reviewed
file.263.path=tests/unit/test_derive_live_log.py
file.263.verdict=reviewed
file.264.path=tests/unit/test_doc_consistency_rules.py
file.264.verdict=reviewed
file.265.path=tests/unit/test_docs_obligation_reuse.py
file.265.verdict=reviewed
file.266.path=tests/unit/test_docs_utils_carriers.py
file.266.verdict=reviewed
file.267.path=tests/unit/test_docs_utils_obligation.py
file.267.verdict=reviewed
file.268.path=tests/unit/test_flow_class_check.py
file.268.verdict=reviewed
file.269.path=tests/unit/test_flow_class_spec_key.py
file.269.verdict=reviewed
file.270.path=tests/unit/test_glossary_utils.py
file.270.verdict=reviewed
file.271.path=tests/unit/test_isomorphism_checker.py
file.271.verdict=reviewed
file.272.path=tests/unit/test_overlap_check.py
file.272.verdict=reviewed
file.273.path=tests/unit/test_pre_analyze_check.py
file.273.verdict=reviewed
file.274.path=tests/unit/test_reconciler_extensions.py
file.274.verdict=reviewed
file.275.path=tests/unit/test_workspace_guard.py
file.275.verdict=reviewed
file.276.path=tests/unit/test_wp_gate.py
file.276.verdict=reviewed
file.277.path=tests/unit/test_wp_report.py
file.277.verdict=reviewed
<!-- coverage-receipt:end -->
