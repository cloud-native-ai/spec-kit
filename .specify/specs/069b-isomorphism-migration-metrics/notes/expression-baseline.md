# Expression Baseline Record — 069b（三项基线）

**Owner of the record shape**: `contracts/measurement-instruments.md` C-8 · **Instrumentation clause owner**: 069b（父编号 041）
**feature**: `069b-isomorphism-migration-metrics`
**frozen_at**: 2026-10-25 · **frozen_commit**: `f0df3d0b`（`requirements.md` 首次提交，author date `2026-10-24`，即「开工前」冻结点）

> 本记录只冻结**值、仪器与命令**，不写降幅结论。降幅归 SC；本切片 5 条 SC 里没有效率降幅条目
> （父 SC-004/005/006 归 069a，其三项已记 `deferred`）。`not-evaluated` 是判据取值，不是 SC 状态词——
> `verification.md` 的 SC 状态仍取 `.specify/templates/verification-log-template.md` 的词表（contract C-7）。

| quantity | frozen_value | frozen_at | frozen_commit | instrument | source_command | verdict |
|----------|--------------|-----------|---------------|------------|----------------|---------|
| `gate_calls` | `not-evaluated`（仪器-对象不匹配：通道只数 exec-quant 的 `unit_id` 记录，而八阶段阻断门禁是脚本；无守恒值可冻结，见 § 仪器-对象缺口） | 2026-10-25 | `f0df3d0b` | exec-quant 运行记录（068 通道）；过滤集合 = 6 个检查类单元；归属 = `run_id` 含 `069b` | `python3 scripts/python/exec-quant.py --action list-records --since 2026-10-24 --format json` 后按集合与归属过滤 | `not-evaluated` |
| `confirmations`（门控观察） | `0` | 2026-10-25 | `f0df3d0b` | feedback 条目 frontmatter；归属 = `run_id` 含 `069b`；再查 `lifecycle_point: gate-*` | `python3 scripts/python/feedback-utils.py --action list --since 2026-10-24 --format json` + `grep -rl 'lifecycle_point: gate-' .specify/memory/feedback/` | `not-evaluated` |
| `confirmations`（clarify 轮次） | `0` | 2026-10-25 | `f0df3d0b` | 本切片无 `/speckit.clarify` 运行记录（切片 requirements 自裁决，preamble 明写「未向用户发起访谈」） | `python3 scripts/python/exec-quant.py --action list-records --since 2026-10-24 --format json`（无 `run_id` 含 `069b` 的 clarify 记录） | `not-evaluated` |
| `wall_clock` | `null` | 2026-10-25 | `f0df3d0b` | 起点 = `git log --diff-filter=A --format='%h %as' -- requirements.md`（首次提交 → `f0df3d0b 2026-10-24`；`git log -1 --format=%as` 取最近一次触及，2026-10-25 实测返回 `2026-10-25`，不可用）；终点 = `/speckit.analyze` 运行判定记录 `determined_at` | `python3 scripts/python/run-determination.py --action history --target /speckit.analyze --json` | `not-evaluated` |

**值域说明**：`confirmations` 两行的 `0` 是**实测绝对值**（通道确实返回 0），不是缺省填充；`gate_calls` 不写 `0` 是
**契约 C-3 的明文义务**（「脚本级检查…不可按次计数…MUST NOT 当作 0」），`wall_clock` 不写数值是**终点记录不存在**。三者
verdict 同为 `not-evaluated`，但原因各不相同：`confirmations` 是绝对值 0 使降幅不可定义，`gate_calls` 与 `wall_clock`
连可比较的值都没有（前者仪器看不见对象，后者仪器未被触发）。

**`gate_calls` 的封闭过滤集合（C-3，事先冻结）**：`/speckit.checklist`、`/speckit.analyze`、`/speckit.review`、
`skill:create-checklist`、`skill:analyze-artifacts`、`skill:review-sdd-process`。计数 = 该集合在记录窗口内、
且 `run_id` 含切片键 `069b` 的记录条数（unit 粒度）。收尾复测 MUST NOT 回选单元集、MUST NOT 改归属规则
（契约 C-9：同一仪器、同一集合、同一样本窗口）。

## 复核（T022 落盘，2026-10-25，同仪器 / 同集合 / 同窗口）

冻结点是 `requirements.md` 的首次提交（`f0df3d0b`，2026-10-24），**冻结值记录的是开工前的状态**；
下面四段是本节复核时各通道的真实返回（不是重新冻结，也不改写上表）：

```text
$ python3 scripts/python/exec-quant.py --action list-records --since 2026-10-24 --format json
→ 7 条记录：/speckit.requirements（069-req-…）、/speckit.clarify（…-069）、/speckit.plan（plan-069a-…）、
  /speckit.tasks（tasks-069a-…）、/speckit.checklist（checklist-069a-…）、/speckit.review（069a-review-…）、
  /speckit.checklist（checklist-069b-20261025t0042z）。
  封闭集合内命中 2 条；其中仅 checklist-069b-… 的 run_id 含 `069b` → 复核时点**命令单元计数** = 1（冻结点 = 0）。
  这两个数都是「检查类命令/技能跑了多少次」，不是「门禁被调用了多少次」；八阶段的阻断门禁是脚本，不在通道里（§ 仪器-对象缺口）。

$ python3 scripts/python/feedback-utils.py --action list --since 2026-10-24 --format json
→ matches = 5（全部 2026-10-24 条目）；逐条查 frontmatter 无 `lifecycle_point` 字段 → 门控观察分项 = 0。
  其中 20261024T164137Z-speckit-checklist.md 的 run_id 为 checklist-069b-…，但无 `lifecycle_point: gate-*`，按 C-4 不计入。

$ python3 scripts/python/run-determination.py --action history --target /speckit.analyze --json
→ counts.total = 5，**无一条 run_id 含 `069b`**。本切片 2026-10-25 的 analyze 轮（`tasks.md` § Generation-time premise
  corrections 记录的三处修正）是自跑，**没有产出 `/speckit.analyze` 运行判定记录**——终点不是「数据窗口里没有」，
  而是本切片从未让该仪器落过一条记录（§ 仪器-对象缺口 第 2 条）。故 `wall_clock` 记 `null` + reason。

$ git log --diff-filter=A --format='%h %as' -- .specify/specs/069b-isomorphism-migration-metrics/requirements.md
→ f0df3d0b 2026-10-24
```

复核对齐结论：四个通道全部可重跑（均 exit 0），归属判据与过滤集合原样可用。三项量的判据都停在 `not-evaluated`，
但**原因不同且都不写成 0**：`confirmations` 是实测 0（降幅不可定义）、`gate_calls` 是仪器看不见对象（无守恒值）、
`wall_clock` 是终点记录在本切片从未生成（缺口已登记）。

## 实测明细（可复算）

**`gate_calls`** — 命令输出（冻结时点、T022 复核前实跑）：窗口内 6 条记录，
`/speckit.requirements`（`069-req-…`）、`/speckit.clarify`（`…-069`）、`/speckit.plan`（`plan-069a-…`）、
`/speckit.tasks`（`tasks-069a-…`）、`/speckit.checklist`（`checklist-069a-…`）、`/speckit.review`（`069a-review-…`）。
其中属检查类过滤集合的 2 条**全部归属 069a**（`run_id` 不含 `069b`），冻结点该计数 = 0，复核时点 = 1（069b 的 checklist 轮）。
**这两个数是命令/技能单元的运行次数，不是门禁调用次数**，因此都不作为本量的值（§ 仪器-对象缺口 第 1 条）。
**不可计部分（仪器边界，不是 0）**：`pre-analyze-check.py`、`validate-requirements.py`、`doc-consistency-check.py`、
`decomposition-check.py`、`account-clause-coverage.py` 与测试套件是脚本而非 exec-quant 的 `unit_id`，
既有通道无法按「每次检查」分开计数——而**它们才是门禁**。本切片真实跑过的门禁数量远大于 0（每次都跑 validate / pre-analyze /
mirror `--check` / 名字级回归），若把通道里的 0 写作本量的值，等于断言「一次门禁都没跑」。故 `frozen_value` 记
`not-evaluated` + 原因，不记 0。

**`confirmations`** — 两个分项都实测为 0：feedback 目录中带 `lifecycle_point: gate-` 的条目 `grep` 命中 0 个文件；
本切片没有 clarify 运行记录（父 069 的 `…-speckit-clarify-069` 属 requirements 阶段，不计入）。
requirements 的 § Clarifications 有 13 条 `- Q:` 自裁决条目，preamble 明写未向用户发问，按 contract C-4 不计入。
绝对值 0 是实测；但作为基线它无法支撑「下降 ≥30%」，故判据记 `not-evaluated`。

**`wall_clock`** — 起点 `2026-10-24`（`f0df3d0b` 的 author date），可复算。终点记录**在本切片不存在**：
`run-determination.py --action history --target /speckit.analyze --json` 返回 5 条记录，其 `run_id` 无一含 `069b`；
本切片 2026-10-25 的 analyze 轮是自跑，未产出 `/speckit.analyze` 运行判定记录。**归因更正（review-fix F6）**：
旧文写「5 条全属其他特性」——那句话只说「不能借用别人的终点」（C-5 本就禁止借用），把缺口说成了取样结果；
真实原因是**本切片自己没有让该仪器落记录**，属运行缺口，不是数据窗口的性质。

## 仪器-对象缺口（review-fix F6，2026-10-25）

三条缺口都**不是**「样本不足」，而是「仪器看不见它要量的对象」。按 review REC-069b-08，仪器-对象适配应在 plan 期校验；
本切片漏了这一检查，此处如实记录，供后续同类切片把该项前置为 plan 门：

1. **`gate_calls`：量的对象是脚本门禁，通道的对象是 `unit_id` 记录。** `shared/workflow/expression-gates.md` § 阶段算子表
   的阻断算子全部是脚本（`validate-requirements.py` / `pre-analyze-check.py` / `doc-consistency-check.py` / `docs-utils.py`）；
   exec-quant 只记录命令与技能单元。冻结的 6 元过滤集因此只能观测「检查类命令/技能跑了几次」，与「门禁调用次数」不是同一个量。
   即使只看代理量，冻结点 0 也让降幅 `(冻结 − 收尾)/冻结` 不可定义。**处置**：不记 0、不记达成；要变得可测必须改落地方式
   （每个门禁脚本在调用点写一条 exec-quant 形状的记录），属框架改动，不在本切片范围。
2. **`wall_clock`：终点仪器在本切片从未被触发。** 起点侧（`git log --diff-filter=A`）已在跨切片一致性修正中改对并实测；
   终点侧的 `/speckit.analyze` 运行判定记录为 0 条。**处置**：记 `null` + reason；同时登记为**本切片的运行缺口**
   （analyze 轮未走记录入口），解除条件是该轮以 `/speckit.analyze` 入口重跑并落记录，或后续把 analyze 的收尾接上运行判定。
3. **`confirmations`：可测但不可比。** 两个分项都是真实 0（通道确实返回 0），不是缺省填充；问题在分母为 0 使降幅不可定义，
   属契约 C-6 已预见的情形。**处置**：值照记 0、判据记 `not-evaluated`，不冒充「零确认」等于「效率改善」。

## 与 SC 的关系

本切片的 5 条 SC（同构映射、客户快照零新增失败、台账双注入、混合 oracle、六面 owner）**都不是效率降幅判据**；
三项基线的用途是给**后续**同类切片提供可比前值。本记录不得被读成「本切片达成了某项降幅」。
