# Quickstart: Visual Project Reporting — Implementation & Verification Walkthrough

**Spec**: [requirements.md](requirements.md) | **Plan**: [plan.md](plan.md) | **Contract**: [contracts/visual-reporting-skills.openapi.yaml](contracts/visual-reporting-skills.openapi.yaml)  
**Requirement → Feature**: `030-summarize-project` → Feature 013 Skills Command

Audience: the agent executing `/speckit.tasks` / `/speckit.implement` for this spec. Steps are ordered Red-Green: contract tests first, then skill content, then mirrors and registry, then end-to-end dry runs.

## 1. Author the contract tests first (Red)

Create two test files modeled on `tests/contract/test_create_skills_prompt_assets.py`:

- `tests/contract/test_summarize_project_prompt_assets.py` — asserts contract items C-1…C-13:
  - `skills/summarize-project/SKILL.md` and `references/reporting-playbook.md` exist; frontmatter `name`, trigger keywords (`项目总结`, `项目汇报`, `进展报告`, `项目进展`, `summarize project`, `project summary`, `project report`), and `skill_id` pattern (C-1, C-2).
  - Ordered five-step workflow section headers; delegation references to `draw-plantuml` (`@startwbs`, `@startgantt`); no `scripts/` directory in the package (C-4, C-5).
  - Consistency/clarification/splitting rules and canonical `## Feedback` block with unit-id `skill:summarize-project` (C-6…C-9, C-13).
  - Registry row in `.specify/instructions.md`; mirror byte-equivalence via directory diff (C-3, C-1).
- `tests/contract/test_analysis_project_uml_assets.py` — asserts C-14…C-20:
  - `skills/analysis-project/SKILL.md` keeps `name: analysis-project`, description mentions UML triggers; four injection points present (C-14, C-15, C-17).
  - `references/uml-visualization-guide.md` exists and contains the view→diagram-type mapping and degradation rule (C-16, C-18).
  - Deliverable-location convention (`docs/overview.md`) and existing required sections still present — regression guard (C-17, SC-007).
  - Mirror byte-equivalence for the edited files (SR-1).

Run and watch them fail:

```bash
python -m pytest tests/contract/test_summarize_project_prompt_assets.py tests/contract/test_analysis_project_uml_assets.py -q
```

## 2. Build WS-A: the `summarize-project` skill (Green)

1. Scaffold `skills/summarize-project/` following `templates/skills-template.md` and the `create-skills` skill conventions (frontmatter, `${SKILL_HOME}` / `${SKILL_WORKDIR}` idioms).
2. Write `SKILL.md` — five-step workflow per data-model.md Part 2 and contract C-4…C-9; every charting step delegates to `draw-plantuml` (cite its howto guides `13-wbs-diagram.md`, `14-gantt-diagram.md` and output conventions); default output location `docs/project-summary/` under the target workspace (user-overridable); end with the canonical `## Feedback` block (unit-id `skill:summarize-project`).
3. Write `references/reporting-playbook.md` — decomposition depth, estimation defaults with visible assumption marking, chart-set splitting, two-chart consistency checklist.
4. Do NOT create a `scripts/` directory — rendering is delegated (SR-2).

## 3. Build WS-B: `analysis-project` UML enhancement (Green)

1. Edit `skills/analysis-project/SKILL.md` at exactly four injection points:
   - Frontmatter `description`: add UML trigger terms (e.g. "UML图", "component/deployment/sequence diagram").
   - Phase 5 (report structure design): plan UML figures for primary views per `references/uml-visualization-guide.md`.
   - Phase 8 (final report assembly): embed rendered figures with captions, PNG default + SVG available, keep `.puml` sources.
   - Output Requirements: UML figures as the standard for primary views; Mermaid retained for secondary sketches; degradation note rule.
2. Create `skills/analysis-project/references/uml-visualization-guide.md` with the normative view→diagram-type mapping (data-model.md Part 1 — including `activity` as the behavior-flow alternative for business/process flows), the `docs/figures/` storage convention with relative-path references, delegation pointers into `draw-plantuml/references/howto/`, and the renderer-unavailable degradation rule.
3. Touch nothing else in the workflow — phases 1–4, 6–7, subagent discipline, and `$WORK_DIR/docs/overview.md` stay byte-identical in behavior (FR-018).

## 4. Registry and mirrors

1. Add the `summarize-project` row to the skills registry in `.specify/instructions.md`; refresh `analysis-project`'s description cell if the registry mirrors skill descriptions.
2. Synchronize mirrors and verify byte-equivalence:

```bash
diff -r skills/summarize-project .specify/skills/summarize-project
diff -r skills/analysis-project   .specify/skills/analysis-project
```

## 5. Green run

```bash
python -m pytest tests/contract/test_summarize_project_prompt_assets.py tests/contract/test_analysis_project_uml_assets.py -q
python -m pytest tests/contract -q   # no regressions in sibling suites
```

## 6. End-to-end dry runs (Success Criteria)

1. **WS-A**: invoke `summarize-project` on a representative workspace (e.g. this repo). Verify: single HTML report under `docs/project-summary/` with images and `.puml` sources co-located; WBS chart + Gantt chart with milestones, progress status, reference-date marker; two-chart naming consistency 100% (SC-003); generation date, scope, assumptions stated (SC-001…SC-005 artifacts).
2. **WS-B**: run `analysis-project` on a representative repository. Verify: `docs/overview.md` produced; primary views carry rendered UML figures (≥1 structural, ≥1 behavioral-or-deployment) with captions, figures stored under `docs/figures/` and referenced by relative paths (SC-006); all pre-existing chapters and conventions intact (SC-007).
3. Record outcomes per SC in `verification.md` during `/speckit.implement`.

## 7. Wrap-up

- Update Feature 013 detail (`Key Changes`) and feature index dates per the Feature Integration Protocol.
- Record skill-run feedback via the canonical `## Feedback` step of each touched skill on first substantial use.
