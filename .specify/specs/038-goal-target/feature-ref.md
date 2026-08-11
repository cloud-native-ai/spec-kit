# Feature Reference: 038-goal-target

**Bound Feature**: Feature 041 — Goal Registry(见 `.specify/memory/features.md` 行 041 与 `.specify/memory/features/041.md`)
**绑定裁决**: 038 clarify/requirements 阶段——Target 是 Goal 概念自身的组成机制(定义随 `goal.md` 归档、由 `/speckit.goal` 撰写、身份挂在 goal 命名空间下),不是团队属性;故与 037 同挂 Feature 041,而非 Feature 027(Team Management)。

## 本计划到 Feature 041 的映射

| Feature 041 已落地能力(037 实现) | 本计划在其上的扩展 | 依据 |
|------------------------------------|--------------------|------|
| `.specify/goal/<slug>/goal.md` 三段式定义(objective / criteria / lifecycle) | 新增**可选装饰件** [[STR-001]] 节——不是第四组成部分(概念锚 annex 定性);三段式与零 Target 行为逐字节不变 | FR-002 |
| `/speckit.goal` 单一撰写入口(create/modify/view/status/criteria/migrate) | 同一入口新增 `targets` 动作组(add/list/set);不另立引擎 | FR-007 |
| `## History` 变更追溯 | Target 授权与状态迁移复用该记法 | FR-006 |
| 036 两级身份解析 + GI-1…GI-4 + summary 交付目录 | **全部不动**——run 级变量是 Target,绑定轴保持静态 | FR-012 |
| `items.jsonl` 台账契约(IL-1…IL-5) | 叠加可选 [[STR-003]] 字段,既有不变式保持 | FR-013 |
| 判据轴(summary 里程碑 = 判据投影,036 FR-013) | 切片轴与其分列;done Target 仅以来源标记**叠加**进里程碑视图 | FR-014…FR-016 |

## 交叉引用

- **Feature 027(Team Management)**:团队侧两个消费面(run 指派、台账归属)触碰其章程边界但不改章程——`templates/commands/team.md` 与 `skills/create-team/` 的变更属 027 的文件域、041 的概念域,经本计划统一扇出。
- **Feature 041 状态处理**:041 当前状态 Implemented(037 交付);038 是其后继扩展切片,不回退状态——features.md 与 details 以注记形式记录 038 规划,状态推进待 038 implement 完成时一并评估。

## 新 Feature 评估

不创建新 Feature:Target 无独立生命周期管理面、无独立注册表——其注册表就是 goal 定义文件本身,与 Feature 041 的"goal 作为一等概念"同一概念域。
