# /speckit.plan

Generate a detailed implementation plan from the requirements specification, producing technical architecture decisions and design artifacts.

## When to Use

- After requirements are defined and clarified — to translate WHAT into HOW
- When you need to make technology choices, define data models, and design API contracts
- To produce the design artifacts that drive task generation

## Syntax

```text
/speckit.plan [planning preferences or constraints]
```

`[planning preferences or constraints]` is optional — specify tech stack, architectural preferences, or constraints.

## Execution Flow

1. **Setup** — Runs `create-new-plan.sh` to initialize the plan directory and copy the plan template to `plan.md`.

2. **Analyze user input** — Determines if `$ARGUMENTS` contains background information, a planning outline, or specific constraints.

3. **Load context** — Reads the requirements spec, constitution, README, project docs, feature memory, and research findings (if available).

4. **Phase 0: Research Review & Context**
   - Gathers information from project docs and feature memory
   - If `research.md` exists, uses its decisions to resolve technical unknowns
   - Fills the Technical Context section (language, framework, storage, testing, performance goals)
   - Marks unknowns as `NEEDS CLARIFICATION`

5. **Fill Constitution Check** — Dynamically derives the principle table from `constitution.md`. Each principle gets a Pass/Fail/Partial status. Failures require justification in the Complexity Tracking section.

6. **Phase 1: Design & Contracts**
   - Extracts entities from the requirements spec → generates `data-model.md`
   - Maps functional requirements to API endpoints → generates contracts under `contracts/`
   - Creates `quickstart.md` with integration scenarios

7. **Post-generation quality gate** — Scans all generated artifacts for internal deliberation markers ("Wait —", "Actually,", "On second thought") and rewrites them as declarative statements.

8. **Feature integration** — Updates the feature registry status from `Draft` to `Planned`.

9. **Report** — Outputs the branch name, plan path, and list of generated artifacts.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Implementation plan | `.specify/specs/<key>/plan.md` |
| Data model | `.specify/specs/<key>/data-model.md` |
| API contracts | `.specify/specs/<key>/contracts/` |
| Quickstart scenarios | `.specify/specs/<key>/quickstart.md` |

## Prerequisites

- Run [`/speckit.requirements`](requirements.md) to produce a requirements specification
- If `requirements.md` contains `[NEEDS CLARIFICATION]`, run [`/speckit.clarify`](clarify.md) first

## Next Steps

- Typically run [`/speckit.tasks`](tasks.md) to decompose the plan into an executable task list
- Optionally run [`/speckit.checklist`](checklist.md) to introduce domain-specific quality gates

## Example

```text
/speckit.plan Use React with TypeScript, PostgreSQL, and REST APIs
```

This produces a plan with the specified tech stack, including data models, API contracts, and a quickstart guide.
