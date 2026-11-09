# Requirements Specification: Non-Disposable（不可一次性处置）

**Requirement Branch**: `092-non-disposable`
**Created**: 2026-11-09
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -

**Input**: 用户原话要点：「在 speckit 框架中引入『Non-Disposable』理念——任何过程和文档都不应是『用过即丢』(use and throw)，需要时常回顾和修正，过去的历史是重要参考；要设计一系列机制，杜绝『这个没用了但是留在这里』『这个过时了但是我现在不想删除』这类把问题推到将来的行为。落点是 `/speckit.history` 命令：执行时先回顾历史 → 设计给出方案 → 向用户确认是否执行。历史回顾的对象是**当前 git HEAD 工作树里 `.specify/` 下记录的历史文件，而不是 git history**；范围包含 `.specify/{archive,derive,goal,history,memory,project,review,specs,state,teams}/*`。这是浩大工程，开发与后续修复都要用 team + 大并发 subagent。」

## Related Feature

**Feature ID**: 092
**Feature Name**: Non-Disposable（不可一次性处置）

## Overview

框架里已有一批「记录不变量」的载体：规格目录、状态脊、验证记录、特性注册表、决定台账、历史蒸馏、回顾报告、证据文件。它们各自与**生成它的那一刻**对齐，却没有机制让它们与**后来的事实**对齐。于是三种退化在无人察觉处累积，而它们的共同形态都是「把问题推到将来」：

1. **取代而未回收**：后出的特性取代了先出特性的正文/守卫/证据路径，先出的那一份仍然以「当前有效」的姿态留在树上（`086` 的 C-016 仍要求字节一致，而 `089` 已把该契约改成声明式投射；`085` 的契约仍写四部分 checkpoint，而 owner 已写五部分）。
2. **一事实上多 owner**：同一个事实/常量/计数在多处各自定义，读数彼此漂移（分解上限有 40 / 60 / 80 / 30 / 120 五个值；指令预算链记 37888 而常量为 38400；宪法条数在计划里陈旧复制）。
3. **状态不可被机器读**：注册表说 `Implemented`，闭环引擎却说 `block`；`verification.md` 没有机器可读的状态块，于是「已实现」与「被阻断」并存且无人报红。

本特性引入 **Non-Disposable 理念**：任何过程与文档都不是用过即丢，历史是必读输入；同时把「过期 / 无用 / 延期」从一种**沉默的默认状态**变成一种**必须被处置的状态**——每种此类状态 MUST 落入一个封闭处置集（归档 / 取代 / 修正 / 显式豁免含到期条件），而「留在原处、什么都不做」不再是可选项。

落点是 `/speckit.history`：它从「把会话蒸馏成主题文档」升级为「**回顾 → 设计 → 用户确认 → 执行**」的四段形态。回顾面不是 git 历史，而是**当前 HEAD 工作树里十个 `.specify/` 历史目录**；其中既有确定性的机械检出（可判定的结构/引用/计数命题），也有语义检出（取代关系、多 owner、延期措辞），后者由 team 的大并发 subagent 承担。修复 lane 消费 `.specify/specs/092-non-disposable/notes/input-review-080-090.md` 的 A–H 语料：这些检出必须能在本树上**复现**这些发现，并在修复 lane 跑完后把它们驱动到零。

本特性不新建第二套历史存储、第二个 `/speckit.history` 入口、第二套并发机制，也不把 A–H 修复做成一次性清理脚本；机制先于清单。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 历史回顾报出「过期却仍活着」的正文（Priority: P1）

用户在一棵已经前行了很多个特性的树上执行 `/speckit.history`。命令先做回顾：它只读当前工作树的 `.specify/`，把十个历史目录纳入范围，并且**不读 git 历史**（不看 commit、不 blame、不 diff 旧版本）。回顾产出一份 **Non-Disposable 报告**：每一条被判定为「过期 / 无用 / 延期」的条目携带其位置（文件:行）、检测类别、触发它的证据、严重度与**建议处置**。

**Why this priority**: 这是理念的可见面。没有一条能被复现的报告，机制无从验证，用户也无从确认；用户原话的落点正是这条命令。

**Independent Test**: 在一棵包含已知取代关系的副本树上执行命令的回顾动作，断言报告里出现该取代关系对应的条目（点名后出实现的正文路径与前出实现的契约文件），且报告条目全部可被逐条定位到 `文件:行`。

**Acceptance Scenarios**:

1. **Given** 一棵 HEAD 工作树中存在「后出特性已取代先出特性的契约」的树，**When** 执行回顾，**Then** 报告含一条 `superseded-live` 类条目，点名两处路径与行号，并给出「归档 / 取代 / 修正 / 豁免」中的建议处置。
2. **Given** 同一棵树上还存在 git 历史里才能看见的旧措辞，**When** 执行回顾，**Then** 该旧措辞不产生任何条目（回顾面不含 git 历史），且报告自述其扫描根集合恰为十个 `.specify/` 历史目录。
3. **Given** 回顾已完成，**When** 读取报告的机器可读形态，**Then** 每条条目含文档定义的固定字段集，且报告带一次覆盖声明（扫描了多少候选、哪些被排除及理由）。

---

### User Story 2 - 「没用了但留着」与「过时了但不想删」都必须被处置（Priority: P1）

用户（或 agent）此前可以把一个过时条目留在原处、不记录任何决定。本特性之后，每一条被判定为过期/无用/延期的条目 MUST 落入封闭处置集之一：**归档**（移入 `.specify/archive/` 并留下指针）、**取代**（由新载体承担，旧载体被标记为被取代并指向新载体）、**修正**（就地改正正文），或**显式豁免**（写下理由 + 到期条件/复核时点）。**「留在原处什么都不做」不是处置**，也无法被记录成处置。

**Why this priority**: 这是理念的核心机制。没有强制处置，回顾只是一份可以永远不理的报告——正是用户要杜绝的行为。

**Independent Test**: 在副本树上把一条条目的处置字段留空或写「原样保留」，断言校验报错并点名该条目；写入四种合法处置之一（豁免须带到期条件）后断言转绿。

**Acceptance Scenarios**:

1. **Given** 报告中的一条条目，**When** 其处置为空或未声明，**Then** 校验以非零退出码报红并点名该条目，报告不得被宣告为已闭合。
2. **Given** 同一条条目，**When** 处置为「豁免」但缺少理由或缺少到期条件，**Then** 校验报红并点名缺失的那一项（豁免不是逃生门）。
3. **Given** 同一条条目，**When** 处置为「豁免」且带理由、到期条件与复核时点，**Then** 校验转绿，该条目在到期条件不再成立时重新成为未处置条目。

---

### User Story 3 - 设计先行，执行要用户确认（Priority: P1）

回顾之后，命令给出**方案**（每类条目将如何处置、影响哪些路径、哪些步骤不可逆），然后**停下来等用户确认**；只有在用户确认之后才执行写盘。用户可以说「只做 A 组」「这批豁免」「先别动 D 组」。

**Why this priority**: 用户原话明确要求「向用户确认是否执行」。没有这道门，一次回顾就可能变成一次无授权的批量改写。

**Independent Test**: 在一棵有未处置条目的副本树上执行命令，断言回顾与方案产出后进程停下（无写盘，`git status --porcelain` 为空），且给出确认请求；在提供确认之后断言写盘发生；在拒绝/未确认时断言写盘不发生。

**Acceptance Scenarios**:

1. **Given** 一次回顾产出 N 条条目，**When** 命令进入方案段，**Then** 方案列出每条的拟处置与影响面，并以一次确认请求结束该段。
2. **Given** 用户在确认前中断，**When** 检查工作树，**Then** 工作树逐字节未变（零写盘），报告中不留「已执行」标记。
3. **Given** 用户只确认了部分分组，**When** 执行段运行，**Then** 只有被确认的分组被处置，未确认分组在报告中保持未处置状态且不被静默丢弃。

---

### User Story 4 - 取代协议：后出特性回收前出载体的全部落点（Priority: P1）

当一个特性取代另一个特性的正文、守卫或证据路径时，取代方 MUST 回收被取代方的**正文 / 守卫 / 证据路径**三类落点：被取代的正文被标记为已被取代并指向新载体，守护该旧行为的守卫被对应替换（旧守卫在旧正文被取代后不得继续要求旧行为），证据路径的旧拼写留有指针而非第二份真相。回收不完整 MUST 可被机械检出。

**Why this priority**: A–H 语料里 `B` 组（`B`/`C`/`H` 的重复形态）是本树最高频的系统性缺陷；只做报告不做协议，下一次取代仍会重演。

**Independent Test**: 在副本树上把某条契约改成与既有守卫相反的要求（模拟一次未回收的取代），断言检查报红并同时点名「旧守卫仍在要求旧行为」；把守卫同步替换后转绿。

**Acceptance Scenarios**:

1. **Given** 一处正文被判为被取代，**When** 运行回收检查，**Then** 该正文必须同时具备「被取代标记」与「指向新载体的指针」，缺任一即报红。
2. **Given** 一处正文被取代而其守卫仍是旧行为，**When** 运行回收检查，**Then** 报红并点名守卫文件与旧行为断言的位置。
3. **Given** 一处证据路径存在多种拼写，**When** 运行回收检查，**Then** 报红并列出全部拼写及其出处；只保留 owner 拼写 + 指针后转绿。

---

### User Story 5 - 单 owner 登记：同一事实只有一处定义（Priority: P2）

一个事实（含义、规则、阈值、枚举、配置值、计数）只允许一处定义（owner），其余位置一律为指针。多 owner MUST 可被机械检出，且检出的读物是「同一个名字/常量在多处被独立赋值或独立陈述」这一可判定形态，而不是人工比对。

**Why this priority**: `D` 组与 `F` 组都是它的实例。它是所有其它检测的底层前提：两处定义必然漂移，漂移必然在下游才暴露。

**Independent Test**: 在副本树上写出同一常量的第二个独立定义，断言检查报红并点名两处路径；把第二处改成指针后转绿。

**Acceptance Scenarios**:

1. **Given** 一个常量在两个文件里各自被赋值为不同的数，**When** 运行多 owner 检查，**Then** 报红并点名两处路径与两个值。
2. **Given** 同一事实被写成指针（引用 owner 路径 + 具名条目），**When** 运行同一检查，**Then** 不报红（指针不是第二定义点）。
3. **Given** 一个 owner 声明存在但该文件缺失，**When** 运行检查，**Then** 报红并点名悬空指针的目标。

---

### User Story 6 - 重编号协议：活绑定必须跟随，历史记录不得改写（Priority: P2）

当一个特性被重编号（或因编号冲突改号），它自身携带的**活绑定**（权威文件里的特性号、任务清单头部的需求号、团队目录名与 slug、契约头部声明的特性号、特性引用文件里的行）MUST 跟随新编号；而**历史记录**（证据文件、日期化回顾、`## Clarifications` 的既往写下的文字、`.specify/state/` 的既往记录）MUST NOT 被改写。二者的判据 MUST 可机械判定，残留的活绑定 MUST 可被检出。

**Why this priority**: `C` 组显示重编号残留会污染**另一个**特性的记录（`089` 的活任务指向 `086` 的注册行）。它是「过时但留着」最有破坏力的一种。

**Independent Test**: 在副本树上把某特性目录的活绑定改回旧编号，断言检查报红并点名该行；把一处历史记录改为新编号，断言检查报红为「改写了历史」。

**Acceptance Scenarios**:

1. **Given** 一份权威文件的活绑定指向与本目录编号不一致的特性号，**When** 运行重编号检查，**Then** 报红并点名该文件与行号。
2. **Given** 一条位于判据所定义的判据面之内的历史记录，**When** 其中出现与目录编号不一致的旧编号，**Then** 不报红（历史记录的旧编号是正当结果）。
3. **Given** 一条历史记录的内容被改写以「修正」旧编号，**When** 运行检查，**Then** 报红并点名该记录。

---

### User Story 7 - 状态与验证可被引擎读（Priority: P1）

一个特性的「已完成」宣称 MUST 能被闭环引擎读取并复核：`verification.md` 携带机器可读的逐条判据状态与 smoke 字段，注册表的行与闭环裁决一致。**「已实现但引擎判 block」是必须报红的矛盾状态**，而不是可被文字解释过去的差异。

**Why this priority**: `A` 组的两条 CRITICAL 都是它。它决定本特性自己的闭环是否可信——也是本特性验证其它特性的仪器。

**Independent Test**: 在副本树上把某特性的注册状态写成 `Implemented` 而其闭环裁决为 `block`，断言检查报红；补齐机器可读状态块使其裁决转绿后断言转绿。

**Acceptance Scenarios**:

1. **Given** 注册表行宣称 `Implemented`/`Ready for Review` 而闭环引擎返回 `block`，**When** 运行状态一致性检查，**Then** 报 `status-claims-implemented-but-blocked` 并点名该特性。
2. **Given** `verification.md` 缺少逐条判据状态或 smoke 字段，**When** 运行检查，**Then** 报红并点名缺失字段名。
3. **Given** 一份声称含闭集（count identity）的验证记录，**When** 该记录的算术恒等式不成立，**Then** 报红并给出两侧读数。

---

### User Story 8 - 大并发 subagent 由既有 team 机制承担（Priority: P2）

回顾的语义判定面很大（本树在十个历史目录下约有 4,345 个文件，其中约 1,900 份规格与状态文档、约 1,850 份证据文件），必须由 team 的大并发 subagent 承担。并发编排 MUST 复用既有 `085` 的 spec-local Temporary Goal/Team 与既有并发机制，MUST NOT 新建第二套并发或调度设施；每个 subagent 只读其分配的片，返回结构化的检出条目。

**Why this priority**: 用户明确要求 team + 大并发。但它是对 P1 的能力输送，缺了它 P1 只是慢，缺了 P1 则并发毫无意义。

**Independent Test**: 对一棵固定副本树跑一次分片回顾，断言并发派发数与配置声明的并发上限一致、每个 subagent 的分配片互不重叠且并集覆盖全部候选、单线程顺序执行得到同一条目集合（顺序无关性）。

**Acceptance Scenarios**:

1. **Given** 一次回顾被分片，**When** 派发完成，**Then** 各片的分区互不重叠、并集等于候选集合，且无片为空。
2. **Given** 同一次回顾以较低并发度重跑，**When** 比较两次的条目集合，**Then** 条目集合按名相同（不因并发度不同而产生不同结论）。
3. **Given** 某个 subagent 返回格式不合规，**When** 汇总，**Then** 该片被标记为「未评估」并在报告中可见，MUST NOT 被计为「无检出」。

---

### User Story 9 - 修复 lane 消费 A–H 语料并把检出驱动到零（Priority: P1）

确认之后执行段是一个**修复 lane**：它按用户确认的方案逐条处置，优先消费 `notes/input-review-080-090.md` 的 A–H 语料（八组、逐条带 `文件:行` 证据），而且每一次修复都留下可复核证据（修复前后两次检出读数、被改动路径清单、对应检测类别）。A–H 的每一条 MUST 在本特性中显式映射为「由哪条 FR/SC 覆盖」或「以何种理由排除」。

**Why this priority**: 用户明确把 A–H 定为验证用例，并要求「跑完后把它们驱动到零」。这是本特性唯一的客观验收底座。

**Independent Test**: 在修复 lane 跑之前记录一次检出读数（应按类别复现 A–H 的发现），跑之后记录第二次读数，断言目标目录的检出集合按名归零或落为带到期条件的豁免；两次读数与改动清单落盘到证据目录。

**Acceptance Scenarios**:

1. **Given** A–H 的八组语料，**When** 完成 A–H 映射表，**Then** 每一条都指向一条 FR/SC 或一条带理由的排除，零遗漏、零「未评估」。
2. **Given** 修复 lane 已跑完，**When** 在同一树上重跑回顾，**Then** 被处置类别的检出集合按名为空，或仅剩已登记豁免条目及其到期条件.
3. **Given** 一次修复动作，**When** 审阅其证据，**Then** 证据含修复前后读数、逐路径改动与对应语料条目编号，缺任一即该修复不成立。

---

### Edge Cases

- **空回顾面**：十个历史目录都为空时，回顾 MUST 报告「无候选」并以成功码结束，MUST NOT 因无输入而宣告 Clean（无输入不是干净）。
- **目录缺失**：十个目录之一不存在时，回顾 MUST 点名缺失目录并继续（不是静默跳过，也不是整体失败）。
- **报告未闭合却被宣称完成**：只要还有未处置条目，「本轮回顾已完成」MUST NOT 被宣告；「报告已产出」与「条目已处置」是两个独立结论。
- **豁免积累**：豁免条目本身会积累成新的仓库垃圾，故豁免 MUST 带复核时点；到期后重新进入未处置集合，不得静默续期。
- **回顾命令与写盘命令的边界**：回顾段与方案段 MUST 零写盘；只有执行段可写，并且只在用户确认之后。
- **语义判定被裁成确定性命中**：用「命中某个关键词」冒充「判定为过期」是误判源；语义条目 MUST 携带能独立复核的引用（两处路径 + 行号），不得只给结论。
- **修复 lane 需要改写他人已交付正文**：对既有 spec 正文、owner 文档与守卫的改动一律以用户确认为前提，并对被改动路径留下前后读数。
- **并发度可变**：并发度是可配置的运行参数，不是判据；判据是条目集合与覆盖声明。
- **同一事实两处都「看起来像 owner」**：由检测按可判定读物（独立赋值 / 独立陈述）判定，HARD 冲突交由用户裁定而非猜测。

## Requirements *(mandatory)*

### Functional Requirements

#### Non-Disposable 的机制层（US2/US1）

- **FR-001**: 框架 MUST 提供 Non-Disposable 的**唯一 owner 文档** `shared/definitions/non-disposable-definitions.md`（本仓运行时投影 `.specify/shared/definitions/non-disposable-definitions.md`），文件头部 MUST 声明它拥有的条目：理念定义、封闭处置集与豁免形态、检测类别的封闭集、回顾面定义、取代协议、重编号判据、报告 schema、与历史存储的边界。
- **FR-002**: 一个状态 MUST 被判为「过期 / 无用 / 延期」，当且仅当它满足 owner 文档中的可判定判据；判据 MUST 是有限项并可被程序或带引用的语义判定复算，MUST NOT 以「作者认为」或「读者感觉」为判据。
- **FR-003**: 每一条被判定的状态 MUST 落入**封闭处置集**之一：`archive`（移入归档并留指针）/ `supersede`（由新载体承担，旧载体标记被取代并指向新载体）/ `correct`（就地修正）/ `exempt`（显式豁免）。集合 MUST 只在 owner 文档中定义，其它位置引用它。
- **FR-004**: `exempt` MUST 同时携带**理由**与**到期条件或复核时点**，缺任一即处置不成立；到期条件不再成立时该条目 MUST 重新成为未处置条目。MUST NOT 存在「永久豁免」形态。
- **FR-005**: 「留在原处不做任何事」MUST NOT 表示为一个处置值，也 MUST NOT 被默认为闭合；未声明处置的条目 MUST 被检出并以非零退出码报出。
- **FR-006**: 框架 MUST 提供一个**只读、确定性**的检出引擎，覆盖可判定的检测类别（文档结构/引用/计数/状态字段/路径拼写/常量重复/重编号活绑定），输出人读与机器可读两种形态，退出码 MUST 区分「无检出」「存在检出」「参数或环境错误」三类。
- **FR-007**: 检出引擎 MUST 输出一次**覆盖声明**：扫描根集合、候选计数、被排除项及其理由；「什么都没扫到于是全绿」MUST NOT 出现——空候选与全绿 MUST 是不同结论。

#### 取代协议（US4）

- **FR-008**: 当一个特性取代另一个特性的正文、守卫或证据路径时，取代方 MUST 回收被取代方的**三类落点**：正文（标记被取代 + 指向新载体）、守卫（旧行为的守护断言被替换或被删除）、证据路径（旧拼写留有指针，不保留第二份真相）。
- **FR-009**: 回收不完整 MUST 可被机械检出：一条被标记为被取代的正文，若其守卫仍要求旧行为、或其证据路径存在第二种拼写、或缺「指向新载体」的指针，检查 MUST 报红并点名路径与行号。
- **FR-010**: 取代 MUST 被记录在 owner 文档规定的登记形态中（被取代项 → 取代项 → 处置 → 证据路径），且登记 MUST 可被检出引擎读取；MUST NOT 只存在于 commit message 或会话记录里。

#### 单 owner 登记（US5）

- **FR-011**: 一个事实（含义、规则、阈值、枚举、配置值、计数）MUST 只有一处定义（owner），其余位置 MUST 为指针（引用 owner 路径与具名条目），MUST NOT 各自复写。
- **FR-012**: 多 owner MUST 可被机械检出，判据 MUST 落在可判定读物上（同一名字/常量在给定轴上下文中被独立赋值或独立陈述），MUST NOT 依赖「两份文本读起来像不像」的人工判断。
- **FR-013**: 检出 MUST 区分**内容重复**（第二份定义，MUST 报红）与**合法重复**（机器再生成的副本、测试内 pin 的字面量、带日期的记录），后者 MUST 由 owner 文档点名的封闭清单定义，不是自由裁量。
- **FR-014**: 指针 MUST 可解析：指向的 owner 路径不存在或指向的具名条目不存在时，检查 MUST 报红并点名悬空指针。

#### 重编号协议（US6）

- **FR-015**: **活绑定**（权威文件中的特性号、任务清单头部的需求号/特性号、团队目录名与 slug、契约头部声明的特性号、特性引用文件的行、注册表行）MUST 跟随目录的实际编号；出现不一致 MUST 被检出并点名文件与行号。
- **FR-016**: **历史记录**（`test-evidence/`、日期化回顾报告、`## Clarifications` 中的既往文字、`.specify/state/` 的既往记录）MUST NOT 被改写以迁就新编号；对它们的改写 MUST 被检出。
- **FR-017**: 活绑定与历史记录的**判据面** MUST 在 owner 文档中封闭列举（按路径与按章节位置），MUST NOT 由「看起来像历史」推断。

#### 状态与验证的机器可读契约（US7）

- **FR-018**: 一个特性的 `verification.md` MUST 携带机器可读的逐条判据状态与 smoke 字段，字段名与取值域由既有 owner（`shared/workflow/acceptance-hardening.md` § Verification Vocabulary）拥有，本特性 MUST 引用而不复写。
- **FR-019**: 注册表状态与闭环裁决 MUST 一致；宣称 `Implemented` / `Ready for Review` 而闭环裁决为 `block` MUST 被检出为矛盾状态并点名该特性（复用既有 reason code `status-claims-implemented-but-blocked`）。
- **FR-020**: 一份声称含闭集恒等式（如 `applicable + exempt == candidates`）的验证记录，当恒等式两侧读数不成立时 MUST 被检出并给出两侧读数；MUST NOT 存在「声明了闭集却无人复算」的验证条目。
- **FR-021**: 状态一致性检查 MUST 复用既有闭环引擎的裁决与 reason code 词表，MUST NOT 在检出引擎中重建第二套裁决逻辑或第二套 reason 词表。

#### 命令执行形态：回顾 → 设计 → 确认 → 执行（US1/US3）

- **FR-022**: `/speckit.history` 的执行形态 MUST 是四段：**回顾 → 设计（方案）→ 用户确认 → 执行**。回顾与方案段 MUST 零写盘；执行段 MUST 只在用户确认之后发生。
- **FR-023**: 回顾面 MUST 恰为当前 HEAD 工作树中 `.specify/{archive,derive,goal,history,memory,project,review,specs,state,teams}` 十个目录下的文件；MUST NOT 读取 git 历史（commit / blame / 旧版本 diff）作为回顾输入；MUST NOT 以「git 历史里也有」作为条目来源。
- **FR-024**: 回顾 MUST NOT 扩大或缩小到该十目录之外；范围 MUST 由一份声明式的根集合定义（与既有事实声明层同构），MUST NOT 由散落在提示文本里的目录名清单决定。
- **FR-025**: 方案段 MUST 逐条给出拟处置、影响路径、可逆性，并以一次确认请求结束该段；确认 MUST 支持部分确认（按分组或按条目），未确认项 MUST 保持未处置并可见。
- **FR-026**: 命令的既有能力（把当前工具的会话历史蒸馏为主题聚合知识库、增量 manifest）MUST 保留为回顾/执行面的一部分，MUST NOT 被移除或另立第二个入口。
- **FR-027**: 命令 MUST NOT 新建第二套历史存储；蒸馏产物仍归 `.specify/history/` 所有，本特性只**读取**它作为回顾输入之一，并新增「回顾/方案/处置」三段产物。
- **FR-028**: `/speckit.history` MUST NOT 成为「批量改写他人已交付正文」的旁路：任何对既有 spec 正文、owner 文档或守卫的改动 MUST 属于用户确认的方案条目，并 MUST 留下前后读数证据。

#### team / 大并发编排义务（US8）

- **FR-029**: 回顾的语义判定面 MUST 由 team 的大并发 subagent 承担；编排 MUST 复用既有 `085` 的 spec-local Temporary Goal/Team 与既有并发机制，MUST NOT 新建第二套 team/并发/调度设施。
- **FR-030**: 每个 subagent MUST 只读其被分配的片，MUST 返回 owner 文档定义的固定字段集的结构化条目；分配 MUST 互不重叠且并集覆盖候选集合。
- **FR-031**: subagent 返回不合规时，该片 MUST 被标记为「未评估」并在报告中可见；MUST NOT 被计为「无检出」（未评估不等于干净）。
- **FR-032**: 回顾结果 MUST 与并发度无关：同一棵树上不同并发度 MUST 得到按名相同的条目集合。

#### 修复 lane（US9）

- **FR-033**: 执行段 MUST 是一个**修复 lane**：按用户确认的方案逐条处置，MUST NOT 是「一次性清理脚本」——处置动作只经由 owner 文档定义的处置途径执行，MUST NOT 引入一条独立的批量删除/批量改写通道。
- **FR-034**: 修复 lane MUST 优先消费 `notes/input-review-080-090.md` 的 A–H 八组语料，且每一条语料 MUST 在规格内显式映射为一条 FR/SC 或一条带理由的排除；MUST NOT 存在未映射条目。
- **FR-035**: 每一次修复 MUST 留下可复核证据：修复前后两次检出读数、被改动路径清单、对应语料条目编号、以及该改动的处置类别；缺任一项该修复 MUST 被判为不成立。
- **FR-036**: 修复 lane 结束后，被处置类别的检出集合 MUST 按名为空，或仅剩已登记豁免及其到期条件；MUST NOT 以「已被人工看过」作为归零依据。
- **FR-037**: 修复 lane MUST 保持历史证据不被删除：归档而非删除（`archive-not-delete`），被取代正文保留其旧文本并加被取代标记。

#### 落点与复用（A1–A3 裁定、A20）

- **FR-038**: 本特性的机制 MUST 复用既有面：历史蒸馏入口 `manage-history`、材料卫生引擎 `sanitize-utils.py`、闭环裁决 `closure-acceptance-check.py`、特性注册表 reconcile、并发 team 机制；MUST NOT 建造第二套 history 入口或第二套存储。
- **FR-039**: 检出引擎的确定性部分 MUST 落在 `scripts/python/` 下的新增只读单文件引擎（与 `sanitize-utils.py` / `closure-acceptance-check.py` 同形态：argparse、只读、退出码 0/1/2、stdout 人读 + `--json` 机器读），并由既有镜像机制生成 `.specify/scripts/python/` 投影。
- **FR-040**: 本特性的验证守卫 MUST 落在既有 `pytest -m contract` 集合内（新增契约测试文件），MUST NOT 新增独立的确认门或独立门禁步骤。
- **FR-041**: 本理念中需要成为**原则**的部分（见 A3）MUST 按既有五处落点同时落地：`templates/constitution-template.md`、本仓 `.specify/memory/constitution.md`、`templates/instructions-template.md` + `.specify/instructions.md` 的常驻段落、`skills/internal/manage-constitution/SKILL.md` 的 `MUST include` 清单、以及双落地守卫的计数 pin（`tests/contract/test_constitution_double_landing.py` 的 template / live / mandate 三计数与 watchlist，`tests/contract/test_fast_fail_discipline.py` 的同批 pin），并产出 Sync Impact Report（MINOR 递增）。

### Key Entities *(include if data involved)*

- **Non-Disposable 状态（Non-Disposable State）**：一个被判定为「过期 / 无用 / 延期」的载体或其局部；属性为位置（文件:行）、检测类别、证据引用、严重度、处置、处置证据路径、到期条件（仅 `exempt`）。
- **处置（Disposition）**：封闭集 `archive` / `supersede` / `correct` / `exempt` 的成员；它是「状态已闭合」的唯一凭据，缺它则该状态仍然开着。
- **检出类别（Detection Category）**：封闭集，至少含 `superseded-live`（被取代仍活）、`multi-owner`（多 owner）、`renumber-live-binding`（重编号活绑定残留）、`status-unreadable`（状态不可读）、`false-closed-set`（闭集恒等式不成立）、`stale-constant`（常量/计数漂移）、`orphan-path`（路径拼写残留/不存在路径）、`deferral-marker`（延期措辞与无到期条件的留存）。成员集只在 owner 文档中定义。
- **回顾面（Review Surface）**：十个 `.specify/` 历史目录的声明式根集合；它是回顾的唯一输入范围，且不含 git 历史。
- **Non-Disposable 报告（NDR）**：回顾的产物；含条目列表、覆盖声明、按类别的计数、未评估片标记；机器可读形态承载核对与闭合判定。
- **修复 lane 证据（Repair Evidence）**：一次处置的前后读数、改动路径、语料编号与处置类别；它是「修复成立」的判据。
- **A–H 映射表（Corpus Mapping）**：`notes/input-review-080-090.md` 八组条目到 FR/SC 或排除理由的显式映射。

### Runtime Stack & Dependency Ownership

本特性不新增运行时依赖：检出引擎、状态一致性与历史蒸馏消费的都是既有框架已声明的解释器与既有引擎；并发面复用既有 team 机制。`Premises` 指向 plan 阶段将定义的执行前提（同 `090` 的 EP 惯例）。

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|----|----------|
| RS-001 | Python 3 解释器（运行检出引擎、状态一致性与既有镜像/闭环引擎） | signed-contract | CPython 上游（本仓只消费） | `requires-python = ">=3.8"`（`pyproject.toml` 既有声明；本特性零新增第三方依赖） | `pyproject.toml` | 新增检出引擎与契约测试在 `>=3.8` 解释器上通过；本特性零新增 import | FR-006, FR-039 | EP-001 |
| RS-002 | pytest 契约测试运行器（承载 FR-040 的守卫） | signed-contract | pytest 上游（本仓只消费） | 以 closure 比较时刻实测 `python3 -m pytest --version` 为准（`090` 记录 2026-11-09 为 `pytest 9.0.3`） | `scripts/bash/run-tests.sh` | `pytest -m contract` 在冻结基线上零新增失败（基线 = 失败 node-id 集合） | FR-040 | EP-001 |
| RS-003 | 既有闭环裁决引擎（`closure-acceptance-check.py` 的 verdict 与 reason code 词表） | signed-contract | 既有 owner `shared/workflow/acceptance-hardening.md` § Closure Verdict | 以该引擎的退出码与 `--json` 输出为读数 | `shared/workflow/acceptance-hardening.md` | 状态一致性检查在 `Implemented` 但对 `block` 的副本树上判红，在两者一致时判绿 | FR-019, FR-021 | EP-002 |
| RS-004 | 既有材料卫生引擎（`sanitize-utils.py` 的类别/处置/台账词汇） | signed-contract | 既有 owner（Feature 047 契约 `045-sanitize-command`） | 其 `CATEGORIES` / `DISPOSITIONS` / `STATES` 字面为其自身 owner，本特性按指针引用 | `.specify/specs/045-sanitize-command/contracts/sanitize-findings.md` | 本特性处置词汇与 sanitize 台账的一致性由一次联合比对取证（相同写作不同写作 MUST 被阐明） | FR-038 | EP-003 |
| RS-005 | 既有 spec-local Temporary Goal/Team 与多 agent 并发机制 | signed-contract | 既有 owner（Feature 085 契约） | 以 `085` 契约的 roster/并发上限声明为读数 | `.specify/specs/085-sdd-temporary-goal-team/contracts/concurrency-and-worktrees.md` | 一次分片回顾的派发数 ≤ 声明的并发上限，分区并集覆盖候选集合 | FR-029, FR-030 | EP-004 |
| RS-006 | 检出引擎（本特性交付的只读确定性能力） | in-scope | 本特性 | — | 本特性 `contracts/`（plan 阶段定义） | 检出引擎在 A–H 语料树上复现各检测类别的发现 | FR-006, FR-007 | EP-001 |
| RS-007 | 回顾→方案→确认→执行 的命令形态（`/speckit.history` 新执行段） | in-scope | 本特性 | — | 本特性 `contracts/`（plan 阶段定义） | 回顾段与方案段零写盘、未确认不执行，由契约测试取证 | FR-022, FR-025 | EP-001 |

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在 `notes/input-review-080-090.md` 的 A–H 语料树上，检出引擎对每一组的发现**可被复现**：A–H 映射表 100% 条目有对应检出或显式排除理由，逐组给出检出读数（条目数、类别、路径）。 **Path**: final
- **SC-002**: 回顾面恰为十个 `.specify/` 历史目录，且回顾不消费 git 历史：注入只在 git 历史中存在的旧措辞后，条目集合按名不变；目录之一缺失时报点名该目录且不静默跳过。 **Path**: final
- **SC-003**: 任一条目若处置为空、或 `exempt` 缺理由缺到期条件，校验以非零退出码报红并点名该条目；四条合法处置（含带到期条件的 `exempt`）全部转绿；「原样保留」不被接受为处置值。 **Path**: final
- **SC-004**: 回顾段与方案段零写盘：在一次有未处置条目的运行中，回顾与方案结束后的 `git status --porcelain` 为空；用户未确认时执行段不发生；用户确认后才发生写盘。 **Path**: final
- **SC-005**: 取代回收可被机械证伪：把一条契约改为与既有守卫相反的要求（未回收的取代）后检查报红并同时点名正文与守卫；同步回收后转绿；三种落点（正文/守卫/证据路径）各有至少一次变异腿。 **Path**: final
- **SC-006**: 多 owner 可被机械检出：注入同一常量的第二个独立定义后检查报红并点名两处与两个值；改成指针后转绿；指针悬空时报红并点名目标。 **Path**: final
- **SC-007**: 重编号协议双向可判：活绑定残留（任务头部/契约头部/团队 slug/特性引用）各报红并点名行号；历史记录中的旧编号不报红；被改写的判据面内历史记录报红。 **Path**: final
- **SC-008**: 状态矛盾被检出：注册表 `Implemented` 而闭环 `block` 时报 `status-claims-implemented-but-blocked`；`verification.md` 缺机器可读状态块或 smoke 字段时报红并点名缺失字段；闭集恒等式不成立时给出两侧读数。 **Path**: final
- **SC-009**: 分片回顾的分区互不重叠且并集覆盖候选集合；不同并发度两次运行得到按名相同的条目集合；一个返回不合规的片被标为「未评估」且不计为干净。 **Path**: final
- **SC-010**: 修复 lane 后重跑同一组检出：被处置类别按名归零或仅剩已登记豁免及其到期条件；每次修复的证据含前后读数、改动路径、语料编号与处置类别，缺任一即该修复不成立。 **Path**: final
- **SC-011**: 本理念的宪法原则按五处落点同批落地并产出 Sync Impact Report（MINOR 递增）；双落地守卫的三条计数 pin 与 watchlist、fast-fail 守卫的 pin 同批移动并有契约测试守护。 **Path**: final
- **SC-012**: 无第二个 history 入口、无第二套历史存储、无第二套并发机制：一次结构检查证明 `manage-history` 仍是唯一蒸馏入口、`.specify/history/` 仍是唯一蒸馏存储、team 机制仍是唯一并发面。 **Path**: supporting
- **SC-013**: 检出引擎与契约测试的既有行为零回归：`pytest -m contract` 与 `pytest -m integration` 相对冻结基线（失败 node-id 集合）零新增失败。 **Path**: supporting
- **SC-014**: 十个历史目录在回顾范围内被完整覆盖：覆盖声明给出的候选计数与一次独立枚举的逐目录计数一致（本阶段实测基线约 `4,345` 个文件；基线是参照物不是阈值）。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 检出引擎对 A–H 语料树的逐组 `--json` 输出（类别、路径、行号、严重度）；A–H 映射表与其检出读数的对照表落盘 `test-evidence/`；每组至少一次运行记录命令、退出码与命中行。
- **SC-002 Source**: 两次运行的条目集合差集（`comm -13` / `comm -23` 风格按名比较）：一次在原树、一次在注入了仅在 git 历史中存在的旧措辞的副本树；另一次在删除一个十目录之一的副本树上读点名行；两次读数落盘 `test-evidence/`。
- **SC-003 Source**: 对副本树报告中处置字段的变异实验（留空 / `exempt` 缺理由 / `exempt` 缺到期条件 / 四种合法处置），逐次读校验退出码与点名行，落盘 `test-evidence/`。
- **SC-004 Source**: 每次运行前后 `git status --porcelain` 与受管目录文件哈希快照；分别在回顾结束、方案结束、确认后三个时点各取一次快照，三次快照落盘并逐字比较。
- **SC-005 Source**: 三条副本树变异腿（正文未标记被取代 / 守卫仍要求旧行为 / 证据路径出现第二种拼写），每条腿记录变异内容、检查退出码、点名行，落盘 `test-evidence/`。
- **SC-006 Source**: 副本树中注入常量第二定义、改成指针、制造悬空指针三次变异前后的检查 `--json` 输出对比，落盘 `test-evidence/`。
- **SC-007 Source**: 四类活绑定各一次变异 + 判据面内历史记录各一次变异（旧编号保留、被改写），读检查退出码与点名行，落盘 `test-evidence/`。
- **SC-008 Source**: `closure-acceptance-check.py --json` 的 `verdict` / `reasons` 与注册表行的对照读数；`verification.md` 字段扫描的缺失字段清单；闭集恒等式两侧的实计数器读数；三者分开记录，MUST NOT 合并成一句「状态一致」。
- **SC-009 Source**: 一次分片回顾的分区清单（片 → 路径集合）与候选集合的差集；两次不同并发度的条目集合差集；一片不合规注入后的「未评估」标记读数；落盘 `test-evidence/`。
- **SC-010 Source**: 修复 lane 前后两次检出引擎的 `--json` 输出按名差集；每次修复的证据包（前后读数、改动路径清单 `git diff --name-only` 范围、语料编号、处置类别）落盘 `test-evidence/`。
- **SC-011 Source**: 修订提交中的宪法 diff（版本行、Sync Impact Report、Last Amended）、指令面段落、`MUST include` 清单条目；`test_constitution_double_landing.py` 与 `test_fast_fail_discipline.py` 的 pin 读数（template / live / mandate / watchlist 与 fast-fail 计数）逐一记录。
- **SC-012 Source**: 一次结构检索的读数：`manage-history` 的入口唯一性、`.specify/history/` 作为唯一蒸馏存储、team 机制的唯一性；检索命令与命中清单落盘 `test-evidence/`。
- **SC-013 Source**: `pytest -m contract` 与 `pytest -m integration` 的失败 node-id 集合，与冻结基线按名比较（`comm -13` / `comm -23` 两向），两向皆空即零新增失败；读数落盘 `test-evidence/`。
- **SC-014 Source**: 覆盖声明的候选计数与一次独立枚举（逐目录 `find`/`rglob` 计数）的对照表；逐目录计数落盘 `test-evidence/`，基线计数注明测量时点。

## Boundary and Ownership (non-duplication)

- **本特性拥有**：Non-Disposable 理念的定义、封闭处置集与豁免形态、检出类别封闭集、回顾面定义、取代协议、重编号的活绑定/历史记录判据面、Non-Disposable 报告 schema、检查入口的判定。
- **本特性引用而不拥有**：One Source of Truth（指针纪律）、Fast Fail（异常上送）、Confirmation Gates（确认门分类）、Directory Governance（目录登记）、Single-Run Evidence（证据捕获）、Concurrent Development Safety（记录一文一件）、接受性硬化/闭环裁决（`shared/workflow/acceptance-hardening.md` § Verification Vocabulary 与 Closure Verdict）、测试执行效率（`shared/guidelines/test-execution-efficiency.md`）、脚本接口契约（`shared/definitions/script-interface-definitions.md`）、Re-Anchoring（`shared/definitions/re-anchoring-definitions.md`）。上述纪律的判据全部由其 owner 文档拥有，本特性只按路径引用。
- **本特性不拥有**：sanitize 的材料卫生类别与台账 schema（Feature 047）、闭环裁决的 reason code 词表（接受性硬化 owner）、team 与并发机制的实现（Feature 085）、历史蒸馏的 manifest schema（`shared/declarations/facts/history-manifest-schema.yaml`）、特性注册表的手工编辑权（`/speckit.feature` 与 `AGENTS.md` 的 ID Register 纪律）。
- **与既有落点的边界**：`sanitize-utils.py` 处理「材料卫生」（死引用、索引一致、断裂符号链接、镜像漂移、冗余）并可执行 `delete`；本特性处理「语义过期 / 多 owner / 重编号 / 状态可读性」，处置以 `archive` / `supersede` / `correct` / `exempt` 为主，二者的类别与处置**不得互相替代**（见 A20）。

## Assumptions

- **A1 — 特性类别判定**：本特性判为 `execution`（`Flow Type: -`）。验收 oracle 是「交付物被机器执行/解析/消费」：检出引擎、状态一致性检查、命令的四段形态与并发分片都以程序读数判定；其中可读性产物（报告、方案）虽为文档形态，其缺陷只在程序判定失效时暴露，故不判 `expression`。
- **A2 — 复用/扩展 vs 新建（裁定，非待决项）**：只读调查（本阶段实测：`skills/internal/manage-history/SKILL.md` 123 行，六步工作流 + Safety Rules；`templates/commands/history.md` 52 行，仅保留入口与 wrap-up；`sanitize-utils.py` 的 `CATEGORIES` 六项 / `DISPOSITIONS` 五项 / `STATES` 三项；`closure-acceptance-check.py` 的七条封闭 reason set；`history-utils.py` 的 `MANIFEST_FACT = "history-manifest-schema"`；`account-clause-coverage.py` 的 `--freeze` 基线形态；`flow-class-check.py` / `workspace-guard.py` 的只读门形态）得出裁定：**扩展 `manage-history` 为回顾段的语义引擎；新建一个只读确定性检出引擎承载可判定部分；复用 `sanitize-utils.py` 仅作为材料卫生类别与台账词汇的既有 owner（不把语义过期塞进 sanitize）；复用 `closure-acceptance-check.py` 的裁决与 reason code；复用 `085` 的 team/并发机制**。理由：`manage-history` 已经是 `/speckit.history` 的唯一执行内核，新建第二个 history 入口会立刻制造本特性自己要消灭的「一事实两 owner」；而把语义过期塞进 sanitize 会让 sanitize 的封闭类别集与其契约漂移。**MUST NOT 建第二个 history 入口或第二套存储。**
- **A3 — 理念落地为宪法原则（裁定）**：本理念中「不可一次性处置」的**规范性条款**（过期/无用/延期状态 MUST 有封闭处置、回顾 MUST 先于设计且执行 MUST 经用户确认、历史 MUST 以 HEAD 工作树为面且 MUST NOT 改写）MUST 成为一条新增宪法原则，按既有五处落点同批落地：`templates/constitution-template.md`、本仓 `.specify/memory/constitution.md`、`templates/instructions-template.md` + `.specify/instructions.md` 常驻段落、`skills/internal/manage-constitution/SKILL.md` 的 `MUST include` 清单、以及双落地守卫的计数 pin（`test_constitution_double_landing.py` 的 template / live / mandate 三计数 + watchlist，`test_fast_fail_discipline.py` 的同批 pin）。按本仓 v1.19.0（22 条）与既有修订记录（MINOR 递增、Sync Impact Report、Last Amended），新增一条为 MINOR 增量；**具体条号与 pin 数值由 plan/implement 阶段在提交时实测确定，本阶段 MUST NOT 预写数值**（预写就是第二个定义点）。模板与本仓的条号天然不同（`090` 已把该差异裁定为正当差异，不「修齐」）。
- **A4 — 回顾面与 git 历史的分界**：回顾只读 HEAD 工作树。判据是「文件是否存在于当前工作树」；同一文本若只存在于 git 历史，不构成回顾输入，也不构成检出条目。「历史」在本特性中指**载体自身的记录属性**（日期化回顾、证据文件、状态脊、既往澄清文字），不是版本控制的历史。
- **A5 — 十目录作为声明式根集合**：十个目录名 MUST 落在与既有事实声明层同构的声明文件中（`shared/declarations/facts/` 惯例），MUST NOT 在每个提示文本里各写一份；目录增删只改声明。
- **A6 — 范围实测基线（参照物，不是阈值）**：本阶段在仓库根实测 `.specify/` 十个历史目录合计 **4,345** 个文件：`archive` 66、`derive` 2、`goal` 55、`history` 7、`memory` 1,210、`project` 10、`review` 1、`specs` 2,893、`state` 27、`teams` 74。其中 `.md` 约 2,500 份、证据类（`test-evidence/`、`.jsonl`/`.txt`/`.json`）约 1,850 份。该规模是「必须 team + 大并发」的量化依据；SC-014 的对照以测量时点为准，基线漂移不构成失败。
- **A7 — 并发度是运行参数不是判据**：用户要求「大并发」，但并发度的具体值属于运行配置（既有 `085` 机制声明）；本特性的判据是分区的完备性、条目集合的并发无关性与「未评估」的可见性。
- **A8 — 检出类别封闭集（当前定义，可扩展的唯一方式是改 owner）**：`superseded-live`、`multi-owner`、`renumber-live-binding`、`status-unreadable`、`false-closed-set`、`stale-constant`、`orphan-path`、`deferral-marker`。新增类别 MUST 修订 owner 文档，MUST NOT 在实现里就地追加。
- **A9 — 处置与 sanitize 处置词汇的关系（待 plan 裁决的一致性问题）**：`sanitize-utils.py` 的 `DISPOSITIONS` 为 `delete / archive / repair / delegate / dismiss`，本特性为 `archive / supersede / correct / exempt`。两者是不同封闭集（前者约束材料卫生、可执行且不可逆；后者约束语义过期、以归档与指针为主）。本阶段裁定**不合并**（合并会改写 sanitize 已交付的契约与台账），但二者的**映射与冲突消解** MUST 在 plan 阶段以一条 decision tension 显式裁定，MUST NOT 留成两套互不知情的词汇。
- **A10 — 豁免是有限期的**：`exempt` 到期后重新成为未处置条目是设计意图，不是缺陷。到期条件的形式（日期 / 事件 / 复核时点）由 owner 文档定义，本阶段不预写具体语法。
- **A11 — 「零」的含义**：SC-001 的「复现」与 SC-010 的「归零」都按**条目名**比较（路径 + 行 + 类别），不按计数比较；计数只作为参照物在测量源中记录。
- **A12 — 本阶段写入边界**：本阶段唯一写入对象是 `.specify/specs/092-non-disposable/requirements.md` 与本阶段门禁读数 `test-evidence/requirements-gates.txt`；MUST NOT 改动实现、模板、其它 spec 正文、状态脊以外的运行时文件；既有脏文件不提交不还原。
- **A13 — 状态脊与注册冲突的披露**：本线状态脊的 `direction_contract.goal_verbatim` 记录了用户原话，其中**未**出现宪法原则/五处落点要求；本规格在 A3 与 FR-041 中把该要求落为可执行条款。这是本阶段的一处**扩展裁定**，不是对原话的改写；若与编排者的意图不符，应在 clarify 阶段裁定而不是由实现自行取舍。
- **A14 — A–H 语料的权威位置**：语料是 `.specify/specs/092-non-disposable/notes/input-review-080-090.md`（日期化输入记录，拥有零规则）。本特性把它当作**验证用例集**消费，MUST NOT 把它改写成规格条文，也 MUST NOT 在它里面登记处置结果（处置结果归 Non-Disposable 报告与修复 lane 证据）。

## A–H Corpus Mapping *(validation cases → FR/SC)*

`notes/input-review-080-090.md` 的八组按「由哪条机制承接」映射。**逐条**（表内单条发现）的映射 MUST 在 plan/tasks 阶段展开为一行的清单，并遵循 FR-034（零未映射）。

| Group | 代表发现 | 检测类别 | 承接 FR | 承接 SC |
|-------|----------|----------|---------|---------|
| A 状态与裁决自相矛盾 | 089 注册 `Implemented` 而闭环 `block`；`verification.md` 无机器可读块；090 注册 `Planned` 而闭环 `accept`；080 无 `**Path**` 标记 | `status-unreadable` | FR-018, FR-019 | SC-008 |
| B 取代未回收 | 086 仍要求字节一致（089 已改投射）；085 契约四部分（owner 已五部分）；067 串行缺省未修订；088 证据路径陷阱与三种拼写 | `superseded-live`, `orphan-path` | FR-008, FR-009, FR-010 | SC-005 |
| C 重编号残留 | 089 绑定 `Feature ID: 086`、任务头部 086、T081 指向 086 的注册行、团队目录 `086-…`；088 八个契约写 `Feature: 087` | `renumber-live-binding` | FR-015, FR-016, FR-017 | SC-007 |
| D 一事实多 owner | 081 状态机三 owner、reason set 两 owner；084 判据两处互斥；088 汇报周期 15 分钟 vs 30 秒；090「规则锚八成员」四种拼写 | `multi-owner` | FR-011, FR-012, FR-013, FR-014 | SC-006 |
| E 闭集声明被测量证伪 | 083 范围自相矛盾与基线三值；083 声称宪法第一条原则实不存在；089 恒等式 `367+737≠751`；084 排除行 8 vs 38 | `false-closed-set` | FR-020 | SC-008 |
| F 常量与计数漂移 | 分解上限 40/60/80/30/120/160 六处；指令预算 37888 vs 38400；宪法 roster 陈旧计数；特性总数算术陈旧 | `stale-constant`, `multi-owner` | FR-011, FR-012, FR-013 | SC-006 |
| G 守卫有语义缺口 | 090 顺序守卫丢失位置比较；`first_no == "1"` 同义反复；`RULE_SET` 漏 ⑧ | `superseded-live`（守卫侧） | FR-009 | SC-005 |
| H 路径与证据残留 | 086 写不存在的 `.specify/skills/external/…`；082/085 指向不存在的证据文件；`.specify/.tmp/086-*` 属正当历史 | `orphan-path` | FR-009, FR-016 | SC-005, SC-007 |

**双向校验**：无 FR 承接的组（空集）与无组承接的检测类别（`deferral-marker` 目前只由理念层 FR-002…FR-005 承接、无 A–H 代表条目）都 MUST 在 plan 阶段显式说明——后者是预期，因为 A–H 回顾不专门检查延期措辞。

## Open Items *(deferred to clarify)*

以下各项本阶段自行裁定后仍具争议性，按 fast-fail 原则**上送**而非就地抹平。它们在 FR/SC 中都有承接位置，故不构成阻断：

- **OI-1（A3/FR-041 的范围外推）**：状态脊的 `goal_verbatim` 未记载「宪法原则 + 五处落点」的要求，而本规格把它落为 FR-041/A3。若编排者认为该要求不属于本特性，FR-041/SC-011 应整条移出。
- **OI-2（A9 处置词汇冲突）**：本特性处置集与 sanitize 的 `DISPOSITIONS` 是两套词汇，判定「不合并 + plan 阶段以 decision tension 裁定映射」。若期望单一词汇，需在 clarify 改判。
- **OI-3（B 组 088 证据路径的处置归属）**：`088` 的 `final-failed.txt` 陷阱属「历史证据的路径拼写」还是「owner 拼写漂移」，决定它归 `orphan-path` 还是 `superseded-live`；本阶段判为 `orphan-path`。

## Clarifications

<!-- 由 /speckit.clarify 填充：- Q: <question> → A: <answer> -->
