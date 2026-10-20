# Research — Phase 0 Decisions（Feature 064）

**Feature**: 064 Subagent 并发归属、CLI 能力档案与生命周期解耦
**Date**: 2026-10-20
**Inputs**: `requirements.md`（含 Clarifications 2026-10-20 两轮）、`/tmp/sdd-064/brief.md`（dated authority，逐字归档于 `notes/source-requirement.md`）、项目宪法 v1.13.0、master `ae0eebeb` 实测、Feature 063 在途分支 `bcf27c77` 只读检视。

本文件只记录**决策、替代方案与否决理由、实测基线**。规则本体落在 `contracts/`、`data-model.md` 与 plan 的 Decisions；此处不复述条款正文。

## 0. 实测基线（2026-10-20，本工作树）

| 检查 | 命令 | 结果 | 对 plan 的含义 |
|------|------|------|----------------|
| 需求校验 | `python3 .specify/scripts/python/validate-requirements.py .specify/specs/064-subagent-concurrency/requirements.md` | exit 0；`scanned 351 lines, 78 definition rows, 4 shared strings`；5 项检查全 pass | 规划起点有效 |
| Probe 注册表 | `python3 .specify/scripts/python/probe-utils.py --action probes --validate` | exit 0；`10 classes, 113 internal + 0 external objects` | 新增 1 个 Object 后的基线；当前无 `skill:sdd-loop-driver` 对象 |
| 编译嵌入 | `python3 .specify/scripts/python/probe-utils.py --action compile-embeds --check` | exit 0；`74 units, zero drift` | 新增 Object 行不得改变 Handler 指纹与编译文本 |
| 技能镜像 | `python3 scripts/python/sync-mirrors.py --check --only skills/external/sdd-loop-driver` | exit 2；3 个 DIFF：`SKILL.md`、`references/dispatch-recipes.md`、`references/watch-model.md` | **既有已提交漂移**；本特性恰好编辑这三份文件，同步后应转为 clean；验收判据为「no NEW drift」，不是绝对 0 |
| shared 镜像 | `python3 scripts/python/sync-mirrors.py --check --only shared/definitions` | exit 2；9 个 DIFF（`agent-definitions.md`、`contract-clause-definitions.md`、`derivation-definitions.md`、`dogfooding-definitions.md`、`framework-map.md`、`goal-definitions.md`、`self-improvement-definitions.md`、`subagent-definitions.md`、`tool-definitions.md`） | `probe-definitions.md` 当前不在漂移集；本特性只对 `shared/definitions/probe-definitions.md` 承担镜像义务，其余漂移为既有基线 |
| Watcher 自测 | `bash skills/external/sdd-loop-driver/scripts/watch-target.sh --self-test` | exit 1；`12 passed, 4 failed`：`pid-reuse`、`zombie`、`manifest`、`pgrep-zero-match-trap-reproduced` | macOS 无 `/proc` 的平台退化已在 063 plan 记录；本特性不得新增失败，且新增归属用例须在 macOS 可判定；不以这 4 项作为本特性回归 |
| Python 测试 | `python3 -m pytest` / `.venv` / `run-tests.sh` 探测 | 无任一解释器安装 pytest；`.venv` 不存在 | 契约测试的 **green 基线在本环境不可测量**；plan 不伪造测试结果，测试执行义务移交 implement 环境并在 verification 记录（Unobserved，不当作通过） |

补充代码事实（用于设计，不在此复述规则）：

- `watch-target.sh` 的 status 解析是 `grep -m 1 '^exit='` + `sentinel=` 正则；pid 解析是 `^pid=` 与 `start=` 正则。**在行尾追加 key=value 信封字段不破坏解析**；heartbeat 只按 mtime 消费，内容格式可扩展。
- 判定状态机与退出码由 `skills/external/sdd-loop-driver/scripts/watch-target.sh` 代码侧拥有（语义映射 `references/watch-model.md` §3）；064 只增加归属过滤，不改判定与退出码。
- 状态脊字段与写入时点由 `references/stage-prompts.md` § Stall Handling & State Spine 拥有；064 只追加 `line_id`/`run_id` 头字段、`cli_observations` 段与派发记录三字段。
- `scripts/python/execution-config.py` 的 `CAPABILITY_MATRIX` 当前只含 `qodercli/claude/codex/opencode`，**无 `hermes`**；hermes 档案仍须存在（骨架），但其派发资格按矩阵为「无条目」，档案只记录观测事实，不改矩阵。
- `scripts/python/sync-mirrors.py` 的 `MIRROR_PAIRS`：`skills/external → .specify/skills`（排除 `site/internal`）、`scripts → .specify/scripts`（strict extras）、`shared → .specify/shared`；新增档案与脚本自动落入既有镜像对。
- 063 在途分支 `bcf27c77` 已含 `contracts/cli-profiles.md`（CP-01…CP-10）与 `FR-044…FR-049`，其 schema owner 设计为 `references/cli/README.md`；该命名与宪法 X（禁止嵌套 `README.md`）冲突，064 以 `references/cli/index.md` 收编。

## 1. R1 — Line Registry 的形态与原子性

**Decision**: 环境级目录（`SPECIFY_LINE_REGISTRY_DIR`，缺省 `${XDG_STATE_HOME:-$HOME/.local/state}/spec-kit/lines`），每线一个 `<line_id>.json`；写入用同目录临时文件 + `fsync(file)` + `os.replace` + `fsync(dir)`；同线更新以 `<line_id>.lock` 的 `fcntl.flock` 排他锁串行化；跨线因文件独立而天然隔离。

**Rationale**:
- 单文件 JSON 可被任意读取方一次解析，避免「读半写」；`os.replace` 在同一文件系统内原子。
- 同线锁只保护「读-改-写」窗口；跨线不共享锁，不会因一条线持锁阻塞其他线。
- 目录位于任一 worktree 之外（registry 缺省在 `$HOME`/`$XDG_STATE_HOME`），可跨项目发现，且不会被 `git clean`/worktree 删除波及。

**Alternatives rejected**:
- 单一 registry JSON：跨线写入需要全局锁，且一次损坏丢失所有线路；违反 FR-003 的「不丢失其他 line 条目」。
- SQLite：新增运行时能力面与平台差异，且与「stdlib 文件 + 无 daemon」的最小形态不符（宪法 IX）。
- 写在项目 `.specify/` 内：违反 FR-001 的「位于 worktree 之外、无需扫描项目发现」。

**Failure behaviour**: 目录不可写、JSON 损坏、锁超时 → 注册/更新显式非零退出；U0.5 注册失败即上送并停止该 line 启动，绝不回退到项目内共享路径（Edge Case 已列）。

## 2. R2 — 归属信封的编码与哨兵保全

**Decision**: 四类载体，全部机器可读且**不进入日志正文**：
1. `status-<line>-<stage>` / `pid-<line>-<stage>` / `heartbeat-<line>-<stage>.log`：在既有 key=value 行尾追加 `line=<id> run=<id> stage=<stage> event=<status|pid|heartbeat>`。
2. 日志旁路 `log-<line>-<stage>.log.meta.jsonl`：runner 启动与终止各追加一条 JSON 对象（`event`/`line_id`/`run_id`/`stage`/`at`，终止条含 `sentinel_seen`、`exit`）。
3. 提示词旁路 `prompt-<line>-<stage>.md.meta.json`：派发前写入的静态信封。
4. Watcher 输出：`WATCH`/`EVIDENCE` 行追加 `line=`、`run=`、`attribution=`（`own|foreign|stale-run|unattributed|legacy`）。

哨兵字面量、日志最后非空行判定、日志正文零改动。

**Rationale**: 事故根因是事件无归属而非哨兵不可靠；把归属写在旁路既不位移哨兵，也不让旧读取方（tail/告警）看到新格式。既有 watcher 的解析正则对追加字段天然兼容（见 §0）。

**Alternatives rejected**:
- 在日志末行后追加 JSON：改变「最后非空行」语义，直接违反 FR-009。
- 把两个字段塞进日志首行：首行在 `-p` 缓冲模式下同样晚到，且无法覆盖 status/heartbeat 的独立归属。
- 每个事件一个单独 sidecar 文件：文件数量爆炸，watcher 读放大。

## 3. R3 — 无标识消息的入口归属

**Decision**: 归属判定下沉为确定性引擎动作 `resolve-message`（`line-registry.py`），驱动只呈现其结果。活动线 = `state ∈ {active, waiting}`。可识别标识 = 显式 `line_id` token，或唯一匹配的 `project_dir` / `repo_root` / `branch`。判定表：

| 活动线数 | 匹配结果 | 结果 |
|----------|----------|------|
| 0 | — | `no-active`：显式报告无活动线路，请求目标 |
| 1 | 无标识 | `route` 到唯一线 |
| 1 | 有标识但与唯一线不匹配 | `no-match`：报告该线与标识不匹配，不路由、不猜测 |
| ≥1 | 唯一匹配 | `route` |
| ≥2 | 无标识 / 多匹配 / 零匹配，首次 | `clarify`：**恰好一个问题** + 候选清单 |
| ≥2 | 用户回答后仍不唯一（`--clarified`） | `ambiguous-stop`：列出候选并停止，不再问第二个问题 |

引擎源码不得调用 `ps`/`pgrep`/进程名或 cwd 推断；契约测试以 PATH 桩与源码扫描双重钉住。

**Rationale**: 把「是否澄清、问几个」变成可测试的确定性输出，避免驱动侧自由发挥；一次澄清后停在候选清单，符合 FR-010 的「不再问第二个问题」。

**Alternatives rejected**: 由驱动自由判断（不可复现，正是事故形态）；用 cwd 推断单线（被需求明确禁止）。

## 4. R4 — worktree 路径、分支与分支纪律

**Decision**: 写线派发前创建 `git worktree add -b line/<line_id> <worktree_path> <base_sha>`；缺省 `worktree_path = <repo_parent>/.spec-kit/worktrees/<repo-basename>/<line_id>`，可由入口参数覆盖；`base_sha = git rev-parse <base-ref>`，`base-ref` 入口参数缺省 `main`（不存在时由驱动显式选择，不猜测）。子代理只在该 worktree 内提交，不切换分支、不创建/删除 worktree。

**Rationale**: 路径与仓库同级但在 worktree 之外，避免被本仓 `git clean` 或镜像脚本波及；分支名携带 `line_id`，天然唯一且可在 Registry 复核。`base_sha` 固定为登记时点，便于 rebase 与重放。

**Alternatives rejected**: 分支名 `feat/<feature>`（同特性多线冲突）；worktree 放在 repo 内（`git status`/镜像/测试会看到它）；由子代理自行建 worktree（违反「一 worktree 一写线」与「阶段子代理不改工作区拓扑」）。

## 5. R5 — Ownership Manifest、重叠与串行化

**Decision**: Manifest 为 `$REGISTRY/manifests/<line_id>.json`（路径集与 `integration_depends_on` 的 owner），Registry 只存 `ownership_manifest_path` 与 `owned_paths` 投影。归一化 = 相对 `repo_root` 展开 → `os.path.realpath` → 去尾分隔符。写-写重叠（任一 owned 路径相等或互相包含）在注册/派发前拒绝；后到线 `state=waiting`，持有 `waiting_reason`、`holder_line_id`、`queued_at`。排序 = `created_at` FIFO，同一时间戳 `line_id` 字典序。持线者死亡**不自动释放**：waiting 保留，上送后由显式 `release-ownership` 处置并留痕。

**Rationale**: 「写入前拒绝」比「运行中加锁」便宜且不会产生半写；Manifest 做 owner、Registry 做投影，符合 FR-020 与 One Source of Truth。

**Alternatives rejected**: 运行期文件锁（跨 git index/构建缓存无法覆盖）；按字符串集合比较（相对/绝对/符号链接会漏判）。

## 6. R6 — 集成队列的确定性

**Decision**: 就绪标记 = Registry 的 `merge_ready=true` + `ready_for_merge_at`（不是 `state` 值，保持状态封闭集不变）。队列 = 以 Manifest `integration_depends_on` 建有向图 → Kahn 分层 → 同层按 `(ready_for_merge_at, line_id)` 升序；检测到环 → 显式拒绝并上送，不合并任何环上线。重放同一 Registry+Manifest 输入得到逐字相同顺序。

**Rationale**: 拓扑依赖优先于同层 FIFO，符合 FR-025；把 `ready_for_merge` 建模为标记而非状态，避免与状态脊/Registry 状态封闭集冲突。

**Alternatives rejected**: 纯时间戳排序（违反显式依赖）；优先级数值（主观且不可重放）。

## 7. R7 — 运行时记录与镜像只集成一次

**Decision**: 每条线把运行时记录写在自身 worktree 内（既有引擎路径），但**提交纪律**只允许阶段产物路径；集成者用 `archive-runtime` 动作把 `.specify/memory/{feedback,session,knowledge}/` 与 exec-quant/run-determination 记录复制到集成侧归档目录（冲突时保留双方并以 `<name>.<line_id>.<n>` 命名、`conflict=true` 标记），再一次性提交；`sync-mirrors.py` 与 `regen-command-copies.py` 只在集成过程执行一次。

**Rationale**: 与现有引擎的写路径零冲突；归档动作输出 JSON 清单，可被测试与收尾汇总消费。冲突保留双方满足 Edge Case「不得静默覆盖任一方」。

**Alternatives rejected**: 每线各自提交运行时记录（Git index 干扰 + 双份）；把运行时目录重定向到 worktree 外（需要改多个引擎的 workspace-root 语义，超出本特性范围）。

## 8. R8 — 脱离式执行、lease、reservation 与重接线

**Decision**:
- **脱离**：本地 `setsid`（可用时）+ `nohup` + stdio 重定向；远端 `ssh + su + nohup`（既有配方）。runner 把 CLI 作为子进程后台启动、记录 `cli_pid` + start token、`wait` 后写 status。
- **Lease**：`<line_id>.driver.lock` 以 `O_CREAT|O_EXCL` 创建，内容 JSON（session/pid/start token/host/acquired_at/heartbeat_at/ttl=600s）；`lease-renew` 刷新 `heartbeat_at`；活持有者（心跳未过期且本地 PID 身份匹配）拒绝夺取；过期 lease 只能经 `lease-break --reason --evidence-ref` 破除，并追加 `<line_id>.lease-history.jsonl`。
- **Reservation**：`$REGISTRY/reservations/<line_id>.<stage>.json` 以 `O_CREAT|O_EXCL` 创建；已有活动 reservation 时第二启动者只能 `attach`（同 run_id 且 PID 身份有效）或拒绝；stale reservation 先验证 PID/心跳/状态脊再显式破除。
- **重接线**：`lease-acquire` → `verify-identity`（runner/cli PID start token；Linux 追加 `/proc/<pid>/cwd`；branch 由 worktree `git rev-parse --abbrev-ref HEAD` 复核）→ `watch-target.sh --once` → 三分支（running 恢复监听 / done 进 U4/U5 / dead 进 U5），零重复派发。

**Rationale**: lease 表达「哪个人类会话在驱动」这一无进程实体的所有权，不能用 flock 的进程生命周期表达；reservation 表达「哪个进程在执行该阶段」，必须由 OS 原子创建保证唯一。两者职责不同、都必需。

**Alternatives rejected**: 只用 flock（驱动是 LLM 会话，无长驻进程可持锁）；只用 PID 文件（PID 可能被复用，且无法表达会话所有权）。

## 9. R9 — orphan / stale / 远端不可达的分类

**Decision**: 只从线自有证据分类：Registry、状态脊、四件套、reservation、lease。`verify-identity` 的判定为 `ok | mismatch | dead | remote-unreachable | unknown`；`orphan-check` 识别「reservation/PID 存在但 Registry/状态脊缺失」「Registry 指向的证据全缺」等组合。远端：本地跑 `classify-remote --probe-json`，探针由 `ssh ... 'python3 line-registry.py --action verify-identity ...'` 产生；ssh 失败（255/超时）→ `stalled`（reason=`remote-unreachable`），绝不记为 dead，绝不触发重派。

**Rationale**: 满足 FR-054/055 与 Edge Cases；把远端探针与本地分类分成两步，使「连接失败」与「进程死亡」在类型上不可混淆，并可离线测试。

**Alternatives rejected**: 本地 `ssh` 内联判定（测试需真实远端）；用 `ps` 发现 orphan（明确禁止）。

## 10. R10 — CLI 能力档案与 063 收编

**Decision**:
- 落点 `skills/external/sdd-loop-driver/references/cli/<cli>.md`，schema/观测程序 owner 为 `references/cli/index.md`（索引型文件按宪法 X 的路径语义选择 `index.md`；宪法 X 的保留名阻断严格范围只覆盖项目根与 `docs/`，因此这是命名一致性选择，不是对治理范围的扩权）。
- 八维度：调用与参数/权限模式；输出模式；后台/超时上限；哨兵可靠性与非终止回显；缓冲/可见性；session/run 日志；detach/信号/孤儿；已知缺陷/版本/证据。
- 观测触发：U2 只读查阅并记录 `profile_id/profile_version/observed_cli_version`；U4/U5 各比对一次。更新顺序：状态脊 `cli_observations` → 档案 provenance → `feedback-utils.py` 恰好一条 `cli-profile:<cli>`；无新事实零反馈。
- Probe Object：`skill-sdd-loop-driver-cli-profile`，优先 `skill-wrapup` class + `unit=skill:sdd-loop-driver` + `lifecycle_point=wrap-up`；若 `probes --validate` 拒绝该组合，则退到 `external-custom` + `custom:skill:sdd-loop-driver`（requirements FR-040 授权），仍不新增 class/handler/lifecycle point。
- 063 逐条裁决见 `notes/063-overlap-adjudication.md`；063 的 stream-json/nohup 作为依赖引用，不复制。

**Rationale**: 档案是行为知识而非派发资格，引用 `CAPABILITY_MATRIX`；`index.md` 同时满足宪法 X 与单一 owner；Probe Object 以最小登记面接入既有反馈链。

**Alternatives rejected**: 继续沿用 063 的 `README.md`（违反宪法 X）；把档案并入 `dispatch-recipes.md`（行为知识会随配方膨胀且失去按 CLI 的检索面）；新建独立 probe class（超出「最小」）。

## 11. R11 — 测试策略与 red-first

**Decision**: Tests Mode = **ON**（可执行 Python 引擎 + shell watcher 扩展）。测试分三层：
- `tests/unit/`：纯函数（路径归一化、队列拓扑排序、信封分类、入口判定表、lease 过期判定）。
- `tests/contract/`：条款级（注册表原子性/锁/状态词表；watcher 归属与退出码不变；档案集合/维度/known-unknown/标记与 Probe Object；SKILL.md 章节与镜像）。
- `tests/integration/`：双线同哨兵隔离与无标识消息；同仓双写线 worktree/队列；主会话 kill/reattach 三分支；CLI 观测→反馈。

Red-first：每个新脚本/扩展先写失败测试并记录 red 运行（`verification.md`）；变异演练至少三项：删除信封过滤、删除 detach、删除 reservation 排他，各使至少一条测试转红。

**Rationale**: 宪法 IV 与 requirements FR-067；fixture 用临时目录/临时 git 仓库，不依赖真实远端或网络。

**Environment note**: 本机无 pytest，green 基线不可测量；这不是「通过」，implement 阶段必须在具备 pytest 的环境补测并留证据。

## 12. R12 — 文档入口与镜像

**Decision**: 更新 `docs/reference/skills/sdd-loop-driver.md` 增加「并发归属与生命周期」「CLI 能力档案」入口（指向 skill 引用，不复述内容）。镜像义务：`skills/external/sdd-loop-driver/**` → `.specify/skills/sdd-loop-driver/**`；`shared/definitions/probe-definitions.md` → `.specify/shared/definitions/probe-definitions.md`；docs 无镜像。验收 = 「本特性触碰的镜像对无 NEW drift」并按 §0 记录基线。

**两顶帽子声明（宪法 XI）**: 本特性编辑的是**框架源**（`skills/external/**`、`shared/definitions/**`、`docs/**`、`tests/**`）；`.specify/skills/**` 与 `.specify/shared/**` 是这个仓库作为客户项目时的**运行时投影**，由 `sync-mirrors.py` 生成，不手工编辑。任何面向所有下游项目的规则都落在源侧并随发布/init 流动，运行时副本只做镜像同步。

**Rationale**: 宪法 XIV（引用不复述）与 plan 模板的镜像义务；`sync-mirrors.py --only` 可把范围限制到本特性触碰的文件。

## 13. 未决事项（不在本阶段猜测）

- qodercli 超时环境变量的 `0/负值` 语义：档案记为 `unknown`，待 implement 期实测填值（requirements FR-036 明确禁止猜测）。
- hermes 的 `CAPABILITY_MATRIX` 条目缺失：由 Feature 061 owner 决定是否补；064 只记录档案与缺口。
- macOS 的 watcher `pid-reuse`/`zombie` 自测为既有平台退化；本特性不扩大也不修复该基线（不引入 `/proc` 依赖的强制判定）。
