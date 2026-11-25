# Improvement Plan — /speckit.status

## Entries（按优先级）

### IP-1 — status-digest.py digest 投影：registry 缺 stage 时可回退读取状态脊

- **Trainee 文件/节**：`.specify/scripts/python/status-digest.py`（digest 渲染的「阶段」列投影；契约侧 `shared/guidelines/reporting-obligations.md` § 九）
- **tweak**：当 registry 条目无 `stage` 字段而工作区存在 `.specify/state/<line_id>.md` 时，从状态脊的机器块读取 `stage` 作为该列取值；读不到仍渲染 `—`。
- **evidence**：`single-observation`——本次 digest 中 095 行 `阶段 —`，而状态脊声明 `stage: tasks`（D-无编号；见 deviations § 材料性分歧）。**该陈旧的主因是 coach/驱动侧未刷新 registry**，本项只是让投影在 registry 缺失时有确定来源；若判定为 registry 职责则本项作废。
- **注意**：这是**单次观察**，不构成对 Trainee 的失败证据；improve-skills 若要求重复证据可拒绝，拒绝按 `optimization: failed`/`skipped` 记录，不重试。

### IP-2 — （无）其余 OC/PE 全通过，无第二个候选。

## Run Status

- run: success
- optimization: skipped（唯一候选 IP-1 为单次观察且主因归 coach 侧 registry 维护；本运行不据此改动 Trainee 文件）
