# Mining Report: claude-code-py → spec-kit

Source analyzed: `/cws_work/claude-code-py` (a Claude Code distribution mirror: docs/config/plugins/examples).
Lens: features/patterns that move spec-kit toward a UNIVERSAL agent-coding framework unifying SKILLS + COMMANDS + WORKFLOWS + SCRIPTS, focusing on hooks, plugins, settings, scripts, enterprise/deployment.

## Project snapshot

claude-code-py bundles a marketplace of 14 first-party plugins (`.claude-plugin/marketplace.json`), each self-contained with a manifest (`.claude-plugin/plugin.json`) that auto-discovers `commands/`, `agents/`, `skills/`, `hooks/`, and `.mcp.json`. Its standout assets are: (1) a full event-driven **hooks system** (PreToolUse, PostToolUse, Stop, SubagentStop, SessionStart/End, UserPromptSubmit, PreCompact, Notification) wired via `hooks.json` and portable `${CLAUDE_PLUGIN_ROOT}` paths; (2) `plugin-dev`, a meta-toolkit of 7 skills that teaches/scaffolds/validates plugins, hooks, and settings; (3) `hookify`, a user-configurable guardrail engine driven by markdown rule files; (4) `ralph-wiggum`, a Stop-hook self-referential loop; and (5) an **enterprise/deployment** layer — layered settings (lax/strict/sandbox), MDM-managed settings (Jamf/Intune/Group Policy templates), and a gateway/GCP reference deployment. spec-kit already has skills/commands/agents/templates/scripts and multi-harness support, so the gaps are precisely hooks, packaging/marketplace, managed settings, and guardrails.

## Top ideas for spec-kit

### 1. Event-driven hooks system (event → script)
- **Idea**: Add a hooks layer so spec-kit can enforce process at lifecycle points — e.g. block `speckit.implement` if no approved plan exists, run a spec-lint on file writes, or verify "tests defined" before a Stop.
- **Source evidence**: `plugins/hookify/hooks/hooks.json`, `plugins/security-guidance/hooks/hooks.json`, `examples/hooks/bash_command_validator_example.py`, `plugins/plugin-dev/skills/hook-development/SKILL.md`.
- **Why it helps**: spec-kit today relies on the agent *choosing* to follow the process (constitution/instructions). Hooks make the workflow *enforceable* deterministically — the missing "PROCESS" pillar of the universal-framework goal. Multi-harness note: Claude Code executes hooks natively; for other harnesses spec-kit ships the scripts + a thin runner.
- **Maps to spec-kit as**: infra + script.
- **Value**: H. **Effort**: M.
- **Adoption sketch**: Define `.specify/hooks/hooks.json` (event → command), a `scripts/bash/run-hook.sh` dispatcher reading JSON on stdin (copy the exit-code contract: 0 ok, 2 = block + stderr fed back to agent), and seed hooks like `pre-implement-requires-plan`, `post-write-spec-lint`, `stop-requires-verification-log` (spec-kit already has `verification-log-template.md`).

### 2. Guardrail rules as markdown files (hookify pattern)
- **Idea**: Let users declare project guardrails as simple markdown-frontmatter rule files instead of code — matcher/condition/action(warn|block)/message — evaluated by one small engine.
- **Source evidence**: `plugins/hookify/core/config_loader.py`, `plugins/hookify/core/rule_engine.py`, `plugins/hookify/commands/hookify.md`, `plugins/hookify/examples/dangerous-rm.local.md`.
- **Why it helps**: spec-kit's constitution encodes *principles*; hookify-style rules encode *enforceable checks* in the same authoring idiom spec-kit already uses (YAML frontmatter + markdown, exactly like its skills/agents/templates). A `/speckit.guardrail` command could even generate rules from conversation frustration signals (the hookify command does this via an analyzer agent).
- **Maps to spec-kit as**: command + script + template.
- **Value**: H. **Effort**: M.
- **Adoption sketch**: Port `rule_engine.py` + `config_loader.py` (self-contained, stdlib-only, ~500 lines) into `scripts/python/`, read rules from `.specify/rules/*.md`, add a `guardrail-rule-template.md` and a `/speckit.guardrail` command. Reuse the block/warn/priority logic verbatim.

### 3. Plugin/marketplace packaging model for distributable spec-kit bundles
- **Idea**: Adopt a manifest + marketplace convention so a team can package a domain-specific spec-kit configuration (its skills + commands + agents + workflows + rules) as an installable, versioned bundle.
- **Source evidence**: `.claude-plugin/marketplace.json`, `plugins/*/.claude-plugin/plugin.json`, `plugins/plugin-dev/skills/plugin-structure/SKILL.md`.
- **Why it helps**: Turns spec-kit from a single repo into an *ecosystem* — the "universal framework" needs a distribution/reuse story. The auto-discovery convention (components at root, manifest in `.claude-plugin/`, portable `${ROOT}` refs) is directly reusable and the categories/versioning give a plugin ecosystem.
- **Maps to spec-kit as**: infra + template.
- **Value**: H. **Effort**: H.
- **Adoption sketch**: Define a `speckit-pack.json` manifest (name/version/author/keywords + component paths), a `marketplace.json` index format, and a `scripts/bash/install-pack.sh`. Ship spec-kit's own skills/commands as the first "pack".

### 4. `plugin-dev`-style meta-toolkit: scaffold + validate spec-kit components
- **Idea**: A bundle of authoring skills + validator scripts + a guided creation command that scaffolds and validates new skills/commands/agents/hooks to a quality bar.
- **Source evidence**: `plugins/plugin-dev/commands/create-plugin.md` (8-phase guided workflow), `plugins/plugin-dev/skills/{plugin-structure,hook-development,plugin-settings,command-development,agent-development}/SKILL.md`, `plugins/plugin-dev/skills/hook-development/scripts/validate-hook-schema.sh` + `test-hook.sh` + `hook-linter.sh`.
- **Why it helps**: spec-kit already has `create-skills`/`create-agent`/`improve-*` skills, but no *validators* or a component-schema linter. The validate/test/lint scripts are copy-ready and raise consistency across a growing framework. `create-plugin.md`'s phased "discovery → planning → clarifying questions → implement → validate → test → document" flow is a strong template for spec-kit's own generators.
- **Maps to spec-kit as**: skill + script + command.
- **Value**: M. **Effort**: M.
- **Adoption sketch**: Add `scripts/bash/validate-component.sh` (frontmatter + structure checks modeled on `validate-hook-schema.sh`) and enrich existing create-* skills with the phased-workflow + validation-agent pattern.

### 5. Layered + managed/enterprise settings with precedence
- **Idea**: A settings hierarchy (managed > project > user) with an enterprise-locked tier that can force policy (allow-only-managed rules/hooks, disable bypass, sandbox).
- **Source evidence**: `examples/settings/{settings-strict,settings-lax,settings-bash-sandbox}.json`, `examples/settings/README.md`, `examples/mdm/managed-settings.json` + `examples/mdm/README.md` (+ macOS `.plist`/`.mobileconfig`, Windows `.admx`/PowerShell templates).
- **Why it helps**: The universal-framework's enterprise gap. Keys like `allowManagedPermissionRulesOnly`, `allowManagedHooksOnly`, `strictKnownMarketplaces`, `disableBypassPermissionsMode` show how to make org policy non-overridable — directly relevant once spec-kit has hooks/packs. spec-kit currently has only `.claude/settings.local.json`.
- **Maps to spec-kit as**: infra + template.
- **Value**: M. **Effort**: M.
- **Adoption sketch**: Define `.specify/settings.json` schema with a precedence resolver in `common.sh`, plus a `managed-settings.json` tier and the three ready-made profile templates (strict/lax/sandbox). MDM/OS-packaging is likely out of scope initially — cite as future.

### 6. Self-referential Stop-loop for iterative workflows (ralph-wiggum)
- **Idea**: A Stop-hook that re-feeds the same task until a completion condition (a `<promise>` string or max-iterations) is met — auto-iterating implement/fix loops.
- **Source evidence**: `plugins/ralph-wiggum/hooks/stop-hook.sh`, `plugins/ralph-wiggum/commands/ralph-loop.md`, and the state-file pattern in `plugins/plugin-dev/skills/plugin-settings/SKILL.md`.
- **Why it helps**: spec-kit workflows (implement-plan, refresh-tools) would benefit from bounded auto-iteration ("keep fixing until verification passes"). The script shows a robust, portable implementation: atomic state-file updates, corruption guards, transcript parsing, `decision:block` + `reason` to re-inject the prompt.
- **Maps to spec-kit as**: script + workflow.
- **Value**: M. **Effort**: M.
- **Adoption sketch**: Requires idea #1 (Stop hooks) first. Add a `.specify/loop.local.md` state file (iteration/max/completion_promise + body prompt) and adapt `stop-hook.sh`.

### 7. SessionStart context-injection + env persistence
- **Idea**: On session start, inject spec-kit's active feature context / constitution reminders as `additionalContext`, and persist detected env (project type, active feature) for the session.
- **Source evidence**: `plugins/explanatory-output-style/hooks-handlers/session-start.sh` (emits `hookSpecificOutput.additionalContext`), hook-development SKILL's `$CLAUDE_ENV_FILE` pattern, spec-kit's existing `scripts/bash/detect-feature-context.sh`.
- **Why it helps**: spec-kit already detects feature context via a script but relies on the harness/agent to load `instructions.md`. A SessionStart hook makes context injection automatic and harness-native, reducing "agent forgot the process" drift.
- **Maps to spec-kit as**: script + infra.
- **Value**: M. **Effort**: L.
- **Adoption sketch**: Wrap `detect-feature-context.sh` output in the `additionalContext` JSON envelope; register as a SessionStart hook once #1 lands.

## Notable code/prompts worth copying (file paths)

- `plugins/hookify/core/rule_engine.py` & `config_loader.py` — self-contained, stdlib-only markdown-rule engine (matcher/condition/action, block>warn priority, per-event output shaping). Near drop-in.
- `plugins/plugin-dev/skills/hook-development/scripts/validate-hook-schema.sh` — thorough JSON/schema/`${ROOT}`/timeout linter; adapt for spec-kit component validation.
- `plugins/plugin-dev/commands/create-plugin.md` — 8-phase guided component-creation workflow (discovery → clarifying questions → validate → test → doc); excellent scaffolding template.
- `plugins/plugin-dev/skills/plugin-settings/SKILL.md` — the `.local.md` frontmatter state-file pattern (parse, quick-exit-if-absent, gitignore, defaults) that unifies config across hooks/commands/agents.
- `plugins/ralph-wiggum/hooks/stop-hook.sh` — robust Stop-loop with atomic writes + corruption guards + transcript JSONL parsing.
- `plugins/security-guidance/hooks/hooks.json` — advanced `asyncRewake`/`rewakeMessage` + `if: "Bash(git commit:*)"` conditional matchers for background review on commit/push (aspirational pattern for spec-kit review gates).
- `examples/settings/settings-strict.json` + `examples/mdm/README.md` — enterprise policy keys and MDM deployment matrix.
- `examples/hooks/bash_command_validator_example.py` — minimal, well-commented PreToolUse validator; ideal starter reference.

## Anti-patterns / what to skip

- **MDM OS-specific packaging** (`examples/mdm/{macos,windows}/*`, `.admx`/`.plist`/PowerShell): heavy, platform-specific, low ROI for spec-kit now. Adopt the *layered settings concept*, defer OS packaging.
- **Gateway/GCP deployment** (`examples/gateway/gcp/*`, Terraform, Dockerfile): tied to Claude Code's proprietary `claude gateway` binary and API-proxy concerns orthogonal to spec-kit's process framework. Not applicable.
- **GitHub issue-triage scripts** (`scripts/*.ts`, `scripts/*.sh`: auto-close-duplicates, sweep, gh.sh): repo-maintenance automation for the Anthropic project itself, not framework features. Skip.
- **hookify's hand-rolled YAML parser** (`config_loader.extract_frontmatter`): brittle re-implementation; if porting, back it with a real YAML lib (spec-kit already uses Python) rather than copying the string-parsing logic.
- **Prompt-based hooks** (LLM-in-the-hook, `type: "prompt"`): powerful but Claude-Code-runtime-specific and non-portable across spec-kit's other harnesses; prefer `type: "command"` scripts for portability.
- **Do NOT re-propose** what spec-kit already has: skills, commands, agents, templates, multi-harness ignore files, per-project `settings.local.json`, create/improve-skill|agent generators.
