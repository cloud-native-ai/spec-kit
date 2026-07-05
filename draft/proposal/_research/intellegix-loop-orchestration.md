# Mining Report: intellegix-code-agent-toolkit → spec-kit

Source project: `/cws_work/intellegix-code-agent-toolkit`
Lens: autonomous loop execution, budget/stagnation control, multi-agent git-worktree orchestration, multi-model council, hooks/rules — as concrete upgrades toward spec-kit's universal SKILLS+COMMANDS+WORKFLOWS+SCRIPTS framework.

## Project snapshot

The intellegix toolkit is a "modular configuration system for Claude Code CLI" whose beating heart is `automated-loop/` — a ~4,000-line Python driver that spawns `claude -p` in a headless NDJSON-streaming loop and autonomously iterates on a project until a completion marker fires or a guardrail trips. It surrounds this with: a **council-automation** subsystem (fan out one question to GPT-5.2 / Claude / Gemini / Sonar via Perplexity, then synthesize with an Opus "extended thinking" judge into structured JSON), a **Perplexity research bridge** used between iterations for web-grounded next-step planning, **git-worktree multi-agent orchestration** (`multi_agent.py` + `/orchestrator-multi`), Claude Code **hooks** (path-guard PreToolUse, time-injection SessionStart/UserPromptSubmit), a language-scoped **rules/** + **patterns/** library, an adversarial **/session-audit** self-scorecard, and a code-enforced read-only **health-check**. Everything is subscription-only (no API keys), Pydantic-validated, and heavily test-covered (377 tests). The single most transferable asset is the loop driver's *decision engine* — how it decides to continue, reset, fall back, or stop — which is exactly the "autonomous loop / budget / stagnation" gap spec-kit has.

## Top ideas for spec-kit

### 1. A generic autonomous loop driver (the continue/stop decision engine)
- **Idea:** Port the loop-control brain of `loop_driver.py` — a headless driver that repeatedly invokes the coding agent, streams structured output, and after each iteration runs an ordered guardrail cascade: budget check → timeout detection → error reset → stagnation check → completion-gate validation → post-validation → next-prompt build. It exits with meaningful codes (0 complete, 1 max-iterations, 2 budget, 3 stagnation).
- **Source evidence:** `automated-loop/loop_driver.py` (`run()` lines 227–673; exit codes 34–37); `automated-loop/config.py` (`LimitsConfig`, `StagnationConfig`, `CompletionGateConfig`); `automated-loop/state_tracker.py`.
- **Why it helps:** spec-kit today is a static, human-in-the-loop `/speckit.*` markdown flow. This gives it the missing *autonomous execution substrate* — run a spec/plan/task set to completion unattended with hard safety rails, the top listed gap.
- **Maps to spec-kit as:** script + infra (a `specify run` loop command wrapping the existing `/speckit.implement` phase).
- **Value:** H · **Effort:** H · **Adoption sketch:** Vendor a slimmed `loop_driver.py` under `scripts/loop/`, replace the Perplexity between-iteration step with spec-kit's own artifacts (spec.md/plan.md/tasks.md as the "next step" source), and make completion = all tasks checked in `tasks.md`. Reuse the Pydantic config verbatim.

### 2. Completion Gate — validate "done" against a checklist, with anti-evasion
- **Idea:** Never trust the agent's self-declared completion. When it emits `PROJECT_COMPLETE`, parse a `## Completion Gate` checklist and reject if any `- [ ]` items remain; count rejections and convert repeated false-completions into a stagnation exit. Detects the evasion case where the agent *deletes* the gate section.
- **Source evidence:** `loop_driver.py` `_parse_completion_gate` (1152–1179), `_validate_completion_gate` (1181–1199), gate-rejection loop (541–587); `config.py` `CompletionGateConfig` (102–110).
- **Why it helps:** spec-kit's `tasks.md` already *is* a checklist — this is a near-free, high-value gate that turns tasks.md into an enforceable exit criterion and stops premature "all done" claims.
- **Maps to spec-kit as:** script + workflow (a gate checker over `tasks.md` used by `/speckit.implement`).
- **Value:** H · **Effort:** L · **Adoption sketch:** A ~40-line checker reading unchecked boxes in the active `tasks.md`; wire it as the completion condition of the loop (idea #1) and/or a standalone `specify check-gate`.

### 3. Stagnation + budget + session-rotation guardrails
- **Idea:** Three orthogonal runaway-prevention mechanisms: (a) **budget** caps per-iteration and total USD; (b) **stagnation** over a sliding window (all-low-turns or all-zero-cost ⇒ first reset the session, then exit code 3 — a two-strike system); (c) **session rotation** — proactively drop the resumed session after N turns / $N / behavioral "context exhaustion" (majority of recent iterations below a turn threshold).
- **Source evidence:** `state_tracker.py` `check_budget` (191–210); `loop_driver.py` `_check_stagnation` (1109–1143), `_should_rotate_session` (1064–1107), two-strike logic (494–530); `config.py` `StagnationConfig` (178–210).
- **Why it helps:** Directly fills spec-kit's "budget/stagnation control" gap. Even for human-driven flows, budget accounting + a "this session is spinning" detector is valuable telemetry.
- **Maps to spec-kit as:** script + infra (part of the loop; `StateTracker` is reusable standalone).
- **Value:** H · **Effort:** M · **Adoption sketch:** Adopt `StateTracker` + `StagnationConfig` as-is; feed it the cost/turn/duration that the agent harness reports per invocation.

### 4. Git-worktree parallel multi-agent orchestration with territory splitting
- **Idea:** Decompose a large plan into N non-overlapping file "territories," give each agent its own git worktree (not a clone, not a subdir), scoped CLAUDE.md, and independent loop; monitor via a dashboard; merge sequentially with `--no-ff` behind a `pre-merge-rollback` tag; auto-resolve shared-file needs via a request queue. Includes an **appropriateness gate** that refuses multi-agent for small/coupled work and falls back to single-agent.
- **Source evidence:** `commands/orchestrator-multi.md` (worktree rationale lines 65–80; appropriateness decision matrix 43–53; territory rules 188–201; staggered launch + TOCTOU note 462–475; merge/rollback 674–753; auto-resolve loop 605–671); `automated-loop/multi_agent.py` (`WorkSplitter.split_for_agents` greedy bin-packing 149–183, `MultiAgentOrchestrator` 204–443).
- **Why it helps:** spec-kit lists "multi-agent parallel orchestration via git worktrees" as a gap. This is a complete, opinionated design — including the failure modes (space-in-path breaks Make, Dropbox sync, lock TTL, staggered launch) most implementations miss.
- **Maps to spec-kit as:** command + workflow + script (`/speckit.orchestrate` over subagent-driven-development, which spec-kit already drafts).
- **Value:** H · **Effort:** H · **Adoption sketch:** Adopt worktrees over spec-kit's existing subagent-driven-development skill; split by the file scopes already declared in `tasks.md`; reuse the appropriateness gate verbatim as a routing preamble.

### 5. Multi-model "council" with a synthesis judge + convergence loop
- **Idea:** For plan/spec review, fan the same prompt to 3 frontier models, then have a stronger model synthesize into strict JSON (`agreements`, `disagreements` w/ per-model positions + assessment, `unique_insights`, `recommended_actions` w/ file paths, `risks`, `confidence`). `/council-refine` loops this until convergence (score ≥ 8 AND no critical issues, OR score-gain < 1, OR max 3 iterations).
- **Source evidence:** `council-automation/synthesis_prompt.md` (JSON schema, 1–23); `commands/council-refine.md` (convergence rule 60–65, scoring query 21–39); example artifact `council-logs/2026-04-21_1105-research-raken-api-command-design.md`.
- **Why it helps:** Fills the "multi-model council cross-checking" gap and gives spec-kit a rigorous *spec/plan-review* stage with a machine-parseable verdict and a principled stop rule.
- **Maps to spec-kit as:** command + template (`/speckit.review`/`/speckit.council`; the JSON schema becomes a review template) + skill.
- **Value:** M · **Effort:** M · **Adoption sketch:** Provider-agnostic: replace the Perplexity/browser transport with whatever multi-model access the target harness has; keep the synthesis prompt + convergence loop, which are the actual IP.

### 6. Adversarial self-audit scorecard with trend tracking
- **Idea:** `/session-audit` compiles session evidence from 6 sources (git diff/log, file mtimes, MEMORY/tasks, tool-call counts, an anti-pattern checklist, prior-audit history) and sends *raw evidence only* to a "hostile senior engineer" judge that must argue the low score first (prosecution/defense → averaged), scored across 8 weighted dimensions varying by session type, with regression alerts vs a rolling 5-session average. Deliberately excludes the agent's own narrative to avoid anchoring bias.
- **Source evidence:** `commands/session-audit.md` (6 sources 48–105; anti-pattern checklist 81–97; adversarial scoring 175–187; weight matrix 164–173; index/trend persistence 265–297).
- **Why it helps:** Fills the "health-check/self-audit" gap with a concrete, bias-aware rubric. The anti-pattern checklist (re-read same file, revert-then-redo, claimed-done-without-verify, enterprise-patterns-on-prototype) is a ready-made quality bar for any agent flow.
- **Maps to spec-kit as:** command + skill + template (a `/speckit.audit` retrospective producing a scorecard artifact).
- **Value:** M · **Effort:** M · **Adoption sketch:** Adopt the checklist + adversarial framing as a skill; persist scorecards to a `.specify/audits/` index mirroring the `audit-index.json` structure.

### 7. Event hooks: PreToolUse path-guard + SessionStart context injection
- **Idea:** Two patterns. (a) A **sentinel-gated PreToolUse guard** — when `.workflow/orchestrator-mode.json` is active, block the orchestrator from editing source/running tests (whitelist markdown + config + specific bash), keeping the orchestrator to "write instructions, launch loops" — *fail-open on any error, zero overhead when no sentinel*. (b) A **SessionStart/UserPromptSubmit hook** that injects authoritative `[TIME SYNC]` so the agent never guesses dates.
- **Source evidence:** `hooks/orchestrator-guard.py` (sentinel read+expiry 56–83, path classification 130–175, bash allow/deny 178–201, fail-open main 204–256); `hooks/inject-time.py` (whole file).
- **Why it helps:** Fills the "event hooks" gap and gives spec-kit a role-enforcement mechanism — e.g. keep a "spec author" agent out of source, or a "reviewer" read-only. The sentinel pattern (role encoded in a cwd-local JSON with TTL, hook enforces) is reusable for any role in spec-kit's role-based agents.
- **Maps to spec-kit as:** infra + script (ship hooks + a `.specify/mode.json` sentinel convention).
- **Value:** M · **Effort:** L · **Adoption sketch:** Ship both hooks in the harness templates; define a spec-kit role→allowed-paths map read by a generalized guard.

### 8. Structured trace + metrics summary per run (observability)
- **Idea:** Every iteration appends a typed event to `.workflow/trace.jsonl` (`loop_start`, `claude_invoke`, `claude_complete` w/ tools_used + files_modified + git-diff stats, `timeout_detected`, `model_fallback`, `stagnation_exit`, `completion_detected`, `loop_end`) with size-based rotation; on exit a `metrics_summary.json` aggregates cost/turns/errors, per-model analytics, tool-usage counts, and files touched. Plus log redaction of API-key patterns.
- **Source evidence:** `loop_driver.py` `_write_trace_event` (128–156), `_write_metrics_summary` (1273–1313), `_capture_git_diff_stats` (916–945); `state_tracker.py` `compute_model_analytics` (239–262); `log_redactor.py`.
- **Why it helps:** Turns spec-kit runs into auditable artifacts (cost per feature, where time went), and the git-diff-stat capture is a cheap per-iteration progress signal that also powers stagnation detection.
- **Maps to spec-kit as:** infra + template (write trace/metrics into the feature's `.specify` dir).
- **Value:** M · **Effort:** L · **Adoption sketch:** Drop-in the trace/redactor modules; emit into the per-feature spec directory so each spec ships with its execution record.

### 9. Model-aware scaling + automatic fallback chain
- **Idea:** Per-model timeout multipliers (opus 2×, haiku 0.5×), per-model max-turn caps (opus 25), and an automatic fallback (opus→sonnet after 2 consecutive timeouts) that reverts after one productive iteration, with exponential-backoff cooldown between timeout retries.
- **Source evidence:** `config.py` `LimitsConfig` model maps (44–71); `loop_driver.py` fallback (393–424), revert (466–481), `_compute_cooldown` (158–164), model-aware turn cap in `_invoke_claude` (685–696).
- **Why it helps:** Practical resilience for any autonomous run under rate limits; the "start on the cheap model, escalate only on failure" policy is a good default for a universal framework.
- **Maps to spec-kit as:** script + infra (loop config).
- **Value:** M · **Effort:** L · **Adoption sketch:** Adopt the config maps; map model names to whatever the target harness exposes.

### 10. Dropbox-safe file-lock registry with TTL crash recovery
- **Idea:** A shared `global_locks.json` write-wait-verify protocol (write lock → sleep sync-delay → re-read → confirm not clobbered) with TTL-based auto-expiry so a crashed agent's locks self-heal, plus per-agent `assigned_files.txt` manifests for fast-path ownership.
- **Source evidence:** `automated-loop/file_locking.py` (`LockRegistry.acquire` 95–169, `_clean_expired_locks` 68–89, `FileManifest` 246–298).
- **Why it helps:** If spec-kit runs agents on a shared filesystem (or the user syncs their repo), this prevents concurrent-write corruption. Even without Dropbox, the TTL crash-recovery + manifest pattern is sound.
- **Maps to spec-kit as:** script (only needed alongside idea #4).
- **Value:** L–M · **Effort:** M · **Adoption sketch:** Prefer worktree isolation (idea #4) which mostly removes the need; keep this only for shared-dir modes. Note: for local git worktrees the whole lock layer is largely redundant (see anti-patterns).

## Notable code/prompts worth copying (file paths)

- `automated-loop/loop_driver.py` — the entire `run()` guardrail cascade and `_invoke_claude` NDJSON-via-tempfile pattern (the tempfile trick at 730–829 works around Node pipe-buffering data loss on kill — worth knowing even if spec-kit uses a different transport).
- `automated-loop/config.py` — copy the Pydantic config tree wholesale; it is the cleanest expression of every knob (limits, stagnation, completion_gate, validation, multi_agent).
- `automated-loop/state_tracker.py` — reusable state + budget + per-model analytics, no loop dependency.
- `council-automation/synthesis_prompt.md` — the multi-model synthesis JSON schema (agreements/disagreements/recommended_actions-with-file_path).
- `commands/session-audit.md` — the anti-pattern checklist (81–97) and adversarial prosecution/defense scoring rubric.
- `commands/orchestrator-multi.md` — the appropriateness decision matrix (43–53), territory rules, and merge/rollback + auto-resolve-shared-header procedure.
- `hooks/orchestrator-guard.py` — the sentinel-gated, fail-open role guard.
- `commands/health-check.md` + `health-check/hc_db.py` design — the "code-enforced read-only boundary" pattern (a single module that *physically* cannot mutate: SQLite `mode=ro`, PG `READ ONLY` txn, hard-refuse) is an excellent model for any spec-kit "safe self-audit" tool.
- `commands/council-refine.md` — the convergence stop rule (score≥8 & no critical, or gain<1, or max 3).
- `automated-loop/research_bridge.py` — the between-iteration "explore codebase → structured next-steps (IMMEDIATE NEXT STEPS / BLOCKERS) → verify plan" prompt structure (287–412), independent of the Perplexity transport.

## Anti-patterns / what to skip

- **Perplexity browser automation (Playwright/Chrome-extension/MCP browser-bridge).** Fragile, subscription/UI-coupled, and orthogonal to spec-kit's goal. Keep the *idea* of a between-iteration research/verify step and the *council synthesis*, but swap the transport for a real multi-model API or the harness's own tools. Skip `mcp-servers/browser-bridge/`, `council_browser.py`, `perplexity-selectors.json`, session-keeper/refresh machinery.
- **Windows-first assumptions.** `taskkill`, `mklink /J` junctions, PowerShell wrappers (`loop_driver.ps1`, `notify.ps1`, `install_keeper_task.ps1`), and "worktree path must have no spaces / avoid Dropbox" are environment-specific; generalize or drop.
- **The Dropbox-sync file-lock layer for local worktrees.** The write-wait-verify + sync-delay complexity exists only because the main repo may live in a synced folder. With real git worktrees on a normal filesystem (idea #4), territory non-overlap already prevents contention — don't port the full lock protocol by default.
- **Fail-open guard as a security boundary.** `orchestrator-guard.py` intentionally allows on any error and defaults to allow for unmatched paths — fine as a *soft role nudge*, but do not present it as enforcement. spec-kit should treat it as guidance, not a sandbox.
- **Domain-specific commands/profiles.** Minecraft MCP, Raken/Perplexity, spreadsheet-audit, pokemon/brain-attic profiles, `construction-bi` agent — ignore; they are the author's private portfolio, not framework material.
- **Hardcoded absolute home paths.** Several commands embed `C:\Users\AustinKidwell\.claude\...` (e.g. health-check row-count history) — must be de-personalized if borrowed.
</content>
</invoke>
