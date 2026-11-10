# Requirements Specification: /speckit.seal — 按 review 结论封装 spec 与分片合并回写（Split Merge-Back & Seal）

**Requirement Branch**: `099-speckit-seal`
**Created**: 2026-11-10
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（编写/修订 `templates/commands/**`、`skills/internal/**`、`shared/workflow/**`、`shared/definitions/**`、`scripts/python/**`、`agents/` 与状态面消费方）与下游项目中运行 `/speckit.*` 流程并需要判定「一条 spec 何时算最终封装、分片如何并回父级、什么状态才可归档」的维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「`Sealed` 是什么、由谁、在什么条件下写入」「一条被拆分交付的 spec 如何把各分片的同名输出件并回父级（编号怎么排、语义怎么对齐、词汇表怎么对齐、冲突怎么呈现）」「seal 失败时状态与报告如何呈现」「归档与既有 `/speckit.feature` / `/speckit.review` / `/speckit.sanitize` / `/speckit.goal` 的边界在哪」时打开本规格，据 FR-001…FR-028 与 SC-001…SC-009 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "新增 `/speckit.seal` 命令：按 review 的结论对 spec 进行封装；sealed 是 Ready for Review 之后的最终态；sealed 的 spec 方可最终归档。承载 split + merge 回写流程：当一条 spec 被拆成多个片段（如 074a/074b）交付时，各分片同名的输出件合并回写父级（至少含 tasks.md，以及所有输出件；流程含编号重排、语义对齐、词汇表对齐）；所有输出件使用同一流程；最终确认由 `/speckit.seal` 完成。背景事实：074 的 074a(32/32)+074b(26/26) 已完成但未合并回父级，父 tasks.md 仍 57 个未勾选行——本特性须让该状态可被 seal 处置，并为 074 的回合提供可执行流程。"

## Related Feature *(mandatory)*

**Feature ID**: 099
**Feature Name**: Speckit Seal（/speckit.seal：按 review 封装 spec 与分片合并回写）

**Binding note**: 经检索 `.specify/features.md` 全表与 `features/` 详情，无既有 Feature 覆盖「检查点封装 / 分片合并回写」；按 `shared/workflow/feature-integration.md` § Feature Binding Rules 新建 Feature 099（先例：090–094 各自 1:1 绑定自身编号）。注册表行与 `features/099-*.md` 详情文件的创建属该规则的 clarify 检点义务；本阶段写面仅 `requirements.md`，该项记录为待办（见 `## Clarifications` 本日 clarify 条目）。

## Overview

框架当前的特性状态机在 `Ready for Review` 之后只有一条通往 `Completed` 的「人工/治理终验」出口：没有任何**机器可判定**的动作把「review 已完成、分片已并回、验收记录齐备」这一状态固定下来，也没有任何门把「最终归档」与「尚未封装」区分开。更具体的缺口来自**拆分交付**：当一条 spec 因规模超限被拆成多个分片（本仓已有 069a/069b 与 074a/074b 两例），每个分片各自走完 requirements → plan → tasks → checklist → analyze → implement → review，但**分片产物从未并回父级**——074 的实测状态是：074a 32/32 与 074b 26/26 全部闭合、两片各有 `review.md` 与 `code-review.md`，而父 `074-goal-team-sdd-unification/` 仍保留 57 个 `[ ]` 任务行、没有父级 `review.md`/`code-review.md`，注册表状态停在 `Ready for Review`。这个状态既不能被判为完成，也不能被干净地归档：它就是本特性要消除的「封装缺失」。

本特性新增 **`/speckit.seal`**：按 review 的结论对 spec 做**最终封装**。`Sealed`（[[STR-001]]）是 `Ready for Review` 之后的**终态**，只有 `Sealed` 的 spec 方可进入最终归档。该命令同时承载 **split + merge 回写流程**：当被测 spec 存在分片时，把各分片**同名的输出件**确定性合并回父级——包含**编号重排**（FR/SC/STR/契约条款/任务行等 ID 家族）、**语义对齐**（分片条目 ↔ 父条目映射的完备性与唯一性）、**词汇表对齐**（共享字符串与项目词汇的单一解析），冲突**必须显式呈现，不得静默择一**；所有输出件走同一条流程；最终确认由 `/speckit.seal` 完成。

**零新增重复机制**是本特性的硬边界：状态机归既有的 status 面（owner `shared/workflow/acceptance-hardening.md` § Feature Status，carrier `templates/feature-details-template.md` § Canonical Status State Machine 与 `shared/workflow/feature-integration.md` § Status State Machine），归档归 `/speckit.sanitize`（归档 lane）与 docs 既有 lane，`/speckit.goal` 的 `migrate-archive` 保持其 goal/team 树迁移职责；本特性只新增 **seal 与 merge-back 的执行面**——一个命令、一个确定性引擎、一份按 spec 的封装记录。

本特性不新增第二个调度器、不新增第二份特性注册表、不改变 SDD 阶段链与哨兵、不自动修复 review 的 P0、不自动归档（归档动作仍由既有 lane 执行，seal 只定义其准入状态）。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 把一条 review 完成的 spec 封装为终态 Sealed (Priority: P1)

维护者对一条已处于 `Ready for Review` 的 spec 运行 `/speckit.seal`。引擎逐条判定封装前置条件——当前 review 记录存在且结论中没有未处置的 P0、验收记录齐备（每条 SC 有状态行、每条 final 路径判据为 `pass`）、若存在分片则合并回写已完成且无未决冲突、工作树没有本流程之外的未提交改动。全部成立时写入一份按 spec 的封装记录并把状态推进为 `Sealed`（[[STR-001]]）；任一不成立时**拒绝封装**，状态保持不变，并逐条点名未满足的条件与修复路径。

**Why this priority**: 这是用户诉求的第一句——「按 review 的结论对 spec 进行封装」。没有这一步，`Ready for Review` 之后没有可判定的终态，归档也就没有准入判据。

**Independent Test**: 对一个 review 干净、验收齐备的单体 spec 运行 seal——断言状态变为 `Sealed`、封装记录存在且与注册表行/详情文件一致、重复运行幂等；再对每一类前置条件各造一个失败夹具——断言每种失败都以具名理由拒绝且状态不变。

**Acceptance Scenarios**:

1. **Given** 一条 `Ready for Review` 的 spec，其 review 结论无未处置 P0、验收行齐备、无分片或分片已合并，**When** 运行 `/speckit.seal`，**Then** 状态推进为 `Sealed`（[[STR-001]]），父 spec 目录出现一份封装记录（[[STR-002]]），注册表行与特性详情同步，且记录钉住本次判定的提交。
2. **Given** 同一条 spec 已 `Sealed`，**When** 再次运行 seal，**Then** 幂等成功并具名报告 `already-sealed`，不产生第二份封装记录、不重复写状态面。
3. **Given** 一条 `Ready for Review` 的 spec，其 review 结论中有一条未被修复、也未被**用户显式裁定**豁免的 P0，**When** 运行 seal，**Then** 拒绝封装：状态保持 `Ready for Review`，报告逐条点名该 P0 及其位置与修复/裁定路径；驱动者或代理的「确认」不计为用户豁免。
4. **Given** 一条非 `Ready for Review` 的 spec（`Draft` / `Planned` / `Implemented` / `Blocked`），**When** 运行 seal，**Then** 以具名理由拒绝，不做任何状态写入。
5. **Given** 一条已被拆分的父 spec，**When** 直接对某个**分片目录**运行 seal，**Then** 以具名理由拒绝（分片不是封装主体），并点名其父 spec 为正确目标。

---

### User Story 2 - 把分片交付的同名输出件确定性合并回父级 (Priority: P1)

维护者对一条带分片的父 spec 运行 seal 的合并回写流程。引擎按**声明顺序**逐分片、逐同名输出件合并：编号按声明映射重排（分片本地 ID → 父 ID；分片独有 ID 按合并顺序追加到父序列），所有引用改写为合并后的 ID，共享字符串与术语对齐到合并后的父级词汇表，语义映射逐条核验完备且唯一；分片测量记录保持原样（dated-record 红线），父级承载合并视图与指针。任何无法确定性归并的差异（同号不同义、同义不同号、无映射条目、同一锚点的双端编辑）都进入**冲突清单**并以显式记录呈现；有未决冲突时 seal 拒绝封装。

**Why this priority**: 这是用户诉求的第二句。没有它，074 这类已完成的分片永远无法并回父级，`Ready for Review` 的父 spec 也永远无法封装；而「静默择一」的合并会制造比不合并更难发现的语义漂移。

**Independent Test**: 用一个含两片分片（各自有 tasks/requirements/contracts 与映射表）的夹具树运行合并两次——断言两次产物逐字节一致、重跑零 diff；再注入「同号不同义」与「无映射条目」两类冲突——断言合并以冲突清单拒绝封装、且没有任何一侧内容被静默丢弃。

**Acceptance Scenarios**:

1. **Given** 父 spec 与两个已闭合分片（分片 requirements.md 声明父映射），**When** 运行合并回写，**Then** 每个同名输出件都产出一条合并记录（来源分片、动作、ID 重映射、检查结果），父级成为唯一现行权威，分片目录被标注 `merged into <父 spec>` 且内容不被改写或删除。
2. **Given** 同一组输入运行两次，**When** 比较两次合并产物与合并清单，**Then** 逐字节一致；成功后的 `apply` 重跑产生零 diff、零重复行、零重复 ID。
3. **Given** 分片 A 的本地 STR 编号与分片 B / 父级同号但字面量不同，**When** 合并，**Then** 该同号不同义进入冲突清单（两侧字面量与位置并列呈现），封装备受阻断，MUST NOT 静默重编号或择一保留。
4. **Given** 分片某条目在父级没有映射目标，**When** 合并，**Then** 该条目进入冲突清单并点名分片与行号；MUST NOT 由引擎自行发明映射。
5. **Given** 父级既有 `verification.md` 采用「聚合指针集」形态（每条 SC 指向分片测量记录），**When** 合并，**Then** 合并视图保持指针形态并补齐缺失行，分片 `verification.md` 作为测量承载者不被改写。

---

### User Story 3 - 为 074 的回合提供可执行流程并留下可复现裁决 (Priority: P1)

维护者按本特性交付的流程对 074 运行合并回写与 seal。流程必须能识别 074a/074b、把它们全部同名输出件并回父级、让父 `tasks.md` 不再携带未勾选行（57 行被拆前记录按既有 non-disposable 纪律被复核与处置，而不是被静默覆盖）、让父级验收记录可被闭包判定器求值（每条 SC 有状态行且 requirements 满足 Path 标记模式）、并产出父级合并后的 review 结论。最终 seal 给出**完整裁决**：要么 `Sealed`，要么一份逐条点名的拒绝清单——每个已知输入缺陷（缺 Path 标记导致闭包判定器 exit 2、共享字符串同号不同义、出厂文档引用分片本地 ID、review P0 只有驱动者记录的豁免、父 tasks.md 的拆前行）都必须被显式解决或显式阻断，MUST NOT 有静默默认。

**Why this priority**: 这是用户对「背景事实」的直接要求——「本特性须让该状态可被 seal 处置，并为 074 的回合提供可执行流程」。没有真实回合，前两条可以停在夹具上；074 回合是本特性的第一次真实验收。

**Independent Test**: 在 074 的当前树上运行完整回合，断言：合并清单覆盖两片的全部输出件；父 `tasks.md` 未勾选行为 0；父 `verification.md` 每条 SC 有状态行；父级 review 记录由两片合并而来且保留 P0 处置引用；seal 裁决要么 `Sealed` 要么列出与实测输入缺陷一一对应的具名阻断项；重复运行幂等。

**Acceptance Scenarios**:

1. **Given** 074 的实测状态（074a 32/32、074b 26/26、父 `tasks.md` 57 个 `[ ]` 行、父级无 `review.md`/`code-review.md`、两片各有 review 记录），**When** 运行完整回合，**Then** 产出合并清单 + 父级封装修正视图，且父 `tasks.md` 的未勾选行数为 0（拆前行作为带日期的拆前记录被显式处置）。
2. **Given** 父/分片 requirements 的 SC 行缺少 `**Path**` 标记（闭包判定器实测 exit 2），**When** 回合运行，**Then** 每一项缺标记必须有显式记录的决定（明确取值或记录过的严格默认为 `final`），MUST NOT 把 exit 2 读作通过。
3. **Given** 074b 本地 STR 编号与父级同号不同义、且出厂文档 `skills/internal/create-team/SKILL.md` 以分片本地 ID 引用 outcome 字面量，**When** 回合做词汇表对齐，**Then** 两类问题都作为冲突项呈现并逐条记录解决（重指向合并后 ID / 改用逐字字面量 / 用户豁免），MUST NOT 静默保留错误解析。
4. **Given** 074b review 的 P0（字母分片分支解析到父目录）只带驱动者记录的豁免，**When** seal 判定 P0 前置条件，**Then** 该 P0 不被视为用户豁免——状态保持 `Ready for Review` 并以具名理由阻断，除非同回合内有修复证据或用户显式裁定。
5. **Given** 回合在任一阻断状态下结束，**When** 再次运行，**Then** 已完成且无变化的合并步骤零 diff，阻断清单与上次一致（可复现），不做部分封装。

---

### User Story 4 - 边界清晰且零新增重复机制 (Priority: P2)

框架维护者核查 seal 的落点：状态值域与转移只在既有 schema owner 上扩展一次，所有消费方同步；归档动作仍归 `/speckit.sanitize` 的归档 lane 与 docs 既有 lane，seal 只提供准入判据；`/speckit.feature` 仍拥有注册表 reconcile，`/speckit.review` 仍拥有 review 记录，`/speckit.goal` 的 `migrate-archive` 仍拥有 goal/team 树迁移；seal 不新增注册表、不新增调度器、不移动/删除 spec 目录。

**Why this priority**: 复用与边界是本框架的既有硬约束（宪法 IX/XIV、Dogfooding 两顶帽子）；seal 若自带第二套状态机或归档动作，会在下一次流程演进里静默分叉。放在 P2 是因为它约束前三条的实现形态，而不是新增用户可见能力。

**Independent Test**: 静态检查 + 契约测试——状态值域只有一个 owner、每个消费方都识得 `Sealed`；seal 引擎不包含目录移动/删除动作；归档入口在非 `Sealed` 时拒绝；两个并发写者写入不同 spec 的 seal 记录时路径互不相同。

**Acceptance Scenarios**:

1. **Given** 状态值域的唯一 owner 与全部消费方，**When** 从任一处移除 `Sealed`，**Then** 漂移守卫契约测试转红并点名该处。
2. **Given** 一条非 `Sealed` 的 spec，**When** 任一归档/退休入口尝试处置它，**Then** 以具名理由拒绝并指向 `/speckit.seal`；`Sealed` 通过同一门。
3. **Given** seal 引擎的动作表，**When** 静态审计，**Then** 不含归档移动、删除、push 或调度循环；对 review 记录与分片测量记录只读。
4. **Given** 两条并行线在同一时刻各自封装不同 spec，**When** 写入封装记录，**Then** 两者落在各自 spec 目录的不同文件，无共享可变聚合文件。

---

### Edge Cases

- **无分片的单体 spec**：合并回写为 `not-applicable` 并在记录中显式写明，MUST NOT 被读成「未执行」或伪造成一次空合并。
- **分片目录只命中一半条件**（名字形如 `<父号><字母>-<slug>` 但 requirements 未声明父，或声明了父但目录名不合形）：不进入分片集合，作为冲突项呈现；分片集合 MUST 由「名字族 + 声明映射」两个条件同时成立确定，并在合并清单中列出所用集合。
- **父级已 `Sealed` 后又发现新分片**：不重新封装；走唯一的审计更正路径（`Sealed → Ready for Review`，须携带使封装结论不成立的证据），重新合并后再封装。
- **分片状态不一**（一片已闭合、另一片仍有未勾选行或未决冲突）：合并不得替分片「补完」；未闭合行保持未闭合，seal 以验收/合并前置条件阻断并点名分片与行。
- **同一 ID 家族内重号**（两片的本地任务行编号都从 T001 起）：按合并顺序确定性重编号，原文行文本保留，来源写入合并清单；MUST NOT 用返回时刻或文件名排序以外的随机因素破平。
- **同一锚点的双端编辑**（父级与分片都改过同一段落且无法由声明映射归并）：进入冲突清单，两侧文本并列；MUST NOT 以「较新者胜出」或「较全者胜出」静默择一。
- **dated-record 边界**：分片 `review.md` / `code-review.md` / `verification.md` / `test-evidence/` 与既有日期化记录 MUST NOT 被合并改写；父级合并视图只能引用它们。
- **闭包判定器 exit 2**（输入缺陷：缺 `Path` 标记等）：按输入缺陷处置（修复并重跑或具名阻断），MUST NOT 读作 `accept`，也 MUST NOT 被吞成通过。
- **封装记录与工作树**：父 spec 树存在本流程之外的未提交改动时拒绝封装（`dirty-spec-tree`），避免对移动中的状态盖章；本流程自身产生的改动在提交后再判定。
- **状态面互相矛盾**（注册表行与特性详情状态不一致，或任一载体缺失）：seal 以 `state-drift` 拒绝（退出码 `2`），不择一采信；修复归既有 reconcile owner。
- **写入阶段失败**（判定全绿但落盘中途失败）：按 FR-009 的原子性恢复已写文件并以退出码 `2` 结束；MUST NOT 留下可被读作半封装的状态。
- **并发封装**：两个 seal 同时作用于同一 spec——后到者读到先到者的封装记录时幂等返回 `already-sealed`；引擎 MUST NOT 依赖锁文件实现（以记录与提交判定为准）。
- **遗留 `Completed` 行**：既有 21 条 `Completed` 记录不追溯改写、不降级；它们不是新状态机的产出，也不自动获得归档准入（见 FR-003、FR-023）。

## Requirements *(mandatory)*

### Functional Requirements

#### A. Sealed 终态与状态机扩展

- **FR-001**: 框架的特性状态值域 MUST 恰好新增一个值 `Sealed`（[[STR-001]]），并新增恰好一条转移 `Ready for Review → Sealed`；`/speckit.seal` 是该转移的**唯一** owner 命令。值域与转移的 schema owner MUST 是既有的 `shared/workflow/acceptance-hardening.md` § Feature Status；其声明式 carrier（`templates/feature-details-template.md` § Canonical Status State Machine 与占位词汇表、`templates/feature-index-template.md` 的状态值域、`shared/workflow/feature-integration.md` § Status State Machine、`skills/internal/manage-features/SKILL.md` 的状态词表）与机器消费面（如 `scripts/python/non-disposable-check.py` 的状态—裁决对照表）MUST 在同一次变更内同步识别 [[STR-001]]；消费面集合由**静态检索**派生，MUST NOT 由手写清单维持。MUST NOT 新增第二套状态机或第二份值域。
- **FR-002**: `Sealed`（[[STR-001]]）MUST 是终态：不存在离开它的前向转移。唯一合法的后向转移 MUST 是审计更正 `Sealed → Ready for Review`，且 MUST 携带使原封装结论不成立的证据并同时落在注册表行与特性详情两处可验证载体上；其余任何后向转移 MUST 判为非法。该例外与既有 `Implemented → Blocked` 审计更正同形，MUST NOT 扩大为一般回退通道。
- **FR-003**: 既有 `Ready for Review → Completed` 出口 MUST 对新转移关闭：新工作 MUST NOT 落 `Completed`。`Completed` 仅作为**遗留记录值**保留于本特性落地之前的行（不追溯改写、不降级、不重判）；所有陈述「终态」的面向新工作的表述 MUST 说 `Sealed`。若宪法生命周期的叙述与既有 status 面在此处不一致，按 one-source-of-truth 处置：schema owner 为准，叙述面在同次变更内收敛，MUST NOT 让两个终态标签并存于新流程（先例：`Blocked` 进入 status 面时宪法叙述未被逐字展开）。
- **FR-004**: seal 的状态写入 MUST 只落在既有状态面上：注册表行 Status 与 Last Updated、特性详情 Status 与 `## Latest Review` 记录、以及按 spec 的封装记录（FR-010）。MUST NOT 新增注册表、台账、队列或状态脊；MUST NOT 移动或删除 spec 目录。

#### B. 封装前置条件与失败语义

- **FR-005**: seal 的 from 状态 MUST 是 `Ready for Review`。已 `Sealed` 的 spec 重入 MUST 幂等成功并具名报告 `already-sealed`；其它任何 from 状态（含 `Draft` / `Planned` / `Implemented` / `Blocked` / 遗留 `Completed`）MUST 以具名理由拒绝且零状态写入。**分片目录 MUST NOT 是封装主体**：分片本身不可被 seal，拒绝理由 MUST 点名其父 spec 为正确目标。状态面互相矛盾（注册表行与特性详情状态不一致，或任一载体缺失）MUST 以 `state-drift` 具名拒绝，退出码 `2`（输入/环境错误），MUST NOT 择一采信任一载体；修复仍归 `/speckit.feature` 的既有 reconcile。
- **FR-006**: 「review 结论无 P0」MUST 按当前 review 记录判定：当前 `review.md`（若存在多个，取当前记录集合，归档记录不计）的 findings 摘要 MUST 显示**零个未处置 P0**——处置只有两种：已修复（有修复指向）或**用户显式裁定豁免**（user-authored artifact 或本会话用户裁定）；驱动者/协调者/代理的确认与「无人反对」MUST NOT 计为豁免。当前 `code-review.md` MUST 零 `blocking` 条目（与既有 `Implemented → Ready for Review` 门同源，MUST NOT 另立判据）。review 记录缺失 MUST 阻断并点名 `/speckit.review`。seal MUST 只读 review 记录：不改写 finding、不重新裁决、不降级。
- **FR-007**: 「验收记录齐备」MUST 以既有闭包判定器 `scripts/python/closure-acceptance-check.py` 的裁决为单一来源：每条 SC 在父 `verification.md` 有状态行；每条 `final` 路径判据为 `pass`；smoke 记录 `pass`；父 `requirements.md` 的每条 SC 行 MUST 满足 `**Path**` 标记模式（恰一个、行尾）。exit 2 MUST 按**输入缺陷**处置（修复后重跑或具名阻断），MUST NOT 读作 `accept`；MUST NOT 由模型或第二个脚本重新推导该裁决。
- **FR-008**: 「合并回写完成」MUST 由合并清单证成（FR-018）：当分片集合非空时，每个分片 × 每个输出件都必须有一条合并记录，未决冲突数为 0，且合并后校验（FR-014…FR-016）全绿；当分片集合为空时，记录 MUST 写 `not-applicable` 并说明判定依据，MUST NOT 静默跳过。
- **FR-009**: 全部前置条件 MUST 同时成立（合取）；任一不成立 MUST 拒绝封装：状态不变、无「已封装」声明、无部分封装。拒绝报告 MUST 逐条点名**全部**未满足条件（不是只报第一条）、每条的修复路径与重跑方式；退出码封闭集 MUST 为 `0`（封装成功或幂等）/ `1`（前置条件拒绝）/ `2`（输入或环境错误），语义专属于 seal 引擎的 `--help` 契约。MUST NOT 以「三缺一」通过。判定与写入 MUST 两阶段执行：全部判定先在只读阶段算齐，只有全部成立才进入写入；写入集中的 [[STR-002]] 与状态面 MUST 同批落盘，任一写入失败 MUST 以原字节恢复已写文件并以退出码 `2` 结束。拒绝（退出码 `1`）MUST NOT 产生任何持久化写入：拒绝报告只经 stdout（及调用方捕获）呈现，MUST NOT 新建拒绝记录文件或第二份台账；重跑由同一确定性重算复现同一清单。
- **FR-010**: 封装记录 MUST 每个 spec 一份，落在父 spec 目录的固定文件名 `seal.md`（[[STR-002]]），机器可读核心至少含：判定时刻与钉住的提交、判定时的 from/to 状态、所引 review 记录路径与其 P0/P1/P2 与 `blocking` 计数、闭包判定器回执（含 exit 码与七键 final_path 记录，逐字复制不再重算）、合并清单指针与分片列表、命中的豁免引用、引擎身份与命令。记录 MUST 引用来源而不复述第二份测量。父 spec 树存在本流程之外的未提交改动时 MUST 拒绝（`dirty-spec-tree`）并指名路径。每 spec 的 [[STR-002]] MUST 只承载**当前**回执；审计更正后再次封装 MUST 原子替换该文件，并在机器可读核心写入 `supersedes: <前回执钉住的提交>`；前回执由 git 历史承载，MUST NOT 另建第二份回执文件或历史聚合。

#### C. 合并回写（split + merge-back）

- **FR-011**: 分片集合 MUST 由两个条件同时成立确定并写入合并清单：(a) 目录名形如 `<父编号><一个或多个字母>-<slug>` 且位于同一 `.specify/specs/`；(b) 该分片 `requirements.md` 显式声明父规格（父映射表或父分支声明）。只命中一个条件的目录 MUST NOT 进入集合，MUST 作为冲突项呈现。分片顺序 MUST 取父级拆分记录的声明顺序；拆分记录缺席时 MUST 取字母后缀的字典序，并记录所用依据。MUST NOT 依赖运行期目录列举顺序。
- **FR-012**: **所有输出件走同一流程**：合并 MUST 以「同名输出件」为合并单位。**候选宇宙**（封闭集）MUST 恰为：`requirements.md`、`plan.md`、`tasks.md`、`data-model.md`、`contracts/`、`research.md`、`quickstart.md`、`feature-ref.md`、`verification.md`、`review.md`、`code-review.md`、`checklists/`、`checkpoints/`、`test-evidence/` 与 `notes/`。**必选下限**：`tasks.md` 无论分片是否产出 MUST 被处置；分片集合非空时，父 `verification.md`（聚合指针视图，缺席则新建）、父 `review.md`（分片 review 记录的汇总指针视图，缺席则新建）与合并清单 MUST 产出。**其余候选按实际产出枚举**：两侧皆有 → `merge`；仅分片有 → `create`；仅父级有 → `keep` 并接受同一套对齐检查；两侧皆无 → `not-applicable`。每个输出件 MUST 记录动作（merge / create / keep / not-applicable）与来源。MUST NOT 为单个输出件发明第二套合并流程：输出件差异只体现在其**声明的 ID 家族**与结构单元上。
- **FR-013**: 合并 MUST 是确定性的：同输入产生逐字节一致的合并产物与合并清单；成功后的 `apply` 重跑 MUST 零 diff、幂等；任何决策 MUST NOT 依赖返回时刻、文件系统列举顺序、随机源或「最后写入者胜出」。不可确定性归并的差异 MUST 进入冲突清单（FR-017），MUST NOT 由启发式择一。
- **FR-014**: **编号重排** MUST 对每个在案的 ID 家族（至少 FR、SC、STR、契约条款、任务行、实体与阶段/检查点标识）给出可判定规则：分片本地 ID 有父映射的 MUST 使用父 ID；无父映射的分片独有 ID MUST 按合并顺序追加到父序列（连续、无空洞、无重复），并写入合并清单的映射表。合并产物内的一切引用 MUST 改写为合并后 ID；引用在映射后不可解析 MUST 判为冲突，MUST NOT 留下悬空引用。同一家族两次运行 MUST 得到同一映射。
- **FR-015**: **语义对齐** MUST 以分片声明的映射表为唯一依据：每个分片需求/判据条目 MUST 有且仅有一个父目标（除非分片显式声明并记录多对一的合法合并）；无映射、映射目标不存在、两个分片条目映射到同一父目标而无声明合并，三者都 MUST 判为冲突。引擎 MUST NOT 用模型转述判断「意思相同」，也 MUST NOT 发明映射。
- **FR-016**: **词汇表对齐** MUST 保证合并后每个共享字符串引用（`[[STR-NNN]]` 形态）解析到合并后的父级唯一注册表；同号不同义（同一 ID 在分片与父级指向不同字面量）MUST 判为冲突，两侧字面量并列呈现，MUST NOT 静默重编号。出厂文档（框架源与镜像）中对分片本地 ID 的引用 MUST 被检出：在合并后语义下解析会改变含义的引用，MUST 逐条记录解决（重指向合并后 ID / 改用逐字字面量 / 用户豁免）。新术语 MUST 经 `.specify/glossary.md` 的既有协议进入词汇表，MUST NOT 在 spec 内联定义第二份术语表。
- **FR-017**: 冲突 MUST 是一等记录：每条含输出件、单元（ID/标题/行区间）、两侧内容摘录、候选处置与状态；任一未决冲突 MUST 阻断 seal（FR-009）。冲突的解决 MUST 显式且留痕（用户裁定或声明的解决规则），MUST NOT 静默择一、MUST NOT 造成内容丢失；引擎 MUST NOT 以「较新/较全/较大/较后」任一单侧截断作为解决。
- **FR-018**: **归属记录** MUST 由合并清单承载，合并清单 MUST 落父 spec 目录的固定文件名 `merge-manifest.json`（机器可读、键序稳定；[[STR-002]] 只引用不复述）：逐输出件记录来源分片与动作，逐单元/逐 ID 记录来源（分片 slug + 原 ID）与重映射；合并完成后父 spec MUST 成为唯一现行权威；分片目录 MUST 被标注 `merged into <父 spec>`（指针或状态行），其内容作为 dated record 保留，MUST NOT 被 seal 删除。分片承载物的后续处置（保留/退役）MUST 按 non-disposable 纪律复核后决定，MUST NOT 默认沉默保留。
- **FR-019**: **证据保全** MUST 遵守 dated-record 红线：分片的 `review.md`、`code-review.md`、`verification.md`、`test-evidence/` 与其它既有日期化测量 MUST NOT 被改写；父级合并视图 MUST 以「汇总行 + 指针」形态引用它们（与 074 父 `verification.md` 既有的聚合指针形态同构），MUST NOT 制造第二份测量。
- **FR-020**: 合并回写的写面 MUST 被限定：只写父 spec 目录、分片的 `merged into` 标注、以及 FR-016 记录过解决方式的出厂文档引用修正；MUST NOT 归档、移动或删除 spec 目录，MUST NOT 触碰 goal/team 树（归 `/speckit.goal` 的 `migrate-archive`），MUST NOT push。并发安全 MUST 按「一 spec 一记录文件」满足：两条并行线封装不同 spec 时写入不同路径，MUST NOT 引入共享可变聚合文件。

#### D. 命令面、边界与取证

- **FR-021**: `/speckit.seal` MUST 由三件产物构成且只有三件：一条命令模板 `templates/commands/seal.md`（逐工具副本经 `scripts/python/regen-command-copies.py` 生成，MUST NOT 手抄）、一个 internal 技能（入口与委派，承载流程说明）、一个确定性引擎 `scripts/python/seal-utils.py`（[[STR-003]]；框架源 + `.specify/` 镜像逐字节一致）。引擎 MUST 仅用 Python 标准库、零新增第三方依赖，MUST 满足宪法 XXI 的脚本接口契约（`--help` / `--version` 零副作用、未声明选项非零拒绝），动作封闭集 MUST 恰为 `merge-plan`（只读：分片集合、逐输出件动作、ID 映射与冲突清单）、`merge-apply`（确定性写父级合并产物、`merge-manifest.json` 与分片 `merged into` 标注）、`seal`（封装判定；成功时同批写 [[STR-002]] 与状态面）、`archive-gate`（只读准入查询：允许退出 `0` / 拒绝退出 `1` 并具名理由 / 输入错误退出 `2`）；每个判定 MUST 由程序给出，MUST NOT 由模型复算。internal 技能 MUST 落 `skills/internal/seal-artifact/SKILL.md`（同族命名先例 `clarify-artifact`），只做入口、编排与报告，MUST NOT 复算判定。
- **FR-022**: 边界 MUST 固定为（全部按指针抵达 owner，不在本规格复述其规则）：`/speckit.feature`（`manage-features`）继续拥有注册表 reconcile 及其声明语义（owner：`skills/internal/manage-features/SKILL.md` 与 `shared/workflow/feature-integration.md` § Status State Machine），seal 只写它拥有的那一条转移与对应记录；`/speckit.review` 继续拥有 review 记录与裁决，seal 只读；`/speckit.sanitize` 的归档 lane（owner：`skills/internal/sanitize-materials/SKILL.md`）与 docs 既有 lane（`/speckit.docs`）继续拥有归档/退休动作，seal 只定义准入状态；`/speckit.goal` 的 `migrate-archive`（owner：`skills/internal/manage-goal/SKILL.md`）继续拥有 spec-local goal/team 树迁移，seal 不迁移、不删除 goal/team 树。
- **FR-023**: **归档准入** MUST 是「只有 `Sealed` 可归档」：任何会退休/归档一条 spec 或把特性行标为归档指针（既有 `Relocated` 形态）的流程 MUST 在动手前查询封装记录与状态，非 `Sealed` MUST 以具名理由拒绝并指向 `/speckit.seal`；准入判据 MUST 只有一个 owner（seal 引擎），消费方按指针查询，MUST NOT 各自实现第二份判定。遗留 `Completed` 行 MUST NOT 被追溯作废，但其归档 MUST 要么先被 seal、要么携带用户显式裁定记录。
- **FR-024**: 「零新增重复机制」 MUST 可静态核验：不新增第二套状态机/值域、不新增第二份注册表或台账、不新增第二个归档机制、不新增调度器或守护进程、不新建并行 spec 树；封装记录与合并清单按 spec 落单文件，MUST NOT 引入共享可变聚合（并发开发安全）。
- **FR-025**: 本特性对每一条可判定断言 MUST 提供契约级或单元级测试（红先或带变异取证），至少覆盖：状态值域漂移守卫、拒绝语义封闭集、合并确定性（两次运行逐字节）、编号与引用完整性、冲突检出（同号不同义、无映射）、归档准入、边界不越权（seal 无移动/删除/push/调度）、并发写路径互异。测试执行 MUST 走既有唯一入口 `scripts/bash/run-tests.sh`。只有措辞变化的检查 MUST NOT 计为取证。

#### E. 074 回合与验收

- **FR-026**: 本特性 MUST 交付一次可执行的 **074 回合**：按 FR-011 识别 074a/074b，按 FR-012…FR-019 合并其全部同名输出件到父 `074-goal-team-sdd-unification/`，产出父级合并后的 review 结论（两片 `review.md` + `code-review.md` 的汇总视图与指针）与合并清单，使父 `tasks.md` 的未勾选行数为 0（57 行拆前记录按 FR-018 的 non-disposable 处置显式复核后保留为带日期记录或标注，MUST NOT 静默覆盖）、父 `verification.md` 每条 SC 有状态行，然后运行 seal。回合终态 MUST 是二值之一：`Sealed` 或带具名阻断清单的拒绝；MUST NOT 有部分封装或静默状态。
- **FR-027**: 074 回合 MUST 对每项实测输入缺陷给出显式处置，MUST NOT 静默默认：(a) 父/分片 SC 行缺 `**Path**` 标记导致闭包判定器 exit 2——逐条记录取值（显式决定，或记录过的严格默认 `final`），MUST NOT 读作通过；(b) 074b 本地 STR 编号与父级同号不同义——按 FR-016 的冲突规则呈现并解决；(c) 出厂文档 `skills/internal/create-team/SKILL.md` 以 074b 分片本地 ID 引用 outcome 字面量（`STR-004`/`STR-005`/`STR-006` 在 074b 本地表为 `completed`/`blocked`/`failed`；父级同号为 `sdd`/`direct`/`adjudicate`）——按 FR-016 检出并记录重指向（合并后父 ID `STR-007`/`STR-008`/`STR-009`）或逐字字面量；(d) 074b review 的 P0（字母分片分支解析到父目录）只带驱动者记录的豁免——按 FR-006 不算用户豁免，须有修复证据或用户显式裁定，否则为具名阻断；(e) 父 `tasks.md` 的 57 行拆前记录——按 FR-018 处置，MUST NOT 静默覆盖或删除。每项 MUST 在回合记录中逐条出现，状态为「已解决（证据指针）」或「阻断（理由）」。
- **FR-028**: 回合裁决 MUST 可复现：合并清单、封装记录或拒绝清单、以及前端状态面三者一致；在阻断状态下重跑 MUST 得到同一阻断清单（幂等、可复现），MUST NOT 因重跑顺序改变结论；回合 MUST NOT 改写任何分片测量记录或 review 记录（FR-019）。

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython 标准库（文件读取、哈希、JSON 与文本判定） | signed-contract | CPython 上游（本仓只消费） | `pyproject.toml` 既有 `requires-python` 下限；本特性零新增第三方依赖 | `pyproject.toml` | 引擎在锁定解释器上跑通全部动作 | FR-021 | EP-001 |
| RS-002 | `pytest`（契约与单元测试） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有测试依赖 | `pyproject.toml` | `bash scripts/bash/run-tests.sh` 全绿 | FR-025 | EP-002 |
| RS-003 | 既有状态与验收引擎（`closure-acceptance-check.py`、status 面、`non-disposable-check.py` 状态—裁决表） | in-scope | 本特性自身（就地扩展其状态值域消费面，不新建引擎） | 不适用（无外部版本面） | 不适用（in-scope） | 状态值域漂移守卫契约测试 | FR-001, FR-007 | EP-003 |

### Key Entities *(include if requirement involves data)*

- **封装记录（Seal record）**：按 spec 一份的最终封装回执，落父 spec 目录 `seal.md`；承载判定时刻与钉住提交、引用的 review 与验收回执、合并清单指针、豁免引用与引擎身份；只引用测量来源，不制造第二份测量。
- **合并清单（Merge manifest）**：一次合并回写的完整归属记录——分片集合与顺序依据、逐输出件动作、逐 ID 家族映射表、冲突清单与解决留痕、合并后校验结果。
- **分片（Slice）**：名字族命中 `<父编号><字母>-<slug>` 且 requirements 显式声明父规格的 spec 目录；是合并的来源，不是封装主体，合并后成为 dated record。
- **冲突项（Conflict）**：无法确定性归并的差异的一等记录；开放即阻断封装；解决必须显式留痕。
- **终态（Sealed）**：`Ready for Review` 之后、可进入最终归档的唯一状态；值域新增一个值、转移新增一条。
- **归档准入（Archive gate）**：既有一切退休/归档动作与唯一封装修正状态之间的判据；owner 是 seal 引擎，消费方只查询。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 封装主路径成立：对一条干净的单体 spec，`/speckit.seal` 把状态从 `Ready for Review` 推进为 `Sealed`（[[STR-001]]），父 spec 目录出现 `seal.md`（[[STR-002]]），注册表行与特性详情同步一致；同一条 spec 重跑幂等且不产生第二条记录；注入「状态面不同步」变异时测试转红。 **Path**: final
- **SC-002**: 拒绝语义完备：对 from 状态错误、P0 未处置（含只有驱动者豁免）、验收行缺失、闭包判定器 exit 2、分片存在未决冲突、分片未闭合、脏 spec 树、状态面漂移（`state-drift`）八类失败各有一个夹具，每一类都以具名理由拒绝且状态不变；「三缺一」夹具 MUST 转红——封装只有在全部条件成立时才发生。 **Path**: final
- **SC-003**: 合并确定性：同一夹具树两次运行产出逐字节一致的合并产物与合并清单；成功后的 `apply` 重跑零 diff；把任一决策改成「按返回时刻排序」注入变异时测试转红。 **Path**: final
- **SC-004**: 合并完整性：合并后的父级产物中，每个在案 ID 家族的序列连续无洞、无重复、零悬空引用；映射表覆盖每个分片条目（无映射、重复映射、目标缺失三类冲突计数为零或全部显式解决）；父 `tasks.md` 未勾选行为 0。任一断言失效时测试转红。 **Path**: final
- **SC-005**: 词汇表对齐有效：同号不同义夹具被检出为冲突（两侧字面量并列），出厂文档引用分片本地 ID 的夹具被检出且解决留痕；不存在「同号不同义静默存活」的合并产物；注入静默重编号变异时测试转红。 **Path**: final
- **SC-006**: 074 真实回合（用户指定的 acceptance 用例）可执行且可复现：以 `.specify/specs/074-goal-team-sdd-unification/` 为目标执行 split→merge-back→seal 全流程；实测输入 MUST 为：074a 32/32、074b 26/26 任务行闭合；父 `tasks.md` 57 个未勾选行；父级无 `review.md`/`code-review.md`；父 `verification.md` 以聚合指针集存在（提交 `91726a641`，每 SC 一行——本条以实测更正简报的「父目录无 verification.md」前提）。回合产出覆盖两片全部实际输出件的合并清单与父级汇总视图；父 `tasks.md` 未勾选行为 0（57 行按 FR-018 显式处置）；父 `verification.md` 每条 SC 有状态行；seal 终态为 `Sealed` 或与 FR-027 五项实测输入一一对应的具名阻断清单；阻断状态下重跑清单一致。 **Path**: final
- **SC-007**: 归档准入有效：非 `Sealed` 的 spec 在任一归档/退休入口被具名拒绝并指向 `/speckit.seal`；`Sealed` 通过同一判据；遗留 `Completed` 的归档路径按 FR-023 记录。把准入判据复制到第二个实现处时测试转红（单一 owner）。 **Path**: supporting
- **SC-008**: 零重复机制可静态核验：状态值域只有一个 owner，全部消费方识别 `Sealed`（任一处移除时漂移守卫转红）；仓库中不存在第二套状态机、第二份注册表、第二个归档机制、调度器或并行 spec 树；seal 引擎 `scripts/python/seal-utils.py`（[[STR-003]]）的动作表不含移动/删除/push/调度。 **Path**: supporting
- **SC-009**: 并发与只读边界成立：两个并发写者对不同 spec 封装时写出不同路径（夹具断言无共享可变聚合）；seal 对 review 记录与分片测量记录的哈希在运行前后一致（只读取证）；对父 spec 树的非本流程改动触发 `dirty-spec-tree` 拒绝。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 单体 spec 夹具（或一条真实单 spec 线）的运行记录：seal 引擎退出码、`seal.md` 内容、`features.md` 行与详情文件的对照快照；幂等重跑的前后哈希对照；变异实测记录在 `test-evidence/`。
- **SC-002 Source**: 八个拒绝夹具（含 `state-drift`）的引擎输出与退出码，逐条比对具名理由与「状态未变」读数；「三缺一」变异记录。
- **SC-003 Source**: 两次运行的合并产物与清单的 sha256 对照；`apply` 重跑的 `git diff --stat` 零输出；「返回时刻排序」变异的转红实测。
- **SC-004 Source**: 合并后产物的程序化扫描（ID 序列、悬空引用、映射覆盖、未勾选行计数），读数写入 `test-evidence/`。
- **SC-005 Source**: 同号不同义与出厂引用两类夹具的冲突清单；解决记录（重指向/逐字/豁免）与合并后解析检查；静默重编号变异的转红实测。
- **SC-006 Source**: 074 回合的合并清单、回合记录与 seal 裁决（封装记录或拒绝清单），逐项对照 FR-027 的五项实测输入；重跑对照。
- **SC-007 Source**: 归档入口的拒绝/通过夹具与引擎查询记录；单一 owner 的检索型断言（第二实现注入转红）。
- **SC-008 Source**: 状态值域漂移守卫契约测试；仓库结构面的静态审计（引擎动作表、目录与注册表清单）；移除 `Sealed` 的变异实测。
- **SC-009 Source**: 并发双写夹具的路径断言；seal 运行前后 review/测量文件哈希对照；脏树拒绝夹具。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"Sealed"` | FR-001, FR-002, SC-001 |
| `STR-002` | `"seal.md"` | FR-010, SC-001 |
| `STR-003` | `"seal-utils.py"` | FR-021, SC-008 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-11-10（无人值守 requirements 阶段，自行裁决并记录）

- Q: `Sealed` 与既有 `Completed` 是什么关系？终态会不会变成两个？ → A: `Sealed`（[[STR-001]]）成为**新工作**的唯一终态，`Ready for Review → Completed` 出口对新转移关闭；`Completed` 只作为遗留记录值保留于本特性之前的行（本仓现有 21 条，不追溯、不降级）。判定理由：用户裁定「sealed 是 Ready for Review 之后的最终态」「sealed 的 spec 方可最终归档」——若 `Completed` 仍可作为前向出口，终态就是二义的，归档准入也不可判定。先例：`Blocked` 当年进入 status 面时，宪法生命周期叙述同样未被逐字展开，operational owner 是 `shared/workflow/acceptance-hardening.md` § Feature Status。（FR-001…FR-003）
- Q: seal 读取「哪一份 review 结论」？拆分场景下父级没有 review，需要先重跑一次父级 review 吗？ → A: 不需要重跑。单体 spec 读其当前 `review.md`/`code-review.md`；拆分 spec 读**合并后的父级 review 汇总视图**（由各分片当前 review 记录合并而来，见 FR-019/FR-026），P0 处置按原记录判定。理由：review 的成本不该被「封装」重复收取，且父级重跑会打断「review → seal」的固定顺序；用户措辞是「按 review 的结论」，不是「按父级 review 的结论」。（FR-006、FR-026）
- Q: 分片本身可以被 seal 吗？ → A: 不可以。唯一封装主体是父 spec（单体 spec 即其自身）；分片是合并来源、合并后成为 dated record。理由：分片共用同一特性注册行与同一 status 面；若允许分片各自 seal，同一行会出现互相覆盖的终态。（FR-005、FR-011）
- Q: 合并回写与 seal 是一条命令还是两条？ → A: 一条命令、两个执行动作（先合并，后封装）；合并可单独「计划/检查」而不封装，但 seal 不能在合并未完成时发生。理由：用户明确「最终确认由 `/speckit.seal` 完成」；拆成两条命令会让「合并完成」与「封装」之间出现无主的中间态。（FR-009、FR-021）
- Q: 合并的确定性边界在哪——散文也能逐字节合并吗？ → A: 结构化单元（ID 行、表格行、条款、任务行、状态行）由引擎确定性合并；散文按声明规则处理——父级文本为权威、分片独有内容进入带来源标注的区块、同一锚点的双端编辑进入冲突清单。理由：不宣称做不到的事；把「散文语义判断」交给模型会让「同输入同结果」不可证。语义对齐的判定依据是**分片声明的映射表**（可机器核验其完备与唯一），不是模型转述。（FR-013、FR-015、FR-017）
- Q: 074 背景事实里「父目录无 verification.md」是否仍成立？ → A: 实测不成立——父 `074-goal-team-sdd-unification/verification.md` 已于 2026-10-29 由提交 `91726a641` 落盘，形态是**聚合指针集**（每条 SC 指向分片测量记录，「never a second measurement」）。仍然成立的是：父 `tasks.md` 57 个 `[ ]` 行（本日实测 `grep -cE '^- \[ \]'` = 57）、父级无 `review.md`/`code-review.md`。本规格以实测为准，并以父级聚合指针形态作为合并视图的同构先例。（FR-019、FR-026）
- Q: 缺 `**Path**` 标记 / 闭包判定器 exit 2 怎么处置？ → A: 按输入缺陷处置，绝不当通过。合并回写必须为每条 SC 记录一个显式取值；若走默认，默认只能是更严格的一侧（`final`），且必须被记录——MUST NOT 静默默认 `supporting`。（FR-007、FR-027）
- Q: 074b review 的 P0 带「驱动者记录的显式豁免」，算不算「review 结论无 P0」？ → A: 不算。既有 waiver 纪律规定只有 user-authored artifact 或用户本会话裁定构成豁免；驱动者/协调者/代理的确认不是。因此 074 回合要么有该 P0 的修复证据、要么有用户显式裁定，否则 seal 以具名理由阻断——这正是「可被 seal 处置」的诚实形态：可执行、可复现、结论明确，而不是为了绿而放行。（FR-006、FR-027）
- Q: 归档准入放在哪？seal 自己会执行归档吗？ → A: seal 从不归档。归档动作仍归既有 lane（`/speckit.sanitize` 的归档 lane、docs 既有 lane、`manage-features` 的归档指针形态），seal 只提供一个**准入判据**（只有 `Sealed` 可归档），消费方按指针查询。理由：用户要求「归档归 sanitize/docs 既有 lane」。（FR-022、FR-023）
- Q: 遗留 `Completed` 行怎么办？ → A: 不追溯改写、不降级；它们不自动获得归档准入，归档需要先 seal 或携带用户显式裁定。这是对「sealed 的 spec 方可最终归档」的诚实落地：既不伪造历史，也不放行未封装者。（FR-003、FR-023）

### Session 2026-11-10（clarify 阶段，无人值守，自行裁决并记录）

- 用户修订指示（2026-11-10，阶段派发）：074-goal-team-sdd-unification（074a 32/32 + 074b 26/26、父 tasks.md 57 未勾选行）必须作为 seal 的真实 acceptance 用例执行 split→merge-back→seal 全流程并落成 SC。→ 已落成 SC-006。简报中的「父目录无 verification.md」经实测不成立：父 verification.md 以聚合指针集存在（提交 `91726a641`，每 SC 一行），本规格与 SC-006 以实测为准。另经实测更正 FR-027(c) 的片号（出厂文档的 outcome 引用对应 074b 本地编号，不是 074a）。
- Q: `Related Feature` 仍为 `Need clarification`，本 spec 绑定哪个 Feature？ → A: 新建 Feature `099`（名称见 `## Related Feature`）。检索 `.specify/features.md` 全表与 `features/` 详情后无既有 Feature 覆盖 seal/合并回写；先例是 090–094 各自 1:1 绑定自身编号。注册表行与详情文件的创建属 feature-integration § Feature Binding Rules 的 clarify 义务；本阶段写面仅 `requirements.md`，故记录为待办，恢复点为下一次 `manage-features` reconcile。
- Q: 封装的状态写入失败或判定被拒时，是否需要回退与持久化拒绝记录？ → A: 两阶段执行（只读判定 → 全成立才写）；`seal.md`（[[STR-002]]）与状态面同批落盘，写入中途失败按原字节恢复已写文件并退出 `2`；拒绝（退出 `1`）零持久化写入，拒绝报告只经 stdout，不新建拒绝记录或第二份台账；重跑由同一确定性重算复现。状态面互相矛盾时以 `state-drift` 退出 `2`，不择一采信。（FR-005、FR-009）
- Q: 审计更正（`Sealed → Ready for Review`）后再次封装，旧回执如何处理？ → A: [[STR-002]] 只承载当前回执；再次封装原子替换并在机器可读核心写 `supersedes: <前回执钉住的提交>`；前回执由 git 历史承载，不建第二份回执文件或历史聚合。（FR-002、FR-010）
- Q: 合并输出件的「必选」与「按实际产出枚举」边界在哪？ → A: 候选宇宙是 FR-012 的 15 个名单（封闭集）；必选下限 = `tasks.md`（无论分片是否产出）+ 分片非空时的父 `verification.md` 聚合指针、父 `review.md` 汇总指针与合并清单（`merge-manifest.json`）；其余候选取并集（任一分片或父级实际存在即进入），逐件记录 `merge`/`create`/`keep`/`not-applicable`，`not-applicable` 仅两侧皆缺席。（FR-012、FR-018）
- Q: 引擎动作与退出码的封闭集是什么？ → A: 动作恰为 `merge-plan`（只读）、`merge-apply`、`seal`、`archive-gate`（只读准入查询）；统一退出码 `0` 成功/幂等、`1` 前置条件拒绝、`2` 输入或环境错误；`--help`/`--version` 零副作用。internal 技能落 `skills/internal/seal-artifact/SKILL.md`，只编排与报告，判定一律由引擎给出。（FR-021）

## Assumptions

- **A1（seal 是 spec 级封装，不是部署动作）**：「封装」指 spec 生命周期的终态与归档准入，不涉及部署/发布/运行时；`Completed` 若在别处表示部署完成，其语义属于部署语境，不在本特性展开。（FR-003）
- **A2（合并是归并视图，不是重写历史）**：dated record 红线优先于「父级单文件完整」的偏好；父级承载汇总与指针，分片测量保持原样。（FR-019）
- **A3（状态值域就地扩展，不迁移存量）**：不重写既有行、不迁移 `.specify/specs/` 布局、不改写既有 `Completed`/`Relocated` 记录。（FR-003）
- **A4（074 回合的终态允许是阻断）**：回合的验收对象是「完整、可复现、逐条点名的裁决」，不是「必须 `Sealed`」；P0 的修复或用户裁定是外部输入，本特性 MUST NOT 以自判豁免替代它。（FR-027、SC-006）
- **A5（零新增运行时依赖）**：引擎 stdlib-only；所有判定复用既有程序与既有状态面，不构建在线服务或数据库。（FR-021、RS-001）
- **A6（ID 家族按制品声明）**：合并只为每个制品**已经声明**的 ID 家族重排；不在合并中发明新的 ID 体系；无法归类的新形态按冲突处理。（FR-014）
- **A7（背景事实以实测为准）**：「父目录无 verification.md」已被实测更正为「父目录有聚合指针集 verification.md」；规格与后续阶段一律引用实测读数，不沿用简报中的旧前提。（FR-019、FR-026）
