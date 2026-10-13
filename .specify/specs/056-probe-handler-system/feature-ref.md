# Feature Reference: 056 ← 056-probe-handler-system

**Spec**: `.specify/specs/056-probe-handler-system/requirements.md` | **Date**: 2026-10-13

## 绑定

- **Feature ID**: 056
- **Feature Name**: Probe-Handler 体系（伞形：Probe / Handler / HandlerBinding 基础设施）
- **Feature Detail**: `.specify/memory/features/056.md`
- **Feature Index 行**: `.specify/memory/features.md`（本次规划推进 Draft → Planned；Implemented 属 /speckit.implement）
- **绑定裁决**: clarify Q2 — 新建伞形 Feature 056；Feature 028 降为域实例（反向交叉引用已写入 028.md）。

## FR → 设计产物映射

| FR | 主题 | 承载产物 |
|----|------|----------|
| FR-001 | 真源伞形扩格（6 Class/72 Object 不变，Slices 启 scripts） | data-model.md § 1/§ 注册表文件布局；contracts/handler-registry.md |
| FR-002 | 新 Class/Object 入册（050 / 运行判定 / 证据 lane，带代码锚点） | data-model.md § 1/§ 2（锚点行号实测） |
| FR-003 | 锚点双向对账 + 变异演练 | contracts/compile-embeds.md § 契约测试锚点（test_probe_engine_action_sets 域） |
| FR-004 | 非实体 probe 目录（纯指针，不入计数） | data-model.md § 3；contracts/handler-registry.md |
| FR-005 | Handler 六字段封闭集 | data-model.md § 4；contracts/handler-registry.md |
| FR-006 | Binding selector/scope/身份三元组/合并规则 | data-model.md § 5；contracts/handler-registry.md |
| FR-007 | action 封闭集对账 + behavior_owner 可达 | contracts/engine-action-sets.md；contracts/handler-registry.md § 校验规则 |
| FR-008 | MVP 5 handler + 次序约束 | data-model.md § MVP Seed Data |
| FR-009 | 引擎动作分区（5/11）+ 外部存储零迁移 | contracts/probe-registry.md；contracts/engine-action-sets.md |
| FR-010 | 编译渲染规则（kind 派生调用形式，Q4）+ 确定性不变量 | contracts/compile-embeds.md；data-model.md § 6 |
| FR-011 | compile → regen → sync 次序契约 | contracts/compile-embeds.md § 传播次序契约 |
| FR-012 | handlers 查询面 + --check + 原子写 + 宿主只读 | contracts/probe-registry.md；contracts/compile-embeds.md |
| FR-013 | 五项语义零回退 | data-model.md § 解析与编译算法 步骤 5/6；Mirror Obligations（既有契约测试延续） |
| FR-014 | order 次序依赖钉住 | data-model.md § Validation Rules Summary 第 7 条 |
| FR-015 | 生成措辞零 BLOCKING_PATTERNS | contracts/compile-embeds.md § 拒写条件 |
| FR-016 | 迁移完成态（唯一形态 / 零段语义） | contracts/compile-embeds.md § 输出与写入语义；plan.md § SC-007 基线 |
| FR-017 | 产物↔真源双向零缺漏（exit 2 错误类） | data-model.md § 漂移与对账错误类 |
| FR-018 | 二期 binding 同规则（显式不入 MVP） | plan.md Technical Context Constraints ⑤；data-model.md（lifecycle_point 值域） |
| FR-019 | 词汇表四改三增 | contracts/handler-registry.md § 词汇表义务 |
| FR-020 | 行为真源冻结 + 接线引用类最小编辑 | plan.md Mirror Obligations（feedback-step/docs-step 行）；data-model.md § 4 |
| FR-021 | 宿主只读（Q6） | contracts/probe-registry.md § 公共旗标；contracts/engine-action-sets.md § 与宿主的关系 |
| FR-022 | docs/reference 更新 | plan.md Source Code tree（docs/reference/skills/ 行） |

SC 映射：SC-001–SC-008 的测量源冻结于 requirements.md § Measurement Sources；SC-007 改前数值 853 冻结于 plan.md § SC-007 基线（具名小节）。

## 本规划对 Feature 记录的更新义务（由 /speckit.plan 收尾执行）

1. `.specify/memory/features.md`：行 056 状态 Draft → Planned；Last Updated 刷新。
2. `.specify/memory/features/056.md`：Status → Planned；Latest Review 记录本规划裁决（引擎分区 5/11、69 编译单元实测、853 基线、behavior_owner kind 分派）。
