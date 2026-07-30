---
slug: requirement-implement-monitor
name: 需求实现过程监控
description: 持续监控任意正在实现的需求（spec）的整体实现过程，报告进度/问题/遗漏并给出建议
goal: >
  对指定的目标需求（run 输入：requirement key，如 034-evidence-infra；缺省时自动探测活跃需求或询问），
  持续监控其从规格到实现收官的整体过程。每 cycle 产出四项：①阶段进度判定（SDD 工件链 + 任务
  勾选/DoD，附证据路径）②问题/偏离清单（约束违反、范围蔓延、工件失同步）③遗漏项清单
  ④可操作建议。成功标准：四项产出齐全；High-Priority 误报率 < 20%（Post-Run Critique 累计）；
  本 loop 对监控对象零写入（仅写本团队目录）。
pattern: continuous
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    lifecycle: persistent
  - agent: qa-engineer
    role: quality-checker
    lifecycle: persistent   # L1 不派遣；预留晋级 L2 后做定向核查
config:
  maturity: L1
  cadence: 2h
  verifier: independent
  max_attempts_per_item: 3
  quality_dimensions:
    - name: progress-accuracy        # 进度对照准确性（阶段判定有据可查）
      weight: 0.30
    - name: deviation-detection      # 问题/偏离检出（纪律违反、约束偏离）
      weight: 0.25
    - name: gap-detection            # 遗漏识别（验收项缺口、开放问题悬置）
      weight: 0.25
    - name: suggestion-actionability # 建议可操作性（指向具体文件/动作）
      weight: 0.20
  threshold: 0.8
  budget:
    max_cycles_per_day: 6
    max_tokens_per_day: 100000
    max_subagents_per_cycle: 0
    on_80pct: report-only
    on_100pct: halt
  kill_switch: loop-pause-all
  constraints_file: .specify/teams/requirement-implement-monitor/constraints.md
  state_spine: .specify/teams/requirement-implement-monitor/STATE.md
  run_log: .specify/teams/requirement-implement-monitor/run-log.jsonl
created: 2026-07-29
updated: 2026-07-29
---

## Goal

对**任意正在实现的需求**提供只读的过程监控：跟踪其从规格起草到实现收官的整体推进，
对过程中出现的问题或遗漏给出建议。监控对象由每次 run 的输入参数决定，团队定义本身
不绑定任何具体需求。

**Run 输入（参数化监控目标）**：

- `target`（必需，可缺省推断）：requirement key（`.specify/specs/<key>/` 目录名，如 `034-evidence-infra`）。
  缺省时按序推断：① 会话上下文中正在讨论的需求；② `specs/` 下 tasks.md 存在未勾选任务的
  最新需求（活跃需求）；③ 均无法确定 → 询问用户，绝不猜测。
- `baseline`（可选）：附加监控基准文档（如 draft/ 设计方案、外部计划文档）；提供时并入证据源。

**通用监控基准（对任意 target 生效，按存在性探测、缺失标 Unobserved）**：

1. SDD 工件链：`.specify/specs/<target>/`（requirements.md / checklists/ / plan.md / tasks.md /
   verification.md 等）——工件间一致性（如 checklist 与 requirements 同步、clarify 决议落实）；
2. 任务与验收：tasks.md 勾选计数、DoD 状态、SC 逐项结论（verification.md）；
3. 版本控制：git log/status 增量——按故事/阶段的 commit 卫生、规格工件入库状态；
4. 项目义务：plan.md 声明的 Mirror Obligations（`diff -rq` 抽查）、约束/红线（范围边界、
   明确不修复项不被误扩）；
5. 关联登记：`.specify/memory/features.md` 与 features/<ID>.md 状态推进；
6. 执行反思信号：`.specify/memory/feedback/` 中与 target 相关的条目（勘察修正、风险预置）。

**每 cycle 成功标准（可验证）**：

- 四项产出齐全：进度判定（附证据路径）、问题/偏离、遗漏项、可操作建议；
- 判定全部有据可查（文件存在性 / diff / 只读测试运行），无凭空推断——「文件存在 ≠ 阶段完成」、
  「未观察保持 Unobserved」；
- High-Priority 误报率 < 20%（跨 cycle 由 Post-Run Critique 累计核算）；
- 对监控对象零写入（仅写本团队目录与 .work 工作区）。

## Static Structure

| Agent | Role | Stage | Type | Lifecycle | L1 职责 |
|-------|------|-------|------|-----------|---------|
| agent-team-supervisor-template | Team Supervisor | 全周期 | Meta | persistent | 独自执行整个 cycle：READ→BUDGET→TRIAGE→ACT(仅写STATE)→SCORE→CRITIQUE→REPORT |
| qa-engineer (`.specify/agents/qa-engineer.agent.md`) | Quality Checker | 核查 | Worker | persistent | **L1 不派遣**（max_subagents_per_cycle=0）；晋级 L2 后承接定向核查任务 |

## Dynamic Structure

**模式**：continuous（长期运营循环），maturity **L1（报告态）**，cadence 2h（活跃实现期；
非活跃期可由 improve-team 调为 1d/1w）。一次 `/speckit.team run requirement-implement-monitor
[<target>]` = 一个有界 cycle；重复由用户/调度驱动。

```
┌─ cycle 开始 ──────────────────────────────────────────────────┐
│ 0. TARGET  解析 run 输入的 target（缺省按 Goal 节推断规则）    │
│ 1. READ    constraints.md + budget + kill-switch               │
│ 2. BUDGET  今日已花核算（≥80% → 精简采集；≥100% → halt）      │
│ 3. TRIAGE  只读证据源采集（通用基准 1–6，对 target 实例化）：  │
│      · 增量锚点优先：tasks.md 勾选计数 + git 文件级 diff       │
│      · 首个 cycle 做全量基线盘点；后续按 Phase/故事推进深检    │
│      · 收官期终验两件套：相关测试只读实跑 + 引擎/门禁实测      │
│ 4. ACT     L1：仅更新 STATE.md（对监控对象零写入）             │
│ 5. VERIFY  （L1 跳过——无交付物改动）                          │
│ 6. SCORE   按 4 个质量维度对照 goal 打分                       │
│ 7. CRITIQUE STATE.md 追加 Post-Run Critique（含上轮 HP 误报核  │
│    算）；run-log.jsonl 追加一行（含 resolved/false_positives） │
│ 8. REPORT  写 runs/<UTC-ts>-report.md；剪枝已解决项            │
└─ cycle 结束（等待下次触发）────────────────────────────────────┘
```

**已验证机制（自 bh-port-monitor 4-cycle 实战沉淀，血统见 runs/ 归档）**：

- **增量锚点模式**：tasks 勾选计数 + git 增量替代全量重扫，采集成本降至全量的 ~40%；
- **误报核算闭环**：每 cycle 复核上轮 HP 项并计入累计误报率（实战 0/3=0%），作为晋级判据来源；
- **终验两件套**：收官判定不采信自报，实跑测试 + 门禁/引擎实测；
- **提醒上限**：同一建议最多主动提醒 3 次（3/3 后仅记录不刷屏）；
- **预算 override 留痕**：断路器可被用户在确认门显式解除，但须在报告与 STATE 双留痕且仅当 cycle 有效。

**晋级路径**：连续 ≥2 个 cadence 周期 L1 运行且 High-Priority 误报率 <20%、constraints 写全、
独立验证者在人工触发改动上验证可用后，由 `improve-team` 评估晋级 L2。注意：本团队 goal 含
「对监控对象零写入」，L1 大概率即终态；晋级仅在 goal 同步修订为允许提交修复草稿时才有意义。

## Lineage

前身为 `bh-port-monitor`（2026-07-29 创建，专用于监控 better-harness→spec-kit 复刻）。
该使命于同日收官（spec 034 全部 41 任务、Feature 038 Implemented），4 个 cycle 的完整档案
保留在 `runs/`（20260729T063425Z ~ 20260729T093345Z）与 `run-log.jsonl` 前 4 行；本团队为其
goal 重定义 + 通用化后的延续，已验证机制全部继承。
