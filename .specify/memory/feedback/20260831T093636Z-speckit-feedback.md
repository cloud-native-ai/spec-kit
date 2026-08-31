---
id: "20260831T093636Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "mode5-introspect-then-mode2-package:20260831T093456Z"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-08-31T09:36:36Z"
summary: "本次运行按用户选择走 Mode 5 自省 → Mode 2 打包 → 清理的完整闭环。范围为 23 条 open 内部条目(零外部条目)。自省阶段以 6 个并行子代理分组回到真实场景核验每条 point,产出 14 个问题(每个含五要素与 path:line 证据锚点)与 5 条排除项(1 条纯门控观察 + 4 条自述无优化点),按根因分区覆盖全部 23 条;核验结论分布为成立/部分成立/不成立三"
---

## Review
本次运行按用户选择走 Mode 5 自省 → Mode 2 打包 → 清理的完整闭环。范围为 23 条 open 内部条目(零外部条目)。自省阶段以 6 个并行子代理分组回到真实场景核验每条 point,产出 14 个问题(每个含五要素与 path:line 证据锚点)与 5 条排除项(1 条纯门控观察 + 4 条自述无优化点),按根因分区覆盖全部 23 条;核验结论分布为成立/部分成立/不成立三类,其中 3 条经核实已被 047 自身实现闭合、故不再作为问题上行,只以'条目 schema 缺本轮已修状态'这一元发现上行。register 结构校验一次通过,用户确认后 18 条置 processed、5 条排除项另行置 ignored,报告转 confirmed。打包 23 条并以 --include-introspection 把报告一并入包(实测 zip 内含 25 个文件,报告在 introspection/ 子目录),dry-run 预览后执行清理:23 条移出活跃存储、cleanup-log 逐条留痕、报告与 zip 保留。三条本轮亲历的第一手佐证(origin 硬编码拉错源、.migration-backups 复发使契约测试变红、sync-mirrors 镜像副本 REPO_ROOT 误解析)被写进对应问题,使其不再是转述而是可复现事实。红线遵守:零网络行为、未自动传输、未运行 mark-submitted(包未投递)。优化点见 points。

## Optimization Points
- **Mode 5 步骤 1 的「摘要投影」拿不到自省真正的分析对象**：步骤 1 规定用 `--action list --disposition open --format json` 取条目摘要投影，但该投影的字段里没有 `## Optimization Points`（只有 200 字截断的 `summary`，且 `make_summary` 在 `scripts/python/feedback-utils.py:86-91` 是硬截断、句子被切在中途）。而自省要核验的恰恰是每个 point。结果是步骤 1 的投影只能用来划范围，真正的分析必须落到逐文件读原文——本轮 23 个条目是靠 6 个并行子代理分组读文件才拿到的。命令面没有为这一步给出「既取到 points 又不违反摘要优先」的路径。建议二选一并写进步骤 1：给引擎补一个 points 投影（`--action list --project points`，只回 unit_id + 每条 point 首句），或在步骤 2 明确「points 是分析目标本身，属摘要优先的记名例外，但 MUST 分组委派给子代理读取而非全量注入主上下文」。
- **报告 schema 的「一个条目只能进一个问题」约束与真实条目形态冲突，且事前无任何提示**：引擎在 `scripts/python/feedback-utils.py:480-481` 强制 `len(members) != len(set(members))` 即违规（V-1 跨问题重复成员），同时 `:476` 要求 members ∪ excluded 恰好等于 scope_entries。但真实条目普遍是「一条目多点、各点根因不同」——本轮 23 条里至少 4 条如此（improve-skills 的 20260820T062957Z 一条含 4 个点分属 3 个根因族；implement 的 20260824T054639Z 两个点分属归因轴与脚本缺陷）。约束逼迫把次要根因塞进 `优化方案` 散文里，证据链因此变细。更麻烦的是：Mode 5 步骤 3 与 `contracts/introspection-report.md` 都没写这条约束，我是在动手写报告前去读引擎源码才发现的，否则会在 register 阶段吃 V-1 拒绝并返工整份报告。建议步骤 3 明写「按条目分区，不是按点分区；一个条目的多个点须择其主根因归属，次要根因在优化方案中标注」，契约文档同步补一条 C 编号。
- **cleanup 与 mark-submitted 的归零语义重叠，导致「未投递却已归零」**：Mode 2 第 5 步把 cleanup 定为打包运行的默认收尾，第 6 步才是投递后的 `mark-submitted`。但 cleanup 把条目移出存储后，counter 自然归零——本轮实测 `--action status` 从 `count_since_submission: 23` 直接变成 `0`，而 `submitted_at` 仍是 `null`。也就是说：包还躺在发件箱里没送出，计数器已经归零，第 6 步的 mark-submitted 变成一个不改变任何可观察状态的空动作。这让「阈值提示」失去了对未投递批次的记忆能力：下一批反馈从 0 起算，无法区分「已投递」与「打完包忘了送」。建议把 counter 与条目存在性解耦（counter 由 submitted_at 与打包记录共同决定），或在第 5 步明确「cleanup 即归零，mark-submitted 仅补记投递时间」，并在包未投递时于状态输出里保留一个 `pending_delivery` 标记。
