# Feature Reference: Visual Project Reporting (summarize-project & analysis-project UML)

**Feature ID**: 013  
**Feature Name**: Skills Command  
**Spec**: [requirements.md](./requirements.md)  
**Plan**: [plan.md](./plan.md)

## Feature Context

This spec is the seventh iteration under Feature 013 (Skills Command):

1. **005-tool-skill-ids**: Deterministic resource IDs for skills and tools
2. **007-skill-install-layout**: Canonical `.specify/skills/` installation layout
3. **008-create-skills-skill**: Extracted creation workflow into `create-skills` skill
4. **012-skill-home-workdir**: `${SKILL_HOME}` / `${SKILL_WORKDIR}` path conventions
5. **013-portable-skill-creation**: Removed tool-manifest coupling for portability
6. **017-consolidate-draft-skills**: Consolidated 9 draft skills into 3 formal skills
7. **030-summarize-project**: Visual project reporting — new `summarize-project` skill plus UML enhancement of `analysis-project` (this spec)

## Problem Statement

Project stakeholders outside the engineering team cannot easily grasp what a project consists of, when things happen, and how far along it is. Two gaps exist in the current skill set: (A) no skill produces a visual project summary — work decomposition plus schedule/milestones — as a shareable report; (B) `analysis-project` produces deep architecture reports that rely on text and lightweight Mermaid sketches, which readers find not intuitive enough for structural understanding.

## Solution

One theme — visualization-driven project information collection and presentation — delivered as two workstreams sharing the `draw-plantuml` skill as the sole rendering path:

- **WS-A**: Create `skills/summarize-project/`, a skill that collects source-traceable work items, decomposes them once into a hierarchy, renders the decomposition as a WBS chart (`@startwbs`) and as a Gantt chart (`@startgantt`, with milestones, dependencies, and progress status), and assembles one self-contained HTML report for external readers.
- **WS-B**: Extend `skills/analysis-project/` at four injection points (frontmatter description, Phase 5 figure planning, Phase 8 figure assembly, Output Requirements) plus one new reference guide so primary analysis views — structure, key flows, deployment topology — are expressed as standard UML diagrams; Mermaid remains for secondary sketches and all existing behavior is preserved.

## Impact on Feature 013

- **Additive with one in-place enhancement**: one new skill package, one existing package edited; no removals.
- **Delegation, not duplication**: neither package adds rendering code; both cite `draw-plantuml` capabilities, keeping diagram expertise in exactly one skill (Constitution IX).
- **Registry growth**: the skills registry gains `summarize-project`; mirrors under `.specify/skills/` follow the canonical layout from spec 007 and byte-equivalence discipline from specs 013/017.
- **Backward compatible**: `analysis-project` keeps its deliverable location, phase workflow, and chapter conventions; UML figures upgrade presentation only.

## Related Files

- Specification: [requirements.md](./requirements.md)
- Plan: [plan.md](./plan.md)
- Data Model: [data-model.md](./data-model.md)
- Contract: [contracts/visual-reporting-skills.openapi.yaml](./contracts/visual-reporting-skills.openapi.yaml)
- Quickstart: [quickstart.md](./quickstart.md)
- Quality Checklist: [checklists/requirements.md](./checklists/requirements.md)
- Feature Detail: `.specify/memory/features/013.md`
- Feature Index: `.specify/memory/features.md`
