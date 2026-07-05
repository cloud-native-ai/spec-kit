# P010 — Command Catalog Expansion

- **Status:** Draft
- **Pillars:** Commands
- **Source projects:** intellegix-code-agent-toolkit, superpowers
- **Value:** M–H · **Effort:** L–M · **Phase:** 1
- **Related:** [[P003]], [[P004]], [[P006]]

## Problem / Gap

spec-kit's `/speckit.*` catalog covers the core SDD spine well: `constitution`, `requirements`,
`clarify`, `plan`, `research`, `tasks`, `analyze`, `implement`, `review`, `checklist`,
`feature`, `agents`, `skills`, `tools`, `instructions` (see `templates/commands/*.md`). But the
catalog stops at the *spine*. It has no commands for the recurring moments *around* the spine
that a universal agent-coding framework needs:

- **No completeness gate** after implement (were tasks actually built, or stubbed?).
- **No design front-door** before spec (a vague idea → a reviewed spec).
- **No debugging entrypoint**, no **issue → reproduce → fix** flow.
- **No convergence/self-critique** step for plans and analyses (all single-pass today).
- **No session hygiene** commands (handoff between sessions, self-audit when going in circles).
- **No orchestration entrypoint** for the parallel task graph that `tasks.md` already implies.

intellegix's 40-command catalog and superpowers' skill-flow expose exactly these high-value
commands. This proposal distills the non-personal, provider-neutral subset into new
`/speckit.*` commands, expressed in the existing command-template idiom and wired with
`handoffs` into the current flow. Many are thin command wrappers over the [[P003]] skills.

## Proposal

Add a grouped set of new `/speckit.*` command templates under `templates/commands/` (draft
first). Each is a small markdown prompt with `description`, `handoffs`, and (where useful) a
`scripts:` prerequisite, exactly like `templates/commands/plan.md` and `review.md`. Skip all
provider-coupled (Perplexity/council) and domain-specific (game-dev, Raken, spreadsheet)
commands; replace external-provider transport with spec-kit's own harness tools (WebSearch /
WebFetch / MCP) and the [[P003]] skills.

### Grouped command catalog

| Group | Command | Purpose | Source |
|-------|---------|---------|--------|
| **Quality & audit** | `/speckit.verify-completeness` | Stub/skeleton audit; cross-check `tasks.md` ↔ changed code | intellegix `stub-check.md` |
| | `/speckit.verify` | Fresh-evidence completion gate before claiming done | superpowers `verification-before-completion` |
| | `/speckit.health-check` | Read-only project health probe with a read-only trust contract | intellegix `health-check.md` |
| **Debug & fix** | `/speckit.debug` | Root-cause-first debugging entrypoint | superpowers `systematic-debugging` |
| | `/speckit.fix-issue` | Issue → failing test → fix → verify | intellegix `fix-issue.md` |
| **Design & converge** | `/speckit.brainstorm` | Pre-spec design dialogue feeding `/speckit.specify` | superpowers `brainstorming` |
| | `/speckit.converge` | Adversarial self-critique + revision loop on an artifact | intellegix `extended-research.md`, `research-perplexity.md` |
| **Orchestration** | `/speckit.orchestrate` | Fan out independent `[P]` tasks to isolated workspaces | intellegix `orchestrator-multi.md` |
| | `/speckit.worktree` | Create/teardown an isolated feature workspace | superpowers `using-git-worktrees` |
| **Lifecycle & session** | `/speckit.handoff` | Session handoff doc (changes, decisions, blockers, next) | intellegix `handoff.md` |
| | `/speckit.finish` | Structured branch-completion menu (merge/PR/keep/discard) | superpowers `finishing-a-development-branch` |
| | `/speckit.session-audit` | Retrospective self-diagnostic when going in circles | intellegix `session-audit.md` |

## Design sketch

New command files land under `templates/commands/` (draft), each ≤~120 lines, factoring heavy
logic into the corresponding [[P003]] skill rather than a mega-prompt (intellegix's 800–1174-line
commands are an explicit anti-pattern). Detail for the top 8:

### 1. `/speckit.verify-completeness`

```yaml
---
description: Audit the implementation for stubs, skeletons, and unfinished work; cross-check each tasks.md item against changed code.
handoffs:
  - label: Analyze Consistency
    agent: speckit.analyze
    prompt: Run a cross-artifact consistency analysis on the flagged gaps.
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
---
```

Body: invoke the `stub-check` skill ([[P003]]) — Grep/Glob for stub markers, map findings to
`tasks.md` items, report incomplete/shallow tasks. Read-only; no fixes.

### 2. `/speckit.verify`

```yaml
---
description: Completion gate — require fresh command evidence before any done/passing/fixed claim.
handoffs:
  - label: Finish Feature
    agent: speckit.finish
    prompt: Proceed to branch completion now that verification passed.
    send: false
---
```

Body: invoke `verification-before-completion` ([[P003]]); run the relevant test/build/lint,
read the output, then report pass/fail with the evidence quoted. Pairs with [[P006]].

### 3. `/speckit.debug`

```yaml
---
description: Root-cause-first debugging entrypoint — reproduce, trace to the true cause, fix the cause, verify.
handoffs:
  - label: Write Failing Test
    agent: speckit.implement
    prompt: Implement the fix behind a failing test that reproduces the root cause.
    send: false
---
```

Body: invoke `systematic-debugging` ([[P003]]); escalate to `dispatching-parallel-agents` for
multi-domain failures. Terminal state hands the confirmed root cause into a TDD fix.

### 4. `/speckit.fix-issue`

```yaml
---
description: Turn a bug report / issue into a failing test, a root-cause fix, and verification.
handoffs:
  - label: Debug Root Cause
    agent: speckit.debug
    prompt: Trace the reported symptom to its root cause first.
    send: true
  - label: Verify
    agent: speckit.verify
    prompt: Verify the fix with fresh evidence.
    send: false
---
```

Body: parse the issue (`$ARGUMENTS` or a URL via WebFetch — never a specific provider),
reproduce with a failing test, delegate to `/speckit.debug`, fix, then `/speckit.verify`.
Reconceived from intellegix `fix-issue.md`, provider-neutral.

### 5. `/speckit.brainstorm`

```yaml
---
description: Collaborative pre-spec design dialogue that shapes a vague idea into a reviewed design note.
handoffs:
  - label: Write Specification
    agent: speckit.specify
    prompt: Turn the approved design into a formal specification.
    send: true
---
```

Body: invoke `brainstorming` ([[P003]]) — one question at a time, 2–3 approaches, gate against
coding before approval, write + self-review a short design note. This is the missing front door
*before* `/speckit.specify`.

### 6. `/speckit.converge`

```yaml
---
description: Run an adversarial self-critique and single-revision loop over a spec-kit artifact until it converges.
handoffs:
  - label: Adjust Plan
    agent: speckit.plan
    prompt: Apply the converged revisions to the implementation plan.
    send: false
scripts:
  sh: scripts/bash/check-prerequisites.sh --json
---
```

Body: take an artifact (plan/analyze/spec output) + a rubric; score 1–10 with
strengths/weaknesses/critical-issues, revise once, re-score, stop on convergence
(score ≥ 8 and critical-issues = 0, or gain < 1, or max 3 iterations). **No external provider**
— same-model self-critique. Wire-able as an optional final step of `/speckit.plan` and
`/speckit.analyze`. Distilled from intellegix `extended-research.md` (convergence rubric,
adversarial floor) with the Perplexity transport dropped.

### 7. `/speckit.orchestrate`

```yaml
---
description: Fan out independent [P] task groups from tasks.md to isolated workspaces, monitor, and reconcile.
handoffs:
  - label: Verify Completeness
    agent: speckit.verify-completeness
    prompt: Audit the merged results for stubs and gaps.
    send: true
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks
---
```

Body: read `tasks.md`, apply a **justification gate** (only parallelize genuinely independent
`[P]` groups), assign each to a worktree-isolated agent via `using-git-worktrees` +
`dispatching-parallel-agents` ([[P003]]), monitor, and provide a `status`/`off` teardown.
This is the command entrypoint for the deeper engine in [[P004]]; the orchestrator role never
edits source itself (strict role boundary from intellegix `orchestrator.md`).

### 8. `/speckit.handoff`

```yaml
---
description: Write a session handoff document — files changed, decisions and rationale, blockers, next steps.
handoffs:
  - label: Session Audit
    agent: speckit.session-audit
    prompt: If the session stalled, run a retrospective self-diagnostic.
    send: false
---
```

Body: emit `handoff.md` into the current feature dir under `.specify/specs/<NNN>/`. Harness-
agnostic; from intellegix `handoff.md`.

The remaining catalog entries (`/speckit.health-check`, `/speckit.worktree`, `/speckit.finish`,
`/speckit.session-audit`) follow the same idiom — thin wrappers with `handoffs`, delegating to
the [[P003]] skills or a read-only probe. `/speckit.health-check` carries the read-only
"trust contract" (a single read-only code path) from intellegix `health-check.md`.

## Source evidence

- intellegix command catalog → `/cws_work/intellegix-code-agent-toolkit/commands/`: `stub-check.md` (3-phase completeness audit), `health-check.md` (read-only 3-layer probe + TRUST CONTRACT), `fix-issue.md` (issue→failing test→fix→verify), `extended-research.md` + `research-perplexity.md` (convergence rubric, adversarial floor, mandatory critique-before-finalize), `orchestrator.md` + `orchestrator-multi.md` (role boundary, multi-agent justification gate, worktrees, `off` teardown), `handoff.md`, `session-audit.md`.
- superpowers flows → `/cws_work/superpowers/skills/`: `brainstorming/SKILL.md` (pre-spec dialogue, terminal→writing-plans), `verification-before-completion/SKILL.md`, `systematic-debugging/SKILL.md`, `using-git-worktrees/SKILL.md`, `finishing-a-development-branch/SKILL.md`, `dispatching-parallel-agents/SKILL.md`.
- spec-kit command idiom to match → `templates/commands/plan.md` (frontmatter `description` + `handoffs` + `scripts.sh`), `templates/commands/review.md` (multi-handoff + `check-prerequisites.sh` flags), `templates/commands/skills.md` (orchestration-entrypoint pattern); prerequisite scripts under `scripts/bash/`.

## Adoption plan

**Phase 1, draft command templates first, no change to the existing spine:**

1. **Quality & audit first** — `/speckit.verify-completeness` and `/speckit.verify`; they are
   thin wrappers over the P0 [[P003]] skills and immediately harden the flow.
2. **Design & converge** — `/speckit.brainstorm` (front door) and `/speckit.converge` (optional
   final step for `plan`/`analyze`, opt-in so single-pass stays the default).
3. **Debug & fix** — `/speckit.debug`, `/speckit.fix-issue`.
4. **Lifecycle & session** — `/speckit.handoff`, `/speckit.finish`, `/speckit.session-audit`,
   `/speckit.health-check`.
5. **Orchestration** — `/speckit.worktree` then `/speckit.orchestrate`, landed only after
   [[P004]]'s task-graph engine is drafted (the command is the entrypoint, [[P004]] is the
   engine).

Each command is registered in the harness command listing via the existing
`/speckit.instructions` regeneration path only when promoted out of `draft/`. Until then the
files sit under `draft/` and are invocable for testing without touching the spine.

## Risks & mitigations

- **Catalog bloat / discoverability.** Group commands by theme (as above), lean on [[P002]]'s
  budgeted index, and add each to the command listing only on promotion.
- **Mega-prompt drift.** Enforce the "thin command → delegates to a skill" rule; heavy logic
  lives in [[P003]] skills and `references/`, never inline (intellegix's 800+-line commands are
  the anti-pattern).
- **Provider coupling / spine overlap.** Every command uses harness-native
  WebSearch/WebFetch/MCP (no Perplexity/council transport) and wraps or brackets the spine
  (brainstorm before specify, verify/finish after implement) rather than rewriting any existing
  `/speckit.*` command.
- **Orchestration risk.** `/speckit.orchestrate` ships behind a justification gate, a strict
  no-edit orchestrator role boundary, and an explicit teardown, and waits on [[P004]].

## Value / Effort rationale

**Value M–H.** These commands turn spec-kit's linear spine into a fuller lifecycle: a design
front door, a completeness/verification gate, a debugging entrypoint, a convergence loop, and
session hygiene — the moments teams actually hit around the spec→implement core. Value is M–H
rather than H because several are convenience wrappers over [[P003]] skills; the durable value
lives in the skills, and the commands make them reachable in the `/speckit.*` idiom.

**Effort L–M.** Each command is a short markdown template following the established
`description`/`handoffs`/`scripts` pattern, delegating to skills that [[P003]] already
supplies. No new infra, no runtime, no dependency, no change to the existing spine.
`/speckit.orchestrate` is the only M-effort item and is explicitly gated on [[P004]].
