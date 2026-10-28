# sdd-project-setup（SDD 项目框架 bootstrap）

**机制一句话**：把目标项目（本地或远端）安装或刷新到 `.specify/` 基线，完成 constitution 与首批内容（feature/docs/goal/agents/team 按需），然后把周期性调协、强化、验证、记录回收与候选清单 handoff 给 `sdd-house-keeping`。真源：`skills/external/sdd-project-setup/SKILL.md`（+ `references/setup-recipes.md`、`scripts/`）。

## 加载与投递

skill 本体是**自包含手册**（SKILL.md + references/ + scripts/），任何宿主 agent 可直接加载；宿主 agent **不需要安装 spec-kit**。加载话术：「初始化 spec-kit」「项目接入 SDD」「框架就绪检查」「调协项目框架」，或 sdd-loop-driver 的 preflight 发现目标项目无 `.specify/` 或机制退化时自动 handoff。

**项目已初始化且本次只需维护/清理**：直接加载 `sdd-house-keeping`，不要重跑 `specify init`。

## 入口参数

| 参数 | 取值 | 说明 |
|------|------|------|
| 目标项目 | 本地路径，或 `ssh <alias>` + 运行用户 + 项目目录；**未给 → 当前项目**（git 根，非 git 取工作目录） | 目标解析唯一契约：`shared/workflow/target-resolution.md`；setup **不依赖 `.specify/`**，不做向上搜索，缺失时由本技能创建 |
| 执行拓扑 / 子代理承载 | 无 host → 本地：编排者直执或宿主**原生子代理**（不启动 `qodercli`）；远端三元组给全 → run-agent 派发外部 agent CLI | 只给 host 或三元组不完整 → 问一个澄清问题，不猜 |
| 模式 | `install`（全新安装）/ `refresh`（刷新既有）/ `bootstrap-content-check`（只查首批内容） | 未给时按 S1 分级：absent=install、degraded/partial=refresh、complete=bootstrap-content-check |
| 目标 AI 工具 | qoder / claude / codex / opencode / hermes / copilot | 未给时 `all` |

## 循环（S0–S2 + HANDOFF）

```text
S0 ENTRY     目标、模式、目标工具
S1 ASSESS    mechanism-inventory.py（13 维度 + 分级）
             + logical-framework.py（required/recommended/conditional）
S2 INSTALL   absent → specify init；partial/degraded → /speckit.instructions 刷新
S2.5 BOOTSTRAP CONTENT
             constitution（缺）→ feature 种子（缺）→ docs 树（缺）
             → goal 3–5 个（缺）→ agents/team（用户明确需要时）
HANDOFF      调 sdd-house-keeping H0–H4；H4 三条件成立才返回 ready；
             house-keeping 不可用 → bootstrap-complete / maintenance-pending
```

**边界**：setup 不执行 sanitize、retention apply、完整 reconcile、强化、验证或候选清单；这些归 house-keeping H1–H5。

## 预算与 hook health

- **指令体积预算**：S2 刷新若报告 `BUDGET ... over`，setup 不实现 R3；完整 S3.4/R3（`placeholder=yes`、`pending`）归 house-keeping H2 的 Budget convergence。
- **宿主 hook 体检**：`hook-health.py` 与 `S4-H` 归 house-keeping H4；`vendor-managed` hook 只报告不自动改。本地拓扑 ①–③ 记 `n/a`，只核对 ④ LLM 配置/⑤ framework 可用性。

## 执行侧可移植性

- 宿主环境无需 `.specify/`——盘点脚本只读扫描目标项目，无副作用。
- **目标项目侧依赖**：`install` 要求执行侧具备 `specify` CLI；既有项目刷新走目标项目内的 `/speckit.instructions`。
- **完成标准**：bootstrap + house-keeping H4 三条件同时成立才判 ready；`.specify/` 存在 ≠ 就绪。

## 三技能软协同

- **非强绑定**：`sdd-project-setup`、`sdd-house-keeping`、`sdd-loop-driver` 各自可独立运行。
- **setup → house-keeping**：bootstrap 完成后 handoff H0–H4；ready 凭证来自 H4。
- **house-keeping → setup**：目标项目缺 `.specify/`/constitution，或 H3 发现 goal/agents/team bootstrap-gap 时回交 setup。
- **setup → sdd-loop-driver**：候选工作清单由 house-keeping H5 提供，是建议而非强制；不携带「必须调用 sdd-loop-driver」的语义。
- **sdd-loop-driver → setup**：preflight ⑤ fail 时 handoff setup 做 bootstrap；bootstrap 完成后再按需 handoff house-keeping 做周期维护。
- **职责切分线**：bootstrap = setup；周期维护 = house-keeping；SDD 阶段循环 = loop-driver。

## 机制归属（Feature 060 委派化）

- **前置检查（五族）与失败处置链**：权威落点 `skills/internal/run-agent/references/dispatch-preflight.md`。
- **通用远端命令形态**：`shared/workflow/external-dispatch-recipes.md`。
- **治理命令的子代理派发**：本地由编排者直执或宿主**原生子代理**承载（不启动 `qodercli`）；远端经 run-agent 派发外部 agent CLI。
- **指令体积预算**：预算常量 owner 是 `scripts/bash/generate-instructions.sh` 的 `INSTRUCTIONS_BUDGET_BYTES`；R1/R2 owner 是 `manage-instructions`；R3 归 house-keeping H2。

## 边界

- 只做 bootstrap：install/refresh + constitution + 首次 feature/docs/goal/agents/team + handoff；不做任何 SDD 阶段推进。
- 不执行破坏性动作；不调用 `/speckit.sanitize`、不调用 retention apply。
- 不 push（除非入口显式授权）；远端形态时既有脏文件不提交不还原。
- 宿主未装 `specify` CLI 且目标项目无 `.specify/`：报告缺口并停止，不自动安装 CLI。
