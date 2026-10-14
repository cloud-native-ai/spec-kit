---
name: 绘图技能交互图表能力建设团队
slug: draw-diagram-interactive
description: 以 iteration 闭环为 draw-diagram 技能建设可交互图表绘制能力(图表随用户输入调整,网页格式交付)
goal: >
  draw-diagram 技能具备绘制可交互图表的能力:图表可根据用户输入做出调整(通常是网页格式)。
  权威定义见 goal_slug 指向的 .specify/goal/draw-diagram-interactive/goal.md,本字段仅为可读性渲染。
goal_slug: draw-diagram-interactive
territory:
  write:
    - skills/external/draw-diagram/**
    - .specify/skills/draw-diagram/**
  read:
    - docs/**
    - .specify/shared/**
    - .specify/teams/.work/draw-diagram-interactive/**
  forbidden:
    - .specify/goal/**
    - .specify/agents/**
pattern: iteration
created: 2026-10-14
updated: 2026-10-14
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    stage: meta
    type: Meta
    lifecycle: temporary
  - agent: agent-stage-executor-template
    role: capability-builder
    stage: executor
    type: Meta   # 操作对象是技能定义(目标工作副本)→ 按操作对象判 Meta;只产补丁到运行工作区,canonical 落盘由 Supervisor 执行
    lifecycle: temporary
  - agent: skill-verifier
    role: capability-verifier
    stage: evaluator
    type: Meta   # 复用既有 .specify/agents/templates/skill-verifier.agent.md;其操作对象是技能执行效果与证据(图表为证据),与其声明身份一致
    lifecycle: temporary
config:
  optimization_target: skills/external/draw-diagram/   # 被建设/优化的技能(目标);优化器只改其工作副本
  benchmark: >
    被评分交付物 = capability-verifier 以「当前采纳的目标副本」实际执行 draw-diagram 规程绘制出的
    一张可交互图表(引擎自选,网页格式交付)。评分对象恒为按最新目标再生产的交付物,不得手改被评产物
    (score = f(target) 不变式)。
  quality_dimensions:
    - name: interactivity        # 交互有效性:图表随用户输入做出调整(点击/悬停/筛选/展开收起任一形式);明确排除动画/动图/视频等形式动态
      weight: 0.45
    - name: correctness          # 正确性:经 draw-diagram 规程真实产出;网页格式可在浏览器打开且渲染无错
      weight: 0.25
    - name: integration          # 整合度:能力按双层结构落位(语义模型→引擎层),不破坏既有静态绘制路径,规程/参考文档同步更新
      weight: 0.30
  threshold: 0.8
  max_iterations: 5
  regression_limit: 2
  regression_check: 每代对既有静态绘制路径抽一例回归执行,确认能力扩展未破坏原功能
  sync_constraint: >
    改动命中 skills/external/draw-diagram/ 后必须与 .specify/skills/draw-diagram/ 双写同步
    (diff -rq 校验字节一致),二者均为独立 git 副本、非符号链接(沿用 draw-plantuml-optimizer 先例)。
---

## Goal

**北极星(可验证)**:draw-diagram 技能具备绘制**可交互图表**的能力——图表可根据用户输入做出调整,通常以网页格式交付。

- **判据(1 条,权威见 goal 定义)**:通过 draw-diagram 技能能够绘制出可交互的图表(通常是网页格式)。判据按程度测量,达标线由本团队 `config.threshold` 承载(加权评分 ≥ 0.8)。
- **边界**:「动态」仅指图表随用户输入做出调整(交互的结果),**不含**动画/动图/视频等形式上的动态。
- **权威性**:goal 内容的单一事实源是 `goal_slug` 指向的定义文件;本节为可读性渲染,不一致时以定义为准并显式报出。

> 静态结构(谁参与)与动态结构(怎么协作)都仅为达成此 goal 而存在。

## Static Structure

Role × Stage × Type 花名册(全部 temporary,按 run 从模板实例化;`skill-verifier` 复用既有持久模板):

| Member | Role | Stage | Type | Lifecycle | 职责 |
|--------|------|-------|------|-----------|------|
| team-supervisor | team-supervisor | Meta(全阶段) | **Meta** | temporary | 定义质量维度/阈值;分解目标派发子任务;评分决策(accept/improve/halt);**唯一 canonical 落盘者**——把采纳的技能补丁落 `skills/external/draw-diagram/` 并执行双写同步 |
| capability-builder | skill-capability-builder | executor | **Meta**(操作对象=技能定义) | temporary | 设计并实现可交互图表能力:只改 `optimization_target` 的**工作副本**(运行工作区内),产出定义类补丁,不写 canonical |
| capability-verifier | skill-verifier | evaluator | **Meta**(操作对象=技能执行效果与证据) | temporary | 以当前采纳的目标副本**实际执行** draw-diagram 绘制可交互图表,产出被评分交付物;按 3 维度评分并给「最大可改进点」;回归检查既有静态路径 |

**约束**:iteration 团队恰含**一个** Team Supervisor(Meta)。交付物为技能定义(定义类文件)→ Worker MUST NOT 直写 canonical,由 Supervisor 落盘(消解条款)。

## Dynamic Structure

**Pattern**:`iteration`(单谱系收敛——能力建设非多角度锦标赛,不设 variants/淘汰)。

**Loop 设置**:`threshold=0.8` · `max_iterations=5` · `regression_limit=2` · 三维权重 交互 0.45 / 正确 0.25 / 整合 0.30。

**握手**:file-path-only。capability-builder 在 `.specify/teams/.work/draw-diagram-interactive/gen-<N>/target-copy/` 改目标副本;capability-verifier 以该副本执行技能,产物与评分卡写入 `gen-<N>/`;canonical 落盘与双写同步只在达标采纳时由 Supervisor 执行。运行中间态全部留在 git-ignored 的 `.work/<slug>/`;最终交付物只落 `optimization_target` 真实路径 + 镜像副本。

### 单代执行流

```mermaid
flowchart TD
  S[Team Supervisor: 冻结本轮目标副本种子, 派发改进点] --> B[capability-builder: 改目标工作副本]
  B --> V[capability-verifier: 以副本执行 draw-diagram 绘制可交互图表]
  V --> E[capability-verifier: 3维评分 + 最大可改进点 + 静态路径回归检查]
  E --> D{Supervisor DECIDE}
  D -->|加权 >= 0.8| ACC[达标: Supervisor 落 canonical + 双写同步, 交付]
  D -->|未达标且未到上限| N[注入最大可改进点 -> 下一代]
  D -->|iter>=5 或 连续2代回归| HALT[停: 恢复历史最优并告警]
  N -.下一代.-> S
```

**每代五相**(iteration 标准相位):
1. **COORDINATE** — Supervisor 以上轮评分为种子,给 capability-builder 派改进子任务(territory = 本代工作副本目录)。
2. **EXECUTE** — builder 改目标工作副本(优化目标不变式:只改目标,不手改被评产物)。
3. **EVALUATE** — verifier 以副本**真实执行技能**再生产交付物并评分(含回归检查)。
4. **DECIDE** — 加权 ≥ 0.8 → 达标停;`iteration ≥ 5` 或连续 2 代回归 → 停并恢复历史最优;否则继续。
5. **IMPROVE** — 把 verifier 的「最大可改进点」注入下一代派发。

### Loop Card

| 相 | 内容 |
|----|------|
| **WHEN** | 用户发起 `/speckit.team run draw-diagram-interactive` |
| **SEE** | goal 定义(`.specify/goal/draw-diagram-interactive/goal.md`)+ 上轮 `runs/` 报告与评分历史 |
| **DO** | 一个迭代代:派 builder 改目标副本 → verifier 以副本执行技能产出交互图表 → 三维评分 |
| **CHECK** | 加权评分(交互 0.45/正确 0.25/整合 0.30)+ verifier 判据「经技能能绘制出随输入调整的网页图表」+ 既有静态路径回归 |
| **STOP** | threshold 0.8 达标 / iteration ≥ 5 / 连续 2 代回归(regression_limit) |
| **LEAVE** | `runs/<UTC-timestamp>-report.md`、评分历史、采纳副本由 Supervisor 落 canonical + 双写同步(diff -rq 校验)、goal summary 按门刷新 |

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports and Post-Run Critique.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team`.
- Boundary: preserve team authority, maturity gates, budget, kill-switch, and verifier independence.
- Verify: validate now and wait for a comparable later run before claiming improvement.
