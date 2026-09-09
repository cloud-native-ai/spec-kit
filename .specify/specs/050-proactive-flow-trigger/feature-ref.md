# Feature Binding: 050-proactive-flow-trigger

**Requirement Key**: `050-proactive-flow-trigger`
**Bound Feature**: Feature 050 — Proactive Flow Trigger(主动触发机制)
**Binding decided**: `/speckit.clarify` Session 2026-09-07(第二轮 R2-Q1)
**Date**: 2026-09-07
**Status transition this plan lands**: `Draft → Planned`

## 绑定结论

需求 050 **新建 Feature 050**,不绑定任何既有 Feature。当前 Feature 总数以 `.specify/memory/features.md` 的头部计数为权威(本 plan 不复制该数值)。

## 绑定依据(证据)

按 `shared/workflow/feature-integration.md` § Feature Binding Rules 的**绑定先例启发式**(候选 Feature 的同胞吸收证据)逐个核验:

| 候选 Feature | Status | 已吸收同胞 specs | 与需求 050 的实际关系 | 判定 |
|---|---|---|---|---|
| 032 Task Complexity Rubric | Implemented | 1(自身) | **最接近的结构先例**:同为嵌入 `.specify/instructions.md`、经 `/speckit.instructions` 非破坏投递的行为指令 | 主题不同(思考深度校准 vs 流程选取)→ 不绑,但其**自成 Feature 的先例**成为本次判定的决定性依据 |
| 008 Instructions Command | Completed | 1(自身) | 仅投递载体(生成触发段所落的文件) | 载体 ≠ 归属 → 不绑 |
| 001 Unify Command Handoffs | Completed | 1(自身) | 能力前身;其 `## Handoffs` 散文段是本特性**种子规则的派生来源** | 需求 050 的 Out of Scope 明确不改命令模板 Handoffs → 不绑 |
| 022 AI Tools Support | Implemented | 4(011/019/021/018) | 拥有 FR-003 的议题(全 agent init 覆盖完整性) | 强吸收者但仅覆盖 1/26 条 FR → 不绑 |
| 028 Feedback Mechanism | Implemented | 3(027/041/047) | 计数-阈值机制与事件记录的**范式来源** | 主题是 feedback 存储与 probe 注册表 → 不绑 |
| 046 Confirmation Gate Governance | Implemented | 1(044) | 破坏性判据与回流约束的**权威来源**(FR-011 / FR-007 只消费) | 消费关系 ≠ 归属 → 不绑 |

**决定性论证**:032 与本需求的投递载体完全相同(指令文件内嵌的行为指令段),而 032 当初**自成一个 Feature** 而非绑 008 Instructions Command。这确立了「以指令段形式嵌入是**投递事实,不是归属事实**」。加之需求 050 引入三个既有 Feature 范围均不覆盖的持久面(规则集 / 晋升态 / 事件与回合遥测),归属新建。

## 本 plan 对 Feature 050 的映射

| 规格面 | 数量 | 落点 |
|---|---|---|
| Functional Requirements | 26(FR-001…FR-023 + FR-005a / FR-005b / FR-009a) | 4 份契约的 **61** 条款 + `data-model.md` 的 **6 组 / 32 条**校验规则(V1…V6) |
| Success Criteria | 15(SC-001…SC-015) | **不是** quickstart 6 场景逐条覆盖(analyze M-07 订正:quickstart 只直接引用其中 8 条)。每条 SC 的**具名产出任务与固化契约**见 `requirements.md` § Measurement Sources —— 该节已重写,15 条全部指名产出任务(T013/T015、T028、T029/T036、T037/T043、T047/T050、T018/T028、T030/T036) |
| User Stories | 4(2×P1 + 2×P2) | US1+US2 = MVP(quickstart 场景 1–3);US3(场景 4–5);US4(场景 6) |
| Key Entities | 7 | `data-model.md` E1…E7 |

**FR → 契约映射(analyze 2026-09-08 全面订正 —— 原表有三条指向断言别的事的条款,且十余条被路由到只断言结构属性的 C-1…C-7)**

- FR-001 → `trigger-section.md` C-1 / C-2 / C-9(双表面、字节镜像、additive reconcile 传播)
- FR-002 → `trigger-section.md` C-4 / C-5(摘要+指针形态、零流程枚举,含 C-5 的检测模式)
- FR-003(硬前置) → `trigger-section.md` C-10 / C-12(路径计数唯一权威 + 声明与生成一致)
- FR-004 → `trigger-section.md` C-9(传播且幂等、块外字节不变)
- FR-005 → `discipline-doc.md` **C-9**(两级预算 + P1–P5 判据表 + 升级率口径)、`trigger-engine.md` C-13(未传 `--probe` 时零制品文件打开)
- FR-005a → `discipline-doc.md` **C-8**(每回合 + 静默 + 评估节奏≠建议节奏)、`trigger-engine.md` C-14(恒写一行遥测)
- FR-005b → `discipline-doc.md` **C-11**(顺序契约)、`trigger-engine.md` C-10(`--compliance-done` 输入通道)+ C-14(`ordering-violation`)、`trigger-section.md` C-3(结构落点)
- FR-006 → `discipline-doc.md` **C-10** ①、`trigger-engine.md` C-15(`payload.suggestion` 含 `invocation` 与 `rationale`)
- FR-007 → `discipline-doc.md` **C-10**(非阻塞提示)、`trigger-section.md` C-6 + `discipline-doc.md` C-3(零 BLOCKING 命中 = 回流约束的机械面)
- FR-008 → `discipline-doc.md` **C-10** ②③④、`trigger-engine.md` **C-20**(会话级重复抑制机制)+ C-12(无匹配即不建议)+ C-15(收敛为一条)、`data-model.md` V6.7 / V6.8
- FR-009 → `trigger-engine.md` C-14(两类记录)、`data-model.md` E3 / E4 + V3.1…V3.4 / V4.1…V4.5
- FR-009a → `trigger-engine.md` `rotate` 行、`data-model.md` V4.3(追加即截断的恒真不变量)/ V4.4(不触及 index.json)
- FR-010 → `trigger-engine.md` C-16 / C-18、`data-model.md` V3.1 / V3.2 / V5.1…V5.4
- FR-011 → `trigger-engine.md` **C-17**(破坏性零容忍,10 次采纳仍不晋升)、`data-model.md` V2.1 / V5.1;判据 owner = `shared/guidelines/confirmation-gates.md`(引用不复述)
- FR-012 → `discipline-doc.md` **C-12** ③⑤。三段式执行报告义务的 owner 是 `shared/guidelines/confirmation-gates.md` L54–60,已由既有 `tests/contract/test_confirmation_gates_execution_report.py` 机械断言;`discipline-doc.md` C-4 **禁止**复述它,故本特性以路径引用消费。**实现期义务**:把本特性两个新表面加入该测试的 `AUTO_EXEC_SURFACES`(analyze M-01 的残留缺口)。复位/降级 → `trigger-engine.md` `reset` / `config` 行 + `data-model.md` V5.3
- FR-013 → `trigger-engine.md` C-8、`data-model.md` V6.4
- FR-014 → `data-model.md` E2 + V2.1…V2.5
- FR-015 → `trigger-engine.md` `tune`(四类指标含误报)/ `record-manual`(漏报关联)、`data-model.md` SM-2
- FR-016 → `discipline-doc.md` **C-14** ③④、`trigger-engine.md` `tune-apply`(两段转移 + 双时间戳)、`data-model.md` SM-2
- FR-017 → `trigger-engine.md` `tune` 行(小样本守卫 + `notes[]` 具名回显)、`data-model.md` SM-2
- FR-018 → `discipline-doc.md` **C-15**、`trigger-engine.md` `config` 行、`data-model.md` V6.1 / V6.8
- FR-019 → `trigger-engine.md` **C-21**(引擎从不自行执行流程 → 抢占在引擎侧结构上不可能)+ `discipline-doc.md` **C-12** ④(agent 侧让位/延后)。**原映射 `Suggestion Shape` 不成立**(该行只管建议形态与频次,全文无"抢占"语义)
- FR-020 → `trigger-engine.md` **C-19**(禁网络能力 import + 写路径限于 `workspaceRoot` + 不入上行通道)、`data-model.md` §存储布局(git 跟踪边界)。**原映射 C-6/C-7/C-8/C-18 全不成立**(那是原子写、root 解析、降级、阈值链)
- FR-021 → `trigger-engine.md` C-18(阈值优先级链与 `feedback-utils.py:resolve_threshold` 同构)+ C-1(stdlib、无平行引擎)
- FR-022 → `seed-derivation.md` C-1…C-10(含 `anchorKind` 两类来源、provenance 逐字引文、漂移检出、同构性、合并时不回退用户调优)
- FR-023 → `data-model.md` E1 + V1.1…V1.6(受控词表、身份≠快照、最具体优先)、`trigger-engine.md` C-11 / C-12

## 状态处理

Feature 050 当前 **Draft**(2026-09-07 注册)。本 plan 落 **`Draft → Planned`** —— 依 `.specify/templates/feature-details-template.md` § Canonical Status State Machine 的 DoD:`plan.md`、`data-model.md`、`contracts/`、`quickstart.md` 均已存在,且 Constitution Check **无未论证的 Fail 行**。

**Constitution 结果订正(analyze 2026-09-08)**:原记 14/14 Pass、Complexity Tracking N/A;订正为 **13 Pass / 1 Partial(Principle XIV)**,Complexity Tracking **已填**并给出完整论证(为何需要该副本、四条被否决的更简替代、五项缓解、残留代价)。Planned 的 DoD 要求是"无**未论证**的 Fail 行",一个**已论证的 Partial** 满足该要求,故 `Draft → Planned` 的转移仍成立、无需回退。

`/speckit.plan` **MUST NOT** 落 `Implemented` —— 该转移由 `/speckit.implement` 持有,且受 Principle VII 的 Pre-Status-Flip Gate(NON-NEGOTIABLE)约束:零 `[ ]` 任务 + 每条 SC 在 `verification.log` 有状态行。

## 注册义务清单

| 义务 | 状态 |
|------|------|
| `.specify/memory/features/050.md` 详情文件(0 残留占位符) | ✅ 已于 clarify 阶段完成 |
| `features.md` 索引行 + 表头计数 49→50(**手工编辑**;`update-feature-index.sh` 为破坏性脚本) | ✅ 已于 clarify 阶段完成 |
| 相邻 Feature 032 反向交叉引用 | ✅ 已于 clarify 阶段完成 |
| `features/050.md` § Status Tracking 的 Planned 行更新为达成 + 设计要点 | ✅ 已于 plan 收尾完成 |
| `features/050.md` § Latest Review 追加本轮设计要点 | ✅ 已于 plan 收尾完成(四项决定性裁定 + 两处被推翻的既有记录 + 门控预算处置) |
| `features.md` 050 行 Status `Draft → Planned` + Last Updated 追加 **plan 阶段注记** | ✅ 已于 plan 收尾完成(手工编辑) |
| 新增 Tool 记录 `.specify/memory/tools/trigger-utils.py.md`(Principle XII 义务) | ⬜ 实现期执行(引擎落地后) |
| glossary 词条(8 条:主动触发点/情境评估/建议规则/阈值晋升/触发学习状态/情境身份/回合遥测/种子规则) | ✅ 已落地,`validate` 通过 |

## 交叉引用(消费关系,非归属)

- **Feature 046 Confirmation Gate Governance**:破坏性判据与回流约束的**唯一权威**。本特性只消费不修改;且门控扫描整数余量为 0,本 plan 以**设计规避**(全部新文案零 `BLOCKING_PATTERNS` 命中)而非改写 `baseline.json` 来守预算(plan.md D-4)。
- **Feature 028 Feedback Mechanism**:阈值解析优先级链的范式来源(`resolve_threshold` / `should_prompt`);**复用范式不复用代码**(引擎间无 import 先例,且 scripts 镜像对为 STRICT 独立副本)。其存储域不受本特性影响。
- **Feature 001 Unify Command Handoffs**:`## Handoffs` 散文段是种子规则的派生来源;`seed-derivation.md` C-7 把二者的一致性钉为漂移检出条款,故 001 的任何 Handoffs 改写都会机械地要求本特性同步种子。
- **Feature 022 AI Tools Support**:FR-003 的路径覆盖修复(`HERMES.md` / `.opencode/instructions.md`)同时消除该 Feature 审计面上 `_check_instructions` 的两处恒 `fail`;022 的 Future Evolution #1(集中式 agent 能力矩阵)与本特性 Out of Scope 的原生 hook 通道同源,宜合并考虑。
- **Feature 032 Task Complexity Rubric**:归属判定的决定性先例;其 Future Evolution #3(把 rubric 结果喂回 028 以调优信号)与本特性 US4 的规则调优形状同构。
- **Feature 040 Token Efficiency Discipline**:Program-First 与 Summary-First 是本特性"每回合评估付得起"的前提;`assess` 的文件打开计数断言(`trigger-engine.md` C-13)是该纪律的机械化。
