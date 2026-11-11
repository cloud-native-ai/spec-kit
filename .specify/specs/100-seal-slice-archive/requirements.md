# Requirements Specification: /speckit.seal — 分片归档步骤（Seal Slice Archive）

**Requirement Branch**: `100-seal-slice-archive`
**Created**: 2026-11-11
**Status**: Draft
**Flow Class**: execution
**Flow Type**: -
**Readers**: 框架维护者（编写/修订 `templates/commands/**`、`skills/internal/**`、`shared/definitions/**`、`scripts/python/**` 与 `.specify/specs/**` 的维护者）与下游项目中运行 `/speckit.seal`、需要判定「已交付分片何时、以何种方式从 `.specify/specs/` 同级目录移入父 spec 的 `slices/`，以及移动后引用为何仍然全部可解析」的维护者——读者基准不新建，按 `.specify/shared/guidelines/user-facing-comprehension.md` § 基准读者与覆盖协议 的全局基准读者判定
**Reading scenario**: 当需要判定「分片归档做什么、不做什么」「归档清单记录什么、放在哪」「哪些引用必须改写、哪些历史文本必须保持原字节」「归档后如何证明零丢失、零悬空引用」「归档与 `/speckit.sanitize` 的退休归档、`archive-gate`、non-disposable 处置集的关系」「seal 终态为阻断时归档还能不能跑」「如何回滚」时打开本规格，据 FR-001…FR-028 与 SC-001…SC-010 决定 `/speckit.clarify` 与后续实现是否放行
**Input**: User description: "需要再优化 speckit.seal 的流程：将 074a 和 074b 清理掉，同时又能保证信息不丢；我倾向于在 074 中建子目录归档 074a 和 074b；需要将这个归档步骤设计一个流程固化到 speckit.seal 的流程中。归档位置为父 spec 目录下的 `slices/` 子目录；信息零丢失（git mv 保留历史 + 清单逐片记录原路径→归档路径、文件清单与哈希、引用更新记录）；归档后未解析引用为 0（fail closed）；确定性更新 register、特性详情、契约、父 spec 内部引用、父 merge-manifest、line registry；触发点为 merge-apply 成功后（Sealed 或 blocked 均可），dry-run 预览 + apply 两阶段；以 074a/074b 真实归档为验收；不新建命令、不改 merge-back 语义、不删除任何记录、可回滚。"

## Related Feature *(mandatory)*

**Feature ID**: Need clarification
**Feature Name**: Need clarification

## Overview

`/speckit.seal` 在 099 中交付了「分片同名输出件合并回写父级 + 封装判定」，但把**分片目录本身的后续处置**明确留给了 non-disposable 复核：099 契约 C-019 写「分片承载物的后续保留/退役 MUST 按 non-disposable 纪律复核后决定，MUST NOT 默认沉默保留」，同时 C-023 / C-008 禁止 merge-apply 与引擎动作表移动、归档或删除 spec 目录。结果是 074 的实测形态（在提交 `48e273d73` 测量）：074a（58 文件 / 约 942 KB）与 074b（54 文件 / 约 827 KB）已全部合并回父级、父级合并清单与指针视图齐备，但两个分片仍作为 `.specify/specs/` 的同级目录存在，被 5 条 `register.md` 推荐行、父 spec 的 143 处路径提及、merge-manifest 的 123 个路径值、框架 owner 文档与 3 个测试文件引用。它们既没有被处置，也没有明确的处置流程——这正是本特性要消除的「合并后残留」。

本特性为 `/speckit.seal` 增加一个**分片归档步骤**：在每个分片已完成合并回写后，把它整体移入父 spec 目录下的 `slices/<原分片目录名>/`（[[STR-001]]），用 `git mv` 保留历史；产出一份按 spec 的归档清单 `archive-manifest.json`（[[STR-002]]），逐片记录原路径→归档路径、文件清单与 sha256、以及每一条引用更新/保留记录；确定性改写全部**活引用**，**日期化记录**保持原字节并只经清单的 `from → to` 映射解析，最终「未解析引用 = 0」作为 apply 的合取前置（fail closed）。该步骤在 merge-apply 成功后即可执行，**不依赖最终 `Sealed` 判定**——074 当前就是「合并完成、封装阻断」的真实状态，归档必须能在此状态落地。

**它不是第二套归档机制**：分片归档复用 non-disposable owner 的 `archive` 处置（一次移动、映射入记录、可逆、永不删除），只扩展其「归档目的地」这一个事实；独立 spec 的退休归档仍由 `/speckit.sanitize` 的归档 lane 与 `archive-gate` 独占。它也不新建命令：流程固化在既有 `/speckit.seal` 的命令模板、`seal-artifact` 技能与 `seal-utils.py` 引擎内。不删除任何记录，移动是纯移动（分片内容字节不变），回滚路径由清单承载并文档化。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 把已交付分片归档进父 spec 的 slices/，零丢失 (Priority: P1)

维护者对一条已完成 merge-apply 的拆分 spec 运行 `/speckit.seal`。流程在合并回写之后给出归档预览：哪几个分片将被移动、从哪到哪、每个分片多少文件、哪些引用将被改写、哪些历史记录将原样保留。确认无阻断后执行 apply：两个分片目录整体 `git mv` 到 `<父 spec>/slices/` 下，目录名与内部相对树保持不变；分片内每一字节不变；一份 `archive-manifest.json` 落父 spec 根，逐片记录移动对、文件清单与哈希。归档完成后，`git status` 显示每个文件一条重命名对，而不是删除。

**Why this priority**: 这是用户诉求的第一句——把 074a/074b 清理掉而信息不丢。没有这一步，合并回写后的分片永远留在同级目录里，`/speckit.seal` 的流程也就没有终点。

**Independent Test**: 对 074 执行归档；断言两个分片只存在于 `074-goal-team-sdd-unification/slices/` 下、文件数与逐文件 sha256 与归档前一致、`git diff --name-status -M` 对每个文件给出重命名对（无纯删除）、归档清单存在且可复核；重跑 apply 断言 `already-archived`（[[STR-005]]）且零 diff。

**Acceptance Scenarios**:

1. **Given** 父 spec 的 `merge-manifest.json` 显示合取前置全部成立（合并完成、零开放冲突、分片已闭合）、工作树在父 spec 与分片范围内干净，**When** 运行归档步骤，**Then** 每个分片目录恰好落在 `<父 spec>/slices/<原分片目录名>/`（[[STR-001]]），分片内文件字节不变，归档清单 `archive-manifest.json`（[[STR-002]]）落父 spec 根且逐片记录移动对、文件清单与 sha256。
2. **Given** 同一次归档已成功，**When** 再次运行 apply，**Then** 以 `0` 退出并具名报告 `already-archived`（[[STR-005]]），不产生第二份归档清单、不重复移动、零 diff。
3. **Given** 一个分片目录仍留在源位置而同名目标已存在于 `slices/`，**When** 运行归档，**Then** 以具名理由拒绝，两个目录都不被改动。
4. **Given** 父 spec 或任一分片存在本流程之外的未提交改动，**When** 运行归档，**Then** 以 `dirty-spec-tree` 具名拒绝并点名路径，零写入。

---

### User Story 2 - 归档后所有引用仍然可解析（活引用改写，历史记录只映射） (Priority: P1)

维护者归档分片后，下一次运行 `/speckit.seal`、`/speckit.feature` 或阅读父 spec 时，所有**当前指针**都已指向归档后的路径：`register.md` 的推荐行、特性详情的活指针区、父 spec 的设计/任务/验收/契约、父 `merge-manifest.json`、框架 owner 文档与镜像、以及硬编码分片路径的测试。**历史记录**——分片内部的 review/code-review/verification/test-evidence、`.specify/memory/**`、`features.md` 的日期化叙述——保持原字节，不因移动而改写；它们的旧路径经归档清单的 `from → to` 映射仍可解析。流程在 apply 前报告未解析引用数，只有为 0 才写入；apply 后复验仍为 0。

**Why this priority**: 「信息不丢」不只是文件还在，更是下一位读者仍能沿引用找到它们。只移动不改引用会制造悬空指针；把历史文本全部改写又会违反 dated-record 红线。两类引用必须分开处置，且结果必须可判定。

**Independent Test**: 用一个含活引用、日期化引用与一个未分类引用的夹具树运行归档：断言活引用全部改写、日期化引用哈希前后一致且经映射可解析、未分类引用让 apply 拒绝；再注入一条指向旧路径的活引用，断言测试转红。

**Acceptance Scenarios**:

1. **Given** 分片路径同时出现在活引用与日期化记录中，**When** 执行归档 apply，**Then** 每条活引用被改写为归档路径并在清单中有 `live-rewrite` 行；每条日期化引用保持原字节，清单中有 `dated-preserved` 行且其旧路径前缀命中 `from → to` 映射。
2. **Given** 归档完成后，**When** 对声明的扫描根重新执行解析检查，**Then** 未解析引用数为 0；其中活引用直接解析到存在的归档路径，日期化引用经清单映射解析到存在的归档路径。
3. **Given** 一处引用落在声明的载体封闭集之外、却仍指向旧分片路径，**When** 运行 plan，**Then** 以 `unclassified-reference` 具名阻断，apply 拒绝。
4. **Given** 归档清单缺少某个分片的 `from → to` 映射，**When** 重新执行解析检查，**Then** 该分片下的日期化引用变为未解析，检查转红。

---

### User Story 3 - 归档步骤固化在 /speckit.seal 流程中，blocked 状态也能执行 (Priority: P1)

维护者运行 `/speckit.seal` 时，流程在 merge-apply 成功之后自动进入归档阶段：先 `archive-plan`（只读预览：分片集、移动对、引用更新计划、阻断清单、退出码），无阻断后 `archive-apply`（写动作），最后才进入封装判定。归档不要求 `Sealed`：074 的封装终态是具名阻断，归档仍必须能执行。整个流程仍是同一个命令、同一个引擎、同一个技能；没有新增 `/speckit.*` 命令，没有新引擎。

**Why this priority**: 用户要求「把这个归档步骤设计一个流程固化到 speckit.seal 的流程中」。如果它只是一次手工 `git mv`，下一条拆分 spec 仍会重复同一残留；如果它要求 `Sealed` 先行，074 这个真实验收对象今天就无法归档。

**Independent Test**: 对一个封装判定会被阻断的夹具 spec（合并已完成、存在具名阻断）运行 `/speckit.seal`，断言归档阶段仍执行且成功；对一个 merge-apply 被拒绝的夹具，断言归档阶段不启动；断言命令名集合与 `COMMAND_BASELINE` 不变。

**Acceptance Scenarios**:

1. **Given** 一条 spec 的 merge-apply 成功、最终封装判定为具名阻断，**When** 运行 `/speckit.seal`，**Then** 归档步骤照常先预览后执行，分片进入 `slices/`（[[STR-001]]），阻断清单与归档清单同时存在且互不覆盖。
2. **Given** 一条 spec 的 merge-apply 被拒绝（开放冲突或分片未闭合），**When** 运行 `/speckit.seal`，**Then** 归档步骤不启动，报告点名上游阻断，零移动、零写入。
3. **Given** 分片集合为空，**When** 运行归档步骤，**Then** 以 `0` 退出并报告 `not-applicable` 及判定依据，零写入、零清单。
4. **Given** 完整仓库，**When** 运行命令面审计，**Then** `/speckit.*` 命令名集合与 `COMMAND_BASELINE` 与改动前一致；新增第 32 个命令时守卫转红。

---

### User Story 4 - 归档有明确边界：不是退休、不改状态、可回滚 (Priority: P2)

维护者需要确信这次移动没有越权：它不把 spec 或分片退休到 `.specify/archive/`，不查询或改写 `archive-gate` 的退休准入，不改注册表状态、不改 `seal.md`、不改合并清单的合并结论（只改其中的路径字段并重算摘要），不碰 goal/team 树，不 push，不删除任何文件。归档清单携带足够信息，使一次移动和它的引用改写可以按文档化步骤逆向恢复为归档前的逐字节状态。

**Why this priority**: 归档动作一旦越界就会与 sanitize / goal / seal 的既有 owner 冲突；没有回滚证据，维护者不会对百余个文件的生产树执行移动。

**Independent Test**: 静态审计引擎写面白名单与动作表；对夹具执行归档后按文档步骤回滚，断言树恢复为归档前的逐字节状态；注入一次删除或一次 status 写入，断言测试转红。

**Acceptance Scenarios**:

1. **Given** 一次成功的归档，**When** 对比前后状态面，**Then** 注册表行、特性详情状态、`seal.md`（若存在）与 `merge-manifest.json` 的合并结论/计数/冲突均为不变；变化的只有路径字段、摘要、归档清单与被移动的目录。
2. **Given** 一次成功的归档，**When** 按契约/quickstart 文档的恢复步骤执行，**Then** 分片回到原路径、活引用回到原值、归档清单移除，树与归档前逐字节一致。
3. **Given** 归档运行，**When** 静态审计引擎动作表与写路径白名单，**Then** 不存在删除、push、goal/team 写入或第二份注册表；唯一的移动动作是 `archive-apply`（[[STR-004]]）且目标被限制在父 spec 的 `slices/` 内（[[STR-001]]）。

---

### Edge Cases

- **分片集合为空**：归档步骤报告 `not-applicable` 与判定依据，退出 `0`，零写入；不得读作「已归档」。
- **部分归档**：一个分片在源、另一个在目标，或同一分片两端同时存在：按输入缺陷退出 `2`，点名路径，零写入；不猜测哪一侧为准。
- **目标目录已存在且源也存在**：`destination-exists` 拒绝（退出 `1`），两侧都不动。
- **源与目标都不存在**：合并清单声称的分片在树上找不到：`slice-missing` 输入缺陷（退出 `2`）。
- **归档后再次运行 merge-plan / merge-apply / seal**：必须通过归档清单发现分片，行为与归档前等价；`merge-apply` 幂等成功且零写入。
- **运行期 line registry 缺失**：worktree 中 `.specify/state/` 不可见时记 `absent`，不阻断；主仓可见时更新并留痕。
- **日期化记录引用旧路径**：保持原字节，经 `from → to` 映射解析；不得为了「看起来干净」改写它们。
- **活引用位于未声明的载体**：`unclassified-reference` 阻断，先把它纳入契约的载体封闭集或修掉，再重跑。
- **移动中途失败**：按原字节恢复已移动目录与已改写文件，退出 `2`；不得留下半归档状态。
- **非 git 工作树**：无法满足 `git mv` 语义时退出 `2` 并点名原因；不得退化为普通 `mv`。
- **同一 spec 并发归档**：后到者读到归档清单即走 `already-archived`；不得产生第二份清单或重复移动。
- **两条线归档不同 spec**：写入不同父 spec 目录下的不同清单路径；不得引入共享可变聚合。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: `/speckit.seal` MUST 在 merge-apply 成功之后提供分片归档步骤；该步骤 MUST 在最终封装判定为 `Sealed` 或任一具名阻断时都可用，MUST NOT 以 `Sealed` 为前置。merge-apply 被拒绝时归档 MUST NOT 启动，并 MUST 点名上游阻断。
- **FR-002**: 归档目的地 MUST 恰为 `<父 spec 目录>/slices/<原分片目录名>/`（[[STR-001]]）；分片目录名 MUST 原样保留，内部相对树 MUST 原样保留，MUST NOT 扁平化、重命名或改变父子关系。`slices/` 的语义 MUST 在框架布局 owner（`.specify/shared/definitions/framework-map.md` 的 Feature specs 行）登记，MUST NOT 创建无文档目录。
- **FR-003**: 归档 MUST 是一次**纯移动**：每个分片目录以 `git mv` 语义整体移动，git 变更视图 MUST 对每个文件呈现重命名对，MUST NEVER 呈现纯删除；MUST NOT 复制后删除，MUST NOT 改写分片内任何文件的字节，MUST NOT 在分片内添加标记行。
- **FR-004**: **零丢失** MUST 可判定：归档前后每个分片的文件数 MUST 相等、逐文件 sha256 MUST 相等、目录内相对路径集合 MUST 相等；归档清单 MUST 逐片记录文件清单与哈希，并记录可复算的聚合摘要。任一不等即归档失败并按原字节回滚。
- **FR-005**: 归档清单 MUST 每个父 spec 一份，落在父 spec 根目录的固定文件名 `archive-manifest.json`（[[STR-002]]），机器可读、键序稳定（`indent=2, sort_keys=True, ensure_ascii=False`）。核心字段集 MUST 在契约中声明为**封闭集**（未知字段 MUST NOT 写入），且该封闭集 MUST 覆盖：schema 版本、目标 spec、生成者与引擎身份、钉住的归档前提交、分片顺序与顺序依据、逐片 `{slug, from, to, file_count, files[{path, sha256}], merged_into_pointer}`、引用更新台账、检查读数与可复算摘要。清单 MUST NOT 含墙钟时间或依赖运行时刻的字段；同输入两次 plan MUST 逐字节一致。
- **FR-006**: 归档前置条件 MUST 是合取：合并清单存在且 `merge.status` 为已完成、开放冲突数为 0、每个分片按 099 的既有闭合判据已闭合、父 spec 与分片范围内无本流程之外的未提交改动、每个分片在源与目标中**恰好存在一侧**。任一不成立 MUST 拒绝或按输入缺陷退出，并逐条点名**全部**未满足条件；MUST NOT 只报第一条，MUST NOT 有部分归档。
- **FR-007**: 分片集合为空时，归档 MUST 以 `0` 退出并具名报告 `not-applicable` 与判定依据（依据 MUST 来自合并清单或分片发现结果，不得只写「无分片」），MUST NOT 创建空清单，MUST NOT 静默跳过。
- **FR-008**: 归档 MUST 由既有 seal 引擎的两个新动作构成：只读的 `archive-plan`（[[STR-003]]）与写入的 `archive-apply`（[[STR-004]]）。动作集合的 owner（099 契约 `seal-engine.contract.md` C-001）MUST 在同一次变更内原地修订为「既有四动作 + 这两个动作」，MUST NOT 新建第二个引擎或第二条命令入口。两个动作 MUST 满足既有脚本接口契约：`--help` / `--version` 零副作用、未声明选项以 `2` 拒绝。退出码 MUST 封闭为 `0`（成功或幂等）/ `1`（前置条件拒绝）/ `2`（输入或环境错误），语义与既有 seal 动作一致。
- **FR-009**: `archive-apply`（[[STR-004]]）MUST 两阶段执行：先在只读阶段重算与 `archive-plan` 相同的完整计划，只有阻断数为 0 才进入写入；写入 MUST 按批次执行并在失败时按原字节恢复已移动目录与已改写文件，以 `2` 结束，MUST NOT 留下可被读作半归档的状态。拒绝（`1`）MUST 零持久化写入，报告只经 stdout，MUST NOT 创建拒绝记录或第二份台账；同输入重跑 MUST 复现同一阻断清单（顺序稳定）。
- **FR-010**: 已归档是幂等成功，不是拒绝：当归档清单存在、每个分片位于目标且源侧不存在时，`archive-apply` MUST 以 `0` 退出并具名报告 `already-archived`（[[STR-005]]），不产生第二份清单、不重复移动、不重复改写引用；`archive-plan` 重跑 MUST 报告零待移动、零未解析。
- **FR-011**: 回滚 MUST 可执行且被文档化：归档清单 MUST 携带恢复所需的全部事实（逐片 `from` / `to`、逐文件哈希、逐条引用的 `before` / `after`）；契约与 quickstart MUST 给出确定性的恢复步骤（逆移动 + 逆向引用改写 + 移除清单）。MUST NOT 新增回滚动作或第二个回滚引擎；按文档步骤执行后树 MUST 与归档前逐字节一致，并由测试夹具证明。
- **FR-012**: 引用分类 MUST 是确定性的封闭判定：每条**命中** MUST 落入 `live-rewrite`（当前指针）/ `dated-preserved`（日期化记录）二值之一；每个被声明的运行期 line registry 载体 MUST 各记一条 `runtime-updated`（存在并更新）或 `absent`（缺席）。载体名册与扫描根 MUST 是封闭集，owner MUST 在本特性的契约中声明；分类 MUST 只依据路径、行前缀、章节边界或文件谓词，MUST NOT 依赖模型对语义的转述判断。任何落在封闭集之外、却仍指向旧分片路径的命中 MUST 成为 `unclassified-reference` 阻断（fail closed）。
- **FR-013**: **活引用** MUST 在同一 apply 批次内被改写为归档路径。必须覆盖的载体下限为：`.specify/register.md` 的推荐行、特性详情的活指针区、父 spec 的 `plan.md` / `research.md` / `quickstart.md` / `tasks.md` / `verification.md` / `review.md` / `code-review.md` / `feature-ref.md` / `contracts/`、父 `merge-manifest.json` 的路径字段、框架 owner 文档与其 `.specify/` 镜像、以及硬编码分片路径的测试文件。每条改写 MUST 在清单中有 `before` / `after` / `carrier` / `line` 记录。
- **FR-014**: **日期化记录** MUST 保持原字节不变：至少包括分片内部全部文件、`.specify/memory/**`、`.specify/history/**`、`features.md` 的日期化 Last Updated 叙述、特性详情的时间线章节。它们的旧分片路径 MUST 只经 `archive-manifest.json`（[[STR-002]]）的 `from → to` 前缀映射解析；运行前后哈希 MUST 一致。父 `tasks.md` 的 `> superseded` 拆分账是**当前合并账**，按活引用处理（改路径、不改历史事实）。
- **FR-015**: 「未解析引用 = 0」MUST 有唯一定义并 fail closed：一条引用被判定为已解析，当且仅当 (a) 其目标路径在树上存在，或 (b) 它是日期化记录中的旧分片路径且该前缀命中归档清单的 `from → to` 映射并落到存在的归档路径。`archive-plan` MUST 报告未解析数；`archive-apply` MUST 在未解析数大于 0 时拒绝；apply 成功后复验 MUST 仍为 0。检查 MUST 覆盖契约声明的扫描根，MUST NOT 只抽查已知载体。
- **FR-016**: 归档清单 MUST 承载完整的**引用台账**：每条命中一条记录，含载体、行号、`before`、`after` 与二值 `kind`（`live-rewrite` / `dated-preserved`）之一；每个运行期载体另有一条 `runtime-updated` 或 `absent` 记录。闭环算术 MUST 成立——扫描命中总数 = `live-rewrite` + `dated-preserved`；`runtime-updated` + `absent` = 被声明的运行期载体数；移动文件行数 = 归档清单的 `files` 行数。任一行缺失或算术不成立 MUST 阻断。
- **FR-017**: 运行期 line registry（环境级，git-ignored 的 `.specify/state/**`）MUST 按活指针处理：当状态根可解析且记录存在时，其中的分片路径引用 MUST 在同一批次更新并记 `runtime-updated`；当状态根不可解析或记录缺席时，清单 MUST 记 `absent` 并说明原因，MUST NOT 因此阻断。该更新 MUST NOT 进入版本库提交范围，MUST NOT 改变任何 line 的 `spine_state` 或阶段读数。
- **FR-018**: 父 `merge-manifest.json` 的更新 MUST 限定为路径字段（至少 `slices[].carrier_tasks`、`dispositions[].evidence[]`、`artifacts[].pointer.paths[]` 与任何其他路径形态的值）；合并结论、计数、冲突、ID 映射与分片顺序 MUST 保持不变；摘要 MUST 按 099 契约 C-034 的既有算法重算，归档清单 MUST 记录更新前后的摘要。MUST NOT 借归档改写 merge-back 语义。
- **FR-019**: 归档后，`merge-plan` / `merge-apply` / `seal` 的分片发现与载体解析 MUST 先读归档清单，把归档分片视为**同一分片集**：MUST NOT 把归档读成「无分片」，MUST NOT 把归档目录读成新的分片候选，MUST NOT 改变分片顺序依据。归档后重跑 `merge-apply` MUST 幂等成功且零写入；seal 的 P0 / `blocking` / 闭合判定 MUST 继续读取归档后的分片原始记录。该条只扩展解析路径，MUST NOT 改变合并回写与封装判定语义。
- **FR-020**: 分片归档 MUST NOT 是退休归档：目的地 MUST 只在父 spec 的 `slices/` 子树内（[[STR-001]]），MUST NOT 写入或查询 `.specify/archive/`，MUST NOT 查询 `archive-gate`，MUST NOT 被任何退休入口复用。处置词汇 MUST 复用 non-disposable owner 的既有四值，本次 MUST 只原地补充 `archive` 的「所属父 spec 的 `slices/`」这一目的地形态；MUST NOT 新增第五个处置值、第二份词表或第二个归档引擎。独立 spec 的退休仍归 `/speckit.sanitize` 归档 lane。
- **FR-021**: 本特性 MUST NOT 新建 `/speckit.*` 命令：`COMMAND_BASELINE` MUST 保持不变，命令名集合 MUST 与改动前逐一相同。归档流程 MUST 固化在既有三件产物内：`templates/commands/seal.md`（及经既有副本生成器产生的逐工具副本）、`skills/internal/seal-artifact/SKILL.md`、`scripts/python/seal-utils.py`；技能 MUST NOT 在引擎判定之外自行给出归档结论。
- **FR-022**: 流程文档 MUST 同步：命令模板 MUST 说明归档发生在 merge-apply 成功之后、先预览后 apply、封装修阻断不阻断归档、以及拒绝语义；命令参考文档与 quickstart MUST 各给出可执行的归档走查与恢复走查；文档 MUST 按指针引用判定 owner，MUST NOT 复述第二份判定表。
- **FR-023**: 契约 MUST 原地扩展既有 owner，不建第二套：099 的 `seal-engine.contract.md`（动作集与写面）、`merge-back.contract.md`（分片后续处置与写面边界）、`records-and-boundaries.contract.md`（四向边界与零重复机制）MUST 在同一变更内修订；本特性的契约页只拥有**归档清单 schema、载体分类与解析定义**这三件新事实。
- **FR-024**: 每条可判定断言 MUST 有契约级或单元级测试（红先或带变异取证），至少覆盖：目的地布局与重命名对、零丢失哈希、清单确定性与闭环算术、引用分类封闭性、活引用改写完整性、日期化记录字节保持、未解析 = 0 的 fail closed、幂等、拒绝语义封闭集、纯移动无删除、归档后 manifest-aware 解析、状态/封装结论不变、无新命令、回滚逐字节恢复、并发写路径互异。测试执行 MUST 走唯一入口 `scripts/bash/run-tests.sh`；只有措辞变化的检查 MUST NOT 计为取证。
- **FR-025**: 本特性 MUST 交付一次可执行的 **074 回合**：对 `.specify/specs/074-goal-team-sdd-unification/` 执行归档，074a 与 074b MUST 恰好落在 `slices/` 下（[[STR-001]]），归档清单 MUST 存在且零丢失断言成立，活引用 MUST 全部解析、日期化引用 MUST 经映射解析、未解析数 MUST 为 0；074 的注册状态与封装结论（当前为具名阻断）MUST 保持不变；全量测试 MUST 零新增红（按失败 node-id 名单比对，既有红不修不掩）。
- **FR-026**: 074 回合 MUST 可复现：归档成功后重跑 `archive-plan` MUST 报告零待移动、零未解析；重跑 `archive-apply` MUST 得到 `already-archived`（[[STR-005]]）与零 diff；阻断态下的阻断清单 MUST 逐条稳定，MUST NOT 因重跑顺序改变结论。
- **FR-027**: **零新增重复机制** MUST 可静态核验：仓库 MUST NOT 因本特性新增第二套处置词表、第二个归档引擎、第二份注册表/台账、调度器或并行 spec 树；归档清单 MUST 每个父 spec 一份单文件，MUST NOT 引入共享可变聚合。两条并行线归档不同 spec 时 MUST 写入不同路径；同一 spec 的并发 apply MUST 由「后到者读清单 → `already-archived`」收敛，MUST NOT 依赖锁文件。
- **FR-028**: 写面 MUST 封闭且可静态审计：`archive-apply`（[[STR-004]]）只允许写 (a) 分片目录在父 spec 树内的移动，(b) 父 spec 的活引用文件、归档清单与 `merge-manifest.json` 路径字段，(c) 契约声明的框架 owner 文档与镜像、测试文件，(d) 可选且缺席不阻断的运行期 state 记录。MUST NOT 删除文件、MUST NOT push、MUST NOT 改注册表状态或 `seal.md`、MUST NOT 触碰 goal/team 树、MUST NOT 写声明集合之外的路径。静态审计以引擎写路径白名单为准，白名单外的写路径出现时审计测试 MUST 转红。

### Runtime Stack & Dependency Ownership

| ID | Capability | Form | Owner | Pin | Contract | Joint acceptance | FR | Premises |
|----|------------|------|-------|-----|----------|------------------|-----|----------|
| RS-001 | CPython 标准库（移动、哈希、JSON、文本与路径判定） | signed-contract | CPython 上游（本仓只消费） | `pyproject.toml` 既有 `requires-python` 下限；本特性零新增第三方依赖 | `pyproject.toml` | 归档动作在锁定解释器上跑通 plan/apply 全部分支 | FR-005, FR-008 | EP-001 |
| RS-002 | `pytest`（契约与单元测试） | signed-contract | pytest 上游（本仓只消费） | `pyproject.toml` 既有测试依赖 | `pyproject.toml` | `bash scripts/bash/run-tests.sh` 全绿且零新增红 | FR-024 | EP-002 |
| RS-003 | `git`（`git mv`、`status --porcelain`、`diff --name-status -M`） | signed-contract | git 上游（本仓只消费） | 运行环境既有 git；非 git 工作树按输入错误退出 `2` | `.specify/workflow/git.md` | 重命名对可判、恢复步骤可执行 | FR-003, FR-011 | EP-003 |
| RS-004 | 既有 seal 引擎与 non-disposable 处置 owner | in-scope | 本特性自身（就地扩展动作集与目的地形态，不新建引擎或词表） | 不适用（无外部版本面） | 不适用（in-scope） | 动作集/写面/边界守卫与静态审计 | FR-020, FR-023 | EP-004 |

### Key Entities *(include if requirement involves data)*

- **Archive Manifest（`archive-manifest.json`，[[STR-002]]）**: 每个父 spec 一份的归档记录；承载分片移动对、逐文件清单与哈希、引用台账、检查读数、钉住的提交与可复算摘要。它是「旧路径 → 归档路径」的唯一解析通道。
- **Archived Slice Entry**: 一个分片的归档条目；含 slug、原路径、归档路径、文件数、逐文件 `{relative_path, sha256}`、以及指回父合并清单的指针。
- **Reference Update Row**: 一条引用处置记录；含载体路径、行号、`before`、`after`、二值 `kind`（`live-rewrite` / `dated-preserved`）；运行期载体另有 `runtime-updated` / `absent` 记录。
- **Runtime State Record**: 环境级、git-ignored 的 line registry 记录；存在时按活指针更新，缺席时在清单中记 `absent`，不改变任何状态读数。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 074 真实验收通过：归档后 074a 与 074b 恰好位于 `.specify/specs/074-goal-team-sdd-unification/slices/` 下（[[STR-001]]），文件数与逐文件 sha256 与归档前一致（运行时探针计数，不写死点值），`archive-manifest.json`（[[STR-002]]）存在且可复核，git 变更视图对每个文件给出重命名对且零纯删除；074 的注册状态与封装结论保持不变。 **Path**: final
- **SC-002**: 零丢失与幂等成立：归档前后逐文件哈希一致；归档成功后重跑 apply 得到 `already-archived`（[[STR-005]]）与零 diff，重跑 plan 得到零待移动、零未解析；把任一文件内容注入变异后哈希检查转红。 **Path**: final
- **SC-003**: 引用完整性 fail closed：活引用全部指向存在的归档路径；日期化引用保持原字节且经清单映射解析；未解析数为 0；注入一条指向旧路径的活引用、或从清单移除一个 `from → to` 映射时，检查 MUST 转红。 **Path**: final
- **SC-004**: 流程集成成立：对封装判定为具名阻断的夹具 spec，`/speckit.seal` 在 merge-apply 成功后仍执行归档；`archive-plan`（[[STR-003]]）与 `archive-apply`（[[STR-004]]）的预览/写入计划一致；退出码封闭为 `0/1/2`；`COMMAND_BASELINE` 不变，新增第 32 个命令时守卫转红。 **Path**: final
- **SC-005**: 边界不越权：归档前后注册表状态、特性详情状态、`seal.md`（若存在）与合并结论/计数/冲突不变；仓库中不存在本特性造成的删除、push、goal/team 写入或 `.specify/archive/` 写入；把一次删除或一次状态写入注入引擎后静态审计转红。 **Path**: supporting
- **SC-006**: 确定性成立：同一夹具树两次 `archive-plan` 的清单逐字节一致；成功 apply 重跑零 diff；把任一排序改成按文件系统时间或返回时刻时测试转红。 **Path**: supporting
- **SC-007**: 清单完整性与闭环算术成立：每个被移动文件在清单中有且仅有一行；每条引用命中在台账中有且仅有一行；`扫描命中总数 = live-rewrite + dated-preserved`、`runtime-updated + absent = 被声明的运行期载体数`、`移动文件行数 = files 行数` 三组两侧复算相等；删掉任一行时检查转红。 **Path**: supporting
- **SC-008**: 运行期 line registry 处置有效：记录存在时其分片路径被更新并记 `runtime-updated`；记录缺席时记 `absent` 且不阻断；两种情形各有夹具，把缺席改成阻断时测试转红。 **Path**: supporting
- **SC-009**: 单一机制与并发安全成立：仓库中不存在第二套处置词表、第二个归档引擎或第二份按 spec 的归档清单；两个夹具 spec 并发归档写入不同路径；把一份清单复制成共享聚合时测试转红。 **Path**: supporting
- **SC-010**: 回滚可执行：按契约/quickstart 文档的恢复步骤执行后，树与归档前逐字节一致（分片位置、活引用、清单存在性全部恢复）；跳过任一步骤时夹具断言转红。 **Path**: supporting

### Measurement Sources & Collection Methods

- **SC-001 Source**: 074 回合的 run 记录：归档前后逐文件 sha256 清单、`git diff --name-status -M` 输出、`archive-manifest.json`、状态面快照；读数写入 `test-evidence/`。
- **SC-002 Source**: 同一回合的前后哈希对照、重跑 apply/plan 的退出码与 `git diff --stat` 零输出；内容变异夹具的转红实测。
- **SC-003 Source**: 解析检查的机读报告（未解析计数、`live-rewrite` / `dated-preserved` 行数）、注入悬空引用与移除映射两类变异实测。
- **SC-004 Source**: 阻断态夹具与 merge-apply 拒绝夹具的引擎输出与退出码；`COMMAND_BASELINE` 审计与命令名集合对照。
- **SC-005 Source**: 归档前后状态面快照、写面静态审计输出、注入删除/状态写入的转红实测。
- **SC-006 Source**: 两次 plan 的 sha256 对照、apply 重跑的 `git diff --stat` 零输出、排序变异实测。
- **SC-007 Source**: 清单的算术复算输出（二值命中计数、运行期载体行数、文件行数）；删行变异实测。
- **SC-008 Source**: 存在/缺席两类运行期夹具的清单行与退出码；缺席转阻断的变异实测。
- **SC-009 Source**: 仓库结构静态审计（词表、引擎、清单路径）；并发双写夹具的路径断言；聚合变异实测。
- **SC-010 Source**: 回滚夹具的前后树哈希对照；跳过步骤的转红实测。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `"slices"` | FR-002, FR-020, SC-001 |
| `STR-002` | `"archive-manifest.json"` | FR-005, FR-014, SC-001 |
| `STR-003` | `"archive-plan"` | FR-008, SC-004 |
| `STR-004` | `"archive-apply"` | FR-008, FR-028, SC-004 |
| `STR-005` | `"already-archived"` | FR-010, FR-026, SC-002 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-11-11（无人值守 requirements 阶段，自行裁决并记录）

- Q: 归档步骤的触发点与 `Sealed` 的关系？ → A: 触发点是 **merge-apply 成功**；`Sealed` 与具名阻断两种终态都可归档（074 当前即阻断态）。merge-apply 本身被拒绝时归档不启动。（FR-001）
- Q: 目的地与清单形态？ → A: 目的地为父 spec 下的 `slices/<原目录名>/`（[[STR-001]]）；清单为父 spec 根的 `archive-manifest.json`（[[STR-002]]），一 spec 一份，与 `merge-manifest.json` 并列。分片内容不做任何改写，记录由清单与父级指针承载。（FR-002、FR-005）
- Q: 「未解析引用 = 0」如何与「历史记录不得改写」相容？ → A: 区分活引用与日期化引用。活引用必须直接解析到存在的归档路径；日期化引用保持原字节，经清单的 `from → to` 映射解析。两者之外即未解析，apply 拒绝。映射是唯一解析通道。（FR-012、FR-014、FR-015）
- Q: 与 sanitize 的退休归档、`archive-gate` 的关系？ → A: 分片归档不是退休：目的地只在父 spec 的 `slices/` 内，不查 `archive-gate`，不写 `.specify/archive/`；处置词汇复用 non-disposable 的 `archive`，只补目的地形态。（FR-020）
- Q: 运行期 line registry 缺席怎么办？ → A: 存在则更新并记 `runtime-updated`；缺席则记 `absent`，不阻断（worktree 中 `.specify/state/` 不可见是正常形态）。（FR-017）

## Assumptions

- **Flow Class 判定**：`execution`。验收 oracle 是程序：命令模板、引擎动作、契约测试、清单算术与引用解析均可被机器执行/解析；交付物不是供人阅读的文档（虽含文档更新，但缺陷只在机器行为偏离时暴露）。
- **074 阻断态**：任务简报导出的「074 seal 回合终态 blocked（099 需求第 027 条 (d) 与 B2 具名）」作为继承前提；本阶段实测复核到「无 `seal.md`、注册状态仍为 `Ready for Review`、合并已完成」。归档不依赖该阻断清单的原文。
- **动作命名**：`archive-plan` / `archive-apply` 沿用 `merge-plan` / `merge-apply` 的房内先例；若 clarify 改名，只改取值不改语义。
- **清单位置**：`archive-manifest.json` 默认放父 spec 根（与 `merge-manifest.json` 并列）；若 clarify 选择 `slices/` 内，需同步调整 FR-005/FR-014 的路径引用。
- **父 `tasks.md` 拆分账**：57 行 `> superseded` 行按活指针处理（改路径、不改历史事实）；分片内部的 `tasks.md` 按日期化记录保持原字节。
- **运行期 state**：`.specify/state/**` 是 git-ignored 的环境级记录；本 worktree 不可见，主仓可见。缺席不阻断。
- **既有 owner 原地修订**：099 契约与非 disposable owner 的修订属于本特性实现范围；不新增第二套契约家族或处置词表。
- **交付面**：不新增命令；`COMMAND_BASELINE`、SDD 阶段链与哨兵、`/speckit.sanitize` 归档 lane、`/speckit.goal` 的 `migrate-archive` 均不变。
