# sdd-loop-driver（无人值守 SDD 循环驱动）

**机制一句话**：以一条一遍性提示词驱动宿主 agent 完成「登录环境 → 以 qodercli 为子代理 → 按阶段推进 SDD 全流程 → 合并 main」的循环闭环，全程自推进、零用户提醒。真源：`skills/external/sdd-loop-driver/SKILL.md`（+ references/ 两份手册）。

## 加载与投递

skill 本体是**自包含手册**（SKILL.md + references/），三种投递形态等价——宿主技能目录安装、提示词内嵌/粘贴、文件路径引用；不依赖任何下载或安装机制。宿主 agent **不需要安装 spec-kit**。

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
- 投递后宿主按手册驱动循环：断点探测 → 阶段派发（脱离模式后台自跑 + 定时间隔检查）→ 哨兵与独立校验 → 续环 → git 状态判定合并收尾。
- **目标项目侧依赖**：仅当子代理要在目标项目执行 `/speckit.*` 阶段命令时，目标项目才需要具备 `.specify/` 结构；目标项目无 `.specify/` 时机制报告停线、不自动初始化。

## 机制归属（Feature 060 委派化）

驱动子代理的公用机制已上收，本技能保留编排本体：

- **前置检查（五族）与失败处置链**：权威落点 `skills/internal/run-agent/references/dispatch-preflight.md`（本技能引用）。
- **反嵌套义务**：权威落点 run-agent 派发治理 + `shared/definitions/subagent-definitions.md`（本技能 Driver Topology 节保留循环视角自检行）。
- **通用派发配方**（断点探测/提示词落盘/runner/本地变体）：`shared/workflow/external-dispatch-recipes.md`；本技能保留差异面——心跳机制、nohup 脱离形态权威落点、阶段链与收尾编排。
- **实例创建**：经 create-agent（`agents/sdd-executor.agent.md` 模板 → 职责实例）。

## 边界

- push / 远程分支操作维持破坏性确认门控（缺省本地合并）。
- 不改变各阶段命令内部流程；不为变体新增机制分支。
- 多线并行时的并发隔离与窄读法授权纪律见 skill 手册 `references/stage-prompts.md`。
