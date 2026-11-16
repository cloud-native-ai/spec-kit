# Requirements Specification: 长任务 line 登记与 status 可见性（Line Registry Registration）

**Requirement Branch**: `102-line-registry-registration`
**Created**: 2026-11-16
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（编写/修订 `shared/guidelines/**`、`scripts/bash/**`、`scripts/python/**`、`templates/commands/**`、`templates/instructions-template.md`、`skills/internal/**` 与 `.specify/specs/**` 的维护者）与下游项目中运行无人值守长任务、使用 `/speckit.status` 判定「现在到底有没有东西在跑」的维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「为什么一个正在跑的后台批量 apply/verify 或长时间测试在 digest 里显示 `nothing-running`」「哪些任务算长任务、这条判据归谁拥有」「`line-run.sh` 登记什么、失败与 SIGKILL 时留下什么」「registry 的写入方到底是谁」「扫描器判什么、凭什么算有牙、活仓库扫描根为何必须是可跟踪路径」「环境段的提醒为什么只有一句指针」时打开本规格，据 FR-001…FR-023 与 SC-001…SC-009 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "固化「长任务必须登记 line、否则立即变红」的机制边界。/speckit.status 的当前态摘要（digest）只读环境级 Line Registry、从不扫进程，因此任何未登记 line 的长任务（后台批量 apply/verify、长时间测试、无人值守批处理）在 digest 中必然显示 nothing-running——这是「未登记即不可见」的机制缺口，不是漏报。本特性交付：① owner 文档 shared/guidelines/reporting-obligations.md § 九 新增判据（预计超过 5 分钟或含后台批量 apply/verify 的任务 MUST 在启动时登记 line、按阶段 heartbeat、结束时 close；未登记即不进入 digest，nothing-running 是准确结论）；② framework 源新增 scripts/bash/line-run.sh 包装器（register → 执行 → 按结果 close；被 SIGKILL 等无法收尾时保留 active 供 digest 显示；registry 写入方是 line-registry.py，不是 journal-utils.py）；③ 接线：run-team 技能在运行前登记 line、执行中 heartbeat、报告时关闭并记录 line_id；templates/commands/status.md 声明 digest 以 registry 为唯一来源、不得改为扫进程；.specify/instructions.md 增加一条指针式环境提醒（经模板同步落地，不复述判据）；④ 契约与行为测试：脚本接口（-h/--version 退出 0、拒绝未声明选项）、临时 registry 下的成功/失败登记行为、扫描器 fixture 正反例（在 .specify/.tmp/ 下造一个含 terraform apply 且未登记的脚本判红，包上 line-run.sh 后判干净）、活仓库可跟踪扫描根干净。所有对外分发的改动落在 framework 源（scripts/、shared/、templates/、skills/）并经 sync-mirrors 投影，不只手改 .specify/ 运行时。"

## Related Feature *(mandatory)*

**Feature ID**: Need clarification
**Feature Name**: Need clarification

## Overview

`/speckit.status` 的当前态摘要（digest）在 087 落地时被固定为**只读环境级 Line Registry、从不扫进程**（`scripts/python/status-digest.py`，owner `shared/guidelines/reporting-obligations.md` § 九）。这条只读边界让 digest 具备确定性，但也让一条未登记 line 的长任务在摘要里**必然**显示 [[STR-006]]：这不是漏报，而是「未登记即不可见」的机制缺口。长任务目前不登记的原因不是没有载体，而是没有一条判据说「必须登记」，也没有一个让登记**顺手发生**的包装器。

本特性固化一条判据与一个载体，使「长任务不登记 line」在本仓**立即变红**，而不是等 status 与事实不符时才被发现：

1. **判据**落在 owner 文档 `shared/guidelines/reporting-obligations.md` § 九：预计超过 5 分钟、或含后台批量 apply/verify 的运行（含长时间测试与无人值守批处理）MUST 在启动时登记 line、按阶段 heartbeat、结束时 close；未登记即不进 digest，[[STR-006]] 是准确结论而非漏报。判据的**判定边界**由该文件拥有，`/speckit.status` 只按路径引用、不复述。
2. **载体**是 framework 源新增的 [[STR-001]] 包装器：`register → 执行 → 按结果 close`；被 SIGKILL 等无法收尾时**保留 active**，让 digest 显示它。任何批量脚本改成 `line-run.sh --line-id <slug> --run-id <id> -- bash batch.sh` 即自动登记，不再依赖 agent 记得手动调引擎。
3. **接线**覆盖三处：`skills/internal/run-team/SKILL.md` 在运行前登记、执行中 heartbeat、报告时关闭并记录 [[STR-007]]；`templates/commands/status.md` 增一句声明 digest 以 registry 为唯一来源、不得改为扫进程；`templates/instructions-template.md` 的既有 `## Progress Reporting Discipline` 环境段增一条**指针式**提醒（一句话 + owner 路径），经模板同步投影到 `.specify/instructions.md` 及其符号链接。
4. **契约与行为测试**证明载体可用且判据有牙：脚本接口、临时 registry 下的成功/失败登记、SIGKILL 残留、扫描器 fixture 正反例、活仓库可跟踪扫描根干净。

**必须纠正的三项前提（不得静默沿用原始方案）**：

- **P1 写入方言**：registry 的唯一写入方是 [[STR-002]]（framework 源 `skills/external/sdd-loop-driver/scripts/line-registry.py`）。`scripts/python/journal-utils.py` 与 registry **零关系**（只写 observer journal），`line-run.sh` 与 run-team 接线都 MUST NOT 经它写 registry。见 FR-005。
- **P2 扫描判据不得是空判**：`.specify/teams/.work/**` 是本仓当前为空的运行期目录，以它作唯一扫描根、以 `terraform apply` 作唯一模式会让测试永远绿。扫描根 MUST 是可跟踪路径，扫描器 MUST 用 fixture 证明有牙。见 FR-012…FR-016。
- **P3 环境段是指针不是副本**：环境段只给一句话 + owner 路径，不复述判据；落地经 `templates/instructions-template.md` 模板同步（不手改再生成产物）。见 FR-019。

**不做什么**：不引入调度器、定时器服务、常驻进程、第三方依赖、第二份 registry、第二份状态脊或任何台账（`reporting-obligations.md` § 十一 的禁令）；不把 digest 改成扫进程；不新建自动 stale 清理；不改 `status-digest.py` 的动作集、退出码闭集与 [[STR-006]] 渲染；不新建第二条 liveness 通道；不推送远端。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **长任务判据 = 人工阈值 + 机械可判定投影**。人工阈值：预计超过 5 分钟、或含后台批量 apply/verify（含长时间测试、无人值守批处理）。机械投影（扫描器判定的封闭集）：脚本内容含 [[STR-004]]、调用 [[STR-005]]、或头部显式标记 [[STR-003]]。 | 人类判据无法对文件机械判定；扫描器只对可判定的投影负责，两者由同一 owner 声明，扫描器不另立语义。 |
| **A-2** | **机械判据只有一份机器可读 owner**：声明层 fact（候选 `shared/declarations/facts/long-task-criteria.yaml`）或扫描器内常量，二者**择一**由 plan 定稿；其余位置（owner 文档、测试、包装器）只引用，不复述封闭集。 | One Source Of Truth；brief §4 要求「判据写成单一 owner（常量或声明）」。 |
| **A-3** | **扫描根 = 可跟踪路径**：`scripts/bash/` 必选，`templates/`、`skills/` 由 plan 按信噪比定稿；`.specify/teams/.work/**` 一类运行期目录 MUST NOT 作为唯一扫描根。 | 运行期目录为空且不受跟踪，以它为唯一根等于空判（brief §4 P2）。 |
| **A-4** | **包装器参数形**：[[STR-001]] `--line-id <slug> --run-id <id> [-- <command…>]`。终止 reason 闭集 = [[STR-008]]（`completed` / `failed`）；条目 state 仍由引擎拥有为 `closed`，本规格不新增状态词。 | 复用 `line-registry.py` 既有 `register` / `deregister --reason` 语义，不新增状态机。 |
| **A-5** | **失败闭合（fail closed）**：登记失败时包装器 MUST NOT 执行被包装命令并 MUST 非零退出、具名原因；执行后关闭失败 MUST 上浮为非零退出，且不得遮蔽被包装命令的结果。 | 若登记失败仍执行，长任务又回到不可见状态，判据失去牙齿；关闭失败则 digest 仍显示 active，必须让操作者看到。 |
| **A-6** | **环境段落点**：`templates/instructions-template.md` 既有 `## Progress Reporting Discipline` 小节内加**一条** bullet（一句话 + `shared/guidelines/reporting-obligations.md` § 九 路径）；`.specify/instructions.md` 由 `/speckit.instructions` 再生成，MUST NOT 手改。 | brief §4 P3；手改 live 文件会在下次再生成时丢失，且破坏符号链接模型的单一来源。 |
| **A-7** | **run-team 接线按现有小节名，不复制简报的旧 PHASE 编号**：在 §1 Load 之后、§6 Orchestrate 之前登记 line；§6 执行期按阶段 heartbeat；§7 Report 关闭并记录 [[STR-007]]。 | brief 写的「PHASE 1 / PHASE 3/4 / Report」与当前技能小节编号（1 Load … 6 Orchestrate、7 Report）不一致；意图明确（开始登记、执行中心跳、报告时关闭），按现有小节名落地方可被维护者定位。 |
| **A-8** | **heartbeat = 经引擎刷新末次事件**（`line-registry.py` 的 `update` 动作，写入带阶段标签的 `last_event`），不新增心跳文件或第二通道；引擎条目已有的 `heartbeat_path` 归既有流程，本特性不改其语义。 | 复用既有载体，满足 § 十一 零新增机制；「按阶段 heartbeat」需要可判定的落地形态。 |
| **A-9** | **并发与重入归引擎**：同 `line_id` 已存在时，包装器 MUST 让引擎的冲突/拒绝结果上浮并按 A-5 闭合，MUST NOT 静默覆盖或重建条目。嵌套包装器各自登记自己的 line。 | 引擎拥有条目身份与状态；包装器是薄适配层，不另立所有权规则。 |
| **A-10** | **SIGKILL 残留保留、无自动清理**：包装器无法收尾时条目保持 `active`（由 digest 按过期界限标记 stale 并显示时长）；本特性不新增清理守护进程或定时器。 | brief §2.2；§ 十一 禁止新守护进程。残留的处置走既有流程。 |
| **A-11** | **组件命名**：包装器 [[STR-001]]（先例 `line-registry.py`）；扫描器名称与路径由 plan 定稿（候选 `scripts/python/line-registration-scan.py`），本规格只固定其可判定行为与退出码，不固定文件名。 | 名称遵循 Grounded Naming 的项目约定；命令/脚本路径按 `templates/commands/status.md` 的先例由 plan 阶段固定。 |
| **A-12** | **Feature 绑定留待 `/speckit.clarify`**：`Related Feature` 保持默认 `Need clarification`。 | `create-requirements` 技能的绑定时机约定：本阶段不查表、不建 Feature。 |
| **A-13** | **「长任务」以调用方生命周期计**：被包装命令若自身立即返回、把工作交给后台而调用方已结束，则包装器正常 close，该后台工作不在本判据范围内（需要可见性的后台工作应自行经包装器或引擎登记）。 | 包装器能观察到的生命周期只有被包装命令的进程；把不可观察的后台生命周期纳入会让判据不可判定。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 后台批量脚本经包装器自动登记，运行期在 digest 里可见 (Priority: P1)

维护者有一个预计要跑十几分钟的批量 apply/verify 脚本。她不再需要记得先手动调 registry 引擎，而是把调用改成 [[STR-001]] `--line-id batch-apply --run-id <id> -- bash batch.sh`。包装器在命令启动前把 line 登记为 `active`，运行期间 digest 能列出这条 line 及其最近活动；命令成功结束以 `completed` 关闭，失败以 [[STR-008]] 中的 `failed` 关闭；若包装器被 SIGKILL，条目保持 `active`，digest 仍显示它（并按过期界限标记 stale 与时长）。

**Why this priority**: 这是用户诉求的第一句——长任务不登记是根本问题；包装器让登记顺手发生，否则判据只是又一条靠记忆执行的义务。

**Independent Test**: 在隔离的 `$SPECIFY_LINE_REGISTRY_DIR` 下运行包装器包住一个短命令：运行期间与结束后各读一次 digest，断言条目出现、state 与 `last_event` 按结果变化；再模拟 SIGKILL，断言条目残留 `active` 且 digest 可见。

**Acceptance Scenarios**:

1. **Given** 隔离 registry 与一个成功的被包装命令，**When** 运行 `line-run.sh --line-id demo --run-id r1 -- true`，**Then** registry 中出现 `line_id=demo` 的条目，运行期间其 `state` 为 `active`，结束后 `state` 为 `closed` 且 reason 为 `completed`，包装器退出 0。
2. **Given** 同一隔离 registry 与一个失败命令，**When** 运行 `line-run.sh --line-id demo2 --run-id r2 -- false`，**Then** 包装器以被包装命令的非零退出码退出，条目 `state` 为 `closed` 且 reason 为 `failed`。
3. **Given** 一个运行中的包装器被 SIGKILL，**When** 读取 registry 与 digest，**Then** 条目仍为 `active`（不被删除、不被标 closed），digest 列出它并显示其最近活动时长。
4. **Given** registry 目录不可写，**When** 运行包装器，**Then** 被包装命令**未被执行**，包装器非零退出并具名报告登记失败。

---

### User Story 2 - 未登记的长任务在本仓立即变红，而不是永远绿 (Priority: P1)

维护者想知道「本仓有没有长任务脚本绕过了登记」。她运行确定性扫描器：它以声明的可跟踪扫描根为单位，对每个命中长任务机械判据（[[STR-004]] / [[STR-005]] / [[STR-003]]）却既未经包装器调用、也未直接调 registry 引擎登记的文件报违规并给出路径；干净时退出 0，有违规时退出 1。扫描器用 fixture 证明有牙：临时造一个含 [[STR-004]] 且未登记的脚本判红，包上包装器后判干净；对活仓库的声明扫描根，读数为 0 违规。

**Why this priority**: 与 US1 同等重要——没有扫描器，判据只是文档措辞；而用空的运行期目录或单一模式做扫描根会让测试永远绿，等于没有判据。

**Independent Test**: 在 `.specify/.tmp/` 下生成正例与反例脚本，分别调用扫描器；再对活仓库扫描根运行一次，断言三组退出码与输出。

**Acceptance Scenarios**:

1. **Given** `.specify/.tmp/` 下一个含 [[STR-004]]、未经包装器调用、也未调 registry 引擎的临时脚本，**When** 以该目录为扫描根运行扫描器，**Then** 退出 1，输出给出该文件路径与被命中的判据。
2. **Given** 同一临时脚本改为经 [[STR-001]] 调用（或直接调用 `line-registry.py` 的 register/update/deregister），**When** 再次扫描，**Then** 退出 0，输出零违规。
3. **Given** 活仓库与声明的可跟踪扫描根，**When** 运行扫描器，**Then** 退出 0，零违规；读数（扫描根清单、文件数与命中数）写入 `test-evidence/`。
4. **Given** 扫描根被误配为一个空的运行期目录（如 `.specify/teams/.work/`），**When** 运行扫描器，**Then** 它按声明的根清单判定并在输出中显示实际根，而不是把空目录渲染成「干净」的等价证明。

---

### User Story 3 - 判据有唯一 owner，下游表面只给指针 (Priority: P2)

维护者要回答「这条判据是谁定的、改一次要改几个文件」。答案必须是：owner 文档 `shared/guidelines/reporting-obligations.md` § 九 拥有判据与判定边界；`templates/commands/status.md` 只声明 digest 以 registry 为唯一来源、不得扫进程；环境段（`templates/instructions-template.md` 投影到 `.specify/instructions.md` 与其符号链接）只有一句指针提醒；技能与测试只按路径引用。删掉任一表面或把 owner 的判据复述进下游，契约测试转红。

**Why this priority**: 判据一旦在多处复述就会漂移；而环境段是让每个会话第一眼就看到提醒的唯一位置，必须是指针而不是副本。

**Independent Test**: 检查四个表面的文本与引用方向；注入一次「删掉环境段指针」与一次「在 status.md 里复述判据」的篡改，断言契约测试各自转红。

**Acceptance Scenarios**:

1. **Given** 本特性落地后的仓库，**When** 阅读 `shared/guidelines/reporting-obligations.md` § 九，**Then** 判据（>5 分钟 / 后台批量 apply/verify、启动登记、阶段 heartbeat、结束 close、未登记即 [[STR-006]]）与判定边界在此，且是唯一详细定义点。
2. **Given** `templates/commands/status.md`，**When** 阅读它，**Then** 它含一句「digest 以 registry 为唯一来源、不得改为扫进程」，且未复述 § 九 的判据条目或增加渲染逻辑。
3. **Given** `templates/instructions-template.md` 的 `## Progress Reporting Discipline`，**When** 阅读它，**Then** 它含一条一句话指针 + owner 路径，且 `.specify/instructions.md` 中该句与模板投影一致（经再生成，不是手改）。

---

### User Story 4 - 无人值守团队运行与 status 接线不再依赖记忆 (Priority: P2)

自动化执行者运行一个团队（`run-team`）。在真正开始编排前，它先登记 line；编排过程中按阶段刷新末次事件；运行报告写入时关闭 line 并把 [[STR-007]] 写进运行报告。于是 digest 在整个团队运行期间都能回答「在跑什么」，运行报告也能把「这次运行对应哪条 line」交给后续审计。

**Why this priority**: 无人值守正是最容易「长时间没东西可见」的场景；把登记写进技能步骤，才让义务随执行体一起被携带。

**Independent Test**: 检查技能文本的三处步骤与运行报告的字段；用契约测试断言步骤存在、[[STR-007]] 字段在报告契约中被要求、删除任一处即红。

**Acceptance Scenarios**:

1. **Given** `skills/internal/run-team/SKILL.md`，**When** 阅读 Workflow，**Then** 它在运行开始前登记 line、在执行期按阶段 heartbeat、在 Report 步骤关闭 line，三处都以引擎路径引用、不复述引擎参数表。
2. **Given** 一次按技能执行的运行，**When** 阅读其运行报告，**Then** 报告携带该次运行的 [[STR-007]]，且该值可在 registry 中解析到对应条目。
3. **Given** 运行期间的 digest，**When** 读取它，**Then** 团队运行对应的 line 被列出（不再显示 [[STR-006]]）。

---

### Edge Cases

- **被包装命令自己派生后台工作后立即返回**：包装器按调用方生命周期正常关闭；该后台工作若也需要可见性，须自行经包装器或引擎登记（A-13）。判据不声称覆盖不可观察的进程。
- **同一 `line_id` 并发/重复登记**：包装器把引擎的拒绝或冲突结果上浮并非零退出，不覆盖既有条目（A-9）。
- **registry 根被 `$SPECIFY_LINE_REGISTRY_DIR` 指向不存在或不可写的目录**：登记失败即不执行（A-5）；错误信息点名该路径。
- **包装器自身被 SIGKILL / 宿主机掉电**：条目保持 `active`；digest 按过期界限将其标记 stale 并显示时长（A-10），不自动删除。
- **被包装命令以信号终止**：非零退出按 `failed` 关闭；若包装器自身无法捕获而退出，条目残留 `active`。
- **扫描器的误报**：判据是内容匹配，注释里出现 [[STR-004]] 也会命中。合规途径有二：经包装器调用、或加头部标记 [[STR-003]] 并把该文件纳入长任务登记；扫描根刻意不含 `tests/` 等夹具目录，避免把测试样本判成产线违规（A-1/A-3）。
- **`run-tests.sh` 自身提供 `--full` 路径**：它不得仅因「支持 `--full`」被判违规；只有调用方脚本（或显式头标记）进入长任务集合（A-1）。
- **环境段再生成**：手改 `.specify/instructions.md` 会在 `/speckit.instructions` 再生成时丢失；改动只落模板（A-6）。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系统 MUST 在 owner 文档 `shared/guidelines/reporting-obligations.md` § 九（当前态摘要契约）新增长任务判据：预计超过 5 分钟、或含后台批量 apply/verify 的运行（含长时间测试、无人值守批处理）MUST 在启动时登记 line、按阶段 heartbeat、结束时 close；未登记的运行不进入 digest，[[STR-006]] 是准确结论而非漏报。判定边界由该文件拥有。
- **FR-002**: 长任务判据的**机械可判定投影**（脚本内容含 [[STR-004]]、调用 [[STR-005]]、或头部标记 [[STR-003]]）MUST 恰好有一个机器可读 owner（A-2）；扫描器、测试与文档 MUST 引用它，MUST NOT 各自复述该封闭集。
- **FR-003**: framework 源 MUST 新增包装器 [[STR-001]]，并经 `scripts/python/sync-mirrors.py` 投影到 `.specify/scripts/bash/`；镜像 MUST NOT 手改。
- **FR-004**: 包装器 MUST 在被包装命令启动前，经 registry 引擎 [[STR-002]] 把 line 登记为 `active`；执行 `--` 之后的命令；按结果关闭：退出 0 → reason `completed`，非零 → reason `failed`。终止 reason 取值域见 [[STR-008]]。
- **FR-005**: 包装器与 run-team 接线对 registry 的写入 MUST 只经 [[STR-002]]；MUST NOT 使用 `scripts/python/journal-utils.py` 写 registry，MUST NOT 把 journal 与 registry 混用为同一存储。
- **FR-006**: 登记失败时，包装器 MUST NOT 执行被包装命令，MUST 以非零退出并具名报告失败原因（fail closed，A-5）。
- **FR-007**: 包装器 MUST 原样传播被包装命令的退出状态；执行后关闭失败 MUST 上浮为非零退出，并同时指名命令结果与 registry 失败，MUST NOT 遮蔽或改写任一方。
- **FR-008**: 包装器被 SIGKILL 等无法收尾时，其 line 条目 MUST 保持 `active`（不被删除、不被改写为 `closed`），使 digest 可见（A-10）。
- **FR-009**: 包装器 MUST 在运行开始与结束时经引擎刷新该 line 的末次事件；当它能观察到阶段边界时，MUST 在每个边界刷新一次（A-8）。MUST NOT 新增心跳文件或第二 liveness 通道。
- **FR-010**: 包装器 MUST 遵守既有的 registry 目录解析顺序（`$SPECIFY_LINE_REGISTRY_DIR` → `$XDG_STATE_HOME/spec-kit/lines` → `~/.local/state/spec-kit/lines`），使测试可用环境变量隔离；MUST NOT 引入新的 registry 根覆盖变量。
- **FR-011**: [[STR-001]] MUST 满足 Script Interface Contract：`-h` / `--help` 与 `--version` 回答后退出 0 且零 registry 写入；未声明选项 MUST 被非零拒绝且不执行被包装命令；MUST NOT 联网、MUST NOT push。
- **FR-012**: 系统 MUST 提供一个确定性、只读的扫描器：扫描声明的可跟踪根，对每个命中长任务机械判据（FR-002）却未经包装器调用、也未直接调用 [[STR-002]] 的 register/update/deregister 的文件报违规，输出文件路径与命中的判据；干净退出 0、有违规退出 1、输入错误退出 2；MUST 支持扫描根覆盖以服务 fixture；MUST NOT 写入、派生进程或联网。
- **FR-013**: 扫描器的活仓库扫描根 MUST 是可跟踪路径（至少含 `scripts/bash/`，可含 `templates/`、`skills/`，由 plan 定稿）；`scripts/` 之外的运行期目录（如 `.specify/teams/.work/**`）MUST NOT 作为唯一扫描根，MUST NOT 以空目录的「零命中」充当干净证据（A-3）。
- **FR-014**: 扫描器 MUST 认可以下两类合规形态：文件经 [[STR-001]] 调用；或文件直接调用 [[STR-002]] 的 register/update/deregister。头部标记 [[STR-003]] 用于让一个**本身**构成长任务的脚本声明自己，避免把仅提供长任务路径的脚本（如 `run-tests.sh` 的 `--full` 选项）误判。
- **FR-015**: 测试 MUST 在 `.specify/.tmp/` 下生成含 [[STR-004]]、未登记的临时脚本，断言扫描器报违规；再把同一脚本改为经 [[STR-001]] 调用，断言扫描器判干净（fixture 有牙，正反两例都断言）。
- **FR-016**: 对活仓库声明的扫描根，扫描器 MUST 给出零违规读数，且该读数（根清单、扫描文件数、命中数）MUST 写入 `test-evidence/`；读数 MUST NOT 以暂定数字冒充实测。
- **FR-017**: `skills/internal/run-team/SKILL.md` MUST 在运行开始前登记 line、在执行期按阶段 heartbeat、在 Report 步骤关闭 line 并把 [[STR-007]] 写入运行报告（落点按 A-7 的现有小节名）；三处 MUST 以路径引用引擎，MUST NOT 复述引擎参数表。
- **FR-018**: `templates/commands/status.md` MUST 增一句声明：digest 以 Line Registry 为唯一来源，MUST NOT 改为扫进程（保持确定性）；该句 MUST NOT 复述 § 九 的判据条目，MUST NOT 增加渲染逻辑。
- **FR-019**: `templates/instructions-template.md` 的 `## Progress Reporting Discipline` 环境段 MUST 增一条**指针式**提醒（一句话 + owner 路径）；`.specify/instructions.md` 及其符号链接 MUST 经再生成获得该句，MUST NOT 手改（A-6）。
- **FR-020**: `/speckit.status` 的 digest MUST 保持只读 registry、零进程派生、动作集与退出码闭集不变，[[STR-006]] 的显式渲染不变；本特性 MUST NOT 引入第二个 parser 或第二个 renderer。
- **FR-021**: 测试 MUST 经唯一入口 `scripts/bash/run-tests.sh` 运行（缺省并行形态，路径与参数原样转交），并按 `contract` / `integration` 标记归档；执行记录（命令、退出码、完整输出、耗时）MUST 留证。
- **FR-022**: 本特性 MUST NOT 引入调度器、定时器服务、常驻进程、第三方依赖、第二份 registry、第二份状态脊或台账（`reporting-obligations.md` § 十一 禁令）；新增物仅限包装器、扫描器、测试与文本接线。
- **FR-023**: 变更 MUST 只提交本特性产物；既有未跟踪文件（`.specify/scripts/line-registry.py`、`.specify/scripts/stage-runner.sh`）MUST NOT 被提交或还原；MUST NOT 推送远端。

### Key Entities *(include if required)*

- **Line（登记的工作单元）**：`line_id`、`run_id`、`state`（取值域归 `line-registry.py`）、`last_event`、`updated_at`，以及既有引擎字段（`driver_session`、`claimed_ns` 等）；由引擎拥有身份与状态。
- **Registry 条目**：环境级 registry 目录下每线一个 `<line_id>.json`；digest 的唯一读取源。
- **长任务脚本**：落在声明扫描根内、命中长任务机械判据的文件；合规形态为经包装器调用、直接调引擎登记、或自身带头部标记。
- **包装器调用**：一次 `line-run.sh --line-id … --run-id … -- <command…>` 运行；产生登记 → 执行 → 关闭三事件，失败与 SIGKILL 各留下可判定的残留形态。
- **Digest 读数**：`/speckit.status` 对 registry 的单次只读投影；[[STR-006]] 是空集合的显式渲染。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖、不新增第三方包——它交付一个 bash 包装器与一个只读扫描器，并消费既有的 Python 解释器、pytest 运行器、既有 line-registry 引擎与既有 status-digest 引擎。每行可机械判定，零散文声明。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段不建 premises 表）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库（扫描器的目录遍历与文本判定、测试夹具生成与 registry 条目读取） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 既有 `requires-python` 下限；本特性零新增第三方依赖 | `pyproject.toml` | 扫描器与新增测试在 `>=3.8` 解释器上经唯一入口 `scripts/bash/run-tests.sh` 通过；本特性新增第三方 import 为零 | FR-012, FR-015 | EP-001, EP-002 |
| RS-002 | POSIX `bash` 运行时（包装器本体及其对被包装命令的子进程调用） | signed-contract | bash 上游 / 运行环境（本仓只消费） | 本仓无版本声明；pin 由 `bash --version` 在 test-evidence 的首次采集记录提供 | `scripts/bash/common.sh` | 包装器在 `bash scripts/bash/line-run.sh` 下完成登记→执行→关闭全程；`-h` / `--version` 退出 0 且零 registry 写入 | FR-003, FR-021 | EP-005 |
| RS-003 | `pytest` 测试运行器（契约测试、行为测试与扫描器 fixture 正反例） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有 pytest 声明；本特性零新增依赖 | `pyproject.toml` | `scripts/bash/run-tests.sh` 运行新增 `contract` / `integration` 测试，结果集相对 implement 入口基线零新增红 | FR-015, FR-016, FR-021 | EP-002 |
| RS-004 | 既有 line-registry 引擎的写入面（`register` / `update` / `deregister`） | signed-contract | 既有 sdd-loop-driver 引擎（本特性只消费，不修改其动作集与状态词） | 仓内既有实现，无外部版本面；pin 由 `--help` 声明的动作集与退出码闭集固定 | `skills/external/sdd-loop-driver/scripts/line-registry.py` | 隔离 `$SPECIFY_LINE_REGISTRY_DIR` 下成功/失败/SIGKILL 三形态在引擎条目上留下 [[STR-007]]、`state` 与 reason；包装器不引用 `journal-utils.py` | FR-004, FR-005, FR-008, FR-009, FR-010 | EP-003 |
| RS-005 | 既有 status-digest 引擎（digest 只读读数的唯一来源） | signed-contract | 既有 `/speckit.status` 摘要引擎（本特性只读消费，不修改动作集与退出码闭集） | 仓内既有实现，无外部版本面；pin 由 FR-020 的闭集不变断言固定 | `scripts/python/status-digest.py` | 隔离 registry 上运行期间与结束后各读一次 digest，读数与 registry 条目一致；本特性对其零修改 | FR-001, FR-020 | EP-004 |
| RS-006 | 包装器 `line-run.sh`（本特性交付的登记→执行→关闭载体） | in-scope | 本特性自身新增的 framework 源脚本 | 不适用（无外部版本面） | `scripts/bash/line-run.sh` | `-h` / `--help`、`--version` 退出 0 且零 registry 写入；登记失败不执行被包装命令；退出码原样传播；SIGKILL 后条目残留 `active` | FR-003, FR-006, FR-007, FR-011 | EP-005 |

**Contract-cell note**: 每个 `Contract` 单元格只放一个仓内可解析路径；`RS-006` 指向本特性的交付面（tasks 阶段创建），不是第二契约。`RS-004` / `RS-005` 的引擎本特性零修改，义务只在其既有契约上被消费与断言。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 可见性闭环可复现——在隔离 registry 下，被包装命令运行期间 digest 列出该 line 且 `state=active`；成功结束显示 `closed`/`completed`，失败结束显示 `closed`/`failed`；SIGKILL 后条目仍为 `active` 且 digest 可见；等价未登记命令运行期间 digest 仍渲染 [[STR-006]]。读数全部取自 digest 与 registry 文件本身，不靠人工转述。 **Path**: final
- **SC-002**: 未登记即变红——`.specify/.tmp/` 下含 [[STR-004]] 且未登记的 fixture 被判违规（退出 1 并给路径），改为经包装器调用后判干净（退出 0）；活仓库声明的可跟踪扫描根读数为 0 违规，根清单与计数写入 `test-evidence/`。删除判据 owner 中的任一成员或在既有可跟踪根注入一个未登记长任务脚本时，读数转红。 **Path**: final
- **SC-003**: registry 单一写入方言——行为测试显示成功/失败两条路径都在 registry 引擎条目上留下 [[STR-007]]、state 与 reason [[STR-008]]；observer journal 路径零新增；静态审计显示 [[STR-001]] 不引用 `journal-utils.py`，且 registry 写入只经 [[STR-002]]。 **Path**: final
- **SC-004**: 接口与失败形态可判定——`-h/--help`、`--version` 退出 0 且 registry 零写入；未声明选项非零拒绝且命令未执行；登记失败时命令未执行；被包装命令退出码原样传播；SIGKILL 模拟后条目仍 `active`。以上均由子进程退出码与 registry 条目断言给出。 **Path**: supporting
- **SC-005**: 长任务登记不再依赖记忆——run-team 的登记/heartbeat/关闭三处步骤、`templates/commands/status.md` 的 registry-only 一句、`templates/instructions-template.md` 的指针行均存在且可按路径定位；删除任一处使契约测试转红（红腿注入）。 **Path**: supporting
- **SC-006**: 分发一致性——`python3 scripts/python/sync-mirrors.py --check` 与 `python3 scripts/python/flow-class-check.py --action check` 退出 0；`python3 scripts/python/doc-consistency-check.py` 若适用则退出 0，若不适用 MUST 记录 `not-evaluated` 与原因，MUST NOT 记成通过。 **Path**: supporting
- **SC-007**: digest 无回归——既有 `tests/contract/test_status_digest*.py` 与 `tests/unit/test_status_digest_unit.py` 全绿；digest 仍不派生进程、动作集与退出码闭集不变，[[STR-006]] 渲染逐字不变。 **Path**: supporting
- **SC-008**: 知识可达——owner § 九 判据、status 命令一句、环境段指针、run-team 三处步骤均可由路径定位；未参与本轮的读者能正确复述「为什么未登记的长任务显示 [[STR-006]]」与「一个批量脚本如何变为可见」；复述失败即不通过。 **Path**: supporting
- **SC-009**: 范围克制——相对特性前基线提交，变更文件集 ⊆ 本规格声明的交付面（包装器、扫描器与其测试、owner 文档、status 命令、instructions 模板、run-team 技能、镜像与文档同步产物、本 spec 目录）；既有未跟踪文件保持未跟踪；无 push。允许的 delta 集合由 plan 声明的交付文件清单给出，plan 之外的新增文件视为违规。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 隔离 `SPECIFY_LINE_REGISTRY_DIR` 的夹具 registry；包装器子进程运行期间/结束后各调一次 `python3 scripts/python/status-digest.py --action digest`，并直接读取条目 JSON；SIGKILL 用 `kill -9` 注入。
- **SC-002 Source**: 扫描器子进程在 fixture 根与活仓库声明根上的退出码与 stdout；fixture 由测试在 `.specify/.tmp/` 下生成并清理；根清单、文件数、命中数写入 `test-evidence/`。
- **SC-003 Source**: 行为测试逐条读取 registry 条目字段与 journal 目录前后计数；静态审计对 [[STR-001]] 做调用面扫描（含镜像树）；判据集合从 A-2 的单一 owner 读取，而非测试硬编码。
- **SC-004 Source**: 子进程退出码矩阵；`--help`/`--version` 前后的 registry 目录快照对比；未声明选项与被包装命令的哨兵文件（执行则出现）断言未执行。
- **SC-005 Source**: 契约测试对四个表面做存在性与引用方向断言（`grep` 级定位 + 红腿注入）；技能与命令文本按路径读取。
- **SC-006 Source**: 三条检查命令的退出码与首条错误抄录；不适用时按 SC 规则记 `not-evaluated`。
- **SC-007 Source**: 既有测试的 pass 计数（经 `scripts/bash/run-tests.sh` 定向运行）与 digest 行为的进程级无写入/无派生断言。
- **SC-008 Source**: 文档路径定位 + 一次复述检查（读者按 `user-facing-comprehension.md` 的全局基准读者定义）。
- **SC-009 Source**: 特性前基线提交（`master` 上本特性分叉点）与实现后的 `git diff --name-only` 集合对比；`git status` 的未跟踪集合对比；`git log` 确认无 push 产物。

## Shared Strings *(recommended: these literals are asserted by tests and consumed by source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"scripts/bash/line-run.sh"` | FR-003, FR-011, FR-014, FR-015, SC-003 |
| `STR-002` | `"line-registry.py"` | FR-004, FR-005, FR-012, FR-014, SC-003 |
| `STR-003` | `"# line-run-required"` | FR-002, FR-014 |
| `STR-004` | `"terraform apply"` | FR-002, FR-015, SC-002 |
| `STR-005` | `"run-tests.sh --full"` | FR-002 |
| `STR-006` | `"nothing-running"` | FR-001, FR-020, SC-001, SC-007, SC-008 |
| `STR-007` | `"line_id"` | FR-017, SC-003 |
| `STR-008` | `"completed"` / `"failed"` | FR-004, SC-003 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!-- Populated by /speckit.clarify. Initial draft carries none; every open choice is adjudicated in Assumptions & Decisions. -->
