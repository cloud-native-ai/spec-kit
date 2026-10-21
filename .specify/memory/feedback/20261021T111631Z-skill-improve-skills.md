---
id: "20261021T111631Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-sdd-loop-driver-20261021"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
disposition: "ignored"
partial: false
created: "2026-10-21T11:16:31Z"
summary: "Improved sdd-loop-driver local-mode behavior: U0 defaults to the current project when host+path are absent; local topology uses the host's native subagent (or orchestrator-direct) and must not launch "
disposition_reason: "introspection-20261021T133447Z: excluded (no actionable framework finding)"
---

## Review
Improved sdd-loop-driver local-mode behavior: U0 defaults to the current project when host+path are absent; local topology uses the host's native subagent (or orchestrator-direct) and must not launch qodercli; U2/U3 distinguish native synchronous wait from remote external runner/watcher; HR6, delegation, dispatch-recipes, watch-model, stage-prompts, docs, and contract test C-23 synced. Gates: shape pass (~4905/5000), redline PASS, 26 contract tests passed.

## Optimization Points
- 无 host+path 时 U0 现在缺省当前项目；本地拓扑使用宿主原生子代理（或驱动者直执），MUST NOT 启动 qodercli；远端拓扑保留外部 CLI + runner/watcher。
- token-efficiency: SKILL.md 可控正文 4999 -> 4905（净减 94）；为容纳新规则压缩了 Efficiency Optimizations 与 References 摘要，未超 5000 预算。
- Pressure test: GREEN 引用 U0 与本地原生拓扑章节并正确回答；RED 在无技能时选择追问用户而不是缺省当前项目，证实 S0 缺口。载体选择一半为 inconclusive（RED 本来就选原生），需在默认 qodercli 的宿主上再验证。
- 附带修复：镜像中 7 个既有的陈旧文件（efficiency-model/cli/profiles/scripts）随本次 sync 收敛到源侧；契约 C-18/C-12 通过。
