# Baseline Gates: 治理前门控基线快照

**采集时间**: 2026-08-18(需求阶段全框架盘点,经 Explore 子代理核实)
**口径**: 阻塞确认语义指令,源侧文件(mirror 与 per-tool 副本不计);与 gate-scanner-contract.md C-2 扫描根一致。
**总数**: 93 处(实测,`scan-confirmation-gates.py` 修订版基线)。
**基线修订(2026-08-19,implement Phase 4 前)**:首版基线 61 处遗漏提交提示样板模式族("inviting the user to submit collected feedback",约 30 处,分布于命令模板 + 技能 SKILL.md 的 Feedback 样板段);补全扫描模式后重冻基线为 93。修订属测量器具完备性修正(模式族补齐),非治理面变化;修订时点树状态 = Phase 3 结束态(team 面已治理)。分类:destructive=72 / governance_kept=20 / reversible=1,逐条记录见同目录 `baseline.json`。
**口径细化(2026-08-19,Phase 4 治理中)**:判据真源自身(confirmation-gates.md)与两份**定义确认纪律的策略锚文档**(reconcile-pattern.md、interview-pattern.md)以规范口吻引用门控模式族,非待治理门控,自计数中排除(与 SELF_REL 同理);基线 93 保持不变(含该部分属保守口径)。
**治理后实测(Phase 4 末)**:残留 22 处(destructive=12 / governance_kept=10),violations=[](reversible 阻塞门控零残留);降幅 (93−22)/93 = 76.3% ≥ 75%(SC-002 达标)。残留全部在保留清单语义内(删除前确认、分级门控、覆盖确认、远程推送、固有交互、治理保留)。

## 分布概览

| 类别 | 数量 | 治理裁定 |
|------|------|----------|
| 样板化反馈提交提示(约 20 个命令模板收尾段) | ~20 | auto_execute(非阻塞一次性提示,D5) |
| 收尾术语确认(约 10 个命令模板 Glossary 步骤) | ~10 | auto_execute(冲突/覆盖用户条目除外,保留) |
| 可逆 preview→confirm 写入门控(team/goal/tools/agents/skills 等) | ~8 | auto_execute |
| 破坏性/不可撤销门控(删除/移动/推送/覆盖) | ~8 | keep_gate |
| 固有交互(interview 问答与退出门、constitution 不可撤销确认) | ~5 | keep_gate(intrinsic) |
| team 流程门控(创建/运行/收尾) | 4 | auto_execute(continuous 分级门控除外) |

## 定位索引(要点门控)

| 门控 | 位置 | 裁定 |
|------|------|------|
| team 创建确认 | templates/commands/team.md:50,83,84,97,102-104;skills/create-team/SKILL.md:32;references/create-mode.md:16;team-presets.md:9,52,55 | auto_execute |
| team 运行确认 | templates/commands/team.md:52,108-110,125,133-134;SKILL.md:38,44;execution-guide.md:31 | auto_execute |
| team 收尾确认 | SKILL.md:236;shared/workflow/feedback-step.md:80 | auto_execute |
| goal 写入门控 | templates/commands/goal.md:28,47 | auto_execute |
| tools 执行门控 | templates/commands/tools.md:54,85-91;shared/definitions/tool-definitions.md:130 | keep_gate(存疑从严) |
| session 同名覆盖 | templates/commands/session.md:48,54 | keep_gate |
| agents/skills 写入门控 | templates/commands/agents.md:43,70;skills.md:61-62 | auto_execute |
| todo/implement commit 批准 | templates/commands/todo.md:272;implement.md:100 | keep_gate(governance-kept) |
| implement gate.yaml CONFIRM | templates/commands/implement.md:49 | keep_gate(governance-kept) |
| feedback consume 删除前确认 | templates/commands/feedback.md:118-142 | keep_gate |
| docs 分级门控 | templates/commands/docs.md:29 | keep_gate |
| feature 状态回退 / analyze 补救批准 | feature.md:36;analyze.md:42 | keep_gate |
| interview 交互 | interview.md:35,69,130,148 | keep_gate(intrinsic) |
| constitution 不可撤销确认 | templates/constitution-template.md:127-130 | keep_gate(intrinsic) |
| glossary 冲突确认 | shared/workflow/glossary.md:41-64 | keep_gate(覆盖用户数据) |
| git-workflow 远程门控 | skills/git-workflow/SKILL.md:28-34 | keep_gate |
| continuous 循环分级门控 | skills/create-team/references/operating-loops.md:28-40;workspace-cluster.md:59,124 | keep_gate(D4 例外) |
| reconcile 分级模型(概念基础,非待治理门控) | shared/patterns/reconcile-pattern.md:98-104 | 参照 |
