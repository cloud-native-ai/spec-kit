# Mining report: claude-code-ts `packages/` + tool infrastructure → spec-kit

Source: `/cws_work/claude-code-ts` (a large TypeScript reimplementation of Claude Code).
Scope inspected: `packages/agent-tools`, `packages/builtin-tools`, `packages/mcp-client`,
`packages/workflow-engine`, `packages/acp-link`, `packages/remote-control-server`,
`packages/cloud-artifacts`, and `src/tools.ts` / `src/constants/tools.ts`.

Lens: what concretely helps evolve spec-kit into a UNIVERSAL agent-coding framework
(SKILLS + COMMANDS + WORKFLOWS + SCRIPTS), ignoring what spec-kit already has.

---

## Project snapshot (1 paragraph)

claude-code-ts is a Bun/TypeScript monorepo that decomposes an agent-coding CLI into
sharply-layered, host-agnostic packages. The tool system is the centerpiece: a single
protocol-level `CoreTool` interface (`packages/agent-tools/src/types.ts`) defines every
tool — built-in, MCP, workflow, or skill — with a uniform contract (schema, `call`,
`checkPermissions`, `isReadOnly`/`isConcurrencySafe`/`isDestructive`, `prompt`,
result-mapping). Tools are registered in one place (`src/tools.ts`) via feature-flag /
env-gated composition, deny-rule filtering, and prompt-cache-stable sorting. Two features
stand out as directly relevant to a "universal framework": (1) a **deferred-tool /
tool-search** mechanism (`SearchExtraToolsTool` + `ExecuteTool` + `CORE_TOOLS`) that lets
an unbounded ecosystem of tools/skills exist without bloating the model's context, exposing
only a small always-loaded core and making the rest discoverable via hybrid TF-IDF+keyword
search; and (2) a **workflow-engine** (`packages/workflow-engine`) — a deterministic,
replayable, ports-driven JS-script orchestrator with `agent()/phase()/parallel()/pipeline()/
workflow()` primitives, journaling/resume, bounded concurrency, token budgets, and auto-retry.
The `mcp-client` package is a clean dependency-injected MCP protocol layer. Everything is
built around a "core has zero host dependencies; the host injects ports/deps" pattern.

---

## Top ideas for spec-kit

### 1. Deferred tools + tool-search (scale the tool/skill/command ecosystem without context bloat)
- **Idea**: Keep a small always-loaded "core" set of tools/skills/commands in the prompt,
  and defer everything else behind a *search* tool. The model calls
  `SearchExtraTools("keywords")` → gets ranked matches → then `ExecuteExtraTool({tool_name, params})`
  to invoke. Hybrid ranking = keyword scoring (0.4) + TF-IDF (0.6); supports `select:<name>`
  for direct pick and `discover:<query>` for schema-only browsing.
- **Source evidence**:
  `packages/builtin-tools/src/tools/SearchExtraToolsTool/SearchExtraToolsTool.ts`,
  `packages/builtin-tools/src/tools/ExecuteTool/ExecuteTool.ts`,
  `src/constants/tools.ts` (the `CORE_TOOLS` allowlist, lines 137-179),
  `src/tools.ts` (`isSearchExtraToolsEnabledOptimistic` gating, lines 277-282).
- **Why it helps**: This is the single most important pattern for spec-kit's universal goal.
  Once you unify skills + commands + workflows + MCP tools, the naive approach explodes the
  system prompt. This gives O(1) prompt cost regardless of ecosystem size. It maps almost
  exactly onto spec-kit's existing skills (`skills/<name>/SKILL.md` with `whenToUse`
  metadata) — the skill listing becomes a searchable index instead of a full dump.
- **Maps to spec-kit as**: [infra] + [command] (a `/speckit.find` or implicit search step).
- **Value**: H · **Effort**: M
- **Adoption sketch**: Define a small `CORE` set (constitution, plan, tasks, implement).
  Build a Python TF-IDF index over each skill/command's `description + whenToUse` frontmatter
  (spec-kit already has this metadata). Emit an index blurb into the agent prompt plus a
  `search_skills`/`run_skill` tool pair (or two slash-commands the harness maps to). Reuse
  the scoring merge in `SearchExtraToolsTool.ts` lines 471-501 and the budget-aware listing
  formatter in `SkillTool/prompt.ts` (`formatCommandsWithinBudget`, gives each listing ~1% of
  the context window and truncates gracefully — lines 71-172).

### 2. A deterministic, replayable workflow engine with `agent/parallel/pipeline/phase` primitives
- **Idea**: Orchestrate multi-step / multi-agent processes as a *script* run by an engine that
  isolates all non-determinism behind "ports" (agent runner, journal store, progress emitter,
  task registrar). The script exposes injected primitives: `agent(prompt, {schema, agentType,
  isolation, allowedTools})`, `parallel([...])`, `pipeline(items, ...stages)`, `phase(name)`,
  `workflow(name, args)` (sub-workflows), `log`, `budget`. Runs detached in the background,
  returns a `run_id`, journals every `agent()` result so resume replays completed steps for free.
- **Source evidence**:
  `packages/workflow-engine/README.md`,
  `packages/workflow-engine/src/engine/hooks.ts` (the primitives + semaphore + budget +
  auto-retry-once + journal-hit replay, lines 55-296),
  `packages/workflow-engine/src/engine/runWorkflow.ts` (resume/replay, sub-workflow depth),
  `packages/workflow-engine/src/tool/WorkflowTool.ts` (the tool surface + prompt),
  `packages/workflow-engine/src/tool/schema.ts` (input schema incl. `maxConcurrency`, `resumeFromRunId`),
  `packages/workflow-engine/src/ports.ts` (the port interfaces),
  `packages/workflow-engine/examples/smoke.ts` (a complete ~250-line wiring against the raw SDK).
- **Why it helps**: spec-kit's SDD flow (constitution→spec→clarify→plan→tasks→analyze→
  implement→review) is *exactly* a workflow. Today it is a chain of slash-commands the human
  drives. An engine lets spec-kit express the whole flow (and user-authored flows) as a durable,
  resumable, parallelizable process — filling the "workflow engine" and "background/parallel
  orchestration" gaps in one move. Named workflows resolve from `.claude/workflows/<name>` —
  spec-kit can ship `speckit-sdd.<ext>` as a bundled workflow.
- **Maps to spec-kit as**: [workflow] + [infra] (engine) + [template] (bundled SDD workflow).
- **Value**: H · **Effort**: H
- **Adoption sketch**: Port the *design*, not the TS. In Python: a `WorkflowRunner` with
  injectable `AgentRunner`/`JournalStore`/`ProgressEmitter`; scripts as Python modules (or a
  small YAML/DSL) exposing `agent/parallel/phase`. Steal the journal-replay-on-resume logic
  (`hooks.ts` lines 73-90), the semaphore-guarded budget check (lines 92-105), and the
  "one agent failure degrades to null, doesn't kill the run" contract (lines 173-220, 222-270).
  Ship spec-kit's canonical SDD chain as the first named workflow; let users drop their own in
  `.speckit/workflows/`.

### 3. One uniform `CoreTool` protocol interface + `buildTool` factory (host-agnostic tool contract)
- **Idea**: Every capability — built-in, MCP, workflow, skill — satisfies one interface with
  rich behavioral metadata: `isReadOnly`, `isConcurrencySafe`, `isDestructive`, `isOpenWorld`,
  `checkPermissions` (allow/deny/ask/passthrough), `validateInput`, `prompt()`, `searchHint`,
  `shouldDefer`/`alwaysLoad`, `mcpInfo`, and result-rendering hooks. A `buildTool()` factory
  fills defaults so each tool declares only what's special.
- **Source evidence**:
  `packages/agent-tools/src/types.ts` (the `CoreTool` interface, lines 111-203),
  `packages/agent-tools/src/registry.ts` (`toolMatchesName`/`findToolByName` incl. aliases),
  `src/tools.ts` (`getAllBaseTools`/`getTools`/`assembleToolPool` composition + dedup).
- **Why it helps**: For a *universal* framework the biggest risk is skills, commands, MCP tools
  and scripts each having ad-hoc shapes. A single descriptor with behavioral flags gives the
  harness a uniform way to reason about permissions, concurrency, read-only-ness, and prompt
  contribution across all four categories. The `searchHint` field is what makes idea #1 rank well.
- **Maps to spec-kit as**: [infra] + [template] (a canonical descriptor schema for skills/commands).
- **Value**: H · **Effort**: M
- **Adoption sketch**: Define a Python dataclass / JSON-schema "capability descriptor" that
  every skill's SKILL.md frontmatter and every command's frontmatter must satisfy: `name`,
  `description`, `whenToUse`, `searchHint`, `readOnly`, `destructive`, `concurrencySafe`,
  `allowedTools`, `model`, `effort`, `context: inline|fork`. Copy the field set from
  `types.ts`. This becomes the single source of truth for search indexing, permission
  defaulting, and prompt assembly.

### 4. Skill invocation model: inline vs forked sub-agent, + safe-property auto-allow permissions
- **Idea**: A skill can run *inline* (its content is injected into the current conversation) or
  *forked* (executed in an isolated sub-agent with its own token budget, model, effort, and
  tool allowlist), chosen by a `context: fork` frontmatter flag. Permissions use an *allowlist
  of safe properties*: a skill auto-runs without prompting only if every property it declares is
  in a known-safe set — any unknown/new property defaults to requiring permission (fail-safe).
- **Source evidence**:
  `packages/builtin-tools/src/tools/SkillTool/SkillTool.ts` — `executeForkedSkill` (lines
  122-293), `contextModifier` that injects allowedTools/model/effort overrides (lines 779-843),
  `skillHasOnlySafeProperties` + `SAFE_SKILL_PROPERTIES` allowlist (lines 879-937).
- **Why it helps**: spec-kit already has skills and role-based Executor-Evaluator-Improver
  agents; the inline-vs-fork distinction and per-skill model/effort/tool overrides give a clean,
  declarative way to run heavy skills in isolation (protecting the main context budget) and to
  bind a skill to a specific role/model. The safe-property permission default is a robust
  security pattern for a plugin ecosystem where third-party skills are untrusted.
- **Maps to spec-kit as**: [skill] + [agent] + [infra].
- **Value**: M · **Effort**: M
- **Adoption sketch**: Add `context: inline|fork`, `model`, `effort`, `allowed-tools` to
  SKILL.md frontmatter. On fork, spawn a sub-agent (spec-kit already has agents) with those
  overrides. Port `SAFE_SKILL_PROPERTIES` as the auto-allow gate for skill execution.

### 5. Dependency-injected MCP client with capability-aware tool annotations
- **Idea**: An MCP integration layer where the *core* (`createMcpManager`) knows nothing about
  transport; the host injects `connectFn` + deps (logger/auth/proxy/imageProcessor). Tool
  discovery converts MCP tools into the same `CoreTool` shape and *maps MCP annotations*
  (`readOnlyHint`, `destructiveHint`, `openWorldHint`, `title`) onto the behavioral flags used
  everywhere else. LRU-cached discovery keyed by server name; unicode sanitization of untrusted
  server output; event-based lifecycle (`connected`/`toolsChanged`/`authRequired`).
- **Source evidence**:
  `packages/mcp-client/src/manager.ts` (manager + events + `setConnectFn`),
  `packages/mcp-client/src/discovery.ts` (annotation→flag mapping, lines 65-107; LRU cache 122-154),
  `packages/mcp-client/src/index.ts` (the clean public surface + injectable interfaces),
  `packages/mcp-client/src/interfaces.ts` (host dependency injection points).
- **Why it helps**: MCP integration is a named spec-kit gap. This shows exactly how to bolt MCP
  onto a uniform tool model: connect servers, discover tools, fold them into the same
  registry/search/permission machinery as native skills/commands — no special-casing downstream.
  The annotation→behavioral-flag mapping is the key trick that makes MCP tools participate in
  permission/concurrency logic.
- **Maps to spec-kit as**: [infra] + [command] (`/speckit.mcp add|list`).
- **Value**: M · **Effort**: M
- **Adoption sketch**: Wrap the official Python MCP SDK in a `McpManager` that yields
  capability-descriptors (idea #3). Map annotations to `readOnly/destructive`. Register the
  results into the same searchable pool as skills/commands so MCP tools are deferred+discovered
  identically.

### 6. Composable, gated tool registry: presets, deny-rule pre-filtering, cache-stable ordering
- **Idea**: A single registry function composes the tool list from feature flags / env, applies
  a `--tools` **preset** system, pre-filters tools blanket-denied by permission rules *before*
  the model ever sees them (including MCP `mcp__server` prefix denies), and sorts built-ins vs
  MCP tools into stable partitions to preserve prompt-cache breakpoints.
- **Source evidence**:
  `src/tools.ts` — `getToolsForDefaultPreset`/`parseToolPreset` (lines 186-208),
  `filterToolsByDenyRules` (lines 295-302), `assembleToolPool` with cache-stable sort (lines
  378-400), `getMergedTools` (lines 416-422); `src/constants/tools.ts` — role-scoped allowlists
  (`ASYNC_AGENT_ALLOWED_TOOLS`, `COORDINATOR_MODE_ALLOWED_TOOLS`, `*_DISALLOWED_TOOLS`).
- **Why it helps**: A universal framework needs a disciplined assembly point. Deny-rule
  pre-filtering (defense at the tool-list level, not just call-time) and role-scoped allowlists
  are directly useful for spec-kit's role-based agents (limit which tools each Executor/Evaluator
  role can touch). Presets give users a `--tools default|minimal|full` knob.
- **Maps to spec-kit as**: [infra] + [agent] (per-role tool scoping).
- **Value**: M · **Effort**: L
- **Adoption sketch**: Centralize spec-kit's tool/skill assembly in one function; add
  per-role allow/deny sets modeled on `constants/tools.ts`; add a preset flag.

---

## Notable code / prompts worth copying (file paths)

- **Tool-search ranking + result phrasing** — `packages/builtin-tools/src/tools/SearchExtraToolsTool/SearchExtraToolsTool.ts`
  (keyword scoring weights lines 281-324; keyword+TF-IDF merge lines 471-501; the `select:`/
  `discover:` prefix protocol; and especially the `mapToolResultToToolResultBlockParam` guidance
  text lines 542-601 that tells the model *exactly* how to proceed — "call directly" vs "use
  ExecuteExtraTool"). This prompt-engineering is reusable verbatim as strings.
- **Deferred-tool execution guardrails** — `ExecuteTool.ts` lines 84-159: validate against the
  target's schema *before* delegating, block undiscovered deferred tools, delegate permissions.
  A robust dispatcher pattern.
- **Budget-aware skill listing formatter** — `SkillTool/prompt.ts` `formatCommandsWithinBudget`
  (lines 71-172): give the listing ~1% of context, never truncate "bundled" entries, degrade to
  names-only under extreme pressure. Directly applicable to spec-kit's skill listing.
- **Skill tool prompt** — `SkillTool/prompt.ts` lines 174-197: the "BLOCKING REQUIREMENT: invoke
  the Skill tool BEFORE responding" phrasing and the "if content already loaded, don't re-invoke"
  guard.
- **Workflow tool prompt** — `WorkflowTool.ts` lines 40-53: a compact, high-signal spec of the
  script execution model and its top pitfalls (no imports, no TS types, one `meta` literal). A
  good template for how to prompt models to author spec-kit workflows/scripts.
- **Workflow engine primitives** — `packages/workflow-engine/src/engine/hooks.ts` in full:
  journal replay, semaphore, budget, auto-retry-once, dead-agent classification
  (`no-structured-output`/`runagent-threw`/`worktree-failed`). The reasoning in the comments is
  the real value.
- **End-to-end minimal wiring** — `packages/workflow-engine/examples/smoke.ts`: a self-contained
  ~250-line reference showing exactly which ports to implement, retry/backoff, and structured-
  output (JSON-schema) extraction. The best on-ramp to reimplement in Python.
- **CoreTool interface** — `packages/agent-tools/src/types.ts` lines 111-203: copy the field set
  as spec-kit's capability-descriptor schema.
- **MCP annotation→flag mapping** — `mcp-client/src/discovery.ts` lines 65-107.

---

## Anti-patterns / what to skip

- **Don't port the Bun/`feature('X')`-macro flag machinery** (`src/tools.ts` lines 14-160). The
  `require()`-inside-conditional dead-code-elimination hack and `bun:bundle` feature macros are
  Bun-build-specific and hostile to readability. Spec-kit (Python) should use plain config /
  entry-point plugin discovery instead. Take the *composition idea*, not the mechanism.
- **`acp-link` and `remote-control-server`** (`packages/acp-link/`, `packages/remote-control-server/`):
  interesting for remote/web control (WebSocket→ACP agent bridge, JWT/API-key auth, SSE event
  streams, a manager UI), but this is heavy infra orthogonal to spec-kit's universal-framework
  core. Low priority — revisit only if spec-kit wants a hosted/remote-driving story. Note the
  `setConnectFn`/ports DI style if you do.
- **`cloud-artifacts`** (`packages/cloud-artifacts/`): a standalone Cloudflare Worker + R2 for
  hosting HTML artifacts. Not import-linked to the CLI and not relevant to SDD. Skip.
- **Analytics coupling in tools**: `SkillTool.ts` is ~50% `logEvent(...)` telemetry with
  PII-tagging (`_PROTO_*`, `AnalyticsMetadata_I_VERIFIED_*`). Strip all of it when mining the
  logic — it obscures the ~200 lines of actual behavior.
- **Over-broad `Context = unknown` / `any` in the protocol layer** (`types.ts` `ToolProgressData
  = any`, `call(..., canUseTool: (...args: any[])`): pragmatic for a decompiled port, but in a
  fresh Python design prefer typed protocols/ABCs for the host context.
- **Don't inline the deferred-tool loading everywhere at once**: the guardrails in `ExecuteTool`
  (must discover before execute) add real friction; adopt idea #1 with a generous CORE set first,
  and only defer skills/commands once the ecosystem is genuinely large.
