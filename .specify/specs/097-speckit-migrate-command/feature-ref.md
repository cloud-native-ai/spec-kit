# Feature Reference — 097 → Feature 024

**Spec**: `requirements.md` · **Plan**: `plan.md` · **Date**: 2026-11-10

## 绑定

| 项 | 值 |
|----|-----|
| Feature ID | 024 |
| Feature Name | Specification Workspace Versioning |
| Feature Detail | `.specify/features/024-specification-workspace-versioning.md` |
| Index Row | `.specify/features.md`（本阶段由 Draft 推进为 **Planned**） |
| 本规格身份 | Feature 024 的首个子规格；实现其「跨 CLI 版本的 `.specify/` 工作区安全升级」能力 |
| 取代关系 | 024 早期设想的 `.specify/version` 标记、版本→迁移注册表、`specify upgrade` 命令由本规格的「声明驱动期望态 + 一次直达」取代（requirements FR-005、FR-020）；024 详情已在本阶段同步改写 Key Changes / Implementation Notes |

## 本计划如何映射到该 Feature

- **能力域对齐**：Feature 024 的目标是「项目跨 CLI 发布安全升级 `.specify/` 工作区」；本计划的 `specify migrate` 即该能力的唯一用户面向入口。
- **不新增 Feature**：本计划不引入新特性、不弃用/合并既有 Feature；功能/非功能分类不变（功能类：用户可用 CLI 面）。
- **注册表动作（本阶段已完成）**：`features.md` 的 024 行 Status `Draft → Planned`、Spec Path 指向本规格、Last Updated 更新；024 详情 Status 与 Key Changes 同步。requirements 阶段遗留的「registry 集成待办恢复点」在本阶段关闭。
- **后续状态归属**：`Planned → Implemented` 由 `/speckit.implement` 推进；本计划不越权。

## FR → WP 矩阵（供 `/speckit.tasks` 切分与覆盖核对）

| FR | 覆盖 WP | 关键落点 |
|----|---------|----------|
| FR-001 命令面/默认干跑/拒绝未声明选项 | WP01 | `contracts/migrate-cli.md` C-1/C-6 |
| FR-002 模板薄投影/两入口同计划 | WP08, WP14 | `contracts/migrate-template.md` T-2/T-3 |
| FR-003 前置条件拒绝并指向 init | WP01 | `contracts/migrate-cli.md` C-2 |
| FR-004 不承担 install/init | WP01 | `contracts/migrate-cli.md` C-2；plan Summary |
| FR-005 期望态来源与读取入口 | WP02, WP03 | `contracts/migrate-engine.md` C-2；`research.md` R-2/R-3/R-6 |
| FR-006 只读、确定性、逐项字段 | WP01, WP03 | `contracts/migrate-cli.md` C-4；`data-model.md` E-1/E-2 |
| FR-007 五维覆盖 | WP03 | `contracts/migrate-engine.md` C-1；`data-model.md` E-8 |
| FR-008 无假绿/可转红 | WP03, WP12, WP13 | `contracts/migrate-engine.md` C-8；WP12 收敛读数 + WP13 逐维度变异断言 |
| FR-009 init 迁移分支复用/等价性 | WP07 | `contracts/migrate-engine.md` C-5 |
| FR-010 sanitize 检查器只读消费 | WP03 | `contracts/migrate-engine.md` C-2/C-5 |
| FR-011 锚点布局引擎唯一承载 | WP03, WP05 | `contracts/migrate-engine.md` C-2/C-3 |
| FR-012 migrate/sanitize 职责边界 | WP09 | `contracts/migrate-engine.md` C-5；`skills/internal/sanitize-materials/SKILL.md` |
| FR-013 goal/team 迁移静止指针 | WP03 | `data-model.md` E-9 |
| FR-014 六值处置封闭集 | WP04 | `contracts/migrate-engine.md` C-3；`data-model.md` E-1 |
| FR-015 双键确认/非交互 blocked/无确认旗标 | WP04 | `contracts/migrate-cli.md` C-5；`contracts/migrate-engine.md` C-6 |
| FR-016 用户内容保护/archive-not-delete | WP04, WP05 | `contracts/migrate-engine.md` C-3/C-6 |
| FR-017 幂等与续跑/无全局回滚 | WP05, WP06 | `contracts/migrate-engine.md` C-7 |
| FR-018 回执逐运行一文一件与恢复路径 | WP06, WP10 | `data-model.md` E-3/E-4；目录登记 |
| FR-019 四类结局与稳定退出码 | WP01 | `contracts/migrate-cli.md` C-3；`data-model.md` E-5 |
| FR-020 跨版本一次直达/源版本只记录 | WP02, WP06 | `data-model.md` E-3 source 字段；`research.md` R-5 |
| FR-021 既有装配面分发 | WP08 | `contracts/migrate-template.md` T-4 |
| FR-022 接口契约（CLI/模板 frontmatter） | WP01, WP08 | `contracts/migrate-cli.md` C-6；`contracts/migrate-template.md` T-1 |
| FR-023 三类夹具由声明生成 | WP11 | `contracts/migrate-engine.md` C-8 |
| FR-024 安全取证可转红 | WP13 | `contracts/migrate-engine.md` C-6/C-8 |
| FR-025 等价/幂等/续跑取证可转红 | WP12, WP14 | `contracts/migrate-engine.md` C-5/C-7；`contracts/migrate-template.md` T-3 |

覆盖核对：25/25 FR 均有 WP 与契约落点；无 FR 落在计划外。
