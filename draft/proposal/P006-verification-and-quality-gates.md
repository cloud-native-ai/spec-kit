# P006 — Verification & Quality Gates

- **Status:** Draft
- **Pillars:** Workflow/Process · Scripts · Skills
- **Source projects:** intellegix-code-agent-toolkit, superpowers, claude-code-ts
- **Value:** H · **Effort:** M · **Phase:** 1
- **Related:** [[P001]], [[P004]], [[P005]], [[P007]]

## Problem / Gap

spec-kit's Spec-Driven philosophy is built on gates — spec → plan → tasks → analyze → implement
→ review — but the gates between *"the agent says it's done"* and *"it is actually, verifiably
done"* are the weakest links. Today:

- **"Done" is self-declared.** `/speckit.implement` finishes when the agent decides it has
  finished. `tasks.md` has precise `[ ]` / `[X]` / `[~]` sigils and a Definition of Done, and
  `verification-log-template.md` has a rigorous per-Success-Criterion schema — but nothing
  *mechanically rejects* a completion claim while `[ ]` rows remain or SCs are unproven. A
  model can mark everything `[X]` and move on.
- **No completeness audit.** After implementation there is no provider-free scan that catches
  the highest-frequency agent failure mode: code that is *stubbed* (`TODO`, `pass`,
  `NotImplementedError`, empty handlers, `raise NotImplemented`) or shallow relative to the
  task it claims to satisfy.
- **No fresh-evidence discipline.** spec-kit has the verification *log* but no behavioral gate
  forbidding "tests pass" / "it works" claims that were never backed by a command run in the
  current session. This is the exact honesty gap superpowers' `verification-before-completion`
  closes.
- **Single-pass spec/plan review.** `/speckit.plan`, `/speckit.analyze`, `/speckit.review`
  produce artifacts in one pass with no adversarial second look and no multi-perspective
  cross-check, so gaps and over-engineering slip through to implementation.

The research repos independently built a *layered* answer: cheap mechanical gates first
(completion, stub-check), then evidence discipline, then — only for high-value artifacts —
adversarial and multi-model review.

## Proposal

Introduce a **layered gate system**, ordered cheapest-and-most-mechanical first, each layer
adoptable on its own and each expressible as a script + a skill (and, where the host supports
it, wired as a hook via [[P001]] rather than relying on the agent to remember):

1. **Completion Gate** — reject self-declared completion against `tasks.md` + the verification
   log, with anti-evasion (detect a *deleted* checklist / DoD section, not just unchecked
   boxes). Provider-free.
2. **Stub-check Completeness Audit** — a provider-free static scan for stub markers and
   shallow implementations, cross-referenced to the tasks that claim those files.
3. **Verification-before-completion** — a discipline gate/skill: no "passing/works/done" claim
   without fresh command evidence captured in this session.
4. **Adversarial two-pass + multi-model council review** — for `spec.md` / `plan.md`, a
   generate → adversarially-critique → revise → converge loop, optionally fanned across
   several models with a synthesis verdict. This is the only LLM-heavy layer and is opt-in.

Layers 1–2 are pure scripts (fast, deterministic, CI-friendly). Layer 3 is a skill plus a
one-line hook reminder. Layer 4 is a skill + template. None disturbs the main `/speckit.*`
flow until promoted; all land in `draft/` first.

## Design sketch

### Layer 1 — Completion Gate (`scripts/python/completion_gate.py`)

Runs against a feature's `tasks.md` + `verification.md`. Exit non-zero (block) when completion
is claimed but unmet.

```
completion_gate.py check <KEY>
  -> reads .specify/specs/<KEY>/tasks.md and verification.md
  -> FAIL if any '^- \[ \]' (open) task row remains
  -> FAIL if DoD "Status:" != green while completion is asserted
  -> FAIL if any SC-NNN_status is fail/unknown  (partial/deferred allowed w/ reason)
  -> ANTI-EVASION:
       * FAIL if the "## Definition of Done" heading is missing (was it deleted?)
       * FAIL if a task row was flipped [ ]->[X] with no matching verification evidence
       * count repeated false-completions in events.jsonl; N in a row => hard stop
  -> PASS only when: zero [ ] rows, DoD green, every SC pass|partial|deferred(w/ reason)
```

Output is machine-parseable (`{"status":"pass|reject","reasons":[...],"open_tasks":[...]}`) so
it can be the exit condition of [[P005]]'s loop, a standalone `specify check-gate`, or a
[[P001]] `Stop` hook. Anti-evasion is the crucial borrow from intellegix: an agent that can't
finish sometimes *deletes the gate* — so a missing gate section is itself a rejection, and
repeated bogus "PROJECT_COMPLETE" claims convert into a stagnation stop.

### Layer 2 — Stub-check Audit (`scripts/python/stub_check.py`)

Three phases, entirely local (Grep/Glob + light heuristics), no model call:

```
Phase 1  pattern scan over changed files (git diff --name-only against baseline_commit):
         TODO | FIXME | XXX | \bpass\b (lone) | NotImplementedError | raise NotImplemented
         | return null/None (stub) | empty {} / :\n    ... | "throw new Error('not impl')"
Phase 2  depth check: for each file a task in tasks.md claims to have implemented, flag
         functions/classes whose body is <= K lines or is only a docstring/pass
Phase 3  cross-reference: map each [X] task -> its declared files (P004 `files` field or the
         path in the task description); report [X] tasks whose files still contain stubs
Output:  stub-report.md + JSON severity buckets {critical|shallow|skeletal}
```

Deliberately provider-free per the mining reports — it is a completeness *scanner*, and one
optional summarization pass can turn the JSON into prose. Pairs with `/speckit.analyze`.

### Layer 3 — Verification-before-completion (skill + hook)

Port superpowers' `verification-before-completion` as `draft/skills/verification-before-completion/`
with spec-kit's calmer tone. Core rule and gate function:

```
Iron rule: a completion/"passing"/"works" claim MUST be preceded, in THIS session, by:
   run the command  ->  read its actual output  ->  then (and only then) make the claim.
Red-flag phrases that require evidence: "should work", "tests pass", "done", "fixed",
   "verified" — each must point to a captured command + output block in verification.md.
```

It references the existing `templates/verification-log-template.md` (fills `SC-NNN_value=` with
the captured evidence) and can be surfaced as a [[P001]] `Stop` / pre-commit hook reminder:
*"run verification before claiming completion."*

### Layer 4 — Adversarial two-pass + council review (skill + template)

For `spec.md` / `plan.md` (not per-line code), a `verify-and-converge` skill:

```
generate artifact
loop (max 3):
   critique pass on the SAME artifact with rubric:
     score 1-10, strengths, weaknesses, CRITICAL issues, missing-vs-requirements, revised sections
   revise artifact from the critique
   converge when: score >= 8 AND no critical issues
                  OR score gain < 1  OR iteration == 3
```

Optional **council** extension (`draft/skills/council-review/` + a JSON review template): fan
the same prompt to N models the host has access to, then a synthesis step emits strict JSON
(`agreements`, `disagreements` with per-model positions, `unique_insights`,
`recommended_actions` with file paths, `risks`, `confidence`). Provider-agnostic: the transport
is whatever the host harness exposes; the IP is the synthesis prompt + convergence stop rule.

### Ordering & wiring

```
/speckit.plan   --> Layer 4 (verify-and-converge on plan.md)          [opt-in]
/speckit.implement completion  --> Layer 1 completion_gate (blocking)
                                --> Layer 2 stub_check (report; blocking on `critical`)
each completion claim           --> Layer 3 fresh-evidence discipline
/speckit.review                 --> Layer 4 council (opt-in, high-value features)
```

Layers 1–3 are the default quality bar; Layer 4 is opt-in for artifacts worth the model spend.
As [[P001]] hooks, Layers 1–2 run on `Stop`/`PostToolUse` automatically; without hooks they run
as `specify` subcommands or as steps the implement skill invokes.

## Source evidence

- **Completion gate + anti-evasion (deleted gate section, repeated false-completion →
  stagnation)** → `intellegix` `automated-loop/loop_driver.py` `_parse_completion_gate`
  (1152–1179), `_validate_completion_gate` (1181–1199), gate-rejection loop (541–587);
  `config.py` `CompletionGateConfig` (102–110); `_research/intellegix-loop-orchestration.md`
  idea #2 and `_research/intellegix-commands-agents-mcp.md`.
- **Stub-check 3-phase completeness audit, provider-free** → `intellegix`
  `commands/stub-check.md`; `_research/intellegix-commands-agents-mcp.md` idea #5.
- **Verification-before-completion (fresh evidence, red-flag phrases, gate function)** →
  `superpowers` `skills/verification-before-completion/SKILL.md` (Iron Law 654–658, Gate
  Function 662–674, rationalization table 701–710); `_research/superpowers.md` idea #5.
- **Adversarial two-pass + convergence rule (score≥8 & no critical, gain<1, or max 3)** →
  `intellegix` `commands/research-perplexity.md`, `commands/extended-research.md`,
  `commands/council-refine.md` (60–65); `_research/intellegix-commands-agents-mcp.md` idea #1.
- **Multi-model council synthesis JSON schema + judge** → `intellegix`
  `council-automation/synthesis_prompt.md` (1–23); `_research/intellegix-loop-orchestration.md`
  idea #5.
- **Completion & blocked *audits* as evidence-based gates ("PROVE completion")** →
  `claude-code-ts` `src/services/goal/prompts.ts`; `_research/claude-code-ts-agent-core.md`
  idea #1 (the audit prose is the model for Layer 1's rejection language).

## Adoption plan

**Phase 1a — mechanical gates (draft).** Ship `completion_gate.py` and `stub_check.py` as
standalone scripts operating on the existing `tasks.md` + `verification.md` schemas. Validate
against completed specs under `.specify/specs/` (e.g. `016-refactor-tools-command`, which
already records deferred tasks) to confirm the gate accepts legitimate `[~]` deferrals and
rejects fabricated completions. No `/speckit.*` change.

**Phase 1b — discipline skill.** Port `verification-before-completion` into
`draft/skills/`, cross-linked to `templates/verification-log-template.md`. Offer it as a
[[P001]] `Stop`/pre-commit hook reminder for hosts with hooks.

**Phase 1c — adversarial/council (opt-in).** Add `verify-and-converge` and `council-review`
skills + a JSON review template, driven manually first (a reviewer runs the skill on
`plan.md`).

**Promotion.** Once the mechanical gates are proven non-flaky, wire Layer 1 as the completion
condition of `/speckit.implement` and Layer 2 as a `/speckit.analyze` sub-step; expose all four
as [[P001]] hooks. Layer 4 stays opt-in per feature. Everything remains in `draft/` until then;
the main flow is untouched.

## Risks & mitigations

- **False rejections blocking legitimate completion.** Mitigation: gates honor the existing
  `[~]` deferred sigil + `deferred_reason` fields; `partial`/`deferred` SC statuses pass with a
  reason. A documented `--override` with a recorded justification exists for genuine edge cases.
- **Stub-check false positives** (a legitimate `pass`, an intentional stub for a deferred
  task). Mitigation: severity buckets — only `critical` blocks; `shallow`/`skeletal` are
  advisory; cross-reference to `[~]` tasks suppresses expected stubs.
- **Anti-evasion feels adversarial / annoys honest users.** Mitigation: keep spec-kit's calm
  tone (soften superpowers' coercive framing per the mining note); the gate reports *what* is
  unmet with file/line pointers, not accusations; user instructions still take precedence.
- **Council cost & provider coupling.** Mitigation: Layer 4 is opt-in and provider-agnostic —
  it uses whatever models the host exposes and degrades to single-model two-pass if only one is
  available; never ship the Perplexity browser transport from the source.
- **Gate drift from schema changes.** Mitigation: gates read the *documented* fields of
  `tasks.md` / `verification-log-template.md`; a `--self-test` fixture guards the parser.

## Value / Effort rationale

**Value: H.** These gates directly enforce the SDD promise — that specs and tasks *drive and
verify* implementation — and target the single highest-frequency agent failure (claiming done
on stubbed/unverified work). Layers 1–2 are near-free once written and pay off on every run;
they are also the exit condition that makes [[P005]]'s autonomous loop safe.

**Effort: M.** Layers 1–3 are small, self-contained, provider-free scripts + one ported skill
over schemas spec-kit already defines — low effort, immediate value, hence Phase 1. Layer 4's
convergence loop and council synthesis add moderate design surface but are opt-in and can
mature independently, keeping the overall effort at M.
