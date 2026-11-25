---
id: "instructions-md-specify-teams-4bf9e650"
scope: "knowledge"
source: "/speckit.instructions"
tags: ["convention", "teams", "instructions", "discovery"]
title: "约定：团队不在 instructions.md 登记，可发现性由 .specify/teams/ 目录承载"
created: "2026-10-06T17:29:13Z"
summary: "新建或修改团队后跑 /speckit.instructions **不会**、也**不需要**在 .specify/instructions.md 里登记该团队。依据：① .specify/shared/definitions/framework-map.md 的 Teams 行是**位置行**（`.specify/teams/<slug>/` — team definitions + runs/"
---

新建或修改团队后跑 /speckit.instructions **不会**、也**不需要**在 .specify/instructions.md 里登记该团队。依据：① .specify/shared/definitions/framework-map.md 的 Teams 行是**位置行**（`.specify/teams/<slug>/` — team definitions + runs/ reports），不逐条枚举团队；② instructions.md 的 ## Skills & Tools 节明写「No registration tables are maintained — agents discover resources natively from the filesystem」，团队沿用同一发现模型；③ instructions.md 的 ## Spec Kit Framework Map 保持模板的 summary + pointer 形态，命令明禁把它扩回内联表。故「同步团队可发现性」的正确结果是**无操作 + 说明为何无需登记**，而不是往指令文件里加一行。副作用面只有符号链接与四套命令副本树，二者由 setup 脚本与 regen-command-copies.py 负责，与团队数量无关。
