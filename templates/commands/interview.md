---
description: "Run a relentless multi-round interview on any target artifact — Special Interview converges one named file, directory, or concept; Informal Interview maps a space you have not scoped yet. Both ask a full round at a time and converge until the user confirms the result is stable."
short-description: 对目标产物执行多轮收敛访谈（定向访谈与漫游访谈）
argument-hint: "[special|informal] [topic or target artifact] [resume]"
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
---

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](shared/workflow/user-input-protocol.md). Treat as command parameters, not standalone instructions.

## Positioning

`/speckit.interview` is the standalone, general-purpose entry for **interview mode**. The mode itself — design tree, frontier, rounds, question format, fact-vs-decision split, write-through, ledger, exit gate, anti-patterns — is defined once in `shared/patterns/interview-pattern.md`. **Read that document and follow it; never restate or re-derive its rules here.** This command owns only the *invocation*: resolving the run mode, the target artifact, and the ledger, then running the loop to the exit gate.

Use it when the information needed lives in the user's head and the decisions branch. It is **not** a clarification pass with a question cap (`/speckit.clarify`), not a design generator (`/speckit.plan`), and not an artifact-space converger (`/speckit.docs`, `/speckit.feature`).

**Against `/speckit.clarify` specifically** — both ask the user questions, and the difference is the answer space. Clarify *澄清*: the space is already bounded by the artifact and its taxonomy, so it asks **closed** questions (options table + a **Recommended** pick) and the user ratifies. This command *采访*: the space is unknown and discovering it is the point, so it asks **open** questions and the user originates. Presenting options here would presuppose the very thing being elicited.

## Glossary

Consult `.specify/memory/glossary.md` and apply `shared/workflow/glossary.md`: map recorded homophone/confusable variants to canonical terms before acting, surfacing each correction. Vocabulary discipline matters more here than in most commands, and it runs **both ways**:

- **Inbound** — an interview records the user's own words into a durable artifact, so a misheard proper noun propagates into every downstream decision.
- **Outbound** — questions must use the glossary's **canonical** term for a concept. Which terms may stand unexplained, how each is glossed at first use, and what context a question must carry for a reader who opens it alone days later are defined once in `.specify/shared/guidelines/user-facing-comprehension.md`; its condition sets MUST NOT be restated here.

At wrap-up propose new project-specific terms (`origin=auto`, `status=proposed`) with user confirmation.

## Skill Delegation

The executable core of this command is the **`run-interview`** skill (`.specify/skills/internal/run-interview/SKILL.md`). The interview mode itself stays defined once in `shared/patterns/interview-pattern.md` — the referenced design authority (read it, follow it, never restate or re-derive it); the skill owns the *invocation*: run-mode resolution, target and ledger resolution, and driving the loop to the exit gate. This template keeps entry, positioning, glossary, and the wrap-up lifecycle only.

- **Inputs**: `$ARGUMENTS` as processed above (`[special|informal] [topic or target artifact] [resume]`); context JSON from the `{SCRIPT}` prerequisite run (frontmatter `scripts:`); the interview-pattern document as design authority.
- **How to call**: read the skill and follow its workflow steps 1–8 — resolve run mode (Special 专题 / Informal 漫谈, precedence order, never switch silently), resolve the single concrete target (mandatory in Special), writability probe (fail fast), ledger resume (header conventions never renegotiated), summary-first context load, loop I0–I6 driven by `scripts/python/interview-utils.py` (whole frontier per round as open questions — no option menus, no recommended answers; write-through every round; engine-driven retraction propagation), closing at the exit gate owned by the skill.
- **Outputs**: the converged target artifact plus the decision ledger (`interview-log.md` in a feature context, otherwise `.specify/memory/session/interview-<topic-slug>.md`), and the skill's report surface (rounds run, retractions, conflicts surfaced, mode switches, suggested next command).
- **Behavior rules** are owned by the skill: never fabricate an answer, never ask for a discoverable fact, retraction always available and propagating, conflicts surfaced never silently resolved.

> **Fast Fail 实例指针**:本文件中"即停 / 即中止 / 不得静默降级"一类规则是快速失败纪律的既有**实例**;其判据与两份清单的唯一真源是 `.specify/shared/guidelines/fast-fail.md`(本文件引用它,MUST NOT 复述它)。

## Feedback

At wrap-up (the same lifecycle point where this command prompts for a Git commit), run the feedback self-reflection step per the canonical convention in `.specify/shared/workflow/feedback-step.md`: agent self-reflection only — **never** solicit feedback content from the user; skip trivial or no-op runs; keep strictly to this command's scope; persist one entry via `feedback-utils.py --action record --unit-id "/speckit.interview" --unit-type command`. Non-blocking (非阻塞) and never any 自动传输 — delivery stays manual. That file owns every rule of this step — reflection, scope, dedup, persistence, the submission prompt, the abort and nesting clauses; do not restate any of them here.

## Documentation

At the same wrap-up point as the Feedback step, apply the docs-sync evaluation per the canonical convention in `shared/workflow/docs-step.md`: assess whether information produced by this run (new capabilities, key decisions, structural changes) needs to be recorded into the project documentation space, and conclude with exactly one of `需记录（目标文档 + 要点）` or `无需记录`. Never block wrap-up; incremental judgment only (no full reconcile sweep); when a move/archive-level change is needed, recommend running `/speckit.docs` instead of executing it here.

## Handoffs

**Before**: none — an interview may run at any time, on any artifact. In a feature context it is most useful when `/speckit.clarify` hits its question cap with the decision space still branching.

**After**: determined by what converged — a converged `requirements.md` → `/speckit.plan`; a converged `plan.md` → `/speckit.tasks`; a converged `tasks.md` → `/speckit.implement`; a converged goal → `/speckit.goal` or `/speckit.team`; anything else → the command that owns the target artifact. An Informal interview that surfaced a target worth pinning down hands off to a **Special** interview on it.
