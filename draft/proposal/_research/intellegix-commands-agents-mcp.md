# Mining Report: intellegix-code-agent-toolkit → spec-kit

Source: `/cws_work/intellegix-code-agent-toolkit` (branch not git-inspected; a modular Claude Code global config `~/.claude`-style repo).
Target: `/cws_work/spec-kit` (specify-cli, Spec-Driven Development CLI).
Lens: ideas for a universal agent-coding framework unifying skills + commands + workflows + scripts, with focus on command breadth, agent patterns, MCP integration, and portfolio governance.

## Project snapshot

The intellegix toolkit is a personal-but-mature Claude Code configuration system built around a "self-driving automation loop" that pairs the Claude Code CLI with Perplexity deep-research (via a home-grown MCP browser bridge) to execute multi-step engineering tasks autonomously with **$0 API cost** (it drives Perplexity's web UI through a Chrome extension instead of paying for API tokens). It ships 40 slash commands (`commands/*.md`), 10 role-based sub-agent definitions (`agents/*.md` with YAML frontmatter binding tools/model/memory/skills), two real MCP servers (`mcp-servers/browser-bridge` — a Node WebSocket↔Chrome-extension bridge with 30 tools, SQLite context persistence, health server, rate limiter, validator; and `mcp-servers/minecraft` — a Python FastMCP server), a portfolio-governance layer (`portfolio/` — tiers, phases, anti-patterns, velocity constraints, decision gates), and an autonomous orchestration engine (`automated-loop/loop_driver.py` + `/orchestrator*` commands that drive parallel Claude agents in git worktrees). The strongest transferable assets are the *governance layer*, the *adversarial two-pass verification loops*, the *worktree-based multi-agent orchestration*, and the *reusable MCP server template* — the many domain-specific commands (game-dev, Raken API, spreadsheets) are personal and should be skipped.

## Command catalog

Grouped by theme. "In spec-kit?" judged against `templates/commands/*.md` (constitution, requirements, clarify, plan, research, tasks, analyze, implement, review, checklist, feature, agents, skills, tools, instructions) and `skills/`.

### Research & verification
| Command | Purpose | In spec-kit? |
|---|---|---|
| `research.md` | Web research pipeline w/ source-reliability tiers, structured output | Partial (`/speckit.research`) |
| `research-perplexity.md` | Deep research via Perplexity + **mandatory two-pass plan critique before ExitPlanMode** | No (verification loop absent) |
| `extended-research.md` | 5–40 iterative verification passes w/ convergence detection, contradiction tracking, adversarial floor, final verdict | No |
| `solve-perplexity.md` | Iterative bug solver w/ contradiction tracking + convergence ("Tier 2.5 escalation ladder") | No |
| `creative-research.md` | 3-stage **divergent** ideation → viability scoring → blueprint (discovers unrequested features) | No |
| `session-audit.md` | Retrospective self-diagnostic: sends own tool-call trace out for independent performance review | No |
| `council-refine.md` / `export-to-council.md` / `council-extract.md` / `cache-perplexity-session.md` / `labs-perplexity.md` / `automate-perplexity.md` / `ensure-space.md` | Multi-model "council" (GPT/Claude/Gemini) refinement + Perplexity browser plumbing | No (provider-coupled, skip) |

### Planning & orchestration
| Command | Purpose | In spec-kit? |
|---|---|---|
| `smart-plan.md` | Multi-phase plan w/ **Phase 0 portfolio gate** (tier/phase constraint check) | Partial (`/speckit.plan`, no governance gate) |
| `implement-perplexity.md` | Bridge blueprint→executable plan w/ research validation, dependency-aware | Partial |
| `orchestrator.md` | Single-loop autonomous executor; strict "you orchestrate, never implement" role boundary | No |
| `orchestrator-multi.md` | N parallel Claude agents in **git worktrees**, scoped instructions, monitor, merge | No |
| `orchestrator-new.md` | Greenfield bootstrapper: intake→research→BLUEPRINT.md→route to orchestrator | No |

### Implementation & fixes
| Command | Purpose | In spec-kit? |
|---|---|---|
| `implement.md` | Feature implementation w/ **Phase 0 portfolio gate** + types-first | Yes (`/speckit.implement`, no gate) |
| `fix-issue.md` | GitHub issue → reproduce (failing test) → fix → verify | No |
| `review.md` | Code review of diff/staged changes | Yes (`/speckit.review`) |

### Audit & quality
| Command | Purpose | In spec-kit? |
|---|---|---|
| `stub-check.md` | 3-phase implementation-completeness audit: finds stubs/shallow/skeletal/non-production code | No (high value) |
| `health-check.md` | Read-only 3-layer prod health check (frontend E2E + DB integrity + audit log) w/ **TRUST CONTRACT** | No |
| `frontend-e2e.md` | Live browser E2E across pages/forms/a11y/responsive w/ per-page error isolation | No |
| `spreadsheet-audit.md` | Excel audit (domain-specific) | No (skip) |

### Lifecycle & governance
| Command | Purpose | In spec-kit? |
|---|---|---|
| `init.md` | Universal project bootstrap w/ auto-detect first-run vs read-only health-check mode | Partial (specify init) |
| `handoff.md` | Session handoff doc (files changed, decisions, blockers, next steps) | No |
| `portfolio-status.md` | Portfolio health review + velocity-constraint enforcement | No |

### Domain-specific (skip — personal/niche)
| Command | Purpose | In spec-kit? |
|---|---|---|
| `gba-*.md` (6), `nds-*.md` (2), `minecraft-build.md` | Emulator/game-dev pipelines w/ anti-hallucination "RECIPE" rules | No (skip; patterns interesting) |
| `raken-api.md`, `raken-perplexity.md` | Raken API context loader + research | No (skip) |

## Top ideas for spec-kit

### 1. Adversarial two-pass verification loop (self-critique before finalizing)
- **Source evidence:** `commands/research-perplexity.md` (mandatory "send plan back for critique (Step 7) BEFORE calling ExitPlanMode … NO EXCEPTIONS"); `commands/extended-research.md` (convergence detection: "score >= 8, no critical issues, score gain < 1 or max 3 iterations", adversarial floor, FINAL_VERDICT); `commands/council-refine.md` (iterate until convergence); `commands/solve-perplexity.md` (contradiction tracking).
- **Why it helps:** spec-kit's `/speckit.plan`, `/speckit.analyze`, `/speckit.review` produce artifacts in a single pass. A structured "generate → adversarially critique → revise once → re-check convergence" loop measurably raises artifact quality and catches gaps before implementation — directly strengthening the SDD gate philosophy.
- **Maps to spec-kit as:** skill (reusable "adversarial-review" / convergence-loop skill) + command augmentation (`/speckit.plan`, `/speckit.analyze`).
- **Value: H | Effort: M**
- **Adoption sketch:** Add a `verify-and-converge` skill: takes an artifact + rubric (score 1–10, strengths, weaknesses, critical issues, revised sections), runs one self-critique pass using the *same* model (no external provider needed — drop the Perplexity coupling), stops on convergence or after N iterations. Wire it as an optional final step in plan/analyze/tasks.

### 2. Portfolio-governance layer (tiers, phases, anti-patterns, gates)
- **Source evidence:** `portfolio/PORTFOLIO.md.example` (Tier T1–T4, Phase Prototype→Development→Hardening→Maintenance→Archive, per-phase Allowed/Forbidden table, 10 explicit anti-patterns, velocity constraints "MAX 2 active feature branches"); `portfolio/DECISIONS.md` (checklists: Start New Project, Archive, Phase Transitions, Feature Freeze triggers); `portfolio/PROJECT_TEMPLATE.md` (≤80-line CLAUDE.md template); enforced in `commands/implement.md` and `commands/smart-plan.md` "Phase 0: Portfolio Gate".
- **Why it helps:** spec-kit has a *constitution* (per-project principles) but NO cross-project governance/lifecycle layer. This is exactly the "portfolio/governance layer" the universal-framework goal calls out as missing. Phase-appropriate constraints (e.g., "no auth/CI/monitoring in Prototype") stop agents from over-engineering — a huge failure mode for autonomous coding agents.
- **Maps to spec-kit as:** template + workflow (a governance gate step) + infra (a `portfolio/PORTFOLIO.md` registry the constitution/plan reads).
- **Value: H | Effort: M**
- **Adoption sketch:** Add `templates/portfolio.md` (registry) + a "Phase Gate" preamble step to `/speckit.plan` and `/speckit.implement` that reads the project's tier/phase and rejects work forbidden by the current phase. Ship the anti-patterns list as constitution defaults.

### 3. Git-worktree multi-agent orchestration
- **Source evidence:** `commands/orchestrator-multi.md` ("split work across N parallel Claude Code agents using git worktrees … monitor … merge"; "Multi-Agent Justification Gate"; worktrees-over-clones/subdirs rationale; `off` teardown); `commands/orchestrator.md` (strict role boundary: orchestrator writes instructions + monitors, never reads/writes source); `automated-loop/loop_driver.py` + `README.md` (spawns Claude in `-p` mode, streams NDJSON, `.workflow/state.json`); `commands/orchestrator-new.md` (greenfield → BLUEPRINT.md → route).
- **Why it helps:** spec-kit's `tasks.md` already produces dependency-ordered, parallelizable tasks and has a draft `subagent-driven-development` skill, but no concrete parallel-execution harness. Worktrees give conflict-free parallel implementation with clean merges — the natural execution engine for a task graph.
- **Maps to spec-kit as:** workflow + script (a `run-parallel-tasks` script) + agent (orchestrator role).
- **Value: H | Effort: H**
- **Adoption sketch:** Add a `scripts/orchestrate.py` that reads `tasks.md`, assigns independent `[P]` task groups to worktree-isolated agents, and a `/speckit.orchestrate` command with the "justification gate" (only parallelize when tasks are truly independent) and a `status`/`off` teardown.

### 4. Reusable MCP server template + MCP integration story
- **Source evidence:** `mcp-servers/browser-bridge/server.js` (clean `BrowserBridgeServer` MCP handler, 30 registered tools, per-CLI `sessionId` isolation); `mcp-servers/browser-bridge/lib/` (`context-manager.js` SQLite persistence, `rate-limiter.js`, `validator.js`, `health-server.js`, `metrics.js`, `logger.js` w/ `sanitizeArgs`); `mcp-servers/browser-bridge/package.json` (`@modelcontextprotocol/sdk`, comprehensive test suite); `mcp-servers/minecraft/README.md` + `server.py` (Python **FastMCP** server, documented registration JSON, extension points).
- **Why it helps:** spec-kit has NO MCP integration. Rather than ship a specific server, spec-kit can adopt the *pattern*: a documented, tested, modular MCP server skeleton (Node + Python variants) with health/metrics/rate-limit/validator libs, plus a registration recipe. This is the concrete on-ramp for the "MCP story".
- **Maps to spec-kit as:** template (`templates/mcp-server/` skeleton) + infra + skill (`create-mcp-server`, mirroring existing `create-skills`).
- **Value: H | Effort: M**
- **Adoption sketch:** Vendor a minimal FastMCP (Python, matches spec-kit's stack) skeleton with lifespan wiring, one example tool, tests, and a README registration block. Add a `/speckit.tools`-adjacent skill that scaffolds an MCP server from a tool spec and emits per-harness `mcpServers` config.

### 5. Implementation-completeness ("stub-check") audit
- **Source evidence:** `commands/stub-check.md` (3-phase audit finding "code that is unfinished, shallow, skeletal, or not production-ready"; local Grep/Glob pattern scan + depth/brevity validation).
- **Why it helps:** After `/speckit.implement`, there is no gate that verifies tasks were *actually* implemented vs stubbed (`TODO`, `pass`, `NotImplementedError`, empty handlers). This is a high-frequency agent failure. A local, provider-free scan closes the loop between tasks.md and real code.
- **Maps to spec-kit as:** skill + command (`/speckit.verify-completeness`), pairs with `/speckit.analyze`.
- **Value: H | Effort: L**
- **Adoption sketch:** A skill that greps for stub markers, cross-checks each `tasks.md` item against changed files, and flags shallow implementations. No LLM council needed — pure static scan + one summarization pass.

### 6. Role-based agent frontmatter contract (tools/model/memory/skills + cross-boundary flagging + persistent memory)
- **Source evidence:** `agents/architect.md`, `agents/research.md`, `agents/testing.md`, `agents/devops.md` — YAML frontmatter `tools:`, `model:`, `memory: project`, `skills: [...]`; per-agent scope directories; deliverable templates; "Cross-Boundary Flagging" (API change → notify Frontend+Backend); "Memory Management" (append decisions to `agent-memory/<role>/MEMORY.md`).
- **Why it helps:** spec-kit's `.agent.md` (see `draft/agents/*.agent.md`) is thinner. Binding **skills to agents**, declaring **allowed tools/model per role**, and a **persistent per-agent memory** convention give a richer, safer agent system and make agents composable with the skills library spec-kit already has.
- **Maps to spec-kit as:** template (`.agent.md` frontmatter schema) + agent.
- **Value: M | Effort: L**
- **Adoption sketch:** Extend spec-kit's `.agent.md` schema to support `skills:`, `tools:`, `model:`, `memory:` and a cross-boundary "notify" convention; teach `/speckit.agents` to emit and validate it.

### 7. Session handoff + retrospective self-audit
- **Source evidence:** `commands/handoff.md` (files changed, work done, blockers, decisions + rationale, next steps); `commands/session-audit.md` (capture tool-call/edit/error/retry trace → independent performance review scorecard; "use when Claude is going in circles").
- **Why it helps:** Long SDD sessions and agent handoffs lose context; a structured handoff artifact + a self-diagnostic scorecard improve reliability and are harness-agnostic. Fits the "workflow/process" pillar.
- **Maps to spec-kit as:** command + skill.
- **Value: M | Effort: L**
- **Adoption sketch:** `/speckit.handoff` writes a handoff.md into the feature dir; a lighter self-audit checklist can run at end of `/speckit.implement`.

### 8. Escalation ladder (structured tiered fallback)
- **Source evidence:** `commands/solve-perplexity.md` ("Tier 2.5 in the escalation ladder — between single-pass research (Tier 2) and user handoff (Tier 3)").
- **Why it helps:** Gives agents a deterministic "what to try next and when to stop / hand off to human" protocol instead of thrashing. Encodes graceful failure.
- **Maps to spec-kit as:** workflow/process doc + skill convention.
- **Value: M | Effort: L**
- **Adoption sketch:** Document a Tier 1 (local) → Tier 2 (research) → Tier 3 (human handoff) ladder in the constitution/process docs; reference it from implement/solve flows.

## Notable code/prompts worth copying (file paths)

- `mcp-servers/browser-bridge/lib/context-manager.js` — SQLite-backed conversation/context persistence pattern for MCP servers.
- `mcp-servers/browser-bridge/lib/{rate-limiter,validator,health-server,metrics,logger}.js` — production-grade MCP server hygiene (rate limiting, input validation, health endpoint, metrics, arg sanitization). Directly reusable as a "MCP_PATTERNS" reference.
- `mcp-servers/minecraft/server.py` (docstring) + `README.md` — clean **FastMCP** lifespan-wiring pattern (matches spec-kit's Python stack) and a copy-paste MCP registration JSON block.
- `commands/extended-research.md` — the convergence-loop rubric, "Risk Register" table, and adversarial pass scheduling are an excellent template for a self-verifying artifact skill (ignore Perplexity plumbing).
- `commands/health-check.md` — the "TRUST CONTRACT / read-only boundary enforced by a single code path (`hc_db.py`)" pattern is a strong safety idiom for any destructive-capable command.
- `commands/orchestrator.md` / `orchestrator-multi.md` — the explicit "Role Boundary (FORBIDDEN)" list and "Multi-Agent Justification Gate" are reusable prompt scaffolding for orchestrator agents.
- `portfolio/PORTFOLIO.md.example` + `DECISIONS.md` + `PROJECT_TEMPLATE.md` — near-verbatim adoptable governance content (tiers, phase Allowed/Forbidden table, anti-patterns, phase-transition checklists, ≤80-line CLAUDE.md rule).
- `agents/architect.md` — deliverable templates (Component/Endpoint/Schema design) + Clean Architecture layer rules + Cross-Boundary Flagging.

## Anti-patterns / what to skip

- **Perplexity browser-automation coupling.** ~13 commands and the whole browser-bridge MCP exist to drive Perplexity's web UI for "$0/query" research. It is fragile (a code comment notes the UI commit key flipped from Enter→Space and must be hand-patched; `perplexity-selectors.json` CSS selectors rot), single-provider, and violates spec-kit's multi-harness neutrality. Copy the *loop/verification logic*, not the transport. spec-kit should use its own harness's tools (WebSearch/WebFetch/MCP) instead.
- **Domain-specific commands.** `gba-*`, `nds-*`, `minecraft-build`, `raken-*`, `spreadsheet-audit` are personal/niche. Skip the commands; the "anti-hallucination RECIPE / VERIFY-state-before-action" rules in `gba-test.md` are a mildly interesting prompt pattern but not core.
- **Hardcoded personal absolute paths.** e.g. `commands/gba-ai-full.md` references `C:\Users\AustinKidwell\...Dropbox\...`; `orchestrator-multi.md` uses `C:\worktrees\`. Never carry these over — spec-kit must stay path-agnostic and cross-platform.
- **Windows-only tooling.** `.ps1`/`.bat` launchers (`focus-chrome.ps1`, `start.bat`, `loop_driver.ps1`, `notify.ps1`) are Windows-bound; keep the Python `loop_driver.py` logic, drop the PowerShell.
- **Over-long/monolithic command files.** Several commands exceed 500–1174 lines (`frontend-e2e.md` 1174, `orchestrator-multi.md` 889) with embedded risk registers and self-referential E2E notes. spec-kit should factor such logic into skills + references rather than mega-prompts.
- **Single-user assumptions in governance.** The portfolio content assumes one developer ("even if just Austin"); generalize the concept (tiers/phases/gates) but drop the personalization.
