# Requirements Specification: sdd-loop-driver 执行效率加固（Loop Efficiency Hardening）

**Requirement Branch**: `067-loop-efficiency-hardening`（intended branch; this draft was created on `065-loop-interruption-recovery` for speed）
**Created**: 2026-10-22
**Status**: Draft
**Input**: User description (2026-10-22): "当前又遇到了效率问题,需要进行一下诊断" → 以 `063-sdd-loop-efficiency` 为参考，把 065a implement 阶段暴露的效率问题固化为一个新 spec：分段派发、part brief、测试经济学、派发级测量与驱动往返收敛。本条 spec 只完成需求；实现走后续阶段。2026-10-22 追加指令（原文逐字）：「继续进行.specify/specs/067-loop-efficiency-hardening中的流程开发,重点在用测试优化, 当前的测试流程太重了, 需要针对当前speckit框架自身的测试流程进行大幅度精简,保证跑一遍完整的测试不超过10分钟。」——据此新增「框架测试套件瘦身」P1 范围（User Story 5、FR-011…FR-021、SC-006…SC-010），与 063 的测试经济学约束正交叠加、不得冲突。

## Related Feature *(mandatory)*

**Feature ID**: 058

**Feature Name**: 无人值守 SDD 循环驱动机制（Unattended SDD Loop Driver）

**Binding rationale**: 本 spec 与 063 一样是 Feature 058 的演化规格（new spec, not a new Feature）：所有效率加固点都落在 `skills/external/sdd-loop-driver/` 的派发/阶段执行承载面，扩展同一机制而非新增能力域。058 的状态保持 `Implemented`，不回退；不新增 Feature ID、不改注册表计数。2026-10-22 范围扩展注记：新增的测试套件瘦身承载面是框架自身的 `tests/` 测试面与规范运行器（开发侧测试经济学），其收益（一次完整运行墙钟 ≤600 秒）直接降低 058/063 两槽位预算的单次成本，仍属同一循环效率演化，不新增 Feature。

## 现状锚点（2026-10-22，dated record；仅作可行性输入，非运行时保证）

- 065a implement 阶段 30 个任务、60 条契约：首个子代理达 40-turn 上限；第二个达 output-token 上限；预算调整为 120 并分段后，T003–T014 由 3 个有界子派发完成。
- 诊断时：14/30 tasks done；unit 58 / contract 25，57 passed / 26 failed；26 个红项集中在 T015 动作 18、T016 probe 5、T018 reference 3。
- 每次子派发都重新读取 tasks/contracts/tests；状态脊有高层 checkpoint，但没有 part brief（任务 ID、目标测试 node id/命令、预期红→绿、禁改文件）。
- 测试先行面积大：83 个测试先于引擎，T015 的 C-46 动作矩阵与 T016 的 probe 矩阵仍是逐条测试写法，尚未表驱动化。
- token/耗时：run-determination 记录为 `not_evaluated`；现状只能用派发次数、任务完成率、测试红项数作为代理指标。

### 框架测试套件现状（2026-10-22，dated record；来源命令/文件随条注明）

- 完整测试入口 = `scripts/bash/run-tests.sh`（规范运行器，自动解析带 pytest 的解释器；本机解析 Python 3.14.6 + pytest 9.1.1；裸 `python3 -m pytest` 不可用）。来源：运行器首行输出 `# test runner:` 加解释器探针（2026-10-22 实测）。
- 规模：298 个测试文件（来源：`find tests -name 'test_*.py' -type f | wc -l`）；约 4553 条用例（contract 3428 / unit 734 / integration 391；来源：驱动者盘点 2026-10-22，计数命令未随附，待基线日志复核）。`pyproject.toml` 仅注册 contract / integration 两个标记，unit = 未标记层。
- 速度线索：063 review 记录 144 条定向用例 123.64s（约 0.86 秒/条；来源：`.specify/specs/063-sdd-loop-efficiency/review.md` 与 `test-evidence/review.jsonl`）。按此外推全量约在 65 分钟量级（纯外推估计，非测量），明显超过 10 分钟；定向集偏快，全量真实值以后台基线为准。
- slow-pattern 线索：驱动者盘点约 234 个测试文件含 subprocess/CliRunner、25 个含 copytree、9 个含 time.sleep（计数命令未记录）；本文件可复算口径（2026-10-22，对测试文件逐一 `grep -rl` 计数）为 110 / 12 / 6。两口径数量级一致，均支持「套件成本以子进程冷启动与工作区复制为主」的同一结论；口径差异披露见 `notes/test-slimming-scope-2026-10-22.md`。
- 仓库无 CI 测试工作流（`.github/workflows/` 不存在，2026-10-22 实测）。
- 全量基线正由驱动者在后台测量（命令 `bash scripts/bash/run-tests.sh -q --durations=50`，落盘 `notes/baseline-full-2026-10-22.log`）；本 spec 更新时该日志未完成，未作为任何证据读取，也不随本 part 提交。

## Assumptions（clarify 阶段可推翻）

- 063 的四项吞吐优化（快车道、两槽位测试预算、plan 只小修、进度可见/脱离）保持不变；本 spec 只补“分段执行 + 测试经济学 + 测量 + 往返收敛”。
- 阶段执行子代理默认 `run-turn-budget` 为 120（已由 commit `696d5f4b` 固化）；本 spec 不主张再次普涨，预算变更必须有派发级证据。
- “忽略测试”是一次显式用户豁免，不是默认策略；豁免必须写入 verification 与 gate 记录，且不得把未跑测试声称为通过。
- 本 spec 自身仍走完整 SDD 链（checklist/analyze/review）；本文件只完成 requirements 阶段。
- 不引入常驻服务、守护进程、外部依赖或新模型 API；测量与分段只用现有 skill/agent/state-spine 载体。
- 065a 是本案的 case study，不是本 spec 的 owner；本 spec 的 owner 是 sdd-loop-driver 的派发与执行规则。
- （2026-10-22 范围扩展，以下为开放项，不擅自定案，clarify 裁决）
- **测量主机口径**：≤600 秒预算以 2026-10-22 基线开发主机（macOS，Python 3.14.6 + pytest 9.1.1，规范运行器）为测量口径；其他主机/CI 口径是否需要另行达标，open。
- **冷/热缓存口径**：达标计时取冷启动（清理 pytest 缓存后的首次完整运行）还是热缓存运行，open；倾向冷启动更可信，等待基线日志与 clarify 定案。
- **并行依赖准入**：是否允许引入 dev-only 并行依赖（如 pytest-xdist 或等价插件），open；FR-017 按「允许且受约束」书写，若 clarify 否决，其「等价加速」分支仍可用，本 spec 不预设结论。
- **「完整运行」边界**：假设 = contract / unit / integration 三层在单次运行器调用中全部执行（含收集与夹具时间）；诊断性标记分层不得改变该边界。
- **合并粒度**：假设测试文件级合并（减少文件数）与用例级合并（表驱动/参数化）都在允许范围内，两者均须台账留证。
- **计数口径披露**：4553 条用例与 234/25/9 slow-pattern 数字来自驱动者盘点；slow-pattern 的可复算口径（110/12/6）差异已披露于 `notes/test-slimming-scope-2026-10-22.md`，不影响结论方向。

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

### User Story 5 - 框架测试套件瘦身：一次完整运行 ≤10 分钟 (Priority: P1)

框架开发者在 spec-kit 自身仓库执行完整测试（063 两槽位预算中的任一槽位）。现状套件以逐测试子进程冷启动与逐测试工作区复制为主成本，全量墙钟远超可接受范围（现状锚点 § 框架测试套件现状）。瘦身完成后，一次完整运行在开发主机上的墙钟不超过 600 秒；测量可重复（固定命令、落 dated 证据）；测试覆盖与漂移防护不下降；失败仍可定位到唯一测试 id。瘦身靠让测试变快、变薄（表驱动合并、fixture 复用、并行或等价加速），绝不靠少跑层、删覆盖或重定义「完整运行」。

**Why this priority**: 用户 2026-10-22 指令的直接要求；完整运行是 063 两槽位预算中每次槽位的固定成本，直接决定无人值守循环的基线与收口耗时，是当前测试流程「太重」的主约束。

**Independent Test**: 瘦身前后各用固定测量命令执行一次完整运行并比较墙钟与分层计数；对基线测试 id 清单与留证台账做集合核对；在合并后的表驱动用例中注入单行失败验证定位能力；核对钉住类契约测试清单仍在完整运行内。

**Acceptance Scenarios**:

1. **Given** 瘦身后的仓库，**When** 用固定测量命令在开发主机上执行一次完整运行，**Then** 墙钟 ≤600 秒，证据（命令、主机、日期、退出码、分层计数、墙钟）落入本 spec 目录 `test-evidence/`；不得以估算、外推或子集运行支撑达标主张。
2. **Given** 同一次完整运行，**When** 审计其构成，**Then** contract / unit / integration 三层全部执行且无路径/测试过滤器；相对基线清单被移除或合并的每条测试都能在留证台账中指向保留的等价覆盖。
3. **Given** 一条被合并进表驱动用例的原独立测试，**When** 注入其对应断言的失败，**Then** 运行输出仍能定位到唯一 node id（文件、用例、参数行标识），且按该 node id 可直接定向重跑。
4. **Given** 漂移防护钉住类契约（技能节集合钉住、镜像同步检查、宪法双落地 watchlist、确认门 SHA 钉住等），**When** 瘦身改动合入，**Then** 这些测试仍在完整运行内且保持绿色（有意更新须记录理由），名称级失败清单能力保持不变。

### Edge Cases

- Part brief 缺失或没有目标测试命令：驱动者 MUST NOT 派发，先补 brief。
- Part 达到 turn 或 output-token 上限：按 U5 记录 budget-exhausted；同一预算不得原样重试。
- 用户豁免测试：verification 与 gate 记录豁免原文；review 必须看到该豁免，不得把 waived 当 pass。
- Part 依赖前一部分的产物：按 tasks.md 的 blockedBy 串行；无依赖的 part 可并行（宿主支持时），但共享状态脊字段需串行写入。
- 测量指标不可得：记 `not_evaluated`；不得用 0 或估算值替代。
- Part 切分后仍超过预算：继续按可验证结果切小，而不是升预算掩盖问题。
- 瘦身后一次完整运行仍 >600 秒：MUST 记录已采取措施与残余耗时的 dated 证据，按显式范围修订或 clarify 升级处理；MUST NOT 静默重定义「完整运行」、静默删除整层测试、跳过 contract / integration 层、伪造通过，或以长期默认 `-k` 子集达标。
- 以任何形式检出「为提速而少跑」（整层移除、默认过滤器、伪绿）：无论墙钟数字多好，一律判不达标。
- 并行执行引入相互污染（共享临时目录、端口、顺序依赖）：MUST 修复隔离后重测；MUST NOT 关闭并行却继续主张并行加速达标。
- 合并后的表驱动用例失败但无法定位到行：判失败定位退化，须恢复行级标识后重测。
- 新增测试依赖在当前开发环境缺失：MUST 显式降级为串行路径并记录，不得伪达标；降级运行不作为 ≤600 秒达标证据。
- 2026-10-22 后台全量基线日志未完成或不可信：以完成后的 dated 记录为准；MUST NOT 读取未完成日志充当通过证据。
- 为提速引入运行时依赖或联网依赖：禁止；检出即判不达标并回退该改动。

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

#### 框架测试套件瘦身（2026-10-22 范围扩展）

- **FR-011**: 「完整运行」的语义 MUST 保持为：以规范运行器 `scripts/bash/run-tests.sh` 执行、不带路径/测试过滤器、三层（contract 标记层、integration 标记层、未标记 unit 层）全部执行的运行。任何优化 MUST NOT 通过把某层移出完整运行、默认追加 `-k`/`-m` 过滤、或重定义「完整运行」来达标；测试分层/标记 MAY 新增诊断性标记（如 slow），但新增标记 MUST NOT 改变完整运行的构成。
- **FR-012**: 墙钟预算：瘦身后一次完整运行在开发主机（2026-10-22 基线口径，见现状锚点）上的墙钟 MUST ≤600 秒。测量 MUST 使用固定命令——运行器调用的端到端墙钟，含收集与夹具时间；证据（命令、主机、日期、退出码、分层计数、墙钟）MUST 落入本 spec 目录 `test-evidence/`；达标主张 MUST 出自该 dated 证据，MUST NOT 以估算、外推或部分运行替代。改动前基线 = 驱动者 2026-10-22 后台全量测量（完成后为 dated record）。
- **FR-013**: 运行器契约不变：规范运行器入口、`--names-out` 名称级失败清单、失败退出码语义 MUST 保持；063 的两槽位预算与名称级回归比较按原语义继续适用——本范围降低每次槽位的成本，不改变槽位语义。
- **FR-014**: 表驱动/参数化合并：矩阵型重复用例（逐条独立函数承载同一契约的行级组合）MUST 合并为表驱动/参数化用例；合并 MUST NOT 减少断言面（每行的断言组合保留），失败输出 MUST 携带行级标识使 node id 唯一可定位。
- **FR-015**: 删除/合并留证：每条被删除或被合并的测试 MUST 在留证台账（本 spec 目录 `test-evidence/test-consolidation-ledger.md`）登记：原测试 id、处置类型（删除/合并/保留）、指向的保留等价覆盖 id、等价依据。无台账条目而从完整运行中消失的测试 id 一律视为静默删除，收口审计判不通过。
- **FR-016**: fixture/工作区复用：逐用例重建的工作区准备（逐测试 copytree、逐测试子进程冷启动等）SHOULD 复用共享 fixture 或 session 级准备；复用 MUST NOT 改变用例的隔离语义与断言对象；因复用引入的相互影响 MUST 以显式隔离修复，不得以牺牲隔离换速度而不记录。
- **FR-017**: 并行或等价加速：MAY 引入并行执行（如 dev-only 的 pytest-xdist）或等价加速手段。采用时 MUST 满足：(a) 新依赖仅进开发侧依赖组，不得扩大 `specify-cli` 运行时依赖；(b) 受影响用例可并行隔离（共享临时目录/端口/顺序依赖 MUST 修复）；(c) 并行关闭时的串行路径仍可用并记录。未采用并行时，MUST 以其他等价手段（合并、复用、惰性准备等）达成预算。
- **FR-018**: 漂移防护不得削弱：现行钉住类契约测试（技能文档节集合钉住、镜像同步检查、宪法双落地 watchlist、确认门准则 SHA 钉住、fast-fail 契约等同类）MUST 全部保留在完整运行内且保持绿色；因本范围有意更新某钉住 MUST 记录理由；MUST NOT 以合并/删除为名移除钉住字面量或降低钉住强度。
- **FR-019**: 测试依赖边界：测试侧新增依赖 MUST 仅限开发侧依赖组，MUST NOT 进入 `specify-cli` 运行时依赖，MUST NOT 引入联网步骤或常驻服务；测试 MUST 在无网环境可运行。
- **FR-020**: 失败定位不退化：任何瘦身改动之后，失败输出 MUST 仍能定位到唯一测试 id；表驱动用例的失败 MUST 可归属到参数行；按 node id 的定向选择（`-k` 或直接 node id）MUST 继续可用。
- **FR-021**: 交付面：本范围的改动落在 `tests/`（用例、fixtures）、`scripts/bash/run-tests.sh`（如需）、`pyproject.toml`（仅开发侧依赖组）与本 spec 目录 `test-evidence/` 留证；MUST NOT 修改 `src/specify_cli` 运行时行为来迁就测试速度；驱动面（FR-010 owner 面）只做引用性更新。

### Key Entities *(include if requirement involves data)*

- **DispatchPart**: `part_id`、`task_ids[]`、`scope`、`turn_budget`、`status`、`commit`。
- **PartBrief**: 任务 ID、允许修改文件、目标测试命令/node id、预期红→绿、禁改文件、验收方式。
- **DispatchLog**: `part_id`、`turns`、`tests_passed`/`tests_failed` 增量、`commit`、`outcome`、`elapsed`/`token` 代理（不可得为 `not_evaluated`）。
- **ConsolidationLedger（测试处置台账，2026-10-22 范围扩展）**: 原测试 id、处置类型（删除/合并/保留）、保留等价覆盖 id、等价依据；一文一件追加式记录，收口审计的核对依据。
- **FullRunMeasurement（完整运行测量，2026-10-22 范围扩展）**: 命令、主机口径、日期、退出码、三层计数、墙钟秒数、证据指针；一次完整运行一条 dated 记录。

### Out of Scope

- 修改 063 的四项吞吐优化本身；本 spec 只补分段执行、测试经济学、测量与往返收敛。
- 新增常驻服务、守护进程、外部依赖或模型 API。
- 全局关闭测试门；测试豁免只能由用户显式声明，且必须留痕。
- 绕过 merge/push/删除/强推的确认门。
- （2026-10-22 范围扩展的排除项）把「完整运行」重定义为跳过任一层（contract / unit / integration）、默认子集或长期 `-k` 过滤；删除整层测试。
- 为提速引入运行时依赖、联网依赖、常驻服务或模型 API；测试在无网环境必须可运行。
- 建设 CI 测试工作流（现状无 CI；是否引入 CI 属独立决策，不在本 spec）。
- 修改 063 两槽位预算与名称级回归比较的语义；本范围只降低每次槽位的成本。
- 修改 `src/specify_cli` 运行时行为以迁就测试速度。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 对 065a 同规模的 30-task implement 夹具，采用本 spec 的分段策略后，预算耗尽子派发为 0，且完成派发数 ≤5（以 dispatch log 计；无可比数据时如实记 `not_evaluated`）。
- **SC-002**: 100% 的子派发都有 part brief 与 dispatch log 条目；驱动者能在不重读全部规格的情况下从 brief 恢复下一 part。
- **SC-003**: 每个 part 的测试红面有界且可归属；全量套件运行次数不超过 063 的两槽位预算。
- **SC-004**: 所有测试豁免在 verification 中可检索（`waived`/`not-run` + 豁免原文），全仓不存在把 waived 写成 pass 的产物。
- **SC-005**: 非破坏性 implement/test 连续段的驱动往返次数较 065a 现状下降（以用户确认次数/驱动轮次计；不可得时记 `not_evaluated`）。
- **SC-006**: 瘦身后，用固定测量命令在开发主机上执行一次完整运行，墙钟 ≤600 秒；证据按 FR-012 落 `test-evidence/`；以估算、子集运行或无证据支撑的达标主张数为 0。改动前基线 = 驱动者 2026-10-22 后台全量测量 dated 记录，仅作对照，不充当达标证据。
- **SC-007**: 完整运行构成不缩水：基线测试 id 清单中每条 id 在瘦身后要么保留、要么在留证台账中指向保留的等价覆盖；contract / unit / integration 三层在每次完整运行中全部执行；无台账条目而消失的测试 id 数为 0。
- **SC-008**: 漂移防护不下降：FR-018 所列钉住类契约测试在完整运行中 100% 保留且绿色（有意更新须有记录）；注入回归演练中名称级差集（`--names-out` 加 `comm -13` 或等价）100% 发现注入失败。
- **SC-009**: 失败定位：在合并后的表驱动用例中注入单行失败，运行输出 100% 定位到唯一 node id；按该 node id 直接定向重跑可复现该失败的比率为 100%（判据 = 注入演练 dated 记录）。
- **SC-010**: 依赖边界：`specify-cli` 运行时依赖集合相对改动前零扩大（判据 = `pyproject.toml` 运行时依赖 diff 为空）；测试侧新增依赖 100% 位于开发侧依赖组；测试代码新增网络调用数为 0（以检索判据）。

### Measurement Sources & Collection Methods

- 状态脊 dispatch log（part/task/turn/test/commit/outcome）。
- `notes/red-first-evidence.md` 与测试运行输出（pass/fail 增量）。
- git commit 哈希与 `git log`。
- token/耗时：run-determination/exec-quant 若不可得，记 `not_evaluated`；不得伪造。
- SC-006 Source：`test-evidence/` 下的完整运行测量 dated 记录（命令、主机、日期、退出码、分层计数、墙钟）加改动前基线 dated 记录对照。
- SC-007 Source：改动前测试 id 清单（基线运行产出或收集清单）、留证台账、瘦身后测试 id 清单三者的集合核对记录。
- SC-008 Source：钉住类契约测试清单核对加注入回归演练的名称级差集记录。
- SC-009 Source：表驱动用例单行失败注入演练的 dated 记录（失败输出节选加定向重跑结果）。
- SC-010 Source：`pyproject.toml` 运行时依赖段 diff、开发依赖组 diff、测试代码网络调用检索记录。

## Clarifications

### Session 2026-10-22

- Q: 新 spec 绑定哪个 Feature？ → A: 绑定 Feature 058（与 063 同一演化特性承载面），不新建 Feature、不改注册表计数；058 状态保持 Implemented。
- Q: 本 spec 是否立即走完整 SDD 链？ → A: 本次只完成 requirements 创建；后续 checklist/analyze/plan 按用户排期推进。
- Q: 065a 当前的 completed 是否受本 spec 影响？ → A: 不受；本 spec 是新需求，065a 继续按用户“忽略测试、尽快收口”的显式授权完成当前周期。

### Session 2026-10-22（P1 范围扩展：框架测试套件瘦身）

- Q: 本 spec 是否纳入「框架测试套件瘦身」范围？ → A: 纳入。用户 2026-10-22 指令原文逐字见文档头部 Input 字段；落为 User Story 5（P1）与 FR-011…FR-021、SC-006…SC-010。
- Q: 与 063 的测试经济学约束是什么关系？ → A: 正交叠加，不冲突：063 约束「完整运行何时跑」（两槽位、名称级差集、定向集规则）；本范围约束「每次完整运行多贵」（一次 ≤600 秒墙钟），两槽位语义原样保留。
- Q: 开放项（并行 dev-only 依赖、冷/热缓存口径、分层边界等）为何不定案？ → A: 按 part brief 要求列入 Assumptions，留待 clarify 裁决；本阶段不预设结论。
