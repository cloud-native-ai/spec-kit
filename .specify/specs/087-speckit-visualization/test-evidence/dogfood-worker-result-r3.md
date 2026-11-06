# Closure 全量验证结果 r3（dogfood worker，in-slot final rerun）

- 运行戳: `r20261106T100000Z-dogfood-r3`
- 日期: 2026-11-06
- 槽位性质: closure 槽位内的**最终 in-slot rerun**（trigger = 跨特性冻结分母对齐 `fedc14d0`）
- 全量运行次数: **1（本轮仅此一次，未再跑第二次；无重跑、无重试）**

## 命令

```
rm -f .specify/specs/087-speckit-visualization/test-evidence/dogfood-worker-done-r3.flag
timeout 590 bash scripts/bash/run-tests.sh --names-out \
  .specify/specs/087-speckit-visualization/final-failed-r3.txt \
  > .specify/specs/087-speckit-visualization/test-evidence/closure-full-suite-r3-20261106T145846Z.log 2>&1
```

## 结果

| 项 | 值 |
|----|-----|
| rc | **1**（pytest 自身退出码；`timeout 590` **未触发**，非 124） |
| passed / failed / skipped | **7695 / 28 / 1**（另有 3 warnings，0 errors） |
| 耗时 | **441.53s（0:07:21）**（pytest 报告值）；进程墙钟 **444s**（runner 前置调用 +3s） |
| pytest 汇总行 | `28 failed, 7695 passed, 1 skipped, 3 warnings in 441.53s` |
| 日志 | `.specify/specs/087-speckit-visualization/test-evidence/closure-full-suite-r3-20261106T145846Z.log`（83921 B） |
| failed-name 清单 | `.specify/specs/087-speckit-visualization/final-failed-r3.txt`（28 条，run-tests.sh 写入） |

### 与历史轮次对比

| 轮次 | failed | passed | 耗时 | 新增 vs baseline | 修复 vs baseline |
|------|--------|--------|------|------------------|------------------|
| baseline | 27 | — | — | — | — |
| r1 (closure) | 58 | 7662 | 435.06s | +31 | 0 |
| r2 (in-slot rerun) | 40 | 7680 | 441.25s | +13 | 0 |
| **r3 (本次 final)** | **28** | **7695** | **441.53s** | **+1** | **0** |

r3 相对 r2：失败 **-12**，通过 **+15**。

## 名称级比较（baseline-failed.txt 27 条 vs final-failed-r3.txt 28 条）

命令：`comm -13 <(sort baseline) <(sort final-r3)` / `comm -23 ...` / `comm -12 ...`

| 分类 | 条数 |
|------|------|
| 新增失败（`comm -13`） | **1**（预期 0，**未达成**） |
| 修复（`comm -23`） | **0** |
| 仍在失败（`comm -12`，baseline ⊆ r3） | **27**（baseline 27 条全部仍在失败） |

### 新增失败名单（1 条，逐条列名、不修）

| # | 测试节点 |
|---|----------|
| 1 | `tests/contract/test_docs_step_injection.py::test_c2b_scope_is_classification_minus_verified_exclusions` |

日志实测断言（`closure-full-suite-r3-20261106T145846Z.log:577` 起）：

```
AssertionError: docs-sync scope drift — missing: ['measure', 'status']; extra: []
```

### 修复名单（0）

（无）

## 新增失败的唯一归因（实测，非推定）

**同一冻结分母族的**最后一个未被对齐的成员**，与 `fedc14d0` 处理的 13 条同族。**

- 机制实测（`python3 -c` 双模块取值）：
  - 属主侧 `test_feedback_command_classification.py::COMPLEX_COMMANDS` = **25** 条，**已含** `measure`/`status`（`fedc14d0` 已对齐）；
  - 消费者侧 `test_docs_step_injection.py::COMPLEX_COMMANDS` = **22** 条，**不含** `measure`/`status`；
  - 差集：`expected - local = ['measure', 'status']`，`local - expected = []`。
- `test_c2b` 的 `expected = classification_complex() - DOCS_STEP_EXCLUDED` 直接读属主集合，本地清单是**手维护的消费副本**——属主已被 `fedc14d0` 推进到 25，本副本未同步，故由绿转红。
- 时点证据：该测试在 r2 日志中为通过（`test_docs_step_injection.py ............................. [ 14%]`），r2 失败清单 40 条、r1 清单 58 条、baseline 27 条中**均不含**该节点（三次 `grep -c` = 0）——即回归由 `fedc14d0` 引入，非长期红。
- 该测试文件自身最近改动为 `7e738423`（063），与 087 无关——漂移在**消费副本**侧，不在被测源码。

**未修复原因（边界）**：修复点在 `tests/contract/test_docs_step_injection.py`，不在本席位写域（本席位只写 `test-evidence/dogfood-worker-*`、`final-failed-r3.txt`、`closure-full-suite-r3-*.log`）。按 dispatch「逐条列名，不修」执行。补法属一次最小编辑（向本地清单追加两条 + 一条 dated note），由有该路径写权的席位执行。

## 观察备注（如实记录，不做修复判断）

1. **r2 的 13 条新增失败已全部转绿**：`cross-feature-alignment.txt` 的 13/13 定向重跑与本次全量口径一致，r3 失败清单中这 13 个节点**零残留**。失败数 40 → 28 的 -12 与之一致（第 13 条 `test_no_live_face_file_retains_the_old_path` 的载体是本轮新增的 `closure-full-suite-r3-*.log`，已被 `RUNTIME_CACHE_PREFIXES` 的 `.specify/specs/087-speckit-visualization/test-evidence/` 覆盖，故仍为绿）。
2. **修复数恒为 0 的解释（与 r2 同）**：baseline 27 条在本轮**全部仍在失败**（`comm -12` = 27），`comm -23` 只能为 0；r1/r2 各自的新增条目本就不在 baseline 集合内，其转绿不进入 fixed 计数。故「-12」只体现在计数与失败名单差集。
3. **预期新增=0 未达成**：dispatch 预期新增 0，实测 1。按 Fast Fail 逐条列名并移交，未作任何修补。该条不阻断其余结论：baseline 面零回归（27/27 仍红，无一条转红于新面）。
4. **超时状态**：`timeout 590` 未触发（rc=1 为 pytest 退出码，非 124），套件自然结束。
5. **边界**：本席位只写 `test-evidence/dogfood-worker-*`、`final-failed-r3.txt`、`closure-full-suite-r3-*.log`；未提交、未 push、未写状态脊、未派发子代理、未加载 sdd-loop-driver。
6. **一处已存在的越界候选（只报告，未处置）**：`test-evidence/` 下存在三个 `.tmp-*.py` 暂存脚本（`.tmp-phase8-rows.py`、`.tmp-repair-phase8.py`、`.tmp-solve.py`），非本席位所写，亦不在本次 brief 内；依 `.gitignore` 与临时目录纪律应属清理面，交由有写权的席位判定。
