# Closure 全量验证结果（dogfood worker）

- 运行戳: r20261106T093000Z-dogfood
- 日期: 2026-11-06
- 全量运行次数: 1（closure 槽位，仅此一次）

## 命令

```
timeout 590 bash scripts/bash/run-tests.sh --names-out .specify/specs/087-speckit-visualization/final-failed.txt > .specify/specs/087-speckit-visualization/test-evidence/closure-full-suite-20261106T130128Z.log 2>&1
```

## 结果

- rc: 1（存在失败用例；timeout 590 未触发，套件自然结束）
- passed / failed / skipped: **7662 / 58 / 1**
- 耗时: **435.06s（0:07:15）**（pytest 报告值；满足 SC-001 >90 秒真实任务要求）
- 日志: `.specify/specs/087-speckit-visualization/test-evidence/closure-full-suite-20261106T130128Z.log`
- failed-name 清单: `.specify/specs/087-speckit-visualization/final-failed.txt`（58 条，运行器写入）

## 名称级比较（baseline-failed.txt 27 条 vs final-failed.txt 58 条）

- 新增失败（comm -13）: **31**
- 修复（comm -23）: **0**

### 新增失败名单（31）

- tests/contract/test_bilingual_expression.py::test_drift_str_literal_unique_consumers
- tests/contract/test_client_guard_sweep.py::test_c57_shipped_text_adds_no_fresh_neutrality_violation
- tests/contract/test_coaching_wiring_contract.py::test_c3_mirrors_and_command_copies_are_zero_drift
- tests/contract/test_coaching_wiring_contract.py::test_c3_probe_compiled_face_is_zero_drift
- tests/contract/test_coaching_wiring_contract.py::test_c8_the_verification_surface_runs_green
- tests/contract/test_compile_propagation_order.py::test_propagation_chain_is_green_in_canonical_order
- tests/contract/test_delegation_classes.py::test_every_template_edge_is_same_class_or_neutral_exempt
- tests/contract/test_expression_compatibility.py::test_c1_zero_new_commands
- tests/contract/test_expression_gate_wiring.py::test_a6_wiring_inventory_matches_the_frozen_denominator
- tests/contract/test_feedback_command_classification.py::test_complex_set_equals_measured_feedback_carriers
- tests/contract/test_feedback_command_classification.py::test_table_covers_every_command_template
- tests/contract/test_flow_class_ledger.py::test_check_reports_79_units_and_zero_gaps
- tests/contract/test_flow_class_ledger.py::test_ledger_has_79_rows_covering_inventory_bidirectionally
- tests/contract/test_flow_class_ledger.py::test_templates_and_skills_never_assign_class_key
- tests/contract/test_goal_migration.py::TestLiveSurfacesAreMigrated::test_no_live_face_file_retains_the_old_path
- tests/contract/test_humanize_command_surface.py::test_wc16_command_roster_unchanged
- tests/contract/test_ledger_reconciliation.py::test_real_tree_reconciles_clean_with_the_declared_coverage_numbers
- tests/contract/test_migration_distribution.py::test_command_template_name_set_matches_frozen_baseline
- tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[scripts/python/measure.py->.specify/scripts/python/measure.py]
- tests/contract/test_mirror_parity_suite.py::test_mirror_file_byte_identical[scripts/python/status-digest.py->.specify/scripts/python/status-digest.py]
- tests/contract/test_probe_nonentity_catalog.py::test_catalog_does_not_participate_in_registry_counts
- tests/contract/test_qoder_command_frontmatter.py::test_every_template_has_short_description
- tests/contract/test_reporting_obligations.py::test_c47_each_scanned_fact_has_exactly_one_definition_site
- tests/contract/test_reporting_obligations.py::test_c47_the_ownership_table_is_readable_and_names_its_delivered_owners
- tests/contract/test_reporting_obligations.py::test_c48_the_new_owner_is_declared_as_owning_and_nothing_else
- tests/contract/test_reporting_obligations.py::test_c48_the_two_relation_tables_describe_the_same_documents
- tests/contract/test_run_skills_wiring.py::test_c9_compile_embeds_zero_drift_75_units
- tests/contract/test_scripts_distribution_parity.py::TestScriptsDistributionParity::test_repo_has_no_orphan_or_drifted_scripts
- tests/contract/test_sdd_compat_containment.py::test_c11_the_flow_class_inventory_stays_clean
- tests/contract/test_shipped_surface_client_neutrality.py::test_shipped_surface_has_no_framework_runtime_references
- tests/contract/test_trigger_engine.py::test_c2_sync_mirrors_check_clean

### 修复名单（0）

（无）

## 观察备注（如实记录）

- baseline 27 条失败在本轮全部仍在失败（fixed=0），另新增 31 条；新增失败集中在 mirror parity / sync-mirrors / 分布一致性类 contract 测试（如 `scripts/python/measure.py`、`status-digest.py` 镜像字节不一致），疑似工作树内存在未同步的镜像漂移。
- 本席位边界：只记录事实与名单，不做修复判断。
