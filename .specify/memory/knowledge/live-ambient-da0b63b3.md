---
id: "live-ambient-da0b63b3"
scope: "knowledge"
source: "/speckit.instructions"
tags: ["instructions", "size-budget", "convention", "two-hats"]
title: "约定：指令预算须由模板与 live 同步满足；ambient 节压回摘要+指针"
created: "2026-10-30T03:50:59Z"
summary: "指令文件的体积预算必须由框架模板与项目 live 文件**同步**满足：`templates/instructions-template.md` 自身在 2026-10-30 时为 36,471 B，已超过脚本的 32,768 B 预算，因此只收敛 `.specify/instructions.md` 是客户端实例修复，新项目仍会一出生就超预算。正确做法（用户 2026-10-30 决策）是把 a"
---

指令文件的体积预算必须由框架模板与项目 live 文件**同步**满足：`templates/instructions-template.md` 自身在 2026-10-30 时为 36,471 B，已超过脚本的 32,768 B 预算，因此只收敛 `.specify/instructions.md` 是客户端实例修复，新项目仍会一出生就超预算。正确做法（用户 2026-10-30 决策）是把 ambient 纪律节压回「规范摘句 + owner 指针」形态，按 templates → .specify/templates 镜像 → .specify/instructions.md 三处同步落地；项目填充节（Documentation Map / Tech Stack / Project Overview / AI Tool Compatibility）只改 live，且不得压回模板骨架。压节时必须逐字保留契约测试钉住的字面量与否定项（Fast Fail 的 lead/binds 句、Progress 的 15 minutes、SDD 路由字节上限声明、各节 owner 路径等）。
