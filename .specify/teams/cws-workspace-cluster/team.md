---
slug: cws-workspace-cluster
name: cws_work Workspace 参考项目洞察收割
description: 以 /cws_work/work.code-workspace 为集群定义源，持续分析 10 个参考开源项目，为 /cws_work/spec-kit 提炼可采纳的改进点
goal: >
  以 `/cws_work/spec-kit`（用户自己的 Harness 项目，快速迭代中）为受益方，对 workspace `folders`
  中除 spec-kit 外的全部参考仓库做持续的只读分析：每 cycle 由 subAgent 并行分析各参考项目的
  定位、架构特点与独到机制，产出①每仓特点档案 ②与 spec-kit 的能力对照 ③可采纳改进点清单
  （每条注明来源仓库+证据路径+建议落点 spec-kit 的具体位置+采纳成本档位）④增量视角（相对上轮
  新增/变化的洞察）。成功标准：四项产出齐全；每条改进点附来源证据路径且指向 spec-kit 的具体
  落点；对全部被分析仓库零写入。
pattern: continuous
preset: project-cluster   # 2026-08-20 由 workspace-cluster 改指泛化后的 project-cluster(花名册仍以 workspace folders 为种子)
created: 2026-07-30
updated: 2026-08-20
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    stage: optimizer
    type: Meta
    lifecycle: persistent
    responsibility: 解析 workspace folders（减去 home_project）生成分析花名册并 diff 上轮；派发 per-repo 只读分析 subAgent（注入统一输出 schema）；对"独到机制"类结论按证据路径抽查复核；汇总为洞察报告；一切对 spec-kit 的采纳动作只提建议、不执行
  - agent: agent-stage-evaluator-template
    role: insight-synthesizer
    stage: evaluator
    type: Worker
    lifecycle: temporary
    responsibility: 通读各仓分析档案，对照 spec-kit 现状（constitution/features/skills/commands）做能力差距判定，蒸馏可采纳改进点并按价值/成本分级；剔除 spec-kit 已具备或不适配的点
  # repo-analyst × N —— N = workspace folders 数 - 1（排除 home_project spec-kit），每 cycle 重算
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/OpenSpec
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/superpowers
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/claw-code-agent
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/intellegix-code-agent-toolkit
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/claude-code-ts
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/claude-code-py
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/learn-claude-code
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/loop-engineering
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/ai-website-cloner-template
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
  - agent: agent-stage-executor-template
    role: repo-analyst
    stage: executor
    type: Worker
    lifecycle: temporary
    territory: /cws_work/better-harness
    responsibility: 只读分析该仓：项目定位、架构、独到机制、可迁移点；输出结构化档案+证据路径
config:
  maturity: L1          # L1=报告态：只产出分析与建议，不对任何仓库（含 spec-kit）做改动
  cadence: 7d
  verifier: independent
  workspace_file: /cws_work/work.code-workspace
  roster_source: workspace_folders
  home_project: /cws_work/spec-kit   # 受益方与对照基线，不作为被分析对象
  roster_rule: folders - home_project
  roster_diff_on_start: true
  write_policy: read-only
  quality_dimensions:
    - name: coverage            # 全部参考仓均有档案
      weight: 0.20
    - name: insight-specificity # 洞察指向具体机制而非泛泛而谈
      weight: 0.30
    - name: evidence-quality    # 每条改进点附来源仓证据路径
      weight: 0.25
    - name: adoption-actionability  # 指向 spec-kit 具体落点+成本档位
      weight: 0.25
  threshold: 0.8
  budget:
    max_cycles_per_day: 2
    max_subagents_per_cycle: 11   # 10 repo-analyst + 1 insight-synthesizer；均为只读分析，不违反 L1 报告态
    on_80pct: report-only
    on_100pct: halt
  kill_switch: loop-pause-all
  constraints_file: .specify/teams/cws-workspace-cluster/constraints.md
  state_spine: .specify/teams/cws-workspace-cluster/STATE.md
  run_log: .specify/teams/cws-workspace-cluster/run-log.jsonl
---

## Goal

以 `/cws_work/spec-kit`（用户自己的 Harness 项目，快速迭代中）为**受益方**，对 workspace `folders`
中除 spec-kit 外的 **10 个参考开源项目**做持续的只读分析（博采众家之长），每 cycle 产出四项：

1. **每仓特点档案** —— 项目定位、架构、独到机制、与 Harness/SDD 相关的设计。
2. **能力对照** —— 参考仓机制 vs spec-kit 现状（constitution / features / skills / commands / teams）。
3. **可采纳改进点清单** —— 每条注明：来源仓库、证据路径、建议落点（spec-kit 的具体文件/机制）、采纳成本档位（小/中/大）。
4. **增量视角** —— 相对上轮新增/变化的洞察（参考仓会持续拉新，spec-kit 会持续迭代）。

**成功标准**：四项齐全；每条改进点附来源证据路径且指向 spec-kit 具体落点；对全部被分析仓库**零写入**
（分析产物只落本团队目录与 run workspace）。

`N`（repo-analyst 实例数）= workspace `folders` 数 − 1（排除 home_project），每 cycle 按 folders 重算。当前 N=10。

## Static Structure

| Role | Stage | Type | Lifecycle | Responsibility |
|------|-------|------|-----------|----------------|
| team-supervisor | optimizer | Meta | persistent | 花名册解析（folders − spec-kit）、并行派发只读分析 subAgent、证据抽查、汇总洞察报告 |
| repo-analyst × 10 | executor | Worker | temporary | 每参考仓一个实例：定位/架构/独到机制/可迁移点，结构化档案+证据路径 |
| insight-synthesizer | evaluator | Worker | temporary | 对照 spec-kit 现状蒸馏可采纳改进点，按价值/成本分级，剔除已具备或不适配项 |

当前分析花名册（10 个参考仓，spec-kit 为对照基线不在其中）：
OpenSpec · superpowers · claw-code-agent · intellegix-code-agent-toolkit · claude-code-ts ·
claude-code-py · learn-claude-code · loop-engineering · ai-website-cloner-template · better-harness

## Dynamic Structure

`pattern: continuous`，maturity **L1**（报告态：只产出分析与建议；对被分析仓与 spec-kit 均零改动）。
subAgent 派发为**只读分析**，不属于 L1 所限制的"改动交付物"范畴（budget 允许 11 个/cycle）。

每个 cycle：

```
1. 读 constraints.md + budget + kill-switch；预算触顶按 on_80pct / on_100pct 降级或中止
2. 解析 workspace folders − home_project → 分析花名册；与 STATE.md 上轮 diff → 增减告警
3. 读 spec-kit 对照基线（constitution / features.md / skills 清单 / commands 清单）
4. 并行派发 repo-analyst × N（注入：仓库路径 + 只读边界 + 统一输出 schema + spec-kit 基线摘要）
5. 回收结构化档案；对"独到机制"类结论按证据路径抽查，不达标打回
6. insight-synthesizer 做能力对照与改进点蒸馏（来源+证据+落点+成本档位）
7. 增量对比：与 STATE.md 已记录洞察 diff，标注新增/变化/已采纳
8. 写 cycle 报告到 runs/ + 更新 STATE.md + append run-log.jsonl
   采纳动作只进"建议清单"，一律交人决策，不自动执行
9. Post-Run Critique：记录本轮低价值/重复洞察占比，用于晋级判据
```

```mermaid
flowchart TD
    A[读 constraints + budget + kill-switch] --> B[解析 folders − spec-kit → 花名册]
    B --> C[roster diff vs STATE.md]
    C --> D[读 spec-kit 对照基线]
    D --> E[并行派发 repo-analyst × 10 只读分析]
    E --> F[证据路径抽查复核]
    F -->|不达标| E
    F --> G[insight-synthesizer 能力对照 + 改进点蒸馏]
    G --> H[增量对比 vs 上轮洞察]
    H --> I[写 runs 报告 + STATE + run-log]
    I --> J[Post-Run Critique]
    J -.->|下个 cycle| A
    G --> K[采纳建议清单 — 交人决策]
```

## Lineage

- 由预置模板 `project-cluster` 实例化（`skills/create-team/templates/teams/project-cluster.md`;
  原名 `workspace-cluster`,2026-08-20 泛化改名——花名册从 .code-workspace 绑定推广为显式项目登记,
  本团队的花名册仍以 workspace folders 为种子源），
  该模板蒸馏自 2026-07 一次真实的 10 仓 IaC 集群运营 Session（复盘见 `draft/Code Workspace.md`）。
- **2026-07-30 goal 重定义**：原 goal 为"11 仓只读 git 一致性守护"（cycle 1 报告存档于
  `runs/20260730T082021Z-report.md`，其 git 巡检血统保留）。应用户明确要求改为"参考项目洞察收割、
  反哺 spec-kit"；结构随之对齐：spec-kit 从被巡检对象改为受益方基线，repo-analyst 11→10，
  consistency-checker → insight-synthesizer，cadence 4h→7d，budget 开放只读 subAgent 派发（0→11）。
  旧 goal 的误报统计按"目标切换基线规则"清零重计。
