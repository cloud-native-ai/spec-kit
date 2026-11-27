# Requirements-Quality Checklist: General Best Practices — 通用最佳实践内容模块（四分类封闭集 + 渐进积累，随框架分发）

**Purpose**: 检验 Feature 111 需求文本（9 FR / 7 SC / 7 Shared Strings / 21 条 A 裁定 / 3 用户故事 / 11 条 Edge Cases / 3 行 Runtime Stack；设计配套为 4 契约 24 条款、19 任务行、9 场景）在 plan 与 tasks 之后的**写作质量**——五文档文档集与四分类封闭集的可判定性、条目形态与「占位 ⇔ 零条目」不变式、积累与晋升的可回放性、框架地图登记与分发/镜像通道、适配与零残留、containment 与记账边界、守卫与测试范围、以及 SC 的可测量性与追溯。每条都是对需求文本（或它点名的 owner 行 / plan 前提）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-27
**Feature (Requirement Scope)**: `111-general-best-practices` → Feature 111 General Best Practices（通用最佳实践）——新独立 Feature（无父切片）；特性索引行与详情文件由后续特性登记阶段落地（FR-009 的唯一例外）。本轮位于 `/speckit.analyze` 与 `/speckit.implement` 之前，按 Feature Integration Protocol 不发起任何状态迁移。
**Requirements (What)**: [../requirements.md](../requirements.md) — 本轮机械读数（2026-11-27，`validate-requirements.py`，逐字输出见 `../test-evidence/checklist-requirements-validator.txt`）：`status: ok`，**0 error(s), 0 warning(s)**；程序计数（见 `../test-evidence/checklist-spec-readings.txt`）：**9 FR**（FR-001…FR-009）、**7 SC**（SC-001…SC-007）、**7 STR**（STR-001…STR-007）、**21 条 A 裁定**（A-1…A-21）、**3 个用户故事**、**11 条 Edge Cases**、**3 行 Runtime Stack**（RS-001…RS-003）、**2 段 Clarifications 会话**。
**Specifications (How, context only)**: [../plan.md](../plan.md)（5 行 Execution Premises EP-001…EP-005；23 条宪法行）、[../data-model.md](../data-model.md)（11 实体 E1–E11 / 12 不变量 INV-01–INV-12 / 3 状态迁移 T1–T3）、[../contracts/](../contracts/)（**4 文件 / 24 条款**：manifest C-101…C-106 / entry-shape C-201…C-205 / accumulation C-301…C-306 / distribution-guard C-401…C-407）、[../quickstart.md](../quickstart.md)（9 场景 S-0…S-8）、[../tasks.md](../tasks.md)（19 任务行；§ Requirement Coverage Map 9/9 与 7/7；24 条款逐条恰认领一次）、[../research.md](../research.md)（M1–M11 / R-1–R-10）、[../feature-ref.md](../feature-ref.md)——**只**用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。
**Readers**: 按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定——需要决定「本需求集能否放行到 analyze / implement」的框架维护者，以及 `specify init` 后在 `.specify/shared/best-practices/` 消费内容、按积累机制沉淀经验的下游项目维护者；不新建读者基准。
**Reading scenario**: 复核者打开本文件，决定三件事：(1) 哪几条需求缺陷必须在 analyze / implement 之前修掉；(2) 哪些项可登记为「已裁定、由下游承载」而放行；(3) 哪些项因判据依赖尚未落地的机制而保持 `not_evaluated`。按条末的 `[Req §…]` / `[contracts §C-NNN]` / `[data-model §…]` / `[plan §…]` 锚回到正文逐字核对。
**Focus / Depth / Audience**: Focus = 阶段简报的八个必覆盖簇（文档集完备与封闭分类集 · 条目形态与占位 · 积累/晋升回放 · 框架地图登记与分发/镜像 · 适配与零残留 · containment 与记账 · 守卫/测试范围 · 可测量性与追溯）；Depth = **Deep**（简报把八簇写成必覆盖集并要求需求全覆盖，默认 Standard 不足以承载）；Audience = **Reviewer**。简报已使意图明确，技能 §2 的三个意图澄清问题按「已预答」跳过，默认值与升深理由记录于此。
**Detection path**: same-author 条件**不成立**——`requirements.md` / `plan.md` / `tasks.md` 由本无人值守 SDD 线内的独立阶段执行体撰写，本执行体未曾撰写所分析的任何制品；按 `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 的「作者不同」分支，门不触发，未派发 fresh-context 检测代理（角色模板亦明令不得再派发代理）。缺口扫描由本执行体直接完成；可机械核对的前提（FR / SC / STR / A / 边界案例 / 条款 / 任务 / EP / RS / 场景计数）均以程序读数当场取证，见 Notes。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成；方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`，结构模板为 `.specify/templates/checklist-template.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner 行 / plan 前提）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，不是一条实现任务。

## 一、文档集与封闭分类集（Document set / closed category set）

- [ ] CHK001 - 模块顶层文档集是否以**封闭集合**逐名写出——`README.md` + [[STR-002]] + [[STR-003]] + [[STR-004]] + [[STR-005]] 恰五个顶层常规文件，任何其它文件**或子目录**都不属于该层，镜像目录携带同名五个文件——且「顶层文件集」的计数单位（常规文件、排除隐藏文件与子目录）是否明确到可直接枚举？[Completeness, Req §FR-001, contracts §C-101, data-model §E1]
- [ ] CHK002 - 封闭分类集的机器形态是否全部可判定——清单**唯一**表格、恰三列（模块 / 文件 / 内容）、恰四行数据行、每行恰一个相对链接、链接目标集合恰为四个 owner 文件、且清单含字面量「封闭集」；「唯一表格」的作用域是清单文件还是整个模块，围栏代码块内的表格是否被排除？[Clarity, Req §FR-001, Req §A-15, contracts §C-102, contracts §C-103]
- [ ] CHK003 - 分类 → owner 文件的映射是否逐项**双向**钉死——编程语言 → [[STR-002]]、系统接口 → [[STR-003]]、编程框架 → [[STR-004]]、编程工具 → [[STR-005]]，四类不多不少；守卫的「集合相等」断言是否同时禁止「表行多于文件」与「文件多于表行」两个方向？[Completeness, Req §FR-001, contracts §C-102]
- [ ] CHK004 - 封闭集变更的三腿义务是否完整且可判定——新增/删除/改名分类 MUST 在同一变更内修订清单表、建立或迁移 owner 文件、更新守卫；「只加文件不改清单」与「只改清单不建文件」均转红；但「**同一变更**」的参照物（一次提交 / 一个阶段的落地 / 整条特性分支）在需求层是否有单一读法？[Completeness, Req §FR-001, contracts §C-106, Req §Edge Cases]
- [ ] CHK005 - 分类范围（scope）的单一所有权是否闭合——清单分类表「内容」列是每类 scope 的唯一所有者，owner 文件不复述，唯一例外是空分类占位旁的一句范围说明；「一句话」是否以可判定边界写出（一句 vs 一段由谁判定）？且清单在表外还 MUST 声明读者与范围、条目形态、积累机制与种子指针——「模块读者」本身是否在需求层被点名，而非仅存在于规格头的 Readers 行？[Consistency, Req §FR-001, Req §FR-002, contracts §C-104, contracts §C-105]

## 二、Owner 文件、条目形态与占位（Owner files / entry shape / placeholder）

- [ ] CHK006 - owner 文件身份是否以可解析形态写出——恰一个 H1 分类标题 + 一个回指清单的块引用（`README.md` 链接 + 字面量「积累机制」+ 条目形态三元「标题 + 实践 + 反例/证据」），且该块是**指针**、不得复述积累规则内容？[Completeness, Req §FR-002, contracts §C-202]
- [ ] CHK007 - 条目形态的字面量集合是否在单一所有者处定格并由各 FR 指回——`## ` 标题 + `**实践**` 项目符号 + `**反例 / 证据**` 项目符号（可选 `**延伸**`；晋升条目另带 `**来源**`），含分隔符两侧空格的确切拼写；缺任一必填项目符号即红——形态定义是否确在 A-16 / FR-001 单点拥有，而不是在 FR / 契约 / 任务中多处逐字复制？[Clarity, Req §FR-001, Req §A-16, contracts §C-201]
- [ ] CHK008 - 「条目」的计数边界是否明确到可写守卫——owner 文件中**任何** `## ` 标题是否一律视为条目起点（因而必须携带两个必填项目符号），还是该文件允许出现其它二级小节？守卫腿 (b) 按 `## ` 枚举条目，未定的读法会让同一模块结构同时被判红与判绿。[Ambiguity, Req §FR-007(b), contracts §C-201]
- [ ] CHK009 - 占位 ⇔ 零条目的**互斥不变式**是否完整——恰一行含 [[STR-006]] 的斜体占位 + 一句范围说明与零个 `## ` 条目同真；有 ≥1 条目时 MUST NOT 带占位；首次晋升同变更移除占位；守卫 MUST NOT 冻结数量——斜体的 Markdown 形态（`*…*` 与 `_…_`）与「恰一行」是否足以让解析唯一？[Consistency, Req §FR-002, Req §A-16, contracts §C-203]
- [ ] CHK010 - 「交付态计数 = 3」与「不冻结数量」的张力是否已内建为单一读法——SC-001 明写计数只约束交付态测量、守卫按互斥不变式判定，Edge Cases 又声明晋升后该计数失效；是否还有第二处把「3」当作验收不变量（某个 SC / 契约 / 任务行）需要同样声明？[Consistency, Req §SC-001, Req §A-16, Req §Edge Cases, contracts §C-203]
- [ ] CHK011 - 种子条目的内容是否以可测量的验收形态写出——三项事实（默认 HTTPS；特殊仓库走 HTTP/SSH 时 MUST 显式提示协议与凭据要求；`~/.git-credentials` 的 HTTP-vs-HTTPS 协议错位反例）加延伸 SSH 口径全部在场，标题字面量 = [[STR-007]]；守卫对这些散文内容的三项断言以哪些**字面 token** 为准是否已规定，还是留给守卫作者自行裁量「算不算提到」？[Measurability, Req §FR-003, Req §SC-002, contracts §C-204]

## 三、渐进积累与晋升回放（Accumulation / promotion replayability）

- [ ] CHK012 - 观察形态是否落在既有引擎**实际存在的字段**上——`feedback-utils.py --action record` 的必填参数是 `--unit-id / --run-id / --review / --points`，其条目形态为 `## Review` + `## Optimization Points`，**没有**名为 `notes` 的字段（`--action args-manifest` 实测，2026-11-27）；而 A-17 / C-301 要求「观察的 notes 携带 `[best-practice]` 与 owner 文件 stem，不新增字段」。标记与 stem 究竟落在记录的哪个既有字段？不构成命令/skill 运行的独立观察又如何满足必填的 unit-id / run-id？[Gap, Req §FR-004, Req §A-17, contracts §C-301]
- [ ] CHK013 - 晋升规则是否可判定且与既有纪律单点对齐——「通用」定义为「反复出现或一次明确的用户纠正」，晋升按 `.specify/shared/guidelines/knowledge-promotion.md` 执行并落在 stem 命名的 owner 文件；从条目 `**来源**` 行反向抵达观察记录的回放路径是否在需求层写成步骤（而不是只说「可回溯」）？[Clarity, Req §FR-004, Req §A-17, contracts §C-302]
- [ ] CHK014 - `**来源**` 行内容是否完整量化——至少含 feedback 条目 ID / ≥7 位 hex 提交号 / 会话原话引用之一，并写明「通用」判定依据（反复出现或一次明确用户纠正）；晋升 MUST NOT 改写既有观察记录、新增 feedback 状态或另立晋升台账——三条禁令是否都在需求层以 MUST NOT 形态出现？[Completeness, Req §FR-004, contracts §C-303, contracts §C-302]
- [ ] CHK015 - 种子的来源行语义是否唯一——FR-003 说模块文本「MUST NOT 编造 feedback ID 或来源行」，A-17 说种子「豁免来源行」，而 tasks / quickstart 把豁免读作「**不带** `**来源**` 项目符号」；「豁免」（可选）与「禁止」（必须缺席）对守卫是两种不同断言，需求文本采用哪一种？[Ambiguity, Req §FR-003, Req §A-17, contracts §C-204, quickstart §S-3]
- [ ] CHK016 - 「无第二机制」的可判定检测面是否前后一致——FR-007(d) 说「`scripts/python/` 下不存在以 best-practices **命名**的引擎文件」，SC-003 说「无 `best-practices.py` / `best_practices.py` 引擎文件」，契约 C-304 用两个确切文件名，任务行用 `best-practices*.py` 通配；四个表述对 `best-practices-utils.py` 或 `best_practices_engine.py` 给出不同裁决——以哪个为准，文本层声明归评审的边界是否随之写明？[Consistency, Req §FR-007(d), Req §SC-003, contracts §C-304]
- [ ] CHK017 - 「指针而非复述」与红线的守卫边界是否写清——清单 MUST NOT 复述 owner 的处置规则、晋升门槛或任何枚举（指针形态允许复述到何种粒度，例如标记约定本身是否算复述？）；「干净运行不得追加空洞条目、不得编造数值」由评审裁定而非守卫断言——这条红线的判定所有者是否被具名（评审阶段），以免无人拥有？[Clarity, Req §FR-004, contracts §C-305, contracts §C-306, Req §A-11]

## 四、框架地图登记与分发/镜像（Registration / distribution / mirror）

- [ ] CHK018 - 地图登记行的可判定形态是否完整——`shared/definitions/framework-map.md` 唯一布局表内的恰一行，与既有 `.specify/shared/` 行相邻、三列形态，Where 单元 = `.specify/shared/best-practices/`，Notes 单元同时含 Feature 111、清单 `README.md` 指针与 `(framework source: shared/best-practices/)`；源与镜像各恰一行——守卫腿 (e) 的双 token 断言之外，Feature 111 是否也被要求以 token 而非任意邻近文本出现？[Measurability, Req §FR-005, Req §A-19, contracts §C-403]
- [ ] CHK019 - 「与既有 `.specify/shared/` 行**相邻**」这一位置要求是否被指派给任何检查面——守卫腿 (e) 只钉存在性与 token 对，未断言邻接；相邻性因此是无人裁定的排版义务，还是应降级为生产者指引（不进入验收）？[Gap, Req §FR-005, Req §A-19, contracts §C-403]
- [ ] CHK020 - 同变更登记与 instructions 禁令是否双写完整——FR-005 要求登记与模块创建同一变更落地（`shared/guidelines/directory-governance.md` § 3），镜像由既有机制再生成、MUST NOT 手改；`.specify/instructions.md` 与指令模板 MUST NOT 新增指针段（A-6 的理由：现有 Framework Map 段已是指针）——这条禁令的 MUST NOT 形态与理由是否都在需求层，而非只在 plan？[Completeness, Req §FR-005, Req §A-6, contracts §C-403]
- [ ] CHK021 - 分发通道是否以封闭清单写成——复用 `specify init` 的 `shared/` 整目录拷贝与 `sync-mirrors.py` 的既有镜像对；MUST NOT 新增或修改 CLI 代码、打包内容、`.gitignore` 规则或运行时存储——四项禁令是否都可从需求文本直接判定？[Completeness, Req §FR-006, contracts §C-401]
- [ ] CHK022 - 镜像再生成与唯一裁决是否可测量——写模式同变更再生成、镜像 MUST NOT 手改、字节一致仅由既有参数化套件裁决、守卫不得复制比较逻辑；SC-004 的「对本模块的源/镜像差集 = 空」在 `--check` 输出中如何读取——配对级 `ok`（落地后 122 文件）加零 `DIFF` 行是否为被接受的等效读数，还是「逐模块差集」要求引擎不输出的粒度？[Measurability, Req §FR-006, Req §SC-004, contracts §C-402]
- [ ] CHK023 - init 分发证明是否三件齐全且执行形态无歧义——代码路径引用、既有 init 集成测试（运行同一拷贝步骤）、`.specify/.tmp/` 内只读演练（`--here --ai qoder --script sh --no-git`）读到恰五文档；且不新增第二个测试文件——但演练用**哪种 CLI** 执行（source-run `PYTHONPATH=src` vs 全局安装的 `specify`，后者自带打包 `shared/`、embedded commit 早于本线）在需求层未指定，会使证明在错误解释下失真；这属于 FR/SC 层的缺口还是可留给下游的执行细节？[Gap, Req §SC-004, Req §A-18, contracts §C-407, tasks §Environment Prerequisites]

## 五、适配与零残留（Adaptation / zero residue）

- [ ] CHK024 - 适配映射是否封闭且可判定——`ai-harness` → `Spec Kit`、`.ah/` → `.specify/`、`/ah.*` → `/speckit.*`、归属 `Feature 040` → `Feature 111`；源模块实测零 `/ah.*` 命中，因此「出现时一并适配」的**条件性条款**在零命中的输入上如何验收（缺席即满足？）；`Feature 040` 归属行不属于三字面量残留扫描，但属归属适配断言——这一区分是否在需求文本中写明？[Completeness, Req §FR-008, Req §SC-005, contracts §C-405]
- [ ] CHK025 - 残留计数是否以可复算的方式量化——五文档内 `ai-harness` / `.ah/` / `/ah.` 三组字面量出现数 = 0；扫描范围是否明确限定为**模块五文档**（而非守卫、规格或整个仓），三个 token 的边界（区分大小写、`.ah/` 与 `/ah.` 互不覆盖）是否说明？[Measurability, Req §FR-008, Req §SC-005, contracts §C-404]
- [ ] CHK026 - 「模块引用的每个仓内路径存在」的引用集合是否可枚举——C-404 前导的「至少」四路径（`.specify/scripts/python/feedback-utils.py`、`shared/guidelines/knowledge-promotion.md`、`.specify/shared/best-practices/`、`tests/contract/test_general_best_practices.py`）并非都能从模块文本中推出：模块是否真的引用镜像目录与守卫文件？「至少」集合是模块引用推导而得的闭合集合，还是一条独立的基础设施断言？两者混写会让守卫的失败原因难以归因。[Ambiguity, Req §FR-008, contracts §C-404]
- [ ] CHK027 - 模块**下游可解析性**是否被任何需求覆盖——模块随 `shared/` 分发到客户项目，而 C-104(b) / T005 要求清单指向 `.specify/specs/111-general-best-practices/contracts/entry-shape.contract.md`（该路径只在框架仓存在，客户项目不收 specs）；FR-008 的存在性义务只按目标仓计，因此该指针能过守卫却对下游断链——应在需求层禁止模块引用未随包分发的路径，还是承认这一耦合并在文本中给出下游独立的形态声明？[Gap, Req §FR-001, Req §FR-008, contracts §C-104, tasks §T005]

## 六、边界封闭与记账（Containment / accounting）

- [ ] CHK028 - containment 声明是否具备封闭宣告的全部要素——基线参照物 `0419adae5`、可推导的允许增量路径集、集合外零差异、引擎/模板/技能/代理/命令/宪法/指令/存储布局/决策治理面改动数 = 0；A-12 规定基线与允许增量集由 FR-009 单点拥有、SC-006 只引用不复述——SC-006 的现有措辞是否确有复述（例如重列路径类别）还是纯引用？[Measurability, Req §FR-009, Req §SC-006, Req §A-12]
- [ ] CHK029 - 残余路径判定程序是否可执行——先做路径集差，残余仅当落在 `.specify/session/` / `.specify/feedback/` / `.specify/exec-quant/` 三存储且其「记录体」（frontmatter 或正文）含特性 key `111-general-best-practices` 或 run id `r20261127T071500Z-111a` 时放行；「记录体」对 per-entry Markdown 与 per-entry JSON 两种形态是否都定义了判定位置与匹配范围？[Clarity, Req §FR-009, Req §A-20, contracts §C-406]
- [ ] CHK030 - 「MUST NOT 改写聚合/索引」与残余谓词是否互不冲突——A-20 禁令点名 `.specify/exec-quant/records.jsonl` / `scores.jsonl`（两文件实测在场，2026-11-27），但残余谓词只按「落在三存储 + 记录体含 key/run-id」放行：一次向 `records.jsonl` 追加含该 key 的行会被路径判定放行，与禁令矛盾；谓词是否需要「仅 per-entry 文件放行、聚合与索引文件一律违规」的明文排除？[Conflict, Req §FR-009, Req §SC-006, Req §A-20, contracts §C-406]
- [ ] CHK031 - 登记例外与词表排除是否双侧写明——后续特性登记阶段对 `.specify/features.md` 与 `.specify/features/111-*.md` 是唯一例外；`.specify/glossary.md` 明确不在声明集内（A-21：线内登记须先修 FR-009，否则线后另行登记）——两个边界是否都出现在 containment 的声明处与 Edge Cases，而非只在一处？[Completeness, Req §FR-009, Req §A-21, Req §Edge Cases]
- [ ] CHK032 - 零改动枚举是否与「不做什么」及 FR-005 / FR-006 一致——SC-006 的枚举（引擎/模板/技能/代理/命令/宪法/指令/存储布局/决策治理）是否覆盖 Overview「不做什么」列出的全部面，且与 FR-005 的 instructions 禁令、FR-006 的 `.gitignore` 禁令无遗漏、无矛盾？[Consistency, Req §SC-006, Req §Overview, contracts §C-403]

## 七、守卫与测试范围（Guard / test scope）

- [ ] CHK033 - 守卫断言范围是否以封闭清单写出——六腿 (a)–(f) 加模块读取前导（残留与引用路径存在）各自点名的断言主体是否完整到可逐条实现，且「六腿」被声明为**穷尽**范围（守卫越界新增第七类断言即缺陷），避免范围漂移？[Completeness, Req §FR-007, contracts §C-404]
- [ ] CHK034 - 守卫的三项禁令是否都以 MUST NOT 形态在场——不复制镜像比较逻辑（字节一致归既有套件）、不冻结占位数量、不声称判定条目语义真伪；三项各自的可接受替代（评审拥有语义判定）是否同样写明？[Completeness, Req §FR-007(b), Req §A-16, contracts §C-205, contracts §C-404]
- [ ] CHK035 - SC-007 的证据形态是否可复算——守卫经 `scripts/bash/run-tests.sh` 退出 0、red-first 记录在场、镜像套件相对**入口基线**零新增红、全量失败名集 ⊆ 入口基线；「入口基线」指哪一份工件（实现入口的全量失败名捕获）是否在需求层可定位，还是仅以 `/speckit.implement` 的 owner 行作间接引用？[Measurability, Req §SC-007]
- [ ] CHK036 - red-first 的失败形态与「唯一新增测试文件」边界是否写明——守卫先于模块落地、以**缺失模块**（而非语法/导入错误）为红因，模块落地后同守卫全绿；本特性不新增第二个测试文件，镜像与 init 证明分别由既有套件与记录演练承担——「红因须为缺失模块」是需求文本的断言还是任务生成的补充？[Clarity, Req §FR-007, Req §SC-004, Req §SC-007, Req §A-7, contracts §C-407]

## 八、可测量性、追溯与假定（Measurability / traceability / assumptions）

- [ ] CHK037 - 七个 SC 是否全部量化并各自点名测量来源——5/5、4/4、100%、3、2/2、0、122、退出 0、名字集差等读数是否每项都有 § Measurement Sources 的采集方式与 Path（final/supporting）标注；是否存在任一条 SC 依赖未被声明的读数（例如「零新增红」需要入口基线工件）？[Measurability, Req §SC-001…§SC-007, Req §Measurement Sources]
- [ ] CHK038 - Shared Strings 是否覆盖守卫要钉的全部跨工件字面量——当前 7 条（[[STR-001]]…[[STR-007]]）之外，`**实践**`、`**反例 / 证据**`、`**延伸**`、`**来源**`、`积累机制`、`封闭集` 这些被 FR / 契约 / 任务 / 守卫多处复制的字面量未登记；按本规格自己的引用约定，它们是否应入表以防漂移？[Gap, Req §Shared Strings, Req §FR-001, Req §FR-007]
- [ ] CHK039 - A 裁定与它锐化的 FR/SC 是否逐条对齐且无矛盾——A-15 / A-16 / A-17 / A-18 / A-19 / A-20 是否分别被 FR-001/002、FR-003/004、FR-006、FR-005、FR-009/SC-006 引用；是否存在反向矛盾（如 A-12 的单一所有权 vs SC-006 的复述、A-16 的「H1 唯一」vs FR-002 的「唯一 H1」措辞差异）？[Consistency, Req §A-12…§A-21, Req §FR-001…§FR-009, Req §SC-006]
- [ ] CHK040 - 运行时栈与前提引用是否闭合——RS-001…RS-003 的 Form / FR / Premises 单元可解析（EP-001…EP-003 由 plan 的 Execution Premises 定义），用户故事的 Independent Test 是否各自映射到至少一条 SC / 守卫腿，从而每个故事都有独立验收面？[Dependency, Req §RS-001…§RS-003, Req §FR-001…§FR-007, Req §User Scenarios & Testing, plan §Execution Premises]

## Notes

- **勾选与判读**：`[x]` 表示该问题已依据需求文本（或点名的 owner 行 / plan 前提）得到回答；答「否」即对 `requirements.md` 的 finding，不是一条实现任务。本阶段交付的是清单器械；逐条作答属于 analyze / review 的判定职责。
- **计数（footer，程序读数）**：共 **40 条**，CHK001…CHK040；**40/40（100%）** 携带至少一个追溯锚（`[Req §…]` / `contracts §C-NNN` / `data-model §…` / `[plan §…]`），满足 ≥80% 下限；soft cap 40 未超出；CHK 编号唯一且顺序连续；无 `Verify` / `Test` / `Confirm` / `Check` 开头的实现检验式条目；无仅能靠运行产品回答的条目。
- **维度计数（按每条的主维度，程序读数）**：Completeness **11**、Measurability **7**、Clarity **6**、Consistency **6**、Gap **5**、Ambiguity **3**、Conflict **1**、Dependency **1** ＝ 40；逐条归属见 `../test-evidence/checklist-selfcheck.txt`。
- **章节计数**：一 5（CHK001–CHK005）/ 二 6（CHK006–CHK011）/ 三 6（CHK012–CHK017）/ 四 6（CHK018–CHK023）/ 五 4（CHK024–CHK027）/ 六 5（CHK028–CHK032）/ 七 4（CHK033–CHK036）/ 八 4（CHK037–CHK040）＝ **40**。
- **覆盖矩阵（FR，9/9）**：FR-001 CHK001,CHK002,CHK003,CHK004,CHK005,CHK007,CHK027,CHK038；FR-002 CHK005,CHK006,CHK009,CHK010,CHK038；FR-003 CHK011,CHK015；FR-004 CHK012,CHK013,CHK014,CHK017；FR-005 CHK018,CHK019,CHK020；FR-006 CHK021,CHK022；FR-007 CHK008,CHK016,CHK033,CHK034,CHK036,CHK038；FR-008 CHK024,CHK025,CHK026,CHK027；FR-009 CHK028,CHK029,CHK030,CHK031,CHK032。
- **覆盖矩阵（SC，7/7）**：SC-001 CHK010,CHK037；SC-002 CHK011,CHK037；SC-003 CHK016,CHK037；SC-004 CHK022,CHK023,CHK036,CHK037；SC-005 CHK024,CHK025,CHK037；SC-006 CHK028,CHK030,CHK032,CHK037；SC-007 CHK035,CHK036,CHK037。
- **覆盖矩阵（契约条款，24/24）**：C-101 CHK001；C-102 CHK002,CHK003；C-103 CHK002；C-104 CHK005,CHK027；C-105 CHK005；C-106 CHK004；C-201 CHK007,CHK008；C-202 CHK006；C-203 CHK009,CHK010；C-204 CHK011,CHK015；C-205 CHK034；C-301 CHK012；C-302 CHK013,CHK014；C-303 CHK014；C-304 CHK016；C-305 CHK017；C-306 CHK017；C-401 CHK021；C-402 CHK022；C-403 CHK018,CHK019,CHK020,CHK032；C-404 CHK025,CHK026,CHK033,CHK036；C-405 CHK024,CHK025；C-406 CHK029,CHK030；C-407 CHK023,CHK036。
- **机械读数（2026-11-27，本阶段当场取证）**：`validate-requirements.py` → `status: ok`，**0 error / 0 warning**（`../test-evidence/checklist-requirements-validator.txt`）；程序计数（`../test-evidence/checklist-spec-readings.txt`）：9 FR / 7 SC / 7 STR / 21 A / 3 US / 11 Edge Cases / 3 RS；`contracts/` 4 文件 24 条款（6+5+6+7）；`plan.md` 5 EP；`tasks.md` 19 任务行；`quickstart.md` 9 场景；`data-model.md` 11 实体 / 12 不变量 / 3 状态迁移。
- **清单自检**：`../test-evidence/checklist-selfcheck.txt` 记录本文件的程序读数（条目数、追溯锚覆盖、FR/SC/条款覆盖、禁用开头、编号连续性、维度直方图）。
- **same-author 检测门**：不成立（见 Detection path）；未派发 fresh-context 检测代理（角色模板与派发均明令不得再派发），检测路径如实记录，不以委托路径冒充直接读。
- **本阶段无 plan-owned 改动**：本文件位于 `checklists/`；`requirements.md` / `plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md` / `tasks.md` 未被触碰，故无 `PLAN-EDIT:` 声明。
- **新增而非覆盖**：本文件为 checklist 阶段**新增**清单；requirements 阶段产出的 `checklists/requirements.md` 保持原样（未被覆盖、未刷新）。同轮不生成 recheck 文件（本阶段无「回答早前条目」的动作）。
- **待下游裁定的观察（不阻塞本阶段）**：本清单的 `[Gap]` / `[Ambiguity]` / `[Conflict]` 条目指出的候选确认点——「同一变更」的参照物（CHK004）、owner 文件 `## ` 的条目计数边界（CHK008）、观测记录的 notes 字段在既有引擎中不存在（CHK012）、种子来源行的「豁免 vs 禁止」两读（CHK015）、第二机制检测面四表述不一致（CHK016）、地图行「相邻」无检查面（CHK019）、SC-004 的逐模块镜像读数形态（CHK022）、init 演练的 CLI 形态未在需求层指定（CHK023）、cited-path「至少」集合的推导来源（CHK026）、模块指向 spec 目录契约文件的下游断链（CHK027）、聚合文件禁令与残余谓词冲突（CHK030）、守卫钉字面量未入 Shared Strings（CHK038）——由 `/speckit.analyze` 或实现阶段按判据取证，不在本阶段预先裁定。
- **Feature 状态**：本轮位于 `/speckit.analyze` / `/speckit.implement` 之前，按 Feature Integration Protocol，checklist 不发起任何状态迁移，仅产出清单；`.specify/features.md` 维持无 Feature 111 行（登记阶段延后，FR-009 唯一例外）。