# /speckit.clarify

Identify underspecified areas in the current feature artifacts and resolve ambiguities through interactive questioning.

## When to Use

- After `/speckit.requirements` when the spec contains `[NEEDS CLARIFICATION]` markers
- After `/speckit.plan` when the plan has unresolved technical decisions
- After `/speckit.tasks` when task descriptions are ambiguous or incomplete
- Whenever the `Related Feature` section still shows `Need clarification`

## Syntax

```text
/speckit.clarify [clarification context]
```

`[clarification context]` is optional — specific areas of ambiguity or additional context to guide the clarification process.

## Execution Flow

### Phase Detection

The command automatically detects which phase of the SDD lifecycle you are in and adapts accordingly:

| Phase | Trigger Condition | Target File | Next Command |
|-------|------------------|-------------|--------------|
| **A: Post-Requirements** | `plan.md` does NOT exist | `requirements.md` | `/speckit.plan` |
| **B: Post-Plan** | `plan.md` exists, `tasks.md` does NOT | `plan.md` | `/speckit.tasks` |
| **C: Post-Tasks** | `tasks.md` exists | `tasks.md` | `/speckit.implement` |

### Execution Steps

1. **Run prerequisites script** — Parses JSON for repo root, branch, requirement ID, and available file paths.

2. **Detect current phase** — Checks which artifacts exist to determine the target file (requirements.md, plan.md, or tasks.md).

3. **Load context** — Reads the constitution, README, feature registry, research findings, and the target artifact.

4. **Coverage scan** — Evaluates each category in the phase-specific taxonomy (functional scope, data model, UX flow, non-functional attributes, etc.) and marks each as Clear / Partial / Missing.

5. **Generate question queue** — Produces up to 5 prioritized questions from categories with Partial or Missing status. Each question is:
   - Answerable with multiple-choice (2–5 options) or a short phrase (≤5 words)
   - Material to downstream artifacts
   - Filtered against research findings to avoid redundancy

6. **Interactive questioning loop** — Presents ONE question at a time with a recommended answer. Accepts user's choice or custom input. Stops when all critical ambiguities are resolved, the user signals completion, or 5 questions are reached.

7. **Integration** — After each accepted answer:
   - Records the Q&A in a `## Clarifications` → `### Session YYYY-MM-DD` section
   - Updates the appropriate section of the target file (e.g., functional requirements, data model, feature linkage)
   - Saves the file immediately

8. **Validation** — Checks for duplicates, lingering placeholders, contradictions, and terminology consistency.

9. **Report** — Outputs the operating mode, questions asked, sections touched, coverage summary, and suggested next command.

## Phase-Specific Behavior

### Mode A (requirements.md)
- Taxonomy covers: feature linkage, functional scope, domain/data model, interaction/UX flow, non-functional attributes, integration, edge cases, constraints, terminology, completion signals
- Updates `Related Feature` with `Feature ID` and `Feature Name` when resolved
- Does NOT modify plan or tasks

### Mode B (plan.md)
- Taxonomy covers: technical context completeness, constitution check, project structure, requirements coverage, data model alignment, API contract alignment, consistency, feasibility
- Resolves `NEEDS CLARIFICATION` fields in the Technical Context table
- Does NOT modify requirements.md

### Mode C (tasks.md)
- Taxonomy covers: story coverage, task completeness, dependency correctness, file path validity, definition of done, format compliance, phase dependencies
- Adds missing tasks or reorders within phases
- Does NOT modify requirements.md or plan.md

## Prerequisites

- At minimum, run [`/speckit.requirements`](requirements.md) first to produce `requirements.md`

## Next Steps

- Mode A → [`/speckit.plan`](plan.md)
- Mode B → [`/speckit.tasks`](tasks.md)
- Mode C → [`/speckit.implement`](implement.md)

## Example

```text
/speckit.clarify
```

The command detects the current phase, scans for ambiguities, and walks you through resolving them one question at a time.
