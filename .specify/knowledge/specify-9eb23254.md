---
id: "specify-9eb23254"
scope: "knowledge"
source: "skill:code-review"
tags: ["workspace-root", "path-resolution", "engines"]
title: "根项目 .specify 锚定原则"
created: "2026-07-27T02:55:33Z"
summary: "原则(用户确立): 所有 speckit 框架的技能和命令, 都应以根项目的 .specify 目录作为一切存储的根目录, 绝不在技能目录等嵌套位置创建 .specify。落地: feedback-utils/memory-utils/history-utils 三引擎统一 resolve_workspace_root — 显式参数 > 脚本自定位(*/.specify/scripts 锚定父项目"
---

原则(用户确立): 所有 speckit 框架的技能和命令, 都应以根项目的 .specify 目录作为一切存储的根目录, 绝不在技能目录等嵌套位置创建 .specify。落地: feedback-utils/memory-utils/history-utils 三引擎统一 resolve_workspace_root — 显式参数 > 脚本自定位(*/.specify/scripts 锚定父项目, 优先级必须高于 CWD 向上查找, 否则技能目录内残留 .specify 会劫持 store) > CWD 向上查找最近 .specify 祖先 > CWD 兜底。bash 侧本即以 SCRIPT_DIR 自定位合规。回归测试: tests/unit/test_workspace_root_resolution.py (15 条参数化, 含 stray nested .specify 场景)。
