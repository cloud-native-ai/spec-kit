# Requirements Specification: 状态感知（State Awareness）— Feature 065 / Slice 065a

**Requirement Branch**: `065-loop-interruption-recovery`  
**Slice**: `065a-state-awareness`  
**Created**: 2026-10-21  
**Status**: Draft  
**Input**: 父 Feature 065 的 `US1 + 快照引擎` 切片。父权威：`.specify/specs/065-loop-interruption-recovery/requirements.md`；分解门记录：`.specify/specs/065-loop-interruption-recovery/notes/decomposition-gate.md`。切片定义：一次只读调用聚合状态脊、Line Registry、四件套、watchbeat、阶段产物、git 提交与可用 watcher 判定，识别中断形态并给出唯一恢复动作建议；本切片不执行任何恢复副作用。

## Related Feature *(mandatory)*

**Feature ID**: 065  
**Feature Name**: SDD 循环中断感知与状态恢复（Loop Interruption Awareness & Recovery）  
**Slice**: `065a-state-awareness`（Feature 065 的切片，不新建 Feature ID，不新建独立 Feature 行）

绑定说明：Feature 065 已在 `2026-10-21` 由 `/speckit.clarify` 注册为 Draft（`.specify/memory/features.md` 索引行与 `.specify/memory/features/065.md` 详情文件）。本切片只复用该绑定，MUST NOT 新建 Feature、MUST NOT 改写注册状态或索引行。父特性 umbrella 的 `plan.md` / `research.md` / `data-model.md` / `contracts/` / `quickstart.md` / `feature-ref.md` 均为未提交证据，不是本切片的权威输入；本切片不修改、不提交它们。

## Slice Scope（分解边界）

本切片是 Feature 065 三切片计划的第一个切片。FR 编号沿用父 requirements 的编号空间；编号间隙是切片切分的显式结果，不是删除、合并或重排。

| 范围 | 父条目 | 本切片处理 |
|------|--------|------------|
| 核心 A 区 | 编号 001–012 | 全部纳入并定义（12 条） |
| 边界 D/E 区 | 编号 038–052 | 按适用性纳入 13 条；不适用 2 条显式记为 out-of-slice |
| 核心 B 区 | 编号 013–024 | 不在本切片；由 `065b-interruption-lifecycle` 承接（US2 + US4） |
| 核心 C 区 | 编号 025–037 | 不在本切片；由 `065c-recovery` 承接（US3） |

本切片 FR 定义总数 = 25（12 条核心 + 13 条边界），低于分解门上限 30。

### In-Slice Boundary FRs（13 条）

- 兼容、分发与测试（D 区）：编号 038、039、040、041、042、043、044、046、047。
- 边界与非目标（E 区）：编号 049、050、051、052。

### Out-of-Slice Boundary FRs（2 条，显式记录）

| 父条目 | 归属切片 | 不纳入本切片的理由 |
|--------|----------|--------------------|
| [D 区第 8 条「测试 MUST 至少覆盖 (a)–(i)」](../065-loop-interruption-recovery/requirements.md#requirements-mandatory)（编号 045） | `065c-recovery`（末切片汇总） | 该测试矩阵跨越三切片：条目 (g)、retry/stop/isolation 与四要素上送件依赖 065c 的变更动作，完整形态检测的 (f)(h)(i) 依赖 065b。065a 按本切片 FR-046 与 SC-006 覆盖自身新增检查，不声称覆盖整张矩阵。 |
| [D 区第 11 条「记录一文一件 + recover 独立原子锁」](../065-loop-interruption-recovery/requirements.md#requirements-mandatory)（编号 048） | `065c-recovery` | 065a 的快照是只读求值，不产生恢复记录、不持有 `recover --apply` 锁，也不执行并发写；记录拓扑与锁语义在 065c 落地。 |

## Assumptions（适用于 065a 的父裁决 + 切片裁决）

以下父 Assumptions 适用于本切片，保留父编号；括注说明切片落点。未列出的父 Assumptions（A-7、A-8、A-9、A-19）均以 `recover` 的变更动作、提交或并发写为前提，不在本切片适用，由 065c 承接。

- **A-1 入口形态**: 新建单一引擎 `loop-state.py`（Python 3 标准库）承载 `snapshot`（只读）、`recover`（默认 dry-run、`--apply` 才变更）与 `check-spine`（只读校验）三个动作，外加 `--self-test`。切片落点：065a 实现并验证 `snapshot` 与 `--self-test` 中属于快照的动作；`recover` / `check-spine` 的动作实现由 065b / 065c 承接，但共享的 CLI 信封与退出码阶梯在本切片冻结。
- **A-2 判定所有权**: watch 域判定仍由 `watch-target.sh` 唯一拥有。`loop-state.py` 只调用 `--once` 或消费调用方提供的 WATCH 快照，绝不重新实现信号优先级与退出码；`loop_state` 在存在活动 target 时逐字等于 watcher 判定。
- **A-3 两套词表分离**: `loop_state`（快照输出的聚合判定，大写）与 `spine_state`（状态脊文件状态，小写连字符）是两个词表，各自有 owner，不互相替代；快照显式报告二者及 `spine_consistent`。
- **A-4 第五信号 watchbeat**: 为检测「已派发但无 watcher」，新增由驱动者写入的 watchbeat 标记（`watchbeat-<line>-<stage>`），每窗口开始/返回各一次原子覆盖。它是驱动者存在证据，不是完成/存活信号，不参与任何 watch 判定；状态脊仍遵守「RUNNING 窗口不写」的既有规则。
- **A-5 动作集合**: 恢复动作取封闭集 `none / watch / verify / resume / retry / stop`。在 `resume / retry / stop` 之外增加 `watch`（继续监听，不重派）、`verify`（进入 U4 独立校验）、`none`（未派发或不适用），以避免把「活着但没人监听」「已完成待校验」误映射到 mutating 动作。
- **A-6 salvage 有界例外**: 产物齐备但无正向终止证据（无哨兵、非 `exit=0`）时，`resume` 必须由驱动者显式记录 `salvage` 判定（依据 = 产物清单 + 无 `ANOMALY:` 行 + U4 产物/纪律核验）才允许提交；未记录时一律 `retry`。切片落点：065a 只在快照的 `recovery_action` 中反映该门，不执行提交；salvage 记录的写入与提交由 065c 承接。
- **A-10 停线不杀进程**: `stop` 只写 `stalled` 与四要素上送件，不 kill、不删 worktree；活进程的 TIMEOUT 停线必须先做最终 `--once` 快照并经用户显式决定。切片落点：065a 只输出 `stop` 建议与理由，不执行。
- **A-11 状态脊机读段**: 状态脊增加固定 fencing 内的 `key: value` 机读段；散文部分不变。legacy 状态脊（无可读段）降级求值，缺字段记 `unknown`，不猜测、不补默认值。
- **A-12 产物映射 owner**: 阶段→产物映射由脚本内数据 + 对应 reference 章节唯一定义，并与 U4 的产物核验清单对齐；plan 阶段使用 `efficiency-model.md` §3 的 plan-owned 集合；analyze 无提交要求，clarify 允许无变更。
- **A-13 远端拓扑**: 聚合器在证据所在主机以同一执行身份运行，或消费调用方经 ssh 采集的 probe 快照；ssh 不可达记 `stalled(remote-unreachable)`，绝不记 `DEAD`。
- **A-14 未派发语义**: 尚未派发的线不在本特性判定范围内；快照以 `UNKNOWN` + `reason=not-dispatched` 表达，恢复动作为 `none`。
- **A-15 Feature 绑定**: 入口已声明特性 ID 065；`2026-10-21` `/speckit.clarify` 已新建并绑定 Feature 065（Draft），注册行与 `.specify/memory/features/065.md` 同批落盘；不另开新 ID。切片复用该绑定，不新增注册行。
- **A-16 derived 映射**: 无活动 watcher 时，`loop_state` 由独立、固定优先级的聚合映射表导出，始终标注 `verdict_source=derived`；它不是 watcher 判定状态机的复制，不得声称具有 watcher 判定的语义或退出码。映射与状态脊 `last_verdict` 冲突时只报 `spine_consistent=false`，不静默择一。
- **A-17 引擎 CLI 契约**: 三个动作共享同一 JSON 信封（含 `schema_version`）与退出码阶梯 `0/1/2`；`recover` 仅在 `resume/retry/stop` 且 `--apply` 时写状态脊恢复记录，`watch` 只刷新 watchbeat，`verify/none` 不写任何状态；远端 probe 快照经 `--probe <file>` 输入。切片落点：065a 冻结并验证 `snapshot` 的信封、退出码与 `--probe` 路径；其余动作在后续切片实现。
- **A-18 状态脊机读段**: 使用独立 fence `<!-- loop-state:begin -->` … `<!-- loop-state:end -->` 与 `spine_schema: v1`；状态键使用 `spine_state:` 前缀，MUST NOT 使用裸 `state:` 键，以避免改变 `line-registry.py` 对首个 `state[:=]` 行的既有读取；状态枚举扩展为 `running / retrying / stalled / reentry-required / done`。切片落点：065a 只读解析并报告 schema，不写状态脊。

切片裁决（写入本切片 Assumptions；`/speckit.clarify` 可推翻）：

- **SA-1 动作建议与执行分离**: 065a 输出 `recovery_action` 与 `interruptions[]`，其封闭动作集与裁决优先级沿用父 requirements C 区的确定性规则；那些规则在本切片只作只读求值，MUST NOT 触发提交、隔离、重派、停线或任何写操作。执行、salvage 记录与四要素上送件归 065c。
- **SA-2 编号空间**: 切片保留父 FR 编号（核心 001–012，边界按父编号），因此 `validate-requirements.py` 的 `id-contiguous` 单项不适用于本切片；该检查器的其余单项（doc-order、dup-id、ref-resolvable、marker-count）仍应通过，结构一致性以 `pre-analyze-check.py` 为准。此裁决不构成对父 FR 的删除、合并或重排。
- **SA-3 跨切片证据**: `stale_signals`、legacy 状态脊与 `remote-unreachable` 的细分检测谓词由 065b 拥有；065a 只保证输出字段、封闭形态集合与 `missing` / `unknown` 语义，不重新定义检测阈值或 watcher 数值。
- **SA-4 只读边界**: 065a 的所有执行路径 MUST NOT 写状态脊、写四件套、移动/删除证据、提交或杀进程；显式 `--out` 持久化是唯一例外，且不得写入状态目录或工作树。
- **SA-5 未提交证据不权威**: umbrella 草稿 plan/research/data-model/contracts/quickstart/feature-ref 不作为本切片的权威输入，也不因其存在而放宽本切片的 FR 范围。

## User Scenarios & Testing *(mandatory)*

### User Story 1 - 一次调用看清一条线的真实状态 (Priority: P1)

使用者或新接手的驱动会话面对一条可能中断的线，不再逐一检查 pid/status/log/heartbeat/产物与 git 提交。只需按线调用一个确定性入口，即可得到：当前阶段与断点、状态脊状态、四件套证据、产物与提交完整性、watcher 最近判定、识别出的中断形态，以及唯一建议的下一步动作。所有缺失信号显式标为 `missing`/`unknown`，不猜测。

**Why this priority**: 这是「状态感知」的最小可用价值，也是恢复与生命周期治理的共同前提；实测事故中恢复耗时几乎全部花在人工拼装这些证据上。

**Independent Test**: 用夹具构造一条「产物齐备、未提交、`exit=1`、无哨兵、无 watcher」的线，调用快照入口，核对输出字段、证据指针与建议动作；再构造一条正常运行中的线与一条未派发的线，核对三者的 `loop_state` 与 `verdict_source` 差异。

**Acceptance Scenarios**:

1. **Given** 一条线的状态脊与四件套可读、watcher 可调用，**When** 执行一次快照，**Then** 输出包含阶段、`loop_state`、`verdict_source`、`watch_verdict`、产物/提交清单、`interruptions[]` 与唯一 `recovery_action`，且所有路径可定位。
2. **Given** 阶段运行中且刚完成一个监听窗口，**When** 执行快照，**Then** `loop_state=RUNNING`、`verdict_source=watcher`，且不报 `unwatched`。
3. **Given** 阶段运行中但驱动者从未启动 watcher（无 watchbeat），**When** 执行快照，**Then** 报 `unwatched` 中断并建议 `watch`，不提交、不重派。
4. **Given** 阶段产物齐备但无哨兵且未提交，**When** 执行快照，**Then** 报 `artifacts-without-completion`，不得判 `DONE`，建议动作遵循 salvage 门。
5. **Given** 任一信号缺失，**When** 执行快照，**Then** 该信号以 `missing`/`unknown` 出现，输出中不出现零值或 `ok` 猜测。

---

### User Story 2 - 既有语义与分发面不回归 (Priority: P2)

使用者在升级后，现有 watcher 判定、四件套格式、Line Registry、阶段命令、确认门与 fast-fail 纪律保持原样；新增能力仅以增量层出现。框架源、运行时镜像、文档与测试保持一致，没有新增常驻服务或外部依赖。

**Why this priority**: 该特性改善的是「出事后的恢复」，若以改变判定语义或引入新运行时为代价，风险大于收益。分解门记录要求 US5 兼容性验收在每个切片运行；本切片以 P2 承接该验收。

**Independent Test**: 运行既有 watcher `--self-test`、驱动技能契约测试、Registry 引擎测试与镜像一致性检查；对比升级前后的判定输出与退出码。

**Acceptance Scenarios**:

1. **Given** 既有 `watch-target.sh --self-test`，**When** 升级后运行，**Then** 全部用例保持绿色，判定与退出码零差异。
2. **Given** 既有四件套与 Registry 条目，**When** 升级后读取，**Then** 字段语义与 action 行为不变，旧条目可读。
3. **Given** 框架源改动，**When** 运行镜像同步与一致性检查，**Then** 运行时镜像字节一致，漂移为 0。
4. **Given** 既有 `/speckit.*` 命令与阶段提示词，**When** 升级后运行，**Then** 三段骨架、哨兵字面量、确认门与 no-push 策略不变。

### Edge Cases

以下仅列适用于 065a 只读快照的边界；涉及 `resume / retry / stop` 执行、隔离、锁与 worktree 的边界由 065c 承接。

- 驱动者派发后在**同一回合**启动 watcher，但 watcher 第一次调用即超时：watchbeat 存在且新鲜，不得报 `unwatched`；按调用失败处理，重入新窗口。
- 监听窗口正常到期（`RUNNING`）与「无 watcher」同时看似成立：以 watchbeat 是否新鲜区分；新鲜 = 正常窗口，不报中断。
- 阶段已写出哨兵但进程仍活：snapshot `loop_state=DONE`，动作 `verify`，不因进程存活改判。
- 哨兵在而产物缺：伪完成，动作建议 `retry`，不得建议 `resume`。
- 产物齐备、无哨兵、但日志最后一行是 `ANOMALY:`：不满足 salvage 前提，动作建议 `retry`。
- 产物齐备、无哨兵、`exit=1`、无异常行：salvage 候选；未记录独立校验前动作仍为 `retry`。
- 旧 status 的 `run_id` 与当前一致但 mtime 早于 `stage_started_at`：按 stale 处理并列入 `stale_signals`。
- 旧 status 无信封且无法判断归属：按可疑处理并列入 `stale_signals`，记录 `legacy-stale` 原因。
- `pid` 文件指向已复用 PID：start ticks 不符，判 `DEAD`/身份不符，不附着。
- deadline 已过、pid 活、心跳新鲜、且 status 尚未出现：建议 `watch` 并延长观察；只有用户显式决定才 `stop`。
- deadline 已过、pid 死、无 status：最终快照后按父 C 区规则给出 `retry` 或 `stop` 建议（执行由 065c 承接）。
- 状态脊是 legacy 格式（无机读段）：降级求值，缺失字段为 `unknown`；不得据默认值建议 `resume`。
- Registry 条目缺失但状态脊与四件套可读：继续求值并记 `registry=missing`；不得因此判 `UNKNOWN`。
- Registry 条目存在但状态脊缺失：`UNKNOWN` + `stop` 建议，上送证据缺口；不得凭 Registry 单独猜阶段。
- 远端 ssh 不可达：`stalled(remote-unreachable)`，重试连通性；不得判 `DEAD`，不得重派。
- 同一次派发内出现多个中断形态（如 `unwatched` + `stale-signal`）：全部列出，动作按父 C 区优先级裁决，不以一条掩盖另一条。
- 快照运行期间 watcher 恰好结束：以 `--once` 的当次输出为准；不得混用两次调用的证据。
- 状态脊与快照同时写入：快照只读，不竞争；恢复写脊遵循单写者与原子替换（写侧由 065c 承接）。

## Requirements *(mandatory)*

### Functional Requirements

#### A. 状态感知（State Awareness）

- **FR-001**: 驱动技能 MUST 提供一个确定性、只读的状态聚合入口 [[STR-001]]（Python 3 标准库、零外部依赖），一次调用聚合状态脊、Line Registry 条目、pid/status/log/heartbeat 四件套、watchbeat 标记、阶段产物、git 提交与可用的 watcher 判定；快照动作 MUST NOT 写文件、改状态、杀进程或修改工作树（显式 `--out` 持久化除外）。
- **FR-002**: 入口的输入解析顺序 MUST 为：显式 `--spine`/`--state-dir`/`--spec-dir`/`--repo`/`--probe` 覆盖 → 按 `--line-id` 读取 Registry 条目 → 失败。`--probe <file>` 是调用方经 ssh 采集的只读 WATCH/probe JSON 快照；显式提供时以它为准并在输出标注 `evidence_source=probe`。Registry 缺失但状态脊与四件套可解析时 MUST 继续求值并记 `registry=missing`；任何必需输入缺失 MUST 显式记为 `missing`，MUST NOT 以零值或猜测填充。
- **FR-003**: 快照输出 MUST 为机器可读 JSON，至少含：`schema_version`（初始值 `1`）、`line_id`、`run_id`、`stage`、`loop_state`、`verdict_source`、`watch_verdict`、`recovery_action`、`spine`（path/state/schema/consistent）、`evidence`（pid/status/log/heartbeat/watchbeat/artifacts/commits，含 `evidence_source=local|probe`）、`interruptions`、`missing_artifacts`、`uncommitted_artifacts`、`stale_signals`、`evaluated_at`；每个信号 MUST 标注 `present|missing|na` 及证据指针。`recover` 输出 MUST 复用同一 `schema_version` 信封，并至少含 `action`、`applied`（bool）、`result`（`dry-run|applied|already-applied|locked|refused|failed`）、`steps[]`、`reason`；增量字段只允许追加，旧读取方 MUST 可忽略未知字段。
- **FR-004**: `loop_state` MUST 取自封闭集 `RUNNING / DONE / INCOMPLETE / ANOMALY / FAILED / DEAD / TIMEOUT / NO_SIGNAL / STALLED / REENTRY_REQUIRED / UNKNOWN`。存在活动 watch target 时，`loop_state` MUST 与 watcher 判定逐字一致且 `verdict_source=watcher`，聚合器 MUST NOT 改写、降级或升级该判定。无 watch target 时以 `verdict_source=derived` 按下列固定优先级推导，且 MUST NOT 复制或声称 watcher 判定：(1) 状态脊 `spine_state=stalled` → `STALLED`，[[STR-004]] → `REENTRY_REQUIRED`；(2) 若（退出记录存在或进程已死）且日志最后非空行以 `ANOMALY:` 开头 → `ANOMALY`，否则退出记录 `exit≠0` → `FAILED`，否则退出记录 `exit=0` 且哨兵存在且产物齐备 → `DONE`，否则退出记录 `exit=0` 且（哨兵缺失或产物缺）→ `INCOMPLETE`；(3) 无退出记录但哨兵存在：产物齐备 → `DONE`，产物缺 → `INCOMPLETE`；(4) 无退出记录、pid 记录存在且进程已死/start ticks 不符 → `DEAD`；(5) 有 `stage_deadline_epoch` 且 now ≥ deadline + deadline grace 且无终态 → `TIMEOUT`（活进程也判 `TIMEOUT`，处置仍按父 requirements B 区第 3 条「deadline 已过而进程仍存活」的继续观察规则，该条由 065b 承接）；(6) pid 记录与退出记录均缺失且超过启动宽限期 → `NO_SIGNAL`；(7) pid 存活或心跳新鲜且未命中上述终态 → `RUNNING`；(8) 其余 → `UNKNOWN`。启动宽限期、deadline grace 与心跳新鲜度均由 watcher 参数/标记 owner 定义（`scripts/watch-target.sh`；本规格不复述数值）。derived 映射的证据谓词与 watcher 同名判定保持一致，但它是独立的聚合映射，不产生 watcher 的退出码；与状态脊 `last_verdict` 冲突时 MUST 报 `spine_consistent=false`，不得静默择一。映射表由 FR-043 的唯一 owner 文档定义，代码与测试引用它。
- **FR-005**: 监听域判定 MUST 经既有 `watch-target.sh --once`（与 runner 同一执行身份）取得，或消费调用方提供的 WATCH 快照；聚合器 MUST NOT 重新定义或声称 watcher 的判定状态机、信号优先级或退出码。watcher 不可用（ssh 255、宿主工具超时、脚本缺失）时 MUST 记为 `watch=unavailable`，并且只能走 FR-004 的 derived 映射（标注 `verdict_source=derived`），MUST NOT 判为阶段失败、`DEAD` 或伪造 watcher 判定。
- **FR-006**: 阶段产物映射 MUST 由单一 owner（脚本内数据 + 对应 reference 章节）定义，覆盖 `requirements / clarify / plan / tasks / checklist / analyze / implement / review`，每阶段显式标注 `commit_required` 与 `no_change_allowed`；映射 MUST 至少覆盖 U4 的产物核验清单（owner：`references/stage-prompts.md` § Independent Verification），plan 阶段另须覆盖其 plan-owned 设计件集合（owner：`references/efficiency-model.md` §3），analyze `commit_required=false`，clarify `no_change_allowed=true`。
- **FR-007**: 产物完整性 MUST 只由「文件存在且非空」判定，MUST NOT 从日志文本推断；哨兵仍是唯一的完成声明；「哨兵在而产物缺」MUST 判为伪完成（`INCOMPLETE` 语义），MUST NOT 因产物部分存在而判 `DONE`。
- **FR-008**: 提交证据 MUST 以状态脊的 `stage_base_commit` 为基线，检查基线之后是否有提交触及该阶段产物路径（implement 为代码/测试提交）；基线缺失时 MUST 记 `commit=unknown`，MUST NOT 回退猜测「最近一次提交」；`commit_required=false` 的阶段记 `not-applicable`。
- **FR-009**: 中断形态 MUST 取自封闭集 `unwatched / dead-no-exit-record / deadline-overrun-live / heartbeat-stalled / artifacts-without-completion / stale-signal / lifecycle-spine-violation / remote-unreachable`；每个条目 MUST 携带证据指针与一句事实描述，MUST NOT 用一个形态掩盖另一个不同根因。
- **FR-010**: 驱动者 MUST 在每个 U3 监听窗口开始时原子写/覆盖 watchbeat 标记 [[STR-002]]`<line>-<stage>`（至少含 `run=<run_id> stage=<stage> window=<seconds> at=<epoch> event=watch-window`），窗口返回时刷新 `event=watch-return`；该标记只证明驱动者存在，MUST NOT 参与任何完成/存活判定；`watch-model.md` §5「RUNNING 窗口不写状态脊」保持不变。
- **FR-011**: 阶段仍在运行（pid 存活或心跳新鲜）而 watchbeat 标记缺失，或标记年龄超过其自身 `window=` 字段 + watcher `--deadline-grace` 缺省值（owner：`scripts/watch-target.sh`；本规格不复述数值）时，快照 MUST 报 [[STR-003]] 中断；其恢复方向 MUST 为重新监听，MUST NOT 触发提交、重派或终止。
- **FR-012**: 引擎 MUST 使用统一退出码阶梯：`0` = 求值或应用成功（`snapshot`、`recover` dry-run、`recover --apply` 成功或 `already-applied`、`check-spine` 通过；`recover` 的 `action=stop` 是成功求值，仍为 0）；`1` = 拒绝或校验失败（`check-spine` 违规、`recover --apply` 因路径冲突/未合并变更/非本阶段文件/并发锁被拒绝、或应用过程中失败）；`2` = 参数错误或必需输入不可读。任何 `loop_state` 都是数据，不得编码为退出码；MUST NOT 复用或重定义 watcher 的判定退出码（10–16）。阶梯 MUST 在 `--help` 与 `--self-test` 中钉住。`--self-test` MUST 覆盖 FR-009 全部中断形态，以及旧信号污染、产物齐备无哨兵、进程死无退出记录、哨兵在产物缺、TIMEOUT 活进程、legacy 状态脊、不可达证据、并发锁与拒绝路径。

#### D/E. 兼容、分发与非目标（适用于 065a 的边界）

- **FR-038**: `watch-target.sh` 的判定状态机、信号优先级、退出码与 `--self-test` 用例 MUST 保持不变；新增标记与聚合 MUST NOT 改变任何既有判定。
- **FR-039**: 四件套文件格式与 `line-registry.py` 的既有 action/字段 MUST 保持兼容；若需增量字段，只允许追加并保证旧条目可读；本特性 MUST NOT 改变 Registry、lease、reservation 或 ownership 语义（owner：Feature 064）。
- **FR-040**: 各 `/speckit.*` 命令内部流程、阶段提示词三段骨架、哨兵字面量、确认门与 fast-fail 纪律 MUST 保持不变；本特性只改驱动技能及其测试与文档。
- **FR-041**: 本特性 MUST NOT 引入常驻服务/daemon、外部服务或新的运行时依赖；实现 MUST 复用既有 shell/Python 标准库、watcher、Registry 与 feedback/probe 机制。
- **FR-042**: 两顶帽子：改动 MUST 落在框架源 `skills/external/sdd-loop-driver/`；`.specify/skills/sdd-loop-driver/` 为生成镜像，MUST NOT 手改；镜像 MUST 经 `sync-mirrors.py` 再生成并通过镜像一致性检查；打包随既有 hatch 构建流程，无手工步骤。
- **FR-043**: 状态感知/中断/恢复规则 MUST 在技能内有一个唯一 owner 文档（references 下的专门文件或章节），SKILL.md 与各 references MUST 引用而非复述判定表；`references/watch-model.md` 仍是 watch 判定的唯一 owner，本特性 MUST NOT 在其中复制状态恢复规则或改变其语义。
- **FR-044**: 文档 MUST 更新：SKILL.md（Hard Requirements 与 References）、owner reference（状态感知、判定表、恢复动作、watchbeat）、`docs/reference/skills/sdd-loop-driver.md`（入口、调用形态、与 watcher/Registry 的关系）；文档取值 MUST 与代码一致。
- **FR-046**: 测试 MUST 含变异演练：移除「无 watcher 检测」「旧信号隔离」「salvage 门」任一行为时，至少一条测试 MUST 转红；全部新检查 MUST 有逆样本，MUST NOT 出现只在通过路径上运行的绿。
- **FR-047**: 单线与多线 MUST 同构：快照按线独立求值，不引入跨线推断；多线调用 MAY 由调用方逐线循环，本特性 MUST NOT 新增 manifest 或批量判定语义。
- **FR-049**: 任何流程 MUST NOT 自动 push、自动合并、删除分支或改写远端历史；恢复程序的提交仅为本地阶段提交。
- **FR-050**: 任何流程 MUST NOT 自动 kill 进程、删除日志/信号/worktree 或静默修复证据缺口；清理只能是显式动作，隔离只能是移动。
- **FR-051**: 本特性 MUST NOT 改变「完成需正证据」原则：哨兵/退出记录仍是完成的正证据，产物齐备只是 U4 证据；唯一有界例外是父 requirements C 区第 4 条的显式 `salvage` 判定（out-of-slice，由 065c 承接），且必须可见与可审计。
- **FR-052**: 本特性 MUST NOT 替代 058 的 U4 独立校验、U5 卡死处置或 064 的 Registry/lease/ownership；它只提供观测与恢复建议，最终去向由驱动者按既有程序裁决。

### Parent FR Mapping

每条切片 FR 与父 requirements 的对应关系如下。父引用统一使用 `#FR-NNN` 形式；切片自身定义保留 `- **FR-NNN**:` 形式。除表中注明的切片调整外，正文逐字沿用父 FR。

| 切片 FR | 父引用 | 切片处理 |
|---------|--------|----------|
| FR-001 | [#FR-001](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-002 | [#FR-002](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-003 | [#FR-003](../065-loop-interruption-recovery/requirements.md) | 逐字沿用；`recover` 信封作为共享接口冻结，动作实现归 065c |
| FR-004 | [#FR-004](../065-loop-interruption-recovery/requirements.md) | 跨切片引用由[父 B 区第 3 条](../065-loop-interruption-recovery/requirements.md#requirements-mandatory)的文字指针替代（原 FR 引用会超出本切片编号空间） |
| FR-005 | [#FR-005](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-006 | [#FR-006](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-007 | [#FR-007](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-008 | [#FR-008](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-009 | [#FR-009](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-010 | [#FR-010](../065-loop-interruption-recovery/requirements.md) | 逐字沿用；标记写入属驱动者行为，快照只读消费 |
| FR-011 | [#FR-011](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-012 | [#FR-012](../065-loop-interruption-recovery/requirements.md) | 逐字沿用；`--self-test` 在 065a 覆盖快照与已实现动作，并发锁/拒绝路径由 065c 追加 |
| FR-038 | [#FR-038](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-039 | [#FR-039](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-040 | [#FR-040](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-041 | [#FR-041](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-042 | [#FR-042](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-043 | [#FR-043](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-044 | [#FR-044](../065-loop-interruption-recovery/requirements.md) | 065a 落地状态感知/入口文档；恢复动作与 watchbeat 章节由 065b/065c 在同一 FR 下补齐 |
| FR-046 | [#FR-046](../065-loop-interruption-recovery/requirements.md) | 065a 对「无 watcher 检测」执行变异演练，并覆盖本切片全部新增检查的逆样本；「旧信号隔离」「salvage 门」的变异演练由 065c 承接 |
| FR-047 | [#FR-047](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-049 | [#FR-049](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-050 | [#FR-050](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |
| FR-051 | [#FR-051](../065-loop-interruption-recovery/requirements.md) | 跨切片引用由[父 C 区第 4 条](../065-loop-interruption-recovery/requirements.md#requirements-mandatory)的文字指针替代（原 FR 引用会超出本切片编号空间） |
| FR-052 | [#FR-052](../065-loop-interruption-recovery/requirements.md) | 逐字沿用 |

### Key Entities *(include if requirement involves data)*

- **Loop State Snapshot（循环状态快照）**: 一次只读求值的结构化结果，聚合状态脊、Registry、四件套、watchbeat、产物、提交与 watcher 判定；含 `loop_state`、`verdict_source`、中断清单、缺失/未提交产物与唯一恢复动作建议。它是观测记录，不是新的状态 owner。
- **Interruption Finding（中断条目）**: 封闭形态之一 + 证据指针 + 一句话事实；可多条并存，动作裁决按优先级消费全部条目，不以一条掩盖另一条。
- **Recovery Decision（恢复裁决）**: `loop_state` + 产物完整性 + 中断形态 + 已试次数映射到唯一动作建议（`none/watch/verify/resume/retry/stop`）；同一输入可复现。065a 只求值，不执行。
- **Watchbeat Marker（驱动者监听标记）**: `watchbeat-<line>-<stage>` 单行原子覆盖文件；只证明驱动者存在，不参与判定。
- **Stage Artifact Map（阶段产物映射）**: 阶段→产物路径/提交要求/允许无变更的唯一映射；与 U4 产物清单对齐。
- **State Spine（状态脊，既有）**: 每线一份的恢复状态文件（owner：058 的 `stage-prompts.md`）；本切片增加读取与一致性报告，不改变其状态词表与写入时点。
- **Watcher Verdict（监听判定，既有）**: 由 `watch-target.sh` 代码侧精确拥有；本切片只消费，不重定义。
- **Line Registry（线路登记册，既有）**: 环境级登记集合（owner：064）；本切片只读消费。

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 实测事故回放夹具（产物齐备未提交、`exit=1`、无哨兵、无 watcher）中，快照在单次调用内识别出至少一个中断形态并给出 `resume` 或 `retry` 建议，人工逐文件检查次数为 0。
- **SC-002**: 同一输入两次快照除 `evaluated_at` 外差异数为 0；任一缺失信号在输出中以 `missing`/`unknown` 出现，零值或 `ok` 猜测次数为 0。
- **SC-003**: 正常监听窗口被误报为 `unwatched` 的次数为 0；进程已死且无退出记录被误判为 `DONE` 的次数为 0；活进程被建议立即终止的次数为 0。
- **SC-004**: 既有 `watch-target.sh --self-test` 通过率为 100%，判定与退出码差异数为 0；四件套与 Registry 兼容读取测试保持绿色。
- **SC-005**: 源与镜像字节一致率为 100%，镜像漂移数为 0；文档入口已更新；新增 daemon/外部依赖数为 0。
- **SC-006**: 本切片新增检查的逆样本覆盖率为 100%；移除「无 watcher 检测」行为时至少 1 条测试转红。

### Measurement Sources & Collection Methods

- **SC-001 / SC-002 Source**: `tests/unit/` 与 `tests/contract/` 下的快照夹具（构造状态脊、四件套、watchbeat、产物与 git 历史）；逐条断言 `interruptions[]`、`loop_state`、`recovery_action` 与字段存在性；事故回放夹具直接使用父 requirements「现状锚点」的事实形态。相同夹具两次运行 diff（剔除 `evaluated_at`）。
- **SC-003 Source**: 正常窗口、进程死无退出记录、TIMEOUT 活进程三组夹具的断言计数；建议动作断言不得出现 kill/terminate 语义。
- **SC-004 Source**: 既有 `watch-target.sh --self-test` 输出、驱动技能契约测试（`tests/contract/test_sdd_loop_driver_skill.py`）与 `line-registry` 引擎测试。
- **SC-005 Source**: `sync-mirrors.py --check --only skills/external/sdd-loop-driver`、`docs/reference/skills/sdd-loop-driver.md` 存在性与内容断言、依赖清单比对。
- **SC-006 Source**: 变异演练记录：移除「无 watcher 检测」行为并运行测试，记录转红用例；逆样本清单由测试文件枚举。
- 所有度量都从测试或运行产生的制品读取，不手填；无法测量的量显式记为未评估。

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "loop-state.py" | FR-001 |
| `STR-002` | "watchbeat-" | FR-010 |
| `STR-003` | "unwatched" | FR-011 |
| `STR-004` | "reentry-required" | FR-004 |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal.

## Clarifications

### Session 2026-10-21 — requirements（无人值守切片）

> 本阶段为无人值守运行，未向用户发起访谈；以下裁决按父 requirements、分解门记录与入口指令自行作出，已同步落入 Assumptions 与相应 FR。`/speckit.clarify` 可推翻。

- Q: 切片 FR 是否重新连续编号？ → A: 不重排。核心沿用父编号 001–012，边界沿用父编号；编号间隙是切片的显式切分结果，不是删除/合并/重排。结构一致性以 `pre-analyze-check.py` 判定；`validate-requirements.py` 的 `id-contiguous` 单项因父编号保留而不适用。
- Q: 哪些 D/E 边界 FR 适用于 065a？ → A: 纳入编号 038–044、046、047、049–052；编号 045（跨切片测试矩阵）与 048（记录拓扑 + recover 锁）显式记为 out-of-slice，分别由 065c 汇总/承接。
- Q: 快照的 `recovery_action` 在 065c 之前如何定义？ → A: 065a 只做只读求值并输出动作建议，封闭动作集与优先级沿用父 requirements C 区规则；不执行提交、隔离、重派、停线或任何写操作。执行与 salvage 记录归 065c。
- Q: 父 FR-004 与 FR-051 引用了本切片外的 FR，如何处理？ → A: 改为父 requirements B 区第 3 条 / C 区第 4 条的文字指针，避免切片内悬空引用；不删除、不合并、不重排父 FR。
- Q: US5 兼容性验收是否进入本切片？ → A: 进入。分解门记录要求每个切片运行 US5 兼容性验收；本切片以 P2 保留其四条验收场景，并由 FR-038–FR-044、FR-049–FR-052 承接。
- Q: Feature 如何绑定？ → A: 复用既有 Feature 065（Draft），不新建 Feature ID、不新增注册行、不改变状态；切片目录只承载本切片的 requirements 与 checklist。
