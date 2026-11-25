# Requirements Specification: Runtime Store Layout — 运行期存储迁出 `.specify/memory/`（Runtime Store Layout）

**Requirement Branch**: `105-runtime-store-layout`
**Created**: 2026-11-25
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（修订引擎路径常量、`templates/`、`skills/`、`shared/`、安装/迁移 CLI、`.specify/glossary.md` 与 `docs/**` 的作者）与下游项目维护者（升级后需要判定「我的运行期数据去哪了、memory 目录还剩什么、哪条路径才是权威」）
**Reading scenario**: 当需要判定「每个 `.specify/memory/*` 子目录的最终归属」「`.specify/memory/` 本身是否仍存在及其唯一含义」「临时记忆（session 层）与 super agent→sub agent 上下文注入是否保持原行为」「既有客户项目的数据如何迁移、何时拒绝而不是静默并存」「新顶层目录由谁拥有、如何登记、是否被忽略」「每个向后不兼容变更由哪条迁移/拒绝行为收口」「如何确定性验收」时打开本规格，据 FR-001…FR-027 与 SC-001…SC-009 放行 `/speckit.clarify` 与后续规划
**Input**: User description: "需要启动一个无人值守开发流程, 将 session/、knowledge/、feedback/、evidence/ 等 runtime store 也从memory目录中移到上层, 让memory目录就仅仅是服务于agent语境下的"记忆"而不是人类语境下的"一切需要记住的东西", 这对之前开发的临时记忆系统和super agent向sub agent动态注入上下文机制很关键."

**输入校正**：①「移到上层」读作迁到 `.specify/` **顶层**、成为一等存储根（`.specify/<store>/`），不是再套一层分组目录；②「memory目录」指当前作为 catch-all 容器的 `.specify/memory/`，其去留由 A-2 裁定；③「临时记忆系统」按源码实测对应 memory 系统的 **session 层**（短期/可遗忘；`memory-types` 闭集为 `session`、`knowledge`；`run-determination` 经 memory 引擎把判定记录持久化进 session），仓内不存在另一个独立的「临时记忆」组件；④「super agent向sub agent动态注入上下文机制」读作既有派发载荷契约（七字段下行 / 四项注入 / 五要素上行，owner：`shared/definitions/superagent-definitions.md`）加子代理可声明的 `memory-recall` 检索，不是第二套机制；本特性只改其存储路径，不改契约语义。

## Related Feature *(mandatory)*

**Feature ID**: 024
**Feature Name**: Specification Workspace Versioning

**Binding basis (2026-11-25 clarify)**: 本规格是 Feature 024 的第二个子规格（首个为 097 `/speckit.migrate`）：024 owns「跨 CLI 版本的 `.specify/` 工作区结构升级与迁移」，本规格把运行期存储从 `.specify/memory/` 迁往顶层存储根并复用 `specify migrate` 的 plan → apply → 回执面。候选排除：055（Conflict-Free Stores）只 owns 逐条一文件的存储协议，且本规格 FR-025 明令该协议保持不变；015（CLI Interface）只 owns 命令面本身——二者均不覆盖「工作区布局迁移」语义。slice 行 105 以 `Draft` 登记，Feature Details 指向 `.specify/features/024-specification-workspace-versioning.md`；父行状态保持 `Ready for Review`，不回退。

## Overview

**实测基线（commit `23938f22e`）**：`.specify/memory/` 现有 12 个子目录——`coaching/`、`evidence/`、`exec-quant/`、`feedback/`、`housekeeping/`、`knowledge/`、`renumber/`、`retention/`、`session/`、`todo/`、`tools/`、`trigger/`；`git ls-files .specify/memory` 计得 2,963 个受跟踪路径。引擎还会按需创建 `sanitize/` 与 `migrate/receipts/`，并保留一个只被扫描器引用的遗留 `draft/`；`git-workflow.md` 是已被取代的遗留单文件，不是存储。

**问题**：当前 `memory/` 同时承担两种互不相干的语义——(1) **记忆系统**的两层存储（`session` = 短期/临时记忆，`knowledge` = 长期/蒸馏记忆），(2) **一切运行期记录**（feedback 条目、evidence 发现、执行量化遥测、触发状态、回收回执、重排计划、缓存、运行报告、教练产物、想法队列、Tool 定义、迁移回执）。后果是：memory 的语义被稀释；记忆检索与派发注入必须面对一个充满非记忆数据的命名空间；「memory」既像系统名又像目录名，读者和引擎都难以判定边界。

**本特性交付**：把每个运行期存储迁到 `.specify/` 顶层的一等存储根；**退役 `.specify/memory/` 这个容器本身**（A-2）；让「memory」只作为**记忆系统**的名字（引擎 + 两个技能 + 两个顶层记忆存储），不再是任何 catch-all 目录的名字；完整保留临时记忆（session 层）与 super agent→sub agent 动态上下文注入的既有行为；为既有客户项目提供不丢数据、不静默复活旧路径的迁移/拒绝契约。

**不做什么**：不新建存储引擎、注册表、调度器或第二套上下文注入机制；不改变任何存储的条目格式、写入协议或消费语义（只改路径与路径引用）；不改写 dated record（历史规格、历史文档、既有记录内容）；不把 `.specify/memory/` 保留为任何形式的第二权威路径。

## Assumptions & Decisions *(adjudicated here, not asked)*

| ID | Assumption / decision | Rationale |
|----|----------------------|-----------|
| **A-1** | **类别判定 = `execution`**：交付物是引擎路径常量、安装/迁移 CLI、模板、技能文本、文档与契约测试；缺陷只在机器执行、解析或断言时暴露。 | 按验收 oracle 判定（flow-class 判据），而非按介质。 |
| **A-2** | **记忆命名空间裁定**：`session/` 与 `knowledge/` **保持为记忆系统**（两层闭集不变），但它们**迁到顶层** `.specify/session/` 与 `.specify/knowledge/`；`.specify/memory/` **作为存储根整体退役**。memory 的唯一含义写入框架地图的墓碑行：「历史上的 catch-all 桶；已退役——agent 语境记忆能力由 `.specify/session/`（临时层）与 `.specify/knowledge/`（长期层）承载；任何引擎 MUST NOT 把它当作活存储创建、读取或写入」。迁移完成后该目录 MUST 不存在（空残留一并移除）；仍有未知残留时按 FR-015 报告，不静默删除。 | 请求同时要求「迁走 session/knowledge」与「memory 目录只服务 agent 记忆」；若两层留下则违背显式迁移集，若两层迁走而 memory 保留则目录无内容可服务。唯一自洽解：**memory 是系统名而非目录名**——两个记忆存储成为顶层一等存储，容器退役。这与 `docs/reference/skills/memory.md` 的既有术语（「memory system」是伞形名，两个 tier 才用 session/knowledge 命名）一致。 |
| **A-3** | **无「原样保留」的子目录**：基线的每个子目录都被分类并给出唯一处置——迁往具名顶层存储，或退役。不得因为「它已存在」而静默保留；新增发现（实现期扫描到、本文表格未列）是**表格修订**，不是静默保留。 | 简报要求完整清点与分类；目录治理要求每个目录有可达含义。 |
| **A-4** | **命名与落点**：沿用既有子目录名作为顶层存储名（`.specify/<store>/`），不新建分组目录、不改名（`session`、`knowledge` 等闭集名保持）。顶层 `.specify/tools/` 与既有 `skills` 域同构（`.specify/skills/` 目录 + `.specify/skills.md` 指南并列），因此 Tool 记录与生成清单同域共存。 | Grounded Naming：名字来自既有存储名；`tools` 有 `skills` 的现行先例。 |
| **A-5** | **`.specify/tools/` 域合并**：Tool 定义记录（`<name>.md`，权威、受跟踪）与生成清单（`{system,shell,project}.json`，机器生成、忽略）同放 `.specify/tools/`；`.specify/.gitignore` 的 `tools/` 全目录忽略规则收窄为仅忽略生成物，记录保持受跟踪。 | 现状已是「记录在 `memory/tools/`、清单在 `.specify/tools/`」的分裂；并入一个 tools 域消除分裂，且与注册义务一致（目录即概念）。 |
| **A-6** | **迁移归属安装/升级面**：一次性迁移由 `specify init`（既有项目刷新）与 `specify migrate`（计划 → apply → 回执）承担，不在每个引擎里做隐式懒迁移，也不做运行时旧路径回退。（2026-11-25 clarify：数据搬迁的唯一执行者是 `specify migrate`；`specify init` 只负责播种新布局与资产刷新，见 FR-013。） | 简报要求迁移/拒绝是显式设计输出；`specify migrate` 已拥有「dry-run → apply → archive-first → 回执」的既有结构，复用优于新建。 |
| **A-7** | **两处并存 = 冲突拒绝**：同一存储的旧位置与新位置**同时存在非空内容**时，MUST 拒绝自动合并，点名两侧路径与修复入口；MUST NOT 静默择一、覆盖或删除。**冲突判定只统计该存储的权威条目**（2026-11-25 clarify 裁定）：机器可再生且被忽略的生成物（如 `.specify/tools/{system,shell,project}.json`）与安装器播种的占位/锚点文件不构成本义上的「内容」——迁移照常执行，且 MUST NOT 覆盖或删除它们（生成物按原 owner 再生或保留，占位留原处）。旧位置存在但为空、新位置任意 ⇒ 属空残留，按 A-2 移除旧目录（不涉数据）。 | 静默合并会伪造权威；拒绝是唯一不丢数据且不复活旧路径的确定行为（fast-fail）。若把生成物/占位计入，任何刷新过新布局的项目都会与旧数据假冲突，迁移永远无法收敛。 |
| **A-8** | **无运行时双路径回退**：迁移完成后，引擎 MUST NOT 回读旧路径作为兼容层；旧路径字面量只允许出现在墓碑行、迁移引擎与其契约测试、以及遗留残留扫描器中。 | 简报明令「不得静默复活旧路径」；只读回退仍是第二权威，会让「数据在哪」不可判定。 |
| **A-9** | **`todo/`、`coaching/`、`housekeeping/` 属运行期记录，迁出**：想法队列（人类 backlog）、教练运行产物、管家运行报告都不是 agent 语境记忆，迁往顶层同名存储。 | 请求把「不是人类语境下的一切需要记住的东西」列为目标；这三者正是其典型。 |
| **A-10** | **`tools/` 不是运行期存储但是定义存储**：它不按 run 累积、不是瞬态数据；其迁出理由是「memory 不再是容器」，其落点由 A-5 决定。 | 分类的判据是语义而非清单长度；定义记录与运行记录必须各自有名。 |
| **A-11** | **文档与词汇表只改活引用**：`docs/**` 的现行页面（concepts / reference / tutorials）与 `.specify/glossary.md`、`.specify/instructions.md`、已分发指南（`templates/tools.md` 等）更新到新路径；dated record（`docs/reference/history/**`、`docs/decisions/**`、`.specify/specs/**`、`.specify/archive/**`、记录型存储内的既有条目）**不改写**。 | 根因修复不等同于重写历史；历史文档是「当时的事实」。与 104 的 A-8 先例一致。 |
| **A-12** | **两顶帽子**：源面是 `templates/`、`skills/`、`shared/`、`scripts/`、`src/`；本仓 `.specify/**` 的镜像与每工具命令副本由 `sync-mirrors.py` / `regen-command-copies.py` / 安装流程再生成，不手改镜像面。 | 本仓是 framework source 兼其自身客户；手改镜像会在同步时丢失。 |
| **A-13** | **Feature 绑定留待 `/speckit.clarify`**：本阶段按 `create-requirements` 契约保持 `Related Feature: Need clarification`，不创建、不绑定 Feature。（2026-11-25 clarify 已履行：已绑定 Feature 024，见 § Related Feature 与 § Clarifications；本条保留为 requirements 阶段的时点记录。） | Feature Integration Protocol 的绑定时点在 clarify。 |
| **A-14** | **零新增机制**：不新增注册表、调度器、常驻进程、评分或第二注入机制；新顶层目录的「登记」复用既有框架地图行（目录治理的登记义务），不建目录索引生成器。 | 宪法 IX / XVII 与简报非目标。 |
| **A-15** | **并发读数**：本阶段为单执行体的有界委派，按 `single-unit` 记录读数三元组（`requested` / `effective` / `effective_reason`）；改动面虽大，但文件读写与验收在同一叶内顺序完成，不构成单执行体内扇出。 | owner：`subagent-definitions.md` § The Concurrency Obligation、`serial-reason.yaml`。 |
| **A-16** | **「Runtime Store」是新概念**：实测 `.specify/shared/definitions/` 下无该词条的 owner；本规格采用简报给出的工作分类（按 run 累积的记录、遥测、缓存、队列、回执、瞬态运行状态），并在实现期提议词汇表条目（用户确认通道），不在本文内联定义一个与既有 owner 竞争的定义。**确认门语义（2026-11-25 clarify 裁定）**：提议文本留在该 run 的证据/笔记中；未经用户确认 MUST NOT 写入 `.specify/glossary.md`；FR-021 对 glossary 的既有活路径更新不受此门影响；无验收标准依赖该新词条，无人值守运行 MUST NOT 因等待确认而阻塞。 | Concept-owner check：无 owner 的概念如实声明为新概念；提议≠落地，且无人值守流程不得被确认门卡死。 |

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 打开 `.specify/` 就能看懂每个存储属于谁、memory 只意味着记忆 (Priority: P1)

维护者浏览 `.specify/`：`session/`、`knowledge/` 是记忆系统的两个 tier；`feedback/`、`evidence/`、`exec-quant/`、`trigger/`、`retention/`、`renumber/`、`sanitize/`、`housekeeping/`、`coaching/`、`todo/`、`tools/`、`migrate/` 各自是一等存储；没有任何 `memory/` 目录可以变成「什么都往里放」的桶。他打开框架地图，每一行都写明该存储的 owner、生命周期与内容类别，墓碑行说明旧根已退役且没有第二权威。

**Why this priority**: 这是用户请求的语义核心——「memory 目录仅仅是 agent 语境的记忆」；没有清晰的顶层归属，其余都是改名。

**Independent Test**: 以基线提交的 `git ls-tree` 清单对照规格的封闭清点表，逐项断言唯一处置；实现后断言旧根不存在、每个目标根已在框架地图登记。

**Acceptance Scenarios**:

1. **Given** 基线提交 `23938f22e` 的 `.specify/memory/` 子目录清单，**When** 对照本规格的 Store Inventory，**Then** 每个子目录（含引擎按需创建的 `sanitize/`、`migrate/receipts/` 与被扫描器引用的遗留 `draft/`）都有且只有一个处置，无遗漏、无「静默保留」。
2. **Given** 实现完成的工作树，**When** 检查 `.specify/memory/`，**Then** 该路径不作为活存储存在，且没有任何引擎/模板/文档把它当作当前位置。
3. **Given** 框架地图，**When** 查找任一顶层存储，**Then** 存在一行给出 owner、生命周期与内容类别；`memory` 只以墓碑行出现。

---

### User Story 2 - 既有客户项目升级不丢数据，冲突时大声拒绝 (Priority: P1)

客户项目的 `.specify/memory/` 里有多年积累的 feedback、exec-quant、session 记录。升级后，这些数据出现在新的顶层存储里，条目内容不变；如果旧位置与新位置都有非空内容，升级/迁移**停下来**，点名两条路径和修复方式，而不是悄悄选一边。重复运行迁移不会产生第二次移动或重复数据。

**Why this priority**: 路径迁移的第一风险是数据丢失或双权威；没有迁移契约，这个特性就是一次危险的改名。

**Independent Test**: 三个夹具——仅旧布局、旧新并存、迁移重跑——分别断言：内容零丢失、确定性拒绝、幂等。

**Acceptance Scenarios**:

1. **Given** 一个只有旧布局数据的夹具项目，**When** 执行迁移，**Then** 每个已知存储的内容移动到对应新顶层路径，条目逐字节一致，回执按 run 记录，旧根在迁移完成后为空并被移除。
2. **Given** 同一存储的旧位置与新位置都含非空内容，**When** 执行迁移，**Then** 迁移拒绝自动合并，输出两侧路径与修复入口，不移动、不覆盖、不删除任何一侧的数据。
3. **Given** 迁移已成功一次，**When** 再次执行迁移，**Then** 判定为已收敛（no-op），不产生重复条目、不重建旧根。
4. **Given** plan 的 § Backward-Incompatible Change Inventory，**When** 逐行执行 `/speckit.migrate` 的 dry-run 与 apply/refuse 并运行清点守卫，**Then** 每一行都产出其具名结局（`migrate:relocate` / `migrate:container-pass` / `migrate:refuse:*` / `compatibility-bridge` / `no-workspace-object`）与证据指针；任一未映射、未迁移或依赖运行时回退 / 人工说明的行使守卫转红（FR-027、SC-009）。

---

### User Story 3 - 临时记忆与上下文注入在新路径下行为不变 (Priority: P1)

一个 super agent 在派发子代理前检索记忆并注入上下文。升级后：`memory-record` 写入 `.specify/session/`（短期）或 `.specify/knowledge/`（长期）；`memory-recall` 仍能按关键词/标签/日期检索；`run-determination` 的判定记录仍落在 session 层并可被召回；派发载荷仍携带七字段下行、四项注入与五要素上行，注入的记忆条目引用新路径，从不引用退役根。记忆检索只返回记忆条目，不再混入 feedback/evidence 等运行记录。

**Why this priority**: 用户明确说这次改动对「临时记忆系统」与「动态注入上下文机制」很关键；路径迁移若破坏这两者，特性即失败。

**Independent Test**: 记录→召回往返；`run-determination` 持久化后可召回；一个派发夹具注入记忆并断言来源路径与载荷字段。

**Acceptance Scenarios**:

1. **Given** 空的会话记忆存储，**When** 通过 memory 引擎记录一条 session 条目并召回，**Then** 引擎在 `.specify/session/` 写入单条目文件、召回命中该条目，内容与写入一致。
2. **Given** 一次完成的运行，**When** `run-determination` 持久化判定记录，**Then** 记录落在 session 层的新路径下且可被召回，记录 schema 不变。
3. **Given** 一个声明了 memory-recall 的子代理派发，**When** 注入上下文，**Then** 注入的来源全部是新顶层记忆存储中的条目，载荷的七字段/五要素契约不变。
4. **Given** 一条只存在于 feedback 或 exec-quant 存储中的文本，**When** 以相同关键词检索记忆，**Then** 记忆检索不返回该文本（记忆边界可验证）。

---

### User Story 4 - Tool 记录与生成清单一处共存，受跟踪与忽略各归其位 (Priority: P2)

维护者打开 `.specify/tools/`：`<name>.md` 是可编辑、受版本控制的 Tool 定义记录；`{system,shell,project}.json` 是机器生成、被忽略的发现清单。二者同域但不互相覆盖，`/speckit.tools` 与复用门都指向同一个位置；`.specify/.gitignore` 的规则恰好忽略生成物，而不是整个目录。

**Why this priority**: 这是迁移中唯一一个「记录 vs 生成物」混居的目录，忽略规则错了会要么丢失记录、要么把生成物提交进库。

**Independent Test**: 夹具运行生成清单后，断言 `*.json` 被忽略、`*.md` 被跟踪；模板与已安装副本的忽略规则逐字一致。

**Acceptance Scenarios**:

1. **Given** `.specify/tools/` 同时存在 `<name>.md` 与生成清单，**When** 检查忽略状态，**Then** 只有生成物被忽略，记录被跟踪。
2. **Given** 框架模板中的 `.specify/.gitignore` 与本仓已安装副本，**When** 逐字比较，**Then** 二者一致（同一变更内同步）。

---

### User Story 5 - 仓库自身（dogfood）完成迁移且镜像零漂移 (Priority: P2)

本仓作为其自身的客户项目执行迁移：2,963 个受跟踪路径按存储归类移动（保留 git 历史），`.specify/instructions.md`、`.specify/glossary.md`、框架地图与运行期脚本指向新路径；`skills/`、`shared/`、`templates/`、`agents/` 的镜像与每工具命令副本在同一变更内再生成，镜像检查干净。

**Why this priority**: 框架源与其自用运行时必须同时收敛，否则下一次 `specify init` 会把旧布局重新种回客户项目。

**Independent Test**: 迁移后 `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 均 rc 0；旧路径字面量在活引用面之外为零。

**Acceptance Scenarios**:

1. **Given** 本仓的 `.specify/memory/`，**When** 执行迁移，**Then** 受跟踪条目按存储移动到新顶层路径，`git log --follow` 可追溯，未分类残留为零或被显式报告。
2. **Given** 迁移后的源面变更，**When** 运行镜像同步与命令副本再生成，**Then** 两处检查均 rc 0，且源与镜像逐字节一致。

---

### User Story 6 - 半迁移与不可迁移状态被诚实报告，不被当作成功 (Priority: P3)

迁移中途被中断、旧位置有未知文件、新位置权限不足、或旧位置是符号链接时，系统不猜、不合并、不清空：它给出点名路径的拒绝与修复入口；下一次运行能从回执/现场状态继续或再次拒绝，绝不以「新建了空存储」冒充成功。

**Why this priority**: 未定义失败形态会让数据看起来「迁移成功但消失了」——这是最坏的结局。

**Independent Test**: 中断注入、未知残留、权限只读三个夹具分别断言确定性拒绝/恢复语义与零静默数据丢失。

**Acceptance Scenarios**:

1. **Given** 旧位置含已知存储之外的未知文件，**When** 迁移完成已知存储，**Then** 未知文件保留原处并逐个报告（归档需用户确认），不被删除、不被当作某存储内容。
2. **Given** 迁移在写入中途被中断，**When** 再次运行，**Then** 依据回执与现场状态判定继续或拒绝，不产生重复条目或半个条目。
3. **Given** 旧位置是新位置的符号链接（或反之），**When** 迁移探测，**Then** 以点名该路径的拒绝收束，不拆链、不跟随写入。

---

### Edge Cases

- **旧空新空**：旧位置存在但为空——按空残留移除旧目录；新建两个记忆存储占位，不产生回执条目（无数据移动）。
- **旧空新非空**：只移除空旧目录；新位置为权威，不合并、不覆盖。
- **旧非空新非空**：冲突拒绝（A-7），即使两侧内容看起来相同也拒绝自动合并；修复入口要求人工裁定（合并或改配），因为「相同」是当时快照，不是持续事实。
- **旧位置含未知顶层文件**（如遗留 `git-workflow.md`）：不当作任何存储；报告并保留，删除需用户确认（archive-first）。
- **迁移与引擎写入交错**：迁移是一次性前置动作；迁移未完成时引擎 MUST NOT 在新位置创建同名存储（否则制造并存冲突）。
- **记忆层与运行记录同名目录**：新顶层命名与既有根目录（项目根的 `feedback/` 入站包目录、spec 内的 `test-evidence/`）不冲突——它们是不同根、不同语义；文档必须消歧。
- **`tools` 记录名与生成清单名同基名**：`X.md` 与 `X.json` 可共存；生成清单不得覆盖记录。
- **只读/权限错误**：迁移以点名路径的拒绝收束，不部分成功后退回。
- **重复运行**：幂等；已收敛时 no-op 且有明确输出。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 存储清点与目标布局

- **FR-001**: 本规格 MUST 维护一份**封闭的存储清点表**（见 § Store Inventory），覆盖基线提交 `23938f22e` 的 `.specify/memory/` 全部子目录、引擎按需创建的存储根（`sanitize/`、`migrate/receipts/`）与被扫描器引用的遗留项（`draft/`、`git-workflow.md`，后者不是存储）；每一项 MUST 有且只有一个处置（迁往具名顶层存储 / 退役）。清点表之外的发现 MUST 走表格修订，MUST NOT 静默保留。
- **FR-002**: 四个具名存储 MUST 迁为顶层一等存储：session 记忆 → [[STR-002]]，长期记忆 → [[STR-003]]，feedback 存储 → [[STR-004]]，evidence 存储 → [[STR-005]]；内容契约（每条目一文件、派生索引即读即建、无共享聚合）保持不变。
- **FR-003**: 其余已知存储 MUST 迁往同名顶层根：exec-quant、trigger、retention、renumber、sanitize、housekeeping、coaching、todo、migrate（回执）；Tool 定义记录与生成清单 MUST 归入 [[STR-006]] 这一 tools 域（A-5）；遗留 `draft/` MUST 退役，不设新家。
- **FR-004**: [[STR-001]] MUST 作为**存储根退役**：任何引擎、模板、技能、文档或测试 MUST NOT 把它创建、读取或写入为活存储；其唯一记录含义 MUST 是框架地图中的墓碑行（A-2 的措辞）。迁移完成后该目录 MUST 不存在；空残留 MUST 移除，未知残留 MUST 按 FR-015 报告而非删除。
- **FR-005**: 每个顶层存储 MUST 有唯一 owning 组件，写在框架地图行内（owner / 生命周期 / 内容类别）；既有写入关系 MUST 原样保留（记忆只经 memory 引擎、feedback 只经 feedback 引擎、evidence 只经 evidence 引擎等），MUST NOT 引入第二写入者或跨存储写入。

#### B. 记忆系统与临时记忆的保持

- **FR-006**: 记忆系统 MUST 保持既有两层闭集（`session` = 短期/临时 → [[STR-002]]、`knowledge` = 长期 → [[STR-003]]）与既有动作契约（record / recall / list / prune / reindex / scope all）；**唯一变化是存储根迁到顶层**。作用域名 MUST NOT 改名，调用方 MUST NOT 硬编码路径（只经引擎解析）。
- **FR-007**: 临时记忆路径 MUST 在迁移后保持行为不变：`run-determination` 的持久化适配器经记忆引擎把判定记录写入 session 层新根，记录可被 `memory-recall` 检索，记录 schema 与字段不变。
- **FR-008**: 记忆检索 MUST 只读取两个记忆存储，MUST NOT 遍历或返回迁出的运行期存储（feedback、evidence、exec-quant、trigger、retention、renumber、sanitize、housekeeping、coaching、todo、tools、migrate）中的条目；该边界 MUST 可被一个反向夹具验证（只存在于运行期存储的文本不被记忆召回返回）。
- **FR-009**: 「memory」MUST 只作为记忆系统（引擎 + record/recall 技能 + 两个记忆存储）的伞形概念名，MUST NOT 再指代任何 catch-all 目录；记忆相关文档与词汇表 MUST 以两个新顶层路径命名两个 tier。

#### C. super agent → sub agent 动态上下文注入

- **FR-010**: 派发载荷契约 MUST 保持不变：七字段下行（`parent_identity`、`child_label`、`role_declaration`、`dispatch_duty`、`depth_position`、`authority_ref`、`return_channel`）、四项既有注入（快速失败、并发义务、汇报义务、再锚定）与五要素上行；记忆上下文的来源 MUST 仍仅是记忆系统经引擎检索的条目。
- **FR-011**: 任何注入到派发中的记忆引用 MUST 指向新顶层记忆存储中的条目；派发载荷 MUST NOT 引用退役根。声明了 memory-recall 的 agent 模板 MUST 在新路径下工作，无需改变声明方式。
- **FR-012**: 本特性 MUST NOT 引入第二套上下文注入机制、第二记忆源或新的注入存储；只允许修改既有机制的路径引用。

#### D. 迁移、升级与客户数据安全

- **FR-013**: 既有客户项目 MUST 有一条一次性迁移路径，把旧布局中每个已知存储的内容移动到对应新顶层路径；迁移 MUST 幂等，且 MUST 按 run 写回执（每条目一文件，MUST NOT 写共享聚合）。**执行者裁定（2026-11-25 clarify）**：数据搬迁的唯一执行者是 `specify migrate`（plan → apply → archive-first → 回执）；`specify init` 只负责全新工作区的布局播种与既有工作区的资产刷新，MUST NOT 搬移旧存储内容——检测到旧位置仍有内容时保持原地不动并指向 `specify migrate`（与 init 对 legacy anchor 的 skip-and-defer 先例一致，A-6、A-8）。
- **FR-014**: 迁移中任何破坏性步骤 MUST archive-first（先归档再处置），数据零丢失，回执 MUST 记录可恢复路径；MUST NOT 以「删除旧目录」代替迁移。
- **FR-015**: 同一存储的旧位置与新位置同时含非空内容时，迁移 MUST 拒绝自动合并（A-7）：点名两侧路径与修复入口（人工裁定合并或改配），MUST NOT 移动、覆盖或删除任何一侧；「非空内容」MUST 按 A-7 的权威条目口径判定（机器可再生的忽略生成物与安装器播种占位不计入，且 MUST NOT 被覆盖或删除）；旧位置含未知项时 MUST 逐个报告并保留，删除只在用户确认后按 FR-014 进行。
- **FR-016**: 迁移完成后，退役根 [[STR-001]] MUST NOT 被重建或被读取；仍有未处理遗留内容的项目在下次引擎使用时 MUST 得到确定性拒绝或迁移指引，MUST NOT 得到一个掩盖旧数据的空新存储。迁移完成状态 MUST 可由现场事实判定（不依赖对话记忆）。
- **FR-017**: 全新初始化 MUST 种出新布局（至少两个记忆存储；其余存储按需懒创建）并 MUST NOT 创建退役根；安装包种入内容与安装器核心资产保留清单 MUST 同步更新。

#### E. 框架面一致性（源、安装、登记、忽略、镜像、文档）

- **FR-018**: 所有活路径常量 MUST 更新到新根，至少覆盖：`memory-utils.py`、`feedback-utils.py`、`evidence-utils.py`、`exec-quant.py`、`run-determination.py`、`sanitize-utils.py`、`renumber-utils.py`、`trigger-utils.py`、`tools-utils.py`、`skills-utils.py`、`migrate` 回执路径、`sdd-project-setup` 与 `sdd-house-keeping` 的 `mechanism-inventory.py`，以及 `shared/declarations/facts/memory-types.yaml` 的路径注记；实现期的仓内扫描是完整性 oracle（见 SC-006），本文列出的是下限而非上限。
- **FR-019**: 安装器/升级面 MUST 更新：核心资产保留清单（`.specify/memory` 一项）、包内种子布局（`memory/session`、`memory/knowledge` 的占位与两个锚点文件的特例复制）、非 Claude 工具的路径改写规则与 `memory/features/` 遗留特例 MUST 与退役根一致；已安装副本与包内模板 MUST 由同一变更产出并一致。
- **FR-020**: 忽略规则 MUST 在同一变更内更新（框架模板与已安装副本逐字一致）：原 `memory/sanitize/`、`memory/trigger/telemetry.jsonl` 等等价规则改到新路径；`.specify/tools/` 的全目录忽略 MUST 收窄为仅生成物（A-5）；`.codexignore` / `.claudeignore` 等忽略模板中的 `!.specify/memory/` 类放行 MUST 改为放行新存储根。
- **FR-021**: 目录治理登记 MUST 完成：框架地图为每个新顶层存储新增一行（owner / 生命周期 / 内容），并以墓碑行记录退役根；`.specify/instructions.md`（模板源与已安装副本）、`.specify/glossary.md` 的活引用（含 `Memory Layer`、`Session(消歧)`、`三捕获机制`、`Renumber Lane`、`Coaching Run`、自省报告等条目中的路径）与已分发指南（如 `templates/tools.md`）MUST 指向新路径。
- **FR-022**: 镜像与副本 MUST 在同一变更内再生成：`skills/`、`shared/`、`templates/`、`agents/` 与 `.specify/` 的镜像对、以及每工具命令副本；`sync-mirrors.py --check` 与 `regen-command-copies.py --check` MUST rc 0，MUST NOT 手改镜像面。
- **FR-023**: dated record MUST NOT 改写：`docs/reference/history/**`、`docs/decisions/**`、`.specify/specs/**`、`.specify/archive/**` 与记录型存储中的既有条目保持原文；它们对旧路径的提及是历史事实，不是活引用。

#### F. 质量与验收

- **FR-024**: 契约测试 MUST 钉住：每个引擎在新根上的往返；退役根在活引用面之外零出现（允许集被守卫测试钉住，见 SC-006）；迁移三种形态（仅旧 / 并存拒绝 / 幂等重跑）；记忆记录→召回；派发注入夹具；全新初始化布局；忽略与跟踪的拆分（`tools/`）；模板与已安装副本一致。
- **FR-025**: 并发写安全 MUST 保持：每个存储仍是每条目一文件、派生索引即读即建；MUST NOT 引入共享可变聚合；每个新存储 MUST 有一个「两写入者产生不同路径」的模拟测试。
- **FR-026**: 验收 MUST 证明**行为保持**而不只是路径存在：记忆记录→召回、feedback 记录→打包/接收链路的路径、evidence 车道读取 feedback、exec-quant 收集、trigger 求值、retention 车道、`run-determination` 持久化、以及一次派发上下文注入场景，全部在新路径下各跑一次并留证。
- **FR-027**: 本特性引入的每一个**向后不兼容变更**（使既有工作区在新版本下的路径或行为不再成立的变更）MUST 在 `/speckit.migrate` 中拥有可执行迁移逻辑，或在迁移不安全处给出确定性拒绝；MUST NOT 只依赖运行时双路径回退或人工操作说明。plan MUST 维护一份**封闭的向后不兼容变更清点**（`plan.md` § Backward-Incompatible Change Inventory），与 § Store Inventory 逐行对应，并覆盖本特性交付的全部路径/契约断点（至少含容器退役、包内种子命名空间改名与 tools 记录/清单分裂）；清点中的每一行 MUST 具名其迁移/拒绝行为（闭集：`migrate:relocate`、`migrate:container-pass`、`migrate:refuse:<M-5 token>`、`compatibility-bridge`、`no-workspace-object`）与证据指针。`no-workspace-object` 只允许用于不进入任何工作区的包内资产命名空间，且其工作区可见后果 MUST 由对应的 store 行与全新初始化夹具覆盖；任何工作区状态变更 MUST NOT 归入该类。清点中任一未映射、未迁移或依赖回退/人工说明的行 MUST 使 FR-027 的守卫测试转红。

### Key Entities *(include if requirement involves data)*

- **Store（存储）**：一个顶层 `.specify/<store>/` 根；属性：name、root path、owner、lifecycle（记忆 tier / 运行记录 / 遥测 / 缓存 / 队列 / 回执 / 定义记录）、内容类别、忽略策略、迁移来源（旧子目录路径）。
- **Memory Tier（记忆层）**：记忆系统的两个成员（`session` 短期/临时、`knowledge` 长期/蒸馏）；闭集 owner 为 `shared/declarations/facts/memory-types.yaml`；路径迁移但成员集不变。
- **Retired Store Root（退役存储根）**：`.specify/memory/` 的墓碑实体；属性：literal、tombstone row 位置、允许出现集（墓碑行 / 迁移引擎与其测试 / 遗留残留扫描器）、禁止行为（创建/读写/回退）。
- **Store Inventory Row（清点行）**：baseline child、classification、target root、owner、note；完整性 oracle 是基线提交的目录清单加引擎声明集。
- **Migration Receipt（迁移回执）**：每次迁移 run 一份，每条目一文件；属性：run id、每个存储的源/目标、条目计数、归档恢复路径、冲突项与未知项清单、结局 token。
- **Injection Payload（注入载荷）**：super agent→sub agent 派发的既有契约（七字段下行、四项注入、五要素上行）；本特性只更新其记忆来源路径，不改字段集。

### Store Inventory (closed)

> 清单口径：基线提交 `23938f22e` 的 `.specify/memory/` 子目录（实测 12 个）＋引擎在源码中声明的按需存储根＋遗留项。任何不在本表内的基线成员是表格缺陷，必须修订本表。

| # | Baseline member | Classification | Disposition / target root | Owner | Note |
|---|-----------------|----------------|---------------------------|-------|------|
| 1 | `session/` | 记忆 tier（短期/临时） | `.specify/session/` | memory 引擎 | 显式迁移集；临时记忆 |
| 2 | `knowledge/` | 记忆 tier（长期/蒸馏） | `.specify/knowledge/` | memory 引擎 | 显式迁移集 |
| 3 | `feedback/` | 运行记录（条目/探针/backlog） | `.specify/feedback/` | feedback 引擎 | 显式迁移集 |
| 4 | `evidence/` | 运行记录（发现集合） | `.specify/evidence/` | evidence 引擎 | 显式迁移集 |
| 5 | `exec-quant/` | 遥测（每单元测量，含 `aggregated/`） | `.specify/exec-quant/` | exec-quant 引擎 | 按 run 累积 |
| 6 | `trigger/` | 运行状态 + 遥测 | `.specify/trigger/` | trigger 引擎 | telemetry 仍忽略 |
| 7 | `retention/` | 回执/摘要/计划/账本 | `.specify/retention/` | sanitize retention lane | 消费→回执→回收 |
| 8 | `renumber/` | 计划/账本 | `.specify/renumber/` | sanitize renumber lane | 重复号修复 |
| 9 | `sanitize/` | 机器可再生缓存（findings/plan） | `.specify/sanitize/` | sanitize 引擎 | 引擎按需创建 |
| 10 | `housekeeping/` | 运行报告（每次运行一份 YAML） | `.specify/housekeeping/` | sdd-house-keeping | 不聚合、不改写旧报告 |
| 11 | `coaching/` | 教练运行产物（每 run 一目录） | `.specify/coaching/` | coaching-skills | expectation/observation/… |
| 12 | `todo/` | 想法队列（人类 backlog） | `.specify/todo/` | manage-todo Park | 非 agent 记忆 |
| 13 | `tools/` | 定义记录（每工具一 `.md`） | `.specify/tools/` | tools 系统 | 与生成清单同域（A-5） |
| 14 | `migrate/receipts/` | 回执（每 run 一份） | `.specify/migrate/receipts/` | `specify migrate` | 引擎按需创建 |
| 15 | `draft/` | 遗留项（无活写入者；仅扫描器引用） | 退役（不设新家） | sanitize 遗留扫描 | 残留按 FR-015 报告 |
| 16 | `git-workflow.md` | 遗留单文件（已被 `.specify/workflow/git.md` 取代） | 非存储；按既有 owner 的遗留规则处理 | git-utils | 不改写 |
| 17 | `.specify/memory/` 容器本身 | 退役容器 | 墓碑行（A-2） | 框架地图 | 无第二权威 |

### Runtime Stack & Dependency Ownership

`execution` 类特性必填；本特性不新增运行时依赖、不新增第三方包——它交付路径常量、安装/迁移面、模板、文档与契约测试，并消费既有 Python 解释器、pytest 运行器、唯一测试入口、既有存储引擎族与既有安装/迁移 CLI。表中 `Premises` 引用的 `EP-NNN` 由 plan 阶段 `## Execution Premises` 定义（本阶段不建 premises 表）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython `>=3.8` 标准库（引擎路径解析、契约测试的文本与文件操作） | signed-contract | CPython 上游（本仓只消费，不打包） | `pyproject.toml` 既有 `requires-python`；本特性零新增第三方依赖 | `pyproject.toml` | 新增测试在 `>=3.8` 解释器上经唯一入口通过；本特性新增第三方 import 为零 | FR-018, FR-024, FR-026 | EP-001 |
| RS-002 | `pytest` 测试运行器（契约 / 集成 / 文档测试） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有 pytest 声明；零新增依赖 | `pyproject.toml` | 经 `scripts/bash/run-tests.sh` 运行新增测试，相对入口基线零新增名字级失败 | FR-024, FR-025, FR-026 | EP-001 |
| RS-003 | POSIX `bash` 运行时（唯一测试入口与安装/迁移脚本） | signed-contract | bash 上游 / 运行环境（本仓只消费） | 不新增显式版本下限；本特性不改动该入口契约 | `scripts/bash/run-tests.sh` | 新增测试全部经该入口执行且一次退出 0 | FR-019, FR-024, FR-026 | EP-001 |
| RS-004 | 既有记忆引擎与记忆技能（记录/召回/裁剪/重建，两层闭集） | in-scope | 本特性修改的 framework 源（`memory-utils.py` 与 memory-* 技能） | 不适用（仓内实现，无外部版本面） | `scripts/python/memory-utils.py` | 记录→召回往返、`run-determination` 持久化可召回、记忆边界反向夹具通过 | FR-006, FR-007, FR-008, FR-009 | EP-002 |
| RS-005 | 既有安装/迁移 CLI（`specify init` 刷新与 `specify migrate` 计划/apply/回执） | in-scope | 本特性修改的 framework 源 CLI | 不适用（仓内实现） | `src/specify_cli/__init__.py` | 三形态迁移夹具（仅旧 / 并存拒绝 / 幂等重跑）与全新初始化夹具通过 | FR-013, FR-014, FR-015, FR-016, FR-017, FR-019 | EP-003 |
| RS-006 | 既有运行期存储引擎族（feedback / evidence / exec-quant / trigger / retention / renumber / sanitize / tools / 技能脚本） | in-scope | 本特性修改的各引擎与技能脚本 | 不适用（仓内实现） | `scripts/python/feedback-utils.py` | 每个引擎在新根上完成一次行为往返；`sync-mirrors.py --check` rc 0 | FR-018, FR-022, FR-026 | EP-002 |

**Contract-cell note**: 每个 `Contract` 单元格只放一个仓内可解析路径；`RS-004`–`RS-006` 指向本特性修改的既有引擎的代表文件，不是第二契约。既有引擎的条目格式与写入协议在本次迁移中零修改，义务只在路径与引用上。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 存储清点封闭且旧根退役：以基线提交 `23938f22e` 的 `.specify/memory/` 子目录集合＋引擎声明集为基线参照物，按目录名集合比较，每个成员在 Store Inventory 中恰有一个处置（允许差异集 = 表中列出的目标根集合与退役项集合，含 [[STR-004]] 与 [[STR-005]] 的顶层目标），集合之外无成员；实现后 [[STR-001]] 不作为活存储存在。**Path**: final
- **SC-002**: 记忆行为保持：在空夹具上执行 session 与 knowledge 各一次记录→召回往返，写入落在两个新顶层记忆存储 [[STR-002]] / [[STR-003]] 且内容一致；`run-determination` 判定记录落在 session 新根并可召回；prune 与 reindex 的既有语义不变。**Path**: final
- **SC-003**: 注入行为保持：一次声明 memory-recall 的派发夹具中，注入的全部记忆引用解析到 [[STR-002]] / [[STR-003]] 中的条目，载荷七字段与五要素齐备；反向夹具证明运行期存储条目不进入记忆召回。**Path**: final
- **SC-004**: 迁移安全：三形态夹具中，仅旧布局的内容零丢失地到达新根（逐字节比较），并存形态确定性拒绝且两侧数据不变，重跑形态幂等（第二次运行无移动、无重复条目、不重建旧根）。**Path**: final
- **SC-005**: 全新初始化：在空夹具上执行初始化后，两个记忆存储以新路径存在、退役根不存在、其余存储懒创建；初始化不产生任何指向退役根的活引用。**Path**: final
- **SC-006**: 活引用面零旧路径：以基线提交 `23938f22e` 加实现起点捕获的允许集为参照，按**产物类**比较（框架源类：`templates/`、`skills/`、`shared/`、`scripts/`、`src/`；运行期指南类：`.specify/instructions.md`、`.specify/glossary.md`；现行文档类：`docs/**` 除 `docs/reference/history/**` 与 `docs/decisions/**`），每类对旧路径字面量 [[STR-001]] 的出现文件集合 MUST 等于声明的允许集（墓碑行、迁移引擎与其契约测试、遗留残留扫描器——该允许集由守卫测试钉住并断言实测 = 声明）；允许集之外的产物 MUST 零出现，允许集之内 MUST 只以墓碑/迁移语境出现。**Path**: supporting
- **SC-007**: 镜像与副本干净：`sync-mirrors.py --check` 与 `regen-command-copies.py --check` 均 rc 0；严格镜像对逐字节一致，相对基线无新增漂移。**Path**: supporting
- **SC-008**: 忽略与跟踪各归其位：`.specify/.gitignore` 模板与已安装副本逐字节一致；基线中被忽略的运行期路径在各自新位置仍被忽略、被跟踪的存储条目仍被跟踪；[[STR-006]] 下 `*.md` 被跟踪、生成 `*.json` 被忽略。**Path**: supporting
- **SC-009**: 向后不兼容变更闭包：plan § Backward-Incompatible Change Inventory 的每一行都映射到一条**被测试的**迁移/拒绝行为；任一 Store Inventory 状态变更行未被映射、或任一映射缺少证据读数，守卫测试 MUST 转红；对全部映射的 store 变更，`/speckit.migrate` 的 dry-run 零写入与 `--apply` 行为 MUST 被演示并留证。**Path**: final

### Measurement Sources & Collection Methods

- **SC-001 Source**: `git ls-tree -d 23938f22e:.specify/memory`（基线子目录名集合）＋实现期对引擎声明集的扫描；与 Store Inventory 表逐行比对；迁移后 `test ! -d .specify/memory` 与残留报告。测于实现完成时一次。
- **SC-002 Source**: `memory-utils.py --action record/recall/list/prune/reindex --format json` 在夹具工作区的输出；`run-determination.py --action determine` 的持久化结果与 `--action history` 检索。每次实现阶段与 review 阶段各一次。
- **SC-003 Source**: 派发夹具（prompt/载荷快照 + 注入条目路径清单）；`run-role-edge`/载荷字段检查器；记忆边界反向查询结果。实现与 review 各一次。
- **SC-004 Source**: 三形态夹具的迁移输出（结局 token、回执文件、`diff -r` 逐字节比较、第二次运行输出）。实现与 review 各一次。
- **SC-005 Source**: 空目录夹具上的 `specify init` 树清单（`find .specify -maxdepth 1`）。实现一次。
- **SC-006 Source**: 仓内扫描（按类枚举出现文件集合）+ 守卫测试的允许集断言。实现与 review 各一次；扫描命令与输出存证。
- **SC-007 Source**: 两个 `--check` 命令的 rc 与输出；严格镜像对的 `cmp` 结果。实现与 review 各一次。
- **SC-008 Source**: `git check-ignore -v` 夹具；模板与已安装副本的 `cmp`。实现一次。
- **SC-009 Source**: `tests/contract/test_runtime_store_layout.py::test_backward_incompatible_inventory_is_closed` 的清单 / 行为闭集 / 证据指针断言与变异演练；M-8 夹具套件的 dry-run 零写入与 `--apply` 读数（legacy / dual / residue）。读数写入 `test-evidence/acceptance-105.md` 的 SC-009 行。实现与 review 各一次。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | ".specify/memory/" | FR-004, FR-016, SC-001, SC-006 |
| `STR-002` | ".specify/session/" | FR-002, FR-006, SC-002, SC-003 |
| `STR-003` | ".specify/knowledge/" | FR-002, FR-006, SC-002, SC-003 |
| `STR-004` | ".specify/feedback/" | FR-002, SC-001 |
| `STR-005` | ".specify/evidence/" | FR-002, SC-001 |
| `STR-006` | ".specify/tools/" | FR-003, SC-008 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-25（无人值守 requirements 阶段，自行裁决并记录）

- Q: `.specify/memory/` 本身保留还是退役？ → A: 退役（A-2）：两个记忆存储迁到顶层并保持为记忆系统；memory 成为系统名而非目录名；墓碑行记录唯一含义。
- Q: `session/` 与 `knowledge/` 迁走是否等于废除记忆？ → A: 否。成员集、作用域名与引擎动作契约全部不变，仅存储根改为顶层。
- Q: 哪些子目录可以留在 `memory/`？ → A: 无。每个子目录都有唯一处置（Store Inventory）；`tools/` 迁入 `.specify/tools/` tools 域，`draft/` 退役。
- Q: 迁移在哪里发生，是否允许运行时旧路径回退？ → A: 由 `specify init` 刷新与 `specify migrate` 承担（A-6）；不允许运行时双路径回退（A-8）。
- Q: 旧新并存如何处理？ → A: 一律拒绝自动合并，点名修复入口（A-7）；仅「旧空」属可安全移除的残留。
- Q: 「临时记忆系统」与「动态注入」是否被重新定义？ → A: 不。前者是 memory 系统的 session 层（实测唯一临时记忆机制），后者是既有派发载荷 + memory-recall；本特性只改路径引用。

### Session 2026-11-25（无人值守 clarify 阶段，Feature 绑定与残留歧义裁决）

- Q: `Related Feature` 绑定到哪个既有 Feature？ → A: 绑定 Feature 024（Specification Workspace Versioning），以 slice 行 105 登记 `Draft`（先例：097/100/102）；父行状态保持 `Ready for Review` 不回退。候选排除：055 只 owns 逐条一文件的存储协议（FR-025 明令保持不变）、015 只 owns CLI 命令面，均不覆盖「工作区布局迁移」语义。
- Q: 一次性迁移的执行者是 `specify init` 刷新还是 `specify migrate`（FR-013 原文「和/或」）？ → A: 数据搬迁唯一执行者 = `specify migrate`（plan → apply → archive-first → 回执）；`specify init` 只播种新布局/刷新资产并跳过旧内容，检测到旧存储内容时原地保留并指向 `specify migrate`；已落为 FR-013 的执行者裁定。
- Q: A-7/FR-015 的「新位置含非空内容」如何对待忽略生成物与安装器占位？ → A: 冲突判定只统计各存储的权威条目；机器可再生且被忽略的生成物（如 `.specify/tools/*.json`）与安装器播种占位/锚点不构成冲突内容，迁移照常执行且不覆盖、不删除它们；已落为 A-7 的口径句与 FR-015 的引用。
- Q: A-16 的「Runtime Store」词汇表条目何时落地、如何确认？ → A: 实现阶段产出提议文本并留在 run 证据/笔记；未经用户确认不写入 `.specify/glossary.md`；FR-021 的既有活路径更新先行；无验收标准依赖该词条，无人值守运行不因等待确认而阻塞。

### Session 2026-11-25（无人值守 tasks 阶段，用户追加要求：不兼容变更的迁移闭包）

**原始追加（逐字）**：

> 需要将所有不向前兼容的修改都在speckit.migrate命令中添加迁移逻辑

- Q: 「不向前兼容的修改」如何解读？ → A: 读作**向后不兼容变更**（backward-incompatible change）：使既有工作区在新版本下的路径或行为不再成立的变更。逐项为 Store Inventory 的 14 个迁移行、容器退役、`draft/` 退役、tools 记录/清单分裂、包内种子命名空间改名（`memory/` → `seed/`）与 migrate 维度集扩展（五 token 闭集 → 六 token）。解读落为 FR-027 与 SC-009，不重编号既有 FR/SC。
- Q: 哪些变更必须由 `/speckit.migrate` 承担？ → A: 凡涉及工作区状态的变更（存储路径、容器、记录/清单分裂）都由 `store-layout` 维度执行（`migrate:relocate` / `migrate:container-pass`）或按 M-5 封闭词表确定性拒绝；不进入任何工作区的包内资产命名空间以 `no-workspace-object` 登记，其工作区可见后果由对应的 store 行与全新初始化夹具覆盖。两类都不允许以运行时双路径回退或人工操作说明替代（与 A-8、FR-013 的执行者裁定一致且更严格）。
- Q: 迁移不安全的形态如何处理？ → A: 复用 M-5 的封闭拒绝词表（`dual-content`、`unknown-residue`、`symlink-source`、`symlink-target`、`permission-denied`、`path-collision:<relpath>`）；拒绝是终态（run `blocked`，exit 3），数据原地保留、两侧路径点名，不回退、不静默跳过、不以「新建空存储」冒充成功。
- Q: 与 097 既有结构的衔接？ → A: 不新建迁移引擎；第六维 `store-layout` 复用既有 plan → apply → archive-first → 回执；旧 v1 回执继续作为续跑输入（`compatibility-bridge`），两个 097 维度 pin 测试改为「前缀保持 + 六 token 全集」守卫（M-1 / M-6 / M-10）。
