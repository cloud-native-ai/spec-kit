# Expression Baseline Record — 069a（三项基线）

**Owner of the record shape**: `data-model.md` E8 · **Instrumentation clause owner**: 069b（父编号 041）
**feature**: `069a-flow-classification-docs-gates`
**frozen_at**: 2026-10-24 · **frozen_commit**: `0f650749`（`requirements.md` 首次提交，即「开工前」冻结点）
**compared_at**: 2026-10-24（收尾对照；逐项结论见下，均**不含**降幅结论）

| 量 | 冻结值 | 收尾值 | 来源命令（本次实跑） | 结论 |
|----|--------|--------|----------------------|------|
| 门禁调用次数（`gate_calls`） | `0` | `0` | `python3 scripts/python/exec-quant.py --action list-records --since 2026-10-20 --format json`，按声明门禁单元集 `{/speckit.docs, skill:create-docs, /speckit.humanize, skill:humanize}` 过滤 | **无可比降幅**（0 → 0；SC-004 记 deferred，reason 见下） |
| 人工确认次数（`confirmations`） | `0` | `0` | 门控观察记录 `feedback-utils.py --action list --lifecycle-point gate-`（0 条）+ clarify 提问轮次（`20261024T043049Z-speckit-clarify.md`：0 个问题） | **无可比降幅**（0 → 0；SC-005 记 deferred） |
| requirements→analyze 墙钟（`wall_clock`） | `null` | `null` | 起点 `git log -1 --format=%cs -- requirements.md` → `2026-10-24`；终点 `run-determination.py --action history --target /speckit.analyze --json`（本切片无运行记录） | **不可比**（终点时间戳缺失；SC-006 记 deferred） |

## 派生口径（可复算）

- **`gate_calls` derivation**：`exec-quant` 记录目录共 26 条记录（文件名前缀 2026-10-24 起 5 条），`unit_id` 命中声明门禁单元集的记录 = **0**。判读边界：0 是「该单元集在记录窗口内没有被调用过」的实测计数，**不等于**「门禁不存在或成本为零」；由于基线与收尾同为 0，`下降 ≥30%`（SC-004）在该基线上数学上不可定义，故不记达标、记 `deferred`。
- **`confirmations` derivation**：`feedback-utils.py --action list` 的反馈条目中无 `lifecycle_point: gate-*`（本切片 5 条条目分别是 requirements / clarify / plan / tasks / checklist）；clarify 以自裁决模式运行并记录 0 个用户问题。0 为实测，非缺省填充。
- **`wall_clock` derivation**：起点取 `requirements.md` 首次提交 author date（`0f650749`，2026-10-24）；终点应为本切片 `/speckit.analyze` 完成时的运行判定记录时间戳——该记录**不存在**（`run-determination.py --action history --target /speckit.analyze` 返回的 5 条记录全部属于其他特性：055 / 064 等）。按 E8 校验规则记 `value: null` + reason，MUST NOT 记 0、MUST NOT 记达成。
- **不确定性声明**：三项量的仪器口径与 `not-evaluated` 降级的规范条款归 069b（父编号 041）；本次只用既有通道取数（不新增采集器），未做任何插桩或补采。

## 与 SC 的关系

SC-004 / SC-005 / SC-006 依赖「同类规模、同类读者面的文档型特性」的前后对照样本；本切片是**第一个**接线切片，`features.md` 中已完成的表达类特性不足 3 个（062 是唯一既存表达类实现，且其基线不是按本协议冻结的），因此三项均记 `deferred`（= not-evaluated），不记 0、不记达标。详见 `verification.md` 的同名 SC 行。
