# Feature Detail: SDD 临时 Goal / 临时 Team 与多 Agent 并发（SDD Temporary Goal/Team and Multi-Agent Concurrency）

**Feature ID**: 085
**Name**: SDD 临时 Goal / 临时 Team 与多 Agent 并发（SDD Temporary Goal/Team and Multi-Agent Concurrency）
**Description**: Preserve stage-specialized agents, worktree isolation, integration queues, and checkpoints; spec-local Temporary Goal/Team is superseded by the unified Anchor-bound archive model.
**Status**: Ready for Review
**Created**: 2026-11-06
**Last Updated**: 2026-11-22（requirements + plan + tasks + implement + review：smoke 43/43；final-path SC 7/7 pass；SC-009 pass（24 项失败在基线 aafbf5a8 复现）；SC-010 partial（未跑完整 driver dogfood）；`review.md` 落盘，code segment `not-evaluated`（评审早于最终提交；feature commit `2cb68c44` 已落盘）；当前 **Ready for Review**）

## Overview

现有 SDD 驱动（Feature 058/064/067/070/074/075）已具备 U0–U6、状态脊、阶段哨兵、工作包拆解、line registry、worktree 与嵌套调用，但 Goal/Team 只以两种方式与 SDD 相接：全局 Goal→Team→SDD 的嵌套调用（074），或驱动内部 run-scoped 的 stage-team preset（070，明确不持久化、不绑定 goal、写包串行）。因此没有一个机制能在一次 SDD 运行内部按阶段建立并持续调整 Goal/Team，也没有把多 agent 并发作为首要效率目标的阶段编排。

本 Feature 建立一条与全局层级并列的**临时层级**：`SDD run → Temporary Goal → Temporary Team → stage agents`。Temporary Goal 在 requirements 后由编排者撰写，Temporary Team 在 clarify+plan 后创建；两者都存放在当前 spec 目录下，随 spec 保留归档。Global Goal/Team 仍是上层控制链，SDD 运行对其只读，并通过 Ownership Manifest 的 forbidden paths 机械禁止写入。

效率是本 Feature 的唯一核心目标：SDD 启动时声明并发度（默认 24），每个阶段按有效并发、就绪工作包、验证预留与资源隔离动态决定 agent 数量与类型；写 agent 各占一条 child line 与独立 worktree，提交由既有集成队列按声明顺序串行完成。阶段边界设置 checkpoint，以既有 wp-report/team run report/ledger 为证据，至多提出一条 team 配置变更并在批准后应用；回归时回滚。

## Latest Review

2026-11-22 implementation audit: stage-specialized roles, the default 24-agent cap, child worktrees, integration queues, and 500-turn role definitions remain. The original spec-local Temporary Goal/Team model has been superseded by 094/101: `spec` and `global` scope values are rejected, and current teams bind Anchor. `Ready for Review` remains the lifecycle status; the old spec-local text below is historical.

## Key Changes

1. **阶段并发与角色族**：保留阶段专用 coordinator / worker / verifier / integrator、默认 24 agent cap、500-turn budget、checkpoint 与配置提案。
2. **当前归档与绑定**：原 spec-local Temporary Goal/Team 已由 094/101 的统一归档和 Anchor 绑定取代；退役的 `spec` / `global` scope 不再被接受。
3. **SDD 阶段接入**：U0 记录并发度（默认 24）与临时 scope 字段；requirements U4 后建 Temporary Goal；clarify+plan U4 后建 Temporary Team；tasks/implement/review 按有效并发扩张 agent。
4. **阶段专用 agent 角色语法**：coordinator / worker / verifier / integrator；用户点名 `sdd-requirement-analyzer`、`sdd-plan-coordinator`、`sdd-plan-executor`；数量与类型动态决定；删除泛化 `sdd-executor`。
5. **每 agent worktree + 集成队列**：child line 携带 `parent_line_id`/`line_role=agent-write`，独立 worktree/branch/territory；`SPECIFY_AGENT_CONCURRENCY_CAP` 默认 24；集成顺序来自工作包声明。
6. **Checkpoint 协同与配置优化**：每阶段四步 checkpoint（产物核验 / Goal degree / 至多一条配置提案 / 下一阶段并发与 roster），复用 improve-team 与 coordinate 的提案-批准形状。
7. **统一预算**：所有保留的框架 agent `run-turn-budget: 500`，渲染副本 `maxTurns`/`steps` 500；删除的 generic executor 不再出现在源、镜像、渲染副本与 manifest。

## Implementation Notes

- **两层级的边界**：Temporary Goal/Team 是 spec-local、run-scoped；对 `sdd-routing-definitions.md` § Hierarchy 只做追加式 carve-out，不反转 global Goal→Team→SDD 规则。
- **070 写串行兼容**：`shared-tree` 仍是默认，`write_isolation=worktree` 只对 temporary-team 运行开启；既有 pinned literal 以追加限定词的方式保留。
- **064 additive**：child line 字段全部可选；root line、ownership 与 integration queue 的既有语义逐字不变。
- **并发不是保证**：requested=24 是目标；effective 由宿主能力、stage max_parallel、ready packages、verifier reserve 与资源容量共同决定，降级必须记录原因。
- **磁盘与 worktree**：每个 child worktree 独立；实施前做磁盘预检，ENOSPC 是命名异常，不得删除其他 worktree 或静默重试。
- **历史记录不可改写**：`.specify/state/`、`.specify/memory/evidence/`、dated review/feedback 是输入，不是编辑对象。

## Future Evolution Suggestions

- 在 dogfood 数据足够后，评估把 checkpoint 的配置提案从“一条规则变更”扩展为有界的多候选比较，但仍复用现有 evidence 与审批形状。
- 如果宿主普遍支持更高的并发，可把 `SPECIFY_AGENT_CONCURRENCY_CAP` 的默认值上调；该值是单一 owner，不在各处复制。
- 若 Temporary Goal 需要跨运行复用，正确路径是显式提升为 Global Goal，而不是让第二次 SDD 运行重写第一次的临时 Goal。

## Related Files

- Feature Index: .specify/features.md
- Feature Detail: .specify/features/085-sdd-temporary-goal-team.md
- Requirements: .specify/specs/085-sdd-temporary-goal-team/requirements.md
- Test Evidence: .specify/specs/085-sdd-temporary-goal-team/test-evidence/（plan/implement 阶段填充）

## Related Specifications/Requirements

- `.specify/specs/085-sdd-temporary-goal-team/requirements.md`（本 Feature 唯一规格，50 FR / 10 SC）
- 相邻 Feature（只引用不改写）：058（U0–U6/状态脊）、064（line registry/worktree/集成队列）、067/075（循环效率）、070（工作包拆解/stage-team preset）、074/074a/074b（Global Goal→Team→SDD 层级与嵌套调用）。

## Status Tracking

- **Draft**: requirements 落盘并绑定 Feature 085；`validate-requirements.py` status ok、`pre-analyze-check.py --stage requirements` decision pass。
- **Planned**: `/speckit.plan` + `/speckit.tasks` 已完成：plan.md、data-model.md、5 个 contracts、quickstart.md、feature-ref.md、tasks.md 落盘；Constitution Check 全 Pass。
- **Implemented**: 26/26 任务关闭；final-path SC 7/7 pass；smoke 43/43；SC-009 pass、SC-010 partial（supporting）。
- **Blocked**: 任务关闭但至少一条 `final` 路径未 pass。
- **Ready for Review**: `review.md` 流水线四段 + ARC 完成；ARC `accept`，final-path 7/7；code segment `not-evaluated`（评审早于最终提交；feature commit `2cb68c44` 已落盘）；当前状态。
- **Completed**: 人工/治理最终验收。
- **Ready for Review** (current): review 与 ARC 已完成，final-path 7/7 pass；SC-010 supporting partial 已披露。原 spec-local Temporary Goal/Team 设计由 094/101 接续，状态不回退。
