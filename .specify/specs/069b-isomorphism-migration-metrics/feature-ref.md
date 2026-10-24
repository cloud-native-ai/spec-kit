# Feature Reference — Feature 069 / Slice 069b

**Date**: 2026-10-25 · **Requirements**: [requirements.md](requirements.md) · **Plan**: [plan.md](plan.md)
**Bound feature**: Feature 069 `执行/表达二元分类与文档型 SDD 同构`（复用 `clarify` 2026-10-24 的既有绑定；不新建 Feature ID、不新增注册行）
**Slice**: `069b-isomorphism-migration-metrics`（Feature 069 的第二个切片）

## 1. FR → 设计落点 → 契约 → 测试

切片本地编号 FR-001…FR-014；父映射见 `notes/parent-fr-mapping.md`。`FR` 一列只写切片本地 ID。

| FR | 主题 | 设计落点 | 契约条款 | 测试面 |
|----|------|----------|----------|--------|
| FR-001 | 同构映射 8 行 × 3 面，名册引用 owner，载体唯一 | owner 文档 § 同构映射；`--action isomorphism`；阶段名册 = `loop-state.py` `STAGE_ARTIFACTS` | `isomorphism-map.md` C-1 / C-2 / C-3 / C-13 | `test_isomorphism_map.py`（表形/行集/24 格/载体唯一） |
| FR-002 | 行级强制标注，标注失真即缺陷 | `强制门禁` + `强制状态` 两列；`(stage, face)` blocking 存在性比对 | `isomorphism-map.md` C-4 / C-5 / C-6 / C-7 | `test_isomorphism_map.py`（正反两侧 + 失真注入） |
| FR-003 | 四类不可同构边界，每条绑定门禁 | owner 文档 § 不可同构边界（4 行表） | `isomorphism-map.md` C-8 / C-9 | `test_isomorphism_map.py`（缺行/无面 id/拆分） |
| FR-004 | 禁止整套移植；跨类只复用不变量 | 算子表代码型算子闭集扫描 + 评审面判定 | `isomorphism-map.md` C-11 | `test_isomorphism_map.py`（闭集命中） |
| FR-005 | 同构主张必须落地 | 格语法 + 许可句闭集 + 评审面 | `isomorphism-map.md` C-7 / C-10 / C-12 | `test_isomorphism_map.py`（口号行 + 介质判据短语） |
| FR-006 | 未刷新行为不变；刷新自动获得 | 零新调用点；单包原子性 | `migration-distribution.md` C-1 / C-2 / C-3 / C-8 | `test_migration_distribution.py`（调用点零新增/载荷清单） |
| FR-007 | 名字级基线零新增失败 | 三快照 + `--names-out` + `comm -13` | `migration-distribution.md` C-6 / C-7 / C-9 | `test_migration_distribution.py`（样本记录与判据形态） |
| FR-008 | 分发走既有路径；零项目侧存储/读取点 | `pyproject.toml` force-include + `init` shared 拷贝 + `hatch_build` | `migration-distribution.md` C-4 / C-5 / C-10 / C-11 | `test_migration_distribution.py`（零新路径/零模板改动） |
| FR-009 | 所有者唯一、键 `flow_class`、映射归该所有者 | owner 开篇 owns 列表 + 表头 | `ledger-reconciler.md` C-5 / C-6 | `test_ledger_reconciliation.py`（表头/版本声明） |
| FR-010 | 声明式行集；反空真下限 + 覆盖率断言 | `check` 扩展：`ledger-truncated` / `coverage` / `red_kind` | `ledger-reconciler.md` C-1 / C-2 / C-3 / C-4 / C-14 | `test_ledger_reconciliation.py`（双注入 + 覆盖率算术） |
| FR-011 | 混合 oracle 一律 `execution` 并叠加 | 台账一致性检查 `mixed-oracle-class` | `ledger-reconciler.md` C-7 | `test_ledger_reconciliation.py`（反例注入） |
| FR-012 | 委托关系机械核验；类中立封闭 | `--action delegation`；模板路径解析 + 清单豁免 | `ledger-reconciler.md` C-8 / C-9 / C-10 | `test_delegation_classes.py`（全绿 + 改类转红） |
| FR-013 | 六面各一个 owner 指针；判据不搬家 | `--action faces` + duplicate 面（封闭主体集） | `ledger-reconciler.md` C-11 / C-12 / C-13 | `test_expression_faces.py`（6/6、锚解析、副本 0） |
| FR-014 | 三项基线同口径同仪器；无样本 `not-evaluated` | 四通道 + `notes/expression-baseline.md` | `measurement-instruments.md` C-1…C-10 | `test_measurement_instruments.py`（记录形态/词表边界/无新采集器） |

**覆盖核对**：14 条 FR 全部出现在至少一个契约条款的引用组内（`account-clause-coverage.py` 的 FR lane 期望 0 uncovered）；
14 条都在上表有落点与测试面。没有「只写进 plan、不进契约、不进测试」的 FR。

## 2. SC → 测量源 → 判据形态

| SC | 判据 | 测量源 | 契约 |
|----|------|--------|------|
| SC-001 | 未标注行 = 0；四类边界齐全且每条可指认门禁处理 | `--action isomorphism` findings=0 + 两表逐行核对记录 | C-2…C-9 |
| SC-002 | 3 个客户快照上名字级新增失败 = 0 | `notes/migration-samples.md` 冻结样本 + 前后 `--names-out` + `comm -13` | C-6 / C-7 / C-8 |
| SC-003 | 双注入各自转红且两红可区分；静默绿 = 0 | `--action check` 两次注入的 `red_kind` + 退出码 | C-1 / C-2 / C-3 |
| SC-004 | 混合 oracle 样本一致率 100%、全落 `execution`；择优 = 0 | 两份互不可见判定记录 + 台账 `basis/flow_class` 一致性 | C-7 |
| SC-005 | 六面 owner 指针 6/6；判据正文在 owner 之外出现 0 次 | `--action faces` + duplicate 面（封闭主体集） | C-11 / C-12 / C-13 |

**口径提醒**：SC-002 的对象是**客户项目快照**，不是框架仓的 `notes/test-baseline-contract.txt`（后者是 FR-007 的框架侧分母，
两者不可互相顶替）。SC-005 的「0 次」是**封闭主体集**上的计数，不是全仓 grep（见 C-13）。
SC-004 的两名判定者是**人工并列证据**：未执行时记 `not-evaluated` + reason，机器侧只保证台账一致性与落类分布。

## 3. 与 069a 的接口（只引用，不复制）

| 069a 已交付物 | 本切片如何使用 |
|----------------|----------------|
| `shared/definitions/flow-class-definitions.md` 的判据 / 两取值 / 台账 / 类中立清单 | 只读与增量：本切片在该文档新增两个章节、一处版本声明、四行指针收敛（P1–P4） |
| `shared/workflow/expression-gates.md` 的六面表 / 阶段算子表 / 调用点表 | 只读：映射的强制声明与 faces 检查都以它为 owner；**本切片不改该文件** |
| `scripts/python/flow-class-check.py` 的 `check` / `lookup` | 扩展 `check`（增量字段与新 kind），`lookup` 零改动 |
| 069a 的 4 份契约与 8 个测试文件 | 不修改；本切片新增 4 份契约与 8 个测试，并保持既有测试绿 |
| 069a 的 `notes/expression-baseline.md` | 只作同口径先例，**不当本片前值** |

## 4. 测试映射（新增 8 个文件）

| 文件 | 断言面 | 对应契约 |
|------|--------|----------|
| `tests/contract/test_isomorphism_map.py` | 表形/行集/24 格格语法；强制标注真实性（正反）；四类边界；口号行；介质判据短语；载体唯一（无第二份映射） | `isomorphism-map.md` C-1…C-12 |
| `tests/contract/test_ledger_reconciliation.py` | `ledger-truncated` floor；`coverage` 算术；`red_kind` 优先级；双注入两种红可区分；`mixed-oracle-class`；`ledger-version-missing` | `ledger-reconciler.md` C-1…C-7 |
| `tests/contract/test_delegation_classes.py` | 27 模板解析、类一致全绿、改类转红、类中立豁免仍绿、无人工清单 | `ledger-reconciler.md` C-8 / C-9 / C-10 |
| `tests/contract/test_expression_faces.py` | 6 行、face id 唯一、指针可解析（含 `§` 锚）、第二绑定表检测、duplicate 面 findings = 0 | `ledger-reconciler.md` C-11 / C-12 / C-13 |
| `tests/contract/test_migration_distribution.py` | 新动作零调用点；`templates/`/`skills/` 零改动；`pyproject` 与 `init` 分发路径在场；样本记录形态；零项目侧存储 | `migration-distribution.md` C-1…C-11 |
| `tests/contract/test_measurement_instruments.py` | 基线记录字段与 `not-evaluated`；四通道命令存在；无新采集器；`verification.md` 词表不变 | `measurement-instruments.md` C-1…C-10 |
| `tests/unit/test_isomorphism_checker.py` | 名册解析、格语法边界、blocking 集合计算、`framework-source-required` 分支 | 同上两份契约的实现细则 |
| `tests/unit/test_reconciler_extensions.py` | `red_kind` 优先级、coverage 数学、delegation 语法与去重、faces 指针拆分 | 同上 |

**红先纪律**：8 个测试文件在实现前必须先红；红的形态 MUST 是「引擎缺该动作 / 缺该章节」，MUST NOT 是 import 或 collection error。

## 5. Feature list review（本阶段只复核，不推进父状态）

- **新增 Feature**：无。本切片复用 Feature 069 的既有绑定。
- **废弃 / 合并 Feature**：无。
- **状态**：Feature 069 行保持 **`Planned`**（`069a = Implemented` / `069b = plan 已落盘`）。本阶段 MUST NOT 写 `Implemented`。
- **登记更新**：`.specify/memory/features/069.md` § Related Specifications 追加本切片 plan 产物清单；
  § Status Tracking 追加「069b plan landed · 2026-10-25」一行。`features.md` 的 069 行只更新 Last Updated 单元格（不改状态列）。
- **分类一致性**：069 为 functional / 框架治理类（与既有登记一致），本切片不改变分类。

## 6. 与父规格的关系

父规格的 41 条 FR 与 13 条 SC 的编号与语义不变；本切片是投影（`notes/parent-fr-mapping.md`）。
父已回写的 069a 规则不被本切片改写；本切片只闭合 069a 留下的三处交接（映射章节、项目侧声明措辞、字面量指针），
并在 069a review 的 REC-069a-06 上只闭合**判据侧**（FR-010 / SC-003），形态取值按 SA-11 在 plan 中裁定（R11）。
