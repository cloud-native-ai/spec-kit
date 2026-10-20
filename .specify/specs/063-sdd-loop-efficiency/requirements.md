# Requirements Specification: sdd-loop-driver 运行效率优化（SDD Loop Efficiency）

**Requirement Branch**: `063-sdd-loop-efficiency`  
**Created**: 2026-10-20  
**Status**: Draft  
**Input**: User description: "优化 sdd-loop-driver 无人值守 SDD 运行吞吐：为中型特性提供显式、可审计的快车道（跳过 checklist，保留 analyze/review）；全量测试每特性运行仅两次（implement 起点与最终收口），中间阶段与 review 使用定向测试并记录证据；plan 阶段预置「下游只小修、不重审」约束（框架命令内部硬约束不可安全实现时显式排除）；阶段派发采用 stream-json 进度可见与 nohup 完全解耦，保持完成哨兵、独立校验、确认门与卡死处置不变。本特性自身仍走完整阶段链（checklist/analyze/review 必需），快车道仅作用于未来运行。" 需求语义权威（brief）已归档为 dated record：[notes/source-requirement.md](notes/source-requirement.md)（2026-10-20 逐字快照）；原 `/tmp/sdd-loop-efficiency-brief.md` 仅保留为 provenance 注记，不再作为权威引用。**CLI 能力档案归属（2026-10-20 裁决）**：CLI 能力档案（集合、必填维度、known/unknown、U2/U4/U5 观测、probe/feedback、契约与测试）唯一归属于 Feature 064（`.specify/specs/064-subagent-concurrency/`；逐条裁决见 `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`）。本规格只保留四项吞吐优化与 stream-json / nohup 能力，不再定义、复制或测试 CLI 档案；需要 CLI 行为知识时指向 064 的 `contracts/cli-profiles.md` 与 `skills/external/sdd-loop-driver/references/cli/index.md`。

## Related Feature *(mandatory)*

**Feature ID**: 058  
**Feature Name**: 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver）  
**Binding rationale**: 063 的四项优化全部落在 Feature 058 的唯一承载面 `skills/external/sdd-loop-driver/`（派发配方、watcher、阶段提示词），扩展同一机制而非新增能力域；按 reuse-first 绑定为演化特性。绑定不改变 058 的 `Implemented` 状态（宪法 VII：状态不得回退）。绑定裁决与证据见 `## Clarifications` Session 2026-10-20。

## 现状锚点（2026-10-20 以源码与制品实测为准；dated record，仅作可行性输入，非运行时保证）

- 阶段链固定为 `requirements → clarify → plan → tasks → checklist → analyze → implement → review`，checklist 与 analyze 均为必经门；哨兵 = 大写阶段名 + `-DONE`（`skills/external/sdd-loop-driver/references/dispatch-recipes.md` § Recipe 4）。
- 阶段 runner 当前以 `-p "$(cat prompt)"` 缓冲输出到单一 log，观察面为阶段粒度，阶段结束前日志静默（同文件 § Recipe 2–3）。`watch-model.md` § 2 已把 `--output-format stream-json` 的 live log 列为可选进度信号，但没有派生规则、哨兵抽取规则或 watcher 接线。
- `nohup` 是远端脱离派发的权威落点（同文件 § Recipe 3）；本地拓扑（§ Recipe 5）只要求直驱，未把脱离写成默认要求。
- implement 技能偏好规范 runner 并以名称级基线做回归比较（`skills/internal/implement-feature/SKILL.md`），但不存在运行级全量测试预算；中间阶段与 review 是否跑全量没有统一约束。
- 全仓检索（2026-10-20）未发现快车道、plan 冻结/只小修约束的既有实现或术语占用：`skills/external/sdd-loop-driver/` 与 `docs/reference/skills/sdd-loop-driver.md` 中相关检索为零命中。
- 契约测试 `tests/contract/test_sdd_loop_driver_skill.py` 钉住 SKILL.md 的 H2 节集合与逐条款行为；技能本体位于 `skills/external/sdd-loop-driver/`，运行时镜像位于 `.specify/skills/sdd-loop-driver/`；逐技能参考页为 `docs/reference/skills/sdd-loop-driver.md`。
- `skills/external/sdd-loop-driver/references/cli/`（`index.md` + 五份档案）与 Probe Object `skill-sdd-loop-driver-cli-profile` 已由 Feature 064 于 2026-10-20 落地；唯一 owner 为 064，063 MUST NOT 新增、修改或复制。063 的 stream-json 默认与 nohup 脱离作为 064 档案记录的既有事实被 064 引用（064 CLP-08/CLP-13）。
- 本规格编写时最大规格编号为 `062`；此后 `063` 与 `064` 已登记，064 为 CLI 能力档案的权威归属。

## Assumptions（对输入中开放点的缺省裁决，clarify 阶段可推翻）

- **Related Feature 已绑定（clarify 2026-10-20）**：绑定 Feature 058（无人值守 SDD 循环驱动机制）作为演化特性；058 的范围覆盖本特性全部四项优化的承载面，绑定后状态保持 `Implemented`，MUST NOT 回退。
- **「中型特性」区间已冻结（clarify 2026-10-20）**：8–30 条 FR、10–40 条任务（含端点）为本特性的权威基线；低于区间的小特性仍走完整链（成本本就低），高于区间的大特性强制完整链。plan 阶段 MUST NOT 自行调整数值；确需调整时 MUST 走显式范围修订并同步 SC-002 夹具。
- **快车道默认关闭**：缺省始终完整链；快车道只在入口携带 [[STR-006]]、或记录交互式用户的原文采纳后启用。
- **测试预算是运行级槽位**：两个槽位 = implement 起点基线、最终收口；最终收口槽内因修复新失败而重跑同一全量套件，记为槽内重跑（含触发与证据），不另开槽；槽外任何全量执行都必须以显式例外记录。
- **plan 约束只在编排层执行**：框架命令内部硬执行是显式排除项；驱动是执行点，非驱动手工调用不受约束。该限制作为已接受的设计代价明确记录。
- **stream-json 为主路径**：对支持的 CLI 默认启用；不支持或派生失败时降级到既有缓冲模式，降级必须留痕，不得伪完成。
- **nohup 脱离适用于本地与远端两种拓扑**：远端原有 `ssh + su + nohup` 形态保留，本地补齐 `nohup + </dev/null + 重定向`。
- **不新增运行时**：不引入常驻服务、守护进程、外部依赖或模型 API；派生与 watcher 只用现有 shell/Python 标准库能力（宪法 IX）。
- **本特性自身走完整链**：checklist/analyze/review 均必经；快车道只作用于未来运行。
- **不改阶段命令内部流程**：四项优化优先在编排层实现；确需下沉时必须在 plan 记录显式设计裁定（变更面、风险、回归证据与替代方案）。
- **向后兼容**：未启用快车道的现有用户看到的行为与改动前一致；哨兵字面量、判定状态机与退出码不变。
- **CLI 能力档案归属 064（2026-10-20 裁决）**：本特性只拥有 stream-json 输出默认与 nohup 脱离；CLI 档案集合、八维、观测、probe/feedback、契约与测试由 Feature 064 唯一拥有（064 的 CLI 档案条款与 `contracts/cli-profiles.md` CLP-01…CLP-17）。063 不新增 `references/cli/`、Probe Object、CP 契约或档案测试；派发记录/状态脊的 CLI 追加字段由 064 `data-model.md` E10 定义，本规格不重复。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 中型特性快车道：显式准入与失败回退 (Priority: P1)

运行操作者为一个中型特性启动无人值守运行。驱动在 `checklist` 门之前，用制品实测值逐条判定准入判据：满足则记录快车道裁决、跳过 `checklist`，但 `analyze` 与 `review` 照常执行；不满足则走完整链。裁决与证据写入状态脊并复现在收尾汇总中；录取后任一判据失效时，运行回退完整链并记录触发。

**Why this priority**: 这是吞吐收益的主来源，同时最容易变成「静默降质」；准入显式化与失败回退共同决定该优化可否被信任。

**Independent Test**: 准备两个夹具——一个落在中型区间且满足全部判据，一个大特性或判据失败；检查派发记录、准入记录与下游阶段行为。

**Acceptance Scenarios**:

1. **Given** 一个含 12 条 FR、25 条任务、无新增引擎/模式/安全面、clarify 已完成且需求阶段质量清单全绿的中型特性，**When** 驱动到达 `checklist` 前的裁决点，**Then** 它写入带逐条证据的快车道准入记录，跳过 `checklist` 派发 `analyze`，并在 implement 后派发 `review`。
2. **Given** 同一组制品但没有入口显式声明或经协议记录采纳，**When** 驱动到达裁决点，**Then** 它执行完整链（含 `checklist`），且不存在快车道记录；快车道不得成为缺省。
3. **Given** 一个已录取的快车道运行，`analyze` 发现需要新增可执行引擎的 CRITICAL 问题，**When** 驱动处置该发现，**Then** 它回退完整链、在适用位置补派 `checklist`，并把回退触发与证据写入状态脊。
4. **Given** 一个含 60 条任务的大特性，**When** 驱动到达裁决点，**Then** 准入被拒绝，失败判据及其实测值被记录，运行走完整链。
5. **Given** 一个快车道运行进入 implement 与 review，**When** 两个阶段执行，**Then** 它们都不把缺失的 checklist 产物当作缺失的必需门，跳过标记在阶段提示词与状态脊中可见。
6. **Given** 运行收口，**When** 生成收尾汇总，**Then** 汇总携带准入裁决、证据指针与 checklist 状态（跳过或已执行）。

---

### User Story 2 - 全量测试预算与定向测试证据 (Priority: P1)

操作者希望一次特性运行不再反复烧全量套件，同时保留发现回归的能力。驱动把全量执行限制为两个槽位——implement 起点基线与最终收口——并要求中间阶段与 review 使用确定性选择的定向测试集，且每次运行都留下可复核证据。

**Why this priority**: 全量套件是运行中最贵的单步；没有预算就没有可预期的吞吐，没有证据就没有可信的回归结论。

**Independent Test**: 用插桩的阶段日志运行一个完整夹具，统计全量调用次数与槽位；在 implement 起点之后注入一个已知回归，检查最终收口是否按名称级差集发现它。

**Acceptance Scenarios**:

1. **Given** 一个完整特性运行，**When** 驱动在收口审计测试台账，**Then** 恰好两个全量槽位被记录：implement 起点（基线，按名称捕获失败名单）与最终收口（名称级回归比较），各带命令、退出码、计数与比较结果。
2. **Given** plan、analyze 或 review 阶段需要验证，**When** 该阶段运行测试，**Then** 它按确定性规则选择定向集，并记录所选路径、选择依据与结果。
3. **Given** 在 implement 起点基线之后注入一个回归，**When** 最终全量运行执行，**Then** 该失败出现在名称级差集中，并被修复或显式归因。
4. **Given** 某个中间阶段想跑第三次全量套件，**When** 驱动处置该请求，**Then** 除非记录带原因与证据的显式例外，请求被拒绝；例外出现在收尾汇总。
5. **Given** 某阶段的测试证据缺失，**When** 收口审计执行，**Then** 台账把缺口报告为 unknown，而不是零或补造值。
6. **Given** 一次调用在收集或执行任何测试前即失败（如解释器缺失），**When** 预算审计执行，**Then** 它被记录为环境失败且不消耗槽位；实际执行了测试的调用则消耗槽位。

---

### User Story 3 - Plan 阶段「只小修、不重审」约束 (Priority: P2)

`plan` 完成后，驱动在下游阶段预置约束：对 plan 拥有的制品只允许小修，不允许静默改写范围、架构、数据模型、契约语义或任务分解，也不为小修触发完整重审回环。需要实质性改动时，下游阶段显式回传决策，由驱动上送。

**Why this priority**: 它直接减少 plan 之后的往返开销，但改变既有回环习惯；安全性取决于分类是否可复核、失败是否显式。

**Independent Test**: 在两个夹具中分别制造小修与实质性 plan 改动，检查阶段门、分类记录与是否出现静默重审。

**Acceptance Scenarios**:

1. **Given** `plan` 已完成，**When** tasks、analyze、implement 或 review 执行，**Then** 阶段提示词携带只小修约束，状态脊把它登记为自 plan 完成起 active。
2. **Given** 下游阶段需要修复 plan.md 的错别字或断链，**When** 它编辑该文件，**Then** 改动被分类为小修并记录，驱动的 U4 校验通过。
3. **Given** 下游阶段发现需要改变架构或契约语义，**When** 它无法在约束下继续，**Then** 它返回显式异常行并附建议改动与实质性理由，不静默编辑 plan。
4. **Given** 下游阶段未声明就修改了 plan 制品，**When** 驱动在 U4 校验，**Then** 该阶段被判门失败，驱动将其分类并上送或按既有规则派发完整 plan 重审。
5. **Given** 发生了一次小修，**When** `analyze` 重新运行，**Then** 不需要完整 plan 重审，且 analyze 门本身的行为与完整链一致。

---

### User Story 4 - 阶段进度可见与驱动会话解耦 (Priority: P1)

操作者希望阶段运行期间看得见进度，而不是盲等；同时，阶段子代理不应因驱动会话或 agent 进程退出而中断。runner 以 stream-json 输出并保留原始事件流，派生出可跟踪的紧凑实时日志，并以 nohup 完全脱离驱动会话。哨兵、独立校验与重入继续工作。

**Why this priority**: 不可见与不可脱离是观测到的两个直接故障源；它们既影响诊断，也影响长阶段能否跑完。

**Independent Test**: 用一个会产生多分钟事件流的夹具阶段，中途终止驱动进程；检查实时日志、哨兵、退出记录、阶段完成情况，以及新会话能否仅凭状态脊接管。

**Acceptance Scenarios**:

1. **Given** 一个持续产生事件的阶段，**When** 驱动监听，**Then** 紧凑实时日志在运行期持续增长，驱动能看到进度行，且不需要独立的 `sleep` 回合。
2. **Given** 阶段正常结束，**When** CLI 发出终止结果，**Then** 派生实时日志的最后一个非空行恰好是阶段哨兵，watcher 返回 DONE，U4 继续核验产物。
3. **Given** 某个非终止 JSON 事件内部出现哨兵字样，**When** watcher 判定，**Then** 该事件不得产生 DONE。
4. **Given** 驱动 agent 进程在阶段中途退出，**When** 脱离的 runner 继续运行，**Then** 阶段完成并写出退出记录；新会话凭状态脊与一次 `--once` 快照核验完成，且不重新派发已完成阶段。
5. **Given** CLI 不支持 stream-json，**When** runner 启动，**Then** 它降级到缓冲模式并记录降级标记，阶段仍按既有哨兵/退出记录/deadline 规则完成或失败。
6. **Given** 派生步骤失败，**When** watcher 判定，**Then** 它回退到原始日志与退出记录并标记降级，绝不报告伪 DONE。

---

### User Story 5 - 安全不变量、自应用与分发 (Priority: P2)

四项优化不得削弱既有安全与质量保证；本特性必须通过框架既有的分发与测试面交付，并且它自身的开发必须走完整阶段链。未启用新行为的现有用户看到的行为不变。

**Why this priority**: 吞吐优化只有在不破坏确认门、独立校验与卡死处置的前提下才可采纳；自应用与分发决定它是否真正到达用户。

**Independent Test**: 检查契约测试、场景夹具、镜像与文档；审计本特性自身运行的阶段产物；对比改动前后的失败测试名单。

**Acceptance Scenarios**:

1. **Given** 修改后的驱动，**When** 检查确认行为，**Then** push 仍是破坏性动作且须显式授权，不存在新的自动批准或绕过路径。
2. **Given** 一个阶段自称完成，**When** 驱动校验，**Then** 校验者不是该阶段执行子代理，哨兵、产物核验与纪律抽查三者仍须同时成立。
3. **Given** 阶段超时或达到重试上限，**When** 运行进入卡死处置，**Then** 既有四要素上送件与状态脊先写后动程序保持不变。
4. **Given** 本特性自身的运行，**When** 审计其产物，**Then** `checklist`、`analyze`、`review` 均已执行，且不存在本特性自身的快车道记录。
5. **Given** 框架源码树，**When** 检查分发，**Then** 技能与参考页已更新、镜像已同步、契约测试与行为夹具在位，且未新增技能、命令或外部依赖。

---

> **Delegated scope（CLI 能力档案，归属 064）**：CLI 能力档案不在本特性范围。其用户故事、观测触发（U2/U4/U5）、probe/feedback 与验收由 Feature 064 拥有（`.specify/specs/064-subagent-concurrency/requirements.md` 的 CLI 档案条款；`contracts/cli-profiles.md` CLP-01…CLP-17；裁决 `.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`）。本规格不重复其故事、场景、实体或验收。063 的 stream-json 默认（FR-026）与 nohup 脱离（FR-031）是 064 档案记录的既有事实，由 064 只读引用。

---

### Edge Cases

- 准入裁决时 `tasks.md` 缺失、不可解析或任务行数无法复算 → 判 full-chain（fail-closed），记录原因，不猜测。
- 准入时满足全部判据，但后续阶段发现新增引擎、模式迁移、安全面或任务数越界 → 回退完整链并记录触发；不得继续以快车道完成。
- 快车道运行中 `analyze` 发现 CRITICAL/HIGH → 按既有门规则修复并重过 analyze；若修复本身使范围越界，则同时触发完整链回退。
- 快车道运行中 `review` 发现 P0 → 按既有 review 优先级处置；P0 未修复或未显式豁免前，不得派发下一特性。
- 入口未携带 [[STR-006]]，或声称快车道但状态脊无入口启用证据 → 按 full-chain 运行；口头或自然语言声明本身不构成准入。
- 需求阶段质量清单缺失或存在失败项 → 判 full-chain，即使 FR/任务数落在中型区间。
- 定向测试集选择结果为空 → 阶段不得声称已验证；必须扩大同族测试范围或按显式例外升级为全量运行，并记录原因。
- 定向集只覆盖部分改动，且剩余改动涉及共享引擎/生成器/公共脚本 → 视为安全信号不足，允许在槽外升级为全量运行，但必须记为显式例外。
- 全量预算的两个槽位已用完，最终收口又发现新失败需要再次全量确认 → 作为最终收口槽内重跑记录（触发 + 证据）；若发生在收口之外，则必须按槽外例外记录。
- 全量运行在收集测试前失败（解释器缺失、依赖缺失）→ 记为环境失败，不消耗槽位；不得把空基线当作全绿。
- 测试证据只给出通过计数、没有名称级差集 → 不满足回归证据要求，收口审计判证据不足。
- 阶段日志丢失或未记录测试命令 → 预算台账报告 unknown；不得推断为零次或两次。
- stream-json 的终止结果事件缺失，但进程正常退出且退出记录 `rc=0` → 按既有 INCOMPLETE 语义处理（配置了哨兵时哨兵缺失即伪完成），不得因流式模式放宽。
- 非终止事件包含哨兵字样，或助手中间输出以哨兵结尾 → 派生与 watcher 不得据此判 DONE；只认终止结果文本。
- 派生进程比 runner 先退出、派生输出不完整 → watcher 回退原始日志/退出记录并标记降级；不得伪完成。
- CLI 不支持 stream-json 或拒绝该旗标 → 降级缓冲模式，保留四件套，阶段不得因旗标不支持而失败。
- 本地拓扑启动 runner 时遗漏 nohup → 派发自检必须标记「未脱离」，状态脊记录风险；不得把该次派发计为受保护运行。
- 驱动进程退出后新会话接手 → 先 `--once` 快照；已完成阶段只核验不重派；运行中阶段恢复监听窗口；不得从头重跑。
- 多线并行 → 每线独立 raw stream、实时日志、pid/status/heartbeat、状态脊与全量测试台账；路径与预算槽位不得共享或互相覆盖。
- 下游阶段修改 plan 制品但提交信息未声明 → U4 通过 `git diff` 分类；未声明改动一律判门失败。
- plan 小修累积到改变语义（多处小修合并后实质改变契约）→ 分类必须按最终差异判定，不得按单次编辑的措辞规避。
- U4 无法判定一处 plan 改动是否改变需求范围、架构/数据模型/契约语义或任务分解范围 → 按 FR-022(b) 作为决策上送，不得自行派发完整 plan 重审。
- 驱动在 plan 完成前退出并在之后重入 → 只小修约束的 active 登记点仍为 plan 完成时；重入后必须从状态脊恢复该状态。
- 快车道运行在收尾时发现准入记录缺失或字段不全 → 收口审计判不可信，按完整链补跑缺失门或上送，不得追认。
- CLI 能力档案相关的边界（版本不一致、无档案、冲突观测、档案运行中更新等）由 Feature 064 的 requirements Edge Cases 拥有；本特性不重复。

## Requirements *(mandatory)*

### Functional Requirements

#### 中型特性快车道

- **FR-001**: 驱动 MUST 支持「中型特性快车道」：在 `checklist` 阶段前以显式准入裁决替代该阶段，`analyze` 与 `review` MUST 保持必经且行为不变；快车道 MUST NOT 跳过其他任何阶段。
- **FR-002**: 快车道 MUST 仅显式启用：U0 入口声明 MUST 携带字面量 [[STR-006]]，并 MUST 原文记入该线状态脊的入口声明；缺失该字面量时，运行 MUST 使用完整阶段链。存在交互式用户时，驱动 MAY 在准入判据实测后提议一次快车道并记录其原文采纳，但 MUST NOT 因等待回答而阻塞运行；无人值守运行中 [[STR-006]] 是唯一启用形式。快车道 MUST NOT 作为缺省、隐式或推断行为。
- **FR-003**: 准入判据 MUST 全部满足，并 MUST 在 `tasks.md` 已产出、`checklist` 派发前以制品实测值判定：(a) `requirements.md` 的 FR 定义行数在 8–30（含端点），`tasks.md` 的任务行数在 10–40（含端点）；FR 定义行 = 匹配 `^- **FR-[0-9]{3}**:` 的行（行首、粗体 ID、三位数字、英文冒号；SC 定义行、说明行与其它 FR 提及不计入），任务行 = 匹配 `^- \[[ xX]\] T[0-9]{3}` 的清单行（分组标题与说明行不计入）；两种计数 MUST 由同一确定性命令复算，MUST NOT 手抄；(b) 特性未修改宪法；(c) 不新增可执行引擎、CLI 命令/模板、技能、外部依赖、网络服务或模型 API；(d) 不涉及安全/隐私敏感面——认证授权、凭据/密钥、数据删除/迁移、发布/外传，以及确认门判据；(e) 单线单分支，且无并发线触碰同一交付路径；(f) `clarify` 已完成、活动澄清标记为零、Related Feature 绑定已解析；(g) 需求阶段自产的质量清单（`checklists/requirements.md`）存在且全部通过。以上判据 MUST 以可复算的制品证据判定，不得以主观规模印象替代。FR-003(a) 的数值区间为本特性冻结基线；调整 MUST 走显式范围修订并同步 SC-002。
- **FR-004**: 驱动 MUST 在派发 `checklist` 前把准入记录写入该线状态脊，字段至少包含：裁决（fast-lane / full-chain）、入口启用证据（[[STR-006]] 或交互式采纳原文）、每条判据的判定与证据指针、实测 FR 定义行数与任务行数、裁决时间；记录 MUST 使用 [[STR-003]] 标记跳过状态。
- **FR-005**: 快车道裁决 MUST 随下游阶段提示词发布（至少 implement 与 review），使任何阶段都不把缺失的 checklist 产物当作缺失的必需门；收尾汇总 MUST 携带 `checklist=skipped(fast-lane)` 或等价可见标记。[[STR-003]]
- **FR-006**: 失败回退（fail-closed）：录取后任一判据失效、或后续阶段发现新事实使判据不再成立（如 analyze 暴露新增引擎/模式/安全面，或任务数越出区间）时，驱动 MUST 回退完整链、在适用位置补派 `checklist`，并记录回退触发与证据；回退 MUST NOT 静默。
- **FR-007**: 快车道 MUST NOT 削弱 `analyze`：CRITICAL/HIGH 归零或已处置的门判据、以及至多一轮的有界回环 MUST 与完整链完全一致；快车道无豁免 analyze 发现的权限。
- **FR-008**: 快车道 MUST NOT 削弱 `review`：`/speckit.review` 的行为、证据义务与发现分级 MUST 与完整链一致。
- **FR-009**: 快车道定义（中型区间、准入判据、准入记录形态、回退规则）MUST 落在 loop driver 的技能面并被契约测试钉住；任何运行 MUST NOT 在缺少准入记录时声称自己走了快车道。
- **FR-010**: 本特性自身的开发 MUST 使用完整阶段链（`checklist`、`analyze`、`review` 均必经），快车道 MUST NOT 作用于本特性自身的运行；该自应用例外 MUST 在规格与收尾证据中可见。

#### 全量测试预算与定向测试

- **FR-011**: 「全量测试运行」定义为以项目规范测试运行器执行、不带路径/测试过滤器的完整套件。本预算以运行线为作用域：每线独立台账与独立槽位，多线并行时互不共享或消耗对方槽位；「每特性运行」指一条运行线的端到端运行。每特性运行的全量预算 MUST 恰好为两个槽位：`implement` 起点（基线，按名称捕获失败名单）与最终收口（与基线做名称级回归比较，位于 review 通过之后、合并之前，由驱动或其派发的独立校验单元执行）。
- **FR-012**: 中间阶段（clarify / plan / tasks / checklist / analyze）与 `review` MUST 只运行定向测试集；MUST NOT 把全量套件作为例行步骤。每个适用阶段（未被授权跳过的中间阶段与 `review`）MUST 留下可唯一判定的阶段测试证据——至少一条 `ran` 运行记录，或一次明确的 `not-run-docs-only` / `empty-selection-escalated` 判定；整阶段没有任何证据记录 MUST 判证据不完整，MUST NOT 从完整性分母中消失。仅文档改动、且改动集不含可执行/测试面时 MUST 记 `not-run-docs-only` 并附改动路径证据；该状态按缩减字段集判定完整（阶段状态、选择依据、改动路径证据、证据指针），运行字段不适用，MUST NOT 记为 `unknown`。快车道按 FR-001 授权跳过 `checklist` 时，该阶段不产生测试运行义务，其测试证据状态 MUST 记为 [[STR-008]]，MUST NOT 记为 `unknown` 或以缺失证据计入完整性分母。
- **FR-013**: 定向测试集的选择 MUST 按确定性规则执行并记录依据：取以下集合的并集——(a) 覆盖本阶段改动路径/模块的测试；(b) 名称或路径指向本特性交付物的契约测试；(c) 本阶段修改了夹具的测试。选择 MUST 以路径/名称映射为依据，不得凭印象；阶段 MUST 记录所选路径、选择依据，以及「为何足以发现本阶段引入的回归」。该确定性规则 MUST 有固定的执行程序（命令或算法）并由技能面单一 owner 钉住；同一制品状态 MUST 复现同一集合，MUST NOT 由各阶段自行选择不同命令。
- **FR-014**: 每次测试运行（全量或定向）MUST 记录证据：命令、选择依据、退出码、passed/failed 计数、新增失败，以及比较基线；最终全量运行 MUST 以名称级差集（`comm -13` 或等价）对 implement 起点基线比较。
- **FR-015**: 回归发现能力 MUST 保留：最终全量运行发现的新失败 MUST 被修复，或被显式归因（既有失败 / 无关 / 不稳定，并附证据）；仅比较通过计数 MUST NOT 被视为满足本要求。
- **FR-016**: 槽外全量运行 MUST 仅以显式例外形式出现：驱动 MUST 记录原因与证据（如定向集不足以建立安全、共享引擎被改动、存在无法解释的失败），并在收尾汇总列出例外次数与原因；最终收口槽内因修复新失败而重跑同一套件 MUST 记为槽内重跑（含触发与证据），不另开槽；MUST NOT 静默超预算。
- **FR-017**: 预算 MUST 以台账形式写入该线状态脊（槽位、阶段、目的、执行序号、触发、时间），并由驱动在最终收口审计；证据缺失 MUST 报告为 unknown，MUST NOT 记为零或补造。
- **FR-018**: 运行器在收集/执行任何测试前即失败（如解释器或依赖缺失）的调用 MUST 单独记录为环境失败，不消耗槽位；任何实际执行了测试的调用 MUST 消耗槽位。
- **FR-019**: 本预算 MUST 在编排层实现（阶段提示词 + 状态脊台账 + 收口审计），MUST NOT 依赖修改框架命令内部流程。

#### Plan 阶段「只小修、不重审」约束

- **FR-020**: `plan` 阶段完成后，驱动 MUST 在下游阶段提示词中预置「只小修」约束：对 plan 拥有的制品（plan.md、data-model、contracts、quickstart、research、feature-ref）的改动 MUST 限于小修——错别字/措辞、断链/引用修复、格式、行级一致性——且 MUST NOT 改变范围、架构、数据模型、契约语义、FR/SC 内容或任务分解。
- **FR-021**: 下游阶段发现需要实质性 plan 改动时 MUST 停止，并以显式异常行（[[STR-005]]）回传建议改动及其实质性理由；MUST NOT 静默改写 plan 或自行重跑完整 plan 阶段。
- **FR-022**: 驱动 MUST 在 U4 校验下游阶段提交：凡触碰 plan 制品的改动 MUST 被分类为小修、实质改动或未声明；未声明或实质性改动 MUST 先判该阶段门失败，再按以下确定性规则分流——(a) 改动为修复既有缺陷所必需、且不改变已批准的需求范围/FR/SC 语义、架构方向、数据模型语义、契约语义或任务分解范围时，驱动派发完整 plan 重审并记录触发；(b) 改动改变上述任一项、引入新能力/安全面，或驱动无法确定时，作为决策以四要素上送，MUST NOT 自行重审。分流 MUST NOT 形成静默重审回环。本条所称「已批准需求基线」初始为 plan 约束激活时记录的 `plan_commit` 中 `requirements.md` 的 FR/SC 定义集合与语义（ID 集与各条语义）；U4 分类记录 MUST 写入 `approved_baseline_commit`，分支 (a)/(b) 的判定 MUST 以该提交的 `requirements.md` 为比较对象，MUST NOT 以工作树当前文本或其它提交替代。**Re-anchoring**：plan 约束激活后，任何在门内完成的 `requirements.md` 变更（含 analyze 路由修复、clarify 写回与显式范围修订）MUST 在下一个依赖该基线的 U4 分类之前触发重新锚定——驱动 MUST 在 E4 记录一条 re-baseline 事件（触发、时间、前一基线提交、新基线提交 = 包含该 `requirements.md` 变更的提交、FR/SC 定义集合与语义差异摘要），并把 `approved_baseline_commit` 更新为新基线提交；变更未提交或无法定位其提交时 MUST NOT re-anchor，受影响 plan 改动一律按 (b) 上送。re-anchoring 本身不构成 plan 重审，也不移动 plan 约束的生效点；此后的 (a)/(b) 判定 MUST 以最新锚定基线为比较对象。为落实新锚定基线所含需求而作的 plan 改动 MUST 按两分支正常分类，MUST NOT 因旧基线缺少该需求而被误判为越界。
- **FR-023**: 该约束 MUST NOT 取消或削弱 analyze 门的上游修复路由：analyze 发现仍须回到所属制品修复并重过该门；约束只约束修复的规模与重审开销，不约束修复是否发生。
- **FR-024**: 每个运行 MUST 在 plan 完成时把该约束登记为 active（含生效点），并在收尾汇总中报告是否发生过 plan 制品改动及其分类。
- **FR-025**: 范围边界：框架命令内部的硬执行 MUST 作为显式排除项；该约束是编排层纪律，驱动是执行点。已接受的设计代价 MUST 显式记录：非驱动手工调用阶段命令不受该约束约束；若后续证明该编排层实现不安全，MUST 另立特性修订，不得静默扩大范围。

#### 进度可见与驱动会话解耦

- **FR-026**: 阶段 runner MUST 默认以 [[STR-001]] 调用阶段 CLI，并把原始事件流完整落盘为 raw stream 证据文件。
- **FR-027**: runner MUST 有一个确定性派生步骤，把 raw stream 在运行期增量转换为紧凑实时日志：每个有意义的进度事件（或按声明的最小节奏）输出一行可读进度，MUST NOT 缓冲到进程退出；实时日志 MUST 可被追加读取与尾部跟踪。
- **FR-028**: 完成哨兵契约 MUST 保持：阶段正常结束时，紧凑实时日志的最后一个非空行 MUST 恰好是阶段哨兵（大写阶段名 + [[STR-002]]）；派生 MUST 取 CLI 的终止结果文本，MUST NOT 让 JSON 信封、事件元数据或非终止事件中的哨兵字样满足判定。
- **FR-029**: watcher MUST 把流式进度只当作可见性信号：进度行数/增长 MUST NOT 单独产生 `DONE` 或 `TIMEOUT`；完成仍须哨兵加 U4 独立校验，超时仍只由阶段 deadline 产生。既有判定与退出码 MUST 保持不变。[[STR-001]]
- **FR-030**: 若 CLI 不支持 stream-json 或派生失败，runner MUST 回退到既有缓冲模式，在状态脊记录 [[STR-004]] 及原因，并继续以退出记录 + 哨兵 + deadline 判定；回退 MUST NOT 自行产生伪完成或阶段失败。
- **FR-031**: 阶段派发 MUST 在本地与远端两种拓扑下都完全脱离驱动会话：以 `nohup` 启动 runner，stdin 接 `/dev/null`，stdout/stderr 重定向到文件，使驱动 agent 进程/会话结束（远端 SSH 断开或本地进程退出）MUST NOT 向阶段子代理发送终止信号或关闭其 stdio。脱离 MUST 是默认形态，不是可选变体。
- **FR-032**: 脱离后驱动 MUST 仍能监听、校验与重入：四件套（pid / status / log / heartbeat）与状态脊字段保持；新会话 MUST 能用 `--once` 快照接管；已完成的阶段 MUST 被核验而非重新派发。脱离 MUST NOT 削弱 U3/U4。
- **FR-033**: watcher MUST 支持把派生实时日志作为哨兵来源，并保留 raw stream 作为证据；其自测 MUST 覆盖：非终止事件中的哨兵字样不计、终止结果事件中的哨兵计、派生失败降级不伪完成、脱离 runner 在驱动退出后存活。[[STR-002]]
- **FR-034**: 进度可见 MUST 减少盲轮询：驱动等待 MUST 仍是既有长轮询窗口，实时日志只在窗口内被读取用于可见性；MUST NOT 新增独立 `sleep` 回合或按固定节奏空转的 agent 循环。
- **FR-035**: raw stream 与派生实时日志 MUST 作为 U4/U5 与事后审计证据保留，沿用运行既有产物约定；MUST NOT 引入新的常驻服务、守护进程或外部依赖。

#### 安全不变量

- **FR-036**: 四项优化 MUST NOT 改变确认门：push 仍是破坏性动作、须显式授权；MUST NOT 新增自动批准或绕过路径。
- **FR-037**: 独立校验 MUST 不变：执行者自报的完成仍只是候选；哨兵、产物核验与纪律抽查 MUST 同时成立，校验者 MUST NOT 是该阶段执行子代理。
- **FR-038**: 卡死处置 MUST 不变：阶段 deadline、重试上限、四要素上送件（发现了什么 / 为何吃重 / 中间产物逐项可定位 / 可选处置）与状态脊先写后动 MUST 保持；脱离运行中途失去驱动 MUST 可恢复，MUST NOT 被静默遗弃。该「不变」MUST 以可复算的行为基线判定，MUST NOT 以名称级测试失败基线替代：在冻结提交（本规格为 `ba2a18db`；若实现起点前另有行为面改动，以首个行为面改动前的提交为准并在状态脊记录差异）上，以三类场景夹具录制处置结果元组——超时（TIMEOUT）、重试上限（stalled + 四要素上送件）、伪完成（退出 rc=0 且哨兵缺失 → INCOMPLETE，不派发下一阶段）；每个元组 MUST 至少记录 watcher 判定、退出码（MUST 区分 watcher 判定退出码与 runner rc）、状态脊卡死状态、消耗的重试次数、四要素上送件齐备性（或不适用）、是否派发下一阶段、状态脊是否先写后动。驱动侧字段（状态脊卡死状态、重试消耗、四要素齐备性、下一阶段派发、先写后动、runner rc）MUST 由唯一执行体的脚本化驱动夹具（`tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py`）观测产生；录制 trace 只能作补充证据，MUST NOT 替代夹具观测，MUST NOT 作为驱动侧字段来源；夹具 MUST NOT 从 U3/U4/U5 判定表转录、MUST NOT 在夹具内硬编码期望值或从基线文件回填；录制 MUST 固定并记录初始已试次数（本规格为 0）。实现前复核（2026-10-20，N-08）：`ba2a18db` 之后的首个行为面提交为 `9e69f3de`（Feature 064 的 line registry），故本规格冻结读数 `ba2a18db` 不适用，实际行为基线取首个行为面改动前的父提交 `a1aac7e5`，差异记录于状态脊与 `notes/pre-change-measurements.md`。基线制品 MUST 为 [[STR-007]]（含 `base_commit`、场景、逐字段元组与录制证据指针），MUST 在实现首个行为面提交之前录制；收口 MUST 由同一可执行夹具在当前树上重放驱动侧步骤，归一化剔除时间戳、PID、绝对路径与耗时后逐字段比较，MUST NOT 仅重读基线文件；任何字段差异 MUST 判回归并修复，MUST NOT 以归因豁免。
- **FR-039**: 四项优化 MUST NOT 降低质量门：analyze/review 必经、必需校验不得静默跳过、测试预算不得静默超支、快车道不得静默启用。

#### 自应用、分发与测试

- **FR-040**: 交付面 MUST 落在 `skills/external/sdd-loop-driver/`（SKILL.md、references、scripts）与 `docs/reference/skills/sdd-loop-driver.md`；MUST 通过既有镜像机制同步到 `.specify/skills/sdd-loop-driver/`；MUST NOT 新增技能、命令或外部依赖。
- **FR-041**: 契约测试 MUST 钉住：快车道准入字段与 fail-closed 回退、测试预算与证据字段、plan 改动分类、stream-json 旗标/派生/哨兵行为、nohup 脱离形态，以及安全不变量。既有 loop-driver 契约（含钉住 H2 节集合的测试）MUST 保持绿色，或因本特性被有意更新并记录理由。
- **FR-042**: 行为夹具 MUST 证明：(a) 中型夹具走快车道、跳过 checklist 且 analyze/review 均执行；(b) 槽外全量超预算且无例外被检出；(c) 下游阶段实质性 plan 改动被 U4 抓获；(d) 驱动中途退出不中断脱离阶段且重入可核验；(e) implement 起点之后注入的回归被最终全量运行发现。
- **FR-043**: 四项优化 MUST 优先在编排层实现；若某优化无法在编排层安全达成，MUST 在 plan 阶段记录显式设计裁定（变更面、风险、回归证据与替代方案），不得静默修改框架命令内部或静默放弃。

#### CLI Capability Profiles（归属 064，仅指针）

CLI 能力档案的集合、必填维度、`known` / `unknown`、provenance、U2/U4/U5 观测、probe/feedback、交付与契约测试由 Feature 064 唯一拥有：`.specify/specs/064-subagent-concurrency/requirements.md`（CLI 档案条款）、`contracts/cli-profiles.md`（CLP-01…CLP-17）、`.specify/specs/064-subagent-concurrency/notes/063-overlap-adjudication.md`。本特性 MUST NOT 定义、复制、测试或注册第二套 CLI 档案；本特性的 stream-json 默认（FR-026）与 nohup 脱离（FR-031）是 064 档案记录的既有事实，由 064 引用。

### 显式排除项（Out of Scope）

- 把框架命令内部（`implement`、`review`、`analyze`、`plan` 等）的硬执行改为本约束的一部分；plan 约束限定为编排层纪律。
- 对大型特性启用快车道，或把快车道设为缺省行为。
- 跳过 `analyze`、`review`、独立校验或任何必需的安全检查。
- 改变哨兵字面量、watcher 判定状态机或既有退出码。
- 新增常驻服务、守护进程、外部依赖、模型 API 或网络传输。
- 自动 push、自动合并远程分支或任何绕过确认门的动作。
- 自动把反馈或运行数据外传。
- 在预算之外自动追加全量运行；槽外全量必须为显式例外。
- 重新设计阶段命令的内部测试策略；本特性只约束编排层的运行预算与证据。
- CLI 能力档案的集合、必填维度、`known`/`unknown` 纪律、观测 probe、反馈标记、契约与测试——由 Feature 064 唯一拥有；本特性只保留 stream-json 输出默认与 nohup 脱离，且 MUST NOT 复制档案内容或建立第二套档案/契约/测试。

### Key Entities *(include if requirement involves data)*

- **Run Line（运行线）**: 一条独立的无人值守循环实例；拥有自己的阶段序列、状态脊与产物命名空间。
- **State Spine（状态脊）**: 每线的持久状态文件；承载断点、已试次数、快车道准入记录、测试预算台账、plan 约束状态与阶段证据指针，是续环与重入的唯一依据。
- **Fast-Lane Admission Record（快车道准入记录）**: 一次裁决的完整证据包——裁决值、逐条判据判定、实测 FR/任务数、证据指针、裁决时间，以及回退触发（如发生）。
- **Test Budget Ledger（全量测试预算台账）**: 全量槽位、阶段、目的、执行序号、触发与时间的记录；区分计划槽位、槽内重跑与槽外例外。
- **Stage Run Evidence（阶段运行证据）**: raw stream、派生实时日志、pid/status/heartbeat 四件套、退出记录与测试证据的集合。
- **Plan Change Classification（plan 改动分类）**: 下游阶段对 plan 制品改动的分类结果（小修 / 实质改动 / 未声明），含判定依据与处置去向。
- **Targeted Test Set（定向测试集）**: 按确定性规则选出的测试路径集合，附选择依据与充分性说明。
- **Stage Dispatch Record（派发记录）**: 阶段名、提示词路径、派发形态（是否脱离）、哨兵字面量、deadline、四件套路径与快车道/plan 约束标记。
- **Stall Behavior Baseline（卡死行为基线）**: 冻结提交上由唯一执行体的脚本化驱动夹具（`driver-stall-fixture.py`）观测的三类卡死场景处置元组（watcher 判定、退出码（watcher 判定退出码与 runner rc）、状态脊卡死状态、重试次数（初始固定为 0，记录消耗值）、四要素齐备性、下一阶段是否派发、状态脊是否先写后动），以及同一可执行夹具的收口重放与归一化比较结果；录制 trace 只作补充证据，驱动侧字段 MUST 为夹具观测值，不得从判定表转录或由 trace 替代。
- **CLI Capability Profile / CLI Observation Record（归属 064，不在本特性实体清单）**: 其唯一 owner 为 Feature 064 的 `data-model.md` E9/E10 与 `contracts/cli-profiles.md`；063 不重复定义字段、观测记录或验收。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 在固定夹具集中，100% 的快车道运行带有完整准入记录（全部判据 + 证据指针 + 实测计数）；无记录的 checklist 跳过数为 0。
- **SC-002**: 满足 FR-003 全部判据的中型夹具运行中，`checklist` 派发次数为 0，`analyze` 至少 1 次，`review` 为 1 次；大特性或任一判据失败的夹具 100% 拒绝快车道并派发完整链。
- **SC-003**: 正常路径的每特性运行全量测试槽位数为 2（观测基线为 6 次全量执行）；无记录的槽外全量执行数为 0；带显式例外的超预算运行 100% 在收尾汇总可见。
- **SC-004**: 在 implement 起点基线之后注入一个已知回归，最终全量运行 100% 在名称级差集中发现它，且该失败被修复或显式归因；仅靠计数比较的分支为 0。
- **SC-005**: 每个适用阶段（未按准入记录被快车道跳过的中间阶段，以及 review）的测试证据完整率为 100%；完整判定按证据形态分流——`ran` 阶段须具备命令、选择依据、退出码、计数、新增失败、比较基线六字段，`not-run-docs-only` 阶段须具备阶段状态、选择依据、改动路径证据与证据指针（运行字段不适用，MUST NOT 报 `unknown`），`empty-selection-escalated` 阶段须具备升级后的运行证据或显式例外证据；按准入记录授权跳过的阶段 MUST 记为 [[STR-008]]、不计入完整性分母，并与 `unknown` 严格区分；完整性分母 = 全部适用阶段数（含文档型阶段），整阶段缺失证据记录的阶段计入分母并判未完整，MUST NOT 静默缩小分母；收口审计 MUST 输出 `stages=N complete=N`；无选择依据的测试运行数为 0；证据缺失在收口审计中被报告为 unknown 的比例为 100%。
- **SC-006**: 下游阶段对 plan 制品的改动 100% 被分类；未声明改动与实质性改动 100% 被 U4 判门失败；静默重审回环数为 0；小修后的 analyze 门结果与完整链一致。
- **SC-007**: 在一个有事件输出的阶段中，每个有效进度事件自被 runner 接收（写入 raw stream 的时刻）到对应派生行写入紧凑实时日志的延迟不超过 120 秒（事件→派生行延迟）；无事件的静默区间不适用该阈值；阶段无事件时伪造进度行数为 0（每条派生行 MUST 可追溯到一条 raw 事件）；驱动独立 `sleep` 回合与固定 cadence 空转次数为 0。
- **SC-008**: 驱动进程中途退出后，脱离阶段继续并完成的比例为 100%；新会话凭状态脊与 `--once` 快照接管、且未重新派发已完成阶段的比例为 100%。
- **SC-009**: 非终止事件中的哨兵字样被判 DONE 的次数为 0；终止结果事件中的哨兵被正确识别的比例为 100%；派生失败时伪 DONE 次数为 0。
- **SC-010**: 未授权 push 次数为 0；确认门绕过次数为 0；独立校验绕过次数为 0；卡死场景（超时 / 重试上限 / 伪完成）的处置结果与 [[STR-007]] 行为基线逐字段一致率为 100%（归一化后零差异；基线在实现首个行为面提交之前的冻结提交上录制，七字段包含驱动侧观测值，由唯一执行体的脚本化驱动夹具产生并经同一可执行夹具重放比较，录制 trace 只作补充证据）；把名称级测试失败基线冒充行为基线的次数为 0；从判定表转录驱动侧字段的次数为 0；以录制 trace 替代夹具观测驱动侧字段的次数为 0。
- **SC-011**: 不支持 stream-json 的 CLI 运行 100% 记录降级标记，伪 DONE 次数为 0，因降级导致的阶段失败次数为 0。
- **SC-012**: 既有 loop-driver 契约测试 100% 保持绿色，或因本特性被有意更新且有记录；相对冻结基线零新增失败（名称级差集为空）；镜像判据 = 本特性触碰的 `sdd-loop-driver` 镜像对零 drift，且全部镜像对相对冻结基线零 NEW drift；其余镜像对的既有漂移作为已记录基线例外保留、不得扩大；未启用快车道的默认行为与改动前一致。
- **SC-013**: 本特性自身运行包含 `checklist`、`analyze`、`review` 的产物与证据；本特性自身运行中的快车道记录数为 0。

> **CLI 能力档案验收（归属 064）**：档案集合、八维、`known`/`unknown`、观测反馈、probe 注册、交付与镜像由 Feature 064 的 SC-006 与 `contracts/cli-profiles.md` 拥有；本特性不重复其成功标准。

### Measurement Sources & Collection Methods

- **SC-001 / SC-002 / SC-003 / SC-005 Source**: 固定夹具运行记录（阶段派发记录、状态脊、收口汇总）加程序化审计脚本；FR 定义行与任务行按 FR-003(a) 的固定模式由确定性命令复算，不手抄；SC-005 的授权跳过阶段以 E1 准入记录与 [[STR-003]] 联结，按 [[STR-008]] 计入不适用项、不计入分母；完整性分母 = 全部适用阶段（含 `not-run-docs-only` 文档型阶段），文档型阶段按缩减字段集判定、运行字段不适用且不报 `unknown`，整阶段缺失证据记录计入分母并判未完整；收口审计逐阶段核对并输出 `stages=N complete=N`。
- **SC-004 Source**: 注入回归夹具的运行证据：implement 起点名称级基线、最终全量运行的 `comm -13` 输出、修复或归因记录。
- **SC-006 Source**: 夹具运行中的 `git diff` 分类记录、U4 校验结论、状态脊约束状态与收尾汇总。
- **SC-007 Source**: raw stream 逐行接收时间戳（runner 从 CLI 读取并写入时打点）与派生实时日志逐行时间戳的逐事件配对；对每条有对应事件的行计算事件→派生行延迟并与 120 秒比较，无事件区间不计入；伪造行审计 = 无对应 raw 事件的派生行计数（须为 0）；驱动调用序列用于独立 `sleep` / 固定 cadence 审计。
- **SC-008 Source**: 脱离存活夹具：中途终止驱动进程，检查 runner 的退出记录与阶段产物；重入演练记录 `--once` 快照与派发决策。
- **SC-009 Source**: 派生与 watcher 夹具：非终止事件注入、终止结果事件、派生失败三类用例的判定记录。
- **SC-010 Source**: 冻结提交上的三类卡死场景录制 [[STR-007]]（超时 / 重试上限 / 伪完成）。watcher 提供 U3 判定；驱动侧字段由唯一执行体的脚本化驱动夹具（`tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py`）执行 U4/U5 程序、以 stub runner 驱动重试消耗，并从状态脊快照、派发记录与退出记录观测产生；录制 trace 只作补充证据，MUST NOT 替代夹具观测。夹具 MUST NOT 从判定表转录、硬编码期望值或从基线文件回填。录制与收口重放 MUST 使用同一可执行夹具与同一初始已试次数（0），归一化剔除时间戳、PID、绝对路径与耗时后逐字段比较；退出码 MUST 区分 watcher 判定退出码与 runner rc；证据类别（自动夹具 / 录制驱动 trace）在验证记录中如实标注；确认门与独立校验由契约条款测试覆盖。
- **SC-011 Source**: 降级夹具：不支持 stream-json 的 CLI 桩、状态脊降级标记、判定与退出码记录。
- **SC-012 Source**: 改动前用 `scripts/bash/run-tests.sh --names-out <file>` 冻结失败名单，改动后用同一命令输出并以 `comm -13` 断言为空；`scripts/python/sync-mirrors.py --check` 的输出按镜像对归属统计——本特性拥有的 `skills/external/sdd-loop-driver` ↔ `.specify/skills/sdd-loop-driver` 对零 DIFF，全部镜像对相对冻结基线零 NEW DIFF，其余镜像对的既有 DIFF 逐条保留在冻结基线清单中并记录为已披露例外。
- **SC-013 Source**: 本规格目录的 `checklists/`、analyze/review 产物与收尾汇总；检索本特性运行记录中的快车道标记（应为 0）。
- **CLI 能力档案 Source（归属 064）**: 由 Feature 064 的 SC-006 与 `contracts/cli-profiles.md` 拥有；063 不重复测量。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "--output-format stream-json" | FR-026, FR-029 |
| `STR-002` | "-DONE" | FR-028, FR-033 |
| `STR-003` | "checklist=skipped(fast-lane)" | FR-004, FR-005 |
| `STR-004` | "progress=degraded" | FR-030 |
| `STR-005` | "ANOMALY:" | FR-021 |
| `STR-006` | "fast-lane=opt-in" | FR-002, FR-004 |
| `STR-007` | "notes/stall-behavior-baseline.json" | FR-038, SC-010 |
| `STR-008` | "not-applicable-skipped-stage" | FR-012, SC-005 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-10-20

- Q: 063 应绑定既有 Feature 058（无人值守 SDD 循环驱动机制）作为演化特性，还是新建 Feature？ → A: 绑定 058。四项优化的承载面均为 058 的 driver skill 面（派发配方、watcher、阶段提示词），扩展同一机制、无新增能力域，符合 reuse-first；058 保持 Implemented，不回退。
- Q: FR-002 的「入口声明 / 入口协议」如何成为可审计的显式启用？ → A: 以 [[STR-006]] 字面量定义入口启用；必须出现在 U0 入口声明并原文写入状态脊。无人值守运行只认该字面量；交互式用户在场时允许驱动提议一次并记录原文采纳，但不得因等待回答阻塞运行。
- Q: 8–30 条 FR / 10–40 条任务的中型区间是否在 clarify 冻结，还是保留 plan 调整权？ → A: 冻结为权威基线；SC-002 夹具与准入裁决依赖精确阈值，plan MUST NOT 自行调整，确需变更走显式范围修订并同步 SC-002。
- Q: 全量测试预算的作用域是每条运行线还是同一特性的多条线共享？ → A: 以运行线为作用域；每线独立台账与两个槽位，多线并行互不共享或消耗，避免跨线协调破坏「一线一状态脊」的独立性。
- Q: U4 发现实质性或未声明 plan 改动时，何时上送决策、何时派发完整 plan 重审？ → A: 采用确定性两分支：修复既有缺陷且不改变已批准范围/架构/数据模型/契约/任务分解 → 派发完整 plan 重审；改变上述任一项、引入新能力或安全面、或无法判定 → 四要素上送，不自行重审。

### Session 2026-10-20（requirements-repair 第 1 轮，analyze 门回环）

- Q: SC-010 的「改动前基线」采用什么证据形态？ → A: 采用行为基线，不收窄为契约测试、也不用名称级测试失败基线替代。规格冻结读数为 `ba2a18db`；实现前复核（N-08）发现其后的首个行为面提交为 `9e69f3de`，实际基线改取首个行为面改动前的父提交 `a1aac7e5` 并在状态脊记录差异；在实现首个行为面提交之前，用超时 / 重试上限 / 伪完成三类场景夹具录制处置元组到 [[STR-007]]；收口以同一组夹具重放，归一化剔除时间戳、PID、绝对路径与耗时后逐字段比较，零差异为通过。名称级测试基线只服务于 SC-012。
- Q: FR-022 的「已批准需求基线」绑定到什么制品与提交？ → A: 绑定 plan U4 通过时记录的 `plan_commit` 中 `requirements.md` 的 FR/SC 定义集合与语义；U4 分类记录写入 `approved_baseline_commit`，分支 (a)/(b) 只与该提交比较，不得使用工作树当前文本或其它提交替代。
- Q: SC-007 的 120 秒阈值计时对象是什么？ → A: 事件→派生行延迟——每条有效事件从 runner 接收（写入 raw stream）到对应派生行写入 live log 不超过 120 秒；无事件区间不适用该阈值，且不得为填补空白伪造进度行；每条派生行必须可追溯到一条 raw 事件。
- Q: 快车道授权跳过的 checklist 在 SC-005 的 100% 证据完整率中如何计？ → A: 记为 [[STR-008]]，不计入分母，且不得记为 `unknown`；联结依据是 E1 准入记录与 [[STR-003]]。
- Q: SC-012 的「镜像零漂移」覆盖多大范围？ → A: 本特性触碰的 `sdd-loop-driver` 镜像对零 drift，全部镜像对相对冻结基线零 NEW drift；其余镜像对的既有漂移作为已记录基线例外保留、不得扩大。
- Q: FR 定义行与任务行的计数语法是什么？ → A: FR 定义行 = `^- **FR-[0-9]{3}**:`（含英文冒号），SC 行与说明行不计入；任务行 = `^- \[[ xX]\] T[0-9]{3}`（准入唯一 owner）。仓库实测/记账命令使用的宽模式 `^- \[[ xX>~]\] T[0-9]{3}` 仅用于仓库任务行记账（当前全为 `[ ]` 时两者同为 52），MUST NOT 用于准入判定；两者不得混用。

### Session 2026-10-20（requirements-repair 第 2 轮，analyze 门回环）

- Q: SC-010 的驱动侧字段如何成为可复算证据？ → A: 保留 100% 实测一致率，不降级。三类场景的驱动侧字段 MUST 由唯一执行体的脚本化驱动夹具（`driver-stall-fixture.py`）观测产生；录制 trace 只作补充证据，MUST NOT 替代夹具观测。watcher 只提供 U3 判定；录制固定并记录初始已试次数（0），退出码 MUST 区分 watcher 判定退出码与 runner rc；收口由同一可执行夹具重放驱动侧步骤，MUST NOT 从判定表转录或仅重读基线文件。名称级测试失败基线只服务 SC-012。
- Q: `requirements.md` 在 plan U4 后被合法修改时，批准基线如何重新锚定？ → A: 在下一个依赖该基线的 U4 分类前记录 re-baseline 事件（触发、时间、前一基线、新基线 = 包含该变更的提交、FR/SC 差异摘要），`approved_baseline_commit` 更新为新基线；变更未提交或无法定位提交时不得 re-anchor，受影响 plan 改动按 FR-022(b) 上送；re-anchoring 不构成 plan 重审、不移动约束生效点，后续分支判定以最新基线为准。
- Q: SC-005 的完整性分母与 `not-run-docs-only` 如何计？ → A: 分母 = 全部适用阶段（含文档型阶段）；文档型阶段按缩减字段集（阶段状态、选择依据、改动路径证据、证据指针）判完整，运行字段不适用且不报 `unknown`；授权跳过（[[STR-008]]）不计入分母；整阶段缺失证据记录计入分母并判未完整；收口审计 MUST 输出 `stages=N complete=N`。

### Session 2026-10-20（tasks-repair-2，CLI-profile 重叠收口）

- Q: 063 在 plan-repair-2 临时加入的 CLI 能力档案条款如何处置？ → A: 按 Feature 064 的 `notes/063-overlap-adjudication.md` 逐条裁决迁入 064（064 的 CLI 档案条款与 `contracts/cli-profiles.md` CLP-01…CLP-17）。063 删除 US6、CLI-profile 临时条款（FR 编号段 044–049、SC 编号段 014–016）、CLI 实体、CLI 边界用例、两个 CLI 共享字符串、provisional 契约与档案测试；只保留指向 064 的指针，禁止双 owner 或静默复制。
- Q: 063 最终保留哪些能力？ → A: 四项吞吐优化（快车道、两槽位测试预算、plan 只小修、stream-json 进度与 nohup 脱离）。stream-json 输出默认（FR-026）与 nohup 脱离（FR-031）作为 064 档案记录的既有事实由 064 引用；063 不复制档案内容。
- Q: probe/feedback 注册如何处置？ → A: 由 064 的最小 Probe Object `skill-sdd-loop-driver-cli-profile` 承担；063 不注册、不修改 `shared/definitions/probe-definitions.md`，不新增任何 CLI-profile 专用 Object 或测试。
- Q: 编号与计数如何收口？ → A: FR 收口到 FR-043，SC 收口到 SC-013，Shared Strings 收口到 STR-008；所有 FR/SC/条款/任务/交付计数与引用 MUST 重算，`validate-requirements.py` 与 `validate-tasks.py` exit 0，且无悬空引用或重复定义。
- Q: 本特性与 064 的依赖方向是什么？ → A: 输出模式的吞吐默认（stream-json）由 063 拥有，064 CLP-08 只记录事实、不得改写；063 实现 stream-json/nohup 时可只读引用 064 的 `references/cli/index.md` 与档案，但 MUST NOT 新增/修改该目录、复制其内容或另立契约。

### Session 2026-10-20（implement 起点，analyze-rerun-3 记录项落地）

- Q: SC-010 的行为基线提交取哪个？ → A: 规格冻结读数 `ba2a18db` 不适用。实现前复核 `git log --oneline ba2a18db..HEAD -- skills/external/sdd-loop-driver/SKILL.md references scripts` 显示首个行为面提交为 `9e69f3de`（Feature 064 的 line registry），故按 FR-038 的兜底条款改取首个行为面改动前的父提交 `a1aac7e5` 作为实际行为基线；差异写入状态脊 stall baseline 行、`notes/pre-change-measurements.md` 与 plan.md § Plan Repair Record 第 5 轮。
- Q: 驱动侧字段的证据形态是否允许 trace 替代夹具？ → A: 不允许。`tests/fixtures/sdd_loop_efficiency/driver-stall-fixture.py` 是唯一执行体与唯一驱动侧字段来源；录制 trace 只能作补充证据，不得替代夹具观测（L-04 收窄）。
