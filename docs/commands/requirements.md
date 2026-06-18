# /speckit.requirements

Create or update a requirements specification from a natural-language feature description.

## When to Use

- Starting a new feature — this is the **first command** in the core development lifecycle
- Translating a business idea, user request, or product brief into a structured specification
- When you need to define WHAT to build and WHY, without specifying HOW

## Syntax

```text
/speckit.requirements <feature description>
```

`<feature description>` is a natural-language description of the feature you want to build.

## Execution Flow

1. **Generate short name** — Analyzes the feature description and creates a concise 2–4 word branch name (e.g., `user-auth`, `analytics-dashboard`).

2. **Check for existing branches** — Fetches all remote branches, scans local branches and `.specify/specs/` directories to determine the next available feature number.

3. **Run setup script** — Executes `create-new-requirement.sh` to create a new git branch and initialize the spec directory at `.specify/specs/<NNN-short-name>/`.

4. **Parse feature description** — Extracts key concepts: actors, actions, data entities, and constraints from the user's input.

5. **Generate specification** — Fills the spec template (`templates/spec-template.md`) with:
   - Overview and context
   - User scenarios and testing flows
   - Functional requirements (each must be testable)
   - Non-functional requirements
   - Success criteria (measurable, technology-agnostic)
   - Key entities
   - Assumptions and edge cases

6. **Initialize feature linkage** — Sets `Feature ID` and `Feature Name` to `Need clarification` (resolved later by `/speckit.clarify`).

7. **Handle ambiguities** — For unclear aspects:
   - Makes informed guesses based on context and industry standards
   - Marks critical unknowns with `[NEEDS CLARIFICATION]` (maximum 3 markers)
   - Prioritizes by impact: scope > security/privacy > user experience > technical details

8. **Quality validation** — Generates a quality checklist at `checklists/requirements.md` and validates the spec against it. If `[NEEDS CLARIFICATION]` markers remain, presents options to the user (max 3 questions) and updates the spec with answers.

9. **Feature integration** — Scans the feature registry (`.specify/memory/features.md`) for a matching feature. Binds the spec to an existing feature or creates a new one.

10. **Report** — Outputs the branch name, spec file path, checklist results, and next-step recommendation.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Requirements specification | `.specify/specs/<NNN-short-name>/requirements.md` |
| Quality checklist | `.specify/specs/<NNN-short-name>/checklists/requirements.md` |
| Feature detail (if new) | `.specify/memory/features/<ID>.md` |
| Feature index update | `.specify/memory/features.md` |

## Guidelines

- Focus on **WHAT** users need and **WHY** — avoid implementation details
- Write for business stakeholders, not developers
- Every requirement must be testable and unambiguous
- Success criteria must be measurable and technology-agnostic
- Document assumptions rather than asking about every unknown

## Prerequisites

- (Optional) Run `/speckit.feature` to ensure the feature registry is current

## Next Steps

- If the spec contains `[NEEDS CLARIFICATION]` markers → run [`/speckit.clarify`](clarify.md)
- If the `Related Feature` section shows `Need clarification` → run [`/speckit.clarify`](clarify.md)
- Otherwise → proceed to [`/speckit.plan`](plan.md)

## Example

```text
/speckit.requirements Build a task management app with Kanban boards, drag-and-drop, and user assignment
```

This generates a requirements specification covering user scenarios, functional requirements, success criteria, and key entities — all focused on what the feature does, not how to implement it.
