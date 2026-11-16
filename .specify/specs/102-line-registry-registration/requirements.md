# Requirements Specification: 长任务 line 登记与 status 可见性（Line Registry Registration）

**Requirement Branch**: `102-line-registry-registration`
**Created**: 2026-11-16
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（编写/修订 `shared/guidelines/**`、`scripts/bash/**`、`scripts/python/**`、`templates/commands/**`、`templates/instructions-template.md`、`skills/internal/**` 与 `.specify/specs/**` 的维护者）与下游项目中运行无人值守长任务、使用 `/speckit.status` 判定「现在到底有没有东西在跑」的维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「为什么一个正在跑的后台批量 apply/verify 或长时间测试在 digest 里显示 `nothing-running`」「哪些任务算长任务、这条判据归谁拥有」「`line-run.sh` 登记什么、失败与 SIGKILL 时留下什么」「registry 的写入方到底是谁」「扫描器判什么、凭什么算有牙、活仓库扫描根为何必须是可跟踪路径」「常驻小节里的提醒为什么只有一句指针」时打开本规格，据 FR-001…FR-023 与 SC-001…SC-009 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "固化「长任务必须登记 line、否则立即变红」的机制边界。/speckit.status 的当前态摘要（digest）只读环境级 Line Registry、从不扫进程，因此任何未登记 line 的长任务（后台批量 apply/verify、长时间测试、无人值守批处理）在 digest 中必然显示 nothing-running——这是「未登记即不可见」的机制缺口，不是漏报。本特性交付：① owner 文档 shared/guidelines/reporting-obligations.md § 九 新增判据（预计超过 5 分钟或含后台批量 apply/verify 的任务 MUST 在启动时登记 line、按阶段 heartbeat、结束时 close；未登记即不进入 digest，nothing-running 是准确结论）；② framework 源新增 scripts/bash/line-run.sh 包装器（register → 执行 → 按结果 close；被 SIGKILL 等无法收尾时保留 active 供 digest 显示；registry 写入方是 line-registry.py，不是 journal-utils.py）；③ 接线：run-team 技能在运行前登记 line、执行中 heartbeat、报告时关闭并记录 line_id；templates/commands/status.md 声明 digest 以 registry 为唯一来源、不得改为扫进程；.specify/instructions.md 增加一条指针式环境提醒（经模板同步落地，不复述判据）；④ 契约与行为测试：脚本接口（-h/--version 退出 0、拒绝未声明选项）、临时 registry 下的成功/失败登记行为、扫描器 fixture 正反例（在 .specify/.tmp/ 下造一个含 terraform apply 且未登记的脚本判红，包上 line-run.sh 后判干净）、活仓库可跟踪扫描根干净。所有对外分发的改动落在 framework 源（scripts/、shared/、templates/、skills/）并经 sync-mirrors 投影，不只手改 .specify/ 运行时。" **输入前提纠正（P4，2026-11-16，以代码为权威）**：`scripts/python/status-digest.py` 除 registry 外还读取 `.specify/state/pid-*`，并对已登记条目的 PID 做 `/proc` / `os.kill` 存活探测（行 888、1265、1304、1330）。因此本规格采用的真实不变量是「line 可见性唯一来源是 registry；存活探测仅限已登记 PID；绝不发现未登记进程」；上文引述的用户原始描述中「只读 registry、从不扫进程」一句按此纠正。

## Related Feature *(mandatory)*

**Feature ID**: 088
**Feature Name**: Speckit 框架可视化（Speckit Framework Visualization）
**Binding basis**: 088 owns `shared/guidelines/reporting-obligations.md` § 九 · 当前态摘要契约（Digest contract）——本特性只向该契约追加一条登记判据并提供载体，属同一 Feature 的后续切片（先例：097 绑定 024、100 绑定 099）。父行状态保持 `Completed` 不回退；102 以 `Draft` 登记为 slice 行，详情指向父 Feature 的 detail 文件。

## Overview

`/speckit.status` 的当前态摘要（digest）的 line 可见性在 087 落地时被固定为**唯一来源是环境级 Line Registry**（`scripts/python/status-digest.py`，owner `shared/guidelines/reporting-obligations.md` § 九）：它会对**已登记条目记录的 PID** 做存活探测（读取 `.specify/state/pid-*`，并用 `/proc` 与 `os.kill` 判断存活），但**绝不发现未登记进程**。这条边界让 digest 具备确定性，也让一条未登记 line 的长任务在摘要里**必然**显示 [[STR-006]]：这不是漏报，而是「未登记即不可见」的机制缺口。长任务目前不登记的原因不是没有载体，而是没有一条判据说「必须登记」，也没有一个让登记**顺手发生**的包装器。

本特性固化一条判据与一个载体，使「长任务不登记 line」在本仓**立即变红**，而不是等 status 与事实不符时才被发现：

1. **判据**落在 owner 文档 `shared/guidelines/reporting-obligations.md` § 九：预计超过 5 分钟、或含后台批量 apply/verify 的运行（含长时间测试与无人值守批处理）MUST 在启动时登记 line、按阶段 heartbeat、结束时 close；未登记即不进 digest，[[STR-006]] 是准确结论而非漏报。判据的**判定边界**由该文件拥有，`/speckit.status` 只按路径引用、不复述。
2. **载体**是 framework 源新增的 [[STR-001]] 包装器：`register → 执行 → 按结果 close`；被 SIGKILL 等无法收尾时**保留 active**，让 digest 显示它。任何批量脚本改成 `line-run.sh --line-id <slug> --run-id <id> -- bash batch.sh` 即自动登记，不再依赖 agent 记得手动调引擎。
3. **接线**覆盖三处：`skills/internal/run-team/SKILL.md` 在运行前登记、执行中 heartbeat、报告时关闭并记录 [[STR-007]]；`templates/commands/status.md` 增一句声明 line 可见性以 registry 为唯一来源、存活探测仅限已登记 PID、绝不发现未登记进程（保持确定性）；`templates/instructions-template.md` 的既有常驻小节 `## Progress Reporting Discipline` 内、`Exemptions and precedence` 之后追加一条**指针式** bullet（一句话 + owner 路径），经模板同步投影到 `.specify/instructions.md` 及其符号链接。
4. **契约与行为测试**证明载体可用且判据有牙：脚本接口、临时 registry 下的成功/失败登记、SIGKILL 残留、扫描器 fixture 正反例、活仓库可跟踪扫描根干净。

**必须纠正的三项前提（不得静默沿用原始方案）**：

- **P1 写入方言**：registry 的唯一写入方是 [[STR-002]]（framework 源 `skills/external/sdd-loop-driver/scripts/line-registry.py`）。`scripts/python/journal-utils.py` 与 registry **零关系**（只写 observer journal），`line-run.sh` 与 run-team 接线都 MUST NOT 经它写 registry。见 FR-005。
- **P2 扫描判据不得是空判**：`.specify/teams/.work/**` 是本仓当前为空的运行期目录，以它作唯一扫描根、以 `terraform apply` 作唯一模式会让测试永远绿。扫描根 MUST 是可跟踪路径，扫描器 MUST 用 fixture 证明有牙。见 FR-012…FR-016。
- **P3 常驻提醒是指针不是副本**：`## Progress Reporting Discipline` 常驻小节里的提醒只给一句话 + owner 路径，不复述判据；落地经 `templates/instructions-template.md` 模板同步（不手改再生成产物）。见 FR-019。

**不做什么**：不引入调度器、定时器服务、常驻进程、第三方依赖、第二份 registry、第二份状态脊或任何台账（`reporting-obligations.md` § 十一 的禁令）；不把 digest 改成发现未登记进程（存活探测仅限已登记 PID）；不新建自动 stale 清理；不改 `status-digest.py` 的动作集、退出码闭集与 [[STR-006]] 渲染；不新建第二条 liveness 通道；不推送远端。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **长任务判据 = 人工阈值 + 机械可判定投影**。人工阈值：预计超过 5 分钟、或含后台批量 apply/verify（含长时间测试、无人值守批处理）。机械投影（扫描器判定的封闭集）：脚本内容含 [[STR-004]]、调用 [[STR-005]]、或头部显式标记 [[STR-003]]。 | 人类判据无法对文件机械判定；扫描器只对可判定的投影负责，两者由同一 owner 声明，扫描器不另立语义。 |
| **A-2** | **机械判据只有一份机器可读 owner**：声明层 fact（候选 `shared/declarations/facts/long-task-criteria.yaml`）或扫描器内常量，二者**择一**由 plan 定稿；其余位置（owner 文档、测试、包装器）只引用，不复述封闭集。→ **已定稿**：取「扫描器内常量」一支，见 A-15。 | One Source Of Truth；brief §4 要求「判据写成单一 owner（常量或声明）」。 |
| **A-3** | **扫描根 = 可跟踪路径**：`scripts/bash/` 必选，`templates/`、`skills/` 由 plan 按信噪比定稿；`.specify/teams/.work/**` 一类运行期目录 MUST NOT 作为唯一扫描根。→ **已定稿**：具体根集合与被判定文件面见 A-21。 | 运行期目录为空且不受跟踪，以它为唯一根等于空判（brief §4 P2）。 |
| **A-4** | **包装器参数形**：[[STR-001]] `--line-id <slug> --run-id <id> -- <command…>`（裸 `--` 与被包装命令均为必填；缺 `--` 或空命令属用法错误）。终止 reason 闭集 = [[STR-008]]（`completed` / `failed`）；条目 state 仍由引擎拥有为 `closed`，本规格不新增状态词。→ **已补齐**：引擎路径规则见 A-17，身份输入与 registry `line_id` 合成规则见 A-18。 | 复用 `line-registry.py` 既有 `register` / `deregister --reason` 语义，不新增状态机。 |
| **A-5** | **失败闭合（fail closed）**：登记失败时包装器 MUST NOT 执行被包装命令并 MUST 非零退出、具名原因；执行后关闭失败 MUST 上浮为非零退出，且不得遮蔽被包装命令的结果。 | 若登记失败仍执行，长任务又回到不可见状态，判据失去牙齿；关闭失败则 digest 仍显示 active，必须让操作者看到。 |
| **A-6** | **常驻小节落点**：`templates/instructions-template.md` 既有 `## Progress Reporting Discipline` 小节内加**一条** bullet（一句话 + `shared/guidelines/reporting-obligations.md` § 九 路径）；`.specify/instructions.md` 由 `/speckit.instructions` 再生成，MUST NOT 手改。→ **精确落点**见 A-22（`Exemptions and precedence` 之后，不新建小节）。 | brief §4 P3；手改 live 文件会在下次再生成时丢失，且破坏符号链接模型的单一来源。 |
| **A-7** | **run-team 接线按现有小节名，不复制简报的旧 PHASE 编号**：在 §1 Load 之后、§6 Orchestrate 之前登记 line；§6 执行期按阶段 heartbeat；§7 Report 关闭并记录 [[STR-007]]。→ **精确落点**见 A-23（§5 顶部登记）。 | brief 写的「PHASE 1 / PHASE 3/4 / Report」与当前技能小节编号（1 Load … 6 Orchestrate、7 Report）不一致；意图明确（开始登记、执行中心跳、报告时关闭），按现有小节名落地方可被维护者定位。 |
| **A-8** | **heartbeat = 经引擎刷新末次事件**（`line-registry.py` 的 `update` 动作，写入带阶段标签的 `last_event`），不新增心跳文件或第二通道；引擎条目已有的 `heartbeat_path` 归既有流程，本特性不改其语义。→ **触发形态与间隔**见 A-19（步骤边界事件，无时间间隔）。 | 复用既有载体，满足 § 十一 零新增机制；「按阶段 heartbeat」需要可判定的落地形态。 |
| **A-9** | **并发与重入归引擎**：同 `line_id` 已存在时，包装器 MUST 让引擎的冲突/拒绝结果上浮并按 A-5 闭合，MUST NOT 静默覆盖或重建条目。嵌套包装器各自登记自己的 line。 | 引擎拥有条目身份与状态；包装器是薄适配层，不另立所有权规则。 |
| **A-10** | **SIGKILL 残留保留、无自动清理**：包装器无法收尾时条目保持 `active`（由 digest 按过期界限标记 stale 并显示时长）；本特性不新增清理守护进程或定时器。→ **过期界限的 owner** 见 A-20（只引用 digest 既有常量）。 | brief §2.2；§ 十一 禁止新守护进程。残留的处置走既有流程。 |
| **A-11** | **组件命名**：包装器 [[STR-001]]（先例 `line-registry.py`）；扫描器名称与路径由 plan 定稿（候选 `scripts/python/line-registration-scan.py`），本规格只固定其可判定行为与退出码，不固定文件名。→ **已定稿**：路径本阶段固定，见 A-16 与 [[STR-009]]。 | 名称遵循 Grounded Naming 的项目约定；命令/脚本路径按 `templates/commands/status.md` 的先例由 plan 阶段固定。 |
| **A-12** | **Feature 绑定留待 `/speckit.clarify`**：`Related Feature` 保持默认 `Need clarification`。→ **已完成**：绑定 Feature 088（slice 行 102），见 A-14 与 `Related Feature`。 | `create-requirements` 技能的绑定时机约定：本阶段不查表、不建 Feature。 |
| **A-13** | **「长任务」以调用方生命周期计**：被包装命令若自身立即返回、把工作交给后台而调用方已结束，则包装器正常 close，该后台工作不在本判据范围内（需要可见性的后台工作应自行经包装器或引擎登记）。 | 包装器能观察到的生命周期只有被包装命令的进程；把不可观察的后台生命周期纳入会让判据不可判定。 |
| **A-14** | **Feature 绑定 = 088（slice 行 102）**：`Feature ID 088` / `Feature Name Speckit 框架可视化（Speckit Framework Visualization）`；102 以 `Draft` 登记，详情指向父 Feature 的 detail 文件，父行状态不回退。 | 088 owns `reporting-obligations.md` § 九（本特性唯一扩展的契约），符合「匹配即绑定」；097/100 提供 slice 行先例。 |
| **A-15** | **机械判据的机器可读 owner = 扫描器模块内常量**（长任务标记集、自声明标记、合规形态、默认扫描根各一个模块级常量）；测试以 `import` 读取，owner 文档只按路径引用、不复述成员。扫描器按解析路径跳过**自身文件**（owner 是判据的声明者而非执行者），并在读数中具名 `owner-skipped`，MUST NOT 把它计入干净命中。否决的替代：声明层 fact——它会新增 fact 注册并突破 FR-022 的「新增物仅限…」与 SC-009 的封闭 delta；若未来第二个引擎也要消费该判据，重开此抉择。 | One Source Of Truth（代码优先）+ 最小交付面；自跳过是具名豁免，不是隐藏。 |
| **A-16** | **扫描器路径本阶段固定**为 [[STR-009]] `scripts/python/line-registration-scan.py`，镜像到 `.specify/scripts/python/`；接口：只读、`--root <path>` 可重复、缺省用 A-21 的默认根、退出码 0/1/2。不新增 fixture 辅助脚本——fixture 由测试在 A-21 的临时根内生成并清理。 | FR-015/SC-002 的测试必须点名可执行路径；留给 plan 会让测试硬编码一个猜测。 |
| **A-17** | **引擎路径唯一规则（有序候选，首个可读者胜）**：(1) `<repo-root>/skills/external/sdd-loop-driver/scripts/line-registry.py`；(2) `<repo-root>/.specify/skills/sdd-loop-driver/scripts/line-registry.py`。`<repo-root>` 由包装器自身路径解析（`scripts/bash/` 或 `.specify/scripts/bash/` 的上两级；若该级目录名为 `.specify` 再上移一级，与 `status-digest.py` 的守卫同形）。两者都不可读 → 登记失败（A-5）：不执行被包装命令、非零退出并具名两个候选路径。MUST NOT 使用 `.specify/scripts/line-registry.py`（未跟踪本机副本）、MUST NOT 经 `PATH` 查找、不新增引擎路径环境变量。 | 与 digest 的引擎解析同向（framework 源优先），且两顶帽子各有一支；客户端项目只存在候选 (2)。 |
| **A-18** | **身份输入与 registry `line_id`**：包装器用 `git rev-parse --show-toplevel` 取绝对 repo root，同时作为引擎的 `--project-dir` 与 `--repo-root`（不得用 `$PWD`；digest 按这两个字段匹配工作区）；非 git 仓库 → 登记失败（A-5）。registry 条目 id 由包装器合成为 `<--line-id>-<--run-id>`（例：`batch-apply-r20261116T090000Z-a001`），使同一 slug 的每次运行天然唯一；该 id 已存在（同一 run 重试）→ 引擎的 `line already exists` 上浮并按 A-5 闭合，MUST NOT 覆盖或删除既有条目。包装器 MUST NOT 放松引擎的 `line_id` / `run_id` 正则，不合规即登记失败、命令不执行。run-team 的 run-id 生成规则：形如 `r<UTC 日期 yyyymmdd>T<UTC 时间 hhmmss>Z-<4 位小写十六进制>`（例 `r20261116T090000Z-a001`），MUST 匹配引擎 `RUN_ID_RE`；run-team 现有的裸 UTC 时间戳 MUST NOT 作为 run-id。测试与运行报告记录的是合成 id（[[STR-007]] 的值）。 | 引擎的 `closed` 是终态且条目文件不删除（`update` 的 `a new attempt requires a new line`），固定 id 会让第二次运行永远失败；合成 id 保住「同一命令形状反复运行」的人机接口。 |
| **A-19** | **heartbeat 形态 = 步骤边界事件，无时间间隔**：包装器只产生两个引擎事件——register（`registered`）与关闭（`completed` / `failed`）；它观察不到被包装命令的内部阶段，故不刷新中间事件（A-13）。run-team 在 §6 的每个编排步骤边界调一次 `update --last-event <step-label>`（标签取技能小节名/阶段名）。不存在定时器、守护进程、心跳文件或第二通道；时间上的「过期」只由 digest 的既有 stale 界判定（A-20）。 | 「按阶段 heartbeat」是可判定的事件序列而非时钟；§ 十一 禁止新守护进程。 |
| **A-20** | **SIGKILL 残留的过期界限只引用既有 owner**：残留 `active` 条目由 digest 依 `scripts/python/status-digest.py` 的 `DEFAULT_STALE_BOUND_SECONDS`（可经 `--stale-bound` 覆盖）标记 stale 并显示时长；本特性不新增阈值、不做自动清理、不删除条目。残留处置走既有流程（既有 `deregister --reason stale-cleanup` 等动作由操作者或既有流程调用）。 | FR-020 要求 digest 闭集不变；§ 十一 禁止清理守护进程；阈值保持单 owner。 |
| **A-21** | **活仓库扫描根 = `scripts/bash/`、`scripts/python/`、`skills/`**（递归；`templates/` 无可执行脚本，不列入）。**被判定文件面 = 常规文件且满足其一：`.sh` / `.bash` / `.py` 扩展名，或首行 shebang**；符号链接一律跳过（不跟随），永不越出 repo root。缺失的默认根 → 退出 2 并具名该根，MUST NOT 把缺失或空目录渲染成干净。**显式 `--root` 与缺省根适用同一存在性判据**：必须存在为目录；缺失、非目录、仓外或存在但零个被判定文件 → 退出 2 并具名该根，MUST NOT 渲染成干净，且不回退到缺省根；运行期目录只禁止作为**缺省**根，作为显式 `--root` 时按同一判据判定。fixture 根 = `.specify/.tmp/line-registry-registration/`（已被 `.specify/.gitignore` 的 `.tmp/` 覆盖），由测试生成并清理。 | 排除 `tests/` 与散文文档后，`skills/` 内 [[STR-005]] 的既有命中（`references/*.md`）不再是脚本，活仓库读数可为零；根清单与文件面同属 A-15 的常量 owner。 |
| **A-22** | **常驻小节落点 = 在 `## Progress Reporting Discipline` 内 `Exemptions and precedence` bullet 之后追加一条**；不新建小节、不改其它 bullet。`templates/instructions-template.md` 是唯一编辑面，`.specify/instructions.md` 及 `AGENTS.md` / `CLAUDE.md` / `QODER.md` / `.github/copilot-instructions.md` 符号链接经再生成获得该句。 | 「环境段」是标签而非锚点——模板中不存在以它为名的段落；按字面锚点落地才可被维护者定位并被契约测试断言。 |
| **A-23** | **run-team 落点（按现有小节名）**：登记放在 **§5 Present & Execute 顶部**（§2 五查若 `blocked` 则不留下悬空 line）；§6 Orchestrate 的每个编排步骤边界 heartbeat（A-19）；§7 Report 在写报告前关闭并把合成 `line_id` 写进报告正文。不修改 `create-team` 的 Report 契约文件——报告字段义务由 run-team §7 自身承载。 | A-7 的意图不变（开始登记、执行中心跳、报告关闭），落点避开 blocked 分支；报告契约 owner 不在本特性交付面。 |
| **A-24** | **双失败退出优先级**：被包装命令非零时，包装器以该命令的退出码退出，并把关闭失败（引擎 payload + 退出码）写到 stderr；被包装命令为 0 而关闭失败时，包装器以引擎的失败退出码退出。任何一方的结果都 MUST NOT 被静默吞掉或改写。 | SC-004 的「退出码原样传播」在正常路径成立；关闭失败必须在数字或文本通道上可见；两者同时失败时数字通道保留命令的真实结果。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 后台批量脚本经包装器自动登记，运行期在 digest 里可见 (Priority: P1)

维护者有一个预计要跑十几分钟的批量 apply/verify 脚本。她不再需要记得先手动调 registry 引擎，而是把调用改成 [[STR-001]] `--line-id batch-apply --run-id <id> -- bash batch.sh`。包装器在命令启动前把 line 登记为 `active`，运行期间 digest 能列出这条 line 及其最近活动；命令成功结束以 `completed` 关闭，失败以 [[STR-008]] 中的 `failed` 关闭；若包装器被 SIGKILL，条目保持 `active`，digest 仍显示它（并按过期界限标记 stale 与时长）。

**Why this priority**: 这是用户诉求的第一句——长任务不登记是根本问题；包装器让登记顺手发生，否则判据只是又一条靠记忆执行的义务。

**Independent Test**: 在隔离的 `$SPECIFY_LINE_REGISTRY_DIR` 下运行包装器包住一个短命令（须保持运行到采样完成，例如 `bash -c 'sleep 2'`；瞬时命令 `true` 不足以采样）：运行期间以 `--workspace <repo-root>` 读一次 digest，断言条目出现且 `state=active`；结束后读 registry 条目文件，断言 `state=closed` 且 reason 按结果取值（digest 按既有规则不列 `closed` 条目；若它是唯一 line，digest 渲染 [[STR-006]]——这是既有行为，不是本特性的断言面）；再模拟 SIGKILL，断言条目残留 `active` 且 digest 列出它。

**Acceptance Scenarios**:

1. **Given** 隔离 registry 与一个成功的被包装命令，**When** 运行 `line-run.sh --line-id demo-batch --run-id r20261116T090000Z-a001 -- bash -c 'sleep 2'`，**Then** registry 中出现 `line_id=demo-batch-r20261116T090000Z-a001` 的条目（A-18），运行期间（采样完成前命令保持运行）其 `state` 为 `active`，结束后 `state` 为 `closed` 且 reason 为 `completed`，包装器退出 0。
2. **Given** 同一隔离 registry 与一个失败命令，**When** 运行 `line-run.sh --line-id demo-fail --run-id r20261116T090000Z-a002 -- false`，**Then** 包装器以被包装命令的非零退出码退出，条目 `state` 为 `closed` 且 reason 为 `failed`。
3. **Given** 一个运行中的包装器被 SIGKILL，**When** 读取 registry 与 digest，**Then** 条目仍为 `active`（不被删除、不被标 closed），digest 列出它并显示其最近活动时长。
4. **Given** registry 目录不可写，**When** 运行包装器，**Then** 被包装命令**未被执行**，包装器非零退出并具名报告登记失败。

---

### User Story 2 - 未登记的长任务在本仓立即变红，而不是永远绿 (Priority: P1)

维护者想知道「本仓有没有长任务脚本绕过了登记」。她运行确定性扫描器：它以声明的可跟踪扫描根为单位，对每个命中长任务机械判据（[[STR-004]] / [[STR-005]] / [[STR-003]]）却既未经包装器调用、也未直接调 registry 引擎登记的文件报违规并给出路径；干净时退出 0，有违规时退出 1。扫描器用 fixture 证明有牙：临时造一个含 [[STR-004]] 且未登记的脚本判红，包上包装器后判干净；对活仓库的声明扫描根，读数为 0 违规。

**Why this priority**: 与 US1 同等重要——没有扫描器，判据只是文档措辞；而用空的运行期目录或单一模式做扫描根会让测试永远绿，等于没有判据。

**Independent Test**: 在 `.specify/.tmp/line-registry-registration/` 下生成正例与反例脚本，分别调用扫描器；再对活仓库扫描根运行一次，断言三组退出码与输出。

**Acceptance Scenarios**:

1. **Given** `.specify/.tmp/line-registry-registration/` 下一个含 [[STR-004]]、未经包装器调用、也未调 registry 引擎的临时脚本，**When** 以该目录为扫描根运行扫描器，**Then** 退出 1，输出给出该文件路径与被命中的判据。
2. **Given** 同一临时脚本改为经 [[STR-001]] 调用（或直接调用 `line-registry.py` 的 register/update/deregister），**When** 再次扫描，**Then** 退出 0，输出零违规。
3. **Given** 活仓库与声明的可跟踪扫描根（A-21：`scripts/bash/`、`scripts/python/`、`skills/`；脚本文件面），**When** 运行扫描器，**Then** 退出 0，零违规；读数（扫描根清单、扫描文件数、命中数与 `owner-skipped` 计数）写入 `test-evidence/`。
4. **Given** 显式 `--root` 指向一个存在但零个被判定文件的运行期目录（如 `.specify/teams/.work/`），**When** 运行扫描器，**Then** 退出 2 并在输出中具名该根（空根属输入错误，MUST NOT 被渲染成干净读数），且不回退到缺省根清单——显式 `--root` 替换而非并入缺省根，故该读数既不复述缺省根，也不构成「缺省根干净」的证据（FR-012, FR-013, A-21）。

---

### User Story 3 - 判据有唯一 owner，下游表面只给指针 (Priority: P2)

维护者要回答「这条判据是谁定的、改一次要改几个文件」。答案必须是：owner 文档 `shared/guidelines/reporting-obligations.md` § 九 拥有判据与判定边界；机械投影的常量 owner 在扫描器模块内（A-15）；`templates/commands/status.md` 只声明 line 可见性以 registry 为唯一来源、存活探测仅限已登记 PID、绝不发现未登记进程；常驻小节（`templates/instructions-template.md` 的 `## Progress Reporting Discipline` 投影到 `.specify/instructions.md` 与其符号链接）只有一句指针提醒；技能与测试只按路径引用。删掉任一表面或把 owner 的判据复述进下游，契约测试转红。

**Why this priority**: 判据一旦在多处复述就会漂移；而常驻小节是让每个会话第一眼就看到提醒的唯一位置，必须是指针而不是副本。

**Independent Test**: 检查四个表面的文本与引用方向；注入一次「删掉常驻提醒」与一次「在 status.md 里复述判据」的篡改，断言契约测试各自转红。

**Acceptance Scenarios**:

1. **Given** 本特性落地后的仓库，**When** 阅读 `shared/guidelines/reporting-obligations.md` § 九，**Then** 判据（>5 分钟 / 后台批量 apply/verify、启动登记、阶段 heartbeat、结束 close、未登记即 [[STR-006]]）与判定边界在此，且是唯一详细定义点。
2. **Given** `templates/commands/status.md`，**When** 阅读它，**Then** 它含一句「line 可见性以 registry 为唯一来源、存活探测仅限已登记 PID、绝不发现未登记进程」，且未复述 § 九 的判据条目或增加渲染逻辑。
3. **Given** `templates/instructions-template.md` 的 `## Progress Reporting Discipline`，**When** 阅读它，**Then** 在 `Exemptions and precedence` bullet 之后含**一条**一句话指针 + owner 路径（不新建小节，A-22），且 `.specify/instructions.md` 中该句与模板投影一致（经再生成，不是手改）。

---

### User Story 4 - 无人值守团队运行与 status 接线不再依赖记忆 (Priority: P2)

自动化执行者运行一个团队（`run-team`）。在真正开始编排前，它先登记 line；编排过程中按阶段刷新末次事件；运行报告写入时关闭 line 并把 [[STR-007]] 写进运行报告。于是 digest 在整个团队运行期间都能回答「在跑什么」，运行报告也能把「这次运行对应哪条 line」交给后续审计。

**Why this priority**: 无人值守正是最容易「长时间没东西可见」的场景；把登记写进技能步骤，才让义务随执行体一起被携带。

**Independent Test**: 检查技能文本的三处步骤与 §7 对报告字段的义务；用契约测试断言三处步骤存在、[[STR-007]] 在 §7 被要求写入报告正文、删除任一处即红。不修改 `create-team` 的 Report 契约文件（A-23）。

**Acceptance Scenarios**:

1. **Given** `skills/internal/run-team/SKILL.md`，**When** 阅读 Workflow，**Then** 它在 §5 顶部登记 line、在 §6 执行期按阶段 heartbeat、在 §7 Report 关闭 line，三处都以引擎路径引用、不复述引擎参数表（A-23）。
2. **Given** 一次按技能执行的运行，**When** 阅读其运行报告，**Then** 报告正文携带该次运行的 [[STR-007]]（合成 id），且该值可在 registry 中解析到对应条目。
3. **Given** 运行期间的 digest，**When** 读取它，**Then** 团队运行对应的 line 被列出（不再显示 [[STR-006]]）。

---

### Edge Cases

- **被包装命令自己派生后台工作后立即返回**：包装器按调用方生命周期正常关闭；该后台工作若也需要可见性，须自行经包装器或引擎登记（A-13）。判据不声称覆盖不可观察的进程。
- **同一 `line_id` 并发/重复登记**：包装器把引擎的拒绝或冲突结果上浮并非零退出，不覆盖既有条目（A-9）。
- **同一 slug 的第二次运行**：registry id 由 `<line-id>-<run-id>` 合成，每次运行天然唯一；同一 run-id 重试等价于重复登记，按引擎 `line already exists` 失败闭合，不覆盖、不删除既有条目（A-18）。
- **registry 根被 `$SPECIFY_LINE_REGISTRY_DIR` 指向不存在或不可写的目录**：登记失败即不执行（A-5）；错误信息点名该路径。
- **包装器自身被 SIGKILL / 宿主机掉电**：条目保持 `active`；digest 按过期界限将其标记 stale 并显示时长（A-10），不自动删除。
- **被包装命令以信号终止**：非零退出按 `failed` 关闭；若包装器自身无法捕获而退出，条目残留 `active`。
- **扫描器的误报**：判据是内容匹配，注释里出现 [[STR-004]] 也会命中。合规途径只有一条：文件含合规调用（经包装器调用，或直接调引擎 register/update/deregister）；头部标记 [[STR-003]] 只宣布「我是长任务」，不构成豁免；扫描根刻意不含 `tests/` 等夹具目录，且只判定脚本文件面（扩展名或 shebang），避免把测试样本与散文文档判成产线违规（A-1/A-21）。
- **扫描器扫到自身**：判据常量所在文件是声明的 owner、不是长任务执行者，按解析路径跳过并在读数中具名 `owner-skipped`；该计数 MUST NOT 被计入「干净」证据（A-15）。
- **显式 `--root` 指向缺失 / 非目录 / 仓外 / 存在但零个被判定文件的目录**：一律输入错误——退出 2 并具名该根，不渲染成干净读数，也不回退到缺省根清单（FR-012 / FR-013 / A-21）；显式 fixture 根只要存在且含至少一个被判定文件即按 A-21 正常判定。
- **`run-tests.sh` 自身提供 `--full` 路径**：它不得仅因「支持 `--full`」被判违规；只有调用方脚本（或显式头标记）进入长任务集合（A-1）。
- **常驻提醒再生成**：手改 `.specify/instructions.md` 会在 `/speckit.instructions` 再生成时丢失；改动只落模板（A-6/A-22）。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 系统 MUST 在 owner 文档 `shared/guidelines/reporting-obligations.md` § 九（当前态摘要契约）新增长任务判据：预计超过 5 分钟、或含后台批量 apply/verify 的运行（含长时间测试、无人值守批处理）MUST 在启动时登记 line、按阶段 heartbeat、结束时 close；未登记的运行不进入 digest，[[STR-006]] 是准确结论而非漏报。阈值判定者为运行者，在启动时按预期时长判断（A-1 的人工阈值；机械可判定投影见 FR-002）。判定边界由该文件拥有；§ 九 同时声明 digest 的真实不变量：line 可见性唯一来源是 registry；存活探测仅限已登记 PID；绝不发现未登记进程。
- **FR-002**: 长任务判据的**机械可判定投影**（脚本内容含 [[STR-004]]、调用 [[STR-005]]、或头部标记 [[STR-003]]）MUST 恰好有一个机器可读 owner：扫描器模块内的判据常量（A-15）；扫描器、测试与文档 MUST 引用它（测试以 `import` 读取），MUST NOT 各自复述该封闭集。扫描器 MUST 按解析路径跳过该 owner 文件本身，并在读数中具名 `owner-skipped`。
- **FR-003**: framework 源 MUST 新增包装器 [[STR-001]]，并经 `scripts/python/sync-mirrors.py` 投影到 `.specify/scripts/bash/`；镜像 MUST NOT 手改。
- **FR-004**: 包装器 MUST 在被包装命令启动前，经 registry 引擎 [[STR-002]] 把 line 登记为 `active`（引擎按 A-17 的有序候选解析；`--project-dir` / `--repo-root` 与 registry `line_id` 按 A-18 派生/合成）；执行 `--` 之后的命令；按结果关闭：退出 0 → reason `completed`，非零 → reason `failed`。终止 reason 取值域见 [[STR-008]]。
- **FR-005**: 包装器与 run-team 接线对 registry 的写入 MUST 只经 [[STR-002]]；MUST NOT 使用 `scripts/python/journal-utils.py` 写 registry，MUST NOT 把 journal 与 registry 混用为同一存储。
- **FR-006**: 登记失败时，包装器 MUST NOT 执行被包装命令，MUST 以非零退出并具名报告失败原因（fail closed，A-5）。
- **FR-007**: 包装器 MUST 原样传播被包装命令的退出状态；执行后关闭失败 MUST 上浮为非零退出，并同时指名命令结果与 registry 失败，MUST NOT 遮蔽或改写任一方。双失败时的退出码优先级按 A-24：命令非零 → 命令退出码 + stderr 关闭失败；命令为 0 且关闭失败 → 引擎的失败退出码。
- **FR-008**: 包装器被 SIGKILL 等无法收尾时，其 line 条目 MUST 保持 `active`（不被删除、不被改写为 `closed`），使 digest 可见（A-10）。
- **FR-009**: 包装器 MUST 在运行开始与结束时经引擎写入该 line 的两个事件（register 与关闭），且 MUST NOT 写中间事件（A-19：包装器观察不到被包装命令的内部阶段）；按阶段 heartbeat 由 run-team 在编排步骤边界承担（FR-017），不存在时间间隔。MUST NOT 新增心跳文件或第二 liveness 通道。
- **FR-010**: 包装器 MUST 遵守既有的 registry 目录解析顺序（`$SPECIFY_LINE_REGISTRY_DIR` → `$XDG_STATE_HOME/spec-kit/lines` → `~/.local/state/spec-kit/lines`），使测试可用环境变量隔离；MUST NOT 引入新的 registry 根覆盖变量。
- **FR-011**: [[STR-001]] MUST 满足 Script Interface Contract：`-h` / `--help` 与 `--version` 回答后退出 0 且零 registry 写入；未声明选项 MUST 被非零拒绝且不执行被包装命令；MUST NOT 联网、MUST NOT push。
- **FR-012**: 系统 MUST 提供确定性、只读的扫描器 [[STR-009]]（`scripts/python/line-registration-scan.py`）：扫描声明的可跟踪根，对每个命中长任务机械判据（FR-002）却未经包装器调用、也未直接调用 [[STR-002]] 的 register/update/deregister 的文件报违规，输出文件路径与命中的判据；干净退出 0、有违规退出 1、输入错误退出 2；MUST 支持 `--root <path>`（可重复）**替换（而非并入）** A-21 的缺省根清单以服务 fixture，每个显式根 MUST 存在为目录（缺失、非目录、仓外或存在但零个被判定文件 → 退出 2 并具名该根，FR-013）；运行期目录的禁令只针对**缺省**根，显式 fixture 根按 A-21 正常判定；MUST NOT 写入、派生进程或联网。
- **FR-013**: 扫描器 [[STR-009]] 的活仓库扫描根 MUST 是可跟踪路径，且固定为 `scripts/bash/`、`scripts/python/`、`skills/`（`templates/` 无可执行脚本不列入）；被判定文件面 = 常规文件且满足 `.sh` / `.bash` / `.py` 扩展名或首行 shebang，符号链接一律跳过（A-21）；运行期目录（如 `.specify/teams/.work/**`）MUST NOT 作为**缺省**扫描根；缺失根与空根（存在但零个被判定文件）MUST 按输入错误退出 2 并具名该根，MUST NOT 被渲染成干净证据——该判据对缺省根与显式 `--root` 一致适用，空根不回退到缺省根（A-3, A-21）。
- **FR-014**: 扫描器 MUST 认可以下两类合规形态：文件经 [[STR-001]] 调用；或文件直接调用 [[STR-002]] 的 register/update/deregister。头部标记 [[STR-003]] 是**命中判据**而非合规豁免：本身构成长任务、但内容不含其它判据成员的脚本用它声明自己，声明后仍须具备合规调用才判干净；仅提供长任务路径的脚本（如 `run-tests.sh` 的 `--full` 选项）不因「提供该路径」被判违规——判据按内容字面匹配。
- **FR-015**: 测试 MUST 在 `.specify/.tmp/line-registry-registration/`（A-21 的 fixture 根，已被 `.gitignore` 覆盖）下生成含 [[STR-004]]、未登记的临时脚本，断言扫描器 [[STR-009]] 报违规；再把同一脚本改为经 [[STR-001]] 调用，断言扫描器判干净；另对同一根内一个带头部标记 [[STR-003]] 且无合规调用的脚本断言判违规（自声明不豁免）（fixture 有牙，正反与自声明三例都断言；测试结束清理该根）。
- **FR-016**: 对活仓库声明的扫描根，扫描器 MUST 给出零违规读数，且该读数（根清单、扫描文件数、命中数、`owner-skipped`）MUST 由测试经唯一入口运行时记录到 `test-evidence/`（扫描器自身保持只读、不写任何文件）；读数 MUST NOT 以暂定数字冒充实测。
- **FR-017**: `skills/internal/run-team/SKILL.md` MUST 在运行开始前登记 line、在执行期按阶段 heartbeat、在 Report 步骤关闭 line 并把 [[STR-007]] 写入运行报告（落点按 A-7 的现有小节名）；三处 MUST 以路径引用引擎，MUST NOT 复述引擎参数表。
- **FR-018**: `templates/commands/status.md` MUST 增一句声明：line 可见性以 Line Registry 为唯一来源——存活探测仅限已登记 PID，MUST NOT 改为发现未登记进程（保持确定性）；该句 MUST NOT 复述 § 九 的判据条目，MUST NOT 增加渲染逻辑。
- **FR-019**: `templates/instructions-template.md` 的 `## Progress Reporting Discipline` 常驻小节内、`Exemptions and precedence` bullet 之后 MUST 增一条**指针式**提醒（一句话 + owner 路径），不新建小节、不改其它 bullet（A-22）；`.specify/instructions.md` 及其符号链接 MUST 经再生成获得该句，MUST NOT 手改（A-6）。
- **FR-020**: `/speckit.status` 的 digest MUST 保持 line 可见性唯一来源为 registry、存活探测仅限已登记 PID、绝不发现未登记进程，零进程派生、动作集与退出码闭集不变，[[STR-006]] 的显式渲染不变；本特性 MUST NOT 引入第二个 parser 或第二个 renderer。
- **FR-021**: 测试 MUST 经唯一入口 `scripts/bash/run-tests.sh` 运行（缺省并行形态，路径与参数原样转交），并按 `contract` / `integration` 标记归档；执行记录（命令、退出码、完整输出、耗时）MUST 留证。包装器五形态（成功 / 命令失败 / 登记失败 / 双失败 / SIGKILL 残留）与扫描器 fixture 正反例、自声明例、活仓库读数 MUST 各有自动测试覆盖。
- **FR-022**: 本特性 MUST NOT 引入调度器、定时器服务、常驻进程、第三方依赖、第二份 registry、第二份状态脊或台账（`reporting-obligations.md` § 十一 禁令）；新增物仅限包装器、扫描器、测试与文本接线。
- **FR-023**: 变更 MUST 只提交本特性产物；既有未跟踪文件（`.specify/scripts/line-registry.py`、`.specify/scripts/stage-runner.sh`）MUST NOT 被提交或还原；MUST NOT 推送远端。

### Key Entities *(include if required)*

- **Line（登记的工作单元）**：`line_id`、`run_id`、`state`（取值域归 `line-registry.py`）、`last_event`、`updated_at`，以及既有引擎字段（`driver_session`、`claimed_ns` 等）；由引擎拥有身份与状态。
- **Registry 条目**：环境级 registry 目录下每线一个 `<line_id>.json`；line 可见性的唯一读取源。
- **长任务脚本**：落在声明扫描根内、命中长任务机械判据的文件；合规形态只有两类——经包装器调用，或直接调引擎登记；头部标记 [[STR-003]] 是**命中判据**（宣布「我是长任务」），不构成合规豁免。
- **包装器调用**：一次 `line-run.sh --line-id … --run-id … -- <command…>` 运行；产生登记 → 执行 → 关闭三事件，失败与 SIGKILL 各留下可判定的残留形态。
- **Digest 读数**：`/speckit.status` 对 registry 的只读投影（line 可见性），并在已登记条目记录的 PID 上叠加存活探测；[[STR-006]] 是空集合的显式渲染。

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖、不新增第三方包——它交付一个 bash 包装器与一个只读扫描器，并消费既有的 Python 解释器、pytest 运行器、既有 line-registry 引擎与既有 status-digest 引擎。每行可机械判定，零散文声明。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段不建 premises 表）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库（扫描器的目录遍历与文本判定、测试夹具生成与 registry 条目读取） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 既有 `requires-python` 下限；本特性零新增第三方依赖 | `pyproject.toml` | 扫描器与新增测试在 `>=3.8` 解释器上经唯一入口 `scripts/bash/run-tests.sh` 通过；本特性新增第三方 import 为零 | FR-012, FR-013, FR-014, FR-015, FR-016 | EP-001, EP-002 |
| RS-002 | POSIX `bash` 运行时（包装器本体及其对被包装命令的子进程调用） | signed-contract | bash 上游 / 运行环境（本仓只消费） | 不新增显式版本下限；包装器须在 bash 3.2（macOS 系统 bash）及以上可用；pin 由 `bash --version` 在 test-evidence 的首次采集记录提供 | `scripts/bash/common.sh` | 包装器在 `bash scripts/bash/line-run.sh` 下完成登记→执行→关闭全程；`-h` / `--version` 退出 0 且零 registry 写入 | FR-003, FR-021 | EP-005 |
| RS-003 | `pytest` 测试运行器（契约测试、行为测试与扫描器 fixture 正反例） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有 pytest 声明；本特性零新增依赖 | `pyproject.toml` | `scripts/bash/run-tests.sh` 运行新增 `contract` / `integration` 测试，结果集相对 implement 入口基线零新增红 | FR-015, FR-016, FR-021 | EP-002 |
| RS-004 | 既有 line-registry 引擎的写入面（`register` / `update` / `deregister`） | signed-contract | 既有 sdd-loop-driver 引擎（本特性只消费，不修改其动作集与状态词） | 仓内既有实现，无外部版本面；pin 由 `--help` 声明的动作集与退出码闭集固定 | `skills/external/sdd-loop-driver/scripts/line-registry.py` | 隔离 `$SPECIFY_LINE_REGISTRY_DIR` 下成功/失败/SIGKILL 三形态在引擎条目上留下 [[STR-007]]、`state` 与 reason；包装器不引用 `journal-utils.py` | FR-004, FR-005, FR-008, FR-009, FR-010 | EP-003 |
| RS-005 | 既有 status-digest 引擎（digest 当前态读数的唯一来源） | signed-contract | 既有 `/speckit.status` 摘要引擎（本特性只读消费，不修改动作集与退出码闭集） | 仓内既有实现，无外部版本面；pin 由 FR-020 的闭集不变断言固定 | `scripts/python/status-digest.py` | 隔离 registry 上运行期间与结束后各读一次 digest，读数与 registry 条目一致；本特性对其零修改 | FR-001, FR-020 | EP-004 |
| RS-006 | 包装器 `line-run.sh`（本特性交付的登记→执行→关闭载体） | in-scope | 本特性自身新增的 framework 源脚本 | 不适用（无外部版本面） | `scripts/bash/line-run.sh` | `-h` / `--help`、`--version` 退出 0 且零 registry 写入；登记失败不执行被包装命令；退出码原样传播；SIGKILL 后条目残留 `active` | FR-003, FR-006, FR-007, FR-011 | EP-005 |

**Contract-cell note**: 每个 `Contract` 单元格只放一个仓内可解析路径；`RS-006` 指向本特性的交付面（tasks 阶段创建），不是第二契约。`RS-004` / `RS-005` 的引擎本特性零修改，义务只在其既有契约上被消费与断言。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 可见性闭环可复现——在隔离 registry 下，被包装命令运行期间 digest 列出该 line 且 `state=active`；结束后 registry 条目为 `closed` 且 reason 为 `completed` / `failed`（digest 按既有规则不列 `closed` 条目；若它是唯一 line，digest 渲染 [[STR-006]]，属既有行为）；SIGKILL 后条目仍为 `active` 且 digest 可见；等价未登记命令运行期间 digest 仍渲染 [[STR-006]]。读数全部取自 digest（`--workspace <repo-root>`）、registry 文件与包装器退出码本身，不靠人工转述。 **Path**: final
- **SC-002**: 未登记即变红——扫描器 [[STR-009]] 对 `.specify/.tmp/line-registry-registration/` 下含 [[STR-004]] 且未登记的 fixture 判违规（退出 1 并给路径），改为经包装器调用后判干净（退出 0）；活仓库声明的可跟踪扫描根（`scripts/bash/`、`scripts/python/`、`skills/`，脚本文件面）读数为 0 违规，根清单、文件数、命中数与 `owner-skipped` 计数写入 `test-evidence/`。删除 `COMPLIANT_INVOCATIONS` 的任一成员、或使自声明不再被识别时，fixture 正反两腿与自声明腿必须转红；在既有可跟踪根注入一个未登记长任务脚本时，读数转红；缺失的默认根必须报输入错误而不是干净。 **Path**: final
- **SC-003**: registry 单一写入方言——行为测试显示成功/失败两条路径都在 registry 引擎条目上留下 [[STR-007]]、state 与 reason [[STR-008]]；observer journal 路径零新增；静态审计显示 [[STR-001]] 不引用 `journal-utils.py`，且 registry 写入只经 [[STR-002]]。 **Path**: final
- **SC-004**: 接口与失败形态可判定——`-h/--help`、`--version` 退出 0 且 registry 零写入；未声明选项非零拒绝且命令未执行；登记失败时命令未执行；被包装命令退出码在正常路径原样传播；双失败时按 A-24 的优先级退出且双方结果都可读到；SIGKILL 模拟后条目仍 `active`。以上均由子进程退出码、stderr 文本与 registry 条目断言给出。 **Path**: supporting
- **SC-005**: 长任务登记不再依赖记忆——run-team 的登记/heartbeat/关闭三处步骤、`templates/commands/status.md` 的 `Single source` 一句（line 可见性以 registry 为唯一来源、存活探测仅限已登记 PID、绝不发现未登记进程）、`templates/instructions-template.md` 的指针行均存在且可按路径定位；删除任一处使契约测试转红（红腿注入）。 **Path**: supporting
- **SC-006**: 分发一致性——`python3 scripts/python/sync-mirrors.py --check` 相对特性前基线**无新增漂移**（基线为 5 条 `DIFF` + 2 条 `ORPHAN`，读数逐字记录；本特性改动的四对镜像行为 `ok`），`python3 scripts/python/flow-class-check.py --action check` 退出 0；`python3 scripts/python/doc-consistency-check.py` 由实现者判定是否适用（判定依据写进读数），适用则退出 0，不适用 MUST 记录 `not-evaluated` 与原因，MUST NOT 记成通过。 **Path**: supporting
- **SC-007**: digest 无回归——既有 `tests/contract/test_status_digest*.py` 与 `tests/unit/test_status_digest_unit.py` 全绿；digest 仍不派生进程、存活探测仅限已登记 PID、绝不发现未登记进程、动作集与退出码闭集不变，[[STR-006]] 渲染逐字不变。 **Path**: supporting
- **SC-008**: 知识可达——owner § 九 判据、status 命令一句、常驻小节指针、run-team 三处步骤均可由路径定位；未参与本轮的读者能正确复述「为什么未登记的长任务显示 [[STR-006]]」与「一个批量脚本如何变为可见」；复述判定：一名未参与本轮的基准读者各写一句答案，两句都正确即 `pass`，任一句错误即 `fail`，无法执行时记 `not-evaluated` 与原因。 **Path**: supporting
- **SC-009**: 范围克制——相对特性前基线提交，变更文件集 ⊆ 本规格声明的交付面（包装器、扫描器与其测试、owner 文档、status 命令、instructions 模板、run-team 技能、镜像与文档同步产物、本 spec 目录，以及生命周期登记所必需的 Feature 注册表文件 `.specify/features.md` 与绑定 Feature 的 detail 文件）；既有未跟踪文件保持未跟踪；无 push。允许的 delta 集合由 plan 声明的交付文件清单给出，plan 之外的新增文件视为违规。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 隔离 `SPECIFY_LINE_REGISTRY_DIR` 的夹具 registry；包装器子进程运行期间调 `python3 scripts/python/status-digest.py --action digest --workspace <repo-root>`（结束后改读条目 JSON，digest 不再列 `closed` 条目）；SIGKILL 用 `kill -9` 注入。
- **SC-002 Source**: 扫描器子进程在 fixture 根与活仓库声明根上的退出码与 stdout；fixture 由测试在 `.specify/.tmp/line-registry-registration/` 下生成并清理；根清单、文件数、命中数、`owner-skipped` 写入 `test-evidence/`。
- **SC-003 Source**: 行为测试逐条读取 registry 条目字段与 journal 目录前后计数；静态审计对 [[STR-001]] 做调用面扫描（含镜像树）；判据集合从 A-15 的单一 owner（扫描器常量）以 `import` 读取，而非测试硬编码。
- **SC-004 Source**: 子进程退出码矩阵（含 A-24 的双失败两例）；`--help`/`--version` 前后的 registry 目录快照对比；未声明选项与被包装命令的哨兵文件（执行则出现）断言未执行；关闭失败的 stderr 文本断言。
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
| `STR-009` | `"scripts/python/line-registration-scan.py"` | FR-012, FR-013, FR-015, SC-002 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-16

- 无人值守裁决：本轮不向用户提问；12 个候选问题全部按「最弱假设 / Recommended」裁决并落到 `Assumptions & Decisions`（A-14…A-24）。未决澄清标记计数为 0（上限 3）。覆盖扫描经 fresh-context 只读子代理独立执行（12 条 findings，全部被采纳或转化为裁决）。
- Q: 本特性绑定哪个 Feature？ → A: 绑定 **Feature 088「Speckit 框架可视化」**，以 slice 行 102 登记（父行状态不回退）；088 owns 本特性唯一扩展的 `reporting-obligations.md` § 九（A-14）。
- Q: 长任务机械判据的唯一 owner 取「声明层 fact」还是「扫描器内常量」？ → A: 取**扫描器模块常量**（测试以 `import` 读取，owner 文档只按路径引用；扫描器按解析路径跳过自身并具名 `owner-skipped`）。声明层 fact 被否决，因为它会新增 fact 注册并突破 FR-022 与 SC-009 的封闭交付面（A-15）。
- Q: 扫描器与辅助脚本的名称/路径本阶段固定还是交 plan？ → A: **本阶段固定** [[STR-009]] `scripts/python/line-registration-scan.py`，接口为只读 + `--root <path>`（可重复）+ 退出码 0/1/2；不新增 fixture 辅助脚本，fixture 由测试内联生成（A-16）。
- Q: `line-run.sh` 解析 `line-registry.py` 的唯一规则是什么？ → A: **有序候选**：`<repo-root>/skills/external/sdd-loop-driver/scripts/line-registry.py` → `<repo-root>/.specify/skills/sdd-loop-driver/scripts/line-registry.py`；首个可读者胜；都不可读即登记失败、具名两个路径、命令不执行；禁用未跟踪的 `.specify/scripts/line-registry.py`、`PATH` 查找与新环境变量（A-17）。
- Q: 引擎的 `--project-dir` / `--repo-root` 从哪来，同一 slug 反复运行时 registry id 如何不冲突？ → A: `git rev-parse --show-toplevel` 同时作为两个字段；registry `line_id` 合成为 `<--line-id>-<--run-id>`（每次运行唯一，同 run 重试按引擎 `line already exists` 失败闭合）；不放松引擎的 id 正则；验收示例中的非法 id 已修正（A-18）。
- Q: 关闭失败与命令失败同时发生时的退出码优先级？ → A: 命令非零 → 以命令退出码退出并把关闭失败写到 stderr；命令为 0 且关闭失败 → 以引擎失败码退出；两方结果都不得被吞掉（A-24）。
- Q: heartbeat 的触发形态与间隔？ → A: **步骤边界事件，无时间间隔**：包装器只有 register 与关闭两个事件；run-team 在 §6 每个编排步骤边界 `update --last-event <step-label>`；无定时器/守护进程/心跳文件/第二通道（A-19）。
- Q: SIGKILL 残留 `active` 的 digest 过期界限归谁？ → A: 只引用 digest 既有 owner（`scripts/python/status-digest.py` 的 `DEFAULT_STALE_BOUND_SECONDS` / `--stale-bound`）；本特性零新增阈值、零自动清理、零删除（A-20）。
- Q: 活仓库扫描根集合与 fixture 落点？ → A: 根 = `scripts/bash/`、`scripts/python/`、`skills/`；被判定文件面 = `.sh`/`.bash`/`.py` 扩展名或首行 shebang 的常规文件，跳过符号链接；fixture 根 = `.specify/.tmp/line-registry-registration/`，测试生成并清理（A-21）。
- Q: 常驻小节的落点是否只经 `templates/instructions-template.md` 投影？ → A: 是。唯一编辑面是模板的 `## Progress Reporting Discipline`，在 `Exemptions and precedence` 之后追加一条 bullet；live 文件与四个符号链接只经再生成获得（A-22）。
- Q: run-team 接线按哪个小节名与落点？ → A: 按现有小节名——§5 顶部登记、§6 编排步骤边界 heartbeat、§7 写报告前关闭并记录 `line_id`；不修改 `create-team` 的 Report 契约文件（A-23）。
- Q: `closed` 条目在 digest 中如何呈现，SC-001 的「结束后显示 closed」是否可观测？ → A: digest 按既有规则不列 `closed` 条目（唯一 line 关闭后渲染 [[STR-006]]，exit 3），故 SC-001 拆为「运行期 digest 断言 active」+「结束后 registry 条目断言 closed/reason」+「SIGKILL 后 digest 仍列出」；本特性不修改该行为（SC-001、SC-007）。
