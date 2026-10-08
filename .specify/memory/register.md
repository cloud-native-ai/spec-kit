# ID Register (编号登记册)

> **本文件是什么**:本仓全部**持久编号标识**的唯一索引 —— 每个编号在**诞生的那一刻**在此登记一行:
> 编号 → 一行含义 → **权威路径**(完整陈述所在,本文件不复述其内容) → 状态。
> 规则 owner:`.specify/instructions.md` § ID Register (编号登记) / 模板源 `templates/instructions-template.md` 同名小节。
> **为什么必须有它**:只活在 session 历史、git-ignored 工作区或对话上下文里的编号,对任何后续 session 均不可解读;
> 引用者却当作已知上下文继续推进 —— 这正是本登记要关闭的静默失效。维护方式:手工(与 glossary 同类),无引擎。

| 编号 | 含义(一行) | 权威路径(完整陈述) | 状态 |
|------|------------|--------------------|------|
| D1–D9 | goal `session-driven-self-improvement` 的 9 轮访谈决策:D1 初版 objective(后被 D7 撤回重述)、D2 满意度判定规则、D3/D6 Target 与阶段轴裁定、D4 改点以 feedback 形记录(被 D5/D7 修正为 sensor)、D5 归一问题、D7 终态=双触发 improve 流程、D8 「断言」实为判断逻辑的概念化、D9 四项细节移出 objective 交团队承接 | `.specify/goal/session-driven-self-improvement/goal.md` § History(逐字留存历次取值)+ `.specify/teams/session-driven-self-improvement/team.md`(D9 承接小节);访谈全账本 `.specify/memory/session/2026-10-05-goal-session-driven-self-improvement-interview.md`(**git-ignored**,短 notebook) | closed(D7 撤回 D1、D5/D7 修正 D4 的链条已在 History 留痕) |
| B1–B4 | 四量口径用户裁定(2026-10-06):B1 机制定名「运行判定」;B2 正确性拆两半只做制品正确性;B3 满意度默认接受+窄例外(紧邻未解决红→not-evaluated);B4 `templates/commands/improve.md` 写权归本团队 | `.specify/teams/session-driven-self-improvement/team.md` § 四量口径裁定 | ratified |
| S1–S5 | 本团队 serial 链五阶段:S1 契约设计、S2 引擎实现、S3 被动触发接线、S4 主动触发命令(两次派发累积)、S5 独立验证 | `.specify/teams/session-driven-self-improvement/team.md` DAG 与 Stage 表 | S1/S2 完成;S3 产出已验证未落地;S4 累积 1 落地;S5 未开始 |
| S3b | 追加阶段:批评与自我批评概念文档(SI-3C 落点) | 同上 team.md DAG(critique-concept-author 席位) | completed(2026-10-08) |
| OI-1…OI-9 | S1 设计契约的 9 个开放项,各项自带选项与 decider,禁止静默解决 | `.specify/teams/session-driven-self-improvement/runs/2026-10-06-S1-judgment-contract.md` § Open items(**tracked** 副本;工作区原件在 git-ignored `outputs/`) | 见下逐项 |
| OI-1 | 「绿但无红先行取证」的 verdict 映射:契约选 (a) `not_evaluated/green_unproven`,已实现;备选 (b) `regressed` 为一行映射改动 | 同上 | resolved(用户裁定 (a) 并已实现;`scripts/python/run-determination.py:201` 单点) |
| OI-2 | 判定记录的持久落点:契约选 (a) 经 `memory-utils.py` 落 `.specify/memory/session/`;**实现期发现该路径不可达**(`SCOPES` 封闭、slug 剥除 `/`、reindex 非递归),S3 停等用户裁定 → 即下述 **D-A** | 同上 + `runs/20261007T170045Z-report.md` § 4 | **pending(D-A)** |
| OI-3 | token/耗时的绝对目标值(相对比较之外的将来项) | Open items § OI-3 | open,不阻塞(decider:用户经 /speckit.goal modify) |
| OI-4 | 语义正确性作为将来独立轴(本轮明确不设计,不留占位轴) | Open items § OI-4 | open,不阻塞 |
| OI-5 | goal.md 旧术语「判断逻辑」的修正 | Open items § OI-5 | resolved(commit 0206e021 经 /speckit.goal 落地) |
| OI-6 | 是否读 tool-session 的用户动作信号(v1 选不读) | Open items § OI-6 | resolved-for-v1 |
| OI-7 | SI-2 悬空的 `/better-harness` 引用处置 | Open items § OI-7 | open,阻塞 S5 检查单 |
| OI-8 | 比较轴容差带(v1 以结构性手段替代数值容差) | Open items § OI-8 | resolved-for-v1 |
| OI-9 | 引擎的未解决红状态输入面(遥测七键 schema 承载不了,引擎留 `OI9_RED_STATE_INPUT` 隔离缝待裁) | Open items § OI-9 + `runs/20261007T170045Z-report.md` | open,与 S3 落地相关 |
| **D-A** | = OI-2 的续裁定:落点不可达后怎么走 —— (i) 拓宽 `memory-utils.py` 放开子目录(与该引擎封闭 scope 契约相抵);(ii) 引擎自写子目录(证伪契约 §15,红五道已落地守卫);(iii) 维持今日扁平 session+tag 落点(契约备选 (b) 证据目录并置为另一候选) | `runs/20261007T170045Z-report.md` § 4 + 契约 § Open items OI-2 | **pending,阻塞 S3 落地**;decider:用户 |
| **D-B** | 引擎与已落地规范文本的两行分歧:`run-determination.py` 的 `green_unproven` 映射(朱印 `:201` 单点) vs 规范文本要求;修法 = 引擎两行 + `tests/contract/test_run_determination_engine.py:1038,1044` 一行 | `runs/20261007T170045Z-report.md` § 4 | **pending,阻塞 S3 落地**;decider:用户(引擎已落地,落地后修改需明示授权) |
| T-001/T-002/T-003 | goal `command-logic-as-classified-skills` 的三个 Target:T-001 技能内外部标注字段、T-002 技能名称/描述/触发定义、T-003 命令瘦身(命令=入口+委派,细节落技能侧,含「每个技能的输入与产出」子句) | `.specify/goal/command-logic-as-classified-skills/goal.md` § Targets | open(并行团队在执行) |
| SI-0…SI-9 | 自我提升工作流的步骤编号(SI-2 证据限定、SI-3 诊断、**SI-3C 批评后派发**、SI-4 路由、SI-5 落地、SI-6 验证、SI-7 台账、SI-8 对比、SI-9 收束) | `shared/workflow/self-improvement-workflow.md` | active |
| F-A02 | 死信发现:2026-09-11 分流给 improve-skills 的修复从未执行,同一错误主张(per-file 符号链接模型)已从 `skills/create-agent/SKILL.md` 扩散进 `templates/commands/agents.md` | `.specify/memory/feedback/backlog.md`(2026-10-07 行)+ `consume-log.md` | open |
| F-01…F-07 / M-1 / M-2 / D-01 | 自省报告 introspection-20261006T140432Z 的 7 个发现 + 2 个元观察 + `--limit` 截断陷阱;各自分流与处置见报告与 backlog | `.specify/memory/feedback/introspection/introspection-20261006T140432Z.md` + `backlog.md` | mixed(详见 backlog 各行状态) |
