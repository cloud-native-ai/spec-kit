---
id: "20260831T121146Z-speckit-feedback"
unit_id: "/speckit.feedback"
unit_type: "command"
run_id: "mode4-consume:20260831T101500Z"
scope: "local"
probe: "speckit-feedback-wrapup"
kind: "internal"
slice: "commands"
partial: false
created: "2026-08-31T12:11:46Z"
summary: "Mode 4 消费闭环完成:框架门通过(.specify/templates + skills + src/specify_cli 齐备),按批处理纪律把 3 个包 46 条作为一批统一处理——2 个独立客户项目(ai-tracing @cc38cf3e 17 条、cli-auth @90c18a65 6 条)+ 框架自用包 23 条(含已 confirmed 的自省报告,其 14 个问题的核验结"
---

## Review
Mode 4 消费闭环完成:框架门通过(.specify/templates + skills + src/specify_cli 齐备),按批处理纪律把 3 个包 46 条作为一批统一处理——2 个独立客户项目(ai-tracing @cc38cf3e 17 条、cli-auth @90c18a65 6 条)+ 框架自用包 23 条(含已 confirmed 的自省报告,其 14 个问题的核验结论按命令规定直接采信,未重复核验)。用户授权后把自用包从发件箱移入收件目录并入这批。读取以 3 个并行子代理分组完成,每条主张都要求 path:line 锚点与 FRAMEWORK/NOT-OURS 标签,避免把客户自身代码问题当框架问题上行。跨包对账产出:5 处跨不同上报者的复发(review.md §4.5 三包命中同一段落、tasks-template GATE runner 与 clarify 提问矛盾各两个独立客户、clarify-taxonomy:80 与 implement.md:53 各两包命中同一行),以及 5 条经源码证伪的上报主张(QWEN.md 符号链接登记、run-tests.sh 不存在、plan 门两选项皆不可用、Feedback/Documentation 顺序未固定、create-docs Hugo)。用户选择 7 项全做直修:review.md 三补、tasks-template 去框架专属 runner、clarify 批量提问规则、clarify-taxonomy 调和分支、implement 归因两轴、docs-utils --allow-special 扩展钩子、constitution 陈旧路径。验证:新 flag 做了行为实测(未传 flag 仍报 QWEN.md、传了不报、同时 DESIGN.md 仍被拦——证明没有把检查变哑),regen-command-copies 与 sync-mirrors --write 均 exit 0、mirror --check 全绿,contract 全量 21→21 零新增失败。6 项系统性发现记为 requirements-candidate,6 项维持自省的 local-sink 分流。原子清理:3 个包全删(含一个 root 所有的孤本,已事先向用户提示风险并获授权),consume-log 留一行含路由与裁决。零网络行为。优化点见 points。

## Optimization Points
- **MANIFEST 里带着上报者的安装版本，Mode 4 却从不使用它**：每个包的 MANIFEST 都有 `Install source: <repo> @ <sha>`（本批两个客户包分别停在 `cc38cf3e` 与 `90c18a65`，框架自用包在 HEAD）。但 Mode 4 的步骤 1-3 完全没有"按上报者安装版本判定主张时效性"的动作——步骤 2 只说收集 `unit_id/probe/slice/run_id/Review/Optimization Points`。后果很实：上报者停在旧提交时，他们的抱怨可能早已在 HEAD 修好，若不先算版本差就会把已修问题当未修上行/返修。本轮是我自己想到才给每个子代理带上"你们的上报者停在 X、当前 HEAD 已前进"的上下文，才拿到 3 条 `already-fixed` 判定（例如 create-docs 的 Hugo 抱怨在 create-docs/create-pages 拆分后已过时）。建议步骤 2 增一条固定动作：从 MANIFEST 取 `@ <sha>`，先算 `<sha>..HEAD` 的变更文件面，把落在该面内的主张标为"可能已修，须核"，落在面外的标为"版本未触碰，抱怨大概率仍成立"——这是纯确定性计算（`git diff --name-only`），完全符合 Program-First。
- **步骤 4 把"删包"写成无条件收尾，却没有"这是不是孤本"的判据**：本批三个包里，`feedback-20260831T092908Z.zip` 是 root 所有、由一个并发进程在我运行期间投递、未被 git 跟踪的**孤本**；另两个一个已在 git 历史中、一个是我自己刚打的（内容仍可从存储与历史重建）。命令对三者一视同仁地要求删除，只靠 consume-log 行留痕。我不得不自己停下来把这个风险提示给用户。建议步骤 4 增一条删除前判据：对每个包判定是否存在第二副本（git 跟踪或历史中可取、或同内容条目仍在活跃存储），**孤本必须在 consume report 里显式点名并单独确认**，不与已入库包同等处理；判定本身是 `git log --all --oneline -- <path>` 级别的确定性检查。
- **冲突裁决的产出没有回流通道，同一错误主张会被反复上报**：本轮 5 条上报主张经源码证伪，其中"QWEN.md 是框架强制的兼容符号链接、已在 Symlink Model 中登记"这类主张会直接误导后续修复方向（真相：`AGENT_CONFIG` 与 `symlink-model.md` 都没有它，`tests/contract/test_export_skill_genericity.py:63` 反而要求 qwen 名不存在）。但裁决结论只写进 `consume-log.md` 与本轮 report，都留在消费侧；上报方永远收不到"你这条被证伪了、原因是 X"。路由表里的 `Acknowledge only` 也是记在消费侧的。下一批同一上报者极可能再报一次同样的错主张，而消费方要重新花一次取证成本。建议步骤 3 增一条可选产出：把证伪与 already-fixed 结论按上报者聚合成一份本地"回执摘要"文件（人工投递，零网络，与红线一致），使 Loop A 从单向上行变成双向对账。
