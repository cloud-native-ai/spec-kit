# P011 — Optional Runtime, Local Models & Benchmarking

- **Status:** Draft
- **Pillars:** Scripts
- **Source projects:** claw-code-agent
- **Value:** M–H · **Effort:** H · **Phase:** 3
- **Related:** [[P008]], [[P009]], [[P004]], [[P013]]

## Problem / Gap

spec-kit is **scaffolding, not a runtime**: `/speckit.*` commands emit markdown prompts and
scripts that an external harness (Claude Code, Copilot, opencode, Qwen, Qoder) executes.
That is the right default and this proposal does not change it. But it leaves three
capabilities off the table entirely:

1. **No way to *execute* the flow without a host harness.** In CI, on an air-gapped box, or
   when validating a template change, there is no `specify`-native way to run a spec →
   implement loop end to end. The framework can describe work but cannot perform it.
2. **No local-model story.** Teams with vLLM/Ollama/LiteLLM deployments (privacy-sensitive,
   offline, cost-constrained) cannot drive the SDD flow with their own models.
3. **No objective measurement.** There is no harness to answer "does this template/skill
   change actually make the flow produce *working* code?" — prompt/template edits ship blind.

claw-code-agent is the reference for exactly this missing half: a zero-dependency Python
agent loop, a stdlib OpenAI-compatible client for local servers, and a self-verifying
benchmark harness. The task is to port the *design* (not the 4,300-line accretion) as an
**optional, opt-in** layer that never competes with the scaffolding model.

## Proposal

Add an **optional runtime** under `src/specify_cli/runtime/`, shipped as an extra
(`specify[runtime]`) and reachable only via new explicit commands. It provides:

- **A. Stdlib OpenAI-compatible client** — `urllib`-only, streaming + tool-calls +
  structured output, cross-vendor usage normalization; driven by three env vars.
- **B. Minimal turn/tool loop** — build system prompt + tool specs, then iterate:
  query → dispatch tool calls → append results → repeat until done or budget hit. Tools come
  from the [[P008]] descriptor registry; shell goes through [[P008]]'s bash-security
  validator.
- **C. Parity-checklist methodology** — a living inventory that enumerates each runtime
  capability, marks Done/Missing, and cites the upstream path it mirrors, keeping the port
  honest and bounded.
- **D. Self-verifying benchmark harness** — tasks as `(instruction, setup, verify)` run in
  isolated throwaway workspaces; `verify` exit 0 = pass. Gives spec-kit a regression signal
  for template/skill/prompt changes.

The runtime consumes existing spec-kit artifacts: it loads a `/speckit.*` template as the
prompt, reads the [[P013]] `status --json`/`instructions` contract to know what to build
next, and can execute [[P009]] workflow steps or [[P004]] task-graph nodes. It adds *no*
new authoring surface — it is an executor for what spec-kit already emits.

## Design sketch

### D.1 Module layout

```
src/specify_cli/runtime/            # only imported when the runtime extra is installed
  __init__.py
  model_client.py     # stdlib OpenAI-compatible client (urllib)
  loop.py             # turn/tool loop
  types.py            # AgentRunResult, ToolCall, UsageStats, BudgetConfig
  session.py          # persist/resume a run
benchmarks/
  tasks/definitions.py   # SpecTask dataclass + seed SDD tasks
  run.py                 # workspace isolation + scoring + artifact capture
draft/proposal/PARITY.md # capability inventory (methodology artifact)
```

### D.2 Model client (A)

```python
# model_client.py — no openai/httpx/SDK dependency
class ModelClient:
    def __init__(self, base_url=env("OPENAI_BASE_URL"),
                 api_key=env("OPENAI_API_KEY"), model=env("OPENAI_MODEL")): ...
    def chat(self, messages, tools=None, response_format=None, stream=False): ...
```

Usage parsing normalizes vendor field variants
(`prompt_tokens`/`prompt_eval_count`/`input_tokens`) into one `UsageStats`, so vLLM,
Ollama, LiteLLM Proxy, and OpenRouter are interchangeable. Backends are documented in a
"local model" doc section mirroring claw-code's TESTING_GUIDE §1 (the three env vars +
server-start commands). No provider is hard-coded; Anthropic/OpenAI hosted endpoints work
through the same OpenAI-compatible shape.

### D.3 Turn/tool loop (B)

```python
# loop.py
def run(prompt: str, tools: list[ToolDescriptor], budget: BudgetConfig) -> AgentRunResult:
    messages = [system_prompt(tools), user(prompt)]
    for turn in range(budget.max_turns):
        resp = client.chat(messages, tools=[t.to_openai_tool() for t in tools])
        if not resp.tool_calls:
            return AgentRunResult(text=resp.text, usage=..., stop="complete")
        for call in resp.tool_calls:
            guard = bash_command_is_safe(...) if call.name == "bash" else ALLOW  # P008
            result = dispatch(call, tools, guard)
            messages.append(tool_result(call, result))
    return AgentRunResult(stop="max_turns", ...)
```

The loop skeleton and dispatch are the *only* parts ported day-one; compaction, microcompact,
and mutation-history bookkeeping from the upstream 4,300-line runtime are explicitly deferred
as optional later layers. Tools are resolved from the [[P008]] registry — the runtime does
not define its own tool set.

### D.4 CLI surface (opt-in, isolated)

```
specify run <artifact|spec-file> [--model … --base-url … --max-turns N]
    # loads the matching /speckit.* template as prompt, drives the loop
specify run --workflow <name>        # execute a P009 workflow step-by-step
specify bench run [--suite sdd] [--json]   # self-verifying benchmark harness
```

`specify run` is absent unless the runtime extra is installed, so the default install and the
default `/speckit.*` experience are byte-for-byte unchanged.

### D.5 Benchmark harness (D)

```python
# benchmarks/tasks/definitions.py
@dataclass
class SpecTask:
    id: str; category: str; difficulty: str
    instruction: str        # what to ask the flow to do
    setup: str              # shell: prepare the workspace
    verify: str             # shell: exit 0 == pass

# benchmarks/run.py
def run_task(task, agent_cmd):
    with temp_workspace() as ws:
        sh(task.setup, cwd=ws)
        invoke(agent_cmd, task.instruction, cwd=ws)   # shells out to `specify run`
        return sh(task.verify, cwd=ws).returncode == 0
```

The runner isolates each task in a temp dir, runs the *real* `specify run` one-shot, scores
pass/fail, prints category/difficulty breakdowns, and (on failure) captures
prompt+output+workspace+`result.json`. Seed suite = SDD-shaped tasks ("given this feature
request, run spec→plan→tasks→implement; tests pass"). Because verification is objective shell
exit codes, this becomes the regression gate for [[P013]] validation and for any
template/skill edit.

### D.6 Parity checklist (C)

`draft/proposal/PARITY.md` uses claw-code's sectioned `[x]/[ ]` format, one section per
runtime surface (client, loop, tools, permissions, sessions, benchmarks), each item citing
the upstream path it mirrors. It separates *functionality parity* from *line-by-line
equivalence* and caps scope: host-app concerns (TUI, remote bridge, voice) are marked
out-of-scope by design, not left as open TODOs.

## Source evidence

- Minimal agent runtime loop (turn/tool cycle, entrypoints) →
  `_research/claw-code-agent.md` idea #1 (`src/agent_runtime.py` `_run_prompt` line 528,
  `run`/`resume` 358-411; loop detail 358-700).
- Stdlib OpenAI-compatible client (streaming, tools, structured output, usage normalization) →
  `_research/claw-code-agent.md` idea #2 (`src/openai_compat.py`; usage norm 91-116, SSE 300-343,
  `response_format` 119-131; backends in `TESTING_GUIDE.md` §1).
- Clean dataclass vocabulary for results/usage/budget →
  `_research/claw-code-agent.md` (`src/agent_types.py`: `AgentRunResult`, `ToolCall`,
  `UsageStats`, `BudgetConfig`, `OutputSchemaConfig`).
- Parity-checklist methodology (Done/Missing + upstream citations, functionality vs line parity) →
  `_research/claw-code-agent.md` idea #4 (`PARITY_CHECKLIST.md`, 20 sections).
- Self-verifying benchmark harness (`instruction/setup/verify`, temp-workspace isolation,
  artifact capture) → `_research/claw-code-agent.md` idea #5
  (`benchmarks/tasks/definitions.py`, `benchmarks/run.py`, `benchmarks/suites/base.py` 35-43, 186-223).
- External-eval plumbing (Harbor adapter, rootless-Docker bootstrap) →
  `_research/claw-code-agent.md` idea #9 (`harbor_adapter.py`, `install_dockor.sh`).
- Tool registry + bash-security consumed by the loop → [[P008]]; state/next-step contract
  the loop reads → [[P013]]; workflow/task-graph steps the loop can execute → [[P009]], [[P004]].

## Adoption plan

Strictly opt-in; nothing here touches the default install or the `/speckit.*` flow.

1. **Client + types (A).** Vendor `openai_compat.py` near-verbatim as
   `runtime/model_client.py` and the dataclasses as `runtime/types.py`. Ship behind the
   `specify[runtime]` extra. Document the three env vars + local-server commands.
2. **Loop (B).** Port the loop skeleton + dispatch into `runtime/loop.py`; wire tool
   resolution to [[P008]]'s `ToolDescriptor` registry and shell guarding to its
   `bash_security.py`. Add `specify run` (guarded by the extra).
3. **Benchmarks (D).** Add `benchmarks/` with `SpecTask` + a runner that shells out to
   `specify run` in temp workspaces; seed 5–10 SDD tasks as smoke tests. Wire into CI as a
   non-blocking signal first.
4. **Parity (C).** Maintain `draft/proposal/PARITY.md` alongside the port; use it to bound
   scope and track coverage. Optional Harbor/rootless-Docker adapters land last for
   cluster/CI eval.

Promotion criteria: the runtime stays in `draft`/extra indefinitely unless a team explicitly
wants a host-free executor; the benchmark harness can graduate independently as a dev tool
even if the runtime does not.

## Risks & mitigations

- **Scope creep toward a competing harness.** The guiding principle is scaffolding, not
  runtime. Mitigate structurally: opt-in extra, separate module tree, no changes to
  `/speckit.*`, and the PARITY doc that explicitly marks host-app scope out of bounds. Port
  the loop skeleton only; defer compaction/history.
- **Dependency bloat.** Client is stdlib-only (`urllib`), preserving the clean CLI. Keep the
  benchmark/GUI-style extras out of the base install (claw-code's GUI added its only 3 runtime
  deps — we exclude that entirely).
- **Local-model quality variance.** The SDD flow may underperform on small models. Frame the
  runtime as "runs anywhere," and use the benchmark harness to publish honest per-model
  numbers rather than implying parity with hosted frontier models.
- **Benchmark results over-trusted.** Bundled task subsets are smoke tests, not scores; label
  them as such and require real task sets before publishing any figure (claw-code's own
  caveat).
- **Security of an autonomous loop.** All shell goes through [[P008]]'s ALLOW/ASK/DENY
  validator; default `--max-turns` and budget caps bound runaway loops; ASK tier maps to the
  existing confirmation UX.

## Value / Effort rationale

**Value M–H:** high for the specific audiences it unlocks (CI execution, local/offline/
privacy-sensitive teams, and — via the benchmark harness — *everyone*, since objective
regression testing of template/skill changes benefits the whole project). Rated M rather
than H overall because it is deliberately optional and off the critical path for most users,
who keep using their host harness.

**Effort H:** even ported as design-not-code, a correct turn/tool loop, cross-vendor client,
session persistence, and an isolated benchmark runner are substantial, and the layer must be
carefully fenced so it never leaks into the default flow. This is why it is Phase 3, sequenced
after the [[P008]] tool registry it depends on.
