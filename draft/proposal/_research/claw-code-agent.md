# Mining Report: claw-code-agent

Source: `/cws_work/claw-code-agent` (HarnessLab/claw-code-agent, branch analyzed at commit `167571d`)

## Project snapshot

claw-code-agent is a **zero-dependency Python reimplementation of the Claude Code agent architecture** aimed at running full agentic coding loops against *local* OpenAI-compatible model servers (vLLM, Ollama, LiteLLM Proxy, OpenRouter). Its runtime core (`src/agent_runtime.py`, ~4,300 lines) is a real, runnable agent loop: it iterates turns, calls a stdlib-only chat client, dispatches ~65 built-in tools, streams tool results, tracks cost/budgets, compacts context, and persists/resumes sessions. It differs sharply from spec-kit's static markdown-driven `/speckit.*` flow: where spec-kit *emits prompts for a host harness to execute*, claw-code-agent *is the harness* — it owns the loop, the tools, and the model connection. The project is explicitly benchmarked (17 eval suites plus custom coding tasks, Terminal-Bench, and a Harbor adapter) and tracks fidelity to upstream Claude Code via a detailed **parity checklist** methodology. For spec-kit's goal of becoming a *universal agent-coding framework unifying skills + commands + workflows + scripts*, this repo is the single most relevant reference for the missing "runtime" half.

## Top ideas for spec-kit

### 1. A minimal, dependency-free agent runtime loop that spec-kit workflows can actually execute
- **Idea**: Add an optional runnable agent loop so spec-kit's `/speckit.*` commands/skills can be *executed* (not just rendered as prompts for a host tool). The loop pattern is compact: build system prompt + tool specs, then `for turn in range(max_turns)`: query model → if tool_calls, execute + append results → else return. See the whole loop in `src/agent_runtime.py:528` (`_run_prompt`), entrypoints `run`/`resume` at `src/agent_runtime.py:358-411`.
- **Source evidence**: `/cws_work/claw-code-agent/src/agent_runtime.py` (loop at line 528; turn/tool cycle), `/cws_work/claw-code-agent/src/agent_types.py` (dataclasses for `AgentRunResult`, `ToolCall`, `UsageStats`, `BudgetConfig`).
- **Why it helps**: spec-kit today depends entirely on an external harness to run its markdown. A small native loop makes spec-kit a *universal* framework that works even where no Claude Code/Cursor host exists (CI, local models, air-gapped), directly closing the "no runnable agent loop/runtime" gap.
- **Maps to spec-kit as**: infra (+ command `specify run`).
- **Value**: H — **Effort**: H.
- **Adoption sketch**: Port `agent_runtime` loop skeleton + `agent_types` dataclasses into `src/specify_cli/runtime/`. Wire a `specify run <spec|task>` command that loads the relevant `/speckit.*` template as the system/user prompt and drives the loop. Keep it optional (host-harness mode stays default).

### 2. Stdlib-only OpenAI-compatible client for local/self-hosted models
- **Idea**: A ~400-line chat client built entirely on `urllib` (no `openai`/`httpx`/SDK) that supports both non-streaming and SSE streaming, tool calls, usage parsing across vendor field-name variants (`prompt_tokens`/`prompt_eval_count`/`input_tokens`), and JSON-schema structured output.
- **Source evidence**: `/cws_work/claw-code-agent/src/openai_compat.py` (full client; usage normalization at lines 91-116; SSE parser at 300-343; response_format at 119-131). Backend setup documented in `/cws_work/claw-code-agent/TESTING_GUIDE.md` §1 (vLLM/Ollama/LiteLLM commands + `OPENAI_BASE_URL/KEY/MODEL` env vars).
- **Why it helps**: Fills the "local-model support" gap with zero new dependencies — spec-kit stays a clean CLI. Lets SDD workflows run on cheap/local models (Qwen3-Coder etc.), broadening adoption to privacy-sensitive and offline users.
- **Maps to spec-kit as**: infra.
- **Value**: H — **Effort**: M.
- **Adoption sketch**: Drop `openai_compat.py` in near-verbatim as `src/specify_cli/runtime/model_client.py`; drive it from the same three env vars. Document a "local model" section mirroring TESTING_GUIDE §1.

### 3. Declarative tool registry: one dataclass → OpenAI tool schema + handler
- **Idea**: Represent each tool as a frozen dataclass (`name`, `description`, JSON-schema `parameters`, `handler`) with a `.to_openai_tool()` method and a `default_tool_registry()` factory returning a `dict[str,AgentTool]`. Execution is uniform (`execute_tool` / `execute_tool_streaming`) with structured `ToolExecutionResult` and error-kind tagging.
- **Source evidence**: `/cws_work/claw-code-agent/src/agent_tools.py` (`AgentTool` dataclass at line 78; `to_openai_tool` at 85; registry factory at 215; ~65 tools; file/edit/glob/grep/bash/web_fetch handlers at 1347-1900).
- **Why it helps**: Gives spec-kit a concrete, extensible tool surface (read/write/edit/glob/grep/bash/web_fetch/LSP) — the "tool implementations" gap. The dataclass-per-tool pattern is exactly how spec-kit could let users register custom tools alongside skills/commands, unifying the "tools" pillar.
- **Maps to spec-kit as**: infra + template (tool-definition scaffold).
- **Value**: H — **Effort**: M.
- **Adoption sketch**: Adopt the `AgentTool` dataclass and registry; start with the read-only + edit + bash subset. Expose a `draft/tools/*` authoring format that compiles to `AgentTool` entries.

### 4. Parity-checklist methodology for tracking coverage against a reference
- **Idea**: A single living checklist that enumerates every capability of the reference implementation, marks Done/Missing with `[x]/[ ]`, cites the exact upstream source path each item mirrors, and groups by runtime surface (runtime, CLI, prompt assembly, tools, permissions, MCP/plugins/skills, etc.). It explicitly separates "functionality parity" from "line-by-line equivalence."
- **Source evidence**: `/cws_work/claw-code-agent/PARITY_CHECKLIST.md` (20 sections; e.g., tool list §6 lines 377-481, tiered "High-Priority Next Steps" 803-844).
- **Why it helps**: spec-kit wants to "unify skills + commands + workflows + scripts" and support "multi-harness" + "parity testing." This is a ready-made governance artifact for tracking which harnesses/agents/skills are supported and what's outstanding — turns a fuzzy roadmap into a checkable inventory.
- **Maps to spec-kit as**: workflow/process (doc + template).
- **Value**: H — **Effort**: L.
- **Adoption sketch**: Create `draft/proposal/PARITY.md` (or per-harness checklists) using the same sectioned `[x]/[ ]` + source-citation format to track command/skill/harness coverage.

### 5. Self-verifying benchmark harness: `instruction + setup + verify` tasks in throwaway workspaces
- **Idea**: Define coding tasks as `(id, category, difficulty, instruction, setup, verify)` where `setup` and `verify` are shell snippets (`verify` returns exit 0 on pass). The runner creates an isolated temp workspace, runs setup, invokes the *real* agent CLI one-shot, runs verify, scores pass/fail, and prints category/difficulty breakdowns. Optional per-problem artifact capture (prompt, agent output, workspace copy, result.json) for failures.
- **Source evidence**: `/cws_work/claw-code-agent/benchmarks/tasks/definitions.py` (`BenchmarkTask` dataclass + tasks), `/cws_work/claw-code-agent/benchmarks/run.py` (workspace isolation + scoring), `/cws_work/claw-code-agent/benchmarks/suites/base.py` (`run_all`, artifact saving lines 186-223, temp-workspace helper 35-43).
- **Why it helps**: Directly fills the "benchmarking/parity testing" gap. Because verification is objective shell exit codes, spec-kit could measure whether its SDD flow *actually produces working code* across models/harnesses — a regression harness for prompt/template changes.
- **Maps to spec-kit as**: script + infra (benchmark suite).
- **Value**: H — **Effort**: M.
- **Adoption sketch**: Add `benchmarks/` with a `SpecTask` dataclass (`instruction/setup/verify`) and a runner that shells out to spec-kit's flow in a temp dir. Seed with SDD-shaped tasks ("write a spec, then implement, then tests pass").
- **Bonus**: 17 standardized eval suites with a JSONL loader + graceful builtin-subset fallback (`benchmarks/suites/*.py`, `benchmarks/download_datasets.py`) and ELO/multiple-choice scorers — reusable if broader evals are ever wanted.

### 6. Prompt-type "bundled skills" with `when_to_use` + `allowed_tools` gating
- **Idea**: Skills defined as dataclasses that (a) generate a prompt (e.g. inject `git diff` into a review prompt), (b) carry `when_to_use` guidance so the *model* can auto-invoke them, (c) restrict `allowed_tools` during execution, and (d) surface in system-reminder listings for discovery.
- **Source evidence**: `/cws_work/claw-code-agent/src/bundled_skills.py` (`BundledSkill` dataclass lines 24-33; `_simplify_prompt` injects live `git diff` lines 39-70).
- **Why it helps**: spec-kit already has skills but as static markdown. The `when_to_use` + `allowed_tools` + dynamic-context-injection pattern makes skills *runtime-aware and auto-selectable*, a step toward unifying skills with the executable runtime.
- **Maps to spec-kit as**: skill (enhanced schema).
- **Value**: M — **Effort**: M.
- **Adoption sketch**: Extend spec-kit SKILL.md frontmatter with `when_to_use`/`allowed_tools`; when the runtime (idea #1) is present, let the model select skills by `when_to_use`.

### 7. Sub-agent definitions as data (allow/deny tool lists, model, one-shot, isolation)
- **Idea**: Built-in agent *types* (explore, general-purpose, verification, plan, etc.) declared as `AgentDefinition` dataclasses with `when_to_use`, per-agent `model`, `tools` allow-list, `disallowed_tools` deny-list, `one_shot`, `max_turns`, `isolation`, and `initial_prompt`. A default deny-set removes dangerous tools from all children.
- **Source evidence**: `/cws_work/claw-code-agent/src/builtin_agents.py` (`AgentDefinition` lines 22-49; `ALL_AGENT_DISALLOWED_TOOLS` 54-58; explore/plan deny-sets 60+). Discovery from `~/.claude/agents` + `./.claude/agents` noted in PARITY §1 lines 117-120.
- **Why it helps**: spec-kit has role-based agents as markdown; this gives a structured, permission-scoped agent schema and a delegation model (topological dependency batching, PARITY §1 lines 47-55) — useful for the "workflow/process" pillar (e.g., planner → implementer → reviewer with scoped tools).
- **Maps to spec-kit as**: agent (schema) + template.
- **Value**: M — **Effort**: M.
- **Adoption sketch**: Add allow/deny tool lists + `model`/`one_shot`/`isolation` fields to spec-kit's `*.agent.md` frontmatter; enforce them when the runtime executes a delegated agent.

### 8. Layered bash security validator (ALLOW/ASK/DENY/PASSTHROUGH)
- **Idea**: A standalone `bash_command_is_safe(command)` returning a `SecurityResult` with a four-state behavior enum, detecting dangerous/obfuscated/destructive commands via composable validators (163 tests per PARITY §8 line 535).
- **Source evidence**: `/cws_work/claw-code-agent/src/bash_security.py` (types + `_allow/_ask/_deny` lines 26-49), permission modes in `agent_tools.py` (`_ensure_shell_allowed` line 1320).
- **Why it helps**: Any runtime that runs shell (idea #1/#3) needs guardrails; the ASK tier maps naturally onto spec-kit's permission/confirmation UX and CI safety.
- **Maps to spec-kit as**: script/infra.
- **Value**: M — **Effort**: L (drop-in module).
- **Adoption sketch**: Vendor `bash_security.py` and call it before executing any bash tool in the runtime.

### 9. Harbor adapter + rootless-Docker bootstrap for cluster/CI benchmarking
- **Idea**: A ~90-line `BaseInstalledAgent` subclass that installs the CLI in a Harbor environment and runs it one-shot against the task cwd (declarative `CLI_FLAGS`/`ENV_VARS`), plus a script that stands up *rootless* Docker entirely under `$SCRATCH` for HPC nodes without root, and a Terminal-Bench-over-Apptainer runner for Docker-less clusters.
- **Source evidence**: `/cws_work/claw-code-agent/harbor_adapter.py`, `/cws_work/claw-code-agent/install_dockor.sh`, `/cws_work/claw-code-agent/benchmarks/run_terminal_bench_local.py`.
- **Why it helps**: Makes external, reproducible eval feasible in restricted environments — supports the "parity testing across harnesses" goal.
- **Maps to spec-kit as**: script/infra.
- **Value**: M — **Effort**: L.
- **Adoption sketch**: Provide an analogous Harbor adapter for `specify` and reuse `install_dockor.sh` verbatim for sandboxed benchmark runs.

### 10. User-facing "Testing Guide" organized by runtime surface, not by file
- **Idea**: A test/QA doc where every implemented feature has at least one concrete copy-pasteable command, grouped by runtime surface (backends, CLI modes, tools, permissions...).
- **Source evidence**: `/cws_work/claw-code-agent/TESTING_GUIDE.md`.
- **Why it helps**: As spec-kit grows commands/skills/workflows, a surface-oriented command catalog doubles as manual-test checklist and living docs.
- **Maps to spec-kit as**: workflow/process (doc).
- **Value**: L — **Effort**: L.
- **Adoption sketch**: Maintain a `TESTING_GUIDE.md` listing one runnable command per command/skill/workflow.

## Notable code/prompts worth copying (file paths)

- `/cws_work/claw-code-agent/src/openai_compat.py` — near-verbatim reusable stdlib OpenAI-compatible client (streaming + tools + structured output + cross-vendor usage parsing).
- `/cws_work/claw-code-agent/src/agent_tools.py` — `AgentTool` dataclass + `to_openai_tool()` + `default_tool_registry()` + concrete file/edit/glob/grep/bash/web_fetch handlers.
- `/cws_work/claw-code-agent/src/agent_runtime.py` (lines 358-700) — the turn loop, continuation-on-truncation, budget checks, reactive compaction.
- `/cws_work/claw-code-agent/src/agent_types.py` — clean dataclass vocabulary (`AgentRunResult`, `ToolCall`, `StreamEvent`, `UsageStats`, `BudgetConfig`, `OutputSchemaConfig`).
- `/cws_work/claw-code-agent/benchmarks/suites/base.py` + `/cws_work/claw-code-agent/benchmarks/run.py` — self-verifying benchmark harness with temp-workspace isolation and artifact capture.
- `/cws_work/claw-code-agent/benchmarks/tasks/definitions.py` — `instruction/setup/verify` task schema (great template for SDD-shaped eval tasks).
- `/cws_work/claw-code-agent/src/bash_security.py` — drop-in ALLOW/ASK/DENY shell validator.
- `/cws_work/claw-code-agent/src/bundled_skills.py` — prompt-type skill schema (`when_to_use`, `allowed_tools`, live-context injection).
- `/cws_work/claw-code-agent/src/builtin_agents.py` — data-driven agent definitions with scoped tool allow/deny.
- `/cws_work/claw-code-agent/PARITY_CHECKLIST.md` — the parity-tracking format.
- `/cws_work/claw-code-agent/harbor_adapter.py`, `/cws_work/claw-code-agent/install_dockor.sh` — external-eval plumbing.

## Anti-patterns / what to skip

- **Don't chase full Claude Code parity.** The parity checklist enumerates hundreds of items (Ink TUI 40+ files, 84+ React hooks, bridge/remote 30+ files, voice/vim/buddy, migrations). Most are host-app concerns irrelevant to spec-kit's framework goal. Copy the *methodology*, not the scope.
- **Skip the "mirrored/scaffold" inventory layers.** PARITY §20 admits large parts of the workspace are "inventory or scaffolding" (`src/commands.py`, `src/tools.py`, `src/reference_data/*`) that don't back real behavior. Adopt only the working runtime modules listed above; don't replicate the empty mirror.
- **Don't over-port the runtime's accreted complexity.** `agent_runtime.py` is ~4,300 lines with deeply interleaved budget/compaction/mutation-serial/lineage bookkeeping. For spec-kit, extract the *loop skeleton and tool dispatch* first; treat compaction/microcompact/mutation-history as optional later layers, not day-one requirements.
- **The GUI (FastAPI + vanilla JS SPA) adds the repo's only 3 runtime deps** (`fastapi`, `uvicorn`, `pydantic` in `pyproject.toml`) — it breaks the "zero dependency" claim. If spec-kit ports the runtime, keep the GUI out to preserve a clean CLI install.
- **Emoji-in-output reporting** (`✅/❌` in benchmark tables) is fine internally but avoid baking emoji into spec-kit's user-facing tooling output.
- **Bundled benchmark subsets are tiny** (5-20 problems/suite) and meant as smoke tests, not real scores — don't treat built-in-subset numbers as authoritative; wire real JSONL datasets before publishing any results.
