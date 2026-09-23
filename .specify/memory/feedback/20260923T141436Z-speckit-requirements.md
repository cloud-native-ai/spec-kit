---
id: "20260923T141436Z-speckit-requirements"
unit_id: "/speckit.requirements"
unit_type: "command"
run_id: "053-machine-decidable-artifacts:requirements:20260923T1"
scope: "local"
probe: "speckit-requirements-wrapup"
kind: "internal"
slice: "commands"
feature: "053-machine-decidable-artifacts"
partial: false
created: "2026-09-23T14:14:36Z"
summary: "本轮 /speckit.requirements 达成其声明目的:把一份由 /speckit.feedback consume 自省报告路由而来的**五项合并输入**(F-03 requirements 校验器 / F-05 条款→任务绿点归属 / F-04③ 覆盖核算 / F-14次生根 goal 判据主体指代形 / F-16次生根 run-checks)蒸馏为一个可落地特性 053「机器可判定"
---

## Review
本轮 /speckit.requirements 达成其声明目的:把一份由 /speckit.feedback consume 自省报告路由而来的**五项合并输入**(F-03 requirements 校验器 / F-05 条款→任务绿点归属 / F-04③ 覆盖核算 / F-14次生根 goal 判据主体指代形 / F-16次生根 run-checks)蒸馏为一个可落地特性 053「机器可判定的制品命题」,产出 5 个用户故事(P1×2、P2×2、P3×1)、48 条 FR(8 组)、12 条 SC、8 个 Key Entities、10 条 Shared Strings、8 条 Edge Cases、4 条 Assumptions,保留 1 个活动澄清标记(FR-027,上限 3)。编号推导按命令规定实测:.specify/specs/ 与 .archive/ 最高 052、顶层 <NNN>-<slug> 分支最高 052、斜杠命名空间分支(gitee/*、github/*)已排除 ⇒ 下一号 053;create-new-requirements.sh 一次跑通,退出 0,分支 053-machine-decidable-artifacts 与 SPEC_FILE 均落地。**概念拥有者核查**(命令第 5.5 步,本轮刚由 F-10② 新增)实测执行:Program-First 归 shared/guidelines/token-efficiency.md、机器绿与变异演练与反空真哨兵归 shared/guidelines/fast-fail.md、条款分区归 .specify/memory/glossary.md(FR-018 直接引用该已登记术语而非另造名词)、门控预算归 confirmation-gates.md 与其扫描器;契约的**条款语法经查无 owner**(实测 110 份契约 = 100 md + 10 yaml,仅 21 份用 **C-N** 形态,templates/ 下无 contracts-template、shared/definitions/ 下无定义文档),故按命令要求把它作为**新概念**写进规格(FR-022)而非内联定义。**保留标识符核查**(第 5.6 步)实测:validate-requirements / run-checks / [green: / clause-ref / validate_requirements 在非 spec、非 memory 的跟踪文件里零命中,goal-utils.py 的现有 action 为 create/validate/check-statement/list/status/objective/criteria/migrate/targets ⇒ run-checks 未被占用。**房子约定对齐**(第 5.4 步)按最高编号 spec(052)的 requirements.md 取样:中文标题 + 英文括注、## Overview 带「现状锚点(以源码实测为准)」表、故事含 Why this priority / Independent Test / Acceptance Scenarios、FR 用 #### 分组、SC 配 Measurement Sources、Shared Strings 用 [[STR-NNN]] 引用约定 —— 逐项沿用。**自证**:初稿写完后按本规格自己规定的判据做了一次人工核验(校验器尚不存在,故用等价 grep/awk,文档序那一项借用了 clarify-taxonomy.md:111 的过渡抽取式),查出并就地修正两个真缺陷:① US1 验收场景为描述「不可解析引用」而裸写示例编号,该示例本身成了本规格里一个真的不可解析引用——修法是把场景改为描述形态而不实例化,并把「反引号包裹者属提及而非引用」补进 FR-009(原先只有 FR-010 对活动标记做了同构区分);② 漏写必备 H2 ,致 5 个故事与 Edge Cases 挂在 Overview 下,节序核验查出后补回。两处都属「结构命题为假而散文读起来通顺」,恰是本特性立论的实测支撑,已记入检查清单的 Notes。复验数据:FR 48 条连续且 ORDER BREAK 0、SC 12 条连续且 ORDER BREAK 0、STR 引用集 = 定义集 = {001..010}(不可解析 0、定义而未被引用 0)、活动标记 1、占位符残留 0、7 个必备 H2 齐备有序。检查清单 16 项:15 通过、1 未完成(活动标记仍在,须 /speckit.clarify 解决);3 项判为通过但逐条写了理由(实现细节/读者基线/SC 技术中立)。**制品提交**已按 artifact-commit-step 执行:删除面审计暂存前后均空、显式路径暂存 2 个文件、全树无他人未提交制品(无上游偏差可报)、单行消息、提交 7c5598c0,提交后树洁净。Related Feature 按命令约定保留 Need clarification,未自行绑定 Feature,未改 .specify/memory/features.md。

## Optimization Points
- 命令第 7 步「Validate spec against each item」对**结构性**清单项没有任何判定者,于是那几行只能由作者目测后打勾——这正是本轮所写规格要消灭的形态,在它自己的生成命令里现行发生。本轮我手工用 grep/awk 复核了四项结构命题(FR/SC 编号连续性与文档序、`[[STR-NNN]]` 引用可解析、活动标记计数、必备 H2 节齐备且有序),其中文档序那一项还得去借 `shared/constants/clarify-taxonomy.md:111` 那段**过渡期**抽取式——即一处本该被移除的临时副本,反过来成了唯一可用的判定工具。查出两个真缺陷(一处不可解析的 STR 引用、一个被漏写的必备 H2)。建议:第 7 步在校验器落地前先点名一个确定性预检形态(哪怕是命令内联的一段固定抽取式),使清单里「编号连续」「引用可解析」「标记计数」「必备节齐备」这四行不由目测盖章;`validate-requirements.py` 落地后即由它接管(本规格 FR-006/FR-012/FR-014 已把该接管与过渡副本的移除写成义务)。
- 写一份**讨论引用机制本身**的规格,对作者是 grep-敌对的,而命令与 `shared/guidelines/requirements-guidelines.md` 都没给作者任何规避约定。实测形态:为了描述「不可解析的 `[[STR-NNN]]` 引用」,我在验收场景里裸写了一个示例编号,该示例立刻变成本规格里一个真的不可解析引用——被自己的判据查出。校验器侧的区分(被反引号包裹者属「提及」而非「引用」)已由本轮新规格的 FR-009/FR-010 承载,但**作者侧**的约定至今无处陈述。建议:在 `shared/guidelines/requirements-guidelines.md` 或模板 `## Shared Strings` 的注记里加一句——凡在散文中讨论一个保留形态(标记、引用、旗标、字段名),MUST 用反引号包裹以示「提及」,裸写即视为「使用」并会被计数与解析检查计入。一句话的成本,可防止任何关于引用的规格自伤。
