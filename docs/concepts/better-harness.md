# Better Harness Orientation

Spec Kit ships several improvement mechanisms — the feedback layer, the evidence
layer, and the `create-*` / `improve-*` skill families. **Better Harness** is the
name of the single goal they all serve: making every project a better *harness*
for agent work — an environment in which an AI agent can understand the task,
execute on supported and repeatable paths, validate its changes, deliver safely,
and carry lessons forward.

> Concepts adapted from the open-source **Better Harness** project (harness
> definition, feedforward/feedback loop, Agent Work Loop dimensions, evidence
> states). Spec Kit's evidence layer already used its evidence-state vocabulary;
> Constitution Principle XIII makes the shared goal explicit.

## Where the goal is expressed

| Layer | Location | Role |
|-------|----------|------|
| Governance | `.specify/memory/constitution.md` — Principle XIII *Better-Harness Orientation* | Binding statement: improvement units reference the goal model and obey evidence discipline |
| Canonical goal model | `.specify/shared/guidelines/better-harness.md` | Single source of truth: harness definition, feedforward/feedback loop, five-dimension model, evidence red lines, improvement tracks |
| Feedback mechanism | `.specify/shared/workflow/feedback-step.md` § Goal anchor | Feedback strengthens the **Learning Capture** dimension |
| Evidence layer | `.specify/shared/workflow/evidence-step.md` (positioning) | The evidence red lines are the goal model's evidence discipline |
| Improvement skills | `improve-skills` / `improve-agent` / `improve-team` / `improve-tools` `## Goal` | Each names the dimension(s) it strengthens |

## The five dimensions in one glance

| Dimension | Question | Spec Kit mechanisms |
|-----------|----------|---------------------|
| Task Understanding | Does the agent know the goal and what "done" means? | constitution, requirements/clarify, feature index, glossary, instructions |
| Controlled Execution | Is work on supported, repeatable paths? | plan/tasks/implement, skills, tool records, scripts, teams |
| Change Validation | Is there evidence the change works? | Test-First, checklist, analyze, verification.log |
| Reliable Delivery | Does speed bypass quality checks or acceptance? | workflow gates, review, git-workflow |
| Learning Capture | Does the next task benefit from this one? | memory, history, feedback, improve-* skills |

## What this is not

- **Not a scoring or maturity-report system.** Spec Kit remains a
  documentation/prompt framework (Principle IX); the orientation adds direction,
  never machinery.
- **Not a change to the feedback red lines.** Feedback still targets the Spec Kit
  framework itself, remains optional user data, and is never transmitted
  automatically.
- **Not a per-unit fork.** The goal model lives in one shared anchor; units
  reference it instead of restating it.
