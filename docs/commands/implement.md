# /speckit.implement

Execute implementation tasks defined in `tasks.md`, with built-in quality validation, progress tracking, and feature status management.

## When to Use

- After the task list is complete — to begin coding
- When you want phase-by-phase, dependency-aware implementation with automatic progress tracking
- To ensure checklists are satisfied before implementation begins

## Syntax

```text
/speckit.implement [implementation scope or priority]
```

`[implementation scope or priority]` is optional — specify constraints, priorities, or scope adjustments.

## Execution Flow

1. **Setup** — Runs `check-prerequisites.sh` to locate the requirements directory and load the task list.

2. **Checklist gate** — If `checklists/` exists:
   - Scans all checklist files, counts total/completed/incomplete items
   - Displays a status table (PASS/FAIL per checklist)
   - If any checklist is incomplete: **stops** and asks whether to proceed
   - If proceeding with incomplete checklists: requires a waiver comment, recorded in `waivers.md`

3. **Load implementation context**:
   - **Required**: `tasks.md`, `plan.md`
   - **Optional**: `data-model.md`, `contracts/`, `research.md`, `quickstart.md`

4. **Project setup verification** — Creates/verifies ignore files (`.gitignore`, `.dockerignore`, etc.) based on the detected tech stack. Verifies git identity is configured before any file edits.

5. **Parse task structure** — Extracts task phases, dependencies, parallel markers, and execution order from `tasks.md`.

6. **Phase-by-phase implementation**:
   - Completes each phase before moving to the next
   - Follows TDD approach: test tasks before implementation tasks
   - Respects sequential dependencies; parallel tasks `[P]` run concurrently
   - Validates each phase completion before proceeding

7. **Progress tracking**:
   - Marks completed tasks as `[X]` in `tasks.md`
   - Marks deferred tasks as `[~]` with an inline `<!-- deferred: <reason> -->` comment
   - Halts on non-parallel task failures
   - Reports progress after each completed task

8. **Pre-status-flip gate** — Before advancing feature status to `Implemented`:
   - Converts intentionally skipped tasks to `[~]` with justification
   - Verifies zero `[ ]` tasks remain
   - Confirms `verification.md` has a status row for every success criterion
   - Checks deferred task registry completeness

9. **Verification log** — Populates `verification.md` from the template:
   - Records baseline commit at run start
   - Fills post-change metrics and success criterion statuses at run end

10. **Feature integration** — Advances feature status from `Planned` to `Implemented` (only if all gate checks pass).

11. **Optional git commit** — Generates a commit command from the commit template and prompts the user to confirm before executing.

## Output Artifacts

| Artifact | Location |
|----------|----------|
| Updated task list | `.specify/specs/<key>/tasks.md` |
| Verification log | `.specify/specs/<key>/verification.md` |
| Waiver record (if applicable) | `.specify/specs/<key>/waivers.md` |
| Implementation code | As specified in task file paths |

## Task Status Markers

| Marker | Meaning |
|--------|---------|
| `- [ ]` | Open — not yet attempted |
| `- [X]` | Done — completed successfully |
| `- [~]` | Deferred — intentionally skipped with documented reason |

## Prerequisites

- Run [`/speckit.tasks`](tasks.md) to ensure a complete, ordered `tasks.md` exists
- If checklists exist, complete them or decide to proceed with known risks

## Next Steps

- Run [`/speckit.review`](review.md) to evaluate SDD process quality
- Optionally run [`/speckit.analyze`](analyze.md) to catch spec/plan/tasks drift
