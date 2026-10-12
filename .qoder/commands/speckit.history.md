---
description: 将当前工具的会话历史增量蒸馏为主题聚合知识库
---
<!-- AUTO-GENERATED from templates/commands/history.md — do not edit; edit the source template, then run scripts/python/regen-command-copies.py -->
## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](.specify/shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions. Recognized optional parameters:

- `--full` — reprocess **all** sessions and regenerate the knowledge base (ignore the incremental manifest).
- A theme focus, date range, or topic hint — narrow which sessions to emphasize.

## Skill Delegation

The executable core of this command is the **`manage-history`** skill (`.specify/skills/internal/manage-history/SKILL.md`): it distills the current AI tool's past conversations for this project into a durable, theme-aggregated knowledge base under `.specify/history/`. This template keeps entry, user input, and the wrap-up lifecycle only.

- **Inputs**: the `$ARGUMENTS` parameters processed above, plus the JSON output of the frontmatter `scripts:` entry (`.specify/scripts/bash/collect-history.sh --json`, the collect-history locate step) identifying tool, session store, session count, and the manifest path; `--full` for a full reprocess; optional theme/date-range/topic narrowing.
- **How to call**: read the skill and follow its Workflow (Steps 1–6) — tool & project identification with the support/empty-store gates, clean-session extraction (trivial sessions skipped, never silently), five-dimension distillation (decisions & rationale / reusable lessons / open TODOs / key interaction flows / user↔model conflicts), theme aggregation with incremental merge, manifest update, run report.
- **Outputs**: the `.specify/history/` document set (`README.md` index, `00-cross-cutting-lessons.md`, one `NN-<theme-slug>.md` per theme) plus `.manifest.json`, and the run report (distilled vs skipped sessions with reasons, themes created/updated, output location).
- **Safety rules** are owned by the skill: read-only on the session store, no verbatim dumps, no silent truncation, unsupported tools stop cleanly.

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.history" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Handoffs

**Before running this command**:
- Have some conversation history with the current tool for this project (this command distills the past, it does not create it).

**After running this command**:
- Run `/speckit.constitution` or `/speckit.instructions` if the distilled history surfaces conventions worth codifying.
- Invoke `memory-record` (`.specify/skills/internal/memory-record/SKILL.md`) to persist key distilled knowledge into long-term project memory.