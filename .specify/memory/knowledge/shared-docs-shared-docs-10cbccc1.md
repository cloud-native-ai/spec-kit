---
id: "shared-docs-shared-docs-10cbccc1"
scope: "knowledge"
source: "/speckit.instructions"
tags: ["convention", "instructions", "documentation", "user-decision"]
title: "shared 与 docs 的文档边界：shared=对外分发使用手册，docs=自身开发文档"
created: "2026-10-14T16:06:01Z"
summary: "用户裁定（2026-10-15，经 /speckit.instructions 传入）：shared 与 docs 两个文档面的边界——(1) `.specify/shared/`（框架源 `shared/` 的运行时投影）是随框架**对外分发**的使用手册层：客户项目 init 时整体获得，使用 specify 框架时可直接参考其中 guidelines/workflow/definitions"
---

用户裁定（2026-10-15，经 /speckit.instructions 传入）：shared 与 docs 两个文档面的边界——(1) `.specify/shared/`（框架源 `shared/` 的运行时投影）是随框架**对外分发**的使用手册层：客户项目 init 时整体获得，使用 specify 框架时可直接参考其中 guidelines/workflow/definitions 的大量文档说明；(2) `docs/` 是 spec-kit 自身作为普通代码项目的**开发文档**，**不随框架分发**（仅为本项目 Hugo 文档站的内容源），只有在开发 spec-kit 源代码时才需要参考。落地：`.specify/instructions.md` Documentation Map 引言边界引注 + Tech Stack docs/ 行指向。后续 instructions 刷新 MUST 把本裁定当 must-keep 用户内容，不得在收敛中删除或改写该引注。
