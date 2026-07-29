# Constraints — bh-port-monitor

> Team Supervisor 在**每个 cycle 最开始**读取本文件并绑定执行。违反任意一条即中止本 cycle 并在 STATE.md 留痕。

## 路径写入白名单（唯一允许写入的位置）

- `.specify/teams/bh-port-monitor/`（STATE.md、run-log.jsonl、runs/、本文件的剪枝性维护）
- `.specify/teams/.work/bh-port-monitor/`（git-ignored 运行中间产物）

**除上述位置外零写入**。特别地，绝不修改：

- 监控对象的任何文件（`scripts/`、`skills/`、`templates/`、`.specify/specs/034-evidence-infra/`、
  `.specify/memory/`、`draft/`、`tests/` 等）——开发由另一 session 负责，双写会产生冲突；
- `.env*`、`auth/`、`payments/`、`secrets/`、`credentials/` 等敏感路径（标准黑名单）；
- `/cws_work/better-harness`（上游仓库，只读基线）。

## 行为门控

- **零派遣**：L1 下 `max_subagents_per_cycle: 0`，Supervisor 独自完成 cycle，不派 worker；
- **只读核查**：可运行只读命令（`git log/status/diff`、`ls`、`diff -rq`、`node --test`/`pytest` 只读执行）；
  绝不运行有副作用的命令（安装、写配置、git commit/push、删除）；
- **建议只进报告**：所有修复建议写入 runs/ 报告与 STATE.md，不代为执行、不开/关 issue/PR；
- **一事一报**：同一问题跨 cycle 跟踪用 STATE.md 条目 + 尝试计数，最多提醒 3 次（`max_attempts_per_item: 3`），
  第 3 次后标记 escalated（等待人工裁决），不再重复刷屏；
- **预算断路器**：cycle 开始/结束各核算一次；≥80% 日预算 → 本 cycle 降 report-only（L1 本身即 report-only，
  则降为最小早退报告）；≥100% 或 kill-switch（`loop-pause-all` 文件存在于团队目录）→ 立即退出。

## 判定纪律（对监控对象的评判标准，与移植方案四纪律对齐）

- **文件存在 ≠ 阶段完成**：P1–P7 进度判定必须对照方案中该阶段的**验收标准**（测试通过、产物合法等），
  仅文件出现只能判 `in-progress`；
- **未观察保持 Unobserved**：没有证据的部分明确标注「未观察」，不推断另一 session 的意图或进度；
- **计数只路由**：文件数/行数等计数仅用于决定去哪深入核查，不得直接生成"问题"结论；
- **误报自省**：每 cycle 的 Post-Run Critique 必须回顾上一 cycle 的 High-Priority 项是否被证伪（误报计数）。

## 沟通

- 每 cycle 报告开头一句话说明本 cycle 做了什么、没做什么；
- High-Priority 问题在报告顶部用表格呈现，附证据路径与建议动作。
