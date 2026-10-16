# sdd-project-setup（SDD 项目框架调协）

**机制一句话**：把目标项目（本地或远端）以调协模式推进到 spec-kit 框架预期的最佳状态——先确定性盘点定缺口，再按需调协，最终验证就绪，产出候选工作清单供下一步选用。真源：`skills/external/sdd-project-setup/SKILL.md`（+ `references/setup-recipes.md`、`scripts/mechanism-inventory.py`）。

## 加载与投递

skill 本体是**自包含手册**（SKILL.md + references/ + scripts/），任何宿主 agent 可直接加载；宿主 agent **不需要安装 spec-kit**（宿主侧只要求具备 `specify` CLI 或对应 agent 的命令执行能力，见边界）。加载话术：「初始化 spec-kit」「项目接入 SDD」「框架就绪检查」「调协项目框架」，或 sdd-loop-driver 的 preflight 发现目标项目无 `.specify/` 或机制退化时自动 handoff。

## 三模式实例化（入口参数清单）

| 参数 | 取值 | 说明 |
|------|------|------|
| 目标项目 | 本地路径，或 `ssh <alias>` + 运行用户 + 项目目录 | 远端形态参数与 sdd-loop-driver 一致 |
| 模式 | `install`（全新安装）/ `refresh`（刷新既有）/ `verify`（只读核查） | 由 sdd-loop-driver 委派时：缺失=install、退化=refresh |
| 目标 AI 工具 | qoder / claude / codex / opencode / hermes / copilot | `specify init --ai <tool>` 的取值 |

## 五步循环（S0–S5）

```text
S0 ENTRY     目标、模式、目标工具（一遍性入口）
S1 ASSESS    mechanism-inventory.py 扫描 .specify/ → 机制矩阵 13 维度
             + 状态分级（absent / degraded / partial / complete）
S2 INSTALL   absent → specify init . --here --ai <tool>；
             partial/degraded → /speckit.instructions 刷新（recover 模式）
S3 RECONCILE 按缺口按需逐项：constitution → sanitize → feature →
             instructions → docs（次序固定、只执行缺项、不整建）
S4 VERIFY    五族前置检查 + 机制矩阵复扫 + 兼容符号链接核验，全绿才算完成
S5 SUGGEST   候选工作清单（未完成 feature / 大改进 feedback / TODO 事项）
```

## 执行侧可移植性

- 宿主环境无需 `.specify/`——盘点脚本只读扫描目标项目，无副作用。
- **目标项目侧依赖**：`install` 模式要求宿主具备 `specify` CLI；既有项目刷新走目标项目内的 `/speckit.instructions`（恢复路径）。
- 状态分级是三态判定而非二态：`.specify/` 存在 ≠ 就绪；S4 三条件（前置检查全 ok + 矩阵达 complete 或缺口已声明 + 符号链接完好）同时成立才判调协完成。

## 与 sdd-loop-driver 的软协同契约

- **非强绑定**：两技能各自可独立运行，互不强依赖。
- **本技能 → sdd-loop-driver**：S5 候选工作清单是建议入口之一（有哪些可做的事），调用与否由用户或上游流程决定。
- **sdd-loop-driver → 本技能**：其 preflight ⑤ 框架检查 fail 时把处置 handoff 过来，处置完成后回到循环。
- 职责切分线：框架调协（install/reconcile/verify/候选清单）= 本技能；SDD 六阶段循环 = sdd-loop-driver。

## 机制归属（Feature 060 委派化）

- **前置检查（五族）与失败处置链**：权威落点 `skills/internal/run-agent/references/dispatch-preflight.md`（本技能 S4 引用，不复写）。
- **通用远端命令形态**：`shared/workflow/external-dispatch-recipes.md`（本技能保留 setup 特有命令：specify init、机制盘点脚本）。
- **治理命令的子代理派发**：经 run-agent（可选形态——独立运行时编排者亦可亲自执行）。

## 边界

- 不做任何 SDD 阶段推进（requirements 等六阶段归 sdd-loop-driver）；S3 只调用治理类命令。
- verify 模式对 complete 项目：出候选清单即止，不做任何写动作。
- 不 push（除非入口显式授权）；远端形态时既有脏文件不提交不还原。
- 宿主未装 `specify` CLI 且目标项目无 `.specify/`：报告缺口并停止，不自动安装 CLI。
