# Requirements Specification: Visual Project Reporting — summarize-project Skill & analysis-project UML Enhancement

**Requirement Branch**: `030-summarize-project`  
**Created**: 2026-07-18  
**Status**: Draft  
**Input**: User description: "创建一个summarize-project技能,这个技能主要是用来做项目总结和汇报.需要充分利用draw-plantuml技能中的可视化能力，特别是"WBS 工作分解"和"甘特图——任务"这两种类型的图表，前者用于工作分解，后者用于呈现分解后各工作的里程碑、时间安排等。这个技能的核心是让外部人员通过图表直观了解当前项目进展。"  
**Extended Input** (2026-07-18, via `/speckit.plan`): "需要在/storage/project/cloud-native-ai/spec-kit/skills/analysis-project技能中也补充和绘制 UML 图相关的动作,这个技能原本是分析一个已存在项目的整体结构，但不够直观。需要在当前需求中，补充针对该技能的优化与完善。调整整个需求的原始结构，不仅添加新技能，也针对已有技能进行优化。核心工作仍是使用可视化方法完成项目信息的搜集与展示。"

> **Scope note**: This requirement covers TWO workstreams under one theme — visualization-driven project information collection and presentation: (A) create the new `summarize-project` skill (User Stories 1–3, FR-001…FR-014); (B) enhance the existing `analysis-project` skill with UML diagramming actions (User Story 4, FR-015…FR-019). Both delegate chart rendering to the `draw-plantuml` skill.

## Related Feature *(mandatory)*

<!--
  ACTION REQUIRED: Keep the default values as "Need clarification" in the initial draft.
  /speckit.clarify must resolve this section to the final Feature binding before planning.
-->

**Feature ID**: 013  
**Feature Name**: Skills Command

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate a visual project summary report (Priority: P1)

As a project member preparing a report for external stakeholders, I want to invoke a `summarize-project` skill with my project materials (documents, task lists, specs, repository history, or a plain description) so that it produces a single report containing a WBS work-breakdown chart and a Gantt schedule chart, letting outsiders grasp "what the project consists of" and "when things happen" at a glance.

**Why this priority**: This is the core value of the skill — turning raw project information into two complementary visuals (decomposition + schedule) packaged as a shareable report. Without this end-to-end flow the skill delivers nothing.

**Independent Test**: Can be fully tested by invoking the skill on a representative project workspace and verifying that a single HTML report is produced containing (a) a rendered WBS chart decomposing the project hierarchically and (b) a rendered Gantt chart showing the same work items on a timeline, plus a brief narrative an external reader can understand.

**Acceptance Scenarios**:

1. **Given** a project workspace with readable materials, **When** the user asks for a project summary report, **Then** the skill collects the work items, decomposes them into a hierarchy of at least phase → task levels, and renders a WBS chart via the draw-plantuml skill's WBS capability.
2. **Given** the work breakdown produced above, **When** the report is assembled, **Then** a Gantt chart rendered via draw-plantuml's Gantt capability presents each scheduled work item with its start/end or duration, key milestones, and mutual dependencies.
3. **Given** the two charts, **When** the skill finishes, **Then** the output is one self-contained HTML report with the rendered charts embedded (PNG with SVG available), concise per-chart explanations, and an overview narrative covering project background, goals, and current progress — without exposing raw diagram source code.

---

### User Story 2 - Show progress status and milestones at a glance (Priority: P2)

As an external stakeholder reading the report, I want the Gantt chart to visually distinguish completed, in-progress, and not-started work, highlight key milestones, and mark the current date, so that I can immediately tell where the project stands and what comes next.

**Why this priority**: The stated core goal is letting external people intuitively understand *current progress*; static structure and schedule alone do not answer "how far along are we". Progress semantics is what makes the report a progress report rather than a plan document.

**Independent Test**: Can be tested independently by generating a report for a project with a known mix of finished, ongoing, and future tasks plus at least one milestone, and verifying that each status class is visually distinct in the Gantt chart, milestones appear as zero-duration markers, and a today/reference marker is present when the project is mid-flight.

**Acceptance Scenarios**:

1. **Given** work items with different completion states, **When** the Gantt chart is rendered, **Then** completed, in-progress (with percent complete), and not-started items are visually distinguishable (e.g., completion coloring/percentage).
2. **Given** the project has key checkpoints (reviews, releases, acceptances), **When** the Gantt chart is rendered, **Then** each checkpoint appears as a milestone diamond anchored to its date or to the end of its associated work item.
3. **Given** a mid-flight project, **When** the report is read, **Then** the reader can locate "now" on the timeline and see which items should be done versus actually done.

---

### User Story 3 - Adapt the report to audience and scope (Priority: P3)

As a project member, I want to optionally constrain the reporting scope (e.g., current iteration/quarter instead of the full lifecycle) and adjust decomposition granularity for different audiences, so that the same skill serves both detailed team retrospectives and high-level external briefings.

**Why this priority**: Valuable but not required for the core MVP; the default full-lifecycle report already satisfies external communication, and scoping controls can be layered on afterwards.

**Independent Test**: Can be tested independently by requesting a scoped report (e.g., "only this quarter") and a coarse-grained report (e.g., "executive level, phases only") and verifying the WBS depth, Gantt entries, and narrative adjust accordingly while remaining internally consistent.

**Acceptance Scenarios**:

1. **Given** a user-specified reporting period, **When** the report is generated, **Then** the Gantt timeline and the narrative cover that period, and out-of-scope work is omitted or clearly de-emphasized.
2. **Given** a granularity request for a high-level audience, **When** the WBS is produced, **Then** decomposition stops at the requested depth and the report stays readable without losing the phase-level structure.

---

### User Story 4 - UML diagramming actions in analysis-project reports (Priority: P2)

As a reader of an analysis-project architecture report, I want the analysis workflow to draw standard UML diagrams (component, deployment, sequence, class/package as appropriate) for the primary architecture, module, and deployment views, so that the report's structure and behavior explanations are intuitive and unambiguous instead of text-only or ad-hoc sketches.

**Why this priority**: analysis-project already produces deep reports but relies on text and lightweight inline sketches, which readers find not intuitive enough for structural understanding; adding UML views directly serves the same "visualization-driven project information presentation" theme as the new skill. It ranks below the new-skill MVP only because the existing skill remains functional without it.

**Independent Test**: Can be tested independently by running analysis-project on a representative repository and verifying that the final report embeds rendered UML charts for its primary views (at minimum one structural view and one behavioral or deployment view), each with a brief explanation, while the existing analysis depth and report structure remain intact.

**Acceptance Scenarios**:

1. **Given** an analysis-project run reaching its architecture/module/deployment views, **When** the report is assembled, **Then** each primary view is expressed as a standard UML diagram whose diagram type matches the view's semantics (component/package for static structure, deployment for runtime topology, sequence for key flows, class/ER for data structures where relevant).
2. **Given** the UML diagrams, **When** they are produced, **Then** they are rendered by delegating to the draw-plantuml skill's UML capabilities and embedded in the report as rendered images (PNG with SVG available) — never as raw diagram source.
3. **Given** a large or complex project, **When** a single diagram would become unreadable, **Then** the view is split into an overview plus drill-down diagram set with consistent naming and cross-references.

---

### Edge Cases

- **Insufficient time information**: when materials lack dates or durations, the skill makes reasonable schedule assumptions, marks them visibly as estimates in the report, and states the assumptions in text — or asks at most one round of clarification (≤4 questions) when guessing would mislead.
- **Very large projects**: when the work breakdown exceeds what one chart can show readably, the skill splits output into a chart set — one overview chart plus per-phase drill-down charts — keeping each chart self-contained and cross-referenced.
- **Project not started or fully complete**: the report still renders correctly, with status semantics degenerating gracefully (all future, or all completed) and the narrative stating the overall state explicitly.
- **Sparse or missing materials**: when the workspace offers almost nothing, the skill asks one focused round of questions instead of fabricating work items; it must never invent work that has no source.
- **Chart rendering failure**: if draw-plantuml rendering fails (e.g., renderer unavailable), the skill reports the failure clearly, keeps the PlantUML sources for retry, and does not silently ship a report with missing images.
- **UML renderer unavailable during analysis**: when draw-plantuml cannot render during an analysis-project run, the report degrades gracefully — primary views fall back to the existing lightweight inline sketches with a visible note, and the degradation is stated in the report rather than silently dropping figures.
- **View-diagram mismatch**: when a forced diagram type would misrepresent the analysis view (e.g., a data schema drawn as a flow), the skill chooses the semantically correct UML type or keeps a textual/table view, preferring correctness of meaning over diagram count.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST provide a dedicated Skill named [[STR-001]] under the project skills directory (`skills/summarize-project`), following the same authoring conventions as existing skills.
- **FR-002**: The Skill's trigger description MUST cover intents such as "项目总结", "项目汇报", "进展报告", "项目进展", "summarize project", and "project summary/report", so agents route such requests to it.
- **FR-003**: The Skill MUST collect and organize project work items from user-provided or workspace-available materials (documents, task lists, specs, plans, repository history, or conversation description), keep each work item traceable to its source, and MUST NOT fabricate work items without evidence.
- **FR-004**: The Skill MUST decompose project work into a hierarchical work breakdown structure covering at least phase → task levels before any charting, and this single breakdown MUST be the shared basis for both charts.
- **FR-005**: The Skill MUST render the work breakdown as a WBS chart by delegating to the draw-plantuml skill's WBS capability (`@startwbs` semantics), not by re-implementing rendering.
- **FR-006**: The Skill MUST render a Gantt chart by delegating to the draw-plantuml skill's Gantt capability (`@startgantt` semantics), presenting each scheduled work item with start/end or duration and inter-item dependencies where they exist.
- **FR-007**: The Gantt chart MUST mark key project milestones as zero-duration milestone elements.
- **FR-008**: The Gantt chart MUST visually distinguish completed, in-progress (with percent complete), and not-started work items, and MUST indicate the current date or reporting reference point for mid-flight projects.
- **FR-009**: Work-item naming and decomposition MUST be consistent across the WBS chart, the Gantt chart, and the narrative; every WBS leaf work item that carries schedule information MUST appear as a Gantt entry.
- **FR-010**: The Skill MUST output one self-contained HTML report containing the rendered charts, a brief explanation per chart, and an overview narrative for external readers covering project background, goals, and current progress; the report MUST NOT embed raw PlantUML source. Default output location is `docs/project-summary/` under the target workspace (HTML, images, and diagram sources co-located in that directory); the user MAY override the location per request.
- **FR-011**: The Skill MUST honor draw-plantuml's output conventions: PNG and SVG both produced, HTML referencing images via relative paths in the same directory, and PlantUML source files kept alongside for future edits.
- **FR-012**: When information is insufficient, the Skill MUST either proceed with explicit, visibly-marked assumptions or ask at most one clarification round of no more than four questions; guessing MUST NOT silently distort scope, dates, or status.
- **FR-013**: For large projects, the Skill MUST split charts into an overview plus drill-down chart set so that each individual chart stays readable, with consistent naming/coloring across the set.
- **FR-014**: The report MUST state its generation date, reporting scope/period, and any estimation assumptions made.
- **FR-015**: The `analysis-project` skill MUST include UML diagramming actions in its analysis workflow so that the report's primary views — architecture structure, key behavior flows, and deployment topology — are expressed as standard UML diagrams rather than text-only or ad-hoc sketches.
- **FR-016**: UML diagrams in `analysis-project` MUST be produced by delegating to the draw-plantuml skill's UML capabilities (standard UML semantics), not by re-implementing diagram syntax or rendering.
- **FR-017**: The diagram type MUST match each view's semantics: component/package diagrams for static structure, deployment diagrams for runtime topology, sequence diagrams for key interaction flows (activity diagrams are the acceptable alternative for business/process flows), and class/ER diagrams for data structures where relevant; each diagram keeps one core point and large views split into chart sets.
- **FR-018**: Existing lightweight inline sketches (e.g., Mermaid) MAY remain for secondary, quick-glance content, but UML-rendered figures become the standard for the report's primary views; the enhancement MUST NOT regress the skill's existing analysis depth, phase workflow, or report location conventions.
- **FR-019**: UML figures in analysis reports MUST follow the same output conventions as the summary report — rendered images (PNG with SVG available) embedded with brief per-figure explanations, diagram sources kept for future edits, and no raw diagram source embedded in the reader-facing report. Figures and their sources are stored under `docs/figures/` of the analyzed workspace, referenced from the report by relative paths.

### Key Entities *(include if requirement involves data)*

- **Work Item**: A unit of project work; attributes include name, hierarchy level (phase/task/sub-task), status (completed / in-progress / not-started), percent complete, optional owner, schedule (start, end or duration), and source reference.
- **Milestone**: A zero-duration checkpoint (review, release, acceptance) anchored to a date or to the end of an associated work item.
- **Summary Report**: The summarize-project deliverable artifact; comprises the overview narrative, WBS chart(s), Gantt chart(s), generation date, reporting scope, and stated assumptions.
- **UML Figure**: A rendered UML view referenced by a report; attributes include diagram type (component/deployment/sequence/class/package/ER), the analysis view it expresses, a short caption, and its image + diagram-source files.
- **Analysis Report**: The analysis-project deliverable (`docs/overview.md` of the analyzed workspace); comprises analysis chapters plus the UML figure set for its primary views.

### Assumptions

- Input materials come from the user's workspace and/or conversation; the skill does not integrate external project-management systems or live data feeds.
- Report language follows the user's conversation language by default.
- Default reporting scope is the full project lifecycle with emphasis on current progress; users may narrow it per request.
- The draw-plantuml skill is present and is the sole rendering path; `summarize-project` orchestrates decomposition and narrative while delegating chart syntax, rendering, and image conventions to it.
- In `analysis-project`, lightweight inline sketches (Mermaid) remain acceptable for secondary content; UML figures apply to primary views. The skill's existing deliverable location and phase workflow are unchanged.
- Default output locations confirmed at clarification: summary report under `docs/project-summary/`, analysis UML figures under `docs/figures/`; both are user-overridable conventions, not hard-coded constraints.
- The initial Related Feature fields intentionally remain unresolved until `/speckit.clarify`, per the command workflow.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A user can obtain a complete visual summary report in a single session within 10 minutes, with at most one clarification round.
- **SC-002**: An external reader, without asking the author anything, can correctly identify from the report alone: (a) what work the project comprises, (b) when major work items and milestones occur, and (c) the project's current progress state.
- **SC-003**: 100% of WBS leaf work items carrying schedule information have a corresponding Gantt entry with identical naming (two-chart consistency).
- **SC-004**: 100% of charts referenced by the report render successfully and display correctly in the HTML output.
- **SC-005**: At least 90% of external readers in a comprehension walkthrough can state the project's current phase and the next upcoming milestone within 3 minutes of reading the report.
- **SC-006**: An analysis-project report for a representative repository embeds rendered UML figures for 100% of its primary views (at minimum: one structural view plus one behavioral or deployment view), and in a readability walkthrough at least 80% of readers judge the UML-enhanced report easier to understand than the text-and-sketch baseline for the same project.
- **SC-007**: The analysis-project enhancement introduces zero regression to its existing behavior: the report still lands at the documented location, all previously required chapters remain present, and 100% of its prior output conventions (evidence citations, chapter order) still hold.

### Measurement Sources & Collection Methods

- **SC-001 Source**: Timed dry-run session records from request to report delivery, including the count of clarification rounds.
- **SC-002 Source**: Structured walkthrough checklist scored by a reviewer playing the external-reader role against a generated report.
- **SC-003 Source**: Cross-check of the generated WBS leaf items against Gantt entries in the produced artifacts (manual or scripted comparison).
- **SC-004 Source**: Rendering logs plus manual inspection of the final HTML report in a browser/preview.
- **SC-005 Source**: Comprehension test with 3–5 external readers; record time-to-answer and correctness for current phase and next milestone.
- **SC-006 Source**: Artifact inspection of a generated analysis report (primary-view figure inventory) plus a reader walkthrough comparing against the pre-enhancement report of the same repository.
- **SC-007 Source**: Regression checklist comparing a post-enhancement analysis report against the skill's documented output requirements; structural contract tests over the skill's prompt assets.

## Shared Strings *(optional, recommended when any string-literal is consumed verbatim by tests, contracts, snippets, or source)*

| String ID | Value (verbatim) | Consumed by |
|-----------|------------------|-------------|
| `STR-001` | "summarize-project" | FR-001, FR-002, skill directory path `skills/summarize-project`, SKILL.md frontmatter `name`, trigger tests |
| `STR-002` | "analysis-project" | FR-015…FR-019, skill directory path `skills/analysis-project`, SKILL.md frontmatter `name`, trigger tests |

**Citation convention**: When an FR, contract, task, or test references one of these strings, write `[[STR-NNN]]` instead of copy-pasting the literal. CI / `/speckit.analyze` can then verify that every `[[STR-NNN]]` reference resolves to a row in this section.

## Clarifications

### Session 2026-07-18

- Q: Which Feature should this specification bind to? → A: `013` / `Skills Command` — following the precedent of all skill-lifecycle iterations (007/008/012/013/017), `summarize-project` is tracked as a skill artifact under the Skills Command parent feature rather than a new standalone feature.
- Scope extension (user directive via `/speckit.plan` input, 2026-07-18): restructured from single-skill creation into a dual-workstream requirement — (A) new `summarize-project` skill, (B) `analysis-project` UML visualization enhancement. Rationale: both share one theme — visualization-driven project information collection and presentation — and one rendering dependency (draw-plantuml), so they are planned and delivered together under the same requirement and feature binding.
- Q: Where does the summarize-project self-contained HTML report live by default? → A: `docs/project-summary/` under the target workspace, with HTML, images, and diagram sources co-located; user-overridable per request. Reflected in FR-010.
- Q: Where do analysis-project's UML images and PlantUML sources live? → A: `docs/figures/` of the analyzed workspace, referenced from the report by relative paths. Reflected in FR-019.
- Q: What is the UML-vs-Mermaid division of labor in analysis-project? → A: Strict primary/secondary split — primary views (structure, key flows, deployment topology, data structures) MUST use rendered UML figures; Mermaid is restricted to secondary, quick-glance content. Confirms FR-018 and keeps SC-006 objectively verifiable.
- Q: Is activity diagram an acceptable alternative to sequence diagram for behavior-flow views? → A: Yes — sequence remains primary for interaction/call-chain flows; activity is the acceptable alternative for business/process flows. Reflected in FR-017.

<!-- 
This section will be populated by /speckit.clarify command with questions and answers.
Format: - Q: <question> → A: <answer>
-->
