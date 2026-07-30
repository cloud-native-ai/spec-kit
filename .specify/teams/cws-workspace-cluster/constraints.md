# Constraints — cws-workspace-cluster（参考项目洞察收割）

集群分析的硬性约束。每个 cycle 开始时读取本文件；违反项一律 REJECT，不得"顺手处理"。

## 〇、目标切换基线规则

- 团队 goal 于 2026-07-30 由"git 一致性守护"重定义为"参考项目洞察收割、反哺 spec-kit"。
- 旧目标的误报率等晋级判据**清零重计**；旧 runs 报告保留为血统，不作为新目标的证据。

## 一、写入边界（最高优先级）

- **对全部被分析仓库零写入**（10 个参考仓 + spec-kit 本体均不改动）。本 loop 只写自己的团队目录
  （`runs/`、`STATE.md`、`run-log.jsonl`）与 git-ignored 的 run workspace
  `.specify/teams/.work/cws-workspace-cluster/`。
- 任何 `git` 写操作或文件编辑，落在任一被分析仓或 spec-kit 业务文件上，都是**越界**。
- **对 spec-kit 的改进点只进建议清单**，一律交人决策；L1 报告态下不自动采纳。

## 二、集群定义源与花名册规则

- **`/cws_work/work.code-workspace` 是唯一集群定义源**；分析花名册 = `folders` − `home_project`。
- `home_project: /cws_work/spec-kit` 是受益方与对照基线，**不作为被分析对象**。
- 相对路径以 workspace 文件所在目录 `/cws_work` 为基准解析。
- 每 cycle 必须 diff folders 与 STATE.md 中上轮 roster，**不依赖记忆**判断成员增减。

## 三、subAgent 派发纪律（L1 下允许只读分析派发）

- 本团队 L1 的"报告态"指**不改任何交付物**；只读分析类 subAgent 派发是允许的
  （budget: `max_subagents_per_cycle: 11`）。
- 每个 repo-analyst 注入：仓库路径 + 只读边界声明 + 统一输出 schema + spec-kit 基线摘要。
- subAgent 输出必须是结构化档案（定位/架构/独到机制/可迁移点），每条机制性结论附**证据路径**。

## 四、证据纪律

- **主 Agent 不轻信 subAgent**："独到机制"类结论必须附来源文件路径；抽查不达标一律打回重做。
- 每条可采纳改进点必须同时具备：来源仓库、证据路径、spec-kit 具体落点、成本档位（小/中/大）。
- 无证据路径的洞察不得进报告。

## 五、已知环境限制（预登记）

| 现象 | 归类原因 |
|------|----------|
| 参考仓工作区存在 `.qoder/` 等未跟踪目录 | agent 会话副作用，非分析对象 |
| 无 SSH key 场景下 fetch 失败 | 执行用户凭证限制；分析基于本地已 checkout 内容即可 |
| 参考仓非最新（落后 origin） | 分析仍有效；报告中注明所据 HEAD |

## 六、预算与熔断

- `max_cycles_per_day: 2`；`max_subagents_per_cycle: 11`（10 analyst + 1 synthesizer）。
- 预算达 80% → `report-only` 降级（跳过高成本深读，标注 skipped(budget)）；达 100% 或
  kill-switch 触发 → `halt`。
- kill-switch：`loop-pause-all`。

## 七、晋级条件（L1 → L2）

- L2 语义：允许把"小而明确"的采纳建议做成**草稿改动**（如 spec-kit 内新建 draft 文件/PR 草稿）供人审。
- 晋级前提：连续 ≥2 cycle 的洞察低价值率（被人判为无用/重复的占比）< 20%；独立验证者就绪；
  本 constraints 已补齐 spec-kit 侧路径黑名单。

## 八、零上下文可接手

团队目录（`team.md` / `constraints.md` / `STATE.md`）必须自足到**另一个 Agent 无任何会话上下文即可接管运营**。
