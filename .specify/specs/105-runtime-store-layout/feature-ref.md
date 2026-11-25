# Feature Reference — 105 → Feature 024

**Spec**: `requirements.md` · **Plan**: `plan.md` · **Date**: 2026-11-25

## 绑定

| 项 | 值 |
|----|-----|
| Feature ID | 024 |
| Feature Name | Specification Workspace Versioning |
| Feature Detail | `.specify/features/024-specification-workspace-versioning.md` |
| Index Row | `.specify/features.md` 行 105（本阶段由 `Draft` 推进为 **Planned**）；父行 024 保持 `Ready for Review` |
| 本规格身份 | Feature 024 的第二个子规格；第一个为 097（`/speckit.migrate` 一次性迁移收尾）。本规格把「跨 CLI 版本的工作区安全升级」从结构面扩展到**运行期存储布局** |
| 关系 | 复用 097 的 plan → apply → archive-first → 回执结构，追加第六维 `store-layout`；097 的 dated 记录不改写，本规格的动作为其封闭维度集的受控扩展（plan T-001） |
| 不新增 Feature | 不引入新特性、不弃用/合并既有 Feature；功能/非功能分类不变（功能类：工作区布局与其升级路径） |
| 后续状态归属 | `Planned → Implemented` 由 `/speckit.implement` 推进；本计划不越权 |

## 本计划如何映射到该 Feature

- Feature 024 的能力是「项目跨 CLI 发布安全升级 `.specify/` 工作区」；105 把存储布局纳入同一升级面：新布局由 init 播种、旧数据由 `specify migrate` 搬迁/拒绝、完成状态由现场事实判定。
- 097 的 `specify migrate` 是唯一数据搬迁执行者（FR-013 的 clarify 裁定）；本计划不新增迁移命令、不建第二迁移引擎。
- 本阶段登记动作：`features.md` 行 105 `Draft → Planned`、Last Updated 更新；024 详情追加 plan 记录，父行状态不变。

## FR → WP 矩阵（供 `/speckit.tasks` 切分与覆盖核对）

| FR | 覆盖 WP | 关键落点 |
|----|---------|----------|
| FR-001 封闭清点与基线参照 | WP01, WP12 | `contracts/store-layout.contract.md` C-1/C-6；`data-model.md` E-2/E-10 |
| FR-002 四个具名存储迁顶层 | WP01, WP07, WP08 | C-1；`migrate-store-layout.contract.md` M-2 |
| FR-003 其余存储同名迁移 + tools 域 + draft 退役 | WP01, WP04, WP07 | C-1/C-4；M-2 |
| FR-004 容器退役与墓碑 | WP01, WP08, WP10 | C-2/C-5；M-4 |
| FR-005 唯一 owner 与登记 | WP01, WP10 | C-3/C-5；E-1 |
| FR-006 记忆两层与动作契约不变 | WP03, WP12 | `memory-and-injection.contract.md` P-1；E-7 |
| FR-007 临时记忆持久化 | WP03, WP12 | P-2 |
| FR-008 记忆检索边界 | WP03, WP12 | P-1/P-5 |
| FR-009 memory 仅系统名 | WP03, WP10 | C-5；P-1 |
| FR-010 注入载荷不变 | WP03, WP12 | P-3；E-8 |
| FR-011 注入引用新路径 | WP03, WP10, WP12 | P-3 |
| FR-012 无第二注入机制 | WP03, WP12 | P-4 |
| FR-013 一次性迁移与执行者裁定 | WP07, WP09 | M-1/M-7 |
| FR-014 archive-first 与恢复 | WP08 | M-4/M-6 |
| FR-015 并存拒绝/未知残留/生成物口径 | WP07, WP08, WP13 | M-2/M-3/M-5；M-8 |
| FR-016 完成后不重建/确定性拒绝 | WP08, WP14 | M-4/M-6/M-7 |
| FR-017 全新初始化新布局 | WP05 | C-7 |
| FR-018 活路径常量全覆盖 | WP02, WP10 | C-6；`live-reference-migration.contract.md` L-1/L-3 |
| FR-019 安装器/升级面 | WP05 | C-7 |
| FR-020 忽略规则同变更 | WP06 | C-4 |
| FR-021 目录登记与文档活引用 | WP01, WP10 | C-5；L-7 |
| FR-022 镜像与副本再生成 | WP11 | L-6 |
| FR-023 dated record 不改写 | WP10, WP11 | L-4 |
| FR-024 契约测试集 | WP12, WP13 | M-8；L-5/L-8 |
| FR-025 并发写安全 | WP02, WP12 | E-1/I-10；M-4 |
| FR-026 行为保持留证 | WP12, WP14, WP15 | P-5；L-8 |
| FR-027 不兼容变更迁移闭包 | WP12, WP15 | `migrate-store-layout.contract.md` M-10；plan § Backward-Incompatible Change Inventory（BC01…BC18） |

覆盖核对：27/27 FR 均有 WP 与契约落点；无 FR 落在计划外。

## SC → 证据矩阵

| SC | 路径 | 证据来源 | WP |
|----|------|----------|-----|
| SC-001 清点封闭 + 旧根退役 | final | `test_runtime_store_layout.py::test_inventory_is_closed` + 基线 `git ls-tree` + 迁移后 `test ! -d` | WP12/WP14 |
| SC-002 记忆行为保持 | final | `test_memory_preservation.py`（record/recall/prune/reindex + run-determination） | WP03/WP12 |
| SC-003 注入行为保持 | final | `test_dispatch_injection_paths.py`（载荷字段 + 来源路径 + 反向夹具） | WP03/WP12 |
| SC-004 迁移安全三形态 | final | `test_store_layout_migration_us1_us2.py`（byte 比较/拒绝/幂等） | WP07/WP08/WP13 |
| SC-005 全新初始化 | final | `test_init_new_layout.py`（树清单/无旧根） | WP05/WP12 |
| SC-006 活引用面零旧路径 | supporting | `test_store_layout_live_refs.py`（允许集双向相等 + 变异转红） | WP10/WP12 |
| SC-007 镜像与副本 | supporting | `sync-mirrors.py --check` + `regen --check` + member-set 基线对比 | WP11/WP14 |
| SC-008 忽略与跟踪 | supporting | `test_tools_domain.py` + `test_specify_gitignore_template.py` + `git check-ignore` 夹具 | WP06/WP12 |
| SC-009 不兼容变更闭包 | final | `test_runtime_store_layout.py::test_backward_incompatible_inventory_is_closed` + M-8 夹具的 dry-run/apply 读数 + `acceptance-105.md` SC-009 行 | WP12/WP15 |

**Failed final-path criteria block the status flip**; supporting criteria are reported with their measured baseline (plan T-003 for SC-007's absolute reading).

## 依赖与边界

- 依赖 097 的 `specify migrate` 已落地（Ready for Review，无 deferred/blocked 记录；见 `plan.md` § Inherited Blockers）。
- 本规格不改写 097 的 dated 记录；扩展关系记录在本计划 T-001 与本规格契约 M-1。
- 不依赖 055（只复用逐条一文件协议，不改）、015（命令面本身）。

## Overlap Adjudication — 2026-11-25 (driver U4)

**Trigger**: `overlap-check.py --spec-dir .specify/specs/105-runtime-store-layout --repo <repo>` returned `overlap` (87 specs checked; 52 path relations on the plan fallback declaration, 34 on the final `feature-ref.md` declaration recorded at `test-evidence/overlap-plan.json`). The clarify-time check was vacuous because no declaration artifact existed before plan; this adjudication is recorded before tasks dispatch.

**Ownership ruling**: this is a time-sliced, non-concurrent ownership decision. No other line has a live executor writing these paths during this run. Feature 105 is the sole writer for the migration edits; prior features retain ownership of their already-delivered behavior and their dated records are not rewritten. No prior scope is removed or narrowed.

| Current delivery path | Current-write owner | Historical owner / boundary |
|---|---|---|
| `src/specify_cli/__init__.py` (and the directory declaration in plan) | Feature 105 for the `store-layout` migration dimension and seed/init path changes | the CLI command families that already own their behavior; 105 MUST NOT change their contracts |
| `.specify/shared/guidelines/decision-tension.md` | Feature 105 only for the live path references in this migration | the decision-tension contract remains owned by Feature 076 |
| `agents/sdd-debt-governor.agent.md` | Feature 105 only for its read-scope path reference | the debt-governor capability remains owned by Feature 103 |
| `docs/concepts/documentation-model.md` | Feature 105 only for the live path references | the documentation model remains owned by the docs/SDD documentation line |
| `docs/reference/commands/migrate.md` | Feature 105 for the store-layout dimension and receipt wording | the base `specify migrate` command remains owned by Feature 097 / parent Feature 024 |
| Parent Feature 024 / 097 shared migration surface | Feature 105 for the new sixth `store-layout` dimension | Feature 097 owns the existing plan → apply → archive-first → receipt mechanism; 105 reuses it without replacing it |

**Checker limitation**: `overlap-check.py` compares the current declaration against the *historical delivered file set* of every sibling spec. For a migration that intentionally touches the CLI and live docs, historical completed features therefore remain in the overlap set by construction. The decision above is the required ownership adjudication; the engine cannot return `clear` without either falsifying the delivery surface or deleting historical ownership, both of which are forbidden. This is recorded as a named residual (`overlap=52, historical/non-concurrent`) in the line state spine, not silently treated as a clear gate.

**No second writer**: the overlap check's other specs are completed/Ready historical specifications; only this line has a live executor. If a future concurrent line activates, this adjudication MUST be revisited before implementation writes resume.
