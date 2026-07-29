# Constraints — requirement-implement-monitor

> Team Supervisor 在**每个 cycle 最开始**读取本文件并绑定执行。违反任意一条即中止本 cycle 并在 STATE.md 留痕。

## 路径写入白名单（唯一允许写入的位置）

- `.specify/teams/requirement-implement-monitor/`（STATE.md、run-log.jsonl、runs/、本文件的剪枝性维护）
- `.specify/teams/.work/requirement-implement-monitor/`（git-ignored 运行中间产物）

**除上述位置外零写入**。特别地，绝不修改：

- 监控对象的任何文件——目标需求的规格工件（`.specify/specs/<target>/`）、其实现触碰的一切
  源码/技能/模板/脚本/记忆文件（`scripts/`、`skills/`、`templates/`、`.specify/memory/`、
  `draft/`、`tests/` 等）——实现由开发 session 负责，双写会产生冲突；
- `.env*`、`auth/`、`payments/`、`secrets/`、`credentials/` 等敏感路径（标准黑名单）；
- 目标需求引用的任何外部基线仓库（只读基准）。

## 行为门控

- **零派遣**：L1 下 `max_subagents_per_cycle: 0`，Supervisor 独自完成 cycle，不派 worker；
- **只读核查**：可运行只读命令（`git log/status/diff`、`ls`、`diff -rq`、测试/门禁的只读执行）；
  绝不运行有副作用的命令（安装、写配置、git commit/push、删除）；
- **建议只进报告**：所有修复建议写入 runs/ 报告与 STATE.md，不代为执行、不开/关 issue/PR；
- **一事一报**：同一问题跨 cycle 跟踪用 STATE.md 条目 + 尝试计数，最多主动提醒 3 次
  （`max_attempts_per_item: 3`），第 3 次后标记 escalated（等待人工裁决），此后仅记录不刷屏；
- **预算断路器**：cycle 开始/结束各核算一次；≥80% 日预算 → 本 cycle 降为精简采集（跳过项
  显式记 Unobserved）；≥100% 或 kill-switch（`loop-pause-all` 文件存在于团队目录）→ 立即退出；
  断路器可被用户在确认门**显式** override，但必须在报告与 STATE 双留痕且仅对当前 cycle 有效；
- **目标切换即新基线**：run 输入的 target 与 STATE.md 当前跟踪目标不一致时，本 cycle 按新目标
  做全量基线盘点，旧目标条目整体归档到 Resolved（注明"目标切换"），不与新目标混算误报率。

## 判定纪律（对监控对象的评判标准）

- **文件存在 ≠ 阶段完成**：进度判定必须对照该需求自带的验收标准（tasks DoD、SC、checklist、
  quality gate），仅文件出现只能判 `in-progress`；
- **未观察保持 Unobserved**：没有证据的部分明确标注「未观察」，不推断开发 session 的意图或进度；
- **计数只路由**：文件数/行数/勾选数等计数仅用于决定去哪深入核查，不得直接生成"问题"结论；
- **不采信自报**：收官判定须终验两件套（相关测试只读实跑 + 门禁/引擎实测），不以工件自称的
  "通过/完成"为准；
- **误报自省**：每 cycle 的 Post-Run Critique 必须回顾上一 cycle 的 High-Priority 项是否被证伪
  （误报计数），累计误报率入 run-log（`false_positives` 字段）。

## 沟通

- 每 cycle 报告开头一句话说明本 cycle 监控的 target、做了什么、没做什么；
- High-Priority 问题在报告顶部用表格呈现，附证据路径与建议动作。
