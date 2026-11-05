# Requirements Specification: 机制/策略分离（Mechanism–Policy Separation）

**Requirement Branch**: `082-mechanism-policy-separation`
**Created**: 2026-11-05
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "优化所有的命令和技能, 需要为所有的命令和技能制定一个原则:机制和策略分离, 采用能力和职责分开的模型, 从"机制"和"能力"这个层面定义逻辑,算法,步骤等, 这套逻辑是归档到skills目录. 从"策略"和"职责"这个层面定义 配置,输入,输出等,这套逻辑是归档到具体的运行环境(如 用户指定的目录,当前工作目录, .specify目录等). 当一个命令或者技能执行时需要同时具备这两方面信息才能进行真正的执行,如果不明确需要提示用户提供. 需要注意的是:这个需求是针对元技能和命令的, 也就是这个原则是落入到 skills/external/create-skills,skills/external/improve-skills 等等用来操作其他命令和技能的流程中, 而不是针对当前项目中加载的这些技能."

> **本行的由来（自用声明）**：标题区两行类别字段先行自用。判定依据见 § Assumptions A1：本特性交付的是一等原则的 owner 文档、元技能/元命令的强制条款与守护测试，缺陷最先以机器面暴露（owner 缺失、元流程未拦住误置、守护测试对违规注入不转红），故按 `.specify/shared/definitions/flow-class-definitions.md` § 判据属 `execution`；`Flow Type` 写 `-`。**本阶段不改任何框架源**——元技能正文与命令模板的落地属 plan/implement 阶段义务。

## Related Feature *(mandatory)*

**Feature ID**: Need clarification
**Feature Name**: Need clarification

（按 create-requirements 技能约定，绑定推迟到 `/speckit.clarify`；本规格不自建 Feature。）

## Assumptions（本阶段的缺省裁决；clarify 阶段可推翻，翻转须给出证据）

- **A1（类别 = `execution`，basis = behavior-oracle）**：验收对象是 owner 文档的可判定性、元流程的拦截行为与守护测试的红绿，都是机器/程序可判的事实；同一原则在技能正文里呈现为 Markdown 不参与判定（owner §不参与判定的因素）——凡以「介质是 Markdown」主张 `expression` 的读法不予采纳。
- **A2（原则的名字：沿用既有 canonical 术语，不新造）**：本节一律称 **机制/策略分离 (Mechanism–Policy Separation)**，其中「机制」聚合用户原话的「机制/能力」两词、「策略」聚合「策略/职责」两词。依据是 `.specify/memory/glossary.md` 已登记 canonical 词 **机制修复 (Mechanism Fix)** 及其 owner §1 对 **机制 (Mechanism)** 的定义（「稳定产生/维护该类工件或行为的流程载体」），该定义已把「流程载体」而非「某次产物」立为机制。本特性**不重定义**该词，只在其上增加一条**相反方向的归档边界**（机制住 skills 目录、策略住运行环境）；两处不是同一事实，故不构成第二 owner（§ Constraints C6）。**变体收敛**：「能力/职责分开」按 § Terminology 映射到两个 canonical 词，不另行登记为独立术语。
- **A3（运行环境侧「落点」由既有路径约定承载，不发明新键）**：运行环境侧已经有两个既有区分：`${SKILL_HOME}`（技能自有资源）与 `${SKILL_WORKDIR}`（运行时/用户面向路径，定义在 `skills/external/create-skills/SKILL.md` § 2/§ 3）。「策略归档到运行环境」= 落在 `${SKILL_WORKDIR}` 侧或被这些约定指名的外部位置（用户指定目录、当前工作目录、`.specify/`），**不新增第三个环境变量、不新增配置键**。这一点同时回答了「闭包是否覆盖 `references/`」：`references/` 是技能自有资源、随技能分发，属机制侧。
- **A4（脚本是双重身份，按输入来源分层）**：`scripts/` 里的脚本原则上属机制，但一个脚本的**输入参数、输出落点、退出码契约**属策略。默认裁决：判据落「脚本的**逻辑**属机制、**参数与落点**属策略」，于是 `runtime-mode.md` 这类文档模板落在机制侧、脚本的 `--out <dir>` 落在策略侧。二者不一致时按内容判、不按文件名判。
- **A5（消费侧义务的实现载体 = 一条共享 workflow 文档，不新建命令、不新建校验器）**：消费侧「识别策略缺失并提示」需要一个唯一形态；本特性的落点是 owner 文档的一个章节，由元技能与元命令以路径引用，不在每个命令里各写一份提示语。**不新增 `/speckit.*` 命令**（与 077 对 069 的同类边界一致）。
- **A6（探针位置 = `improve-skills` 与 `create-skills` 的自检步骤，不新增独立脚本）**：作者侧「误置探针」落在元技能既有步骤里（`create-skills` § 6 校验、`improve-skills` § 8 最终检查），理由是这两处已经在做「规范符合性」判定，加一条判定不需要新机器。若 plan 证明书面判定不可判定，再决定是否抽成确定性脚本，**本阶段不预设脚本**。
- **A7（范围收紧的落地含义）**：用户原话以「优化所有的命令和技能」开头，末句又明确「针对元技能和命令……而不是针对当前项目中加载的这些技能」。本规格按末句执行：**交付面是元层**，对既有 15 个 external 技能与 38 个 internal 技能**零回溯改造**。任何把本原则一次性套到既有技能正文上的做法都越界。
- **A8（Feature 绑定）**：`Related Feature` 保持 `Need clarification`；候选复核见 § Constraints C7，由 `/speckit.clarify` 裁决新建或绑定。
- **A9（现状锚点，dated record，仅作可行性输入）**：`skills/external/create-skills/SKILL.md` 已有「Storage location options」「`${SKILL_HOME}` / `${SKILL_WORKDIR}` path conventions」「Content NOT to include」三段，但**没有**把「逻辑/算法/步骤 vs 配置/输入/输出」立为判定边界；`improve-skills` § 5 有「Keep `SKILL.md` a contract」「Codify deterministic logic」两条相邻规则，但判的是「该放 SKILL.md 还是 references/scripts」，**不是**「技能 vs 运行环境」；`merge-skills`、`coaching-skills` 无任何相关内容。即：现有规则解决**技能内部**的归档问题，本特性补的是**技能外部**（技能 ↔ 运行环境）的归档问题。此读数是 as-of 2026-11-05 的实测，不构成运行时保证。
- **A10（完成收尾的就地修复，2026-11-05 记录）**：requirements 的完成收尾 pass 只做三件事——(i) 把 FR-001 / FR-017 中被反引号包裹的 `[[STR-001]]` / `[[STR-003]]` 改为裸露引用（validator 只在代码 span 外识别 `[[STR-nnn]]`，否则双向 `ref-resolvable` 报 4 条）；(ii) FR-001 原句把「机制侧/策略侧的成员枚举」写进了正文，而 § Terminology 的同一枚举是 A2/C6 明写的 dated record、owner 定稿后不再跟踪——两处枚举相同即违反 FR-015 自己要求的「owner 唯一、其余以路径引用」，故把枚举从 FR-001 移出、改由 FR-002(a) 的判据派生，属对已记录意图的纠正（单一读法、局部可逆、不改判据）；(iii) 本假设行。判据取值、Shared Strings 值、`Consumed by` 单元格与 `Related Feature` 均未改动。

## Terminology（本规格内两层的判据口径）

> 术语的 canonical 名与语义归 `.specify/shared/definitions/mechanism-policy-definitions.md`（本特性新建的 owner，见 FR-005）。本节只声明**本规格在判别时用哪一句话**，plan 阶段 MUST 把这句话迁入 owner 并在 owner 中定稿；本规格 MUST NOT 成为该定义的第二个 owner。

| 用户原话 | 本规格用词 | 一句话判别口径（待 owner 定稿的候选，本阶段只作判定依据） |
|---|---|---|
| 机制、能力、逻辑、算法、步骤 | **机制 (Mechanism)** | 换一个运行环境仍然成立的那部分：判定规则、算法、步骤顺序、可复用方法。**判据**：把运行环境换掉，这段文字要不要改？不要改 → 机制 |
| 策略、职责、配置、输入、输出 | **策略 (Policy)** | 只在某个具体运行环境成立的那部分：路径、目标目录、交付物落点、输入来源、输出形态、运行模式绑定。**判据**：换掉运行环境，这段文字必须改 → 策略 |

**判定的两个可观测方向**：给定一段内容，若其去向改变而读者问「为什么该改」答不出运行环境，归机制；若答得出运行环境，归策略。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 作者在新建技能时被强制区分两层，误置当场被拦下 (Priority: P1)

一名作者通过 `create-skills` 新建一个技能。流程走到收尾时，技能必须回答两个问题：「哪些内容是这个技能的机制」「这个技能要把策略读自/写到哪个运行环境」。若作者把某个运行环境的绝对路径或某个用户目录名写进了技能正文，流程必须把它标为误置并给出改正方向，而不是静默通过。

**Why this priority**: 用户原话的落点是「落入 `skills/external/create-skills` 等元流程中」。没有这一条，原则只是一篇文档。这是唯一能让原则**在新资产上自动生效**的路径。
**Independent Test**: 在一个沙箱里用 `create-skills` 造一个故意把 `C:\Users\<me>\out\` 写进 `SKILL.md` 主体的技能，观察流程是否在收尾前点名该行并要求改正；再用一个正确分层的技能跑同一流程，确认不误报。两条都能独立观察，且不改动任何既有技能。

**Acceptance Scenarios**:

1. **Given** 一个新建技能把运行环境路径（用户指定目录、当前工作目录硬编码形态）写进了 `SKILL.md` 主体，**When** 作者走到 `create-skills` 的收尾校验，**Then** 流程输出一条可定位的误置判定（点名文件与行），并说明该内容应改落到策略侧的哪一处，且不得报告完成。
2. **Given** 一个新建技能把「判定规则/步骤顺序」整段写进了 `references/runbook.md` 之外的用户目录说明，**When** 作者走到收尾校验，**Then** 流程同样给出机制误置判定（可复用逻辑不应住在运行环境的说明里），并指明应迁回技能自有资源。
3. **Given** 一个正确分层的技能（机制在其自有资源，策略以参数/输入约定表达），**When** 作者走到同一收尾校验，**Then** 流程给出通过判定，不产生误报，也不要求作者补充任何内容。

---

### User Story 2 - 改进技能时，被引用的运行环境文件先与技能正文对账再判改进方向 (Priority: P1)

一名作者通过 `improve-skills` 改进一个既有技能。改进流程已经有「读全文」的步骤；本特性要求它在读运行时，MUST 把被引用的运行环境文件（输入、输出、配置、目标目录）与技能正文一起看成同一份契约，并说明「策略在哪里取值」。当某个策略来源不存在或说不清时，流程必须把它作为候选改进项提出来，而不是把当前技能里的某个硬编码值当成默认策略。

**Why this priority**: `improve-skills` 是既有技能进入本条原则的唯一通道。缺了它，原则只对新技能生效（US1），对存量技能永久失效——而用户明确禁止回溯改造存量正文，对账通道是唯一的替代。
**Independent Test**: 取一个引用了外部输入文件、但正文里写死了该文件默认路径的测试技能，跑 `improve-skills`，观察候选清单里是否出现「策略来源不明」一项，且改进方向是「改为提示用户提供」，而不是「保留默认值」。

**Acceptance Scenarios**:

1. **Given** 一个技能的正文把某个输入路径写成了固有值，且该路径指向运行环境，**When** 作者用 `improve-skills` 改进它，**Then** 该问题出现在候选改进清单里，条目点名违反的是「策略落运行环境」一侧，给出的方向是让策略在运行时由用户/环境提供。
2. **Given** 一个技能的两层已经分开（机制在正文，策略以输入约定表达），**When** 同一流程运行，**Then** 不产生该侧的任何候选条目，候选清单与改动前的基线相比不因本原则而增加。
3. **Given** 一次批量改进（用户点名一组技能），**When** 流程运行，**Then** 本原则的判定以一次批量口径执行，不为每个技能重复一遍同一判定。

---

### User Story 3 - 消费侧：策略缺失时以统一形态提示，而不是猜 (Priority: P2)

任何命令或技能真正开跑之前，都要同时拿到机制与策略两份信息。当策略侧缺失或含糊（比如「输出到哪」没说、目标目录不存在、输入文件未给），流程 MUST 以**一条统一形态的提示**向用户索取，并且 MUST NOT 用技能里的某个默认值顶替、MUST NOT 静默按当前目录落盘。

**Why this priority**: 这是用户原话「如果不明确需要提示用户提供」的直接兑现。它排在 P1 之下，因为它的落地形态（一条共享提示契约）需要先由 US1/US2 的作者侧判定建立起「什么算策略缺失」的口径。
**Independent Test**: 用一个不带输出目录参数、正文也无默认值的测试技能跑一次，观察输出是否是「一条点名缺失项 + 请用户提供」的提示，且没有任何文件被写到任一路径；再补上该参数跑同一技能，观察是否正常产出。

**Acceptance Scenarios**:

1. **Given** 策略信息缺失（目标目录未提供），**When** 命令或技能即将执行副作用，**Then** 流程在写任何文件之前停下并输出统一形态提示，点名**缺的是哪一个策略项**，并给出用户可以照做的提供方式。
2. **Given** 策略信息含糊（用户给了一个相对路径且当前工作目录不明确），**When** 流程判定，**Then** 走同一个提示形态，明写歧义点，而不是默认选当前工作目录。
3. **Given** 两层信息齐备，**When** 流程执行，**Then** 不产生任何提示，行为与改动前逐字节一致。

---

### User Story 4 - 同族元技能与元命令的成员裁定是封闭的、可复算的 (Priority: P2)

用户点名了两个元技能并要求「同族候选由 requirements 阶段按同一谓词裁定」。本故事交付的是**裁定结果 + 谓词**：哪些流程属于元层、哪些不属于，以及为什么。

**Why this priority**: 范围不清就必然回溯改造存量技能。成员表是一份"不得越过"的边界，而不是新增能力。
**Independent Test**: 把裁定表交给第二个人，让他仅凭表中的谓词对 `skills/external/` 下任一技能做一次归属判定，他得出的结论与表中一致。

**Acceptance Scenarios**:

1. **Given** 裁定谓词与成员表，**When** 另一个人对任一 external 技能独立判定，**Then** 结论与表一致（含被排除者及其排除理由）。
2. **Given** 一个**被排除**的技能（例如只服务于某个具体产物的技能），**When** 本特性落地完成，**Then** 它的正文未被本特性改动（零回溯改造）。

---

### Edge Cases

- **内容两边都沾（既是算法又要读配置）**：按「换掉运行环境要不要改」逐段拆开；拆不开时按 § Terminology 的两个方向各判一次，冲突记为待澄清而不是任选一边。
- **技能自己就是「运行环境」的一部分**（例如 `sdd-loop-driver` 往 `.specify/state/` 写状态）：写状态**这一动作的规则**是机制，**写到哪个根**是策略——后者已由 `shared/guidelines/directory-governance.md` § 5 登记，本特性 MUST NOT 新增第二个根。
- **策略缺失发生在读取侧而非写入侧**（输入文件不存在）：同样走统一提示形态，但不得把「文件不存在」与「没说要读哪个文件」混成一条——前者是环境错误，后者是策略缺失。
- **standalone 部署没有 `.specify/`**：策略的合法取值随之收窄（例如 `.specify/` 不是候选）；提示形态不变，候选集合由运行模式决定。
- **跨语言的同一内容**（中文标题 + 英文正文）：按内容判，不按语言判；双语表述本身不构成机制内容。
- **元命令的「模板」与「正文」**：命令模板 `templates/commands/*.md` 的步骤属机制；它指向的运行环境路径属策略；两者在同一个文件里时仍按行判。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 原则本体与两层的判定 (US1, US4)

- **FR-001**: 框架 MUST 拥有一条一等原则「机制/策略分离」（英文名 [[STR-003]]），声明机制侧与策略侧的归档面，且该原则 MUST 有唯一 owner 文档；两侧的成员由 owner 文档按 FR-002(a) 的判据派生并声明，本规格不列举。
- **FR-002**: owner 文档 MUST 给出**双向可用的边界测试**，至少覆盖：(a) 「换掉运行环境这段文字要不要改」的二值判据，并以它机械派生两侧成员表——本规格只把它写成一句判别口径（§ Terminology），成员枚举属 owner 文档，不在此重述；(b) **误置的两类症状**——机制住进运行环境（可复用逻辑散落在用户目录/运行说明里）与策略写死进机制（运行环境路径、目录名被固化进技能自有资源），每类各给出至少一条可观测表现。
- **FR-003**: owner 文档 MUST 明确两层**不必在同一文件内分开、但在语义上必须可分开**：同一条目可以同时含两层内容时，判定按内容逐段进行，MUST NOT 以「文件名/目录名」代替内容判定（与 § Assumptions A4 一致）。
- **FR-004**: owner 文档 MUST 把「机制层落在技能资产（技能定义本体及其 `references/`、`scripts/`、`assets/`）」「策略层落在运行环境（用户指定目录、当前工作目录、`.specify/` 等）」写成**归档规则**，并 MUST 说明该规则与 `shared/guidelines/directory-governance.md` 的关系是引用而非复制（后者仍拥有目录能否存在这件事）。

#### B. 执行时的双输入与缺失提示 (US3)

- **FR-005**: 一个命令或技能 MUST 同时具备两层信息才可执行；MUST NOT 以某种「机制默认值」顶替缺失的策略，MUST NOT 静默挑选默认落点（含当前工作目录）。
- **FR-006**: 当策略缺失或不明确时，执行流程 MUST 以**统一形态**向用户索取；该形态 MUST 至少承载三件事：缺失/含糊的是哪一个策略项、为什么此刻需要它、用户可照做的提供方式。形态 owner 唯一，其余位置以路径引用。
- **FR-007**: 判定 MUST 区分「策略缺失」（没说要哪一份）与「环境错误」（给了但取不到），二者的提示形态可以共用、但措辞与后续动作 MUST 可区分。
- **FR-008**: 双输入检查 MUST 发生在**任何副作用之前**（尤其写文件、建目录、删改）；缺策略时流程的停止不得留下半成品。

#### C. 落点范围：元层封闭集 (US4)

- **FR-009**: 本原则 MUST 落入**元技能/元命令**——「用来操作其他命令与技能的流程」——并至少覆盖 `skills/external/create-skills` 与 `skills/external/improve-skills`。
- **FR-010**: 同族候选的纳入裁定 MUST 以**一条谓词**机械判定（谓词见 § Constraints C1），并输出**封闭的成员表 + 排除理由**；成员表 MUST 可被第三方按同一谓词独立复算（US4 独立测试）。
- **FR-011**: 本特性 MUST NOT 回溯改造当前项目中已加载的技能（`skills/external/` 与 `skills/internal/` 下除成员表所列元技能以外的全部技能，正文零改动）；MUST NOT 新增 `/speckit.*` 命令。

#### D. 作者侧义务 (US1, US2)

- **FR-012**: 创建流程（`create-skills`）MUST 在既有收尾校验中新增一条**机制/策略分离检查**，至少判定：技能正文是否把运行环境路径/目录名固化为机制、可复用逻辑是否落在了运行环境说明里；判定 MUST 可定位（点名文件与位置）且禁止「只给结论」。
- **FR-013**: 改进流程（`improve-skills`）MUST 在其调研/候选清单阶段新增一条同源判定，并把「策略来源不存在或说不清」列为**候选**改进项；MUST NOT 把技能里现存的硬编码值当作默认策略继承。
- **FR-014**: 合并流程（`merge-skills`）与教练流程（`coaching-skills`）MUST 各按成员表裁定的结果接入原则：纳入者新增一条判定；排除者 MUST 在成员表中写明不纳入的理由。

#### E. 规范合规与产出 (所有)

- **FR-015**: 本特性的全部新增事实 MUST 遵守 One Source of Truth：owner 唯一、其余以路径引用；MUST NOT 在元技能正文里复制 owner 的判据表或词表。
- **FR-016**: 本特性 MUST NOT 建立第二套分类数据文件、第二套门禁、或第二个目录根；任何新增目录/owner 文档 MUST 在同一趟完成登记（`directory-governance.md` § 3、`framework-map.md`）。
- **FR-017**: 本特性交付的 `requirements.md` MUST 在 `## Related Feature` 之前携带且仅携带一行类别声明（[[STR-001]]），取值域由 `.specify/shared/definitions/flow-class-definitions.md` § 特性线声明面 拥有。
- **FR-018**: 术语命名 MUST 沿用既有 canonical 术语（§ Assumptions A2），MUST NOT 为「机制」「策略」两个已知词另立第三套名字；用户原话中的「能力/职责」按 § Terminology 映射收敛。

### Key Entities

- **机制侧内容 (Mechanism Content)**：判定规则、算法、步骤顺序、可复用方法。归属：技能资产。属性：换掉运行环境仍成立。
- **策略侧内容 (Policy Content)**：路径、目标目录、交付物落点、输入来源、输出形态、运行模式绑定。归属：运行环境。属性：换掉运行环境必须改。
- **误置 (Misplacement)**：两层内容落到对侧归档面的状态。两类症状（机制误置、策略误置），见 FR-002(b)。
- **元层成员表 (Meta-layer Membership)**：按 C1 谓词判定的封闭技能/命令集合 + 排除理由。它是裁定结果，不是新注册表——落点见 C6。

### Runtime Stack & Dependency Ownership（082 自身的运行时栈表）

本特性交付的运行时能力是框架自身的镜像/命令副本再生成（RS-004，`in-scope`）；其余四项由外部供给、本仓只消费，按 FR-009 的判据记 `signed-contract`——它们是 SC-002 的独立复算与 SC-003 的漂移守卫得以执行的运行时前提，不以散文声明替代表行。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | Python 3 解释器（运行契约测试与任何确定性检查） | signed-contract | CPython 上游（本仓只消费） | `requires-python >= "3.8"`（`pyproject.toml` 已声明，不新增 pin） | `pyproject.toml` | 本特性新增/改动的守卫测试在 `>=3.8` 解释器上通过，且新增脚本 stdlib-only（静态 import 清单为空） | FR-010, FR-016 | EP-001 |
| RS-002 | pytest（守卫测试运行器） | signed-contract | pytest 上游（本仓只消费） | 无声明 pin；执行时以 `pytest --version` 原文记录进 test-evidence | `scripts/bash/run-tests.sh` | 基线差集为空（`head 失败集 − 基线失败集`）且新增守卫测试全绿 | FR-010, FR-016 | EP-001 |
| RS-003 | `git`（SC-003 的逐字节比较与漂移守卫） | signed-contract | git 上游（本仓只消费） | 无声明 pin；执行时以 `git --version` 原文记录进 test-evidence | `scripts/bash/common.sh` | `git diff --stat [[STR-002]]..HEAD -- skills/ templates/commands/` 与逐字节比较可复现；审计前后 `git status --porcelain` 增量为空 | FR-015, FR-016 | EP-001 |
| RS-004 | 本仓的镜像与命令副本再生成（`sync-mirrors.py` / `regen-command-copies.py`） | in-scope | 本仓 `scripts/python/` | 仓内 commit（同一次提交） | `scripts/python/sync-mirrors.py` | `python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/regen-command-copies.py --check` 均 exit 0 | FR-016 | EP-001 |
| RS-005 | 受支持的 agent 宿主（加载并执行元技能流程，用于 SC-002 的检出/误报测量） | signed-contract | 各受支持 agent 工具上游（本仓只消费） | 无声明 pin；执行时以宿主名 + 版本原文记录进 test-evidence | `docs/reference/cli/supported-agent-tools.md` | 同一误置样本在改动前/后各执行一次纳入的元技能流程，检出记录与误报记录原文落 test-evidence；宿主与版本同趟记录 | FR-012, FR-013 | EP-002 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对给定的 N 条待判定内容（机制/策略混合样本），由**两位独立判定者**仅凭 owner 文档判定，结论一致率达到 100%（分歧即判据不可判定）。**Path**: final
- **SC-002**: 被纳入的元技能（成员表全量）在创建/改进流程中，对「故意误置样本」的检出率为 100%，对「正确分层样本」的误报数为 0。**Path**: final
- **SC-003**: 成员表之外的全部既有技能与全部既有命令模板，其正文相对本特性基线提交 [[STR-002]] **逐字节未变**；比较口径与允许差异集按 `.specify/shared/guidelines/closed-set-claims.md` 的五要件声明（允许差异集按产物类声明并配漂移守卫）。**Path**: final
- **SC-004**: 策略缺失时，零个文件被写到任何路径（副作用前停止）；补齐策略后同一输入产出与改动前逐字节一致。**Path**: final
- **SC-005**: 一个未参与本特性的读者，仅凭 owner 文档能正确回答「这段内容该归哪一层」不少于 owner 文档附录给出的全部样例。**Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**：本特性 test-evidence 目录下的一次双判定人样本运行；判定人按 § Assumptions A1 的独立上下文协议（fresh-context read-only）执行；样本集与两份结论同趟落盘，重跑即复算。
- **SC-002 Source**：按 SC-002 的两个样本各跑一次纳入的元技能流程；证据 = 流程输出的检出/误报记录原文。基线 = 改动前同一流程对同样的正确分层样本的输出（应同样零误报）。
- **SC-003 Source**：`git diff --stat [[STR-002]]..HEAD -- skills/ templates/commands/` 与逐字节比较脚本；比较单元与被排除路径由漂移守卫钉住（见 FR-016 与 closed-set-claims § 要件 3）。
- **SC-004 Source**：沙箱内跑一次缺策略的执行，前后各取一次目录快照比较；补齐后再跑取输出哈希。
- **SC-005 Source**：owner 文档附录的样例题 + 一次读者作答记录（可复算：同一题集重测）。

## Constraints（落地约束；判据 owner 在外部，此处只引用）

- **C1（元层谓词，FR-010 的唯一判据）**：一个流程属于元层，当且仅当**它的产出改变另一命令或技能的定义/行为**。由此：`create-skills`（产出新技能）、`improve-skills`（产出变更后的技能）、`merge-skills`（产出合并后的目标技能并下线源技能）纳入；`coaching-skills` 的产出是「观察到的偏差 + 微调计划」，它**本身不改写**受训技能——按逐字谓词判为**不纳入强制检查**，但因它派发受训技能的真实执行（消费侧形态），按 FR-014 的「排除者写理由」处置；`/speckit.skills` 命令按其路由表**转发**给上述元技能，故它作为**命令面**随成员表一并声明接线位置，不新增第二套判定。**本表是 requirements 阶段的裁定结果；plan 阶段若改谓词，MUST 重算全表并在 plan 中记录，MUST NOT 只改一行。**
- **C2（既有 owner 不做第二 owner）**：`shared/definitions/dogfooding-definitions.md` § 1 拥有的是「机制 vs 问题」的修复方向；本特性拥有的是「机制 vs 策略」的归档面。两者共享「机制」一词但事实不同；落 plan 时 MUST 在 owner 文档开头声明它**拥有些什么**，并 MUST 以路径引用 dogfooding owner 而不复制其定义。
- **C3（`${SKILL_HOME}` / `${SKILL_WORKDIR}` 是既有约定）**：定义在 `skills/external/create-skills/SKILL.md`；本特性 MUST NOT 复制该定义，也 MUST NOT 新增第三个路径占位符。
- **C4（目录治理）**：新 owner 文档落 `shared/definitions/`（既有目录，非新目录树）；若最终需要新目录，MUST 同趟登记 `.specify/shared/definitions/framework-map.md` 与 `directory-governance.md` § 2。**本特性不新增任何目录根。**
- **C5（Token 效率）**：元技能的检查新增 MUST 以「一行判定 + 指向 owner 的路径」形态落地，MUST NOT 把判据表嵌入多个元技能正文；判定步骤若为固定规则，plan 阶段优先考虑确定性程序。
- **C6（一源）**：`§ Terminology` 在本规格内是**判定口径**（dated record，属允许的“dated record”类重复），owner 定稿后 MUST 从 owner 引用，本规格不随之更新——本规格冻结于 2026-11-05。
- **C7（Feature 绑定候选复核，交 clarify）**：已有 Feature 中与「元技能/元命令」相关的候选需按 `feature-integration.md` § Feature Binding Rules 复核——本阶段**不预判**归属，只登记复核义务；绑定结果 MUST 进入 `## Clarifications`。
- **C8（不建立第二套门禁）**：本特性的作者侧检查挂接在元技能**既有**校验步骤里；MUST NOT 新增独立门禁命令、独立检查脚本或第二套清单（与 § Assumptions A6 一致）。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `**Flow Class**: execution` | FR-017；本文件头部；`flow-class-check.py --action lookup --unit-id "spec:082-mechanism-policy-separation"` |
| `STR-002` | `3ffeb26e` | SC-003（基线提交）；test-evidence 的 stage-status 行 |
| `STR-003` | `Mechanism–Policy Separation` | FR-001；owner 文档标题；术语表登记 |

**Citation convention**: 引用时写 `[[STR-NNN]]`；本文已在上列位置使用该形式。

## Clarifications

<!-- 由 /speckit.clarify 填充，格式：- Q: <question> → A: <answer> -->
