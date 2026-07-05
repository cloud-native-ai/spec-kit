# P005 — Autonomous Loop Driver

- **Status:** Draft
- **Pillars:** Workflow/Process · Scripts
- **Source projects:** intellegix-code-agent-toolkit, claude-code-ts, claude-code-py
- **Value:** H · **Effort:** H · **Phase:** 2
- **Related:** [[P001]], [[P004]], [[P006]], [[P009]]

## Problem / Gap

spec-kit is a human-in-the-loop markdown flow: a person drives each `/speckit.*` step and decides
when a feature is done. There is no *autonomous execution substrate* — no way to run an approved
spec/plan/task set to completion unattended, and no safety rails if an agent spins, burns budget,
or declares success prematurely. The Executor-Evaluator-Improver roles describe *how* to iterate
but nothing *drives* the iteration or *decides when to stop*.

Two failure modes matter most. First, **runaway**: an agent loops on the same edit, or keeps
spending with no progress. Second, **false completion**: an agent claims "all done" without
evidence, or (worse) satisfies a completion check by deleting the checklist it was measured
against. A universal framework needs a driver whose whole job is the continue/stop decision, with
hard guardrails and an anti-evasion completion gate.

## Proposal

Add an opt-in **loop driver** that repeatedly invokes the coding agent over the active feature's
artifacts and, after each iteration, runs an ordered guardrail cascade before deciding to
continue, reset, or stop. It ships in two forms so it works with or without a native hook runner:

1. **External driver** — a slimmed Python `loop_driver.py` (vendored from intellegix) that spawns
   the harness headlessly, streams structured output, and enforces budget / timeout / stagnation
   / completion, exiting with meaningful codes. Driven by `specify run` (or `/speckit.run`).
2. **In-harness Stop-loop** — a `Stop` hook (via [[P001]]) that re-injects a continuation prompt
   until a completion condition or iteration cap is met, for harnesses where an external driver
   is impractical (the ralph-wiggum pattern).

The completion condition reuses what spec-kit already has: **`tasks.md` is the checklist.** A run
is complete only when every `- [ ]` is checked and the completion gate cannot be evaded. Steering
prompts (continuation / blocked / budget-limit) come from the claude-code-ts goal loop, whose
Completion Audit and Blocked Audit are the crown jewels.

## Design sketch

### File layout (lands in `draft/` first)

```
draft/
  scripts/loop/
    loop_driver.py        # run() guardrail cascade + invoke wrapper (slimmed)
    config.py             # Pydantic: Limits / Stagnation / CompletionGate
    state_tracker.py      # per-iteration cost/turns + budget + analytics
    completion_gate.py    # parse tasks.md unchecked boxes + anti-evasion
  templates/loop/
    continuation.md       # re-state objective + remaining tasks + Completion Audit
    blocked.md            # Blocked Audit (≥3 consecutive turns before "blocked")
  commands/
    speckit.run.md        # opt-in driver command wrapping /speckit.implement
```

Per-run state lives under the feature dir so each spec ships with its execution record:
`.specify/specs/<feature>/.loop/{state.json, trace.jsonl, metrics_summary.json}`.

### Guardrail cascade (per iteration)

```
budget check → timeout detection → error reset → stagnation check
  → completion-gate validation → post-validation → build next prompt
```

Exit codes: `0` complete · `1` max iterations · `2` budget exhausted · `3` stagnation.

### Config (Pydantic, copied near-verbatim)

```python
class LimitsConfig(BaseModel):
    max_iterations: int = 25
    max_total_usd: float = 10.0
    max_usd_per_iteration: float = 2.0
    iteration_timeout_s: int = 900

class StagnationConfig(BaseModel):
    window: int = 3                 # sliding window of recent iterations
    min_turns: int = 2             # all-below ⇒ stagnating
    two_strike: bool = True        # 1st strike resets session, 2nd exits code 3

class CompletionGateConfig(BaseModel):
    require_all_tasks_checked: bool = True
    max_false_completions: int = 2  # repeated false "done" ⇒ stagnation exit
```

### Completion gate (anti-evasion)

```python
def evaluate(tasks_md: str) -> GateResult:
    boxes = parse_checkboxes(tasks_md)          # ('- [ ]' | '- [x]', text)
    if not boxes:                               # evasion: checklist deleted/emptied
        return GateResult(complete=False, reason="task checklist missing")
    unchecked = [t for state, t in boxes if state == " "]
    if unchecked:
        return GateResult(complete=False, remaining=unchecked)
    return GateResult(complete=True)
```

The driver never trusts a self-declared `PROJECT_COMPLETE`; it re-reads `tasks.md`, rejects if
any box is open, counts rejections, and converts repeated false completions into a stagnation
exit. A missing/emptied checklist is treated as *incomplete*, not complete.

### Stagnation + session rotation

Over a sliding window, if all recent iterations are below the turn threshold (or all zero-cost),
the driver first **resets the resumed session** (strike 1); a second consecutive stagnant window
exits with code `3`. Session rotation also fires proactively after N turns / $N or on behavioral
"context exhaustion" (majority of recent iterations below a turn floor). `state_tracker.py` is
reusable standalone and is fed the cost/turn/duration the harness reports per invocation.

### Continuation steering prompt (template)

```markdown
<goal-steering>
Objective: {{ spec.objective }}
Remaining tasks (from tasks.md):
{{ remaining_tasks }}

## Completion Audit
Do NOT stop merely because you cannot find remaining work. To claim completion you must
PROVE each acceptance criterion in spec.md is satisfied, with fresh command evidence
(see [[P006]]). If you cannot prove it, continue.
</goal-steering>
```

`blocked.md` mirrors the Blocked Audit: the *same* blocking condition must persist for ≥3
consecutive turns before the run may mark itself blocked — preventing premature give-up.

### In-harness Stop-loop variant (via [[P001]])

A `Stop` hook reads `.loop/state.json`, and while `iteration < max` and the completion gate is
open, emits `decision: block` with the continuation prompt as the reason, re-feeding the agent.
Atomic state writes + corruption guards keep it robust (ralph-wiggum).

### Observability

Every iteration appends a typed event to `trace.jsonl` (`loop_start`, `agent_invoke`,
`agent_complete` with tools/files/diff-stats, `timeout_detected`, `stagnation_exit`,
`completion_detected`, `loop_end`); on exit `metrics_summary.json` aggregates cost/turns/errors
and files touched. Git-diff stats double as a cheap per-iteration progress signal for stagnation
detection. API-key patterns are redacted from logs.

## Source evidence

- Loop `run()` guardrail cascade + exit codes + NDJSON invoke —
  `/cws_work/intellegix-code-agent-toolkit/automated-loop/loop_driver.py` (`run()` 227–673),
  `/cws_work/intellegix-code-agent-toolkit/automated-loop/config.py` (LimitsConfig,
  StagnationConfig, CompletionGateConfig).
- Completion gate parse/validate + evasion handling —
  `.../automated-loop/loop_driver.py` `_parse_completion_gate` (1152–1179),
  `_validate_completion_gate` (1181–1199), gate-rejection loop (541–587).
- Stagnation, two-strike, session rotation —
  `.../automated-loop/loop_driver.py` `_check_stagnation` (1109–1143),
  `_should_rotate_session` (1064–1107); `.../automated-loop/state_tracker.py` `check_budget`
  (191–210).
- Trace/metrics observability + redaction —
  `.../automated-loop/loop_driver.py` `_write_trace_event` (128–156),
  `_write_metrics_summary` (1273–1313); `.../automated-loop/log_redactor.py`.
- Goal continuation loop + Completion/Blocked Audits + persisted goal state —
  `/cws_work/claude-code-ts/src/services/goal/prompts.ts`,
  `/cws_work/claude-code-ts/src/services/goal/goalState.ts` (`MAX_GOAL_TURNS`,
  `BLOCKED_CONSECUTIVE_THRESHOLD=3`), `/cws_work/claude-code-ts/src/hooks/useGoalContinuation.ts`.
- Bounded loop thresholds + continuation nudge —
  `/cws_work/claude-code-ts/src/query/tokenBudget.ts` (`COMPLETION_THRESHOLD=0.9`),
  `/cws_work/claude-code-ts/src/QueryEngine.ts` (typed terminal results).
- Stop-hook self-referential loop (in-harness variant) —
  `/cws_work/claude-code-py/plugins/ralph-wiggum/hooks/stop-hook.sh`,
  `/cws_work/claude-code-py/plugins/ralph-wiggum/commands/ralph-loop.md`.

## Adoption plan

1. **Vendor a slimmed `loop_driver.py` + `config.py` + `state_tracker.py` into
   `draft/scripts/loop/`.** Replace intellegix's between-iteration Perplexity research step with
   spec-kit's own artifacts (spec.md / plan.md / tasks.md as the "next step" source). Copy the
   Pydantic config tree verbatim.
2. **Add `completion_gate.py`** as a ~40-line checker over the active `tasks.md`; expose it both
   as the loop's completion condition and as a standalone `specify check-gate`.
3. **Ship the steering templates** (`continuation.md`, `blocked.md`) and wire the audits against
   the spec's acceptance criteria and [[P006]] verification evidence.
4. **Provide the in-harness `Stop`-loop** as a [[P001]] hook for harnesses without a headless
   driver, sharing the same `.loop/state.json` and completion gate.
5. **Keep it strictly opt-in.** The driver wraps `/speckit.implement`; it does not alter the
   command or any other `/speckit.*` step. **The main flow is untouched** unless a user explicitly
   invokes `specify run`.

## Risks & mitigations

- **Runaway cost/time.** *Mitigation:* hard budget/turn/timeout caps with typed exit codes; cheap
  git-diff progress signal feeding stagnation detection.
- **Premature or evaded completion.** *Mitigation:* anti-evasion gate over `tasks.md`, false-
  completion counter, evidence-based Completion Audit; missing checklist ⇒ incomplete.
- **Harness portability.** The external driver needs a headless CLI (e.g. `claude -p`). *Mitigation:*
  the in-harness Stop-loop variant covers harnesses without one; the driver transport is pluggable.
- **Scope creep vs [[P009]].** The loop drives a *single feature to completion*; multi-step /
  multi-agent orchestration is the workflow engine's job. *Mitigation:* keep the driver focused;
  compose it as one node inside a [[P009]] workflow when richer orchestration is needed.

## Value / Effort rationale

**Value H:** unattended run-to-completion with real safety rails is the single most-cited process
gap, and the completion gate turns spec-kit's existing `tasks.md` into an enforceable exit
criterion almost for free. **Effort H:** although the config and completion gate are near-drop-in,
the driver, session-rotation logic, and dual (external + in-harness) delivery are genuine
engineering, and the driver couples to whatever headless transport each harness exposes. Phase 2:
it depends on [[P001]]'s Stop hook and pairs with [[P004]]/[[P006]], so it lands after the Phase-1
process layer is stable.
