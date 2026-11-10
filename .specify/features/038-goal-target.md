# Feature Detail: Evidence Infrastructure

**Feature ID**: 038  
**Name**: Evidence Infrastructure  
**Description**: Public evidence-collection infrastructure ported from Better Harness (`/cws_work/better-harness`, commit `b2e621d`, MIT): a consumer-neutral evidence layer producing a unified `findings.json` contract across 5 lanes, plus the evidence-first refactor of the improve-* skills and a longitudinal verification loop (intervention ledger + compare).  
**Status**: Implemented  
**Created**: 2026-07-29  
**Last Updated**: 2026-07-29

## Overview

把 Better Harness 的证据采集与规范化能力移植为 Spec Kit 的基础设施级公共流程,遵循方案文档 `draft/2026-07-29-better-harness-evidence-port-plan.md`(Draft v2)的三项已定决策:

- **D1 源码复制托管**:采集子集(session-analysis、core-change-watch、agent-customize、asset-baseline、可选 dependency-governance,约 1.0 MB、零 npm 依赖)复制到 `scripts/js/better-harness/`,附 UPSTREAM.md 溯源台账 + MIT LICENSE;与上游再同步为手动、按文件、diff 驱动。
- **D2 多 CLI 扩展自有演进**:平台适配器(会话适配器 + 资产 provider)成为 Spec Kit 自有演进面,逐步覆盖八种受支持工具;现状以源码探测(doctor)为准,不依赖上游 roadmap 文档。
- **D3 Spec Kit 执行工件入证据**:teams 运行工件(runs/、STATE.md、run-log.jsonl)与 `.specify/memory/feedback/` 条目升格为一等证据泳道(纯 Python 实现,无 Node 时保底可用)。

两层分离:公共证据层(collect-evidence 技能 + evidence-utils.py 编排器 → findings.json 合同,evidenceState 七态,剥离一切裁决字段)对消费者中立;消费层(improve-skills/agent/team)按 evidenceState 分拣候选(Unobserved 红线、候选冻结)后走各自既有优化流程;干预台账 + compare 提供纵向验证(Outcome-supported 判定,禁止无证据"已修复"结论)。

四条证据纪律:配置存在 ≠ 观察到使用;未观察保持 Unobserved 不推断;计数只路由不产生发现;隐私语义面片不出原文。

## Key Changes (planned)

1. `scripts/js/better-harness/` 引擎子集落库(+ UPSTREAM.md、LICENSE、tests/js/ 子集测试)。
2. `evidence-utils.py`(stdlib-only):doctor/collect/list/latest/compare;产物落 `.specify/memory/evidence/<run-id>/`。
3. runs / feedback 两条 Spec Kit 自有泳道(纯 Python)。
4. `collect-evidence` 技能(双镜像 + 注册表)+ `.specify/shared/workflow/evidence-step.md` 单一事实源。
5. improve-skills / improve-agent / improve-team 接入证据步骤;improve-team 原始工件解析下沉为 runs 泳道消费。
6. 干预台账 + compare 纵向验证闭环。
7. 平台适配器持续扩展(顺序以 doctor 探测定序)。

## Related

- Spec: `.specify/specs/034-evidence-infra/requirements.md`
- 关联(数据源/消费者,非归属):028 Feedback Mechanism(feedback 泳道数据源 + feedback-step 对偶约定)、027 Team Management(runs 泳道数据源、improve-team 消费方)、013 Skills Command(collect-evidence 技能载体)。

## Latest Review

2026-07-29 `/speckit.implement`:41/41 任务完成(零延期)。落地:引擎子集(b2e621d,~1.1MB,零 npm 依赖;剔除 findings-recommend 裁决层、补入 asset-eval 隐性依赖)+ UPSTREAM.md/LICENSE + 全量镜像;evidence-utils.py 五 action ×2 镜像;五泳道全通(无 Node 降级实测:三 Node 泳道显式 unavailable、runs/feedback 保底交付);collect-evidence 技能(中立红线由结构测试钉住,含 runtime-mode gate)+ evidence-step.md 双镜像;improve-* 三技能证据先行改造(improve-team 原始工件解析下沉 runs 泳道);两轮 dogfood 闭环(干预台账 → compare verdict=Unobserved 诚实判定);平台探测报告交付。测试:node 182/182 + 新增 contract 62 + integration 13;全套 84F/953P 相对基线零新增失败(失败集 diff 证明)。SC-001…008 全 pass。状态 Planned → Implemented。

2026-07-29 `/speckit.plan`:plan.md(Constitution Check 11 原则,VIII 为受治理分叉 Partial 豁免)+ data-model(9 实体 E1–E9)+ contracts ×3(findings 合同 C-F1…14 / evidence-utils CLI C-E1…11 / 子集边界 C-B1…7)+ quickstart(7 场景,含无 Node 降级)+ feature-ref。勘察修正两点入 plan:CLI 入口结构(session-analysis 入口在根级、core-change-watch 无 cli.mjs)、agent-lint 4 文件纳入子集(asset-baseline 的 lint 依赖)。交付边界:US1–US6 + doctor 探测报告(Clarify Q3)。状态 Draft → Planned。

2026-07-29 `/speckit.requirements` + `/speckit.clarify`:spec 034 起草完成(7 用户故事、FR-001~014、SC-001~008、11 Shared Strings);subagent 核实 better-harness 历史会话(1261e61e)修订 3 处事实偏差(Claude 适配器上游已有源码、源码探测优先于上游文档、时点计数动态化);Feature 038 注册。状态 Draft。
