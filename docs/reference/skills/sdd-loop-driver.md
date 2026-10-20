# sdd-loop-driver（无人值守 SDD 循环驱动）

**机制一句话**：以一条一遍性提示词驱动宿主 agent 完成「登录环境 → 以 qodercli 为子代理 → 按阶段推进 SDD 全流程 → 合并 main」的循环闭环，全程自推进、零用户提醒。真源：`skills/external/sdd-loop-driver/SKILL.md`（+ references/ 三份手册 + `scripts/watch-target.sh`）。

## 加载与投递

skill 本体是**自包含手册**（SKILL.md + references/ + scripts/），三种投递形态等价——宿主技能目录安装、提示词内嵌/粘贴、文件路径引用；不依赖任何下载或安装机制。宿主 agent **不需要安装 spec-kit**。

## 双拓扑实例化（入口参数清单）

| 参数 | 远端拓扑 | 本地拓扑 |
|------|----------|----------|
| 登录别名 | `ssh <alias>`（如 root 登录后 `su <run-user>`） | 无（本机直驱） |
| 执行身份 | `su <run-user>`（如 develop） | 当前用户 |
| 项目路径 | `/cws_work/<project>` 等入口声明 | 本地路径 |
| 子代理 CLI | qodercli（`DISPATCH_CLI` 可覆盖） | 同左 |
| 断点阶段 | 可不声明（自动探测） | 同左 |
| 终态权威文档 | 入口声明路径 | 同左 |

入口话术示例见 skill 手册 `## When to Load`；典型形态：「使用SDD开发模式推动 <项目>……需要使用一个循环来完成这项工作，而不是每次由我提醒你『重试』或者『继续』。」

## 执行侧可移植性

- 宿主环境**无需** `.specify/` 目录、无需安装 spec-kit——skill 全部操作要点内联自包含。
- 投递后宿主按手册驱动循环：断点探测 → 阶段派发（脱离模式后台自跑）→ 统一监听（长轮询窗口，事件优先）→ 哨兵与独立校验 → 续环 → git 状态判定合并收尾。
- **目标项目侧依赖**：仅当子代理要在目标项目执行 `/speckit.*` 阶段命令时，目标项目才需要具备 `.specify/` 结构；目标项目无 `.specify/` 时机制报告停线、不自动初始化。

## 机制归属（Feature 060 委派化）

驱动子代理的公用机制已上收，本技能保留编排本体：

- **前置检查（五族）与失败处置链**：权威落点 `skills/internal/run-agent/references/dispatch-preflight.md`（本技能引用）。
- **反嵌套义务**：权威落点 run-agent 派发治理 + `shared/definitions/subagent-definitions.md`（本技能 Driver Topology 节保留循环视角自检行）。
- **通用派发配方**（断点探测/提示词落盘/runner/本地变体）：`shared/workflow/external-dispatch-recipes.md`；本技能保留差异面——正证据四件套（pid/status/log/heartbeat）、统一监听模型、nohup 脱离形态权威落点、阶段链与收尾编排。
- **实例创建**：经 create-agent（`agents/sdd-executor.agent.md` 模板 → 职责实例）。

## 统一监听模型

等待/监控/轮询/wait/monitor 的语义统一收敛到 `references/watch-model.md`，参考实现为 `scripts/watch-target.sh`：

- **信号**：退出记录、完成哨兵、PID（含 start ticks/PID 复用校验）、心跳、日志尾行；完成必须有正证据——进程消失、日志静默、`pgrep` 零匹配都不是完成。
- **机制阶梯**：长轮询窗口（一次调用内等待，事件发生即返回）→ 宿主原生通知（仅作补充，不得结束驱动者会话）→ 间隔轮询回退；禁止独立 `sleep` 回合空等。
- **窗口 ≠ 超时**：单窗口到期只返回 `RUNNING` 并立即重入；只有阶段 deadline 产生 `TIMEOUT`。
- **Deadline grace / TIMEOUT 不是可杀信号**：watcher 在 deadline 后继续采样 `--deadline-grace`（缺省 120s），晚完成重判 `DONE`/`FAILED`；收到 `TIMEOUT` 先 `--once` 最终快照，`pid=alive` + `heartbeat=fresh` 时优先延长/继续，停线须用户显式决定并保留 worktree/status/log。
- **多线批量**：manifest 模式一次连接检查多条线，任一线终止即返回全部快照。
- **pgrep 陷阱**：`pgrep -c` 零匹配会先打印 0 再以退出码 1 结束，`|| echo 0` 会追加第二个 0；存活判据一律用 PID 文件 + `kill -0`，watcher 自测覆盖零匹配、僵尸、PID 复用等反向用例。

## 并发归属与生命周期

- **Line Registry**：环境级线路登记（`scripts/line-registry.py`，stdlib-only）；每个事件携带 `(line_id, run_id)` 归属信封，`foreign`/`stale-run`/`unattributed` 不改变当前线路状态；无标识消息经确定性入口判定（恰好一次澄清，禁止进程扫描推断）。规则真源：`skills/external/sdd-loop-driver/references/stage-prompts.md` 的 Line Registration/Envelope/Ingress 节。
- **工作区隔离与集成队列**：worktree-per-write-line、Ownership Manifest 归一化重叠、FIFO 串行化、确定性拓扑队列、运行时归档一次与每批一次镜像。操作序列见 `references/dispatch-recipes.md` Recipe 7。
- **生命周期解耦**：脱离式 runner（`setsid`/`nohup`/`disown`）、driver lease、`(line_id, stage)` 原子 reservation、重接线三分支（running/done/dead）与远端不可达分类。程序见 `references/stage-prompts.md` 的 Reattach & Lifecycle 节；监听归属层见 `references/watch-model.md` §11。

## CLI 能力档案

每个作为 subagent 调用的 CLI 在 `skills/external/sdd-loop-driver/references/cli/` 拥有独立档案（八维度、known/unknown 与 provenance）。`references/cli/index.md` 是 schema 与观测程序的 owner；派发前（U2）查阅、U4/U5 观测后更新，并记录 `cli-profile:<cli>` 反馈。派发资格仍由 Feature 061 的 `CAPABILITY_MATRIX` 唯一拥有。本页只提供入口，不复述档案内容。

## 触发与路由

- 以 `/sdd-loop-driver` 给出功能/改进描述 = SDD 目标；目标项目可为当前仓库，**包括 sdd-loop-driver 自身**。
- 改进对象是技能本身时仍走阶段链；只有入口显式声明「只做技能维护、不走 SDD」才允许 improve-skills/create-skills 等维护路径。
- 入口参数缺失时按缺省解析（当前仓库 / 本地直驱 / 入口描述为权威 / U1 自动探测），不得因参数不全切换流程。
- 进入 U2 前执行 U0.5 自检：未写出入口声明与阶段计划，不得直接编辑目标仓库。规则真源见 `skills/external/sdd-loop-driver/SKILL.md`。

## 边界

- push / 远程分支操作维持破坏性确认门控（缺省本地合并）。
- 不改变各阶段命令内部流程；不为变体新增机制分支。
- 多线并行时的并发隔离与窄读法授权纪律见 skill 手册 `references/stage-prompts.md`。
