# Feature Detail: Agent Skill Enablement

**Feature ID**: 026  
**Name**: Agent Skill Enablement  
**Description**: Wire the seven Worker capability templates to prefer relevant installed skills through declared mappings.
**Status**: Implemented
**Created**: 2026-07-13  
**Last Updated**: 2026-11-22

## Overview

The seven `agent-capacity-*-template.md` Worker capability templates under `skills/internal/create-agent/templates/` declare non-empty `skills:` mappings and a shared `## Skill Enablement` protocol. Each template prefers an applicable framework skill over improvising the same operation, while contract tests ensure that referenced skills exist and that forbidden meta-skills are not declared.

## Latest Review

2026-11-22 implementation audit: Feature 044 changed the actual carrier from `agents/*.agent.md` to the seven Worker capability templates. Current behavior is validated by `tests/contract/test_agent_skill_enablement.py`; older draw-plantuml, analysis-project, and think-skills mapping examples are historical, not the current roster.

## Key Changes

1. Enumerate the 7 built-in role agents as the scope of skill enablement.
2. Have each built-in agent declare its role-relevant skills in a consistent, discoverable format.
3. Add per-agent guidance to prefer an applicable framework skill over manual/ad-hoc execution.
4. Enforce that every referenced skill exists in the installed skill set (zero dangling references, canonical identifiers).
5. Define fallback behavior when no relevant skill applies or a skill fails, without regressing existing tools/EEI/handoffs.
6. (Plan Phase) Design locked: add `skills:` frontmatter + a single-source `## Skill Enablement` section (shared protocol snippet `agent-skill-enablement.md` + per-role skill table) to all 7 agents, mirrored into `create-agent` role templates. Evidence: `plan.md`, `data-model.md`.
7. (Plan Phase) Authoritative Agent–Skill mapping defined (e.g. requirements-analyst → draw-plantuml/memory-recall/memory-record/think-skills; module-designer → analysis-project/git-workflow/git-submodule-edit/memory-record/think-skills); reference-only (`sdd-workflow`) and meta skills excluded. Evidence: `data-model.md` § Agent–Skill Mapping.
8. (Plan Phase) Contract + test-first gate set: `contracts/agent-skill-enablement-contract.md` (C-1…C-5) and a failing-first `tests/contract/test_agent_skill_enablement.py`. Evidence: `contracts/`.
9. (Implement Phase) Added `skills:` frontmatter + `## Skill Enablement` section to all 7 shipped role agents (`agents/*.agent.md`) and mirrored to `.specify/agents/`. Evidence: `verification.md` (SC-001/SC-003/SC-005 pass).
10. (Implement Phase) Added single-source protocol snippet `skills/internal/create-agent/templates/agent-skill-enablement.md` and mirrored the same additions into all 7 `agent-role-*-template.md` generators (C-3 parity). Evidence: `verification.md`.
11. (Implement Phase) Authored `tests/contract/test_agent_skill_enablement.py` (43 assertions: T-1…T-5 + union subset + template parity) — Red→Green; 0 dangling refs, 0 non-declarable slugs (SC-002). Documented convention in `docs/reference/agents/command-and-skills.md` and `docs/agents/design.md`.

## Implementation Notes

- Current carrier: `skills/internal/create-agent/templates/agent-capacity-*-template.md`; the old `agents/*.agent.md` paths are historical.
- The shared protocol snippet is `agent-skill-enablement.md`; declarations use each template's `skills:` frontmatter and `## Skill Enablement` body.
- `tests/contract/test_agent_skill_enablement.py` checks non-empty mappings, existing skill references, and the forbidden meta-skill set.
- Earlier role-agent and skill-mapping examples in the numbered delivery history are not a current path or roster authority.

## Future Evolution Suggestions

- Add automated validation that agent skill references remain a subset of installed skills.
- Provide a machine-readable agent→skill mapping for discovery tooling.
- Extend skill enablement to custom/project-specific agents created via `/speckit.agents`.

## Related Files

- Feature Index: .specify/features.md
- Feature Detail: .specify/features/026-agent-skill-enablement.md
- Specification: .specify/specs/025-agent-skill-enablement/requirements.md
- Quality Checklist: .specify/specs/025-agent-skill-enablement/checklists/requirements.md

## Status Tracking

- **Draft**: Concept and feature registry entry created; requirements specification exists and is clarified.
- **Planned**: Implementation plan, data model, and design artifacts exist for the requirement bound to this feature.
- **Implemented**: Task breakdown completed and all tasks closed/deferred with verification evidence per Success Criteria.
- **Ready for Review**: Deferred tasks resolved or waived and review evidence produced.
- **Completed**: Accepted; all built-in agents are skill-enabled as part of the supported framework.

## Related Specifications/Requirements

- Specification: .specify/specs/025-agent-skill-enablement/requirements.md
  Quality Checklist: .specify/specs/025-agent-skill-enablement/checklists/requirements.md
