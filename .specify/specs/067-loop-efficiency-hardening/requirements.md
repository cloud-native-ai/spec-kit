# Requirements Specification: sdd-loop-driver 执行效率加固（Loop Efficiency Hardening）

**Requirement Branch**: `067-loop-efficiency-hardening`（intended branch; this draft was created on `065-loop-interruption-recovery` for speed）
**Created**: 2026-10-22
**Status**: Draft
**Input**: User description (2026-10-22): "当前又遇到了效率问题,需要进行一下诊断" → 以 `063-sdd-loop-efficiency` 为参考，把 065a implement 阶段暴露的效率问题固化为一个新 spec：分段派发、part brief、测试经济学、派发级测量与驱动往返收敛。本条 spec 只完成需求；实现走后续阶段。

## Related Feature *(mandatory)*

**Feature ID**: 058

**Feature Name**: 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver）

**Binding rationale**: 本 spec 与 063 一样是 Feature 058 的演化规格（new spec, not a new Feature）：所有效率加固点都落在 `skills/external/sdd-loop-driver/` 的派发/阶段执行承载面，扩展同一机制而非新增能力域。058 的状态保持 `Implemented`，不回退；不新增 Feature ID、不改注册表计数。

## 现状锚点（2026-10-22，dated record；仅作可行性输入，非运行时保证）

- 065a implement 阶段 30 个任务、60 条契约：首个子代理达 40-turn 上限；第二个达 output-token 上限；预算调整为 120 并分段后，T003–T014 由 3 个有界子派发完成。
- 诊断时：14/30 tasks done；unit 58 / contract 25，57 passed / 26 failed；26 个红项集中在 T015 动作 18、T016 probe 5、T018 reference 3。
- 每次子派发都重新读取 tasks/contracts/tests；状态脊有高层 checkpoint，但没有 part brief（任务 ID、目标测试 node id/命令、预期红→绿、禁改文件）。
- 测试先行面积大：83 个测试先于引擎，T015 的 C-46 动作矩阵与 T016 的 probe 矩阵仍是逐条测试写法，尚未表驱动化。
- token/耗时：run-determination 记录为 `not_evaluated`；现状只能用派发次数、任务完成率、测试红项数作为代理指标。

## Assumptions（clarify 阶段可推翻）

- 063 的四项吞吐优化（快车道、两槽位测试预算、plan 只小修、进度可见/脱离）保持不变；本 spec 只补“分段执行 + 测试经济学 + 测量 + 往返收敛”。
- 阶段执行子代理默认 `run-turn-budget` 为 120（已由 commit `696d5f4b` 固化）；本 spec 不主张再次普涨，预算变更必须有派发级证据。
- “忽略测试”是一次显式用户豁免，不是默认策略；豁免必须写入 verification 与 gate 记录，且不得把未跑测试声称为通过。
- 本 spec 自身仍走完整 SDD 链（checklist/analyze/review）；本文件只完成 requirements 阶段。
- 不引入常驻服务、守护进程、外部依赖或新模型 API；测量与分段只用现有 skill/agent/state-spine 载体。
- 065a 是本案的 case study，不是本 spec 的 owner；本 spec 的 owner 是 sdd-loop-driver 的派发与执行规则。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 有界分段派发：part brief 与预算匹配 (Priority: P1)

驱动者把一个大阶段拆成可独立验证的 part；每个 part 在派发前写出 part brief（任务 ID、文件、测试目标、预期红→绿、禁改文件、预算），子代理在预算内完成并回传 `PARTn-DONE` 或 `ANOMALY`，驱动者 U4 通过后才进入下一 part。

**Why this priority**: 40-turn 与 output-token 两次失败的直接原因就是“阶段太大 + 没有 brief”；这是吞吐的主约束。

**Independent Test**: 对一个含 30 任务的 implement 夹具，检查每个 sub-dispatch 都有 part brief、预算、part 结果与 U4 记录；统计预算耗尽次数。

**Acceptance Scenarios**:

1. **Given** 一个 30 任务的 implement 阶段，**When** 驱动者开始分段，**Then** 每个 part 的 brief 含任务 ID、文件、目标测试命令/node id、预期红→绿、禁改文件与 `run-turn-budget`，并写入状态脊。
2. **Given** 一个 part 在预算内完成，**When** 子代理回传 `PARTn-DONE`，**Then** 驱动者独立核验任务/测试/提交后才派发下一 part；不得凭子代理自报通过。
3. **Given** 一个 part 达到预算上限，**When** 驱动者处置，**Then** 按 U5 记录 budget-exhausted，缩小 part 或升预算后重派；不得用同一预算原样重试。
4. **Given** 一个 part 的红测试面超过该 part 的预算所能覆盖，**When** 驱动者切分，**Then** 按可验证结果（动作矩阵 / probe / reference / docs / verification）切分，而不是按任务号机械切 8 条。

### User Story 2 - 测试经济学：表驱动、定向选择与显式豁免 (Priority: P1)

执行者用表驱动/参数化测试和既有 fixture 覆盖矩阵型契约；中间 part 只跑目标测试集，全量套件沿用 063 的两槽位预算；用户显式要求忽略测试时，verification 记录 `waived/not-run`，gate 项按豁免处置，绝不伪绿。

**Why this priority**: 测试先行面积是当前最大的回合消耗来源；测试豁免又最容易演变成静默降质。

**Independent Test**: 检查 T015/T016 的测试是否表驱动；检查一次中间 part 的运行命令是否为定向集；检查一次显式豁免的 verification 是否没有 “pass” 伪称。

**Acceptance Scenarios**:

1. **Given** C-46 的 18 个动作组合，**When** 执行者编写测试，**Then** 使用一个表驱动/参数化用例承载行级矩阵，而不是 18 个独立函数的重复样板。
2. **Given** 一个中间 part 只改了动作模块，**When** 执行者验证，**Then** 只跑动作相关的定向测试；全量套件只在 063 规定的两个槽位运行。
3. **Given** 用户显式声明“忽略测试”，**When** 收口写 verification，**Then** 测试项记 `waived/not-run` 与豁免原文，Completion Gate 的测试项记 `void/waived`，不得写 `pass`。
4. **Given** 一个测试因夹具/断言过严而非契约失败，**When** 执行者修正，**Then** 修正必须附契约依据并写入 red-first-evidence；不得为变绿削弱契约。

### User Story 3 - 派发级测量与学习 (Priority: P2)

驱动者记录每个 part 的 task ID、turn 数（可得时）、测试 pass/fail 增量、commit、outcome 与耗时/ token 代理；不可得指标记 `not_evaluated`，不编造数字。下一轮分段用这些记录调整 part 大小与预算。

**Why this priority**: 当前只有派发次数与红项数，无法判断预算是否真的够、哪类 part 最吃回合。

**Independent Test**: 检查状态脊的 dispatch log 是否覆盖本 spec 的每个 part；删除一条记录后能否从日志恢复下一步分段决策。

**Acceptance Scenarios**:

1. **Given** 一个完成的 part，**When** 驱动者收口，**Then** dispatch log 追加 part/task/turn/test/commit/outcome；turn 或 token 不可得时写 `not_evaluated`。
2. **Given** 连续两个 part 的 turn 数接近预算，**When** 驱动者规划下一 part，**Then** 缩小任务面或升预算，并记录依据。
3. **Given** 一个 part 的测试红项没有减少，**When** 驱动者评估，**Then** 记录为 no-progress，不得仅凭“已提交”宣称进展。

### User Story 4 - 微缺口合流与驱动往返收敛 (Priority: P2)

小的 U4 缺口（如一个路径回退、一个断言）默认并入下一 part 的 brief，而不是单独派发；非破坏性的 implement/test 连续段可一次性预授权，遇到 ANOMALY 或破坏性门才停。

**Why this priority**: 微缺口单独派发与频繁确认会把“无人值守”退化成多轮往返。

**Independent Test**: 检查一次含微缺口的运行是否把缺口并入下一 part；检查一次预授权运行是否只在破坏性门停下。

**Acceptance Scenarios**:

1. **Given** U4 发现一个不影响 gate 的小缺口，**When** 驱动者规划下一 part，**Then** 缺口进入下一 part 的 brief 与验收项，不单独派发。
2. **Given** 用户预授权“按 split plan 继续非破坏性 implement/test”，**When** 运行推进，**Then** 驱动者不逐 part 请求确认；遇到 merge/push/删除/强推等破坏性动作仍停。
3. **Given** 一个微缺口阻塞 gate，**When** 驱动者处置，**Then** 允许单独派发并记录原因，不得为了省派发而跳过 gate。

### Edge Cases

- Part brief 缺失或没有目标测试命令：驱动者 MUST NOT 派发，先补 brief。
- Part 达到 turn 或 output-token 上限：按 U5 记录 budget-exhausted；同一预算不得原样重试。
- 用户豁免测试：verification 与 gate 记录豁免原文；review 必须看到该豁免，不得把 waived 当 pass。
- Part 依赖前一部分的产物：按 tasks.md 的 blockedBy 串行；无依赖的 part 可并行（宿主支持时），但共享状态脊字段需串行写入。
- 测量指标不可得：记 `not_evaluated`；不得用 0 或估算值替代。
- Part 切分后仍超过预算：继续按可验证结果切小，而不是升预算掩盖问题。

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: 每个子派发 MUST 有一份 part brief，至少含任务 ID、允许修改的文件、目标测试命令/node id、预期红→绿、禁改文件、`run-turn-budget` 与本 part 的验收方式；brief 写入状态脊或独立 `part-brief.md`，子代理只按 brief 执行。
- **FR-002**: 大阶段（implement >20 任务或契约 >40 条）MUST 拆为 ≤8 任务的 part；当红测试面集中在一类断言时，MUST 按可验证结果切分（动作矩阵 / probe / reference / docs / verification），不得按任务号机械切分。
- **FR-003**: 阶段执行子代理默认 `run-turn-budget` 为 120；预算变更 MUST 有派发级证据（turn 数、预算耗尽记录、任务/测试面），并同步 `agents/sdd-executor.agent.md`、`.specify/agents/templates/`、各工具 render 与 skill 源文件。
- **FR-004**: 子派发 brief MUST 要求执行者用工具分段写文件（每次 Write/Edit 一部分），MUST NOT 在一个回复里输出整段实现或整份测试；回传只给改动清单、测试计数、提交哈希与残留风险。
- **FR-005**: 矩阵型契约的测试 SHOULD 使用表驱动/参数化与既有 fixture；中间 part MUST 只跑目标测试集，全量套件 MUST 遵守 063 的两槽位预算（implement 起点与最终收口），槽外全量必须显式例外。
- **FR-006**: 用户显式要求忽略测试时，verification MUST 记 `waived/not-run` 与豁免原文；Completion Gate 的测试相关项 MUST 记 `void/waived`；任何产物 MUST NOT 把未跑测试写成 `pass` 或 `green`。
- **FR-007**: 驱动者 MUST 为每个 part 追加 dispatch log：part ID、task IDs、turn 数（可得时）、测试 pass/fail 增量、commit、outcome、耗时/token 代理；不可得指标记 `not_evaluated`，不得编造数字。
- **FR-008**: 不影响 gate 的 U4 微缺口 MUST 默认为并入下一 part 的 brief 与验收项，不单独派发；仅当缺口阻塞 gate 或跨越 part 边界时才允许单独派发，并记录原因。
- **FR-009**: 驱动者 MAY 对非破坏性的 implement/test 连续段做一次性预授权（按 split plan 继续，遇到 ANOMALY 或破坏性门才停）；merge/push/删除/强推等破坏性动作 MUST 继续走确认门。
- **FR-010**: 本 spec 的 owner 是 sdd-loop-driver 的 `SKILL.md`、`references/dispatch-recipes.md` 与 `agents/sdd-executor.agent.md`；运行时镜像与各工具 render MUST 由生成命令产出并验证，不得手改镜像。

### Key Entities *(include if requirement involves data)*

- **DispatchPart**: `part_id`、`task_ids[]`、`scope`、`turn_budget`、`status`、`commit`。
- **PartBrief**: 任务 ID、允许修改文件、目标测试命令/node id、预期红→绿、禁改文件、验收方式。
- **DispatchLog**: `part_id`、`turns`、`tests_passed`/`tests_failed` 增量、`commit`、`outcome`、`elapsed`/`token` 代理（不可得为 `not_evaluated`）。

### Out of Scope

- 修改 063 的四项吞吐优化本身；本 spec 只补分段执行、测试经济学、测量与往返收敛。
- 新增常驻服务、守护进程、外部依赖或模型 API。
- 全局关闭测试门；测试豁免只能由用户显式声明，且必须留痕。
- 绕过 merge/push/删除/强推的确认门。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对 065a 同规模的 30-task implement 夹具，采用本 spec 的分段策略后，预算耗尽子派发为 0，且完成派发数 ≤5（以 dispatch log 计；无可比数据时如实记 `not_evaluated`）。
- **SC-002**: 100% 的子派发都有 part brief 与 dispatch log 条目；驱动者能在不重读全部规格的情况下从 brief 恢复下一 part。
- **SC-003**: 每个 part 的测试红面有界且可归属；全量套件运行次数不超过 063 的两槽位预算。
- **SC-004**: 所有测试豁免在 verification 中可检索（`waived`/`not-run` + 豁免原文），全仓不存在把 waived 写成 pass 的产物。
- **SC-005**: 非破坏性 implement/test 连续段的驱动往返次数较 065a 现状下降（以用户确认次数/驱动轮次计；不可得时记 `not_evaluated`）。

### Measurement Sources & Collection Methods

- 状态脊 dispatch log（part/task/turn/test/commit/outcome）。
- `notes/red-first-evidence.md` 与测试运行输出（pass/fail 增量）。
- git commit 哈希与 `git log`。
- token/耗时：run-determination/exec-quant 若不可得，记 `not_evaluated`；不得伪造。

## Clarifications

### Session 2026-10-22

- Q: 新 spec 绑定哪个 Feature？ → A: 绑定 Feature 058（与 063 同一演化特性承载面），不新建 Feature、不改注册表计数；058 状态保持 Implemented。
- Q: 本 spec 是否立即走完整 SDD 链？ → A: 本次只完成 requirements 创建；后续 checklist/analyze/plan 按用户排期推进。
- Q: 065a 当前的 completed 是否受本 spec 影响？ → A: 不受；本 spec 是新需求，065a 继续按用户“忽略测试、尽快收口”的显式授权完成当前周期。
