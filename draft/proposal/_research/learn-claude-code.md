# Mining report: learn-claude-code → spec-kit

Source repo: `/cws_work/learn-claude-code` (content on branch `gitlab/main`; working tree empty).
Read via `git -C /cws_work/learn-claude-code show gitlab/main:<path>`.

## Project snapshot

`learn-claude-code` ("Harness Engineering for Real Agents") is a teaching repo that reconstructs a Claude-Code-style agent harness in ~20 incremental, runnable Python lessons. Each lesson isolates one *harness* mechanism and layers it on the previous one without changing the core loop: the agent loop (`s01`), a tool-dispatch map + path sandbox (`s02`), permission gates (`s03_permission`), a hook registry (`s04_hooks`), TodoWrite planning (`s03/s05`), disposable subagents (`s04/s06`), on-demand skill loading (`s05/s07`), multi-layer context compaction (`s06/s08`), a **file-based task graph** with dependencies (`s07/s12`), background threads (`s08/s13`), cron scheduling (`s14`), persistent teammate mailboxes (`s09/s15`), request-response team protocols (`s10/s16`), autonomous task-claiming (`s11/s17`), git **worktree-per-task isolation** with an event stream (`s12/s18`), MCP tool plugins (`s19`), and a comprehensive capstone (`s20`). The English docs under `docs/en/s01..s12` are the clearest narrative; the `sNN_*/README.en.md` + `code.py` folders carry the full 20-lesson set and reference implementations. Its central lesson for spec-kit: **durable, file-based state (tasks, worktrees, mailboxes, transcripts, events) is the coordination substrate that survives compaction, restarts, and works across any host agent** — exactly the layer spec-kit currently lacks under its static markdown.

## Lesson-by-lesson takeaways

| Lesson (doc/code path) | Reusable pattern | spec-kit adoption |
|---|---|---|
| s01 agent loop (`docs/en/s01-the-agent-loop.md`) | One loop, one exit condition (`stop_reason != tool_use`); everything layers on top without touching it | Documentation/reference model that grounds spec-kit's EEI triad and framework claims; not a runtime to reimplement |
| s02 tool use (`docs/en/s02-tool-use.md`) | Tool = handler + schema in a `{name: fn}` dispatch map; `safe_path()` workspace sandbox | Extend `templates/tool-*-template.md` + `.specify/memory/tools.md` registry with a path-sandbox helper script; confirms registry approach |
| s03 permission (`s03_permission/README.en.md`) | 3-gate pipeline: hard **deny** → rule-based **ask** → **allow**; gate runs before every tool call | Ship permission rules as host-agent config (Claude Code `settings.json`) + a `guardrails` skill; deny-list is explicitly *not* real security |
| s04 hooks (`s04_hooks/README.en.md`) | Extension points (`UserPromptSubmit/PreToolUse/PostToolUse/Stop`) hang *on* the loop via a registry; non-None return blocks | Map SDD gates (constitution checks, auto-commit, logging) to host hook events instead of prose in command files |
| s03/s05 TodoWrite (`docs/en/s03-todo-write.md`) | Exactly one `in_progress` at a time + "nag reminder" injected after N idle rounds | Encode "single active task" + progress-ledger convention into tasks-template and implement command prompts (nag needs loop control; express as convention) |
| s04/s06 subagent (`docs/en/s04-subagent.md`) | Fresh `messages=[]` per subtask, return only final summary; child tools exclude `task` (no recursion) | Already close to `draft/skills/subagent-driven-development`; adopt the no-recursion guardrail + "return summary only" contract explicitly |
| s05/s07 skill loading (`docs/en/s05-skill-loading.md`) | Two layers: names+descriptions in system prompt (cheap), full `SKILL.md` body via tool_result (on demand) | **Validates spec-kit's existing Resource Registry + SKILL.md model**; add a loader script that emits Layer-1 index automatically |
| s06/s08 context compact (`docs/en/s06-context-compact.md`, `s08_context_compact/README.en.md`) | Cheap-first, expensive-last: micro/snip compaction → LLM summary at token threshold → manual `compact` tool; save transcript to disk first | New gap. `/speckit.compact` command + `context-compaction` skill + transcript persistence to `.specify/specs/<f>/.transcripts/` |
| s07/s12 task system (`docs/en/s07-task-system.md`, `agents/s07_task_system.py`) | One JSON file per task with `blockedBy` DAG; completing a task auto-clears it from dependents; answers ready/blocked/done; survives compaction | **Highest-value gap.** Task-graph manager script + template replacing/augmenting flat `tasks.md` |
| s08/s13 background tasks (`docs/en/s08-background-tasks.md`) | Daemon thread runs slow cmd, result enqueued, loop drains notifications before next LLM call | Background runner script for tests/builds during `/speckit.implement`; notifications as files |
| s14 cron scheduler (`s14_cron_scheduler/README.en.md`) | Independent scheduler thread + queue decouples scheduling from execution; durable jobs | Low fit — spec-kit is a scaffolding CLI, not a daemon host; skip beyond doc |
| s09/s15 agent teams (`docs/en/s09-agent-teams.md`) | Persistent teammates + `config.json` roster + append-only JSONL inbox (drain-on-read) | Async mailbox infra for role agents beyond linear handoffs; `.specify/specs/<f>/.team/` |
| s10/s16 team protocols (`docs/en/s10-team-protocols.md`) | One request-response FSM (`pending→approved/rejected`) w/ `request_id` correlation drives shutdown AND plan approval | Formalize spec-kit's plan-review gate + graceful handoff as a protocol template with correlation IDs |
| s11/s17 autonomous agents (`docs/en/s11-autonomous-agents.md`) | Teammates scan the task board, self-claim unclaimed+unblocked tasks; idle-poll loop; identity re-injection after compaction | Autonomous `/speckit.implement` loop over the task graph; identity re-injection guards against post-compaction amnesia |
| s12/s18 worktree isolation (`docs/en/s12-worktree-task-isolation.md`, `agents/s12_worktree_task_isolation.py`) | Task = control plane, git worktree = execution plane, bound by `task_id`; keep/remove teardown; `events.jsonl`; crash-recovery from disk | **High-value gap.** Worktree-per-task script + skill for parallel, collision-free feature implementation |
| s19 mcp (`s19_mcp_plugin/README.en.md`) | Discover (`tools/list`) + invoke (`tools/call`) + `mcp__server__tool` namespacing + `assemble_tool_pool` | Aligns with spec-kit's `mcp-builder`; adopt namespacing + tool-pool assembly convention |

## Top ideas for spec-kit

### 1. File-based Task Graph (DAG) — the coordination backbone
- **Source evidence**: `docs/en/s07-task-system.md`; `agents/s07_task_system.py` (`class TaskManager`, `create/update/_clear_dependency`, `blockedBy` at lines 47-116); `s12_task_system/code.py`.
- **Why it helps**: spec-kit's `templates/tasks-template.md` produces a *flat markdown checklist* — no dependencies, no ready/blocked queries, no machine-readable state, and it dies when the host compacts context. A `.tasks/task_N.json` graph with `blockedBy` edges answers "what's ready / blocked / done", auto-unblocks dependents on completion, and persists across restarts. It is the substrate every later idea (autonomy, worktrees, teams) reads from.
- **Maps to spec-kit as**: **script** (`scripts/python/task_graph.py` CRUD + ready/blocked queries) + **template** (JSON task schema) + **command** (`/speckit.tasks` emits the graph alongside human-readable `tasks.md`).
- **Value: H** · **Effort: M**
- **Adoption sketch**: `/speckit.tasks` writes both `tasks.md` (human) and `.specify/specs/<feature>/.tasks/*.json` (machine, with `id/subject/status/blockedBy/owner/worktree`). `/speckit.implement` reads the graph, works only ready tasks, marks `in_progress`→`completed`, and calls the clear-dependency step. Keep it host-agnostic (plain files any agent can read).

### 2. Worktree-per-task isolation with event stream + crash recovery
- **Source evidence**: `docs/en/s12-worktree-task-isolation.md`; `agents/s12_worktree_task_isolation.py` (`class EventBus.emit` lines 82-118, `TaskManager.bind_worktree` line 183, `index.json`/`events.jsonl`); `s18_worktree_isolation/code.py`.
- **Why it helps**: Enables *parallel* feature/task implementation without file collisions — each task runs in `git worktree add -b wt/<name>`, bound to its task by ID; `keep`/`remove(complete_task=true)` handles teardown+completion in one step; every lifecycle step emits to `events.jsonl` so state reconstructs from disk after a crash. spec-kit has a `git-workflow` skill but no worktree-per-task lane; this is the missing piece for safe multi-agent SDD.
- **Maps to spec-kit as**: **script** (`scripts/bash/worktree-lane.sh` + python registry) + **skill** (`worktree-task-isolation`) wired to idea #1's task graph.
- **Value: H** · **Effort: M**
- **Adoption sketch**: Add `worktree` field to the task JSON; a skill instructs the host to allocate a lane per risky/parallel task, run edits with `cwd` in the lane, and close with keep/remove. Ship an `events.jsonl` append convention for observability + recovery.

### 3. Multi-layer context compaction + transcript persistence
- **Source evidence**: `docs/en/s06-context-compact.md`; `s08_context_compact/README.en.md` (four-layer `snip_compact` keeping head+tail, tool_use/tool_result pairing rule); `agents/s06_context_compact.py`, `s08_context_compact/code.py`.
- **Why it helps**: Long SDD sessions (spec→plan→tasks→implement over many files) overflow the host context and lose the plan. The cheap-first/expensive-last ladder (drop old tool results → snip middle → LLM summary at threshold → save transcript to disk before summarizing) keeps sessions durable. Critical: the tool_use↔tool_result pairing invariant during trimming is a subtle correctness rule spec-kit should encode.
- **Maps to spec-kit as**: **command** (`/speckit.compact`) + **skill** (`context-compaction`) + **infra** (transcript files under `.specify/specs/<f>/.transcripts/`).
- **Value: H** · **Effort: M**
- **Adoption sketch**: A skill that tells the host to summarize the session into a resumable brief written to disk (never lost), preserving the constitution + active task IDs, then continue. Pair with idea #1 so the durable task graph is the recovery anchor.

### 4. Autonomous task-claiming loop + identity re-injection
- **Source evidence**: `docs/en/s11-autonomous-agents.md` (`scan_unclaimed_tasks`, idle-poll, identity re-injection when `len(messages) <= 3`); `s17_autonomous_agents/code.py`.
- **Why it helps**: Turns `/speckit.implement` from lead-directed ("do task 3, now task 4") into self-organizing: an implementer scans the board, claims the first pending+unowned+unblocked task, completes it, loops. Identity re-injection fixes post-compaction amnesia ("who am I / what task"). Directly leverages idea #1.
- **Maps to spec-kit as**: **agent** (`sdd-implementer` autonomous variant, building on `draft/agents/sdd-implementer.agent.md`) + **workflow**.
- **Value: M/H** · **Effort: M**
- **Adoption sketch**: Implementer agent prompt: "read `.tasks/`, claim first ready task (set owner+in_progress), implement, complete, repeat until none ready." Add an identity/role re-read step so it re-grounds after any compaction.

### 5. Request-response protocol FSM for plan approval & graceful handoff
- **Source evidence**: `docs/en/s10-team-protocols.md` (`shutdown_requests`/`plan_requests` dicts, `pending→approved/rejected` FSM, `request_id` correlation, one FSM two applications).
- **Why it helps**: spec-kit already has an implicit plan-review gate (plan command → tasks) and role handoffs, but no correlated, auditable handshake. A single request-response FSM with `request_id` cleanly models "teammate submits plan → lead approves/rejects with feedback" and "graceful shutdown", giving traceable gates for high-risk changes.
- **Maps to spec-kit as**: **template** (protocol/handshake) + **command** step in plan/review + reuse in `draft/agents/sdd-task-reviewer.agent.md`.
- **Value: M** · **Effort: L**
- **Adoption sketch**: Add a small handshake convention (request_id + status + feedback, appended to a JSONL) that plan-review and the two-verdict task review already in draft can adopt for correlation and audit.

### 6. Persistent teammate mailbox (append-only JSONL, drain-on-read)
- **Source evidence**: `docs/en/s09-agent-teams.md` (`class MessageBus.send/read_inbox`, `.team/config.json` roster, per-member `.jsonl` inboxes).
- **Why it helps**: spec-kit's role agents (`.specify/agents/*.agent.md`) communicate only via linear handoffs. An append-only mailbox lets roles exchange async messages/broadcasts and lets a lead track roster status — enabling non-linear collaboration (e.g., test-engineer pinging module-designer) without a live runtime.
- **Maps to spec-kit as**: **infra/script** (`.specify/specs/<f>/.team/inbox/*.jsonl`) + convention referenced by agent templates.
- **Value: M** · **Effort: M**
- **Adoption sketch**: Ship a `mailbox.py` helper (send/read-drain) and a `.team/config.json` roster schema; agents read their inbox at the start of each invocation and append messages instead of relying solely on handoff order.

### 7. Permission gates + hook registry as host config
- **Source evidence**: `s03_permission/README.en.md` (deny→ask→allow, `PERMISSION_RULES`); `s04_hooks/README.en.md` (`HOOKS` registry, four events, non-None-blocks).
- **Why it helps**: spec-kit encodes safety/guardrails as *prose* in command files and the constitution — nothing enforces it. Mapping constitution checks, auto-commit, and logging to host hook events (Claude Code `settings.json` `PreToolUse`/`PostToolUse`) makes guardrails executable and keeps command prose lean ("hang on the loop, don't write into it").
- **Maps to spec-kit as**: **infra** (settings.json hook config + `scripts/` hook handlers) + **skill** (`guardrails`).
- **Value: M** · **Effort: L/M**
- **Adoption sketch**: Provide a hook bundle: PreToolUse → constitution/path-sandbox check, PostToolUse → auto `git add`/log, Stop → session summary. Note the deny-list is a teaching demo, not security.

### 8. A versioned "Harness Reference Model" grounding the framework
- **Source evidence**: `docs/en/s01..s12` (the layered narrative + "What Changed" diff tables).
- **Why it helps**: spec-kit's goal is to *be* a universal agent framework, but it has no documented reference model of the agent loop / tool-use / subagent / skill / compaction / task / team layers. Adopting this 12-layer taxonomy (loop → tools → planning → context isolation → skills → compaction → tasks → background → teams → protocols → autonomy → worktrees) as internal reference docs gives every skill/command/agent a shared vocabulary and a maturity ladder.
- **Maps to spec-kit as**: **documentation/template** under `docs/` + a mapping in the constitution.
- **Value: M** · **Effort: L**
- **Adoption sketch**: One reference doc per layer with spec-kit's concrete artifact for it; use the "What Changed" table style to track spec-kit's own capability evolution.

## Notable code / prompts worth copying (file paths, gitlab/main)

- `agents/s07_task_system.py` — `TaskManager` with `blockedBy` DAG + `_clear_dependency` auto-unblock (lines 47-116). Cleanest reference for idea #1.
- `agents/s12_worktree_task_isolation.py` — `EventBus.emit` (append-only lifecycle events, lines 82-118), `TaskManager.bind_worktree` (control↔execution binding, line 183), `index.json`/`events.jsonl` schema. Reference for idea #2.
- `s08_context_compact/code.py` + `s08_context_compact/README.en.md` — `snip_compact` with head/tail retention and the tool_use↔tool_result pairing invariant. Reference for idea #3.
- `docs/en/s05-skill-loading.md` — the two-layer skill model; near-verbatim confirmation of spec-kit's Resource Registry + SKILL.md design (good text to cite in spec-kit docs).
- `docs/en/s10-team-protocols.md` — the single request-response FSM prompt pattern for plan approval / shutdown (idea #5).
- `docs/en/s11-autonomous-agents.md` — `scan_unclaimed_tasks` + identity re-injection snippet (idea #4).
- `skills/agent-builder/references/subagent-pattern.py` and `skills/agent-builder/SKILL.md` — a ready SKILL.md-style write-up of the subagent pattern.

## Anti-patterns / what to skip

- **Do not reimplement the agent loop as a runtime inside spec-kit.** spec-kit is a scaffolding CLI; the *host* agent (Claude Code/Copilot/etc.) owns the loop. Adopt these patterns as **file-state + prompt/skill conventions + scripts**, not a competing Python runtime. The value is durable disk state, not a new executor.
- **Nag-reminder injection and micro-compact-per-turn require controlling the loop** — spec-kit can't do these from static markdown. Express "one active task" / "re-read identity" / "summarize to disk" as conventions the host follows, not as loop hooks it must own.
- **Threading-based teammates/background/cron (`threading.Thread`, daemon loops, `s14` scheduler)** don't map to a scaffolding CLI. Model teams via files (mailboxes/task graph) and let the host or CI drive execution; skip long-lived daemons.
- **The string-match deny list is explicitly flagged as not real security** in `s03_permission` (shell expansion/variants bypass it). Do not ship it as a security control — use it only as a UX speed-bump; real enforcement belongs in host permission config.
- **MCP mock handlers in `s19` are teaching stubs** (no real subprocess/JSON-RPC). Copy the naming (`mcp__server__tool`) and tool-pool assembly ideas, not the mock transport.
- **Avoid duplicating state stores.** spec-kit already keeps state under `.specify/specs/<feature>/`; put `.tasks/`, `.team/`, `.worktrees/`, `.transcripts/` under that root rather than inventing repo-root siblings, to respect existing isolation guarantees noted in `draft/README.md`.
