---
description: Critically review the SDD process for the current feature and produce a self-contained, improvement-focused report for the spec-kit maintainers.
short-description: 批判性评审当前特性的 SDD 过程，出具改进导向报告
handoffs:
  - label: Analyze For Consistency
    agent: speckit.analyze
    prompt: Run a read-only consistency analysis to catch cross-artifact drift.
    send: true
  - label: Refine Requirements
    agent: speckit.requirements
    prompt: Refine the requirements specification based on review findings.
    send: true
  - label: Adjust Plan
    agent: speckit.plan
    prompt: Adjust the implementation plan based on review findings.
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-spec --include-spec --include-plan --include-tasks
---

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](shared/workflow/user-input-protocol.md). Treat as command parameters guiding review focus.

## Delegation

Produce a **self-contained, improvement-focused** review report for spec-kit framework maintainers — a critique of the SDD process that produced the feature (process/tooling quality, never the feature's business merits, never the code it produced). The entire executable flow — portable context capture with commit-reachability verification, process execution-history reconstruction (with working-tree fallbacks), core artifact loading, problem-first diagnosis with same-author delegation, independent P0 validation, and template-filled report generation — is delegated to one internal skill; this command keeps entry and the wrap-up lifecycle only.

- **Skill**: `review-sdd-process` — runtime path `.specify/skills/internal/review-sdd-process/SKILL.md`.
- **Inputs**: the feature's artifact chain under `REQUIREMENTS_DIR` (plus `FEATURE_ID`, `FEATURE_NAME`, `AVAILABLE_DOCS`), resolved by the frontmatter `scripts:` prerequisite run (`{SCRIPT}`) from repo root; `$ARGUMENTS` guide review focus (wired by `## User Input` above). Timing: run after `/speckit.implement` completes.
- **Outputs**: the review report written to `REQUIREMENTS_DIR/review.md` (review-template structure, self-contained), plus the closing summary — `REQUIREMENTS_KEY`, feature name, commit SHA, report path, finding counts (P0/P1/P2 by category), top 3 recommendations.

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.review" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Handoffs

**Before**: Run after `/speckit.implement` for complete artifact chain.

**After**: Apply improvements to spec-kit templates/commands/scripts. Optionally iterate requirements/plan.
