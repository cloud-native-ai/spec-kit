# Requirements Specification: init 落章机制——以 commit id 为唯一标识的框架来源回溯(Framework Source Stamp)

**Requirement Branch**: `043-init-commit-stamp`  
**Created**: 2026-08-17  
**Status**: Draft  
**Input**: User description: "需要在init命令中增加一个机制:在init命令后需要将当前speckit的版本信息(以commit id为版本号)写到目标项目中,需要达成的效果是在目标项目中可以通过这个信息反向的查看来源于哪个代码切片.当前不使用正式的版本号,以commit id作为唯一标识."

> **词汇表映射**(`.specify/memory/glossary.md` 协议):输入中"代码切片"为高危混淆词(Goal Target「目标切片」/ System Slice「系统切片」),本需求语义映射为 **git commit(框架仓的一次提交)**;"init命令" 指 `specify init` CLI 命令;"speckit" 即本框架 Spec Kit。

## Related Feature *(mandatory)*

**Feature ID**: 045  
**Feature Name**: Framework Source Provenance

## Overview

**定位**。`specify init` 在目标项目内生成 `.specify/` 工作区(模板、脚本、技能、指令),但产物**不携带任何框架来源标识**:目标项目无法回答"这套脚手架出自框架仓的哪一次提交"。本需求为 init 增加一个**落章(stamp)机制**:init 完成后,将当前框架源码的 **git commit id** 写入目标项目,使持有目标项目的人可以凭该 id 在框架仓反向定位产出这套产物的精确代码切片(如 `git show <commit>`)。**不使用正式版本号**:commit id 是唯一标识。

**现状锚点(以源码实测为准)**:

- init 实现于 `src/specify_cli/__init__.py`(`def init`,L2443 起;`init_git_repo` L2344),分发形态为 wheel(`pyproject.toml` `version = "0.0.22"`,hatchling 构建)——**已安装的 wheel 内没有 git 仓**,commit id 无法在 init 运行时从安装目录直接探测;开发/checkout 形态则可探测。
- 既有 `.specify/agents/<manifest>` JSON(`version: 1`)是 **per-tool agent 渲染跟踪**(记录渲染了哪些 agent 文件),与本需求正交,不承载框架来源。
- 目标项目侧 `.specify/instructions.md` 是指令真源,但其内容不含框架版本语义;升级路径(init 增量 copytree)不记录来源。

**核心不变量一句话**:commit id 是唯一版本标识——可得则真(与产出产物的框架源码一致)、不可得则明示(哨兵值 + 原因,绝不臆造);落章只随 init 发生;读取方零猜测。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - init 落章:目标项目获得可回溯的框架 commit 标识 (Priority: P1)

作为在项目中执行 `specify init` 的使用者,我希望 init 完成后目标项目内存在一份机器可读、人也可读的框架来源标识,记录产出本次脚手架的框架源码 commit id——让我(或接手的同事)随时能凭它在框架仓执行 `git show <commit>`,精确回答"这套 `.specify/` 来自哪个代码切片"。

**Why this priority**: 用户诉求的最小完整闭环:没有"落章 + 可回溯"这一步,刷新与降级都无从谈起。它自身即 MVP:一次 init,一份标识,一次成功回溯。

**Independent Test**: 在临时目录执行 init(框架源为已知 commit 的 checkout)→ 断言标识文件存在、commit id 等于框架仓 `git rev-parse HEAD` → 在框架仓执行 `git show <该 id>` 成功命中。

**Acceptance Scenarios**:

1. **Given** 一个空目标目录与一个处于已知 commit 的框架源, **When** `specify init`, **Then** 目标项目内出现来源标识文件([[STR-001]]),其 commit 字段为该框架 commit 的完整十六进制 id;init 正常完成,落章不改变 init 既有产物。
2. **Given** 已落章的目标项目, **When** 使用者凭标识中的 commit id 在框架仓执行 `git show <id>`, **Then** 成功定位产出该脚手架的代码切片,全程不需要目标项目保存框架仓副本。
3. **Given** 标识文件, **When** 工具解析, **Then** 至少可读出框架名([[STR-003]])与 commit id;文件为结构化格式,字段稳定,后续增量扩展不破坏既有字段。

---

### User Story 2 - 升级刷新:重复 init 更新标识,无旧值残留 (Priority: P2)

作为通过再次 `specify init` 升级项目脚手架的使用者,我希望落章随每次 init 刷新为**本次**框架源 commit——旧 commit 不残留、不误导,使回溯永远指向最近一次 init 的真实来源。

**Why this priority**: init 的升级路径(增量 copytree)是既有常规操作;若落章不刷新,标识会持续指向陈旧切片,比没有标识更糟(错误的回溯结论)。

**Independent Test**: 用 commit A 的框架源 init → 换 commit B 的框架源再次 init → 断言标识文件 commit 字段等于 B、文件中不存在 A 的值;两次 init 的其他产物行为不变。

**Acceptance Scenarios**:

1. **Given** 已由 commit A 落章的目标项目, **When** 以 commit B 的框架源再次 init, **Then** 标识刷新为 B;刷新仅改写标识自身,不破坏目标项目其他内容。
2. **Given** 从未落章的既有项目(本需求引入前 init 的存量项目), **When** 升级 init, **Then** 零迁移成本获得标识;读取方在标识缺失时视为"来源未知",不臆测。
3. **Given** 标识文件, **When** 检查其唯一性语义, **Then** 正式版本号(如 pyproject `0.0.22`)不作为标识键——即使未来顺带展示,唯一标识仍且仅是 commit id。

---

### User Story 3 - 不可得时的诚实降级:显式哨兵,绝不臆造 (Priority: P3)

作为在非常规环境(分发产物构建于框架仓之外、或运行环境无 git)中使用 init 的使用者,我希望 commit 真不可得时,落章**显式记录不可得**([[STR-002]] 哨兵值 + 原因),init 本身照常成功——而不是得到一个臆造的占位 id、也不是让 init 失败。

**Why this priority**: 落章是附随信息,不是门禁。诚实降级保证标识语义的可信度(有值必真),同时不把 init 的可用性绑在 git 可达性上。独立可测:构造无 git 信息的运行形态即可验证。

**Independent Test**: 在剥离 git 信息的环境执行 init → 断言标识文件存在、commit 字段为 [[STR-002]] 哨兵值并附原因;臆造 id 出现 0 次;init 退出成功。

**Acceptance Scenarios**:

1. **Given** 框架源 commit 无法解析的运行形态, **When** init, **Then** 标识文件落盘,commit 字段为 [[STR-002]],另附不可得原因;init 以成功退出码结束。
2. **Given** 开发/checkout 运行形态且框架工作树有未提交修改, **When** init, **Then** 标识仍指向 HEAD commit,并附带"工作树脏"标记(信息性)——脚手架实际含未提交内容时不冒充纯净 HEAD。
3. **Given** 任一形态的标识文件, **When** 读取, **Then** 三态语义明确:有效 commit / 显式不可得 / (文件缺失=来源未知);不存在第四种臆造态。

---

### Edge Cases

- 标识文件被使用者手工删除 → 下次 init 重新落章;读取方遇缺失按"来源未知"处理,不重建、不臆测。
- 框架仓为 shallow clone / commit 历史不完整 → 不影响落章(`git rev-parse HEAD` 仍可用);回溯方在框架仓能否 `git show` 取决于其自身克隆,不是落章的责任。
- 目标项目将 `.specify/` 纳入自身版本管理 → 标识随目标项目版本化,属预期行为;目标项目的提交与框架 commit 分属两轴,互不混淆。
- commit id 采用完整形式(40 位十六进制)→ 避免缩写在回溯时歧义;不提供缩写落盘选项。
- 标识文件字段未来扩展 → 既有字段名与语义 MUST 保持稳定(增量扩展,不重命名不重义)。
- init 的落章写入与既有 agents manifest 写入 → 相互独立,互不读取、互不覆盖。

## Requirements *(mandatory)*

### Functional Requirements

**落章与格式**

- **FR-001**: `specify init` 成功完成时,MUST 在目标项目写入一份框架来源标识文件(默认路径 [[STR-001]]),记录产出本次脚手架的框架源码 git commit id(完整十六进制形式)作为**唯一版本标识**。
- **FR-002**: 标识 MUST NOT 以正式版本号(如 pyproject version)作为标识键或唯一性依据;commit id 是唯一的来源判定依据。
- **FR-003**: 标识文件 MUST 机器可读且人可读:至少含框架名([[STR-003]])、commit id、落章时间戳(UTC);字段名与语义稳定,后续扩展 MUST 增量进行。

**可得性(跨安装形态)**

- **FR-004**: 标识 MUST 在两种常见运行形态下均可获得:运行于框架 git checkout 时 MUST 直接探测源仓 commit;以已安装分发行态运行时,MUST 依赖构建期嵌入分发行的源 commit 信息(init 运行时读取,不在安装目录臆测 git)。
- **FR-005**: commit 真不可得时,MUST 以 [[STR-002]] 哨兵值落章并附原因,MUST NOT 写入臆造/占位 id,MUST NOT 因落章失败而使 init 失败(落章是附随信息,非门禁)。

**刷新与兼容**

- **FR-006**: 重复 init(升级路径)MUST 将标识刷新为本次框架源 commit,旧值 MUST NOT 残留于标识文件;刷新 MUST 仅改写标识自身,MUST NOT 影响目标项目其他内容。
- **FR-007**: 本需求引入前的存量项目经升级 init 后 MUST 零迁移获得标识;标识缺失时读取方 MUST 视为"来源未知",MUST NOT 重建或推断。

**回溯闭环**

- **FR-008**: 仅凭标识文件内容(框架名 + commit id)MUST 足以在框架仓执行 `git show <commit>` 定位产出该脚手架的精确代码切片;回溯 MUST NOT 要求目标项目保存框架仓副本或网络访问。

### Key Entities *(include if requirement involves data)*

- **框架来源标识(Framework Source Stamp)**:一次 init 的来源记录实体——框架名、commit id(或哨兵值+原因)、UTC 落章时间戳;生命周期 = 随 init 落盘、随下次 init 刷新;单一落盘位置,不分散、不复制。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: checkout 形态 init 后,目标项目标识文件存在率 100%,且 commit id 与框架仓 `git rev-parse HEAD` 逐字符一致。
- **SC-002**: 回溯闭环:对若干不同框架 commit 产出的 init 产物,凭标识在框架仓执行 `git show` 100% 命中对应切片(0 次命中错误切片)。
- **SC-003**: 不可得形态下哨兵记录率 100%(臆造 id 出现 0 次),init 成功率与引入前一致(落章导致 init 失败的次数为 0)。
- **SC-004**: 升级刷新后旧 commit 残留率 0(标识恒反映最近一次 init 来源)。
- **SC-005**: 正式版本号被用作唯一标识的次数为 0。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 契约/集成测试——临时框架 checkout + 临时目标目录执行 init,断言 [[STR-001]] 存在且 commit 等于 `git rev-parse HEAD`。
- **SC-002 Source**: 集成测试——同一框架仓取 ≥2 个 commit 分别 init,对每个标识执行 `git show --quiet <id>` 断言退出码 0 且 id 各自正确。
- **SC-003 Source**: 契约测试——构造剥离 git 信息的运行形态,断言哨兵值与原因字段、init 退出码;扫描标识文件断言无臆造 40-hex。
- **SC-004 Source**: 集成测试——双 commit 先后 init,断言最终文件不含旧值(grep 旧 id 为 0 命中)。
- **SC-005 Source**: 契约测试——断言标识键字段的取值域不含 pyproject version;文档/代码评审确认唯一性表述。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | ".specify/source.json" | FR-001/FR-006/FR-007, US1 场景 1, SC-001/SC-004, 后续 contracts 与测试断言(2026-08-17 clarify 裁定:避开 024 保留的 .specify/version,与 Feature 名的 source 轴一致) |
| `STR-002` | "unavailable" | FR-005, US3 场景 1, SC-003(commit 不可得哨兵值) |
| `STR-003` | "spec-kit" | FR-003, US1 场景 3(标识文件中的框架名字段值) |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Out of Scope

- 正式版本号体系(semver 治理、版本比较、升级建议)——本需求明确不引入,commit id 是唯一标识。
- 框架仓多远端(github/gitee/gitlab)的 URL 解析与自动 clone——回溯动作由人在框架仓执行,标识不承诺网络能力。
- 目标项目内的"当前 stamp vs 上游最新"自动比对/升级提示——读取方后续另行需求。
- init 之外的落章/刷新入口(独立 refresh 命令、`/speckit.instructions` 写 stamp)——落章只随 init 发生。
- 工作树脏(dirty)标记——标识恒指 HEAD,不附脏标记(含内容级 diff 摘要);需要时另行需求。
- `.specify/` 内既有文件(instructions.md、agents manifest)的结构改动——落章为新增独立文件。

## Assumptions

- 标识文件路径与命名 [[STR-001]](单一 JSON 文件,UTF-8;2026-08-17 clarify 裁定,避开 024 的 schema 轴路径)。
- commit id 取完整 40 位十六进制;时间戳取 UTC ISO-8601。
- 落章写入发生在 init 流程末尾(产物落齐后),写入失败按 FR-005 的"不阻塞 init"处理并告警。
- "已安装分发行态"的构建期嵌入属于实现细节(构建钩子/打包步骤),其形态由 /speckit.plan 决定;本规格只约束其效果(FR-004)。
- 跨输入模态无关:落章由 init 进程自动完成,无用户输入面。

## Clarifications

### Session 2026-08-17

- Q: 已安装分发行态(wheel/sdist)的 commit 获取机制? → A: **构建期嵌入**——构建钩子在分发行内嵌入源 commit,init 运行时读嵌入值;checkout 形态直测不变(FR-004 原样确认)。实现将修改 pyproject/构建链(仓门禁 confirm 面),plan 阶段定具体钩子形态。
- Q: dirty 工作树标记如何处理? → A: **移除**——标识恒指 HEAD,不附脏标记;FR-005 收窄、US3 场景 2 删除、Key Entity 与 features/045.md 同步;Out of Scope 增补(dirty 标记整体出局,含内容级摘要)。无 FR/US 编号变动。
- Q: 落章文件最终路径? → A: `.specify/source.json`(STR-001 表行已改;引用经 [[STR-001]] 零改动)——避开 024 保留的 `.specify/version`,与 045「source 轴」命名一致。
- Q: 需求 043 绑定哪个 Feature? → A: **新建 Feature 045 Framework Source Provenance**:来源溯源(commit 轴)与 024 的 workspace schema 版本轴(迁移注册表/upgrade)正交;与 024 双向交叉引用并互相注明文件名保留(`.specify/version` 归 024 的 schema 标记设想);024 保持 Draft 不动。
