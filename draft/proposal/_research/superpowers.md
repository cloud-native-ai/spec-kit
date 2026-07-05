# Mining Report: superpowers → spec-kit

Source project: `/cws_work/superpowers` (obra/superpowers — a Claude Code / multi-harness *skills-library methodology* plugin).
Target: `/cws_work/spec-kit` (Spec-Driven Development CLI). Goal: evolve into a universal agent-coding framework unifying SKILLS + COMMANDS + WORKFLOWS + SCRIPTS.
Scope of this report: everything of value in superpowers **except** subagent-driven-development and test-driven-development (already ported into `spec-kit/draft/skills/`).

## Project snapshot

superpowers is a cross-platform plugin (Claude Code, Cursor, Copilot CLI, Codex, Pi, Antigravity) whose entire product is a *library of process skills* plus the machinery to make an agent actually invoke them. Each skill is a `SKILL.md` with YAML frontmatter (`name`, `description` written as a "Use when…" trigger) and heavy behavioral scaffolding — Iron Laws, HARD-GATEs, red-flag/rationalization tables, graphviz decision flows, and quick-reference tables. Skills chain into a pipeline (brainstorming → writing-plans → subagent-driven-development/executing-plans → requesting-code-review → verification-before-completion → finishing-a-development-branch). The linchpin is infra: a **SessionStart hook** (`hooks/session-start` invoked via the polyglot `hooks/run-hook.cmd`) that force-injects the `using-superpowers` bootstrap skill into every conversation, and that bootstrap skill mandates "check for an applicable skill BEFORE any action." This is precisely the *enforcement + discovery* layer spec-kit lacks: spec-kit ships skills but relies on the agent noticing them.

## Skill catalog

| Skill (file) | Purpose | Value to spec-kit (beyond SDD/TDD) |
|---|---|---|
| `skills/using-superpowers/SKILL.md` | Bootstrap meta-skill: "invoke relevant skill before ANY response," skill-priority ordering, red-flag rationalization table, per-platform reference files | HIGH — the discovery/enforcement convention that makes a skill library actually get used |
| `skills/brainstorming/SKILL.md` | Pre-implementation design dialogue: one question at a time, 2-3 approaches, HARD-GATE against coding before approved design, writes+commits a spec, spec self-review | HIGH — a genuine front-door *before* `/speckit.specify`; fills the "vague idea → reviewed spec" gap |
| `skills/writing-plans/SKILL.md` | Turn spec into bite-sized TDD task plan: exact file paths, Consumes/Produces interfaces between tasks, no-placeholders rule, self-review vs spec | HIGH — directly enriches spec-kit's `tasks`/`plan` templates |
| `skills/systematic-debugging/SKILL.md` (+`root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`, `find-polluter.sh`) | Root-cause-first debugging: Iron Law, 4 phases, "3 fixes = question architecture," backward tracing, multi-layer validation, flaky-test fixes | HIGH — spec-kit has *no* debugging methodology; near-total gap, mostly copy-paste |
| `skills/verification-before-completion/SKILL.md` | Gate: "no completion claims without fresh verification evidence"; command→read output→then claim; red-flag phrase list | HIGH — spec-kit has a `verification-log-template.md` but no enforcing gate/skill |
| `skills/requesting-code-review/SKILL.md` (+`code-reviewer.md`) | Dispatch a fresh reviewer subagent with a precise prompt template; severity-categorized output | MED — spec-kit's SDD draft has reviewer prompts; the standalone template + "review early/often" cadence still adds value |
| `skills/receiving-code-review/SKILL.md` | How to *receive* review: verify before implementing, no performative agreement, YAGNI check, push-back protocol | MED-HIGH — genuinely absent; a discipline skill, not just a template |
| `skills/dispatching-parallel-agents/SKILL.md` | Fan out one agent per *independent* problem domain; prompt structure; when NOT to | MED — spec-kit's extensions concept has "fan-out" but no runtime methodology |
| `skills/using-git-worktrees/SKILL.md` | Ensure isolated workspace: detect existing isolation, prefer native tools, git-worktree fallback, baseline-test gate | MED — complements spec-kit's three-tier `git-workflow`; adds per-feature isolation |
| `skills/finishing-a-development-branch/SKILL.md` | Structured completion menu (merge/PR/keep/discard), env detection, provenance-based cleanup, typed discard confirm | MED — clean end-of-workflow bookend |
| `skills/executing-plans/SKILL.md` | Inline (non-subagent) plan execution with checkpoints | LOW-MED — alternative to the already-ported SDD skill for harnesses without subagents |
| `skills/writing-skills/SKILL.md` (+`anthropic-best-practices.md`, `persuasion-principles.md`, `testing-skills-with-subagents.md`) | TDD-for-skills: pressure-test with subagents before deploying | LOW — spec-kit already has create-skills/improve-skills/think-skills; only the *pressure-testing* idea is novel |

Infra (not skills):
| File | Purpose |
|---|---|
| `hooks/hooks.json`, `hooks/hooks-cursor.json` | Register SessionStart hook (matcher `startup\|clear\|compact`) per harness |
| `hooks/run-hook.cmd` | Cross-platform polyglot (cmd.exe batch + bash) wrapper; extensionless script names to dodge Windows auto-`bash` detection |
| `hooks/session-start` | Reads `using-superpowers/SKILL.md`, JSON-escapes it, emits harness-specific context-injection JSON (`additionalContext` / `hookSpecificOutput` / `additional_context`) |

## Top ideas for spec-kit

### 1. SessionStart auto-injection hook that force-loads a bootstrap skill
- **Source evidence:** `hooks/session-start`, `hooks/run-hook.cmd`, `hooks/hooks.json`, `hooks/hooks-cursor.json`.
- **Why it helps:** spec-kit's skills live in `.specify/skills/` and depend on the agent *choosing* to look. This hook guarantees a bootstrap ("here is how to find and use spec-kit skills/commands; check before acting") is injected at every session/clear/compact — the missing enforcement layer for a universal framework. The polyglot wrapper + per-harness JSON output is a solved multi-platform problem (spec-kit already targets Claude/Copilot/Qwen/opencode/Qoder/Cursor).
- **Maps to spec-kit as:** infra (hooks/) + a new bootstrap skill (`.specify/skills/using-speckit/`).
- **Value:** H · **Effort:** M
- **Adoption sketch:** Add a `hooks/` dir + `run-hook.cmd` + `session-start` that injects a short `using-speckit` skill (a spec-kit-flavored `using-superpowers`) listing the `/speckit.*` pipeline and the "check for a skill/command before acting" rule; register per-harness in the plugin manifests. Reuse superpowers' JSON-escape and multi-field emit logic verbatim.

### 2. `brainstorming` skill as the pre-spec design gate
- **Source evidence:** `skills/brainstorming/SKILL.md` (HARD-GATE lines 13-15; checklist lines 21-33; spec self-review 112-120; terminal state → writing-plans line 62).
- **Why it helps:** spec-kit jumps from feature idea to `/speckit.specify`. brainstorming adds the collaborative "one-question-at-a-time, propose 2-3 approaches, get approval, write+commit spec, self-review" front door — decomposing over-scoped requests before a spec is written. Its terminal-state discipline (only next step is writing-plans) is exactly the chaining spec-kit wants.
- **Maps to spec-kit as:** skill + optionally a `/speckit.brainstorm` command feeding `/speckit.specify`.
- **Value:** H · **Effort:** M
- **Adoption sketch:** Port as `.specify/skills/brainstorming/`, retarget spec path to `.specify/specs/<NNN>/…`, and make its terminal state "invoke `/speckit.specify` / writing-plans." Drop the browser visual-companion (heavy, optional).

### 3. `systematic-debugging` skill + three supporting techniques
- **Source evidence:** `skills/systematic-debugging/SKILL.md` (Iron Law line 356; 4 phases; Phase 4.5 "3+ fixes = question architecture" lines 537-551), `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`, `find-polluter.sh`.
- **Why it helps:** Total gap in spec-kit. Root-cause-first + red-flag table + architectural-escape-hatch is high-leverage and largely language-agnostic (examples are TS but the process is universal; spec-kit is Python so re-example lightly).
- **Maps to spec-kit as:** skill (with `references/` for the three techniques).
- **Value:** H · **Effort:** L-M (mostly copy; swap TS examples for pytest/Python).
- **Adoption sketch:** New `.specify/skills/systematic-debugging/` with the three technique files as references; cross-link to the ported TDD skill for Phase-4 failing-test creation.

### 4. `writing-plans` task-decomposition discipline folded into spec-kit's plan/tasks templates
- **Source evidence:** `skills/writing-plans/SKILL.md` — Task Structure with Consumes/Produces interfaces (lines 243-288), "No Placeholders" failures (290-299), Self-Review vs spec (306-316), Execution Handoff (318-336).
- **Why it helps:** spec-kit already has `templates/plan-template.md` and `tasks-template.md`, but superpowers adds concrete rigor: exact file paths, verbatim global constraints, inter-task interface contracts, an explicit "these are plan failures" placeholder blacklist, and a spec-coverage self-review. This is the difference between a plan an agent can execute unattended and one it can't.
- **Maps to spec-kit as:** template enrichment (`tasks-template.md`/`plan-template.md`) + optionally a `writing-plans` skill.
- **Value:** H · **Effort:** M
- **Adoption sketch:** Merge the "No Placeholders" list, the Consumes/Produces interface block, and the self-review checklist into `templates/tasks-template.md`; wire the Execution Handoff to spec-kit's SDD draft skill.

### 5. `verification-before-completion` gate skill (candidate Stop-hook)
- **Source evidence:** `skills/verification-before-completion/SKILL.md` — Iron Law (654-658), Gate Function (662-674), Common Failures table (678-687), rationalization table (701-710).
- **Why it helps:** spec-kit has `verification-log-template.md` and a Test-First constitution principle but no behavioral gate forbidding "done/passing" claims without fresh command evidence. This is cheap, universal honesty enforcement — and pairs naturally with the hook infra (could be a Stop hook reminder).
- **Maps to spec-kit as:** skill + infra (Stop/pre-commit hook reminder) + link into the existing verification-log template.
- **Value:** M-H · **Effort:** L
- **Adoption sketch:** Port the SKILL.md nearly verbatim; reference it from `verification-log-template.md`; optionally add a Stop hook that reminds "run verification before claiming completion."

### 6. `using-superpowers`-style discovery meta-skill + "Use when…" trigger convention + skill-chaining terminal states
- **Source evidence:** `skills/using-superpowers/SKILL.md` (the Rule, Skill Priority, Red Flags table), the `description:` "Use when…" frontmatter convention across every skill, and terminal-state handoffs (brainstorming line 62; writing-plans 318-336).
- **Why it helps:** spec-kit skills already carry rich trigger keyword lists (e.g. `git-workflow`), but there is no *meta* convention that (a) mandates checking, (b) defines process-skill-before-implementation priority, and (c) formalizes one-skill-hands-to-the-next chaining. Standardizing "Use when…" + explicit terminal states turns spec-kit's skills/commands into a composable pipeline — core to the universal-framework goal.
- **Maps to spec-kit as:** convention (skills authoring guide + `create-skills`/`improve-skills` update) + the bootstrap skill from Idea #1.
- **Value:** M-H · **Effort:** M
- **Adoption sketch:** Codify "Use when…" descriptions + a required "Next skill/command" terminal-state field in `skills-template.md` and the create-skills checklist; the bootstrap skill teaches the priority/red-flag rules.

### 7. Code-review pair: reviewer subagent template + `receiving-code-review` discipline
- **Source evidence:** `skills/requesting-code-review/code-reviewer.md` (full reviewer prompt, read-only rules, severity output), `skills/receiving-code-review/SKILL.md` (verify-before-implement, no performative agreement lines 769-788, YAGNI check, push-back protocol).
- **Why it helps:** spec-kit's SDD draft has reviewer prompts (`draft/skills/subagent-driven-development/assets/final-code-reviewer-prompt.md`) but nothing for *receiving* review — the "verify, don't perform agreement, push back with reasoning" discipline is absent and valuable for any agent workflow, plus the standalone read-only reviewer template is reusable outside SDD.
- **Maps to spec-kit as:** skill (`receiving-code-review`) + template (`code-reviewer.md`, complementing `review-template.md`).
- **Value:** M · **Effort:** L
- **Adoption sketch:** Port `receiving-code-review` as a skill; adopt `code-reviewer.md`'s read-only + severity-categorized format into `templates/review-template.md`.

### 8. `using-git-worktrees` + `finishing-a-development-branch` bookends
- **Source evidence:** `skills/using-git-worktrees/SKILL.md` (Step 0 isolation detection incl. submodule guard lines 214-227; ignore-verification 268-274), `skills/finishing-a-development-branch/SKILL.md` (4-option menu 460-483; provenance cleanup 553-574).
- **Why it helps:** spec-kit's `git-workflow` covers three-tier branch sync but not per-feature workspace isolation or a structured completion menu. These bracket the SDD implement phase cleanly and are harness-portable (native-tool-first with git fallback).
- **Maps to spec-kit as:** two skills (or one "feature-lifecycle" skill).
- **Value:** M · **Effort:** L-M
- **Adoption sketch:** Port both; have `using-git-worktrees` run before `/speckit.implement` and `finishing-a-development-branch` after, reconciling with the existing three-tier `git-workflow` doc.

### 9. `dispatching-parallel-agents` methodology
- **Source evidence:** `skills/dispatching-parallel-agents/SKILL.md` (when-to-use flow lines 19-35; agent prompt structure 88-114; "when NOT to use" 130-135).
- **Why it helps:** spec-kit's extensions concept mentions "fan-out" but provides no runtime guidance for splitting independent failures/tasks across concurrent subagents with focused, self-contained prompts. Directly leverages spec-kit's existing agent/triad infrastructure.
- **Maps to spec-kit as:** skill (pairs with the role/triad agents).
- **Value:** M · **Effort:** L
- **Adoption sketch:** Port as a skill; reference from the SDD and systematic-debugging skills for multi-domain failures.

## Notable code/prompts worth copying (file paths)

- `hooks/session-start` — JSON-escape via bash parameter substitution + per-harness context-injection field selection (`additional_context` vs `hookSpecificOutput.additionalContext` vs top-level `additionalContext`). Copy the emit logic wholesale.
- `hooks/run-hook.cmd` — polyglot cmd/bash wrapper + extensionless-script rationale (Windows auto-bash workaround). Reusable for any spec-kit hook.
- `skills/requesting-code-review/code-reviewer.md` — complete read-only reviewer subagent prompt with severity buckets and a worked example.
- `skills/systematic-debugging/defense-in-depth.md` & `root-cause-tracing.md` — the 4-layer validation pattern and backward-tracing recipe (adapt examples to Python).
- `skills/systematic-debugging/find-polluter.sh` — test-bisection script to locate a state-polluting test.
- `skills/systematic-debugging/condition-based-waiting.md` — generic `waitFor` polling pattern to kill flaky arbitrary-timeout tests.
- The frontmatter `description: "Use when…"` convention + red-flag/rationalization *table* format (`using-superpowers`, `verification-before-completion`, `systematic-debugging`) — a reusable authoring pattern for spec-kit's `skills-template.md`.

## Anti-patterns / what to skip

- **Don't re-port SDD/TDD** — already in `draft/skills/`. `executing-plans` is only worth it as a no-subagent fallback.
- **`writing-skills` is largely redundant** — spec-kit already has create-skills/improve-skills/think-skills. Only mine the *pressure-testing-skills-with-subagents* idea, not the whole skill.
- **Skip the browser visual-companion** in brainstorming (`skills/brainstorming/visual-companion.md`, `scripts/`) — heavy, Node-server-based, optional; port the text dialogue flow only.
- **Tone down the coercive framing** — superpowers uses "you have no choice / this is not negotiable / violating the letter is violating the spirit / dishonesty" language. Keep the *gates and checklists* but soften rhetoric to match spec-kit's calmer instruction style; over-strong mandates can backfire and conflict with spec-kit's "user instructions take precedence" model.
- **Don't blindly copy TS/Node examples** — systematic-debugging, condition-based-waiting, and worktree setup assume Node/npm; re-example in Python/pytest since spec-kit is Python.
- **Don't duplicate git mechanics** — reconcile `using-git-worktrees`/`finishing-a-development-branch` with spec-kit's existing three-tier `git-workflow` rather than shipping a conflicting parallel model.
