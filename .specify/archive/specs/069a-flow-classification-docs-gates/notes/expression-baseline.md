# Expression Baseline Record — 069a（三项基线）

**Owner of the record shape**: `data-model.md` E8 · **Instrumentation clause owner**: 069b（父编号 041）
**feature**: `069a-flow-classification-docs-gates`
**frozen_at**: 2026-10-24 · **frozen_commit**: `0f650749`（`requirements.md` 首次提交，即「开工前」冻结点）
**compared_at**: 2026-10-24（收尾对照；三项均**不含**降幅结论）

> **口径修正（2026-10-24，review F8）**：本文件上一版把 `gate_calls` 的分母取成「门禁 owner 调用点表的四个单元 id（W1/W3/W2/W4）」，在记录窗口内命中 0 条，于是写下「0 → 0，无可比降幅」。
> 那不是 requirements 对 SC-004 的定义：口径（a）的分母是**本特性运行中执行的检查类单元调用总数**（checklist / analyze / review / pre-analyze 检查 / `validate-*`）。四个 W 单元是本切片**新接线**的文档型入口，本切片当然不会调用自己，用它们做分母等于用「还没接上的东西」冒充基线。
> 本版按口径（a）重记：把实际跑过的检查类调用逐项列出，能计的计、不能计的写明仪器边界，并**照实记 `not-evaluated`**，不再用 0 冒充。

| 量 | 冻结值 | 收尾值 | 来源命令（本次实跑） | 结论 |
|----|--------|--------|----------------------|------|
| 门禁调用次数（`gate_calls`，口径 a） | `0`（冻结时本特性尚未开工，无任何调用） | **2 条仪器可见**：`/speckit.checklist` ×1（2026-10-24T12:55:53Z，run `checklist-069a-20261024t2055z`）+ `/speckit.review` ×1（2026-10-24T15:14:46Z，run `069a-review-20261024T1515Z`）；另有**仪器不可分**的检查脚本调用（见下「不可计部分」） | `python3 scripts/python/exec-quant.py --action list-records --since 2026-10-20 --format json`，按 `unit_id ∈ {/speckit.checklist, /speckit.analyze, /speckit.review}` 过滤，再按 `run_id` 归到本切片 | **not-evaluated**：冻结值是「特性尚未开工」的零，不是「同类特性在协议下测得的前值」，分子式 `(冻结 − 收尾)/冻结` 在分母为 0 时不可定义；不得记 0 降幅、不得记达标 |
| 人工确认次数（`confirmations`，口径 b） | `0` | `0`：门控观察记录 `feedback-utils.py --action list --lifecycle-point gate-` 命中 0 条（本切片 6 条反馈条目均无 `lifecycle_point`）；clarify 提问轮次 = 0（`20261024T043049Z-speckit-clarify.md`：自裁决，0 个用户问题） | 同左两命令 | **not-evaluated**：绝对值为 0（「单阶段人工确认 ≤3」在该 0 上成立），但「下降 ≥30%」在 0 基线上不可定义；无同类前值样本 |
| requirements→analyze 墙钟（`wall_clock`） | `null` | `null` | 起点 `git log -1 --format=%cs -- requirements.md` → `2026-10-24`；终点 `run-determination.py --action history --target /speckit.analyze --json`（本切片无运行记录） | **不可比**（终点时间戳缺失；SC-006 记 deferred） |

## 派生口径（可复算）

- **`gate_calls` derivation（口径 a）**：分母 = 本特性运行中**实际执行的检查类调用**。
  - **仪器可见部分（exec-quant，unit 粒度）**：本切片 6 条记录里属检查类的 2 条 —— `/speckit.checklist` 1、`/speckit.review` 1；`/speckit.analyze` 0（本切片未运行该阶段）。`/speckit.requirements`、`/speckit.clarify`、`/speckit.plan`、`/speckit.tasks` 是**产出类**单元，不进口径（a）的分子。
  - **不可计部分（仪器边界，不是 0）**：`pre-analyze-check.py --stage {requirements,plan,tasks}`（plan 记录 `advisories=79`、checklist 记录 `advisories=90`）、`validate-requirements.py`、`validate-tasks.py`、`decomposition-check.py`、`account-clause-coverage.py`，以及 8 支测试模块。它们是脚本而不是 exec-quant 的 `unit_id`，**既有通道无法按「每次检查」分开计数**——这正是「仪器不可分」的事实，不是「没有发生」。
  - **声明门禁单元集（口径 b 的过滤集合）**：`{/speckit.docs, skill:create-docs, /speckit.humanize, skill:humanize}` 在本窗口命中 0 条。该 0 的含义只是「本切片没有调用自己新接的四个入口」，**不作为门禁调用次数的分母**（上一版把它当分母，是本条被 review 判为「过滤后的 0 基线冒充」的原因）。两项数字都记在这里，读者可自行核对，但结论只取口径（a）。
  - **判读边界**：由于冻结值是开工前的零、且既有仪器不能把脚本级检查拆分成「每次调用」，SC-004 的下降率在大方向上**不可判定**；改计 0 或编一个假前值都是伪造。按 E8 记 `not-evaluated`（= 收尾 SC 行的 `deferred` + reason）。
- **`confirmations` derivation（口径 b）**：门控观察记录 0 条 + clarify 提问 0 轮 = 0。0 是实测，不是缺省填充；但作为**基线**它同样无法支撑「下降 ≥30%」，故只报绝对值。
- **`wall_clock` derivation**：起点取 `requirements.md` 首次提交 author date（`0f650749`，2026-10-24）；终点应为本切片 `/speckit.analyze` 完成时的运行判定记录时间戳——该记录**不存在**（`run-determination.py --action history --target /speckit.analyze` 返回的 5 条记录全部属于其他特性：055 / 064 等）。按 E8 校验规则记 `value: null` + reason，MUST NOT 记 0、MUST NOT 记达成。
- **不确定性声明**：三项量的仪器口径与 `not-evaluated` 降级的规范条款归 069b（父编号 041）；本次只用既有通道取数（不新增采集器），未做任何插桩或补采。若要给出可比降幅，需在**下一个**同类表达类特性上按同一口径先冻前值、再收尾复测。

## 与 SC 的关系

SC-004 / SC-005 / SC-006 要求「同类规模、同类读者面的文档型特性」的前后对照样本；本切片是**第一个**接线切片，`features.md` 中已完成的表达类特性不足 3 个（062 是唯一既存表达类实现，其基线不是按本协议冻结的），因此三项均记 `deferred`（= not-evaluated），不记 0、不记达标。SC-004 的收尾绝对量按口径（a）记 2 条仪器可见检查调用 + 一组仪器不可分的脚本检查，供 069b 的仪器化对照。
