# Contract: Team Flow(团队流程零确认)

**改写面**: `templates/commands/team.md`、`skills/create-team/SKILL.md` + `references/create-mode.md` / `team-presets.md` / `execution-guide.md` / `summary-mapping.md`、`shared/workflow/feedback-step.md`
**溯源**: FR-004、FR-005、FR-006、FR-009;澄清会话 2026-08-18(continuous 例外、提交提示形态)

## C-1 创建零确认

`/speckit.team` create 与 create-team 技能 MUST 在生成定义后直接落盘 `team.md`;落盘前 MUST NOT 出现"等待用户确认后才持久化"的指令。goal-based create 分支的目标分解提案经 `/speckit.goal targets --add` 核准的流程语义不变,但提案呈现 MUST NOT 作为落盘前的阻塞确认。

## C-2 运行零确认

`/speckit.team` run MUST 按定义直接启动执行;"MUST NOT execute before confirmation"类指令 MUST 从一次性协作模式(parallel / serial / iteration)的流程中移除。

## C-3 continuous 例外

持续循环类(continuous / operating loop)运行 MUST 保留 `references/operating-loops.md` 与 `workspace-cluster.md` 中既有分级门控,本契约 MUST NOT 改写这两个文件中的门控条文。

## C-4 收尾自动化

team 运行结束后的收尾动作(总结、反馈记录等)MUST 自动完成,MUST NOT 以用户确认为前置。达阈值反馈提交提示 MUST 以收尾报告内一行非阻塞提示形态呈现(附 `feedback-utils.py --action package` 提交途径),MUST NOT 阻塞收尾,MUST NOT 触发任何自动传输。

## C-5 落盘后呈现

创建落盘后 MUST 向用户呈现定义内容与修改途径(如 `/speckit.team` modify、improve-team 技能);运行启动后与收尾完成时 MUST 按 execution-report-contract 输出执行报告。

## C-6 team 触发的技能调用非交互

team run 派发调用的技能 MUST 保持非交互(既有 summary-mapping.md 约束不变);本契约移除的确认门控 MUST NOT 以其他交互形态(选择菜单、二次提问)回流。

## C-7 副本传播

team.md 改写 MUST 经 regen-command-copies.py 再生全部 per-tool 副本;create-team 技能改写 MUST 经 sync-mirrors.py 同步 `.specify/skills/create-team/`;手工同步副本视为违约。
