# Expression Baseline Record — 069b（三项基线）

**Owner of the record shape**: `contracts/measurement-instruments.md` C-8 · **Instrumentation clause owner**: 069b（父编号 041）
**feature**: `069b-isomorphism-migration-metrics`
**frozen_at**: 2026-10-25 · **frozen_commit**: `f0df3d0b`（`requirements.md` 首次提交，author date `2026-10-24`，即「开工前」冻结点）

> 本记录只冻结**值、仪器与命令**，不写降幅结论。降幅归 SC；本切片 5 条 SC 里没有效率降幅条目
> （父 SC-004/005/006 归 069a，其三项已记 `deferred`）。`not-evaluated` 是判据取值，不是 SC 状态词——
> `verification.md` 的 SC 状态仍取 `.specify/templates/verification-log-template.md` 的词表（contract C-7）。

| quantity | frozen_value | frozen_at | frozen_commit | instrument | source_command | verdict |
|----------|--------------|-----------|---------------|------------|----------------|---------|
| `gate_calls` | `0` | 2026-10-25 | `f0df3d0b` | exec-quant 运行记录（068 通道）；过滤集合 = 6 个检查类单元；归属 = `run_id` 含 `069b` | `python3 scripts/python/exec-quant.py --action list-records --since 2026-10-24 --format json` 后按集合与归属过滤 | `not-evaluated` |
| `confirmations`（门控观察） | `0` | 2026-10-25 | `f0df3d0b` | feedback 条目 frontmatter；归属 = `run_id` 含 `069b`；再查 `lifecycle_point: gate-*` | `python3 scripts/python/feedback-utils.py --action list --since 2026-10-24 --format json` + `grep -rl 'lifecycle_point: gate-' .specify/memory/feedback/` | `not-evaluated` |
| `confirmations`（clarify 轮次） | `0` | 2026-10-25 | `f0df3d0b` | 本切片无 `/speckit.clarify` 运行记录（切片 requirements 自裁决，preamble 明写「未向用户发起访谈」） | `python3 scripts/python/exec-quant.py --action list-records --since 2026-10-24 --format json`（无 `run_id` 含 `069b` 的 clarify 记录） | `not-evaluated` |
| `wall_clock` | `null` | 2026-10-25 | `f0df3d0b` | 起点 = `git log --diff-filter=A --format='%h %as' -- requirements.md`（首次提交 → `f0df3d0b 2026-10-24`；`git log -1 --format=%as` 取最近一次触及，2026-10-25 实测返回 `2026-10-25`，不可用）；终点 = `/speckit.analyze` 运行判定记录 `determined_at` | `python3 scripts/python/run-determination.py --action history --target /speckit.analyze --json` | `not-evaluated` |

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
  封闭集合内命中 2 条；其中仅 checklist-069b-… 的 run_id 含 `069b` → 复核时点计数 = 1（冻结值仍为 0）。

$ python3 scripts/python/feedback-utils.py --action list --since 2026-10-24 --format json
→ matches = 5（全部 2026-10-24 条目）；逐条查 frontmatter 无 `lifecycle_point` 字段 → 门控观察分项 = 0。
  其中 20261024T164137Z-speckit-checklist.md 的 run_id 为 checklist-069b-…，但无 `lifecycle_point: gate-*`，按 C-4 不计入。

$ python3 scripts/python/run-determination.py --action history --target /speckit.analyze --json
→ counts.total = 5，全部属其他特性/切片（无 run_id 含 `069b`）→ wall_clock 终点不存在，记 `null` + reason。

$ git log --diff-filter=A --format='%h %as' -- .specify/specs/069b-isomorphism-migration-metrics/requirements.md
→ f0df3d0b 2026-10-24
```

复核对齐结论：四个通道全部可重跑（均 exit 0），归属判据与过滤集合原样可用；`confirmations` 两个分项与
`wall_clock` 仍无本切片样本，判据保持 `not-evaluated`（不记 0、不记达成）。

## 实测明细（可复算）

**`gate_calls`** — 命令输出（冻结时点、T022 复核前实跑）：窗口内 6 条记录，
`/speckit.requirements`（`069-req-…`）、`/speckit.clarify`（`…-069`）、`/speckit.plan`（`plan-069a-…`）、
`/speckit.tasks`（`tasks-069a-…`）、`/speckit.checklist`（`checklist-069a-…`）、`/speckit.review`（`069a-review-…`）。
其中属检查类过滤集合的 2 条**全部归属 069a**（`run_id` 不含 `069b`），故本切片冻结值为 **0**。
**不可计部分（仪器边界，不是 0）**：`pre-analyze-check.py`、`validate-requirements.py`、`doc-consistency-check.py`、
`decomposition-check.py`、`account-clause-coverage.py` 与测试套件是脚本而非 exec-quant 的 `unit_id`，
既有通道无法按「每次检查」分开计数。基线值为 0 使降幅 `(冻结 − 收尾)/冻结` 不可定义，故判据记 `not-evaluated`。

**`confirmations`** — 两个分项都为 0：feedback 目录中带 `lifecycle_point: gate-` 的条目 `grep` 命中 0 个文件；
本切片没有 clarify 运行记录（父 069 的 `…-speckit-clarify-069` 属 requirements 阶段，不计入）。
requirements 的 § Clarifications 有 13 条 `- Q:` 自裁决条目，preamble 明写未向用户发问，按 contract C-4 不计入。
绝对值 0 是实测；但作为基线它无法支撑「下降 ≥30%」，故判据记 `not-evaluated`。

**`wall_clock`** — 起点 `2026-10-24`（`f0df3d0b` 的 author date）。终点记录不存在：
`run-determination.py --action history --target /speckit.analyze --json` 返回的 5 条记录全部属其他特性/切片
（`064-subagent-concurrency-analyze-rerun-…` 等），无 `069b` 记录。按 contract C-5 记 `null` + reason。

## 与 SC 的关系

本切片的 5 条 SC（同构映射、客户快照零新增失败、台账双注入、混合 oracle、六面 owner）**都不是效率降幅判据**；
三项基线的用途是给**后续**同类切片提供可比前值。本记录不得被读成「本切片达成了某项降幅」。
