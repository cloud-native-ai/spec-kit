# Contract: 全量测试预算与定向测试（test-budget）

**Feature**: 063 → Feature 058（演化）
**FR 覆盖**: FR-011…FR-019
**载体**: `references/efficiency-model.md`、`references/stage-prompts.md`、`scripts/audit-test-budget.py`、`docs/reference/skills/sdd-loop-driver.md`

- **TB-01（全量定义与作用域）**: 「全量测试运行」= 以项目规范测试运行器执行、不带路径/测试过滤器的完整套件。预算以**运行线**为作用域：每线独立台账与两个槽位，多线并行互不共享或消耗；「每特性运行」指一条运行线的端到端运行（FR-011）。
- **TB-02（恰两个槽位）**: 每线全量预算 MUST 恰好为两个槽位：`baseline`（implement 起点，按名称捕获失败名单）与 `closure`（最终收口，与基线做名称级回归比较，位于 review 通过之后、合并之前，由驱动或其派发的独立校验单元执行）（FR-011）。
- **TB-03（baseline 程序）**: `implement` 阶段提示词 MUST 要求在执行首个任务前运行一次全量套件，使用项目规范 runner 的 `--names-out`（本仓 = `scripts/bash/run-tests.sh --names-out <spec-dir>/baseline-failed.txt`），并写入 E2 台账与 E3 证据：命令、rc、passed/failed、失败名单路径。E2 baseline 行 MUST 最终出现在 `state_spine_path`（E8 U0 入口声明）指向的状态脊围栏中：本地拓扑（`spine_write_mode=direct`）可执行侧直接追加；远端拓扑（`transport`）执行侧只写 `<spec-dir>/test-evidence/implement.jsonl` 传输行与名称名单，驱动 MUST 在 U4 后把它合并进状态脊并记录 `merge_source`/`merged_at`；传输行在合并前 MUST NOT 作为台账或审计来源，执行侧 MUST NOT 创建第二份台账。`implement` 阶段内 MUST NOT 再运行第二次全量套件（其内部回归比较义务改由收口槽位承担；确需全量必须按槽外例外记录）。closure 修复重入 MUST 携带 `baseline_slot=skip(closure-repair)`，MUST NOT 再消耗 baseline 槽位。
- **TB-04（closure 程序）**: 收口全量 MUST 使用同一规范 runner 与 `--names-out <spec-dir>/final-failed.txt`；回归比较 MUST 为名称级差集（`comm -13 baseline final` 或等价），MUST NOT 以通过计数比较替代（FR-014/FR-015）。新失败 MUST 被修复或显式归因（既有失败/无关/不稳定 + 证据）。
- **TB-05（中间阶段定向集与固定选择程序）**: `clarify` / `plan` / `tasks` / `checklist` / `analyze` 与 `review` MUST 只运行定向测试集；选择 MUST 由固定程序 `targeted-set-v1` 执行并记录依据，MUST NOT 凭印象（FR-012/FR-013）。本条款是算法定义的唯一 owner；技能面载体 `references/efficiency-model.md` §2.3 MUST 与本算法一致并由契约测试钉住。
  - **输入**：`stage_base`（阶段起点提交）、`spec_dir`、`changed_paths`（`git diff --name-only --diff-filter=ACMR <stage_base>..HEAD` 与 `git status --porcelain` 的路径并集）、`test_roots`（`tests/unit`、`tests/contract`、`tests/integration`、`tests/scenarios`）。
  - **(a) 改动路径覆盖**：候选文件 = `find <test_roots> -type f -name 'test_*.py' | LC_ALL=C sort`；对每个不在 `test_roots` 下的 `changed_path`，选中内容包含该仓库相对路径或其模块 stem（basename 去扩展名）的候选文件（`grep -lF` 固定字符串匹配，不做模糊匹配）。
  - **(b) 交付物契约测试**：本特性短名从 `spec_dir` 目录名去掉编号前缀派生；选中内容包含该短名或交付面路径（`skills/external/sdd-loop-driver`、`docs/reference/skills/sdd-loop-driver.md`）的契约/集成测试。
  - **(c) 夹具变更**：`changed_path` 在 `test_roots` 下时选中该文件自身；在 `tests/fixtures/` 下时选中内容引用该夹具路径的测试文件。
  - **排序与输出**：所选路径去重后按 `LC_ALL=C sort -u` 排序；输出为每行一个仓库相对测试路径的纯文本（stdout），供 E3 的 `selected_paths[]` 原样记录。
  - **复现性**：同一 `stage_base` + 同一工作树状态 MUST 产生同一集合；阶段 MUST 记录完整命令、`stage_base`、输出文本（或摘要 + 哈希）与充分性说明。不同阶段 MUST NOT 使用不同选择命令。
  - **空集**：按 TB-06 的 `empty-selection-escalated` 处置。
- **TB-06（定向证据字段）**: 每次定向运行 MUST 记录：命令、选择依据（规则 + 命令输出摘要）、所选路径、充分性说明、rc、passed/failed、新增失败、比较基线（E3）。`selected_paths` 为空且本阶段改动可执行面 → MUST 扩大同族范围或按显式例外升级为全量，并记录原因；仅文档改动时 MUST 记录 `not-run-docs-only` 与 `changed_paths[]` 改动路径证据（FR-013/FR-014）。`not-run-docs-only` 按缩减字段集判定完整：`stage`、`row_type=stage-status`、`status`、`selection_basis`、`changed_paths[]`、`evidence_ptr` 六项；运行字段（命令、rc、计数、新增失败、基线）不适用，MUST NOT 报 `unknown`。快车道按 FR-001 授权跳过 `checklist` 时，该阶段不产生定向运行，E3 MUST 记录 `status=not-applicable-skipped-stage`（[[STR-008]]），以 E1 准入记录与 [[STR-003]] 为联结证据；MUST NOT 记为 `unknown`，MUST NOT 计入 SC-005 完整性分母。
- **TB-07（台账格式与审计）**: 台账 MUST 以状态脊内 JSONL 围栏承载（E2），字段至少含槽位、阶段、目的、执行序号、触发、时间；`scripts/audit-test-budget.py` MUST 在收口审计：槽位数、槽外例外、槽内重跑、环境失败、缺失证据报告 `unknown`（MUST NOT 记为零或补造），并输出可粘贴进收尾汇总的摘要（FR-017）。审计 MUST 支持 `--logs-dir` 扫描阶段日志中的全量 runner 命令：日志中出现但台账未入账的全量命中 → 违规；日志缺失 → `unknown`，MUST NOT 当零。收口审计 MUST 以 E1 准入记录与 [[STR-003]] 联结识别授权跳过阶段，将其计为 [[STR-008]] 而非 `unknown`，且不计入 SC-005 完整性分母。审计 MUST 逐阶段检查每个适用阶段恰有一条 `row_type=stage-status` 的 E3 行：缺行 → 计入完整性分母并判未完整（MUST NOT 静默缩小分母）；`not-run-docs-only` 按 TB-06 的缩减字段集判完整；摘要 MUST 输出 `stages=N complete=N`（N = 适用阶段总数，含文档型阶段）。跨拓扑合并的 E2 行 MUST 记录 `merge_source`/`merged_at`，审计 MUST 校验其槽位语义与直接写入一致。
- **TB-08（槽外例外与槽内重跑）**: 槽外全量 MUST 仅以 `out-of-slot-exception` 形式出现，必须记录原因与证据（定向集不足、共享引擎被改动、无法解释的失败等），收尾汇总 MUST 列出例外次数与原因。最终收口因修复新失败而重跑同一套件 MUST 记为 `in-slot-rerun`（含触发与证据），不另开槽；MUST NOT 静默超预算（FR-016）。
- **TB-09（环境失败）**: 在收集/执行任何测试前即失败的调用（解释器或依赖缺失、收集前错误）MUST 记为 `environment-failure`，不消耗槽位，必须附证据；任何实际执行了测试的调用（含 0 tests collected 的选择失败）MUST 消耗槽位（FR-018）。
- **TB-10（编排层实现）**: 本预算 MUST 在编排层实现（阶段提示词 + 状态脊台账 + 收口审计），MUST NOT 依赖修改框架命令内部流程（FR-019）。

## 可追溯性

| 条款 | FR | 计划测试 |
|------|-----|----------|
| TB-01 | FR-011 | `test_tb_01_full_run_definition` |
| TB-02 | FR-011, SC-003 | `test_tb_02_two_slots_only` |
| TB-03 | FR-011, FR-014 | `test_tb_03_baseline_prompt`；集成 `test_sdd_loop_efficiency_regression.py`；远端传输/合并用例 |
| TB-04 | FR-014, FR-015, SC-004 | `test_tb_04_name_level_diff`；集成回归注入夹具 |
| TB-05 | FR-012, FR-013 | `test_tb_05_targeted_selection_rule` |
| TB-06 | FR-013, FR-014, SC-005 | `test_tb_06_evidence_fields`；`test_tb_06_docs_only_reduced_fields` |
| TB-07 | FR-017, SC-005 | `test_tb_07_ledger_audit_unknown`；单测 `test_audit_test_budget.py`（含 `stages=N complete=N` 与缺失 stage-status 行） |
| TB-08 | FR-016, SC-003 | `test_tb_08_exception_and_rerun` |
| TB-09 | FR-018 | `test_tb_09_environment_failure_no_slot` |
| TB-10 | FR-019 | `test_tb_10_orchestration_layer_only` |
