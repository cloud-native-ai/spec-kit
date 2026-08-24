---
id: "20260822T044605Z-skill-improve-skills"
unit_id: "skill:improve-skills"
unit_type: "skill"
run_id: "improve-browser-utils-tier-reorder-2026-08-22"
scope: "local"
probe: "skill-improve-skills-wrapup"
kind: "internal"
slice: "skills"
partial: false
created: "2026-08-22T04:46:05Z"
summary: "De-agented browser-utils tier classification (capability-based, no Wukong/Qoder/Claude Code names) and reordered tiers (T1 built-in, T2 Playwright, T3 MCP connector) across SKILL.md + 6 reference/guid"
---

## Review
De-agented browser-utils tier classification (capability-based, no Wukong/Qoder/Claude Code names) and reordered tiers (T1 built-in, T2 Playwright, T3 MCP connector) across SKILL.md + 6 reference/guide files, mirrored both trees byte-equal; skill-shape exit 0; 24/24 agent-specific-config contract tests pass. Surfaced norm conflict: full removal of agent guides/Agent-Specific Configuration is blocked by contract tests C-002–C-004.

## Optimization Points
- **Research-first paid off**: grepping for contract tests before editing revealed C-002–C-004 mandate the Agent-Specific Configuration section and claude-code/copilot guides — a silent removal would have broken the suite. When a user requirement implies removing structure, grep tests/contract/** for mandated sections BEFORE proposing the edit plan.
