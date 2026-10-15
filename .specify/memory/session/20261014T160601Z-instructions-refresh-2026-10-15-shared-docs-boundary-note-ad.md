---
id: "20261014T160601Z-instructions-refresh-2026-10-15-shared-docs-boundary-note-ad"
scope: "session"
source: "/speckit.instructions"
tags: ["instructions", "residual-report"]
title: "instructions refresh 2026-10-15: shared/docs boundary note added (partial update)"
created: "2026-10-14T16:06:01Z"
summary: "Residual report (partial update, 用户请求=区分 shared/docs 两个文档面)。CONVERGED: (1) Documentation Map 引言新增边界引注——.specify/shared/（框架源 shared/ 的运行时投影）=随框架对外分发的使用手册层，客户项目 init 整体获得、可直接参考；docs/=spec-kit 自身开发文档，不随框"
---

Residual report (partial update, 用户请求=区分 shared/docs 两个文档面)。CONVERGED: (1) Documentation Map 引言新增边界引注——.specify/shared/（框架源 shared/ 的运行时投影）=随框架对外分发的使用手册层，客户项目 init 整体获得、可直接参考；docs/=spec-kit 自身开发文档，不随框架分发（仅本项目文档站内容源），只在开发 spec-kit 源码时参考；(2) Tech Stack Key Directories 的 docs/ 行由 "User-facing documentation" 改为指向该边界（消除与用户裁定的措辞冲突）。TOLERATED: 其余全部章节逐字节未动；Documentation Map 24 行路径脚本化存在性核验全过。RECOVERED: 无——旧备份 2026-07-11 独有标题仅 Resource Registry 族，属 Action 5 规定退役的机器注册表（由 Skills & Tools 指针+目录发现取代），非丢失。PENDING: 尺寸 33384→33898 B，超 32768 B 预算 1130 B；R1/R2 均无合法候选（正 delta 行全部 placeholder=yes 项目填充型；唯一 project-owned 章节仅 787 B 未达 4 KB 阈值）——需用户裁定（调 INSTRUCTIONS_BUDGET_BYTES 或拆分 Documentation Map）。提交 5ca10ec6（仅 instructions.md；新备份被 .gitignore:56 忽略属预期）。
