# Data Model: 确认门控精简(Feature 046)

本 Feature 无持久化存储;实体为判据概念、扫描输出 schema 与报告结构。校验规则均溯源自 requirements.md 的 FR。

## Entity 1: Confirmation Gate(确认门控记录)

扫描脚本对每个检出的阻塞确认指令产出一条记录。

| 字段 | 语义 | 校验规则 |
|------|------|----------|
| `id` | 门控唯一标识 | 形如 `gate-<nnn>`,扫描内唯一 |
| `file` | 源文件相对路径 | MUST 位于扫描根(templates/commands/、skills/、shared/、templates/*.md)内 |
| `line` | 行号 | 正整数 |
| `trigger` | 触发场景摘要 | 非空,≤120 字符 |
| `action_class` | 所保护动作的归类 | 枚举:`destructive` / `reversible` / `governance_kept` / `intrinsic`(FR-001、FR-002、D2) |
| `verdict` | 治理裁定 | 枚举:`keep_gate` / `auto_execute`;`destructive`/`governance_kept`/`intrinsic` → `keep_gate`,`reversible` → `auto_execute`(FR-007) |
| `evidence` | 判据依据引用 | 指向判据文档条目或保护清单行 |

**状态迁移**: `unclassified` →(判据归类)→ `keep_gate` | `auto_execute` →(实现完成)→ `remediated`。存疑记录 MUST 落 `destructive`(存疑从严,FR-002)。

## Entity 2: Confirmation Taxonomy(确认分类判据)

判据真源(shared/guidelines/confirmation-gates.md)的结构约束。

| 组成 | 语义 | 校验规则 |
|------|------|----------|
| 两级判据 | 破坏性/不可撤销 → 前置确认;可逆 → 自动执行 | MUST 与 FR-001 逐字一致 |
| 破坏性动作清单 | 保守可枚举 | MUST 至少含:删除文件或数据、移动/归档既有工件、远程推送、覆盖用户既有内容(FR-002) |
| 治理保留清单 | 凭清单保留的门控(不依赖可逆性推断) | MUST 枚举:访谈退出门、宪章不可撤销确认、git commit 显式批准、implement gate.yaml CONFIRM、git-workflow 远程操作门控、tools invoke 预览门控(D2、FR-011) |
| 存疑从严规则 | 无法归类时按破坏性处理 | MUST 存在且可被扫描脚本引用(FR-002) |
| 回流约束 | 新增/修订命令与技能不得引入非破坏性阻塞门控 | MUST 存在(FR-003) |

## Entity 3: Execution Report(执行报告)

自动执行动作完成后的呈现结构。

| 要素 | 语义 | 校验规则 |
|------|------|----------|
| 执行内容 | 做了什么 | 三要素缺一不可(FR-009) |
| 产出/变更工件 | 落盘或变更的对象列表 | 逐项列明,可定位 |
| 修改途径 | 如何修改/撤销 | 指向既有修订命令或编辑入口(FR-009) |

**粒度规则**: 单个琐碎动作并入所属流程收尾报告逐项列明;仅流程主要产出动作独立出完整报告(FR-009 豁免)。同流程多动作合并为一次收尾呈现(Edge Case)。失败时附中间产物如实报告(FR-010)。

## Entity 4: Gate Scan Report(扫描汇总)

扫描脚本的聚合输出(SC-002/SC-005 度量面)。

| 字段 | 语义 | 校验规则 |
|------|------|----------|
| `total` | 检出阻塞门控总数 | 非负整数 |
| `by_class` | 按 action_class 计数 | 各键之和 = total |
| `by_verdict` | 按 verdict 计数 | 各键之和 = total |
| `baseline_delta` | 与基线快照的差值 | 提供 `--baseline` 时 MUST 输出;无基线时为 null |
| `violations` | verdict=auto_execute 但仍以阻塞形态存在的门控列表 | 治理完成后 MUST 为空(SC-002 残留口径) |

**关系**: Gate Scan Report 1 — N Confirmation Gate;Confirmation Taxonomy 约束全部 Confirmation Gate 的归类;Execution Report 是 verdict=auto_execute 门控移除后的替代呈现机制。
