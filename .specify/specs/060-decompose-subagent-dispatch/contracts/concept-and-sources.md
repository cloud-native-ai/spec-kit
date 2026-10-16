# Contract: 概念真源深化（concept-and-sources）

**Feature**: 060 | **FR 覆盖**: FR-001, FR-002, FR-006, FR-009, FR-013（真源侧条款——以本文件可追溯性表为准）
**性质**: 结构契约——条款由契约测试机械判定（tests/contract/test_agent_dispatch_mechanism.py，实现期落位）。

## S 节：agent-definitions.md 扩格

- **C-1**: agent-definitions.md MUST 在既有结构内增补「驱动子代理作为公用机制」的接线段（建议落点：Transformation Chain 节后），内容为：编排类技能（sdd-loop-driver / sdd-project-setup 等）行使三层的方式——创建经 create-agent、派发经 run-agent、修正经 improve-agent；该段 MUST 引用 subagent-definitions 与 external-dispatch-recipes，MUST NOT 复制其规则正文。
- **C-2**: 该接线段 MUST 声明职责切分线：框架调协与 SDD 循环编排 = 驱动技能本体；创建/派发/修正 = 三技能承接面。编排本体（六阶段循环、状态脊、调协五步、候选清单）MUST NOT 被描述为三技能职责。
- **C-3**: agent-definitions.md 的三层词条 owner 地位不变：本特性 MUST NOT 在该文件之外新增三层定义性正文（全仓检索判定，SC-006）。

## S 节：subagent-definitions.md 扩格

- **C-4**: subagent-definitions.md MUST 增补「Execution 拓扑声明」段：本地/远端两拓扑要素表（数据模型 E3 的字段面）、内联参数与执行配置文件双形态、冲突拒收规则（同给且任一要素不一致 → 拒收并列冲突字段，快速失败纪律）。
- **C-5**: 该段 MUST 声明与 external-dispatch-recipes.md 的既有分工不变：本段拥有"声明什么"，配方文档拥有"怎么执行"；分歧时契约赢（既有规则延续）。
- **C-6**: 反嵌套义务 MUST 以引用形态出现在 subagent-definitions 的 Dispatch-Time Governance Obligation 节（指向 run-agent 的派发前置义务），原文语义（循环层级恒为 1）MUST NOT 被改写。

## S 节：层界判定规则（FR-002 落点）

- **C-7**: 抽象阶梯的层界判定 MUST 固化为三行可判定规则，落在 agent-definitions.md 接线段内：Template=能力面（含"以项目目录为工作目录、加载项目上下文、执行 SDD 命令"三要素即判 Template 层）；Instance=职责绑定（capacity-scope 引用 + 单一职责）；Execution=运行拓扑（任一拓扑要素出现即判 Execution 层）。
- **C-8**: 越层变更禁令 MUST 成文：改能力不改拓扑、改拓扑不改能力——判定方式：一次变更 diff 涉及的实体层（E1/E2 vs E3 字段面）。

## 可追溯性

| 条款 | FR | 测试（实现期） |
|------|-----|----------------|
| C-1/C-2 | FR-001, FR-013 | test_c1_delegation_section_in_agent_definitions |
| C-3 | FR-001 | test_c3_no_third_owner_of_three_layers |
| C-4/C-5 | FR-006（真源侧） | test_c4_topology_declaration_section |
| C-6 | FR-009 | test_c6_anti_nesting_referenced_in_governance |
| C-7/C-8 | FR-002 | test_c7_layer_boundary_rules_present |
