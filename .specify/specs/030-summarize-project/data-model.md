# Data Model: Visual Project Reporting — summarize-project & analysis-project UML Enhancement

**Spec**: [requirements.md](requirements.md) | **Plan**: [plan.md](plan.md)  
**Requirement → Feature**: `030-summarize-project` → Feature 013 Skills Command

This model has two parts: **domain entities** (the information the two skills collect and present) and the **skill package structural model** (the prompt-asset layout the contract tests assert).

## Part 1 — Domain Entities

### Work Item

A unit of project work collected from user-provided or workspace-available materials (FR-003).

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `name` | string | yes | Non-empty; identical wording across WBS chart, Gantt chart, and narrative (FR-009) |
| `level` | enum: `phase` / `task` / `sub-task` | yes | Hierarchy covers at least `phase` → `task` (FR-004) |
| `parent` | Work Item reference | no | Absent on root phases; forms the single decomposition tree (FR-004) |
| `status` | enum: `completed` / `in-progress` / `not-started` | yes | Drives Gantt status presentation (FR-008) |
| `percent_complete` | integer 0–100 | no | Mandatory when `status = in-progress`; 100 ⇔ `completed`, 0 ⇔ `not-started` |
| `owner` | string | no | Free text; omitted when unknown — never invented (FR-003) |
| `schedule` | `{ start: date, end: date } \| { start: date, duration: days }` | no | Present ⇔ the item appears in the Gantt chart (FR-009); marked `estimated: true` when assumed (FR-012) |
| `source` | string | yes | Traceable reference to the material the item was derived from (FR-003) |

**State lifecycle**: `not-started` → `in-progress` → `completed`. Degenerate states (all `not-started`, or all `completed`) are valid and must render correctly (edge case: project not started / fully complete).

### Milestone

A zero-duration checkpoint anchored to a date or to the end of an associated Work Item (FR-007).

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `name` | string | yes | Non-empty |
| `anchor` | `date` \| Work Item reference | yes | Exactly one of absolute date or "at end of work item X" |
| `kind` | enum: `review` / `release` / `acceptance` / `other` | yes | Defaults to `other` |

### Summary Report

The `summarize-project` deliverable: one self-contained HTML document (FR-010).

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `narrative` | prose | yes | Covers project background, goals, current progress (FR-010); language follows the conversation (Assumptions) |
| `wbs_charts` | 1..n rendered chart + caption | yes | Rendered via draw-plantuml WBS capability (FR-005); n>1 only as overview + drill-down set (FR-013) |
| `gantt_charts` | 1..n rendered chart + caption | yes | Rendered via draw-plantuml Gantt capability (FR-006); contains milestones (FR-007), status semantics (FR-008), reference-date marker for mid-flight projects |
| `location` | directory path | yes | Default `docs/project-summary/` under the target workspace; HTML, images, and `.puml` sources co-located; user-overridable (Clarifications 2026-07-18) |
| `generated_at` | date | yes | Stated in the report (FR-014) |
| `scope` | string | yes | Reporting period/scope statement; defaults to full lifecycle (FR-014, Assumptions) |
| `assumptions` | list of strings | no | Every estimation default visibly marked (FR-012, FR-014) |
| `images` | PNG + SVG per chart | yes | Both formats produced, relative-path references, `.puml` sources kept alongside (FR-011) |

**Consistency rule (FR-009 / SC-003)**: for every WBS leaf Work Item where `schedule` is present, exactly one Gantt entry exists with identical `name`; the converse also holds (no orphan Gantt bars).

### UML Figure

A rendered UML view embedded in an Analysis Report (FR-015…FR-019).

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `diagram_type` | enum: `component` / `package` / `deployment` / `sequence` / `activity` / `class` / `er` | yes | MUST match the view's semantics per the mapping below (FR-017) |
| `view` | enum: `architecture-structure` / `behavior-flow` / `deployment-topology` / `data-structure` | yes | The analysis view the figure expresses |
| `caption` | string | yes | Brief explanation adjacent to the figure (FR-019) |
| `image_png` / `image_svg` | file path | yes | Both produced; PNG referenced by default, SVG for zoom (draw-plantuml conventions) |
| `source_puml` | file path | yes | Kept for future edits; never embedded raw in the report (FR-019) |
| `set_role` | enum: `standalone` / `overview` / `drill-down` | yes | `overview` + ≥1 `drill-down` when a view is split for readability (FR-017, US4-AC3) |

**View → diagram-type mapping (FR-017)**:

| View | Primary type | Acceptable alternative |
|------|--------------|------------------------|
| `architecture-structure` | `component` | `package` |
| `behavior-flow` | `sequence` | `activity` (for business/process flows) |
| `deployment-topology` | `deployment` | — |
| `data-structure` | `class` | `er` |

If no type fits a view without misrepresentation, the figure is omitted for that view and the textual/table form is kept (edge case: view-diagram mismatch).

### Analysis Report

The `analysis-project` deliverable at `$WORK_DIR/docs/overview.md` (unchanged location, FR-018).

| Field | Type | Required | Validation |
|-------|------|----------|------------|
| `chapters` | prose chapters | yes | Existing required chapters preserved: architecture, tech stack, modules, git evolution, deployment, evaluation (FR-018 / SC-007) |
| `primary_figures` | set of UML Figure | yes | ≥1 figure for `architecture-structure` AND ≥1 for `behavior-flow` or `deployment-topology` (SC-006); 100% of primary views covered; figure files and sources stored under `docs/figures/` of the analyzed workspace, referenced by relative paths (Clarifications 2026-07-18) |
| `secondary_sketches` | inline Mermaid | no | Permitted for secondary, quick-glance content only (FR-018) |
| `degradation_notes` | list of strings | no | Visible note per primary view that fell back to sketch when rendering was unavailable (edge case: UML renderer unavailable) |

## Part 2 — Skill Package Structural Model

Both workstreams ship prompt-artifact packages. Structure asserted by contract tests:

```text
skills/summarize-project/            # NEW (canonical)
├── SKILL.md                         # frontmatter: name=summarize-project, description with trigger
│                                    #   keywords (项目总结/项目汇报/进展报告/项目进展/
│                                    #   summarize project/project summary/project report),
│                                    #   skill_id="<SKILL:.specify/skills/summarize-project/SKILL.md>"
│                                    # body: 5-step workflow (collect → decompose → WBS → Gantt → HTML)
│                                    #       + delegation sections + ## Feedback (canonical block)
└── references/
    └── reporting-playbook.md        # decomposition depth, estimation defaults & assumption marking,
                                     # chart-set splitting, two-chart consistency checklist

skills/analysis-project/             # EXISTING (canonical) — edited in place
├── SKILL.md                         # edits at 4 injection points: frontmatter description (+UML),
│                                    #   Phase 5 (plan UML figures), Phase 8 (assemble figures),
│                                    #   Output Requirements (UML standard for primary views)
└── references/
    └── uml-visualization-guide.md   # NEW: view→diagram-type mapping, delegation pointers
                                     #   to draw-plantuml howto guides, degradation rule

.specify/skills/summarize-project/   # NEW MIRROR — byte-equivalent to canonical
.specify/skills/analysis-project/    # MIRROR — resynchronized to canonical
```

**Structural rules**:

- **SR-1**: `skills/<name>/` is canonical; `.specify/skills/<name>/` is a byte-equivalent mirror (specs 013/017 convention).
- **SR-2**: Neither package contains rendering code; `SKILL.md` and reference guides name `draw-plantuml` as the delegation target (FR-005/006/011/016; Constitution IX).
- **SR-3**: `.specify/instructions.md` skills registry gains exactly one row for `summarize-project`; `analysis-project`'s row stays (description refreshed if the registry mirrors skill descriptions).
- **SR-4**: `summarize-project/SKILL.md` embeds the canonical `## Feedback` block (unit-id `skill:summarize-project`), as every skill does since Feature 028.
- **SR-5**: All new document filenames are lowercase kebab-case under semantic paths (Constitution X).

## Traceability

| Entity / Rule | Requirement | Success Criterion |
|---------------|-------------|-------------------|
| Work Item, consistency rule | FR-003, FR-004, FR-008, FR-009, FR-012 | SC-003 |
| Milestone | FR-007 | SC-002, SC-005 |
| Summary Report | FR-010, FR-011, FR-013, FR-014 | SC-001, SC-002, SC-004 |
| UML Figure + mapping | FR-015…FR-019 | SC-006 |
| Analysis Report | FR-018, FR-019 | SC-006, SC-007 |
| SR-1…SR-5 | FR-001, FR-002, FR-005, FR-016; Constitution IX/X | SC-004, SC-007 |
