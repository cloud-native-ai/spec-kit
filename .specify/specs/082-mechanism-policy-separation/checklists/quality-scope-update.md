# Requirements-Quality Checklist: 元技能治理：机制/策略分离与技能引用归一化（082 scope update）

**Purpose**: 判本特性**需求文本本身**的质量——两层归档边界是否可判定、五消费方接线是否各有唯一 owner 引用、归一化三值输出与失败语义是否闭合、quickstart 14 场景与 SC-001…SC-009 的分母是否可复算。**不判实现是否通过**；每一项的答案是一句关于需求/契约文本的判断，任何需要「跑一下产品才知道」的项都不属本清单。
**Created**: 2026-11-05（`/speckit.checklist`，checklist 阶段；scope update 后）
**Depth**: Standard（维度全覆盖、按风险优先级）· **Audience**: Reviewer（规格评审者 / 实现者 / 后续 clarify 裁决者）
**Feature (Requirement Scope)**: `.specify/memory/features.md` Feature 082（`Draft`）· [`.specify/specs/082-mechanism-policy-separation/requirements.md`](../requirements.md)
**Requirements (What)**: [requirements.md](../requirements.md)——条款 id 面：FR-001…FR-030 / SC-001…SC-009 / STR-001…STR-005
**Specifications (How, context only)**: [plan.md](../plan.md)、[tasks.md](../tasks.md)、[data-model.md](../data-model.md)、[contracts/](../contracts/)、[quickstart.md](../quickstart.md) — **只用于发现缺项、歧义、冲突与追溯断点**，不判它们自身写得对不对
**Readers**: 规格评审者（判断 082 的需求是否可据以实现，以及哪些缺口必须在实现前由谁裁决）、实现者（把这份清单当作实现前的自检面）；两者都具备本仓 SDD 语汇
**Reading scenario**: 在 `/speckit.analyze` 与 `/speckit.implement` 之前逐项作答；每一项要么给出「已定义 + 出处」，要么登记为缺口并指明裁决阶段
**Sibling**: [`checklists/requirements.md`](./requirements.md) 是 requirements 阶段的质量清单（本文件**不覆盖、不重复**它的判定项）；本文件只判 scope update 之后两个能力合流的**跨条款质量**。

> **逐项纪律**：每项是**问题** + 维度标签 + 追溯引用（`[Req §…]` / `[Gap]` / `[Ambiguity]` / `[Conflict]` / `[Assumption]` / `[Dependency]`）。`[Req §X]` 指 requirements.md 的小节；`[Plan §…]` / `[Contracts §…]` / `[DataModel §…]` / `[QS §S…]` / `[Tasks §…]` 指 How 侧产物，仅用于暴露需求缺项。**行号与计数一律不写进本文件**（按设计在本仓会漂移），只写路径与条款 id；凡计数都指向机器读数。

---

## A. 完整性 —— 两个能力的条款面是否齐备（Completeness）

- [ ] CHK001 是否有一条 FR 规定：某一侧信息缺失时**如何发现、在哪里发现、发现后向谁报告**（而不只是「MUST 提示用户」）？[Completeness, Req §FR-005/§FR-006]
- [ ] CHK002 是否有一条 FR 规定**消费侧改动的载体**——共享提示形态住在唯一 owner、元技能只带路径引用——且同时给出「既有技能正文零回溯改造」时的**可达性**论证（新形态如何到达存量技能的执行路径）？[Completeness, Req §FR-009/§FR-011, Assumption §A5]
- [ ] CHK003 「修正后重跑」路径是否被写成需求：作者改正误置后，元技能给出 `pass` 的**依据**是什么（同一判据复查，还是另起一次判定）？[Completeness, Gap；DataModel §SM-1 给出了状态，需求侧未落到 FR]
- [ ] CHK004 机制/策略原则在**哪些产物类型**上生效是否穷举：技能正文之外的技能自有资源（`references/` / `scripts/` / `assets/`）、命令模板正文与镜像层，是否各有明确的「生效 / 不生效」裁定？[Completeness, Req §Edge Cases 第 6 条, Assumption §A4]
- [ ] CHK005 两个能力各自要求「owner 文档必须在开头声明拥有什么 / 不拥有什么」，但**所有权声明本身**是否也要求一条变更记录条目（谁在何时改了文法或判据）？[Completeness, Gap, Req §FR-019；Contract §OD-10]
- [ ] CHK006 单条内容**同时命中两层的误置**（既写了运行环境路径、又住了可复用逻辑）判定顺序是否规定：先报机制误置、先报策略误置，还是两条都报？[Gap, Completeness]
- [ ] CHK007 「五个消费方」这个集合本身是否被定义成**封闭**（可以增长吗、增长时改哪一处）？[Completeness, Req §FR-026/§FR-029]
- [ ] CHK008 当 `/speckit.skills` 与同名技能**同时存在**时，「两类对象一并报告」的报告项是否被列明（同 FR-024 四类失败那样逐项可核对）？[Completeness, Req §FR-023(b)/§Edge Cases]

## B. 清晰性 —— 判据与术语是否无歧义（Clarity / Ambiguity）

- [ ] CHK009 「换掉运行环境这段文字要不要改」这一二值判据是否点明由**谁**来问（作者 / 执行流程 / 独立判定者），以及在 `待澄清` 情形下由谁裁决？[Clarity, Req §Terminology/§Edge Cases 第 1 条]
- [ ] CHK010 「统一形态」是否被定义为**字段封闭的结构**（三件必需项 + 明确禁止的第四项），从而「统一」不是「大致一致」？[Clarity, Req §FR-006；DataModel §E-5 给出恰 3 项，需求侧未写死「恰」]
- [ ] CHK011 「可定位」是否规定了最小可核对项（文件 + 位置 + 引文），使「给出一条可定位的误置判定」可以被第三方逐项核对？[Clarity, Req §FR-012, US1 场景 1]
- [ ] CHK012 「归一化后的标识」是否规定了**允许的字符面与形状**（名称就是一个名字；名字里保留 `.md` 是否合法）——否则两个实现都可以自称「符合」？[Ambiguity, Req §FR-021/§FR-030, §Clarifications ① 第 6、11 条]
- [ ] CHK013 owner 文档的**文件名**本身是否被当作事实：需求以 `skill-reference-definitions.md` 与 `Mechanism–Policy Separation` 两处以不同方式指同一份 owner，文件名/标题是否是需求的一部分？[Ambiguity, Req §Shared Strings STR-003/STR-004]
- [ ] CHK014 「策略来源不存在或说不清」是一个**二值**判定还是两档（不存在 / 说不清各一种候选条目）？[Ambiguity, Req §FR-013；Tasks §T013 Checkpoint（US2）]
- [ ] CHK015 「零命中」「路径越界」「目录无 `SKILL.md`」「两层不同命中」四类**互斥**是否由需求文本给出判定优先顺序（一个输入同时满足两类时归哪一类）？[Ambiguity, Req §FR-024/§SC-009]
- [ ] CHK016 「元技能」是否被定义为**流程**而非**路径**（`run-skills` 住在 `skills/internal/` 而其余在 `skills/external/`）？[Clarity, Req §Constraints C1；Plan §D3 已按真实路径修正，需求侧只按流程裁定]
- [ ] CHK017 「双向可用的边界测试」是否点明两向各是什么，且两向的合格条件各自可判？[Clarity, Req §FR-002]
- [ ] CHK018 「输出形态」允许两种（名称 / 路径 + 层级）：**哪一种用于哪类输入**是否被规定，还是由每个消费方自选？[Ambiguity, Req §FR-021/§FR-030]
- [ ] CHK019 「命令面」判定与「技能标识」判定是否各有**一个**可观察的区分特征（而不是「按情况判断」）？[Clarity, Req §FR-023(b)/§FR-030]
- [ ] CHK020 「镜像层与其安装副本属于同一技能」的**层**是否被定义（层 = 源树与 `.specify/` 运行时的两处，还是「层 = 每个宿主工具」）？[Ambiguity, Req §FR-023(c)/§Edge Cases]

## C. 一致性 —— 条款之间与跨产物之间是否互相打架（Consistency / Conflict）

- [ ] CHK021 双能力共用的「元层谓词」（C1）与「五消费方接线」（FR-026）：前者把 `run-skills` / `coaching-skills` 判为 `excluded`，后者要求这两份 `SKILL.md` 必改——需求文本是否明写这两条**各管一面**，还是需要读者自己消解？[Conflict, Req §Constraints C1 vs §FR-026；Plan §SU-01 已裁，需求侧未回写]
- [ ] CHK022 两份 owner 的**文件名**在需求中以字面出现（`skill-reference-definitions.md` / `mechanism-policy-definitions.md`），是否与 plan/契约中的 owner 路径及标题串（`STR-003` 的英文标题）保持同一拼写？[Consistency, Req §Shared Strings vs §Assumptions §A11；Contracts §OD-01]
- [ ] CHK023 SC-007 的**允许差异集**（三类：owner 自身 / owner 生成镜像 / 既有测试字面量）与「五消费方各恰一条源路径引用」是否相容：消费方的引用串若被扫描面计入，是否构成第四类允许重复？[Conflict, Req §SC-007 Source]
- [ ] CHK024 `coaching-skills` 同时被要求「不得出现机制/策略字面」（SW-05）与「是引用侧必改消费方」（SR-06），且其「真实改写仍经 improve-skills」通道句必须保留——三者是否在需求文本内一致（而不必读者去 plan 求证）？[Consistency, Req §FR-014 vs §FR-026；Contracts §SW-05/§SR-06]
- [ ] CHK025 需求把「接受形式集合」定为封闭六项，而 §Edge Cases 说「接受形式会增长」——增长路径（一次 owner 修订）是否与 FR-029 的「零新增」边界在同一段里不冲突？[Consistency, Req §FR-020/§Edge Cases/§FR-029]
- [ ] CHK026 FR-021 说归一化「MUST 不含被剥掉的前缀/后缀」，§Clarifications ① 第 8 条又说「保留原值不得成为第四种结果」——需求是否在**一处**给出这两条的统一表述（剥什么、留什么）？[Conflict, Req §FR-021/§Clarifications ①]
- [ ] CHK027 两个能力「零新增」清单（命令 / 门禁脚本 / 目录根 / 环境变量 / 第二套分类文件）是否在机制/策略侧与引用侧**各写一遍**，两处是否一致、是否构成一条边界的两个 owner？[Consistency, Req §FR-011/§FR-016 vs §FR-029]
- [ ] CHK028 引用文法侧把「按名称解析哪个位置优先」交出去给 `run-skills` § 1，而 `run-skills` 自身是消费方之一（必改）——需求是否说明**改动消费方不得改动该阶梯**的可判形态？[Consistency, Req §FR-022 vs §FR-026；Contracts §SR-01]
- [ ] CHK029 「归一化 MUST NOT 要求交互」与消费侧「策略缺失 MUST 提示用户」是否在需求内被明写为两条**不同**交互面，而非同一开关的两种说法？[Consistency, Req §FR-021 vs §FR-006]
- [ ] CHK030 FR-017 要求类别声明「且仅携带一行」：该条在 scope update（文件长度、章节增删）之后是否仍然可判，其**判据 owner** 是否被需求点名？[Consistency, Req §FR-017]

## D. 可测性 —— 每条 SC 是否真的量得出来（Measurability）

- [ ] CHK031 SC-001 的 N 与**判定者协议**是否由需求给出（同一位判定者的两次运行算不算两位）？[Measurability, Req §SC-001/§SC-001 Source]
- [ ] CHK032 SC-002 的「检出率 100% / 误报 0」分母（哪些元技能 × 哪些样本）是否由需求给出固定数量，还是由成员表事后决定？[Measurability, Req §SC-002/§SC-002 Source]
- [ ] CHK033 SC-007 的「恰一条引用」在「一份引用覆盖两个参数」的消费方（`merge-skills` 的 Source/Target）上如何计数，需求是否点明？[Measurability, Req §SC-007；Contracts §SR-04]
- [ ] CHK034 SC-006 的「≥ 12 个输入」与「覆盖六种形式 + 变体」是否足以覆盖 SC-008 / SC-009 的正负例与四类失败，还是三条 SC 各需自己的行数下限？[Measurability, Req §SC-006 vs §SC-008/§SC-009]
- [ ] CHK035 SC-009 的「不串味」是否给出一个可判的形态（每条断言的互斥字段），而不只是「MUST NOT 互相串味」？[Measurability, Req §SC-009]
- [ ] CHK036 SC-008 的「至少 1 条负例」是否规定负例的**选型标准**（同形但非命令 / 同前缀但非命令），以免负例选成「随便一个不存在的名字」？[Measurability, Req §SC-008]
- [ ] CHK037 SC-003 / SC-007 的包含性声明是否各自**独立**写足五要件（基线参照物 / 比较单元 / 允许差异集来源 / 补集断言 / 聚合词清零），且两条不共用一要件？[Measurability, Req §SC-003/§SC-007 Source；owner `shared/guidelines/closed-set-claims.md`]
- [ ] CHK038 SC-004 的「零个文件被写到任何路径」是否规定了**观察面**（目录快照含哪些根、含不含临时目录与缓存）？[Measurability, Req §SC-004/§SC-004 Source]
- [ ] CHK039 SC-005 是 `supporting` 路径：「不少于附录给出的全部样例」意味着 100%，那为什么不干脆写成 `final`——需求是否说明该标注的判据？[Measurability, Req §SC-005/§path-marker]

## E. 可追溯性与分母可复算（Traceability & Denominator）

- [ ] CHK040 每条 FR 是否都能追到一个 US、一个 SC 或一条 Constraints 条款（反向亦然）——尤其 FR-001 与两个 owner 的「拥有/不拥有声明」是否各有至少一条 SC 兜底？[Traceability, Req §Functional Requirements/§Success Criteria]
- [ ] CHK041 quickstart 的 14 个场景**逐个**是否有判据（命令 + 判据 + Predicates/Premises），且每个 `deferred` 场景是否点名它依赖的前提与**闭合者**（哪条 FR / 哪个任务关闭它）？[Traceability, Req §SC-006/§SC-007；QS §S1–§S14]
- [ ] CHK042 quickstart 的 `deferred` 场景是否每个都能追到一个 SC 或一个 EP（例如 S6→SC-004、S7→SC-002、S8→SC-001/SC-005、S11→SC-006、S12→EP-007(a)）——是否存在无人认领的场景？[Traceability, Gap, QS §Scenario table]
- [ ] CHK043 SC 的分母是否**全部**指向机器读数（附录题集条数、fixture 行数、扫描分母、接线份数），而没有任何一条分母仍写作「成员表全量」「全部既有」「按附录」这类**未定量**表述？[Measurability, Req §SC-001…§SC-009；DataModel §E-7/§GM-13]
- [ ] CHK044 定性判据（命中 / 未命中、一致 / 不一致、可达 / 不可达）的**取值域**是否在各处一致写为二值或三值，没有被「基本一致」「大体可见」这类档位稀释？[Measurability, Req §SC-001…§SC-009]
- [ ] CHK045 「清单 / 矩阵 / 登记表」类载体是否都有**一个**需求侧指名的真实落点（而不是「由 plan 决定」），使第三方按同一分母复算时知道该打开哪个文件？[Traceability, Req §FR-030/§SC-006 Source]

## F. 范围边界 —— 哪些不做是否可判（Scope Boundary）

- [ ] CHK046 「零回溯改造」的边界是否可机械判定：哪些文件属于「存量技能正文」（按成员表 / 按目录 / 按一切非成员），以及镜像层是否在边界内？[Boundary, Req §FR-011/§SC-003]
- [ ] CHK047 「不新增门禁脚本」与「把判定挂进元技能既有步骤」的边界是否可判：既有步骤里**新增一行判定**算不算新增门禁？[Boundary, Req §Constraints C8/§FR-016]
- [ ] CHK048 「不新增目录根」是否与「本文允许把新夹具/参考资料放进既有根下的新子目录」相容——需求是否给出「根」与「子目录」的判据来源？[Boundary, Req §Constraints C4/§FR-016]
- [ ] CHK049 「不新增环境变量 / 配置键」在 standalone 部署下是否仍成立（无 `.specify/` 时运行模式如何得知）？[Boundary, Assumption, Req §Assumptions §A3/§Edge Cases 第 4 条]
- [ ] CHK050 用户原话「优化所有的命令和技能」与末句「针对元技能而非当前项目技能」的范围矛盾，需求是否在**正文一处**显式裁定而非只在 Assumptions 里说明？[Conflict, Req §Assumptions §A7]

## G. 边界条件 —— 边角情形是否写进需求（Edge Cases）

- [ ] CHK051 章节目录名本身就是一个被操作对象时的情形（`skills/`、`shared/` 等**目录名**被当作技能名输入）是否定为一类结果？[Edge Case, Req §Edge Cases]
- [ ] CHK052 `run-skills`「名字可省扩展名」与归一化「不剥 `.md`」的冲突，需求是否给出**唯一**消解（而非只写「owner MUST 消歧」）？[Conflict, Req §Clarifications ① 第 11 条/§Edge Cases]
- [ ] CHK053 归一化收到空串 / 纯空白 / 只有前缀（`/`、`@`、`skill:`）时归哪一类，需求是否点名？[Edge Case, Gap, Req §FR-024]
- [ ] CHK054 策略侧「用户给了一个**相对路径**」与「策略缺失」是否被明确分成两种结果，且各自的后续动作可区分？[Edge Case, Req §US3 场景 2/§FR-007]
- [ ] CHK055 当两个消费方在一次流程中**嵌套调用**（例如 `coaching-skills` 派发受训技能执行）时，策略检查与归一化各在**哪一层**执行一次，需求是否说明？[Edge Case, Req §FR-023(d)/§Edge Cases]
- [ ] CHK056 两个 owner 同时缺席（尚未创建）时，五个消费方的判定与归一化应表现为「失败关闭」还是「跳过」，需求是否说明？[Edge Case, Gap, Req §FR-024]

## H. 风险与依赖（Risks & Dependencies）

- [ ] CHK057 「起点 = 工作树中的未提交实现」这一前提的**失效路径**是否被写成需求：若起点与规格冲突，实现者保留起点还是以规格为准，各自的判据是什么？[Dependency, Assumption, Req §Assumptions §A11/§FR-027]
- [ ] CHK058 「以相对框架根解析源路径」这条安装态前提是否被需求写成**可验断言**（而不是「应当解析得到」），并为不可解析的情形留出裁决点？[Dependency, Assumption, Req §Clarifications ② standalone 段；Plan §EP-007(a)]
- [ ] CHK059 「所有容器都按 owner 正文现场归一化」是否是一条**依赖**（每个宿主执行体是否照做只有实测能证明）——需求是否显式登记这一「测试证明过程可复算、不证明执行体照做」的缺口？[Dependency, Gap, Req §SC-006…§SC-009]
- [ ] CHK060 词表登记（canonical `机制/策略分离 (Mechanism–Policy Separation)`）作为跨特性共享的单文件注册表，其**登记义务**是否在需求里落到一条可追溯的条款（而不只在 plan 的 D9）？[Dependency, Req §Clarifications Session 2026-11-05 A2 条 vs §Shared Strings]
- [ ] CHK061 被改技能既有的体积预算债务（三份 `SKILL.md` 改动前已超预算）是否被需求承认为**既有债务**，从而不被误当作本特性的回归判据？[Dependency, Assumption, Req §SC-002；Plan §EP-003]
- [ ] CHK062 对既有能力组件（`run-skills` 的位置阶梯、目录治理、镜像模型）的依赖，是否在需求里以**路径引用**表达且明写「不拥有」？[Dependency, Req §Constraints C3/C9/§FR-022]

## I. 双语与术语（Bilingual Expression & Terminology）

- [ ] CHK063 本特性新增的 canonical 术语是否有且只有**一处** canonical 名与一处双语形态（`机制/策略分离 (Mechanism–Policy Separation)`），且其登记 status 与「已 ratified / proposed」口径一致？[Terminology, Req §Assumptions §A2/§Clarifications A2 条]
- [ ] CHK064 「机制」「策略」「能力」「职责」四个用户词组是否各自映射到明确的 canonical 词，且需求**不**把它们当作四个独立术语？[Terminology, Req §Terminology]
- [ ] CHK065 既有 canonical 词「机制修复 (Mechanism Fix)」与本特性「机制」的关系是否写成一条**不构成第二 owner** 的声明，且该声明在需求内可定位？[Terminology, Req §Assumptions §A2/§Constraints C2]
- [ ] CHK066 机制/策略两侧的成员词表是否**只**住在 owner，需求正文只保留一句判据口径并标注为 dated record？[Terminology, Req §Constraints C6/§Assumptions §A10]
- [ ] CHK067 技能标识的字面形态前缀（反引号包裹还是裸串）在需求侧是否有**一处**唯一结论——而不是「正文用反引号、契约扫描裸串」两种读法并存？[Ambiguity, Contract §GM-12 要件 4 的「归一化步骤字面与四类失败名」vs §GM-11 对 `[[STR-004]]` 的「恰好一条引用」；契约代码块形态未被需求声明为口径
- [ ] CHK068 「dated record」与「共享提示形态」两类正文的**豁免边界**是否互斥（同一段话不能既是 owner 的 dated record 又是消费方必须逐字携带的共享形态）？[Ambiguity, Req §Constraints C5/C6/§Assumptions A5]

## J. 目录与镜像治理（Directory & Mirror Governance）

- [ ] CHK069 两份 owner 是否各有唯一的落点类别（`shared/definitions/` vs `shared/guidelines/`），且该选择的判据被需求引用而非重述？[Governance, Req §Constraints C4/§FR-016]
- [ ] CHK070 新增 owner 文档与新增技能自有资源是否在同一趟完成目录登记（哪两处登记、各自登记什么），需求是否点名？[Governance, Req §FR-016]
- [ ] CHK071 「镜像层不得作为引用坐标」与「镜像层必须继续生成」是否在需求内被明写成**两条**不同义务（引用面 ≠ 镜像面）？[Governance, Req §FR-028/§Clarifications ②]
- [ ] CHK072 消费方引用**源路径**还是**运行时镜像路径**的口径，是否在需求中有一处**唯一**结论（而非「两种都可，看部署」）？[Governance, Req §Clarifications ②/§Shared Strings STR-004]
- [ ] CHK073 镜像与命令副本的「零漂移」判据是否只以 `--check` 的退出码表达，且需求未把任何文件**计数**钉成期望值？[Governance, Req §FR-028；Plan §Mirror Obligations]
- [ ] CHK074 临时产物与证据目录落点是否被需求约束到既有受管根（不新增临时根）？[Governance, Req §FR-016/§Constraints C4]

## K. One Source Of Truth（一源）

- [ ] CHK075 两份 owner 是否互相明写「不复制对方的表行 / 规则」，且「不复制」各有**一条**机械可判的形态（字符面零命中而非「应当不重复」）？[One Source of Truth, Req §Constraints C9/§FR-015]
- [ ] CHK076 需求内部自身是否存在同一事实的两处枚举（机制/策略成员、消费方名单、零新增清单），且每一处都有「dated record / 指向 owner」的豁免声明？[One Source of Truth, Req §Constraints C6/§FR-015]
- [ ] CHK077 Shared Strings 是否只登记会被**逐字消费**的字面量，且每个 STR 的 `Consumed by` 都能在仓内定位到消费点（含测试、契约、源）？[One Source of Truth, Req §Shared Strings/§Constraints C10]
- [ ] CHK078 「元层成员表」是否只住一处：需求只给谓词（C1）与裁定结果，owner 给成员表本体，二者是否互不复制？[One Source of Truth, Req §Constraints C1/§FR-010]
- [ ] CHK079 SC-006 的矩阵与 SC-007 的扫描各自断言什么是否互不重叠（矩阵 = 期望值，扫描 = 接线与复制面），需求是否点到两者的**唯一载体**？[One Source of Truth, Req §SC-006 Source/§SC-007 Source]
- [ ] CHK080 两份能力各自的「允许差异集」是否共用一个分母（而非按能力各开一张），需求是否明写这一点？[One Source of Truth, Req §SC-003/§SC-007；DataModel §GM-03]

## L. 两条已登记的 implement 义务是否在需求侧有对应检查点（Carried Obligations）

> 这两条来自 tasks 阶段登记的 `C3` / `C2`（见 `test-evidence/tasks-scope-update-gates.txt`），属**已知未闭合项**；本段只问「需求侧有没有对应的检查点」，不判实现。

- [ ] CHK081 **green-point 归属**：需求是否要求「每条 FR / 契约条款都有一个**可被机器解析**的绿点归属」，还是只要求「有测试载体」？若为后者，「测试存在」与「条款被覆盖」之间的差是否被需求显式承认？[Traceability, Gap, Req §FR-001…§FR-030]
- [ ] CHK082 **coverage baseline**：需求是否规定 FR→载体覆盖率的**基线来源**（冻结在哪个产物、由哪一阶段冻结），使「已覆盖」可被判而不只是手写矩阵？[Traceability, Gap, Req §SC-003/§SC-007]
- [ ] CHK083 这两条义务的**闭合阶段与责任人**是否在需求或 plan 中被点名（谁在 implement 收口时提供一份可复算的覆盖读数）？[Dependency, Plan §DoD/§Completion Gate；Tasks §C2/C3]
- [ ] CHK084 已登记的覆盖基线缺口（accountant 报 `baseline-missing`）与既有流程纪律冲突：本仓的契约面任务模板要求在**生成期**冻结 `coverage-baseline.txt`，而 082 的 tasks 阶段未产出该文件并把义务推给 implement——需求/契约是否声明「本特性有契约集，故不适用『无契约集可跳过』」？[Conflict, Gap, Req §SC-003/§SC-007；`.specify/skills/internal/create-tasks/SKILL.md` § Coverage baseline 义务]
- [ ] CHK085 契约条款的可解析性（条款 id 形态）是否被需求定为一项**前提**：若四份契约的条款形态使「行级绿点归属」不可解析，需求侧哪一条兜住「条款被覆盖」这件事？[Dependency, Req §FR-001…§FR-030；`.specify/shared/definitions/contract-clause-definitions.md`]

## M. 收口与验收断言是否被需求考虑（Closure Plan）**— 设计侧，非实现测试**

- [ ] CHK086 关停面（`verification.md` 的 `final` 路径行、smoke 三件套、closure 判定）是否被需求承认为本特性的**交付义务**——还是完全不提，留给 `/speckit.implement` 的流程默认值？若后者，需求的「验收」是否因此少了一条可追溯的落点？[Gap, Traceability, Req §Success Criteria/§SC-00N `**Path**` 标注]
- [ ] CHK087 smoke 是否可以由一条**确定性本地命令**充当（本特性无服务、无网络、无外部依赖）？需求是否写明了这个判断，使「smoke 不可确定性 ⇒ 特性被记为 finding」这条既有纪律在本特性上不至于被误触发？[Gap, Measurability, Req §Runtime Stack §RS-001…RS-005]
- [ ] CHK088 每个 `final` 路径 SC 的「pass」在**同一份**关停记录里是否有一个指名的读取面（而不是四散在各 `test-evidence/sc-*.txt`）？需求是否要求这一份汇总读数存在？[Gap, Measurability, Req §Measurement Sources]
- [ ] CHK089 需求的 `**Path**:` 标注（`final` / `supporting`）与验收纪律的取值域是否同一套（谁拥有这个域，需求是否引用而非自定）？[Traceability, Req §SC-005 `**Path**: supporting`]

## Notes

- **用法**：逐项作答；答「已定义」必须附出处（条款 id / 路径 / 章节锚）；答「未定义」即记缺口，并写明应在哪一阶段裁决（clarify / plan / implement / 下一轮 checklists recheck）。
- **作答形态**：本清单是**第一轮**（创建即未答）。按 `create-checklist` 技能的 recheck 规则，第二轮作答落**新文件** `checklists/recheck-<date>-<topic>.md`，逐条引原文；本文件不被就地刷新。
- **与 requirements 阶段清单的关系**：`checklists/requirements.md` 判的是「规格作为文档是否合格」；本文件判的是「两个能力合流后，跨条款的判据、分母、边界与一源是否仍然成立」。两文件的缺口项**互不替代**。
- **不写计数**：本文件不手抄 FR / SC / STR / 任务 / 场景的条数；任何计数的唯一权威是 `validate-requirements.py` 的输出与 `test-evidence/*-gates.txt` 的实测原文。
- **两份已知漂移（本清单不修，登记在此供评审者核对）**：① 需求侧条款把两份 owner 简称为 `mechanism-policy-definitions.md` / `skill-reference-definitions.md`，而 `STR-003` 的英文标题 `Mechanism–Policy Separation` 与 owner 文件名不同形——谁是 canonical 名、谁是主键，见 CHK013 / CHK022；② `STR-004` 的 owner 路径在需求中写作框架源路径，而起点实现里五份 `SKILL.md` 引用镜像路径——口径裁决在 §Clarifications ②，需求本身不留第二读法。**本清单只提出问题，不作裁决。**
