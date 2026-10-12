---
name: 重构后机制完整性团队
slug: post-refactor-mechanism-integrity
description: serial 三阶段链(S1 修复与端态回归测试 → S2 升级仿真独立验证 → S3 判据对账与收口),把「反向迁移缺口修复 + 全 .specify 面机制对账」从设计落到验证闭合;阶段内 native 并发派发,每次交接独立验证门
goal: >
  承接已定义 Goal `post-refactor-mechanism-integrity`(权威定义:.specify/goal/post-refactor-mechanism-integrity/goal.md)。
  本字段仅为可读性渲染,与定义不一致时以定义为准。终态:客户项目旧 .specify 结构经新版 specify init 升级后正常运转
  (平铺 internal 残留清除、用户技能红线不动、内部技能不可见);且 .specify 除 skills/ 外全部目录与文件均有机制支撑,无无主文件。
  **成功判据以定义为准,本团队不复述其文本**(定义持有 1 条)。
goal_slug: post-refactor-mechanism-integrity
territory:
  write:
    - src/specify_cli/**            # F1/F2 升级迁移时序与双存语义(单引擎文件)
    - tests/**                      # F3 端态回归测试 + 相关用例修订
    - docs/**                       # 迁移方案收敛(notes → 升级节要点稿)与发布相关文档
    - .specify/teams/post-refactor-mechanism-integrity/**   # 团队自身 run 信息
    - .specify/memory/feedback/**   # 反馈条目
    - .specify/memory/register.md   # 编号登记追加(指针行)
    - .specify/skills/**            # 仅由 sync-mirrors.py 再生成写入;MUST NOT 手改
    - .qoder/commands/**, .claude/commands/**, .github/prompts/**, .opencode/command/**   # 仅由 regen-command-copies.py 写入
  read:
    - .specify/goal/post-refactor-mechanism-integrity/**
    - .specify/**
    - skills/**
    - scripts/**
    - shared/**
    - docs/**
  forbidden:
    - .specify/goal/**             # authored:只经 /speckit.goal 引擎渲染
    - .qoder/agents/**             # 宿主 agent 注册面:仅由 render-agents 渲染器写;禁手改
    - .qoder/skills/**             # 与 .specify/skills 的同源符号链接面
    - .github/skills               # 符号链接
    - AGENTS.md, CLAUDE.md, QODER.md, .github/copilot-instructions.md   # 兼容符号链接,经 /speckit.instructions 再生
    - .specify/memory/feedback/probe-map.md   # 派生物:由 feedback-utils.py --action map 重建,禁手编
  non_path:
    - { type: dispatch-modality, target: 阶段内独立单元以 **native** 并发派发(一响应块多调用);framework-engineer / skill-verifier 两席均已驻宿主注册面;supervisor 由编排会话承担(virtual,不发任务给自身)。virtual 仅作宿主不可用时的降级并须披露 }
    - { type: write-authority, target: 业务路径(src/tests/docs)由 Worker 在 territory 内直写;定义类文件(team.md / agent 定义)由 Worker 产出工作区补丁、MUST 由唯一 Meta supervisor 落 canonical;SKILL.md 类文件本团队不涉(除非另行裁定) }
    - { type: evidence-base, target: S1 的红先行基准 = docs/notes/consumer-upgrade-migration-plan.md §1(旧消费者升级仿真:kept 15 = 缺陷样本;命令与 transcript 在 §7);S2 复核 MUST 独立重跑仿真而非复用其 transcript }
    - { type: handover, target: 本团队承接 /speckit.goal 创建的 goal `post-refactor-mechanism-integrity` 与已设计迁移方案 F1–F3;T-001(open)为唯一 Target,单团队路径不设 focus_target,run 级可 --target T-001 聚焦 }
    - { type: ceiling, target: 门控预算——`python3 .specify/scripts/python/scan-confirmation-gates.py` 的 total MUST 保持 ≤ 23(易变测量值以可重跑命令 + as-of 基线表达) }
    - { type: regeneration, target: canonical 落盘后 MUST 依序跑两再生成引擎并 --check 退出 0:`scripts/python/sync-mirrors.py` 与 `scripts/python/regen-command-copies.py`(自 canonical 副本调用);镜像不删旧投影,退役条目手工回收并披露 }
    - { type: checkpoint, target: 起步状态(2026-10-11):树全绿 —— 两引擎 --check 0、门控 23、全量 3523P/1F(c7 为另案窗口项,见 register);重构两提交已推三端;升级仿真现场 /tmp/upgrade-sim 与 /tmp/sim-wheel 留存 }
pattern: serial
created: 2026-10-11
updated: 2026-10-11
members:
  - agent: agent-team-supervisor-template
    role: team-supervisor
    stage: meta
    type: Meta
    lifecycle: temporary                 # 只解析为 .specify/skills/internal/create-team/templates/agents/ 下的临时模板;由编排会话承担
    responsibility: 唯一 Meta 与 Lead:读 goal 判据 + progress → 按拓扑序派发阶段;阶段内把独立单元并发派发给 native 席位 → 消费 skill-verifier 判定表跑交接验证门 → 唯一有权把定义类补丁落到 canonical → canonical 落盘后跑再生成引擎并核实 --check 0 → 每阶段收尾跑门控与测试子集 → 写 run report / progress;永不亲自执行单位任务
    blockedBy: []
  - agent: framework-engineer
    role: framework-engineer
    stage: executor
    type: Worker
    lifecycle: temporary                 # 席位生命周期为单次运行;容量定义持久于 .specify/agents/instances/framework-engineer.agent.md(已渲染 .qoder/agents/)
    responsibility: 单位执行者(可并发多重 Execution):F1/F2 引擎修复、F3 端态回归测试、判据对账表与迁移文档收敛——均限派发 territory 内;定义类文件只产补丁
    blockedBy: []
  - agent: skill-verifier
    role: contract-checker
    stage: evaluator
    type: Meta
    lifecycle: temporary                 # 容量定义持久于 .specify/agents/templates/skill-verifier.agent.md(已渲染 .qoder/agents/)
    responsibility: 每次交接的独立判定席(默认 REJECT):独立重跑升级仿真(独立 venv + 新 wheel,不复用他人 transcript)、回放 S1 测试、核判据证据;判定 MUST 附实读证据(路径 + 具体事实);只写判定报告到工作区,不落 canonical
    blockedBy: [framework-engineer]
config:
  handoff_protocol: file-path-only
  progress_file: .specify/teams/.work/post-refactor-mechanism-integrity/progress.md
  failure_strategy: retry-once-then-escalate
  verification: independent
  dispatch: native-concurrent
  progression: S1 → S2 → S3
  target_map:
    T-001: [S1-fix-and-regression, S2-upgrade-sim-verify]
    # S3-criterion-reconcile 对 goal 整体(无 target_ref)
  regeneration: >
    每次 canonical 落盘后由 supervisor 依序执行(并核实 --check 退出 0):
    ① `python3 scripts/python/sync-mirrors.py`;② `python3 scripts/python/regen-command-copies.py`。
    MUST 自 canonical 副本调用。
  invariants: >
    每个 stage 的 quality_gate MUST 复核:① 门控扫描 total ≤ 23;② 补丁不触碰 territory.forbidden;
    ③ 有 canonical 落盘者,两再生成引擎已跑且 --check 0;④ 并发单元的 territory 两两不相交(派发载荷逐单元声明)。
summary:
    enabled: true
    every: 1
    delivery_dir: .specify/goal/post-refactor-mechanism-integrity/summary/
    interactive: false
---

## Goal

**权威定义**:`.specify/goal/post-refactor-mechanism-integrity/goal.md`(`goal_slug` 引用,非内容副本)。终态与判据以定义为准;本文件不复述判据文本。可达成性分析(创建时):单团队短期可达成——工程切片 = 已设计 F1–F3(小改、单引擎文件),判据对账面可枚举。

## Static Structure

| Agent | Role | Stage | Type | Lifecycle | 派发模态 | 写面（显式） |
|-------|------|-------|------|-----------|----------|--------------|
| `agent-team-supervisor-template` | team-supervisor | meta | **Meta** | temporary | virtual（编排会话承担） | canonical 定义类落盘、两引擎输出、团队目录、progress、report |
| `framework-engineer` | framework-engineer | executor | Worker | temporary（容量持久） | **native（并发）** | territory 内业务路径直写（src/tests/docs） |
| `skill-verifier` | contract-checker | evaluator | **Meta** | temporary（容量持久） | **native** | 仅工作区（判定报告） |

**席位解析**:三席均解析到既有持久容量定义(instance/template),**无新席位实例化 → 无 render-agents 渲染触发**(经任务项 7 判据)。

## Dynamic Structure

**Pattern**:serial(质量优先)。选择依据:修复→仿真验证→对账收口为强依赖链(S2 消费 S1 产物、S3 消费 S2 证据),DAG `S1 → S2 → S3`;并发性体现在阶段内单元级(如需拆并发),不改变链式语义。

**Workflow**:

```json
{
  "workflow_id": "post-refactor-mechanism-integrity-chain",
  "name": "重构后机制完整性链",
  "stages": [
    {
      "stage_id": "S1-fix-and-regression",
      "agent_kind": "framework-engineer",
      "target_ref": "T-001",
      "task": "F1 将 migrate_flat_internal_skills 调用重排至内部层拷贝之前(真升级由此 migrated 15/kept 0);F2 双存分支对框架名单内平铺旧副本改为移除(计数 removed_stale;用户技能红线不动),同步修订既有 both-exist 用例期望;F3 新增端态回归测试(伪 resource 树+伪旧装 → 跑拷贝+清理/迁移 → 断言:平铺内部名=0、nested=15、用户技能在、副本引用=运行时形),红先行基准=docs/notes/consumer-upgrade-migration-plan.md §1(kept 15 样本)。",
      "inputs_from": [],
      "outputs": [".specify/teams/.work/post-refactor-mechanism-integrity/S1/"],
      "blockedBy": [],
      "quality_gate": "① F3 测试先红(kept 样本)后绿(红先行证据)② 相关测试(迁移/重写/移植三组)全绿 ③ 两引擎 --check 0 ④ 门控 ≤ 23 ⑤ 不含 forbidden 改动"
    },
    {
      "stage_id": "S2-upgrade-sim-verify",
      "agent_kind": "skill-verifier",
      "target_ref": "T-001",
      "task": "独立复核:以独立 venv + 本仓新 wheel 对伪旧消费者独立重跑升级仿真(不复用他人 transcript),断言端态与研究方案 §5 自检片段;回放 S1 全部测试;出逐项判定表(附实读证据)。",
      "inputs_from": ["S1-fix-and-regression"],
      "outputs": [".specify/teams/.work/post-refactor-mechanism-integrity/S2/"],
      "blockedBy": ["S1-fix-and-regression"],
      "quality_gate": "① 判定表全 PASS(附实读证据≥2处)② 仿真端态:平铺内部名=0 / nested=15 / 用户技能原样 ③ 未发现异常或具名上送"
    },
    {
      "stage_id": "S3-criterion-reconcile",
      "agent_kind": "framework-engineer",
      "target_ref": null,
      "task": "判据对账与收口(goal 整体):`.specify/` 除 skills/ 外逐目录/文件 → 机制支撑(流程/脚本)对照表,覆盖无遗漏、缺口零或全部具名(修或转交);迁移方案文档按 S1/S2 结论收敛(notes → 目标文档升级节要点稿);发布清单(版本号、升级命令、自检片段)成稿待发布流程消费。",
      "inputs_from": ["S2-upgrade-sim-verify"],
      "outputs": [".specify/teams/.work/post-refactor-mechanism-integrity/S3/"],
      "blockedBy": ["S2-upgrade-sim-verify"],
      "quality_gate": "① 对账表逐项可定位(文件→支撑机制)且无遗漏面 ② 缺口为零或全部具名(附处置)③ 引擎/门控复核 ④ 不含 forbidden 改动"
    }
  ],
  "handoff_protocol": "file-path-only",
  "progress_file": ".specify/teams/.work/post-refactor-mechanism-integrity/progress.md"
}
```

**DAG（无环）**:`S1 → S2 → S3`;交接串行,每门由 skill-verifier 独立验证(S2 本身即独立验证席,S1/S3 的交接门由 skill-verifier 承担)。

**失败策略**:retry-once-then-escalate;MUST NOT 用 retry 承载单元累积。

**Summary 刷新**:每阶段交接验证通过后刷新一次(`every: 1`)→ `.specify/goal/post-refactor-mechanism-integrity/summary/`;门控顺序与状态行口径由 `skills/internal/create-team/SKILL.md` §Summary Refresh 持有。

## Self-Improvement Contract

- Subject: this persisted team definition; member executions are evidence.
- Observe: completed run reports and Post-Run Critique.
- Improve: follow `.specify/shared/workflow/self-improvement-workflow.md`; route through `improve-team`.
- Boundary: preserve team authority, dispatch-concurrency mandate, budget, kill-switch, and verifier independence.
- Verify: validate now and wait for a comparable later run before claiming improvement.
