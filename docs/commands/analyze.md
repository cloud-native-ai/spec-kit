# /speckit.analyze

Perform a non-destructive cross-artifact consistency and quality analysis across requirements, plan, tasks, and feature metadata.

## When to Use

- After `/speckit.tasks` to validate artifact consistency before implementation
- At any stage to catch inconsistencies, duplications, ambiguities, and coverage gaps
- To verify constitution compliance across all specification artifacts
- When you suspect terminology drift or conflicting requirements between artifacts

## Syntax

```text
/speckit.analyze [analysis focus area]
```

`[analysis focus area]` is optional — specify particular domains or concerns to focus on.

## Execution Flow

1. **Initialize analysis context** — Runs `check-prerequisites.sh` to locate the requirements directory. Derives absolute paths for `requirements.md`, `plan.md`, and `tasks.md`. Aborts if any required file is missing.

2. **Derive feature lookup context** — Identifies the most likely bound feature using explicit references in `requirements.md`, branch naming hints, or string similarity against the feature index.

3. **Load artifacts** (progressive disclosure — only minimal necessary context):
   - From `requirements.md`: functional/non-functional requirements, user stories, edge cases, feature metadata
   - From `plan.md`: architecture choices, data model references, phases, constraints
   - From `tasks.md`: task IDs, descriptions, phase grouping, parallel markers, file paths
   - From feature registry: index rows, matching detail file, spec linkage fields
   - From constitution: principle names and normative statements

4. **Build semantic models** — Creates internal representations:
   - Requirements inventory with stable keys
   - User story/action inventory
   - Task coverage mapping (task → requirement)
   - Constitution rule set
   - Feature linkage model with confidence levels

5. **Detection passes** (limited to 50 findings):
   - **Duplication**: Near-duplicate requirements
   - **Ambiguity**: Vague adjectives lacking measurable criteria, unresolved placeholders
   - **Underspecification**: Requirements missing outcomes, stories missing acceptance criteria
   - **Constitution alignment**: Conflicts with MUST principles, missing mandated sections
   - **Coverage gaps**: Requirements with zero tasks, tasks with no mapped requirement
   - **Inconsistency**: Terminology drift, missing data entities, task ordering contradictions
   - **Feature relevance**: Missing feature binding, incorrect metadata, index/detail divergence

6. **Severity assignment**:
   - **CRITICAL**: Constitution violations, missing core artifacts, zero-coverage blocking requirements
   - **HIGH**: Duplicate/conflicting requirements, ambiguous security/performance attributes
   - **MEDIUM**: Terminology drift, missing non-functional coverage, weak feature mapping
   - **LOW**: Style/wording improvements, minor redundancy

7. **Produce analysis report** — Structured markdown with:
   - Findings table (ID, Category, Severity, Location, Summary, Recommendation)
   - Coverage Summary Table
   - Feature Linkage Summary Table
   - Constitution Alignment Issues
   - Unmapped Tasks
   - Metrics (total requirements, tasks, coverage %, ambiguity count, etc.)

8. **Next actions** — Recommends resolving CRITICAL issues before implementation, or proceeding if only LOW/MEDIUM issues remain.

9. **Offer remediation** — Asks if the user wants concrete remediation suggestions (does NOT apply them automatically).

## Key Characteristics

- **Strictly read-only** — does not modify any files
- **Constitution is non-negotiable** — constitution conflicts are always CRITICAL
- **Evidence-based** — findings are grounded in artifact content, not speculation
- **Deterministic** — rerunning without changes produces consistent results

## Prerequisites

- Run [`/speckit.tasks`](tasks.md) first to produce a complete `tasks.md`

## Next Steps

- If CRITICAL/HIGH issues found → fix in [`/speckit.requirements`](requirements.md), [`/speckit.plan`](plan.md), or [`/speckit.tasks`](tasks.md) and re-run analysis
- If issues are acceptable → proceed to [`/speckit.implement`](implement.md)
