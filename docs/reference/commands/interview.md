# /speckit.interview

Run a relentless multi-round interview on any target artifact: elicit what only you know, write every answer through immediately, and converge until you confirm the result is stable.

The mode itself is defined once in `.specify/shared/patterns/interview-pattern.md`. This page documents the command; read the pattern for the mechanics.

## When to Use

- A decision space **branches** — each answer unlocks questions that did not exist before it, so a fixed questionnaire cannot cover it
- The information lives in **your head** (intent, priority, trade-off acceptance), not in the repo, the docs, or a tool
- [`/speckit.clarify`](clarify.md) hit its 5-question cap with critical ambiguities still open
- [`/speckit.plan`](plan.md) cannot fill Technical Context without inventing decisions you never made
- A long elicitation must survive across sessions or days — the ledger carries it

Do **not** use it for facts the agent can look up, for a single yes/no approval, for read-only analysis ([`/speckit.analyze`](analyze.md), [`/speckit.review`](review.md)), or in an unattended run.

## Syntax

```text
/speckit.interview [topic or target artifact] ["resume"]
```

Both arguments are optional. Naming a path or artifact pins the target; naming a topic starts a fresh interview; `resume` continues from an existing ledger.

## Execution Flow

1. **Resolve context** — Runs the prerequisites script for repo root, branch, requirement ID, and artifact paths. A non-feature branch is not an error; it selects the non-feature ledger location.

2. **Resolve the target artifact** — What converges, in precedence order: a path named in the arguments → the current phase's primary artifact (`tasks.md` → `plan.md` → `requirements.md`, first that exists) → a new interview record. The resolved target is stated back to you before anything is asked.

3. **Writability probe** — Verifies the target and its directory are writable *before* generating questions, so a permissions problem cannot cost you a session's answers.

4. **Resolve the ledger and resume** — In a feature context `<REQUIREMENTS_DIR>/interview-log.md`, otherwise `.specify/memory/session/interview-<topic-slug>.md`. An existing ledger's header conventions are read and never renegotiated; already-settled branches are reported rather than re-asked.

5. **Run the loop** (`I0`–`I5` of the pattern):
   - Seed the **design tree** from the target artifact, the surrounding context, and your input
   - Compute the **frontier** — every decision whose prerequisites are already settled
   - Dispatch subagents for environment **facts**, without blocking the round
   - Ask the **whole frontier in one round**, numbered, each with a recommended answer — then wait
   - **Write through** to the target artifact (overwrite-style, latest round wins) and update the ledger, then recompute the frontier

6. **Exit gate** — When the frontier is empty, the consolidated understanding is presented and **your explicit confirmation** is required. Reopening a branch puts it back in the tree and the loop continues. An empty frontier is the agent's opinion; the confirmation is yours.

## Question Format

Every question is numbered and carries a recommended answer, which turns an interrogation into a review:

```text
❓ **Q1** — **Storage backend**: The ledger needs to survive across sessions. Options: (a) a
file beside the spec, (b) a central store, (c) conversation-only.

➡️ (a) — it matches the existing walkthrough-ledger convention and keeps the trail next to
the artifact it serves.
```

## Guarantees

| Guarantee | What it means |
|-----------|---------------|
| **Facts are the agent's job** | You are never asked for something discoverable from the code, config, or docs |
| **Decisions are yours** | Intent, priority, and trade-offs are put to you and waited on — never inferred |
| **Write-through** | Each round lands in the artifact before the next round is asked; nothing is banked |
| **No fabrication** | An unasked branch stays open in the ledger; it is never filled in to look finished |
| **Resumable** | Interruption stops at a round boundary with the ledger complete and a stated resume point |
| **You end it** | The session closes on your confirmation, not on the agent running out of questions |

## Prerequisites

None. An interview may run at any time, on any artifact. In a feature context it is most useful when [`/speckit.clarify`](clarify.md) reaches its cap with the decision space still branching.

## Next Steps

Determined by what converged:

- `requirements.md` → [`/speckit.plan`](plan.md)
- `plan.md` → [`/speckit.tasks`](tasks.md)
- `tasks.md` → [`/speckit.implement`](implement.md)
- a goal → [`/speckit.goal`](goal.md) or [`/speckit.team`](team.md)
- anything else → the command that owns that artifact

## Example

```text
/speckit.interview plan.md
```

Resolves `plan.md` as the target, resumes any existing ledger, then asks the whole askable frontier per round — each question numbered with a recommendation — writing your answers into the plan as you go, until you confirm the design is stable.
