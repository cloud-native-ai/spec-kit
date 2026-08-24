---
name: browser-utils
description: |
  Browser automation and web application testing with three-tier strategy selection.
  Detects available browser capabilities and selects the best automation approach:
  Tier 1 — built-in browser (native browser tools exposed by the agent runtime),
  Tier 2 — Playwright headless automation (script-driven Chromium), Tier 3 — MCP
  connector + Chrome extension (desktop Chrome via MCP tool calls). Supports
  JavaScript and Python execution,
  auto-detects dev servers, manages server lifecycle, writes test scripts, takes
  screenshots, tests responsive design, validates UX, automates browser tasks.
  Use when the user mentions "browser", "Playwright", "web test", "screenshot",
  "automation", "responsive", "headless", "form fill", "login flow", "broken links",
  "浏览器", "网页测试", "截图", "自动化", "响应式测试", "表单填写",
  "UI测试", "端到端测试", "E2E测试", "browser-use", "MCP browser"
skill_id: "<SKILL:.specify/skills/browser-utils/SKILL.md>"
---

# Browser Utilities

## Overview

General-purpose browser automation skill with a **three-tier strategy** that adapts
to the executing agent's capabilities. The skill detects which tier applies and
routes to the appropriate automation approach.

- **Tier 1 — Built-in Browser**: The agent runtime exposes native browser tools (e.g., `navigate`, `click`, `screenshot`); operate the browser directly through them.
- **Tier 2 — Playwright Headless**: Script-driven automation — use Playwright to drive a headless or visible Chromium browser via JavaScript/Python scripts.
- **Tier 3 — MCP Connector + Chrome Extension**: A `browser-use` MCP server is available; control the desktop Chrome browser through MCP tool calls.

## Strategy Selection

**Execute this decision tree BEFORE any browser automation work.**

```
Step 1: Detect available browser capabilities
    |-- Native browser tools are available (navigate, click, screenshot as built-in tools)
    |   --> TIER 1: Use built-in browser tools directly
    |
    |-- Bash/script execution is available (default path)
    |   --> TIER 2: Use Playwright headless automation (see § Tier 2 below)
    |
    |-- browser-use MCP server is available (navigate_page, take_snapshot, click, etc.)
    |   --> TIER 3: Use MCP connector (see § Tier 3 below)
```

### Capability Detection Signals

| Tier | Detection Signal |
|------|-----------------|
| **Tier 1** | System prompt mentions built-in browser capabilities; native `navigate`/`click`/`screenshot` tools are present without requiring MCP or scripts |
| **Tier 2** | Shell/script execution tools (e.g., `Bash`/`Write`/`Read`) are available and neither Tier 1 nor Tier 3 applies — the default path |
| **Tier 3** | `browser-use` MCP server is available; tools like `navigate_page`, `take_snapshot`, `click`, `fill` are present in the tool list |

> **If you cannot determine your capabilities, default to Tier 2 (Playwright).**

---

## Site Memory & Direction Routing

Every task targeting a specific site MUST pass through site-memory routing **before** executing. Memory lives under `${SKILL_HOME}/site/<host[:port]>/` and is managed exclusively by the deterministic engine — never hand-edit `state.json`:

```bash
python3 ${SKILL_HOME}/scripts/site-memory.py --action get-state --site <host[:port]> --skill-home "${SKILL_HOME}"
```

```
Step 2: get-state --site <host[:port]> → route by returned state
  null        → EXPLORATION: init; complete task page-level; append-record every DOM op + request (redacted)
  exploration → OPTIMIZATION: distill records → write-recipe → transition; complete task hybrid
  optimization|validation → VALIDATION: run recipe vs expect; record-validation (pass→sealed, fail→optimization)
  sealed      → SEALED: run recipe with zero page probing; on failure transition to optimization + re-distill
```

**Whatever the state, the user's task is always completed in full** — state only changes *how* (exploratory / hybrid / sealed execution), never *whether*.

**Reporting obligation**: any run that creates or updates `site/` memory MUST close with an output line reminding the caller that site memory is caller-owned runtime data — the skill neither ships nor archives it — and that the calling project/agent owns its management (commit it to their own repo, back it up, or git-ignore it) per their policy. Ownership detail: [`references/site-memory.md`](references/site-memory.md) § Ownership.

**Direction selection (Tier 2/3)**: page-level direction simulates real user operations (forms, clicks, DOM reads) — required for exploration and for steps a recipe marks `type: "page"`. Request-level direction issues the underlying network calls directly in the page context (`fetch`, inheriting the session) — preferred whenever a `recipe.json` exists. Patterns and code: [`references/request-level-patterns.md`](references/request-level-patterns.md); state machine semantics, record/recipe/evidence formats, and engine CLI detail: [`references/site-memory.md`](references/site-memory.md).

---

## Tier 1: Built-in Browser

When the executing agent has a built-in browser component, use its native browser
tools directly. No MCP calls, no script files, no Playwright setup needed.

**How to use**: Call the agent's native browser tools (e.g., `navigate`, `click`,
`screenshot`, `get_text`) as you would any other agent tool. The browser session
is managed by the agent runtime.

**Key advantages**:
- Zero setup — browser is already available
- Full session persistence — cookies, localStorage, and auth state carry over
- Real browser rendering — no headless emulation gaps

**Constraints**:
- Tool availability depends on the agent runtime; check which tools are actually exposed
- Some agents may not expose `evaluate_script` or network inspection

---

## Tier 2: Playwright Headless Automation

When Tier 1 is unavailable, use Playwright to drive a Chromium
browser via JavaScript or Python scripts.

### Run Mode Selection (choose FIRST, before writing any script)

Tier 2 has **two mutually exclusive run modes**. Decide which one applies before
writing code — they use different browser binaries and launch options, and picking
the wrong one silently fails (e.g. a real logged-in site redirects to its login page).

| | **Mode 1 — Clean Test Browser** | **Mode 2 — Real Chrome Profile** |
|---|---|---|
| Purpose | Frontend/localhost automation & E2E testing | Reach sites that need an existing login state |
| Browser | Playwright's bundled Chromium / Chrome for Testing | Real Google Chrome (`channel: 'chrome'`) |
| Launch | `chromium.launch()` (fresh ephemeral context) | `chromium.launchPersistentContext(userDataDir, …)` |
| Keychain | Default `--use-mock-keychain` (kept) | `ignoreDefaultArgs: ['--use-mock-keychain']` (real keychain) |
| Login state | None (clean slate each run) | Reuses cookies/localStorage from the profile |

**Selection rule** (apply in order):
1. Target is `localhost`/a dev server, or the task is testing the user's own frontend → **Mode 1** (default).
2. Task needs an authenticated/internal site, OR the user supplies a Chrome `userDataDir`/profile → **Mode 2**.
3. If it is ambiguous whether login state is required, **ask the user to confirm the mode before launching** (see Strict Requirement #3).

Mode 2 has strict preconditions (profile must not be in use; real Chrome; real
keychain). For the full launch recipe, preflight checks, and failure-symptom table,
see [references/playwright-patterns.md § Run Modes (Tier 2)](./references/playwright-patterns.md#run-modes-tier-2).

**JavaScript path**: Write Playwright scripts to `/tmp`, execute via the universal
runner `${SKILL_HOME}/scripts/js/run.js`.

**Python path**: Use `sync_playwright` with `${SKILL_HOME}/scripts/python/with_server.py`
for server lifecycle management.

For code examples, patterns, and helper usage, see
[references/playwright-patterns.md](./references/playwright-patterns.md).

For the complete Playwright API reference, see
[references/playwright-api.md](./references/playwright-api.md).

### Setup

**JavaScript** (one-time):
```bash
cd ${SKILL_HOME}/scripts/js && npm run setup
```

Before the first script of a session, verify the install actually **loads** (a
partial/corrupt `node_modules` passes `install` but throws `Cannot find module
'./lib/bootstrap'` at runtime). This one-liner self-repairs:
```bash
cd ${SKILL_HOME}/scripts/js && node -e "require('playwright'); console.log('playwright OK')" \
  || { rm -rf node_modules/playwright* && npm install; }
```
See [references/playwright-patterns.md § Preflight: verify the Playwright install](./references/playwright-patterns.md#preflight-verify-the-playwright-install-actually-resolves).

**Python** (one-time):
```bash
pip install playwright && playwright install chromium
```

### JavaScript Workflow

1. **Auto-detect dev servers** (for localhost testing):
   ```bash
   cd ${SKILL_HOME}/scripts/js && node -e "require('./lib/helpers').detectDevServers().then(s => console.log(JSON.stringify(s)))"
   ```
   - 1 server → use it automatically
   - Multiple → ask user which one
   - None → ask for URL or help start dev server

2. **Write script to `/tmp`** — never write to skill or project directory

3. **Execute via runner**:
   ```bash
   cd ${SKILL_HOME}/scripts/js && node run.js /tmp/playwright-test-*.js
   ```

### Python Workflow

1. **Check if server is running** — if not, use `with_server.py`:
   ```bash
   python ${SKILL_HOME}/scripts/python/with_server.py --help
   ```

2. **Write Playwright script** with only automation logic (server managed by helper)

3. **Execute**:
   ```bash
   python ${SKILL_HOME}/scripts/python/with_server.py --server "npm run dev" --port 5173 -- python your_script.py
   ```

For decision tree (static vs dynamic), reconnaissance-then-action pattern, and
Python examples, see [references/playwright-patterns.md](./references/playwright-patterns.md).

---

## Tier 3: MCP Connector (browser-use)

When the agent has access to the `browser-use` MCP server, control the desktop
Chrome browser through MCP tool calls. No script files needed.

**Core workflow**: Navigate → `take_snapshot` → act on elements by `uid` → verify.

**Available tools** (16 total): `navigate_page`, `take_snapshot`, `take_screenshot`,
`click`, `fill`, `press_key`, `hover`, `drag`, `upload_file`, `handle_dialog`,
`wait_for`, `evaluate_script`, `list_pages`, `select_page`, `list_network_requests`,
`list_console_messages`.

For the complete tool reference, operation patterns, and best practices, see
[references/mcp-browser-tools.md](./references/mcp-browser-tools.md).

**Key advantages**:
- Operates the user's real desktop Chrome — full extension and profile support
- Interactive — no script files to write and manage
- a11y tree snapshots provide structured element identification

**Constraints**:
- Requires Chrome with the browser-use extension to be running
- Snapshot uids are ephemeral — always snapshot before acting
- No persistent sessions across MCP server restarts

---

## Strict Requirements

1. **Detect capabilities FIRST** — always run the Strategy Selection decision tree before any browser work
2. **Tier 2: Select run mode FIRST** — before writing any script, decide Mode 1 (clean test browser) vs Mode 2 (real Chrome profile) per § Run Mode Selection. The two modes use different binaries and launch options; picking wrong fails silently.
3. **Tier 2: Confirm the mode when login state is ambiguous** — if it is unclear whether the target needs an existing login, or the user references a Chrome profile/`userDataDir`, ask the user to confirm Mode 2 (and which profile) before launching a real profile.
4. **Tier 2 Mode 2: Preflight and release the profile** — the target `userDataDir` must have no running Chrome (singleton lock) or launch is silently handed off to the existing window and exits ("正在现有的浏览器会话中打开"). Verify no process holds the profile before launching; if one does, ask the user to close it. Always close the context in a `finally` block so the singleton lock is released for the next run and the user's own Chrome.
5. **Tier 2: Detect servers FIRST** — for localhost testing (Mode 1), always run `detectDevServers()` before writing test code
6. **Write scripts to `/tmp`** — never write test files to the skill directory or user's project (`/tmp/playwright-test-*.js`)
7. **Parameterize URLs** — put detected/provided URL in a `TARGET_URL` constant at the top of every script
8. **Visible browser by default (Tier 2)** — use `headless: false` unless user explicitly requests headless mode
9. **Tier 3: Always snapshot before acting** — uids from stale snapshots are invalid after page changes
10. **Wait strategies over fixed timeouts** — use `waitForSelector`, `waitForURL`, `waitForLoadState` (Tier 2) or `wait_for` (Tier 3) instead of arbitrary sleeps
11. **Error handling** — always use try-catch for robust automation; screenshot on error for debugging
12. **Tier 2 SPA traversal: settle dynamic content, prove login, screenshot every module** — before extracting a module, wait for lazy content (Grafana panels / tab bodies / expandable rows) to actually render — never extract an empty "(0 panels)" shell; count real panel ELEMENTS as the authoritative panel count (a framework's own "(N panels)" row-header label is a collapsed-state artifact — do not surface it) and scope panel/field titles to the header node so table/stat bodies are not swallowed; assert the first navigation did NOT land on a login page (fail fast) and record a run log; capture a per-module screenshot and a one-line PURPOSE, treating a failed screenshot as a recorded problem, not a silent skip. See [references/playwright-patterns.md § SPA Site Traversal & Module Extraction](./references/playwright-patterns.md#spa-site-traversal--module-extraction-tier-2)

## Conventions

- **Tier preference**: Tier 1 > Tier 2 > Tier 3 — always use the highest available tier
- **Inline vs files (Tier 2)**: Inline for quick one-off tasks (screenshot, check element); files for complex tests
- **slowMo (Tier 2)**: Use `slowMo: 100` to make actions visible and easier to follow
- **Custom headers (Tier 2)**: Use `PW_HEADER_NAME`/`PW_HEADER_VALUE` env vars to identify automated traffic
- **Console output**: Use `console.log()` (JS) or `print()` (Python) to track progress
- **Full-site enumeration (Tier 2)**: To map every module of an SPA (left-nav + hash routes) into a design doc, use one reused context, resumable checkpoints, and per-module extraction — see [references/playwright-patterns.md § SPA Site Traversal & Module Extraction](./references/playwright-patterns.md#spa-site-traversal--module-extraction-tier-2)

## Path Conventions

This Skill follows the canonical path conventions:

- Use `${SKILL_HOME}/<relative-path>` for every Skill-owned resource reference.
- Use `${SKILL_WORKDIR}/<relative-path>` for every runtime/user-facing path.
- Never embed agent-specific install paths.

## Resources

| Directory | Contents |
|-----------|----------|
| `${SKILL_HOME}/scripts/js/` | `run.js` universal executor, `package.json`, `lib/helpers.js` |
| `${SKILL_HOME}/scripts/python/` | `with_server.py` server lifecycle manager |
| `${SKILL_HOME}/scripts/` | `site-memory.py` — site memory engine (state machine, records, recipes, validation evidence; see § Site Memory & Direction Routing) |
| `${SKILL_HOME}/references/` | `playwright-api.md`, `playwright-patterns.md`, `mcp-browser-tools.md`, `extension-bridge-patterns.md`, `site-memory.md`, `request-level-patterns.md`, `claude-code-guide.md`, `copilot-guide.md`, `qoder-guide.md` |
| `${SKILL_HOME}/examples/` | Python example scripts (element discovery, static HTML, console logging) |

## Dependencies

- **Tier 1**: Agent's built-in browser (no external dependencies)
- **Tier 2 JavaScript**: Node.js (>=14.0.0), Playwright npm package (`^1.57.0`), Chromium browser
- **Tier 2 Python**: Python (>=3.8), `playwright` Python package, Chromium browser
- **Tier 3**: `browser-use` MCP server + Chrome with browser-use extension

## Agent-Specific Configuration

### Step 1: Identify Executing Agent

Before executing this skill's workflow, identify which AI agent you are:

| Agent | Detection Signals |
|-------|-------------------|
| **Claude Code** | System prompt contains "Claude Code"; tools include `Agent`, `Edit`, `Bash`, `Read`; `.claude/` directory exists |
| **GitHub Copilot** | Running in VS Code Copilot Chat context; `.github/copilot-instructions.md` loaded; tools include `workspace edit`, `@terminal` |
| **Qoder CLI** | `.qoder/` directory exists; `AGENTS.md` instructions loaded |
| **opencode** | `.opencode/` directory exists |
| **Codex CLI** | `.codex/` directory exists |
| **Hermes Agent** | `.hermes/` directory exists |

If you cannot identify your agent, skip Step 2 and proceed with the standard workflow.

### Step 2: Load Agent-Specific Guidance

If you identified your agent in Step 1, check if a guide exists at:

```
${SKILL_HOME}/references/<agent-slug>-guide.md
```

Where `<agent-slug>` is: `claude-code`, `copilot`, `qoder`, `opencode`, `codex`, `hermes`.

If the guide exists, read it and apply the agent-specific tool mappings, best practices, and pitfall avoidances during execution. If no guide exists for your agent, proceed with the standard workflow.

### Step 3: Capture Execution Feedback

If you encounter an agent-specific obstacle during execution (e.g., a tool call is unavailable, output format doesn't match expectations, a workaround was needed), generate a feedback document at:

```
.specify/memory/feedback/browser-utils-<agent-slug>-<YYYY-MM-DDTHH-MM-SS>.md
```

The feedback document MUST contain:

```markdown
# Agent Execution Feedback

**Source**: browser-utils
**Agent**: <agent-slug>
**Timestamp**: <ISO-8601>
**Outcome**: <success-with-workaround | partial-failure | full-failure>

## Obstacle
[Description of the agent-specific issue encountered]

## Workaround Applied
[What was done to work around the issue, if anything]

## Suggested Improvement
[Specific change to the skill or reference document that would prevent this issue]
```

Only generate feedback when a genuine agent-specific obstacle was encountered.

## Feedback

**Runtime-mode gate.** If `${SKILL_WORKDIR}/.specify/` does not exist, this skill is
running in standalone mode (a non–Spec Kit deployment, e.g. a global agent skills
directory) — skip this entire Feedback step: no engine call, no feedback entry.

At the end of a substantial run of this skill, perform an agent self-reflection step (never solicit feedback content from the user), following the canonical convention in `.specify/shared/workflow/feedback-step.md`:

1. **Gate on qualification & completion.** Only proceed if this run reached a meaningful wrap-up. Skip trivial/no-op runs; for an aborted run use the abort/partial rule below.
2. **Reflect (no user input).** Review this run against this skill's declared purpose and produce a short review plus ≥1 concrete, skill-specific optimization point. If the run was clean, use exactly: `No significant optimization points identified this run.`
3. **Scope guard.** Keep strictly to this skill's operation; do NOT produce a global/whole-project assessment (that is `/speckit.review`'s job). Entries are `scope: local`.
4. **Dedup guard.** Use a stable `run_id`; if a parent flow already recorded feedback for this same `(unit_id, run_id)`, the engine no-ops.
5. **Persist** via the engine:
   ```bash
   python3 "${SKILL_WORKDIR:-.}/.specify/scripts/python/feedback-utils.py" --action record \
     --unit-id "skill:browser-utils" --unit-type skill \
     --run-id "<stable-run-id>" --feature "<feature-key-if-any>" \
     --review "<review prose>" --points-file "<points file>"
   ```
   Probe attribution: the engine resolves the unit to its probe object automatically — the entry inherits kind/slice from the probe registry. External custom units record via `--unit-id custom:<owner>/<name> --unit-type custom-unit`; their entries stay host-project-local and never enter upstream packages.
6. **Consolidated submission prompt(非阻塞).** If the returned `should_prompt` is `true`, append ONE non-blocking line to the wrap-up report inviting submission (point the user to the `/speckit.feedback package` command — the user-facing path; never paste the raw `feedback-utils.py` engine call into the user-facing line); it MUST NOT block the wrap-up flow and MUST NOT trigger any 自动传输 (manual delivery only; `--action mark-submitted` runs only if the user initiates submission). Below threshold, do not prompt.

**Abort / partial-run rule.** If the run failed before wrap-up, either skip recording or record with `--partial` and a `## Review` beginning `**Partial run** — `.
