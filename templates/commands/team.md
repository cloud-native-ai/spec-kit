---
description: Single entry point for all team operations — create, modify, and run agent teams via intent routing.
short-description: 团队操作统一入口：按意图路由创建、修改或运行代理团队
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

Process `$ARGUMENTS` per the [User Input Protocol](shared/workflow/user-input-protocol.md). If empty, execute the **Default Behavior (No Arguments)** defined below. If non-empty but intent is ambiguous or unsupported, report capabilities and request the missing intent (do NOT guess silently).

## Outline

`/speckit.team` is the **single entry point** for every **team** operation — the multi-agent analogue of `/speckit.agents`. It recognizes intent, then routes to the owning team skill. It delegates to skills and does **NOT** render templates inline. It MUST NOT serve single-agent authoring (that is `/speckit.agents`), and single-agent commands MUST NOT serve team operations.

What a **team** is — the **goal** (north star, not a task list; concrete, verifiable, distinct from `description`, deliberately revisable never drifting; it decides which roles/stages are needed and which collaboration pattern fits), the static structure (Role × Stage × Type roster), the dynamic structure (the four collaboration patterns and their priorities), and the persistence layout — is defined once in the owning skill's Conceptual Model: `skills/internal/create-team/references/conceptual-model.md` (goal concept and Goal–Team binding: `references/goal.md` + `.specify/shared/definitions/goal-definitions.md`; optimization-goal classification: `skills/internal/create-team/references/optimization-goals.md`; continuous operating discipline: `references/operating-loops.md`). Reference, do not restate.

### Modes → Capability Routing

`/speckit.team` exposes **exactly three modes**:

| Mode | Recognized intent | Delegates to skill |
|------|-------------------|--------------------|
| **create** | "创建团队", "组织一个团队", "组建团队", "new team", "build a team" | `create-team` |
| **modify** | "修改团队", "调整团队", "优化 team", "improve/adjust team" | `improve-team` |
| **run** | "运行团队", "执行团队", "run/execute team", "跑一遍"(可选 `--target T-<nnn>` 指定目标切片) | `create-team` (execution path) |

**Routing flow**:

1. **Recognize intent** from `$ARGUMENTS` and conversation/repo context: classify as `create`, `modify`, or `run`.
2. **create** → `create-team`: establish the goal first (check the **Goal-Based Create** branch below first), then derive the roster (static) + pattern config (dynamic) from it — preset matching runs `python3 skills/internal/create-team/scripts/match-team-preset.py`, pattern selection follows the decision tree in `skills/internal/create-team/references/patterns.md`. The full create-mode procedure (derive, 直接落盘 `.specify/teams/<slug>/team.md` without a blocking wait per `shared/guidelines/confirmation-gates.md`, then present the definition and the modify path, and close per the execution-report convention — `shared/guidelines/confirmation-gates.md` § 执行报告) is the skill's create-mode procedure: `skills/internal/create-team/references/create-mode.md`.
3. **modify** → `improve-team`: targeted, evidence-based, structure-preserving edits to any of the team's three parts — the **goal** (redefining it is a first-class edit that realigns both structures), the **static structure**, or the **dynamic structure**. Re-persist and bump `updated`.
4. **run** → `create-team` execution path: follow the **preview → execute** sequence below.
5. **Empty arguments** → execute **Default Behavior (No Arguments)** below.
6. **Non-empty but ambiguous / unsupported** → report capabilities and request the missing intent (see "Ambiguous or Unsupported Intent" below).
7. **modify / run targeting a team that does not exist** under `.specify/teams/` → report **"team not found"** and offer to `create` it.

### Default Behavior (No Arguments)

When `$ARGUMENTS` is empty, the command MUST execute the following sequence instead of routing to a mode:

1. **List all existing teams** — scan `.specify/teams/*/team.md` and present a summary table with each team's `slug`, `name`, `goal`, and `pattern`. If no teams exist, state "No teams found" explicitly.
2. **Give contextual suggestions** — based on the current conversation, recent repo activity, and the listed teams, recommend the most relevant next action. Examples:
   - A team whose goal aligns with the current task → suggest `run <slug>`.
   - A team whose structure seems outdated relative to recent changes → suggest `modify <slug>`.
   - No teams exist or no team fits the current need → suggest `create` with a proposed goal derived from context.
   Suggestions MUST be grounded in observable context (conversation history, repo state, team definitions), NOT fabricated.
3. **Show capability summary** — briefly list the three modes (create / modify / run) so the user knows what operations are available.

This behavior is informational and non-destructive: it MUST NOT create, modify, or run any team without explicit user instruction.

### Ambiguous or Unsupported Intent

When intent cannot be resolved from non-empty arguments, the command MUST report the recognized capabilities and request the missing intent. It MUST NOT guess silently or fail without a message. Report this capability listing:

- **create** — establish the team's **goal**, then author a new team (static + dynamic structure) organized around it and persist it → `create-team`
- **modify** — adjust/optimize an existing team — reshape its structure, or **redefine its goal** and realign the structure to the new goal → `improve-team`
- **run** — restate the **goal**, render the team's structure, and execute it directly (preview is disclosure, not a gate) → `create-team`

### Goal-Based Create — deterministic entry (create path)

When a token in `$ARGUMENTS` exactly matches an archived `<goal-slug>` under `.specify/goal/`, the create path enters the **goal-based branch** directly. The entry is deterministic and engine-driven — recognition runs `python3 scripts/python/goal-utils.py list --json` and exact-matches the token (or a path to its `goal.md`); it MUST NOT be asserted from memory or semantics, and the branch decision is disclosed in the run output rather than gated on confirmation. Two rejections stop without writing: a **dangling reference** (user-named but absent from `list`) errors with the verbatim prefix `goal 未定义:` and points to `/speckit.goal create`; a **terminal goal** (`achieved`/`abandoned`) is reported and refused. Everything after entry — loading via `parse_goal` (objective, criteria incl. the `None provided.` missing state, status, targets, history), the four-element analysis, the decomposition proposal with batch approval, territory discipline, and team derivation/落盘 — is the skill's branch procedure: `skills/internal/create-team/references/create-mode.md` → *Goal-based create branch*.

### Run Mode (preview → execute)

The **run** mode MUST follow the preview → execute sequence: the preview is disclosure, and the team executes directly once presented (可逆动作自动执行,判据:`shared/guidelines/confirmation-gates.md`); **continuous** loops are the exception and keep their tiered gates (`skills/internal/create-team/references/operating-loops.md`, `templates/teams/project-cluster.md`).

1. **Load** the target team from `.specify/teams/<slug>/team.md`.
2. **Resolve the effective Target, then run the five checks (preview validation).** `run <team-slug> [--target <T-<nnn> | <goal-slug>.T-<nnn>>]` — the local form `T-<nnn>` is canonical; the qualified form is accepted only when its `<goal-slug>` equals the bound goal. The engine is the single point of truth for every judgment — never re-derive it in prose, and the five checks themselves are UNCHANGED: `python3 scripts/python/goal-utils.py run-checks <team-slug> [--target <T-<nnn>>] --json` (internally `parse_goal` / `preview_target_check` / `resolve_effective_target`). Resolution order is 显式 `--target` > `focus_target` > 无; an illegal `focus_target` reports `source=input-error` and stops (fix via `improve-team`), never silently ignored. `focus_target` 是 run 级 `--target` 的**预填**——不是写域声明、不是 Goal–Team 绑定变更、不参与 goal 身份解析;未声明且未显式指定(`source=none`)时全流程与引入前逐字节等价。 One call returns `team_slug` / `goal_slug` / `identity_kind` / `{effective, source, declared_focus}` / the five `checks` (1..5, each with `id`/`name`/`verdict`/`message`) / `verdict` / `blocked`; a check with no precondition to evaluate records `not-evaluated` — never `ok`. `blocked` is the field that means "this run must stop"; exit codes: `0` pass / `2` invalid input / `3` team not found / `4` goal unparseable / `5` blocked. The five checks cover: bound-goal resolution (with `--target`, a missing goal definition stops and points to `/speckit.goal migrate`), dangling `T-<nnn>` reference (stop; remedy `/speckit.goal targets --add`), terminal-Target reference (stop; reopen via `/speckit.goal targets --set open --id <T-nnn>`, no execution bypass), cross-goal reference (refused), and the goal's own terminal state (refused).
3. **Restate the Goal** up front, so both structures are read as means to that end.
4. **Render Static Structure** — the roster as a Role × Stage × Type matrix: each member agent, its role, its type (Worker/Meta), and its lifecycle (persistent/temporary) — and **Render Dynamic Structure**: the pattern, its parallelism/DAG/threshold/operating settings, and an execution flow diagram (textual / mermaid / PlantUML).
5. **Present & execute** — present the **goal** and both structures, then execute directly; the presentation is disclosure, not a blocking gate (事后修改途径:`/speckit.team` modify / `improve-team`). Disclose the summary decision (refresh or suppressed gate) — the periodic summary lands in the goal index `.specify/goal/<goal-slug>/summary/`, never in the team directory — and the Target assignment line per `skills/internal/create-team/SKILL.md` → Summary Refresh, in the verbatim forms `本次 Target: T-<nnn> — <statement>(open)`, `本次 Target: 无(对 goal 整体运行)`, or — when the resolution source is `team-default` — `本次 Target: T-<nnn> — <statement>(open)(团队默认)`; then orchestrate per the team's pattern (delegating to `create-team`'s execution engine): territory validation before parallel dispatch, DAG (no-cycle) validation + per-handoff verification before serial chain, mandatory max-iteration cap for iteration loops, and one cycle per continuous run at the declared maturity level with an independent verifier at L2+. Per-member dispatch modality follows `.specify/shared/definitions/subagent-definitions.md`; external CLI dispatch MUST honor its Visibility Contract. Users may halt mid-execution at any time.
6. **Report** — after execution finishes, write the dated run report to `.specify/teams/<slug>/runs/<UTC-timestamp>-report.md` per `create-team`'s Report contract (mandatory every run, incl. the `## Verification` section); a Target-assigned run's report carries the fixed `**Target 指派**` field — `**Target 指派**: T-<nnn>(<statement>)` or `无(goal 整体)`, with the source marker `(团队默认)` appended on the team-default path — and new ledger entries carry `"target_ref": "T-<nnn>"`.

**`--target` invariants**: Goal–Team binding, identity resolution, and the summary delivery directory are unchanged by `--target` — it is this run's focus slice, not a rebinding or a write-domain declaration.

Output discipline: run intermediates stay in the git-ignored `.specify/teams/.work/<slug>/`; deliverables go only to their declared target paths — the full discipline is `skills/internal/create-team/SKILL.md` → Run Workspace, Reports & Output Discipline.

### Persistence

Canonical store: the team **directory** `.specify/teams/<slug>/` — definition at `team.md`, run reports under `runs/`; no per-tool symlink. The persisted schema (frontmatter, `## Goal` authored first, `## Static Structure`, `## Dynamic Structure`) is owned by `create-team` (`references/create-mode.md`).

## Wrap-up

<!-- AUTO-GENERATED by probe-utils.py --action compile-embeds — truth source: .specify/shared/definitions/probe-definitions.md (## Handler / ## HandlerBinding) — fingerprint: 466ed9a49174 — do not edit; edit the registry, then recompile -->

1. Run Determination — `python3 .specify/scripts/python/run-determination.py --action determine --unit-id "/speckit.team" --unit-type command`
2. Feedback Record — `python3 .specify/scripts/python/feedback-utils.py --action record --unit-id "/speckit.team" --unit-type command`
3. Threshold Notice — `.specify/shared/workflow/feedback-step.md` § "Threshold prompt protocol (canonical semantics for step 6)"
4. Token Reflection — `.specify/shared/workflow/feedback-step.md` § "Reflection procedure (the embedded step points here)"
5. Docs Sync Eval — `.specify/shared/workflow/docs-step.md` § "Evaluation procedure (the embedded step points here)"

## Handoffs

**Before**: Optional `/speckit.agents` to author or refine the single agents that will become team members.

**After**: Run `/speckit.instructions` to sync discoverability of newly created teams and team skills.
