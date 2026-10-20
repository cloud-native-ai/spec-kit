# Data Model — Feature 064

**Feature**: 064 Subagent 并发归属、CLI 能力档案与生命周期解耦
**Date**: 2026-10-20
**Scope**: 本文件拥有 064 引入的实体字段、状态词表与校验规则。既有实体（状态脊、watcher 判定、`CAPABILITY_MATRIX`、feedback/exec-quant 记录）由各自 owner 拥有，本文件只声明 064 追加的字段与其约束。

约定：`MUST` 规则编号 `V-<实体>-<n>` 被 `contracts/` 引用；时间为 ISO-8601 UTC（`YYYY-MM-DDTHH:MM:SSZ`）；路径在写入 Registry 前归一化为绝对路径。

---

## E1. Line Registry Entry（线路登记条目）

**存储**: `$SPECIFY_LINE_REGISTRY_DIR/<line_id>.json`（目录缺省见 R1）；同线锁 `<line_id>.lock`；Manifest 在 `$SPECIFY_LINE_REGISTRY_DIR/manifests/<line_id>.json`；reservation 在 `$SPECIFY_LINE_REGISTRY_DIR/reservations/<line_id>.<stage>.json`；lease 在 `$SPECIFY_LINE_REGISTRY_DIR/<line_id>.driver.lock`。

**Fields**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `schema_version` | int | always | 当前 `1` |
| `line_id` | string | always | 环境内唯一、不复用；格式 `^[a-z0-9][A-Za-z0-9-]{7,63}$`，生成规则 `<project-slug>-<YYYYMMDDTHHMMSSZ>-<4hex>` |
| `run_id` | string | always | 一次执行尝试；格式 `^r[0-9]{8}T[0-9]{6}Z-[0-9a-f]{4}$`；reattach 复用，重试换新 |
| `project_dir` | abs path | always | 目标项目根（含 `.specify/`） |
| `repo_root` | abs path | always | git 仓库根 |
| `worktree_path` | abs path | write lines | 独立 worktree；只读线可为 `null` 或独立只读视图 |
| `branch` | string | write lines | `line/<line_id>`；只读线记录其观察分支 |
| `base_sha` | string | write lines | 创建 worktree 时的 trunk 提交 |
| `driver_session` | string | always | 驱动侧会话标识（宿主提供；不可为空串） |
| `cli` | string | always | 子代理 CLI 名（如 `qodercli`） |
| `runner_pid` / `runner_start_token` | int/string | after dispatch | 成对出现；`start_token` 见 V-LR-7 |
| `cli_pid` / `cli_start_token` | int/string | after dispatch | CLI 子进程；requirements 的 `qodercli_pid` 是其在 `cli=qodercli` 时的同一值（Decision D-02） |
| `prompt_path` / `status_path` / `log_path` / `heartbeat_path` | abs path | after dispatch | 四件套 + 提示词 |
| `meta_paths` | object | after dispatch | `{prompt, log}` → 旁路信封文件路径 |
| `owned_paths` | string[] | write lines | Ownership Manifest 的投影（可再生） |
| `ownership_manifest_path` | abs path | write lines | Manifest owner 指针 |
| `stage` | string\|null | active | 当前阶段（`requirements`…`review`）；`waiting` 可为 null |
| `state` | enum | always | 见 V-LR-4 |
| `waiting_reason` / `holder_line_id` / `queued_at` | string/null | waiting | 串行化票据 |
| `merge_ready` / `ready_for_merge_at` | bool/ISO | integration | 集成队列输入；仅当 `state=completed` 时为 true，`integration-record` 后置 false；不进入 `state` 封闭集 |
| `integration_result` | object\|null | after integration | `{status: merged\|failed\|skipped, at, commit, reason}`；记录时 `state` 保持 `completed`，直到 U6 关闭 |
| `worktree_retained` | bool | U6 | 未合并/未提交时 `true` |
| `resources` | object\|null | active | `{ports:[start,end], cache_dir, tmp_dir}` |
| `remote` | object\|null | remote only | `{alias, run_user, remote_root}`；Registry 仍在驱动侧 |
| `last_event` | string | always | 最近一次状态事件（如 `u2-dispatch`） |
| `created_at` / `updated_at` / `closed_at` | ISO | always/always/U6 | `closed_at` 仅 closed |
| `lease` | object\|null | always (nullable) | `{holder_session, holder_pid, holder_start_token, acquired_at, heartbeat_at, ttl_seconds}` 的只读投影（真源为 lease 文件）；无 lease 时为 `null` |

**Validation rules**

- **V-LR-1**: 必填字段缺失或类型不符 → 写入拒绝（引擎 exit 2），不得产生半有效条目。
- **V-LR-2**: `line_id` 全局唯一；创建以 `O_CREAT|O_EXCL` 打开 `<line_id>.json`，已存在即重新生成或失败，绝不复用。
- **V-LR-3**: 重试/重新派发 MAY 产生新 `run_id`（本实现缺省产生新值）；无论用新值还是复用，旧尝试的结局 MUST 保留在 `run_history`（追加数组，含起止时间与结局）。重接线 MUST 复用原 `run_id`。
- **V-LR-4**: `state` 封闭集 `active | waiting | stalled | completed | orphaned | stale | closed`；其他取值拒绝。
- **V-LR-5**: `waiting` 必须有 `waiting_reason` 与 `queued_at`；因归属重叠时还必须带 `holder_line_id`；`waiting` 期间不得存在活动阶段执行（无 reservation、无存活 PID）。
- **V-LR-6**: `active` 且已派发时，四件套路径、`stage`、`runner_pid`、`cli_pid` 必须齐备；未派发时允许 `stage=null` 且无 PID。
- **V-LR-7**: `start_token` 是平台身份令牌：Linux 为 `/proc/<pid>/stat` 字段 22；macOS 为 `ps -p <pid> -o lstart=` 的规范化字符串。PID 不得单独存在而无 token。
- **V-LR-8**: `remote` 条目必须含 `alias`、`run_user`、`remote_root`；Registry 路径必须仍在驱动侧（不得写入远端共享目录）。
- **V-LR-9**: Registry `state` 与状态脊不得矛盾：已派发的 `active` ↔ 脊 `running/retrying`；`stalled` ↔ 脊 `stalled`；`completed` ↔ 脊 `done`（全部阶段完成，等待或已完成集成）。尚未派发的 `active`（`stage=null`、无 PID/四件套）与 `waiting` 没有阶段执行，不构成矛盾。`closed/stale/orphaned` 为终态/待处置态：以 `closed_at`、`last_event` 与保留的状态脊证据记录原因（如 `abandoned`、`stale-cleanup`），不再要求与脊当前值相等。
- **V-LR-10**: `closed` 条目保留全部历史字段，`closed_at` 必填；`list --active` 只返回 `active/waiting`（不返回 `stalled/completed/closed/stale/orphaned`）。
- **V-LR-11**: 未知扩展字段必须原样保留（向前兼容）；引擎不得因未知字段拒绝读取。
- **V-LR-12**: 并发读取方永不观察到不可解析 JSON、重复 `line_id` 或丢失其他条目（由 per-file 原子替换 + 目录独立保证）。

**State transitions**

```text
register(U0.5) ──> active（无重叠/未超 cap）| waiting(ownership-overlap|concurrency-cap)
waiting ──promote──> active           (holder 集成合并并 U6 closed / explicit release / disjoint)
active ──u5──> stalled ──retry(new run_id)──> active | ──explicit abandon(u6)──> closed
active ──explicit abandon(u6)──> closed
active ──u4 all stages done──> completed (写线: merge_ready=true, ready_for_merge_at; 只读线: merge_ready=false, 直接 u6)
completed ──integration-record(merged|failed)──> completed (状态不变；merge_ready=false；integration_result 记录)
completed ──u6(merged 或 explicit abandon)──> closed
active ──identity fail / evidence expired──> stale ──explicit cleanup──> closed
active/waiting ──line-owned evidence missing──> orphaned ──explicit disposition──> closed
```

`completed` 是唯一的 pre-merge 状态：全部阶段完成即进入，集成结果不引入新状态。U6 MUST 在 `integration_result` 记录之后执行；worktree 只在 merged 时由集成序列移除，failed/abandoned 时保留。`stalled` 与 `waiting` 不自动迁移；任何破除/释放都是显式动作并写入 `last_event`/历史。

---

## E2. Line Envelope（线路信封）

**Purpose**: 把每个事件归属到唯一 `(line_id, run_id)`，且不改变日志正文与哨兵最后一行。

**Fields**（JSON 旁路与 key=value 载体同一语义）

| Field | Type | Required |
|-------|------|----------|
| `line_id` | string | always |
| `run_id` | string | always |
| `stage` | string | always |
| `event` | enum | always |
| `at` | epoch seconds | always |
| `sentinel_seen` | 0\|1 | terminal status/log meta only |
| `exit` | int | terminal status/log meta only |
| `verdict` | string | watcher events only |
| `attribution` | enum | watcher/monitor output only |

`event` 封闭集：`prompt | pid | heartbeat | status | log-start | log-terminal | watcher-verdict | monitor | registry-update | integration`。

**Carriers**

| Carrier | Encoding | Owner |
|---------|----------|-------|
| `status-<line>-<stage>` | 行尾追加 ` line=… run=… stage=… event=status` | runner |
| `pid-<line>-<stage>` | 行尾追加 ` line=… run=… stage=… event=pid` | runner |
| `heartbeat-<line>-<stage>.log` | `at=… line=… run=… stage=… event=heartbeat` | runner |
| `log-<line>-<stage>.log.meta.jsonl` | 每行一个 JSON 对象 | runner（单写者，append-only） |
| `prompt-<line>-<stage>.md.meta.json` | 单个 JSON 对象 | driver（派发前） |
| `WATCH` / `EVIDENCE` 行 | 追加 ` line=… run=… attribution=…` | watcher |

**Validation rules**

- **V-EN-1**: 日志正文 MUST NOT 包含信封；哨兵字面量与「最后非空行」判定不变。
- **V-EN-2**: 分类封闭集 `own | foreign | stale-run | unattributed | legacy`：
  - `own`: `(line_id, run_id)` 与当前监听目标一致；
  - `foreign`: `line_id` 不同；
  - `stale-run`: `line_id` 相同、`run_id` 不同；
  - `unattributed`: 字段缺失或 JSON 不可解析；
  - `legacy`: watcher 未提供 `--line-id/--run-id`，保持 058 兼容行为（无归属过滤）。
- **V-EN-3**: 只有 `own` 事件可参与判定、进度与 Registry 状态；其余三类只可出现在摘要/线日志，不得计入。
- **V-EN-4**: meta 为 append-only 单写者；允许最后一行不完整（读者忽略不可解析的尾行），但不得重写历史行。
- **V-EN-5**: 信封中的 `line_id/run_id` 必须与文件名嵌入值一致；不一致按 `unattributed` 处理并报告。

---

## E3. Ownership Manifest（归属清单）

**Storage**: `$REGISTRY/manifests/<line_id>.json`（owner）；Registry 只存投影与指针。

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `schema_version` | int | always | `1` |
| `line_id` | string | always | 与 Registry 一致 |
| `owned_paths` | string[] | always | 写归属 |
| `read_only_paths` | string[] | always | 只读 |
| `forbidden_paths` | string[] | always | 禁止访问 |
| `integration_depends_on` | string[] | optional | 拓扑依赖的 line_id 列表 |
| `declared_at` | ISO | always | 声明时间 |

**Validation rules**

- **V-OM-1**: 路径按 V-OM-2 归一化后比较；同一 Manifest 内部不得有 owned 与 forbidden 的交集。
- **V-OM-2**: 归一化 = 相对路径以 `repo_root` 展开 → `os.path.realpath` → 去除尾部分隔符；符号链接解析到真实路径。
- **V-OM-3**: 写-写重叠 = 任一线 A 的 owned 路径等于或包含于另一线 B 的 owned 路径（双向）；注册/派发前检测，命中即拒绝或串行化。
- **V-OM-4**: 写线 MUST NOT 写入另一活动线的 `read_only_paths` 或 `forbidden_paths`；命中按重叠处理。
- **V-OM-5**: `integration_depends_on` 只能引用已注册的 line_id；引用不存在 → 队列构建显式失败，不忽略。
- **V-OM-6**: Manifest 是路径集与依赖的 owner；Registry 的 `owned_paths` 必须可由 Manifest 再生，冲突时以 Manifest 为准并修复投影。

---

## E4. Driver Lease（驱动租约）

**Storage**: `$REGISTRY/<line_id>.driver.lock`（JSON）；历史 `$REGISTRY/<line_id>.lease-history.jsonl`。

| Field | Type | Required |
|-------|------|----------|
| `line_id` | string | always |
| `holder_session` | string | always |
| `holder_pid` / `holder_start_token` | int/string | always |
| `host` | string | always |
| `acquired_at` / `heartbeat_at` | ISO | always；`heartbeat_at` 由每次续租刷新 |
| `ttl_seconds` | int | always；缺省 600；续租周期 MUST ≤ `ttl_seconds/3`（缺省 ≤200s） |

**Validation rules**

- **V-DL-1**: 获取以 `O_CREAT|O_EXCL` 创建；已存在时读取持有者。
- **V-DL-2**: 持有者存活 = `now < heartbeat_at + ttl` 且（本地）PID 与 start token 匹配；存活 → 夺取拒绝（引擎 exit 3）。心跳过期但（本地）PID 仍存活且 token 匹配 → `suspected-alive`：不得自动夺取，也不得按普通过期 lease 自动破除。`host` 与当前主机不同时，PID 证据经远端探针获取；拿不到 PID 证据不构成 `suspected-alive`，按心跳过期与状态脊证据处置。
- **V-DL-3**: 过期 lease 只能经 `lease-break --reason <…> --evidence-ref <…>` 破除；破除前必须验证持有者死亡/心跳过期证据；`suspected-alive` 只能追加 `--override` 显式破除，并在历史行记录「PID 活 + 心跳过期」证据；每次破除追加历史行。
- **V-DL-4**: `lease-renew` 只允许持有者本人；持有者 MUST 在 U2 派发、U3 终止、U4 校验、U5 处置各续租一次，且任意两次续租间隔 MUST ≤ `ttl_seconds/3`（缺省 ≤200s）；`lease-release` 只允许持有者本人；两者都刷新/删除 lease 文件。
- **V-DL-5**: 一个 line 同时最多一个有效 lease；lease 指向的 session 与 Registry `driver_session` 不一致时，以 lease 为准并记录 `last_event=lease-owner-changed`。

---

## E5. Stage Reservation（阶段预占）

**Storage**: `$REGISTRY/reservations/<line_id>.<stage>.json`。

| Field | Type | Required |
|-------|------|----------|
| `line_id` / `stage` / `run_id` | string | always |
| `pid` / `start_token` | int/string | always |
| `host` | string | always |
| `started_at` | ISO | always |

**Validation rules**

- **V-SR-1**: 创建必须 `O_CREAT|O_EXCL`；同一 `(line_id, stage)` 同时最多一个活动 reservation。
- **V-SR-2**: 第二启动者：若 reservation 的 `run_id` 与当前尝试相同且 PID 身份有效 → `attach`（附着监听）；否则拒绝（exit 3）。
- **V-SR-3**: stale reservation（PID 死亡/token 不符/心跳过期/状态脊显示该阶段已结束）只能显式破除；破除前留证据，写入 `<line_id>.<stage>.reservation-history.jsonl`。
- **V-SR-4**: U6 或阶段最终失败上送后释放 reservation；释放是显式动作。
- **V-SR-5**: reservation 存在但无对应 Registry/状态脊 → orphan 证据，必须调查，不得直接重派。

---

## E6. Identity / Reattach Snapshot

**Artifact**（不落盘为独立实体；由引擎输出 JSON）

| Field | Type | Notes |
|-------|------|-------|
| `line_id` / `run_id` | string | 当前尝试 |
| `identity` | enum | `ok \| mismatch \| dead \| remote-unreachable \| unknown` |
| `runner` / `cli` | object | `{pid, start_token_match, alive}` |
| `cwd_check` | enum | `ok \| mismatch \| unsupported \| skipped` |
| `branch_check` | enum | `ok \| mismatch \| skipped` |
| `reservation` | object\|null | 当前 reservation 摘要 |
| `lease` | object\|null | 当前 lease 摘要 |
| `evidence` | object | 四件套路径与读取摘要（不复制正文） |
| `branch_hint` | enum | `running \| done \| dead \| orphaned \| stalled`（提示，最终去向由驱动按合同分支表裁决） |

**Validation rules**

- **V-ID-1**: `identity=ok` 必须同时满足：runner PID token 匹配；`cli_pid`（若登记）token 匹配；branch 与 Registry 一致；cwd 检查为 `ok` 或 `unsupported`。
- **V-ID-2**: 任一同源 token 不符 → `mismatch`（PID 复用）；进程不存在 → `dead`。
- **V-ID-3**: 远端探针缺失/ssh 失败 → `remote-unreachable`，禁止映射为 `dead`。
- **V-ID-4**: 重接线 MUST 在 `identity` 计算后、任何重派前，先执行一次 `watch-target.sh --once`；两结果共同决定分支。
- **V-ID-5**: `identity=ok` 且快照 RUNNING → 只恢复监听；`done` → U4/U5；`dead/mismatch` → U5；`orphaned` → 调查；`remote-unreachable` → stalled 并重试连通性。

---

## E7. Integration Queue

**Inputs**: Registry 中 `state=completed` 且 `merge_ready=true` 的条目 + 各线 Manifest `integration_depends_on`。

**Computed entry**: `{order, line_id, ready_for_merge_at, layer, depends_on}`。

**Validation rules**

- **V-IQ-1**: 排序 = 拓扑分层（Kahn）→ 同层 `(ready_for_merge_at, line_id)` 升序；同输入重放逐字相同。
- **V-IQ-2**: 环 → 拒绝构建并上送，不合并任何环上线。
- **V-IQ-3**: 依赖满足 = 依赖 line 的 `integration_result.status=merged`（包括已 `closed` 的 merged 历史）。依赖 line 存在但尚未 merged（仍 `merge_ready=true` 未执行、`integration_result.status=failed`、或已 closed 且未合并）→ 该依赖视为未满足，条目留在队列并显式报告，不静默跳过；依赖 line_id 不存在或 Manifest 引用非法 → 按 V-OM-5 显式失败，不构建队列。
- **V-IQ-4**: 每线执行序列固定：rebase → 完整质量门 → 合并 → `integration-record`（更新该线 Registry 条目；`state` 保持 `completed`，`merge_ready=false`）→ 归档运行时 → 移除 worktree（仅 merged）；镜像同步与命令副本再生成不在逐线序列内，MUST 在整批条目处置后统一执行一次。任一步失败保留 worktree 与证据，继续下一条。
- **V-IQ-5**: 集成不得 force push、不得绕过确认门；push 仍需显式授权。

---

## E8. Runtime Archive Record

**Artifact**: 集成侧归档目录下 `runtime-archive-<line_id>.json`。

| Field | Type | Notes |
|-------|------|-------|
| `line_id` / `run_id` | string | 来源线 |
| `source_worktree` | abs path | 归档来源 |
| `dest_dir` | abs path | 集成侧目标 |
| `files` | array | `{original, archived_name, sha256, conflict}` |
| `created_at` | ISO | |

**Runtime-record path set**（本实体拥有的封闭集；E8 之外的文档只引用）：

```text
<worktree>/.specify/memory/feedback/
<worktree>/.specify/memory/session/
<worktree>/.specify/memory/knowledge/
<worktree>/.specify/memory/exec-quant/
```

**Excluded stores**（明确不在本集合内，任何文档不得把它们并入运行时归档）：

| Store | 排除理由 |
|-------|----------|
| `<worktree>/.specify/memory/evidence/` | 线级证据，随 worktree 保留/上送，不由集成合并 |
| `<worktree>/.specify/history/` | 主线派生的项目知识库，不允许按线分叉合并 |
| `<worktree>/.specify/memory/trigger/` | 宿主运行状态；line MUST NOT 写入 |

**Validation rules**

- **V-AR-1**: 归档必须在移除 worktree 之前完成，并以文件哈希核对。
- **V-AR-2**: 同名冲突保留双方：归档名 `<basename>.<line_id>.<n>`，`conflict=true`；禁止覆盖任一方。
- **V-AR-3**: 归档清单随集成提交一次性提交；各线阶段提交不得包含运行时记录（V-AR-4）。
- **V-AR-4**: 线的阶段提交只允许阶段产物路径；运行时记录路径集合以上方 **Runtime-record path set** 为唯一枚举，其他文档只引用本处，不得另列清单。
- **V-AR-5**: 归档与提交失败 → 保留 worktree 并上送；不得删除运行时记录。

---

## E9. CLI Capability Profile（CLI 能力档案）

**Storage**: `skills/external/sdd-loop-driver/references/cli/index.md`（schema/观测程序 owner）+ `<cli>.md`（每 CLI 一份，集合 `qodercli/claude/codex/opencode/hermes`）。

**Eight dimensions**（每条目一行）：`invocation`、`output_mode`、`timeouts`、`sentinel`、`buffering`、`session_logs`、`detach_signals`、`defects_versions`。

| Field | Type | Required |
|-------|------|----------|
| `dimension` | enum | always |
| `status` | enum | `known \| unknown` |
| `value` | string | known 必填；unknown 不得填猜测值 |
| `observed_at` | date | known |
| `cli_version` | string | known |
| `evidence_ptr` | string | known（命令/日志/提交指针） |

**Provenance table**（每份档案）：`date | trigger (U2\|U4\|U5) | observation | change | feedback_id`。

**Validation rules**

- **V-CLP-1**: 五份档案必须存在；`qodercli` 的八维度必须全部有 `known` 或 `unknown` 标注；其余四份允许全 `unknown`，但不得留空维度。
- **V-CLP-2**: `known` 必须带 `observed_at`、`cli_version`、`evidence_ptr`；`unknown` 不得含猜测值；超时 0/负值语义未实测即 `unknown`。
- **V-CLP-3**: 观测更新顺序 = 状态脊 `cli_observations` → 档案 provenance → 一条 `cli-profile:<cli>` 反馈；一次观测事件恰好一条反馈；无新事实零反馈。
- **V-CLP-4**: 档案不得改变哨兵、watcher 判定、退出码、确认门、阶段 deadline 或测试预算；当前阶段使用 U2 记录的形态。
- **V-CLP-5**: 派发资格（可接受形态/旗标/支持集）以 `scripts/python/execution-config.py` 的 `CAPABILITY_MATRIX` 为准；档案只记录观测，冲突时以矩阵为准并产生反馈，不暗改矩阵。
- **V-CLP-6**: 缺陷条目保留历史；修复记录 `fixed_in`；版本/平台不一致视为新观测，不沿用旧结论；冲突观测同存并附证据。

---

## E10. State Spine Extension（既有实体的追加字段）

状态脊 owner 仍是 `references/stage-prompts.md` § Stall Handling & State Spine；064 只追加：

| 追加字段/段 | 写入时点 | 规则 |
|-------------|----------|------|
| `line_id` / `run_id` 头字段 | U0 入口声明 | 与 Registry 一致；不改变既有字段语义 |
| `cli_observations` 段（append-only） | U4/U5 观测事件 | 三要素：观测事实 / 对照的档案条目 / 影响；先写段再改档案 |
| 派发记录 `profile_id` / `profile_version` / `observed_cli_version` | U2 | 只读查阅结果；当前阶段后续观测不得回溯改写 |
| `lease_acquired_at` / `lease_holder_session` | 重接线 | 与 lease 文件一致 |
| `resume_snapshot`（identity/branch_hint/verdict） | 重接线 | 一次性快照证据指针，不复制正文 |

**V-SS-1**: 064 的追加不得改变既有状态脊字段、阶段状态词或写入顺序；既有 `running/retrying/stalled/done` 仍由 058 owner 决定。

---

## E11. Resource Allocation

| Field | Type | Notes |
|-------|------|-------|
| `ports` | [int,int] | 端口块；缺省起点 39000、块大小 20（可配置） |
| `cache_dir` | abs path | `<repo_parent>/.spec-kit/cache/<repo-basename>/<line_id>` |
| `tmp_dir` | abs path | `<repo_parent>/.spec-kit/tmp/<repo-basename>/<line_id>` |
| `concurrency_cap` | int | 缺省 4；`SPECIFY_LINE_CONCURRENCY_CAP` 可覆盖 |

**Validation rules**

- **V-RA-1**: 端口块在活动线之间不得重叠；分配取最小空闲块；只登记不绑定，线必须只在自己的块内监听。
- **V-RA-2**: 活动线数（`active` 且已派发）超过 cap → 新线进入 `waiting`（`waiting_reason=concurrency-cap`），不得派发。
- **V-RA-3**: 缓存/临时目录每线独立；允许只读共享缓存，但不得写入共享路径；禁止启动全局服务。
- **V-RA-4**: 资源分配写入 Registry `resources` 并在收尾汇总中报告。

---

## 关系图（文本）

```text
Line Registry Entry 1 ── 1 Ownership Manifest
        │ 1
        ├── 0..1 Driver Lease
        ├── 0..1 Stage Reservation (per active stage; history keeps past)
        ├── 0..n Envelope events (status/pid/heartbeat/log.meta/prompt.meta)
        ├── 0..1 State Spine (existing; 064 adds fields)
        ├── 0..1 Resource Allocation
        ├── 0..n Runtime Archive Record (per integration)
        └── 0..1 Integration Queue Entry (when merge_ready)

CLI Capability Profile 1 ── n observations ── 1 feedback entry per event (cli-profile:<cli>)
```
