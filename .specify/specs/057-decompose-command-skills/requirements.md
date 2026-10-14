# Requirements Specification: agent/team/skills 命令的技能化分解补全(run-skills 与 run-team)

**Requirement Branch**: `057-decompose-command-skills`
**Created**: 2026-10-14
**Status**: Draft
**Input**: User description: "进一步分解agent,team,skills等/speckit.*命令…目前还缺少: 1) run-skills(运行未注册技能,自身必须注册到 agent,内部记录 internal/external 技能全部约定与框架内部结构) 2) improve-skills/merge-skills/think-skills 对应 modify 语义,不再新建 3) agent 系列已全,只需检查 /speckit.agents 正确使用这些技能 4) run-team — 将 /speckit.team run 流程提取为 run-team 技能"

## Related Feature *(mandatory)*

**Feature ID**: 057
**Feature Name**: 命令技能化分解补全

## Overview

本特性是 goal `command-logic-as-classified-skills`(T-001/T-003,命令核心逻辑尽可能由技能承载、命令模板只保留入口与委派)在 agent/team/skills 三个命令面上的补全:补齐缺失的 run 语义技能(run-skills、run-team),核查既有接线,不新建任何与既有技能语义重复的技能。

「internal / external 技能标注」的概念真源为 goal `.specify/goal/command-logic-as-classified-skills/goal.md`(internal = 只服务 spec-kit 框架自身逻辑;external = 与 spec-kit 无依赖、任何项目皆可直接使用);术语与消歧真源为词汇表条目「技能分类标注 (Skill Classification)」。约束侧读取:skill 化命令逻辑产出的新技能 MUST 带标注,否则干扰既有技能分发与处理体系(标注必要性为用户 2026-10-05 口述主张,经词汇表该条记录,引用时按其要求标注口述属性,非制品事实)。本特性新增的两个技能均落在 internal 层、均带标注;其中 run-skills 是「内部技能默认不被 agent 发现」规则的一个具名例外(见 Assumptions)。

### 现状锚点(以源码与目录实测为准,2026-10-14)

- **技能盘面**:`skills/external/` 实测 11 个技能目录(create-docs, create-pages, create-skills, database-utils, document-utils, draw-diagram, git-workspace, improve-docs, improve-skills, merge-skills, think-skills);`skills/internal/` 实测 35 个(analyze-artifacts … summarize-project,含 run-agent、create-agent、create-team、improve-agent、improve-team)。
- **run-skills / run-team 全树零命中**(grep 实测仅本规格草案出现)。
- **/speckit.agents**(41 行):意图表 3 行,run/空参 → `run-agent`、create → `create-agent`、refine → `improve-agent`,均按 runtime path 引用;团队操作外派 `/speckit.team`。与既有三个 agent 技能一一对应,无缺口。
- **/speckit.team**(104 行):三模式;create → `create-team`、modify → `improve-team`;**run 模式无专属技能**——路由行指向 `create-team` 执行路径,且 Run Mode § 六步流程(引擎五查预检、目标重述、双结构渲染、present & execute、`--target` 不变量、报告契约、输出纪律)全部**内联在命令模板中**;命令无 Delegation 节。
- **/speckit.skills**(63 行):路由表仅两行(NOT exists → `create-skills`、EXISTS → `improve-skills`);`merge-skills`、`think-skills` 已存在于 external 层但**未入路由**;无 run 语义路由。
- **发现模型分歧**:`.specify/skills.md` 指南声称 internal 技能 "not agent-visible — /speckit.* workflows consume them via explicit paths only";但本仓宿主(Qoder CLI)实测**发现并可直接调用 internal 技能**(本会话技能清单可见 create-requirements 等,加载自 `.qoder/skills/internal/…`)。「注册到 agent」因此是宿主相关观测,不是框架事实——run-skills 的解析 MUST 以工作区位置为准,不依赖宿主注册状态。

### Assumptions

- **「注册到 agent」= 宿主技能发现面使技能可被直接调用**(斜杠命令 / Skill 面)。不同宿主发现机制不同;**已裁定基准(2026-10-14 澄清)**:run-skills 按工作区位置解析、不依赖宿主注册状态;同名多命中时 dev 规范层(canonical)优先于 installed 镜像。run-skills 自身则 MUST 抵达宿主发现面(用户可直呼其名);对发现机制无法注册 internal 技能的宿主,降级路径为 `/speckit.skills` 的 run 意图路由(显式路径加载,功能等价可达)。
- run-skills 作为「internal 技能不被 agent 发现」规则的**具名例外**存在:`.specify/skills.md` 指南的相应表述随本特性更新,把例外写明——这既满足用户「必须注册到 agent」的硬要求,也不推翻其余 internal 技能的既有消费方式(显式路径引用)。
- **行为平价(behavior parity)是 run-team 提取的验收基线**:Run Mode 流程是搬家而非重设计——每条既有义务以同等或更严强度落入 run-team,语义逐条可追溯;FR-010 对五查/`--target` 等义务仅作**点名锚定**用于平价比对,不搬运其定义正文(现行真源 `templates/commands/team.md` § Run Mode,落盘后真源移交 run-team)。
- 本特性不改任何既有技能的**外部行为**;FR-015 把命令侧残留细节移入对应技能属内容吸收,不算行为变更。接线漂移修命令模板路由行;技能自身缺陷不在本特性范围,记录后走 improve 流程。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - run-skills:运行未注册技能的统一入口 (Priority: P1)

agent 用户想执行一个技能,但它没有被宿主 agent 发现(没有可直呼的斜杠命令)——例如刚由 create-skills 产出尚未随镜像/安装抵达宿主发现面的技能、或宿主只扫描部分层。用户直接调用 **run-skills**(它自身已注册到 agent、可直呼),给出技能名或路径;run-skills 在框架已知技能位置间做确定性解析,加载命中的 `SKILL.md`,按其正文执行并把该技能自己的产出转述给用户。run-skills 是运行入口而非「未注册专用门」:已注册目标照常可跑并获非阻断提示(FR-007)。

**Why this priority**:用户点名的第一个缺口;skills 命令族 run 语义的唯一载体,且是唯一要求「自身注册到 agent」的新实体——没有它,run 语义只能靠人工读路径执行。

**Independent Test**:在工作区放一个有效 `SKILL.md` 但宿主未发现它;仅凭 run-skills 一次调用即完成解析、加载、执行并转述产出,无需任何其他环境指令。

**Acceptance Scenarios**:

1. **Given** 工作区某技能位置存在带合法 `SKILL.md` 的技能且宿主未注册它, **When** 用户以技能名调用 run-skills, **Then** run-skills 按其文档化的搜索顺序解析出规范路径并披露所选路径,加载并按 `SKILL.md` 正文执行,转述该技能自身的产出/报告。
2. **Given** 同名技能命中多个位置, **When** 解析时, **Then** 应用 run-skills 文档化的确定性优先级并在输出中披露所选路径;用户可用显式路径覆盖。
3. **Given** 技能名未命中任何位置, **When** 调用 run-skills, **Then** 停在异常点并给出可行动错误,逐项列出已搜索的位置(快速失败,无静默兜底)。
4. **Given** 目标技能其实已被宿主注册, **When** 经 run-skills 调用, **Then** 照常执行,并披露「可直接用斜杠命令调用」的非阻断提示。
5. **Given** 非 Spec-Kit 部署(无 `.specify/`), **When** 运行 external 目标技能, **Then** 按 runtime-mode 纪律降级执行(框架耦合步骤跳过,技能主体照跑)。

---

### User Story 2 - run-team:/speckit.team run 流程提取为技能 (Priority: P1)

用户运行 `/speckit.team run <slug>`,体验与今天完全一致(五查预检 → 目标重述 → 双结构渲染 → present & execute → 报告),但命令模板不再承载这段流程——run 语义的全部义务移入 **run-team** 技能,`/speckit.team` 收缩为入口 + 意图路由 + 委派表。

**Why this priority**:用户点名的第二个缺口;它直接兑现 goal 判据「命令只包含该调用哪些技能以及如何调用」在 team 面的落地,并消除命令模板中最大一块内联流程。

**Independent Test**:结构上验证 team.md 的 Run Mode 程序性步骤清零、路由行指向 run-team;行为上按既有 Run Mode 义务清单逐条对映,零丢失。

**Acceptance Scenarios**:

1. **Given** `.specify/teams/` 下存在某团队, **When** `/speckit.team run <slug>` 执行, **Then** 命令委派给 run-team,执行流程与现行内联流程义务逐条等价(五查预检仍以 goal-utils 引擎为唯一判定点、`--target` 解析顺序与不变量不变、报告契约含 Target 指派字段、输出纪律不变)。
2. **Given** 提取完成, **When** 读 team.md, **Then** Run Mode 程序性细节不复存在——只余路由行(run → run-team)与委派所需的输入/产出说明;create/modify 两行不变。
3. **Given** run-team 执行中需要派发子代理(按团队 pattern 编排), **When** 派发, **Then** 沿用现行派发治理(subagent-definitions 的模态、快速失败注入子句、异常回传行),提取不降低任何治理强度。
4. **Given** continuous 循环团队, **When** run, **Then** 分级门控与现行一致(平价覆盖,不因提取而放开)。

---

### User Story 3 - 接线核查与 modify 语义封口 (Priority: P2)

对 agent/skills 两个命令面做接线核查:**不新建任何与既有技能语义重复的技能**。/speckit.agents 的意图表逐行核对到既有三个 agent 技能;/speckit.skills 的 modify 语义由既有 improve-skills(常规改优)、merge-skills(合并)、think-skills(思想演练/模拟执行)承载,路由表补齐相应意图行并接入 run-skills(run 语义)。

**Why this priority**:纯核查与路由行修补,无新能力;但它是「不造重复技能」这一用户约束的落点,也是 run-skills 被命令面触达的接线。

**Independent Test**:对三个命令模板的路由表逐行断言:每个语义族(create/modify/run)的每一行都指向既有技能的规范 runtime path,零指向不存在的技能、零语义重复的新技能。

**Acceptance Scenarios**:

1. **Given** /speckit.agents 现行意图表, **When** 逐行核对, **Then** run/空参 → run-agent、create → create-agent、refine → improve-agent,路径与输入/产出描述与技能实况一致;发现漂移即修路由行(不改技能)。
2. **Given** /speckit.skills 路由表, **When** 核对, **Then** create 行不变;modify 语义族三技能(improve-skills / merge-skills / think-skills)按意图各有路由行;run 意图 → run-skills。
3. **Given** 三个命令模板, **When** 审查, **Then** 除「调用哪个技能 + 输入/产出」外的操作细节均已落在技能侧(goal `command-logic-as-classified-skills` 判据 1)。

---

### Edge Cases

- **同名技能跨层命中**(如同名存在于 external 与 internal 层,或 dev 规范层与 installed 镜像层不一致):run-skills 按文档化优先级解析并披露所选路径;优先级必须在技能内一次性写明,不临场裁量。
- **目标 `SKILL.md` 存在但无效**(frontmatter 缺失/损坏、正文为空):快速失败,报可行动错误(路径 + 缺陷),不静默跳过、不猜测意图。
- **把 `/speckit.*` 命令名当技能名喂给 run-skills**(如 `run-skills requirements`):命令不是技能——run-skills 报告该名字属命令面并指向对应 `/speckit.*` 入口,不强行执行。
- **run-team 目标团队不存在**:`.specify/teams/` 下无匹配 slug → 沿用现行 "team not found" 语义并提示 create 路径(平价,行为不变)。
- **run-skills 被要求运行的对象是自身**(run-skills 递归调用 run-skills):合法(它也是技能),但输出披露这一点;无特殊分支逻辑。

## Requirements *(mandatory)*

### Functional Requirements

#### 术语、分层与注册面(US1/US3)

- **FR-001**: 系统 MUST 新增两个 internal 技能,规范路径分别为 [[STR-001]] 与 [[STR-002]](canonical 落 `skills/internal/<name>/`,镜像到 `.specify/skills/internal/<name>/`,按 sync-mirrors 模型),frontmatter 带内部技能标注,「技能分类标注」约束侧规则对二者生效。
- **FR-002**: run-skills MUST 注册到 agent(抵达宿主技能发现面、可被用户直接调用),作为「internal 技能不被 agent 发现」规则的具名例外;`.specify/skills.md` 指南 MUST 同步更新,写明该例外及其理由(运行未注册技能的入口本身必须可被调用),其余 internal 技能的显式路径消费方式不变。对发现机制无法注册 internal 技能的宿主,降级路径 MUST 存在:`/speckit.skills` 的 run 意图路由以显式路径加载同一技能,功能等价可达。

#### run-skills 解析与执行(US1)

- **FR-003**: run-skills MUST 接受技能标识(名称或规范路径)为输入,在框架已知技能位置集(dev 规范层 `skills/external/`、`skills/internal/`;installed 层 `.specify/skills/` 平铺与 `internal/` 嵌套)间做**确定性解析**;同名多命中时的优先级**已裁定(2026-10-14)**:dev 规范层(canonical)优先于 installed 镜像,优先级在技能体内一次性写明。**信任边界(已裁定)**:显式路径输入 MUST 落在上述已知技能位置集内,越界路径按 FR-004 快速失败。所选路径 MUST 在输出中披露。
- **FR-004**: 解析零命中、目标 `SKILL.md` 无效、或显式路径越出已知技能位置集时,run-skills MUST 停在异常点并输出可行动错误(逐项列出已搜索位置,或指出文件缺陷/路径越界),MUST NOT 静默兜底、MUST NOT 降级为近似猜测(快速失败纪律)。
- **FR-005**: run-skills MUST 以「加载并遵照目标技能 `SKILL.md` 正文执行」的方式运行该技能(输入按调用方接线、产出转述回调用方),MUST NOT 将任一目标技能的逻辑内联复制进自身。
- **FR-006**: run-skills 技能体 MUST 自足到「无本仓 ambient 指令的 agent 仅读它即可完成一次运行」:以**引用真源 + 内联最小操作事实**记录框架约定——技能分层与各层规范路径、internal/external 标注语义(真源 goal `.specify/goal/command-logic-as-classified-skills/goal.md` 与词汇表条目)、发现无注册表规则与 `.github/skills` 兼容链接、镜像模型(改 canonical 不改镜像)、`${SKILL_HOME}`/`${SKILL_WORKDIR}` 路径约定、runtime-mode 门控;其中位置搜索顺序作为最小操作事实内联,其余一律引用既有真源,不复制其规则正文(One Source Of Truth)。
- **FR-007**: run-skills 对任意目标技能(含已注册者)照常执行;「已注册」判定为**尽力检测**(2026-10-14 裁定:按工作区内宿主扫描目录近似判断——注册是宿主相关观测,技能体内无确定性来源),判不准也照常执行,提示措辞为「可能可直接斜杠调用」(非阻断)。
- **FR-008**: run-skills MUST 按 runtime-mode 纪律门控:非 Spec-Kit 部署下 external 目标技能照常可运行,框架耦合步骤按门控降级,不因缺 `.specify/` 而整体失败;非 Spec-Kit 部署下 **internal 目标技能拒绝执行**并给出可行动错误(internal 技能按 goal T-002 配合 `.specify/` 目录结构,离开该结构无运行意义)。

#### run-team 提取与平价(US2)

- **FR-009**: `/speckit.team` 的 run 模式 MUST 委派给 [[STR-002]] 技能;命令模板的 Run Mode 程序性内容清零,仅保留路由行与该技能的输入/产出说明(goal T-003:命令只记录调用哪些技能与每个技能的输入和产出)。
- **FR-010**: run-team MUST 以**行为平价**承接现行 Run Mode 全部义务——五查预检(goal-utils 引擎为唯一判定点、`not-evaluated` 语义、blocked/退出码)、目标重述、静态/动态结构渲染、present & execute(披露非门禁)、`--target` 解析顺序(显式 > focus_target > 无)与全部不变量、按 pattern 编排(territory 校验、DAG 无环、迭代上限、continuous 单轮与独立校验者)、派发治理(subagent-definitions 模态 + 快速失败注入子句 + 异常回传行)、报告契约(强制含 `## Verification`、Target 指派字段逐字形态、`target_ref` 台账)、输出纪律(`.work/` 中转)——每条义务以同等或更严强度落进技能,零丢失;落盘后这些义务的真源由 team.md § Run Mode 移交 run-team,team.md 改为引用。
- **FR-011**: team.md 的 Modes → Capability Routing 表 MUST 更新 run 行指向 run-team;create → create-team、modify → improve-team 两行不变;run 行不再指向 create-team 执行路径。
- **FR-012**: run-team 的边界与 /speckit.team 一致:单代理操作外派 `/speckit.agents`,不承接 create/modify 语义(那是既有两技能的职责),提交流程不改写任何既有语义。

#### 接线核查与 modify 封口(US3)

- **FR-013**: `/speckit.agents` 意图表 MUST 逐行核对到既有三个 agent 技能(run/空参 → run-agent、create → create-agent、refine → improve-agent),路径、输入/产出描述与技能实况一致;漂移修路由行,MUST NOT 新建 agent 系技能。
- **FR-014**: `/speckit.skills` 路由表 MUST 补齐 modify 族意图行——常规改优 → improve-skills、合并 → merge-skills、思想演练/模拟执行 → think-skills——并新增 run 意图 → run-skills(runtime path [[STR-001]]);create 行不变;MUST NOT 新建任何 modify 或 run 语义的新技能(用户裁定:三者已覆盖 modify 语义)。
- **FR-015**: 三个命令模板(agents.md / team.md / skills.md)MUST NOT 在「调用哪个技能 + 输入/产出」之外承载操作细节;发现残留细节即移入对应技能或真源文档,命令侧只留引用。

### Key Entities *(include if requirement involves data)*

- **Skill Descriptor(技能描述符)**: 技能的可定位身份——名称、层(internal/external)、canonical 路径、installed 镜像路径、`SKILL.md` 有效性、宿主注册状态(宿主相关观测,非框架事实);run-skills 的解析对象。**身份/唯一性(2026-10-14 裁定)**:以 canonical 路径为准——同一技能的 installed 镜像副本不是独立技能(镜像 = 投影);同名且不同 canonical 路径是两个技能,冲突经 FR-003 优先级消解。
- **技能位置搜索顺序(Skill Location Search Order)**: run-skills 一次解析所 travers 的有序位置清单与同名多命中优先级;真源为 run-skills 技能体(FR-006 内联的最小操作事实)。
- **Team Run Flow Obligation Set(团队运行义务集)**: 从 team.md § Run Mode 提取、由 run-team 承接的义务清单(五查预检/渲染/编排/派发治理/报告/输出纪律);落盘前真源 team.md,落盘后真源 run-team。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对工作区内任一带合法 `SKILL.md` 且宿主未注册的技能,仅凭 run-skills 一次调用(无其他环境指令)即完成解析、加载、执行并转述产出——新会话/新上下文可用。
- **SC-002**: run-skills 解析确定性:同一输入恒得同一路径;零命中输出逐项列出全部已搜索位置;多命中披露优先级与所选路径。
- **SC-003**: run-team 行为平价:现行 team.md § Run Mode 义务清单逐条对映到 run-team,丢失义务数为 0,每条强度同级或更严。
- **SC-004**: 结构收敛可测:team.md 的 Run Mode 节**程序性内容为 0**——无程序性编号步骤/祈使流程,仅存路由行(run → [[STR-002]])与该技能的输入/产出说明;skills.md 路由表覆盖 3 个语义族、共 5 行路由(create 1 + modify 族 3:improve-skills/merge-skills/think-skills + run → [[STR-001]]);agents.md 意图表 3 行全部指向既有技能;全树无与既有技能语义重复的新技能目录。
- **SC-005**: run-skills 的可调用性以框架自有交付物判定:[[STR-001]] 存在于规范层且镜像同步、`.specify/skills.md` 指南载明 internal 例外条目、本仓宿主技能发现面可见该技能——前两项是判定指标,末项是宿主观测指标(2026-10-14 裁定,宿主可见性单独成立不构成通过)。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 新上下文执行记录(fresh-context 调用 run-skills 运行一个宿主未发现的技能,产出该技能自身的报告)。
- **SC-002 Source**: run-skills 的解析行为记录(零命中/多命中/唯一命中三类输入各一例的实跑输出)。
- **SC-003 Source**: 义务对映表(tasks.md 产物):现行 Run Mode 逐条义务 × run-team 落点 × 强度判定;评审抽样核对。
- **SC-004 Source**: 结构断言(grep/契约测试):team.md 步骤计数、三个路由表逐行、`skills/{external,internal}/` 目录清单对语义重复的排查。
- **SC-005 Source**: 本仓宿主技能发现面清单 + `.specify/skills.md` 指南文本断言。

## Shared Strings

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `skills/internal/run-skills` | FR-001, FR-014, SC-004, SC-005, tasks T-NNN, contracts/run-skills-wiring.md |
| `STR-002` | `skills/internal/run-team` | FR-001, FR-009, SC-004, tasks T-NNN, contracts/run-skills-wiring.md |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

<!--
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->

### Session 2026-10-14

- Q: Related Feature 绑定到哪个 Feature? → A: 新建 Feature 057「命令技能化分解补全」(候选 013 Skills Command / 019 Agents Command / 026 Agent Skill Enablement / 027 Team Management / 039 Harvested Harness Improvements 均 Implemented;无单一既有 Feature 覆盖跨 agents/team/skills 三个命令面的分解工作,027 明文把 run 编排留在 create-team,绑定需先改其范围记录)
- Q: run-skills 的解析基准与同名多命中优先级? → A: 已裁定基准 = 按工作区位置解析、不依赖宿主注册状态;同名多命中 dev 规范层(canonical)优先于 installed 镜像
- Q: 显式路径输入的信任边界? → A: 限已知技能位置集内,越界快速失败并给可行动错误
- Q: FR-007 的已注册目标斜杠提示如何检测注册状态? → A: 尽力检测——按工作区内宿主扫描目录近似判断,判不准也照常执行,措辞「可能可直接斜杠调用」(非阻断)
