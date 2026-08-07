---
id: "20260807T064532Z-skill-draw-mermaid"
unit_id: "skill:draw-mermaid"
unit_type: "skill"
run_id: "20260807-remote-first"
scope: "local"
feature: "remote-first-rendering"
partial: false
created: "2026-08-07T06:45:32Z"
summary: "Remote-first policy: default backend server (mermaid.ink); local mermaid-cli only after user consent (TTY prompt or non-TTY guidance + exit 1, never silent fallback). SKILL.md 核心原则/Step8/输出要求 + howto/"
---

## Review
Remote-first policy: default backend server (mermaid.ink); local mermaid-cli only after user consent (TTY prompt or non-TTY guidance + exit 1, never silent fallback). SKILL.md 核心原则/Step8/输出要求 + howto/12 §1 updated. Verified live: default→server; unreachable→consent gate exit 1.

## Optimization Points
- 用户反馈（团队使用中发现）：agent 倾向跳过技能内置远端渲染、自行下载本地渲染工具（jar/mmdc/字体）并卡在本地环境问题。修复：渲染脚本默认后端改为 server（远端优先），新增 local_consent_gate（远端不可用时 TTY 询问 / 非 TTY 打印指引退出，绝不静默回退本地）；SKILL.md 增加「远端渲染优先」核心原则 + Step 8/输出要求同步；howto/12 更新后端说明。另修复 PLANTUML_SERVER_FALLBACKS 空串未禁用公网回退的 `:-` 语义 bug（改 `-`）。
- 建议：draw-d3js/draw-echarts 为纯 HTML 输出技能，无渲染服务，不需此机制；但可在 SKILL.md 说明其输出不依赖任何渲染服务。
