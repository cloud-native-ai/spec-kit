---
id: "mem-041c0dc2"
scope: "knowledge"
source: "/speckit.instructions"
tags: ["instructions", "size-budget", "route-r1", "placeholder", "convention"]
title: "指令节体积比较必须排除模板占位符骨架节(否则把正确的项目填充判为漂移)"
created: "2026-09-20T06:44:41Z"
summary: "**约定(2026-09-20 实测确立)**:比较活动指令文件与模板的同名节体积时,**模板版本仍含占位符 token(`[Bracketed ...]`、`{{VAR}}`)的节 MUST 被排除**——那是项目本来就该填大的骨架,「活动侧比模板大」是它的正确终态而非漂移。"
---

**约定(2026-09-20 实测确立)**:比较活动指令文件与模板的同名节体积时,**模板版本仍含占位符 token(`[Bracketed ...]`、`{{VAR}}`)的节 MUST 被排除**——那是项目本来就该填大的骨架,「活动侧比模板大」是它的正确终态而非漂移。

**为什么**:本仓实测,按纯体积比较会命中 `Documentation Map`(+3295 B)、`Tech Stack & Resources`(+2677 B)、`Project Overview`(+200 B)三节,而它们全是骨架节;压缩它们等于删除真实项目内容。同批第 4 项命中(`AI Tool Compatibility`,+551 B)也不是候选:活动侧多出的 tier 分层与 canonical 来源指引在模板侧**没有 owner 承载**,压缩即丢失。⇒ 该比较的假阳性率实测 **4/4**。

**推论**:体积差只是**候选筛选**,不是判据。判据是「被删细节是否确有 owner 承载」——先开 owner 确认,未承载则**不是**收敛候选,要么不动,要么先把细节移进 owner(走 R2 的机械迁移)再压。

**落点**:`templates/commands/instructions.md` Action 5 Route R1 的两道过滤器;守卫 `tests/contract/test_instructions_size_budget.py`(断言 R1 文本含排除规则与否定结论)。
