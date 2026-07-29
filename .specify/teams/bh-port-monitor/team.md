---
slug: bh-port-monitor
name: Better Harness 复刻监控
description: 持续监控 better-harness→spec-kit 能力复刻进展，报告问题/遗漏并给出建议
goal: >
  持续监控「better-harness 能力复刻到 spec-kit」的开发进展（开发在另一 session 进行），
  基准为 draft/2026-07-29-better-harness-evidence-port-plan.md（v2）的 P1–P7 实施计划、
  D1–D3 决策、四条证据纪律、§8 不移植清单，以及 spec 034-evidence-infra / Feature 038。
  每 cycle 产出：①P1–P7 对照验收标准的进度判定 ②问题/偏离清单 ③遗漏项清单 ④可操作建议。
  成功标准：每 cycle 报告四项产出齐全；High-Priority 误报率 < 20%（Post-Run Critique 累计）；
  本 loop 绝不修改监控对象的任何文件。
pattern: continuous
members:
  - agent: agent-role-team-supervisor-template
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
    - name: progress-accuracy        # 进度对照准确性（P1–P7 判定有据可查）
      weight: 0.30
    - name: deviation-detection      # 问题/偏离检出（纪律违反、决策偏离）
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
  constraints_file: .specify/teams/bh-port-monitor/constraints.md
  state_spine: .specify/teams/bh-port-monitor/STATE.md
  run_log: .specify/teams/bh-port-monitor/run-log.jsonl
created: 2026-07-29
updated: 2026-07-29
---

## Goal

持续监控「将 /cws_work/better-harness 项目能力完整复刻到 /cws_work/spec-kit」这一开发工作
（在另一个 session 中进行）的整体进展，对过程中出现的问题或遗漏给出建议。

**监控基准（真相源，按优先级）**：

1. `draft/2026-07-29-better-harness-evidence-port-plan.md`（v2）——P1–P7 实施计划与逐阶段验收标准、
   D1（源码复制托管）/ D2（多 CLI 扩展）/ D3（runs+feedback 一等泳道）三项已定决策、
   四条证据纪律（配置存在≠观察到使用 / Unobserved 不推断 / 计数只路由 / 隐私语义面片）、
   §8 有意不移植清单、§9 剩余开放问题。
2. `.specify/specs/034-evidence-infra/`——本移植工作的 SDD 规格工件。
3. `.specify/memory/features/038.md` 与 `features.md` 中对应条目。
4. 上游基线：`/cws_work/better-harness` @ `b2e621d`（v0.3.0，MIT）。

**每 cycle 成功标准（可验证）**：

- 报告包含四项产出：进度判定（P1–P7 逐项，附证据路径）、问题/偏离、遗漏项、可操作建议；
- 判定全部有据可查（文件存在性 / diff / 测试结果），无凭空推断——遵守自身也适用的
  「未观察保持 Unobserved」纪律；
- High-Priority 误报率 < 20%（跨 cycle 由 Post-Run Critique 累计核算）；
- 本 loop 对监控对象**零写入**（仅写本团队目录）。

## Static Structure

| Agent | Role | Stage | Type | Lifecycle | L1 职责 |
|-------|------|-------|------|-----------|---------|
| agent-role-team-supervisor-template | Team Supervisor | 全周期 | Meta | persistent | 独自执行整个 cycle：READ→BUDGET→TRIAGE→ACT(仅写STATE)→SCORE→CRITIQUE→REPORT |
| qa-engineer (`.specify/agents/qa-engineer.agent.md`) | Quality Checker | 核查 | Worker | persistent | **L1 不派遣**（max_subagents_per_cycle=0）；晋级 L2 后承接定向核查任务 |

## Dynamic Structure

**模式**：continuous（长期运营循环），maturity **L1（报告态）**，cadence 2h（活跃开发期）。
一次 `/speckit.team run bh-port-monitor` = 一个有界 cycle；重复由用户/调度驱动。

```
┌─ cycle 开始 ────────────────────────────────────────────────┐
│ 1. READ    constraints.md + budget + kill-switch            │
│ 2. BUDGET  今日已花核算（≥80% → report-only；≥100% → halt）│
│ 3. TRIAGE  只读证据源采集：                                 │
│      · git log/status/diff（spec-kit 工作树）               │
│      · scripts/js/better-harness/ 落库状态 vs 方案 §3.1     │
│      · .specify/specs/034-evidence-infra/ 工件演进          │
│      · evidence-utils.py / skills/collect-evidence 存在性   │
│      · tests/js/ + pytest contract 测试结果（只读运行）     │
│      · UPSTREAM.md / LICENSE / 双镜像 diff -rq              │
│      · features/038.md 状态、§9 开放问题解决情况            │
│ 4. ACT     L1：仅更新 STATE.md（不改任何监控对象文件）      │
│ 5. VERIFY  （L1 跳过——无交付物改动）                       │
│ 6. SCORE   按 4 个质量维度对照 goal 打分                    │
│ 7. CRITIQUE STATE.md 追加 Post-Run Critique；run-log 追加   │
│ 8. REPORT  写 runs/<UTC-ts>-report.md；剪枝已解决项         │
└─ cycle 结束（等待下次触发）─────────────────────────────────┘
```

**晋级路径**：连续 ≥2 个 cadence 周期 L1 运行且 High-Priority 误报率 <20%、constraints 写全、
独立验证者在人工触发改动上验证可用后，由 `improve-team` 评估晋级 L2（届时才允许对小而明确项
提出草稿级修复，并派遣 qa-engineer 独立核查）。
