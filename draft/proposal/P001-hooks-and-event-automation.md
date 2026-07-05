# P001 — Hooks & Event Automation

- **Status:** Draft
- **Pillars:** Workflow/Process · Infra
- **Source projects:** claude-code-py, superpowers, claude-code-ts, learn-claude-code
- **Value:** H · **Effort:** M · **Phase:** 1
- **Related:** [[P005]], [[P006]], [[P009]], [[P012]]

## Problem / Gap

spec-kit encodes process as *prose*. The constitution states principles, command files
describe steps, and skills carry trigger keywords — but nothing *enforces* any of it. Whether
`/speckit.implement` runs before an approved plan exists, whether a spec is linted after it is
written, or whether a completion claim is backed by verification evidence all depend on the
agent choosing to comply. This is the missing **Process** backbone of the universal-framework
goal: the workflow should be deterministically steerable at lifecycle points, not merely
suggested.

Everything downstream in this proposal set benefits from the same layer. The autonomous loop
([[P005]]) needs a `Stop` signal; verification gates ([[P006]]) want to fire on `Stop` /
`PreToolUse`; the workflow engine ([[P009]]) wants `PostToolUse` progress events. A single,
well-factored hook layer powers all of them.

## Proposal

Add an event-driven hook layer to spec-kit, expressed as configuration and small scripts that
layer on top of the host harness — not a runtime spec-kit owns. Three capabilities:

1. **An event → command hook system** wired through `.specify/hooks/hooks.json`, dispatched by a
   portable runner that follows the standard exit-code contract (`0` = ok, `2` = block with
   stderr fed back to the agent). Events: `SessionStart`, `UserPromptSubmit`, `PreToolUse`,
   `PostToolUse`, `Stop`, `SubagentStop`, `PreCompact`.
2. **Markdown guardrail rules** authored in spec-kit's existing frontmatter idiom
   (`.specify/rules/*.md`: matcher / condition / action / message), evaluated by one small
   stdlib engine — so users declare enforceable checks the same way they write skills and
   templates.
3. **Hooks declared from skill/agent frontmatter** that auto-register for the session, so the
   automation travels *with* the artifact (a TDD skill can run tests on `PostToolUse[Edit]`; a
   spec skill can validate on `Stop`).

On Claude Code these map natively to `settings.json` hooks. For harnesses without a native hook
runner, spec-kit ships the scripts plus a thin dispatcher so the same rules are reusable.

## Design sketch

### File layout (lands in `draft/` first)

```
draft/
  hooks/
    hooks.json                # event → command registration
    run-hook.sh               # POSIX dispatcher (reads hook JSON on stdin)
    run-hook.cmd              # polyglot cmd/bash wrapper for Windows
    handlers/
      session-start.sh        # inject using-speckit bootstrap + feature context
      pre-implement-guard.sh  # block implement without an approved plan
      post-write-spec-lint.sh # lint spec/plan on write
      stop-verification.sh    # remind/require verification evidence (see [[P006]])
  rules/
    dangerous-rm.md
    require-plan-before-implement.md
  scripts/python/
    rule_engine.py            # matcher/condition/action, block > warn priority
    rule_loader.py            # parse rule frontmatter (backed by a real YAML lib)
```

### `hooks.json` — event → command

```json
{
  "hooks": {
    "SessionStart": [
      { "matcher": "startup|clear|compact",
        "command": "${SPECIFY_DIR}/hooks/handlers/session-start.sh" }
    ],
    "PreToolUse": [
      { "matcher": "Write|Edit",
        "command": "${SPECIFY_DIR}/hooks/run-hook.sh rules" }
    ],
    "Stop": [
      { "command": "${SPECIFY_DIR}/hooks/handlers/stop-verification.sh" }
    ]
  }
}
```

The dispatcher reads the harness's hook-input JSON on stdin, runs matching handlers/rules, and
uses the exit-code contract: exit `2` blocks the action and the handler's **stderr** is fed back
to the agent as the reason. Any other non-zero is a soft warning; `0` allows.

### Guardrail rule (markdown + frontmatter)

```markdown
---
id: require-plan-before-implement
event: PreToolUse
matcher: "Bash"
condition: "command contains 'speckit.implement'"
action: block            # block | warn
message: "No approved plan found for the active feature. Run /speckit.plan first."
priority: 100
---
Blocks the implement phase until `plan.md` exists and the plan-review gate has passed.
The engine resolves `block` over `warn` when multiple rules match.
```

`rule_engine.py` and `rule_loader.py` are a stdlib-only port of the hookify engine
(matcher/condition/action, `block` beats `warn`, per-event output shaping). Rules read from
`.specify/rules/*.md`; a later `/speckit.guardrail` command can scaffold new ones.

### Hooks declared from skill / agent frontmatter

```yaml
---
name: test-driven-development
description: "Use when implementing a task that needs tests written first."
hooks:
  PostToolUse:
    - matcher: "Edit|Write"
      type: command
      command: "scripts/bash/run-tests.sh {{file}}"
      once: false
  Stop:
    - type: command
      command: "scripts/python/verify_tests_ran.py"
---
```

A small `register_frontmatter_hooks` step collects `hooks:` blocks from active
skills/agents and merges them into the session hook set (agent `Stop` hooks rewrite to
`SubagentStop`). This is the "automation travels with the artifact" pattern — the core of
unifying skills + workflows + scripts.

### SessionStart auto-injection

`session-start.sh` wraps the existing `scripts/bash/detect-feature-context.sh` output plus a
short `using-speckit` bootstrap ("here is the `/speckit.*` pipeline; check for an applicable
skill/command before acting") in the harness context-injection envelope, selecting the right
field per harness:

```bash
# Claude Code:  {"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":"…"}}
# opencode/qwen: {"additionalContext":"…"}  |  cursor: {"additional_context":"…"}
```

### Claude Code wiring (`.claude/settings.json`)

```json
{ "hooks": { "SessionStart": [ { "hooks": [
  { "type": "command", "command": ".specify/hooks/handlers/session-start.sh" } ] } ] } }
```

### Seed hooks shipped with the layer

| Hook | Event | Effect |
|------|-------|--------|
| `session-start` | SessionStart | inject feature context + bootstrap |
| `pre-implement-guard` | PreToolUse | block implement without approved plan |
| `post-write-spec-lint` | PostToolUse | lint spec/plan/tasks structure on write |
| `stop-verification` | Stop | require a fresh verification log ([[P006]]) |

## Source evidence

- Event → script hook model, exit-code-2 block contract, `${ROOT}` portability —
  `/cws_work/claude-code-py/plugins/hookify/hooks/hooks.json`,
  `/cws_work/claude-code-py/examples/hooks/bash_command_validator_example.py`,
  `/cws_work/claude-code-py/plugins/plugin-dev/skills/hook-development/SKILL.md`.
- Markdown guardrail rule engine (matcher/condition/action, block>warn) —
  `/cws_work/claude-code-py/plugins/hookify/core/rule_engine.py`,
  `/cws_work/claude-code-py/plugins/hookify/core/config_loader.py`,
  `/cws_work/claude-code-py/plugins/hookify/examples/dangerous-rm.local.md`.
- Hooks declared from skill/agent frontmatter, auto-register/auto-clean, `once`, agent-`Stop`→
  `SubagentStop` — `/cws_work/claude-code-ts/src/utils/hooks/registerFrontmatterHooks.ts`,
  `/cws_work/claude-code-ts/src/utils/hooks/registerSkillHooks.ts`,
  `/cws_work/claude-code-ts/src/utils/hooks/hookEvents.ts`.
- SessionStart context-injection + polyglot wrapper —
  `/cws_work/superpowers/hooks/session-start`, `/cws_work/superpowers/hooks/run-hook.cmd`,
  `/cws_work/superpowers/hooks/hooks.json`;
  spec-kit's existing `scripts/bash/detect-feature-context.sh`.
- Hook registry model (four events, non-None/blocking return) and permission gate layering —
  `/cws_work/learn-claude-code` `s04_hooks/README.en.md`, `s03_permission/README.en.md`.
- Conditional/async review-on-commit matchers (aspirational) —
  `/cws_work/claude-code-py/plugins/security-guidance/hooks/hooks.json`.

## Adoption plan

1. **Land in `draft/hooks/` + `draft/rules/` + `draft/scripts/python/`** — no wiring into the
   live flow. Port `rule_engine.py` / `rule_loader.py` (back the frontmatter parse with the YAML
   lib spec-kit already depends on rather than the hand-rolled parser).
2. **Ship the runner + three seed handlers** (`session-start`, `post-write-spec-lint`,
   `stop-verification`) and prove them against Claude Code `settings.json`.
3. **Add the `hooks:` frontmatter block** to the skill/agent templates and a
   `register_frontmatter_hooks` helper; keep it opt-in per artifact.
4. **Promote deliberately.** Only after review does `/speckit.instructions` emit the hook
   registration into host config. Until then the layer is inert: **nothing here changes the
   `/speckit.*` command flow** — hooks observe and gate, they do not rewrite the pipeline.

## Risks & mitigations

- **Portability.** Only Claude Code executes hooks natively today. *Mitigation:* ship the
  scripts + thin dispatcher so other harnesses can run rules on demand; treat native hooks as an
  enhancement, not a requirement.
- **Over-blocking / friction.** Aggressive `block` rules could stall legitimate work.
  *Mitigation:* default seed rules to `warn`; require explicit opt-in for `block`; honor
  spec-kit's "user instructions take precedence" model.
- **Guardrails are not security.** String-match matchers are bypassable. *Mitigation:* document
  them as a UX/process speed-bump; real enforcement belongs in host permission config ([[P012]]).
- **Prompt/LLM-in-the-hook is non-portable.** *Mitigation:* prefer `type: command` scripts;
  treat `prompt`/`agent` hooks as Claude-Code-only extras.

## Value / Effort rationale

**Value H:** this is the enforceable process layer the framework lacks, and the shared substrate
for [[P005]], [[P006]], and [[P009]] — high leverage per line. **Effort M:** the rule engine and
session-start logic are near-drop-in ports from claude-code-py and superpowers; the frontmatter
hook registration is modest; no runtime is built. Phase 1 because it is mostly config + small
scripts and touches nothing in the live pipeline until promoted.
