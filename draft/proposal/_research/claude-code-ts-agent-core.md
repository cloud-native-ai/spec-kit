# Mining report: claude-code-ts — Agent Core & Runtime

Scope mined: `/cws_work/claude-code-ts` — the agent loop (`src/query.ts`, `src/QueryEngine.ts`,
`src/query/*`), orchestration (`src/coordinator/*`, agent-team tools), event hooks
(`src/utils/hooks*`), context/memory (`src/services/compact/*`, `src/memdir/*`), background /
autonomous work (`src/services/goal/*`, `src/proactive/*`, `src/jobs/*`, `src/utils/autonomy*`),
and self-improvement (`src/services/skillLearning/*`).

## Project snapshot

claude-code-ts is a large (~5k-line REPL, 60+ builtin tools) TypeScript reimplementation of the
Claude Code CLI built on Bun. Its agent core is a streaming turn loop (`query()` in `src/query.ts`,
wrapped by the stateful `QueryEngine` in `src/QueryEngine.ts`) that persists a message transcript,
runs tools, and enforces `maxTurns` / `maxBudgetUsd` / `taskBudget` limits. Layered on top are the
pieces most relevant to spec-kit's "universal framework" goal: a **coordinator/worker**
orchestration mode, **agent teams** (team == task-list, named teammates, message passing), a
lifecycle **hooks** system (`PreToolUse`/`PostToolUse`/`Stop`/`SubagentStop`/`SessionStart`/
`PreCompact`… as shell/prompt/agent hooks, declarable from skill & agent frontmatter), multi-strategy
**context compaction**, an LLM-selected **memory directory**, an autonomous **goal loop** with
steering prompts + completion/blocked audits, **managed autonomy flows** (resumable multi-step
processes with approval gates), scheduled/cron autonomy, and a **skill-learning** subsystem that
observes sessions and auto-generates new skills/commands/agents. Almost all runtime is gated behind
`feature()` flags. The reusable value for spec-kit (a Python CLI shipping markdown templates that
drive a host chat agent) is mostly in the *declarative artifact designs and prompt/process patterns*,
not the TS runtime itself.

## Top ideas for spec-kit

### 1. Autonomous "goal" continuation loop with completion & blocked audits
- **Idea**: A first-class objective that auto-continues the agent turn-by-turn until done, steered by
  three injected prompt templates (continuation / budget-limit / objective-updated), each wrapped in
  `<goal-steering>` XML, and gated by a strict **Completion Audit** ("PROVE completion, not merely
  fail to find remaining work") and a **Blocked Audit** ("same blocking condition must persist ≥3
  consecutive turns before marking blocked"). State (objective, tokens, turns, blockedAttempts) is
  persisted to the transcript so `--resume` carries the goal.
- **Source evidence**: `src/services/goal/prompts.ts` (the three templates + audits),
  `src/services/goal/goalState.ts` (`MAX_GOAL_TURNS=150`, `BLOCKED_CONSECUTIVE_THRESHOLD=3`),
  `src/hooks/useGoalContinuation.ts` (idle→enqueue→continue loop; yields to user input),
  `src/services/goal/goalStorage.ts` (hydrate on resume).
- **Why it helps**: spec-kit already has Executor-Evaluator-Improver roles but no autonomous
  "keep going until the spec is satisfied" driver. The audit prompts are the crown jewels — they
  turn a fuzzy "are we done?" into an evidence-based gate that pairs perfectly with spec-kit's
  acceptance criteria / tasks.
- **Maps to**: workflow + template (steering prompts) + command (`/speckit.goal`).
- **Value**: H · **Effort**: M · **Adoption sketch**: Ship a `goal` workflow: a `continuation.md`
  template that re-states the spec objective + remaining tasks + a Completion Audit against the
  spec's acceptance criteria, plus a `blocked.md`. The host agent re-invokes with the continuation
  prompt until the audit passes or a turn/token budget is hit. Track state in a small JSON beside
  the spec.

### 2. Coordinator/worker orchestration pattern (async task-notification protocol)
- **Idea**: A "coordinator" persona whose whole job is to decompose work, fan out parallel **workers**
  via an Agent/spawn tool, and synthesize. Workers run autonomously with the standard toolset minus
  orchestration primitives. Results return **asynchronously as user-role messages** wrapped in
  `<task-notification>` XML (task-id, status, summary, result, usage). The prompt explicitly teaches
  parallelism, when-to-serialize (read-only parallel, write-heavy one-at-a-time), real verification
  ("prove it works, don't rubber-stamp"), failure handling (continue same worker with its context),
  and mid-flight cancellation.
- **Source evidence**: `src/coordinator/coordinatorMode.ts` (`getCoordinatorSystemPrompt`, worker
  tool context injection), `src/coordinator/workerAgent.ts` (worker agent definition + system prompt).
- **Why it helps**: this is a concrete, copy-pasteable design for spec-kit's "subagent dispatch /
  parallel task orchestration" gap. The `<task-notification>` schema and the Task Workflow table
  (Research→Synthesis→Implementation→Verification) map cleanly onto SDD phases.
- **Maps to**: agent + workflow + template (coordinator system prompt).
- **Value**: H · **Effort**: M · **Adoption sketch**: Add a `coordinator` agent template and a
  `worker` agent template to spec-kit; drive them from a `/speckit.orchestrate` workflow that maps
  spec tasks to parallel worker prompts and collects `<task-notification>` results into the plan.

### 3. Lifecycle hooks declarable from skill/agent frontmatter
- **Idea**: A rich event-hook system with events `PreToolUse`, `PostToolUse`, `PostToolUseFailure`,
  `PermissionDenied`, `Stop`, `SubagentStop`, `PreCompact`/`PostCompact`, `SessionStart`,
  `SessionEnd`, `UserPromptSubmit`, `Setup`, `Notification`. Hooks come in three flavors — **command**
  (shell), **prompt** (LLM with `$ARGUMENTS` substitution, runs on a small/fast model),
  and **agent** (spawns a sub-query) — and can be declared inside a **skill's or agent's
  frontmatter**, auto-registered as session-scoped hooks (with `once: true` one-shot support), and
  auto-cleaned when the session/agent ends. Agent frontmatter `Stop` hooks are auto-rewritten to
  `SubagentStop`.
- **Source evidence**: `src/utils/hooks.ts` (runner), `src/utils/hooks/hookEvents.ts` (event set),
  `src/utils/hooks/execPromptHook.ts`, `src/utils/hooks/execAgentHook.ts`,
  `src/utils/hooks/registerFrontmatterHooks.ts`, `src/utils/hooks/registerSkillHooks.ts`.
- **Why it helps**: spec-kit's biggest automation gap is "hooks/event automation." Letting a skill or
  agent *carry its own hooks* (e.g. a TDD skill that runs tests on `PostToolUse[Edit]`, or a spec
  skill that validates the spec on `Stop`) is exactly the "unify skills + workflows + scripts"
  vision — the automation travels with the artifact.
- **Maps to**: infra + skill/template (frontmatter schema) + script (command hooks).
- **Value**: H · **Effort**: M · **Adoption sketch**: Define a `hooks:` frontmatter block for
  spec-kit skills/agents (command | prompt | agent), plus emit the standard hook-input JSON at
  lifecycle points so any host that supports hooks (Claude Code) wires them automatically.

### 4. Skill/command/agent auto-generation from observed "instincts" (self-improvement)
- **Idea**: Observe sessions → distill reusable `Instinct` records (`trigger` + `action` + `scope` +
  evidence + confidence, status pending→promoted) → when enough correlated instincts accumulate,
  auto-generate a **new skill, command, or agent** draft. A learning policy decides the target
  artifact type and threshold; a promotion/lifecycle step manages confidence and pruning; a
  skill-gap store tracks missing capabilities.
- **Source evidence**: `src/services/skillLearning/index.ts` (module map), `instinctParser.ts`
  (Instinct model), `evolution.ts` (`EvolutionCandidate` → skill|command|agent),
  `skillGenerator.ts` / `commandGenerator.ts` / `agentGenerator.ts`, `learningPolicy.ts`,
  `promotion.ts`, `skillGapStore.ts`.
- **Why it helps**: This is the literal embodiment of spec-kit's "universal framework unifying
  skills+commands+workflows" — a feedback loop that *grows* the artifact library from real usage.
  Even a lightweight version (a `/speckit.learn` command that reads a transcript and proposes a new
  skill/command markdown) would be a standout differentiator.
- **Maps to**: workflow + command + infra.
- **Value**: H · **Effort**: H · **Adoption sketch**: Start with the artifact model (instinct →
  candidate → drafted skill/command/agent markdown) and a manual `/speckit.evolve` command that
  reviews recent specs/PRs and emits draft artifacts into `.specify/`; automate promotion later.

### 5. Managed autonomy flows — resumable multi-step processes with approval gates
- **Idea**: A declarative multi-step "flow" record: ordered steps each with `name`, `prompt`, and
  per-step `status` (pending/running/completed/failed/cancelled), a wait/approval state, and
  triggers. Runs are persisted (`runs.json`), survive process restarts (stale-run recovery), and
  certain steps (e.g. a `report` step) require approval via a `PreToolUse` hook gate. Unified
  `autonomyRuns` layer normalizes triggers (scheduled-task, heartbeat, manual) into queued prompts.
- **Source evidence**: `src/utils/autonomyFlows.ts` (`ManagedAutonomyFlowStep`, statuses, advance/
  cancel), `src/utils/autonomyRuns.ts` (unified trigger → queued prompt, stale recovery),
  `src/hooks/useScheduledTasks.ts` (cron → autonomy run).
- **Why it helps**: spec-kit workflows are currently static markdown with no execution/checkpoint
  state. A persisted step-status flow with approval gates is exactly a "process/workflow engine" —
  and it's resumable, which addresses the session-continuity gap.
- **Maps to**: workflow + infra + template (flow definition).
- **Value**: H · **Effort**: M · **Adoption sketch**: Define a `workflow.yml`/`.md` flow spec
  (steps with prompts + approval flags), and a runner that tracks per-step status in a JSON sidecar
  so `specify workflow resume` picks up where it stopped. spec-kit's `draft/skills/spec-kit-extensions`
  already has a `workflow-template.yml` — align its schema to this step-status model.

### 6. Multi-strategy context compaction + the structured summary prompt
- **Idea**: Several complementary strategies rather than one: (a) full **compaction** producing a
  9-section structured summary via a detailed prompt with an `<analysis>` scratchpad that's stripped
  before the summary re-enters context; (b) **microcompact** that clears only stale tool *results*
  (Read/Bash/Grep/Glob/WebFetch) while keeping the reasoning; (c) **time-based** clearing with a
  `[Old tool result content cleared]` marker; (d) **snip**. Auto-compaction fires on token
  thresholds and reserves output budget.
- **Source evidence**: `src/services/compact/prompt.ts` (the 9-section summary template +
  `NO_TOOLS_PREAMBLE`), `src/services/compact/microCompact.ts`, `apiMicrocompact.ts`,
  `autoCompact.ts`, `snipCompact.ts`.
- **Why it helps**: addresses the "context/memory compaction" gap. Even for a template-driven CLI,
  shipping the **9-section compaction prompt** as a reusable template gives host agents a proven way
  to summarize long SDD sessions without losing spec intent (note section 6: "List ALL user
  messages" and section 9: verbatim next-step quotes to prevent drift).
- **Maps to**: template (compaction prompt) + workflow.
- **Value**: M · **Effort**: L · **Adoption sketch**: Ship `templates/compact-summary.md` and a
  `/speckit.compact` command; optionally a microcompact-style "drop old tool output" guidance in
  long workflows.

### 7. LLM-selected memory directory with a strict "what NOT to save" taxonomy
- **Idea**: A `MEMORY.md` entrypoint (capped 200 lines / 25KB) plus a directory of memory files, each
  with frontmatter `type` (user | feedback | project | reference) and a description. On each query, a
  cheap model scans memory *headers* and selects up to 5 relevant files. A sharp taxonomy forbids
  storing anything derivable from project state (code patterns, architecture, git history) —
  memory is only for non-derivable context.
- **Source evidence**: `src/memdir/memdir.ts` (entrypoint caps, prompt loading),
  `src/memdir/findRelevantMemories.ts` (LLM selection prompt), `src/memdir/memoryTypes.ts`
  (4-type taxonomy + "what not to save").
- **Why it helps**: gives spec-kit durable cross-session memory (user prefs, prior feedback,
  project conventions) with a discipline that keeps it small — directly supports "context/memory"
  and "session continuity."
- **Maps to**: skill + template + infra.
- **Value**: M · **Effort**: M · **Adoption sketch**: Adopt the type taxonomy + "what not to save"
  as a memory skill; store memories under `.specify/memory/` with frontmatter descriptions; a
  `/speckit` step selects relevant ones by description.

### 8. Bounded loops: maxTurns / maxBudgetUsd / taskBudget with continuation nudges
- **Idea**: The loop enforces turn caps, USD budget, and a per-task token budget, emitting typed
  terminal results (`error_max_turns`, `error_max_budget_usd`). A separate budget tracker injects a
  "continuation nudge" at 90% completion threshold and detects diminishing returns.
- **Source evidence**: `src/QueryEngine.ts` (budget/turn checks, typed results),
  `src/query/tokenBudget.ts` (`COMPLETION_THRESHOLD=0.9`, continue/stop decision).
- **Why it helps**: any autonomous spec-kit loop needs guardrails; these are the concrete thresholds
  and the "nudge vs stop" decision logic.
- **Maps to**: infra + script.
- **Value**: M · **Effort**: L · **Adoption sketch**: Bake turn/budget caps into the goal/workflow
  runner (idea #1/#5).

### 9. Headless "template jobs" with stop-hook status classification
- **Idea**: A named markdown template + args instantiates a job directory with `state.json`; after
  each turn a **Stop hook** classifies the job status (running/completed) from the assistant message
  (tool_use present → running; `stop_reason==end_turn` → completed). Templates are discovered from
  `.claude/templates` up the tree + user-level dir.
- **Source evidence**: `src/jobs/templates.ts` (discovery), `src/jobs/state.ts` (`JobState`),
  `src/jobs/classifier.ts` (status classification in a Stop hook).
- **Why it helps**: a clean model for spec-kit "background/parallel task" runs driven by reusable
  templates, with a simple, model-free completion signal.
- **Maps to**: workflow + script + template.
- **Value**: M · **Effort**: M · **Adoption sketch**: `specify job new <template> <args>` creating a
  job dir with state.json; classify completion via a Stop hook.

### 10. Proactive tick loop with self-controlled cadence
- **Idea**: An idle-driven "tick" mode: when active and the user is idle, the REPL injects `<tick>`
  prompts so the model keeps working; a `SleepTool` lets the model set its own next-wake cadence;
  ticks are blocked after API errors to prevent tick→error→tick runaway.
- **Source evidence**: `src/proactive/index.ts` (state machine, `contextBlocked` guard).
- **Why it helps**: an alternative autonomy primitive (heartbeat-style) for long-running spec
  maintenance/watch tasks.
- **Maps to**: workflow + infra.
- **Value**: L-M · **Effort**: M · **Adoption sketch**: optional; a watch mode for spec drift.

## Notable code/prompts worth copying (file paths)

- **Goal steering + audits** — `src/services/goal/prompts.ts` (continuation/budget/objective-updated
  templates; Completion Audit + Blocked Audit text). Highest-leverage prose to lift near-verbatim.
- **Coordinator system prompt** — `src/coordinator/coordinatorMode.ts` `getCoordinatorSystemPrompt`
  (Task Workflow phase table, concurrency rules, "What Real Verification Looks Like",
  `<task-notification>` schema).
- **Worker agent prompt** — `src/coordinator/workerAgent.ts` (concise autonomous-worker charter).
- **9-section compaction summary prompt** — `src/services/compact/prompt.ts` (`BASE_COMPACT_PROMPT`,
  `NO_TOOLS_PREAMBLE`, `<analysis>` scratchpad convention).
- **Memory-selection prompt + taxonomy** — `src/memdir/findRelevantMemories.ts`
  (`SELECT_MEMORIES_SYSTEM_PROMPT`), `src/memdir/memoryTypes.ts`.
- **TeamCreate / SendMessage tool prompts** — `packages/builtin-tools/src/tools/TeamCreateTool/prompt.ts`,
  `.../SendMessageTool/prompt.ts` (team==task-list model, automatic message delivery, task ownership,
  shutdown/plan-approval protocol).
- **Instinct model + evolution** — `src/services/skillLearning/instinctParser.ts`,
  `src/services/skillLearning/evolution.ts` (trigger/action/confidence → skill|command|agent).
- **Managed flow model** — `src/utils/autonomyFlows.ts` (step status machine + approval wait state).

## Anti-patterns / what to skip

- **Don't port the TS runtime.** `src/query.ts`/`QueryEngine.ts` are enormous, tightly coupled to
  Bun, the Anthropic streaming SDK, Ink/React state, and prompt-cache micro-optimizations
  (fire-and-forget transcript writes, cache-key preservation, `feature()` DCE). spec-kit should mine
  the *designs and prompts*, not the code. Reimplementing the streaming loop is out of scope for a
  template-driving CLI.
- **Feature-flag sprawl.** ~65 `feature()` flags with subtle interactions (COORDINATOR_MODE,
  TEAMMEM, HISTORY_SNIP, KAIROS, CONTEXT_COLLAPSE disabled, etc.). Don't replicate the flag matrix;
  pick the finished ideas.
- **React-hook driven control flow.** The goal/proactive/scheduled loops live in Ink React hooks
  (`useGoalContinuation`, `useScheduledTasks`) with `useLayoutEffect` race handling. That coupling is
  an artifact of the REPL UI; spec-kit should express the same logic as a plain runner loop.
- **In-memory-only orchestration state** in the coordinator/team path leans on a live process +
  message queue. For spec-kit prefer the *persisted* models (autonomyFlows `runs.json`, jobs
  `state.json`, goal-on-transcript) which are resumable and host-agnostic.
- **Over-broad team broadcast** (`SendMessage to: "*"`) is explicitly flagged as expensive; keep
  addressing point-to-point.
