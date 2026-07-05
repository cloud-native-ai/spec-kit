---
name: subagent-driven-development
description: |
  Execute an implementation plan by dispatching a fresh implementer subagent per task, gating each task behind a two-verdict review (spec compliance + code quality) with a fix-and-re-review loop, then running one broad whole-branch review before finishing. Preserves context hygiene via file handoffs and a durable progress ledger. Use this when the user mentions ["subagent driven development", "SDD", "dispatch subagent per task", "fresh subagent per task", "implementer subagent", "task reviewer", "two-phase review", "two-verdict review", "spec compliance review", "code quality review", "whole-branch review", "final code review", "implementer status protocol", "model selection for subagents", "progress ledger", "context hygiene", "file handoff", "子代理驱动开发", "任务分派", "每个任务派发子代理", "实现子代理", "任务审查", "两阶段审查", "双结论审查", "规范合规审查", "代码质量审查", "整分支审查", "最终代码审查", "实现者状态协议", "模型选择", "进度台账", "上下文卫生", "文件交接"]
skill_id: "<SKILL:draft/skills/subagent-driven-development/SKILL.md>"
---

# subagent-driven-development

> **Status: draft** — adapted from superpowers (skills/subagent-driven-development). Incubating in draft/; not wired into the main /speckit.* flow.

## Overview

Execute an implementation plan by delegating each task to a purpose-built subagent instead of doing the work inline. The controller (you) never writes production code. Its whole job is orchestration: hand each task to a fresh implementer subagent, gate the result behind a two-verdict task review, run a fix-and-re-review loop until the gate is clean, mark the task complete in a durable progress ledger, and — after every task passes — dispatch one broad whole-branch review before finishing.

**Why subagents:** You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you keep them focused and give them exactly what they need — never your session's history. This also preserves your own context for coordination work, which is the scarce resource across a long plan.

**Continuous execution:** Do not pause to check in between tasks. Execute all tasks from the plan without stopping. The only reasons to stop are: a `BLOCKED` status you cannot resolve, ambiguity that genuinely prevents progress, or all tasks complete. "Should I continue?" prompts waste your partner's time — they asked you to execute the plan, so execute it.

**Narration:** between tool calls, narrate at most one short line — the ledger and the tool results carry the record.

**Relationship to the .specify agent triad:** Spec Kit ships a role-based agent triad (requirements-analyst → system-designer → module-designer → test-engineer → qa-engineer) for the `/speckit.*` flow. SDD is a lighter, self-contained loop that runs on the generic Agent/Task tooling: one implementer role and one reviewer role per task, dispatched fresh each time. You may map roles onto the triad if a project already uses it (e.g. dispatch the reviewer as qa-engineer), but SDD does not require it and defines everything it needs below.

## When to Use

Use SDD when **all** of the following hold:

- You have an implementation plan with discrete tasks (e.g. a `tasks.md` or a plan file with `## Task N` headings).
- The tasks are mostly independent — not so tightly coupled that they must be written together in one head.
- You want to stay in the current session (no handoff to a parallel session) and iterate continuously without a human in the loop between tasks.

Do **not** use SDD when: there is no plan yet (brainstorm and write one first), the work is a single tightly-coupled change (do it directly), or the tasks demand constant human judgement between them.

### Pre-flight plan review

Before dispatching Task 1, scan the plan once for conflicts:

- tasks that contradict each other or the plan's global constraints
- anything the plan explicitly mandates that the review rubric treats as a defect (a test that asserts nothing, verbatim duplication of a logic block)

Present everything you find to your partner as **one batched question** — each finding beside the plan text that mandates it, asking which governs — before execution begins, not one interrupt per discovery mid-plan. If the scan is clean, proceed without comment. The review loop remains the net for conflicts that only emerge from implementation.

## Core principle

**Fresh subagent per task + two-verdict task review (spec compliance + code quality) + broad final review = high quality, fast iteration.**

Four doctrines make this work, and none is optional:

1. **Fresh subagent per task.** Every implementer and every reviewer starts clean. A dispatch prompt describes *one task*, never the session's history. Never paste accumulated prior-task summaries into later dispatches.
2. **Two-phase task review.** Each task is gated by a reviewer that returns two verdicts — spec compliance (✅/❌/⚠️) and code quality (Approved / Needs fixes). Both are required; a report missing either is not accepted.
3. **File handoffs, never paste.** Task briefs, implementer reports, and review diffs move as files. Bulk artifacts never enter the controller's context.
4. **Durable progress ledger.** Completion is recorded in a file on disk, not only in memory, so a compaction cannot lose your place and cause re-dispatch of finished work.

## Per-task loop

Working files live under `draft/.sdd/` in the repo working tree (task briefs, implementer reports, review diffs, and `progress.md`). This is draft scratch; keep it git-ignored. Create it with a self-ignoring `.gitignore`:

```bash
root=$(git rev-parse --show-toplevel)
dir="$root/draft/.sdd"; mkdir -p "$dir"; printf '*\n' > "$dir/.gitignore"; echo "$dir"
```

At skill start, read the ledger and resume (see [Context hygiene & progress ledger](#context-hygiene--progress-ledger)). Then, for each task not already marked complete:

1. **Prepare the task brief.** Extract the task's full text to a file so it never passes through your context: `draft/.sdd/task-N-brief.md`. See [references/model-selection-and-progress.md](references/model-selection-and-progress.md) for a `task-brief`-style snippet. Record the current commit as **BASE** before dispatching — never `HEAD~1` later, which silently drops all but the last commit of a multi-commit task.

2. **Dispatch a fresh implementer subagent.** Use [assets/implementer-prompt.md](assets/implementer-prompt.md). Pick the model explicitly per [Model selection](#model-selection). The dispatch carries: one line on where this task fits; the brief path ("read this first — it is your requirements, use the exact values verbatim"); interfaces/decisions from earlier tasks the brief cannot know; your resolution of any ambiguity you spotted; and the report-file path (`draft/.sdd/task-N-report.md`). Exact values (numbers, magic strings, signatures, test cases) live only in the brief.

3. **Answer questions before work begins.** If the implementer asks clarifying questions, answer clearly and completely, then let it proceed. Do not rush it into implementation.

4. **Handle the implementer's status.** The implementer returns one of four statuses (under 15 lines; detail is in the report file):
   - **DONE** — proceed to review.
   - **DONE_WITH_CONCERNS** — read the concerns first. If they touch correctness or scope, address them before review; if they are observations ("this file is getting large"), note them in the ledger and proceed.
   - **NEEDS_CONTEXT** — provide the missing information and re-dispatch.
   - **BLOCKED** — assess the blocker: context problem → add context, re-dispatch same model; needs more reasoning → re-dispatch a more capable model; too large → split the task; plan is wrong → escalate to the human. **Never** ignore an escalation or force the same model to retry unchanged.

5. **Write the review diff file and dispatch the task reviewer.** Generate a review package for `BASE..HEAD` (commit list + `git diff --stat` + `git diff -U10`) into `draft/.sdd/review-<base7>..<head7>.diff` — see the `review-package` snippet in the reference. Dispatch the task reviewer ([assets/task-reviewer-prompt.md](assets/task-reviewer-prompt.md)) with three paths — the same brief, the report, and the diff file — plus the global constraints that bind this task (copied verbatim from the plan, not process rules). The reviewer returns two verdicts.

6. **Run the fix-and-re-review loop.** If spec is ❌ or quality is Needs fixes, dispatch **one** fix subagent (the implementer contract still applies — it re-runs the covering tests and appends results to the report file) with the complete Critical + Important findings list. Then regenerate the diff and re-dispatch the reviewer. Repeat until spec is ✅ **and** quality is Approved. Resolve every ⚠️ "cannot verify from diff" item yourself before marking complete — you hold the cross-task context the reviewer lacks; a confirmed gap is a failed spec review, send it back. Record Minor findings in the ledger for the final review to triage.

7. **Mark the task complete in the progress ledger.** Append one line in the same message as your other bookkeeping: `Task N: complete (commits <base7>..<head7>, review clean)`.

After all tasks are complete:

8. **Dispatch one broad whole-branch review.** Use [assets/final-code-reviewer-prompt.md](assets/final-code-reviewer-prompt.md) on the **most capable available model**. Generate a package for `MERGE_BASE..HEAD` (`MERGE_BASE = git merge-base <trunk> HEAD`) and hand it the printed path plus the accumulated Minor-findings list. If it returns findings, dispatch **one** fix subagent with the complete list — not one fixer per finding.

9. **Finish.** Once the whole-branch review is clean, hand off to the project's branch-completion flow (e.g. the `/speckit.*` merge/PR path or `git-workflow`). Done.

## Model selection

Use the **least powerful model that can handle each role** to conserve cost and increase speed, and **always specify the model explicitly** when dispatching — an omitted model silently inherits the session's model, often the most capable and most expensive, which defeats this entire section.

- **Mechanical implementation** (1–2 files, complete spec, or plan text that contains the code to transcribe) → cheapest tier.
- **Integration / judgment** (multi-file coordination, pattern matching, debugging) → standard tier.
- **Architecture / design**, and the **final whole-branch review** → most capable tier.
- **Reviewers** → scale to the diff's size, complexity, and risk; a mid-tier model is the floor.

**Turn count beats token price.** Wall-clock and context cost scale with how many turns a subagent takes, and the cheapest models routinely take 2–3× the turns on multi-step work — costing more overall. Use a mid-tier model as the floor for reviewers and for implementers working from prose; drop to the cheapest tier only when the task is transcription-plus-testing or a single-file mechanical fix.

Full doctrine with the complexity-signal table: [references/model-selection-and-progress.md](references/model-selection-and-progress.md).

## Context hygiene & progress ledger

**File handoffs.** Everything you paste into a dispatch — and everything a subagent prints back — stays resident in your context for the rest of the session and is re-read on every later turn. So move artifacts as files: task brief → `draft/.sdd/task-N-brief.md`; implementer report → `draft/.sdd/task-N-report.md`; review diff → `draft/.sdd/review-<base7>..<head7>.diff`. The controller reads only the short return message; bulk content never enters its context. Fix dispatches append to the same report file and return a short summary. Never make a subagent read the whole plan — hand it its brief.

**Constructing reviewer prompts (do not pre-judge).** Never tell a reviewer what *not* to flag or pre-rate a finding's severity ("treat as Minor at most"). If you believe something is a false positive, let the reviewer raise it and adjudicate it in the loop. A finding labeled plan-mandated — or any finding that conflicts with the plan's text — is the human's decision: present the finding beside the plan text and ask which governs. Do not add open-ended directives ("check all uses") without a concrete task-specific reason, and do not ask a reviewer to re-run tests the implementer already ran.

**Durable progress ledger.** Conversation memory does not survive compaction; controllers that lost their place have re-dispatched entire completed task sequences — the single most expensive failure observed. Track progress in `draft/.sdd/progress.md`, not only in todos:

- At skill start, read the ledger (`cat "$(git rev-parse --show-toplevel)/draft/.sdd/progress.md"` — absent on first run). Tasks marked complete there are **done** — do not re-dispatch them; resume at the first task not marked complete.
- The ledger is your recovery map: the commits it names exist in git even when your context no longer remembers creating them. After compaction, trust the ledger and `git log` over recollection.
- `git clean -fdx` destroys the ledger (git-ignored scratch); if that happens, recover from `git log`.

Ledger format and file-handoff snippets: [references/model-selection-and-progress.md](references/model-selection-and-progress.md).

### Red flags

**Never:**
- Start implementation on the trunk branch without explicit user consent.
- Skip task review, or accept a report missing either verdict (spec compliance AND code quality are both required).
- Move to the next task while the review has open Critical/Important issues.
- Dispatch multiple implementation subagents in parallel (they conflict).
- Make a subagent read the whole plan file — hand it its task brief.
- Skip scene-setting context, or ignore a subagent's questions.
- Accept "close enough" on spec compliance, or skip a re-review after fixes.
- Let implementer self-review replace actual review — both are needed.
- Tell a reviewer what not to flag, or pre-rate a finding's severity.
- Dispatch a task reviewer without a diff file — generate it first.
- Re-dispatch a task the ledger already marks complete — check the ledger (and `git log`) after any compaction or resume.
- Omit the model on a dispatch (it inherits the most expensive one).

## Resources

### Assets (`assets/`)
- `implementer-prompt.md` — implementer subagent dispatch template (6-step job, TDD RED/GREEN evidence, self-review checklist, four-status protocol, <15-line return).
- `task-reviewer-prompt.md` — two-verdict task reviewer template (Part 1 Spec Compliance ✅/❌/⚠️; Part 2 Code Quality; "Do Not Trust the Report"; Critical/Important/Minor calibration; output format).
- `final-code-reviewer-prompt.md` — broad whole-branch review template for the final gate before finishing.

### References (`references/`)
- `model-selection-and-progress.md` — model-selection doctrine (complexity signals, turn-count economics), the progress-ledger format, and the file-handoff / context-hygiene rules with `task-brief` / `review-package` / `sdd-workspace` helper snippets adapted to `draft/.sdd/`.
