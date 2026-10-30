# Requirements Specification: Coaching Skills（教练技能）

**Requirement Branch**: `078-coaching-skills`  
**Created**: 2026-10-30  
**Status**: Draft  
**Flow Class**: execution
**Flow Type**: -
**Input**: User description: "将外部技能 think-skills 重命名并重构为 coaching-skills（教练技能）。

命名与意象：coaching-skills 取「教练」意象——站在场边观察 → 发现动作/行为的偏差 → 给出具体微调建议（tweaks/adjustments）。它不再只是静态心智推演，而是「先给预期，再看真实执行，最后给微调」的教练闭环。

执行逻辑（必须全部覆盖）：
1) Coach 自身是技能，通过参数传入一个 Trainee 技能（名称或路径，external/internal 均可）。
2) 定位并理解 Trainee 技能；沿用原 think-skills 的心智模拟流程，在真实执行之前产出「执行预期」。预期同时覆盖执行结果与执行过程：结果以「正确性」衡量（应产出什么、验收判据、允许偏差），过程以「效率」衡量（预计步骤数、工具调用、重试/冗余、关键路径）。
3) 用一个子代理执行 Trainee 技能完成实际工作；Coach 在自己的 session 中观察并记录子代理执行 Trainee 的过程与结果（需要可观测的执行记录契约，如逐步日志/工具调用/产物/耗时；子代理不可见的部分要显式标注为观测缺口）。
4) 依据「预期 vs 实际」整理 Trainee 的提升计划，然后调用 improve-skills 针对该 Trainee 进行优化。

主次原则：本技能以「按 Trainee 原本流程完成实际工作」为主，以「对 Trainee 技能做优化」为辅；不得为了收集优化素材而忽略或简化 Trainee 的正确执行流程。优化动作只在执行闭环完成后进行。

重命名与兼容面（已实测的影响面）：
- 重命名必须同时改身份坐标：源目录 skills/external/<name>/、frontmatter name、skill_id / Resource ID（Canonical ID/Path）、运行时 unit id skill:<name>、flow-class 定义行、probe 定义行与 probe id、/speckit.skills 路由表行与路径、description 触发词。
- 已知引用面：77 个受版本管理文件；需手改的源码 19 个（技能本体 2、路由模板 1、agents 2、create-agent 角色模板 4、run-skills 1、shared/definitions 2、src/specify_cli OBSOLETE 名册 1、docs 2、contract tests 4）。派生面（.specify 镜像、命令副本、.qoder/.claude/.github agents、Wrap-up 编译块、probe-map）只能再生成，不能手改。
- 旧项目兼容：旧目录名必须进入 src/specify_cli/__init__.py 的 _OBSOLETE_SKILLS，使升级后的项目删除残留目录；升级不得删除用户自建的同名符号链接。
- 四个冻结基线测试（test_expression_compatibility、test_migration_distribution、test_skill_layer_visibility_guards、test_run_skills_wiring）必须显式更新并注明日期与理由，不得静默改计数。
- 历史记录（.specify/specs/**、memory/evidence/**、features/*.md、reviews、eval-baseline、按旧 unit id 归档的 run 记录）不改写、不回填。

触发与用户面：用户面触发词要覆盖「教练 / 陪练 / 观察执行 / 预期 vs 实际 / 执行偏差 / 微调建议 / coaching」等；重命名后旧触发词是否保留由设计决定，但必须在 description 里明确新的可调用方式（含 Trainee 参数形式）。/speckit.skills 的 modify 路由行要改为 coaching-skills 并保留对 Trainee 的传参说明。

非目标：不新增第二套子代理派发机制，复用宿主原生子代理 / 既有 run-agent / run-skills 能力；不改变 improve-skills 的契约，只按既有入口调用它；不做多 Trainee 并行教练、不做自动合并、不做历史 run 记录迁移；不把 coaching-skills 做成 internal 技能，保持 external 分层。"

## Related Feature *(mandatory)*

**Feature ID**: 078  
**Feature Name**: Coaching Skills（教练技能）

## Assumptions（对输入中开放点的缺省裁决，clarify 阶段可推翻）

- **A1（编号依据）**：编号 078 由脚手架 `create-new-requirements.sh` 按 `.specify/specs/` 实测最大目录号（077）加一得出；`features.md` 的行数不是最大编号，两者不一致属既有状态，本特性不借机回填。
- **A2（类别判定 = execution）**：本特性的交付物是技能定义、路由/定义/名册接线与契约测试；验收时由宿主解析技能、由确定性检查器与契约测试消费，缺陷以「技能解析不到 / 路由指向旧名 / 单元 id 不匹配」这类机器可见差异暴露，按 `.specify/shared/definitions/flow-class-definitions.md` 判据属 `execution`，`Flow Type` 写 `-`。
- **A3（命名裁决）**：`coaching-skills` 取自用户指令，按 Grounded Naming 优先级高于工程惯例与同族仿写；全仓撞名扫描（目录 + 全部 `SKILL.md` 的 `name`）结果为 0 命中。与既有 `create/improve/merge/run-skills` 的「技能管理族」后缀语义重叠是**已知且有意的**：本技能的核心动作是「带一个 Trainee 跑一次真实流程」，不是修改技能本身。
- **A4（参数形态）**：调用形态为 `coaching-skills <trainee-name|trainee-path> <work>`，一次一个 Trainee 与一件真实工作；`<work>` 是工作本身（目标、输入、期望交付），教练与子代理**各自在本方上下文中独立理解**。任一参数缺失时技能 MUST 用一句普通澄清询问并停止（**不是确认门**，不新增 BLOCKING 命中），不得自行选题。**旧触发词中纯静态推演的说法（thought experiment / 思想实验 / 不要真的执行）MUST NOT 保留**——它们承诺零副作用，与本技能会真实派发子代理相矛盾；只保留能表达「先给预期、再看真实执行」的说法。」
- **A5（派发机制与优先级）**：复用宿主原生子代理派发；**两者都存在时原生派发优先**，`run-agent` 仅作降级入口；`run-skills` 只负责解析并执行 Trainee，**本身不承担派发**。子代理内部按 Trainee 自身 SKILL.md 执行。不新增第二套派发机制；实际采用哪条路径 MUST 记入观测记录。
- **A6（观测通道与缺省）**：宿主能看到子代理事件时以**宿主事件**为主（字段标 [[STR-011]]）；看不到时子代理 MUST 回传结构化记录（逐步动作、工具调用、产物、耗时、状态变化，字段标 [[STR-012]]）；两通道都有时字段级冲突以宿主事件为准。两者都拿不到的步骤以 [[STR-006]] 标注为观测缺口，**不得编造**；缺口不计入效率评分，但必须在报告中计数与点名。
- **A7（两个新概念无既有 owner）**：本文定义的「结果—正确性」与「过程—效率」在框架内无既有 owner；本文是它们的首个定义点，plan/contracts 可细化但 MUST NOT 另立第二份定义。它们与 `run-determination` 的四量（token 消耗/耗时/制品正确性/满意度）不是同一组概念：后者描述一次运行的判定，前者描述「Trainee 相对预期」的偏差。
- **A8（旧项目升级）**：旧目录名进入 `_OBSOLETE_SKILLS` 后，`specify init` 的加性 copytree 会留下旧目录，清理步骤 MUST 删除该**实体目录**，但 MUST NOT 删除用户自建的同名**符号链接**（既有清理纪律：符号链接可能是用户别名）。
- **A9（历史不改写）**：不改写的边界是**本特性 `078-coaching-skills` 自己的产物目录之外的既有记录**——其他特性的 `.specify/specs/<其他特性>/**`、`memory/evidence/**`、`features/<其他ID>.md`、reviews、eval-baseline、按 `skill:think-skills` 归档的 run/feedback 记录均为 dated record，不改写、不回填。本特性自身的产物（`.specify/specs/078-coaching-skills/**`、`.specify/memory/features/078.md` 与本特性新写入的 run/feedback 记录）不属历史记录，MUST 可正常改写与重跑；新名的 run 从空历史开始（不继承旧名 run 记录）。
- **A10（封闭清单判据）**：「活接线面」是封闭集——本特性开始前实测的 19 个需手改源文件（技能本体 2、路由模板 1、agents 2、create-agent 角色模板 4、run-skills 1、shared/definitions 2、src `_OBSOLETE_SKILLS` 1、docs 2、contract tests 4），加上由它们再生成的派生面；SC-006 / SC-008 的零残留与零漂移判据以该封闭集为参照，历史记录不在集合内（A9）。**允许差异集恰为一项**：`_OBSOLETE_SKILLS` 中保留旧名的那一行（FR-020 要求它必须存在）；除此之外空集。
- **A11（零新增门禁）**：门控预算整数余量当前为 0（既有 owner 记载），本特性 MUST NOT 在扫描面新增任何命中 `BLOCKING_PATTERNS` 的文案；判定单位是 `git diff` 的**新增行**而非总量（总量相等允许「加一门、删一门」的规避）。技能流程中的「暂停询问」措辞 MUST 按既有门禁纪律书写，且不得以确认门形态表达。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一次教练闭环：先给预期，再看真实执行，最后给微调 (Priority: P1)

用户带着一个 Trainee 技能与一件真实工作调用 `coaching-skills`。技能先产出执行预期（结果正确性与过程效率两类判据），再派发一个子代理按 Trainee 自己的流程完成工作，教练在自己的 session 里记录过程与结果，最后给出提升计划并调用 `improve-skills`。

**Why this priority**: 这是本特性的全部价值所在；没有这条闭环，重命名只是换名字。

**Independent Test**: 用一个夹具 Trainee 与一件夹具工作跑一次完整教练运行，检查四个产物按序存在：执行预期 → 观测记录 → 偏差报告 → 提升计划；且夹具工作的主产物已真实产生。

**Acceptance Scenarios**:

1. **Given** 一个可解析的 Trainee 与一件真实工作，**When** 用户调用 `coaching-skills <trainee>`，**Then** 技能在任何子代理派发之前先写出执行预期，并在派发后产出观测记录、偏差报告与提升计划。
2. **Given** Trainee 的主流程会产出某个工件，**When** 子代理执行完成，**Then** 该工件真实存在，且教练的观测记录能逐步对应到 Trainee 的流程步骤。
3. **Given** `improve-skills` 在本环境不可用或优化被拒绝，**When** 执行闭环已完成且主工件已按判据完成，**Then** `run: success` 且优化状态按 [[STR-010]] 单列，不把执行判为失败。

---

### User Story 2 - 预期必须双维度可判定 (Priority: P1)

执行预期不是一段感想：结果面写清应产出什么、验收判据与允许偏差；过程面写清预计步骤数、工具调用轮廓、重试/冗余余量与关键路径。两类判据都能在执行后被逐条核对。

**Why this priority**: 没有可判定的预期，后面的「偏差」与「提升计划」都无从谈起。

**Independent Test**: 给一个含已知正确性缺陷与已知效率退化的夹具 Trainee 写预期，执行后偏差报告必须在这两个维度各至少给出一条带证据的偏差。

**Acceptance Scenarios**:

1. **Given** 一个 Trainee 流程，**When** 教练产出预期，**Then** 预期同时包含[[STR-008]]与[[STR-009]]两个小节，且每个判据都有可核对对象（工件名、检查项、步骤/调用数量级或关键路径节点）。
2. **Given** 预期中某项无法从 Trainee 文本推导，**When** 写预期，**Then** 该项被标为未知/校验缺口，而不是补一个看似合理的数字。

---

### User Story 3 - 子代理真实执行，教练只观测不代跑 (Priority: P2)

教练派发一个子代理执行 Trainee 的真实工作，自己只观察与记录；子代理不可见的步骤显式标为观测缺口，绝不编造。

**Why this priority**: 「真实执行」与「可审计的观测」是教练与静态推演的分水岭；但它的价值依赖 US1 的闭环成立。

**Independent Test**: 构造一个含不可观测步骤的夹具执行，检查记录中恰好出现一条[[STR-006]]标记且没有任何被编造的步骤。

**Acceptance Scenarios**:

1. **Given** 一次派发，**When** 子代理按 Trainee 流程执行，**Then** 观测记录逐步含触发/指令、动作、工具调用、状态变化、产物与耗时，并注明观测来源。
2. **Given** 某步骤在教练侧不可见，**When** 记录，**Then** 该步骤标[[STR-006]]并计入缺口清单，而不是被省略或补写。
3. **Given** 子代理失败、超时或被拒绝，**When** 记录，**Then** 失败被如实记录，运行不会被叙述为完成。

---

### User Story 4 - 重命名后调用面与分发面一致，旧项目可平滑升级 (Priority: P2)

技能改名为 `coaching-skills` 后，用户触发词、`/speckit.skills` 路由、运行时 unit id、flow-class 与 probe 定义、镜像与命令副本全部一致；已安装旧名的项目升级后旧目录被清理，用户自建的同名链接不受影响。

**Why this priority**: 不一致的重命名会让技能「文件在但叫不出来」或「叫得出来但统计不到」。

**Independent Test**: 在新树上跑 `flow-class-check`、probe 编译检查、镜像/副本漂移检查与四个冻结基线测试；再用一个含旧目录与用户同名列链接的夹具项目跑一次 `specify init`。

**Acceptance Scenarios**:

1. **Given** 重命名已落地，**When** 检查活接线面，**Then** [[STR-002]] 在活接线面出现 0 次，[[STR-001]] 在技能目录、frontmatter、skill_id、路由行、flow-class 行与 probe 行中一致出现。
2. **Given** 一个已安装旧名的项目，**When** 运行 `specify init`，**Then** 旧实体目录被删除，而用户自建的旧名符号链接保留。
3. **Given** 派生面，**When** 运行镜像与命令副本的 `--check`，**Then** 两者均零漂移。

### Edge Cases

- Trainee 名称同时存在于 external 与 internal 两层：MUST 停止并点名两个候选，不得就近择一。
- `<work>` 缺失或为空：MUST 用一句普通澄清询问并停止，不派发子代理。
- 教练在预期阶段已对 `<work>` 形成结论：MUST 不把该结论写入派发载荷（FR-009/FR-029）；否则双上下文独立读数被压成一份。
- Trainee 目录存在但 `SKILL.md` 缺失或 frontmatter 非法：MUST 在预期阶段之前拒绝，不派发子代理。
- Trainee 就是 `coaching-skills` 自身：MUST 拒绝递归教练（深度只允许 1），不派发。
- Trainee 流程含破坏性/需确认步骤：子代理 MUST 遵循 Trainee 自身的确认门；教练 MUST 在派发前把该门作为**用户确认点**转达（破坏性动作保留前置确认，属既有治理门而非新增门），拿到答复后再派发；MUST NOT 为了「跑通」而替它跳过，也 MUST NOT 让子代理自行批准。
- 子代理产出了工件但流程中途失败：主结果按 Trainee 流程的真实状态报告（部分完成），偏差报告必须区分「结果偏差」与「过程偏差」。
- 观测记录为空或子代理未回传日志：MUST 把缺口如实计入并以 `evidence: none` 标记提升计划、`run: partial` 收束——**计划仍要产出**（US1 的四产物不因证据缺失而少一件），但每条微调 MUST 标注为无执行证据的假设。
- `improve-skills` 存在但拒绝该目标：运行以 Trainee 产出为主结果结束，优化状态单列，不重试到无限。
- 用户在运行中只想要执行、不想要优化：MUST 允许在闭环完成后跳过优化，并明确报告 `optimization: skipped`（[[STR-010]] 的封闭值之一）。

## Requirements *(mandatory)*

### Functional Requirements

#### A. Trainee 参数与解析

- **FR-001**: [[STR-001]] MUST 恰好接受两个位置参数：Trainee 目标（技能名或路径）与真实工作 `<work>`（非空）；任一缺失 MUST fail-closed 并点名缺失项。Trainee 目标MUST 复用 `run-skills` 的解析语义（canonical 优先于镜像）覆盖 external（`skills/external/<name>`、`.specify/skills/<name>`）与 internal（`skills/internal/<name>`、`.specify/skills/internal/<name>`）两层。源与镜像指向同一技能时 MUST 视为**同一个命中**，不构成同名冲突；仅当 external 与 internal 两层各有一个同名技能时 MUST fail-closed、点名两个候选并停止；未找到时 MUST fail-closed 并点名目标坐标。MUST NOT 就近择一或猜路径。`<work>` MUST 原样进入 [[STR-007]] 与子代理载荷，教练 MUST NOT 用它替换 Trainee 目标或反过来。
- **FR-002**: Coach MUST 在写预期之前读取 Trainee 的 `SKILL.md` 与执行所必需的引用文件；此阶段 MUST NOT 修改 Trainee 的任何文件，也 MUST NOT 触发 Trainee 的副作用。
- **FR-003**: Trainee 解析 MUST 复用既有解析入口（`run-skills` 的解析语义），MUST NOT 新增第二套技能定位规则；当宿主只能显式路径加载时，MUST 走 `run-skills` 的既有降级路径。

#### B. 执行预期（[[STR-007]]）

- **FR-004**: Coach MUST 在任何子代理派发之前产出并落盘 [[STR-007]]（文件 [[STR-014]]，位于运行目录 [[STR-013]]）；该产物 MUST 同时包含[[STR-008]]与[[STR-009]]两个小节，缺一即判运行不合格。
- **FR-005**: [[STR-008]] MUST 逐条声明：应产出的工件/结论、验收判据、允许偏差；每条 MUST 在执行后可被观测记录逐条核对（可核对对象为工件路径、检查项或明确判定语句）。**主工件 MUST 由 [[STR-008]] 的第一条判据点名**；没有工件形态产出的 Trainee，其第一条判据 MUST 点名一个可核对的结论（决定/报告/判定语句）。**允许偏差 MUST 是可判定的形态**——要么二值通过/不通过，要么给出数值/区间容差与越界严重度；MUST NOT 留下「大致符合」这类不可判定的措辞。
- **FR-006**: [[STR-009]] MUST 逐条声明：预计步骤数量级、工具调用轮廓、允许的重试/冗余、关键路径节点；每项 MUST 从 Trainee 文本推导，无法推导的项 MUST 标为未知/校验缺口，MUST NOT 编造数字。
- **FR-007**: [[STR-007]] MUST 由原 `think-skills` 的心智模拟流程产出（含自然语言逻辑与程序化逻辑的分层审计），并在产物中记录假设、未知与禁止的真实副作用。
- **FR-008**: 预期阶段 MUST 零副作用：MUST NOT 调用工具执行 Trainee、MUST NOT 写 Trainee 目录、MUST NOT 发起网络请求或外部动作。

#### C. 真实执行与观测

- **FR-009**: Coach MUST 为每次运行派发恰好一个子代理执行 Trainee；派发载荷 MUST 包含 `<work>` 原文、Trainee 目标与「按 Trainee 自身 `SKILL.md` 执行」的指示，MUST NOT 加入教练的 [[STR-007]]、偏差猜测或预期结论，也 MUST NOT 把 Trainee 流程改写成教练自己的简化流程。
- **FR-010**: 一次运行的主成功条件 MUST 是 Trainee 的真实工作完成（主工件产生）；优化 MUST NOT 成为执行的前置条件，也 MUST NOT 挤占或缩短执行。
- **FR-011**: Coach MUST 把观测记录落盘为 [[STR-015]]（运行目录 [[STR-013]]），逐步包含：步骤、触发/指令、动作、工具调用、状态变化、产物、耗时与一致性检查；每步 MUST 标明观测来源（[[STR-011]] 或 [[STR-012]]，冲突以宿主事件为准），教练不可见的步骤 MUST 标[[STR-006]]并计入缺口清单。**「一致性检查」只做观测判定**——该步是否推进 [[STR-008]] 的关键路径、是否偏离 [[STR-007]] 预计的步骤，MUST NOT 借一致性检查去执行 Trainee 的验证逻辑（FR-012）。**缺口计数规则**：SC-004 只数步骤行上的 [[STR-006]] 标记，摘要行用普通文字描述缺口，不重复标记。
- **FR-012**: Coach MUST NOT 自己执行 Trainee 的步骤（禁止与子代理并行重跑），也 MUST NOT 向子代理的工作注入额外副作用。
- **FR-013**: 子代理失败、超时或拒绝时，Coach MUST 如实记录失败坐标与已完成部分（无法观测的部分按 [[STR-006]] 标注，不得以缺口掩盖失败）；运行状态 MUST NOT 被叙述为完成。**「继续」只指继续到偏差报告与提升计划，MUST NOT 触发第二次子代理派发**（FR-009 的恰好一个子代理不因失败而放宽）；Trainee 的失败语义 MUST 在 [[STR-007]] 中预先抽取，作为教练判断继续/停止的输入。

#### D. 评估与提升

- **FR-014**: 执行闭环结束后，Coach MUST 按[[STR-008]]与[[STR-009]]两个维度对比「预期 vs 实际」，产出偏差报告 [[STR-016]]（运行目录 [[STR-013]]）；每条偏差 MUST 引用观测记录中的具体步骤或产物作为证据，并 MUST 区分结果偏差与过程偏差。
- **FR-015**: Coach MUST 产出 Trainee 的提升计划 [[STR-017]]（运行目录 [[STR-013]]），条目 MUST 指向 Trainee 的具体文件/章节与具体微调动作（tweak/adjustment），MUST NOT 给泛泛而谈的建议。
- **FR-016**: Coach MUST 通过 `improve-skills` 的既有入口应用提升计划（传入 Trainee 目标与偏差证据）；教练 MUST NOT 在本次运行内直接改写 Trainee 文件，MUST NOT 改变 `improve-skills` 的契约。
- **FR-017**: 运行结论 MUST 使用封闭值域：`run: success|partial|failed`；优化状态 MUST 使用封闭值域 [[STR-010]]。优化被跳过、不可用或失败时，运行 MUST 仍以 Trainee 的真实产出为主结果报告，MUST NOT 因此把执行判为失败（此时 `run` 至多 `partial`，除非 Trainee 主工件已按判据完成）。

#### E. 身份、分发与兼容

- **FR-018**: 重命名 MUST 同步替换全部活身份坐标（旧名 [[STR-002]] → 新名 [[STR-001]]）：源目录 `skills/external/` 下的新目录、frontmatter `name`、`skill_id` 与 Resource ID 的 Canonical ID/Path、运行时 unit id [[STR-003]]、flow-class 定义行、probe 定义行与 probe id [[STR-004]]、`/speckit.skills` 路由行与路径、description 触发词与 Trainee 参数形态。
- **FR-019**: `/speckit.skills` 的 modify 路由行 MUST 指向 [[STR-005]]，并 MUST 写明调用形态 `coaching-skills <trainee-name|trainee-path>`。
- **FR-020**: 旧目录名 [[STR-002]] MUST 加入 `src/specify_cli/__init__.py` 的 `_OBSOLETE_SKILLS`；升级清理 MUST 删除该实体目录，MUST NOT 删除用户自建的同名符号链接。
- **FR-021**: 派生面（`.specify/skills/**`、命令副本、渲染后的宿主 agents、编译的 `## Wrap-up`、probe-map）MUST 由既有再生成入口产出，MUST NOT 手改。
- **FR-022**: 全部活接线引用（`agents/skill-verifier.agent.md`、`agents/structure-adjuster.agent.md`、四个 `create-agent` 角色模板、`run-skills` 的 modify 族说明、docs 两处）MUST 更新为新名；活接线面 MUST NOT 残留 [[STR-002]]。
- **FR-023**: 四个冻结基线测试 MUST 显式更新并注明日期与理由；MUST NOT 静默改计数，更新后的计数 MUST 与目录实测一致。
- **FR-024**: **本特性 `078-coaching-skills` 产物目录之外的**既有记录（其他特性的 `.specify/specs/<其他特性>/**`、`memory/evidence/**`、其他 `features/<ID>.md`、reviews、eval-baseline、按旧 unit id 归档的 run/feedback 记录）MUST NOT 被改写或回填；反过来，本特性自身产物（`.specify/specs/078-coaching-skills/**`、`.specify/memory/features/078.md`）不属历史记录，MUST 可正常改写与重跑，MUST NOT 以「历史不改写」为由拒绝更新。

#### F. 治理

- **FR-025**: 实现 MUST NOT 新增第二套子代理派发机制；MUST 复用宿主原生子代理 / `run-agent` / `run-skills` 的既有能力。
- **FR-026**: [[STR-001]] MUST 保持 `external` 分类（面向消费项目用户与代理），MUST NOT 迁入 internal 层。
- **FR-027**: 实现 MUST NOT 新增阻断式确认门；判定单位是 `git diff` 的**新增行**：这些行 MUST 0 命中 `scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS`。总量比较不作判据（总量相等允许「加一门、删一门」）。基线读数（改动前实测）MUST 记入测量证据，使「0 新增」可复核。
- **FR-028**: 教练运行 MUST 落盘到按 run-id 隔离的运行目录 [[STR-013]]，四个产物分别为 [[STR-014]]/[[STR-015]]/[[STR-016]]/[[STR-017]]（记录类数据一文一件，两个并发运行写入不同路径）；同一 Trainee 的两次优化 MUST NOT 并发应用——第二个运行在检测到同一 Trainee 的优化进行中时 MUST fail-closed 并点名冲突 run-id，MUST NOT 交错改写同一技能。
- **FR-029**: Coach 与 Trainee MUST 在**独立上下文**中分别理解同一份 `<work>`：教练在自己的上下文中产出预期，子代理只拿 `<work>` 原文与 Trainee 定义执行。两份独立读数 MUST 被保留为回路价值的一部分——偏差报告 MUST 指出「教练预期与 Trainee 实际理解/执行」的实质分歧（超出正常执行噪声的部分），MUST NOT 由教练预先消化 `<work>` 来消除这种独立性。

### Key Entities *(include if requirement involves data)*

- **Coach Run**: 一次教练运行，绑定 run-id、一个 Trainee、一件真实工作、一个运行目录 [[STR-013]] 与四个产物文件 [[STR-014]]/[[STR-015]]/[[STR-016]]/[[STR-017]]。
- **Trainee Target**: 被教练的技能，含名称、路径、层级（external/internal）、解析状态，以及它收到的 `<work>` 原文。
- **Execution Expectation**: 执行预期，含结果正确性判据集与过程效率判据集，以及假设/未知/禁止副作用。
- **Observation Record**: 观测记录，逐步承载动作、工具调用、状态变化、产物、耗时、观测来源与观测缺口。
- **Deviation Finding**: 偏差条目，含维度（correctness/efficiency）、预期值、实际值、证据引用与严重度。
- **Improvement Plan**: 提升计划，含按优先级排序的微调条目，每条指向 Trainee 文件/章节与证据。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 一次夹具教练运行在 [[STR-013]] 下按序产出四个文件 [[STR-014]]/[[STR-015]]/[[STR-016]]/[[STR-017]]（4/4），且夹具工作的主工件真实存在 1/1；缺任一文件即判失败。
- **SC-002**: 顺序可判定——[[STR-007]] 的运行记录中 [[STR-014]] 的落盘时点严格早于第一次子代理动作；删掉该文件后重跑检查失败（阴性对照 1/1）。
- **SC-003**: 双维度判定——含植入的正确性缺陷与效率退化的夹具，偏差报告在 [[STR-008]] 与 [[STR-009]] 两个维度各至少一条带证据的偏差（2/2）；只有单一维度时判失败。
- **SC-004**: 观测诚实性——含一處不可观测步骤的夹具，记录中[[STR-006]]恰出现一次（1/1），且无编造步骤（人工复核 0 条）。
- **SC-005**: 执行优先——在夹具中同时移除 `improve-skills` 的源与镜像两层并让入口指向一个不存在的单元（确保「不可用」可构造），运行仍交付 Trainee 主工件（1/1），并以 `optimization: unavailable`（[[STR-010]]）单列报告（1/1）。
- **SC-006**: 重命名一致性——在 A10 的封闭活接线面内 [[STR-002]] 出现次数**恰为 1**（仅 `_OBSOLETE_SKILLS` 行，允许差异集见 A10）；FR-018 的**八个身份坐标**逐个核对、每个坐标各以一条判定通过：① 源目录（`skills/external/[[STR-001]]/` 存在、`skills/external/[[STR-002]]/` 不存在）；② frontmatter `name`；③ `skill_id` 与 Resource ID 的 Canonical ID/Path；④ 运行时 unit id [[STR-003]]（`flow-class-check.py --action lookup` 对其解析为 `execution / behavior-oracle`）；⑤ flow-class 定义行；⑥ probe 定义行与 probe id [[STR-004]]（probe 编译 `--check` 退出 0）；⑦ `/speckit.skills` 路由行与路径（指向 [[STR-005]]）；⑧ description 触发词与 Trainee 调用形态（点名 [[STR-001]] 且写明 `[[STR-001]] <trainee-name|trainee-path> <work>`）。计数按坐标而非子串，[[STR-001]] 被 [[STR-003]] 包含不重复计（8/8）。
- **SC-007**: 升级兼容——夹具项目含旧实体目录与用户同名符号链接，跑一次 `specify init` 后旧目录被删除、符号链接保留（2/2）。
- **SC-008**: 派生零漂移——`sync-mirrors.py --check` 与 `regen-command-copies.py --check` 均退出 0；门控判定与 FR-027/A11 同单位：`git diff <base> -- <A10 封闭活接线面> | grep '^+'` 的**新增行 0 命中** `scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS`（命令、pattern 集与改动前基线读数 MUST 记入测量证据，「0 新增」可复核；不使用前后总量相等作判据）（3/3）。
- **SC-009**: 冻结基线显式更新——四个测试文件中新名与日期注记同时存在，且四个文件在新树上通过；无「只改名不注记」的条目（4/4）。

### Measurement Sources & Collection Methods

- **SC-001 Source**: 夹具运行的四个产物路径 + 主工件路径存在性检查，由契约测试在临时项目内断言。
- **SC-002 Source**: 运行日志/产物 mtime 与派发记录的顺序比对；阴性对照通过删除预期产物重跑。
- **SC-003 Source**: 植入式夹具的偏差报告；按维度解析条目数。
- **SC-004 Source**: 观测记录中 [[STR-006]] 标记计数 + 人工/脚本复核编造项。
- **SC-005 Source**: 将 improve-skills 从夹具环境移除后运行，读取运行结论。
- **SC-006 Source**: 按八个坐标逐项取证的记录——目录存在性、frontmatter 与 `skill_id`/Canonical ID 解析、`flow-class-check.py --action lookup` 解析记录、`probe-utils.py` 编译检查、路由行文本、description 文本；旧名计数取 `git grep` 在 A10 封闭面内的命中。
- **SC-007 Source**: 夹具安装项目的 `specify init` 前后目录/链接状态。
- **SC-008 Source**: `sync-mirrors.py --check` 与 `regen-command-copies.py --check` 的退出码；`git diff <base> -- <A10 封闭面> | grep '^+'` 的新增行逐行对照 `scan-confirmation-gates.py` 的 `BLOCKING_PATTERNS`；改动前基线读数（同命令、同 pattern 集）与判定结果一并入证据。
- **SC-009 Source**: 四个冻结基线测试的源码注记与测试结果。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | `coaching-skills` | FR-001, FR-018, FR-026, SC-006, 路由行, 目录名 |
| `STR-002` | `think-skills` | FR-020, FR-022, SC-006, `_OBSOLETE_SKILLS` |
| `STR-003` | `skill:coaching-skills` | FR-018, SC-006, flow-class 行, probe 行 |
| `STR-004` | `skill-coaching-skills-wrapup` | FR-018, probe 定义, 编译块 |
| `STR-005` | `skills/external/coaching-skills/SKILL.md` | FR-019, SC-006, 路由表 |
| `STR-006` | `observation-gap` | FR-011, FR-013, SC-004, 观测记录 |
| `STR-007` | `Execution Expectation` | FR-004, FR-007, SC-002 |
| `STR-008` | `Outcome Correctness` | FR-005, FR-014, SC-003 |
| `STR-009` | `Process Efficiency` | FR-006, FR-014, SC-003 |
| `STR-010` | `optimization: applied|skipped|unavailable|failed` | FR-017, SC-005, 运行报告 |
| `STR-011` | `host-event` | FR-011, A6, 观测记录 |
| `STR-012` | `self-report` | FR-011, A6, 观测记录 |
| `STR-013` | `.specify/memory/coaching/<run-id>/` | FR-004, FR-011, FR-014, FR-015, FR-028, SC-001 |
| `STR-014` | `expectation.md` | FR-004, SC-001, SC-002 |
| `STR-015` | `observation.md` | FR-011, SC-001 |
| `STR-016` | `deviations.md` | FR-014, SC-001 |
| `STR-017` | `improvement-plan.md` | FR-015, SC-001 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-10-30

- Q: 078 的 Feature 绑定方式？（原为 Need clarification，无现成匹配 Feature） → A: 新建 Feature 078（Status: Draft），建立 `.specify/memory/features/078.md` 详情与索引行，并在 057 的 Related Specifications 追加反向交叉引用。
- Q: Trainee 要做的「真实工作」从哪里来？ → A: 第二个位置参数 `<work>`；教练与 Trainee 在**两个独立上下文**中分别理解同一份 work，保留两份独立读数用于交叉验证 harness 的有效性（落为 FR-029，并约束派发载荷只用 work 原文，FR-009）。
- Q: 教练「观察」子代理执行的通道以什么为准？ → A: 宿主事件为主（[[STR-011]]）、子代理自报兜底（[[STR-012]]），逐字段标来源，字段级冲突以宿主事件为准（A6 / FR-011）。
- Q: 四个产物落在哪里、以什么形态？ → A: 独立运行目录 [[STR-013]]，四个固定文件 [[STR-014]] / [[STR-015]] / [[STR-016]] / [[STR-017]]（FR-004 / FR-011 / FR-014 / FR-015 / FR-028）。

**本轮覆盖扫描说明**：同一作者条件成立（规格由本轮会话写成），覆盖扫描由两个 fresh-context 只读子代理分域执行。共 24 条发现：20 条由既有 owner 事实裁决并已就地修正（源/镜像同实体不算重名、状态封闭值域、门禁按新增行判定、缺口计数规则、并发隔离、主工件声明、失败后不二次派发等），4 条作为上面的问答写回；无未决项。

<!--
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
