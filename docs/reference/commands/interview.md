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

## Run Modes

Standalone invocation has two run modes. **Both ask a full round at a time** — the whole askable frontier in one message, as open questions — then wait, write through, and recompute. They differ in **what is being converged**, and therefore in what each round's write does.

### Special Interview (专题访谈) — converge one target

Pins down **one** thing: the description or definition of a named file, directory, or concept. A single concrete target is **mandatory**, and the design tree stays bounded to it — answers implying changes elsewhere are recorded as out-of-scope rather than acted on.

Each round: ask the frontier → **edit that one target in place** → **show the change back**, so you see your decisions as recorded text and can correct a misread before the next round.

Converged when the definition is complete and internally consistent **and** you confirm.

### Informal Interview (漫谈访谈) — map a space

**Maps a space** whose shape is not yet known. May start from a bare topic, and the set of artifacts can legitimately grow as the map forms.

Each round: ask the frontier → **consolidate and organize** — reconcile the answers against each other (a later one may qualify an earlier one), group them by area, and split or add artifacts as the shape emerges. Which areas grew is reported back, so you watch the map form rather than only the answers.

Converged when the frontier is empty, every area has a home, **and** you confirm.

### Which one runs

Resolved before the first question: an explicit `special` / `informal` argument wins; then a resumed ledger's recorded mode; then a concrete file/directory/concept target implies **Special** and a broad topic implies **Informal**; if still ambiguous you are asked once. The resolved mode and its reason are stated back to you and recorded in the ledger header.

Switching mid-interview happens **only when you ask for it**, and is recorded as a ledger header amendment. An Informal round that exposes a target worth pinning down offers a Special interview on it rather than quietly deep-diving.

## Syntax

```text
/speckit.interview [special|informal] [topic or target artifact] [resume]
```

All arguments are optional. Naming a path or artifact pins the target; naming a topic starts a fresh interview; `resume` continues from an existing ledger.

## Execution Flow

1. **Resolve context** — Runs the prerequisites script for repo root, branch, requirement ID, and artifact paths. A non-feature branch is not an error; it selects the non-feature ledger location.

2. **Resolve the target artifact** — What converges, in precedence order: a path named in the arguments → the current phase's primary artifact (`tasks.md` → `plan.md` → `requirements.md`, first that exists) → a new interview record. The resolved target is stated back to you before anything is asked.

3. **Writability probe** — Verifies the target and its directory are writable *before* generating questions, so a permissions problem cannot cost you a session's answers.

4. **Resolve the ledger and resume** — In a feature context `<REQUIREMENTS_DIR>/interview-log.md`, otherwise `.specify/memory/session/interview-<topic-slug>.md`. An existing ledger's header conventions are read and never renegotiated; already-settled branches are reported rather than re-asked.

5. **Run the loop** (`I0`–`I6` of the pattern):
   - Seed the **design tree** from the target artifact, the surrounding context, and your input, then **plan branch isolation** — independent branches first, and the most widely-depended-on questions asked earliest
   - Compute the **frontier** — every decision whose prerequisites are already settled
   - Dispatch subagents for environment **facts**, without blocking the round
   - Ask **the whole frontier in one round** — each question self-contained: ID, plain-language title, its **Context** as a quote block, then an **open question** (no options, no recommendation) — then wait
   - **Write through** (overwrite-style, latest round wins), recording each decision's **ID, dependencies, and artifact span**: Special edits the one target and **echoes the change back**; Informal **reconciles and organizes** the round into records. Then recompute the frontier
   - A retracted answer at any point re-enters at **`I6`** and propagates (see [Changing Your Mind](#changing-your-mind-翻供))

6. **Exit gate** — When the mode's convergence criterion is met, the consolidated understanding is presented and **your explicit confirmation** is required. Reopening a branch puts it back in the tree and the loop continues. An empty frontier is the agent's opinion; the confirmation is yours.

## Question Format

A question you have to decode is a question you answer badly, so every question ships with **its own context** — you should never need to scroll back, reconstruct what was decided earlier, or ask what a word means. And the question itself is **open**: no option menu, no recommended answer.

```text
❓ **D4** — **Retry behaviour for failed messages**

> **Context**: You chose a message queue for storage (D1) and Redis as the queue (D3).
> Redis Streams has no built-in retry limit, so whatever we do here we have to build.
> Your answer will be written into `## Storage > Retry policy` of `plan.md`, and it
> shapes what happens to a message that keeps failing — including whether we need a
> holding area for messages that exhausted their retries.

What should happen when processing a message fails?
```

### Why no options, and no recommendation

This is the difference between **interviewing (采访)** and **clarifying (澄清)**:

| | [`/speckit.clarify`](clarify.md) | `/speckit.interview` |
|---|---|---|
| The answer space | **Already known** — bounded by the artifact and its taxonomy | **Unknown** — discovering it is the point |
| Question shape | **Closed**: options table + a **Recommended** pick | **Open**: you define the space |
| Your role | You ratify or correct a proposal | You originate the answer |

An option menu asserts that the agent already knows the possibilities. In an interview it usually does not — and being shown three choices makes you pick the closest one instead of saying what was actually on your mind. The good answer is often the option nobody listed. A recommendation has the same problem in a subtler form: you read it, find it plausible, agree, and what ends up in the artifact is the agent's opinion wearing your name.

If you are stuck, ask — you will get examples as **explicitly non-exhaustive illustrations**, never renumbered into a menu and never with one marked as recommended.

### How prompts are presented

The rule is **whatever shows the prompt best**: if your agent CLI has a tool that presents a given prompt more clearly than plain text, it is used; if nothing fits, the prompt arrives as **markdown or plain text**. A tool is used for what it does for you as the reader, never because it happens to exist.

Fit depends on the prompt's shape. A **choice widget** (`AskUserQuestion` in this CLI: a few preset options plus an "Other" escape) is a good surface for a genuinely closed question and a bad one for an open question, because seeing three choices pulls you toward the closest instead of what you actually think:

| Prompt | How it appears |
|--------|----------------|
| The interview questions themselves | **Markdown**, open — no widget fits an unknown answer space |
| Which run mode to use | Choice widget, where available |
| Which of two conflicting decisions gives way | Choice widget, where available |
| Keep a decision after a retraction, or re-answer it | Choice widget, where available |
| Park a branch as out of scope | Choice widget, where available |
| Final confirmation, or reopen a branch | Choice widget, where available |

If your CLI has no suitable tool — or none at all — the same prompts arrive as plain text. Nothing about the loop changes, and no question is skipped over a missing tool.

### What the format guarantees

| Rule | Why |
|------|-----|
| **Context is mandatory**, set apart as a blockquote — why now, what it builds on, what it changes | An answer given without knowing what it affects is a guess; the quote block keeps background and question visually separate |
| **Open questions only** — no options, no recommendation | Presenting choices anchors you; recommending one records the agent's view as yours |
| **"What", not "whether"** | "Should we retry 3 times?" collapses the space into ratifying a proposal |
| **Earlier decisions are named, not just cited** — "Redis as the queue (D3)", never a bare `D3` | You should not have to look up your own history |
| **Plain language, your vocabulary** — not the codebase's internals | "What should happen when a message fails?" beats "what is the `max_retry` semantic?" |
| **Special terms glossed inline, every question** | You may read one question in isolation, days later |
| **One decision per question** | A question with "and" in it hides two answers |

The ID is your handle: "change D3" is all it takes to retract an answer later.

## Changing Your Mind (翻供)

Answers are not final, and revising one is expected rather than an interruption. Each decision is recorded with a stable **ID**, the premises it **depends on**, and the **span of the artifact it wrote** — which is what lets a change propagate instead of leaving contradictions behind.

When you retract a decision, the command:

1. Walks the recorded dependency edges to find **everything reachable** from it — not just the immediate next question
2. Sorts those into **still valid** (with the reason they survive), **needs confirmation** (re-asked openly, showing what you said before as context — not as a recommendation to accept), and **invalidated**
3. **Rolls back the invalidated spans** in the artifact, so no text derived from the old premise survives
4. **Re-opens** the invalidated decisions and re-asks them in dependency order
5. **Records the retraction** — what changed, what was invalidated, what was kept and why

Two consequences worth knowing: the most widely-depended-on questions are asked **first**, so a late change of mind costs less; and a retraction raised at the final confirmation gate simply reopens the loop — the gate is not a point of no return.

## Guarantees

| Guarantee | What it means |
|-----------|---------------|
| **Facts are the agent's job** | You are never asked for something discoverable from the code, config, or docs |
| **Decisions are yours** | Intent, priority, and trade-offs are put to you and waited on — never inferred |
| **Write-through** | Every round lands in the artifact before the next round is asked; nothing is banked |
| **Retraction propagates** | Revising an answer re-asks whatever depended on it and rolls back what it wrote — never a silent local edit |
| **Conflicts are surfaced** | When two answers disagree, both are named and you choose which gives way; nothing is quietly overwritten |
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

## Examples

**Special** — pin down one target's definition:

```text
/speckit.interview special .specify/shared/patterns/interview-pattern.md
```

Resolves the file as the single target, then asks the whole askable frontier each round — editing the document and showing you the change after every round — until the definition is complete and you confirm it. Branches that are not about this file are recorded as out-of-scope rather than acted on.

**Informal** — map a space you have not scoped yet:

```text
/speckit.interview informal "how we want release automation to work"
```

Asks the whole askable frontier each round, then reconciles the answers against each other and organizes them into records — splitting or adding artifacts as the shape emerges — and reports which areas grew before the next round. When a round exposes something worth pinning down properly, it offers a Special interview on that target rather than quietly deep-diving.
