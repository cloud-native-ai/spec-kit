# Contract — Status `Sealed` 与归档准入

**Feature**: 099-speckit-seal | **Date**: 2026-11-10 | **Plan**: [plan.md](../plan.md)
**Owns**: 状态值域的唯一扩展、carrier 同步义务、终态与审计更正、`Completed` 的遗留地位、漂移守卫、
归档准入的唯一实现点与 `state-drift` 语义。

**C-024** — 值域恰好 +1，转移恰好 +1，owner 命令唯一。

特性状态值域 MUST 恰好新增一个值 `Sealed`（STR-001），并新增恰好一条转移 `Ready for Review → Sealed`；
`/speckit.seal` 是该转移的唯一 owner 命令。MUST NOT 新增第二套状态机或第二份值域。

(FR-001)

**C-025** — schema owner 唯一，carrier 同批投影，消费面由静态检索派生。

值域与转移的 schema owner MUST 是 `shared/workflow/acceptance-hardening.md` § Feature Status。声明式
carrier（`templates/feature-details-template.md` § Canonical Status State Machine 与
`[FEATURE_STATUS]` 词汇行、`templates/feature-index-template.md` 的状态值域、
`shared/workflow/feature-integration.md` § Status State Machine、`skills/internal/manage-features/SKILL.md`
的状态词表）与机器消费面（`shared/definitions/non-disposable-definitions.md` 的状态域行、
`scripts/python/non-disposable-check.py` 的状态×裁决表、
`scripts/python/closure-acceptance-check.py` 的 completion-claim 家族）MUST 在同一次变更内识别 `Sealed`。
消费面集合 MUST 由静态检索派生（`grep` 证据入 `test-evidence/`），MUST NOT 由手写清单维持。

(FR-001)

**C-026** — 终态语义与唯一后向转移。

`Sealed` MUST 是终态：不存在离开它的前向转移。唯一合法的后向转移 MUST 是审计更正
`Sealed → Ready for Review`，且 MUST 携带使原封装结论不成立的证据、同时落在注册表行与特性详情两处载体上；
其余后向转移 MUST 判为非法。该例外与既有 `Implemented → Blocked` 审计更正同形，MUST NOT 扩大为一般回退通道。

(FR-002)

**C-027** — `Ready for Review → Completed` 对新工作关闭；叙述面同批收敛。

既有 `Ready for Review → Completed` 出口 MUST 对新工作关闭：该转移不再产生新的 `Completed` 行；新工作 MUST NOT 落 `Completed`。`Completed`
仅作为遗留记录值保留于本特性落地之前的行（不追溯改写、不降级、不重判）；所有陈述「终态」的面向新工作的表述
MUST 说 `Sealed`。宪法生命周期叙述与模板副本 MUST 在同次变更内收敛（叙述面以 schema owner 为准；
先例：`Blocked` 进入 status 面时叙述未被逐字展开，本次因 FR-003 明示要求收敛而展开）。`Completed` 行
MUST NOT 自动获得归档准入（见 C-030）。

(FR-003)

**C-028** — 状态写入只落既有面。

`seal` 的状态写入 MUST 只落：注册表行 `Status` 与 `Last Updated`、特性详情 `Status` 与 `## Latest Review`
记录、以及 `seal.md`（STR-002）。MUST NOT 新增注册表、台账、队列或状态脊；MUST NOT 移动或删除 spec 目录。

(FR-004)

**C-029** — 漂移守卫：移除即红、点名到面。

任一 carrier 或消费面移除 `Sealed` 时，漂移守卫契约测试 MUST 转红并点名该 surface。守卫集至少覆盖：
模板转移表状态集、模板 `[FEATURE_STATUS]` 行、索引模板词汇行、feature-integration 协议行、manage-features
词表、non-disposable 状态表、closure completion-claim 家族。既有两处以「恰六值」编码的 pin（`test_status_gate_owner.py`、`test_acceptance_state_machine.py`）
MUST 在同一次变更内更新为「恰七值」；`test_acceptance_schema_ownership.py` 不编码六值字面量，但其
「每个投影落在域内」断言 MUST 在七值域下保持转绿——MUST NOT 为让它变绿而放宽或删除断言。

(FR-001, SC-008)

**C-030** — 归档准入只有一个 owner；非 `Sealed` 一律拒绝并指回 `/speckit.seal`。

任何会退休/归档 spec 或把特性行标为归档指针的流程，MUST 在动手前通过 `seal-utils.py --action archive-gate`
查询准入：允许 `0` / 拒绝 `1` 并具名理由 / 输入错误 `2`。非 `Sealed` MUST 被拒绝并指向 `/speckit.seal`；
遗留 `Completed` 行不可由 seal 处置（FR-005 不接受其为 from 状态），其归档 MUST 携带按 C-044 字面
形态记录的用户显式裁定，否则同样拒绝。准入判据 MUST 只在本引擎实现；
消费方按指针查询，MUST NOT 各自实现第二份判定——把判据复制到第二处时守卫测试 MUST 转红。

(FR-022, FR-023)

**C-031** — `state-drift` 以输入错误结束，不择一采信。

注册表行与特性详情的状态不一致，或任一载体缺失时，`seal`（及 `archive-gate`）MUST 以 `state-drift` 具名
拒绝并以退出码 `2` 结束，MUST NOT 择一采信任一载体；修复归 `/speckit.feature` 的既有 reconcile，引擎
MUST NOT 自行改写状态去消除漂移。读取口径 MUST 与闭包引擎 `resolve_claimed_status` 同源：只读详情
`**Status**` 行与注册表 `Status` 列；spec 文档内其它 `**Status**` 行（如 `requirements.md` 的 Draft）
不参与判定。

(FR-005, SC-002)
