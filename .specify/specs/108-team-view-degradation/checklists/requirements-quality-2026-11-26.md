# Requirements-Quality Checklist: Team View Degradation Hardening — 真实团队定义下的诚实呈现与降级语义

**Purpose**: 检验 Feature 108 需求文本（25 FR / 8 SC / 3 Shared Strings / 4 契约 35 条款）在 plan 与 tasks 之后的**写作质量**——报告时间戳语法的封闭性、三分类与最新选择的可判定性、残留与不确定性的边界、缺失产物与四态纪律、binding/goal 归一的「只呈现不修复」、名册矩阵异常的触发面、降级原因封闭集与退出码映射、健康输出的逐字节保真、单引擎与只读边界、兼容/迁移声明，以及每条 FR/SC/条款的可追溯性。每条都是对需求文本（或它点名的 owner 行/plan 前提）的提问，**不是**对实现行为的检验：凡只有跑一遍产品才能回答的条目，本身就是本清单的缺陷。
**Created**: 2026-11-26
**Feature (Requirement Scope)**: `108-team-view-degradation` → 父 Feature 027 Team Management（`.specify/features.md` 切片行 108 当前 `Planned`；父行保持 `Ready for Review`；本轮位于 `/speckit.implement` 之前，按 Feature Integration Protocol 不发起 `Implemented → Ready for Review` 迁移）
**Requirements (What)**: [../requirements.md](../requirements.md) — 本轮机械读数（2026-11-26，`validate-requirements.py`，逐字输出见 `../test-evidence/checklist-requirements-validator.txt`）：`status: ok`，**239 行 / 33 definition rows / 3 shared strings / 0 error / 0 warning**；程序计数（`../test-evidence/checklist-spec-readings.txt`）：**25 FR**（FR-001…FR-025）、**8 SC**（SC-001…SC-008）、**3 STR**（STR-001…STR-003）、**17 条 A 裁定**（A-1…A-17）、**3 个用户故事**、**12 条 Edge Cases**、**5 行 Runtime Stack**（RS-001…RS-005）、**2 段 Clarifications 会话**。
**Specifications (How, context only)**: [../plan.md](../plan.md)（9 行 Execution Premises EP-001…EP-009；23 条宪法行）、[../data-model.md](../data-model.md)（10 实体 C1–C10 / 10 不变量 INV-01…INV-10）、[../contracts/](../contracts/)（**4 文件 / 35 条款**：program C-101…C-109 / recognition C-201…C-208 / presentation C-301…C-309 / labels C-401…C-409）、[../quickstart.md](../quickstart.md)（8 场景 S-0…S-7）、[../tasks.md](../tasks.md)（29 任务行；§ Requirement Coverage Map 25/25 与 8/8；35 条款逐条恰认领一次）——**只**用于暴露需求的缺口、歧义与冲突，**从不**为它们自身打分。
**Readers**: 按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定——需要决定「本需求集能否放行到 analyze / implement」的框架维护者与下游团队档案使用者；不新建读者基准。
**Reading scenario**: 复核者打开本文件，决定三件事：(1) 哪几条需求缺陷必须在 analyze / implement 之前修掉；(2) 哪些项可登记为「已裁定、由下游承载」而放行；(3) 哪些项因判据依赖尚未落地的机制而保持 `not_evaluated`。按条末的 `[Req §…]` / `[contracts §C-NNN]` / `[data-model §…]` 锚回到正文逐字核对。
**Focus / Depth / Audience**: Focus = 阶段简报的九个必覆盖簇（报告识别/分类/最新/残留 · 缺失产物 · binding/goal 归一指引 · 名册矩阵异常 · 降级原因与退出码映射 · 金标准输出保全 · 单引擎/无第二读取器 · 兼容/迁移 · 可追溯性）；Depth = **Deep**（简报把九簇写成必覆盖集并要求 25 FR + 8 SC 全覆盖，默认 Standard 不足以承载）；Audience = **Reviewer**。简报已使意图明确，技能 §2 的三个意图澄清问题按「已预答」跳过，默认值与升深理由记录于此。
**Detection path**: same-author 条件**不成立**——`requirements.md` / `plan.md` / `tasks.md` 由本无人值守 SDD 线内的独立阶段执行体撰写，本执行体未曾撰写所分析的任何制品；按 `.specify/shared/workflow/objective-analysis-gate.md` § When the gate fires 的「作者不同」分支，门不触发，未派发 fresh-context 检测代理（角色模板与派发均明令不得再派发代理）。缺口扫描由本执行体直接完成；可机械核对的前提（FR / SC / STR / A / 边界案例 / 条款 / 任务 / EP / RS / 场景计数）均以程序读数当场取证，见 Notes。

**Note**: 由 `/speckit.checklist` 按 `.specify/skills/internal/create-checklist/SKILL.md` 生成；方法论 owner 为 `.specify/shared/guidelines/checklist-methodology.md`，结构模板为 `.specify/templates/checklist-template.md`。勾选一条的唯一依据是**需求文本本身**（或该条目点名的 owner 行 / plan 前提）给出了答案；答「否」产出的是对 `requirements.md` 的 finding，不是一条实现任务。

## 一、报告识别、三分类、最新选择与残留（Report recognition / classification / latest / residue）

- [ ] CHK001 - 报告时间戳语法是否作为**封闭集**被逐项写出——五种前导语形（`YYYYMMDDThhmmssZ` / `YYYYMMDDThhmmZ` / `YYYY-MM-DDThh:mm:ssZ` / `YYYY-MM-DDThh-mm-ssZ` / `YYYY-MM-DDThhmmssZ`）、合法 UTC 日历时刻校验、仅限文件名起始位置、以及时间戳后的剩余段 `(?:-[0-9a-f]{4})?-(?:report|stage)\.md`（小写 4-hex 可选、角色词恰为 `report` 或 `stage`）——并规定不完整/模糊匹配一律不被猜测？大小写与扩展名 `.md` 的边界是否可判定？[Completeness, Clarity, Req §FR-001, contracts §C-201, contracts §C-202, data-model §C2]
- [ ] CHK002 - 三分类是否按**固定次序**且仅依据文件名可判定地写出：(1) 无可解析前导时间戳 → 残留（含仅日期前缀、形似 progress-snapshot / judgment-contract、非 `.md` 文件）；(2) 有戳 + 报告剩余段 → 运行报告；(3) 有戳 + 其它剩余段 → 辅助产物；且辅助产物不得竞争 latest、不得计入残留，残留不得计为报告？[Completeness, Clarity, Req §FR-003, contracts §C-202]
- [ ] CHK003 - 残留与辅助产物的呈现上限是否在**需求层**量化——总数 + 有界示例（示例上限与省略计数同时给出）——还是上限只存在于 `C-205` / `C-406`（示例 ≤ 3）而 `FR-004` 只对残留说「有界」、对辅助产物未给形态？[Gap, Clarity, Req §FR-004, contracts §C-205, contracts §C-406]
- [ ] CHK004 - 「最新」是否被完整量化——解析时间戳最大者、并列按文件名字典序升序第一份、禁止 mtime/内容推断、禁止回落到更旧的已识别报告——且规范化 token（UTC、`YYYYMMDDThhmmssZ`、秒精度；`hhmm` 形补 `00`）与其两处载体（`as_of.latest_report_timestamp` 与概览「最近运行」列）在同一需求内一致；单团队「最近报告」行显示文件名而非 token 是否明确？[Measurability, Clarity, Req §FR-002, Req §FR-006, Req §SC-001, Req §SC-006, contracts §C-203, contracts §C-204, data-model §C5]
- [ ] CHK005 - `SC-001` 的生产复现 fixture 是否枚举了它据以断言 5/5 的**全部五个**报告/辅助样本？需求正文点名 3 份报告 + 1 份 `-seat-result.md` + 2 个无时间戳文件（合计 4 个报告/辅助样本），而 `quickstart.md` S-2 另含一份与辅助产物同时间戳的 `20261008T214100Z-report.md` 才构成 5 个样本——该并列报告是否必须进入需求层枚举，否则 5/5 无法仅凭需求文本独立复算？[Gap, Consistency, Req §SC-001, Req §User Story 1 Independent Test, quickstart §S-2]
- [ ] CHK006 - 不确定性谓词及其边界是否全部写明——`runs/` 可读且残留 ≥ 1 即「最新不可证明」→ `report-recognition-uncertain` + 退出码 5；`runs/` 缺失或为空、或全部非报告文件均带可解析时间戳（仅辅助产物）时不产生不确定性；`runs/` 不可读时维持既有 `不可读` 命名状态且**不**产生不确定性（残留无法计数）？[Completeness, Clarity, Req §FR-005, Req §Edge Cases, contracts §C-206]
- [ ] CHK007 - 边界案例是否逐条落到可判定处置——同一时间戳的报告 + 辅助产物（报告胜出、辅助不参与）、同时间戳两份报告（名字典序）、`runs/` 缺失 vs 为空 vs 不可读、以及 `runs/` 内的子目录/非常规条目（是否被排除在「每个常规文件」之外）？[Coverage, Edge Cases, Req §Edge Cases, Req §FR-003, Req §FR-005]
- [ ] CHK008 - 概览模式是否被要求复用同一识别与规范化入口、以行内 `（report-recognition-uncertain：残留 N）` 披露残留、维持 `0/2` 退出域、且不可判定行不得留空或取旧值？[Consistency, Req §FR-006, Req §Edge Cases, contracts §C-207]

## 二、缺失产物与状态纪律（Missing artifacts / state discipline）

- [ ] CHK009 - `缺失 / 为空 / 不可读 / 未记录` 四态是否被要求保持既有含义、逐字不互相替代、适用于全部新面（残留、辅助产物、不可读报告、pattern 不适用）、且缺失事实不得渲染为 `0` 或编造值？[Completeness, Consistency, Req §FR-010, contracts §C-307, contracts §C-402, contracts §C-408]
- [ ] CHK010 - `items.jsonl` 缺失是否要求呈现 `缺失` 并带**后果**（无台账聚合计数、无非终态信号），同时保持 `为空`（存在但零行）与 `不可读` 的既有区分，禁止零值/空聚合/占位行冒充？[Completeness, Req §FR-007, contracts §C-304]
- [ ] CHK011 - 持续运营脊柱（`constraints.md` / `STATE.md` / `run-log.jsonl`）是否按**声明 pattern** 给出三种可判定处置——`continuous` 缺失 = 真实缺口 `缺失`；已声明非 `continuous` = `按声明 pattern 不适用` + `operating-loops.md` § 8 指针；未声明 pattern = 适用性不可判定并披露 owner 无缺省——且部分存在时逐文件混合呈现？[Completeness, Req §FR-008, Req §A-8, contracts §C-305, data-model §C10]
- [ ] CHK012 - 未声明 pattern 时的期望结果是否可从 `FR-008` / `A-8` 的「按 owner 的缺省语义呈现并披露该缺省来源」唯一读出？schema owner（`create-mode.md` § Schema notes）实测**不声明缺省**，于是唯一成立的读法是 `适用性不可判定` + 披露「owner 不声明缺省」——需求是否应把该结论直接写死，避免「按缺省呈现」被误读为存在一个默认值？[Ambiguity, Consistency, Req §FR-008, Req §A-8, contracts §C-305, research §M5/R-10]
- [ ] CHK013 - 「最新报告存在但不可读」是否被明确为**文件级命名状态**（点名路径、组内字段行呈现 `不可读` 而非静默 `未记录`），且单独出现时**不**产生降级原因、**不**改变退出码？[Clarity, Req §FR-009, Req §FR-018, contracts §C-208, contracts §C-306]
- [ ] CHK014 - 「仅残留」时运行报告状态的专名（`未识别（unrecognized）—— 仅残留，最新不可确定`）是否被定义为封闭标签词汇表的成员，且可与四态词汇共存而不坍缩（既不 `为空` 也不 `缺失`）？[Consistency, Clarity, Req §FR-005, Req §FR-010, contracts §C-405, contracts §C-406]

## 三、绑定与 goal 归一（Binding / goal normalization, guidance only）

- [ ] CHK015 - 绑定可读性是否被限定为**仅由引擎读动作决定**（读成功 + `owner` / `owner_id` / `origin` 三键齐备），不可读时保留引擎**逐字原因**并区分「无 binding 块」与「缺键 <names>」，且禁止以缺省值填补或从其它字段推断？[Completeness, Req §FR-011, contracts §C-301, data-model §C7]
- [ ] CHK016 - 绑定不可读是否要求两个受制裁修复指针（`/speckit.team modify` 与引擎写面 `goal-utils.py bind`）并点名记录语义 owner（`anchor-definitions.md` § The Binding Record），且明确 view **零写**、不执行修复？[Completeness, Clarity, Req §FR-012, contracts §C-301]
- [ ] CHK017 - frontmatter 声明 `goal` 键（内联长文本或 slug 形态）时是否一律呈现命名状态 `goal 需归一为 anchor_slug` 并附修复指针（`/speckit.team modify`；需要派生锚点时 `goal-utils.py migrate`），取值形态不得改变该状态、该键不得因 `anchor_slug` 已声明而被静默略过？[Completeness, Clarity, Req §FR-013, contracts §C-302, data-model §C8]
- [ ] CHK018 - 身份解析次序是否明确保持不变（`anchor_slug` > `goal_slug` > 推断），归一建议不得改变本次呈现的身份类型、不得触发迁移，并覆盖 `goal_slug` 旧拼写/并存的边界？[Consistency, Req §FR-014, Req §Edge Cases, contracts §C-302]
- [ ] CHK019 - 「不推断」是否以**四组事实的封闭清单**写出（绑定值、goal→slug、最新报告、名册差异），并要求每处呈现恰为「读得的事实」或「命名状态（含原因）」，无猜测值、无填补缺省？[Completeness, Req §FR-019, contracts §C-309]

## 四、名册矩阵异常（Roster matrix anomaly）

- [ ] CHK020 - 正文矩阵缺 `agent` 列时是否要求矩阵组携带 `形态异常` 并点名缺列、已解析矩阵行仍完整呈现；**重复声明 `agent` 列**的情形目前只出现在 `C-303` / `C9`，`FR-015` 正文仅覆盖「缺列」——需求层是否需要补齐该形态，否则 `形态异常` 的触发面在需求与契约之间不一致？[Gap, Completeness, Req §FR-015, contracts §C-303, data-model §C9]
- [ ] CHK021 - `roster_delta` 不可比对时是否要求呈现 [[STR-002]] 并附原因、禁止以 `未记录` 冒充、frontmatter 成员全量列出、`seats` / `stage_seats` 的已声明/未声明按声明子集披露、且矩阵完全不可解析时以对应 `不可读` / `缺失` / `为空` 原因给出 `不可比对`？[Completeness, Req §FR-016, contracts §C-303, contracts §C-407, contracts §C-403]
- [ ] CHK022 - `seats` / `stage_seats` 未声明时所谓「owner 指针」是否点名到具体 owner（`create-mode.md` § Schema notes 的默认值指针），使「含 owner 指针」在需求层可判定而不是悬空要求？[Dependency, Gap, Req §FR-016, contracts §C-303, contracts §C-403]

## 五、降级原因与退出码（Degradation reasons / exit codes）

- [ ] CHK023 - 降级原因是否被写为封闭集 `{engine-degraded, report-recognition-uncertain}`、每个活跃原因逐个点名（可并存）、固定次序（引擎原因先、识别不确定后）是否在需求层声明；原因是否经既有 `errors[].code` 承载且 `degraded` 当且仅当至少一个原因活跃？[Clarity, Completeness, Req §FR-017, Req §A-9, contracts §C-104, contracts §C-105, data-model §C6]
- [ ] CHK024 - 原因→退出码映射是否逐项钉死为 `5`（2/2）且退出码闭集保持 `0/2/3/4/5` 不变、CLI 面不新增选项（`--target` 仍以 2 拒绝）、映射由测试逐项钉住？[Measurability, Req §FR-017, Req §FR-018, Req §SC-005, contracts §C-103, contracts §C-104]
- [ ] CHK025 - 「单独不降级」的边界是否全部写明——`缺失` / `为空` 单独出现不触发 5、文件级命名状态（含最新报告不可读）本身不产生原因也不单独改变退出码、`engine-degraded` 仅由引擎读动作失败（binding/锚点）触发、无集合外退出码？[Clarity, Req §FR-018, contracts §C-104, contracts §C-306]
- [ ] CHK026 - 退出码 4（定义损坏）与退出码 5（降级）在同一输入上并存时的**优先级/边界**是否被规定？两份语义都声明「既有」保留，但需求未给「二者同时成立时哪个胜出」，也未声明该组合是否不可达——这是本需求集唯一未闭合的退出码接缝。[Gap, Conflict, Req §FR-018, Req §FR-025]
- [ ] CHK027 - 三面一致性是否要求三方（`docs/reference/commands/team.md` 的 View Mode、`skills/internal/view-team/SKILL.md` 的错误导航行、程序 `--help`/模块声明）各自点名两个原因 id 并引用同一 owner 契约，且允许「指向单一 owner 的指针」形态并须由测试断言？[Completeness, Req §FR-020, contracts §C-109]

## 六、金标准输出与兼容/迁移（Golden output / compatibility / migration）

- [ ] CHK028 - `FR-022` 是否具备封闭声明的全部要素——基线参照物（提交 `54c6efa8c` 的程序）、健康谓词（三键 binding、全部紧凑 `-report.md`、无残留、`agent` 列、无 `goal`、报告可读）、空允许增量、同 fixture 机器 diff + 退出码相等——且允许增量只适用于不满足谓词的输入？[Measurability, Req §FR-022, Req §A-10, Req §SC-004, contracts §C-107]
- [ ] CHK029 - 对不满足健康谓词的输入，`A-11` 的「具名纠正增量」是否枚举到可判定（哪些输入形态、哪些输出会变），使「其余不变」这类未定义聚合确实不承载验收语义？[Consistency, Measurability, Req §FR-022, Req §A-11]
- [ ] CHK030 - 健康谓词的 goal 条件是否自洽？`FR-022` / `A-10` 写「无**内联** `goal`」，`C-107` 与 clarify 裁决写「无 `goal` 键」，而 `FR-013` 要求**任何**已声明 `goal` 键（含 slug 形态）都呈现命名状态——一个 `goal: <slug>` 的团队在「无内联 goal」读法下必须逐字节保真，却按 `FR-013` 必须新增状态行，两条 MUST 不能同真；需求文本应采用哪一种读法？[Conflict, Consistency, Req §FR-022, Req §A-10, Req §FR-013, Req §Clarifications (2026-11-26 clarify session), contracts §C-107]
- [ ] CHK031 - 无形态变更声明是否可判定——报告命名 owner（`create-team` § Report contract）与 `team.md` schema 相对基线不动、既有团队零迁移、所有曾合规的名字仍是运行报告、任何未来的形态变更必须同批附带迁移或确定性拒绝——且「形态变更」本身的边界是否定义到能判断何时触发该义务？[Completeness, Ambiguity, Req §FR-023, Req §A-3, contracts §C-108]
- [ ] CHK032 - 加性呈现规则是否写明——六组标题与既有行全部保留、新增状态行只增不删/不重排/不合并、`view-team` 技能的「程序 stdout 逐字重发 + 正文外降级说明」规则不变，且降级说明不得替代/删减/改写六组正文？[Completeness, Req §FR-025, contracts §C-308, contracts §C-409]

## 七、单引擎、只读边界与非功能依赖（One engine / read-only / NFR）

- [ ] CHK033 - 单一读取引擎是否以**可判定检测面**表述——恰有一个 `classify_runs()` 定义与一个编译后的时间戳语法、单团队与概览都经该入口取得分类/最新/规范化值、源码树中不存在第二匹配规则/第二读取器/第二存储/缓存/快照/索引/registry？[Measurability, Req §FR-021, Req §FR-006, contracts §C-102, data-model §INV-01, data-model §INV-02]
- [ ] CHK034 - `goal-utils.py` 的零修改边界与只读动作白名单（`binding team <slug>`、`list`、`targets <anchor-slug> --list`）是否写明，view 不调用 `bind` / `migrate`，使「零修改 + 仅三读」可被源码扫描判定？[Completeness, Req §FR-021, Req §RS-004, contracts §C-101]
- [ ] CHK035 - 只读性是否以可测量的方式写出——不写文件/不建目录/不派发席位/不登记 run line/不联网，healthy / degraded / overview 三场景前后 fixture 内容哈希一致（新增/修改/删除 = 0），`-h` / `--help` / `--version` 退出 0 且零写盘？[NFR, Req §SC-007, Req §FR-012, contracts §C-101, contracts §C-106]
- [ ] CHK036 - 非功能依赖边界是否闭合——零新增第三方依赖、CPython `>=3.8` 标准库内实现、测试经唯一入口 `scripts/bash/run-tests.sh`，且 RS-001 的 joint acceptance 可机械判定？[Dependency, NFR, Req §RS-001, Req §RS-002, Req §RS-003, Req §FR-021, plan §EP-001]

## 八、可测量性、覆盖与追溯（Measurability / coverage / traceability）

- [ ] CHK037 - `SC-001` / `SC-002` / `SC-003` 的断言是否全部量化且各自点名测量来源——5/5 分类、冒充最新 = 0、13/13 识别、状态 ≠ 为空/缺失且退出 0、六个具名状态、9/9 成员、`/speckit.team modify` ≥ 1、编造零值/占位值 = 0？[Measurability, Req §SC-001, Req §SC-002, Req §SC-003, Req §Measurement Sources]
- [ ] CHK038 - `SC-004` / `SC-005` / `SC-006` 是否可被机器读数判定——stdout diff 行数 = 0 且退出码相同、2/2 映射 + 集合外取值 = 0 + 仅缺失/为空退出 0（1/1）+ help/version 零写（2/2）、概览与单团队 token 一致率 100% + 源码识别入口数 = 1？[Measurability, Req §SC-004, Req §SC-005, Req §SC-006, Req §Measurement Sources]
- [ ] CHK039 - `SC-007` / `SC-008` 是否各自可复算——三场景工作树哈希差 = 0；新增与既有相关测试经 `run-tests.sh` 一次执行退出 0，且覆盖 FR 点名的全部形态（非标准命名、辅助产物、残留、不确定性、缺 binding、内联 goal、缺 agent 列、缺失产物、不可读报告、健康保真）？[Measurability, Req §SC-007, Req §SC-008, Req §Measurement Sources]
- [ ] CHK040 - 追溯与单一活所有者是否闭合——每条 FR/SC 有唯一 ID、每条 `[[STR-NNN]]` 引用解析到 Shared Strings 行且 `Consumed by` 准确、每条契约条款引用到至少一个 FR、渲染标签词汇表以 `view-labels` 契约为唯一活 owner 且 103 的 data-model / program contract 降级为日期化记录（不再被引用为活 owner）、RS-001…RS-005 行的 Form / FR / Premises 单元格可解析？[Traceability, Consistency, Req §FR-024, Req §A-15, Req §Shared Strings, Req §Runtime Stack, contracts §C-401, contracts §C-404]

## Notes

- **勾选与判读**：`[x]` 表示该问题已依据需求文本（或点名的 owner 行 / plan 前提）得到回答；答「否」即对 `requirements.md` 的 finding，不是一条实现任务。本阶段交付的是清单器械；逐条作答属于 analyze / review 的判定职责。
- **计数（footer）**：共 **40 条**，CHK001…CHK040；**40/40（100%）** 携带至少一个追溯锚（`[Req §…]` / `contracts §C-NNN` / `data-model §…` / `[Gap]` 等），满足 ≥80% 下限；soft cap 40 未超出；CHK 编号唯一且顺序连续；无 `Verify` / `Test` / `Confirm` / `Check` 开头的实现检验式条目；无仅能靠运行产品回答的条目。
- **维度计数（按每条的主维度，程序读数）**：Completeness **15**、Measurability **7**、Gap **4**、Consistency **4**、Clarity **3**、Dependency **2**、Coverage **1**、Ambiguity **1**、Conflict **1**、NFR **1**、Traceability **1** ＝ 40；逐条归属见 `../test-evidence/checklist-selfcheck.txt`。
- **章节计数**：一 8（CHK001–CHK008）/ 二 6（CHK009–CHK014）/ 三 5（CHK015–CHK019）/ 四 3（CHK020–CHK022）/ 五 5（CHK023–CHK027）/ 六 5（CHK028–CHK032）/ 七 4（CHK033–CHK036）/ 八 4（CHK037–CHK040）＝ **40**。
- **覆盖矩阵（FR，25/25）**：FR-001 CHK001；FR-002 CHK004；FR-003 CHK002,CHK003,CHK007；FR-004 CHK003；FR-005 CHK006,CHK007,CHK014；FR-006 CHK004,CHK008,CHK033；FR-007 CHK010；FR-008 CHK011,CHK012；FR-009 CHK013；FR-010 CHK009,CHK014；FR-011 CHK015；FR-012 CHK016,CHK035；FR-013 CHK017,CHK030；FR-014 CHK018；FR-015 CHK020；FR-016 CHK021,CHK022；FR-017 CHK023,CHK024；FR-018 CHK013,CHK024,CHK025,CHK026；FR-019 CHK019；FR-020 CHK027；FR-021 CHK033,CHK034；FR-022 CHK028,CHK029,CHK030；FR-023 CHK031；FR-024 CHK040；FR-025 CHK026,CHK032。
- **覆盖矩阵（SC，8/8）**：SC-001 CHK004,CHK005,CHK037；SC-002 CHK037；SC-003 CHK037；SC-004 CHK028,CHK038；SC-005 CHK024,CHK038；SC-006 CHK004,CHK038；SC-007 CHK035,CHK039；SC-008 CHK039。
- **覆盖矩阵（契约条款，35/35）**：C-101 CHK034,CHK035；C-102 CHK033；C-103 CHK024；C-104 CHK023,CHK024,CHK025；C-105 CHK023；C-106 CHK035；C-107 CHK028,CHK030；C-108 CHK031；C-109 CHK027；C-201 CHK001；C-202 CHK001,CHK002；C-203 CHK004；C-204 CHK004；C-205 CHK003；C-206 CHK006；C-207 CHK008；C-208 CHK013；C-301 CHK015,CHK016；C-302 CHK017,CHK018；C-303 CHK020,CHK021,CHK022；C-304 CHK010；C-305 CHK011,CHK012；C-306 CHK013,CHK025；C-307 CHK009；C-308 CHK032；C-309 CHK019；C-401 CHK040；C-402 CHK009；C-403 CHK021,CHK022；C-404 CHK040；C-405 CHK014；C-406 CHK003,CHK014；C-407 CHK021；C-408 CHK009；C-409 CHK032。
- **机械读数（2026-11-26，本阶段当场取证）**：`validate-requirements.py` → `status: ok`，**239 行 / 33 definition rows / 3 shared strings / 0 error / 0 warning**（`../test-evidence/checklist-requirements-validator.txt`）；程序计数（`../test-evidence/checklist-spec-readings.txt`）：25 FR / 8 SC / 3 STR / 17 A / 3 US / 12 Edge Cases / 5 RS；`contracts/` 4 文件 35 条款（9+8+9+9）；`plan.md` 9 EP；`tasks.md` 29 任务行；`quickstart.md` 8 场景；`data-model.md` 10 实体 / 10 不变量。
- **清单自检**：`../test-evidence/checklist-selfcheck.txt` 记录本文件的程序读数（条目数、追溯锚覆盖、FR/SC/条款覆盖、禁用开头、编号连续性）。
- **same-author 检测门**：不成立（见 Detection path）；未派发 fresh-context 检测代理（角色模板与派发均明令不得再派发），检测路径如实记录，不以委托路径冒充直接读。
- **本阶段无 plan-owned 改动**：本文件位于 `checklists/`；`plan.md` / `data-model.md` / `contracts/` / `quickstart.md` / `research.md` / `feature-ref.md` 未被触碰，故无 `PLAN-EDIT:` 声明。
- **新增而非覆盖**：本文件为 checklist 阶段**新增**清单；requirements 阶段产出的 `checklists/requirements.md` 保持原样（未被覆盖、未刷新）。同轮不生成 recheck 文件（本阶段无「回答早前条目」的动作）。
- **待下游裁定的观察（不阻塞本阶段）**：本清单的 `[Gap]` / `[Ambiguity]` / `[Conflict]` 条目指出的候选确认点——需求层的示例上限量化（CHK003）、`SC-001` fixture 枚举与 5/5 的复算（CHK005）、未声明 pattern 的「缺省语义」读法（CHK012）、重复 `agent` 列的触发面（CHK020）、`seats`/`stage_seats` owner 指针的具体化（CHK022）、退出码 4 vs 5 的优先级（CHK026）、健康谓词 goal 条件的两种读法（CHK030）、「形态变更」的边界（CHK031）——由 `/speckit.analyze` 或实现阶段按判据取证，不在本阶段预先裁定。
- **Feature 状态**：本轮位于 `/speckit.implement` 之前，按 Feature Integration Protocol，checklist 不发起 `Implemented → Ready for Review` 迁移，仅产出清单；`.specify/features.md` 行 108 维持 `Planned`，父行 027 维持 `Ready for Review`。
