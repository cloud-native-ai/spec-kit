# Constraints — cws-workspace-cluster

集群运营的硬性约束。每个 cycle 开始时读取本文件；违反项一律 REJECT，不得"顺手处理"。

## 一、写入边界（最高优先级）

- **对被守护仓库零写入**。本 loop 只写自己的团队目录（`runs/`、`STATE.md`、`run-log.jsonl`）与
  git-ignored 的 run workspace `.specify/teams/.work/cws-workspace-cluster/`。
- 任何 `git commit` / `git push` / `git checkout` / 文件编辑，落在 11 个 folder 中的任何一个，都是**越界**。
- **写操作三级分类**：`read-only` / `mutate-local` / `mutate-cloud`。本 loop 在 L1 只允许 `read-only`；
  `mutate-cloud` 永久强制人工确认并留痕。

## 二、集群定义源

- **`/cws_work/work.code-workspace` 是唯一集群定义源** —— 不另建 roster 配置；folder 的增减即成员的增减。
- workspace 混用相对路径与绝对路径：**相对路径以 workspace 文件所在目录 `/cws_work` 为基准解析**。
  （实测：`spec-kit`、`loop-engineering`、`ai-website-cloner-template`、`better-harness` 为相对；其余为绝对。）
- 每 cycle 必须 diff folders 与 STATE.md 中上轮 roster，**不依赖记忆**判断成员增减。

## 三、子模块

- 当前 11 个仓库**均无 `.gitmodules`**（2026-07-30 实测）。
- 子模块拦截规则**保留声明**：一旦任何 folder 出现子模块边，对子模块工作区副本的直接修改必须被拦截，
  改走"上游提交 → fetch+checkout → gitlink bump"管线。

## 四、证据纪律

- **主 Agent 不轻信 subAgent**：根因结论必须附证据；证据类型不匹配的结论一律打回重做。
  例：判定"网络问题"必须附连通性证据；判定"构建产物过期"必须附源码 HEAD/mtime 与产物特征串比对。
- 每条进度/问题结论必须附**证据路径**。无证据的结论不得进报告。

## 五、已知环境限制（预登记的"已知预期失败"）

这些**不是缺陷**，报告中必须归类为"环境限制"：

| 现象 | 归类原因 |
|------|----------|
| `spec-kit` 工作区大量未提交改动（实测 44 项） | 正在进行中的开发工作，非异常 |
| `better-harness` 工作区大量未提交改动（实测 488 项） | 已知的大批量工作区状态，非异常 |
| `OpenSpec` / `superpowers` / `claude-code-py` 各 1 项脏改动 | 轻微在途改动，非异常 |
| 分支名不统一（`main` × 8 / `master` × 3） | 各仓上游历史差异，非本集群可裁决；仅报告不判错 |
| 无 SSH key 导致的 fetch/publickey 失败 | 执行用户凭证限制，非仓库异常 |
| `refresh-tools.sh --help` 退出码 1 | 该脚本设计如此；预检应用 `--project --json` |

## 六、预算与熔断

- `max_cycles_per_day: 6`；`max_subagents_per_cycle: 0`（L1 不派遣）。
- 预算达 80% → `report-only` 降级；达 100% 或 kill-switch 触发 → `halt`。
- kill-switch：`loop-pause-all`。

## 七、晋级条件（L1 → L2）

在累积足够 cycle 的误报率数据、且 High-Priority 误报率 < 20% 之前，**不得晋级**。
晋级后方可并行派发 repo-analyst，并启用独立 verifier（默认 REJECT 无证据结论）。

## 八、零上下文可接手

团队目录（`team.md` / `constraints.md` / `STATE.md`）必须自足到**另一个 Agent 无任何会话上下文即可接管运营**。
