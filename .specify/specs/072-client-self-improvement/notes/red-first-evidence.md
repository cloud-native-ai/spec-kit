# Red-First Evidence — Feature 072 client-self-improvement

> Owner slot: `.specify/specs/072-client-self-improvement/notes/red-first-evidence.md`
> 判定面: SC-006。五个新契约测试组每组一条红先行记录，**四字段缺一即该组声称无效**:
> ① 命令行 ② 真实输出 ③ 退出码 ④ 失败计数。
> 记录形态归 tasks.md § Notes；本文件在 T001 只立骨架，各组红运行由对应任务行(T004/T009/T013/T016/T020)回填。

## 五个新契约测试文件（点名）

| # | 测试文件 | 行为组 | 认领行 | 契约条款 |
|---|----------|--------|--------|----------|
| 1 | `tests/contract/test_client_capture.py` | 采集(非交互路径五步 + capture 子命令面) | T004 | C-10…C-16 (capture-step.md) |
| 2 | `tests/contract/test_client_armed_state.py` | 武装态三值(已武装/未武装/歧义) | T009 | C-1…C-9 (client-identity-and-armed-state.md) |
| 3 | `tests/contract/test_client_package_exclusion.py` | 打包排除 + 载体闭集 | T013 | C-25…C-28 (digest-and-carriers.md) |
| 4 | `tests/contract/test_client_improve_loop.py` | 客户主体改进循环(SI-0…SI-9 复用) | T016 | C-33…C-39 (client-improvement-loop.md) |
| 5 | `tests/contract/test_client_metrics.py` | 循环度量即读即建(只读 client-metrics) | T020 | C-40…C-45 (cadence-and-metrics.md) |

## 红先行记录骨架（每组一条，回填时替换占位）

### G1 — test_client_capture.py (T004)

- 命令行: _pending — 红运行后回填_
- 真实输出: _pending_
- 退出码: _pending_
- 失败计数: _pending_

### G2 — test_client_armed_state.py (T009)

- 命令行: _pending — 红运行后回填_
- 真实输出: _pending_
- 退出码: _pending_
- 失败计数: _pending_

### G3 — test_client_package_exclusion.py (T013)

- 命令行: _pending — 红运行后回填_
- 真实输出: _pending_
- 退出码: _pending_
- 失败计数: _pending_

### G4 — test_client_improve_loop.py (T016)

- 命令行: _pending — 红运行后回填_
- 真实输出: _pending_
- 退出码: _pending_
- 失败计数: _pending_

### G5 — test_client_metrics.py (T020)

- 命令行: _pending — 红运行后回填_
- 真实输出: _pending_
- 退出码: _pending_
- 失败计数: _pending_

## 纪律备注

- 红运行 MUST 在未改动树(实现编辑前)上执行；失败计数 = 该文件 pytest 报告的 failed 数。
- 守护性复跑(071 六套件、`test_expression_compatibility.py` C-5、`test_review_p1_review_loop.py`、feedback/probe 族)是迁移/回归例外，**不作红先行声称**，不进本文件。
- 实现完成后同命令全绿即为该组转绿证据(GATE-5)。
