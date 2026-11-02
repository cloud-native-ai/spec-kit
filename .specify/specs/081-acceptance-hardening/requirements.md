# Requirements Specification: Stricter Acceptance & Artifact Review（更严格的验收与产物审查）

**Requirement Branch**: `081-acceptance-hardening`
**Created**: 2026-11-01
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "推进 spec-kit 框架更严格的验收标准（Phase 1-4 整合为一个特性）：(1) 让 Implemented 不再可能零通过——requirements 的每条 SC 标注 Path: final|supporting，Planned→Implemented 要求所有 final 路径 SC 为 pass，并新增 Blocked 状态与 blocked 验证词表（含 reduced measurement 阶梯）；(2) 每个 execution 特性必须有一条确定性最小 smoke test，记录命令/退出码/证据路径；smoke test 跑不起来即 Blocked 而非 Implemented；(3) 新增确定性 closure-acceptance-check.py，以封闭原因集输出 accept|block，被 implement / review / sdd-loop-driver 的 closure 与 merge 门调用；(4) 运行时栈/依赖所有权表（requirements）与执行前提/继承 blocker 表（plan）成为结构化一等产物，pre-analyze-check 增加对应确定性发现；(5) /speckit.review 从「只回顾 SDD 流程」扩展为同时审查各阶段产物本身与实现/diff/smoke 结果，并新增 Acceptance Reality Check 与 Implemented→Ready for Review 的第四个条件；(6) 词表/注册表/迁移/文档/镜像同步：Blocked 进入三处词表 owner、--audit-existing 只读审计、命令模板与逐工具副本及镜像重生成、CHANGELOG 与 owner 指针更新、pytest 契约/单元测试与正负夹具。非目标：不改阶段序列与哨兵、不回写历史状态、不新增第二套并行门禁、不替换 code-review 技能、不削弱 partial/deferred 的诚实性。"

## Related Feature *(mandatory)*

**Feature ID**: 081
**Feature Name**: 更严格的验收与产物审查（Stricter Acceptance & Artifact Review）

**Binding basis**: `/speckit.clarify` Mode A 按 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules 扫描候选人后判定无归属，新建 Feature 081；详情落在 `.specify/memory/features/081.md`，索引行由 `.specify/memory/features.md` 承载（`Total Features` 与行数同趟重算）。候选人复核与 ID 取值的裁决见 `## Clarifications` § Session 2026-11-03。

## Assumptions（clarify 阶段逐条裁决；每条给出裁决、证据与对产物的影响）

裁决语法：**ratified** = 原假设成立、证据在仓内可复核；**revised** = 前提成立但表述或边界需改写，改写内容即该条正文；**superseded** = 该假设要交给后续阶段做的事已在本阶段完成。没有一条被静默丢弃。

- **A1（类别判定 = execution，basis = behavior-oracle）— 裁决：ratified**。主交付物是确定性脚本、门禁条款与命令模板；缺陷最先在机器面暴露（checker 对被禁止的特性返回 `accept`、门禁放行一个 final-path 全未通过的切片、`--check` 退出码非 0），按 `.specify/shared/definitions/flow-class-definitions.md` § 判据属 `execution`，`Flow Type` 写 `-`。产物中包含大量 Markdown（模板、文档），但介质不参与判定（owner §不参与判定的因素）。**证据**：`python3 .specify/scripts/python/flow-class-check.py --action lookup --unit-id "spec:081-acceptance-hardening"` → `flow_class: execution` / `flow_type: -` / `source: declaration` / `marker: null` / exit 0——类别由本文件头部声明行解析，不依赖任何注册表行。
- **A2（Feature 绑定）— 裁决：superseded（本阶段已执行）**。原表述「`Related Feature` 保持 `Need clarification`，预计新建」由本阶段兑现：已按 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules 落定**新建 Feature 081**，并写出详情文件与索引行。**候选人复核**：本仓 `features.md` 的 026 是「Agent Skill Enablement」（spec 025），055 是「冲突无关存储」，062 是「Humanize Command」（spec 080 绑定的目标），071 是「Review × Code-Review 组合」但只治理**两段**的既有组合与严重度不互转，077 是「文档型阶段门禁」、079 是「双语表述」——均不覆盖「final 路径阈值 + smoke 硬条件 + 三处共享判定 + 产物/实现审查」这一组合，故 create 而非 bind。
- **A3（review 组合结构）— 裁决：revised（结构从「两段」改为「四段 + 一次确定性判定」）**。
  - **终态组合与固定顺序**：① 过程段 `review-sdd-process`（保留）→ ② 产物段（新增）→ ③ 实现段（新增）→ ④ 代码段 `code-review`（保留）→ ⑤ **Acceptance Reality Check**（不是段，是确定性判定）。
  - **各段判定对象**：① = 产出该切片的 SDD 流程本身（流程与工具质量，不是业务价值，也不是代码）；② = 当次存在的每个阶段产物本身（完整性、内部一致性、可追溯性、依赖与前提所有权、验收诚实性）；③ = 本次实现本身（`base..head` 的实现相对 requirements 与 tasks 的正确性、范围与回归，并实跑或核验 smoke 并记录命令／退出码／证据路径）；④ = 该切片已提交代码 delta 中可验证的缺陷；⑤ = 「声称的特性状态」与「final 路径实际通过数」是否对得上。
  - **顺序理由**：过程段无条件先跑且最便宜，它交代切片是怎么被做出来的；产物段只读已在盘上的文件；实现段需要 `base..head` 且要实跑 smoke（最贵），排在读盘之后；代码段是最深的 diff 阅读，放在实现段之后以免与实现段的结论抢跑；ARC 最后，因为它裁决的是**声称的状态**与前面各段已确立的证据之间的差额，早跑等于在证据产生前下判断，且它直接压住 `Implemented → Ready for Review` 的翻转点。
  - **职责边界（MUST 在该 owner 内声明）**：`review-sdd-process` MUST NOT 被当作产物段或实现段的替代；实现段 MUST NOT 由代码段代答，代码段 MUST NOT 由实现段代答（两段各自成文、各自定级、互不转换）；ARC 的判定 MUST NOT 由任何模型判断代替，它只读 `verification.md` 与特性状态；段数与顺序是模板属性，`$ARGUMENTS` 不得选择跳过任一段。`code-review` 仍保留（FR-014 明文「MUST NOT 替换」），故终态是**四段 + 一次判定**而非三段。
  - **owner 改写点**：`templates/commands/review.md` § Composition 现以「two segments, one fixed order」把「恰好两段」写成封闭结构，`## Delegation` 亦写明「Each segment is delegated to its existing skill」。本特性 MUST 在该 owner 内改写标题句、段数断言与 Delegation 形态，并逐段补出 ②③ 两段的 Skill／判定对象／严重度／输入／输出五项，以及 ⑤ 的调用点与产出（三计数 + 固定 P0）。
  - **本阶段不改源**：Two Hats——该改写属框架源（`templates/commands/review.md`，逐工具副本由 `scripts/python/regen-command-copies.py` 重生成），是 plan/implement 阶段的义务；clarify 阶段只把它写成 `requirements` 的强制条款（FR-013），MUST NOT 在本阶段手改模板，也 MUST NOT 以手改 `.specify/` 镜像代替。
- **A4（`Path` 标注的落位）— 裁决：ratified 并收紧**。标注写在 SC 定义行内（`- **SC-001**: … **Path**: final`），不新增独立小节表：`Path` 是每条 SC 的属性而非全局集合，行内标记不需要第二处与 SC 列表保持同步的表（否则违反一源）。**确定性可解析性证据**：`scripts/python/validate-requirements.py` 的 `DEFINITION_RE = ^- \*\*(FR|SC)-(\d+)([a-z]?)\*\*` 锚定行首、不消费冒号之后的内容；`skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` 的 `SC_DEF = ^- \*\*SC-(\d{3})\*\*:` 同样只锚前缀——两处解析器都容得下行尾标记。**收紧条款**：标记 MUST 是 SC 定义行的**最后一个 token**、形如 `**Path**: final` 或 `**Path**: supporting`，每行恰好出现一次；行中不得出现第二处 `**Path**`。closure checker 按该形态机械解析，取二值之外或缺失即判不合格（FR-001）。
- **A5（`blocked` 字面的四处不同语义）— 裁决：ratified**。四处封闭集与 owner 各自独立：特性状态 `Blocked`（owner `templates/feature-details-template.md` § Canonical Status State Machine）、verification 行 `blocked`（owner `templates/verification-log-template.md`，其词表现为 `pass|fail|partial|deferred|unknown`）、线状态 `blocked`（owner `skills/external/sdd-loop-driver/scripts/line-registry.py` 的 `STATE_VALUES`）、任务行 `[blockedBy: …]`（owner `templates/tasks-template.md`，该处是**任务依赖标签**、不是状态）。本特性新增其中两处（特性状态、线状态），各处写进自己的 owner；调和结论只落一处（FR-019）。
- **A6（线状态集的扩张）— 裁决：revised（给出八项具体处置，并更正一处用词）**。`STATE_VALUES` 现为封闭集 `{active, waiting, stalled, completed, orphaned, stale, closed}`。**用词更正**：该文件内不存在名为 `revival` 的符号或动作（`grep -n "revive\|revival"` 零命中），原假设中的「revival」实指 `promote-waiting` 与 `ownership-check` 两条恢复路径，本规格一律用后者命名。八项处置（plan 必须逐项落地，FR-017 的断言覆盖）：
  1. `STATE_VALUES` 加入 `blocked`（7 → 8 个取值）。
  2. `ACTIVE_STATES = {active, waiting}` **不变**：`blocked` 不是活跃态——它不进 `--active` 列表（`action_list`）、不进 `_active_entries`、不占并发槽（`promote-waiting` 的 `active` 计数只看 `state == "active"`）。
  3. `HOLDING_STATES = {active, completed}` **不变**，但 MUST 声明 `blocked` 不持有任何资源：转入 `blocked` 时 MUST 释放 lease 并清空 `holder_line_id` / `waiting_reason`（与 `closed` 同款清理），否则阻塞线会像泄漏的 lease 一样把等待者钉死。
  4. `merge_ready`：`merge_ready=true` 要求 `state=completed` 的既有前置**不变**；新增不变量 `state=blocked ⇒ merge_ready` MUST NOT 为真（在同一校验点断言，不靠前置隐式排除）。
  5. `integration-enqueue` / `integration-plan` / `integration-record` 均要求 `state=completed`，**不变**：`blocked` 线结构性不可入队、不可记录合并结果。
  6. **终态守卫集 `{closed, stale, orphaned}` MUST NOT 加入 `blocked`**（`ownership-check`、`release-ownership`、`allocate-resources`、`archive-runtime` 等处的 `not in {closed, stale, orphaned}` 守卫）：那三值语义是「不可再动作」，而 `blocked` 按设计可恢复，恢复路径是既有的 `update --state active` 并记 unblock 原因。
  7. `promote-waiting` 要求 `state == "waiting"`，**不变**：`blocked` 线不得经该动作直接复活，也不得绕过 `ownership-check` 的重新取权。
  8. `deregister --reason stale-cleanup` 会写 `stale_from_state = <前值>`；MUST 声明该字段可承载新值 `blocked`（不需要枚举扩张，但要写进注释与测试）。
  - 不引入任何「线状态不再回退」规则：线状态集本就没有 never-regress 语义，本特性不为它新增一条。
- **A7（新 schema 的单一 owner 落点）— 裁决：ratified**。两张新表（运行时栈/依赖所有权、执行前提与继承 blocker）以及 `Path` 标注、封闭原因集的 schema，owner 只有一个文件 `shared/workflow/acceptance-hardening.md`（该路径当前不存在，是 FR-022 的交付物；目录 `shared/workflow/` 已存在且承载同类规范文档）；其镜像由 mirror 引擎生成，其余模板/命令/技能只引用路径与章节锚。
- **A8（冻结集）— 裁决：revised（收窄）**。原表述把「loop 的 U0–U6 流程全部冻结」写死，与 FR-017 冲突：FR-017 明确要求 driver 的 closure/merge 步改跑 [[STR-005]] 并在 [[STR-007]] 时把线标 `blocked`，那正是 U6 内的判定变化。收窄后的冻结集：阶段序列、阶段哨兵、watcher 语义、test-budget 槽位、U0–U6 的**阶段骨架与顺序**冻结；**唯一例外**是 closure/merge 步的判定来源（改由 [[STR-005]] 给出）与线状态集（加 `blocked`）。历史特性状态与历史 verification 记录仍不回写（审计只读）。
- **A9（零 clarification marker）— 裁决：ratified**。本规格不含 `[NEEDS CLARIFICATION]` 标记；`validate-requirements.py` 的 `marker-count` 项 pass。开放点全部在仓内可裁决（现有 owner 文档、`line-registry.py` 的封闭集、`review.md` 的组合声明），裁决记于本节。
- **A10（语言）— 裁决：ratified**。正文中文；契约面字面量（脚本路径、命令、状态值、原因标签、列名）一律英文原样，MUST NOT 翻译或音译（本文件自身即样本）。
- **A11（`026` 是外部事故的代称，不是本仓可核验的特性）— 裁决：新增（clarify 补齐）**。本规格四处以「026」指代触发本特性的事故，但该编号在本仓不可核验：本仓 `features.md` 的 026 是「Agent Skill Enablement」（bound spec 025），`.specify/specs/` 下不存在 `026-*` 目录，规格树内只有本文件引用这个编号。因此 026 的**规范内容**以本规格的内联重述为准——「任务全关 + 每条 SC 有状态行 + final 路径 SC 全 `blocked`/`deferred`」「运行时外部化成散文」——任何产物 MUST NOT 把 026 当作可核验证据引用，也 MUST NOT 补造其细节。Feature 081 的详情文件同样只按内联重述记录该形态。
- **A12（review 新增两段的严重度与载体）— 裁决：新增（clarify 补齐）**。不新增第三套严重度词汇：产物段与实现段产出 `P0`/`P1`/`P2`（owner `skills/internal/review-sdd-process/SKILL.md`），代码段继续用自己的六级（owner `skills/internal/code-review/SKILL.md`），ARC 的 [[STR-016]] 固定为 `P0`；两个家族之间仍无映射表、无转换、无统一分数。方法论载体 MUST 是一个能以运行时路径抵达的具名 owner（首选新增内部技能，沿用 owner 现有「段 → 技能」形态），`templates/commands/review.md` MUST NOT 内联方法论；载体究竟是新技能还是既有技能下的命名文档，由 plan 决定并记录。
- **A13（三张「前提／环境」表不叠位）— 裁决：新增（clarify 补齐）**。`templates/tasks-template.md` § Environment Prerequisites 已声明自己是「probe conclusions 的唯一落地处」。若不划界，FR-010／FR-011 会造出第二处 owner，直接违反 FR-019／FR-022。边界：plan § Execution Premises = 计划期承重前提及其证据状态；plan § Inherited Blockers = 依赖特性详情里的 `## Deferred`／blocked 记录及本特性的处置；tasks § Environment Prerequisites = 任务生成期的环境探针判决（带探测命令与日期）。三者判定对象互斥，同一事实 MUST 只落一处，其余以 `(see § …)` 指针引用。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - final 路径没通过就不叫「实现了」，而且必须有 smoke test (Priority: P1)

项目所有者看到某特性在注册表里是 `Implemented` 时，要能确信：它的主用户旅程至少真实跑通过一次，并且有一条一条命令就能跑的 smoke test 作为最低证据。今天这两条都不成立——只要 `tasks.md` 的复选框全关、每条 SC 有一行状态（哪怕是 `partial` / `deferred` / `unknown`），特性就能翻成 `Implemented`。

**Why this priority**: 这是本特性的定义性价值。没有它，后三条用户故事都只是给一个没有阈值的门禁加装饰。

**Independent Test**: 取一个「任务全关 + 每条 SC 有状态行 + 所有 final-path SC 都是 `blocked`/`deferred`」的夹具，分别触发 implement、review、driver closure 三处门，检查三处全部拒绝并各自给出封闭原因集内的命名原因；再取一个「final-path SC 全 `pass` + 合格 smoke 记录」的正夹具，检查三处全部放行。

**Acceptance Scenarios**:

1. **Given** 一个 `tasks.md` 零 `[ ]`、`verification.md` 每条 SC 都有状态行、但所有 final-path SC 均为 `blocked` 或 `deferred` 的特性，**When** `/speckit.implement` 尝试 `Planned → Implemented`，**Then** 转移被拒绝，产出的原因取自封闭原因集（含 [[STR-008]]），特性状态 MUST NOT 被写成 `Implemented`。
2. **Given** 同一个夹具，**When** `/speckit.review` 与 `sdd-loop-driver` 的 closure/merge 步各自运行 [[STR-005]]，**Then** 两处都输出 [[STR-007]]，合并被拒绝，且拒绝原因与 implement 处的命名一致。
3. **Given** 一个 final-path SC 全 `pass`、但 `verification.md` 里没有 smoke 命令与退出码的特性，**When** 尝试进入完成态，**Then** 该特性 MUST 被判为 [[STR-001]]，MUST NOT 被判为 `Implemented`。
4. **Given** 一个纯文档（`expression` 类）特性，**When** 走同一条门，**Then** 「必须有 final SC」的要求对它不生效，MUST NOT 因此阻断它，也 MUST NOT 迫使它编造一条 final SC。

---

### User Story 2 - 「运行时由 X 提供」必须是一行可验收的记录，已知的坏前提必须被继承 (Priority: P1)

产品所有者要能回答两个问题：这个特性依赖的运行时栈归谁、由谁联合验收；以及它所依赖的其它特性已经测出的坏结论有没有被处置。今天两个问题都只能靠散文回答：一句「由 A 线／某仓提供」可以顶替任何验收责任，而一条已知的负面实测结论可以被降级成「范围外 P2」一行搁置。

**Why this priority**: 与 US1 同级——US1 判「测没测过」，US2 判「测的东西在不在自己手里、已知的坑有没有被继承」。026 的两次失守分别属于这两类。

**Independent Test**: 造三份最小夹具：一份把运行时依赖只写成散文（无表行），一份把 `signed-contract` 行的 pin 与契约路径留空，一份让依赖特性详情里存在一行未处置的 `## Deferred`。分别跑确定性检查，检查三类各自被指名拒绝。

**Acceptance Scenarios**:

1. **Given** 一个 `execution` 特性的 requirements 里只有「本能力由 X 仓提供」这类散文、没有运行时栈表行，**When** 确定性检查运行，**Then** 报 `runtime-dependency-not-owned` 并阻断下一阶段。
2. **Given** 一行 `Form` = `signed-contract` 但缺 contract 路径、pin 或具名联合验收 owner，**When** 确定性检查运行，**Then** 该行被指名拒绝。
3. **Given** 依赖特性详情里有一行 `## Deferred`，而本特性 plan 的继承 blocker 表没有处置它，**When** 确定性检查运行，**Then** 报 `inherited-blocker-undisposed` 并给出该行的出处。
4. **Given** plan 里有一条 `Status` = `falsified` 但没有 `Decision`，**When** 确定性检查运行，**Then** 报 `falsified-premise-undecided`。

---

### User Story 3 - review 既审「这次 SDD 做得对不对」，也审「产物和实现本身对不对」 (Priority: P1)

维护者跑 `/speckit.review` 时，要拿到的不只是一份流程回顾，而是三件事：各阶段产物本身有没有缺陷（完整性、一致性、可追溯、所有权、验收诚实性）；这次实现（diff）是否满足需求与任务；以及「声称的状态」与「final 路径实际通过数」是否对得上。

**Why this priority**: US1 让门禁有阈值，US3 让 review 真的能看见阈值被绕过的地方——只在门禁上加阈值、review 仍只看流程，等于把唯一的发现窗口关掉。

**Independent Test**: 对一个刚实现的切片跑一次 review，检查 `review.md` 同时含产物审查段（覆盖当次存在的每个阶段产物）、实现审查段（含 smoke 命令、退出码、证据路径）与 Acceptance Reality Check 的 final-path 计数；再用一个「声称 `Implemented` 但 final-path 通过数为 0」的夹具，检查产出 P0 级 [[STR-016]] 且拒绝转移。

**Acceptance Scenarios**:

1. **Given** 一个 requirements 里存在一条 FR 没有对应任务、也没有对应证据行的切片，**When** 产物审查段运行，**Then** 产出一条带严重度与「产物路径 + 行号」定位的 finding。
2. **Given** 一次 `base..head` 的实现 diff，**When** 实现审查段运行，**Then** 它运行或核验 smoke test 并记录命令、退出码与证据路径；MUST NOT 以 `code-review` 的通用 delta 评审代替该段。
3. **Given** 一个声称 `Implemented` 而 final-path `pass` 计数为 0 的夹具，**When** Acceptance Reality Check 运行，**Then** 产出一条 P0 [[STR-016]]，`review.md` 记录 `pass` / `blocked` / `deferred` 三个计数，且 `Implemented → Ready for Review` 被拒绝。

---

### User Story 4 - 词表、注册表、迁移、文档与镜像一起对齐 (Priority: P2)

框架维护者要能安全地把这套新规则铺进一个已经在跑的老仓库：`Blocked` 出现在该出现的三处词表里，`--audit-existing` 只读地报出「按新规则会变 Blocked」的现有特性，逐工具副本与镜像由生成器重生成而不是手改，`CHANGELOG` 与各 owner 指针都指回同一个 owner。

**Why this priority**: P2——它是前三条的落地卫生。没有它，新规则会以「某处词表没有 `Blocked`」「镜像与源不一致」的形式退化成局部约定。

**Independent Test**: 在既有仓库上跑 `--audit-existing`，检查零写入、历史状态零变更、输出清单带原因列；再跑两个 `--check`（逐工具副本、镜像），检查 exit 0。

**Acceptance Scenarios**:

1. **Given** 一个含历史 `Implemented` 特性的仓库，**When** 运行 `--audit-existing`，**Then** `git status --porcelain` 增量为空、历史状态零变更，且输出逐条列出「会变 `Blocked`」的特性与原因。
2. **Given** 一份手工改过 `.specify/skills` 镜像的树，**When** 跑镜像引擎的 `--check`，**Then** exit 非 0，且手改镜像不是本特性允许的主改动方式。
3. **Given** 一个新的状态值 `Blocked`，**When** 检查三处词表 owner，**Then** 三处都含该值且语义一致；状态机转移表含新增的转移行与审计纠正例外。

### Edge Cases

- **特性文件缺失**：closure checker 在 `verification.md` 不存在或不可解析时 MUST 以退出码 2 表示输入错误，MUST NOT 把它读作 [[STR-006]]。三处调用点都在 `Planned` 之后，因此「缺文件」永远是缺陷而不是正常态。
- **只有 supporting SC 的表达类特性**：`final` 路径规则对它是空真——MUST NOT 被读成「必须编造一条 final SC」，也 MUST NOT 因此让它永久停在 [[STR-001]]。
- **smoke test 需要外部环境**：不得因为「需要真集群／真网络」而放行。要么用本地夹具把它做成确定性命令，要么特性为 [[STR-001]]。这与 `partial` 的诚实性一致：加了阈值，没有删除任何状态。
- **reduced measurement 存在却未运行**：`blocked` / `deferred` / `partial` 行写了 `reduced_measurement` 却把 `reduced_measurement_run` 记成 `no`，判该行非法（「诚实」不构成可接受）。
- **用户显式豁免**：`Implemented → Ready for Review` 的第四个条件允许用户豁免，但豁免 MUST 落在该转移 owner 已声明的可核验载体上；agent 的确认不是用户裁定，无异议也不是豁免。
- **final 与 supporting 混合**：只要有一条 final SC 非 `pass` 即 [[STR-007]]，原因点名该 SC；supporting SC 的非 `pass` 不单独阻断。
- **审计遇到历史遗留的「零通过但 Implemented」**：`--audit-existing` 只报告，MUST NOT 改写历史状态，也 MUST NOT 以其发现阻断其它阶段的正常运行。
- **review 的实测结论不得充当 implement 的门禁输入（循环）**：任何 SC 若只能在 review 阶段测量，MUST NOT 被记为 [[STR-003]]；否则 `Planned → Implemented` 要求它 `pass`，而它要等 review，`Blocked → Ready for Review` 又非法（FR-003），门禁自锁。本规格据此把 SC-006 保持在 [[STR-004]]（见该 SC 的 Path 裁决）。
- **三张「前提／环境」表不得叠位**：plan § Execution Premises、plan § Inherited Blockers 与 `templates/tasks-template.md` § Environment Prerequisites 的判定对象互斥，同一事实 MUST 只落一处、其余以 `(see § …)` 指针引用；同一事实出现两处即「一源多写」缺陷（承载 FR-019、FR-022）。理由见 A13。
- **线 `blocked` 与 `merge_ready` 互斥**：`merge_ready=true` 要求 `state=completed`；一条线一旦被判 [[STR-007]] 并标 [[STR-002]]，其 `merge_ready` MUST NOT 为真。两者同时为真即闭合判定被绕过，MUST 判为缺陷而不是「历史残留」。

## Requirements *(mandatory)*

### Functional Requirements

#### A. final 路径验收、`Blocked`、smoke test 与 closure checker（US1）

- **FR-001**: `requirements.md` 中每条 SC 定义行 MUST 携带 `Path` 标注，取值取封闭二值 [[STR-003]] 与 [[STR-004]]：`final` = 该 SC 证明特性的主用户旅程／产品流程可用；`supporting` = 辅助质量、卫生、文档或非阻断证据。每个 `execution` 类特性 MUST 至少有一条 [[STR-003]] SC；`expression` 类特性不受该下限约束。标注 MUST 写在 SC 定义行内、作为该行最后一个 token（形态 `**Path**: final`，每行恰好一次），使确定性校验器能判定（解析器容差见 A4）；缺失、出现两次或取二值之外的值即不合格。
- **FR-002**: `Planned → Implemented` MUST 为四条件合取：① `tasks.md` 零 `[ ]`；② 每条 SC 有 verification 状态行；③ **每条 [[STR-003]] 路径 SC 的状态为 `pass`**；④ 该特性的基本 smoke test 为 `pass`。该转移的判据 owner 仍是 `templates/feature-details-template.md` § Canonical Status State Machine，其他产物 MUST 只引用不复制。
- **FR-003**: MUST 新增 [[STR-001]] 为一等特性状态并写入上述 owner 的转移表：`Planned → Blocked`（任务已关闭但至少一条 [[STR-003]] 路径 SC 非 `pass`）；`Blocked → Implemented` 仅在 blocker 解除且 [[STR-003]] 路径 SC 全 `pass` 时允许；`Blocked → Ready for Review` MUST 非法；`Implemented → Blocked` 仅允许作为审计纠正，且 MUST 引用证据。
- **FR-004**: `templates/verification-log-template.md`（词表 owner）MUST 增加 [[STR-002]] 并给出与 `deferred` 的区分：`blocked` = 环境无法测量该断言、因此特性不可验收；`deferred` = 本轮未尝试但特性仍可验收（仅限 `supporting` 路径）。`blocked` / `deferred` / `partial` 行 MUST 携带 `blocked_at`（或原因）、`reduced_measurement`、`reduced_measurement_run=yes|no`、`why_reduced_insufficient`、`unblock` 五项；当存在可用的 reduced measurement 而 `reduced_measurement_run=no` 时该行 MUST 判为非法（对应命名原因 [[STR-010]]）。
- **FR-005**: 每个 `execution` 特性 MUST 在其 `tasks.md` / `verification.md` 中命名**恰好一条**确定性、最小、可复现的 smoke 命令，端到端覆盖该特性的主流程（不是完整 E2E 套件），并记录命令原文、退出码、证据路径三件。本特性（081）的 smoke 命令 MUST 至少覆盖三件事：在临时夹具上运行 `specify init`；对正／负夹具运行 closure checker；运行 `python3 scripts/python/regen-command-copies.py --check`。smoke test 无法运行时该特性 MUST 为 [[STR-001]]，MUST NOT 为 `Implemented`。
- **FR-006**: MUST 交付框架自有的确定性脚本 [[STR-005]]。它读取 `requirements.md`、`plan.md`、`tasks.md`、`verification.md`、特性注册表／详情与依赖特性详情，输出 [[STR-006]] 或 [[STR-007]]；`block` 时 MUST 给出**封闭原因集**中的命名原因：[[STR-008]]、[[STR-009]]（后接 `SC-NNN`）、[[STR-010]]（后接 `SC-NNN`）、[[STR-011]]（后接 `RS-NNN`）、[[STR-012]]（后接 `EP-NNN`）、[[STR-013]]（后接依赖特性 ID）、[[STR-014]]。退出码 MUST 区分三态：0 = [[STR-006]]、1 = [[STR-007]]、2 = 输入缺失或不可解析。输出 MUST 同时给出 [[STR-003]] 路径的三计数（`final_pass` / `final_blocked` / `final_deferred`），供 FR-015 的 Acceptance Reality Check 直接引用，MUST NOT 由第二处重新统计。脚本 MUST 只读、stdlib-only、不含模型判断。
- **FR-007**: [[STR-005]] MUST 有 pytest 契约／单元测试与两套最小夹具：① 负夹具复现 026 模式（任务全关、每条 SC 有状态行、final-path SC 全 `blocked`/`deferred`），断言 [[STR-007]] 且原因在封闭集内；② 正夹具（final-path 全 `pass`、smoke 记录齐备），断言 [[STR-006]]。夹具 MUST 是声明式最小文件集（requirements/plan/tasks/verification/注册表），MUST NOT 依赖真实特性目录。
- **FR-008**: [[STR-005]] MUST 被三处调用：`/speckit.implement`（`Planned → Implemented` 判定前）、`/speckit.review`（`Implemented → Ready for Review` 判定前）、`sdd-loop-driver` 的 closure/merge 步。任一处得到 [[STR-007]] MUST 拒绝该转移或合并并输出命名原因；MUST NOT 用模型判断代替脚本判定。

#### B. 运行时栈／依赖所有权、执行前提与继承 blocker（US2）

- **FR-009**: `execution` 特性的 `requirements.md` MUST 包含强制表 § Runtime Stack & Dependency Ownership，列固定为 `ID | Capability | Form | Owner | Pin | Joint acceptance | FR`；`Form` 取封闭集 `in-scope | signed-contract | user-waived`：`in-scope` MUST 有对应 FR、对应任务与 verification 中的联合验收；`signed-contract` MUST 给出契约路径、pin（commit/digest/version）、外部 owner 与具名联合验收 owner 或命令；`user-waived` MUST 引用用户裁定并写明残余风险。仅以散文声明「由某仓／某线提供」而无表行 MUST 判违规（[[STR-011]]）。`in-scope` 的判据是**本特性交付该能力**；由外部供给、本仓只消费的运行时能力 MUST 记 `signed-contract`（或 `user-waived`），MUST NOT 记 `in-scope`——否则「外部化」只是换了个 Form 值而已。纯文档／表达类特性 MAY 记 `not-required` 并给理由。
- **FR-010**: `plan.md` MUST 包含强制表 § Execution Premises，列 `ID | Premise | Evidence | Status | Decision`；`Status` 取封闭集 `verified | unverified | falsified`；`falsified` MUST 带 `Decision` ∈ `resolve-in-scope | fallback | user-waiver`（缺失即 [[STR-012]]）；每条依赖运行时能力的 FR MUST 引用一个 premise ID。已知的负面结论 MUST NOT 被降级为「范围外 P2/P3」一行搁置。
- **FR-011**: `plan.md` MUST 包含 § Inherited Blockers 表：对每个被依赖特性，其详情中每一行 `## Deferred`／blocked 记录 MUST 被处置为 `resolved | inherited | not-applicable` 并附证据；确定性检查 MUST 从依赖特性详情抽取这些行，任一行未处置即失败（[[STR-013]]）。
- **FR-012**: 四类确定性发现 MUST 落地并被阻断：运行时栈行缺失或为空、`signed-contract` 缺 pin 或契约、`falsified` premise 缺 decision、继承 blocker 未处置。它们 MUST 在 requirements/plan 的 U4 处运行并阻断下一阶段；落地载体是既有 `skills/external/sdd-loop-driver/scripts/pre-analyze-check.py` 或同层框架 checker，MUST NOT 新建第二套并行门禁体系。

#### C. review 审查实现与产物（US3）

- **FR-013**: `/speckit.review` MUST 新增强制**产物审查**：对当次存在的每个阶段产物（`requirements.md`、`plan.md`、`tasks.md`、`contracts/`、`data-model.md`、`quickstart.md`、`verification.md`）判定完整性、内部一致性、可追溯性（FR→task→SC→证据）、依赖／前提所有权与验收诚实性，每条 finding MUST 带严重度与「产物路径 + 行号」定位。`templates/commands/review.md` § Composition 现把「恰好两段、固定顺序」写成封闭结构（原句 `Composition — two segments, one fixed order`），本特性 MUST 在该 owner 内把它改写为**四段加一次确定性判定、固定顺序**（过程段 → 产物段 → 实现段 → 代码段 → Acceptance Reality Check），并逐段声明判定对象与职责边界；组合定义、顺序理由与边界条款以本规格 A3 为准。`review-sdd-process` 的判定对象仍是流程，MUST NOT 被当作产物审查或实现审查的替代。该 owner 改写是 plan／implement 阶段的义务（Two Hats：改框架源并重生成逐工具副本），MUST NOT 在本 clarify 阶段改源，也 MUST NOT 以手改 `.specify/` 镜像代替。
- **FR-014**: `/speckit.review` MUST 新增强制**实现审查**：以 `base..head` 的实现 diff 为对象，对照 requirements 与 tasks 判定正确性、范围与回归，运行或核验 smoke test 并记录命令、退出码与证据路径。该段的判定对象是本次实现本身，MUST 与 `code-review` 的通用 delta 评审、与流程回顾相互区分，且 MUST NOT 替换 `code-review`。两段的判定对象互不代答：实现段不得由代码段代答，代码段不得由实现段代答；两段各自成文、各自定级、互不转换。该段的方法论载体 MUST 是能以运行时路径抵达的具名 owner（见 A12），模板 MUST NOT 内联方法论。
- **FR-015**: `/speckit.review` MUST 新增 **Acceptance Reality Check**：统计 [[STR-003]] 路径 SC 的 `pass` / `blocked` / `deferred` 计数并与特性声明的状态比较；当特性声明 `Implemented` 或 `Ready for Review` 而该 `pass` 计数为 0 时，MUST 产出 P0 [[STR-016]] 并拒绝该转移；三个计数 MUST 写入 `review.md`（可核验载体）。
- **FR-016**: `Implemented → Ready for Review` 门 MUST 增加第四个合取条件：不存在处于 `blocked` / `deferred` / `fail` 的 [[STR-003]] 路径 SC，除非有显式用户豁免。判据 owner 仍是 `templates/feature-details-template.md` § Canonical Status State Machine；`/speckit.review`、`/speckit.checklist` 与 `.specify/shared/workflow/feature-integration.md` § Pre-Status-Flip Gate MUST 只引用该 owner，不复制条款。
- **FR-017**: `sdd-loop-driver` 的 closure/merge 步 MUST 运行 [[STR-005]]；得到 [[STR-007]] 时 MUST 拒绝合并、把该线标记为 [[STR-002]] 并记录命名原因，该线 MUST NOT 成为 `completed`。线状态封闭集的扩张（[[STR-002]] 加入 `line-registry.py`）MUST 同时处置由此受影响的既有约束（`merge_ready`、`ACTIVE_STATES`、`HOLDING_STATES`、终态守卫集 `{closed, stale, orphaned}`、`promote-waiting`、各 `integration-*` 动作、`deregister --reason stale-cleanup` 写入的 `stale_from_state`），MUST NOT 留下与新值矛盾的旧约束；逐项处置内容以 A6 的八项为准（该文件中不存在 `revival` 符号，恢复路径名为 `promote-waiting`／`ownership-check`）。

#### D. 词表、注册表、迁移、文档与镜像同步（US4）

- **FR-018**: [[STR-001]] MUST 写入三处词表 owner：`templates/feature-index-template.md`、`templates/feature-details-template.md` § Canonical Status State Machine、`skills/internal/manage-features/SKILL.md` 的状态词表。never-regress-status 规则 MUST 增加一条**窄**例外：`Implemented → Blocked` 仅在审计纠正且引用证据时允许；其余回退仍非法。
- **FR-019**: 既有 `blocked` / `not-required` 的用法 MUST 与新词表对齐：词表 owner 之外的每一处 [[STR-002]] 出现点 MUST 被逐条归入「新词表用法」或「与本词表无关的既有封闭集」（如线状态集、任务行的 `[blockedBy: …]`），MUST NOT 让同名字面表达第三种含义；调和结论 MUST 只落一处（本特性 owner 文档），MUST NOT 在多处各自表述。
- **FR-020**: [[STR-005]] MUST 提供只读 [[STR-015]] 模式：报告现有 `Implemented` 特性中按新规则会变成 [[STR-001]] 的清单与原因。该模式 MUST 零写入（无文件创建或修改，`git status --porcelain` 增量恒空）、MUST NOT 改任何历史状态；其退出码 MUST 只反映输入有效性（0 = 审计完成，2 = 输入缺失或不可解析），MUST NOT 因发现而改为阻断语义。
- **FR-021**: `templates/commands/implement.md`、`templates/commands/review.md`、`templates/commands/tasks.md` MUST 按需更新以接入新门；逐工具副本 MUST 由 `python3 scripts/python/regen-command-copies.py` 重生成且 `--check` exit 0；镜像 MUST 由仓库的 mirror 引擎（`scripts/python/sync-mirrors.py`）同步且 `--check` exit 0。MUST NOT 以手改 `.specify/skills`、`.specify/shared`、`.specify/scripts` 镜像副本作为主改动。
- **FR-022**: 新 schema（`Path` 标注、封闭原因集、两张新表的列与取值域）的 owner MUST 是单一文件 [[STR-017]]，其镜像由 mirror 引擎生成；`CHANGELOG.md` MUST 记录本特性；既有 owner（`templates/feature-details-template.md`、`templates/verification-log-template.md`、`.specify/shared/workflow/feature-integration.md`、`templates/tasks-template.md` 的 GATE-4、`skills/internal/implement-feature/SKILL.md`、`skills/internal/review-sdd-process/SKILL.md`、`skills/external/sdd-loop-driver/`）MUST 以「路径 + 章节锚」指回该 owner，MUST NOT 复制同一张表或同一份阈值。
- **FR-023**: MUST 提供 pytest 单元／契约测试覆盖 closure checker、四处门禁与审计模式；实现前 MUST 把失败用例 id 集合采集到 `<spec-dir>/baseline-failed.txt` 作为基线参照物，并在同一次采集里把 `pytest --version` 与 `git --version` 的原文一并落到 `test-evidence/`（这就是运行时栈 RS-002／RS-003 行的 pin——本仓此前没有任何版本声明，pin 只能由首次运行记录，MUST NOT 凭空写一个版本号）；实现后 `head 失败集 − 基线失败集` MUST 为空（0 个新增失败）；本特性的 smoke 命令（见 FR-005）MUST 通过，且同一命令连跑两次退出码一致。
- **FR-024**: 改动 MUST 落在框架源（`templates/`、`shared/`、`skills/`、`scripts/`）；`.specify/` 下的同名文件是生成镜像，任一镜像与源出现差异时 MUST 判为缺陷，修复方式是重生成而不是手改镜像（由 FR-021 的两个 `--check` 证明）。
- **FR-025**: 新增的脚本／测试／夹具路径 MUST 被登记并在目录治理文档中就位；每个新门禁 MUST 有一个确定性脚本给出的判定，MUST NOT 存在「只能由模型判断」的新门禁；临时产物 MUST 落 `.specify/.tmp/`。

### Key Entities *(include if requirement involves data)*

- **Feature Status Value**：特性生命周期状态，取值集与转移表归 `templates/feature-details-template.md` § Canonical Status State Machine；本特性新增 `Blocked` 与它的四条转移。
- **Path-annotated Success Criterion**：一条带 `Path` 属性（`final` / `supporting`）的 SC 定义行；属性决定它在验收门里的权重——`final` 必须 `pass`，`supporting` 允许 `deferred`。
- **Verification Status Row**：`verification.md` 中每条 SC 的一行记录；本特性新增 `blocked` 值与五个测量阶梯字段。
- **Closure Verdict**：closure checker 的输出，二值 `accept` / `block` 加一个来自封闭原因集的命名原因；是 `/speckit.implement`、`/speckit.review`、driver closure/merge 三处共享的唯一判定来源。
- **Runtime Stack Row**：一行 `ID | Capability | Form | Owner | Pin | Joint acceptance | FR`，声明该特性依赖的一项运行时能力归谁、如何联合验收。
- **Execution Premise**：一行 `ID | Premise | Evidence | Status | Decision`，声明 plan 依赖的一条执行前提及其是否已被证据支持。
- **Inherited Blocker**：依赖特性详情中的一条 `## Deferred`／blocked 记录，加上本特性对它的处置（`resolved` / `inherited` / `not-applicable`）。
- **Smoke Test Record**：一条覆盖主流程的最小命令，加命令原文、退出码、证据路径三件。
- **Review Finding**：四段之一产出的一条带严重度、产物路径与行号定位的结论；`F-ACCEPTANCE` 是 Acceptance Reality Check 的固定 P0 项。

### Runtime Stack & Dependency Ownership（081 自身的运行时栈表）

本特性**交付**的运行时能力只有一条（RS-004：`specify init` 在 `src/` 内实现）。其余三条是由外部供给、本仓只消费的能力——按 FR-009 的判据它们 MUST 记 `signed-contract` 并给出契约路径、pin 与具名联合验收，MUST NOT 记 `in-scope`（记 `in-scope` 会把「外部化」洗成一个 Form 值）。026 的失守形态不是「有没有外部依赖」，而是「外部依赖只写成散文、无表行、无 pin、无联合验收」：本表四行都必须可机械判，零散文行。

| ID | Capability | Form | Owner | Pin | Joint acceptance | FR |
|----|------------|------|-------|-----|------------------|-----|
| RS-001 | Python 3 解释器（跑 closure checker、validator、审计模式） | signed-contract | CPython 上游（本仓只消费）；契约路径 `pyproject.toml` § `[project] requires-python` + `scripts/bash/run-tests.sh` § `resolve_python` | `requires-python >= "3.8"`（已在 `pyproject.toml` 声明，不新增 pin）；新增脚本 stdlib-only——无第三方 import，机械可判 | 本特性全部新脚本在 `>=3.8` 解释器上通过 FR-007 的正／负夹具测试与 FR-005 的 smoke，且静态 import 清单为空 | FR-006, FR-007, FR-020 |
| RS-002 | pytest（契约／单元测试运行器） | signed-contract | pytest 上游（本仓只消费）；契约路径 `scripts/bash/run-tests.sh`（解释器与 pytest 解析的唯一入口） | 本仓当前**无** pytest 版本声明（`pyproject.toml` 只有 `[tool.pytest.ini_options]`，无 pin）；pin 由 FR-023 在采集基线同一次记录的 `pytest --version` 原文提供，落 `test-evidence/` | 基线重跑在同一 pin 上复现失败集（`head 失败集 − 基线失败集` 为空），且新增测试全绿 | FR-023 |
| RS-003 | `git`（实现审查的 `base..head` delta 解析；两个 `--check` 的树差异判定；审计的 `git status --porcelain`） | signed-contract | git 上游（本仓只消费）；契约路径 `scripts/bash/common.sh` § `check_dependency`（只检存在、不检版本） | 本仓无版本声明；pin 由 FR-023 同一次采集记录的 `git --version` 原文提供，落 `test-evidence/` | 实跑一次 `base..head` 解析（实现段据此成文）+ `regen-command-copies.py --check` 与 `sync-mirrors.py --check` 均 exit 0 + 审计前后 `git status --porcelain` 增量为空 | FR-014, FR-020, FR-021 |
| RS-004 | 本仓自己的 `specify init`（smoke 命令在临时夹具上执行它） | in-scope | 本仓 `src/` 与 `scripts/` | 仓内 commit（同一次提交） | smoke 命令在临时目录执行 `specify init` 后退出码为 0 且夹具被生成 | FR-005 |

### Decomposition & Ceiling

本规格 FR 25 条、SC 9 条，均在分解上限（FR ≤ 30）之内，**不需要**切片为 081a–081d。US1–US4 四组本身就是 plan 阶段可用的天然切片边界：若 plan 判定单次实现过重，可按该四组切成 081a（US1）、081b（US2）、081c（US3）、081d（US4），且 MUST NOT 因此删除任何一条 FR。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 026 形态被三处门拒绝——负夹具（任务全关、每条 SC 有状态行、[[STR-003]] 路径 SC 全 `blocked`/`deferred`）分别触发 `/speckit.implement`、`/speckit.review`、driver closure/merge，三处全部输出 [[STR-007]]（3/3 拒绝，0 处放行）；每次拒绝的命名原因逐字命中封闭集其一（[[STR-008]] / [[STR-009]] / [[STR-014]] 之一，3/3），不得为自由文本。**Path**: final
- **SC-002**: 正路径不误杀且 smoke 是硬条件——正夹具（[[STR-003]] 路径 SC 全 `pass` + smoke 记录齐备）走完 `Planned → Implemented → Ready for Review` 全程 [[STR-006]]，误拒 0（2/2）；同一夹具删掉 smoke 记录后状态 MUST 为 [[STR-001]] 而非 `Implemented`（1/1）。**Path**: final
- **SC-003**: 词表与状态机对齐——[[STR-001]] 在三处 owner 各出现且语义一致（3/3）；`templates/feature-details-template.md` 的转移表含四条新增行（`Planned→Blocked`、`Blocked→Implemented`、`Blocked→Ready for Review` 非法、`Implemented→Blocked` 审计例外，4/4）；never-regress-status 的窄例外存在（1/1）。**Path**: supporting
- **SC-004**: 验证词表与测量阶梯可判——词表 owner 含 [[STR-002]]（1/1）；`blocked`/`deferred`/`partial` 行缺任一必填字段、或存在可用 reduced measurement 而 `reduced_measurement_run=no` 时均被判非法（夹具 3/3），其中「有可用测量却未跑」一项 MUST 命中 [[STR-010]]。**Path**: supporting
- **SC-005**: 所有权与前提是结构化一等产物——本 requirements 的运行时栈表行数 ≥1 且每行 `Form` 合法（分母 = 实测行数，L/L）；plan 的 Execution Premises 与 Inherited Blockers 表存在，依赖特性 deferred 行处置率 100%（100%）；四类确定性缺陷各被指名抓到（4/4）。**Path**: supporting
- **SC-006**: review 四段与 Acceptance Reality Check 齐备且可定位——一次 review 的 `review.md` 同时含产物审查段（覆盖当次实际存在的每个阶段产物，覆盖率 = 实测分母）、实现审查段（含 smoke 命令原文、退出码、证据路径，3/3）与 Acceptance Reality Check 的 final-path 三计数（`pass`/`blocked`/`deferred` 齐备，3/3）；每条 finding 带严重度与「产物路径 + 行号」（抽样 L/L）；负夹具下产出 P0 [[STR-016]] 并拒绝转移（1/1）。实现期可确定性测量的部分是**结构与 schema**：组合声明存在且段数与固定顺序与 A3 一致、finding 定位字段可解析、三计数行齐备、负夹具下 [[STR-016]] 与拒绝转移；「一次真实 review 的 `review.md`」只能在 review 阶段采证。**Path 裁决**：这里保持 [[STR-004]]（clarify 的显式裁决）——若把它记为 [[STR-003]]，081 自身的 `Planned → Implemented` 将要求 SC-006 为 `pass`，而 SC-006 只能在 review 阶段测量，同时 `Blocked → Ready for Review` 非法（FR-003），于是形成无解的循环门禁；review 处的**门禁强制力**已由 SC-001 的第三个调用点（[[STR-003]] 路径）覆盖，因此保持 [[STR-004]] 不失去约束。**Path**: supporting
- **SC-007**: 审计只读且可判——[[STR-015]] 在既有仓库上运行时文件系统零写入（`git status --porcelain` 增量行数 = 0）、历史特性状态零变更（0 变更），输出清单每行带原因列（L/L）。**Path**: supporting
- **SC-008**: smoke 记录存在且可复现——081 的 `tasks.md`／`verification.md` 给出恰好一条 smoke 记录（命令原文、退出码、证据路径，3/3），同一命令连跑两次退出码相同（2/2），且该命令覆盖 FR-005 要求的三件事（3/3）。**Path**: supporting
- **SC-009**: 框架卫生，含一条可判定的包含性声明——① `python3 scripts/python/regen-command-copies.py --check` 与 `python3 scripts/python/sync-mirrors.py --check` 均 exit 0（2/2）；② 测试基线包含性成立，五要件齐备：**基线参照物** = 本特性实现起始提交上由 `bash scripts/bash/run-tests.sh` 采集的失败用例 id 集合（存于 `<spec-dir>/baseline-failed.txt`）；**比较单元** = 失败用例 id 集合（按 id 比对，不按字节，也不用「全仓测试」这类未定义聚合词）；**允许差异集来源** = 空集（新失败一条都不允许，机械可得）；**补集与不变量** = `head 失败集 − 基线失败集` MUST 为空（0 个新增失败），而 `基线失败集 − head 失败集` MUST 逐条列为已修复项（MUST NOT 静默丢弃）；③ `CHANGELOG.md` 含本特性条目（1/1）；④ schema 唯一性：由 Shared Strings 表与 owner 文档章节目录**机械导出**的列名与取值域字面量，在 `templates/` 与 `shared/` 两类路径下的出现点，除 owner 文档外 MUST 为 0，且守卫测试把真实命中枚举出来并断言等于豁免清单（0 个未豁免命中）。**Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 负夹具目录（`tests/fixtures/` 下的声明式最小文件集）加三处调用点的实际运行日志与退出码；原因标签用封闭集逐字匹配，不用模型判读。
- **SC-002 Source**: 正夹具加两次状态机运行日志；删除 smoke 记录前后读取状态字段。
- **SC-003 Source**: 三个 owner 文件的检索计数、转移表行计数、never-regress 段落存在性检查。
- **SC-004 Source**: 词表 owner 的取值列表，加三份非法行夹具喂给 checker 后的退出码与原因串。
- **SC-005 Source**: 本文件 § Runtime Stack & Dependency Ownership 与 `plan.md` 两张表；四类缺陷夹具喂给 `pre-analyze-check.py`（或同层 checker）的输出。
- **SC-006 Source**: 一次真实 review 的 `review.md` 分段解析（段存在性、三计数行、finding 定位字段），加负夹具的运行结论。
- **SC-007 Source**: 审计模式运行前后的 `git status --porcelain` 与 `features.md`／`features/*.md` 状态字段快照。
- **SC-008 Source**: `tasks.md`／`verification.md` 中的 smoke 记录行；同一命令两次运行的退出码。
- **SC-009 Source**: 两个 `--check` 的退出码；`<spec-dir>/baseline-failed.txt` 与 head 失败集的两集合差（采集命令与基线相同，id 级比对）；`CHANGELOG.md` 检索；由 Shared Strings 表与 owner 章节导出的字面量清单 × `templates/` 与 `shared/` 的出现点枚举（守卫测试输出）。

## Constraints（落地约束，判据在外部 owner）

- **Two Hats**：本特性改的是框架源（`templates/`、`shared/`、`skills/`、`scripts/`）；`.specify/` 同名文件是生成镜像。机制与拓扑归 `.specify/shared/definitions/dogfooding-definitions.md` § 2.1，此处不复述（承载 FR-024）。
- **One Source of Truth**：判据归 `.specify/shared/guidelines/one-source-of-truth.md`；本特性新 schema 的单一 owner 是 FR-022 指定的文档（承载 FR-019、FR-022）。
- **Program-First**：判据归 `.specify/shared/guidelines/token-efficiency.md`；本特性所有新门禁都是确定性脚本判定（承载 FR-025）。
- **Fast Fail**：判据归 `.specify/shared/guidelines/fast-fail.md`；本特性不新增中间严重度层，`accept` / `block` 是二值（承载 FR-006）。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `Blocked` | FR-003, FR-005, FR-018, SC-003 |
| `STR-002` | `blocked` | FR-004, FR-017, FR-019, SC-004 |
| `STR-003` | `final` | FR-001, FR-002, FR-003, SC-001 |
| `STR-004` | `supporting` | FR-001 |
| `STR-005` | `scripts/python/closure-acceptance-check.py` | FR-006, FR-007, FR-008, FR-017, FR-020 |
| `STR-006` | `accept` | FR-006, SC-002 |
| `STR-007` | `block` | FR-006, FR-008, FR-017, SC-001 |
| `STR-008` | `zero-final-path-pass` | FR-006, SC-001 |
| `STR-009` | `final-path-not-pass:` | FR-006, SC-001 |
| `STR-010` | `blocked-without-measurement-ladder:` | FR-006, SC-004 |
| `STR-011` | `runtime-dependency-not-owned:` | FR-006, FR-009 |
| `STR-012` | `falsified-premise-undecided:` | FR-006, FR-010 |
| `STR-013` | `inherited-blocker-undisposed:` | FR-006, FR-011 |
| `STR-014` | `status-claims-implemented-but-blocked` | FR-006, SC-001 |
| `STR-015` | `--audit-existing` | FR-020, SC-007 |
| `STR-016` | `F-ACCEPTANCE` | FR-015, SC-006 |
| `STR-017` | `shared/workflow/acceptance-hardening.md` | FR-022 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

本次运行未提出 clarification marker（见 A9）：所有开放点均在目标仓库内可裁决，裁决记在 `## Assumptions`。`/speckit.clarify` 若仍需提问，答案按 `<question>` → `<answer>` 追加为 `### Session <date>` 小节。

### Session 2026-11-03

本轮为无人值守运行，**零提问**：答案空间由仓内证据闭合，每条裁决的证据写在 `## Assumptions` 对应条目内。下列五行是本轮改变产物的五个决定（不含只在 Assumptions 内落地的 A11）。

- Q: 本规格绑到既有 Feature 还是新建？→ A: 新建 **Feature 081**。复核 026／055／062／071／077／079 均不覆盖「final 路径阈值 + smoke 硬条件 + 三处共享判定 + 产物／实现审查」的组合（依据 `.specify/shared/workflow/feature-integration.md` § Feature Binding Rules 的 bind/create 判据与 binding-precedent 启发式）。**ID 取值 081** 而非「下一个空号 080」：本仓 spec key 与 Feature ID 是两套编号（spec 080 绑的是 Feature 062），取与 spec key 对齐的 081 是 Grounded Naming 下「用户指令 > 项目惯例」的直接结果；080 留空与既有 054／066／067／075 留空同形。已落 `.specify/memory/features/081.md` 与 `.specify/memory/features.md` 行（`Total Features` 同趟重算）。
- Q: `/speckit.review` 的终态组合是什么？→ A: **四段 + 一次确定性判定、固定顺序** = 过程段 `review-sdd-process` → 产物段（新增）→ 实现段（新增）→ 代码段 `code-review` → Acceptance Reality Check（确定性判定，不委派技能）。理由、顺序与边界见 A3。用户需求里的「三件事」指新增的三项职责（产物审查、实现审查、ARC），但 `code-review` 按 FR-014 不得被替换，故终态不是三段。`templates/commands/review.md` § Composition 的 owner 文本改写**不在本阶段落地**（Two Hats），已写成 FR-013 的 plan／implement 义务。
- Q: `Path` 怎么标、final 集合是哪几条？→ A: 标注写 SC 定义行行尾、形如 `**Path**: final`，每行恰好一次（A4 的解析器容差证据）；final 集合 = **SC-001、SC-002**，其余七条 `supporting`。SC-006 明确**不**升级为 final：把它记为 final 会让 081 自己的 implement 门禁依赖一个只能在 review 阶段产生的测量，与 `Blocked → Ready for Review` 非法叠加后自锁（见该 SC 的 Path 裁决与 Edge Cases）。review 处的门禁强制力由 SC-001 的第三个调用点承担，不需要靠染指 `Path` 来补。
- Q: 运行时栈表每行真的都是 `in-scope` 吗？→ A: 不是。**RS-001（CPython）／RS-002（pytest）／RS-003（git）= `signed-contract`**（本仓只消费，不交付），**RS-004（`specify init`）= `in-scope`**（本仓交付）。三条外部行各带契约路径与联合验收；由于本仓此前没有 pytest／git 的版本声明，pin 由 FR-023 在采集基线时记录的 `--version` 原文提供，MUST NOT 凭空写版本号。判据补进 FR-009：`in-scope` 意味着「本特性交付该能力」。
- Q: `blocked` 进入线状态集后，既有约束怎么处置？→ A: 八项逐条处置写进 A6（`STATE_VALUES` 扩容、`ACTIVE_STATES` 与 `HOLDING_STATES` 不变并声明不持有资源、`merge_ready` 加互斥不变量、`integration-*` 结构性不可达、终态守卫集**不**纳入 `blocked`、`promote-waiting` 不得直通、`stale_from_state` 可承载新值、不新增线级 never-regress 规则）；同时更正原假设的用词——该文件里没有 `revival` 符号，恢复路径叫 `promote-waiting`／`ownership-check`。FR-017 的清单按此改写，MUST NOT 留下与新值矛盾的旧约束。

