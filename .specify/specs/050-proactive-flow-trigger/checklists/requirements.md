# Specification Quality Checklist: 主动触发机制(Proactive Flow Trigger)

**Purpose**: Validate specification completeness and quality before proceeding to planning  
**Created**: 2026-09-07  
**Feature**: [../requirements.md](../requirements.md)

## Content Quality

- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Success criteria are technology-agnostic (no implementation details)
- [x] All acceptance scenarios are defined
- [x] Edge cases are identified
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria
- [x] User scenarios cover primary flows
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification

## Notes

- ~~`Feature ID: Need clarification` is pending by design~~ → **已解决**(clarify 2026-09-07 第二轮 R2-Q1):**新建 Feature 050 Proactive Flow Trigger**。注册义务已全部完成——`.specify/memory/features/050.md` 详情文件(0 残留占位符)、`features.md` 索引行 + 表头计数 49→50(**手工编辑**,`update-feature-index.sh` 为破坏性脚本,承 Feature 049 记录)、相邻 Feature 032 加反向交叉引用。索引一致性已程序校验:50 行 / header 50 / ID 唯一且 1–50 连续 / 详情文件 50 份。
- Validation details (2026-09-07, iteration 1):
  - **Content quality**: spec describes WHAT/WHY(埋点交付、情境评估建议、阈值晋升、规则优化). The only file paths cited are **existing repo anchors** in 现状锚点 and Measurement Sources(house convention from specs 047/049),不是对新解法的实现规定;新解法的落盘路径/格式/是否引擎化被显式推迟到 `/speckit.plan`(见 Assumptions)。
  - **NEEDS CLARIFICATION markers: 3 raised → 3 resolved**(2026-09-07,同会话内由用户裁定;残留 0):
    1. 触发通道范围 → **A:仅指令文件常驻指令**(不建 agent 原生 hook)。
    2. 情境评估证据预算 → **C:环境信息为主 + 按需升级确定性探测**(升级判据须显式声明)。
    3. 评估触发时机 → **B:每个用户回合都评估**(评估静默,建议输出另受频次约束)。
  - **Testability**: FR 共 **23 条**(FR-001…FR-021 + clarify 插入的 FR-005a / FR-005b,沿用需求 049 的 FR-002a 字母后缀惯例以稳住既有编号),每条至少映射一个 Acceptance Scenario 或 SC;SC 共 **12 条**(SC-001…SC-012),每条具名 Measurement Source。
  - **安全边界已硬编码为需求而非取舍**:FR-011(破坏性永不晋升)+ SC-005(破坏性流程自动执行数 0,零容忍)+ Out of Scope(破坏性自动执行永久排除)。此为本特性最大风险面,已在三处交叉锁定。
  - **治理合规**:FR-007(非阻塞,回流约束)+ SC-008(门控扫描新增违规 0);FR-002(引用不复制,单一事实源);FR-005(摘要优先,token 效率);FR-021(单引擎坍缩)。
  - **术语冲突已显式避让**:用户输入的"埋点"/"自省"与词汇表既有 **Feedback Probe** / **Feedback Introspection**(需求 047)语义不同;本规格采用**主动触发点 / 情境评估**独立术语,按 glossary 协议提交待确认(见 Assumptions)。
  - **标识符预留核查已执行**:`PROACTIVE` / `AUTO_TRIGGER` / `SUGGEST*` 零占用;已占用需避让项已列入 Assumptions。
  - **现状锚点已逐条实测**:指令生成链与 symlink 落点、模板 17 章节无触发段、`_INSTRUCTIONS_FILE_MAP` 6 声明 vs 4 生成的覆盖缺口、25/25 命令模板带 `## Handoffs`(先有鸡蛋问题)、feedback 阈值机制同构先例、确认门控判据、状态落盘范式、框架无 hook 能力位、**constitution 每回合合规义务先例**(Documentation Map L13 + 常驻指令 L22 + L90)与其**plan 期门控的边界**(`plan-template.md:31–33` + `plan.md:63–66`)。
- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`.

## Clarify Pass — Session 2026-09-07

三项裁定 + 一项用户追加指示,及其落地改动:

| 决策 | 结果 | 规格改动 |
|------|------|----------|
| 触发通道范围 | **A:仅指令文件常驻指令**;不建 agent 原生 hook | Overview 1;US1 叙述(含漏报为已接受风险 + US4 漏报检测作补偿控制);FR-003 升级为**硬前置**;新增 Edge Case「agent 未遵守指令 → 完全不触发」;Out of Scope 由"取决于澄清"改为**确定排除** |
| 情境评估证据预算 | **C:环境信息为主 + 按需升级确定性探测** | Overview 2;US2 叙述 + 场景 9/10;FR-005 改为两级预算 + 升级判据须显式声明;新增 Edge Case「按需升级退化为每回合升级」;**新增 SC-011**(探测调用率 ≤ 20%) |
| 评估触发时机 | **B:每个用户回合都评估** | Overview 2;US2 叙述 + 场景 1/8;**新增 FR-005a**(每回合 + 静默 + 评估节奏≠建议节奏 + 与 FR-005 同时落地);FR-008 措辞收窄为"建议输出频次";SC-011 含"无适用流程回合可见输出 0" |
| 用户追加指示:挂在 constitution 每回合分析之后 | **采纳,并按实测收敛为两级** | 新增 2 条现状锚点(constitution 常驻指令 vs plan 期枚举门控);**新增 FR-005b**(顺序契约:合规先行、同一趟接续;禁止把 plan 期完整门控每回合化);US2 场景 11;**新增 SC-012**;新增 Edge Case「plan 期完整 Constitution Check 被误搬到每回合」;Out of Scope 增 2 项;Assumptions 增挂载位置一条 |

**核实说明(输入理智检查)**:用户表述"针对 constitution 的遵守必须要求每个请求都进行分析处理"——实测**部分成立**。每回合分析义务确实存在且正靠必经指令路径投递(`templates/instructions-template.md` Documentation Map 首行 + 表尾常驻指令「ALWAYS check the relevant document from the map above first」),但**形式化的逐原则 Constitution Check 门控是 plan 期**(`plan-template.md:31–33` GATE,由 `/speckit.plan` 动态枚举)。二者混同会导致把昂贵门控搬到每回合——已按"只挂轻量义务"收敛,并在 FR-005b ②、Edge Case、Out of Scope 三处设防。

**三项裁定的相互依赖已显式记录**(Assumptions):Q3=B 的可负担性依赖 Q2=C 的近零默认预算;Q1=A 的漏报风险依赖 US4 漏报检测;Q2=C 的升级纪律依赖 SC-011 比率上限。单独实现任一项都会使另外两项代价失控。

后置校验:`NEEDS CLARIFICATION` 残留 **0**;模板占位符残留 **0**;FR **23** 条、SC **12** 条(12 outcomes + 12 sources 一一对应)、User Story **4** 个(2×P1 + 2×P2)、Acceptance Scenario 共 **30** 条(US1 6 / US2 11 / US3 8 / US4 5)、Edge Case **14** 项;**8** 个一级章节顺序完好(Related Feature → Overview → User Scenarios & Testing → Requirements → Success Criteria → Clarifications → Out of Scope → Assumptions,与需求 049 一致);历史 Clarifications 为首次写入,无追加冲突;`Related Feature` 仍为 `Need clarification`(按设计移交 `/speckit.clarify`);glossary 新增 5 条经引擎 detect-conflict 无冲突后直写、validate 通过。

## Clarify Pass — Session 2026-09-07(第二轮 · Mode A)

五项裁定及其落地改动(标号用 **R2-Qn** 前缀,以区别同日首轮的 Q1–Q3):

| 决策 | 结果 | 规格改动 |
|------|------|----------|
| R2-Q1 Feature 绑定 | **新建 Feature 050 Proactive Flow Trigger** | `Related Feature` 解析 + 6 候选核验表 + 绑定依据;新建 `features/050.md`;`features.md` 索引行 + 计数 49→50(手工编辑);Feature 032 加反向交叉引用 |
| R2-Q2 规则集冷启动 | **带出厂种子,且从既有 `## Handoffs` 派生** | **新增 FR-022**;FR-014 增"来源(种子/学习)"字段;Key Entities 建议规则增来源;US2 场景 12 + Independent Test (f);**新增 SC-013** + Source;新增 Edge Case「种子更新与用户调优冲突」;Assumptions 一条;落地层级假设改写(种子随模板分发、学习产物不分发) |
| R2-Q3 阈值语义 | **连续采纳,一次拒绝即重置**(首轮遗留项) | FR-010 去掉"推断默认待确认"标注并写入裁定理由 + 引用 FR-023;Assumptions 阈值语义条改为已决;US3 场景 3 无需改动即成立 |
| R2-Q4 情境身份 | **粗粒度受控词表**(生命周期阶段 × 待处理信号集) | **新增 FR-023**;FR-014/FR-010 引用之;**新增 Key Entity 情境身份**(并与其区分"情境快照");建议事件属性改为携带情境身份;US2 场景 13;**新增 SC-014**(跨会话一致率 100% + 指纹反模式判别)+ Source;新增 Edge Case「受控词表覆盖不足」;Assumptions 一条 |
| R2-Q5 遥测缺口 | **扩展 FR-009 增每回合最小遥测** | **FR-009 改写为两类记录** + **新增 FR-009a**(有界 + 保留窗口 + 可轮转 + 晋升计数为聚合态不由原始行重算);**新增 Key Entity 回合遥测**;晋升态实体补聚合态约束;SC-011/SC-012 Source 由"人工观察"改为指向自产遥测;**新增 SC-015** + Source;新增 Edge Case「遥测轮转与晋升计数」 |

**本轮发现并修复的两处规格缺陷**(不是新增取舍,是既有文本的错误):

1. **SC-011 / SC-012 无生产它们的 FR**——两条 SC 的 Source 引用"回合级观察记录",但 FR-009 只记录**发生了建议**的事件,静默回合零痕迹 → 两条 SC 的分母不存在、当时不可测。SC-011 恰是"按需升级"退化为"每回合跑脚本"的唯一护栏,不可测即等于无护栏。已由 R2-Q5 闭合。
2. **SC-008 只测 violations、未测 total 上限**——`tests/contract/test_confirmation_gates_sweep.py` 断言 `total ≤ baseline["total"] × 0.25`(baseline 取自需求 044),实测当前 total **23**、violations 0 → **整数余量为 0**;而 `scan-confirmation-gates.py` 的 `SCAN_ROOT_FILES=("templates",)` **覆盖 `templates/instructions-template.md`**,本特性文案天然是"建议/确认/询问"语义,极易命中 `BLOCKING_PATTERNS`。SC-008 已扩为"violations 0 **且** total 不超上限",Source 补 sweep 契约测试,并把该约束记入 `features/050.md` Implementation Notes 首条(待 plan 阶段优先复核)。

**append-only 不变式校验**:首轮 session 块 4 行**逐字保留**,本轮追加 5 行 + 1 行后置校验 → Clarifications 条目计数 **4 → 9**(严格递增);session 标题 1 → 2;无 Edit 覆盖历史。

**后置校验(程序复核)**:`NEEDS CLARIFICATION` 残留 **0**(余下 3 处字面量均为 FR-022/R2-Q2 对 `## Handoffs` 条件式的**引用**与一句元陈述,非占位符);`Need clarification` 残留 **0**;FR **26**(FR-001…FR-023 + FR-005a/FR-005b/FR-009a)、SC **15** outcomes + **15** sources 一一对应、Key Entities **7**、User Story **4**、Acceptance Scenario **32**、Edge Case **17**、一级章节 **8** 个顺序完好;Feature 索引 50 行 / header 50 / ID 1–50 连续唯一 / 详情文件 50 份 / `features/050.md` 占位符 0。

## Status

**All checklist items pass.** 无未决澄清项,`Related Feature` 已解析并完成全部注册义务。→ 可直接进入 **`/speckit.plan`**。

plan 阶段须优先处理的两项已记录在 `features/050.md` Implementation Notes:① **确认门控预算余量为 0** 且触发段落点在扫描范围内——措辞必须按非阻塞提示写,落地前复跑扫描器验证 total 未增;② 首轮三项裁定**不可拆分实现**(每回合评估的可负担性完全依赖近零默认证据预算)。
