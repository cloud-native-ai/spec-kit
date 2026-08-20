---
title: 证据引擎会话获取能力补强(P1–P5 结转)
status: parked
parked_at: 2026-08-12
origin: draft/2026-07-29-export-session-vs-evidence-collection.md 归档结转
tags: [evidence, session, backlog]
---

对比结论中以下五项未落地,随证据引擎下次迭代窗口评估:

1. **P1 cwd 精确匹配补强**——scripts/js/better-harness/session-analysis/platforms/claude.mjs 读 jsonl 内真实 `cwd` 字段。
2. **P2 opencode SQLite 数据源**——scripts/python/evidence-utils.py 相关适配增加 `opencode.db` 根。
3. **P3 currentSessionId() 下沉**——统一 env 清单。
4. **P4 qoder 模型识别 state.vscdb**。
5. **P5 requestId 级 evidenceRef(可选)**。
