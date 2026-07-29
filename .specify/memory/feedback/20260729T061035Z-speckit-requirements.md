---
id: "20260729T061035Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "034-evidence-infra-20260729"
scope: "local"
feature: "034-evidence-infra"
partial: false
created: "2026-07-29T06:10:35Z"
summary: "对 better-harness 证据基础设施移植方案完成规格化:7 用户故事、14 FR、8 SC、11 Shared Strings;并行 subagent 核实历史会话后修订 3 处事实偏差(Claude 适配器现状、源码探测优先于上游文档、时点计数动态化);保留 1 个镜像策略澄清项交 /speckit.clarify。"
---

## Review
对 better-harness 证据基础设施移植方案完成规格化:7 用户故事、14 FR、8 SC、11 Shared Strings;并行 subagent 核实历史会话后修订 3 处事实偏差(Claude 适配器现状、源码探测优先于上游文档、时点计数动态化);保留 1 个镜像策略澄清项交 /speckit.clarify。

## Optimization Points
- 后台 subagent 与主线规格起草并行是有效模式,但规格中依赖 subagent 核实的事实性声明(平台矩阵、子集大小、存量计数)应从一开始就写成"待核实/动态探测"口径,避免结果返回后需要多处回改(本次回改了 US3/US7/FR-012/SC-004/Assumptions 五处)。
- 对"移植类"需求,建议命令流程显式增加一步"上游文档 vs 上游源码一致性预检",本次发现上游 roadmap 与代码不一致(Claude provider 已实现但文档称缺失),该类偏差直接影响故事优先级与工作量估计。
