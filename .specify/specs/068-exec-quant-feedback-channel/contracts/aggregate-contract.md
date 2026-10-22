# Contract: 汇总腿（Aggregate — 显式动作）

**Feature**: 068 | **File scope**: `scripts/python/exec-quant.py`(+ mirror) |
**FR served**: FR-011 ~ FR-014 | **引擎动作**: `--action aggregate`（新增）

- **C-18** 动作签名

- exec-quant.py 新增动作 `aggregate`，注册进 `ACTIONS` 元组与 `ARG_MANIFEST`
  （argparse parser 保持旗标唯一事实源；`--action args-manifest` 契约自动覆盖
  新旗标——直接复用既有机制，零新校验器）。
- 参数：`--workspace-root`（既有）、`--format {text,json}`（缺省 json，
  与既有 `list-records` 形态一致）。零新增必需参数。

- **C-19** 消费面

- 只读 `<workspace>/.specify/memory/exec-quant/aggregated/**/records/*.json`
  信封记录（data-model § E6）；**MUST NOT** 读本地 `records/` / `scores/`
  （US3 语境 = 聚合层；本地记录无源归因）。
- 信封不可读（非 dict、缺 `record` 键）→ `skipped_unreadable` 计数，非阻塞。
- 本仓自身作为源项目之一出现在聚合层时，与其他源项目同权呈现（分组按信封
  `source_project`，零特判）。

- **C-20** 视图口径（机器可读）

stdout JSON 与落盘产物同构（data-model § E7）：

- `sources[]`：按 `source_project` 分组 → `record_count`、
  `units{unit_id: count}`、`quality{field: {evaluated, not_evaluated}}`、
  `coverage{not_evaluated_total, evaluated_total}`、`record_files[]`。
- `totals`：全局计数 + 未测总占比。
- 字段值形态归一（D8）：`{value, provenance}` 对象 → evaluated；裸
  `[[STR-002]]` 或缺失键 → not_evaluated；对未知新字段按 not_evaluated 处理
  （Edge Cases：引擎版本差异零硬编码）。
- **可对账**（FR-011）：`sources[].record_files[]` 列出该组计入的全部信封文件名，
  任一数字可由名单重放核对。

- **C-21** 零臆造

- 未测/缺失字段 MUST 以 `[[STR-002]]` 显式计数呈现（FR-013）；产物 MUST NOT
  含任何填补值、外推值或杜撰基线。
- 汇总动作不评估、不打分、不判阈值（Explicit Exclusions：打分模型出界）——
  只做计数与分布投影。

- **C-22** 产物落盘

- `aggregated/summaries/<summary-id>.json`，一次汇总一个新文件；旧文件零改写
  （append-only 按条，FR-012）；`summary-id` 用 `entry_filename()` 形态。
- 产物含 `generated_at` 与 `store_digest`（信封文件总数 / identity_key 总数），
  支撑可重建性核对（重跑产生新文件、数字一致）。

- **C-23** 触发与边界

- **显式动作**：MUST NOT 随接收自动执行（FR-011 / C-17）；用户可达入口 =
  exec-quant 引擎动作（本契约），Path A 文档面与 docs 引用该入口为建议后续
  步骤（零新增命令）。
- 零网络、零外发；产物仅落本仓 `aggregated/`（FR-014）。
- 动作重复执行安全：只读消费面 + 新文件产物，天然幂等可审计。
