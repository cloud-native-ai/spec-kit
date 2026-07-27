---
id: "dogfood-code-review-f1495907"
scope: "knowledge"
source: "skill:improve-skills"
feature: "code-review"
tags: ["code-review", "dogfooding", "workflow-convention", "feedback-loop"]
title: "Dogfood code-review 技能：所有改动经其展现与审查"
created: "2026-07-26T09:55:45Z"
summary: "用户决策（2026-07-26）：本项目自身 dogfood 新创建的 code-review 技能。后续所有代码修改或需用户确认的改动，均使用 code-review 技能（git-delta 工作流：diff 渲染 / review 逐文件 / note 分级意见 / report --summary 门禁）进行展现与审查，而非裸 git diff。目的：在真实使用中持续收集对该技能本身的反馈"
---

用户决策（2026-07-26）：本项目自身 dogfood 新创建的 code-review 技能。后续所有代码修改或需用户确认的改动，均使用 code-review 技能（git-delta 工作流：diff 渲染 / review 逐文件 / note 分级意见 / report --summary 门禁）进行展现与审查，而非裸 git diff。目的：在真实使用中持续收集对该技能本身的反馈，驱动 /improve-skills 循环改进。执行要点：审查意见使用六级分类（blocking/important/suggestion/nitpick/question/praise）；合入前以 report --summary 判定门禁；观察到的技能缺陷/低效点记录到 .specify/memory/feedback/ 并在下一轮 improve-skills 中修复。
