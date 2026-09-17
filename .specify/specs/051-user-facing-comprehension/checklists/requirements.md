# Specification Quality Checklist: 面向用户可理解性纪律(User-Facing Comprehension)

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-09-17
**Feature**: [requirements.md](../requirements.md)

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

- Items marked incomplete require spec updates before `/speckit.clarify` or `/speckit.plan`

---

## Validation Record — Pass 1 → Pass 2 (2026-09-17)

### Content Quality — findings

| Item | Verdict | Evidence |
|------|---------|----------|
| No implementation details | **PASS** | 规格全文不指定语言、框架或 API。所有路径引用(`shared/guidelines/…`、`templates/…`、`scan-confirmation-gates.py` 的 `POLICY_DOCS`)是**既有工件的身份**,即本特性要改写的对象本身,不是实现选型。契约测试引用的是**既有测试文件的先例形态**(如 `test_one_source_of_truth.py` 的 `FORBIDDEN` 断言),用于说明守卫应对齐何种房子惯例,未规定测试框架或断言库。 |
| Focused on user value | **PASS** | 每个 User Story 均以读者的实际处境开篇(「用户在一个门控前停下」「一位用户在自己的项目里跑 init」),`**Why this priority**` 段以失效后果而非技术优雅度论证(「一个需要解码的提示换来的是自信地批准错东西」)。 |
| Written for non-technical stakeholders | **PASS** | 本规格自身遵守它所定义的纪律:每个内部标识符首次出现时附中文说明(如 `POLICY_DOCS`(策略文档豁免集)、`MUST include` 清单(强制包含的原则清单)、消费单元(comprehension obligation 的计账粒度));罗马数字/行号引用一律具名说明其为何相关。 |
| All mandatory sections completed | **PASS** | `Related Feature`(按命令约定保持 Need clarification)、`User Scenarios & Testing`(5 stories + 14 edge cases)、`Requirements`(36 FR + 9 Key Entities)、`Success Criteria`(16 SC + 16 Source)、`Shared Strings`(6 STR + 命名依据)、`Clarifications`(Session 2026-09-17,2 条)均已填充;模板占位注释与未用槽位已删除。 |

### Requirement Completeness — findings

| Item | Verdict | Evidence |
|------|---------|----------|
| No [NEEDS CLARIFICATION] markers | **PASS(Pass 2)** | Pass 1 曾有 2 处标记,均属**范围**类决策(优先级最高档)、多选解释并存且无显然默认,故按 `requirements-guidelines.md` 判据以表格形式一并提出而非猜测。二者已于 Pass 2 获用户裁定并记入 `## Clarifications` > `### Session 2026-09-17`:**R1-Q1=A**(界面类接入广度 → 全做,含两处搬家,FR-016)、**R1-Q2=C**(Principle XIV 既有缺口 → 一起修,并当双落点守卫的首个受测样本,FR-028 + FR-035)。**注**:全文仍有 2 处 `` `[NEEDS CLARIFICATION]` `` 字面命中(现状锚点第 43 行、FR-020),但二者均为**反引号包裹的标记名引用**——指 `requirements-guidelines.md:72-88` 所定义的那个提示模板本身,是本纪律要接入的对象;非活动标记。按文本检索判定标记残留时 MUST 区分二者。 |
| Testable and unambiguous | **PASS** | 36 条 FR 全部使用 RFC-2119 关键词且指向可核验对象,分 7 个主题组(真源与常驻可见性 / 行话侧程度 / 上下文侧程度 / 界面类扩散 / 下游导出 / 漂移守卫 / 观察与反馈)。程度类 FR 显式排除形容性表述:FR-007 规定「不能完全杜绝 jargon」MUST 落地为**可判定的许可条件**、MUST NOT 落地为「尽量少用」;FR-013 规定机械判据 MUST 使两个独立评审者得出同一结论。两处澄清裁定后 FR-016 / FR-028 已从开放选项变为确定义务。 |
| Success criteria measurable | **PASS** | 16 条 SC 全部带数值或可判定量:100%(SC-001/004/005/008/009/014/015)、0(SC-002/010/011/013/016)、1(SC-003)、≥90%(SC-006)、0%(SC-007)、≥20 条样本(SC-006)、不变(SC-012)。SC-003 / SC-012 / SC-015 各带实测基线(38 处 / 0 真源;18 条阻塞模式 / 0 措辞检查;`grep -c "One Source"` 在两个模板文件双双为 0)。 |
| Success criteria technology-agnostic | **PASS** | SC 全部以读者/评审者/项目视角表述(「一位本会话未打开过仓库的读者能…」「两位互不沟通的评审者…一致率 ≥90%」「新建下游项目…含原则的比例」),不引用框架、语言或数据库。SC-002/SC-003/SC-012 提及的检索与扫描是**既有工件的行为**,作为度量手段具名,而非技术选型。 |
| All acceptance scenarios defined | **PASS** | 5 个 story 共 26 条 Given/When/Then,均为具体状态转移而非重述 FR。含反向场景:US2-S5 断言既有判据**未被改写**且门控计数不变;US3-S4 覆盖下游拒绝该原则的路径;US3-S7 断言人为删除任一侧落点后 CI 失败;US5-S2 断言两条模式特有规则**原文保留**。 |
| Edge cases identified | **PASS** | 14 条,覆盖三类真实边界:① 白名单/黑名单的临界(无用户视角途径时、用户先用行话时、白话改写损失精度时、机器消费的消息);② 与既有纪律的冲突(下限 vs 非阻塞单行、下限 vs 摘要优先、每问注解 vs 不啰嗦);③ 静默失效路径(文档地图表加一行不生效、只改模板不改命令、嵌入契约不可丢弃清单未列指针、新增第 39 处表面自身成漂移点、194 个机械副本的手工批改诱惑)。 |
| Scope clearly bounded | **PASS** | `## Out of Scope` 13 条,逐条点名不属本特性的既有权威(门控是否触发的判据、Token 效率纪律、执行报告三要素定义、访谈模式其他规则、澄清既有形态裁定、词汇表机制、主动触发规则集),并显式排除任何新运行时机制(FR-033 同源)。 |
| Dependencies and assumptions identified | **PASS** | `## Assumptions` 14 条,含:命名与预留标识符核查结论、程度表达形态的选型依据(四种房子先例中为何取条件表 + 机械测试而非裸数值)、暴露通道的静默失效风险、镜像无需注册的实测依据、同批加守卫的不可拆分性、**接入广度已裁定(R1-Q1=A)**、**Principle XIV 回流已裁定(R1-Q2=C)**、宪章编号在模板(11→13)与活动宪章(14→15)不同属正常、版本递增 1.11.0→1.12.0、plan 门控自动传导 MUST 实测验证、US4 排 P2 的证据依据、输入模态、落地层级、待提交的术语提案。Pass 2 已删除两条被裁定取代的旧假设(「接入广度的默认倾向(待裁定)」「前车之鉴作为动机而非范围」),未留双份说法。 |

### Feature Readiness — findings

| Item | Verdict | Evidence |
|------|---------|----------|
| All FRs have clear acceptance criteria | **PASS** | 36 条 FR 分为 7 个主题组(真源与常驻可见性 / 行话侧程度 / 上下文侧程度 / 界面类扩散 / 下游导出 / 漂移守卫 / 观察与反馈),编号 FR-001..FR-036 连续无缺号(已机械核验),每条至少被一个 Acceptance Scenario 或一条 SC 的度量对象覆盖。守卫类 FR-029..FR-035 与 SC-009/010/012/013/015/016 一一对应;FR-036 由 SC-003 的观察标记约定覆盖。 |
| User scenarios cover primary flows | **PASS** | 5 个 story 覆盖用户显式提出的三项诉求:定义到 `shared/guidelines` 并设定程度(US1)、扩散到面向用户的流程含确认与 feedback(US2/US4/US5)、输出到下游 constitution 经模板与命令(US3)。优先级分布 3×P1 + 2×P2,未凑数亦未强行合并为三槽。R1-Q1=A 的全量裁定由 US5(收敛 + 两处搬家)与 US3(含 XIV 回流,S6/S7)承载,未新增 story 亦未留下未覆盖的裁定。 |
| Feature meets measurable outcomes | **PASS** | SC-003 的基线(38 处独立措辞 / 0 真源 / 0 统一名字)直接来自实现前实测,构成本特性的核心可验证目标;SC-001/002/013 覆盖用户点名的两片(门控、反馈);SC-005/015 覆盖下游导出与双落点守卫(含 XIV 回流的 0% → 100% 基线);SC-006/008 覆盖用户要求的「设定好程度」是否真的可判定;SC-016 覆盖 R1-Q1=A 选择最大接入广度所引入的回归风险。 |
| No implementation details leak | **PASS** | 规格不规定文档的节序、测试的组织方式、脚本的语言或再生机制的实现;凡涉及时均以「对齐既有先例形态」表述并指向该先例的路径,把选型留给 `/speckit.plan`。两处澄清裁定后,FR-016 与 FR-028 已由**范围**开放项转为确定义务,规格内不再有开放选型。 |

### Iteration summary

- **Pass 1(初稿)**: 15 / 16 项通过。唯一未通过项为 `No [NEEDS CLARIFICATION] markers remain`——2 处标记(FR-016 界面类接入广度、FR-028 Principle XIV 既有缺口处置)均属**范围**类决策(优先级最高档)、多选解释并存、无显然默认,故按 `requirements-guidelines.md` 的判据以表格格式一并提出等待用户答复,而非自行猜测。其余 15 项无需改写,未触发改写迭代。
- **Pass 2(裁定回写)**: 用户答复 **R1-Q1=A**(全做,含两处搬家)、**R1-Q2=C**(一起修,并当守卫样本)。回写动作:① 两处答案记入 `## Clarifications` > `### Session 2026-09-17`;② FR-016 / FR-028 的标记替换为裁定义务并附裁定依据;③ 新增 **FR-035**(双落点守卫一般化,以 XIV 为首个受测样本),原观察类 FR-035 顺延为 **FR-036**;④ 新增 **STR-006**(XIV 原则名,逐字取自活动宪章 `:155`,已实测核对);⑤ SC-004 去掉分批条件式、SC-005 增列 XIV 的 0% → 100% 基线,新增 **SC-015**(双落点守卫覆盖率与变异式有效性)、**SC-016**(两处搬家的既有行为回归数为 0)及各自的 Source;⑥ US3 补两条验收场景(S6 下游收到 XIV、S7 删除任一侧落点即 CI 失败)并更新其叙述与 Independent Test;⑦ Overview 差异表的「下游导出」「漂移守卫」两行更新;⑧ Key Entities 的「宪章原则导出」「漂移守卫」两条更新;⑨ Assumptions 删除两条被裁定取代的旧假设,新增两条已裁定假设并更新宪章编号假设。**结果:16 / 16 项全部通过。**
- **计数机械核验(Pass 2 后)**: FR 36(FR-001..FR-036 连续)、SC 16、SC Source 16、STR 6(全部被引用)、Key Entities 9、User Story 5、Acceptance Scenario 26、Edge Case 14、Out of Scope 13、Assumption 14、FR 主题组 7。
- **活动标记残留**: 0。全文 2 处 `` `[NEEDS CLARIFICATION]` `` 字面命中均为反引号包裹的**标记名引用**(指 `requirements-guidelines.md:72-88` 定义的提示模板本身,即 FR-020 要接入的对象),非活动标记——见上文该行证据。
- **`Related Feature: Need clarification`** 按命令约定视为 pending,由 `/speckit.clarify` 依 Feature Binding Rules 解析,不计为本清单的失败项。
- **下一相就绪**: 无活动标记 ⇒ 可直接进入 `/speckit.plan`;但因 `Related Feature` 仍为 Need clarification,按命令 Handoffs 约定应先经 `/speckit.clarify` 完成 Feature 绑定。
