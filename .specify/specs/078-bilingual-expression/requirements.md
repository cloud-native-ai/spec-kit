# Requirements Specification: 双语表述（Bilingual Expression）

**Requirement Branch**: `078-bilingual-expression`
**Created**: 2026-10-30
**Status**: Draft
**Flow Class**: expression
**Flow Type**: technique-document
**Readers**: 框架维护者（编写与评审 `shared/`、`templates/` 文档的作者）、词汇表维护者、下游项目使用者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 判断一处概念/流程的定义行是否必须双语、其形态（方向/括号宽度/紧贴/用词）是否合规时打开本规格核对 FR-001…FR-018，并据其决定是否为 `/speckit.plan` 放行
**Input**: User description: "在当前项目中增加一个新的特性: \"双语表述\". 这个特性的主要内容是: 所有核心概念,关键流程在定义名词和动词的时候需要添加中英文双语的形式, 中文(English)或English(中文), 在之前的框架中已经包含了这一概念,很多核心文档也是这样实践的. 这样做的好处是在不同的context和大语言模型中能够\"锚定语义\", 避免因为名词或动词的错误理解造成语义错误."

## Related Feature *(mandatory)*

**Feature ID**: 078
**Feature Name**: 双语表述（Bilingual Expression）

**绑定结论**：绑定**新建 Feature 078**（`Draft`，2026-10-30 立项）；登记行与详情文件随本阶段落盘。**不**把本规格挂到任何既有 Feature 名下。

**reuse-first 复核（宪法 VII；判据是「该 Feature 是否已拥有本特性要建立的能力」，不是「是否持有交付载体」）**：

| 候选 Feature | 与本特性的关系 | 裁决 |
|---|---|---|
| 014 One Source of Truth | 拥有「唯一 owner + 指针不复制」的引用纪律；不拥有双语形态的任何规则（方向、形态、覆盖面、豁免） | 原则前序，不是归属 |
| 018 Grounded Naming | 拥有命名来源顺序（用户 > 项目惯例 > 同类兄弟）；不拥有术语的双语呈现规则 | 命名来源 ≠ 双语形态；无关归属 |
| Glossary / `.specify/memory/glossary.md` 机制 | 拥有术语的 Canonical/Variants 登记面；不拥有「定义处何时必须双语」的写作约定 | 是本约定的**消费方**（FR-005 以词汇表为准），不是归属 |
| instructions 生成机制（008 / `/speckit.instructions`） | 拥有 ambient 小节的分发载体（`templates/instructions-template.md` → `generate-instructions.sh` → `.specify/instructions.md`）；不拥有双语规则本体 | 载体 ≠ 归属；本特性对其做「摘要 + 指针」扩展（FR-011） |
| 069 执行/表达分类与文档型门禁 | 拥有特性线类别判据；本线按其判据自声明为 `expression`（理由见 § Assumptions A2） | 类别判据的引用方，不是归属 |

**新建理由**：仓内 grep `bilingual|双语` 于 `shared/`、`templates/`、`src/`、`scripts/` 零命中——该概念无 owner、无规则、无守卫；既有双语并置全部是自发实践（§ 现状锚点）。按宪法 VII 复核后无既有 Feature 拥有该能力，故新建。

## 现状锚点（2026-10-30 本机实测；dated record，仅作可行性输入，非运行时保证）

测量口径：`python3` 内联脚本扫描（`pathlib.rglob` + 正则，脚本文字描述见本表下方），范围 `shared/` + `templates/` + `.specify/`（排除 `.specify/specs/` 与 `.specify/history/`），共 2333 个 `.md` 文件。

| # | 测量项 | 实测 |
|---|--------|------|
| M-1 | 半角形态 `中文(English)` 的行长匹配总数 | 1609 |
| M-2 | 全角形态 `English（中文）` 的行长匹配总数 | 1383 |
| M-3 | `shared/`+`templates/` 中同一文件混用两种方向/宽度的文件数 | 32 |
| M-4 | `shared/`+`templates/` 仅用 EN-first（多为全角）的文件数 | 37 |
| M-5 | `shared/`+`templates/` 仅用 `中文(English)` 半角的文件数 | 2 |
| M-6 | `shared/`+`templates/` 完全无双语形态的文件数 | 31 |
| M-7 | 项目词汇表条目总数 / Canonical 已是双语形态（含括号）的条目数 | 161 / 132 |

**解读（三条可判定结论）**：

1. **概念存在但无规则**：双语并置遍布 2333 个文件中的逾百件，却没有任何文档声明何时必须双语、用哪种括号——形态完全自发。
2. **形态不一致（M-1 vs M-2）**：半角 `中文(English)` 与全角 `English（中文）` 并存且量级相当（1609 vs 1383），32 个文件内部混用——同一概念的锚定形式在两种宽度间漂移，正是本特性要消除的缺陷。
3. **词汇表已先行（M-7）**：132/161 条 Canonical 已双语化，说明「定义处双语」已被实践接受，缺的是把它写成可执行约定的 owner 文档。

M-1/M-2 为行长匹配聚合数（同一行多次出现会重复计数），作量级锚点使用，不作精确基线；M-3…M-7 为文件级/条目级精确计数。测量脚本（两枚内联 heredoc，可重放）：第一枚按「CJK…(ASCII) 半角」与「ASCII…（CJK） 全角」两枚正则逐文件累计；第二枚按文件统计方向/宽度共存关系，并解析词汇表行首 `|` 统计 Canonical 双语条目。

## Assumptions（对输入中开放点的缺省裁决，clarify 阶段可推翻）

- **A1（输入笔误更正，用户已裁决）**：原文「English(中问)」按「English(中文)」理解（`中问` 为 `中文` 的笔误，U0 入口声明已记）。
- **A2（Flow Class = `expression`，basis = reader-oracle；承重决策）**：按 `.specify/shared/definitions/flow-class-definitions.md` 两步判据——主交付物是双语写作约定的 owner 文档（`shared/guidelines/bilingual-expression.md`）；其缺陷最先在**读者面**暴露（作者写错方向/宽度、读者跨 context 误读锚点）。最强反题：交付物含被机器执行的确定性检查器，是否构成 mixed-oracle 改判 `execution`？裁决：否——形态检查器只是「结构 / 链接 / 构建」类检查，按判据「结构检查通过不构成充分条件、MUST NOT 参与判定」不改判；约定的最终验收由读者承担，检查器不签字语义。预期反指标：plan 阶段若把检查器升格为最终验收 oracle，须 re-baseline 改判 `execution` 并重跑本阶段门禁。判别性依据：边界例「站点构建通过不改变判定」同构。
- **A3（Flow Type = `technique-document`）**：本线主交付物是框架自身的写作技术规范，属 owner 封闭集中的技术文档；`user-manual` / `reference` / `runbook` / `design-note` 均不贴合（约定不是给用户/运维/设计的说明）。
- **A4（唯一形态裁决：半角括号、无前置空格；承重决策）**：唯一形态定为 `中文(English)` 与 `English(中文)`——半角括号、括号紧贴两侧词条、括号内为另一语言。最强反题：仓内 EN-first 全角形态量级更大（M-2 = 1383 处）。裁决依据 Grounded Naming 来源顺序：**用户输入最高优先**——用户原文逐字以半角书写两种方向；全角形态是自发实践、非用户裁决。预期反指标：既有 1383 处全角形态在新约定下全部不合规——这正是现状锚点要暴露的缺陷而非迁移负担（FR-006 不追溯）。重开条件：用户明示全角优先。
- **A5（词汇表 Canonical 双语化）**：以中文为主的项目词汇表，新增/修订条目的 Canonical 采用 `中文(English)` 形态；纯英文专名（如 Spec Kit、SDD）维持原样并依赖 FR-004 豁免。这是裁决而非共识，clarify 可推翻。
- **A6（Related Feature 本阶段直接绑定）**：派发简报裁决「解析为新建 Feature 078 并写绑定结论」，覆盖技能默认的「Need clarification」初始化；故无 `[NEEDS CLARIFICATION]` 标记。
- **A7（检查器为交付物之一，但语义判断不在其内）**：确定性检查器按 FR-009/FR-010 交付；它只判机械形态，「这行是否定义处」的可判定信号由 owner 文档界定（FR-002），信号之外的部分由评审面承担，检查器不做语义判断、LLM 不参与匹配计数。
- **A8（中文侧用词以词汇表为准的判读）**：「中文侧用词以项目词汇表为准」（简报 §4）落实为——同一概念的英文形式由 owner 约定给出后，中文形式 MUST 与词汇表 Canonical 的中文侧一致；词汇表无该词条时，先登记词条再使用双语形态。
- **A9（无人值守 clarify 的裁决权威与登记位置）**：本轮 `/speckit.clarify` 无人值守运行，访谈式问题按 materiality 过滤（答案会改变下游产物的才成题）由执行者自行裁决；全部裁决以 Q/A 形态登记于 `## Clarifications` → `### Session 2026-10-30`（本阶段追加 5 行），可推翻项（A5 等）经复核后维持原裁决。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 框架作者在核心概念的定义处写出双语形态，读者跨 context / 跨模型读到一致的语义锚点 (Priority: P1)

任何维护 `shared/` 或 `templates/` 文档的作者，在**定义**一个核心概念名词或关键流程动词时（owner 文档的定义行、术语条目、章节标题中的概念名），按唯一 owner 约定给出 `中文(English)` 或 `English(中文)` 形态；不同 context 与不同大语言模型的读者读到同一概念时，两种语言的语义互为约束，减少误读。

**Why this priority**：这是用户需求的本体——「锚定语义」的收益只在定义处统一形态后兑现；没有唯一约定，自发实践会继续漂移（现状锚点 M-3：32 个文件内部混用两种形态）。

**Independent Test**: 取任一 `shared/definitions/` 概念条目做改写演练：按其文档主语言给出定义行双语形态，对照 owner 文档逐条核验方向、括号宽度、紧贴形态是否唯一正确——通过即证明约定可执行、可教学。

**Acceptance Scenarios**:

1. **Given** 一份主语言为中文的 owner 文档正在定义新概念名词, **When** 作者写定义行, **Then** 形态必须是 `中文(English)`（半角括号、紧贴），其他写法（全角、加空格、括号语言同向）按 owner 约定可逐条判为不合规。
2. **Given** 一份主语言为英文的文档正在定义关键流程动词, **When** 作者写定义行, **Then** 形态必须是 `English(中文)`，方向与中文文档相反。
3. **Given** 同一概念在第二份文档中被**定义**, **When** 作者引用其双语形态, **Then** 中英两侧与首次定义及词汇表 Canonical 完全一致。

---

### User Story 2 - 词汇表维护者登记新术语时，Canonical 直接采用双语形态 (Priority: P1)

维护 `.specify/memory/glossary.md` 的人新增或修订条目时，Canonical 列按 A5 采用 `中文(English)` 双语形态（纯英文专名豁免），其他文档的中文侧用词以该 Canonical 为准。

**Why this priority**：词汇表是 132/161 已双语化的最大定义面（M-7），也是 FR-005 一致性的判定基准；不把词汇表纳入约定，跨文档一致性没有锚点。

**Independent Test**: 登记一个虚构词条并按约定改写 Canonical，用 FR-005 的判定规则核对「第二处定义与 Canonical 一致」——通过即证明一致性要求可操作。

**Acceptance Scenarios**:

1. **Given** 一个新项目术语需要登记, **When** 维护者写入词汇表, **Then** Canonical 为 `中文(English)` 形态、Variants 收集中文侧易混写形式，Origin/Status 按词汇表既有协议填写。
2. **Given** 词汇表中已存在某词条, **When** 作者在另一份文档定义同一概念, **Then** 中文侧用词与 Canonical 中文侧逐字一致；不一致时以词汇表为准并登记变体。

---

### User Story 3 - 下游项目经 `specify init` 获得约定的 ambient 摘要与指针 (Priority: P2)

任一使用 Spec Kit 的下游项目在 init / 刷新 instructions 后，其 `.specify/instructions.md` 出现本约定的 ambient 小节（一段摘要 + owner 路径指针），作者知道去框架源查完整规则。

**Why this priority**：本特性属框架源（两顶帽子）；只改本仓运行时副本等于没做。分发路径是约定的生存方式，但它是 US1/US2 的下游消费，可独立测试。

**Independent Test**: 在临时目录对已安装框架跑一次 instructions 生成（或检查 `generate-instructions.sh` 的输入模板），断言 ambient 小节存在且只含摘要 + 指针——通过即证明分发面可达。

**Acceptance Scenarios**:

1. **Given** 下游项目执行 init / instructions 刷新, **When** 生成 `.specify/instructions.md`, **Then** ambient 小节包含本约定的一句话摘要与 owner 文档路径指针，且不复述规则枚举。
2. **Given** ambient 小节已存在, **When** owner 文档修订规则, **Then** ambient 内容无需同步改写（指针形态天然免漂移）。

---

### User Story 4 - 维护者运行确定性检查器，机械校验定义行形态与覆盖面 (Priority: P2)

维护者在提交前或评审时运行检查器，对 owner 文档登记的定义面做机械扫描：定义行是否含括号双语、括号语言是否与文档主语言相反、owner 覆盖面是否齐全；输出可定位到文件与行。

**Why this priority**：Program-First（Token Efficiency）要求固定规则的文本判断交给确定性程序；检查器把 US1 的人工核验降为机器判定，但只做机械面（A7），不签字语义。

**Independent Test**: 构造一条合规定义行与一条全角违规行作为夹具，运行检查器，断言合规行 pass、违规行 fail 且输出指认行号——通过即证明机械判定可红可绿。

**Acceptance Scenarios**:

1. **Given** 某定义行使用全角括号（A4 违规）, **When** 检查器扫描, **Then** 该行判 fail 并给出文件与行号定位。
2. **Given** 某定义行括号语言与文档主语言同向, **When** 检查器扫描, **Then** 该行判 fail。
3. **Given** owner 覆盖面清单中某个定义面整段缺失, **When** 检查器核验覆盖面, **Then** 输出缺失项清单。

---

### Edge Cases

- **主语言混合的文档**：中英段落交替时，方向规则以哪一段为准？→ 按文档声明的主语言判定（文档头 / frontmatter / 首段），owner 文档给出判定信号；无法判定主语言的文档默认按段落各自的语言执行方向规则（保守形态，不强制统一）。
- **既有双形态已并存的概念**（如某概念已有 `English（中文）` 全角与 `English(中文)` 半角两种写法）：新约定下以哪种为准？→ 以词汇表 Canonical 为准（FR-005）；词汇表缺失时先登记词条；既有提及处不追溯（FR-006）。
- **代码块、行内代码、路径、命令字面量中的括号**：这些是豁免面（FR-004）——检查器 MUST NOT 扫描代码块与行内代码内部，否则误报淹没真实缺陷。
- **「定义处」无法被机械识别的部分**：owner 文档用可判定信号（术语表条目行、定义行排版特征、章节标题中的概念名）界定检查输入；信号覆盖不到的新形态先由评审面承担，owner 文档在下次修订时补信号——检查器不发明语义判断（A7）。
- **第三方专名与公认缩写**：如 Spec Kit、SDD 首次定义后可单语使用；首次定义处仍需双语（除非属 FR-004 豁免的纯专名）。
- **模板中立性冲突**：`templates/` 面向所有下游项目，ambient 摘要不得写本仓专属路径——指针一律写框架源相对路径（`shared/guidelines/bilingual-expression.md`），由镜像机制解析（FR-012）。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 约定本体（owner 文档）

- **FR-001**: 新建唯一 owner 文档 [[STR-001]]，承载双语表述约定的全部事实：何时必须双语（定义处判据）、括号方向规则、唯一形态（括号宽度/空格/紧贴方式）、覆盖定义面封闭集、豁免面封闭集、跨文档一致性规则、迁移边界。其他任何位置（命令模板、技能、契约、测试、instructions、词汇表）MUST 以「路径 + 章节锚」引用该 owner，MUST NOT 复述其方向、形态、覆盖面或豁免的枚举。
- **FR-002**: 约束对象限定为「定义处」：核心概念（名词）与关键流程（动词/流程名）**被定义**的位置——owner 文档的定义行、词汇表条目、概念/流程的首次定义、章节标题中的概念名。每一次提及不要求双语；owner 文档 MUST 给出「定义处」的可判定信号清单（排版特征），供 FR-009 检查器与人工核验共用。
- **FR-003**: 方向规则：文档主语言为中文 → 形态为 [[STR-002]]；文档主语言为英文 → 形态为 [[STR-003]]；括号内一律为另一语言，同一文档以文档主语言决定括号语言。主语言混合文档的判定信号与保守缺省由 owner 文档规定（Edge Cases 首条）。
- **FR-004**: 豁免面为封闭集：代码标识符、路径、命令字面量、API 名、YAML/JSON 键、第三方专名；公认缩写（如 SDD）在首次双语定义后可单语使用。豁免面清单的唯一 owner 是 FR-001 的 owner 文档，本 FR 不复述其扩充规则。
- **FR-005**: 一致性规则：同一概念在不同文档中的中英双语形态 MUST 一致；中文侧用词以项目词汇表（`.specify/memory/glossary.md`）Canonical 为准，不一致处以词汇表为准并登记变体（A8）。词汇表 Canonical 的双语化形态按 Assumptions A5 执行。
- **FR-006**: 迁移边界：约定只约束**新写内容与 owner 文档的维护**；既有 dated records、已完成规格、历史记录不做追溯重写。存量不合规形态（现状锚点 M-1/M-2）记为已知差异，随各文档下次自然修订时收敛。

#### B. 覆盖面（哪些定义面必须双语）

- **FR-007**: owner 文档登记覆盖定义面封闭集，至少包含：词汇表条目 Canonical、`shared/definitions/` 概念条目、`shared/guidelines/` 与 `shared/workflow/` 文档的标题与定义行、宪法原则标题、instructions ambient 小节标题、`templates/` 章节标题、命令与技能名首次定义处。封闭集的增删只能经 owner 文档修订。
- **FR-008**: instructions ambient 层只承载「一段摘要 + owner 路径指针」（指针值 = [[STR-001]]），其形态、位置与生成方式遵循既有 ambient 小节惯例（见 `templates/instructions-template.md` 中 `## One Source Of Truth` 等同类小节）；ambient MUST NOT 复述 FR-001 的规则枚举。

#### C. 机械守卫（确定性检查器）

- **FR-009**: 交付确定性检查器，只做可机械判定的事：（a）定义行是否含括号双语形态；（b）括号语言是否与所在文档主语言相反；（c）owner 覆盖定义面是否齐全。检查器 MUST NOT 进入代码块与行内代码内部（豁免面），MUST NOT 做语义判断，LLM MUST NOT 参与匹配与计数（Program-First）。实现 MUST 复用既有校验脚本风格与公共工具（如 `glossary-utils.py` 的读取模式），不新造检查引擎。
- **FR-010**: 检查器的输入信号取 FR-002 的可判定信号清单；信号覆盖不到的定义形态不在检查器判定范围，由评审面承担。检查器的运行入口、退出码语义与门禁挂接面在 plan 阶段确定，本阶段不绑定具体门禁算子。

#### D. 分发（两顶帽子）

- **FR-011**: 全部规则性变更落在框架源：[[STR-001]]（owner）、`templates/instructions-template.md`（ambient 小节）；经镜像同步与 `specify init` 分发到全部下游项目。本仓 `.specify/` 运行时副本 MUST 由再同步 / 刷新机制产生，MUST NOT 手改（两顶帽子纪律）。
- **FR-012**: 模板中立性：`templates/` 内的 ambient 摘要不得出现本仓专属路径、提交号或内容；指针一律写框架源相对路径，由既有镜像机制解析到运行时位置。

#### E. 不变量、边界与登记

- **FR-013**: 与 `.specify/shared/guidelines/user-facing-comprehension.md` 的 jargon 白名单不冲突：白名单术语的**提及处**维持可白名单状态，**定义处**仍须双语——两规则作用于不同面，owner 文档声明其交界处理。
- **FR-014**: 与 One Source of Truth（宪法 XIV）对齐：双语规则只有 FR-001 一处 owner；ambient 只有摘要 + 指针；漂移守卫由本特性的契约测试或检查器承担（plan 阶段落具体形式）。
- **FR-015**: Scope Discipline（宪法 IX）：不新增运行时、服务、后台进程；交付物限于 owner 文档、ambient 小节、检查器脚本及其测试、 Feature 登记。
- **FR-016**: 迁移执行边界：不做一次性大规模重写；存量差异清单化（由 FR-009 检查器的扫描输出派生）但不批量改写；每个文档在其下次自然修订时按 owner 约定收敛。
- **FR-017**: Feature 登记：Feature 078 在 `.specify/memory/features.md` 登记行、`.specify/memory/features/078.md` 详情随本阶段落盘；登记遵守 `shared/workflow/feature-integration.md` 的索引纪律（手维护，头与行同改）。
- **FR-018**: ID 登记：本特性产出的 durable identifier（契约条款号、决策记录号等）在首次 coin 时登记 `.specify/memory/register.md`。

### 显式排除项（Out of Scope）

- 全文双语化（每一次提及都双语）：明确不做，噪声会稀释定义处的锚定作用（FR-002）。
- 既有文档的批量重写与强制迁移（FR-006 / FR-016）。
- 语义层面的判断（「这个括号里的英文是否译得准」）：约定只管形态，不管翻译质量。
- 除 instructions ambient 之外的命令模板 / 技能正文改写：它们只加指针（FR-008），不复制规则。
- 新命令或新阶段：本特性不产生 `/speckit.*` 命令。

### Key Entities *(include if requirement involves data)*

- **双语表述约定（Bilingual Expression Convention）**：本特性的核心实体，物化为 owner 文档 `shared/guidelines/bilingual-expression.md`；属性：方向规则、唯一形态字面量、覆盖定义面封闭集、豁免面封闭集、一致性规则、迁移边界。
- **定义处（Definition Site）**：概念/流程被定义的位置；属性：所在文档主语言、可判定信号（排版特征）、所属覆盖定义面。
- **术语条目（Glossary Entry）**：词汇表行；属性：Canonical（A5 双语形态）、Variants、与约定的引用关系（FR-005 的判定基准）。
- **检查器（Checker）**：确定性脚本；属性：输入信号清单（派生自 FR-002）、豁免扫描规则（FR-004）、输出形态（文件+行号定位）、退出码语义（plan 阶段定）。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 双语表述约定在唯一 owner 文档中成文，且对 `shared/`、`templates/`、`.specify/`（排除 specs/history）的定向抽查中，owner 文档之外出现方向/形态/覆盖面/豁免枚举的复制位置数为 **0**（封闭清单：以 FR-001 四组枚举的关键词表做检索，基线为交付当日的实测快照）。
- **SC-002**: 交付后的新写/修订内容中，覆盖定义面（FR-007 封闭集）内定义行的双语形态合规率 **100%**（判定方式：FR-009 检查器扫描 + 评审面复核抽样，误差 0；不适用全角旧形态，因其不在「新写」范围）。
- **SC-003**: 一条下游项目（临时树）执行 instructions 生成后，其 instructions 文件含本约定 ambient 小节且形态为「摘要 + 指针」的实测次数 ≥ 1，且 ambient 中规则枚举复述处数为 0。
- **SC-004**: 存量文档被本特性改写的文件数（追溯重写）为 **0**；迁移只发生在 owner 文档自身与各文档的自然修订中。
- **SC-005**: 对词汇表全部双语 Canonical 词条的跨文档一致性抽查中，第二处定义的中文侧用词与 Canonical 不一致的处数为 **0**（抽查范围：覆盖定义面封闭集内、词汇表已有词条的概念）。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 检查器或 `grep` 定向检索（关键词表来自 FR-001 四组枚举；检索命令与快照随 evidence 留档），在 review 阶段执行一次；基线快照于本特性交付当日冻结。
- **SC-002 Source**: FR-009 检查器对覆盖定义面的全量扫描输出（文件+行号清单）+ `/speckit.review` 评审面抽样复核；每个交付里程碑后各测一次。
- **SC-003 Source**: 临时目录 instructions 生成实跑的产物文件检查（`test-evidence/` 留档），implement / review 阶段各一次。
- **SC-004 Source**: 本特性全部提交的 diff 文件清单审计——除 owner 文档与登记文件外，既有文档的修改行数为 0（`git diff --stat` 对照 FR-006/FR-016 白名单）。
- **SC-005 Source**: 以词汇表双语 Canonical 列表为输入的检查器交叉扫描（或人工核验清单），plan 阶段定抽样比例，review 阶段执行。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "shared/guidelines/bilingual-expression.md" | FR-001、FR-008、FR-011 指针、ambient 小节、契约测试、检查器常量 |
| `STR-002` | "中文(English)" | FR-003、A4、owner 文档形态条款、检查器合规形态常量、夹具 |
| `STR-003` | "English(中文)" | FR-003、A4、owner 文档形态条款、检查器合规形态常量、夹具 |

**Citation convention**: 当 FR、契约、任务或测试引用以上字符串时写 `[[STR-NNN]]` 而非复制字面量。`中文(English)` / `English(中文)` 中的「中文」「English」为占位符（表示任一词条与另一语言词条），检查器的实际形态常量由 owner 文档给出正则形态，本表登记的是展示形态。

## Clarifications

### Session 2026-10-30

- Q: 原文「English(中问)」的读法 → A: 按「English(中文)」理解，`中问` 为 `中文` 的笔误（用户裁决，U0 入口声明；登记为 Assumptions A1）。
- Q: 括号形态的唯一标准（半角/全角、空格） → A: 半角括号、紧贴两侧词条（`中文(English)` / `English(中文)`），依据 Grounded Naming 用户输入优先（Assumptions A4）；全角 1383 处存量形态记为已知差异不追溯。
- Q: Related Feature 绑定时机（技能默认「Need clarification」） → A: 派发简报裁决本阶段直接绑定新建 Feature 078（Assumptions A6）。
- Q: 读者声明缺失（G-clarify-reader 算子，blocking）如何补齐 → A: 头部（前 40 非空行内）补 `**Readers**` / `**Reading scenario**` 两行且值非空；读者基准不新建，引用 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议。
- Q: A5（词汇表 Canonical 双语化，原文留「clarify 可推翻」）本轮是否推翻 → A: 维持 A5。Canonical 是 FR-005 跨文档一致性的唯一判定基准，回退单语将使 SC-005 失去锚点；现状锚点 M-7（132/161 已双语化）表明该实践已被接受；推翻需联动改写 FR-005 / US2 / SC-005 而无下游收益，materiality 过滤不通过。
- Q: 唯一形态的大小写维度（`english(中文)` vs `English(中文)`）是否需新增显式条款 → A: 无需新增 FR。FR-005 与 US2 验收场景的「逐字一致 / 以词汇表 Canonical 为准」已把大小写纳入精确匹配；检查器的形态常量（含大小写）归 owner 文档（FR-001）与 plan 阶段落实，本阶段不锁定字面量。
- Q: A2 / A4 携带条件升级条款（re-baseline / 重开条件）是否构成未决选择 → A: 不构成。按 decision-tension 形态为承重决策记录预期反指标与重开条件，是裁决的组成部分而非挂起项；判定维持 Flow Class `expression`（A2）与半角唯一形态（A4）。
- Q: FR-010 / FR-014 / SC-005 将机制决定（检查器运行入口与退出码、漂移守卫形态、SC-005 抽样比例）推迟至 plan 阶段，是否现在锁定 → A: 维持分阶段推迟。三处均在规格内留名了决定者与义务，属 SDD 固有分工；现在锁定只缩减 plan 自由度、不改变任何下游产物内容，materiality 过滤不通过。
