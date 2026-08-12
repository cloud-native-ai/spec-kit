# Feature Detail: Session Export

**Feature ID**: 043  
**Name**: Session Export  
**Description**: AI agent CLI 会话的导出侧命名与资产化——`/speckit.session export --name <名称>` 导出当前(或指定)会话为用户命名目录 + 会话描述文档(元信息 + 结构化总结);执行面为通用化改造后的 `export-session` 技能(恰好六家 CLI 支持面)。  
**Status**: Implemented  
**Created**: 2026-08-12  
**Last Updated**: 2026-08-12

## Overview

Registered as Draft during `/speckit.clarify` for requirement 039 (2026-08-12), which resolved the binding decision: **new Feature** rather than binding 022 AI Tools Support or 026 Agent Skill Enablement — session export is a first-class capability that *consumes* the tool-support and skill surfaces, not a component of either.

Host AI agent CLIs expose no official session naming/renaming mechanism (sessions carry auto-generated IDs; only resume/continue by ID). This Feature lands the degraded route decided in the parked-todo disposition: **rename on the export side** — export the session's raw records into a user-named directory, plus a description document (script-extracted meta + agent-authored structured summary, degradable over budget).

## Scope (per requirement 039)

- `/speckit.session` command (first subcommand: `export`), preview → confirm → execute gate, delegating to the skill.
- `export-session` rework: support face converges to exactly six CLIs (claude-code / codex-cli / qoder-cli / copilot / opencode / hermes); six existing non-target adapters removed with zero residue; platform-specific dependencies removed (generic skill); zip → named-directory product shape; locate mechanisms and five-value exit codes preserved; Copilot/Hermes storage probed at implementation time (honest no-source declaration).
- Session description doc: deterministic meta + faithful structured summary.
- Team-run traceability linkage (dispatch label → exported session dir), P3.

## Related Files

- .specify/specs/039-session-export/requirements.md — requirement spec (4 US / 16 FR / 6 SC)

**039-session-export planned (2026-08-12)**: `/speckit.plan` 通过 Constitution 13/13 Pass(无 Complexity Tracking)。设计工件:data-model.md(3 实体)+ 3 份契约(session-command / export-skill-rework / session-description)+ quickstart.md + feature-ref.md。Phase 0 决策 D1–D8:命令面单一 export 子命令委托技能;导出根 `.session-export/<name>/` 且覆盖走交互确认(无 --force);单脚本改造——删六家适配器、zip→目录、copilot/hermes 探测式适配器(本机实测无落盘);描述文档脚本元信息 + agent 总结双半体,预算双阈值 50,000 行 / 32 MB;退出码五值保持。

**039-session-export implemented (2026-08-12)**: 20/20 任务关闭。export.py 彻底改造(2093→1652 行):删六家适配器、PARSERS 收敛六家(claude-code/codex-cli/qoder-cli/opencode 保留 + copilot/hermes 探测式)、zip→用户命名目录、--name 必填(文法/冲突纪律)、session-meta.json + SESSION.md 双形态(预算双阈值 50,000 行/32 MB);SKILL.md v2.0.0 重写(通用化,去 aone-open 依赖,补 ## Feedback + runtime-mode gate);templates/commands/session.md + 4 per-tool 副本;docs/reference/commands/session.md。全套件对比基线名称级零新增失败(1723 passed);63 例新测试全绿;quickstart §1–§5 走查回写。Pre-Status-Flip Gate pass。
