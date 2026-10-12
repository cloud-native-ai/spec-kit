---
description: Generate a requirements-quality checklist for the current feature (Feature as requirement-level scope).
short-description: 为当前特性生成需求质量检查清单
handoffs:
   - label: Back to Plan
     agent: speckit.plan
     prompt: Review or adjust the plan to satisfy checklist items.
     send: true
   - label: Back to Tasks
     agent: speckit.tasks
     prompt: Update/regenerate tasks to include quality gates implied by the checklist.
     send: true
   - label: Implement Project
     agent: speckit.implement
     prompt: Proceed with implementation once checklist items are satisfied.
     send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
---

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions.

## Delegation

`/speckit.checklist` generates a requirements-quality checklist for the current feature — an instrument that tests the specification ("unit tests for requirements writing"), not the implementation.

**Load and follow** `.specify/skills/internal/create-checklist/SKILL.md`:

- **Inputs**: `REQUIREMENTS_DIR` + `AVAILABLE_DOCS` parsed from this command's declared prerequisite script, `{SCRIPT}`, run from repo root (all paths absolute); `$ARGUMENTS` as parameters that may pre-answer the intent-clarification step; feature context from `requirements.md`, plus `plan.md` / `tasks.md` (if present) for gap-finding only.
- **Outputs**: a NEW checklist file under `REQUIREMENTS_DIR/checklists/` (short descriptive `[domain].md` filename, items numbered from CHK001, ≥80% traceability, soft cap 40) — never overwriting an existing one — plus a report (output path, item count, focus areas, depth level, user-specified items incorporated). Feature status transitions `Implemented → Ready for Review` per the Feature Integration Protocol when applicable.

The skill owns the entire workflow: intent clarification (up to three questions, defaults Depth=Standard / Audience=Reviewer / Focus=top 2 relevance clusters), request understanding, same-author gap-finding delegation, checklist generation under the methodology owner (`shared/guidelines/checklist-methodology.md`), canonical structure (`templates/checklist-template.md`), and the report.

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.checklist" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Handoffs

**Before**: Run after requirements exist (ideally plan/tasks too) so checklist is grounded.

**After**: If items fail → iterate `/speckit.plan` or `/speckit.tasks`. Once satisfied → `/speckit.implement`.
