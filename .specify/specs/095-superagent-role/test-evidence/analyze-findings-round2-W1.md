# Analyze Findings — Round 2, W1（requirements × requirements-quality checklist）

- **Unit**: `/speckit.analyze`（round-2 并发波 Worker W1）· **Run**: `r20261110T055657Z-b095-r2w1`（线 run `r20261110T055657Z-b095`）· **Stage**: analyze round 2 · **Date**: 2026-11-10
- **Read domain（文件级、互斥）**: `.specify/specs/095-superagent-role/requirements.md`、`.specify/specs/095-superagent-role/checklists/requirements-quality-2026-11-10.md`
- **Governance inputs read（非 spec 制品）**: `.specify/constitution.md`；`analyze-artifacts` SKILL 与 `references/detection-and-severity.md`、`references/validation-and-report.md`；`.specify/features.md`（095 行与总数）、`.specify/features/095-superagent-role.md`（registry pass）；`feature-integration.md`、`one-source-of-truth.md`、`closed-set-claims.md`；上轮 `analyze-findings-W1.md`、`analyze-merged-2026-11-10.md`、`analyze-repair-dispositions-2026-11-10.md`（rerun delta 与 residue 输入）；`.specify/state/095-superagent-role.md`（run 标识与阶段状态）。
- **Not read（按读域隔离）**: `plan.md`、`tasks.md`、`data-model.md`、`contracts/`、`quickstart.md`、`feature-ref.md`、其他 Worker 的 round-2 findings。因此 **pass E（task 覆盖）与 pass I（decision tension）不由 W1 裁决**；clause/FR coverage accountant 归集成者第 3 步，未由 W1 运行。
- **只读声明**: 未修改任何制品；本文件是唯一产物写面。除本文件外只执行 wrap-up 记账三引擎（Run Determination / Exec Quant / Feedback Record），不提交、不 push。
- **same-author**: 制品由本线前序阶段代理撰写；W1 是 analyze 波派发的 fresh-context 只读检测者（same-author gate 的委派载体），未参与撰写。
- **Flow class（阶段简报给定）**: `execution` / `source: declaration` / marker `-` / error `-`；W1 本阶段未新增 flow-class 引擎读取。
- **Round-2 口径**: 重裁上轮 W1 的 29 条 findings（8 fixed / 1 partially-fixed / 20 deferred）并做全严重度重扫；开放 MEDIUM/LOW 逐条登记为 residue；checklist pass H 重新问责 39 条。
- **锚点前缀**: `REQ:` = `requirements.md`（行号按本轮实读）；`CHK:` = `checklists/requirements-quality-2026-11-10.md`；`FEAT:` = `.specify/features/095-superagent-role.md`；`CONST:` = `.specify/constitution.md`。

## 裁决摘要

- **26 条当前 findings**：**3 HIGH / 20 MEDIUM / 3 LOW / 0 CRITICAL**。3 条 HIGH（W1-30 / W1-31 / W1-32）为本轮提案，须经集成者独立验证波确认；MEDIUM/LOW 跳过验证。
- **上轮 delta**：8 条完全关闭（W1-01/02/03/05/06/11/24/27），1 条部分关闭（W1-04 → 残留重报为 W1-32），20 条维持（deferred）。
- **门禁含义**：W1 读域内两处上轮 CRITICAL 已核验关闭；但仍有 3 条 HIGH 提案与 20 条 deferred MEDIUM。**本证据不支持在验证波与跨 Worker 合并前宣称 analyze 门通过**。

## Findings（当前开放集）

| ID | Status | Severity | Propagation surface | Category | Anchor(s) | 一句话事实 | 建议归属（指针） |
|----|--------|----------|---------------------|----------|-----------|------------|------------------|
| W1-30 | new（W2-02 修复残留） | **HIGH** | `role-edge` 契约 + SC-001 角色集输出 | Inconsistency / Ambiguity | REQ:125、128、197、210、239 | 同一机读字面量 `dual-role` 同时被定义为「双角色集合标记」（STR-002 / Key Entities / SC-001）与「已授予派发职责的声明值」（FR-005），且 FR-005 用字面量而非 [[STR-002]]；契约无法仅凭 token 判别语义。 | `/speckit.requirements`：FR-005 / Shared Strings / Key Entities |
| W1-31 | new（X-01 同根残留） | **HIGH** | implement 完成门（SC-009 → verification.log） | Inconsistency / containment claim | REQ:177、218 | SC-009 要求四类既有治理契约测试「全绿」，而 FR-036 把完成门判据定义为相对 implement 起点基线的零新增失败并豁免基线既有红；若基线含这四类测试的既有红，两条判据不可同时满足。 | `/speckit.requirements`：SC-009（对齐 FR-036 或点名基线绿证据） |
| W1-32 | residual of W1-04 | **HIGH** | SC-001 测量源 → test-evidence 夹具 | Inconsistency / Coverage | REQ:29、39、128、210、223 | W1-04 修复未扫到测量源与故事叙述：SC-001 Source 仍写「违例三类」，US1 故事只列三类示例，与 FR-005 / US1 AS3 / SC-001 的四类违例矛盾。 | `/speckit.requirements`：SC-001 Source + US1 叙述 |
| W1-33 | new（CHK016 残留） | MEDIUM | 等待 / 恢复契约（FR-012） | Gap / Traceability | REQ:138；CHK:35 | FR-012 要求按「既有阈值」区分 slow / stalled，但全篇未给出该阈值或分类的 owner 路径（FR-013 的 attribution owner 已在 W1-01 修复中补上）。 | `/speckit.requirements`：FR-012 补 owner 路径（或 plan/contract） |
| W1-34 | new | MEDIUM | SC-002 上行回传断言 | Inconsistency / Coverage | REQ:148、211、224 | SC-002 只断言双重角色上行回传的三个要素，而其测量源写「四项断言」、FR-019 定义四项（含边界与异常停止）；缺项可能在测试中被漏掉或被源清单补回。 | `/speckit.requirements`：SC-002 / SC-002 Source |
| W1-35 | residual of W1-27 | LOW | Shared Strings 引用图（合约 / 测试读取） | Traceability | REQ:38、49、53、103、239-243、245 | Shared Strings 反向引用仍不完整：表未列 US1 AS2 / US2 IT+AS1 的括号引用，US5 AS3 直接复制字面量 `not-observed` 而非 [[STR-006]]，且引用约定未声明 US 文本是否在范围内。 | `/speckit.requirements`：Shared Strings / citation convention |
| W1-07 | carried over | MEDIUM | role-edge contract | Ambiguity（输入边界） | REQ:128、126；CHK:21 | FR-005 未定义输入记录集与执行树边界（单根 / 多根、跨 run 无关记录如何隔离），边与深度在不同仓库上不可确定。 | plan / contract |
| W1-08 | carried over | MEDIUM | role-edge contract + SC 集 | Inconsistency（覆盖） | REQ:126、128、210-219；CHK:22 | FR-003 要求 `conflict` 报错并点名两处路径，但 FR-005 的输出枚举没有它、也没有任何 SC 验证它，该 MUST 既无输出归宿也无红测。 | `/speckit.requirements` / plan |
| W1-09 | carried over | MEDIUM | role-edge contract | Ambiguity（优先级） | REQ:126、283；CHK:23 | FR-003 允许根身份取状态脊 `run_id` 或 line registry `line_id` 而未给优先级，A11 只把实现名交给 plan。 | plan / contract（X-03 指 data-model §3） |
| W1-10 | carried over | MEDIUM | role-edge / return contract + SC-005 | Underspecification（Gap） | REQ:126、139、214；CHK:24 | 边记录要求「派发尝试标识」，FR-013 的重试 / 陈旧判定依赖它，但没有既有字段被指明为该标识。 | plan / contract |
| W1-12 | carried over | MEDIUM | protocol contract | Ambiguity（owner + 可扩展性） | REQ:136、262；CHK:32 | FR-010 声明封闭消息分类集却把 owner 写成未具名的「owner 文档」，同时又说「最少区分四类」，owner 与可扩展规则都未固定。 | `/speckit.requirements` |
| W1-13 | carried over | MEDIUM | protocol contract | Gap（载体） | REQ:136、142；CHK:33 | 四类消息中的 `ack` 与 `attention-escalation` 未映射到任何既有载荷 / 回传通道，行使它们就会造出 FR-016 禁止的第二通道。 | plan / contract |
| W1-14 | carried over | MEDIUM | edge lifecycle contract | Gap（载体） | REQ:141；CHK:34 | FR-015 要求把 `completed / failed / cancelled` 写入既有载体，但没有既有记录被指明承载 `cancelled`。 | plan / contract |
| W1-15 | carried over | MEDIUM | recovery contract + SC-005 | Gap（词表 / 载体） | REQ:162、214；CHK:46 | FR-027 / SC-005 要求把仍被判定在跑的子项标为 `interrupted` / `attention`，但词表 owner 与承载标记的记录都未具名。 | plan / contract |
| W1-16 | carried over | MEDIUM | recovery contract + SC-005 | Gap（可观测性） | REQ:163、140、214；CHK:47 | FR-028 要求 resume 前重验证授权，但只有失败路径有具名记录；没有记录区分「已重验证的恢复」与「未验证的恢复」。 | plan / contract |
| W1-17 | carried over | MEDIUM | state-sync contract | Gap（写目标） | REQ:160；CHK:43 | FR-025 要求在下一个外部动作前持久化「边 + 已收到返回」，却未指明具体 per-entry 载体，而唯一被引用的 run report 是单文件产物。 | plan / contract |
| W1-18 | carried over | MEDIUM | status-read contract | Inconsistency | REQ:161、167；CHK:44 | FR-026 要求从状态层、Assignment 事实层与宿主事件层派生，FR-029 又要求同一次状态读取；该单次读取覆盖哪几层未说明。 | plan / contract（W2-01 共享物化） |
| W1-19 | carried over | MEDIUM | digest contract + SC-006 | Ambiguity（有界性） | REQ:167、169；CHK:51 | 「条目 MUST 有界」未说明 cap 是单条还是整集、`omitted` 在哪个集合上声明，FR-031 的父 + 子形状可能被静默截断。 | plan / contract |
| W1-20 | carried over | MEDIUM | run-report mapping + digest contract | Inconsistency | REQ:167、168；CHK:52 | FR-029 要求每行显示父边身份，FR-030 的映射表 schema（`label → 角色 → 工作区`）没有父列，也未给 join 规则。 | `/speckit.requirements` / plan |
| W1-21 | carried over | MEDIUM | dispatch-face contract + SC-002/003/007 | Coverage | REQ:175、211-216；CHK:59 | FR-034 要求 team 与 driver 阶段载荷携带角色字段，但 SC-002 只验证 run-agent 注入、SC-003 只验证边记录，两个接线点无验证。 | `/speckit.requirements` |
| W1-22 | carried over | MEDIUM | test-plan + SC-009 | Ambiguity / Coverage | REQ:177、178、218；CHK:60 | FR-036 的「全套契约测试」未定义是 `contract` 标记、整个 `tests/` 还是具名模块清单，且没有 SC 验证改写 / 保持 / 移除处置台账。 | `/speckit.requirements` / plan |
| W1-23 | carried over | MEDIUM | appendix contract + SC-010 | Measurability | REQ:182、219；CHK:68 | FR-038 / SC-010 要求「可解析证据路径」却未定义可解析（存在 / 可解析内容 / 命令可复现），也未把切片集钉到测量时点或 commit。 | `/speckit.requirements` |
| W1-25 | carried over | MEDIUM | authorization contract | Ambiguity（形态覆盖） | REQ:140、130、69-70；CHK:37 | FR-014 的封闭授权面（能力键 / 席位策略 / 路由裁决 / team territory）未被证明能为 SSH 形态或通用非 SDD 扇出给出可解析授权依据。 | `/speckit.requirements` / plan |
| W1-26 | carried over | MEDIUM | owner-doc assertions + SC-007 | Measurability | REQ:173、174、216、284；CHK:57 | FR-032 / FR-033 与 SC-007 禁止复制 owner 规则文本并要求转红，但没有客观判据区分合法指针与副本，红腿依赖散文判断。 | plan / contract |
| W1-28 | carried over | LOW | 预算测量记录 | Traceability | REQ:285、174；CHK:58 | A13 记录三个字节数与 946 B 余量，但无可复现命令或证据路径，测量无法仅凭需求重导。 | `/speckit.requirements` |
| W1-29 | carried over | LOW | owner-doc assertions | Ambiguity | REQ:173、269；CHK:56 | FR-032 的 owner 文档内容清单要求「术语边界」，却未点名要消歧的术语，该节的完整性不可断言。 | `/speckit.requirements` |

### C/H 行的检测侧证据边界（不得作为验证者 verdict 传入）

- **W1-30**：已实测三处文本（REQ:125/197/210 的标记语义 vs REQ:128 的声明语义）与 Shared Strings 行（REQ:239）；未测量下游契约是否已用 `dispatch_duty` 分离字段（W2-04 的修复记录提到该键）。若契约已按字段分离，claim 收窄为「requirements 文本未声明字段作用域」。
- **W1-31**：已实测两处判据文本（REQ:177 vs 218）；未运行测试套件，因此基线中这四类治理测试是否已有红未测量。若基线确实全绿，SC-009 与 FR-036 仍缺「基线绿」的显式参照物，claim 降为可读性 / 可判定性问题。
- **W1-32**：已实测 SC-001 Source（REQ:223「违例三类」）与四处四类文本（REQ:39/128/210、US1 叙述 REQ:29 仅列三类示例）；未发现其他「三类」残留于 requirement 正文。修复动作只涉及一处词与一处叙述，不改语义。

## Rerun Delta（相对上轮 W1）

### Resolved Since Last Run（已核验关闭）

| 上轮 ID | 关闭证据（本轮实读） |
|---------|----------------------|
| W1-01 | REQ:139（FR-013）删去 attribution 五取值枚举，改为 `watch-model.md` § 11 owner 指针 + 「本规格不复述该枚举」。 |
| W1-02 | FEAT:16 `## Implementation Notes`、FEAT:55 `## Related Files` 已存在；宪法 Feature Documentation Requirements 的四节齐备。 |
| W1-03 | REQ:125（FR-002）、REQ:197（Key Entities）、REQ:210（SC-001）统一为 `{subagent, superagent}` 集合 + `dual-role` 组合标记、非第三取值。残留 token 语义冲突另报 W1-30。 |
| W1-05 | REQ:128（FR-005）点名声明载体：team 映射行 `role` 列 / stage envelope `role_edge` 中的显式 `superagent` 断言；`dual-role` 不再被当作 superagent 主张。 |
| W1-06 | REQ:147（FR-018）改为逐项匹配 [[STR-003]] 标识与九项 item-id 句柄，缺项阻断；字面量 owner 指向 `data-model.md` § 7。 |
| W1-11 | REQ:146（FR-017）改为「MUST 恰好包含下列九项（封闭清单，不得增项）」。 |
| W1-24 | REQ:182（FR-038）已含「切片机制主张」与 [[STR-006]] 的「未观测理由」；FR-038 半边关闭。FR-033 段位置仍记录于 Clarifications Q5（同一制品内，不构成缺陷）。 |
| W1-27 | REQ:239-241 已补 STR-002←FR-005、STR-003←FR-034、STR-004←FR-004/FR-034；原 finding 点名的三处 FR 级缺口关闭。US 级残留另报 W1-35。 |

### Partially Resolved

- **W1-04**：FR-005（REQ:128）、US1 AS3（REQ:39）、SC-001（REQ:210）已改为四类；但 **SC-001 Source（REQ:223）仍写「违例三类」**，US1 故事叙述（REQ:29）也只列三类示例。残留重报为 **W1-32（HIGH）**。

### New Since Last Run

- **W1-30（HIGH）**：`dual-role` token 双语义；根因与 W2-02 的修复相关（收窄了违例谓词，但未分离 token）。
- **W1-31（HIGH）**：SC-009「全绿」vs FR-036「唯一判据 / 基线豁免」；X-01 只修了 plan 半边，SC-009 未在其证据锚点内。
- **W1-33（MEDIUM）**：CHK016 的 FR-012 半边残留（slow / stalled owner 未具名）；上轮把该半边记为 covered-by 过宽。
- **W1-34（MEDIUM）**：SC-002 三要素 vs SC-002 Source「四项断言」vs FR-019 四项义务。

### Residual of a Fixed Finding

- **W1-35（LOW）**：W1-27 的 US 级残留（未列 US1 AS2 / US2 IT+AS1；US5 AS3 字面量 `not-observed`）。

### Carried Over（requirements 文本未变，维持上轮归属）

W1-07、W1-08、W1-09、W1-10、W1-12、W1-13、W1-14、W1-15、W1-16、W1-17、W1-18、W1-19、W1-20、W1-21、W1-22、W1-23、W1-25、W1-26、W1-28、W1-29。

## Residue Registry（上轮 29 条逐条状态）

| 上轮 ID | Sev | 本轮状态 | Disposition | 理由 / 证据 |
|---------|-----|----------|-------------|-------------|
| W1-01 | C | fixed | fixed | REQ:139 owner 指针替换枚举（本轮实读）。 |
| W1-02 | C | fixed | fixed | FEAT:16/55 四节齐备（本轮实读）。 |
| W1-03 | H | fixed | fixed | REQ:125/197/210 形态统一；token 残留另报 W1-30。 |
| W1-04 | H | partially-fixed | deferred（残余） | 主文本已改四类；SC-001 Source 与 US1 叙述残留，重报 W1-32。 |
| W1-05 | H | fixed | fixed | REQ:128 声明载体具名。 |
| W1-06 | H | fixed | fixed | REQ:147 逐项句柄 + 阻断。 |
| W1-07 | M | open | deferred | requirements 未变；输入集 / 树边界仍缺。 |
| W1-08 | M | open | deferred | requirements 未变；下游 data-model §2 / contract C-3 已有 `conflicts` 行（W2-06 记录），但 requirement 侧输出 / 退出 / SC 仍缺。 |
| W1-09 | M | open | deferred | requirements 未变；下游 data-model §3 解析顺序见 X-03 记录。 |
| W1-10 | M | open | deferred | requirements 未变；`attempt` 已出现在下游冲突行（W2-06 记录）。 |
| W1-11 | M | fixed | fixed | REQ:146「恰好九项」。 |
| W1-12 | M | open | deferred | REQ:136 未变；封闭 vs 最少四类、owner 未具名。 |
| W1-13 | M | open | deferred | REQ:136/142 未变；ack / escalation 无载体映射。 |
| W1-14 | M | open | deferred | REQ:141 未变；cancelled 无承载记录。 |
| W1-15 | M | open | deferred | REQ:162/214 未变；interrupted / attention 无 owner。 |
| W1-16 | M | open | deferred | REQ:163 未变；resume 重验证无正向记录。 |
| W1-17 | M | open | deferred | REQ:160 未变；per-entry 载体未点名。 |
| W1-18 | M | open | deferred | REQ:161/167 未变；单次读取层覆盖未说明（W2-01 已改共享物化）。 |
| W1-19 | M | open | deferred | REQ:167/169 未变；cap 单位 / omitted 范围未定义。 |
| W1-20 | M | open | deferred | REQ:167/168 未变；映射表父列 / join 规则未给（feature detail 的 plan 投影已加 `parent`）。 |
| W1-21 | M | open | deferred | REQ:175 未变；team / driver 载荷无 SC。 |
| W1-22 | M | open | deferred | REQ:177/178 未变；套件范围 / 处置台账无 SC。 |
| W1-23 | M | open | deferred | REQ:182 未变；「可解析」与测量点未定义。 |
| W1-24 | M | fixed | fixed | REQ:182 已含机制主张 + not-observed 理由。 |
| W1-25 | M | open | deferred | REQ:140 未变；非 SDD / SSH 授权面未证。 |
| W1-26 | M | open | deferred | REQ:173/174 未变；指针 vs 副本无结构判据。 |
| W1-27 | L | fixed（cited scope） | fixed | REQ:239-241 三处 FR 级缺口关闭；US 级残留重报 W1-35。 |
| W1-28 | L | open | deferred | REQ:285 未变；A13 无命令 / 证据路径。 |
| W1-29 | L | open | deferred | REQ:173 未变；「术语边界」未点名术语。 |

**Residue 合计**：29 = 8 fixed + 1 partially-fixed + 20 deferred + 0 rejected。无静默丢条。

## Checklist Accountability（pass H）

**等式**：39 unchecked = **25 raised-as-finding + 14 covered-by + 0 unraised/undispositioned**。

- CHK001 disposition: covered-by requirements.md §FR-001 / §FR-002
- CHK002 disposition: raised-as-finding W1-30
- CHK003 disposition: raised-as-finding W1-32
- CHK004 disposition: covered-by requirements.md §FR-005
- CHK005 disposition: raised-as-finding W1-07
- CHK006 disposition: raised-as-finding W1-08
- CHK007 disposition: raised-as-finding W1-09
- CHK008 disposition: raised-as-finding W1-10
- CHK009 disposition: covered-by requirements.md §FR-008 / §FR-001 / §FR-005
- CHK010 disposition: covered-by requirements.md §FR-022 (d) / §FR-011 (e) / §FR-010 + Clarifications Q3 (g)
- CHK011 disposition: covered-by requirements.md §FR-017（恰好九项、不得增项）
- CHK012 disposition: covered-by requirements.md §FR-018（逐项句柄；字面量 owner 指向 data-model.md §7，存在性未在 W1 读域核对）
- CHK013 disposition: raised-as-finding W1-12
- CHK014 disposition: raised-as-finding W1-13
- CHK015 disposition: raised-as-finding W1-14
- CHK016 disposition: raised-as-finding W1-33（FR-013 半边 covered-by requirements.md §FR-013）
- CHK017 disposition: covered-by requirements.md §FR-009 / §FR-019 / §FR-020
- CHK018 disposition: raised-as-finding W1-25
- CHK019 disposition: covered-by requirements.md §FR-022 / §FR-024（owner 文件存在性不在 W1 读域）
- CHK020 disposition: covered-by requirements.md §FR-022 / §FR-023（grain 与读数三元组归既有 owner）
- CHK021 disposition: raised-as-finding W1-17
- CHK022 disposition: raised-as-finding W1-18
- CHK023 disposition: covered-by requirements.md §FR-026 / §SC-005
- CHK024 disposition: raised-as-finding W1-15
- CHK025 disposition: raised-as-finding W1-16
- CHK026 disposition: raised-as-finding W1-19
- CHK027 disposition: raised-as-finding W1-20
- CHK028 disposition: raised-as-finding W1-29
- CHK029 disposition: raised-as-finding W1-26
- CHK030 disposition: raised-as-finding W1-28（触发条件半边 covered-by requirements.md §FR-033 / §A7）
- CHK031 disposition: raised-as-finding W1-21
- CHK032 disposition: raised-as-finding W1-22
- CHK033 disposition: covered-by requirements.md §FR-035 / §SC-008 / Measurement Sources SC-008
- CHK034 disposition: covered-by requirements.md §SC-003 / §US3 Independent Test / §A3
- CHK035 disposition: covered-by requirements.md §FR-038（机制主张 + not-observed 理由）+ Clarifications Q5（FR-033 段位置）
- CHK036 disposition: raised-as-finding W1-35
- CHK037 disposition: raised-as-finding W1-23
- CHK038 disposition: raised-as-finding W1-30
- CHK039 disposition: covered-by checklists/requirements-quality-2026-11-10.md §七（39/39 均可由需求正文或点名 owner 行回答，无一条要求运行产品）

**`[Gap]` 子集**：按 tag 列表任意位置匹配为 **10** 条（CHK004 / 008 / 010 / 015 / 016 / 019 / 021 / 024 / 025 / 039）= 6 raised（CHK008/015/016/021/024/025）+ 4 covered-by（CHK004/010/019/039）+ 0。上轮报告的「9」只计 tag 首位匹配；CHK039 的 `Gap` 位于第二位，故完整子集为 10，问责等式不受影响。

## 其他检测面

- **A 重复**：0 条新 duplication。FR-029/030/031/035 的「不新建 renderer / parser」按作用面不同属逐面约束；US2 AS1 的九项复述是验收映射。W1-30 是语义过载，不是副本问题。
- **B 歧义 / C 欠指定 / F 不一致**：已逐条落入 W1-07…W1-35。
- **D 宪法对齐**：W1-01（XIV One Source of Truth）与 W1-02（Feature Documentation Requirements）均已核验关闭；读域内无新增 CRITICAL 宪法冲突。W1-30 按 F 不一致（HIGH）报告而非 XIV：两处陈述作用于不同记录位置（输出角色集标记 vs 输入声明值），缺的是字段作用域声明；若验证者把 Shared Strings 行读作该 token 的语义 owner，则按 XIV 优先级升为 CRITICAL。
- **E 覆盖**：未裁决（`tasks.md` 不在 W1 读域）。修复轮的确定性记录报告 `account-clause-coverage.py` 仍 `status: uncovered`、29 条子句超出冻结基线、FR 契约引用组 18 uncovered（`analyze-repair-dispositions-2026-11-10.md` §3，非 W1 复测）。
- **G Feature linkage / registry**：requirements 的 `Related Feature` 095（REQ:14-15）与 `.specify/features.md:102` 行、`.specify/features/095-superagent-role.md` 的 ID / Name / Spec Path 一致；索引 `Total Features: 90` 与 90 行一致（机械核对）；Feature 095 行与详情文件均为 `Planned`（analyze 无状态迁移，合法）；详情文件四节齐备。无 registry finding。
- **I Decision Tension**：未裁决（`plan.md` 不在 W1 读域，归 W2 / 集成者）。

## Coverage Summary

| 维度 | 读数 | 说明 |
|------|------|------|
| Checklist 问责 | 39/39 = 100% dispositioned | 25 raised + 14 covered-by + 0 |
| Requirement ↔ task 覆盖 | 未测 | `tasks.md` 与 `account-clause-coverage.py` 不在 W1 读域；见集成者第 3 步 |
| Feature linkage | 1/1 consistent | 095 行 / 详情 / 需求绑定一致 |
| Shared Strings 正向解析 | 6/6 可解析 | 所有 `[[STR-NNN]]` 均在表中有行（validator `ref-resolvable` pass） |
| Shared Strings 反向完整 | 部分 | 3 条 US 级消费者未列 + 1 处字面量复制（W1-35） |

## Systemic Observations

- **SO-R2-1（修复扇出缺口）**：W1-04 把违例集从三类改为四类时，主 FR / AS / SC 都改了，但 SC-001 的测量源与 US1 故事叙述未同步（W1-32）。计数变更需要机械扫描「三类 / 四类」全部出现点，而不只改被判红的那一行。
- **SO-R2-2（token 过载残留）**：W2-02 通过收窄违例谓词修掉了误判，但没有分离 `dual-role` 的两个语义（W1-30）；下游已引入 `dispatch_duty`，requirements 侧应使用它或显式声明字段作用域。
- **SO-R2-3（Shared Strings 反向弱面）**：W1-27 只关了 FR 级缺口，US 级消费者与字面量复制仍在（W1-35）；引用约定需要声明 US 文本是否在范围内，或把反向核对机械化。
- **SO-R2-4（观察，非 finding）**：checklist 头部的 `287 行 / 53,696 B` 是创建时快照；当前 `requirements.md` 实测 55,778 B（`wc -c`）。按 one-source-of-truth 的 dated-record 豁免，不作为 finding；下游复核者不应把它当作当前读数。
- **SO-R2-5（deferred 簇）**：20 条 deferred MEDIUM/LOW 集中在字段级 schema / 载体命名（输入树、conflict 输出、attempt id、消息与终止载体、恢复标记、digest cap）。这是与 plan / contracts 的既定分工，但集成者在清门前应核对下游 owner 是否已闭合，而不是当作已解决。

## Metrics

- **Requirements**：validator `status: ok`，6 标签全 pass，0 error / 0 warning（`scanned: 288 lines, 48 definition rows, 6 shared strings`）；`wc -c` = 55,778 B；38 FR（FR-001…FR-038 连续）；10 SC（final 7 / supporting 3）；6 Shared Strings；5 用户故事；10 Edge Cases；16 Clarification Q（6 + 10）；15 Assumptions（A1–A15）。
- **Checklist**：39 条（`grep -c '^- \[ \] CHK'`），全部未勾选；39 条全部 dispositioned；`[Gap]` 标记（任意位置）= 10 条。
- **Findings**：26 条 = **3 HIGH / 20 MEDIUM / 3 LOW / 0 CRITICAL**；其中 new/residual 6 条（3H / 2M / 1L），carried 20 条（18M / 2L）。
- **Round-1 delta**：29 = 8 fixed + 1 partially-fixed + 20 deferred + 0 rejected。
- **验证状态**：W1-30 / W1-31 / W1-32 为 detector 提案，**pending 集成者独立验证波**；W1 未自验 C/H。

## Limitations

- 读域隔离使 pass E / pass I、clause coverage accountant 与 plan/tasks/contracts 侧映射无法在本文件裁决；这些属集成者与 W2/W3。
- 修复处置文件是 dated record；本文件引用的下游闭合（data-model §3、contract `conflicts`、`dispatch_duty` 等）来自该记录，未在 W1 读域内复测。
- W1 是 detector，不是 validator；3 条 HIGH 的严重度与证据边界须由 fresh-context 验证者独立裁决。
- checklist 的条目文本是创建时快照；本轮只对当前 requirements 文本重新 disposition，未刷新 checklist 条目本身（按其自身协议应新建 recheck 文件）。
