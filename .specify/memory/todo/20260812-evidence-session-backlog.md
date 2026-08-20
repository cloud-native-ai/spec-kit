---
title: 证据引擎会话获取能力补强(P1–P5 结转)
status: parked
parked_at: 2026-08-12
origin: draft/2026-07-29-export-session-vs-evidence-collection.md 归档结转(对比 export-session 技能的 6 项优化项;源文档已于结转后按「已合入即删除」纪律移除,全部要点已内联于本文件)
tags: [evidence, session, better-harness, backlog]
---

对比结论中 P6(doctor 三态探测)已实现;以下五项未落地,随证据引擎下次迭代窗口按价值/成本评估:

1. **P1 cwd 精确匹配补强**——claude 适配器 `probeTranscript`/`isWorkspaceMatch` 已部分实现,补齐全平台读 jsonl 内真实 `cwd` 字段精确匹配(规避目录名编码差异)。
2. **P2 opencode SQLite 数据源**——`platforms/opencode.mjs` 增加 `opencode.db`(session/message/part 表)根,还原父子会话(parent_id);node:sqlite 需 Node 22.5+,低版本降级标记 unavailable。
3. **P3 currentSessionId() 下沉**——统一 env 清单(`CLAUDE_(CODE_)SESSION_ID`、`CODEX_THREAD_ID/SESSION_ID` 等),使 `collect-evidence --target 当前会话` 从"最近一个"升级为"精确这一个"。
4. **P4 qoder 模型识别 state.vscdb**——cwd → workspaceStorage hash → state.vscdb → `chat.modelConfig.session.<sid>` 作为模型识别第一优先级。
5. **P5 requestId 级 evidenceRef(可选)**——`chatcmpl-<uuid>` 形态产品在 episode facts 附带 requestId(不可逆,符合隐私纪律)。

## Evolution Log

- 2026-08-12 parked(自 draft 归档结转)。属 Feature 038 证据层自有演进面;逐项独立立项,不与适配器点亮(P7)混批。
