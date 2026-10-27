# `/speckit.improve`

Active trigger of the self-improvement flow: resolve one improvement target, read its run-determination history (why), qualify evidence into a frozen candidate list (what), then route each candidate to the canonical improver (how). The command is a thin entry-plus-delegation shell — every loop step is owned by `shared/workflow/self-improvement-workflow.md` (SI-0…SI-9) and executed by the `self-improvement` skill (`skills/internal/self-improvement/SKILL.md`, installed at `.specify/skills/internal/self-improvement/SKILL.md`).

## When to Use

- After a completed run of an Execution Subject left a concern worth investigating (a recurring failure, a friction the user names, one axis of the run determination regressing)
- When a framework-unit finding from `/speckit.review` or the feedback digest names a specific skill, agent, tool record, or team definition as the subject
- When a client project's own feedback channel (`kind: external` entries) points at a `custom:<owner>/<name>` artifact that meets the Execution Subject criteria

## Syntax

```text
/speckit.improve <target> [scope narrowing]
```

The target resolves to exactly **one** Execution Subject (criteria owner: `shared/definitions/self-improvement-definitions.md` § Execution Subject — five criteria, applied unchanged to every subject kind, custom subjects included):

| Target form | Subject kind |
|---|---|
| `/speckit.<command>` | command template (pending row — no improver yet, see below) |
| `skill:<name>` | Skill |
| an agent artifact (role slug or `.specify/agents/...` path) | agent |
| a tool record (name / alias / `tool_id` under `.specify/memory/tools/`) | tool record |
| a team (slug or `.specify/teams/<slug>/team.md`) | team definition |
| `custom:<owner>/<name>` | host-project custom unit |

If the stated target resolves to no durable artifact with a canonical owner, it is not an Execution Subject: the loop halts at subject resolution (SI-0), reports 「没有唯一所有者」(no unique editable definition), records the observation for a follow-up carrier (e.g. `/speckit.todo` Park Mode), assumes no ownership, and mutates no file. If `$ARGUMENTS` is empty and the conversation does not unambiguously name the target, the command asks one targeted question — it never guesses a subject silently.

## Segments — why → what → how

**Step 1 — why: read the target's run-determination history.** `python3 .specify/scripts/python/run-determination.py --action history --target "<unit-id>" --json` (optional `--limit` / `--unsettled`). The output shape is the engine's; an axis with a non-null `reason` is reported as not evaluated, never as fine, and an empty history proves nothing about past runs. Corroboration rides the session-history lane (`memory-utils.py --action recall --scope session`), index rows only.

**Custom subjects (`custom:<owner>/<name>`) — observation source and disclosure.** A custom subject has no run-determination history the engine can persist: the engine's source contract accepts only command and skill unit forms and fail-closes with `persisted: false` plus its reason — `the memory engine's --source contract does not accept <unit-id>; the record is emitted but not landed`. The why digest for a custom subject therefore states the disclosure 「运行判定历史未评估」 with that engine reason verbatim, and observes through this unit's `kind: external` feedback entries (`feedback-utils.py --action list --kind external --unit-id "<unit-id>"`) plus the existing evidence lanes (`shared/workflow/evidence-step.md`, cited, never restated). No invented source string, no forged history, and an empty engine history is never read as "past runs were fine". Widening the engine's source contract is its owner's action, outside this command.

**Step 2 — what: qualify and freeze evidence.** SI-2 per the workflow, via `evidence-utils.py` (`latest` / `list` / `collect`); only the per-finding projection and the top-level findings digest are consumed — never `findings.json` wholesale, never raw lane files. The candidate list freezes once evidence states are classified: no qualified candidate → close as no-op and keep the observations; cross-subject or systemic candidate → escalate without broad local mutation.

**Step 3 — how: diagnose, critique, route, apply, validate, record.** Diagnosis names the affected Better-Harness dimension by reference; every proposal carries one executed falsification attempt before dispatch (owner: `shared/guidelines/critique-and-self-critique.md`). Routing keeps the existing dispatch table:

| Subject kind | Route to |
|---|---|
| Agent Template/Instance/config | `improve-agent` |
| Skill | `improve-skills` |
| Tool record | `improve-tools` |
| Team definition | `improve-team` |

A command template is an Execution Subject but has no improver yet — it degrades to Assisted Improvement (edit `templates/commands/<name>.md` in the framework source, regenerate per-tool copies with `regen-command-copies.py`, then validate; in a client project, route the finding through `/speckit.feedback` upstream instead of editing generated copies). A `custom:<owner>/<name>` target routes by what the artifact actually is; when no row fits, it follows its normal assisted flow — this command adds no client improver. The command never mutates a subject itself.

## Preserved loop constraints

- Exactly one intervention ledger (Step E's `intervention.json`, beside the baseline evidence run) — no second store, no aggregate score over the run-determination axes.
- The attempt limit is a hard limit: reaching it stops automatic iteration and demands assisted review.
- A passing check supports only **intervention applied; outcome pending** — the outcome is reported pending until SI-8's comparison of comparable runs completes, never as "improved" on validation alone.

## Wrap-up

The command's wrap-up records its own run determination, exec quant, and feedback entry per the compiled `## Wrap-up` step, then the routed improver's report returns with outcome pending and the next comparison point. A client project's findings about framework assets route through `/speckit.feedback` — never through a direct edit of framework-owned surfaces.

## See Also

- Execution order and constraints: [Self-Improvement Workflow](../../shared/workflow/self-improvement-workflow.md) (canonical at `shared/workflow/self-improvement-workflow.md`)
- Concepts: `shared/definitions/self-improvement-definitions.md` · policy: `shared/guidelines/self-improvement.md`
- Evidence lanes and the intervention ledger: `shared/workflow/evidence-step.md`
- Client feedback channel: [Feedback Command](feedback.md) (`kind: external` entries, the custom subject's observation source)
