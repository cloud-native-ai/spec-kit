<!--
  Shared "Skill Enablement" snippet — SINGLE SOURCE OF TRUTH.

  This file is NOT a standalone agent template. It is the canonical wording of the
  skill-preference protocol that every built-in role agent (`agents/*.agent.md`) and
  its generator (`agent-role-*-template.md`) composes into a `## Skill Enablement`
  section. Edit the protocol text HERE only; keep every agent/template copy identical
  so agent→skill guidance stays uniform and discoverable (FR-009, SC-005).

  The ONLY per-agent-varying part is the `| Skill | When to use |` table, whose skill
  set MUST equal that agent's `skills:` frontmatter list. Do not reword the shared
  protocol paragraph per agent (contract C-2).
-->

## Skill Enablement

Framework skills and agent definitions install together, so every skill I declare is guaranteed to be invocable. I therefore prefer an applicable framework skill over performing the same operation manually or ad-hoc, and I delegate the operation to the skill rather than reimplementing its logic inline. When more than one skill could apply, I choose the most role-specific one. When no relevant skill applies — or a relevant skill is unavailable or fails at runtime — I complete the operation directly and surface the failure rather than stalling or fabricating a skill reference. The skills below are my role-relevant, curated set; any other installed skill remains available as a fallback.

| Skill | When to use |
|-------|-------------|
| <!-- per-role rows; one per `skills:` slug --> | |
