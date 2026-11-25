# Contract: 迁移与兼容（migration-and-compat）

**Feature**: 107-decision-governance → Feature 107 Decision Governance（AI Agent 决策项治理）
**FR 覆盖**: FR-027…FR-029
**载体**: `shared/definitions/decision-definitions.md` § Legacy & Migration；`plan.md` § Backward-Incompatible Change Inventory（封闭清单 owner）；`templates/commands/migrate.md` + `specify migrate`（既有收敛引擎，本特性不新增维度）。

本契约把「旧记录怎么办」变成可执行、可测试的命题：新契约只约束落地后新建的记录，旧记录零改写、报告 `legacy`；任何不兼容形态都有迁移或确定性拒绝，不靠运行时双路径回退或人工说明。

## 条款

- **C-501** (closed inventory): the backward-incompatible change inventory MUST be the closed set `{BC-01…BC-06}` declared in `plan.md`; every row MUST name its migration or deterministic-refusal behavior and the test that pins it; an unmapped row or a row outside the set MUST turn the mapping guard red. (FR-029, SC-009)
- **C-502** (no retroactive rewrite): the base corpus at `08b59695c` — `T-NNN` records, checkpoint files, run-report bodies, register `D-…`/`T-…` rows, clarifications and review/analyze report bodies — MUST NOT be rewritten; the acceptance reading is an empty `git diff 08b59695c..HEAD` over those paths; a legacy record MUST be reported `legacy` and MUST NOT be judged invalid. (FR-028)
- **C-503** (BC-04 via the existing migrate dimension): the new instruction section MUST reach an initialized workspace through `/speckit.migrate`'s existing `templates-generated` dimension — a dry-run `specify migrate --format json` MUST list the `.specify/instructions.md` convergence item; the feature MUST NOT add a migrate dimension, command or second planner. (FR-029)
- **C-504** (BC-02 refusal at the contract boundary): a decision-backed dispatch without a decision block MUST be refused deterministically at payload construction (M-06); a non-decision dispatch without a block stays legal; legacy payloads MUST NOT be rewritten. (FR-029)
- **C-505** (no fallback-only resolution): no row may be resolved solely by a runtime dual-path fallback or a manual instruction; every row MUST map to an executable migration or a deterministic refusal with a test and an evidence pointer. (FR-029)
- **C-506** (mirror/copy closure in the same change): mirrors MUST be regenerated in the same change and judged against the measured baseline — `sync-mirrors.py --check` with no NEW drift (`test-evidence/sync-mirrors-baseline.txt`, rc 0) and `regen-command-copies.py --check` rc 0; the instruction template and the generated live file MUST agree on the new section (`cmp` on the extracted section) and stay inside the declared section cap and the raised total budget (T-001). (FR-026, FR-027, SC-008)

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| C-501 | FR-029, SC-009 | `test_decision_governance_migration_map.py::test_bc_row_set_closed_and_mapped` |
| C-502 | FR-028 | `test_decision_governance_migrate_dryrun.py::test_base_corpus_zero_rewrite` |
| C-503 | FR-029 | `test_decision_governance_migrate_dryrun.py::test_instructions_generated_dimension` |
| C-504 | FR-029 | `test_decision_governance_guards.py::test_m06_dispatch_without_block_refused` |
| C-505 | FR-029 | `test_decision_governance_migration_map.py::test_no_fallback_only_row` |
| C-506 | FR-026, FR-027 | `test_decision_governance_contracts.py::test_mirror_and_copy_closure` |

## FR 覆盖核对

- FR-027…FR-029 由本文件 C-501…C-506 承接；SC-008 / SC-009 的读数在实现与 review 各测一次。
- `/speckit.migrate` 的维度闭集不被本特性扩宽；迁移行为只消费既有 `templates-generated` 维度与既有拒绝面。
