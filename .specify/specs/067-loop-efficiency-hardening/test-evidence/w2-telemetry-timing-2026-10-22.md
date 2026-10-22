# W2 Part C Family Timing — before/after — 2026-10-22

**Tasks**: T013 + T014 (implement part C · trigger telemetry 进程内动作化)
**Premise**: RC-07 钩子中和与 T007 implement 起点槽位已落地;R-C1 判定计时运行于树 `12e05cf0`(引擎侧零改动,RC-07 后该家族仍高于 plan 带);R-C2/R-C3 复测运行于「`12e05cf0` + 本 part 唯一代码改动 = `tests/integration/test_trigger_telemetry.py` 改写」的工作树,该改动随后作为提交 `e30ea169` 落地(运行先于提交,内容一致)。
**Decision applied**(part brief 第 1 条): C 家族为强制改写面(不适用 no-op 分支)——消除 60+ 次引擎子进程冷启动,保留真 CLI 子进程冒烟钉住。

## 改写内容(T013)

- importlib 载入 `scripts/python/trigger-utils.py`,进程内直调 `main(argv)`(套件既有模式,同 `test_trigger_engine.py`);**引擎文件零改动**(禁改面遵守)。
- 每次进程内调用显式传 `--workspace`(进程内调用没有子进程 CWD 可依;pytest CWD 是仓库根,不得参与 root 解析——这是进程内化的关键正确性点)。
- 动作间显式状态重置:`reset_engine_state()` 在运行器切换工作区(即每个用例边界)时对新命名空间重执行引擎模块(FR-016)。事实基础:引擎模块级仅声明不可变常量,全部可变状态在工作区文件内、argparse parser 每次 `main()` 重建(grep 核对:无 `global`、无缓存);重执行式重置使「未来引擎若引入模块级可变态」也无法跨用例泄漏。
- 新增 `test_cli_subprocess_smoke_pins_payload_and_exit_semantics`:≥1 条真 CLI 子进程冒烟(3 次真实 `sys.executable` 起进程),钉 9 键 envelope 形状、分级退出码(0/1)、`ok/errors` 形状,并以同 argv 在孪生工作区断言子进程 ↔ 进程内 envelope 等价(仅归一 `generatedAt`/`workspaceRoot`,FR-020)。
- 12 条既有用例 id 与断言集零改动,仅换执行机制(subprocess → 进程内);台账 12 行 retained 随本提交回填。

## Commands actually run (targeted only; no full suite — T007/T034 是唯二全量槽位)

| # | command | when | exit | wall |
|---|---|---|---|---|
| R-C1 | `bash scripts/bash/run-tests.sh tests/integration/test_trigger_telemetry.py -q --durations=0` | 改写前判定计时(before 列) | 0 | 23.36 s(pytest) |
| R-C2 | 同 R-C1 | 改写后复测(after 列) | 0 | 1.14 s |
| R-C3 | 同 R-C1 | 方差第 2 样本 | 0 | 0.84 s |

## 逐条时长对照(12 条既有 id + 新增冒烟)

| node id(后缀) | 基线 call(T007 全量)* | R-C1 call | R-C2 call |
|---|---|---|---|
| test_row_count_never_exceeds_the_window | 6.22 | 5.64 | 0.06 |
| test_rotation_loses_no_rule_state | 7.39 | 5.47 | 0.06 |
| test_sixty_turns_then_rotate_keeps_at_most_the_window | 6.31 | 5.38 | 0.06 |
| test_unrelated_turns_produce_no_visible_output | — | 1.69 | 0.02 |
| test_rotate_keeps_the_most_recent_rows | — | 0.98 | 0.01 |
| test_escalation_rate_is_computed_over_session_turns | — | 0.89 | 0.01 |
| test_rotate_does_not_touch_index_file | — | 0.63 | 0.01 |
| test_consecutive_survives_window_shrink | — | 0.60 | 0.01 |
| test_every_assess_writes_exactly_one_row | — | 0.56 | 0.01 |
| test_escalation_over_budget_is_flagged | — | 0.39 | <0.005 |
| test_probe_budget_is_configurable | — | 0.08 | <0.005 |
| test_telemetry_is_git_ignored_but_index_is_not | — | 0.03 | 0.02 |
| **12 条既有合计** | — | **17.32** | **~0.20** |
| test_cli_subprocess_smoke_pins_payload_and_exit_semantics(新增) | — | — | 0.29 |

\* 基线列取自 `baseline-durations-2026-10-22.txt` 全量运行(top-50 仅含 3 条重头);R-C1 列为 RC-07 后、本 part 改写前的同文件定向读数。

## 结果

- **T013 目标 3 条(sixty-turns / row_count / rotation_loses_no_rule_state)**:R-C1 合计 16.49 s → R-C2 合计 **0.18 s**。plan 预期带 4–6 s,实测**低于带下缘**(进程内直调的回收超出预估——解释器冷启动占比比 plan-probes P-3 估计更高)。
- **家族整轮**:12 passed in 23.36 s → **13 passed in 1.14 s**(R-C3 0.84 s);状态脊预期「telemetry ≤6 s family」达成(低于 1.2 s)。
- **CLI 冒烟钉住核对**(T014 任务行要求):冒烟用例经 `subprocess.run([sys.executable, ENGINE, ...])` 真实起进程 3 次(0.29 s call 时长与 3 次解释器冷启动量级一致);钉住内容 = 9 键 envelope 集合、`--action init` 退出 0 + `ok:true`、`--action bogus` 退出 1 + `ok:false`、非特征 assess 建议 `null`、孪生工作区同 argv 进程内/子进程 envelope 等价。
- **进程内全局态无跨用例泄漏证据**:重置 helper 在每次工作区切换时对新命名空间重执行引擎模块(结构性保证);12 条用例 + 冒烟在 R-C2/R-C3 两轮全部通过,其中 SC-015 字节级对照用例(rotation_loses_no_rule_state)通过即学习计数器无泄漏的行为佐证。

## 台账

- `test-evidence/test-consolidation-ledger.md` 追加 **12 行 retained**(12 条既有 id,机制改写:subprocess → 进程内直调;id 与断言集零改动)+ **1 条 LED-08 reportive 注**(新增冒烟 id 为 post-only 覆盖,无基线 id 消失,不占行)。

## 口径与限制(诚实声明)

- 本页数字为 implement 期定向计时(单次/两次运行),非 MP-02 冷缓存口径;达标主张只认 closure 槽位(T034),本页不构成 SC-006 主张。
- R-C2/R-C3 运行时该测试文件尚未提交;提交 `e30ea169` 与运行树内容一致(无运行后改动)。
- 13 passed 中含新增冒烟用例;「未运行面」:本 part 未运行全量套件,未运行其他家族。
