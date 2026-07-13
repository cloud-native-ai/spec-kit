# Feature Reference

**Requirement**: 026-agent-team-management
**Bound Feature**: 027 — Team Management
**Status transition (this phase)**: Draft → Planned (`/speckit.plan`)

## Linkage

- Feature Index row: `.specify/memory/features.md` (ID 027)
- Feature Detail: `.specify/memory/features/027.md`
- Spec: `.specify/specs/026-agent-team-management/requirements.md`
- Plan: `.specify/specs/026-agent-team-management/plan.md`

## Relationship to existing features

- **019 Agents Command** — remains the single-agent domain (`create-agent`/`improve-agent`, `/speckit.agents`). This feature *removes* the multi-agent responsibilities from 019's surface (orchestration, triad, team-supervisor, Conceptual Model) and relocates them to 027. Feature 019 detail should note the scope reduction when 027 is implemented.
- **013 Skills Command** — unaffected mechanism; the skill rename/add flows through the existing skills install/registry path.

## Classification

Functional feature (new user-facing command + skills). No non-functional reclassification of existing features.
