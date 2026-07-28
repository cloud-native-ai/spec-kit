# /speckit.checklist

Generate a requirements-quality checklist — "unit tests for English" — that validates the clarity, completeness, and consistency of requirements.

## When to Use

- Before implementation to ensure requirements are well-specified
- When you need domain-specific quality gates (UX, security, API, performance)
- To validate that requirements are testable and unambiguous
- As a quality gate between planning and implementation

## Syntax

```text
/speckit.checklist [checklist type or focus area]
```

`[checklist type or focus area]` is optional — specify a domain (e.g., `security`, `ux`, `api`, `performance`) or describe the quality dimension to focus on.

## Core Concept: Unit Tests for Requirements

Checklists test the **quality of the requirements themselves**, NOT whether the implementation works:

| Correct (tests requirements quality) | Wrong (tests implementation) |
|--------------------------------------|------------------------------|
| "Are visual hierarchy requirements defined with measurable criteria?" | "Verify landing page displays 3 episode cards" |
| "Is 'prominent display' quantified with specific sizing?" | "Test hover states work on desktop" |
| "Are accessibility requirements specified for all interactive elements?" | "Confirm logo click navigates home" |

## Execution Flow

1. **Setup** — Runs `check-prerequisites.sh` to locate the requirements directory.

2. **Clarify intent** — Generates up to 3 contextual clarifying questions based on the user's input and signals from `requirements.md`. Questions cover:
   - Scope refinement (local module vs. integration touchpoints)
   - Risk prioritization (which areas need mandatory gating)
   - Depth calibration (lightweight sanity list vs. formal release gate)
   - Audience framing (author-only vs. peer review)

3. **Understand user request** — Combines arguments and clarifying answers to derive the checklist theme, must-have items, and category scaffolding.

4. **Load feature context**:
   - `requirements.md`: feature scope, requirements, acceptance criteria
   - `plan.md` (if exists): specification context for gap detection
   - `tasks.md` (if exists): decomposition for missing requirements detection

5. **Generate checklist** — Creates a file in `checklists/` with items grouped by quality dimensions:
   - **Requirement Completeness** — are all necessary requirements documented?
   - **Requirement Clarity** — are requirements specific and unambiguous?
   - **Requirement Consistency** — do requirements align without conflicts?
   - **Acceptance Criteria Quality** — are success criteria measurable?
   - **Scenario Coverage** — are all flows/cases addressed?
   - **Edge Case Coverage** — are boundary conditions defined?
   - **Non-Functional Requirements** — are performance, security, accessibility specified?
   - **Dependencies & Assumptions** — are they documented and validated?

   Each item follows the pattern: `- [ ] CHK### Are [requirement type] defined/specified/documented for [scenario]? [Quality Dimension, Req §X]`

6. **Report** — Outputs the checklist file path, item count, and focus areas selected.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Quality checklist | `.specify/specs/<key>/checklists/<domain>.md` |

## Checklist Types

| Type | File | Focus |
|------|------|-------|
| UX | `ux.md` | Visual hierarchy, interaction states, accessibility, responsiveness |
| API | `api.md` | Error formats, rate limiting, authentication, versioning |
| Security | `security.md` | Authentication, data protection, threat model, compliance |
| Performance | `performance.md` | Metrics, load conditions, degradation, measurability |

Each run creates a **new file** (never overwrites existing checklists), allowing multiple checklists of different types.

## Prerequisites

- Run after you have a requirements specification (and ideally a plan/tasks)

## Next Steps

- If checklist items fail → iterate on [`/speckit.plan`](plan.md) and/or [`/speckit.tasks`](tasks.md) until they pass
- Once satisfied → proceed to [`/speckit.implement`](implement.md)
