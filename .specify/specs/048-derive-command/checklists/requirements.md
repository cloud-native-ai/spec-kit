# Specification Quality Checklist: 推导式架构生成(Derivation Command)

**Purpose**: Validate specification completeness and quality before proceeding to planning
**Created**: 2026-09-05
**Feature**: [requirements.md](../requirements.md)
**Concept authority**: `shared/definitions/derivation-definitions.md` — 四套记录 schema、四级溯源等级、C1–C7、A1–A14、封闭禁用论证集与能力降级规则的唯一真源。本清单只判定「需求是否忠实**引用**它」,不复述其任何表或规则。

## Content Quality

- [x] No implementation details (languages, frameworks, APIs) — 出现的引擎名/动作名/退出码属本仓「命令自带 stdlib 引擎」的**交付面契约**(同 045→047 惯例),未规定模块结构、类名或算法
- [x] Focused on user value and business needs — 价值主张为「可被独立读者重放的推导」而非「文献摘要」;每个 US 的 Why-this-priority 段给出它在价值链上的位置
- [x] Written for non-technical stakeholders — 技术性特性,按本仓惯例(045/046)用领域语言 + 英文字段名
- [x] All mandatory sections completed — Related Feature / User Scenarios & Testing / Requirements / Success Criteria 齐备;Key Entities 因涉及数据而保留

## Requirement Completeness

- [x] No [NEEDS CLARIFICATION] markers remain — 零标记;六条 Clarifications 全部带裁定结论与日期
- [x] Requirements are testable and unambiguous — 38 条 FR 均有可判定主体(见「FR 可测性」);首轮列出的三处枚举/证据面欠指定已随概念锚修正与 FR-001/FR-004/FR-009/FR-014/FR-029 改写而闭合(见 Notes)
- [x] Success criteria are measurable — SC-001..006 全为计数 / 比率 / 退出码判定,无「显著改善」类措辞
- [x] Success criteria are technology-agnostic — SC 只引用引擎 JSON 输出与既有扫描器,不指定实现手段
- [x] All acceptance scenarios are defined — 5 + 5 + 10 + 6 = 26 条 Given/When/Then,覆盖四条 US
- [x] Edge cases are identified — 10 条(重复 URL、标题党、快照截断、付费墙、探活未能运行、回音壁、手工编辑算子库、slug 重名、来源事后降级、预算触顶)
- [x] Scope is clearly bounded — 独立 `## Out of Scope` 节(六条:语料不随包分发、`probe-links` 非爬虫、不改用户源代码、不替代 Plan、不做特性级调研、`.specify/derive/` 非镜像对),与 Clarifications 第 1 条、概念锚 §Derivation vs Research vs Plan 互不重复 → Notes N-5 已闭合
- [x] Dependencies and assumptions identified — 依赖面为概念锚、probe 注册表、framework-map、门控扫描器与测试基线;假设以 SC-006 的六项基线数字显式落地

## User Story Independence(每个 US 可独立测试)

- [x] US1 可独立验收 — 固定四类语料一次落地即可断言四行的 `access` / `resolved_via` / `grade` / `title_mismatch` 与 `## Unverifiable Sources` 收录;不需要算子库或链存在
- [x] US2 可独立验收 — 同主题两次顺序运行,断言重复 `move_id` = 0、重复归一化 `inference_form` = 0、第二次 `stats` 的 reused/reinforced > 0;输入只需已落地的来源表
- [x] US3 可独立验收 — 以来源表 + 算子库 fixture 建链断言 `validate` 退出码 0;四类缺陷注入各自断言退出码 4 且错误信息定位到规则编号;不依赖 US4 的接线
- [x] US4 可独立验收 — fixture 产物上的 `validate` JSON(`semanticChecksPending` 恰为 A11/A14)+ 四个契约面断言;不需要一次真实推导
- [x] 优先级与依赖序一致 — P1(地基)→ P1(方法层)→ P1(交付物)→ P2(可信与接线);US1 失守则 US2/US3 不成立已在 Why 段说明,不存在循环依赖

## FR 可测性与实现中立

- [x] 每条 FR 有可判定主体 — 引擎判定(FR-002/003/005/013/014/018/019/020/022/026/027/028/029/030/032/033)、契约测试(FR-012/015/016/034/035/036/037/038)、agent 语义责任(FR-004 的等级判断、FR-010/011/021/023/025 的语义半)
- [x] 机械/语义半分界诚实 — 含语义成分的规则(C4/C5/C6/C7、A11/A14)只钉「引擎拒绝其**退化形态**」,未假装整条规则可程序化判定
- [x] 无实现泄漏 — 未出现内部数据结构、类名、第三方库或算法选择;`probe-links` 的离线容错(FR-033)是对可观测行为的要求,不是对实现的要求
- [x] FR 之间无相互矛盾 — FR-004(仅前两级可锚定)与 FR-007(降级时全部 unverified、可锚定步骤数为 0)一致;FR-024(预算触顶如实报告)与 FR-023(终止条件显式声明)互补而非重叠

## 概念锚一致性(引用而非复述)

- [x] 四套 schema 未在需求内重列字段语义 — Key Entities 每条只给一句用途 + 属性名清单,字段含义指向锚
- [x] C1–C7 / A1–A14 / 等级与 `access` / `resolved_via` / 算子 `status` 各枚举按锚引用 — FR-017..FR-025 逐条标注规则编号,FR-029 引用 [[STR-002]];需求侧不复列任何取值集(首轮曾复列「六态 / 四值」计数,已改为引用)
- [x] FR-036 显式确立锚为唯一真源,并要求命令模板、引擎 docstring、词汇表与用户文档**引用而非复述**
- [x] 封闭禁用集按 [[STR-001]] 引用,需求正文零复列字面量;扩充须同改锚与引擎(FR-019)
- [x] 枚举可达性已闭合 — 锚修正后 `access` / `resolved_via` 的每个取值都有产生路径(无产生路径的 `not-found` 与 `publisher-index` 已删除);`paywalled` 分支与「探活未能运行 → `unknown` + `unverified`」分支由 FR-001 承载,`unknown` → `grade: unverified` 的强制耦合由 FR-004 承载 → Notes N-1 已闭合
- [x] A13 有可判定证据面 — FR-029 把 A13 钉为「本次运行报告为新发放的每个算子都解析到库中的一行」,即它经 `moves-add`(唯一写入者)落库;执行面见 `contracts/derivation-model.md` C-40/C-41 → Notes N-2 已闭合

## Shared Strings 纪律

- [x] 八条 STR 全部以 `[[STR-NNN]]` 引用,正文零复列字面量 — STR-001(FR-019/SC-004)、STR-002(FR-029/FR-030/US4 AS1)、STR-003+STR-004(FR-032)、STR-005(FR-034/US4 AS4)、STR-006(FR-012/FR-016/FR-038/Key Entities/Out of Scope)、STR-007(FR-007/US1 AS5/SC-005)、STR-008(FR-023/FR-024/FR-029 的 A12 半/US3 AS7)
- [x] 每条 STR 的 Consumed by 列齐备(FR + 契约文件 + 引擎常量 + 测试),plan 阶段可一对一落地
- [x] 引用约定在表下显式声明,防止后续产物退回复写字面量

## SC 可度量性与度量源

- [x] 六条 SC 一一对应 Measurement Sources 条目,且各自指明采集时机与基线 — SC-001/SC-004 基线 0;SC-006 基线为门控 total 23 / probe internal 72 / 复杂命令分类 18 / docs-step 分类 15 / 全套件 50 条既有失败
- [x] 度量源为既有机制而非新建仪表 — 引擎 `validate` / `stats` 的 JSON、`feedback-utils.py --action probes --validate|--reconcile`、`scripts/python/scan-confirmation-gates.py --json`、`run-tests.sh --names-out` 与 `baseline-failed.txt` 的名字级差集
- [x] FR→SC 覆盖完整 — FR-036(唯一真源)/ FR-037(分发中性)/ FR-038(framework-map 新行)已由扩写后的 SC-006 承载,各自有可判定计数(根相对锚引用数 ≥ 1 且含字面 `never restate`、复述命中数 = 0;两文件真实域名与编号命中数 = 0;framework-map 中 `.specify/derive/` 行数 = 1),度量源见 SC-006 Source → Notes N-3 已闭合
- [x] SC 与 US 独立测试互不重复计数 — SC-001/SC-005 落在 US1、SC-003 落在 US2、SC-002/SC-004 落在 US3、SC-006 落在 US4,无一条 SC 缺乏可执行入口

## 用户裁定可追溯性(Clarifications → FR)

- [x] 裁定 1「重点是学思维方式、构建推导链路、逐步形成完整架构」→ FR-009/FR-010(算子非结论)、FR-017..FR-028(链与架构)、FR-029/FR-030(A14 语义背书)
- [x] 裁定 2「必须联网核实来源」→ FR-001..FR-003、FR-006/FR-007、FR-033;SC-001/SC-005
- [x] 裁定 3「走完整 SDD 特性流程」→ 过程性裁定,由本 spec 目录的产物集与 `.specify/memory/features/049.md` 的 Status Tracking 承载,无需 FR
- [x] 裁定 4「产物落项目级推导档案」→ [[STR-006]]、Key Entities「Derivation Archive」、FR-038(新存储根登记进布局真源)
- [x] 裁定 5「算子跨运行累积为项目级库」→ FR-012..FR-016、[[STR-006]]、SC-003
- [x] 裁定 6(设计裁定)「真实语料不随框架分发」→ FR-037(分发文件客户中性、示例槽位化合成)

## Feature Readiness

- [x] All functional requirements have clear acceptance criteria — 38 条 FR 全部可映射到 26 条 AS 或 SC 度量;原三条纪律型要求(FR-036/037/038)已由 SC-006 的三项计数直接承载,不再只靠既有守卫测试间接覆盖
- [x] User scenarios cover primary flows — 落地 → 抽取 → 建链组装 → 自审与接线,覆盖命令全生命周期
- [x] Feature meets measurable outcomes defined in Success Criteria
- [x] No implementation details leak into specification
- [x] Related Feature 已解析 — Feature 049(判定为新 Feature),归属裁定与候选拒绝理由见 `../feature-ref.md`

## Notes

- **N-1(枚举可达性,阻塞 plan 前澄清)**:`access` 六态中只有 `live` / `wayback:<ts>` / `dead` 由 FR-001 的三级次序产生,`unknown` 由 FR-033 的网络错误产生;`not-found` 与 `dead` 的区分、`paywalled` 的判定入口、以及 `resolved_via: publisher-index` 的产生路径均无 FR 承载。同时,「`access: unknown` 是否强制 `grade: unverified`」未定义 —— 这直接决定 FR-004 的锚定门控在网络故障时的行为。
- **N-2(A13 证据面)**:A13 被划为引擎判定,但需求未规定 `moves-add` 留下任何可事后核验的写入痕迹;若仅靠行形/ID 单调性推断,则「手写了一行形式完全合法的算子」不可检出。plan 阶段须在引擎契约里钉死判定依据,或把 A13 降为 agent 背书项。
- **N-3(SC 覆盖)**:FR-036/FR-037/FR-038 属纪律型要求,建议 plan 阶段以既有守卫测试(shipped-surface 中性扫描、framework-map 行存在性)作为其度量源补进 SC-006,而非新立 SC。
- **N-4(算子库 `status` 语义)**:FR-009 的 `status`(new/reused/reinforced)是**运行相对**语义,而 FR-012/FR-016 要求它是项目级单表里**一行一列**的持久状态且 `superseded` 永存;SC-003 又从 `stats` 而非该列取度量。同一列同时承载「本次运行处置」与「算子持久状态」在语义上冲突 —— 见 `../data-model.md` §2 的建模说明。
- **N-5(范围节)**:需求以 Clarifications 第 1 条排除四种误读、以概念锚的对照表划清与 Research / Plan 的边界,实质范围是闭合的;缺的只是一个显式 Out of Scope 节。建议 plan 前补一节,把「不做文献摘要、不做特性级调研、不引用 Plan、不随包分发真实语料」四条集中列出。
- **N-6(跨作用域身份)**:`M-<nnn>` 为项目级、`S-<nnn>` 为**每主题**发放(FR-014 vs 锚 §Source Record),而算子的 `anchor` 指向 `S-<k>` 且无主题限定 —— 项目级库里的 `anchor: S-003` 跨主题不可解析。需求未规定限定形式,详见 `../data-model.md` 身份语法节的未决项。
- 第 1 轮验证:41 项通过 / 4 项未通过 —— 三个概念锚与度量面缺口(N-1 枚举可达性、N-2 A13 证据面、N-3 FR→SC 覆盖)加一个结构缺口(缺显式 Out of Scope 节,N-5);另 3 项(N-4 算子库 `status` 语义、N-6 跨作用域身份、以及 `--force` 重脚手架对既有档案的处置)为记录在案的建模观察,不构成需求缺陷但须在 plan 阶段裁定。
- **第 2 轮闭合记录(2026-09-05,概念锚修正 + 设计裁定后;上方 N-1…N-6 原文保留为首轮记录,不再代表现状)**:
  - N-1 → 锚删除无产生路径的 `access: not-found` 与 `resolved_via: publisher-index`,新增付费墙分支与「探活未能运行 → `unknown`」分支;FR-001 承载两分支,FR-004 钉死 `unknown` → `grade: unverified`。
  - N-2 → A13 钉为「本次运行报告为新发放的每个算子都解析到库中的一行」(FR-029;执行面 `contracts/derivation-model.md` C-40/C-41,库侧留痕为引擎写入标记 + 独写者约束)。
  - N-3 → SC-006 扩写,FR-036/037/038 各得一项可判定计数,度量源写进 SC-006 Source。
  - N-4 → `status` 收窄为**持久**二值 `active`/`superseded`;`new`/`reused`/`reinforced` 改为 `moves-add` 与 `stats` 输出的**运行相对处置**,不再是库列(FR-009;`contracts/move-library.md` C-17/C-18;`data-model.md` §2)。
  - N-5 → 新增 `## Out of Scope` 节(六条),位置按 046/047 惯例置于 Shared Strings 之后、Clarifications 之前。
  - N-6 → `anchor` 采用点号命名限定形式 `<topic-slug>.S-<nnn>`(FR-014;`data-model.md` ID-3;`contracts/move-library.md` C-6/C-20),`--force` 的内容处置由 `contracts/derive-engine.md` C-12 裁定为「备份 `.bak` 后重脚手架」。
- 第 2 轮验证:45 项通过 / 0 项未通过 —— 首轮 4 项未通过全部闭合,3 项建模观察全部由锚或契约裁定;仍开放的两项属**设计层**而非需求层,记录在 `../data-model.md` §未决建模项(`Q-<k>` 无消解状态、同主题重跑对 `derive.md` 是覆写还是增补)。
