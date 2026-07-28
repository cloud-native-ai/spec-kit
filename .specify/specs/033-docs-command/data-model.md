# Data Model: /speckit.docs (Feature 037)

实体均为文件/文档形态（模板框架，无数据库）。字段名与字面量以 requirements.md `## Shared Strings` 为单一事实源（[[STR-001]]="draft"、[[STR-002]]="expired"、[[STR-003]]="archived"、[[STR-004]]="expires"）。

## 1. Docs Space（文档空间）

| 字段 | 说明 | 校验 |
|------|------|------|
| root_entries | 根目录入口文件集：README.md、ARCHITECTURE.md、CONTRIBUTING.md、CHANGELOG.md | 名称全大写（FR-010）；"一屏"尺寸阈值（FR-007，确定性） |
| docs_tree | `docs/` 目录树：concepts/ tutorials/ tasks/ reference/ decisions/ contribute/ notes/ | 六类正式目录 + notes 临时区（FR-002） |
| archive_zone | `docs/archive/` 归档区 | 只进不出；同名冲突后缀 `__<ts>` 避让（FR-004） |
| workspace | `.specify/docs/` 运行产物工作区 | 干跑计划、审计日志落盘处（FR-003）；不混入 docs/ |
| zones | A=root_entries+docs_tree（读写）；B=代码/规格目录（只读）；C=符号链接等锚点（跳过） | 越区写入为缺陷 |

## 2. Desired-State Baseline（期望态基线）

合成来源（优先级升序，FR-003）：模板 < 规则阈值 < 原则 < 外部权威事实 < 本地既有惯例 < 本次用户输入。
组成：目录分类（FR-002）、根目录职责（FR-010 注册表）、尺寸/命名/链接规则（FR-007）、文档生命周期流转（FR-002c）。

## 3. Special-Name Registry（特殊文档注册表，FR-010）

| 字段 | 说明 |
|------|------|
| name | 全大写文件名（唯一键） |
| semantic | 固定语义（一行） |
| location | 约定位置（当前均为项目根目录） |

种子数据：README.md=索引 docs/ 全部；ARCHITECTURE.md=摘要 concepts+decisions；CONTRIBUTING.md=摘要 contribute；CHANGELOG.md=自包含时间线。
规则：可扩展（新增须登记 semantic）；普通文档 kebab-case、禁用保留名；违规属确定性差异维度。

## 4. ADR Entry（决策记录，FR-005）

| 字段 | 说明 | 校验 |
|------|------|------|
| number | 四位序号 NNNN | 连续性为确定性维度 |
| title / date / deciders | 标题、YYYY-MM-DD、决策者 | 必填 |
| status | Proposed \| Accepted \| Deprecated \| Superseded by ADR-XXXX | 状态只标注不改写历史 |
| body | 背景 / 决策 / 替代方案 / 后果 | 模板四节 |

状态迁移：Proposed → Accepted → (Deprecated | Superseded by)；只追加，无删除。

## 5. Note（notes 临时文档，FR-006）

frontmatter（YAML，扁平键值）：

| 键 | 必填 | 校验 |
|----|------|------|
| title | ✅ | 非空 |
| created | ✅ | ISO 日期 |
| [[STR-004]] (expires) | ✅ | ISO 日期；默认 created + 60 天 |
| status | ✅ | ∈ { [[STR-001]], [[STR-002]], [[STR-003]] } |
| target | ❌ | 预期归宿路径；status=[[STR-003]] 时必填且文件须存在 |
| tags | ❌ | 列表 |

状态机（FR-006b）：
```
draft --(超期扫描标记)--> expired --(人工确认删除)--> [删除，仅限 notes 区]
draft --(合入 target)--> archived（正文顶部标注归宿链接）
expired --(续期：更新 expires)--> draft
```

## 6. Reconcile Artifacts（调谐产物，FR-003）

| 产物 | 形态 | 落点 | 必产 |
|------|------|------|------|
| 观察快照 | 内联报告 | 会话内 | ✅ |
| 干跑计划 | 文件（`[x]/[ ]` 可勾选退出行） | `.specify/docs/plans/` | 移动/归档/重组类动作存在时 |
| 审计日志 | 文件（时间戳、作用域、逐项动作+结果、容忍摘要、回滚依据） | `.specify/docs/audit/` | ✅（零收敛也落"全维度在容忍带内"） |
| 残差报告 | 内联报告（已收敛/已归档/已容忍/待人工决策） | 会话内 | ✅ |

## 7. Docs-Sync Step（文档同步步骤，FR-011）

| 字段 | 说明 |
|------|------|
| 定义源 | `shared/workflow/docs-step.md`（+ `.specify/shared/` 镜像）单一事实源 |
| 插入点 | 核心命令收尾，与 Feedback 步骤同一生命周期点 |
| 输入 | 本次运行产生的信息（新能力/决策/结构变化） |
| 输出 | `需记录（目标文档 + 要点）` 或 `无需记录` 二选一 |
| 约束 | 非阻断；增量评估（禁全量 R0–R6）；写入遵循期望态基线 + 安全写入门禁 |

## 实体关系

Desired-State Baseline ⊇ Special-Name Registry；Docs Space 被调谐环消费产出 Reconcile Artifacts；Note ∈ Docs Space.docs_tree.notes；Docs-Sync Step 的写入目标 ∈ Docs Space（经语义路由）；ADR Entry ∈ docs_tree.decisions。
