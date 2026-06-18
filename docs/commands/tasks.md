# /speckit.tasks

Break down the implementation plan into granular, dependency-ordered, actionable tasks organized by user story.

## When to Use

- After the implementation plan is ready — to create an executable task list
- When you need to decompose a plan into specific, ordered implementation steps
- To establish parallel execution opportunities and dependency chains

## Syntax

```text
/speckit.tasks [task prioritization or constraints]
```

`[task prioritization or constraints]` is optional. The input can be:
- **Background info**: Context or constraints applied during task generation
- **Task outline**: Phase breakdown used as the organizational structure
- **Additional task entries**: Specific tasks merged into the generated list

## Execution Flow

1. **Setup** — Runs `check-prerequisites.sh` to locate the requirements directory and available design documents.

2. **Load design documents**:
   - **Required**: `plan.md` (tech stack, architecture), `requirements.md` (user stories with priorities)
   - **Optional**: `data-model.md` (entities), `contracts/` (API endpoints), `research.md` (decisions), `quickstart.md` (test scenarios)

3. **Detect test mode** — Parses `constitution.md` for test-mandating principles (TDD, Test-First, Contract-Driven). Prints a banner declaring Tests Mode ON or OFF with the rationale.

4. **Generate task list**:
   - Maps user stories (P1, P2, P3) to phases
   - Maps data model entities and API contracts to their owning user stories
   - Generates tasks in strict checklist format: `- [ ] [TaskID] [P?] [Story?] Description with file path`
   - Identifies parallel execution opportunities (tasks affecting different files with no dependencies)

5. **Organize into phases**:
   - **Phase 1**: Setup (project initialization)
   - **Phase 2**: Foundational (blocking prerequisites for all stories)
   - **Phase 3+**: One phase per user story in priority order
   - **Final Phase**: Polish & cross-cutting concerns

6. **Validate DoD format** — Ensures the Definition of Done section uses `- DoD-N:` prefix format (not checkboxes).

7. **Feature integration** — Updates the feature registry with task generation activity.

8. **Report** — Outputs the total task count, per-story breakdown, parallel opportunities, and suggested MVP scope.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Task list | `.specify/specs/<key>/tasks.md` |

## Task Format

Every task follows this strict format:

```text
- [ ] T001 Create project structure per implementation plan
- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py
- [ ] T012 [P] [US1] Create User model in src/models/user.py
```

- `- [ ]` — Markdown checkbox (required)
- `T001` — Sequential task ID (required)
- `[P]` — Parallel marker, only if parallelizable (optional)
- `[US1]` — User story label, required for story-phase tasks (optional for setup/foundational)
- Description with exact file path (required)

## Prerequisites

- Run [`/speckit.plan`](plan.md) to produce a plan and design artifacts

## Next Steps

- Optionally run [`/speckit.analyze`](analyze.md) to check cross-artifact consistency
- Optionally run [`/speckit.checklist`](checklist.md) to create quality gates
- Then run [`/speckit.implement`](implement.md) to execute the tasks phase-by-phase
