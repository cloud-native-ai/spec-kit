# Closure 全量验证结果 r2（dogfood worker，in-slot rerun）

- 运行戳: r20261106T100000Z-dogfood-r2
- 日期: 2026-11-06
- 槽位性质: closure 槽位内的 in-slot rerun（trigger = 镜像漂移与预期增量修复）
- 全量运行次数: **1（本 rerun 仅此一次，未再跑第二次）**

## 命令

```
rm -f .specify/specs/088-speckit-visualization/test-evidence/dogfood-worker-done-r2.flag
timeout 590 bash scripts/bash/run-tests.sh --names-out \
  .specify/specs/088-speckit-visualization/final-failed-r2.txt \
  > .specify/specs/088-speckit-visualization/test-evidence/closure-full-suite-r2-20261106T144304Z.log 2>&1
```

## 结果

- rc: **1**（存在失败用例；`timeout 590` 未触发，套件自然结束）
- passed / failed / skipped: **7680 / 40 / 1**（另有 3 warnings）
- 耗时: **441.25s（0:07:21）**（pytest 报告值；进程墙钟 443s，含 runner 前置调用）
- 日志: `.specify/specs/088-speckit-visualization/test-evidence/closure-full-suite-r2-20261106T144304Z.log`
- failed-name 清单: `.specify/specs/088-speckit-visualization/final-failed-r2.txt`（40 条，run-tests.sh 写入）
- 与上一轮 closure（r1: 58 failed / 7662 passed / 435.06s）相比: 失败 **-18**，通过 **+18**

## 名称级比较（baseline-failed.txt 27 条 vs final-failed-r2.txt 40 条）

命令：`comm -13 <(sort baseline) <(sort final-r2)` / `comm -23 ...`

- 新增失败（comm -13）: **13**
- 修复（comm -23）: **0**
- 仍在失败（comm -12）: **27**（baseline 27 条全部仍在失败）

### 新增失败名单（13）及其实测根因

| # | 测试 | 日志实测断言 |
|---|------|--------------|
| 1 | `tests/contract/test_bilingual_expression.py::test_drift_str_literal_unique_consumers` | `STR-001 consumed at tests/contract/test_reporting_obligations.py` 逃出唯一消费点 |
| 2 | `tests/contract/test_client_guard_sweep.py::test_c57_shipped_text_adds_no_fresh_neutrality_violation` | 新引入框架运行时引用：`shared/guidelines/reporting-obligations.md`、`skills/internal/create-team/scripts/validate-roster.py`、`templates/commands/measure.md` |
| 3 | `tests/contract/test_delegation_classes.py::test_every_template_edge_is_same_class_or_neutral_exempt` | `commands_scanned` 应为 27，实测 29 |
| 4 | `tests/contract/test_expression_compatibility.py::test_c1_zero_new_commands` | 命令模板名集漂移：expected 27, found 29，对称差 `['measure', 'status']` |
| 5 | `tests/contract/test_expression_gate_wiring.py::test_a6_wiring_inventory_matches_the_frozen_denominator` | 模板清单 29，expected 27 |
| 6 | `tests/contract/test_feedback_command_classification.py::test_complex_set_equals_measured_feedback_carriers` | 右侧多出 `'measure'` |
| 7 | `tests/contract/test_feedback_command_classification.py::test_table_covers_every_command_template` | 表/模板漂移：未列模板 `['measure', 'status']` |
| 8 | `tests/contract/test_goal_migration.py::TestLiveSurfacesAreMigrated::test_no_live_face_file_retains_the_old_path` | 两个 live-face 日志仍引用迁移前路径：`test-evidence/baseline-full-suite-20261106T063158Z.log`、`test-evidence/closure-full-suite-20261106T130128Z.log` |
| 9 | `tests/contract/test_ledger_reconciliation.py::test_real_tree_reconciles_clean_with_the_declared_coverage_numbers` | 实测 83，声明 81 |
| 10 | `tests/contract/test_migration_distribution.py::test_command_template_name_set_matches_frozen_baseline` | `unexpected=['measure', 'status'] missing=[]` |
| 11 | `tests/contract/test_qoder_command_frontmatter.py::test_every_template_has_short_description` | `measure.md` short-description 55 字符，上限 50 |
| 12 | `tests/contract/test_run_skills_wiring.py::test_c9_compile_embeds_zero_drift_75_units` | 期望 `77 units`，实测 `79 units, zero drift` |
| 13 | `tests/contract/test_shipped_surface_client_neutrality.py::test_shipped_surface_has_no_framework_runtime_references` | `templates/commands/measure.md:19`、`shared/guidelines/reporting-obligations.md:149/184` 出现框架运行时引用 |

### 修复名单（0）

（无）

## 观察备注（如实记录，不做修复判断）

1. **同族收敛而非逐条独立**：13 条新增失败中，11 条归属于同一个载体族 —— 087 交付新增的两个命令模板 `measure`、`status` 落在多处"冻结分母"上（C-1 零新增命令、A-6 wiring 分母、模板清单、feedback 分类表、delegation `commands_scanned`、run-skills 编译单元数 77→79、ledger 81→83），另 2 条是 `measure.md` / `reporting-obligations.md` 的客户端中立性引用。崩溃面是"087 自身交付物 vs 一批仍钉在旧分母的契约"，与 dispatch 所述"预期增量修复"一致；上一轮 r1 报出的 mirror parity / sync-mirrors 漂移类新增失败（`measure.py`、`status-digest.py`、`test_c2_sync_mirrors_check_clean`、`test_c3_mirrors_and_command_copies_are_zero_drift` 等 18 条）在本轮**全部转绿**，故失败数 58→40。
2. **修复数 0 的解释**：名称级 `comm -23` 为 0 是因为 baseline 27 条在本轮**全部仍在失败**（`comm -12` = 27），而 r1 新增的 18 条相对 baseline 本就不在其集合内，其转绿不进入 `comm -23`。因此"18 条转绿"只体现在计数（58→40）与失败名单差集，不体现在对 baseline 的 fixed 数上。
3. **一处由本 harness 自造的失败**：新增第 8 条（`test_no_live_face_file_retains_the_old_path`）的 offendor 是两个**测试日志**文件 —— 其中 `baseline-full-suite-20261106T063158Z.log` 在 r1 之前已存在，但该测试在 r1 时为绿、r2 时为红；两个文件都是 full-suite 日志（pytest 会打印引用旧路径的测试源码上下文）。该失败的载体是本运行的证据产物自身，而非框架源码；如实记录，不修改（超出本席位写域）。
4. **超时状态**：`timeout 590` 未触发（rc=1 为 pytest 自身退出码，非 124），套件自然结束。
5. **边界**：本席位只写 `test-evidence/dogfood-worker-*`、`final-failed-r2.txt`、`closure-full-suite-r2-*.log`；未提交、未 push、未写状态脊、未派发子代理。
