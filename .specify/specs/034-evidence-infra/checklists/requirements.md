# Specification Quality Checklist: 公共证据采集基础设施(Better Harness 能力移植)+ improve-* 证据驱动改造

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-07-29
**Feature**: [requirements.md](../requirements.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs) — 说明:本需求属"基础设施移植"类,D1/D2/D3 决策(源码托管路径、Node/Python 双栈、合同字段)本身即需求约束,是 WHAT 而非 HOW;与既往基础设施类规格(027/033)口径一致
- [x] Focused on user value and business needs — 每个故事以维护者/技能作者/流程执行者视角陈述价值
- [x] Written for non-technical stakeholders — 关键机制均有中文语义解释(泳道、证据合同、干预台账)
- [x] All mandatory sections completed — Related Feature(默认待澄清)、Stories、FR、SC、Key Entities 齐备

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain — 2026-07-29 clarify 会话解决:FR-014 镜像策略定为全量镜像(Q2);标记清零(grep 验证 0 处)
- [x] Requirements are testable and unambiguous — 各 FR 均有 MUST/MUST NOT 边界与对应 SC
- [x] Success criteria are measurable — SC-001~008 均为 100%/零出现/一次通过类可核验口径
- [x] Success criteria are technology-agnostic — 以产物、演练与核对记录为口径;涉及 pytest/tests/js 处为项目既有测试栈事实而非新技术选型
- [x] All acceptance scenarios are defined — 7 个故事共 21 条 Given/When/Then
- [x] Edge cases are identified — 10 条(分叉漂移、边界侵蚀、降级、超龄、空源、隐私穿透、越界、候选膨胀、镜像漂移、目录权限)
- [x] Scope is clearly bounded — FR-001 子集边界 + 方案 §8 不移植清单纳入 Assumptions;US7 明示为持续演进长尾
- [x] Dependencies and assumptions identified — Assumptions 8 条,含方案开放问题的处置口径

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria — FR-001~014 均映射到 SC/场景;FR-014 已定稿(全量镜像)
- [x] User scenarios cover primary flows — 引擎落库 → 合同 → 自有泳道 → 公共技能 → 消费改造 → 纵向闭环 → 平台扩展全链路;US7 交付边界已定(doctor 报告 + 定序建议)
- [x] Feature meets measurable outcomes defined in Success Criteria — SC 覆盖全部 7 个故事;SC-008 拆分边界内/后续迭代口径
- [x] No implementation details leak into specification — 与 Content Quality 首项同口径:保留的路径/文件名为决策级约束;纯实现细节(函数名、行号)未进入规格。Feature 绑定已解决(Feature 038 Evidence Infrastructure,2026-07-29 clarify)

## Notes

- 已完成(2026-07-29 clarify):FR-014 镜像策略(全量镜像)与 Feature 绑定(038 Evidence Infrastructure)均已解决;另定 US7 交付边界(doctor 报告 + 定序建议,新适配器留后续迭代)。检查单全项通过,可进入 `/speckit.plan`。
- 已完成:subagent 对 better-harness 历史会话(1261e61e)的核实结果已回并应用——方案主体属实;三处修订已入规格:(a) Claude 会话适配器与资产 provider 源码已存在,US7 改为"核实补齐"而非从零自研;(b) FR-012 增加"平台支持以源码探测为准、不依赖上游 roadmap 文档"约束;(c) "48+ 条 feedback" 等时点计数改为动态探测口径(US3/SC-004/Assumptions)。
- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`
