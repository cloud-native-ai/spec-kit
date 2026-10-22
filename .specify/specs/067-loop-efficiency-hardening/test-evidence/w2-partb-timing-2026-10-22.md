# W2 Part B Family Timing — before/after — 2026-10-22

**Tasks**: T008 + T009 + T010 + T011 + T012 (implement part B)
**Premise**: RC-07 钩子中和（T003）与 implement 起点槽位（T007，commit `e95a5920`）已落地；本 part 全部计时运行于树 `50a56fea`。
**Decision rule applied**（part brief 第 1 条，先测后改）: 每家族先跑一次定向计时；若已落入 plan §W2 设计带 → 记录 "already in band after RC-07; no change"，不制造改动。四个家族的判定计时全部落带（或低于带），**本 part 零代码改动**；T012 复测列为同树复核读数，非改动后验证。

## Commands actually run (targeted only; no full suite — T007/T034 是唯二全量槽位)

| # | command | when | exit | wrapper wall |
|---|---|---|---|---|
| R1 | `bash scripts/bash/run-tests.sh tests/integration/test_worktree_integration_queue.py -q --durations=0` | 判定计时（before 列） | 0 | 22 s |
| R2 | `bash scripts/bash/run-tests.sh tests/contract/test_workspace_isolation_contract.py -q --durations=0` | 判定计时 | 0 | 32 s |
| R3 | `bash scripts/bash/run-tests.sh "tests/contract/test_store_state_protocol.py::TestTwoBranchMerge" -q --durations=0` | 判定计时 | 0 | 5 s |
| R4 | `bash scripts/bash/run-tests.sh tests/unit/test_audit_plan_changes.py tests/unit/test_loop_state_engine.py -q --durations=0` | 判定计时 | 1（基线内失败，见 §T011） | 24 s |
| R5 | 同 R1 | T012 复测列 | 0 | 18 s |
| R6 | 同 R2 | T012 复测列 | 0 | 30 s |
| R7 | 同 R3 | T012 复测列 | 0 | 6 s |
| R8 | 同 R4 | T012 复测列 | 1（同名基线内失败） | 22 s |
| R9 | 同 R3 | T010 方差第 3 样本 | 0 | 4 s |

R1–R4 与 R5–R8 之间树零改动（无任何代码/夹具提交）。

## T008 · worktree queue（6 条；基线 53.8 s；带 12–18 s）

| node id（后缀） | 基线 call | R1 call | R5 call |
|---|---|---|---|
| test_integration_executor_merges_queue_and_replay_is_identical | 27.13 | 8.91 | 6.61 |
| test_integration_executor_failure_retains_worktree_and_continues | 8.62 | 2.84 | 3.46 |
| test_disjoint_write_lines_commit_concurrently | 7.04 | 1.74 | 1.39 |
| test_integration_executor_refuses_preexisting_rebase | 4.05 | 1.16 | 1.31 |
| test_failed_integration_retains_worktree_and_records | 3.74 | 1.33 | 0.99 |
| test_runtime_archive_once_before_removal | 3.26 | 1.14 | 0.53 |
| **6 条合计** | **53.84** | **17.12** | **14.29** |

文件整轮：R1 = 9 passed in 20.43 s；R5 = 9 passed in 17.19 s。
**Verdict: already in band after RC-07; no change**（17.12 / 14.29 ∈ [12, 18]）。

## T009 · workspace isolation（3 条；基线 13.5 s；预期带 5–6 s）

| node id（后缀） | 基线 call | R2 call | R6 call |
|---|---|---|---|
| test_p0_merged_requires_real_head_containment | 6.19 | 1.36 | 1.16 |
| test_p0_merged_u6_close_unblocks_waiter | 4.27 | 1.93 | 1.73 |
| test_wi_13_deterministic_queue | 3.08 | 1.42 | 1.28 |
| **3 条合计** | **13.54** | **4.71** | **4.17** |

文件整轮：R2 = 46 passed in 31.96 s；R6 = 46 passed in 29.40 s。
**Verdict: below the predicted band after RC-07; no change**（4.71 / 4.17 均低于 5–6 预测带下缘——实际回收超过 plan 预估；带是预估区间而非下限，目标已达成，不制造改动）。

## T010 · store-state two-branch merge（1 条；基线 8.92 s；带 ≤4 s）

`TestTwoBranchMerge::test_branch_merge_yields_zero_conflicts_and_both_entries`：

| 读数 | call | 整轮 |
|---|---|---|
| 基线 | 8.92 | — |
| R3（判定计时） | 3.43 | 1 passed in 3.64 s |
| R7（复测） | 4.98 | 1 passed in 5.32 s |
| R9（第 3 样本） | 3.11 | 1 passed in 3.37 s |

**Verdict: no change**——判定计时（brief 第 1 步的决定输入）3.43 s 落带 ≤4 s。R7 的 4.98 s 超带读数如实记录并归因：该用例含 2×1.1 s 硬编码 sleep（跨文件名秒界的确定性等待，测试内注释声明）+ 3 次 `feedback-utils.py` 子进程冷启动，零代码改动下两轮相差 1.55 s，为子进程冷启动/文件缓存方差；夹具侧手段（base 仓 + 克隆）最多再省 ≈0.3 s 仓库构建份额，对 2.2 s 固定 sleep 不构成达带杠杆。三样本 2/3 落带；**本记录不声称该家族稳定落带**（如需达标主张，以 T034 closure 槽位复验为准，MP-08）。

## T011 · audit_plan_changes + loop_state（4 条慢条；带 ≤5 s）

| node id | 基线 call | R4 call | R8 call |
|---|---|---|---|
| test_audit_plan_changes.py::test_accumulated_minor_edits_use_final_diff | 5.22 | 0.66 | 0.67 |
| test_audit_plan_changes.py::test_multi_commit_touch_set | 4.41 | 0.62 | 0.67 |
| test_loop_state_engine.py::test_implement_document_only_commit_is_not_complete | 4.72 | 0.92 | 0.82 |
| test_loop_state_engine.py::test_derived_spine_state_wins_over_terminal_evidence | 3.53 | 0.81 | 0.78 |
| **4 条合计** | **17.88** | **3.01** | **2.94** |

两文件整轮：R4 = 1 failed, 65 passed in 23.58 s；R8 = 1 failed, 65 passed in 21.44 s。
**Verdict: already in band after RC-07; no change**（3.01 / 2.94 ≤ 5 s）。
口径注：brief 写「基线合计 ≈13 s」，dated durations 记录中上述 4 条命名慢条合计实为 17.88 s；本对照严格按同 4 条 id 同法取数（entry 级 like-for-like），两种口径下结论一致（均落带）。

### loop_state 3 条基线失败用例的观察（如实记录，非本 part 处置对象）

三条名册内失败（T007 in-stage 清单 `baseline-failures-2026-10-22-implement-start.txt` 全部在册，已逐名 grep 核对）在 R4/R8 定向运行中的实测状态：

- `test_terminal_states_with_unknown_commit_baseline_never_verify` — **失败**（两轮均失败，与其 in-stage 基线状态一致；同名出现在 R4/R8 FAILED 行）。
- `test_unwatched_detector_positive_expired_and_negative` — 通过（R4 0.50 s；定向运行形态）。
- `test_watchbeat_marker_projection_and_freshness` — 通过（定向运行形态）。

后两条在全量套件上下文失败、定向运行通过，呈顺序/状态依赖形态。**本 part 对这三个 id 零触碰**（零代码改动，T011 的「夹具改动不得成为失败原因」约束以零改动方式满足）；其 triage 归 T027，本记录不声称任何修复或转绿。

## RC-07 env 经引擎/执行器子进程继承生效的核对（T008 任务行要求）

- **静态核对**：`tests/fixtures/line_fixtures.py` `base_env()` 在调用时复制 `os.environ`（引擎子进程 env 来源，`run_engine()` 原样传入 `subprocess.run`）；conftest autouse fixture 经 `monkeypatch.setenv` 改写进程 `os.environ` → 引擎子进程继承 `GIT_CONFIG_GLOBAL/SYSTEM`。worktree 用例的 `_execute()`（integrate-lines.py 执行器）以无 `env=` 的 `subprocess.run` 启动 → 整体继承测试进程 env。
- **行为佐证**：回收幅度与钩子税份额吻合（6 条合计 53.84 → 17.12/14.29 s；最大条 replay 27.13 → 6.61–8.91 s，其成本主体为执行器内部 git 操作），与「引擎子进程内提交免钩子」的预期方向、量级一致。

## 台账与禁改面

- **Ledger: no ledger changes** — 本 part 零用例合并/改写/删除，`test-evidence/test-consolidation-ledger.md` 未追加行（LED-01…LED-03 追加式纪律无触发项）。
- 禁改面合规：本 part 未改动 `src/`、`scripts/`、`pyproject.toml`、镜像面、注册表、`requirements.md`、`plan.md`、任何测试文件（含 brief 点名的 5 个测试文件——零改动）。产物仅本证据文件 + `tasks.md` 中 T008–T012 的状态复选框。
- 未运行面：全量套件未运行（槽位纪律）；brief 点名 5 个测试文件之外的任何家族未运行。

## 口径与限制（诚实声明）

- 本页全部数字为 implement 期定向计时（runner 透传 pytest `--durations=0`，单次运行），非 MP-02 冷缓存口径；达标主张只认 closure 槽位（MP-08），本页不构成 SC-006 主张。
- 未改动任何代码，故 before/after 列之差为同树运行方差（R1–R4 vs R5–R9），不代表改动收益。
