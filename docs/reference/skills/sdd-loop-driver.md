# sdd-loop-driver（无人值守 SDD 循环驱动）

**机制一句话**：以一条一遍性提示词驱动宿主 agent 完成「登录环境 → 本地用宿主原生子代理 / 远端用 qodercli 为子代理 → 按阶段推进 SDD 全流程 → 合并 main」的循环闭环，全程自推进、零用户提醒。真源：`skills/external/sdd-loop-driver/SKILL.md`（+ references/ 五份手册（含效率 owner `efficiency-model.md`、状态感知 owner `state-awareness.md`）+ `scripts/`）。

## 加载与投递

skill 本体是**自包含手册**（SKILL.md + references/ + scripts/），三种投递形态等价——宿主技能目录安装、提示词内嵌/粘贴、文件路径引用；不依赖任何下载或安装机制。宿主 agent **不需要安装 spec-kit**。

## 双拓扑实例化（入口参数清单）

| 参数 | 远端拓扑 | 本地拓扑 |
|------|----------|----------|
| 登录别名 | `ssh <alias>`（如 root 登录后 `su <run-user>`） | 无（本机原生子代理） |
| 执行身份 | `su <run-user>`（如 develop） | 当前用户 |
| 项目路径 | `/cws_work/<project>` 等入口声明 | 本地路径；缺省当前项目 |
| 子代理承载 | qodercli（`DISPATCH_CLI` 可覆盖） | 宿主原生子代理（不启动 qodercli） |
| 断点阶段 | 可不声明（自动探测） | 同左 |
| 终态权威文档 | 入口声明路径 | 同左 |

**本地缺省**：未给 host+path → 当前项目；子代理用宿主原生形态，MUST NOT 启动 qodercli。远端才使用 qodercli 等外部 CLI 与 runner/统一监听模型。

入口话术示例见 skill 手册 `## When to Load`；典型形态：「使用SDD开发模式推动 <项目>……需要使用一个循环来完成这项工作，而不是每次由我提醒你『重试』或者『继续』。」

## 执行侧可移植性

- 宿主环境**无需** `.specify/` 目录、无需安装 spec-kit——skill 全部操作要点内联自包含。
- 投递后宿主按手册驱动循环：断点探测 → 阶段派发（远端脱离后台自跑；本地原生直接调用）→ 统一监听（仅外部 CLI：长轮询窗口，事件优先）→ 哨兵与独立校验 → 续环 → git 状态判定合并收尾。
- **目标项目侧依赖**：仅当子代理要在目标项目执行 `/speckit.*` 阶段命令时，目标项目才需要具备 `.specify/` 结构；目标项目无 `.specify/` 时机制报告停线、不自动初始化。

## 机制归属（Feature 060 委派化）

驱动子代理的公用机制已上收，本技能保留编排本体：

- **前置检查（五族）与失败处置链**：权威落点 `skills/internal/run-agent/references/dispatch-preflight.md`（本技能引用）。
- **反嵌套义务**：权威落点 run-agent 派发治理 + `shared/definitions/subagent-definitions.md`（本技能 Driver Topology 节保留循环视角自检行）。
- **通用派发配方**（断点探测/提示词落盘/runner；外部本地变体仅用于显式外部派发）：`shared/workflow/external-dispatch-recipes.md`；本技能保留差异面——正证据四件套（pid/status/log/heartbeat）、统一监听模型、nohup 脱离形态权威落点、阶段链与收尾编排。
- **实例创建**：经 create-agent（`agents/sdd-executor.agent.md` 模板 → 职责实例）。

## 统一监听模型

等待/监控/轮询/wait/monitor 的语义统一收敛到 `references/watch-model.md`，参考实现为 `scripts/watch-target.sh`。**适用范围**：仅外部 CLI 派发（远端拓扑）；本地原生调用是同步阻塞调用，返回即判定，不进入本模型。

- **信号**：退出记录、完成哨兵、PID（含 start ticks/PID 复用校验）、心跳、日志尾行；完成必须有正证据——进程消失、日志静默、`pgrep` 零匹配都不是完成。
- **机制阶梯**：长轮询窗口（一次调用内等待，事件发生即返回）→ 宿主原生通知（仅作补充，不得结束驱动者会话）→ 间隔轮询回退；禁止独立 `sleep` 回合空等。
- **监听签名唯一**：每个窗口 MUST 携带字面量 `--iter <run_id>-w<NN>`（`NN` 递增）；同参数连续调用会被宿主判为重复并误报卡死，令牌不能用 `$(date)`/`$$` 等运行时展开（owner：`references/watch-model.md` §3.2）。
- **窗口 ≠ 超时**：单窗口到期只返回 `RUNNING` 并立即重入；只有阶段 deadline 产生 `TIMEOUT`。
- **Deadline grace / TIMEOUT 不是可杀信号**：watcher 在 deadline 后继续采样 `--deadline-grace`（缺省 120s），晚完成重判 `DONE`/`FAILED`；收到 `TIMEOUT` 先 `--once` 最终快照，`pid=alive` + `heartbeat=fresh` 时优先延长/继续，停线须用户显式决定并保留 worktree/status/log。
- **多线批量**：manifest 模式一次连接检查多条线，任一线终止即返回全部快照。
- **pgrep 陷阱**：`pgrep -c` 零匹配会先打印 0 再以退出码 1 结束，`|| echo 0` 会追加第二个 0；存活判据一律用 PID 文件 + `kill -0`，watcher 自测覆盖零匹配、僵尸、PID 复用等反向用例。

## 状态感知快照（065a-state-awareness）

**机制一句话**：一次调用把一条线的脊、Registry、四件套、watchbeat、产物与提交证据、watcher 判定聚合成一个 JSON 信封，给出唯一恢复动作建议。**只读**——不写脊、不杀进程、不删证据；字段面 owner 是本技能参考手册 `references/state-awareness.md`，本页只给入口与关系。

- **入口**：`scripts/loop-state.py`（Python ≥ 3.8，仅标准库，无常驻进程、无网络轮询）。
- **调用形态**：
  - `--action snapshot --line-id <line> [--stage …] [--state-dir …] [--spec-dir …] [--repo …] [--spine …] [--watch-script …] [--out …]` — 读本地证据给出聚合快照；`--out` 是唯一写路径（落在 state dir / repo 内一律拒绝）。
  - `--probe <file>` — 只消费调用方采集的 probe JSON（形状 (a) 快照信封 / 形状 (b) 最小可达性），不读本地证据、不调本地 watcher，与本地路径参数互斥。
  - `--self-test` — 自建临时夹具跑内建用例，末行 `SELF-TEST: N passed, M failed`。
  - `--action recover` / `--action check-spine` — 本切片只返回结构化拒绝信封（owner 分别为 065c / 065b）。
- **信封**：`schema_version=1`；`loop_state` 取十一值封闭集，`recovery_action` 取 `none/watch/verify/resume/retry/stop` 中恰好一个；缺失值一律 `null`。
- **退出码**：`0` 求值成功（任何 `loop_state` 都是数据）、`1` 拒绝或校验失败、`2` 参数错误或必需输入不可读/不可解析；watcher 的 `10–16` 是**数据**，只写入 `watch_verdict.exit_code`。
- **与 watcher 的关系**：有活动 watch target 时 `loop_state` 与 `watch-target.sh` 的判定逐字一致（`verdict_source=watcher`）；无 target 时按 `requirements.md` FR-004 的优先级在本地派生（`verdict_source=derived`）。判定状态机与退出码语义的 owner 是 `references/watch-model.md`，本入口不复述、不改写。
- **与 Registry 的关系**：`scripts/line-registry.py` 的条目提供路径与 `stage` 回退（显式参数 > Registry 条目 > 环境约定 > `null`）；条目缺失记 `status=missing` 且不致命，绝不猜路径、不扫进程。
- **只读边界**：快照不改任何 mtime、不写四件套与工作树；`stop` 只是建议，停线须在最终快照与用户显式决定之后。

## 运行效率优化（063-sdd-loop-efficiency 切片；058 演化）

四项编排层优化，规则与字段面 owner 是 skill 参考手册 `references/efficiency-model.md`：

- **中型特性快车道**：仅入口携带 `fast-lane=opt-in` 时，在 tasks 后按七项机械判据裁决；录取则跳过 checklist、保留 analyze/review，判据失效即 fail-closed 回退完整链（默认仍是完整链）。
- **两槽位测试预算**：每线只有 implement 起点 baseline 与 review 后 closure 两次全量；中间阶段与 review 用 `targeted-set-v1` 定向集并记录证据；槽外全量必须是有原因与证据的显式例外，缺失证据报 `unknown`。
- **plan 只小修约束**：plan 完成后下游只允许小修并须 `PLAN-EDIT:` 声明；实质改动必须显式异常回传并由驱动按两分支处置；requirements 门内变更按最新锚点 re-baseline。
- **进度可见与脱离**：阶段 runner 默认 stream-json，原始事件流与派生 live log 同时保留；本地与远端都用 `nohup` 脱离；`--once` 重入只核验、不重派。

**上游效率门（2026-10-21 增补）**：

- **大特性拆分门**：plan 入口 FR >30 或 tasks U4 任务 >40 时判 `split-required`，驱动必须先拆成各自落入区间（8–30 FR / 10–40 任务）的切片，再逐条走完整链（`scripts/decomposition-check.py`）。
- **确定性预检**：requirements/plan/tasks 的 U4 在派发下一阶段前运行 `scripts/pre-analyze-check.py`，机械拦截重复/悬空 ID、`blockedBy` 断链、计数声明漂移与死路径；机械项不再留到 analyze。
- **跨特性重叠预检**：clarify U4 运行 `scripts/overlap-check.py` 比较同级特性的共享交付路径（`same-path`/`nested-path`），重叠必须先完成归属裁决并写入两条线状态脊，才能派发 plan。

**日志形态变化（已披露）**：stream 模式新增 `raw-<line>-<stage>.jsonl` 与派生 `log-<line>-<stage>.log`；CLI 不支持该输出模式或派生失败时降级为既有缓冲模式，并在 status 记录 `progress=degraded` 与原因。完成判定不变：哨兵仍只认 live log 最后非空行，watcher 判定与退出码、确认门、独立校验与卡死处置均未改变。

## 任务拆解与配合（070-subagent-task-teams 切片）

阶段级任务拆解层：把一个阶段拆成有界 Work Package，确定性门裁决后按图调度，独立校验、确定性集成；阶段哨兵与 U4 不变。本页只给入口与指针（运行时 owner：skill 手册 `references/decomposition-model.md`，本节不复述规则）：

- **门**：`scripts/wp-gate.py --check plan|preflight|retry`——确定性、stdlib-only、不派发、不写脊；拒绝码与退出码以 `references/decomposition-model.md` §12 与 070 契约为准。
- **默认启用**：`plan` / `implement` / `review` = `auto`（门通过、至少两个包且收益成立才拆解）；`analyze` / `clarify` 仅在显式 `on` 时启用；其余阶段保持单子代理。
- **退出与回退**：U0 声明 `decomposition: auto|off`、`decomposition_stages`、`decomposition_slot_cap`；阶段 attempt 可带 `decomposition_override`。`disabled` / `single-package` / `fallback` 都走原有单子代理路径（提示词、派发、哨兵、U4 不变）；fallback 必须具名原因，且绝不运行部分包集。
- **团队形状**：`templates/stage-team-preset.md` 是运行域 preset——不写入 `.specify/teams/`，不改 `create-team` / `run-team`。
- **报表**：`scripts/wp-report.py` 从状态脊派生协调报告；缺失来源记 `not_evaluated`。
- **边界**：只新增 U4 之前的步骤；哨兵、U4、阶段链、两槽位测试预算、plan 小修约束，以及 064/067/068 语义均不变。

## 并发归属与生命周期

- **Line Registry**：环境级线路登记（`scripts/line-registry.py`，stdlib-only）；每个事件携带 `(line_id, run_id)` 归属信封，`foreign`/`stale-run`/`unattributed` 不改变当前线路状态；无标识消息经确定性入口判定（恰好一次澄清，禁止进程扫描推断）。规则真源：`skills/external/sdd-loop-driver/references/stage-prompts.md` 的 Line Registration/Envelope/Ingress 节。
- **工作区隔离与集成队列**：worktree-per-write-line、Ownership Manifest 归一化重叠、FIFO 串行化、确定性拓扑队列、运行时归档一次与每批一次镜像。操作序列见 `references/dispatch-recipes.md` Recipe 7。
- **生命周期解耦**：脱离式 runner（`setsid`/`nohup`/`disown`）、driver lease、`(line_id, stage)` 原子 reservation、重接线三分支（running/done/dead）与远端不可达分类。程序见 `references/stage-prompts.md` 的 Reattach & Lifecycle 节；监听归属层见 `references/watch-model.md` §11。

## CLI 能力档案

每个作为 subagent 调用的 CLI 在 `skills/external/sdd-loop-driver/references/cli/` 拥有独立档案（八维度、known/unknown 与 provenance）。`references/cli/index.md` 是 schema 与观测程序的 owner；派发前（U2）查阅、U4/U5 观测后更新，并记录 `cli-profile:<cli>` 反馈。派发资格仍由 Feature 061 的 `CAPABILITY_MATRIX` 唯一拥有。本页只提供入口，不复述档案内容。

## Hook 兜底与远程 SSH（2026-10-19 增强）

- Qoder CLI 的 `Stop`/`SubagentStop` hooks 可作为**提前完成信号**：runner 用 `--settings` 按派发注入 Stop hook，hook 原子写 `hook-event-<stage>.json` 并尽力写 FIFO；watcher 用 `--hook-done`/`--hook-fifo` 缩短等待。hook 只产生 `hook=observed`，DONE 仍由退出记录 + 哨兵决定。
- 远端 SSH：hook 在 run-user 侧写 done/FIFO；本地每个窗口用 `ssh … "su - <run-user> -c 'bash --noprofile --norc -c …'"` 长读 FIFO，事件返回后再跑 `watch-target.sh --once` 取权威判定。断线不杀远端进程，下一窗口先查 `done.json`。
- 观测侧故障矩阵（pgrep 零匹配、无关会话作用域、登录 shell 噪声、共享目录误删、hook 未触发、进程消失≠完成）与双信号规则见 skill 手册 `references/watch-model.md` §12–§13。


## 触发与路由

- 以 `/sdd-loop-driver` 给出功能/改进描述 = SDD 目标；目标项目可为当前仓库，**包括 sdd-loop-driver 自身**。
- 改进对象是技能本身时仍走阶段链；只有入口显式声明「只做技能维护、不走 SDD」才允许 improve-skills/create-skills 等维护路径。
- 入口参数缺失时按缺省解析（当前项目 / 本地原生子代理 / 入口描述为权威 / U1 自动探测），不得因参数不全切换流程。
- 进入 U2 前执行 U0.5 自检：未写出入口声明与阶段计划，不得直接编辑目标仓库。规则真源见 `skills/external/sdd-loop-driver/SKILL.md`。

## 边界

- push / 远程分支操作维持破坏性确认门控（缺省本地合并）。
- 不改变各阶段命令内部流程；不为变体新增机制分支。
- 多线并行时的并发隔离与窄读法授权纪律见 skill 手册 `references/stage-prompts.md`。
