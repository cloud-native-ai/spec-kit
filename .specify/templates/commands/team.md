---
description: Single entry point for all team operations — create, modify, and run agent teams via intent routing.
handoffs:
  - label: Update Instructions
    agent: speckit.instructions
    prompt: Refresh project instructions so newly created teams and team skills are discoverable.
    send: false
---

## User Input

```text
$ARGUMENTS
```

Process `$ARGUMENTS` per the [User Input Protocol](shared/workflow/user-input-protocol.md). If empty, infer intent from conversation/repo context. If intent is ambiguous or unsupported, report capabilities and request the missing intent (do NOT guess silently).

## Outline

`/speckit.team` is the **single entry point** for every **team** operation — the multi-agent analogue of `/speckit.agents`. It recognizes intent, then routes to the owning team skill. It delegates to skills and does **NOT** render templates inline. It MUST NOT serve single-agent authoring (that is `/speckit.agents`), and single-agent commands MUST NOT serve team operations.

A **team** is a named, reusable multi-agent structure organized around a single **goal**. Every team has three parts: a **goal** (the team's overall final objective — the north star that all work serves), a **static structure** (Role × Stage × Type roster — *who* participates), and a **dynamic structure** (collaboration pattern — parallel / serial / team-loop — with its parallelism/DAG/iteration settings and execution flow — *how* they collaborate). The static and dynamic structures exist **only to achieve the goal**; whatever they are, they MUST be organized and run around it. Persistent teams are stored at the canonical location `.specify/teams/<slug>.team.md`. The multi-agent Conceptual Model that underpins teams is defined once in `skills/create-team/references/conceptual-model.md`.

### Goal — 团队的最终目标

Every team MUST have a **goal** set at creation and carried for its whole lifetime. The goal is the team's single overall final objective — the reason the team exists — and it governs both structures below.

- **North star, not a task list.** The goal states the desired end outcome, not the steps. The static structure (roster) and dynamic structure (pattern) are both *derived from* and *subordinate to* the goal: the goal decides which roles/stages are needed and which collaboration pattern fits.
- **Concrete and verifiable.** State the goal so progress toward it can be judged — ideally with explicit success criteria / quality dimensions and, where possible, a measurable target (e.g. a score threshold, a passing test suite, a coverage bar). The **evaluator** stage and the **team-loop** `threshold` / quality dimensions measure progress *against the goal*; a goal that cannot be evaluated cannot drive a loop.
- **Distinct from `description`.** `description` is a one-line label; the **goal** is the operational objective the whole team is organized around. A team has exactly **one** goal (sub-objectives belong to member roles/stages).
- **Deliberately revisable, never drifting.** The goal stays fixed while a team runs and never changes as a *side effect* of restructuring — but it is not frozen. The **modify** mode can deliberately **redefine an existing team's goal**; when it does, the static and dynamic structures MUST be re-checked and realigned to serve the new goal.

When a goal's theme is **optimization**, `create-team` further classifies it (**one-time vs continuous**) and, for continuous optimization, selects a strategy (**elimination vs progressive**) — see `skills/create-team/references/optimization-goals.md`.

The goal is persisted as the `goal` frontmatter field and rendered as a `## Goal` section (see Persistence).

### Modes → Capability Routing

`/speckit.team` exposes **exactly three modes**:

| Mode | Recognized intent | Delegates to skill |
|------|-------------------|--------------------|
| **create** | "创建团队", "组织一个团队", "组建团队", "new team", "build a team" | `create-team` |
| **modify** | "修改团队", "调整团队", "优化 team", "improve/adjust team" | `improve-team` |
| **run** | "运行团队", "执行团队", "run/execute team", "跑一遍" | `create-team` (execution path) |

**Routing flow**:

1. **Recognize intent** from `$ARGUMENTS` and conversation/repo context: classify as `create`, `modify`, or `run`.
2. **create** → `create-team`: **first establish the goal** — elicit it from `$ARGUMENTS` / conversation / repo context, or ask for it, and confirm it with the user — then propose a roster (static structure) + pattern config (dynamic structure) **derived from that goal**; on confirmation persist `.specify/teams/<slug>.team.md` (or run one-shot without persisting).
3. **modify** → `improve-team`: load the existing team and apply targeted, evidence-based edits to any of its three parts — the **goal**, the **static structure**, or the **dynamic structure**. Structure edits are structure-preserving and keep serving the current goal. **Redefining the goal is a first-class, supported edit**: when the goal changes, re-evaluate and realign the roster and pattern to serve the new goal. Re-persist and bump `updated`.
4. **run** → `create-team` execution path: follow the **preview → confirm → execute** gate below.
5. **Ambiguous / unsupported** → see below.
6. **modify / run targeting a team that does not exist** under `.specify/teams/` → report **"team not found"** and offer to `create` it.

### Ambiguous or Unsupported Intent

When intent cannot be resolved, the command MUST report the recognized capabilities and request the missing intent. It MUST NOT guess silently or fail without a message. Report this capability listing:

- **create** — establish the team's **goal**, then author a new team (static + dynamic structure) organized around it and persist it → `create-team`
- **modify** — adjust/optimize an existing team — reshape its structure, or **redefine its goal** and realign the structure to the new goal → `improve-team`
- **run** — restate the **goal**, render the team's structure, and execute it after confirmation → `create-team`

### Run Mode (preview → confirm → execute)

The **run** mode MUST follow this sequence and MUST NOT execute before confirmation:

1. **Load** the target team from `.specify/teams/<slug>.team.md`.
2. **Restate the Goal** — surface the team's `goal` up front, so both structures below are read as *means to that end* and execution can be judged against it.
3. **Render Static Structure** — the roster as a Role × Stage × Type matrix: each member agent, its role, its type (Worker/Meta), and its lifecycle (persistent/temporary).
4. **Render Dynamic Structure** —
   - the collaboration `pattern` (parallel / serial / team-loop);
   - the **parallelism** (parallel: degree + territories; serial: DAG stage order; team-loop: threshold, max_iterations, regression_limit, quality dimensions);
   - an **execution flow diagram** (textual / mermaid / PlantUML flow showing dispatch / handoff / loop edges).
5. **Confirmation gate** — present the **goal** and both structures, and ask the user to confirm. The team executes **only** on explicit confirmation.
   - On confirm → orchestrate per the team's pattern (delegating to `create-team`'s execution engine): territory validation before parallel dispatch, DAG (no-cycle) validation before serial chain, mandatory max-iteration cap for team loops, file-path-only handoff. Throughout, work is steered toward the **goal**, and the evaluator/team-loop measures progress against it (iterate until the goal's threshold is met or the cap is reached).
   - On decline → stop without executing; optionally suggest `modify`.

### Persistence

- Canonical store: `.specify/teams/<slug>.team.md` (Markdown + YAML frontmatter). No per-tool symlink — teams are a framework-internal concept.
- Each persisted team carries frontmatter (`slug`, `name`, `description`, `goal`, `pattern`, `members`, `config`, `created`, `updated`), a `## Goal` section (the team's overall final objective + success criteria), a `## Static Structure` section, and a `## Dynamic Structure` section (see `skills/create-team/SKILL.md` and the data model). The `## Goal` section is authored first — the static and dynamic sections are organized to serve it.

## Handoffs

**Before**: Optional `/speckit.agents` to author or refine the single agents that will become team members.

**After**: Run `/speckit.instructions` to sync discoverability of newly created teams and team skills.
