## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions.

## Outline

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` from repo root; parse REQUIREMENTS_DIR and AVAILABLE_DOCS. All paths must be absolute.

2. **Check checklists status** (if `REQUIREMENTS_DIR/checklists/` exists):
   - Count total/completed/incomplete items per checklist
   - If incomplete: STOP, show table, ask "Proceed anyway? (yes/no)"
   - If user proceeds: require waiver comment, record in `REQUIREMENTS_DIR/waivers.md`
   - If all complete: proceed automatically

3. **Load context**: tasks.md (REQUIRED), plan.md (REQUIRED), data-model.md, contracts/, research.md, quickstart.md (IF EXISTS).

4. **Project Setup Verification**: Create/verify ignore files based on detected tech stack. For detailed patterns per technology, see `.specify/shared/workflow/ignore-patterns.md`.

5. **Parse tasks.md**: Extract phases, dependencies, task details (ID, description, file paths, parallel markers [P]), execution flow.

6. **Implement feature**:
   - Phase-by-phase; complete each before next
   - Respect dependencies; parallel tasks [P] can run together
   - TDD approach: test tasks before implementation tasks
   - Validate every project-side regen/build command (fail-open EXIT=0 insufficient — verify output artifacts)

7. **Progress tracking**:
   - Report after each completed task
   - Halt on non-parallel task failure; for [P] continue successful, report failed
   - Mark completed: `[X]`. Deferred (resource unavailable): `[~]` with `<!-- deferred: <reason> -->`. Never leave deferred work as `[ ]`.
   - **Evidence-backed closure**: only mark `[X]` for work you have actually executed and verified. Each closure MUST be justified by concrete evidence (a passing test id, a command/grep result, or a diff of the named target file). Do NOT close a task whose named file was not changed.

8. **Completion validation**: All tasks `[X]` or `[~]` (no `[ ]` remaining). Features match spec. Tests pass. **Commit gate**: commit after each task or logical group; the spec dir MUST NOT be left *entirely* uncommitted when validation completes — an uncommitted implementation leaves no per-task audit trail and breaks `/speckit.review`'s git-based history reconstruction. Do not report the Definition of Done as "met" while the whole feature is uncommitted.

9. **Pre-Status-Flip Gate** and **Verification Log**: Apply the full gate protocol from `.specify/shared/workflow/feature-integration.md` § Pre-Status-Flip Gate. Populate `REQUIREMENTS_DIR/verification.md` from `.specify/templates/verification-log-template.md`.

## Feature Integration

Apply [Feature Integration Protocol](.specify/shared/workflow/feature-integration.md). This command's transition: `Planned → Implemented` (requires gate pass).

## Optional: Git Commit

After implementation, generate commit command using `.specify/templates/commit-template.md`:
- Collect: BRANCH, REQUIREMENTS_KEY, FEATURE_TITLE, TYPE, SCOPE, SUBJECT
- Display `git add -A && git commit -m "{msg}"` — only execute on explicit user approval

## Handoffs

**Before**: `/speckit.tasks` to ensure complete tasks.md exists.

**After**: `/speckit.review` for SDD process quality evaluation. Optional `/speckit.analyze` for drift detection.