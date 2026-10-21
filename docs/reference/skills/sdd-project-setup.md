# sdd-project-setup（SDD 项目框架调协）

**机制一句话**：把目标项目（本地或远端）以调协模式推进到 spec-kit 框架预期的最佳状态——先确定性盘点定缺口，再按需调协，最终验证就绪，产出候选工作清单供下一步选用。真源：`skills/external/sdd-project-setup/SKILL.md`（+ `references/setup-recipes.md`、`scripts/mechanism-inventory.py`）。

## 加载与投递

skill 本体是**自包含手册**（SKILL.md + references/ + scripts/），任何宿主 agent 可直接加载；宿主 agent **不需要安装 spec-kit**（宿主侧只要求具备 `specify` CLI 或对应 agent 的命令执行能力，见边界）。加载话术：「初始化 spec-kit」「项目接入 SDD」「框架就绪检查」「调协项目框架」，或 sdd-loop-driver 的 preflight 发现目标项目无 `.specify/` 或机制退化时自动 handoff。

## 三模式实例化（入口参数清单）

| 参数 | 取值 | 说明 |
|------|------|------|
| 目标项目 | 本地路径，或 `ssh <alias>` + 运行用户 + 项目目录；**路径与 host 都未给 → 当前项目**（git 根，非 git 仓库取工作目录） | 远端形态参数与 sdd-loop-driver 一致 |
| 执行拓扑 / 子代理承载 | 无 host → 本地：编排者直执或宿主**原生子代理**（不启动 `qodercli`）；远端三元组给全 → run-agent 派发外部 agent CLI | 只给 host 或三元组不完整 → 问一个澄清问题，不猜 |
| 模式 | `install`（全新安装）/ `refresh`（刷新既有）/ `verify`（只读核查） | 未给时按 S1 分级：absent=install、degraded/partial=refresh、complete=verify；委派时缺失=install、退化=refresh |
| 目标 AI 工具 | qoder / claude / codex / opencode / hermes / copilot | 未给时 `all`；`specify init --ai <tool>` 的取值 |

## 五步循环（S0–S5）

```text
S0 ENTRY     目标、模式、目标工具（一遍性入口）
S1 ASSESS    mechanism-inventory.py 扫描 .specify/ → 机制矩阵 13 维度
             + 状态分级（absent / degraded / partial / complete）
S2 INSTALL   absent → specify init . --here --ai <tool>；
             partial/degraded → /speckit.instructions 刷新（recover 模式）
S3 RECONCILE 按缺口按需逐项：constitution → sanitize → feature →
             instructions → docs（次序固定、只执行缺项、不整建）
S3+ STRENGTHEN 强化序列（机制就绪后的增值建设，按需逐项）：
             history → docs 深化 → research → feature 特性生成 →
             goal（定义 3–5 个项目目标）
S4 VERIFY    五族前置检查 + 宿主 hook 体检 + 机制矩阵复扫 + 兼容符号链接核验，
             全绿才算完成
S5 SUGGEST   候选工作清单（未完成 feature / 大改进 feedback / TODO 事项）
```

- **指令体积预算**：S3 的 `/speckit.instructions` 后读取生成器 `BUDGET` 报告；超预算先走 `manage-instructions` 的 R1/R2，仍超时按 `setup-recipes.md` § S3.4 的 R3 回退外迁 project-filled 大章节；无法收敛时列为 pending（预算上调/拆分章节），不静默转述告警。
- **宿主 hook 体检**：S4 运行 `scripts/hook-health.py`，检出会在每次工具调用同步阻塞的 hook（工具事件 + `async` 未开 + timeout ≤5s）。普通同步 hook 由 `--fix` 置 `async: true`（写前备份）；带 `_*_managed` 标记或落在自愈遥测路径（AITrace/r2c、yunke、loongsuite、a1）的 vendor hook 会被其 agent 秒级回写，脚本只报告并给出处置选项。退出码 `0` 干净/已修复、`10` 有未解决风险（登记未处理清单）、`2` 参数错误；verify 模式只读。
- **本地拓扑前置检查**：① SSH、② 运行用户、③ 子代理 CLI 不适用（无 `ssh`/`su`/外部 CLI），逐项记 `n/a`；只核对 ④ LLM 配置与 ⑤ spec-kit 可用性。远端拓扑五族全查。

## 执行侧可移植性

- 宿主环境无需 `.specify/`——盘点脚本只读扫描目标项目，无副作用。
- **目标项目侧依赖**：`install` 模式要求宿主具备 `specify` CLI；既有项目刷新走目标项目内的 `/speckit.instructions`（恢复路径）。
- 状态分级是三态判定而非二态：`.specify/` 存在 ≠ 就绪；S4 三条件（前置检查全 ok + 矩阵达 complete 或缺口已声明 + 符号链接完好）同时成立才判调协完成。

## 与 sdd-loop-driver 的软协同契约

- **非强绑定**：两技能各自可独立运行，互不强依赖。
- **本技能 → sdd-loop-driver**：S5 候选工作清单是建议入口之一（有哪些可做的事），调用与否由用户或上游流程决定。
- **sdd-loop-driver → 本技能**：其 preflight ⑤ 框架检查 fail 时把处置 handoff 过来，处置完成后回到循环。
- 职责切分线：框架调协（install/reconcile/strengthen/verify/候选清单）= 本技能；SDD 完整阶段循环 = sdd-loop-driver。

## 机制归属（Feature 060 委派化）

- **前置检查（五族）与失败处置链**：权威落点 `skills/internal/run-agent/references/dispatch-preflight.md`（本技能 S4 引用，不复写）。
- **通用远端命令形态**：`shared/workflow/external-dispatch-recipes.md`（本技能保留 setup 特有命令：specify init、机制盘点脚本）。
- **治理命令的子代理派发**：本地缺省由编排者直执或宿主**原生子代理**承载（不启动 `qodercli`）；远端经 run-agent 派发外部 agent CLI（可选形态——独立运行时编排者亦可亲自执行）。
- **指令体积预算**：预算常量 owner 是 `scripts/bash/generate-instructions.sh` 的 `INSTRUCTIONS_BUDGET_BYTES`；R1/R2 owner 是 `manage-instructions`；setup 负责触发、验证与 R3 初始化回退。

## 边界

- 不做任何 SDD 阶段推进（requirements 等六阶段归 sdd-loop-driver）；S3 只调用治理类命令。
- verify 模式对 complete 项目：出候选清单即止，不做任何写动作。
- 不 push（除非入口显式授权）；远端形态时既有脏文件不提交不还原。
- 宿主未装 `specify` CLI 且目标项目无 `.specify/`：报告缺口并停止，不自动安装 CLI。
