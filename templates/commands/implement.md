---
description: Implement the feature by processing and implementing all tasks defined in tasks.md
short-description: 按 tasks.md 顺序逐项实现当前特性的全部任务
handoffs:
  - label: Review Implementation
    agent: speckit.review
    prompt: Review the workflow and artifacts after implementation.
    send: true
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a read-only cross-artifact analysis to catch drift and gaps.
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
---

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions.

## Glossary

Consult the project glossary (`.specify/memory/glossary.md`, ambient via the Documentation Map) and apply the protocol in `.specify/shared/workflow/glossary.md`:

- **Before acting on the user input**, map any recorded homophone/confusable variant to its canonical term (correcting voice/dictated input); surface each correction so the user can override it, and defer to the user on ambiguous variants.
- **At wrap-up**, propose any new project-specific terms (`origin=auto`, `status=proposed`), excluding common words; run conflict detection; non-conflicting new terms MUST be written directly and merged into the wrap-up report (non-blocking); only writes that conflict with or overwrite an existing user entry MUST still pause for user confirmation. User-authored entries are authoritative.

## Skill Delegation

The executable core of this command is the **`implement-feature`** skill (`.specify/skills/internal/implement-feature/SKILL.md`): it turns the feature's `tasks.md` into a completed, verified, committed implementation. This template keeps entry, user input, glossary, the feature-status flip, and the wrap-up lifecycle only.

- **Inputs**: `$ARGUMENTS` (processed per the User Input Protocol); `REQUIREMENTS_DIR` and `AVAILABLE_DOCS` from the `{SCRIPT}` prerequisite run (frontmatter `scripts:`), all paths absolute; `tasks.md` and `plan.md` are REQUIRED.
- **How to call**: read the skill and follow its steps 1–9 — checklist exemption gate (waiver probe), summary-first context load, project setup + writability pre-probe, topological `tasks.md` parse (dependencies, `[P]`, `[blockedBy]`, `[>]` claims), phase-by-phase TDD implementation (mechanical write gate, failure attribution first, batched regens, evidence-backed closure IDENTIFY→RUN→READ→VERIFY→CLAIM), progress tracking with honest deferred-task marks, Completion Gate re-validation + commit gate (deletion-surface audit, approval routing), Pre-Status-Flip Gate + verification log.
- **Also owned by the skill**: mid-run user directives (scope revision — upstream first, append-only tasks, re-verify the touched surface), the opt-in Long-Run self-iterating loop (state file, iteration cap, stagnation two-strike), and the Optional Git Commit fallback (`templates/commit-template.md`, explicit user approval only).
- **Outputs**: every task `[X]` or honestly `[~]`, the `## Completion Gate` re-validated against the current tree, `verification.md` populated, phase-boundary commits landed.

> **Fast Fail 实例指针**:本文件中"即停 / 即中止 / 不得静默降级"一类规则是快速失败纪律的既有**实例**;其判据与两份清单的唯一真源是 `.specify/shared/guidelines/fast-fail.md`(本文件引用它,MUST NOT 复述它)。

## Feature Integration

Apply [Feature Integration Protocol](shared/workflow/feature-integration.md). This command's transition: `Planned → Implemented` (requires gate pass).

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.implement" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Handoffs

**Before**: `/speckit.tasks` to ensure complete tasks.md exists.

**After**: `/speckit.review` for SDD process quality evaluation. Optional `/speckit.analyze` for drift detection.
